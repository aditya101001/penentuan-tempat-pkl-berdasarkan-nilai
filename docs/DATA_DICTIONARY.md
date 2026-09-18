# Kamus Data

## dataset_siswa.xlsx — sheet `Siswa`

| Kolom | Tipe | Rentang | Wajib | Dipakai clustering | Keterangan |
|-------|------|---------|-------|--------------------|------------|
| `ID_Siswa` | string | S001… | Ya | Tidak | Identifier anonim |
| `Nama` | string | — | Tidak | Tidak | Internal saja |
| `Programming_X` | numeric | 0–100 | Ya | **Ya** | Nilai PPLG kelas X |
| `Software_X` | numeric | 0–100 | Ya | **Ya** | Nilai PPLG kelas X |
| `SistemOperasi_XI` | numeric | 0–100 | Ya | **Ya** | Nilai TJKT XI |
| `Jaringan_XI` | numeric | 0–100 | Ya | **Ya** | Nilai TJKT XI |
| `Troubleshooting_XI` | numeric | 0–100 | Ya | **Ya** | Nilai TJKT XI |
| `Keamanan_XI` | numeric | 0–100 | Ya | **Ya** | Nilai TJKT XI |
| `Minat_Programming` | int | 1–5 | Ya | **Ya** | Kuesioner |
| `Minat_Networking` | int | 1–5 | Ya | **Ya** | Kuesioner |
| `Minat_Support` | int | 1–5 | Ya | **Ya** | Kuesioner |
| `Minat_Cybersecurity` | int | 1–5 | Ya | **Ya** | Kuesioner |
| `Kedisiplinan` | int | 1–4 | Tidak | Tidak | Sikap opsional |
| `KerjaSama` | int | 1–4 | Tidak | Tidak | Sikap opsional |
| `Penilaian_Guru` | string | Software/Network/Support/Design | Tidak | Tidak | Validasi kualitatif |

10 variabel inti = 6 nilai + 4 minat (bold). `FEATURE_COLS` di `config.py`.

Contoh 3 baris dummy:

| ID | Programming_X | Jaringan_XI | Minat_Programming | Minat_Networking | Penilaian_Guru |
|----|---------------|-------------|-------------------|------------------|----------------|
| S001 | 84 | 58 | 5 | 2 | Software |
| S002 | 55 | 88 | 2 | 5 | Network |
| S003 | 62 | 70 | 2 | 3 | Support |

## dataset_dudi.xlsx — sheet `DUDI`

| Kolom | Tipe | Rentang | Keterangan |
|-------|------|---------|------------|
| `Nama_DUDI` | string | unik | Nama perusahaan/mitra |
| `Networking` | int 1–5 | kebutuhan jaringan |
| `Support` | int 1–5 | IT support |
| `Server_Cloud` | int 1–5 | server/cloud |
| `Programming` | int 1–5 | programming |
| `Cybersecurity` | int 1–5 | keamanan |

Contoh: `PT Jaringan Nusantara | 5 | 3 | 4 | 2 | 4`

## Aturan Validasi
- Missing → drop baris + warning + log jumlah drop
- Tipe salah → coerce numeric, gagal → drop + pesan baris
- Di luar rentang → warning + drop baris
- `Penilaian_Guru` kosong → skip validasi kualitatif (warning, bukan error)
