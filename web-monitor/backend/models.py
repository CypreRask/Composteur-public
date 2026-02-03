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
    co2: int = Field(ge=0, le=10000)      # Max 10.000 ppm
    temp_scd: float = Field(ge=-20, le=100) # -20 to 100°C
    hum_scd: float = Field(ge=0, le=100)    # 0-100%
    
    # AHT20 (Env)
    temp_aht: float = Field(ge=-20, le=100)
    hum_aht: float = Field(ge=0, le=100)
    
    # NPK Sensor
    soil_hum: float = Field(ge=0, le=100)
    soil_temp: float = Field(ge=-20, le=100)
    soil_ec: int = Field(ge=0, le=20000) # Max 20k us/cm
    soil_ph: float = Field(ge=0, le=14)  # pH 0-14
    soil_n: int = Field(ge=0, le=3000)   # Max 3000 mg/kg
    soil_p: int = Field(ge=0, le=3000)
    soil_k: int = Field(ge=0, le=3000)
    
    # Metadata
    rssi: Optional[int] = None
    snr: Optional[float] = None
