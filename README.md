# CalcVerse — interactive calculator site (Astro)

Static site: every calculator is ONE `.mdx` file. The shared engine renders the
widget, solves for any field, shows steps, draws a chart, syncs the URL and
generates SEO markup. Built for thousands of pages.

## Run

```bash
npm install
npm run dev        # http://localhost:4321
npm run build      # static site in dist/  → upload to Cloudflare Pages / Netlify / any host
npm test           # solver unit tests
```

Before launch edit `src/site.config.ts` (name, url, locale) and `site` in `astro.config.mjs`.

## Add a calculator (the only thing you repeat 2,000+ times)

Create `src/content/calculators/<category>/<slug>.mdx` → URL `/<category>/<slug>`.

```yaml
---
title: Ohm's Law Calculator
description: ≤170 chars, shown in Google
category: physics            # must exist in src/data/categories.ts
keywords: [ohm, voltage]     # used by site search
updated: 2026-10-27
featured: false              # true = shown on home page
variables:
  - { id: V, label: Voltage, family: voltage, unit: V, default: 24, min: 0 }
  - { id: I, label: Current, family: current, unit: mA, min: 0 }
  - { id: R, label: Resistance, family: resistance, default: 250, min: 0 }
equations:
  - V = I * R                # written in BASE units (first unit of each family)
chart: { x: R, y: I, from: 50, to: 1000 }   # optional
faq:
  - { q: Question?, a: Answer. }
related: [conversion/number-to-million]     # build fails if a link is broken
---

## Article content in Markdown/MDX…
```

### Variable options

| Key | Meaning |
|---|---|
| `family` | unit family from `src/lib/units.ts` (length, mass, time, percent, temperature, pressure, voltage, current, resistance, power, currency, none) |
| `unit` | default display unit id |
| `default` | starting value (display unit). Fields with defaults are the initial inputs |
| `min` / `max` | bounds in **base** units — helps the solver pick the right root |
| `prefix` / `suffix` | e.g. `₹`, `kg/m²` |
| `decimals` | round displayed result |
| `options` | turns field into a dropdown (`{label, value}`) |
| `bands` | coloured category bar (e.g. BMI ranges) |
| `help` | tooltip text |

Special families: `date` (date picker; `default` = days from today, e.g. 0 = today) and `clock` (time picker; `default` = hours, e.g. 17.5 = 17:30).

Top-level `dataset: { label, default }` adds a list box (paste numbers). Equations can then use
`data_n, data_sum, data_mean, data_median, data_mode, data_modecount, data_min, data_max, data_range, data_q1, data_q3, data_sd, data_sdp, data_var, data_varp, data_gmean, data_sumsq`.

Top-level `freedom` overrides how many inputs are needed (default = variables − equations).

### Equations
`+ - * / ^`, parentheses, `mod fact gamma nCr nPr normcdf erf yearsBetween monthsBetween workdays weekday sqrt cbrt abs exp ln log log10 log2 sin cos tan asin acos atan sinh cosh tanh min max pow floor ceil round`, constants `pi e g0` (so never name a variable `e`, `pi` or `g0` — the build rejects it).
Labels containing commas or colons must be quoted in YAML: `label: "Sand, dry"`.
Write each relation once — the solver rearranges it (numerically when needed),
and solves coupled equations (e.g. Ohm's law from P and R).

### Add a unit family
Add an entry in `src/lib/units.ts`. First unit = base (factor 1). Offsets are supported (°C/°F).

## Authors
Edit `src/data/authors.ts` (name, bio, photo in `public/authors/`, LinkedIn). Calculators use `author: <id>` (default: santaji-gadepatil) and optional `reviewer: <id>`.

## Structure

```
src/
  content/calculators/<cat>/<slug>.mdx   ← content (one file per calculator)
  content.config.ts                      ← frontmatter schema (validated at build)
  data/categories.ts                     ← nav categories, icons, colours
  lib/expr.ts      safe expression parser
  lib/solver.ts    solve-for-any-field engine
  lib/units.ts     unit families
  components/Calculator.tsx, Chart.tsx   ← interactive widget (Preact)
  pages/           home, category, calculator, /embed/…, search.json, robots.txt
```

## Built-in features
Solve any field · per-field units · clear-to-calculate · step-by-step working ·
interactive chart (switch axes, range, hover) · shareable URL state · copy result ·
embed iframe code (backlinks) · instant search · dark mode · breadcrumbs ·
WebApplication / FAQPage / BreadcrumbList schema · sitemap · ad slot placeholder.
