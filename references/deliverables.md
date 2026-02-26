# Deliverables Reference

Two deliverables for every audit: a full PDF proposal and an infographic highlights PNG.
Both are generated programmatically — do not use pandoc or wkhtmltopdf.

---

## PDF Audit Report

**Tool**: ReportLab (`pip install reportlab --break-system-packages`)
**Output**: `[ClientName]_SEO_Audit.pdf` → `/mnt/user-data/outputs/`
**Page size**: Letter (8.5" × 11") — 612 × 792 points

### Color palette (apply client brand colors)
Extract from live site first (see SKILL.md Step 1b).
Fall back to neutral dark palette if brand colors aren't recoverable.

```python
# Example palette structure
BRAND_PRIMARY   = "#e14e8a"   # client's primary brand color
BRAND_SECONDARY = "#4e375e"   # client's secondary brand color
BRAND_ACCENT    = "#9ada5e"   # client's accent color
BLACK     = "#0d0d0d"
WHITE     = "#ffffff"
GRAY_DARK = "#2a2a2a"
GRAY_MID  = "#636e72"
GRAY_LIGHT= "#f4f4f4"
RED_FAIL  = "#c0392b"
GREEN_PASS= "#27ae60"
AMBER_WARN= "#e67e22"
```

### PDF sections (in order)

#### 1. Cover page
- Full-bleed brand color background (or dark if brand is light)
- Client name in large BigShoulders or similar display font
- "SEO AUDIT & COMPETITIVE ANALYSIS" subtitle
- "Prepared by Southwell Media" in small mono font
- Month + Year
- Diagonal accent shapes using secondary brand color

#### 2. Table of contents
- Light background
- Section numbers + page titles
- Accent rule line in brand primary color

#### 3. Executive summary
- Opening paragraph: market context + one-sentence verdict
- Stat callout bar (4 stats): key numbers from the audit
  - Direct competitors analyzed
  - Target keywords identified
  - Quick wins available
  - Critical blockers (if any)
- 2-3 paragraph narrative covering the opportunity

#### 4. Business overview & site analysis
- What the business does (2-3 paragraphs)
- Geographic scope and service model
- Current site status — what's live, what's missing
- Structured issue table: Category | Issue | Severity (color-coded)

#### 5. Competitor analysis
- 6-8 competitor profiles, each with:
  - Name, type (National/Local), headline differentiator
  - Strengths (2-3 bullet points)
  - Weaknesses (2-3 bullet points)
- Feature comparison matrix table
  - Rows: key SEO features
  - Columns: competitors + client
  - ✓ / ✗ / — for each cell

#### 6. Keyword research
- 4 sections (one per tier) with colored headers
- Table per tier: Keyword | Intent | Difficulty | Target Page
- Brief narrative per tier explaining the opportunity

#### 7. Technical SEO audit
- 6-9 category sections
- Each item: status badge (FAIL/WARN/PASS) + category + finding
- Two-column layout where possible for density
- Color-coded: red background for FAIL sections, green for PASS, amber for WARN

#### 8. Content strategy
- Page structure roadmap (what exists vs. what needs to be built)
- Top 10 blog posts with title, target keyword, and why it matters

#### 9. Quick wins
- Numbered list 1-10
- Each item: time estimate badge + action + brief rationale
- Hard blockers highlighted in red with "BLOCKER" label
- Non-blockers in priority order

#### 10. Strategic opportunities
- 3 opportunities, each on its own visual block
- Opportunity number (01/02/03), title, 2-3 paragraph explanation
- Focus on what's specific to this client and market — not generic

#### 11. Closing / Southwell positioning
- Brief paragraph: Southwell can execute the technical implementation
- Contact info
- Do NOT say "good luck" — the audit is the pitch

---

## ReportLab implementation notes

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
```

### Font recommendation
Use built-in Helvetica for body, Helvetica-Bold for headings.
Or register custom TTF fonts if BigShoulders/IBMPlexMono are available.

### Avoid ReportLab XML pitfalls
Never use HTML link tags with `rel=` attributes in Paragraph() text.
ReportLab's XML parser doesn't support all HTML attributes.
Strip any `<a rel="...">` or use plain text for URLs.

### Color conversion
ReportLab uses `colors.HexColor("#xxxxxx")` — always pass hex strings.
Never pass RGB tuples directly to HexColor.

### Table styling pattern
```python
TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor(BRAND_PRIMARY)),  # header row
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor(GRAY_LIGHT), colors.white]),
    ('FONTSIZE', (0,1), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor(GRAY_MID)),
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor(GRAY_MID)),
])
```

---

## Infographic Highlights PNG

**Tool**: Pillow (`pip install pillow --break-system-packages`)
**Output**: `[ClientName]_SEO_Infographic.png` → `/mnt/user-data/outputs/`
**Canvas**: 1400 × 3200 px (tall infographic format, 72dpi equivalent)
**Font directory**: `/mnt/skills/examples/canvas-design/canvas-fonts/`

### Design philosophy: HAUL MANIFEST / DEMOLITION DISPATCH
Industrial reckoning aesthetic. Black fields, brand color accents, monospaced data.
Every element earns its place. No decoration.

### Color usage
- Background: `#0d0d0d` (near-black)
- Brand primary: header background, section accents, key data points
- Brand secondary: competitor cards, opportunity numbers
- Brand accent: stat numbers, section titles, positive indicators
- RED `#c0392b`: hard blockers, FAIL status
- GREEN `#2d6a4f`: PASS status
- AMBER: WARN status (use brand accent if it reads as warning-adjacent)
- GRAY `#6e6e6e`: secondary text, borders

### Font stack
```python
FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"

# Primary display font
font("BigShoulders-Bold.ttf", 130)   # Hero titles (BIG JUNK)
font("BigShoulders-Bold.ttf", 72)    # Section numbers
font("BigShoulders-Bold.ttf", 48)    # Section headers

# Data / mono font  
font("IBMPlexMono-Bold.ttf", 36)     # Large data
font("IBMPlexMono-Bold.ttf", 22)     # Table headers
font("IBMPlexMono-Regular.ttf", 18)  # Table data
font("IBMPlexMono-Regular.ttf", 14)  # Small labels

# Body / UI font
font("WorkSans-Bold.ttf", 28)        # Card titles
font("WorkSans-Regular.ttf", 22)     # Card body
font("WorkSans-Regular.ttf", 18)     # List items
font("WorkSans-Regular.ttf", 15)     # Fine print

# Accent
font("GeistMono-Bold.ttf", 20)       # Badge labels
font("GeistMono-Regular.ttf", 16)    # Small mono
font("Outfit-Bold.ttf", 26)          # Competitor names
```

### Section order (top to bottom)
1. **Header block** (260px) — Brand color background, "BIG JUNK / SEO AUDIT / HIGHLIGHTS", diagonal accent shapes, "Prepared by Southwell Media" badge
2. **Stat bar** (160px) — Dark background, 4 key numbers (competitors, keywords, quick wins, blockers)
3. **Critical blockers** (if any) — Red section header, 5-item table with red left border
4. **Technical SEO audit** — BigShoulders header, 2-column grid of FAIL/WARN/PASS items
5. **Competitor landscape** — Centered mono label, 2-column competitor cards with tinted left borders
6. **Keyword targets** — Purple/brand section header, 4-column keyword table (one per tier)
7. **3 strategic opportunities** — Brand color banner, 3-column layout with large numbers
8. **Top 10 pre-launch actions** — BigShoulders header, numbered list with time badges
9. **Footer** (110px) — "SOUTHWELL MEDIA" in brand accent, tagline, URL, confidential note

### Helper functions to always include
```python
def rect(x, y, w, h, fill, radius=0):
    if radius == 0:
        draw.rectangle([x, y, x+w, y+h], fill=fill)
    else:
        draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill)

def hrule(y, x1=MARGIN, x2=W-MARGIN, color=GRAY2, thick=1):
    draw.rectangle([x1, y, x2, y+thick], fill=color)

def text_c(txt, y, font_, color, x=W//2):
    bb = draw.textbbox((0,0), txt, font=font_)
    tw = bb[2] - bb[0]
    draw.text((x - tw//2, y), txt, font=font_, fill=color)

def text_l(txt, x, y, font_, color):
    draw.text((x, y), txt, font=font_, fill=color)

def text_r(txt, x, y, font_, color):
    bb = draw.textbbox((0,0), txt, font=font_)
    tw = bb[2] - bb[0]
    draw.text((x - tw, y), txt, font=font_, fill=color)
```

---

## Naming and output

```python
# Always save to outputs directory
import shutil
shutil.copy('/home/claude/output.pdf', '/mnt/user-data/outputs/ClientName_SEO_Audit.pdf')
shutil.copy('/home/claude/output.png', '/mnt/user-data/outputs/ClientName_SEO_Infographic.png')
```

After generating both files, call `present_files` with the PNG first (visual impact),
then the PDF. Keep the closing message brief — let the files speak.
