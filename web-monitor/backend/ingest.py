import paho.mqtt.client as mqtt
import json
import os
from dotenv import load_dotenv
from sqlmodel import Session
from database import engine, create_db_and_tables
from models import CompostMeasure
from datetime import datetime

# Load Env
load_dotenv(dotenv_path="../.env")

TTN_BROKER = os.getenv("TTN_BROKER")
TTN_PORT = int(os.getenv("TTN_PORT", 1883))
TTN_APP_ID = os.getenv("TTN_APP_ID")
TTN_API_KEY = os.getenv("TTN_API_KEY")

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[OK] Connected to TTN ({rc})")
    client.subscribe(f"v3/{TTN_APP_ID}@ttn/devices/+/up")

def on_message(client, userdata, msg):
    try:
        print(f"[MQTT] MQTT MSG: {msg.topic}") # DEBUG
        payload_str = msg.payload.decode('utf-8')
        # print(payload_str) # Uncomment to see full raw JSON if needed
        data_json = json.loads(payload_str)
        
        # Check if we have decoded payload (from TTN Payload Formatter)
        if 'uplink_message' in data_json and 'decoded_payload' in data_json['uplink_message']:
            decoded = data_json['uplink_message']['decoded_payload']
            metadata = data_json['uplink_message'].get('rx_metadata', [{}])[0]
            
            print(f"[RX] Received Frame #{decoded.get('frame_id', '?')}")
            
            # Map to DB Model
            measure = CompostMeasure(
                timestamp=datetime.utcnow(),
                frame_id=decoded.get('frame_id', 0),
                
                mq137=decoded.get('mq137_raw', 0),
                mq4=decoded.get('mq4_raw', 0),
                mq7=decoded.get('mq7_raw', 0),
                
                co2=decoded.get('co2_ppm', 0),
                temp_scd=decoded.get('temp_compost_scd', 0.0),
                hum_scd=decoded.get('hum_compost_scd', 0.0),
                
                temp_aht=decoded.get('temp_air_aht', 0.0),
                hum_aht=decoded.get('hum_air_aht', 0.0),
                
                soil_hum=decoded.get('soil_hum', 0.0),
                soil_temp=decoded.get('soil_temp', 0.0),
                soil_ec=decoded.get('soil_ec', 0),
                soil_ph=decoded.get('soil_ph', 0.0),
                soil_n=decoded.get('soil_n', 0),
                soil_p=decoded.get('soil_p', 0),
                soil_k=decoded.get('soil_k', 0),
                
                rssi=metadata.get('rssi'),
                snr=metadata.get('snr')
            )
            
            # Save to DB
            with Session(engine) as session:
                session.add(measure)
                session.commit()
                print("[SAVE] Saved to DB")
                
        else:
            print("[WARN] No decoded payload found. Check TTN Payload Formatter.")
            
    except Exception as e:
        print(f"[ERR] Error processing message: {e}")

if __name__ == "__main__":
    create_db_and_tables() # Ensure DB exists
    
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(TTN_APP_ID, TTN_API_KEY)
    client.on_connect = on_connect
    client.on_message = on_message
    
    print(f"[CONN] Connecting to {TTN_BROKER}...")
    client.connect(TTN_BROKER, TTN_PORT, 60)
    client.loop_forever()
