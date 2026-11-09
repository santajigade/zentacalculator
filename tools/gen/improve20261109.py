"""Improve pass (2026-11-09) for thin pages from the first batch (2026-10-27):
electronics/capacitor-energy, electronics/resonant-frequency, physics/orbital-period, physics/doppler-effect.
Keyword-first titles, 120-160 char descriptions, intros with the "<topic> calculator" phrase,
worked examples and reference tables computed here, practical notes, re-checked FAQs.
Slugs, categories and existing variable ids are unchanged (asserted). Re-running regenerates the same files."""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from page import page, BASE
from ib import intro
U = '2026-11-09'
G = 6.6743e-11
pi = math.pi
DONE = []

def ids_of(cid):
    fm = open(os.path.join(BASE, cid + '.mdx')).read().split('---')[1]
    d = yaml.safe_load(fm); return [v['id'] for v in d['variables']], d['category']

def W(cid, fm, body):
    cat, slug = cid.split('/')
    old_ids, old_cat = ids_of(cid)
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (cid, len(d))
    assert 'featured' not in fm
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    page(cat, slug, fm, body)
    new_ids, new_cat = ids_of(cid)
    assert new_cat == old_cat == cat, cid
    assert all(i in new_ids for i in old_ids), (cid, old_ids, new_ids)
    DONE.append(cid)

def eng(x, unit, d=4):
    for f, p in ((1e9, 'G'), (1e6, 'M'), (1e3, 'k'), (1, ''), (1e-3, 'm'), (1e-6, 'µ'), (1e-9, 'n'), (1e-12, 'p')):
        if abs(x) >= f * 0.9995:
            return f"{float(f'{x/f:.{d}g}'):g} {p}{unit}"
    return f"{x:.3g} {unit}"

# ---------------------------------------------------------------- Capacitor energy
cC, cV, cV2 = 1000e-6, 50.0, 25.0
cE = 0.5 * cC * cV ** 2; cQ = cC * cV; cEu = 0.5 * cC * (cV ** 2 - cV2 ** 2)
caps = [('100 µF electrolytic', 100e-6, 25), ('1,000 µF electrolytic', 1000e-6, 50), ('Camera flash, 200 µF', 200e-6, 330),
        ('4,700 µF DC bus', 4700e-6, 400), ('VFD DC link, 2 × 2,200 µF', 4400e-6, 650), ('Supercapacitor 10 F', 10, 2.7),
        ('Supercapacitor 3,000 F', 3000, 2.7)]
ce_rows = ''
for nm, C, V in caps:
    E = 0.5 * C * V * V
    ce_rows += f"| {nm} | {V:g} V | {C*V:,.4g} C | {E:,.4g} J | {E/3600:.4g} Wh |\n"
cf_rows = ''.join(f"| {k*100:.0f}% | {(1-k*k)*100:.0f}% | {k*k*100:.0f}% |\n" for k in (0.9, 0.75, 0.5, 0.25, 0.1, 0))
W('electronics/capacitor-energy', f'''
title: Capacitor Energy Calculator (Stored Energy ½CV² & Charge)
description: Calculate the energy stored in a capacitor (½CV²), its charge (Q = CV) and the usable energy when it discharges to a lower voltage — for DC links and supercaps.
category: electronics
{intro("A capacitor stores energy in the electric field between its plates, and the amount rises with the square of the voltage — see the [capacitor working principle](https://www.instrumentationblog.in/capacitor-working-principle/) and how [supercapacitors](https://www.instrumentationblog.in/supercapacitor-working-principle/) store far more. This capacitor energy calculator gives the stored energy in joules, the charge in coulombs and the usable energy delivered when the capacitor discharges to a lower voltage.")}
keywords: [capacitor energy calculator, energy stored in capacitor, 1/2 cv2, capacitor charge calculator, q = cv, supercapacitor energy, capacitor joules, usable capacitor energy]
updated: {U}
variables:
  - {{ id: C, label: Capacitance, family: capacitance, unit: uF, default: {cC*1e6:g}, min: 0 }}
  - {{ id: V, label: Voltage (charged to), family: voltage, unit: V, default: {cV:g}, min: 0 }}
  - {{ id: E, label: Stored energy, family: energy, unit: J, min: 0 }}
  - {{ id: Q, label: Charge, suffix: C (coulombs), min: 0, decimals: 6 }}
  - {{ id: V2, label: Voltage it discharges down to, family: voltage, unit: V, default: {cV2:g}, min: 0, help: 'For example the minimum input voltage of the regulator it feeds. Enter 0 for a full discharge.' }}
  - {{ id: Eu, label: Usable energy between the two voltages, family: energy, unit: J, min: 0 }}
  - {{ id: fu, label: Share of stored energy that is usable, family: percent, unit: '%', min: 0 }}
equations:
  - E = 0.5 * C * V^2
  - Q = C * V
  - Eu = 0.5 * C * (V^2 - V2^2)
  - fu = Eu / E
faq:
  - q: How much energy does a capacitor store?
    a: E = ½ × C × V², with C in farads and V in volts, giving joules. A 1,000 µF capacitor at 50 V stores {cE:g} J.
  - q: How much usable energy is there between two voltages?
    a: E = ½ C (V₁² − V₂²). Discharging from full voltage to half voltage delivers 75% of the stored energy, which is why supercapacitor backup circuits use a converter that works down to a low input voltage.
  - q: Why are charged capacitors dangerous?
    a: Large capacitors in power supplies, VFDs and microwave ovens can hold a lethal charge for minutes after switch-off. Safety standards treat a capacitor above about 60 V DC as a shock hazard once its stored charge exceeds a few tens of microcoulombs — a 10 µF capacitor at 100 V already holds 1,000 µC. Always discharge it and verify 0 V with a meter.
  - q: How do I convert capacitor energy to watt-hours?
    a: Divide joules by 3,600. A 3,000 F, 2.7 V supercapacitor stores 10,935 J, or about 3.04 Wh.
related: [electronics/capacitors-series-parallel, physics/rc-time-constant, electronics/inductor-energy, electronics/capacitor-lifetime]
''', f'''
## How to use the capacitor energy calculator

Enter the **capacitance** and the **voltage** it is charged to. The calculator gives the stored energy and the charge. To see how much of that energy a circuit can actually use, enter the **voltage it discharges down to** — the usable energy and its share of the total appear below. Press × on Voltage to find the voltage needed to store a given energy.

## Capacitor energy and charge formulas

<p class="formula">E = ½ C V² &nbsp;·&nbsp; Q = C V &nbsp;·&nbsp; E<sub>usable</sub> = ½ C (V₁² − V₂²)</p>

Because energy grows with V², doubling the voltage stores four times the energy, while doubling the capacitance only doubles it.

## Worked example

A {cC*1e6:,.0f} µF capacitor charged to {cV:g} V that feeds a circuit which stops working below {cV2:g} V:

- Stored energy E = ½ × {cC:g} F × {cV:g}² = **{cE:g} J**
- Charge Q = {cC:g} × {cV:g} = **{cQ:g} C**
- Usable energy = ½ × {cC:g} × ({cV:g}² − {cV2:g}²) = **{cEu:g} J**, or **{cEu/cE*100:.0f}%** of the stored energy

## Stored energy of common capacitors

| Capacitor | Voltage | Charge | Energy | Energy (Wh) |
|---|---|---|---|---|
{ce_rows}
## How much energy is usable?

| Discharged to (% of full voltage) | Energy delivered | Energy left |
|---|---|---|
{cf_rows}
## Practical notes

- **Supercapacitors vs batteries:** a 3,000 F, 2.7 V supercapacitor stores about 3 Wh — roughly what a few AA batteries hold — but can deliver it in seconds and survive hundreds of thousands of cycles, which suits short backup, regenerative braking and burst power.
- **Series strings:** capacitors in series share the voltage, so the bank voltage rises but the capacitance falls (1/C = 1/C₁ + 1/C₂); use balancing resistors or active balancing for supercapacitors.
- **Derating:** electrolytic capacitance has a −20% tolerance and falls with age and cold; ceramic capacitors lose capacitance under DC bias. Use the worst-case value for hold-up time.
- **Safe discharge:** use a resistor sized for the energy (not a screwdriver), and allow for dielectric absorption — a large capacitor can recover a few percent of its voltage after being shorted.
''')

# ---------------------------------------------------------------- LC resonant frequency
rL, rC, rR = 10.0, 100e-9, 1.0   # L in µH (existing suffix variable)
rf = 1 / (2 * pi * math.sqrt(rL * 1e-6 * rC)); rw = 2 * pi * rf; rX = rw * rL * 1e-6; rQ = rX / rR; rBW = rf / rQ
rl_rows = ''
for L, C in ((1e-6, 100e-12), (10e-6, 100e-12), (100e-6, 1e-9), (10e-6, 100e-9), (1e-3, 1e-6), (100e-3, 100e-6), (240e-6, 105.5e-12)):
    f = 1 / (2 * pi * math.sqrt(L * C))
    rl_rows += f"| {eng(L, 'H')} | {eng(C, 'F')} | {eng(f, 'Hz')} | {math.sqrt(L/C):,.4g} Ω |\n"
rc_rows = ''
for nm, f in (('50 Hz (mains harmonic filter)', 50), ('1 kHz (audio)', 1e3), ('455 kHz (AM IF)', 455e3), ('1 MHz (AM broadcast)', 1e6),
              ('10.7 MHz (FM IF)', 10.7e6), ('100 MHz (FM broadcast)', 100e6)):
    rc_rows += f"| {nm} | " + ' | '.join(eng(1 / ((2 * pi * f) ** 2 * L), 'F') for L in (1e-6, 100e-6, 10e-3)) + " |\n"
W('electronics/resonant-frequency', f'''
title: LC Resonant Frequency Calculator (f = 1/2π√LC, Q & Bandwidth)
description: Calculate the resonant frequency of an LC circuit, the L or C needed to tune to a frequency, and the Q factor and bandwidth of a series RLC circuit.
category: electronics
{intro("An inductor and a capacitor together resonate at one frequency, where their reactances are equal and cancel — the principle behind radio tuning, oscillators and tuned filters, explained in [LC resonant circuit frequency](https://www.instrumentationblog.in/lc-resonant-circuit-frequency/). This LC resonant frequency calculator gives the resonant frequency from L and C (or the component needed for a target frequency), plus the reactance at resonance, the Q factor and the bandwidth when you add the circuit's series resistance.")}
keywords: [resonant frequency calculator, lc resonant frequency calculator, lc resonance, tank circuit, resonance frequency formula, rlc q factor, resonance bandwidth, 1/2pi sqrt lc]
updated: {U}
variables:
  - {{ id: L, label: Inductance, suffix: µH, default: {rL:g}, min: 0 }}
  - {{ id: C, label: Capacitance, family: capacitance, unit: nF, default: {rC*1e9:g}, min: 0 }}
  - {{ id: f, label: Resonant frequency, suffix: Hz, min: 0 }}
  - {{ id: w, label: Angular frequency, suffix: rad/s, min: 0 }}
  - {{ id: R, label: Series resistance (coil + capacitor ESR), family: resistance, unit: ohm, default: {rR:g}, min: 0 }}
  - {{ id: X, label: Reactance of L (and of C) at resonance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Q, label: Quality factor Q (series RLC), min: 0, decimals: 2 }}
  - {{ id: BW, label: −3 dB bandwidth, suffix: Hz, min: 0 }}
equations:
  - f = 1 / (2 * pi * sqrt(L * 1e-6 * C))
  - w = 2 * pi * f
  - X = w * L * 1e-6
  - Q = X / R
  - BW = f / Q
faq:
  - q: What is the resonant frequency formula?
    a: f₀ = 1 ÷ (2π√(LC)), with L in henries and C in farads. 10 µH with 100 nF resonates at {rf/1e3:.2f} kHz.
  - q: What happens at resonance?
    a: The inductive and capacitive reactances are equal (X_L = X_C = √(L/C)) and cancel. A series LC circuit then has its minimum impedance (just R); a parallel LC circuit has its maximum impedance.
  - q: How do I find the capacitor for a frequency?
    a: Enter the target frequency and the inductance, then press × on Capacitance. C = 1 ÷ ((2πf)² L) — for example 240 µH needs about 105 pF to tune to 1 MHz.
  - q: What sets the bandwidth of a resonant circuit?
    a: Resistance. For a series RLC circuit Q = X ÷ R = (1/R)√(L/C) and the −3 dB bandwidth is f₀ ÷ Q, so halving R halves the bandwidth and makes the resonance twice as sharp.
related: [electronics/lc-filter, electronics/reactance, electronics/air-core-inductor, electronics/crystal-load-capacitance]
''', f'''
## How to use the LC resonant frequency calculator

Enter the **inductance** in microhenries and the **capacitance**. The calculator gives the resonant frequency and the angular frequency. Add the **series resistance** of the coil and capacitor to get the reactance at resonance, the Q factor and the bandwidth. To design for a target frequency, enter the frequency and one component and press × on the other.

## LC resonant frequency formulas

<p class="formula">f₀ = 1 ÷ (2π√(LC)) &nbsp;·&nbsp; ω₀ = 2πf₀</p>

<p class="formula">X<sub>L</sub> = X<sub>C</sub> = ω₀L = √(L/C) &nbsp;·&nbsp; Q = X ÷ R &nbsp;·&nbsp; BW = f₀ ÷ Q</p>

## Worked example

L = {rL:g} µH, C = {rC*1e9:g} nF and a total series resistance of {rR:g} Ω:

- f₀ = 1 ÷ (2π√({rL:g} × 10⁻⁶ × {rC:g})) = **{rf:,.0f} Hz** ({rf/1e3:.2f} kHz), ω₀ = **{rw:,.0f} rad/s**
- Reactance at resonance X = ω₀L = **{rX:.3f} Ω** (equal to √(L/C))
- Q = {rX:.3f} ÷ {rR:g} = **{rQ:.2f}**, bandwidth = {rf:,.0f} ÷ {rQ:.2f} = **{rBW:,.0f} Hz**

## Resonant frequencies

| L | C | f₀ | √(L/C) |
|---|---|---|---|
{rl_rows}
## Capacitance needed to resonate at a frequency

| Target frequency | with 1 µH | with 100 µH | with 10 mH |
|---|---|---|---|
{rc_rows}
## Series vs parallel resonance

| | Series LC | Parallel LC (tank) |
|---|---|---|
| Impedance at f₀ | Minimum (≈ R) | Maximum (≈ Q × X) |
| Current at f₀ | Maximum | Minimum from source |
| Use | Band-pass in series path, notch filters | Oscillators, tuned amplifiers |

## Practical notes

- **Stray capacitance** of the coil, PCB and transistor adds to C, so real circuits resonate lower than calculated — at high frequencies leave room to trim.
- Coil resistance rises with frequency (skin effect), so Q measured at the working frequency is lower than a DC-resistance estimate suggests.
- Capacitors for tuned circuits should be stable types: C0G/NP0 ceramic, silver mica or polypropylene. X7R and Y5V ceramics drift with temperature and voltage.
- For a second-order low-pass filter (inductor in series, capacitor across a load), use the [LC filter calculator](/electronics/lc-filter/) to see the attenuation and peaking.
''')

# ---------------------------------------------------------------- Orbital period
oM, oa = 5.972e24, 6779e3
oT = 2 * pi * math.sqrt(oa ** 3 / (G * oM)); ov = math.sqrt(G * oM / oa)
def hm(s):
    h = int(s // 3600); m = round((s - h * 3600) / 60)
    if m == 60: h, m = h + 1, 0
    return f"{h} h {m:02d} min"
orbits = [('Low Earth orbit (ISS)', 420, 6371 + 420), ('Starlink shell', 550, 6371 + 550), ('Sun-synchronous weather satellites', 850, 6371 + 850),
          ('GPS (MEO)', 20200, 6371 + 20200), ('Geostationary (above the equator)', 35786, 6378 + 35786), ('Moon (mean distance)', 384400 - 6371, 384400)]
oe_rows = ''
for nm, h, r in orbits:
    T = 2 * pi * math.sqrt((r * 1e3) ** 3 / (G * oM)); v = math.sqrt(G * oM / (r * 1e3))
    ts = hm(T) if T < 2 * 86400 else f"{T/86400:.2f} days"
    oe_rows += f"| {nm} | {h:,} km | {r:,} km | {ts} | {v*3.6:,.0f} km/h |\n"
GMs, AU = 1.32712440018e20, 1.495978707e11
planets = [('Mercury', 0.387098), ('Venus', 0.723332), ('Earth', 1.000001), ('Mars', 1.523679), ('Jupiter', 5.2044), ('Saturn', 9.5826), ('Uranus', 19.2184), ('Neptune', 30.07)]
op_rows = ''
for nm, a in planets:
    T = 2 * pi * math.sqrt((a * AU) ** 3 / GMs) / (365.25 * 86400)
    op_rows += f"| {nm} | {a:g} AU | {T:.3f} years | {T*365.25:,.1f} days |\n"
W('physics/orbital-period', f'''
title: Orbital Period Calculator (Kepler's Third Law, T = 2π√(a³/GM))
description: Calculate the orbital period and speed of a satellite, moon or planet from the central mass and orbit radius using Kepler's third law — ISS, GPS and GEO.
category: physics
{intro("How long a satellite or planet takes to go round depends only on the mass it orbits and the size of its orbit. This orbital period calculator applies Kepler's third law, T = 2π√(a³/GM), to give the period and the circular orbital speed for any orbit radius — from the ISS and GPS satellites to geostationary orbit and the planets.")}
keywords: [orbital period calculator, keplers third law calculator, satellite orbit calculator, orbital speed calculator, geostationary orbit, iss orbit period, orbital velocity]
updated: {U}
variables:
  - {{ id: M, label: Central mass, suffix: kg, default: {oM:g}, min: 0, help: 'Earth 5.972 × 10²⁴ kg, Moon 7.342 × 10²² kg, Mars 6.417 × 10²³ kg, Sun 1.989 × 10³⁰ kg.' }}
  - {{ id: a, label: Orbit radius or semi-major axis (from centre), family: length, unit: km, imperialUnit: mi, default: {oa/1e3:g}, min: 0, help: 'Altitude + planet radius (Earth mean radius 6,371 km).' }}
  - {{ id: T, label: Orbital period, family: seconds, unit: min, min: 0 }}
  - {{ id: v, label: Orbital speed (circular orbit), family: velocity, unit: kmh, imperialUnit: mph, min: 0 }}
equations:
  - T = 2 * pi * sqrt(a^3 / (6.6743e-11 * M))
  - v = sqrt(6.6743e-11 * M / a)
faq:
  - q: What is Kepler's third law?
    a: "The square of the orbital period is proportional to the cube of the orbit's semi-major axis: T² = 4π²a³ ÷ (GM), where G = 6.674 × 10⁻¹¹ N·m²/kg² and M is the central mass."
  - q: How long does the ISS take to orbit Earth?
    a: About 92–93 minutes at roughly 400–420 km altitude, travelling at about 27,600 km/h, so the crew see about 16 sunrises a day.
  - q: What is a geostationary orbit?
    a: A circular orbit 35,786 km above the equator (42,164 km from Earth's centre) with a period of one sidereal day, 23 h 56 min, so the satellite stays above one point on the ground.
  - q: Should I enter altitude or radius?
    a: Radius from the centre — add the planet's radius to the altitude. For Earth, add 6,371 km (6,378 km at the equator). For an elliptical orbit use the semi-major axis, the average of the closest and farthest distances from the centre.
related: [physics/escape-velocity, physics/gravitational-force, physics/centripetal-force, physics/angular-velocity]
''', f'''
## How to use the orbital period calculator

Enter the **central mass** (Earth by default) and the **orbit radius** measured from the centre (altitude + planet radius). You get the period and the orbital speed for a circular orbit. To find the orbit radius for a given period — for example a geostationary orbit — enter the period and press × on the radius.

## Orbital period formulas

<p class="formula">T = 2π √(a³ ÷ GM) &nbsp;·&nbsp; v = √(GM ÷ a) = 2πa ÷ T</p>

G = 6.6743 × 10⁻¹¹ N·m²/kg². The formula assumes the orbiting body is much lighter than the central mass; for two comparable bodies replace M by M₁ + M₂.

## Worked example

The ISS at about 408 km altitude, a = 6,371 + 408 = {oa/1e3:,.0f} km around Earth (M = 5.972 × 10²⁴ kg):

- T = 2π √((6.779 × 10⁶ m)³ ÷ (6.6743 × 10⁻¹¹ × 5.972 × 10²⁴)) = **{oT:,.0f} s = {oT/60:.2f} min**
- v = √(GM ÷ a) = **{ov:,.0f} m/s = {ov*3.6:,.0f} km/h**

## Earth orbits

| Orbit | Altitude | Radius | Period | Speed |
|---|---|---|---|---|
{oe_rows}
The Moon's real sidereal period (27.32 days) is slightly shorter than this value because the Moon's own mass (1.2% of Earth's) also counts.

## Planets around the Sun

| Planet | Semi-major axis | Period | Period |
|---|---|---|---|
{op_rows}
For the Sun, T in years ≈ a³ᐟ² with a in astronomical units — Mars at 1.524 AU takes about 1.88 years.

## Practical notes

- **Higher orbits are slower.** Orbital speed falls as 1/√a, so to catch a spacecraft ahead of you, you drop to a lower, faster orbit first.
- Low orbits decay because of atmospheric drag; the ISS is reboosted every few months.
- The period depends only on the semi-major axis, not on how elongated an elliptical orbit is; the speed, however, varies around an ellipse (fastest at perigee).
''')

# ---------------------------------------------------------------- Doppler effect
df, dv, dvo, dvs = 700.0, 343.0, 0.0, 72 / 3.6
dfo = df * (dv + dvo) / (dv - dvs); dsh = dfo / df - 1; dfr = df * dv / (dv + dvs)
dd_rows = ''
for kmh in (30, 50, 72, 100, 120, 200, 300):
    s = kmh / 3.6; a = df * dv / (dv - s); r = df * dv / (dv + s)
    dd_rows += f"| {kmh} km/h | {a:.1f} Hz | {r:.1f} Hz | {a-r:.1f} Hz | {12*math.log2(a/r):.2f} |\n"
ds_rows = ''.join(f"| Air, {T} °C | {331.3*math.sqrt(1+T/273.15):.1f} m/s |\n" for T in (-20, 0, 10, 20, 30, 40))
W('physics/doppler-effect', f'''
title: Doppler Effect Calculator (Sound Frequency Shift)
description: Calculate the frequency heard from a moving sound source or by a moving observer with the Doppler effect formula — for sirens, trains and cars.
category: physics
{intro("When a sound source moves towards you its pitch rises, and when it moves away the pitch falls. This Doppler effect calculator gives the frequency heard for any combination of source and observer speeds, and the percentage shift. The same principle is used in radar speed guns, medical ultrasound and [Doppler ultrasonic flow meters](https://www.instrumentationblog.in/transit-time-vs-doppler-ultrasonic-flow-meter/).")}
keywords: [doppler effect calculator, doppler shift calculator, observed frequency, moving source frequency, siren frequency, doppler formula, doppler effect sound]
updated: {U}
variables:
  - {{ id: f, label: Source frequency, suffix: Hz, default: {df:g}, min: 0 }}
  - {{ id: v, label: Speed of sound, family: velocity, unit: ms, default: {dv:g}, min: 1, help: '343 m/s in air at 20 °C; 331 m/s at 0 °C; about 1,480 m/s in water.' }}
  - {{ id: vo, label: Observer speed (towards the source is positive), family: velocity, unit: kmh, imperialUnit: mph, default: {dvo:g} }}
  - {{ id: vs, label: Source speed (towards the observer is positive), family: velocity, unit: kmh, imperialUnit: mph, default: {dvs*3.6:g} }}
  - {{ id: fo, label: Observed frequency, suffix: Hz, min: 0, decimals: 1 }}
  - {{ id: sh, label: Shift, family: percent, unit: '%' }}
equations:
  - fo = f * (v + vo) / (v - vs)
  - sh = fo / f - 1
faq:
  - q: What is the Doppler effect formula for sound?
    a: f′ = f × (v + v_o) ÷ (v − v_s), where v is the speed of sound, v_o the observer's speed towards the source and v_s the source's speed towards the observer. Use negative speeds for motion apart.
  - q: Why does a siren drop in pitch as it passes?
    a: While the vehicle approaches, each wave is emitted a little closer to you, so the waves arrive bunched up (higher pitch); after it passes they are stretched out (lower pitch). The jump happens as it goes by.
  - q: How do I calculate a receding source?
    a: Enter the source speed as a negative number. A 700 Hz siren moving away at 72 km/h (20 m/s) is heard at {dfr:.0f} Hz; approaching at the same speed it is heard at {dfo:.0f} Hz.
  - q: Does the Doppler effect apply to light?
    a: Yes. Light from galaxies moving away is shifted towards red (redshift), which shows the universe is expanding. Light has no medium, so it uses the relativistic formula based only on the relative speed.
related: [physics/wavelength-frequency, physics/speed-of-sound, physics/beat-frequency, physics/decibel]
''', f'''
## How to use the Doppler effect calculator

Enter the **source frequency**, the **speed of sound** (343 m/s in air at 20 °C) and the speeds of the **observer** and **source**. Use positive speeds when they move **towards** each other and negative speeds when they move **apart**. The calculator gives the frequency heard and the shift as a percentage of the source frequency.

## Doppler effect formula

<p class="formula">f′ = f × (v + v<sub>o</sub>) ÷ (v − v<sub>s</sub>)</p>

Speeds are measured relative to the air. Wind changes the effective speeds, and the formula holds only while the source is slower than sound.

## Worked example

An ambulance siren at {df:g} Hz approaches a standing observer at 72 km/h (20 m/s), with the speed of sound {dv:g} m/s:

- Approaching: f′ = {df:g} × {dv:g} ÷ ({dv:g} − 20) = **{dfo:.1f} Hz**, a shift of **+{dsh*100:.2f}%**
- Moving away: f′ = {df:g} × {dv:g} ÷ ({dv:g} + 20) = **{dfr:.1f} Hz**
- The pitch drops by {dfo-dfr:.1f} Hz as it passes — about {12*math.log2(dfo/dfr):.1f} semitones, roughly a whole tone

## Siren at 700 Hz passing a standing listener

| Vehicle speed | Approaching | Moving away | Drop as it passes | Semitones |
|---|---|---|---|---|
{dd_rows}
## Speed of sound in air

| Medium | Speed |
|---|---|
{ds_rows}| Water, 20 °C | about 1,480 m/s |
| Steel | about 5,900 m/s |

Speed of sound in air is 331.3 √(1 + T/273.15) m/s, rising about 0.6 m/s per °C.

## Practical notes

- **Radar and laser speed guns** use the Doppler shift of reflected waves; for a reflection the shift is doubled (the target acts as a moving observer and then a moving source).
- **Doppler ultrasonic flow meters** measure the shift of sound reflected by bubbles or particles in the liquid, so they need some suspended solids or gas; clean liquids need a transit-time meter.
- **Medical ultrasound** uses the same principle to measure blood flow velocity.
- At or above the speed of sound the denominator becomes zero or negative: the waves pile up into a shock wave, heard as a sonic boom.
''')

print(len(DONE), 'improved:', ' '.join(DONE))
