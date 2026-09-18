import tempfile
from pathlib import Path
import pandas as pd

from generate_dummy_data import generate_siswa, generate_dudi
from src.preprocessing import preprocess, scale_features
from src.dbscan_runner import run_dbscan
from src.profiling import profile_clusters
from src.matching import match_to_dudi
from src.export import export_results
from src.visualization import plot_clusters


def test_export_creates_three_excels(tmp_path=Path(tempfile.mkdtemp())):
    df = generate_siswa(n=20, seed=40)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    labels = run_dbscan(X_scaled, eps=0.9, min_samples=5)
    profil = profile_clusters(df, labels)
    m = match_to_dudi(profil, generate_dudi())
    paths = export_results(df, labels, profil, m, out_dir=tmp_path)
    for p in paths.values():
        assert p.exists()
        assert p.stat().st_size > 0
    # cek kolom hasil
    hasil = pd.read_excel(paths["hasil"])
    assert "Cluster" in hasil.columns and "Kategori" in hasil.columns


def test_export_all_noise_still_creates_files(tmp_path=Path(tempfile.mkdtemp())):
    import numpy as np
    df = generate_siswa(n=10, seed=41)
    labels = np.array([-1] * 10)
    profil = profile_clusters(df, labels)
    assert profil.empty
    m = match_to_dudi(profil, generate_dudi())
    paths = export_results(df, labels, profil, m, out_dir=tmp_path)
    for p in paths.values():
        assert p.exists()


def test_plot_clusters_creates_png(tmp_path=Path(tempfile.mkdtemp())):
    df = generate_siswa(n=20, seed=42)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    labels = run_dbscan(X_scaled, eps=0.9, min_samples=5)
    out = tmp_path / "plot.png"
    plot_clusters(X_scaled, labels, out_path=out)
    assert out.exists()
