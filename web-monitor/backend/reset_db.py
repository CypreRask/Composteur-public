import os
from database import engine, create_db_and_tables
from sqlmodel import Session, select
from models import CompostMeasure
import time

DB_FILE = "compost.db"

def reset():
    print(f"Current Working Directory: {os.getcwd()}")
    
    # 1. DELETE DB
    if os.path.exists(DB_FILE):
        try:
            os.remove(DB_FILE)
            print(f"[DEL] Deleted existing {DB_FILE}")
        except Exception as e:
            print(f"[WARN] Could not delete {DB_FILE}: {e}")
            return
    else:
        print(f"[INFO] {DB_FILE} did not exist.")

    # 2. CREATE DB
    print("[NEW] Creating new Database & Tables...")
    create_db_and_tables()

    # 3. SEED
    print("[SEED] Seeding initial data...")
    with Session(engine) as session:
        measure = CompostMeasure(
             timestamp=time.time(),
             
             # Env
             temp_aht=20.5,
             hum_aht=55.0,
             
             # Compost Sensor (SCD)
             temp_scd=45.2,
             hum_scd=62.0,
             co2=1250,
             
             # Gas
             mq137=100,
             mq4=50,
             mq7=50,
             
             # Frame
             frame_id=1,
             
             # NPK (Soil)
             soil_hum=65.0,
             soil_temp=42.0,
             soil_ec=100,
             soil_ph=6.8,
             soil_n=140,
             soil_p=85,
             soil_k=200
        )
        session.add(measure)
        session.commit()
        session.refresh(measure)
        print(f"[OK] Inserted Row ID: {measure.id}")

    # 4. VERIFY
    with Session(engine) as session:
        count = session.exec(select(CompostMeasure)).all()
        print(f"[CHECK] Verification: Found {len(count)} rows in DB.")

if __name__ == "__main__":
    reset()
