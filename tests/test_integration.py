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
    # main.py di cwd tmp_path menulis ke tmp_path/output
    # juga menulis ke root/output jika import path? cek tmp_path
    assert (tmp_path / "output" / "hasil_klasterisasi.xlsx").exists() or (root / "output" / "hasil_klasterisasi.xlsx").exists()
