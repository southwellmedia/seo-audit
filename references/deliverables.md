# Deliverables Reference

One deliverable per audit: a full PDF proposal.
Generated programmatically with Python ReportLab. Do NOT use pandoc, wkhtmltopdf, or any other conversion tool.

**Install before generating:**
```bash
pip install reportlab --break-system-packages -q
```

---

## PDF Audit Report

**Output**: `/mnt/user-data/outputs/[ClientName]_SEO_Audit.pdf`

Extract brand colors from the live site before writing any code (see SKILL.md Step 1b).
Use those colors throughout the document as accents. If extraction fails, choose a professional
color palette that fits the client's industry.

The PDF must use a **light background** — white or near-white pages. No dark mode. Brand colors
are used as accents (headers, rules, badges, callout bars), not as page backgrounds.

The PDF should look polished enough to send to a client cold — a professional agency proposal,
not a script output. You have full creative latitude on layout, typography, spacing, cover design,
and visual hierarchy. Make it look good. Use your judgment.

**The stat callout bar in the executive summary must be a self-contained block** — it cannot
overlap or collide with any surrounding text. Build it as its own Table flowable with explicit
row heights, placed after the verdict paragraph with a Spacer above and below it.

Fonts are available at `/mnt/skills/examples/canvas-design/canvas-fonts/` — register any of them
with ReportLab if they improve the result.

---

## Required sections (in order)

1. **Cover page** — client name, "SEO Audit & Competitive Analysis", date, "Prepared by [agency_name]"
2. **Table of contents**
3. **Executive summary** — market context, one-sentence verdict, 4-stat callout bar (competitors, keywords, quick wins, blockers)
4. **Business overview & site analysis** — what they do, current site status, issue table
5. **Competitor analysis** — 6-8 competitor profiles + feature comparison matrix
6. **Keyword research** — 4 tiers, table per tier
7. **Technical SEO audit** — PASS / WARN / FAIL per category, hard blockers visually distinct
8. **Content strategy** — page roadmap + top 10 blog posts
9. **Quick wins** — ranked by impact ÷ effort, time estimates, blockers called out
10. **Strategic opportunities** — 3 specific opportunities, not generic advice
11. **Closing** — [agency_name] executes the work; the audit is the pitch

---

## Output

```python
import shutil
slug = client_name.replace(" ", "_")
shutil.copy('/home/claude/audit.pdf', f'/mnt/user-data/outputs/{slug}_SEO_Audit.pdf')
```

Call `present_files` with the PDF. Keep the closing message to 2-3 sentences.
