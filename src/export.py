"""export — tulis 3 Excel sesuai PRD §8."""
from pathlib import Path

import pandas as pd
import numpy as np

import config


def _style_excel(path: Path):
    """Auto-fit kolom & freeze header via openpyxl."""
    try:
        from openpyxl import load_workbook
        wb = load_workbook(path)
        for ws in wb.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            for col in ws.columns:
                max_len = max(len(str(c.value)) if c.value else 0 for c in col)
                ws.column_dimensions[col[0].column_letter].width = min(max_len + 2, 30)
        wb.save(path)
    except Exception:
        pass  # style gagal bukan fatal


def export_results(df_siswa: pd.DataFrame, labels: np.ndarray, profil: pd.DataFrame,
                   dudi_match: dict, out_dir: str | Path | None = None):
    """Export 3 Excel. Return dict paths."""
    out_dir = Path(out_dir) if out_dir else Path(config.OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    # mapping cluster → kategori & DUDI
    from src.profiling import assign_kategori
    kategori_map = assign_kategori(profil) if not profil.empty else {}

    # 1. hasil_klasterisasi.xlsx
    hasil = df_siswa.copy()
    hasil["Cluster"] = labels
    hasil["Kategori"] = [kategori_map.get(int(l), "Noise" if l == -1 else "Unknown") for l in labels]
    hasil["Rekomendasi_DUDI"] = [dudi_match.get(int(l), {}).get("Nama_DUDI", "-") if l != -1 else "-" for l in labels]
    hasil["Jarak_DUDI"] = [dudi_match.get(int(l), {}).get("Jarak", None) if l != -1 else None for l in labels]
    # TOPSIS Skor jika ada
    if any("Skor" in v for v in dudi_match.values()):
        hasil["Skor_TOPSIS"] = [dudi_match.get(int(l), {}).get("Skor", None) if l != -1 else None for l in labels]
        hasil["Ranking_Top3"] = ["; ".join([f"{n}({s})" for n, s in dudi_match.get(int(l), {}).get("ranking", [])[:3]]) if l != -1 else "-" for l in labels]
    p1 = out_dir / "hasil_klasterisasi.xlsx"
    hasil.to_excel(p1, index=False, sheet_name="Hasil")
    _style_excel(p1)

    # 2. profil_cluster.xlsx
    p2 = out_dir / "profil_cluster.xlsx"
    if not profil.empty:
        prof_out = profil.copy()
        prof_out["Kategori"] = [kategori_map.get(int(i), "-") for i in prof_out.index]
        prof_out["Rekomendasi_DUDI"] = [dudi_match.get(int(i), {}).get("Nama_DUDI", "-") for i in prof_out.index]
        prof_out["Jarak_DUDI"] = [dudi_match.get(int(i), {}).get("Jarak", None) for i in prof_out.index]
        if any("Skor" in v for v in dudi_match.values()):
            prof_out["Skor_TOPSIS"] = [dudi_match.get(int(i), {}).get("Skor", None) for i in prof_out.index]
            prof_out["Ranking_Top3"] = ["; ".join([f"{n}({s})" for n, s in dudi_match.get(int(i), {}).get("ranking", [])[:3]]) for i in prof_out.index]
            prof_out["Gap_Terbesar"] = [dudi_match.get(int(i), {}).get("gap_terbesar", "-") for i in prof_out.index]
        prof_out.to_excel(p2, sheet_name="Profil")
    else:
        pd.DataFrame({"info": ["Tidak ada cluster (semua noise)"]}).to_excel(p2, index=False)
    _style_excel(p2)

    # 3. laporan_noise.xlsx
    p3 = out_dir / "laporan_noise.xlsx"
    noise_df = hasil[hasil["Cluster"] == -1].copy()
    if noise_df.empty:
        # tetap buat file dengan header
        pd.DataFrame(columns=hasil.columns).to_excel(p3, index=False)
    else:
        noise_df.to_excel(p3, index=False)
    _style_excel(p3)

    return {"hasil": p1, "profil": p2, "noise": p3}
