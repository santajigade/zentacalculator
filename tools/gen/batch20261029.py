import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
D = '2026-10-29'
G = 9.80665
RHO_CU = 1.724e-8

# ---------------------------------------------------------------- RTD lead wire error
def rw(L, A): return RHO_CU * L / A
ex_rw = rw(50, 0.5e-6); ex_e2 = 2 * ex_rw; ex_t2 = ex_e2 / (100 * 0.00385); ex_e3 = ex_rw * 0.05; ex_t3 = ex_e3 / (100 * 0.00385)
rows = ''.join(f"| {L} m | " + ' | '.join(f"{2*rw(L, A*1e-6)/(100*0.00385):.2f} °C" for A in (0.5, 1.0, 1.5)) + ' |\n' for L in (10, 25, 50, 100, 200))
page('engineering', 'rtd-lead-wire-error', f'''
title: RTD Lead Wire Error Calculator (2-, 3- and 4-Wire Pt100)
description: Calculate the temperature error caused by lead wire resistance in 2-wire and 3-wire Pt100 or Pt1000 RTD circuits from cable length and size.
category: engineering
{intro("Every metre of copper between an RTD and its transmitter adds resistance that the instrument reads as extra temperature. This RTD lead wire error calculator shows how big that error is for 2-wire and 3-wire connections — see the [difference between 2-wire, 3-wire and 4-wire RTDs](ib:difference-between-2-wire-rtd-3-wire-rtd-and-4-wire-rtd) and [how to test an RTD](ib:how-to-test-an-rtd-pt100).")}
keywords: [rtd lead wire error calculator, 2 wire rtd error, 3 wire rtd lead resistance, pt100 cable length error, rtd lead resistance compensation, pt1000 lead error]
updated: {D}
variables:
  - id: R0
    label: RTD type
    default: 100
    options:
      - {{ label: 'Pt100 (100 Ω at 0 °C)', value: 100 }}
      - {{ label: 'Pt1000 (1000 Ω at 0 °C)', value: 1000 }}
  - {{ id: a, label: Temperature coefficient α (per °C), default: 0.00385, min: 0, decimals: 5, help: 'IEC 60751 platinum: 0.00385 Ω/Ω/°C.' }}
  - {{ id: L, label: Cable length (one way), family: length, unit: m, imperialUnit: ft, default: 50, min: 0 }}
  - {{ id: A, label: Conductor cross-section, family: area, unit: mm2, default: 0.5, min: 0 }}
  - {{ id: mm, label: Resistance mismatch between leads (3-wire), family: percent, unit: '%', default: 5, min: 0 }}
  - {{ id: Rw, label: Resistance of one lead, family: resistance, unit: ohm, min: 0 }}
  - {{ id: E2, label: 2-wire error (resistance), family: resistance, unit: ohm, min: 0 }}
  - {{ id: dT2, label: 2-wire temperature error, family: tempdiff, unit: K, min: 0 }}
  - {{ id: E3, label: 3-wire error (resistance), family: resistance, unit: ohm, min: 0 }}
  - {{ id: dT3, label: 3-wire temperature error, family: tempdiff, unit: K, min: 0 }}
equations:
  - Rw = 1.724e-8 * L / A
  - E2 = 2 * Rw
  - dT2 = E2 / (R0 * a)
  - E3 = Rw * mm
  - dT3 = E3 / (R0 * a)
faq:
  - q: How much error does lead resistance cause in a 2-wire Pt100?
    a: A Pt100 changes by about 0.385 Ω per °C, so every 0.385 Ω of total loop resistance reads as 1 °C high. 50 m of 0.5 mm² copper (both leads) adds about 3.4 Ω — nearly 9 °C.
  - q: How does a 3-wire RTD cancel lead resistance?
    a: The third wire puts one lead in each arm of the measuring bridge (or lets the transmitter measure it), so equal lead resistances cancel. Only the difference between the leads remains as error.
  - q: Is a 4-wire RTD completely free of lead error?
    a: Practically yes. Current flows in one pair and voltage is sensed on the other pair, which carries almost no current, so lead resistance does not enter the reading.
  - q: Does a Pt1000 reduce lead wire error?
    a: Yes, by a factor of ten. The same lead resistance is ten times smaller compared with the sensor's 3.85 Ω/°C sensitivity, which is why Pt1000 is often used with 2-wire connections.
related: [engineering/pt100-resistance, electrical/wire-resistance, engineering/loop-resistance, engineering/instrument-accuracy]
''', f'''
## How to use the RTD lead wire error calculator

Choose **Pt100** or **Pt1000**, enter the **cable length** from sensor to transmitter, the **conductor size** and, for 3-wire circuits, the expected **mismatch** between lead resistances (typically 1–5% for one cable, more if leads run through terminals or different cores). The calculator gives the resistance of one lead and the temperature error for 2-wire and 3-wire connections. Lead resistance uses annealed copper at 20 °C (1.724 × 10⁻⁸ Ω·m).

## RTD lead wire error formula

<p class="formula">R<sub>lead</sub> = ρ × L ÷ A</p>

<p class="formula">2-wire: ΔT = 2 R<sub>lead</sub> ÷ (R<sub>0</sub> × α) &nbsp;·&nbsp; 3-wire: ΔT = R<sub>lead</sub> × mismatch ÷ (R<sub>0</sub> × α)</p>

R<sub>0</sub> × α is the sensor sensitivity: 0.385 Ω/°C for a Pt100 and 3.85 Ω/°C for a Pt1000.

## Example

Pt100, 50 m of 0.5 mm² copper, 5% lead mismatch:

- One lead: 1.724 × 10⁻⁸ × 50 ÷ 0.5 × 10⁻⁶ = **{ex_rw:.3f} Ω**
- 2-wire: {ex_e2:.3f} Ω ÷ 0.385 = **{ex_t2:.2f} °C** reading high
- 3-wire: {ex_e3:.4f} Ω ÷ 0.385 = **{ex_t3:.2f} °C**
- 4-wire: **≈ 0 °C**

## 2-wire Pt100 error by cable length and size

| Length (one way) | 0.5 mm² | 1.0 mm² | 1.5 mm² |
|---|---|---|---|
{rows}
For a Pt1000 divide these errors by ten.

## Practical notes

- Use **3-wire** for most plant Pt100s and **4-wire** for laboratory or custody-transfer accuracy.
- Head-mounted transmitters remove the long RTD cable entirely — the 4–20 mA loop carries the signal instead.
- Copper resistance rises about 0.39% per °C, so cable running through hot areas adds more error than this 20 °C figure.
- A 2-wire error can be trimmed out at one temperature by a fixed offset, but it is only correct while the cable temperature stays the same.
''')

# ---------------------------------------------------------------- Calibration error
c_err = 12.05 - 12; c_pct = c_err / 16; c_rd = c_err / 12; c_used = c_pct / 0.0025
page('engineering', 'calibration-error', f'''
title: Calibration Error Calculator (% of Span, As-Found / As-Left)
description: Calculate instrument calibration error as a percent of span and of reading, and check as-found or as-left results against the tolerance.
category: engineering
{intro("Calibration compares an instrument's reading with a reference standard and decides whether the error is inside tolerance. This calibration error calculator works out the error in units, percent of span and percent of reading, and how much of the tolerance is used — see [how to calculate calibration error](ib:calibration-error-calculation) and [as-found and as-left on calibration certificates](ib:calibration-certificate-as-found-as-left).")}
keywords: [calibration error calculator, percent of span error, as found as left tolerance, transmitter calibration error, calibration tolerance check, instrument error calculation]
updated: {D}
variables:
  - {{ id: Lo, label: Output range low (e.g. 4 mA), default: 4, help: 'Use any unit — mA, bar, °C — as long as all values match.' }}
  - {{ id: Hi, label: Output range high (e.g. 20 mA), default: 20 }}
  - {{ id: X, label: Expected (reference) value, default: 12 }}
  - {{ id: Y, label: Measured (as-found) value, default: 12.05 }}
  - {{ id: Tol, label: Tolerance (± % of span), family: percent, unit: '%', default: 0.25, min: 0 }}
  - {{ id: Err, label: Error (measured − expected), decimals: 4 }}
  - {{ id: Ps, label: Error (% of span), family: percent, unit: '%', decimals: 3 }}
  - {{ id: Pr, label: Error (% of reading), family: percent, unit: '%', decimals: 3 }}
  - {{ id: U, label: Tolerance used (over 100% = fail), family: percent, unit: '%', min: 0, decimals: 1 }}
equations:
  - Err = Y - X
  - Ps = Err / (Hi - Lo)
  - Pr = Err / X
  - U = abs(Ps) / Tol
faq:
  - q: How do I calculate calibration error as a percent of span?
    a: Error % of span = (measured − expected) ÷ (upper range − lower range) × 100. For a 4–20 mA transmitter reading 12.05 mA instead of 12 mA, the error is 0.05 ÷ 16 = 0.31% of span.
  - q: What is the difference between as-found and as-left?
    a: As-found is the reading before any adjustment and shows how far the instrument drifted since the last calibration. As-left is the reading after adjustment and must be inside the tolerance.
  - q: What tolerance should I use?
    a: Usually the plant's calibration tolerance for that loop, which is often equal to or wider than the manufacturer's accuracy — for example ±0.25% or ±0.5% of span for a pressure transmitter.
  - q: What is the difference between % of span and % of reading?
    a: Percent of span divides by the full range, so it is constant across the scale. Percent of reading divides by the actual value, so the same error looks larger near the bottom of the range.
related: [engineering/five-point-calibration, engineering/instrument-accuracy, engineering/4-20ma-scaling, math/percent-error]
''', f'''
## How to use the calibration error calculator

Enter the **output range** of the instrument (4 and 20 for a 4–20 mA transmitter), the **expected value** from your reference standard, the **measured value** and the **tolerance** as ± % of span. The calculator gives the error, the error as a percentage of span and of reading, and the share of the tolerance used: **over 100% means the point fails**.

## Calibration error formulas

<p class="formula">Error = Measured − Expected</p>

<p class="formula">% of span = Error ÷ (URV − LRV) × 100 &nbsp;·&nbsp; % of reading = Error ÷ Expected × 100</p>

<p class="formula">Tolerance used = |% of span| ÷ Tolerance × 100</p>

## Example

A 4–20 mA pressure transmitter at 50% input should read 12.000 mA; it reads 12.050 mA. Tolerance ±0.25% of span:

- Error = **+{c_err:.3f} mA**
- % of span = 0.05 ÷ 16 = **{c_pct*100:.4f}%**
- % of reading = 0.05 ÷ 12 = **{c_rd*100:.3f}%**
- Tolerance used = 0.3125 ÷ 0.25 = **{c_used*100:.0f}%** → as-found **fail**, adjust and record as-left

## Tolerance in mA for a 4–20 mA loop

| Tolerance (% of span) | ± mA | ± µA |
|---|---|---|
''' + ''.join(f"| ±{t}% | {16*t/100:.3f} mA | {16*t*10:.0f} µA |\n" for t in (0.1, 0.25, 0.5, 1.0, 2.0)) + '''
## Good calibration practice

- Use a reference at least **4 times more accurate** than the tolerance (test uncertainty ratio 4:1).
- Record **as-found** data before touching zero or span — it is what tells you whether the process was measured correctly since the last calibration.
- Test up and down the scale to reveal **hysteresis**; the [5-point calibration calculator](/engineering/five-point-calibration/) lists the test points.
''')

# ---------------------------------------------------------------- 5-point calibration
pts = [0, 0.25, 0.5, 0.75, 1]
tbl = ''.join(f"| {int(p*100)}% | {0+p*10:g} bar | {4+16*p:.2f} mA | {1+4*p:.2f} V |\n" for p in pts)
page('engineering', 'five-point-calibration', f'''
title: 5-Point Calibration Calculator (0–25–50–75–100% Table)
description: Generate a 5-point calibration table for any transmitter — input values and expected 4–20 mA (or other) outputs at 0, 25, 50, 75 and 100% of range.
category: engineering
{intro("A 5-point check at 0, 25, 50, 75 and 100% of range is the standard way to calibrate a transmitter and reveal zero, span and linearity errors. This 5-point calibration calculator builds the table of input values and expected outputs for any range — see the [calibration process for a DP transmitter](ib:calibration-process-differential-pressure-transmitter).")}
keywords: [5 point calibration calculator, five point calibration table, transmitter calibration points, 4-20ma calibration table, 0 25 50 75 100 calibration, calibration check sheet]
updated: {D}
variables:
  - {{ id: LRV, label: Input range low (LRV), default: 0, help: 'Process units, e.g. bar, °C, mbar, %.' }}
  - {{ id: URV, label: Input range high (URV), default: 10 }}
  - {{ id: Olo, label: Output low (e.g. 4 mA), default: 4 }}
  - {{ id: Ohi, label: Output high (e.g. 20 mA), default: 20 }}
  - {{ id: I25, label: Input at 25%, decimals: 4 }}
  - {{ id: I50, label: Input at 50%, decimals: 4 }}
  - {{ id: I75, label: Input at 75%, decimals: 4 }}
  - {{ id: O25, label: Expected output at 25%, decimals: 4 }}
  - {{ id: O50, label: Expected output at 50%, decimals: 4 }}
  - {{ id: O75, label: Expected output at 75%, decimals: 4 }}
equations:
  - I25 = LRV + 0.25 * (URV - LRV)
  - I50 = LRV + 0.5 * (URV - LRV)
  - I75 = LRV + 0.75 * (URV - LRV)
  - O25 = Olo + 0.25 * (Ohi - Olo)
  - O50 = Olo + 0.5 * (Ohi - Olo)
  - O75 = Olo + 0.75 * (Ohi - Olo)
faq:
  - q: Why calibrate at five points?
    a: Zero and span alone only fix the ends of the range. The 25, 50 and 75% points show non-linearity, and testing upscale then downscale reveals hysteresis.
  - q: What are the 5 calibration points for a 4–20 mA transmitter?
    a: 4, 8, 12, 16 and 20 mA, corresponding to 0, 25, 50, 75 and 100% of the calibrated input range.
  - q: Does the table work for a suppressed or elevated zero?
    a: Yes. Enter a negative LRV for an elevated range (for example −50 to +150 mbar) and the input points are spaced across that range.
  - q: What about reverse-acting outputs?
    a: Enter the output high value as the low and vice versa (for example 20 and 4) — the expected outputs then decrease as the input rises.
related: [engineering/calibration-error, engineering/4-20ma-scaling, engineering/signal-converter, engineering/instrument-accuracy]
''', f'''
## How to use the 5-point calibration calculator

Enter the **calibrated input range** (LRV and URV) and the **output range** (4 and 20 for a 4–20 mA transmitter, 1 and 5 for a 1–5 V signal). The calculator gives the input to apply and the output you should read at 25, 50 and 75%; the 0% and 100% points are the range ends you entered. Record the measured values and check each one with the [calibration error calculator](/engineering/calibration-error/).

## Calibration point formula

<p class="formula">Input<sub>p</sub> = LRV + p × (URV − LRV) &nbsp;·&nbsp; Output<sub>p</sub> = O<sub>low</sub> + p × (O<sub>high</sub> − O<sub>low</sub>)</p>

where p = 0, 0.25, 0.5, 0.75 and 1.

## Example: 0–10 bar pressure transmitter

| Point | Input | 4–20 mA output | 1–5 V output |
|---|---|---|---|
{tbl}
## Calibration procedure

1. Isolate the transmitter, connect the pressure source and a reference gauge, and connect a multimeter or calibrator in the loop.
2. Apply each point **upscale** (0 → 100%) and record the output, then repeat **downscale** (100 → 0%).
3. Calculate the error at each point as % of span. If any point is out of tolerance, adjust zero and span and repeat to record as-left data.
4. For DP flow transmitters with square-root extraction, the output at 25% DP is 50% flow — see the [DP flow square-root calculator](/engineering/dp-flow-square-root/).
''')

# ---------------------------------------------------------------- PLC analog scaling
pa_pct = (20736 - 0) / 27648; pa_eu = 0 + pa_pct * 10; pa_res = 10 / 27648
plc = [('Siemens S7-1200 / S7-1500 (nominal range)', 0, 27648), ('12-bit converter', 0, 4095), ('Mitsubishi Q64AD (normal resolution)', 0, 4000),
       ('Modicon M340 (default)', 0, 10000), ('15-bit unsigned', 0, 32767), ('16-bit unsigned', 0, 65535)]
plct = ''.join(f"| {nm} | {a:,} – {b:,} | {100/(b-a):.5f}% | {16000/(b-a):.3f} µA |\n" for nm, a, b in plc)
page('engineering', 'plc-analog-scaling', f'''
title: PLC Analog Scaling Calculator (Raw Counts to Engineering Units)
description: Convert PLC analog input raw counts to engineering units and back — for Siemens 0–27648, 0–4095, 0–32767 and any custom raw range.
category: engineering
{intro("A PLC analog input card turns a 4–20 mA or 0–10 V signal into a raw integer that the program must scale into bar, °C or m³/h. This PLC analog scaling calculator converts raw counts to engineering units in either direction and shows the resolution — see [PLC analog scaling from raw counts](ib:plc-analog-scaling-raw-count) and [analog signal resolution in PLCs](ib:analog-signal-resolution-in-plc).")}
keywords: [plc analog scaling calculator, raw count to engineering units, analog input scaling formula, siemens 27648 scaling, plc scaling 4-20ma, scale analog input plc]
updated: {D}
variables:
  - {{ id: Cmin, label: Raw count at range low, default: 0 }}
  - {{ id: Cmax, label: Raw count at range high, default: 27648, help: 'Siemens S7-1200/1500: 27648. 12-bit cards: 4095. Check the card manual.' }}
  - {{ id: Emin, label: Engineering units at range low, default: 0 }}
  - {{ id: Emax, label: Engineering units at range high, default: 10 }}
  - {{ id: C, label: Raw count, default: 20736 }}
  - {{ id: P, label: Percent of range, family: percent, unit: '%', decimals: 2 }}
  - {{ id: EU, label: Value in engineering units, decimals: 4 }}
  - {{ id: R, label: Resolution (engineering units per count), decimals: 6 }}
equations:
  - P = (C - Cmin) / (Cmax - Cmin)
  - EU = Emin + P * (Emax - Emin)
  - R = (Emax - Emin) / (Cmax - Cmin)
faq:
  - q: What is the PLC analog scaling formula?
    a: EU = EU_min + (raw − raw_min) ÷ (raw_max − raw_min) × (EU_max − EU_min). It is the equation of a straight line through the two range end points.
  - q: Why does Siemens use 27648 instead of 32767?
    a: Siemens maps the nominal range to 0–27648 and keeps the counts above it (up to 32511) for overrange, so the program can detect a signal above 20 mA before it saturates.
  - q: How do I convert engineering units back to raw counts?
    a: Clear the raw count, enter the value in engineering units and calculate — raw = raw_min + (EU − EU_min) ÷ (EU_max − EU_min) × (raw_max − raw_min).
  - q: Does the raw range change for 4–20 mA versus 0–20 mA?
    a: On many cards, yes — some map 4–20 mA to the full raw range while others give a non-zero count at 4 mA (for example 3277–16384 on older 16384-count cards). Always check the input card manual.
related: [engineering/4-20ma-scaling, electronics/adc-resolution, engineering/signal-converter, engineering/five-point-calibration]
''', f'''
## How to use the PLC analog scaling calculator

Enter the **raw count range** of the analog input card for your signal type, the **engineering range** of the transmitter and the **raw count** the PLC is reading. You get the value in engineering units, the percent of range and the resolution of one count. To go the other way, clear the raw count and enter a value in engineering units.

## PLC analog scaling formula

<p class="formula">EU = EU<sub>min</sub> + (Raw − Raw<sub>min</sub>) ÷ (Raw<sub>max</sub> − Raw<sub>min</sub>) × (EU<sub>max</sub> − EU<sub>min</sub>)</p>

This is what the Siemens NORM_X / SCALE_X pair, the Rockwell SCP instruction and most PLC "scale" blocks calculate.

## Example

A 0–10 bar transmitter on a Siemens S7-1200 input (0–27648) reads **20736** counts:

- Percent of range = 20736 ÷ 27648 = **{pa_pct*100:.1f}%**
- Pressure = 0 + 0.75 × 10 = **{pa_eu:g} bar**
- Resolution = 10 ÷ 27648 = **{pa_res:.6f} bar per count**

## Raw ranges and resolution of common analog inputs

| Card / converter | Raw range | One count (% of span) | One count on 4–20 mA |
|---|---|---|---|
{plct}
Raw ranges depend on card model and configuration — confirm with the manufacturer's manual.

## Tips

- Scale in **floating point** (REAL) to avoid integer truncation.
- Clamp or alarm values outside the range: below about 3.8 mA or above 20.5 mA usually means a sensor fault (NAMUR NE 43).
- If the transmitter already does square-root extraction, scale linearly; otherwise apply the root after scaling.
''')

# ---------------------------------------------------------------- Signal converter
sc = ''.join(f"| {p}% | {4+0.16*p:.2f} mA | {0.2*p:.2f} mA | {1+0.04*p:.2f} V | {0.1*p:.2f} V |\n" for p in (0, 10, 25, 50, 75, 90, 100))
page('engineering', 'signal-converter', f'''
title: Signal Converter Calculator (4–20 mA ↔ 0–10 V ↔ 1–5 V)
description: Convert between 4–20 mA, 0–20 mA, 0–10 V and 1–5 V analog signals and percent of range — for transmitters, PLCs and signal isolators.
category: engineering
{intro("Field instruments, PLC inputs and drives use different analog standards, and a signal isolator or converter maps one onto another by percent of range. This signal converter calculator translates 4–20 mA, 0–20 mA, 0–10 V and 1–5 V values in any direction — see [4 to 20 mA signal conversion](ib:4-to-20-ma-signal-conversion) and why [4–20 mA is the best signal for industrial automation](ib:4-20ma-the-best-signal-for-industrial-automation).")}
keywords: [signal converter calculator, 4-20ma to 0-10v calculator, ma to volts converter, 1-5v to 4-20ma, 0-10v to 4-20ma conversion, analog signal conversion]
updated: {D}
variables:
  - {{ id: I, label: 4–20 mA signal, family: current, unit: mA, default: 12 }}
  - {{ id: P, label: Percent of range, family: percent, unit: '%', decimals: 2 }}
  - {{ id: I0, label: 0–20 mA signal, family: current, unit: mA }}
  - {{ id: V10, label: 0–10 V signal, family: voltage, unit: V }}
  - {{ id: V15, label: 1–5 V signal, family: voltage, unit: V }}
  - {{ id: V5, label: 0–5 V signal, family: voltage, unit: V }}
equations:
  - P = (I - 0.004) / 0.016
  - I0 = 0.02 * P
  - V10 = 10 * P
  - V15 = 1 + 4 * P
  - V5 = 5 * P
faq:
  - q: How do I convert 4–20 mA to 0–10 V?
    a: Find the percent of range, (mA − 4) ÷ 16, then multiply by 10 V. 12 mA is 50%, which is 5 V.
  - q: How do I convert 4–20 mA to 1–5 V?
    a: Pass the current through a precision 250 Ω resistor — 4 mA gives 1 V and 20 mA gives 5 V. This is how many DCS and PLC voltage inputs read current loops.
  - q: Can I convert 0–10 V to 4–20 mA with a resistor?
    a: No. Converting voltage to a current loop needs an active converter or isolator that drives a controlled current. Going from current to voltage only needs a resistor.
  - q: Why is 4 mA used instead of 0 mA?
    a: A live zero lets the receiver tell a 0% signal from a broken wire (0 mA), and leaves enough current to power 2-wire transmitters.
related: [engineering/4-20ma-scaling, engineering/plc-analog-scaling, engineering/loop-resistance, electronics/voltage-divider]
''', f'''
## How to use the signal converter calculator

Enter a value in **any one** field — a 4–20 mA current, a percent of range or one of the voltage signals — and the calculator fills in the equivalent value for every other standard. All conversions are linear by percent of range.

## Signal conversion formulas

<p class="formula">% = (I<sub>4–20</sub> − 4 mA) ÷ 16 mA</p>

<p class="formula">I<sub>0–20</sub> = 20 mA × % &nbsp;·&nbsp; V<sub>0–10</sub> = 10 V × % &nbsp;·&nbsp; V<sub>1–5</sub> = 1 V + 4 V × % &nbsp;·&nbsp; V<sub>0–5</sub> = 5 V × %</p>

## Example

12 mA on a 4–20 mA loop:

- Percent = (12 − 4) ÷ 16 = **50%**
- 0–20 mA = **10 mA**, 0–10 V = **5 V**, 1–5 V = **3 V**, 0–5 V = **2.5 V**

## Signal conversion table

| % of range | 4–20 mA | 0–20 mA | 1–5 V | 0–10 V |
|---|---|---|---|---|
{sc}
## Choosing a signal

- **4–20 mA** is immune to voltage drop along the cable, detects a broken wire and can power 2-wire transmitters — the plant standard.
- **0–10 V** is common for drives, dampers and building automation over short distances.
- **1–5 V** is the voltage across a 250 Ω resistor in a 4–20 mA loop and is how many controllers read current inputs.
''')

# ---------------------------------------------------------------- Low-flow cutoff
lf = ''.join(f"| {q}% | {q*q/100:g}% | {50/q:g} |\n" for q in (1, 2, 3, 5, 7, 10, 20, 50, 100))
page('engineering', 'low-flow-cutoff', f'''
title: Low Flow Cutoff Calculator (Square-Root DP Flow)
description: Calculate the DP at a square-root low-flow cutoff, the cutoff flow and the noise gain near zero for orifice and other DP flow transmitters.
category: engineering
{intro("With square-root extraction, flow = √DP, so tiny DP noise near zero becomes a large, jumping flow reading. A low-flow cutoff forces the output to zero below a set point. This low flow cutoff calculator converts the cutoff between flow and DP and shows how much the root amplifies noise — see [square-root extraction in DP flow measurement](ib:square-root-extraction-dp-flow).")}
keywords: [low flow cutoff calculator, square root low flow cutoff, dp flow cutoff, flow cutoff percentage, square root extraction noise, orifice low flow cutoff]
updated: {D}
variables:
  - {{ id: q, label: Cutoff (% of maximum flow), family: percent, unit: '%', default: 5, min: 0, max: 1 }}
  - {{ id: Qmax, label: Maximum flow, family: flow, unit: m3h, imperialUnit: gpm, default: 100, min: 0 }}
  - {{ id: DPmax, label: DP at maximum flow, family: pressure, unit: mbar, default: 250, min: 0 }}
  - {{ id: x, label: Cutoff (% of maximum DP), family: percent, unit: '%', min: 0, max: 1, decimals: 3 }}
  - {{ id: Qc, label: Cutoff flow, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: DPc, label: Cutoff DP, family: pressure, unit: mbar, min: 0 }}
  - {{ id: Gn, label: Noise gain at cutoff (× flow % per DP %), min: 0, decimals: 2 }}
equations:
  - x = q^2
  - Qc = q * Qmax
  - DPc = x * DPmax
  - Gn = 1 / (2 * q)
faq:
  - q: Why is a low-flow cutoff needed with square-root extraction?
    a: Near zero the slope of √DP becomes very steep. At 1% flow, a DP change of 0.01% of span moves the flow reading by 0.5% — so transmitter noise and zero drift look like real flow.
  - q: What cutoff value is typical?
    a: Most DP flow transmitters and DCS blocks use a cutoff between 5% and 10% of flow, which is only 0.25% to 1% of DP.
  - q: What is the noise gain?
    a: It is the slope of the square-root curve, d(flow) ÷ d(DP) = 1 ÷ (2 × flow fraction). At 5% flow it is 10, so 0.1% DP noise becomes 1% flow noise.
  - q: Does the cutoff hide real flow?
    a: Yes, anything below the cutoff reads zero. Totalizers will miss it, so choose a meter with better turndown if low flows matter.
related: [engineering/dp-flow-square-root, engineering/orifice-flow, engineering/turndown-ratio, engineering/4-20ma-scaling]
''', f'''
## How to use the low flow cutoff calculator

Enter the **cutoff** as a percentage of maximum flow, the **maximum flow** and the **DP at maximum flow** (the transmitter's calibrated span). You get the cutoff in DP terms, the actual cutoff flow and DP, and the noise gain at that point. To find the flow corresponding to a DP cutoff set in a transmitter, clear the flow cutoff and enter the DP percentage.

## Low flow cutoff formulas

<p class="formula">Flow fraction q = √(DP fraction) &nbsp;⇔&nbsp; DP fraction = q²</p>

<p class="formula">Noise gain = d(q) ÷ d(DP) = 1 ÷ (2q)</p>

## Example

Cutoff at 5% flow on a 0–100 m³/h meter with 250 mbar DP span:

- DP at cutoff = 0.05² = **0.25%** of span → **0.625 mbar**
- Cutoff flow = **5 m³/h**
- Noise gain = 1 ÷ (2 × 0.05) = **10** — each 0.1% of DP noise shows as 1% flow

## Flow, DP and noise gain

| Flow (% of max) | DP (% of max) | Noise gain |
|---|---|---|
{lf}
## Where to apply the cutoff

- In the **transmitter** (many smart DP transmitters have a configurable low-flow cutoff and linear-to-root transition).
- Or in the **DCS/PLC** flow block — but only in one place, not both.
- Fix zero drift first: re-zero the transmitter at line pressure with equalising valve open before blaming noise.
''')

# ---------------------------------------------------------------- Ziegler-Nichols
Ku, Pu = 2, 60
zn = [('P only', 0.5*Ku, None, None), ('PI', 0.45*Ku, Pu/1.2, None), ('PID (classic)', 0.6*Ku, Pu/2, Pu/8),
      ('PI (Tyreus–Luyben)', Ku/3.2, 2.2*Pu, None), ('PID (Tyreus–Luyben)', Ku/2.2, 2.2*Pu, Pu/6.3)]
znt = ''.join(f"| {nm} | {kc:.3g} | {100/kc:.0f}% | {('%.3g s' % ti) if ti else '—'} | {('%.3g s' % td) if td else '—'} |\n" for nm, kc, ti, td in zn)
page('engineering', 'ziegler-nichols-pid-tuning', f'''
title: Ziegler–Nichols PID Tuning Calculator (Ultimate Gain Method)
description: Calculate P, PI and PID controller settings from ultimate gain Ku and ultimate period Pu using the Ziegler–Nichols closed-loop tuning rules.
category: engineering
{intro("The Ziegler–Nichols closed-loop method finds the gain at which a loop just oscillates steadily (Ku) and the period of that oscillation (Pu), then sets the controller from simple ratios. This Ziegler–Nichols PID tuning calculator gives P, PI and PID settings — see the [PID controller tuning guide](ib:pid-controller-tuning-guide) and [step-test, relay and Ziegler–Nichols auto-tuning in a DCS](ib:dcs-pid-auto-tune-step-test-relay-feedback-ziegler-nichols).")}
keywords: [ziegler nichols calculator, pid tuning calculator, ultimate gain method, ziegler nichols tuning rules, ku pu tuning, closed loop pid tuning]
updated: {D}
variables:
  - {{ id: Ku, label: Ultimate gain (Ku), default: 2, min: 0 }}
  - {{ id: Pu, label: Ultimate period (Pu), family: seconds, unit: s, default: 60, min: 0 }}
  - {{ id: Kp, label: P-only controller gain, min: 0, decimals: 3 }}
  - {{ id: Kpi, label: PI controller gain, min: 0, decimals: 3 }}
  - {{ id: Tipi, label: PI integral time, family: seconds, unit: s, min: 0 }}
  - {{ id: Kpid, label: PID controller gain, min: 0, decimals: 3 }}
  - {{ id: Tipid, label: PID integral time, family: seconds, unit: s, min: 0 }}
  - {{ id: Td, label: PID derivative time, family: seconds, unit: s, min: 0 }}
equations:
  - Kp = 0.5 * Ku
  - Kpi = 0.45 * Ku
  - Tipi = Pu / 1.2
  - Kpid = 0.6 * Ku
  - Tipid = Pu / 2
  - Td = Pu / 8
faq:
  - q: How do I find Ku and Pu?
    a: Put the controller in automatic with integral and derivative off, then raise the gain in small steps until the process variable oscillates with constant amplitude. That gain is Ku and the time between peaks is Pu.
  - q: What are the Ziegler–Nichols PID settings?
    a: Kc = 0.6 Ku, Ti = Pu ÷ 2 and Td = Pu ÷ 8. For PI, Kc = 0.45 Ku and Ti = Pu ÷ 1.2.
  - q: Why are Ziegler–Nichols settings so aggressive?
    a: They target a quarter-amplitude decay, which overshoots and oscillates. Many engineers halve the gain, or use the gentler Tyreus–Luyben rules shown in the table.
  - q: How do I convert gain to proportional band?
    a: PB (%) = 100 ÷ Kc. A gain of 1.2 is a proportional band of about 83%.
related: [engineering/lambda-tuning, engineering/fopdt-step-test, engineering/sensor-response-time, engineering/4-20ma-scaling]
''', f'''
## How to use the Ziegler–Nichols PID tuning calculator

Enter the **ultimate gain** Ku and the **ultimate period** Pu from your closed-loop test. The calculator gives the controller gain for P, PI and PID control and the integral and derivative times in seconds. Settings assume the ideal (non-interacting) PID form with integral time in seconds per repeat; check whether your controller uses gain or proportional band, and repeats per minute or minutes per repeat.

## Ziegler–Nichols closed-loop rules

| Controller | K<sub>c</sub> | T<sub>i</sub> | T<sub>d</sub> |
|---|---|---|---|
| P | 0.5 K<sub>u</sub> | — | — |
| PI | 0.45 K<sub>u</sub> | P<sub>u</sub> ÷ 1.2 | — |
| PID | 0.6 K<sub>u</sub> | P<sub>u</sub> ÷ 2 | P<sub>u</sub> ÷ 8 |

## Example

A loop oscillates steadily at **Ku = {Ku}** with a period **Pu = {Pu} s**:

| Rule | K<sub>c</sub> | PB | T<sub>i</sub> | T<sub>d</sub> |
|---|---|---|---|---|
{znt}
## Cautions

- The test drives the loop to the edge of instability — don't do it on loops where oscillation is unsafe; use a step test and the [lambda tuning calculator](/engineering/lambda-tuning/) instead.
- Valve stiction and sensor lag change Ku and Pu; fix mechanical problems first.
- After tuning, test with a small set-point step and reduce gain if overshoot is excessive.
''')

# ---------------------------------------------------------------- Lambda / Cohen-Coon
K, tau, th, lam = 2, 60, 10, 30
lkc = tau / (K * (lam + th)); r = th / tau
cckc = (1 / K) * (tau / th) * (0.9 + th / (12 * tau)); ccti = th * (30 + 3 * r) / (9 + 20 * r)
lt = ''.join(f"| {l:g} s ({l/th:g} θ) | {tau/(K*(l+th)):.3f} | {tau:g} s |\n" for l in (10, 20, 30, 60, 120))
page('engineering', 'lambda-tuning', f'''
title: Lambda Tuning Calculator (IMC PI & Cohen–Coon)
description: Calculate PI controller gain and integral time from process gain, time constant and dead time using lambda (IMC) tuning, with Cohen–Coon for comparison.
category: engineering
{intro("Lambda tuning sets a PI controller so the closed loop responds like a first-order lag with a time constant λ that you choose — fast or gentle, with no overshoot. This lambda tuning calculator uses process gain, time constant and dead time from a step test and compares the result with Cohen–Coon — see [PID controller tuning parameters](ib:pid-controller-tuning-parameters) and [how to tune a PID controller](ib:how-to-tune-a-pid-controller).")}
keywords: [lambda tuning calculator, imc tuning calculator, cohen coon calculator, pi controller tuning, fopdt tuning rules, self regulating loop tuning]
updated: {D}
variables:
  - {{ id: K, label: Process gain (Δ PV % ÷ Δ output %), default: 2, min: 0 }}
  - {{ id: tau, label: Process time constant (τ), family: seconds, unit: s, default: 60, min: 0 }}
  - {{ id: th, label: Dead time (θ), family: seconds, unit: s, default: 10, min: 0 }}
  - {{ id: lam, label: Closed-loop time constant (λ), family: seconds, unit: s, default: 30, min: 0, help: 'λ = τ for a robust loop, ≥ 3θ for safety; smaller λ is faster but less robust.' }}
  - {{ id: Kc, label: Lambda PI gain, min: 0, decimals: 3 }}
  - {{ id: Ti, label: Lambda PI integral time, family: seconds, unit: s, min: 0 }}
  - {{ id: Kcc, label: Cohen–Coon PI gain, min: 0, decimals: 3 }}
  - {{ id: Ticc, label: Cohen–Coon PI integral time, family: seconds, unit: s, min: 0 }}
equations:
  - Kc = tau / (K * (lam + th))
  - Ti = tau
  - Kcc = (1 / K) * (tau / th) * (0.9 + th / (12 * tau))
  - Ticc = th * (30 + 3 * th / tau) / (9 + 20 * th / tau)
faq:
  - q: What is the lambda tuning formula?
    a: For a self-regulating process, Kc = τ ÷ (K × (λ + θ)) and Ti = τ. λ is the closed-loop time constant you want.
  - q: How do I choose lambda?
    a: Start with λ equal to the process time constant (or three times the dead time, whichever is larger). Smaller λ gives a faster but less robust loop; larger λ is slower and more tolerant of model error.
  - q: Why does Cohen–Coon give a much higher gain?
    a: Cohen–Coon aims for quarter-amplitude decay, so it is aggressive and sensitive to model error. It is mainly useful for loops with dead time that is large compared with the time constant.
  - q: Where do K, τ and θ come from?
    a: From an open-loop step test — use the [FOPDT step test calculator](/engineering/fopdt-step-test/) to extract them from the 28.3% and 63.2% response times.
related: [engineering/fopdt-step-test, engineering/ziegler-nichols-pid-tuning, engineering/sensor-response-time, engineering/turndown-ratio]
''', f'''
## How to use the lambda tuning calculator

Enter the **process gain** K, **time constant** τ and **dead time** θ of a first-order-plus-dead-time (FOPDT) model, plus the desired **closed-loop time constant** λ. The calculator gives the lambda (IMC) PI settings and the Cohen–Coon PI settings for comparison. Gains are dimensionless (% output per % PV); integral time is in seconds per repeat.

## Lambda (IMC) PI tuning

<p class="formula">K<sub>c</sub> = τ ÷ [K × (λ + θ)] &nbsp;·&nbsp; T<sub>i</sub> = τ</p>

## Cohen–Coon PI tuning

<p class="formula">K<sub>c</sub> = (1/K)(τ/θ)(0.9 + θ/12τ) &nbsp;·&nbsp; T<sub>i</sub> = θ(30 + 3θ/τ) ÷ (9 + 20θ/τ)</p>

## Example

K = {K}, τ = {tau} s, θ = {th} s, λ = {lam} s:

- Lambda PI: K<sub>c</sub> = 60 ÷ (2 × 40) = **{lkc:.3f}**, T<sub>i</sub> = **{tau} s**
- Cohen–Coon PI: K<sub>c</sub> = **{cckc:.3f}**, T<sub>i</sub> = **{ccti:.1f} s**

The Cohen–Coon gain is more than three times higher — expect overshoot. Lambda tuning gives a smooth, non-oscillating response.

## Effect of λ on controller gain (same process)

| λ | K<sub>c</sub> | T<sub>i</sub> |
|---|---|---|
{lt}
## Notes

- These rules are for **self-regulating** processes (flow, temperature, pressure). Integrating processes such as tank level need the integrating-process lambda rules.
- Flow loops are often tuned with λ of 1–3 × τ; temperature loops with λ = τ or slower.
- Coordinate λ across cascaded loops: the inner (slave) loop should be at least 3–5 times faster than the outer loop.
''')

# ---------------------------------------------------------------- FOPDT step test
du, dy, t28, t63 = 10, 20, 25, 40
f_tau = 1.5 * (t63 - t28); f_th = t63 - f_tau; f_K = dy / du
page('engineering', 'fopdt-step-test', f'''
title: FOPDT Step Test Calculator (Gain, Time Constant, Dead Time)
description: Find process gain, time constant and dead time of a first-order-plus-dead-time model from an open-loop step test using the 28.3% and 63.2% times.
category: engineering
{intro("An open-loop step test — change the controller output in manual and watch the process variable — is the standard way to model a process before tuning. This FOPDT step test calculator turns the step size and the times to reach 28.3% and 63.2% of the response into process gain, time constant and dead time — see [step-test and auto-tune methods in DCS PID controllers](ib:dcs-pid-auto-tune-step-test-relay-feedback-ziegler-nichols).")}
keywords: [fopdt calculator, step test calculator, process time constant calculator, dead time calculation, process gain calculation, two point method smith]
updated: {D}
variables:
  - {{ id: du, label: Controller output step, family: percent, unit: '%', default: 10 }}
  - {{ id: dy, label: Process variable change (% of span), family: percent, unit: '%', default: 20 }}
  - {{ id: t28, label: Time to 28.3% of the change, family: seconds, unit: s, default: 25, min: 0 }}
  - {{ id: t63, label: Time to 63.2% of the change, family: seconds, unit: s, default: 40, min: 0 }}
  - {{ id: K, label: Process gain (K), decimals: 3 }}
  - {{ id: tau, label: Time constant (τ), family: seconds, unit: s, min: 0 }}
  - {{ id: th, label: Dead time (θ), family: seconds, unit: s }}
  - {{ id: r, label: Controllability ratio (θ ÷ τ), min: 0, decimals: 3 }}
equations:
  - K = dy / du
  - tau = 1.5 * (t63 - t28)
  - th = t63 - tau
  - r = th / tau
faq:
  - q: How do I measure t28 and t63?
    a: Measure both times from the moment the output was stepped. Find the final change in PV, then read the times when the PV has moved 28.3% and 63.2% of that change.
  - q: What is the two-point method formula?
    a: Smith's method gives τ = 1.5 × (t63 − t28) and θ = t63 − τ. The process gain is the PV change divided by the output change, both in % of span.
  - q: What does the θ/τ ratio tell me?
    a: Below about 0.2 the loop is easy to control; above 1 it is dead-time dominant and needs slow, careful tuning or advanced control.
  - q: What if the dead time comes out negative?
    a: The response is not first order (for example, it overshoots or is integrating). Check the data, use a larger step, or fit the model by eye from the tangent at the steepest point.
related: [engineering/lambda-tuning, engineering/ziegler-nichols-pid-tuning, engineering/sensor-response-time, physics/rc-time-constant]
''', f'''
## How to use the FOPDT step test calculator

With the controller in **manual**, make a step in the output and record the PV until it settles. Enter the **output step**, the total **PV change** (both in % of span), and the times when the PV reached **28.3%** and **63.2%** of its final change. You get the process gain, time constant, dead time and the θ/τ ratio. Use the result in the [lambda tuning calculator](/engineering/lambda-tuning/).

## Two-point (Smith) method

<p class="formula">K = ΔPV ÷ ΔOP &nbsp;·&nbsp; τ = 1.5 (t<sub>63.2</sub> − t<sub>28.3</sub>) &nbsp;·&nbsp; θ = t<sub>63.2</sub> − τ</p>

The points come from the first-order response 1 − e<sup>−t/τ</sup>, which reaches 28.3% at τ/3 and 63.2% at τ after the dead time.

## Example

A 10% output step raises a temperature PV by 20% of span; the PV reaches 28.3% of its change at 25 s and 63.2% at 40 s:

- K = 20 ÷ 10 = **{f_K:g}**
- τ = 1.5 × (40 − 25) = **{f_tau:g} s**
- θ = 40 − 22.5 = **{f_th:g} s**
- θ/τ = **{f_th/f_tau:.3f}**

## First-order response reference

| Time after dead time | Response (% of final) |
|---|---|
''' + ''.join(f"| {lbl} | {(1-math.exp(-k))*100:.1f}% |\n" for lbl, k in (('τ/3', 1/3), ('τ/2', 0.5), ('τ', 1), ('2τ', 2), ('3τ', 3), ('4τ', 4), ('5τ', 5))) + '''
## Step test tips

- Make the step large enough to see clearly above noise (typically 5–10% output), but small enough to stay safe.
- Wait for the process to be steady before the step, and repeat in the opposite direction to check for non-linearity.
- Valve deadband and stiction add apparent dead time — check valve response separately.
''')

# ---------------------------------------------------------------- Sensor response time
st_tau, st_t, T0, Tf = 8, 10, 20, 100
st_fr = 1 - math.exp(-st_t / st_tau); st_T = T0 + (Tf - T0) * st_fr
page('engineering', 'sensor-response-time', f'''
title: Sensor Response Time Calculator (Time Constant, T63, T90)
description: Calculate T50, T63.2, T90 and T99 response times of a first-order sensor from its time constant, and the reading at any time after a step change.
category: engineering
{intro("Temperature sensors in thermowells, pressure transmitters with damping and many analysers respond like a first-order lag, reaching 63.2% of a step change in one time constant. This sensor response time calculator converts the time constant into T50, T90 and T99 and predicts the reading at any time — see [temperature sensor response time](ib:temperature-sensor-response-time) and [pressure transmitter damping and response time](ib:pressure-transmitter-damping-response-time).")}
keywords: [sensor response time calculator, time constant calculator, t90 response time, t63 time constant, thermocouple response time, first order lag calculator]
updated: {D}
variables:
  - {{ id: tau, label: Time constant (τ = T63.2), family: seconds, unit: s, default: 8, min: 0 }}
  - {{ id: t, label: Time after step change, family: seconds, unit: s, default: 10, min: 0 }}
  - {{ id: T0, label: Initial reading, family: temperature, unit: C, imperialUnit: F, default: 20 }}
  - {{ id: Tf, label: New process value, family: temperature, unit: C, imperialUnit: F, default: 100 }}
  - {{ id: T50, label: T50 response time, family: seconds, unit: s, min: 0 }}
  - {{ id: T90, label: T90 response time, family: seconds, unit: s, min: 0 }}
  - {{ id: T99, label: T99 response time, family: seconds, unit: s, min: 0 }}
  - {{ id: fr, label: Fraction of step reached at time t, family: percent, unit: '%', min: 0, max: 1, decimals: 2 }}
  - {{ id: Tr, label: Reading at time t, family: temperature, unit: C, imperialUnit: F }}
equations:
  - T50 = tau * ln(2)
  - T90 = tau * ln(10)
  - T99 = tau * ln(100)
  - fr = 1 - exp(-t / tau)
  - Tr = T0 + (Tf - T0) * fr
faq:
  - q: What is the time constant of a sensor?
    a: The time to reach 63.2% of a step change, assuming a first-order response. After 5 time constants the sensor has reached 99.3%.
  - q: How do I convert T90 to a time constant?
    a: For a first-order sensor, T90 = τ × ln 10 ≈ 2.303 τ, so τ = T90 ÷ 2.303. Enter T90 here and the time constant is solved for you.
  - q: Why is my thermowell sensor so slow?
    a: The thermowell wall, air gap and fluid velocity add thermal lag. A spring-loaded sensor tip, thermal paste and a thinner, shorter well all reduce the time constant.
  - q: Does transmitter damping add to the response time?
    a: Yes. Damping is a first-order filter with its own time constant; combined with the sensor, the total response is slower than either alone.
related: [engineering/fopdt-step-test, engineering/pt100-resistance, electronics/rl-time-constant, physics/rc-time-constant]
''', f'''
## How to use the sensor response time calculator

Enter the sensor's **time constant** (the T63.2 value from the datasheet) and a **time** after a step change. The calculator gives T50, T90 and T99 and the fraction of the step reached. Enter the **initial** and **new process value** to see what the sensor reads at that time. To work from a datasheet T90, clear the time constant and enter T90.

## First-order response formulas

<p class="formula">Reading(t) = T<sub>0</sub> + (T<sub>final</sub> − T<sub>0</sub>)(1 − e<sup>−t/τ</sup>)</p>

<p class="formula">T<sub>x</sub> = −τ × ln(1 − x) &nbsp;·&nbsp; T50 = 0.693 τ &nbsp;·&nbsp; T90 = 2.303 τ &nbsp;·&nbsp; T99 = 4.605 τ</p>

## Example

A Pt100 in a thermowell with τ = 8 s; the process jumps from 20 °C to 100 °C:

- T50 = **{st_tau*math.log(2):.2f} s**, T90 = **{st_tau*math.log(10):.2f} s**, T99 = **{st_tau*math.log(100):.2f} s**
- After 10 s: 1 − e<sup>−10/8</sup> = **{st_fr*100:.2f}%** of the step
- Reading = 20 + 80 × {st_fr:.4f} = **{st_T:.2f} °C**

## Response time multiples

| Time | Response (% of step) |
|---|---|
''' + ''.join(f"| {k} τ | {(1-math.exp(-k))*100:.1f}% |\n" for k in (0.5, 1, 2, 2.303, 3, 4, 4.605, 5)) + '''
## Typical time constants (in water, approximate)

| Sensor | Typical τ |
|---|---|
| Bare 0.5 mm mineral-insulated thermocouple | under 0.5 s |
| 6 mm sheathed Pt100 | 2–5 s |
| Pt100 in a drilled thermowell | 10–60 s |
| Pressure transmitter (no damping) | 0.1–0.3 s |

Response in air or gas is many times slower than in flowing liquid.
''')

# ---------------------------------------------------------------- Rotameter density correction
def rot(q1, r1, r2, rf): return q1 * math.sqrt((rf - r2) * r1 / ((rf - r1) * r2))
ro_cf = rot(1, 998, 800, 8000)
rtab = ''.join(f"| {nm} | {r2} kg/m³ | {rot(1, 998, r2, 8000):.3f} |\n" for nm, r2 in (('Petrol (gasoline)', 740), ('Ethanol', 789), ('Diesel', 832), ('Light oil', 900), ('Water (cal. fluid)', 998), ('Seawater', 1025), ('Glycol 50%', 1070), ('Sulphuric acid 98%', 1840)))
page('engineering', 'rotameter-correction', f'''
title: Rotameter Correction Calculator (Density Correction Factor)
description: Correct a rotameter (variable area flow meter) reading for a liquid of different density from the calibration fluid, using the float density.
category: engineering
{intro("A rotameter is calibrated for one fluid, usually water, and reads wrong when the liquid's density changes because the float settles at a different height. This rotameter correction calculator converts the scale reading to actual flow using the float density — see the [metal tube rotameter working principle](ib:metal-tube-rotameter-working) and [10 factors in rotameter selection](ib:rotameter-selection-10-factors).")}
keywords: [rotameter correction calculator, rotameter density correction, variable area flow meter correction factor, rotameter conversion factor, rotameter different liquid, float density correction]
updated: {D}
variables:
  - {{ id: Q1, label: Scale reading, family: flow, unit: Lmin, imperialUnit: gpm, default: 10, min: 0 }}
  - {{ id: r1, label: Calibration fluid density, family: density, unit: kgm3, default: 998, min: 0 }}
  - {{ id: r2, label: Actual fluid density, family: density, unit: kgm3, default: 800, min: 0 }}
  - {{ id: rf, label: Float density, family: density, unit: kgm3, default: 8000, min: 0, help: 'Stainless steel ≈ 8000, aluminium ≈ 2700, PVDF ≈ 1780 kg/m³.' }}
  - {{ id: CF, label: Correction factor, min: 0, decimals: 4 }}
  - {{ id: Q2, label: Actual volume flow, family: flow, unit: Lmin, imperialUnit: gpm, min: 0 }}
  - {{ id: M2, label: Actual mass flow, family: massflow, unit: kgh, min: 0 }}
equations:
  - CF = sqrt((rf - r2) * r1 / ((rf - r1) * r2))
  - Q2 = Q1 * CF
  - M2 = Q2 * r2
faq:
  - q: How do I correct a rotameter for a different liquid?
    a: Multiply the scale reading by √[(ρf − ρ2) ρ1 ÷ ((ρf − ρ1) ρ2)], where ρf is the float density, ρ1 the calibration fluid density and ρ2 the actual fluid density.
  - q: Does a lighter liquid read high or low?
    a: Low. A lighter liquid gives less buoyancy and drag, so the float sits lower; the actual flow is higher than the scale shows (correction factor above 1).
  - q: What about gas rotameters?
    a: Because the float is far denser than any gas, the correction simplifies to Q2 = Q1 × √(ρ1 ÷ ρ2), where density depends on gas, pressure and temperature.
  - q: Does viscosity matter?
    a: Yes, for viscous liquids. This correction assumes viscosity close to the calibration fluid; above a few cP the manufacturer's viscosity immunity ceiling should be checked.
related: [engineering/gas-flow-correction, engineering/flow-meter-k-factor, engineering/turndown-ratio, physics/density]
''', f'''
## How to use the rotameter correction calculator

Enter the **scale reading**, the **density of the calibration fluid** (998 kg/m³ for water at 20 °C), the **density of the liquid you are measuring** and the **float density**. You get the correction factor, the actual volume flow and the mass flow. Enter a desired actual flow and clear the scale reading to find what the scale should show.

## Rotameter density correction formula

<p class="formula">Q<sub>actual</sub> = Q<sub>scale</sub> × √[ (ρ<sub>f</sub> − ρ<sub>2</sub>) ρ<sub>1</sub> ÷ ((ρ<sub>f</sub> − ρ<sub>1</sub>) ρ<sub>2</sub>) ]</p>

## Example

A water-calibrated rotameter with a stainless-steel float (8000 kg/m³) reads 10 L/min on a liquid of 800 kg/m³:

- CF = √[(8000 − 800) × 998 ÷ ((8000 − 998) × 800)] = **{ro_cf:.4f}**
- Actual flow = 10 × {ro_cf:.4f} = **{10*ro_cf:.2f} L/min**
- Mass flow = **{10*ro_cf*0.8*60:.0f} kg/h**

## Correction factors for a water-calibrated meter (stainless float)

| Liquid | Density | Correction factor |
|---|---|---|
{rtab}
Densities are typical values at about 20 °C; use your actual fluid density.

## Notes

- Correction assumes the same float and tube and a viscosity close to the calibration fluid.
- For large density differences it is better to order the meter scaled for the actual fluid.
''')

# ---------------------------------------------------------------- Vortex shedding frequency
vs_f = 0.2 * 3 / 0.02; vs_Q = 3 * math.pi * 0.1**2 / 4; vs_K = vs_f / (vs_Q * 1000)
vtab = ''.join(f"| {v:g} m/s | " + ' | '.join(f"{0.2*v/(d/1000):.1f} Hz" for d in (10, 20, 40)) + ' |\n' for v in (0.3, 1, 3, 5, 10, 30))
page('engineering', 'vortex-shedding-frequency', f'''
title: Vortex Shedding Frequency Calculator (Strouhal Number)
description: Calculate vortex shedding frequency from flow velocity, bluff body or cylinder width and Strouhal number — for vortex flow meters and thermowells.
category: engineering
{intro("Fluid flowing past a bluff body sheds vortices alternately from each side at a frequency proportional to velocity — the principle of the vortex flow meter and the cause of thermowell vibration. This vortex shedding frequency calculator uses the Strouhal relation f = St·V/d — see [how a vortex shedding flowmeter works](ib:vortex-shedding-flowmeter-working) and [vortex flow meter troubleshooting](ib:vortex-flow-meter-troubleshooting).")}
keywords: [vortex shedding frequency calculator, strouhal number calculator, vortex flow meter frequency, karman vortex frequency, bluff body shedding frequency, thermowell vortex shedding]
updated: {D}
variables:
  - {{ id: V, label: Flow velocity, family: velocity, unit: ms, imperialUnit: fts, default: 3, min: 0 }}
  - {{ id: d, label: Bluff body / cylinder width, family: length, unit: mm, imperialUnit: in, default: 20, min: 0 }}
  - {{ id: St, label: Strouhal number, default: 0.2, min: 0, help: 'About 0.2 for a circular cylinder over a wide Reynolds range (300 – 200,000).' }}
  - {{ id: D, label: Pipe internal diameter, family: length, unit: mm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: f, label: Shedding frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: Q, label: Volume flow, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: Kf, label: Pulses per litre (K-factor), min: 0, decimals: 4 }}
equations:
  - f = St * V / d
  - Q = V * pi * D^2 / 4
  - Kf = f / (Q * 1000)
faq:
  - q: What is the vortex shedding frequency formula?
    a: f = St × V ÷ d, where St is the Strouhal number (about 0.2 for cylinders), V the velocity and d the width of the body facing the flow.
  - q: Why is the vortex meter linear?
    a: Over a wide Reynolds number range the Strouhal number is nearly constant, so the frequency is proportional to velocity and therefore to volume flow.
  - q: Why does vortex shedding matter for thermowells?
    a: If the shedding frequency approaches the thermowell's natural frequency the well resonates and can break by fatigue. ASME PTC 19.3 TW requires checking this frequency ratio.
  - q: Is the calculated K-factor exact for my meter?
    a: No. The bluff body partly blocks the pipe, raising local velocity, and real meters are flow-calibrated. Use the meter's stamped K-factor for measurement.
related: [engineering/flow-meter-k-factor, engineering/pipe-flow-velocity, engineering/reynolds-number, engineering/turndown-ratio]
''', f'''
## How to use the vortex shedding frequency calculator

Enter the **flow velocity**, the **width** of the bluff body (or the diameter of a cylinder such as a thermowell) and the **Strouhal number**. You get the shedding frequency. Add the **pipe internal diameter** to see the volume flow and an approximate K-factor in pulses per litre.

## Vortex shedding formula

<p class="formula">f = St × V ÷ d</p>

<p class="formula">Q = V × π D² ÷ 4 &nbsp;·&nbsp; K = f ÷ Q</p>

## Example

Water at 3 m/s past a 20 mm bluff body (St = 0.2) in a 100 mm pipe:

- f = 0.2 × 3 ÷ 0.020 = **{vs_f:g} Hz**
- Q = 3 × π × 0.1² ÷ 4 = **{vs_Q*3600:.2f} m³/h**
- K ≈ 30 ÷ {vs_Q*1000:.2f} L/s = **{vs_K:.3f} pulses per litre**

## Shedding frequency for St = 0.2

| Velocity | d = 10 mm | d = 20 mm | d = 40 mm |
|---|---|---|---|
{vtab}
## Practical notes

- Vortex meters need a minimum Reynolds number (typically about 10,000–20,000) to shed regularly — below that they cut off.
- Typical sizing velocities: liquids 0.3–7 m/s, gases and steam about 2–80 m/s.
- Pipe vibration at frequencies near the shedding frequency can cause false counts; see the [K-factor calculator](/engineering/flow-meter-k-factor/) for pulse-to-flow scaling.
''')

# ---------------------------------------------------------------- Manning
def man(nm, b, y, S):
    A = b * y; P = b + 2 * y; R = A / P; V = (1 / nm) * R ** (2 / 3) * S ** 0.5; return A, P, R, V, V * A
mA, mP, mR, mV, mQ = man(0.013, 2, 0.5, 0.001)
mtab = ''.join(f"| {y:g} m | {man(0.013,2,y,0.001)[3]:.3f} m/s | {man(0.013,2,y,0.001)[4]:.3f} m³/s |\n" for y in (0.1, 0.25, 0.5, 0.75, 1.0, 1.5))
page('engineering', 'manning-equation', f'''
title: Manning Equation Calculator (Open Channel Flow)
description: Calculate open channel velocity and flow with the Manning equation for a rectangular channel from width, depth, slope and roughness n.
category: engineering
{intro("The Manning equation is the standard formula for uniform flow in open channels, ditches and part-full gravity drains, relating velocity to roughness, hydraulic radius and slope. This Manning equation calculator works in SI units for a rectangular channel — see [open channel flow measurement](ib:open-channel-flow-measurement) and the [Parshall flume](ib:parshall-flume-open-channel-flow).")}
keywords: [manning equation calculator, open channel flow calculator, manning formula, hydraulic radius calculator, channel flow rate, manning n values]
updated: {D}
variables:
  - {{ id: nm, label: Manning roughness (n), default: 0.013, min: 0, decimals: 4 }}
  - {{ id: b, label: Channel bottom width, family: length, unit: m, imperialUnit: ft, default: 2, min: 0 }}
  - {{ id: y, label: Flow depth, family: length, unit: m, imperialUnit: ft, default: 0.5, min: 0 }}
  - {{ id: S, label: Channel slope, family: percent, unit: '%', default: 0.1, min: 0, decimals: 4, help: 'Fall per length: 0.1% = 1 m per 1000 m.' }}
  - {{ id: A, label: Flow area, family: area, unit: m2, imperialUnit: ft2, min: 0 }}
  - {{ id: P, label: Wetted perimeter, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: R, label: Hydraulic radius, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: V, label: Mean velocity, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: Q, label: Flow rate, family: flow, unit: m3s, imperialUnit: cfm, min: 0 }}
equations:
  - A = b * y
  - P = b + 2 * y
  - R = A / P
  - V = (1 / nm) * R^(2/3) * sqrt(S)
  - Q = V * A
faq:
  - q: What is the Manning equation?
    a: In SI units V = (1/n) R^(2/3) S^(1/2), where V is mean velocity in m/s, R the hydraulic radius in m, S the slope and n the roughness coefficient. Flow Q = V × A.
  - q: What is the hydraulic radius?
    a: Flow area divided by wetted perimeter. For a rectangular channel of width b and depth y, R = b·y ÷ (b + 2y).
  - q: How do I use Manning in US units?
    a: The US form includes a factor 1.486, V = (1.486/n) R^(2/3) S^(1/2) with feet. This calculator works internally in SI, so you can switch display units freely.
  - q: Can I find the normal depth for a given flow?
    a: Yes. Clear the depth, enter the flow rate and calculate — the depth is solved numerically.
related: [engineering/weir-flow, engineering/hazen-williams, engineering/darcy-weisbach-head-loss, engineering/pipe-flow-velocity]
''', f'''
## How to use the Manning equation calculator

Enter the **roughness coefficient n**, the channel **bottom width**, the **flow depth** and the **slope**. You get the flow area, wetted perimeter, hydraulic radius, mean velocity and flow rate. To find the normal depth for a known flow, clear the depth and enter the flow.

## Manning equation (SI)

<p class="formula">V = (1/n) × R<sup>2/3</sup> × S<sup>1/2</sup> &nbsp;·&nbsp; Q = V × A</p>

<p class="formula">Rectangular channel: A = b·y &nbsp;·&nbsp; P = b + 2y &nbsp;·&nbsp; R = A ÷ P</p>

## Example

Concrete channel (n = 0.013), 2 m wide, 0.5 m deep, slope 0.1%:

- A = **{mA:g} m²**, P = **{mP:g} m**, R = **{mR:.4f} m**
- V = (1/0.013) × {mR:.4f}<sup>2/3</sup> × √0.001 = **{mV:.3f} m/s**
- Q = {mV:.3f} × 1 = **{mQ:.3f} m³/s** ({mQ*3600:,.0f} m³/h)

## Flow vs depth (same channel)

| Depth | Velocity | Flow |
|---|---|---|
{mtab}
## Typical Manning n values

| Surface | n |
|---|---|
| PVC / HDPE pipe | 0.009–0.011 |
| Finished concrete | 0.012–0.014 |
| Unfinished concrete | 0.014–0.017 |
| Corrugated metal | 0.022–0.026 |
| Earth channel, clean | 0.018–0.025 |
| Natural stream, some weeds and stones | 0.030–0.040 |

## Notes

- Manning assumes steady, uniform, fully turbulent flow; it is not valid near weirs, gates or sudden changes.
- For flow measurement, use a calibrated structure such as a weir or flume — see the [weir flow calculator](/engineering/weir-flow/).
''')

# ---------------------------------------------------------------- Hazen-Williams
def hw(Q, d, L, C): return 10.67 * L * Q ** 1.852 / (C ** 1.852 * d ** 4.8704)
hQ = 50 / 3600; hh = hw(hQ, 0.1, 100, 130); hv = hQ / (math.pi * 0.01 / 4)
htab = ''.join(f"| {d} mm | {hQ/(math.pi*(d/1000)**2/4):.2f} m/s | {hw(hQ, d/1000, 100, 130):.3f} m | {hw(hQ, d/1000, 100, 130)*9.80665:.2f} kPa |\n" for d in (65, 80, 100, 125, 150, 200))
page('engineering', 'hazen-williams', f'''
title: Hazen–Williams Calculator (Water Pipe Head Loss)
description: Calculate friction head loss and pressure drop in water pipes with the Hazen–Williams equation from flow, pipe diameter, length and C factor.
category: engineering
{intro("The Hazen–Williams equation is the go-to empirical formula for friction loss in water supply, fire-protection and irrigation pipes, using a single roughness C factor. This Hazen–Williams calculator gives head loss, pressure drop and velocity in SI units — see [how to calculate pressure drop in pipes](ib:calculate-pressure-drop-in-pipes).")}
keywords: [hazen williams calculator, hazen williams equation, water pipe head loss calculator, pipe friction loss calculator, c factor pipe, pressure drop water pipe]
updated: {D}
variables:
  - {{ id: Q, label: Flow rate, family: flow, unit: m3h, imperialUnit: gpm, default: 50, min: 0 }}
  - {{ id: d, label: Pipe internal diameter, family: length, unit: mm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: L, label: Pipe length, family: length, unit: m, imperialUnit: ft, default: 100, min: 0 }}
  - {{ id: C, label: Hazen–Williams C factor, default: 130, min: 1, help: 'PVC/HDPE 150, copper 130–140, new steel 120–140, old cast iron 80–100.' }}
  - {{ id: hf, label: Head loss, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: dp, label: Pressure drop (water), family: pressure, unit: kPa, imperialUnit: psi, min: 0 }}
  - {{ id: V, label: Velocity, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
equations:
  - hf = 10.67 * L * Q^1.852 / (C^1.852 * d^4.8704)
  - dp = 9806.65 * hf
  - V = Q / (pi * d^2 / 4)
faq:
  - q: What is the Hazen–Williams formula in SI units?
    a: h_f = 10.67 × L × Q^1.852 ÷ (C^1.852 × d^4.87), with head loss and length in metres, flow in m³/s and diameter in metres.
  - q: When should I not use Hazen–Williams?
    a: It is valid only for water at roughly 5–25 °C in turbulent flow. For other liquids, hot water, viscous fluids or gases, use the Darcy–Weisbach equation.
  - q: What C factor should I use?
    a: About 150 for plastic pipe, 130–140 for copper and new lined pipe, 120 for new steel and 100 or less for old, tuberculated cast iron. Design codes often specify the value.
  - q: How does pipe size affect head loss?
    a: Strongly — head loss varies with d^−4.87, so one size larger pipe often cuts friction loss by more than half.
related: [engineering/darcy-weisbach-head-loss, engineering/minor-losses, engineering/pipe-flow-velocity, engineering/pump-power]
''', f'''
## How to use the Hazen–Williams calculator

Enter the **flow rate**, the pipe **internal diameter**, its **length** and the **C factor** for the pipe material. You get the friction head loss, the equivalent pressure drop for water and the flow velocity. Add fittings with the [minor losses calculator](/engineering/minor-losses/).

## Hazen–Williams equation (SI)

<p class="formula">h<sub>f</sub> = 10.67 × L × Q<sup>1.852</sup> ÷ (C<sup>1.852</sup> × d<sup>4.87</sup>)</p>

<p class="formula">Δp = ρ g h<sub>f</sub> ≈ 9.81 kPa per metre of head</p>

## Example

50 m³/h of water through 100 m of 100 mm pipe, C = 130:

- Q = 50 ÷ 3600 = 0.01389 m³/s
- h<sub>f</sub> = **{hh:.3f} m** of head
- Δp = **{hh*9.80665:.2f} kPa** ({hh*9.80665/6.894757:.2f} psi)
- Velocity = **{hv:.2f} m/s**

## Head loss per 100 m at 50 m³/h (C = 130)

| Pipe ID | Velocity | Head loss | Pressure drop |
|---|---|---|---|
{htab}
## Typical C factors

| Pipe material | C |
|---|---|
| PVC, HDPE, copper (smooth) | 140–150 |
| Cement-lined ductile iron | 130–140 |
| New welded steel | 120 |
| Galvanised steel | 120 |
| Old cast iron | 80–100 |
''')

# ---------------------------------------------------------------- Minor losses
mk, mv, mrho, mf, mD = 0.9, 2, 998, 0.02, 0.05
mh = mk * mv**2 / (2 * G); mdp = mrho * G * mh; mle = mk * mD / mf
fitt = [('Gate valve, fully open', 0.15), ('Ball valve, fully open', 0.05), ('Globe valve, fully open', 10), ('Swing check valve', 2.0), ('Butterfly valve, fully open', 0.5),
        ('90° elbow, standard', 0.75), ('90° elbow, long radius', 0.45), ('45° elbow', 0.4), ('Tee, flow through run', 0.4), ('Tee, flow through branch', 1.0),
        ('Pipe entrance, sharp-edged', 0.5), ('Pipe exit into tank', 1.0)]
ftab = ''.join(f"| {nm} | {k:g} | {k*4/(2*G)*1000:.0f} mm | {k*0.05/0.02:.2f} m |\n" for nm, k in fitt)
page('engineering', 'minor-losses', f'''
title: Minor Losses Calculator (Fitting K Factors & Equivalent Length)
description: Calculate pressure loss through pipe fittings and valves from K factors and velocity, plus the equivalent pipe length — with a table of typical K values.
category: engineering
{intro("Valves, elbows, tees, entrances and exits each add a pressure loss proportional to velocity head, described by a resistance coefficient K. This minor losses calculator adds them up, converts the loss to pressure and gives the equivalent straight-pipe length — see [how to calculate pressure drop in pipes](ib:calculate-pressure-drop-in-pipes).")}
keywords: [minor losses calculator, pipe fitting loss calculator, k factor pressure drop, equivalent length calculator, valve pressure loss, fittings head loss]
updated: {D}
variables:
  - {{ id: K, label: Total K (sum of all fittings), default: 0.9, min: 0, help: 'Add the K values of every fitting — see the table below.' }}
  - {{ id: V, label: Flow velocity, family: velocity, unit: ms, imperialUnit: fts, default: 2, min: 0 }}
  - {{ id: rho, label: Fluid density, family: density, unit: kgm3, default: 998, min: 0 }}
  - {{ id: f, label: Darcy friction factor (for equivalent length), default: 0.02, min: 0 }}
  - {{ id: D, label: Pipe internal diameter, family: length, unit: mm, imperialUnit: in, default: 50, min: 0 }}
  - {{ id: hL, label: Head loss, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: dp, label: Pressure loss, family: pressure, unit: kPa, imperialUnit: psi, min: 0 }}
  - {{ id: Le, label: Equivalent pipe length, family: length, unit: m, imperialUnit: ft, min: 0 }}
equations:
  - hL = K * V^2 / (2 * g0)
  - dp = rho * g0 * hL
  - Le = K * D / f
faq:
  - q: How do I calculate minor losses in a pipe?
    a: Head loss = K × V² ÷ 2g, where K is the sum of all fitting coefficients and V the velocity in the pipe. Multiply by ρg for pressure loss.
  - q: What is equivalent length?
    a: The length of straight pipe that would give the same loss as the fittings, L_e = K × D ÷ f. Adding it to the real pipe length lets you use one Darcy–Weisbach calculation.
  - q: Are minor losses really minor?
    a: Not always. In short pipe runs with many valves and fittings — pump suction lines, skids, plant rooms — fitting losses can exceed straight-pipe friction.
  - q: Where do K values come from?
    a: From manufacturer data (often given as Cv or Kv for valves) or published tables such as Crane TP-410. Values vary with size and design, so tables give typical figures.
related: [engineering/darcy-weisbach-head-loss, engineering/hazen-williams, engineering/control-valve-kv-cv, engineering/pipe-flow-velocity]
''', f'''
## How to use the minor losses calculator

Add up the **K factors** of every valve and fitting in the line and enter the total, with the **velocity** in the pipe and the **fluid density**. You get the head loss and pressure loss. Enter the **Darcy friction factor** and **pipe diameter** to see the equivalent straight-pipe length (find f from the [Darcy–Weisbach calculator](/engineering/darcy-weisbach-head-loss/)).

## Minor loss formulas

<p class="formula">h<sub>L</sub> = K × V² ÷ 2g &nbsp;·&nbsp; Δp = ρ g h<sub>L</sub> = K × ½ρV²</p>

<p class="formula">L<sub>e</sub> = K × D ÷ f</p>

## Example

A 50 mm water line at 2 m/s with total K = 0.9 (for example one standard elbow plus a gate valve), f = 0.02:

- h<sub>L</sub> = 0.9 × 2² ÷ (2 × 9.807) = **{mh:.4f} m**
- Δp = 998 × 9.807 × {mh:.4f} = **{mdp/1000:.3f} kPa**
- L<sub>e</sub> = 0.9 × 0.05 ÷ 0.02 = **{mle:.2f} m** of straight pipe

## Typical K values (fully turbulent flow)

Head loss at 2 m/s and equivalent length in 50 mm pipe with f = 0.02:

| Fitting | K | Head loss | L<sub>e</sub> |
|---|---|---|---|
{ftab}
K values are typical; they depend on size, design and manufacturer.

## Valve K from Cv or Kv

For a valve with flow coefficient Kv (m³/h at 1 bar) and pipe diameter d in mm, K ≈ 0.0016 × d⁴ ÷ Kv². See the [control valve Kv/Cv calculator](/engineering/control-valve-kv-cv/).
''')

# ================================================================ PHYSICS
page('physics', 'impulse', f'''
title: Impulse Calculator (Impulse–Momentum Theorem)
description: Calculate impulse from force and time, and the resulting change in velocity or momentum — J = F·Δt = m·Δv — with worked examples.
category: physics
intro: "Impulse is the product of force and the time it acts, and it equals the change in an object's momentum. This impulse calculator applies the impulse–momentum theorem to find impulse, change in velocity, force or contact time — useful for collisions, kicks, airbags and rocket burns."
keywords: [impulse calculator, impulse momentum theorem, impulse formula, change in momentum calculator, force time calculator, impulse physics]
updated: {D}
variables:
  - {{ id: F, label: Average force, family: force, unit: N, imperialUnit: lbf, default: 500 }}
  - {{ id: t, label: Contact time, family: seconds, unit: s, default: 0.1, min: 0 }}
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 2, min: 0 }}
  - {{ id: J, label: Impulse (= change in momentum), suffix: N·s }}
  - {{ id: dv, label: Change in velocity, family: velocity, unit: ms, imperialUnit: fts }}
equations:
  - J = F * t
  - dv = J / m
faq:
  - q: What is the formula for impulse?
    a: J = F × Δt, the average force multiplied by the time it acts. By the impulse–momentum theorem it also equals m × Δv.
  - q: What are the units of impulse?
    a: Newton-seconds (N·s), which are the same as kg·m/s — the units of momentum.
  - q: Why do airbags and crumple zones reduce injury?
    a: The change in momentum in a crash is fixed, so stretching the stopping time lowers the average force by the same factor.
  - q: How do I find the force from a change in velocity?
    a: Enter the mass, the change in velocity and the contact time, and clear the force — F = m × Δv ÷ Δt.
related: [physics/momentum, physics/force, physics/elastic-collision, physics/acceleration]
''', '''
## How to use the impulse calculator

Enter the **average force**, the **contact time** and the **mass** of the object. You get the impulse and the change in velocity it produces. Any field can be the unknown: enter mass, change in velocity and time to find the average force.

## Impulse formula

<p class="formula">J = F × Δt = m × Δv = Δp</p>

## Example

A 500 N average force acts on a 2 kg ball for 0.1 s:

- J = 500 × 0.1 = **50 N·s**
- Δv = 50 ÷ 2 = **25 m/s**

## Same impulse, different stopping times

Stopping a 70 kg person moving at 15 m/s (Δp = 1,050 N·s):

| Stopping time | Average force |
|---|---|
''' + ''.join(f"| {t:g} s | {1050/t:,.0f} N ({1050/t/(70*G):.1f} g) |\n" for t in (0.01, 0.05, 0.1, 0.2, 0.5)) + '''
## Notes

- Impulse and momentum are **vectors** — a ball that bounces back has a change in velocity of up to twice its speed.
- For a force that varies with time, impulse is the area under the force–time graph.
''')

c1 = ((2-1)*3 + 2*1*(-1))/3; c2 = ((1-2)*(-1) + 2*2*3)/3; ci = (2*3 + 1*(-1))/3; ke0 = 0.5*2*9 + 0.5*1*1; kel = ke0 - 0.5*3*ci**2
page('physics', 'elastic-collision', f'''
title: Elastic & Inelastic Collision Calculator (1D)
description: Calculate final velocities after a one-dimensional elastic or perfectly inelastic collision from masses and initial velocities, plus kinetic energy lost.
category: physics
intro: "In every collision momentum is conserved; in an elastic collision kinetic energy is conserved too, while in a perfectly inelastic one the objects stick together. This elastic collision calculator gives the final velocities for both cases in one dimension and the kinetic energy lost when the bodies stick."
keywords: [elastic collision calculator, inelastic collision calculator, collision final velocity, conservation of momentum calculator, perfectly inelastic collision, 1d collision physics]
updated: {D}
variables:
  - {{ id: m1, label: Mass 1, family: mass, unit: kg, imperialUnit: lb, default: 2, min: 0 }}
  - {{ id: u1, label: Initial velocity 1, family: velocity, unit: ms, imperialUnit: fts, default: 3 }}
  - {{ id: m2, label: Mass 2, family: mass, unit: kg, imperialUnit: lb, default: 1, min: 0 }}
  - {{ id: u2, label: Initial velocity 2 (negative = opposite direction), family: velocity, unit: ms, imperialUnit: fts, default: -1 }}
  - {{ id: v1, label: Elastic — final velocity 1, family: velocity, unit: ms, imperialUnit: fts }}
  - {{ id: v2, label: Elastic — final velocity 2, family: velocity, unit: ms, imperialUnit: fts }}
  - {{ id: vc, label: Perfectly inelastic — common velocity, family: velocity, unit: ms, imperialUnit: fts }}
  - {{ id: dKE, label: Kinetic energy lost (inelastic), family: energy, unit: J, min: 0 }}
equations:
  - v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)
  - v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)
  - vc = (m1 * u1 + m2 * u2) / (m1 + m2)
  - dKE = 0.5 * m1 * u1^2 + 0.5 * m2 * u2^2 - 0.5 * (m1 + m2) * vc^2
faq:
  - q: What is the formula for an elastic collision?
    a: v1 = [(m1 − m2) u1 + 2 m2 u2] ÷ (m1 + m2) and v2 = [(m2 − m1) u2 + 2 m1 u1] ÷ (m1 + m2). Both momentum and kinetic energy are conserved.
  - q: What happens in a perfectly inelastic collision?
    a: The bodies stick together and move at v = (m1 u1 + m2 u2) ÷ (m1 + m2). Momentum is conserved but the maximum possible kinetic energy is lost to heat, sound and deformation.
  - q: How do I enter objects moving towards each other?
    a: Choose one direction as positive and give the other object a negative velocity, as in the default example.
  - q: What happens when equal masses collide elastically?
    a: They exchange velocities — the moving one stops and the stationary one moves off at the original speed, like billiard balls or Newton's cradle.
related: [physics/momentum, physics/impulse, physics/kinetic-energy, physics/speed-distance-time]
''', f'''
## How to use the elastic collision calculator

Enter the two **masses** and their **initial velocities** along the same line, using a negative sign for motion in the opposite direction. You get the final velocities if the collision is perfectly elastic, the common velocity if the objects stick together, and the kinetic energy lost in that inelastic case. Real collisions lie between the two.

## Collision formulas

<p class="formula">Momentum: m<sub>1</sub>u<sub>1</sub> + m<sub>2</sub>u<sub>2</sub> = m<sub>1</sub>v<sub>1</sub> + m<sub>2</sub>v<sub>2</sub></p>

<p class="formula">Elastic: v<sub>1</sub> = [(m<sub>1</sub> − m<sub>2</sub>)u<sub>1</sub> + 2m<sub>2</sub>u<sub>2</sub>] ÷ (m<sub>1</sub> + m<sub>2</sub>) &nbsp;·&nbsp; v<sub>2</sub> = [(m<sub>2</sub> − m<sub>1</sub>)u<sub>2</sub> + 2m<sub>1</sub>u<sub>1</sub>] ÷ (m<sub>1</sub> + m<sub>2</sub>)</p>

<p class="formula">Perfectly inelastic: v = (m<sub>1</sub>u<sub>1</sub> + m<sub>2</sub>u<sub>2</sub>) ÷ (m<sub>1</sub> + m<sub>2</sub>)</p>

## Example

A 2 kg cart at 3 m/s meets a 1 kg cart moving at −1 m/s (towards it):

- Total momentum = 2 × 3 + 1 × (−1) = **5 kg·m/s**
- Elastic: v<sub>1</sub> = (1 × 3 − 2) ÷ 3 = **{c1:.3f} m/s**, v<sub>2</sub> = (1 + 12) ÷ 3 = **{c2:.3f} m/s**
- Stuck together: v = 5 ÷ 3 = **{ci:.3f} m/s**
- Kinetic energy before = {ke0:g} J; after sticking = {0.5*3*ci**2:.3f} J → **{kel:.3f} J lost**

## Coefficient of restitution

Real collisions are described by e = (v<sub>2</sub> − v<sub>1</sub>) ÷ (u<sub>1</sub> − u<sub>2</sub>): e = 1 for elastic, e = 0 for perfectly inelastic. Typical values: steel ball on steel about 0.6–0.9, basketball about 0.75–0.85, clay about 0.
''')

page('physics', 'friction-force', f'''
title: Friction Force Calculator (Coefficient of Friction)
description: Calculate friction force from the coefficient of friction and normal force or mass, or find the coefficient — with a table of static and kinetic values.
category: physics
intro: "Friction opposes sliding between two surfaces and is proportional to how hard they are pressed together. This friction force calculator uses F = μN to find the friction force, the normal force or the coefficient of friction, for an object resting on a level surface or any known normal force."
keywords: [friction force calculator, coefficient of friction calculator, static friction calculator, kinetic friction formula, normal force friction, friction coefficient table]
updated: {D}
variables:
  - {{ id: mu, label: Coefficient of friction (μ), default: 0.4, min: 0 }}
  - {{ id: m, label: Mass (on a level surface), family: mass, unit: kg, imperialUnit: lb, default: 10, min: 0 }}
  - {{ id: N, label: Normal force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: Ff, label: Friction force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
equations:
  - N = m * g0
  - Ff = mu * N
faq:
  - q: What is the formula for friction force?
    a: F = μ × N, where μ is the coefficient of friction and N the normal force pressing the surfaces together. On a level surface N = m × g.
  - q: What is the difference between static and kinetic friction?
    a: Static friction is the maximum force before an object starts to slide; kinetic friction acts while it is sliding and is usually lower. That is why it takes more force to start pushing a box than to keep it moving.
  - q: Does friction depend on contact area?
    a: For dry, rigid surfaces, no — the classical (Amontons) law says friction depends only on μ and the normal force. Tyres and soft materials deviate from this.
  - q: How do I find the coefficient of friction?
    a: Measure the force needed to slide the object and its normal force, enter both and clear μ — μ = F ÷ N.
related: [physics/inclined-plane, physics/force, physics/weight, physics/work-and-power]
''', '''
## How to use the friction force calculator

Enter the **coefficient of friction** and the **mass** of an object on a level surface — the normal force N = mg is calculated for you — and you get the friction force. For a sloped surface or an extra pressing force, clear the mass and enter the **normal force** directly, or use the [inclined plane calculator](/physics/inclined-plane/).

## Friction formula

<p class="formula">F<sub>f</sub> = μ × N &nbsp;·&nbsp; N = m × g (level surface)</p>

## Example

A 10 kg crate on a floor with μ = 0.4:

- N = 10 × 9.807 = **98.07 N**
- F<sub>f</sub> = 0.4 × 98.07 = **''' + f"{0.4*10*G:.2f}" + ''' N** — the force needed to keep it sliding

## Typical coefficients of friction (dry, approximate)

| Surfaces | Static μ<sub>s</sub> | Kinetic μ<sub>k</sub> |
|---|---|---|
| Steel on steel | 0.74 | 0.57 |
| Aluminium on steel | 0.61 | 0.47 |
| Copper on steel | 0.53 | 0.36 |
| Rubber on dry concrete | 1.0 | 0.8 |
| Wood on wood | 0.25–0.5 | 0.2 |
| Glass on glass | 0.94 | 0.4 |
| Waxed ski on snow | 0.14 | 0.1 |
| PTFE on PTFE | 0.04 | 0.04 |
| Ice on ice | 0.1 | 0.03 |

Values vary widely with surface finish, contamination and lubrication — use measured values for design.
''')

ip_t = math.radians(30); ip_par = 10*G*math.sin(ip_t); ip_N = 10*G*math.cos(ip_t); ip_a = G*(math.sin(ip_t) - 0.2*math.cos(ip_t)); ip_up = 10*G*(math.sin(ip_t) + 0.2*math.cos(ip_t))
iptab = ''.join(f"| {a}° | {G*math.sin(math.radians(a)):.3f} | {G*(math.sin(math.radians(a))-0.2*math.cos(math.radians(a))):.3f} |\n" for a in (5, 10, 15, 20, 30, 45, 60))
page('physics', 'inclined-plane', f'''
title: Inclined Plane Calculator (Forces, Friction & Acceleration)
description: Calculate the forces on an inclined plane — parallel and normal components, friction, acceleration down the slope and the push needed to move up.
category: physics
intro: "On a slope, gravity splits into a component pulling the object down the incline and a component pressing it into the surface, which sets the friction. This inclined plane calculator resolves those forces and gives the acceleration of a sliding object and the force needed to push it up at steady speed."
keywords: [inclined plane calculator, incline force calculator, ramp force calculator, acceleration down incline, friction on inclined plane, force parallel to incline]
updated: {D}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 10, min: 0 }}
  - {{ id: th, label: Angle of incline, family: angle, unit: deg, default: 30, min: 0 }}
  - {{ id: mu, label: Coefficient of kinetic friction (μ), default: 0.2, min: 0 }}
  - {{ id: Fp, label: Force parallel to slope (m g sin θ), family: force, unit: N, imperialUnit: lbf }}
  - {{ id: N, label: Normal force (m g cos θ), family: force, unit: N, imperialUnit: lbf }}
  - {{ id: Ff, label: Friction force, family: force, unit: N, imperialUnit: lbf }}
  - {{ id: a, label: Acceleration down the slope, suffix: m/s² }}
  - {{ id: Fu, label: Force to push up at constant speed, family: force, unit: N, imperialUnit: lbf }}
equations:
  - Fp = m * g0 * sin(th)
  - N = m * g0 * cos(th)
  - Ff = mu * N
  - a = g0 * (sin(th) - mu * cos(th))
  - Fu = m * g0 * (sin(th) + mu * cos(th))
faq:
  - q: What is the acceleration down an inclined plane?
    a: a = g (sin θ − μ cos θ). Without friction it is simply g sin θ — about 4.9 m/s² on a 30° slope.
  - q: What does a negative acceleration mean?
    a: Friction is larger than the pull down the slope, so a block at rest will not start sliding (if μ is the static coefficient) and a sliding block slows down.
  - q: At what angle will an object start to slide?
    a: When tan θ exceeds the static coefficient of friction — the angle of repose θ = arctan μs. For μs = 0.5 that is about 26.6°.
  - q: How much force is needed to push a load up a ramp?
    a: F = m g (sin θ + μ cos θ) at steady speed, ignoring acceleration. A shallower ramp needs less force but a longer distance.
related: [physics/friction-force, physics/force, physics/weight, physics/acceleration]
''', f'''
## How to use the inclined plane calculator

Enter the **mass**, the **angle** of the slope and the **coefficient of friction** (use 0 for a frictionless slope). You get the gravity component along the slope, the normal force, the friction force, the acceleration of a sliding object and the force needed to push it up the slope at constant speed.

## Inclined plane formulas

<p class="formula">F<sub>∥</sub> = m g sin θ &nbsp;·&nbsp; N = m g cos θ &nbsp;·&nbsp; F<sub>f</sub> = μ N</p>

<p class="formula">a = g (sin θ − μ cos θ) &nbsp;·&nbsp; F<sub>up</sub> = m g (sin θ + μ cos θ)</p>

## Example

A 10 kg block on a 30° slope with μ = 0.2:

- F<sub>∥</sub> = 10 × 9.807 × 0.5 = **{ip_par:.2f} N**
- N = 10 × 9.807 × 0.866 = **{ip_N:.2f} N**, friction = **{0.2*ip_N:.2f} N**
- a = 9.807 × (0.5 − 0.2 × 0.866) = **{ip_a:.3f} m/s²** down the slope
- Push up at constant speed = **{ip_up:.2f} N**

## Acceleration by angle (m/s²)

| Angle | No friction | μ = 0.2 |
|---|---|---|
{iptab}
Negative values mean friction prevents sliding.
''')

av_w = 2*math.pi*1450/60
avtab = ''.join(f"| {r:,} rpm | {2*math.pi*r/60:.2f} rad/s | {r/60:.2f} Hz |\n" for r in (1, 60, 750, 1000, 1500, 3000, 3600, 10000))
page('physics', 'angular-velocity', f'''
title: Angular Velocity Calculator (rpm to rad/s & Linear Speed)
description: Convert rpm to rad/s and Hz, and calculate the linear (tangential) speed at any radius — for motors, wheels, pulleys and rotating shafts.
category: physics
intro: "Rotating machines are rated in revolutions per minute, but physics formulas use angular velocity in radians per second. This angular velocity calculator converts between rpm, rad/s and Hz and gives the tangential speed at any radius, v = ωr — handy for motor shafts, wheels, grinding discs and fans."
keywords: [angular velocity calculator, rpm to rad/s, rad/s to rpm, tangential velocity calculator, rpm to linear speed, rotational speed converter]
updated: {D}
variables:
  - {{ id: N, label: Rotational speed, suffix: rpm, default: 1450, min: 0 }}
  - {{ id: r, label: Radius, family: length, unit: mm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: w, label: Angular velocity (ω), suffix: rad/s, min: 0 }}
  - {{ id: f, label: Rotational frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: v, label: Tangential (rim) speed, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: T, label: Time per revolution, family: seconds, unit: ms, min: 0 }}
equations:
  - w = 2 * pi * N / 60
  - f = N / 60
  - v = w * r
  - T = 1 / f
faq:
  - q: How do I convert rpm to rad/s?
    a: Multiply by 2π and divide by 60, so ω = rpm × 0.10472. 1,450 rpm is about 151.8 rad/s.
  - q: How do I find linear speed from rpm?
    a: v = ω × r = 2π r × rpm ÷ 60. A 200 mm diameter disc at 1,450 rpm has a rim speed of about 15.2 m/s.
  - q: What is the difference between angular velocity and frequency?
    a: Frequency counts revolutions per second (Hz); angular velocity counts radians per second. One revolution is 2π radians, so ω = 2πf.
  - q: Why does rim speed matter?
    a: Grinding wheels, saw blades and fans have a maximum safe peripheral speed, and belt and conveyor speeds are set by pulley rim speed.
related: [engineering/pulley-speed, physics/centripetal-force, physics/rotational-kinetic-energy, engineering/torque-power-speed]
''', f'''
## How to use the angular velocity calculator

Enter the **speed in rpm** and a **radius**. You get the angular velocity in rad/s, the rotational frequency in Hz, the tangential speed at that radius and the time for one revolution. Enter rad/s or a rim speed instead and clear rpm to convert the other way.

## Angular velocity formulas

<p class="formula">ω = 2π × N ÷ 60 &nbsp;·&nbsp; f = N ÷ 60 &nbsp;·&nbsp; v = ω × r</p>

## Example

A 4-pole motor at 1,450 rpm driving a 200 mm diameter disc (r = 100 mm):

- ω = 2π × 1450 ÷ 60 = **{av_w:.2f} rad/s**
- f = **{1450/60:.2f} Hz** (one turn every {60000/1450:.1f} ms)
- Rim speed = {av_w:.2f} × 0.1 = **{av_w*0.1:.2f} m/s**

## rpm conversion table

| Speed | Angular velocity | Frequency |
|---|---|---|
{avtab}''')

rk_I = 0.5*20*0.25**2; rk_w = 2*math.pi*1000/60; rk_E = 0.5*rk_I*rk_w**2
page('physics', 'rotational-kinetic-energy', f'''
title: Rotational Kinetic Energy Calculator (Flywheel Energy)
description: Calculate rotational kinetic energy ½Iω² and moment of inertia for a disc, ring or sphere from mass, radius and rpm — for flywheels and rotors.
category: physics
intro: "A spinning body stores kinetic energy that depends on its moment of inertia and the square of its angular velocity. This rotational kinetic energy calculator works out the moment of inertia of common shapes and the stored energy from rpm — useful for flywheels, motor rotors, grinding wheels and coast-down estimates."
keywords: [rotational kinetic energy calculator, flywheel energy calculator, moment of inertia calculator, kinetic energy of rotation, i omega squared, spinning disc energy]
updated: {D}
variables:
  - id: k
    label: Shape
    default: 0.5
    options:
      - {{ label: 'Solid disc or cylinder (½ m r²)', value: 0.5 }}
      - {{ label: 'Thin ring or hoop (m r²)', value: 1 }}
      - {{ label: 'Solid sphere (⅖ m r²)', value: 0.4 }}
      - {{ label: 'Thin hollow sphere (⅔ m r²)', value: 0.666667 }}
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 20, min: 0 }}
  - {{ id: r, label: Radius, family: length, unit: mm, imperialUnit: in, default: 250, min: 0 }}
  - {{ id: N, label: Speed, suffix: rpm, default: 1000, min: 0 }}
  - {{ id: I, label: Moment of inertia, suffix: kg·m², min: 0, decimals: 4 }}
  - {{ id: w, label: Angular velocity, suffix: rad/s, min: 0 }}
  - {{ id: E, label: Rotational kinetic energy, family: energy, unit: J, min: 0 }}
equations:
  - I = k * m * r^2
  - w = 2 * pi * N / 60
  - E = 0.5 * I * w^2
faq:
  - q: What is the formula for rotational kinetic energy?
    a: E = ½ I ω², where I is the moment of inertia in kg·m² and ω the angular velocity in rad/s. It mirrors ½ m v² for straight-line motion.
  - q: What is the moment of inertia of a solid disc?
    a: I = ½ m r². A thin ring of the same mass and radius has twice that, m r², because all its mass is at the rim.
  - q: Why are flywheels shaped like rims?
    a: Putting mass far from the axis raises the moment of inertia, so a rim-heavy flywheel stores more energy for the same weight.
  - q: How does speed affect stored energy?
    a: Energy rises with the square of speed — doubling rpm stores four times the energy, which is also why overspeed failures are so violent.
related: [physics/kinetic-energy, physics/angular-velocity, physics/torque, engineering/torque-power-speed]
''', f'''
## How to use the rotational kinetic energy calculator

Choose the **shape**, then enter the **mass**, the **radius** and the **speed in rpm**. You get the moment of inertia, the angular velocity and the stored rotational kinetic energy. For other shapes, clear the mass and enter a known moment of inertia directly.

## Rotational kinetic energy formula

<p class="formula">E = ½ I ω² &nbsp;·&nbsp; I = k m r² &nbsp;·&nbsp; ω = 2π N ÷ 60</p>

## Example

A 20 kg solid steel disc of radius 250 mm spinning at 1,000 rpm:

- I = ½ × 20 × 0.25² = **{rk_I:.4f} kg·m²**
- ω = 2π × 1000 ÷ 60 = **{rk_w:.2f} rad/s**
- E = ½ × {rk_I} × {rk_w:.2f}² = **{rk_E:,.0f} J** ({rk_E/3600:.3f} Wh)

## Moments of inertia of common shapes

| Shape (about central axis) | I |
|---|---|
| Solid disc or cylinder | ½ m r² |
| Thin ring or hoop | m r² |
| Thick ring, radii r₁ and r₂ | ½ m (r₁² + r₂²) |
| Solid sphere | ⅖ m r² |
| Thin hollow sphere | ⅔ m r² |
| Rod about its centre, length L | m L² ÷ 12 |
| Rod about one end | m L² ÷ 3 |

## Energy vs speed for the example disc

| Speed | Energy |
|---|---|
''' + ''.join(f"| {s:,} rpm | {0.5*rk_I*(2*math.pi*s/60)**2:,.0f} J |\n" for s in (500, 1000, 1500, 3000, 6000)))

sm_w = math.sqrt(2000/5); sm_f = sm_w/(2*math.pi); sm_d = 5*G/2000
page('physics', 'spring-mass-frequency', f'''
title: Spring-Mass Frequency Calculator (Natural Frequency)
description: Calculate the natural frequency, angular frequency and period of a mass on a spring from spring constant and mass — or from static deflection.
category: physics
intro: "A mass on a spring oscillates at a natural frequency set only by its stiffness and mass, f = (1/2π)√(k/m). This spring-mass frequency calculator gives the frequency, angular frequency, period and static deflection — the basis of vibration isolation, machine mounts and simple harmonic motion problems."
keywords: [spring mass frequency calculator, natural frequency calculator, spring mass system, simple harmonic oscillator frequency, period of spring, static deflection natural frequency]
updated: {D}
variables:
  - {{ id: k, label: Spring constant (stiffness), suffix: N/m, default: 2000, min: 0 }}
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 5, min: 0 }}
  - {{ id: w, label: Angular frequency (ω), suffix: rad/s, min: 0 }}
  - {{ id: f, label: Natural frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: T, label: Period, family: seconds, unit: s, min: 0 }}
  - {{ id: d, label: Static deflection under gravity, family: length, unit: mm, imperialUnit: in, min: 0 }}
equations:
  - w = sqrt(k / m)
  - f = w / (2 * pi)
  - T = 1 / f
  - d = m * g0 / k
faq:
  - q: What is the natural frequency of a spring-mass system?
    a: f = (1 ÷ 2π) × √(k ÷ m). Stiffer springs raise the frequency; heavier masses lower it.
  - q: How do I find natural frequency from static deflection?
    a: f = (1 ÷ 2π) × √(g ÷ δ). A mount that sags 25 mm under its load has a natural frequency of about 3.2 Hz — enter the deflection and clear the spring constant.
  - q: How is this used for vibration isolation?
    a: Isolation starts when the forcing frequency is more than √2 times the natural frequency; designers usually aim for a ratio of 3 or more.
  - q: Does gravity change the frequency of a vertical spring?
    a: No. Gravity shifts the equilibrium position by the static deflection, but the oscillation frequency is the same as horizontal.
related: [physics/hookes-law, physics/pendulum, physics/wavelength-frequency, electronics/resonant-frequency]
''', f'''
## How to use the spring-mass frequency calculator

Enter the **spring constant** in N/m and the **mass**. You get the angular frequency, the natural frequency in Hz, the period of one oscillation and the static deflection of the spring under the weight. If you know the deflection instead, clear the spring constant and enter it.

## Spring-mass formulas

<p class="formula">ω = √(k ÷ m) &nbsp;·&nbsp; f = ω ÷ 2π &nbsp;·&nbsp; T = 1 ÷ f</p>

<p class="formula">δ = m g ÷ k &nbsp;⇒&nbsp; f = (1/2π) √(g ÷ δ)</p>

## Example

A 5 kg mass on a 2,000 N/m spring:

- ω = √(2000 ÷ 5) = **{sm_w:g} rad/s**
- f = 20 ÷ 2π = **{sm_f:.3f} Hz**
- T = **{1/sm_f:.4f} s**
- Static deflection = 5 × 9.807 ÷ 2000 = **{sm_d*1000:.1f} mm**

## Natural frequency from static deflection

| Static deflection | Natural frequency |
|---|---|
''' + ''.join(f"| {d:g} mm | {math.sqrt(G/(d/1000))/(2*math.pi):.2f} Hz |\n" for d in (1, 2.5, 5, 10, 25, 50, 100)) + '''
## Notes

- Springs in **series** combine as 1/k = 1/k₁ + 1/k₂; in **parallel**, k = k₁ + k₂.
- Damping lowers the observed frequency slightly: ω<sub>d</sub> = ω √(1 − ζ²).
- See the [Hooke's law calculator](/physics/hookes-law/) to find k from a force and extension.
''')

print('done')
