"""SEO improvements from the first Search Console export (2026-11-03): match real queries with tables, FAQs and titles."""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expand as X
X.BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'content', 'calculators')
U = '2026-11-03'

def set_fm(cid, **kv):
    p = f'{X.BASE}/{cid}.mdx'; s = open(p).read()
    for k, v in kv.items():
        s = re.sub(rf'^{k}: .*$', f'{k}: ' + X.q(v), s, count=1, flags=re.M)
    open(p, 'w').write(s)

def ind(n):  # Indian grouping
    s = str(int(round(n))); last = s[-3:]; rest = s[:-3]
    parts = []
    while len(rest) > 2: parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest: parts.insert(0, rest)
    return ','.join(parts + [last]) if parts else last
def g(x, d=2): return f'{x:,.{d}f}'.rstrip('0').rstrip('.') if d else f'{x:,.0f}'

# 1 Number to million ------------------------------------------------------
set_fm('conversion/number-to-million', title='Number to Million Converter (Million, Lakh & Crore in Numbers)',
       description='Convert numbers to millions, billions, lakhs and crores — e.g. 2.5 million in numbers is 2,500,000 (25 lakh). Instant two-way converter with tables.')
rows = ''.join(f'| {m:g} million | {g(m*1e6,0)} | {ind(m*1e6)} | {m*10:g} lakh{f" ({m/10:g} crore)" if m>=10 else ""} |\n' for m in [0.1, 0.25, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 7.5, 10, 15, 20, 25, 50, 100, 250, 500, 1000])
crows = ''.join(f'| {c:g} crore | {c*10:g} million | {g(c*1e7,0)} |\n' for c in [0.5, 1, 1.5, 2, 2.5, 3, 4.5, 5, 7.5, 10, 25, 50, 100, 1000])
X.expand('conversion/number-to-million', f'''
## Millions in numbers

| Million | In numbers (international) | Indian format | Lakh / crore |
|---|---|---|---|
{rows}
## Crore to million

| Crore | Million | In numbers |
|---|---|---|
{crows}
**Rule of thumb:** 1 million = 10 lakh, and 1 crore = 10 million.
''', faq=[('How do you write 2.5 million in numbers?', '2,500,000 — two million five hundred thousand. In the Indian system that is 25,00,000 or 25 lakh.'),
          ('How many million is 4.5 crore?', '45 million (45,000,000), because 1 crore equals 10 million.'),
          ('How many zeros are in a million?', 'Six: 1,000,000. A billion has nine zeros and a crore has seven.')],
         before='## Short scale vs long scale', updated=U)

# 2 kW to hp ---------------------------------------------------------------
set_fm('conversion/kw-to-hp', title='kW to HP Converter – Kilowatts to Horsepower (with Chart)',
       description='Convert kW to hp and hp to kW for motors, engines and pumps — 1 kW = 1.341 hp. Includes a chart from 0.37 kW to 500 kW in mechanical hp and metric PS.')
kw = [0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45, 47, 55, 75, 88, 90, 100, 110, 120, 132, 150, 160, 200, 250, 300, 315, 400, 440, 500]
rows = ''.join(f'| {k:g} kW | {k/0.74569987158:.1f} hp | {k/0.73549875:.1f} PS |\n' for k in kw)
X.expand('conversion/kw-to-hp', f'''
## kW to hp for common ratings

| Kilowatts | Horsepower (mechanical) | Metric hp (PS / pk / CV) |
|---|---|---|
{rows}''', faq=[('What is 120 kW in hp?', f'{120/0.74569987158:.1f} mechanical horsepower, or {120/0.73549875:.1f} PS (metric hp).'),
                 ('What is 47 kW in hp?', f'{47/0.74569987158:.1f} hp (mechanical) or {47/0.73549875:.1f} PS.'),
                 ('Is pk the same as PS?', 'Yes. PS (German), pk (Dutch) and CV (French/Italian) all mean metric horsepower, 735.5 W — slightly less than mechanical hp (745.7 W).')],
         before='## Definitions', updated=U)

# 3 km to miles ------------------------------------------------------------
set_fm('conversion/km-to-miles', title='KM to Miles Converter (Kilometers to Miles + Chart)',
       description='Convert km to miles and miles to km — 1 km = 0.621371 miles. Charts for race distances, road trips and odometer readings from 1 km to 100,000 km.')
km = [1, 2, 3, 5, 8, 10, 15, 20, 21.0975, 25, 30, 40, 42.195, 50, 60, 80, 100, 120, 150, 160, 200, 250, 300, 500, 1000, 1609.344, 2000, 5000, 10000, 20000, 25000, 30000, 40000, 50000, 80000, 100000]
rows = ''.join(f'| {g(k,4)} km | {g(k*0.621371192,2)} mi |\n' for k in km)
X.expand('conversion/km-to-miles', f'''
## Kilometres to miles: from runs to odometer readings

| Kilometres | Miles |
|---|---|
{rows}
Car odometer readings are often written as "30k" or "80k" — 30,000 km is about **18,641 miles** and 80,000 km about **49,710 miles**.
''', faq=[('How far is 80k in miles?', '80 km is 49.71 miles. If "80k" means 80,000 km on an odometer, that is 49,710 miles.'),
          ('How many miles is 1,609.344 km?', 'Exactly 1,000 miles — one mile is defined as 1.609344 km.'),
          ('How many miles is 25,000 km?', '15,534 miles.')],
         before='## Speed limits', updated=U)

# 4 lbs to kg --------------------------------------------------------------
set_fm('conversion/lbs-to-kg', title='Lbs to Kg Converter (Pounds to Kilograms + Chart)',
       description='Convert lbs to kg and kg to lbs — 1 lb = 0.4536 kg. Charts from 1 to 400 lb for body weight, luggage and gym plates, plus a quick mental trick.')
rows = ''.join(f'| {l} lb | {l*0.45359237:.1f} kg | {l+5} lb | {(l+5)*0.45359237:.1f} kg |\n' for l in range(100, 410, 10))
X.expand('conversion/lbs-to-kg', f'''
## Pounds to kilograms: 100–415 lb

| Pounds | Kilograms | Pounds | Kilograms |
|---|---|---|---|
{rows}''', faq=[('How many kg is 150 lbs?', f'{150*0.45359237:.1f} kg.'), ('How many kg is 200 lbs?', f'{200*0.45359237:.1f} kg.')],
         before='## Definitions', updated=U)

# 5 Centrifuge RCF ↔ RPM ---------------------------------------------------
set_fm('biology/centrifuge-rcf', title='RCF to RPM Calculator (g-Force ↔ RPM Centrifuge Converter)',
       description='Convert RCF (× g) to RPM and RPM to g-force for any centrifuge rotor radius — e.g. 1000 × g at 10 cm ≈ 2,990 rpm. Includes ready tables for common g values.')
radii = [5, 7, 8.5, 10, 15]
gs = [100, 300, 500, 1000, 1500, 2000, 3000, 5000, 10000, 12000, 15000, 20000]
rpm = lambda G, r: math.sqrt(G / (1.118e-5 * r))
rows = ''.join(f'| {G:,} × g | ' + ' | '.join(f'{rpm(G,r):,.0f}' for r in radii) + ' |\n' for G in gs)
X.expand('biology/centrifuge-rcf', f'''
## RCF to RPM table (by rotor radius)

| RCF | r = 5 cm | r = 7 cm | r = 8.5 cm | r = 10 cm | r = 15 cm |
|---|---|---|---|---|---|
{rows}
Values are rpm, from rpm = √(RCF ÷ (1.118 × 10⁻⁵ × r)). Use your rotor's maximum radius from the manual for the closest match to protocol g-forces.

## RCF vs RPM: what is the difference?

**RPM** is how fast the rotor turns. **RCF** (relative centrifugal force, written × g) is the force the sample actually feels, as a multiple of Earth's gravity. Two centrifuges at the same rpm give different g-forces if their rotors have different radii — which is why protocols specify × g.
''', faq=[('Is RCF the same as g?', 'RCF is expressed in multiples of g. "1,000 × g" and "1,000 g" mean a relative centrifugal force 1,000 times Earth\'s gravity.'),
          ('How do I convert 1000 × g to rpm?', f'It depends on the rotor radius: about {rpm(1000,10):,.0f} rpm at 10 cm, {rpm(1000,8.5):,.0f} rpm at 8.5 cm and {rpm(1000,15):,.0f} rpm at 15 cm.'),
          ('How do I convert rpm to g?', 'RCF = 1.118 × 10⁻⁵ × radius (cm) × rpm². Enter rpm and radius in the calculator to get × g.')],
         before='## Why protocols use × g', updated=U)

# 6 Primer Tm -------------------------------------------------------------
set_fm('biology/primer-tm', title='Primer Tm Calculator – Free Primer Melting Temperature (Wallace Rule)',
       description='Free primer Tm calculator: estimate DNA primer melting temperature from A, T, G and C counts, GC content and a suggested annealing temperature for PCR.')
X.expand('biology/primer-tm', '''
## How accurate is this Tm calculator?

This calculator uses the Wallace rule, which gives a quick, reliable estimate for primers of about 14–25 bases at standard PCR salt conditions. Commercial and polymerase-specific Tm calculators usually use the **nearest-neighbor** method with corrections for salt, Mg²⁺ and primer concentration, so their results can differ by 2–5 °C.

For the best results:

- Use the **same calculator for both primers** so they are matched to each other.
- Aim for both primers within **2–5 °C** of each other.
- Confirm the annealing temperature with a **gradient PCR** — the optimum is often 3–5 °C below the lower Tm.
- If you use a high-fidelity polymerase, follow its supplier's Tm method, as some recommend annealing above the calculated Tm.
''', faq=[('Which primer Tm calculator is most accurate?', 'Nearest-neighbor calculators with salt and Mg²⁺ corrections are the most accurate. The Wallace rule used here is a fast estimate that is usually within a few degrees for 14–25-base primers.'),
          ('Why do different Tm calculators give different values?', 'They use different formulas (Wallace, GC%, nearest-neighbor) and different assumptions about salt, magnesium and primer concentrations.'),
          ('What is a PCR gradient?', 'A run where each column of the block uses a different annealing temperature, so you can find the best temperature for a new primer pair in one experiment.')],
         before='## Primer problems to avoid', updated=U)

# 7 Speed converter: kph to mph -------------------------------------------
set_fm('conversion/speed-converter', title='Speed Converter – km/h to mph, m/s & Knots (with Chart)',
       description='Convert speed between km/h, mph, m/s, ft/s and knots — 1 km/h = 0.6214 mph. Includes a km/h to mph chart from 10 to 400 km/h for driving and sport.')
rows = ''.join(f'| {k} km/h | {k*0.621371192:.1f} mph | {k/3.6:.1f} m/s | {k*0.539956803:.1f} kn |\n' for k in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 180, 200, 250, 300, 322, 350, 400])
X.expand('conversion/speed-converter', f'''
## km/h to mph, m/s and knots

| km/h | mph | m/s | knots |
|---|---|---|---|
{rows}''', faq=[('What is 322 km/h in mph?', '200.1 mph — the kind of top speed reached by supercars and MotoGP bikes.'),
                 ('How do I convert km/h to mph quickly?', 'Multiply by 0.62, or multiply by 5 and divide by 8: 80 km/h ≈ 50 mph.')],
         before='## Speed unit definitions', updated=U)

# 8 Slope -----------------------------------------------------------------
set_fm('math/slope', title='Slope Calculator – Find the Slope of a Line from Two Points',
       description='Free slope calculator: find the slope m = (y₂ − y₁) ÷ (x₂ − x₁) of a line through two points, plus distance, angle and the line equation, step by step.')
print('done')
