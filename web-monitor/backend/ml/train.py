import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
import sys

# Ensure backend dir is in path to find database.py if needed, 
# but here we use raw sqlite for simplicity/speed in script.
DB_PATH = "../compost.db"
# Force absolute path to be safe
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # .../backend/ml
# compost.db is in .../backend (parent of ml)
DB_PATH = os.path.join(BASE_DIR, "..", "compost.db")
# We want to save in .../backend/ml/compost_model.pkl
MODEL_PATH = os.path.join(BASE_DIR, "compost_model.pkl")

def train_model():
    print("[TRAIN] Starting Model Training...")
    
    if not os.path.exists(DB_PATH):
        print(f"[ERR] Database not found at {DB_PATH}")
        return

    # 1. Load Data
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT timestamp, temp_scd, soil_hum, co2 
        FROM compostmeasure 
        ORDER BY timestamp ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if len(df) < 50:
        print("[WARN] Not enough data to train (need at least 50 points).")
        return

    print(f"[DATA] Loaded {len(df)} data points.")

    # 2. Preprocessing & Feature Engineering
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # Target: Predict Temperature IN 1 HOUR
    # We shift the temperature column back by 1 row (assuming ~1 measure/hour? or we resample)
    # If data is irregular, we should ideally resample. Let's assume irregular and simple shift for MVP.
    # A better approach for MVP: Target is NEXT temperature.
    df['target_temp_next'] = df['temp_scd'].shift(-1)
    
    # Features
    df['hour'] = df['timestamp'].dt.hour
    df['is_day'] = df['hour'].apply(lambda h: 1 if 6 <= h <= 20 else 0)
    
    # Drop NAs (last row has no target)
    df = df.dropna()
    
    features = ['temp_scd', 'soil_hum', 'co2', 'hour']
    X = df[features]
    y = df['target_temp_next']
    
    # 3. Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"[OK] Training Complete.")
    print(f"[MSE] MSE: {mse:.4f}")
    print(f"[R2] R² Score: {r2:.4f} (1.0 is perfect)")
    
    # 6. Save Model
    joblib.dump(model, MODEL_PATH)
    print(f"[SAVE] Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
