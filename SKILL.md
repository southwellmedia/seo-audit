---
name: seo-audit
description: >
  Run a full SEO audit and competitive analysis of a client website and produce a
  client-ready PDF proposal. Use when the user asks for an "SEO audit", to "audit this
  site", for "competitive analysis for [client]", "SEO for [URL]", "how is [client] doing
  on SEO", "what's wrong with this site from an SEO standpoint", or a pre-launch SEO check,
  or wants a client's search visibility, keyword strategy, local presence or AI search
  visibility analyzed. Covers live site recon, brand colors, competitors, keywords,
  technical and AI-visibility audit, content strategy, quick wins and the PDF.
---

# SEO Audit Skill

A systematic SEO audit for service businesses, producing a proposal an agency can send
cold. Three business-model branches: **B2C local**, **multi-location B2C**, and **B2B**
(single- or multi-market).

The work happens in this order — intake, recon, competitors, keywords, technical audit,
AI visibility, blockers and quick wins, content strategy, opportunities — and everything
found is written to `findings.json`, which a bundled script renders into the PDF.

Paths below like `references/…` and `scripts/…` are relative to this skill's folder.

---

## Step 0: Intake — get the URL, infer the rest, confirm once

**The only thing you must have to start is the URL.** If the user didn't give one, ask.

Then open the site and infer as much as you can before asking anything else: business name,
services, city/market, neighborhoods or cities named in testimonials and service-area copy,
whether it's live or a staging/pre-launch build, and whether it sells to consumers or businesses.

Then confirm in **one round** of questions (a multiple-choice question tool if you have one,
otherwise one short message). Pre-fill each with what you found so the user can just confirm:

1. **Business & service** — "This looks like [business], a [service] company. Right?"
   Don't assume the service from the URL; similar-sounding services can have very different
   competitive landscapes.
2. **Market & scope** — "[City], serving [areas found]. Wider than that?" (one metro / several
   cities / several states). This decides the branch and the location-page plan.
3. **Locations** — one location, several physical locations, or service-area only?
4. **Anything you know already** — known competitors to include, a previous domain (for
   redirect checks), Google Business Profile status, Search Console access or a keyword-tool
   export, and for B2B the priority markets and the buyer role.

Skip any question the conversation already answers. If the user isn't around to answer,
go with your inferences and say which ones you made when you deliver the report.

**Agency name** — for the cover and closing. Use what you know about the user (memory,
profile, earlier messages). If you don't know it, add it to the confirmation round. Never
invent one: if the user can't be asked, leave `meta.agency_name` empty (the PDF then omits
"Prepared by") and mention it when you deliver.

### Classify the business model

| Branch | Signals | Read next |
|--------|---------|-----------|
| **B2C Local** | Consumers, one metro, one location or service-area business | `references/b2c-local.md` |
| **Multi-location B2C** | Consumers, several physical locations with their own addresses | `references/multi-location.md` + `references/b2c-local.md` |
| **B2B** | Sells to businesses/organizations on contract, one market or many | `references/b2b.md` |

If the signals conflict, ask — the competitive framework differs between branches.

### What the location answers change

| Input | Changes |
|-------|---------|
| Primary city | Tier 1 keywords, competitor search scope, LocalBusiness schema |
| Neighborhoods / suburbs | Tier 2 keywords, location page roadmap, testimonial cross-check |
| Several locations | Per-location pages and GBP scorecard (multi-location branch) |
| Several markets (B2B) | One genuine page per market, build order by priority market |

---

## Step 1: Live site recon

Audit what's actually built, not what the brief says. Use whichever browser tool this
environment has; fall back to fetching pages if there's no browser (and note that you
couldn't check rendering).

### 1a. Walk the site
- Homepage top to bottom; every page in the nav and the footer
- `robots.txt` and `sitemap.xml`
- View-source (raw HTML) for the homepage and one service page — compare with the rendered
  page to spot JavaScript-only content

### 1b. Brand colors
Run `scripts/extract_brand_colors.js` in the page (any tool that evaluates JavaScript).
It returns declared theme colors, brand-like CSS variables, colors ranked by frequency per
role (buttons, links, headings, header), and the logo URL. Pick primary / secondary / accent
from that — usually the button background and CSS tokens agree. If you can't run JavaScript,
look at the logo and buttons and choose; record `brand.source` either way.

### 1c. Document
**Business identity:** name, address (real or placeholder?), phone (does the `tel:` href
match the display?), email, services listed, areas served, what they lead with.

**Structure:** every live page (URL + title), nav structure, whether services are real
URLs or homepage anchors, copyright year.

**Trust & content:** real photos or stock, testimonials (names? locations? dates?),
CTAs linking to `#`, stat counters that don't render.

**For competitors too:** content gaps — what does a buyer need to know before calling that
this site doesn't answer? Where is their SEO clearly weak?

---

## Step 2: Competitive research

Find **6–8 direct competitors**: 2–3 national/franchise players (the ceiling) and 3–5
local or regional operators (the real fight). Start from any the user named.

Per competitor: name, URL, HQ, scale, differentiator, SEO strengths, SEO weaknesses, and
**current** review count and rating with the source. Pull the numbers; never assume them.

Build a **feature matrix**: competitors as rows, 5–7 SEO features as columns. Choose
features that matter in *this* market — e.g. service pages, location pages, published
pricing, active blog, LocalBusiness schema, GBP review volume, cited in AI answers. Keep
labels to one or two words.

The branch reference file has what to look for per model.

---

## Step 3: Keyword research

Four tiers, 40–50 keywords total. Full method in `references/keywords.md`.

| Tier | Intent | Conversion | Built from |
|------|--------|------------|------------|
| 1 Primary Core | Mixed | Medium | Service + primary city, "near me" |
| 2 Local / Neighborhood | Transactional | High | Neighborhoods, suburbs, locations, markets |
| 3 Long-Tail High-Intent | Transactional | Very high | Specific urgent situations, buyer types |
| 4 Informational | Informational | Low | Buyer questions, competitor blogs and FAQs |

For each: intent, difficulty (LOW / MEDIUM / HIGH — an estimate unless you have tool data),
target page, and whether an AI Overview appears. Use Search Console or keyword-tool data when
the user can provide it, and say where numbers came from. Never invent search volumes.

---

## Step 4: Technical SEO audit

Work through `references/technical-checklist.md` — all 13 sections. Rate each item
PASS / WARN / FAIL / N/A and record the basis: **measured**, **observed**, or **estimated**.

Measure what can be measured:
- **Core Web Vitals** — PageSpeed Insights API for the homepage and one key page (mobile);
  use field data when it exists, lab data otherwise, and label which
- **Indexation** — `site:domain.com` count and odd URLs (or Search Console if available)
- **Schema** — Rich Results Test and the Schema.org validator

Don't recommend tactics that no longer work: FAQ rich results ended in May 2026, HowTo
rich results in 2023, and Google doesn't show stars for a business's own reviews.
Section 5 of the checklist has the details.

---

## Step 5: AI search visibility

Checklist section 13. Three parts:

1. **Crawler access** — robots.txt and bot-protection settings for search/answer bots
   (OAI-SearchBot, PerplexityBot, Bingbot, Claude-SearchBot) vs. training-only bots.
2. **Citation spot-check** — 5–8 Tier 1/Tier 3 queries in whichever AI surfaces you can
   reach. Who gets named, and which sources (Yelp, Reddit, local lists) do the answers lean on?
3. **Entity consistency** — NAP across GBP, Bing Places, Apple Business Connect and directories.

Report what you observed as a dated snapshot. If you can't reach an AI surface, say so
rather than guessing.

---

## Step 6: Separate hard blockers from quick wins

**Hard blockers** — the site shouldn't launch (or must be fixed this week if live):
- Placeholder contact info (555 numbers, fake addresses, `tel:` mismatch)
- Dead CTAs (links to `#`)
- Stat counters stuck at 0
- Staging domain indexable, or `noindex`/`Disallow: /` left on production
- Missing legal pages (Privacy Policy, Terms)
- Search/answer bots blocked unintentionally

**Quick wins** — high impact, low effort, ranked by impact ÷ effort. Estimate effort in hours
from what you actually found, not preset numbers. Blockers always come first in the PDF.

---

## Step 7: Content strategy

- **Page roadmap** — core pages, one page per service, location/market pages, audience or
  vertical pages, blog. Mark each exists / weak / missing with a priority.
- **Top 10 blog posts** — ranked by opportunity; each targets a keyword tier, serves a clear
  purpose (cost guide, comparison, local, FAQ, process), and fits what the client actually knows.

---

## Step 8: Strategic opportunities

Exactly **3** angles where this client can beat this competitive set, each grounded in
something you found. For each: the specific gap, why it matters in this market, and what to build.

The question behind each: what does a buyer need before they'll pick up the phone that
nobody in this market provides well?

Good: "No competitor has neighborhood pages, yet 9 of 12 testimonials name three neighborhoods."
"Nobody publishes pricing, and the market leader's reviews keep complaining about surprise quotes."
"AI answers here cite Yelp and one local 'best of' list — the client is in neither."

Not acceptable: "Create great content." "Build more backlinks." "Improve site speed."

---

## Step 9: Build and check the PDF

Full spec in `references/deliverables.md`.

1. Write everything to `findings.json` in the shape of `assets/findings.example.json`.
2. Check that the numbers in your prose match the data (blocker count, competitor count).
3. Render: `python3 <skill-dir>/scripts/build_report.py findings.json -o [ClientName]_SEO_Audit.pdf`
4. Check: `python3 <skill-dir>/scripts/check_pdf.py [ClientName]_SEO_Audit.pdf`, then look at the contact
   sheet and key pages. Fix and re-render until it's clean.
5. Deliver the PDF with the environment's file-sharing tool, with a 2–3 sentence summary.

---

## Tone and framing

- Never "create great content" or "build backlinks" without specifics
- Quantify effort in hours or days
- Every finding is labeled blocker vs. improvement, and measured vs. estimated
- Call out what's working — clients need to know that too
- Verify competitor claims before using them; ratings and pages change
- The audit is the pitch: it closes with [agency_name] ready to do the work, not "good luck"
