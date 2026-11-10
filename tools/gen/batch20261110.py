"""Batch 2026-11-10 — 6 calculators: engineering (pressure vessel wall thickness, hydrostatic test pressure,
air receiver size), chemistry (conductivity cell constant), math (3×3 matrix determinant & inverse,
circle through three points). All reference tables are computed here; defaults match the worked examples."""
import sys, math, os, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro
D = '2026-11-10'
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

def sgn(x, f='{:g}'):
    """number with a typographic minus"""
    if x == 0: x = 0  # avoid printing a negative zero
    s = f.format(x)
    return s.replace('-', '−')

# ======================================================================= ENGINEERING

# ---------------------------------------------------------------- Pressure vessel wall thickness (ASME VIII-1 UG-27 / UG-32)
vP, vD, vS, vE, vCA, vtn = 1.0e6, 1500e-3, 138e6, 0.85, 3e-3, 10e-3
def vessel(P_, D_, S, E, CA, tn):
    R = D_ / 2 + CA                       # inside radius in the corroded condition
    tc = P_ * R / (S * E - 0.6 * P_)      # circumferential (longitudinal joints) UG-27(c)(1)
    tl = P_ * R / (2 * S * E + 0.4 * P_)  # longitudinal (circumferential joints) UG-27(c)(2)
    treq = max(tc, tl) + CA
    th = P_ * R / (2 * S * E - 0.2 * P_) + CA            # hemispherical head UG-32(f)
    te = P_ * 2 * R / (2 * S * E - 0.2 * P_) + CA        # 2:1 ellipsoidal head UG-32(d)
    tt = 0.885 * P_ * 2 * R / (S * E - 0.1 * P_) + CA    # torispherical head, L = D, r = 0.06 L, UG-32(e)
    tcor = tn - CA
    mawp = S * E * tcor / (R + 0.6 * tcor)
    chk = P_ / (S * E)
    return R, tc, tl, treq, th, te, tt, mawp, chk
vR, vtc, vtl, vtreq, vth, vte, vtt, vMAWP, vchk = vessel(vP, vD, vS, vE, vCA, vtn)
vt_rows = ''
for Dm in (500, 1000, 1500, 2000, 3000):
    cells = []
    for Pb in (5, 10, 20, 40):
        r = vessel(Pb * 1e5, Dm * 1e-3, 138e6, 1.0, 0, 0.01)
        cells.append(f"{r[1]*1000:.2f} mm")
    vt_rows += f"| {Dm:,} mm | " + ' | '.join(cells) + " |\n"
vh_rows = ''
for nm, i in (('Cylindrical shell', 3), ('Hemispherical head', 4), ('2:1 ellipsoidal head', 5), ('Torispherical head (6% knuckle)', 6)):
    r = vessel(vP, vD, vS, vE, vCA, vtn)
    vh_rows += f"| {nm} | {r[i]*1000:.2f} mm |\n"
P('engineering', 'pressure-vessel-thickness', f'''
title: Pressure Vessel Thickness Calculator (ASME VIII Shell & Head)
description: Calculate pressure vessel shell and head thickness with ASME VIII Div 1 UG-27 and UG-32 formulas, including joint efficiency, corrosion allowance and MAWP.
category: engineering
{intro("The wall of a cylindrical pressure vessel must resist the hoop stress from internal pressure, which is twice the longitudinal stress, so the circumferential formula almost always sets the thickness. This pressure vessel thickness calculator applies the ASME Section VIII Division 1 thin-wall formulas (UG-27 for the shell, UG-32 for hemispherical, 2:1 ellipsoidal and torispherical heads) with weld joint efficiency and corrosion allowance, and back-calculates the MAWP of the plate you choose.")}
keywords: [pressure vessel thickness calculator, asme pressure vessel thickness calculation, shell thickness calculation, ug-27 thickness, pressure vessel head thickness, ellipsoidal head thickness, mawp calculator]
updated: {D}
variables:
  - {{ id: P, label: Internal design pressure (gauge), family: pressure, unit: MPa, imperialUnit: psi, default: {vP/1e6:g}, min: 0, help: 'Include the static head of liquid at the point considered if it is significant.' }}
  - {{ id: Di, label: Inside diameter (new), family: length, unit: mm, imperialUnit: in, default: {vD*1000:g}, min: 0 }}
  - {{ id: S, label: Allowable stress at design temperature, family: pressure, unit: MPa, imperialUnit: psi, default: {vS/1e6:g}, min: 0, help: 'From ASME Section II Part D — e.g. SA-516 Gr 70 is 138 MPa (20 ksi) at moderate temperatures.' }}
  - id: E
    label: Weld joint efficiency E
    default: {vE:g}
    options:
      - {{ label: '1.00 — Type 1 butt weld, full radiography (or seamless)', value: 1.0 }}
      - {{ label: '0.85 — Type 1 butt weld, spot radiography', value: 0.85 }}
      - {{ label: '0.70 — Type 1 butt weld, no radiography', value: 0.7 }}
      - {{ label: '0.80 — Type 2 butt weld (backing strip), spot RT', value: 0.8 }}
      - {{ label: '0.65 — Type 2 butt weld, no radiography', value: 0.65 }}
  - {{ id: CA, label: Corrosion allowance, family: length, unit: mm, imperialUnit: in, default: {vCA*1000:g}, min: 0 }}
  - {{ id: tn, label: Nominal plate thickness chosen (for MAWP), family: length, unit: mm, imperialUnit: in, default: {vtn*1000:g}, min: 0 }}
  - {{ id: R, label: Inside radius, corroded, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: tc, label: Shell thickness — circumferential stress (no CA), family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: tl, label: Shell thickness — longitudinal stress (no CA), family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: treq, label: Minimum shell thickness incl. corrosion allowance, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: th, label: Hemispherical head thickness incl. CA, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: te, label: 2:1 ellipsoidal head thickness incl. CA, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: tt, label: Torispherical head thickness incl. CA, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: MAWP, label: Shell MAWP with the chosen plate (corroded), family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
  - id: chk
    label: Pressure ratio P ÷ (S E)
    min: 0
    decimals: 4
    bands:
      - {{ max: 0.385, label: Within the UG-27 thin-wall limit (≤ 0.385), color: '#16a34a' }}
      - {{ max: 1e9, label: Above 0.385 — use the thick-wall formulas of Appendix 1-2, color: '#dc2626' }}
equations:
  - R = Di / 2 + CA
  - tc = P * R / (S * E - 0.6 * P)
  - tl = P * R / (2 * S * E + 0.4 * P)
  - treq = max(tc, tl) + CA
  - th = P * R / (2 * S * E - 0.2 * P) + CA
  - te = P * 2 * R / (2 * S * E - 0.2 * P) + CA
  - tt = 0.885 * P * 2 * R / (S * E - 0.1 * P) + CA
  - MAWP = S * E * (tn - CA) / (R + 0.6 * (tn - CA))
  - chk = P / (S * E)
faq:
  - q: How do you calculate the thickness of a pressure vessel shell?
    a: For a cylindrical shell under internal pressure, ASME VIII-1 UG-27 gives t = P R ÷ (S E − 0.6 P) for the circumferential (hoop) stress and t = P R ÷ (2 S E + 0.4 P) for the longitudinal stress, where R is the inside radius in the corroded condition. Use the larger value and add the corrosion allowance.
  - q: What is weld joint efficiency?
    a: A factor E from ASME Table UW-12 that reduces the allowable stress to reflect the quality of weld inspection. A double-welded butt joint is 1.0 with full radiography, 0.85 with spot radiography and 0.70 with none. Seamless parts use E = 1.
  - q: Why is a 2:1 ellipsoidal head about as thick as the shell?
    a: Its formula t = P D ÷ (2 S E − 0.2 P) uses the diameter instead of the radius, so the result is almost the same as the shell's hoop-stress thickness. A hemispherical head needs only about half the shell thickness, and a standard torispherical head about 1.77 times.
  - q: What is MAWP?
    a: The maximum allowable working pressure is the highest gauge pressure the weakest part of the vessel can take at its design temperature, in the corroded condition. For the shell it is MAWP = S E t ÷ (R + 0.6 t), with t the nominal thickness minus corrosion allowance (and minus any mill under-tolerance).
related: [engineering/hydrostatic-test-pressure, engineering/barlow-formula, engineering/factor-of-safety, engineering/horizontal-tank-volume]
''', f'''
## How to use the pressure vessel thickness calculator

Enter the **design pressure** (gauge), the **inside diameter** of the new vessel, the **allowable stress** of the plate material at the design temperature, the **weld joint efficiency** and the **corrosion allowance**. The calculator gives the shell thickness for the hoop and longitudinal stresses, the minimum shell thickness including corrosion allowance, and the thickness of hemispherical, 2:1 ellipsoidal and torispherical heads. Enter the **plate thickness you intend to use** to see its MAWP. All formulas use the corroded inside radius, R = D/2 + CA.

## Pressure vessel thickness formulas (ASME VIII Div 1)

<p class="formula">Shell, hoop stress (UG-27): t = P R ÷ (S E − 0.6 P) &nbsp;·&nbsp; longitudinal: t = P R ÷ (2 S E + 0.4 P)</p>

<p class="formula">Hemispherical head (UG-32): t = P R ÷ (2 S E − 0.2 P) &nbsp;·&nbsp; 2:1 ellipsoidal: t = P D ÷ (2 S E − 0.2 P)</p>

<p class="formula">Torispherical head (crown radius = D, knuckle 6%): t = 0.885 P D ÷ (S E − 0.1 P) &nbsp;·&nbsp; MAWP = S E t ÷ (R + 0.6 t)</p>

The shell formulas are valid when t ≤ R/2 and P ≤ 0.385 S E. The head formulas give the thickness after forming — order heads with extra thickness for thinning in the knuckle.

## Worked example

A vessel with a {vD*1000:,.0f} mm inside diameter for {vP/1e6:g} MPa (10 bar g), SA-516 Gr 70 plate (S = {vS/1e6:g} MPa), spot-radiographed joints (E = {vE:g}) and {vCA*1000:g} mm corrosion allowance:

- Corroded inside radius R = {vD*1000/2:g} + {vCA*1000:g} = **{vR*1000:g} mm**
- Hoop stress: t = {vP/1e6:g} × {vR*1000:g} ÷ ({vS/1e6:g} × {vE:g} − 0.6 × {vP/1e6:g}) = **{vtc*1000:.2f} mm**
- Longitudinal stress: t = {vP/1e6:g} × {vR*1000:g} ÷ (2 × {vS/1e6:g} × {vE:g} + 0.4 × {vP/1e6:g}) = **{vtl*1000:.2f} mm**
- Minimum shell thickness = {vtc*1000:.2f} + {vCA*1000:g} = **{vtreq*1000:.2f} mm**, so a {vtn*1000:g} mm plate is chosen
- MAWP of the {vtn*1000:g} mm plate (corroded, {vtn*1000-vCA*1000:g} mm) = {vS/1e6:g} × {vE:g} × {vtn*1000-vCA*1000:g} ÷ ({vR*1000:g} + 0.6 × {vtn*1000-vCA*1000:g}) = **{vMAWP/1e6:.4f} MPa** ({vMAWP/1e5:.2f} bar g)
- Pressure ratio P ÷ (S E) = **{vchk:.4f}** — well within the thin-wall limit

Heads for the same vessel (including the {vCA*1000:g} mm corrosion allowance):

| Component | Minimum thickness |
|---|---|
{vh_rows}
## Shell thickness for common sizes

Hoop-stress thickness for S = 138 MPa, E = 1.0, no corrosion allowance:

| Inside diameter | 5 bar g | 10 bar g | 20 bar g | 40 bar g |
|---|---|---|---|---|
{vt_rows}
## Practical notes

- **Mill tolerance:** plate is usually ordered to the nominal thickness, but pipe used as a shell can be 12.5% thinner — subtract the under-tolerance before checking MAWP.
- **Minimum thickness:** UG-16 sets an absolute minimum of 1.5 mm (1/16 in) for shells and heads, excluding corrosion allowance; many owners specify 6 mm or more for fabrication and handling.
- External pressure (vacuum), wind, seismic, nozzle loads and supports often need more thickness than internal pressure — check them separately (UG-28 for vacuum).
- After fabrication the vessel is proved with a [hydrostatic test](/engineering/hydrostatic-test-pressure/) at about 1.3 × MAWP.
- This calculator is a design aid for preliminary sizing; a code vessel must be designed and stamped by a qualified engineer using the current edition of the code.
''')

# ---------------------------------------------------------------- Hydrostatic test pressure
hP, hk, hSt, hSd, hh, hrho = 10e5, 1.3, 138e6, 125e6, 6.0, 1000.0
def hydro(P_, k, St, Sd, h, rho):
    r = St / Sd; Pt = k * P_ * r; Pb = Pt + rho * G * h
    return r, Pt, Pb, 1.5 * Pt, 2 * Pt, 4 * Pt
hr, hPt, hPb, hG1, hG2, hG4 = hydro(hP, hk, hSt, hSd, hh, hrho)
ht_rows = ''
for Pb in (3.5, 5, 10, 16, 25, 40, 100):
    ht_rows += f"| {Pb:g} bar g | {1.3*Pb:.2f} bar g | {1.5*Pb:.2f} bar g | {1.1*Pb:.2f} bar g | {2*1.3*Pb:.1f} bar |\n"
hs_rows = ''
for h in (2, 5, 10, 20, 30, 50):
    hs_rows += f"| {h} m | {1000*G*h/1e5:.3f} bar | {1000*G*h/6894.757:.2f} psi |\n"
P('engineering', 'hydrostatic-test-pressure', f'''
title: Hydrostatic Test Pressure Calculator (ASME VIII & B31.3)
description: Calculate hydrostatic or pneumatic test pressure for vessels and piping to ASME VIII Div 1 and B31.3, with stress ratio, static head and gauge range.
category: engineering
{intro("A hydrostatic test proves a new pressure vessel or piping system by filling it with water and holding it above its design pressure, as described in [hydrostatic testing in the oil and gas industry](ib:hydrostatic-testing-in-oil-gas-industry). This hydrostatic test pressure calculator applies the ASME Section VIII Division 1 (1.3 × MAWP) and ASME B31.3 (1.5 × design pressure) factors with the temperature stress ratio, adds the static head at the lowest point and suggests a test gauge range.")}
keywords: [hydrostatic test pressure calculator, hydrotest pressure calculation, hydro test pressure formula, asme b31.3 test pressure, pressure vessel test pressure, pneumatic test pressure, 1.5 times design pressure]
updated: {D}
variables:
  - {{ id: P, label: Design pressure or MAWP (gauge), family: pressure, unit: bar, imperialUnit: psi, default: {hP/1e5:g}, min: 0 }}
  - id: k
    label: Code and test type
    default: {hk:g}
    options:
      - {{ label: 'ASME VIII Div 1 hydrostatic (UG-99) — 1.3', value: 1.3 }}
      - {{ label: 'ASME B31.3 piping hydrostatic (345.4) — 1.5', value: 1.5 }}
      - {{ label: 'Pneumatic test, ASME VIII-1 UG-100 or B31.3 — 1.1', value: 1.1 }}
  - {{ id: St, label: Allowable stress at test temperature, family: pressure, unit: MPa, imperialUnit: psi, default: {hSt/1e6:g}, min: 0 }}
  - {{ id: Sd, label: Allowable stress at design temperature, family: pressure, unit: MPa, imperialUnit: psi, default: {hSd/1e6:g}, min: 0, help: 'Equal to the test-temperature value for services at or near ambient temperature.' }}
  - {{ id: h, label: Height of the lowest point below the test gauge, family: length, unit: m, imperialUnit: ft, default: {hh:g}, min: 0 }}
  - {{ id: rho, label: Test fluid density, family: density, unit: kgm3, default: {hrho:g}, min: 0, help: 'Water ≈ 1000 kg/m³. Use 0 for a pneumatic test.' }}
  - {{ id: r, label: Stress ratio St ÷ Sd, min: 0, decimals: 4 }}
  - {{ id: Pt, label: Test pressure at the top (gauge), family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
  - {{ id: Pb, label: Pressure at the lowest point, family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
  - {{ id: G1, label: Test gauge range — minimum (1.5 × test), family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
  - {{ id: G2, label: Test gauge range — preferred (2 × test), family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
  - {{ id: G4, label: Test gauge range — maximum (4 × test), family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
equations:
  - r = St / Sd
  - Pt = k * P * r
  - Pb = Pt + rho * g0 * h
  - G1 = 1.5 * Pt
  - G2 = 2 * Pt
  - G4 = 4 * Pt
faq:
  - q: How is hydrostatic test pressure calculated?
    a: For a pressure vessel to ASME VIII Div 1 (UG-99), test pressure = 1.3 × MAWP × (stress at test temperature ÷ stress at design temperature), using the lowest ratio of the materials in the vessel. For process piping to ASME B31.3, P_T = 1.5 × P × S_T ÷ S, with the ratio not taken above 6.5.
  - q: Why is the test pressure 1.5 times the design pressure?
    a: The margin proves the strength and leak-tightness of the welds and joints with a safety allowance over normal operation. ASME VIII-1 used 1.5 until the 1999 addenda lowered it to 1.3 when the design margin on tensile strength was reduced; B31.3 piping still uses 1.5.
  - q: Where is the test pressure measured?
    a: ASME VIII-1 specifies the test pressure at the top of the vessel in its test position. The bottom sees the test pressure plus the water head, about 0.098 bar per metre, which must not over-stress any part.
  - q: What range should the test pressure gauge have?
    a: ASME VIII-1 UG-102 says the dial range should preferably be about double the test pressure, and never less than 1.5 times or more than 4 times it. Gauges must be calibrated, and a recorder or second gauge is common practice.
related: [engineering/pressure-vessel-thickness, engineering/barlow-formula, engineering/hydrostatic-pressure, engineering/absolute-gauge-pressure]
''', f'''
## How to use the hydrostatic test pressure calculator

Enter the **design pressure or MAWP**, choose the **code and test type**, and enter the **allowable stress** of the material at the test temperature and at the design temperature (the same value for ambient services). Add the **height of the lowest point** below the test gauge and the **test fluid density** to see the pressure at the bottom of the system. The calculator also gives the test gauge ranges allowed by UG-102.

## Hydrostatic test pressure formulas

<p class="formula">ASME VIII-1 UG-99: P<sub>T</sub> = 1.3 × MAWP × (S<sub>T</sub> ÷ S) &nbsp;·&nbsp; ASME B31.3: P<sub>T</sub> = 1.5 × P × (S<sub>T</sub> ÷ S)</p>

<p class="formula">Pneumatic: P<sub>T</sub> = 1.1 × P × (S<sub>T</sub> ÷ S) &nbsp;·&nbsp; P<sub>bottom</sub> = P<sub>T</sub> + ρ g h</p>

In B31.3 the stress ratio is capped at 6.5, and the test pressure is reduced if it would make the hoop stress exceed the yield strength at test temperature. Under the European PED (2014/68/EU) the vessel test pressure is at least the greater of 1.25 × the maximum allowable pressure (corrected for temperature) and 1.43 × PS.

## Worked example

A vessel with MAWP {hP/1e5:g} bar g at a design temperature where S = {hSd/1e6:g} MPa, tested with water at ambient (S<sub>T</sub> = {hSt/1e6:g} MPa) to ASME VIII-1; the bottom is {hh:g} m below the gauge:

- Stress ratio = {hSt/1e6:g} ÷ {hSd/1e6:g} = **{hr:.4f}**
- Test pressure = 1.3 × {hP/1e5:g} × {hr:.4f} = **{hPt/1e5:.2f} bar g** at the top
- At the bottom: {hPt/1e5:.2f} + 1000 × 9.807 × {hh:g} ÷ 10⁵ = **{hPb/1e5:.2f} bar g**
- Test gauge: at least **{hG1/1e5:.1f} bar**, preferably about **{hG2/1e5:.1f} bar** (a 0–25 or 0–40 bar gauge), and not more than **{hG4/1e5:.1f} bar**

## Test pressure without temperature correction

For ambient-temperature services (S<sub>T</sub> = S). The last column is the preferred gauge range for an ASME VIII-1 test.

| Design pressure | ASME VIII-1 hydro (1.3×) | B31.3 hydro (1.5×) | Pneumatic (1.1×) | Gauge range for 1.3× |
|---|---|---|---|---|
{ht_rows}
## Static head of water added at the lowest point

| Height below gauge | Extra pressure | Extra pressure |
|---|---|---|
{hs_rows}
## Practical notes

- **Hold time:** B31.3 requires at least 10 minutes at test pressure; ASME VIII-1 then lowers the pressure to at least test pressure ÷ 1.3 for the visual inspection of all joints.
- **Metal temperature:** keep it at least 17 °C (30 °F) above the minimum design metal temperature during a VIII-1 test, but not over 48 °C (120 °F) for close inspection, to avoid brittle fracture.
- **Vent the high points** before pressurising — trapped air makes a hydrotest store energy like a pneumatic test.
- **Isolate instruments**, relief valves and anything with a lower rating, following a written [hydrotest procedure for piping](ib:hydrotest-procedure-for-piping-system), and [select a calibrated test gauge](ib:pressure-gauge-selection-7-factors) with the right range.
- A pneumatic test stores far more energy than a hydrotest; use it only when water cannot be used, with an exclusion zone and a staged pressure increase.
''')

# ---------------------------------------------------------------- Air receiver size
aQc, aQd, at, aPa, aP1, aP2, af = 0.100, 0.150, 120.0, 101325.0, 7.5e5, 6.0e5, 60.0
def receiver(Qc, Qd, t, Pa, P1, P2, f):
    dP = P1 - P2
    Vs = t * max(Qd - Qc, 0) * Pa / dP                 # storage for a demand event (drawdown)
    Vc = 0.25 * Qc * Pa / ((f / 3600) * dP)            # load/unload cycling (T0 = T1)
    return dP, Vs, Vc, max(Vs, Vc)
adP, aVs, aVc, aV = receiver(aQc, aQd, at, aPa, aP1, aP2, af)
ar_rows = ''
for Qc in (0.010, 0.025, 0.050, 0.100, 0.200, 0.400):
    cells = []
    for dPb in (0.5, 1.0, 1.5, 2.0):
        cells.append(f"{0.25*Qc*101325/((60/3600)*dPb*1e5)*1000:,.0f} L")
    ar_rows += f"| {Qc*1000:g} L/s ({Qc*60:.1f} m³/min, {Qc/0.028316846592*60:.0f} cfm) | " + ' | '.join(cells) + " |\n"
ad_rows = ''
for t in (30, 60, 120, 300):
    cells = []
    for net in (0.010, 0.050, 0.100):
        cells.append(f"{t*net*101325/1.5e5:.2f} m³")
    ad_rows += f"| {t:g} s | " + ' | '.join(cells) + " |\n"
P('engineering', 'air-receiver-size', f'''
title: Air Receiver Size Calculator (Compressed Air Tank Volume)
description: Calculate compressed air receiver tank size for a peak demand event and for compressor load/unload cycling, from flow, pressure band and time.
category: engineering
{intro("A compressed air receiver stores air between the compressor's cut-out and cut-in pressures, covering short demand peaks and stopping the compressor from cycling too often. This air receiver size calculator works out the tank volume needed to ride through a demand event from the pressure drop you can accept, and the volume needed to keep a load/unload compressor within its maximum cycle rate, then gives the larger of the two.")}
keywords: [air receiver size calculator, air receiver tank sizing, compressed air receiver calculation, air tank size calculator, receiver volume formula, compressor tank size, air receiver capacity]
updated: {D}
variables:
  - {{ id: Qc, label: Compressor capacity (free air delivery), family: flow, unit: Ls, imperialUnit: cfm, default: {aQc*1000:g}, min: 0 }}
  - {{ id: Qd, label: Peak air demand during the event (free air), family: flow, unit: Ls, imperialUnit: cfm, default: {aQd*1000:g}, min: 0 }}
  - {{ id: t, label: Duration of the peak demand, family: seconds, unit: s, default: {at:g}, min: 0 }}
  - {{ id: Pa, label: Atmospheric pressure (absolute), family: pressure, unit: kPa, imperialUnit: psi, default: {aPa/1000:g}, min: 0 }}
  - {{ id: P1, label: Receiver pressure at start (cut-out / unload), family: pressure, unit: bar, imperialUnit: psi, default: {aP1/1e5:g}, min: 0 }}
  - {{ id: P2, label: Minimum acceptable pressure (cut-in / load), family: pressure, unit: bar, imperialUnit: psi, default: {aP2/1e5:g}, min: 0, help: 'Same reference as P1 (both gauge or both absolute) — only the difference matters.' }}
  - {{ id: f, label: Maximum compressor load cycles per hour, suffix: per h, default: {af:g}, min: 0, help: 'From the compressor maker; often 30–120 per hour for load/unload screw compressors.' }}
  - {{ id: dP, label: Usable pressure band P1 − P2, family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
  - {{ id: Vs, label: Volume for the demand event, family: volume, unit: m3, imperialUnit: galUS, min: 0 }}
  - {{ id: Vc, label: Volume for compressor cycling, family: volume, unit: m3, imperialUnit: galUS, min: 0 }}
  - {{ id: V, label: Recommended receiver volume (larger of the two), family: volume, unit: m3, imperialUnit: galUS, min: 0 }}
equations:
  - dP = P1 - P2
  - Vs = t * max(Qd - Qc, 0) * Pa / dP
  - Vc = 0.25 * Qc * Pa / ((f / 3600) * dP)
  - V = max(Vs, Vc)
faq:
  - q: How do you calculate air receiver size?
    a: For a demand event, V = t × (Q_demand − Q_compressor) × P_atm ÷ (P₁ − P₂), with flows as free air. For load/unload control, V = Q_c × P_atm ÷ (4 × f_max × ΔP), where f_max is the maximum number of load cycles per unit time. Use consistent units and pick the larger volume.
  - q: Why is the compressor flow multiplied by 0.25 in the cycling formula?
    a: The time between load cycles is shortest when the demand is exactly half of the compressor capacity. At that point the receiver fills and empties at the same rate, and the cycle time is 4V ΔP ÷ (Q_c P_atm), which gives the factor 1/4.
  - q: Is the pressure band in gauge or absolute pressure?
    a: Either, as long as both pressures use the same reference — only the difference P₁ − P₂ appears. Atmospheric pressure must be absolute, because it converts free air into compressed volume.
  - q: Should I use a wet or a dry receiver?
    a: A wet receiver before the dryer cools the air and drops out condensate, and smooths the compressor's flow. A dry receiver after the dryer stores clean air close to large intermittent users. Many systems use both, and the volumes add.
related: [engineering/compressor-power, engineering/absolute-gauge-pressure, engineering/gas-flow-correction, physics/ideal-gas-law]
''', f'''
## How to use the air receiver size calculator

Enter the **compressor capacity** and the **peak demand** as free air delivery, the **duration** of the peak, the local **atmospheric pressure**, the **receiver pressure at the start** of the event (the compressor unload or cut-out pressure) and the **lowest pressure** your equipment can accept. Add the compressor's **maximum load cycles per hour**. The calculator gives the volume needed for each case and recommends the larger one. If the compressor is off during the event (for example, a backup tank), enter 0 for its capacity in the demand-event case.

## Air receiver sizing formulas

<p class="formula">Demand event: V = t × (Q<sub>d</sub> − Q<sub>c</sub>) × P<sub>atm</sub> ÷ (P<sub>1</sub> − P<sub>2</sub>)</p>

<p class="formula">Load/unload cycling: V = 0.25 × Q<sub>c</sub> × P<sub>atm</sub> ÷ (f<sub>max</sub> × (P<sub>1</sub> − P<sub>2</sub>))</p>

Both assume the air in the receiver stays at about the same temperature as the intake air. The cycling formula is the one used in compressor manufacturers' sizing guides; the worst case is a demand equal to half the compressor capacity.

## Worked example

A compressor delivering {aQc*1000:g} L/s ({aQc*60:g} m³/min) between {aP1/1e5:g} and {aP2/1e5:g} bar g, with a {at:g} s peak demand of {aQd*1000:g} L/s and a limit of {af:g} load cycles per hour, at sea level:

- Pressure band = {aP1/1e5:g} − {aP2/1e5:g} = **{adP/1e5:g} bar**
- Demand event: V = {at:g} × ({aQd:g} − {aQc:g}) × {aPa:,.0f} ÷ {adP:,.0f} = **{aVs:.3f} m³**
- Cycling: V = 0.25 × {aQc:g} × {aPa:,.0f} ÷ ({af:g}/3600 × {adP:,.0f}) = **{aVc:.3f} m³**
- Recommended receiver: **{aV:.3f} m³** ({aV/0.003785411784:,.0f} US gal) — the next standard size is a 5 m³ tank

## Receiver volume for compressor cycling

At 60 load cycles per hour and sea-level intake:

| Compressor capacity | ΔP = 0.5 bar | ΔP = 1.0 bar | ΔP = 1.5 bar | ΔP = 2.0 bar |
|---|---|---|---|---|
{ar_rows}
## Receiver volume for a demand event

Net shortfall (demand − compressor) and a 1.5 bar usable band:

| Event duration | 10 L/s shortfall | 50 L/s shortfall | 100 L/s shortfall |
|---|---|---|---|
{ad_rows}
## Practical notes

- **Doubling the pressure band halves the receiver**, but every 1 bar of extra discharge pressure costs about 7% more compressor energy — a pressure/flow controller downstream of a large receiver is often cheaper.
- Variable-speed compressors need much less storage than load/unload machines; follow the maker's minimum system volume.
- Receivers are pressure vessels: they need a relief valve sized for the full compressor capacity, a pressure gauge, an automatic drain and periodic inspection — see the [pressure vessel thickness calculator](/engineering/pressure-vessel-thickness/).
- Include the volume of large distribution headers when they are close to the users; piping volume acts as storage too.
''')

# ======================================================================= CHEMISTRY

# ---------------------------------------------------------------- Conductivity cell constant
cks, cT, ca, cRs, cKn, cRx = 1413.0, 22.0, 1.9, 720.0, 1.0, 2400.0
def cell(ks, T, a, Rs, Kn, Rx):
    f = 1 + a / 100 * (T - 25); kT = ks * f; K = kT * 1e-6 * Rs; err = (K / Kn - 1) * 100
    kx = K / Rx * 1e6; kx25 = kx / f
    return f, kT, K, err, kx, kx25
cf, ckT, cK, cerr, ckx, ckx25 = cell(cks, cT, ca, cRs, cKn, cRx)
STD = (('0.001 mol/L KCl', 146.9), ('0.01 mol/L KCl', 1413.0), ('0.1 mol/L KCl', 12880.0))
cr_rows = ''
for K in (0.01, 0.1, 0.5, 1.0, 10.0):
    cr_rows += f"| {K:g} cm⁻¹ | " + ' | '.join((f"{K/(ks*1e-6):,.0f} Ω" if K/(ks*1e-6) >= 1000 else f"{K/(ks*1e-6):.4g} Ω") for _, ks in STD) + " |\n"
cs_rows = ''
for K, rng in ((0.01, 'ultrapure and pure water, < 20 µS/cm'), (0.1, 'boiler feed, condensate, RO permeate, 1–200 µS/cm'),
               (1.0, 'drinking, cooling and process water, 10–20,000 µS/cm'), (10.0, 'brines, acids, CIP solutions, > 1,000 µS/cm')):
    cs_rows += f"| {K:g} cm⁻¹ | {rng} |\n"
P('chemistry', 'conductivity-cell-constant', f'''
title: Conductivity Cell Constant Calculator (KCl Calibration)
description: Calculate a conductivity cell constant K from a KCl standard and the measured resistance, with temperature correction, and convert sample readings to µS/cm.
category: chemistry
{intro("A conductivity cell measures resistance, and its cell constant K (the ratio of electrode spacing to electrode area, in cm⁻¹) converts that resistance into conductivity, κ = K ÷ R. This conductivity cell constant calculator finds K from a potassium chloride standard of known conductivity, corrects the standard for the measuring temperature, shows the deviation from the nominal constant and converts a sample resistance into conductivity at 25 °C — the [cell constant calibration](ib:conductivity-sensor-cell-constant-calibration) done on every conductivity analyser.")}
keywords: [conductivity cell constant calculator, cell constant calculation, conductivity cell constant formula, kcl conductivity standard, cell constant k, conductivity calibration, conductivity meter calibration]
updated: {D}
variables:
  - {{ id: ks, label: Conductivity of the standard at 25 °C, suffix: µS/cm, default: {cks:g}, min: 0, help: 'KCl at 25 °C: 0.001 mol/L = 146.9 µS/cm, 0.01 mol/L = 1413 µS/cm, 0.1 mol/L = 12,880 µS/cm.' }}
  - {{ id: T, label: Temperature during measurement, family: temperature, unit: C, imperialUnit: F, default: {cT:g} }}
  - {{ id: a, label: Temperature coefficient, suffix: '%/°C', default: {ca:g}, min: 0, help: 'KCl standards ≈ 1.9–2.0 %/°C; natural waters ≈ 2 %/°C.' }}
  - {{ id: Rs, label: Measured resistance in the standard, family: resistance, unit: ohm, default: {cRs:g}, min: 0 }}
  - {{ id: Kn, label: Nominal cell constant, suffix: cm⁻¹, default: {cKn:g}, min: 0 }}
  - {{ id: Rx, label: Measured resistance in the sample (same temperature), family: resistance, unit: ohm, default: {cRx:g}, min: 0 }}
  - {{ id: kT, label: Conductivity of the standard at the measuring temperature, suffix: µS/cm, min: 0, decimals: 1 }}
  - {{ id: K, label: Cell constant K, suffix: cm⁻¹, min: 0, decimals: 4 }}
  - id: err
    label: Deviation from the nominal cell constant
    suffix: '%'
    decimals: 2
    bands:
      - {{ max: -10, label: More than 10% low — clean or replace the cell, color: '#dc2626' }}
      - {{ max: -2, label: 2–10% low — enter the measured K, color: '#eab308' }}
      - {{ max: 2, label: Within ±2% of nominal, color: '#16a34a' }}
      - {{ max: 10, label: 2–10% high — enter the measured K, color: '#eab308' }}
      - {{ max: 1e9, label: More than 10% high — check the cell and standard, color: '#dc2626' }}
  - {{ id: kx, label: Sample conductivity at measuring temperature, suffix: µS/cm, min: 0, decimals: 1 }}
  - {{ id: kx25, label: Sample conductivity compensated to 25 °C, suffix: µS/cm, min: 0, decimals: 1 }}
equations:
  - kT = ks * (1 + a / 100 * (T - 298.15))
  - K = kT * 1e-6 * Rs
  - err = (K / Kn - 1) * 100
  - kx = K / Rx * 1e6
  - kx25 = kx / (1 + a / 100 * (T - 298.15))
faq:
  - q: How do you calculate the cell constant of a conductivity cell?
    a: Measure the resistance R of the cell in a standard solution of known conductivity κ and multiply, K = κ × R. With κ in S/cm and R in ohms, K is in cm⁻¹. For example 1413 µS/cm × 708 Ω = 1.000 cm⁻¹.
  - q: Which KCl standard should I use?
    a: Choose a standard close to the conductivity you will measure — 146.9 µS/cm (0.001 mol/L) for pure water cells with K = 0.1, 1413 µS/cm (0.01 mol/L) for K = 1 cells and 12,880 µS/cm (0.1 mol/L) for K = 10 cells. Very dilute standards below about 100 µS/cm absorb CO₂ from the air and are hard to keep accurate.
  - q: Why does temperature matter for conductivity?
    a: Ion mobility rises with temperature, so conductivity increases by about 2% per °C. Standards are certified at 25 °C; correct them to the measuring temperature (or measure at 25 °C), and compensate sample readings back to 25 °C with the same coefficient.
  - q: How far can the cell constant drift from its nominal value?
    a: Manufacturers state the nominal K to about ±5–10%, which is why each cell is calibrated. A K that has fallen noticeably since the last calibration usually means fouling or coating of the electrodes, and the cell should be cleaned before recalibrating.
related: [chemistry/tds-conductivity, chemistry/water-hardness, chemistry/ppm, engineering/calibration-error]
''', f'''
## How to use the conductivity cell constant calculator

Enter the **conductivity of the standard** at 25 °C, the **temperature** of the standard during the measurement, its **temperature coefficient** and the **resistance** your meter reads with the cell in the standard. The calculator gives the conductivity of the standard at that temperature, the **cell constant K** and its deviation from the **nominal constant**. Enter a **sample resistance** to convert it into conductivity, both at the measuring temperature and compensated to 25 °C. If your meter reads conductance instead, resistance = 1 ÷ conductance (1 mS → 1,000 Ω).

## Cell constant formulas

<p class="formula">κ<sub>T</sub> = κ<sub>25</sub> × [1 + α (T − 25)] &nbsp;·&nbsp; K = κ<sub>T</sub> × R<sub>std</sub></p>

<p class="formula">κ<sub>sample</sub> = K ÷ R<sub>sample</sub> &nbsp;·&nbsp; κ<sub>25</sub> = κ<sub>T</sub> ÷ [1 + α (T − 25)]</p>

K = d ÷ A for two parallel electrodes a distance d apart with area A. Linear temperature compensation with α ≈ 2 %/°C is accurate within a few degrees of 25 °C; for pure water, non-linear compensation is needed — see [how conductivity sensors work](ib:conductivity-sensor-working).

## Worked example

A K = 1 cell is placed in 0.01 mol/L KCl ({cks:g} µS/cm at 25 °C) at {cT:g} °C and reads {cRs:g} Ω:

- Standard at {cT:g} °C: {cks:g} × [1 + {ca/100:g} × ({cT:g} − 25)] = **{ckT:.1f} µS/cm**
- Cell constant K = {ckT:.1f} × 10⁻⁶ × {cRs:g} = **{cK:.4f} cm⁻¹**, which is **{sgn(cerr, '{:.2f}')}%** from the nominal 1.0 — enter {cK:.4f} in the analyser
- A sample reading {cRx:,.0f} Ω at the same temperature: κ = {cK:.4f} ÷ {cRx:,.0f} = **{ckx:.1f} µS/cm**, or **{ckx25:.1f} µS/cm** at 25 °C

## Expected resistance in KCl standards (25 °C)

| Cell constant | 0.001 mol/L KCl (146.9 µS/cm) | 0.01 mol/L KCl (1413 µS/cm) | 0.1 mol/L KCl (12,880 µS/cm) |
|---|---|---|---|
{cr_rows}
## Choosing a cell constant

| Cell constant | Typical application |
|---|---|
{cs_rows}
## Practical notes

- **Rinse the cell** with deionised water and then with a little of the standard before measuring, so the standard is not diluted.
- Keep the standard at a stable temperature and measure it with the same probe sensor that the analyser uses for compensation.
- Avoid air bubbles between the electrodes; tap the cell or immerse it at an angle.
- Toroidal (inductive) sensors have a cell factor too, but it also depends on the distance to the pipe wall — calibrate them installed or in a large container.
''')

# ======================================================================= MATH

# ---------------------------------------------------------------- 3×3 matrix determinant & inverse
M0 = [[2, 1, 1], [1, 3, 2], [1, 0, 0]]
def det3(m):
    (a, b, c), (d, e, f), (g, h, i) = m
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
def inv3(m):
    (a, b, c), (d, e, f), (g, h, i) = m
    dt = det3(m)
    cof = [[e * i - f * h, -(d * i - f * g), d * h - e * g],
           [-(b * i - c * h), a * i - c * g, -(a * h - b * g)],
           [b * f - c * e, -(a * f - c * d), a * e - b * d]]
    return [[cof[j][k] / dt for j in range(3)] for k in range(3)], cof
mdet = det3(M0); minv, mcof = inv3(M0)
mtr = M0[0][0] + M0[1][1] + M0[2][2]
# check A·A⁻¹ = I
for r_ in range(3):
    for c_ in range(3):
        s_ = sum(M0[r_][k] * minv[k][c_] for k in range(3)); assert abs(s_ - (r_ == c_)) < 1e-12
def mat(m, f='{:g}'):
    return ' ; '.join(' '.join(sgn(x, f) for x in row) for row in m)
EXM = [('Identity', [[1, 0, 0], [0, 1, 0], [0, 0, 1]]), ('Diagonal 2, 3, 4', [[2, 0, 0], [0, 3, 0], [0, 0, 4]]),
       ('Rotation 90° about z', [[0, -1, 0], [1, 0, 0], [0, 0, 1]]), ('Upper triangular', [[1, 2, 3], [0, 4, 5], [0, 0, 6]]),
       ('Rows 1 2 3 / 4 5 6 / 7 8 9', [[1, 2, 3], [4, 5, 6], [7, 8, 9]]), ('This page\'s example', M0)]
mx_rows = ''
for nm, m in EXM:
    dt = det3(m)
    mx_rows += f"| {nm} | {mat(m)} | {sgn(dt)} | {'singular — no inverse' if abs(dt) < 1e-12 else 'invertible'} |\n"
mvars = ''
for r_ in range(3):
    for c_ in range(3):
        mvars += f"  - {{ id: a{r_+1}{c_+1}, label: 'Row {r_+1}, column {c_+1} (a{r_+1}{c_+1})', default: {M0[r_][c_]} }}\n"
mout = ''
for r_ in range(3):
    for c_ in range(3):
        mout += f"  - {{ id: i{r_+1}{c_+1}, label: 'Inverse, row {r_+1} column {c_+1}', decimals: 6 }}\n"
# inverse element (r,c) = cofactor(c,r)/det
CF = {(1, 1): 'a22 * a33 - a23 * a32', (1, 2): '-(a21 * a33 - a23 * a31)', (1, 3): 'a21 * a32 - a22 * a31',
      (2, 1): '-(a12 * a33 - a13 * a32)', (2, 2): 'a11 * a33 - a13 * a31', (2, 3): '-(a11 * a32 - a12 * a31)',
      (3, 1): 'a12 * a23 - a13 * a22', (3, 2): '-(a11 * a23 - a13 * a21)', (3, 3): 'a11 * a22 - a12 * a21'}
meqs = ''
for r_ in range(1, 4):
    for c_ in range(1, 4):
        meqs += f"  - i{r_}{c_} = ({CF[(c_, r_)]}) / det\n"
P('math', 'matrix-determinant', f'''
title: Matrix Determinant Calculator 3×3 (with Inverse Matrix)
description: Calculate the determinant, trace and inverse of a 3×3 matrix by cofactor expansion, with step-by-step working — also works for 2×2 matrices.
category: math
{intro("The determinant of a square matrix is a single number that tells you whether the matrix can be inverted, how it scales areas and volumes, and whether a system of linear equations has a unique solution. This matrix determinant calculator expands a 3×3 matrix by cofactors, gives its trace and, when the determinant is not zero, the full inverse matrix from the adjugate.")}
keywords: [matrix determinant calculator, determinant calculator 3x3, inverse matrix calculator, 3x3 matrix inverse, determinant of a matrix, cofactor expansion, adjugate matrix]
updated: {D}
variables:
{mvars.rstrip()}
  - {{ id: det, label: Determinant det(A), decimals: 6 }}
  - {{ id: tr, label: Trace (sum of the diagonal), decimals: 6 }}
{mout.rstrip()}
equations:
  - det = a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31)
  - tr = a11 + a22 + a33
{meqs.rstrip()}
faq:
  - q: How do you find the determinant of a 3×3 matrix?
    a: Expand along the first row, det = a₁₁(a₂₂a₃₃ − a₂₃a₃₂) − a₁₂(a₂₁a₃₃ − a₂₃a₃₁) + a₁₃(a₂₁a₃₂ − a₂₂a₃₁). Each bracket is the determinant of the 2×2 minor left after deleting that element's row and column, and the signs alternate +, −, +.
  - q: How do you find the inverse of a 3×3 matrix?
    a: Replace every element by its cofactor, transpose the result to get the adjugate, and divide by the determinant, A⁻¹ = adj(A) ÷ det(A). Check it by multiplying, A × A⁻¹ = I.
  - q: What does a determinant of zero mean?
    a: The matrix is singular — its rows (and columns) are linearly dependent, it squashes space into a plane or line, and it has no inverse. A system of equations with that coefficient matrix has either no solution or infinitely many.
  - q: How do I use this for a 2×2 matrix?
    a: Enter the 2×2 matrix in the top-left corner, set a₃₃ = 1 and the other entries of row 3 and column 3 to 0. The determinant is then ad − bc and the top-left block of the inverse is the 2×2 inverse.
related: [math/system-of-3-equations, math/system-of-equations, math/vector, math/cubic-equation]
''', f'''
## How to use the matrix determinant calculator

Enter the nine elements of the 3×3 matrix row by row — a₁₂ is row 1, column 2. The calculator gives the **determinant**, the **trace** and the nine elements of the **inverse matrix**. If the determinant is zero the matrix is singular and the inverse elements show as infinite or undefined. Fractions such as 1/3 can be typed as decimals.

## Determinant and inverse formulas

<p class="formula">det A = a<sub>11</sub>(a<sub>22</sub>a<sub>33</sub> − a<sub>23</sub>a<sub>32</sub>) − a<sub>12</sub>(a<sub>21</sub>a<sub>33</sub> − a<sub>23</sub>a<sub>31</sub>) + a<sub>13</sub>(a<sub>21</sub>a<sub>32</sub> − a<sub>22</sub>a<sub>31</sub>)</p>

<p class="formula">C<sub>ij</sub> = (−1)<sup>i+j</sup> M<sub>ij</sub> &nbsp;·&nbsp; A⁻¹ = adj(A) ÷ det A = C<sup>T</sup> ÷ det A</p>

M<sub>ij</sub> is the minor — the determinant of the 2×2 matrix left after deleting row i and column j. For a 2×2 matrix the determinant is ad − bc and the inverse is [d −b ; −c a] ÷ (ad − bc).

## Worked example

A = [{mat(M0)}] (rows separated by semicolons):

- det A = 2 × (3 × 0 − 2 × 0) − 1 × (1 × 0 − 2 × 1) + 1 × (1 × 0 − 3 × 1) = 0 + 2 − 3 = **{sgn(mdet)}**
- Trace = 2 + 3 + 0 = **{mtr}**
- Cofactor matrix C = [{mat(mcof)}]
- Inverse A⁻¹ = Cᵀ ÷ ({sgn(mdet)}) = **[{mat(minv)}]**
- Check: A × A⁻¹ gives the identity matrix

## Determinants of common matrices

| Matrix | Elements (rows) | Determinant | Inverse |
|---|---|---|---|
{mx_rows}
## Properties of determinants

- Swapping two rows changes the sign of the determinant; multiplying a row by k multiplies it by k.
- Adding a multiple of one row to another leaves the determinant unchanged — the basis of Gaussian elimination.
- det(AB) = det A × det B, det(Aᵀ) = det A and det(A⁻¹) = 1 ÷ det A.
- The determinant of a triangular matrix is the product of its diagonal elements.
- |det A| is the volume of the parallelepiped spanned by the rows; its sign tells you whether the orientation is flipped.

## Practical notes

- A determinant that is tiny compared with the size of the elements means the matrix is **ill-conditioned**: small changes in the data cause large changes in the inverse or in the solution of the equations.
- To solve **A x = b** for three unknowns, use the [system of 3 equations calculator](/math/system-of-3-equations/) — it applies Cramer's rule, which is det-based too.
- In engineering, 3×3 determinants appear in vector cross products, rotation matrices, stress tensors and the Clarke and Park transformations.
''')

# ---------------------------------------------------------------- Circle through three points
cx1, cy1, cx2, cy2, cx3, cy3 = 1.0, 1.0, 2.0, 4.0, 5.0, 3.0
def circ(x1, y1, x2, y2, x3, y3):
    Dd = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    s1, s2, s3 = x1 * x1 + y1 * y1, x2 * x2 + y2 * y2, x3 * x3 + y3 * y3
    h = (s1 * (y2 - y3) + s2 * (y3 - y1) + s3 * (y1 - y2)) / Dd
    k = (s1 * (x3 - x2) + s2 * (x1 - x3) + s3 * (x2 - x1)) / Dd
    r = math.hypot(x1 - h, y1 - k)
    return Dd, h, k, r, -2 * h, -2 * k, h * h + k * k - r * r, 2 * pi * r, pi * r * r
cD, ch, ck, cr, cDg, cEg, cFg, cC, cA = circ(cx1, cy1, cx2, cy2, cx3, cy3)
CX = [((0, 0), (4, 0), (0, 3)), ((1, 0), (0, 1), (-1, 0)), ((0, 0), (2, 2), (4, 0)), ((-3, 4), (4, 3), (5, 0)), ((1, 1), (2, 4), (5, 3)), ((0, 0), (1, 1), (2, 2))]
cx_rows = ''
for (a, b, c) in CX:
    Dd = 2 * (a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1]))
    pts = f"({sgn(a[0])}, {sgn(a[1])}), ({sgn(b[0])}, {sgn(b[1])}), ({sgn(c[0])}, {sgn(c[1])})"
    if Dd == 0:
        cx_rows += f"| {pts} | collinear — no circle | — |\n"
    else:
        r_ = circ(*a, *b, *c)
        cx_rows += f"| {pts} | ({sgn(r_[1], '{:.4g}')}, {sgn(r_[2], '{:.4g}')}) | {r_[3]:.4g} |\n"
P('math', 'circle-three-points', f'''
title: Circle Through 3 Points Calculator (Centre, Radius, Equation)
description: Find the circle through three points — its centre, radius, standard and general equations, circumference and area — with the circumcircle formulas.
category: math
{intro("Any three points that are not on one straight line lie on exactly one circle, the circumcircle of the triangle they form. This circle through 3 points calculator finds the centre (h, k) and radius r of that circle, writes its standard equation (x − h)² + (y − k)² = r² and its general form x² + y² + Dx + Ey + F = 0, and gives the circumference and area — handy for fitting an arc to three measured points.")}
keywords: [circle through 3 points calculator, circle from three points, find center and radius of circle, equation of a circle calculator, circumcircle calculator, circle equation from points, three point circle]
updated: {D}
variables:
  - {{ id: x1, label: Point 1 — x₁, default: {cx1:g} }}
  - {{ id: y1, label: Point 1 — y₁, default: {cy1:g} }}
  - {{ id: x2, label: Point 2 — x₂, default: {cx2:g} }}
  - {{ id: y2, label: Point 2 — y₂, default: {cy2:g} }}
  - {{ id: x3, label: Point 3 — x₃, default: {cx3:g} }}
  - {{ id: y3, label: Point 3 — y₃, default: {cy3:g} }}
  - {{ id: Dd, label: 'Determinant term d (0 = points are collinear)', decimals: 6 }}
  - {{ id: h, label: Centre x-coordinate h, decimals: 6 }}
  - {{ id: k, label: Centre y-coordinate k, decimals: 6 }}
  - {{ id: r, label: Radius r, min: 0, decimals: 6 }}
  - {{ id: Dg, label: 'General form coefficient D (= −2h)', decimals: 6 }}
  - {{ id: Eg, label: 'General form coefficient E (= −2k)', decimals: 6 }}
  - {{ id: Fg, label: 'General form coefficient F (= h² + k² − r²)', decimals: 6 }}
  - {{ id: C, label: Circumference 2πr, min: 0, decimals: 6 }}
  - {{ id: A, label: Area πr², min: 0, decimals: 6 }}
equations:
  - Dd = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
  - h = ((x1^2 + y1^2) * (y2 - y3) + (x2^2 + y2^2) * (y3 - y1) + (x3^2 + y3^2) * (y1 - y2)) / Dd
  - k = ((x1^2 + y1^2) * (x3 - x2) + (x2^2 + y2^2) * (x1 - x3) + (x3^2 + y3^2) * (x2 - x1)) / Dd
  - r = sqrt((x1 - h)^2 + (y1 - k)^2)
  - Dg = -2 * h
  - Eg = -2 * k
  - Fg = h^2 + k^2 - r^2
  - C = 2 * pi * r
  - A = pi * r^2
faq:
  - q: How do you find the equation of a circle through three points?
    a: The centre is equally far from all three points, so it lies where the perpendicular bisectors of two chords meet. Solving those two linear equations gives h = [s₁(y₂ − y₃) + s₂(y₃ − y₁) + s₃(y₁ − y₂)] ÷ d and k = [s₁(x₃ − x₂) + s₂(x₁ − x₃) + s₃(x₂ − x₁)] ÷ d, where sᵢ = xᵢ² + yᵢ² and d = 2[x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)]. The radius is the distance from the centre to any of the points.
  - q: What if the three points are on a straight line?
    a: Then d = 0 and no circle passes through them — the perpendicular bisectors are parallel. The calculator shows an infinite or undefined centre and radius.
  - q: What is the general form of the equation of a circle?
    a: x² + y² + Dx + Ey + F = 0, with D = −2h, E = −2k and F = h² + k² − r². You can also find D, E and F directly by substituting the three points and solving the three linear equations.
  - q: How do I find the radius of an arc from three measured points?
    a: Measure the coordinates of three points on the arc — for example both ends and the middle — and enter them. For a chord of length c and height (sagitta) s the radius is also r = c² ÷ (8s) + s ÷ 2.
related: [math/circle, math/distance-midpoint, math/arc-length, math/system-of-3-equations]
''', f'''
## How to use the circle through 3 points calculator

Enter the coordinates of **three points** that are not on a straight line. The calculator gives the **centre (h, k)**, the **radius r**, the coefficients of the **general equation** x² + y² + Dx + Ey + F = 0, and the **circumference** and **area** of the circle. The determinant term d is zero when the points are collinear — then no circle exists.

## Circle through three points formulas

<p class="formula">d = 2[x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)] &nbsp;·&nbsp; sᵢ = xᵢ² + yᵢ²</p>

<p class="formula">h = [s₁(y₂ − y₃) + s₂(y₃ − y₁) + s₃(y₁ − y₂)] ÷ d &nbsp;·&nbsp; k = [s₁(x₃ − x₂) + s₂(x₁ − x₃) + s₃(x₂ − x₁)] ÷ d</p>

<p class="formula">r = √[(x₁ − h)² + (y₁ − k)²] &nbsp;·&nbsp; (x − h)² + (y − k)² = r²</p>

## Worked example

Points ({cx1:g}, {cy1:g}), ({cx2:g}, {cy2:g}) and ({cx3:g}, {cy3:g}):

- s₁ = {cx1**2+cy1**2:g}, s₂ = {cx2**2+cy2**2:g}, s₃ = {cx3**2+cy3**2:g}
- d = 2[1 × (4 − 3) + 2 × (3 − 1) + 5 × (1 − 4)] = **{sgn(cD)}**
- h = [2 × 1 + 20 × 2 + 34 × (−3)] ÷ ({sgn(cD)}) = **{ch:g}**, k = [2 × 3 + 20 × (−4) + 34 × 1] ÷ ({sgn(cD)}) = **{ck:g}**
- r = √[(1 − 3)² + (1 − 2)²] = √5 = **{cr:.6f}**
- Equation: **(x − {ch:g})² + (y − {ck:g})² = 5**, or x² + y² {'−' if cDg < 0 else '+'} {abs(cDg):g}x {'−' if cEg < 0 else '+'} {abs(cEg):g}y {'−' if cFg < 0 else '+'} {abs(cFg):.6g} = 0
- Circumference = **{cC:.6f}**, area = **{cA:.6f}**

## Example point sets

| Points | Centre (h, k) | Radius |
|---|---|---|
{cx_rows}
For a right triangle the centre is the midpoint of the hypotenuse — the first row is the 3-4-5 triangle with radius 2.5.

## Practical notes

- **Measuring an arc or a pipe bend:** pick the three points as far apart as possible along the arc; points close together make the radius very sensitive to measurement errors.
- The centre is the **circumcentre** of the triangle formed by the points — inside the triangle if it is acute, on the hypotenuse if it is right-angled and outside if it is obtuse.
- To check a result, the distance from the centre to each point should equal r — use the [distance and midpoint calculator](/math/distance-midpoint/).
- For more than three noisy points, a least-squares circle fit gives a better estimate than any single set of three.
''')

print(len(DESC), 'pages:', ' '.join(DESC))
