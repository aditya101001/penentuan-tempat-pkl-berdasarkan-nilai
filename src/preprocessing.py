"""preprocess — pilih fitur inti & StandardScaler."""
import pandas as pd
from sklearn.preprocessing import StandardScaler

import config


def preprocess(df: pd.DataFrame, feature_cols: list[str] | None = None):
    """Ambil FEATURE_COLS, return (X_raw DataFrame, cols_used).

    Raise ValueError jika kolom hilang atau DataFrame kosong.
    """
    cols = feature_cols or config.FEATURE_COLS
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom fitur hilang: {missing}")
    X_raw = df[cols].copy()
    if X_raw.empty:
        raise ValueError("X_raw kosong setelah filter fitur")
    return X_raw, cols


def scale_features(X_raw: pd.DataFrame):
    """StandardScaler fittransform. Return (X_scaled ndarray, scaler)."""
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw.values)
    return X_scaled, scaler
