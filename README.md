# seo-audit

> A Claude skill for running systematic SEO audits and competitive analyses for service businesses — built by [Southwell Media](https://southwellmedia.com).

This skill gives Claude a repeatable methodology for auditing a client website and producing a client-ready PDF proposal your agency can send cold.

---

## What it produces

- **`[Client]_SEO_Audit.pdf`** — the proposal: competitive analysis, keyword research, technical and AI-visibility audit, content strategy, blockers, quick wins and three strategic opportunities. Light pages with the client's brand colors as accents.
- **`findings.json`** — every finding in structured form. Re-render the PDF after edits, compare against a re-audit in six months, or turn it into a deck or doc.

## What it covers

- Live site recon, including brand-color extraction from the live CSS
- Business model classification: B2C local, multi-location B2C, or B2B
- 6–8 competitors with a feature comparison matrix
- 40–50 keywords across 4 intent tiers, with AI Overview flags
- Technical audit across 13 categories — PASS / WARN / FAIL, each marked measured, observed, or estimated
- Core Web Vitals from the PageSpeed Insights API (real-user data when available)
- **AI search visibility** — AI crawler access, who ChatGPT / Perplexity / AI Overviews cite for the client's key queries, and entity consistency across directories
- Hard blockers separated from quick wins, with effort estimates
- Page roadmap and top 10 blog posts
- 3 strategic opportunities grounded in actual competitive gaps

---

## Usage

```
Run an SEO audit for https://example.com
```

Claude opens the site, infers the business, market and model, confirms them with you in one round of questions, then runs the full workflow.

---

## Skill structure

```
seo-audit/
├── SKILL.md                          # Workflow and decision logic
├── references/
│   ├── b2c-local.md                  # Consumer, single-market
│   ├── multi-location.md             # Consumer, several physical locations
│   ├── b2b.md                        # Business buyers, single- or multi-market
│   ├── keywords.md                   # 4-tier keyword framework
│   ├── technical-checklist.md        # 13-section technical + AI-visibility checklist
│   └── deliverables.md               # findings.json format, render and check steps
├── scripts/
│   ├── extract_brand_colors.js       # Run in the page to pull brand colors
│   ├── build_report.py               # findings.json → PDF
│   └── check_pdf.py                  # Renders pages, flags layout and data problems
└── assets/
    ├── findings.example.json         # Complete example (fictional client)
    └── fonts/                        # Instrument Sans & Serif (SIL OFL)
```

---

## Requirements

- A browser tool that can evaluate JavaScript (for recon and brand colors). Without one, Claude falls back to fetching pages and notes what it couldn't check.
- Python 3 with `reportlab`, `pypdfium2` and `pillow`:
  ```bash
  pip install reportlab pypdfium2 pillow
  ```
- Fonts are bundled — no other skill needed.

Try the renderer on the example:

```bash
python3 scripts/build_report.py assets/findings.example.json -o example.pdf
python3 scripts/check_pdf.py example.pdf
```

---

## Installation

Zip the folder and upload it through Claude's skill settings:

```bash
zip -r seo-audit.zip seo-audit/ -x "seo-audit/.git/*"
```

For Claude Code, place the folder in `~/.claude/skills/` (or a project's `.claude/skills/`).

---

## Business model branching

| Model | When | Examples |
|-------|------|----------|
| B2C Local | Consumers, one metro, one location or service-area business | Trades, home services, independent professionals |
| Multi-location B2C | Consumers, several physical locations | Dental/medical groups, gyms, salons, auto service chains |
| B2B | Sells to businesses on contract, one market or many | Commercial cleaning, facilities, managed IT, B2B professional services |

Classification happens before research — getting it wrong invalidates the competitive analysis.

---

## Key methodology notes

**Blockers vs. quick wins** — issues that should stop a launch (placeholder phone numbers, dead CTAs, indexable staging, blocked AI search bots) are separated from optimizations and shown first.

**Measured vs. estimated** — every rating says how it was determined, so a client can tell a PageSpeed measurement from a judgment call. No invented search volumes.

**Current guidance only** — no pitching FAQ rich results (removed May 2026), HowTo rich results (removed 2023), or star ratings for a business's own testimonials (not shown since 2019).

**Specific opportunities** — the three strategic opportunities come from gaps actually found in the competitive set. "Create great content" is never an output.

**The audit is the pitch** — the closing positions your agency to do the work. Your agency name comes from what Claude knows about you, or it asks.

---

## License

MIT — use freely, attribution appreciated. Bundled fonts are under the SIL Open Font License (see `assets/fonts/`).

Built and maintained by [Southwell Media](https://southwellmedia.com) — a Dallas-based digital agency.
