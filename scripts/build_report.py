#!/usr/bin/env python3
"""Render an SEO audit PDF from a findings JSON file.

Usage:
    python3 build_report.py findings.json [-o Client_SEO_Audit.pdf]

The findings format is documented in references/deliverables.md and shown in
assets/findings.example.json. Missing optional sections are skipped; missing
required fields stop the build with a list of what to fill in.

Requires: reportlab (pip install reportlab).
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Frame, KeepTogether,
                                    NextPageTemplate, PageBreak, PageTemplate, Paragraph,
                                    Spacer, Table, TableStyle)
    from reportlab.platypus.tableofcontents import TableOfContents
except ImportError:
    sys.exit("reportlab is not installed. Run: pip install reportlab "
             "(add --break-system-packages if pip refuses).")

HERE = Path(__file__).resolve().parent
FONT_DIR = HERE.parent / "assets" / "fonts"

PAGE_W, PAGE_H = letter
MARGIN = 0.8 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

INK = colors.HexColor("#1B1F24")
MUTED = colors.HexColor("#5B6470")
RULE = colors.HexColor("#E3E6EA")
ZEBRA = colors.HexColor("#F6F7F9")

RATING_STYLE = {
    "FAIL": ("#B42318", "#FEECEB"),
    "WARN": ("#9A5B00", "#FFF4DE"),
    "PASS": ("#1E7A46", "#E7F6EC"),
    "N/A": ("#5B6470", "#EEF0F3"),
}
SEVERITY_STYLE = {
    "blocker": ("#B42318", "#FEECEB"),
    "high": ("#B42318", "#FEECEB"),
    "medium": ("#9A5B00", "#FFF4DE"),
    "low": ("#5B6470", "#EEF0F3"),
}
MATRIX_VALUES = {"yes": ("Yes", "#1E7A46"), "no": ("No", "#B42318"),
                 "partial": ("Partial", "#9A5B00")}

# Characters the bundled font lacks → safe replacements.
GLYPH_FIXES = {"✓": "Yes", "✔": "Yes", "✗": "No", "✘": "No", "●": "•", "≤": "<=",
               "≥": ">=", "★": "*", "​": ""}

TIER_NAMES = {1: "Tier 1 — Primary Core", 2: "Tier 2 — Local / Neighborhood",
              3: "Tier 3 — Long-Tail High-Intent", 4: "Tier 4 — Informational / Blog"}


# ---------------------------------------------------------------- color helpers
def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c * 255))):02x}" for c in rgb)


def luminance(h):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(h, other, t):
    a, b = hex_to_rgb(h), hex_to_rgb(other)
    return rgb_to_hex(tuple(x + (y - x) * t for x, y in zip(a, b)))


def readable_on_white(h, target=4.5):
    """Darken a brand color until it's readable as text on white."""
    c = h
    for _ in range(20):
        if contrast(c, "#ffffff") >= target:
            return c
        c = mix(c, "#000000", 0.12)
    return c


def text_on(h):
    return "#ffffff" if contrast(h, "#ffffff") >= contrast(h, "#1B1F24") else "#1B1F24"


class Palette:
    def __init__(self, brand):
        primary = self._valid(brand.get("primary")) or "#1F4E8C"
        accent = self._valid(brand.get("accent")) or self._valid(brand.get("secondary")) or primary
        self.primary = primary
        self.primary_ink = readable_on_white(primary)          # headings, rules, numbers
        self.accent_ink = readable_on_white(accent)
        self.band = primary                                       # cover band / table header
        self.on_band = text_on(primary)
        self.tint = mix(primary, "#ffffff", 0.9)                  # stat bar background
        self.tint_strong = mix(primary, "#ffffff", 0.78)

    @staticmethod
    def _valid(v):
        if not isinstance(v, str):
            return None
        v = v.strip()
        if not re.fullmatch(r"#?([0-9a-fA-F]{6}|[0-9a-fA-F]{3})", v):
            return None
        return v if v.startswith("#") else "#" + v


# ---------------------------------------------------------------- fonts & styles
def register_fonts():
    files = {
        "Sans": "InstrumentSans-Regular.ttf",
        "Sans-Bold": "InstrumentSans-Bold.ttf",
        "Sans-Italic": "InstrumentSans-Italic.ttf",
        "Serif": "InstrumentSerif-Regular.ttf",
        "Serif-Italic": "InstrumentSerif-Italic.ttf",
    }
    try:
        for name, f in files.items():
            pdfmetrics.registerFont(TTFont(name, str(FONT_DIR / f)))
        pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold",
                                      italic="Sans-Italic", boldItalic="Sans-Bold")
        return {"sans": "Sans", "bold": "Sans-Bold", "italic": "Sans-Italic",
                "serif": "Serif", "serif_italic": "Serif-Italic"}
    except Exception as e:  # fall back to built-ins rather than failing the deliverable
        print(f"warning: bundled fonts not loaded ({e}); using Helvetica/Times", file=sys.stderr)
        return {"sans": "Helvetica", "bold": "Helvetica-Bold", "italic": "Helvetica-Oblique",
                "serif": "Times-Roman", "serif_italic": "Times-Italic"}


def make_styles(F, P):
    s = {}
    s["body"] = ParagraphStyle("body", fontName=F["sans"], fontSize=9.6, leading=14.2,
                               textColor=INK, spaceAfter=6)
    s["lead"] = ParagraphStyle("lead", parent=s["body"], fontSize=11.5, leading=17)
    s["muted"] = ParagraphStyle("muted", parent=s["body"], textColor=MUTED, fontSize=8.6, leading=12)
    s["h1"] = ParagraphStyle("h1", fontName=F["serif"], fontSize=30, leading=34,
                             textColor=INK, spaceAfter=4)
    s["kicker"] = ParagraphStyle("kicker", fontName=F["bold"], fontSize=8.5, leading=11,
                                 textColor=colors.HexColor(P.primary_ink), spaceAfter=2)
    s["h2"] = ParagraphStyle("h2", fontName=F["bold"], fontSize=12, leading=16,
                             textColor=INK, spaceBefore=12, spaceAfter=6)
    s["h3"] = ParagraphStyle("h3", fontName=F["bold"], fontSize=10, leading=14,
                             textColor=colors.HexColor(P.primary_ink), spaceBefore=8, spaceAfter=3)
    s["cell"] = ParagraphStyle("cell", fontName=F["sans"], fontSize=8.3, leading=11, textColor=INK)
    s["cell_b"] = ParagraphStyle("cell_b", parent=s["cell"], fontName=F["bold"])
    s["cell_head"] = ParagraphStyle("cell_head", parent=s["cell"], fontName=F["bold"],
                                    textColor=colors.HexColor(P.on_band))
    s["verdict"] = ParagraphStyle("verdict", fontName=F["serif_italic"], fontSize=17, leading=23,
                                  textColor=INK, spaceBefore=4, spaceAfter=4)
    s["stat_num"] = ParagraphStyle("stat_num", fontName=F["serif"], fontSize=28, leading=30,
                                   textColor=colors.HexColor(P.primary_ink), alignment=1)
    s["stat_label"] = ParagraphStyle("stat_label", fontName=F["bold"], fontSize=7.5, leading=9.5,
                                     textColor=MUTED, alignment=1)
    s["toc0"] = ParagraphStyle("toc0", fontName=F["sans"], fontSize=11, leading=22, textColor=INK)
    s["card_title"] = ParagraphStyle("card_title", fontName=F["bold"], fontSize=10.5, leading=14,
                                     textColor=INK, spaceAfter=3)
    return s


# ---------------------------------------------------------------- text helpers
def clean(text):
    """Escape for ReportLab's mini-markup and replace glyphs the font lacks."""
    if text is None:
        return ""
    t = str(text)
    for k, v in GLYPH_FIXES.items():
        t = t.replace(k, v)
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def P_(text, style):
    return Paragraph(clean(text), style)


def badge_cell(label, fg, bg, F):
    st = ParagraphStyle("b", fontName=F["bold"], fontSize=7.6, leading=10,
                        textColor=colors.HexColor(fg), alignment=1)
    return Paragraph(clean(label), st), colors.HexColor(bg)


def tier_of(k):
    """Keyword tier as an int; 0 when missing or not a number (validate() warns)."""
    try:
        return int(k.get("tier", 0))
    except (TypeError, ValueError):
        return 0


def fmt_hours(h):
    if h is None or h == "":
        return "—"
    try:
        h = float(h)
    except (TypeError, ValueError):
        return clean(h)
    if h < 1:
        return f"{round(h * 60)} min"
    if h >= 8 and h % 8 == 0:
        d = int(h // 8)
        return f"{d} day" + ("s" if d > 1 else "")
    return (f"{h:g} hr" + ("s" if h != 1 else ""))


# ---------------------------------------------------------------- document
class AuditDoc(BaseDocTemplate):
    def __init__(self, path, data, palette, fonts, **kw):
        super().__init__(path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=MARGIN + 0.15 * inch, bottomMargin=MARGIN,
                         title=f"{data['meta']['client_name']} — SEO Audit",
                         author=data["meta"].get("agency_name", ""), **kw)
        self.data, self.pal, self.F = data, palette, fonts
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="body",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([
            PageTemplate(id="cover", frames=[frame], onPage=self.draw_cover),
            PageTemplate(id="body", frames=[frame], onPage=self.draw_chrome),
        ])

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and getattr(f, "_toc_text", None):
            key = f"sec-{self.seq.nextf('sec')}"
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(f._toc_text, key, level=0)
            self.notify("TOCEntry", (0, f._toc_text, self.page, key))

    # cover drawn directly on the canvas
    def draw_cover(self, c, doc):
        m, pal, F = self.data["meta"], self.pal, self.F
        band_h = PAGE_H * 0.52
        c.saveState()
        c.setFillColor(colors.HexColor(pal.band))
        c.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
        on = colors.HexColor(pal.on_band)
        c.setFillColor(on)
        c.setFont(F["bold"], 9)
        c.drawString(MARGIN, PAGE_H - MARGIN, "SEO AUDIT & COMPETITIVE ANALYSIS")
        # client name — shrink to fit
        name = m["client_name"]
        size = 46
        while size > 22 and pdfmetrics.stringWidth(name, F["serif"], size) > CONTENT_W:
            size -= 2
        c.setFont(F["serif"], size)
        c.drawString(MARGIN, PAGE_H - band_h + 1.25 * inch, name)
        c.setFont(F["sans"], 11)
        sub = " · ".join(x for x in [m.get("url", "").replace("https://", "").replace("http://", "").rstrip("/"),
                                     m.get("market", "")] if x)
        c.drawString(MARGIN, PAGE_H - band_h + 0.85 * inch, sub)
        # lower half
        c.setFillColor(INK)
        y = PAGE_H - band_h - 0.9 * inch
        c.setFont(F["bold"], 8.5)
        c.setFillColor(MUTED)
        date_x = MARGIN + CONTENT_W / 2 if m.get("agency_name") else MARGIN
        if m.get("agency_name"):
            c.drawString(MARGIN, y, "PREPARED BY")
        c.drawString(date_x, y, "DATE")
        c.setFillColor(INK)
        c.setFont(F["serif"], 20)
        if m.get("agency_name"):
            c.drawString(MARGIN, y - 26, m["agency_name"])
        c.drawString(date_x, y - 26, m.get("date", ""))
        if m.get("business_model"):
            c.setFont(F["bold"], 8.5)
            c.setFillColor(MUTED)
            c.drawString(MARGIN, y - 72, "BUSINESS MODEL")
            c.setFillColor(INK)
            c.setFont(F["sans"], 11)
            c.drawString(MARGIN, y - 90, m["business_model"])
        c.setStrokeColor(colors.HexColor(pal.primary_ink))
        c.setLineWidth(2)
        c.line(MARGIN, MARGIN + 18, MARGIN + 0.6 * inch, MARGIN + 18)
        c.setFont(F["sans"], 8)
        c.setFillColor(MUTED)
        c.drawString(MARGIN, MARGIN, "Confidential — prepared for " + name)
        c.restoreState()

    def draw_chrome(self, c, doc):
        m, F = self.data["meta"], self.F
        c.saveState()
        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        top = PAGE_H - MARGIN + 0.05 * inch
        c.line(MARGIN, top, PAGE_W - MARGIN, top)
        c.setFont(F["bold"], 7.5)
        c.setFillColor(colors.HexColor(self.pal.primary_ink))
        c.drawString(MARGIN, top + 7, m["client_name"].upper())
        c.setFillColor(MUTED)
        c.setFont(F["sans"], 7.5)
        c.drawRightString(PAGE_W - MARGIN, top + 7, "SEO Audit · " + m.get("date", ""))
        c.drawString(MARGIN, MARGIN - 0.4 * inch, m.get("agency_name", ""))
        c.drawRightString(PAGE_W - MARGIN, MARGIN - 0.4 * inch, str(doc.page))
        c.restoreState()


# ---------------------------------------------------------------- builders
class Builder:
    def __init__(self, data, pal, F, S):
        self.d, self.pal, self.F, self.S = data, pal, F, S
        self.n = 0

    def section(self, title, intro=None):
        self.n += 1
        out = [Spacer(1, 22), CondPageBreak(2.2 * inch)] if self.n > 1 else []
        out.append(Paragraph(f"{self.n:02d}", self.S["kicker"]))
        h = Paragraph(clean(title), self.S["h1"])
        h._toc_text = title
        out.append(h)
        out.append(Spacer(1, 4))
        if intro:
            out.append(P_(intro, self.S["muted"]))
        out.append(Spacer(1, 8))
        return out

    def h2(self, text):
        # never leave a subheading stranded at the bottom of a page
        return [CondPageBreak(1.4 * inch), Paragraph(clean(text), self.S["h2"])]

    def table(self, header, rows, widths, extra=None, zebra=True):
        S = self.S
        data = [[Paragraph(clean(h), S["cell_head"]) for h in header]]
        for r in rows:
            data.append([c if not isinstance(c, (str, int, float)) and c is not None
                         else Paragraph(clean(c), S["cell"]) for c in r])
        t = Table(data, colWidths=[w * CONTENT_W for w in widths], repeatRows=1)
        st = [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(self.pal.band)),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE),
        ]
        if zebra:
            for i in range(2, len(data), 2):
                st.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
        if extra:
            st.extend(extra)
        t.setStyle(TableStyle(st))
        return t

    # 1. TOC
    def toc(self):
        toc = TableOfContents()
        toc.levelStyles = [self.S["toc0"]]
        toc.dotsMinLevel = 0
        return [Paragraph("Contents", self.S["h1"]), Spacer(1, 14), toc, PageBreak()]

    # 2. Executive summary
    def executive_summary(self):
        es, S, pal = self.d.get("executive_summary", {}), self.S, self.pal
        out = self.section("Executive Summary")
        if es.get("market_context"):
            out.append(P_(es["market_context"], S["lead"]))
        if es.get("verdict"):
            out.append(Spacer(1, 6))
            v = Table([[Paragraph(clean(es["verdict"]), S["verdict"])]], colWidths=[CONTENT_W])
            v.setStyle(TableStyle([
                ("LINEBEFORE", (0, 0), (0, 0), 3, colors.HexColor(pal.primary_ink)),
                ("LEFTPADDING", (0, 0), (-1, -1), 14), ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            out.append(v)
        # stat bar: its own table with fixed row heights, spacers on both sides
        stats = es.get("stats") or self.auto_stats()
        out.append(Spacer(1, 16))
        cells = [[Paragraph(clean(s["value"]), S["stat_num"]) for s in stats],
                 [Paragraph(clean(s["label"]).upper(), S["stat_label"]) for s in stats]]
        bar = Table(cells, colWidths=[CONTENT_W / len(stats)] * len(stats), rowHeights=[38, 26])
        bar_style = [
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(pal.tint)),
            ("VALIGN", (0, 0), (-1, 0), "BOTTOM"), ("VALIGN", (0, 1), (-1, 1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, 0), 10), ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
            ("TOPPADDING", (0, 1), (-1, 1), 2), ("BOTTOMPADDING", (0, 0), (-1, 0), 0),
        ]
        for i in range(1, len(stats)):
            bar_style.append(("LINEBEFORE", (i, 0), (i, -1), 0.8, colors.HexColor(pal.tint_strong)))
        bar.setStyle(TableStyle(bar_style))
        out += [KeepTogether([bar]), Spacer(1, 18)]
        if es.get("key_points"):
            out += self.h2("What we found")
            for p in es["key_points"]:
                out.append(Paragraph("•&nbsp;&nbsp;" + clean(p), ParagraphStyle(
                    "kp", parent=S["body"], leftIndent=12, firstLineIndent=-12)))
        return out

    def auto_stats(self):
        d = self.d
        blockers = len(d.get("blockers", [])) or sum(1 for t in d.get("technical", []) if t.get("blocker"))
        return [
            {"value": str(len(d.get("competitors", []))), "label": "Competitors analyzed"},
            {"value": str(len(d.get("keywords", []))), "label": "Keywords mapped"},
            {"value": str(len(d.get("quick_wins", []))), "label": "Quick wins"},
            {"value": str(blockers), "label": "Hard blockers"},
        ]

    # 3. Business overview
    def business_overview(self):
        bo, S = self.d.get("business_overview", {}), self.S
        if not bo:
            return []
        out = self.section("Business Overview & Site Analysis")
        if bo.get("summary"):
            out.append(P_(bo["summary"], S["lead"]))
        facts = []
        if bo.get("services"):
            facts.append(("Services", ", ".join(bo["services"])))
        if bo.get("areas_served"):
            facts.append(("Areas served", ", ".join(bo["areas_served"])))
        if bo.get("site_status"):
            facts.append(("Current site", bo["site_status"]))
        if facts:
            t = Table([[Paragraph(clean(k).upper(), S["stat_label"]), P_(v, S["body"])] for k, v in facts],
                      colWidths=[1.3 * inch, CONTENT_W - 1.3 * inch])
            t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("ALIGN", (0, 0), (0, -1), "LEFT"),
                                   ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
                                   ("TOPPADDING", (0, 0), (-1, -1), 6),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
            for row in t._cellvalues:
                row[0].style = ParagraphStyle("fl", parent=S["stat_label"], alignment=0)
            out += [Spacer(1, 6), t]
        if bo.get("issues"):
            out += self.h2("Issues found during recon")
            rows, extra = [], []
            for i, iss in enumerate(bo["issues"], start=1):
                sev = (iss.get("severity") or "medium").lower()
                fg, bg = SEVERITY_STYLE.get(sev, SEVERITY_STYLE["medium"])
                b, bgc = badge_cell(sev.upper(), fg, bg, self.F)
                rows.append([b, Paragraph(clean(iss.get("issue")), S["cell_b"]), iss.get("detail", "")])
                extra.append(("BACKGROUND", (0, i), (0, i), bgc))
            out.append(self.table(["Severity", "Issue", "Detail"], rows, [0.13, 0.37, 0.5],
                                  extra=extra, zebra=False))
        return out

    # 4. Competitors
    def competitors(self):
        comps, S = self.d.get("competitors", []), self.S
        if not comps:
            return []
        out = self.section("Competitor Analysis",
                           "Review counts and ratings are as observed on the date of this audit.")
        for c in comps:
            rv = c.get("reviews") or {}
            rev = ""
            if rv.get("count") is not None:
                rev = f"{rv.get('rating', '—')} ★ · {rv['count']} reviews ({rv.get('source', 'Google')})".replace("★", "stars")
            head = Table([[Paragraph(clean(c["name"]), S["card_title"]),
                           Paragraph(clean(rev), ParagraphStyle("r", parent=S["muted"], alignment=2))]],
                         colWidths=[CONTENT_W * 0.6, CONTENT_W * 0.4])
            head.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0),
                                      ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                      ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
            meta = " · ".join(x for x in [c.get("url", "").replace("https://", "").rstrip("/"),
                                          c.get("hq"), c.get("scale")] if x)
            body = [head, P_(meta, S["muted"])]
            if c.get("differentiator"):
                body.append(P_(c["differentiator"], S["body"]))
            sw = Table([[Paragraph("<b>Strengths</b><br/>" + clean(c.get("strengths", "—")), S["cell"]),
                         Paragraph("<b>Weaknesses</b><br/>" + clean(c.get("weaknesses", "—")), S["cell"])]],
                       colWidths=[CONTENT_W / 2] * 2)
            sw.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                    ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#F1F8F4")),
                                    ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#FDF3F2")),
                                    ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                                    ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
            body += [sw, Spacer(1, 14)]
            out.append(KeepTogether(body))
        fm = self.d.get("feature_matrix")
        if fm and fm.get("features") and fm.get("rows"):
            out.append(CondPageBreak(2.5 * inch))
            out += self.h2("Feature comparison")
            feats = fm["features"]
            name_w = 0.26
            fw = (1 - name_w) / len(feats)
            rows, extra = [], []
            for ri, r in enumerate(fm["rows"], start=1):
                cells = [Paragraph(clean(r["name"]), S["cell_b"] if r.get("is_client") else S["cell"])]
                for v in r.get("values", []):
                    key = str(v).strip().lower()
                    label, col = MATRIX_VALUES.get(key, (str(v), "#1B1F24"))
                    cells.append(Paragraph(clean(label), ParagraphStyle(
                        "m", parent=S["cell"], alignment=1, textColor=colors.HexColor(col),
                        fontName=self.F["bold"] if key in MATRIX_VALUES else self.F["sans"])))
                rows.append(cells)
                if r.get("is_client"):
                    extra.append(("BACKGROUND", (0, ri), (-1, ri), colors.HexColor(self.pal.tint)))
            t = self.table(["Business"] + feats, rows, [name_w] + [fw] * len(feats), extra=extra)
            t.setStyle(TableStyle([("ALIGN", (1, 0), (-1, -1), "CENTER")]))
            for cell in t._cellvalues[0][1:]:
                cell.style = ParagraphStyle("ch", parent=S["cell_head"], alignment=1, fontSize=7.6, leading=9.6)
            out.append(t)
        return out

    # 5. Keywords
    def keywords(self):
        kws, S = self.d.get("keywords", []), self.S
        if not kws:
            return []
        out = self.section("Keyword Research",
                           "Difficulty is a relative estimate from the live results page unless a "
                           "source is shown. 'AI' marks terms where a Google AI Overview appeared; "
                           "'?' means it couldn't be checked.")
        diff_col = {"LOW": "#1E7A46", "MEDIUM": "#9A5B00", "HIGH": "#B42318"}
        for tier in (1, 2, 3, 4):
            tk = [k for k in kws if tier_of(k) == tier]
            if not tk:
                continue
            rows = []
            for k in tk:
                kw = clean(k["keyword"])
                if k.get("source"):
                    kw += f"<br/><font color='#5B6470' size='7'>{clean(k['source'])}</font>"
                d = str(k.get("difficulty", "")).upper()
                rows.append([Paragraph(kw, S["cell_b"]), k.get("intent", ""),
                             Paragraph(f"<font color='{diff_col.get(d, '#1B1F24')}'><b>{clean(d)}</b></font>", S["cell"]),
                             k.get("target_page", ""),
                             {True: "AI", False: "", None: "?"}.get(k.get("ai_overview"), "?")])
            heading = Paragraph(clean(TIER_NAMES[tier]), S["h3"])
            table = self.table(["Keyword", "Intent", "Difficulty", "Target page", "AI"], rows,
                               [0.42, 0.14, 0.12, 0.26, 0.06])
            # short tiers stay with their heading; long ones may split (header row repeats)
            out += [KeepTogether([heading, table])] if len(rows) <= 8 else [CondPageBreak(1.5 * inch), heading, table]
            out.append(Spacer(1, 4))
        return out

    # 6. Technical
    def technical(self):
        tech, S, F = self.d.get("technical", []), self.S, self.F
        if not tech:
            return []
        counts = {k: sum(1 for t in tech if str(t.get("rating", "")).upper() == k) for k in RATING_STYLE}
        summary = " · ".join(f"{v} {k}" for k, v in counts.items() if v)
        out = self.section("Technical SEO Audit", summary + ". Basis shows whether a rating was "
                           "measured with a tool, observed directly, or estimated.")
        cats = []
        for t in tech:
            if t.get("category") not in cats:
                cats.append(t.get("category"))
        for cat in cats:
            rows, extra = [], []
            items = [t for t in tech if t.get("category") == cat]
            for i, t in enumerate(items, start=1):
                rating = str(t.get("rating", "N/A")).upper()
                fg, bg = RATING_STYLE.get(rating, RATING_STYLE["N/A"])
                b, bgc = badge_cell(rating, fg, bg, F)
                check = clean(t.get("check"))
                if t.get("blocker"):
                    check += "<br/><font color='#B42318' size='7'><b>HARD BLOCKER</b></font>"
                rows.append([Paragraph(check, S["cell_b"]), b, t.get("finding", ""),
                             Paragraph(f"<font color='#5B6470'>{clean(t.get('basis', ''))}</font>", S["cell"])])
                extra.append(("BACKGROUND", (1, i), (1, i), bgc))
            out.append(KeepTogether([Paragraph(clean(cat), S["h3"]),
                                     self.table(["Check", "Rating", "Finding", "Basis"], rows,
                                                [0.28, 0.1, 0.48, 0.14], extra=extra, zebra=False)]))
        cwv = self.d.get("core_web_vitals")
        if cwv:
            def grade(v, good, poor):
                if v is None:
                    return "—", "#5B6470"
                return (v, "#1E7A46") if v <= good else ((v, "#9A5B00") if v <= poor else (v, "#B42318"))
            rows = []
            for r in cwv:
                cells = [f"{r.get('url', '')} ({r.get('strategy', 'mobile')})"]
                for key, good, poor, unit in (("lcp_s", 2.5, 4.0, "s"), ("cls", 0.1, 0.25, ""),
                                              ("inp_ms", 200, 500, " ms"), ("tbt_ms", 200, 600, " ms")):
                    v, col = grade(r.get(key), good, poor)
                    txt = f"{v}{unit}" if v != "—" else v
                    cells.append(Paragraph(f"<font color='{col}'><b>{clean(txt)}</b></font>", S["cell"]))
                src = r.get("source", "")
                cells.append("Real users (CrUX)" if src == "field" else ("Lab (Lighthouse)" if src == "lab" else src))
                rows.append(cells)
            out.append(KeepTogether([Paragraph("Core Web Vitals", S["h3"]),
                                     self.table(["Page", "LCP", "CLS", "INP", "TBT", "Data"], rows,
                                                [0.3, 0.11, 0.11, 0.11, 0.11, 0.26])]))
            out.append(P_("Thresholds: LCP ≤ 2.5s, CLS ≤ 0.1, INP ≤ 200 ms. Lab tests can't measure "
                          "INP; Total Blocking Time is the lab proxy.", S["muted"]))
        return out

    # 7. AI visibility
    def ai_visibility(self):
        ai, S = self.d.get("ai_visibility"), self.S
        if not ai:
            return []
        out = self.section("AI Search Visibility",
                           "AI answers vary by person, place and day. This is a snapshot of what "
                           "we saw, not a ranking.")
        if ai.get("summary"):
            out.append(P_(ai["summary"], S["lead"]))
        if ai.get("crawlers"):
            col = {"allowed": "#1E7A46", "blocked": "#B42318", "partial": "#9A5B00"}
            rows = [[Paragraph(clean(c["agent"]), S["cell_b"]),
                     Paragraph(f"<font color='{col.get(str(c.get('status')).lower(), '#1B1F24')}'><b>"
                               f"{clean(str(c.get('status', '')).capitalize())}</b></font>", S["cell"]),
                     c.get("note", "")] for c in ai["crawlers"]]
            out += [Paragraph("Crawler access", S["h3"]),
                    self.table(["Crawler", "Status", "Note"], rows, [0.3, 0.15, 0.55])]
        if ai.get("citations"):
            rows = [[Paragraph(clean(c["query"]), S["cell_b"]), c.get("surface", ""),
                     Paragraph(("<font color='#1E7A46'><b>Yes</b></font>" if c.get("client_cited")
                                else "<font color='#B42318'><b>No</b></font>"), S["cell"]),
                     c.get("cited", "")] for c in ai["citations"]]
            out += [Paragraph("Who AI answers cite", S["h3"]),
                    self.table(["Query", "Surface", "Client cited", "Cited instead"], rows,
                               [0.32, 0.18, 0.12, 0.38])]
        return out

    # 8. Content strategy
    def content_strategy(self):
        cs, S = self.d.get("content_strategy", {}), self.S
        if not cs:
            return []
        out = self.section("Content Strategy")
        if cs.get("page_roadmap"):
            st_col = {"missing": "#B42318", "weak": "#9A5B00", "exists": "#1E7A46"}
            rows = [[Paragraph(clean(p["page"]), S["cell_b"]), p.get("url", ""), p.get("type", ""),
                     Paragraph(f"<font color='{st_col.get(str(p.get('status')).lower(), '#1B1F24')}'><b>"
                               f"{clean(str(p.get('status', '')).capitalize())}</b></font>", S["cell"]),
                     p.get("priority", "")] for p in cs["page_roadmap"]]
            out += [*self.h2("Page roadmap"),
                    self.table(["Page", "URL", "Type", "Status", "Priority"], rows,
                               [0.24, 0.32, 0.14, 0.15, 0.15])]
        if cs.get("blog_posts"):
            rows = [[str(i), Paragraph(clean(b["title"]), S["cell_b"]), b.get("keyword", ""),
                     f"Tier {b['tier']}" if b.get("tier") else "", b.get("purpose", "")]
                    for i, b in enumerate(cs["blog_posts"], start=1)]
            out += [*self.h2("Priority blog posts"),
                    self.table(["#", "Title", "Target keyword", "Tier", "Purpose"], rows,
                               [0.05, 0.43, 0.27, 0.1, 0.15])]
        return out

    # 9. Blockers + quick wins
    def quick_wins(self):
        S, F = self.S, self.F
        blockers, wins = self.d.get("blockers", []), self.d.get("quick_wins", [])
        if not blockers and not wins:
            return []
        out = self.section("Blockers & Quick Wins",
                           "Blockers come first: fix these before anything else. Quick wins are "
                           "ranked by impact relative to effort.")
        if blockers:
            red, red_bg = "#B42318", "#FEECEB"
            items = []
            for b in blockers:
                txt = f"<b>{clean(b['title'])}</b><br/>{clean(b.get('detail', ''))}"
                if b.get("fix"):
                    txt += f"<br/><font color='{red}'><b>Fix:</b></font> {clean(b['fix'])}"
                items.append([Paragraph(txt, S["cell"])])
            t = Table([[Paragraph("<b>HARD BLOCKERS</b>", ParagraphStyle(
                "bh", parent=S["cell"], textColor=colors.HexColor(red)))]] + items, colWidths=[CONTENT_W])
            t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(red_bg)),
                                   ("LINEBEFORE", (0, 0), (0, -1), 3, colors.HexColor(red)),
                                   ("LEFTPADDING", (0, 0), (-1, -1), 12),
                                   ("TOPPADDING", (0, 0), (-1, -1), 6),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                                   ("LINEBELOW", (0, 1), (-1, -2), 0.4, colors.HexColor("#F5C2BD"))]))
            out += [t, Spacer(1, 14)]
        if wins:
            rows = [[Paragraph(f"<b>{i}</b>", S["cell"]),
                     Paragraph(f"<b>{clean(w['title'])}</b><br/>{clean(w.get('detail', ''))}", S["cell"]),
                     w.get("impact", ""), fmt_hours(w.get("effort_hours"))]
                    for i, w in enumerate(wins, start=1)]
            out += [*self.h2("Quick wins"),
                    self.table(["#", "Action", "Impact", "Effort"], rows, [0.06, 0.66, 0.13, 0.15])]
        return out

    # 10. Opportunities
    def opportunities(self):
        ops, S = self.d.get("opportunities", []), self.S
        if not ops:
            return []
        out = self.section("Strategic Opportunities")
        for i, o in enumerate(ops, start=1):
            num = Paragraph(f"{i}", ParagraphStyle("on", parent=S["stat_num"], fontSize=34, leading=36))
            body = [Paragraph(clean(o["title"]), S["card_title"])]
            for label, key in (("The gap", "gap"), ("Why it matters", "why"), ("What to build", "action")):
                if o.get(key):
                    body.append(Paragraph(f"<b>{label}.</b> {clean(o[key])}", S["body"]))
            t = Table([[num, body]], colWidths=[0.6 * inch, CONTENT_W - 0.6 * inch])
            t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("LEFTPADDING", (0, 0), (0, 0), 0),
                                   ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.HexColor(self.pal.primary_ink)),
                                   ("TOPPADDING", (0, 0), (-1, -1), 10)]))
            out += [KeepTogether([t]), Spacer(1, 10)]
        return out

    # 11. Closing
    def closing(self):
        c, m, S, pal = self.d.get("closing", {}), self.d["meta"], self.S, self.pal
        out = self.section("Next Steps")
        if c.get("headline"):
            out.append(Paragraph(clean(c["headline"]), S["verdict"]))
        if c.get("body"):
            out.append(P_(c["body"], S["lead"]))
        lines = [f"<b>{clean(m['agency_name'])}</b>"] if m.get("agency_name") else []
        for k in ("cta", "contact"):
            if c.get(k):
                lines.append(clean(c[k]))
        if m.get("agency_url"):
            lines.append(clean(m["agency_url"].replace("https://", "")))
        if not lines:
            return out
        box = Table([[Paragraph("<br/>".join(lines), ParagraphStyle(
            "cb", parent=S["body"], textColor=colors.HexColor(pal.on_band), fontSize=10.5, leading=16))]],
            colWidths=[CONTENT_W])
        box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(pal.band)),
                                 ("LEFTPADDING", (0, 0), (-1, -1), 18), ("TOPPADDING", (0, 0), (-1, -1), 16),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 16)]))
        out += [Spacer(1, 14), box]
        return out


# ---------------------------------------------------------------- validation & main
REQUIRED = ["meta.client_name", "meta.date", "executive_summary.verdict"]
RECOMMENDED = ["competitors", "keywords", "technical", "quick_wins", "opportunities"]


def validate(data):
    errors, warnings = [], []
    for path in REQUIRED:
        cur = data
        for part in path.split("."):
            cur = cur.get(part) if isinstance(cur, dict) else None
        if not cur:
            errors.append(f"missing required field: {path}")
    if not (data.get("meta") or {}).get("agency_name"):
        warnings.append("meta.agency_name is empty: the cover and closing will omit 'Prepared by'")
    for key in RECOMMENDED:
        if not data.get(key):
            warnings.append(f"section '{key}' is empty and will be skipped")
    for i, t in enumerate(data.get("technical", [])):
        r = str(t.get("rating", "")).upper()
        if r not in RATING_STYLE:
            warnings.append(f"technical[{i}] rating '{t.get('rating')}' should be PASS/WARN/FAIL/N/A")
        if t.get("basis") and str(t["basis"]).split(" ")[0] not in ("measured", "observed", "estimated"):
            warnings.append(f"technical[{i}] basis should start with measured/observed/estimated")
    for i, k in enumerate(data.get("keywords", [])):
        if tier_of(k) not in (1, 2, 3, 4):
            warnings.append(f"keywords[{i}] tier must be 1-4")
    if len(data.get("opportunities", [])) not in (0, 3):
        warnings.append("the methodology calls for exactly 3 strategic opportunities")
    fm = data.get("feature_matrix") or {}
    for r in fm.get("rows", []):
        if len(r.get("values", [])) != len(fm.get("features", [])):
            errors.append(f"feature_matrix row '{r.get('name')}' has {len(r.get('values', []))} "
                          f"values for {len(fm.get('features', []))} features")
    return errors, warnings


def build(data, out_path):
    pal = Palette(data.get("brand", {}))
    F = register_fonts()
    S = make_styles(F, pal)
    doc = AuditDoc(str(out_path), data, pal, F)
    b = Builder(data, pal, F, S)
    story = [NextPageTemplate("body"), PageBreak()]          # page 1 = cover (canvas-drawn)
    story += b.toc()
    for part in (b.executive_summary, b.business_overview, b.competitors, b.keywords,
                 b.technical, b.ai_visibility, b.content_strategy, b.quick_wins,
                 b.opportunities, b.closing):
        story += part()
    doc.multiBuild(story)
    return doc.page


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("findings", help="path to findings JSON")
    ap.add_argument("-o", "--output", help="output PDF path (default: <Client>_SEO_Audit.pdf next to the JSON)")
    args = ap.parse_args()
    try:
        data = json.loads(Path(args.findings).read_text())
    except OSError as e:
        sys.exit(f"error: can't read {args.findings}: {e.strerror or e}")
    except json.JSONDecodeError as e:
        sys.exit(f"error: {args.findings} is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}")
    if not isinstance(data, dict):
        sys.exit(f"error: {args.findings} must contain a JSON object at the top level, "
                 f"not {type(data).__name__}")
    errors, warnings = validate(data)
    for w in warnings:
        print("warning:", w, file=sys.stderr)
    if errors:
        for e in errors:
            print("error:", e, file=sys.stderr)
        sys.exit(1)
    slug = re.sub(r"[^A-Za-z0-9]+", "_", data["meta"]["client_name"]).strip("_")
    out = Path(args.output) if args.output else Path(args.findings).with_name(f"{slug}_SEO_Audit.pdf")
    pages = build(data, out)
    print(f"wrote {out} ({pages} pages)")


if __name__ == "__main__":
    main()
