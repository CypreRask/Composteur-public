from sqlmodel import Session
from database import engine, create_db_and_tables
from models import CompostMeasure
from datetime import datetime, timedelta
import random
import math

def generate_data():
    create_db_and_tables()
    
    with Session(engine) as session:
        # Generate 7 days back
        start_date = datetime.now() - timedelta(days=7)
        
        print("[GEN] Generating 7 days of mock compost data...")
        
        for hour in range(24 * 7):
            current_time = start_date + timedelta(hours=hour)
            
            # --- SIMULATION LOGIC ---
            # Temperature follows a daily cycle
            # Peak at 14:00 (hour 14), Low at 02:00 (hour 2)
            # Base temp + Amplitude * sin()
            day_cycle = math.sin((current_time.hour - 8) * math.pi / 12) 
            
            # Compost Heat (Biological activity adds heat over time + cycle)
            # Random fluctuations
            base_temp = 45.0 + (hour / (24*7)) * 5 # Slowly heating up over the week
            temp_scd = base_temp + (day_cycle * 2) + random.uniform(-0.5, 0.5)
            
            # Ambient follows similar but cooler cycle
            temp_aht = 15.0 + (day_cycle * 5) + random.uniform(-1, 1)
            
            # Humidity (inverse to temp usually)
            hum_scd = 60.0 - (day_cycle * 5) + random.uniform(-2, 2)
            
            # CO2 (Biological activity)
            co2 = 800 + (base_temp * 10) + random.randint(-50, 50)
            
            measure = CompostMeasure(
                timestamp=current_time,
                frame_id=hour,
                
                # Gas
                mq137=100 + random.randint(-10, 10),
                mq4=50 + random.randint(-5, 5),
                mq7=50 + random.randint(-5, 5),
                
                # SCD
                co2=int(co2),
                temp_scd=round(temp_scd, 2),
                hum_scd=round(hum_scd, 2),
                
                # AHT
                temp_aht=round(temp_aht, 2),
                hum_aht=50.0 + random.uniform(-5, 5),
                
                # NPK
                soil_hum=65.0 - (hour/100), # Drying out slowly
                soil_temp=round(temp_scd - 2, 2),
                soil_ec=100 + random.randint(0, 10),
                soil_ph=7.0 + random.uniform(-0.1, 0.1),
                soil_n=150 - int(hour/5),
                soil_p=80,
                soil_k=200
            )
            session.add(measure)
            
        session.commit()
        print(f"[OK] Generated {24*7} data points successfully!")

if __name__ == "__main__":
    generate_data()
