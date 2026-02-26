---
name: seo-audit
description: >
  Run a full SEO audit and competitive analysis for a client website, producing
  a professional PDF proposal and infographic highlights PNG. Use this skill
  whenever a user mentions "SEO audit", "audit this site", "competitive analysis
  for [client]", "SEO for [URL]", "how is [client] doing on SEO", or asks to
  analyze a client's online presence, keyword strategy, or search visibility.
  Also trigger when a user says things like "we're about to launch this site"
  or "what's wrong with this site from an SEO standpoint." This skill covers
  the full workflow: live site recon, brand color extraction, competitor research,
  keyword categorization, technical audit, content strategy, quick wins, and
  deliverable generation (PDF + infographic PNG). Built by Southwell Media.
---

# SEO Audit Skill — Southwell Media Methodology

A systematic local-service SEO audit workflow for producing client-ready proposals.
Covers both **B2C single-market** (e.g. junk removal, HVAC, roofing) and
**B2B multi-state** (e.g. valet trash, facilities management) business models.

---

## Step 0: Client intake — ask before doing anything

Run this intake before any research, recon, or analysis. If information is already
clear from context, skip that question — don't ask what you already know.

**Do not proceed past Step 0 until you have: URL, city, and industry at minimum.**

---

### Core questions (always ask if not provided)

**1. URL**
"What's the URL of the site we're auditing?"
→ Used for: live recon, brand color extraction, technical audit

**2. Business name**
"What's the business name?" (or infer from URL if obvious)
→ Used for: deliverable filenames, report cover, competitive framing

**3. Industry / service**
"What service do they provide?"
→ Used for: business model classification, competitor research, keyword tiers
→ ⚠️ Do not assume from the URL — confirm. "junk removal" ≠ "valet trash"
   even if both involve hauling.

---

### Location questions (always ask — these shape the entire audit)

**4. Primary city / market**
"What city or metro is their primary market?"
→ Used for: Tier 1 keywords (`[service] [city]`), competitor research scope,
   Google Business Profile advice, LocalBusiness schema coordinates

**5. Neighborhoods or districts served**
"Do they serve specific neighborhoods or areas within that city?
Any areas they're known for or want to target?"
→ Used for: Tier 2 keyword list, location page roadmap, testimonial seeding
→ If they don't know: pull from testimonials during recon (Step 1) and
   come back to confirm — "I found mentions of Oak Lawn, Deep Ellum, and
   Uptown in your testimonials — should we target these as neighborhood pages?"

**6. Geographic scope**
"Is this just [city], or do they serve a wider region — multiple cities,
the whole metro, or multiple states?"
→ Used for: business model classification (B2C local vs. B2B multi-state),
   number of location pages needed, keyword volume expectations

| Answer | Classification | Location page scope |
|--------|---------------|-------------------|
| One city / metro | B2C Local (likely) | 5-12 neighborhood pages |
| Multi-city, one state | B2C Regional | City pages + neighborhoods |
| Multi-state | B2B Multi-State (likely) | One page per major market |

**7. Service radius (B2C only)**
If B2C: "How far out do they travel? Do they serve suburbs like [Plano, Frisco,
Irving] or just the core city?"
→ Used for: extending Tier 2 keywords to adjacent suburbs, additional location pages
→ Suburbs are often less competitive than the city center — high-value targets

---

### Conditional questions (only ask if relevant)

**8. Launch status** — ask if unclear from context
"Is this site currently live, or is this a pre-launch / rebuild situation?"
→ If pre-launch: staging domain blocking becomes a hard blocker
→ If rebuild: ask for old URL to check redirect needs

**9. Old domain / previous site** — ask if it's a rebuild or rebrand
"Was there a previous website or domain? What was the URL?"
→ Used for: 301 redirect audit, link equity preservation, old URL 404 checks

**10. Known competitors** — ask to save research time
"Are there any competitors you're already aware of — either ones you worry
about or ones you want to beat?"
→ If yes: start research from those, fill gaps to 6-8 total
→ If no: identify from scratch via web search

**11. Priority markets (B2B multi-state only)**
"Which of your service states or cities are highest priority for new business?"
→ Used for: location page build order, which markets to research competitively first

**12. Existing Google Business Profile**
"Do they have a Google Business Profile set up? Do you know how many reviews
they have?"
→ Used for: GBP recommendations section, review generation strategy,
   "near me" keyword advice

---

### What changes based on location answers

This is why location questions matter — each answer has downstream consequences:

| Location input | What it changes |
|---------------|----------------|
| Primary city | Tier 1 keywords, competitor search scope, LocalBusiness schema |
| Neighborhoods named | Tier 2 keyword list, location page count, testimonial cross-reference |
| Suburbs / service radius | Additional Tier 2 keywords, extended location page roadmap |
| Multi-state scope | Switches to B2B branch, one page-per-market strategy |
| No neighborhoods known | Flag during recon — pull from testimonials, return to confirm |

---

### After intake: classify the business model

Based on answers, classify into one of two branches:

| Branch | Signals | Read next |
|--------|---------|-----------|
| **B2C Local** | Single city/metro, consumer-facing, on-demand | `references/b2c-local.md` |
| **B2B Multi-State** | Multi-region, sells to property managers or businesses, contract-based | `references/b2b-multistate.md` |

> ⚠️ When in doubt, confirm with the user before branching.
> The entire competitive analysis framework differs between the two.

---

## Step 1: Live site recon

Before any analysis, audit what's actually built — not what the brief says exists.

### 1a. Browser navigation (use Claude in Chrome tools)
- Navigate to the live URL
- Screenshot the homepage, scroll through all sections
- Note every page in the nav — don't trust what the client told you
- Check footer for sitemap-style links — often reveals pages nav misses

### 1b. Brand color extraction (always do this — needed for deliverables)
Use `javascript_tool` to extract exact brand colors from the live CSS:

```javascript
// Resolve oklch/hsl to hex via canvas
function resolveColor(colorStr) {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = 1;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = colorStr;
  ctx.fillRect(0, 0, 1, 1);
  const [r, g, b] = ctx.getImageData(0, 0, 1, 1).data;
  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
}

// Get computed colors from key elements
const brandEls = document.querySelectorAll('[class*="brand"], [class*="primary"], [class*="accent"], h1, button, a');
const colors = {};
brandEls.forEach(el => {
  const cs = getComputedStyle(el);
  ['color','backgroundColor'].forEach(prop => {
    const val = cs[prop];
    if (val && !val.includes('rgba(0, 0, 0, 0)') && !val.includes('255, 255, 255')) {
      colors[el.className?.toString().slice(0,50)] = { [prop]: resolveColor(val) };
    }
  });
});
JSON.stringify(colors, null, 2);
```

Record: primary color, secondary color, accent color, background, text color.
These are required for the infographic deliverable.

### 1c. What to document from recon
- All live pages (URL + title)
- Navigation structure
- Contact info accuracy (phone, email, address — flag placeholders)
- Copyright year
- Any CTAs that link to `#` (dead links)
- Stat counters or dynamic elements that may not be rendering

---

## Step 2: Competitive research

See the relevant reference file for industry-specific competitor lists and what to look for.

General framework (applies to both branches):

**Find 6-8 direct competitors.** Mix of:
- 2-3 national/franchise players (understand the ceiling)
- 3-4 local/regional operators (understand the real fight)

**For each competitor, document:**
- Name, URL, headquarters, scale
- Core differentiators (1-2 sentences)
- SEO strengths (content depth, location pages, reviews, schema)
- SEO weaknesses (generic content, no pricing, thin local signals)
- Review volume and average rating

**Build a feature matrix** — columns are competitors, rows are key SEO features:
- Location/city pages
- Blog/content marketing
- Pricing transparency
- Schema markup
- Review volume
- App or tech differentiator
- Eco/social angle

---

## Step 3: Keyword research

Organize into 4 tiers. See `references/keywords.md` for full framework.

**Location inputs from Step 0 directly feed this step:**
- Primary city → Tier 1 (`[service] [city]`)
- Neighborhoods named → Tier 2 starting list
- Suburbs / service radius → extend Tier 2 beyond city center
- Testimonials (from Step 1 recon) → additional Tier 2 seeds if neighborhoods weren't known upfront

| Tier | Intent | Volume | Conversion | Location input used |
|------|--------|--------|------------|-------------------|
| Primary Core | Mixed | High | Medium | Primary city |
| Local/Neighborhood | Transactional | Medium | High | Named neighborhoods + suburbs |
| Long-Tail High-Intent | Transactional | Low | Very High | Primary city + specific situations |
| Informational/Blog | Informational | High | Low | No location needed |

Target 40-50 keywords total across all tiers. Document for each:
- Search intent
- Relative difficulty (LOW / MEDIUM / HIGH)
- Target page (homepage, service page, location page, blog)

---

## Step 4: Technical SEO audit

Run through every item in `references/technical-checklist.md`.

Rate each item: **PASS** / **WARN** / **FAIL**

Categories to cover:
1. Page structure & completeness
2. Title tags & meta descriptions
3. Heading hierarchy (H1/H2/H3)
4. Schema markup (LocalBusiness, FAQPage, Service, Review)
5. Internal linking & navigation
6. JavaScript / dynamic content risks
7. Infrastructure (sitemap.xml, robots.txt, canonicals, redirects)
8. Images (alt text, format, lazy loading)

---

## Step 5: Separate hard blockers from quick wins

This is a critical Southwell distinction — don't mix these.

**Hard blockers** = site should NOT go live until resolved:
- Placeholder contact info (555 numbers, fake addresses)
- Dead CTAs (links to `#`)
- Stat counters showing 0 with no real data
- Staging domain not blocked from indexing
- Legal pages missing (Privacy Policy, Terms)

**Quick wins** = high-impact, low-effort improvements ranked by impact ÷ effort:
- Title tag and H1 rewrites (1 hr)
- Meta descriptions (2 hrs)
- Schema markup — LocalBusiness + FAQPage (2-3 hrs)
- Sitemap + robots.txt (1 hr)
- 301 redirects from old URLs (1 hr)
- Service page builds (days)
- Location page builds (days)

Always flag blockers in RED in the deliverable. Quick wins in numbered priority order.

---

## Step 6: Content strategy

Two outputs:

**Page structure roadmap** — what pages should exist:
- Core pages (homepage, about, contact, quote/request)
- Service pages (one per service)
- Location pages (one per market — real pages, not anchor links)
- Audience landing pages (property managers, contractors, HOAs, etc.)
- Blog

**Top 10 blog posts** — ranked by search opportunity:
- Must target a specific keyword tier
- Must serve a content purpose (pillar, comparison, FAQ, local)
- Must fit the client's actual expertise

---

## Step 7: Strategic opportunities

Identify 3 specific angles where this client can outmaneuver competitors.
These should be genuinely unique to this business — not generic SEO advice.

Good examples:
- "No competitor has neighborhood-level pages despite testimonials citing those areas"
- "Market leader has 1.0-star reviews — own the reliability messaging angle"
- "Only player in this market without published pricing — transparency is a differentiator"

Bad examples (too generic, don't use):
- "Create great content"
- "Build more backlinks"
- "Improve site speed"

---

## Step 8: Generate deliverables

Two deliverables every time:

### 8a. Full PDF audit report
See `references/deliverables.md` for PDF structure and ReportLab implementation.

Sections (in order):
1. Cover page (client name, brand colors, "Prepared by Southwell Media")
2. Table of contents
3. Executive summary with stat callout bar
4. Business overview & site analysis
5. Competitor analysis with feature matrix
6. Keyword research tables by tier
7. Technical SEO audit with PASS/WARN/FAIL ratings
8. Content strategy (page roadmap + blog post list)
9. Quick wins ranked list
10. Strategic opportunities

### 8b. Infographic highlights PNG
See `references/deliverables.md` for PIL canvas implementation.

Uses canvas-design skill philosophy: HAUL MANIFEST / DEMOLITION DISPATCH aesthetic.
- Black background, brand colors as primary accents
- BigShoulders font for headers, IBMPlexMono for data
- Sections: stat bar, critical blockers, technical audit grid,
  competitor landscape, keyword targets, 3 strategic opportunities, quick wins

Use the brand colors extracted in Step 1b. Do not use generic orange/orange2.

---

## Deliverable naming convention

```
[ClientName]_SEO_Audit.pdf
[ClientName]_SEO_Infographic.png
```

Both go to `/mnt/user-data/outputs/`.

---

## Notes on tone and framing

- Never write "create great content" as a recommendation
- Never recommend "build backlinks" without specifics
- Always quantify effort in hours or days
- Always note when a finding is a blocker vs. an improvement
- Southwell Media positioning: we execute the technical work — the audit is the pitch
- The audit closes with Southwell's capability to implement, not a vague "good luck"
