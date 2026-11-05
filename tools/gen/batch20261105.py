import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
D = '2026-11-05'
G = 9.80665
def rad(x): return x * math.pi / 180
DESC = []
def P(cat, slug, fm, body):
    import re
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    DESC.append(slug)
    page(cat, slug, fm, body)

# ======================================================================= ENGINEERING

# ---------------------------------------------------------------- LMTD
Thi, Tho, Tci, Tco, U, Qd = 150.0, 90.0, 30.0, 70.0, 500.0, 250000.0
def lmtd(a, b): return a if abs(a - b) < 1e-12 else (a - b) / math.log(a / b)
d1, d2 = Thi - Tco, Tho - Tci
LM = lmtd(d1, d2); Ar = Qd / (U * LM)
p1, p2 = Thi - Tci, Tho - Tco; LMp = lmtd(p1, p2)
lm_rows = ''
for a, b in [(80, 60), (60, 40), (50, 10), (40, 20), (30, 15), (20, 5), (100, 50), (10, 9)]:
    lm_rows += f"| {a} K | {b} K | {(a+b)/2:g} K | {lmtd(a, b):.2f} K |\n"
P('engineering', 'lmtd', f'''
title: LMTD Calculator (Log Mean Temperature Difference & HX Area)
description: Calculate the log mean temperature difference (LMTD) for counterflow or parallel-flow heat exchangers, plus heat duty or area from Q = U·A·LMTD.
category: engineering
{intro("The log mean temperature difference is the true average driving force for heat transfer between two fluids in a heat exchanger. This LMTD calculator works out the LMTD from the four terminal temperatures for counterflow or parallel flow, then sizes the exchanger with Q = U·A·LMTD — see the [types of heat exchangers](ib:types-of-heat-exchangers) and how a [plate heat exchanger works](ib:plate-heat-exchanger-working-principle).")}
keywords: [lmtd calculator, log mean temperature difference calculator, heat exchanger area calculator, lmtd formula, counterflow heat exchanger, q = u a lmtd, heat exchanger sizing]
updated: {D}
variables:
  - id: s
    label: Flow arrangement
    default: 1
    options:
      - {{ label: Counterflow, value: 1 }}
      - {{ label: Parallel flow (co-current), value: 0 }}
  - {{ id: Thi, label: Hot fluid inlet temperature, family: temperature, unit: C, imperialUnit: F, default: {Thi:g} }}
  - {{ id: Tho, label: Hot fluid outlet temperature, family: temperature, unit: C, imperialUnit: F, default: {Tho:g} }}
  - {{ id: Tci, label: Cold fluid inlet temperature, family: temperature, unit: C, imperialUnit: F, default: {Tci:g} }}
  - {{ id: Tco, label: Cold fluid outlet temperature, family: temperature, unit: C, imperialUnit: F, default: {Tco:g} }}
  - {{ id: U, label: Overall heat transfer coefficient U, suffix: W/m²·K, default: {U:g}, min: 0 }}
  - {{ id: Q, label: Heat duty, family: power, unit: kW, imperialUnit: BTUh, default: {Qd/1000:g}, min: 0 }}
  - {{ id: dT1, label: Temperature difference at end 1 (ΔT₁), family: tempdiff, unit: K }}
  - {{ id: dT2, label: Temperature difference at end 2 (ΔT₂), family: tempdiff, unit: K }}
  - {{ id: LM, label: Log mean temperature difference (LMTD), family: tempdiff, unit: K }}
  - {{ id: A, label: Required heat transfer area, family: area, unit: m2, imperialUnit: ft2, min: 0 }}
equations:
  - dT1 = Thi - s * Tco - (1 - s) * Tci
  - dT2 = Tho - s * Tci - (1 - s) * Tco
  - LM = (dT1 - dT2) / ln(dT1 / dT2)
  - Q = U * A * LM
faq:
  - q: What is the LMTD formula?
    a: LMTD = (ΔT₁ − ΔT₂) ÷ ln(ΔT₁ ÷ ΔT₂), where ΔT₁ and ΔT₂ are the hot-to-cold temperature differences at the two ends of the exchanger.
  - q: How are ΔT₁ and ΔT₂ defined for counterflow?
    a: For counterflow, ΔT₁ = hot inlet − cold outlet and ΔT₂ = hot outlet − cold inlet. For parallel flow, ΔT₁ = hot inlet − cold inlet and ΔT₂ = hot outlet − cold outlet.
  - q: Why is counterflow better than parallel flow?
    a: With the same terminal temperatures counterflow gives a larger LMTD, so it needs less area, and it lets the cold outlet temperature rise above the hot outlet temperature.
  - q: What about shell-and-tube exchangers with several passes?
    a: Multiply the counterflow LMTD by a correction factor F (usually 0.75–1.0 from TEMA charts) — Q = U·A·F·LMTD. Designs with F below about 0.8 are normally avoided.
related: [engineering/heat-duty, engineering/convection-heat-transfer, engineering/chiller-tonnage, chemistry/specific-heat]
''', f'''
## How to use the LMTD calculator

Choose **counterflow** or **parallel flow** and enter the inlet and outlet temperatures of both fluids. The calculator returns ΔT₁, ΔT₂ and the LMTD. Enter the **overall heat transfer coefficient U** and the **heat duty Q** to get the required area — or clear Q and enter an area to find how much heat an existing exchanger can transfer.

## LMTD formula

<p class="formula">LMTD = (ΔT₁ − ΔT₂) ÷ ln(ΔT₁ ÷ ΔT₂) &nbsp;·&nbsp; Q = U × A × LMTD</p>

## Worked example

Hot oil cools from 150 °C to 90 °C, water heats from 30 °C to 70 °C, counterflow, U = 500 W/m²·K, duty 250 kW:

- ΔT₁ = 150 − 70 = **{d1:g} K**, ΔT₂ = 90 − 30 = **{d2:g} K**
- LMTD = ({d1:g} − {d2:g}) ÷ ln({d1:g} ÷ {d2:g}) = **{LM:.2f} K**
- A = 250,000 ÷ (500 × {LM:.2f}) = **{Ar:.2f} m²**

In parallel flow the same temperatures give ΔT₁ = {p1:g} K, ΔT₂ = {p2:g} K and LMTD = {LMp:.2f} K, so {Qd/(U*LMp):.2f} m² would be needed.

## LMTD vs arithmetic mean

| ΔT₁ | ΔT₂ | Arithmetic mean | LMTD |
|---|---|---|---|
{lm_rows}
The arithmetic mean always overstates the driving force; the error is small only when ΔT₁ and ΔT₂ are close.

## Notes

- If ΔT₁ = ΔT₂ the formula is 0 ÷ 0 — the LMTD then equals that common ΔT.
- A temperature cross (ΔT ≤ 0 at one end) is impossible for the chosen arrangement — check the temperatures.
- Typical U values: water–water plate exchanger 2,000–6,000 W/m²·K, shell-and-tube water–water 800–1,500, oil–water 100–400, gas–gas 10–50.
''')

# ---------------------------------------------------------------- Pump affinity laws
Q1, H1, P1, N1, N2, Dm1, Dm2 = 100.0, 50.0, 18.5, 1450.0, 1160.0, 250.0, 250.0
r = N2 / N1
pa_rows = ''
for pct in (100, 90, 80, 70, 60, 50):
    k = pct / 100
    pa_rows += f"| {pct}% ({N1*k:.0f} rpm) | {Q1*k:.1f} m³/h | {H1*k*k:.1f} m | {P1*k**3:.2f} kW | {100*(1-k**3):.0f}% |\n"
P('engineering', 'pump-affinity-laws', f'''
title: Pump Affinity Laws Calculator (Speed & Impeller Diameter)
description: Apply the pump affinity laws — find new flow, head and power of a centrifugal pump after a change in speed (VFD) or impeller diameter (trimming).
category: engineering
{intro("The affinity laws predict how a centrifugal pump's flow, head and power change with speed or impeller diameter: flow scales with the ratio, head with its square and power with its cube. This pump affinity laws calculator applies them for a VFD speed change or an impeller trim — useful when comparing [centrifugal vs positive displacement pumps](ib:centrifugal-vs-positive-displacement-pump) or sizing a [VFD](ib:vfd-sizing-selection-guide).")}
keywords: [pump affinity laws calculator, affinity laws, pump speed change calculator, impeller trimming calculator, vfd pump energy savings, pump flow head power speed, centrifugal pump laws]
updated: {D}
variables:
  - {{ id: Q1, label: Original flow rate Q₁, family: flow, unit: m3h, imperialUnit: gpm, default: {Q1:g}, min: 0 }}
  - {{ id: H1, label: Original head H₁, family: length, unit: m, imperialUnit: ft, default: {H1:g}, min: 0 }}
  - {{ id: P1, label: Original shaft power P₁, family: power, unit: kW, imperialUnit: hp, default: {P1:g}, min: 0 }}
  - {{ id: N1, label: Original speed N₁, suffix: rpm, default: {N1:g}, min: 0 }}
  - {{ id: N2, label: New speed N₂, suffix: rpm, default: {N2:g}, min: 0 }}
  - {{ id: D1, label: Original impeller diameter D₁, family: length, unit: mm, imperialUnit: in, default: {Dm1:g}, min: 0 }}
  - {{ id: D2, label: New impeller diameter D₂, family: length, unit: mm, imperialUnit: in, default: {Dm2:g}, min: 0 }}
  - {{ id: Q2, label: New flow rate Q₂, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: H2, label: New head H₂, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: P2, label: New shaft power P₂, family: power, unit: kW, imperialUnit: hp, min: 0 }}
equations:
  - Q2 = Q1 * (N2 / N1) * (D2 / D1)
  - H2 = H1 * (N2 / N1)^2 * (D2 / D1)^2
  - P2 = P1 * (N2 / N1)^3 * (D2 / D1)^3
faq:
  - q: What are the pump affinity laws?
    a: Q₂/Q₁ = N₂/N₁, H₂/H₁ = (N₂/N₁)² and P₂/P₁ = (N₂/N₁)³. The same relations hold approximately for a change in impeller diameter D at constant speed.
  - q: How much energy does slowing a pump save?
    a: Power falls with the cube of speed, so running at 80% speed needs about 51% of the power — a 49% saving — if the system has little static head.
  - q: Do the affinity laws work with high static head?
    a: Not directly. They move the pump along curves of constant efficiency, but a system with large static head does not follow those curves — find the new duty point on the system curve instead.
  - q: How accurate are they for impeller trimming?
    a: Reasonably for trims up to about 10–15% of diameter. Beyond that efficiency drops and the actual head and flow fall below the predicted values.
related: [engineering/pump-power, engineering/fan-affinity-laws, engineering/pressure-to-head, engineering/torque-power-speed]
''', f'''
## How to use the pump affinity laws calculator

Enter the pump's known duty point — **flow, head and shaft power** — at the original speed and impeller diameter, then enter the **new speed** and/or **new diameter**. Keep D₂ = D₁ for a pure speed change, or N₂ = N₁ for an impeller trim.

## Pump affinity laws

<p class="formula">Q₂ = Q₁ (N₂/N₁)(D₂/D₁) &nbsp;·&nbsp; H₂ = H₁ (N₂/N₁)²(D₂/D₁)² &nbsp;·&nbsp; P₂ = P₁ (N₂/N₁)³(D₂/D₁)³</p>

## Worked example

A pump delivers 100 m³/h at 50 m head and absorbs 18.5 kW at 1,450 rpm. A VFD slows it to 1,160 rpm (ratio {r:.2f}):

- Q₂ = 100 × {r:.2f} = **{Q1*r:.1f} m³/h**
- H₂ = 50 × {r:.2f}² = **{H1*r*r:.1f} m**
- P₂ = 18.5 × {r:.2f}³ = **{P1*r**3:.2f} kW** — a {100*(1-r**3):.0f}% power reduction

## Speed reduction table (100 m³/h, 50 m, 18.5 kW at 1,450 rpm)

| Speed | Flow | Head | Power | Power saving |
|---|---|---|---|---|
{pa_rows}
## Notes

- Efficiency is assumed constant — real savings are slightly lower because motor and VFD losses rise at low load.
- Check that the reduced head still overcomes the static head of the system.
- For fans and blowers the same laws apply; see the [fan affinity laws calculator](/engineering/fan-affinity-laws/).
''')

# ---------------------------------------------------------------- Fan power & affinity
fQ, fdp, feta, fN1, fN2 = 10000.0, 1000.0, 0.70, 1450.0, 1160.0
fQs = fQ / 3600; fPa = fQs * fdp; fPs = fPa / feta; fr = fN2 / fN1
fa_rows = ''
for pct in (100, 90, 80, 70, 60, 50):
    k = pct / 100
    fa_rows += f"| {pct}% | {fQ*k:,.0f} m³/h | {fdp*k*k:.0f} Pa | {fPs*k**3/1000:.2f} kW |\n"
P('engineering', 'fan-affinity-laws', f'''
title: Fan Power & Fan Affinity Laws Calculator (CFM, Pa, kW)
description: Calculate fan air and shaft power from airflow, pressure rise and efficiency, then use the fan affinity laws to predict flow, pressure and power at a new speed.
category: engineering
{intro("A fan's air power is simply airflow times pressure rise, and its shaft power is that divided by the fan efficiency. This fan affinity laws calculator finds both, then scales flow, pressure and power to a new speed — flow with the speed ratio, pressure with its square and power with its cube — which is how [VFD energy savings](ib:vfd-sizing-selection-guide) on fans are estimated.")}
keywords: [fan affinity laws calculator, fan power calculator, fan shaft power, blower power calculator, fan laws, cfm static pressure power, fan speed change]
updated: {D}
variables:
  - {{ id: Q, label: Airflow, family: flow, unit: m3h, imperialUnit: cfm, default: {fQ:g}, min: 0 }}
  - {{ id: dp, label: Fan total pressure rise, family: pressure, unit: Pa, imperialUnit: inH2O, default: {fdp:g}, min: 0 }}
  - {{ id: eta, label: Fan efficiency (total), family: percent, unit: '%', default: {feta*100:g}, min: 0.01, max: 1 }}
  - {{ id: N1, label: Present speed N₁, suffix: rpm, default: {fN1:g}, min: 0 }}
  - {{ id: N2, label: New speed N₂, suffix: rpm, default: {fN2:g}, min: 0 }}
  - {{ id: Pa, label: Air power, family: power, unit: kW, imperialUnit: hp, min: 0 }}
  - {{ id: Ps, label: Fan shaft power, family: power, unit: kW, imperialUnit: hp, min: 0 }}
  - {{ id: Q2, label: Airflow at new speed, family: flow, unit: m3h, imperialUnit: cfm, min: 0 }}
  - {{ id: dp2, label: Pressure at new speed, family: pressure, unit: Pa, imperialUnit: inH2O, min: 0 }}
  - {{ id: Ps2, label: Shaft power at new speed, family: power, unit: kW, imperialUnit: hp, min: 0 }}
equations:
  - Pa = Q * dp
  - Ps = Pa / eta
  - Q2 = Q * N2 / N1
  - dp2 = dp * (N2 / N1)^2
  - Ps2 = Ps * (N2 / N1)^3
faq:
  - q: How do I calculate fan power?
    a: Air power = Q × Δp (m³/s × Pa = W). Shaft power = air power ÷ fan efficiency. 10,000 m³/h at 1,000 Pa is 2.78 kW of air power, or about 3.97 kW at the shaft with a 70% efficient fan.
  - q: What are the fan affinity laws?
    a: At constant air density, Q₂/Q₁ = N₂/N₁, p₂/p₁ = (N₂/N₁)² and P₂/P₁ = (N₂/N₁)³.
  - q: What is the fan power formula in imperial units?
    a: Shaft horsepower = CFM × total pressure (in. w.g.) ÷ (6356 × efficiency).
  - q: Should I use static or total pressure?
    a: Use fan total pressure with total efficiency, or fan static pressure with static efficiency — do not mix them. Both give the same shaft power.
related: [engineering/pump-affinity-laws, engineering/pump-power, engineering/torque-power-speed, electrical/three-phase-motor-power]
''', f'''
## How to use the fan power calculator

Enter the **airflow**, the **pressure rise** across the fan and the **fan efficiency** to get air and shaft power. Then enter the present and new **speeds** to see how flow, pressure and power change — for example when a VFD slows the fan.

## Fan power and fan law formulas

<p class="formula">P<sub>air</sub> = Q × Δp &nbsp;·&nbsp; P<sub>shaft</sub> = Q × Δp ÷ η &nbsp;·&nbsp; Q₂ = Q₁(N₂/N₁) &nbsp;·&nbsp; Δp₂ = Δp₁(N₂/N₁)² &nbsp;·&nbsp; P₂ = P₁(N₂/N₁)³</p>

## Worked example

10,000 m³/h ({fQs:.4f} m³/s) against 1,000 Pa, fan efficiency 70%, slowed from 1,450 to 1,160 rpm:

- Air power = {fQs:.4f} × 1,000 = **{fPa/1000:.3f} kW**
- Shaft power = {fPa/1000:.3f} ÷ 0.70 = **{fPs/1000:.3f} kW**
- At 1,160 rpm: Q = **{fQ*fr:,.0f} m³/h**, Δp = **{fdp*fr*fr:.0f} Pa**, shaft power = **{fPs*fr**3/1000:.3f} kW**

## Fan speed table (10,000 m³/h, 1,000 Pa, 70% efficiency)

| Speed | Airflow | Pressure | Shaft power |
|---|---|---|---|
{fa_rows}
## Notes

- Air density matters: pressure and power scale with density, so a fan handling hot air needs less power for the same volume flow.
- Add motor and drive losses to the shaft power when sizing the motor.
''')

# ---------------------------------------------------------------- Pressure to head
hp_dp, hp_rho = 5e5, 998.0
hp_H = hp_dp / (hp_rho * G)
hp_rows = ''
for name, rho in [('Water (20 °C)', 998), ('Seawater', 1025), ('Diesel', 840), ('Petrol', 740), ('Ethylene glycol', 1110), ('Sulphuric acid 98%', 1830), ('Mercury', 13534)]:
    hp_rows += f"| {name} | {rho} | {1e5/(rho*G):.3f} m | {6894.757293168/(rho*G)/0.3048:.3f} ft |\n"
P('engineering', 'pressure-to-head', f'''
title: Pressure to Head Calculator (Bar, psi to Metres of Pump Head)
description: Convert pressure to head and head to pressure for any liquid — pump head from pressure in bar, kPa or psi using H = Δp ÷ (ρ·g), with a density table.
category: engineering
{intro("Pump curves are drawn in metres or feet of head, while gauges read in bar or psi, so you often need to convert between them. This pressure to head calculator uses H = Δp ÷ (ρ·g) for any liquid density — the same relation behind [hydrostatic level measurement](ib:hydrostatic-level-measurement).")}
keywords: [pressure to head calculator, head to pressure calculator, bar to metres head, psi to feet of head, pump head from pressure, pressure head formula, metres of water column]
updated: {D}
variables:
  - {{ id: dp, label: Pressure (or pressure difference), family: pressure, unit: bar, imperialUnit: psi, default: {hp_dp/1e5:g}, min: 0 }}
  - {{ id: rho, label: Liquid density, family: density, unit: kgm3, imperialUnit: lbft3, default: {hp_rho:g}, min: 0 }}
  - {{ id: H, label: Head, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: SG, label: Specific gravity (vs water at 4 °C), min: 0 }}
equations:
  - H = dp / (rho * g0)
  - SG = rho / 999.97
faq:
  - q: How do I convert pressure to head?
    a: H = Δp ÷ (ρ × g). For water, 1 bar ≈ 10.2 m of head and 1 psi ≈ 2.31 ft of head.
  - q: How do I calculate pump head from gauge readings?
    a: Take discharge pressure minus suction pressure and convert with H = Δp ÷ (ρg). For total head also add the elevation difference between the gauges and any velocity-head difference.
  - q: Why does pump head not depend on the liquid?
    a: A pump adds the same head (energy per unit weight) to any liquid of similar viscosity, but the pressure it produces is proportional to density — so a pump makes less pressure on petrol than on water.
  - q: What is the head of 1 psi of water?
    a: About 0.703 m or 2.31 ft of water at room temperature.
related: [engineering/hydrostatic-pressure, engineering/pump-power, engineering/pump-affinity-laws, engineering/darcy-weisbach-head-loss]
''', f'''
## How to use the pressure to head calculator

Enter the **pressure** (or pressure difference across a pump) and the **liquid density**. The calculator returns the equivalent **head** of that liquid. To go the other way, clear the pressure and enter the head.

## Pressure head formula

<p class="formula">H = Δp ÷ (ρ × g) &nbsp;·&nbsp; Δp = ρ × g × H</p>

## Worked example

A pump raises water (ρ = 998 kg/m³) by 5 bar:

- H = 500,000 ÷ (998 × 9.80665) = **{hp_H:.2f} m** of head ({hp_H/0.3048:.1f} ft)

## Head of 1 bar and 1 psi for common liquids

| Liquid | Density (kg/m³) | Head per bar | Head per psi |
|---|---|---|---|
{hp_rows}
## Notes

- Use the density at the pumping temperature — hot water at 90 °C (965 kg/m³) gives about 3% more head per bar than cold water.
- Gauge readings must both be gauge or both be absolute; only the difference matters for pump head.
''')

# ---------------------------------------------------------------- Convection
ch, cA, cTs, cTf = 25.0, 2.0, 80.0, 25.0
cQ = ch * cA * (cTs - cTf)
cv_rows = ''
for name, lo, hi in [('Free convection — air', 2, 25), ('Free convection — water', 50, 1000), ('Forced convection — air', 25, 250), ('Forced convection — water', 100, 20000), ('Forced convection — oil', 50, 1500), ('Boiling water', 2500, 100000), ('Condensing steam', 5000, 100000)]:
    cv_rows += f"| {name} | {lo:,} – {hi:,} | {lo*cA*(cTs-cTf):,.0f} – {hi*cA*(cTs-cTf):,.0f} W |\n"
P('engineering', 'convection-heat-transfer', f'''
title: Convection Heat Transfer Calculator (Q = h·A·ΔT)
description: Calculate convective heat transfer rate with Newton's law of cooling, Q = h·A·ΔT, or solve for the heat transfer coefficient, area or temperature difference.
category: engineering
{intro("Convection is heat carried away by a moving fluid, and its rate is set by the heat transfer coefficient h, the surface area and the surface-to-fluid temperature difference. This convection heat transfer calculator solves Q = h·A·(Ts − T∞) for any one unknown and lists typical h values — it pairs with [calculating heat loss in piping](ib:calculate-heat-loss-in-piping).")}
keywords: [convection heat transfer calculator, q = h a delta t calculator, heat transfer coefficient calculator, convective heat transfer formula, newton's law of cooling convection, heat flux calculator]
updated: {D}
variables:
  - {{ id: h, label: Heat transfer coefficient h, suffix: W/m²·K, default: {ch:g}, min: 0 }}
  - {{ id: A, label: Surface area, family: area, unit: m2, imperialUnit: ft2, default: {cA:g}, min: 0 }}
  - {{ id: Ts, label: Surface temperature, family: temperature, unit: C, imperialUnit: F, default: {cTs:g} }}
  - {{ id: Tf, label: Fluid (bulk) temperature, family: temperature, unit: C, imperialUnit: F, default: {cTf:g} }}
  - {{ id: Q, label: Heat transfer rate, family: power, unit: W, imperialUnit: BTUh }}
  - {{ id: q, label: Heat flux, suffix: W/m² }}
equations:
  - Q = h * A * (Ts - Tf)
  - q = Q / A
faq:
  - q: What is the convection heat transfer formula?
    a: Q = h × A × (Ts − T∞), where h is the convective heat transfer coefficient (W/m²·K), A the surface area and Ts − T∞ the difference between surface and fluid temperature.
  - q: What is a typical heat transfer coefficient for air?
    a: About 2–25 W/m²·K in still air (natural convection) and 25–250 W/m²·K with forced air flow.
  - q: Is this the same as Newton's law of cooling?
    a: Yes — Q = hAΔT is Newton's law of cooling. The physics version of that law gives the temperature-versus-time curve of a cooling object.
  - q: What does a negative result mean?
    a: The fluid is hotter than the surface, so heat flows into the surface instead of out of it.
related: [physics/newtons-law-of-cooling, physics/heat-conduction, engineering/lmtd, physics/stefan-boltzmann-law]
''', f'''
## How to use the convection heat transfer calculator

Enter the **heat transfer coefficient h**, the **surface area** and the **surface and fluid temperatures**. The calculator returns the heat transfer rate and the heat flux. Clear any input and enter Q to solve for it — for example the h needed to remove a known heat load.

## Convection formula

<p class="formula">Q = h × A × (T<sub>s</sub> − T<sub>∞</sub>) &nbsp;·&nbsp; q = Q ÷ A</p>

## Worked example

A 2 m² surface at 80 °C in air at 25 °C with h = 25 W/m²·K:

- Q = 25 × 2 × (80 − 25) = **{cQ:,.0f} W**
- Heat flux = {cQ:,.0f} ÷ 2 = **{cQ/cA:,.0f} W/m²**

## Typical heat transfer coefficients (2 m², ΔT = 55 K)

| Situation | h (W/m²·K) | Heat transfer rate |
|---|---|---|
{cv_rows}
## Notes

- Hot surfaces also lose heat by radiation — at 80 °C in still air it can equal the convective loss; see the [Stefan–Boltzmann calculator](/physics/stefan-boltzmann-law/).
- For heat transfer between two fluids through a wall, use an overall coefficient U and the [LMTD calculator](/engineering/lmtd/).
''')

# ---------------------------------------------------------------- Chiller tonnage
TRW = 3516.8528
chQ, chdT, chcp, chrho = 50.0, 5.0, 4186.0, 998.0
chW = chrho * chQ / 3600 * chcp * chdT
ct_rows = ''
for q in (10, 25, 50, 100, 200, 500):
    ct_rows += f"| {q} m³/h | " + ' | '.join(f"{chrho*q/3600*chcp*dt/TRW:.1f}" for dt in (4, 5, 6, 8)) + " |\n"
P('engineering', 'chiller-tonnage', f'''
title: Chiller Tonnage Calculator (TR from Flow & ΔT)
description: Calculate chiller capacity in tons of refrigeration (TR) and kW from chilled water flow and temperature difference, Q = m·cp·ΔT, with a sizing table.
category: engineering
{intro("A chiller's cooling load is the heat the chilled water picks up: mass flow × specific heat × temperature rise. This chiller tonnage calculator turns flow and ΔT into kW and tons of refrigeration (1 TR = 3.517 kW) — see the step-by-step guide to [calculating industrial chiller capacity](ib:calculate-industrial-chiller-capacity).")}
keywords: [chiller tonnage calculator, chiller capacity calculator, tons of refrigeration calculator, tr calculation formula, chilled water flow calculator, chiller sizing, kw to tr]
updated: {D}
variables:
  - {{ id: V, label: Chilled water flow rate, family: flow, unit: m3h, imperialUnit: gpm, default: {chQ:g}, min: 0 }}
  - {{ id: dT, label: Temperature difference (return − supply), family: tempdiff, unit: K, imperialUnit: F, default: {chdT:g}, min: 0 }}
  - {{ id: cp, label: Specific heat of the fluid, suffix: J/kg·K, default: {chcp:g}, min: 0 }}
  - {{ id: rho, label: Fluid density, family: density, unit: kgm3, imperialUnit: lbft3, default: {chrho:g}, min: 0 }}
  - {{ id: Q, label: Cooling load, family: power, unit: kW, imperialUnit: BTUh, min: 0 }}
  - {{ id: TR, label: Chiller capacity, family: power, unit: TR, min: 0 }}
equations:
  - Q = rho * V * cp * dT
  - TR = Q
faq:
  - q: How do I calculate chiller tonnage?
    a: Cooling load Q = ρ × flow × cp × ΔT. Divide the result in kW by 3.517 to get tons of refrigeration. 50 m³/h of water with a 5 K rise is about 290 kW or 82.5 TR.
  - q: What is the GPM formula for chiller tons?
    a: Tons = GPM × ΔT(°F) ÷ 24 for water. It comes from 500 × GPM × ΔT BTU/h divided by 12,000 BTU/h per ton.
  - q: How much is 1 ton of refrigeration?
    a: 12,000 BTU/h = 3.517 kW — the heat needed to melt one short ton of ice in 24 hours.
  - q: What about glycol?
    a: Use the glycol mixture's specific heat and density. 30% ethylene glycol has cp ≈ 3,700 J/kg·K, so it carries about 10% less heat than water at the same flow and ΔT.
related: [engineering/heat-duty, engineering/lmtd, engineering/pump-power, chemistry/specific-heat]
''', f'''
## How to use the chiller tonnage calculator

Enter the **chilled water flow**, the **temperature difference** between return and supply water, and the fluid's **specific heat** and **density** (defaults are water). The calculator gives the cooling load in kW and in tons of refrigeration. To size the flow for a known load, clear the flow and enter the tonnage.

## Chiller capacity formula

<p class="formula">Q = ρ × V̇ × c<sub>p</sub> × ΔT &nbsp;·&nbsp; TR = Q (kW) ÷ 3.517</p>

## Worked example

50 m³/h of water returning at 12 °C and supplied at 7 °C (ΔT = 5 K):

- Mass flow = 998 × 50 ÷ 3,600 = {chrho*chQ/3600:.2f} kg/s
- Q = {chrho*chQ/3600:.2f} × 4,186 × 5 = **{chW/1000:.1f} kW**
- Capacity = {chW/1000:.1f} ÷ 3.517 = **{chW/TRW:.1f} TR**

## Chiller capacity (TR) by flow and ΔT (water)

| Flow | ΔT 4 K | ΔT 5 K | ΔT 6 K | ΔT 8 K |
|---|---|---|---|---|
{ct_rows}
## Notes

- Add a design margin of 10–20% and allow for pump heat and pipe heat gains.
- Comfort cooling usually uses 7 °C supply / 12 °C return (ΔT 5 K); process chillers vary.
''')

# ---------------------------------------------------------------- Compressor power (isentropic)
k_, cp1, cp2, cV, cT1, ceta = 1.4, 1.01325e5, 8e5, 600.0, 20.0, 0.75
cVs = cV / 3600
def cpow(p1, p2, V, k, eta): return k / (k - 1) * p1 * V * ((p2 / p1) ** ((k - 1) / k) - 1) / eta
cPis = cpow(cp1, cp2, cVs, k_, 1); cPs = cPis / ceta
cT2 = (cT1 + 273.15) * (cp2 / cp1) ** ((k_ - 1) / k_) - 273.15
cp_rows = ''
for p2 in (3, 5, 7, 8, 10, 13):
    pr = p2 * 1e5 / cp1
    cp_rows += f"| {p2} bar(a) | {pr:.2f} | {cpow(cp1, p2*1e5, cVs, k_, ceta)/1000:.1f} kW | {cpow(cp1, p2*1e5, cVs, k_, ceta)/1000/(cV/60):.2f} kW per m³/min | {(cT1+273.15)*pr**((k_-1)/k_)-273.15:.0f} °C |\n"
P('engineering', 'compressor-power', f'''
title: Compressor Power Calculator (Isentropic, Single Stage)
description: Estimate air or gas compressor power from inlet flow, suction and discharge pressure and isentropic efficiency, plus the ideal discharge temperature.
category: engineering
{intro("The ideal work to compress a gas follows the isentropic (adiabatic) relation, and real compressors need more by the inverse of their isentropic efficiency. This compressor power calculator gives the shaft power and ideal discharge temperature for a single stage — staging, explained in [single-stage vs multi-stage compressors](ib:single-stage-and-multi-stage-compressor), cuts power at high pressure ratios.")}
keywords: [compressor power calculator, isentropic compressor power, air compressor kw calculator, adiabatic compression power, compressor discharge temperature, gas compressor power formula, compressor sizing]
updated: {D}
variables:
  - {{ id: V, label: Inlet volumetric flow (actual), family: flow, unit: m3h, imperialUnit: cfm, default: {cV:g}, min: 0 }}
  - {{ id: p1, label: Suction pressure (absolute), family: pressure, unit: bar, imperialUnit: psi, default: {cp1/1e5:g}, min: 0 }}
  - {{ id: p2, label: Discharge pressure (absolute), family: pressure, unit: bar, imperialUnit: psi, default: {cp2/1e5:g}, min: 0 }}
  - {{ id: T1, label: Suction temperature, family: temperature, unit: C, imperialUnit: F, default: {cT1:g}, min: 0 }}
  - {{ id: k, label: Ratio of specific heats k (cp/cv), default: {k_:g}, min: 1.0001, help: 'Air and N₂ 1.40, natural gas ≈ 1.3, CO₂ 1.29, H₂ 1.41.' }}
  - {{ id: eta, label: Isentropic efficiency, family: percent, unit: '%', default: {ceta*100:g}, min: 0.01, max: 1 }}
  - {{ id: Pis, label: Ideal (isentropic) power, family: power, unit: kW, imperialUnit: hp, min: 0 }}
  - {{ id: Ps, label: Compressor shaft power, family: power, unit: kW, imperialUnit: hp, min: 0 }}
  - {{ id: T2, label: Ideal discharge temperature, family: temperature, unit: C, imperialUnit: F }}
equations:
  - Pis = k / (k - 1) * p1 * V * ((p2 / p1)^((k - 1) / k) - 1)
  - Ps = Pis / eta
  - T2 = T1 * (p2 / p1)^((k - 1) / k)
faq:
  - q: What is the isentropic compressor power formula?
    a: P = (k ÷ (k − 1)) × p₁ × V₁ × [(p₂ ÷ p₁)^((k−1)/k) − 1] ÷ η, with absolute pressures, actual inlet flow V₁ in m³/s and isentropic efficiency η.
  - q: How much power does an air compressor need per m³/min?
    a: Roughly 6–7 kW per m³/min of free air at 7–8 bar(g) for a typical two-stage or oil-injected screw compressor. A single stage to 8 bar(a) at 75% isentropic efficiency needs about 6.3 kW per m³/min of shaft power.
  - q: Why must pressures be absolute?
    a: The compression ratio p₂/p₁ only has physical meaning in absolute pressure. Add atmospheric pressure (about 1.013 bar) to gauge readings.
  - q: When should I use multiple stages?
    a: Above a pressure ratio of about 4–5 per stage the discharge temperature gets too high. Intercooled stages with equal pressure ratios approach isothermal compression and use less power.
related: [engineering/gas-flow-correction, physics/ideal-gas-law, engineering/fan-affinity-laws, engineering/absolute-gauge-pressure]
''', f'''
## How to use the compressor power calculator

Enter the **actual inlet flow**, the **suction and discharge pressures in absolute units**, the **suction temperature**, the gas's **ratio of specific heats k** and the compressor's **isentropic efficiency**. The calculator returns the ideal power, the shaft power and the ideal (isentropic) discharge temperature.

## Isentropic compression formulas

<p class="formula">P = k/(k−1) × p₁ V₁ × [(p₂/p₁)<sup>(k−1)/k</sup> − 1] ÷ η &nbsp;·&nbsp; T₂ = T₁ (p₂/p₁)<sup>(k−1)/k</sup></p>

## Worked example

600 m³/h ({cVs:.4f} m³/s) of air at 1.01325 bar(a) and 20 °C compressed to 8 bar(a), k = 1.4, η = 75%:

- Pressure ratio = 8 ÷ 1.01325 = {cp2/cp1:.3f}; exponent (k−1)/k = {(k_-1)/k_:.4f}
- Ideal power = 3.5 × 101,325 × {cVs:.4f} × ({(cp2/cp1)**((k_-1)/k_):.4f} − 1) = **{cPis/1000:.1f} kW**
- Shaft power = {cPis/1000:.1f} ÷ 0.75 = **{cPs/1000:.1f} kW**
- Ideal discharge temperature = 293.15 × {(cp2/cp1)**((k_-1)/k_):.4f} − 273.15 = **{cT2:.0f} °C**

## Single-stage power vs discharge pressure (600 m³/h air, η = 75%)

| Discharge | Ratio | Shaft power | Specific power | Ideal T₂ |
|---|---|---|---|---|
{cp_rows}
## Notes

- Real discharge temperature is higher than the ideal value, roughly T₁ + (T₂ − T₁) ÷ η.
- Add motor efficiency and transmission losses to size the driver.
''')

# ---------------------------------------------------------------- Residence time
rV, rQ = 10.0, 5.0
rt = rV / rQ
rt_rows = ''
for V in (1, 5, 10, 25, 50, 100):
    rt_rows += f"| {V} m³ | " + ' | '.join(f"{V/q*60:.0f} min" if V / q < 2 else f"{V/q:.1f} h" for q in (2, 5, 10, 20, 50)) + " |\n"
P('engineering', 'residence-time', f'''
title: Residence Time Calculator (Hold-Up Time, τ = V ÷ Q)
description: Calculate residence time (hold-up or hydraulic retention time) of a tank, reactor or pipe from volume and flow rate, plus space velocity in volumes per hour.
category: engineering
{intro("Residence time is the average time a fluid spends inside a vessel — the liquid volume divided by the throughput. This residence time calculator works out τ = V ÷ Q for tanks, reactors, settling basins and pipes, and the space velocity (tank turnovers per hour).")}
keywords: [residence time calculator, hold up time calculator, hydraulic retention time calculator, space time reactor, retention time formula, tank residence time, space velocity calculator]
updated: {D}
variables:
  - {{ id: V, label: Liquid volume (working volume), family: volume, unit: m3, imperialUnit: galUS, default: {rV:g}, min: 0 }}
  - {{ id: Q, label: Volumetric flow rate (throughput), family: flow, unit: m3h, imperialUnit: gpm, default: {rQ:g}, min: 0 }}
  - {{ id: tau, label: Residence time τ, family: seconds, unit: h, min: 0 }}
  - {{ id: SV, label: Space velocity (volumes per hour), suffix: 1/h, min: 0 }}
equations:
  - tau = V / Q
  - SV = 3600 / tau
faq:
  - q: What is the residence time formula?
    a: τ = V ÷ Q — the working volume of the vessel divided by the volumetric flow rate through it. 10 m³ with 5 m³/h flowing through gives 2 hours.
  - q: Is residence time the same as space time?
    a: For a reactor, space time τ = V ÷ Q₀ is based on the inlet flow. It equals the mean residence time when the fluid density does not change through the reactor.
  - q: What is space velocity?
    a: The reciprocal of space time — how many vessel volumes pass through per hour. A residence time of 2 hours is a space velocity of 0.5 h⁻¹.
  - q: Do all particles stay for τ?
    a: Only in ideal plug flow. In a well-mixed tank, residence times follow an exponential distribution — about 63% of the fluid leaves before τ.
related: [engineering/vertical-tank-volume, engineering/horizontal-tank-volume, engineering/pipe-flow-velocity, engineering/mass-flow-rate]
''', f'''
## How to use the residence time calculator

Enter the **working (liquid) volume** and the **flow rate** through the vessel. The calculator returns the residence time and the space velocity. To size a vessel, clear the volume and enter the residence time you need.

## Residence time formula

<p class="formula">τ = V ÷ Q &nbsp;·&nbsp; SV = 1 ÷ τ</p>

## Worked example

A 10 m³ buffer tank with 5 m³/h flowing through it:

- τ = 10 ÷ 5 = **{rt:g} h** (120 min)
- Space velocity = 1 ÷ 2 h = **{1/rt:g} h⁻¹**

## Residence time by volume and flow

| Volume | 2 m³/h | 5 m³/h | 10 m³/h | 20 m³/h | 50 m³/h |
|---|---|---|---|---|---|
{rt_rows}
## Notes

- Use the liquid volume at normal operating level, not the vessel's total volume — get it from the [vertical tank](/engineering/vertical-tank-volume/) or [horizontal tank](/engineering/horizontal-tank-volume/) calculator.
- For a pipe, residence time = length ÷ velocity.
''')

# ---------------------------------------------------------------- Kinematic viscosity
vmu, vrho = 1.002, 998.2
vnu = vmu / vrho * 1000
kv_rows = ''
for name, mu, rho in [('Water, 20 °C', 1.002, 998.2), ('Water, 80 °C', 0.355, 971.8), ('Air, 20 °C', 0.0181, 1.204), ('Petrol', 0.6, 740), ('Diesel', 3.0, 840), ('Ethylene glycol, 20 °C', 16.1, 1113), ('SAE 30 oil, 40 °C', 90, 875), ('Glycerine, 20 °C', 1412, 1260)]:
    kv_rows += f"| {name} | {mu:g} | {rho:g} | {mu/rho*1000:.4g} |\n"
P('engineering', 'kinematic-viscosity', f'''
title: Kinematic Viscosity Calculator (cP to cSt, Dynamic ↔ Kinematic)
description: Convert dynamic viscosity (cP, mPa·s, Pa·s) to kinematic viscosity (cSt, mm²/s) and back with ν = μ ÷ ρ, with values for water, oils and air.
category: engineering
{intro("Dynamic viscosity measures a fluid's resistance to shear, while kinematic viscosity is that resistance divided by density. This kinematic viscosity calculator converts between the two with ν = μ ÷ ρ — so cP becomes cSt — as covered in [viscosity measurement explained](ib:viscosity-measurement-explained).")}
keywords: [kinematic viscosity calculator, cp to cst calculator, dynamic to kinematic viscosity, centipoise to centistokes, viscosity conversion, mm2/s to cp, kinematic viscosity formula]
updated: {D}
variables:
  - {{ id: mu, label: Dynamic viscosity μ, family: viscosity, unit: cP, default: {vmu:g}, min: 0 }}
  - {{ id: rho, label: Density ρ, family: density, unit: kgm3, imperialUnit: lbft3, default: {vrho:g}, min: 0 }}
  - {{ id: nu, label: Kinematic viscosity ν (cSt = mm²/s), suffix: cSt, min: 0 }}
equations:
  - nu = mu / rho * 1e6
faq:
  - q: How do I convert cP to cSt?
    a: Divide by the density in g/cm³ — cSt = cP ÷ SG. Water at 20 °C is 1.002 cP ÷ 0.998 = 1.004 cSt.
  - q: What is the kinematic viscosity formula?
    a: ν = μ ÷ ρ. In SI, Pa·s ÷ kg/m³ gives m²/s; 1 cSt = 1 mm²/s = 10⁻⁶ m²/s.
  - q: Which viscosity does the Reynolds number use?
    a: Either — Re = ρvD ÷ μ = vD ÷ ν. Use kinematic viscosity when the fluid data is given in cSt.
  - q: Why do lubricating oils use cSt?
    a: Oil viscosity grades (ISO VG) are measured with gravity-driven capillary viscometers, which directly measure kinematic viscosity in cSt at 40 °C.
related: [engineering/reynolds-number, engineering/darcy-weisbach-head-loss, physics/stokes-law, physics/density]
''', f'''
## How to use the kinematic viscosity calculator

Enter the **dynamic viscosity** (pick cP, mPa·s, P or Pa·s) and the **density** at the same temperature. The calculator returns the kinematic viscosity in centistokes (mm²/s). To go from cSt to cP, clear the dynamic viscosity and enter the kinematic value.

## Kinematic viscosity formula

<p class="formula">ν = μ ÷ ρ &nbsp;·&nbsp; ν (cSt) = μ (cP) ÷ ρ (g/cm³)</p>

## Worked example

Water at 20 °C, μ = 1.002 cP and ρ = 998.2 kg/m³:

- ν = 0.001002 ÷ 998.2 = 1.004 × 10⁻⁶ m²/s = **{vnu:.4f} cSt**

## Dynamic and kinematic viscosity of common fluids

| Fluid | μ (cP) | ρ (kg/m³) | ν (cSt) |
|---|---|---|---|
{kv_rows}
## Notes

- Viscosity changes strongly with temperature — always use μ and ρ at the same temperature.
- 1 P (poise) = 100 cP = 0.1 Pa·s; 1 St (stokes) = 100 cSt = 10⁻⁴ m²/s.
''')

# ---------------------------------------------------------------- Barlow
bS, bt, bD, bF = 290e6, 7.11e-3, 168.3e-3, 0.72
bPb = 2 * bS * bt / bD; bPa = bPb * bF
bw_rows = ''
for nps, od, wt in [('2"', 60.3, 3.91), ('3"', 88.9, 5.49), ('4"', 114.3, 6.02), ('6"', 168.3, 7.11), ('8"', 219.1, 8.18), ('10"', 273.0, 9.27), ('12"', 323.8, 10.31)]:
    pb = 2 * 241e6 * wt / od
    bw_rows += f"| {nps} Sch 40 | {od} | {wt} | {pb/1e6:.1f} | {pb*0.72/1e6:.1f} |\n"
P('engineering', 'barlow-formula', f'''
title: Barlow's Formula Calculator (Pipe Wall Thickness & Pressure)
description: Use Barlow's formula P = 2·S·t ÷ D to find the burst or allowable pressure of a pipe, or the wall thickness needed, with a design factor and Sch 40 table.
category: engineering
{intro("Barlow's formula relates the internal pressure a pipe can hold to its wall thickness, outside diameter and material strength. This Barlow's formula calculator gives the burst pressure and the design (allowable) pressure with a design factor, or the minimum wall thickness for a given pressure — a quick check before [hydrostatic testing](ib:hydrostatic-testing-in-oil-gas-industry).")}
keywords: [barlow's formula calculator, pipe wall thickness calculator, pipe pressure rating calculator, barlow formula, pipe burst pressure calculator, hoop stress pipe, allowable pipe pressure]
updated: {D}
variables:
  - {{ id: S, label: Material strength (SMYS or allowable stress), family: pressure, unit: MPa, imperialUnit: psi, default: {bS/1e6:g}, min: 0 }}
  - {{ id: t, label: Wall thickness, family: length, unit: mm, imperialUnit: in, default: {bt*1000:g}, min: 0 }}
  - {{ id: D, label: Outside diameter, family: length, unit: mm, imperialUnit: in, default: {bD*1000:g}, min: 0 }}
  - {{ id: F, label: Design factor (1 = burst), default: {bF:g}, min: 0, max: 1, help: 'ASME B31.8 class 1 = 0.72, class 2 = 0.60, class 3 = 0.50, class 4 = 0.40.' }}
  - {{ id: Pb, label: Pressure at which hoop stress reaches S (F = 1), family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
  - {{ id: Pd, label: Design (allowable) pressure, family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
equations:
  - Pb = 2 * S * t / D
  - Pd = Pb * F
faq:
  - q: What is Barlow's formula?
    a: P = 2 × S × t ÷ D, where S is the allowable or yield stress, t the wall thickness and D the outside diameter. It is the thin-wall hoop stress equation.
  - q: How do I find the wall thickness for a given pressure?
    a: Rearrange to t = P × D ÷ (2 × S × F). In the calculator clear the wall thickness and enter the design pressure.
  - q: Which strength value should I use?
    a: For gas pipelines (ASME B31.8) use the specified minimum yield strength with a design factor. For burst estimates use tensile strength with F = 1. For process piping use the code allowable stress.
  - q: Does Barlow's formula include corrosion allowance?
    a: No. Add corrosion allowance and mill tolerance (often 12.5% of wall) to the thickness — ASME B31.3 uses t = PD ÷ 2(SEW + PY) plus allowances.
related: [engineering/hydrostatic-pressure, engineering/factor-of-safety, engineering/water-hammer, engineering/pipe-flow-velocity]
''', f'''
## How to use the Barlow's formula calculator

Enter the pipe material **strength**, the **wall thickness** and the **outside diameter**, plus a **design factor**. The calculator returns the pressure at which the hoop stress equals S and the design pressure. Clear the wall thickness and enter a design pressure to find the minimum wall.

## Barlow's formula

<p class="formula">P = 2 S t ÷ D &nbsp;·&nbsp; P<sub>design</sub> = 2 S t F ÷ D &nbsp;·&nbsp; t = P D ÷ (2 S F)</p>

## Worked example

6" API 5L X42 line pipe (SMYS 290 MPa), OD 168.3 mm, wall 7.11 mm, design factor 0.72:

- P at SMYS = 2 × 290 × 7.11 ÷ 168.3 = **{bPb/1e6:.2f} MPa** ({bPb/1e5:.0f} bar)
- Design pressure = {bPb/1e6:.2f} × 0.72 = **{bPa/1e6:.2f} MPa** ({bPa/1e5:.0f} bar)

## Schedule 40 carbon steel pipe, S = 241 MPa (API 5L Gr B SMYS)

| Size | OD (mm) | Wall (mm) | P at SMYS (MPa) | P with F = 0.72 (MPa) |
|---|---|---|---|---|
{bw_rows}
## Notes

- Barlow's formula is a thin-wall approximation; it is conservative for thick walls (D/t below about 20).
- Always verify against the governing code (ASME B31.1, B31.3, B31.4, B31.8) before use.
''')

# ---------------------------------------------------------------- Valve authority
va_v, va_s = 0.5, 1.0
va_N = va_v / (va_v + va_s)
va_rows = ''
for dv in (0.1, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0):
    va_rows += f"| {dv:g} bar | " + ' | '.join(f"{dv/(dv+ds):.2f}" for ds in (0.5, 1.0, 2.0)) + " |\n"
P('engineering', 'valve-authority', f'''
title: Valve Authority Calculator (Control Valve Authority N)
description: Calculate control valve authority from the valve and circuit pressure drops, N = Δp valve ÷ (Δp valve + Δp system), with the recommended range.
category: engineering
{intro("Valve authority is the share of the circuit's variable pressure drop taken by the control valve at full flow — too low and the valve loses control at small openings. This valve authority calculator works out N from the valve and system pressure drops and rates the result, a useful check when choosing a [control valve flow coefficient](ib:control-valve-flow-coefficient).")}
keywords: [valve authority calculator, control valve authority, valve authority formula, hvac valve authority, control valve pressure drop, valve sizing authority, n = dp valve]
updated: {D}
variables:
  - {{ id: dpv, label: Pressure drop across the fully open valve, family: pressure, unit: bar, imperialUnit: psi, default: {va_v:g}, min: 0 }}
  - {{ id: dps, label: Pressure drop of the rest of the circuit (pipes, coil, fittings), family: pressure, unit: bar, imperialUnit: psi, default: {va_s:g}, min: 0 }}
  - id: N
    label: Valve authority N
    min: 0
    max: 1
    decimals: 3
    bands:
      - {{ max: 0.25, label: Poor — valve will hunt at low flow, color: '#dc2626' }}
      - {{ max: 0.5, label: Acceptable, color: '#eab308' }}
      - {{ max: 1.01, label: Good control, color: '#16a34a' }}
equations:
  - N = dpv / (dpv + dps)
faq:
  - q: What is valve authority?
    a: N = Δp across the fully open valve ÷ (that Δp + the pressure drop of the rest of the controlled circuit at design flow). It ranges from 0 to 1.
  - q: What is a good valve authority?
    a: Between 0.5 and about 0.7 is the usual design target for HVAC two-way valves; 0.25 is generally the lowest acceptable value.
  - q: Why not make the authority close to 1?
    a: Because the valve would then take almost all the available pressure, which wastes pump energy. Authority around 0.5 balances control quality and pumping cost.
  - q: What pressure drops should be included?
    a: Only the part of the circuit whose flow the valve varies — the coil, branch piping and fittings — not the constant-pressure parts upstream of a differential pressure controller.
related: [engineering/control-valve-kv-cv, engineering/minor-losses, engineering/darcy-weisbach-head-loss, engineering/pump-power]
''', f'''
## How to use the valve authority calculator

Enter the **pressure drop across the valve** when fully open at design flow and the **pressure drop of the rest of the circuit** (coil, branch pipe and fittings) at the same flow. The calculator returns the authority N and rates it.

## Valve authority formula

<p class="formula">N = Δp<sub>valve</sub> ÷ (Δp<sub>valve</sub> + Δp<sub>circuit</sub>)</p>

## Worked example

A valve dropping 0.5 bar in a branch whose coil and pipework drop 1.0 bar:

- N = 0.5 ÷ (0.5 + 1.0) = **{va_N:.3f}** — acceptable, but a smaller valve (higher Δp) would control better.

## Authority for different pressure drops

| Valve Δp | Circuit 0.5 bar | Circuit 1 bar | Circuit 2 bar |
|---|---|---|---|
{va_rows}
## Notes

- Low authority distorts an equal-percentage characteristic toward quick-opening, so most flow change happens in the first part of the stroke.
- To raise authority choose a valve with a smaller Kv / Cv — check it with the [control valve Kv/Cv calculator](/engineering/control-valve-kv-cv/).
''')

# ---------------------------------------------------------------- Spherical tank
sD, sh = 10.0, 4.0
sR = sD / 2
def sv(R, h): return math.pi * h * h * (3 * R - h) / 3
sV = sv(sR, sh); sVf = 4 / 3 * math.pi * sR ** 3
sp_rows = ''
for f in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
    h = f * sD
    sp_rows += f"| {f*100:.0f}% ({h:.1f} m) | {sv(sR, h):.2f} m³ | {sv(sR, h)/sVf*100:.1f}% |\n"
P('engineering', 'spherical-tank-volume', f'''
title: Spherical Tank Volume Calculator (Partially Filled Sphere)
description: Calculate the liquid volume in a partially filled spherical tank from its diameter and liquid level, the full capacity and percent filled, with a level table.
category: engineering
{intro("Storage spheres for LPG, ammonia and other pressurised liquids hold far more or less than a simple level percentage suggests, because the cross-section changes with height. This spherical tank volume calculator uses the spherical-cap formula to convert level to volume — the basis of [LPG level measurement in bullets and spheres](ib:lpg-level-measurement-bullet-sphere) and of [tank volume from level](ib:tank-volume-from-level-measurement).")}
keywords: [spherical tank volume calculator, partially filled sphere volume, sphere tank level to volume, spherical cap volume, lpg sphere volume, tank strapping sphere, sphere fill percentage]
updated: {D}
variables:
  - {{ id: D, label: Sphere inside diameter, family: length, unit: m, imperialUnit: ft, default: {sD:g}, min: 0 }}
  - {{ id: h, label: Liquid level (from bottom), family: length, unit: m, imperialUnit: ft, default: {sh:g}, min: 0 }}
  - {{ id: V, label: Liquid volume, family: volume, unit: m3, imperialUnit: galUS, min: 0 }}
  - {{ id: Vt, label: Total capacity, family: volume, unit: m3, imperialUnit: galUS, min: 0 }}
  - {{ id: f, label: Percent filled (by volume), family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - V = pi * h^2 * (3 * D / 2 - h) / 3
  - Vt = pi * D^3 / 6
  - f = V / Vt
faq:
  - q: What is the formula for a partially filled sphere?
    a: V = π h² (3R − h) ÷ 3, where R is the radius and h the liquid depth. It is the volume of a spherical cap and holds for any level from 0 to 2R.
  - q: Why is 50% level exactly 50% volume?
    a: A sphere is symmetrical about its equator, so half the height holds half the volume. Below and above the middle, volume changes much more slowly per unit level than in a vertical cylinder.
  - q: How full should an LPG sphere be filled?
    a: Typically to no more than 85% of volume to leave vapour space for thermal expansion — check the local regulation and the design.
  - q: Does the calculator use inside or outside diameter?
    a: Inside diameter. Subtract twice the wall thickness from the outside diameter for an accurate capacity.
related: [engineering/horizontal-tank-volume, engineering/vertical-tank-volume, math/sphere, engineering/dp-level-range]
''', f'''
## How to use the spherical tank volume calculator

Enter the **inside diameter** of the sphere and the **liquid level** measured from the bottom. The calculator returns the liquid volume, the full capacity and the percent filled. To find the level for a given volume, clear the level and enter the volume.

## Spherical tank volume formula

<p class="formula">V = π h² (3R − h) ÷ 3 &nbsp;·&nbsp; V<sub>total</sub> = π D³ ÷ 6</p>

## Worked example

A 10 m sphere (R = 5 m) with 4 m of liquid:

- V = π × 4² × (15 − 4) ÷ 3 = **{sV:.2f} m³**
- Capacity = π × 10³ ÷ 6 = **{sVf:.2f} m³**
- Filled = {sV:.2f} ÷ {sVf:.2f} = **{sV/sVf*100:.1f}%** — at 40% of the level

## Level-to-volume table for a 10 m sphere

| Level | Volume | % of capacity |
|---|---|---|
{sp_rows}
## Notes

- Level and volume are only equal (in percent) at 0, 50% and 100%.
- For mass, multiply the volume by the liquid density at the measured temperature.
''')

# ---------------------------------------------------------------- Absolute / gauge pressure
ag_pg, ag_alt = 2e5, 0.0
def patm(z): return 101325 * (1 - 2.25577e-5 * z) ** 5.25588
ag_pa = patm(ag_alt); ag_abs = ag_pg + ag_pa
ag_rows = ''
for z in (0, 500, 1000, 1500, 2000, 3000, 4000, 5000):
    ag_rows += f"| {z:,} m | {patm(z)/1000:.2f} kPa | {patm(z)/1e5:.4f} bar | {patm(z)/6894.757293168:.2f} psi |\n"
P('engineering', 'absolute-gauge-pressure', f'''
title: Absolute to Gauge Pressure Calculator (and Vacuum)
description: Convert gauge pressure to absolute pressure and back, including vacuum readings, with atmospheric pressure set directly or estimated from altitude.
category: engineering
{intro("Gauge pressure is measured relative to the surrounding atmosphere, absolute pressure relative to a perfect vacuum, and the difference is the local atmospheric pressure. This absolute to gauge pressure calculator converts between them — and handles vacuum as negative gauge pressure — as explained in [absolute vs gauge pressure](ib:absolute-vs-gauge-pressure) and [how to calculate vacuum pressure](ib:how-to-calculate-vacuum-pressure).")}
keywords: [absolute to gauge pressure calculator, gauge to absolute pressure, psia to psig, bar g to bar a, vacuum pressure calculator, atmospheric pressure altitude, absolute pressure formula]
updated: {D}
variables:
  - {{ id: pg, label: Gauge pressure (negative = vacuum), family: pressure, unit: bar, imperialUnit: psi, default: {ag_pg/1e5:g}, min: -1e7 }}
  - {{ id: z, label: Altitude above sea level, family: length, unit: m, imperialUnit: ft, default: {ag_alt:g}, min: -500, max: 11000 }}
  - {{ id: pa, label: Atmospheric pressure, family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
  - {{ id: pabs, label: Absolute pressure, family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
equations:
  - pa = 101325 * (1 - 2.25577e-5 * z)^5.25588
  - pabs = pg + pa
faq:
  - q: How do I convert gauge pressure to absolute pressure?
    a: Add atmospheric pressure — p_abs = p_gauge + p_atm. At sea level 2 bar(g) is 3.013 bar(a), and 100 psig is 114.7 psia.
  - q: How is vacuum related to gauge pressure?
    a: Vacuum is negative gauge pressure. A vacuum of 0.6 bar at sea level is −0.6 bar(g), or 1.013 − 0.6 = 0.413 bar(a).
  - q: Why does altitude matter?
    a: Atmospheric pressure falls about 12% per 1,000 m near sea level, so the same absolute pressure reads differently on a gauge at altitude. Enter the altitude or override atmospheric pressure with a barometer reading.
  - q: Can absolute pressure be negative?
    a: No — zero absolute is a perfect vacuum, so the most negative gauge reading possible is minus the atmospheric pressure.
related: [engineering/hydrostatic-pressure, engineering/gas-flow-correction, engineering/manometer, engineering/compressor-power]
''', f'''
## How to use the absolute to gauge pressure calculator

Enter the **gauge pressure** (use a negative value for vacuum) and the **altitude**. The calculator estimates atmospheric pressure with the standard-atmosphere formula and returns the absolute pressure. To convert absolute to gauge, clear the gauge pressure and enter the absolute value. If you have a barometer reading, clear the altitude and enter the atmospheric pressure directly.

## Absolute pressure formulas

<p class="formula">p<sub>abs</sub> = p<sub>gauge</sub> + p<sub>atm</sub> &nbsp;·&nbsp; p<sub>atm</sub> = 101,325 × (1 − 2.25577×10⁻⁵ z)<sup>5.25588</sup> Pa</p>

## Worked example

2 bar(g) at sea level:

- p<sub>atm</sub> = **{ag_pa/1e5:.5f} bar**
- p<sub>abs</sub> = 2 + {ag_pa/1e5:.5f} = **{ag_abs/1e5:.5f} bar(a)**

## Standard atmospheric pressure by altitude

| Altitude | kPa | bar | psi |
|---|---|---|---|
{ag_rows}
## Notes

- Weather changes atmospheric pressure by about ±3% around the standard value.
- Gas flow corrections and compressor calculations always need absolute pressure.
''')

# ---------------------------------------------------------------- Manometer
mrm, mrf, mL, mth = 1000.0, 1.2, 0.150, 30.0
mh = mL * math.sin(rad(mth)); mdp = (mrm - mrf) * G * mh
mn_rows = ''
for name, rho in [('Water', 1000), ('Red gauge oil (SG 0.826)', 826), ('Paraffin (SG 0.80)', 800), ('Mercury', 13595)]:
    mn_rows += f"| {name} | " + ' | '.join(f"{(rho-1.2)*G*0.1*math.sin(rad(a)):.1f}" for a in (90, 30, 10)) + " |\n"
P('engineering', 'manometer', f'''
title: Manometer Calculator (U-Tube & Inclined Manometer)
description: Calculate differential pressure from a U-tube or inclined manometer reading, Δp = (ρm − ρf)·g·L·sin θ, for water, oil or mercury filled manometers.
category: engineering
{intro("A manometer measures pressure difference as the height of a liquid column, and tilting the tube spreads a small height over a longer, easier-to-read scale. This manometer calculator converts a U-tube or inclined manometer reading into pressure, including the effect of the fluid above the manometer liquid — see the [U-tube manometer working principle and formula](ib:u-tube-manometer-working-formula).")}
keywords: [manometer calculator, u tube manometer calculator, inclined manometer calculator, manometer formula, differential pressure manometer, mm water column to pa, manometer reading to pressure]
updated: {D}
variables:
  - {{ id: rm, label: Manometer liquid density, family: density, unit: kgm3, imperialUnit: lbft3, default: {mrm:g}, min: 0 }}
  - {{ id: rf, label: Density of the fluid above it (process fluid), family: density, unit: kgm3, imperialUnit: lbft3, default: {mrf:g}, min: 0 }}
  - {{ id: L, label: Reading along the tube, family: length, unit: mm, imperialUnit: in, default: {mL*1000:g}, min: 0 }}
  - {{ id: th, label: Tube angle from horizontal (90° = U-tube), family: angle, unit: deg, default: {mth:g}, min: 0, max: 1.5707964 }}
  - {{ id: h, label: Vertical height difference, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: dp, label: Differential pressure, family: pressure, unit: Pa, imperialUnit: inH2O, min: 0 }}
equations:
  - h = L * sin(th)
  - dp = (rm - rf) * g0 * h
faq:
  - q: What is the U-tube manometer formula?
    a: Δp = (ρm − ρf) × g × h, where ρm is the manometer liquid density, ρf the density of the fluid above it and h the difference in liquid levels. For gases ρf is usually negligible.
  - q: How does an inclined manometer work?
    a: The vertical height is h = L × sin θ, so at 30° the scale reading L is twice the vertical height; at about 5.7° it is ten times. This makes small pressures easier to read.
  - q: What fluid should I use in a manometer?
    a: Water or light gauge oil for small draft and filter pressures (a few hundred Pa), mercury for pressures of tens of kPa. Mercury is now avoided for safety reasons.
  - q: What is 1 mm of water column in pascals?
    a: About 9.81 Pa (9.80665 Pa by definition at standard gravity).
related: [engineering/hydrostatic-pressure, engineering/absolute-gauge-pressure, engineering/pressure-to-head, engineering/pitot-tube-velocity]
''', f'''
## How to use the manometer calculator

Enter the **manometer liquid density**, the **density of the fluid above it** (air ≈ 1.2 kg/m³, or the process liquid), the **reading along the tube** and the **tube angle** — 90° for a vertical U-tube. The calculator returns the vertical height and the differential pressure.

## Manometer formula

<p class="formula">h = L × sin θ &nbsp;·&nbsp; Δp = (ρ<sub>m</sub> − ρ<sub>f</sub>) × g × h</p>

## Worked example

A water-filled inclined manometer at 30° reads 150 mm along the tube, measuring air:

- h = 150 × sin 30° = **{mh*1000:.0f} mm**
- Δp = (1,000 − 1.2) × 9.80665 × {mh:.3f} = **{mdp:.1f} Pa**

## Pressure for a 100 mm scale reading (Pa, measuring air)

| Manometer liquid | Vertical (90°) | Inclined 30° | Inclined 10° |
|---|---|---|---|
{mn_rows}
## Notes

- For a liquid-over-liquid manometer (for example mercury under water) the fluid density term matters: use ρ<sub>m</sub> − ρ<sub>f</sub>.
- Level the instrument carefully — an error of 1° at a 10° incline changes the reading by about 10%.
''')

# ======================================================================= ELECTRONICS

# ---------------------------------------------------------------- Crystal load capacitance
xC1, xC2, xCs = 22.0, 22.0, 5.0
xCL = xC1 * xC2 / (xC1 + xC2) + xCs
xl_rows = ''
for CL in (6, 7, 8, 9, 10, 12, 12.5, 16, 18, 20):
    xl_rows += f"| {CL:g} pF | " + ' | '.join(f"{2*(CL-cs):.0f} pF" if CL > cs else '—' for cs in (2, 3, 5)) + " |\n"
P('electronics', 'crystal-load-capacitance', f'''
title: Crystal Load Capacitance Calculator (Pierce Oscillator Caps)
description: Calculate crystal load capacitance from the two Pierce oscillator capacitors and stray capacitance, CL = C1·C2 ÷ (C1 + C2) + Cstray, and pick the right caps.
category: electronics
{intro("A quartz crystal only oscillates at its marked frequency when the circuit presents the load capacitance it was cut for. This crystal load capacitance calculator finds the effective load from the two capacitors of a Pierce oscillator plus board stray capacitance — see how a [crystal oscillator works](ib:crystal-oscillator-working-principle).")}
keywords: [crystal load capacitance calculator, crystal capacitor calculator, pierce oscillator capacitors, load capacitance formula, crystal cl calculation, microcontroller crystal capacitors, stray capacitance crystal]
updated: {D}
variables:
  - {{ id: C1, label: Capacitor C1 (XIN to ground), family: capacitance, unit: pF, default: {xC1:g}, min: 0 }}
  - {{ id: C2, label: Capacitor C2 (XOUT to ground), family: capacitance, unit: pF, default: {xC2:g}, min: 0 }}
  - {{ id: Cs, label: Stray capacitance (pins + PCB), family: capacitance, unit: pF, default: {xCs:g}, min: 0, help: 'Typically 2–5 pF; check the microcontroller datasheet for pin capacitance.' }}
  - {{ id: CL, label: Effective load capacitance CL, family: capacitance, unit: pF, min: 0 }}
equations:
  - CL = C1 * C2 / (C1 + C2) + Cs
faq:
  - q: What is the crystal load capacitance formula?
    a: CL = (C1 × C2) ÷ (C1 + C2) + Cstray. The two capacitors are effectively in series across the crystal, plus the stray capacitance of the pins and traces.
  - q: How do I choose the capacitors for a crystal?
    a: With equal capacitors, C1 = C2 = 2 × (CL − Cstray). A 12.5 pF crystal with 3 pF stray needs two 19 pF capacitors — use 18 pF or 20 pF standard values.
  - q: What happens if the load capacitance is wrong?
    a: The frequency shifts — usually by a few to a few tens of ppm. Too much capacitance lowers the frequency and can stop a weak oscillator from starting; too little raises it.
  - q: Why not just use 22 pF?
    a: 22 pF suits 18–20 pF crystals. Low-power 32.768 kHz crystals rated 6–12.5 pF need much smaller capacitors, and 22 pF can make them run slow or fail to start.
related: [electronics/555-timer, electronics/resonant-frequency, electronics/capacitors-series-parallel, electronics/rc-phase-shift-oscillator]
''', f'''
## How to use the crystal load capacitance calculator

Enter the two **load capacitors** of the Pierce oscillator and an estimate of the **stray capacitance** of the pins and PCB traces. The calculator returns the effective load capacitance seen by the crystal — compare it with the CL on the crystal datasheet.

## Crystal load capacitance formula

<p class="formula">C<sub>L</sub> = C₁C₂ ÷ (C₁ + C₂) + C<sub>stray</sub> &nbsp;·&nbsp; equal caps: C₁ = C₂ = 2 (C<sub>L</sub> − C<sub>stray</sub>)</p>

## Worked example

C1 = C2 = 22 pF with 5 pF stray:

- Series value = 22 × 22 ÷ 44 = 11 pF
- C<sub>L</sub> = 11 + 5 = **{xCL:g} pF** — matches a 16 pF crystal

## Capacitor value needed (C1 = C2) for each crystal CL

| Crystal CL | Stray 2 pF | Stray 3 pF | Stray 5 pF |
|---|---|---|---|
{xl_rows}
## Notes

- Round to the nearest standard E12 value (10, 12, 15, 18, 22, 27 pF) and verify the frequency with a counter if accuracy matters.
- Keep crystal traces short and guard them with ground to keep stray capacitance low and predictable.
''')

# ---------------------------------------------------------------- UART baud rate error
uf, ub, uos = 16e6, 115200.0, 16
def ubaud(f, b, os_):
    N = round(f / (os_ * b)); act = f / (os_ * N); return N, act, (act - b) / b
uN, uact, uerr = ubaud(uf, ub, uos)
ua_rows = ''
for b in (9600, 19200, 38400, 57600, 115200, 230400, 250000):
    cells = []
    for f in (8e6, 16e6, 11.0592e6, 48e6):
        N, a, e = ubaud(f, b, 16)
        cells.append(f"{e*100:+.2f}%")
    ua_rows += f"| {b:,} | " + ' | '.join(cells) + " |\n"
P('electronics', 'uart-baud-rate-error', f'''
title: UART Baud Rate Error Calculator (Divisor & Actual Baud)
description: Calculate the UART baud rate divisor, actual baud rate and percentage error for any clock frequency and oversampling, with an error table for common crystals.
category: electronics
{intro("A UART makes its bit clock by dividing the system clock by an integer, so the actual baud rate is rarely exactly what you asked for. This UART baud rate error calculator finds the nearest divisor, the real baud rate and the error — keep it within about ±2% for reliable links, as explained in [UART frame format and baud rate](ib:uart-communication-frame-baud-rate).")}
keywords: [uart baud rate error calculator, baud rate calculator, ubrr calculator, uart divisor calculator, baud rate error percentage, serial baud rate clock, avr baud rate]
updated: {D}
variables:
  - {{ id: f, label: Peripheral clock frequency, family: frequency, unit: MHz, default: {uf/1e6:g}, min: 0 }}
  - {{ id: b, label: Desired baud rate, suffix: bit/s, default: {ub:g}, min: 1 }}
  - id: os
    label: Oversampling
    default: 16
    options:
      - {{ label: 16× (normal mode), value: 16 }}
      - {{ label: 8× (double speed), value: 8 }}
  - {{ id: N, label: Divisor (UBRR / BRR = N − 1 on AVR), min: 0 }}
  - {{ id: ba, label: Actual baud rate, suffix: bit/s, min: 0 }}
  - {{ id: err, label: Baud rate error, family: percent, unit: '%', decimals: 2 }}
equations:
  - N = max(1, round(f / (os * b)))
  - ba = f / (os * N)
  - err = (ba - b) / b
faq:
  - q: How is the UART baud rate divisor calculated?
    a: N = f_clk ÷ (oversampling × baud), rounded to the nearest integer. The actual baud rate is then f_clk ÷ (oversampling × N). On AVR the register value is UBRR = N − 1.
  - q: What baud rate error is acceptable?
    a: Keep each end within about ±2% (the total mismatch between the two ends must stay under roughly 4–5% for 8-N-1 frames). Below ±1% is good practice.
  - q: Why do 11.0592 MHz and 18.432 MHz crystals exist?
    a: They divide exactly into standard baud rates, giving 0% error at 9,600, 19,200, 57,600 and 115,200 baud.
  - q: Does fractional baud rate generation help?
    a: Yes — many STM32, NXP and ESP32 UARTs have a fractional divider, which reduces the error to a small fraction of a percent. This calculator assumes an integer divider.
related: [electronics/adc-resolution, electronics/pwm-duty-cycle, electronics/crystal-load-capacitance, electronics/555-timer]
''', f'''
## How to use the UART baud rate error calculator

Enter the UART's **clock frequency**, the **baud rate** you want and the **oversampling** mode. The calculator rounds to the nearest integer divisor and shows the actual baud rate and the percentage error.

## UART baud rate formulas

<p class="formula">N = round(f<sub>clk</sub> ÷ (OS × baud)) &nbsp;·&nbsp; baud<sub>actual</sub> = f<sub>clk</sub> ÷ (OS × N) &nbsp;·&nbsp; error = (baud<sub>actual</sub> − baud) ÷ baud</p>

## Worked example

16 MHz clock, 115,200 baud, 16× oversampling:

- f ÷ (16 × 115,200) = {uf/(16*ub):.3f} → N = **{uN}** (UBRR = {uN-1})
- Actual baud = 16,000,000 ÷ (16 × {uN}) = **{uact:,.0f} bit/s**
- Error = **{uerr*100:.2f}%** — too large; use 8× mode or a 11.0592 / 18.432 MHz crystal

## Baud rate error, 16× oversampling

| Baud rate | 8 MHz | 16 MHz | 11.0592 MHz | 48 MHz |
|---|---|---|---|---|
{ua_rows}
## Notes

- Both ends contribute error — a ±2% error on each side can add up to 4%.
- RC oscillators (internal clocks) can themselves be ±1–2% off; use a crystal for high baud rates.
''')

# ---------------------------------------------------------------- RC phase-shift oscillator
oR, oC = 10e3, 10e-9
of = 1 / (2 * math.pi * oR * oC * math.sqrt(6))
ro_rows = ''
for R in (1e3, 4.7e3, 10e3, 47e3, 100e3):
    ro_rows += f"| {R/1e3:g} kΩ | " + ' | '.join(f"{1/(2*math.pi*R*C*math.sqrt(6)):,.1f} Hz" for C in (1e-9, 10e-9, 100e-9, 1e-6)) + " |\n"
P('electronics', 'rc-phase-shift-oscillator', f'''
title: RC Phase Shift Oscillator Calculator (Frequency & Gain)
description: Calculate the frequency of a three-stage RC phase shift oscillator, f = 1 ÷ (2π·R·C·√6), and the feedback resistor for the required gain of 29.
category: electronics
{intro("An RC phase shift oscillator uses three RC sections to shift the signal by 180°, and an inverting amplifier to supply the other 180° and make up the loss. This RC phase shift oscillator calculator gives the oscillation frequency and the gain resistor needed — one of the [types of transistor oscillators](ib:types-of-transistor-oscillators), and a cousin of the [Wien bridge oscillator](ib:wien-bridge-oscillator-circuit).")}
keywords: [rc phase shift oscillator calculator, phase shift oscillator frequency, rc oscillator calculator, phase shift oscillator formula, op amp phase shift oscillator, rc oscillator frequency formula, gain of 29]
updated: {D}
variables:
  - {{ id: R, label: Resistance per stage R, family: resistance, unit: kohm, default: {oR/1e3:g}, min: 0 }}
  - {{ id: C, label: Capacitance per stage C, family: capacitance, unit: nF, default: {oC*1e9:g}, min: 0 }}
  - {{ id: f, label: Oscillation frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: Rf, label: Minimum feedback resistor (gain 29), family: resistance, unit: kohm, min: 0 }}
equations:
  - f = 1 / (2 * pi * R * C * sqrt(6))
  - Rf = 29 * R
faq:
  - q: What is the frequency of an RC phase shift oscillator?
    a: For three identical RC sections, f = 1 ÷ (2π R C √6) ≈ 0.065 ÷ (RC). With 10 kΩ and 10 nF it oscillates at about 650 Hz.
  - q: Why must the gain be 29?
    a: At the frequency where the three-section ladder shifts the phase by 180°, it attenuates the signal to 1/29. The amplifier needs a gain of at least 29 to sustain oscillation.
  - q: How do I set the gain with an op-amp?
    a: Use an inverting amplifier whose input resistor is the last R of the ladder, and a feedback resistor Rf ≥ 29R. Use slightly more (about 30–32R) for reliable start-up.
  - q: Why is the output not a perfect sine wave?
    a: Excess gain drives the amplifier into clipping. Amplitude stabilisation with diodes or a thermistor in the feedback path keeps distortion low.
related: [electronics/rc-filter, electronics/op-amp-gain, electronics/555-timer, electronics/crystal-load-capacitance]
''', f'''
## How to use the RC phase shift oscillator calculator

Enter the **resistance** and **capacitance** used in each of the three identical RC sections. The calculator returns the oscillation frequency and the minimum feedback resistor for an inverting op-amp stage. To design for a frequency, clear R or C and enter the frequency.

## RC phase shift oscillator formula

<p class="formula">f = 1 ÷ (2π R C √6) &nbsp;·&nbsp; |A| ≥ 29 → R<sub>f</sub> ≥ 29 R</p>

## Worked example

R = 10 kΩ, C = 10 nF in each section:

- f = 1 ÷ (2π × 10,000 × 10 × 10⁻⁹ × 2.449) = **{of:.1f} Hz**
- R<sub>f</sub> ≥ 29 × 10 kΩ = **290 kΩ** (use 300–330 kΩ)

## Frequency for common R and C values

| R | 1 nF | 10 nF | 100 nF | 1 µF |
|---|---|---|---|---|
{ro_rows}
## Notes

- The formula assumes the ladder is not loaded — drive it from a low impedance and let the last R go to the op-amp virtual ground.
- For a transistor version the √6 factor changes slightly with the loading of the transistor's input.
''')

# ======================================================================= ELECTRICAL

# ---------------------------------------------------------------- Ferranti effect
fVs, fl, fL, fC, ff = 400.0, 300.0, 1.0, 11.5, 50.0
fbeta = 2 * math.pi * ff * math.sqrt(fL * 1e-6 * fC * 1e-12)
fVr = fVs / math.cos(fbeta * fl * 1e3)
fe_rows = ''
for l in (50, 100, 200, 300, 400, 500, 800):
    r_ = 1 / math.cos(fbeta * l * 1e3)
    fe_rows += f"| {l} km | {r_:.4f} | {100*(r_-1):.2f}% | {fVs*r_:.1f} kV |\n"
P('electrical', 'ferranti-effect', f'''
title: Ferranti Effect Calculator (Receiving-End Voltage Rise)
description: Calculate the receiving-end voltage rise of a lightly loaded or open transmission line due to the Ferranti effect from line length, inductance and capacitance.
category: electrical
{intro("On a long, lightly loaded transmission line the charging current flowing through the line inductance makes the receiving-end voltage rise above the sending-end voltage. This Ferranti effect calculator uses the lossless-line equation Vr = Vs ÷ cos(βl) to find that rise — see the [Ferranti effect in transmission lines](ib:ferranti-effect-transmission-line).")}
keywords: [ferranti effect calculator, receiving end voltage rise, open circuit transmission line voltage, ferranti effect formula, long transmission line voltage, line charging voltage rise, shunt reactor sizing]
updated: {D}
variables:
  - {{ id: Vs, label: Sending-end voltage, family: voltage, unit: kV, default: {fVs:g}, min: 0 }}
  - {{ id: l, label: Line length, family: length, unit: km, imperialUnit: mi, default: {fl:g}, min: 0 }}
  - {{ id: L, label: Series inductance per km, suffix: mH/km, default: {fL:g}, min: 0 }}
  - {{ id: C, label: Shunt capacitance per km, suffix: nF/km, default: {fC:g}, min: 0 }}
  - {{ id: f, label: System frequency, family: frequency, unit: Hz, default: {ff:g}, min: 0 }}
  - {{ id: bl, label: Electrical length βl, family: angle, unit: deg, min: 0 }}
  - {{ id: Vr, label: Receiving-end voltage (no load), family: voltage, unit: kV, min: 0 }}
  - {{ id: rise, label: Voltage rise, family: percent, unit: '%', decimals: 2 }}
equations:
  - bl = 2 * pi * f * sqrt(L * 1e-6 * C * 1e-12) * l
  - Vr = Vs / cos(bl)
  - rise = Vr / Vs - 1
faq:
  - q: What is the Ferranti effect?
    a: The rise of receiving-end voltage above sending-end voltage on a long line at light load or no load. The line's shunt capacitance draws a leading charging current, and its flow through the series inductance raises the voltage along the line.
  - q: What is the Ferranti effect formula?
    a: For a lossless line on open circuit, Vr = Vs ÷ cos(βl), with β = ω√(LC). A useful approximation is Vr ≈ Vs × (1 + ω²LC·l² ÷ 2).
  - q: How big is the Ferranti rise?
    a: For a 50 Hz overhead line it is roughly 0.5% at 100 km, 5% at 300 km and about 15% at 500 km.
  - q: How is the Ferranti effect controlled?
    a: With shunt reactors at the line ends (switched in at light load), SVCs or STATCOMs, and by energising long lines from the stronger end.
related: [electrical/per-unit, electrical/cable-voltage-drop, electrical/capacitor-bank-kvar, electrical/skin-depth]
''', f'''
## How to use the Ferranti effect calculator

Enter the **sending-end voltage**, the **line length**, the line's **inductance and capacitance per km** and the **frequency**. The calculator returns the line's electrical length, the open-circuit receiving-end voltage and the percentage rise. Typical overhead-line values are about 1.0 mH/km and 11–12 nF/km; cables have much higher capacitance.

## Ferranti effect formula

<p class="formula">β = 2πf √(LC) &nbsp;·&nbsp; V<sub>r</sub> = V<sub>s</sub> ÷ cos(βl)</p>

## Worked example

A 400 kV, 300 km, 50 Hz overhead line with L = 1.0 mH/km and C = 11.5 nF/km, open at the far end:

- β = 2π × 50 × √(1.0×10⁻⁶ × 11.5×10⁻¹²) = {fbeta*1e3:.4e} rad/km
- βl = {fbeta*fl*1e3:.4f} rad ({fbeta*fl*1e3*180/math.pi:.2f}°)
- V<sub>r</sub> = 400 ÷ cos({fbeta*fl*1e3:.4f}) = **{fVr:.1f} kV** — a **{100*(fVr/fVs-1):.2f}%** rise

## Ferranti rise vs line length (400 kV, 1.0 mH/km, 11.5 nF/km, 50 Hz)

| Length | Vr ÷ Vs | Rise | Vr |
|---|---|---|---|
{fe_rows}
## Notes

- The lossless model slightly overstates the rise; line resistance and any load reduce it.
- Underground cables show the effect over much shorter distances because their capacitance is 20–50 times higher.
''')

# ---------------------------------------------------------------- Lumen method
lE, lLen, lW, lF, lUF, lMF = 500.0, 10.0, 8.0, 4000.0, 0.6, 0.8
lA = lLen * lW
lN = lE * lA / (lF * lUF * lMF); lNr = math.ceil(lN - 1e-9); lEa = lNr * lF * lUF * lMF / lA
lm_rows2 = ''
for name, E in [('Corridors, stores', 100), ('Warehouse', 200), ('Classroom', 300), ('Office, control room', 500), ('Workshop — fine work', 750), ('Inspection, drawing office', 1000)]:
    nn = E * lA / (lF * lUF * lMF)
    lm_rows2 += f"| {name} | {E} lux | {nn:.1f} | {math.ceil(nn - 1e-9)} |\n"
P('electrical', 'lumen-method', f'''
title: Lumen Method Calculator (Number of Light Fixtures & Lux)
description: Calculate how many light fixtures a room needs for a target lux level with the lumen method, N = E·A ÷ (Φ·UF·MF), and the illuminance actually achieved.
category: electrical
{intro("The lumen method is the standard hand calculation for general lighting: the lumens needed equal target illuminance × area, corrected for how much light reaches the work plane and for ageing and dirt. This lumen method calculator gives the number of fixtures and the resulting lux — the same steps as in this [lighting design calculation](ib:lighting-design-calculation).")}
keywords: [lumen method calculator, number of light fixtures calculator, lux calculator room, lighting calculation formula, how many lights do i need, lumens to lux room, utilization factor maintenance factor]
updated: {D}
variables:
  - {{ id: E, label: Required illuminance, suffix: lux, default: {lE:g}, min: 0 }}
  - {{ id: Lr, label: Room length, family: length, unit: m, imperialUnit: ft, default: {lLen:g}, min: 0 }}
  - {{ id: Wr, label: Room width, family: length, unit: m, imperialUnit: ft, default: {lW:g}, min: 0 }}
  - {{ id: F, label: Lumen output per fixture, suffix: lm, default: {lF:g}, min: 0 }}
  - {{ id: UF, label: Utilisation factor (UF), default: {lUF:g}, min: 0.01, max: 1, help: 'Fraction of lamp lumens reaching the work plane — 0.4–0.7 depending on room shape, reflectances and fitting.' }}
  - {{ id: MF, label: Maintenance factor (MF), default: {lMF:g}, min: 0.01, max: 1, help: 'Allowance for lumen depreciation and dirt — 0.7–0.9 for LED in clean rooms.' }}
  - {{ id: N, label: Number of fixtures (exact), min: 0 }}
  - {{ id: Nr, label: Number of fixtures (rounded up), min: 0 }}
  - {{ id: Ea, label: Illuminance with rounded-up fixtures, suffix: lux, min: 0 }}
equations:
  - N = E * Lr * Wr / (F * UF * MF)
  - Nr = ceil(N)
  - Ea = Nr * F * UF * MF / (Lr * Wr)
faq:
  - q: What is the lumen method formula?
    a: N = (E × A) ÷ (Φ × UF × MF), where E is the required illuminance in lux, A the area in m², Φ the lumens per fixture, UF the utilisation factor and MF the maintenance factor.
  - q: How many lux does an office need?
    a: EN 12464-1 recommends 500 lux on the task area for offices and control rooms, 300 lux for classrooms and 100–200 lux for corridors and warehouses.
  - q: What is the utilisation factor?
    a: The fraction of the lamps' light that reaches the working plane. It depends on the room index, surface reflectances and the fitting's light distribution and comes from the manufacturer's UF table.
  - q: How should I arrange the fixtures?
    a: In a regular grid with spacing no more than the fitting's maximum spacing-to-height ratio (often 1.0–1.5 × mounting height above the work plane), so the lighting is uniform.
related: [electrical/kw-to-amps, electrical/load-factor, electronics/led-resistor, physics/inverse-square-law]
''', f'''
## How to use the lumen method calculator

Enter the **target illuminance**, the **room length and width**, the **lumens per fixture** and the **utilisation and maintenance factors**. The calculator returns the exact number of fixtures, the number rounded up and the illuminance you will actually get.

## Lumen method formula

<p class="formula">N = E × A ÷ (Φ × UF × MF) &nbsp;·&nbsp; E<sub>achieved</sub> = N × Φ × UF × MF ÷ A</p>

## Worked example

An office 10 m × 8 m (80 m²) needs 500 lux, using 4,000 lm LED panels with UF = 0.6 and MF = 0.8:

- N = 500 × 80 ÷ (4,000 × 0.6 × 0.8) = 40,000 ÷ 1,920 = **{lN:.2f}** → **{lNr} fixtures**
- Achieved = {lNr} × 1,920 ÷ 80 = **{lEa:.0f} lux**

## Fixtures for an 80 m² room by application (4,000 lm, UF 0.6, MF 0.8)

| Application | Target | Exact N | Fixtures |
|---|---|---|---|
{lm_rows2}
## Notes

- In practice round to a number that fits a neat grid (for example 21 → 4 × 5 = 20 or 4 × 6 = 24) and recheck the lux.
- The lumen method gives the average illuminance; use lighting software to check uniformity and glare.
''')

# ---------------------------------------------------------------- Polarization index
pR30, pR1, pR10 = 800.0, 1000.0, 2500.0
pPI = pR10 / pR1; pDAR = pR1 / pR30
P('electrical', 'polarization-index', f'''
title: Polarization Index Calculator (PI & DAR Insulation Test)
description: Calculate the polarization index (PI = R10 min ÷ R1 min) and dielectric absorption ratio (DAR = R60 s ÷ R30 s) from megger readings, with IEEE 43 limits.
category: electrical
{intro("A healthy insulation's resistance keeps rising during a megger test as the dielectric polarizes, while moist or contaminated insulation levels off quickly. This polarization index calculator turns the 30-second, 1-minute and 10-minute readings into the PI and DAR — follow the [insulation resistance test with a megger](ib:insulation-resistance-test-megger) procedure and compare with [motor insulation classes](ib:motor-insulation-classes).")}
keywords: [polarization index calculator, pi test calculator, dielectric absorption ratio calculator, insulation resistance test, megger pi value, ieee 43 polarization index, motor insulation test]
updated: {D}
variables:
  - {{ id: R30, label: Insulation resistance at 30 s, family: resistance, unit: Mohm, default: {pR30:g}, min: 0 }}
  - {{ id: R1, label: Insulation resistance at 1 min, family: resistance, unit: Mohm, default: {pR1:g}, min: 0 }}
  - {{ id: R10, label: Insulation resistance at 10 min, family: resistance, unit: Mohm, default: {pR10:g}, min: 0 }}
  - id: PI
    label: Polarization index PI (R10 ÷ R1)
    min: 0
    decimals: 2
    bands:
      - {{ max: 1, label: Dangerous, color: '#dc2626' }}
      - {{ max: 2, label: Questionable, color: '#eab308' }}
      - {{ max: 4, label: Good, color: '#16a34a' }}
      - {{ max: 1e12, label: Very good, color: '#15803d' }}
  - id: DAR
    label: Dielectric absorption ratio DAR (R60s ÷ R30s)
    min: 0
    decimals: 2
    bands:
      - {{ max: 1, label: Poor, color: '#dc2626' }}
      - {{ max: 1.25, label: Questionable, color: '#eab308' }}
      - {{ max: 1.6, label: Good, color: '#16a34a' }}
      - {{ max: 1e12, label: Excellent, color: '#15803d' }}
equations:
  - PI = R10 / R1
  - DAR = R1 / R30
faq:
  - q: How is the polarization index calculated?
    a: PI = insulation resistance after 10 minutes ÷ insulation resistance after 1 minute, both at the same test voltage. 2,500 MΩ ÷ 1,000 MΩ gives a PI of 2.5.
  - q: What is a good polarization index?
    a: IEEE 43 recommends a minimum PI of 2.0 for class B, F and H insulation and 1.5 for class A. Below 1.0 the insulation is likely wet, dirty or damaged.
  - q: What is the dielectric absorption ratio?
    a: DAR = 60-second reading ÷ 30-second reading. It is a quicker test; above about 1.25 is acceptable and above 1.6 excellent.
  - q: When is the PI test not meaningful?
    a: If the 1-minute insulation resistance is above about 5,000 MΩ, IEEE 43 notes the PI may not be meaningful because the current is too small to measure reliably.
related: [electrical/three-phase-motor-power, electrical/earthing-resistance, electrical/wire-resistance, electrical/transformer-efficiency]
''', f'''
## How to use the polarization index calculator

Apply the test voltage with an insulation resistance tester and record the readings at **30 seconds**, **1 minute** and **10 minutes**. Enter them and the calculator returns the polarization index and the dielectric absorption ratio, each with a condition rating.

## Polarization index formulas

<p class="formula">PI = R<sub>10 min</sub> ÷ R<sub>1 min</sub> &nbsp;·&nbsp; DAR = R<sub>60 s</sub> ÷ R<sub>30 s</sub></p>

## Worked example

Motor winding readings at 1,000 V DC: 800 MΩ at 30 s, 1,000 MΩ at 1 min, 2,500 MΩ at 10 min:

- PI = 2,500 ÷ 1,000 = **{pPI:.2f}** — good (above the IEEE 43 minimum of 2.0)
- DAR = 1,000 ÷ 800 = **{pDAR:.2f}** — questionable on its own, which is why the 10-minute test is preferred

## Interpreting PI and DAR

| Condition | PI | DAR |
|---|---|---|
| Dangerous / poor | below 1.0 | below 1.0 |
| Questionable | 1.0 – 2.0 | 1.0 – 1.25 |
| Good | 2.0 – 4.0 | 1.25 – 1.6 |
| Very good | above 4.0 | above 1.6 |

## Notes

- Insulation resistance roughly halves for every 10 °C rise — correct readings to 40 °C before comparing with past tests; PI is a ratio and is less sensitive to temperature.
- Discharge the winding fully after the test, for at least four times the test duration.
''')

print('pages', len(DESC))
