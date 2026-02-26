# B2B Multi-State Audit Reference

For businesses selling to other businesses across multiple geographic markets.
Examples: valet trash, commercial cleaning, facilities management, property amenity services.

---

## Business model characteristics

- **Customer**: Property managers, HOA boards, corporate facility teams
- **Sales motion**: Contract-based, longer sales cycle, relationship-driven
- **Decision speed**: Slow (multi-stakeholder approval, RFP process)
- **Key trust signals**: Named client logos (Greystar, Cushman & Wakefield), service area proof, operational consistency, technology/tracking
- **Primary conversion**: Quote request, demo call, or sales meeting — not same-day booking

---

## Competitive landscape — what to look for

### National enterprise players
- Often dominant in brand awareness and review volume
- SEO strength: city pages, press releases, sub-brands
- SEO weakness: templated content, copy-paste errors across city pages, poor consumer reviews
- Opportunity: Property managers are sophisticated buyers who see through generic templates

### Regional operators
- Often better on service quality, worse on SEO
- Look for: niche differentiation (employee-owned, eco, app-based, local ownership)
- Usually missing: location pages, blog, pricing transparency

### What to document per competitor
- Name, URL, HQ, scale (units served, states)
- Technology platform (app, GPS tracking, photo verification)
- Content marketing maturity (blog: active/inactive/none)
- Location page strategy (count, quality: genuine vs. template)
- Consumer review profile (Google, Yelp, industry platforms like Revyse)
- Pricing: transparent / estimate-only / hidden
- Differentiator angle (employee-owned, eco, app, local, pricing)
- Any competitor comparison pages they've built

---

## Keyword tiers for B2B multi-state

### Tier 1: Primary core
Format: `[service] service` / `[service] for apartments`
- Brand-level terms — hard to rank short-term but essential
- Target: homepage

### Tier 2: Market / city
Format: `[service] service [city]`
- One keyword per market served — each requires its own location page
- Priority: home market first, then highest-revenue markets
- Example: "valet trash service Dallas", "valet trash service Denver"

### Tier 3: Long-tail B2B intent
Format: qualifier + service + audience
- "valet trash service for property managers"
- "valet trash service pricing for apartments"
- "switch valet trash providers" (captures competitor-dissatisfied buyers)
- "best valet trash company [city]"
- Vertical-specific: "valet trash for student housing", "valet trash for senior living"

### Tier 4: Informational / blog
- "what is [service]" — defines the market
- "how much does [service] cost" — pricing searches from PMs doing research
- "is [service] worth it" — mid-funnel evaluation content
- "[service] vs [alternative]" — comparison content
- "how to implement [service]" — operational guide for PMs
- "[service] ROI" / "[service] increase NOI" — financial justification content for decision-makers

---

## Technical audit priorities for B2B multi-state

### Highest impact
1. **Location pages** — one real page per market, not anchor links
   - `/locations/dallas-fort-worth/` not `/?state=Texas#service-area`
   - Each page: local market context, recycling ordinances if applicable, local testimonial
2. **LocalBusiness schema** — HQ address + service area coverage
3. **FAQPage schema** — property manager FAQ content (usually already exists on site)
4. **Client logo schema / Review markup** — named PM company references are strong signals

### Common B2B-specific fails
- Location "pages" are actually JavaScript-filtered map sections — not indexable
- Service area expressed as "12 states" map with no individual city content
- No navigation menu (property managers won't dig for info)
- Vague "contact us for pricing" with no indication of cost range
- Orphaned service pages not linked from navigation
- Staging domain accessible to crawlers (Vercel/Netlify subdomain not blocked)

### JavaScript rendering risk
B2B sites often use dynamic maps or state filters for service areas.
Flag if: map loads via JS, state filter uses URL params not real paths.
Google indexes the HTML — if service area content only appears after JS runs,
Googlebot may miss it entirely. Recommend: static location pages as the fix.

### Redirect infrastructure
B2B clients often rebrand or rebuild. Always check:
- Old domain / old URLs returning 404 instead of 301
- Staging domain indexed alongside production
- Canonical tags absent (duplicate content risk)

---

## Content strategy for B2B multi-state

### Core pages (must exist at launch)
- Homepage (keyword-optimized, client logos above the fold)
- About (company history, values, leadership — B2B buyers research the company)
- All service pages (one per service)
- Location pages (one per market — not a map widget)
- Property managers landing page (dedicated B2B pitch)
- Vertical pages (HOAs, student housing, senior living — if served)
- Blog
- Pricing / packages (rare in B2B but high-value if done)

### Top blog post types that work for B2B multi-state
1. "What Is [Service]? The Complete Guide for Property Managers"
2. "How Much Does [Service] Cost? [Year] Pricing by Market"
3. "[Service] vs [Alternative]: Which Is Right for Your Property?"
4. "5 Signs It's Time to Switch Your [Service] Provider" (competitor displacement)
5. "How [Service] Increases Your Property's NOI: A Data-Driven Guide"
6. "The Property Manager's Guide to Implementing [Service]"
7. "Recycling Mandates by City: What Multifamily Property Managers Need to Know"
8. "[Service] for HOA Communities: What You Need to Know"
9. "Apartment Amenities That Actually Increase Property Value in [Year]"
10. "[Competitor] vs [Client]: An Honest Comparison" (captures comparison searches)

### Competitor comparison pages
High-value for B2B. Build: `/[client]-vs-[competitor]/`
Captures property managers actively evaluating options.
Works best when the competitor has poor reviews — lead with that.

---

## Strategic opportunities unique to B2B multi-state

Check for these before writing the "3 strategic opportunities" section:

1. **Location page gap** — Do competitors have real location pages or just a map widget?
   If map widget: genuine location pages with local content will outrank.

2. **Competitor review vulnerability** — Does the market leader have terrible consumer reviews?
   If yes (Valet Living = 1.0-2.9 stars): displacement content targeting "[competitor] complaints"
   and "switch [service] provider" is extremely high-value.

3. **Underserved markets** — Are any of the client's service cities low-competition?
   If yes: prioritize those for early location page wins before tackling high-competition cities.

4. **Sustainability angle** — Does any competitor authentically own eco/sustainability?
   If no and client has composting or recycling programs: this is a content moat.

5. **Pricing transparency** — Does anyone publish pricing in this B2B market?
   If no: even a pricing range guide captures buyers who are frustrated by "contact us."

6. **Technology platform** — Does the client have GPS tracking, photo verification, app?
   If yes and competitors don't: build technology-forward content and landing pages.

7. **Industry review platforms** — Is the client on Revyse, G2, Capterra, or similar?
   If not: early mover advantage on platforms that already rank for "[service] reviews."
