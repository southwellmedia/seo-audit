#!/usr/bin/env python3
"""Pre-delivery check for an audit PDF.

Usage:
    python3 check_pdf.py Client_SEO_Audit.pdf [--out-dir pages/]

Renders every page to PNG (so you can look at them), writes a contact sheet of all
pages, and flags problems that are easy to miss: near-empty pages, leftover
placeholders, and text that suggests a data bug ("None", "nan", "{", "[City]").

Exit code is 1 when a problem is found. Always look at the PNGs too — this catches
mechanical problems, not layout taste.

Requires: pypdfium2 and Pillow (pip install pypdfium2 pillow).
"""
import argparse
import re
import sys
from pathlib import Path

try:
    import pypdfium2 as pdfium
    from PIL import Image, ImageStat
except ImportError:
    sys.exit("Missing dependency. Run: pip install pypdfium2 pillow "
             "(add --break-system-packages if pip refuses).")

SUSPICIOUS = [
    # whole-line only: "None of the competitors…" is fine English
    (r"(?m)^\s*(None|nan|NaN|null|undefined)\s*$", "None/nan/null leaked in as a whole cell"),
    (r"[{}]", "curly brace — unfilled template or raw JSON"),
    (r"\[(City|Service|Client|Neighborhood|Brand Name|Year|agency_name)\]", "unfilled [placeholder]"),
    (r"\bTODO\b|\bTBD\b|lorem ipsum", "draft marker"),
    (r"555-\d{4}", "555 phone number — confirm it's quoted as a finding, not the agency's contact"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--out-dir", help="where to write page PNGs (default: <pdf>_pages/)")
    ap.add_argument("--scale", type=float, default=1.2, help="render scale (1.0 = 72 dpi)")
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    out_dir = Path(args.out_dir) if args.out_dir else pdf_path.with_name(pdf_path.stem + "_pages")
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = pdfium.PdfDocument(str(pdf_path))
    problems, notes, thumbs = [], [], []
    for i in range(len(doc)):
        page = doc[i]
        n = i + 1
        img = page.render(scale=args.scale).to_pil().convert("RGB")
        img.save(out_dir / f"page-{n:02d}.png")
        thumbs.append(img)

        text = page.get_textpage().get_text_range()
        words = len(text.split())
        # near-empty page check (cover excluded): little text AND mostly white pixels
        ink = 255 - ImageStat.Stat(img.convert("L")).mean[0]
        if n > 1 and words < 25 and ink < 6:
            problems.append(f"page {n}: nearly empty ({words} words) — likely a stray page break")
        for pattern, why in SUSPICIOUS:
            for m in re.finditer(pattern, text, flags=re.IGNORECASE if "lorem" in pattern else 0):
                snippet = text[max(0, m.start() - 30): m.end() + 30].replace("\n", " ").replace("\r", " ")
                target = notes if pattern.startswith("555") else problems
                target.append(f"page {n}: {why}: …{snippet.strip()}…")
                break

    # contact sheet: 4 across
    cols = 4
    tw = 300
    th = int(tw * thumbs[0].height / thumbs[0].width)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 10, rows * th + (rows + 1) * 10), (200, 204, 210))
    for idx, t in enumerate(thumbs):
        r, c = divmod(idx, cols)
        sheet.paste(t.resize((tw, th)), (10 + c * (tw + 10), 10 + r * (th + 10)))
    sheet_path = out_dir / "contact-sheet.png"
    sheet.save(sheet_path)

    print(f"{len(doc)} pages rendered to {out_dir}/")
    print(f"contact sheet: {sheet_path}")
    for p in problems:
        print("PROBLEM:", p)
    for n in notes:
        print("check:", n)
    if not problems:
        print("no mechanical problems found — now look at the pages")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
