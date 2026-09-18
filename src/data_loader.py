"""load_data & validate_input — load Excel, cek missing/tipe/rentang."""
import warnings
from pathlib import Path

import pandas as pd

import config

SISWA_REQUIRED = ["ID_Siswa"] + config.FEATURE_COLS
DUDI_REQUIRED = ["Nama_DUDI", "Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"]


def _coerce_numeric(df: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, list[str]]:
    warns = []
    for c in cols:
        if c not in df.columns:
            warns.append(f"Kolom {c} tidak ditemukan")
            continue
        df[c] = pd.to_numeric(df[c], errors="coerce")
        n_nan = df[c].isna().sum()
        if n_nan > 0:
            warns.append(f"{c}: {n_nan} nilai non-numerik → NaN")
    return df, warns


def validate_input(df: pd.DataFrame, is_siswa: bool = True) -> tuple[pd.DataFrame, list[str]]:
    """Validasi rentang & drop baris invalid. Return (df_clean, warnings)."""
    warns: list[str] = []
    if df.empty:
        warns.append("DataFrame kosong")
        return df, warns

    # cek kolom wajib
    required = SISWA_REQUIRED if is_siswa else DUDI_REQUIRED
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        warns.append(f"Kolom wajib hilang: {missing_cols}")

    if is_siswa:
        # rentang nilai 0-100
        nilai_cols = ["Programming_X", "Software_X", "SistemOperasi_XI", "Jaringan_XI", "Troubleshooting_XI", "Keamanan_XI"]
        minat_cols = ["Minat_Programming", "Minat_Networking", "Minat_Support", "Minat_Cybersecurity"]
        for c in nilai_cols:
            if c in df.columns:
                out = ((df[c] < 0) | (df[c] > 100)) & df[c].notna()
                if out.any():
                    warns.append(f"{c}: {out.sum()} nilai di luar 0–100 → baris di-drop")
        for c in minat_cols:
            if c in df.columns:
                out = ((df[c] < 1) | (df[c] > 5)) & df[c].notna()
                if out.any():
                    warns.append(f"{c}: {out.sum()} nilai di luar 1–5 → baris di-drop")

        # drop baris dengan FEATURE_COLS NaN atau out-of-range
        before = len(df)
        # coerce sudah dilakukan caller
        mask_invalid = pd.Series(False, index=df.index)
        for c in config.FEATURE_COLS:
            if c in df.columns:
                if c in nilai_cols:
                    mask_invalid |= (df[c] < 0) | (df[c] > 100) | df[c].isna()
                else:
                    mask_invalid |= (df[c] < 1) | (df[c] > 5) | df[c].isna()
        if mask_invalid.any():
            df = df[~mask_invalid].copy()
            warns.append(f"Drop {mask_invalid.sum()} baris invalid (dari {before} → {len(df)})")
    else:
        dudi_cols = ["Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"]
        for c in dudi_cols:
            if c in df.columns:
                out = ((df[c] < 1) | (df[c] > 5)) & df[c].notna()
                if out.any():
                    warns.append(f"DUDI {c}: {out.sum()} di luar 1–5")

    return df, warns


def load_data(siswa_path: str | Path = config.INPUT_SISWA, dudi_path: str | Path = config.INPUT_DUDI):
    """Load kedua Excel. Return (df_siswa, df_dudi, warnings).

    Tidak crash pada file hilang — raise FileNotFoundError dengan pesan jelas.
    """
    warns: list[str] = []
    siswa_path = Path(siswa_path)
    dudi_path = Path(dudi_path)

    if not siswa_path.exists():
        raise FileNotFoundError(f"File siswa tidak ditemukan: {siswa_path} — jalankan generate_dummy_data.py")
    if not dudi_path.exists():
        raise FileNotFoundError(f"File DUDI tidak ditemukan: {dudi_path} — jalankan generate_dummy_data.py")

    df_siswa = pd.read_excel(siswa_path, sheet_name=0, engine="openpyxl")
    df_dudi = pd.read_excel(dudi_path, sheet_name=0, engine="openpyxl")

    # coerce numeric
    df_siswa, w1 = _coerce_numeric(df_siswa, config.FEATURE_COLS)
    df_dudi, w2 = _coerce_numeric(df_dudi, ["Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"])
    warns.extend(w1)
    warns.extend(w2)

    df_siswa, w3 = validate_input(df_siswa, is_siswa=True)
    df_dudi, w4 = validate_input(df_dudi, is_siswa=False)
    warns.extend(w3)
    warns.extend(w4)

    return df_siswa, df_dudi, warns
