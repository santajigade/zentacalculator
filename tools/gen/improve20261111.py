"""Improve pass (2026-11-11) for thin pages from the first batch (2026-10-27):
physics/hookes-law, chemistry/charles-law, chemistry/molality, physics/buoyancy.
Keyword-first titles, 120-160 char descriptions, intros with the "<topic> calculator" phrase,
worked examples and reference tables computed here, practical notes, re-checked FAQs (duplicate FAQs removed,
Gay-Lussac link fixed). Slugs, categories and existing variable ids are unchanged (asserted).
Re-running regenerates the same files."""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from page import page, BASE
from ib import intro
U = '2026-11-11'
G = 9.80665
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
    t = re.search(r'^intro: (.*)$', fm, re.M).group(1)
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    page(cat, slug, fm, body)
    new_ids, new_cat = ids_of(cid)
    assert new_cat == old_cat == cat, cid
    assert all(i in new_ids for i in old_ids), (cid, old_ids, new_ids)
    DONE.append(cid)

# ---------------------------------------------------------------- Hooke's law
hk, hx = 500.0, 0.04
hF = hk * hx; hE = 0.5 * hk * hx ** 2; hm = hF / G
hf_rows = ''
for k in (100, 500, 1000, 5000, 20000):
    hf_rows += f"| {k:,} N/m | " + ' | '.join(f"{k*x/1000:,.4g} N" for x in (5, 10, 20, 50)) + " |\n"
hs_rows = ''
for k1, k2 in ((500, 500), (500, 1000), (200, 800), (1000, 3000)):
    hs_rows += f"| {k1:,} and {k2:,} N/m | {k1+k2:,} N/m | {k1*k2/(k1+k2):,.1f} N/m |\n"
hT = 2 * math.pi * math.sqrt(0.5 / hk)
W('physics/hookes-law', f'''
title: Hooke's Law Calculator (Spring Force F = kx)
description: Calculate spring force, spring constant or extension with Hooke's law F = kx, plus the elastic energy stored and the equivalent hanging mass.
category: physics
{intro("Within its elastic limit, a spring pushes back with a force proportional to how far it is stretched or compressed — Hooke's law, F = kx. This Hooke's law calculator gives the spring force, the elastic potential energy stored and the mass that would produce the same force when hung from the spring, and solves for the spring constant or the extension when you know the force.")}
keywords: [hookes law calculator, spring constant calculator, spring force calculator, f = kx calculator, elastic potential energy calculator, spring extension calculator, spring stiffness]
updated: {U}
variables:
  - {{ id: k, label: Spring constant (k), suffix: N/m, default: {hk:g}, min: 0, help: '1 N/mm = 1,000 N/m; 1 lbf/in = 175.13 N/m.' }}
  - {{ id: x, label: Extension or compression, family: length, unit: cm, imperialUnit: in, default: {hx*100:g}, min: 0 }}
  - {{ id: F, label: Spring force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: E, label: Stored elastic energy, family: energy, unit: J, min: 0 }}
  - {{ id: m, label: Equivalent hanging mass (F ÷ g), family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - F = k * x
  - E = 0.5 * k * x^2
  - m = F / g0
faq:
  - q: What is Hooke's law?
    a: The force needed to stretch or compress a spring is proportional to the change in length, F = k x, where k is the spring constant. It holds as long as the spring stays within its elastic limit; the spring then pulls back with the same force in the opposite direction (F = −k x).
  - q: How do I find the spring constant?
    a: Hang a known mass from the spring and measure the extension, then divide the weight by the extension, k = m g ÷ x. A 1 kg mass (9.81 N) that stretches a spring by 2 cm gives k = 9.81 ÷ 0.02 ≈ 490 N/m. Using several masses and taking the slope of the force–extension line is more accurate.
  - q: How much energy does a spring store?
    a: E = ½ k x², the area under the force–extension line. A 500 N/m spring compressed 4 cm stores ½ × 500 × 0.04² = 0.4 J. Doubling the compression stores four times the energy.
  - q: How do springs in series and parallel combine?
    a: In parallel the stiffnesses add, k = k₁ + k₂. In series the compliances add, 1/k = 1/k₁ + 1/k₂, so two equal springs end to end are half as stiff as one.
related: [physics/spring-mass-frequency, physics/youngs-modulus, physics/potential-energy, engineering/spring-rate]
''', f'''
## How to use the Hooke's law calculator

Enter the **spring constant** and the **extension or compression** from the spring's free length. The calculator gives the **spring force**, the **elastic energy** stored and the **equivalent hanging mass** — the mass whose weight equals that force. To find the spring constant, enter the force and the extension and press × on the spring constant; to find the extension for a load, enter the force and press × on the extension.

## Hooke's law formulas

<p class="formula">F = k x &nbsp;·&nbsp; E = ½ k x² &nbsp;·&nbsp; m = F ÷ g</p>

- **k** = spring constant (stiffness) in N/m
- **x** = change in length from the free length, in metres
- **g** = 9.80665 m/s²

## Worked example

A spring with k = {hk:g} N/m is stretched by {hx*100:g} cm ({hx:g} m):

- Force = {hk:g} × {hx:g} = **{hF:g} N**
- Energy stored = ½ × {hk:g} × {hx:g}² = **{hE:g} J**
- Equivalent hanging mass = {hF:g} ÷ 9.80665 = **{hm:.3f} kg** — hanging about 2 kg from this spring stretches it by 4 cm

## Spring force for common stiffnesses

| Spring constant | 5 mm | 10 mm | 20 mm | 50 mm |
|---|---|---|---|---|
{hf_rows}
## Springs in series and parallel

| Two springs | Parallel (k₁ + k₂) | Series (k₁k₂ ÷ (k₁ + k₂)) |
|---|---|---|
{hs_rows}
## Mass on a spring

A mass m on a spring oscillates with period T = 2π√(m ÷ k). A 0.5 kg mass on a {hk:g} N/m spring bounces with a period of **{hT:.3f} s** — see the [spring–mass frequency calculator](/physics/spring-mass-frequency/).

## Practical notes

- **Elastic limit:** beyond it the spring takes a permanent set and no longer returns to its free length; real springs also become non-linear near solid height (compression) or when the coils open up (extension).
- **Initial tension:** close-wound extension springs need a starting force before they stretch at all — add it to k x.
- To design a coil spring from wire size, coil diameter and number of turns, use the [spring rate calculator](/engineering/spring-rate/).
- For solid materials the same law appears as stress = Young's modulus × strain; steel has a Young's modulus of about 200 GPa — see the [Young's modulus calculator](/physics/youngs-modulus/).
''')

# ---------------------------------------------------------------- Charles's law
cV1, cT1, cT2 = 2.0, 20.0, 80.0
cV2 = cV1 * (cT2 + 273.15) / (cT1 + 273.15); cdV = cV2 - cV1
ct_rows = ''
for T in (-50, -20, 0, 25, 50, 100, 200, 500):
    v = 2 * (T + 273.15) / (25 + 273.15)
    ct_rows += f"| {T} °C | {T+273.15:.2f} K | {v:.3f} L | {(v/2-1)*100:+.1f}% |\n"
cGL = (100 + 273.15) / (20 + 273.15)
W('chemistry/charles-law', f'''
title: Charles's Law Calculator (V₁/T₁ = V₂/T₂)
description: Calculate the new volume or temperature of a gas at constant pressure with Charles's law V₁/T₁ = V₂/T₂, with °C and °F converted to kelvin for you.
category: chemistry
{intro("At constant pressure, the volume of a fixed amount of gas is directly proportional to its absolute temperature, so heating a gas makes it expand and cooling it makes it shrink. This Charles's law calculator solves V₁/T₁ = V₂/T₂ for whichever volume or temperature you leave blank, converts Celsius and Fahrenheit to kelvin automatically and shows the change in volume.")}
keywords: [charles law calculator, charles's law calculator, v1/t1 = v2/t2 calculator, gas volume and temperature, constant pressure gas law, volume temperature relationship, charles law formula]
updated: {U}
variables:
  - {{ id: V1, label: Initial volume, family: volume, unit: L, imperialUnit: ft3, default: {cV1:g}, min: 0 }}
  - {{ id: T1, label: Initial temperature, family: temperature, unit: C, imperialUnit: F, default: {cT1:g}, min: 0 }}
  - {{ id: V2, label: Final volume, family: volume, unit: L, imperialUnit: ft3, min: 0 }}
  - {{ id: T2, label: Final temperature, family: temperature, unit: C, imperialUnit: F, default: {cT2:g}, min: 0 }}
  - {{ id: dV, label: Change in volume (V₂ − V₁), family: volume, unit: L, imperialUnit: ft3 }}
equations:
  - V1 / T1 = V2 / T2
  - dV = V2 - V1
faq:
  - q: What is Charles's law?
    a: At constant pressure, the volume of a fixed amount of an ideal gas is directly proportional to its absolute temperature, V ∝ T, so V₁ ÷ T₁ = V₂ ÷ T₂. Doubling the absolute temperature doubles the volume.
  - q: Why must the temperature be in kelvin?
    a: Volume is proportional to absolute temperature, measured from absolute zero. Using °C would wrongly suggest that going from 20 °C to 80 °C quadruples the volume, and would give zero or negative volumes at and below 0 °C. The calculator converts °C and °F to kelvin before solving.
  - q: What is an example of Charles's law in everyday life?
    a: A hot-air balloon rises because the heated air inside expands and becomes less dense; a party balloon shrinks when taken out into the cold; and bread rises in the oven as gas bubbles in the dough expand.
  - q: Does Charles's law work for real gases?
    a: Very well for gases such as air, nitrogen and helium at ordinary pressures and temperatures well above their boiling points. It breaks down near condensation and at high pressures, where the van der Waals or other real-gas equations are needed.
related: [chemistry/gay-lussacs-law, chemistry/boyles-law, chemistry/combined-gas-law, physics/ideal-gas-law]
''', f'''
## How to use the Charles's law calculator

Enter **any three** of the initial volume, initial temperature, final volume and final temperature, in the units you prefer. The calculator converts the temperatures to kelvin, solves for the fourth value and shows the **change in volume**. The pressure and the amount of gas are assumed constant — if the pressure changes too, use the [combined gas law calculator](/chemistry/combined-gas-law/).

## Charles's law formula

<p class="formula">V₁ ÷ T₁ = V₂ ÷ T₂ &nbsp;·&nbsp; V₂ = V₁ × T₂ ÷ T₁ &nbsp;·&nbsp; T₂ = T₁ × V₂ ÷ V₁ &nbsp;(T in kelvin)</p>

T(K) = T(°C) + 273.15 and T(K) = (T(°F) + 459.67) × 5/9.

## Worked example

A {cV1:g} L balloon is warmed from {cT1:g} °C to {cT2:g} °C at constant pressure:

- T₁ = {cT1:g} + 273.15 = **{cT1+273.15:.2f} K**, T₂ = {cT2:g} + 273.15 = **{cT2+273.15:.2f} K**
- V₂ = {cV1:g} × {cT2+273.15:.2f} ÷ {cT1+273.15:.2f} = **{cV2:.4f} L**
- Change in volume = {cV2:.4f} − {cV1:g} = **{cdV:.4f} L**, an increase of {cdV/cV1*100:.1f}%

## Volume against temperature

A gas that fills 2 L at 25 °C, at constant pressure:

| Temperature | Absolute temperature | Volume | Change from 25 °C |
|---|---|---|---|
{ct_rows}
Each 1 °C change alters the volume by 1/{25+273.15:.2f} of its value at 25 °C — about 0.34%.

## Absolute zero

Extend the straight volume–temperature line backwards and it reaches zero volume at **−273.15 °C** (0 K). Charles's and Gay-Lussac's measurements were among the first clues that such an absolute zero of temperature exists.

## Related gas laws

- **Gay-Lussac's law** (constant volume): P₁ ÷ T₁ = P₂ ÷ T₂. A sealed can at 1 atm and 20 °C reaches about {cGL:.2f} atm at 100 °C — see the [Gay-Lussac's law calculator](/chemistry/gay-lussacs-law/).
- **Boyle's law** (constant temperature): P₁V₁ = P₂V₂ — see the [Boyle's law calculator](/chemistry/boyles-law/).
- All of them are special cases of the [ideal gas law](/physics/ideal-gas-law/) PV = nRT.

## Practical notes

- **Constant pressure in practice** means a gas free to expand: a balloon, a piston that moves freely, or a gas holder. In a rigid vessel the pressure rises instead.
- **Thermal expansion of gas in a pipe:** a 1% change in absolute temperature changes the actual volume flow by 1%, which is why gas flow meters correct to standard conditions.
- Humid air contains water vapour that can condense when it cools, so the dry-gas law slightly overestimates the shrinkage of moist air near its dew point.
''')

# ---------------------------------------------------------------- Molality
mms, mM, mmw, mi = 11.69, 58.44, 0.5, 2.0
mn = mms / mM; mb = mn / mmw; mw = mms / 1000 / (mms / 1000 + mmw)
mTf = mi * 1.86 * mb; mTb = mi * 0.512 * mb
SOL = (('Sodium chloride, NaCl', 58.44, 2), ('Calcium chloride, CaCl₂', 110.98, 3), ('Glucose, C₆H₁₂O₆', 180.16, 1), ('Sucrose, C₁₂H₂₂O₁₁', 342.30, 1), ('Urea, CH₄N₂O', 60.06, 1), ('Ethylene glycol, C₂H₆O₂', 62.07, 1))
ms_rows = ''
for nm, M, i in SOL:
    b = 10 / M / 1.0
    ms_rows += f"| {nm} | {M:g} g/mol | {i} | {b:.4f} mol/kg | {i*1.86*b:.3f} °C |\n"
KS = (('Water', 1.86, 0.512), ('Benzene', 5.12, 2.53), ('Acetic acid', 3.90, 3.07), ('Cyclohexane', 20.0, 2.79), ('Camphor', 37.7, 5.95))
mk_rows = ''.join(f"| {nm} | {kf:g} K·kg/mol | {kb:g} K·kg/mol |\n" for nm, kf, kb in KS)
W('chemistry/molality', f'''
title: Molality Calculator (mol/kg) with Freezing Point Drop
description: Calculate molality in mol/kg from the mass of solute, its molar mass and the mass of solvent, with mass percent and freezing and boiling point change in water.
category: chemistry
{intro("Molality is the number of moles of solute per kilogram of solvent, so unlike molarity it does not change when the solution warms up or cools down. This molality calculator works out the moles of solute and the molality from the masses you weigh out, gives the mass percent of the solution, and estimates the freezing point depression and boiling point elevation for a water solution.")}
keywords: [molality calculator, how to calculate molality, mol/kg calculator, molal concentration, molality formula, molality to freezing point, molality vs molarity]
updated: {U}
variables:
  - {{ id: ms, label: Mass of solute, family: mass, unit: g, default: {mms:g}, min: 0 }}
  - {{ id: M, label: Molar mass of solute, suffix: g/mol, default: {mM:g}, min: 0, help: 'NaCl 58.44, glucose 180.16, sucrose 342.30, urea 60.06 g/mol.' }}
  - {{ id: mw, label: Mass of solvent, family: mass, unit: kg, imperialUnit: lb, default: {mmw:g}, min: 0 }}
  - {{ id: i, label: "Van 't Hoff factor i (particles per formula unit)", default: {mi:g}, min: 0, help: '1 for sugars and urea, about 2 for NaCl, 3 for CaCl₂ (ideal values).' }}
  - {{ id: n, label: Moles of solute, suffix: mol, min: 0 }}
  - {{ id: b, label: Molality, suffix: mol/kg, min: 0 }}
  - {{ id: w, label: Mass percent of solute in the solution, family: percent, unit: '%', min: 0 }}
  - {{ id: dTf, label: Freezing point depression if the solvent is water, family: tempdiff, unit: K, imperialUnit: F, min: 0 }}
  - {{ id: dTb, label: Boiling point elevation if the solvent is water, family: tempdiff, unit: K, imperialUnit: F, min: 0 }}
equations:
  - n = ms * 1000 / M
  - b = n / mw
  - w = ms / (ms + mw)
  - dTf = i * 1.86 * b
  - dTb = i * 0.512 * b
faq:
  - q: How do you calculate molality?
    a: Divide the moles of solute by the mass of solvent in kilograms, b = n ÷ m_solvent. The moles come from the mass of solute divided by its molar mass. For 11.69 g of NaCl (0.2 mol) in 0.5 kg of water, b = 0.2 ÷ 0.5 = 0.4 mol/kg.
  - q: What is the difference between molality and molarity?
    a: Molality is moles per kilogram of solvent; molarity is moles per litre of solution. Molality does not change with temperature because masses do not, while the volume of a solution, and so its molarity, does. For dilute water solutions the two are nearly equal.
  - q: Why is molality used for freezing point depression?
    a: Colligative properties depend on the ratio of solute particles to solvent molecules, which molality expresses directly and independently of temperature. ΔT_f = i K_f b and ΔT_b = i K_b b, with K_f = 1.86 and K_b = 0.512 K·kg/mol for water.
  - q: How do you convert molarity to molality?
    a: b = c ÷ (ρ − c M ÷ 1000), with c in mol/L, the solution density ρ in kg/L and M in g/mol. The bracket is the mass of solvent in one litre of solution.
related: [chemistry/molarity, chemistry/freezing-point-depression, chemistry/boiling-point-elevation, chemistry/mass-percent]
''', f'''
## How to use the molality calculator

Enter the **mass of solute**, its **molar mass** and the **mass of solvent** — the solvent alone, not the whole solution. The calculator gives the **moles of solute**, the **molality** and the **mass percent**. Enter the **van 't Hoff factor** to estimate how much the solution's freezing point falls and boiling point rises if the solvent is water. To find how much solute to weigh for a target molality, enter the molality and press × on the mass of solute.

## Molality formula

<p class="formula">n = m<sub>solute</sub> ÷ M &nbsp;·&nbsp; b = n ÷ m<sub>solvent</sub> (kg) &nbsp;·&nbsp; w = m<sub>solute</sub> ÷ (m<sub>solute</sub> + m<sub>solvent</sub>)</p>

<p class="formula">ΔT<sub>f</sub> = i K<sub>f</sub> b &nbsp;·&nbsp; ΔT<sub>b</sub> = i K<sub>b</sub> b &nbsp;(water: K<sub>f</sub> = 1.86, K<sub>b</sub> = 0.512 K·kg/mol)</p>

## Worked example

{mms:g} g of sodium chloride (M = {mM:g} g/mol, i ≈ {mi:g}) dissolved in {mmw:g} kg of water:

- Moles of NaCl = {mms:g} ÷ {mM:g} = **{mn:.4f} mol**
- Molality = {mn:.4f} ÷ {mmw:g} = **{mb:.4f} mol/kg**
- Mass percent = {mms:g} ÷ ({mms:g} + {mmw*1000:g}) = **{mw*100:.3f}%**
- Freezing point depression = {mi:g} × 1.86 × {mb:.4f} = **{mTf:.3f} °C**, so the solution freezes at about −{mTf:.2f} °C
- Boiling point elevation = {mi:g} × 0.512 × {mb:.4f} = **{mTb:.4f} °C**, so it boils at about {100+mTb:.2f} °C at 1 atm

## 10 g of common solutes in 1 kg of water

| Solute | Molar mass | i | Molality | Freezing point drop |
|---|---|---|---|---|
{ms_rows}
On a mass basis, salts and small molecules lower the freezing point far more than sugar — which is why salt, not sugar, is used on icy roads.

## Freezing and boiling point constants

| Solvent | K<sub>f</sub> | K<sub>b</sub> |
|---|---|---|
{mk_rows}
## Molality vs molarity

| | Molality (b) | Molarity (c) |
|---|---|---|
| Definition | mol of solute per kg of solvent | mol of solute per L of solution |
| Changes with temperature? | No | Yes — the volume changes |
| Measured by | Weighing only | Weighing and a volumetric flask |
| Used for | Colligative properties, physical chemistry | Titrations and everyday lab work |

## Practical notes

- **Real salt solutions** have an effective van 't Hoff factor below the ideal value — about 1.8–1.9 for NaCl at 0.1–1 mol/kg — so the freezing point drop is a little smaller than calculated.
- The simple formulas are for **dilute** solutions. A 50% ethylene glycol antifreeze protects to about −37 °C, which the dilute formula cannot predict.
- To make a solution of a given molarity instead, use the [molarity calculator](/chemistry/molarity/); for freezing points of other solvents use the [freezing point depression calculator](/chemistry/freezing-point-depression/).
''')

# ---------------------------------------------------------------- Buoyancy
bV, brf, bm = 0.010, 1000.0, 8.0
bFb = brf * G * bV; bW = bm * G; bWa = bW - bFb; bro = bm / bV; bfs = min(bro / brf, 1)
FLU = (('Fresh water (4 °C)', 1000), ('Fresh water (20 °C)', 998.2), ('Seawater', 1025), ('Dead Sea water', 1240), ('Olive oil', 915), ('Petrol (gasoline)', 740), ('Mercury (20 °C)', 13546), ('Air (20 °C, 1 atm)', 1.204))
bf_rows = ''.join(f"| {nm} | {r:,g} kg/m³ | {r*G*1e-3:.4g} N | {r*1e-3:.4g} kg |\n" for nm, r in FLU)
OBJ = (('Balsa wood', 160), ('Pine wood', 500), ('Ice', 917), ('Human body (lungs full)', 985), ('Polyethylene (HDPE)', 950), ('Aluminium', 2700), ('Steel', 7850))
bo_rows = ''
for nm, r in OBJ:
    fw, fs = r / 1000, r / 1025
    st = lambda f: f"floats, {f*100:.0f}% submerged" if f < 1 else "sinks"
    bo_rows += f"| {nm} | {r:,} kg/m³ | {st(fw)} | {st(fs)} |\n"
W('physics/buoyancy', f'''
title: Buoyancy Calculator (Archimedes' Principle)
description: Calculate the buoyant force on an object in water or another fluid, its apparent weight and density, and whether and how deep it will float.
category: physics
{intro("An object in a fluid is pushed upward by a force equal to the weight of the fluid it displaces — Archimedes' principle. It explains why ships float, why balloons rise and why things feel lighter underwater. This buoyancy calculator gives the buoyant force, the object's weight and apparent weight, its average density and, if it floats, how much of it sits below the surface.")}
keywords: [buoyancy calculator, buoyant force calculator, archimedes principle calculator, will it float calculator, apparent weight in water, upthrust calculator, displacement calculator]
updated: {U}
variables:
  - {{ id: V, label: Volume of the object (fully submerged), family: volume, unit: L, imperialUnit: ft3, default: {bV*1000:g}, min: 0, help: 'For a partly submerged object, enter only the volume below the surface to get the buoyant force on it.' }}
  - {{ id: rf, label: Fluid density, family: density, unit: kgm3, imperialUnit: lbft3, default: {brf:g}, min: 0, help: 'Fresh water 1000, seawater 1025, air 1.2 kg/m³.' }}
  - {{ id: m, label: Object mass, family: mass, unit: kg, imperialUnit: lb, default: {bm:g}, min: 0 }}
  - {{ id: Fb, label: Buoyant force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: W, label: Weight in air, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: Wa, label: Apparent weight (negative = floats up), family: force, unit: N, imperialUnit: lbf }}
  - {{ id: ro, label: Average density of the object, family: density, unit: kgm3, imperialUnit: lbft3, min: 0 }}
  - {{ id: fs, label: Fraction submerged when floating (100% = sinks), family: percent, unit: '%', min: 0 }}
equations:
  - Fb = rf * g0 * V
  - W = m * g0
  - Wa = W - Fb
  - ro = m / V
  - fs = min(ro / rf, 1)
faq:
  - q: What is Archimedes' principle?
    a: A body wholly or partly immersed in a fluid is pushed upward by a force equal to the weight of the fluid it displaces, F_b = ρ_fluid × g × V_displaced. It applies to liquids and gases alike.
  - q: How do I know if something will float?
    a: Compare its average density with the fluid's. If the object is less dense it floats; if it is denser it sinks. In the calculator a negative apparent weight means the fully submerged object is pushed up and will rise to the surface.
  - q: How much of a floating object is underwater?
    a: The fraction submerged equals the object's density divided by the fluid's density. Ice at 917 kg/m³ floats with about 89% of its volume below the surface in seawater and about 92% in fresh water.
  - q: Why do steel ships float?
    a: The hull encloses a large volume of air, so the average density of the ship — steel, air and cargo together — is less than that of water. Loading the ship lowers it in the water until the displaced water again equals its total weight.
related: [physics/density, physics/pressure, engineering/hydrostatic-pressure, physics/weight]
''', f'''
## How to use the buoyancy calculator

Enter the **volume** of the object, the **density of the fluid** and the object's **mass**. The calculator gives the **buoyant force** when the object is fully submerged, its **weight**, its **apparent weight** underwater, its **average density** and, if it floats, the **fraction of its volume below the surface**. A negative apparent weight means the object floats up. To find the volume of an irregular object from a weighing in water, enter the apparent weight and press × on the volume.

## Buoyancy formulas

<p class="formula">F<sub>b</sub> = ρ<sub>fluid</sub> g V &nbsp;·&nbsp; W = m g &nbsp;·&nbsp; W<sub>apparent</sub> = W − F<sub>b</sub></p>

<p class="formula">ρ<sub>object</sub> = m ÷ V &nbsp;·&nbsp; fraction submerged = ρ<sub>object</sub> ÷ ρ<sub>fluid</sub> (if less than 1)</p>

## Worked example

A {bV*1000:g} L object with a mass of {bm:g} kg, held fully under fresh water ({brf:g} kg/m³):

- Buoyant force = {brf:g} × 9.80665 × {bV:g} = **{bFb:.2f} N**
- Weight = {bm:g} × 9.80665 = **{bW:.2f} N**
- Apparent weight = {bW:.2f} − {bFb:.2f} = **{bWa:.2f} N** — the object is pushed up and will float
- Average density = {bm:g} ÷ {bV:g} = **{bro:g} kg/m³**, so it floats with **{bfs*100:.0f}%** of its volume underwater

## Buoyant force per litre in common fluids

| Fluid | Density | Buoyant force per litre | Mass displaced per litre |
|---|---|---|---|
{bf_rows}
## Will it float?

| Material | Density | In fresh water | In seawater |
|---|---|---|---|
{bo_rows}
## Weighing in water

Weighing an object in air and then fully under water gives its density without measuring the volume: ρ<sub>object</sub> = ρ<sub>water</sub> × W<sub>air</sub> ÷ (W<sub>air</sub> − W<sub>water</sub>). Archimedes is said to have used this to test whether a crown was pure gold, and it is still used to measure body fat and the density of minerals.

## Practical notes

- **Balloons and airships** float in air for the same reason: the lift is (ρ<sub>air</sub> − ρ<sub>gas</sub>) × g × V, about 10.2 N (a lift of roughly 1 kg) per cubic metre of helium at 20 °C and sea-level pressure.
- **Level measurement:** displacer level transmitters work on buoyancy — the apparent weight of a long float falls as the liquid rises around it.
- Water density changes with temperature and salinity, so a ship floats a little higher in cold seawater than in warm fresh water; load lines on the hull mark the allowed draught for each.
''')

print(len(DONE), 'improved:', ' '.join(DONE))
