import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
D = '2026-10-27'
s3 = math.sqrt(3)

# ---------------------------------------------------------------- kVA to kW
page('engineering', 'kva-to-kw', f'''
title: kVA to kW Converter (and kW to kVA)
description: Convert kVA to kW and kW to kVA using power factor — for generators, UPS, transformers and DG set sizing.
category: engineering
keywords: [kva to kw, kw to kva, kva to kw conversion, power factor, generator kva, ups kva, apparent power, real power, kvar]
updated: {D}
featured: true
variables:
  - {{ id: S, label: Apparent power (kVA), suffix: kVA, default: 100, min: 0 }}
  - {{ id: pf, label: Power factor (cos φ), default: 0.8, min: 0.01, max: 1 }}
  - {{ id: P, label: Real power (kW), suffix: kW, min: 0 }}
  - {{ id: Q, label: Reactive power (kVAr), suffix: kVAr, min: 0 }}
equations:
  - P = S * pf
  - Q = sqrt(S^2 - P^2)
faq:
  - q: How do I convert kVA to kW?
    a: Multiply kVA by the power factor. 100 kVA at 0.8 power factor is 80 kW.
  - q: How do I convert kW to kVA?
    a: Divide kW by the power factor. 80 kW at 0.8 power factor is 100 kVA.
  - q: Why are generators rated in kVA?
    a: Because their limit is set by current (heating of windings), which depends on kVA, not just kW. Most diesel generator sets are rated at 0.8 power factor.
  - q: What is a good power factor?
    a: 0.95 or higher is considered good for industrial loads. Many utilities charge penalties below about 0.9.
related: [engineering/kw-to-amps, engineering/three-phase-motor-power, engineering/amps-to-watts, conversion/kw-to-hp]
''', f'''
## How to use this calculator

Enter the **apparent power in kVA** and the **power factor**. The calculator gives real power (kW) and reactive power (kVAr). To go from kW to kVA, press × on kVA and type the kW.

## The formulas

<p class="formula">kW = kVA × PF &nbsp;·&nbsp; kVA = kW ÷ PF &nbsp;·&nbsp; kVAr = √(kVA² − kW²)</p>

These come from the **power triangle**: real power (kW) and reactive power (kVAr) are at right angles, and apparent power (kVA) is the hypotenuse.

## kVA to kW chart

| kVA | PF 0.8 | PF 0.85 | PF 0.9 | PF 0.95 |
|---|---|---|---|---|
''' + ''.join(f"| {s} | {s*.8:g} kW | {s*.85:g} kW | {s*.9:g} kW | {s*.95:g} kW |\n" for s in [1, 5, 10, 15, 25, 62.5, 100, 125, 250, 500, 1000]) + f'''
## Generator (DG set) sizing

1. Add up the kW of all loads that may run together.
2. Divide by the generator's rated power factor (usually 0.8) to get kVA.
3. Allow for motor starting currents — direct-on-line motors draw 6–8 times their running current briefly.
4. Add a margin of 20–25% so the generator does not run continuously near full load.

**Example**: 60 kW of loads ÷ 0.8 = 75 kVA; with a 25% margin, choose about **100 kVA**.

## UPS sizing

UPS units list both VA and W. A 1,000 VA UPS rated at 0.6 PF supports only 600 W; modern units often have 0.9–1.0 PF. Size by **watts** for the connected load.

## Power factor of common loads

| Load | Typical PF |
|---|---|
| Resistive heaters, incandescent lamps | 1.0 |
| Induction motor, full load | 0.80–0.90 |
| Induction motor, light load | 0.3–0.6 |
| LED drivers and SMPS (with PFC) | 0.9–0.99 |
| Older fluorescent lighting | 0.5–0.9 |

## Improving power factor

Capacitor banks supply reactive power locally so less has to come from the grid. Raising PF from 0.75 to 0.95 on a 100 kW load cuts apparent power from 133 kVA to 105 kVA, reducing current, cable losses and transformer loading. The capacitor bank needed is the difference in kVAr: {100*math.tan(math.acos(.75))-100*math.tan(math.acos(.95)):.0f} kVAr.
''')

# ---------------------------------------------------------------- kW to amps
page('engineering', 'kw-to-amps', f'''
title: kW to Amps Calculator (Single-Phase, Three-Phase and DC)
description: Convert kilowatts to amps for single-phase, three-phase and DC circuits using voltage and power factor — with charts for 230 V and 415 V.
category: engineering
keywords: [kw to amps, kilowatts to amps, kw to amps three phase, kw to amps single phase, power to current, amps calculator, current calculation]
updated: {D}
featured: true
variables:
  - {{ id: P, label: Power, family: power, unit: kW, imperialUnit: hp, default: 10, min: 0 }}
  - id: ph
    label: System
    default: 1.7320508
    options:
      - {{ label: Three-phase (line-to-line voltage), value: 1.7320508 }}
      - {{ label: Single-phase AC, value: 1 }}
      - {{ label: DC (use power factor 1), value: 1.000001 }}
  - {{ id: V, label: Voltage, family: voltage, unit: V, default: 415, min: 0 }}
  - {{ id: pf, label: Power factor, default: 0.85, min: 0.01, max: 1, help: Use 1 for DC and resistive loads. }}
  - {{ id: I, label: Current, family: current, unit: A, min: 0 }}
equations:
  - P = ph * V * I * pf
faq:
  - q: How many amps is 1 kW?
    a: At 230 V single-phase and unity power factor, about 4.35 A. At 415 V three-phase with 0.85 PF, about 1.64 A.
  - q: What is the formula for kW to amps in three-phase?
    a: I = P ÷ (√3 × V × PF), with P in watts and V the line-to-line voltage.
  - q: How many amps does a 10 kW three-phase load draw at 415 V?
    a: About 16.4 A at 0.85 power factor.
  - q: Do I use phase or line voltage for three-phase?
    a: Use the line-to-line voltage (for example 400 V or 415 V) with the √3 formula.
related: [engineering/amps-to-watts, engineering/kva-to-kw, engineering/three-phase-motor-power, engineering/cable-voltage-drop]
''', f'''
## How to use this calculator

1. Enter the **power** in kW (or switch to W or hp).
2. Choose **three-phase**, **single-phase** or **DC**.
3. Enter the **voltage** and **power factor** (use 1 for DC or purely resistive loads).

The calculator gives the current. It works in reverse too — enter amps and press × on Power to find kW.

## The formulas

| System | Current |
|---|---|
| DC | I = P ÷ V |
| Single-phase AC | I = P ÷ (V × PF) |
| Three-phase AC | I = P ÷ (√3 × V<sub>L</sub> × PF) |

P is in watts. For a motor, use the **electrical input** power (rated output ÷ efficiency).

## kW to amps chart

| kW | 230 V 1-ph (PF 1) | 230 V 1-ph (PF 0.85) | 415 V 3-ph (PF 0.85) | 400 V 3-ph (PF 0.85) |
|---|---|---|---|---|
''' + ''.join(f"| {p} | {p*1000/230:.1f} A | {p*1000/230/.85:.1f} A | {p*1000/(s3*415*.85):.1f} A | {p*1000/(s3*400*.85):.1f} A |\n" for p in [0.5, 1, 1.5, 2, 3, 5, 7.5, 10, 15, 22, 37, 55, 75, 100]) + '''
## Choosing a breaker and cable

The calculated current is the **running** current. When selecting protection and cable:

- Choose a breaker rated above the running current (often the next standard size, such as 16 A, 20 A, 25 A, 32 A).
- Check the cable's current-carrying capacity for its installation method.
- Allow for motor starting current and check the [voltage drop](/engineering/cable-voltage-drop/).
- Follow local wiring regulations.

## Single-phase vs three-phase

For the same power, a three-phase circuit carries much less current per conductor than a single-phase one, which is why large motors and buildings use three-phase supplies. 10 kW is 43.5 A at 230 V single-phase but only 16.4 A per line at 415 V three-phase (PF 0.85).

## Common voltages

| Region | Single-phase | Three-phase |
|---|---|---|
| India, UK, Europe, Australia | 230–240 V | 400–415 V |
| USA, Canada (residential) | 120 / 240 V | 208 V or 480 V |
| Japan | 100 V | 200 V |
''')

# ---------------------------------------------------------------- amps to watts
page('engineering', 'amps-to-watts', f'''
title: Amps to Watts Calculator (and Watts to Amps)
description: Convert amps to watts for DC, single-phase and three-phase circuits — with charts for 12 V, 120 V and 230 V.
category: engineering
keywords: [amps to watts, watts to amps, amps to kw, how many watts is an amp, 12v amps to watts, 230v amps to watts, ampere to watt]
updated: {D}
variables:
  - {{ id: I, label: Current, family: current, unit: A, default: 10, min: 0 }}
  - {{ id: V, label: Voltage, family: voltage, unit: V, default: 230, min: 0 }}
  - id: ph
    label: System
    default: 1
    options:
      - {{ label: DC or single-phase AC, value: 1 }}
      - {{ label: Three-phase AC (line voltage), value: 1.7320508 }}
  - {{ id: pf, label: Power factor, default: 1, min: 0.01, max: 1 }}
  - {{ id: P, label: Power, family: power, unit: W, imperialUnit: W, min: 0 }}
equations:
  - P = ph * V * I * pf
faq:
  - q: How many watts is 1 amp?
    a: It depends on voltage. At 230 V it is 230 W; at 120 V it is 120 W; at 12 V it is 12 W (for DC or unity power factor).
  - q: How many watts can a 16 A socket supply?
    a: About 3,680 W at 230 V. Many appliances are limited to a little less for continuous use.
  - q: How many amps is 2,000 watts?
    a: About 8.7 A at 230 V or 16.7 A at 120 V.
related: [engineering/kw-to-amps, physics/ohms-law, engineering/kva-to-kw, everyday-life/electricity-cost]
''', '''
## How to use this calculator

Enter the **current** and **voltage**, choose the system and enter the power factor (1 for DC, heaters and kettles). The calculator gives the power in watts. To go from watts to amps, press × on Current and type the watts.

## The formulas

| System | Power |
|---|---|
| DC | P = V × I |
| Single-phase AC | P = V × I × PF |
| Three-phase AC | P = √3 × V<sub>L</sub> × I × PF |

## Amps to watts chart (PF 1)

| Amps | 12 V | 24 V | 120 V | 230 V |
|---|---|---|---|---|
''' + ''.join(f"| {a} A | {a*12:g} W | {a*24:g} W | {a*120:g} W | {a*230:,} W |\n" for a in [0.5, 1, 2, 5, 6, 10, 13, 15, 16, 20, 25, 32]) + '''
## Socket and circuit limits

| Socket / circuit | Max power (approx.) |
|---|---|
| UK 13 A plug (230 V) | 3,000 W |
| India 6 A socket (230 V) | 1,380 W |
| India 16 A socket (230 V) | 3,680 W |
| US 15 A outlet (120 V) | 1,800 W (1,440 W continuous) |
| US 20 A circuit (120 V) | 2,400 W (1,920 W continuous) |

High-power appliances such as kettles, heaters, geysers and air conditioners should use suitably rated sockets.

## Battery systems

For 12 V and 24 V systems (cars, solar, boats), current is high for modest power: a 1,200 W inverter at 12 V draws about 100 A from the battery, plus losses. Use thick cables and fuses close to the battery.

## Watts, VA and power factor

For AC loads with a power factor below 1 (motors, some electronics), the real power in watts is lower than volts × amps. That product is the apparent power in VA — see the [kVA to kW converter](/engineering/kva-to-kw/).
''')

# ---------------------------------------------------------------- inverter battery backup
def backup(ah, v, n, load, eff=0.85, dod=0.8): return ah*v*n*eff*dod/load
page('everyday-life', 'inverter-battery-backup', f'''
title: Inverter Battery Backup Calculator
description: Find how many hours your inverter battery will run your load — or the battery Ah you need for a target backup time.
category: everyday-life
keywords: [inverter battery backup calculator, battery backup time, inverter backup, battery ah calculator, ups backup time, how long will inverter battery last, 150ah battery backup]
updated: {D}
featured: true
variables:
  - {{ id: ah, label: Battery capacity, suffix: Ah, default: 150, min: 0 }}
  - {{ id: v, label: Battery voltage, family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: n, label: Number of batteries, default: 1, min: 1 }}
  - {{ id: load, label: Connected load, family: power, unit: W, default: 300, min: 0.001 }}
  - {{ id: eff, label: Inverter efficiency, family: percent, unit: '%', default: 85, min: 0.01, max: 1 }}
  - {{ id: dod, label: Usable depth of discharge, family: percent, unit: '%', default: 80, min: 0.01, max: 1, help: About 50–80% for lead-acid; 80–100% for lithium. }}
  - {{ id: t, label: Backup time, family: time, unit: h, min: 0 }}
  - {{ id: wh, label: Usable energy, suffix: Wh, min: 0, decimals: 0 }}
equations:
  - wh = ah * v * n * eff * dod
  - t = wh / load / 8766
faq:
  - q: How long will a 150Ah battery run a 300 W load?
    a: "About {backup(150,12,1,300):.1f} hours with a 12 V battery, 85% inverter efficiency and 80% usable capacity."
  - q: How do I calculate inverter battery backup?
    a: Backup hours = battery Ah × voltage × number of batteries × inverter efficiency × usable depth of discharge ÷ load in watts.
  - q: What size battery do I need for 4 hours of backup?
    a: Press × on Battery capacity, enter your load and set the backup time to 4 hours. For 300 W on 12 V, about 147 Ah.
  - q: Why is real backup shorter than calculated?
    a: Lead-acid batteries deliver less capacity at high currents, age over time and lose capacity in heat. Older batteries may give 50–70% of their rated backup.
related: [ecology/battery-storage, engineering/amps-to-watts, everyday-life/electricity-cost, other/battery-life]
''', '''
## How to use this calculator

1. Enter the **battery capacity in Ah** and **voltage** (most home inverter batteries are 12 V).
2. Enter the **number of batteries** (a 24 V inverter uses two 12 V batteries in series).
3. Enter the **connected load** in watts — add up the fans, lights and other devices you will run.
4. Adjust efficiency and usable depth of discharge if you know them.

The calculator shows the backup time and usable energy. To size a battery for a target time, press × on Battery capacity and enter the hours you want.

## The formula

<p class="formula">Backup (h) = Ah × V × n × η × DoD ÷ Load (W)</p>

## Backup time chart (12 V battery, 85% efficiency, 80% DoD)

| Load | 100 Ah | 150 Ah | 200 Ah | 2 × 150 Ah (24 V) |
|---|---|---|---|---|
''' + ''.join(f"| {l} W | {backup(100,12,1,l):.1f} h | {backup(150,12,1,l):.1f} h | {backup(200,12,1,l):.1f} h | {backup(150,12,2,l):.1f} h |\n" for l in [100, 200, 300, 400, 500, 750, 1000]) + '''
## Typical home loads

| Appliance | Power (approx.) |
|---|---|
| LED bulb | 9–12 W |
| Ceiling fan (regular) | 60–75 W |
| Ceiling fan (BLDC) | 28–35 W |
| Wi-Fi router | 10–15 W |
| LED TV (43–55 in) | 60–120 W |
| Laptop | 45–65 W |
| Refrigerator (average running) | 100–200 W |
| Desktop computer | 150–300 W |

A home with 4 fans, 6 LED lights, a router and a TV draws about 300–400 W.

## Choosing the inverter (VA) rating

Inverters are rated in VA. Divide your peak load in watts by about 0.7–0.8: a 600 W peak load needs at least an 800–900 VA inverter. Do not confuse inverter VA (how much power at once) with battery Ah (how long it lasts).

## Battery types

| Battery | Typical life | Usable DoD | Maintenance |
|---|---|---|---|
| Flat plate (lead-acid) | 2–4 years | 50% | Water top-up |
| Tall tubular (lead-acid) | 5–8 years | 70–80% | Water top-up |
| Lithium (LFP) | 8–12+ years | 80–100% | None |

## Getting more backup

- Switch to BLDC fans and LED lights — they can halve the load.
- Keep batteries topped up with distilled water and in a ventilated, shaded spot.
- Replace batteries as a set; mixing old and new reduces backup.
''')

# ---------------------------------------------------------------- EV charging time
def ev(kwh, s, e, kw, eff=0.9): return kwh*(e-s)/(kw*eff)
page('ecology', 'ev-charging-time', f'''
title: EV Charging Time Calculator
description: Work out how long it takes to charge an electric car from your current level to a target — at home, on a wallbox or at a fast charger.
category: ecology
keywords: [ev charging time calculator, electric car charging time, how long to charge ev, ev charger kw, fast charging time, 7.4 kw charger time]
updated: {D}
variables:
  - {{ id: B, label: Battery capacity (usable), suffix: kWh, default: 60, min: 0 }}
  - {{ id: st, label: Current charge level, family: percent, unit: '%', default: 20, min: 0, max: 1 }}
  - {{ id: tg, label: Target charge level, family: percent, unit: '%', default: 80, min: 0, max: 1 }}
  - {{ id: kw, label: Charger power, suffix: kW, default: 7.4, min: 0.1 }}
  - {{ id: eff, label: Charging efficiency, family: percent, unit: '%', default: 90, min: 0.1, max: 1 }}
  - {{ id: en, label: Energy drawn from the grid, suffix: kWh, min: 0, decimals: 1 }}
  - {{ id: t, label: Charging time, family: time, unit: h, min: 0 }}
  - {{ id: pr, label: Electricity price, family: currency, default: 0.15, min: 0, decimals: 3 }}
  - {{ id: cost, label: Cost of this charge, family: currency, min: 0, decimals: 2 }}
equations:
  - en = B * (tg - st) / eff
  - t = en / kw / 8766
  - cost = en * pr
faq:
  - q: How long does it take to charge an EV at home?
    a: "On a 7.4 kW wallbox, a 60 kWh battery from 20% to 80% takes about {ev(60,.2,.8,7.4):.1f} hours. On a 2.3 kW domestic socket it takes about {ev(60,.2,.8,2.3):.0f} hours."
  - q: Why do fast chargers slow down above 80%?
    a: To protect the battery, the car reduces charging power as it fills. The last 20% can take as long as the first 60%.
  - q: What charger power can my car accept?
    a: Check the car’s maximum AC charging rate (often 7–11 kW, some 22 kW) and maximum DC rate. The car charges at the lower of the charger’s and the car’s limit.
related: [ecology/ev-vs-petrol, ecology/battery-storage, ecology/solar-output, everyday-life/fuel-cost]
''', '''
## How to use this calculator

Enter the **usable battery capacity**, the **current** and **target** charge levels, and the **charger power**. You get the energy drawn, the charging time and the cost.

## The formula

<p class="formula">Time = Battery kWh × (target % − start %) ÷ (charger kW × efficiency)</p>

The efficiency covers losses in the charger, cables and battery — typically 85–95%.

## Charging time chart (60 kWh battery, 20% → 80%)

| Charger | Power | Time |
|---|---|---|
''' + ''.join(f"| {n} | {k} kW | {(lambda h: f'{int(h)} h {round(h%1*60):02d} min')(ev(60,.2,.8,k))} |\n" for n, k in [('Domestic socket (India 15 A)', 3.3), ('Domestic socket (UK 10 A)', 2.3), ('Wallbox, single-phase', 7.4), ('Wallbox, three-phase', 11), ('AC public charger', 22), ('DC fast charger', 50), ('DC rapid charger', 150)]) + '''
DC times are optimistic: fast chargers deliver full power only in the middle of the charge range, and many cars accept less than the charger's maximum.

## Charger levels

| Type | Power | Typical use |
|---|---|---|
| Portable / domestic socket | 2–3.3 kW | Overnight top-ups |
| AC wallbox | 7–22 kW | Home and workplace |
| DC fast | 25–60 kW | Highway stops |
| DC ultra-fast | 100–350 kW | Long trips (car permitting) |

## Charge to 80% for daily use

Many manufacturers recommend charging to about 80% for daily driving and to 100% only before long trips. This reduces battery wear and avoids the slow final stage of charging.

## Cost per km

Divide the cost of a charge by the range added. If 40 kWh costs 6.00 and adds 250 km, that is 2.4 per 100 km. Compare with fuel using the [EV vs petrol calculator](/ecology/ev-vs-petrol/).
''')

# ---------------------------------------------------------------- CGPA to percentage
page('everyday-life', 'cgpa-to-percentage', f'''
title: CGPA to Percentage Calculator
description: Convert CGPA to percentage using CBSE, AICTE, Mumbai University and other common formulas — or convert percentage back to CGPA.
category: everyday-life
keywords: [cgpa to percentage, cgpa to percentage calculator, cbse cgpa to percentage, cgpa into percentage, sgpa to percentage, aicte cgpa conversion, percentage to cgpa]
updated: {D}
featured: true
variables:
  - {{ id: g, label: CGPA (out of 10), default: 8.2, min: 0, max: 10 }}
  - id: m
    label: Conversion formula
    default: 1
    options:
      - {{ label: CBSE (CGPA × 9.5), value: 1 }}
      - {{ label: AICTE ((CGPA − 0.75) × 10), value: 2 }}
      - {{ label: Mumbai University (7.1 × CGPA + 11), value: 3 }}
      - {{ label: Simple (CGPA × 10), value: 4 }}
  - {{ id: p, label: Percentage, family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - p = (max(0, 1 - abs(m - 1)) * 9.5 * g + max(0, 1 - abs(m - 2)) * (g - 0.75) * 10 + max(0, 1 - abs(m - 3)) * (7.1 * g + 11) + max(0, 1 - abs(m - 4)) * 10 * g) / 100
faq:
  - q: How do I convert CGPA to percentage in CBSE?
    a: Multiply the CGPA by 9.5. A CGPA of 8.2 is 77.9%.
  - q: What is the AICTE formula for CGPA to percentage?
    a: Percentage = (CGPA − 0.75) × 10. A CGPA of 8.2 is 74.5%.
  - q: How do I convert percentage to CGPA?
    a: Press × on CGPA and type your percentage. For CBSE, divide the percentage by 9.5.
  - q: Which formula should I use?
    a: Use the formula printed on your marksheet or published by your board or university. Employers and universities abroad often ask for the official conversion.
related: [other/grade-percentage, everyday-life/grade-needed, math/percentage, math/average]
''', f'''
## How to use this calculator

1. Enter your **CGPA** on a 10-point scale.
2. Choose the **conversion formula** your board or university uses.

The percentage appears instantly. To go from percentage to CGPA, press × on CGPA and type the percentage.

## Conversion formulas

| Board / university | Formula |
|---|---|
| CBSE (Class 10, older CCE scheme) | % = CGPA × 9.5 |
| AICTE recommended (engineering) | % = (CGPA − 0.75) × 10 |
| University of Mumbai (10-point scale) | % = 7.1 × CGPA + 11 |
| Several universities (simple) | % = CGPA × 10 |

Universities set their own rules, and some publish a different formula or a conversion table. Always check your marksheet or university notice.

## CGPA to percentage chart

| CGPA | CBSE (×9.5) | AICTE | Mumbai | ×10 |
|---|---|---|---|---|
''' + ''.join(f"| {g} | {g*9.5:.1f}% | {(g-.75)*10:.1f}% | {7.1*g+11:.1f}% | {g*10:.0f}% |\n" for g in [5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]) + '''
Values above 100% are not possible; the Mumbai formula reaches 100% at a CGPA of about 12.5, so a 10 CGPA gives 82%.

## SGPA vs CGPA

- **SGPA** (semester grade point average) covers a single semester.
- **CGPA** (cumulative) is the credit-weighted average of all SGPAs so far:

<p class="formula">CGPA = Σ(SGPA × semester credits) ÷ Σ(credits)</p>

If credits are equal each semester, CGPA is simply the average of the SGPAs.

## Why CBSE used 9.5

CBSE derived 9.5 from the average percentage of students scoring in the top grade band across subjects. It applied to the CCE grading scheme; check current CBSE marksheets for how results are reported now.

## Applying abroad

Universities abroad may ask for a WES or similar credential evaluation, which converts grades using its own method. Keep your official transcripts and the university's conversion certificate.
''')

# ---------------------------------------------------------------- GCF / LCM
page('math', 'gcf-lcm', f'''
title: GCF and LCM Calculator (HCF and LCM)
description: Find the greatest common factor (GCF/HCF) and least common multiple (LCM) of two numbers, with the Euclidean method explained.
category: math
keywords: [gcf calculator, lcm calculator, hcf and lcm, greatest common factor, highest common factor, least common multiple, gcd, euclidean algorithm]
updated: {D}
featured: true
variables:
  - {{ id: a, label: First number, default: 84, min: 0, decimals: 0 }}
  - {{ id: b, label: Second number, default: 36, min: 0, decimals: 0 }}
  - {{ id: g, label: GCF / HCF, min: 0, decimals: 0 }}
  - {{ id: l, label: LCM, min: 0, decimals: 0 }}
  - {{ id: pr, label: Product (a × b = GCF × LCM), min: 0, decimals: 0 }}
equations:
  - g = gcd(a, b)
  - l = lcm(a, b)
  - pr = a * b
freedom: 2
faq:
  - q: What is the GCF of 84 and 36?
    a: 12. The LCM is 252.
  - q: What is the difference between HCF and GCF?
    a: Nothing — highest common factor (HCF), greatest common factor (GCF) and greatest common divisor (GCD) all mean the same thing.
  - q: How are GCF and LCM related?
    a: For two positive whole numbers, GCF × LCM = a × b. So LCM = a × b ÷ GCF.
  - q: How do I find the GCF of three numbers?
    a: Find the GCF of the first two, then the GCF of that result and the third number. The LCM works the same way.
related: [math/fraction-to-decimal, math/ratio, statistics/combinations, math/exponent]
''', '''
## How to use this calculator

Enter two **whole numbers**. The calculator shows their greatest common factor (GCF, also called HCF or GCD) and least common multiple (LCM).

## The Euclidean algorithm

The fastest way to find the GCF is to repeatedly replace the larger number with the remainder of dividing it by the smaller one:

| Step | Division | Remainder |
|---|---|---|
| 1 | 84 ÷ 36 = 2 | 12 |
| 2 | 36 ÷ 12 = 3 | 0 |

When the remainder reaches 0, the last non-zero remainder — **12** — is the GCF.

Then LCM = 84 × 36 ÷ 12 = **252**.

## Prime factorisation method

Write each number as a product of primes:

- 84 = 2² × 3 × 7
- 36 = 2² × 3²

- **GCF**: lowest power of each common prime — 2² × 3 = 12
- **LCM**: highest power of every prime — 2² × 3² × 7 = 252

## GCF and LCM table

| Numbers | GCF | LCM |
|---|---|---|
''' + ''.join(f"| {a}, {b} | {math.gcd(a,b)} | {a*b//math.gcd(a,b)} |\n" for a, b in [(12, 18), (15, 25), (24, 36), (8, 12), (14, 21), (45, 60), (17, 23), (100, 75)]) + '''
Numbers with a GCF of 1, such as 17 and 23, are **coprime**.

## Where they are used

- **Simplifying fractions**: divide top and bottom by the GCF. 36/84 = 3/7.
- **Adding fractions**: use the LCM of the denominators as the common denominator. 1/12 + 1/18 uses 36.
- **Scheduling**: two buses every 12 and 18 minutes leave together every 36 minutes (the LCM).
- **Tiling**: the largest square tile that fits a 84 × 36 cm area exactly is 12 cm (the GCF).
''')

# ---------------------------------------------------------------- square root
page('math', 'square-root', f'''
title: Square Root Calculator
description: Find the square root, cube root and square of any number — with a table of perfect squares and simplified radicals.
category: math
keywords: [square root calculator, square root, sqrt, cube root calculator, root calculator, perfect squares, simplify square root]
updated: {D}
featured: true
variables:
  - {{ id: x, label: Number, default: 50, min: 0 }}
  - {{ id: r, label: Square root (√x), min: 0 }}
  - {{ id: c, label: Cube root (∛x), min: 0 }}
  - {{ id: sq, label: Square (x²), min: 0 }}
equations:
  - r = sqrt(x)
  - c = cbrt(x)
  - sq = x^2
freedom: 1
faq:
  - q: What is the square root of 50?
    a: About 7.0711. In simplest radical form, √50 = 5√2.
  - q: Can I find the number from its square root?
    a: Yes. Press × on Number and type the square root — the calculator squares it.
  - q: What is the square root of a negative number?
    a: It is not a real number. √−1 is the imaginary unit i, so √−9 = 3i.
  - q: What are perfect squares?
    a: Whole numbers whose square roots are whole numbers, such as 1, 4, 9, 16, 25 and 36.
related: [math/exponent, math/pythagorean-theorem, math/logarithm, math/quadratic-equation]
''', '''
## How to use this calculator

Enter any non-negative **number** to see its square root, cube root and square. It works backwards too: type a value in Square root and the original number is calculated.

## Perfect squares and cubes

| n | n² | n³ | n | n² | n³ |
|---|---|---|---|---|---|
''' + ''.join(f"| {a} | {a*a} | {a**3} | {a+10} | {(a+10)**2} | {(a+10)**3:,} |\n" for a in range(1, 11)) + '''
## Square roots of 1 to 20

| x | √x | x | √x |
|---|---|---|---|
''' + ''.join(f"| {a} | {math.sqrt(a):.4f} | {a+10} | {math.sqrt(a+10):.4f} |\n" for a in range(1, 11)) + '''
## Simplifying square roots

Look for the largest perfect-square factor:

- √50 = √(25 × 2) = **5√2**
- √72 = √(36 × 2) = **6√2**
- √48 = √(16 × 3) = **4√3**

## Estimating by hand

Find the two perfect squares around the number. √50 lies between √49 = 7 and √64 = 8, much closer to 7. A first estimate of 7.07 is accurate to two decimals.

**Newton's method** refines any guess g: new g = (g + x ÷ g) ÷ 2. Starting from 7 for √50: (7 + 50/7) ÷ 2 = 7.0714 — already correct to four decimal places.

## Rules for roots

- √(a × b) = √a × √b
- √(a ÷ b) = √a ÷ √b
- √a + √b is **not** √(a + b)
- x<sup>1/2</sup> = √x and x<sup>1/3</sup> = ∛x

## Where square roots appear

The [Pythagorean theorem](/math/pythagorean-theorem/), standard deviation, the quadratic formula, circle radius from area and RMS voltage all use square roots.
''')
print('batchA2 done')
