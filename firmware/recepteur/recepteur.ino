#include <heltec_unofficial.h>
#include <LoRaWAN_ESP32.h>

LoRaWANNode* node;

#define UART_RX 20
#define UART_TX 19

// Frame Definition: Header(1) + Len(1) + Payload(32) + CRC(2) = 36 bytes
#define TOTAL_FRAME_SIZE 36
#define PAYLOAD_SIZE 32

uint8_t buffer[TOTAL_FRAME_SIZE];
uint8_t bufferIndex = 0;
bool syncing = true;
unsigned long lastSerialTime = 0;

// --- CONFIG LORAWAN (Keys to be filled) ---
uint64_t joinEUI = 0x0000000000000000ULL; // YOUR_JOIN_EUI
uint64_t devEUI = 0x0000000000000000ULL;  // YOUR_DEV_EUI
uint8_t appKey[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }; // YOUR_APP_KEY
uint8_t nwkKey[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 }; // YOUR_NWK_KEY (Optional/For ABP)

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

void setup() {
  Serial.begin(115200);
  heltec_setup();
  
  Serial2.begin(9600, SERIAL_8N1, UART_RX, UART_TX);
  Serial.println("\n--- 🏁 RECEIVER SLAVE WAKEUP (V2 Fixed) ---");
  
  // Initialize LoRaWAN
  int16_t state = radio.begin();
  if (state != RADIOLIB_ERR_NONE) {
    Serial.println("❌ Radio Fail");
    goToSleep();
  }

  node = persist.manage(&radio);
  
  // Force OTAA Join if not activated
  if (!node->isActivated()) {
    Serial.println("⚠️ Not Joined! Attempting standard join...");
    Serial.printf("DevEUI: %08X%08X (Check on TTN!)\n", (uint32_t)(devEUI>>32), (uint32_t)devEUI);

    unsigned long startJoin = millis();
    state = node->beginOTAA(joinEUI, devEUI, nwkKey, appKey);
    unsigned long joinDuration = millis() - startJoin;

    if (state == RADIOLIB_ERR_NONE) {
        Serial.printf("✅ Join Success! (Took %lums)\n", joinDuration);
        persist.saveSession(node); // IMMEDIATE SAVE
    } else {
        Serial.printf("❌ Join Failed: %d\n", state);
        // We go to sleep if join fails, hoping next RST will try again better
        goToSleep();
    }
  }

  // Window for UART reception (timeout 10s)
  lastSerialTime = millis();
}

void loop() {
  // Check Timeout (if Master woke us but sent nothing valid)
  if (millis() - lastSerialTime > 15000 && bufferIndex == 0) {
    Serial.println("❌ Timeout waiting for UART. Sleeping.");
    goToSleep();
  }

  while (Serial2.available()) {
    lastSerialTime = millis(); // Refresh timeout on activity
    uint8_t b = Serial2.read();

    if (syncing) {
      if (b == 0xBB) { // Header
        buffer[0] = b;
        bufferIndex = 1;
        syncing = false;
        Serial.print("🔹 Sync! ");
      }
    } else {
      buffer[bufferIndex++] = b;
      
      if (bufferIndex == TOTAL_FRAME_SIZE) {
        // Full Frame Received
        Serial.println("📦 Frame Complete. Verifying CRC...");
        
        // Structure: [BB] [LEN] [PAYLOAD...32...] [CRC_L] [CRC_H]
        // Payload starts at index 2, length 32
        uint8_t* payloadPtr = &buffer[2];
        uint16_t receivedCRC = buffer[34] | (buffer[35] << 8);
        uint16_t calculatedCRC = calculateCRC16(payloadPtr, PAYLOAD_SIZE);
        
        if(receivedCRC == calculatedCRC) {
           Serial.println("✅ CRC Valid! Sending to TTN...");
           sendLoRaWAN(payloadPtr, PAYLOAD_SIZE);
           // After successful send, we sleep immediately
           goToSleep(); 
        } else {
           Serial.printf("❌ CRC Fail (Exp: %04X, Got: %04X). Resetting buffer.\n", calculatedCRC, receivedCRC);
           // We stay awake to try catching the next repetition from Master
           syncing = true;
           bufferIndex = 0;
        }
      }
    }
  }
}

void sendLoRaWAN(uint8_t* data, size_t len) {
  uint8_t downlink[256];
  size_t lenDown = sizeof(downlink);
  
  // Send Uplink
  int16_t state = node->sendReceive(data, len, 1, downlink, &lenDown);
  
  if (state == RADIOLIB_ERR_NONE) {
    Serial.println("📡 Upload Success");
  } else {
    Serial.printf("❌ Upload Fail: %d\n", state);
  }
}

void goToSleep() {
  Serial.println("💤 Deep Sleep (Waiting for RST)...");
  Serial.flush();
  
  // Save Session
  persist.saveSession(node);
  
  // Deep Sleep indefini (L'ESP32 Master nous réveillera via RST)
  heltec_deep_sleep(24 * 3600); 
}
