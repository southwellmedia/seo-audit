# B2B Service Audit Reference

For businesses that sell to other businesses or organizations on contract — in one market
or across many. Examples: commercial cleaning, facilities and maintenance services,
managed IT, commercial landscaping, staffing, security, waste and recycling, commercial
HVAC, B2B professional services (accounting, legal, engineering).

Two variants share this reference:

| Variant | Signals | Location strategy |
|---------|---------|-------------------|
| **Single-market B2B** | One metro, sells to businesses | City + major suburb pages; focus on industry/vertical pages over geography |
| **Multi-market B2B** | Several metros or states | One genuine page per market; build order by priority market |

---

## Business model characteristics

- **Customer**: The specific buyer role matters more than the company — identify it at
  intake (e.g. facility manager, office manager, property manager, operations director,
  procurement, IT lead, owner of a small business)
- **Sales motion**: Contract-based, longer cycle, relationship-driven
- **Decision speed**: Slow — multiple stakeholders, sometimes an RFP
- **Key trust signals**: Named client logos and case studies (with permission), proof of
  coverage in the buyer's market, certifications/insurance/compliance, how service
  quality is reported to the buyer
- **Primary conversion**: Quote request, consultation, or sales call — not same-day booking

---

## Competitive landscape — what to look for

### National / enterprise players
Check whether large national operators compete in this category. Patterns worth
verifying (confirm each is true before using it as a strategic angle):
- Do their city pages have real local content, or are they copy-paste templates?
- What do their reviews actually say? Pull current ratings — don't assume.
- Do buyers complain about them in reviews, forums, or Reddit? About what, specifically?

### Regional and local operators
Often better on service, weaker on SEO. Look for:
- Their differentiation angle (ownership model, specialization, technology, response time, pricing model)
- What they're missing: location pages, vertical pages, case studies, blog, pricing guidance

### What to document per competitor
- Name, URL, HQ, scale (markets served)
- Verticals or buyer types they target explicitly
- Proof assets: case studies, client logos, certifications, reporting/portal
- Content marketing maturity (blog: active / inactive / none)
- Location page strategy (count; genuine content vs. template)
- Review profile — current numbers from Google and any industry platforms (G2, Clutch, Capterra, trade directories)
- Pricing: published / range given / "contact us" only
- Comparison or "alternative to" pages they've built

---

## Keyword strategy for B2B

See `keywords.md` for the 4-tier framework. B2B-specific notes:

- **Tier 1** — category-defining terms + city/market for the homepage and main service pages
- **Tier 2** — one keyword cluster per market (multi-market) or per vertical (single-market).
  For single-market B2B, `[service] for [industry] [city]` is often a better Tier 2 than neighborhoods.
- **Tier 3** — the buyer role and their evaluation intent: `[service] for [buyer type]`,
  `switch [service] provider`, `[service] pricing for [business type]`, `best [service] company [city]`
- **Tier 4** — business-case content: cost, ROI, compliance, "how to evaluate vendors",
  `[service] vs [alternative/in-house]`. B2B buyers need material to justify the decision internally.

Comparison pages (`/[client]-vs-[competitor]/`, `/[competitor]-alternatives/`) are high-value
for B2B — keep them factual and fair, and verify every claim about the competitor.

---

## Technical audit priorities for B2B

### Highest impact
1. **Location pages** (multi-market) — one real page per market, not a map widget
   - `/locations/dallas-fort-worth/` not `/?state=Texas#service-area`
   - Each page: local context, local clients or case studies if any, relevant local regulations
2. **Vertical / buyer pages** — one page per industry or buyer type served
3. **Organization + LocalBusiness schema** — HQ address, `areaServed` for every market, `sameAs` profiles
4. **Proof content in HTML** — case studies, client logos with alt text, certifications as text, not only images

### Common B2B fails
- Location "pages" are JavaScript-filtered map sections — not indexable
- Service area shown as a map of "12 states" with no individual market content
- No main navigation (B2B buyers won't dig)
- "Contact us for pricing" with no indication of cost range or pricing model
- Orphaned service or vertical pages
- Staging domain crawlable (Vercel/Netlify preview subdomains)
- Case studies locked in PDFs or gated forms — not indexable, not citable by AI

### JavaScript rendering risk
B2B sites often use dynamic maps or state filters. Flag if the map loads via JS or the
filter uses URL params instead of real paths. Static location pages are the fix.

### Redirect infrastructure
B2B clients often rebrand or rebuild. Check:
- Old domain / old URLs returning 404 instead of 301
- Staging domain indexed alongside production
- Canonical tags missing

---

## Content strategy for B2B

### Core pages
- Homepage (keyword-optimized; client logos above the fold if available)
- About (history, leadership, values — B2B buyers research the company)
- One page per service
- One page per vertical / buyer type
- Location pages (multi-market)
- Case studies
- Blog
- Pricing or "how pricing works" page (rare in B2B, high-value if the client will publish ranges)

### Blog post types that work for B2B
1. "What Is [Service]? The Complete Guide for [Buyer Type]"
2. "How Much Does [Service] Cost? [Year] Pricing Guide"
3. "[Service] vs [Alternative / In-House]: Which Is Right for You?"
4. "Signs It's Time to Switch Your [Service] Provider"
5. "How [Service] Reduces Cost / Risk for [Buyer Type]"
6. "How to Evaluate [Service] Vendors: Questions to Ask Before Signing"
7. "[Service] for [Specific Industry]: What You Need to Know"
8. "[Client] vs [Competitor]: An Honest Comparison"
9. Compliance, regulatory, or operational content specific to the category and markets
10. Case-study-led posts: "How [Client Type] Cut [Metric] With [Service]"

---

## Strategic opportunities for B2B

Check each during research. Only use the ones confirmed true for this market.

1. **Location page gap** — Competitors use a map widget or templated pages? Genuine market pages win.
2. **Vertical page gap** — Nobody speaks directly to a specific industry the client serves well?
3. **Competitor review vulnerability** — Market leader has poor reviews about a specific
   problem the client solves? Pull current ratings first. If confirmed: "alternatives" and
   "switch provider" content is high-value.
4. **Underserved markets** — Any of the client's markets low-competition? Build those location pages first.
5. **Pricing transparency** — Nobody publishes pricing or ranges? Even a "how pricing works"
   guide captures buyers frustrated by "contact us."
6. **Proof gap** — Competitors make claims with no case studies or reporting? The client's
   documented results (with permission) are hard to copy.
7. **Industry review platforms** — Client missing from the platforms that rank for
   "[service] reviews" or that AI answers cite (G2, Clutch, trade directories)?
8. **Content gap** — What does the buyer need to know before signing that nobody explains
   well? Read competitors' blogs, FAQs and support content to find it.
