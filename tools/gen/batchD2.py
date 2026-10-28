import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
from ib import L
D = '2026-10-27'; pi = math.pi
E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

# 1 LED resistor
page('electronics', 'led-resistor', f'''
title: LED Resistor Calculator
description: Calculate the series resistor value and wattage for one LED or a string of LEDs from supply voltage, forward voltage and current.
category: electronics
keywords: [led resistor calculator, led current limiting resistor, resistor for led, led series resistor, led forward voltage, led resistor value, 5v 12v led resistor]
updated: {D}
featured: true
variables:
  - {{ id: Vs, label: Supply voltage, family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: Vf, label: LED forward voltage, family: voltage, unit: V, default: 2.0, min: 0 }}
  - {{ id: n, label: LEDs in series, default: 3, min: 1 }}
  - {{ id: If, label: LED current, family: current, unit: mA, default: 20, min: 0 }}
  - {{ id: R, label: Resistor value, family: resistance, unit: ohm, min: 0 }}
  - {{ id: P, label: Resistor power, family: power, unit: mW, min: 0 }}
equations:
  - R = (Vs - n * Vf) / If
  - P = If^2 * R
faq:
  - q: How do I calculate an LED resistor?
    a: R = (supply voltage − LED forward voltage × number of LEDs) ÷ LED current. A red LED (2 V) at 20 mA on 5 V needs (5 − 2) ÷ 0.02 = 150 Ω.
  - q: What if the calculated value is not a standard resistor?
    a: Choose the next higher standard value. It slightly reduces current and brightness but is safer for the LED.
  - q: What resistor wattage do I need?
    a: At least twice the calculated power. For most single indicator LEDs, a 0.25 W resistor is plenty.
  - q: Can I put LEDs in parallel with one resistor?
    a: It is not recommended — small differences in forward voltage make one LED take most of the current. Give each LED or string its own resistor.
related: [physics/ohms-law, electronics/voltage-divider, physics/resistors-series-parallel, electronics/resistor-color-code]
{L(('led-resistor-calculation', 'LED Resistor Calculation'), ('led-working-principle', 'LED Working Principle'))}''', '''
## How to use this calculator

Enter the **supply voltage**, the LED's **forward voltage** (from the datasheet or the table below), the **number of LEDs in series** and the **current**. You get the resistor value and the power it will dissipate.

## The formula

<p class="formula">R = (V<sub>s</sub> − n × V<sub>f</sub>) ÷ I<sub>f</sub> &nbsp;·&nbsp; P = I<sub>f</sub>² × R</p>

## Typical forward voltages

| LED colour | Forward voltage |
|---|---|
| Infrared | 1.2–1.5 V |
| Red | 1.8–2.2 V |
| Orange, yellow | 2.0–2.2 V |
| Green (standard) | 2.0–2.4 V |
| Green (bright), blue, white | 2.8–3.4 V |
| UV | 3.1–4.0 V |

Standard 5 mm indicator LEDs are usually rated 20 mA; many work well at 5–10 mA.

## Resistor values at 20 mA

| Supply | Red (2.0 V) | White/blue (3.2 V) |
|---|---|---|
''' + ''.join(f"| {v} V | {(v-2)/0.02:.0f} Ω | {(v-3.2)/0.02:.0f} Ω |\n" for v in [3.3, 5, 9, 12, 24]) + '''
## Standard values

The nearest E12 values are 10, 12, 15, 18, 22, 27, 33, 39, 47, 56, 68 and 82 (× 1, 10, 100, 1k…). Round up to the next value. See the [resistor colour code calculator](/electronics/resistor-color-code/).

## High-power LEDs

For power LEDs (350 mA and above) a resistor wastes too much energy and does not compensate for temperature. Use a constant-current LED driver instead.

## Indicator LEDs on 24 V DC panels

For a 24 V PLC panel indicator at 10 mA with a 2 V LED: R = 22 ÷ 0.01 = 2.2 kΩ, dissipating 0.22 W — use a 0.5 W resistor.
''')

# 2 Voltage divider
page('electronics', 'voltage-divider', f'''
title: Voltage Divider Calculator
description: Calculate the output voltage of a resistor voltage divider, or the resistor values needed for a target output — with divider current and power.
category: electronics
keywords: [voltage divider calculator, resistor divider, voltage divider formula, vout r2/(r1+r2), potential divider, resistor ratio calculator]
updated: {D}
variables:
  - {{ id: Vin, label: Input voltage, family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: R1, label: R1 (top), family: resistance, unit: kohm, default: 10, min: 0 }}
  - {{ id: R2, label: R2 (bottom), family: resistance, unit: kohm, default: 4.7, min: 0 }}
  - {{ id: Vout, label: Output voltage, family: voltage, unit: V, min: 0 }}
  - {{ id: I, label: Divider current, family: current, unit: mA, min: 0 }}
  - {{ id: P, label: Total power, family: power, unit: mW, min: 0 }}
equations:
  - Vout = Vin * R2 / (R1 + R2)
  - I = Vin / (R1 + R2)
  - P = Vin * I
faq:
  - q: What is the voltage divider formula?
    a: Vout = Vin × R2 ÷ (R1 + R2), where R2 is the resistor between the output and ground.
  - q: How do I choose resistor values?
    a: Pick R2, then R1 = R2 × (Vin ÷ Vout − 1). Keep the divider current at least 10 times the load current so the load does not pull the output down.
  - q: Can I power a circuit from a voltage divider?
    a: Generally no. The output voltage changes with load current. Use a voltage regulator to power circuits; dividers are for sensing and reference voltages.
  - q: How do I scale 24 V down for a 3.3 V ADC?
    a: A 62 kΩ / 10 kΩ divider gives 24 × 10 ÷ 72 = 3.33 V. Add a small capacitor across R2 to filter noise.
related: [electronics/current-divider, physics/ohms-law, physics/resistors-series-parallel, electronics/adc-resolution]
{L(('voltage-divider-rule-explained', 'Voltage Divider Rule Explained'), ('kirchhoffs-voltage-law-kvl-explained', 'Kirchhoff’s Voltage Law (KVL) Explained'))}''', '''
## How to use this calculator

Enter the **input voltage** and the two resistors (**R1** on top, **R2** to ground). You get the output voltage, the current through the divider and the power it wastes. To design a divider, enter the target output and one resistor and press × on the other.

## The formula

<p class="formula">V<sub>out</sub> = V<sub>in</sub> × R₂ ÷ (R₁ + R₂)</p>

## Common divider ratios

| R1 | R2 | Ratio | 12 V in | 24 V in |
|---|---|---|---|---|
''' + ''.join(f"| {a} k | {b} k | {b/(a+b):.3f} | {12*b/(a+b):.2f} V | {24*b/(a+b):.2f} V |\n" for a, b in [(10, 10), (10, 4.7), (10, 3.3), (22, 10), (39, 10), (62, 10), (100, 10)]) + '''
## Loading effect

A load resistance R<sub>L</sub> across R2 acts in parallel with it, reducing the output. Keep R<sub>L</sub> at least ten times R2, or buffer the output with an op-amp [voltage follower](/electronics/op-amp-gain/).

## Choosing resistance values

- **Lower values** (1–10 kΩ): stiffer output, more current wasted.
- **Higher values** (100 kΩ–1 MΩ): low power for battery circuits, but more sensitive to noise and ADC input current.

## Measuring with a divider

Dividers scale high voltages for ADCs and meters. Use 1% or better resistors with low temperature coefficients for accurate measurement, and make sure each resistor's voltage rating is not exceeded.
''')

# 3 Current divider
page('electronics', 'current-divider', f'''
title: Current Divider Calculator
description: Calculate how a total current splits between two parallel resistors using the current divider rule — with branch currents and equivalent resistance.
category: electronics
keywords: [current divider calculator, current divider rule, parallel resistor current, branch current calculator, current division formula]
updated: {D}
variables:
  - {{ id: It, label: Total current, family: current, unit: A, default: 1, min: 0 }}
  - {{ id: R1, label: R1, family: resistance, unit: ohm, default: 100, min: 0 }}
  - {{ id: R2, label: R2, family: resistance, unit: ohm, default: 300, min: 0 }}
  - {{ id: I1, label: Current through R1, family: current, unit: A, min: 0 }}
  - {{ id: I2, label: Current through R2, family: current, unit: A, min: 0 }}
  - {{ id: Req, label: Equivalent resistance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: V, label: Voltage across the pair, family: voltage, unit: V, min: 0 }}
equations:
  - I1 = It * R2 / (R1 + R2)
  - I2 = It * R1 / (R1 + R2)
  - Req = R1 * R2 / (R1 + R2)
  - V = It * Req
faq:
  - q: What is the current divider rule?
    a: For two parallel resistors, I₁ = I_total × R₂ ÷ (R₁ + R₂). Each branch gets a share of the current in proportion to the other branch's resistance.
  - q: Which resistor carries more current?
    a: The smaller one. Current takes all paths, but more of it flows through lower resistance.
  - q: How do I handle more than two branches?
    a: Use conductances: I_n = I_total × G_n ÷ ΣG, where G = 1 ÷ R.
  - q: Where is the current divider used?
    a: In ammeter shunts, current-sharing resistors and in analysing parallel loads.
related: [electronics/voltage-divider, physics/resistors-series-parallel, physics/ohms-law, electronics/wheatstone-bridge]
{L(('current-divider-rule-explained', 'Current Divider Rule Explained'), ('kirchhoffs-current-law-kcl-explained', 'Kirchhoff’s Current Law (KCL) Explained'), ('shunt-resistors-in-instrumentation', 'Shunt Resistors in Instrumentation'))}''', '''
## How to use this calculator

Enter the **total current** entering the parallel pair and the two **resistances**. You get each branch current, the equivalent resistance and the voltage across the pair.

## The formulas

<p class="formula">I₁ = I<sub>T</sub> × R₂ ÷ (R₁ + R₂) &nbsp;·&nbsp; I₂ = I<sub>T</sub> × R₁ ÷ (R₁ + R₂)</p>

## Example

1 A into 100 Ω and 300 Ω in parallel:

- I₁ = 1 × 300 ÷ 400 = **0.75 A**
- I₂ = 1 × 100 ÷ 400 = **0.25 A**
- R<sub>eq</sub> = 75 Ω, V = 75 V

## Ammeter shunts

To extend a meter that reads 1 mA full scale with 100 Ω internal resistance to read 1 A, the shunt must carry 999 mA: R<sub>shunt</sub> = 100 × 0.001 ÷ 0.999 ≈ **0.1001 Ω**.

## 4–20 mA and 250 Ω

A 250 Ω resistor converts a 4–20 mA loop current into 1–5 V for a voltage input — a common trick that relies on Ohm's law rather than division. Keep loop resistance within the transmitter's limits — see the [loop resistance calculator](/engineering/loop-resistance/).
''')

# 4 555 astable
def f555(r1, r2, c): return 1.44/((r1+2*r2)*c)
page('electronics', '555-timer', f'''
title: 555 Timer Calculator (Astable Mode)
description: Calculate the frequency, duty cycle, high time and low time of a 555 timer in astable mode from R1, R2 and C — or choose parts for a target frequency.
category: electronics
keywords: [555 timer calculator, 555 astable calculator, ne555 frequency, 555 duty cycle, 555 oscillator, 555 timer formula, square wave generator]
updated: {D}
variables:
  - {{ id: R1, label: R1, family: resistance, unit: kohm, default: 1, min: 0 }}
  - {{ id: R2, label: R2, family: resistance, unit: kohm, default: 10, min: 0 }}
  - {{ id: C, label: Timing capacitor C, family: capacitance, unit: uF, default: 10, min: 0 }}
  - {{ id: f, label: Frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: th, label: High time, family: seconds, unit: ms, min: 0 }}
  - {{ id: tl, label: Low time, family: seconds, unit: ms, min: 0 }}
  - {{ id: D, label: Duty cycle, family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - th = 0.693 * (R1 + R2) * C
  - tl = 0.693 * R2 * C
  - f = 1 / (th + tl)
  - D = th / (th + tl)
faq:
  - q: What is the 555 astable frequency formula?
    a: f = 1.44 ÷ ((R1 + 2R2) × C). With R1 = 1 kΩ, R2 = 10 kΩ and C = 10 µF, the frequency is about 6.86 Hz.
  - q: Why can't the duty cycle go below 50%?
    a: The capacitor charges through R1 + R2 but discharges through R2 only, so the high time is always longer. Add a diode across R2 to get duty cycles under 50%.
  - q: What is the minimum R1?
    a: About 1 kΩ, to limit the discharge transistor current when it turns on.
  - q: How accurate is the 555?
    a: Typically 1–2% plus component tolerances. Use film capacitors rather than electrolytics for stable timing.
related: [physics/rc-time-constant, electronics/pwm-duty-cycle, electronics/rc-filter, physics/wavelength-frequency]
{L(('555-timer-ic-explained', '555 Timer IC Explained'),)}''', '''
## How to use this calculator

Enter **R1**, **R2** and the timing capacitor **C**. You get the output frequency, the high and low times and the duty cycle. To design for a frequency, enter it with two components and press × on the third.

## The formulas (astable)

<p class="formula">t<sub>H</sub> = 0.693 (R₁ + R₂) C &nbsp;·&nbsp; t<sub>L</sub> = 0.693 R₂ C</p>

<p class="formula">f = 1.44 ÷ ((R₁ + 2R₂) C) &nbsp;·&nbsp; D = (R₁ + R₂) ÷ (R₁ + 2R₂)</p>

## Example frequencies (R1 = 1 kΩ)

| R2 | C | Frequency | Duty cycle |
|---|---|---|---|
''' + ''.join(f"| {r2} kΩ | {cl} | {(lambda x: f'{x/1000:.2f} kHz' if x>=1000 else f'{x:.2f} Hz')(f555(1e3,r2*1e3,c))} | {(1+r2)/(1+2*r2)*100:.0f}% |\n" for r2, cl, c in [(10, '100 µF', 100e-6), (10, '10 µF', 10e-6), (47, '1 µF', 1e-6), (10, '100 nF', 100e-9), (10, '10 nF', 10e-9), (1, '10 nF', 10e-9)]) + '''
## Monostable mode

In one-shot (monostable) mode, the output pulse lasts t = 1.1 × R × C after a trigger. 100 kΩ and 10 µF give about 1.1 s.

## 555 pin functions

| Pin | Name | Use |
|---|---|---|
| 1 | GND | 0 V |
| 2 | Trigger | Starts timing below ⅓ V<sub>cc</sub> |
| 3 | Output | Up to about 200 mA |
| 4 | Reset | Tie to V<sub>cc</sub> if unused |
| 5 | Control | 10 nF to ground for stability |
| 6 | Threshold | Ends timing above ⅔ V<sub>cc</sub> |
| 7 | Discharge | Discharges the timing capacitor |
| 8 | V<sub>cc</sub> | 4.5–16 V (bipolar NE555) |

The CMOS version (7555, TLC555) runs from 2 V and uses far less current.
''')

# 5 RC filter
def fc(r, c): return 1/(2*pi*r*c)
page('electronics', 'rc-filter', f'''
title: RC Filter Cutoff Frequency Calculator
description: Calculate the −3 dB cutoff frequency of an RC low-pass or high-pass filter, or the R or C needed for a target cutoff — with attenuation at any frequency.
category: electronics
keywords: [rc filter calculator, cutoff frequency calculator, rc low pass filter, rc high pass filter, 1/2πrc, -3db frequency, corner frequency]
updated: {D}
variables:
  - {{ id: R, label: Resistance, family: resistance, unit: kohm, default: 10, min: 0 }}
  - {{ id: C, label: Capacitance, family: capacitance, unit: nF, default: 100, min: 0 }}
  - {{ id: fc, label: Cutoff frequency (−3 dB), family: frequency, unit: Hz, min: 0 }}
  - {{ id: tau, label: Time constant (RC), family: seconds, unit: ms, min: 0 }}
  - {{ id: f, label: Test frequency, family: frequency, unit: Hz, default: 1000, min: 0 }}
  - {{ id: Glp, label: Low-pass gain at test frequency, suffix: dB, decimals: 2 }}
  - {{ id: Ghp, label: High-pass gain at test frequency, suffix: dB, decimals: 2 }}
equations:
  - fc = 1 / (2 * pi * R * C)
  - tau = R * C
  - Glp = -10 * log10(1 + (f / fc)^2)
  - Ghp = -10 * log10(1 + (fc / f)^2)
faq:
  - q: What is the cutoff frequency of an RC filter?
    a: fc = 1 ÷ (2πRC). At this frequency the output is 70.7% of the input (−3 dB). 10 kΩ and 100 nF give 159 Hz.
  - q: What is the difference between low-pass and high-pass?
    a: A low-pass filter (R in series, C to ground) passes low frequencies; a high-pass filter (C in series, R to ground) passes high frequencies. Both have the same cutoff formula.
  - q: How steep is an RC filter?
    a: First order — 20 dB per decade (6 dB per octave) beyond the cutoff. For steeper roll-off, cascade stages or use an active filter.
  - q: How do I filter noise on a sensor signal?
    a: Choose a cutoff well above the signal bandwidth but below the noise frequency — for slow process signals, a few hertz is common.
related: [physics/rc-time-constant, electronics/reactance, physics/decibel, electronics/op-amp-gain]
{L(('rc-low-pass-high-pass-filter', 'RC Low-Pass and High-Pass Filters'), ('active-filter-sallen-and-key', 'Active Filter: Sallen-Key Topology'), ('rc-and-rl-time-constant-explained', 'RC and RL Time Constant Explained'))}''', '''
## How to use this calculator

Enter **R** and **C** to get the cutoff frequency and time constant. Add a **test frequency** to see how much a low-pass or high-pass filter attenuates it. To design a filter, enter the target cutoff and one component, then press × on the other.

## The formulas

<p class="formula">f<sub>c</sub> = 1 ÷ (2πRC)</p>

<p class="formula">Low-pass gain = −10 log₁₀[1 + (f/f<sub>c</sub>)²] dB &nbsp;·&nbsp; High-pass gain = −10 log₁₀[1 + (f<sub>c</sub>/f)²] dB</p>

## Common RC combinations

| R | C | Cutoff |
|---|---|---|
''' + ''.join(f"| {rl} | {cl} | {(lambda x: f'{x/1000:.2f} kHz' if x>=1000 else f'{x:.2f} Hz')(fc(r,c))} |\n" for rl, cl, r, c in [('100 kΩ', '10 µF', 1e5, 10e-6), ('10 kΩ', '10 µF', 1e4, 10e-6), ('10 kΩ', '1 µF', 1e4, 1e-6), ('10 kΩ', '100 nF', 1e4, 100e-9), ('1 kΩ', '100 nF', 1e3, 100e-9), ('1 kΩ', '10 nF', 1e3, 10e-9), ('100 Ω', '1 nF', 100, 1e-9)]) + '''
## Low-pass response

| Frequency | Gain | Output (of input) |
|---|---|---|
| 0.1 f<sub>c</sub> | −0.04 dB | 99.5% |
| 0.5 f<sub>c</sub> | −0.97 dB | 89.4% |
| f<sub>c</sub> | −3.01 dB | 70.7% |
| 2 f<sub>c</sub> | −6.99 dB | 44.7% |
| 10 f<sub>c</sub> | −20.0 dB | 9.95% |
| 100 f<sub>c</sub> | −40.0 dB | 1.0% |

## Practical tips

- The source impedance adds to R; the load impedance appears in parallel with C. Keep the load at least ten times R.
- For ADC anti-aliasing, set the cutoff below half the sampling rate.
- Use C0G/NP0 or film capacitors for stable filters; ceramic X7R values change with voltage and temperature.
''')

# 6 Op-amp gain
page('electronics', 'op-amp-gain', f'''
title: Op-Amp Gain Calculator (Inverting and Non-Inverting)
description: Calculate the voltage gain and output of an inverting or non-inverting op-amp amplifier from Rf and Rin — or the resistor needed for a target gain.
category: electronics
keywords: [op amp gain calculator, inverting amplifier calculator, non inverting amplifier gain, opamp gain formula, rf rin, amplifier gain db]
updated: {D}
variables:
  - id: t
    label: Configuration
    default: 1
    options:
      - {{ label: Non-inverting (1 + Rf/Rin), value: 1 }}
      - {{ label: Inverting (−Rf/Rin), value: 0 }}
  - {{ id: Rf, label: Feedback resistor (Rf), family: resistance, unit: kohm, default: 100, min: 0 }}
  - {{ id: Ri, label: Input / ground resistor (Rin), family: resistance, unit: kohm, default: 10, min: 0.000001 }}
  - {{ id: Vin, label: Input voltage, family: voltage, unit: mV, default: 100 }}
  - {{ id: G, label: Voltage gain, decimals: 3 }}
  - {{ id: Vout, label: Output voltage (ideal), family: voltage, unit: V }}
  - {{ id: GdB, label: Gain in dB, suffix: dB, decimals: 2 }}
equations:
  - G = t * (1 + Rf / Ri) - (1 - t) * Rf / Ri
  - Vout = G * Vin
  - GdB = 20 * log10(abs(G))
faq:
  - q: What is the gain of a non-inverting amplifier?
    a: G = 1 + Rf ÷ Rin, where Rin is the resistor from the inverting input to ground. 100 kΩ and 10 kΩ give a gain of 11.
  - q: What is the gain of an inverting amplifier?
    a: G = −Rf ÷ Rin. The minus sign means the output is inverted. 100 kΩ and 10 kΩ give −10.
  - q: Why is my output lower than calculated?
    a: The output cannot swing beyond the supply rails (minus a headroom of 0.1–2 V depending on the op-amp), and gain falls at high frequency due to the gain-bandwidth product.
  - q: What is a voltage follower?
    a: A non-inverting amplifier with Rf = 0 and no Rin — a gain of exactly 1. It buffers a high-impedance source.
related: [electronics/rc-filter, electronics/voltage-divider, physics/decibel, electronics/adc-resolution]
{L(('operational-amplifier-op-amp-basics', 'Operational Amplifier (Op-Amp) Basics'), ('voltage-follower-unity-gain-buffer-explained', 'Voltage Follower (Unity-Gain Buffer) Explained'), ('instrumentation-amplifier-vs-op-amp-key-differences', 'Instrumentation Amplifier vs Op-Amp'))}''', '''
## How to use this calculator

Choose **non-inverting** or **inverting**, and enter the **feedback resistor**, the **input resistor** and an **input voltage**. You get the gain (as a ratio and in dB) and the ideal output. To pick a resistor for a target gain, enter the gain and press × on Rf or Rin.

## The formulas

| Configuration | Gain |
|---|---|
| Non-inverting | G = 1 + R<sub>f</sub> ÷ R<sub>in</sub> |
| Inverting | G = −R<sub>f</sub> ÷ R<sub>in</sub> |
| Voltage follower | G = 1 |

Input impedance is very high for the non-inverting amplifier and equal to R<sub>in</sub> for the inverting amplifier.

## Resistor pairs for common gains

| Target gain | Non-inverting Rf / Rin | Inverting Rf / Rin |
|---|---|---|
| 2 | 10 k / 10 k | 20 k / 10 k |
| 5 | 40.2 k / 10 k | 49.9 k / 10 k |
| 10 | 90.9 k / 10 k | 100 k / 10 k |
| 11 | 100 k / 10 k | 110 k / 10 k |
| 101 | 100 k / 1 k | 100 k / 990 Ω |

## Bandwidth

Every op-amp has a gain-bandwidth product (GBW). An op-amp with 1 MHz GBW at a gain of 100 has a bandwidth of only about 10 kHz.

## Instrumentation amplifiers

For bridge sensors and thermocouples, use an instrumentation amplifier, which rejects common-mode voltage and sets gain with a single resistor.
''')

# 7 Resistor color code
digits = ['Black', 'Brown', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet', 'Grey', 'White']
dopts = ''.join(f"      - {{ label: '{c} ({i})', value: {i} }}\n" for i, c in enumerate(digits))
mults = [('Silver (× 0.01)', 0.01), ('Gold (× 0.1)', 0.1), ('Black (× 1)', 1), ('Brown (× 10)', 10), ('Red (× 100)', 100), ('Orange (× 1k)', 1e3), ('Yellow (× 10k)', 1e4), ('Green (× 100k)', 1e5), ('Blue (× 1M)', 1e6), ('Violet (× 10M)', 1e7)]
mopts = ''.join(f"      - {{ label: '{l}', value: {v} }}\n" for l, v in mults)
tols = [('Brown (±1%)', 0.01), ('Red (±2%)', 0.02), ('Green (±0.5%)', 0.005), ('Blue (±0.25%)', 0.0025), ('Violet (±0.1%)', 0.001), ('Grey (±0.05%)', 0.0005), ('Gold (±5%)', 0.05), ('Silver (±10%)', 0.1)]
topts = ''.join(f"      - {{ label: '{l}', value: {v} }}\n" for l, v in tols)
page('electronics', 'resistor-color-code', f'''
title: Resistor Color Code Calculator (4-Band)
description: Find a resistor's value and tolerance from its 4 colour bands — or look up the colours for any resistance. Includes the full colour chart.
category: electronics
keywords: [resistor color code calculator, resistor colour code, 4 band resistor, resistor value from colors, resistor color chart, brown black red, resistor bands]
updated: {D}
variables:
  - id: b1
    label: Band 1 (first digit)
    default: 1
    options:
{dopts}  - id: b2
    label: Band 2 (second digit)
    default: 0
    options:
{dopts}  - id: m
    label: Band 3 (multiplier)
    default: 100
    options:
{mopts}  - id: tol
    label: Band 4 (tolerance)
    default: 0.05
    options:
{topts}  - {{ id: R, label: Resistance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Rmin, label: Minimum value, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Rmax, label: Maximum value, family: resistance, unit: ohm, min: 0 }}
equations:
  - R = (10 * b1 + b2) * m
  - Rmin = R * (1 - tol)
  - Rmax = R * (1 + tol)
faq:
  - q: How do I read a resistor colour code?
    a: Hold the resistor with the tolerance band (usually gold or silver) on the right. The first two bands are digits, the third is the multiplier and the fourth is tolerance. Brown–black–red–gold is 10 × 100 = 1 kΩ ±5%.
  - q: What is a good way to remember the colours?
    a: Black 0, brown 1, red 2, orange 3, yellow 4, green 5, blue 6, violet 7, grey 8, white 9 — the order of the rainbow sits in the middle.
  - q: What about 5-band resistors?
    a: They have three digit bands, then multiplier and tolerance. They are used for 1% and better precision resistors.
  - q: Which end do I start from?
    a: The end with the band closest to the edge. Gold and silver are never first bands.
related: [electronics/led-resistor, physics/resistors-series-parallel, physics/ohms-law, electronics/voltage-divider]
{L(('resistor-color-code-guide', 'Resistor Color Code Guide'), ('what-is-resistance', 'What Is Resistance?'))}''', '''
## How to use this calculator

Choose the four **colour bands** from left to right. The calculator shows the resistance and its tolerance range. The default — brown, black, red, gold — is 1 kΩ ±5%.

## The colour chart

| Colour | Digit | Multiplier | Tolerance |
|---|---|---|---|
| Black | 0 | × 1 | — |
| Brown | 1 | × 10 | ±1% |
| Red | 2 | × 100 | ±2% |
| Orange | 3 | × 1 k | — |
| Yellow | 4 | × 10 k | — |
| Green | 5 | × 100 k | ±0.5% |
| Blue | 6 | × 1 M | ±0.25% |
| Violet | 7 | × 10 M | ±0.1% |
| Grey | 8 | — | ±0.05% |
| White | 9 | — | — |
| Gold | — | × 0.1 | ±5% |
| Silver | — | × 0.01 | ±10% |

## Common resistors

| Value | Bands |
|---|---|
| 100 Ω | Brown, black, brown |
| 220 Ω | Red, red, brown |
| 330 Ω | Orange, orange, brown |
| 470 Ω | Yellow, violet, brown |
| 1 kΩ | Brown, black, red |
| 4.7 kΩ | Yellow, violet, red |
| 10 kΩ | Brown, black, orange |
| 47 kΩ | Yellow, violet, orange |
| 100 kΩ | Brown, black, yellow |
| 1 MΩ | Brown, black, green |

## E-series values

Resistors come in standard series. E12 (±10%): ''' + ', '.join(f'{x:g}' for x in E12) + ''' — repeated for each decade. E24 (±5%) adds values in between, and E96 (±1%) has 96 per decade.

## SMD resistors

Surface-mount resistors use number codes: "103" = 10 × 10³ = 10 kΩ; "4R7" = 4.7 Ω; E96 parts use codes like "01C" = 10 kΩ.
''')

# 8 Capacitor energy
page('electronics', 'capacitor-energy', f'''
title: Capacitor Energy and Charge Calculator
description: Calculate the energy stored in a capacitor and its charge from capacitance and voltage — for supercapacitors, DC links and flash circuits.
category: electronics
keywords: [capacitor energy calculator, energy stored in capacitor, 1/2 cv2, capacitor charge calculator, q = cv, supercapacitor energy, capacitor joules]
updated: {D}
variables:
  - {{ id: C, label: Capacitance, family: capacitance, unit: uF, default: 1000, min: 0 }}
  - {{ id: V, label: Voltage, family: voltage, unit: V, default: 50, min: 0 }}
  - {{ id: E, label: Stored energy, family: energy, unit: J, min: 0 }}
  - {{ id: Q, label: Charge, suffix: C (coulombs), min: 0, decimals: 6 }}
equations:
  - E = 0.5 * C * V^2
  - Q = C * V
faq:
  - q: How much energy does a capacitor store?
    a: E = ½ × C × V². A 1,000 µF capacitor at 50 V stores 1.25 J.
  - q: How much usable energy is there between two voltages?
    a: E = ½ C (V₁² − V₂²). A supercapacitor discharged from full voltage to half voltage delivers 75% of its stored energy.
  - q: Why are charged capacitors dangerous?
    a: Large capacitors in power supplies, VFDs and microwave ovens can hold lethal energy for minutes after switch-off. Always discharge and verify with a meter before working.
  - q: What is the charge on a capacitor?
    a: Q = C × V, in coulombs.
related: [physics/rc-time-constant, electronics/inductor-energy, electronics/reactance, electronics/capacitor-lifetime]
{L(('capacitor-working-principle', 'Capacitor Working Principle'), ('supercapacitor-working-principle', 'Supercapacitor Working Principle'), ('capacitor-types-explained', 'Capacitor Types Explained'), ('how-to-test-a-capacitor', 'How to Test a Capacitor'))}''', '''
## How to use this calculator

Enter the **capacitance** and the **voltage**. The calculator gives the stored energy and the charge. Press × on Voltage to find the voltage needed to store a given energy.

## The formulas

<p class="formula">E = ½ × C × V² &nbsp;·&nbsp; Q = C × V</p>

## Stored energy examples

| Capacitor | Voltage | Energy |
|---|---|---|
| 100 µF electrolytic | 25 V | 0.031 J |
| 1,000 µF electrolytic | 50 V | 1.25 J |
| 4,700 µF DC bus | 400 V | 376 J |
| Camera flash, 200 µF | 330 V | 10.9 J |
| Supercapacitor 10 F | 2.7 V | 36.5 J |
| Supercapacitor 3,000 F | 2.7 V | 10,935 J (3.04 Wh) |

## Supercapacitors vs batteries

A 3,000 F, 2.7 V supercapacitor stores about 3 Wh — roughly what a few AA batteries hold — but can deliver it in seconds and survive hundreds of thousands of cycles. They suit short backup, regenerative braking and burst power.

## Safety

Energy above about 0.25 J at voltages over 50 V can give a dangerous shock. Discharge large capacitors through a suitable resistor (not a screwdriver), then confirm 0 V with a meter.

## Series and parallel

- Parallel: C = C₁ + C₂ (same voltage rating).
- Series: 1/C = 1/C₁ + 1/C₂ — higher voltage, lower capacitance; use balancing resistors.
''')

# 9 Inductor energy
page('electronics', 'inductor-energy', f'''
title: Inductor Energy Calculator
description: Calculate the energy stored in an inductor's magnetic field from inductance and current with E = ½LI² — for chokes, relays and SMPS design.
category: electronics
keywords: [inductor energy calculator, energy stored in inductor, 1/2 li2, magnetic energy, inductor current energy, choke energy]
updated: {D}
variables:
  - {{ id: L, label: Inductance, family: inductance, unit: mH, default: 10, min: 0 }}
  - {{ id: I, label: Current, family: current, unit: A, default: 2, min: 0 }}
  - {{ id: E, label: Stored energy, family: energy, unit: J, min: 0 }}
  - {{ id: dt, label: Switch-off time, family: seconds, unit: ms, default: 1, min: 0 }}
  - {{ id: V, label: Induced voltage at switch-off (L·di/dt), family: voltage, unit: V, min: 0 }}
equations:
  - E = 0.5 * L * I^2
  - V = L * I / dt
faq:
  - q: How much energy does an inductor store?
    a: E = ½ × L × I². A 10 mH inductor carrying 2 A stores 20 mJ.
  - q: Why do relay coils need flyback diodes?
    a: When the current is interrupted quickly, the coil tries to keep it flowing, producing a voltage spike of L × di/dt that can reach hundreds of volts and damage transistors. A diode gives the current a safe path.
  - q: What is inductor saturation?
    a: Above a certain current the core can hold no more magnetic flux, so inductance falls sharply. Always stay below the saturation current in the datasheet.
  - q: Where is inductor energy used?
    a: Switch-mode power supplies store energy in inductors each cycle and release it to the output; ignition coils use it to create high-voltage sparks.
related: [electronics/capacitor-energy, electronics/reactance, electronics/buck-converter, physics/rc-time-constant]
{L(('inductor-working-principle', 'Inductor Working Principle'), ('inductor-saturation-current', 'Inductor Saturation Current'), ('lenzs-law-electromagnetic-induction', 'Lenz’s Law and Electromagnetic Induction'))}''', '''
## How to use this calculator

Enter the **inductance** and the **current** to get the stored energy. Add a **switch-off time** to estimate the voltage spike if the current is interrupted that quickly without suppression.

## The formulas

<p class="formula">E = ½ × L × I² &nbsp;·&nbsp; V = L × di/dt</p>

## Energy examples

| Inductor | Current | Energy |
|---|---|---|
| 10 µH SMPS inductor | 5 A | 0.125 mJ |
| 100 µH choke | 3 A | 0.45 mJ |
| 10 mH filter choke | 2 A | 20 mJ |
| Relay coil, 1 H | 30 mA | 0.45 mJ |
| Contactor coil, 5 H | 0.2 A | 100 mJ |
| Motor winding, 50 mH | 20 A | 10 J |

## Suppressing inductive kick

| Method | Release speed | Notes |
|---|---|---|
| Flyback diode | Slow | Simplest for DC coils; delays relay drop-out |
| Diode + Zener | Fast | Clamps to a set voltage |
| RC snubber | Medium | Works on AC and DC |
| Varistor (MOV) | Fast | Common on AC contactor coils |

## Saturation and core choice

Ferrite cores saturate at about 0.3–0.4 T, iron powder and silicon steel at higher flux. Gapped cores store most of the energy in the air gap, which is why SMPS inductors use them.
''')

# 10 Heat sink
page('electronics', 'heat-sink', f'''
title: Heat Sink Calculator (Thermal Resistance)
description: Calculate the maximum heat sink thermal resistance for a transistor, MOSFET or regulator from power dissipation, junction and ambient temperatures.
category: electronics
keywords: [heat sink calculator, thermal resistance calculator, heatsink selection, junction temperature calculation, rth sa, mosfet heat sink, regulator heat sink]
updated: {D}
variables:
  - {{ id: P, label: Power dissipated, family: power, unit: W, default: 10, min: 0 }}
  - {{ id: Tj, label: Maximum junction temperature (design), family: temperature, unit: C, imperialUnit: F, default: 125 }}
  - {{ id: Ta, label: Ambient temperature, family: temperature, unit: C, imperialUnit: F, default: 40 }}
  - {{ id: Rjc, label: Junction-to-case resistance (Rθjc), suffix: °C/W, default: 1.5, min: 0 }}
  - {{ id: Rcs, label: Case-to-sink resistance (Rθcs), suffix: °C/W, default: 0.5, min: 0 }}
  - {{ id: Rsa, label: Maximum heat sink resistance (Rθsa), suffix: °C/W, decimals: 2 }}
  - {{ id: Rt, label: Total junction-to-ambient allowed, suffix: °C/W, decimals: 2 }}
equations:
  - Rt = (Tj - Ta) / P
  - Rsa = Rt - Rjc - Rcs
faq:
  - q: How do I choose a heat sink?
    a: Calculate the total allowed thermal resistance, (Tj − Ta) ÷ P, subtract the device's Rθjc and the interface Rθcs, and choose a heat sink with a lower Rθsa than the result.
  - q: What if the result is negative?
    a: Even an infinite heat sink cannot keep the junction cool enough. Reduce power, use a device with lower Rθjc, or add forced air cooling.
  - q: What junction temperature should I design for?
    a: Stay 20–30 °C below the datasheet maximum (often 150 or 175 °C) for reliability — 110–125 °C is a common design target.
  - q: What is a typical case-to-sink resistance?
    a: 0.1–0.5 °C/W for a TO-220 with thermal paste; 0.5–1.5 °C/W with a silicone or mica insulating pad.
related: [physics/heat-conduction, electronics/capacitor-lifetime, electrical/three-phase-motor-power, physics/ohms-law]
{L(('heat-sink-calculation', 'Heat Sink Calculation'), ('what-is-thermal-conductivity', 'What Is Thermal Conductivity?'))}''', '''
## How to use this calculator

Enter the **power** the device dissipates, the design **junction temperature**, the **ambient temperature** inside the enclosure, and the device's **Rθjc** and interface **Rθcs**. The result is the highest heat sink thermal resistance you can use.

## The thermal circuit

<p class="formula">T<sub>j</sub> = T<sub>a</sub> + P × (R<sub>θjc</sub> + R<sub>θcs</sub> + R<sub>θsa</sub>)</p>

<p class="formula">R<sub>θsa</sub> ≤ (T<sub>j</sub> − T<sub>a</sub>) ÷ P − R<sub>θjc</sub> − R<sub>θcs</sub></p>

## Example

10 W in a TO-220 MOSFET (Rθjc 1.5 °C/W), thermal pad 0.5 °C/W, 40 °C ambient, 125 °C target:

- Total allowed = 85 ÷ 10 = 8.5 °C/W
- R<sub>θsa</sub> ≤ 8.5 − 1.5 − 0.5 = **6.5 °C/W**

## Typical package resistances

| Package | Rθjc | Rθja (no heat sink) |
|---|---|---|
| TO-92 | — | 150–200 °C/W |
| SOT-23 | — | 200–350 °C/W |
| D-PAK (on PCB copper) | 1–3 °C/W | 40–80 °C/W |
| TO-220 | 0.5–3 °C/W | 50–65 °C/W |
| TO-247 | 0.3–1 °C/W | 35–45 °C/W |

## Typical heat sinks

| Heat sink | Rθsa (natural convection) |
|---|---|
| Small clip-on TO-220 | 15–25 °C/W |
| Extruded fin, 50 mm | 4–8 °C/W |
| Extruded fin, 100 mm | 1.5–3 °C/W |
| Large finned profile | 0.5–1 °C/W |
| With fan airflow | 2–4 times lower |

Mount fins vertically for natural convection, and remember the enclosure air temperature — not room temperature — is the ambient.
''')

# 11 ADC resolution
page('electronics', 'adc-resolution', f'''
title: ADC Resolution Calculator (LSB and Step Size)
description: Calculate ADC step size (LSB), number of levels and the digital code for an input voltage from bit depth and reference voltage — including 4–20 mA PLC inputs.
category: electronics
keywords: [adc resolution calculator, lsb calculator, adc step size, bits to voltage resolution, analog to digital converter, adc counts, plc analog resolution]
updated: {D}
variables:
  - {{ id: n, label: ADC resolution, suffix: bits, default: 12, min: 1, max: 32 }}
  - {{ id: Vr, label: Full-scale (reference) voltage, family: voltage, unit: V, default: 3.3, min: 0 }}
  - {{ id: Vin, label: Input voltage, family: voltage, unit: V, default: 1.65, min: 0 }}
  - {{ id: N, label: Number of levels, min: 0, decimals: 0 }}
  - {{ id: lsb, label: Step size (1 LSB), family: voltage, unit: mV, min: 0 }}
  - {{ id: code, label: Digital output code, min: 0, decimals: 0 }}
  - {{ id: snr, label: Ideal SNR, suffix: dB, decimals: 2 }}
equations:
  - N = 2^n
  - lsb = Vr / N
  - code = min(floor(Vin / lsb), N - 1)
  - snr = 6.02 * n + 1.76
faq:
  - q: What is ADC resolution?
    a: The smallest voltage change the ADC can detect — one least significant bit (LSB) — equal to full-scale voltage ÷ 2ⁿ. A 12-bit ADC with a 3.3 V reference resolves about 0.806 mV.
  - q: What is the digital code for a voltage?
    a: Code = floor(V_in ÷ LSB). 1.65 V on a 12-bit, 3.3 V ADC gives code 2,048.
  - q: Is more bits always better?
    a: Only if noise and reference accuracy are good enough to use them. The effective number of bits (ENOB) is often 1–3 bits less than the nominal resolution.
  - q: What resolution do PLC analog inputs have?
    a: Commonly 12–16 bits. A 16-bit input on 4–20 mA resolves about 0.25 µA per count when it spans 0–21 mA across 65,536 counts.
related: [engineering/4-20ma-scaling, electronics/snr, electronics/voltage-divider, electronics/op-amp-gain]
{L(('analog-to-digital-conversion-explained', 'Analog-to-Digital Conversion Explained'), ('analog-signal-resolution-in-plc', 'Analog Signal Resolution in PLCs'), ('plc-analog-scaling-raw-count', 'PLC Analog Scaling from Raw Counts'), ('adc-working-principle-explained', 'ADC Working Principle'))}''', '''
## How to use this calculator

Enter the ADC's **resolution in bits**, the **full-scale reference voltage** and an **input voltage**. You get the number of levels, the step size, the digital code and the theoretical signal-to-noise ratio.

## The formulas

<p class="formula">LSB = V<sub>ref</sub> ÷ 2ⁿ &nbsp;·&nbsp; Code = ⌊V<sub>in</sub> ÷ LSB⌋ &nbsp;·&nbsp; SNR<sub>ideal</sub> = 6.02n + 1.76 dB</p>

## Resolution by bit depth

| Bits | Levels | LSB at 3.3 V | LSB at 5 V | LSB at 10 V |
|---|---|---|---|---|
''' + ''.join(f"| {b} | {2**b:,} | {3.3/2**b*1000:.4g} mV | {5/2**b*1000:.4g} mV | {10/2**b*1000:.4g} mV |\n" for b in [8, 10, 12, 14, 16, 24]) + '''
## 4–20 mA inputs

PLC analog cards often map 4–20 mA to a raw count range, for example:

| Card scaling | Counts per mA |
|---|---|
| 0–27,648 for 4–20 mA (Siemens S7) | 1,728 |
| 0–32,000 for 4–20 mA | 2,000 |
| 6,242–31,208 for 4–20 mA (Rockwell 16-bit) | 1,560 |

Convert counts to engineering units with the [4–20 mA scaling calculator](/engineering/4-20ma-scaling/).

## Getting the best from an ADC

- Use a stable, low-noise reference — its error appears directly in every reading.
- Filter the input below half the sample rate to prevent aliasing — see the [RC filter calculator](/electronics/rc-filter/).
- Average or oversample: averaging 4ⁿ samples adds about n bits of resolution when noise is present.
''')

# 12 SNR
page('electronics', 'snr', f'''
title: Signal-to-Noise Ratio (SNR) Calculator
description: Calculate signal-to-noise ratio in dB from signal and noise voltages or powers — with ENOB (effective number of bits) for ADCs.
category: electronics
keywords: [snr calculator, signal to noise ratio, snr in db, enob calculator, signal to noise formula, noise floor, 20 log snr]
updated: {D}
variables:
  - {{ id: Vs, label: Signal (RMS), family: voltage, unit: mV, default: 1000, min: 0 }}
  - {{ id: Vn, label: Noise (RMS), family: voltage, unit: mV, default: 1, min: 0.0000001 }}
  - {{ id: snr, label: SNR, suffix: dB, decimals: 2 }}
  - {{ id: ratio, label: Power ratio, min: 0, decimals: 0 }}
  - {{ id: enob, label: Effective number of bits (ENOB), suffix: bits, decimals: 2 }}
equations:
  - snr = 20 * log10(Vs / Vn)
  - ratio = (Vs / Vn)^2
  - enob = (snr - 1.76) / 6.02
faq:
  - q: How do I calculate SNR in dB?
    a: For voltages, SNR = 20 log₁₀(V_signal ÷ V_noise); for powers, SNR = 10 log₁₀(P_signal ÷ P_noise). Both give the same dB value.
  - q: What is a good SNR?
    a: It depends on the application. Process instrumentation and audio aim for 60–100 dB; Wi-Fi works from about 20–25 dB; 10 dB is marginal for most signals.
  - q: What is ENOB?
    a: The effective number of bits — the resolution of an ideal ADC with the same SNR. ENOB = (SINAD − 1.76) ÷ 6.02.
  - q: How can I improve SNR?
    a: Increase the signal level early in the chain, shield and twist cables, filter out-of-band noise, use differential inputs and average multiple readings.
related: [physics/decibel, electronics/adc-resolution, electronics/rc-filter, electronics/op-amp-gain]
{L(('signal-to-noise-ratio-snr-calculator', 'Signal-to-Noise Ratio (SNR) Calculator and Guide'), ('what-is-signal-integrity', 'What Is Signal Integrity?'), ('decibel-in-electronics-db-dbm', 'Decibels in Electronics: dB and dBm'))}''', '''
## How to use this calculator

Enter the **RMS signal** and **RMS noise** voltages (any matching unit). You get the SNR in dB, the power ratio and the equivalent ADC resolution (ENOB).

## The formulas

<p class="formula">SNR = 20 log₁₀(V<sub>s</sub> ÷ V<sub>n</sub>) = 10 log₁₀(P<sub>s</sub> ÷ P<sub>n</sub>)</p>

<p class="formula">ENOB = (SNR − 1.76) ÷ 6.02</p>

## SNR reference

| SNR | Voltage ratio | ENOB |
|---|---|---|
''' + ''.join(f"| {s} dB | {10**(s/20):,.0f} : 1 | {(s-1.76)/6.02:.1f} |\n" for s in [20, 40, 50, 60, 74, 86, 98, 110]) + '''
An ideal 12-bit ADC reaches 74 dB and an ideal 16-bit ADC 98 dB.

## Sources of noise

| Noise | Cause | Remedy |
|---|---|---|
| Thermal (Johnson) | Random electron motion in resistors | Lower resistance, narrower bandwidth |
| Mains hum (50/60 Hz) | Magnetic and capacitive pickup | Twisted pairs, shielding, notch or integrating ADC |
| Switching noise | SMPS, VFDs | Layout, ferrites, filtering |
| Quantisation | ADC step size | More bits, dithering |

## Thermal noise floor

A resistor's noise voltage is √(4kTRB). A 10 kΩ resistor at 25 °C over 10 kHz bandwidth produces about 1.3 µV RMS.
''')

# 13 PWM duty
page('electronics', 'pwm-duty-cycle', f'''
title: PWM Duty Cycle Calculator
description: Calculate PWM duty cycle, period, on-time and average output voltage from frequency and pulse width — for motor speed control, LEDs and microcontrollers.
category: electronics
keywords: [pwm duty cycle calculator, duty cycle formula, pwm average voltage, pulse width modulation, on time off time, pwm frequency, arduino pwm]
updated: {D}
variables:
  - {{ id: f, label: PWM frequency, family: frequency, unit: kHz, default: 1, min: 0 }}
  - {{ id: ton, label: On time (pulse width), family: seconds, unit: ms, default: 0.25, min: 0 }}
  - {{ id: V, label: Supply voltage (amplitude), family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: T, label: Period, family: seconds, unit: ms, min: 0 }}
  - {{ id: D, label: Duty cycle, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: toff, label: Off time, family: seconds, unit: ms, min: 0 }}
  - {{ id: Vav, label: Average voltage, family: voltage, unit: V, min: 0 }}
  - {{ id: Vrms, label: RMS voltage, family: voltage, unit: V, min: 0 }}
equations:
  - T = 1 / f
  - D = ton / T
  - toff = T - ton
  - Vav = D * V
  - Vrms = sqrt(D) * V
faq:
  - q: What is duty cycle?
    a: The fraction of each period that the signal is on. 0.25 ms on in a 1 ms period is a 25% duty cycle.
  - q: What is the average voltage of a PWM signal?
    a: V_avg = duty cycle × amplitude. 25% of 12 V gives 3 V average.
  - q: What PWM frequency should I use?
    a: About 20–25 kHz for DC motors to stay above hearing, a few hundred hertz or more for LED dimming to avoid visible flicker, and 50 Hz for hobby servos.
  - q: How does an 8-bit PWM value map to duty cycle?
    a: Duty = value ÷ 255. An analogWrite of 64 on an Arduino gives about 25%.
related: [electronics/555-timer, electronics/buck-converter, physics/wavelength-frequency, electronics/rc-filter]
{L(('pulse-width-modulation-duty-cycle', 'Pulse Width Modulation and Duty Cycle'), ('vfd-working-principle-explained', 'VFD Working Principle Explained'))}''', '''
## How to use this calculator

Enter the **PWM frequency**, the **on time** and the signal **amplitude**. You get the period, duty cycle, off time, and the average and RMS output voltages. To find the on time for a target duty cycle, enter the duty cycle and press × on On time.

## The formulas

<p class="formula">T = 1 ÷ f &nbsp;·&nbsp; D = t<sub>on</sub> ÷ T &nbsp;·&nbsp; V<sub>avg</sub> = D × V &nbsp;·&nbsp; V<sub>rms</sub> = √D × V</p>

## 8-bit PWM values

| Duty cycle | 8-bit value (0–255) | 10-bit value (0–1023) | Average of 12 V |
|---|---|---|---|
''' + ''.join(f"| {d}% | {round(d/100*255)} | {round(d/100*1023)} | {d/100*12:.2f} V |\n" for d in [0, 10, 25, 50, 75, 90, 100]) + '''
## Typical PWM frequencies

| Application | Frequency |
|---|---|
| Hobby servo | 50 Hz (1–2 ms pulse) |
| LED dimming | 200 Hz – 20 kHz |
| DC motor drive | 16–25 kHz |
| Switch-mode power supply | 50 kHz – 2 MHz |
| VFD output (carrier) | 2–16 kHz |

## Average vs RMS

A resistive heater cares about RMS (its power is V²/R), while a DC motor's speed follows the average voltage. At 25% duty, 12 V gives 3 V average but 6 V RMS — the heater gets 25% of full power.
''')

# 14 Buck converter
def buckL(vi, vo, f, di): return vo*(vi-vo)/(vi*f*di)
page('electronics', 'buck-converter', f'''
title: Buck Converter Calculator (Inductor and Capacitor)
description: Calculate duty cycle, inductor value, ripple current and output capacitor for a buck (step-down) DC-DC converter.
category: electronics
keywords: [buck converter calculator, buck inductor calculation, step down converter design, buck duty cycle, output capacitor ripple, dc dc converter calculator]
updated: {D}
variables:
  - {{ id: Vi, label: Input voltage, family: voltage, unit: V, default: 24, min: 0 }}
  - {{ id: Vo, label: Output voltage, family: voltage, unit: V, default: 5, min: 0 }}
  - {{ id: Io, label: Output current, family: current, unit: A, default: 2, min: 0 }}
  - {{ id: f, label: Switching frequency, family: frequency, unit: kHz, default: 500, min: 0 }}
  - {{ id: r, label: Inductor ripple (of output current), family: percent, unit: '%', default: 30, min: 0.01 }}
  - {{ id: dV, label: Allowed output ripple, family: voltage, unit: mV, default: 20, min: 0 }}
  - {{ id: D, label: Duty cycle (ideal), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: dI, label: Ripple current (peak-to-peak), family: current, unit: A, min: 0 }}
  - {{ id: L, label: Inductance required, family: inductance, unit: uH, min: 0 }}
  - {{ id: Ipk, label: Peak inductor current, family: current, unit: A, min: 0 }}
  - {{ id: C, label: Output capacitance (min.), family: capacitance, unit: uF, min: 0 }}
equations:
  - D = Vo / Vi
  - dI = r * Io
  - L = Vo * (Vi - Vo) / (Vi * f * dI)
  - Ipk = Io + dI / 2
  - C = dI / (8 * f * dV)
faq:
  - q: What is the duty cycle of a buck converter?
    a: Ideally D = V_out ÷ V_in. Converting 24 V to 5 V needs about 21%; losses push it slightly higher.
  - q: How do I choose the inductor ripple?
    a: 20–40% of the output current is a common compromise between inductor size and ripple. 30% is a good starting point.
  - q: How is the inductance calculated?
    a: L = V_out × (V_in − V_out) ÷ (V_in × f × ΔI). For 24 V to 5 V at 2 A, 500 kHz and 30% ripple, L ≈ 13 µH.
  - q: What sets the output ripple voltage?
    a: Capacitance and the capacitor's ESR. The formula here covers capacitance; with electrolytics, ripple is usually dominated by ESR × ΔI.
related: [electronics/boost-converter, electronics/inductor-energy, electronics/pwm-duty-cycle, electronics/capacitor-energy]
{L(('buck-converter-working-principle', 'Buck Converter Working Principle'), ('synchronous-rectification-buck-converter', 'Synchronous Rectification in Buck Converters'), ('capacitor-esr-equivalent-series-resistance', 'Capacitor ESR (Equivalent Series Resistance)'))}''', f'''
## How to use this calculator

Enter the **input** and **output voltage**, **output current**, **switching frequency**, the **inductor ripple** as a percentage of output current, and the allowed **output voltage ripple**. You get the duty cycle, ripple current, inductance, peak inductor current and minimum output capacitance.

## The formulas (continuous conduction)

| Quantity | Formula |
|---|---|
| Duty cycle | D = V<sub>o</sub> ÷ V<sub>i</sub> |
| Inductance | L = V<sub>o</sub>(V<sub>i</sub> − V<sub>o</sub>) ÷ (V<sub>i</sub> f ΔI) |
| Peak current | I<sub>pk</sub> = I<sub>o</sub> + ΔI ÷ 2 |
| Output capacitance | C = ΔI ÷ (8 f ΔV) |

## Example

24 V to 5 V at 2 A, 500 kHz, 30% ripple (0.6 A):

- D = **20.8%**
- L = 5 × 19 ÷ (24 × 500,000 × 0.6) = **{buckL(24,5,500e3,0.6)*1e6:.1f} µH** → use 15 µH
- Peak current = **2.3 A** — choose an inductor rated above this for saturation
- For 20 mV ripple, C ≥ 0.6 ÷ (8 × 500,000 × 0.02) = **7.5 µF** → use 22 µF ceramic

## Inductance vs frequency (24 V → 5 V, 0.6 A ripple)

| Frequency | Inductance |
|---|---|
''' + ''.join(f"| {fl} | {buckL(24,5,fv,0.6)*1e6:.1f} µH |\n" for fl, fv in [('100 kHz', 100e3), ('250 kHz', 250e3), ('500 kHz', 500e3), ('1 MHz', 1e6), ('2 MHz', 2e6)]) + '''
Higher frequency allows smaller inductors and capacitors but increases switching losses.

## Design checks

- Inductor saturation current above I<sub>pk</sub> with margin; RMS rating above I<sub>o</sub>.
- Input capacitor sized for RMS ripple current ≈ I<sub>o</sub>√(D(1 − D)).
- Use the controller datasheet's compensation and layout guidance — tight loops around the switch, diode and input capacitor matter most.
''')

# 15 Boost converter
page('electronics', 'boost-converter', f'''
title: Boost Converter Calculator (Inductor and Capacitor)
description: Calculate duty cycle, input current, inductor value and output capacitor for a boost (step-up) DC-DC converter.
category: electronics
keywords: [boost converter calculator, boost inductor calculation, step up converter design, boost duty cycle, boost converter formula, dc dc boost]
updated: {D}
variables:
  - {{ id: Vi, label: Input voltage, family: voltage, unit: V, default: 5, min: 0 }}
  - {{ id: Vo, label: Output voltage, family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: Io, label: Output current, family: current, unit: A, default: 0.5, min: 0 }}
  - {{ id: eta, label: Efficiency, family: percent, unit: '%', default: 90, min: 0.01, max: 1 }}
  - {{ id: f, label: Switching frequency, family: frequency, unit: kHz, default: 500, min: 0 }}
  - {{ id: r, label: Inductor ripple (of input current), family: percent, unit: '%', default: 30, min: 0.01 }}
  - {{ id: dV, label: Allowed output ripple, family: voltage, unit: mV, default: 50, min: 0 }}
  - {{ id: D, label: Duty cycle, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: Ii, label: Input (average inductor) current, family: current, unit: A, min: 0 }}
  - {{ id: L, label: Inductance required, family: inductance, unit: uH, min: 0 }}
  - {{ id: Ipk, label: Peak switch current, family: current, unit: A, min: 0 }}
  - {{ id: C, label: Output capacitance (min.), family: capacitance, unit: uF, min: 0 }}
equations:
  - D = 1 - Vi * eta / Vo
  - Ii = Vo * Io / (Vi * eta)
  - L = Vi * D / (f * r * Ii)
  - Ipk = Ii * (1 + r / 2)
  - C = Io * D / (f * dV)
faq:
  - q: What is the duty cycle of a boost converter?
    a: D = 1 − V_in × η ÷ V_out. Boosting 5 V to 12 V at 90% efficiency needs a duty cycle of about 62.5%.
  - q: How much input current does a boost converter draw?
    a: I_in = V_out × I_out ÷ (V_in × η). 12 V at 0.5 A from 5 V at 90% efficiency draws about 1.33 A.
  - q: How high can a boost converter step up?
    a: Practically about 5–8 times. Very high duty cycles cause large losses and control problems.
  - q: Why is the output ripple larger than a buck's?
    a: The output capacitor alone supplies the load while the switch is on, so the output current is pulsed.
related: [electronics/buck-converter, electronics/inductor-energy, electronics/pwm-duty-cycle, electronics/capacitor-energy]
{L(('boost-converter-working-principle', 'Boost Converter Working Principle'), ('pfc-circuit-boost-power-factor-correction', 'PFC Circuit: Boost Power Factor Correction'), ('sepic-converter-working-design', 'SEPIC Converter Working and Design'))}''', '''
## How to use this calculator

Enter the **input** and **output voltage**, **output current**, expected **efficiency**, **switching frequency**, inductor **ripple** and allowed **output ripple**. You get the duty cycle, input current, inductance, peak switch current and minimum output capacitance.

## The formulas (continuous conduction)

| Quantity | Formula |
|---|---|
| Duty cycle | D = 1 − V<sub>i</sub>η ÷ V<sub>o</sub> |
| Input current | I<sub>i</sub> = V<sub>o</sub>I<sub>o</sub> ÷ (V<sub>i</sub>η) |
| Inductance | L = V<sub>i</sub> D ÷ (f ΔI) |
| Output capacitance | C = I<sub>o</sub> D ÷ (f ΔV) |

## Example

5 V to 12 V at 0.5 A, 90% efficiency, 500 kHz, 30% ripple:

- D = 1 − 4.5 ÷ 12 = **62.5%**
- Input current = 6 ÷ 4.5 = **1.33 A**
- ΔI = 0.4 A, L = 5 × 0.625 ÷ (500,000 × 0.4) = **15.6 µH** → use 15–22 µH
- Peak switch current = **1.53 A**
- For 50 mV ripple, C ≥ 0.5 × 0.625 ÷ (500,000 × 0.05) = **12.5 µF**

## Design checks

- The switch and diode must handle the full output voltage plus spikes.
- Inductor saturation current must exceed the peak current.
- A boost converter has no short-circuit protection by itself — current flows straight from input to output through the inductor and diode.
- At very light loads the converter enters discontinuous mode, and the formulas above no longer apply.

## Related topologies

- **Buck-boost and SEPIC** give an output above or below the input.
- **PFC boost stages** in power supplies shape input current to follow the mains voltage.
''')

# 16 Wheatstone bridge
page('electronics', 'wheatstone-bridge', f'''
title: Wheatstone Bridge Calculator
description: Calculate the output voltage of a Wheatstone bridge, or the unknown resistance at balance — for strain gauges, RTDs and sensor circuits.
category: electronics
keywords: [wheatstone bridge calculator, bridge circuit calculator, unknown resistance, bridge output voltage, balanced bridge, strain gauge bridge, quarter bridge]
updated: {D}
variables:
  - {{ id: Vs, label: Excitation voltage, family: voltage, unit: V, default: 10, min: 0 }}
  - {{ id: R1, label: R1 (top left), family: resistance, unit: ohm, default: 1000, min: 0 }}
  - {{ id: R2, label: R2 (bottom left), family: resistance, unit: ohm, default: 1000, min: 0 }}
  - {{ id: R3, label: R3 (top right), family: resistance, unit: ohm, default: 1000, min: 0 }}
  - {{ id: Rx, label: Rx (bottom right, unknown), family: resistance, unit: ohm, default: 1010, min: 0 }}
  - {{ id: Vo, label: Bridge output voltage, family: voltage, unit: mV }}
  - {{ id: Rb, label: Rx for balance, family: resistance, unit: ohm, min: 0 }}
equations:
  - Vo = Vs * (Rx / (R3 + Rx) - R2 / (R1 + R2))
  - Rb = R3 * R2 / R1
faq:
  - q: What is the balance condition of a Wheatstone bridge?
    a: The output is zero when R1 ÷ R2 = R3 ÷ Rx, so Rx = R3 × R2 ÷ R1.
  - q: How does a Wheatstone bridge measure small changes?
    a: At balance the output is zero, so a small change in one resistor produces a small voltage that can be amplified, without a large fixed offset.
  - q: What is a quarter, half and full bridge?
    a: The number of active sensing elements — one, two or four. A full bridge with four strain gauges gives four times the output of a quarter bridge and better temperature compensation.
  - q: Is the output linear?
    a: Only approximately for small changes. For large changes, use the exact formula here.
related: [electronics/voltage-divider, engineering/pt100-resistance, physics/resistors-series-parallel, electronics/op-amp-gain]
{L(('wheatstone-bridge-10-applications', 'Wheatstone Bridge: 10 Applications'),)}''', '''
## How to use this calculator

Enter the **excitation voltage** and the four resistances. The calculator gives the bridge output voltage (between the two midpoints) and the value of Rx that would balance the bridge.

## The formulas

<p class="formula">V<sub>out</sub> = V<sub>s</sub> × [R<sub>x</sub> ÷ (R₃ + R<sub>x</sub>) − R₂ ÷ (R₁ + R₂)]</p>

<p class="formula">Balance: R<sub>x</sub> = R₃ × R₂ ÷ R₁</p>

## Example: 1% change in a quarter bridge

All arms 1,000 Ω, Rx = 1,010 Ω, 10 V excitation:

V<sub>out</sub> = 10 × (1,010 ÷ 2,010 − 0.5) = **24.9 mV**

## Output vs resistance change (10 V, 1 kΩ arms)

| ΔR/R | Quarter bridge | Full bridge (4 active arms) |
|---|---|---|
''' + ''.join(f"| {d}% | {10*((1+d/100)/(2+d/100)-0.5)*1000:.2f} mV | {10*d/100*1000:.1f} mV |\n" for d in [0.01, 0.1, 0.5, 1, 2, 5]) + '''
## Applications

- **Strain gauges and load cells**: tiny resistance changes from strain.
- **RTD measurement**: three-wire bridge circuits cancel lead resistance — see the [Pt100 calculator](/engineering/pt100-resistance/).
- **Pressure sensors**: piezoresistive silicon bridges inside most pressure transmitters.
- **Gas sensors** and hot-wire anemometers.

## Strain gauge output

For a quarter bridge, V<sub>out</sub> ≈ V<sub>s</sub> × GF × ε ÷ 4, where GF ≈ 2 for metal foil gauges. 1,000 µε at 10 V gives about 5 mV.
''')

# 17 Capacitor lifetime
def clife(L0, T0, T): return L0*2**((T0-T)/10)
page('electronics', 'capacitor-lifetime', f'''
title: Electrolytic Capacitor Life Calculator (10 °C Rule)
description: Estimate the expected life of an aluminium electrolytic capacitor at your operating temperature from its rated hours and temperature, using the 10-degree rule.
category: electronics
keywords: [capacitor life calculator, electrolytic capacitor lifetime, capacitor life expectancy, 10 degree rule, arrhenius capacitor, capacitor hours at temperature]
updated: {D}
variables:
  - {{ id: L0, label: Rated life, family: seconds, unit: h, default: 2000, min: 0 }}
  - {{ id: T0, label: Rated temperature, suffix: °C, default: 105 }}
  - {{ id: T, label: Actual core temperature, suffix: °C, default: 55 }}
  - {{ id: Lx, label: Expected life, family: seconds, unit: h, min: 0 }}
  - {{ id: y, label: Expected life in years (24/7), min: 0, decimals: 1 }}
equations:
  - Lx = L0 * 2^((T0 - T) / 10)
  - y = Lx / 3600 / 8760
faq:
  - q: What is the 10-degree rule for capacitors?
    a: The life of an aluminium electrolytic capacitor roughly doubles for every 10 °C drop in its core temperature, because electrolyte evaporation follows the Arrhenius law.
  - q: How long will a 2,000-hour, 105 °C capacitor last at 55 °C?
    a: 2,000 × 2⁵ = 64,000 hours, or about 7.3 years of continuous use.
  - q: Should I use ambient or core temperature?
    a: Core (hotspot) temperature — ambient plus self-heating from ripple current. Many manufacturers also include a ripple current factor.
  - q: Does voltage affect life?
    a: Less than temperature for most aluminium electrolytics. Some manufacturers add a factor for operating below rated voltage.
related: [electronics/heat-sink, electronics/capacitor-energy, chemistry/arrhenius-equation, electronics/buck-converter]
{L(('electrolytic-capacitor-lifetime-calculation', 'Electrolytic Capacitor Lifetime Calculation'), ('electrolytic-vs-ceramic-vs-tantalum-capacitor-failure-modes', 'Electrolytic vs Ceramic vs Tantalum Capacitor Failure Modes'), ('capacitor-esr-equivalent-series-resistance', 'Capacitor ESR Explained'))}''', '''
## How to use this calculator

Enter the capacitor's **rated life** and **rated temperature** from the datasheet (for example 2,000 h at 105 °C), and the **actual core temperature** in your circuit. You get the expected life in hours and years of continuous operation.

## The formula

<p class="formula">L = L₀ × 2<sup>(T₀ − T) ÷ 10</sup></p>

## Life at different temperatures

| Core temperature | 1,000 h @ 85 °C | 2,000 h @ 105 °C | 5,000 h @ 105 °C | 10,000 h @ 105 °C |
|---|---|---|---|---|
''' + ''.join(f"| {T} °C | {clife(1000,85,T):,.0f} h | {clife(2000,105,T):,.0f} h | {clife(5000,105,T):,.0f} h | {clife(10000,105,T):,.0f} h |\n" for T in [85, 75, 65, 55, 45, 40]) + '''
One year of continuous use is 8,760 hours. Manufacturers often cap estimates at 15 years because of seal ageing.

## Extending capacitor life

- Keep capacitors away from heat sinks, resistors and transformers.
- Choose 105 °C, long-life series for power supplies and drives.
- Stay within the ripple current rating — ripple heats the core.
- Improve enclosure ventilation; every 10 °C counts double.

## Why it matters

Electrolytic capacitors are the most common wear-out part in power supplies, VFDs and UPSs. Rising ESR and falling capacitance are early warning signs, which is why drive makers recommend replacing DC-bus capacitors on a schedule.
''')

# 18 PCB trace width
def tw(I, dT, oz, k): A = (I/(k*dT**0.44))**(1/0.725); return A/(1.378*oz)
page('electronics', 'pcb-trace-width', f'''
title: PCB Trace Width Calculator (IPC-2221)
description: Calculate the PCB trace width needed for a current and temperature rise using the IPC-2221 formula — for external and internal layers and copper weights.
category: electronics
keywords: [pcb trace width calculator, ipc 2221 calculator, trace current capacity, pcb track width, copper thickness oz, trace temperature rise, pcb current carrying]
updated: {D}
variables:
  - {{ id: I, label: Current, family: current, unit: A, default: 3, min: 0 }}
  - {{ id: dT, label: Allowed temperature rise, suffix: °C, default: 10, min: 0.1 }}
  - {{ id: oz, label: Copper weight, suffix: oz/ft², default: 1, min: 0.1 }}
  - id: k
    label: Layer
    default: 0.048
    options:
      - {{ label: External (outer) layer, value: 0.048 }}
      - {{ label: Internal layer, value: 0.024 }}
  - {{ id: A, label: Cross-section area, suffix: mil², min: 0, decimals: 1 }}
  - {{ id: w, label: Minimum trace width, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: wm, label: Minimum trace width in mils, suffix: mil, min: 0, decimals: 1 }}
equations:
  - A = (I / (k * dT^0.44))^(1 / 0.725)
  - wm = A / (1.378 * oz)
  - w = wm * 0.0000254
faq:
  - q: How wide should a PCB trace be for 1 A?
    a: On an outer layer with 1 oz copper and a 10 °C rise, IPC-2221 gives about 0.3 mm (12 mil). Inner layers need about 2.6 times the width.
  - q: Why do inner layers need wider traces?
    a: Inner layers are surrounded by FR-4, which conducts heat poorly, so they cannot shed heat as well as outer layers.
  - q: What does 1 oz copper mean?
    a: 1 ounce of copper spread over 1 square foot — a thickness of about 35 µm (1.378 mil).
  - q: Is IPC-2221 accurate?
    a: It is conservative for most designs. The newer IPC-2152 standard uses more detailed data that accounts for planes and board thickness.
related: [electrical/cable-voltage-drop, physics/ohms-law, electronics/heat-sink, electronics/led-resistor]
{L(('pcb-via-current-capacity', 'PCB Via Current Capacity (IPC-2152)'), ('controlled-impedance-pcb-traces', 'Controlled Impedance PCB Traces'))}''', '''
## How to use this calculator

Enter the **current**, the allowed **temperature rise** above ambient, the **copper weight** and whether the trace is on an **external or internal layer**. You get the required cross-section and minimum width in millimetres and mils.

## The IPC-2221 formula

<p class="formula">I = k × ΔT<sup>0.44</sup> × A<sup>0.725</sup></p>

with A in square mils, k = 0.048 for external layers and 0.024 for internal layers. Width = A ÷ (1.378 × copper oz).

## Trace width for 1 oz copper, 10 °C rise

| Current | External layer | Internal layer |
|---|---|---|
''' + ''.join(f"| {I} A | {tw(I,10,1,0.048)*0.0254:.2f} mm ({tw(I,10,1,0.048):.0f} mil) | {tw(I,10,1,0.024)*0.0254:.2f} mm ({tw(I,10,1,0.024):.0f} mil) |\n" for I in [0.5, 1, 2, 3, 5, 10]) + '''
## Copper weights

| Copper | Thickness |
|---|---|
| 0.5 oz | 17.5 µm |
| 1 oz | 35 µm |
| 2 oz | 70 µm |
| 3 oz | 105 µm |

Doubling copper weight roughly halves the width needed.

## Other checks

- **Voltage drop**: long, thin traces drop voltage. 1 oz copper has about 0.5 mΩ per square.
- **Vias**: a standard 0.3 mm via carries roughly 1–2 A; use several vias in parallel for high currents.
- **Spacing**: high-voltage traces need clearance and creepage per IPC-2221 or IEC 60664.
''')
print('D2 done')
