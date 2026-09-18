import numpy as np
from generate_dummy_data import generate_siswa
from src.preprocessing import preprocess, scale_features


def test_preprocess_selects_feature_cols():
    df = generate_siswa(n=20, seed=10)
    X_raw, cols = preprocess(df)
    assert list(X_raw.columns) == cols
    assert X_raw.shape == (20, 10)


def test_scale_mean_zero_std_one():
    df = generate_siswa(n=30, seed=11)
    X_raw, _ = preprocess(df)
    X_scaled, _ = scale_features(X_raw)
    assert X_scaled.shape == X_raw.shape
    # mean ~0, std ~1
    assert np.allclose(X_scaled.mean(axis=0), 0, atol=1e-9)
    assert np.allclose(X_scaled.std(axis=0, ddof=0), 1, atol=1e-9)


def test_preprocess_raises_on_missing_col():
    df = generate_siswa(n=5, seed=12).drop(columns=["Programming_X"])
    try:
        preprocess(df)
        assert False, "should raise"
    except ValueError as e:
        assert "hilang" in str(e)
