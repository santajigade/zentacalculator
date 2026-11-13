"""Batch 2026-11-13 — 6 calculators: engineering (cooling tower range/approach/evaporation/blowdown,
compressed air leak cost, boiler efficiency by the direct method), chemistry (excess air from flue-gas O2),
electronics (RC snubber design), electrical (lightning protection rolling sphere).
All reference tables are computed here (steam enthalpies with the iapws package, IAPWS-IF97);
defaults match the worked examples."""
import sys, math, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro
from iapws import IAPWS97
D = '2026-11-13'
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

# ---------------------------------------------------------------- Cooling tower
def tower(Th, Tc, Twb, Q, coc, drift):
    R = Th - Tc; A = Tc - Twb; eff = R / (R + A)
    heat = 1000 * 4186 * Q / 3600 * R          # W, Q in m3/h
    E = 0.00153 * Q * R                        # m3/h  (= 0.00085 x Q x range in deg F)
    Dr = drift * Q
    B = E / (coc - 1) - Dr
    M = E + B + Dr
    return dict(R=R, A=A, eff=eff, heat=heat, TR=heat / 3516.8528, E=E, Dr=Dr, B=B, M=M)
cTh, cTc, cTw, cQ, cC, cD = 37.0, 32.0, 28.0, 500.0, 4.0, 0.0002
CT = tower(cTh, cTc, cTw, cQ, cC, cD)
ce_rows = ''
for R in (3, 4, 5, 6, 8, 10, 12):
    ce_rows += f"| {R} °C ({R*1.8:g} °F) | " + ' | '.join(f"{0.00153*Q*R:,.2f} m³/h" for Q in (100, 500, 1000, 5000)) + f" | {0.153*R:.2f}% |\n"
cc_rows = ''
for coc in (1.5, 2, 3, 4, 5, 6, 8, 10):
    r = tower(cTh, cTc, cTw, 1000, coc, 0)
    cc_rows += f"| {coc:g} | {r['E']:.2f} | {r['B']:.2f} | {r['M']:.2f} | {r['M']*24:,.0f} m³ |\n"

P('engineering', 'cooling-tower', f'''
title: Cooling Tower Calculator (Range, Approach, Evaporation)
description: Calculate cooling tower range, approach and efficiency, heat rejected in kW and tons, and the evaporation, blowdown and makeup water for a given flow.
category: engineering
{intro("A cooling tower rejects heat from condenser or process water by evaporating a small part of it into the air. This cooling tower calculator works out the range, approach and effectiveness from the hot water, cold water and wet bulb temperatures, the heat rejected in kW and refrigeration tons, and the evaporation, drift, blowdown and makeup water flows for the cycles of concentration you run.")}
keywords: [cooling tower calculator, cooling tower range and approach, cooling tower efficiency calculation, cooling tower evaporation loss, cooling tower makeup water calculation, cooling tower blowdown calculation, cycles of concentration calculator]
updated: {D}
variables:
  - {{ id: Th, label: Hot water temperature (tower inlet), family: temperature, unit: C, imperialUnit: F, default: {cTh:g} }}
  - {{ id: Tc, label: Cold water temperature (tower outlet), family: temperature, unit: C, imperialUnit: F, default: {cTc:g} }}
  - {{ id: Twb, label: Ambient wet bulb temperature, family: temperature, unit: C, imperialUnit: F, default: {cTw:g} }}
  - {{ id: Q, label: Circulating water flow, family: flow, unit: m3h, imperialUnit: gpm, default: {cQ:g}, min: 0 }}
  - {{ id: coc, label: Cycles of concentration, default: {cC:g}, min: 1.000001, help: 'Ratio of dissolved solids (or chloride, or conductivity) in the circulating water to that in the makeup water. Typically 3–7.' }}
  - {{ id: dr, label: Drift loss (% of circulating flow), family: percent, unit: '%', default: {cD*100:g}, min: 0, help: 'Modern drift eliminators: 0.001–0.005%. Older towers: 0.02–0.2%.' }}
  - {{ id: R, label: Range (hot − cold), family: tempdiff, unit: K, imperialUnit: F }}
  - {{ id: A, label: Approach (cold − wet bulb), family: tempdiff, unit: K, imperialUnit: F }}
  - {{ id: eff, label: Cooling tower effectiveness, family: percent, unit: '%' }}
  - {{ id: H, label: Heat rejected, family: power, unit: kW, imperialUnit: TR, min: 0 }}
  - {{ id: E, label: Evaporation loss, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: Dr, label: Drift loss, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: B, label: Blowdown, family: flow, unit: m3h, imperialUnit: gpm }}
  - {{ id: M, label: Makeup water, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
equations:
  - R = Th - Tc
  - A = Tc - Twb
  - eff = R / (R + A)
  - H = 1000 * 4186 * Q * R
  - E = 0.00153 * Q * R
  - Dr = dr * Q
  - B = E / (coc - 1) - Dr
  - M = E + B + Dr
faq:
  - q: What are range and approach in a cooling tower?
    a: The range is the drop in water temperature across the tower (hot water in minus cold water out); it is set by the heat load and the flow. The approach is how close the cold water gets to the ambient wet bulb temperature (cold water minus wet bulb); it depends on the tower size and fill. A tower cooling water from 37 °C to 32 °C at a 28 °C wet bulb has a 5 °C range and a 4 °C approach.
  - q: How do you calculate cooling tower efficiency?
    a: Effectiveness = range ÷ (range + approach) = (T_hot − T_cold) ÷ (T_hot − T_wet bulb). It is the fraction of the maximum possible cooling actually achieved — 5 ÷ (5 + 4) = 55.6% in the example. Typical towers run at 55–75%; the water can never be cooled below the wet bulb temperature.
  - q: How much water does a cooling tower evaporate?
    a: About 0.153% of the circulating flow for every 1 °C of range (the rule E = 0.00085 × flow × range in °F from Perry's handbook), so roughly 1% of the flow for every 6.5 °C (12 °F). A 500 m³/h tower with a 5 °C range evaporates about 3.8 m³/h. The rule assumes nearly all heat leaves as latent heat; the real figure is a little lower in cold weather.
  - q: How do you calculate blowdown and makeup water?
    a: Blowdown B = E ÷ (COC − 1) − drift, and makeup M = evaporation + blowdown + drift = E × COC ÷ (COC − 1). Raising the cycles of concentration from 2 to 5 cuts the makeup by over a third, but the water treatment must then cope with higher scaling and corrosion potential.
related: [engineering/chiller-tonnage, engineering/heat-duty, engineering/lmtd, engineering/dew-point, engineering/pump-power]
''', f'''
## How to use the cooling tower calculator

Enter the **hot water temperature** returning to the tower, the **cold water temperature** leaving the basin, the **ambient wet bulb temperature**, the **circulating water flow**, the **cycles of concentration** and the **drift loss**. The calculator gives the range, the approach, the tower effectiveness, the heat rejected (in kW or refrigeration tons) and the evaporation, drift, blowdown and makeup flows. Leave any one input blank to solve for it — for example enter the makeup you can afford and find the cycles of concentration you must reach.

## Cooling tower formulas

<p class="formula">Range = T<sub>hot</sub> − T<sub>cold</sub> &nbsp;·&nbsp; Approach = T<sub>cold</sub> − T<sub>wb</sub> &nbsp;·&nbsp; Effectiveness = Range ÷ (Range + Approach)</p>

<p class="formula">Heat rejected = ρ c<sub>p</sub> Q × Range &nbsp;·&nbsp; E = 0.00153 × Q × Range(°C) &nbsp;·&nbsp; B = E ÷ (COC − 1) − D &nbsp;·&nbsp; M = E + B + D</p>

Water is taken as 1,000 kg/m³ with c<sub>p</sub> = 4.186 kJ/kg·K. E is evaporation, D drift, B blowdown and M makeup, all in the same flow units as Q.

## Worked example

A {cQ:g} m³/h condenser water circuit returns at {cTh:g} °C and leaves the tower at {cTc:g} °C on a day with a {cTw:g} °C wet bulb; the tower runs at {cC:g} cycles with {cD*100:g}% drift:

- Range = {cTh:g} − {cTc:g} = **{CT['R']:g} °C**; approach = {cTc:g} − {cTw:g} = **{CT['A']:g} °C**
- Effectiveness = {CT['R']:g} ÷ ({CT['R']:g} + {CT['A']:g}) = **{CT['eff']*100:.1f}%**
- Heat rejected = 1,000 × 4.186 × {cQ:g} ÷ 3,600 × {CT['R']:g} = **{CT['heat']/1000:,.0f} kW** ({CT['TR']:,.0f} TR)
- Evaporation E = 0.00153 × {cQ:g} × {CT['R']:g} = **{CT['E']:.3f} m³/h**
- Drift D = {cD*100:g}% × {cQ:g} = **{CT['Dr']:.2f} m³/h**
- Blowdown B = {CT['E']:.3f} ÷ ({cC:g} − 1) − {CT['Dr']:.2f} = **{CT['B']:.3f} m³/h**
- Makeup M = {CT['E']:.3f} + {CT['B']:.3f} + {CT['Dr']:.2f} = **{CT['M']:.2f} m³/h** (about {CT['M']*24:.0f} m³ per day)

## Evaporation loss by range and flow

| Range | 100 m³/h | 500 m³/h | 1,000 m³/h | 5,000 m³/h | % of flow |
|---|---|---|---|---|---|
{ce_rows}
## Blowdown and makeup by cycles of concentration

Per 1,000 m³/h of circulating water with a {cTh-cTc:g} °C range (evaporation {0.00153*1000*5:.2f} m³/h), drift neglected:

| Cycles (COC) | Evaporation (m³/h) | Blowdown (m³/h) | Makeup (m³/h) | Makeup per day |
|---|---|---|---|---|
{cc_rows}
## Practical notes

- **Approach sets the tower size:** halving the approach roughly doubles the fill and air required, so designs rarely go below 3 °C (5 °F). A rising approach at the same load and wet bulb points to fouled fill, blocked nozzles or a fan problem.
- **Range follows the load:** for a fixed flow the range rises and falls with the heat load; the approach stays fairly constant.
- **Cycles of concentration** are usually measured as the ratio of conductivity or chloride in the basin to that in the makeup water. Gains above about 6–8 cycles are small, while scaling risk keeps rising.
- **Design wet bulb:** size the tower on the local summer design wet bulb (often the 1% or 0.4% value), not the dry bulb temperature. Use the [dew point calculator](/engineering/dew-point/) for humidity checks and the [chiller tonnage calculator](/engineering/chiller-tonnage/) to size the chiller the tower serves.
''')

# ---------------------------------------------------------------- Compressed air leak cost
G = 1.4; RA = 287.05; PA = 101325.0; RHO_REF = PA / (RA * 293.15)
CHOKE = (2 / (G + 1)) ** ((G + 1) / (2 * (G - 1)))
def leak(dmm, pg, TC, Cd, n, SP, H, price):
    A = pi / 4 * (dmm / 1000) ** 2
    P0 = pg + PA; T = TC + 273.15
    m = Cd * A * P0 * math.sqrt(G / (RA * T)) * CHOKE
    Qf = m / RHO_REF
    Pw = SP * 1000 * Qf * 60
    E = Pw * n * H / 1000
    return dict(A=A, m=m, Qf=Qf, Pw=Pw, E=E, cost=E * price)
lD, lP, lT, lCd, lN, lSP, lH, lPr = 3.0, 7e5, 20.0, 0.65, 1, 6.5, 8000, 8.0
LK = leak(lD, lP, lT, lCd, lN, lSP, lH, lPr)
lk_rows = ''
for dmm in (0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10):
    cells = []
    for pb in (4, 6, 7, 8, 10):
        r = leak(dmm, pb * 1e5, lT, lCd, 1, lSP, lH, lPr)
        cells.append(f"{r['Qf']*60000:,.0f}" if r['Qf'] * 60000 >= 100 else f"{r['Qf']*60000:,.1f}")
    lk_rows += f"| {dmm:g} mm ({dmm/25.4:.3f} in) | " + ' | '.join(cells) + " |\n"
lc_rows = ''
for dmm in (1, 2, 3, 5, 6, 10):
    r = leak(dmm, lP, lT, lCd, 1, lSP, lH, lPr)
    lc_rows += f"| {dmm:g} mm | {r['Qf']*60000:,.0f} L/min ({r['Qf']/0.028316846592*60:,.1f} cfm) | {r['Pw']/1000:,.2f} kW | {r['E']:,.0f} kWh | {r['cost']:,.0f} |\n"
# check against the US DOE table: 1/16 in hole at 100 psig, Cd = 1 -> about 6.5 cfm
_doe = leak(1.5875, 689476, 20, 1.0, 1, 1, 1, 1)['Qf'] / 0.028316846592 * 60
assert abs(_doe - 6.49) < 0.1, _doe

P('engineering', 'compressed-air-leak', f'''
title: Compressed Air Leak Calculator (Flow, kW & Cost)
description: Calculate the air flow lost through a compressed air leak from hole size and pressure, the compressor power it wastes and the yearly energy and cost.
category: engineering
{intro("Leaks are the biggest single waste in most compressed air systems — a typical plant loses 20–30% of its compressor output through fittings, hoses, drains and worn seals. This compressed air leak calculator estimates the free-air flow through a leak from the hole diameter and line pressure using choked-flow equations, then converts it into the compressor power it wastes and the energy and money lost per year — the numbers you need to justify a leak survey or a repair.")}
keywords: [compressed air leak calculator, compressed air leak cost, air leak flow rate calculation, cost of compressed air leaks, compressed air leak cfm, air leakage calculation formula, leak hole size flow calculator]
updated: {D}
variables:
  - {{ id: d, label: Leak hole diameter (equivalent), family: length, unit: mm, imperialUnit: in, default: {lD:g}, min: 0 }}
  - {{ id: p, label: Line pressure (gauge), family: pressure, unit: bar, imperialUnit: psi, default: {lP/1e5:g}, min: 0, help: 'The formula assumes choked flow, valid above about 0.9 bar g (13 psig).' }}
  - {{ id: T, label: Air temperature in the line, family: temperature, unit: C, imperialUnit: F, default: {lT:g} }}
  - {{ id: Cd, label: Discharge coefficient, default: {lCd:g}, min: 0, max: 1, help: '1.0 for a smooth rounded hole, about 0.61 for a sharp-edged hole. 0.65 is a common value for real leaks.' }}
  - {{ id: n, label: Number of similar leaks, default: {lN:g}, min: 0 }}
  - {{ id: SP, label: Compressor specific power, suffix: kW per m³/min, default: {lSP:g}, min: 0, help: 'Electrical input per m³/min of free air delivered. About 6–7 for a loaded screw compressor at 7 bar; higher for part-load or older machines.' }}
  - {{ id: H, label: Hours the system is pressurised per year, suffix: h/year, default: {lH:g}, min: 0 }}
  - {{ id: price, label: Electricity price per kWh, family: currency, default: {lPr:g}, min: 0, decimals: 2 }}
  - {{ id: Ah, label: Leak hole area, family: area, unit: mm2, imperialUnit: in2, min: 0 }}
  - {{ id: m, label: Mass flow through each leak, family: massflow, unit: kgh, imperialUnit: lbh, min: 0 }}
  - {{ id: Qf, label: Free air lost per leak, family: flow, unit: Lmin, imperialUnit: cfm, min: 0 }}
  - {{ id: Pw, label: Compressor power wasted per leak, family: power, unit: kW, imperialUnit: hp, min: 0 }}
  - {{ id: E, label: Energy wasted per year (all leaks), family: energy, unit: kWh, min: 0 }}
  - {{ id: cost, label: Cost of the leaks per year, family: currency, min: 0, decimals: 0 }}
equations:
  - Ah = pi / 4 * d^2
  - m = Cd * Ah * (p + 101325) * sqrt(1.4 / (287.05 * T)) * 0.578704
  - Qf = m / 1.20412
  - Pw = SP * 1000 * Qf * 60
  - E = Pw * n * H * 3600
  - cost = E / 3600000 * price
faq:
  - q: How much air does a compressed air leak waste?
    a: A 3 mm hole at 7 bar g loses about {LK['Qf']*60000:,.0f} litres of free air per minute ({LK['Qf']/0.028316846592*60:.1f} cfm) with a discharge coefficient of 0.65. The flow rises with the square of the hole diameter and roughly in proportion to the absolute pressure, so a 6 mm hole wastes four times as much.
  - q: How is the flow through a leak calculated?
    a: Above about 0.9 bar g the air reaches sonic speed in the hole (choked flow), so the mass flow is ṁ = C_d A P₀ √(γ ÷ (R T)) × (2 ÷ (γ + 1))^((γ+1)/(2(γ−1))), with P₀ the absolute line pressure, γ = 1.4 and R = 287 J/kg·K for air. Dividing by the density of free air (1.204 kg/m³ at 20 °C and 1.013 bar) gives the free air delivery the compressor must make up.
  - q: How much does a compressed air leak cost?
    a: Multiply the free air lost by the compressor's specific power to get the kW wasted, then by the operating hours and the electricity price. A 3 mm leak at 7 bar wastes about {LK['Pw']/1000:.1f} kW — around {LK['E']:,.0f} kWh in 8,000 hours, or {LK['cost']:,.0f} a year at a price of 8 per kWh.
  - q: How do you measure the total leakage in a plant?
    a: With all air-using equipment off, run the compressor and time its load and unload cycles — leakage (%) = load time ÷ (load + unload time) × 100. Alternatively, isolate a receiver of known volume and time the pressure decay. Ultrasonic leak detectors then locate the individual leaks.
related: [engineering/compressor-power, engineering/air-receiver-size, engineering/orifice-flow, engineering/gas-flow-correction, electrical/load-factor]
''', f'''
## How to use the compressed air leak calculator

Enter the **equivalent hole diameter** of the leak, the **line pressure**, the **air temperature** and a **discharge coefficient**, then the **number of similar leaks**, your compressor's **specific power**, the **hours per year** the system is pressurised and the **electricity price**. The calculator gives the mass flow and free air lost per leak, the compressor power wasted, and the yearly energy and cost for all the leaks. The price field takes any currency — enter ₹ per kWh, $ per kWh or € per kWh and the cost comes out in the same currency.

## Compressed air leak formula

<p class="formula">ṁ = C<sub>d</sub> A P<sub>0</sub> √(γ ÷ (R T)) × (2 ÷ (γ + 1))<sup>(γ+1)/(2(γ−1))</sup> = 0.5787 C<sub>d</sub> A P<sub>0</sub> √(1.4 ÷ (287.05 T))</p>

<p class="formula">Q<sub>free air</sub> = ṁ ÷ 1.204 kg/m³ &nbsp;·&nbsp; P<sub>wasted</sub> = specific power × Q &nbsp;·&nbsp; cost = P × n × hours × price</p>

P<sub>0</sub> is the absolute line pressure (gauge + 1.01325 bar), T the absolute air temperature and A the hole area. Free air is referred to 20 °C and 1.01325 bar. The equation applies to choked (sonic) flow, which holds for any line pressure above about 0.9 bar g. With C<sub>d</sub> = 1 it reproduces the US Department of Energy leak table (a 1/16 in hole at 100 psig loses 6.5 cfm).

## Worked example

One {lD:g} mm leak on a {lP/1e5:g} bar g line at {lT:g} °C, C<sub>d</sub> = {lCd:g}, compressor specific power {lSP:g} kW per m³/min, {lH:,} hours a year, electricity at {lPr:g} per kWh:

- Hole area A = π ÷ 4 × {lD:g}² = **{LK['A']*1e6:.3f} mm²**
- Absolute pressure P<sub>0</sub> = {lP/1e5:g} + 1.01325 = {(lP+PA)/1e5:.5f} bar; T = {lT+273.15:.2f} K
- Mass flow ṁ = 0.5787 × {lCd:g} × {LK['A']*1e6:.4f} × 10⁻⁶ × {lP+PA:,.0f} × √(1.4 ÷ (287.05 × {lT+273.15:.2f})) = **{LK['m']*3600:.2f} kg/h**
- Free air lost = {LK['m']:.5f} ÷ 1.20412 = **{LK['Qf']*60000:,.0f} L/min** ({LK['Qf']*60:.3f} m³/min, {LK['Qf']/0.028316846592*60:.1f} cfm)
- Power wasted = {lSP:g} × {LK['Qf']*60:.4f} = **{LK['Pw']/1000:.2f} kW**
- Energy per year = {LK['Pw']/1000:.3f} × {lH:,} = **{LK['E']:,.0f} kWh**, costing **{LK['cost']:,.0f}** a year

## Air lost through a leak by hole size and pressure

Free air lost in L/min per leak, C<sub>d</sub> = {lCd:g}, air at {lT:g} °C (multiply by 0.0353 for cfm):

| Hole diameter | 4 bar g | 6 bar g | 7 bar g | 8 bar g | 10 bar g |
|---|---|---|---|---|---|
{lk_rows}
## Yearly cost of a single leak at 7 bar g

{lSP:g} kW per m³/min, {lH:,} hours a year, {lPr:g} per kWh (scale the cost column for your own tariff):

| Hole | Air lost | Power wasted | Energy per year | Cost per year |
|---|---|---|---|---|
{lc_rows}
## Practical notes

- **Lower the pressure:** every 1 bar reduction in header pressure cuts leakage by roughly 1/8 at 7 bar and saves about 6–7% of compressor energy as well.
- **Where leaks hide:** quick couplings, hose connections, filter–regulator–lubricator units, condensate drains stuck open, pipe joints and cylinder rod seals account for most of the losses.
- **Leak tags:** a survey with an ultrasonic detector, tagging each leak and estimating its size, then using a table like the one above to rank repairs, usually pays back in weeks.
- **Part-load compressors** use more energy per m³ than the full-load specific power, so the true saving from fixing leaks can be higher. Use the [compressor power calculator](/engineering/compressor-power/) to estimate the specific power from the pressure ratio and the [air receiver size calculator](/engineering/air-receiver-size/) for pressure-decay leak tests.
''')

# ---------------------------------------------------------------- Boiler efficiency (direct method)
def boiler(ms, hs, Tfw, mf, gcv):
    hfw = 4.19 * Tfw
    Qs = ms / 3600 * (hs - hfw)      # kW, ms in kg/h, h in kJ/kg
    Qf = mf / 3600 * gcv
    return dict(hfw=hfw, Qs=Qs, Qf=Qf, eta=Qs / Qf, er=ms / mf)
bms, bhs, bTf, bmf, bgcv = 10000.0, 2781.0, 85.0, 700.0, 42700.0
BO = boiler(bms, bhs, bTf, bmf, bgcv)
hs_rows = ''
for pg in (3, 5, 7, 10, 12, 15, 17.5, 20, 25, 30):
    s = IAPWS97(P=(pg + 1.01325) / 10, x=1)
    hs_rows += f"| {pg:g} bar g ({pg*14.5038:,.0f} psig) | {s.T-273.15:.1f} °C | {s.h:,.1f} kJ/kg ({s.h/2.326:,.0f} Btu/lb) | {s.h/4.1868:,.1f} kcal/kg |\n"
s10 = IAPWS97(P=(10 + 1.01325) / 10, x=1)
assert abs(s10.h - bhs) < 1, s10.h
sup_rows = ''
for pg, T in ((10, 250), (10, 300), (20, 300), (40, 400), (65, 480), (100, 540)):
    s = IAPWS97(P=(pg + 1.01325) / 10, T=T + 273.15)
    sup_rows += f"| {pg:g} bar g, {T} °C | {s.h:,.1f} kJ/kg |\n"
fw_rows = ''
for T in (30, 60, 85, 105, 120, 150):
    w = IAPWS97(P=1.5 if T < 110 else 2.0 if T < 140 else 5.0, T=T + 273.15)
    fw_rows += f"| {T} °C | {w.h:,.1f} kJ/kg | {4.19*T:,.1f} kJ/kg |\n"
eff_rows = ''
for gcv_nm, gcv in (('Natural gas (about 52,000)', 52000), ('Furnace oil / LSHS (about 42,700)', 42700), ('Diesel (about 45,500)', 45500), ('Bituminous coal (about 25,000)', 25000), ('Indian coal (about 16,700)', 16700), ('Rice husk / wood (about 14,000)', 14000)):
    eff_rows += f"| {gcv_nm} | " + ' | '.join(f"{bms*(bhs-4.19*bTf)/(eta*gcv):,.0f} kg/h" for eta in (0.70, 0.80, 0.85, 0.90)) + " |\n"

P('engineering', 'boiler-efficiency', f'''
title: Boiler Efficiency Calculator (Direct Method)
description: Calculate boiler efficiency by the direct method from steam flow, steam and feedwater enthalpy, fuel flow and GCV, with the evaporation ratio and heat output.
category: engineering
{intro("The direct method (input–output method) measures boiler efficiency as the useful heat carried away by the steam divided by the heat released by the fuel. This boiler efficiency calculator uses the steam flow, the steam enthalpy, the feedwater temperature, the fuel consumption and its gross calorific value to give the efficiency, the heat output in kW, the fuel heat input and the evaporation ratio — and solves backwards for the fuel a boiler will need at a given efficiency.")}
keywords: [boiler efficiency calculator, boiler efficiency direct method, boiler efficiency formula, evaporation ratio calculator, boiler fuel consumption calculation, steam boiler efficiency calculation, input output method boiler efficiency]
updated: {D}
variables:
  - {{ id: ms, label: Steam generation rate, family: massflow, unit: kgh, imperialUnit: lbh, default: {bms:g}, min: 0 }}
  - {{ id: hs, label: Enthalpy of the steam, suffix: kJ/kg, default: {bhs:g}, min: 0, help: 'From steam tables at the boiler outlet pressure (and temperature if superheated). Saturated steam at 10 bar g is about 2,781 kJ/kg.' }}
  - {{ id: Tfw, label: Feedwater temperature, family: temperature, unit: C, imperialUnit: F, default: {bTf:g} }}
  - {{ id: mf, label: Fuel consumption, family: massflow, unit: kgh, imperialUnit: lbh, default: {bmf:g}, min: 0, help: 'For gas, convert the volume flow to kg/h with the gas density, or enter the GCV per Nm³ and the flow in Nm³/h as if it were kg/h.' }}
  - {{ id: gcv, label: Gross calorific value of the fuel (GCV), suffix: kJ/kg, default: {bgcv:g}, min: 0, help: '1 kcal/kg = 4.1868 kJ/kg. Furnace oil about 10,200 kcal/kg (42,700 kJ/kg).' }}
  - {{ id: hfw, label: Feedwater enthalpy (≈ 4.19 × T in °C), suffix: kJ/kg, decimals: 1 }}
  - {{ id: Qs, label: Heat output to the steam, family: power, unit: kW, imperialUnit: BTUh, min: 0 }}
  - {{ id: Qf, label: Heat input from the fuel, family: power, unit: kW, imperialUnit: BTUh, min: 0 }}
  - {{ id: eta, label: Boiler efficiency (GCV basis), family: percent, unit: '%' }}
  - {{ id: er, label: Evaporation ratio (kg steam per kg fuel), min: 0, decimals: 2 }}
equations:
  - hfw = 4.19 * (Tfw - 273.15)
  - Qs = ms * (hs - hfw) * 1000
  - Qf = mf * gcv * 1000
  - eta = Qs / Qf
  - er = ms / mf
faq:
  - q: What is the formula for boiler efficiency by the direct method?
    a: Efficiency = steam flow × (steam enthalpy − feedwater enthalpy) ÷ (fuel flow × GCV) × 100. For 10,000 kg/h of 10 bar g saturated steam (2,781 kJ/kg) from 85 °C feedwater (356 kJ/kg), burning 700 kg/h of furnace oil at 42,700 kJ/kg, η = 10,000 × 2,425 ÷ (700 × 42,700) = {BO['eta']*100:.1f}%.
  - q: What is the difference between the direct and indirect methods?
    a: The direct method compares the heat in the steam with the heat in the fuel, so it needs accurate steam and fuel flow measurements but gives no detail about where heat is lost. The indirect (heat loss) method of BS 845 and ASME PTC 4 subtracts the individual losses — dry flue gas, moisture, unburnt fuel, radiation and blowdown — from 100%, which shows what to fix. Both should agree within a couple of percent.
  - q: What is a good boiler efficiency?
    a: On a GCV basis, well-run gas-fired boilers reach about 80–85% (over 90% when condensing), oil-fired 80–85%, and coal and biomass boilers 70–80%. Efficiencies quoted on the net (NCV) basis are higher by roughly 5% for oil and 10% for natural gas, so always check which basis is used.
  - q: What is the evaporation ratio of a boiler?
    a: The evaporation ratio is the kilograms of steam generated per kilogram of fuel burnt. It is a quick daily check of performance — around 13–14 for furnace oil and 4–6 for Indian coal — but it depends on the steam pressure and feedwater temperature, so compare it only at similar operating conditions.
related: [engineering/heat-duty, chemistry/excess-air, engineering/pipe-heat-loss, engineering/tank-heater-sizing, engineering/mass-flow-rate]
''', f'''
## How to use the boiler efficiency calculator

Enter the **steam generation rate**, the **enthalpy of the steam** from steam tables (see the table below), the **feedwater temperature**, the **fuel consumption** over the same period and the fuel's **gross calorific value**. The calculator gives the feedwater enthalpy, the heat output to the steam, the fuel heat input, the **boiler efficiency** and the **evaporation ratio**. To estimate fuel consumption, enter the expected efficiency and leave the fuel flow blank.

## Boiler efficiency formula (direct method)

<p class="formula">η = Q<sub>steam</sub> ÷ Q<sub>fuel</sub> = m<sub>s</sub> (h<sub>s</sub> − h<sub>fw</sub>) ÷ (m<sub>f</sub> × GCV) &nbsp;·&nbsp; evaporation ratio = m<sub>s</sub> ÷ m<sub>f</sub></p>

The feedwater enthalpy is taken as h<sub>fw</sub> ≈ 4.19 × T (kJ/kg, T in °C), which is within 1% of the steam tables up to 150 °C. Measure steam and fuel over at least an hour of steady load; blowdown water and steam used inside the plant (for oil heating or atomising) are not counted as output.

## Worked example

A boiler generates {bms:,.0f} kg/h of saturated steam at 10 bar g ({bhs:,.0f} kJ/kg) from {bTf:g} °C feedwater, burning {bmf:g} kg/h of furnace oil with a GCV of {bgcv:,.0f} kJ/kg ({bgcv/4.1868:,.0f} kcal/kg):

- Feedwater enthalpy h<sub>fw</sub> = 4.19 × {bTf:g} = **{BO['hfw']:.2f} kJ/kg**
- Heat output = {bms:,.0f} ÷ 3,600 × ({bhs:,.0f} − {BO['hfw']:.2f}) = **{BO['Qs']:,.0f} kW**
- Heat input = {bmf:g} ÷ 3,600 × {bgcv:,.0f} = **{BO['Qf']:,.0f} kW**
- Efficiency η = {BO['Qs']:,.1f} ÷ {BO['Qf']:,.1f} = **{BO['eta']*100:.2f}%**
- Evaporation ratio = {bms:,.0f} ÷ {bmf:g} = **{BO['er']:.2f} kg of steam per kg of oil**

## Enthalpy of saturated steam

Computed from the IAPWS-IF97 steam tables (gauge pressure on 1.01325 bar atmosphere):

| Pressure | Saturation temperature | Enthalpy h<sub>g</sub> | Enthalpy (kcal/kg) |
|---|---|---|---|
{hs_rows}
For superheated steam use the enthalpy at the actual outlet temperature:

| Steam conditions | Enthalpy |
|---|---|
{sup_rows}
## Feedwater enthalpy: steam tables vs the 4.19 × T approximation

| Feedwater temperature | Steam tables | 4.19 × T |
|---|---|---|
{fw_rows}
## Fuel needed for the example boiler at different efficiencies

{bms:,.0f} kg/h of 10 bar g saturated steam from {bTf:g} °C feedwater ({BO['Qs']:,.0f} kW output). GCV in kJ/kg:

| Fuel | 70% | 80% | 85% | 90% |
|---|---|---|---|---|
{eff_rows}
## Practical notes

- **Excess air** is the biggest controllable loss: too much air carries heat up the stack, too little leaves unburnt fuel. Check it from the flue gas oxygen with the [excess air calculator](/chemistry/excess-air/).
- **Feedwater temperature:** every 6 °C rise in feedwater temperature (from an economiser or condensate return) saves roughly 1% of fuel.
- **Wet steam:** if the steam has a dryness fraction x below 1, use h = h<sub>f</sub> + x h<sub>fg</sub>; ignoring carry-over overstates the efficiency.
- **GCV or NCV:** Indian (BEE) practice and most boiler tests use the gross value; European boiler ratings often use the net value and can exceed 100% for condensing boilers.
- For the heat needed by a process stream, use the [heat duty calculator](/engineering/heat-duty/); for distribution losses after the boiler, use the [pipe heat loss calculator](/engineering/pipe-heat-loss/).
''')

# ======================================================================= CHEMISTRY

# ---------------------------------------------------------------- Excess air from flue gas O2
def xair(O2, CO2max, afr, mf):
    EA = O2 / (20.9 - O2); lam = 1 + EA
    return dict(EA=EA, lam=lam, CO2=CO2max * (20.9 - O2) / 20.9, ma=mf * afr * lam, ms=mf * afr)
xO2, xC, xA, xm = 3.0, 11.7, 17.2, 100.0
XA = xair(xO2, xC, xA, xm)
FUELS = (('Natural gas', 11.7, 17.2), ('Propane (LPG)', 13.7, 15.7), ('Light fuel oil / diesel', 15.4, 14.5), ('Heavy fuel oil', 15.8, 13.8), ('Bituminous coal', 18.5, 10.5), ('Wood (dry)', 20.3, 6.0))
xo_rows = ''
for o in (0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12):
    x = xair(o, 11.7, 17.2, 1)
    xo_rows += f"| {o:g}% | {x['EA']*100:.1f}% | {x['lam']:.3f} | " + ' | '.join(f"{c*(20.9-o)/20.9:.1f}%" for c in (11.7, 15.4, 18.5)) + " |\n"
xf_rows = ''.join(f"| {nm} | {c:g}% | {a:g} | {c*(20.9-3)/20.9:.1f}% | {a*xair(3,c,a,1)['lam']:.2f} |\n" for nm, c, a in FUELS)

P('chemistry', 'excess-air', f'''
title: Excess Air Calculator (Flue Gas O₂ to Excess Air)
description: Calculate excess combustion air and the air ratio (lambda) from the oxygen in dry flue gas, estimate CO₂ and the actual air flow for natural gas, oil or coal.
category: chemistry
{intro("Burners need some air beyond the stoichiometric amount to burn fuel completely, but every extra kilogram of air heats up and leaves through the stack. This excess air calculator converts the oxygen measured in dry flue gas — usually by a [zirconia oxygen analyzer](ib:zirconia-oxygen-analyzer-working-principle) in the flue — into percent excess air and the air ratio λ, and estimates the CO₂ in the flue gas and the combustion air flow for the fuel you burn.")}
keywords: [excess air calculator, flue gas o2 to excess air, excess air formula, combustion air calculation, lambda air ratio calculator, excess oxygen to excess air, combustion efficiency excess air]
updated: {D}
variables:
  - {{ id: O2, label: Oxygen in dry flue gas, family: percent, unit: '%', default: {xO2:g}, min: 0, max: 0.2089, help: 'By volume, dry basis (as read by an extractive analyser or a portable combustion analyser).' }}
  - id: CO2max
    label: Fuel (maximum CO₂ at zero excess air)
    default: {xC:g}
    options:
{''.join(f"      - {{ label: '{nm} (CO₂ max {c:g}%)', value: {c:g} }}" + chr(10) for nm, c, a in FUELS)}  - {{ id: afr, label: Stoichiometric air–fuel ratio, suffix: kg air/kg fuel, default: {xA:g}, min: 0, help: 'Natural gas about 17.2, propane 15.7, diesel 14.5, heavy oil 13.8, coal 9–11, dry wood about 6.' }}
  - {{ id: mf, label: Fuel flow, family: massflow, unit: kgh, imperialUnit: lbh, default: {xm:g}, min: 0 }}
  - {{ id: EA, label: Excess air, family: percent, unit: '%', min: 0 }}
  - {{ id: lam, label: Air ratio λ (actual ÷ stoichiometric air), min: 0, decimals: 3 }}
  - {{ id: CO2, label: Estimated CO₂ in dry flue gas, family: percent, unit: '%', min: 0 }}
  - {{ id: ma0, label: Stoichiometric air flow, family: massflow, unit: kgh, imperialUnit: lbh, min: 0 }}
  - {{ id: ma, label: Actual combustion air flow, family: massflow, unit: kgh, imperialUnit: lbh, min: 0 }}
equations:
  - EA = O2 / (0.209 - O2)
  - lam = 1 + EA
  - CO2 = CO2max / 100 * (0.209 - O2) / 0.209
  - ma0 = mf * afr
  - ma = ma0 * lam
faq:
  - q: How do you calculate excess air from O₂?
    a: Excess air (%) = O₂ ÷ (20.9 − O₂) × 100, with O₂ the percent oxygen in the dry flue gas and 20.9% the oxygen in air. 3% O₂ gives 3 ÷ 17.9 = 16.8% excess air, so the burner is supplied with 1.168 times the stoichiometric air.
  - q: What is a good excess air level?
    a: Typical targets are 10–20% excess air (about 2–3.5% O₂) for natural gas, 15–25% (3–4% O₂) for oil and 20–40% (3.5–6% O₂) for coal and biomass. Lower is more efficient as long as carbon monoxide stays low — trim the air until CO starts to rise, then back off a little.
  - q: How do you estimate CO₂ from O₂ in flue gas?
    a: CO₂ = CO₂max × (20.9 − O₂) ÷ 20.9, where CO₂max is the CO₂ the fuel produces with exactly stoichiometric air (about 11.7% for natural gas, 15.4% for light oil, 18.5% for bituminous coal). The relation holds for complete combustion on a dry basis.
  - q: Why is the formula only approximate?
    a: It assumes complete combustion on a dry basis and that the extra air simply dilutes the flue gas. The exact excess air depends a little on the fuel's hydrogen, carbon and nitrogen content, and any CO in the flue gas or air leaking into the duct ahead of the analyser makes the reading unrepresentative. For most boilers and furnaces the simple formula is within a few percent of excess air.
related: [engineering/boiler-efficiency, chemistry/enthalpy-of-reaction, chemistry/bomb-calorimeter, chemistry/gas-density, engineering/mass-flow-rate]
''', f'''
## How to use the excess air calculator

Enter the **oxygen in the dry flue gas**, pick the **fuel** (it sets the maximum CO₂), enter its **stoichiometric air–fuel ratio** and the **fuel flow**. The calculator gives the percent **excess air**, the **air ratio λ**, the expected **CO₂** in the flue gas and the stoichiometric and actual **combustion air flows**. To find the O₂ setpoint for a target excess air, enter the excess air and leave the O₂ blank.

## Excess air formula

<p class="formula">Excess air = O<sub>2</sub> ÷ (20.9 − O<sub>2</sub>) &nbsp;·&nbsp; λ = 20.9 ÷ (20.9 − O<sub>2</sub>) &nbsp;·&nbsp; CO<sub>2</sub> = CO<sub>2,max</sub> × (20.9 − O<sub>2</sub>) ÷ 20.9</p>

<p class="formula">Actual air = fuel flow × stoichiometric air–fuel ratio × λ</p>

O<sub>2</sub> and CO<sub>2</sub> are percentages by volume on a dry basis. An in-situ zirconia probe measures on a wet basis and reads about 10–20% lower than a dry analyser on gas-fired plant, so convert the reading or use the dry value from a portable analyser.

## Worked example

A natural gas boiler burns {xm:g} kg/h of gas (stoichiometric air–fuel ratio {xA:g}) and the analyser reads {xO2:g}% O₂ in the dry flue gas:

- Excess air = {xO2:g} ÷ (20.9 − {xO2:g}) = {xO2:g} ÷ {20.9-xO2:.1f} = **{XA['EA']*100:.2f}%**
- Air ratio λ = 1 + {XA['EA']:.4f} = **{XA['lam']:.4f}**
- Expected CO₂ = {xC:g} × ({20.9-xO2:.1f} ÷ 20.9) = **{XA['CO2']:.2f}%**
- Stoichiometric air = {xm:g} × {xA:g} = **{XA['ms']:,.0f} kg/h**; actual air = {XA['ms']:,.0f} × {XA['lam']:.4f} = **{XA['ma']:,.0f} kg/h**

## Flue gas O₂ to excess air and CO₂

| O₂ (dry) | Excess air | λ | CO₂, natural gas | CO₂, light oil | CO₂, coal |
|---|---|---|---|---|---|
{xo_rows}
## Typical fuel data

At 3% O₂ in the dry flue gas:

| Fuel | CO₂ max | Stoichiometric air (kg/kg) | CO₂ at 3% O₂ | Actual air at 3% O₂ (kg/kg fuel) |
|---|---|---|---|---|
{xf_rows}
Values are typical; the exact figures depend on the fuel analysis.

## Practical notes

- **Why it matters:** cutting excess air on a gas boiler from 50% to 15% typically improves efficiency by 1.5–2.5 percentage points, because less air is heated to stack temperature.
- **Air in-leakage:** air leaking into the furnace or duct upstream of the analyser makes the O₂ read high; compare readings at the furnace exit and the stack to find leaks.
- **O₂ trim:** many burners use a flue gas oxygen analyser to trim the air damper automatically, holding O₂ on a setpoint that varies with firing rate — see how [paramagnetic oxygen analyzers](ib:paramagnetic-oxygen-analyzer-working) and zirconia probes compare.
- To see what the air setting means for fuel use, combine the result with the [boiler efficiency calculator](/engineering/boiler-efficiency/); to convert gas volumes and densities, use the [gas density calculator](/chemistry/gas-density/).
''')

# ======================================================================= ELECTRONICS

# ---------------------------------------------------------------- RC snubber
def snub(f0, f1, Cadd, k, V, fsw):
    x = (f0 / f1) ** 2
    Cp = Cadd / (x - 1)
    Lp = 1 / ((2 * pi * f0) ** 2 * Cp)
    Z = math.sqrt(Lp / Cp)
    Cs = k * Cp
    return dict(x=x, Cp=Cp, Lp=Lp, Z=Z, Cs=Cs, Ps=Cs * V ** 2 * fsw, tau=Z * Cs)
sf0, sf1, sCa, sk, sV, sfs = 80e6, 40e6, 220e-12, 4.0, 48.0, 200e3
SN = snub(sf0, sf1, sCa, sk, sV, sfs)
sr_rows = ''
for r in (1.2, 1.5, 2.0, 2.5, 3.0):
    sr_rows += f"| {r:g} | {1/(r*r-1):.3f} × C<sub>add</sub> | " + ' | '.join(f"{1/(r*r-1)*ca*1e12:.0f} pF" for ca in (100e-12, 220e-12, 470e-12, 1e-9)) + " |\n"
sp_rows = ''
for V in (12, 24, 48, 100, 400):
    sp_rows += f"| {V} V | " + ' | '.join(f"{c*V*V*fs*1000:,.1f} mW" if c*V*V*fs < 1 else f"{c*V*V*fs:,.2f} W" for c, fs in ((100e-12, 100e3), (470e-12, 100e3), (1e-9, 100e3), (1e-9, 500e3), (4.7e-9, 100e3))) + " |\n"

P('electronics', 'rc-snubber', f'''
title: RC Snubber Calculator (Ringing Frequency Method)
description: Design an RC snubber from the measured ringing frequency: find parasitic capacitance and inductance, snubber resistor and capacitor values and resistor power.
category: electronics
{intro("Fast switching edges in MOSFET, diode and transformer circuits excite the stray inductance and capacitance of the layout into high-frequency ringing that raises voltage stress and EMI. This RC snubber calculator uses the proven measure-and-add-capacitance method: from the ringing frequency before and after adding a known test capacitor it finds the parasitic capacitance and inductance, the characteristic impedance, and a resistor and capacitor that damp the ringing — plus the power the snubber resistor must dissipate. The design steps follow this guide to [RC snubber circuit design](ib:snubber-circuit-rc-design).")}
keywords: [rc snubber calculator, snubber circuit design, snubber capacitor calculation, snubber resistor calculation, mosfet snubber design, rc snubber formula, ringing frequency snubber]
updated: {D}
variables:
  - {{ id: f0, label: Ringing frequency (as measured), family: frequency, unit: MHz, default: {sf0/1e6:g}, min: 0 }}
  - {{ id: Ca, label: Test capacitor added across the switch, family: capacitance, unit: pF, default: {sCa*1e12:g}, min: 0, help: 'Add capacitors until the ringing frequency drops by about half; a 2:1 drop gives the most accurate result.' }}
  - {{ id: f1, label: Ringing frequency with the test capacitor, family: frequency, unit: MHz, default: {sf1/1e6:g}, min: 0 }}
  - {{ id: k, label: Snubber capacitor multiplier (Cs ÷ Cp), default: {sk:g}, min: 1, help: 'Usually 3–4. Larger values damp better but raise the resistor loss.' }}
  - {{ id: V, label: Voltage switched, family: voltage, unit: V, default: {sV:g}, min: 0 }}
  - {{ id: fsw, label: Switching frequency, family: frequency, unit: kHz, default: {sfs/1e3:g}, min: 0 }}
  - {{ id: Cp, label: Parasitic capacitance, family: capacitance, unit: pF, min: 0 }}
  - {{ id: Lp, label: Parasitic (loop) inductance, family: inductance, unit: nH, min: 0 }}
  - {{ id: Z0, label: Characteristic impedance √(Lp ÷ Cp), family: resistance, unit: ohm, min: 0 }}
  - {{ id: Rs, label: Snubber resistor, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Cs, label: Snubber capacitor, family: capacitance, unit: pF, min: 0 }}
  - {{ id: Ps, label: Power dissipated in the snubber resistor, family: power, unit: W, min: 0 }}
  - {{ id: tau, label: Snubber time constant Rs × Cs, family: seconds, unit: ns, min: 0 }}
equations:
  - Cp = Ca / ((f0 / f1)^2 - 1)
  - Lp = 1 / ((2 * pi * f0)^2 * Cp)
  - Z0 = sqrt(Lp / Cp)
  - Rs = Z0
  - Cs = k * Cp
  - Ps = Cs * V^2 * fsw
  - tau = Rs * Cs
faq:
  - q: How do you calculate an RC snubber?
    a: Measure the ringing frequency f₀, add a known capacitor C_add across the switch and measure the new frequency f₁. The parasitic capacitance is C_p = C_add ÷ ((f₀ ÷ f₁)² − 1), the inductance L_p = 1 ÷ ((2πf₀)² C_p) and the snubber resistor R = √(L_p ÷ C_p). Choose the snubber capacitor 3–4 times C_p so that R, not the capacitor, sets the damping.
  - q: How much power does a snubber resistor dissipate?
    a: P = C_s × V² × f_sw — the capacitor's stored energy ½C V² is dissipated in the resistor once when it charges and once when it discharges, every switching cycle. A 293 pF snubber switching 48 V at 200 kHz dissipates about 0.13 W, so a 0.25 W or larger pulse-rated resistor is used.
  - q: Why add a capacitor until the frequency halves?
    a: When f₁ = f₀ ÷ 2 the added capacitor is exactly three times the parasitic capacitance, so the measurement is well above the scope probe and fixture capacitance and the result is not sensitive to small reading errors. Any ratio works with the formula, but ratios close to 1 give poor accuracy.
  - q: What type of resistor and capacitor should a snubber use?
    a: Use a low-inductance resistor (thick-film or carbon composition, not wirewound) and a capacitor with low ESL rated well above the peak voltage — C0G/NP0 ceramic or polypropylene film. Keep the snubber loop as short as possible, directly across the device that rings.
related: [electronics/mosfet-power-loss, electronics/resonant-frequency, electronics/reactance, electronics/rc-filter, electronics/buck-converter]
''', f'''
## How to use the RC snubber calculator

Measure the **ringing frequency** at the switch node with the circuit running and a short ground lead on the scope probe. Solder a **test capacitor** across the device (start with a few hundred pF) and measure the **new ringing frequency** — aim for about half the original. Enter both frequencies and the test capacitor, the **capacitor multiplier**, the **voltage switched** and the **switching frequency**. The calculator gives the parasitic capacitance and inductance, the characteristic impedance, the snubber resistor and capacitor and the resistor's power dissipation.

## RC snubber formulas

<p class="formula">C<sub>p</sub> = C<sub>add</sub> ÷ [(f<sub>0</sub> ÷ f<sub>1</sub>)² − 1] &nbsp;·&nbsp; L<sub>p</sub> = 1 ÷ [(2π f<sub>0</sub>)² C<sub>p</sub>]</p>

<p class="formula">R<sub>s</sub> = Z<sub>0</sub> = √(L<sub>p</sub> ÷ C<sub>p</sub>) &nbsp;·&nbsp; C<sub>s</sub> = k × C<sub>p</sub> (k ≈ 3–4) &nbsp;·&nbsp; P<sub>R</sub> = C<sub>s</sub> V² f<sub>sw</sub></p>

The ringing is the resonance of the loop inductance with the parasitic capacitance, f = 1 ÷ (2π√(LC)). A resistor equal to the characteristic impedance gives close to critical damping; the series capacitor blocks DC so the resistor only conducts during the edges.

## Worked example

A 48 V synchronous buck switching at {sfs/1e3:g} kHz rings at {sf0/1e6:g} MHz on the switch node. Adding {sCa*1e12:g} pF across the low-side MOSFET drops the ringing to {sf1/1e6:g} MHz:

- Frequency ratio squared (f<sub>0</sub> ÷ f<sub>1</sub>)² = ({sf0/1e6:g} ÷ {sf1/1e6:g})² = {SN['x']:g}
- Parasitic capacitance C<sub>p</sub> = {sCa*1e12:g} ÷ ({SN['x']:g} − 1) = **{SN['Cp']*1e12:.2f} pF**
- Parasitic inductance L<sub>p</sub> = 1 ÷ ((2π × {sf0/1e6:g} MHz)² × {SN['Cp']*1e12:.2f} pF) = **{SN['Lp']*1e9:.2f} nH**
- Snubber resistor R<sub>s</sub> = √({SN['Lp']*1e9:.2f} nH ÷ {SN['Cp']*1e12:.2f} pF) = **{SN['Z']:.2f} Ω** — use 27 Ω
- Snubber capacitor C<sub>s</sub> = {sk:g} × {SN['Cp']*1e12:.2f} = **{SN['Cs']*1e12:.1f} pF** — use 330 pF (or 270 pF)
- Resistor power P = {SN['Cs']*1e12:.1f} pF × {sV:g}² × {sfs/1e3:g} kHz = **{SN['Ps']:.3f} W**; time constant R<sub>s</sub>C<sub>s</sub> = **{SN['tau']*1e9:.2f} ns**

## Parasitic capacitance from the frequency drop

| f<sub>0</sub> ÷ f<sub>1</sub> | C<sub>p</sub> | C<sub>add</sub> = 100 pF | 220 pF | 470 pF | 1 nF |
|---|---|---|---|---|---|
{sr_rows}
## Snubber resistor power P = C V² f

| Voltage | 100 pF at 100 kHz | 470 pF at 100 kHz | 1 nF at 100 kHz | 1 nF at 500 kHz | 4.7 nF at 100 kHz |
|---|---|---|---|---|---|
{sp_rows}
## Practical notes

- **Fix the layout first:** a shorter hot loop and a closer input capacitor reduce L<sub>p</sub>, raise the ringing frequency and reduce the energy the snubber has to absorb.
- **Check the result:** fit the calculated R and C, then confirm on the scope that the overshoot is damped within one or two cycles. Adjust R ±50% to fine-tune; if the loss is too high, reduce k towards 2.
- **Rating:** the resistor sees pulses of up to V ÷ R at every edge — choose a pulse-rated part and allow at least twice the calculated average power.
- **Snubber loss counts as switching loss** — include it in the converter efficiency with the [MOSFET power loss calculator](/electronics/mosfet-power-loss/). To check the ringing frequency from L and C, use the [resonant frequency calculator](/electronics/resonant-frequency/).
''')

# ======================================================================= ELECTRICAL

# ---------------------------------------------------------------- Rolling sphere
LPL = (('I', 20, 3, 5, 0.99), ('II', 30, 5, 10, 0.97), ('III', 45, 10, 15, 0.91), ('IV', 60, 16, 20, 0.84))
def sphere(R, H, h):
    Hc = min(H, R)
    d0 = math.sqrt(Hc * (2 * R - Hc))
    dh = math.sqrt(h * (2 * R - h))
    return dict(Hc=Hc, d0=d0, dh=dh, d=d0 - dh, I=(R / 10) ** (1 / 0.65), sag=lambda w: R - math.sqrt(R * R - (w / 2) ** 2))
rR, rH, rh = 45.0, 15.0, 6.0
RS = sphere(rR, rH, rh)
rl_rows = ''.join(f"| LPL {nm} | {R} m | {I} kA | {10*I**0.65:.1f} m | {m} × {m} m | {p*100:g}% |\n" for nm, R, I, m, p in LPL)
rd_rows = ''
for H in (3, 5, 10, 15, 20, 30, 45, 60):
    rd_rows += f"| {H} m | " + ' | '.join(f"{sphere(R, H, 0)['d0']:.1f} m" for nm, R, I, m, p in LPL) + " |\n"
rp_rows = ''
for h in (0, 2, 4, 6, 8, 10, 12):
    rp_rows += f"| {h} m | " + ' | '.join(f"{sphere(R, H, h)['d']:.1f} m" for R, H in ((20, 10), (30, 15), (45, 15), (45, 20), (60, 25))) + " |\n"
rs_rows = ''.join(f"| {w} m | " + ' | '.join(f"{(R - math.sqrt(R*R - (w/2)**2))*100:.0f} cm" for nm, R, I, m, p in LPL) + " |\n" for w in (5, 10, 15, 20, 30))
assert abs(RS['d0'] - math.sqrt(15 * 75)) < 1e-9

P('electrical', 'rolling-sphere', f'''
title: Rolling Sphere Calculator (Lightning Protection Radius)
description: Calculate the radius protected by a lightning rod or mast with the IEC 62305 rolling sphere method for LPL I–IV, at ground level and at the object height.
category: electrical
{intro("The rolling sphere method places air terminals so that an imaginary sphere rolled over the structure touches only the lightning protection system, never the parts being protected. This rolling sphere calculator gives the horizontal protection distance of a vertical lightning rod or mast at ground level and at the height of the object, for the sphere radius of each lightning protection level (LPL I–IV) in IEC 62305-3. For the background to the method, see this explanation of the [rolling sphere lightning protection](ib:lightning-protection-system-rolling-sphere) concept.")}
keywords: [rolling sphere calculator, rolling sphere method lightning protection, lightning protection radius calculator, lightning rod protection area, iec 62305 rolling sphere radius, lightning mast protection zone, air terminal protection radius]
updated: {D}
variables:
  - id: R
    label: Lightning protection level (sphere radius)
    default: {rR:g}
    options:
{''.join(f"      - {{ label: 'LPL {nm} — {R} m sphere', value: {R} }}" + chr(10) for nm, R, I, m, p in LPL)}  - {{ id: H, label: Height of the rod or mast tip above ground, family: length, unit: m, imperialUnit: ft, default: {rH:g}, min: 0 }}
  - {{ id: h, label: Height of the object to protect, family: length, unit: m, imperialUnit: ft, default: {rh:g}, min: 0 }}
  - {{ id: d0, label: Protected radius at ground level, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: d, label: Protected radius at the object height, family: length, unit: m, imperialUnit: ft }}
  - {{ id: Imin, label: Smallest lightning current intercepted, family: current, unit: kA, min: 0 }}
equations:
  - d0 = sqrt(min(H, R) * (2 * R - min(H, R)))
  - d = d0 - sqrt(h * (2 * R - h))
  - Imin = (R / 10)^(1 / 0.65) * 1000
faq:
  - q: What is the rolling sphere radius for each lightning protection level?
    a: IEC 62305-3 uses a sphere radius of 20 m for LPL I, 30 m for LPL II, 45 m for LPL III and 60 m for LPL IV. The matching mesh sizes are 5 × 5 m, 10 × 10 m, 15 × 15 m and 20 × 20 m. NFPA 780 uses a 46 m (150 ft) sphere for ordinary structures.
  - q: How do you calculate the protection radius of a lightning rod?
    a: For a rod of height H no taller than the sphere radius R, the protected distance at the height h of an object is d = √(H(2R − H)) − √(h(2R − h)). A 15 m mast with a 45 m sphere (LPL III) protects a radius of {RS['d0']:.1f} m at ground level and {RS['d']:.1f} m at a height of 6 m.
  - q: Why does a mast taller than the sphere radius not protect more?
    a: Once the rod is taller than R the sphere can touch its side, and the zone below is the same as for a rod of height R — the protected radius at ground can never exceed R. Tall structures above 60 m can also be struck on the side, so IEC 62305 requires side air terminations on their upper part.
  - q: How is the sphere radius related to lightning current?
    a: The striking distance follows the electrogeometric model R = 10 × I^0.65 (R in m, I in kA). A smaller sphere catches weaker strokes as well — the 20 m sphere of LPL I intercepts strokes down to 3 kA, which covers about 99% of flashes, while the 60 m sphere of LPL IV only guarantees interception of strokes above 16 kA (84%).
related: [electrical/earthing-resistance, electrical/earth-conductor-size, math/right-triangle-trig, math/circle]
''', f'''
## How to use the rolling sphere calculator

Pick the **lightning protection level** from your IEC 62305-2 risk assessment — it sets the rolling sphere radius — and enter the **height of the rod or mast tip** and the **height of the object** to be protected. The calculator gives the protected radius at ground level, the protected radius at the object's height and the smallest lightning current the system intercepts. The object is protected if every point of it lies within the protected radius at its height. Enter a required radius to find the mast height needed.

## Rolling sphere formula

<p class="formula">d<sub>0</sub> = √(H (2R − H)) &nbsp;·&nbsp; d(h) = √(H (2R − H)) − √(h (2R − h)) &nbsp;(H ≤ R)</p>

<p class="formula">R = 10 × I<sup>0.65</sup> &nbsp;(R in m, I in kA)</p>

R is the sphere radius, H the rod height and h the height of the point being checked. The formula comes from the geometry of a sphere resting on the ground and touching the rod tip. For H > R, use H = R. The calculation is for a single vertical rod on flat ground; between two or more masts the sphere sags less and the protected zone is larger.

## Worked example

A {rH:g} m mast protects equipment {rh:g} m tall at LPL III ({rR:g} m sphere):

- At ground level d<sub>0</sub> = √({rH:g} × (2 × {rR:g} − {rH:g})) = √{rH*(2*rR-rH):g} = **{RS['d0']:.2f} m**
- At the object height √({rh:g} × (2 × {rR:g} − {rh:g})) = √{rh*(2*rR-rh):g} = {RS['dh']:.2f} m
- Protected radius at {rh:g} m d = {RS['d0']:.2f} − {RS['dh']:.2f} = **{RS['d']:.2f} m**
- Smallest stroke intercepted I = ({rR:g} ÷ 10)^(1 ÷ 0.65) = **{RS['I']:.2f} kA**

Any part of the equipment more than {RS['d']:.1f} m from the mast at a height of {rh:g} m needs another air terminal.

## Lightning protection levels (IEC 62305)

| Level | Sphere radius R | Minimum peak current | R from 10 × I<sup>0.65</sup> | Mesh size | Interception probability |
|---|---|---|---|---|---|
{rl_rows}
## Protected radius at ground level by mast height

| Mast height | LPL I (20 m) | LPL II (30 m) | LPL III (45 m) | LPL IV (60 m) |
|---|---|---|---|---|
{rd_rows}
## Protected radius at the object height

| Object height | 10 m mast, LPL I | 15 m mast, LPL II | 15 m mast, LPL III | 20 m mast, LPL III | 25 m mast, LPL IV |
|---|---|---|---|---|---|
{rp_rows}
## Sphere sag between two air terminals

Depth the sphere dips below the line joining two conductors at the same height, p = R − √(R² − (w ÷ 2)²):

| Spacing w | LPL I | LPL II | LPL III | LPL IV |
|---|---|---|---|---|
{rs_rows}
## Practical notes

- **Roofs:** air termination rods on a flat roof must project far enough above the roof for the sphere not to touch the roof between them — check the sag table against the rod height above the roof.
- **Protection angle method:** IEC 62305-3 also allows a protection-angle method for simple structures; it gives similar results for short rods but becomes conservative for tall masts. The rolling sphere method works for any shape.
- **Earthing:** an air termination is only effective with low-impedance down conductors and a good earth termination — check it with the [earthing resistance calculator](/electrical/earthing-resistance/) and size conductors with the [earth conductor size calculator](/electrical/earth-conductor-size/).
- This calculator is a design aid; the final layout must be checked by a competent designer against IEC 62305, NFPA 780 or your local standard.
''')

print(len(DESC), 'pages:', ' '.join(DESC))
