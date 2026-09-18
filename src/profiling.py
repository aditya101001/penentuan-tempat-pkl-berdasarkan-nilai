"""profiling — profile_clusters & detect_noise."""
import pandas as pd
import numpy as np

import config


def profile_clusters(df: pd.DataFrame, labels: np.ndarray, feature_cols: list[str] | None = None) -> pd.DataFrame:
    """Hitung mean per cluster (exclude noise -1). Return DataFrame index=cluster."""
    cols = feature_cols or config.FEATURE_COLS
    df2 = df.copy()
    df2["Cluster"] = labels
    # exclude noise untuk profil
    clustered = df2[df2["Cluster"] != -1]
    if clustered.empty:
        # return empty dengan kolom yang benar
        return pd.DataFrame(columns=cols + ["Jumlah_Anggota"])
    profil = clustered.groupby("Cluster")[cols].mean().round(2)
    counts = clustered.groupby("Cluster").size().rename("Jumlah_Anggota")
    profil = profil.join(counts)
    profil.index.name = "Cluster"
    return profil


def detect_noise(df: pd.DataFrame, labels: np.ndarray) -> pd.DataFrame:
    """Return subset siswa dengan label -1."""
    return df[labels == -1].copy()


def assign_kategori(profil: pd.DataFrame) -> dict[int, str]:
    """Mapping cluster → kategori (Software/Network/Support) via skor agregat."""
    mapping: dict[int, str] = {}
    for cl in profil.index:
        row = profil.loc[cl]
        soft = float(row.get("Programming_X", 0)) + float(row.get("Software_X", 0)) + float(row.get("Minat_Programming", 0)) * 20
        net = float(row.get("Jaringan_XI", 0)) + float(row.get("SistemOperasi_XI", 0)) + float(row.get("Minat_Networking", 0)) * 20
        sup = float(row.get("Troubleshooting_XI", 0)) + float(row.get("Keamanan_XI", 0)) + float(row.get("Minat_Support", 0)) * 20
        scores = {"Software": soft, "Network": net, "Support": sup}
        mapping[int(cl)] = max(scores, key=lambda k: scores[k])
    return mapping
