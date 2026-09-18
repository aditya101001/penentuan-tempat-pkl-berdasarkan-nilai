# Ringkas Algoritma

## Kenapa DBSCAN (bukan KMeans)
- Jumlah cluster tidak perlu ditebak di awal (data PKL eksploratif)
- Menangani outlier/noise eksplisit (label -1) — siswa tidak cocok cluster mana pun tetap terlapor
- Bentuk cluster tidak harus spherical

## StandardScaler
Wajib sebelum DBSCAN karena skala beda: nilai 0–100 vs minat 1–5. Tanpa scaler, nilai mendominasi jarak Euclidean. `StandardScaler → mean 0, std 1` per fitur.

## k-Distance Graph & Elbow
- Hitung jarak ke k-th nearest neighbor (k = 2 × dimensi = 20) untuk tiap titik, sort ascending, plot.
- Titik elbow = eps kandidat. Implementasi: coba `KneeLocator` (kneed), fallback ke max gradient (selisih terbesar antar titik berurutan).
- Grafik disimpan `k_distance_graph.png`; eps final tetap dari `config.py` (grafik untuk verifikasi manual).

## DBSCAN
`sklearn.cluster.DBSCAN(eps, min_samples)` pada `X_scaled`. Output `labels` (−1 = noise).

## Silhouette Coefficient
Validasi kuantitatif: `silhouette_score(X_scaled[labels!=-1], labels[labels!=-1])` — exclude noise. Range −1..1, >0.5 baik, <0.2 overlap. Return `None` jika <2 cluster (bukan error).

## Profil Cluster
Mean per variabel per cluster → tabel `profil_cluster.xlsx`.

## Matching ke DUDI — Dua Mode

**Baseline Euclidean (`src/matching.py`):**
- Normalisasi profil: nilai 0–100 → 1–5 via `(x/100)*4+1`; minat sudah 1–5.
- Hitung Euclidean antara profil cluster (5 dimensi DUDI) vs tiap DUDI → ranking terkecil = rekomendasi.
- Kelemahan: anggap semua kriteria sama penting — tidak realistis (ISP butuh Networking 2× lebih penting).

**Eksperimen Opsional — AHP-TOPSIS Berbobot (`src/matching_topsis.py`, Future Work, bukan metode utama):**
- Hanya diaktifkan jika syarat Lampiran C prd.md terpenuhi (persetujuan pembimbing + pairwise matrix asli Hubin + CR<0.1 + bukti empiris). Bukan default.
- Langkah Hwang & Yoon 1981: (1) normalisasi vektor `r_ij = x_ij/sqrt(sum x_j^2)`, (2) berbobot `v = r * w` (w dari AHP Hubin), (3) ideal positif = max, negatif = min, (4) skor `C = D-/(D+ + D-)` 0-1 + ranking Top-3 + gap terbesar.
- Bobot `DUDI_WEIGHTS` di `config.py` dikomentari sebagai eksperimen — default Euclidean equal weight (0.20).
- Output eksperimen: `Skor_TOPSIS`, `Ranking_Top3`, `Gap_Terbesar` untuk pembekalan (hanya jika mode topsis).

Ref: Ester et al. 1996 (DBSCAN), Rousseeuw 1987 (Silhouette), Hwang & Yoon 1981 (TOPSIS), Saaty 1980 (AHP).
