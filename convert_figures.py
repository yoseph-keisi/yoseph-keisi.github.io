#!/usr/bin/env python3
"""
Convert TIFF and PDF figures to PNG for browser compatibility.
Run once: python convert_figures.py
"""
from pathlib import Path

FIGURES = Path(r'c:\Users\ykeis\OneDrive\Desktop\yoseph-keisi.github.io-main\Figures')

TIFFS = [
    'Figure_Pressure_Comparison.tiff',
    'Figure_TKE_Comparison.tiff',
    'final_nearbody_tke_chordwise_AIAA.tiff',
    'robustness_overlay.tiff',
]

PDFS = [
    '5-parameter-equation-characterization.pdf',
]

# ── TIFF → PNG via Pillow ────────────────────────────────────────
try:
    from PIL import Image
    for fname in TIFFS:
        src = FIGURES / fname
        dst = FIGURES / (Path(fname).stem + '.png')
        if not src.exists():
            print(f'SKIP (missing): {fname}')
            continue
        img = Image.open(src)
        img = img.convert('RGB')
        img.save(dst, 'PNG', optimize=True)
        size_kb = dst.stat().st_size // 1024
        print(f'OK  {fname}  ->  {dst.name}  ({size_kb} KB)')
except ImportError:
    print('Pillow not found. Install with:  pip install pillow')

# -- PDF -> PNG via PyMuPDF (preferred) or pdf2image fallback -----
for fname in PDFS:
    src = FIGURES / fname
    dst = FIGURES / (Path(fname).stem + '.png')
    if not src.exists():
        print(f'SKIP (missing): {fname}')
        continue
    converted = False
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(src))
        page = doc[0]
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        pix.save(str(dst))
        doc.close()
        size_kb = dst.stat().st_size // 1024
        print(f'OK (PyMuPDF): {fname} -> {dst.name} ({size_kb} KB)')
        converted = True
    except ImportError:
        pass
    if not converted:
        try:
            from pdf2image import convert_from_path
            pages = convert_from_path(str(src), dpi=200)
            if pages:
                pages[0].save(dst, 'PNG')
                size_kb = dst.stat().st_size // 1024
                print(f'OK (pdf2image): {fname} -> {dst.name} ({size_kb} KB)')
        except ImportError:
            print('No PDF converter found. Install: pip install pymupdf')
