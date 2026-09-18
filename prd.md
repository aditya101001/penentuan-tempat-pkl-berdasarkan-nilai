# PRD — Sistem Klasterisasi DBSCAN untuk Rekomendasi Penempatan PKL
> **RANCANGAN TUNGGAL FINAL.**

> Turunan langsung dari `requirement_skripsi_dbscan.md` — dokumen ini menjadi acuan build, test, dan kelengkapan dokumentasi agar sistem dapat berjalan reproduksibel untuk BAB 4 skripsi.

## KEPUTUSAN FINAL

| Aspek | Keputusan Baru | Alasan |
|-------|-----------------|--------|
| Klasterisasi | Tetap DBSCAN (`eps=2.5, min_samples=5`) | Tidak berubah |
| Matching DUDI (default) | **Euclidean** — sesuai judul, tidak perlu revisi rumusan masalah | Konsistensi judul, aman di sidang |
| Matching DUDI (opsional) | TOPSIS+AHP — **hanya diaktifkan** jika: (1) dosen pembimbing setuju revisi rumusan masalah/judul, (2) ada pairwise comparison matrix asli dari Waka Hubin + CR < 0.1 terlampir, (3) tidak diklaim sebagai fakta sebelum diuji ke data asli | Hindari klaim tak berdasar, hindari kerja tambahan tanpa persetujuan |
| Klaim akurasi | Hapus "naikkan akurasi 10-15%" — ganti jadi hipotesis: "TOPSIS berpotensi meningkatkan akurasi dibanding Euclidean — perlu diuji dengan data asli, belum ada bukti empiris" | Klaim harus berbasis bukti, bukan asumsi |

**Perintah final:**
```bash
python main.py                          # default euclidean (resmi BAB 4)
python main.py --matching topsis        # eksperimen — cetak warning, jangan pakai resmi tanpa persetujuan
```

| Field | Isi |
|-------|-----|
| **Judul** | Penerapan Algoritma DBSCAN untuk Klasterisasi Profil Kompetensi dan Minat Siswa Kelas XI sebagai Dasar Rekomendasi Kesesuaian Penempatan PKL Berbasis Kebutuhan DUDI (Studi Kasus SMK IT Bina Adzkia) |
| **Versi** | 1.2 — 2026-09-18 (Euclidean default, TOPSIS eksperimen) |
| **Status** | Implemented — Euclidean default resmi; TOPSIS eksperimen non-default (lihat Lampiran C) |
| **Stack** | Python 3.10+ · pandas · numpy · scikit-learn · scipy · matplotlib · seaborn · openpyxl |
| **Input** | `dataset_siswa.xlsx` + `dataset_dudi.xlsx` |
| **Output** | 3 Excel + 2 PNG (lihat §8) — default Euclidean; mode `topsis` hanya eksperimen |

---

## 1. Ringkasan

Sistem mengelompokkan siswa kelas XI TJKT berdasarkan **10 variabel inti** (6 nilai akademik + 4 minat) dengan DBSCAN, memprofilkan tiap cluster, mencocokkan ke kebutuhan DUDI via **Euclidean (default, jarak lurus tanpa bobot)**. Mode **TOPSIS+AHP tersedia sebagai opsi eksperimen** (skor 0-1 + ranking Top-3 + gap) — **memerlukan syarat tambahan sebelum dipakai resmi (lihat Lampiran C)** — lalu memvalidasi secara kuantitatif (Silhouette) dan kualitatif (Penilaian_Guru). Output bersifat **rekomendasi awal untuk Waka Hubin**, bukan keputusan final.

Prinsip: **modular, reproduksibel, non-interaktif** (CLI/Excel saja, tanpa web app/DB/deployment). DBSCAN tetap inti (sesuai judul).

---

## 2. Tujuan & Success Metrics

| Tujuan | Metric Sukses |
|--------|---------------|
| Klasterisasi berjalan reproduksibel | `pytest` hijau, run ulang hasil identik (seed fixed) |
| Parameter DBSCAN transparan | `k_distance_graph.png` ter-generate + rekomendasi eps tercetak |
| Validasi kuantitatif | Silhouette Coefficient terhitung (exclude noise); `nan` jika <2 cluster — tidak crash |
| Validasi kualitatif | % kesesuaian + Cohen's Kappa vs `Penilaian_Guru` (skip gracefully jika kolom kosong) |
| Output non-teknis readable | 3 Excel + 2 PNG sesuai template; Waka Hubin paham tanpa penjelasan teknis |
| Edge case tertangani | Tidak crash pada: semua 1 cluster, semua noise, missing value, `Penilaian_Guru` kosong |

---

## 3. Scope

### In Scope
- Load & validasi Excel, preprocessing, StandardScaler, k-distance graph, DBSCAN, silhouette, profil cluster, deteksi noise, matching DUDI, visualisasi, export.
- `generate_dummy_data.py` (40 siswa default, configurable).
- Unit & integration test.
- Dokumentasi minimal agar BAB 4 dapat direplikasi penguji.

### Out of Scope (jangan dibangun)
- Web app / dashboard / API.
- Database (SQLite/Postgres).
- Deployment / Docker / CI cloud (cukup lokal).
- Auto-tunning hyperparameter kompleks (cukup k-distance + elbow sederhana).

---

## 4. Personas

| Persona | Kebutuhan |
|---------|-----------|
| **Mahasiswa (peneliti)** | Menjalankan pipeline end-to-end, menghasilkan lampiran BAB 4 |
| **Waka Hubin / Guru** | Membaca `hasil_klasterisasi.xlsx` + `profil_cluster.xlsx` untuk pertimbangan PKL |
| **Penguji Skripsi** | Mereplikasi hasil dari nol (clone → install → run → test hijau) |

---

## 5. Spesifikasi Data

### 5.1 `dataset_siswa.xlsx` — 1 sheet `Siswa`

| Kolom | Tipe | Rentang | Wajib | Dipakai clustering? |
|-------|------|---------|-------|---------------------|
| `ID_Siswa` | string S### | unik | Ya | Tidak (identifier) |
| `Nama` | string | — | Tidak | Tidak |
| `Programming_X` | int/float | 0–100 | Ya | **Ya** |
| `Software_X` | int/float | 0–100 | Ya | **Ya** |
| `SistemOperasi_XI` | int/float | 0–100 | Ya | **Ya** |
| `Jaringan_XI` | int/float | 0–100 | Ya | **Ya** |
| `Troubleshooting_XI` | int/float | 0–100 | Ya | **Ya** |
| `Keamanan_XI` | int/float | 0–100 | Ya | **Ya** |
| `Minat_Programming` | int | 1–5 | Ya | **Ya** |
| `Minat_Networking` | int | 1–5 | Ya | **Ya** |
| `Minat_Support` | int | 1–5 | Ya | **Ya** |
| `Minat_Cybersecurity` | int | 1–5 | Ya | **Ya** |
| `Kedisiplinan` | int | 1–4 | Tidak | Tidak (opsional, exclude default) |
| `KerjaSama` | int | 1–4 | Tidak | Tidak |
| `Penilaian_Guru` | string | Software/Network/Support/Design | Tidak | Tidak — hanya validasi kualitatif |

**10 variabel inti** = 6 nilai + 4 minat (baris bold). Inilah `FEATURE_COLS` default.

### 5.2 `dataset_dudi.xlsx` — 1 sheet `DUDI`

| Kolom | Tipe | Rentang |
|-------|------|---------|
| `Nama_DUDI` | string | unik |
| `Networking` | int 1–5 | |
| `Support` | int 1–5 | |
| `Server_Cloud` | int 1–5 | |
| `Programming` | int 1–5 | |
| `Cybersecurity` | int 1–5 | |

### 5.3 Aturan Validasi Input
- Missing value → warning + baris di-drop atau diisi median (pilih satu, **dokumentasikan**; default: drop + log jumlah drop).
- Tipe salah → `coerce` dengan pesan jelas (contoh: `"Jaringan_XI baris 12 bukan numerik"`).
- Di luar rentang → warning, clamp atau tolak (default: tolak baris + catat).
- `Penilaian_Guru` kosong/null → skip validasi kualitatif dengan `logger.warning`, bukan error.

---

## 6. Arsitektur & Struktur Direktori

### 6.1 Prinsip Modularitas (wajib)
Satu script panjang dilarang. Pisah per fungsi/file dengan docstring singkat:

```
skripsi/
├── requirement_skripsi_dbscan.md
├── prd.md                         # ← dokumen ini
├── README.md                      # cara run berurutan (wajib)
├── docs/
│   ├── DATA_DICTIONARY.md         # kamus data 5.1–5.2 + contoh isi
│   ├── ALGORITMA.md               # ringkas DBSCAN, StandardScaler, elbow, silhouette, matching Euclidean vs TOPSIS
│   └── VALIDASI.md                # cara baca silhouette & kappa
├── dataset_siswa.xlsx             # (gitignore jika data asli sensitif)
├── dataset_dudi.xlsx
├── config.py                      # eps, min_samples, FEATURE_COLS, DUDI_WEIGHTS, paths — bukan hardcode
├── src/
│   ├── __init__.py
│   ├── data_loader.py             # load_data() + validate_input()
│   ├── preprocessing.py           # preprocess() + StandardScaler
│   ├── dbscan_runner.py           # k_distance_graph(), suggest_eps(), run_dbscan()
│   ├── validation.py              # silhouette_score_wrap(), qualitative_validation()
│   ├── profiling.py               # profile_clusters(), detect_noise()
│   ├── matching.py                # match_to_dudi() — euclidean baseline
│   ├── matching_topsis.py         # topsis_rank() — AHP-TOPSIS berbobot (usulan)
│   ├── visualization.py           # plot_clusters() (PCA jika >2D)
│   └── export.py                  # export_results() — handle Skor_TOPSIS + Ranking_Top3
├── generate_dummy_data.py         # CLI: --n 40 --seed 42 --out dataset_siswa.xlsx
├── main.py                        # orkestrasi 12 langkah berurutan
├── requirements.txt               # atau pyproject.toml
├── tests/
│   ├── test_data_loader.py
│   ├── test_preprocessing.py
│   ├── test_dbscan_runner.py
│   ├── test_validation.py
│   ├── test_matching.py
│   ├── test_export.py
│   └── test_integration.py        # end-to-end dengan dummy data
└── output/                        # gitignore, hasil generate
    ├── hasil_klasterisasi.xlsx
    ├── profil_cluster.xlsx
    ├── laporan_noise.xlsx
    ├── k_distance_graph.png
    └── hasil_cluster_plot.png
```

### 6.2 Config (`config.py`)
```python
FEATURE_COLS = [
    "Programming_X","Software_X","SistemOperasi_XI","Jaringan_XI",
    "Troubleshooting_XI","Keamanan_XI",
    "Minat_Programming","Minat_Networking","Minat_Support","Minat_Cybersecurity"
]
EPS = 2.5              # 2.5 → 2 cluster pada dummy n=40 (0.7 semua noise di 10D scaled)
MIN_SAMPLES = 5
K_DISTANCE_K = 2 * len(FEATURE_COLS)  # =20, untuk k-distance graph (visual saja)
RANDOM_STATE = 42
INPUT_SISWA = "dataset_siswa.xlsx"
INPUT_DUDI  = "dataset_dudi.xlsx"
OUTPUT_DIR  = "output"
DUDI_WEIGHTS = {"Networking":0.25,"Support":0.20,"Server_Cloud":0.15,"Programming":0.25,"Cybersecurity":0.15} # AHP, sum 1.0
```

---

## 7. Alur Program — 12 Langkah Berurutan

| # | Langkah | Fungsi | Catatan Implementasi |
|---|---------|--------|----------------------|
| 1 | Load & validasi | `load_data()` | `openpyxl`, cek missing/tipe/rentang; return `DataFrame` + `warnings: list` |
| 2 | Preprocessing | `preprocess(df)` | pilih `FEATURE_COLS`, cleaning, return `X_raw` |
| 3 | Standardisasi | `StandardScaler` | fit hanya pada `X_raw`; simpan scaler jika perlu inverse |
| 4 | Penentuan eps | `k_distance_graph(X_scaled)` | hitung k-distance (NearestNeighbors k=K_DISTANCE_K), sort, plot; `suggest_eps()` via KneeLocator/`kneedle` atau max gradient; **simpan PNG**, cetak rekomendasi, eps final tetap dari `config.py` |
| 5 | DBSCAN | `run_dbscan(X_scaled, eps, min_samples)` | `sklearn.cluster.DBSCAN`; return `labels` |
| 6 | Validasi kuantitatif | `silhouette_score_wrap()` | exclude `label==-1`; jika n_cluster<2 → return `None` + warning |
| 7 | Profilisasi | `profile_clusters(df, labels)` | groupby cluster → mean per variabel; tampilkan tabel (console + Excel) |
| 8 | Noise | `detect_noise(df, labels)` | filter `label==-1`; jangan hapus, laporkan terpisah |
| 9 | Matching DUDI | `match_to_dudi()` **(default Euclidean, resmi)** — `topsis_rank()` **hanya eksperimen** (lihat Lampiran C) | normalisasi profil: `(x/100)*4+1` → 1–5; Euclidean: jarak lurus; TOPSIS eksperimen: normalisasi vektor → berbobot AHP → jarak ke ideal +/- → skor 0-1 + ranking Top-3 + gap |
| 10 | Validasi kualitatif | `qualitative_validation()` | mapping cluster→kategori (argmax profil), bandingkan ke `Penilaian_Guru`; hitung accuracy (%) + `cohen_kappa_score` (skip jika kolom kosong) |
| 11 | Visualisasi | `plot_clusters()` | scatter 2D: pakai 2 fitur representatif atau PCA(n_components=2); warna per cluster, `x` untuk noise |
| 12 | Export | `export_results()` | 3 Excel + 2 PNG ke `output/`; buat folder jika belum ada |

---

## 8. Spesifikasi Output

| File | Isi |
|------|-----|
| `output/hasil_klasterisasi.xlsx` | `dataset_siswa` + `Cluster` + `Kategori` + `Rekomendasi_DUDI` + `Jarak_DUDI` (mode default Euclidean; jika eksperimen `topsis` tambah `Skor_TOPSIS` + `Ranking_Top3`) |
| `output/profil_cluster.xlsx` | baris=cluster, mean tiap variabel + `Jumlah_Anggota` + `Rekomendasi_DUDI` + `Jarak_DUDI` (jika eksperimen `topsis` tambah `Skor_TOPSIS` + `Ranking_Top3` + `Gap_Terbesar`) |
| `output/laporan_noise.xlsx` | subset `hasil_klasterisasi` di mana `Cluster==-1`, plus alasan (opsional) |
| `output/k_distance_graph.png` | line sorted k-distance + garis vertikal eps rekomendasi |
| `output/hasil_cluster_plot.png` | scatter PCA/cluster |

Semua Excel: header freeze, autofilter, lebar kolom auto-fit.

---

## 9. Build & Run — Agar Reproduksibel

### 9.1 Prasyarat
- Python 3.10+ (uji di 3.10, 3.11, 3.12)
- `pip` atau `uv`

### 9.2 Setup (sekali)
```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# atau: pip install pandas numpy scikit-learn scipy matplotlib seaborn openpyxl
```

`requirements.txt` dipin versi minor:
```
pandas>=2.0,<3
numpy>=1.24
scikit-learn>=1.3
scipy>=1.11
matplotlib>=3.7
seaborn>=0.12
openpyxl>=3.1
kneed>=0.8  # opsional untuk KneeLocator, fallback ke gradient jika tak ada
pytest>=8
```

### 9.3 Menjalankan (berurutan — untuk README.md)
```bash
# 1. Generate dummy jika data asli belum ada
python generate_dummy_data.py --n 40 --seed 42

# 2. Jalankan pipeline penuh
python main.py                          # default euclidean (resmi BAB 4)
python main.py --matching topsis --eps 2.5  # eksperimen — warning, butuh persetujuan pembimbing (Lampiran C)
# atau step-by-step:
python -m src.data_loader
python -m src.preprocessing
# main.py yang direkomendasikan — orkestrasi 12 langkah
```

`main.py` harus:
- baca `config.py`
- log tiap langkah ke stdout
- exit code 0 sukses, 1 jika validasi input gagal total
- tidak crash pada edge case (warning + lanjut)

### 9.4 Verifikasi Cepat
```bash
pytest -q
pytest --cov=src --cov-report=term-missing  # opsional
python generate_dummy_data.py --n 10 && python main.py && ls -lh output/
```

---

## 10. Strategi Testing — Agar Build Selalu Hijau

### 10.1 Jenis Test

| Level | File | Apa yang diuji |
|-------|------|----------------|
| **Unit** | `test_data_loader.py` | missing value, tipe salah, rentang di luar skala, file tidak ada |
|  | `test_preprocessing.py` | FEATURE_COLS terpilih, StandardScaler mean≈0 std≈1 |
|  | `test_dbscan_runner.py` | DBSCAN label shape, k-distance graph ter-generate, suggest_eps return float |
|  | `test_validation.py` | silhouette exclude noise, return None jika <2 cluster, kappa skip jika Penilaian_Guru kosong |
|  | `test_matching.py` | normalisasi 0–100→1–5 benar, euclidean ranking benar |
|  | `test_matching_topsis.py` | TOPSIS eksperimen — skor 0-1, ranking Top-3, gap (bukan fitur resmi) |
|  | `test_export.py` | 3 Excel + 2 PNG terbuat, kolom sesuai §8 (kolom Skor_TOPSIS hanya jika topsis eksperimen) |
| **Integration** | `test_integration.py` | `generate_dummy_data(40) → main.py → semua output ada + tidak crash` |
| **Edge** | di masing-masing | semua 1 cluster, semua noise, n=5 (min_samples > n), Penilaian_Guru kosong |

### 10.2 Perintah Test
```bash
pytest -q                          # wajib hijau sebelum klaim selesai
pytest -k test_integration -xvs    # debug pipeline penuh
pytest --tb=short                  # ringkas
```

### 10.3 Kriteria Build Hijau
- `pytest -q` → `passed` semua (atau `skipped` yang terdokumentasi).
- `python main.py` dengan dummy 40 baris → 5 file output ada, tidak ada traceback.
- `python main.py` dengan `Penilaian_Guru` dikosongkan → warning, tetap export.
- `python main.py` dengan 1 baris di luar rentang (mis. 999) → baris ditolak dengan pesan, pipeline lanjut.

### 10.4 CI Lokal (opsional tapi direkomendasikan)
Buat `Makefile` atau `justfile`:
```makefile
setup:  pip install -r requirements.txt
dummy:  python generate_dummy_data.py --n 40
run:    python main.py
test:   pytest -q
all:    dummy run test
```

---

## 11. Dokumentasi Wajib — Supaya Sistem Berjalan Baik

Tanpa ini, penguji/reviewer tidak bisa mereplikasi. Buat **sekarang**, bukan menjelang sidang.

| # | Dokumen | Lokasi | Isi Minimal | Kapan Dibuat |
|---|---------|--------|-------------|--------------|
| 1 | **README.md** | root | Prasyarat, setup venv, `requirements.txt`, cara run berurutan (copy-pasteable), struktur output, cara ubah eps/min_samples/DUDI_WEIGHTS via `config.py`, FAQ error umum | **Sebelum coding** (skeleton dulu) |
| 2 | **DATA_DICTIONARY.md** | `docs/` | Tabel §5.1–5.2 + contoh 3 baris dummy + penjelasan 10 variabel inti vs opsional | Bersama `generate_dummy_data.py` |
| 3 | **ALGORITMA.md** | `docs/` | 1 hlm: kenapa DBSCAN (vs KMeans), StandardScaler, k-distance/elbow, silhouette, matching Euclidean (utama) vs TOPSIS berbobot eksperimen (Lampiran C) + referensi | Saat implementasi `dbscan_runner.py`; TOPSIS saat eksperimen |
| 4 | **KAJIAN_PUSTAKA.md** | `docs/` | 6 penelitian terdahulu DBSCAN+TOPSIS/AHP untuk PKL/magang + tabel perbandingan + novelty — TOPSIS sebagai Future Work (Lampiran C) | Untuk BAB 2 |
| 5 | **VALIDASI.md** | `docs/` | Cara baca silhouette (-1 s/d 1), interpretasi kappa, contoh tabel validasi kualitatif | Saat `validation.py` |
| 6 | **Docstring tiap fungsi** | `src/*.py` | 2–3 baris: tujuan, params, return, raise — untuk lampiran source code skripsi | Wajib per fungsi |
| 7 | **CHANGELOG.md** (opsional) | root | Tanggal, perubahan eps/dataset, hasil silhouette — jejak untuk BAB 4 | Tiap eksperimen |
| 8 | **.gitignore** | root | `output/`, `.venv/`, `__pycache__/`, `*.xlsx` (kecuali dummy contoh bila perlu) | Awal |

**Template README.md minimal** (wajib ada):
```markdown
# Skripsi DBSCAN PKL
## Setup
## Cara Generate Dummy
## Cara Run
## Cara Ubah Parameter
## Output
## Cara Test (pytest -q)
## Troubleshooting
```

---

## 12. Kriteria Penerimaan (Acceptance Criteria)

Sistem dinyatakan **siap BAB 4** jika semua ini terpenuhi:

- [ ] `pip install -r requirements.txt` berhasil di Python 3.10+ fresh venv
- [ ] `python generate_dummy_data.py --n 40` menghasilkan `dataset_siswa.xlsx` valid (sesuai §5.1)
- [ ] `python main.py` (default euclidean) menghasilkan 5 file §8 tanpa error; `python main.py --matching topsis` tetap jalan tapi cetak warning eksperimen
- [ ] `k_distance_graph.png` menampilkan kurva + garis eps rekomendasi
- [ ] `hasil_cluster_plot.png` menampilkan cluster berwarna + noise terpisah
- [ ] Silhouette tercetak (atau `N/A — hanya 1 cluster/noise` dengan warning, bukan crash)
- [ ] `profil_cluster.xlsx` berisi mean per cluster + rekomendasi DUDI (euclidean: Jarak_DUDI; topsis eksperimen tambah Skor_TOPSIS + Ranking_Top3 + Gap_Terbesar)
- [ ] `laporan_noise.xlsx` berisi daftar noise (boleh 0 baris, header tetap ada)
- [ ] Validasi kualitatif mencetak `% kesesuaian` (dan kappa jika memungkinkan)
- [ ] `pytest -q` hijau (≥15 test: 7 unit + integration + edge cases, termasuk `test_matching_topsis.py` eksperimen)
- [ ] README.md + 4 docs di `docs/` ada dan akurat
- [ ] `config.py` menjadi satu-satunya tempat ubah eps/min_samples/FEATURE_COLS (DUDI_WEIGHTS hanya eksperimen, lihat Lampiran C)
- [ ] Tidak ada hardcode parameter di tengah fungsi

---

## 13. Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|--------|--------|----------|
| Semua data jadi 1 cluster / semua noise | Silhouette `nan`, visualisasi hambar | Tangani di kode (return None + warning), dokumentasikan di VALIDASI.md; sediakan panduan tuning eps di README |
| `Penilaian_Guru` kosong | Validasi kualitatif gagal | Skip dengan warning, tetap export; test khusus |
| Skala nilai vs minat beda (0–100 vs 1–5) | Clustering bias ke nilai | StandardScaler wajib sebelum DBSCAN; matching pakai normalisasi terpisah |
| Data asli belum tersedia | Tidak bisa uji | `generate_dummy_data.py` dengan distribusi realistis (3 persona: programmer/network/support) |
| Penguji pakai Python/OS berbeda | Hasil beda | Pin versi di requirements, `RANDOM_STATE=42`, catat versi di README |

---

## 14. Rencana Implementasi Bertahap (untuk eksekusi)

| Fase | Deliverable | Verifikasi |
|------|-------------|------------|
| **F1 — Skeleton & Data** | `config.py`, `generate_dummy_data.py`, `src/data_loader.py`, `docs/DATA_DICTIONARY.md`, `requirements.txt`, `.gitignore` | `pytest tests/test_data_loader.py` hijau |
| **F2 — Pipeline Inti** | `preprocessing.py`, `dbscan_runner.py` (k-distance + DBSCAN), `visualization.py` | `k_distance_graph.png` + `hasil_cluster_plot.png` ter-generate |
| **F3 — Validasi & Matching** | `validation.py`, `profiling.py`, `matching.py` (Euclidean resmi) + `matching_topsis.py` (eksperimen, Lampiran C) | Silhouette + kappa tercetak, `profil_cluster.xlsx` benar (default euclidean) |
| **F4 — Export & Orkestrasi** | `export.py`, `main.py`, `tests/test_integration.py` | `python main.py` → 5 file + `pytest -q` hijau |
| **F5 — Dokumentasi Akhir** | `README.md`, `ALGORITMA.md`, `VALIDASI.md`, docstring lengkap | Orang baru bisa `clone → setup → dummy → run → test` tanpa tanya |

---

## 15. Lampiran — Perintah Penting (Copy-Paste)

```bash
# Setup awal
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Generate & run
python generate_dummy_data.py --n 40 --seed 42
python main.py                          # default euclidean (resmi BAB 4)
python main.py --matching topsis        # eksperimen — warning, butuh Lampiran C

# Test
pytest -q
pytest --cov=src -q

# Cek output
ls -lh output/
libreoffice output/hasil_klasterisasi.xlsx  # atau buka di Excel
eog output/k_distance_graph.png

# Ubah parameter
# edit config.py: EPS, MIN_SAMPLES, FEATURE_COLS
```

---

## Lampiran C — Syarat Aktivasi TOPSIS+AHP (Eksperimen, Bukan Default)

Mode `topsis` **tidak boleh dipakai sebagai hasil resmi BAB 4** kecuali ketiga syarat terpenuhi:

1. **Persetujuan pembimbing** — revisi rumusan masalah/judul disetujui (judul saat ini hanya menyebut DBSCAN)
2. **Pairwise matrix asli** — ada matriks perbandingan berpasangan 5×5 dari Waka Hubin (skala Saaty 1-9) terlampir
3. **CR < 0.1 + bukti empiris** — Consistency Ratio dihitung dan < 0.1, serta tidak diklaim "naikkan akurasi 10-15%" sebelum diuji ke data asli (ganti jadi hipotesis: "TOPSIS berpotensi meningkatkan akurasi dibanding Euclidean — perlu diuji dengan data asli, belum ada bukti empiris")

Jika syarat belum terpenuhi, gunakan **Euclidean (default)**. Kode `matching_topsis.py` tetap ada untuk eksperimen masa depan, tidak dihapus.

---

*PRD ini mengikat. Jika ada perubahan requirement dari pembimbing, ubah PRD dulu, baru kode — agar BAB 4 konsisten.*
