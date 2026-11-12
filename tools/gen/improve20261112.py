"""Improve pass (2026-11-12) for thin pages from the first batch (2026-10-27):
physics/heat-conduction, electronics/wheatstone-bridge, electronics/inductor-energy, chemistry/daltons-law.
Keyword-first titles, 120-160 char descriptions, intros with the "<topic> calculator" phrase,
worked examples and reference tables computed here, practical notes, re-checked FAQs and related links.
Existing instrumentationblog.in links are kept; none are added. Slugs, categories and existing variable
ids are unchanged (asserted). Re-running regenerates the same files."""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from page import page, BASE
from ib import intro
U = '2026-11-12'
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

# ---------------------------------------------------------------- Heat conduction (Fourier's law)
hk, hA, hdT, hd = 0.04, 10.0, 20.0, 0.1
hQ = hk * hA * hdT / hd; hU = hk / hd; hR = hd / hk; hq = hk * hdT / hd; hE = hQ * 24 / 1000
MAT = (('Copper', 390), ('Aluminium', 220), ('Carbon steel', 50), ('Stainless steel', 16), ('Concrete (dense)', 1.4),
       ('Brick', 0.77), ('Glass', 1.0), ('Water', 0.6), ('Softwood timber', 0.13), ('Gypsum plasterboard', 0.21),
       ('Mineral wool', 0.035), ('Expanded polystyrene (EPS)', 0.035), ('PIR / polyurethane foam', 0.023), ('Still air', 0.026))
hm_rows = ''.join(f"| {nm} | {k:g} | {k*20/0.1:,.4g} W/m² | {0.1/k:,.4g} m²·K/W |\n" for nm, k in MAT)
ht_rows = ''
for nm, k in (('Mineral wool', 0.035), ('EPS', 0.035), ('PIR foam', 0.023), ('Softwood', 0.13)):
    ht_rows += f"| {nm} (k = {k:g}) | " + ' | '.join(f"{k/Ut*1000:,.0f} mm" for Ut in (0.5, 0.3, 0.2, 0.15)) + " |\n"
LAY = (('Inside surface resistance', None, 0.13), ('Gypsum plasterboard', (0.0125, 0.21), None),
       ('Mineral wool between studs (ignoring the studs)', (0.1, 0.035), None), ('Brick outer leaf', (0.102, 0.77), None),
       ('Outside surface resistance', None, 0.04))
lay_rows = ''; Rtot = 0.0
for nm, tk, Rs in LAY:
    Rl = Rs if Rs is not None else tk[0] / tk[1]
    Rtot += Rl
    desc = f"{tk[0]*1000:g} mm, k = {tk[1]:g}" if tk else 'standard value'
    lay_rows += f"| {nm} | {desc} | {Rl:.3f} |\n"
Uw = 1 / Rtot
W('physics/heat-conduction', f'''
title: Heat Conduction Calculator (Fourier's Law, U-Value & R-Value)
description: Calculate heat flow through a wall, slab or insulation layer with Fourier's law, plus heat flux, U-value, R-value and the energy lost per day.
category: physics
{intro("Heat flows through solids from hot to cold at a rate set by the material's thermal conductivity, thickness and area. Fourier's law is the basis of insulation design and heat exchanger calculations — see [what thermal conductivity is](https://www.instrumentationblog.in/what-is-thermal-conductivity/) and the main [types of heat exchangers](https://www.instrumentationblog.in/types-of-heat-exchangers/). This heat conduction calculator gives the heat flow, the heat flux, the U-value and R-value of the layer and the energy lost per day, and solves for any one value you leave blank.")}
keywords: [heat conduction calculator, fouriers law calculator, heat transfer through wall, thermal conductivity calculator, u value calculator, r value calculator, conductive heat loss calculator, heat flux calculator]
updated: {U}
variables:
  - {{ id: k, label: Thermal conductivity (k), suffix: W/m·K, default: {hk:g}, min: 0 }}
  - {{ id: A, label: Area, family: area, unit: m2, imperialUnit: ft2, default: {hA:g}, min: 0 }}
  - {{ id: dT, label: Temperature difference, family: tempdiff, unit: K, imperialUnit: F, default: {hdT:g}, min: 0 }}
  - {{ id: d, label: Thickness, family: length, unit: mm, imperialUnit: in, default: {hd*1000:g}, min: 0 }}
  - {{ id: Q, label: Heat flow, family: power, unit: W, imperialUnit: BTUh, min: 0 }}
  - {{ id: q, label: Heat flux (heat flow per m²), suffix: W/m², min: 0, decimals: 2 }}
  - {{ id: U, label: U-value, suffix: W/m²·K, min: 0, decimals: 3 }}
  - {{ id: Rv, label: R-value, suffix: m²·K/W, min: 0, decimals: 2 }}
  - {{ id: E24, label: Energy conducted per day, family: energy, unit: kWh, min: 0 }}
equations:
  - Q = k * A * dT / d
  - q = k * dT / d
  - U = k / d
  - Rv = d / k
  - E24 = Q * 24 * 3600
faq:
  - q: What is Fourier's law of heat conduction?
    a: The rate of heat flow through a material is proportional to its thermal conductivity, its area and the temperature difference across it, and inversely proportional to its thickness — Q = k A ΔT ÷ d. Heat always flows from the hotter side to the colder side.
  - q: What is the difference between U-value and R-value?
    a: The R-value (thermal resistance, m²·K/W) is thickness ÷ conductivity — the higher it is, the better the insulation. The U-value is its inverse, the heat flow per m² for each degree of temperature difference, so a lower U-value is better.
  - q: How do I calculate the U-value of a wall with several layers?
    a: Add the R-values of all layers in series, d ÷ k for each, plus the inside and outside surface resistances (typically 0.13 and 0.04 m²·K/W for a wall), then U = 1 ÷ total R. Studs, ties and other thermal bridges increase the real U-value.
  - q: How much heat does a wall lose in a day?
    a: Multiply the heat flow in watts by 24 hours and divide by 1,000 to get kWh per day. 80 W of steady loss is 1.92 kWh per day; over a heating season use the degree-days for your location instead of a fixed temperature difference.
related: [engineering/pipe-heat-loss, engineering/convection-heat-transfer, physics/stefan-boltzmann-law, engineering/heat-duty]
''', f'''
## How to use the heat conduction calculator

Enter the material's **thermal conductivity**, the **area**, the **temperature difference** between the two faces and the **thickness**. You get the heat flow, the heat flux per square metre, the U-value and R-value of the layer and the energy conducted in 24 hours. Leave any one input blank — for example the thickness — and enter a heat flow to solve for it.

## Fourier's law formula

<p class="formula">Q = k × A × ΔT ÷ d &nbsp;·&nbsp; q = Q ÷ A = k ΔT ÷ d</p>

<p class="formula">U = k ÷ d &nbsp;·&nbsp; R = d ÷ k &nbsp;·&nbsp; multi-layer: U = 1 ÷ (R<sub>si</sub> + Σ d ÷ k + R<sub>se</sub>)</p>

## Worked example

{hA:g} m² of {hd*1000:g} mm mineral wool (k = {hk:g} W/m·K) with {hdT:g} °C between its faces:

- Heat flow Q = {hk:g} × {hA:g} × {hdT:g} ÷ {hd:g} = **{hQ:g} W**
- Heat flux q = {hQ:g} ÷ {hA:g} = **{hq:g} W/m²**
- U-value = {hk:g} ÷ {hd:g} = **{hU:g} W/m²·K**; R-value = {hd:g} ÷ {hk:g} = **{hR:g} m²·K/W**
- Energy per day = {hQ:g} × 24 ÷ 1,000 = **{hE:g} kWh**

The same area of 100 mm dense concrete (k = 1.4) would conduct {1.4*hA*hdT/hd:,.0f} W — {1.4/hk:.0f} times as much.

## Thermal conductivity and heat flux of materials

Typical k values; heat flux and R-value for a 100 mm layer with a 20 °C difference:

| Material | k (W/m·K) | Heat flux | R-value of 100 mm |
|---|---|---|---|
{hm_rows}
Conductivity varies with density, moisture and temperature — use the manufacturer's declared value for design.

## Insulation thickness for a target U-value

Single layer, surface resistances ignored:

| Material | U = 0.5 | U = 0.3 | U = 0.2 | U = 0.15 W/m²·K |
|---|---|---|---|---|
{ht_rows}
## Multi-layer wall example

| Layer | Thickness and k | R (m²·K/W) |
|---|---|---|
{lay_rows}| **Total** | | **{Rtot:.3f}** |

U = 1 ÷ {Rtot:.3f} = **{Uw:.3f} W/m²·K**. Surface resistances are the usual values for horizontal heat flow through a wall (ISO 6946).

## Windows

| Glazing | Typical U-value (W/m²·K) |
|---|---|
| Single glazing | 5.0–5.8 |
| Double glazing (air filled) | 2.6–2.8 |
| Double, low-e, argon | 1.2–1.6 |
| Triple glazing | 0.6–0.8 |

## Practical notes

- **Imperial R-values:** US R-values use ft²·°F·h/BTU. Multiply an SI R-value by 5.678 to convert: R 2.5 SI ≈ R-14 US.
- **Steady state:** Fourier's law as used here gives the steady heat flow once temperatures have settled; heavy walls take hours to respond to a change in temperature.
- **Pipes and cylinders:** for insulation around a pipe the area grows with radius, so use the logarithmic formula in the [pipe heat loss calculator](/engineering/pipe-heat-loss/).
- **Surfaces:** the air films on each side add resistance; to calculate them, use the [convection heat transfer calculator](/engineering/convection-heat-transfer/).
''')

# ---------------------------------------------------------------- Wheatstone bridge
wVs, wR1, wR2, wR3, wRx = 10.0, 1000.0, 1000.0, 1000.0, 1010.0
wVo = wVs * (wRx / (wR3 + wRx) - wR2 / (wR1 + wR2)); wRb = wR3 * wR2 / wR1
wmVV = wVo / wVs * 1000; wRth = wR1 * wR2 / (wR1 + wR2) + wR3 * wRx / (wR3 + wRx)
wIs = wVs / (wR1 + wR2) + wVs / (wR3 + wRx); wP = wVs * wIs
wt_rows = ''
for x in (0.0001, 0.001, 0.005, 0.01, 0.02, 0.05):
    q = 10 * ((1 + x) / (2 + x) - 0.5); lin = 10 * x / 4
    wt_rows += f"| {x*100:g}% | {q*1000:.3f} mV | {lin*1000:.3f} mV | {(lin-q)/q*100:.2f}% | {10*x/2*1000:.2f} mV | {10*x*1000:.2f} mV |\n"
ws_rows = ''
for ue in (100, 500, 1000, 2000):
    for Vs in (5, 10):
        x = 2.0 * ue * 1e-6
        ws_rows += f"| {ue:,} µε | {Vs} V | {Vs*((1+x)/(2+x)-0.5)*1000:.3f} mV | {Vs*x/2*1000:.3f} mV | {Vs*x*1000:.3f} mV |\n"
W('electronics/wheatstone-bridge', f'''
title: Wheatstone Bridge Calculator (Output Voltage & Balance)
description: Calculate Wheatstone bridge output voltage, sensitivity in mV/V, balance resistance, output resistance and supply current for sensor bridge circuits.
category: electronics
{intro("A Wheatstone bridge measures very small resistance changes by balancing two voltage dividers against each other. It sits inside strain gauges, load cells, pressure sensors and RTD circuits — see these [Wheatstone bridge applications](https://www.instrumentationblog.in/wheatstone-bridge-10-applications/). This Wheatstone bridge calculator gives the exact output voltage, the output in mV/V, the resistance that balances the bridge, the bridge's output resistance and the current and power it draws from the excitation supply.")}
keywords: [wheatstone bridge calculator, bridge circuit calculator, unknown resistance calculator, bridge output voltage, balanced bridge, strain gauge bridge calculator, quarter bridge, mv/v calculator]
updated: {U}
variables:
  - {{ id: Vs, label: Excitation voltage, family: voltage, unit: V, default: {wVs:g}, min: 0 }}
  - {{ id: R1, label: R1 (top left), family: resistance, unit: ohm, default: {wR1:g}, min: 0 }}
  - {{ id: R2, label: R2 (bottom left), family: resistance, unit: ohm, default: {wR2:g}, min: 0 }}
  - {{ id: R3, label: R3 (top right), family: resistance, unit: ohm, default: {wR3:g}, min: 0 }}
  - {{ id: Rx, label: "Rx (bottom right, unknown)", family: resistance, unit: ohm, default: {wRx:g}, min: 0 }}
  - {{ id: Vo, label: Bridge output voltage, family: voltage, unit: mV }}
  - {{ id: Rb, label: Rx for balance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: mVV, label: Output per volt of excitation, suffix: mV/V, decimals: 4 }}
  - {{ id: Rth, label: Output resistance of the bridge, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Is, label: Current drawn from the supply, family: current, unit: mA, min: 0 }}
  - {{ id: Pb, label: Power dissipated in the bridge, family: power, unit: mW, min: 0 }}
equations:
  - Vo = Vs * (Rx / (R3 + Rx) - R2 / (R1 + R2))
  - Rb = R3 * R2 / R1
  - mVV = Vo / Vs * 1000
  - Rth = R1 * R2 / (R1 + R2) + R3 * Rx / (R3 + Rx)
  - Is = Vs / (R1 + R2) + Vs / (R3 + Rx)
  - Pb = Vs * Is
faq:
  - q: What is the balance condition of a Wheatstone bridge?
    a: The output is zero when the two dividers have the same ratio, R1 ÷ R2 = R3 ÷ Rx, so the unknown resistance is Rx = R3 × R2 ÷ R1. In a classic balanced-bridge measurement R3 is a calibrated variable resistor adjusted until a galvanometer reads zero.
  - q: How does a Wheatstone bridge measure small changes?
    a: At balance the output is zero, so a small change in one resistor produces a small voltage on a zero background that can be amplified, without the large fixed offset a single divider would have. Changes in excitation or temperature that affect all arms equally also cancel.
  - q: What is a quarter, half and full bridge?
    a: The number of active sensing elements — one, two or four. With the same fractional change, a half bridge (two active arms of opposite sign) gives twice the output of a quarter bridge and a full bridge four times, and the half and full bridges are linear and better temperature-compensated.
  - q: Is the output of a quarter bridge linear?
    a: Only approximately. The exact output is V_s × [(1 + x) ÷ (2 + x) − ½] for a fractional change x, which is close to V_s x ÷ 4 for small x but falls about x ÷ 2 below it — 0.5% low at a 1% change. This calculator always uses the exact formula.
related: [electronics/strain-gauge, electronics/voltage-divider, engineering/pt100-resistance, electronics/instrumentation-amplifier-gain]
''', f'''
## How to use the Wheatstone bridge calculator

Enter the **excitation voltage** and the four resistances: R1 and R2 form the left divider (R1 at the top), R3 and Rx the right divider (Rx at the bottom). The calculator gives the **bridge output voltage** between the two midpoints (positive when the right midpoint is higher), the same output in **mV/V** as quoted on load cell datasheets, the value of Rx that would **balance** the bridge, the **output resistance** seen by the amplifier and the **current and power** drawn from the supply. To find an unknown Rx from a measured output, enter the output voltage and press × on Rx.

## Wheatstone bridge formulas

<p class="formula">V<sub>out</sub> = V<sub>s</sub> × [R<sub>x</sub> ÷ (R₃ + R<sub>x</sub>) − R₂ ÷ (R₁ + R₂)] &nbsp;·&nbsp; balance: R<sub>x</sub> = R₃ × R₂ ÷ R₁</p>

<p class="formula">R<sub>out</sub> = R₁ ∥ R₂ + R₃ ∥ R<sub>x</sub> &nbsp;·&nbsp; I<sub>s</sub> = V<sub>s</sub> ÷ (R₁ + R₂) + V<sub>s</sub> ÷ (R₃ + R<sub>x</sub>)</p>

## Worked example: 1% change in a quarter bridge

All fixed arms {wR1:,.0f} Ω, Rx = {wRx:,.0f} Ω, {wVs:g} V excitation:

- V<sub>out</sub> = {wVs:g} × ({wRx:,.0f} ÷ {wR3+wRx:,.0f} − {wR2:,.0f} ÷ {wR1+wR2:,.0f}) = {wVs:g} × ({wRx/(wR3+wRx):.6f} − 0.5) = **{wVo*1000:.3f} mV**
- Sensitivity = {wVo*1000:.3f} ÷ {wVs:g} = **{wmVV:.4f} mV/V**
- Balance resistance = {wR3:,.0f} × {wR2:,.0f} ÷ {wR1:,.0f} = **{wRb:,.0f} Ω**
- Output resistance = {wR1*wR2/(wR1+wR2):g} + {wR3*wRx/(wR3+wRx):.2f} = **{wRth:.2f} Ω**
- Supply current = {wVs:g} ÷ {wR1+wR2:,.0f} + {wVs:g} ÷ {wR3+wRx:,.0f} = **{wIs*1000:.3f} mA**, dissipating **{wP*1000:.2f} mW**

## Output against resistance change (10 V, equal arms)

| ΔR/R | Quarter bridge (exact) | Quarter bridge (V<sub>s</sub>x/4) | Linearity error | Half bridge | Full bridge |
|---|---|---|---|---|---|
{wt_rows}
## Strain gauge bridge output (gauge factor 2)

| Strain | Excitation | Quarter bridge | Half bridge | Full bridge |
|---|---|---|---|---|
{ws_rows}
## Practical notes

- **Self-heating:** the current through each arm heats the sensor; strain gauges and RTDs are often excited at 2–5 V (or less) to keep the power per element to a few milliwatts.
- **Lead resistance:** in a quarter bridge the lead wires are in series with the gauge. A three-wire connection puts one lead in each adjacent arm so their effect cancels — the same idea as in three-wire RTD bridges, see the [Pt100 calculator](/engineering/pt100-resistance/).
- **Amplifier:** the output is a small differential signal on a common-mode voltage of about V<sub>s</sub> ÷ 2, so it needs an [instrumentation amplifier](/electronics/instrumentation-amplifier-gain/) rather than a single-ended op-amp stage.
- **Load cells** are rated in mV/V at full load (commonly 1–3 mV/V): a 2 mV/V cell excited at 10 V gives 20 mV at its rated capacity. Use the [strain gauge calculator](/electronics/strain-gauge/) to convert strain to resistance change.
''')

# ---------------------------------------------------------------- Inductor energy
iL, iI, idt = 0.01, 2.0, 0.001
iE = 0.5 * iL * iI ** 2; iV = iL * iI / idt; iP = iE / idt
INDS = (('10 µH SMPS inductor', 10e-6, 5), ('100 µH power choke', 100e-6, 3), ('1 mH filter inductor', 1e-3, 1),
        ('10 mH filter choke', 10e-3, 2), ('Relay coil, 1 H', 1.0, 0.03), ('Contactor coil, 5 H', 5.0, 0.2),
        ('Motor winding, 50 mH', 50e-3, 20), ('Ignition coil primary, 7 mH', 7e-3, 7))
def fmtJ(E):
    return f"{E*1e6:.4g} µJ" if E < 1e-3 else f"{E*1e3:.4g} mJ" if E < 1 else f"{E:.4g} J"
ie_rows = ''.join(f"| {nm} | {I:g} A | {fmtJ(0.5*L*I*I)} |\n" for nm, L, I in INDS)
ig_rows = ''
for L in (1e-6, 10e-6, 100e-6, 1e-3, 10e-3, 100e-3):
    lab = f"{L*1e6:g} µH" if L < 1e-3 else f"{L*1e3:g} mH"
    ig_rows += f"| {lab} | " + ' | '.join(fmtJ(0.5 * L * I * I) for I in (0.1, 1, 5, 10, 20)) + " |\n"
W('electronics/inductor-energy', f'''
title: Inductor Energy Calculator (E = ½LI²)
description: Calculate the energy stored in an inductor from inductance and current with E = ½LI², plus the switch-off voltage and the average power released.
category: electronics
{intro("An inductor stores energy in its magnetic field while current flows, and releases it when the current changes — which is why switching off a coil can cause a voltage spike. Learn the [inductor working principle](https://www.instrumentationblog.in/inductor-working-principle/) and the limits set by [inductor saturation current](https://www.instrumentationblog.in/inductor-saturation-current/). This inductor energy calculator gives the stored energy, the voltage induced if the current is switched off in a given time and the average power released, and solves for the inductance or current when you know the energy.")}
keywords: [inductor energy calculator, energy stored in inductor, 1/2 li2 calculator, magnetic energy calculator, inductor current energy, choke energy, inductive kickback voltage]
updated: {U}
variables:
  - {{ id: L, label: Inductance, family: inductance, unit: mH, default: {iL*1000:g}, min: 0 }}
  - {{ id: I, label: Current, family: current, unit: A, default: {iI:g}, min: 0 }}
  - {{ id: E, label: Stored energy, family: energy, unit: J, min: 0 }}
  - {{ id: dt, label: Switch-off time, family: seconds, unit: ms, default: {idt*1000:g}, min: 0 }}
  - {{ id: V, label: Induced voltage at switch-off (L·di/dt), family: voltage, unit: V, min: 0 }}
  - {{ id: Pav, label: Average power released during switch-off, family: power, unit: W, min: 0 }}
equations:
  - E = 0.5 * L * I^2
  - V = L * I / dt
  - Pav = E / dt
faq:
  - q: How much energy does an inductor store?
    a: E = ½ × L × I², with L in henries and I in amperes giving joules. A 10 mH inductor carrying 2 A stores ½ × 0.01 × 2² = 0.02 J (20 mJ). Doubling the current stores four times the energy.
  - q: Why do relay coils need flyback diodes?
    a: When the current is interrupted quickly, the coil tries to keep it flowing, producing a voltage of L × di/dt that can reach hundreds of volts and damage the switching transistor or burn relay contacts. A diode across the coil gives the current a path so the stored energy dies away in the coil resistance.
  - q: What is inductor saturation?
    a: Above a certain current the core can hold no more magnetic flux, so the inductance falls sharply and the current rises quickly. Ferrite cores saturate at roughly 0.3–0.5 T; always keep the peak current below the saturation current given in the datasheet.
  - q: Where is inductor energy used?
    a: Switch-mode power supplies store energy in an inductor or transformer each switching cycle and release it to the output; ignition coils use it to create the high-voltage spark, and superconducting magnets store megajoules in their field.
related: [electronics/rl-time-constant, electronics/capacitor-energy, electronics/flyback-transformer, electronics/buck-converter]
''', f'''
## How to use the inductor energy calculator

Enter the **inductance** and the **current** to get the stored energy. Add a **switch-off time** to estimate the average voltage induced if the current falls to zero in that time without suppression, and the average power the stored energy is released at. To find the current that stores a given energy, enter the energy and press × on the current.

For more background, read [Lenz’s Law and Electromagnetic Induction](https://www.instrumentationblog.in/lenzs-law-electromagnetic-induction/).

## Inductor energy formulas

<p class="formula">E = ½ × L × I² &nbsp;·&nbsp; V = L × di/dt ≈ L × I ÷ Δt &nbsp;·&nbsp; P<sub>avg</sub> = E ÷ Δt</p>

The voltage is the average over a linear fall in current; an abrupt interruption is faster still, so the real spike is limited only by the coil's stray capacitance or by arcing across the switch.

## Worked example

A {iL*1000:g} mH choke carrying {iI:g} A is switched off in {idt*1000:g} ms:

- Stored energy E = ½ × {iL:g} × {iI:g}² = **{iE:g} J** ({iE*1000:g} mJ)
- Induced voltage V = {iL:g} × {iI:g} ÷ {idt:g} = **{iV:g} V**
- Average power released = {iE:g} ÷ {idt:g} = **{iP:g} W**

Interrupting the same current in 10 µs would induce about {iL*iI/1e-5:,.0f} V — why a suppression diode is essential.

## Energy stored in common inductors

| Inductor | Current | Energy |
|---|---|---|
{ie_rows}
## Stored energy by inductance and current

| Inductance | 0.1 A | 1 A | 5 A | 10 A | 20 A |
|---|---|---|---|---|---|
{ig_rows}
## Suppressing inductive kick

| Method | Release speed | Notes |
|---|---|---|
| Flyback diode | Slow | Simplest for DC coils; delays relay drop-out |
| Diode + Zener | Fast | Clamps to a set voltage |
| RC snubber | Medium | Works on AC and DC |
| Varistor (MOV) | Fast | Common on AC contactor coils |

## Practical notes

- **Saturation and core choice:** ferrite cores saturate at about 0.3–0.5 T, iron powder and silicon steel at higher flux. Gapped cores store most of their energy in the air gap, which is why SMPS inductors and flyback transformers use them.
- **Energy per cycle:** a converter that stores E each switching period at frequency f transfers up to P = E × f — 20 µJ at 100 kHz is 2 W.
- **Decay time:** with a flyback diode the current dies away with the coil's L/R time constant; see the [RL time constant calculator](/electronics/rl-time-constant/).
- To compare with energy stored in an electric field, use the [capacitor energy calculator](/electronics/capacitor-energy/).
''')

# ---------------------------------------------------------------- Dalton's law
dnA, dnT, dP = 21.0, 100.0, 1.0
dx = dnA / dnT; dpA = dx * dP; dpR = dP - dpA
AIR = (('Nitrogen, N₂', 78.084), ('Oxygen, O₂', 20.946), ('Argon, Ar', 0.934), ('Carbon dioxide, CO₂', 0.042))
da_rows = ''.join(f"| {nm} | {v:g}% | {v/100:.5f} atm | {v/100*101.325:.3f} kPa |\n" for nm, v in AIR)
dd_rows = ''
for dep in (0, 10, 20, 30, 40, 50):
    Pa = 1 + dep / 10
    dd_rows += f"| {dep} m | {Pa:.1f} atm | " + ' | '.join(f"{f*Pa:.2f} atm" for f in (0.21, 0.32, 0.36)) + " |\n"
dm_rows = ''
for f in (0.21, 0.28, 0.32, 0.36, 0.40, 0.50):
    dm_rows += f"| {f*100:.0f}% | {10*(1.4/f-1):.1f} m | {10*(1.6/f-1):.1f} m |\n"
dh_rows = ''
for h in (0, 1000, 2000, 3000, 4000, 5000, 6000, 8848):
    p = 101.325 * (1 - 2.25577e-5 * h) ** 5.25588
    dh_rows += f"| {h:,} m | {p:.1f} kPa | {0.20946*p:.1f} kPa | {0.20946*p/(0.20946*101.325)*100:.0f}% |\n"
W('chemistry/daltons-law', f'''
title: Dalton's Law Calculator (Partial Pressure & Mole Fraction)
description: Calculate the partial pressure of a gas in a mixture from its mole fraction or percentage and the total pressure — for air, diving gases and gas analysis.
category: chemistry
{intro("In a mixture of gases each gas exerts its own partial pressure, as if it filled the container alone, and the partial pressures add up to the total pressure. This Dalton's law calculator gives the mole fraction and partial pressure of a gas from its moles or volume percentage and the total pressure, along with the combined partial pressure of the other gases — used in diving, anaesthesia, combustion and gas analysis.")}
keywords: [daltons law calculator, partial pressure calculator, mole fraction calculator, dalton's law of partial pressures, oxygen partial pressure calculator, gas mixture pressure, ppo2 calculator]
updated: {U}
variables:
  - {{ id: nA, label: Moles (or %) of gas A, default: {dnA:g}, min: 0 }}
  - {{ id: nT, label: Total moles (or 100%), default: {dnT:g}, min: 0.0001 }}
  - {{ id: P, label: Total pressure (absolute), family: pressure, unit: atm, imperialUnit: psi, default: {dP:g}, min: 0 }}
  - {{ id: x, label: Mole fraction of A, min: 0, max: 1, decimals: 4 }}
  - {{ id: pA, label: Partial pressure of A, family: pressure, unit: atm, imperialUnit: psi, min: 0 }}
  - {{ id: pR, label: Partial pressure of all the other gases, family: pressure, unit: atm, imperialUnit: psi, min: 0 }}
equations:
  - x = nA / nT
  - pA = x * P
  - pR = P - pA
faq:
  - q: What is Dalton's law of partial pressures?
    a: The total pressure of a mixture of non-reacting gases equals the sum of the partial pressures of the individual gases, P = p₁ + p₂ + p₃ + … Each partial pressure equals the gas's mole fraction times the total pressure, pᵢ = xᵢ P.
  - q: What is the partial pressure of oxygen in air?
    a: Dry air is 20.95% oxygen by volume, so at sea level (101.325 kPa) the oxygen partial pressure is about 21.2 kPa or 0.21 atm. It falls in proportion to the total pressure at altitude and rises with depth under water.
  - q: Why does partial pressure matter in diving?
    a: Oxygen becomes toxic to the nervous system at partial pressures above about 1.4–1.6 atm. Every 10 m of seawater adds about 1 atm, so air reaches 1.4 atm of oxygen at about 57 m, and oxygen-enriched nitrox mixes reach it at shallower depths — their maximum operating depth.
  - q: Can I use percentages instead of moles?
    a: Yes. For ideal gases the volume percentage equals the mole percentage, so enter the percentage and 100 as the total. Mass percentages must first be converted to moles using the molar masses.
related: [physics/ideal-gas-law, chemistry/combined-gas-law, chemistry/henrys-law, chemistry/gas-density]
''', f'''
## How to use the Dalton's law calculator

Enter the **moles** (or volume percent) of the gas you are interested in, the **total moles** (or 100) and the **total absolute pressure** of the mixture. You get the **mole fraction**, the **partial pressure** of the gas and the partial pressure of the remaining gases. To find the total pressure at which a gas reaches a given partial pressure, enter that partial pressure and press × on the total pressure.

## Dalton's law formulas

<p class="formula">x<sub>A</sub> = n<sub>A</sub> ÷ n<sub>total</sub> &nbsp;·&nbsp; p<sub>A</sub> = x<sub>A</sub> × P<sub>total</sub></p>

<p class="formula">P<sub>total</sub> = p₁ + p₂ + p₃ + … &nbsp;·&nbsp; p<sub>others</sub> = P<sub>total</sub> − p<sub>A</sub></p>

## Worked example

Oxygen at {dnA:g}% in air at {dP:g} atm:

- Mole fraction x = {dnA:g} ÷ {dnT:g} = **{dx:g}**
- Oxygen partial pressure = {dx:g} × {dP:g} = **{dpA:g} atm** ({dpA*101.325:.2f} kPa)
- The other gases contribute {dP:g} − {dpA:g} = **{dpR:g} atm**

## Composition of dry air at sea level

| Gas | Volume % | Partial pressure | In kPa |
|---|---|---|---|
{da_rows}
## Oxygen partial pressure with depth

Seawater, about 1 atm per 10 m:

| Depth | Absolute pressure | Air (21% O₂) | Nitrox 32 | Nitrox 36 |
|---|---|---|---|---|
{dd_rows}
## Maximum operating depth by oxygen fraction

Depth at which the oxygen partial pressure reaches the limit, MOD = 10 × (pO₂ ÷ F<sub>O₂</sub> − 1):

| Oxygen in the mix | MOD at pO₂ 1.4 atm | MOD at pO₂ 1.6 atm |
|---|---|---|
{dm_rows}
## Oxygen partial pressure at altitude

International Standard Atmosphere:

| Altitude | Air pressure | O₂ partial pressure | Of sea-level value |
|---|---|---|---|
{dh_rows}
## Practical notes

- **Gas collected over water** is saturated with water vapour, so p<sub>gas</sub> = P<sub>atm</sub> − p<sub>H₂O</sub>; the water vapour pressure is about 2.34 kPa at 20 °C, 3.17 kPa at 25 °C and 4.25 kPa at 30 °C.
- **Real gases:** Dalton's law is exact for ideal gases and very close for air and most gases near atmospheric pressure; at high pressure molecular interactions cause small deviations.
- **Gas analysers** measure concentration as a fraction; to get the partial pressure that drives dissolution or reaction, multiply by the absolute pressure — see the [Henry's law calculator](/chemistry/henrys-law/) for gas solubility.
- Diving tables round to 10 m per atm and use absolute pressure; always follow your training agency's limits.
''')

print(len(DONE), 'improved:', ' '.join(DONE))
