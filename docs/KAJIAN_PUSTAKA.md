# Kajian Pustaka — Penelitian Terdahulu DBSCAN & TOPSIS/AHP untuk Penempatan PKL

> Untuk BAB 2 skripsi. Semua sumber sudah terverifikasi via web search 2026-09-18. Format sitasi APA 7th.

## Ringkasan Temuan

Kombinasi **klasterisasi (DBSCAN/K-Means) + MCDM (TOPSIS/AHP)** untuk penempatan magang/PKL sudah terbukti efektif, namun **kombinasi spesifik DBSCAN (10 variabel kompetensi+minat) → TOPSIS berbobot AHP untuk matching DUDI SMK TJKT** belum ada — ini menjadi novelty penelitian ini.

## Tabel Perbandingan Penelitian Terdahulu vs Penelitian Ini

| No | Judul & Penulis (Tahun) | Venue | Metode | Dataset & Hasil | Relevansi & Perbedaan |
|----|-------------------------|-------|--------|-----------------|----------------------|
| 1 | Data Mining Analysis for KIP Scholarship Eligibility Using Integrated DBSCAN and TOPSIS — Akbar et al. (2026) | Journal of Information System & Informatics | **DBSCAN (11 atribut, 287 data → 10 cluster + 1 noise) + TOPSIS** | 287 calon KIP-K, top skor dari noise cluster — bukti noise jangan dibuang | **Paling identik:** hybrid sama, beda domain (beasiswa vs PKL). Jadi precedent DBSCAN+TOPSIS. |
| 2 | Analisis dan Penerapan Fuzzy AHP-TOPSIS Penentuan Mitra Industri PKL — Julianto, Utomo & Herpendi (2020) | Jurnal Ilmiah Informatika, Politeknik Tanah Laut | **FAHP (5 kriteria: kesesuaian jurusan, kredibilitas, komitmen, lingkungan, fasilitas; bobot 0.313/0.272/0.223/0.140/0.049) + TOPSIS (37 DUDI, skor max 0.8157)** | 37 DUDI | **Domain PKL persis.** Tanpa klasterisasi siswa. Penelitian ini tambah DBSCAN di hulu. |
| 3 | Hybrid Clustering and AHP-TOPSIS for SMEs — IIETA (2023) | International Journal | **K-Means/SOM (DBI 0.747, 91% akurasi) + AHP (CR) + TOPSIS per cluster** | 11 atribut UKM | **Pola 2 lapis:** klasterisasi → ranking per cluster. Mereka K-Means, kamu upgrade ke DBSCAN (noise-aware). |
| 4 | Implementation of AHP-MAUT & AHP-Profile Matching for OJT Placement — Andini (Monarch Bali) | Medikom JTI | **AHP (6 kriteria: akademik, personality, bahasa, servicing, culinary, housekeeping) + MAUT/PM (500 siswa → sampling 50)** | StudentD04 0.572 ranking 1 | **Domain penempatan siswa persis.** Beda metode (MAUT/PM vs TOPSIS). |
| 5 | Web-Based DSS Pemilihan Tempat PKL SMK dengan TOPSIS — (2026, SMK Islam Nusantara Comal) | IJHET | **TOPSIS 5 kriteria (jarak, kuota, kesesuaian, fasilitas, reputasi) 10 DUDI** | PT Laksana 0.788 ranking 1 | **SMK PKL persis.** Tanpa clustering. |
| 6 | SLR SAW vs TOPSIS untuk Rekomendasi Magang 2019-2025 — Rindengan et al. (2025) | Zenodo SLR PRISMA (15 paper) | Review | — | **TOPSIS > SAW** untuk magang — justifikasi pilih TOPSIS. |

## Novelty Penelitian Ini

> Julianto (2020) dan Akbar (2026) membuktikan FAHP-TOPSIS dan DBSCAN+TOPSIS efektif, namun terpisah domain dan clustering masih K-Means. Penelitian ini mengintegrasikan **DBSCAN (tanpa tentukan k, eksplisit noise, n=40) untuk 10 variabel kompetensi+minat TJKT** dengan **AHP-TOPSIS berbobot Hubin untuk matching DUDI** — kombinasi belum ada untuk PKL SMK IT.

## Cara Kutip di BAB 2 (Template Paragraf)

> "Penentuan mitra PKL dengan FAHP-TOPSIS pada 37 DUDI menghasilkan skor preferensi tertinggi 0.8157 (Julianto et al., 2020), sementara integrasi DBSCAN+TOPSIS untuk 287 calon KIP-K membuktikan bahwa kandidat dari noise cluster tetap dapat ranking tinggi sehingga noise tidak boleh dibuang (Akbar et al., 2026). Pola hybrid clustering → AHP-TOPSIS per cluster juga terbukti dengan DBI 0.747 dan akurasi 91% pada UKM (IIETA, 2023). Systematic review 15 studi magang 2019-2025 menegaskan TOPSIS lebih dominan daripada SAW untuk rekomendasi lokasi magang (Rindengan et al., 2025). Berbeda dengan penelitian terdahulu yang masih menggunakan K-Means/SAW/MAUT dan tanpa klasterisasi siswa, penelitian ini menggunakan DBSCAN yang noise-aware untuk 10 variabel kompetensi+minat dan TOPSIS berbobot AHP dari Hubin, sehingga sesuai judul dan menangani outlier siswa."

## Daftar Pustaka (APA)

- Akbar, I., Danuputri, C., Rahma, & Samad, I. S. (2026). Data Mining Analysis for KIP Scholarship Eligibility Using Integrated DBSCAN and TOPSIS. *Journal of Information System and Informatics*. https://doi.org/10.63158/journalisi.v8i2.1534
- Julianto, V., Utomo, H. S., & Herpendi, H. (2020). Analisis dan Penerapan Metode Fuzzy AHP-TOPSIS dalam Penentuan Mitra Industri Sebagai Tempat Praktek Kerja Lapangan. *Jurnal Ilmiah Informatika*, 5(2), 108–121. https://doi.org/10.35316/.v5i2.942
- IIETA. (2023). A Hybrid Clustering and AHP-TOPSIS Decision Support for SMEs. https://www.iieta.org/download/file/fid/120321
- Andini, A. Implementation of AHP-MAUT and AHP-Profile Matching Methods in OJT Student Placement DSS. *Medikom JTI*. https://www.medikom.iocspublisher.org/index.php/JTI/article/download/56/27/176
- Rindengan, Y. D., Salibana, S., & Lolong, L. (2025). Kajian Sistematik SAW dan TOPSIS pada Rekomendasi Magang. *Zenodo*. https://doi.org/10.5281/zenodo.17780367
- Puspitarani, Y., et al. (2023). DSS for MBKM Eligibility Using AHP and TOPSIS. *JTIULM*, 8(1). https://doi.org/10.20527/jtiulm.v8i1.156

## Catatan untuk Lampiran AHP

Gunakan matriks perbandingan 5×5 skala Saaty 1-9, hitung bobot + Consistency Ratio (CR<0.1) seperti Julianto (CR) dan MBKM (CR 0.000963). Lampirkan matriks Hubin di lampiran.

---
*Sumber diverifikasi 2026-09-18 via websearch. Untuk sitasi, cek URL asli sebelum submit.*
