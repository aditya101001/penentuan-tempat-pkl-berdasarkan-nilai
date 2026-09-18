import pandas as pd
import tempfile
from pathlib import Path

from generate_dummy_data import generate_siswa, generate_dudi
from src.data_loader import load_data, validate_input
import config


def test_validate_drops_out_of_range():
    df = generate_siswa(n=10, seed=1)
    df.loc[0, "Programming_X"] = 999
    df.loc[1, "Minat_Programming"] = 99
    df_clean, warns = validate_input(df, is_siswa=True)
    assert len(df_clean) < len(df)
    assert any("di luar" in w for w in warns)


def test_validate_missing_becomes_nan_then_drop():
    df = generate_siswa(n=10, seed=2)
    df.loc[0, "Jaringan_XI"] = "bukan angka"
    # coerce akan jadi NaN lalu di-drop
    df["Jaringan_XI"] = pd.to_numeric(df["Jaringan_XI"], errors="coerce")
    df_clean, _ = validate_input(df, is_siswa=True)
    assert len(df_clean) == 9


def test_load_data_roundtrip(tmp_path: Path = Path(tempfile.mkdtemp())):
    s = tmp_path / "s.xlsx"
    d = tmp_path / "d.xlsx"
    generate_siswa(n=15, seed=3).to_excel(s, index=False)
    generate_dudi().to_excel(d, index=False)
    df_s, df_d, warns = load_data(s, d)
    assert len(df_s) == 15
    assert len(df_d) >= 5
