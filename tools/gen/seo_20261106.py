"""SEO pass from the 2026-11-06 Search Console export: pages ranking 5-20 with impressions but no clicks.
# NOTE: one-shot script (appends sections); do not re-run on already-updated pages.
Query-matched titles/descriptions/intros, duplicate FAQs removed, extra outputs, tables and internal links."""
import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expand as X
X.BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'content', 'calculators')
U = '2026-11-06'

def path(cid): return f'{X.BASE}/{cid}.mdx'
def load(cid):
    _, fm, body = open(path(cid)).read().split('---', 2); return fm, body
def save(cid, fm, body):
    from fixflow import fix_text
    open(path(cid), 'w').write(fix_text('---' + fm + '---' + body))

def set_fm(cid, **kv):
    fm, body = load(cid)
    for k, v in kv.items():
        if k == 'description': assert 120 <= len(v) <= 160, (cid, len(v))
        if isinstance(v, list): line = f'{k}: [' + ', '.join(v) + ']'
        elif k == 'intro': line = 'intro: ' + json.dumps(v, ensure_ascii=False)
        else: line = f'{k}: ' + X.q(v)
        assert re.search(rf'^{k}: ', fm, re.M), (cid, k)
        fm = re.sub(rf'^{k}: .*$', lambda m: line, fm, count=1, flags=re.M)
    fm = re.sub(r'^updated: .*$', f'updated: {U}', fm, flags=re.M)
    save(cid, fm, body)

def norm(q): return re.sub(r'[^a-z0-9 ]', '', q.lower().replace('football league', 'league')).strip()
def dedupe_faq(cid):
    fm, body = load(cid)
    m = re.search(r'^faq:\n((?:  .*\n|    .*\n)*)', fm, re.M)
    items = re.findall(r'(  - q: (.*)\n    a: .*\n)', m.group(1))
    seen, out = set(), ''
    for block, q in items:
        k = norm(q.strip('"'))
        if k in seen: continue
        seen.add(k); out += block
    fm = fm[:m.start(1)] + out + fm[m.end(1):]
    save(cid, fm, body)

def add_vars(cid, var_lines, eqs):
    fm, body = load(cid)
    i = fm.index('equations:')
    fm = fm[:i] + ''.join(f'  - {v}\n' for v in var_lines) + fm[i:]
    m = re.search(r'^equations:\n((?:  - .*\n)*)', fm, re.M)
    fm = fm[:m.end()] + ''.join(f'  - {e}\n' for e in eqs) + fm[m.end():]
    save(cid, fm, body)

def replace_body(cid, old, new):
    fm, body = load(cid); assert body.count(old) == 1, (cid, old[:40]); save(cid, fm, body.replace(old, new))

def cut_section(cid, heading):
    fm, body = load(cid)
    i = body.index(heading); j = body.find('\n## ', i + 1)
    body = body[:i] + (body[j + 1:] if j != -1 else '')
    save(cid, fm, body.rstrip('\n') + '\n')

# 1 Number to million ------------------------------------------------------
c = 'conversion/number-to-million'
set_fm(c, title='Million in Numbers – Number to Million, Lakh & Crore Converter',
       intro="How do you write 2.5 million in numbers? It is 2,500,000 — or 25 lakh in the Indian system. This number to million converter turns millions, billions, lakhs and crores into digits instantly in both directions, with ready-made tables for common values.",
       keywords=['million in numbers', 'number to million converter', '2.5 million in numbers', 'million to lakh', 'crore to million', 'billion to million', 'indian numbering', 'international numbering'])
dec = [0.75, 1.25, 2.73, 3.2, 4.8, 6.5, 12.5, 23.4, 37.5, 125, 261, 750]
rows = ''.join(f'| {m:g} million | {m*1e6:,.0f} | {m*10:g} lakh{f" ({m/10:g} crore)" if m >= 10 else ""} |\n' for m in dec)
X.expand(c, f'''
## Decimal millions in numbers

To write a decimal million in digits, multiply by 1,000,000 — move the decimal point six places right.

| Million | In numbers | Lakh / crore |
|---|---|---|
{rows}''', faq=[('How do you write 23.4 million in numbers?', '23,400,000 — 23.4 × 1,000,000. In India that is 2.34 crore (2,34,00,000).'),
                ('How do you write 3.2 million in numbers?', '3,200,000, which is 32 lakh.')],
         before='## Crore to million', updated=U)
dedupe_faq(c)

# 2 Slope ------------------------------------------------------------------
c = 'math/slope'
set_fm(c, title='Slope Calculator – Slope, Y-Intercept & Line Equation (2 Points)',
       description='Free slope calculator: find the slope m = (y₂ − y₁) ÷ (x₂ − x₁) from two points, plus the y-intercept, line equation, percent grade, angle and distance.',
       intro="Slope measures how steep a line is — the rise divided by the run between two points. This slope calculator finds the slope from two points and also gives the y-intercept, the equation y = mx + b, the percent grade, the angle and the distance, with every step shown.",
       keywords=['slope calculator', 'slope from two points', 'slope intercept form', 'y-intercept calculator', 'rise over run', 'gradient calculator', 'slope formula', 'percent grade'],
       related=['math/distance-midpoint', 'math/linear-interpolation', 'construction/roof-pitch', 'math/right-triangle-trig', 'math/pythagorean-theorem'])
add_vars(c, ['{ id: b, label: Y-intercept b (line y = mx + b) }', "{ id: gr, label: 'Percent grade (slope × 100)', family: percent, unit: '%' }"],
         ['b = y1 - m * x1', 'gr = m'])
replace_body(c, '- Angle = tan⁻¹(1.333) = **53.13°**', '- Angle = tan⁻¹(1.333) = **53.13°**\n- Y-intercept b = 2 − 1.333 × 1 = **0.667**, so the line is **y = 1.333x + 0.667**\n- Percent grade = 1.333 × 100 = **133.3%**')
cut_section(c, '## Slope as grade and angle')
X.expand(c, '''
## Related calculators

- [Distance and midpoint calculator](/math/distance-midpoint/) — the distance and midpoint between the same two points.
- [Linear interpolation calculator](/math/linear-interpolation/) — find y at any x on the line through two points.
- [Roof pitch calculator](/construction/roof-pitch/) — slope expressed as rise per 12 inches of run.
''', faq=[('How do I write the equation of a line from two points?', 'Find the slope m = (y₂ − y₁) ÷ (x₂ − x₁), then the intercept b = y₁ − m x₁. The line is y = mx + b. For (1, 2) and (4, 6) it is y = 1.333x + 0.667.')],
         before=None, updated=U)
dedupe_faq(c)

# 3 Cost per use -----------------------------------------------------------
c = 'everyday-life/cost-per-use'
set_fm(c, title='Cost Per Use Calculator (Cost Per Wear & Value for Money)',
       description='Work out the true cost per use or cost per wear of anything — clothes, shoes, gadgets, gym memberships and subscriptions — including upkeep costs.',
       intro="Cost per use divides everything you pay for an item by how often you use it, so a long-lasting purchase can turn out cheaper than a bargain. This cost per use calculator includes running and upkeep costs and works as a cost per wear calculator for clothes and shoes too.",
       keywords=['cost per use calculator', 'cost per wear calculator', 'cost per use', 'value for money calculator', 'is it worth it calculator', 'gym cost per visit'],
       related=['everyday-life/unit-price', 'everyday-life/habit-cost', 'everyday-life/electricity-cost', 'finance/roi'])
items = [('Winter coat', 300, 0, 150), ('Fast-fashion jacket', 40, 0, 10), ('Leather boots', 180, 40, 300), ('Running shoes', 120, 0, 120), ('Laptop (4 years)', 1000, 0, 1000), ('Coffee machine', 250, 60, 900), ('Gym membership (year)', 480, 0, 100)]
rows = ''.join(f'| {n} | {p:,} | {r:,} | {u:,} | {(p+r)/u:.2f} |\n' for n, p, r, u in items)
X.expand(c, f'''
## Cost per use examples

| Item | Price | Upkeep | Uses | Cost per use |
|---|---|---|---|---|
{rows}
The coat costs {300/40:.1f} times as much as the jacket but works out at {300/150:.2f} per wear against {40/10:.2f}.
''', before='## Gym membership', updated=U)
dedupe_faq(c)

# 4 Primer Tm --------------------------------------------------------------
c = 'biology/primer-tm'
set_fm(c, title='Primer Tm Calculator – DNA Melting Temperature for PCR',
       description='Free primer Tm calculator: DNA primer melting temperature by the Wallace rule and the basic GC formula, GC content and a suggested PCR annealing temperature.',
       intro="A primer's melting temperature (Tm) is where half of it is bound to its target DNA, and the PCR annealing temperature is set from it. This primer Tm calculator gives two estimates — the Wallace rule for short primers and the basic GC formula for longer oligos — plus GC content and a starting annealing temperature.",
       keywords=['primer tm calculator', 'tm calculator', 'melting temperature calculator', 'primer melting temperature', 'wallace rule', 'annealing temperature calculator', 'pcr primer tm', 'oligo tm'],
       related=['biology/gc-content', 'biology/pcr-amplification', 'biology/dna-concentration', 'biology/dna-copy-number'])
add_vars(c, ['{ id: tmb, label: Melting temperature (basic GC formula), suffix: °C, decimals: 1 }'],
         ['tmb = 64.9 + 41 * (g + c - 16.4) / (a + t + g + c)'])
tmb = 64.9 + 41 * (10 - 16.4) / 20
replace_body(c, '- GC = **50%**', f'- GC = **50%**\n- Basic GC formula: 64.9 + 41 × (10 − 16.4) ÷ 20 = **{tmb:.1f} °C**\n\nThe two estimates differ by about {60-tmb:.0f} °C — the Wallace rule runs high for 20-mers, which is why a gradient PCR is the safest way to set the annealing temperature.')
replace_body(c, '<p class="formula">Tm = 2(A + T) + 4(G + C)</p>', '<p class="formula">Tm = 2(A + T) + 4(G + C) &nbsp;·&nbsp; Tm = 64.9 + 41 × (G + C − 16.4) ÷ N</p>')
replace_body(c, '| Wallace rule (this calculator) |', '| Wallace rule (this calculator) |')
replace_body(c, '| Basic GC formula: 64.9 + 41(GC − 16.4)/N | Longer oligos |', '| Basic GC formula: 64.9 + 41(GC − 16.4)/N (this calculator) | Longer oligos |')
replace_body(c, 'This calculator uses the Wallace rule, which gives', 'This calculator shows the Wallace rule and the basic GC formula. The Wallace rule gives')
dedupe_faq(c)

# 5 Data storage -----------------------------------------------------------
c = 'other/data-storage-converter'
set_fm(c, title='Data Storage Converter – Bytes, KB, MB, GB, TB (Decimal & Binary)',
       intro="Data storage is measured in kilobytes, megabytes, gigabytes and terabytes, in both decimal (1,000) and binary (1,024) steps — which is why a 1 TB drive shows as 931 GB. This data storage converter (GB calculator) converts between bytes, MB, GB, TB, MiB and GiB in both systems at once.",
       keywords=['data storage converter', 'data storage calculator', 'gb calculator', 'mb to gb', 'gb to tb', 'bytes converter', 'gib vs gb', 'file size converter'],
       related=['other/download-time', 'other/video-file-size', 'other/print-size-dpi'])
units = [('1 KB', 1e3), ('1 MB', 1e6), ('1 GB', 1e9), ('500 GB', 5e11), ('1 TB', 1e12), ('2 TB', 2e12), ('4 TB', 4e12)]
rows = ''.join(f'| {n} | {b:,.0f} | {b/1024**2:,.2f} MiB | {b/1024**3:,.3f} GiB |\n' for n, b in units)
X.expand(c, f'''
## Decimal to binary sizes

| Decimal size | Bytes | In MiB | In GiB |
|---|---|---|---|
{rows}''', before='## Bits vs bytes', updated=U)
dedupe_faq(c)

# 6 Football points --------------------------------------------------------
c = 'sports/football-points'
set_fm(c, title='Football Points Calculator – League Points, PPG & Goal Difference',
       description='Free football points calculator: work out league table points (3 for a win, 1 for a draw), points per game and goal difference from wins, draws and losses.',
       intro="League tables award 3 points for a win, 1 for a draw and none for a loss. This football points calculator totals a team's points from its results and adds points per game and goal difference — handy for checking the table, predicting a finish or comparing teams with games in hand.",
       keywords=['football points calculator', 'league points calculator', 'football table calculator', 'soccer points calculator', 'points per game', 'goal difference', '3 points for a win'],
       related=['sports/win-percentage'])
proj = ''.join(f'| {p:.2f} | {p*38:.0f} | {p*34:.0f} | {p*46:.0f} |\n' for p in (1.0, 1.2, 1.5, 1.8, 2.0, 2.3, 2.5))
X.expand(c, f'''
## Projected season points from points per game

| Points per game | 38 games | 34 games | 46 games |
|---|---|---|---|
{proj}''', before='## Tie-breakers', updated=U)
dedupe_faq(c)
print('done')
