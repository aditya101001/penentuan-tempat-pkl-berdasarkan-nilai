# Skripsi DBSCAN — Klasterisasi PKL

Penerapan DBSCAN untuk klasterisasi profil kompetensi + minat siswa kelas XI TJKT sebagai dasar rekomendasi penempatan PKL berbasis kebutuhan DUDI.

## Prasyarat
- Python 3.10+ (tested 3.10–3.12)
- pip / uv

## Setup (sekali)
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Cara Generate Data Dummy
Data asli belum ada? Pakai dummy 40 siswa:
```bash
python generate_dummy_data.py --n 40 --seed 42
# overwrite:
python generate_dummy_data.py --n 40 --seed 42 --force
# custom:
python generate_dummy_data.py --n 60 --seed 123 --out dataset_siswa.xlsx --dudi dataset_dudi.xlsx
```
Hasil: `dataset_siswa.xlsx` (sheet Siswa) + `dataset_dudi.xlsx` (sheet DUDI).

## Cara Run (pipeline 12 langkah)
```bash
python main.py                                  # default topsis berbobot (usulan, paling defensible)
python main.py --matching euclidean             # baseline untuk perbandingan BAB 4
python main.py --matching topsis --eps 2.5
# atau dengan path custom:
python main.py --siswa dataset_siswa.xlsx --dudi dataset_dudi.xlsx --eps 2.5 --min-samples 5 --matching topsis
```
Output di `output/` (mode topsis):
- `hasil_klasterisasi.xlsx` — siswa + Cluster + Kategori + Rekomendasi DUDI + Skor_TOPSIS + Ranking_Top3
- `profil_cluster.xlsx` — mean per cluster + Rekomendasi + Skor_TOPSIS + Ranking_Top3 + Gap_Terbesar
- `laporan_noise.xlsx` — daftar noise (label -1)
- `k_distance_graph.png` — kurva k-distance + garis eps rekomendasi
- `hasil_cluster_plot.png` — scatter PCA per cluster

Log menampilkan silhouette, % kesesuaian guru, rekomendasi eps, dan ranking TOPSIS (skor 0-1).

## Cara Ubah Parameter
Edit `config.py` (satu-satunya sumber):
```python
EPS = 2.5
MIN_SAMPLES = 5
FEATURE_COLS = [...]  # 10 variabel inti
DUDI_WEIGHTS = {"Networking":0.25,"Support":0.20,"Server_Cloud":0.15,"Programming":0.25,"Cybersecurity":0.15} # AHP
```
Atau via CLI: `python main.py --eps 2.5 --min-samples 5 --matching topsis`

## Cara Test
```bash
pytest -q
pytest --cov=src --cov-report=term-missing  # coverage
pytest -k test_integration -xvs            # debug end-to-end
```

## Struktur Direktori
```
config.py  generate_dummy_data.py  main.py  requirements.txt
src/  (data_loader, preprocessing, dbscan_runner, validation, profiling, matching, visualization, export)
tests/  output/  docs/
```

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `FileNotFoundError: dataset_siswa.xlsx` | Jalankan `python generate_dummy_data.py --n 40` dulu |
| Semua jadi 1 cluster / semua noise | Tuning `EPS` di `config.py` (naikkan jika semua noise, turunkan jika 1 cluster); lihat `k_distance_graph.png` |
| `Penilaian_Guru` kosong → validasi kualitatif N/A | Normal — warning dicetak, pipeline tetap export |
| Silhouette `nan` | Terjadi jika <2 cluster (exclude noise); cek profil cluster |
| `ModuleNotFoundError: kneed` | `pip install kneed` atau fallback gradient sudah otomatis |
| `openpyxl` error | `pip install openpyxl` |

## Dokumen Terkait
- `requirement_skripsi_dbscan.md` — requirement mentah
- `prd.md` — PRD tunggal final (v1.1 TOPSIS terintegrasi)
- `docs/KAJIAN_PUSTAKA.md` — 6 penelitian terdahulu DBSCAN+TOPSIS/AHP + novelty (untuk BAB 2)
- `docs/DATA_DICTIONARY.md` — kamus data
- `docs/ALGORITMA.md` — ringkas algoritma (Euclidean vs TOPSIS)
- `docs/VALIDASI.md` — cara baca hasil validasi
