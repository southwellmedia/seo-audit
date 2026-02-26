# B2B Multi-State Audit Reference

For businesses selling to other businesses across multiple geographic markets.
Examples: any service sold on contract to property managers, HOA boards, corporate facility teams, or multi-location business operators.

---

## Business model characteristics

- **Customer**: Property managers, HOA boards, corporate facility teams
- **Sales motion**: Contract-based, longer sales cycle, relationship-driven
- **Decision speed**: Slow (multi-stakeholder approval, RFP process)
- **Key trust signals**: Named client logos (if available), service area proof, operational consistency, technology/tracking
- **Primary conversion**: Quote request, demo call, or sales meeting — not same-day booking

---

## Competitive landscape — what to look for

### National enterprise players
Research whether large national operators are present in this category. Common patterns
to verify (confirm these are actually true before using as strategic angles):
- Do their city pages have real local content or are they copy-paste templates?
- What do their consumer reviews actually look like — check current ratings, don't assume
- Are they missing neighborhood or sub-market targeting?
- Do property managers complain about them in online forums or reviews?

### Regional operators
Often better on service quality, worse on SEO. Look for:
- Niche differentiation (employee-owned, eco, app-based, local ownership)
- What they're missing: location pages, blog, pricing transparency

### What to document per competitor
- Name, URL, HQ, scale (markets served, states)
- Technology platform (app, GPS tracking, photo verification, reporting portal)
- Content marketing maturity (blog: active/inactive/none)
- Location page strategy (count, quality: genuine content vs. copy-paste template)
- Review profile — pull current numbers from Google, Yelp, and industry platforms
- Pricing: transparent / estimate-only / hidden
- Differentiator angle (employee-owned, eco, app, local, pricing)
- Any competitor comparison pages they've built

---

## Keyword strategy for B2B multi-state

See `keywords.md` for the full 4-tier framework. B2B-specific notes:

- **Tier 1** targets the homepage with category-defining terms
- **Tier 2** is one keyword per market — each city requires its own location page
- **Tier 3** should target the B2B buyer specifically: property managers, HOA boards,
  facility directors. Include audience qualifiers and switching/evaluation intent terms
  ("switch [service] provider", "[service] pricing for apartments", "best [service] company [city]")
- **Tier 4** should justify the service financially and operationally — B2B buyers need
  to build a business case. Content like "[service] ROI", "how to implement [service]",
  "[service] vs [alternative]" serves mid-funnel decision-makers

Competitor comparison pages are high-value for B2B. Build `/[client]-vs-[competitor]/`
to capture buyers actively evaluating options.

---

## Technical audit priorities for B2B multi-state

### Highest impact
1. **Location pages** — one real page per market, not anchor links
   - `/locations/dallas-fort-worth/` not `/?state=Texas#service-area`
   - Each page: local market context, any relevant local regulations, local testimonial if possible
2. **LocalBusiness schema** — HQ address + service area coverage
3. **FAQPage schema** — property manager FAQ content (usually already exists on site)
4. **Review markup** — named client company references are strong trust signals

### Common B2B-specific fails
- Location "pages" are actually JavaScript-filtered map sections — not indexable
- Service area expressed as "12 states" map with no individual city content
- No main navigation (B2B buyers won't dig for information)
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
- Homepage (keyword-optimized, client logos above the fold if available)
- About (company history, values, leadership — B2B buyers research the company)
- One page per service
- Location pages (one per market — not a map widget)
- Audience landing pages (property managers, HOAs, specific verticals served)
- Blog
- Pricing or packages page (rare in B2B but high-value if client will publish it)

### Blog post types that work for B2B multi-state
1. "What Is [Service]? The Complete Guide for [Audience]"
2. "How Much Does [Service] Cost? [Year] Pricing Guide"
3. "[Service] vs [Alternative]: Which Is Right for You?"
4. "Signs It's Time to Switch Your [Service] Provider"
5. "How [Service] Reduces Cost / Improves Operations for [Audience]"
6. "The [Audience] Guide to Implementing [Service]"
7. "[Service] for [Specific Vertical]: What You Need to Know"
8. "How to Evaluate [Service] Vendors: What to Ask Before Signing"
9. "[Client] vs [Competitor]: An Honest Comparison"
10. Regulatory, compliance, or operational content specific to the client's category and markets

### Competitor comparison pages
High-value for B2B. Build: `/[client]-vs-[competitor]/`
Captures buyers actively evaluating options. Works best when the competitor has
documented weaknesses — verify current review scores and complaints before building
the page around them.

---

## Strategic opportunities for B2B multi-state

Check each of these during research. Only use the ones confirmed to be true —
don't carry assumptions in from other audits.

1. **Location page gap** — Do competitors have real location pages or just a map widget?
   If map widget: genuine location pages with local content will outrank.

2. **Competitor review vulnerability** — Does the market leader have poor consumer reviews?
   Pull current ratings before using this angle — ratings change. If confirmed: displacement
   content targeting "[competitor] alternatives" and "switch [service] provider" is high-value.

3. **Underserved markets** — Are any of the client's service cities low-competition?
   If yes: prioritize those for early location page wins before tackling high-competition cities.

4. **Sustainability angle** — Does any competitor authentically own eco/sustainability?
   If no and client has relevant programs: this can be a content moat.

5. **Pricing transparency** — Does anyone publish pricing in this B2B market?
   If no: even a pricing range guide captures buyers frustrated by "contact us for pricing."

6. **Technology platform** — Does the client have GPS tracking, photo verification, or a
   reporting portal that competitors lack? If yes: build technology-forward content and
   landing pages around it.

7. **Industry review platforms** — Is the client listed on relevant review or directory platforms for their category (G2, Capterra, industry-specific directories)?
   If not: early mover advantage on platforms that already rank for "[service] reviews."

8. **Content gap** — What questions are competitors failing to answer for property managers?
   Look at their blogs, FAQ pages, and support content. What does a property manager need
   to know before signing a contract that nobody is explaining well?
