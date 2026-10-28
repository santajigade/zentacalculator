import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
from ib import L
D = '2026-10-27'; pi = math.pi; r3 = math.sqrt(3)
def kvar(P, a, b): return P*(math.tan(math.acos(a)) - math.tan(math.acos(b)))

# 1 Power factor correction
page('electrical', 'power-factor-correction', f'''
title: Power Factor Correction Calculator (Capacitor kVAr)
description: Calculate the capacitor bank kVAr and capacitance needed to raise power factor from its present value to a target — with current reduction.
category: electrical
keywords: [power factor correction calculator, capacitor bank kvar calculation, kvar required, apfc panel sizing, improve power factor, capacitor size for power factor, kvar formula]
updated: {D}
featured: true
variables:
  - {{ id: P, label: Active load power, family: power, unit: kW, imperialUnit: hp, default: 100, min: 0 }}
  - {{ id: pf1, label: Present power factor, default: 0.75, min: 0.01, max: 1 }}
  - {{ id: pf2, label: Target power factor, default: 0.95, min: 0.01, max: 1 }}
  - {{ id: V, label: Line voltage, family: voltage, unit: V, default: 415, min: 0 }}
  - {{ id: f, label: Supply frequency, family: frequency, unit: Hz, default: 50, min: 1 }}
  - {{ id: Q, label: Capacitor bank required, suffix: kVAr, min: 0, decimals: 2 }}
  - {{ id: C, label: Capacitance per phase (delta), family: capacitance, unit: uF, min: 0 }}
  - {{ id: S1, label: Apparent power before, suffix: kVA, min: 0, decimals: 1 }}
  - {{ id: S2, label: Apparent power after, suffix: kVA, min: 0, decimals: 1 }}
  - {{ id: red, label: Line current reduction, family: percent, unit: '%', min: 0 }}
equations:
  - Q = P / 1000 * (tan(acos(pf1)) - tan(acos(pf2)))
  - C = Q * 1000 / 3 / (2 * pi * f * V^2)
  - S1 = P / 1000 / pf1
  - S2 = P / 1000 / pf2
  - red = 1 - pf1 / pf2
faq:
  - q: How do I calculate the kVAr needed for power factor correction?
    a: kVAr = kW × (tan φ₁ − tan φ₂), where φ₁ = acos(present PF) and φ₂ = acos(target PF). For 100 kW from 0.75 to 0.95 you need about 55.3 kVAr.
  - q: What power factor should I aim for?
    a: Most utilities penalise below 0.90–0.95. A target of 0.95–0.98 is common. Avoid correcting to unity or leading, which can cause over-voltage and resonance.
  - q: Why does the current fall after correction?
    a: The capacitor supplies the reactive current locally, so the supply only carries the active part plus less reactive current. Current falls in proportion to PF₁ ÷ PF₂.
  - q: Do I need detuned capacitors?
    a: Where drives and other non-linear loads create harmonics, use detuned (reactor-protected) banks — typically 7% detuning — to avoid harmonic resonance.
related: [electrical/kva-to-kw, electrical/three-phase-motor-power, electrical/thd, electrical/transformer-current]
{L(('how-to-calculate-capacitor-bank-kvar-formula', 'How to Calculate Capacitor Bank kVAr (Formula)'), ('capacitor-bank-sizing-power-factor-correction', 'Capacitor Bank Sizing for Power Factor Correction'), ('power-factor-improvement-calculation', 'Power Factor Improvement Calculation'), ('power-factor-kw-kva-kvar', 'Power Factor, kW, kVA and kVAr Explained'))}''', f'''
## How to use this calculator

Enter the **active load** in kW, the **present** and **target power factor**, and the supply **voltage** and **frequency**. You get the capacitor kVAr required, the capacitance per phase for a delta-connected bank, the kVA before and after, and how much the line current falls.

## The formula

<p class="formula">Q<sub>c</sub> = P × (tan φ₁ − tan φ₂), &nbsp; φ = cos⁻¹(PF)</p>

For a delta-connected three-phase bank, each capacitor sees the line voltage:

<p class="formula">C per phase = Q<sub>c</sub> ÷ (3 × 2πf × V<sub>L</sub>²)</p>

## Example

100 kW at 0.75 PF, corrected to 0.95 at 415 V, 50 Hz:

- tan φ₁ = 0.882, tan φ₂ = 0.329
- Q<sub>c</sub> = 100 × (0.882 − 0.329) = **{kvar(100,0.75,0.95):.1f} kVAr**
- kVA falls from 133.3 to 105.3 and line current falls by **21%**

## kVAr multiplier table (kVAr per kW)

| Present PF | to 0.90 | to 0.95 | to 0.98 | to 1.00 |
|---|---|---|---|---|
''' + ''.join(f"| {a:.2f} | {kvar(1,a,0.90):.3f} | {kvar(1,a,0.95):.3f} | {kvar(1,a,0.98):.3f} | {kvar(1,a,1.0):.3f} |\n" for a in [0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90]) + '''
Multiply the factor by the load kW to get the kVAr required.

## Why correct power factor?

- **Lower bills**: avoid utility penalties for low PF and reduce kVA maximum demand charges.
- **Free up capacity**: the same transformer and cables can carry more kW.
- **Lower losses**: I²R losses in cables and transformers fall with current.
- **Better voltage**: less reactive current means less voltage drop.

## Fixed vs automatic correction

- **Fixed capacitors** at individual motors suit constant loads. Size them to about 90% of the motor's no-load magnetising kVAr to avoid self-excitation.
- **APFC panels** (automatic power factor correction) switch capacitor steps as the plant load changes. They are the usual choice for a main LV board.

## Harmonics

Capacitors lower the system's resonant frequency. With VFDs, UPSs and other non-linear loads, check harmonic levels with the [THD calculator](/electrical/thd/) and use detuned reactors where needed.
''')

# 2 Induction motor slip
def ns(f, p): return 120*f/p
page('electrical', 'induction-motor-slip', f'''
title: Induction Motor Slip and Synchronous Speed Calculator
description: Calculate synchronous speed, slip and rotor frequency of an induction motor from supply frequency, number of poles and rated speed.
category: electrical
keywords: [motor slip calculator, synchronous speed calculator, induction motor slip, 120f/p, motor rpm calculation, rotor frequency, number of poles]
updated: {D}
variables:
  - {{ id: f, label: Supply frequency, family: frequency, unit: Hz, default: 50, min: 0 }}
  - id: p
    label: Number of poles
    default: 4
    options:
      - {{ label: 2 poles, value: 2 }}
      - {{ label: 4 poles, value: 4 }}
      - {{ label: 6 poles, value: 6 }}
      - {{ label: 8 poles, value: 8 }}
      - {{ label: 10 poles, value: 10 }}
      - {{ label: 12 poles, value: 12 }}
  - {{ id: Nr, label: Rotor (rated) speed, suffix: rpm, default: 1460, min: 0 }}
  - {{ id: Ns, label: Synchronous speed, suffix: rpm, min: 0, decimals: 0 }}
  - {{ id: s, label: Slip, family: percent, unit: '%' }}
  - {{ id: fr, label: Rotor frequency, family: frequency, unit: Hz, min: 0 }}
equations:
  - Ns = 120 * f / p
  - s = (Ns - Nr) / Ns
  - fr = s * f
faq:
  - q: What is synchronous speed?
    a: The speed of the rotating magnetic field, Ns = 120 × f ÷ P. A 4-pole motor on 50 Hz has a synchronous speed of 1,500 rpm.
  - q: What is slip in an induction motor?
    a: The difference between synchronous speed and rotor speed, as a percentage of synchronous speed. Typical full-load slip is 1–5%.
  - q: Why can't an induction motor run at synchronous speed?
    a: At synchronous speed, the rotor would not cut any magnetic flux, so no current would be induced and no torque produced.
  - q: How do I find the number of poles from the nameplate speed?
    a: Pick the synchronous speed just above the nameplate speed. A 2,940 rpm motor on 50 Hz is 2-pole (3,000 rpm); a 960 rpm motor is 6-pole (1,000 rpm).
related: [electrical/three-phase-motor-power, engineering/torque-power-speed, electrical/kw-to-amps, electrical/voltage-unbalance]
{L(('induction-motor-slip-explained', 'Induction Motor Slip Explained'), ('how-ac-induction-motor-works', 'How an AC Induction Motor Works'), ('motor-nameplate-details-explained', 'Motor Nameplate Details Explained'), ('synchronous-motor-working-principle', 'Synchronous Motor Working Principle'))}''', '''
## How to use this calculator

Enter the **supply frequency**, choose the **number of poles** and enter the motor's **rated speed** from the nameplate. You get the synchronous speed, slip and rotor current frequency.

## The formulas

<p class="formula">N<sub>s</sub> = 120 × f ÷ P &nbsp;·&nbsp; s = (N<sub>s</sub> − N<sub>r</sub>) ÷ N<sub>s</sub> &nbsp;·&nbsp; f<sub>r</sub> = s × f</p>

## Synchronous speeds

| Poles | 50 Hz | 60 Hz | Typical full-load speed (50 Hz) |
|---|---|---|---|
''' + ''.join(f"| {p} | {ns(50,p):,.0f} rpm | {ns(60,p):,.0f} rpm | {t} rpm |\n" for p, t in [(2, '2,880–2,970'), (4, '1,420–1,485'), (6, '940–990'), (8, '710–740'), (10, '570–590'), (12, '480–495')]) + '''
## Example

A 4-pole motor on 50 Hz with a nameplate speed of 1,460 rpm:

- N<sub>s</sub> = 120 × 50 ÷ 4 = **1,500 rpm**
- Slip = (1,500 − 1,460) ÷ 1,500 = **2.67%**
- Rotor frequency = 0.0267 × 50 = **1.33 Hz**

## What slip tells you

- **Load**: slip rises roughly in proportion to load. A motor running at half its rated slip is lightly loaded — a quick field check of loading.
- **Size**: large, high-efficiency motors have lower slip (around 0.5–1.5%); small motors may have 4–6%.
- **Rotor faults**: broken rotor bars show up as current sidebands at (1 ± 2s) × f in motor current signature analysis.

## Speed control with a VFD

Changing frequency changes synchronous speed: at 25 Hz, a 4-pole motor runs near 750 rpm. Slip in rpm stays roughly constant at a given torque.
''')

# 3 Transformer turns ratio
page('electrical', 'transformer-turns-ratio', f'''
title: Transformer Turns Ratio Calculator
description: Calculate transformer secondary voltage, turns ratio and primary or secondary current from the number of turns or voltages.
category: electrical
keywords: [transformer turns ratio calculator, secondary voltage calculator, transformer ratio, np ns vp vs, transformer winding turns, step down transformer]
updated: {D}
variables:
  - {{ id: Vp, label: Primary voltage, family: voltage, unit: V, default: 230, min: 0 }}
  - {{ id: Np, label: Primary turns, default: 1000, min: 0 }}
  - {{ id: Ns, label: Secondary turns, default: 52, min: 0 }}
  - {{ id: Vs, label: Secondary voltage, family: voltage, unit: V, min: 0 }}
  - {{ id: Is, label: Secondary current, family: current, unit: A, default: 5, min: 0 }}
  - {{ id: Ip, label: Primary current, family: current, unit: A, min: 0 }}
  - {{ id: a, label: Turns ratio (Np ÷ Ns), min: 0, decimals: 3 }}
equations:
  - a = Np / Ns
  - Vs = Vp / a
  - Ip = Is / a
faq:
  - q: What is the transformer turns ratio?
    a: The ratio of primary turns to secondary turns, Np ÷ Ns. For an ideal transformer it equals the voltage ratio Vp ÷ Vs and the inverse of the current ratio.
  - q: How do I calculate secondary voltage?
    a: Vs = Vp × Ns ÷ Np. A 230 V transformer with 1,000 primary and 52 secondary turns gives about 12 V.
  - q: Why does current change the opposite way to voltage?
    a: Power in equals power out (ignoring losses), so if voltage is stepped down by 20 times, current is stepped up by 20 times.
  - q: How is the turns ratio tested on site?
    a: With a transformer turns ratio (TTR) tester. The measured ratio should be within ±0.5% of the nameplate ratio on each tap.
related: [electrical/transformer-current, electrical/transformer-efficiency, electrical/transformer-short-circuit, physics/ohms-law]
{L(('transformer-turns-ratio-secondary-voltage', 'Transformer Turns Ratio and Secondary Voltage'), ('transformer-routine-and-type-tests', 'Transformer Routine and Type Tests'), ('isolation-transformer-working-uses', 'Isolation Transformer Working and Uses'))}''', '''
## How to use this calculator

Enter the **primary voltage**, **primary turns** and **secondary turns**, plus the **secondary load current**. You get the turns ratio, secondary voltage and primary current. Fill any consistent set — for example, both voltages and primary turns to find secondary turns.

## The ideal transformer equations

<p class="formula">V<sub>p</sub> ÷ V<sub>s</sub> = N<sub>p</sub> ÷ N<sub>s</sub> = I<sub>s</sub> ÷ I<sub>p</sub></p>

## Example

230 V primary, 1,000 turns; 52 secondary turns:

- Ratio = 1,000 ÷ 52 = 19.23
- Secondary voltage = 230 ÷ 19.23 = **11.96 V**
- With 5 A secondary load, the primary draws 5 ÷ 19.23 = **0.26 A**

## Turns per volt

Small transformers are often designed by turns per volt, which depends on core area and flux density: turns/V ≈ 1 ÷ (4.44 × f × B × A). For a 50 Hz core with 10 cm² area at 1.2 T, that is about 3.75 turns per volt.

## Three-phase ratios

For three-phase transformers, the voltage ratio uses line voltages, and the vector group affects the turns ratio:

| Connection | Line voltage ratio |
|---|---|
| Yy or Dd | Np ÷ Ns |
| Dy (delta primary, star secondary) | Np ÷ (√3 × Ns) |
| Yd (star primary, delta secondary) | √3 × Np ÷ Ns |

A Dyn11 11 kV/433 V distribution transformer has a phase-winding turns ratio of 11,000 ÷ 250 = 44.

## Real transformers

On load, the secondary voltage drops slightly because of winding resistance and leakage reactance (regulation, typically 2–5%). Transformers are often wound with a few percent extra turns to compensate.
''')

# 4 Transformer efficiency
def teff(S, x, pf, Pi, Pc): o = x*S*pf; return o/(o+Pi+x*x*Pc)
page('electrical', 'transformer-efficiency', f'''
title: Transformer Efficiency Calculator (Iron and Copper Losses)
description: Calculate transformer efficiency at any load and power factor from no-load (core) and full-load (copper) losses — plus the load for maximum efficiency.
category: electrical
keywords: [transformer efficiency calculator, transformer losses, iron loss copper loss, maximum efficiency transformer, no load loss, load loss, all day efficiency]
updated: {D}
variables:
  - {{ id: S, label: Transformer rating, suffix: kVA, default: 1000, min: 0 }}
  - {{ id: x, label: Load (fraction of rated), family: percent, unit: '%', default: 75, min: 0 }}
  - {{ id: pf, label: Load power factor, default: 0.9, min: 0.01, max: 1 }}
  - {{ id: Pi, label: No-load (core) loss, family: power, unit: kW, default: 1.4, min: 0 }}
  - {{ id: Pc, label: Full-load (copper) loss, family: power, unit: kW, default: 9.5, min: 0 }}
  - {{ id: Po, label: Output power, family: power, unit: kW, min: 0 }}
  - {{ id: Pl, label: Total losses, family: power, unit: kW, min: 0 }}
  - {{ id: eff, label: Efficiency, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: xm, label: Load for maximum efficiency, family: percent, unit: '%', min: 0 }}
equations:
  - Po = x * S * 1000 * pf
  - Pl = Pi + x^2 * Pc
  - eff = Po / (Po + Pl)
  - xm = sqrt(Pi / Pc)
faq:
  - q: How do I calculate transformer efficiency?
    a: Efficiency = output ÷ (output + core loss + x² × full-load copper loss), where x is the load as a fraction of rating.
  - q: When is a transformer most efficient?
    a: When copper loss equals core loss, at a load of √(core loss ÷ copper loss). For distribution transformers this is typically 35–55% load.
  - q: Why does copper loss vary with load squared?
    a: Copper loss is I²R, and current is proportional to load.
  - q: What are typical efficiencies?
    a: Large power and distribution transformers are 98–99.7% efficient at rated load. Small control transformers may be 90–96%.
related: [electrical/transformer-current, electrical/transformer-turns-ratio, electrical/transformer-short-circuit, electrical/kva-to-kw]
{L(('transformer-efficiency-calculation', 'Transformer Efficiency Calculation'), ('transformer-cooling-methods-onan-onaf', 'Transformer Cooling Methods: ONAN, ONAF'), ('transformer-maintenance-checklist', 'Transformer Maintenance Checklist'))}''', f'''
## How to use this calculator

Enter the **rating**, the **load** as a percentage, the load **power factor**, and the **no-load** and **full-load losses** from the test certificate or datasheet. You get the output, total losses, efficiency and the load at which efficiency peaks.

## The formulas

<p class="formula">η = x·S·PF ÷ (x·S·PF + P<sub>i</sub> + x²·P<sub>c</sub>)</p>

<p class="formula">Maximum efficiency at x = √(P<sub>i</sub> ÷ P<sub>c</sub>)</p>

## Efficiency vs load (1,000 kVA, 1.4 kW core loss, 9.5 kW copper loss)

| Load | PF 1.0 | PF 0.9 | PF 0.8 |
|---|---|---|---|
''' + ''.join(f"| {x*100:.0f}% | {teff(1000,x,1,1.4,9.5)*100:.2f}% | {teff(1000,x,0.9,1.4,9.5)*100:.2f}% | {teff(1000,x,0.8,1.4,9.5)*100:.2f}% |\n" for x in [0.1, 0.25, 0.384, 0.5, 0.75, 1.0, 1.1]) + f'''
Maximum efficiency occurs at √(1.4 ÷ 9.5) = **{math.sqrt(1.4/9.5)*100:.0f}% load**.

## Core loss vs copper loss

| Loss | Depends on | Present |
|---|---|---|
| Core (iron, no-load) | Voltage and frequency | Whenever energised, even with no load |
| Copper (load) | Current squared | Rises with load |

Because core loss is constant, a lightly loaded transformer runs 24 hours a day with relatively poor efficiency. Low-loss amorphous-core transformers cut core loss by 60–70%.

## All-day (energy) efficiency

For distribution transformers, compare energy rather than power: total kWh delivered ÷ (kWh delivered + core loss × 24 h + Σ copper loss × hours at each load). This is how loss capitalisation and energy-efficiency standards rank transformers.
''')

# 5 UPS sizing
page('electrical', 'ups-sizing', f'''
title: UPS Size Calculator (kVA)
description: Calculate the UPS kVA rating needed for your load from watts, power factor and a growth margin — for homes, offices, servers and control panels.
category: electrical
keywords: [ups size calculator, ups kva calculation, ups sizing, how to size a ups, ups capacity calculator, va to watts, online ups sizing]
updated: {D}
variables:
  - {{ id: P, label: Total load, family: power, unit: W, default: 4000, min: 0 }}
  - {{ id: pf, label: UPS output power factor, default: 0.9, min: 0.1, max: 1, help: 'Modern online UPSs are usually rated at 0.9 or 1.0 PF; older units at 0.8.' }}
  - {{ id: m, label: Growth and safety margin, family: percent, unit: '%', default: 25, min: 0 }}
  - {{ id: S, label: Minimum UPS rating, suffix: kVA, min: 0, decimals: 2 }}
  - {{ id: Pw, label: Minimum UPS watt rating, family: power, unit: kW, min: 0 }}
equations:
  - S = P * (1 + m) / pf / 1000
  - Pw = P * (1 + m)
faq:
  - q: How do I calculate UPS size?
    a: Add up the load in watts, add a margin of 20–30% for growth, and divide by the UPS power factor. 4 kW × 1.25 ÷ 0.9 ≈ 5.6 kVA, so choose a 6 kVA UPS.
  - q: Should I size by kVA or kW?
    a: Both. The load must not exceed either the kVA or the kW rating of the UPS. Check the datasheet for both figures.
  - q: How much margin should I add?
    a: 20–30% is common. It allows for future loads and keeps the UPS from running near full load, which improves reliability and battery runtime.
  - q: Does UPS size decide backup time?
    a: No. Backup time depends on the battery bank. See the battery backup calculator.
related: [everyday-life/inverter-battery-backup, electrical/kva-to-kw, electrical/amps-to-watts, everyday-life/electricity-cost]
{L(('ups-capacity-kva-calculation', 'UPS Capacity (kVA) Calculation'), ('calculate-battery-backup-time', 'How to Calculate Battery Backup Time'), ('ups-topology-comparison', 'UPS Topology Comparison: Offline, Line-Interactive, Online'))}''', '''
## How to use this calculator

Add up the **load** of everything the UPS will power, in watts. Enter the UPS's **output power factor** and a **margin** for growth. You get the minimum kVA and kW rating; choose the next standard size up.

## The formula

<p class="formula">UPS kVA = Load W × (1 + margin) ÷ PF ÷ 1,000</p>

## Typical loads

| Equipment | Typical power |
|---|---|
| Desktop PC with monitor | 150–300 W |
| Laptop | 45–100 W |
| Network switch (24-port) | 30–60 W |
| Wi-Fi router | 10–20 W |
| 1U server | 250–500 W |
| Laser printer (printing) | 400–800 W |
| PLC control panel | 100–500 W |
| LED lighting per room | 30–60 W |

Use measured or nameplate input power. Avoid connecting laser printers, heaters and motors to small UPSs — their inrush current can overload them.

## Standard UPS ratings

1, 2, 3, 5, 6, 10, 15, 20, 30, 40, 60, 80, 100, 120, 160 and 200 kVA are common sizes.

## Choosing the topology

| Type | Best for |
|---|---|
| Offline (standby) | Home PCs, small loads |
| Line-interactive | Offices, network racks — handles voltage swings |
| Online double-conversion | Servers, industrial control, medical, sensitive loads |

## Backup time

The UPS rating sets how much load it can carry; the battery sets how long. See the [battery backup calculator](/everyday-life/inverter-battery-backup/) to size the batteries.
''')

# 6 Earthing resistance
def rod(rho, L, d): return rho/(2*pi*L)*(math.log(8*L/d)-1)
page('electrical', 'earthing-resistance', f'''
title: Earthing Resistance Calculator (Earth Rod)
description: Calculate the earth resistance of a vertical earth rod or pipe electrode from soil resistivity, length and diameter — and how many rods you need.
category: electrical
keywords: [earthing resistance calculator, earth rod resistance, earth pit resistance, soil resistivity, earth electrode calculation, grounding resistance, pipe earthing]
updated: {D}
variables:
  - {{ id: rho, label: Soil resistivity, suffix: Ω·m, default: 100, min: 0 }}
  - {{ id: L, label: Rod length (buried), family: length, unit: m, imperialUnit: ft, default: 3, min: 0 }}
  - {{ id: d, label: Rod diameter, family: length, unit: mm, imperialUnit: in, default: 16, min: 0 }}
  - {{ id: R, label: Resistance of one rod, family: resistance, unit: ohm, min: 0 }}
equations:
  - R = rho / (2 * pi * L) * (ln(8 * L / d) - 1)
faq:
  - q: What is the formula for earth rod resistance?
    a: R = ρ ÷ (2πL) × (ln(8L ÷ d) − 1), the Dwight formula used in IEEE 142 and IS 3043, where ρ is soil resistivity, L the rod length and d its diameter.
  - q: What earth resistance is acceptable?
    a: Common targets are 1 Ω or less for substations, under 5 Ω for industrial and electrical equipment earthing, and up to 10 Ω for lightning protection. Follow your local standard.
  - q: Does a thicker rod lower resistance?
    a: Only slightly. Doubling the diameter reduces resistance by about 10–15%. Length and soil resistivity matter far more.
  - q: How do I reduce earth resistance?
    a: Drive longer rods, add more rods spaced at least their own length apart, or treat the soil around the electrode with backfill compound.
related: [electrical/earth-conductor-size, physics/ohms-law, electrical/transformer-short-circuit, electrical/cable-voltage-drop]
{L(('earthing-resistance-calculation', 'Earthing Resistance Calculation'), ('tn-tt-it-earthing-systems', 'TN, TT and IT Earthing Systems'), ('earthing-aspects-in-industrial-process-plants', 'Earthing in Industrial Process Plants'))}''', f'''
## How to use this calculator

Enter the **soil resistivity** (measured with a Wenner four-pin test, or estimated from the table), and the **length** and **diameter** of the rod or pipe. The calculator gives the resistance of a single electrode.

## The formula (Dwight)

<p class="formula">R = ρ ÷ (2πL) × [ln(8L ÷ d) − 1]</p>

## Soil resistivity

| Soil | Typical resistivity (Ω·m) |
|---|---|
| Marshy ground, clay with moisture | 2–50 |
| Loam and garden soil | 5–100 |
| Clay, sandy clay | 20–200 |
| Sand and gravel | 100–1,000 |
| Dry sand | 500–5,000 |
| Rock | 1,000–10,000+ |

Resistivity rises sharply when soil dries out or freezes, so measure in the dry season where possible.

## Single rod resistance (16 mm rod)

| Length | 50 Ω·m | 100 Ω·m | 300 Ω·m |
|---|---|---|---|
''' + ''.join(f"| {L} m | {rod(50,L,0.016):.1f} Ω | {rod(100,L,0.016):.1f} Ω | {rod(300,L,0.016):.1f} Ω |\n" for L in [1.2, 2, 3, 4.5, 6]) + '''
## Multiple rods

Rods in parallel do not divide resistance perfectly because their resistance areas overlap. Spaced at least one rod length apart, two rods give about 55–60% of one rod's resistance, three about 40%, and four about 33%. Closer spacing gives less improvement.

## Testing

Measure earth resistance with the fall-of-potential (three-pole) method, with the current spike at least 5–10 times the electrode length away. Clamp-on testers work only where there is a parallel return path.
''')

# 7 Earth conductor size
def adia(I, t, k): return I*math.sqrt(t)/k
page('electrical', 'earth-conductor-size', f'''
title: Earth Conductor Size Calculator (Adiabatic Equation)
description: Calculate the minimum protective earth conductor size from fault current and disconnection time with the adiabatic equation S = I√t / k (IEC 60364-5-54).
category: electrical
keywords: [earth conductor size calculation, earthing cable size, adiabatic equation, protective conductor size, i2t/k, earth wire size, cpc size]
updated: {D}
variables:
  - {{ id: I, label: Prospective fault current, family: current, unit: kA, default: 10, min: 0 }}
  - {{ id: t, label: Disconnection time, family: seconds, unit: s, default: 0.4, min: 0 }}
  - id: k
    label: Conductor and insulation (k factor)
    default: 143
    options:
      - {{ label: 'Copper, separate, PVC insulated (k 143)', value: 143 }}
      - {{ label: 'Copper, separate, XLPE/EPR insulated (k 176)', value: 176 }}
      - {{ label: 'Copper, core of PVC cable (k 115)', value: 115 }}
      - {{ label: 'Bare copper, no fire risk (k 159)', value: 159 }}
      - {{ label: 'Aluminium, separate, PVC insulated (k 95)', value: 95 }}
      - {{ label: 'Aluminium, separate, XLPE insulated (k 116)', value: 116 }}
      - {{ label: 'Steel, separate, PVC insulated (k 52)', value: 52 }}
  - {{ id: S, label: Minimum cross-section, family: area, unit: mm2, min: 0 }}
equations:
  - S = I * sqrt(t) / k * 1e-6
faq:
  - q: What is the adiabatic equation?
    a: S = √(I²t) ÷ k, the minimum conductor cross-section that can carry the fault current for the disconnection time without exceeding its final temperature. It is given in IEC 60364-5-54 and BS 7671.
  - q: Where does the k factor come from?
    a: It depends on the conductor material and the insulation’s initial and final temperatures. IEC 60364-5-54 Annex A tabulates the values.
  - q: What disconnection time should I use?
    a: The actual operating time of the protective device at the fault current, from its time–current curve. Final circuits often require 0.4 s; distribution circuits 5 s.
  - q: Can I use the simple table instead?
    a: Yes, IEC 60364-5-54 also allows sizing by the line conductor size — equal up to 16 mm², 16 mm² up to 35 mm², and half above that.
related: [electrical/earthing-resistance, electrical/transformer-short-circuit, electrical/cable-voltage-drop, electrical/kw-to-amps]
{L(('earth-conductor-size-calculation', 'Earth Conductor Size Calculation'), ('earth-fault-loop-impedance-zs-testing', 'Earth Fault Loop Impedance (Zs) Testing'), ('short-circuit-current-calculation', 'Short Circuit Current Calculation'))}''', f'''
## How to use this calculator

Enter the **prospective earth fault current**, the protective device's **disconnection time** at that current, and choose the **conductor and insulation** type. The result is the minimum cross-section; select the next standard size up.

## The adiabatic equation

<p class="formula">S = √(I² × t) ÷ k</p>

- **S** = cross-section in mm²
- **I** = fault current in A (rms)
- **t** = disconnection time in seconds
- **k** = material factor

## Minimum sizes (copper, PVC, k = 143)

| Fault current | 0.1 s | 0.4 s | 1 s | 5 s |
|---|---|---|---|---|
''' + ''.join(f"| {I} kA | {adia(I*1000,0.1,143):.1f} mm² | {adia(I*1000,0.4,143):.1f} mm² | {adia(I*1000,1,143):.1f} mm² | {adia(I*1000,5,143):.0f} mm² |\n" for I in [1, 2, 5, 10, 20, 31.5]) + '''
## Standard sizes

1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240 and 300 mm².

## Simplified method (IEC 60364-5-54 Table 54.2)

| Line conductor S | Protective conductor (same material) |
|---|---|
| S ≤ 16 mm² | S |
| 16 < S ≤ 35 mm² | 16 mm² |
| S > 35 mm² | S ÷ 2 |

## Check the earth fault loop too

A conductor large enough thermally must also have low enough impedance for the protective device to trip within the required time. Verify the earth fault loop impedance Zs on site.
''')

# 8 Voltage unbalance
page('electrical', 'voltage-unbalance', f'''
title: Voltage Unbalance Calculator (NEMA Method)
description: Calculate percentage voltage unbalance from three line voltages, plus the motor derating and extra temperature rise it causes.
category: electrical
keywords: [voltage unbalance calculator, phase unbalance, nema voltage unbalance, motor derating unbalance, three phase voltage imbalance, percent unbalance]
updated: {D}
variables:
  - {{ id: Va, label: Voltage L1–L2, family: voltage, unit: V, default: 412, min: 0 }}
  - {{ id: Vb, label: Voltage L2–L3, family: voltage, unit: V, default: 405, min: 0 }}
  - {{ id: Vc, label: Voltage L3–L1, family: voltage, unit: V, default: 418, min: 0 }}
  - {{ id: Vav, label: Average voltage, family: voltage, unit: V, min: 0 }}
  - {{ id: dev, label: Maximum deviation from average, family: voltage, unit: V, min: 0 }}
  - {{ id: u, label: Voltage unbalance, family: percent, unit: '%', min: 0 }}
  - {{ id: dt, label: Approximate extra winding temperature rise, family: percent, unit: '%', min: 0 }}
equations:
  - Vav = (Va + Vb + Vc) / 3
  - dev = max(max(abs(Va - Vav), abs(Vb - Vav)), abs(Vc - Vav))
  - u = dev / Vav
  - dt = 2 * (u * 100)^2 / 100
faq:
  - q: How do I calculate voltage unbalance?
    a: Average the three line voltages, find the largest deviation of any one from the average, and divide by the average. 412, 405 and 418 V give 1.6%.
  - q: What voltage unbalance is acceptable?
    a: NEMA MG 1 advises derating motors above 1% unbalance and not operating them above 5%. Many utilities aim to keep unbalance below 2%.
  - q: Why is unbalance bad for motors?
    a: It creates negative-sequence current that opposes rotation and heats the rotor. Temperature rise increases by about twice the square of the percentage unbalance.
  - q: What causes voltage unbalance?
    a: Unevenly distributed single-phase loads, a blown capacitor fuse, high-resistance connections, open-delta transformers and long feeders.
related: [electrical/three-phase-motor-power, electrical/induction-motor-slip, electrical/thd, electrical/cable-voltage-drop]
{L(('voltage-unbalance-calculation-motors', 'Voltage Unbalance Calculation for Motors'), ('motor-protection-relay-types', 'Motor Protection Relay Types'), ('power-quality-issues-vfd-plc', 'Power Quality Issues with VFDs and PLCs'))}''', '''
## How to use this calculator

Measure the three **line-to-line voltages** with a true-RMS meter and enter them. You get the average, the maximum deviation, the percentage unbalance and the approximate increase in motor winding temperature rise.

## The formula (NEMA MG 1)

<p class="formula">% unbalance = 100 × max. deviation from average ÷ average voltage</p>

Extra temperature rise ≈ 2 × (% unbalance)² percent.

## Example

412, 405 and 418 V:

- Average = 411.7 V
- Largest deviation = 411.7 − 405 = 6.7 V
- Unbalance = 6.7 ÷ 411.7 = **1.62%**
- Temperature rise increases by about **5.2%**

## Motor derating (NEMA MG 1, approximate)

| Voltage unbalance | Derating factor |
|---|---|
| 0–1% | 1.00 |
| 2% | 0.95 |
| 3% | 0.88 |
| 4% | 0.82 |
| 5% | 0.75 |

Do not operate motors above 5% unbalance.

## Current unbalance

A small voltage unbalance causes a much larger current unbalance — typically 6 to 10 times larger. A 2% voltage unbalance can produce 15–20% current unbalance, which may trip motor protection relays set for phase unbalance.

## Other definitions

IEC 61000 uses the ratio of negative-sequence to positive-sequence voltage. For small unbalances it gives results close to the NEMA method above.
''')

# 9 THD
page('electrical', 'thd', f'''
title: THD Calculator (Total Harmonic Distortion)
description: Calculate total harmonic distortion (THD) of voltage or current from the fundamental and harmonic magnitudes, with IEEE 519 limits.
category: electrical
keywords: [thd calculator, total harmonic distortion, harmonic distortion calculation, ieee 519 limits, thd formula, voltage thd, current thd]
updated: {D}
variables:
  - {{ id: h1, label: Fundamental (50/60 Hz) magnitude, default: 100, min: 0.0001 }}
  - {{ id: h3, label: 3rd harmonic, default: 2, min: 0 }}
  - {{ id: h5, label: 5th harmonic, default: 4, min: 0 }}
  - {{ id: h7, label: 7th harmonic, default: 3, min: 0 }}
  - {{ id: h11, label: 11th harmonic, default: 1.5, min: 0 }}
  - {{ id: h13, label: 13th harmonic, default: 1, min: 0 }}
  - {{ id: thd, label: Total harmonic distortion, family: percent, unit: '%', min: 0 }}
  - {{ id: rms, label: True RMS (same units as inputs), min: 0, decimals: 2 }}
equations:
  - thd = sqrt(h3^2 + h5^2 + h7^2 + h11^2 + h13^2) / h1
  - rms = sqrt(h1^2 + h3^2 + h5^2 + h7^2 + h11^2 + h13^2)
faq:
  - q: What is THD?
    a: Total harmonic distortion — the RMS of all harmonic components divided by the fundamental, expressed as a percentage.
  - q: What are the IEEE 519 voltage THD limits?
    a: 8% THD for systems up to 1 kV, 5% for 1–69 kV, 2.5% for 69–161 kV and 1.5% above 161 kV, at the point of common coupling.
  - q: Which harmonics do drives produce?
    a: Six-pulse VFDs and rectifiers mainly produce the 5th, 7th, 11th and 13th harmonics. Single-phase loads such as PCs and LED drivers add the 3rd.
  - q: Can I enter percentages instead of volts or amps?
    a: Yes — enter 100 for the fundamental and each harmonic as a percentage of it.
related: [electrical/power-factor-correction, electrical/voltage-unbalance, physics/decibel, electrical/kva-to-kw]
{L(('harmonic-distortion-thd-calculation-power-systems', 'Harmonic Distortion (THD) Calculation in Power Systems'), ('power-harmonics-explained', 'Power Harmonics Explained'), ('active-harmonic-filter-working-sizing', 'Active Harmonic Filter Working and Sizing'), ('neutral-conductor-sizing-harmonics', 'Neutral Conductor Sizing with Harmonics'))}''', '''
## How to use this calculator

Enter the **fundamental** and **harmonic magnitudes** from a power quality analyser — either in volts, amps or as percentages of the fundamental. You get the THD and the true RMS value. Enter 0 for harmonics you do not have.

## The formula

<p class="formula">THD = √(V₂² + V₃² + V₄² + …) ÷ V₁</p>

<p class="formula">True RMS = √(V₁² + V₂² + V₃² + …) = V₁ × √(1 + THD²)</p>

## Example

Fundamental 100; harmonics 2, 4, 3, 1.5 and 1 (3rd, 5th, 7th, 11th, 13th):

THD = √(4 + 16 + 9 + 2.25 + 1) ÷ 100 = **5.7%**

## IEEE 519-2014 voltage limits

| Bus voltage at PCC | Individual harmonic | THD |
|---|---|---|
| ≤ 1 kV | 5.0% | 8.0% |
| 1 kV – 69 kV | 3.0% | 5.0% |
| 69 kV – 161 kV | 1.5% | 2.5% |
| > 161 kV | 1.0% | 1.5% |

Current limits (TDD) depend on the ratio of short-circuit current to load current at the point of common coupling.

## Typical current THD

| Load | Current THD |
|---|---|
| 6-pulse VFD, no choke | 80–120% |
| 6-pulse VFD with 3–5% line reactor | 35–45% |
| 12-pulse drive | 10–15% |
| Active front-end drive | under 5% |
| LED lighting, SMPS | 20–150% |

## Problems caused by harmonics

- Overheating of transformers, cables and neutral conductors (triplen harmonics add in the neutral).
- Nuisance tripping of breakers and failure of capacitor banks through resonance.
- Errors in meters that are not true-RMS.
''')

# 11 Per-unit
page('electrical', 'per-unit', f'''
title: Per-Unit System Calculator (Base Impedance and Base Change)
description: Calculate base impedance, base current and per-unit impedance for power system studies — and convert per-unit values to a new base.
category: electrical
keywords: [per unit calculator, per unit system, base impedance, base current, change of base per unit, pu impedance, power system analysis]
updated: {D}
variables:
  - {{ id: Sb, label: Base power, suffix: MVA, default: 10, min: 0 }}
  - {{ id: Vb, label: Base voltage (line), family: voltage, unit: kV, default: 11, min: 0 }}
  - {{ id: Z, label: Actual impedance, family: resistance, unit: ohm, default: 0.6, min: 0 }}
  - {{ id: Zb, label: Base impedance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Ib, label: Base current, family: current, unit: A, min: 0 }}
  - {{ id: Zpu, label: Per-unit impedance, min: 0, decimals: 5 }}
  - {{ id: Sn, label: New base power, suffix: MVA, default: 100, min: 0 }}
  - {{ id: Vn, label: New base voltage, family: voltage, unit: kV, default: 11, min: 0 }}
  - {{ id: Zpn, label: Per-unit impedance on new base, min: 0, decimals: 5 }}
equations:
  - Zb = Vb^2 / (Sb * 1e6)
  - Ib = Sb * 1e6 / (sqrt(3) * Vb)
  - Zpu = Z / Zb
  - Zpn = Zpu * (Vb / Vn)^2 * (Sn / Sb)
faq:
  - q: What is the per-unit system?
    a: Expressing voltages, currents and impedances as fractions of chosen base values. It removes transformer ratios from calculations and makes equipment of different sizes easy to compare.
  - q: How do I calculate base impedance?
    a: Z_base = (kV_base)² ÷ MVA_base. For 11 kV and 10 MVA, Z_base = 12.1 Ω.
  - q: How do I change a per-unit value to a new base?
    a: Z_new = Z_old × (V_old ÷ V_new)² × (S_new ÷ S_old).
  - q: What is the link between % impedance and per unit?
    a: Percentage impedance is per-unit × 100. A transformer with 6% impedance has 0.06 pu on its own rating.
related: [electrical/transformer-short-circuit, electrical/transformer-current, electrical/kva-to-kw, electronics/reactance]
{L(('per-unit-system-power-system', 'Per-Unit System in Power Systems'), ('calculate-short-circuit-fault-current', 'How to Calculate Short Circuit Fault Current'))}''', f'''
## How to use this calculator

Choose a **base power** and **base voltage**, and enter an **actual impedance** in ohms. You get the base impedance, base current and per-unit impedance. Enter a **new base** to convert the per-unit value — for example from a transformer's own rating to a 100 MVA system base.

## The formulas

| Quantity | Formula |
|---|---|
| Base impedance | Z<sub>b</sub> = kV<sub>b</sub>² ÷ MVA<sub>b</sub> |
| Base current | I<sub>b</sub> = MVA<sub>b</sub> ÷ (√3 × kV<sub>b</sub>) |
| Per-unit | Z<sub>pu</sub> = Z<sub>Ω</sub> ÷ Z<sub>b</sub> |
| Change of base | Z<sub>new</sub> = Z<sub>old</sub> × (V<sub>old</sub>/V<sub>new</sub>)² × (S<sub>new</sub>/S<sub>old</sub>) |

## Base impedances

| Voltage | 10 MVA base | 100 MVA base |
|---|---|---|
''' + ''.join(f"| {v} kV | {v*v/10:.4g} Ω | {v*v/100:.4g} Ω |\n" for v in [0.415, 3.3, 6.6, 11, 22, 33, 66, 132, 220]) + '''
## Example: transformer on a system base

A 2.5 MVA transformer with 6.25% impedance on its own base, converted to 100 MVA:

Z = 0.0625 × (100 ÷ 2.5) = **2.5 pu** on 100 MVA.

## Short-circuit with per-unit

Fault current in pu = 1 ÷ Z<sub>total,pu</sub>; multiply by base current for amps. Adding source, transformer and cable impedances in per unit is how quick fault-level studies are done by hand.
''')

# 12 VFD braking resistor
page('electrical', 'braking-resistor', f'''
title: VFD Braking Resistor Calculator
description: Calculate the maximum braking resistor value and average power rating for a VFD braking chopper from DC bus voltage, braking power and duty cycle.
category: electrical
keywords: [braking resistor calculator, vfd braking resistor sizing, dynamic braking resistor, braking chopper, dc bus voltage, regenerative braking resistor]
updated: {D}
variables:
  - {{ id: Vdc, label: Chopper switch-on DC bus voltage, family: voltage, unit: V, default: 760, min: 0, help: 'Typically about 760–800 V for 400 V drives and 380–400 V for 230 V drives — see the drive manual.' }}
  - {{ id: Pb, label: Peak braking power, family: power, unit: kW, imperialUnit: hp, default: 15, min: 0 }}
  - {{ id: dc, label: Braking duty cycle, family: percent, unit: '%', default: 10, min: 0, max: 1 }}
  - {{ id: R, label: Maximum resistance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Pr, label: Continuous (average) resistor power, family: power, unit: kW, min: 0 }}
  - {{ id: Ipk, label: Peak braking current, family: current, unit: A, min: 0 }}
equations:
  - R = Vdc^2 / Pb
  - Pr = Pb * dc
  - Ipk = Vdc / R
faq:
  - q: How do I size a braking resistor?
    a: The resistance must be low enough to absorb the peak braking power — R ≤ V_dc² ÷ P — but not below the drive’s minimum allowed value. The power rating must cover the average braking power.
  - q: What is the braking power?
    a: The rate at which energy flows back from the motor and load while decelerating. For a quick estimate, take the motor rating for full-torque braking, or calculate from inertia and deceleration time.
  - q: What is the duty cycle?
    a: The fraction of time spent braking. A 10-second stop every 100 seconds is 10%. Cranes and lifts can be 20–50%.
  - q: What happens if the resistor is too small in ohms?
    a: The chopper current exceeds its rating and the drive trips or the chopper is damaged. Always respect the drive's minimum resistance.
related: [engineering/torque-power-speed, physics/ohms-law, electrical/three-phase-motor-power, physics/kinetic-energy]
{L(('vfd-braking-resistor-sizing', 'VFD Braking Resistor Sizing'), ('vfd-sizing-selection-guide', 'VFD Sizing and Selection Guide'), ('vfd-overload-trip-causes', 'VFD Overload Trip Causes'))}''', '''
## How to use this calculator

Enter the **DC bus voltage** at which the braking chopper switches on, the **peak braking power** and the **duty cycle**. You get the maximum resistor value, the average power rating and the peak current.

## The formulas

<p class="formula">R<sub>max</sub> = V<sub>DC</sub>² ÷ P<sub>brake</sub> &nbsp;·&nbsp; P<sub>avg</sub> = P<sub>brake</sub> × duty</p>

## Example

A 400 V drive (chopper at 760 V) braking 15 kW for 10% of the time:

- R<sub>max</sub> = 760² ÷ 15,000 = **38.5 Ω**
- Average power = **1.5 kW**

Choose a resistor between the drive's minimum resistance and 38.5 Ω, rated at least 1.5 kW continuous.

## Typical chopper thresholds

| Drive supply | Chopper threshold |
|---|---|
| 230 V | 375–400 V DC |
| 400–415 V | 750–800 V DC |
| 480 V | 800–850 V DC |
| 690 V | 1,100–1,200 V DC |

## Braking power from load inertia

For a flywheel or conveyor: P ≈ J × ω × Δω ÷ t (J in kg·m², ω in rad/s, t in s). Kinetic energy to dissipate is ½Jω².

## Alternatives

For long or frequent braking — cranes, centrifuges, downhill conveyors — a regenerative (active front-end) drive returns energy to the supply instead of wasting it as heat.
''')

# 13 Star-delta
page('electrical', 'star-delta-transformation', f'''
title: Star-Delta (Y-Δ) Transformation Calculator
description: Convert delta (Δ) resistances or impedances to an equivalent star (Y), and star to delta — for circuit analysis and network simplification.
category: electrical
keywords: [star delta transformation calculator, delta to star conversion, y delta transformation, delta to wye, wye to delta, network theorem, resistor network]
updated: {D}
variables:
  - {{ id: Rab, label: Delta resistance R_ab, family: resistance, unit: ohm, default: 30, min: 0 }}
  - {{ id: Rbc, label: Delta resistance R_bc, family: resistance, unit: ohm, default: 60, min: 0 }}
  - {{ id: Rca, label: Delta resistance R_ca, family: resistance, unit: ohm, default: 90, min: 0 }}
  - {{ id: Ra, label: Star resistance R_a, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Rb, label: Star resistance R_b, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Rc, label: Star resistance R_c, family: resistance, unit: ohm, min: 0 }}
equations:
  - Ra = Rab * Rca / (Rab + Rbc + Rca)
  - Rb = Rab * Rbc / (Rab + Rbc + Rca)
  - Rc = Rbc * Rca / (Rab + Rbc + Rca)
faq:
  - q: How do I convert delta to star?
    a: Each star resistance equals the product of the two delta resistances touching that node, divided by the sum of all three. R_a = R_ab × R_ca ÷ (R_ab + R_bc + R_ca).
  - q: How do I convert star to delta?
    a: Each delta resistance equals the sum of the pairwise products of the star resistances divided by the opposite star resistance. Enter the star values here and press × on the delta fields to solve backwards.
  - q: What about balanced loads?
    a: For three equal resistances, R_star = R_delta ÷ 3, and R_delta = 3 × R_star.
  - q: Does this work for AC impedances?
    a: Yes, with complex impedances. This calculator handles resistances (or magnitudes of identical-angle impedances).
related: [physics/resistors-series-parallel, physics/ohms-law, electronics/wheatstone-bridge, electrical/three-phase-motor-power]
{L(('star-delta-transformation-formula', 'Star-Delta Transformation Formula'), ('dol-vs-star-delta-starter-which-to-use', 'DOL vs Star-Delta Starter: Which to Use'))}''', '''
## How to use this calculator

Enter the three **delta resistances** between terminals a–b, b–c and c–a. The calculator gives the equivalent **star resistances** connected from each terminal to a common centre point. To go from star to delta, enter the star values and solve for the delta fields with the × buttons.

## Delta to star

<p class="formula">R<sub>a</sub> = R<sub>ab</sub>R<sub>ca</sub> ÷ ΣR &nbsp;·&nbsp; R<sub>b</sub> = R<sub>ab</sub>R<sub>bc</sub> ÷ ΣR &nbsp;·&nbsp; R<sub>c</sub> = R<sub>bc</sub>R<sub>ca</sub> ÷ ΣR</p>

## Star to delta

<p class="formula">R<sub>ab</sub> = (R<sub>a</sub>R<sub>b</sub> + R<sub>b</sub>R<sub>c</sub> + R<sub>c</sub>R<sub>a</sub>) ÷ R<sub>c</sub></p>

and similarly for R<sub>bc</sub> (÷ R<sub>a</sub>) and R<sub>ca</sub> (÷ R<sub>b</sub>).

## Example

Delta 30, 60 and 90 Ω (sum 180 Ω):

- R<sub>a</sub> = 30 × 90 ÷ 180 = **15 Ω**
- R<sub>b</sub> = 30 × 60 ÷ 180 = **10 Ω**
- R<sub>c</sub> = 60 × 90 ÷ 180 = **30 Ω**

## When to use it

- Simplifying bridge networks that cannot be reduced with series and parallel rules alone.
- Converting delta-connected loads to star for per-phase calculations in three-phase systems.
- Analysing the [Wheatstone bridge](/electronics/wheatstone-bridge/) when it is unbalanced.

## Star-delta motor starting

A motor started in star sees 1/√3 of line voltage, so starting current and torque fall to one third of their direct-on-line values. After a few seconds, the starter switches to delta for full voltage.
''')
print('D1 done')
