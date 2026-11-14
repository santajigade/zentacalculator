"""Improve pass (2026-11-14) for thin pages from the first batch (2026-10-27):
physics/momentum, physics/pressure, statistics/permutations.
Keyword-first titles, 120-160 char descriptions, intros with the "<topic> calculator" phrase,
worked examples and reference tables computed here, practical notes, re-checked FAQs and related links.
Fixes: momentum page claimed a car at 0.5 km/h has "similar" momentum to a cricket ball (it has 27x more);
permutations page printed the full 68-digit 52! in a table. Existing instrumentationblog.in links on the
pressure page are kept; none are added. Slugs, categories and existing variable ids are unchanged
(asserted); a few output variables are added. Re-running regenerates the same files."""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from page import page, BASE
U = '2026-11-14'
DONE = []

def ids_of(cid):
    fm = open(os.path.join(BASE, cid + '.mdx')).read().split('---')[1]
    d = yaml.safe_load(fm); return [v['id'] for v in d['variables']], d['category'], d.get('featured')

def W(cid, fm, body):
    cat, slug = cid.split('/')
    old_ids, old_cat, old_feat = ids_of(cid)
    assert not old_feat, cid
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (cid, len(d))
    assert 'featured' not in fm
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    page(cat, slug, fm, body)
    new_ids, new_cat, _ = ids_of(cid)
    assert new_cat == old_cat == cat, cid
    assert all(i in new_ids for i in old_ids), (cid, old_ids, new_ids)
    DONE.append(cid)

# ---------------------------------------------------------------- Momentum
mm, mv = 0.16, 140.0
mvs = mv / 3.6; mp = mm * mvs; mke = 0.5 * mm * mvs ** 2
car_v = mp / 1200 * 3.6
OBJ = [('Tennis serve', 0.058, 200), ('Cricket ball (fast bowler)', 0.16, 140), ('Football kick', 0.43, 100),
       ('Sprinter', 75, 36), ('Cyclist with bike', 85, 25), ('Car', 1200, 50), ('Car', 1200, 100),
       ('Loaded truck', 30000, 60), ('Bullet (9 mm)', 0.008, 1300)]
mo_rows = ''.join(f"| {nm} | {m:,g} kg | {v:,g} km/h | {m*v/3.6:,.1f} kg·m/s | {0.5*m*(v/3.6)**2:,.0f} J |\n" for nm, m, v in OBJ)
# perfectly inelastic collisions: 1,000 kg car at 20 m/s hits a stationary car of mass m2
ci_rows = ''
for m2 in (500, 1000, 1500, 2000, 5000):
    vf = 1000 * 20 / (1000 + m2); ke0 = 0.5 * 1000 * 20 ** 2; ke1 = 0.5 * (1000 + m2) * vf ** 2
    ci_rows += f"| {m2:,} kg | {vf:.2f} m/s | {ke0/1000:.0f} kJ | {ke1/1000:.1f} kJ | {(1-ke1/ke0)*100:.0f}% |\n"

W('physics/momentum', f'''
title: Momentum Calculator (p = mv, Linear Momentum)
description: Calculate linear momentum from mass and velocity (p = mv), or find the mass or velocity from a momentum, with kinetic energy and collision examples.
category: physics
intro: "Momentum is mass times velocity — a measure of how hard a moving object is to stop, and a quantity that is conserved in every collision. This momentum calculator finds the linear momentum p = mv from any mass and speed, or the speed or mass from a known momentum, and also gives the kinetic energy so you can compare the two."
keywords: [momentum calculator, p = mv, linear momentum calculator, momentum formula, calculate momentum, kg m/s, conservation of momentum, momentum and kinetic energy]
updated: {U}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: {mm:g}, min: 0 }}
  - {{ id: v, label: Velocity, family: velocity, unit: kmh, imperialUnit: mph, default: {mv:g} }}
  - {{ id: p, label: Momentum, suffix: kg·m/s }}
  - {{ id: ke, label: Kinetic energy (½mv²), family: energy, unit: J, imperialUnit: BTU, min: 0 }}
equations:
  - p = m * v
  - ke = 0.5 * m * v^2
faq:
  - q: How do you calculate momentum?
    a: Multiply the mass in kg by the velocity in m/s, p = m × v. Convert km/h to m/s by dividing by 3.6 first. A 160 g cricket ball at 140 km/h (38.89 m/s) has p = 0.16 × 38.89 = {mp:.2f} kg·m/s.
  - q: What are the units of momentum?
    a: Kilogram-metres per second (kg·m/s), which is the same as newton-seconds (N·s), because a force of 1 N acting for 1 s changes momentum by 1 kg·m/s. In US customary units momentum is usually given in slug·ft/s or lbf·s.
  - q: What is conservation of momentum?
    a: When no outside force acts, the total momentum of a system stays the same — the total before a collision or explosion equals the total after. Momentum is a vector, so velocities in opposite directions have opposite signs.
  - q: What is the difference between momentum and kinetic energy?
    a: Momentum (mv) is a vector and is conserved in every collision; kinetic energy (½mv²) is a scalar and is only conserved in elastic collisions. Doubling the speed doubles the momentum but quadruples the kinetic energy, which is why speed matters so much in crashes.
related: [physics/impulse, physics/kinetic-energy, physics/elastic-collision, physics/force, physics/acceleration, physics/speed-distance-time]
''', f'''
## How to use the momentum calculator

Enter the **mass** and the **velocity** to get the momentum in kg·m/s and the kinetic energy. To find a speed, clear the velocity and enter the momentum; to find a mass, clear the mass. Both mass and velocity have unit selectors (kg, g, lb; km/h, m/s, mph and more), and the calculation is always done in SI units. Enter a negative velocity for motion in the opposite direction.

## Momentum formula

<p class="formula">p = m × v &nbsp;·&nbsp; KE = ½ m v² = p² ÷ 2m</p>

p is in kg·m/s when m is in kg and v in m/s. The change in momentum equals the impulse, Δp = F × Δt.

## Worked example

A {mm*1000:g} g cricket ball bowled at {mv:g} km/h:

- Speed in m/s = {mv:g} ÷ 3.6 = {mvs:.2f} m/s
- Momentum p = {mm:g} × {mvs:.2f} = **{mp:.2f} kg·m/s**
- Kinetic energy = ½ × {mm:g} × {mvs:.2f}² = **{mke:.1f} J**

A 1,200 kg car has the same momentum when crawling at only {car_v:.3f} km/h ({car_v/3.6*100:.2f} cm/s) — yet at that speed its kinetic energy is just {0.5*1200*(car_v/3.6)**2:.3f} J, because the energy depends on v².

## Momentum of everyday objects

| Object | Mass | Speed | Momentum | Kinetic energy |
|---|---|---|---|---|
{mo_rows}
## Conservation of momentum in a collision

In a collision with no outside forces, the total momentum before equals the total after:

<p class="formula">m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂</p>

If the objects stick together (a perfectly inelastic collision) the common final speed is v = (m₁u₁ + m₂u₂) ÷ (m₁ + m₂). A 1,000 kg car at 20 m/s hitting a stationary car:

| Stationary car | Final speed | KE before | KE after | KE lost |
|---|---|---|---|---|
{ci_rows}
Momentum is conserved in every case, but most of the kinetic energy turns into deformation, heat and sound. For bouncing (elastic) collisions use the [elastic collision calculator](/physics/elastic-collision/).

## Practical notes

- **Direction matters:** momentum is a vector. In a head-on collision, give one velocity a negative sign before adding momenta.
- **Stopping force:** the average force needed to stop an object is its momentum divided by the stopping time, F = p ÷ t — see the [impulse calculator](/physics/impulse/). Air bags, crumple zones and catching a ball with "soft hands" all work by making t longer.
- **Recoil:** when a gun fires or a rocket burns, the forward momentum of the bullet or exhaust equals the backward momentum of the gun or rocket. A heavier gun recoils more slowly for the same bullet.
- At speeds approaching the speed of light, use relativistic momentum p = γmv instead.
''')

# ---------------------------------------------------------------- Pressure
pF, pA = 700.0, 400.0
pP = pF / (pA / 1e4)
SIT = [('Person standing (two feet)', 700, 400), ('Person on one foot', 700, 200), ('Person on one stiletto heel', 700, 1),
       ('Person on snowshoes', 700, 3000), ('Elephant (four feet)', 50000, 4000), ('Car tyre contact patch (each)', 3000, 150),
       ('Drawing pin point', 20, 0.0001)]
si_rows = ''.join(f"| {nm} | {F:,g} N | {A:,g} cm² | {F/(A/1e4)/1000:,.1f} kPa | {F/(A/1e4)/6894.757:,.2f} psi |\n" for nm, F, A in SIT)
UNITS = [('1 Pa', 1), ('1 kPa', 1e3), ('1 bar', 1e5), ('1 atm', 101325), ('1 psi', 6894.757), ('1 MPa (1 N/mm²)', 1e6),
         ('1 kgf/cm²', 98066.5), ('1 mmHg', 133.322), ('1 m of water', 9806.65)]
un_rows = ''.join(f"| {nm} | {pa:,.6g} Pa | {pa/1e3:,.6g} kPa | {pa/1e5:,.6g} bar | {pa/6894.757:,.5g} psi |\n" for nm, pa in UNITS)
hy_rows = ''
for d1, d2, F1 in ((10, 50, 100), (20, 100, 200), (25, 250, 300)):
    A1 = math.pi / 4 * (d1 / 1000) ** 2; A2 = math.pi / 4 * (d2 / 1000) ** 2; p = F1 / A1
    hy_rows += f"| {d1} mm | {d2} mm | {F1} N | {p/1e5:,.2f} bar | {p*A2/1000:,.2f} kN |\n"

W('physics/pressure', f'''
title: Pressure Calculator (P = F/A, Force and Area)
description: Calculate pressure from force and area with P = F/A, or the force or area from a pressure — in Pa, kPa, bar, psi or MPa, with examples and unit tables.
category: physics
intro: "Pressure is force spread over an area, P = F ÷ A. It explains why sharp knives cut and why wide tyres do not sink, and it is one of the most measured quantities in industry — see [absolute vs gauge pressure](https://www.instrumentationblog.in/absolute-vs-gauge-pressure/) and [Pascal's law in pressure instruments](https://www.instrumentationblog.in/understanding-pascals-law-pressure-instruments/). This pressure calculator finds the pressure from any force and area, or the force or area you need for a target pressure, in Pa, kPa, bar, psi or MPa."
keywords: [pressure calculator, p = f/a, pressure formula, force and area to pressure, calculate pressure from force, pressure in pascals, force over area calculator, psi calculator]
updated: {U}
variables:
  - {{ id: F, label: Force, family: force, unit: N, imperialUnit: lbf, default: {pF:g}, min: 0 }}
  - {{ id: A, label: Area, family: area, unit: cm2, imperialUnit: in2, default: {pA:g}, min: 0 }}
  - {{ id: P, label: Pressure, family: pressure, unit: kPa, imperialUnit: psi, min: 0 }}
equations:
  - P = F / A
faq:
  - q: What is the pressure formula?
    a: Pressure = force ÷ area, P = F/A. With the force in newtons and the area in square metres the pressure is in pascals (1 Pa = 1 N/m²). 700 N on 400 cm² (0.04 m²) is 17,500 Pa = 17.5 kPa.
  - q: How do I find force from pressure and area?
    a: Rearrange to F = P × A. A pressure of 6 bar (600,000 Pa) on a 50 mm diameter piston (0.001963 m²) gives 1,178 N. Clear the force box, enter the pressure and the area, and the calculator does this for you.
  - q: Why do sharp knives cut better?
    a: The same force on a much smaller area creates a much higher pressure. A knife edge or a pin point concentrates the force on a tiny area so the pressure exceeds the strength of the material; snowshoes do the opposite and spread your weight so you do not sink.
  - q: How do I convert kPa to psi?
    a: Divide by 6.895 (1 psi = 6.894757 kPa). 200 kPa is 29.0 psi and 1 bar is 14.5 psi. Use the pressure converter for other units.
related: [conversion/pressure-converter, engineering/hydrostatic-pressure, engineering/hydraulic-cylinder-force, engineering/absolute-gauge-pressure, physics/force, physics/buoyancy]
''', f'''
## How to use the pressure calculator

Enter the **force** and the **area** it acts on. The pressure appears in kPa, or any unit you pick — Pa, bar, psi, MPa, atm and more. Clear any one box to solve for it: enter a pressure and an area to get the force, or a force and a pressure limit to get the minimum area. The units of force and area can be changed independently; the calculation is done in newtons and square metres.

## Pressure formula

<p class="formula">P = F ÷ A &nbsp;·&nbsp; F = P × A &nbsp;·&nbsp; A = F ÷ P</p>

P in pascals, F in newtons, A in m². Remember that 1 cm² = 0.0001 m² and 1 mm² = 0.000001 m²; a weight in kg must be multiplied by g = 9.81 m/s² to give a force in newtons.

## Worked example

A 71 kg person (weight about {pF:g} N) standing on two feet with a total contact area of {pA:g} cm²:

- Area = {pA:g} cm² = {pA/1e4:g} m²
- P = {pF:g} ÷ {pA/1e4:g} = **{pP:,.0f} Pa** = **{pP/1000:g} kPa** ({pP/6894.757:.2f} psi)

On one stiletto heel of 1 cm² carrying the full weight, the pressure is {pF:g} ÷ 0.0001 = **{pF/1e-4/1e3:,.0f} kPa** — 400 times higher.

## Pressure examples

| Situation | Force | Area | Pressure | Pressure (psi) |
|---|---|---|---|---|
{si_rows}
## Pressure unit conversions

| Unit | Pa | kPa | bar | psi |
|---|---|---|---|---|
{un_rows}
## Pressure in liquids and hydraulics

In a liquid at rest, pressure rises with depth, P = ρ g h: every 10 m of water adds about 98 kPa — roughly one atmosphere (see the [hydrostatic pressure calculator](/engineering/hydrostatic-pressure/)). Pressure applied to an enclosed liquid is transmitted equally in all directions (Pascal's principle), so a small force on a small piston creates a large force on a large piston:

| Small piston | Large piston | Force on small piston | Pressure | Force on large piston |
|---|---|---|---|---|
{hy_rows}
Car brakes, jacks and presses use this; size real cylinders with the [hydraulic cylinder force calculator](/engineering/hydraulic-cylinder-force/).

## Practical notes

- **Gauge vs absolute:** most gauges read pressure above atmospheric (gauge pressure). Add about 101.3 kPa to get absolute pressure at sea level — see the [absolute and gauge pressure calculator](/engineering/absolute-gauge-pressure/).
- **Pressure vs stress:** stress in a solid has the same units (N/m², often given as MPa = N/mm²) and the same formula, but acts in a particular direction, while fluid pressure acts equally in all directions.
- **Tyres:** a tyre's contact patch grows until patch area × inflation pressure roughly equals the load on the wheel, which is why under-inflated tyres flatten and wear at the edges.
''')

# ---------------------------------------------------------------- Permutations
def nPr(n, r): return math.perm(n, r)
qn, qr = 10, 3
qP = nPr(qn, qr); qPr = qn ** qr; qC = math.comb(qn, qr)
SITU = [('Podium: 3 from 8 runners', 8, 3), ('4-digit PIN, no repeated digits', 10, 4), ('Arrange 5 books on a shelf', 5, 5),
        ('President, VP and secretary from 20', 20, 3), ('Batting order of 11 players', 11, 11), ('3-letter codes, no repeated letters', 26, 3),
        ('Top 4 of 32 teams in order', 32, 4)]
st_rows = ''.join(f"| {s} | {n} | {r} | {nPr(n, r):,} | {math.comb(n, r):,} |\n" for s, n, r in SITU)
gr_rows = ''
for n in (4, 5, 6, 8, 10, 12):
    gr_rows += f"| {n} | " + ' | '.join(f"{nPr(n, r):,}" if r <= n else '—' for r in (1, 2, 3, 4, 5, 6)) + " |\n"
rep_rows = ''.join(f"| {s} | {n} | {r} | {n**r:,} | {nPr(n, r):,} |\n" for s, n, r in
                   (('4-digit PIN', 10, 4), ('6-digit OTP', 10, 6), ('3-letter code', 26, 3), ('Coin tossed 10 times', 2, 10), ('Byte (8 bits)', 2, 8)))
f52 = math.factorial(52)

W('statistics/permutations', f'''
title: Permutation Calculator (nPr, Order Matters)
description: Calculate permutations nPr = n!/(n − r)! — ordered arrangements of r items from n — plus permutations with repetition and the matching combinations.
category: statistics
intro: "A permutation counts the ways to arrange items when the order matters — race finishing positions, PIN codes or the order of songs in a playlist. This permutation calculator works out nPr = n! ÷ (n − r)! for any n and r, and also gives the count when items may repeat (n to the power r) and the number of combinations nCr, so you can see how much the order adds."
keywords: [permutation calculator, npr calculator, permutation formula, permutations with repetition, number of arrangements, order matters, npr vs ncr, how many ways to arrange]
updated: {U}
variables:
  - {{ id: n, label: Total items (n), default: {qn}, min: 0 }}
  - {{ id: r, label: Items chosen and arranged (r), default: {qr}, min: 0 }}
  - {{ id: P, label: Permutations nPr (no repetition), min: 0 }}
  - {{ id: Pr, label: Permutations with repetition (nʳ), min: 0 }}
  - {{ id: C, label: Combinations nCr (order ignored), min: 0 }}
equations:
  - P = nPr(n, r)
  - Pr = n^r
  - C = nCr(n, r)
faq:
  - q: What is the permutation formula?
    a: nPr = n! ÷ (n − r)!, which is the product of r numbers counting down from n. For n = 10 and r = 3 that is 10 × 9 × 8 = 720. When all n items are arranged (r = n) it is simply n!.
  - q: What is the difference between permutations and combinations?
    a: Permutations count ordered arrangements; combinations count unordered selections. Each selection of r items can be arranged in r! orders, so nPr = nCr × r!. From 10 people you can form 120 committees of 3 but 720 ordered line-ups of 3.
  - q: How do you count permutations with repetition?
    a: When each position can reuse any of the n items, there are nʳ arrangements. A 4-digit PIN with repeats allowed has 10⁴ = 10,000 possibilities, against 10P4 = 5,040 when every digit must be different.
  - q: How many ways can letters with repeats be arranged?
    a: Divide n! by the factorial of each repeat count. MISSISSIPPI has 11 letters with 4 S, 4 I and 2 P, so there are 11! ÷ (4! × 4! × 2!) = 34,650 distinct arrangements.
related: [statistics/combinations, math/factorial, statistics/probability, statistics/binomial-probability, statistics/birthday-paradox, statistics/hypergeometric-distribution]
''', f'''
## How to use the permutation calculator

Enter the **total number of items** n and how many of them are **chosen and arranged**, r. The calculator gives the number of permutations without repetition (nPr), the number with repetition allowed (nʳ) and, for comparison, the number of combinations where order does not matter (nCr). r must not be larger than n for nPr and nCr; with repetition any r works.

## Permutation formulas

<p class="formula">nPr = n! ÷ (n − r)! = n × (n − 1) × … × (n − r + 1)</p>

<p class="formula">with repetition: nʳ &nbsp;·&nbsp; combinations: nCr = nPr ÷ r!</p>

## Worked example

How many ways can gold, silver and bronze be awarded among {qn} runners?

- {qn}P{qr} = {qn}! ÷ ({qn} − {qr})! = {qn} × {qn-1} × {qn-2} = **{qP:,}**
- If one runner could win more than one medal (repetition allowed): {qn}<sup>{qr}</sup> = **{qPr:,}**
- If only the group of three medal winners mattered, not who won which medal: {qn}C{qr} = {qP} ÷ {qr}! = **{qC:,}**

## Common permutation problems

| Situation | n | r | Permutations nPr | Combinations nCr |
|---|---|---|---|---|
{st_rows}
## nPr table

| n | r = 1 | r = 2 | r = 3 | r = 4 | r = 5 | r = 6 |
|---|---|---|---|---|---|---|
{gr_rows}
## With and without repetition

| Situation | n | r | With repetition (nʳ) | Without repetition (nPr) |
|---|---|---|---|---|
{rep_rows}
## Practical notes

- **Circular arrangements:** seating n people around a round table, where rotations count as the same, gives (n − 1)! arrangements — 6 people can sit in 5! = 120 distinct ways.
- **Huge numbers:** a deck of 52 cards can be ordered in 52! ≈ {f52/10**67:.2f} × 10<sup>67</sup> ways, so every well-shuffled deck is almost certainly in an order never seen before. Use the [factorial calculator](/math/factorial/) for large factorials.
- **Probability:** the chance of guessing an ordered outcome at random is 1 ÷ nPr — 1 in {qP} for the podium example. Unordered outcomes use the [combinations calculator](/statistics/combinations/).
''')

print(len(DONE), 'improved:', ' '.join(DONE))
