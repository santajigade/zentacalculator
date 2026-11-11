"""Batch 2026-11-11 — 6 calculators: engineering (cone-bottom tank volume, tank fill & drain time,
tank heater sizing), chemistry (Brix to specific gravity, integrated rate law), math (SSS triangle solver).
All reference tables are computed here; defaults match the worked examples."""
import sys, math, os, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro
D = '2026-11-11'
pi = math.pi
G = 9.80665
DESC = []
def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    t = re.search(r'^intro: (.*)$', fm, re.M).group(1)
    assert 'featured' not in fm
    DESC.append(slug)
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)  # typographic minus for negative numbers in the text
    page(cat, slug, fm, body)

# ======================================================================= ENGINEERING

# ---------------------------------------------------------------- Cone-bottom tank volume
def cone_tank(D_, H, hc, d, h):
    Vcone = pi * hc / 12 * (d * d + d * D_ + D_ * D_)
    Vt = Vcone + pi * D_ ** 2 / 4 * H
    y = min(h, hc)
    Ds = d + (D_ - d) * y / hc
    V = pi * y / 12 * (d * d + d * Ds + Ds * Ds) + pi * D_ ** 2 / 4 * min(max(h - hc, 0), H)
    ang = 2 * math.atan((D_ - d) / (2 * hc))
    wa = math.atan(2 * hc / (D_ - d))
    return Vcone, Vt, Ds, V, V / Vt, ang, wa
cD, cH, chc, cd, ch = 2.0, 3.0, 1.0, 0.1, 2.5
cVcone, cVt, cDs, cV, cpc, cang, cwa = cone_tank(cD, cH, chc, cd, ch)
cl_rows = ''
for lv in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0):
    r = cone_tank(cD, cH, chc, cd, lv)
    cl_rows += f"| {lv:g} m | {r[2]:.3f} m | {r[3]*1000:,.0f} L | {r[4]*100:.1f}% |\n"
cc_rows = ''
for Dm in (1.0, 1.5, 2.0, 3.0, 4.0):
    cells = []
    for inc in (60, 90, 120):
        hcone = (Dm / 2) / math.tan(math.radians(inc / 2))
        cells.append(f"{hcone:.3f} m / {pi*hcone/12*Dm**2*1000:,.0f} L")
    cc_rows += f"| {Dm:g} m | " + ' | '.join(cells) + " |\n"
P('engineering', 'cone-bottom-tank-volume', f'''
title: Cone Bottom Tank Volume Calculator (Level to Volume)
description: Calculate the liquid volume in a vertical tank with a conical bottom from its level, with total capacity, percent full, cone volume and cone angle.
category: engineering
{intro("Many process tanks, silos and hoppers have a conical bottom so they drain completely, which makes the level-to-volume relationship non-linear near the outlet. This cone bottom tank volume calculator works out the liquid volume for any level measured from the outlet, the total capacity, the percentage full, the volume held in the cone and the cone angle — the same strapping calculation used to set up [automatic tank gauging](ib:automatic-tank-gauging-explained) or a level transmitter.")}
keywords: [cone bottom tank volume calculator, conical bottom tank volume, cone tank volume calculator, hopper volume calculator, silo volume calculator, conical tank level to volume, tank with cone bottom capacity]
updated: {D}
variables:
  - {{ id: D, label: Tank inside diameter, family: length, unit: m, imperialUnit: ft, default: {cD:g}, min: 0 }}
  - {{ id: H, label: Height of the cylindrical part (straight side), family: length, unit: m, imperialUnit: ft, default: {cH:g}, min: 0 }}
  - {{ id: hc, label: Height of the cone, family: length, unit: m, imperialUnit: ft, default: {chc:g}, min: 0 }}
  - {{ id: d, label: Outlet diameter at the bottom of the cone, family: length, unit: m, imperialUnit: ft, default: {cd:g}, min: 0, help: 'Enter 0 for a cone that comes to a point.' }}
  - {{ id: h, label: Liquid level measured from the outlet, family: length, unit: m, imperialUnit: ft, default: {ch:g}, min: 0 }}
  - {{ id: V, label: Liquid volume, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: Vt, label: Total tank capacity, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: pc, label: Percent full, family: percent, unit: '%', min: 0 }}
  - {{ id: Vcone, label: Volume of the cone section, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: Ds, label: Diameter of the liquid surface, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: ang, label: Included cone angle, family: angle, unit: deg, min: 0 }}
  - {{ id: wa, label: Cone wall angle from horizontal, family: angle, unit: deg, min: 0 }}
equations:
  - Vcone = pi * hc / 12 * (d^2 + d * D + D^2)
  - Vt = Vcone + pi * D^2 / 4 * H
  - Ds = d + (D - d) * min(h, hc) / hc
  - V = pi * min(h, hc) / 12 * (d^2 + d * Ds + Ds^2) + pi * D^2 / 4 * min(max(h - hc, 0), H)
  - pc = V / Vt
  - ang = 2 * atan((D - d) / (2 * hc))
  - wa = atan(2 * hc / (D - d))
faq:
  - q: How do you calculate the volume of a cone bottom tank?
    a: Add the volume of the cone (a frustum if the outlet has a diameter) to the volume of the cylinder above it. The cone holds V = π h (d² + d D + D²) ÷ 12, where h is the cone height, D the tank diameter and d the outlet diameter; the cylinder holds π D² H ÷ 4. For d = 0 the cone formula becomes π D² h ÷ 12, one third of a cylinder of the same height.
  - q: How do you find the volume at a level inside the cone?
    a: The liquid forms a smaller cone (or frustum). Its surface diameter grows linearly from the outlet diameter at the bottom to the tank diameter at the top of the cone, so at level h it is d + (D − d) h ÷ h_cone, and the volume is π h (d² + d Dₛ + Dₛ²) ÷ 12.
  - q: Why is the volume not proportional to the level in a cone bottom tank?
    a: In the cone the cross-section grows with the square of the height, so the first 10% of the cone height holds only about 0.1% of the cone volume for a pointed cone. Above the cone the tank is a straight cylinder and every metre of level adds the same volume.
  - q: What cone angle should a hopper or tank bottom have?
    a: Liquid tanks often use a 60°–90° included angle (walls 45°–60° from horizontal). Hoppers for powders and granular solids usually need steeper walls, often 60°–70° from horizontal, for reliable mass flow — the exact angle depends on the wall friction of the material.
related: [engineering/vertical-tank-volume, engineering/horizontal-tank-volume, math/frustum-volume, engineering/tank-drain-time]
''', f'''
## How to use the cone bottom tank volume calculator

Enter the **inside diameter** of the tank, the **height of the straight cylindrical side**, the **height of the cone** and the **outlet diameter** at the bottom of the cone (0 for a pointed cone). Then enter the **liquid level measured from the outlet**. The calculator gives the liquid volume, the total capacity, the percentage full, the volume of the cone section, the diameter of the liquid surface and the cone angle. To find the level for a given volume, enter the volume and press × on the level.

## Cone bottom tank volume formulas

<p class="formula">V<sub>cone</sub> = π h<sub>c</sub> (d² + d D + D²) ÷ 12 &nbsp;·&nbsp; V<sub>total</sub> = V<sub>cone</sub> + π D² H ÷ 4</p>

<p class="formula">Level h ≤ h<sub>c</sub>: D<sub>s</sub> = d + (D − d) h ÷ h<sub>c</sub>, V = π h (d² + d D<sub>s</sub> + D<sub>s</sub>²) ÷ 12</p>

<p class="formula">Level h &gt; h<sub>c</sub>: V = V<sub>cone</sub> + π D² (h − h<sub>c</sub>) ÷ 4 &nbsp;·&nbsp; included angle = 2 atan[(D − d) ÷ (2 h<sub>c</sub>)]</p>

## Worked example

A tank {cD:g} m in diameter with a {cH:g} m straight side, a {chc:g} m deep cone and a {cd*1000:g} mm outlet, filled to {ch:g} m above the outlet:

- Cone volume = π × {chc:g} × ({cd:g}² + {cd:g} × {cD:g} + {cD:g}²) ÷ 12 = **{cVcone*1000:,.1f} L**
- Total capacity = {cVcone*1000:,.1f} + π × {cD:g}² × {cH:g} ÷ 4 × 1000 = **{cVt*1000:,.1f} L**
- The level is above the cone, so the liquid surface is the full **{cDs:g} m** diameter
- Liquid volume = {cVcone*1000:,.1f} + π × {cD:g}² × ({ch:g} − {chc:g}) ÷ 4 × 1000 = **{cV*1000:,.1f} L**
- Percent full = {cV*1000:,.1f} ÷ {cVt*1000:,.1f} = **{cpc*100:.2f}%**
- Included cone angle = 2 atan({cD-cd:g} ÷ {2*chc:g}) = **{math.degrees(cang):.2f}°**, so the walls slope at **{math.degrees(cwa):.2f}°** from horizontal

## Level to volume table for the example tank

| Level from outlet | Surface diameter | Volume | Percent full |
|---|---|---|---|
{cl_rows}
The first quarter of the cone height holds very little liquid — which is why level transmitters on cone bottom tanks need a strapping table rather than a linear scale.

## Cone height and volume for common cone angles

Pointed cones (outlet diameter 0); each cell gives the cone height and the volume it holds.

| Tank diameter | 60° included angle | 90° included angle | 120° included angle |
|---|---|---|---|
{cc_rows}
## Practical notes

- **Measure the level from the true bottom:** a level transmitter mounted on the cone or the straight side has a zero offset — add the height of its tapping above the outlet before using this calculator.
- **Dead volume:** liquid in the outlet nozzle and pipe below the cone is not included.
- For a flat-bottomed vertical tank use the [vertical tank volume calculator](/engineering/vertical-tank-volume/); for a horizontal drum use the [horizontal tank volume calculator](/engineering/horizontal-tank-volume/).
- **Solids:** for powders in a silo, the top surface forms a heap at the angle of repose instead of a flat surface, and the bulk density varies with compaction, so treat the result as an estimate.
''')

# ---------------------------------------------------------------- Tank fill and drain time (Torricelli)
def drain(D_, d, Cd, h1, h2, Qf):
    At = pi * D_ ** 2 / 4; a = pi * d ** 2 / 4
    t = At / (Cd * a) * math.sqrt(2 / G) * (math.sqrt(h1) - math.sqrt(h2))
    Q1 = Cd * a * math.sqrt(2 * G * h1); Q2 = Cd * a * math.sqrt(2 * G * h2)
    Vd = At * (h1 - h2)
    return At, a, t, Q1, Q2, Vd, (Vd / t if t else 0), Vd / Qf
tD, td, tCd, th1, th2, tQf = 2.0, 0.05, 0.61, 3.0, 0.2, 10 / 3600
tAt, ta, tt, tQ1, tQ2, tVd, tQa, ttf = drain(tD, td, tCd, th1, th2, tQf)
td_rows = ''
for Dm in (1.0, 2.0, 3.0, 5.0):
    cells = []
    for dmm in (25, 50, 100, 150):
        r = drain(Dm, dmm / 1000, 0.61, 3.0, 0.0, 1)
        cells.append(f"{r[2]/60:,.1f} min")
    td_rows += f"| {Dm:g} m | " + ' | '.join(cells) + " |\n"
tl_rows = ''
tot = drain(tD, td, tCd, th1, 0.0, 1)[2]
for lv in (3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.2, 0.0):
    tl_rows += f"| {lv:g} m | {drain(tD, td, tCd, th1, lv, 1)[2]/60:.1f} min | {tCd*ta*math.sqrt(2*G*lv)*3600:.2f} m³/h |\n"
P('engineering', 'tank-drain-time', f'''
title: Tank Drain Time Calculator (Fill & Empty Time)
description: Calculate how long a tank takes to drain by gravity through a bottom outlet (Torricelli's law), the outflow rate, and the time to fill it at a set flow.
category: engineering
{intro("A tank emptying through a hole or short nozzle in its bottom slows down as it drains, because the outflow velocity depends on the square root of the liquid head. This tank drain time calculator integrates Torricelli's law to give the time to drop from one level to another, the starting and final outflow and the volume drained, and also the time needed to fill the same volume at a constant inflow.")}
keywords: [tank drain time calculator, tank draining time, time to empty a tank, torricelli law calculator, tank fill time calculator, gravity drain time, orifice discharge time]
updated: {D}
variables:
  - {{ id: D, label: Tank inside diameter (vertical cylinder), family: length, unit: m, imperialUnit: ft, default: {tD:g}, min: 0 }}
  - {{ id: d, label: Outlet (orifice) diameter, family: length, unit: mm, imperialUnit: in, default: {td*1000:g}, min: 0 }}
  - id: Cd
    label: Discharge coefficient of the outlet
    default: {tCd:g}
    options:
      - {{ label: '0.61 — sharp-edged hole in a thin bottom plate', value: 0.61 }}
      - {{ label: '0.82 — short tube or nozzle (2–3 diameters long)', value: 0.82 }}
      - {{ label: '0.97 — well-rounded (bell-mouth) outlet', value: 0.97 }}
      - {{ label: '0.50 — re-entrant tube projecting into the tank', value: 0.5 }}
  - {{ id: h1, label: Starting liquid level above the outlet, family: length, unit: m, imperialUnit: ft, default: {th1:g}, min: 0 }}
  - {{ id: h2, label: Final liquid level above the outlet, family: length, unit: m, imperialUnit: ft, default: {th2:g}, min: 0, help: 'Enter 0 to empty the tank completely.' }}
  - {{ id: Qf, label: Fill flow rate (for the fill time), family: flow, unit: m3h, imperialUnit: gpm, default: {tQf*3600:g}, min: 0 }}
  - {{ id: t, label: Drain time from h1 to h2, family: seconds, unit: min, min: 0 }}
  - {{ id: Q1, label: Outflow at the start, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: Q2, label: Outflow at the end, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: Vd, label: Volume drained, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: Qa, label: Average outflow, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: tf, label: Time to fill from h2 to h1 (outlet closed), family: seconds, unit: min, min: 0 }}
equations:
  - t = (pi * D^2 / 4) / (Cd * pi * d^2 / 4) * sqrt(2 / g0) * (sqrt(h1) - sqrt(h2))
  - Q1 = Cd * pi * d^2 / 4 * sqrt(2 * g0 * h1)
  - Q2 = Cd * pi * d^2 / 4 * sqrt(2 * g0 * h2)
  - Vd = pi * D^2 / 4 * (h1 - h2)
  - Qa = Vd / t
  - tf = Vd / Qf
faq:
  - q: How do you calculate the time to drain a tank?
    a: For a vertical cylindrical tank open to the atmosphere and emptying through a bottom outlet, Torricelli's law gives the outflow Q = C_d a √(2 g h). Integrating as the level falls gives t = (A ÷ (C_d a)) × √(2 ÷ g) × (√h₁ − √h₂), where A is the tank cross-section and a the outlet area.
  - q: Why does a tank drain more slowly as it empties?
    a: The outflow velocity is √(2 g h), so it falls as the head h drops. Draining the bottom quarter of the height takes as long as draining the top three quarters, and emptying a tank from full takes twice as long as it would at the starting flow rate.
  - q: What discharge coefficient should I use?
    a: About 0.61 for a sharp-edged hole in a thin plate, 0.8–0.82 for a short tube or nozzle, 0.95–0.98 for a smooth bell-mouthed outlet and about 0.5 for a tube projecting into the tank. If the tank drains through a long pipe or a valve, the pipe friction controls the flow and the coefficient is much lower.
  - q: How is the fill time calculated?
    a: With a constant inflow and the outlet closed, the fill time is simply the volume between the two levels divided by the flow rate. If the outlet stays open, the level rises only until the outflow √(2 g h) term equals the inflow.
related: [engineering/orifice-flow, engineering/vertical-tank-volume, engineering/cone-bottom-tank-volume, engineering/residence-time]
''', f'''
## How to use the tank drain time calculator

Enter the **inside diameter** of the vertical tank, the **diameter of the outlet** and its type (which sets the **discharge coefficient**), and the **starting and final levels** measured above the outlet. The calculator gives the **drain time**, the outflow at the start and the end, the volume drained and the average flow. Enter a **fill flow rate** to see how long it takes to fill the same volume back up with the outlet closed. To find the outlet size for a required drain time, enter the time and press × on the outlet diameter.

## Tank drain time formula (Torricelli's law)

<p class="formula">Q = C<sub>d</sub> a √(2 g h) &nbsp;·&nbsp; t = (A ÷ C<sub>d</sub> a) × √(2 ÷ g) × (√h<sub>1</sub> − √h<sub>2</sub>)</p>

<p class="formula">Fill time = A (h<sub>1</sub> − h<sub>2</sub>) ÷ Q<sub>fill</sub></p>

A = π D² ÷ 4 is the tank cross-section, a = π d² ÷ 4 the outlet area and g = 9.80665 m/s². The formula assumes a constant cross-section, a tank open to the atmosphere (or vented) and an outlet discharging freely to atmosphere.

## Worked example

A {tD:g} m diameter tank with a {td*1000:g} mm sharp-edged bottom outlet (C<sub>d</sub> = {tCd:g}) drains from {th1:g} m to {th2:g} m:

- Tank area A = π × {tD:g}² ÷ 4 = {tAt:.4f} m²; outlet area a = π × {td:g}² ÷ 4 = {ta*1e4:.3f} cm²
- Drain time = ({tAt:.4f} ÷ ({tCd:g} × {ta:.7f})) × √(2 ÷ 9.80665) × (√{th1:g} − √{th2:g}) = {tt:,.0f} s = **{tt/60:.2f} min**
- Outflow at the start = {tCd:g} × {ta:.7f} × √(2 × 9.80665 × {th1:g}) × 3600 = **{tQ1*3600:.2f} m³/h**, falling to **{tQ2*3600:.2f} m³/h** at {th2:g} m
- Volume drained = {tAt:.4f} × ({th1:g} − {th2:g}) = **{tVd*1000:,.0f} L**, an average of **{tQa*3600:.2f} m³/h**
- Filling it back at {tQf*3600:g} m³/h takes {tVd:.4f} ÷ {tQf*3600:g} = **{ttf/60:.2f} min**

## Level against time for the example tank

Time from {th1:g} m to each level, and the outflow at that level ({td*1000:g} mm sharp-edged outlet):

| Level | Time from {th1:g} m | Outflow |
|---|---|---|
{tl_rows}
Emptying completely takes {tot/60:.1f} min — the last {th2:g} m alone takes {(tot-tt)/60:.1f} min.

## Time to empty a tank from 3 m

Sharp-edged outlet (C<sub>d</sub> = 0.61), starting 3 m above the outlet:

| Tank diameter | 25 mm outlet | 50 mm outlet | 100 mm outlet | 150 mm outlet |
|---|---|---|---|---|
{td_rows}
Doubling the outlet diameter cuts the time by four; doubling the tank diameter multiplies it by four.

## Practical notes

- **Drain lines and valves:** if the tank empties through a pipe, the friction and fittings reduce the flow. Use the [orifice flow calculator](/engineering/orifice-flow/) or a pipe pressure-drop calculation for the real outflow; a pipe that drops below the tank adds head and can speed up draining.
- **Closed tanks** need a vent sized for the outflow, otherwise the vacuum above the liquid slows or stops draining.
- **Cone or dished bottoms** hold extra liquid below the straight side; for a [cone bottom tank](/engineering/cone-bottom-tank-volume/) the last part drains faster than this formula predicts because the area shrinks.
- Vortexing near the end of draining can draw air into the outlet and reduce the flow further.
''')

# ---------------------------------------------------------------- Tank heater sizing
def heater(V, rho, cp, T1, T2, th, U, A, Ta, eff, Vs, ph):
    m = V * rho
    E = m * cp * 1000 * (T2 - T1)
    Ph = E / th
    Pl = U * A * ((T1 + T2) / 2 - Ta)
    Pr = (Ph + Pl) / eff
    Phold = U * A * (T2 - Ta) / eff
    I = Pr / (Vs * ph)
    return m, E, Ph, Pl, Pr, Phold, I
hV, hrho, hcp, hT1, hT2, hth, hU, hA, hTa, heff, hVs, hph = 2.0, 1000.0, 4.186, 15.0, 60.0, 3 * 3600, 0.8, 10.0, 15.0, 1.0, 415.0, math.sqrt(3)
hm, hE, hPh, hPl, hPr, hPhold, hI = heater(hV, hrho, hcp, hT1, hT2, hth, hU, hA, hTa, heff, hVs, hph)
hk_rows = ''
for L in (100, 200, 500, 1000, 2000, 5000):
    cells = []
    for hr in (0.5, 1, 2, 4):
        cells.append(f"{L*4.186*40/(hr*3600):,.1f} kW")
    hk_rows += f"| {L:,} L | " + ' | '.join(cells) + " |\n"
FL = (('Water', 1000, 4.186), ('Seawater', 1025, 3.99), ('Ethylene glycol 50% (v/v)', 1070, 3.35), ('Light fuel oil', 870, 1.9), ('Vegetable oil', 920, 2.0), ('Milk', 1030, 3.93))
hf_rows = ''.join(f"| {nm} | {r:,} kg/m³ | {c:g} kJ/kg·K | {r*c/3600:.3f} kWh |\n" for nm, r, c in FL)
P('engineering', 'tank-heater-sizing', f'''
title: Tank Heater Sizing Calculator (kW to Heat a Tank)
description: Calculate the heater kW needed to heat a tank of liquid in a set time, including heat loss, holding power, energy in kWh and the supply current.
category: engineering
{intro("The heater for a process tank, hot-water cylinder or oil heating tank must supply the sensible heat of the liquid in the heat-up time and make up the heat lost through the walls while it warms. This tank heater sizing calculator works out the energy needed, the heat-up power, the average heat loss, the total heater kW, the power needed to hold the temperature and the current drawn on a single- or three-phase supply.")}
keywords: [tank heater sizing calculator, heater kw calculation for tank, immersion heater sizing, tank heating calculation, kw required to heat water, heating time calculator, water heating power calculator]
updated: {D}
variables:
  - {{ id: V, label: Liquid volume, family: volume, unit: L, imperialUnit: galUS, default: {hV*1000:g}, min: 0 }}
  - {{ id: rho, label: Liquid density, family: density, unit: kgm3, imperialUnit: lbft3, default: {hrho:g}, min: 0 }}
  - {{ id: cp, label: Specific heat of the liquid, suffix: kJ/kg·K, default: {hcp:g}, min: 0, help: 'Water 4.186, oils about 1.9–2.1, 50% glycol about 3.3.' }}
  - {{ id: T1, label: Starting temperature, family: temperature, unit: C, imperialUnit: F, default: {hT1:g} }}
  - {{ id: T2, label: Final temperature, family: temperature, unit: C, imperialUnit: F, default: {hT2:g} }}
  - {{ id: th, label: Heat-up time, family: seconds, unit: h, default: {hth/3600:g}, min: 0 }}
  - {{ id: U, label: Heat loss coefficient of the tank wall, suffix: W/m²·K, default: {hU:g}, min: 0, help: 'About 0.5–1 for an insulated tank, 5–12 for bare steel in still air.' }}
  - {{ id: A, label: Outside surface area of the tank, family: area, unit: m2, imperialUnit: ft2, default: {hA:g}, min: 0 }}
  - {{ id: Ta, label: Ambient temperature, family: temperature, unit: C, imperialUnit: F, default: {hTa:g} }}
  - {{ id: eff, label: Heater efficiency, family: percent, unit: '%', default: {heff*100:g}, min: 0, help: 'Electric immersion heaters put practically all their power into the liquid.' }}
  - {{ id: Vs, label: Supply voltage (line-to-line for three-phase), family: voltage, unit: V, default: {hVs:g}, min: 0 }}
  - id: ph
    label: Supply
    default: {hph}
    options:
      - {{ label: Three-phase, value: {hph} }}
      - {{ label: Single-phase, value: 1 }}
  - {{ id: m, label: Mass of liquid, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
  - {{ id: E, label: Heat to raise the temperature, family: energy, unit: kWh, min: 0 }}
  - {{ id: Ph, label: Heat-up power (no losses), family: power, unit: kW, imperialUnit: BTUh, min: 0 }}
  - {{ id: Pl, label: Average heat loss during heat-up, family: power, unit: kW, imperialUnit: BTUh }}
  - {{ id: Pr, label: Required heater power, family: power, unit: kW, imperialUnit: BTUh, min: 0 }}
  - {{ id: Phold, label: Power to hold the final temperature, family: power, unit: kW, imperialUnit: BTUh }}
  - {{ id: I, label: Heater current at full power, family: current, unit: A, min: 0 }}
equations:
  - m = V * rho
  - E = m * cp * 1000 * (T2 - T1)
  - Ph = E / th
  - Pl = U * A * ((T1 + T2) / 2 - Ta)
  - Pr = (Ph + Pl) / eff
  - Phold = U * A * (T2 - Ta) / eff
  - I = Pr / (Vs * ph)
faq:
  - q: How do you calculate the heater kW needed to heat a tank?
    a: Heater power = m × cp × ΔT ÷ t plus the heat lost while heating, divided by the heater efficiency. For water, heating 1,000 L by 1 °C takes 1.163 kWh, so 1,000 L from 15 °C to 60 °C needs about 52 kWh — 26 kW for a two-hour heat-up before losses.
  - q: How long will a heater take to heat a tank?
    a: Time = m × cp × ΔT ÷ (heater power − heat loss). Enter your heater power in the required-power field and press × on the heat-up time to have the calculator solve for it.
  - q: How much heat does a tank lose?
    a: Heat loss = U × A × (liquid temperature − ambient). An insulated tank with U ≈ 0.8 W/m²·K loses very little, but a bare steel tank at 60 °C in still air (U ≈ 8–10 W/m²·K) can lose about 0.4 kW per square metre of surface, and wind or an outdoor location increases this further.
  - q: Should I add a safety margin to the heater size?
    a: Yes — a margin of 10–20% is common to cover low supply voltage (heater output falls with the square of the voltage), scaling of the element, uncertain losses and an open tank surface. Open tanks lose a lot of heat by evaporation, which this calculator does not include.
related: [engineering/heat-duty, chemistry/specific-heat, engineering/convection-heat-transfer, electrical/kw-to-amps]
''', f'''
## How to use the tank heater sizing calculator

Enter the **volume**, **density** and **specific heat** of the liquid, the **starting and final temperatures** and the **heat-up time** you need. Add the tank's **heat loss coefficient**, **outside surface area** and the **ambient temperature** to include losses, the **heater efficiency**, and the **supply voltage and phases** to get the current. The calculator gives the heat energy, the heat-up power, the average heat loss, the **required heater power**, the power needed to hold the tank at temperature and the current. To find the heat-up time for a heater you already have, enter its kW in the required-power field and press × on the heat-up time.

## Tank heating formulas

<p class="formula">E = m c<sub>p</sub> (T<sub>2</sub> − T<sub>1</sub>) &nbsp;·&nbsp; P<sub>heat-up</sub> = E ÷ t</p>

<p class="formula">P<sub>loss</sub> = U A [(T<sub>1</sub> + T<sub>2</sub>) ÷ 2 − T<sub>a</sub>] &nbsp;·&nbsp; P = (P<sub>heat-up</sub> + P<sub>loss</sub>) ÷ η</p>

<p class="formula">P<sub>hold</sub> = U A (T<sub>2</sub> − T<sub>a</sub>) ÷ η &nbsp;·&nbsp; I = P ÷ (√3 V) three-phase, I = P ÷ V single-phase</p>

The loss during heat-up uses the average liquid temperature, a good approximation when the losses are small compared with the heater power.

## Worked example

A {hV*1000:,.0f} L insulated water tank (U = {hU:g} W/m²·K, {hA:g} m² of surface) is heated from {hT1:g} °C to {hT2:g} °C in {hth/3600:g} hours by an immersion heater on a {hVs:g} V three-phase supply; the room is at {hTa:g} °C:

- Mass = {hV:g} m³ × {hrho:g} kg/m³ = **{hm:,.0f} kg**
- Heat = {hm:,.0f} × {hcp:g} × ({hT2:g} − {hT1:g}) = {hE/1e6:.2f} MJ = **{hE/3.6e6:.2f} kWh**
- Heat-up power = {hE/3.6e6:.2f} kWh ÷ {hth/3600:g} h = **{hPh/1000:.2f} kW**
- Average loss = {hU:g} × {hA:g} × ({(hT1+hT2)/2:g} − {hTa:g}) = **{hPl/1000:.3f} kW**
- Required heater power = ({hPh/1000:.2f} + {hPl/1000:.3f}) ÷ {heff:g} = **{hPr/1000:.2f} kW** — choose a 36 or 40 kW heater with a margin
- Holding power at {hT2:g} °C = {hU:g} × {hA:g} × ({hT2:g} − {hTa:g}) = **{hPhold/1000:.3f} kW**
- Current = {hPr:,.0f} ÷ (√3 × {hVs:g}) = **{hI:.2f} A**

## Heater kW to heat water by 40 °C

Water (4.186 kJ/kg·K), no heat losses:

| Volume | 30 min | 1 hour | 2 hours | 4 hours |
|---|---|---|---|---|
{hk_rows}
## Energy to heat 1,000 L by 1 °C

| Liquid | Density | Specific heat | Energy per 1,000 L per °C |
|---|---|---|---|
{hf_rows}
## Practical notes

- **Element watt density:** keep the surface loading of immersion elements low for viscous oils and sugar solutions (often below 2–3 W/cm²) to avoid coking or scorching; water heaters can run at about 8–10 W/cm².
- **Thermostat and over-temperature cut-out:** the heater should be controlled by a thermostat or a temperature controller and protected by an independent high-limit cut-out and a low-level interlock, so it never runs dry.
- **Voltage:** a resistive heater's power falls with the square of the voltage — a heater rated at 415 V gives only about 90% of its kW at 394 V.
- For flowing liquids (heat exchangers, inline heaters) use the [heat duty calculator](/engineering/heat-duty/) with the mass flow rate instead of a volume and time.
''')

# ======================================================================= CHEMISTRY

# ---------------------------------------------------------------- Brix to specific gravity
RW = 998.2
def brix_sg(B):
    return 1 + B / (258.6 - B / 258.2 * 227.1)
bB = 12.0
def bx_of(sg):
    lo, hi = 0.0, 85.0
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if brix_sg(mid) < sg else (lo, mid)
    return lo
bSG = brix_sg(bB); brho = bSG * RW; bBe = 145 - 145 / bSG; bTw = 200 * (bSG - 1); bsug = bB / 100 * brho
bt_rows = ''
for B in (0, 2, 5, 8, 10, 12, 15, 20, 25, 30, 40, 50):
    s = brix_sg(B)
    bt_rows += f"| {B} °Bx | {s:.4f} | {s*RW:,.1f} kg/m³ | {145-145/s:.2f} °Bé | {200*(s-1):.1f} °Tw | {B/100*s*RW:,.1f} g/L |\n"
PROD = (('Sugarcane juice (raw)', 16, 22), ('Grape must for wine', 20, 25), ('Orange juice', 10, 13), ('Apple juice', 10, 13), ('Beer wort (original gravity)', 10, 18), ('Cola soft drink', 10, 11), ('Honey', 79, 83))
bp_rows = ''.join(f"| {nm} | {a}–{b} °Bx |\n" for nm, a, b in PROD)
P('chemistry', 'brix-specific-gravity', f'''
title: Brix to Specific Gravity Calculator (°Bx, °Bé, °Tw)
description: Convert degrees Brix to specific gravity and density and back, with Baumé, Twaddell and sugar content in g/L, for juices, wort, syrups and sugar solutions.
category: chemistry
{intro("Degrees Brix is the sugar content of a solution as percent sucrose by mass, and it is linked to the solution's density, which is why refractometers and hydrometers read in °Bx. This Brix to specific gravity calculator converts °Bx to specific gravity, density, degrees Baumé and degrees Twaddell, and gives the sugar content in grams per litre — or works backwards from a measured [specific gravity](ib:what-is-specific-gravity) or a density reading from an inline [Coriolis density meter](ib:coriolis-density-measurement).")}
keywords: [brix to specific gravity calculator, specific gravity to brix, brix to density, brix calculator, baume to specific gravity, degrees brix conversion, twaddell to specific gravity]
updated: {D}
variables:
  - {{ id: Bx, label: Degrees Brix, suffix: °Bx, default: {bB:g}, min: 0, max: 85, decimals: 2 }}
  - {{ id: SG, label: Specific gravity (20/20 °C), min: 0, decimals: 5 }}
  - {{ id: rhow, label: Density of water at the reference temperature, family: density, unit: kgm3, imperialUnit: lbft3, default: {RW:g}, min: 0, help: '998.2 kg/m³ at 20 °C; 999.0 kg/m³ at 15.6 °C (60 °F).' }}
  - {{ id: rho, label: Solution density, family: density, unit: kgm3, imperialUnit: lbft3, min: 0 }}
  - {{ id: Be, label: 'Degrees Baumé (heavy liquids, 145 scale)', suffix: °Bé, decimals: 2 }}
  - {{ id: Tw, label: Degrees Twaddell, suffix: °Tw, decimals: 2 }}
  - {{ id: sug, label: Sugar (sucrose) content, suffix: g/L, min: 0, decimals: 1 }}
equations:
  - SG = 1 + Bx / (258.6 - Bx / 258.2 * 227.1)
  - rho = SG * rhow
  - Be = 145 - 145 / SG
  - Tw = 200 * (SG - 1)
  - sug = Bx / 100 * rho
faq:
  - q: How do you convert Brix to specific gravity?
    a: A widely used fit to the sucrose tables is SG = 1 + °Bx ÷ (258.6 − °Bx ÷ 258.2 × 227.1), for specific gravity at 20 °C relative to water at 20 °C. It agrees with the standard sucrose tables to within about 0.001 in specific gravity (roughly 0.2 °Bx) over the usual 0–60 °Bx range. A quick rule of thumb is SG ≈ 1 + °Bx ÷ 250.
  - q: What is the difference between Brix, Plato and Baumé?
    a: Brix and Plato are both percent sucrose by mass and differ only in the fourth decimal place, so brewers use them interchangeably. Baumé is a hydrometer scale — SG = 145 ÷ (145 − °Bé) for liquids heavier than water — and 1 °Bé is roughly 1.8 °Bx for sugar solutions.
  - q: How do I convert specific gravity to Brix?
    a: Enter the specific gravity and press × on the Brix field — the calculator solves the same equation backwards. For example, SG 1.040 is about {bx_of(1.04):.1f} °Bx and SG 1.080 about {bx_of(1.08):.1f} °Bx.
  - q: Does Brix measure sugar in fruit juice exactly?
    a: Only for pure sucrose solutions. In juices, wine must and syrups the other dissolved solids — acids, minerals and other sugars — also raise the density and refractive index, so °Bx is an estimate of total soluble solids rather than an exact sugar content.
related: [engineering/api-gravity, physics/density, chemistry/mass-percent, chemistry/dilution]
''', f'''
## How to use the Brix to specific gravity calculator

Enter the **degrees Brix** from a refractometer or a Brix hydrometer. The calculator gives the **specific gravity** at 20/20 °C, the **density** of the solution, the equivalent **degrees Baumé** and **degrees Twaddell**, and the **sugar content** in grams per litre. To convert the other way, enter a specific gravity, density, Baumé or Twaddell value and press × on the Brix field. Change the water density only if your specific gravity uses a different reference temperature.

## Brix, specific gravity, Baumé and Twaddell formulas

<p class="formula">SG = 1 + °Bx ÷ (258.6 − °Bx ÷ 258.2 × 227.1) &nbsp;·&nbsp; ρ = SG × ρ<sub>water</sub></p>

<p class="formula">°Bé = 145 − 145 ÷ SG &nbsp;·&nbsp; °Tw = 200 (SG − 1) &nbsp;·&nbsp; sugar (g/L) = °Bx ÷ 100 × ρ (kg/m³)</p>

For liquids lighter than water the Baumé scale is SG = 140 ÷ (130 + °Bé), and petroleum products use [API gravity](/engineering/api-gravity/) instead.

## Worked example

A juice reads **{bB:g} °Bx** on a refractometer:

- SG = 1 + {bB:g} ÷ (258.6 − {bB:g} ÷ 258.2 × 227.1) = 1 + {bB:g} ÷ {258.6 - bB/258.2*227.1:.3f} = **{bSG:.5f}**
- Density = {bSG:.5f} × {RW:g} = **{brho:,.1f} kg/m³**
- Baumé = 145 − 145 ÷ {bSG:.5f} = **{bBe:.2f} °Bé**; Twaddell = 200 × ({bSG:.5f} − 1) = **{bTw:.2f} °Tw**
- Sugar content = {bB:g} ÷ 100 × {brho:,.1f} = **{bsug:.1f} g/L**

## Brix to specific gravity table

| Brix | Specific gravity (20/20 °C) | Density | Baumé | Twaddell | Sugar |
|---|---|---|---|---|---|
{bt_rows}
## Typical Brix values

| Product | Typical Brix |
|---|---|
{bp_rows}
## Practical notes

- **Temperature:** refractometers and hydrometers are calibrated at 20 °C; a reading taken warmer reads low (roughly 0.05–0.08 °Bx per °C near room temperature for sugar solutions). Use automatic temperature compensation or correct the reading.
- **Fermenting liquids:** alcohol lowers both density and refractive index, so a refractometer reading on fermenting wort or wine must be corrected before converting it.
- **Inline measurement:** in sugar mills, dairies and juice plants Brix is measured continuously with density meters or process refractometers, and the density is converted to Brix with the same sucrose tables.
- To dilute a concentrate to a target Brix, use mass balance: m₁ × Bx₁ = m₂ × Bx₂ — or the [dilution calculator](/chemistry/dilution/) for a quick estimate.
''')

# ---------------------------------------------------------------- Integrated rate law
def rate(n, A0, k, t):
    I0, I1, I2 = (1 - n) * (2 - n) / 2, n * (2 - n), n * (n - 1) / 2
    A = I0 * max(A0 - k * t, 0) + I1 * A0 * math.exp(-k * t) + I2 * A0 / (1 + k * t * A0)
    th = I0 * A0 / (2 * k) + I1 * math.log(2) / k + I2 / (k * A0)
    return A, A / A0, 1 - A / A0, th, k * A ** n
rn, rA0, rk, rt = 1, 0.5, 1.0e-3, 600.0
rA, rf, rX, rth, rr = rate(rn, rA0, rk, rt)
r0 = rate(0, rA0, 1e-4, rt); r2 = rate(2, rA0, 2e-3, rt)
rh_rows = ''
for m in (0.5, 1, 2, 3, 4, 5, 7, 10):
    rh_rows += f"| {m:g} | {100*0.5**m:.3g}% | {100*(1-0.5**m):.3g}% |\n"
# three orders with the same initial half-life (A0 = 1 M, t½ = 10 min)
ro_rows = ''
th0 = 600.0
k0, k1, k2 = 1 / (2 * th0), math.log(2) / th0, 1 / th0
for tm in (0, 5, 10, 20, 30, 40):
    ts = tm * 60
    ro_rows += f"| {tm} min | {rate(0, 1, k0, ts)[0]:.3f} M | {rate(1, 1, k1, ts)[0]:.3f} M | {rate(2, 1, k2, ts)[0]:.3f} M |\n"
P('chemistry', 'integrated-rate-law', f'''
title: Integrated Rate Law Calculator (Zero, First & Second Order)
description: Calculate reactant concentration after a time for zero, first and second order reactions, with half-life, conversion, rate and time to reach a target.
category: chemistry
{intro("The integrated rate law tells you how the concentration of a reactant falls with time, and its form depends on the reaction order: linear for zero order, exponential for first order and hyperbolic for second order. This integrated rate law calculator gives the remaining concentration, the fraction converted, the half-life and the rate at any time for all three orders, and can solve for the time, rate constant or starting concentration instead.")}
keywords: [integrated rate law calculator, rate law calculator, first order reaction calculator, second order reaction calculator, zero order reaction, reaction half life calculator, concentration after time]
updated: {D}
variables:
  - id: n
    label: Reaction order
    default: {rn}
    options:
      - {{ label: 'Zero order — rate = k', value: 0 }}
      - {{ label: 'First order — rate = k[A]', value: 1 }}
      - {{ label: 'Second order — rate = k[A]²', value: 2 }}
  - {{ id: A0, label: Initial concentration [A]₀, suffix: mol/L, default: {rA0:g}, min: 0 }}
  - {{ id: k, label: 'Rate constant k (per second: M/s, 1/s or 1/(M·s))', default: {rk:g}, min: 0, help: 'Zero order: mol L⁻¹ s⁻¹; first order: s⁻¹; second order: L mol⁻¹ s⁻¹. Convert a per-minute constant by dividing by 60.' }}
  - {{ id: t, label: Time elapsed, family: seconds, unit: min, default: {rt/60:g}, min: 0 }}
  - {{ id: A, label: 'Concentration remaining [A]', suffix: mol/L, min: 0, decimals: 5 }}
  - {{ id: f, label: Fraction remaining [A] ÷ [A]₀, family: percent, unit: '%', min: 0 }}
  - {{ id: X, label: Conversion (fraction reacted), family: percent, unit: '%', min: 0 }}
  - {{ id: th, label: Half-life (from [A]₀), family: seconds, unit: min, min: 0 }}
  - {{ id: r, label: 'Rate at time t, −d[A]/dt', suffix: mol/(L·s), min: 0, decimals: 7 }}
equations:
  - A = (1 - n) * (2 - n) / 2 * max(A0 - k * t, 0) + n * (2 - n) * A0 * exp(-k * t) + n * (n - 1) / 2 * A0 / (1 + k * t * A0)
  - f = A / A0
  - X = 1 - A / A0
  - th = (1 - n) * (2 - n) / 2 * A0 / (2 * k) + n * (2 - n) * ln(2) / k + n * (n - 1) / 2 / (k * A0)
  - r = k * A^n
faq:
  - q: What are the integrated rate laws?
    a: Zero order [A] = [A]₀ − k t; first order ln[A] = ln[A]₀ − k t, so [A] = [A]₀ e^(−kt); second order 1/[A] = 1/[A]₀ + k t. Plotting [A], ln[A] or 1/[A] against time gives a straight line of slope −k, −k or +k respectively, which is how the order is found from experimental data.
  - q: How do you calculate the half-life of a reaction?
    a: For first order t½ = ln 2 ÷ k = 0.693 ÷ k, independent of concentration. For zero order t½ = [A]₀ ÷ (2k), and for second order t½ = 1 ÷ (k [A]₀) — both depend on the starting concentration, so successive half-lives get shorter (zero order) or longer (second order).
  - q: How do I find the time to reach a certain concentration?
    a: Enter the target concentration in the [A] field and press × on the time — the calculator solves the rate law for t. For first order, t = ln([A]₀ ÷ [A]) ÷ k; for second order t = (1/[A] − 1/[A]₀) ÷ k.
  - q: What are the units of the rate constant?
    a: They depend on the order so that the rate always comes out in mol L⁻¹ s⁻¹ — mol L⁻¹ s⁻¹ for zero order, s⁻¹ for first order and L mol⁻¹ s⁻¹ for second order. In general the units are (mol/L)^(1−n) s⁻¹.
related: [chemistry/half-life, chemistry/arrhenius-equation, chemistry/activation-energy, chemistry/equilibrium-constant]
''', f'''
## How to use the integrated rate law calculator

Choose the **reaction order**, then enter the **initial concentration**, the **rate constant** (always per second) and the **time elapsed**. The calculator gives the **concentration remaining**, the fraction remaining and converted, the **half-life** measured from the starting concentration and the **rate** at that moment. To find the time to reach a given concentration, enter it in the [A] field and press × on the time; the same works for the rate constant or the starting concentration.

## Integrated rate law equations

| Order | Rate law | Integrated form | Straight-line plot | Half-life |
|---|---|---|---|---|
| Zero | rate = k | [A] = [A]₀ − k t | [A] vs t, slope −k | [A]₀ ÷ 2k |
| First | rate = k[A] | [A] = [A]₀ e<sup>−kt</sup> | ln[A] vs t, slope −k | ln 2 ÷ k |
| Second | rate = k[A]² | 1/[A] = 1/[A]₀ + k t | 1/[A] vs t, slope +k | 1 ÷ (k[A]₀) |

The second-order form is for a single reactant (2A → products) or for A + B with equal starting concentrations.

## Worked example

A first-order decomposition with k = {rk:g} s⁻¹ starts at [A]₀ = {rA0:g} mol/L. After {rt/60:g} min ({rt:g} s):

- [A] = {rA0:g} × e<sup>−{rk:g} × {rt:g}</sup> = {rA0:g} × e<sup>−{rk*rt:g}</sup> = **{rA:.5f} mol/L**
- Fraction remaining = **{rf*100:.2f}%**, so **{rX*100:.2f}%** has reacted
- Half-life = 0.6931 ÷ {rk:g} = {rth:.1f} s = **{rth/60:.2f} min**
- Rate at {rt/60:g} min = {rk:g} × {rA:.5f} = **{rr*1e4:.4f} × 10⁻⁴ mol/(L·s)**

For comparison, a zero-order reaction with k = 1 × 10⁻⁴ M/s would have [A] = {rA0:g} − 10⁻⁴ × {rt:g} = **{r0[0]:.2f} mol/L** after the same time, and a second-order reaction with k = 2 × 10⁻³ M⁻¹s⁻¹ would have [A] = 1 ÷ (1/{rA0:g} + 0.002 × {rt:g}) = **{r2[0]:.4f} mol/L**.

## First-order decay by half-lives

| Half-lives elapsed | Remaining | Reacted |
|---|---|---|
{rh_rows}
## How the three orders differ

All three start at 1 mol/L with a first half-life of 10 minutes:

| Time | Zero order | First order | Second order |
|---|---|---|---|
{ro_rows}
A zero-order reaction runs at a constant rate and stops abruptly when the reactant is used up; a second-order reaction slows down most as the concentration falls.

## Practical notes

- **Rate constants depend on temperature** — often roughly doubling for every 10 °C rise. Use the [Arrhenius equation calculator](/chemistry/arrhenius-equation/) to correct k to another temperature.
- **Pseudo-first-order:** when one reactant is in large excess, its concentration hardly changes and a second-order reaction behaves as first order with k′ = k [B]₀.
- Radioactive decay, drug elimination and many decompositions are first order; reactions on a saturated catalyst surface or limited by an enzyme at high substrate concentration are approximately zero order.
- For radioactive decay with a known half-life, the [half-life calculator](/chemistry/half-life/) works directly in years.
''')

# ======================================================================= MATH

# ---------------------------------------------------------------- SSS triangle solver
def sss(a, b, c):
    s = (a + b + c) / 2
    K = math.sqrt(s * (s - a) * (s - b) * (s - c))
    A = math.acos((b * b + c * c - a * a) / (2 * b * c)); B = math.acos((a * a + c * c - b * b) / (2 * a * c)); C = pi - A - B
    return dict(s=s, P=2 * s, K=K, A=A, B=B, C=C, ha=2 * K / a, hb=2 * K / b, hc=2 * K / c, r=K / s, R=a * b * c / (4 * K),
                ma=0.5 * math.sqrt(2 * b * b + 2 * c * c - a * a), mb=0.5 * math.sqrt(2 * a * a + 2 * c * c - b * b), mc=0.5 * math.sqrt(2 * a * a + 2 * b * b - c * c))
sa, sb, sc = 7.0, 8.0, 9.0
S = sss(sa, sb, sc)
dg = math.degrees
TR = ((3, 4, 5), (5, 12, 13), (1, 1, 1), (5, 5, 8), (6, 7, 8), (2, 3, 4), (10, 10, 10), (7, 8, 9))
def kind(a, b, c):
    x = sorted((a, b, c)); q = x[0] ** 2 + x[1] ** 2 - x[2] ** 2
    sides = 'equilateral' if a == b == c else 'isosceles' if len({a, b, c}) == 2 else 'scalene'
    ang = 'right' if abs(q) < 1e-9 else 'acute' if q > 0 else 'obtuse'
    return f"{sides}, {ang}"
st_rows = ''
for a, b, c in TR:
    r = sss(a, b, c)
    st_rows += f"| {a}, {b}, {c} | {dg(r['A']):.2f}°, {dg(r['B']):.2f}°, {dg(r['C']):.2f}° | {r['K']:.4g} | {r['r']:.4g} | {r['R']:.4g} | {kind(a, b, c)} |\n"
P('math', 'sss-triangle', f'''
title: SSS Triangle Calculator (Angles, Area from 3 Sides)
description: Solve a triangle from its three sides (SSS) — all three angles, area by Heron's formula, perimeter, heights, medians, inradius and circumradius.
category: math
{intro("When you know the lengths of all three sides of a triangle, everything else about it is fixed: the law of cosines gives the angles and Heron's formula gives the area. This SSS triangle calculator solves the whole triangle from three sides — the three angles, the area, the perimeter and semi-perimeter, the three heights and medians, and the radii of the inscribed and circumscribed circles.")}
keywords: [sss triangle calculator, triangle calculator 3 sides, find angles of a triangle given 3 sides, herons formula calculator, triangle area from three sides, triangle solver, sss calculator]
updated: {D}
variables:
  - {{ id: a, label: Side a, family: length, unit: cm, imperialUnit: in, default: {sa:g}, min: 0 }}
  - {{ id: b, label: Side b, family: length, unit: cm, imperialUnit: in, default: {sb:g}, min: 0 }}
  - {{ id: c, label: Side c, family: length, unit: cm, imperialUnit: in, default: {sc:g}, min: 0 }}
  - {{ id: A, label: Angle A (opposite side a), family: angle, unit: deg, min: 0 }}
  - {{ id: B, label: Angle B (opposite side b), family: angle, unit: deg, min: 0 }}
  - {{ id: C, label: Angle C (opposite side c), family: angle, unit: deg, min: 0 }}
  - {{ id: P, label: Perimeter, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: K, label: Area (Heron's formula), family: area, unit: cm2, imperialUnit: in2, min: 0 }}
  - {{ id: ha, label: Height to side a, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: hb, label: Height to side b, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: hc, label: Height to side c, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: ma, label: Median to side a, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: mb, label: Median to side b, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: mc, label: Median to side c, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: r, label: Inradius (inscribed circle), family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: R, label: Circumradius (circumscribed circle), family: length, unit: cm, imperialUnit: in, min: 0 }}
equations:
  - A = acos((b^2 + c^2 - a^2) / (2 * b * c))
  - B = acos((a^2 + c^2 - b^2) / (2 * a * c))
  - C = acos((a^2 + b^2 - c^2) / (2 * a * b))
  - P = a + b + c
  - K = sqrt((a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c)) / 4
  - ha = 2 * K / a
  - hb = 2 * K / b
  - hc = 2 * K / c
  - ma = sqrt(2 * b^2 + 2 * c^2 - a^2) / 2
  - mb = sqrt(2 * a^2 + 2 * c^2 - b^2) / 2
  - mc = sqrt(2 * a^2 + 2 * b^2 - c^2) / 2
  - r = 2 * K / P
  - R = a * b * c / (4 * K)
faq:
  - q: How do you find the angles of a triangle from three sides?
    a: Use the law of cosines rearranged for the angle — cos A = (b² + c² − a²) ÷ (2bc), and the same pattern for B and C. Take the inverse cosine of each. The three angles always add up to 180°, which is a useful check.
  - q: What is Heron's formula?
    a: The area of a triangle with sides a, b and c is √[s(s − a)(s − b)(s − c)], where s = (a + b + c) ÷ 2 is the semi-perimeter. For sides 3, 4 and 5, s = 6 and the area is √(6 × 3 × 2 × 1) = 6.
  - q: Can any three lengths make a triangle?
    a: No — each side must be shorter than the sum of the other two (the triangle inequality). For 2, 3 and 6 the two short sides add up to only 5, so no triangle exists and the calculator shows no valid angles or area.
  - q: How do I tell if a triangle is right, acute or obtuse from its sides?
    a: Compare the square of the longest side c with a² + b². If c² = a² + b² the triangle is right-angled, if c² is smaller it is acute and if c² is larger it is obtuse. The largest angle is always opposite the longest side.
related: [math/law-of-cosines, math/law-of-sines, math/triangle-area, math/pythagorean-theorem]
''', f'''
## How to use the SSS triangle calculator

Enter the lengths of the **three sides** a, b and c in any unit. The calculator gives the three **angles** (angle A is opposite side a), the **perimeter**, the **area** from Heron's formula, the **heights** (altitudes) and **medians** to each side and the radii of the **inscribed** and **circumscribed** circles. If the sides break the triangle inequality, no triangle exists and the angles and area cannot be calculated. For two sides and the included angle, use the [law of cosines calculator](/math/law-of-cosines/) instead.

## SSS triangle formulas

<p class="formula">cos A = (b² + c² − a²) ÷ 2bc &nbsp;·&nbsp; cos B = (a² + c² − b²) ÷ 2ac &nbsp;·&nbsp; cos C = (a² + b² − c²) ÷ 2ab</p>

<p class="formula">s = (a + b + c) ÷ 2 &nbsp;·&nbsp; Area = √[s(s − a)(s − b)(s − c)]</p>

<p class="formula">h<sub>a</sub> = 2 Area ÷ a &nbsp;·&nbsp; m<sub>a</sub> = ½ √(2b² + 2c² − a²) &nbsp;·&nbsp; r = Area ÷ s &nbsp;·&nbsp; R = abc ÷ (4 Area)</p>

## Worked example

A triangle with sides a = {sa:g} cm, b = {sb:g} cm and c = {sc:g} cm:

- cos A = ({sb:g}² + {sc:g}² − {sa:g}²) ÷ (2 × {sb:g} × {sc:g}) = {(sb*sb+sc*sc-sa*sa):g} ÷ {2*sb*sc:g} = {(sb*sb+sc*sc-sa*sa)/(2*sb*sc):.4f}, so **A = {dg(S['A']):.2f}°**
- cos B = ({sa:g}² + {sc:g}² − {sb:g}²) ÷ (2 × {sa:g} × {sc:g}) = {(sa*sa+sc*sc-sb*sb)/(2*sa*sc):.4f}, so **B = {dg(S['B']):.2f}°**
- C = 180° − {dg(S['A']):.2f}° − {dg(S['B']):.2f}° = **{dg(S['C']):.2f}°**
- Perimeter = **{S['P']:g} cm**, semi-perimeter s = {S['s']:g} cm
- Area = √({S['s']:g} × {S['s']-sa:g} × {S['s']-sb:g} × {S['s']-sc:g}) = √{S['s']*(S['s']-sa)*(S['s']-sb)*(S['s']-sc):g} = **{S['K']:.4f} cm²**
- Heights: h<sub>a</sub> = **{S['ha']:.4f} cm**, h<sub>b</sub> = **{S['hb']:.4f} cm**, h<sub>c</sub> = **{S['hc']:.4f} cm**
- Medians: m<sub>a</sub> = **{S['ma']:.4f} cm**, m<sub>b</sub> = **{S['mb']:.4f} cm**, m<sub>c</sub> = **{S['mc']:.4f} cm**
- Inradius r = {S['K']:.4f} ÷ {S['s']:g} = **{S['r']:.4f} cm**; circumradius R = {sa*sb*sc:g} ÷ (4 × {S['K']:.4f}) = **{S['R']:.4f} cm**

## Solved triangles

| Sides | Angles A, B, C | Area | Inradius | Circumradius | Type |
|---|---|---|---|---|---|
{st_rows}
## Practical notes

- **Rounding:** when two sides are nearly equal to the third side added up (a very flat triangle), the angles and area become very sensitive to small measurement errors.
- **Setting out on site:** builders use three measured sides — a 3-4-5 or 6-8-10 triangle — to set out a right angle, and surveyors solve plots of land by dividing them into triangles measured on all three sides.
- The medians meet at the centroid, two thirds of the way from each corner; the inscribed circle touches all three sides and the circumscribed circle passes through all three corners.
- For a right triangle with two known sides, the [Pythagorean theorem calculator](/math/pythagorean-theorem/) gives the third side directly.
''')

print(len(DESC), 'pages:', ' '.join(DESC))
