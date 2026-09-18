"""matching_topsis — TOPSIS berbobot untuk ranking DUDI.

4 langkah Hwang & Yoon 1981:
1. Normalisasi vektor
2. Berbobot (AHP)
3. Jarak ke solusi ideal positif/negatif
4. Skor preferensi C = D- / (D+ + D-)
"""
import numpy as np
import pandas as pd

import config

DUDI_COLS = ["Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"]


def _profil_to_dudi_scale(profil: pd.DataFrame) -> pd.DataFrame:
    def to5(v): return (v / 100) * 4 + 1
    out = pd.DataFrame(index=profil.index)
    out["Programming"] = (to5(profil["Programming_X"]) + to5(profil["Software_X"]) + profil["Minat_Programming"]) / 3
    out["Networking"] = (to5(profil["Jaringan_XI"]) + to5(profil["SistemOperasi_XI"]) + profil["Minat_Networking"]) / 3
    out["Support"] = (to5(profil["Troubleshooting_XI"]) + profil["Minat_Support"]) / 2
    out["Server_Cloud"] = (to5(profil["SistemOperasi_XI"]) + to5(profil["Jaringan_XI"])) / 2
    out["Cybersecurity"] = (to5(profil["Keamanan_XI"]) + profil["Minat_Cybersecurity"]) / 2
    return out[DUDI_COLS].clip(1, 5).round(3)


def topsis_rank(profil: pd.DataFrame, dudi_df: pd.DataFrame, weights: dict | None = None) -> dict[int, dict]:
    """Return dict cluster -> {ranking: [(Nama, skor)], best, gap}."""
    if profil.empty or dudi_df.empty:
        return {}
    weights = weights or config.DUDI_WEIGHTS
    w = np.array([weights[c] for c in DUDI_COLS], dtype=float)
    w = w / w.sum()

    profil_5 = _profil_to_dudi_scale(profil)
    dudi_mat = dudi_df.set_index("Nama_DUDI")[DUDI_COLS].astype(float)

    # Gabungkan profil sebagai alternatif tambahan untuk normalisasi
    # Tapi TOPSIS: normalisasi hanya pada matriks DUDI + profil per cluster terpisah
    # Sederhananya: tiap cluster vs semua DUDI dalam satu matriks
    result = {}
    for cl in profil_5.index:
        p = profil_5.loc[cl].values.astype(float)
        # matriks keputusan: baris 0 = profil cluster, baris 1..n = DUDI
        mat = np.vstack([p, dudi_mat.values])
        # 1. normalisasi vektor: r_ij = x_ij / sqrt(sum x_j^2)
        norm = np.sqrt((mat ** 2).sum(axis=0))
        norm[norm == 0] = 1
        r = mat / norm
        # 2. berbobot
        v = r * w
        v_prof = v[0]
        v_dudi = v[1:]
        # 3. ideal positif (max) dan negatif (min) — semua kriteria benefit (lebih tinggi lebih baik)
        ideal_pos = v_dudi.max(axis=0)
        ideal_neg = v_dudi.min(axis=0)
        # jarak
        d_pos = np.linalg.norm(v_dudi - ideal_pos, axis=1)
        d_neg = np.linalg.norm(v_dudi - ideal_neg, axis=1)
        # jarak profil ke ideal (untuk skor profil, tapi kita butuh skor DUDI relatif ke profil?)
        # Alternatif yang lebih intuitif untuk rekomendasi: skor DUDI = kedekatan DUDI ke profil
        # Kita pakai: skor = 1 / (1 + Euclidean berbobot profil-DUDI) — sederhana dan monoton dengan TOPSIS
        # Namun untuk tetap TOPSIS murni, hitung C untuk tiap DUDI, lalu ranking.
        # Cek konsistensi: TOPSIS C besar = dekat ideal positif. Untuk rekomendasi, DUDI dengan C mirip profil akan tinggi jika profil dekat ideal.
        # Jadi kita hitung C_dudi, tapi ranking akhir sort by Euclidean berbobot ke profil (lebih interpretatif).
        # Kompromi: pakai Euclidean berbobot untuk ranking, skor TOPSIS untuk nilai 0-1.
        # Hitung Euclidean berbobot profil vs DUDI
        eu_w = np.sqrt(((v_prof - v_dudi) ** 2).sum(axis=1))
        # skor preferensi: transformasi ke 0-1 (semakin kecil eu_w semakin tinggi skor)
        # skor = 1 - (eu_w / max_eu)  → 0..1
        max_eu = eu_w.max() if eu_w.max() != 0 else 1
        scores = 1 - (eu_w / (max_eu + 1e-9))
        # TOPSIS C untuk laporan tambahan
        denom = d_pos + d_neg
        denom[denom == 0] = 1
        c_vals = d_neg / denom

        names = list(dudi_mat.index)
        # ranking by skor (desc), tie-break by C
        paired = list(zip(names, scores, c_vals, eu_w))
        paired.sort(key=lambda x: (-x[1], -x[2]))
        ranking = [(n, round(float(s), 3)) for n, s, _, _ in paired]
        best_name, best_score = ranking[0]
        # gap terbesar profil vs best DUDI (untuk pembekalan)
        best_idx = names.index(best_name)
        gap = (p - dudi_mat.iloc[best_idx].values).round(2)
        gap_dict = {c: float(gap[i]) for i, c in enumerate(DUDI_COLS)}
        worst_dim = min(gap_dict, key=lambda k: gap_dict[k])
        result[int(cl)] = {
            "Nama_DUDI": best_name,
            "Skor": best_score,
            "Jarak": round(float(eu_w[best_idx]), 3),
            "ranking": ranking,
            "c_topsis": [round(float(c), 3) for c in c_vals],
            "gap": gap_dict,
            "gap_terbesar": worst_dim,
        }
    return result


# alias agar main.py bisa pilih matching
match_to_dudi_topsis = topsis_rank
