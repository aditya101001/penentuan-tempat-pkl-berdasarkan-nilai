"""matching — normalisasi profil cluster ke skala DUDI 1-5 & Euclidean."""
import numpy as np
import pandas as pd

DUDI_COLS = ["Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"]

# mapping profil (skala asli) ke DUDI 1-5
# nilai 0-100 → 1-5 : (x/100)*4+1 ; minat sudah 1-5
def _profil_to_dudi_scale(profil: pd.DataFrame) -> pd.DataFrame:
    """Normalisasi profil cluster ke skala 1-5 per dimensi DUDI."""
    # Ambil rata-rata yang relevan
    # Programming DUDI ← Programming_X, Software_X, Minat_Programming
    # Networking ← Jaringan_XI, SistemOperasi_XI, Minat_Networking
    # Support ← Troubleshooting_XI, Minat_Support
    # Server_Cloud ← SistemOperasi_XI, Jaringan_XI (infra)
    # Cybersecurity ← Keamanan_XI, Minat_Cybersecurity
    out = pd.DataFrame(index=profil.index)
    # helper: 0-100 → 1-5
    def to5(v): return (v / 100) * 4 + 1
    out["Programming"] = (to5(profil["Programming_X"]) + to5(profil["Software_X"]) + profil["Minat_Programming"]) / 3
    out["Networking"] = (to5(profil["Jaringan_XI"]) + to5(profil["SistemOperasi_XI"]) + profil["Minat_Networking"]) / 3
    out["Support"] = (to5(profil["Troubleshooting_XI"]) + profil["Minat_Support"]) / 2
    out["Server_Cloud"] = (to5(profil["SistemOperasi_XI"]) + to5(profil["Jaringan_XI"])) / 2
    out["Cybersecurity"] = (to5(profil["Keamanan_XI"]) + profil["Minat_Cybersecurity"]) / 2
    # clamp 1-5
    out = out.clip(1, 5).round(2)
    return out[DUDI_COLS]


def match_to_dudi(profil: pd.DataFrame, dudi_df: pd.DataFrame) -> dict[int, dict]:
    """Untuk tiap cluster, hitung Euclidean ke tiap DUDI, return dict cluster→{Nama_DUDI, jarak, ranking}.

    Jika profil kosong → return {}.
    Honey: O(n_clusters * n_dudi), fine untuk n<100.
    """
    if profil.empty or dudi_df.empty:
        return {}
    profil_5 = _profil_to_dudi_scale(profil)
    dudi_mat = dudi_df.set_index("Nama_DUDI")[DUDI_COLS].astype(float)

    result: dict[int, dict] = {}
    for cl in profil_5.index:
        p = profil_5.loc[cl].values.astype(float)
        dists = {}
        for nama, row in dudi_mat.iterrows():
            d = float(np.linalg.norm(p - row.values.astype(float)))
            dists[nama] = round(d, 3)
        sorted_d = sorted(dists.items(), key=lambda x: x[1])
        best_nama, best_dist = sorted_d[0]
        result[int(cl)] = {"Nama_DUDI": best_nama, "Jarak": best_dist, "ranking": sorted_d}
    return result
