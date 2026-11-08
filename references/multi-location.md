# Multi-Location B2C Audit Reference

For consumer-facing businesses with **several physical locations**, each with its own
address and (ideally) its own Google Business Profile. Examples: dental and medical
groups, veterinary clinics, gyms, salons, auto service chains, restaurant groups,
franchise territories, storage facilities.

The difference from `b2c-local.md`: each location competes in its own map pack. The site's
job is to give every location a strong, distinct page, and the GBP work multiplies by the
number of locations.

Read `b2c-local.md` too — its GBP, trust-signal and content guidance all applies per location.

---

## Business model characteristics

- **Customer**: Consumers choosing the nearest good option
- **Decision driver**: Proximity + reviews + availability (hours, booking)
- **Primary conversion**: Call, directions, or online booking for a specific location
- **Ranking reality**: Each location ranks in the map pack around its own address. A
  strong location in one suburb does little for a weak one across town.

---

## What to audit (in addition to the standard checklist)

### Location pages
| Check | Pass Condition | Common Fail |
|-------|---------------|-------------|
| One page per location | `/locations/[city-or-area]/` for every address | One "Locations" page with a list or map |
| Unique content | Each page has its own staff, photos, parking/directions notes, services offered there, local reviews | Same template text with the city name swapped |
| Location NAP | Exact name, address, phone matching that location's GBP | Corporate phone on every page |
| Location schema | LocalBusiness per page with that location's address, geo and hours, linked to the parent Organization | One schema block for the whole brand |
| Store locator indexable | Locator links to real location pages in HTML | JS-only locator with no crawlable links |
| Hours & holiday hours | Per-location, current | Generic brand hours |

### Google Business Profiles (per location)
For each location (or a representative sample if there are many — say which):
- Profile claimed and verified; primary category correct and consistent across locations
- Website link points to **that location's page**, not the homepage
- Review count, average rating, and how recently reviews came in
- Owner responses to reviews
- Photos: real and recent, from that location
- Duplicate or stale profiles (closed or moved locations still live)

Build a location scorecard: one row per location, columns for reviews, rating, review
recency, page quality, GBP completeness. The weakest locations are usually the fastest wins.

### Brand-level
- Duplicate content across location pages (check 2–3 pages side by side)
- Internal linking: homepage → locations hub → each location → its services
- Closed locations: page 301s to the nearest open location, GBP marked permanently closed

---

## Keyword strategy

See `keywords.md`. Multi-location notes:

- **Tier 1** — brand-level category terms for the homepage and service pages
- **Tier 2** — `[service] [location city/area]` for each location; this is the core of the strategy
- **Tier 3** — `[service] near [landmark / neighborhood near a location]`, `[service] open now [city]`,
  `[service] [location] accepting new patients` (or the category's equivalent)
- **Tier 4** — brand-level educational content shared across locations

---

## Strategic opportunities to check

1. **Templated location pages across competitors** — genuinely local pages win
2. **Weak-location turnaround** — one or two locations with few or old reviews dragging
   down an otherwise strong brand; a focused review-generation push is a quick, measurable win
3. **GBP website links** — competitors (or the client) pointing every GBP to the homepage;
   pointing each to its location page is a fast fix
4. **Per-location booking** — nobody lets you book a specific location online
5. **Local proof** — staff bios, local community involvement, and location photos that
   templated competitor pages can't match
