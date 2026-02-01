#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_AHTX0.h>
#include <SensirionI2cScd4x.h>
#include <esp_sleep.h>

// --- PINOUT DEFINITIONS ---
// Power Management
const int PIN_MOSFET = 4;
const int PIN_WAKE_SLAVE = 23; // Send Pulse to Heltec RST

// Multiplexer
const int MUX_S0 = 32;
const int MUX_S1 = 33;
const int MUX_S2 = 25;
const int MUX_S3 = 26;
const int MUX_SIG = 34;

// I2C Sensors
const int I2C1_SDA = 21;
const int I2C1_SCL = 22;
const int I2C2_SDA = 13;
const int I2C2_SCL = 14;

// NPK Sensor (RS485)
const int DE_RE_PIN = 5;
const int RX_PIN_NPK = 16;
const int TX_PIN_NPK = 17;

// Link to Receiver (UART)
const int TX_PIN_LINK = 18;
const int RX_PIN_LINK = 19; 

// --- TIMING CONFIG (PRODUCTION MODE - ~4H CYCLE) ---
const unsigned long PREHEAT_DURATION = 600 * 1000UL; // 10 minutes (600s)
// Sleep = 4 hours
const uint64_t SLEEP_DURATION_US = 4ULL * 60ULL * 60ULL * 1000000ULL; // 4 Hours

// --- OBJECTS ---
Adafruit_AHTX0 aht;
SensirionI2cScd4x scd4x;

// --- DATA STRUCTURE (32 BYTES payload + 2 CRC) ---
struct __attribute__((packed)) CompostFrame {
  uint8_t header;         // 0xBB
  uint8_t len;            // 32
  uint8_t frameCounter;
  
  // Data (31 bytes remaining for payload logic in receiver)
  // Actually we keep the 32 bytes structure for simplicity in payload
  // And wrap it
} frameHeader;

// Actual Payload (32 bytes)
struct __attribute__((packed)) CompostPayload {
  uint8_t frameCounter;
  uint16_t mq137;         
  uint16_t mq4;           
  uint16_t mq7;           
  uint16_t scd_co2;       
  int16_t scd_temp;       
  uint16_t scd_hum;       
  int16_t aht_temp;       
  uint16_t aht_hum;       
  uint16_t npk_hum;       
  int16_t npk_temp;       
  uint16_t npk_ec;        
  uint16_t npk_ph;        
  uint16_t npk_n;         
  uint16_t npk_p;         
  uint16_t npk_k;         
  uint8_t padding; // To reach 32 bytes total with frameCounter
};

CompostPayload payload;

// NPK Query
const byte npkQuery[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x07, 0x04, 0x08};

// CRC16 Function (Poly 0x8005)
uint16_t calculateCRC16(uint8_t *data, size_t len) {
  uint16_t crc = 0xFFFF;
  for (size_t i = 0; i < len; i++) {
    crc ^= data[i];
    for (int j = 0; j < 8; j++) {
      if ((crc & 0x0001) != 0) {
        crc >>= 1;
        crc ^= 0xA001; 
      } else {
        crc >>= 1;
      }
    }
  }
  return crc;
}

void readSensors();
uint16_t readMuxAvg(int channel);
void readNPK();

void setup() {
  Serial.begin(115200);
  Serial.println("\n--- 🏁 STARTING MASTER 4H CYCLE ---");
  // Note: WiFi and Bluetooth are OFF by default if not included/started.
  // No need to explicitly call disable commands unless using those libraries.

  // Init Pins
  pinMode(PIN_MOSFET, OUTPUT); digitalWrite(PIN_MOSFET, HIGH); // START PREHEAT IMMEDIATELY
  pinMode(PIN_WAKE_SLAVE, OUTPUT); digitalWrite(PIN_WAKE_SLAVE, HIGH); // Default High (RST inactive)
  
  pinMode(MUX_S0, OUTPUT); pinMode(MUX_S1, OUTPUT);
  pinMode(MUX_S2, OUTPUT); pinMode(MUX_S3, OUTPUT);
  pinMode(DE_RE_PIN, OUTPUT); digitalWrite(DE_RE_PIN, LOW);

  // Links
  Serial1.begin(9600, SERIAL_8N1, RX_PIN_LINK, TX_PIN_LINK); 
  Serial2.begin(4800, SERIAL_8N1, RX_PIN_NPK, TX_PIN_NPK);   

  // I2C
  Wire.begin(I2C1_SDA, I2C1_SCL);        
  Wire1.begin(I2C2_SDA, I2C2_SCL, 100000); 

  // Init Sensors
  if (!aht.begin(&Wire)) Serial.println("❌ AHT20 Fail");
  
  scd4x.begin(Wire1, SCD41_I2C_ADDR_62);
  scd4x.stopPeriodicMeasurement();
  scd4x.startPeriodicMeasurement();

  // Load Frame Counter from RTC Memory (simulated here by static or lost, 
  // better if we use RTC_DATA_ATTR or handle it by receiver time)
  // For now simple counter
}

RTC_DATA_ATTR int bootCount = 0;

void loop() {
  Serial.printf("🔥 Preheat Start (10 min)... Boot #%d\n", bootCount++);
  
  // 1. Preheat Loop (Active Wait to keep SCD and things running if needed, or Light Sleep)
  // For Simplicity and Extension board safety -> Active Wait with millis
  unsigned long startPreheat = millis();
  while(millis() - startPreheat < PREHEAT_DURATION) {
      // Blink or print every minute?
      if((millis() - startPreheat) % 60000 == 0) Serial.println("... Heating ...");
      delay(10); 
  }

  // 2. Measure All
  Serial.println("📏 Measuring...");
  readSensors();

  // 3. Cut Power
  digitalWrite(PIN_MOSFET, LOW);
  Serial.println("❄️ MOSFET OFF");

  // 4. Wake Slave
  Serial.println("🔔 Waking Slave...");
  digitalWrite(PIN_WAKE_SLAVE, LOW);
  delay(50); // Pulse 50ms
  digitalWrite(PIN_WAKE_SLAVE, HIGH);
  
  // Wait for Slave Boot + OTAA Join
  // Receiver has a 15s timeout. We wait 5s which is enough for restored session.
  // (OTAA initial join can take 5-8s, but session restore is fast)
  Serial.println("⏳ Waiting 5s for Slave Boot...");
  delay(5000); 

  // 5. Build Frame & Send
  uint8_t buffer[64];
  int idx = 0;
  
  buffer[idx++] = 0xBB; // Header
  buffer[idx++] = sizeof(payload); // Len (32)
  memcpy(&buffer[idx], &payload, sizeof(payload));
  idx += sizeof(payload);
  
  uint16_t crc = calculateCRC16((uint8_t*)&payload, sizeof(payload));
  buffer[idx++] = crc & 0xFF;
  buffer[idx++] = (crc >> 8) & 0xFF; // Little Endian CRC in frame

  Serial.printf("📤 Sending %d bytes (CRC: %04X)...\n", idx, crc);
  
  // Repeat 5 times (Safety net)
  for(int i=0; i<5; i++) {
    Serial1.write(buffer, idx);
    Serial1.flush();
    delay(200);
  }

  // 6. Sleep
  Serial.println("💤 Entering Light Sleep (4h)...");
  
  // Power Down SCD41 (Stop Periodic)
  scd4x.stopPeriodicMeasurement();

  Serial1.flush(); // Ensure everything sent
  
  // Configure Wakeup Timer
  esp_sleep_enable_timer_wakeup(SLEEP_DURATION_US);
  
  // Light Sleep (preserves RAM, keeps 3.3V stable usually)
  esp_light_sleep_start();
  
  // After Wakeup -> Restart SCD
  Serial.println("⏰ WAKE UP!");
  scd4x.startPeriodicMeasurement();

  digitalWrite(PIN_MOSFET, HIGH); // Restart Heating immediately
}

void readSensors() {
  // AHT
  sensors_event_t humidity, temp;
  if(aht.getEvent(&humidity, &temp)){
      payload.aht_temp = (int16_t)(temp.temperature * 100);
      payload.aht_hum = (uint16_t)(humidity.relative_humidity * 100);
  } else {
      payload.aht_temp = 0; payload.aht_hum = 0;
  }

  // SCD
  uint16_t co2; float t, h;
  if(!scd4x.readMeasurement(co2, t, h)) {
      payload.scd_co2 = co2;
      payload.scd_temp = (int16_t)(t*100);
      payload.scd_hum = (uint16_t)(h*100);
  }

  // MQs (Averaged)
  payload.mq137 = readMuxAvg(0);
  payload.mq4 = readMuxAvg(1);
  payload.mq7 = readMuxAvg(2);

  // NPK
  readNPK();
}

uint16_t readMuxAvg(int channel) {
  digitalWrite(MUX_S0, bitRead(channel, 0));
  digitalWrite(MUX_S1, bitRead(channel, 1));
  digitalWrite(MUX_S2, bitRead(channel, 2));
  digitalWrite(MUX_S3, bitRead(channel, 3));
  delay(10); 
  
  long sum = 0;
  int samples = 32;
  for(int i=0; i<samples; i++) {
    sum += analogRead(MUX_SIG);
    delay(2);
  }
  return (uint16_t)(sum / samples);
}

void readNPK() {
  while(Serial2.available()) Serial2.read();
  
  digitalWrite(DE_RE_PIN, HIGH);
  Serial2.write(npkQuery, sizeof(npkQuery));
  Serial2.flush();
  digitalWrite(DE_RE_PIN, LOW);

  unsigned long start = millis();
  uint8_t buf[30];
  int i = 0;
  while(millis() - start < 500) {
    if(Serial2.available()) {
       buf[i++] = Serial2.read();
       if(i >= 19) break;
    }
  }

  if (i >= 19) {
    payload.npk_hum = (buf[3] << 8) | buf[4];
    payload.npk_temp = (buf[5] << 8) | buf[6];
    payload.npk_ec = (buf[7] << 8) | buf[8];
    payload.npk_ph = (buf[9] << 8) | buf[10];
    payload.npk_n = (buf[11] << 8) | buf[12];
    payload.npk_p = (buf[13] << 8) | buf[14];
    payload.npk_k = (buf[15] << 8) | buf[16];
  }
}
