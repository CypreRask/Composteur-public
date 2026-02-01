from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import List
from database import get_session, create_db_and_tables
from models import CompostMeasure
from heuristic_engine import analyze_dataframe
import pandas as pd
import os



app = FastAPI(title="Compost Monitor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def on_startup():
    import os
    from database import engine
    from sqlmodel import Session, select
    
    print(f"[DB] DATABASE DEBUG: Looking for DB at: {os.path.abspath('./compost.db')}")
    create_db_and_tables()


    
    with Session(engine) as session:
        count = session.exec(select(CompostMeasure)).all()
        print(f"[DB] DATABASE DEBUG: Found {len(count)} rows in database.")
        if len(count) == 0:
            print("[WARN] WARNING: Database is empty!")
        else:
            print("To ensure data fetch works, checking latest:")
            latest = session.exec(select(CompostMeasure).order_by(CompostMeasure.timestamp.desc()).limit(1)).first()
            print(f"[OK] Latest Entry ID: {latest.id if latest else 'None'}")

@app.get("/api/latest", response_model=CompostMeasure)
def get_latest_measure(session: Session = Depends(get_session)):
    statement = select(CompostMeasure).order_by(CompostMeasure.timestamp.desc()).limit(1)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    
    # --- HEURISTIC ANALYSIS (On-the-fly) ---
    # Fetch last 48h of data for context
    # (In prod this should be cached or async)
    history_query = select(CompostMeasure).order_by(CompostMeasure.timestamp.desc()).limit(200) # Enough for 24h
    history_data = session.exec(history_query).all()
    
    analysis = None
    if history_data:
        # Convert to Pandas
        df = pd.DataFrame([h.dict() for h in history_data])
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        analysis = analyze_dataframe(df)

    response_dict = result.dict()
    if analysis:
        response_dict['heuristic'] = analysis
    else:
        response_dict['heuristic'] = {'score': 50, 'reliability': 'LOW', 'gate_label': 'NO_DATA'}
    
    return response_dict



@app.get("/api/history", response_model=List[CompostMeasure])
def get_history(limit: int = 100, session: Session = Depends(get_session)):
    statement = select(CompostMeasure).order_by(CompostMeasure.timestamp.desc()).limit(limit)
    results = session.exec(statement).all()
    return results

from sqlalchemy import text

@app.get("/api/history/stats")
def get_history_stats(days: int = 30, session: Session = Depends(get_session)):
    """
    Returns aggregated daily stats (Avg Temp, Avg Hum, etc.) for the last X days.
    """
    # SQLite-specific date truncation
    query = text(f"""
        SELECT 
            DATE(timestamp) as day, 
            AVG(temp_scd) as avg_temp, 
            AVG(soil_hum) as avg_hum,
            MIN(temp_scd) as min_temp,
            MAX(temp_scd) as max_temp,
            AVG(co2) as avg_co2
        FROM compostmeasure
        WHERE timestamp >= date('now', '-{days} days')
        GROUP BY day
        ORDER BY day ASC
    """)
    
    results = session.exec(query).all()
    
    # Format as JSON list
    stats = []
    for row in results:
        stats.append({
            "day": row[0],
            "avg_temp": round(row[1] or 0, 1),
            "avg_hum": round(row[2] or 0, 1),
            "min_temp": round(row[3] or 0, 1),
            "max_temp": round(row[4] or 0, 1),
            "avg_co2": int(row[5] or 0)
        })
        
    return stats

@app.get("/api/history/aggregate")
def get_history_aggregate(interval: str = "day", days: int = 30, session: Session = Depends(get_session)):
    """
    Returns aggregated data grouped by 'hour' or 'day'.
    Perfect for high-res charts (Month View = 30 days * 24h = 720 points).
    """
    valid_intervals = {"hour": "%Y-%m-%d %H:00:00", "day": "%Y-%m-%d", "month": "%Y-%m"}
    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail="Invalid interval. Use 'hour' or 'day'.")
    
    date_format = valid_intervals[interval]
    
    # SQL Query: Group by truncated timestamp (bucket)
    query = text(f"""
        SELECT 
            strftime('{date_format}', timestamp) as bucket, 
            AVG(temp_scd) as avg_temp, 
            AVG(hum_scd) as avg_hum,
            AVG(co2) as avg_co2,
            AVG(mq137) as avg_nh3,
            AVG(mq4) as avg_ch4
        FROM compostmeasure
        WHERE timestamp >= date('now', '-{days} days')
        GROUP BY bucket
        ORDER BY bucket ASC
    """)
    
    results = session.exec(query).all()
    
    data = []
    for row in results:
        data.append({
            "timestamp": row[0],
            "temp": round(row[1] or 0, 1),
            "hum": round(row[2] or 0, 1),
            "co2": int(row[3] or 0),
            "nh3": int(row[4] or 0),
            "ch4": int(row[5] or 0)
        })
        
    return data

# --- ML INFERENCE ---
import joblib
import pandas as pd
from pydantic import BaseModel
from datetime import datetime

class PredictionRequest(BaseModel):
    temp_scd: float
    soil_hum: float
    co2: float

model = None
MODEL_PATH = "ml/compost_model.pkl"

@app.on_event("startup")
def load_ml_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        print("[ML] ML Model loaded successfully!")
    except Exception as e:
        print(f"[WARN] Could not load ML model: {e}")

@app.post("/api/predict")
def predict_future(data: PredictionRequest):
    """
    Predicts temperature for the next 12 hours (recursive).
    """
    if not model:
        # Fallback if no model trained yet
        return {"error": "Model not trained", "forecast": []}
    
    forecast = []
    current_temp = data.temp_scd
    current_hour = datetime.now().hour
    
    # Recursive prediction for 12 hours
    for i in range(12):
        next_hour = (current_hour + i + 1) % 24
        
        # Prepare feature vector (must match training columns: temp_scd, soil_hum, co2, hour)
        features = pd.DataFrame([{
            'temp_scd': current_temp,
            'soil_hum': data.soil_hum, # Assume constant for short term
            'co2': data.co2,           # Assume constant
            'hour': next_hour
        }])
        
        # Predict
        next_temp = model.predict(features)[0]
        forecast.append({"hour": next_hour, "temp": round(next_temp, 1)})
        
        # Update current_temp for next step (feedback loop)
        current_temp = next_temp
        
    return {"forecast": forecast}

import httpx
import os

@app.get("/api/weather")
async def get_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    lat = os.getenv("OPENWEATHER_LAT")
    lon = os.getenv("OPENWEATHER_LON")
    
    if not api_key:
        # Mock Response if no key
        return {
            "weather": [{"main": "Clear", "description": "ciel dégagé"}],
            "main": {"temp": 20, "humidity": 50},
            "sys": {"sunrise": 1600000000, "sunset": 1600050000},
            "mock": True
        }
    
    # Using 'weather' endpoint (Current weather data)
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=fr"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
             # Fallback to mock if API fails/quota exceeded
             print(f"Weather API Error: {resp.status_code}")
             return {
                "weather": [{"main": "Clear", "description": "ciel dégagé (fallback)"}],
                "main": {"temp": 15, "humidity": 60},
                "sys": {"sunrise": 0, "sunset": 0},
                "mock": True
            }
        return resp.json()

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Compost Monitor Backend"}
