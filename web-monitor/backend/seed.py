from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import CompostMeasure
import time

def seed():
    create_db_and_tables()
    with Session(engine) as session:
        # Check if empty
        existing = session.exec(select(CompostMeasure)).first()
        if existing:
            print("Database already has data.")
            return

        print("Seeding database with initial data...")
        measure = CompostMeasure(
             timestamp=time.time(),
             temp_scd=45.0,
             hum_scd=60.0,
             co2=1200,
             temp_aht=20.0,
             hum_aht=50.0,
             mq137=100.0,
             mq4=50,       # Added
             mq7=50,       # Added
             frame_id=1,   # Added
             soil_hum=65.0,
             soil_temp=40.0,
             soil_ec=100,  # Added
             soil_ph=7.0,
             soil_n=150.0,
             soil_p=80.0,
             soil_k=200.0
        )
        session.add(measure)
        session.commit()
        print("Done!")

if __name__ == "__main__":
    seed()
