# Deliverables Reference

One deliverable per audit: a PDF proposal, built in two steps.

1. **Write `findings.json`** — every finding from the audit, structured. This is the real work
   product: it can be re-rendered, compared against a later re-audit, or turned into a deck or doc.
2. **Render it** with the bundled script, then check the result.

```bash
pip install reportlab pypdfium2 pillow        # add --break-system-packages if pip refuses
python3 <skill-dir>/scripts/build_report.py findings.json -o <ClientName>_SEO_Audit.pdf
python3 <skill-dir>/scripts/check_pdf.py <ClientName>_SEO_Audit.pdf
```

`<skill-dir>` is the folder this skill was loaded from (the one containing `SKILL.md`).
Write `findings.json` and the PDF in the current working directory unless the user asked
for another location.

Don't hand-build the PDF layout in a new script each run. If the layout needs to change,
change `build_report.py` so every future audit gets the improvement.

---

## findings.json

`assets/findings.example.json` is a complete, realistic example — copy its shape.
Every section except `meta` and `executive_summary.verdict` is optional; empty sections are
skipped (the script warns). Keep text tight: these are table cells and callouts, not essays.

| Key | Contents |
|-----|----------|
| `meta` | `client_name`, `url`, `date`, `agency_name`, `agency_url`, `business_model`, `market`, `launch_status` |
| `brand` | `primary`, `secondary`, `accent` as hex, plus `source` ("extracted from live CSS" or "chosen — extraction failed") |
| `executive_summary` | `market_context` (2–3 sentences), `verdict` (one sentence), `key_points` (3–5), optional `stats` (else auto: competitors, keywords, quick wins, blockers) |
| `business_overview` | `summary`, `services[]`, `areas_served[]`, `site_status`, `issues[]` (`issue`, `severity`: blocker/high/medium/low, `detail`) |
| `competitors[]` | `name`, `url`, `hq`, `scale`, `differentiator`, `strengths`, `weaknesses`, `reviews` {`count`, `rating`, `source`} |
| `feature_matrix` | `features[]` (short labels, ≤ 2 words — columns are narrow), `rows[]` {`name`, `is_client`, `values[]`: yes/no/partial or short text} |
| `keywords[]` | `keyword`, `tier` 1–4, `intent`, `difficulty` LOW/MEDIUM/HIGH, `target_page`, `ai_overview` bool, optional `source` (e.g. "Search Console: 410 impressions, avg. position 14") |
| `technical[]` | `category`, `check`, `rating` PASS/WARN/FAIL/N/A, `finding`, `basis` measured/observed/estimated, optional `blocker` true |
| `core_web_vitals[]` | `url`, `strategy`, `source` field/lab, `lcp_s`, `cls`, `inp_ms`, `tbt_ms` (null when not available) |
| `ai_visibility` | `summary`, `crawlers[]` {`agent`, `status` allowed/blocked/partial, `note`}, `citations[]` {`query`, `surface`, `client_cited`, `cited`} |
| `blockers[]` | `title`, `detail`, `fix` |
| `quick_wins[]` | `title`, `detail`, `impact` High/Medium/Low, `effort_hours` (number) — already in priority order |
| `content_strategy` | `page_roadmap[]` {`page`, `url`, `type`, `status` exists/weak/missing, `priority`}, `blog_posts[]` {`title`, `keyword`, `tier`, `purpose`} |
| `opportunities[]` | exactly 3: `title`, `gap`, `why`, `action` |
| `closing` | `headline`, `body`, `cta`, `contact` |

**Consistency checks before rendering** — the numbers in prose must match the data:
the count of blockers in `key_points` or `verdict` equals `blockers[]`, competitor counts match,
and every quick win references something actually found.

---

## What the PDF contains (in order)

1. Cover — client name on the brand color, URL and market, "Prepared by [agency_name]", date
2. Contents
3. Executive summary — market context, verdict, 4-stat bar, key points
4. Business overview & site analysis — facts table, issues by severity
5. Competitor analysis — profiles + feature matrix (client row highlighted)
6. Keyword research — one table per tier, AI Overview flags, data sources where measured
7. Technical SEO audit — PASS/WARN/FAIL by category, basis column, blockers marked, Core Web Vitals
8. AI search visibility — crawler access, who AI answers cite
9. Content strategy — page roadmap + priority blog posts
10. Blockers & quick wins — blockers in a red block first, then ranked quick wins with effort
11. Strategic opportunities — the 3 opportunities as gap / why / what to build
12. Next steps — the agency executes the work; the audit is the pitch

Design rules the script already enforces: light pages, brand color used for the cover band,
table headers and accents (auto-darkened when too light to read as text, and text on the band
flips to dark when the brand color is light), bundled Instrument Sans/Serif fonts, and a
self-contained stat bar that can't collide with surrounding text.

---

## Check before delivering

`check_pdf.py` renders every page to PNG plus a contact sheet and flags near-empty pages,
unfilled placeholders, raw JSON and `None`/`null` cells. It exits non-zero on a problem.

Then **look at the contact sheet and at least the cover, executive summary and technical
pages** with your image-reading tool. Fix anything that's off — in `findings.json` (wrong
counts, cells too long) or in `build_report.py` (layout) — and re-render. Don't send a PDF
you haven't looked at.

---

## Delivering

Hand the PDF to the user with whatever file-sharing mechanism this environment provides.
Keep the message to 2–3 sentences: the headline finding, the number of blockers, and that
`findings.json` is available if they want a deck, a doc, or a re-audit later.
