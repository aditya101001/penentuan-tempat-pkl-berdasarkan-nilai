# Requirement Project — Skripsi DBSCAN Pemetaan PKL

## Judul
Penerapan Algoritma DBSCAN untuk Klasterisasi Profil Kompetensi dan Minat Siswa Kelas XI sebagai Dasar Rekomendasi Kesesuaian Penempatan Praktik Kerja Lapangan (PKL) Berbasis Kebutuhan Dunia Usaha dan Dunia Industri (DUDI): Studi Kasus SMK IT Bina Adzkia

## Konteks
- Siswa kelas X mengikuti program keahlian PPLG (Pengembangan Perangkat Lunak dan Gim) — kompetensi programming
- Siswa kelas XI mengikuti konsentrasi TJKT (Teknik Jaringan Komputer dan Telekomunikasi) — kompetensi jaringan/infrastruktur
- Tujuan akhir: rekomendasi awal penempatan PKL kelas XI berdasarkan profil kompetensi + minat, dicocokkan ke kategori kebutuhan DUDI
- Output BUKAN keputusan final, tapi bahan pertimbangan Waka Hubin

## Tujuan Aplikasi/Sistem
1. Mengelompokkan siswa berdasarkan profil kompetensi + minat menggunakan DBSCAN
2. Memprofilkan karakteristik tiap cluster
3. Mencocokkan tiap cluster ke kategori kebutuhan DUDI (proses terpisah dari DBSCAN)
4. Memvalidasi hasil clustering (Silhouette Coefficient + perbandingan penilaian guru/Hubin)
5. Menghasilkan laporan/output yang bisa dibaca non-teknis (Waka Hubin, Kepala Sekolah)

## Struktur Data Input

### 1. Dataset Siswa (Excel: `dataset_siswa.xlsx`)
Kolom:
- `ID_Siswa` (string, anonim: S001, S002, dst)
- `Nama` (opsional, untuk internal — jangan dipakai di clustering)
- `Programming_X` (0-100, nilai kelas X PPLG)
- `Software_X` (0-100, nilai kelas X PPLG)
- `SistemOperasi_XI` (0-100, nilai kelas XI TJKT)
- `Jaringan_XI` (0-100, nilai kelas XI TJKT)
- `Troubleshooting_XI` (0-100, nilai kelas XI TJKT)
- `Keamanan_XI` (0-100, nilai kelas XI TJKT)
- `Minat_Programming` (1-5, kuesioner)
- `Minat_Networking` (1-5, kuesioner)
- `Minat_Support` (1-5, kuesioner)
- `Minat_Cybersecurity` (1-5, kuesioner)
- `Kedisiplinan` (1-4, opsional, nilai sikap)
- `KerjaSama` (1-4, opsional, nilai sikap)
- `Penilaian_Guru` (string, kategori: Software/Network/Support/Design — untuk validasi, diisi manual oleh guru/Hubin)

### 2. Dataset DUDI (Excel: `dataset_dudi.xlsx`)
Kolom:
- `Nama_DUDI` (string)
- `Networking` (1-5)
- `Support` (1-5)
- `Server_Cloud` (1-5)
- `Programming` (1-5)
- `Cybersecurity` (1-5)

## Requirement Teknis (Python)

### Library
```
pandas
numpy
scikit-learn
scipy
matplotlib
seaborn
openpyxl
```

### Alur Program (wajib berurutan, buat modular per fungsi/file)
1. **Load & validasi data** — cek missing value, tipe data salah, rentang nilai di luar skala (tolak/beri warning, jangan crash)
2. **Preprocessing** — cleaning, pilih fitur (10 variabel inti dari kisi-kisi), encoding jika ada kategorikal
3. **Standardisasi** — StandardScaler untuk semua fitur numerik sebelum DBSCAN
4. **Penentuan parameter DBSCAN**:
   - Generate k-distance graph (k = 2 × jumlah dimensi fitur), simpan sebagai gambar
   - Beri rekomendasi otomatis titik elbow (pakai `kneedle` algorithm kalau bisa, atau least-effort: cari titik dengan perubahan gradien terbesar) — tapi tetap tampilkan grafik untuk verifikasi manual
5. **Jalankan DBSCAN** — parameter eps & min_samples bisa diubah lewat variabel/config, bukan hardcode di tengah kode
6. **Validasi kuantitatif** — hitung Silhouette Coefficient (exclude noise dari perhitungan)
7. **Profilisasi cluster** — rata-rata tiap variabel per cluster, tampilkan dalam tabel
8. **Deteksi & laporkan noise** — daftar siswa dengan label -1, tampilkan terpisah (bukan dihapus)
9. **Matching ke DUDI** — normalisasi profil cluster ke skala DUDI (1-5), hitung jarak euclidean, rekomendasikan DUDI terdekat per cluster
10. **Validasi kualitatif** — bandingkan hasil cluster (setelah dikategorikan: Software/Network/Support/dst) dengan kolom `Penilaian_Guru`, hitung persentase kesesuaian sederhana (dan Cohen's Kappa jika memungkinkan)
11. **Visualisasi** — scatter plot cluster (2 fitur representatif atau reduksi PCA jika >2 dimensi perlu divisualisasikan), simpan sebagai gambar
12. **Export hasil**:
    - `hasil_klasterisasi.xlsx` (data siswa + kolom Cluster + Kategori + Rekomendasi DUDI)
    - `profil_cluster.xlsx` (ringkasan tiap cluster)
    - `laporan_noise.xlsx` (daftar siswa noise)
    - `k_distance_graph.png`
    - `hasil_cluster_plot.png`

### Requirement Tambahan
- Kode harus modular (pisah fungsi: `load_data()`, `preprocess()`, `run_dbscan()`, `validate()`, `match_dudi()`, `export_results()`) — bukan satu script panjang tanpa fungsi
- Tambahkan docstring singkat tiap fungsi (untuk lampiran source code di skripsi)
- Buatkan juga **script generate dataset dummy** (`generate_dummy_data.py`) untuk uji coba sebelum data asli sekolah tersedia — jumlah baris bisa diatur (misal default 40 siswa)
- Tangani kasus edge: seluruh data jadi satu cluster, seluruh data jadi noise, kolom `Penilaian_Guru` kosong (skip validasi kualitatif dengan warning, jangan error)
- Buat `README.md` singkat cara menjalankan tiap script secara berurutan

## Yang TIDAK dibutuhkan (batasan scope)
- Tidak perlu web app / dashboard interaktif (bukan bagian skripsi ini)
- Tidak perlu database — cukup file Excel sebagai input/output
- Tidak perlu deployment — hanya script lokal untuk hasil BAB 4
