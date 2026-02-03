
import pandas as pd
import numpy as np
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    import heuristic_engine
except ImportError:
    print("Error: Could not import heuristic_engine.")
    sys.exit(1)

def run_test(name, df_input, expected_checks):
    print(f"\n--- Running Test: {name} ---")
    try:
        # 1. Processing
        df = heuristic_engine._ensure_cols(df_input.copy(), ["timestamp", "co2", "mq137", "mq4", "mq7", "soil_ec"], fill=0.0)
        df = heuristic_engine.detect_spikes(df, cols=["co2", "mq137", "mq4", "mq7", "soil_ec"])
        df = heuristic_engine.compute_indices(df)
        df = heuristic_engine.apply_gating(df)
        df = heuristic_engine.compute_score(df)
        
        last_row = df.iloc[-1]
        
        # 2. Validation
        print(f"OUTPUT: Score={last_row['score']:.2f}, Gate={last_row['gate_code']}, Trend={last_row['cn_trend']}")
        print(f"DETAILS: R1={last_row['R1']:.4f}, R2={last_row['R2']:.4f}, EC_Norm={last_row['ec_norm']:.2f}, dCO2={last_row['dco2_dt']:.2f}, CO2={last_row['co2_ema']:.0f}")

        all_passed = True
        for check_name, check_fn in expected_checks.items():
            result = check_fn(last_row)
            status = "PASS" if result else "FAIL"
            print(f"CHECK {check_name}: {status}")
            if not result:
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"CRASH: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_base_signals(hours=200):
    timestamps = pd.date_range(start="2023-01-01", periods=hours, freq="1H")
    # Healthy baseline
    data = {
        "timestamp": timestamps,
        "co2": np.random.normal(1000, 50, hours),
        "mq137": np.random.normal(5, 1, hours), # Low NH3
        "mq4": np.random.normal(5, 1, hours),   # Low CH4
        "mq7": np.random.normal(5, 1, hours),   # Low CO
        "soil_ec": np.linspace(0.4, 0.6, hours) # Moderate EC
    }
    return pd.DataFrame(data)

def main():
    print("Starting Algorithm Verification (Dynamic Signals)...")
    
    # TEST 1: IDEAL CONDITIONS
    df_ideal = generate_base_signals()
    run_test("Ideal Active Compost", df_ideal, {
        "Score is Healthy (>30)": lambda r: r["score"] > 30,
        "Gate is OK (0)": lambda r: r["gate_code"] == 0
    })

    # TEST 2: ANAEROBIC STEP CHANGE
    # Scenario: Healthy for 150h, then CH4 spikes and stays high
    df_ana = generate_base_signals()
    # Create a step change at index 150
    df_ana.loc[150:, "mq4"] = 250.0 # High CH4
    
    run_test("Anaerobic Step Change", df_ana, {
        "Gate is ANAEROBIC (2)": lambda r: r["gate_code"] == 2,
        "Gate Active is True": lambda r: r["gate_active"] == True
    })

    # TEST 3: INACTIVE FADE
    # Scenario: CO2 fades to ambient over time
    df_inact = generate_base_signals()
    # Ramp down CO2
    for i in range(100, 200):
        df_inact.loc[i, "co2"] = max(420, 1000 - (i-100)*10) # Drop 10ppm per hour until 420
        
    run_test("Inactive Fade", df_inact, {
        "Gate is INACTIVE (3)": lambda r: r["gate_code"] == 3
    })

    # TEST 4: MATURITY
    # Scenario: High Activity -> Low Activity BUT High EC
    df_mat = generate_base_signals()
    # 1. EC rises significantly
    df_mat["soil_ec"] = np.linspace(0.4, 1.5, 200) # Ends high
    # 2. Activity drops in last 24h
    start_drop = 150
    for i in range(start_drop, 200):
         df_mat.loc[i, "co2"] = max(500, 2000 - (i-start_drop)*30) # Precipitous drop
         
    run_test("Mature Condition", df_mat, {
        "Gate is MATURE (1)": lambda r: r["gate_code"] == 1,
        "Gate is NOT Inactive": lambda r: r["gate_code"] != 3
    })
    
    # TEST 5: ZERO/NaN INPUTS (Robustness)
    df_zeros = generate_base_signals(50)
    for col in ["co2", "mq137", "mq4", "mq7", "soil_ec"]:
        df_zeros[col] = 0.0
        
    run_test("Zero Inputs", df_zeros, {
        "Does not crash": lambda r: True,
        "Ratios valid (EPSILON handled)": lambda r: not np.isnan(r["R1"])
    })

if __name__ == "__main__":
    main()
