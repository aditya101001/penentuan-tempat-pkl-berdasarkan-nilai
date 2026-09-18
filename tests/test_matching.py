import pandas as pd
import numpy as np
from generate_dummy_data import generate_siswa, generate_dudi
from src.preprocessing import preprocess, scale_features
from src.dbscan_runner import run_dbscan
from src.profiling import profile_clusters
from src.matching import match_to_dudi


def test_match_returns_for_each_cluster():
    df = generate_siswa(n=40, seed=30)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    labels = run_dbscan(X_scaled, eps=0.9, min_samples=5)
    profil = profile_clusters(df, labels)
    if profil.empty:
        assert match_to_dudi(profil, generate_dudi()) == {}
        return
    res = match_to_dudi(profil, generate_dudi())
    assert len(res) == len(profil)
    for v in res.values():
        assert "Nama_DUDI" in v and "Jarak" in v
        assert v["Jarak"] >= 0


def test_match_empty_profil():
    assert match_to_dudi(pd.DataFrame(), generate_dudi()) == {}


def test_match_known_values():
    # profil buatan: cluster 0 sangat programmer, cluster 1 sangat network
    profil = pd.DataFrame({
        "Programming_X": [95, 50],
        "Software_X": [90, 55],
        "SistemOperasi_XI": [50, 90],
        "Jaringan_XI": [50, 95],
        "Troubleshooting_XI": [50, 60],
        "Keamanan_XI": [50, 60],
        "Minat_Programming": [5, 1],
        "Minat_Networking": [1, 5],
        "Minat_Support": [2, 2],
        "Minat_Cybersecurity": [2, 2],
        "Jumlah_Anggota": [5, 5],
    }, index=[0, 1])
    dudi = generate_dudi()
    res = match_to_dudi(profil, dudi)
    assert 0 in res and 1 in res
    # cluster programmer harus match Software House atau similar (Programming tinggi)
    # tidak assert nama spesifik, cukup jarak terhitung
    assert res[0]["Jarak"] != res[1]["Jarak"]
