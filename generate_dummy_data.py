#!/usr/bin/env python3
"""Generate dataset dummy untuk uji pipeline sebelum data asli tersedia.

Usage:
    python generate_dummy_data.py --n 40 --seed 42
    python generate_dummy_data.py --n 40 --seed 42 --out dataset_siswa.xlsx --dudi dataset_dudi.xlsx
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SISWA_COLS = [
    "ID_Siswa", "Nama",
    "Programming_X", "Software_X", "SistemOperasi_XI", "Jaringan_XI",
    "Troubleshooting_XI", "Keamanan_XI",
    "Minat_Programming", "Minat_Networking", "Minat_Support", "Minat_Cybersecurity",
    "Kedisiplinan", "KerjaSama", "Penilaian_Guru",
]

DUDI_COLS = ["Nama_DUDI", "Networking", "Support", "Server_Cloud", "Programming", "Cybersecurity"]

DUDI_TEMPLATE = [
    ["PT Jaringan Nusantara", 5, 3, 4, 2, 4],
    ["CV Solusi IT Support", 3, 5, 2, 3, 2],
    ["Cloud & Data Center ID", 4, 2, 5, 3, 5],
    ["Software House Malang", 2, 3, 3, 5, 2],
    ["Cyber Security Lab", 3, 2, 4, 4, 5],
    ["StarNet ISP", 5, 4, 3, 1, 3],
]


def _clip(v, lo, hi):
    return int(np.clip(round(v), lo, hi))


def generate_siswa(n: int = 40, seed: int = 42) -> pd.DataFrame:
    """Generate n baris siswa dengan 3 persona + noise. Return DataFrame."""
    rng = np.random.default_rng(seed)
    rows = []
    # proporsi persona: 35% programmer, 35% network, 30% support
    for i in range(n):
        pid = f"S{i+1:03d}"
        nama = f"Siswa {i+1}"
        r = rng.random()
        # noise 8%: acak semua rendah/inkonsisten
        is_noise = r < 0.08
        if is_noise:
            prog = _clip(rng.normal(55, 15), 0, 100)
            soft = _clip(rng.normal(55, 15), 0, 100)
            so = _clip(rng.normal(55, 15), 0, 100)
            jar = _clip(rng.normal(55, 15), 0, 100)
            tro = _clip(rng.normal(55, 15), 0, 100)
            kea = _clip(rng.normal(55, 15), 0, 100)
            mp = _clip(rng.integers(1, 6), 1, 5)
            mn = _clip(rng.integers(1, 6), 1, 5)
            ms = _clip(rng.integers(1, 6), 1, 5)
            mc = _clip(rng.integers(1, 6), 1, 5)
            guru = rng.choice(["Software", "Network", "Support", "Design"])
        elif r < 0.38:  # programmer
            prog = _clip(rng.normal(82, 8), 0, 100)
            soft = _clip(rng.normal(80, 8), 0, 100)
            so = _clip(rng.normal(62, 10), 0, 100)
            jar = _clip(rng.normal(58, 10), 0, 100)
            tro = _clip(rng.normal(60, 10), 0, 100)
            kea = _clip(rng.normal(60, 10), 0, 100)
            mp = _clip(rng.normal(4.3, 0.6), 1, 5)
            mn = _clip(rng.normal(2.2, 0.7), 1, 5)
            ms = _clip(rng.normal(2.5, 0.7), 1, 5)
            mc = _clip(rng.normal(2.4, 0.7), 1, 5)
            guru = "Software"
        elif r < 0.73:  # network
            prog = _clip(rng.normal(58, 10), 0, 100)
            soft = _clip(rng.normal(60, 10), 0, 100)
            so = _clip(rng.normal(82, 7), 0, 100)
            jar = _clip(rng.normal(85, 7), 0, 100)
            tro = _clip(rng.normal(78, 8), 0, 100)
            kea = _clip(rng.normal(72, 8), 0, 100)
            mp = _clip(rng.normal(2.3, 0.7), 1, 5)
            mn = _clip(rng.normal(4.4, 0.5), 1, 5)
            ms = _clip(rng.normal(3.2, 0.7), 1, 5)
            mc = _clip(rng.normal(3.5, 0.7), 1, 5)
            guru = "Network"
        else:  # support
            prog = _clip(rng.normal(60, 10), 0, 100)
            soft = _clip(rng.normal(62, 10), 0, 100)
            so = _clip(rng.normal(70, 9), 0, 100)
            jar = _clip(rng.normal(68, 9), 0, 100)
            tro = _clip(rng.normal(82, 7), 0, 100)
            kea = _clip(rng.normal(78, 8), 0, 100)
            mp = _clip(rng.normal(2.5, 0.7), 1, 5)
            mn = _clip(rng.normal(3.0, 0.7), 1, 5)
            ms = _clip(rng.normal(4.3, 0.5), 1, 5)
            mc = _clip(rng.normal(3.0, 0.7), 1, 5)
            guru = "Support"

        rows.append([pid, nama, prog, soft, so, jar, tro, kea, mp, mn, ms, mc,
                     _clip(rng.integers(2, 5), 1, 4), _clip(rng.integers(2, 5), 1, 4), guru])

    df = pd.DataFrame(rows, columns=SISWA_COLS)
    return df


def generate_dudi() -> pd.DataFrame:
    df = pd.DataFrame(DUDI_TEMPLATE, columns=DUDI_COLS)
    return df


def main():
    p = argparse.ArgumentParser(description="Generate dummy dataset siswa & DUDI")
    p.add_argument("--n", type=int, default=40, help="Jumlah siswa (default 40)")
    p.add_argument("--seed", type=int, default=42, help="Random seed")
    p.add_argument("--out", type=str, default="dataset_siswa.xlsx", help="Output siswa")
    p.add_argument("--dudi", type=str, default="dataset_dudi.xlsx", help="Output dudi")
    p.add_argument("--force", action="store_true", help="Overwrite jika file ada")
    args = p.parse_args()

    out_siswa = Path(args.out)
    out_dudi = Path(args.dudi)

    if out_siswa.exists() and not args.force:
        print(f"[warn] {out_siswa} sudah ada — gunakan --force untuk overwrite. Skip.")
    else:
        df = generate_siswa(n=args.n, seed=args.seed)
        df.to_excel(out_siswa, index=False, sheet_name="Siswa")
        print(f"[ok] {out_siswa} — {len(df)} baris")

    if out_dudi.exists() and not args.force:
        print(f"[warn] {out_dudi} sudah ada — skip (pakai --force untuk overwrite)")
    else:
        dudi = generate_dudi()
        dudi.to_excel(out_dudi, index=False, sheet_name="DUDI")
        print(f"[ok] {out_dudi} — {len(dudi)} baris")


if __name__ == "__main__":
    main()
