import tempfile
from pathlib import Path
import numpy as np

from generate_dummy_data import generate_siswa
from src.preprocessing import preprocess, scale_features
from src.dbscan_runner import k_distance_values, suggest_eps, k_distance_graph, run_dbscan


def _X(n=40, seed=42):
    df = generate_siswa(n=n, seed=seed)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    return X_scaled


def test_k_distance_sorted():
    X = _X()
    kd = k_distance_values(X)
    assert len(kd) == len(X)
    assert np.all(kd[:-1] <= kd[1:])


def test_suggest_eps_in_range():
    X = _X()
    kd = k_distance_values(X)
    eps = suggest_eps(kd)
    assert kd[0] <= eps <= kd[-1]


def test_run_dbscan_label_shape():
    X = _X(n=20)
    labels = run_dbscan(X, eps=0.7, min_samples=5)
    assert len(labels) == len(X)


def test_run_dbscan_all_noise_if_eps_tiny():
    X = _X(n=10)
    labels = run_dbscan(X, eps=0.01, min_samples=5)
    assert (labels == -1).all()


def test_run_dbscan_min_samples_gt_n():
    X = _X(n=5)
    labels = run_dbscan(X, eps=0.7, min_samples=10)
    assert (labels == -1).all()


def test_k_distance_graph_creates_file(tmp_path=Path(tempfile.mkdtemp())):
    X = _X(n=20)
    out = tmp_path / "k.png"
    kd, reco = k_distance_graph(X, out_path=out)
    assert out.exists()
    assert out.stat().st_size > 0
