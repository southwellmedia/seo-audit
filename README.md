# seo-audit

> A Claude skill for running systematic SEO audits and competitive analyses for local service businesses — built by [Southwell Media](https://southwellmedia.com).

This skill gives Claude a repeatable methodology for auditing client websites and producing a client-ready PDF proposal.

---

## What it produces

One deliverable per audit:

- **`[Client]_SEO_Audit.pdf`** — Full proposal with competitive analysis, keyword research, technical audit, content strategy, and prioritized quick wins. Light background, client brand colors applied as accents throughout.

## What it covers

- Live site recon (browser automation + CSS brand color extraction)
- Business model classification (B2C single-market vs. B2B multi-state)
- Competitive landscape — 6-8 competitors with feature comparison matrix
- Keyword research — 40-50 keywords across 4 intent tiers
- Technical SEO audit — FAIL / WARN / PASS across 9 categories
- Hard blocker identification (site should not launch until resolved)
- Content strategy — page roadmap + top 10 blog posts
- 3 strategic opportunities specific to the client and market
- Quick wins ranked by impact ÷ effort with time estimates

---

## Usage

In a Claude conversation with this skill installed:

```
Run an SEO audit for [client name] at [URL]
```

Claude will ask for any missing context (industry, geographic scope, business model) then proceed through the full workflow.

---

## Skill structure

```
seo-audit/
├── SKILL.md                        # Core workflow and decision logic
└── references/
    ├── b2c-local.md                # B2C single-market methodology
    ├── b2b-multistate.md           # B2B multi-state methodology
    ├── technical-checklist.md      # Full technical SEO checklist
    ├── keywords.md                 # 4-tier keyword framework
    └── deliverables.md             # PDF requirements and design guidance
```

---

## Requirements

- Claude with computer use enabled (for browser recon and brand color extraction)
- Python 3 with `reportlab` (`pip install reportlab`)
- Canvas fonts from the [canvas-design skill](https://github.com/southwellmedia/canvas-design) at `/mnt/skills/examples/canvas-design/canvas-fonts/`

---

## Installation

Upload `seo-audit.skill` through the Claude skill manager. To build the `.skill` file from source:

```bash
zip -r seo-audit.skill seo-audit/
```

---

## Business model branching

The skill automatically branches based on client type:

| Model | When | Examples |
|-------|------|---------|
| B2C Local | Single market, consumer-facing, on-demand | Trades, home services, professional services |
| B2B Multi-State | Multi-region, sells to businesses, contract-based | Commercial services, facilities management, property amenities |

Classification happens before any research — getting this wrong invalidates the competitive analysis.

---

## Key methodology notes

**Hard blockers vs. quick wins** — The skill separates issues that prevent launch (placeholder phone numbers, dead CTAs, unblocked staging domains) from optimization opportunities. These are visually distinct in the PDF.

**Brand color extraction** — Brand colors are pulled directly from the live site's CSS using browser JS, not guessed. The PDF always matches the client's actual palette.

**Strategic opportunities are specific** — The 3 opportunities section is grounded in actual competitive gaps found during research, not generic SEO advice. "Create great content" is never an output.

**The audit is the pitch** — the closing section positions your agency to execute the implementation, not just deliver the report. The PDF uses your agency name on the cover and closing, pulled from your Claude memory or asked during intake.

---

## License

MIT — use freely, attribution appreciated.

Built and maintained by [Southwell Media](https://southwellmedia.com) — a Dallas-based digital agency.
