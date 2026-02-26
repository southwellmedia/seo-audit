# seo-audit

> A Claude skill for running systematic SEO audits and competitive analyses for local service businesses — built by [Southwell Media](https://southwellmedia.com).

This skill gives Claude a repeatable methodology for auditing client websites and producing client-ready PDF proposals.

---

## What it produces

One deliverable per audit:

- **`[Client]_SEO_Audit.pdf`** — Full proposal with competitive analysis, keyword research, technical audit, content strategy, and prioritized quick wins

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
    └── deliverables.md             # PDF specs + code patterns
```

---

## Requirements

- Claude with computer use enabled (for browser recon and brand color extraction)
- Python 3 with `reportlab` and `pillow` (`pip install reportlab pillow`)
- Canvas fonts from the [canvas-design skill](https://github.com/southwellmedia/canvas-design) at `/mnt/skills/examples/canvas-design/canvas-fonts/`

---

## Business model branching

The skill automatically branches based on client type:

| Model | When | Examples |
|-------|------|---------|
| B2C Local | Single market, consumer-facing, on-demand | Junk removal, HVAC, roofing, pool service |
| B2B Multi-State | Multi-region, sells to businesses, contract-based | Valet trash, commercial cleaning, facilities management |

Classification happens before any research — getting this wrong invalidates the competitive analysis.

---

## Key methodology notes

**Hard blockers vs. quick wins** — The skill separates issues that prevent launch (placeholder phone numbers, dead CTAs, unblocked staging domains) from optimization opportunities. These are visually distinct in the deliverable.

**Brand color extraction** — Brand colors are pulled directly from the live site's CSS using browser JS, not guessed. The PDF always matches the client's actual palette.

**Strategic opportunities are specific** — The 3 opportunities section is grounded in actual competitive gaps found during research, not generic SEO advice. "Create great content" is never an output.

**The audit is the pitch** — Southwell Media uses these as client proposals. The closing section positions Southwell to execute the implementation, not just deliver the report.

---

## License

MIT — use freely, attribution appreciated.

Built and maintained by [Southwell Media](https://southwellmedia.com) — a Dallas-based digital agency delivering custom websites in 14-21 days for local service businesses.
