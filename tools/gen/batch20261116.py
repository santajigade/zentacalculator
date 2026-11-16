"""Batch 2026-11-16: 6 calculators. Engineering (steam consumption, conveyor belt capacity, proof test coverage), electronics (decoupling capacitor) and chemistry (molar flow rate, reactor conversion). Assembled from three sections; every table and worked example is computed here from the calculator defaults."""

# ======================================================================= SECTION _batch_a1.py
"""Batch 2026-11-16 slice A1: steam consumption (engineering) and conveyor belt capacity (engineering).
Steam tables are computed with the iapws package (IAPWS-IF97); all worked examples use the defaults."""
import sys, math, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro as _intro
from iapws import IAPWS97
D = '2026-11-16'
pi = math.pi
DASH = re.compile('[' + chr(0x2013) + chr(0x2014) + ']')
DONE = []


def intro(p1, p2, phrase):
    assert phrase.lower() in p1.lower(), phrase
    t = p1 + '\n\n' + p2
    plain = re.sub(r'\]\(ib:[a-z0-9-]+\)', ']', t)
    n = len(plain.split())
    assert 60 <= n <= 90, (phrase, n)
    return _intro(t)


def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    assert 'featured' not in fm
    assert not DASH.search(fm) and not DASH.search(body), slug
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    n = len(body.split())
    assert n >= 520, (slug, n)
    page(cat, slug, fm, body)
    DONE.append(f'{cat}/{slug}')


# ---------------------------------------------------------------- Steam consumption
def sat(barg):
    p = (barg + 1.01325) / 10  # MPa absolute
    w = IAPWS97(P=p, x=0); s = IAPWS97(P=p, x=1)
    return dict(T=w.T - 273.15, hf=w.h, hg=s.h, hfg=s.h - w.h, v=s.v)

ST = {g: sat(g) for g in (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20)}
st_rows = ''.join(f"| {g} bar(g) | {g+1.01325:.2f} bar(a) | {r['T']:.1f} °C | {r['hf']:,.0f} | {r['hfg']:,.0f} | {r['hg']:,.0f} | {r['v']:.3f} |\n"
                  for g, r in ST.items())
h3, h10 = ST[3]['hfg'], ST[10]['hfg']
sm, scp, sT1, sT2, sh, se = 5000.0, 4.19, 20.0, 80.0, round(h3), 0.95
sdT = sT2 - sT1
sQ = sm / 3600 * scp * 1000 * sdT          # W
sms = sQ / (sh * 1000 * se)                 # kg/s
sr = 1000 * sms / (sm / 3600)
# at 10 bar(g) instead
sms10 = sQ / (round(h10) * 1000 * se)
# flash steam fraction when 3 bar(g) condensate drops to atmospheric
flash = (ST[3]['hf'] - ST[0]['hf']) / ST[0]['hfg']
# credit from subcooling condensate to 90 C in the heater
sub_h = sh + (ST[3]['hf'] - IAPWS97(T=90 + 273.15, P=(3 + 1.01325) / 10).h)
sms_sub = sQ / (sub_h * 1000 * se)
# steam per tonne of water heated by dT at 3 bar(g)
sp_rows = ''
for dT in (20, 40, 60, 80):
    sp_rows += f"| {dT} K | " + ' | '.join(f"{1000*4.19*dT/(ST[g]['hfg']*se):.1f} kg" for g in (1, 3, 7, 10)) + " |\n"
fuel_kw = sms * 3600  # kg/h

P('engineering', 'steam-consumption', f'''
title: Steam Consumption Calculator (Heating with Saturated Steam)
description: Calculate steam consumption in kg/h to heat a product stream from its flow, specific heat and temperature rise, using the latent heat at steam pressure.
category: engineering
{intro("Steam heats a product by condensing and giving up its latent heat. This steam consumption calculator finds the heat duty to warm a flowing liquid and the steam flow in kg/h needed to supply it at your steam pressure, including an allowance for losses.",
       "Process, utility and instrument engineers use it to size steam control valves, steam traps and flow meters, to check boiler load and to compare heating options before a heat exchanger is specified.", 'steam consumption calculator')}
keywords: [steam consumption calculator, steam consumption formula, steam required to heat water, kg of steam per hour, steam flow calculation heat exchanger, latent heat of steam, steam load calculation]
published: {D}
updated: {D}
variables:
  - {{ id: m, label: Product mass flow, family: massflow, unit: kgh, imperialUnit: lbh, default: {sm:g}, min: 0 }}
  - {{ id: cp, label: Product specific heat (cp), suffix: kJ/kg·K, default: {scp:g}, min: 0, help: 'Water 4.19 · Milk about 3.9 · Light oil about 2.0 · Air 1.005' }}
  - {{ id: T1, label: Product inlet temperature, family: temperature, unit: C, imperialUnit: F, default: {sT1:g} }}
  - {{ id: T2, label: Product outlet temperature, family: temperature, unit: C, imperialUnit: F, default: {sT2:g} }}
  - {{ id: hfg, label: Latent heat of steam at supply pressure (hfg), suffix: kJ/kg, default: {sh}, min: 1, help: 'Saturated steam: 0 bar(g) {ST[0]["hfg"]:,.0f} · 3 bar(g) {h3:,.0f} · 7 bar(g) {ST[7]["hfg"]:,.0f} · 10 bar(g) {h10:,.0f} kJ/kg (see the table below).' }}
  - {{ id: eff, label: Heat utilisation (allowance for losses), family: percent, unit: '%', default: {se*100:g}, min: 0.01, max: 1, help: 'Share of the steam heat that reaches the product. 95% is typical for an insulated heat exchanger; open tanks and direct injection with losses are lower.' }}
  - {{ id: dT, label: Temperature rise, family: tempdiff, unit: K, imperialUnit: F }}
  - {{ id: Q, label: Heat duty, family: power, unit: kW, imperialUnit: BTUh }}
  - {{ id: ms, label: Steam consumption, family: massflow, unit: kgh, imperialUnit: lbh, min: 0 }}
  - {{ id: r, label: Steam per tonne of product, suffix: kg/t, min: 0, decimals: 1 }}
equations:
  - dT = T2 - T1
  - Q = m * cp * 1000 * dT
  - ms = Q / (hfg * 1000 * eff)
  - r = 1000 * ms / m
faq:
  - q: How do I calculate steam consumption?
    a: "Find the heat the product needs, Q = ṁ × cp × ΔT, then divide by the heat each kilogram of steam gives up when it condenses, which is its latent heat hfg at the supply pressure. Divide again by the heat utilisation to allow for losses. Heating 5,000 kg/h of water by 60 K with 3 bar(g) steam needs about {sms*3600:.0f} kg/h."
  - q: How much steam is needed to heat 1,000 litres of water?
    a: "Heating 1,000 kg of water by 60 K takes 1,000 × 4.19 × 60 = 251,400 kJ. At 3 bar(g), where hfg is about {h3:,.0f} kJ/kg, that is {251400/h3:.0f} kg of steam with no losses, or {251400/h3/se:.0f} kg with a 95% allowance. Divide by the heating time in hours for kg/h."
  - q: Why use the latent heat and not the total enthalpy of steam?
    a: "In an indirect heater the steam condenses and leaves through the trap as hot condensate at about the steam temperature, so only the latent heat is given to the product. The total enthalpy hg applies only if the condensate is also cooled to the product temperature, as in direct steam injection."
  - q: Is higher pressure steam better for heating?
    a: "Not per kilogram. Latent heat falls as pressure rises, from {ST[0]['hfg']:,.0f} kJ/kg at atmospheric pressure to {h10:,.0f} kJ/kg at 10 bar(g), so low pressure steam carries more usable heat per kg. Higher pressure gives a hotter steam temperature and a smaller heat exchanger, and lets steam be distributed in smaller pipes."
  - q: How does steam consumption relate to boiler capacity?
    a: "Add the consumption of all users that run at the same time, then add distribution losses and a margin. A boiler rated 'from and at 100 °C' produces less steam when the feedwater is colder or the pressure is higher, so convert the rating before comparing it with the steam demand."
related: [engineering/heat-duty, engineering/tank-heater-sizing, engineering/boiler-efficiency, engineering/pipe-heat-loss, engineering/lmtd, engineering/mass-flow-rate]
''', f'''
## How to use the steam consumption calculator

Enter the **product mass flow**, its **specific heat**, the **inlet and outlet temperatures**, the **latent heat** of the steam at the pressure in the heater (read it from the table below) and the **heat utilisation**. The calculator gives the temperature rise, the heat duty, the steam consumption in kg/h and the steam needed per tonne of product. To find the product flow a given steam supply can heat, enter the steam flow and press × on the product flow so it becomes the result.

## Steam consumption formula

<p class="formula">Q = ṁ<sub>p</sub> × c<sub>p</sub> × (T<sub>2</sub> − T<sub>1</sub>) &nbsp;·&nbsp; ṁ<sub>s</sub> = Q ÷ (h<sub>fg</sub> × η)</p>

ṁ<sub>p</sub> is the product flow in kg/s, c<sub>p</sub> the specific heat in J/kg·K, h<sub>fg</sub> the latent heat in J/kg and η the heat utilisation as a fraction. The result ṁ<sub>s</sub> is in kg/s; multiply by 3,600 for kg/h. Use the pressure **inside the heater**, after the control valve, because that is where the steam condenses.

## Worked example

A plate heat exchanger warms **{sm:,.0f} kg/h** of water (c<sub>p</sub> = {scp:g} kJ/kg·K) from **{sT1:g} °C** to **{sT2:g} °C** with saturated steam at **3 bar(g)**, where h<sub>fg</sub> = {h3:,.1f} kJ/kg (rounded to {sh:,}). Heat utilisation is {se*100:g}%:

- Temperature rise = {sT2:g} − {sT1:g} = **{sdT:g} K**
- Heat duty Q = {sm:,.0f} ÷ 3,600 × {scp:g} × {sdT:g} = **{sQ/1000:.1f} kW**
- Steam consumption = {sQ/1000:.1f} ÷ ({sh:,} × {se:g}) = {sms:.4f} kg/s = **{sms*3600:.1f} kg/h**
- Steam per tonne of water = **{sr:.1f} kg/t**

With 10 bar(g) steam in the heater (h<sub>fg</sub> = {h10:,.0f} kJ/kg) the same duty needs {sms10*3600:.1f} kg/h, about {(sms10/sms-1)*100:.0f}% more steam by mass. If the condensate is sub-cooled to 90 °C inside the heater before it leaves, each kg gives {sub_h:,.0f} kJ and the consumption falls to {sms_sub*3600:.0f} kg/h.

## Saturated steam table (IAPWS-IF97)

Computed for gauge pressures above a standard atmosphere of 1.01325 bar. h<sub>f</sub>, h<sub>fg</sub> and h<sub>g</sub> are in kJ/kg; v<sub>g</sub> is the specific volume of the steam in m³/kg:

| Gauge pressure | Absolute | Saturation temperature | h<sub>f</sub> | h<sub>fg</sub> | h<sub>g</sub> | v<sub>g</sub> |
|---|---|---|---|---|---|---|
{st_rows}
## Steam needed per tonne of water

For water (c<sub>p</sub> = 4.19 kJ/kg·K) with {se*100:g}% heat utilisation:

| Temperature rise | 1 bar(g) | 3 bar(g) | 7 bar(g) | 10 bar(g) |
|---|---|---|---|---|
{sp_rows}
## How steam consumption is used in practice

The steam flow sets the size of everything on the steam side. The **control valve** is sized for the maximum steam flow with the heater pressure as its outlet pressure; the **steam trap** must pass the same mass of condensate against the back pressure of the return line; and a **steam flow meter** (vortex or orifice with pressure and temperature compensation) is ranged a little above it. At start-up the product is cold and the heater sees a much larger temperature difference, so the start-up load can be two or three times the running load; size traps for it.

When the condensate returns to an atmospheric tank, part of it flashes back to steam: condensate at 3 bar(g) dropping to 0 bar(g) flashes {flash*100:.1f}% of its mass. That flash steam can be recovered in a flash vessel for low pressure heating, which is one reason plants measure steam and condensate flows separately.

## Common mistakes

- **Using the boiler pressure instead of the heater pressure.** The control valve drops the pressure, so the steam condenses at the lower pressure with a higher latent heat and a lower temperature.
- **Using total enthalpy h<sub>g</sub> for an indirect heater.** The condensate leaves hot, so only h<sub>fg</sub> (plus any sub-cooling) heats the product. Using h<sub>g</sub> understates the steam by roughly 20%.
- **Mixing kJ and kW without hours.** kW is kJ/s; a duty in kW divided by kJ/kg gives kg/s, which must be multiplied by 3,600 for kg/h.
- **Ignoring heat losses and the vessel.** Open tanks lose heat from the surface, and batch heating also warms the vessel steel; a 100% utilisation figure is never reached.
- **Sizing for running load only.** Cold start-up and stalled condensate drainage can multiply the load, and an undersized trap waterlogs the heater.
''')

# ---------------------------------------------------------------- Conveyor belt capacity
cD, cN, cA, cR, cL = 500.0, 60.0, 0.06, 850.0, 100.0
cv = pi * cD / 1000 * cN / 60
cQv = cA * cv
cQm = cQv * cR
cq = cA * cR
ct = cL / cv
# belt thickness effect: 12 mm belt on the pulley adds to the pitch diameter
cvt = pi * (cD + 12) / 1000 * cN / 60
# capacity table, t/h at the default bulk density, by belt speed and load area
cap_rows = ''
for v in (1.0, 1.5, 2.0, 2.5, 3.0, 4.0):
    cap_rows += f"| {v:.1f} m/s | " + ' | '.join(f"{a*v*cR*3.6:,.0f} t/h" for a in (0.02, 0.04, 0.06, 0.10, 0.15)) + " |\n"
MAT = [('Coal (bituminous, crushed)', 800, 900), ('Wheat', 750, 800), ('Cement (Portland, loose)', 1200, 1500),
       ('Limestone (crushed)', 1400, 1600), ('Sand (dry)', 1500, 1700), ('Gravel', 1600, 1800), ('Iron ore', 2000, 2400)]
mat_rows = ''
for nm, lo, hi in MAT:
    mid = (lo + hi) / 2
    mat_rows += f"| {nm} | {lo:,} to {hi:,} kg/m³ | {cA*cv*mid*3.6:,.0f} t/h |\n"
# speed needed for a 400 t/h target on the default belt
c_target = 400.0
cv_need = c_target / 3.6 / (cA * cR)
cN_need = cv_need * 60 / (pi * cD / 1000)

P('engineering', 'conveyor-belt-capacity', f'''
title: Conveyor Belt Capacity Calculator (Speed and t/h)
description: Calculate conveyor belt speed from pulley diameter and rpm, then the capacity in m³/h and t/h from the load cross section and bulk density.
category: engineering
{intro("A belt conveyor carries a strip of bulk material whose cross section moves at belt speed. This conveyor belt capacity calculator finds the belt speed from the drive pulley diameter and rpm, then the volume and tonnes per hour, the load per metre and the travel time.",
       "Mechanical, process and instrument engineers use it to check a conveyor against plant throughput, to set the speed of a variable speed drive and to range belt scales and speed sensors.", 'conveyor belt capacity calculator')}
keywords: [conveyor belt capacity calculator, conveyor belt speed calculator, conveyor capacity formula, belt conveyor tph calculation, conveyor belt speed formula, conveyor load per metre, belt conveyor capacity in tonnes per hour]
published: {D}
updated: {D}
variables:
  - {{ id: D, label: Drive pulley diameter (over the belt), family: length, unit: mm, imperialUnit: in, default: {cD:g}, min: 0, help: 'For belt speed use the diameter to the middle of the belt: pulley plus lagging plus belt thickness.' }}
  - {{ id: N, label: Drive pulley speed, suffix: rpm, default: {cN:g}, min: 0 }}
  - {{ id: A, label: Cross-sectional area of the load on the belt, family: area, unit: m2, imperialUnit: ft2, default: {cA:g}, min: 0, help: 'From the belt manufacturer or design standard for the belt width, troughing angle and surcharge angle.' }}
  - {{ id: rho, label: Bulk density of the material, family: density, unit: kgm3, imperialUnit: lbft3, default: {cR:g}, min: 0 }}
  - {{ id: Lc, label: Conveyor length (centre to centre), family: length, unit: m, imperialUnit: ft, default: {cL:g}, min: 0 }}
  - {{ id: v, label: Belt speed, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: Qv, label: Volumetric capacity, family: flow, unit: m3h, imperialUnit: cfm, min: 0 }}
  - {{ id: Qm, label: Mass capacity, family: massflow, unit: th, imperialUnit: lbh, min: 0 }}
  - {{ id: q, label: Load per metre of belt, suffix: kg/m, min: 0, decimals: 1 }}
  - {{ id: t, label: Material travel time, family: seconds, unit: s, min: 0 }}
equations:
  - v = pi * D * N / 60
  - Qv = A * v
  - Qm = A * v * rho
  - q = A * rho
  - t = Lc / v
faq:
  - q: How do you calculate conveyor belt capacity?
    a: "Multiply the cross-sectional area of the material on the belt by the belt speed to get volume per second, then by the bulk density for mass. In tonnes per hour: Q = 3.6 × A × v × ρ with A in m², v in m/s and ρ in kg/m³. A 0.06 m² load at 1.571 m/s on coal of 850 kg/m³ gives about {cQm*3.6:.0f} t/h."
  - q: How do you calculate conveyor belt speed?
    a: "Belt speed is the circumference of the drive pulley times its revolutions per second: v = π × D × N ÷ 60, with D in metres and N in rpm. A 500 mm pulley at 60 rpm moves the belt at {cv:.3f} m/s. Find the pulley rpm from the motor speed divided by the gearbox ratio."
  - q: What is a typical conveyor belt speed?
    a: "Most bulk conveyors run between about 1 and 4 m/s. Fine, dusty or fragile materials and feeders run slower; long overland conveyors carrying coal or ore can run at 4 to 6 m/s or more. Higher speed raises capacity for a given belt width but increases wear, dust and spillage at transfers."
  - q: What does the load per metre tell me?
    a: "Load per metre, q = A × ρ, is the weight the idlers and belt carry on each metre of conveyor. It is needed for idler selection and belt tension, and a belt scale measures it directly: the scale reads kg/m, a speed sensor reads m/s, and their product is the flow rate in kg/s."
  - q: Why is the measured capacity lower than the design capacity?
    a: "The design area assumes the belt is loaded full and evenly across its width. In practice feed varies, material slumps on inclines, and the belt is rarely filled to the full surcharge, so many conveyors run at 70 to 90% of their theoretical capacity. Size with a margin and check with a belt scale."
related: [engineering/pulley-speed, engineering/belt-tension, engineering/gear-ratio, engineering/torque-power-speed, engineering/mass-flow-rate, physics/density]
''', f'''
## How to use the conveyor belt capacity calculator

Enter the **drive pulley diameter** (to the middle of the belt), the **pulley speed** in rpm, the **cross-sectional area** of the load on the belt, the material's **bulk density** and the **conveyor length**. The calculator gives the belt speed, the volume and mass capacity, the load per metre and how long material takes to travel from tail to head. To find the pulley speed for a target capacity, enter the capacity and press × on the speed so it becomes the result.

## Conveyor belt capacity formula

<p class="formula">v = π × D × N ÷ 60 &nbsp;·&nbsp; Q<sub>v</sub> = A × v &nbsp;·&nbsp; Q<sub>m</sub> = A × v × ρ &nbsp;·&nbsp; q = A × ρ</p>

D is in metres, N in rpm, A in m², ρ in kg/m³ and v in m/s, so Q<sub>v</sub> is in m³/s and Q<sub>m</sub> in kg/s. Multiply Q<sub>v</sub> by 3,600 for m³/h and Q<sub>m</sub> by 3.6 for t/h.

## Worked example

A coal conveyor has a **{cD:g} mm** drive pulley turning at **{cN:g} rpm**. The belt design gives a load cross section of **{cA:g} m²**, the coal's bulk density is **{cR:g} kg/m³** and the conveyor is **{cL:g} m** long:

- Belt speed v = π × {cD/1000:g} × {cN:g} ÷ 60 = **{cv:.3f} m/s**
- Volumetric capacity = {cA:g} × {cv:.3f} = {cQv:.4f} m³/s = **{cQv*3600:.1f} m³/h**
- Mass capacity = {cQv:.4f} × {cR:g} = {cQm:.2f} kg/s = **{cQm*3.6:.1f} t/h**
- Load per metre = {cA:g} × {cR:g} = **{cq:.1f} kg/m**
- Travel time = {cL:g} ÷ {cv:.3f} = **{ct:.1f} s**

To reach {c_target:.0f} t/h on the same belt the speed must rise to {c_target:.0f} ÷ 3.6 ÷ {cq:.1f} = {cv_need:.3f} m/s, which is {cN_need:.1f} rpm at the pulley.

## Capacity by belt speed and load area

Tonnes per hour at a bulk density of {cR:g} kg/m³. The area depends on belt width, troughing angle and surcharge angle:

| Belt speed | 0.02 m² | 0.04 m² | 0.06 m² | 0.10 m² | 0.15 m² |
|---|---|---|---|---|---|
{cap_rows}
## Typical bulk densities

Loose bulk densities vary with moisture, size grading and compaction, so these are typical ranges only; measure your material where accuracy matters. The last column is the capacity of the example belt ({cA:g} m² at {cv:.3f} m/s) at the middle of each range:

| Material | Typical bulk density | Capacity on example belt |
|---|---|---|
{mat_rows}
## How the load area is found

The load cross section is set by the **belt width**, the **troughing angle** of the idlers (often 20°, 35° or 45°) and the **surcharge angle**, the angle the material heap forms on the moving belt, which is usually 10° to 20° less than its angle of repose. Belt manufacturers and design standards such as CEMA and ISO 5048 publish the area for each combination, and only part of the belt width (the edge distance is kept clear) is loaded. A steeply inclined conveyor carries a smaller heap, so the area is reduced on inclines.

## Measuring capacity in practice

Plants measure the actual flow with a **belt weigher**: load cells under one or more idlers give the load per metre, and a speed sensor on a tail or bend pulley gives the belt speed. The integrator multiplies them into t/h and totalises tonnes. Zero calibration is done with the belt running empty and span calibration with test weights or a material test. Speed is often also monitored by a zero speed switch to trip the conveyor if the belt slips or breaks.

## Common mistakes

- **Using the bare pulley diameter.** The belt speed follows the middle of the belt. A 12 mm belt on this {cD:g} mm pulley raises the speed from {cv:.3f} to {cvt:.3f} m/s, a {(cvt/cv-1)*100:.1f}% difference that also shows up in a belt scale's totals.
- **Using the motor rpm.** The pulley turns at the motor speed divided by the gearbox and any belt drive ratio.
- **Using particle density instead of bulk density.** Bulk density includes the voids between lumps and is often half the solid density or less.
- **Treating the theoretical capacity as the rating.** Uneven feed, inclines and spillage keep real capacity below A × v × ρ; leave a margin.
- **Mixing units.** A in m² times v in m/s gives m³/s, not m³/h; forgetting the factor of 3,600 makes capacity look tiny.
''')

print(len(DONE), 'pages:', ' '.join(DONE))

# ======================================================================= SECTION _batch_a2.py
"""Batch 2026-11-16, slice A2: proof test coverage (engineering) and decoupling capacitor (electronics).
All reference tables and worked examples are computed here from the calculator defaults."""
import sys, math, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro as _intro
D = '2026-11-16'
pi = math.pi
DASH = re.compile('[' + chr(0x2013) + chr(0x2014) + ']')
DONE = []


def intro(p1, p2, phrase):
    assert phrase.lower() in p1.lower(), phrase
    t = p1 + '\n\n' + p2
    plain = re.sub(r'\]\(ib:[a-z0-9-]+\)', ']', t)
    n = len(plain.split())
    assert 60 <= n <= 90, (phrase, n)
    return _intro(t)


def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    assert 'featured' not in fm
    assert not DASH.search(fm) and not DASH.search(body), slug
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    n = len(body.split())
    assert n >= 520, (slug, n)
    page(cat, slug, fm, body)
    DONE.append(f'{cat}/{slug}')


def sil(pfd):
    rrf = 1 / pfd
    return max(0, min(4, math.floor(math.log10(rrf))))


def sci(x):
    m, e = f'{x:.2e}'.split('e')
    return f'{m} × 10<sup>{int(e)}</sup>'


# ---------------------------------------------------------------- Proof test coverage
def ptc(lam, TI, c, MT):
    l = lam * 1e-9
    pfd = l * 8760 * (c * TI + (1 - c) * MT) / 2
    pfp = l * 8760 * TI / 2
    return dict(pfd=pfd, pfp=pfp, ratio=pfd / pfp, rrf=1 / pfd, sil=sil(pfd))
pL, pT, pC, pM = 500.0, 1.0, 0.9, 15.0
PT = ptc(pL, pT, pC, pM)
lam_h = pL * 1e-9
part1 = lam_h * 8760 * pC * pT / 2
part2 = lam_h * 8760 * (1 - pC) * pM / 2
pt_rows = ''
for c in (0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0):
    pt_rows += f"| {c*100:.0f}% | " + ' | '.join(f"{ptc(pL, pT, c, m)['pfd']:.5f} (SIL {ptc(pL, pT, c, m)['sil']})" for m in (5, 10, 15, 20)) + " |\n"
# target: highest lambda for SIL 2 (PFD < 0.01) at the default TI, PTC, MT
lam_max = 0.01 / (1e-9 * 8760 * (pC * pT + (1 - pC) * pM) / 2)
# needed coverage to stay below 0.005 at the default lambda
c_need = (0.005 * 2 / (lam_h * 8760) - pM) / (pT - pM)
# shorter interval needed with PTC 90% to get back to the perfect test PFD
ti_eq = (PT['pfp'] * 2 / (lam_h * 8760) - (1 - pC) * pM) / pC
cov_rows = ''
for dev, c in (('Pressure transmitter, full calibration with applied pressure', '90 to 98%'),
               ('Pressure transmitter, current loop test only (no pressure applied)', '50 to 70%'),
               ('Shutdown valve, full stroke with leak test', '90 to 99%'),
               ('Shutdown valve, full stroke without leak test', '70 to 90%'),
               ('Shutdown valve, partial stroke test', '50 to 80% of the valve λDU'),
               ('Safety PLC, I/O and logic test per manual', '90 to 99%')):
    cov_rows += f'| {dev} | {c} |\n'

P('engineering', 'proof-test-coverage', f'''
title: Proof Test Coverage Calculator (PFDavg with Imperfect Proof Tests)
description: Calculate 1oo1 PFDavg with an imperfect proof test: proof test coverage, test interval and mission time, compared with a perfect test, with RRF and SIL.
category: engineering
{intro("Proof test coverage is the share of dangerous undetected failures that a proof test actually finds. This proof test coverage calculator adds the failures a test misses, which stay hidden until overhaul or the end of the mission time, to the 1oo1 PFDavg, as covered in [proof test interval and coverage](ib:proof-test-interval-coverage-safety-transmitters-iec-61511).",
       "Safety engineers use it in SIL verification to show how much an imperfect test raises PFDavg, and to choose the test procedure, test interval and overhaul interval that keep the SIF within its SIL.", 'proof test coverage calculator')}
keywords: [proof test coverage calculator, proof test coverage, ptc pfdavg, imperfect proof test, pfdavg mission time, proof test interval sil, iec 61511 proof test coverage, partial proof test]
published: {D}
updated: {D}
variables:
  - {{ id: lam, label: Dangerous undetected failure rate (λDU), suffix: FIT, default: {pL:g}, min: 0, help: '1 FIT = 1 failure per 10⁹ hours. Use the λDU of the whole 1oo1 safety function (sensor, logic solver and final element).' }}
  - {{ id: TI, label: Proof test interval, suffix: years, default: {pT:g}, min: 0 }}
  - {{ id: PTC, label: Proof test coverage, family: percent, unit: '%', default: {pC*100:g}, min: 0, max: 1, help: 'Fraction of λDU the proof test reveals. 100% is a perfect test.' }}
  - {{ id: MT, label: Mission time (or overhaul interval), suffix: years, default: {pM:g}, min: 0, help: 'Time after which the failures the proof test misses are found and repaired: a full overhaul, replacement, or the end of the plant life.' }}
  - {{ id: PFD, label: PFDavg with imperfect proof test, min: 0, decimals: 6 }}
  - {{ id: PFDp, label: PFDavg with a perfect proof test, min: 0, decimals: 6 }}
  - {{ id: ratio, label: Increase over a perfect test (times), min: 0, decimals: 2 }}
  - {{ id: RRF, label: Risk reduction factor (1/PFDavg), min: 0, decimals: 0 }}
  - {{ id: SIL, label: SIL achieved (by PFDavg only), min: 0, decimals: 0 }}
equations:
  - PFD = lam * 1e-9 * 8760 * (PTC * TI + (1 - PTC) * MT) / 2
  - PFDp = lam * 1e-9 * 8760 * TI / 2
  - ratio = PFD / PFDp
  - RRF = 1 / PFD
  - SIL = max(0, min(4, floor(log10(RRF))))
faq:
  - q: What is proof test coverage?
    a: "Proof test coverage (PTC) is the fraction of dangerous undetected failures that a proof test detects. A test that applies a real process signal and checks the trip action end to end may reach 90% or more; a test that only simulates the transmitter output reaches much less, because failures of the sensing element are not exercised."
  - q: What is the PFDavg formula with proof test coverage?
    a: "For a 1oo1 function, PFDavg ≈ PTC × λDU × TI ÷ 2 + (1 − PTC) × λDU × MT ÷ 2. The first term is the part the proof test finds every TI; the second is the part that stays hidden until the mission time MT, when the device is overhauled or replaced."
  - q: Why does mission time matter so much?
    a: "Failures the proof test cannot find build up for the whole mission time, not just one test interval. With 10% of λDU missed and a 15 year mission time, the hidden part alone averages 0.1 × 15 ÷ 2 = 0.75 years of exposure, which is more than the 0.45 years from the tested part with a 1 year interval."
  - q: Can I make up for low coverage by testing more often?
    a: "Only partly. Testing more often shrinks the first term, but the second term, (1 − PTC) × λDU × MT ÷ 2, does not depend on the test interval. Once it dominates, the only fixes are a better test procedure, a shorter overhaul interval or a device with a lower λDU."
  - q: Does a partial stroke test count as a proof test?
    a: "A partial stroke test is a partial proof test with limited coverage of the valve failures, typically 50 to 80% of the valve λDU. It is modelled as an extra test with its own interval and coverage, and the full stroke proof test is still needed for the rest."
  - q: What proof test coverage should I assume if the vendor gives none?
    a: "Do not assume 100%. Many SIL verifications use 90% for a well written end to end procedure and lower values for partial tests, but the figure should come from a failure mode review of the actual test steps, as IEC 61511 asks."
related: [engineering/pfd-avg, engineering/safe-failure-fraction, engineering/availability-mtbf, engineering/weibull-reliability, statistics/exponential-distribution]
''', f'''
## How to use the proof test coverage calculator

Enter the **dangerous undetected failure rate** λDU of the safety function in FIT, the **proof test interval** in years, the **proof test coverage** of your test procedure and the **mission time**, which is when the failures the test misses are finally found: at overhaul, replacement or the end of the plant life. The calculator gives PFDavg with the imperfect test, PFDavg if the test were perfect, how many times worse the imperfect test is, the risk reduction factor and the SIL band that PFDavg supports. To find the coverage you need for a target PFDavg, enter the target and press × on proof test coverage.

## PFDavg formula with proof test coverage

<p class="formula">PFD<sub>avg</sub> ≈ PTC × λ<sub>DU</sub> × TI ÷ 2 + (1 − PTC) × λ<sub>DU</sub> × MT ÷ 2</p>

λ<sub>DU</sub> is in failures per hour (FIT × 10<sup>−9</sup>), and TI and MT are in hours (years × 8,760). The first term is the familiar 1oo1 result for the failures the test reveals; the second treats the unrevealed failures as if their only "test" were the mission time. With PTC = 100% the formula reduces to λ<sub>DU</sub> × TI ÷ 2, the [PFDavg calculation formula](ib:pfdavg-calculation-formula) for a perfect test. The simplified form is valid while λ<sub>DU</sub> × MT is small (well below 0.1); it ignores repair time and common cause, which matter for redundant architectures.

## Worked example

A 1oo1 safety function has λDU = **{pL:g} FIT**, is proof tested every **{pT:g} year** with a procedure judged to cover **{pC*100:g}%** of dangerous undetected failures, and is overhauled at the end of a **{pM:g} year** mission time:

- λDU = {pL:g} × 10⁻⁹ = {lam_h*1e7:.0f} × 10⁻⁷ per hour
- Tested part = {pC:g} × {lam_h*1e7:.0f} × 10⁻⁷ × {pT*8760:,.0f} h ÷ 2 = **{part1:.6f}**
- Hidden part = {1-pC:.1f} × {lam_h*1e7:.0f} × 10⁻⁷ × {pM*8760:,.0f} h ÷ 2 = **{part2:.6f}**
- PFDavg = {part1:.6f} + {part2:.6f} = **{PT['pfd']:.6f}**, RRF = **{PT['rrf']:.0f}**, so the function is in the **SIL {PT['sil']}** band
- With a perfect test PFDavg would be **{PT['pfp']:.6f}**, so the imperfect test makes it **{PT['ratio']:.2f} times** higher

To bring PFDavg below 0.005 without changing the overhaul interval, the coverage must rise to **{c_need*100:.1f}%**. The largest λDU that still meets SIL 2 (PFDavg below 0.01) with this test regime is **{lam_max:,.0f} FIT**.

## PFDavg by coverage and mission time

For λDU = {pL:g} FIT and a {pT:g} year proof test interval. The 100% row is the perfect test and does not depend on mission time:

| Proof test coverage | MT 5 years | MT 10 years | MT 15 years | MT 20 years |
|---|---|---|---|---|
{pt_rows}
## Typical proof test coverage values

These ranges are typical of published SIL verification practice and manufacturer safety manuals; always use the coverage stated for your device and test procedure:

| Test | Typical coverage |
|---|---|
{cov_rows}
## How coverage is handled in practice

IEC 61511 asks that proof test procedures are written for each safety function, and that the SIL verification uses realistic assumptions about what they reveal. The usual workflow is to list the dangerous undetected failure modes of each device from its FMEDA, mark which ones each test step exercises, and add up the λDU of the covered modes to get PTC. A pressure transmitter test that only injects a current at the logic solver input never checks a plugged impulse line or a drifted sensor, so its coverage is low; applying a real pressure at the transmitter is much better. For final elements, a full stroke with a tight shutoff check finds most failures, while a partial stroke test covers only the sticking modes.

The mission time term also explains why overhaul matters. A valve that is never fully refurbished carries its untestable failures for the whole plant life, so many operators set an overhaul or replacement interval for safety valves and include it as MT. In this example the hidden part alone is {part2:.6f}, already more than the perfect test PFDavg of {PT['pfp']:.6f}, so no proof test interval, however short, can bring the function back to the perfect test figure.

## Common mistakes

- **Assuming 100% coverage.** Most SIL calculations that ignore coverage are optimistic. At {pC*100:g}% coverage and {pM:g} years, PFDavg is {PT['ratio']:.1f} times the perfect test figure.
- **Using the proof test interval as the mission time.** MT is when the hidden failures are found, often 10 to 20 years, not the test interval.
- **Counting diagnostic coverage as proof test coverage.** Online diagnostics already move failures from λDU to λDD. Proof test coverage applies to what is left in λDU.
- **Shortening TI to fix a coverage problem.** The hidden term does not depend on TI, so testing monthly cannot cure a poor test procedure.
- **Taking coverage from a generic table without checking the procedure.** A test that skips the leak check or uses a simulated signal must be credited with the lower figure.
''')

# ---------------------------------------------------------------- Decoupling capacitor
def dec(dI, dV, dt, Cd, ESL):
    C = dI * dt / dV
    Zt = dV / dI
    fs = 1 / (2 * pi * math.sqrt(ESL * Cd))
    fL = Zt / (2 * pi * ESL)
    return dict(C=C, Zt=Zt, fs=fs, fL=fL)
dI0, dV0, dt0, Cd0, L0 = 0.5, 0.033, 2e-6, 100e-9, 0.5e-9
DC = dec(dI0, dV0, dt0, Cd0, L0)
# SRF table: capacitor values x typical mounted ESL
srf_rows = ''
for c, lab in ((10e-9, '10 nF'), (100e-9, '100 nF'), (1e-6, '1 µF'), (4.7e-6, '4.7 µF'), (10e-6, '10 µF'), (47e-6, '47 µF')):
    srf_rows += f"| {lab} | " + ' | '.join(f"{1/(2*pi*math.sqrt(l*c))/1e6:.1f} MHz" for l in (0.4e-9, 0.6e-9, 1.0e-9, 2.0e-9)) + " |\n"
# required C table
need_rows = ''
for dI, dV, dt, case in ((0.1, 0.05, 1e-6, '0.1 A step, 50 mV droop, 1 µs'),
                         (0.5, 0.033, 2e-6, '0.5 A step, 33 mV droop (1% of 3.3 V), 2 µs'),
                         (1.0, 0.05, 5e-6, '1 A step, 50 mV droop, 5 µs'),
                         (2.0, 0.018, 1e-6, '2 A step, 18 mV droop (1.5% of 1.2 V), 1 µs'),
                         (5.0, 0.05, 10e-6, '5 A step, 50 mV droop, 10 µs')):
    need_rows += f"| {case} | {dV/dI*1000:.1f} mΩ | {dI*dt/dV*1e6:.1f} µF |\n"
# parallel caps needed so the combined ESL stays below Zt at 100 MHz
f100 = 100e6
n100 = math.ceil(2 * pi * f100 * L0 / DC['Zt'])
# ESR check: a 10 uF ceramic of 5 mOhm vs Zt
Xc1M = 1 / (2 * pi * 1e6 * DC['C'])

P('electronics', 'decoupling-capacitor', f'''
title: Decoupling Capacitor Calculator (Bulk Capacitance and SRF)
description: Calculate the decoupling capacitance for a load current step and allowed voltage droop, the target impedance and a capacitor's self resonant frequency.
category: electronics
{intro("A decoupling capacitor supplies sudden load current locally so the supply rail does not dip while the regulator catches up. This decoupling capacitor calculator finds the capacitance for a current step, droop limit and hold time, the target impedance, and a capacitor's self resonant frequency, as explained in [how decoupling capacitors work](ib:how-decoupling-capacitors-work).",
       "Hardware and PCB designers use it to size bulk and local capacitors for microcontrollers, FPGAs and ADCs, and to check that the capacitors chosen still act as capacitors at the frequencies that matter.", 'decoupling capacitor calculator')}
keywords: [decoupling capacitor calculator, decoupling capacitor value, bypass capacitor calculator, bulk capacitor calculation, target impedance pdn, capacitor self resonant frequency, esl capacitor, decoupling capacitance formula]
published: {D}
updated: {D}
variables:
  - {{ id: dI, label: Load current step (ΔI), family: current, unit: A, default: {dI0:g}, min: 0 }}
  - {{ id: dV, label: Allowed voltage droop (ΔV), family: voltage, unit: mV, default: {dV0*1000:g}, min: 0, help: 'Often 1 to 5% of the rail voltage, from the device datasheet.' }}
  - {{ id: dt, label: Time the capacitor must supply the step (Δt), family: seconds, unit: us, default: {dt0*1e6:g}, min: 0, help: 'Roughly the time the regulator needs to respond: about 1 ÷ (4 × loop bandwidth) for a switching regulator, or the hold-up time required.' }}
  - {{ id: C, label: Required decoupling capacitance, family: capacitance, unit: uF, min: 0 }}
  - {{ id: Zt, label: Target impedance of the supply network, family: resistance, unit: mohm, min: 0 }}
  - {{ id: Cd, label: Value of one decoupling capacitor (for the SRF check), family: capacitance, unit: nF, default: {Cd0*1e9:g}, min: 0 }}
  - {{ id: ESL, label: Mounted ESL of that capacitor (with vias), family: inductance, unit: nH, default: {L0*1e9:g}, min: 0, help: 'Typical mounted values: 0402 about 0.4 to 0.6 nH, 0603 about 0.6 to 0.9 nH, 0805 about 0.8 to 1.2 nH, through-hole electrolytic several nH.' }}
  - {{ id: fs, label: Self resonant frequency of the capacitor, family: frequency, unit: MHz, min: 0 }}
  - {{ id: fL, label: Frequency where its ESL reactance reaches the target impedance, family: frequency, unit: MHz, min: 0 }}
equations:
  - C = dI * dt / dV
  - Zt = dV / dI
  - fs = 1 / (2 * pi * sqrt(ESL * Cd))
  - fL = Zt / (2 * pi * ESL)
faq:
  - q: How do I calculate the decoupling capacitor value?
    a: "From the charge the capacitor must deliver: C = ΔI × Δt ÷ ΔV. A 0.5 A step that must be supplied for 2 µs with no more than 33 mV droop needs 0.5 × 2 µs ÷ 0.033 V = 30.3 µF of effective capacitance."
  - q: Why use 100 nF decoupling capacitors?
    a: "100 nF in a small package is a long standing compromise: enough charge for the fast edges of a logic IC and a self resonant frequency in the tens of MHz. Its value matters less than its mounted inductance; a 100 nF in 0402 with short vias outperforms a larger value on long traces."
  - q: What is the self resonant frequency of a capacitor?
    a: "It is the frequency where the capacitor's reactance and its equivalent series inductance cancel: f = 1 ÷ (2π√(ESL × C)). Below it the part behaves as a capacitor; above it, as an inductor whose impedance rises with frequency, and only the ESR remains at resonance."
  - q: What is target impedance in power distribution design?
    a: "It is the highest impedance the supply network may have at any frequency so that the expected current step causes no more than the allowed ripple: Z = ΔV ÷ ΔI. Designers keep the combined impedance of regulator, bulk, ceramic and plane capacitance below it up to the frequency of the load current edges."
  - q: Should I use several values of decoupling capacitor in parallel?
    a: "Mixing values spreads the resonances, but parallel resonance peaks can appear between them. Many designers now prefer several capacitors of the same small package and value, which lowers the total ESL without creating anti resonances, plus bulk capacitance near the regulator."
  - q: Does DC bias reduce decoupling capacitance?
    a: "Yes, for class II ceramics such as X5R and X7R. A 10 µF 6.3 V capacitor in 0603 can lose half or more of its capacitance at 3.3 V, so check the manufacturer's DC bias curve and size the effective capacitance, not the marked value."
related: [electronics/resonant-frequency, electronics/reactance, electronics/capacitors-series-parallel, electronics/capacitor-energy, electronics/buck-converter, electronics/lm317]
''', f'''
## How to use the decoupling capacitor calculator

Enter the **load current step**, the **allowed voltage droop** and the **time the capacitors must supply the step** before the regulator responds. The calculator gives the capacitance needed and the target impedance of the supply network. In the second part, enter the **value and mounted ESL of one decoupling capacitor** to get its self resonant frequency, and the frequency above which a single capacitor's inductance alone exceeds the target impedance. To find the largest current step a given capacitance can handle, enter the capacitance and press × on the current step.

## Decoupling capacitor formulas

<p class="formula">C = ΔI × Δt ÷ ΔV &nbsp;·&nbsp; Z<sub>t</sub> = ΔV ÷ ΔI</p>

<p class="formula">f<sub>SRF</sub> = 1 ÷ (2π √(ESL × C)) &nbsp;·&nbsp; f<sub>L</sub> = Z<sub>t</sub> ÷ (2π × ESL)</p>

The first formula is the charge balance Q = C × ΔV: the capacitor supplies ΔI for Δt and its voltage falls by ΔV. The SRF formula is the series LC resonance of the capacitor and its mounting inductance. Above f<sub>L</sub> the inductive reactance 2πf × ESL of one capacitor is already larger than Z<sub>t</sub>, so more capacitors in parallel, or a lower inductance layout, are needed.

## Worked example

A 3.3 V rail feeds a microcontroller whose current jumps by **{dI0:g} A** when it wakes up. The droop must stay within 1% (**{dV0*1000:g} mV**) and the switching regulator needs about **{dt0*1e6:g} µs** to respond:

- Required capacitance C = {dI0:g} × {dt0*1e6:g} × 10⁻⁶ ÷ {dV0:g} = **{DC['C']*1e6:.1f} µF**
- Target impedance Z<sub>t</sub> = {dV0:g} ÷ {dI0:g} = **{DC['Zt']*1000:.0f} mΩ**
- One {Cd0*1e9:g} nF capacitor with {L0*1e9:g} nH mounted ESL resonates at 1 ÷ (2π √({L0*1e9:g} × 10⁻⁹ × {Cd0*1e9:g} × 10⁻⁹)) = **{DC['fs']/1e6:.1f} MHz**
- Its ESL reactance reaches {DC['Zt']*1000:.0f} mΩ at {DC['Zt']:.3f} ÷ (2π × {L0*1e9:g} × 10⁻⁹) = **{DC['fL']/1e6:.1f} MHz**

A practical choice is a 47 µF bulk capacitor near the regulator (leaving margin for DC bias derating) plus 100 nF ceramics at each supply pin. To hold {DC['Zt']*1000:.0f} mΩ up to 100 MHz with {L0*1e9:g} nH parts, about {n100} capacitors in parallel are needed, because their inductances combine like parallel resistors. At 1 MHz the {DC['C']*1e6:.1f} µF bulk has a reactance of only {Xc1M*1000:.1f} mΩ, well under the target.

## Self resonant frequency by value and mounted ESL

Computed from f = 1 ÷ (2π√(LC)). The ESL columns are typical mounted values (capacitor plus pads and vias): about 0.4 nH for a 0402 with via in pad, 0.6 nH for 0603, 1 nH for 0805 and 2 nH for a long trace or larger case:

| Capacitance | ESL 0.4 nH | ESL 0.6 nH | ESL 1.0 nH | ESL 2.0 nH |
|---|---|---|---|---|
{srf_rows}
## Capacitance needed for common load steps

| Load step, droop and hold time | Target impedance | Capacitance needed |
|---|---|---|
{need_rows}
## How decoupling is designed in practice

A power distribution network is built in layers. The regulator itself holds the rail at low frequency, up to its loop bandwidth. **Bulk capacitors** (tens to hundreds of µF, electrolytic, polymer or large ceramics) cover the gap from there up to a few hundred kHz, and this is the capacitance the first formula sizes. **Local ceramic capacitors** of 100 nF to 1 µF at each supply pin cover the range up to tens of MHz, and above that only the **plane capacitance** of closely spaced power and ground planes and the capacitance inside the IC package help.

Layout decides how well the local capacitors work. The loop from the capacitor through its vias to the IC pin and back sets the mounted ESL, which is usually larger than the capacitor's own ESL. Place the capacitor on the same side as the IC, as close to the pin as possible, with the vias right at the pads, and connect straight into solid planes rather than through thin traces.

## Common mistakes

- **Using the marked value of a ceramic.** DC bias and temperature can remove half the capacitance of an X5R part; size for the effective value.
- **Ignoring ESL.** Adding a larger value does not help at high frequency if it sits on a long trace; above its SRF a capacitor is an inductor.
- **Forgetting ESR on bulk capacitors.** An electrolytic with 100 mΩ ESR already drops 50 mV at a 0.5 A step, more than the {dV0*1000:g} mV budget in this example, before any capacitance is used.
- **Taking Δt too short.** If the regulator responds in 10 µs but Δt is entered as 1 µs, the bulk capacitance comes out ten times too small.
- **Placing all capacitors far from the load.** Bulk capacitance near the regulator does nothing for the fast edges at the IC pins.
''')

print('done', DONE)

# ======================================================================= SECTION _batch_a3.py
"""Batch 2026-11-16 slice A3: chemistry (molar flow rate, CSTR and PFR reactor conversion).
All reference tables and worked examples are computed here from the calculator defaults."""
import sys, math, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro as _intro
D = '2026-11-16'
R = 8.314462618
DASH = re.compile('[' + chr(0x2013) + chr(0x2014) + ']')
DONE = []


def intro(p1, p2, phrase):
    assert phrase.lower() in p1.lower(), phrase
    t = p1 + '\n\n' + p2
    plain = re.sub(r'\]\(ib:[a-z0-9-]+\)', ']', t)
    n = len(plain.split())
    assert 60 <= n <= 90, (phrase, n)
    return _intro(t)


def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    assert 'featured' not in fm
    assert not DASH.search(fm) and not DASH.search(body), slug
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    n = len(body.split())
    assert n >= 520, (slug, n)
    page(cat, slug, fm, body)
    DONE.append(f'{cat}/{slug}')


# ======================================================================= Molar flow rate
AW = dict(H=1.008, C=12.011, N=14.007, O=15.999, S=32.06, Cl=35.45, Ar=39.948)
def mm(f):
    return sum(AW[el] * (int(c) if c else 1) for el, c in re.findall(r'([A-Z][a-z]?)(\d*)', f))
Vn = R * 273.15 / 101325 * 1000          # m3/kmol at 0 C, 1 atm
Vs = R * 288.15 / 101325 * 1000          # 15 C, 1 atm
V20 = R * 293.15 / 101325 * 1000         # 20 C, 1 atm
mF, mM, mT, mP, mZ = 500.0, round(mm('N2'), 3), 25.0, 6.0, 1.0
mn = mF / mM                              # kmol/h
mQ = mn * 1000 / 3600 * mZ * R * (mT + 273.15) / (mP * 1e5) * 3600   # m3/h actual
mQn = mn * Vn
mQs = mn * Vs
mns = mn * 1000 / 3600                    # mol/s
gas_rows = ''
for nm, f in (('Hydrogen', 'H2'), ('Methane', 'CH4'), ('Ammonia', 'NH3'), ('Water vapour', 'H2O'), ('Nitrogen', 'N2'),
              ('Carbon monoxide', 'CO'), ('Oxygen', 'O2'), ('Hydrogen sulphide', 'H2S'), ('Argon', 'Ar'),
              ('Carbon dioxide', 'CO2'), ('Propane', 'C3H8'), ('Sulphur dioxide', 'SO2'), ('Chlorine', 'Cl2')):
    M = mm(f)
    sub = re.sub(r'(\d)', lambda m: chr(0x2080 + int(m.group(1))), f)
    gas_rows += f"| {nm} | {sub} | {M:.3f} | {1000/M:.2f} | {1000/M*Vn:,.1f} | {M/Vn:.4f} |\n"
gas_rows += f"| Air (dry) | mixture | 28.965 | {1000/28.965:.2f} | {1000/28.965*Vn:,.1f} | {28.965/Vn:.4f} |\n"
mv_rows = ''
for lab, T, Pp in (('Normal (DIN 1343), 0 °C and 1.01325 bar', 273.15, 101325), ('Standard (ISO 13443), 15 °C and 1.01325 bar', 288.15, 101325),
                   ('20 °C and 1.01325 bar', 293.15, 101325), ('IUPAC STP, 0 °C and 1 bar', 273.15, 100000),
                   ('60 °F and 14.696 psia (US gas industry)', 288.7056, 101325)):
    v = R * T / Pp * 1000
    mv_rows += f"| {lab} | {v:.3f} m³/kmol | {v/0.028316846592/2.20462262:.1f} ft³/lb-mol |\n"
# mixture example: 100 kmol/h of 80% CH4 + 20% CO2 (mole basis)
mixM = 0.8 * mm('CH4') + 0.2 * mm('CO2')
mixm = 100 * mixM
# pressure effect: actual volume at 1, 6, 20 bar
pr_rows = ''
for pb in (1.01325, 2, 6, 10, 20, 40):
    q = mn * 1000 / 3600 * R * (mT + 273.15) / (pb * 1e5) * 3600
    pr_rows += f"| {pb:g} bar(a) | {q:,.2f} m³/h | {mQn/q:.2f} |\n"

P('chemistry', 'molar-flow-rate', f'''
title: Molar Flow Rate Calculator (Mass, Molar and Gas Volume Flow)
description: Convert mass flow to molar flow in kmol/h and mol/s, then to actual gas volume flow and Nm³/h or Sm³/h using the ideal gas law and molar volume.
category: chemistry
{intro("Molar flow rate is the number of moles passing a point per unit time, the basis of every reaction and material balance. This molar flow rate calculator converts a mass flow and molar mass into kmol/h and mol/s, and for a gas into actual, normal and standard volume flow, as discussed in [actual, standard and normal flow](ib:actual-flow-standard-flow-normal-flow).",
       "Chemical and process engineers use it to write stream tables and check stoichiometry, and instrument engineers use it to compare mass, volumetric and normalised flow meter readings.", 'molar flow rate calculator')}
keywords: [molar flow rate calculator, mass flow to molar flow, kmol/h to kg/h, molar flow to volumetric flow, kmol/h to Nm3/h, mol/s calculator, molar flow formula]
published: {D}
updated: {D}
variables:
  - {{ id: m, label: Mass flow rate, family: massflow, unit: kgh, imperialUnit: lbh, default: {mF:g}, min: 0 }}
  - {{ id: M, label: Molar mass, suffix: g/mol (kg/kmol), default: {mM:g}, min: 0, help: 'N₂ 28.014, air 28.965, O₂ 31.998, CO₂ 44.009, CH₄ 16.043, H₂ 2.016, H₂O 18.015. For a mixture use the mole-weighted average.' }}
  - {{ id: T, label: Actual gas temperature, family: temperature, unit: C, imperialUnit: F, default: {mT:g} }}
  - {{ id: Pa, label: Actual absolute pressure, family: pressure, unit: bar, imperialUnit: psi, default: {mP:g}, min: 0, help: 'Absolute = gauge + atmospheric (1.01325 bar at sea level).' }}
  - {{ id: Z, label: Compressibility factor Z, default: {mZ:g}, min: 0, decimals: 4, help: '1 for an ideal gas. Only affects the actual volume flow.' }}
  - {{ id: n, label: Molar flow rate, suffix: kmol/h, min: 0, decimals: 4 }}
  - {{ id: ns, label: Molar flow rate, suffix: mol/s, min: 0, decimals: 4 }}
  - {{ id: Q, label: Actual volume flow at T and P, family: flow, unit: m3h, imperialUnit: cfm, min: 0 }}
  - {{ id: Qn, label: Normal volume flow (0 °C and 1.01325 bar), suffix: Nm³/h, min: 0 }}
  - {{ id: Qs, label: Standard volume flow (15 °C and 1.01325 bar), suffix: Sm³/h, min: 0 }}
equations:
  - n = m * 3600 / M
  - ns = n / 3.6
  - Q = ns * Z * 8.314462618 * T / Pa
  - Qn = n * 8.314462618 * 273.15 / 101.325
  - Qs = n * 8.314462618 * 288.15 / 101.325
faq:
  - q: How do I convert mass flow to molar flow?
    a: "Divide the mass flow by the molar mass: ṅ = ṁ ÷ M. Because 1 kmol of a substance has a mass of M kg, kg/h divided by kg/kmol gives kmol/h. For example, 500 kg/h of nitrogen (M = 28.014) is {mn:.3f} kmol/h, or {mns:.3f} mol/s."
  - q: How do I convert kmol/h to Nm³/h?
    a: "Multiply by the molar volume at normal conditions, {Vn:.3f} Nm³/kmol at 0 °C and 1.01325 bar. So 1 kmol/h of any ideal gas is {Vn:.3f} Nm³/h. At standard conditions of 15 °C the factor is {Vs:.3f} Sm³/kmol, which is why the same molar flow gives a Sm³/h figure about 5.5% higher."
  - q: Why is molar flow used instead of mass flow in reaction balances?
    a: "Chemical equations balance in moles, not kilograms. One mole of methane reacts with two moles of oxygen whatever their masses, so converting each stream to kmol/h makes stoichiometric ratios, excess air and conversion direct to read. Mass is conserved too, but moles show what actually reacts."
  - q: Does pressure change the molar flow rate?
    a: "No. Molar flow, like mass flow, is the same at any pressure and temperature along a pipe at steady state. Only the actual volume flow changes: doubling the absolute pressure halves the actual m³/h, while kmol/h, kg/h and Nm³/h stay the same."
  - q: How do I find the molar mass of a gas mixture?
    a: "Take the mole-fraction weighted average: M = Σ yᵢ Mᵢ. A biogas of 80 mol% methane and 20 mol% CO₂ has M = 0.8 × {mm('CH4'):.3f} + 0.2 × {mm('CO2'):.3f} = {mixM:.3f} g/mol. If you know mass fractions wᵢ instead, use 1 ÷ M = Σ wᵢ ÷ Mᵢ."
related: [engineering/mass-flow-rate, engineering/gas-flow-correction, chemistry/gas-density, chemistry/moles, physics/ideal-gas-law, chemistry/combustion-air]
''', f'''
## How to use the molar flow rate calculator

Enter the **mass flow rate** and the **molar mass** of the stream. The calculator returns the molar flow in kmol/h and mol/s. For a gas, also enter the **actual temperature**, the **absolute pressure** and, if you know it, the **compressibility factor Z**; the calculator then gives the actual volume flow at line conditions and the normal (Nm³/h) and standard (Sm³/h) volume flows. For a liquid, ignore the gas results. To go the other way, enter a molar flow and press × on the mass flow so that it becomes the result.

## Molar flow rate formula

<p class="formula">ṅ = ṁ ÷ M</p>

<p class="formula">Q<sub>actual</sub> = ṅ Z R T ÷ P &nbsp;·&nbsp; Q<sub>N</sub> = ṅ × {Vn:.3f} m³/kmol &nbsp;·&nbsp; Q<sub>S</sub> = ṅ × {Vs:.3f} m³/kmol</p>

ṁ is the mass flow, M the molar mass in kg/kmol (numerically equal to g/mol), R = 8.314462618 J/(mol·K), T the absolute temperature in kelvin and P the absolute pressure in Pa. The molar volumes come from the same law: V<sub>m</sub> = R T ÷ P = 8.314462618 × 273.15 ÷ 101,325 = {Vn/1000:.6f} m³/mol at 0 °C.

## Worked example

Nitrogen flows at **{mF:g} kg/h** (M = {mM:g} g/mol) at **{mT:g} °C** and **{mP:g} bar(a)**, treated as an ideal gas (Z = 1):

- Molar flow = {mF:g} ÷ {mM:g} = **{mn:.4f} kmol/h**
- In SI units = {mn:.4f} × 1,000 ÷ 3,600 = **{mns:.4f} mol/s**
- Actual volume flow = {mns:.4f} × 8.314462618 × {mT+273.15:.2f} ÷ {mP*1e5:,.0f} = {mQ/3600:.6f} m³/s = **{mQ:.2f} m³/h**
- Normal volume flow = {mn:.4f} × {Vn:.3f} = **{mQn:.2f} Nm³/h**
- Standard volume flow = {mn:.4f} × {Vs:.3f} = **{mQs:.2f} Sm³/h**

The pipe carries only {mQ:.1f} m³/h of real gas, but the same gas would fill {mQn:.1f} m³/h at normal conditions, about {mQn/mQ:.1f} times more.

## Molar masses of common gases

Computed from IUPAC standard atomic weights. The last two columns give the molar flow and normal volume flow for 1,000 kg/h, and the ideal gas density at 0 °C and 1.01325 bar:

| Gas | Formula | M (g/mol) | kmol/h per 1,000 kg/h | Nm³/h per 1,000 kg/h | ρ<sub>N</sub> (kg/Nm³) |
|---|---|---|---|---|---|
{gas_rows}
## Molar volume at common reference conditions

Every ideal gas occupies the same volume per mole at a given temperature and pressure, so the reference condition must always be stated with a "normal" or "standard" flow:

| Reference condition | Molar volume | Imperial |
|---|---|---|
{mv_rows}
## Effect of pressure on actual volume flow

For the {mF:g} kg/h nitrogen example at {mT:g} °C. Molar, mass and normal flows are unchanged; only the actual volume changes:

| Absolute pressure | Actual volume flow | Nm³/h per actual m³/h |
|---|---|---|
{pr_rows}
## How molar flow is used in practice

Process design starts with a **stream table** in kmol/h, because reactor feeds, combustion air and absorber gas rates are all set by mole ratios. Instruments rarely measure moles directly: a **Coriolis meter** gives kg/h, a **thermal mass meter** is usually calibrated in Nm³/h of a reference gas, and a **DP, vortex or turbine meter** gives actual volume flow that must be corrected for pressure and temperature. Converting each reading to kmol/h puts them on the same footing, which is how plant engineers reconcile meters around a unit and spot a drifting transmitter. For a mixture, work out the average molar mass from the gas analysis first; a change in composition changes the kmol/h for the same kg/h.

## Common mistakes

- **Using gauge pressure.** The gas law needs absolute pressure. Entering 5 bar(g) as 5 bar instead of {5+1.01325:.5g} bar(a) overstates the actual volume flow by {(6.01325/5-1)*100:.0f}%.
- **Mixing up normal and standard.** Nm³ at 0 °C and Sm³ at 15 °C differ by {(Vs/Vn-1)*100:.1f}%, and some companies use 20 °C or 60 °F. Always state the reference.
- **Using °C in the gas law.** T must be in kelvin; 25 °C is 298.15 K, not 25.
- **Averaging molar masses by mass fraction.** For a mixture, M is the mole-fraction weighted average; weighting by mass fraction gives the wrong value whenever the components have different molar masses.
- **Applying Z to normal flow.** At 0 °C and 1 atm most gases are close to ideal, so Z mainly corrects the actual volume at high pressure; use the Z at line conditions.
''')


# ======================================================================= Reactor conversion
def rc(V, v0, k, CA0):
    tau = V / v0                     # h
    Da = k * tau
    Xc = Da / (1 + Da)
    Xp = 1 - math.exp(-Da)
    return dict(tau=tau, Da=Da, Xc=Xc, Xp=Xp, Cc=CA0 * (1 - Xc), Cp=CA0 * (1 - Xp), r=(math.exp(Da) - 1) / Da)
rV, rv0, rk, rC = 2.0, 4.0, 1.5, 2.0
RC = rc(rV, rv0, rk, rC)
da_rows = ''
for Da in (0.1, 0.25, 0.5, 1, 2, 3, 5, 10):
    da_rows += f"| {Da:g} | {Da/(1+Da)*100:.1f}% | {(1-math.exp(-Da))*100:.1f}% | {(math.exp(Da)-1)/Da:.2f} |\n"
vr_rows = ''
for X in (0.5, 0.8, 0.9, 0.95, 0.99, 0.999):
    dc = X / (1 - X); dp = -math.log(1 - X)
    vr_rows += f"| {X*100:g}% | {dc:.2f} | {dp:.3f} | {dc/dp:.2f} |\n"
# tanks in series for 90% conversion: N (1/(1-X))^(1/N) - N ... Da_total = N((1-X)^(-1/N) - 1)
ts_rows = ''
for N in (1, 2, 3, 5, 10):
    dt = N * ((1 - 0.9) ** (-1 / N) - 1)
    ts_rows += f"| {N} | {dt:.3f} | {dt/math.log(10):.2f} |\n"
ts_rows += f"| PFR (N → ∞) | {math.log(10):.3f} | 1.00 |\n"
# example target: k tau needed for 90%
tgtX = 0.9
tauC = tgtX / (1 - tgtX) / rk
tauP = -math.log(1 - tgtX) / rk

P('chemistry', 'reactor-conversion', f'''
title: Reactor Conversion Calculator (CSTR and PFR, First Order)
description: Find first order conversion in a CSTR and a PFR from reactor volume, feed flow and rate constant, with space time, Damköhler number and outlet concentrations.
category: chemistry
{intro("Conversion is the fraction of a reactant used up in a reactor. This reactor conversion calculator finds the space time, the Damköhler number and the first order conversion in a continuous stirred tank (CSTR) and in a plug flow reactor (PFR) of the same volume, with the outlet concentration for each.",
       "Chemical engineering students use it for reactor design problems, and process engineers use it to estimate how far a throughput increase or a cooler reactor will cut conversion.", 'reactor conversion calculator')}
keywords: [reactor conversion calculator, cstr conversion calculator, pfr conversion calculator, first order reaction conversion, space time reactor, damkohler number, cstr vs pfr volume]
published: {D}
updated: {D}
variables:
  - {{ id: V, label: Reactor volume (reacting volume), family: volume, unit: m3, imperialUnit: galUS, default: {rV:g}, min: 0 }}
  - {{ id: v0, label: Volumetric feed flow rate, family: flow, unit: m3h, imperialUnit: gpm, default: {rv0:g}, min: 0 }}
  - {{ id: k, label: First order rate constant k, suffix: 1/h, default: {rk:g}, min: 0, help: 'Multiply a per-minute constant by 60, or a per-second constant by 3,600. k depends strongly on temperature (Arrhenius).' }}
  - {{ id: CA0, label: Feed concentration of A, suffix: mol/L, default: {rC:g}, min: 0 }}
  - {{ id: tau, label: Space time τ = V ÷ v₀, family: seconds, unit: h, min: 0 }}
  - {{ id: Da, label: Damköhler number k τ, min: 0, decimals: 4 }}
  - {{ id: Xc, label: Conversion in a CSTR, family: percent, unit: '%', min: 0 }}
  - {{ id: Xp, label: Conversion in a PFR, family: percent, unit: '%', min: 0 }}
  - {{ id: Cc, label: Outlet concentration from the CSTR, suffix: mol/L, min: 0, decimals: 4 }}
  - {{ id: Cp, label: Outlet concentration from the PFR, suffix: mol/L, min: 0, decimals: 4 }}
  - {{ id: rV, label: CSTR volume needed to match the PFR conversion (ratio), suffix: × PFR volume, min: 0, decimals: 3 }}
equations:
  - tau = V / v0
  - Da = k * tau / 3600
  - Xc = Da / (1 + Da)
  - Xp = 1 - exp(-Da)
  - Cc = CA0 * (1 - Xc)
  - Cp = CA0 * (1 - Xp)
  - rV = (exp(Da) - 1) / Da
faq:
  - q: Why does a PFR give higher conversion than a CSTR of the same volume?
    a: "A CSTR is perfectly mixed, so the whole tank reacts at the low outlet concentration. In a PFR the concentration falls gradually along the length, so most of the volume reacts at a higher concentration and therefore a higher first order rate. For any positive order the PFR needs less volume for the same conversion."
  - q: What is the Damköhler number?
    a: "For a first order reaction Da = k τ, the ratio of the residence time to the reaction time 1 ÷ k. Da well below 1 means the fluid leaves before much reacts; Da of 1 gives 50% in a CSTR and 63.2% in a PFR; Da above about 5 gives high conversion in either reactor."
  - q: How do I find the space time for a target conversion?
    a: "Rearrange the design equation. CSTR: τ = X ÷ (k (1 − X)). PFR: τ = −ln(1 − X) ÷ k. For 90% conversion with k = {rk:g} per hour, the CSTR needs τ = {tauC:.2f} h and the PFR τ = {tauP:.3f} h. Multiply by the feed flow to get the volume."
  - q: Is space time the same as residence time?
    a: "Only when the density does not change through the reactor, which is the case for most liquid phase reactions and is assumed here. For gas reactions that change the number of moles, or for large temperature changes, the actual mean residence time differs from V ÷ v₀ measured at feed conditions."
  - q: Why use several CSTRs in series?
    a: "Each tank works at a lower concentration than the one before, so a chain of tanks approaches plug flow. For 90% first order conversion, one CSTR needs Da = 9, two in series need a total of {2*((0.1)**-0.5-1):.2f}, and ten need {10*((0.1)**-0.1-1):.2f}, close to the PFR value of {math.log(10):.3f}."
related: [engineering/residence-time, chemistry/integrated-rate-law, chemistry/arrhenius-equation, chemistry/half-life, chemistry/activation-energy, chemistry/percent-yield]
''', f'''
## How to use the reactor conversion calculator

Enter the **reacting volume**, the **volumetric feed flow**, the **first order rate constant** k in reciprocal hours and the **feed concentration** of the reactant. The calculator gives the space time, the Damköhler number, the conversion and outlet concentration for an ideal CSTR and for an ideal PFR of that volume, and how many times larger a CSTR must be to match the PFR conversion. To size a reactor for a target conversion, enter the conversion and press × on the volume so that it becomes the result.

## Reactor conversion formulas

For an irreversible first order reaction A → products, isothermal, at constant density:

<p class="formula">τ = V ÷ v₀ &nbsp;·&nbsp; Da = k τ</p>

<p class="formula">CSTR: X = Da ÷ (1 + Da) &nbsp;·&nbsp; PFR: X = 1 − e<sup>−Da</sup> &nbsp;·&nbsp; C<sub>A</sub> = C<sub>A0</sub> (1 − X)</p>

These follow from the design equations V = F<sub>A0</sub> X ÷ (−r<sub>A</sub>) for the CSTR and V = F<sub>A0</sub> ∫ dX ÷ (−r<sub>A</sub>) for the PFR, with −r<sub>A</sub> = k C<sub>A0</sub> (1 − X). For the same conversion as the PFR, the CSTR needs (e<sup>Da</sup> − 1) ÷ Da times the volume.

## Worked example

A liquid phase reaction with k = **{rk:g} h⁻¹** runs in a **{rV:g} m³** reactor fed at **{rv0:g} m³/h** with C<sub>A0</sub> = **{rC:g} mol/L**:

- Space time τ = {rV:g} ÷ {rv0:g} = **{RC['tau']:.2f} h** ({RC['tau']*60:.0f} min)
- Damköhler number Da = {rk:g} × {RC['tau']:.2f} = **{RC['Da']:.2f}**
- CSTR conversion = {RC['Da']:.2f} ÷ (1 + {RC['Da']:.2f}) = **{RC['Xc']*100:.2f}%**, outlet C<sub>A</sub> = {rC:g} × (1 − {RC['Xc']:.4f}) = **{RC['Cc']:.4f} mol/L**
- PFR conversion = 1 − e<sup>−{RC['Da']:.2f}</sup> = **{RC['Xp']*100:.2f}%**, outlet C<sub>A</sub> = **{RC['Cp']:.4f} mol/L**
- To reach {RC['Xp']*100:.2f}% in a CSTR you would need (e<sup>{RC['Da']:.2f}</sup> − 1) ÷ {RC['Da']:.2f} = **{RC['r']:.3f}** times the volume, or {rV*RC['r']:.2f} m³

## Conversion against Damköhler number

| Da = k τ | CSTR conversion | PFR conversion | CSTR ÷ PFR volume for the PFR conversion |
|---|---|---|---|
{da_rows}
## Volume needed for a target conversion

Da required (proportional to reactor volume at fixed k and feed flow) and the CSTR to PFR volume ratio:

| Target conversion | Da for a CSTR | Da for a PFR | Volume ratio |
|---|---|---|---|
{vr_rows}
## CSTRs in series for 90% conversion

Total Da = N [(1 − X)<sup>−1/N</sup> − 1] for N equal tanks:

| Number of tanks | Total Da | Total volume ÷ PFR volume |
|---|---|---|
{ts_rows}
## How conversion estimates are used in practice

The ideal CSTR and PFR are the two limits of real mixing. A well agitated stirred tank behaves close to a CSTR, while a long tubular reactor, a packed bed or a pipe reactor in turbulent flow is close to a PFR. Engineers use these formulas to **screen reactor types**, to **scale up** from a lab rate constant, and to judge the effect of operating changes: raising the feed flow by 25% cuts τ and Da by 20%, and in this example drops the CSTR conversion from {RC['Xc']*100:.1f}% to {0.6/1.6*100:.1f}%. The rate constant comes from batch kinetics, for example by fitting ln(C<sub>A0</sub> ÷ C<sub>A</sub>) against time, and is corrected for temperature with the Arrhenius equation. A tracer test (residence time distribution) shows where a real vessel sits between the two ideals.

## Common mistakes

- **Mixing time units.** k in min⁻¹ with τ in hours gives Da 60 times too small. Convert k to h⁻¹ first, as this calculator expects.
- **Using the total vessel volume.** Use the liquid (reacting) volume; vapour space, jackets and dead zones do not react.
- **Applying the first order formulas to other orders.** For a second order reaction, X depends on C<sub>A0</sub> as well as k τ, and these formulas no longer hold.
- **Ignoring reversibility.** A reversible reaction cannot exceed its equilibrium conversion however long τ is; check the equilibrium constant first.
- **Assuming isothermal operation.** An exothermic reaction heats the reactor and raises k; without cooling, the real conversion and the safety margin can differ greatly from the isothermal estimate.
''')

print(len(DONE), 'pages:', ' '.join(DONE))
