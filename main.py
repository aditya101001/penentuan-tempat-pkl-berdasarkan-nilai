#!/usr/bin/env python3
"""Orkestrasi 12 langkah pipeline DBSCAN PKL.

Usage:
    python main.py
    python main.py --siswa dataset_siswa.xlsx --dudi dataset_dudi.xlsx --eps 0.7 --min-samples 5
"""
import argparse
import warnings
from pathlib import Path

import config
from src.data_loader import load_data
from src.preprocessing import preprocess, scale_features
from src.dbscan_runner import k_distance_graph, run_dbscan
from src.profiling import profile_clusters, detect_noise
from src.validation import silhouette_score_wrap, qualitative_validation
from src.matching import match_to_dudi
from src.matching_topsis import topsis_rank
from src.visualization import plot_clusters
from src.export import export_results


def main(siswa: str = config.INPUT_SISWA, dudi: str = config.INPUT_DUDI,
         eps: float | None = None, min_samples: int | None = None,
         matching: str = "topsis"):
    eps = eps if eps is not None else config.EPS
    min_samples = min_samples if min_samples is not None else config.MIN_SAMPLES

    print("=== Pipeline DBSCAN PKL — 12 Langkah ===\n")

    # 1-2 load & validate
    print("[1-2] Load & validasi data...")
    df_siswa, df_dudi, warns = load_data(siswa, dudi)
    for w in warns:
        print(f"  warn: {w}")
    print(f"  siswa: {len(df_siswa)} baris, dudi: {len(df_dudi)} baris")
    if df_siswa.empty:
        print("[error] Tidak ada data siswa valid — abort")
        return 1

    # 2-3 preprocess & scaler
    print("\n[2] Preprocessing — pilih 10 fitur inti...")
    X_raw, cols = preprocess(df_siswa)
    print(f"  fitur: {cols}")

    print("[3] Standardisasi (StandardScaler)...")
    X_scaled, scaler = scale_features(X_raw)

    # 4 k-distance
    print(f"\n[4] k-distance graph (k={config.K_DISTANCE_K})...")
    k_dist, reco = k_distance_graph(X_scaled)
    print(f"  rekomendasi eps: {reco:.4f} (pakai eps={eps})")

    # 5 DBSCAN
    print(f"\n[5] DBSCAN eps={eps} min_samples={min_samples}...")
    labels = run_dbscan(X_scaled, eps=eps, min_samples=min_samples)
    from collections import Counter
    cnt = Counter(labels)
    n_cluster = len([k for k in cnt if k != -1])
    n_noise = cnt.get(-1, 0)
    print(f"  cluster: {n_cluster}, noise: {n_noise}, distribusi: {dict(cnt)}")
    if n_cluster == 0:
        print("  warn: semua noise — coba naikkan eps atau turunkan min_samples")
    if n_cluster == 1 and n_noise == 0:
        print("  warn: semua jadi 1 cluster — coba turunkan eps")

    # 6 silhouette
    print("\n[6] Validasi kuantitatif — Silhouette...")
    sil = silhouette_score_wrap(X_scaled, labels)
    if sil is None:
        print("  silhouette: N/A (hanya <2 cluster, exclude noise)")
    else:
        print(f"  silhouette: {sil:.4f}")

    # 7 profil
    print("\n[7] Profilisasi cluster...")
    profil = profile_clusters(df_siswa, labels)
    if profil.empty:
        print("  (tidak ada cluster — semua noise)")
    else:
        print(profil.to_string())

    # 8 noise
    print("\n[8] Deteksi noise...")
    noise_df = detect_noise(df_siswa, labels)
    print(f"  noise: {len(noise_df)} siswa")
    if not noise_df.empty:
        print(noise_df[["ID_Siswa"] + config.FEATURE_COLS[:3]].head(10).to_string(index=False))

    # 9 matching DUDI
    mode = matching.lower()
    print(f"\n[9] Matching ke DUDI ({mode})...")
    if mode == "topsis":
        dudi_match = topsis_rank(profil, df_dudi)
        for cl, info in dudi_match.items():
            print(f"  Cluster {cl} → {info['Nama_DUDI']} (skor {info['Skor']}, jarak {info['Jarak']}) rank2={info['ranking'][1] if len(info['ranking'])>1 else '-'} gap={info['gap_terbesar']}")
    else:
        dudi_match = match_to_dudi(profil, df_dudi)
        for cl, info in dudi_match.items():
            print(f"  Cluster {cl} → {info['Nama_DUDI']} (jarak {info['Jarak']})")

    # 10 validasi kualitatif
    print("\n[10] Validasi kualitatif vs Penilaian_Guru...")
    qual = qualitative_validation(df_siswa, labels, profil)
    if qual is None:
        print("  N/A — Penilaian_Guru kosong atau tidak ada cluster")
    else:
        print(f"  kesesuaian: {qual['accuracy']:.1%} ({qual['n_match']}/{qual['n_total']}), kappa={qual['kappa']}")
        print(f"  mapping: {qual['mapping']}")

    # 11 visualisasi
    print("\n[11] Visualisasi cluster (PCA)...")
    p = plot_clusters(X_scaled, labels)
    print(f"  disimpan: {p}")

    # 12 export
    print("\n[12] Export hasil...")
    paths = export_results(df_siswa, labels, profil, dudi_match)
    for k, v in paths.items():
        print(f"  {k}: {v}")
    print(f"  k_distance_graph: {config.OUTPUT_FILES['k_distance']}")
    print(f"  cluster_plot: {config.OUTPUT_FILES['cluster_plot']}")

    print("\n=== Selesai ===")
    if sil is not None:
        print(f"Silhouette={sil:.3f} | Cluster={n_cluster} Noise={n_noise}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Pipeline DBSCAN PKL")
    ap.add_argument("--siswa", default=config.INPUT_SISWA)
    ap.add_argument("--dudi", default=config.INPUT_DUDI)
    ap.add_argument("--eps", type=float, default=None)
    ap.add_argument("--min-samples", type=int, default=None, dest="min_samples")
    ap.add_argument("--matching", choices=["euclidean", "topsis"], default="topsis", help="Metode matching DUDI")
    args = ap.parse_args()
    raise SystemExit(main(siswa=args.siswa, dudi=args.dudi, eps=args.eps, min_samples=args.min_samples, matching=args.matching))
