import sys, math, os, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
D = '2026-11-06'
pi = math.pi
F = 96485.33212; R = 8.314462618
DESC = []
def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    t = re.search(r'^intro: (.*)$', fm, re.M).group(1)
    DESC.append(slug)
    page(cat, slug, fm, body)

# ======================================================================= ELECTRONICS

# ---------------------------------------------------------------- Summing amplifier
sV = (1.0, 0.5, -0.2); sR = (10e3, 10e3, 20e3); sRf = 10e3
sVo = -sRf * sum(v / r for v, r in zip(sV, sR))
dac_rows = ''
for code in (1, 2, 4, 8, 5, 10, 15):
    bits = [(code >> (3 - i)) & 1 for i in range(4)]       # MSB first
    vo = -10e3 * sum(b * 5.0 / (10e3 * 2 ** i) for i, b in enumerate(bits))
    dac_rows += f"| {code} | {''.join(map(str, bits))} | {vo:.4f} V |\n"
P('electronics', 'summing-amplifier', f'''
title: Summing Amplifier Calculator (Inverting Op-Amp Adder)
description: Calculate the output voltage of an inverting op-amp summing amplifier from up to three input voltages, input resistors and the feedback resistor.
category: electronics
{intro("An inverting summing amplifier adds several input voltages, each weighted by the ratio of the feedback resistor to its own input resistor, because the inverting input sits at a virtual ground. This summing amplifier calculator gives the output voltage and input current for three inputs — the circuit builds on the [inverting amplifier gain formula](ib:inverting-amplifier-gain-formula) covered in [op-amp basics](ib:operational-amplifier-op-amp-basics).")}
keywords: [summing amplifier calculator, op amp summing amplifier, inverting summing amplifier formula, op amp adder calculator, summing amplifier output voltage, audio mixer op amp]
updated: {D}
variables:
  - {{ id: V1, label: Input voltage V₁, family: voltage, unit: V, default: {sV[0]:g} }}
  - {{ id: R1, label: Input resistor R₁, family: resistance, unit: kohm, default: {sR[0]/1e3:g}, min: 0 }}
  - {{ id: V2, label: Input voltage V₂, family: voltage, unit: V, default: {sV[1]:g} }}
  - {{ id: R2, label: Input resistor R₂, family: resistance, unit: kohm, default: {sR[1]/1e3:g}, min: 0 }}
  - {{ id: V3, label: Input voltage V₃, family: voltage, unit: V, default: {sV[2]:g} }}
  - {{ id: R3, label: Input resistor R₃, family: resistance, unit: kohm, default: {sR[2]/1e3:g}, min: 0 }}
  - {{ id: Rf, label: Feedback resistor R_f, family: resistance, unit: kohm, default: {sRf/1e3:g}, min: 0 }}
  - {{ id: Iin, label: Total current into the summing node, family: current, unit: mA }}
  - {{ id: Vout, label: Output voltage, family: voltage, unit: V }}
equations:
  - Iin = V1 / R1 + V2 / R2 + V3 / R3
  - Vout = -Rf * Iin
faq:
  - q: What is the formula for an inverting summing amplifier?
    a: Vout = −R_f × (V₁/R₁ + V₂/R₂ + V₃/R₃). With all resistors equal it is simply −(V₁ + V₂ + V₃).
  - q: Why is the output negative?
    a: The inputs drive the inverting terminal, so the sum is inverted. Follow it with a unity-gain inverting stage, or use a non-inverting summing circuit, if you need a positive sum.
  - q: Do the inputs interact with each other?
    a: No. The inverting input is held at virtual ground, so each input current depends only on its own voltage and resistor. That isolation is why the circuit is used in audio mixers.
  - q: What limits the output?
    a: The op-amp supply rails. The result is only valid while |Vout| stays below the output swing limit — typically 1–2 V inside the rails, or close to the rails for rail-to-rail parts.
related: [electronics/op-amp-gain, electronics/differential-amplifier, electronics/op-amp-integrator, electronics/voltage-divider]
''', f'''
## How to use the summing amplifier calculator

Enter up to three **input voltages** with their **input resistors**, and the **feedback resistor**. Set an unused input voltage to 0. The calculator returns the current into the summing node and the output voltage. To weight the inputs equally, make all input resistors the same; to scale the sum, change R<sub>f</sub>.

## Summing amplifier formula

<p class="formula">V<sub>out</sub> = −R<sub>f</sub> (V₁/R₁ + V₂/R₂ + V₃/R₃)</p>

Each input contributes a gain of −R<sub>f</sub>/R<sub>n</sub>. Choose the non-inverting input resistor (to ground) ≈ R₁ ∥ R₂ ∥ R₃ ∥ R<sub>f</sub> to cancel bias-current offset in bipolar op-amps.

## Worked example

V₁ = 1 V and V₂ = 0.5 V through 10 kΩ, V₃ = −0.2 V through 20 kΩ, R<sub>f</sub> = 10 kΩ:

- Current = 1/10k + 0.5/10k − 0.2/20k = **{sum(v / r for v, r in zip(sV, sR))*1e3:.2f} mA**
- V<sub>out</sub> = −10 kΩ × {sum(v / r for v, r in zip(sV, sR))*1e3:.2f} mA = **{sVo:.2f} V**

## Binary-weighted 4-bit DAC (5 V logic, R = 10 kΩ, 2R, 4R, 8R, R<sub>f</sub> = 10 kΩ)

| Code | Bits | Output |
|---|---|---|
{dac_rows}
A summing amplifier with binary-weighted input resistors is the simplest digital-to-analogue converter; practical DACs use an R-2R ladder because it needs only two resistor values.

## Design notes

- Keep input resistors in the 1 kΩ–100 kΩ range: lower values load the sources, higher values add noise and offset.
- For a **mixer**, use equal input resistors and a potentiometer in series with each input.
- An **averaging amplifier** uses R<sub>f</sub> = R/N for N equal inputs.
''')

# ---------------------------------------------------------------- Differential amplifier
dV1, dV2, dR1, dR2, dR3, dR4 = 1.0, 1.2, 10e3, 100e3, 10e3, 100e3
da = dR4 / (dR3 + dR4) * (1 + dR2 / dR1); db = dR2 / dR1
dVo = da * dV2 - db * dV1
cm_rows = ''
for G in (1, 10, 100):
    cm_rows += f"| {G} | " + ' | '.join(f"{20*math.log10((1+G)/(4*t)):.0f} dB" for t in (0.05, 0.01, 0.001, 0.0001)) + " |\n"
P('electronics', 'differential-amplifier', f'''
title: Differential Amplifier Calculator (Op-Amp Subtractor)
description: Calculate the output voltage, differential gain and common-mode gain of a four-resistor op-amp differential amplifier (subtractor) from V1, V2 and R1–R4.
category: electronics
{intro("A differential amplifier amplifies the difference between two voltages while rejecting what they have in common — the classic four-resistor op-amp subtractor. This differential amplifier calculator gives the output voltage, differential gain and common-mode gain for any resistor values, so you can see how resistor mismatch spoils the CMRR described in [differential amplifier basics and CMRR](ib:differential-amplifier-explained-basics-and-cmrr).")}
keywords: [differential amplifier calculator, op amp differential amplifier formula, subtractor circuit calculator, difference amplifier gain, common mode gain, cmrr resistor mismatch, op amp subtractor]
updated: {D}
variables:
  - {{ id: V1, label: Voltage at inverting side V₁, family: voltage, unit: V, default: {dV1:g} }}
  - {{ id: V2, label: Voltage at non-inverting side V₂, family: voltage, unit: V, default: {dV2:g} }}
  - {{ id: R1, label: R₁ (V₁ to inverting input), family: resistance, unit: kohm, default: {dR1/1e3:g}, min: 0 }}
  - {{ id: R2, label: R₂ (feedback), family: resistance, unit: kohm, default: {dR2/1e3:g}, min: 0 }}
  - {{ id: R3, label: R₃ (V₂ to non-inverting input), family: resistance, unit: kohm, default: {dR3/1e3:g}, min: 0 }}
  - {{ id: R4, label: R₄ (non-inverting input to ground), family: resistance, unit: kohm, default: {dR4/1e3:g}, min: 0 }}
  - {{ id: Vout, label: Output voltage, family: voltage, unit: V }}
  - {{ id: Ad, label: Differential gain, decimals: 4 }}
  - {{ id: Acm, label: Common-mode gain, decimals: 5 }}
equations:
  - Vout = R4 / (R3 + R4) * (1 + R2 / R1) * V2 - R2 / R1 * V1
  - Ad = (R4 / (R3 + R4) * (1 + R2 / R1) + R2 / R1) / 2
  - Acm = R4 / (R3 + R4) * (1 + R2 / R1) - R2 / R1
faq:
  - q: What is the differential amplifier formula?
    a: In general Vout = V₂·R₄/(R₃+R₄)·(1 + R₂/R₁) − V₁·R₂/R₁. With R₁ = R₃ and R₂ = R₄ it reduces to Vout = (R₂/R₁)(V₂ − V₁).
  - q: What is common-mode gain?
    a: The gain for a voltage applied equally to both inputs. It is zero when R₂/R₁ = R₄/R₃ exactly; any resistor mismatch lets some common-mode voltage through.
  - q: How does resistor tolerance affect CMRR?
    a: Worst-case CMRR ≈ (1 + G) ÷ (4t), where t is the resistor tolerance. With 1% resistors and a gain of 1 that is only about 34 dB, so precision work uses 0.1% or matched networks.
  - q: When should I use an instrumentation amplifier instead?
    a: When the sources have high or unequal impedance (bridges, thermocouples) — the four-resistor circuit loads the inputs with R₁ and R₃+R₄, unlike an in-amp's buffered inputs.
related: [electronics/instrumentation-amplifier-gain, electronics/op-amp-gain, electronics/summing-amplifier, electronics/wheatstone-bridge]
''', f'''
## How to use the differential amplifier calculator

Enter the two input voltages and the four resistors. **R₁** and **R₂** set the inverting gain; **R₃** and **R₄** form the divider on the non-inverting input. The calculator returns the output, the differential gain and the common-mode gain — try changing R₄ by 1% to see how mismatch creates common-mode error.

## Differential amplifier formula

<p class="formula">V<sub>out</sub> = V₂ · R₄/(R₃ + R₄) · (1 + R₂/R₁) − V₁ · R₂/R₁</p>

<p class="formula">Matched (R₁ = R₃, R₂ = R₄): V<sub>out</sub> = (R₂/R₁)(V₂ − V₁)</p>

Writing V<sub>out</sub> = A<sub>d</sub>(V₂ − V₁) + A<sub>cm</sub>(V₁ + V₂)/2 separates the wanted differential gain from the unwanted common-mode gain.

## Worked example

V₁ = {dV1:g} V, V₂ = {dV2:g} V, R₁ = R₃ = 10 kΩ, R₂ = R₄ = 100 kΩ:

- V<sub>out</sub> = {dV2:g} × (100/110) × 11 − {dV1:g} × 10 = **{dVo:.2f} V**
- Differential gain = **{(da+db)/2:g}**, common-mode gain = **{da-db:g}**

## Worst-case CMRR from resistor tolerance

| Gain | 5% | 1% | 0.1% | 0.01% |
|---|---|---|---|---|
{cm_rows}
Values from CMRR ≈ (1 + G)/(4t); the op-amp's own CMRR sets a further limit.

## Notes

- The input impedance is R₁ at the V₁ input and R₃ + R₄ at the V₂ input — drive it from low-impedance sources.
- For a reference offset, connect the bottom of R₄ to a reference voltage instead of ground; it adds directly to the output.
''')

# ---------------------------------------------------------------- Op-amp integrator
iVin, iR, iC, it, iV0, if_ = 1.0, 10e3, 100e-9, 1e-3, 0.0, 1000.0
iRC = iR * iC; iramp = -iVin / iRC; iVo = iV0 + iramp * it; if0 = 1 / (2 * pi * iRC)
int_rows = ''
for f in (10, 100, if0, 1e3, 10e3):
    g = 1 / (2 * pi * f * iRC)
    int_rows += f"| {f:,.1f} Hz | {g:.4g} | {20*math.log10(g):.1f} dB | 90° lead (inverted: −90° + 180°) |\n"
P('electronics', 'op-amp-integrator', f'''
title: Op-Amp Integrator Calculator (Ramp Rate & Unity-Gain Frequency)
description: Calculate the output ramp rate, output voltage after a time, unity-gain frequency and AC gain of an inverting op-amp integrator from R, C and input voltage.
category: electronics
{intro("An op-amp integrator charges a feedback capacitor with a current set by the input resistor, so a constant input produces a linear ramp and a sine input is attenuated by 20 dB per decade. This op-amp integrator calculator gives the ramp rate, the output after a chosen time and the unity-gain frequency — see the [op-amp integrator and differentiator](ib:op-amp-integrator-differentiator) explained.")}
keywords: [op amp integrator calculator, integrator circuit formula, op amp integrator output voltage, integrator ramp rate, unity gain frequency integrator, rc integrator op amp, miller integrator]
updated: {D}
variables:
  - {{ id: Vin, label: Input voltage (constant), family: voltage, unit: V, default: {iVin:g} }}
  - {{ id: R, label: Input resistor R, family: resistance, unit: kohm, default: {iR/1e3:g}, min: 0 }}
  - {{ id: C, label: Feedback capacitor C, family: capacitance, unit: nF, default: {iC*1e9:g}, min: 0 }}
  - {{ id: t, label: Integration time, family: seconds, unit: ms, default: {it*1e3:g}, min: 0 }}
  - {{ id: V0, label: Initial output voltage, family: voltage, unit: V, default: {iV0:g} }}
  - {{ id: f, label: Signal frequency (for AC gain), family: frequency, unit: Hz, default: {if_:g}, min: 0 }}
  - {{ id: k, label: Output ramp rate, suffix: V/s }}
  - {{ id: Vout, label: Output voltage after time t, family: voltage, unit: V }}
  - {{ id: f0, label: Unity-gain frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: G, label: AC gain magnitude at f, min: 0, decimals: 4 }}
equations:
  - k = -Vin / (R * C)
  - Vout = V0 + k * t
  - f0 = 1 / (2 * pi * R * C)
  - G = 1 / (2 * pi * f * R * C)
faq:
  - q: What is the output of an op-amp integrator?
    a: Vout(t) = V₀ − (1/RC)∫Vin dt. For a constant input that is a straight ramp of slope −Vin/(RC) volts per second.
  - q: What is the unity-gain frequency of an integrator?
    a: f₀ = 1/(2πRC). Below f₀ the gain is greater than one, above it less, falling at 20 dB per decade.
  - q: Why does a practical integrator need a resistor across the capacitor?
    a: Without it the DC gain is the op-amp's open-loop gain, so input offset voltage and bias current slowly drive the output into the rail. A resistor R_f in parallel with C limits DC gain to −R_f/R, at the cost of integrating only above 1/(2πR_fC).
  - q: Where are integrators used?
    a: In the I term of analogue PID controllers, triangle-wave and ramp generators, dual-slope ADCs, active filters and charge amplifiers.
related: [electronics/rc-filter, electronics/op-amp-gain, physics/rc-time-constant, electronics/summing-amplifier]
''', f'''
## How to use the op-amp integrator calculator

Enter the **input voltage**, the **input resistor** and the **feedback capacitor**. Add an **integration time** to see where the ramp has reached, and an **initial output voltage** if the capacitor is not discharged. The **signal frequency** gives the AC gain for sine-wave inputs.

## Op-amp integrator formula

<p class="formula">V<sub>out</sub>(t) = V₀ − (1/RC) ∫ V<sub>in</sub> dt &nbsp;·&nbsp; constant input: V<sub>out</sub> = V₀ − V<sub>in</sub> t / RC</p>

<p class="formula">|G| = 1 / (2π f R C) &nbsp;·&nbsp; f₀ = 1 / (2π R C)</p>

## Worked example

1 V input, R = 10 kΩ, C = 100 nF (RC = {iRC*1e3:g} ms):

- Ramp rate = −1 ÷ {iRC:g} = **{iramp:,.0f} V/s**
- After 1 ms the output has moved to **{iVo:.2f} V**
- Unity-gain frequency f₀ = **{if0:.2f} Hz**; at 1 kHz the gain is **{1/(2*pi*1e3*iRC):.4f}**

## Gain vs frequency (R = 10 kΩ, C = 100 nF)

| Frequency | Gain | Gain (dB) | Phase |
|---|---|---|---|
{int_rows}
## Design notes

- The output can only ramp until it reaches the op-amp's output swing limit; reset the capacitor with a switch for repeating ramps.
- Use a low-leakage film (C0G, polypropylene) capacitor — electrolytics leak and drift.
- For a square-wave input the integrator produces a triangle wave of peak-to-peak amplitude V<sub>in</sub> T/(2RC) for a symmetric ±V<sub>in</sub> square of period T.
''')

# ---------------------------------------------------------------- Sallen-Key low-pass
kR1, kR2, kC1, kC2, kf = 10e3, 10e3, 22e-9, 10e-9, 5000.0
kfc = 1 / (2 * pi * math.sqrt(kR1 * kR2 * kC1 * kC2)); kQ = math.sqrt(kR1 * kR2 * kC1 * kC2) / (kC2 * (kR1 + kR2))
def skH(f, fc, Q): x = f / fc; return 1 / math.sqrt((1 - x * x) ** 2 + (x / Q) ** 2)
kH = skH(kf, kfc, kQ)
q_rows = ''
for name, Q in (('Critically damped', 0.5), ('Bessel', 1 / math.sqrt(3)), ('Butterworth', 1 / math.sqrt(2)), ('Q = 1', 1.0), ('Chebyshev 1 dB ripple', 0.9565)):
    q_rows += f"| {name} | {Q:.4f} | {4*Q*Q:.3f} | {20*math.log10(skH(1, 1, Q)):+.2f} dB |\n"
P('electronics', 'sallen-key-low-pass', f'''
title: Sallen-Key Low-Pass Filter Calculator (Cutoff Frequency & Q)
description: Calculate the cutoff frequency, Q factor and attenuation of a unity-gain Sallen-Key second-order active low-pass filter from R1, R2, C1 and C2.
category: electronics
{intro("The Sallen-Key topology builds a second-order active filter from one op-amp, two resistors and two capacitors, giving a 40 dB-per-decade roll-off. This Sallen-Key low-pass filter calculator finds the cutoff frequency, the Q factor and the attenuation at any frequency for the unity-gain version — see the [Sallen and Key active filter](ib:active-filter-sallen-and-key) explained and compare it with a simple [RC low-pass filter](ib:rc-low-pass-high-pass-filter).")}
keywords: [sallen key low pass filter calculator, sallen key filter calculator, second order low pass filter, active low pass filter calculator, sallen key cutoff frequency, butterworth filter op amp, sallen key q factor]
updated: {D}
variables:
  - {{ id: R1, label: R₁ (input resistor), family: resistance, unit: kohm, default: {kR1/1e3:g}, min: 0 }}
  - {{ id: R2, label: R₂ (second resistor), family: resistance, unit: kohm, default: {kR2/1e3:g}, min: 0 }}
  - {{ id: C1, label: C₁ (feedback capacitor to output), family: capacitance, unit: nF, default: {kC1*1e9:g}, min: 0 }}
  - {{ id: C2, label: C₂ (capacitor to ground), family: capacitance, unit: nF, default: {kC2*1e9:g}, min: 0 }}
  - {{ id: f, label: Frequency of interest, family: frequency, unit: Hz, default: {kf:g}, min: 0 }}
  - {{ id: fc, label: Cutoff (natural) frequency f₀, family: frequency, unit: Hz, min: 0 }}
  - {{ id: Q, label: Quality factor Q, min: 0, decimals: 4 }}
  - {{ id: H, label: Gain at frequency f, min: 0, decimals: 4 }}
  - {{ id: HdB, label: Gain at frequency f (dB), suffix: dB, decimals: 2 }}
equations:
  - fc = 1 / (2 * pi * sqrt(R1 * R2 * C1 * C2))
  - Q = sqrt(R1 * R2 * C1 * C2) / (C2 * (R1 + R2))
  - H = 1 / sqrt((1 - (f / fc)^2)^2 + (f / (fc * Q))^2)
  - HdB = 20 * log10(H)
faq:
  - q: What is the cutoff frequency of a Sallen-Key low-pass filter?
    a: f₀ = 1 ÷ (2π√(R₁R₂C₁C₂)). For a Butterworth response (Q = 0.707) f₀ is also the −3 dB frequency.
  - q: How is Q calculated for a unity-gain Sallen-Key filter?
    a: Q = √(R₁R₂C₁C₂) ÷ [C₂(R₁ + R₂)], where C₁ is the feedback capacitor and C₂ goes to ground. With R₁ = R₂, Q = ½√(C₁/C₂).
  - q: How do I design a Butterworth Sallen-Key filter?
    a: Choose R₁ = R₂ = R and C₁ = 2C₂ (so Q = 0.707), then set f₀ = 1/(2πR C₂√2). For example R = 10 kΩ, C₂ = 10 nF and C₁ = 20 nF give about 1.13 kHz.
  - q: What is the roll-off of a Sallen-Key filter?
    a: 40 dB per decade (12 dB per octave) above the cutoff. Cascade two stages with the right Q values for a fourth-order, 80 dB/decade filter.
related: [electronics/rc-filter, electronics/resonant-frequency, electronics/op-amp-gain, electronics/reactance]
''', f'''
## How to use the Sallen-Key low-pass filter calculator

Enter the two resistors and two capacitors of a **unity-gain** Sallen-Key low-pass stage: **R₁** from the input, **R₂** to the op-amp's non-inverting input, **C₁** from the R₁–R₂ junction back to the output, and **C₂** from the non-inverting input to ground. Add a **frequency** to see the gain there.

## Sallen-Key low-pass formulas

<p class="formula">f₀ = 1 / (2π √(R₁R₂C₁C₂)) &nbsp;·&nbsp; Q = √(R₁R₂C₁C₂) / [C₂(R₁ + R₂)]</p>

<p class="formula">|H(f)| = 1 / √[(1 − (f/f₀)²)² + (f / (f₀Q))²]</p>

## Worked example

R₁ = R₂ = 10 kΩ, C₁ = 22 nF, C₂ = 10 nF:

- f₀ = 1 ÷ (2π √(10k × 10k × 22n × 10n)) = **{kfc:,.1f} Hz**
- Q = ½ √(22/10) = **{kQ:.4f}** — close to Butterworth
- At 5 kHz the gain is **{kH:.4f}** ({20*math.log10(kH):.1f} dB)

## Response types for an equal-resistor design (R₁ = R₂)

| Response | Q | C₁ / C₂ = 4Q² | Gain at f₀ |
|---|---|---|---|
{q_rows}
For the Chebyshev case f₀ is the natural frequency, not the −3 dB point.

## Design notes

- Use C0G/NP0 or film capacitors; X7R ceramics change value with voltage and add distortion.
- The op-amp's gain-bandwidth product should be at least 100 × f₀ × Q for an accurate response.
- High-frequency feedthrough limits the stop-band depth of Sallen-Key low-pass filters; a multiple-feedback (MFB) topology is better when deep attenuation is needed.
''')

# ---------------------------------------------------------------- Schmitt trigger
hVr, hR1, hR2, hVoh, hVol = 2.5, 10e3, 100e3, 5.0, 0.0
hTH = (hVr * hR2 + hVoh * hR1) / (hR1 + hR2); hTL = (hVr * hR2 + hVol * hR1) / (hR1 + hR2)
hy_rows = ''
for ratio in (2, 5, 10, 20, 50, 100):
    hh = 5.0 / (1 + ratio)
    hy_rows += f"| {ratio} | {hh*1e3:,.0f} mV | {2.5*ratio/(1+ratio)+5/(1+ratio):.3f} V | {2.5*ratio/(1+ratio):.3f} V |\n"
P('electronics', 'schmitt-trigger', f'''
title: Schmitt Trigger Calculator (Comparator Hysteresis Thresholds)
description: Calculate the upper and lower switching thresholds and hysteresis of an inverting comparator Schmitt trigger from Vref, R1, R2 and the output levels.
category: electronics
{intro("A Schmitt trigger adds positive feedback to a comparator so it switches at two different input levels, which stops noisy, slow signals from causing chatter at the output. This Schmitt trigger calculator gives the upper and lower thresholds and the hysteresis band for an inverting comparator — see [Schmitt trigger hysteresis](ib:schmitt-trigger-hysteresis) and [comparator circuits](ib:comparator-circuits-explained) explained.")}
keywords: [schmitt trigger calculator, comparator hysteresis calculator, schmitt trigger threshold voltage, hysteresis resistor calculation, inverting schmitt trigger formula, upper and lower threshold voltage]
updated: {D}
variables:
  - {{ id: Vr, label: Reference voltage V_ref, family: voltage, unit: V, default: {hVr:g} }}
  - {{ id: R1, label: R₁ (V_ref to non-inverting input), family: resistance, unit: kohm, default: {hR1/1e3:g}, min: 0 }}
  - {{ id: R2, label: R₂ (output to non-inverting input), family: resistance, unit: kohm, default: {hR2/1e3:g}, min: 0 }}
  - {{ id: Voh, label: Output high level V_OH, family: voltage, unit: V, default: {hVoh:g} }}
  - {{ id: Vol, label: Output low level V_OL, family: voltage, unit: V, default: {hVol:g} }}
  - {{ id: VTH, label: Upper threshold (input rising), family: voltage, unit: V }}
  - {{ id: VTL, label: Lower threshold (input falling), family: voltage, unit: V }}
  - {{ id: Vh, label: Hysteresis, family: voltage, unit: mV }}
  - {{ id: Vc, label: Centre of the hysteresis band, family: voltage, unit: V }}
equations:
  - VTH = (Vr * R2 + Voh * R1) / (R1 + R2)
  - VTL = (Vr * R2 + Vol * R1) / (R1 + R2)
  - Vh = VTH - VTL
  - Vc = (VTH + VTL) / 2
faq:
  - q: How do you calculate Schmitt trigger thresholds?
    a: For an inverting comparator with R₁ from V_ref and R₂ from the output to the + input, V_TH = (V_ref·R₂ + V_OH·R₁)/(R₁ + R₂) and V_TL = (V_ref·R₂ + V_OL·R₁)/(R₁ + R₂).
  - q: What is the hysteresis of a Schmitt trigger?
    a: The gap between the thresholds, V_H = (V_OH − V_OL) × R₁/(R₁ + R₂). A larger R₂ gives less hysteresis.
  - q: How much hysteresis should I use?
    a: More than the peak-to-peak noise on the input — commonly 1–5% of the signal range, or a few tens of millivolts for a clean signal.
  - q: Does an open-drain comparator change the calculation?
    a: Yes. The output high level is set by the pull-up resistor, which also sits in series with R₂, so V_OH is lower than the pull-up supply unless R₂ is much larger than the pull-up.
related: [electronics/voltage-divider, electronics/op-amp-gain, electronics/555-timer, electronics/ntc-thermistor]
''', f'''
## How to use the Schmitt trigger calculator

Enter the **reference voltage**, the two resistors of the positive-feedback divider and the comparator's **output high and low levels**. The signal drives the inverting input. The calculator returns the two switching points, the hysteresis and the centre of the band. To design, choose the hysteresis you need and adjust R₂/R₁.

## Schmitt trigger formulas

<p class="formula">V<sub>TH</sub> = (V<sub>ref</sub> R₂ + V<sub>OH</sub> R₁) / (R₁ + R₂) &nbsp;·&nbsp; V<sub>TL</sub> = (V<sub>ref</sub> R₂ + V<sub>OL</sub> R₁) / (R₁ + R₂)</p>

<p class="formula">V<sub>H</sub> = V<sub>TH</sub> − V<sub>TL</sub> = (V<sub>OH</sub> − V<sub>OL</sub>) R₁ / (R₁ + R₂)</p>

## Worked example

V<sub>ref</sub> = 2.5 V, R₁ = 10 kΩ, R₂ = 100 kΩ, rail-to-rail output 0–5 V:

- V<sub>TH</sub> = (2.5 × 100k + 5 × 10k) ÷ 110k = **{hTH:.4f} V**
- V<sub>TL</sub> = (2.5 × 100k) ÷ 110k = **{hTL:.4f} V**
- Hysteresis = **{(hTH-hTL)*1e3:.1f} mV**, centred on {(hTH+hTL)/2:.3f} V

## Hysteresis vs R₂/R₁ (V<sub>ref</sub> = 2.5 V, output 0–5 V)

| R₂ / R₁ | Hysteresis | V<sub>TH</sub> | V<sub>TL</sub> |
|---|---|---|---|
{hy_rows}
## Notes

- The output goes **low** when the input rises above V<sub>TH</sub> and **high** when it falls below V<sub>TL</sub> (inverting action).
- Positive feedback shifts the band centre above V<sub>ref</sub>; to centre it, lower V<sub>ref</sub> or add a resistor from the + input to ground.
''')

# ---------------------------------------------------------------- I2C pull-up
iVdd, iVol, iIol, itr, iCb, iRp = 3.3, 0.4, 3e-3, 300e-9, 200e-12, 2.2e3
iRmin = (iVdd - iVol) / iIol; iRmax = itr / (0.8473 * iCb); itrp = 0.8473 * iRp * iCb
i2_rows = ''
for C in (50e-12, 100e-12, 200e-12, 300e-12, 400e-12):
    i2_rows += f"| {C*1e12:.0f} pF | {1e-6/(0.8473*C)/1e3:.2f} kΩ | {300e-9/(0.8473*C)/1e3:.2f} kΩ | {120e-9/(0.8473*C)/1e3:.3f} kΩ |\n"
P('electronics', 'i2c-pull-up-resistor', f'''
title: I2C Pull-Up Resistor Calculator (Min & Max Rp)
description: Calculate the minimum and maximum I2C pull-up resistor from supply voltage, sink current, bus capacitance and rise time for 100 kHz, 400 kHz and 1 MHz buses.
category: electronics
{intro("I²C lines are open-drain, so pull-up resistors set both the low-level current the devices must sink and the rise time of every edge. This I2C pull-up resistor calculator finds the allowed range from the I²C specification and the rise time of the value you pick — background on [pull-up and pull-down resistor values](ib:pull-up-pull-down-resistor-values) and [SPI vs I²C](ib:spi-vs-i2c-protocol-comparison).")}
keywords: [i2c pull up resistor calculator, i2c pull-up resistor value, i2c rise time calculation, i2c bus capacitance, pull up resistor for i2c 3.3v, 4.7k pull up i2c, i2c rp min max]
updated: {D}
variables:
  - {{ id: Vdd, label: Pull-up supply voltage, family: voltage, unit: V, default: {iVdd:g}, min: 0 }}
  - id: tr
    label: Bus speed (maximum rise time)
    default: {itr}
    options:
      - {{ label: 'Standard mode 100 kHz (1000 ns)', value: 1e-6 }}
      - {{ label: 'Fast mode 400 kHz (300 ns)', value: {itr} }}
      - {{ label: 'Fast-mode Plus 1 MHz (120 ns)', value: 1.2e-7 }}
  - {{ id: Vol, label: Maximum low-level voltage V_OL, family: voltage, unit: V, default: {iVol:g}, min: 0 }}
  - {{ id: Iol, label: Low-level sink current I_OL, family: current, unit: mA, default: {iIol*1e3:g}, min: 0, help: '3 mA for Standard and Fast mode, 20 mA for Fast-mode Plus.' }}
  - {{ id: Cb, label: Total bus capacitance, family: capacitance, unit: pF, default: {iCb*1e12:g}, min: 0 }}
  - {{ id: Rp, label: Chosen pull-up resistor, family: resistance, unit: kohm, default: {iRp/1e3:g}, min: 0 }}
  - {{ id: Rmin, label: Minimum pull-up resistor, family: resistance, unit: kohm, min: 0 }}
  - {{ id: Rmax, label: Maximum pull-up resistor, family: resistance, unit: kohm, min: 0 }}
  - {{ id: trp, label: Rise time with chosen resistor, family: seconds, unit: ns, min: 0 }}
  - {{ id: Is, label: Sink current with chosen resistor, family: current, unit: mA, min: 0 }}
equations:
  - Rmin = (Vdd - Vol) / Iol
  - Rmax = tr / (0.8473 * Cb)
  - trp = 0.8473 * Rp * Cb
  - Is = (Vdd - Vol) / Rp
faq:
  - q: How do I calculate the I2C pull-up resistor value?
    a: R_min = (V_DD − V_OL) ÷ I_OL and R_max = t_r ÷ (0.8473 × C_b). Any value between the two works; pick a lower value for faster edges and a higher one for lower power.
  - q: Where does the 0.8473 factor come from?
    a: I²C rise time is measured from 30% to 70% of V_DD. For an RC charge that takes RC × ln(0.7/0.3) = 0.8473 RC.
  - q: Is 4.7 kΩ right for I2C?
    a: For 100 kHz with modest capacitance, yes. At 400 kHz and 200 pF the maximum is about 1.8 kΩ, so 4.7 kΩ gives too slow a rise time — use 1.5–2.2 kΩ.
  - q: How do I estimate bus capacitance?
    a: Add about 10 pF per device pin plus roughly 1–2 pF per cm of PCB trace or cable; measure the rise time with an oscilloscope to confirm.
related: [electronics/voltage-divider, electronics/rc-filter, electronics/uart-baud-rate-error, physics/rc-time-constant]
''', f'''
## How to use the I2C pull-up resistor calculator

Enter the **pull-up supply**, choose the **bus speed** (which sets the maximum rise time from the I²C specification), and enter the **sink current** and **bus capacitance**. The calculator returns the allowed range of pull-up values. Enter the resistor you plan to fit to check its rise time and sink current.

## I2C pull-up formulas

<p class="formula">R<sub>p(min)</sub> = (V<sub>DD</sub> − V<sub>OL(max)</sub>) / I<sub>OL</sub> &nbsp;·&nbsp; R<sub>p(max)</sub> = t<sub>r</sub> / (0.8473 × C<sub>b</sub>)</p>

## Worked example

3.3 V bus, Fast mode (t<sub>r</sub> ≤ 300 ns), V<sub>OL</sub> = 0.4 V at 3 mA, 200 pF:

- R<sub>p(min)</sub> = (3.3 − 0.4) ÷ 3 mA = **{iRmin:,.0f} Ω**
- R<sub>p(max)</sub> = 300 ns ÷ (0.8473 × 200 pF) = **{iRmax:,.0f} Ω**
- A 2.2 kΩ resistor gives t<sub>r</sub> = **{itrp*1e9:.0f} ns** — too slow; a 1.5 kΩ gives {0.8473*1.5e3*iCb*1e9:.0f} ns and passes

## Maximum pull-up resistor vs bus capacitance

| Bus capacitance | Standard (1000 ns) | Fast (300 ns) | Fast-mode Plus (120 ns) |
|---|---|---|---|
{i2_rows}
## I²C timing limits (NXP UM10204)

| Mode | Clock | Max rise time | Max bus capacitance | I<sub>OL</sub> at V<sub>OL</sub> = 0.4 V |
|---|---|---|---|---|
| Standard | 100 kHz | 1000 ns | 400 pF | 3 mA |
| Fast | 400 kHz | 300 ns | 400 pF | 3 mA |
| Fast-mode Plus | 1 MHz | 120 ns | 550 pF | 20 mA |

## Notes

- Fit one pull-up per line (SDA and SCL) for the whole bus — module boards often add their own, which appear in parallel.
- If no value satisfies both limits, reduce capacitance, use a bus buffer, or use an active current-source pull-up.
''')

# ---------------------------------------------------------------- Microstrip impedance
mw, mh, mt, mer = 0.3e-3, 0.2e-3, 35e-6, 4.3
def ms(w, h, t, er): return 87 / math.sqrt(er + 1.41) * math.log(5.98 * h / (0.8 * w + t))
mZ = ms(mw, mh, mt, mer); mtpd = 85 * math.sqrt(0.475 * mer + 0.67) / 25.4
mz_rows = ''
for w in (0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4):
    mz_rows += f"| {w:.2f} mm | {w/0.2:.2f} | " + ' | '.join(f"{ms(w*1e-3, 0.2e-3, 35e-6, er):.1f} Ω" for er in (3.5, 4.3, 4.6)) + " |\n"
P('electronics', 'microstrip-impedance', f'''
title: Microstrip Impedance Calculator (PCB Trace Z₀, IPC-2141)
description: Calculate the characteristic impedance and propagation delay of a surface microstrip PCB trace from trace width, thickness, dielectric height and εr.
category: electronics
{intro("A surface microstrip is a PCB trace on an outer layer over a ground plane; its characteristic impedance depends on trace width, copper thickness, dielectric height and the board's dielectric constant. This microstrip impedance calculator uses the IPC-2141 approximation to size [controlled-impedance PCB traces](ib:controlled-impedance-pcb-traces) and to check a [PCB layer stackup](ib:pcb-layer-stackup-design) before you ask the fabricator for a field-solver result.")}
keywords: [microstrip impedance calculator, pcb trace impedance calculator, 50 ohm trace width, characteristic impedance microstrip, ipc-2141 microstrip formula, controlled impedance calculator, fr4 trace impedance]
updated: {D}
variables:
  - {{ id: w, label: Trace width w, family: length, unit: mm, imperialUnit: in, default: {mw*1e3:g}, min: 0 }}
  - {{ id: t, label: Copper thickness t, family: length, unit: um, default: {mt*1e6:g}, min: 0, help: '1 oz copper ≈ 35 µm, 2 oz ≈ 70 µm, 0.5 oz ≈ 17.5 µm (add plating for outer layers).' }}
  - {{ id: h, label: Dielectric height to ground plane h, family: length, unit: mm, imperialUnit: in, default: {mh*1e3:g}, min: 0 }}
  - {{ id: er, label: Dielectric constant εr, default: {mer:g}, min: 1, help: 'FR-4 is typically 4.0–4.6 at 1 GHz; Rogers RO4350B is 3.48 (design value 3.66).' }}
  - {{ id: Z0, label: Characteristic impedance Z₀, family: resistance, unit: ohm, min: 0 }}
  - {{ id: tpd, label: Propagation delay, suffix: ps/mm, min: 0, decimals: 2 }}
  - {{ id: wh, label: Width-to-height ratio w/h (valid 0.1–2.0), min: 0, decimals: 3 }}
equations:
  - Z0 = 87 / sqrt(er + 1.41) * ln(5.98 * h / (0.8 * w + t))
  - tpd = 85 * sqrt(0.475 * er + 0.67) / 25.4
  - wh = w / h
faq:
  - q: What is the microstrip impedance formula?
    a: The IPC-2141 approximation is Z₀ = 87/√(εr + 1.41) × ln[5.98h/(0.8w + t)], valid for 0.1 < w/h < 2.0 and 1 < εr < 15.
  - q: How wide is a 50 Ω trace on FR-4?
    a: Roughly 1.8–2 times the dielectric height. On 0.2 mm prepreg with εr 4.3 and 1 oz copper it is about 0.33 mm; on 1.6 mm two-layer board it is about 3 mm.
  - q: How accurate is this calculator?
    a: Within about ±5% inside the valid range. Solder mask lowers Z₀ by 1–3 Ω, and εr varies with frequency and glass weave, so final stackups should be confirmed with a field solver or by the fabricator.
  - q: What is the propagation delay on a microstrip?
    a: About 85√(0.475εr + 0.67) ps per inch — roughly 5.6–5.9 ps/mm on FR-4, slower than in free space because part of the field travels in the dielectric.
related: [electronics/pcb-trace-width, electronics/antenna-length, electronics/reactance, electronics/free-space-path-loss]
''', f'''
## How to use the microstrip impedance calculator

Enter the **trace width**, **copper thickness**, the **dielectric height** between the trace and its reference plane, and the board's **dielectric constant**. The calculator returns Z₀, the propagation delay and the w/h ratio — keep w/h between 0.1 and 2.0, where the formula is valid. Clear the width and enter a target Z₀ to find the width.

## Microstrip impedance formula (IPC-2141)

<p class="formula">Z₀ = 87 / √(ε<sub>r</sub> + 1.41) × ln[5.98 h / (0.8 w + t)]</p>

<p class="formula">t<sub>pd</sub> = 85 √(0.475 ε<sub>r</sub> + 0.67) ps/in</p>

## Worked example

0.3 mm trace, 35 µm copper, 0.2 mm prepreg, ε<sub>r</sub> = 4.3:

- Z₀ = 87 ÷ √5.71 × ln(1.196 ÷ 0.275) = **{mZ:.1f} Ω**
- Propagation delay = **{mtpd:.2f} ps/mm** ({mtpd*25.4:.0f} ps/in)

## Z₀ vs trace width (h = 0.2 mm, t = 35 µm)

| Width | w/h | ε<sub>r</sub> 3.5 | ε<sub>r</sub> 4.3 | ε<sub>r</sub> 4.6 |
|---|---|---|---|---|
{mz_rows}
## Notes

- Wider traces, thinner dielectric and higher ε<sub>r</sub> all lower the impedance.
- Keep the reference plane continuous under the trace — a split plane breaks the return path and the impedance.
- Differential pairs, stripline and coplanar waveguide need different formulas.
''')

# ======================================================================= CHEMISTRY

# ---------------------------------------------------------------- Limiting reagent
lmA, lMA, la, lmB, lMB, lb, lp, lMP = 50.0, 28.014, 1, 10.0, 2.016, 3, 2, 17.031
lnA, lnB = lmA / lMA, lmB / lMB; lx = min(lnA / la, lnB / lb)
lmP = lx * lp * lMP; lAx = (lnA - la * lx) * lMA; lBx = (lnB - lb * lx) * lMB
P('chemistry', 'limiting-reagent', f'''
title: Limiting Reagent Calculator (Limiting Reactant & Excess)
description: Find the limiting reagent of a reaction from the masses, molar masses and coefficients of two reactants — with the theoretical yield and excess left over.
category: chemistry
{intro("In a reaction the limiting reagent is the reactant that runs out first, so it alone fixes how much product can form; the other reactant is left in excess. This limiting reagent calculator converts both masses to moles, divides by the balanced-equation coefficients to find which runs out, and returns the theoretical yield and the mass of excess reactant remaining.")}
keywords: [limiting reagent calculator, limiting reactant calculator, how to find limiting reagent, excess reactant calculator, stoichiometry calculator, theoretical yield from limiting reagent, mole ratio calculator]
updated: {D}
variables:
  - {{ id: mA, label: Mass of reactant A, family: mass, unit: g, imperialUnit: g, default: {lmA:g}, min: 0 }}
  - {{ id: MA, label: Molar mass of A, suffix: g/mol, default: {lMA:g}, min: 0 }}
  - {{ id: a, label: Coefficient of A in the balanced equation, default: {la}, min: 0 }}
  - {{ id: mB, label: Mass of reactant B, family: mass, unit: g, imperialUnit: g, default: {lmB:g}, min: 0 }}
  - {{ id: MB, label: Molar mass of B, suffix: g/mol, default: {lMB:g}, min: 0 }}
  - {{ id: b, label: Coefficient of B, default: {lb}, min: 0 }}
  - {{ id: p, label: Coefficient of the product, default: {lp}, min: 0 }}
  - {{ id: MP, label: Molar mass of the product, suffix: g/mol, default: {lMP:g}, min: 0 }}
  - {{ id: xA, label: Moles of A ÷ coefficient, suffix: mol, min: 0, decimals: 4 }}
  - {{ id: xB, label: Moles of B ÷ coefficient, suffix: mol, min: 0, decimals: 4 }}
  - {{ id: mP, label: Theoretical yield of product, family: mass, unit: g, imperialUnit: g, min: 0 }}
  - {{ id: mAx, label: Excess A left over (0 if A is limiting), family: mass, unit: g, imperialUnit: g, min: 0 }}
  - {{ id: mBx, label: Excess B left over (0 if B is limiting), family: mass, unit: g, imperialUnit: g, min: 0 }}
equations:
  - xA = mA * 1000 / MA / a
  - xB = mB * 1000 / MB / b
  - mP = min(xA, xB) * p * MP / 1000
  - mAx = (xA - min(xA, xB)) * a * MA / 1000
  - mBx = (xB - min(xA, xB)) * b * MB / 1000
faq:
  - q: How do you find the limiting reagent?
    a: Convert each reactant to moles, then divide by its coefficient in the balanced equation. The reactant with the smaller result is the limiting reagent.
  - q: Is the limiting reagent always the one with the smaller mass?
    a: No. It depends on moles and on the mole ratio. In N₂ + 3H₂ → 2NH₃, 10 g of hydrogen limits 50 g of nitrogen because each mole of N₂ needs three moles of H₂.
  - q: How do I calculate the theoretical yield from the limiting reagent?
    a: Multiply the limiting reagent's moles-per-coefficient by the product's coefficient to get moles of product, then multiply by the product's molar mass.
  - q: How much excess reactant is left?
    a: Subtract the moles consumed (coefficient × reaction extent) from the moles present and convert back to grams. The calculator shows this as the excess left over.
related: [chemistry/theoretical-yield, chemistry/percent-yield, chemistry/moles, chemistry/percent-composition]
''', f'''
## How to use the limiting reagent calculator

Balance the equation first. Enter the **mass**, **molar mass** and **coefficient** for each reactant, then the **coefficient** and **molar mass** of the product you want. The reactant with the smaller "moles ÷ coefficient" is limiting — its excess shows as 0 — and the theoretical yield is calculated from it.

## Limiting reagent method

<p class="formula">n = m / M &nbsp;·&nbsp; ξ = min(n<sub>A</sub>/a, n<sub>B</sub>/b) &nbsp;·&nbsp; m<sub>product</sub> = ξ × p × M<sub>product</sub></p>

ξ (the reaction extent) is the number of times the balanced equation can "run" before the limiting reagent is used up.

## Worked example: N₂ + 3H₂ → 2NH₃

50 g N₂ (28.014 g/mol) and 10 g H₂ (2.016 g/mol):

- N₂: {lnA:.4f} mol ÷ 1 = **{lnA/la:.4f}**
- H₂: {lnB:.4f} mol ÷ 3 = **{lnB/lb:.4f}** → hydrogen is the limiting reagent
- NH₃ = {lx:.4f} × 2 × 17.031 = **{lmP:.2f} g**
- N₂ left over = ({lnA:.4f} − {lx:.4f}) × 28.014 = **{lAx:.2f} g**

## Steps by hand

1. Write and balance the chemical equation.
2. Convert every reactant mass to moles with its molar mass.
3. Divide each by its coefficient; the smallest value identifies the limiting reagent.
4. Use that value with the product's coefficient to find moles and grams of product.

Compare the theoretical yield with what you actually recovered using the [percent yield calculator](/chemistry/percent-yield/).
''')

# ---------------------------------------------------------------- Theoretical yield
ym, yMR, yr, yp, yMP, ya = 2.00, 138.12, 1, 1, 180.16, 2.10
ynR = ym / yMR; ymT = ynR * yp / yr * yMP; yY = ya / ymT
ty_rows = ''
for name, MR, r_, p_, MPp, prod in (('Salicylic acid → aspirin', 138.12, 1, 1, 180.16, 'aspirin'),
                                    ('Glucose → ethanol (fermentation)', 180.156, 1, 2, 46.069, 'ethanol'),
                                    ('CaCO₃ → CaO (calcination)', 100.086, 1, 1, 56.077, 'CaO'),
                                    ('Fe₂O₃ → Fe (reduction)', 159.687, 1, 2, 55.845, 'Fe'),
                                    ('CH₄ → CO₂ (combustion)', 16.043, 1, 1, 44.009, 'CO₂')):
    ty_rows += f"| {name} | {p_}:{r_} | {1000/MR*p_/r_*MPp:,.1f} g {prod} |\n"
P('chemistry', 'theoretical-yield', f'''
title: Theoretical Yield Calculator (Grams of Product & % Yield)
description: Calculate the theoretical yield of a reaction in grams from the mass of the limiting reagent, the mole ratio and molar masses — plus the percent yield.
category: chemistry
{intro("The theoretical yield is the maximum mass of product a reaction can give if all of the limiting reagent reacts as the balanced equation says. This theoretical yield calculator turns the mass of the limiting reagent into moles, applies the mole ratio and converts back to grams of product — and, if you enter what you actually obtained, gives the percent yield.")}
keywords: [theoretical yield calculator, how to calculate theoretical yield, theoretical yield formula, grams of product calculator, mole ratio yield, percent yield and theoretical yield, stoichiometry yield]
updated: {D}
variables:
  - {{ id: m, label: Mass of limiting reagent, family: mass, unit: g, imperialUnit: g, default: {ym:g}, min: 0 }}
  - {{ id: MR, label: Molar mass of limiting reagent, suffix: g/mol, default: {yMR:g}, min: 0 }}
  - {{ id: r, label: Coefficient of limiting reagent, default: {yr}, min: 0 }}
  - {{ id: p, label: Coefficient of product, default: {yp}, min: 0 }}
  - {{ id: MP, label: Molar mass of product, suffix: g/mol, default: {yMP:g}, min: 0 }}
  - {{ id: ma, label: Actual yield (optional), family: mass, unit: g, imperialUnit: g, default: {ya:g}, min: 0 }}
  - {{ id: nP, label: Moles of product, suffix: mol, min: 0, decimals: 5 }}
  - {{ id: mT, label: Theoretical yield, family: mass, unit: g, imperialUnit: g, min: 0 }}
  - {{ id: Y, label: Percent yield, family: percent, unit: '%', min: 0, decimals: 1 }}
equations:
  - nP = m * 1000 / MR * p / r
  - mT = nP * MP / 1000
  - Y = ma / mT
faq:
  - q: How do you calculate theoretical yield?
    a: Moles of limiting reagent = mass ÷ molar mass; moles of product = that × (product coefficient ÷ reagent coefficient); theoretical yield = moles of product × molar mass of product.
  - q: What is the difference between theoretical and actual yield?
    a: Theoretical yield is the calculated maximum; actual yield is what you recover. Percent yield = actual ÷ theoretical × 100%.
  - q: Can percent yield be over 100%?
    a: Not for a pure, dry product. A result above 100% usually means the product is wet or contaminated, or the wrong limiting reagent was used.
  - q: What if I don't know which reactant is limiting?
    a: Work out moles ÷ coefficient for each reactant first — the smallest is limiting. The limiting reagent calculator does this for two reactants.
related: [chemistry/limiting-reagent, chemistry/percent-yield, chemistry/moles, chemistry/molarity]
''', f'''
## How to use the theoretical yield calculator

Enter the **mass of the limiting reagent**, its **molar mass**, the **coefficients** of the reagent and the product from the balanced equation, and the **molar mass of the product**. The calculator returns the moles and grams of product. Enter your **actual yield** to see the percent yield.

## Theoretical yield formula

<p class="formula">m<sub>theoretical</sub> = (m<sub>reagent</sub> / M<sub>reagent</sub>) × (p / r) × M<sub>product</sub></p>

<p class="formula">% yield = m<sub>actual</sub> / m<sub>theoretical</sub> × 100%</p>

## Worked example: aspirin synthesis

2.00 g salicylic acid (138.12 g/mol) reacts 1 : 1 to give aspirin (180.16 g/mol); 2.10 g of aspirin is recovered:

- Moles = 2.00 ÷ 138.12 = **{ynR:.5f} mol**
- Theoretical yield = {ynR:.5f} × 180.16 = **{ymT:.3f} g**
- Percent yield = 2.10 ÷ {ymT:.3f} = **{yY*100:.1f}%**

## Theoretical yield from 1 kg of reagent

| Reaction | Product : reagent | Theoretical yield |
|---|---|---|
{ty_rows}
## Why actual yield is lower

- Incomplete reaction or an equilibrium that does not go to completion
- Side reactions forming other products
- Losses in filtration, transfer, washing and recrystallisation
''')

# ---------------------------------------------------------------- Solution preparation
sc, sV_, sM, spur = 0.1, 500e-6, 58.44, 0.995
sm = sc * sV_ * 1000 * sM / spur          # grams
sp_rows = ''
for name, M in (('Sodium chloride NaCl', 58.44), ('Potassium chloride KCl', 74.55), ('Sodium hydroxide NaOH', 40.00),
                ('Sodium carbonate Na₂CO₃', 105.99), ('Potassium dihydrogen phosphate KH₂PO₄', 136.09),
                ('Copper(II) sulfate pentahydrate CuSO₄·5H₂O', 249.69), ('Glucose C₆H₁₂O₆', 180.16),
                ('Disodium EDTA dihydrate', 372.24)):
    sp_rows += f"| {name} | {M:.2f} | {0.1*M:.3f} g | {M:.2f} g |\n"
P('chemistry', 'solution-preparation', f'''
title: Solution Preparation Calculator (Mass of Solid Needed)
description: Calculate how many grams of solid to weigh out to make a solution of a given molarity and volume, corrected for reagent purity, with common reagent masses.
category: chemistry
{intro("To make a solution of known molarity you weigh out moles × molar mass of the solid, dissolve it and make up to volume. This solution preparation calculator gives the mass of solid needed for any concentration and volume, corrected for reagent purity, and lists the masses for common lab reagents.")}
keywords: [solution preparation calculator, mass needed for molar solution, how many grams to make a solution, grams to make 0.1 m solution, molar solution preparation, reagent purity correction, make a solution from solid]
updated: {D}
variables:
  - {{ id: c, label: Target concentration, suffix: mol/L, default: {sc:g}, min: 0 }}
  - {{ id: V, label: Final solution volume, family: volume, unit: mL, imperialUnit: mL, default: {sV_*1e6:g}, min: 0 }}
  - {{ id: M, label: Molar mass of the solid (as weighed), suffix: g/mol, default: {sM:g}, min: 0, help: 'Use the molar mass of the form you weigh — including water of crystallisation for hydrates.' }}
  - {{ id: pur, label: Reagent purity (assay), family: percent, unit: '%', default: {spur*100:g}, min: 0.01, max: 1 }}
  - {{ id: n, label: Moles of solute needed, suffix: mol, min: 0, decimals: 5 }}
  - {{ id: m, label: Mass to weigh out, family: mass, unit: g, imperialUnit: g, min: 0 }}
equations:
  - n = c * V * 1000
  - m = n * M / pur / 1000
faq:
  - q: How do I calculate the mass needed for a solution?
    a: Mass (g) = molarity (mol/L) × volume (L) × molar mass (g/mol). Divide by the purity as a fraction if the reagent is not 100% pure.
  - q: How many grams of NaCl make 1 L of 1 M solution?
    a: 58.44 g. For 500 mL of 0.1 M you need 0.1 × 0.5 × 58.44 = 2.922 g (2.937 g at 99.5% purity).
  - q: Should I add the solid to the full volume of water?
    a: No. Dissolve it in less water, then make up to the mark in a volumetric flask, because the solid itself takes up volume.
  - q: How do I handle hydrates?
    a: Use the molar mass of the hydrate you are weighing. CuSO₄·5H₂O is 249.69 g/mol, not 159.61 g/mol for anhydrous CuSO₄.
related: [chemistry/molarity, chemistry/dilution, chemistry/normality, chemistry/mass-percent]
''', f'''
## How to use the solution preparation calculator

Enter the **concentration** you want, the **final volume** of solution, the **molar mass** of the solid you are weighing and its **purity** from the label or certificate of analysis. The calculator returns the moles needed and the mass to weigh. Clear the mass and enter a mass you have to find the concentration it makes.

## Solution preparation formula

<p class="formula">m = c × V × M ÷ purity</p>

with c in mol/L, V in litres, M in g/mol and purity as a fraction.

## Worked example

500 mL of 0.1 M NaCl (58.44 g/mol) from 99.5% pure salt:

- Moles = 0.1 × 0.500 = **{sc*sV_*1000:.3f} mol**
- Mass = 0.05 × 58.44 ÷ 0.995 = **{sm:.4f} g**

## Mass needed for 1 litre of solution

| Reagent | Molar mass (g/mol) | 0.1 M | 1 M |
|---|---|---|---|
{sp_rows}
## Good practice

- Use an analytical balance and a Class A volumetric flask for standard solutions.
- Hygroscopic solids such as NaOH absorb water while weighing — standardise those solutions by titration.
- To prepare a weaker solution from a stock instead, use the [dilution calculator](/chemistry/dilution/).
''')

# ---------------------------------------------------------------- Equilibrium constant
eA, eB, eC, eD = 0.50, 1.50, 0.10, 1.0
ea, eb, ec, ed, eT = 1, 3, 2, 0, 773.15
eKc = eC ** ec * eD ** ed / (eA ** ea * eB ** eb); edn = ec + ed - ea - eb
eKp = eKc * (0.0820574 * eT) ** edn
kp_rows = ''
for T in (298.15, 500, 773.15, 1000):
    RT = 0.0820574 * T
    kp_rows += f"| {T:g} K | {RT:.3f} | " + ' | '.join(f"{RT**dn:.4g}" for dn in (-2, -1, 1, 2)) + " |\n"
P('chemistry', 'equilibrium-constant', f'''
title: Equilibrium Constant Calculator (Kc and Kp)
description: Calculate the equilibrium constant Kc from equilibrium concentrations and coefficients, and convert it to Kp with Kp = Kc(RT)^Δn at any temperature.
category: chemistry
{intro("The equilibrium constant Kc is the ratio of product to reactant concentrations at equilibrium, each raised to its coefficient in the balanced equation; for gases it is often given as Kp in partial pressures instead. This equilibrium constant calculator works out Kc for aA + bB ⇌ cC + dD and converts it to Kp with Kp = Kc(RT)^Δn.")}
keywords: [equilibrium constant calculator, kc calculator, kp calculator, kp to kc, kc to kp conversion, kp = kc(rt)^delta n, equilibrium expression calculator, how to calculate kc]
updated: {D}
variables:
  - {{ id: cA, label: Concentration [A], suffix: mol/L, default: {eA:g}, min: 0 }}
  - {{ id: a, label: Coefficient a, default: {ea}, min: 0 }}
  - {{ id: cB, label: Concentration [B], suffix: mol/L, default: {eB:g}, min: 0 }}
  - {{ id: b, label: Coefficient b, default: {eb}, min: 0 }}
  - {{ id: cC, label: Concentration [C], suffix: mol/L, default: {eC:g}, min: 0 }}
  - {{ id: c, label: Coefficient c, default: {ec}, min: 0 }}
  - {{ id: cD, label: Concentration [D], suffix: mol/L, default: {eD:g}, min: 0 }}
  - {{ id: d, label: Coefficient d (0 if no D), default: {ed}, min: 0 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, imperialUnit: F, default: {eT-273.15:g} }}
  - {{ id: Kc, label: Equilibrium constant Kc, min: 0 }}
  - {{ id: dn, label: Change in moles of gas Δn, decimals: 3 }}
  - {{ id: Kp, label: Equilibrium constant Kp (pressures in atm), min: 0 }}
equations:
  - Kc = cC^c * cD^d / (cA^a * cB^b)
  - dn = c + d - a - b
  - Kp = Kc * (0.0820574 * T)^dn
faq:
  - q: How do you calculate Kc?
    a: For aA + bB ⇌ cC + dD, Kc = [C]^c[D]^d ÷ ([A]^a[B]^b) using equilibrium molar concentrations. Pure solids and liquids are left out.
  - q: What is the relationship between Kp and Kc?
    a: Kp = Kc(RT)^Δn, where R = 0.08206 L·atm/(mol·K), T is in kelvin and Δn is moles of gaseous products minus moles of gaseous reactants. When Δn = 0, Kp = Kc.
  - q: What does a large K mean?
    a: K much greater than 1 means products dominate at equilibrium; K much less than 1 means reactants dominate. K says nothing about how fast equilibrium is reached.
  - q: Does K change with concentration or pressure?
    a: No — only temperature changes K. Changing concentrations or pressure shifts the position of equilibrium, but the ratio returns to the same K.
related: [chemistry/gibbs-free-energy, chemistry/cell-potential, chemistry/daltons-law, chemistry/molarity]
''', f'''
## How to use the equilibrium constant calculator

Enter the **equilibrium concentrations** and **coefficients** for reaction aA + bB ⇌ cC + dD. For a reaction with fewer species, set the unused coefficient to 0. Enter the **temperature** to convert Kc to Kp — the conversion assumes every species counted in Δn is a gas; set the coefficient of any solid or liquid to 0.

## Equilibrium constant formulas

<p class="formula">K<sub>c</sub> = [C]<sup>c</sup>[D]<sup>d</sup> / ([A]<sup>a</sup>[B]<sup>b</sup>)</p>

<p class="formula">K<sub>p</sub> = K<sub>c</sub>(RT)<sup>Δn</sup> &nbsp;·&nbsp; Δn = (c + d) − (a + b), R = 0.0820574 L·atm/(mol·K)</p>

## Worked example: N₂ + 3H₂ ⇌ 2NH₃

Illustrative equilibrium mixture at 500 °C: [N₂] = 0.50 M, [H₂] = 1.50 M, [NH₃] = 0.10 M:

- K<sub>c</sub> = 0.10² ÷ (0.50 × 1.50³) = **{eKc:.6f}**
- Δn = 2 − 4 = **{edn:g}**
- K<sub>p</sub> = {eKc:.6f} × (0.0820574 × 773.15)<sup>−2</sup> = **{eKp:.4g}**

## (RT)<sup>Δn</sup> conversion factors

| Temperature | RT (L·atm/mol) | Δn = −2 | Δn = −1 | Δn = +1 | Δn = +2 |
|---|---|---|---|---|---|
{kp_rows}
## Notes

- With pressures in bar use R = 0.0831446 L·bar/(mol·K).
- The reaction quotient Q uses the same expression with non-equilibrium values: if Q < K the reaction moves forward, if Q > K it moves back.
- K is linked to the standard Gibbs energy by ΔG° = −RT ln K — see the [Gibbs free energy calculator](/chemistry/gibbs-free-energy/).
''')

# ---------------------------------------------------------------- Cell potential
cEc, cEa, cn, cT = 0.34, -0.76, 2, 298.15
cE = cEc - cEa; cdG = -cn * F * cE / 1000; clK = cn * F * cE / (R * cT * math.log(10))
cells = [('F₂ + 2e⁻ → 2F⁻', 2.87), ('Au³⁺ + 3e⁻ → Au', 1.50), ('Cl₂ + 2e⁻ → 2Cl⁻', 1.36), ('O₂ + 4H⁺ + 4e⁻ → 2H₂O', 1.23),
         ('Br₂ + 2e⁻ → 2Br⁻', 1.07), ('Ag⁺ + e⁻ → Ag', 0.80), ('Fe³⁺ + e⁻ → Fe²⁺', 0.77), ('I₂ + 2e⁻ → 2I⁻', 0.54),
         ('Cu²⁺ + 2e⁻ → Cu', 0.34), ('2H⁺ + 2e⁻ → H₂', 0.00), ('Pb²⁺ + 2e⁻ → Pb', -0.13), ('Sn²⁺ + 2e⁻ → Sn', -0.14),
         ('Ni²⁺ + 2e⁻ → Ni', -0.25), ('Fe²⁺ + 2e⁻ → Fe', -0.44), ('Zn²⁺ + 2e⁻ → Zn', -0.76), ('Al³⁺ + 3e⁻ → Al', -1.66),
         ('Mg²⁺ + 2e⁻ → Mg', -2.37), ('Na⁺ + e⁻ → Na', -2.71), ('Li⁺ + e⁻ → Li', -3.04)]
ce_rows = ''.join(f"| {h} | {e:+.2f} V |\n" for h, e in cells)
cx_rows = ''
for name, ec_, ea_, nn in (('Daniell cell (Cu / Zn)', 0.34, -0.76, 2), ('Silver / copper', 0.80, 0.34, 2), ('Zinc / hydrogen', 0.00, -0.76, 2), ('Chlorine / hydrogen', 1.36, 0.00, 2), ('Silver / zinc', 0.80, -0.76, 2)):
    E = ec_ - ea_
    cx_rows += f"| {name} | {E:.2f} V | {nn} | {-nn*F*E/1000:.1f} kJ/mol |\n"
P('chemistry', 'cell-potential', f'''
title: Cell Potential Calculator (E°cell, ΔG° and K)
description: Calculate the standard cell potential E°cell from cathode and anode reduction potentials, plus the standard Gibbs energy ΔG° = −nFE° and equilibrium constant K.
category: chemistry
{intro("The standard cell potential of a galvanic cell is the reduction potential of the cathode minus that of the anode; a positive value means the reaction is spontaneous. This cell potential calculator gives E°cell, the standard Gibbs energy change ΔG° = −nFE° and the equilibrium constant K, with a table of standard reduction potentials.")}
keywords: [cell potential calculator, standard cell potential calculator, e cell calculator, ecell = ecathode - eanode, delta g = -nfe, galvanic cell voltage, standard reduction potential table]
updated: {D}
variables:
  - {{ id: Ec, label: Standard reduction potential of cathode E°, family: voltage, unit: V, default: {cEc:g} }}
  - {{ id: Ea, label: Standard reduction potential of anode E°, family: voltage, unit: V, default: {cEa:g} }}
  - {{ id: n, label: Electrons transferred n, default: {cn}, min: 1 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, imperialUnit: F, default: {cT-273.15:g} }}
  - {{ id: E, label: Standard cell potential E°cell, family: voltage, unit: V }}
  - {{ id: dG, label: Standard Gibbs energy change ΔG°, suffix: kJ/mol, decimals: 2 }}
  - {{ id: lK, label: log₁₀ K, decimals: 2 }}
  - {{ id: K, label: Equilibrium constant K, min: 0 }}
equations:
  - E = Ec - Ea
  - dG = -n * 96485.33212 * E / 1000
  - lK = n * 96485.33212 * E / (8.314462618 * T * ln(10))
  - K = 10^lK
faq:
  - q: How do you calculate standard cell potential?
    a: E°cell = E°cathode − E°anode, using the standard reduction potentials of both half-reactions as listed in tables. Do not multiply E° by the coefficients when balancing electrons.
  - q: How is cell potential related to Gibbs free energy?
    a: ΔG° = −nFE°cell, with F = 96,485 C/mol. A positive E° gives a negative ΔG°, so the reaction is spontaneous.
  - q: How do I find the equilibrium constant from E°?
    a: ln K = nFE°/(RT). At 25 °C this is log₁₀ K = nE°/0.05916 V. The Daniell cell (1.10 V, n = 2) has K ≈ 10³⁷.
  - q: What about non-standard concentrations?
    a: Use the Nernst equation, E = E° − (RT/nF) ln Q, to correct the cell potential for actual concentrations and temperature.
related: [chemistry/nernst-equation, chemistry/gibbs-free-energy, chemistry/faraday-electrolysis, chemistry/equilibrium-constant]
''', f'''
## How to use the cell potential calculator

Look up the **standard reduction potentials** of both half-reactions in the table below. The **cathode** is where reduction happens (higher E°); the **anode** is oxidised (lower E°). Enter both values as **reduction** potentials, the **number of electrons** in the balanced overall reaction and the temperature.

## Cell potential formulas

<p class="formula">E°<sub>cell</sub> = E°<sub>cathode</sub> − E°<sub>anode</sub> &nbsp;·&nbsp; ΔG° = −nFE°<sub>cell</sub> &nbsp;·&nbsp; ln K = nFE°<sub>cell</sub> / RT</p>

F = 96,485.33 C/mol and R = 8.314 J/(mol·K).

## Worked example: Daniell cell

Cu²⁺/Cu cathode (+0.34 V) and Zn²⁺/Zn anode (−0.76 V), n = 2, 25 °C:

- E°<sub>cell</sub> = 0.34 − (−0.76) = **{cE:.2f} V**
- ΔG° = −2 × 96,485 × {cE:.2f} = **{cdG:.1f} kJ/mol**
- log₁₀ K = **{clK:.2f}**, so K ≈ **{10**(clK - math.floor(clK)):.2f} × 10<sup>{math.floor(clK)}</sup>**

## Standard reduction potentials at 25 °C

| Half-reaction | E° |
|---|---|
{ce_rows}
## Example cells

| Cell | E°<sub>cell</sub> | n | ΔG° |
|---|---|---|---|
{cx_rows}''')

# ---------------------------------------------------------------- Dissolved oxygen saturation
def DOsat(tc, S=0.0, Pa=1.0):
    T = tc + 273.15
    l = (-139.34411 + 1.575701e5 / T - 6.642308e7 / T**2 + 1.243800e10 / T**3 - 8.621949e11 / T**4
         - S * (1.7674e-2 - 1.0754e1 / T + 2.1407e3 / T**2))
    C = math.exp(l)
    pw = math.exp(11.8571 - 3840.70 / T - 216961 / T**2); th = 0.000975 - 1.426e-5 * tc + 6.436e-8 * tc**2
    return C * Pa * ((1 - pw / Pa) * (1 - th * Pa)) / ((1 - pw) * (1 - th))
oT, oS, oP = 20.0, 0.0, 101.325
o20 = DOsat(oT, oS, oP / 101.325); o20alt = DOsat(oT, 0, 90.0 / 101.325)
do_rows = ''
for t in (0, 5, 10, 15, 20, 25, 30, 35, 40):
    do_rows += f"| {t} °C | {DOsat(t):.2f} | {DOsat(t, 10):.2f} | {DOsat(t, 20):.2f} | {DOsat(t, 35):.2f} |\n"
P('chemistry', 'dissolved-oxygen-saturation', f'''
title: Dissolved Oxygen Saturation Calculator (mg/L vs Temperature)
description: Calculate the dissolved oxygen saturation concentration of water in mg/L from temperature, salinity and barometric pressure, plus a sample's percent saturation.
category: chemistry
{intro("Water in equilibrium with air holds a fixed amount of oxygen that falls as temperature and salinity rise and as barometric pressure drops. This dissolved oxygen saturation calculator uses the Benson–Krause equations adopted in Standard Methods to give the saturation value in mg/L and the percent saturation of a measured sample — the reference an [optical dissolved oxygen sensor](ib:how-do-optical-dissolved-oxygen-sensors-work) is calibrated against.")}
keywords: [dissolved oxygen saturation calculator, do saturation calculator, oxygen solubility in water calculator, dissolved oxygen mg/l temperature, percent saturation dissolved oxygen, do saturation table, benson krause equation]
updated: {D}
variables:
  - {{ id: T, label: Water temperature, family: temperature, unit: C, imperialUnit: F, default: {oT:g} }}
  - {{ id: S, label: Salinity, suffix: g/kg (ppt), default: {oS:g}, min: 0, help: 'Fresh water 0; brackish 1–30; seawater about 35.' }}
  - {{ id: P, label: Barometric pressure, family: pressure, unit: kPa, imperialUnit: mmHg, default: {oP:g}, min: 0 }}
  - {{ id: DOm, label: Measured dissolved oxygen (optional), suffix: mg/L, default: 7.5, min: 0 }}
  - {{ id: C0, label: Saturation at 1 atm, suffix: mg/L, min: 0, decimals: 3 }}
  - {{ id: Cs, label: Saturation at the given pressure, suffix: mg/L, min: 0, decimals: 3 }}
  - {{ id: sat, label: Percent saturation of the sample, family: percent, unit: '%', min: 0, decimals: 1 }}
equations:
  - C0 = exp(-139.34411 + 1.575701e5 / T - 6.642308e7 / T^2 + 1.2438e10 / T^3 - 8.621949e11 / T^4 - S * (1.7674e-2 - 10.754 / T + 2140.7 / T^2))
  - Cs = C0 * (P / 101325) * (1 - exp(11.8571 - 3840.7 / T - 216961 / T^2) / (P / 101325)) * (1 - (0.000975 - 1.426e-5 * (T - 273.15) + 6.436e-8 * (T - 273.15)^2) * (P / 101325)) / ((1 - exp(11.8571 - 3840.7 / T - 216961 / T^2)) * (1 - (0.000975 - 1.426e-5 * (T - 273.15) + 6.436e-8 * (T - 273.15)^2)))
  - sat = DOm / Cs
faq:
  - q: What is the dissolved oxygen saturation at 20 °C?
    a: 9.09 mg/L for fresh water at 1 atm (101.325 kPa). It is 14.62 mg/L at 0 °C, 8.26 mg/L at 25 °C and 7.56 mg/L at 30 °C.
  - q: How does salinity affect dissolved oxygen?
    a: Dissolved salts reduce oxygen solubility. Seawater at 35 g/kg holds about 18–20% less oxygen than fresh water — 7.40 mg/L at 20 °C.
  - q: How do I correct DO saturation for altitude?
    a: Saturation is roughly proportional to barometric pressure (corrected for water vapour). At about 1,000 m elevation pressure is near 90 kPa, so saturation at 20 °C drops to about 8.05 mg/L.
  - q: What is percent saturation?
    a: Measured DO ÷ saturation DO × 100%. Values above 100% (supersaturation) occur with strong algal photosynthesis or aeration; values below about 60% stress fish.
related: [chemistry/henrys-law, chemistry/water-hardness, chemistry/raoults-law, chemistry/ppm]
''', f'''
## How to use the dissolved oxygen saturation calculator

Enter the **water temperature**, the **salinity** (0 for fresh water) and the local **barometric pressure** — use the actual station pressure, not the sea-level-corrected value from a weather report. The calculator gives the saturation concentration at 1 atm and at your pressure. Enter a **measured DO** to see the percent saturation.

## Dissolved oxygen saturation formula (Benson & Krause)

<p class="formula">ln C* = −139.34411 + 1.575701×10⁵/T − 6.642308×10⁷/T² + 1.2438×10¹⁰/T³ − 8.621949×10¹¹/T⁴ − S(1.7674×10⁻² − 10.754/T + 2140.7/T²)</p>

with C* in mg/L, T in kelvin and S in g/kg. The pressure correction is

<p class="formula">C<sub>P</sub> = C* × P × [(1 − P<sub>wv</sub>/P)(1 − θP)] / [(1 − P<sub>wv</sub>)(1 − θ)]</p>

where P is in atm, ln P<sub>wv</sub> = 11.8571 − 3840.70/T − 216961/T² and θ = 0.000975 − 1.426×10⁻⁵ t + 6.436×10⁻⁸ t² (t in °C).

## Worked example

Fresh water at 20 °C and 101.325 kPa:

- C* = **{o20:.3f} mg/L**
- A sample reading 7.5 mg/L is at **{7.5/o20*100:.1f}%** saturation
- At 90 kPa (about 1,000 m elevation) saturation falls to **{o20alt:.2f} mg/L**

## Dissolved oxygen saturation table (mg/L at 1 atm)

| Temperature | Fresh water | 10 g/kg | 20 g/kg | Seawater 35 g/kg |
|---|---|---|---|---|
{do_rows}
## Notes

- DO probes are calibrated in water-saturated air or air-saturated water using these saturation values.
- Biochemical oxygen demand (BOD) tests and aeration design both start from the saturation concentration.
''')

# ---------------------------------------------------------------- Bomb calorimeter
bC, bdT, bqf, bm, bM, bdn, bT = 10.0, 2.648, 50.0, 1.000, 122.12, -0.5, 298.15
bq = bC * 1000 * bdT - bqf; bUg = -bq / 1000 / bm; bn = bm / bM; bUm = -bq / 1000 / bn
bH = bUm + bdn * R * bT / 1000
fuels = [('Benzoic acid (calibration standard)', 122.12, 26.434), ('Sucrose', 342.30, 16.49), ('Naphthalene', 128.17, 40.13), ('Glucose', 180.16, 15.56), ('Ethanol', 46.07, 29.67)]
bf_rows = ''.join(f"| {nm} | {M:.2f} | {u:.2f} kJ/g | {u*M:,.0f} kJ/mol |\n" for nm, M, u in fuels)
P('chemistry', 'bomb-calorimeter', f'''
title: Bomb Calorimeter Calculator (Heat of Combustion ΔU & ΔH)
description: Calculate the heat of combustion from a bomb calorimeter run — heat released, ΔcU per gram and per mole, and ΔcH — from calorimeter constant, ΔT and mass.
category: chemistry
{intro("In a bomb calorimeter a sample burns in oxygen inside a sealed steel vessel, so the heat released raises the temperature of the calorimeter at constant volume. This bomb calorimeter calculator turns the calorimeter constant and temperature rise into the heat released, the energy of combustion ΔcU per gram and per mole, and the enthalpy of combustion ΔcH.")}
keywords: [bomb calorimeter calculator, heat of combustion calculator, bomb calorimetry formula, calorimeter constant, q = c delta t, enthalpy of combustion calculator, constant volume calorimetry]
updated: {D}
variables:
  - {{ id: C, label: Calorimeter heat capacity (constant), suffix: kJ/K, default: {bC:g}, min: 0 }}
  - {{ id: dT, label: Corrected temperature rise ΔT, family: tempdiff, unit: K, default: {bdT:g}, min: 0 }}
  - {{ id: qf, label: Fuse wire and other corrections, family: energy, unit: J, default: {bqf:g}, min: 0 }}
  - {{ id: m, label: Sample mass, family: mass, unit: g, imperialUnit: g, default: {bm:g}, min: 0 }}
  - {{ id: M, label: Molar mass of sample, suffix: g/mol, default: {bM:g}, min: 0 }}
  - {{ id: dn, label: Change in moles of gas Δn(g) per mole, default: {bdn:g}, help: 'Moles of gaseous products minus gaseous reactants (including O₂) per mole of fuel; water is taken as liquid.' }}
  - {{ id: T, label: Reference temperature, family: temperature, unit: C, imperialUnit: F, default: 25 }}
  - {{ id: q, label: Heat released by the sample, family: energy, unit: kJ, min: 0 }}
  - {{ id: Ug, label: Energy of combustion ΔcU per gram, suffix: kJ/g, decimals: 3 }}
  - {{ id: Um, label: Molar energy of combustion ΔcU, suffix: kJ/mol, decimals: 1 }}
  - {{ id: Hm, label: Molar enthalpy of combustion ΔcH, suffix: kJ/mol, decimals: 1 }}
equations:
  - q = C * 1000 * dT - qf
  - Ug = -q / 1000 / (m * 1000)
  - Um = -q / 1000 / (m * 1000 / M)
  - Hm = Um + dn * 8.314462618 * T / 1000
faq:
  - q: How do you calculate heat of combustion from a bomb calorimeter?
    a: q = C_cal × ΔT, minus corrections such as fuse wire. Divide by the sample mass for kJ/g, or by moles for kJ/mol, and make it negative because heat is released.
  - q: Why does a bomb calorimeter measure ΔU rather than ΔH?
    a: The bomb is sealed, so combustion happens at constant volume and no expansion work is done; the heat measured is the internal energy change. ΔH = ΔU + Δn(g)RT converts it to constant pressure.
  - q: How is the calorimeter constant found?
    a: By burning a known mass of benzoic acid, whose certified energy of combustion is about 26.434 kJ/g, and dividing the heat released by the measured temperature rise.
  - q: What is the difference between gross and net calorific value?
    a: The bomb gives the gross (higher) value because the water formed condenses. The net (lower) value subtracts the latent heat of that water.
related: [chemistry/specific-heat, chemistry/gibbs-free-energy, physics/final-temperature, physics/latent-heat]
''', f'''
## How to use the bomb calorimeter calculator

Enter the **calorimeter constant** (from a benzoic acid calibration), the **corrected temperature rise**, any **fuse wire or acid corrections**, the **sample mass** and its **molar mass**. For ΔH, enter **Δn(g)** from the balanced combustion equation per mole of sample.

## Bomb calorimetry formulas

<p class="formula">q = C<sub>cal</sub> × ΔT − q<sub>corr</sub> &nbsp;·&nbsp; Δ<sub>c</sub>U = −q / n &nbsp;·&nbsp; Δ<sub>c</sub>H = Δ<sub>c</sub>U + Δn<sub>g</sub>RT</p>

## Worked example: benzoic acid

C₆H₅COOH + 7.5 O₂ → 7 CO₂ + 3 H₂O(l), so Δn(g) = 7 − 7.5 = −0.5. A 1.000 g sample raises a 10.0 kJ/K calorimeter by 2.648 K, with a 50 J fuse correction:

- q = 10.0 × 2.648 − 0.050 = **{bq/1000:.2f} kJ**
- Δ<sub>c</sub>U = **{bUg:.2f} kJ/g** = {bUg:.2f} × 122.12 = **{bUm:,.1f} kJ/mol**
- Δ<sub>c</sub>H = {bUm:,.1f} + (−0.5)(8.314 × 10⁻³)(298.15) = **{bH:,.1f} kJ/mol**

## Typical energies of combustion (−Δ<sub>c</sub>U, approximate)

| Substance | Molar mass (g/mol) | Per gram | Per mole |
|---|---|---|---|
{bf_rows}
## Notes

- Correct ΔT for heat exchange with the surroundings (Regnault–Pfaundler or graphical extrapolation).
- Nitric and sulfuric acid formed from N and S in the sample release extra heat — titrate the bomb washings to correct for it.
''')

# ======================================================================= MATH

# ---------------------------------------------------------------- 2x2 system
a1, b1, c1, a2, b2, c2 = 2, 3, 13, 1, -1, -1
D2 = a1 * b2 - a2 * b1; x2 = (c1 * b2 - c2 * b1) / D2; y2 = (a1 * c2 - a2 * c1) / D2
P('math', 'system-of-equations', f'''
title: System of Equations Calculator (2 Variables, Cramer's Rule)
description: Solve a system of two linear equations in x and y with Cramer's rule — shows the determinant and tells you when there is no unique solution.
category: math
{intro("A system of two linear equations ax + by = c has one solution where the two lines cross, none if they are parallel and infinitely many if they are the same line. This system of equations calculator solves for x and y with Cramer's rule and shows the determinant, which is zero exactly when there is no unique solution.")}
keywords: [system of equations calculator, simultaneous equations calculator, solve two equations two unknowns, cramer's rule calculator, linear equations solver 2x2, solve for x and y, elimination method calculator]
updated: {D}
variables:
  - {{ id: a1, label: a₁ (x coefficient, equation 1), default: {a1} }}
  - {{ id: b1, label: b₁ (y coefficient, equation 1), default: {b1} }}
  - {{ id: c1, label: c₁ (right-hand side, equation 1), default: {c1} }}
  - {{ id: a2, label: a₂ (x coefficient, equation 2), default: {a2} }}
  - {{ id: b2, label: b₂ (y coefficient, equation 2), default: {b2} }}
  - {{ id: c2, label: c₂ (right-hand side, equation 2), default: {c2} }}
  - {{ id: Dt, label: Determinant D = a₁b₂ − a₂b₁, decimals: 6 }}
  - {{ id: x, label: x, decimals: 6 }}
  - {{ id: y, label: y, decimals: 6 }}
equations:
  - Dt = a1 * b2 - a2 * b1
  - x = (c1 * b2 - c2 * b1) / Dt
  - y = (a1 * c2 - a2 * c1) / Dt
faq:
  - q: How do you solve two equations with two unknowns?
    a: By substitution, elimination or Cramer's rule. With Cramer's rule, x = (c₁b₂ − c₂b₁)/D and y = (a₁c₂ − a₂c₁)/D, where D = a₁b₂ − a₂b₁.
  - q: What does a determinant of zero mean?
    a: The lines are parallel (no solution) or identical (infinitely many solutions). Check whether one equation is a multiple of the other.
  - q: How do I enter an equation like y = 2x + 1?
    a: Rearrange it to the form ax + by = c first, i.e. −2x + y = 1, so a = −2, b = 1 and c = 1.
  - q: How can I check the answer?
    a: Substitute x and y back into both original equations — each left-hand side should equal its right-hand side.
related: [math/system-of-3-equations, math/quadratic-equation, math/slope, math/linear-interpolation]
''', f'''
## How to use the system of equations calculator

Write both equations in the form **a·x + b·y = c** and enter the six coefficients. The calculator returns the determinant and the solution. If the determinant is 0, the equations have no unique solution.

## Cramer's rule for two equations

<p class="formula">D = a₁b₂ − a₂b₁ &nbsp;·&nbsp; x = (c₁b₂ − c₂b₁) / D &nbsp;·&nbsp; y = (a₁c₂ − a₂c₁) / D</p>

## Worked example

Solve 2x + 3y = 13 and x − y = −1:

- D = 2 × (−1) − 1 × 3 = **{D2}**
- x = (13 × (−1) − (−1) × 3) ÷ ({D2}) = **{x2:g}**
- y = (2 × (−1) − 1 × 13) ÷ ({D2}) = **{y2:g}**
- Check: 2(2) + 3(3) = 13 ✓ and 2 − 3 = −1 ✓

## Solving by elimination

1. Multiply the equations so one variable has equal and opposite coefficients.
2. Add the equations to eliminate that variable and solve for the other.
3. Substitute back to find the first variable.

## Types of solution

| Determinant | Lines | Solutions |
|---|---|---|
| D ≠ 0 | Intersect at one point | Exactly one |
| D = 0, equations proportional | Same line | Infinitely many |
| D = 0, not proportional | Parallel | None |
''')

# ---------------------------------------------------------------- 3x3 system
A3 = [[1, 1, 1], [2, -1, 3], [1, 2, -1]]; d3 = [6, 9, 2]
def det3(M): return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
                     + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
def repl(M, j): return [[d3[i] if k == j else M[i][k] for k in range(3)] for i in range(3)]
DD = det3(A3); Dx, Dy, Dz = det3(repl(A3, 0)), det3(repl(A3, 1)), det3(repl(A3, 2))
vars3 = ''
for i in range(3):
    for k, nm in enumerate('abc'):
        vars3 += f"  - {{{{ id: {nm}{i+1}, label: {nm}{'₁₂₃'[i]} ({'xyz'[k]} coefficient, equation {i+1}), default: {A3[i][k]} }}}}\n"
    vars3 += f"  - {{{{ id: d{i+1}, label: d{'₁₂₃'[i]} (right-hand side, equation {i+1}), default: {d3[i]} }}}}\n"
vars3 = vars3.replace('{{', '{').replace('}}', '}')
DET = 'a1 * (b2 * c3 - c2 * b3) - b1 * (a2 * c3 - c2 * a3) + c1 * (a2 * b3 - b2 * a3)'
P('math', 'system-of-3-equations', f'''
title: 3 Variable System of Equations Calculator (Cramer's Rule)
description: Solve three linear equations in x, y and z with Cramer's rule — enter the coefficients to get the determinant, Dx, Dy, Dz and the unique solution.
category: math
{intro("Three linear equations in three unknowns describe three planes, and when they meet at a single point the system has one solution. This 3 variable system of equations calculator finds that point with Cramer's rule, showing the coefficient determinant and the three replacement determinants so you can follow the working.")}
keywords: [3 variable system of equations calculator, system of 3 equations calculator, three equations three unknowns, cramer's rule 3x3, solve for x y z, 3x3 determinant calculator, simultaneous equations 3 variables]
updated: {D}
variables:
{vars3.rstrip()}
  - {{ id: Dt, label: Determinant D, decimals: 6 }}
  - {{ id: Dx, label: Dx (x column replaced by d), decimals: 6 }}
  - {{ id: Dy, label: Dy (y column replaced by d), decimals: 6 }}
  - {{ id: Dz, label: Dz (z column replaced by d), decimals: 6 }}
  - {{ id: x, label: x = Dx ÷ D, decimals: 6 }}
  - {{ id: y, label: y = Dy ÷ D, decimals: 6 }}
  - {{ id: z, label: z = Dz ÷ D, decimals: 6 }}
equations:
  - Dt = {DET}
  - Dx = {DET.replace('a1', 'd1').replace('a2', 'd2').replace('a3', 'd3')}
  - Dy = {DET.replace('b1', 'd1').replace('b2', 'd2').replace('b3', 'd3')}
  - Dz = {DET.replace('c1', 'd1').replace('c2', 'd2').replace('c3', 'd3')}
  - x = Dx / Dt
  - y = Dy / Dt
  - z = Dz / Dt
faq:
  - q: How do you solve 3 equations with 3 variables?
    a: Use elimination to reduce to two equations in two unknowns, or Cramer's rule — x = Dx/D, y = Dy/D, z = Dz/D, where each D is a 3×3 determinant.
  - q: How is a 3×3 determinant calculated?
    a: By cofactor expansion along the first row, D = a₁(b₂c₃ − c₂b₃) − b₁(a₂c₃ − c₂a₃) + c₁(a₂b₃ − b₂a₃).
  - q: What if the determinant is zero?
    a: There is no unique solution — the planes are parallel or meet in a line, giving no solutions or infinitely many. Gaussian elimination tells you which.
  - q: Is Cramer's rule efficient?
    a: For 2×2 and 3×3 systems it is quick and clear. For larger systems Gaussian elimination or matrix methods are far more efficient.
related: [math/system-of-equations, math/quadratic-equation, math/vector, math/linear-interpolation]
''', f'''
## How to use the 3 variable system of equations calculator

Write each equation as **a·x + b·y + c·z = d** and enter its four numbers. Use 0 for a missing variable. The calculator returns D, Dx, Dy, Dz and the solution; if D = 0 there is no unique solution.

## Cramer's rule for three equations

<p class="formula">D = a₁(b₂c₃ − c₂b₃) − b₁(a₂c₃ − c₂a₃) + c₁(a₂b₃ − b₂a₃)</p>

<p class="formula">x = D<sub>x</sub>/D &nbsp;·&nbsp; y = D<sub>y</sub>/D &nbsp;·&nbsp; z = D<sub>z</sub>/D</p>

D<sub>x</sub>, D<sub>y</sub> and D<sub>z</sub> are the same determinant with the x, y or z column replaced by the right-hand sides d.

## Worked example

Solve x + y + z = 6, 2x − y + 3z = 9 and x + 2y − z = 2:

- D = 1(1 − 6) − 1(−2 − 3) + 1(4 + 1) = **{DD}**
- D<sub>x</sub> = **{Dx}**, D<sub>y</sub> = **{Dy}**, D<sub>z</sub> = **{Dz}**
- x = {Dx}/{DD} = **{Dx/DD:g}**, y = {Dy}/{DD} = **{Dy/DD:g}**, z = {Dz}/{DD} = **{Dz/DD:g}**
- Check: 1 + 2 + 3 = 6 ✓, 2 − 2 + 9 = 9 ✓, 1 + 4 − 3 = 2 ✓

## Solving by elimination

1. Use equation 1 to eliminate x from equations 2 and 3.
2. Solve the resulting two equations in y and z (see the [two-variable system of equations calculator](/math/system-of-equations/)).
3. Substitute y and z back into equation 1 to find x.
''')

# ---------------------------------------------------------------- Pyramid volume
pl, pw, ph = 6.0, 6.0, 4.0
pV = pl * pw * ph / 3; psl = math.hypot(ph, pw / 2); psw = math.hypot(ph, pl / 2)
pLA = pl * psl + pw * psw; pTA = pLA + pl * pw; pe = math.sqrt(ph**2 + (pl / 2)**2 + (pw / 2)**2)
py_rows = ''
for s, h in ((1, 1), (2, 1.5), (3, 2), (5, 3), (10, 6), (230.3, 146.6)):
    py_rows += f"| {s:g} m | {h:g} m | {s*s*h/3:,.3f} m³ | {s*s + 2*s*math.hypot(h, s/2):,.3f} m² |\n"
P('math', 'pyramid-volume', f'''
title: Pyramid Volume Calculator (Volume, Slant Height & Surface Area)
description: Calculate the volume, slant heights, edge length, lateral area and total surface area of a right rectangular or square pyramid from its base and height.
category: math
{intro("A pyramid holds exactly one third of the volume of a prism with the same base and height. This pyramid volume calculator handles right rectangular and square pyramids, giving the volume together with the slant heights, lateral edge length, lateral area and total surface area.")}
keywords: [pyramid volume calculator, volume of a pyramid, square pyramid calculator, pyramid surface area calculator, slant height of pyramid, rectangular pyramid volume, pyramid formula]
updated: {D}
variables:
  - {{ id: l, label: Base length, family: length, unit: m, imperialUnit: ft, default: {pl:g}, min: 0 }}
  - {{ id: w, label: Base width, family: length, unit: m, imperialUnit: ft, default: {pw:g}, min: 0 }}
  - {{ id: h, label: Height (apex to base), family: length, unit: m, imperialUnit: ft, default: {ph:g}, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: sl, label: Slant height to the length edges, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: sw, label: Slant height to the width edges, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: ed, label: Lateral edge length, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: LA, label: Lateral surface area, family: area, unit: m2, imperialUnit: ft2, min: 0 }}
  - {{ id: TA, label: Total surface area, family: area, unit: m2, imperialUnit: ft2, min: 0 }}
equations:
  - V = l * w * h / 3
  - sl = sqrt(h^2 + (w / 2)^2)
  - sw = sqrt(h^2 + (l / 2)^2)
  - ed = sqrt(h^2 + (l / 2)^2 + (w / 2)^2)
  - LA = l * sl + w * sw
  - TA = LA + l * w
faq:
  - q: What is the formula for the volume of a pyramid?
    a: V = (1/3) × base area × height. For a rectangular base, V = l × w × h ÷ 3; for a square base of side a, V = a²h ÷ 3.
  - q: How do I find the slant height of a pyramid?
    a: For a right pyramid, the slant height to an edge of length l is √(h² + (w/2)²) — the hypotenuse of the triangle formed by the height and half the other base side.
  - q: What is the surface area of a square pyramid?
    a: Total area = a² + 2a·s, where s = √(h² + (a/2)²) is the slant height. The four triangular faces each have area a·s/2.
  - q: Does the formula work for any base shape?
    a: The volume V = Bh/3 works for any base — triangular, hexagonal or circular (a cone) — as long as h is the perpendicular height. The slant and surface formulas here are for rectangular bases.
related: [math/frustum-volume, math/cone, math/box-volume, math/pythagorean-theorem]
''', f'''
## How to use the pyramid volume calculator

Enter the **base length**, **base width** and perpendicular **height** of a right pyramid (apex directly above the centre of the base). For a square pyramid make length and width equal. The calculator returns the volume, both slant heights, the lateral edge and the surface areas.

## Pyramid formulas

<p class="formula">V = l w h / 3 &nbsp;·&nbsp; s<sub>l</sub> = √(h² + (w/2)²) &nbsp;·&nbsp; s<sub>w</sub> = √(h² + (l/2)²)</p>

<p class="formula">Lateral area = l·s<sub>l</sub> + w·s<sub>w</sub> &nbsp;·&nbsp; Total area = lateral area + l·w &nbsp;·&nbsp; edge = √(h² + (l/2)² + (w/2)²)</p>

## Worked example

A square pyramid with a 6 m × 6 m base and 4 m height:

- V = 6 × 6 × 4 ÷ 3 = **{pV:g} m³**
- Slant height = √(4² + 3²) = **{psl:g} m**
- Lateral area = 6 × 5 + 6 × 5 = **{pLA:g} m²**; total area = **{pTA:g} m²**
- Lateral edge = √(16 + 9 + 9) = **{pe:.3f} m**

## Square pyramids

| Base side | Height | Volume | Total surface area |
|---|---|---|---|
{py_rows}
The last row uses the Great Pyramid of Giza's approximate original dimensions (230.3 m base, 146.6 m height).
''')

# ---------------------------------------------------------------- Frustum volume
fR, fr, fh = 5.0, 3.0, 4.0     # cm
fV = pi * fh / 3 * (fR**2 + fR * fr + fr**2); fs = math.hypot(fh, fR - fr)
fL = pi * (fR + fr) * fs; fT = fL + pi * (fR**2 + fr**2)
fb_rows = ''
for D_, d_, h_ in ((30, 25, 30), (28, 24, 26), (32, 26, 35), (40, 30, 40), (60, 45, 70)):
    v = pi * h_ / 3 * ((D_/2)**2 + (D_/2)*(d_/2) + (d_/2)**2) / 1000
    fb_rows += f"| {D_} cm | {d_} cm | {h_} cm | {v:.2f} L |\n"
P('math', 'frustum-volume', f'''
title: Frustum Volume Calculator (Truncated Cone)
description: Calculate the volume, slant height, lateral area and total surface area of a conical frustum (truncated cone) from the two radii and height.
category: math
{intro("A frustum is a cone with its top cut off parallel to the base — the shape of buckets, flower pots, lampshades and many hoppers. This frustum volume calculator gives the volume, slant height, lateral area and total surface area of a conical frustum from the bottom and top radii and the height.")}
keywords: [frustum volume calculator, truncated cone volume, volume of a frustum, frustum of a cone calculator, bucket volume calculator, frustum surface area, tapered tub volume]
updated: {D}
variables:
  - {{ id: R, label: Large (base) radius R, family: length, unit: cm, imperialUnit: in, default: {fR:g}, min: 0 }}
  - {{ id: r, label: Small (top) radius r, family: length, unit: cm, imperialUnit: in, default: {fr:g}, min: 0 }}
  - {{ id: h, label: Height h, family: length, unit: cm, imperialUnit: in, default: {fh:g}, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: cm3, imperialUnit: in3, min: 0 }}
  - {{ id: s, label: Slant height, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: LA, label: Lateral (side) surface area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
  - {{ id: TA, label: Total surface area (with both ends), family: area, unit: cm2, imperialUnit: in2, min: 0 }}
equations:
  - V = pi * h / 3 * (R^2 + R * r + r^2)
  - s = sqrt(h^2 + (R - r)^2)
  - LA = pi * (R + r) * s
  - TA = LA + pi * (R^2 + r^2)
faq:
  - q: What is the formula for the volume of a frustum?
    a: V = (πh/3)(R² + Rr + r²), where R and r are the radii of the two circular ends and h is the perpendicular height.
  - q: How do I find the slant height of a frustum?
    a: s = √(h² + (R − r)²). The lateral surface area is then π(R + r)s.
  - q: How do I calculate the volume of a bucket?
    a: Measure the top and bottom diameters and the depth, halve the diameters to get radii, and use the frustum formula. Divide cm³ by 1,000 for litres.
  - q: What about a square or rectangular frustum?
    a: For any frustum with similar parallel ends of areas A₁ and A₂, V = (h/3)(A₁ + A₂ + √(A₁A₂)). For a square frustum with sides a and b that is (h/3)(a² + ab + b²).
related: [math/cone, math/cylinder-volume, math/pyramid-volume, math/sphere]
''', f'''
## How to use the frustum volume calculator

Enter the **large radius**, the **small radius** and the **height** between the two parallel faces. For a bucket or pot measured by diameter, halve each diameter first. The calculator gives the volume, the slant height and the surface areas.

## Frustum formulas

<p class="formula">V = (π h / 3)(R² + R r + r²) &nbsp;·&nbsp; s = √(h² + (R − r)²)</p>

<p class="formula">Lateral area = π (R + r) s &nbsp;·&nbsp; Total area = π (R + r) s + π R² + π r²</p>

## Worked example

R = 5 cm, r = 3 cm, h = 4 cm:

- V = (π × 4 ÷ 3)(25 + 15 + 9) = **{fV:.2f} cm³**
- Slant height = √(16 + 4) = **{fs:.3f} cm**
- Lateral area = π × 8 × {fs:.3f} = **{fL:.2f} cm²**; total area = **{fT:.2f} cm²**

## Bucket and tub volumes

| Top diameter | Bottom diameter | Depth | Volume |
|---|---|---|---|
{fb_rows}
## Notes

- If r = 0 the formula becomes the cone volume πR²h/3; if r = R it becomes the cylinder πR²h.
- For a partly filled bucket, use the radius at the liquid surface as the top radius and the liquid depth as h.
''')

# ---------------------------------------------------------------- Torus
tR, tr = 10.0, 3.0     # cm
tV = 2 * pi**2 * tR * tr**2; tA = 4 * pi**2 * tR * tr
to_rows = ''
for name, R_, r_ in (('Bagel', 4.5, 2.0), ('Doughnut', 4.0, 2.5), ('O-ring 100 × 5 mm', 5.25, 0.25), ('Swim ring', 25, 10), ('Car tyre inner tube', 30, 9)):
    to_rows += f"| {name} | {R_:g} cm | {r_:g} cm | {2*pi**2*R_*r_**2:,.1f} cm³ | {4*pi**2*R_*r_:,.1f} cm² |\n"
P('math', 'torus', f'''
title: Torus Volume Calculator (Volume & Surface Area)
description: Calculate the volume and surface area of a torus (doughnut or ring shape) from its major and minor radii, plus the inner and outer diameters of the ring.
category: math
{intro("A torus is the doughnut shape made by sweeping a circle of radius r around an axis at distance R from its centre. This torus volume calculator gives the volume and surface area with Pappus's theorem, along with the inner and outer diameters — handy for O-rings, inner tubes and ring-shaped tanks.")}
keywords: [torus volume calculator, volume of a torus, torus surface area calculator, doughnut volume formula, ring volume calculator, o-ring volume, pappus theorem torus]
updated: {D}
variables:
  - {{ id: R, label: Major radius R (centre of torus to centre of tube), family: length, unit: cm, imperialUnit: in, default: {tR:g}, min: 0 }}
  - {{ id: r, label: Minor radius r (radius of the tube), family: length, unit: cm, imperialUnit: in, default: {tr:g}, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: cm3, imperialUnit: in3, min: 0 }}
  - {{ id: A, label: Surface area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
  - {{ id: Di, label: Inner diameter, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: Do, label: Outer diameter, family: length, unit: cm, imperialUnit: in, min: 0 }}
equations:
  - V = 2 * pi^2 * R * r^2
  - A = 4 * pi^2 * R * r
  - Di = 2 * (R - r)
  - Do = 2 * (R + r)
faq:
  - q: What is the volume of a torus?
    a: V = 2π²Rr², where R is the distance from the centre of the torus to the centre of the tube and r is the tube radius. It equals the tube's cross-section area πr² times the path length 2πR.
  - q: What is the surface area of a torus?
    a: A = 4π²Rr — the tube circumference 2πr times the path length 2πR.
  - q: How do I get R and r from inner and outer diameters?
    a: r = (outer − inner) ÷ 4 and R = (outer + inner) ÷ 4. An O-ring of 90 mm inner diameter and 5 mm section has r = 2.5 mm and R = 47.5 mm.
  - q: What if r is larger than R?
    a: The tube overlaps itself (a spindle torus) and the formulas overcount the volume. They are valid for r ≤ R.
related: [math/sphere, math/cylinder-volume, math/circle, math/frustum-volume]
''', f'''
## How to use the torus volume calculator

Enter the **major radius R** — from the centre of the hole to the centre of the tube — and the **minor radius r** of the tube itself. The calculator returns the volume, the surface area and the inner and outer diameters of the ring. If you have diameters, R = (D<sub>outer</sub> + D<sub>inner</sub>)/4 and r = (D<sub>outer</sub> − D<sub>inner</sub>)/4.

## Torus formulas

<p class="formula">V = 2π² R r² &nbsp;·&nbsp; A = 4π² R r</p>

These follow from Pappus's centroid theorems: the volume is the cross-section area times the distance its centroid travels, and the area is the cross-section perimeter times that distance.

## Worked example

R = 10 cm, r = 3 cm:

- V = 2π² × 10 × 9 = **{tV:,.2f} cm³** ({tV/1000:.3f} L)
- A = 4π² × 10 × 3 = **{tA:,.2f} cm²**
- Inner diameter = **{2*(tR-tr):g} cm**, outer diameter = **{2*(tR+tr):g} cm**

## Everyday tori (approximate)

| Object | R | r | Volume | Surface area |
|---|---|---|---|---|
{to_rows}''')

# ---------------------------------------------------------------- Modulo
ma_, mb_ = 17, 5
mo_rows = ''
for a_, b_ in ((17, 5), (-17, 5), (17, -5), (-17, -5), (100, 7), (2026, 12), (5.5, 2)):
    fl = math.floor(a_ / b_); tq = int(a_ / b_)
    mo_rows += f"| {a_:g} | {b_:g} | {fl} | {a_ - b_*fl:g} | {a_ - b_*tq:g} |\n"
P('math', 'modulo', f'''
title: Modulo Calculator (a mod b, Remainder & Quotient)
description: Calculate a mod b, the quotient and the remainder for positive and negative numbers — showing the floored modulo and the truncated remainder used in C and Java.
category: math
{intro("The modulo operation gives the remainder left after dividing one number by another, the basis of clock arithmetic, check digits and cyclic counters. This modulo calculator returns a mod b, the integer quotient and the remainder, and shows how the result differs for negative numbers between mathematical (floored) modulo and the truncated remainder of C, Java and JavaScript.")}
keywords: [modulo calculator, mod calculator, a mod b, remainder calculator, modulus calculator, negative modulo, modular arithmetic calculator]
updated: {D}
variables:
  - {{ id: a, label: Dividend a, default: {ma_} }}
  - {{ id: b, label: Divisor b (modulus), default: {mb_} }}
  - {{ id: q, label: Quotient floor(a ÷ b), decimals: 0 }}
  - {{ id: m, label: a mod b (floored, sign of b), decimals: 6 }}
  - {{ id: rt, label: Truncated remainder (C / Java / JavaScript %), decimals: 6 }}
equations:
  - q = floor(a / b)
  - m = mod(a, b)
  - rt = a - b * sign(a / b) * floor(abs(a / b))
faq:
  - q: What is a mod b?
    a: The remainder after dividing a by b, so that a = b × q + (a mod b). For example 17 mod 5 = 2, because 17 = 5 × 3 + 2.
  - q: What is −17 mod 5?
    a: In mathematics (floored division) it is 3, because −17 = 5 × (−4) + 3. In C, Java and JavaScript, −17 % 5 gives −2, because they truncate the quotient towards zero.
  - q: Which languages use floored modulo?
    a: Python's %, Ruby, and spreadsheet MOD() return a result with the sign of the divisor (floored). C, C++, Java, JavaScript and C# return a result with the sign of the dividend (truncated).
  - q: Can modulo be used with decimals?
    a: Yes. 5.5 mod 2 = 1.5. Floating-point rounding can make results like 0.3 mod 0.1 come out very slightly off zero.
related: [math/gcf-lcm, math/fraction-to-decimal, math/factorial, math/exponent]
''', f'''
## How to use the modulo calculator

Enter the **dividend a** and the **divisor b**. The calculator returns the floored quotient, **a mod b** (the mathematical modulo, which always has the sign of b) and the **truncated remainder** that the % operator gives in C-family languages. For positive numbers the two are the same.

## Modulo formula

<p class="formula">a mod b = a − b × ⌊a ÷ b⌋ &nbsp;·&nbsp; truncated remainder = a − b × trunc(a ÷ b)</p>

## Worked example

17 mod 5:

- 17 ÷ 5 = 3.4, so the quotient is **3**
- 17 − 5 × 3 = **2**, so 17 mod 5 = 2

## Floored vs truncated

| a | b | ⌊a/b⌋ | a mod b (floored) | a % b (truncated) |
|---|---|---|---|---|
{mo_rows}
## Uses of modular arithmetic

- **Clock time** — 15:00 + 10 hours = 25 mod 24 = 01:00.
- **Even and odd** — n mod 2 is 0 for even numbers, 1 for odd.
- **Check digits** — ISBN-10 uses mod 11, IBAN uses mod 97.
- **Cyclic counters and ring buffers** — index = (index + 1) mod size.
''')

print(len(DESC), 'pages:', ' '.join(DESC))
