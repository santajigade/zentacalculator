import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
D = '2026-11-03'
G = 9.80665
C0 = 299792458.0         # speed of light, m/s
KE = 8.9875517923e9      # Coulomb constant, N·m²/C²
R = 8.314462618          # gas constant, J/(mol·K)

# ================================================================ PHYSICS

# ---------------------------------------------------------------- Electric field & potential
ef_q, ef_r = 5.0, 0.5
ef_E = KE * ef_q * 1e-6 / ef_r**2
ef_V = KE * ef_q * 1e-6 / ef_r
ef_rows = ''.join(f"| {r:g} m | {KE*1e-6/r**2:,.0f} V/m | {KE*1e-6/r:,.0f} V |\n" for r in (0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10))
page('physics', 'electric-field', f'''
title: Electric Field Calculator (Point Charge E & Potential V)
description: Calculate the electric field strength and electric potential at a distance from a point charge with E = kq/r² and V = kq/r, plus the force on a test charge.
category: physics
{intro("A point charge creates an electric field that weakens with the square of distance, and an electric potential that falls off with distance itself. This electric field calculator applies Coulomb's law to give the field strength E, the potential V and the force on a test charge placed at that point — the same field that a [capacitor uses to store energy](ib:capacitor-working-principle) between its plates.")}
keywords: [electric field calculator, electric field strength calculator, electric potential calculator, point charge electric field, e = kq/r^2, v = kq/r, coulomb constant]
updated: {D}
variables:
  - {{ id: q, label: Source charge, suffix: µC, default: 5, help: 'Negative for a negative charge; the field then points toward the charge.' }}
  - {{ id: r, label: Distance from the charge, family: length, unit: m, imperialUnit: ft, default: 0.5, min: 0 }}
  - {{ id: q0, label: Test charge, suffix: µC, default: 1 }}
  - {{ id: E, label: Electric field strength, suffix: V/m }}
  - {{ id: V, label: Electric potential, family: voltage, unit: V }}
  - {{ id: F, label: Force on the test charge, family: force, unit: N, imperialUnit: lbf }}
equations:
  - E = 8.9875517923e9 * q * 1e-6 / r^2
  - V = 8.9875517923e9 * q * 1e-6 / r
  - F = E * q0 * 1e-6
faq:
  - q: What is the formula for the electric field of a point charge?
    a: E = kq ÷ r², where k = 8.988 × 10⁹ N·m²/C², q is the charge in coulombs and r the distance in metres. The unit is volts per metre, which is the same as newtons per coulomb.
  - q: What is the difference between electric field and electric potential?
    a: The field E is a vector — the force per coulomb on a test charge — and falls as 1/r². The potential V = kq/r is a scalar — the energy per coulomb — and falls as 1/r. The field is the rate at which potential changes with distance.
  - q: How do I find the field from several charges?
    a: Calculate the field of each charge separately and add them as vectors (superposition). Potentials are simply added as numbers, which is often easier.
  - q: What field strength causes air to break down?
    a: Dry air at sea level breaks down at roughly 3 × 10⁶ V/m (3 kV/mm), which limits how much charge an object in air can hold.
related: [physics/coulombs-law, physics/parallel-plate-capacitor, physics/lorentz-force, physics/ohms-law]
''', f'''
## How to use the electric field calculator

Enter the **source charge** in microcoulombs (negative for a negative charge), the **distance** from it, and optionally a **test charge**. The calculator returns the electric field strength, the electric potential at that point (taking zero at infinity) and the force on the test charge. Clear the distance and enter a field value to find how far away a given field strength occurs.

## Electric field formula

<p class="formula">E = k q ÷ r² &nbsp;·&nbsp; V = k q ÷ r &nbsp;·&nbsp; F = E q<sub>0</sub></p>

k = 1 ÷ (4πε<sub>0</sub>) = 8.9875517923 × 10⁹ N·m²/C².

## Example

A 5 µC charge, measured 0.5 m away:

- E = 8.988 × 10⁹ × 5 × 10⁻⁶ ÷ 0.5² = **{ef_E:,.0f} V/m**
- V = 8.988 × 10⁹ × 5 × 10⁻⁶ ÷ 0.5 = **{ef_V:,.0f} V**
- Force on a 1 µC test charge = {ef_E:,.0f} × 10⁻⁶ = **{ef_E*1e-6:.4f} N**

## Field and potential of a 1 µC charge

| Distance | Field E | Potential V |
|---|---|---|
{ef_rows}
## Notes

- Outside a uniformly charged sphere the field is the same as for a point charge at its centre.
- Between two parallel plates the field is uniform, E = V ÷ d — see the [parallel plate capacitor calculator](/physics/parallel-plate-capacitor/).
- The force between two charges follows directly from [Coulomb's law](/physics/coulombs-law/).
''')

# ---------------------------------------------------------------- Speed of sound in gases
ss_g, ss_M, ss_T, ss_f = 1.4, 28.965, 20.0, 1000.0
def sos(g, M, Tc): return math.sqrt(g * R * (Tc + 273.15) / (M * 1e-3))
ss_v = sos(ss_g, ss_M, ss_T)
gases = [('Dry air', 1.4, 28.965), ('Nitrogen (N₂)', 1.4, 28.014), ('Oxygen (O₂)', 1.395, 31.999), ('Carbon dioxide (CO₂)', 1.289, 44.01),
         ('Methane (CH₄)', 1.304, 16.043), ('Hydrogen (H₂)', 1.405, 2.016), ('Helium (He)', 1.667, 4.0026), ('Argon (Ar)', 1.667, 39.948)]
ss_rows = ''.join(f"| {nm} | {g:g} | {M:g} | {sos(g, M, 0):.0f} m/s | {sos(g, M, 20):.0f} m/s | {sos(g, M, 100):.0f} m/s |\n" for nm, g, M in gases)
ss_trows = ''.join(f"| {t} °C | {sos(1.4, 28.965, t):.1f} m/s | {sos(1.4, 28.965, t)/1000*1000:.1f} mm/ms |\n" for t in (-40, -20, 0, 10, 20, 30, 40, 60, 80, 100))
page('physics', 'speed-of-sound', f'''
title: Speed of Sound Calculator (Air & Gases, by Temperature)
description: Calculate the speed of sound in air or any ideal gas from temperature, heat capacity ratio γ and molar mass with v = √(γRT/M), plus the wavelength.
category: physics
{intro("Sound travels faster in warm gas and in light gas, because the speed depends on temperature and molar mass rather than pressure. This speed of sound calculator uses v = √(γRT/M) for air, nitrogen, CO₂, helium and other gases — the same temperature correction that [ultrasonic level transmitters](ib:how-does-an-ultrasonic-level-transmitter-work) and [ultrasonic flow meters](ib:how-ultrasonic-flow-meter-works) apply to their time-of-flight readings.")}
keywords: [speed of sound calculator, speed of sound in air calculator, speed of sound temperature, sound velocity in gas, v = sqrt(gamma r t / m), speed of sound helium, wavelength of sound]
updated: {D}
variables:
  - {{ id: gam, label: Heat capacity ratio γ (cp/cv), default: 1.4, min: 1, help: 'Air, N₂, O₂ ≈ 1.40 · CO₂ 1.29 · CH₄ 1.30 · He, Ar 1.667' }}
  - {{ id: M, label: Molar mass, suffix: g/mol, default: 28.965, min: 0, help: 'Dry air 28.965 · N₂ 28.014 · CO₂ 44.01 · He 4.003' }}
  - {{ id: T, label: Gas temperature, family: temperature, unit: C, imperialUnit: F, default: 20, min: 0 }}
  - {{ id: f, label: Sound frequency, family: frequency, unit: Hz, default: 1000, min: 0 }}
  - {{ id: v, label: Speed of sound, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: lam, label: Wavelength, family: length, unit: m, imperialUnit: ft, min: 0 }}
equations:
  - v = sqrt(gam * 8.314462618 * T / (M * 1e-3))
  - lam = v / f
faq:
  - q: What is the speed of sound in air?
    a: About 331 m/s at 0 °C and 343 m/s at 20 °C in dry air. It rises by roughly 0.6 m/s for every degree Celsius.
  - q: Does pressure change the speed of sound?
    a: Not for an ideal gas. Raising the pressure raises the density by the same factor, so √(γP/ρ) = √(γRT/M) stays the same. Only temperature and gas composition matter.
  - q: Why does helium make your voice sound higher?
    a: Sound travels almost three times faster in helium (about 1,000 m/s), so the resonances of your vocal tract shift upward even though your vocal cords vibrate at the same rate.
  - q: How does humidity affect the speed of sound?
    a: Water vapour (18 g/mol) is lighter than air, so humid air carries sound slightly faster — about 0.1–0.6% faster at room temperature, depending on humidity.
related: [physics/wavelength-frequency, physics/doppler-effect, physics/decibel, engineering/ultrasonic-level]
''', f'''
## How to use the speed of sound calculator

Enter the gas's **heat capacity ratio γ**, its **molar mass** and the **temperature**. The calculator returns the speed of sound and, for the frequency you enter, the wavelength. Values for common gases are in the table below; for mixtures use the mole-weighted molar mass.

## Speed of sound formula

<p class="formula">v = √(γ R T ÷ M) &nbsp;·&nbsp; λ = v ÷ f</p>

R = 8.314 J/(mol·K), T is the absolute temperature in kelvin and M the molar mass in kg/mol.

## Example

Dry air (γ = 1.4, M = 28.965 g/mol) at 20 °C:

- v = √(1.4 × 8.314 × 293.15 ÷ 0.028965) = **{ss_v:.1f} m/s**
- Wavelength of a 1 kHz tone = {ss_v:.1f} ÷ 1000 = **{ss_v/ss_f:.4f} m**

## Speed of sound in common gases

| Gas | γ | M (g/mol) | 0 °C | 20 °C | 100 °C |
|---|---|---|---|---|---|
{ss_rows}
## Speed of sound in dry air by temperature

| Temperature | Speed | Distance per millisecond |
|---|---|---|
{ss_trows}
## Practical notes

- An ultrasonic level gauge that assumes 343 m/s but works in 60 °C air reads the distance about {(sos(1.4,28.965,60)/sos(1.4,28.965,20)-1)*100:.1f}% short — the reason these instruments carry a temperature sensor. See the [ultrasonic level calculator](/engineering/ultrasonic-level/).
- Sound travels much faster in liquids and solids (water ≈ 1,480 m/s, steel ≈ 5,900 m/s); this formula applies to gases only.
''')

# ---------------------------------------------------------------- String frequency (standing waves)
sf_L, sf_T, sf_mu, sf_n = 0.648, 70.0, 0.4, 1
sf_v = math.sqrt(sf_T / (sf_mu * 1e-3))
sf_f = sf_n / (2 * sf_L) * sf_v
sf_rows = ''.join(f"| {k} | {k*sf_f:.1f} Hz | {2*sf_L/k:.3f} m | {k-1} |\n" for k in range(1, 9))
page('physics', 'string-frequency', f'''
title: String Frequency Calculator (Standing Waves & Harmonics)
description: Find the fundamental frequency and harmonics of a vibrating string from its length, tension and linear density, f = (n/2L)·√(T/μ), plus wave speed.
category: physics
intro: "A string fixed at both ends vibrates in standing waves whose wavelengths fit a whole number of half-waves into its length. This string frequency calculator uses f = (n ÷ 2L) √(T ÷ μ) to find the fundamental and harmonic frequencies, the wave speed and the wavelength — useful for musical instruments, cables and wire-tension checks."
keywords: [string frequency calculator, standing wave calculator, vibrating string frequency, string tension frequency, harmonics calculator, f = 1/2l sqrt(t/mu), guitar string tension calculator]
updated: {D}
variables:
  - {{ id: L, label: Vibrating length, family: length, unit: mm, imperialUnit: in, default: 648, min: 0 }}
  - {{ id: T, label: String tension, family: force, unit: N, imperialUnit: lbf, default: 70, min: 0 }}
  - {{ id: mu, label: Linear density (mass per length), suffix: g/m, default: 0.4, min: 0, help: 'Mass of the string divided by its length. A steel guitar high-E string is about 0.4 g/m.' }}
  - {{ id: k, label: Harmonic number n, default: 1, min: 1 }}
  - {{ id: v, label: Wave speed on the string, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: f, label: Frequency of harmonic n, family: frequency, unit: Hz, min: 0 }}
  - {{ id: lam, label: Wavelength, family: length, unit: mm, imperialUnit: in, min: 0 }}
equations:
  - v = sqrt(T / (mu * 1e-3))
  - f = k / (2 * L) * v
  - lam = 2 * L / k
faq:
  - q: What is the formula for the frequency of a string?
    a: f = (n ÷ 2L) × √(T ÷ μ), where L is the vibrating length, T the tension in newtons, μ the mass per metre in kg/m and n the harmonic number (1 for the fundamental).
  - q: How does tension change the pitch?
    a: Frequency is proportional to the square root of tension, so raising the pitch by an octave (double the frequency) needs four times the tension.
  - q: What are harmonics?
    a: A string can vibrate with 1, 2, 3… half-wavelengths along its length. These modes have frequencies n × f₁ and together give an instrument its tone. Harmonic n has n − 1 nodes between the ends.
  - q: How do I find the tension needed for a note?
    a: Enter the length, the linear density and the target frequency, then clear the tension field. The calculator solves T = μ (2Lf ÷ n)².
related: [physics/wavelength-frequency, physics/beat-frequency, physics/simple-harmonic-motion, physics/speed-of-sound]
''', f'''
## How to use the string frequency calculator

Enter the **vibrating length** (nut to bridge on an instrument), the **tension**, the string's **linear density** in grams per metre and the **harmonic number**. The calculator returns the wave speed, the frequency of that harmonic and its wavelength. To find the tension for a target note, enter the frequency and clear the tension.

## String frequency formula

<p class="formula">v = √(T ÷ μ) &nbsp;·&nbsp; f<sub>n</sub> = n v ÷ (2L) &nbsp;·&nbsp; λ<sub>n</sub> = 2L ÷ n</p>

## Example

A steel guitar string, 648 mm long, 0.4 g/m, tensioned to 70 N:

- Wave speed v = √(70 ÷ 0.0004) = **{sf_v:.1f} m/s**
- Fundamental f₁ = 1 ÷ (2 × 0.648) × {sf_v:.1f} = **{sf_f:.1f} Hz** (close to the E₄ note at 329.6 Hz)

## Harmonics of the example string

| Harmonic n | Frequency | Wavelength | Nodes between ends |
|---|---|---|---|
{sf_rows}
## Notes

- Stiff, thick strings are slightly inharmonic: their overtones sit a little above exact multiples of f₁.
- The same equation estimates the tension in a stay cable or wire rope from its measured natural frequency.
- Two strings tuned slightly apart produce audible beats — see the [beat frequency calculator](/physics/beat-frequency/).
''')

# ---------------------------------------------------------------- Beat frequency
bf_1, bf_2 = 440.0, 444.0
bf_b = abs(bf_1 - bf_2)
bf_rows = ''.join(f"| 440 Hz | {440+d:g} Hz | {d:g} Hz | {1/d:.3f} s | {440+d/2:g} Hz |\n" for d in (0.5, 1, 2, 3, 4, 5, 7, 10))
page('physics', 'beat-frequency', f'''
title: Beat Frequency Calculator (f_beat = |f₁ − f₂|)
description: Calculate the beat frequency and beat period when two tones of nearly equal frequency combine, plus the perceived average pitch, for tuning and acoustics.
category: physics
intro: "When two sound waves of slightly different frequency overlap, their sum swells and fades at a rate equal to the difference between them. This beat frequency calculator gives the number of beats per second, the time between beats and the average pitch you hear — the basis of tuning instruments by ear."
keywords: [beat frequency calculator, beats per second calculator, beat frequency formula, f beat = f1 - f2, tuning beats, beat period, interference of sound waves]
updated: {D}
variables:
  - {{ id: f1, label: Frequency 1, family: frequency, unit: Hz, default: 440, min: 0 }}
  - {{ id: f2, label: Frequency 2, family: frequency, unit: Hz, default: 444, min: 0 }}
  - {{ id: fb, label: Beat frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: Tb, label: Beat period, family: seconds, unit: s, min: 0 }}
  - {{ id: fa, label: Perceived (average) pitch, family: frequency, unit: Hz, min: 0 }}
equations:
  - fb = abs(f1 - f2)
  - Tb = 1 / fb
  - fa = (f1 + f2) / 2
faq:
  - q: What is beat frequency?
    a: The rate at which the loudness of two combined tones rises and falls. It equals the difference between the two frequencies, f_beat = |f₁ − f₂|.
  - q: How are beats used to tune instruments?
    a: Play the string together with a reference tone and adjust until the beats slow down and disappear. At 0 Hz beat frequency the two are in unison.
  - q: Why can't we hear beats between very different frequencies?
    a: Above roughly 15–20 Hz the beats blur into a rough sound, and with larger differences the ear hears two separate tones instead.
  - q: What pitch do you hear during beats?
    a: The average of the two frequencies, (f₁ + f₂) ÷ 2, whose loudness pulses at the beat frequency.
related: [physics/string-frequency, physics/wavelength-frequency, physics/doppler-effect, physics/decibel]
''', f'''
## How to use the beat frequency calculator

Enter the two **frequencies**. The calculator returns the beat frequency (beats per second), the beat period and the average pitch you hear. To find an unknown second frequency, count the beats and remember there are two answers: f₁ + f<sub>beat</sub> or f₁ − f<sub>beat</sub>.

## Beat frequency formula

<p class="formula">f<sub>beat</sub> = |f<sub>1</sub> − f<sub>2</sub>| &nbsp;·&nbsp; T<sub>beat</sub> = 1 ÷ f<sub>beat</sub> &nbsp;·&nbsp; f<sub>avg</sub> = (f<sub>1</sub> + f<sub>2</sub>) ÷ 2</p>

The sum of two equal-amplitude waves is 2A cos(2π·Δf/2·t) · sin(2π·f<sub>avg</sub>·t); the envelope peaks twice per cycle of Δf/2, so loudness pulses at Δf.

## Example

A tuning fork at 440 Hz and a string at 444 Hz:

- Beat frequency = |440 − 444| = **{bf_b:g} Hz** (four beats every second)
- Beat period = 1 ÷ {bf_b:g} = **{1/bf_b:g} s**
- Perceived pitch = (440 + 444) ÷ 2 = **{(bf_1+bf_2)/2:g} Hz**

## Beats against an A440 reference

| Reference | Second tone | Beat frequency | Beat period | Perceived pitch |
|---|---|---|---|---|
{bf_rows}
## Notes

- The same principle appears in radio as the heterodyne: mixing two signals produces their difference frequency.
- Beats also occur between a moving and a stationary source because of the [Doppler effect](/physics/doppler-effect/).
''')

# ---------------------------------------------------------------- Inverse square law
is_I1, is_d1, is_d2 = 100.0, 1.0, 3.0
is_I2 = is_I1 * (is_d1 / is_d2)**2
is_dB = 20 * math.log10(is_d2 / is_d1)
is_rows = ''.join(f"| {k:g} × | {100/k**2:.2f}% | {20*math.log10(k):.2f} dB |\n" for k in (1.5, 2, 3, 4, 5, 10, 20, 50, 100))
page('physics', 'inverse-square-law', f'''
title: Inverse Square Law Calculator (Light, Sound & Radiation)
description: Calculate how intensity of light, sound or radiation falls with distance using I₂ = I₁(d₁/d₂)², with the decibel drop and distance for a target level.
category: physics
intro: "Energy spreading out from a point source covers an area that grows with the square of distance, so its intensity falls as 1/d². This inverse square law calculator scales a measured intensity, illuminance, sound intensity or radiation dose rate from one distance to another and gives the change in decibels."
keywords: [inverse square law calculator, inverse square law light, inverse square law sound, radiation dose distance calculator, intensity distance formula, i1 d1^2 = i2 d2^2, lux distance calculator]
updated: {D}
variables:
  - {{ id: I1, label: Intensity at distance 1, default: 100, min: 0, help: 'Any unit — lux, W/m², µSv/h, cd — the result is in the same unit.' }}
  - {{ id: d1, label: Distance 1, family: length, unit: m, imperialUnit: ft, default: 1, min: 0 }}
  - {{ id: d2, label: Distance 2, family: length, unit: m, imperialUnit: ft, default: 3, min: 0 }}
  - {{ id: I2, label: Intensity at distance 2, min: 0 }}
  - {{ id: ratio, label: Intensity ratio I₂/I₁, family: percent, unit: '%', min: 0 }}
  - {{ id: dB, label: Level change (drop), suffix: dB, decimals: 2 }}
equations:
  - I2 = I1 * (d1 / d2)^2
  - ratio = (d1 / d2)^2
  - dB = 20 * log10(d2 / d1)
faq:
  - q: What is the inverse square law?
    a: The intensity from a point source is inversely proportional to the square of the distance, I ∝ 1/d². Doubling the distance cuts the intensity to one quarter.
  - q: How many decibels does sound drop when distance doubles?
    a: About 6 dB (20 × log₁₀ 2 = 6.02 dB) for a point source in free field. Indoors, reflections make the drop smaller.
  - q: How does the inverse square law apply to radiation safety?
    a: Dose rate from a small gamma source falls as 1/d², so moving from 1 m to 2 m cuts exposure to 25%. Distance is one of the three basic protections, with time and shielding.
  - q: When does the inverse square law not apply?
    a: Close to large sources (a line or area source), with focused beams such as lasers or spotlights, and where the medium absorbs energy (fog, water). A rule of thumb is that it holds beyond about five times the source's largest dimension.
related: [physics/decibel, physics/stefan-boltzmann-law, physics/radioactive-activity, physics/gravitational-force]
''', f'''
## How to use the inverse square law calculator

Enter the **intensity measured at distance 1** in any unit, then the two **distances**. The calculator returns the intensity at distance 2 in the same unit, the ratio as a percentage and the level change in decibels. To find how far away a target intensity occurs, enter I₂ and clear distance 2.

## Inverse square law formula

<p class="formula">I<sub>2</sub> = I<sub>1</sub> × (d<sub>1</sub> ÷ d<sub>2</sub>)² &nbsp;·&nbsp; ΔL = 20 log<sub>10</sub>(d<sub>2</sub> ÷ d<sub>1</sub>) dB</p>

## Example

A lamp gives 100 lux at 1 m. At 3 m:

- I₂ = 100 × (1 ÷ 3)² = **{is_I2:.2f} lux** ({is_I2/is_I1*100:.2f}% of the original)
- Level change = 20 × log₁₀(3) = **{is_dB:.2f} dB**

## Intensity versus distance multiple

| Distance multiple | Remaining intensity | Drop in dB |
|---|---|---|
{is_rows}
## Notes

- Decibels use 10 log₁₀ of an intensity ratio, which equals 20 log₁₀ of the distance ratio.
- The same 1/r² rule governs gravity and electric fields — see the [gravitational force calculator](/physics/gravitational-force/).
''')

# ---------------------------------------------------------------- Time dilation
td_t0, td_b = 1.0, 0.9
td_g = 1 / math.sqrt(1 - td_b**2)
td_rows = ''.join(f"| {b*100:g}% | {b*C0/1000:,.0f} km/s | {1/math.sqrt(1-b*b):.4f} | {365.25/math.sqrt(1-b*b):,.1f} days |\n" for b in (0.01, 0.1, 0.3, 0.5, 0.8, 0.9, 0.95, 0.99, 0.999))
page('physics', 'time-dilation', f'''
title: Time Dilation Calculator (Special Relativity, Lorentz Factor)
description: Calculate relativistic time dilation and the Lorentz factor γ for a speed as a fraction of light speed — how much time passes for a stationary observer.
category: physics
intro: "Special relativity predicts that a moving clock ticks slower than a clock at rest, by the Lorentz factor γ = 1/√(1 − v²/c²). This time dilation calculator converts the proper time measured on board into the time that passes for a stationary observer, and gives γ and the speed in km/s."
keywords: [time dilation calculator, lorentz factor calculator, special relativity calculator, relativistic time dilation, gamma factor, t = t0 / sqrt(1 - v^2/c^2), twin paradox calculator]
updated: {D}
variables:
  - {{ id: t0, label: Proper time (moving clock), family: time, unit: yr, default: 1, min: 0 }}
  - {{ id: b, label: Speed as a fraction of light speed (v/c), family: percent, unit: '%', default: 90, min: 0, max: 0.999999999 }}
  - {{ id: gam, label: Lorentz factor γ, min: 1, decimals: 4 }}
  - {{ id: t, label: Time for the stationary observer, family: time, unit: yr, min: 0 }}
  - {{ id: dt, label: Extra time elapsed (t − t₀), family: time, unit: yr, min: 0 }}
  - {{ id: v, label: Speed, family: velocity, unit: ms, imperialUnit: mph, min: 0 }}
equations:
  - gam = 1 / sqrt(1 - b^2)
  - t = gam * t0
  - dt = t - t0
  - v = b * 299792458
faq:
  - q: What is the time dilation formula?
    a: t = t₀ ÷ √(1 − v²/c²) = γ t₀, where t₀ is the proper time measured by the moving clock and t the time measured by an observer who sees it moving at speed v.
  - q: What is the Lorentz factor?
    a: γ = 1 ÷ √(1 − v²/c²). It is 1 at rest, about 1.005 at 10% of light speed, 2.29 at 90% and grows without limit as v approaches c.
  - q: Is time dilation real?
    a: Yes. Fast muons from cosmic rays survive long enough to reach the ground only because of it, and GPS satellite clocks are corrected for both velocity (special) and gravitational (general) time dilation.
  - q: Does the moving traveller feel time slow down?
    a: No. Each observer sees their own clock tick normally. The difference appears when the clocks are compared, as in the twin paradox.
related: [physics/mass-energy-equivalence, physics/de-broglie-wavelength, physics/photon-energy, physics/speed-distance-time]
''', f'''
## How to use the time dilation calculator

Enter the **proper time** that passes on the moving clock and the **speed as a percentage of the speed of light**. The calculator returns the Lorentz factor γ, the time that passes for a stationary observer, the extra time and the speed itself. Clear the speed and enter both times to find the speed that produces a given dilation.

## Time dilation formula

<p class="formula">γ = 1 ÷ √(1 − v²/c²) &nbsp;·&nbsp; t = γ × t<sub>0</sub></p>

c = 299,792,458 m/s.

## Example

A spacecraft travels at 90% of light speed for 1 year of on-board time:

- γ = 1 ÷ √(1 − 0.9²) = 1 ÷ √0.19 = **{td_g:.4f}**
- Time for an observer on Earth = {td_g:.4f} × 1 = **{td_g:.4f} years** ({td_g*365.25:.0f} days)
- Extra time = **{td_g-1:.4f} years**

## Lorentz factor by speed

| Speed (v/c) | Speed | γ | Earth time for 1 year on board |
|---|---|---|---|
{td_rows}
## Notes

- The same γ contracts lengths along the motion (L = L₀ ÷ γ) and raises the energy of a moving mass (E = γmc²) — compare the [E = mc² calculator](/physics/mass-energy-equivalence/).
- Gravity also slows clocks (general relativity); this calculator covers only the speed effect.
''')

# ---------------------------------------------------------------- Final temperature of a mixture
ft_m1, ft_c1, ft_T1, ft_m2, ft_c2, ft_T2 = 0.5, 897.0, 150.0, 2.0, 4186.0, 20.0
ft_Tf = (ft_m1*ft_c1*ft_T1 + ft_m2*ft_c2*ft_T2) / (ft_m1*ft_c1 + ft_m2*ft_c2)
ft_Q = ft_m1 * ft_c1 * (ft_T1 - ft_Tf)
mats = [('Water', 4186), ('Ice (−10 °C)', 2050), ('Aluminium', 897), ('Copper', 385), ('Iron / steel', 450), ('Glass', 840), ('Olive oil', 1970), ('Ethanol', 2440)]
ft_rows = ''.join(f"| {nm} | {c:,} | {(1*c*100+1*4186*20)/(1*c+1*4186):.1f} °C |\n" for nm, c in mats)
page('physics', 'final-temperature', f'''
title: Final Temperature Calculator (Mixing Two Substances)
description: Find the equilibrium temperature when two substances at different temperatures are mixed, from their masses and specific heats, plus the heat transferred.
category: physics
intro: "When a hot object meets a cold one in an insulated container, heat flows until both reach the same temperature, and the heat lost by one equals the heat gained by the other. This final temperature calculator solves that heat balance for any two substances from their masses, specific heat capacities and starting temperatures."
keywords: [final temperature calculator, equilibrium temperature calculator, mixing temperature calculator, specific heat mixture, heat balance calculator, calorimetry final temperature, m1c1t1 + m2c2t2]
updated: {D}
variables:
  - {{ id: m1, label: Mass of substance 1, family: mass, unit: kg, imperialUnit: lb, default: 0.5, min: 0 }}
  - {{ id: c1, label: Specific heat of substance 1, suffix: J/kg·K, default: 897, min: 0, help: 'Water 4186 · Aluminium 897 · Steel 450 · Copper 385' }}
  - {{ id: T1, label: Temperature of substance 1, family: temperature, unit: C, imperialUnit: F, default: 150, min: 0 }}
  - {{ id: m2, label: Mass of substance 2, family: mass, unit: kg, imperialUnit: lb, default: 2, min: 0 }}
  - {{ id: c2, label: Specific heat of substance 2, suffix: J/kg·K, default: 4186, min: 0 }}
  - {{ id: T2, label: Temperature of substance 2, family: temperature, unit: C, imperialUnit: F, default: 20, min: 0 }}
  - {{ id: Tf, label: Final (equilibrium) temperature, family: temperature, unit: C, imperialUnit: F, min: 0 }}
  - {{ id: Q, label: Heat transferred from 1 to 2, family: energy, unit: kJ, imperialUnit: BTU }}
equations:
  - Tf = (m1 * c1 * T1 + m2 * c2 * T2) / (m1 * c1 + m2 * c2)
  - Q = m1 * c1 * (T1 - Tf)
faq:
  - q: How do you calculate the final temperature of a mixture?
    a: Set heat lost equal to heat gained, m₁c₁(T₁ − T_f) = m₂c₂(T_f − T₂), and solve — T_f = (m₁c₁T₁ + m₂c₂T₂) ÷ (m₁c₁ + m₂c₂). It is a weighted average of the temperatures, weighted by heat capacity m·c.
  - q: What if one of the substances melts or boils?
    a: This formula assumes no phase change. If ice melts or water boils, add the latent heat (m·L) to the balance — see the latent heat calculator.
  - q: Why does a small hot metal block barely warm a lot of water?
    a: Water's specific heat (4186 J/kg·K) is about 4.7 times aluminium's and 11 times copper's, so water absorbs a lot of heat for a small temperature rise.
  - q: Do the temperatures have to be in kelvin?
    a: No. Because the formula is a weighted average and uses only temperature differences, °C, °F or K all give the correct result in the same scale.
related: [chemistry/specific-heat, physics/latent-heat, engineering/heat-duty, physics/newtons-law-of-cooling]
''', f'''
## How to use the final temperature calculator

Enter the **mass**, **specific heat capacity** and **starting temperature** of each substance. The calculator returns the equilibrium temperature and the heat that flows from substance 1 to substance 2 (negative if substance 1 is the colder one). It assumes an insulated container and no melting or boiling.

## Final temperature formula

<p class="formula">T<sub>f</sub> = (m<sub>1</sub>c<sub>1</sub>T<sub>1</sub> + m<sub>2</sub>c<sub>2</sub>T<sub>2</sub>) ÷ (m<sub>1</sub>c<sub>1</sub> + m<sub>2</sub>c<sub>2</sub>) &nbsp;·&nbsp; Q = m<sub>1</sub>c<sub>1</sub>(T<sub>1</sub> − T<sub>f</sub>)</p>

## Example

A 0.5 kg aluminium block at 150 °C is dropped into 2 kg of water at 20 °C:

- Heat capacities: 0.5 × 897 = 448.5 J/K and 2 × 4186 = 8,372 J/K
- T<sub>f</sub> = (448.5 × 150 + 8,372 × 20) ÷ (448.5 + 8,372) = **{ft_Tf:.2f} °C**
- Heat transferred Q = 448.5 × (150 − {ft_Tf:.2f}) = **{ft_Q/1000:.2f} kJ**

## 1 kg at 100 °C mixed with 1 kg of water at 20 °C

| Substance at 100 °C | Specific heat (J/kg·K) | Final temperature |
|---|---|---|
{ft_rows}
## Notes

- Real containers absorb some heat; in a calorimeter, add the vessel's heat capacity (its "water equivalent") to the cold side.
- For heating a flowing stream rather than a batch, use the [heat duty calculator](/engineering/heat-duty/).
''')

# ---------------------------------------------------------------- Carnot efficiency
ca_Th, ca_Tc, ca_Q = 500.0, 30.0, 100.0
ca_eta = 1 - (ca_Tc + 273.15) / (ca_Th + 273.15)
ca_COPr = (ca_Tc + 273.15) / (ca_Th - ca_Tc)
ca_COPh = (ca_Th + 273.15) / (ca_Th - ca_Tc)
ca_rows = ''.join(f"| {th} °C | {(1-(25+273.15)/(th+273.15))*100:.1f}% |\n" for th in (100, 200, 300, 400, 500, 600, 800, 1000, 1500))
ca_hp = ''.join(f"| {tc} °C | 35 °C | {(35+273.15)/(35-tc):.2f} | {(tc+273.15)/(35-tc):.2f} |\n" for tc in (-20, -10, 0, 5, 10, 15))
page('physics', 'carnot-efficiency', f'''
title: Carnot Efficiency Calculator (Heat Engine, Heat Pump COP)
description: Calculate the maximum Carnot efficiency of a heat engine and the ideal COP of a refrigerator or heat pump from hot and cold reservoir temperatures.
category: physics
{intro("No heat engine working between two temperatures can beat the efficiency of an ideal reversible Carnot cycle, η = 1 − T_c/T_h, and no refrigerator or heat pump can beat the Carnot COP. This Carnot efficiency calculator gives all three limits from the reservoir temperatures, together with the maximum work from a heat input — the benchmark for judging real [chiller capacity and COP](ib:calculate-industrial-chiller-capacity).")}
keywords: [carnot efficiency calculator, carnot cycle calculator, maximum efficiency heat engine, carnot cop calculator, heat pump cop calculator, 1 - tc/th, thermal efficiency limit]
updated: {D}
variables:
  - {{ id: Th, label: Hot reservoir temperature, family: temperature, unit: C, imperialUnit: F, default: 500, min: 0 }}
  - {{ id: Tc, label: Cold reservoir temperature, family: temperature, unit: C, imperialUnit: F, default: 30, min: 0 }}
  - {{ id: Qh, label: Heat input rate, family: power, unit: kW, imperialUnit: BTUh, default: 100, min: 0 }}
  - {{ id: eta, label: Carnot efficiency, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: W, label: Maximum work output, family: power, unit: kW, imperialUnit: hp, min: 0 }}
  - {{ id: COPr, label: Carnot COP (refrigerator), min: 0, decimals: 3 }}
  - {{ id: COPh, label: Carnot COP (heat pump), min: 0, decimals: 3 }}
equations:
  - eta = 1 - Tc / Th
  - W = eta * Qh
  - COPr = Tc / (Th - Tc)
  - COPh = Th / (Th - Tc)
faq:
  - q: What is the Carnot efficiency formula?
    a: η = 1 − T_c ÷ T_h, with both temperatures in kelvin. It is the highest efficiency any heat engine can reach between those two temperatures.
  - q: Why must temperatures be in kelvin?
    a: The formula uses a ratio of absolute temperatures. The calculator converts °C or °F to kelvin for you; entering 500 °C and 30 °C means 773.15 K and 303.15 K.
  - q: How efficient are real power plants compared with Carnot?
    a: Typically 50–70% of the Carnot limit. A steam plant with 550 °C steam and 30 °C cooling water has a Carnot limit near 63% but achieves about 35–45%; combined-cycle gas plants reach about 60%.
  - q: What is the Carnot COP of a heat pump?
    a: COP = T_h ÷ (T_h − T_c). Heating to 35 °C from 0 °C outside gives an ideal COP of 8.8; real heat pumps achieve about 3–4.5 because of compressor and heat-exchanger losses.
related: [physics/ideal-gas-law, engineering/heat-duty, physics/work-and-power, physics/stefan-boltzmann-law]
''', f'''
## How to use the Carnot efficiency calculator

Enter the **hot** and **cold reservoir temperatures** and, optionally, the **heat input rate**. The calculator returns the Carnot efficiency, the maximum power output, and the ideal coefficients of performance for a refrigerator and a heat pump working between the same temperatures.

## Carnot efficiency formula

<p class="formula">η = 1 − T<sub>c</sub> ÷ T<sub>h</sub> &nbsp;·&nbsp; W = η × Q<sub>h</sub></p>

<p class="formula">COP<sub>ref</sub> = T<sub>c</sub> ÷ (T<sub>h</sub> − T<sub>c</sub>) &nbsp;·&nbsp; COP<sub>HP</sub> = T<sub>h</sub> ÷ (T<sub>h</sub> − T<sub>c</sub>)</p>

## Example

An engine takes 100 kW of heat at 500 °C (773.15 K) and rejects heat at 30 °C (303.15 K):

- η = 1 − 303.15 ÷ 773.15 = **{ca_eta*100:.2f}%**
- Maximum work = {ca_eta:.4f} × 100 = **{ca_eta*100:.2f} kW**
- Carnot COP as a refrigerator = 303.15 ÷ 470 = **{ca_COPr:.3f}**; as a heat pump = 773.15 ÷ 470 = **{ca_COPh:.3f}**

## Carnot efficiency with a 25 °C cold sink

| Hot temperature | Carnot efficiency |
|---|---|
{ca_rows}
## Ideal heat pump and refrigerator COP (delivering heat at 35 °C)

| Cold source | Hot side | Carnot COP (heating) | Carnot COP (cooling) |
|---|---|---|---|
{ca_hp}
## Notes

- Efficiency improves by raising T<sub>h</sub> or lowering T<sub>c</sub>; that is why gas turbines run hot and power plants want cold cooling water.
- A smaller temperature lift gives a much higher heat-pump COP, which is why underfloor heating (low flow temperature) suits heat pumps.
''')

# ================================================================ ENGINEERING — MECHANICAL DESIGN

# ---------------------------------------------------------------- Bolt torque
bt_K, bt_D, bt_F, bt_At = 0.2, 12.0, 30.0, 84.3
bt_T = bt_K * bt_D * 1e-3 * bt_F * 1e3
bt_s = bt_F * 1e3 / (bt_At * 1e-6) / 1e6
bolts = [('M6', 6, 1.0), ('M8', 8, 1.25), ('M10', 10, 1.5), ('M12', 12, 1.75), ('M16', 16, 2.0), ('M20', 20, 2.5), ('M24', 24, 3.0), ('M30', 30, 3.5)]
def At(d, p): return math.pi / 4 * (d - 0.9382 * p)**2
def sp88(d): return 580 if d <= 16 else 600
bt_rows = ''.join(f"| {nm} × {p:g} | {At(d,p):.1f} mm² | {0.75*sp88(d)*At(d,p)/1000:.1f} kN | {0.2*d*1e-3*0.75*sp88(d)*At(d,p):.0f} N·m | {0.75*830*At(d,p)/1000:.1f} kN | {0.2*d*1e-3*0.75*830*At(d,p):.0f} N·m |\n" for nm, d, p in bolts)
page('engineering', 'bolt-torque', f'''
title: Bolt Torque Calculator (T = K·D·F, Preload & Stress)
description: Calculate bolt tightening torque from preload, nominal diameter and nut factor with T = K·D·F, plus bolt stress — with an ISO metric 8.8 and 10.9 torque table.
category: engineering
intro: "Tightening torque is the practical way to set a bolt's clamping force, but only a small part of the torque stretches the bolt — most is lost to friction in the threads and under the nut. This bolt torque calculator uses the short-form equation T = K × D × F, with the nut factor K capturing that friction, and checks the resulting tensile stress in the bolt."
keywords: [bolt torque calculator, bolt tightening torque, torque to preload calculator, nut factor, t = kdf, bolt preload calculator, metric bolt torque chart]
updated: {D}
variables:
  - {{ id: K, label: Nut factor K, default: 0.2, min: 0, help: 'Dry steel ≈ 0.20 · zinc plated ≈ 0.20 · lightly oiled ≈ 0.15–0.18 · MoS₂ paste ≈ 0.10–0.12' }}
  - {{ id: d, label: Nominal bolt diameter, family: length, unit: mm, imperialUnit: in, default: 12, min: 0 }}
  - {{ id: F, label: Target preload (clamp force), family: force, unit: kN, imperialUnit: lbf, default: 30, min: 0 }}
  - {{ id: At, label: Tensile stress area, family: area, unit: mm2, imperialUnit: in2, default: 84.3, min: 0, help: 'M8 36.6 · M10 58.0 · M12 84.3 · M16 157 · M20 245 mm²' }}
  - {{ id: T, label: Tightening torque, family: torque, unit: Nm, imperialUnit: lbft, min: 0 }}
  - {{ id: s, label: Bolt tensile stress, family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
equations:
  - T = K * d * F
  - s = F / At
faq:
  - q: What is the formula for bolt torque?
    a: T = K × D × F, where K is the nut factor (about 0.2 for dry steel), D the nominal diameter and F the desired preload. Use metres and newtons to get N·m.
  - q: What preload should a bolt have?
    a: A common target is 70–75% of the bolt's proof load for reusable joints. For an ISO 8.8 bolt up to M16 the proof stress is 580 MPa, so 75% is about 435 MPa on the tensile stress area.
  - q: How much does lubrication change the torque?
    a: A lot. Oiled or MoS₂-coated threads have a lower K, so the same torque produces 30–60% more preload. Always use the K value matching the actual thread condition, or the bolt may be over-stressed.
  - q: Why is torque tightening imprecise?
    a: Friction varies from bolt to bolt, so the same torque can give ±25% scatter in preload. Critical joints use torque-angle tightening, hydraulic tensioners or ultrasonic bolt-elongation measurement.
related: [engineering/torque-power-speed, physics/torque, engineering/factor-of-safety, engineering/hydraulic-cylinder-force]
''', f'''
## How to use the bolt torque calculator

Enter the **nut factor K**, the **nominal bolt diameter**, the **target preload** and the bolt's **tensile stress area**. The calculator returns the tightening torque and the tensile stress the preload creates. To find the preload a given torque produces, enter the torque and clear the preload.

## Bolt torque formula

<p class="formula">T = K × D × F &nbsp;·&nbsp; σ = F ÷ A<sub>t</sub></p>

For ISO metric threads the tensile stress area is A<sub>t</sub> = π/4 × (d − 0.9382 p)², where p is the thread pitch.

## Example

An M12 × 1.75 bolt (A<sub>t</sub> = 84.3 mm²) tightened dry (K = 0.2) to a 30 kN preload:

- T = 0.2 × 0.012 m × 30,000 N = **{bt_T:.0f} N·m**
- Bolt stress σ = 30,000 ÷ 84.3 = **{bt_s:.0f} MPa** — about {bt_s/580*100:.0f}% of the 580 MPa proof stress of class 8.8

## Indicative torque for ISO metric coarse bolts (K = 0.2, 75% of proof load)

| Thread | Stress area | Preload 8.8 | Torque 8.8 | Preload 10.9 | Torque 10.9 |
|---|---|---|---|---|---|
{bt_rows}
Proof stresses from ISO 898-1: class 8.8 — 580 MPa (≤ M16), 600 MPa (> M16); class 10.9 — 830 MPa. Use the fastener supplier's data for critical joints.

## Notes

- Check the clamped joint as well as the bolt: soft gaskets and painted surfaces relax and lose preload.
- Use the [factor of safety calculator](/engineering/factor-of-safety/) to compare the bolt stress with the material's proof or yield strength.
''')

# ---------------------------------------------------------------- Shaft diameter for torque
sd_P, sd_N, sd_tau = 15.0, 1450.0, 40.0
sd_T = sd_P * 1e3 / (2 * math.pi * sd_N / 60)
sd_d = (16 * sd_T / (math.pi * sd_tau * 1e6)) ** (1/3)
def sdd(P, N, tau=40): T = P*1e3/(2*math.pi*N/60); return (16*T/(math.pi*tau*1e6))**(1/3)*1000
sd_rows = ''.join(f"| {P:g} kW | {P*1e3/(2*math.pi*1450/60):.1f} N·m | {sdd(P,1450):.1f} mm | {sdd(P,960):.1f} mm | {sdd(P,2900):.1f} mm |\n" for P in (0.75, 2.2, 5.5, 11, 15, 30, 55, 90, 160))
page('engineering', 'shaft-diameter', f'''
title: Shaft Diameter Calculator (Torsion, from Power & Speed)
description: Calculate the minimum diameter of a solid shaft to transmit a given power at a given speed without exceeding the allowable shear stress, τ = 16T/πd³.
category: engineering
intro: "A rotating shaft must carry its torque without the torsional shear stress at its surface exceeding a safe limit. This shaft diameter calculator converts power and speed into torque and then sizes a solid circular shaft from the torsion formula τ = 16T ÷ (πd³), using an allowable shear stress that already includes your safety margin."
keywords: [shaft diameter calculator, shaft size calculator, torsional shear stress calculator, shaft design calculator, solid shaft torque, tau = 16t / pi d^3, motor shaft diameter]
updated: {D}
variables:
  - {{ id: P, label: Power transmitted, family: power, unit: kW, imperialUnit: hp, default: 15, min: 0 }}
  - {{ id: N, label: Shaft speed, suffix: rpm, default: 1450, min: 0 }}
  - {{ id: tau, label: Allowable shear stress, family: pressure, unit: MPa, imperialUnit: psi, default: 40, min: 0, help: 'Commercial steel shafting with keyways ≈ 40 MPa (ASME guideline); higher for alloy steels without keyways.' }}
  - {{ id: T, label: Torque, family: torque, unit: Nm, imperialUnit: lbft, min: 0 }}
  - {{ id: d, label: Minimum shaft diameter, family: length, unit: mm, imperialUnit: in, min: 0 }}
equations:
  - T = P / (2 * pi * N / 60)
  - d = (16 * T / (pi * tau))^(1/3)
faq:
  - q: How do you calculate shaft diameter from torque?
    a: For a solid round shaft, d = ∛(16T ÷ (π τ)), where T is the torque and τ the allowable shear stress. Torque comes from power and speed, T = P ÷ (2πN/60).
  - q: What allowable shear stress should I use?
    a: The ASME shaft code suggests the lower of 18% of ultimate strength or 30% of yield, reduced by 25% for keyways. For commercial mild-steel shafting this gives about 40 MPa.
  - q: Does this account for bending?
    a: No. Shafts carrying pulleys, gears or overhung loads also bend. Then combine them with the equivalent torque √(M² + T²) in place of T, and apply shock factors for the load type.
  - q: How does speed affect shaft size?
    a: At the same power, torque is inversely proportional to speed, and diameter grows with the cube root of torque. Halving the speed increases the diameter by about 26%.
related: [engineering/torque-power-speed, physics/torque, engineering/bending-stress, engineering/gear-ratio]
''', f'''
## How to use the shaft diameter calculator

Enter the **power** to be transmitted, the **shaft speed** in rpm and the **allowable shear stress** for the shaft material. The calculator returns the torque and the minimum solid-shaft diameter; round up to the next standard size. To check an existing shaft, enter its diameter and clear the allowable stress to see the actual stress.

## Shaft diameter formula (torsion)

<p class="formula">T = P ÷ (2πN ÷ 60) &nbsp;·&nbsp; τ = 16 T ÷ (π d³) &nbsp;·&nbsp; d = ∛(16 T ÷ (π τ))</p>

## Example

A 15 kW motor running at 1,450 rpm, steel shaft with τ<sub>allow</sub> = 40 MPa:

- T = 15,000 ÷ (2π × 1450 ÷ 60) = **{sd_T:.2f} N·m**
- d = ∛(16 × {sd_T:.2f} ÷ (π × 40 × 10⁶)) = **{sd_d*1000:.1f} mm** → choose a 25 mm shaft

## Minimum shaft diameter at τ = 40 MPa

| Power | Torque at 1450 rpm | d at 1450 rpm | d at 960 rpm | d at 2900 rpm |
|---|---|---|---|---|
{sd_rows}
## Notes

- Keyways, shoulders and grooves concentrate stress; fatigue design for these features needs stress-concentration factors.
- Long shafts may be governed by twist rather than strength — a common limit is 0.25° per metre for machinery shafts.
- Check that a motor's shaft size matches its output torque using the [torque, power & speed calculator](/engineering/torque-power-speed/).
''')

# ---------------------------------------------------------------- Beam deflection (point load)
bd_P, bd_L, bd_E, bd_I = 5.0, 3.0, 200000.0, 1943.0
EI = bd_E * 1e6 * bd_I * 1e-8
bd_ss = bd_P * 1e3 * bd_L**3 / (48 * EI)
bd_c = bd_P * 1e3 * bd_L**3 / (3 * EI)
bd_rows = ''.join(f"| {L:g} m | {5e3*L**3/(48*EI)*1000:.2f} mm | L/{L/(5e3*L**3/(48*EI)):,.0f} | {5e3*L**3/(3*EI)*1000:.1f} mm | {5e3*L/4/1000:.2f} kN·m |\n" for L in (1, 1.5, 2, 2.5, 3, 4, 5, 6))
page('engineering', 'beam-deflection', f'''
title: Beam Deflection Calculator (Simply Supported & Cantilever)
description: Calculate the maximum deflection and bending moment of a simply supported beam with a central point load and a cantilever with an end load, from E and I.
category: engineering
{intro("How much a beam sags depends on the load, the cube of its span and its flexural stiffness E·I. This beam deflection calculator gives the maximum deflection and bending moment for the two most common cases — a simply supported beam with a central point load and a cantilever with a load at its tip — the same elastic bending that a [beam-type load cell](ib:load-cell-working-principle) uses to measure force.")}
keywords: [beam deflection calculator, simply supported beam deflection, cantilever beam deflection, point load deflection, pl^3/48ei, pl^3/3ei, steel beam deflection calculator]
updated: {D}
variables:
  - {{ id: P, label: Point load, family: force, unit: kN, imperialUnit: lbf, default: 5, min: 0 }}
  - {{ id: L, label: Span (length), family: length, unit: m, imperialUnit: ft, default: 3, min: 0 }}
  - {{ id: E, label: Young's modulus E, family: pressure, unit: MPa, imperialUnit: psi, default: 200000, min: 0, help: 'Steel 200,000–210,000 MPa · Aluminium 69,000 · Timber 8,000–12,000' }}
  - {{ id: I, label: Second moment of area I, suffix: cm⁴, default: 1943, min: 0, help: 'IPE 200 ≈ 1943 cm⁴ (strong axis). For a rectangle use b·h³/12.' }}
  - {{ id: dss, label: Deflection — simply supported, centre load, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: Mss, label: Max moment — simply supported, family: torque, unit: kNm, imperialUnit: lbft, min: 0 }}
  - {{ id: dc, label: Deflection — cantilever, end load, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: Mc, label: Max moment — cantilever, family: torque, unit: kNm, imperialUnit: lbft, min: 0 }}
equations:
  - dss = P * L^3 / (48 * E * I * 1e-8)
  - Mss = P * L / 4
  - dc = P * L^3 / (3 * E * I * 1e-8)
  - Mc = P * L
faq:
  - q: What is the deflection formula for a simply supported beam?
    a: With a point load P at mid-span, δ = PL³ ÷ (48EI). For a uniformly distributed load w per metre, δ = 5wL⁴ ÷ (384EI). Both occur at mid-span.
  - q: What is the deflection of a cantilever beam?
    a: With a point load P at the free end, δ = PL³ ÷ (3EI) — 16 times the simply supported value for the same span. With a uniform load w, δ = wL⁴ ÷ (8EI).
  - q: What deflection limit should a beam meet?
    a: Typical serviceability limits are span/360 for floors with brittle finishes, span/250 for general floors and span/180 for roofs. Check your design code.
  - q: What is EI?
    a: The flexural rigidity — Young's modulus of the material times the second moment of area of the cross-section. Doubling the depth of a rectangular beam increases I, and the stiffness, eightfold.
related: [engineering/bending-stress, engineering/area-moment-of-inertia, physics/youngs-modulus, engineering/factor-of-safety]
''', f'''
## How to use the beam deflection calculator

Enter the **point load**, the **span**, the material's **Young's modulus** and the section's **second moment of area I** in cm⁴ (from a steel table or the [area moment of inertia calculator](/engineering/area-moment-of-inertia/)). The calculator returns the maximum deflection and bending moment for a simply supported beam loaded at mid-span and for a cantilever loaded at its tip. Self-weight is not included.

## Beam deflection formulas

<p class="formula">Simply supported, centre load: δ = P L³ ÷ (48 E I) &nbsp;·&nbsp; M = P L ÷ 4</p>

<p class="formula">Cantilever, end load: δ = P L³ ÷ (3 E I) &nbsp;·&nbsp; M = P L</p>

## Example

A steel IPE 200 (I = 1,943 cm⁴, E = 200 GPa) spanning 3 m with a 5 kN load:

- EI = 200 × 10⁹ × 1,943 × 10⁻⁸ = {EI/1e6:.2f} × 10⁶ N·m²
- Simply supported: δ = 5,000 × 3³ ÷ (48 × {EI/1e6:.2f} × 10⁶) = **{bd_ss*1000:.2f} mm** (span/{bd_L/bd_ss:,.0f}); M = 5 × 3 ÷ 4 = **{bd_P*bd_L/4:.2f} kN·m**
- As a 3 m cantilever: δ = 5,000 × 3³ ÷ (3 × {EI/1e6:.2f} × 10⁶) = **{bd_c*1000:.1f} mm**; M = **{bd_P*bd_L:.0f} kN·m**

## Deflection of the example beam (5 kN) by span

| Span | Simply supported δ | Span/δ | Cantilever δ | Max moment (s.s.) |
|---|---|---|---|---|
{bd_rows}
## Other common load cases

| Case | Maximum deflection | Maximum moment |
|---|---|---|
| Simply supported, uniform load w | 5wL⁴ ÷ (384EI) | wL² ÷ 8 |
| Cantilever, uniform load w | wL⁴ ÷ (8EI) | wL² ÷ 2 |
| Fixed both ends, centre load P | PL³ ÷ (192EI) | PL ÷ 8 |

## Notes

- Check the bending stress as well as deflection — use the [bending stress calculator](/engineering/bending-stress/) with the moment from this page.
- These formulas assume small, elastic deflections of a straight, uniform beam.
''')

# ---------------------------------------------------------------- Bending stress
bs_M, bs_Z, bs_Sy = 15.0, 194.0, 250.0
bs_s = bs_M * 1e3 / (bs_Z * 1e-6) / 1e6
ipe = [('IPE 100', 34.2), ('IPE 120', 53.0), ('IPE 140', 77.3), ('IPE 160', 109), ('IPE 180', 146), ('IPE 200', 194), ('IPE 240', 324), ('IPE 300', 557)]
bs_rows = ''.join(f"| {nm} | {Z:g} cm³ | {Z*1e-6*250e6/1e3:.1f} kN·m | {Z*1e-6*250e6/1.5/1e3:.1f} kN·m |\n" for nm, Z in ipe)
page('engineering', 'bending-stress', f'''
title: Bending Stress Calculator (σ = M/Z = M·y/I)
description: Calculate the maximum bending stress in a beam from bending moment and section modulus, σ = M/Z, and compare it with yield strength for a factor of safety.
category: engineering
{intro("A bending moment stretches one face of a beam and compresses the other, with the stress greatest at the outer fibres. This bending stress calculator applies σ = M ÷ Z (equivalently M·y ÷ I) to find that peak stress and compares it with the material's yield strength — the surface strain it produces is what [strain gauges](ib:strain-gauge-working-principle) measure on loaded beams.")}
keywords: [bending stress calculator, flexural stress calculator, beam bending stress, section modulus stress, sigma = m/z, my/i calculator, maximum bending stress formula]
updated: {D}
variables:
  - {{ id: M, label: Bending moment, family: torque, unit: kNm, imperialUnit: lbft, default: 15, min: 0 }}
  - {{ id: Z, label: Elastic section modulus Z, suffix: cm³, default: 194, min: 0, help: 'Z = I ÷ y_max. IPE 200 ≈ 194 cm³; rectangle b·h²/6; solid round πd³/32.' }}
  - {{ id: Sy, label: Yield strength of the material, family: pressure, unit: MPa, imperialUnit: psi, default: 250, min: 0, help: 'S235 / A36 ≈ 235–250 MPa · S355 ≈ 355 MPa · 6061-T6 aluminium ≈ 240 MPa' }}
  - {{ id: s, label: Maximum bending stress, family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
  - {{ id: FoS, label: Factor of safety against yield, min: 0, decimals: 2 }}
equations:
  - s = M / (Z * 1e-6)
  - FoS = Sy / s
faq:
  - q: What is the bending stress formula?
    a: σ = M·y ÷ I = M ÷ Z, where M is the bending moment, y the distance from the neutral axis to the outer fibre, I the second moment of area and Z = I/y the elastic section modulus.
  - q: Where is bending stress highest?
    a: At the top and bottom surfaces, farthest from the neutral axis, at the section with the largest bending moment — mid-span of a simply supported beam, or the fixed end of a cantilever.
  - q: What is the difference between elastic and plastic section modulus?
    a: The elastic modulus Z gives the moment at which the outer fibre first yields. The plastic modulus (larger, by about 15% for I-beams and 50% for rectangles) gives the moment when the whole section has yielded; steel design codes use it for compact sections.
  - q: How do I get the bending moment?
    a: For a simply supported beam with a central load it is PL/4; with a uniform load wL²/8; for a cantilever with an end load PL. The beam deflection calculator gives these moments too.
related: [engineering/beam-deflection, engineering/area-moment-of-inertia, engineering/factor-of-safety, physics/youngs-modulus]
''', f'''
## How to use the bending stress calculator

Enter the **bending moment**, the section's **elastic section modulus Z** in cm³ and the material's **yield strength**. The calculator returns the maximum bending stress at the outer fibre and the factor of safety against yielding. To size a section, enter the stress you will allow and clear Z.

## Bending stress formula

<p class="formula">σ = M × y ÷ I = M ÷ Z &nbsp;·&nbsp; FoS = S<sub>y</sub> ÷ σ</p>

## Example

An IPE 200 (Z = 194 cm³) carrying a 15 kN·m moment, S235/A36-type steel with 250 MPa yield:

- σ = 15,000 N·m ÷ 194 × 10⁻⁶ m³ = **{bs_s:.1f} MPa**
- Factor of safety = 250 ÷ {bs_s:.1f} = **{bs_Sy/bs_s:.2f}**

## Moment capacity of IPE sections (S<sub>y</sub> = 250 MPa)

| Section | Z (strong axis) | Moment at first yield | With FoS 1.5 |
|---|---|---|---|
{bs_rows}
Section moduli are nominal values from European IPE tables.

## Notes

- Slender beams can fail by lateral-torsional buckling before reaching the yield stress; design codes reduce the capacity of unrestrained beams.
- Combine bending with axial or shear stresses (for example with the von Mises criterion) when both act together.
''')

# ---------------------------------------------------------------- Area moment of inertia
mi_b, mi_h, mi_D, mi_di = 100.0, 200.0, 60.0, 0.0
mi_Ir = mi_b * mi_h**3 / 12 / 1e4
mi_Zr = mi_b * mi_h**2 / 6 / 1e3
mi_Ic = math.pi * (mi_D**4 - mi_di**4) / 64 / 1e4
mi_Zc = mi_Ic * 1e4 / (mi_D / 2) / 1e3
pipes = [('25 NB (33.4 × 3.4)', 33.4, 3.38), ('50 NB (60.3 × 3.9)', 60.3, 3.91), ('80 NB (88.9 × 5.5)', 88.9, 5.49), ('100 NB (114.3 × 6.0)', 114.3, 6.02), ('150 NB (168.3 × 7.1)', 168.3, 7.11), ('200 NB (219.1 × 8.2)', 219.1, 8.18)]
def tube(D, t): di = D - 2*t; I = math.pi*(D**4-di**4)/64/1e4; return I, I*1e4/(D/2)/1e3
mi_rows = ''.join(f"| {nm} | {tube(D,t)[0]:,.1f} cm⁴ | {tube(D,t)[1]:,.2f} cm³ |\n" for nm, D, t in pipes)
mi_rrows = ''.join(f"| {b} × {h} mm | {b*h**3/12/1e4:,.1f} cm⁴ | {b*h**2/6/1e3:,.1f} cm³ | {h*b**3/12/1e4:,.1f} cm⁴ |\n" for b, h in ((50, 100), (50, 150), (75, 150), (100, 200), (100, 300), (150, 300)))
page('engineering', 'area-moment-of-inertia', f'''
title: Area Moment of Inertia Calculator (Rectangle, Circle, Tube)
description: Calculate the second moment of area I and section modulus Z of rectangular, solid round and hollow circular sections for beam deflection and bending stress.
category: engineering
intro: "The second moment of area I describes how a cross-section's material is spread around its bending axis, and it decides how stiff a beam is. This area moment of inertia calculator gives I and the elastic section modulus Z for a rectangle and for a solid or hollow circular section, in the cm⁴ and cm³ units used in steel tables."
keywords: [area moment of inertia calculator, second moment of area calculator, moment of inertia rectangle, moment of inertia circle, section modulus calculator, bh^3/12, hollow tube moment of inertia]
updated: {D}
variables:
  - {{ id: b, label: Rectangle width b, family: length, unit: mm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: h, label: Rectangle depth h (in the bending direction), family: length, unit: mm, imperialUnit: in, default: 200, min: 0 }}
  - {{ id: Do, label: Circle outer diameter D, family: length, unit: mm, imperialUnit: in, default: 60, min: 0 }}
  - {{ id: Di, label: Circle inner diameter d (0 = solid), family: length, unit: mm, imperialUnit: in, default: 0, min: 0 }}
  - {{ id: Ir, label: I — rectangle, suffix: cm⁴, min: 0 }}
  - {{ id: Zr, label: Z — rectangle, suffix: cm³, min: 0 }}
  - {{ id: Ic, label: I — circle / tube, suffix: cm⁴, min: 0 }}
  - {{ id: Zc, label: Z — circle / tube, suffix: cm³, min: 0 }}
equations:
  - Ir = b * h^3 / 12 * 1e8
  - Zr = b * h^2 / 6 * 1e6
  - Ic = pi * (Do^4 - Di^4) / 64 * 1e8
  - Zc = pi * (Do^4 - Di^4) / (32 * Do) * 1e6
faq:
  - q: What is the moment of inertia of a rectangle?
    a: I = b h³ ÷ 12 about the centroidal axis parallel to b, where h is the depth in the direction of bending. The section modulus is Z = b h² ÷ 6.
  - q: What is the moment of inertia of a circle and a tube?
    a: Solid circle I = π d⁴ ÷ 64; hollow tube I = π (D⁴ − d⁴) ÷ 64. The section modulus is I divided by the outer radius, Z = π (D⁴ − d⁴) ÷ (32 D).
  - q: Is area moment of inertia the same as mass moment of inertia?
    a: No. The area moment (m⁴) describes a cross-section's resistance to bending; the mass moment (kg·m²) describes a body's resistance to rotation. They share a name and the r² weighting but are used for different problems.
  - q: Why are I-beams so efficient?
    a: I grows with the square of the distance from the neutral axis, so putting most material in flanges far from the centre gives a high I and Z for little weight.
related: [engineering/beam-deflection, engineering/bending-stress, physics/rotational-kinetic-energy, physics/youngs-modulus]
''', f'''
## How to use the area moment of inertia calculator

For a **rectangle**, enter the width b and the depth h measured in the direction of bending. For a **round section**, enter the outer diameter and the inner diameter (0 for a solid bar). The calculator returns the second moment of area I in cm⁴ and the elastic section modulus Z in cm³ for both shapes — ready for the [beam deflection](/engineering/beam-deflection/) and [bending stress](/engineering/bending-stress/) calculators.

## Second moment of area formulas

<p class="formula">Rectangle: I = b h³ ÷ 12 &nbsp;·&nbsp; Z = b h² ÷ 6</p>

<p class="formula">Circle / tube: I = π (D⁴ − d⁴) ÷ 64 &nbsp;·&nbsp; Z = π (D⁴ − d⁴) ÷ (32 D)</p>

1 cm⁴ = 10⁻⁸ m⁴ and 1 cm³ = 10⁻⁶ m³.

## Example

A 100 × 200 mm timber beam bending about its strong axis, and a 60 mm solid steel bar:

- Rectangle: I = 100 × 200³ ÷ 12 = {mi_Ir*1e4:,.0f} mm⁴ = **{mi_Ir:,.1f} cm⁴**; Z = 100 × 200² ÷ 6 = **{mi_Zr:,.1f} cm³**
- Solid bar: I = π × 60⁴ ÷ 64 = **{mi_Ic:.2f} cm⁴**; Z = π × 60³ ÷ 32 = **{mi_Zc:.2f} cm³**

## Rectangular sections

| b × h | I (strong axis) | Z (strong axis) | I (weak axis) |
|---|---|---|---|
{mi_rrows}
## Steel pipe (Schedule 40) as a beam

| Pipe | I | Z |
|---|---|---|
{mi_rows}
## Notes

- Turning a rectangle on its side swaps b and h: a 100 × 200 mm plank is four times stiffer on edge than flat.
- For built-up shapes, add the I of each part about the common axis using the parallel-axis theorem, I = I<sub>c</sub> + A d².
''')

# ---------------------------------------------------------------- Spring rate (helical compression)
sr_d, sr_D, sr_n, sr_G, sr_F = 2.0, 20.0, 10.0, 79300.0, 20.0
sr_k = sr_G * 1e6 * (sr_d*1e-3)**4 / (8 * (sr_D*1e-3)**3 * sr_n)
sr_C = sr_D / sr_d
sr_Kw = (4*sr_C - 1) / (4*sr_C - 4) + 0.615 / sr_C
sr_tau = sr_Kw * 8 * sr_F * sr_D*1e-3 / (math.pi * (sr_d*1e-3)**3)
def kw(C): return (4*C-1)/(4*C-4)+0.615/C
sr_rows = ''.join(f"| {C:g} | {kw(C):.3f} |\n" for C in (4, 5, 6, 8, 10, 12, 14, 16))
sr_krows = ''.join(f"| {d:g} mm | {D:g} mm | {79.3e9*(d/1e3)**4/(8*(D/1e3)**3*10)/1000:.2f} N/mm |\n" for d, D in ((1, 10), (1.5, 12), (2, 16), (2, 20), (3, 25), (4, 32), (5, 40), (6, 50)))
page('engineering', 'spring-rate', f'''
title: Spring Rate Calculator (Helical Compression Spring)
description: Calculate helical compression spring rate from wire diameter, coil diameter, active coils and shear modulus, plus deflection and Wahl shear stress.
category: engineering
intro: "The stiffness of a coil spring comes from twisting its wire, so it depends strongly on the wire diameter and the coil diameter. This spring rate calculator uses k = G d⁴ ÷ (8 D³ n) for a helical compression or extension spring, then finds the deflection under a load and the corrected shear stress in the wire using the Wahl factor."
keywords: [spring rate calculator, spring constant calculator, compression spring calculator, helical spring stiffness, k = gd^4/8d^3n, wahl factor, spring stress calculator]
updated: {D}
variables:
  - {{ id: d, label: Wire diameter d, family: length, unit: mm, imperialUnit: in, default: 2, min: 0 }}
  - {{ id: D, label: Mean coil diameter D, family: length, unit: mm, imperialUnit: in, default: 20, min: 0, help: 'Mean diameter = outer diameter − wire diameter.' }}
  - {{ id: n, label: Number of active coils, default: 10, min: 0, help: 'Squared-and-ground ends: active coils ≈ total coils − 2.' }}
  - {{ id: G, label: Shear modulus G, family: pressure, unit: MPa, imperialUnit: psi, default: 79300, min: 0, help: 'Music wire / spring steel 79,300 MPa · Stainless 302 69,000 MPa · Phosphor bronze 41,000 MPa' }}
  - {{ id: F, label: Applied load, family: force, unit: N, imperialUnit: lbf, default: 20, min: 0 }}
  - {{ id: k, label: Spring rate, suffix: N/mm, min: 0, decimals: 3 }}
  - {{ id: x, label: Deflection under load, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: C, label: Spring index C = D/d, min: 0, decimals: 2 }}
  - {{ id: tau, label: Corrected shear stress (Wahl), family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
equations:
  - k = G * d^4 / (8 * D^3 * n) / 1000
  - x = F / (k * 1000)
  - C = D / d
  - tau = ((4 * C - 1) / (4 * C - 4) + 0.615 / C) * 8 * F * D / (pi * d^3)
faq:
  - q: What is the formula for spring rate?
    a: k = G d⁴ ÷ (8 D³ n), where G is the shear modulus of the wire, d the wire diameter, D the mean coil diameter and n the number of active coils.
  - q: How do wire and coil diameter affect stiffness?
    a: Stiffness rises with the fourth power of wire diameter and falls with the cube of coil diameter. A 10% thicker wire makes the spring 46% stiffer; a 10% larger coil makes it 25% softer.
  - q: What is the Wahl factor?
    a: A correction, K_w = (4C − 1)/(4C − 4) + 0.615/C, for the extra stress on the inside of the coil caused by wire curvature and direct shear. It matters most for tightly wound springs with a small index C.
  - q: What spring index is recommended?
    a: C = D/d between about 4 and 12. Below 4 the spring is hard to coil; above 12 it tends to buckle and tangle.
related: [physics/hookes-law, physics/spring-mass-frequency, engineering/factor-of-safety, physics/youngs-modulus]
''', f'''
## How to use the spring rate calculator

Enter the **wire diameter**, the **mean coil diameter**, the number of **active coils** and the wire material's **shear modulus**, plus a **load** to check. The calculator returns the spring rate in N/mm, the deflection under that load, the spring index and the Wahl-corrected shear stress in the wire. Compare the stress with the wire's allowable value (often 40–50% of its tensile strength for static loads).

## Spring rate formula

<p class="formula">k = G d⁴ ÷ (8 D³ n) &nbsp;·&nbsp; x = F ÷ k</p>

<p class="formula">τ = K<sub>w</sub> × 8 F D ÷ (π d³) &nbsp;·&nbsp; K<sub>w</sub> = (4C − 1) ÷ (4C − 4) + 0.615 ÷ C</p>

## Example

Music wire (G = 79.3 GPa), d = 2 mm, D = 20 mm, 10 active coils, loaded with 20 N:

- k = 79.3 × 10⁹ × 0.002⁴ ÷ (8 × 0.02³ × 10) = **{sr_k/1000:.3f} N/mm**
- Deflection = 20 ÷ {sr_k/1000:.3f} = **{sr_F/sr_k*1000:.2f} mm**
- Index C = 20 ÷ 2 = {sr_C:g}; Wahl factor K<sub>w</sub> = {sr_Kw:.4f}
- τ = {sr_Kw:.4f} × 8 × 20 × 0.02 ÷ (π × 0.002³) = **{sr_tau/1e6:.1f} MPa**

## Wahl correction factor

| Spring index C | K<sub>w</sub> |
|---|---|
{sr_rows}
## Spring rate for steel springs with 10 active coils

| Wire d | Mean coil D | Rate k |
|---|---|---|
{sr_krows}
## Notes

- Springs in series add like resistors in parallel (1/k = 1/k₁ + 1/k₂); springs in parallel add directly.
- The natural frequency of the spring with a mass on it follows from the [spring-mass frequency calculator](/physics/spring-mass-frequency/).
''')

# ---------------------------------------------------------------- Gear ratio
gr_z1, gr_z2, gr_N1, gr_T1, gr_eta = 20, 60, 1450.0, 50.0, 98.0
gr_i = gr_z2 / gr_z1
gr_N2 = gr_N1 / gr_i
gr_T2 = gr_T1 * gr_i * gr_eta / 100
gr_rows = ''.join(f"| {z1} : {z2} | {z2/z1:.3f} | {1450*z1/z2:.1f} rpm | {50*z2/z1*0.98:.1f} N·m |\n" for z1, z2 in ((20, 20), (20, 30), (18, 45), (20, 60), (17, 68), (15, 75), (12, 96)))
page('engineering', 'gear-ratio', f'''
title: Gear Ratio Calculator (Speed & Torque from Teeth)
description: Calculate gear ratio, output speed and output torque of a gear pair from the number of teeth, input speed, input torque and gear efficiency.
category: engineering
intro: "A gear pair trades speed for torque in proportion to its tooth counts: a small pinion driving a large gear slows the output and multiplies the torque. This gear ratio calculator gives the ratio, the output speed and the output torque after gear losses, for spur, helical and other parallel or bevel gear pairs."
keywords: [gear ratio calculator, gear speed calculator, gear torque calculator, number of teeth ratio, output rpm calculator, gear reduction calculator, driver driven gear]
updated: {D}
variables:
  - {{ id: z1, label: Teeth on the driving gear (pinion), default: 20, min: 1 }}
  - {{ id: z2, label: Teeth on the driven gear, default: 60, min: 1 }}
  - {{ id: N1, label: Input speed, suffix: rpm, default: 1450, min: 0 }}
  - {{ id: T1, label: Input torque, family: torque, unit: Nm, imperialUnit: lbft, default: 50, min: 0 }}
  - {{ id: eta, label: Gear efficiency, family: percent, unit: '%', default: 98, min: 0, max: 1, help: 'Spur / helical pair ≈ 97–99% · bevel ≈ 95–98% · worm 40–90%' }}
  - {{ id: i, label: Gear ratio (z₂ ÷ z₁), min: 0, decimals: 3 }}
  - {{ id: N2, label: Output speed, suffix: rpm, min: 0, decimals: 1 }}
  - {{ id: T2, label: Output torque, family: torque, unit: Nm, imperialUnit: lbft, min: 0 }}
equations:
  - i = z2 / z1
  - N2 = N1 / i
  - T2 = T1 * i * eta
faq:
  - q: How do you calculate gear ratio?
    a: Gear ratio = teeth on the driven gear ÷ teeth on the driving gear. A 20-tooth pinion driving a 60-tooth gear gives 3 : 1 — the output turns three times slower with three times the torque (less losses).
  - q: How do I find the output speed?
    a: N₂ = N₁ × z₁ ÷ z₂ = N₁ ÷ ratio. Speed and tooth count are inversely proportional because both gears move the same number of teeth past the mesh.
  - q: What is the ratio of a multi-stage gearbox?
    a: Multiply the ratios of each stage. Two stages of 3 : 1 and 4 : 1 give 12 : 1 overall; efficiencies also multiply (0.98 × 0.98 ≈ 0.96).
  - q: Does an idler gear change the ratio?
    a: No. An idler between two gears only reverses the direction of rotation; the ratio still depends only on the first and last gears.
related: [engineering/pulley-speed, engineering/torque-power-speed, engineering/shaft-diameter, sports/cycling-gear-speed]
''', f'''
## How to use the gear ratio calculator

Enter the **number of teeth** on the driving and driven gears, the **input speed**, the **input torque** and the **efficiency** of the gear mesh. The calculator returns the gear ratio, the output speed and the output torque. A ratio below 1 is a speed-up (overdrive) and reduces torque.

## Gear ratio formula

<p class="formula">i = z<sub>2</sub> ÷ z<sub>1</sub> &nbsp;·&nbsp; N<sub>2</sub> = N<sub>1</sub> ÷ i &nbsp;·&nbsp; T<sub>2</sub> = T<sub>1</sub> × i × η</p>

## Example

A 20-tooth pinion on a 1,450 rpm motor delivering 50 N·m drives a 60-tooth gear with 98% efficiency:

- Ratio i = 60 ÷ 20 = **{gr_i:g} : 1**
- Output speed = 1,450 ÷ 3 = **{gr_N2:.1f} rpm**
- Output torque = 50 × 3 × 0.98 = **{gr_T2:.0f} N·m**

## Gear pairs on a 1,450 rpm, 50 N·m input (98% efficiency)

| z₁ : z₂ | Ratio | Output speed | Output torque |
|---|---|---|---|
{gr_rows}
## Notes

- Use gear counts with no common factor (a "hunting tooth" ratio such as 17 : 68 → 17 : 69) to spread wear evenly across teeth.
- Belt and chain drives follow the same speed rule with pulley diameters or sprocket teeth — see the [pulley speed calculator](/engineering/pulley-speed/).
- Size the output shaft for the increased torque with the [shaft diameter calculator](/engineering/shaft-diameter/).
''')

# ---------------------------------------------------------------- Bearing L10 life
bl_C, bl_P, bl_N, bl_p = 32.5, 4.0, 1500.0, 3.0
bl_L = (bl_C / bl_P)**bl_p
bl_h = bl_L * 1e6 / (60 * bl_N)
bl_rows = ''.join(f"| {r:g} | {r**3:,.0f} | {r**3*1e6/(60*1500):,.0f} h | {r**(10/3):,.0f} | {r**(10/3)*1e6/(60*1500):,.0f} h |\n" for r in (2, 3, 4, 5, 6, 8, 10, 12))
page('engineering', 'bearing-life', f'''
title: Bearing Life Calculator (L10 Rating Life, Hours)
description: Calculate the basic L10 rating life of a ball or roller bearing in millions of revolutions and operating hours from dynamic load rating, load and speed.
category: engineering
intro: "Rolling bearings eventually fail by fatigue of the raceways, and their life is quoted statistically as L10 — the life that 90% of identical bearings will reach. This bearing life calculator applies the ISO 281 basic rating life equation L10 = (C ÷ P)^p and converts it into operating hours at the shaft speed."
keywords: [bearing life calculator, l10 bearing life calculator, bearing rating life, bearing life hours, iso 281 bearing life, l10 = (c/p)^3, ball bearing life calculator]
updated: {D}
variables:
  - id: p
    label: Bearing type (life exponent)
    default: 3
    options:
      - {{ label: 'Ball bearing (p = 3)', value: 3 }}
      - {{ label: 'Roller bearing (p = 10/3)', value: 3.333333 }}
  - {{ id: C, label: Basic dynamic load rating C, family: force, unit: kN, imperialUnit: lbf, default: 32.5, min: 0, help: 'From the bearing catalogue — for example about 32.5 kN for a 6208 deep-groove ball bearing.' }}
  - {{ id: P, label: Equivalent dynamic load P, family: force, unit: kN, imperialUnit: lbf, default: 4, min: 0 }}
  - {{ id: N, label: Rotational speed, suffix: rpm, default: 1500, min: 0 }}
  - {{ id: L10, label: Rating life L10, suffix: million rev, min: 0, decimals: 1 }}
  - {{ id: L10h, label: Rating life in hours L10h, family: seconds, unit: h, min: 0 }}
equations:
  - L10 = (C / P)^p
  - L10h = L10 * 1e6 / (60 * N) * 3600
faq:
  - q: What is L10 bearing life?
    a: The number of revolutions (or hours at constant speed) that 90% of a group of identical bearings will complete or exceed before the first sign of fatigue. Median (L50) life is roughly four to five times L10.
  - q: What is the bearing life formula?
    a: L10 = (C ÷ P)^p million revolutions, with p = 3 for ball bearings and 10/3 for roller bearings. In hours, L10h = 10⁶ ÷ (60 n) × L10, where n is the speed in rpm.
  - q: How does load affect bearing life?
    a: Very strongly. For a ball bearing, doubling the load cuts life to one-eighth; halving it raises life eightfold.
  - q: What life should I design for?
    a: Typical targets are 8,000–12,000 h for machines used intermittently, 20,000–30,000 h for 8-hour-a-day machinery, and 40,000–60,000 h or more for continuous 24-hour service such as pumps and fans.
related: [engineering/shaft-diameter, engineering/gear-ratio, engineering/availability-mtbf, engineering/torque-power-speed]
''', f'''
## How to use the bearing life calculator

Choose **ball** or **roller** bearing, then enter the **basic dynamic load rating C** from the catalogue, the **equivalent dynamic load P** acting on the bearing and the **speed**. The calculator returns the L10 life in millions of revolutions and in operating hours. To pick a bearing, enter the required hours and clear C to get the load rating you need.

## Bearing life formula (ISO 281)

<p class="formula">L<sub>10</sub> = (C ÷ P)<sup>p</sup> &nbsp;·&nbsp; L<sub>10h</sub> = 10⁶ ÷ (60 n) × L<sub>10</sub></p>

p = 3 for ball bearings, 10/3 for roller bearings. When both radial and axial loads act, P = X F<sub>r</sub> + Y F<sub>a</sub> with the X and Y factors from the catalogue.

## Example

A deep-groove ball bearing with C = 32.5 kN carries 4 kN at 1,500 rpm:

- L<sub>10</sub> = (32.5 ÷ 4)³ = **{bl_L:.1f} million revolutions**
- L<sub>10h</sub> = 10⁶ ÷ (60 × 1500) × {bl_L:.1f} = **{bl_h:,.0f} hours**

## Life versus load ratio at 1,500 rpm

| C/P | Ball L₁₀ (million rev) | Ball L₁₀h | Roller L₁₀ (million rev) | Roller L₁₀h |
|---|---|---|---|---|
{bl_rows}
## Notes

- Modern catalogues add a modified life L<sub>nm</sub> = a₁ a<sub>ISO</sub> L₁₀, which accounts for lubrication, contamination and the required reliability.
- Real bearings often fail early from poor lubrication, misalignment or contamination rather than fatigue. On inverter-fed motors, [shaft currents from VFDs](ib:vfd-motor-bearing-currents) can also damage the raceways.
''')

# ---------------------------------------------------------------- Factor of safety
fs_S, fs_s, fs_nr = 250.0, 100.0, 2.0
fs_n = fs_S / fs_s
mtl = [('Structural steel S235 / A36', 250), ('Structural steel S355', 355), ('Carbon steel AISI 1045 (cold drawn)', 530), ('Stainless 304 (annealed)', 215), ('Aluminium 6061-T6', 276), ('Aluminium 7075-T6', 503), ('Titanium Ti-6Al-4V', 880), ('Grey cast iron (ultimate tensile)', 200)]
fs_rows = ''.join(f"| {nm} | {S} MPa | {S/1.5:.0f} MPa | {S/2:.0f} MPa | {S/3:.0f} MPa |\n" for nm, S in mtl)
page('engineering', 'factor-of-safety', f'''
title: Factor of Safety Calculator (FoS & Margin of Safety)
description: Calculate the factor of safety and margin of safety from material strength and working stress or load — and the allowable stress for a required safety factor.
category: engineering
intro: "A factor of safety tells you how many times stronger a part is than it needs to be for the load it carries. This factor of safety calculator divides the material's strength by the actual working stress, gives the margin of safety, and works out the allowable stress for the safety factor your design code or company standard requires."
keywords: [factor of safety calculator, safety factor calculator, margin of safety calculator, allowable stress calculator, fos formula, design factor, yield strength safety factor]
updated: {D}
variables:
  - {{ id: S, label: Material strength (yield or ultimate), family: pressure, unit: MPa, imperialUnit: psi, default: 250, min: 0 }}
  - {{ id: s, label: Working (applied) stress, family: pressure, unit: MPa, imperialUnit: psi, default: 100, min: 0, help: 'You can also enter loads in the same unit for both fields — the ratio is the same.' }}
  - {{ id: nr, label: Required factor of safety, default: 2, min: 0 }}
  - {{ id: n, label: Factor of safety, min: 0, decimals: 2 }}
  - {{ id: MS, label: Margin of safety, family: percent, unit: '%' }}
  - {{ id: sa, label: Allowable stress for required FoS, family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
equations:
  - n = S / s
  - MS = S / s - 1
  - sa = S / nr
faq:
  - q: How do you calculate factor of safety?
    a: FoS = strength ÷ applied stress (or failure load ÷ working load). A bracket with 250 MPa yield strength stressed to 100 MPa has a factor of safety of 2.5.
  - q: What is the difference between factor of safety and margin of safety?
    a: Margin of safety = FoS − 1. A factor of safety of 2.5 is a margin of 1.5 (150%). Aerospace work often quotes the margin, where any positive value passes.
  - q: What factor of safety should I use?
    a: Typical values are 1.25–1.5 for well-known loads and materials (aircraft structures), 2–3 for general machine design, 3–4 for uncertain loads or brittle materials, and higher for lifting equipment and pressure parts as set by codes.
  - q: Should I use yield or ultimate strength?
    a: Use yield strength for ductile metals where permanent deformation counts as failure, and ultimate strength for brittle materials such as cast iron or ceramics. State which one you used.
related: [engineering/bending-stress, physics/youngs-modulus, engineering/bolt-torque, engineering/weld-size]
''', f'''
## How to use the factor of safety calculator

Enter the **material strength** (yield strength for ductile metals, ultimate strength for brittle ones) and the **working stress** in the part. The calculator returns the factor of safety and the margin of safety. Enter the **required factor of safety** to get the allowable working stress for design.

## Factor of safety formula

<p class="formula">FoS = S ÷ σ<sub>working</sub> &nbsp;·&nbsp; MS = FoS − 1 &nbsp;·&nbsp; σ<sub>allow</sub> = S ÷ FoS<sub>required</sub></p>

## Example

A steel part with 250 MPa yield strength is stressed to 100 MPa; the design standard asks for FoS = 2:

- FoS = 250 ÷ 100 = **{fs_n:.2f}**
- Margin of safety = {fs_n:.2f} − 1 = **{(fs_n-1)*100:.0f}%**
- Allowable stress at FoS 2 = 250 ÷ 2 = **{fs_S/fs_nr:.0f} MPa** — the part passes

## Allowable stress for common materials

| Material | Strength used | FoS 1.5 | FoS 2 | FoS 3 |
|---|---|---|---|---|
{fs_rows}
Strengths are typical minimum values; use the certified values for your material grade and thickness.

## Notes

- For fatigue (fluctuating) loading, compare the stress amplitude with the endurance limit, not the static strength.
- Find working stresses with the [bending stress](/engineering/bending-stress/), [bolt torque](/engineering/bolt-torque/) or [weld size](/engineering/weld-size/) calculators.
''')

# ---------------------------------------------------------------- Fillet weld size
ws_s, ws_L, ws_F, ws_ta = 6.0, 100.0, 50.0, 145.0
ws_a = 0.70710678 * ws_s
ws_tau = ws_F * 1e3 / (ws_a * 1e-3 * ws_L * 1e-3) / 1e6
ws_Fm = ws_ta * 1e6 * ws_a * 1e-3 * ws_L * 1e-3 / 1e3
ws_rows = ''.join(f"| {s} mm | {0.70710678*s:.2f} mm | {145*0.70710678*s/1000:.3f} kN/mm | {145*0.70710678*s*100/1000:.1f} kN |\n" for s in (3, 4, 5, 6, 8, 10, 12, 16))
page('engineering', 'weld-size', f'''
title: Fillet Weld Size Calculator (Throat, Stress & Capacity)
description: Calculate fillet weld throat thickness, shear stress and load capacity from leg size, weld length and allowable stress — a = 0.707 × leg size.
category: engineering
intro: "A fillet weld transfers load through its throat, the shortest distance from the root to the weld face, which for an equal-leg weld is 0.707 times the leg size. This fillet weld size calculator finds the throat, the shear stress for a given load and weld length, and the load the weld can safely carry at an allowable stress."
keywords: [fillet weld size calculator, weld strength calculator, fillet weld throat thickness, weld capacity calculator, weld stress calculator, 0.707 leg size, aws fillet weld strength]
updated: {D}
variables:
  - {{ id: s, label: Fillet leg size, family: length, unit: mm, imperialUnit: in, default: 6, min: 0 }}
  - {{ id: L, label: Effective weld length, family: length, unit: mm, imperialUnit: in, default: 100, min: 0, help: 'Total length of weld carrying the load, excluding start and end craters.' }}
  - {{ id: F, label: Applied load, family: force, unit: kN, imperialUnit: lbf, default: 50, min: 0 }}
  - {{ id: ta, label: Allowable shear stress on the throat, family: pressure, unit: MPa, imperialUnit: psi, default: 145, min: 0, help: 'AWS D1.1: 0.30 × electrode strength — E70 / E7018 ≈ 145 MPa (21 ksi).' }}
  - {{ id: a, label: Throat thickness, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: tau, label: Shear stress on the throat, family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
  - {{ id: Fmax, label: Weld load capacity, family: force, unit: kN, imperialUnit: lbf, min: 0 }}
  - {{ id: u, label: Utilisation, family: percent, unit: '%', min: 0 }}
equations:
  - a = 0.70710678 * s
  - tau = F / (a * L)
  - Fmax = ta * a * L
  - u = tau / ta
faq:
  - q: How do you calculate fillet weld strength?
    a: Capacity = allowable shear stress × throat × length, with throat a = 0.707 × leg size for an equal-leg 45° fillet. A 6 mm fillet 100 mm long at 145 MPa carries about 61.5 kN.
  - q: Why is the throat 0.707 times the leg?
    a: The throat of a right-angled isosceles triangle is the leg times sin 45° = 0.7071. It is the smallest section through the weld, so the stress is calculated there.
  - q: What allowable stress should I use for fillet welds?
    a: AWS D1.1 allows 0.30 × the electrode's tensile strength on the effective throat — about 145 MPa (21 ksi) for E70XX electrodes. Eurocode 3 uses a directional or simplified method based on the parent metal's strength.
  - q: Is there a minimum fillet weld size?
    a: Yes. Codes set minimum leg sizes based on the thicker plate (in AWS D1.1: 3 mm up to 6 mm plate, 5 mm for 6–12 mm, 6 mm for 12–20 mm and 8 mm above) so the weld cools slowly enough to fuse properly, and a maximum leg along plate edges.
related: [engineering/factor-of-safety, engineering/bending-stress, engineering/bolt-torque, physics/youngs-modulus]
''', f'''
## How to use the fillet weld size calculator

Enter the **leg size**, the **effective weld length**, the **load** and the **allowable shear stress** on the throat. The calculator returns the throat thickness, the actual stress, the weld's load capacity and its utilisation (below 100% passes). Clear the leg size and enter the load to find the fillet size you need.

## Fillet weld formula

<p class="formula">a = 0.707 × s &nbsp;·&nbsp; τ = F ÷ (a × L) &nbsp;·&nbsp; F<sub>max</sub> = τ<sub>allow</sub> × a × L</p>

## Example

A 6 mm fillet, 100 mm long, made with E70 electrodes (τ<sub>allow</sub> = 145 MPa), carries 50 kN:

- Throat a = 0.707 × 6 = **{ws_a:.2f} mm**
- Stress τ = 50,000 ÷ ({ws_a:.2f} × 100) = **{ws_tau:.1f} MPa**
- Capacity = 145 × {ws_a:.2f} × 100 = **{ws_Fm:.1f} kN**; utilisation {ws_tau/ws_ta*100:.0f}% — OK

## Fillet weld capacity at 145 MPa (E70 electrode)

| Leg size | Throat | Capacity per mm of weld | Capacity of 100 mm |
|---|---|---|---|
{ws_rows}
## Notes

- This simplified method treats the load as shear on the throat in any direction; it is conservative for welds loaded transversely.
- The parent metal next to the weld must also be checked.
- Compare the weld stress with your required [factor of safety](/engineering/factor-of-safety/).
''')

# ================================================================ STATISTICS

# ---------------------------------------------------------------- Bayes' theorem
by_pA, by_pBA, by_pBnA = 0.01, 0.95, 0.05
by_pB = by_pBA * by_pA + by_pBnA * (1 - by_pA)
by_pAB = by_pBA * by_pA / by_pB
by_pAnB = (1 - by_pBA) * by_pA / (1 - by_pB)
by_rows = ''.join(f"| {p*100:g}% | {0.95*p/(0.95*p+0.05*(1-p))*100:.1f}% | {0.99*p/(0.99*p+0.01*(1-p))*100:.1f}% |\n" for p in (0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5))
page('statistics', 'bayes-theorem', f'''
title: Bayes' Theorem Calculator (Posterior Probability)
description: Calculate the posterior probability P(A|B) with Bayes' theorem from a prior, the true-positive rate and the false-positive rate, for tests and alarms.
category: statistics
intro: "Bayes' theorem updates a prior belief with new evidence: it turns the probability of a positive test given a condition into the probability of the condition given a positive test. This Bayes' theorem calculator works from the prior probability, the true-positive rate and the false-positive rate, and shows why rare events give many false alarms."
keywords: [bayes theorem calculator, bayes calculator, posterior probability calculator, conditional probability calculator, p(a|b), false positive paradox, bayes rule]
updated: {D}
variables:
  - {{ id: pA, label: Prior probability P(A), family: percent, unit: '%', default: 1, min: 0, max: 1, help: 'How common A is before the evidence — for example the prevalence of a condition.' }}
  - {{ id: pBA, label: P(B | A) — true-positive rate, family: percent, unit: '%', default: 95, min: 0, max: 1, help: 'Sensitivity: chance of the evidence when A is true.' }}
  - {{ id: pBnA, label: P(B | not A) — false-positive rate, family: percent, unit: '%', default: 5, min: 0, max: 1, help: '1 − specificity: chance of the evidence when A is false.' }}
  - {{ id: pB, label: Total probability of the evidence P(B), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: pAB, label: Posterior P(A | B), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: pAnB, label: P(A | not B), family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - pB = pBA * pA + pBnA * (1 - pA)
  - pAB = pBA * pA / pB
  - pAnB = (1 - pBA) * pA / (1 - pB)
faq:
  - q: What is Bayes' theorem?
    a: P(A|B) = P(B|A) × P(A) ÷ P(B), where P(B) = P(B|A)P(A) + P(B|not A)(1 − P(A)). It gives the probability of A after observing B.
  - q: Why is a positive result from a 95% accurate test often wrong?
    a: When the condition is rare, false positives from the large healthy group outnumber the true positives. With 1% prevalence and a 5% false-positive rate, only about 16% of positives are real.
  - q: What are prior and posterior probabilities?
    a: The prior P(A) is what you believe before the evidence; the posterior P(A|B) is the updated probability after it. Today's posterior can be the prior for the next test.
  - q: What is P(A | not B)?
    a: The chance that A is true even though the evidence was negative — the false-negative risk. It depends on the sensitivity and the prior.
related: [statistics/probability, statistics/relative-risk, statistics/odds-probability, statistics/binomial-probability]
''', f'''
## How to use the Bayes' theorem calculator

Enter the **prior probability** of A, the probability of the evidence B when A is true (**true-positive rate** or sensitivity) and when A is false (**false-positive rate**, 1 − specificity). The calculator returns the overall probability of seeing B, the posterior probability of A given B, and the probability of A despite a negative result.

## Bayes' theorem formula

<p class="formula">P(A|B) = P(B|A) × P(A) ÷ P(B)</p>

<p class="formula">P(B) = P(B|A) × P(A) + P(B|¬A) × (1 − P(A))</p>

## Example

A condition affects 1% of people. A test detects it 95% of the time and gives a false positive 5% of the time:

- P(B) = 0.95 × 0.01 + 0.05 × 0.99 = **{by_pB*100:.2f}%**
- P(A|B) = 0.95 × 0.01 ÷ {by_pB:.4f} = **{by_pAB*100:.2f}%**
- P(A|not B) = 0.05 × 0.01 ÷ {1-by_pB:.4f} = **{by_pAnB*100:.4f}%**

Out of 10,000 people: 95 true positives and 495 false positives — so only about 1 in 6 positives has the condition.

## Posterior probability after one positive result

| Prior P(A) | Test 95% / 5% | Test 99% / 1% |
|---|---|---|
{by_rows}
## Notes

- A second, independent positive test uses the first posterior as the new prior and raises the probability sharply.
- The same reasoning applies to alarm systems: a sensitive alarm for a rare fault produces mostly nuisance trips.
''')

# ---------------------------------------------------------------- Exponential distribution
ex_l, ex_x = 0.5, 3.0
ex_cdf = 1 - math.exp(-ex_l * ex_x)
ex_pdf = ex_l * math.exp(-ex_l * ex_x)
ex_rows = ''.join(f"| {k:g} × mean | {(1-math.exp(-k))*100:.2f}% | {math.exp(-k)*100:.2f}% |\n" for k in (0.1, 0.25, 0.5, math.log(2), 1, 2, 3, 4, 5))
page('statistics', 'exponential-distribution', f'''
title: Exponential Distribution Calculator (CDF, PDF, Mean)
description: Calculate exponential distribution probabilities P(X ≤ x) and P(X > x), the density, mean and median from the rate λ — for waiting times and failure times.
category: statistics
intro: "The exponential distribution models the time between random, independent events that happen at a constant average rate — calls arriving, radioactive decays or component failures. This exponential distribution calculator gives the probability that the waiting time is shorter or longer than x, the probability density, the mean and the median."
keywords: [exponential distribution calculator, exponential cdf calculator, exponential probability calculator, waiting time probability, 1 - e^(-lambda x), exponential pdf, memoryless distribution]
updated: {D}
variables:
  - {{ id: lam, label: Rate λ (events per unit time), default: 0.5, min: 0, help: 'Mean time between events = 1/λ.' }}
  - {{ id: x, label: Time or value x, default: 3, min: 0 }}
  - {{ id: Pl, label: P(X ≤ x), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: Pg, label: P(X > x), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: f, label: Probability density f(x), min: 0, decimals: 5 }}
  - {{ id: mu, label: Mean (and standard deviation), min: 0, decimals: 4 }}
  - {{ id: med, label: Median, min: 0, decimals: 4 }}
equations:
  - Pl = 1 - exp(-lam * x)
  - Pg = exp(-lam * x)
  - f = lam * exp(-lam * x)
  - mu = 1 / lam
  - med = ln(2) / lam
faq:
  - q: What is the exponential distribution formula?
    a: The density is f(x) = λe^(−λx) for x ≥ 0, and the cumulative probability is P(X ≤ x) = 1 − e^(−λx). The mean and standard deviation are both 1/λ.
  - q: What does memoryless mean?
    a: The chance of waiting another t units does not depend on how long you have already waited. P(X > s + t | X > s) = P(X > t). It is the only continuous distribution with this property.
  - q: How is it related to the Poisson distribution?
    a: If events occur as a Poisson process with rate λ, the number in a fixed time is Poisson and the time between events is exponential with the same λ.
  - q: How is it used in reliability?
    a: With a constant failure rate λ, reliability over time t is R(t) = e^(−λt) and the MTBF is 1/λ. After one MTBF only about 36.8% of units are still working.
related: [statistics/poisson-probability, statistics/normal-distribution, engineering/availability-mtbf, physics/radioactive-activity]
''', f'''
## How to use the exponential distribution calculator

Enter the **rate λ** — the average number of events per unit of time — and the value **x** in the same time unit. The calculator returns the probability that the waiting time is at most x and more than x, the density at x, and the mean and median. To find the time by which a given share of events has happened, enter P(X ≤ x) and clear x.

## Exponential distribution formulas

<p class="formula">P(X ≤ x) = 1 − e<sup>−λx</sup> &nbsp;·&nbsp; P(X &gt; x) = e<sup>−λx</sup> &nbsp;·&nbsp; f(x) = λ e<sup>−λx</sup></p>

<p class="formula">Mean = 1 ÷ λ &nbsp;·&nbsp; Median = ln 2 ÷ λ</p>

## Example

Customers arrive at an average rate of 0.5 per minute. The chance that the next one arrives within 3 minutes:

- P(X ≤ 3) = 1 − e<sup>−0.5 × 3</sup> = **{ex_cdf*100:.2f}%**
- P(X > 3) = **{(1-ex_cdf)*100:.2f}%**
- Density f(3) = 0.5 × e<sup>−1.5</sup> = **{ex_pdf:.5f}**
- Mean wait = **{1/ex_l:g} min**; median = ln 2 ÷ 0.5 = **{math.log(2)/ex_l:.4f} min**

## Probabilities in multiples of the mean

| x | P(X ≤ x) | P(X > x) |
|---|---|---|
{ex_rows}
(0.693 × mean is the median.)

## Notes

- The exponential model fits the flat "useful life" part of the reliability bathtub curve, not early failures or wear-out; use the Weibull distribution for those.
- Radioactive decay follows the same law, with λ the decay constant — see the [radioactive activity calculator](/physics/radioactive-activity/).
''')

if __name__ == '__main__':
    print('ok')
