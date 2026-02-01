function decodeUplink(input) {
  var bytes = input.bytes;
  var data = {};

  if (bytes.length !== 32) {
    return {
      errors: ["Invalid Payload Length"],
    };
  }

  data.frame_id = bytes[0];

  // Little Endian (pour les capteurs MQ, SCD, AHT)
  function readUint16LE(idx) {
    return (bytes[idx] | (bytes[idx+1] << 8));
  }
  
  function readInt16LE(idx) {
    var val = bytes[idx] | (bytes[idx+1] << 8);
    if (val & 0x8000) { val = val - 0x10000; }
    return val;
  }

  // Big Endian (pour NPK uniquement - CORRECTION)
  function readUint16BE(idx) {
    return ((bytes[idx] << 8) | bytes[idx+1]);
  }
  
  function readInt16BE(idx) {
    var val = (bytes[idx] << 8) | bytes[idx+1];
    if (val & 0x8000) { val = val - 0x10000; }
    return val;
  }

  // Gaz MQs (LE)
  data.mq137_raw = readUint16LE(1);
  data.mq4_raw = readUint16LE(3);
  data.mq7_raw = readUint16LE(5);

  // SCD41 (LE)
  data.co2_ppm = readUint16LE(7);
  data.temp_compost_scd = readInt16LE(9) / 100.0;
  data.hum_compost_scd = readUint16LE(11) / 100.0;

  // AHT20 (LE)
  data.temp_air_aht = readInt16LE(13) / 100.0;
  data.hum_air_aht = readUint16LE(15) / 100.0;

  // NPK (BE - CORRIGÉ)
  data.soil_hum = readUint16BE(17) / 10.0;
  data.soil_temp = readInt16BE(19) / 10.0;
  data.soil_ec = readUint16BE(21);
  data.soil_ph = readUint16BE(23) / 10.0;
  data.soil_n = readUint16BE(25);
  data.soil_p = readUint16BE(27);
  data.soil_k = readUint16BE(29);

  return {
    data: data,
    warnings: [],
    errors: []
  };
}
