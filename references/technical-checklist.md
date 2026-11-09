# Technical SEO Checklist

Rate every item: **PASS** / **WARN** / **FAIL**. Add **N/A** when a check genuinely
doesn't apply (e.g. no blog yet on a pre-launch site — that's a roadmap item, not a fail).

Every rating records **how it was determined**:

- `measured` — from a tool or API (PageSpeed Insights, Search Console, schema validator, page source)
- `observed` — seen directly in the browser or page source during recon
- `estimated` — a judgment call; say what it's based on

The PDF shows this so the client can tell a measured Core Web Vitals score from an educated
guess. Never present an estimate as a measurement.

Flag FAIL items in red in deliverables, WARN in amber.

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
| Title width | Roughly 50–60 characters (Google truncates at ~600px, not a fixed character count) | Under 30 (too thin) or long enough that the keyword is cut off |
| Format | Keyword — Location \| Brand | Brand first, keyword buried |

Google rewrites a large share of titles, usually when the title is vague, stuffed, or
doesn't match the H1. A clear title that matches the page's H1 is the best way to keep yours.

**Recommended format:**
- Homepage: `[Primary Keyword] [City] | [Brand Name]`
- Service page: `[Service Name] [City] | [Brand Name]`
- Location page: `[Service] in [Neighborhood/City] | [Brand Name]`

---

## 3. Meta Descriptions

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Explicit meta descriptions | Defined in `<head>` | Missing — Google writes its own from body text |
| Unique per page | No duplicates | Same description on all pages |
| Contains CTA | "Get a free quote", "Call today", "Same-day available" | Purely descriptive, no action |
| Length | ~140–160 characters | Under 100 (missed opportunity) |
| Includes keyword | Primary keyword appears naturally | Keyword-free |

Meta descriptions aren't a ranking factor. They affect click-through, and Google often
replaces them with a snippet that better matches the query. Rate them WARN at worst,
never FAIL.

---

## 4. Heading Hierarchy

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| One clear H1 per page | A single H1 that names the page topic | Two H1s, or no H1 |
| H1 contains keyword | Primary keyword in H1 | H1 is a brand tagline with zero keyword signal |
| Logical H2/H3 nesting | H2s for sections, H3s for subsections | All headings the same level, or headings used for styling |

Heading-level skips (H1 → H3) are an accessibility issue more than a ranking one — rate WARN.

---

## 5. Structured Data (Schema)

Run a two-part schema audit for every site. Use Google's Rich Results Test and the
Schema.org validator (validator.schema.org) — the first tells you what Google will show,
the second tells you whether the markup is valid at all.

**Part 1 — What exists (and is it useful?)**
List every schema type found. For each:
- Type, and whether it's complete or skeleton-only
- Accurate? (real phone, address, hours — matches the page and the GBP)
- Verdict: STRONG / WEAK / BROKEN

**Part 2 — What's missing (prioritized)**
Only flag HIGH and MEDIUM gaps. For each HIGH item, write the actual JSON-LD fix.

| Schema Type | When to use | Priority | What it does now |
|-------------|-------------|----------|------------------|
| LocalBusiness (most specific subtype — `Plumber`, `Dentist`, `HVACBusiness`…) | Every local business | CRITICAL | Entity understanding; feeds knowledge panel and AI answers |
| Organization | Homepage of any business | HIGH | Logo, sameAs links to profiles, entity consolidation |
| Service | Each service page | MEDIUM | Clarifies what's offered; no rich result |
| BreadcrumbList | Any page 2+ levels deep | MEDIUM | Breadcrumb trail in results |
| Person | Named founder/practitioner with real credentials | MEDIUM | E-E-A-T signal, entity linking |
| FAQPage | Pages with a genuine FAQ | LOW | **No rich result** (see below) |
| Review / AggregateRating | Only for products or third-party-sourced reviews | LOW / don't recommend for the business itself | **No stars for the business's own reviews** (see below) |

**What changed — don't promise these in an audit:**

- **FAQ rich results are gone.** Google stopped showing FAQ rich results for all sites on
  May 7, 2026 (after limiting them to government and health sites in 2023). FAQPage markup
  isn't deprecated and Google still reads it, so existing markup can stay, but never pitch it
  as "enables rich results." The FAQ *content* still matters — it answers buyer questions and
  is the kind of passage AI answers quote.
- **No self-serving review stars.** Since 2019 Google doesn't show star ratings for reviews
  a LocalBusiness or Organization publishes about itself, whether added directly or via a
  widget. Marking up on-site testimonials as AggregateRating won't produce stars, and
  inflated markup can earn a manual action. Point review effort at the Google Business
  Profile instead — that's where stars show for local businesses.
- **HowTo rich results** were removed in 2023. Don't recommend HowTo markup for results.

**LocalBusiness minimum fields:**
```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "",
  "url": "",
  "telephone": "",
  "email": "",
  "image": "",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "",
    "addressLocality": "",
    "addressRegion": "",
    "postalCode": "",
    "addressCountry": "US"
  },
  "geo": { "@type": "GeoCoordinates", "latitude": 0, "longitude": 0 },
  "openingHoursSpecification": [],
  "areaServed": [],
  "sameAs": []
}
```

Use the most specific `@type` that fits. Fill `sameAs` with the GBP, Yelp, BBB, Facebook,
LinkedIn and industry-directory URLs — it ties the entity together for search engines and AI.
Service-area businesses that hide their address on GBP should omit `streetAddress` and
`geo` (coordinates would reveal the hidden location) and rely on `areaServed`.

---

## 6. Internal Linking & Navigation

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Main nav exists | Header navigation with key pages | Logo + phone only |
| Services in nav | All service pages linked | Services dropdown missing |
| Footer links | Footer links to all key pages | Footer has contact info only |
| No dead links | No `href="#"` on real CTAs | "SCHEDULE NOW" links to # |
| Breadcrumbs | Present on service/location pages | No breadcrumbs |
| Homepage → Service pages | Service cards link to real pages | Cards link to anchor (#services) |

---

## 7. JavaScript & Dynamic Content

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Key content in HTML | Critical text present in the raw HTML response | Content only appears after JS runs |
| Location data indexable | Location content in static HTML | Map loads via `fetch()` after page load |
| No URL-param pages | Locations at `/locations/texas/` | Locations at `/?state=Texas#map` |
| Links are real links | Navigation uses `<a href>` | Click handlers on `<div>`s — not crawlable |
| Stat counters | Show real numbers in the HTML | Counters stuck at 0 (JS not loading) |

**How to check:** compare the raw HTML (view-source, or fetch the URL without running JS)
against the rendered page. Anything that only exists in the rendered version is at risk.

**Why it matters:** Google does render JavaScript, usually within minutes, but rendering
can fail and JS-only content is the first thing to go missing. The bigger reason now is
that **most AI crawlers (GPTBot, ClaudeBot, PerplexityBot) don't execute JavaScript at all.**
Content that only appears after JS runs is invisible to them, so it can't be cited in AI answers.

---

## 8. Infrastructure & Indexing

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| sitemap.xml | Exists, lists only indexable 200-status URLs, submitted to GSC | Missing, or lists redirects/404s |
| robots.txt | Exists, references sitemap, doesn't block important paths | Missing, or `Disallow: /` left over from staging |
| Canonical tags | Every indexable page has a self-referencing `<link rel="canonical">`; duplicates/variants point to the preferred URL | Absent — staging and production both indexed; or every page canonicals to the homepage |
| Staging blocked | Staging domain returns noindex, auth, or redirects | Vercel/Netlify preview subdomain indexed |
| 301 redirects | Old URLs redirect to new equivalents | Old URLs return 404 |
| HTTPS | Full SSL, no mixed content, HTTP → HTTPS redirect | HTTP pages or mixed-content warnings |
| www / non-www | One version, the other 301s to it | Both resolve separately |
| Indexation | Key pages indexed (confirm per URL); no junk URLs in results | Staging, parameter, tag or old-domain URLs showing in results; key pages confirmed missing |

**Indexation check:** run `site:domain.com` in Google and note the approximate count and any
odd URLs (staging, parameters, tag pages, old domain). If the client grants Search Console
access, use the Pages (indexing) report instead — it's authoritative. `site:` counts are
rough and often wrong in both directions, so a low count is only a lead: check the key
pages individually (`site:domain.com/services/drain-cleaning/` or Search Console's URL
Inspection) before reporting anything as not indexed. Junk URLs that do show up are a real finding.

---

## 9. Mobile & Page Experience

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Mobile-responsive | Layout renders correctly at 375px | Fixed-width layout breaks on mobile |
| Tap targets | Buttons and links at least ~44px tall | Tiny links impossible to tap |
| Text readable without zoom | Base font 16px or larger | 12px body text |
| No horizontal scroll | Content fits viewport width | Elements overflow |
| LCP (Largest Contentful Paint) | ≤ 2.5s | Hero image or font blocking render |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | Images without dimensions, late-loading fonts |
| INP (Interaction to Next Paint) | ≤ 200ms | Heavy JS blocking interaction |

**Measure these — don't eyeball them.** Run the PageSpeed Insights API for the homepage and
one key service page, mobile strategy:

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<URL>&strategy=mobile
```

Open it with the browser or a web fetch tool (the API works without a key at low volume).
From the JSON:

- `loadingExperience.metrics` — **real-user (CrUX) field data** for LCP, CLS, INP. Use this
  when present; it's what Google uses. Mark `measured (field)`.
- `lighthouseResult.audits` — **lab data** (`largest-contentful-paint`,
  `cumulative-layout-shift`, `total-blocking-time`). Use when the site has too little
  traffic for field data. Mark `measured (lab)` and note that lab INP isn't available —
  Total Blocking Time is the proxy.

If the API can't be reached, mark LCP, CLS and INP **N/A — not measured** and leave the values
null; don't estimate them by eye. You can still note visible causes (a huge hero image,
layout jumping as fonts load) as findings in their own rows.

---

## 10. Images

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Alt text | Descriptive alt on meaningful images | Empty alt or filename as alt |
| Format | WebP or AVIF | Unoptimized JPG/PNG |
| Lazy loading | `loading="lazy"` on below-fold images (never on the LCP hero) | Hero lazy-loaded, or nothing lazy-loaded |
| Dimensions | `width`/`height` set | Missing — causes layout shift |
| File size | Under ~200KB for most images | Multi-MB images |
| Real photos | Actual job/team/location photos | Generic stock (trust killer for local service) |

---

## 11. Social & Open Graph Meta

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| og:title / og:description | Set explicitly | Missing |
| og:image | 1200×630 image set | Missing — shares show a blank card |
| og:url | Canonical URL | Missing |
| twitter:card | `summary_large_image` | Missing — X shows a small card |

These don't affect rankings; rate missing tags WARN.

---

## 12. Contact Info & Placeholders

This section trips up new sites most often. Always check:

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Phone number real | Not 555-xxxx, not a placeholder tel: href | Placeholder number in HTML |
| Tel: href matches display | The number shown = the number dialed | Display and href differ |
| Email real | Active inbox, correct domain | Placeholder or unmonitored address |
| Address real | Real street address | "123 Main St" placeholder |
| Business hours | Accurate hours listed | No hours or "TBD" |
| NAP matches GBP | Name, address, phone identical to the Google Business Profile | Different phone or suite number |
| Copyright year | Current year | Prior year — a trust signal (looks abandoned), not a ranking factor |

---

## 13. AI Search Visibility

AI Overviews, ChatGPT search, Perplexity, Gemini and Copilot now answer many local
"who should I hire" questions directly. This section checks whether the client can be
found and cited there. It's newer ground than classic SEO — report what you observe and
don't overpromise outcomes.

### 13a. Crawler access (robots.txt)

Read `robots.txt` and check each of these user agents:

| User agent | Owner | What blocking it does |
|------------|-------|----------------------|
| `Googlebot` | Google | Blocks Search *and* AI Overviews — never block |
| `Google-Extended` | Google | Opts out of Gemini model training/grounding; does **not** affect Search or AI Overviews |
| `Bingbot` | Microsoft | Blocks Bing and Copilot; ChatGPT search also leans on Bing's index |
| `OAI-SearchBot` | OpenAI | Blocks the client from appearing in ChatGPT search results |
| `GPTBot` | OpenAI | Opts out of model training only |
| `ChatGPT-User` | OpenAI | Blocks fetches when a user asks ChatGPT to open the page |
| `PerplexityBot` | Perplexity | Blocks Perplexity search results |
| `ClaudeBot` / `Claude-SearchBot` / `Claude-User` | Anthropic | Training / search / user-requested fetches |
| `Applebot-Extended` | Apple | Opts out of Apple model training only |

Also check for a blanket `User-agent: *` / `Disallow: /`, and for Cloudflare or other bot
protection that challenges or blocks these crawlers (common on sites behind Cloudflare's
"block AI bots" toggle).

- **FAIL** — a search/answer bot (`OAI-SearchBot`, `PerplexityBot`, `Bingbot`, `Claude-SearchBot`) is blocked unintentionally.
- **WARN** — training-only bots blocked. That's a legitimate business choice; note it and confirm it's deliberate.
- **PASS** — search/answer bots allowed.

User-agent lists change. Check the vendors' crawler documentation if anything here looks out of date.

### 13b. Citation spot-check

Pick 5–8 queries from Tier 1 and Tier 3 (e.g. "best [service] in [city]",
"[service] company near [neighborhood]"). For each, check what you can reach:

- **Google AI Overview** — does one appear? Is the client cited? Which competitors are?
- **ChatGPT / Perplexity** — if you have browser access, ask the question and record who is
  named and which URLs are cited.

Record results in a small table: query → AI surface → client cited (Y/N) → who was cited.
Note which sources the AI leaned on (Yelp, Reddit, local "best of" lists, BBB, directories)
— those are where the client needs a presence. Answers vary by user, location and day;
present this as a snapshot, not a ranking.

If you can't reach an AI surface from this session, say so and skip it rather than guessing.

### 13c. Entity consistency

AI answers lean heavily on third-party sources and on how consistently the business is
described across the web.

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| NAP consistency | Same name, address, phone on GBP, Yelp, BBB, Apple Business Connect, Bing Places, Facebook, industry directories | Old phone or address on several directories |
| Bing Places & Apple Business Connect | Claimed and complete | Unclaimed — invisible to Copilot / Siri / Apple Maps |
| `sameAs` in schema | Links the site to its profiles | Missing |
| Third-party mentions | Appears in local "best of" lists, local news, Reddit threads, review sites | Exists only on its own site and GBP |

### 13d. Answer-ready content

| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| Direct answers | Service pages state plainly what's offered, where, for whom, and roughly what it costs | Vague marketing copy with no concrete facts |
| Question coverage | FAQ / guide content answers the real pre-hire questions | No FAQ, or generic filler questions |
| Extractable facts | Prices, service areas, hours, years in business, licensing as plain text | Facts buried in images or JS-only widgets |

`llms.txt` is optional and unproven — there's little evidence major AI search products use
it. Mention it at most as a low-priority nice-to-have; never rate its absence as a FAIL.

---

## Quick reference: what the ratings mean in a proposal

- **FAIL** = Actively hurting you right now. Fix before launch or fix immediately.
- **WARN** = A missed opportunity. Not breaking, but leaving ranking and conversion on the table.
- **PASS** = Done correctly. Call it out — clients need to know what's working too.
- **N/A** = Doesn't apply to this site yet.
