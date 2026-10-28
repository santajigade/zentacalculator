import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
from ib import intro
D = '2026-10-28'; r3 = math.sqrt(3); pi = math.pi

# ======================= ELECTRICAL =======================
page('electrical', 'motor-starting-current', f'''
title: Motor Starting Current Calculator (DOL, Star-Delta, Soft Starter)
description: Estimate the starting (inrush) current of an induction motor for DOL, star-delta, autotransformer and soft-starter starting from full-load current.
category: electrical
{intro("A three-phase induction motor started direct-on-line (DOL) draws 6–8 times its full-load current for a few seconds, which can dip the supply voltage and trip protection. Reduced-voltage starters cut that inrush — compare the options in [DOL vs star-delta starter](ib:dol-vs-star-delta-starter-which-to-use) and [motor starting methods compared](ib:motor-starting-methods-compared). This motor starting current calculator estimates the inrush for each method.")}
keywords: [motor starting current calculator, dol starting current, star delta starting current, inrush current motor, locked rotor current, soft starter current, motor starting current formula]
updated: {D}
variables:
  - {{ id: Ifl, label: Motor full-load current (FLC), family: current, unit: A, default: 20, min: 0 }}
  - {{ id: k, label: DOL starting current (× FLC), default: 6.5, min: 1, help: 'Locked-rotor current ratio from the motor datasheet — typically 6–8 for IE2/IE3 motors.' }}
  - id: m
    label: Starting method
    default: 0.333333
    options:
      - {{ label: 'Direct-on-line (100% voltage)', value: 1 }}
      - {{ label: 'Star-delta (58% voltage)', value: 0.333333 }}
      - {{ label: 'Autotransformer 80% tap', value: 0.64 }}
      - {{ label: 'Autotransformer 65% tap', value: 0.4225 }}
      - {{ label: 'Autotransformer 50% tap', value: 0.25 }}
  - {{ id: Idol, label: DOL starting current, family: current, unit: A, min: 0 }}
  - {{ id: Is, label: Line starting current with chosen method, family: current, unit: A, min: 0 }}
  - {{ id: Ts, label: Starting torque (% of DOL torque), family: percent, unit: '%', min: 0 }}
equations:
  - Idol = k * Ifl
  - Is = Idol * m
  - Ts = m
faq:
  - q: What is the starting current of a motor?
    a: Started direct-on-line, an induction motor draws its locked-rotor current — typically 6 to 8 times full-load current — until it approaches full speed.
  - q: How much does a star-delta starter reduce starting current?
    a: To one third of the DOL value. Each winding sees 1/√3 of line voltage in star, and line current is one third. Starting torque also falls to one third.
  - q: Why does starting torque fall as much as current?
    a: Torque is proportional to voltage squared. With an autotransformer, line current and torque both scale with the tap ratio squared.
  - q: What about soft starters and VFDs?
    a: A soft starter typically limits current to 2.5–4 × FLC; a VFD can start a motor at about 1–1.5 × FLC with full torque.
related: [electrical/three-phase-motor-power, electrical/induction-motor-slip, electrical/cable-voltage-drop, electrical/generator-size]
''', '''
## How to use the motor starting current calculator

Enter the motor's **full-load current** from the nameplate, the **DOL starting current ratio** (I<sub>A</sub>/I<sub>N</sub> from the datasheet) and choose the **starting method**. You get the DOL inrush, the line current with your starter and the starting torque as a percentage of DOL torque.

## Motor starting current formula

<p class="formula">I<sub>DOL</sub> = k × I<sub>FL</sub> &nbsp;·&nbsp; I<sub>start</sub> = I<sub>DOL</sub> × (V<sub>start</sub>/V<sub>rated</sub>)²</p>

For star-delta the factor is (1/√3)² = 1/3; for autotransformers it is the tap ratio squared.

## Comparison of starting methods

| Method | Line current (× DOL) | Torque (× DOL) | Typical line current |
|---|---|---|---|
| Direct-on-line | 1.00 | 1.00 | 6–8 × FLC |
| Star-delta | 0.33 | 0.33 | 2–2.7 × FLC |
| Autotransformer 80% | 0.64 | 0.64 | 4–5 × FLC |
| Autotransformer 65% | 0.42 | 0.42 | 2.5–3.4 × FLC |
| Soft starter (current limit) | adjustable | low | 2.5–4 × FLC |
| VFD | — | up to 1.5 × rated | 1–1.5 × FLC |

## Example

A 11 kW, 415 V motor with 20 A FLC and a 6.5 × starting ratio:

- DOL starting current = **130 A**
- Star-delta starting current = **43 A**, with one third of the DOL starting torque

## Choosing a method

- **DOL** suits small motors (typically up to 7.5–11 kW) on a stiff supply.
- **Star-delta** suits pumps and fans that start lightly loaded, but causes a current spike at changeover.
- **Soft starters** give smooth acceleration and reduce mechanical shock.
- **VFDs** give the lowest current and full torque, plus speed control.

Check the voltage dip a large motor causes on a generator or weak supply — see the [generator size calculator](/electrical/generator-size/).
''')

page('electrical', 'generator-size', f'''
title: Generator Size Calculator (DG Set kVA)
description: Calculate the diesel generator (DG set) kVA rating needed for your connected load, power factor, future margin and largest motor start.
category: electrical
{intro("A diesel generator must supply the running load and also survive the surge when the largest motor starts. Undersized sets stall or trip; oversized sets run lightly loaded and wet-stack. This generator size calculator gives the minimum kVA from both checks — see [how to calculate generator size for industrial load](ib:how-to-calculate-generator-size-industrial-load) and how an [AMF panel auto-starts a DG](ib:amf-panel-working-dg-auto-start).")}
keywords: [generator size calculator, dg set size calculation, diesel generator kva calculator, generator sizing for motor starting, kva required for load, genset sizing]
updated: {D}
variables:
  - {{ id: P, label: Total running load, family: power, unit: kW, imperialUnit: hp, default: 80, min: 0 }}
  - {{ id: pf, label: Load power factor, default: 0.8, min: 0.1, max: 1 }}
  - {{ id: mg, label: Future and safety margin, family: percent, unit: '%', default: 20, min: 0 }}
  - {{ id: Pm, label: Largest motor (started last), family: power, unit: kW, imperialUnit: hp, default: 22, min: 0 }}
  - {{ id: ks, label: Starting kVA per motor kW, default: 2.5, min: 0, help: 'About 6–7 for DOL, 2–2.5 for star-delta, 1.5–2.5 for soft starters, 1.2–1.5 for VFDs.' }}
  - {{ id: Sr, label: kVA for running load, suffix: kVA, min: 0, decimals: 1 }}
  - {{ id: Ss, label: kVA during largest motor start, suffix: kVA, min: 0, decimals: 1 }}
  - {{ id: S, label: Recommended minimum generator rating, suffix: kVA, min: 0, decimals: 1 }}
equations:
  - Sr = P / 1000 / pf * (1 + mg)
  - Ss = ((P - Pm) / 1000 / pf + Pm / 1000 * ks) / 1.5
  - S = max(Sr, Ss)
faq:
  - q: How do I calculate generator size?
    a: Divide the running load in kW by the power factor (usually 0.8) to get kVA, add 20–25% margin, and check that the set can also handle the largest motor starting.
  - q: Why use 0.8 power factor?
    a: Generators are rated in kVA at 0.8 PF. A 100 kVA set delivers up to 80 kW.
  - q: Why does motor starting matter?
    a: A motor draws several times its running kVA when starting. Most generators can supply about 1.5–2 times their rating briefly while keeping voltage dip around 15–20%; this calculator uses 1.5.
  - q: Is a bigger generator always better?
    a: No. Diesel sets run best above 30–40% load; long periods at light load cause wet-stacking and carbon build-up.
related: [electrical/motor-starting-current, electrical/ups-sizing, electrical/kva-to-kw, electrical/three-phase-motor-power]
''', '''
## How to use the generator size calculator

Enter the **total running load** in kW, its **power factor**, a **margin** for growth, the **largest motor** that starts while the rest of the load is running, and its **starting kVA per kW** for the starter type. The calculator gives the kVA needed for running and for the motor start; choose a standard rating at or above the larger figure.

## Generator size formula

<p class="formula">kVA<sub>run</sub> = kW ÷ PF × (1 + margin)</p>

<p class="formula">kVA<sub>start</sub> = [(kW − kW<sub>motor</sub>) ÷ PF + kW<sub>motor</sub> × k<sub>s</sub>] ÷ 1.5</p>

The 1.5 factor assumes the generator can carry 150% of its rating momentarily during motor starting while keeping voltage dip acceptable. Check the manufacturer's motor-starting curves for an exact selection.

## Example

80 kW running load at 0.8 PF with 20% margin; the last motor is 22 kW on a star-delta starter:

- Running: 80 ÷ 0.8 × 1.2 = **120 kVA**
- Starting: (58 ÷ 0.8 + 22 × 2.5) ÷ 1.5 = **85 kVA**
- Choose **125 kVA**

## Starting kVA per kW by starter

| Starter | kVA per kW (approx.) |
|---|---|
| Direct-on-line | 6–7 |
| Star-delta | 2–2.5 |
| Autotransformer | 3–4 |
| Soft starter | 1.5–2.5 |
| VFD | 1.2–1.5 |

## Standard DG set ratings (India)

15, 20, 25, 30, 40, 62.5, 82.5, 100, 125, 160, 200, 250, 320, 380, 500, 625, 750, 1,010, 1,250, 1,500 and 2,000 kVA.

## Other checks

- **Non-linear loads** (VFDs, UPSs) may need generator derating or a larger alternator.
- **Altitude and temperature** reduce output — derate above 1,000 m or 40 °C.
- **Step loading**: start the largest motors first, when the generator is lightly loaded.
''')

page('electrical', 'ct-burden', f'''
title: CT Burden Calculator (VA)
description: Calculate current transformer (CT) burden in VA from secondary current, lead length, cable size and relay or meter burden — and check it against the CT rating.
category: electrical
{intro("A current transformer (CT) can only hold its accuracy while the load on its secondary — the burden — stays within its VA rating. Long leads and thin cable add more burden than people expect, especially with 5 A secondaries. This CT burden calculator adds up leads and devices; see [CT burden calculation](ib:ct-burden-calculation-va) and the [current transformer working principle](ib:current-transformer-working-principle).")}
keywords: [ct burden calculator, current transformer burden calculation, ct va calculation, ct lead burden, 1a vs 5a ct, ct sizing]
updated: {D}
variables:
  - id: Is
    label: CT secondary rating
    default: 5
    options:
      - {{ label: 5 A, value: 5 }}
      - {{ label: 1 A, value: 1 }}
  - {{ id: L, label: Lead length (one way), family: length, unit: m, imperialUnit: ft, default: 50, min: 0 }}
  - {{ id: A, label: Cable cross-section, family: area, unit: mm2, default: 2.5, min: 0 }}
  - {{ id: Rd, label: Device burden (relay + meter + transducer), suffix: VA, default: 2, min: 0 }}
  - {{ id: Rl, label: Lead loop resistance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Bl, label: Lead burden, suffix: VA, min: 0, decimals: 2 }}
  - {{ id: B, label: Total burden, suffix: VA, min: 0, decimals: 2 }}
equations:
  - Rl = 2 * L * 1.72e-8 / A
  - Bl = Is^2 * Rl
  - B = Bl + Rd
faq:
  - q: What is CT burden?
    a: The total load on the CT secondary — relays, meters and leads — usually expressed in VA at rated secondary current. VA = I² × R.
  - q: Why are 1 A CTs preferred for long cable runs?
    a: Lead burden rises with current squared, so a 1 A secondary has 25 times less lead burden than a 5 A secondary over the same cable.
  - q: What happens if the burden exceeds the CT rating?
    a: Accuracy degrades and protection CTs may saturate during faults, causing relays to under-reach or operate slowly.
  - q: Is it dangerous to open a CT secondary?
    a: Yes. An open-circuited CT secondary can develop thousands of volts. Always short the secondary before disconnecting a meter or relay.
related: [electrical/transformer-current, electrical/transformer-short-circuit, physics/ohms-law, electrical/wire-resistance]
''', '''
## How to use the CT burden calculator

Choose the **CT secondary rating**, enter the **one-way lead length** and **cable size**, and the **burden of the connected devices** from their datasheets. The calculator gives the lead loop resistance, lead burden and total burden. Select a CT whose rated burden is at least the total — ideally 25–100% of it, since accuracy is specified within that band.

## CT burden formula

<p class="formula">R<sub>leads</sub> = 2 × L × ρ ÷ A &nbsp;·&nbsp; VA<sub>leads</sub> = I<sub>s</sub>² × R<sub>leads</sub></p>

with copper resistivity ρ = 1.72 × 10⁻⁸ Ω·m at 20 °C.

## Lead burden: 5 A vs 1 A (2.5 mm² copper)

| One-way length | Loop resistance | 5 A lead burden | 1 A lead burden |
|---|---|---|---|
''' + ''.join(f"| {L} m | {2*L*1.72e-8/2.5e-6:.3f} Ω | {25*2*L*1.72e-8/2.5e-6:.2f} VA | {2*L*1.72e-8/2.5e-6:.3f} VA |\n" for L in [5, 10, 25, 50, 100, 200]) + '''
## Typical device burdens

| Device | Burden |
|---|---|
| Digital multifunction meter | 0.1–0.5 VA |
| Numerical protection relay | 0.1–0.5 VA |
| Electromechanical overcurrent relay | 3–10 VA |
| Moving-iron ammeter | 1–3 VA |

## Standard CT burdens

2.5, 5, 10, 15 and 30 VA. Metering CTs are specified as e.g. **0.5 / 5 VA**; protection CTs as e.g. **5P20 / 15 VA**.

## Safety

Never open-circuit a live CT secondary — short it first with the test block or shorting link.
''')

page('electrical', 'wire-resistance', f'''
title: Wire Resistance Calculator (Copper and Aluminium)
description: Calculate the resistance of a copper or aluminium wire or cable from length, cross-section and temperature — plus resistance per km.
category: electrical
{intro("Every conductor has resistance that rises with length and temperature and falls with cross-section. It sets voltage drop, cable heating and the burden on instrument loops. This wire resistance calculator handles copper and aluminium at any temperature — see [what resistance is](ib:what-is-resistance) and [electrical conductivity explained](ib:electrical-conductivity-explained).")}
keywords: [wire resistance calculator, cable resistance calculator, copper wire resistance, resistance per km, conductor resistance at temperature, aluminium cable resistance, resistivity calculator]
updated: {D}
variables:
  - id: rho
    label: Conductor material
    default: 1.724e-8
    options:
      - {{ label: Copper (annealed), value: 1.724e-8 }}
      - {{ label: Aluminium, value: 2.826e-8 }}
      - {{ label: Silver, value: 1.59e-8 }}
      - {{ label: Gold, value: 2.44e-8 }}
      - {{ label: Nichrome, value: 1.1e-6 }}
  - {{ id: L, label: Length (total conductor length), family: length, unit: m, imperialUnit: ft, default: 100, min: 0 }}
  - {{ id: A, label: Cross-section area, family: area, unit: mm2, default: 1.5, min: 0 }}
  - {{ id: T, label: Conductor temperature, suffix: °C, default: 20 }}
  - {{ id: R20, label: Resistance at 20 °C, family: resistance, unit: ohm, min: 0 }}
  - {{ id: R, label: Resistance at temperature, family: resistance, unit: ohm, min: 0 }}
  - {{ id: rkm, label: Resistance per km (at temperature), suffix: Ω/km, min: 0, decimals: 3 }}
equations:
  - R20 = rho * L / A
  - R = R20 * (1 + 0.00393 * (T - 20))
  - rkm = R / L * 1000
faq:
  - q: How do I calculate wire resistance?
    a: R = ρ × L ÷ A, where ρ is the resistivity, L the length and A the cross-section. 100 m of 1.5 mm² copper has about 1.15 Ω at 20 °C.
  - q: How does temperature affect resistance?
    a: Copper and aluminium resistance rises about 0.39–0.40% per °C. At 70 °C, copper resistance is about 20% higher than at 20 °C.
  - q: Should I use the one-way or round-trip length?
    a: For a circuit, use the total conductor length — twice the one-way distance for a two-wire circuit.
  - q: Why is aluminium cable larger than copper?
    a: Aluminium's resistivity is about 64% higher, so it needs roughly 1.6 times the cross-section for the same resistance.
related: [electrical/cable-voltage-drop, physics/ohms-law, engineering/loop-resistance, electrical/ct-burden]
''', '''
## How to use the wire resistance calculator

Choose the **material**, enter the **total conductor length**, the **cross-section** and the **operating temperature**. You get the resistance at 20 °C, at your temperature, and per kilometre.

## Wire resistance formula

<p class="formula">R = ρ × L ÷ A &nbsp;·&nbsp; R<sub>T</sub> = R₂₀ × [1 + α(T − 20)]</p>

The calculator uses α = 0.00393 /°C, the temperature coefficient of copper; aluminium (0.00403 /°C) is very close.

## Copper conductor resistance at 20 °C

| Size | Ω/km (calculated) | Typical IEC 60228 max (Class 2) |
|---|---|---|
''' + ''.join(f"| {a} mm² | {1.724e-8/(a*1e-6)*1000:.2f} | {m} |\n" for a, m in [(0.5, '36.0'), (0.75, '24.5'), (1, '18.1'), (1.5, '12.1'), (2.5, '7.41'), (4, '4.61'), (6, '3.08'), (10, '1.83'), (16, '1.15'), (25, '0.727')]) + '''
Real stranded conductors are slightly higher than the solid-wire calculation because of stranding and compaction.

## AWG equivalents

| AWG | Area | Copper Ω/km |
|---|---|---|
| 24 | 0.205 mm² | 84.2 |
| 20 | 0.519 mm² | 33.3 |
| 18 | 0.823 mm² | 21.0 |
| 16 | 1.31 mm² | 13.2 |
| 14 | 2.08 mm² | 8.29 |
| 12 | 3.31 mm² | 5.21 |
| 10 | 5.26 mm² | 3.28 |

## Uses

- Voltage drop — see the [cable voltage drop calculator](/electrical/cable-voltage-drop/).
- 4–20 mA loop budgets — see the [loop resistance calculator](/engineering/loop-resistance/).
- RTD lead-wire error: 2-wire RTDs read high by the lead resistance (about 0.39 °C per 0.15 Ω for a Pt100).
''')

page('electrical', 'line-phase-voltage', f'''
title: Line and Phase Voltage Calculator (Star and Delta)
description: Convert between line and phase voltage and current for star (wye) and delta connections — with three-phase power from either.
category: electrical
{intro("In a three-phase system, line values are measured between lines and phase values across each winding or load. In star (wye), line voltage is √3 times phase voltage; in delta, line current is √3 times phase current. This line and phase voltage calculator converts both ways — see [star vs delta connection](ib:star-vs-delta-connection) explained.")}
keywords: [line voltage phase voltage calculator, star delta voltage, phase to line voltage, 415 to 240, wye voltage calculator, line current phase current delta, three phase voltage]
updated: {D}
variables:
  - id: c
    label: Connection
    default: 1
    options:
      - {{ label: Star (wye), value: 1 }}
      - {{ label: Delta, value: 0 }}
  - {{ id: VL, label: Line voltage, family: voltage, unit: V, default: 415, min: 0 }}
  - {{ id: Vp, label: Phase voltage, family: voltage, unit: V, min: 0 }}
  - {{ id: IL, label: Line current, family: current, unit: A, default: 10, min: 0 }}
  - {{ id: Ip, label: Phase current, family: current, unit: A, min: 0 }}
  - {{ id: pf, label: Power factor, default: 0.85, min: 0, max: 1 }}
  - {{ id: P, label: Total real power, family: power, unit: kW, min: 0 }}
equations:
  - Vp = VL / (c * sqrt(3) + (1 - c))
  - Ip = IL / ((1 - c) * sqrt(3) + c)
  - P = sqrt(3) * VL * IL * pf
faq:
  - q: What is the relationship between line and phase voltage in star?
    a: V_line = √3 × V_phase. A 415 V system has about 240 V from each line to neutral.
  - q: What about delta?
    a: Line and phase voltages are equal, but line current is √3 times the phase (winding) current.
  - q: Is three-phase power different for star and delta?
    a: No. P = √3 × V_L × I_L × PF for both, using line values.
  - q: Why is 400 V three-phase paired with 230 V single-phase?
    a: Because 400 ÷ √3 ≈ 230 V — the single-phase supply is one phase of the star system.
related: [electrical/kw-to-amps, electrical/three-phase-motor-power, electrical/star-delta-transformation, electrical/motor-starting-current]
''', '''
## How to use the line and phase voltage calculator

Choose **star** or **delta**, enter the **line voltage** and **line current** (or the phase values, using the × buttons), and the **power factor**. The calculator gives the phase voltage and current and the total three-phase power.

## Line and phase formulas

| Connection | Voltage | Current |
|---|---|---|
| Star (wye) | V<sub>L</sub> = √3 × V<sub>ph</sub> | I<sub>L</sub> = I<sub>ph</sub> |
| Delta | V<sub>L</sub> = V<sub>ph</sub> | I<sub>L</sub> = √3 × I<sub>ph</sub> |

<p class="formula">P = √3 × V<sub>L</sub> × I<sub>L</sub> × PF = 3 × V<sub>ph</sub> × I<sub>ph</sub> × PF</p>

## Common system voltages

| Line voltage | Phase (line–neutral) voltage | Where |
|---|---|---|
''' + ''.join(f"| {v} V | {v/r3:.0f} V | {w} |\n" for v, w in [(208, 'North America (commercial)'), (380, 'Older IEC, parts of Asia'), (400, 'Europe, IEC standard'), (415, 'India, UK, Australia'), (440, 'Marine, older Indian plants'), (480, 'North America (industrial)'), (690, 'Large motors, mining'), (11000, 'MV distribution'), (33000, 'Sub-transmission')]) + '''
## Motor windings

A motor nameplate marked **Δ 415 V / Y 690 V** has windings rated at 415 V. On a 415 V supply it runs in delta, and can be started in star (where each winding gets 240 V) — the basis of the star-delta starter. See the [motor starting current calculator](/electrical/motor-starting-current/).
''')

page('electrical', 'earth-fault-loop-impedance', f'''
title: Earth Fault Loop Impedance Calculator (Zs)
description: Calculate prospective earth fault current from loop impedance Zs, or the maximum Zs for an MCB to trip within 0.4 s — for TN systems.
category: electrical
{intro("For an MCB or fuse to disconnect an earth fault quickly, the earth fault loop impedance (Zs) must be low enough to let a large fault current flow. Testing Zs is part of every installation inspection — see [earth fault loop impedance (Zs) testing](ib:earth-fault-loop-impedance-zs-testing). This earth fault loop impedance calculator gives the fault current and the maximum Zs for common MCBs.")}
keywords: [earth fault loop impedance calculator, zs calculator, maximum zs mcb, prospective fault current, earth loop impedance, disconnection time, ze r1 r2]
updated: {D}
variables:
  - {{ id: U0, label: Nominal voltage to earth (U0), family: voltage, unit: V, default: 230, min: 0 }}
  - {{ id: Ze, label: External loop impedance (Ze), family: resistance, unit: ohm, default: 0.35, min: 0 }}
  - {{ id: R12, label: Circuit R1 + R2, family: resistance, unit: ohm, default: 0.4, min: 0 }}
  - id: k
    label: MCB type (instantaneous trip multiple)
    default: 5
    options:
      - {{ label: Type B (5 × In), value: 5 }}
      - {{ label: Type C (10 × In), value: 10 }}
      - {{ label: Type D (20 × In), value: 20 }}
  - {{ id: In, label: MCB rating, family: current, unit: A, default: 32, min: 0 }}
  - {{ id: Zs, label: Earth fault loop impedance (Zs), family: resistance, unit: ohm, min: 0 }}
  - {{ id: If, label: Prospective earth fault current, family: current, unit: A, min: 0 }}
  - {{ id: Zmax, label: Maximum Zs for instantaneous trip, family: resistance, unit: ohm, min: 0 }}
  - {{ id: ok, label: Margin (positive = MCB trips instantly), family: resistance, unit: ohm }}
equations:
  - Zs = Ze + R12
  - If = 0.95 * U0 / Zs
  - Zmax = 0.95 * U0 / (k * In)
  - ok = Zmax - Zs
faq:
  - q: What is earth fault loop impedance?
    a: The total impedance of the path a fault current takes — transformer winding, line conductor, the fault, the protective conductor and the return path. Zs = Ze + (R1 + R2).
  - q: How do I find the maximum Zs for an MCB?
    a: Max Zs = Cmin × U0 ÷ Ia, where Ia is the current that trips the MCB instantly (5 × In for Type B) and Cmin = 0.95. A 32 A Type B gives 1.37 Ω.
  - q: Why apply a 0.8 factor when testing?
    a: Tests are done at ambient temperature, but conductors run hotter in service with higher resistance. Measured Zs should be at most about 80% of the tabulated maximum.
  - q: What are typical Ze values?
    a: In the UK, typical maximums are 0.8 Ω for TN-S and 0.35 Ω for TN-C-S (PME) supplies.
related: [electrical/earth-conductor-size, electrical/earthing-resistance, electrical/transformer-short-circuit, electrical/wire-resistance]
''', '''
## How to use the earth fault loop impedance calculator

Enter the **voltage to earth**, the **external loop impedance Ze** (measured at the origin or from the supplier), the circuit's **R1 + R2** (line plus protective conductor resistance), the **MCB type** and its **rating**. You get Zs, the prospective fault current, the maximum Zs for instantaneous tripping, and the margin.

## Earth fault loop impedance formula

<p class="formula">Z<sub>s</sub> = Z<sub>e</sub> + (R₁ + R₂) &nbsp;·&nbsp; I<sub>f</sub> = C<sub>min</sub> × U₀ ÷ Z<sub>s</sub></p>

<p class="formula">Z<sub>s,max</sub> = C<sub>min</sub> × U₀ ÷ I<sub>a</sub></p>

with C<sub>min</sub> = 0.95 and I<sub>a</sub> the instantaneous trip current of the device.

## Maximum Zs for MCBs (230 V, 0.4 s)

| Rating | Type B | Type C | Type D |
|---|---|---|---|
''' + ''.join(f"| {i} A | {0.95*230/(5*i):.2f} Ω | {0.95*230/(10*i):.2f} Ω | {0.95*230/(20*i):.2f} Ω |\n" for i in [6, 10, 16, 20, 25, 32, 40, 50, 63]) + '''
For measured values at room temperature, compare against about 80% of these figures.

## Reducing Zs

- Use larger line and protective conductors (lower R1 + R2).
- Shorten the circuit or move the distribution board closer.
- Use RCD protection where Zs cannot be reduced enough — in TT systems this is the usual solution.

## Measuring R1 + R2

Link line and protective conductor at the distribution board and measure between them at each outlet with a low-resistance ohmmeter. Copper 2.5/1.5 mm² cable has about 19.5 mΩ/m for R1 + R2 at 20 °C.
''')

page('electrical', 'transformer-size', f'''
title: Transformer Size Calculator (kVA Rating from Load)
description: Calculate the transformer kVA rating needed for your connected load from kW, power factor, diversity factor and future growth — and pick the next standard size.
category: electrical
{intro("Choosing a transformer means turning the connected load into a kVA figure, allowing for diversity, power factor and future growth. Too small and it overheats; too large and it wastes money and no-load losses. This transformer size calculator follows the usual method — see [how to calculate transformer kVA rating](ib:how-to-calculate-transformer-kva-rating).")}
keywords: [transformer size calculator, transformer kva calculation, transformer sizing, kva rating calculator, distribution transformer selection, diversity factor, how to size a transformer]
updated: {D}
variables:
  - {{ id: P, label: Total connected load, family: power, unit: kW, imperialUnit: hp, default: 500, min: 0 }}
  - {{ id: df, label: Demand / diversity factor, default: 0.7, min: 0.01, max: 1, help: 'Fraction of connected load expected to run at the same time — often 0.6–0.8 for industrial plants.' }}
  - {{ id: pf, label: Power factor (after correction), default: 0.9, min: 0.1, max: 1 }}
  - {{ id: g, label: Future growth margin, family: percent, unit: '%', default: 25, min: 0 }}
  - {{ id: Pd, label: Maximum demand, family: power, unit: kW, min: 0 }}
  - {{ id: S, label: Required transformer rating, suffix: kVA, min: 0, decimals: 0 }}
equations:
  - Pd = P * df
  - S = Pd / 1000 / pf * (1 + g)
faq:
  - q: How do I calculate transformer size?
    a: Multiply connected load by the diversity factor to get maximum demand, divide by power factor for kVA, add a growth margin, then choose the next standard rating.
  - q: What diversity factor should I use?
    a: It depends on how loads operate together. Continuous process plants may be 0.8–0.9; workshops and buildings 0.5–0.7.
  - q: Why not size exactly to the load?
    a: Transformers last longer and are most efficient at 50–80% load, and margins allow for growth and motor starting.
  - q: Should harmonics be considered?
    a: Yes. With many VFDs, UPSs or rectifiers, use a K-rated transformer or derate a standard one.
related: [electrical/transformer-current, electrical/transformer-efficiency, electrical/power-factor-correction, electrical/generator-size]
''', '''
## How to use the transformer size calculator

Enter the **total connected load** in kW, the **demand (diversity) factor**, the **power factor** you expect after correction and a **growth margin**. The calculator gives maximum demand and the required kVA. Choose the next standard rating above the result.

## Transformer sizing formula

<p class="formula">kVA = (connected kW × demand factor) ÷ PF × (1 + growth margin)</p>

## Example

500 kW connected, 0.7 demand factor, 0.9 PF, 25% growth:

- Maximum demand = 350 kW
- kVA = 350 ÷ 0.9 × 1.25 = **486 kVA** → choose **500 kVA**

## Standard distribution transformer ratings

16, 25, 63, 100, 160, 200, 250, 315, 400, 500, 630, 800, 1,000, 1,250, 1,600, 2,000 and 2,500 kVA (IS 1180 / IEC 60076).

## Typical demand factors

| Installation | Demand factor |
|---|---|
| Continuous process plant | 0.8–0.9 |
| General manufacturing | 0.6–0.8 |
| Commercial buildings | 0.5–0.7 |
| Residential complexes | 0.4–0.6 |

## After sizing

- Check full-load current and protection with the [transformer current calculator](/electrical/transformer-current/).
- Check fault level with the [transformer short-circuit calculator](/electrical/transformer-short-circuit/).
- Plan capacitor banks with the [power factor correction calculator](/electrical/power-factor-correction/) — a better PF reduces the kVA you need.
''')

# ======================= ENGINEERING =======================
def vt(D, h): return pi*D*D/4*h
page('engineering', 'vertical-tank-volume', f'''
title: Vertical Tank Volume Calculator (Level to Volume)
description: Calculate the volume of liquid in a vertical cylindrical tank from its diameter and level — with full capacity, percentage fill and litres per mm.
category: engineering
{intro("In a vertical cylindrical tank, volume rises in direct proportion to level, so one strapping factor converts a level reading into litres. This vertical tank volume calculator gives liquid volume, total capacity and percent full — see [tank volume from level measurement](ib:tank-volume-from-level-measurement) and how to [select the right level sensor](ib:how-to-select-the-right-level-sensor).")}
keywords: [vertical tank volume calculator, cylindrical tank volume, tank level to volume, liters in tank calculator, vertical cylinder tank capacity, tank strapping]
updated: {D}
variables:
  - {{ id: D, label: Tank inside diameter, family: length, unit: m, imperialUnit: ft, default: 3, min: 0 }}
  - {{ id: H, label: Tank height (straight side), family: length, unit: m, imperialUnit: ft, default: 5, min: 0 }}
  - {{ id: h, label: Liquid level, family: length, unit: m, imperialUnit: ft, default: 3.2, min: 0 }}
  - {{ id: V, label: Liquid volume, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: Vt, label: Total capacity, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: pc, label: Percent full, family: percent, unit: '%', min: 0 }}
  - {{ id: k, label: Volume per mm of level, suffix: L/mm, min: 0, decimals: 3 }}
equations:
  - V = pi * D^2 / 4 * h
  - Vt = pi * D^2 / 4 * H
  - pc = h / H
  - k = pi * D^2 / 4
faq:
  - q: How do I calculate the volume of a vertical tank?
    a: Volume = π × D² ÷ 4 × level. A 3 m diameter tank holds 7,069 litres per metre of level.
  - q: Does this include a cone or dished bottom?
    a: No — it covers the cylindrical part. Add the bottom volume separately, or use the cone calculator for conical bottoms.
  - q: How do I convert a level transmitter to volume?
    a: Because volume is linear with level in a vertical cylinder, you can scale the 4–20 mA signal directly to volume once the tank diameter is known.
  - q: Why use litres per mm?
    a: It is a quick strapping factor — multiply any level change in mm to get the volume added or removed.
related: [engineering/horizontal-tank-volume, engineering/hydrostatic-pressure, math/cylinder-volume, engineering/dp-level-range]
''', f'''
## How to use the vertical tank volume calculator

Enter the tank's **inside diameter**, its **straight-side height** and the **liquid level** measured from the bottom. The calculator gives the liquid volume, total capacity, percentage full and the volume per millimetre of level. To find the level for a given volume, enter the volume and press × on Liquid level.

## Vertical tank volume formula

<p class="formula">V = (π × D² ÷ 4) × h</p>

## Capacity per metre of level

| Diameter | Litres per metre | Litres per mm |
|---|---|---|
''' + ''.join(f"| {d} m | {vt(d,1)*1000:,.0f} L | {vt(d,1):.3f} L |\n" for d in [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]) + '''
## Level measurement for vertical tanks

| Technology | Notes |
|---|---|
| Hydrostatic / DP | Measures pressure; needs liquid density — see the [hydrostatic pressure calculator](/engineering/hydrostatic-pressure/) |
| Radar | Non-contact; unaffected by density and temperature |
| Ultrasonic | Non-contact; affected by vapour and foam — see the [ultrasonic level calculator](/engineering/ultrasonic-level/) |
| Float / magnetostrictive | High accuracy for inventory |

## Bottoms and tops

Cone and dished ends add volume below the straight side. Strapping tables for custody transfer also allow for wall thickness, deadwood (internals) and tank expansion with temperature.
''')

page('engineering', 'dp-level-range', f'''
title: DP Level Transmitter Range Calculator (Wet Leg and Dry Leg)
description: Calculate LRV and URV for a differential pressure level transmitter on open, dry-leg or wet-leg tanks — with zero elevation and suppression.
category: engineering
{intro("A DP transmitter measures level as the pressure of the liquid column, so its calibration range depends on liquid density, tap positions and any fill in the impulse lines. Getting LRV and URV right is the key step — see [wet leg and dry leg level measurement](ib:wet-leg-dry-leg-level-measurement) and [zero elevation and zero suppression](ib:zero-elevation-and-zero-suppression). This DP level range calculator works out both.")}
keywords: [dp level transmitter calculation, wet leg calculation, dry leg level measurement, lrv urv calculation, zero suppression elevation, differential pressure level range, dp transmitter calibration range]
updated: {D}
variables:
  - {{ id: sg, label: Process liquid specific gravity, default: 1.0, min: 0 }}
  - {{ id: H, label: Measuring span (min to max level), family: length, unit: mm, imperialUnit: in, default: 3000, min: 0 }}
  - {{ id: h0, label: Height of min level above HP tap, family: length, unit: mm, imperialUnit: in, default: 500, min: 0, help: 'Positive if the lowest level to measure is above the transmitter HP tap (zero suppression).' }}
  - id: w
    label: LP (reference) leg
    default: 0
    options:
      - {{ label: Open tank or dry leg, value: 0 }}
      - {{ label: Wet leg (filled), value: 1 }}
  - {{ id: sgs, label: Wet-leg fill specific gravity, default: 1.0, min: 0 }}
  - {{ id: Hs, label: Wet-leg height (LP tap to transmitter), family: length, unit: mm, imperialUnit: in, default: 4000, min: 0 }}
  - {{ id: LRV, label: LRV (at minimum level), suffix: mmH₂O, decimals: 1 }}
  - {{ id: URV, label: URV (at maximum level), suffix: mmH₂O, decimals: 1 }}
  - {{ id: span, label: Calibrated span, suffix: mmH₂O, min: 0, decimals: 1 }}
equations:
  - LRV = (sg * h0 - w * sgs * Hs) * 1000
  - URV = (sg * (h0 + H) - w * sgs * Hs) * 1000
  - span = sg * H * 1000
faq:
  - q: How do I calculate LRV and URV for a DP level transmitter?
    a: LRV = SG × (height from HP tap to min level) − (wet-leg SG × wet-leg height); URV = LRV + SG × span. Results are in mm (or inches) of water column.
  - q: What is zero suppression?
    a: When the minimum level is above the HP tap, the transmitter already sees pressure at 0% — the LRV is positive.
  - q: What is zero elevation?
    a: With a wet leg, the reference side has a constant head that makes the DP negative at low level — the LRV is negative and the range is "elevated".
  - q: Does the span depend on the wet leg?
    a: No. Span is always the process liquid SG × measuring height; the wet leg only shifts the range.
related: [engineering/hydrostatic-pressure, engineering/4-20ma-scaling, engineering/vertical-tank-volume, engineering/horizontal-tank-volume]
''', '''
## How to use the DP level range calculator

Enter the **specific gravity** of the process liquid, the **measuring span** (distance between minimum and maximum level), and the height of the **minimum level above the HP tap**. Choose **open/dry leg** or **wet leg**; for a wet leg, enter the fill fluid's SG and the leg height. The calculator gives LRV, URV and span in mm of water column (1 mmH₂O ≈ 0.0981 mbar).

## DP level range formulas

<p class="formula">LRV = SG<sub>p</sub> × h₀ − SG<sub>s</sub> × H<sub>s</sub></p>

<p class="formula">URV = SG<sub>p</sub> × (h₀ + H) − SG<sub>s</sub> × H<sub>s</sub></p>

The wet-leg term is zero for open tanks and dry legs.

## Example: wet-leg tank

Process SG 1.0, span 3,000 mm, minimum level 500 mm above the HP tap, wet leg filled with water (SG 1.0) 4,000 mm high:

- LRV = 500 − 4,000 = **−3,500 mmH₂O**
- URV = 3,500 − 4,000 = **−500 mmH₂O**
- Span = **3,000 mmH₂O**

## Choosing the reference leg

| Tank | LP side | Range type |
|---|---|---|
| Open to atmosphere | Vented | Suppressed or zero-based |
| Closed, non-condensing gas | Dry leg | Suppressed or zero-based |
| Closed, condensing vapour (steam drums) | Wet leg | Elevated (negative LRV) |
| Closed, either | Remote diaphragm seals (capillary) | Elevated, fill fluid SG |

## Tips

- Wet legs must stay full — a partly drained leg causes large level errors.
- With diaphragm seals, use the capillary fill fluid SG and the vertical distance between seals.
- Density changes shift the reading; for varying density see [DP level measurement with varying density](https://www.instrumentationblog.in/dp-level-measurement-varying-density/).
''')

def api(sg): return 141.5/sg-131.5
page('engineering', 'api-gravity', f'''
title: API Gravity Calculator (API to Specific Gravity)
description: Convert API gravity to specific gravity and density and back — for crude oil, fuels and petroleum products at 60 °F.
category: engineering
{intro("API gravity is the petroleum industry's scale for how heavy or light an oil is compared with water: higher API means lighter oil. It converts directly to specific gravity and density at 60 °F. This API gravity calculator works both ways — see [what specific gravity is](ib:what-is-specific-gravity).")}
keywords: [api gravity calculator, api to specific gravity, specific gravity to api, api gravity formula, crude oil density, oil api degree, api to density]
updated: {D}
variables:
  - {{ id: API, label: API gravity, suffix: °API, default: 35, decimals: 2 }}
  - {{ id: SG, label: Specific gravity (60/60 °F), min: 0.0001, decimals: 4 }}
  - {{ id: rho, label: Density at 60 °F, family: density, unit: kgm3, imperialUnit: lbft3, min: 0 }}
equations:
  - SG = 141.5 / (API + 131.5)
  - rho = SG * 999.016
faq:
  - q: What is the API gravity formula?
    a: API = 141.5 ÷ SG − 131.5, where SG is the specific gravity at 60 °F relative to water at 60 °F.
  - q: What API gravity is water?
    a: Exactly 10 °API. Oils lighter than water have API above 10; heavier oils below 10.
  - q: What is light and heavy crude?
    a: Light crude is above about 31.1 °API, medium 22.3–31.1 °API, heavy 10–22.3 °API and extra-heavy below 10 °API.
  - q: Why does API gravity matter?
    a: Lighter crudes yield more petrol and diesel and sell at a higher price; API also feeds volume correction and flow measurement calculations.
related: [physics/density, engineering/mass-flow-rate, engineering/hydrostatic-pressure, engineering/dp-level-range]
''', '''
## How to use the API gravity calculator

Enter the **API gravity** to get specific gravity and density at 60 °F, or enter **specific gravity** or **density** and press × on API gravity to convert the other way.

## API gravity formula

<p class="formula">°API = 141.5 ÷ SG − 131.5 &nbsp;·&nbsp; SG = 141.5 ÷ (°API + 131.5)</p>

Density uses water at 60 °F (999.016 kg/m³).

## API gravity of common products

| Product | Typical °API | SG |
|---|---|---|
''' + ''.join(f"| {n} | {a} | {141.5/(a+131.5):.3f} |\n" for n, a in [('Heavy fuel oil', 12), ('Heavy crude (e.g. Maya)', 21), ('Arab Medium', 30), ('Brent', 38), ('WTI', 40), ('Diesel', 35), ('Kerosene / jet fuel', 45), ('Petrol (gasoline)', 60)]) + '''
## Crude classification

| Class | °API |
|---|---|
| Light | > 31.1 |
| Medium | 22.3 – 31.1 |
| Heavy | 10 – 22.3 |
| Extra heavy | < 10 |

## Temperature correction

API gravity is defined at 60 °F (15.6 °C). Hydrometer readings at other temperatures are corrected to 60 °F with the API MPMS Chapter 11.1 tables before use.
''')

page('engineering', 'turndown-ratio', f'''
title: Turndown Ratio Calculator (Flow Meter Rangeability)
description: Calculate the turndown ratio of a flow meter or control valve from maximum and minimum flow — and the minimum flow for a given turndown.
category: engineering
{intro("Turndown (rangeability) is the ratio of the maximum to the minimum flow an instrument can measure or control accurately. It decides whether one meter or valve can cover the whole operating range — see [turndown ratio in flow meters](ib:turndown-ratio-in-flow-meters) and [control valve rangeability](ib:control-valve-rangeability-turndown). This turndown ratio calculator works it out in either direction.")}
keywords: [turndown ratio calculator, flow meter turndown, rangeability calculator, minimum flow calculation, turndown ratio formula, flow meter range]
updated: {D}
variables:
  - {{ id: Qmax, label: Maximum flow, family: flow, unit: m3h, imperialUnit: gpm, default: 100, min: 0 }}
  - {{ id: Qmin, label: Minimum flow, family: flow, unit: m3h, imperialUnit: gpm, default: 10, min: 0 }}
  - {{ id: TD, label: Turndown ratio (x : 1), min: 0, decimals: 1 }}
  - {{ id: dpr, label: DP ratio at min flow (DP meters), family: percent, unit: '%', min: 0 }}
equations:
  - TD = Qmax / Qmin
  - dpr = (Qmin / Qmax)^2
faq:
  - q: What is turndown ratio?
    a: The maximum flow divided by the minimum flow that can be measured within the stated accuracy. A meter covering 10 to 100 m³/h has a 10:1 turndown.
  - q: Why do orifice plates have low turndown?
    a: DP is proportional to flow squared, so at 10% flow the DP is only 1% of maximum — too small to measure accurately. Practical turndown is about 3:1 to 5:1 with one transmitter.
  - q: Which flow meters have high turndown?
    a: Coriolis (often 100:1), electromagnetic and ultrasonic meters (30–100:1). Vortex meters are around 10–20:1.
  - q: Is turndown the same as rangeability?
    a: They are often used interchangeably. For control valves, rangeability is the ratio of maximum to minimum controllable Cv.
related: [engineering/dp-flow-square-root, engineering/orifice-flow, engineering/flow-meter-k-factor, engineering/instrument-accuracy]
''', '''
## How to use the turndown ratio calculator

Enter the **maximum** and **minimum flow**. You get the turndown ratio and, for differential pressure meters, the DP at minimum flow as a percentage of the DP at maximum flow. Enter a turndown and press × on Minimum flow to find the lowest flow a meter can handle.

## Turndown ratio formula

<p class="formula">Turndown = Q<sub>max</sub> ÷ Q<sub>min</sub></p>

<p class="formula">DP meters: ΔP<sub>min</sub> ÷ ΔP<sub>max</sub> = (Q<sub>min</sub> ÷ Q<sub>max</sub>)²</p>

## Typical turndown by meter type

| Flow meter | Typical turndown |
|---|---|
| Orifice / Venturi (one DP transmitter) | 3:1 – 5:1 |
| Variable area (rotameter) | 10:1 |
| Vortex | 10:1 – 20:1 |
| Turbine | 10:1 – 50:1 |
| Electromagnetic | 30:1 – 100:1+ |
| Ultrasonic (transit time) | 30:1 – 100:1 |
| Coriolis | 50:1 – 100:1+ |
| Thermal mass | 50:1 – 100:1 |

## DP at reduced flow

| Flow | DP (% of max) |
|---|---|
| 100% | 100% |
| 50% | 25% |
| 30% | 9% |
| 20% | 4% |
| 10% | 1% |

## Accuracy across the range

Meters specified in **% of reading** keep the same relative accuracy across their turndown; meters specified in **% of full scale** become much less accurate at low flow. See the [instrument accuracy calculator](/engineering/instrument-accuracy/).
''')

def c_air(T): return 331.3*math.sqrt(1+T/273.15)
page('engineering', 'ultrasonic-level', f'''
title: Ultrasonic Level Calculator (Time of Flight and Temperature)
description: Calculate the distance and liquid level measured by an ultrasonic level transmitter from echo time and air temperature — with the speed-of-sound correction.
category: engineering
{intro("An ultrasonic level transmitter sends a sound pulse down to the liquid surface and times the echo. Because the speed of sound in air changes about 0.6 m/s per °C, temperature compensation is essential. This ultrasonic level calculator converts echo time into distance and level — see [ultrasonic level transmitter working](ib:ultrasonic-level-transmitter-working) and [how an ultrasonic level transmitter works](ib:how-does-an-ultrasonic-level-transmitter-work).")}
keywords: [ultrasonic level calculator, time of flight level calculation, ultrasonic level transmitter, speed of sound temperature, echo time to distance, ultrasonic distance calculator]
updated: {D}
variables:
  - {{ id: t, label: Echo time (round trip), family: seconds, unit: ms, default: 20, min: 0 }}
  - {{ id: T, label: Air temperature, suffix: °C, default: 30 }}
  - {{ id: E, label: Empty distance (sensor face to tank bottom), family: length, unit: m, imperialUnit: ft, default: 6, min: 0 }}
  - {{ id: c, label: Speed of sound in air, family: velocity, unit: ms, min: 0 }}
  - {{ id: d, label: Distance to surface, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: L, label: Liquid level, family: length, unit: m, imperialUnit: ft }}
equations:
  - c = 331.3 * sqrt(1 + T / 273.15)
  - d = c * t / 2
  - L = E - d
faq:
  - q: How does an ultrasonic level sensor calculate distance?
    a: Distance = speed of sound × echo time ÷ 2, because the pulse travels down and back. Level = empty distance − measured distance.
  - q: How much does temperature affect the reading?
    a: The speed of sound changes by about 0.17% per °C. Without compensation, a 20 °C error causes about 3.5% distance error.
  - q: What is the blanking distance?
    a: A zone just below the sensor where echoes cannot be measured while the transducer is still ringing — typically 0.25–0.5 m.
  - q: When is ultrasonic a poor choice?
    a: With heavy vapour, foam, dust, high pressure or vacuum, or strong turbulence. Radar is usually better in those cases.
related: [engineering/vertical-tank-volume, engineering/hydrostatic-pressure, physics/speed-distance-time, physics/doppler-effect]
''', '''
## How to use the ultrasonic level calculator

Enter the **round-trip echo time**, the **air temperature** in the tank and the **empty distance** from the sensor face to the bottom (0% level). You get the speed of sound, the distance to the surface and the liquid level.

## Ultrasonic level formula

<p class="formula">c = 331.3 × √(1 + T/273.15) m/s &nbsp;·&nbsp; d = c × t ÷ 2 &nbsp;·&nbsp; Level = E − d</p>

## Speed of sound in air

| Temperature | Speed of sound | Distance error if 20 °C assumed |
|---|---|---|
''' + ''.join(f"| {T} °C | {c_air(T):.1f} m/s | {(c_air(T)/c_air(20)-1)*100:+.1f}% |\n" for T in [-20, 0, 10, 20, 30, 40, 60, 80]) + '''
## Example

Echo time 20 ms at 30 °C, empty distance 6 m:

- c = 349.0 m/s, distance = 349.0 × 0.020 ÷ 2 = **3.49 m**
- Level = 6 − 3.49 = **2.51 m**

## Installation tips

- Keep the liquid surface out of the blanking distance at maximum level.
- Mount away from the tank wall, inlet stream and internal ladders to avoid false echoes.
- Use the sensor's built-in temperature probe; vapour layers with a different gas composition still cause errors.
- For foam, vapour or pressure, consider [radar level measurement](https://www.instrumentationblog.in/radar-level-selection-non-contact-vs-guided-wave/).
''')

page('engineering', 'instrument-accuracy', f'''
title: Instrument Accuracy Calculator (% of Span vs % of Reading)
description: Convert instrument accuracy between % of span, % of full scale and % of reading — and find the measurement error at any point in the range.
category: engineering
{intro("Instrument accuracy can be stated as a percentage of span, of full scale or of reading — and the difference matters most at low readings. A meter that is ±1% of full scale can be ±10% of reading at 10% of range. This instrument accuracy calculator shows the real error — see [accuracy reading vs full scale](ib:flow-meter-accuracy-reading-vs-full-scale) and [pressure transmitter accuracy specifications](ib:pressure-transmitter-accuracy-specifications).")}
keywords: [instrument accuracy calculator, percent of span accuracy, percent of reading vs full scale, measurement error calculation, transmitter accuracy, accuracy specification]
updated: {D}
variables:
  - {{ id: lo, label: Range low (LRV), default: 0 }}
  - {{ id: hi, label: Range high (URV), default: 100 }}
  - {{ id: rd, label: Reading, default: 25 }}
  - {{ id: acc, label: Accuracy (% of span), family: percent, unit: '%', default: 0.5, min: 0 }}
  - {{ id: err, label: Error band (±, engineering units), min: 0, decimals: 4 }}
  - {{ id: ar, label: Same accuracy as % of reading, family: percent, unit: '%', min: 0 }}
  - {{ id: lo2, label: Reading could be as low as, decimals: 4 }}
  - {{ id: hi2, label: Reading could be as high as, decimals: 4 }}
equations:
  - err = acc * (hi - lo)
  - ar = err / abs(rd)
  - lo2 = rd - err
  - hi2 = rd + err
faq:
  - q: What is the difference between % of span and % of reading?
    a: Accuracy in % of span (or full scale) gives a fixed error in engineering units across the whole range. % of reading scales with the measured value, so it stays tight at low readings.
  - q: How do I convert % of span to % of reading?
    a: Error (units) = % of span × span; then % of reading = error ÷ reading. ±0.5% of a 0–100 span at a reading of 25 is ±0.5 units, or ±2% of reading.
  - q: Is accuracy the same as precision?
    a: No. Accuracy is closeness to the true value; precision is repeatability. See accuracy vs precision.
  - q: Does rangeability change accuracy?
    a: Yes. Re-ranging a transmitter to a smaller span usually increases the error as a % of the new span — check the turndown effect in the datasheet.
related: [math/percent-error, engineering/turndown-ratio, engineering/4-20ma-scaling, statistics/standard-deviation]
''', '''
## How to use the instrument accuracy calculator

Enter the instrument's **range** (LRV and URV), the current **reading** and the **accuracy as a percentage of span**. You get the error band in engineering units, the same error expressed as a percentage of reading, and the range in which the true value could lie.

## Accuracy formulas

<p class="formula">Error = ±(% of span) × (URV − LRV) &nbsp;·&nbsp; % of reading = Error ÷ Reading</p>

## ±1% of full scale vs ±1% of reading (0–100 range)

| Reading | Error at ±1% FS | as % of reading | Error at ±1% of reading |
|---|---|---|---|
''' + ''.join(f"| {r} | ±1.0 | ±{100/r:.1f}% | ±{r/100:.2f} |\n" for r in [100, 75, 50, 25, 10, 5]) + '''
## Typical accuracy specifications

| Instrument | Typical accuracy |
|---|---|
| Smart pressure / DP transmitter | ±0.04–0.1% of span |
| Industrial pressure gauge (class 1.0) | ±1% of full scale |
| Electromagnetic flow meter | ±0.2–0.5% of reading |
| Coriolis flow meter | ±0.1% of reading |
| Vortex flow meter | ±0.75–1% of reading |
| Variable area meter | ±1–2% of full scale |
| Pt100 Class A | ±(0.15 + 0.002 × t) °C |

## Total probable error

Several independent errors (transmitter, ambient temperature effect, static pressure effect, card) combine as the square root of the sum of squares — not a simple sum. For calibration checks see [calibration error calculation](https://www.instrumentationblog.in/calibration-error-calculation/) and [accuracy vs precision](https://www.instrumentationblog.in/difference-between-accuracy-and-precision/).
''')

def jk(rho, a, dv): return rho*a*dv
page('engineering', 'water-hammer', f'''
title: Water Hammer Calculator (Joukowsky Equation)
description: Calculate the surge pressure from sudden valve closure or pump trip with the Joukowsky equation — with wave speed and critical closure time.
category: engineering
{intro("When a valve closes quickly or a pump trips, the moving liquid stops suddenly and its momentum turns into a pressure spike that can burst pipes and damage instruments. This water hammer calculator uses the Joukowsky equation to estimate the surge — see the [Joukowsky equation for water hammer](ib:joukowsky-equation-water-hammer) and the [hammer effect in pressure gauges](ib:hammer-effect-in-pressure-gauges).")}
keywords: [water hammer calculator, joukowsky equation, surge pressure calculation, pressure surge valve closure, water hammer formula, pipeline surge, critical closure time]
updated: {D}
variables:
  - {{ id: rho, label: Liquid density, family: density, unit: kgm3, imperialUnit: lbft3, default: 1000, min: 0 }}
  - {{ id: a, label: Pressure wave speed, family: velocity, unit: ms, imperialUnit: fts, default: 1200, min: 0, help: 'About 1,000–1,400 m/s in steel pipe full of water, 300–500 m/s in PVC/HDPE.' }}
  - {{ id: dv, label: Velocity change, family: velocity, unit: ms, imperialUnit: fts, default: 2, min: 0 }}
  - {{ id: L, label: Pipe length (valve to reservoir), family: length, unit: m, imperialUnit: ft, default: 500, min: 0 }}
  - {{ id: dP, label: Surge pressure rise, family: pressure, unit: bar, imperialUnit: psi, min: 0 }}
  - {{ id: dH, label: Surge head, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: tc, label: Critical closure time (2L/a), family: seconds, unit: s, min: 0 }}
equations:
  - dP = rho * a * dv
  - dH = a * dv / g0
  - tc = 2 * L / a
faq:
  - q: What is the Joukowsky equation?
    a: ΔP = ρ × a × Δv — the pressure rise when flow velocity changes suddenly, where ρ is density, a the pressure wave speed and Δv the velocity change.
  - q: How big can water hammer be?
    a: Stopping water flowing at 2 m/s in steel pipe causes a surge of about 24 bar — often more than the operating pressure.
  - q: What is the critical closure time?
    a: 2L ÷ a, the time for a pressure wave to travel to the reservoir and back. Closing faster than this gives the full Joukowsky surge; closing slower reduces it.
  - q: How is water hammer prevented?
    a: Slow-closing valves, surge tanks, air vessels, surge relief valves, VFD ramp-down of pumps and lower design velocities.
related: [engineering/pipe-flow-velocity, engineering/darcy-weisbach-head-loss, engineering/pump-power, engineering/hydrostatic-pressure]
''', f'''
## How to use the water hammer calculator

Enter the liquid **density**, the **pressure wave speed** for your pipe material, the **velocity change** (usually the full flow velocity for a sudden stop) and the **pipe length** to the nearest reservoir or open end. You get the surge pressure, the surge head and the critical closure time.

## Joukowsky equation

<p class="formula">ΔP = ρ × a × Δv &nbsp;·&nbsp; ΔH = a × Δv ÷ g &nbsp;·&nbsp; t<sub>c</sub> = 2L ÷ a</p>

## Surge for water in steel pipe (a = 1,200 m/s)

| Velocity stopped | Surge pressure | Surge head |
|---|---|---|
''' + ''.join(f"| {v} m/s | {jk(1000,1200,v)/1e5:.1f} bar | {1200*v/9.80665:.0f} m |\n" for v in [0.5, 1, 1.5, 2, 3]) + '''
## Typical wave speeds (water)

| Pipe | Wave speed |
|---|---|
| Steel | 1,000–1,400 m/s |
| Ductile iron | 1,000–1,300 m/s |
| Concrete | 900–1,200 m/s |
| PVC | 300–500 m/s |
| HDPE | 200–400 m/s |

Flexible plastic pipes have lower wave speeds, so surges are smaller.

## Protecting instruments

Pressure gauges and transmitters on lines prone to surges need snubbers, liquid-filled gauges or pulsation dampers, and a pressure rating above the surge pressure.
''')

def pfd(l, ti): return l*ti/2
page('engineering', 'pfd-avg', f'''
title: PFDavg Calculator (SIL Verification, 1oo1)
description: Calculate the average probability of failure on demand (PFDavg) for a 1oo1 safety function from dangerous undetected failure rate and proof test interval — with SIL band.
category: engineering
{intro("In a safety instrumented system, each safety function must reach a target probability of failure on demand (PFDavg) that sets its SIL. For a single channel, PFDavg depends on the dangerous undetected failure rate and how often it is proof tested. This PFDavg calculator does the 1oo1 calculation — see the [PFDavg calculation formula](ib:pfdavg-calculation-formula), [what SIL is](ib:what-is-sil-safety-integrity-level) and [SIL verification](ib:sil-verification).")}
keywords: [pfdavg calculator, pfd avg calculation, sil calculation, probability of failure on demand, sil verification calculator, proof test interval, lambda du, iec 61511]
updated: {D}
variables:
  - {{ id: lam, label: Dangerous undetected failure rate (λDU), suffix: FIT, default: 500, min: 0, help: '1 FIT = 1 failure per 10⁹ hours.' }}
  - {{ id: TI, label: Proof test interval, suffix: years, default: 1, min: 0 }}
  - {{ id: PFD, label: PFDavg (1oo1), min: 0, decimals: 6 }}
  - {{ id: RRF, label: Risk reduction factor (1/PFDavg), min: 0, decimals: 0 }}
  - {{ id: SIL, label: SIL achieved (by PFDavg only), min: 0, decimals: 0 }}
equations:
  - PFD = lam * 1e-9 * TI * 8760 / 2
  - RRF = 1 / PFD
  - SIL = max(0, min(4, floor(log10(RRF))))
faq:
  - q: What is the PFDavg formula for 1oo1?
    a: PFDavg ≈ λDU × TI ÷ 2, where λDU is the dangerous undetected failure rate per hour and TI the proof test interval in hours.
  - q: What PFDavg does each SIL need?
    a: SIL 1 — 10⁻² to 10⁻¹; SIL 2 — 10⁻³ to 10⁻²; SIL 3 — 10⁻⁴ to 10⁻³; SIL 4 — 10⁻⁵ to 10⁻⁴ (low-demand mode, IEC 61511).
  - q: Is PFDavg enough to claim a SIL?
    a: No. You must also meet architectural constraints (hardware fault tolerance), systematic capability and proof-test coverage requirements.
  - q: How do I lower PFDavg?
    a: Test more often, choose devices with lower λDU, add redundancy (1oo2, 2oo3) or improve diagnostic coverage.
related: [engineering/availability-mtbf, statistics/probability, statistics/poisson-probability, engineering/instrument-accuracy]
''', f'''
## How to use the PFDavg calculator

Enter the **dangerous undetected failure rate** λDU for the whole safety function (sensor + logic solver + final element) in FIT, and the **proof test interval** in years. You get PFDavg, the risk reduction factor and the SIL band that PFDavg alone supports.

## PFDavg formula (1oo1, low demand)

<p class="formula">PFD<sub>avg</sub> ≈ λ<sub>DU</sub> × TI ÷ 2 &nbsp;·&nbsp; RRF = 1 ÷ PFD<sub>avg</sub></p>

This simplified formula assumes perfect proof testing and ignores repair time and common-cause failures.

## SIL bands (low-demand mode)

| SIL | PFDavg | Risk reduction factor |
|---|---|---|
| SIL 1 | ≥ 10⁻² to < 10⁻¹ | 10 – 100 |
| SIL 2 | ≥ 10⁻³ to < 10⁻² | 100 – 1,000 |
| SIL 3 | ≥ 10⁻⁴ to < 10⁻³ | 1,000 – 10,000 |
| SIL 4 | ≥ 10⁻⁵ to < 10⁻⁴ | 10,000 – 100,000 |

## PFDavg vs proof test interval (λDU = 500 FIT)

| Test interval | PFDavg | RRF |
|---|---|---|
''' + ''.join(f"| {ti} | {pfd(500e-9,h):.2e} | {1/pfd(500e-9,h):,.0f} |\n" for ti, h in [('3 months', 2190), ('6 months', 4380), ('1 year', 8760), ('2 years', 17520), ('5 years', 43800)]) + '''
## Redundant architectures

| Architecture | Simplified PFDavg |
|---|---|
| 1oo1 | λ<sub>DU</sub> TI / 2 |
| 1oo2 | (λ<sub>DU</sub> TI)² / 3 + β λ<sub>DU</sub> TI / 2 |
| 2oo3 | (λ<sub>DU</sub> TI)² + β λ<sub>DU</sub> TI / 2 |

β is the common-cause factor (typically 2–10%). For a full assessment, follow IEC 61508/61511 — see [SIL determination methods](https://www.instrumentationblog.in/sil-determination-risk-graph-lopa-consequence-severity-matrix/).
''')

page('engineering', 'availability-mtbf', f'''
title: Availability Calculator (MTBF and MTTR)
description: Calculate equipment availability from MTBF and MTTR, plus failure rate, expected downtime per year and the probability of running without failure.
category: engineering
{intro("Availability is the fraction of time equipment is ready to work. It depends on how often it fails (MTBF) and how quickly it is repaired (MTTR). This availability calculator also gives the failure rate, downtime per year and reliability over a mission time — useful for comparing instruments, pumps and control systems, and for [SIS final element reliability](ib:sis-final-element-reliability).")}
keywords: [availability calculator, mtbf mttr calculator, availability formula, mtbf calculation, downtime per year, reliability calculator, failure rate calculator]
updated: {D}
variables:
  - {{ id: mtbf, label: MTBF (mean time between failures), family: seconds, unit: h, default: 87600, min: 0 }}
  - {{ id: mttr, label: MTTR (mean time to repair), family: seconds, unit: h, default: 8, min: 0 }}
  - {{ id: tm, label: Mission time, family: seconds, unit: h, default: 8760, min: 0 }}
  - {{ id: A, label: Availability, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: dt, label: Expected downtime per year, family: seconds, unit: h, min: 0 }}
  - {{ id: lam, label: Failure rate, suffix: failures/year, min: 0, decimals: 4 }}
  - {{ id: R, label: Probability of no failure during mission, family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - A = mtbf / (mtbf + mttr)
  - dt = (1 - A) * 8760 * 3600
  - lam = 8760 * 3600 / mtbf
  - R = exp(-tm / mtbf)
faq:
  - q: How do I calculate availability?
    a: Availability = MTBF ÷ (MTBF + MTTR). An MTBF of 10 years and MTTR of 8 hours gives 99.991%.
  - q: What does MTBF really mean?
    a: The average operating time between failures across a population. An MTBF of 10 years does not mean each unit lasts 10 years — with a constant failure rate, only about 37% survive that long.
  - q: What is "five nines"?
    a: 99.999% availability — about 5.3 minutes of downtime per year.
  - q: How do I improve availability?
    a: Reduce failures (better equipment, condition monitoring) or shorten repairs (spares on site, diagnostics, redundancy with online repair).
related: [engineering/pfd-avg, statistics/poisson-probability, statistics/probability, finance/payback-period]
''', '''
## How to use the availability calculator

Enter the **MTBF**, the **MTTR** and a **mission time**. You get availability, expected downtime per year, failure rate, and the probability of running through the mission time without a failure (assuming a constant failure rate).

## Availability formulas

<p class="formula">A = MTBF ÷ (MTBF + MTTR) &nbsp;·&nbsp; λ = 1 ÷ MTBF &nbsp;·&nbsp; R(t) = e<sup>−t/MTBF</sup></p>

## Availability and downtime

| Availability | Downtime per year |
|---|---|
| 99% | 87.6 hours |
| 99.9% | 8.76 hours |
| 99.99% | 52.6 minutes |
| 99.999% | 5.26 minutes |

## Redundancy

Two identical units in parallel, where either can do the job, have unavailability of roughly (1 − A)². Two 99% units give about 99.99% — the reason redundant PLCs, transmitters and pumps are used on critical duties.

## MTBF, failure rate and FIT

| MTBF | Failure rate | FIT (failures per 10⁹ h) |
|---|---|---|
| 1 year (8,760 h) | 1 per year | 114,155 |
| 10 years | 0.1 per year | 11,416 |
| 100 years | 0.01 per year | 1,142 |
| 1,000 years | 0.001 per year | 114 |

For safety instrumented functions, the dangerous undetected portion of the failure rate drives the [PFDavg](/engineering/pfd-avg/).
''')
print('E1 done')
