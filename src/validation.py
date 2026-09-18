"""validation — silhouette (exclude noise) & qualitative vs Penilaian_Guru."""
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, silhouette_score


def silhouette_score_wrap(X_scaled: np.ndarray, labels: np.ndarray) -> float | None:
    """Silhouette exclude noise. Return None jika <2 cluster (bukan error)."""
    mask = labels != -1
    X_f = X_scaled[mask]
    y_f = labels[mask]
    n_cluster = len(set(y_f)) if len(y_f) else 0
    if n_cluster < 2:
        warnings.warn(f"Silhouette N/A — hanya {n_cluster} cluster (exclude noise)")
        return None
    if len(X_f) != len(y_f) or len(X_f) < 2:
        return None
    try:
        return float(silhouette_score(X_f, y_f))
    except Exception as e:
        warnings.warn(f"Silhouette gagal: {e}")
        return None


def _kategori_from_profil(profil: pd.DataFrame) -> dict[int, str]:
    """Mapping cluster → kategori via skor agregat."""
    mapping: dict[int, str] = {}
    for cl in profil.index:
        row = profil.loc[cl]
        soft = float(row.get("Programming_X", 0)) + float(row.get("Software_X", 0)) + float(row.get("Minat_Programming", 0)) * 20
        net = float(row.get("Jaringan_XI", 0)) + float(row.get("SistemOperasi_XI", 0)) + float(row.get("Minat_Networking", 0)) * 20
        sup = float(row.get("Troubleshooting_XI", 0)) + float(row.get("Keamanan_XI", 0)) + float(row.get("Minat_Support", 0)) * 20
        scores = {"Software": soft, "Network": net, "Support": sup}
        best = max(scores, key=lambda k: scores[k])
        mapping[int(cl)] = best
    return mapping


def qualitative_validation(df_siswa: pd.DataFrame, labels: np.ndarray, profil: pd.DataFrame | None = None):
    """Bandingkan Kategori cluster vs Penilaian_Guru. Return dict atau None jika skip."""
    if "Penilaian_Guru" not in df_siswa.columns:
        warnings.warn("Penilaian_Guru tidak ada — skip validasi kualitatif")
        return None
    if profil is None or profil.empty:
        warnings.warn("Profil kosong — skip mapping kategori")
        return None
    guru_series = df_siswa["Penilaian_Guru"].astype(str).str.strip()
    pred, true = [], []
    mapping = _kategori_from_profil(profil)
    for idx, lab in enumerate(labels):
        if lab == -1:
            continue
        g = str(guru_series.iloc[idx]).strip()
        if not g or g.lower() == "nan":
            continue
        pred.append(mapping.get(int(lab), "Support"))
        true.append(g)
    if not pred:
        warnings.warn("Tidak ada pasangan pred/guru yang valid")
        return None
    pred_n = [p.lower() for p in pred]
    true_n = [t.lower() for t in true]
    n_match = sum(p == t for p, t in zip(pred_n, true_n))
    acc = n_match / len(pred_n) if pred_n else 0
    kappa = None
    try:
        kappa = float(cohen_kappa_score(true_n, pred_n))
    except Exception as e:
        warnings.warn(f"Kappa gagal: {e}")
    return {"accuracy": acc, "kappa": kappa, "n_match": n_match, "n_total": len(pred_n), "mapping": mapping}
