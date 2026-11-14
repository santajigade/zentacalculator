"""Batch 2026-11-14 — 6 calculators: engineering (belt tension by the Euler–Eytelwein capstan equation,
press fit / interference fit contact pressure by Lamé thick-cylinder theory), chemistry (stoichiometric
combustion air from the ultimate analysis, GCV to NCV conversion), math (significant figures and
rounding, inverse trigonometric functions). All reference tables are computed here; defaults match the
worked examples. (Steam consumption was deferred: it needs IAPWS steam tables, which are not available
in this run.)"""
import sys, math, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro
D = '2026-11-14'
pi = math.pi
DESC = []
def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    assert 'featured' not in fm
    DESC.append(slug)
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    page(cat, slug, fm, body)

# ======================================================================= ENGINEERING

# ---------------------------------------------------------------- Belt tension
def belt(Pkw, N, Dmm, mu, th_deg, beta, w):
    v = pi * Dmm / 1000 * N / 60
    Te = Pkw * 1000 / v
    th = th_deg * pi / 180
    R = math.exp(mu * th / math.sin(beta * pi / 360))
    Tc = w * v ** 2
    T1 = Te * R / (R - 1) + Tc
    T2 = Te / (R - 1) + Tc
    a, b = T1 - Tc, T2 - Tc
    Fs = math.sqrt(a * a + b * b - 2 * a * b * math.cos(th))
    return dict(v=v, Te=Te, R=R, Tc=Tc, T1=T1, T2=T2, T0=(T1 + T2) / 2, Fs=Fs)
bP, bN, bD, bmu, bth, bb, bw = 3.0, 1440.0, 150.0, 0.25, 170.0, 38.0, 0.19
BT = belt(bP, bN, bD, bmu, bth, bb, bw)
br_rows = ''
for mu in (0.15, 0.2, 0.25, 0.3, 0.35, 0.4):
    br_rows += f"| {mu:g} | " + ' | '.join(f"{math.exp(mu*t*pi/180/math.sin(be*pi/360)):,.2f}" for be, t in ((180, 180), (180, 150), (38, 180), (38, 150), (34, 180))) + " |\n"
bs_rows = ''
for Pk in (0.75, 1.5, 3, 5.5, 7.5, 11, 15):
    r = belt(Pk, 1440, 150, bmu, bth, bb, 0)
    r2 = belt(Pk, 1440, 250, bmu, bth, bb, 0)
    bs_rows += f"| {Pk:g} kW | {r['v']:.2f} m/s | {r['Te']:,.0f} N | {r['T1']:,.0f} N | {r['T2']:,.0f} N | {r2['Te']:,.0f} N | {r2['T1']:,.0f} N |\n"
bc_rows = ''
for v in (5, 10, 15, 20, 25, 30):
    bc_rows += f"| {v} m/s | " + ' | '.join(f"{w*v*v:,.1f} N" for w in (0.06, 0.12, 0.19, 0.30, 0.66)) + " |\n"
BETAS = [('Flat belt (no groove)', 180), ('V-belt in a 34° groove', 34), ('V-belt in a 36° groove', 36), ('V-belt in a 38° groove', 38), ('V-belt, 40° belt angle', 40)]

P('engineering', 'belt-tension', f'''
title: Belt Tension Calculator (Tight & Slack Side, V & Flat Belts)
description: Calculate tight-side and slack-side belt tension, the tension ratio, centrifugal tension and shaft load for flat and V-belt drives from power and speed.
category: engineering
{intro("A belt transmits power through the difference between the tension on its tight side and its slack side, and friction around the pulley limits how large that difference can get. This belt tension calculator uses the Euler–Eytelwein (capstan) equation to work out the tension ratio, the tight-side and slack-side tensions, the centrifugal tension, the static installation tension and the load on the shaft bearings for flat and V-belt drives.")}
keywords: [belt tension calculator, tight side and slack side tension, v belt tension calculation, belt tension formula, t1/t2 = e^(μθ), capstan equation, belt drive shaft load, centrifugal tension of belt]
published: {D}
updated: {D}
variables:
  - {{ id: P, label: Power transmitted, family: power, unit: kW, imperialUnit: hp, default: {bP:g}, min: 0 }}
  - {{ id: N, label: Speed of the smaller (driver) pulley, suffix: rpm, default: {bN:g}, min: 0 }}
  - {{ id: D, label: Pitch diameter of that pulley, family: length, unit: mm, imperialUnit: in, default: {bD:g}, min: 0 }}
  - {{ id: mu, label: Coefficient of friction (belt on pulley), default: {bmu:g}, min: 0, help: 'Rubber or fabric belt on cast iron or steel: about 0.25–0.35 dry. Leather on cast iron: about 0.3. Use a lower value if the drive may get oily or wet.' }}
  - {{ id: th, label: Angle of wrap on the smaller pulley, suffix: °, default: {bth:g}, min: 0, max: 360, help: 'θ ≈ 180° − 2·asin((D − d) ÷ 2C), with C the centre distance. 180° for equal pulleys.' }}
  - id: beta
    label: Belt type / groove angle
    default: {bb:g}
    options:
{''.join(f"      - {{ label: '{nm}', value: {b} }}" + chr(10) for nm, b in BETAS)}  - {{ id: w, label: Belt mass per metre (all belts), suffix: kg/m, default: {bw:g}, min: 0, help: 'Classical V-belt sections: Z ≈ 0.06, A ≈ 0.12, B ≈ 0.19, C ≈ 0.30, D ≈ 0.66 kg/m. Multiply by the number of belts. Enter 0 to ignore centrifugal tension.' }}
  - {{ id: v, label: Belt speed, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: Te, label: Effective tension (T1 − T2), family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: R, label: Tension ratio T1 ÷ T2 (friction part), min: 0, decimals: 3 }}
  - {{ id: Tc, label: Centrifugal tension, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: T1, label: Tight-side tension, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: T2, label: Slack-side tension, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: T0, label: Static (installation) tension, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: Fs, label: Load on the shaft (bearing load), family: force, unit: N, imperialUnit: lbf, min: 0 }}
equations:
  - v = pi * D * N / 60
  - Te = P / v
  - R = exp(mu * th * pi / 180 / sin(beta * pi / 360))
  - Tc = w * v^2
  - T1 = Te * R / (R - 1) + Tc
  - T2 = Te / (R - 1) + Tc
  - T0 = (T1 + T2) / 2
  - Fs = sqrt((T1 - Tc)^2 + (T2 - Tc)^2 - 2 * (T1 - Tc) * (T2 - Tc) * cos(th * pi / 180))
faq:
  - q: How do you calculate tight side and slack side belt tension?
    a: First find the effective tension Te = power ÷ belt speed. The capstan equation sets the ratio T1 ÷ T2 = e^(μθ) for a flat belt, or e^(μθ ÷ sin(β/2)) for a V-belt with groove angle β. Then T1 = Te × R ÷ (R − 1) and T2 = Te ÷ (R − 1), plus the centrifugal tension mv² on both sides. For 3 kW at 11.3 m/s, Te = 265 N.
  - q: Why does a V-belt grip better than a flat belt?
    a: The wedge action in the groove multiplies the normal force on the belt sides by 1 ÷ sin(β/2). In a 38° groove that is about 3.07, so a friction coefficient of 0.25 behaves like 0.77 on a flat pulley, and the same tension ratio is reached with far less installation tension and shaft load.
  - q: What is centrifugal tension in a belt?
    a: The tension needed to keep the belt moving around the pulleys, Tc = m × v², where m is the mass per metre and v the belt speed. It adds equally to both sides, does not help transmit power and is not felt by the bearings. It matters above about 20 m/s, which is why very fast drives need lighter belts.
  - q: How tight should a belt be?
    a: The static tension when the drive is stopped should be about (T1 + T2) ÷ 2 at full load, so the belt does not slip on start-up. Manufacturers turn this into a deflection force at the middle of the span. Too much tension overloads bearings and shortens belt life; too little causes slip, squeal and glazing.
related: [engineering/pulley-speed, engineering/torque-power-speed, engineering/chain-length, engineering/shaft-diameter, engineering/bearing-life, physics/friction-force]
''', f'''
## How to use the belt tension calculator

Enter the **power** the belt must carry, the **speed** and **pitch diameter** of the smaller pulley, the **friction coefficient**, the **angle of wrap** on that pulley, the **belt type** (flat or the V-groove angle) and the **belt mass per metre**. The calculator gives the belt speed, the effective tension, the tension ratio, the centrifugal tension, the tight- and slack-side tensions, the static installation tension and the resultant load on the shaft. The smaller pulley is used because it has the smaller wrap angle, so it is the one that slips first.

## Belt tension formulas

<p class="formula">v = π D N ÷ 60 &nbsp;·&nbsp; T<sub>e</sub> = T<sub>1</sub> − T<sub>2</sub> = P ÷ v</p>

<p class="formula">(T<sub>1</sub> − T<sub>c</sub>) ÷ (T<sub>2</sub> − T<sub>c</sub>) = e<sup>μθ ÷ sin(β/2)</sup> &nbsp;·&nbsp; T<sub>c</sub> = m v²</p>

<p class="formula">F<sub>shaft</sub> = √(T<sub>1</sub>′² + T<sub>2</sub>′² − 2 T<sub>1</sub>′ T<sub>2</sub>′ cos θ), with T′ = T − T<sub>c</sub></p>

θ is the wrap angle in radians and β the groove angle (β = 180° gives sin 90° = 1, the flat-belt case). The static tension T<sub>0</sub> = (T<sub>1</sub> + T<sub>2</sub>) ÷ 2.

## Worked example

A {bP:g} kW motor at {bN:g} rpm drives through a single B-section V-belt ({bw:g} kg/m) on a {bD:g} mm pitch-diameter pulley in a {bb:g}° groove, with μ = {bmu:g} and {bth:g}° of wrap:

- Belt speed v = π × {bD/1000:g} × {bN:g} ÷ 60 = **{BT['v']:.2f} m/s**
- Effective tension Te = {bP*1000:,.0f} ÷ {BT['v']:.2f} = **{BT['Te']:.1f} N**
- Tension ratio = e^({bmu:g} × {bth*pi/180:.4f} ÷ sin {bb/2:g}°) = e^{bmu*bth*pi/180/math.sin(bb*pi/360):.4f} = **{BT['R']:.3f}**
- Centrifugal tension Tc = {bw:g} × {BT['v']:.2f}² = **{BT['Tc']:.1f} N**
- Tight side T1 = {BT['Te']:.1f} × {BT['R']:.3f} ÷ {BT['R']-1:.3f} + {BT['Tc']:.1f} = **{BT['T1']:.1f} N**
- Slack side T2 = {BT['Te']:.1f} ÷ {BT['R']-1:.3f} + {BT['Tc']:.1f} = **{BT['T2']:.1f} N**
- Static tension T0 = **{BT['T0']:.1f} N**; shaft load = **{BT['Fs']:.1f} N**

## Tension ratio T1 ÷ T2 by friction and wrap angle

| μ | Flat, 180° | Flat, 150° | V 38°, 180° | V 38°, 150° | V 34°, 180° |
|---|---|---|---|---|---|
{br_rows}
## Belt tensions by power

Single V-belt in a {bb:g}° groove, μ = {bmu:g}, {bth:g}° wrap, driver at 1,440 rpm, centrifugal tension neglected:

| Power | Belt speed (150 mm) | Te (150 mm) | T1 (150 mm) | T2 (150 mm) | Te (250 mm) | T1 (250 mm) |
|---|---|---|---|---|---|---|
{bs_rows}
A larger pulley raises the belt speed and cuts every tension in proportion — one of the simplest ways to relieve an overloaded belt or bearing.

## Centrifugal tension by belt speed

| Belt speed | Z (0.06 kg/m) | A (0.12 kg/m) | B (0.19 kg/m) | C (0.30 kg/m) | D (0.66 kg/m) |
|---|---|---|---|---|---|
{bc_rows}
## Practical notes

- **Design margin on friction:** the capstan equation gives the tension ratio at the point of slip. Belt makers design with an effective ratio of about 5 for V-belts at 180° wrap (Gates uses an effective friction of 0.5123 per radian) and about 2–3 for flat belts, so the belt does not creep when the friction drops with wear, dust or oil.
- **Wrap angle:** the wrap on the small pulley is about 180° − 57.3° × (D − d) ÷ C, with C the centre distance. Below about 120° add an idler or increase the centre distance.
- **Speed:** most V-belts run best at 10–30 m/s. Below 5 m/s the tensions get large; above 30 m/s centrifugal tension eats into the capacity. Find pulley speeds and ratios with the [pulley speed calculator](/engineering/pulley-speed/) and the torque at each shaft with the [torque, power and speed calculator](/engineering/torque-power-speed/).
- **Bearing loads:** the shaft load is close to T1 + T2 for wraps near 180°. Use it to check the shaft with the [shaft diameter calculator](/engineering/shaft-diameter/) and the bearing life with the [bearing life calculator](/engineering/bearing-life/).
''')

# ---------------------------------------------------------------- Press fit
def press(d, dl, Do, Di, Eh, Es, nh, ns, mu, L):
    ah = (Do**2 + d**2) / (Do**2 - d**2)
    as_ = (d**2 + Di**2) / (d**2 - Di**2)
    p = dl / (d / Eh * (ah + nh) + d / Es * (as_ - ns))
    F = pi * mu * p * d * L
    return dict(p=p, sh=p * ah, ss=-p * as_, F=F, T=F * d / 2, ah=ah, as_=as_)
fd, fdl, fDo, fDi, fE, fn, fmu, fL = 0.05, 40e-6, 0.1, 0.0, 200e9, 0.3, 0.15, 0.05
PF = press(fd, fdl, fDo, fDi, fE, fE, fn, fn, fmu, fL)
pf_rows = ''
for dl in (10, 20, 30, 40, 50, 60, 80):
    pf_rows += f"| {dl} µm | " + ' | '.join(f"{press(fd, dl*1e-6, Do, 0, fE, fE, fn, fn, fmu, fL)['p']/1e6:,.1f}" for Do in (0.065, 0.075, 0.1, 0.15)) + f" | {press(fd, dl*1e-6, 0.1, 0, fE, fE, fn, fn, fmu, fL)['T']:,.0f} N·m |\n"
pr_rows = ''
for dmm in (10, 20, 30, 50, 80, 100, 150):
    pr_rows += f"| {dmm} mm | " + ' | '.join(f"{press(dmm/1000, dmm*k*1e-6, dmm*2/1000, 0, fE, fE, fn, fn, fmu, dmm/1000)['p']/1e6:,.0f}" for k in (0.5, 1.0, 1.5)) + " |\n"
ALPHA = 11.5e-6
ps_rows = ''
for dmm in (20, 50, 100, 200):
    for dl in (dmm * 0.8, dmm * 1.5):
        c = max(0.001 * dmm, 0) * 1000  # assembly clearance 0.001 x d, in µm
        dT = (dl + c) * 1e-6 / (ALPHA * dmm / 1000)
        ps_rows += f"| {dmm} mm | {dl:g} µm | {c:g} µm | {dT:,.0f} K |\n"

P('engineering', 'press-fit', f'''
title: Press Fit Calculator (Interference Fit Pressure & Force)
description: Calculate interference fit contact pressure, hub and shaft hoop stresses, press-in force and torque capacity from the interference and diameters.
category: engineering
{intro("An interference (press or shrink) fit holds a hub on a shaft by making the shaft slightly larger than the bore, so the parts squeeze each other. This press fit calculator uses Lamé's thick-cylinder equations to find the contact pressure from the diametral interference, the hoop stresses in the hub and shaft, the axial force needed to press the parts together and the torque the joint can carry before it slips.")}
keywords: [press fit calculator, interference fit calculator, interference fit pressure, shrink fit calculator, press fit force calculation, lame equation interference fit, hub hoop stress, press fit torque capacity]
published: {D}
updated: {D}
variables:
  - {{ id: d, label: Nominal interface diameter, family: length, unit: mm, imperialUnit: in, default: {fd*1000:g}, min: 0 }}
  - {{ id: dl, label: Diametral interference (shaft − bore), family: length, unit: um, default: {fdl*1e6:g}, min: 0, help: 'Shaft diameter minus bore diameter. For a fit like H7/s6 use the mean or the maximum interference from the ISO 286 tolerance tables.' }}
  - {{ id: Do, label: Hub outer diameter, family: length, unit: mm, imperialUnit: in, default: {fDo*1000:g}, min: 0 }}
  - {{ id: Di, label: Shaft bore diameter (0 = solid shaft), family: length, unit: mm, imperialUnit: in, default: 0, min: 0 }}
  - {{ id: Eh, label: Hub Young's modulus, suffix: GPa, default: {fE/1e9:g}, min: 0, help: 'Steel ≈ 200–210 GPa, cast iron ≈ 100–120, aluminium alloy ≈ 70, bronze ≈ 110, titanium ≈ 110.' }}
  - {{ id: Es, label: Shaft Young's modulus, suffix: GPa, default: {fE/1e9:g}, min: 0 }}
  - {{ id: nh, label: Hub Poisson's ratio, default: {fn:g}, min: 0, max: 0.5 }}
  - {{ id: ns, label: Shaft Poisson's ratio, default: {fn:g}, min: 0, max: 0.5 }}
  - {{ id: mu, label: Coefficient of friction at the interface, default: {fmu:g}, min: 0, help: 'Steel on steel: about 0.1–0.15 for a lubricated press fit, 0.15–0.25 for a dry or shrink fit.' }}
  - {{ id: L, label: Length of engagement, family: length, unit: mm, imperialUnit: in, default: {fL*1000:g}, min: 0 }}
  - {{ id: p, label: Contact pressure, family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
  - {{ id: sh, label: Hub hoop stress at the bore (tension), family: pressure, unit: MPa, imperialUnit: psi }}
  - {{ id: ss, label: Shaft hoop stress at the surface (compression), family: pressure, unit: MPa, imperialUnit: psi }}
  - {{ id: F, label: Axial press-in force, family: force, unit: kN, imperialUnit: lbf, min: 0 }}
  - {{ id: T, label: Torque capacity before slip, family: torque, unit: Nm, imperialUnit: lbft, min: 0 }}
equations:
  - p = dl / (d / (Eh * 1e9) * ((Do^2 + d^2) / (Do^2 - d^2) + nh) + d / (Es * 1e9) * ((d^2 + Di^2) / (d^2 - Di^2) - ns))
  - sh = p * (Do^2 + d^2) / (Do^2 - d^2)
  - ss = -p * (d^2 + Di^2) / (d^2 - Di^2)
  - F = pi * mu * p * d * L
  - T = F * d / 2
faq:
  - q: How do you calculate interference fit pressure?
    a: With Lamé's equation p = δ ÷ [d/E_h × ((D_o² + d²)/(D_o² − d²) + ν_h) + d/E_s × ((d² + d_i²)/(d² − d_i²) − ν_s)], where δ is the diametral interference. For a solid steel shaft in a steel hub it simplifies to p = Eδ ÷ 2d × (1 − d²/D_o²). A 40 µm interference on 50 mm with a 100 mm hub gives 60 MPa.
  - q: How much force is needed to press fit a shaft?
    a: F = π μ p d L — the contact pressure times the contact area times the friction coefficient. The example joint (60 MPa, 50 mm × 50 mm, μ = 0.15) needs about 70.7 kN, roughly 7.2 tonnes. Add a margin because the friction while pressing can be higher than the static value used for torque.
  - q: How much torque can a press fit transmit?
    a: T = F × d ÷ 2 = π μ p d² L ÷ 2. The example carries about 1,770 N·m before it slips. Shrink fits usually have more torque capacity than press fits of the same interference because the surfaces are not smoothed by pressing.
  - q: How hot should a hub be heated for a shrink fit?
    a: Enough to expand the bore by the interference plus an assembly clearance of about 0.001 × d: ΔT = (δ + clearance) ÷ (α × d). For steel (α ≈ 11.5 × 10⁻⁶ /K), a 50 mm bore with 40 µm interference needs about 157 K above the shaft temperature. Bearings are usually limited to about 120 °C.
related: [engineering/shaft-diameter, engineering/thermal-expansion, engineering/bearing-life, engineering/bolt-torque, engineering/factor-of-safety, physics/youngs-modulus]
''', f'''
## How to use the press fit calculator

Enter the **nominal diameter** at the joint, the **diametral interference** (shaft diameter minus bore diameter), the **hub outer diameter**, the **shaft bore** (0 for a solid shaft), the **elastic modulus and Poisson's ratio** of both parts, the **friction coefficient** and the **length of engagement**. The calculator gives the contact pressure, the hoop stress in the hub at the bore and in the shaft at its surface, the axial force needed to press the parts together and the torque the fit can transmit. Leave the interference blank and enter a pressure to find the interference you need.

## Interference fit formulas (Lamé)

<p class="formula">p = δ ÷ [ (d ÷ E<sub>h</sub>) × ((D<sub>o</sub>² + d²) ÷ (D<sub>o</sub>² − d²) + ν<sub>h</sub>) + (d ÷ E<sub>s</sub>) × ((d² + d<sub>i</sub>²) ÷ (d² − d<sub>i</sub>²) − ν<sub>s</sub>) ]</p>

<p class="formula">σ<sub>hub</sub> = p (D<sub>o</sub>² + d²) ÷ (D<sub>o</sub>² − d²) &nbsp;·&nbsp; σ<sub>shaft</sub> = −p (d² + d<sub>i</sub>²) ÷ (d² − d<sub>i</sub>²)</p>

<p class="formula">F = π μ p d L &nbsp;·&nbsp; T = F d ÷ 2</p>

δ is the diametral interference, d the nominal diameter, D<sub>o</sub> the hub outside diameter and d<sub>i</sub> the shaft bore. The hub hoop stress is the highest stress in the joint and occurs at the bore.

## Worked example

A solid steel shaft is pressed into a steel hub: d = {fd*1000:g} mm, interference {fdl*1e6:g} µm, hub outside diameter {fDo*1000:g} mm, E = {fE/1e9:g} GPa, ν = {fn:g}, μ = {fmu:g}, engagement {fL*1000:g} mm:

- Hub factor (D<sub>o</sub>² + d²) ÷ (D<sub>o</sub>² − d²) = ({fDo*1000:g}² + {fd*1000:g}²) ÷ ({fDo*1000:g}² − {fd*1000:g}²) = {PF['ah']:.4f}
- Contact pressure p = {fdl:g} ÷ [{fd:g} ÷ {fE:.3g} × ({PF['ah']:.4f} + {fn:g} + 1 − {fn:g})] = **{PF['p']/1e6:.1f} MPa**
- Hub hoop stress = {PF['p']/1e6:.1f} × {PF['ah']:.4f} = **{PF['sh']/1e6:.1f} MPa** (tension); shaft hoop stress = **{PF['ss']/1e6:.1f} MPa** (compression)
- Press-in force F = π × {fmu:g} × {PF['p']/1e6:.1f} MPa × {fd:g} × {fL:g} = **{PF['F']/1000:.1f} kN**
- Torque capacity T = {PF['F']/1000:.1f} kN × {fd/2:g} m = **{PF['T']:,.0f} N·m**

## Contact pressure (MPa) by interference and hub size

Solid steel shaft in a steel hub, d = 50 mm, E = 200 GPa, ν = 0.3; the last column is the torque capacity for a 100 mm hub, 50 mm long, μ = 0.15:

| Interference | Hub OD 65 mm | Hub OD 75 mm | Hub OD 100 mm | Hub OD 150 mm | Torque (100 mm hub) |
|---|---|---|---|---|---|
{pf_rows}
## Contact pressure (MPa) by size for a given interference per mm

Steel on steel, hub OD = 2d, engagement length L = d; interference given in µm per mm of diameter:

| Diameter | 0.5 µm/mm | 1.0 µm/mm | 1.5 µm/mm |
|---|---|---|---|
{pr_rows}
With the hub OD fixed at 2d, the pressure depends only on the interference ratio δ/d, which is why fits are often specified in µm per mm (or ‰ of the diameter).

## Shrink fit heating temperature (steel hub)

Temperature rise ΔT = (δ + clearance) ÷ (α d), with α = 11.5 × 10⁻⁶ /K and an assembly clearance of 0.001 × d:

| Bore | Interference | Clearance | Temperature rise |
|---|---|---|---|
{ps_rows}
## Practical notes

- **Check the hub stress:** the hub hoop stress plus the radial pressure must stay well below the yield strength of the hub; cast-iron hubs are brittle and need a larger margin. Size the shaft separately with the [shaft diameter calculator](/engineering/shaft-diameter/).
- **Surface finish:** pressing smooths the surface peaks, so some of the measured interference is lost — roughly 0.8 × (Rz shaft + Rz bore) for ground surfaces. Allow for this on small, fine fits.
- **Temperature and speed:** different expansion coefficients (an aluminium hub on a steel shaft) change the interference with temperature, and at high speed centrifugal growth of the hub reduces the pressure. Check the expansion with the [thermal expansion calculator](/engineering/thermal-expansion/).
- **Tolerances:** use the minimum interference from the tolerance tables for the torque check and the maximum interference for the stress check and press force.
''')

# ======================================================================= CHEMISTRY

# ---------------------------------------------------------------- Combustion air
KC, KH, KS = 31.998 / 12.011, 15.999 / (2 * 1.008), 31.998 / 32.06
O2AIR = 0.2314; RHO_AIR = 1.2922
def cair(C, H, O, S):
    o2 = KC * C + KH * H + KS * S - O
    return o2, o2 / O2AIR
aC, aH, aO, aS, aEA, amf = 0.859, 0.12, 0.007, 0.005, 0.15, 100.0
aO2, aA0 = cair(aC, aH, aO, aS)
aA = aA0 * (1 + aEA)
FUELC = [('Methane / natural gas (CH₄)', 74.87, 25.13, 0, 0),
         ('Propane / LPG (C₃H₈)', 81.71, 18.29, 0, 0),
         ('Diesel (typical)', 86.4, 13.3, 0, 0.3),
         ('Heavy fuel oil (typical)', 85.9, 12.0, 0.7, 0.5),
         ('Bituminous coal (typical, as fired)', 66.0, 4.5, 7.5, 1.0),
         ('Indian coal (typical, as fired)', 41.1, 2.8, 9.9, 0.4),
         ('Wood, oven dry', 50.0, 6.0, 43.0, 0),
         ('Ethanol (C₂H₅OH)', 52.14, 13.13, 34.73, 0),
         ('Hydrogen (H₂)', 0, 100, 0, 0)]
fc_rows = ''
for nm, C, H, O, S in FUELC:
    o2, a0 = cair(C / 100, H / 100, O / 100, S / 100)
    fc_rows += f"| {nm} | {C:g} | {H:g} | {O:g} | {S:g} | {o2:.3f} | {a0:.2f} | {a0/RHO_AIR:.2f} |\n"
ea_rows = ''
for ea in (0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0):
    ea_rows += f"| {ea*100:g}% | {1+ea:.2f} | {aA0*(1+ea):.2f} | {aA0*(1+ea)/RHO_AIR:.2f} | {aA0*(1+ea)*amf:,.0f} kg/h |\n"

P('chemistry', 'combustion-air', f'''
title: Combustion Air Calculator (Stoichiometric Air from Fuel Analysis)
description: Calculate the theoretical (stoichiometric) air needed to burn a fuel from its C, H, O and S content, plus actual air with excess air in kg and Nm³.
category: chemistry
{intro("Every kilogram of fuel needs a fixed amount of oxygen to burn completely, set by how much carbon, hydrogen and sulphur it contains. This combustion air calculator works out the theoretical (stoichiometric) oxygen and air from the fuel's ultimate analysis, then adds your excess air to give the actual air–fuel ratio, the air volume in Nm³ per kg and the air flow a burner or boiler fan must supply.")}
keywords: [combustion air calculator, stoichiometric air calculation, theoretical air required for combustion, air fuel ratio from ultimate analysis, combustion air requirement, excess air combustion calculation, air required to burn fuel]
published: {D}
updated: {D}
variables:
  - {{ id: C, label: Carbon in the fuel (mass), family: percent, unit: '%', default: {aC*100:g}, min: 0, max: 1 }}
  - {{ id: H, label: Hydrogen in the fuel (mass), family: percent, unit: '%', default: {aH*100:g}, min: 0, max: 1 }}
  - {{ id: O, label: Oxygen in the fuel (mass), family: percent, unit: '%', default: {aO*100:g}, min: 0, max: 1 }}
  - {{ id: S, label: Sulphur in the fuel (mass), family: percent, unit: '%', default: {aS*100:g}, min: 0, max: 1, help: 'Use the ultimate analysis on the same basis as the fuel flow (usually as fired). Nitrogen, moisture and ash need no oxygen.' }}
  - {{ id: EA, label: Excess air, family: percent, unit: '%', default: {aEA*100:g}, min: 0, help: 'Typical: natural gas 5–15%, fuel oil 10–20%, pulverised coal 15–25%, stoker coal and biomass 30–60%.' }}
  - {{ id: mf, label: Fuel flow, family: massflow, unit: kgh, imperialUnit: lbh, default: {amf:g}, min: 0 }}
  - {{ id: O2r, label: Theoretical oxygen, suffix: kg O₂/kg fuel, min: 0, decimals: 3 }}
  - {{ id: A0, label: Stoichiometric air–fuel ratio, suffix: kg air/kg fuel, min: 0, decimals: 2 }}
  - {{ id: A, label: Actual air–fuel ratio (with excess air), suffix: kg air/kg fuel, min: 0, decimals: 2 }}
  - {{ id: Vn, label: Actual air volume, suffix: Nm³/kg fuel, min: 0, decimals: 2 }}
  - {{ id: ma, label: Combustion air flow, family: massflow, unit: kgh, imperialUnit: lbh, min: 0 }}
  - {{ id: Qn, label: Combustion air flow (normal volume), suffix: Nm³/h, min: 0, decimals: 0 }}
equations:
  - O2r = 2.6641 * C + 7.9360 * H + 0.9981 * S - O
  - A0 = O2r / 0.2314
  - A = A0 * (1 + EA)
  - Vn = A / 1.2922
  - ma = A * mf
  - Qn = ma * 3600 / 1.2922
faq:
  - q: How do you calculate the air required for combustion?
    a: "Find the oxygen needed per kg of fuel: O₂ = 2.664 C + 7.936 H + 0.998 S − O (mass fractions), then divide by 0.2314, the mass fraction of oxygen in air. This is the familiar 11.5 C + 34.3 (H − O/8) + 4.3 S. For heavy fuel oil with 85.9% C, 12% H, 0.7% O and 0.5% S the stoichiometric air is about 14.0 kg per kg of fuel."
  - q: Where do the factors 2.664 and 7.936 come from?
    a: "From the reactions C + O₂ → CO₂ and 2H₂ + O₂ → 2H₂O: 12.011 kg of carbon needs 31.998 kg of oxygen (2.664 kg/kg) and 2.016 kg of hydrogen needs 15.999 kg (7.936 kg/kg). Sulphur burns to SO₂ and needs 0.998 kg/kg. Oxygen already in the fuel reduces what the air must supply."
  - q: What is a typical air–fuel ratio?
    a: About 17.2 kg/kg for natural gas, 15.7 for propane, 14.5 for diesel, 14 for heavy fuel oil, 8–9 for good bituminous coal and about 6 for dry wood. Real burners run 5–50% above these to make sure every fuel particle meets enough oxygen.
  - q: How do I convert air mass to volume?
    a: Divide by the density of air at normal conditions, 1.2922 kg/Nm³ at 0 °C and 1.01325 bar. 14 kg of air is about 10.8 Nm³. For fan sizing, convert normal m³ to actual m³ at the fan inlet temperature and pressure.
related: [chemistry/excess-air, engineering/boiler-efficiency, chemistry/gcv-to-ncv, chemistry/percent-composition, chemistry/limiting-reagent, engineering/gas-flow-correction]
''', f'''
## How to use the combustion air calculator

Enter the fuel's **carbon, hydrogen, oxygen and sulphur** content by mass (the ultimate analysis, as fired), the **excess air** you run and the **fuel flow**. The calculator gives the theoretical oxygen and stoichiometric air–fuel ratio, the actual air–fuel ratio with excess air, the air volume in normal cubic metres per kg of fuel and the total combustion air flow in kg/h and Nm³/h. If you know the flue-gas oxygen instead of the excess air, find the excess air first with the [excess air calculator](/chemistry/excess-air/).

## Combustion air formula

<p class="formula">O<sub>2,th</sub> = 2.664 C + 7.936 H + 0.998 S − O &nbsp;(kg O<sub>2</sub> per kg fuel)</p>

<p class="formula">A<sub>0</sub> = O<sub>2,th</sub> ÷ 0.2314 &nbsp;·&nbsp; A = A<sub>0</sub> (1 + EA) &nbsp;·&nbsp; V = A ÷ 1.2922 Nm³/kg</p>

C, H, O and S are mass fractions of the fuel; 0.2314 is the mass fraction of oxygen in dry air and 1.2922 kg/Nm³ the density of air at 0 °C and 1 atm.

## Worked example

Heavy fuel oil with C {aC*100:g}%, H {aH*100:g}%, O {aO*100:g}% and S {aS*100:g}%, burned at {aEA*100:g}% excess air at {amf:g} kg/h:

- Theoretical oxygen = 2.664 × {aC:g} + 7.936 × {aH:g} + 0.998 × {aS:g} − {aO:g} = **{aO2:.3f} kg O₂/kg**
- Stoichiometric air A<sub>0</sub> = {aO2:.3f} ÷ 0.2314 = **{aA0:.2f} kg air/kg fuel**
- Actual air A = {aA0:.2f} × {1+aEA:.2f} = **{aA:.2f} kg/kg** = {aA/RHO_AIR:.2f} Nm³/kg
- Air flow = {aA:.2f} × {amf:g} = **{aA*amf:,.0f} kg/h** ≈ {aA*amf/RHO_AIR:,.0f} Nm³/h

## Stoichiometric air for common fuels

Typical ultimate analyses (mass %); the air figures are computed from the formula above:

| Fuel | C | H | O | S | O₂ (kg/kg) | Air (kg/kg) | Air (Nm³/kg) |
|---|---|---|---|---|---|---|---|
{fc_rows}
## Actual air by excess air

For the heavy fuel oil in the example at {amf:g} kg/h:

| Excess air | Air ratio λ | Air (kg/kg) | Air (Nm³/kg) | Air flow |
|---|---|---|---|---|
{ea_rows}
## Practical notes

- **Basis matters:** the ultimate analysis must be on the same basis (as fired, air dried or dry) as the fuel flow. Coal analyses are often reported dry; correct them for the moisture you actually burn.
- **Gaseous fuels:** for natural gas you can enter the mass composition of the gas (methane is 74.9% C and 25.1% H), or work in volume: 1 Nm³ of methane needs 2 Nm³ of O₂, that is 9.52 Nm³ of air.
- **Humid air:** the formula is for dry air. Humid air carries a little less oxygen per kg, so fans move about 1–2% more mass on a hot, humid day.
- **Too little or too much air:** below stoichiometric the fuel burns incompletely and forms CO and soot; every 10% of unnecessary excess air costs roughly 0.5–1% of boiler efficiency in extra stack loss. Check overall efficiency with the [boiler efficiency calculator](/engineering/boiler-efficiency/).
''')

# ---------------------------------------------------------------- GCV to NCV
HW = 2.442; KW = 18.015 / 2.016
def ncv(g, H, M): return g - HW * (KW * H + M)
gG, gH, gM = 45.6, 0.135, 0.0
gW = KW * gH + gM; gN = ncv(gG, gH, gM)
FUELG = [('Hydrogen', 141.8, 100, 0), ('Methane', 55.5, 25.13, 0), ('Propane', 50.35, 18.29, 0),
         ('Butane', 49.5, 17.34, 0), ('Petrol (gasoline)', 46.5, 13.5, 0), ('Diesel', 45.6, 13.5, 0),
         ('Heavy fuel oil', 42.7, 11.5, 0.5), ('Ethanol', 29.7, 13.13, 0), ('Methanol', 22.7, 12.58, 0),
         ('Bituminous coal (as fired)', 28.0, 4.5, 8), ('Indian coal (as fired)', 16.7, 2.8, 6)]
fg_rows = ''
for nm, g, H, M in FUELG:
    n_ = ncv(g, H / 100, M / 100)
    fg_rows += f"| {nm} | {g:g} | {H:g}% | {M:g}% | {n_:.2f} | {n_/g*100:.1f}% | {n_*1000/4.1868:,.0f} |\n"
wd_rows = ''
for M in (0, 10, 20, 30, 40, 50, 60):
    m = M / 100; g = 20.0 * (1 - m); H = 0.06 * (1 - m); n_ = ncv(g, H, m)
    wd_rows += f"| {M}% | {g:.2f} | {n_:.2f} | {n_/g*100 if g else 0:.1f}% | {n_*1000/4.1868:,.0f} |\n"

P('chemistry', 'gcv-to-ncv', f'''
title: GCV to NCV Calculator (Gross to Net Calorific Value)
description: Convert gross calorific value (GCV, HHV) to net calorific value (NCV, LHV) from the hydrogen and moisture content of a fuel, in MJ/kg, kcal/kg and BTU/lb.
category: chemistry
{intro("The gross calorific value of a fuel counts the heat released when the water formed in combustion condenses; the net value assumes that water leaves as vapour. This GCV to NCV calculator subtracts the latent heat of the water formed from the fuel's hydrogen and the moisture it already contains, so you can quote boiler efficiencies, fuel prices and emission factors on either basis.")}
keywords: [gcv to ncv calculator, gross to net calorific value, hhv to lhv calculator, higher heating value to lower heating value, net calorific value formula, ncv from gcv, calorific value conversion kcal/kg]
published: {D}
updated: {D}
variables:
  - {{ id: G, label: Gross calorific value (GCV / HHV), suffix: MJ/kg, default: {gG:g}, min: 0, help: '1 MJ/kg = 238.85 kcal/kg = 429.92 BTU/lb. Enter a kcal/kg figure divided by 238.85.' }}
  - {{ id: H, label: Hydrogen in the fuel (mass), family: percent, unit: '%', default: {gH*100:g}, min: 0, max: 1 }}
  - {{ id: M, label: Moisture in the fuel (mass), family: percent, unit: '%', default: {gM*100:g}, min: 0, max: 1, help: 'Total moisture on the same basis as the GCV (as received or as fired).' }}
  - {{ id: W, label: Water vapour formed, suffix: kg/kg fuel, min: 0, decimals: 3 }}
  - {{ id: N, label: Net calorific value (NCV / LHV), suffix: MJ/kg, decimals: 3 }}
  - {{ id: r, label: NCV as a share of GCV, family: percent, unit: '%' }}
  - {{ id: Gk, label: GCV in kcal/kg, suffix: kcal/kg, min: 0, decimals: 0 }}
  - {{ id: Nk, label: NCV in kcal/kg, suffix: kcal/kg, decimals: 0 }}
  - {{ id: Nb, label: NCV in BTU/lb, suffix: BTU/lb, decimals: 0 }}
equations:
  - W = 8.936 * H + M
  - N = G - 2.442 * W
  - r = N / G
  - Gk = G * 1000 / 4.1868
  - Nk = N * 1000 / 4.1868
  - Nb = N * 429.923
faq:
  - q: What is the difference between GCV and NCV?
    a: The gross (higher) calorific value includes the latent heat recovered when the water vapour in the flue gas condenses back to liquid at 25 °C. The net (lower) value leaves that water as vapour, which is what happens in most boilers, engines and furnaces. NCV is therefore lower by the latent heat of the water formed — about 6% for diesel and 10% for natural gas.
  - q: What is the formula to convert GCV to NCV?
    a: NCV = GCV − 2.442 × (8.936 H + M) MJ/kg, where H is the hydrogen and M the moisture content as mass fractions. 2.442 MJ/kg is the latent heat of water at 25 °C and 8.936 kg of water forms from every kg of hydrogen. For diesel (45.6 MJ/kg, 13.5% H) NCV ≈ 42.65 MJ/kg.
  - q: Which value is used for boiler efficiency?
    a: Indian (BEE) and US (ASME PTC 4) practice quote boiler efficiency on GCV; European practice and EN standards usually use NCV, which gives a figure several points higher for the same boiler. Condensing boilers can exceed 100% on an NCV basis because they recover some of the latent heat. Always state the basis.
  - q: Why does wet fuel have a much lower NCV?
    a: Moisture adds no heat but must be evaporated, and it also dilutes the dry fuel. Wood with 20 MJ/kg GCV when dry falls to about 8.1 MJ/kg NCV at 50% moisture, which is why biomass is usually priced on a net, as-received basis.
related: [engineering/boiler-efficiency, chemistry/combustion-air, chemistry/bomb-calorimeter, chemistry/enthalpy-of-reaction, conversion/energy-converter, chemistry/excess-air]
''', f'''
## How to use the GCV to NCV calculator

Enter the **gross calorific value** in MJ/kg, the fuel's **hydrogen content** and its **moisture content** (by mass, on the same basis as the GCV). The calculator gives the water vapour formed per kg of fuel, the **net calorific value** in MJ/kg, kcal/kg and BTU/lb and the NCV as a percentage of the GCV. To go the other way, clear the GCV and enter the NCV. If the GCV is in kcal/kg, divide it by 238.85 first, or read the kcal/kg outputs.

## GCV to NCV formula

<p class="formula">NCV = GCV − 2.442 × (8.936 H + M) &nbsp;MJ/kg</p>

H and M are the hydrogen and moisture mass fractions. 8.936 = 18.015 ÷ 2.016 is the mass of water formed by burning 1 kg of hydrogen, and 2.442 MJ/kg is the latent heat of vaporisation of water at 25 °C, the reference temperature of ISO and ASTM calorific value tests. In kcal/kg the same rule reads NCV = GCV − 583 × (8.936 H + M).

## Worked example

Diesel with a GCV of {gG:g} MJ/kg, {gH*100:g}% hydrogen and no moisture:

- Water formed = 8.936 × {gH:g} + {gM:g} = **{gW:.3f} kg/kg**
- NCV = {gG:g} − 2.442 × {gW:.3f} = **{gN:.3f} MJ/kg**
- NCV ÷ GCV = **{gN/gG*100:.1f}%**
- In kcal/kg: GCV = {gG*1000/4.1868:,.0f} kcal/kg, NCV = **{gN*1000/4.1868:,.0f} kcal/kg**; in BTU/lb NCV = {gN*429.923:,.0f}

## GCV and NCV of common fuels

Typical gross values; NCV computed from the hydrogen and moisture shown:

| Fuel | GCV (MJ/kg) | Hydrogen | Moisture | NCV (MJ/kg) | NCV ÷ GCV | NCV (kcal/kg) |
|---|---|---|---|---|---|---|
{fg_rows}
## Wood: effect of moisture

Wood with 20.0 MJ/kg GCV and 6% hydrogen when oven-dry, on an as-received (wet) basis:

| Moisture | GCV (MJ/kg) | NCV (MJ/kg) | NCV ÷ GCV | NCV (kcal/kg) |
|---|---|---|---|---|
{wd_rows}
## Practical notes

- **Same basis for everything:** GCV, hydrogen and moisture must all be as received, as fired, air dried or dry — mixing bases is the most common error. Hydrogen reported "including the hydrogen in moisture" must be corrected first.
- **Standards:** ISO 1928 and ASTM D5865 give more detailed net-value corrections (constant pressure versus constant volume, oxygen and nitrogen terms) that change the result by well under 1%; the simple formula is what most energy audits use.
- **Gaseous fuels:** for gases quoted in MJ/Nm³ convert to MJ/kg with the gas density first, or use the published NCV directly (natural gas is typically about 90% of its GCV).
- Calorific values are measured in a bomb calorimeter — see the [bomb calorimeter calculator](/chemistry/bomb-calorimeter/) — and used in the [boiler efficiency calculator](/engineering/boiler-efficiency/).
''')

# ======================================================================= MATH

# ---------------------------------------------------------------- Significant figures / rounding
def sig(x, n):
    if x == 0: return 0.0
    e = math.floor(math.log10(abs(x))); s = 10.0 ** (e - n + 1)
    return math.copysign(math.floor(abs(x) / s + 0.5) * s, x)
def rnd(x, d): return math.copysign(math.floor(abs(x) * 10 ** d + 0.5) / 10 ** d, x)
sx, sn, sd = 1234.5678, 3, 2
sR = sig(sx, sn); sE = math.floor(math.log10(abs(sx))); sRd = rnd(sx, sd)
def fmt(v):
    s = f"{v:.10g}"
    return s
sf_rows = ''
for x in (123456.789, 1234.5678, 9.87654, 0.0045678, 0.000987654, 299792458):
    sf_rows += f"| {x:,.10g} | " + ' | '.join((f"{sig(x, n):,.{max(0, n - 1 - math.floor(math.log10(abs(x))))}f}" if abs(sig(x, n)) >= 1000 else f"{float(f'{sig(x, n):.{n}g}'):g}") for n in (1, 2, 3, 4, 5)) + " |\n"
RULES = [('4,508', 4, 'Zeros between non-zero digits count'), ('0.00450', 3, 'Leading zeros never count; the trailing zero after the decimal point does'),
         ('45.00', 4, 'Trailing zeros after a decimal point count'), ('4500', '2 (ambiguous)', 'Trailing zeros in a whole number are ambiguous — write 4.5 × 10³ or 4.500 × 10³'),
         ('4500.', 4, 'A decimal point after the number makes the zeros count'), ('6.022 × 10²³', 4, 'In scientific notation every digit of the mantissa counts'),
         ('12 eggs', 'exact (∞)', 'Counted numbers and defined constants are exact')]
ru_rows = ''.join(f"| {a} | {b} | {c} |\n" for a, b, c in RULES)

P('math', 'significant-figures', f'''
title: Significant Figures Calculator (Round to Sig Figs)
description: Round any number to a chosen number of significant figures or decimal places, with the rules for counting sig figs and worked examples.
category: math
intro: "Significant figures show how precisely a number is known: 1,230 to three significant figures is not the same claim as 1,234.5678. This significant figures calculator rounds any number to the number of sig figs you choose, gives its power-of-ten exponent for scientific notation and also rounds to a fixed number of decimal places, using the round-half-away-from-zero rule taught in school."
keywords: [significant figures calculator, sig fig calculator, round to significant figures, sig figs rounding, rounding calculator, round to decimal places, significant digits calculator]
published: {D}
updated: {D}
variables:
  - {{ id: x, label: Number to round, default: {sx} }}
  - {{ id: n, label: Significant figures, default: {sn}, min: 1, max: 15 }}
  - {{ id: dp, label: Decimal places, default: {sd}, min: 0, max: 10 }}
  - {{ id: r, label: Rounded to significant figures }}
  - {{ id: ex, label: Power of ten (scientific notation exponent), decimals: 0 }}
  - {{ id: m, label: Mantissa (r ÷ 10^exponent) }}
  - {{ id: rd, label: Rounded to decimal places }}
equations:
  - ex = floor(log10(abs(x)))
  - r = sign(x) * floor(abs(x) / 10^(ex - n + 1) + 0.5) * 10^(ex - n + 1)
  - m = r / 10^ex
  - rd = sign(x) * floor(abs(x) * 10^dp + 0.5) / 10^dp
faq:
  - q: How do you round to significant figures?
    a: Find the first non-zero digit, count n digits from it, and look at the next digit — if it is 5 or more round up, otherwise round down, then replace the dropped digits in front of the decimal point with zeros. 1,234.5678 to 3 sig figs is 1,230; 0.0045678 to 3 sig figs is 0.00457.
  - q: How many significant figures does 0.00450 have?
    a: Three. Leading zeros only locate the decimal point and never count; the 4, the 5 and the trailing zero after the decimal point do. In scientific notation it is 4.50 × 10⁻³, which makes the count obvious.
  - q: How many significant figures should an answer have?
    a: For multiplication and division, keep as many significant figures as the least precise input. For addition and subtraction, keep as many decimal places as the input with the fewest decimal places. Round only the final answer, not intermediate steps.
  - q: What is the difference between significant figures and decimal places?
    a: Decimal places count digits after the decimal point; significant figures count digits from the first non-zero digit. 0.00457 has 5 decimal places but only 3 significant figures, while 1,234.57 has 2 decimal places and 6 significant figures.
related: [math/scientific-notation, math/percent-error, math/fraction-to-decimal, math/exponent, math/logarithm, statistics/measurement-uncertainty]
''', f'''
## How to use the significant figures calculator

Enter the **number**, the number of **significant figures** you want and, separately, a number of **decimal places**. The calculator returns the number rounded to that many significant figures, its power-of-ten exponent and mantissa (so r = mantissa × 10<sup>exponent</sup> in scientific notation) and the number rounded to the chosen decimal places. Halves are rounded away from zero (2.5 → 3, −2.5 → −3). Trailing zeros that are significant (such as 2.50) cannot be shown in a number box, so write the result with the number of figures you asked for.

## Rounding formula

<p class="formula">e = ⌊log<sub>10</sub>|x|⌋ &nbsp;·&nbsp; r = sign(x) × ⌊|x| ÷ 10<sup>e − n + 1</sup> + ½⌋ × 10<sup>e − n + 1</sup></p>

<p class="formula">rounded to d decimal places = sign(x) × ⌊|x| × 10<sup>d</sup> + ½⌋ ÷ 10<sup>d</sup></p>

e is the position of the first significant digit (the exponent in scientific notation) and n the number of significant figures.

## Worked example

Round {sx} to {sn} significant figures and to {sd} decimal places:

- First significant digit: e = ⌊log<sub>10</sub> {sx}⌋ = **{sE}** (the number is {sx/10**sE:.8g} × 10<sup>{sE}</sup>)
- Rounding unit = 10<sup>{sE} − {sn} + 1</sup> = {10**(sE-sn+1):g}; {sx} ÷ {10**(sE-sn+1):g} = {sx/10**(sE-sn+1):.8g} → {math.floor(sx/10**(sE-sn+1)+0.5)}
- Rounded to {sn} sig figs = {math.floor(sx/10**(sE-sn+1)+0.5)} × {10**(sE-sn+1):g} = **{sR:,.0f}** = {sR/10**sE:g} × 10<sup>{sE}</sup>
- Rounded to {sd} decimal places = **{sRd:,.2f}**

## Rounding examples by number of significant figures

| Number | 1 s.f. | 2 s.f. | 3 s.f. | 4 s.f. | 5 s.f. |
|---|---|---|---|---|---|
{sf_rows}
## Rules for counting significant figures

| Number | Significant figures | Rule |
|---|---|---|
{ru_rows}
## Practical notes

- **Measurements:** quote a result to the precision of the instrument — a ruler read to 1 mm gives 23.4 cm (3 s.f.), not 23.4000 cm. Combine uncertainties with the [measurement uncertainty calculator](/statistics/measurement-uncertainty/).
- **Rounding 5s:** this calculator rounds halves away from zero. Some scientific software and IEEE 754 arithmetic use "round half to even" (banker's rounding), where 2.5 → 2 and 3.5 → 4; this avoids a small upward bias when many values are rounded.
- **Binary floating point:** a decimal like 2.675 is stored as 2.67499999…, so any computer may round it to 2.67 instead of 2.68. If an exact half matters, add a tiny amount or use more figures.
- Use the [scientific notation calculator](/math/scientific-notation/) to convert the result to and from E-notation.
''')

# ---------------------------------------------------------------- Inverse trig
ix = 0.5
iS, iC, iT = math.degrees(math.asin(ix)), math.degrees(math.acos(ix)), math.degrees(math.atan(ix))
iCt = 90 - iT
it_rows = ''
for x, lab in ((-1, '−1'), (-math.sqrt(3) / 2, '−√3/2 (−0.8660)'), (-math.sqrt(2) / 2, '−√2/2 (−0.7071)'), (-0.5, '−1/2'), (0, '0'),
               (0.5, '1/2'), (math.sqrt(2) / 2, '√2/2 (0.7071)'), (math.sqrt(3) / 2, '√3/2 (0.8660)'), (1, '1')):
    it_rows += f"| {lab} | {math.degrees(math.asin(x)):.4g}° | {math.asin(x):.4f} | {math.degrees(math.acos(x)):.4g}° | {math.acos(x):.4f} |\n"
ia_rows = ''
for x, lab in ((-math.sqrt(3), '−√3 (−1.732)'), (-1, '−1'), (-1 / math.sqrt(3), '−1/√3 (−0.5774)'), (0, '0'), (1 / math.sqrt(3), '1/√3 (0.5774)'),
               (0.5, '0.5'), (1, '1'), (math.sqrt(3), '√3 (1.732)'), (2, '2'), (10, '10'), (100, '100')):
    ia_rows += f"| {lab} | {math.degrees(math.atan(x)):.4f}° | {math.atan(x):.4f} | {90-math.degrees(math.atan(x)):.4f}° |\n"
sl_rows = ''.join(f"| {p}% | {p/100:g} | {math.degrees(math.atan(p/100)):.2f}° |\n" for p in (1, 2, 5, 8, 10, 15, 25, 50, 100))

P('math', 'inverse-trig', f'''
title: Inverse Trig Calculator (arcsin, arccos, arctan)
description: Calculate arcsin, arccos, arctan and arccot of any value in degrees and radians, with tables of exact angles and the principal value ranges of each function.
category: math
intro: "The inverse trigonometric functions run sine, cosine and tangent backwards: given a ratio, they return the angle. This inverse trig calculator finds arcsin, arccos, arctan and arccot of any number in degrees or radians, using the standard principal-value ranges, and also works the other way — enter an angle to get back the ratio. Use it to find an angle from the sides of a right triangle, a slope or a phasor."
keywords: [inverse trig calculator, arcsin calculator, arccos calculator, arctan calculator, inverse sine calculator, inverse cosine, inverse tangent calculator, sin⁻¹ cos⁻¹ tan⁻¹]
published: {D}
updated: {D}
variables:
  - {{ id: x, label: Value (ratio), default: {ix:g}, help: 'arcsin and arccos need −1 ≤ x ≤ 1; arctan and arccot accept any number.' }}
  - {{ id: asn, label: arcsin x (sin⁻¹), family: angle, unit: deg }}
  - {{ id: ac, label: arccos x (cos⁻¹), family: angle, unit: deg }}
  - {{ id: at, label: arctan x (tan⁻¹), family: angle, unit: deg }}
  - {{ id: act, label: arccot x (cot⁻¹), family: angle, unit: deg }}
equations:
  - asn = asin(x)
  - ac = acos(x)
  - at = atan(x)
  - act = pi / 2 - atan(x)
faq:
  - q: What is arcsin of 0.5?
    a: 30° (π/6 = 0.5236 rad), because sin 30° = 0.5. Sine is also 0.5 at 150°, but arcsin always returns the principal value between −90° and +90°. Likewise arccos 0.5 = 60° and arctan 0.5 = 26.565°.
  - q: What are the ranges of the inverse trig functions?
    a: "arcsin: −90° to 90° (−π/2 to π/2); arccos: 0° to 180° (0 to π); arctan: −90° to 90°, never reaching ±90°; arccot (as used here): 0° to 180°. These principal values make each inverse a true function with one answer."
  - q: Is sin⁻¹ the same as 1/sin?
    a: No. sin⁻¹ x means arcsin x, the angle whose sine is x. The reciprocal 1/sin x is the cosecant, csc x. Calculators label the inverse function sin⁻¹, which causes this common mix-up.
  - q: How do I find other angles with the same sine or cosine?
    a: "For sine, the other solution in 0–360° is 180° − arcsin x; for cosine it is 360° − arccos x; for tangent add 180°. The general solutions are θ = arcsin x + 360°k or 180° − arcsin x + 360°k, θ = ±arccos x + 360°k and θ = arctan x + 180°k."
related: [math/right-triangle-trig, math/angle-converter, math/law-of-sines, math/law-of-cosines, math/pythagorean-theorem, math/slope]
''', f'''
## How to use the inverse trig calculator

Enter a **value** — a ratio such as opposite ÷ hypotenuse — and read arcsin, arccos, arctan and arccot. Switch any result between degrees, radians, gradians or turns with its unit selector. To go the other way, clear the value and type an angle into one of the result boxes: the calculator returns the sine, cosine or tangent of that angle as the value. arcsin and arccos are only defined for values from −1 to 1.

## Inverse trig formulas and ranges

<p class="formula">θ = arcsin x ⇔ sin θ = x, −90° ≤ θ ≤ 90° &nbsp;·&nbsp; θ = arccos x ⇔ cos θ = x, 0° ≤ θ ≤ 180°</p>

<p class="formula">θ = arctan x ⇔ tan θ = x, −90° &lt; θ &lt; 90° &nbsp;·&nbsp; arccot x = 90° − arctan x</p>

Useful identities: arcsin x + arccos x = 90°, arctan x + arctan(1/x) = 90° for x &gt; 0, and arcsin(−x) = −arcsin x.

## Worked example

Find the angles whose sine, cosine, tangent and cotangent equal {ix:g}:

- arcsin {ix:g} = **{iS:g}°** ({math.asin(ix):.4f} rad), since sin 30° = 0.5
- arccos {ix:g} = **{iC:g}°** ({math.acos(ix):.4f} rad); check: {iS:g}° + {iC:g}° = 90°
- arctan {ix:g} = **{iT:.3f}°** ({math.atan(ix):.4f} rad)
- arccot {ix:g} = 90° − {iT:.3f}° = **{iCt:.3f}°**

In a right triangle with opposite side 1 and adjacent side 2, the angle is arctan(1/2) = {iT:.2f}°.

## arcsin and arccos of exact values

| x | arcsin x | arcsin (rad) | arccos x | arccos (rad) |
|---|---|---|---|---|
{it_rows}
## arctan and arccot values

| x | arctan x | arctan (rad) | arccot x |
|---|---|---|---|
{ia_rows}
## Gradient (percent slope) to angle

The angle of a slope is arctan(rise ÷ run):

| Gradient | rise ÷ run | Angle |
|---|---|---|
{sl_rows}
## Practical notes

- **Two-argument arctangent:** arctan(y/x) cannot tell (1, 1) from (−1, −1). For angles of vectors, phasors or coordinates use atan2(y, x), which returns the full −180° to 180° range — see the [vector calculator](/math/vector/).
- **Degrees vs radians:** spreadsheets and programming languages return radians; multiply by 180/π (57.2958) to get degrees. Convert other units with the [angle converter](/math/angle-converter/).
- **Solving triangles:** use arcsin with the [law of sines](/math/law-of-sines/) (watch for the ambiguous case where 180° − θ is also a solution) and arccos with the [law of cosines](/math/law-of-cosines/), which never has that ambiguity.
''')

print(len(DESC), 'pages:', ' '.join(DESC))
