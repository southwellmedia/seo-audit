// Brand color extraction — run in the page context of the client's live site
// (any browser tool that can evaluate JavaScript on the page).
// Returns JSON: declared theme colors, CSS custom properties that look like brand tokens,
// and computed colors ranked by how often they appear on prominent elements.
// Pick primary / secondary / accent from the output; don't take it blindly.
(() => {
  const toHex = (str) => {
    if (!str) return null;
    const c = document.createElement('canvas');
    c.width = c.height = 1;
    const ctx = c.getContext('2d', { willReadFrequently: true });
    ctx.fillStyle = '#010203';            // sentinel: unchanged means the value didn't parse
    ctx.fillStyle = str.trim();
    if (ctx.fillStyle === '#010203' && !/^#010203$/i.test(str.trim())) return null;
    ctx.clearRect(0, 0, 1, 1);
    ctx.fillRect(0, 0, 1, 1);
    const [r, g, b, a] = ctx.getImageData(0, 0, 1, 1).data;
    if (a < 128) return null;               // transparent / mostly transparent
    return '#' + [r, g, b].map((v) => v.toString(16).padStart(2, '0')).join('');
  };

  // Near-white, near-black and greys are rarely the brand color — flag, don't drop.
  const isNeutral = (hex) => {
    const n = parseInt(hex.slice(1), 16);
    const r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    return max - min < 18 || max > 245 && min > 235 || max < 25;
  };

  // 1. Declared theme color
  const themeColor = toHex(document.querySelector('meta[name="theme-color"]')?.content);

  // 2. CSS custom properties on :root / body whose names look like brand tokens
  const tokenPattern = /(brand|primary|secondary|accent|highlight|cta|button|link|theme|main)/i;
  const tokens = {};
  for (const el of [document.documentElement, document.body]) {
    const cs = getComputedStyle(el);
    for (const name of cs) {
      if (!name.startsWith('--') || !tokenPattern.test(name)) continue;
      const hex = toHex(cs.getPropertyValue(name));
      if (hex) tokens[name] = hex;
    }
  }

  // 3. Computed colors on prominent elements, counted by frequency and role
  const roles = {
    button_bg: { sel: 'button, .btn, [class*="button"], a[class*="btn"], input[type="submit"]', prop: 'backgroundColor' },
    button_text: { sel: 'button, .btn, [class*="button"], a[class*="btn"]', prop: 'color' },
    link: { sel: 'a', prop: 'color' },
    heading: { sel: 'h1, h2, h3', prop: 'color' },
    header_bg: { sel: 'header, nav, [class*="header"], [class*="navbar"]', prop: 'backgroundColor' },
    footer_bg: { sel: 'footer', prop: 'backgroundColor' },
    section_bg: { sel: 'section, [class*="hero"], [class*="banner"]', prop: 'backgroundColor' },
    body_text: { sel: 'p', prop: 'color' },
    page_bg: { sel: 'body', prop: 'backgroundColor' },
  };
  const byRole = {};
  const overall = {};
  for (const [role, { sel, prop }] of Object.entries(roles)) {
    const counts = {};
    document.querySelectorAll(sel).forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;     // skip hidden elements
      const hex = toHex(getComputedStyle(el)[prop]);
      if (!hex) return;
      counts[hex] = (counts[hex] || 0) + 1;
      overall[hex] = (overall[hex] || 0) + 1;
    });
    byRole[role] = Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 4)
      .map(([hex, count]) => ({ hex, count, neutral: isNeutral(hex) }));
  }

  // 4. Logo — often the most reliable brand reference
  const logo = document.querySelector('header img, [class*="logo"] img, img[alt*="logo" i], img[src*="logo" i]');

  const ranked = Object.entries(overall)
    .sort((a, b) => b[1] - a[1])
    .map(([hex, count]) => ({ hex, count, neutral: isNeutral(hex) }));

  return JSON.stringify({
    theme_color: themeColor,
    css_tokens: tokens,
    by_role: byRole,
    top_non_neutral: ranked.filter((c) => !c.neutral).slice(0, 6),
    top_neutral: ranked.filter((c) => c.neutral).slice(0, 4),
    logo_src: logo?.currentSrc || logo?.src || null,
  }, null, 2);
})();
