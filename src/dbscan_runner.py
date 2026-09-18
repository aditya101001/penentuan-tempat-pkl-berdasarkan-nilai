"""k_distance_graph, suggest_eps, run_dbscan."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors

import config


def k_distance_values(X_scaled: np.ndarray, k: int | None = None) -> np.ndarray:
    """Hitung sorted k-distance untuk tiap titik."""
    k = k or config.K_DISTANCE_K
    # k tidak boleh >= n_samples
    k = min(k, max(1, len(X_scaled) - 1))
    nn = NearestNeighbors(n_neighbors=k)
    nn.fit(X_scaled)
    distances, _ = nn.kneighbors(X_scaled)
    k_dist = distances[:, -1]
    return np.sort(k_dist)


def suggest_eps(k_dist: np.ndarray) -> float:
    """Rekomendasi eps via KneeLocator atau max gradient fallback."""
    # coba kneed
    try:
        from kneed import KneeLocator
        x = np.arange(len(k_dist))
        kl = KneeLocator(x, k_dist, curve="convex", direction="increasing")
        if kl.knee is not None:
            return float(k_dist[kl.knee])
    except Exception:
        pass
    # fallback: max gradient (least-effort elbow)
    if len(k_dist) < 3:
        return float(k_dist[-1]) if len(k_dist) else 0.5
    grads = np.diff(k_dist)
    idx = int(np.argmax(grads))
    # eps di titik setelah lompatan terbesar
    return float(k_dist[min(idx + 1, len(k_dist) - 1)])


def k_distance_graph(X_scaled: np.ndarray, k: int | None = None, out_path: str | Path | None = None, eps_reco: float | None = None):
    """Generate & simpan k-distance graph. Return (k_dist, eps_reco)."""
    k = k or config.K_DISTANCE_K
    out_path = Path(out_path) if out_path else config.OUTPUT_FILES["k_distance"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    k_dist = k_distance_values(X_scaled, k=k)
    reco = eps_reco if eps_reco is not None else suggest_eps(k_dist)

    plt.figure(figsize=(7, 4))
    plt.plot(k_dist, marker=".", markersize=3, linewidth=1)
    plt.axhline(reco, linestyle="--", color="red", label=f"eps reco {reco:.3f}")
    plt.axvline(np.searchsorted(k_dist, reco), linestyle=":", color="red", alpha=0.6)
    plt.xlabel(f"Points sorted by {k}-distance")
    plt.ylabel(f"{k}-distance")
    plt.title(f"k-distance graph (k={k})")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return k_dist, reco


def run_dbscan(X_scaled: np.ndarray, eps: float | None = None, min_samples: int | None = None):
    """Jalankan DBSCAN. Return labels ndarray."""
    eps = eps if eps is not None else config.EPS
    min_samples = min_samples if min_samples is not None else config.MIN_SAMPLES
    # honey: min_samples > n → semua noise, jangan crash
    if min_samples > len(X_scaled):
        return np.full(len(X_scaled), -1, dtype=int)
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(X_scaled)
    return labels
