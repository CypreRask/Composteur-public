import pandas as pd
import numpy as np

# ============================================================
# COMPOST C/N TREND ENGINE (Kimi report-like)
# Sensors mapping:
# - co2      : CO2 ppm (e.g., SCD41)
# - mq137    : NH3 proxy (MQ137 raw / ppm-estimate if calibrated)
# - mq4      : CH4 proxy (MQ4)
# - mq7      : CO proxy  (MQ7)
# - soil_ec  : EC mS/cm (or proxy)
# ============================================================

# ----------------------------
# CONFIG (defaults you can tune)
# ----------------------------
EPSILON = 10.0  # ppm (avoid divide-by-zero in ratios)

# Resampling
RESAMPLE_RULE = "1h"  # engine expects 1h steps after resample

# EMA smoothing target (in hours on 1H grid)
EMA_HOURS = 24

# Windows on 1H grid
WIN_SHORT = 6          # ~6h
WIN_12H = 12           # ~12h
WIN_48H = 48           # ~48h
WIN_7D = 24 * 7        # 168h

# Gates thresholds
AMBIENT_CO2 = 420.0          # ppm
SEUIL_CO2_BAS_DELTA = 500.0  # ppm above ambient -> "active"
# Inactive gate: CO2_ema < AMBIENT + delta_low. Use a conservative absolute too.
INACTIVE_ABS_CO2 = 600.0     # ppm (fallback)
INACTIVE_REQUIRE_SUM = 40    # out of last 48h

# Anaerobic gate: R2 > max(p90_history, R2_FLOOR)
R2_FLOOR = 0.10
R2_PCTL = 0.90
ANAEROBIC_REQUIRE_SUM = 4    # out of last 6h

# Mature gate (heuristic): EC high + activity dropping
EC_NORM_HIGH = 0.80
DCO2_DROP = -50.0            # ppm over 12h
MATURE_REQUIRE_SUM = 6       # out of last 12h

# Spike detection (robust z using MAD)
SPIKE_WIN = 12        # ~12h
SPIKE_Z = 3.5         # robust z threshold

# Score weights (IMPORTANT: w1 should be NEGATIVE if low score = low C/N when NH3 rises)
POIDS = {"w1": -0.5, "w2": -0.2, "w3": 0.3, "w4": 0.2}

# Category thresholds
TH_LOW = 30
TH_HIGH = 70


# ============================================================
# Helpers
# ============================================================

def _ensure_cols(df: pd.DataFrame, required, fill=0.0) -> pd.DataFrame:
    columns_map = {} # Case insensitivity or mapping? Assuming exact match for now.
    for c in required:
        if c not in df.columns:
            df[c] = fill
    return df

def _to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df

def _resample_1h(df: pd.DataFrame) -> pd.DataFrame:
    # expects timestamp column
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp")
    df = df.set_index("timestamp")
    # median is robust vs spikes; you can choose mean
    # Numeric only for safety
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_resampled = df[numeric_cols].resample(RESAMPLE_RULE).median()
    # fill short gaps
    df_resampled = df_resampled.interpolate(limit=6)  # up to 6h gap (Safe for 4h cycles)
    df_resampled = df_resampled.reset_index()
    return df_resampled

def _rolling_mad(x: pd.Series, window: int) -> pd.Series:
    med = x.rolling(window=window, min_periods=1).median()
    mad = (x - med).abs().rolling(window=window, min_periods=1).median()
    return med, mad

def detect_spikes(df: pd.DataFrame, cols) -> pd.DataFrame:
    df["is_spike"] = False
    for col in cols:
        if col not in df.columns: continue
        s = df[col].astype(float)
        med, mad = _rolling_mad(s, SPIKE_WIN)
        # avoid 0 MAD
        mad_safe = mad.replace(0, np.nan)
        rz = 0.6745 * (s - med) / mad_safe
        spike = rz.abs() > SPIKE_Z
        df["is_spike"] = df["is_spike"] | spike.fillna(False)
    return df


# ============================================================
# CORE
# ============================================================

def compute_indices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input df must be 1H-resampled (or close), with columns:
    ['timestamp','co2','mq137','mq4','mq7','soil_ec'].
    """

    required = ["co2", "mq137", "mq4", "mq7", "soil_ec"]
    df = _ensure_cols(df, required, fill=0.0)

    span = int(max(2, EMA_HOURS))  # on 1H grid

    df["co2_ema"] = df["co2"].ewm(span=span, adjust=False).mean()
    df["nh3_ema"] = df["mq137"].ewm(span=span, adjust=False).mean()
    df["ch4_ema"] = df["mq4"].ewm(span=span, adjust=False).mean()
    df["co_ema"]  = df["mq7"].ewm(span=span, adjust=False).mean()
    df["ec_ema"]  = df["soil_ec"].ewm(span=span, adjust=False).mean()

    # Ratios (normalized by CO2)
    df["R1"] = df["nh3_ema"] / (df["co2_ema"] + EPSILON)
    df["R2"] = df["ch4_ema"] / (df["co2_ema"] + EPSILON)
    df["R3"] = df["co_ema"]  / (df["co2_ema"] + EPSILON)

    # EC normalization via rolling quantiles (7 days)
    ec = df["ec_ema"].astype(float)
    ec_min = ec.rolling(window=WIN_7D, min_periods=1).quantile(0.05)
    ec_max = ec.rolling(window=WIN_7D, min_periods=1).quantile(0.95)
    denom = (ec_max - ec_min).clip(lower=0.1)  # avoid tiny denominators
    df["ec_norm"] = ((ec - ec_min) / denom).clip(lower=0.0, upper=1.5)

    # Activity trend: delta over 12h
    df["dco2_dt"] = df["co2_ema"].diff(periods=WIN_12H)

    return df


def apply_gating(df: pd.DataFrame) -> pd.DataFrame:
    """
    gate_code:
      0 = OK
      1 = MATURE
      2 = ANAEROBIC
      3 = INACTIVE
      4 = SPIKE (pointwise exclusion; doesn't mean biology state)
    """
    df["gate_code"] = 0
    df["gate_active"] = False

    # Gate 4: spikes override pointwise (but keep other codes for sustained states)
    if "is_spike" in df.columns:
        df.loc[df["is_spike"], "gate_code"] = 4
        df.loc[df["is_spike"], "gate_active"] = True

    # -------- Anaerobic gate (R2 high sustained) --------
    # Adaptive threshold: p90 of last 7d of R2 (excluding spikes)
    # BUT we also need an absolute ceiling because if it's always anaerobic, 
    # history will adapt and mask the danger.
    R2_CEILING = 0.20 # 20% CH4/CO2 ratio is definitely anaerobic/dangerous
    
    r2 = df["R2"].astype(float)
    ok_for_thresh = (df["gate_code"] != 4)
    r2_hist = r2.where(ok_for_thresh)
    r2_p90 = r2_hist.rolling(window=WIN_7D, min_periods=24).quantile(R2_PCTL)
    r2_thresh = np.maximum(r2_p90.fillna(R2_FLOOR), R2_FLOOR)

    mask_ana = (r2 > r2_thresh) | (r2 > R2_CEILING)
    ana_sust = mask_ana.rolling(window=WIN_SHORT, min_periods=1).sum() >= ANAEROBIC_REQUIRE_SUM

    # Apply Anaerobic (Priority 2)
    # Use explicit mask so we don't depend on "gate_code==0" check failing after set
    mask_set_ana = ana_sust & (df["gate_code"] == 0)
    df.loc[mask_set_ana, "gate_code"] = 2
    df.loc[mask_set_ana, "gate_active"] = True

    # -------- Mature gate (EC high + activity dropping) --------
    # Priority 1: Mature takes precedence over Inactive
    # If EC is high and activity drops, it's mature, not just dead.
    mask_mature = (df["ec_norm"] > EC_NORM_HIGH) & (df["dco2_dt"] < DCO2_DROP)
    mature_sust = mask_mature.rolling(window=WIN_12H, min_periods=1).sum() >= MATURE_REQUIRE_SUM

    # Apply Mature (can overwrite OK or Anaerobic if we decide maturity explains it better, but usually OK)
    # Let's say Mature overrides Anaerobic? No, Anaerobic is a risk. Mature overrides OK.
    mask_set_mat = mature_sust & (df["gate_code"] != 4) & (df["gate_code"] != 2)
    df.loc[mask_set_mat, "gate_code"] = 1
    df.loc[mask_set_mat, "gate_active"] = True

    # -------- Inactive gate (CO2 too low sustained) --------
    # Priority 3: Only if NOT mature and NOT anaerobic
    co2 = df["co2_ema"].astype(float)
    # FIX: Use AND for absolute fallback to avoid false positives on 'active but lowish' composts
    # OLD: mask_inact = (co2 < (AMBIENT_CO2 + SEUIL_CO2_BAS_DELTA)) | (co2 < INACTIVE_ABS_CO2)
    # NEW: Either very close to ambient OR below absolute floor AND delta check
    # Let's simplify: Inactive means CO2 IS LOW.
    # Strict condition: CO2 must be < 600 OR (CO2 < 900 AND no activity) - effectively similar but let's trust the absolute
    mask_inact = (co2 < INACTIVE_ABS_CO2) 
    inact_sust = mask_inact.rolling(window=WIN_48H, min_periods=1).sum() >= INACTIVE_REQUIRE_SUM

    # Only set Inactive if currently OK (don't overwrite Mature or Anaerobic)
    mask_set_inact = inact_sust & (df["gate_code"] == 0)
    df.loc[mask_set_inact, "gate_code"] = 3
    df.loc[mask_set_inact, "gate_active"] = True

    return df


def compute_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Report-like raw score:
      S = w1*ln(R1+1) + w2*ln(R2+1) + w3*EC_norm + w4*sign(dCO2)*ln(|dCO2|+1)
    Then normalize to 0-100 via quantiles (q05-q95) on valid points (gate_code==0).
    """
    ln_r1 = np.log(df["R1"].clip(lower=0) + 1.0)
    ln_r2 = np.log(df["R2"].clip(lower=0) + 1.0)

    d = df["dco2_dt"].fillna(0.0).astype(float)
    term_d = np.sign(d) * np.log(np.abs(d) + 1.0)

    score_raw = (
        POIDS["w1"] * ln_r1 +
        POIDS["w2"] * ln_r2 +
        POIDS["w3"] * df["ec_norm"].fillna(0.0).astype(float) +
        POIDS["w4"] * term_d
    )
    df["score_raw"] = score_raw

    # Quantile normalization on valid points
    valid = (df["gate_code"] == 0)
    sr_valid = score_raw.where(valid)

    q05 = sr_valid.rolling(window=WIN_7D, min_periods=48).quantile(0.05)
    q95 = sr_valid.rolling(window=WIN_7D, min_periods=48).quantile(0.95)

    # fallback: global if rolling not ready
    if sr_valid.notna().sum() >= 10:
        g05 = sr_valid.quantile(0.05)
        g95 = sr_valid.quantile(0.95)
    else:
        # conservative fallback if almost no data
        g05, g95 = float(score_raw.min()), float(score_raw.max())
        if np.isclose(g05, g95):
            g05, g95 = g05 - 1.0, g95 + 1.0

    q05 = q05.fillna(g05)
    q95 = q95.fillna(g95)

    denom = (q95 - q05).replace(0, np.nan)
    score_norm = 100.0 * (score_raw - q05) / denom
    score_norm = score_norm.replace([np.inf, -np.inf], np.nan).fillna(50.0).clip(0.0, 100.0)

    df["score"] = score_norm

    # Category only if valid
    df["cn_trend"] = "INDETERMINATE"
    df.loc[valid & (df["score"] < TH_LOW), "cn_trend"] = "CN_TOO_LOW"     # excess N, NH3 tends to rise
    df.loc[valid & (df["score"] >= TH_LOW) & (df["score"] <= TH_HIGH), "cn_trend"] = "CN_OPTIMAL"
    df.loc[valid & (df["score"] > TH_HIGH), "cn_trend"] = "CN_TOO_HIGH"  # excess C, activity slows

    # Reliability flag
    df["reliability"] = np.where(df["gate_code"] == 0, "HIGH",
                          np.where(df["gate_code"] == 4, "MEDIUM", "LOW"))

    return df


def analyze_dataframe(df_history: pd.DataFrame) -> dict | None:
    """
    df_history columns expected:
      ['timestamp','co2','mq137','mq4','mq7','soil_ec']
    timestamp can be datetime-like or string.
    """
    if df_history is None or df_history.empty:
        return None

    df = df_history.copy()
    df = _to_datetime(df)
    df = _ensure_cols(df, ["timestamp", "co2", "mq137", "mq4", "mq7", "soil_ec"], fill=0.0)

    # Resample to 1H for stable trend logic
    df = _resample_1h(df)
    
    # If resampling killed all data (e.g. only 1 point), return dummy or fail gracefully
    if df.empty:
        return None

    # Spike detection first (on raw/resampled)
    df = detect_spikes(df, cols=["co2", "mq137", "mq4", "mq7", "soil_ec"])

    # Indices -> gating -> score
    df = compute_indices(df)
    df = apply_gating(df)
    df = compute_score(df)

    if df.empty:
        return None

    latest = df.iloc[-1]

    gate_label = {
        0: "OK",
        1: "MATURE",
        2: "ANAEROBIC",
        3: "INACTIVE",
        4: "SPIKE",
    }.get(int(latest["gate_code"]), "UNKNOWN")

    status = {
        "timestamp": str(latest["timestamp"]),
        "score": round(float(latest["score"]), 1),
        "cn_trend": str(latest["cn_trend"]),
        "gate_code": int(latest["gate_code"]),
        "gate_label": gate_label,
        "reliability": str(latest["reliability"]),
        "R1": round(float(latest["R1"]), 6),
        "R2": round(float(latest["R2"]), 6),
        "R3": round(float(latest["R3"]), 6),
        "ec_norm": round(float(latest["ec_norm"]), 3),
        "dco2_dt": round(float(latest["dco2_dt"]) if pd.notna(latest["dco2_dt"]) else 0.0, 2),
        "is_spike": bool(latest.get("is_spike", False)),
    }
    return status
