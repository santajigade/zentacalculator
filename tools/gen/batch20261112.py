"""Batch 2026-11-12 — 6 calculators: engineering (air changes per hour, insulated pipe heat loss,
roller chain length & sprocket), chemistry (enthalpy of reaction from heats of formation, gas density),
math (fraction calculator). All reference tables are computed here; defaults match the worked examples."""
import sys, math, os, re
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro
D = '2026-11-12'
pi = math.pi
R = 8.314462618
DESC = []
def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    assert 'featured' not in fm
    DESC.append(slug)
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)  # typographic minus for negative numbers in the text
    page(cat, slug, fm, body)

# ======================================================================= ENGINEERING

# ---------------------------------------------------------------- Air changes per hour
aL, aW, aH, aQ, aT = 5.0, 4.0, 2.7, 300.0, 6.0
aV = aL * aW * aH
aACH = aQ / aV
aQr = aT * aV
atc = 60 / aACH
a99 = math.log(100) / aACH * 60
a999 = math.log(1000) / aACH * 60
M3H_CFM = 1 / (0.028316846592 * 60)  # 1 cfm = 0.028316846592 m³/min = 1.699 m³/h
aq_rows = ''
for vol in (25, 50, 100, 250, 500, 1000):
    cells = [f"{vol*x:,.0f} m³/h ({vol*x*M3H_CFM:,.0f} cfm)" for x in (2, 4, 6, 12)]
    aq_rows += f"| {vol:,} m³ ({vol/0.028316846592:,.0f} ft³) | " + ' | '.join(cells) + " |\n"
ar_rows = ''
for x in (1, 2, 4, 6, 8, 10, 12, 15, 20, 25):
    ar_rows += f"| {x} | {60/x:.1f} min | {math.log(10)/x*60:.0f} min | {math.log(100)/x*60:.0f} min | {math.log(1000)/x*60:.0f} min |\n"
P('engineering', 'air-changes-per-hour', f'''
title: Air Changes per Hour Calculator (ACH, CFM & m³/h)
description: Calculate air changes per hour (ACH) from room size and airflow, the CFM or m³/h needed for a target ACH, and the time to clear 99% of airborne contaminants.
category: engineering
{intro("Air changes per hour (ACH) tells you how many times the air in a room is replaced by ventilation or air cleaning every hour, and it is the usual way ventilation rates for offices, labs, workshops, clean rooms and hospital rooms are specified. This air changes per hour calculator gives the ACH from the room dimensions and the airflow, the airflow in m³/h or CFM needed to reach a target ACH, and how long the ventilation takes to remove 99% and 99.9% of an airborne contaminant — a quick check on the fan or [HVAC system](ib:what-is-an-hvac-system) serving the room.")}
keywords: [air changes per hour calculator, ach calculator, cfm to ach, ach to cfm, room air change rate, ventilation rate calculator, air changes per hour formula, cfm calculator for room]
updated: {D}
variables:
  - {{ id: Lr, label: Room length, family: length, unit: m, imperialUnit: ft, default: {aL:g}, min: 0 }}
  - {{ id: Wr, label: Room width, family: length, unit: m, imperialUnit: ft, default: {aW:g}, min: 0 }}
  - {{ id: Hr, label: Ceiling height, family: length, unit: m, imperialUnit: ft, default: {aH:g}, min: 0 }}
  - {{ id: Q, label: Supply (or exhaust) airflow, family: flow, unit: m3h, imperialUnit: cfm, default: {aQ:g}, min: 0 }}
  - {{ id: ACHt, label: Target air changes per hour, suffix: per hour, default: {aT:g}, min: 0 }}
  - {{ id: V, label: Room volume, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: ACH, label: Air changes per hour with this airflow, suffix: per hour, min: 0, decimals: 2 }}
  - {{ id: Qr, label: Airflow needed for the target ACH, family: flow, unit: m3h, imperialUnit: cfm, min: 0 }}
  - {{ id: tc, label: Time for one air change, family: seconds, unit: min, min: 0 }}
  - {{ id: t99, label: Time to remove 99% of an airborne contaminant, family: seconds, unit: min, min: 0 }}
  - {{ id: t999, label: Time to remove 99.9%, family: seconds, unit: min, min: 0 }}
equations:
  - V = Lr * Wr * Hr
  - ACH = Q * 3600 / V
  - Qr = ACHt * V / 3600
  - tc = V / Q
  - t99 = ln(100) * V / Q
  - t999 = ln(1000) * V / Q
faq:
  - q: How do you calculate air changes per hour?
    a: ACH = airflow per hour ÷ room volume. In metric units ACH = Q (m³/h) ÷ V (m³); in US units ACH = CFM × 60 ÷ room volume in cubic feet. A 54 m³ room supplied with 300 m³/h of air has 300 ÷ 54 = 5.6 air changes per hour.
  - q: How do you convert ACH to CFM?
    a: CFM = ACH × room volume (ft³) ÷ 60. For a 12 × 15 ft room with an 8 ft ceiling (1,440 ft³) and a target of 6 ACH, the airflow needed is 6 × 1,440 ÷ 60 = 144 CFM.
  - q: How long does it take to remove airborne contaminants?
    a: With good mixing the concentration falls exponentially, C = C₀ e^(−ACH × t), so removing 99% takes ln(100) ÷ ACH = 4.6 ÷ ACH hours and 99.9% takes 6.9 ÷ ACH hours. At 12 ACH that is about 23 and 35 minutes — the same figures used in US CDC guidance for healthcare rooms.
  - q: How many air changes per hour does a room need?
    a: It depends on the use and the governing code. Homes and offices are normally designed on outdoor air per person or per floor area rather than ACH; airborne infection isolation rooms in US hospitals need at least 12 ACH under ASHRAE 170, and laboratories, kitchens and clean rooms are often much higher. Always check the standard that applies to your building.
related: [engineering/fan-affinity-laws, conversion/flow-rate-converter, engineering/chiller-tonnage, math/box-volume]
''', f'''
## How to use the air changes per hour calculator

Enter the **length, width and ceiling height** of the room and the **airflow** supplied (or extracted) by the fan, air handler or air purifier. The calculator gives the room volume, the **air changes per hour**, the time for one air change and the time needed to remove 99% and 99.9% of an airborne contaminant. Enter a **target ACH** to see the airflow you need in m³/h or CFM. Switch to imperial units to work in feet and CFM.

## Air changes per hour formula

<p class="formula">ACH = Q ÷ V &nbsp;(Q in m³/h, V in m³) &nbsp;·&nbsp; ACH = CFM × 60 ÷ V (V in ft³)</p>

<p class="formula">Q<sub>required</sub> = ACH × V &nbsp;·&nbsp; time to remove a fraction f = ln[1 ÷ (1 − f)] ÷ ACH</p>

The removal time assumes the supply air is clean and mixes well with the room air, with no new contaminant released during the period.

## Worked example

A {aL:g} m × {aW:g} m office with a {aH:g} m ceiling is supplied with {aQ:g} m³/h of air:

- Room volume V = {aL:g} × {aW:g} × {aH:g} = **{aV:g} m³** ({aV/0.028316846592:,.0f} ft³)
- ACH = {aQ:g} ÷ {aV:g} = **{aACH:.2f} air changes per hour**
- One air change takes 60 ÷ {aACH:.2f} = **{atc:.1f} min**
- 99% removal takes ln(100) ÷ {aACH:.2f} × 60 = **{a99:.1f} min**, and 99.9% takes **{a999:.1f} min**
- For a target of {aT:g} ACH the airflow must be {aT:g} × {aV:g} = **{aQr:g} m³/h** ({aQr*M3H_CFM:.1f} CFM)

## Airflow needed for a given ACH

| Room volume | 2 ACH | 4 ACH | 6 ACH | 12 ACH |
|---|---|---|---|---|
{aq_rows}
## Time to remove airborne contaminants

Well-mixed room with clean supply air:

| ACH | One air change | 90% removed | 99% removed | 99.9% removed |
|---|---|---|---|---|
{ar_rows}
## Practical notes

- **Mixing matters:** short-circuiting between a supply diffuser and a nearby extract grille can leave parts of the room poorly ventilated, so the effective ACH is lower than the calculated value.
- **Air purifiers:** use the clean air delivery rate (CADR) as the airflow — a purifier with a CADR of 250 m³/h in a 50 m³ room adds 5 ACH of clean air.
- **Recirculated air** only counts towards contaminant removal if it passes through an effective filter; outdoor-air requirements in ventilation codes are usually stated separately.
- To change a fan's airflow by changing its speed, use the [fan affinity laws calculator](/engineering/fan-affinity-laws/); to convert between m³/h, L/s and CFM, use the [flow rate converter](/conversion/flow-rate-converter/).
''')

# ---------------------------------------------------------------- Insulated pipe heat loss
def pipeloss(D1, t, k, Tp, Ta, h, hb, L):
    D2 = D1 + 2 * t
    Ri = math.log(D2 / D1) / (2 * pi * k) if t > 0 else 0.0
    Rs = 1 / (h * pi * D2)
    qL = (Tp - Ta) / (Ri + Rs)
    Ts = Ta + qL * Rs
    qb = hb * pi * D1 * (Tp - Ta)
    return D2, Ri, Rs, qL, qL * L, Ts, qb, 1 - qL / qb, qL * L * 8760 / 1000
pD1, pt, pk, pTp, pTa, ph, phb, pL = 0.1143, 0.05, 0.045, 150.0, 20.0, 10.0, 15.0, 100.0
pD2, pRi, pRs, pqL, pQ, pTs, pqb, psv, pEy = pipeloss(pD1, pt, pk, pTp, pTa, ph, phb, pL)
PIPES = (('DN25 (1")', 0.0334), ('DN50 (2")', 0.0603), ('DN80 (3")', 0.0889), ('DN100 (4")', 0.1143), ('DN150 (6")', 0.1683), ('DN200 (8")', 0.2191))
pt_rows = ''
for nm, od in PIPES:
    cells = [f"{pipeloss(od, 0.0001, pk, pTp, pTa, ph, phb, 1)[6]:,.0f}"]
    for th in (25, 50, 75, 100):
        r = pipeloss(od, th / 1000, pk, pTp, pTa, ph, phb, 1)
        cells.append(f"{r[3]:,.1f}")
    pt_rows += f"| {nm}, {od*1000:g} mm OD | " + ' | '.join(cells) + " |\n"
ps_rows = ''
for Tp in (60, 100, 150, 200, 250):
    r = [pipeloss(pD1, th / 1000, pk, Tp, pTa, ph, phb, 1) for th in (25, 50, 100)]
    ps_rows += f"| {Tp} °C | " + ' | '.join(f"{x[3]:.1f} W/m, {x[5]:.1f} °C" for x in r) + " |\n"
P('engineering', 'pipe-heat-loss', f'''
title: Pipe Heat Loss Calculator (Insulated & Bare Pipe)
description: Calculate heat loss per metre from an insulated or bare pipe, the insulation surface temperature, the total loss for a pipe run and the yearly energy wasted.
category: engineering
{intro("Hot pipes for steam, hot water, thermal oil and process fluids lose heat continuously to the surrounding air, and insulation is the cheapest way to cut that loss. This pipe heat loss calculator works out the loss per metre through cylindrical insulation and the outer air film, the insulation surface temperature, the total loss for the pipe run, the yearly energy and how much the insulation saves compared with a bare pipe — the same calculation explained in this guide to [calculating heat loss in piping](ib:calculate-heat-loss-in-piping).")}
keywords: [pipe heat loss calculator, insulated pipe heat loss, heat loss from pipe per meter, pipe insulation heat loss calculation, bare pipe heat loss, steam pipe heat loss, insulation surface temperature calculator]
updated: {D}
variables:
  - {{ id: D1, label: Pipe outside diameter, family: length, unit: mm, imperialUnit: in, default: {pD1*1000:g}, min: 0 }}
  - {{ id: t, label: Insulation thickness, family: length, unit: mm, imperialUnit: in, default: {pt*1000:g}, min: 0.000001 }}
  - {{ id: k, label: Thermal conductivity of the insulation, suffix: W/m·K, default: {pk:g}, min: 0, help: 'At the mean insulation temperature. Mineral wool about 0.04–0.05, calcium silicate 0.06, PIR foam 0.025.' }}
  - {{ id: Tp, label: Pipe (fluid) temperature, family: temperature, unit: C, imperialUnit: F, default: {pTp:g} }}
  - {{ id: Ta, label: Ambient air temperature, family: temperature, unit: C, imperialUnit: F, default: {pTa:g} }}
  - {{ id: h, label: Outer surface heat transfer coefficient (insulated), suffix: W/m²·K, default: {ph:g}, min: 0, help: 'Convection plus radiation. About 8–10 indoors in still air with a metal jacket or painted surface, 20–30 outdoors in wind.' }}
  - {{ id: hb, label: Surface coefficient of the bare pipe, suffix: W/m²·K, default: {phb:g}, min: 0, help: 'Bare steel radiates strongly: about 12–20 indoors at 100–250 °C.' }}
  - {{ id: L, label: Length of the pipe run, family: length, unit: m, imperialUnit: ft, default: {pL:g}, min: 0 }}
  - {{ id: D2, label: Outside diameter over the insulation, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: Ri, label: Thermal resistance of the insulation per metre, suffix: m·K/W, min: 0, decimals: 4 }}
  - {{ id: Rs, label: Thermal resistance of the outer air film per metre, suffix: m·K/W, min: 0, decimals: 4 }}
  - {{ id: qL, label: Heat loss per metre of insulated pipe, suffix: W/m, min: 0, decimals: 2 }}
  - {{ id: Q, label: Total heat loss of the run, family: power, unit: kW, imperialUnit: BTUh, min: 0 }}
  - {{ id: Ts, label: Insulation surface temperature, family: temperature, unit: C, imperialUnit: F }}
  - {{ id: qb, label: Heat loss per metre of bare pipe, suffix: W/m, min: 0, decimals: 1 }}
  - {{ id: sv, label: Heat loss saved by the insulation, family: percent, unit: '%' }}
  - {{ id: Ey, label: Energy lost per year (8,760 h), family: energy, unit: kWh, min: 0 }}
equations:
  - D2 = D1 + 2 * t
  - Ri = ln(D2 / D1) / (2 * pi * k)
  - Rs = 1 / (h * pi * D2)
  - qL = (Tp - Ta) / (Ri + Rs)
  - Q = qL * L
  - Ts = Ta + qL * Rs
  - qb = hb * pi * D1 * (Tp - Ta)
  - sv = 1 - qL / qb
  - Ey = Q * 8760 * 3600
faq:
  - q: How do you calculate heat loss from an insulated pipe?
    a: Add the thermal resistance of the insulation, ln(D₂ ÷ D₁) ÷ (2πk), to the resistance of the outer air film, 1 ÷ (h π D₂), both per metre of pipe. The heat loss per metre is the temperature difference divided by the total, q = (T_pipe − T_air) ÷ (R_ins + R_surface). The pipe wall and the inside film add very little resistance and are usually ignored.
  - q: How much heat does a bare pipe lose?
    a: A bare steel pipe loses q = h π D (T_pipe − T_air) per metre, with h around 12–20 W/m²·K indoors once radiation is included. A bare 4-inch (DN100) pipe at 150 °C in a 20 °C room loses roughly 450–750 W per metre — ten or more times as much as the same pipe with 50 mm of mineral wool.
  - q: Why does doubling the insulation thickness not halve the heat loss?
    a: The insulation resistance grows with the logarithm of the diameter ratio, and the outer surface gets larger as the insulation gets thicker. Each extra 25 mm therefore saves less than the one before — which is why economic insulation thickness is found by balancing insulation cost against the value of the heat saved.
  - q: What surface temperature should pipe insulation have?
    a: Personnel protection limits are commonly set around 50–60 °C for surfaces people can touch, depending on the standard and the jacket material. Use the surface temperature from this calculator to check the insulation thickness, remembering that a shiny aluminium jacket runs hotter than a painted one because it radiates less.
related: [physics/heat-conduction, engineering/convection-heat-transfer, physics/stefan-boltzmann-law, engineering/heat-duty]
''', f'''
## How to use the pipe heat loss calculator

Enter the **pipe outside diameter**, the **insulation thickness** and its **thermal conductivity**, the **pipe and ambient temperatures** and the **outer surface coefficient**. The calculator gives the heat loss per metre, the total for the **pipe run length**, the **insulation surface temperature**, the yearly energy lost if the pipe runs continuously, and — using the **bare pipe coefficient** — how much the insulation saves compared with leaving the pipe bare. To find the insulation thickness for a target loss per metre or surface temperature, enter that value and press × on the insulation thickness.

## Pipe heat loss formula

<p class="formula">R<sub>ins</sub> = ln(D<sub>2</sub> ÷ D<sub>1</sub>) ÷ (2π k) &nbsp;·&nbsp; R<sub>s</sub> = 1 ÷ (h π D<sub>2</sub>)</p>

<p class="formula">q = (T<sub>pipe</sub> − T<sub>air</sub>) ÷ (R<sub>ins</sub> + R<sub>s</sub>) &nbsp;·&nbsp; T<sub>surface</sub> = T<sub>air</sub> + q R<sub>s</sub> &nbsp;·&nbsp; q<sub>bare</sub> = h<sub>b</sub> π D<sub>1</sub> (T<sub>pipe</sub> − T<sub>air</sub>)</p>

D<sub>1</sub> is the pipe outside diameter, D<sub>2</sub> = D<sub>1</sub> + 2 × thickness, k the insulation conductivity and h the combined convection and radiation coefficient at the outer surface. The steel wall and the inside film are neglected — they add well under 1% to the resistance of an insulated pipe.

## Worked example

A DN100 steam line ({pD1*1000:g} mm OD) at {pTp:g} °C, insulated with {pt*1000:g} mm of mineral wool (k = {pk:g} W/m·K), runs {pL:g} m through a {pTa:g} °C plant room (h = {ph:g} W/m²·K):

- Outside diameter over the insulation D<sub>2</sub> = {pD1*1000:g} + 2 × {pt*1000:g} = **{pD2*1000:g} mm**
- R<sub>ins</sub> = ln({pD2:.4f} ÷ {pD1:.4f}) ÷ (2π × {pk:g}) = **{pRi:.4f} m·K/W**
- R<sub>s</sub> = 1 ÷ ({ph:g} × π × {pD2:.4f}) = **{pRs:.4f} m·K/W**
- Heat loss q = ({pTp:g} − {pTa:g}) ÷ ({pRi:.4f} + {pRs:.4f}) = **{pqL:.2f} W/m**, so the {pL:g} m run loses **{pQ/1000:.2f} kW**
- Surface temperature = {pTa:g} + {pqL:.2f} × {pRs:.4f} = **{pTs:.2f} °C**
- Bare, the same pipe would lose {phb:g} × π × {pD1:.4f} × {pTp-pTa:g} = **{pqb:.1f} W/m**, so the insulation saves **{psv*100:.1f}%**
- Running all year, the insulated run loses {pQ/1000:.2f} × 8,760 = **{pEy:,.0f} kWh**

## Heat loss per metre by pipe size and insulation thickness

Pipe at {pTp:g} °C, air at {pTa:g} °C, k = {pk:g} W/m·K, h = {ph:g} W/m²·K; bare pipe with h = {phb:g} W/m²·K. Values in W/m.

| Pipe | Bare | 25 mm | 50 mm | 75 mm | 100 mm |
|---|---|---|---|---|---|
{pt_rows}
## Heat loss and surface temperature by pipe temperature

DN100 pipe, same conditions; each cell gives the loss per metre and the surface temperature. (In practice k rises with temperature, so check the manufacturer's k at the mean insulation temperature for hot lines.)

| Pipe temperature | 25 mm insulation | 50 mm insulation | 100 mm insulation |
|---|---|---|---|
{ps_rows}
## Typical insulation conductivity

| Insulation | k at about 50–100 °C mean (W/m·K) | Usual service range |
|---|---|---|
| Mineral (rock) wool | 0.037–0.050 | to about 650 °C |
| Glass wool | 0.035–0.045 | to about 250–450 °C |
| Calcium silicate | 0.055–0.065 | to about 650 °C |
| Cellular glass | 0.042–0.050 | cryogenic to about 430 °C |
| Polyurethane / PIR foam | 0.022–0.028 | about −180 to 120 °C |
| Flexible elastomeric foam | 0.033–0.040 | about −50 to 105 °C |

## Practical notes

- **Wet insulation** conducts heat many times better than dry insulation — damaged cladding that lets rain in can make the real loss far higher than calculated.
- **Valves, flanges and supports** left bare can add the equivalent of several metres of bare pipe each; removable insulation jackets pay back quickly on steam systems.
- **Small tubes and cables:** below the critical radius r = k ÷ h (a few millimetres for typical values) adding insulation can increase the heat loss — this never applies to normal process pipes.
- The heat lost by a steam line turns into condensate; divide the loss in kW by the latent heat (about 2,100 kJ/kg at low pressure) to estimate the condensate load for steam traps. For [heat tracing](ib:heat-tracing-in-piping-systems), the tracer must supply at least this loss at the minimum ambient temperature.
- For flat walls and layers, use the [heat conduction calculator](/physics/heat-conduction/); for the surface film alone, use the [convection heat transfer calculator](/engineering/convection-heat-transfer/).
''')

# ---------------------------------------------------------------- Roller chain length & sprocket
def chain(p, N1, N2, C, n1):
    S = (N1 + N2) / 2; K = ((N2 - N1) / (2 * pi)) ** 2
    Lp = 2 * C / p + S + K * p / C
    Lr = 2 * math.ceil(Lp / 2 - 1e-9)
    x = ((Lr - S) + math.sqrt((Lr - S) ** 2 - 8 * K)) / 4
    return dict(Lp=Lp, Lr=Lr, Lm=Lr * p, Ca=x * p, i=N2 / N1, n2=n1 * N1 / N2, v=N1 * p * n1 / 60,
                Dp1=p / math.sin(pi / N1), Dp2=p / math.sin(pi / N2), S=S, K=K)
cp_, cN1, cN2, cC, cn1 = 0.0127, 17, 34, 0.5, 500.0
CH = chain(cp_, cN1, cN2, cC, cn1)
CHAINS = (('ANSI 25', '04C', 6.35), ('ANSI 35', '06C', 9.525), ('ANSI 40', '08A', 12.7), ('ANSI 50', '10A', 15.875),
          ('ANSI 60', '12A', 19.05), ('ANSI 80', '16A', 25.4), ('ANSI 100', '20A', 31.75), ('ANSI 120', '24A', 38.1))
cpd_rows = ''
for nm, iso, pmm in CHAINS:
    cpd_rows += f"| {nm} / {iso} | {pmm:g} mm ({pmm/25.4:g} in) | " + ' | '.join(f"{pmm/math.sin(pi/N):.1f}" for N in (9, 12, 15, 17, 19, 21, 25)) + " |\n"
cl_rows = ''
for C_p in (30, 40, 50, 60, 80):
    r = chain(1, cN1, cN2, C_p, 1)
    cl_rows += f"| {C_p} pitches | {r['Lp']:.2f} | {r['Lr']} | {r['Ca']:.2f} pitches |\n"
P('engineering', 'chain-length', f'''
title: Chain Length Calculator (Roller Chain & Sprocket)
description: Calculate roller chain length in links from sprocket teeth and centre distance, the exact centre distance, speed ratio, chain speed and pitch diameters.
category: engineering
{intro("A roller chain drive is defined by the chain pitch, the number of teeth on each sprocket and the distance between the shaft centres. This chain length calculator works out the chain length in pitches, rounds it up to a whole even number of links, gives the exact centre distance that number of links needs, and also calculates the speed ratio, the driven shaft speed, the chain speed and the pitch diameter of both sprockets.")}
keywords: [chain length calculator, roller chain length calculator, sprocket calculator, chain links calculator, sprocket pitch diameter calculator, chain drive calculator, chain centre distance calculator, chain speed calculator]
updated: {D}
variables:
  - {{ id: p, label: Chain pitch, family: length, unit: mm, imperialUnit: in, default: {cp_*1000:g}, min: 0, help: 'ANSI 25 = 6.35 mm, 35 = 9.525 mm, 40 = 12.7 mm, 50 = 15.875 mm, 60 = 19.05 mm, 80 = 25.4 mm.' }}
  - {{ id: N1, label: Teeth on the driving (small) sprocket, default: {cN1}, min: 1, decimals: 0 }}
  - {{ id: N2, label: Teeth on the driven (large) sprocket, default: {cN2}, min: 1, decimals: 0 }}
  - {{ id: C, label: Centre distance between the shafts, family: length, unit: mm, imperialUnit: in, default: {cC*1000:g}, min: 0 }}
  - {{ id: n1, label: Speed of the driving sprocket, suffix: rpm, default: {cn1:g}, min: 0 }}
  - {{ id: Lp, label: Chain length for this centre distance, suffix: pitches, min: 0, decimals: 2 }}
  - {{ id: Lr, label: Chain length rounded up to an even number of links, suffix: links, min: 0, decimals: 0 }}
  - {{ id: Lm, label: Length of the chain, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: Ca, label: Exact centre distance for the rounded chain, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: i, label: Speed ratio (N2 ÷ N1), min: 0, decimals: 3 }}
  - {{ id: n2, label: Speed of the driven sprocket, suffix: rpm, min: 0, decimals: 1 }}
  - {{ id: v, label: Chain speed, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: Dp1, label: Pitch diameter of the driving sprocket, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: Dp2, label: Pitch diameter of the driven sprocket, family: length, unit: mm, imperialUnit: in, min: 0 }}
equations:
  - Lp = 2 * C / p + (N1 + N2) / 2 + ((N2 - N1) / (2 * pi))^2 * p / C
  - Lr = 2 * ceil(Lp / 2)
  - Lm = Lr * p
  - Ca = p / 4 * (Lr - (N1 + N2) / 2 + sqrt((Lr - (N1 + N2) / 2)^2 - 8 * ((N2 - N1) / (2 * pi))^2))
  - i = N2 / N1
  - n2 = n1 * N1 / N2
  - v = N1 * p * n1 / 60
  - Dp1 = p / sin(pi / N1)
  - Dp2 = p / sin(pi / N2)
faq:
  - q: How do you calculate roller chain length?
    a: In pitches, L = 2C ÷ p + (N₁ + N₂) ÷ 2 + [(N₂ − N₁) ÷ 2π]² × p ÷ C, where C is the centre distance, p the pitch and N₁ and N₂ the tooth counts. Round the result up to the next even whole number of links and multiply by the pitch for the length. For 17 and 34 teeth on ANSI 40 chain at 500 mm centres, L = 104.43 pitches, so use 106 links.
  - q: Why should a chain have an even number of links?
    a: A chain with an odd number of pitches needs an offset (cranked) link to join it, which is weaker than standard links — often derated by about 20–35%. Choosing an even number of links and adjusting the centre distance or using a tensioner avoids it.
  - q: How do you find the pitch diameter of a sprocket?
    a: Pitch diameter = p ÷ sin(180° ÷ N). A 17-tooth sprocket for 12.7 mm (ANSI 40) chain has a pitch diameter of 12.7 ÷ sin(10.59°) = 69.1 mm. The outside diameter is a little larger and depends on the tooth form.
  - q: What centre distance is best for a chain drive?
    a: Manufacturers usually recommend 30–50 pitches, with a maximum of about 80 pitches without a guide or idler. The chain should wrap at least 120° around the small sprocket, which is easier with ratios below about 7:1.
related: [engineering/gear-ratio, engineering/pulley-speed, engineering/torque-power-speed, sports/cycling-gear-speed]
''', f'''
## How to use the chain length calculator

Enter the **chain pitch**, the **number of teeth** on the driving and driven sprockets and the planned **centre distance** between the shafts. The calculator gives the chain length in pitches, the length **rounded up to an even number of links**, the chain length in mm or inches and the **exact centre distance** that whole chain needs (so you know how far to set the shafts or the tensioner). Enter the **driving speed** to get the driven speed and the chain speed; the sprocket **pitch diameters** are given as well.

## Chain length formula

<p class="formula">L<sub>p</sub> = 2C ÷ p + (N<sub>1</sub> + N<sub>2</sub>) ÷ 2 + [(N<sub>2</sub> − N<sub>1</sub>) ÷ 2π]² × p ÷ C</p>

<p class="formula">C = (p ÷ 4) × [L − (N<sub>1</sub> + N<sub>2</sub>) ÷ 2 + √( (L − (N<sub>1</sub> + N<sub>2</sub>) ÷ 2)² − 8 [(N<sub>2</sub> − N<sub>1</sub>) ÷ 2π]² )]</p>

<p class="formula">v = N<sub>1</sub> p n<sub>1</sub> ÷ 60 &nbsp;·&nbsp; n<sub>2</sub> = n<sub>1</sub> N<sub>1</sub> ÷ N<sub>2</sub> &nbsp;·&nbsp; D<sub>p</sub> = p ÷ sin(180° ÷ N)</p>

The second formula is the first one solved for the centre distance, used once the chain length has been rounded to whole links.

## Worked example

An ANSI 40 (12.7 mm pitch) chain drive with a {cN1}-tooth driving sprocket at {cn1:g} rpm and a {cN2}-tooth driven sprocket, shafts {cC*1000:g} mm apart:

- Chain length = 2 × {cC*1000:g} ÷ {cp_*1000:g} + ({cN1} + {cN2}) ÷ 2 + [({cN2} − {cN1}) ÷ 2π]² × {cp_*1000:g} ÷ {cC*1000:g} = {2*cC/cp_:.3f} + {CH['S']:g} + {CH['K']*cp_/cC:.3f} = **{CH['Lp']:.2f} pitches**
- Rounded up to an even number: **{CH['Lr']} links**, a chain **{CH['Lm']*1000:,.1f} mm** long
- With {CH['Lr']} links the centre distance becomes **{CH['Ca']*1000:.1f} mm** — set the shafts there or take up the slack with a tensioner
- Speed ratio = {cN2} ÷ {cN1} = **{CH['i']:g}**, so the driven sprocket turns at **{CH['n2']:g} rpm**
- Chain speed = {cN1} × {cp_:g} × {cn1:g} ÷ 60 = **{CH['v']:.3f} m/s**
- Pitch diameters: **{CH['Dp1']*1000:.2f} mm** and **{CH['Dp2']*1000:.2f} mm**

## Sprocket pitch diameter (mm)

| Chain | Pitch | 9 T | 12 T | 15 T | 17 T | 19 T | 21 T | 25 T |
|---|---|---|---|---|---|---|---|---|
{cpd_rows}
## Chain length against centre distance

{cN1}-tooth and {cN2}-tooth sprockets, centre distance in pitches (multiply by the pitch for mm):

| Centre distance | Exact length (pitches) | Links to use | Centre distance for those links |
|---|---|---|---|
{cl_rows}
## Practical notes

- **Sprocket size:** small sprockets cause chordal speed variation and faster wear — 17 teeth or more is usual for moderate and high speeds, and an odd tooth count on the small sprocket with an even number of links spreads the wear.
- **Slack:** allow about 2% of the centre distance as sag on the slack side of a horizontal drive, and provide adjustment of at least two pitches for chain wear.
- **Lubrication:** chain speed and pitch decide whether manual, drip, bath or forced lubrication is needed — check the manufacturer's power rating tables, which also give the kW capacity of each chain size.
- **Wear:** a roller chain is normally replaced when it has stretched by about 1.5–3% of its length; measure over several pitches with the chain under tension.
- To check shaft speeds and torque for a drive, use the [gear ratio calculator](/engineering/gear-ratio/) or the [torque, power and speed calculator](/engineering/torque-power-speed/).
''')

# ======================================================================= CHEMISTRY

# ---------------------------------------------------------------- Enthalpy of reaction
HF = {  # standard enthalpy of formation at 298.15 K, kJ/mol (NIST/CRC values, rounded to 0.1)
    'H2O(l)': -285.8, 'H2O(g)': -241.8, 'CO2(g)': -393.5, 'CO(g)': -110.5, 'CH4(g)': -74.8, 'C3H8(g)': -103.8,
    'C2H5OH(l)': -277.6, 'C6H12O6(s)': -1273.3, 'NH3(g)': -45.9, 'NO(g)': 91.3, 'NO2(g)': 33.2, 'SO2(g)': -296.8,
    'HCl(g)': -92.3, 'NaCl(s)': -411.2, 'CaCO3(s)': -1206.9, 'CaO(s)': -634.9, 'Fe2O3(s)': -824.2, 'Al2O3(s)': -1675.7,
    'O2(g)': 0.0, 'N2(g)': 0.0, 'H2(g)': 0.0, 'Al(s)': 0.0, 'Fe(s)': 0.0}
def dH(react, prod):
    return sum(n * HF[s] for n, s in prod) - sum(n * HF[s] for n, s in react)
RX = (('Methane combustion', 'CH₄ + 2 O₂ → CO₂ + 2 H₂O(l)', [(1, 'CH4(g)'), (2, 'O2(g)')], [(1, 'CO2(g)'), (2, 'H2O(l)')]),
      ('Propane combustion', 'C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O(l)', [(1, 'C3H8(g)'), (5, 'O2(g)')], [(3, 'CO2(g)'), (4, 'H2O(l)')]),
      ('Ethanol combustion', 'C₂H₅OH + 3 O₂ → 2 CO₂ + 3 H₂O(l)', [(1, 'C2H5OH(l)'), (3, 'O2(g)')], [(2, 'CO2(g)'), (3, 'H2O(l)')]),
      ('Glucose oxidation', 'C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O(l)', [(1, 'C6H12O6(s)'), (6, 'O2(g)')], [(6, 'CO2(g)'), (6, 'H2O(l)')]),
      ('Hydrogen combustion', '2 H₂ + O₂ → 2 H₂O(l)', [(2, 'H2(g)'), (1, 'O2(g)')], [(2, 'H2O(l)')]),
      ('Carbon monoxide combustion', '2 CO + O₂ → 2 CO₂', [(2, 'CO(g)'), (1, 'O2(g)')], [(2, 'CO2(g)')]),
      ('Haber process', 'N₂ + 3 H₂ → 2 NH₃', [(1, 'N2(g)'), (3, 'H2(g)')], [(2, 'NH3(g)')]),
      ('Limestone calcination', 'CaCO₃ → CaO + CO₂', [(1, 'CaCO3(s)')], [(1, 'CaO(s)'), (1, 'CO2(g)')]),
      ('Thermite reaction', '2 Al + Fe₂O₃ → Al₂O₃ + 2 Fe', [(2, 'Al(s)'), (1, 'Fe2O3(s)')], [(1, 'Al2O3(s)'), (2, 'Fe(s)')]),
      ('Nitric oxide oxidation', '2 NO + O₂ → 2 NO₂', [(2, 'NO(g)'), (1, 'O2(g)')], [(2, 'NO2(g)')]))
rx_rows = ''
for nm, eq, r, p in RX:
    x = dH(r, p)
    rx_rows += f"| {nm} | {eq} | {x:+,.1f} kJ | {'exothermic' if x < 0 else 'endothermic'} |\n"
NAMES = {'H2O(l)': 'Water, liquid — H₂O(l)', 'H2O(g)': 'Water vapour — H₂O(g)', 'CO2(g)': 'Carbon dioxide — CO₂(g)', 'CO(g)': 'Carbon monoxide — CO(g)',
         'CH4(g)': 'Methane — CH₄(g)', 'C3H8(g)': 'Propane — C₃H₈(g)', 'C2H5OH(l)': 'Ethanol — C₂H₅OH(l)', 'C6H12O6(s)': 'Glucose — C₆H₁₂O₆(s)',
         'NH3(g)': 'Ammonia — NH₃(g)', 'NO(g)': 'Nitric oxide — NO(g)', 'NO2(g)': 'Nitrogen dioxide — NO₂(g)', 'SO2(g)': 'Sulfur dioxide — SO₂(g)',
         'HCl(g)': 'Hydrogen chloride — HCl(g)', 'NaCl(s)': 'Sodium chloride — NaCl(s)', 'CaCO3(s)': 'Calcium carbonate — CaCO₃(s)',
         'CaO(s)': 'Calcium oxide — CaO(s)', 'Fe2O3(s)': 'Iron(III) oxide — Fe₂O₃(s)', 'Al2O3(s)': 'Aluminium oxide — Al₂O₃(s)'}
hf_rows = ''.join(f"| {NAMES[k]} | {HF[k]:+.1f} |\n" for k in NAMES)
er1, eH1, er2, eH2 = 1, HF['CH4(g)'], 2, HF['O2(g)']
ep1, eP1, ep2, eP2 = 1, HF['CO2(g)'], 2, HF['H2O(l)']
eM, en = 16.04, 1.0
eHp = ep1 * eP1 + ep2 * eP2; eHr = er1 * eH1 + er2 * eH2; edH = eHp - eHr
eq_ = edH * en / er1; eqm = edH / (er1 * eM)
P('chemistry', 'enthalpy-of-reaction', f'''
title: Enthalpy of Reaction Calculator (ΔH from Heats of Formation)
description: Calculate the enthalpy change of a reaction (ΔH°rxn) from standard enthalpies of formation using Hess's law, with heat released per mole and per gram.
category: chemistry
{intro("The heat released or absorbed by a chemical reaction can be worked out without doing the experiment: by Hess's law, the enthalpy change equals the total enthalpy of formation of the products minus that of the reactants. This enthalpy of reaction calculator takes up to two reactants and two products with their coefficients and standard enthalpies of formation, and gives ΔH°rxn, whether the reaction is exothermic or endothermic, and the heat for a chosen amount of reactant per mole and per gram.")}
keywords: [enthalpy of reaction calculator, delta h calculator, heat of reaction calculator, enthalpy change calculator, hess's law calculator, standard enthalpy of formation calculator, enthalpy of combustion calculator]
updated: {D}
variables:
  - {{ id: nr1, label: Coefficient of reactant 1, default: {er1}, min: 0 }}
  - {{ id: Hr1, label: ΔHf° of reactant 1, suffix: kJ/mol, default: {eH1:g} }}
  - {{ id: nr2, label: Coefficient of reactant 2 (0 if none), default: {er2}, min: 0 }}
  - {{ id: Hr2, label: ΔHf° of reactant 2, suffix: kJ/mol, default: {eH2:g}, help: 'Elements in their standard state (O₂, H₂, N₂, C graphite, metals) are 0.' }}
  - {{ id: np1, label: Coefficient of product 1, default: {ep1}, min: 0 }}
  - {{ id: Hp1, label: ΔHf° of product 1, suffix: kJ/mol, default: {eP1:g} }}
  - {{ id: np2, label: Coefficient of product 2 (0 if none), default: {ep2}, min: 0 }}
  - {{ id: Hp2, label: ΔHf° of product 2, suffix: kJ/mol, default: {eP2:g} }}
  - {{ id: M1, label: Molar mass of reactant 1, suffix: g/mol, default: {eM:g}, min: 0 }}
  - {{ id: n, label: Amount of reactant 1 that reacts, suffix: mol, default: {en:g}, min: 0 }}
  - {{ id: Hp, label: Total enthalpy of formation of the products, suffix: kJ, decimals: 2 }}
  - {{ id: Hr, label: Total enthalpy of formation of the reactants, suffix: kJ, decimals: 2 }}
  - {{ id: dH, label: Enthalpy of reaction ΔH°rxn (as written), suffix: kJ, decimals: 2 }}
  - {{ id: q, label: Enthalpy change for this amount of reactant 1, suffix: kJ, decimals: 2 }}
  - {{ id: qm, label: Enthalpy change per gram of reactant 1, suffix: kJ/g, decimals: 3 }}
equations:
  - Hp = np1 * Hp1 + np2 * Hp2
  - Hr = nr1 * Hr1 + nr2 * Hr2
  - dH = Hp - Hr
  - q = dH * n / nr1
  - qm = dH / (nr1 * M1)
faq:
  - q: How do you calculate the enthalpy of reaction from enthalpies of formation?
    a: ΔH°rxn = Σ n ΔHf°(products) − Σ n ΔHf°(reactants), where n are the coefficients in the balanced equation. For CH₄ + 2 O₂ → CO₂ + 2 H₂O(l), ΔH = [−393.5 + 2 × (−285.8)] − [−74.8 + 0] = −890.3 kJ per mole of methane.
  - q: What does a negative enthalpy of reaction mean?
    a: A negative ΔH means the products hold less enthalpy than the reactants, so the reaction releases heat to the surroundings (exothermic) — all combustion reactions are like this. A positive ΔH means heat must be supplied (endothermic), as in decomposing limestone into lime and carbon dioxide.
  - q: What is Hess's law?
    a: The enthalpy change of a reaction is the same whatever route the reaction takes, because enthalpy is a state function. You can therefore add or subtract known reaction equations — and their ΔH values — to get the ΔH of a reaction that is hard to measure. Using enthalpies of formation is the most common application.
  - q: Why is the ΔHf° of oxygen zero?
    a: The standard enthalpy of formation of an element in its most stable form at 1 bar and 25 °C is defined as zero — this applies to O₂(g), H₂(g), N₂(g), graphite and solid metals. Ozone and diamond are not the most stable forms, so their values are not zero.
related: [chemistry/bomb-calorimeter, chemistry/gibbs-free-energy, chemistry/specific-heat, chemistry/limiting-reagent]
''', f'''
## How to use the enthalpy of reaction calculator

Write the **balanced equation** first. Enter the **coefficient** and the **standard enthalpy of formation** (ΔHf°, kJ/mol) of each reactant and product — the table below lists common values, and elements in their standard state are 0. For a reaction with only one reactant or product, set the second coefficient to 0. The calculator gives ΔH°rxn for the equation as written. Add the **molar mass** of reactant 1 and the **amount** that reacts to get the heat for that amount and per gram.

## Enthalpy of reaction formula (Hess's law)

<p class="formula">ΔH°<sub>rxn</sub> = Σ n ΔH<sub>f</sub>°(products) − Σ n ΔH<sub>f</sub>°(reactants)</p>

<p class="formula">q = ΔH°<sub>rxn</sub> × n<sub>reacting</sub> ÷ coefficient &nbsp;·&nbsp; q per gram = ΔH°<sub>rxn</sub> ÷ (coefficient × M)</p>

Watch the physical state: liquid water (−285.8 kJ/mol) gives the higher heating value of a fuel, water vapour (−241.8 kJ/mol) the lower heating value.

## Worked example: combustion of methane

CH₄(g) + 2 O₂(g) → CO₂(g) + 2 H₂O(l)

- Products: {ep1} × ({eP1:g}) + {ep2} × ({eP2:g}) = **{eHp:,.1f} kJ**
- Reactants: {er1} × ({eH1:g}) + {er2} × {eH2:g} = **{eHr:,.1f} kJ**
- ΔH°rxn = {eHp:,.1f} − ({eHr:,.1f}) = **{edH:,.1f} kJ** per mole of methane — exothermic
- Per gram of methane (M = {eM:g} g/mol): {edH:,.1f} ÷ {eM:g} = **{eqm:.3f} kJ/g**, i.e. about {abs(eqm):.1f} MJ/kg, the higher heating value of methane

## Enthalpy of reaction for common reactions

Calculated from the formation enthalpies below (kJ for the equation as written, products' water as liquid):

| Reaction | Equation | ΔH°rxn | Type |
|---|---|---|---|
{rx_rows}
## Standard enthalpies of formation at 25 °C

| Substance | ΔHf° (kJ/mol) |
|---|---|
{hf_rows}
Values from standard thermochemical tables (NIST, CRC Handbook), rounded to 0.1 kJ/mol; different tables can differ by a few tenths.

## Practical notes

- **Scale with the equation:** doubling all coefficients doubles ΔH, and reversing the reaction changes its sign.
- **Standard conditions:** ΔH° is for 1 bar and 25 °C. At other temperatures the value changes a little, by the difference in heat capacity of products and reactants (Kirchhoff's law).
- **Bond enthalpies** give only rough estimates (often within 5–10%) because they are averages; formation enthalpies give much better values.
- To measure a heat of combustion directly, use the [bomb calorimeter calculator](/chemistry/bomb-calorimeter/); to decide whether a reaction is spontaneous, combine ΔH with entropy in the [Gibbs free energy calculator](/chemistry/gibbs-free-energy/).
''')

# ---------------------------------------------------------------- Gas density
MAIR = 28.9647
def gdens(Pa, TK, M, Z=1.0):
    return Pa * M / 1000 / (Z * R * TK)
gP, gT, gM, gZ = 101325.0, 293.15, MAIR, 1.0
grho = gdens(gP, gT, gM, gZ); gSG = gM / MAIR; gv = 1 / grho; gVm = gZ * R * gT / gP * 1000; grN = gdens(101325, 273.15, gM)
GASES = (('Hydrogen, H₂', 2.016), ('Helium, He', 4.0026), ('Methane, CH₄', 16.043), ('Ammonia, NH₃', 17.031), ('Nitrogen, N₂', 28.014),
         ('Carbon monoxide, CO', 28.010), ('Air (dry)', MAIR), ('Oxygen, O₂', 31.999), ('Hydrogen sulfide, H₂S', 34.08),
         ('Argon, Ar', 39.948), ('Carbon dioxide, CO₂', 44.010), ('Propane, C₃H₈', 44.097), ('Butane, C₄H₁₀', 58.122), ('Chlorine, Cl₂', 70.90))
gg_rows = ''.join(f"| {nm} | {M:g} | {gdens(101325, 273.15, M):.4f} | {gdens(101325, 288.15, M):.4f} | {gdens(101325, 293.15, M):.4f} | {M/MAIR:.3f} |\n" for nm, M in GASES)
ga_rows = ''
for bg in (0, 1, 2, 4, 6, 8, 10, 16):
    Pabs = (bg + 1.01325) * 1e5
    ga_rows += f"| {bg} bar(g) | {Pabs/1e5:.3f} bar(a) | " + ' | '.join(f"{gdens(Pabs, 273.15 + t, MAIR):.3f}" for t in (0, 20, 40, 60)) + " |\n"
P('chemistry', 'gas-density', f'''
title: Gas Density Calculator (from Pressure, Temperature & Molar Mass)
description: Calculate the density of any gas from absolute pressure, temperature and molar mass with ρ = PM/ZRT, plus specific gravity, specific volume and molar volume.
category: chemistry
{intro("The density of a gas changes with pressure and temperature, so it has to be calculated at the actual operating conditions for flow measurement, compressor and vessel sizing or buoyancy checks. This gas density calculator uses the ideal gas law with an optional compressibility factor Z to give the density from the absolute pressure, temperature and molar mass, along with the specific gravity relative to air, the specific volume, the molar volume and the density at normal conditions — the values needed for [pressure and temperature compensation](ib:temperature-and-pressure-compensation) of gas flow meters.")}
keywords: [gas density calculator, density of gas formula, ideal gas density calculator, gas density at pressure and temperature, air density calculator, specific gravity of gas, compressibility factor density, rho pm rt]
updated: {D}
variables:
  - {{ id: P, label: Absolute pressure, family: pressure, unit: kPa, imperialUnit: psi, default: {gP/1000:g}, min: 0, help: 'Absolute = gauge + atmospheric (101.325 kPa at sea level).' }}
  - {{ id: T, label: Gas temperature, family: temperature, unit: C, imperialUnit: F, default: {gT-273.15:g}, min: 0 }}
  - {{ id: M, label: Molar mass of the gas, suffix: g/mol, default: {gM:g}, min: 0, help: 'Air 28.96, N₂ 28.01, O₂ 32.00, CO₂ 44.01, CH₄ 16.04, H₂ 2.016.' }}
  - {{ id: Z, label: Compressibility factor Z, default: {gZ:g}, min: 0, decimals: 4, help: '1 for an ideal gas; close to 1 for air and N₂ near ambient conditions.' }}
  - {{ id: rho, label: Gas density, family: density, unit: kgm3, imperialUnit: lbft3, min: 0, decimals: 4 }}
  - {{ id: SG, label: Specific gravity relative to air, min: 0, decimals: 4 }}
  - {{ id: sv, label: Specific volume, suffix: m³/kg, min: 0, decimals: 4 }}
  - {{ id: Vm, label: Molar volume, suffix: L/mol, min: 0, decimals: 3 }}
  - {{ id: rhoN, label: Ideal density at normal conditions (0 °C and 101.325 kPa), family: density, unit: kgm3, imperialUnit: lbft3, min: 0, decimals: 4 }}
equations:
  - rho = P * M / 1000 / (Z * 8.314462618 * T)
  - SG = M / 28.9647
  - sv = 1 / rho
  - Vm = Z * 8.314462618 * T / P * 1000
  - rhoN = 101325 * M / 1000 / (8.314462618 * 273.15)
faq:
  - q: How do you calculate the density of a gas?
    a: ρ = P M ÷ (Z R T), with P the absolute pressure in Pa, M the molar mass in kg/mol, R = 8.314 J/(mol·K), T the absolute temperature in kelvin and Z the compressibility factor (1 for an ideal gas). Dry air at 101.325 kPa and 20 °C has a density of 101,325 × 0.028965 ÷ (8.314 × 293.15) = 1.204 kg/m³.
  - q: How does gas density change with pressure and temperature?
    a: Density is proportional to absolute pressure and inversely proportional to absolute temperature. Doubling the absolute pressure doubles the density; heating a gas from 20 °C to 60 °C (293 K to 333 K) lowers its density by about 12%.
  - q: What is the specific gravity of a gas?
    a: It is the gas density divided by the density of air at the same pressure and temperature, which for ideal gases equals M ÷ 28.96. Gases with a specific gravity below 1, such as methane (0.55) and hydrogen (0.07), rise in air; propane (1.52) and CO₂ (1.52) collect in low places.
  - q: When do I need the compressibility factor Z?
    a: Near room temperature and up to a few bar, air, nitrogen, oxygen and methane have Z within about 1% of 1, so the ideal gas law is fine. At high pressure (natural gas pipelines, gas cylinders) or near condensation (CO₂, propane, steam), Z can be well below 1 — use a value from an equation of state, AGA-8 or a Z chart.
related: [physics/ideal-gas-law, engineering/gas-flow-correction, physics/density, chemistry/combined-gas-law]
''', f'''
## How to use the gas density calculator

Enter the **absolute pressure** (gauge pressure plus atmospheric), the **gas temperature**, the **molar mass** of the gas and, for real gases at high pressure, its **compressibility factor Z**. The calculator gives the **density** at those conditions, the specific gravity relative to air, the specific volume, the molar volume and the ideal density at normal conditions (0 °C, 1 atm). For a gas mixture, use the mole-fraction-weighted molar mass, M = Σ x<sub>i</sub> M<sub>i</sub>.

## Gas density formula

<p class="formula">ρ = P M ÷ (Z R T) &nbsp;·&nbsp; SG = M ÷ M<sub>air</sub> &nbsp;·&nbsp; v = 1 ÷ ρ &nbsp;·&nbsp; V<sub>m</sub> = Z R T ÷ P</p>

R = 8.314462618 J/(mol·K), M<sub>air</sub> = 28.9647 g/mol, P in Pa absolute, T in K and M in kg/mol (g/mol ÷ 1,000).

## Worked example: air at 20 °C

Dry air (M = {gM:g} g/mol) at {gP/1000:g} kPa absolute and {gT-273.15:g} °C, treated as ideal (Z = 1):

- ρ = {gP:,.0f} × {gM/1000:.7f} ÷ (1 × 8.314462618 × {gT:g}) = **{grho:.4f} kg/m³**
- Specific gravity = {gM:g} ÷ 28.9647 = **{gSG:.4f}**
- Specific volume = 1 ÷ {grho:.4f} = **{gv:.4f} m³/kg**
- Molar volume = 8.314462618 × {gT:g} ÷ {gP:,.0f} × 1000 = **{gVm:.3f} L/mol**
- At 0 °C and 101.325 kPa the same air would have a density of **{grN:.4f} kg/m³**

## Density of common gases at 1 atm (ideal gas)

| Gas | M (g/mol) | ρ at 0 °C (kg/m³) | ρ at 15 °C | ρ at 20 °C | SG (air = 1) |
|---|---|---|---|---|---|
{gg_rows}
Real-gas values at 1 atm differ from these by less than 1% for most gases; CO₂, H₂S, NH₃, Cl₂ and butane are a little denser because Z is below 1.

## Compressed air density (kg/m³)

Dry air, ideal gas, atmospheric pressure 1.01325 bar:

| Gauge pressure | Absolute pressure | 0 °C | 20 °C | 40 °C | 60 °C |
|---|---|---|---|---|---|
{ga_rows}
## Practical notes

- **Always use absolute pressure and temperature** — using gauge pressure or °C directly is the most common mistake.
- **Humid air** is slightly less dense than dry air because water vapour (18.02 g/mol) is lighter than air; at 30 °C and high humidity the difference is around 1–2%.
- **Standard conditions differ:** "normal" (0 °C, 1.01325 bar) is common in Europe and Asia, while "standard" may mean 15 °C or 60 °F and 1 atm. State which one you use when converting volumes — see the [gas flow correction calculator](/engineering/gas-flow-correction/).
- For the full ideal gas law with volume and moles, use the [ideal gas law calculator](/physics/ideal-gas-law/).
''')

# ======================================================================= MATH

# ---------------------------------------------------------------- Fraction calculator
fa, fb, fc, fd = 3, 4, 5, 6
F1, F2 = Fraction(fa, fb), Fraction(fc, fd)
fs, fdf, fp, fq = F1 + F2, F1 - F2, F1 * F2, F1 / F2
def fr(x):
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else f"{x.numerator}"
def mixed(x):
    if x.denominator == 1 or abs(x) < 1: return fr(x)
    w = int(abs(x.numerator) // x.denominator); r = abs(x.numerator) % x.denominator
    return f"{'-' if x < 0 else ''}{w} {r}/{x.denominator}"
EX = ((1, 2, 1, 3), (2, 3, 3, 4), (5, 8, 3, 8), (7, 10, 2, 5), (1, 6, 4, 9), (11, 12, 5, 18), (-3, 4, 1, 2))
fx_rows = ''
for a, b, c, d in EX:
    x, y = Fraction(a, b), Fraction(c, d)
    fx_rows += f"| {a}/{b} and {c}/{d} | {fr(x+y)} | {fr(x-y)} | {fr(x*y)} | {fr(x/y)} |\n"
lcd = fb * fd // math.gcd(fb, fd)
P('math', 'fraction-calculator', f'''
title: Fraction Calculator (Add, Subtract, Multiply, Divide)
description: Add, subtract, multiply and divide two fractions at once — every answer simplified to lowest terms and shown as a decimal, with the steps explained.
category: math
{intro("Working with fractions means finding common denominators, multiplying across and simplifying the result — easy to get wrong by hand. This fraction calculator takes two fractions and gives their sum, difference, product and quotient at the same time, each reduced to lowest terms with the greatest common factor and also shown as a decimal.")}
keywords: [fraction calculator, adding fractions calculator, subtracting fractions, multiplying fractions calculator, dividing fractions calculator, simplify fractions, fractions with different denominators]
updated: {D}
variables:
  - {{ id: a, label: Numerator of the first fraction, default: {fa}, decimals: 0 }}
  - {{ id: b, label: Denominator of the first fraction, default: {fb}, min: 1, decimals: 0 }}
  - {{ id: c, label: Numerator of the second fraction, default: {fc}, decimals: 0 }}
  - {{ id: d, label: Denominator of the second fraction, default: {fd}, min: 1, decimals: 0 }}
  - {{ id: sN, label: Sum a/b + c/d — numerator, decimals: 0 }}
  - {{ id: sD, label: Sum — denominator, decimals: 0 }}
  - {{ id: sv, label: Sum as a decimal, decimals: 6 }}
  - {{ id: dN, label: Difference a/b − c/d — numerator, decimals: 0 }}
  - {{ id: dD, label: Difference — denominator, decimals: 0 }}
  - {{ id: dv, label: Difference as a decimal, decimals: 6 }}
  - {{ id: pN, label: Product a/b × c/d — numerator, decimals: 0 }}
  - {{ id: pD, label: Product — denominator, decimals: 0 }}
  - {{ id: pv, label: Product as a decimal, decimals: 6 }}
  - {{ id: qN, label: Quotient a/b ÷ c/d — numerator, decimals: 0 }}
  - {{ id: qD, label: Quotient — denominator, decimals: 0 }}
  - {{ id: qv, label: Quotient as a decimal, decimals: 6 }}
equations:
  - sN = sign(b * d) * (a * d + c * b) / gcd(a * d + c * b, b * d)
  - sD = abs(b * d) / gcd(a * d + c * b, b * d)
  - sv = (a * d + c * b) / (b * d)
  - dN = sign(b * d) * (a * d - c * b) / gcd(a * d - c * b, b * d)
  - dD = abs(b * d) / gcd(a * d - c * b, b * d)
  - dv = (a * d - c * b) / (b * d)
  - pN = sign(b * d) * a * c / gcd(a * c, b * d)
  - pD = abs(b * d) / gcd(a * c, b * d)
  - pv = a * c / (b * d)
  - qN = sign(b * c) * a * d / gcd(a * d, b * c)
  - qD = abs(b * c) / gcd(a * d, b * c)
  - qv = a * d / (b * c)
freedom: 4
faq:
  - q: How do you add fractions with different denominators?
    a: Rewrite both fractions over a common denominator, add the numerators and simplify. For 3/4 + 5/6 the lowest common denominator is 12, so 9/12 + 10/12 = 19/12, which is 1 7/12 as a mixed number. Multiplying the denominators (24) also works — you just have more simplifying to do at the end.
  - q: How do you multiply and divide fractions?
    a: To multiply, multiply the numerators together and the denominators together — 3/4 × 5/6 = 15/24 = 5/8. To divide, multiply by the reciprocal of the second fraction — 3/4 ÷ 5/6 = 3/4 × 6/5 = 18/20 = 9/10.
  - q: How do you simplify a fraction?
    a: Divide the numerator and the denominator by their greatest common factor. For 38/24 the GCF is 2, giving 19/12. A fraction is in lowest terms when the GCF of the numerator and denominator is 1.
  - q: How do I enter a mixed number or a negative fraction?
    a: Convert a mixed number to an improper fraction first — 2 1/3 becomes (2 × 3 + 1)/3 = 7/3. For a negative fraction, put the minus sign on the numerator, for example −3 over 4.
related: [math/fraction-to-decimal, math/gcf-lcm, math/ratio, math/percentage]
''', f'''
## How to use the fraction calculator

Enter the **numerator and denominator** of each fraction as whole numbers (put a minus sign on the numerator for a negative fraction). The calculator gives the **sum, difference, product and quotient** of the two fractions together, each simplified to lowest terms, plus the decimal value of each answer. Convert mixed numbers to improper fractions before entering them.

## Fraction formulas

<p class="formula">a/b + c/d = (ad + bc) ÷ bd &nbsp;·&nbsp; a/b − c/d = (ad − bc) ÷ bd</p>

<p class="formula">a/b × c/d = ac ÷ bd &nbsp;·&nbsp; a/b ÷ c/d = ad ÷ bc</p>

Each result is then divided top and bottom by the greatest common factor (GCF) of its numerator and denominator.

## Worked example: {fa}/{fb} and {fc}/{fd}

- **Sum:** ({fa} × {fd} + {fc} × {fb}) ÷ ({fb} × {fd}) = {fa*fd + fc*fb}/{fb*fd}; GCF {math.gcd(fa*fd + fc*fb, fb*fd)} → **{fr(fs)}** = {mixed(fs)} = {float(fs):.6f}
- **Difference:** ({fa} × {fd} − {fc} × {fb}) ÷ ({fb} × {fd}) = {fa*fd - fc*fb}/{fb*fd}; GCF {math.gcd(fa*fd - fc*fb, fb*fd)} → **{fr(fdf)}** = {float(fdf):.6f}
- **Product:** ({fa} × {fc}) ÷ ({fb} × {fd}) = {fa*fc}/{fb*fd}; GCF {math.gcd(fa*fc, fb*fd)} → **{fr(fp)}** = {float(fp):.6f}
- **Quotient:** ({fa} × {fd}) ÷ ({fb} × {fc}) = {fa*fd}/{fb*fc}; GCF {math.gcd(fa*fd, fb*fc)} → **{fr(fq)}** = {float(fq):.6f}

With the lowest common denominator ({lcd}) the sum is {fa*lcd//fb}/{lcd} + {fc*lcd//fd}/{lcd} = {fa*lcd//fb + fc*lcd//fd}/{lcd} — the same answer with less simplifying.

## Solved examples

| Fractions | Sum | Difference | Product | Quotient |
|---|---|---|---|---|
{fx_rows}
## Practical notes

- **Mixed numbers:** an improper fraction such as 19/12 is 1 whole and 7/12 left over — divide the numerator by the denominator; the quotient is the whole number and the remainder is the new numerator.
- **Dividing by zero:** a fraction with a denominator of 0 is undefined, and you cannot divide by a fraction whose numerator is 0.
- **Cancel first:** when multiplying, cancelling common factors across before multiplying keeps the numbers small — 4/9 × 3/8 = (1 × 1)/(3 × 2) = 1/6.
- To turn a fraction into a decimal or percentage, use the [fraction to decimal calculator](/math/fraction-to-decimal/); to find the GCF or LCM of two numbers, use the [GCF and LCM calculator](/math/gcf-lcm/).
''')

print(len(DESC), 'pages:', ' '.join(DESC))
