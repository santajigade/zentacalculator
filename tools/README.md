# Daily calculator batch — playbook

Goal: publish ~20 accurate, SEO-ready calculators per day (focus: engineering, electrical, electronics, physics, chemistry, math, statistics). Backlog: `tools/ROADMAP.md`.

## 1. Pick the batch
- Take the next ~20 unchecked items from `tools/ROADMAP.md`, mixing 2–3 categories.
- Skip anything that already exists (`ls src/content/calculators/*/`) or duplicates another page.
- Find matching instrumentationblog.in articles: `grep -i <keyword> tools/gen/ib_slugs.txt`.

## 2. Write the generator
Create `tools/gen/batch<DATE>.py` (copy the pattern of `batchE1.py` / `batchE2.py`):
- `page(category, slug, frontmatter, body)` from `page.py`; `intro(text)` from `ib.py` expands `[label](ib:slug)` to instrumentationblog.in URLs.
- Frontmatter: `title` (keyword first, ≤ 60 chars ideally), `description` (120–160 chars), `category`, `intro` (2–3 sentences, contains the exact keyword phrase "X calculator", 1–3 in-text instrumentationblog.in links where relevant), `keywords`, `updated`, `variables`, `equations`, `faq` (3–4), `related` (existing ids only).
- Body headings: `## How to use the X calculator`, `## X formula`, examples, reference tables computed in Python (never typed by hand), practical notes.
- Variables are stored in **SI base units** (family units in `src/lib/units.ts`); percent family stores fractions; reserved ids: `pi`, `e`, `g0`, `data_*`.
- Do **not** set `featured: true` on new calculators (the homepage picks its own popular lists).
- Select option values must be unique (add 0.000001 to duplicates). YAML answers must not start with `%`, `*`, `&`, `!`, `|`, `>`.

### Linking rules for instrumentationblog.in (SEO)
- Link **only when an article genuinely matches the calculator** — never force a link onto every page. Pages with no relevant article get none.
- **1–3 contextual, in-text links** per page (intro or body), with **descriptive, varied anchor text** (the article topic), never the same anchor or "instrumentationblog" brand anchor everywhere.
- **No sitewide links** (header, footer, sidebar, template blocks) to instrumentationblog.in.
- Mix in other authoritative references (standards bodies, manufacturer data, Wikipedia) where useful, so outbound links are not all to one domain.
- Never invent a slug — only use slugs in `tools/gen/ib_slugs.txt`.

## 3. Verify
```
python3 tools/gen/batch<DATE>.py
python3 tools/gen/validate.py            # must print bad 0 / bad2 0
npm run build && python3 tools/gen/linkcheck.py   # must print 0
setsid npx astro preview --port 4399 &   # (never pkill by pattern)
node tools/test/t8.cjs <ids>   # 0 errors, 0 warnings
node tools/test/t6.cjs <ids>   # 0 overflow at 360 px
node tools/test/t9.cjs <ids>   # read every default result and check it by hand against the worked example
```
Fix any example text that disagrees with the calculator.

## 4. Publish
- Add the new ids to the right `groups` in `src/data/catseo.ts` (create a new group/subcategory if needed).
- Tick the items in `tools/ROADMAP.md`.
- `bash deploy.sh` (publishes `dist/` to the `site` branch → Hostinger).
- Commit to `main` and `git push origin main`.
