import paho.mqtt.client as mqtt
import base64
import json
import csv
import os
import requests
import struct
from datetime import datetime

# === CONFIG TTN MQTT ===
TTN_SERVER = "eu1.cloud.thethings.network"
TTN_PORT = 1883
TTN_APP_ID = "votre-app-id"
TTN_API_KEY = "NNSXS.VOTRE_CLÉ_API_ICI.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# === CONFIG OpenWeatherMap (Nice centre) ===
OWM_API_KEY = "votre_clé_api_openweathermap"
LATITUDE = 43.7102
LONGITUDE = 7.2620

# === Préparation du répertoire de stockage ===
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data") # Relative path
os.makedirs(DATA_DIR, exist_ok=True)

# === Fonction de parsing de la nouvelle trame 32 octets (V2) ===
def parse_payload(payload_bytes):
    if len(payload_bytes) != 32:
        print(f"⚠️ Erreur: taille de trame incorrecte ({len(payload_bytes)} vs 32 attendus)")
        return None

    try:
        # Structure Little Endian (<)
        # B = u8 (header)
        # B = u8 (frame)
        # H = u16 (mq137)
        # H = u16 (mq4)
        # H = u16 (mq7)
        # H = u16 (scd_co2)
        # h = i16 (scd_temp)
        # H = u16 (scd_hum)
        # h = i16 (aht_temp)
        # H = u16 (aht_hum)
        # H = u16 (npk_hum)
        # h = i16 (npk_temp)
        # H = u16 (npk_ec)
        # H = u16 (npk_ph)
        # H = u16 (npk_n)
        # H = u16 (npk_p)
        # H = u16 (npk_k)
        
        values = struct.unpack('<BBHHHHhHhHHHHHHH', payload_bytes)
        
        # Extraction
        header = values[0] # Should be 0xBB
        frame = values[1]
        
        data = {
            "frame": frame,
            "mq137": values[2],
            "mq4": values[3],
            "mq7": values[4],
            "co2": values[5],
            "temp_scd": values[6] / 100.0,
            "hum_scd": values[7] / 100.0,
            "temp_aht": values[8] / 100.0,
            "hum_aht": values[9] / 100.0,
            "soil_hum": values[10] / 10.0,
            "soil_temp": values[11] / 10.0,
            "soil_ec": values[12],
            "soil_ph": values[13] / 10.0,
            "soil_n": values[14],
            "soil_p": values[15],
            "soil_k": values[16]
        }
        
        return data
        
    except Exception as e:
        print(f"Parsing error: {e}")
        return None

# === Récupération météo externe ===
def get_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={OWM_API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['main']['temp'], data['main']['humidity'], data['main']['pressure']
    except Exception as e:
        print(f"Erreur météo: {e}")
        return None, None, None

# === Sauvegarde CSV ===
def save_to_csv(timestamp, data, weather):
    date_str = timestamp.strftime("%Y-%m-%d")
    filename = os.path.join(DATA_DIR, f"data_v2_{date_str}.csv")
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        headers = [
            "timestamp", "frame", 
            "mq137", "mq4", "mq7", 
            "co2", "temp_compost", "humidity_compost", # Using SCD as main compost internal
            "temp_aht", "humidity_aht",
            "soil_temp", "soil_hum", "soil_ec", "soil_ph", "soil_n", "soil_p", "soil_k",
            "temp_ext", "humidity_ext", "pressure_ext"
        ]
        
        if not file_exists:
            writer.writerow(headers)
            
        row = [
            timestamp.isoformat(), data['frame'],
            data['mq137'], data['mq4'], data['mq7'],
            data['co2'], data['temp_scd'], data['hum_scd'],
            data['temp_aht'], data['hum_aht'],
            data['soil_temp'], data['soil_hum'], data['soil_ec'], data['soil_ph'], data['soil_n'], data['soil_p'], data['soil_k'],
            weather[0], weather[1], weather[2]
        ]
        writer.writerow(row)

# === Callback MQTT ===
def on_connect(client, userdata, flags, rc):
    print("Connecté à TTN MQTT")
    client.subscribe(f"v3/{TTN_APP_ID}@ttn/devices/+/up")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        raw_payload_b64 = payload['uplink_message']['frm_payload']
        payload_bytes = base64.b64decode(raw_payload_b64)

        data = parse_payload(payload_bytes)
        if data:
            timestamp = datetime.utcnow()
            weather = get_weather()
            
            print(f"📥 {timestamp} | Fr:{data['frame']} | CO2:{data['co2']} | T_Soil:{data['soil_temp']} | MQ137:{data['mq137']}")
            save_to_csv(timestamp, data, weather)
    except Exception as e:
        print(f"Error processing message: {e}")

# === Connexion MQTT ===
client = mqtt.Client()
client.username_pw_set(TTN_APP_ID, TTN_API_KEY)
client.on_connect = on_connect
client.on_message = on_message

client.connect(TTN_SERVER, TTN_PORT, 60)
client.loop_forever()
