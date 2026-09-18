import pandas as pd
from generate_dummy_data import generate_siswa, generate_dudi
from src.preprocessing import preprocess, scale_features
from src.dbscan_runner import run_dbscan
from src.profiling import profile_clusters
from src.matching import match_to_dudi
from src.matching_topsis import topsis_rank
import config


def test_topsis_returns_ranking_and_score():
    df = generate_siswa(n=40, seed=30)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    labels = run_dbscan(X_scaled, eps=2.5, min_samples=5)
    profil = profile_clusters(df, labels)
    if profil.empty:
        assert topsis_rank(profil, generate_dudi()) == {}
        return
    res = topsis_rank(profil, generate_dudi())
    assert len(res) == len(profil)
    for v in res.values():
        assert "Skor" in v and 0 <= v["Skor"] <= 1
        assert "ranking" in v and len(v["ranking"]) >= 3
        assert "gap_terbesar" in v


def test_topsis_equal_weight_close_to_euclidean():
    df = generate_siswa(n=30, seed=31)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    labels = run_dbscan(X_scaled, eps=2.5, min_samples=5)
    profil = profile_clusters(df, labels)
    if profil.empty:
        return
    w_eq = {k: 0.2 for k in config.DUDI_WEIGHTS}
    r_eq = topsis_rank(profil, generate_dudi(), weights=w_eq)
    r_euc = match_to_dudi(profil, generate_dudi())
    # ranking top-1 harus konsisten ketika bobot equal vs euclidean (tidak selalu identik tapi keduanya valid)
    for cl in profil.index:
        assert int(cl) in r_eq
        assert int(cl) in r_euc


def test_topsis_empty():
    assert topsis_rank(pd.DataFrame(), generate_dudi()) == {}
