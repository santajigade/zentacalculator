import sys, math, re, glob; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
from ib import L
D = '2026-10-27'

page('engineering', 'loop-resistance', f'''
title: 4–20 mA Loop Resistance Calculator (Maximum Loop Load)
description: Check whether a 4–20 mA loop has enough voltage — maximum loop resistance from supply and transmitter lift-off voltage, with cable and barrier resistance.
category: engineering
keywords: [4-20ma loop resistance calculator, loop load calculation, maximum loop resistance, transmitter lift off voltage, loop power supply, 250 ohm resistor, 2 wire transmitter load]
updated: {D}
variables:
  - {{ id: Vs, label: Loop supply voltage, family: voltage, unit: V, default: 24, min: 0 }}
  - {{ id: Vt, label: Transmitter minimum voltage (lift-off), family: voltage, unit: V, default: 10.5, min: 0 }}
  - {{ id: Im, label: Maximum loop current, family: current, unit: mA, default: 22, min: 0, help: 'Use 22 mA (or 23 mA) so the loop still works at the NAMUR NE 43 fault levels and saturation.' }}
  - {{ id: Rin, label: Input resistance of receiver (PLC/DCS card), family: resistance, unit: ohm, default: 250, min: 0 }}
  - {{ id: Rb, label: Barrier or isolator resistance, family: resistance, unit: ohm, default: 0, min: 0 }}
  - {{ id: len, label: Cable length (one way), family: length, unit: m, imperialUnit: ft, default: 500, min: 0 }}
  - {{ id: rc, label: Conductor resistance, suffix: Ω/km, default: 12.1, min: 0, help: '1.5 mm² copper ≈ 12.1 Ω/km; 1.0 mm² ≈ 18.1 Ω/km; 0.5 mm² ≈ 36 Ω/km at 20 °C.' }}
  - {{ id: Rmax, label: Maximum allowed loop resistance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Rl, label: Actual loop resistance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: M, label: Margin (negative = loop will not work), family: resistance, unit: ohm }}
  - {{ id: Vtx, label: Voltage left at transmitter at max. current, family: voltage, unit: V }}
equations:
  - Rmax = (Vs - Vt) / Im
  - Rl = Rin + Rb + 2 * len / 1000 * rc
  - M = Rmax - Rl
  - Vtx = Vs - Im * Rl
faq:
  - q: How do I calculate maximum loop resistance?
    a: R_max = (supply voltage − transmitter minimum voltage) ÷ maximum loop current. With 24 V, a 10.5 V transmitter and 22 mA, R_max ≈ 614 Ω.
  - q: Why use 22 mA instead of 20 mA?
    a: Transmitters signal faults and over-range above 20 mA (NAMUR NE 43 uses ≥ 21 mA for failure). The loop must still deliver enough voltage at those currents or the alarm signal is lost.
  - q: What happens if the loop resistance is too high?
    a: The transmitter runs out of voltage at high currents, so readings clip near the top of the range — often seen as a reading that never reaches 100%.
  - q: Does HART need a minimum resistance?
    a: Yes. HART communication needs at least 230–250 Ω of loop resistance between the power supply and the transmitter.
related: [engineering/4-20ma-scaling, electrical/cable-voltage-drop, physics/ohms-law, electronics/current-divider]
{L(('instrument-loop-impedance-4-20ma-accuracy', 'Instrument Loop Impedance and 4–20 mA Accuracy'), ('2-wire-3-wire-4-wire-transmitters-in-industrial-automation', '2-Wire, 3-Wire and 4-Wire Transmitters'), ('namur-ne43-standard-explained', 'NAMUR NE 43 Standard Explained'), ('4-to-20-ma-current-loop-explained', '4 to 20 mA Current Loop Explained'))}''', '''
## How to use this calculator

Enter the **loop supply voltage**, the transmitter's **minimum operating (lift-off) voltage** from its datasheet, the **maximum loop current**, the receiver's **input resistance**, any **barrier or isolator** resistance, and the **cable length and conductor resistance**. The calculator shows the maximum resistance the loop can tolerate, the actual resistance and the margin.

## The formulas

<p class="formula">R<sub>max</sub> = (V<sub>supply</sub> − V<sub>transmitter,min</sub>) ÷ I<sub>max</sub></p>

<p class="formula">R<sub>loop</sub> = R<sub>input</sub> + R<sub>barrier</sub> + 2 × length × r<sub>cable</sub></p>

## Example

24 V supply, transmitter needs 10.5 V, 22 mA maximum, 250 Ω PLC input, 500 m of 1.5 mm² cable:

- R<sub>max</sub> = 13.5 ÷ 0.022 = **614 Ω**
- Cable = 2 × 0.5 × 12.1 = 12.1 Ω; total loop = **262 Ω**
- Margin = **352 Ω** — the loop works, with room for a barrier

## Typical voltage drops in a loop

| Component | Typical drop at 20 mA |
|---|---|
| 250 Ω input resistor | 5 V |
| Zener barrier | 6–9 V (about 300–450 Ω) |
| Galvanic isolator (loop-powered input) | 2–4 V |
| Loop-powered indicator | 1–3 V |
| 1 km of 1.5 mm² cable (2 cores) | 0.5 V |

## Conductor resistance (copper, 20 °C)

| Cross-section | Resistance per conductor |
|---|---|
| 0.5 mm² | 36.0 Ω/km |
| 0.75 mm² | 24.5 Ω/km |
| 1.0 mm² | 18.1 Ω/km |
| 1.5 mm² | 12.1 Ω/km |
| 2.5 mm² | 7.41 Ω/km |

## Troubleshooting a low-voltage loop

If the reading clips before 100%, measure the voltage at the transmitter terminals while forcing 20–22 mA. If it is below the lift-off voltage, raise the supply, remove a series device, or use a lower-resistance input.
''')

# ---- add Further reading to existing calculators ----
links = {
 'engineering/4-20ma-scaling': [('4-to-20-ma-signal-conversion-calculator', '4 to 20 mA Signal Conversion Calculator'), ('4-to-20-ma-current-loop-explained', '4 to 20 mA Current Loop Explained'), ('plc-analog-scaling-raw-count', 'PLC Analog Scaling from Raw Counts')],
 'engineering/dp-flow-square-root': [('square-root-extraction-dp-flow', 'Square Root Extraction in DP Flow Measurement'), ('mistakes-in-dp-flow-measurement', 'Common Mistakes in DP Flow Measurement'), ('dp-flow-transmitter-calibration-5-point', 'DP Flow Transmitter 5-Point Calibration')],
 'engineering/flow-meter-k-factor': [('flow-meter-k-factor-calculations', 'Flow Meter K-Factor Calculations'), ('turndown-ratio-in-flow-meters', 'Turndown Ratio in Flow Meters')],
 'engineering/gas-flow-correction': [('actual-flow-standard-flow-normal-flow', 'Actual Flow vs Standard Flow vs Normal Flow'), ('what-is-mmscfd-natural-gas-flow-rate', 'What Is MMSCFD? Natural Gas Flow Rate')],
 'engineering/orifice-flow': [('orifice-plate-flow-measurement', 'Orifice Plate Flow Measurement'), ('orifice-plate-sizing-guide', 'Orifice Plate Sizing Guide'), ('flow-nozzle-vs-orifice-plate-vs-venturi', 'Flow Nozzle vs Orifice Plate vs Venturi')],
 'engineering/venturi-flow': [('venturi-tube-flow-meter', 'Venturi Tube Flow Meter'), ('flow-nozzle-vs-orifice-plate-vs-venturi', 'Flow Nozzle vs Orifice Plate vs Venturi')],
 'engineering/pitot-tube-velocity': [('averaging-pitot-tube-working-principle', 'Averaging Pitot Tube Working Principle')],
 'engineering/pt100-resistance': [('rtd-pt100-vs-pt1000-differences', 'RTD Pt100 vs Pt1000 Differences'), ('callendar-van-dusen-equation-rtd', 'Callendar–Van Dusen Equation for RTDs'), ('how-to-test-an-rtd-pt100', 'How to Test an RTD (Pt100)'), ('rtd-self-heating-error', 'RTD Self-Heating Error')],
 'engineering/reynolds-number': [('what-is-reynolds-number', 'What Is Reynolds Number?')],
 'engineering/hydrostatic-pressure': [('hydrostatic-level-measurement', 'Hydrostatic Level Measurement'), ('dp-transmitter-level-measurement', 'DP Transmitter Level Measurement'), ('zero-elevation-and-zero-suppression', 'Zero Elevation and Zero Suppression')],
 'engineering/horizontal-tank-volume': [('tank-volume-from-level-measurement', 'Tank Volume from Level Measurement'), ('automatic-tank-gauging-explained', 'Automatic Tank Gauging Explained')],
 'engineering/darcy-weisbach-head-loss': [('calculate-pressure-drop-in-pipes', 'How to Calculate Pressure Drop in Pipes'), ('bernoullis-equation-formula', 'Bernoulli’s Equation Formula')],
 'engineering/control-valve-kv-cv': [('control-valve-flow-coefficient', 'Control Valve Flow Coefficient (Cv)'), ('control-valve-sizing-basic-requirements', 'Control Valve Sizing: Basic Requirements'), ('control-valve-rangeability-turndown', 'Control Valve Rangeability and Turndown')],
 'engineering/mass-flow-rate': [('difference-between-mass-flow-and-volumetric-flow', 'Mass Flow vs Volumetric Flow'), ('thermal-mass-flow-meter-working', 'Thermal Mass Flow Meter Working')],
 'engineering/pump-power': [('centrifugal-vs-positive-displacement-pump', 'Centrifugal vs Positive Displacement Pump')],
 'engineering/weir-flow': [('measure-flow-rate-level-sensors', 'Measuring Flow Rate with Level Sensors')],
 'electrical/kva-to-kw': [('power-factor-kw-kva-kvar', 'Power Factor, kW, kVA and kVAr Explained'), ('active-reactive-and-apparent-power', 'Active, Reactive and Apparent Power')],
 'electrical/kw-to-amps': [('how-to-calculate-three-phase-power', 'How to Calculate Three-Phase Power'), ('single-phase-vs-three-phase-power', 'Single-Phase vs Three-Phase Power')],
 'electrical/three-phase-motor-power': [('motor-full-load-current-flc', 'Motor Full Load Current (FLC)'), ('how-to-calculate-three-phase-power', 'How to Calculate Three-Phase Power'), ('motor-efficiency-classes-iec-60034', 'Motor Efficiency Classes (IEC 60034)')],
 'electrical/cable-voltage-drop': [('voltage-drop-calculation', 'Voltage Drop Calculation'), ('cable-size-for-load-current', 'Cable Size for Load Current'), ('cable-sizing-motor-feeders', 'Cable Sizing for Motor Feeders')],
 'electrical/transformer-current': [('how-to-calculate-transformer-kva-rating', 'How to Calculate Transformer kVA Rating'), ('transformer-inrush-current', 'Transformer Inrush Current')],
 'electrical/transformer-short-circuit': [('short-circuit-current-calculation', 'Short Circuit Current Calculation'), ('calculate-short-circuit-fault-current', 'How to Calculate Short Circuit Fault Current')],
 'electronics/reactance': [('impedance-reactance-ac-circuits', 'Impedance and Reactance in AC Circuits'), ('phase-angle-in-ac-circuits', 'Phase Angle in AC Circuits')],
 'electronics/resonant-frequency': [('lc-resonant-circuit-frequency', 'LC Resonant Circuit Frequency')],
 'physics/ohms-law': [('basics-of-ohms-law', 'Basics of Ohm’s Law'), ('electrical-units-of-measure-explained', 'Electrical Units of Measure Explained')],
 'physics/resistors-series-parallel': [('series-vs-parallel-circuits-explained', 'Series vs Parallel Circuits Explained')],
 'physics/rc-time-constant': [('rc-and-rl-time-constant-explained', 'RC and RL Time Constant Explained'), ('snubber-circuit-rc-design', 'Snubber Circuit RC Design')],
 'physics/decibel': [('decibel-in-electronics-db-dbm', 'Decibels in Electronics: dB and dBm')],
 'physics/density': [('what-is-specific-gravity', 'What Is Specific Gravity?'), ('coriolis-density-measurement', 'Coriolis Density Measurement')],
 'physics/heat-conduction': [('what-is-thermal-conductivity', 'What Is Thermal Conductivity?'), ('types-of-heat-exchangers', 'Types of Heat Exchangers')],
 'physics/pressure': [('absolute-vs-gauge-pressure', 'Absolute vs Gauge Pressure'), ('understanding-pascals-law-pressure-instruments', 'Pascal’s Law and Pressure Instruments'), ('u-tube-manometer-working-formula', 'U-Tube Manometer Working and Formula')],
 'physics/doppler-effect': [('transit-time-vs-doppler-ultrasonic-flow-meter', 'Transit-Time vs Doppler Ultrasonic Flow Meters')],
 'chemistry/henderson-hasselbalch': [('ph-meter-calibration-buffers', 'pH Meter Calibration Buffers')],
 'chemistry/nernst-equation': [('what-is-ph-sensor-how-does-it-work', 'What Is a pH Sensor and How Does It Work?'), ('ph-sensor-troubleshooting', 'pH Sensor Troubleshooting')],
 'math/percent-error': [('calibration-error-calculation', 'Calibration Error Calculation'), ('instrument-accuracy-and-error', 'Instrument Accuracy and Error'), ('difference-between-accuracy-and-precision', 'Accuracy vs Precision')],
 'ecology/solar-system-size': [('solar-pv-system-sizing-calculation', 'Solar PV System Sizing Calculation')],
 'everyday-life/inverter-battery-backup': [('calculate-battery-backup-time', 'How to Calculate Battery Backup Time'), ('industrial-battery-charger-float-boost', 'Industrial Battery Charger: Float and Boost')],
 'everyday-life/electricity-cost': [('electrical-energy-consumption-calculation', 'Electrical Energy Consumption Calculation')],
}
B = '/home/claude/zentacalculator/src/content/calculators/'
for cid, items in links.items():
    p = B + cid + '.mdx'; s = open(p).read()
    if '\nlinks:' in s: continue
    a = s.index('\n---', 3)
    s = s[:a] + '\n' + L(*items).rstrip('\n') + s[a:]
    open(p, 'w').write(s)
print('D3 done', len(links))
