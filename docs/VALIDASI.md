# Cara Baca Hasil Validasi

## Kuantitatif — Silhouette Coefficient
- **Rumus**: rata-rata (b−a)/max(a,b) per titik; a=jarak intra-cluster, b=jarak inter-cluster terdekat.
- **Range**: −1 (salah cluster) .. 0 (overlap) .. 1 (padat & terpisah).
- **Interpretasi**:
  | Nilai | Arti | Tindak lanjut |
  |-------|------|---------------|
  | >0.5 | Baik, cluster terpisah | Pertahankan eps |
  | 0.25–0.5 | Cukup, ada overlap | Coba tuning eps ±0.1 |
  | <0.25 | Buruk | Cek k-distance graph, cek StandardScaler |
  | `nan`/`None` | <2 cluster (exclude noise) | Normal jika semua 1 cluster / semua noise — bukan error |

Di-code: `validation.silhouette_score_wrap()` — exclude noise, warning jika <2 cluster.

## Kualitatif — vs Penilaian Guru
- Mapping cluster→kategori: argmax profil (mis. dominan Programming → Software, Jaringan → Network).
- **% Kesesuaian** = (cocok / total berlabel) × 100. Cocok = Kategori cluster == Penilaian_Guru.
- **Cohen's Kappa** = kesepakatan terkoreksi chance (−1..1). >0.6 substantial, 0.4–0.6 moderate. Dihitung via `sklearn.metrics.cohen_kappa_score`.
- Jika `Penilaian_Guru` kosong semua → skip, cetak warning, pipeline tetap export.

## Contoh Output Log
```
[silhouette] 0.43 (n_cluster=3, noise=2)
[qualitative] kesesuaian 72.5% (29/40), kappa=0.58
```

## Untuk BAB 4
Sertakan: tabel profil cluster, grafik k-distance, scatter plot, nilai silhouette + kappa, dan kutipan `laporan_noise.xlsx`.
