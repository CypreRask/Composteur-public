from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class CompostMeasure(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    frame_id: int
    
    # Gas Sensors (Raw)
    mq137: int
    mq4: int
    mq7: int
    
    # SCD41 (CO2 + Env)
    co2: int
    temp_scd: float
    hum_scd: float
    
    # AHT20 (Env)
    temp_aht: float
    hum_aht: float
    
    # NPK Sensor
    soil_hum: float
    soil_temp: float
    soil_ec: int
    soil_ph: float
    soil_n: int
    soil_p: int
    soil_k: int
    
    # Metadata
    rssi: Optional[int] = None
    snr: Optional[float] = None
