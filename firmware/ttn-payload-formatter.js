/**
 * TTN Payload Formatter - Composteur V2
 * 
 * À copier dans la console The Things Network :
 * Applications → [Votre App] → Payload formatters → Uplink → Custom JavaScript formatter
 * 
 * Structure de la trame (32 bytes):
 * [0]     : Frame ID (uint8)
 * [1-2]   : MQ137 raw (uint16 LE)
 * [3-4]   : MQ4 raw (uint16 LE)  
 * [5-6]   : MQ7 raw (uint16 LE)
 * [7-8]   : CO2 ppm (uint16 LE)
 * [9-10]  : Temp SCD (int16 LE, divisé par 100)
 * [11-12] : Hum SCD (uint16 LE, divisé par 100)
 * [13-14] : Temp AHT (int16 LE, divisé par 100)
 * [15-16] : Hum AHT (uint16 LE, divisé par 100)
 * [17-18] : Soil Hum (uint16 BE, divisé par 10) ⚠️ Big Endian
 * [19-20] : Soil Temp (int16 BE, divisé par 10) ⚠️ Big Endian
 * [21-22] : Soil EC (uint16 BE) ⚠️ Big Endian
 * [23-24] : Soil pH (uint16 BE, divisé par 10) ⚠️ Big Endian
 * [25-26] : Soil N (uint16 BE, mg/kg) ⚠️ Big Endian
 * [27-28] : Soil P (uint16 BE, mg/kg) ⚠️ Big Endian
 * [29-30] : Soil K (uint16 BE, mg/kg) ⚠️ Big Endian
 * [31]    : Padding/Reserved
 * 
 * NOTE IMPORTANTE : Les valeurs NPK sont en Big Endian car le capteur RS485
 * envoie naturellement en MSB-first, et l'ESP32 conserve cet ordre.
 */

function decodeUplink(input) {
  var bytes = input.bytes;
  var data = {};

  if (bytes.length !== 32) {
    return {
      errors: ["Invalid Payload Length: expected 32, got " + bytes.length],
    };
  }

  // Octet 0 : Frame ID (Compteur)
  data.frame_id = bytes[0];

  // Helper Little Endian (pour MQ, SCD, AHT)
  function readUint16LE(idx) {
    return (bytes[idx] | (bytes[idx+1] << 8));
  }
  
  function readInt16LE(idx) {
    var val = bytes[idx] | (bytes[idx+1] << 8);
    if (val & 0x8000) { val = val - 0x10000; }
    return val;
  }
  
  // Helper Big Endian (pour NPK uniquement)
  function readUint16BE(idx) {
    return ((bytes[idx] << 8) | bytes[idx+1]);
  }
  
  function readInt16BE(idx) {
    var val = (bytes[idx] << 8) | bytes[idx+1];
    if (val & 0x8000) { val = val - 0x10000; }
    return val;
  }

  // --- GAZ MQs (Raw ADC values) - Little Endian ---
  data.mq137_raw = readUint16LE(1);  // NH3
  data.mq4_raw = readUint16LE(3);    // CH4 (Méthane)
  data.mq7_raw = readUint16LE(5);    // CO (Monoxyde de carbone)

  // --- SCD41 (Capteur CO2/Temp/Hum dans le compost) - Little Endian ---
  data.co2_ppm = readUint16LE(7);
  data.temp_compost_scd = readInt16LE(9) / 100.0;
  data.hum_compost_scd = readUint16LE(11) / 100.0;

  // --- AHT20 (Temp/Hum air ambiant) - Little Endian ---
  data.temp_air_aht = readInt16LE(13) / 100.0;
  data.hum_air_aht = readUint16LE(15) / 100.0;

  // --- Capteur NPK RS485 (Sol) - BIG ENDIAN ⚠️ ---
  data.soil_hum = readUint16BE(17) / 10.0;    // Humidité sol (%)
  data.soil_temp = readInt16BE(19) / 10.0;    // Température sol (°C)
  data.soil_ec = readUint16BE(21);            // Conductivité électrique (µS/cm)
  data.soil_ph = readUint16BE(23) / 10.0;     // pH
  data.soil_n = readUint16BE(25);             // Azote (mg/kg)
  data.soil_p = readUint16BE(27);             // Phosphore (mg/kg)
  data.soil_k = readUint16BE(29);             // Potassium (mg/kg)

  return {
    data: data,
    warnings: [],
    errors: []
  };
}
