"""Batch 2026-11-09 — 6 calculators: electronics (LC low-pass filter, flyback transformer),
engineering (NPSH available, dew point), statistics (X-bar & R control chart), math (cubic equation).
All reference tables are computed here; defaults match the worked examples."""
import sys, math, os, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro
D = '2026-11-09'
pi = math.pi
DESC = []
def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    t = re.search(r'^intro: (.*)$', fm, re.M).group(1)
    assert 'featured' not in fm
    DESC.append(slug)
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)  # typographic minus for negative numbers in the text
    page(cat, slug, fm, body)

def eng(x, unit, d=3):
    """engineering-prefix formatting, e.g. 5.9 kHz"""
    for f, p in ((1e9, 'G'), (1e6, 'M'), (1e3, 'k'), (1, ''), (1e-3, 'm'), (1e-6, 'µ'), (1e-9, 'n'), (1e-12, 'p')):
        if abs(x) >= f * 0.9995:
            return f"{float(f'{x/f:.{d}g}'):g} {p}{unit}"
    return f"{x:.3g} {unit}"

# ======================================================================= ELECTRONICS

# ---------------------------------------------------------------- LC low-pass filter
lL, lC, lR, lf = 33e-6, 22e-6, 1.2, 100e3
def lc(L, C, R, f):
    f0 = 1 / (2 * pi * math.sqrt(L * C)); Z0 = math.sqrt(L / C); Q = R / Z0; x = f / f0
    H = 1 / math.sqrt((1 - x * x) ** 2 + (x / Q) ** 2)
    return f0, Z0, Q, x, H, 20 * math.log10(H), 20 * math.log10(Q)
lf0, lZ0, lQ, lx, lH, lA, lG = lc(lL, lC, lR, lf)
lc_rows = ''
for L, C in ((10e-6, 10e-6), (22e-6, 47e-6), (33e-6, 22e-6), (47e-6, 100e-6), (100e-6, 100e-6), (1e-3, 10e-6), (10e-3, 1e-6)):
    f0 = 1 / (2 * pi * math.sqrt(L * C)); Z0 = math.sqrt(L / C)
    lc_rows += f"| {eng(L, 'H')} | {eng(C, 'F')} | {eng(f0, 'Hz')} | {Z0:.3g} Ω |\n"
lq_rows = ''
for x in (0.5, 1, 2, 5, 10, 100):
    cells = []
    for Q in (0.5, 0.707, 1.0, 2.0, 5.0):
        H = 1 / math.sqrt((1 - x * x) ** 2 + (x / Q) ** 2); cells.append(f"{20*math.log10(H):+.1f} dB")
    lq_rows += f"| {x:g} × f₀ | " + ' | '.join(cells) + " |\n"
P('electronics', 'lc-filter', f'''
title: LC Filter Calculator (Low-Pass Cutoff, Q & Attenuation)
description: Calculate the cutoff frequency, characteristic impedance, Q factor and attenuation of a second-order LC low-pass filter driving a resistive load.
category: electronics
{intro("A series inductor followed by a shunt capacitor makes a second-order low-pass filter that falls at 40 dB per decade above its cutoff — the output filter of every [buck converter](ib:buck-converter-working-principle), and a common supply and audio filter. This LC filter calculator gives the cutoff frequency, the characteristic impedance √(L/C), the Q factor set by the load and the attenuation at any frequency, so you can check both ripple rejection and resonant peaking.")}
keywords: [lc filter calculator, lc low pass filter calculator, lc filter cutoff frequency, lc filter design, second order low pass filter, lc filter q factor, output filter attenuation]
updated: {D}
variables:
  - {{ id: L, label: Inductance L (series), family: inductance, unit: uH, default: {lL*1e6:g}, min: 0 }}
  - {{ id: C, label: Capacitance C (shunt), family: capacitance, unit: uF, default: {lC*1e6:g}, min: 0 }}
  - {{ id: R, label: Load resistance R, family: resistance, unit: ohm, default: {lR:g}, min: 0, help: 'The resistance across the capacitor — e.g. output voltage ÷ load current.' }}
  - {{ id: f, label: Frequency to check, family: frequency, unit: kHz, default: {lf/1e3:g}, min: 0, help: 'For a switching supply, the switching frequency (ripple frequency).' }}
  - {{ id: f0, label: Cutoff (resonant) frequency f₀, family: frequency, unit: Hz, min: 0 }}
  - {{ id: Z0, label: Characteristic impedance √(L/C), family: resistance, unit: ohm, min: 0 }}
  - id: Q
    label: Q factor with this load
    min: 0
    decimals: 3
    bands:
      - {{ max: 0.5, label: Over-damped — slow roll-off near f₀, color: '#eab308' }}
      - {{ max: 1.0, label: Well damped (0.5–1) — little or no peaking, color: '#16a34a' }}
      - {{ max: 2.0, label: Some peaking at f₀, color: '#f97316' }}
      - {{ max: 1e9, label: High peaking — add damping, color: '#dc2626' }}
  - {{ id: x, label: Frequency ratio f ÷ f₀, min: 0, decimals: 3 }}
  - {{ id: H, label: Gain at the chosen frequency (Vout ÷ Vin), min: 0, decimals: 6 }}
  - {{ id: AdB, label: Gain at the chosen frequency, suffix: dB, decimals: 1 }}
  - {{ id: G0, label: Gain at f₀ (peaking), suffix: dB, decimals: 2 }}
equations:
  - f0 = 1 / (2 * pi * sqrt(L * C))
  - Z0 = sqrt(L / C)
  - Q = R / Z0
  - x = f / f0
  - H = 1 / sqrt((1 - x^2)^2 + (x / Q)^2)
  - AdB = 20 * log10(H)
  - G0 = 20 * log10(Q)
faq:
  - q: What is the cutoff frequency of an LC filter?
    a: f₀ = 1 ÷ (2π√(LC)), with L in henries and C in farads. Above f₀ the output falls at 40 dB per decade (12 dB per octave), twice as fast as an RC filter.
  - q: What does the load resistance do to an LC filter?
    a: It sets the damping. Q = R ÷ √(L/C). A light load (high R) gives a high Q and a resonant peak at f₀; a load near √(L/C) gives Q ≈ 1 and a flat response. At Q = 0.707 the response is maximally flat (Butterworth).
  - q: How much does an LC filter attenuate ripple?
    a: Well above f₀ the gain is about (f₀ ÷ f)². A filter with f₀ = 1 kHz reduces 100 kHz ripple by about 10,000 times (−80 dB), before capacitor ESR and ESL limit it.
  - q: How do I damp an LC filter?
    a: Add resistance in series with an extra capacitor across C (an RC damper), use a capacitor with suitable ESR, or put a resistor in parallel with the inductor. The damper should give an effective Q of about 0.5–1.
related: [electronics/resonant-frequency, electronics/rc-filter, electronics/buck-converter, electronics/reactance]
''', f'''
## How to use the LC filter calculator

Enter the series **inductance**, the shunt **capacitance**, the **load resistance** across the capacitor and a **frequency to check** (for a switching regulator, the switching frequency). The calculator gives the cutoff frequency, the characteristic impedance, the Q factor and the gain at your frequency as a ratio and in dB, plus the gain at f₀, which shows how much the filter peaks. To design for a target cutoff, enter f₀ and the inductance and press × on Capacitance.

## LC low-pass filter formulas

<p class="formula">f₀ = 1 ÷ (2π√(LC)) &nbsp;·&nbsp; Z₀ = √(L ÷ C) &nbsp;·&nbsp; Q = R ÷ Z₀</p>

<p class="formula">|H(f)| = 1 ÷ √[(1 − x²)² + (x ÷ Q)²], &nbsp; x = f ÷ f₀</p>

At f = f₀ the gain equals Q. Far above f₀ it approaches 1 ÷ x², i.e. −40 dB per decade. The formula is for ideal parts — the ESR of the capacitor adds damping but also a zero that flattens the roll-off at high frequency.

## Worked example

A buck converter output filter with L = {lL*1e6:g} µH, C = {lC*1e6:g} µF and a {lR:g} Ω load, switching at {lf/1e3:g} kHz:

- f₀ = 1 ÷ (2π√({lL*1e6:g} µH × {lC*1e6:g} µF)) = **{lf0:,.0f} Hz**
- Z₀ = √({lL*1e6:g} µH ÷ {lC*1e6:g} µF) = **{lZ0:.4f} Ω**, so Q = {lR:g} ÷ {lZ0:.4f} = **{lQ:.3f}** — well damped
- At {lf/1e3:g} kHz, x = {lx:.3f} and the gain is **{lH:.6f}** = **{lA:.1f} dB**, so the ripple is reduced about {1/lH:,.0f} times
- Gain at f₀ = 20 log₁₀({lQ:.3f}) = **{lG:.2f} dB** — no significant peaking

## Cutoff frequency and characteristic impedance

| L | C | f₀ | Z₀ = √(L/C) |
|---|---|---|---|
{lc_rows}
## Gain versus frequency and Q

| Frequency | Q = 0.5 | Q = 0.707 | Q = 1 | Q = 2 | Q = 5 |
|---|---|---|---|---|---|
{lq_rows}
## Practical notes

- **Light load = high Q.** A converter filter that is well damped at full load can ring at no load; check Q at the minimum load too.
- Place f₀ at least a decade below the switching frequency, and well away from the control-loop crossover frequency of the regulator.
- Use the capacitance **at the working voltage** — ceramic X5R/X7R capacitors can lose 50% or more of their value under DC bias.
- The inductor must not saturate at the peak load current, and its self-resonant frequency limits attenuation at very high frequencies.
- An LC input filter in front of a switching regulator can make it oscillate (negative input impedance); its output impedance Z₀ should be well below the regulator's input impedance.
''')

# ---------------------------------------------------------------- Flyback transformer
fVmin, fVmax, fVo, fVf, fD, fPo, feta, ffs = 18.0, 32.0, 5.0, 0.5, 0.45, 10.0, 0.80, 100e3
def fly(Vmin, Vmax, Vo, Vf, Dm, Po, eta, fs):
    n_ = Vmin * Dm / ((1 - Dm) * (Vo + Vf)); Vor = n_ * (Vo + Vf); Vds = Vmax + Vor
    Pin = Po / eta; Ipk = 2 * Pin / (Vmin * Dm); Lp = Vmin * Dm / (Ipk * fs); Isp = n_ * Ipk; Dmin = Vor / (Vor + Vmax)
    return n_, Vor, Vds, Pin, Ipk, Lp, Isp, Dmin
fn, fVor, fVds, fPin, fIpk, fLp, fIsp, fDmin = fly(fVmin, fVmax, fVo, fVf, fD, fPo, feta, ffs)
fl_rows = ''
# universal AC input: bulk capacitor minimum ≈ 100 V DC, maximum 265 V × √2 ≈ 375 V
for Vo, Vf in ((5, 0.5), (12, 0.7), (24, 0.7)):
    for Dm in (0.40, 0.45, 0.50):
        r = fly(100, 375, Vo, Vf, Dm, 20, 0.85, 65e3)
        fl_rows += f"| {Vo} V | {Dm*100:.0f}% | {r[0]:.2f} | {r[1]:.0f} V | {r[2]:.0f} V |\n"
P('electronics', 'flyback-transformer', f'''
title: Flyback Transformer Calculator (Turns Ratio & Inductance)
description: Calculate flyback transformer turns ratio, reflected voltage, switch voltage stress, peak current and primary inductance from input, output and duty cycle.
category: electronics
{intro("A flyback converter stores energy in a coupled inductor while the switch is on and releases it to the output when the switch turns off, so the transformer turns ratio sets both the duty cycle and the voltage the switch must block. This flyback transformer calculator gives the turns ratio, the reflected output voltage, the drain–source voltage stress, the peak primary current and the primary inductance for operation at the edge of discontinuous mode, as described in [how a flyback converter works](ib:flyback-converter-working-principle-explained).")}
keywords: [flyback transformer calculator, flyback turns ratio calculator, flyback transformer design, flyback primary inductance, reflected voltage flyback, flyback duty cycle, flyback converter calculator]
updated: {D}
variables:
  - {{ id: Vmin, label: Minimum DC input voltage, family: voltage, unit: V, default: {fVmin:g}, min: 0, help: 'For AC input, the lowest bulk-capacitor voltage (≈ 100 V DC for 85 V AC).' }}
  - {{ id: Vmax, label: Maximum DC input voltage, family: voltage, unit: V, default: {fVmax:g}, min: 0, help: 'For 265 V AC input, about 375 V DC.' }}
  - {{ id: Vo, label: Output voltage, family: voltage, unit: V, default: {fVo:g}, min: 0 }}
  - {{ id: Vf, label: Output diode forward voltage, family: voltage, unit: V, default: {fVf:g}, min: 0, help: 'Schottky ≈ 0.4–0.6 V, fast silicon ≈ 0.7–1 V, synchronous rectifier ≈ 0.05–0.1 V.' }}
  - {{ id: D, label: Maximum duty cycle (at minimum input), family: percent, unit: '%', default: {fD*100:g}, min: 0, max: 0.99 }}
  - {{ id: Po, label: Output power, family: power, unit: W, default: {fPo:g}, min: 0 }}
  - {{ id: eta, label: Expected efficiency, family: percent, unit: '%', default: {feta*100:g}, min: 0.01, max: 1 }}
  - {{ id: fs, label: Switching frequency, family: frequency, unit: kHz, default: {ffs/1e3:g}, min: 0 }}
  - {{ id: n, label: Turns ratio Np ÷ Ns, min: 0, decimals: 3 }}
  - {{ id: Vor, label: Reflected output voltage, family: voltage, unit: V, min: 0 }}
  - {{ id: Vds, label: Switch voltage at max input (before leakage spike), family: voltage, unit: V, min: 0 }}
  - {{ id: Pin, label: Input power, family: power, unit: W, min: 0 }}
  - {{ id: Ipk, label: Peak primary current, family: current, unit: A, min: 0 }}
  - {{ id: Lp, label: Maximum primary inductance for DCM, family: inductance, unit: uH, min: 0 }}
  - {{ id: Isp, label: Peak secondary current, family: current, unit: A, min: 0 }}
  - {{ id: Dmin, label: Duty cycle at maximum input (boundary mode), family: percent, unit: '%', min: 0 }}
equations:
  - n = Vmin * D / ((1 - D) * (Vo + Vf))
  - Vor = n * (Vo + Vf)
  - Vds = Vmax + Vor
  - Pin = Po / eta
  - Ipk = 2 * Pin / (Vmin * D)
  - Lp = Vmin * D / (Ipk * fs)
  - Isp = n * Ipk
  - Dmin = Vor / (Vor + Vmax)
faq:
  - q: How do you calculate the turns ratio of a flyback transformer?
    a: From volt-second balance at the minimum input voltage and maximum duty cycle, Np ÷ Ns = V_in,min × D_max ÷ [(1 − D_max) × (V_out + V_f)].
  - q: What is the reflected voltage in a flyback converter?
    a: While the secondary conducts, the output voltage plus the diode drop appears on the primary multiplied by the turns ratio, V_OR = n × (V_out + V_f). It adds to the input voltage across the switch, so the switch sees V_in,max + V_OR plus a leakage-inductance spike.
  - q: How is the primary inductance chosen?
    a: For discontinuous (DCM) operation all the energy ½ L I_pk² must be delivered every cycle, so L_p ≤ (V_in,min × D_max)² ÷ (2 × P_in × f_s). A larger inductance pushes the converter into continuous mode (CCM) with lower peak current but a right-half-plane zero in the control loop.
  - q: What duty cycle should a flyback use?
    a: Typically 40–50% at minimum input. A higher duty cycle lowers the primary peak current but raises the reflected voltage and the switch voltage stress; with universal AC input this usually means a 600–800 V MOSFET and an RCD clamp.
related: [electronics/buck-boost-converter, electronics/buck-converter, electronics/mosfet-power-loss, electrical/transformer-turns-ratio]
''', f'''
## How to use the flyback transformer calculator

Enter the **minimum and maximum DC input voltage**, the **output voltage**, the **rectifier forward voltage**, the **maximum duty cycle** you want at minimum input, the **output power**, an expected **efficiency** and the **switching frequency**. The calculator returns the turns ratio, the reflected voltage and the switch voltage, the peak primary and secondary currents, and the largest primary inductance that keeps the converter in discontinuous mode at full load (boundary mode at minimum input).

## Flyback transformer formulas

<p class="formula">n = N<sub>p</sub> ÷ N<sub>s</sub> = V<sub>in,min</sub> D<sub>max</sub> ÷ [(1 − D<sub>max</sub>)(V<sub>out</sub> + V<sub>f</sub>)] &nbsp;·&nbsp; V<sub>OR</sub> = n (V<sub>out</sub> + V<sub>f</sub>)</p>

<p class="formula">V<sub>DS</sub> = V<sub>in,max</sub> + V<sub>OR</sub> &nbsp;·&nbsp; I<sub>pk</sub> = 2 P<sub>in</sub> ÷ (V<sub>in,min</sub> D<sub>max</sub>) &nbsp;·&nbsp; L<sub>p</sub> = V<sub>in,min</sub> D<sub>max</sub> ÷ (I<sub>pk</sub> f<sub>s</sub>)</p>

The inductance and peak current are for the boundary between continuous and discontinuous conduction at minimum input and full load; any lower inductance keeps the converter in DCM.

## Worked example

A {fPo:g} W, {fVo:g} V flyback from an {fVmin:g}–{fVmax:g} V DC bus, Schottky diode (V<sub>f</sub> = {fVf:g} V), D<sub>max</sub> = {fD*100:g}%, efficiency {feta*100:g}%, {ffs/1e3:g} kHz:

- Turns ratio n = {fVmin:g} × {fD:g} ÷ ({1-fD:g} × {fVo+fVf:g}) = **{fn:.3f}**
- Reflected voltage V<sub>OR</sub> = {fn:.3f} × {fVo+fVf:g} = **{fVor:.2f} V**; switch voltage at {fVmax:g} V input = **{fVds:.2f} V** (choose a ≥ 80 V MOSFET to allow for the leakage spike)
- Input power {fPo:g} ÷ {feta:g} = **{fPin:g} W**, peak primary current = 2 × {fPin:g} ÷ ({fVmin:g} × {fD:g}) = **{fIpk:.3f} A**
- Primary inductance L<sub>p</sub> = {fVmin*fD:g} ÷ ({fIpk:.3f} × {ffs:,.0f}) = **{fLp*1e6:.2f} µH**; peak secondary current = **{fIsp:.2f} A**
- At {fVmax:g} V input the duty cycle drops to about **{fDmin*100:.1f}%**

## Universal-input (85–265 V AC) designs, 20 W

Bulk-capacitor voltage 100–375 V DC, efficiency 85%:

| Output | D<sub>max</sub> | Turns ratio | V<sub>OR</sub> | V<sub>DS</sub> before spike |
|---|---|---|---|---|
{fl_rows}
The leakage-inductance spike typically adds 30–50% of V<sub>OR</sub>, which is why 650 V or 800 V MOSFETs are used on universal-input flybacks.

## Practical notes

- **Clamp the leakage spike** with an RCD clamp or TVS; set the clamp voltage about 1.5 × V<sub>OR</sub> and keep it below the MOSFET rating with 10–20% margin.
- The core must store ½ L<sub>p</sub> I<sub>pk</sub>² without saturating — flyback cores need an air gap, and the gap stores most of the energy.
- Round the turns to whole numbers and recalculate the duty cycle; an auxiliary winding for the controller supply uses the same volts-per-turn.
- Secondary RMS current is much higher than the DC output current at low duty cycle, so size the output capacitor for ripple current, not just capacitance.
''')

# ======================================================================= ENGINEERING

# ---------------------------------------------------------------- NPSH available
G = 9.80665
_n = [0, 1167.0521452767, -724213.16703206, -17.073846940092, 12020.82470247, -3232555.0322333,
      14.91510861353, -4823.2657361591, 405113.40542057, -0.23855557567849, 650.17534844798]
def psat(TK):  # IAPWS-IF97 region 4 saturation pressure, Pa
    th = TK + _n[9] / (TK - _n[10]); A = th * th + _n[1] * th + _n[2]; B = _n[3] * th * th + _n[4] * th + _n[5]; C = _n[6] * th * th + _n[7] * th + _n[8]
    return (2 * C / (-B + math.sqrt(B * B - 4 * A * C))) ** 4 * 1e6
RHO = {10: 999.70, 20: 998.21, 30: 995.65, 40: 992.22, 50: 988.03, 60: 983.20, 70: 977.76, 80: 971.79, 90: 965.31, 100: 958.35}
assert abs(psat(373.15) - 101418) < 10
nPa, nT, nhz, nhf, nNr = 101325.0, 40, -3.0, 1.2, 4.0
nPv = round(psat(nT + 273.15) / 1000, 3) * 1000; nrho = RHO[nT]
nHp = nPa / (nrho * G); nHv = nPv / (nrho * G); nNa = nHp - nHv + nhz - nhf; nM = nNa - nNr; nR = nNa / nNr
np_rows = ''
for T, rho in RHO.items():
    pv = psat(T + 273.15)
    np_rows += f"| {T} °C | {pv/1000:.3f} kPa | {rho:.2f} kg/m³ | {pv/(rho*G):.2f} m | {(101325-pv)/(rho*G):.2f} m |\n"
na_rows = ''
for h in (0, 500, 1000, 1500, 2000, 3000):
    pa = 101325 * (1 - 2.25577e-5 * h) ** 5.25588
    na_rows += f"| {h:,} m | {pa/1000:.1f} kPa | {(pa-psat(293.15))/(998.21*G):.2f} m | {(pa-psat(333.15))/(983.20*G):.2f} m |\n"
P('engineering', 'npsh-available', f'''
title: NPSH Available Calculator (NPSHa for Pumps)
description: Calculate the net positive suction head available (NPSHa) for a pump from tank pressure, vapour pressure, liquid density, static height and suction losses.
category: engineering
{intro("A centrifugal pump cavitates when the pressure at its eye falls to the liquid's vapour pressure, so the suction system must supply more head than the pump needs. This NPSH available calculator works out NPSHa from the pressure on the liquid surface, the vapour pressure and density of the liquid, the static height and the suction-line friction, then compares it with the pump's NPSHr — the check explained in [NPSH and cavitation](ib:npsh-and-cavitation-explained).")}
keywords: [npsh available calculator, npsha calculator, npsh calculation, net positive suction head calculator, pump cavitation calculator, npsh margin, npshr vs npsha]
updated: {D}
variables:
  - {{ id: Pa, label: Absolute pressure on the liquid surface, family: pressure, unit: kPa, imperialUnit: psi, default: {nPa/1000:g}, min: 0, help: 'Open tank: local atmospheric pressure. Closed vessel: gauge pressure + atmospheric.' }}
  - {{ id: Pv, label: Vapour pressure of the liquid at pumping temperature, family: pressure, unit: kPa, imperialUnit: psi, default: {nPv/1000:g}, min: 0, help: 'Water: 2.34 kPa at 20 °C, 7.38 kPa at 40 °C, 19.9 kPa at 60 °C, 101.4 kPa at 100 °C.' }}
  - {{ id: rho, label: Liquid density, family: density, unit: kgm3, default: {nrho:g}, min: 0 }}
  - {{ id: hz, label: Liquid level above pump centreline, family: length, unit: m, imperialUnit: ft, default: {nhz:g}, help: 'Positive for a flooded suction, negative for a suction lift (level below the pump).' }}
  - {{ id: hf, label: Suction line friction and fitting losses, family: length, unit: m, imperialUnit: ft, default: {nhf:g}, min: 0 }}
  - {{ id: NPSHr, label: Pump NPSH required (from pump curve), family: length, unit: m, imperialUnit: ft, default: {nNr:g}, min: 0 }}
  - {{ id: Hp, label: Pressure head on the surface, family: length, unit: m, imperialUnit: ft }}
  - {{ id: Hv, label: Vapour pressure head, family: length, unit: m, imperialUnit: ft }}
  - {{ id: NPSHa, label: NPSH available, family: length, unit: m, imperialUnit: ft }}
  - {{ id: M, label: NPSH margin (NPSHa − NPSHr), family: length, unit: m, imperialUnit: ft }}
  - id: R
    label: NPSH margin ratio (NPSHa ÷ NPSHr)
    decimals: 2
    bands:
      - {{ max: 1.0, label: Below 1 — the pump will cavitate, color: '#dc2626' }}
      - {{ max: 1.1, label: Under 1.1 — inadequate margin, color: '#f97316' }}
      - {{ max: 1.3, label: 1.1–1.3 — acceptable only for low-energy pumps, color: '#eab308' }}
      - {{ max: 1e9, label: 1.3 or more — comfortable margin for most services, color: '#16a34a' }}
equations:
  - Hp = Pa / (rho * g0)
  - Hv = Pv / (rho * g0)
  - NPSHa = Hp - Hv + hz - hf
  - M = NPSHa - NPSHr
  - R = NPSHa / NPSHr
faq:
  - q: How do you calculate NPSH available?
    a: NPSHa = (P_surface − P_vapour) ÷ (ρg) + h_static − h_friction, using absolute pressures. h_static is positive when the liquid level is above the pump centreline and negative for a suction lift.
  - q: What is the difference between NPSHa and NPSHr?
    a: NPSHa is a property of the suction system — the head above vapour pressure available at the pump inlet. NPSHr is a property of the pump, from the manufacturer's curve, usually defined as the NPSH at which head drops by 3% (NPSH3). NPSHa must exceed NPSHr.
  - q: How much NPSH margin is needed?
    a: Hydraulic Institute guideline ANSI/HI 9.6.1 suggests NPSHa ÷ NPSHr ratios from about 1.1 up to 2.5 depending on the pump's suction energy and service; many specifications ask for at least 1 m (3 ft) of margin or a 1.3 ratio.
  - q: Why does hot water cause cavitation more easily?
    a: Vapour pressure rises steeply with temperature — from 2.3 kPa at 20 °C to 101 kPa at 100 °C — so the vapour head term eats almost all of the atmospheric head. Boiling or near-boiling liquids need a flooded suction with enough static height.
related: [engineering/pump-power, engineering/darcy-weisbach-head-loss, engineering/minor-losses, engineering/pressure-to-head]
''', f'''
## How to use the NPSH available calculator

Enter the **absolute pressure on the liquid surface** (atmospheric pressure for an open tank), the liquid's **vapour pressure** at the pumping temperature, its **density**, the **liquid level relative to the pump centreline** (negative for a suction lift), the **suction-line losses** at the design flow and the pump's **NPSHr** from its curve. The calculator gives each head term, the NPSH available, the margin in metres and the NPSHa ÷ NPSHr ratio.

## NPSH available formula

<p class="formula">NPSH<sub>a</sub> = (P<sub>surface</sub> − P<sub>v</sub>) ÷ (ρ g) + h<sub>z</sub> − h<sub>f</sub></p>

All pressures are absolute. Calculate NPSHa at the **maximum flow** (highest friction and NPSHr), the **lowest liquid level** and the **highest liquid temperature** you expect.

## Worked example

Water at {nT} °C (P<sub>v</sub> = {nPv/1000:g} kPa, ρ = {nrho:g} kg/m³) lifted from an open sump at sea level, liquid level {abs(nhz):g} m below the pump, {nhf:g} m suction loss, pump NPSHr = {nNr:g} m:

- Pressure head = {nPa:,.0f} ÷ ({nrho:g} × 9.807) = **{nHp:.2f} m**
- Vapour pressure head = {nPv:,.0f} ÷ ({nrho:g} × 9.807) = **{nHv:.3f} m**
- NPSH<sub>a</sub> = {nHp:.2f} − {nHv:.3f} − {abs(nhz):g} − {nhf:g} = **{nNa:.2f} m**
- Margin = {nNa:.2f} − {nNr:g} = **{nM:.2f} m**, ratio **{nR:.2f}** — comfortable

## Vapour pressure of water and NPSH from an open tank (sea level)

The last column is the NPSHa with zero static height and zero suction loss — the most a sea-level open tank can provide at that temperature.

| Temperature | Vapour pressure | Density | Vapour head | Max NPSHa, open tank |
|---|---|---|---|---|
{np_rows}
Vapour pressure from the IAPWS-IF97 saturation equation.

## Effect of altitude (open tank, no static height or losses)

| Site altitude | Atmospheric pressure | NPSHa, water 20 °C | NPSHa, water 60 °C |
|---|---|---|---|
{na_rows}
## Practical notes

- A suction lift of more than about 4–5 m with cold water usually leaves too little NPSHa — move the pump lower or use a flooded suction.
- **Reduce suction losses**: use a suction pipe one size larger than the pump inlet, keep it short, and avoid strainers or valves that can clog close to the pump.
- For liquids at their boiling point (condensate, deaerator outlet, refrigerants) P<sub>surface</sub> = P<sub>v</sub>, so NPSHa is just the static height minus losses.
- If you have a suction gauge reading, NPSHa = (P<sub>gauge</sub> + P<sub>atm</sub> − P<sub>v</sub>) ÷ ρg + v²/2g + gauge height above the pump centreline.
''')

# ---------------------------------------------------------------- Dew point
DB, DC = 17.625, 243.04  # Magnus coefficients (Alduchov & Eskridge 1996)
def dew(T, RH):
    g_ = math.log(RH) + DB * T / (DC + T); Td = DC * g_ / (DB - g_)
    es = 610.94 * math.exp(DB * T / (T + DC)); e = RH * es; AH = e / (461.5 * (T + 273.15)) * 1000
    return g_, Td, es, e, AH
dT, dRH = 25.0, 0.60
dg, dTd, des, de, dAH = dew(dT, dRH)
dw_rows = ''
for T in (0, 10, 15, 20, 25, 30, 35, 40):
    dw_rows += f"| {T} °C | " + ' | '.join(f"{dew(T, rh)[1]:.1f} °C" for rh in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)) + " |\n"
P('engineering', 'dew-point', f'''
title: Dew Point Calculator (Temperature & Relative Humidity)
description: Calculate the dew point from air temperature and relative humidity with the Magnus formula, plus vapour pressure, absolute humidity and dew point spread.
category: engineering
{intro("The dew point is the temperature at which air becomes saturated and water starts to condense on a surface. This dew point calculator finds it from the dry-bulb temperature and relative humidity using the Magnus formula, and also gives the vapour pressure, absolute humidity and the temperature margin to condensation — useful for HVAC, coating work and [dew point in instrument air](ib:dew-point-in-instrument-air-risks). It works in reverse too: enter a dew point to get the relative humidity, as a [capacitive RH sensor](ib:humidity-sensor-capacitive-rh) transmitter would report.")}
keywords: [dew point calculator, dew point from relative humidity, calculate dew point, dew point temperature calculator, magnus formula dew point, relative humidity to dew point, absolute humidity calculator]
updated: {D}
variables:
  - {{ id: T, label: Air (dry-bulb) temperature, family: temperature, unit: C, imperialUnit: F, default: {dT:g} }}
  - {{ id: RH, label: Relative humidity, family: percent, unit: '%', default: {dRH*100:g}, min: 0.000001, max: 1 }}
  - {{ id: gam, label: Magnus function γ(T, RH), decimals: 5 }}
  - {{ id: Td, label: Dew point temperature, family: temperature, unit: C, imperialUnit: F }}
  - id: dTd
    label: Dew point spread (T − Td)
    family: tempdiff
    unit: K
    imperialUnit: F
    bands:
      - {{ max: 2, label: Under 2 °C — condensation likely on cool surfaces, color: '#dc2626' }}
      - {{ max: 3, label: 2–3 °C — too close for painting or coating (needs ≥ 3 °C), color: '#f97316' }}
      - {{ max: 1e9, label: 3 °C or more above the dew point, color: '#16a34a' }}
  - {{ id: es, label: Saturation vapour pressure, family: pressure, unit: kPa, min: 0, decimals: 4 }}
  - {{ id: ea, label: Actual vapour pressure, family: pressure, unit: kPa, min: 0, decimals: 4 }}
  - {{ id: AH, label: Absolute humidity, suffix: g/m³, min: 0, decimals: 2 }}
equations:
  - gam = ln(RH) + 17.625 * (T - 273.15) / (243.04 + T - 273.15)
  - Td = 273.15 + 243.04 * gam / (17.625 - gam)
  - dTd = T - Td
  - es = 610.94 * exp(17.625 * (T - 273.15) / (T - 273.15 + 243.04))
  - ea = RH * es
  - AH = ea / (461.5 * T) * 1000
faq:
  - q: How do you calculate dew point from temperature and humidity?
    a: With the Magnus formula, γ = ln(RH) + bT ÷ (c + T) and T_d = c γ ÷ (b − γ), where T is in °C, RH is a fraction, b = 17.625 and c = 243.04 °C. It is accurate to about ±0.35 °C between −40 and 50 °C.
  - q: Is there a quick rule of thumb for dew point?
    a: Above about 50% RH, the dew point is roughly T − (100 − RH%) ÷ 5. At 25 °C and 60% RH that gives 17 °C; the Magnus formula gives {dTd:.1f} °C.
  - q: What dew point feels comfortable?
    a: Dew points below about 13 °C feel dry and comfortable, 16–18 °C starts to feel humid, and above 21 °C feels oppressive, because sweat cannot evaporate easily.
  - q: Why does instrument air need a low dew point?
    a: Compressed air that cools below its dew point condenses water in lines and instruments, causing corrosion and freezing. ISA-7.0.01 asks for a pressure dew point at least 10 °C below the lowest temperature the air lines will see.
related: [conversion/temperature-converter, chemistry/daltons-law, physics/latent-heat, engineering/chiller-tonnage]
''', f'''
## How to use the dew point calculator

Enter the **air temperature** and the **relative humidity**. The calculator gives the dew point, the spread between air temperature and dew point, the saturation and actual vapour pressures and the absolute humidity (grams of water per cubic metre of air). To find the **relative humidity from a dew point**, enter the dew point and the air temperature and press × on Relative humidity.

## Dew point formula (Magnus)

<p class="formula">γ = ln(RH) + b T ÷ (c + T) &nbsp;·&nbsp; T<sub>d</sub> = c γ ÷ (b − γ)</p>

<p class="formula">e<sub>s</sub> = 610.94 × exp[b T ÷ (T + c)] Pa &nbsp;·&nbsp; AH = RH × e<sub>s</sub> ÷ (R<sub>v</sub> × T<sub>K</sub>)</p>

with T in °C, b = 17.625, c = 243.04 °C (Alduchov & Eskridge) and R<sub>v</sub> = 461.5 J/(kg·K), the gas constant of water vapour. The formula is for saturation over liquid water; below 0 °C the frost point is slightly higher than the dew point it gives.

## Worked example

Air at {dT:g} °C and {dRH*100:g}% relative humidity:

- γ = ln({dRH:g}) + 17.625 × {dT:g} ÷ (243.04 + {dT:g}) = **{dg:.5f}**
- T<sub>d</sub> = 243.04 × {dg:.5f} ÷ (17.625 − {dg:.5f}) = **{dTd:.2f} °C**, a spread of **{dT-dTd:.2f} °C**
- Saturation vapour pressure = **{des/1000:.4f} kPa**, actual vapour pressure = **{de/1000:.4f} kPa**
- Absolute humidity = {de:.1f} ÷ (461.5 × {dT+273.15:.2f}) = **{dAH:.2f} g/m³**

## Dew point table

| Air temperature | 30% RH | 40% RH | 50% RH | 60% RH | 70% RH | 80% RH | 90% RH |
|---|---|---|---|---|---|---|---|
{dw_rows}
## Practical notes

- **Coatings and painting:** most paint specifications (ISO 8502-4) require the steel surface to be at least 3 °C above the dew point.
- **Pipes and ducts sweat** when their surface is below the dew point of the surrounding air — insulate chilled-water lines with a vapour barrier.
- **Compressed air:** the pressure dew point is higher than the atmospheric dew point of the same air, because compression raises the vapour pressure. Use the dryer manufacturer's data or a pressure dew point meter for instrument air.
- RH sensors are usually accurate to ±2–3% RH; near saturation, that alone moves the dew point by about 0.5 °C.
''')

# ======================================================================= STATISTICS

# ---------------------------------------------------------------- X-bar & R control chart
CC = {2: (1.880, 0, 3.267, 1.128), 3: (1.023, 0, 2.574, 1.693), 4: (0.729, 0, 2.282, 2.059), 5: (0.577, 0, 2.114, 2.326),
      6: (0.483, 0, 2.004, 2.534), 7: (0.419, 0.076, 1.924, 2.704), 8: (0.373, 0.136, 1.864, 2.847), 9: (0.337, 0.184, 1.816, 2.970),
      10: (0.308, 0.223, 1.777, 3.078)}
for k, (A2, D3, D4, d2) in CC.items():   # A2 = 3 / (d2 √n)
    assert abs(3 / (d2 * math.sqrt(k)) - A2) < 0.0015, k
def sel(idx):
    return ' + '.join(f"(step(n - {k-0.5:g}) - step(n - {k+0.5:g})) * {v[idx]:g}" for k, v in CC.items() if v[idx] != 0)
cX, cR, cn = 50.0, 2.0, 5
cA2, cD3, cD4, cd2 = CC[cn]
cUx, cLx, cUr, cLr, cs = cX + cA2 * cR, cX - cA2 * cR, cD4 * cR, cD3 * cR, cR / cd2
cc_rows = ''.join(f"| {k} | {v[0]:.3f} | {v[1]:.3f} | {v[2]:.3f} | {v[3]:.3f} |\n" for k, v in CC.items())
cl_rows = ''.join(f"| {k} | {cX-v[0]*cR:.3f} – {cX+v[0]*cR:.3f} | {v[1]*cR:.3f} – {v[2]*cR:.3f} | {cR/v[3]:.4f} |\n" for k, v in CC.items())
opts = ''.join(f"      - {{ label: '{k}', value: {k} }}\n" for k in CC)
P('statistics', 'control-chart', f'''
title: Control Chart Calculator (X-bar & R Chart Limits)
description: Calculate X-bar and R control chart limits — UCL, centre line and LCL — from the grand mean, average range and subgroup size, with A2, D3 and D4 constants.
category: statistics
{intro("An X-bar and R chart tracks the average and the range of small subgroups taken from a process, and flags points outside limits set three standard errors from the centre line. This control chart calculator takes the grand mean, the average range and the subgroup size, looks up the A₂, D₃, D₄ and d₂ constants and gives the upper and lower control limits for both charts, plus the estimated process standard deviation.")}
keywords: [control chart calculator, x bar r chart calculator, ucl lcl calculator, control limits calculator, x bar chart limits, range chart limits, a2 d3 d4 constants, spc calculator]
updated: {D}
variables:
  - {{ id: X, label: Grand mean X̿ (average of subgroup means), default: {cX:g} }}
  - {{ id: Rb, label: Average range R̄, default: {cR:g}, min: 0 }}
  - id: n
    label: Subgroup size n
    default: {cn}
    options:
{opts.rstrip()}
  - {{ id: A2, label: A₂ constant, decimals: 3 }}
  - {{ id: D3, label: D₃ constant, decimals: 3 }}
  - {{ id: D4, label: D₄ constant, decimals: 3 }}
  - {{ id: d2, label: d₂ constant, decimals: 3 }}
  - {{ id: UCLx, label: X-bar chart upper control limit (UCL), decimals: 4 }}
  - {{ id: LCLx, label: X-bar chart lower control limit (LCL), decimals: 4 }}
  - {{ id: UCLr, label: R chart upper control limit, decimals: 4 }}
  - {{ id: LCLr, label: R chart lower control limit, decimals: 4 }}
  - {{ id: s, label: Estimated process standard deviation σ = R̄ ÷ d₂, decimals: 4 }}
equations:
  - A2 = {sel(0)}
  - D3 = {sel(1)}
  - D4 = {sel(2)}
  - d2 = {sel(3)}
  - UCLx = X + A2 * Rb
  - LCLx = X - A2 * Rb
  - UCLr = D4 * Rb
  - LCLr = D3 * Rb
  - s = Rb / d2
faq:
  - q: How do you calculate X-bar chart control limits?
    a: UCL = X̿ + A₂R̄ and LCL = X̿ − A₂R̄, where X̿ is the average of the subgroup means, R̄ the average subgroup range and A₂ a constant that depends on the subgroup size (0.577 for n = 5).
  - q: How do you calculate R chart control limits?
    a: UCL = D₄R̄ and LCL = D₃R̄. For subgroups of 6 or fewer D₃ = 0, so the lower limit of the range chart is zero.
  - q: Where do the A₂, D₃ and D₄ constants come from?
    a: They come from the distribution of the range of n normal values. d₂ is the mean of that range in standard-deviation units, so σ ≈ R̄ ÷ d₂, and A₂ = 3 ÷ (d₂√n) puts the X-bar limits at ±3 standard errors.
  - q: Are control limits the same as specification limits?
    a: No. Control limits come from the process data and show what the process actually does; specification limits come from the customer or design. Use the process capability calculator to compare the two.
related: [statistics/process-capability, statistics/six-sigma, statistics/standard-deviation, statistics/normal-distribution]
''', f'''
## How to use the control chart calculator

Collect at least 20–25 subgroups of the same size (typically 4 or 5 consecutive parts). Work out the mean and the range (max − min) of each subgroup, then enter the **average of the subgroup means** (X̿), the **average range** (R̄) and the **subgroup size**. The calculator shows the control chart constants and the control limits for the X-bar chart and the R chart, and estimates the short-term process standard deviation.

## X-bar and R chart formulas

<p class="formula">X-bar chart: UCL = X̿ + A₂R̄ &nbsp;·&nbsp; CL = X̿ &nbsp;·&nbsp; LCL = X̿ − A₂R̄</p>

<p class="formula">R chart: UCL = D₄R̄ &nbsp;·&nbsp; CL = R̄ &nbsp;·&nbsp; LCL = D₃R̄ &nbsp;·&nbsp; σ̂ = R̄ ÷ d₂</p>

## Worked example

A filling line is sampled in subgroups of {cn} bottles. Over 25 subgroups the grand mean is {cX:g} g and the average range is {cR:g} g:

- For n = {cn}: A₂ = {cA2:.3f}, D₃ = {cD3:g}, D₄ = {cD4:.3f}, d₂ = {cd2:.3f}
- X-bar chart: UCL = {cX:g} + {cA2:.3f} × {cR:g} = **{cUx:.3f} g**, LCL = **{cLx:.3f} g**
- R chart: UCL = {cD4:.3f} × {cR:g} = **{cUr:.3f} g**, LCL = **{cLr:g} g**
- Estimated process standard deviation σ = {cR:g} ÷ {cd2:.3f} = **{cs:.4f} g**

## Control chart constants

| n | A₂ | D₃ | D₄ | d₂ |
|---|---|---|---|---|
{cc_rows}
## Limits for X̿ = {cX:g} and R̄ = {cR:g} at each subgroup size

| n | X-bar chart LCL – UCL | R chart LCL – UCL | σ̂ = R̄ ÷ d₂ |
|---|---|---|---|
{cl_rows}
## Practical notes

- **Plot the R chart first.** If the range is out of control, the X-bar limits (which depend on R̄) are not reliable.
- Common out-of-control signals besides a point outside the limits: 7–8 points in a row on one side of the centre line, 6 points steadily rising or falling, and 2 of 3 points beyond 2σ (Western Electric rules).
- Remove points with a known, corrected special cause and recalculate the limits; do not remove points just because they are outside.
- For subgroups larger than about 10, use an X-bar and S chart; for single readings, use an individuals (I-MR) chart.
''')

# ======================================================================= MATH

# ---------------------------------------------------------------- Cubic equation
def cbrt(v): return math.copysign(abs(v) ** (1 / 3), v)
def step(v): return 1 if v > 1e-9 else 0
def cubic(a, b, c, d):
    p = (3 * a * c - b * b) / (3 * a * a); q = (2 * b ** 3 - 9 * a * b * c + 27 * a * a * d) / (27 * a ** 3)
    Dd = (q / 2) ** 2 + (p / 3) ** 3; s = b / (3 * a)
    Dl = 18 * a * b * c * d - 4 * b ** 3 * d + b * b * c * c - 4 * a * c ** 3 - 27 * a * a * d * d
    u = cbrt(-q / 2 + math.sqrt(max(Dd, 0))); v = cbrt(-q / 2 - math.sqrt(max(Dd, 0)))
    r = 2 * math.sqrt(max(-p / 3, 0)); th = math.acos(min(max(-q / 2 / math.sqrt(max(-(p / 3) ** 3, 1e-300)), -1), 1)) / 3
    w = step(Dd)
    x1 = w * (u + v - s) + (1 - w) * (r * math.cos(th) - s)
    x2 = w * (-(u + v) / 2 - s) + (1 - w) * (r * math.cos(th - 2 * pi / 3) - s)
    x3 = w * (-(u + v) / 2 - s) + (1 - w) * (r * math.cos(th + 2 * pi / 3) - s)
    im = w * math.sqrt(3) / 2 * abs(u - v)
    return p, q, Dd, Dl, x1, x2, x3, im
# self-test against numpy
import random
try:
    import numpy as np
    random.seed(7)
    for _ in range(3000):
        a = random.choice([-1, 1]) * random.uniform(0.1, 5); b, c, d = (random.uniform(-10, 10) for _ in range(3))
        if random.random() < 0.3:  # integer roots
            r1, r2, r3 = (random.randint(-5, 5) for _ in range(3)); a, b, c, d = 1, -(r1 + r2 + r3), r1 * r2 + r1 * r3 + r2 * r3, -r1 * r2 * r3
        _, _, Dd, _, x1, x2, x3, im = cubic(a, b, c, d)
        got = sorted([complex(x1, 0), complex(x2, im), complex(x3, -im)], key=lambda z: (round(z.real, 3), z.imag))
        ref = sorted(np.roots([a, b, c, d]), key=lambda z: (round(z.real, 3), z.imag))
        for g_, r_ in zip(sorted(got, key=lambda z: (z.real, z.imag)), sorted(ref, key=lambda z: (z.real, z.imag))):
            assert abs(g_ - r_) < 1e-4 * max(1, abs(r_)) or abs(g_.real - r_.real) < 2e-3, (a, b, c, d, got, ref)
except ImportError:
    pass
ka, kb, kc, kd = 1, -6, 11, -6
kp, kq, kD, kDl, k1, k2, k3, kim = cubic(ka, kb, kc, kd)
wp, wq, wD, wDl, w1, w2, w3, wim = cubic(1, 0, -2, -5)
cu_rows = ''
for eq, co in (('x³ − 6x² + 11x − 6 = 0', (1, -6, 11, -6)), ('x³ − 2x − 5 = 0', (1, 0, -2, -5)), ('x³ − 3x + 2 = 0', (1, 0, -3, 2)),
               ('x³ − 1 = 0', (1, 0, 0, -1)), ('2x³ − 4x² − 22x + 24 = 0', (2, -4, -22, 24)), ('x³ + x + 1 = 0', (1, 0, 1, 1)),
               ('x³ − 15x − 4 = 0', (1, 0, -15, -4))):
    p_, q_, D_, Dl_, a1, a2, a3, im_ = cubic(*co)
    if im_ > 1e-9:
        roots = f"{a1:.4g}; {a2:.4g} ± {im_:.4g}i"; kind = 'one real, two complex'
    else:
        rs = sorted({round(v, 6) + 0.0 for v in (a1, a2, a3)}, reverse=True)
        roots = ', '.join(f"{v:.4g}" for v in rs); kind = 'three distinct real' if Dl_ > 1e-9 else 'repeated real root'
    cu_rows += f"| {eq} | {Dl_:,.4g} | {kind} | {roots} |\n"
P('math', 'cubic-equation', f'''
title: Cubic Equation Calculator (Solve ax³ + bx² + cx + d = 0)
description: Solve any cubic equation ax³ + bx² + cx + d = 0 — real and complex roots, the discriminant and the depressed-cubic working with Cardano's formula.
category: math
{intro("Every cubic equation has three roots: either three real roots or one real root and a pair of complex conjugates. This cubic equation calculator finds all three from the coefficients a, b, c and d, using Cardano's formula when there is one real root and the trigonometric method when there are three, and shows the discriminant that tells you which case you have.")}
keywords: [cubic equation calculator, cubic equation solver, solve cubic equation, cubic formula calculator, roots of cubic equation, cardano formula calculator, cubic discriminant]
updated: {D}
variables:
  - {{ id: a, label: a (x³ coefficient — not zero), default: {ka} }}
  - {{ id: b, label: b (x² coefficient), default: {kb} }}
  - {{ id: c, label: c (x coefficient), default: {kc} }}
  - {{ id: d, label: d (constant), default: {kd} }}
  - {{ id: p, label: Depressed cubic p, decimals: 6 }}
  - {{ id: q, label: Depressed cubic q, decimals: 6 }}
  - {{ id: Dc, label: Cardano test value (q/2)² + (p/3)³, decimals: 6 }}
  - id: Dl
    label: Discriminant Δ
    decimals: 4
    bands:
      - {{ max: -1e-9, label: Δ < 0 — one real root and two complex roots, color: '#2563eb' }}
      - {{ max: 1e-9, label: Δ = 0 — a repeated real root, color: '#eab308' }}
      - {{ max: 1e300, label: Δ > 0 — three distinct real roots, color: '#16a34a' }}
  - {{ id: x1, label: Root x₁ (always real), decimals: 6 }}
  - {{ id: x2, label: Root x₂ (real part), decimals: 6 }}
  - {{ id: x3, label: Root x₃ (real part), decimals: 6 }}
  - {{ id: im, label: Imaginary part of x₂ and x₃ (±), decimals: 6, help: '0 when all three roots are real; otherwise x₂ = real part + i·this, x₃ = real part − i·this.' }}
equations:
  - p = (3 * a * c - b^2) / (3 * a^2)
  - q = (2 * b^3 - 9 * a * b * c + 27 * a^2 * d) / (27 * a^3)
  - Dc = (q / 2)^2 + (p / 3)^3
  - Dl = 18 * a * b * c * d - 4 * b^3 * d + b^2 * c^2 - 4 * a * c^3 - 27 * a^2 * d^2
  - x1 = step(Dc) * (cbrt(-q / 2 + sqrt(max(Dc, 0))) + cbrt(-q / 2 - sqrt(max(Dc, 0))) - b / (3 * a)) + (1 - step(Dc)) * (2 * sqrt(max(-p / 3, 0)) * cos(acos(min(max(-q / 2 / sqrt(max(-(p / 3)^3, 1e-300)), -1), 1)) / 3) - b / (3 * a))
  - x2 = step(Dc) * (-(cbrt(-q / 2 + sqrt(max(Dc, 0))) + cbrt(-q / 2 - sqrt(max(Dc, 0)))) / 2 - b / (3 * a)) + (1 - step(Dc)) * (2 * sqrt(max(-p / 3, 0)) * cos(acos(min(max(-q / 2 / sqrt(max(-(p / 3)^3, 1e-300)), -1), 1)) / 3 - 2 * pi / 3) - b / (3 * a))
  - x3 = step(Dc) * (-(cbrt(-q / 2 + sqrt(max(Dc, 0))) + cbrt(-q / 2 - sqrt(max(Dc, 0)))) / 2 - b / (3 * a)) + (1 - step(Dc)) * (2 * sqrt(max(-p / 3, 0)) * cos(acos(min(max(-q / 2 / sqrt(max(-(p / 3)^3, 1e-300)), -1), 1)) / 3 + 2 * pi / 3) - b / (3 * a))
  - im = step(Dc) * sqrt(3) / 2 * abs(cbrt(-q / 2 + sqrt(max(Dc, 0))) - cbrt(-q / 2 - sqrt(max(Dc, 0))))
faq:
  - q: How do you solve a cubic equation?
    a: Divide by a and substitute x = t − b/(3a) to get the depressed cubic t³ + pt + q = 0. If (q/2)² + (p/3)³ > 0, Cardano's formula t = ∛(−q/2 + √…) + ∛(−q/2 − √…) gives the one real root; otherwise the three real roots are t = 2√(−p/3) cos[(1/3) arccos((−q/2)/√(−(p/3)³)) − 2πk/3], k = 0, 1, 2.
  - q: What does the discriminant of a cubic tell you?
    a: Δ = 18abcd − 4b³d + b²c² − 4ac³ − 27a²d². If Δ > 0 there are three distinct real roots, if Δ = 0 at least two roots are equal, and if Δ < 0 there is one real root and two complex conjugate roots.
  - q: Does every cubic have a real root?
    a: Yes. A cubic goes to +∞ at one end and −∞ at the other, so its graph must cross the x-axis at least once. Complex roots of a real cubic always come in conjugate pairs.
  - q: Can I check the roots?
    a: The roots satisfy x₁ + x₂ + x₃ = −b/a, x₁x₂ + x₁x₃ + x₂x₃ = c/a and x₁x₂x₃ = −d/a (Vieta's formulas). For x³ − 6x² + 11x − 6 the roots 1, 2 and 3 add to 6 and multiply to 6.
related: [math/quadratic-equation, math/system-of-3-equations, math/complex-number, math/exponent]
''', f'''
## How to use the cubic equation calculator

Write your equation in the form **ax³ + bx² + cx + d = 0** and enter the four coefficients (use 0 for a missing term — for x³ − 2x − 5 = 0 enter a = 1, b = 0, c = −2, d = −5). The calculator gives the depressed-cubic values p and q, the discriminant, and the three roots. When there is only one real root, x₂ and x₃ show the real part of the complex pair and the last result shows its imaginary part. The coefficient a must not be zero — with a = 0 the equation is a quadratic.

## Cubic formula

<p class="formula">x = t − b ÷ 3a &nbsp;·&nbsp; t³ + pt + q = 0 &nbsp;·&nbsp; p = (3ac − b²) ÷ 3a² &nbsp;·&nbsp; q = (2b³ − 9abc + 27a²d) ÷ 27a³</p>

<p class="formula">One real root (Cardano): t = ∛(−q/2 + √D) + ∛(−q/2 − √D), &nbsp; D = (q/2)² + (p/3)³ &gt; 0</p>

<p class="formula">Three real roots: t<sub>k</sub> = 2√(−p/3) · cos[⅓ arccos((−q/2) ÷ √(−(p/3)³)) − 2πk/3], &nbsp; k = 0, 1, 2</p>

The trigonometric form avoids the cube roots of complex numbers that Cardano's formula needs when all three roots are real (the "casus irreducibilis").

## Worked examples

**x³ − 6x² + 11x − 6 = 0** (a = 1, b = −6, c = 11, d = −6):

- p = (3 × 11 − 36) ÷ 3 = **{kp:g}**, q = (2 × (−216) − 9 × (−66) + 27 × (−6)) ÷ 27 = **{kq:g}**
- D = (q/2)² + (p/3)³ = **{kD:.6f}** (negative), discriminant Δ = **{kDl:g}** — three distinct real roots
- Roots: x₁ = **{k1:.6g}**, x₂ = **{k2:.6g}**, x₃ = **{k3:.6g}** — so the equation factors as (x − 1)(x − 2)(x − 3)

**x³ − 2x − 5 = 0** (the equation Newton used to demonstrate his method):

- p = {wp:g}, q = {wq:g}, D = {wD:.6f} (positive), Δ = {wDl:g} — one real root
- x₁ = **{w1:.6f}**, x₂, x₃ = **{w2:.6f} ± {wim:.6f}i**

## Example cubic equations

| Equation | Discriminant Δ | Roots | Values |
|---|---|---|---|
{cu_rows}
## Practical notes

- Results are rounded; a repeated root may show tiny differences such as 0.999999 and 1.000001 because of floating-point arithmetic.
- To **factor** a cubic with an integer root r, divide by (x − r) to leave a quadratic — the rational root theorem says any rational root is a factor of d divided by a factor of a.
- Cubic equations appear in the van der Waals and Peng–Robinson equations of state, beam deflection, box-volume optimisation and interest-rate problems.
''')

print(len(DESC), 'pages:', ' '.join(DESC))
