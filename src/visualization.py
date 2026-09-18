"""visualization — scatter plot cluster (PCA jika >2D)."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA

import config


def plot_clusters(X_scaled: np.ndarray, labels: np.ndarray, out_path: str | Path | None = None):
    """Simpan scatter 2D. Jika dimensi >2 pakai PCA. Noise = 'x' hitam."""
    out_path = Path(out_path) if out_path else config.OUTPUT_FILES["cluster_plot"]
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n_samples = len(X_scaled)
    if n_samples == 0:
        return None

    # reduksi ke 2D
    if X_scaled.shape[1] > 2:
        pca = PCA(n_components=2, random_state=config.RANDOM_STATE)
        X2 = pca.fit_transform(X_scaled)
        xlabel, ylabel = f"PC1 ({pca.explained_variance_ratio_[0]:.0%})", f"PC2 ({pca.explained_variance_ratio_[1]:.0%})"
    else:
        X2 = X_scaled[:, :2] if X_scaled.shape[1] == 2 else np.hstack([X_scaled, np.zeros((n_samples, 1))])[:, :2]
        xlabel, ylabel = config.FEATURE_COLS[0], config.FEATURE_COLS[1] if len(config.FEATURE_COLS) > 1 else "Dim2"

    plt.figure(figsize=(7, 5))
    unique = sorted(set(labels))
    n_col = max(len([u for u in unique if u != -1]), 1)
    try:
        cmap = plt.get_cmap("tab10", n_col)
    except TypeError:
        cmap = plt.cm.get_cmap("tab10", n_col)
    for idx, lab in enumerate(unique):
        mask = labels == lab
        if lab == -1:
            plt.scatter(X2[mask, 0], X2[mask, 1], c="black", marker="x", s=40, label="Noise", alpha=0.7)
        else:
            plt.scatter(X2[mask, 0], X2[mask, 1], c=[cmap(idx)], label=f"Cluster {lab}", alpha=0.8, edgecolors="white", linewidth=0.5, s=50)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title("Hasil Klasterisasi DBSCAN")
    plt.legend(loc="best", fontsize=8)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path
