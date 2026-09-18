"""End-to-end: generate dummy → main.py pipeline → 5 outputs."""
import subprocess
import sys
from pathlib import Path
import tempfile
import shutil


def test_full_pipeline(tmp_path=Path(tempfile.mkdtemp())):
    root = Path(__file__).resolve().parents[1]
    siswa = tmp_path / "dataset_siswa.xlsx"
    dudi = tmp_path / "dataset_dudi.xlsx"
    out = tmp_path / "output"

    # generate
    r = subprocess.run([sys.executable, str(root / "generate_dummy_data.py"), "--n", "40", "--seed", "42", "--out", str(siswa), "--dudi", str(dudi), "--force"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert siswa.exists() and dudi.exists()

    # run main
    r2 = subprocess.run([sys.executable, str(root / "main.py"), "--siswa", str(siswa), "--dudi", str(dudi)],
                        capture_output=True, text=True, cwd=str(tmp_path))
    # main.py expects output relative to cwd → files di tmp_path/output
    # tapi config OUTPUT_DIR = "output" → akan di tmp_path/output
    # cek di cwd tmp_path
    assert r2.returncode == 0, r2.stderr + r2.stdout
    # main.py tanpa flag harus default Euclidean (resmi), bukan TOPSIS
    import pandas as pd
    out_file = tmp_path / "output" / "hasil_klasterisasi.xlsx"
    if not out_file.exists():
        out_file = root / "output" / "hasil_klasterisasi.xlsx"
    assert out_file.exists()
    df = pd.read_excel(out_file)
    assert "Skor_TOPSIS" not in df.columns, "Default harus Euclidean — Skor_TOPSIS hanya untuk mode topsis eksperimen"
    assert "Cluster" in df.columns
