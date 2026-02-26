# Technical SEO Checklist

Rate every item: PASS / WARN / FAIL
Flag FAIL items in red in deliverables. WARN items in amber.

---

## 1. Page Structure & Completeness

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| All promised services have dedicated pages | `/services/[name]/` exists and is live | Service sections are homepage anchors only |
| Core pages exist | Home, About, Contact, Quote/Request all live | Missing About or no quote path |
| Location pages exist | Real pages at `/locations/[city]/` | Map widget with JS filtering |
| Blog exists | `/blog/` with at least 3 posts | No blog at all |
| URL structure | Lowercase, hyphenated, logical hierarchy | Underscores, dynamic params, uppercase |
| No orphan pages | Every page reachable from nav or footer | Service pages not linked anywhere |

---

## 2. Title Tags

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Homepage title includes primary keyword | Primary service + city in title | Brand name only with no keyword |
| All titles unique | No two pages share a title | Service page title = homepage title |
| Title includes location | City or region in title for local businesses | No location modifier |
| Title length | 50-60 characters | Under 30 (too thin) or over 70 (truncated) |
| Format | Keyword — Location \| Brand | Brand first, keyword buried |

**Recommended format:**
- Homepage: `[Primary Keyword] [City] \| [Brand Name]`
- Service page: `[Service Name] [City] \| [Brand Name]`
- Location page: `[Service] in [Neighborhood/City] \| [Brand Name]`

---

## 3. Meta Descriptions

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Explicit meta descriptions | Defined in `<head>`, not auto-pulled from content | Google writing its own from body text |
| Unique per page | No duplicates | Same description on all pages |
| Contains CTA | "Get a free quote", "Call today", "Same-day available" | Purely descriptive, no action |
| Length | 140-160 characters | Under 100 (missed opportunity) |
| Includes keyword | Primary keyword appears naturally | Keyword-free |

---

## 4. Heading Hierarchy

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Single H1 per page | Exactly one H1 | Two H1s on homepage |
| H1 contains keyword | Primary keyword in H1 | H1 is a brand tagline with zero keyword signal |
| Logical H2/H3 nesting | H2s for sections, H3s for subsections | H3s used before H2s, or all headings same level |
| No heading skips | H1 → H2 → H3, not H1 → H3 | Jumping levels |

---

## 5. Schema Markup

Run a two-part schema audit for every site:

**Part 1 — What exists (and is it useful?)**
Open page source or use a schema validator. List every schema type found. For each:
- What type is it?
- Is it complete or skeleton-only?
- Is it accurate (real phone, real address, real hours)?
- Verdict: STRONG / WEAK / BROKEN

**Part 2 — What's missing or weak (prioritized)**
Only flag HIGH and MEDIUM priority gaps. For each HIGH priority item, generate the fix.

| Schema Type | When Required | Priority |
|-------------|---------------|---------|
| LocalBusiness | Every local business site | CRITICAL |
| FAQPage | Any page with FAQ section | HIGH — enables rich results |
| Service | Each service page | HIGH |
| Review / AggregateRating | When testimonials exist | HIGH — enables star ratings in SERP |
| Organization | Homepage | MEDIUM |
| BreadcrumbList | Any page 2+ levels deep | MEDIUM |
| Person | Named founder with documented expertise | MEDIUM — E-E-A-T signal |

**LocalBusiness minimum required fields:**
```json
{
  "@type": "LocalBusiness",
  "name": "",
  "url": "",
  "telephone": "",
  "email": "",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "",
    "addressLocality": "",
    "addressRegion": "",
    "postalCode": "",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 0, "longitude": 0 },
  "openingHours": [],
  "areaServed": []
}
```

---

## 6. Internal Linking & Navigation

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Main nav exists | Header navigation with key pages | Logo + phone only |
| Services in nav | All service pages linked | Services dropdown missing |
| Footer sitemap | Footer links to all key pages | Footer has contact info only |
| No dead links | No `href="#"` on real CTAs | "SCHEDULE NOW" links to # |
| Breadcrumbs | Present on service/location pages | No breadcrumbs |
| Homepage → Service pages | Service cards link to real pages | Cards link to anchor (#services) |

---

## 7. JavaScript & Dynamic Content

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Key content in HTML | Critical text in source HTML | Content only appears after JS runs |
| Location data indexable | Location content in static HTML | Map loads via `fetch()` after page load |
| No URL param pages | Locations at `/locations/texas/` | Locations at `/?state=Texas#map` |
| Stat counters | Show real numbers or are static | Counters stuck at 0 (JS not loading) |

> Note: Google runs a "two-wave" indexing process — HTML first, JS later.
> Content in the JS-only wave may not be indexed for days or may be missed entirely.
> Any content critical to SEO should be in the static HTML.

---

## 8. Infrastructure

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| sitemap.xml | Exists, submitted to GSC | Missing |
| robots.txt | Exists, references sitemap | Missing |
| Canonical tags | Every page has `<link rel="canonical">` | Absent — staging + production both indexed |
| Staging blocked | Staging domain returns noindex or redirects | Vercel/Netlify subdomain indexed |
| 301 redirects | Old URLs redirect to new equivalents | Old URLs return 404 |
| HTTPS | Full SSL, no mixed content | HTTP pages or mixed content warnings |
| Copyright year | Shows current year | Shows prior year (suggests abandoned site) |

---

## 9. Mobile & Page Experience

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Mobile-responsive | Layout renders correctly on 375px viewport | Fixed-width layout breaks on mobile |
| Tap targets | Buttons and links at least 44px tall | Tiny links impossible to tap accurately |
| Text readable without zoom | Base font size 16px or larger | 12px body text requiring pinch-zoom |
| No horizontal scroll | Content fits viewport width | Elements overflow causing side-scroll |
| LCP (Largest Contentful Paint) | Under 2.5s | Hero image or font blocking render |
| CLS (Cumulative Layout Shift) | Score under 0.1 | Images without dimensions, late-loading fonts |
| INP (Interaction to Next Paint) | Under 200ms | Heavy JS blocking interaction response |

> Check Core Web Vitals in Google Search Console if the site has enough traffic data.
> For new sites use PageSpeed Insights (pagespeed.web.dev) as a proxy.

---

## 10. Images

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Alt text | All images have descriptive alt attributes | Empty alt or filename as alt |
| Format | WebP or AVIF | Unoptimized JPG/PNG |
| Lazy loading | `loading="lazy"` on below-fold images | All images load immediately |
| File size | Under 200KB for most images | Multi-MB images |
| Real photos | Actual job/team/location photos | Generic stock photos (trust killer for local service) |

---

## 11. Social & Open Graph Meta

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| og:title | Set explicitly, keyword-relevant | Missing or defaults to page title |
| og:description | Set explicitly with CTA | Missing or same as meta description |
| og:image | 1200×630px image set | Missing — social shares show blank card |
| og:url | Canonical URL set | Missing |
| twitter:card | `summary_large_image` set | Missing — Twitter/X shows small card |

---

## 12. Contact Info & Placeholders

This section trips up new sites most often. Always check:

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Phone number real | Not 555-xxxx, not placeholder tel: href | Placeholder number in HTML |
| Tel: href matches display | The number shown = the number dialed | Display and href are different numbers |
| Email real | Active inbox, correct domain | Placeholder or unmonitored address |
| Address real | Real street address | "123 Main St" placeholder |
| Business hours | Accurate hours listed | No hours or "TBD" |

---

## Quick reference: what FAIL means in a proposal

- **FAIL** = This issue is actively hurting you right now. Fix before launch or fix immediately.
- **WARN** = This is a missed opportunity. Not breaking, but leaving ranking and conversion on the table.
- **PASS** = This is done correctly. Call it out — clients need to know what's working too.
