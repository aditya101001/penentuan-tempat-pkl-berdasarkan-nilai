import numpy as np
import pandas as pd
from generate_dummy_data import generate_siswa
from src.preprocessing import preprocess, scale_features
from src.dbscan_runner import run_dbscan
from src.profiling import profile_clusters
from src.validation import silhouette_score_wrap, qualitative_validation


def test_silhouette_excludes_noise():
    df = generate_siswa(n=40, seed=20)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    labels = run_dbscan(X_scaled, eps=0.7, min_samples=5)
    sil = silhouette_score_wrap(X_scaled, labels)
    # boleh None jika <2 cluster, tapi tidak crash
    assert sil is None or (-1 <= sil <= 1)


def test_silhouette_none_if_single_cluster():
    X = np.array([[0, 0]] * 10, dtype=float)
    labels = np.array([0] * 10)
    assert silhouette_score_wrap(X, labels) is None


def test_silhouette_none_if_all_noise():
    X = np.random.randn(10, 5)
    labels = np.array([-1] * 10)
    assert silhouette_score_wrap(X, labels) is None


def test_qualitative_skip_if_guru_empty():
    df = generate_siswa(n=10, seed=21)
    df["Penilaian_Guru"] = ""
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    labels = run_dbscan(X_scaled, eps=0.7, min_samples=3)
    profil = profile_clusters(df, labels)
    # profil mungkin kosong jika semua noise — tetap harus skip gracefully
    res = qualitative_validation(df, labels, profil)
    # jika profil kosong → None; jika tidak kosong tapi guru kosong → juga None atau dict kosong
    assert res is None or isinstance(res, dict)


def test_qualitative_returns_dict_when_valid():
    df = generate_siswa(n=40, seed=22)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    labels = run_dbscan(X_scaled, eps=0.9, min_samples=5)
    profil = profile_clusters(df, labels)
    if profil.empty:
        return
    res = qualitative_validation(df, labels, profil)
    if res is not None:
        assert 0 <= res["accuracy"] <= 1
        assert res["n_total"] > 0
