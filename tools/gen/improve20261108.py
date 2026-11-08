"""Improve pass (2026-11-08) for thin pages from the first batch (2026-10-27):
chemistry/grahams-law, physics/escape-velocity, physics/torque (current-divider was improved on 2026-11-07).
Keyword-first titles, 120-160 char descriptions, intros with the "<topic> calculator" phrase,
worked examples and reference tables computed here, practical notes, re-checked FAQs.
Slugs, categories and existing variable ids are unchanged (asserted). Re-running regenerates the same files."""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from page import page, BASE
from ib import intro
U = '2026-11-08'
G = 6.6743e-11
DONE = []

def ids_of(cid):
    fm = open(os.path.join(BASE, cid + '.mdx')).read().split('---')[1]
    d = yaml.safe_load(fm); return [v['id'] for v in d['variables']], d['category']

def W(cid, fm, body):
    cat, slug = cid.split('/')
    old_ids, old_cat = ids_of(cid)
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (cid, len(d))
    assert 'featured' not in fm
    page(cat, slug, fm, body)
    new_ids, new_cat = ids_of(cid)
    assert new_cat == old_cat == cat, cid
    assert all(i in new_ids for i in old_ids), (cid, old_ids, new_ids)
    DONE.append(cid)

# ---------------------------------------------------------------- Graham's law
gases = [('Hydrogen (H₂)', 2.016), ('Helium (He)', 4.003), ('Methane (CH₄)', 16.04), ('Ammonia (NH₃)', 17.03),
         ('Neon (Ne)', 20.18), ('Nitrogen (N₂)', 28.01), ('Oxygen (O₂)', 32.00), ('Argon (Ar)', 39.95),
         ('Carbon dioxide (CO₂)', 44.01), ('Chlorine (Cl₂)', 70.90), ('Sulphur hexafluoride (SF₆)', 146.06)]
g_rows = ''.join(f"| {nm} | {M:g} | {math.sqrt(28.96/M):.2f}× | {math.sqrt(M/28.96):.2f}× |\n" for nm, M in gases)
gH, gO = 2.016, 32.00; gr = math.sqrt(gO / gH)
g_ratio = 0.672  # unknown gas effuses 0.672 times as fast as O2
gMu = 32.00 / g_ratio ** 2
gNH3 = math.sqrt(36.46 / 17.03); gU = math.sqrt(352.02 / 349.03)
W('chemistry/grahams-law', f'''
title: Graham's Law Calculator (Rate of Effusion & Molar Mass)
description: Calculate how many times faster one gas effuses or diffuses than another with Graham's law, or find an unknown molar mass from a measured rate ratio.
category: chemistry
{intro("Lighter gases escape through small holes and spread out faster than heavier ones: Graham's law says the rate is inversely proportional to the square root of the molar mass. This Graham's law calculator gives the rate ratio and time ratio of two gases, and works backwards to find an unknown molar mass from a measured effusion rate.")}
keywords: [grahams law calculator, graham's law of effusion calculator, rate of effusion calculator, diffusion rate, molar mass from effusion, effusion rate ratio, gas diffusion]
updated: {U}
variables:
  - {{ id: M1, label: Molar mass of gas 1, suffix: g/mol, default: 2.016, min: 0.0001 }}
  - {{ id: M2, label: Molar mass of gas 2, suffix: g/mol, default: 32.00, min: 0.0001 }}
  - {{ id: r, label: Rate ratio (gas 1 ÷ gas 2), min: 0, decimals: 4 }}
  - {{ id: tr, label: Time ratio (gas 1 ÷ gas 2), min: 0, decimals: 4 }}
equations:
  - r = sqrt(M2 / M1)
  - tr = 1 / r
faq:
  - q: What is Graham's law?
    a: The rate of effusion of a gas is inversely proportional to the square root of its molar mass, rate₁ ÷ rate₂ = √(M₂ ÷ M₁), at the same temperature and pressure.
  - q: How much faster does hydrogen effuse than oxygen?
    a: About {gr:.2f} times faster, since √(32.00 ÷ 2.016) ≈ {gr:.2f}.
  - q: How do I find an unknown molar mass with Graham's law?
    a: Measure the rate ratio of the unknown gas against a known gas, enter the ratio and the known molar mass, and solve for the unknown molar mass — M_unknown = M_known ÷ (rate ratio)².
  - q: Why do helium balloons deflate faster than air-filled ones?
    a: Helium atoms are light (4 g/mol) and small, so they escape through the balloon wall much faster than the nitrogen and oxygen in air (about 29 g/mol on average).
related: [chemistry/daltons-law, physics/ideal-gas-law, chemistry/moles, chemistry/combined-gas-law]
''', f'''
## How to use the Graham's law calculator

Enter the **molar masses** of two gases in g/mol. The calculator gives how many times faster gas 1 effuses than gas 2 and the ratio of the times taken for the same amount to escape. To find an **unknown molar mass**, enter the known gas as gas 2 and the measured rate ratio, then press × on the molar mass of gas 1 to solve for it.

## Graham's law formula

<p class="formula">Rate₁ ÷ Rate₂ = √(M₂ ÷ M₁) &nbsp;·&nbsp; t₁ ÷ t₂ = √(M₁ ÷ M₂)</p>

<p class="formula">M₁ = M₂ ÷ (Rate₁ ÷ Rate₂)²</p>

The law follows from kinetic theory: at the same temperature all gases have the same average kinetic energy, ½mv², so the mean molecular speed is proportional to 1/√M.

## Worked examples

Hydrogen (2.016 g/mol) against oxygen (32.00 g/mol):

- Rate ratio = √(32.00 ÷ 2.016) = **{gr:.4f}** — hydrogen effuses about four times faster
- Time ratio = 1 ÷ {gr:.4f} = **{1/gr:.4f}** — it takes a quarter of the time

An unknown gas effuses {g_ratio:g} times as fast as oxygen:

- M = 32.00 ÷ {g_ratio:g}² = **{gMu:.1f} g/mol** — close to chlorine, Cl₂ (70.90 g/mol)

## Effusion rates relative to air (28.96 g/mol)

| Gas | Molar mass (g/mol) | Rate relative to air | Time relative to air |
|---|---|---|---|
{g_rows}
## Effusion vs diffusion

- **Effusion** — gas escaping through a hole smaller than the mean free path into a vacuum. Graham's law applies closely.
- **Diffusion** — gas spreading through another gas. Graham's law gives the right trend, but collisions with the other gas make it approximate.

## Practical examples

- **Ammonia and HCl tube** — cotton wool soaked in ammonia (17.03 g/mol) and hydrochloric acid (HCl, 36.46 g/mol) at opposite ends of a tube form a white ring of ammonium chloride nearer the HCl end, because ammonia diffuses about {gNH3:.2f} times faster.
- **Uranium enrichment** — gaseous diffusion plants separated ²³⁵UF₆ (349.03 g/mol) from ²³⁸UF₆ (352.02 g/mol). The ideal separation factor per stage is only {gU:.4f}, so thousands of stages were needed.
- **Leak testing** — helium is used as a tracer gas because it passes through tiny leaks far faster than air and is easy to detect.
''')

# ---------------------------------------------------------------- Escape velocity
bodies = [('Moon', 7.342e22, 1737.4), ('Mercury', 3.3011e23, 2439.7), ('Mars', 6.4171e23, 3389.5),
          ('Venus', 4.8675e24, 6051.8), ('Earth', 5.9722e24, 6371.0), ('Uranus', 8.681e25, 25362),
          ('Neptune', 1.02413e26, 24622), ('Saturn', 5.6834e26, 58232), ('Jupiter', 1.8982e27, 69911),
          ('Sun', 1.98847e30, 696340)]
e_rows = ''
for nm, M, Rk in bodies:
    v = math.sqrt(2 * G * M / (Rk * 1e3))
    e_rows += f"| {nm} | {M:.3e} | {Rk:,.0f} | {v/1e3:.2f} km/s | {v*3.6:,.0f} km/h | {G*M/(Rk*1e3)**2:.2f} m/s² |\n"
eM, eR = 5.972e24, 6371e3
ev = math.sqrt(2 * G * eM / eR); eg = G * eM / eR ** 2; evo = math.sqrt(G * eM / eR)
alt_rows = ''
for h in (0, 400, 2000, 20200, 35786, 384400):
    r_ = eR + h * 1e3
    alt_rows += f"| {h:,} km | {math.sqrt(G*eM/r_)/1e3:.2f} km/s | {math.sqrt(2*G*eM/r_)/1e3:.2f} km/s |\n"
W('physics/escape-velocity', f'''
title: Escape Velocity Calculator (km/s from Mass & Radius)
description: Calculate the escape velocity in km/s and km/h from any planet, moon or star's mass and radius, with surface gravity and circular orbital velocity.
category: physics
{intro("Escape velocity is the speed an unpowered object needs to break free of a body's gravity, about 11.2 km/s from the Earth's surface. This escape velocity calculator works it out from the mass and radius of any planet, moon or star, and also gives the surface gravity and the circular orbital velocity at the same distance.")}
keywords: [escape velocity calculator, escape velocity formula, escape velocity of earth, escape speed calculator, 11.2 km/s, planet escape velocity, sqrt 2gm/r, orbital velocity]
updated: {U}
variables:
  - {{ id: M, label: Mass of the body, suffix: kg, default: 5.972e24, min: 0 }}
  - {{ id: R, label: Radius (or distance from centre), family: length, unit: km, imperialUnit: mi, default: 6371, min: 0 }}
  - {{ id: v, label: Escape velocity, family: velocity, unit: kmh, imperialUnit: mph, min: 0 }}
  - {{ id: vk, label: Escape velocity in km/s, suffix: km/s, min: 0, decimals: 3 }}
  - {{ id: vo, label: Circular orbital velocity at this distance, suffix: km/s, min: 0, decimals: 3 }}
  - {{ id: g, label: Surface gravity (gravity at this distance), suffix: m/s², min: 0, decimals: 3 }}
equations:
  - v = sqrt(2 * 6.6743e-11 * M / R)
  - vk = v / 1000
  - vo = vk / sqrt(2)
  - g = 6.6743e-11 * M / R^2
faq:
  - q: What is the escape velocity of Earth?
    a: About 11.19 km/s (roughly 40,300 km/h or 25,000 mph) from the surface, ignoring air resistance and the Earth's rotation.
  - q: What is the escape velocity formula?
    a: v = √(2GM ÷ R), where G = 6.674 × 10⁻¹¹ N·m²/kg², M is the mass of the body and R the distance from its centre. It comes from setting kinetic energy ½mv² equal to the gravitational energy GMm ÷ R needed to reach infinity.
  - q: Does escape velocity depend on the mass of the rocket?
    a: No. It depends only on the mass of the planet and the distance from its centre. A heavier rocket needs more energy to escape, but the same speed.
  - q: Do rockets actually reach escape velocity?
    a: Not necessarily. Escape velocity is the speed for an unpowered object launched once. A rocket that keeps thrusting can climb away more slowly; spacecraft heading to other planets do reach about 11 km/s relative to the Earth, usually starting from a parking orbit.
related: [physics/orbital-period, physics/gravitational-force, physics/weight, physics/centripetal-force]
''', f'''
## How to use the escape velocity calculator

Enter the **mass** of the planet, moon or star in kilograms and its **radius** — or, for escape from an orbit, the distance from the centre (radius + altitude). The calculator gives the escape velocity in km/h (or mph) and km/s, the circular orbital velocity at the same distance and the gravitational acceleration there. The defaults are for the Earth.

## Escape velocity formula

<p class="formula">v<sub>esc</sub> = √(2GM ÷ R) &nbsp;·&nbsp; v<sub>orbit</sub> = √(GM ÷ R) = v<sub>esc</sub> ÷ √2</p>

G = 6.6743 × 10⁻¹¹ N·m²/kg². Because g = GM/R², the formula can also be written v<sub>esc</sub> = √(2gR).

## Worked example

Earth: M = 5.972 × 10²⁴ kg, R = 6,371 km:

- v<sub>esc</sub> = √(2 × 6.6743 × 10⁻¹¹ × 5.972 × 10²⁴ ÷ 6.371 × 10⁶) = **{ev/1e3:.3f} km/s** = **{ev*3.6:,.0f} km/h**
- Circular orbital velocity at the surface = {ev/1e3:.3f} ÷ √2 = **{evo/1e3:.3f} km/s**
- Surface gravity = **{eg:.3f} m/s²**

## Escape velocities in the solar system

| Body | Mass (kg) | Radius (km) | Escape velocity | In km/h | Surface gravity |
|---|---|---|---|---|---|
{e_rows}
## Escape and orbital velocity above the Earth

| Altitude | Circular orbital velocity | Escape velocity |
|---|---|---|
{alt_rows}
400 km is about the height of the International Space Station, 20,200 km GPS, 35,786 km geostationary orbit and 384,400 km the Moon's distance. See the [orbital period calculator](/physics/orbital-period/) for the time to go round.

## Practical notes

- Launching **eastward** from near the equator gains up to 0.47 km/s from the Earth's rotation.
- Real launches need more than escape velocity in total because of **gravity losses and air drag** — typically 1.5–2 km/s extra for reaching orbit.
- The **Moon has no atmosphere** largely because its escape velocity is only about 2.4 km/s: over millions of years, fast-moving gas molecules escape.
- A **black hole** is an object whose escape velocity at the event horizon equals the speed of light: R = 2GM ÷ c².
''')

# ---------------------------------------------------------------- Torque
tF, tr, tth = 200.0, 0.3, 90.0
tT = tF * tr * math.sin(math.radians(tth))
f_rows = ''
for T in (25, 50, 100, 150, 250):
    f_rows += f"| {T} N·m | " + ' | '.join(f"{T/L:,.0f} N ({T/L/9.80665:.1f} kgf)" for L in (0.2, 0.3, 0.5)) + " |\n"
a_rows = ''
for a in (90, 75, 60, 45, 30, 15, 0):
    a_rows += f"| {a}° | {math.sin(math.radians(a)):.3f} | {tF*tr*math.sin(math.radians(a)):.1f} N·m |\n"
W('physics/torque', f'''
title: Torque Calculator (τ = F × r × sin θ)
description: Calculate torque from force, lever arm length and angle, or the force needed to reach a target torque with a spanner or wrench — in N·m, lbf·ft or kgf·m.
category: physics
{intro("Torque is the turning effect of a force: the force multiplied by its perpendicular distance from the pivot. This torque calculator gives the torque from the force, the lever arm length and the angle between them, or works backwards to the force or spanner length needed for a target torque, in N·m, lbf·ft or kgf·m.")}
keywords: [torque calculator, torque formula, torque equation, force times distance, moment of force calculator, wrench torque calculator, lever arm, newton metre]
updated: {U}
variables:
  - {{ id: F, label: Force, family: force, unit: N, imperialUnit: lbf, default: 200, min: 0 }}
  - {{ id: r, label: Lever arm length, family: length, unit: m, imperialUnit: ft, default: 0.3, min: 0 }}
  - {{ id: th, label: Angle between force and lever, family: angle, unit: deg, default: 90, min: 0, max: 3.1416 }}
  - {{ id: T, label: Torque, family: torque, unit: Nm, imperialUnit: lbft, min: 0 }}
  - {{ id: rp, label: Perpendicular lever arm (r × sin θ), family: length, unit: m, imperialUnit: ft, min: 0 }}
equations:
  - T = F * r * sin(th)
  - rp = r * sin(th)
faq:
  - q: What is the torque formula?
    a: τ = F × r × sin θ, where F is the force, r the distance from the pivot to where the force acts and θ the angle between the force and the lever. At 90° it is simply force × distance.
  - q: Why is a longer spanner easier to use?
    a: Torque is force × distance, so doubling the handle length halves the force needed for the same torque.
  - q: What is the difference between torque and work?
    a: Both have units of newton-metres, but torque is a turning effect (a vector along the axis of rotation), while work is energy (a scalar), normally written in joules.
  - q: How do I convert N·m to lbf·ft and kgf·m?
    a: 1 N·m = 0.7376 lbf·ft = 0.10197 kgf·m. So 100 N·m ≈ 73.8 lbf·ft ≈ 10.2 kgf·m.
related: [conversion/torque-converter, engineering/torque-power-speed, engineering/bolt-torque, physics/rotational-kinetic-energy]
''', f'''
## How to use the torque calculator

Enter the **force**, the **lever arm length** (from the pivot or bolt centre to where the force is applied) and the **angle** between the force and the lever — 90° for a push at right angles. The calculator gives the torque and the effective (perpendicular) lever arm. To find the force needed for a specified torque, enter the torque and press × on Force.

## Torque formula

<p class="formula">τ = F × r × sin θ &nbsp;·&nbsp; τ = F × r<sub>⊥</sub></p>

Torque is greatest when the force is perpendicular to the lever (θ = 90°) and zero when pushing along the lever (θ = 0°).

## Worked example

A force of {tF:g} N on a {tr:g} m spanner at {tth:g}°:

- τ = {tF:g} × {tr:g} × sin 90° = **{tT:g} N·m** = {tT*0.737562:.1f} lbf·ft = {tT/9.80665:.2f} kgf·m
- Pushing at 45° instead gives only {tF*tr*math.sin(math.radians(45)):.1f} N·m — the perpendicular lever arm shrinks to {tr*math.sin(math.radians(45)):.3f} m

## Effect of the angle ({tF:g} N on a {tr:g} m lever)

| Angle | sin θ | Torque |
|---|---|---|
{a_rows}
## Force needed for common torques

| Torque | 20 cm spanner | 30 cm spanner | 50 cm breaker bar |
|---|---|---|---|
{f_rows}
## Levers and balance

A lever balances when the torques on both sides are equal: F₁ × r₁ = F₂ × r₂. A 50 kg child 2 m from a see-saw pivot balances a 100 kg adult 1 m from it.

## Typical torques

| Task | Typical torque |
|---|---|
| Opening a jar lid | 1–3 N·m |
| M8 steel bolt (property class 8.8) | about 25 N·m |
| Bicycle pedal (hard effort) | 50–100 N·m |
| Car wheel nuts | 80–140 N·m |
| Small car engine (peak) | 100–250 N·m |

## Practical notes

- Use a calibrated **torque wrench** where a bolt torque is specified, and hold it at the marked grip — pulling elsewhere changes the lever length.
- An **in-line extension** on a torque wrench increases the applied torque: actual torque = reading × (L + extension) ÷ L, where L is the wrench length.
- For the torque needed to reach a given bolt preload, use the [bolt torque calculator](/engineering/bolt-torque/); for torque from power and speed, the [torque–power–speed calculator](/engineering/torque-power-speed/).
''')

print(len(DONE), 'improved:', ' '.join(DONE))
