import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
D = '2026-10-30'
G = 9.80665
H = 6.62607015e-34      # Planck constant, J·s
C0 = 299792458.0        # speed of light, m/s
QE = 1.602176634e-19    # elementary charge, C
NA = 6.02214076e23      # Avogadro constant, 1/mol
FARADAY = 96485.33212   # C/mol
RGAS = 8.314462618      # J/(mol·K)
ME = 9.1093837015e-31   # electron mass, kg
MP = 1.67262192369e-27  # proton mass, kg
MN = 1.67492749804e-27  # neutron mass, kg

SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
def sci(x, d=3):
    m, e = f"{x:.{d}e}".split('e')
    return f"{m} × 10{str(int(e)).translate(SUP)}"

# ================================================================ PHYSICS

# ---------------------------------------------------------------- Simple harmonic motion
shm_A, shm_f, shm_t = 0.1, 2.0, 0.1
shm_w = 2 * math.pi * shm_f
shm_ph = shm_w * shm_t
shm_x = shm_A * math.cos(shm_ph); shm_v = -shm_A * shm_w * math.sin(shm_ph); shm_a = -shm_w**2 * shm_x
shm_rows = ''.join(f"| {fr:g} T | {math.degrees(2*math.pi*fr):.0f}° | {math.cos(2*math.pi*fr):+.3f} A | {-math.sin(2*math.pi*fr):+.3f} Aω | {-math.cos(2*math.pi*fr):+.3f} Aω² |\n"
                   for fr in (0, 0.125, 0.25, 0.375, 0.5, 0.75, 1))
shm_rows = shm_rows.replace('+0.000', '0').replace('-0.000', '0')
page('physics', 'simple-harmonic-motion', f'''
title: Simple Harmonic Motion Calculator (SHM x, v and a)
description: Calculate displacement, velocity and acceleration in simple harmonic motion at any time from amplitude, frequency and phase — plus period and peak values.
category: physics
intro: "Simple harmonic motion is the back-and-forth motion of a spring, pendulum or vibrating machine, where the restoring force is proportional to displacement. This simple harmonic motion calculator gives the displacement, velocity and acceleration at any instant, along with the period, angular frequency and peak values."
keywords: [simple harmonic motion calculator, shm calculator, shm displacement velocity acceleration, x = a cos wt, angular frequency, maximum velocity shm, oscillation calculator]
updated: {D}
variables:
  - {{ id: A, label: Amplitude, family: length, unit: m, imperialUnit: in, default: 0.1, min: 0 }}
  - {{ id: f, label: Frequency, family: frequency, unit: Hz, default: 2, min: 0 }}
  - {{ id: t, label: Time, family: seconds, unit: s, default: 0.1, min: 0 }}
  - {{ id: ph, label: Phase angle at t = 0, family: angle, unit: deg, default: 0 }}
  - {{ id: w, label: Angular frequency (ω), suffix: rad/s, min: 0 }}
  - {{ id: T, label: Period, family: seconds, unit: s, min: 0 }}
  - {{ id: x, label: Displacement x(t), family: length, unit: m, imperialUnit: in }}
  - {{ id: v, label: Velocity v(t), family: velocity, unit: ms }}
  - {{ id: a, label: Acceleration a(t), suffix: m/s² }}
  - {{ id: vm, label: Maximum velocity, family: velocity, unit: ms, min: 0 }}
  - {{ id: am, label: Maximum acceleration, suffix: m/s², min: 0 }}
equations:
  - w = 2 * pi * f
  - T = 1 / f
  - x = A * cos(w * t + ph)
  - v = -A * w * sin(w * t + ph)
  - a = -(w^2) * x
  - vm = A * w
  - am = A * w^2
faq:
  - q: What are the equations of simple harmonic motion?
    a: x = A cos(ωt + φ), v = −Aω sin(ωt + φ) and a = −ω² x, where A is the amplitude, ω = 2πf the angular frequency and φ the phase angle.
  - q: Where is velocity maximum in SHM?
    a: At the equilibrium position (x = 0), where the speed is Aω. At the turning points (x = ±A) the velocity is zero and the acceleration reaches its maximum, Aω².
  - q: Does the period depend on amplitude?
    a: Not for ideal simple harmonic motion. The period depends only on the system — √(m/k) for a spring, √(L/g) for a small-angle pendulum — which is why SHM is used for clocks.
  - q: What phase angle should I use?
    a: Use 0° if the motion starts at maximum displacement (released from rest at +A) and −90° if it starts at the centre moving in the positive direction.
related: [physics/spring-mass-frequency, physics/pendulum, physics/hookes-law, physics/wavelength-frequency]
''', f'''
## How to use the simple harmonic motion calculator

Enter the **amplitude** (maximum displacement), the **frequency** of oscillation, the **time** at which you want the state and the **phase angle** at t = 0. The calculator returns the angular frequency, period, the displacement, velocity and acceleration at that instant, and the maximum velocity and acceleration. Negative values mean the object is on, or moving towards, the negative side of equilibrium.

## Simple harmonic motion formulas

<p class="formula">x = A cos(ωt + φ) &nbsp;·&nbsp; v = −Aω sin(ωt + φ) &nbsp;·&nbsp; a = −ω² x</p>

<p class="formula">ω = 2πf &nbsp;·&nbsp; T = 1 ÷ f &nbsp;·&nbsp; v<sub>max</sub> = Aω &nbsp;·&nbsp; a<sub>max</sub> = Aω²</p>

## Example

A mass oscillates with amplitude 0.1 m at 2 Hz, starting from +A (φ = 0). At t = 0.1 s:

- ω = 2π × 2 = **{shm_w:.4f} rad/s**, T = **{1/shm_f:g} s**
- ωt = {shm_ph:.4f} rad ({math.degrees(shm_ph):.0f}°)
- x = 0.1 × cos 72° = **{shm_x:.4f} m**
- v = −0.1 × {shm_w:.3f} × sin 72° = **{shm_v:.4f} m/s**
- a = −{shm_w**2:.2f} × {shm_x:.4f} = **{shm_a:.3f} m/s²**
- v<sub>max</sub> = **{shm_A*shm_w:.4f} m/s**, a<sub>max</sub> = **{shm_A*shm_w**2:.2f} m/s²**

## Position, velocity and acceleration over one cycle (φ = 0)

| Time | Phase | Displacement | Velocity | Acceleration |
|---|---|---|---|---|
{shm_rows}
## Notes

- Velocity leads displacement by 90° and acceleration is always opposite to displacement — the signature of SHM.
- Total energy stays constant: ½ k A² = ½ m v<sub>max</sub>².
- Real oscillators lose energy to damping, so the amplitude decays with time while the frequency stays almost the same.
- To get the frequency of a spring or pendulum first, use the [spring-mass frequency](/physics/spring-mass-frequency/) or [pendulum](/physics/pendulum/) calculators.
''')

# ---------------------------------------------------------------- Young's modulus (stress & strain)
ym_F, ym_d, ym_L, ym_dL = 10000.0, 0.010, 2.0, 1.25e-3
ym_A = math.pi * ym_d**2 / 4
ym_s = ym_F / ym_A; ym_e = ym_dL / ym_L; ym_E = ym_s / ym_e
mats = [('Structural steel', 200), ('Stainless steel', 193), ('Cast iron', 110), ('Aluminium alloy', 69), ('Copper', 117),
        ('Brass', 100), ('Titanium alloy', 114), ('Concrete', 30), ('Glass', 70), ('Wood (along grain)', 11), ('Nylon', 3), ('Rubber', 0.05)]
ym_rows = ''.join(f"| {nm} | {E:g} GPa | {100e6/(E*1e9)*1e6:,.0f} µε | {100e6/(E*1e9)*1000:.3g} mm |\n" for nm, E in mats)
page('physics', 'youngs-modulus', f'''
title: Young's Modulus Calculator (Stress, Strain & Elongation)
description: Calculate stress, strain and Young's modulus from force, cross-section, original length and extension — or find the elongation of a bar under load.
category: physics
{intro("Young's modulus measures how stiff a material is in tension or compression: the ratio of stress to strain in the elastic range. This Young's modulus calculator works out stress, strain, modulus and extension for a rod, wire or bar — the same relationship a [strain gauge](ib:strain-gauge-working-principle) uses to turn tiny deformations into force or pressure readings.")}
keywords: [youngs modulus calculator, stress strain calculator, modulus of elasticity, elongation calculator, tensile stress formula, strain formula, e = stress / strain]
updated: {D}
variables:
  - {{ id: F, label: Axial force, family: force, unit: kN, imperialUnit: lbf, default: 10 }}
  - {{ id: A, label: Cross-sectional area, family: area, unit: mm2, imperialUnit: in2, default: {ym_A*1e6:.4f}, min: 0, help: 'A 10 mm diameter rod has an area of 78.54 mm².' }}
  - {{ id: L0, label: Original length, family: length, unit: m, imperialUnit: ft, default: 2, min: 0 }}
  - {{ id: dL, label: Extension (change in length), family: length, unit: mm, imperialUnit: in, default: 1.25 }}
  - {{ id: s, label: Stress (σ), family: pressure, unit: MPa, imperialUnit: psi }}
  - {{ id: ep, label: Strain (ε) }}
  - {{ id: E, label: Young's modulus (E), family: pressure, unit: MPa, imperialUnit: psi, min: 0 }}
  - {{ id: EG, label: Young's modulus in GPa, suffix: GPa, min: 0 }}
equations:
  - s = F / A
  - ep = dL / L0
  - E = s / ep
  - EG = E / 1e9
faq:
  - q: How do you calculate Young's modulus?
    a: E = stress ÷ strain = (F ÷ A) ÷ (ΔL ÷ L₀). A 10 kN load on a 10 mm steel rod 2 m long that stretches 1.25 mm gives about 204 GPa.
  - q: How do I find the elongation of a bar?
    a: ΔL = F L₀ ÷ (A E). Enter the force, area, length and the material's modulus, and clear the extension field.
  - q: What is the difference between stress and strain?
    a: Stress is force per unit area (Pa or MPa). Strain is the fractional change in length (dimensionless, often quoted in microstrain, µε = 10⁻⁶).
  - q: When is Young's modulus valid?
    a: Only in the linear elastic region — below the proportional limit, roughly below the yield strength. Beyond that, strain grows faster than stress and the deformation becomes permanent.
related: [physics/hookes-law, electronics/strain-gauge, engineering/thermal-expansion, physics/force]
''', f'''
## How to use the Young's modulus calculator

Enter the **axial force**, the **cross-sectional area** of the specimen, its **original length** and the measured **extension**. The calculator gives the stress, strain and Young's modulus in MPa and GPa. To predict the extension instead, enter the modulus of the material (for example 200,000 MPa for steel) and clear the extension field. Use a negative force and extension for compression.

## Stress, strain and Young's modulus formulas

<p class="formula">σ = F ÷ A &nbsp;·&nbsp; ε = ΔL ÷ L<sub>0</sub> &nbsp;·&nbsp; E = σ ÷ ε</p>

<p class="formula">ΔL = F L<sub>0</sub> ÷ (A E)</p>

## Example

A 10 mm diameter steel rod, 2 m long, carries a 10 kN tensile load and stretches 1.25 mm:

- A = π × 10² ÷ 4 = **{ym_A*1e6:.2f} mm²**
- σ = 10,000 ÷ {ym_A*1e6:.2f} mm² = **{ym_s/1e6:.2f} MPa**
- ε = 1.25 ÷ 2000 = **{ym_e:.6f}** ({ym_e*1e6:.0f} µε)
- E = {ym_s/1e6:.2f} ÷ {ym_e:.6f} = **{ym_E/1e6:,.0f} MPa ≈ {ym_E/1e9:.1f} GPa** — typical for steel

## Typical Young's modulus and strain at 100 MPa

| Material | E | Strain at 100 MPa | Extension of 1 m at 100 MPa |
|---|---|---|---|
{ym_rows}
Values are typical room-temperature figures; grades and alloys vary. Rubber and nylon would not stay elastic at 100 MPa — those rows only show how compliant they are.

## Notes

- 1 GPa = 1,000 MPa = 1 kN/mm². Most metals sit between 40 and 400 GPa.
- The modulus falls as temperature rises — carbon steel loses roughly 5–10% of its room-temperature value by 300 °C.
- For a spring-like view of the same bar, its stiffness is k = A E ÷ L<sub>0</sub>; see the [Hooke's law calculator](/physics/hookes-law/).
''')

# ---------------------------------------------------------------- Stokes' law / terminal velocity
def stokes(d, rp, rf, mu): return (rp - rf) * G * d**2 / (18 * mu)
st_d, st_rp, st_rf, st_mu = 50e-6, 2650.0, 998.0, 0.001
st_v = stokes(st_d, st_rp, st_rf, st_mu); st_Re = st_rf * st_v * st_d / st_mu; st_F = 3 * math.pi * st_mu * st_d * st_v
def _vs(v): return f"{v*1e6:.3g} µm/s" if v < 1e-3 else f"{v*1000:.3g} mm/s"
def _ts(t): return f"{t/3600:.3g} h" if t > 7200 else f"{t/60:.3g} min"
def _re(r): return sci(r, 1) if r < 0.01 else f"{r:.2g}"
st_rows = ''.join(f"| {d:g} µm | {_vs(stokes(d*1e-6, 2650, 998, 0.001))} | {_re(998*stokes(d*1e-6, 2650, 998, 0.001)*d*1e-6/0.001)} | {_ts(1/stokes(d*1e-6, 2650, 998, 0.001))} |\n"
                  for d in (1, 5, 10, 20, 50, 100))
page('physics', 'stokes-law', f'''
title: Stokes' Law Calculator (Terminal Settling Velocity)
description: Calculate the terminal settling velocity of a small sphere in a fluid with Stokes' law, plus the particle Reynolds number to check the law is valid.
category: physics
{intro("Stokes' law describes how fast a small sphere sinks or rises through a viscous fluid once drag balances its weight and buoyancy. This Stokes' law calculator gives the terminal settling velocity, drag force and particle Reynolds number — useful for sedimentation tanks, dust settling, [viscosity measurement](ib:viscosity-measurement-explained) with a falling-ball viscometer and emulsions.")}
keywords: [stokes law calculator, terminal velocity calculator, settling velocity calculator, stokes settling velocity, falling ball viscometer, particle settling rate, sedimentation velocity]
updated: {D}
variables:
  - {{ id: d, label: Particle diameter, family: length, unit: um, imperialUnit: in, default: 50, min: 0 }}
  - {{ id: rp, label: Particle density, family: density, unit: kgm3, imperialUnit: lbft3, default: 2650, min: 0 }}
  - {{ id: rf, label: Fluid density, family: density, unit: kgm3, imperialUnit: lbft3, default: 998, min: 0 }}
  - {{ id: mu, label: Fluid dynamic viscosity, family: viscosity, unit: mPas, default: 1.0, min: 0, help: 'Water at 20 °C ≈ 1.0 mPa·s; air ≈ 0.018 mPa·s.' }}
  - {{ id: v, label: Terminal settling velocity, family: velocity, unit: ms }}
  - {{ id: Re, label: Particle Reynolds number (valid below ~1), min: 0, decimals: 4 }}
  - {{ id: Fd, label: Drag force at terminal velocity, family: force, unit: N, min: 0 }}
equations:
  - v = (rp - rf) * g0 * d^2 / (18 * mu)
  - Re = rf * abs(v) * d / mu
  - Fd = 3 * pi * mu * d * abs(v)
faq:
  - q: What is Stokes' law for settling velocity?
    a: v = (ρp − ρf) g d² ÷ (18 μ). Velocity grows with the square of particle diameter, so a particle twice as large settles four times faster.
  - q: When is Stokes' law valid?
    a: For creeping flow around a smooth sphere — particle Reynolds number below about 1 (strictly below 0.1 for high accuracy). Larger or faster particles need a drag coefficient correlation instead.
  - q: What does a negative velocity mean?
    a: The particle is lighter than the fluid, so it rises instead of sinking — for example oil droplets or air bubbles in water.
  - q: How is Stokes' law used to measure viscosity?
    a: In a falling-ball viscometer a ball of known size and density falls a measured distance; rearranging gives μ = (ρp − ρf) g d² ÷ (18 v). Clear the viscosity field and enter the measured velocity.
related: [engineering/reynolds-number, physics/buoyancy, physics/drag-force, physics/density]
''', f'''
## How to use the Stokes' law calculator

Enter the **particle diameter**, the **particle density**, the **fluid density** and the fluid's **dynamic viscosity**. The calculator returns the terminal settling velocity (negative means the particle rises), the drag force at that speed and the **particle Reynolds number** — keep it below about 1 for Stokes' law to apply. To find viscosity from a falling-ball test, clear the viscosity and enter the measured velocity.

## Stokes' law formula

<p class="formula">v<sub>t</sub> = (ρ<sub>p</sub> − ρ<sub>f</sub>) g d² ÷ (18 μ)</p>

<p class="formula">F<sub>d</sub> = 3 π μ d v &nbsp;·&nbsp; Re<sub>p</sub> = ρ<sub>f</sub> v d ÷ μ</p>

## Example

A 50 µm quartz sand grain (2,650 kg/m³) settling in water at 20 °C (998 kg/m³, 1.0 mPa·s):

- v = (2650 − 998) × 9.807 × (50 × 10⁻⁶)² ÷ (18 × 0.001) = **{st_v:.6f} m/s** ({st_v*1000:.2f} mm/s)
- Re = 998 × {st_v:.6f} × 50 × 10⁻⁶ ÷ 0.001 = **{st_Re:.3f}** — below 1, so Stokes' law applies
- Drag force = 3π × 0.001 × 50 × 10⁻⁶ × {st_v:.6f} = **{sci(st_F, 3)} N**, equal to the grain's submerged weight

## Settling of quartz particles in water at 20 °C

| Diameter | Settling velocity | Reynolds number | Time to settle 1 m |
|---|---|---|---|
{st_rows}
At 100 µm the Reynolds number approaches 1, so Stokes' law starts to overpredict the velocity of larger grains.

## Notes

- Viscosity changes strongly with temperature — water at 5 °C is about 1.5 mPa·s, slowing settling by a third.
- Non-spherical particles settle more slowly than the equivalent sphere.
- For larger objects, use the [drag force calculator](/physics/drag-force/) with a drag coefficient instead.
''')

# ---------------------------------------------------------------- Drag force
dr_rho, dr_v, dr_Cd, dr_A = 1.225, 100/3.6, 0.30, 2.2
dr_F = 0.5 * dr_rho * dr_v**2 * dr_Cd * dr_A; dr_P = dr_F * dr_v
shapes = [('Flat plate (normal to flow)', 1.28), ('Cube', 1.05), ('Upright cyclist', 0.9), ('Sphere (subcritical)', 0.47),
          ('Typical car', 0.30), ('Streamlined car', 0.25), ('Streamlined body', 0.04)]
dr_rows = ''.join(f"| {nm} | {cd:g} | {0.5*1.225*(50/3.6)**2*cd:,.1f} N | {0.5*1.225*(100/3.6)**2*cd:,.1f} N | {0.5*1.225*(150/3.6)**2*cd:,.1f} N |\n" for nm, cd in shapes)
page('physics', 'drag-force', f'''
title: Drag Force Calculator (F = ½ρv²CdA) & Power to Overcome Drag
description: Calculate aerodynamic or hydrodynamic drag force from fluid density, speed, drag coefficient and frontal area — and the power needed to overcome it.
category: physics
intro: "Drag is the resistance a fluid exerts on a moving object, and it grows with the square of speed. This drag force calculator uses the drag equation F = ½ρv²C<sub>d</sub>A to find the force and the power needed to push through air or water — for cars, cyclists, wind loads, sensors in pipes and falling objects."
keywords: [drag force calculator, drag equation, aerodynamic drag calculator, air resistance calculator, drag coefficient, power to overcome drag, wind resistance force]
updated: {D}
variables:
  - {{ id: rho, label: Fluid density, family: density, unit: kgm3, imperialUnit: lbft3, default: 1.225, min: 0, help: 'Air at sea level 15 °C: 1.225 kg/m³. Water: about 1000 kg/m³.' }}
  - {{ id: v, label: Speed relative to the fluid, family: velocity, unit: kmh, imperialUnit: mph, default: 100, min: 0 }}
  - {{ id: Cd, label: Drag coefficient (Cd), default: 0.30, min: 0, decimals: 3 }}
  - {{ id: A, label: Frontal (reference) area, family: area, unit: m2, imperialUnit: ft2, default: 2.2, min: 0 }}
  - {{ id: F, label: Drag force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: P, label: Power to overcome drag, family: power, unit: kW, imperialUnit: hp, min: 0 }}
equations:
  - F = 0.5 * rho * v^2 * Cd * A
  - P = F * v
faq:
  - q: What is the drag force formula?
    a: F = ½ ρ v² Cd A — half the fluid density times speed squared times the drag coefficient times the frontal area.
  - q: Why does drag power rise with the cube of speed?
    a: Drag force grows with v², and power is force × speed, so power grows with v³. Driving at 130 km/h instead of 100 km/h needs about 2.2 times the power to beat air drag.
  - q: What is a typical drag coefficient?
    a: About 0.25–0.35 for modern cars, 0.47 for a sphere, 1.0–1.3 for flat plates and bluff shapes, and 0.04 for a streamlined teardrop.
  - q: Which area should I use?
    a: The frontal area projected onto a plane perpendicular to the flow for vehicles and bluff bodies. Wings use plan area, so check which reference area the Cd value was measured with.
related: [physics/stokes-law, physics/work-and-power, physics/force, engineering/pitot-tube-velocity]
''', f'''
## How to use the drag force calculator

Enter the **fluid density**, the **speed** of the object relative to the fluid, its **drag coefficient** and its **frontal area**. You get the drag force and the power needed to overcome it at that speed. Clear any field to solve for it instead — for example, enter a measured drag force and clear C<sub>d</sub> to find the drag coefficient.

## Drag equation

<p class="formula">F<sub>d</sub> = ½ ρ v² C<sub>d</sub> A</p>

<p class="formula">P = F<sub>d</sub> × v = ½ ρ v³ C<sub>d</sub> A</p>

## Example

A car with C<sub>d</sub> = 0.30 and 2.2 m² frontal area at 100 km/h (27.78 m/s) in sea-level air:

- F = 0.5 × 1.225 × 27.78² × 0.30 × 2.2 = **{dr_F:.1f} N**
- P = {dr_F:.1f} × 27.78 = **{dr_P/1000:.2f} kW** just to push the air aside

## Drag force on 1 m² of frontal area in sea-level air

| Shape | Cd | 50 km/h | 100 km/h | 150 km/h |
|---|---|---|---|---|
{dr_rows}
Drag coefficients are typical values; the real Cd depends on Reynolds number, surface finish and exact shape.

## Notes

- Air density falls with altitude and temperature (about 1.0 kg/m³ at 2,000 m), reducing drag.
- At very low Reynolds numbers (dust, fine droplets) use [Stokes' law](/physics/stokes-law/) instead.
- Terminal velocity of a falling object is where drag equals weight: v = √(2 m g ÷ (ρ C<sub>d</sub> A)).
''')

# ---------------------------------------------------------------- Latent heat
LH = [('Water — melting / freezing (334 kJ/kg)', 334), ('Water — boiling at 100 °C (2,257 kJ/kg)', 2257),
      ('Ethanol — melting (108 kJ/kg)', 108), ('Ammonia — boiling at −33 °C (1,369 kJ/kg)', 1369),
      ('Aluminium — melting (397 kJ/kg)', 397), ('Copper — melting (209 kJ/kg)', 209),
      ('Iron — melting (247 kJ/kg)', 247), ('Lead — melting (23 kJ/kg)', 23)]
lh_opts = ''.join(f"      - {{ label: '{lb}', value: {v} }}\n" for lb, v in LH)
lh_m, lh_L = 2.0, 2257
lh_Q = lh_m * lh_L * 1000
lh_rows = ''.join(f"| {lb.split(' (')[0]} | {v:,} kJ | {v/3600:.4g} kWh |\n" for lb, v in LH)
page('physics', 'latent-heat', f'''
title: Latent Heat Calculator (Q = mL) — Melting & Boiling Energy
description: Calculate the heat needed to melt, freeze, boil or condense a substance with Q = mL — water, ethanol, ammonia and metals, or any specific latent heat.
category: physics
intro: "Latent heat is the energy a substance absorbs or releases while it changes phase at constant temperature — melting, freezing, boiling or condensing. This latent heat calculator applies Q = mL to find the energy for a given mass, or the mass that a given amount of energy can melt or evaporate."
keywords: [latent heat calculator, q = ml calculator, latent heat of fusion, latent heat of vaporization, energy to melt ice, energy to boil water, specific latent heat]
updated: {D}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 2, min: 0 }}
  - id: L
    label: Substance and phase change (specific latent heat)
    default: 2257
    options:
{lh_opts.rstrip()}
  - {{ id: Q, label: Heat energy, family: energy, unit: kJ, imperialUnit: BTU, min: 0 }}
  - {{ id: Qk, label: Heat energy in kWh, suffix: kWh, min: 0 }}
equations:
  - Q = m * L * 1000
  - Qk = Q / 3.6e6
faq:
  - q: What is the formula for latent heat?
    a: Q = m × L, where m is the mass and L the specific latent heat of fusion (melting) or vaporisation (boiling) in J/kg.
  - q: How much energy does it take to boil 1 kg of water?
    a: About 2,257 kJ (0.63 kWh) once it is already at 100 °C — more than five times the 419 kJ needed to heat it from 0 to 100 °C.
  - q: Why does temperature stay constant during melting or boiling?
    a: The added energy breaks the bonds between molecules instead of making them move faster, so the temperature holds until the phase change is complete.
  - q: Is energy released when steam condenses?
    a: Yes — exactly the same amount, 2,257 kJ per kg at 100 °C. This is why steam is such an effective heating medium and why steam burns are severe.
related: [chemistry/specific-heat, engineering/heat-duty, physics/newtons-law-of-cooling, physics/heat-conduction]
''', f'''
## How to use the latent heat calculator

Enter the **mass** and choose the **substance and phase change**. The calculator gives the heat that must be added (melting, boiling) or removed (freezing, condensing) in kJ and kWh. To find how much mass a given amount of heat can melt or evaporate, clear the mass and enter the energy.

## Latent heat formula

<p class="formula">Q = m × L</p>

L<sub>f</sub> is the specific latent heat of fusion (solid ↔ liquid) and L<sub>v</sub> the specific latent heat of vaporisation (liquid ↔ gas). This calculation covers only the phase change; add the sensible heat m c ΔT from the [specific heat calculator](/chemistry/specific-heat/) to bring the substance to its melting or boiling point first.

## Example

Boiling off 2 kg of water that is already at 100 °C:

- Q = 2 kg × 2,257 kJ/kg = **{lh_Q/1000:,.0f} kJ**
- = {lh_Q/1000:,.0f} ÷ 3,600 = **{lh_Q/3.6e6:.3f} kWh**

## Energy per kilogram for each phase change

| Substance and change | Energy per kg | In kWh |
|---|---|---|
{lh_rows}
Values are at the normal melting or boiling point at 1 atm; the latent heat of vaporisation of water falls as pressure (and boiling temperature) rises.

## Notes

- Melting ice absorbs as much energy as heating the same water by about 80 °C — the basis of ice storage cooling.
- Steam tables give h<sub>fg</sub> for water at other pressures, for example about 2,015 kJ/kg at 10 bar(a).
- Use the [heat duty calculator](/engineering/heat-duty/) when a stream changes temperature at a steady flow rate.
''')

# ---------------------------------------------------------------- Newton's law of cooling
nc_T0, nc_Ta, nc_k, nc_t = 90.0, 20.0, 0.05, 10.0
nc_T = nc_Ta + (nc_T0 - nc_Ta) * math.exp(-nc_k * nc_t)
nc_th = math.log(2) / nc_k
nc_rows = ''.join(f"| {t:g} min | {nc_Ta + (nc_T0-nc_Ta)*math.exp(-nc_k*t):.1f} °C | {math.exp(-nc_k*t)*100:.1f}% |\n" for t in (0, 5, 10, 15, 20, 30, 45, 60, 90))
page('physics', 'newtons-law-of-cooling', f'''
title: Newton's Law of Cooling Calculator (Temperature vs Time)
description: Calculate how an object cools or heats towards ambient over time with Newton's law of cooling, find the cooling constant k and the half-time.
category: physics
{intro("Newton's law of cooling says an object's rate of temperature change is proportional to the difference between it and its surroundings, giving an exponential approach to ambient. This Newton's law of cooling calculator finds the temperature after any time, the cooling constant from a measurement and the time for the difference to halve — the same first-order behaviour behind a [temperature sensor's response time](ib:temperature-sensor-response-time).")}
keywords: [newtons law of cooling calculator, cooling rate calculator, temperature vs time cooling, cooling constant k, exponential cooling, how long to cool, newton cooling formula]
updated: {D}
variables:
  - {{ id: T0, label: Initial temperature, family: temperature, unit: C, imperialUnit: F, default: 90 }}
  - {{ id: Ta, label: Ambient (surrounding) temperature, family: temperature, unit: C, imperialUnit: F, default: 20 }}
  - {{ id: k, label: Cooling constant k (per minute), default: 0.05, min: 0, decimals: 5 }}
  - {{ id: t, label: Elapsed time, family: seconds, unit: min, default: 10, min: 0 }}
  - {{ id: Tt, label: Temperature after time t, family: temperature, unit: C, imperialUnit: F }}
  - {{ id: th, label: Half-time (difference halves), family: seconds, unit: min, min: 0 }}
  - {{ id: tau, label: Time constant (1/k), family: seconds, unit: min, min: 0 }}
equations:
  - Tt = Ta + (T0 - Ta) * exp(-k * t / 60)
  - th = 60 * ln(2) / k
  - tau = 60 / k
faq:
  - q: What is the formula for Newton's law of cooling?
    a: T(t) = Tₐ + (T₀ − Tₐ) e^(−kt). The temperature difference to ambient decays exponentially with the cooling constant k.
  - q: How do I find the cooling constant k?
    a: Measure the temperature at a known time, clear k and enter the measured value — k = −ln[(T − Tₐ) ÷ (T₀ − Tₐ)] ÷ t. For example, coffee falling from 90 to 62.5 °C in 10 minutes in a 20 °C room gives k ≈ 0.05 per minute.
  - q: Does it work for heating too?
    a: Yes. If the ambient is hotter than the object, the same equation gives an exponential rise towards ambient.
  - q: When is Newton's law of cooling accurate?
    a: When heat loss is dominated by convection with a roughly constant heat transfer coefficient, the object's temperature is uniform, and the temperature difference is moderate. Strong radiation or boiling make k change with temperature.
related: [physics/heat-conduction, engineering/sensor-response-time, physics/latent-heat, chemistry/half-life]
''', f'''
## How to use the Newton's law of cooling calculator

Enter the **initial temperature** of the object, the **ambient temperature**, the **cooling constant** k (per minute) and the **elapsed time**. The calculator returns the temperature at that time, the **half-time** (when the difference to ambient has halved) and the time constant 1/k. To find k from a measurement, clear k and enter the measured temperature; to find how long cooling takes, clear the time.

## Newton's law of cooling formula

<p class="formula">T(t) = T<sub>a</sub> + (T<sub>0</sub> − T<sub>a</sub>) e<sup>−kt</sup></p>

<p class="formula">t<sub>½</sub> = ln 2 ÷ k &nbsp;·&nbsp; τ = 1 ÷ k &nbsp;·&nbsp; k = h A ÷ (m c)</p>

The constant k combines the heat transfer coefficient h, surface area A, mass m and specific heat c of the object.

## Example

A cup of coffee at 90 °C in a 20 °C room with k = 0.05 per minute, after 10 minutes:

- T = 20 + (90 − 20) × e<sup>−0.05 × 10</sup> = 20 + 70 × {math.exp(-0.5):.4f} = **{nc_T:.2f} °C**
- Half-time = ln 2 ÷ 0.05 = **{nc_th:.2f} min**
- Time constant = 1 ÷ 0.05 = **{1/nc_k:g} min**

## Cooling curve for the example (90 °C → 20 °C ambient, k = 0.05 /min)

| Time | Temperature | Remaining difference |
|---|---|---|
{nc_rows}
After one time constant 36.8% of the difference remains; after five time constants less than 1% remains.

## Notes

- Stirring, wind or a fan raises h and therefore k — the cup cools faster.
- The same exponential law describes a thermometer or [sensor reaching a step change](/engineering/sensor-response-time/), with τ as its time constant.
- Forensic "time since death" estimates use the same principle, with empirically corrected k values.
''')

# ---------------------------------------------------------------- Photon energy
def ph_eV(lam_nm): return H * C0 / (lam_nm * 1e-9) / QE
pe_lam = 532.0
pe_fT = C0 / (pe_lam * 1e-9) / 1e12; pe_EJ = H * pe_fT * 1e12; pe_eV = pe_EJ / QE; pe_Em = pe_EJ * NA / 1000; pe_N = 1e-3 / pe_EJ
bands = [('UV-C germicidal lamp', 254), ('UV-A / violet laser', 405), ('Blue LED', 450), ('Green laser', 532), ('Red laser', 650),
         ('Near-IR (sensors, remotes)', 850), ('Near-IR LED', 940), ('Telecom fibre', 1550)]
pe_rows = ''.join(f"| {nm} | {lam} nm | {C0/(lam*1e-9)/1e12:.1f} THz | {ph_eV(lam):.3f} eV | {ph_eV(lam)*QE*NA/1000:.1f} kJ/mol |\n" for nm, lam in bands)
page('physics', 'photon-energy', f'''
title: Photon Energy Calculator (E = hf = hc/λ) in eV and Joules
description: Calculate photon energy in electronvolts and joules from wavelength, plus frequency, energy per mole and photons per second for a given light power.
category: physics
{intro("A photon's energy depends only on its frequency, E = hf, or equivalently on its wavelength, E = hc/λ. This photon energy calculator converts a wavelength into energy in eV and joules, frequency, energy per mole and the number of photons a light source emits per second — useful for lasers, LEDs, [photodiodes and phototransistors](ib:photodiode-vs-phototransistor-key-differences) and photochemistry.")}
keywords: [photon energy calculator, e = hf calculator, wavelength to ev, photon energy in ev, e = hc / lambda, photons per second calculator, planck equation]
updated: {D}
variables:
  - {{ id: lam, label: Wavelength (nm), default: 532, min: 0 }}
  - {{ id: fT, label: Frequency (THz), min: 0 }}
  - {{ id: eV, label: Photon energy (eV), min: 0, decimals: 4 }}
  - {{ id: EJ, label: Photon energy (joules), family: energy, unit: J, min: 0 }}
  - {{ id: Em, label: Energy per mole of photons (kJ/mol), min: 0 }}
  - {{ id: P, label: Light (optical) power, family: power, unit: mW, default: 1, min: 0 }}
  - {{ id: N, label: Photons per second, min: 0 }}
equations:
  - fT = 299792.458 / lam
  - EJ = 6.62607015e-34 * fT * 1e12
  - eV = EJ / 1.602176634e-19
  - Em = EJ * 6.02214076e20
  - N = P / EJ
faq:
  - q: How do I convert wavelength to photon energy in eV?
    a: E (eV) = 1239.84 ÷ λ (nm). A 532 nm green laser photon carries about 2.33 eV.
  - q: What is the energy of a photon in joules?
    a: E = h f = h c ÷ λ, with h = 6.626 × 10⁻³⁴ J·s and c = 2.998 × 10⁸ m/s. A 532 nm photon has about 3.73 × 10⁻¹⁹ J.
  - q: How many photons per second does a 1 mW laser emit?
    a: Divide the power by the photon energy. A 1 mW green laser at 532 nm emits about 2.7 × 10¹⁵ photons per second.
  - q: Why can't infrared light trigger some photodetectors?
    a: A photon can only free an electron if its energy exceeds the material's band gap. Silicon (1.12 eV) responds up to about 1,100 nm; beyond that, detectors such as InGaAs are needed.
related: [physics/wavelength-frequency, physics/de-broglie-wavelength, electronics/led-resistor, physics/snells-law]
''', f'''
## How to use the photon energy calculator

Enter the **wavelength in nanometres**. The calculator returns the frequency in THz, the photon energy in electronvolts and joules and the energy of one mole of photons. Enter the **optical power** of a source to find how many photons it emits each second. To go from energy to wavelength, clear the wavelength and enter the energy in eV.

## Photon energy formula

<p class="formula">E = h f = h c ÷ λ</p>

<p class="formula">E (eV) ≈ 1239.84 ÷ λ (nm) &nbsp;·&nbsp; N = P ÷ E</p>

h = 6.62607015 × 10⁻³⁴ J·s (Planck constant), c = 299,792,458 m/s and 1 eV = 1.602176634 × 10⁻¹⁹ J — all exact SI values.

## Example

A 532 nm green laser with 1 mW output:

- f = 299,792,458 ÷ 532 × 10⁻⁹ = **{pe_fT:.2f} THz**
- E = 6.626 × 10⁻³⁴ × {pe_fT:.2f} × 10¹² = **{sci(pe_EJ, 4)} J** = **{pe_eV:.4f} eV**
- Per mole: **{pe_Em:.1f} kJ/mol**
- Photons per second = 0.001 ÷ {sci(pe_EJ, 4)} = **{sci(pe_N, 3)}**

## Photon energy of common light sources

| Source | Wavelength | Frequency | Energy | Per mole |
|---|---|---|---|---|
{pe_rows}
## Notes

- Shorter wavelength means higher energy: UV-C photons (about 4.9 eV) can break chemical bonds, which is why they disinfect.
- An LED's forward voltage is roughly its photon energy in eV — a blue LED needs about 2.8–3.3 V, a red one about 1.8–2.2 V.
- For a matter wave instead of light, use the [de Broglie wavelength calculator](/physics/de-broglie-wavelength/).
''')

# ---------------------------------------------------------------- de Broglie wavelength
db_m, db_v = ME, 1.0e6
db_p = db_m * db_v; db_lam = H / db_p; db_KE = 0.5 * db_m * db_v**2 / QE
def lam_e(V, rel=True):
    E = QE * V
    p = math.sqrt(2 * ME * E * (1 + (E / (2 * ME * C0**2) if rel else 0)))
    return H / p
db_rows = ''.join(f"| {V:,} V | {lam_e(V, False)*1e12:.3f} pm | {lam_e(V)*1e12:.3f} pm |\n" for V in (10, 100, 1000, 10000, 100000, 300000))
page('physics', 'de-broglie-wavelength', f'''
title: de Broglie Wavelength Calculator (λ = h/mv)
description: Calculate the de Broglie wavelength of an electron, proton, neutron or any mass from its velocity, with momentum and kinetic energy in eV.
category: physics
intro: "Every moving particle behaves as a wave whose wavelength is Planck's constant divided by its momentum, λ = h/p. This de Broglie wavelength calculator gives the matter wavelength, momentum and kinetic energy of electrons, protons, neutrons or any object — the physics behind electron microscopes and electron diffraction."
keywords: [de broglie wavelength calculator, lambda = h / mv, matter wave calculator, electron wavelength calculator, de broglie equation, wavelength of electron, particle wavelength]
updated: {D}
variables:
  - id: m
    label: Particle (rest mass)
    default: {ME!r}
    options:
      - {{ label: 'Electron (9.109 × 10⁻³¹ kg)', value: {ME!r} }}
      - {{ label: 'Proton (1.673 × 10⁻²⁷ kg)', value: {MP!r} }}
      - {{ label: 'Neutron (1.675 × 10⁻²⁷ kg)', value: {MN!r} }}
      - {{ label: 'Alpha particle (6.645 × 10⁻²⁷ kg)', value: 6.6446573357e-27 }}
  - {{ id: v, label: Velocity, family: velocity, unit: ms, default: 1000000, min: 0, help: 'Non-relativistic formula — keep v below about 10% of the speed of light (3 × 10⁷ m/s).' }}
  - {{ id: p, label: Momentum (kg·m/s), min: 0 }}
  - {{ id: lnm, label: de Broglie wavelength (nm), min: 0 }}
  - {{ id: KE, label: Kinetic energy (eV), min: 0 }}
equations:
  - p = m * v
  - lnm = 6.62607015e-34 / p * 1e9
  - KE = 0.5 * m * v^2 / 1.602176634e-19
faq:
  - q: What is the de Broglie wavelength formula?
    a: λ = h ÷ p = h ÷ (m v), where h = 6.626 × 10⁻³⁴ J·s. Heavier or faster particles have shorter wavelengths.
  - q: What is the wavelength of an electron moving at 10⁶ m/s?
    a: About 0.727 nm — comparable to the spacing of atoms in a crystal, which is why electrons diffract from crystals.
  - q: Why don't everyday objects show wave behaviour?
    a: Their momentum is enormous by comparison. A 0.15 kg ball at 40 m/s has λ ≈ 1.1 × 10⁻³⁴ m, far too small to observe.
  - q: When do I need the relativistic formula?
    a: Above about 10% of the speed of light. For electrons accelerated through more than a few kilovolts, use p = √(2 m E (1 + E ÷ 2mc²)); the table below shows the difference.
related: [physics/photon-energy, physics/momentum, physics/kinetic-energy, physics/wavelength-frequency]
''', f'''
## How to use the de Broglie wavelength calculator

Choose the **particle** and enter its **velocity**. The calculator returns the momentum, the de Broglie wavelength in nanometres and the kinetic energy in electronvolts. To find the velocity needed for a given wavelength, clear the velocity and enter the wavelength.

## de Broglie wavelength formula

<p class="formula">λ = h ÷ p = h ÷ (m v)</p>

<p class="formula">KE = ½ m v² &nbsp;·&nbsp; λ = h ÷ √(2 m KE)</p>

## Example

An electron (9.109 × 10⁻³¹ kg) moving at 1 × 10⁶ m/s:

- p = 9.109 × 10⁻³¹ × 10⁶ = **{sci(db_p, 4)} kg·m/s**
- λ = 6.626 × 10⁻³⁴ ÷ {sci(db_p, 4)} = **{db_lam*1e9:.4f} nm**
- KE = ½ × 9.109 × 10⁻³¹ × (10⁶)² = **{db_KE:.3f} eV**

## Wavelength of electrons accelerated through a voltage

| Accelerating voltage | Non-relativistic λ | Relativistic λ |
|---|---|---|
{db_rows}
Transmission electron microscopes run at 100–300 kV, giving wavelengths of a few picometres — far below the 400–700 nm of visible light.

## Notes

- For an electron accelerated from rest through V volts, λ (nm) ≈ 1.226 ÷ √V (non-relativistic).
- Thermal neutrons (about 2,200 m/s) have λ ≈ 0.18 nm, ideal for neutron diffraction.
- The [photon energy calculator](/physics/photon-energy/) does the equivalent conversion for light, where λ = h c ÷ E.
''')

# ================================================================ CHEMISTRY

# ---------------------------------------------------------------- Ka ↔ pKa, Kb ↔ pKb
pk_Ka = 1.8e-5
pk_pKa = -math.log10(pk_Ka); pk_Kb = 1e-14 / pk_Ka; pk_pKb = 14 - pk_pKa
acids = [('Phosphoric acid (pKa₁)', 2.15), ('Hydrofluoric acid', 3.17), ('Formic acid', 3.75), ('Lactic acid', 3.86), ('Benzoic acid', 4.20),
         ('Acetic acid', 4.76), ('Carbonic acid (pKa₁)', 6.35), ('Hypochlorous acid', 7.53), ('Hydrocyanic acid', 9.21), ('Ammonium ion', 9.25)]
pk_rows = ''.join(f"| {nm} | {p:.2f} | {sci(10**-p, 2)} | {14-p:.2f} | {sci(10**-(14-p), 2)} |\n" for nm, p in acids)
page('chemistry', 'pka', f'''
title: pKa Calculator — Ka to pKa, Kb to pKb and Back
description: Convert Ka to pKa and back, and find the conjugate base Kb and pKb at 25 °C using Ka × Kb = Kw — with a table of pKa values for common acids.
category: chemistry
{intro("pKa is the negative logarithm of an acid's dissociation constant: the lower the pKa, the stronger the acid. This pKa calculator converts Ka to pKa (or pKa to Ka) and gives the Kb and pKb of the conjugate base — the numbers you need to pick a buffer, as in [pH meter calibration buffers](ib:ph-meter-calibration-buffers), or to estimate pH.")}
keywords: [pka calculator, ka to pka, pka to ka, kb to pkb, pkb calculator, acid dissociation constant, pka + pkb = 14]
updated: {D}
variables:
  - {{ id: Ka, label: Acid dissociation constant Ka, default: 0.000018, min: 0 }}
  - {{ id: pKa, label: pKa, decimals: 4 }}
  - {{ id: Kb, label: Kb of the conjugate base, min: 0 }}
  - {{ id: pKb, label: pKb of the conjugate base, decimals: 4 }}
equations:
  - pKa = -log10(Ka)
  - Kb = 1e-14 / Ka
  - pKb = 14 - pKa
faq:
  - q: How do I convert Ka to pKa?
    a: pKa = −log₁₀(Ka). Acetic acid has Ka = 1.8 × 10⁻⁵, so its pKa is 4.74.
  - q: How do I convert pKa back to Ka?
    a: Ka = 10^(−pKa). Clear the Ka field, enter the pKa and the calculator does the antilog.
  - q: What is the relationship between pKa and pKb?
    a: For a conjugate acid–base pair in water at 25 °C, Ka × Kb = Kw = 1.0 × 10⁻¹⁴, so pKa + pKb = 14.
  - q: What does pKa tell you about a buffer?
    a: A buffer works best within about ±1 pH unit of the acid's pKa, and at pH = pKa the acid and its conjugate base are present in equal amounts.
related: [chemistry/weak-acid-ph, chemistry/henderson-hasselbalch, chemistry/ph, chemistry/titration]
''', f'''
## How to use the pKa calculator

Enter the **acid dissociation constant Ka** (you can type it as 0.000018 or 1.8e-5). The calculator returns the pKa and the Kb and pKb of the conjugate base. To go the other way, clear Ka and enter a pKa, Kb or pKb. For a weak base, enter its Kb in the Kb field and read the pKa of its conjugate acid.

## Ka, pKa, Kb and pKb formulas

<p class="formula">pKa = −log₁₀ Ka &nbsp;·&nbsp; Ka = 10<sup>−pKa</sup></p>

<p class="formula">Ka × Kb = K<sub>w</sub> = 1.0 × 10⁻¹⁴ &nbsp;·&nbsp; pKa + pKb = 14 (25 °C)</p>

## Example

Acetic acid, Ka = 1.8 × 10⁻⁵:

- pKa = −log₁₀(1.8 × 10⁻⁵) = **{pk_pKa:.4f}**
- Kb (acetate ion) = 10⁻¹⁴ ÷ 1.8 × 10⁻⁵ = **{sci(pk_Kb, 3)}**
- pKb = 14 − {pk_pKa:.4f} = **{pk_pKb:.4f}**

## pKa of common weak acids at 25 °C

| Acid | pKa | Ka | pKb of conjugate base | Kb of conjugate base |
|---|---|---|---|---|
{pk_rows}
Literature values vary by about ±0.05 between sources and with ionic strength.

## Notes

- K<sub>w</sub> changes with temperature (pK<sub>w</sub> ≈ 14.17 at 20 °C and 13.26 at 50 °C), so pKa + pKb = 14 holds only at 25 °C.
- Polyprotic acids have one pKa per proton — phosphoric acid has 2.15, 7.20 and 12.35.
- Use the [Henderson–Hasselbalch calculator](/chemistry/henderson-hasselbalch/) to find buffer pH from pKa and the acid–base ratio.
''')

# ---------------------------------------------------------------- pH of weak acid / weak base
def wx(K, C): return (math.sqrt(K * K + 4 * K * C) - K) / 2
wa_x = wx(1.8e-5, 0.1); wa_pH = -math.log10(wa_x); wa_al = wa_x / 0.1
wb_x = wx(1.8e-5, 0.1); wb_pH = 14 + math.log10(wb_x)
wa_rows = ''.join(f"| {C:g} mol/L | {-math.log10(wx(1.8e-5, C)):.3f} | {wx(1.8e-5, C)/C*100:.2f}% | {14+math.log10(wx(1.8e-5, C)):.3f} |\n" for C in (1, 0.5, 0.1, 0.05, 0.01, 0.001))
page('chemistry', 'weak-acid-ph', f'''
title: Weak Acid pH Calculator (and Weak Base pH from Ka or Kb)
description: Calculate the pH of a weak acid or weak base solution from Ka or Kb and concentration, using the exact quadratic — plus percent dissociation.
category: chemistry
{intro("A weak acid only partly dissociates, so its pH depends on both its concentration and its Ka. This weak acid pH calculator solves the equilibrium exactly with the quadratic formula — and works for weak bases from Kb — giving the pH, [H⁺] or [OH⁻] and the percent dissociated. A [pH sensor](ib:what-is-ph-sensor-how-does-it-work) measures the same quantity directly.")}
keywords: [weak acid ph calculator, ph of weak acid, weak base ph calculator, ph from ka and concentration, percent dissociation, acetic acid ph, ice table ph]
updated: {D}
variables:
  - id: t
    label: Solution type
    default: 1
    options:
      - {{ label: 'Weak acid (enter Ka)', value: 1 }}
      - {{ label: 'Weak base (enter Kb)', value: 0 }}
  - {{ id: K, label: Ka (acid) or Kb (base), default: 0.000018, min: 0, help: 'Acetic acid Ka = 1.8e-5; ammonia Kb = 1.8e-5.' }}
  - {{ id: C, label: Initial concentration, suffix: mol/L, default: 0.1, min: 0 }}
  - {{ id: x, label: '[H⁺] (acid) or [OH⁻] (base) at equilibrium', suffix: mol/L, min: 0 }}
  - {{ id: pH, label: pH, decimals: 3 }}
  - {{ id: al, label: Percent dissociated, family: percent, unit: '%', min: 0, decimals: 3 }}
equations:
  - x = (sqrt(K^2 + 4 * K * C) - K) / 2
  - pH = t * (-log10(x)) + (1 - t) * (14 + log10(x))
  - al = x / C
faq:
  - q: How do you calculate the pH of a weak acid?
    a: Solve Ka = x² ÷ (C − x) for x = [H⁺], which gives x = (−Ka + √(Ka² + 4 Ka C)) ÷ 2, then pH = −log₁₀ x. For 0.1 M acetic acid this gives pH 2.88.
  - q: Can I use the shortcut x = √(Ka C)?
    a: Yes, when the acid is less than about 5% dissociated (C ÷ Ka above roughly 400). The calculator always uses the exact quadratic, so it stays correct for dilute or stronger weak acids.
  - q: How is weak base pH calculated?
    a: The same way with Kb — x is then [OH⁻], pOH = −log₁₀ x and pH = 14 − pOH at 25 °C. 0.1 M ammonia (Kb = 1.8 × 10⁻⁵) has pH 11.13.
  - q: Why does dilution increase percent dissociation?
    a: Le Chatelier's principle — diluting shifts the equilibrium towards more ions. 0.1 M acetic acid is 1.3% dissociated; 0.001 M is about 12.5%.
related: [chemistry/pka, chemistry/ph, chemistry/henderson-hasselbalch, chemistry/molarity]
''', f'''
## How to use the weak acid pH calculator

Choose **weak acid** or **weak base**, enter its **Ka** or **Kb** and the **initial concentration** in mol/L. The calculator returns the equilibrium [H⁺] (or [OH⁻] for a base), the pH and the percent dissociated. If you only know the pKa, convert it first with the [pKa calculator](/chemistry/pka/).

## Weak acid pH formula

<p class="formula">Ka = x² ÷ (C − x) &nbsp;⇒&nbsp; x = (−Ka + √(Ka² + 4 Ka C)) ÷ 2</p>

<p class="formula">Acid: pH = −log₁₀ x &nbsp;·&nbsp; Base: pH = 14 + log₁₀ x &nbsp;·&nbsp; % dissociated = x ÷ C × 100</p>

Water's own ionisation is ignored, which is accurate unless the solution is extremely dilute (below about 10⁻⁶ mol/L) or the acid extremely weak.

## Examples

0.1 mol/L acetic acid (Ka = 1.8 × 10⁻⁵):

- x = (−1.8 × 10⁻⁵ + √((1.8 × 10⁻⁵)² + 4 × 1.8 × 10⁻⁵ × 0.1)) ÷ 2 = **{sci(wa_x, 4)} mol/L**
- pH = −log₁₀({sci(wa_x, 4)}) = **{wa_pH:.3f}**
- Percent dissociated = **{wa_al*100:.3f}%**

0.1 mol/L ammonia (Kb = 1.8 × 10⁻⁵): [OH⁻] = {sci(wb_x, 4)} mol/L, pH = 14 + log₁₀(x) = **{wb_pH:.3f}**.

## pH of acetic acid and ammonia vs concentration (K = 1.8 × 10⁻⁵)

| Concentration | Acetic acid pH | Acetic acid % dissociated | Ammonia pH |
|---|---|---|---|
{wa_rows}
## Notes

- pH 14 + log x assumes 25 °C; at other temperatures use the local pK<sub>w</sub>.
- For a mixture of a weak acid and its salt (a buffer), use the [Henderson–Hasselbalch calculator](/chemistry/henderson-hasselbalch/) instead.
- Strong acids are fully dissociated — use the [pH calculator](/chemistry/ph/) with [H⁺] = C.
''')

# ---------------------------------------------------------------- Gay-Lussac's law
gl_P1, gl_T1, gl_T2 = 200.0, 20.0, 80.0
gl_P2 = gl_P1 * (gl_T2 + 273.15) / (gl_T1 + 273.15)
gl_rows = ''.join(f"| {T:g} °C | {(T+273.15)/293.15:.3f} | {200*(T+273.15)/293.15:.1f} kPa | {200*(T+273.15)/293.15-101.325:.1f} kPa |\n" for T in (-20, 0, 20, 40, 60, 80, 100, 150))
page('chemistry', 'gay-lussacs-law', f'''
title: Gay-Lussac's Law Calculator (P₁/T₁ = P₂/T₂)
description: Calculate the new pressure or temperature of a gas in a closed, rigid container with Gay-Lussac's law — pressure is proportional to absolute temperature.
category: chemistry
intro: "In a sealed, rigid container the pressure of a gas rises in direct proportion to its absolute temperature. This Gay-Lussac's law calculator finds the final pressure after heating or cooling — or the temperature that produces a given pressure — for gas cylinders, aerosol cans, tyres and sealed vessels."
keywords: [gay lussacs law calculator, p1/t1 = p2/t2, pressure temperature law, gas pressure temperature calculator, amontons law, constant volume gas law, pressure law]
updated: {D}
variables:
  - {{ id: P1, label: Initial pressure (absolute), family: pressure, unit: kPa, imperialUnit: psi, default: 200, min: 0 }}
  - {{ id: T1, label: Initial temperature, family: temperature, unit: C, imperialUnit: F, default: 20, min: 0 }}
  - {{ id: P2, label: Final pressure (absolute), family: pressure, unit: kPa, imperialUnit: psi, min: 0 }}
  - {{ id: T2, label: Final temperature, family: temperature, unit: C, imperialUnit: F, default: 80, min: 0 }}
equations:
  - P1 / T1 = P2 / T2
faq:
  - q: What is Gay-Lussac's law?
    a: At constant volume and amount of gas, pressure is proportional to absolute temperature — P₁ ÷ T₁ = P₂ ÷ T₂. It is also called Amontons's law or the pressure law.
  - q: Must I use absolute pressure?
    a: Yes. Gauge pressure is measured from atmosphere, not from zero, so add atmospheric pressure (about 101.3 kPa) first. Temperatures are converted to kelvin automatically.
  - q: Why do aerosol cans warn against heat?
    a: Pressure rises with absolute temperature. A can at 20 °C heated to 80 °C sees its pressure rise by about 20%, and much more if liquid propellant evaporates.
  - q: How is Gay-Lussac's law different from Charles's law?
    a: Charles's law holds pressure constant and relates volume to temperature; Gay-Lussac's law holds volume constant and relates pressure to temperature.
related: [chemistry/charles-law, chemistry/boyles-law, chemistry/combined-gas-law, physics/ideal-gas-law]
''', f'''
## How to use the Gay-Lussac's law calculator

Enter the **initial absolute pressure** and **temperature**, and the **final temperature**. The calculator gives the final absolute pressure. Enter any three of the four values to solve for the fourth — for example, the temperature at which a vessel reaches its design pressure.

## Gay-Lussac's law formula

<p class="formula">P<sub>1</sub> ÷ T<sub>1</sub> = P<sub>2</sub> ÷ T<sub>2</sub> &nbsp;⇒&nbsp; P<sub>2</sub> = P<sub>1</sub> × T<sub>2</sub> ÷ T<sub>1</sub></p>

Temperatures are absolute (K = °C + 273.15) and pressures absolute.

## Example

A sealed container holds gas at 200 kPa absolute and 20 °C. It is heated to 80 °C:

- T<sub>1</sub> = 293.15 K, T<sub>2</sub> = 353.15 K
- P<sub>2</sub> = 200 × 353.15 ÷ 293.15 = **{gl_P2:.2f} kPa absolute** ({gl_P2-101.325:.1f} kPa gauge)

## Pressure of a gas sealed at 200 kPa(a) and 20 °C

| Temperature | P ÷ P₁ | Absolute pressure | Gauge pressure |
|---|---|---|---|
{gl_rows}
## Notes

- Real gases follow the law well at moderate pressures; near condensation or at very high pressure use a compressibility factor.
- Liquids trapped in a closed pipe behave very differently — thermal expansion of a liquid can raise pressure by several bar per °C, which is why thermal relief valves are fitted.
- To change pressure, volume and temperature together, use the [combined gas law calculator](/chemistry/combined-gas-law/).
''')

# ---------------------------------------------------------------- Avogadro's law
av_V1, av_n1, av_n2 = 6.0, 0.25, 0.40
av_V2 = av_V1 * av_n2 / av_n1; av_Vm = av_V1 / av_n1
conds = [('0 °C, 1 atm (STP, older definition)', 273.15, 101325), ('0 °C, 1 bar (IUPAC STP)', 273.15, 100000),
         ('15 °C, 1 atm', 288.15, 101325), ('20 °C, 1 atm (NTP)', 293.15, 101325), ('25 °C, 1 atm', 298.15, 101325), ('25 °C, 1 bar (SATP)', 298.15, 100000)]
av_rows = ''.join(f"| {nm} | {RGAS*T/P*1000:.3f} L/mol |\n" for nm, T, P in conds)
page('chemistry', 'avogadros-law', f'''
title: Avogadro's Law Calculator (V₁/n₁ = V₂/n₂)
description: Calculate gas volume or moles at constant temperature and pressure with Avogadro's law, plus the molar volume — with a table of molar volumes at STP and NTP.
category: chemistry
intro: "Avogadro's law states that, at the same temperature and pressure, equal volumes of gas contain equal numbers of molecules — so volume is proportional to the amount of gas. This Avogadro's law calculator finds the new volume when moles are added or removed, or the moles in a given volume, and shows the molar volume."
keywords: [avogadros law calculator, v1/n1 = v2/n2, volume and moles of gas, molar volume calculator, avogadro gas law, gas volume moles, 22.4 l per mol]
updated: {D}
variables:
  - {{ id: V1, label: Initial volume, family: volume, unit: L, imperialUnit: ft3, default: 6, min: 0 }}
  - {{ id: n1, label: Initial amount of gas, suffix: mol, default: 0.25, min: 0 }}
  - {{ id: V2, label: Final volume, family: volume, unit: L, imperialUnit: ft3, min: 0 }}
  - {{ id: n2, label: Final amount of gas, suffix: mol, default: 0.40, min: 0 }}
  - {{ id: Vm, label: Molar volume at these conditions, suffix: L/mol, min: 0 }}
equations:
  - V1 / n1 = V2 / n2
  - Vm = V1 / n1 * 1000
faq:
  - q: What is Avogadro's law?
    a: At constant temperature and pressure, the volume of a gas is directly proportional to the number of moles — V₁ ÷ n₁ = V₂ ÷ n₂.
  - q: What is the molar volume of a gas at STP?
    a: 22.414 L/mol at 0 °C and 1 atm, or 22.711 L/mol at 0 °C and 1 bar (the current IUPAC STP). At 25 °C and 1 atm it is about 24.47 L/mol.
  - q: Does Avogadro's law depend on the type of gas?
    a: No. For ideal gases the molar volume is the same for hydrogen, oxygen or carbon dioxide at the same conditions; real gases deviate slightly at high pressure.
  - q: How does Avogadro's law relate to the ideal gas law?
    a: It is the ideal gas law PV = nRT with P and T held constant, so V ÷ n = RT ÷ P is a constant — the molar volume.
related: [physics/ideal-gas-law, chemistry/moles, chemistry/charles-law, chemistry/gay-lussacs-law]
''', f'''
## How to use the Avogadro's law calculator

Enter the **initial volume** and **amount of gas** in moles, and the **final amount**. The calculator gives the final volume at the same temperature and pressure, and the molar volume implied by your first state. Enter any three of the four values to solve for the remaining one.

## Avogadro's law formula

<p class="formula">V<sub>1</sub> ÷ n<sub>1</sub> = V<sub>2</sub> ÷ n<sub>2</sub> &nbsp;⇒&nbsp; V<sub>2</sub> = V<sub>1</sub> × n<sub>2</sub> ÷ n<sub>1</sub></p>

<p class="formula">V<sub>m</sub> = V ÷ n = R T ÷ P</p>

## Example

A balloon holds 6.0 L containing 0.25 mol of gas. Gas is added until it holds 0.40 mol, at the same temperature and pressure:

- V<sub>2</sub> = 6.0 × 0.40 ÷ 0.25 = **{av_V2:.1f} L**
- Molar volume = 6.0 ÷ 0.25 = **{av_Vm:.1f} L/mol** — about room temperature at 1 atm

## Molar volume of an ideal gas

| Conditions | Molar volume |
|---|---|
{av_rows}
Calculated from V<sub>m</sub> = RT ÷ P with R = 8.314462618 J/(mol·K).

## Notes

- Keep temperature and pressure the same in both states; if they change too, use the [ideal gas law calculator](/physics/ideal-gas-law/).
- In gas reactions, volumes combine in the same ratios as moles — 2 L of H₂ reacts with 1 L of O₂.
- Convert grams to moles with the [moles calculator](/chemistry/moles/).
''')

# ---------------------------------------------------------------- Faraday electrolysis
METALS = [('Copper — Cu²⁺', 63.546, 2), ('Silver — Ag⁺', 107.8682, 1), ('Nickel — Ni²⁺', 58.6934, 2), ('Zinc — Zn²⁺', 65.38, 2),
          ('Tin — Sn²⁺', 118.71, 2), ('Iron — Fe²⁺', 55.845, 2), ('Gold — Au⁺ (cyanide bath)', 196.96657, 1),
          ('Chromium — Cr³⁺', 51.9961, 3), ('Aluminium — Al³⁺', 26.9815385, 3), ('Hydrogen gas — 2H⁺', 1.00794, 1)]
fe_opts = ''.join(f"      - {{ label: '{nm} ({M/z:.4f} g/mol per electron)', value: {M/z:.6f} }}\n" for nm, M, z in METALS)
fe_I, fe_th, fe_Me = 2.0, 1.0, 63.546 / 2
fe_Q = fe_I * fe_th * 3600; fe_m = fe_Q * fe_Me / FARADAY; fe_ne = fe_Q / FARADAY
fe_rows = ''.join(f"| {nm} | {M:g} | {z} | {M/z*3600/FARADAY:.4f} g |\n" for nm, M, z in METALS)
page('chemistry', 'faraday-electrolysis', f'''
title: Faraday's Law of Electrolysis Calculator (Mass Deposited)
description: Calculate the mass of metal deposited or dissolved in electrolysis and electroplating from current, time and current efficiency with Faraday's law.
category: chemistry
intro: "Faraday's laws of electrolysis say the mass of a substance deposited at an electrode is proportional to the charge passed and to its molar mass divided by the electrons transferred. This Faraday's law of electrolysis calculator finds the mass plated or dissolved, the charge and moles of electrons — for copper, nickel, silver, zinc, gold and more."
keywords: [faraday electrolysis calculator, faradays law of electrolysis, electroplating calculator, mass deposited electrolysis, m = itm / nf, electrochemical equivalent, plating time calculator]
updated: {D}
variables:
  - {{ id: I, label: Current, family: current, unit: A, default: 2, min: 0 }}
  - {{ id: t, label: Time, family: seconds, unit: h, default: 1, min: 0 }}
  - id: Me
    label: Metal and ion (molar mass ÷ electrons)
    default: {fe_Me:.6f}
    options:
{fe_opts.rstrip()}
  - {{ id: eta, label: Current efficiency, family: percent, unit: '%', default: 100, min: 0, max: 100 }}
  - {{ id: Q, label: Charge passed (coulombs), min: 0 }}
  - {{ id: ne, label: Moles of electrons, suffix: mol, min: 0 }}
  - {{ id: m, label: Mass deposited or dissolved, family: mass, unit: g, imperialUnit: oz, min: 0 }}
equations:
  - Q = I * t
  - ne = Q / 96485.33212
  - m = ne * Me * eta / 1000
faq:
  - q: What is Faraday's law of electrolysis formula?
    a: m = (I × t × M) ÷ (z × F), where I is current, t time in seconds, M molar mass, z the electrons per ion and F = 96,485 C/mol the Faraday constant.
  - q: How much copper does 1 ampere-hour deposit?
    a: About 1.186 g from a Cu²⁺ (acid sulfate) bath at 100% efficiency. Silver deposits about 4.025 g per A·h because it needs only one electron per atom.
  - q: What is current efficiency?
    a: The share of the current that actually deposits the metal. The rest evolves hydrogen or drives side reactions — acid copper and nickel baths run at 95–100%, hard chromium from chromic acid only about 10–25%.
  - q: How do I find the plating time for a given mass?
    a: Clear the time field and enter the target mass. t = m × z × F ÷ (I × M × efficiency).
related: [chemistry/nernst-equation, chemistry/moles, physics/ohms-law, electronics/battery-charge-time]
''', f'''
## How to use the Faraday's law of electrolysis calculator

Enter the **current**, the **time**, the **metal and its ion** (which fixes molar mass ÷ electrons) and the **current efficiency**. The calculator returns the charge passed, the moles of electrons and the mass deposited at the cathode (or dissolved from the anode). Clear the time or current to find how long, or how much current, a target mass needs.

## Faraday's law of electrolysis formula

<p class="formula">m = (I × t × M × η) ÷ (z × F)</p>

<p class="formula">Q = I × t &nbsp;·&nbsp; n<sub>e</sub> = Q ÷ F &nbsp;·&nbsp; F = 96,485.332 C/mol</p>

M ÷ z is the mass deposited per mole of electrons; the chromium option uses Cr³⁺ (z = 3) — decorative and hard chrome plating from chromic acid is Cr(VI), z = 6, which halves the mass per coulomb.

## Example

Copper plating from an acid sulfate (Cu²⁺) bath at 2 A for 1 hour, 100% efficiency:

- Q = 2 × 3,600 = **{fe_Q:,.0f} C**
- n<sub>e</sub> = {fe_Q:,.0f} ÷ 96,485 = **{fe_ne:.5f} mol** of electrons
- m = {fe_ne:.5f} × 63.546 ÷ 2 = **{fe_m:.4f} g** of copper

## Mass deposited per ampere-hour (100% efficiency)

| Metal and ion | Molar mass (g/mol) | Electrons z | Mass per A·h |
|---|---|---|---|
{fe_rows}
## Notes

- Divide the mass by density and plated area for thickness — copper is 8.96 g/cm³, so 2.37 g over 100 cm² is about 2.6 µm.
- Real plating thickness varies across a part; edges and corners plate faster than recesses.
- The same law gives the hydrogen produced by water electrolysis: about 0.0376 g (0.42 L at 0 °C, 1 atm) per ampere-hour.
''')

# ---------------------------------------------------------------- Activation energy from two rates
def Ea_two(k1, k2, T1, T2): return RGAS * math.log(k2 / k1) / (1 / T1 - 1 / T2)
ae_k1, ae_k2, ae_T1, ae_T2 = 0.001, 0.004, 25 + 273.15, 45 + 273.15
ae_Ea = Ea_two(ae_k1, ae_k2, ae_T1, ae_T2)
ae_inv = 1 / ae_T1 - 1 / ae_T2
ae_rows = ''.join(f"| {E} kJ/mol | {math.exp(E*1000/RGAS*(1/298.15-1/308.15)):.2f}× | {math.exp(E*1000/RGAS*(1/298.15-1/348.15)):.1f}× |\n" for E in (20, 40, 50, 60, 80, 100, 150))
page('chemistry', 'activation-energy', f'''
title: Activation Energy Calculator from Two Rate Constants
description: Calculate activation energy (Ea) from rate constants at two temperatures with the two-point Arrhenius equation — or predict the rate at a new temperature.
category: chemistry
intro: "Activation energy is the energy barrier a reaction must overcome, and it controls how sharply the rate rises with temperature. This activation energy calculator uses the two-point form of the Arrhenius equation to find Ea from rate constants (or rates, or reaction times) measured at two temperatures — or the new rate constant once Ea is known."
keywords: [activation energy calculator, ea from two temperatures, two point arrhenius equation, ln k2/k1 calculator, activation energy formula, rate constant temperature, arrhenius two temperatures]
updated: {D}
variables:
  - {{ id: k1, label: Rate constant k₁ at T₁, default: 0.001, min: 0, help: 'Any units — rates or 1/time also work, as long as k₁ and k₂ use the same units.' }}
  - {{ id: T1, label: Temperature T₁, family: temperature, unit: C, imperialUnit: F, default: 25, min: 0 }}
  - {{ id: k2, label: Rate constant k₂ at T₂, default: 0.004, min: 0 }}
  - {{ id: T2, label: Temperature T₂, family: temperature, unit: C, imperialUnit: F, default: 45, min: 0 }}
  - {{ id: r, label: Rate ratio k₂ ÷ k₁, min: 0 }}
  - {{ id: Ea, label: Activation energy (kJ/mol), decimals: 3 }}
equations:
  - r = k2 / k1
  - Ea = 8.314462618 * ln(r) / (1 / T1 - 1 / T2) / 1000
faq:
  - q: How do you calculate activation energy from two temperatures?
    a: Ea = R × ln(k₂ ÷ k₁) ÷ (1/T₁ − 1/T₂), with R = 8.314 J/(mol·K) and temperatures in kelvin. A rate that quadruples from 25 °C to 45 °C gives Ea ≈ 54.7 kJ/mol.
  - q: Can I use reaction times instead of rate constants?
    a: Yes, but invert them — the rate constant is inversely proportional to the time to reach the same conversion, so use k₁ = 1/t₁ and k₂ = 1/t₂.
  - q: Does the old rule "rate doubles every 10 °C" fit?
    a: Only for activation energies around 50 kJ/mol near room temperature — that gives a factor of about 1.9 from 25 to 35 °C. Higher Ea means a steeper rise.
  - q: How do I predict the rate at another temperature?
    a: Enter k₁, T₁, the new T₂ and the activation energy, and clear k₂ and the ratio — the calculator solves k₂ = k₁ × exp[(Ea ÷ R)(1/T₁ − 1/T₂)].
related: [chemistry/arrhenius-equation, chemistry/half-life, chemistry/gibbs-free-energy, chemistry/specific-heat]
''', f'''
## How to use the activation energy calculator

Enter the **rate constant** measured at the first **temperature** and the rate constant at the second temperature. The calculator gives the ratio k₂/k₁ and the **activation energy** in kJ/mol. To predict a rate constant, enter k₁, both temperatures and Ea, and clear k₂ and the ratio.

## Two-point Arrhenius equation

<p class="formula">ln(k<sub>2</sub> ÷ k<sub>1</sub>) = (E<sub>a</sub> ÷ R) × (1/T<sub>1</sub> − 1/T<sub>2</sub>)</p>

<p class="formula">E<sub>a</sub> = R ln(k<sub>2</sub> ÷ k<sub>1</sub>) ÷ (1/T<sub>1</sub> − 1/T<sub>2</sub>)</p>

R = 8.314 J/(mol·K); temperatures must be absolute (kelvin). The pre-exponential factor A cancels, so only the two measurements are needed — use the [Arrhenius equation calculator](/chemistry/arrhenius-equation/) to work with A directly.

## Example

A rate constant rises from 0.0010 at 25 °C to 0.0040 at 45 °C:

- ln(0.0040 ÷ 0.0010) = ln 4 = **{math.log(4):.4f}**
- 1/298.15 − 1/318.15 = **{sci(ae_inv, 4)} K⁻¹**
- E<sub>a</sub> = 8.314 × {math.log(4):.4f} ÷ {sci(ae_inv, 4)} = **{ae_Ea/1000:.2f} kJ/mol**

## How much faster a reaction runs when heated from 25 °C

| Activation energy | 25 → 35 °C | 25 → 75 °C |
|---|---|---|
{ae_rows}
## Notes

- Measure the two rates as far apart in temperature as practical — a small ΔT magnifies measurement error in Ea.
- A curved Arrhenius plot (ln k vs 1/T) means the mechanism changes with temperature; two points will then give only an average Ea.
- Typical values: enzyme reactions 30–60 kJ/mol, many organic reactions 50–100 kJ/mol, diffusion-controlled reactions below 20 kJ/mol.
''')

# ================================================================ ELECTRONICS
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
def nearest_e24(x):
    best = None
    for dec in range(0, 7):
        for b in E24:
            v = round(b * 10**dec, 6)
            if best is None or abs(math.log(v / x)) < abs(math.log(best / x)): best = v
    return best
def ohm(x): return f"{x/1000:g} kΩ" if x >= 1000 else f"{x:g} Ω"

# ---------------------------------------------------------------- LM317
def lm317(R1, R2): return 1.25 * (1 + R2 / R1) + 50e-6 * R2
lm_R1, lm_R2, lm_Vi, lm_IL = 240.0, 715.0, 12.0, 0.5
lm_Vo = lm317(lm_R1, lm_R2); lm_Pd = (lm_Vi - lm_Vo) * lm_IL
lm_rows = ''
for Vt in (1.8, 3.3, 5, 6, 9, 12, 15, 24):
    r2 = 240 * (Vt / 1.25 - 1); e = nearest_e24(r2)
    lm_rows += f"| {Vt:g} V | {r2:.0f} Ω | {ohm(e)} | {lm317(240, e):.2f} V |\n"
page('electronics', 'lm317', f'''
title: LM317 Calculator — Output Voltage, Resistors & Power Dissipation
description: Calculate LM317 output voltage from R1 and R2 (or the R2 for a target voltage), plus dropout headroom and regulator power dissipation.
category: electronics
{intro("The LM317 is an adjustable three-terminal linear regulator that holds 1.25 V between its output and adjust pins, so two resistors set the output voltage. This LM317 calculator finds the output voltage or the R2 value you need, and the heat the regulator must dissipate — see [linear vs switching voltage regulators](ib:linear-vs-switching-voltage-regulators) and [LDO dropout voltage](ib:ldo-regulator-dropout-voltage) for when a linear regulator is the right choice.")}
keywords: [lm317 calculator, lm317 resistor calculator, lm317 output voltage formula, lm317 r1 r2, adjustable voltage regulator calculator, lm317 power dissipation, linear regulator calculator]
updated: {D}
variables:
  - {{ id: R1, label: R1 (output to adjust), family: resistance, unit: ohm, default: 240, min: 0, help: '240 Ω (about 5 mA through the divider) helps meet the minimum load current; 120 Ω is also common.' }}
  - {{ id: R2, label: R2 (adjust to ground), family: resistance, unit: ohm, default: 715, min: 0 }}
  - {{ id: Vi, label: Input voltage, family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: IL, label: Load current, family: current, unit: A, default: 0.5, min: 0 }}
  - {{ id: Vo, label: Output voltage, family: voltage, unit: V, min: 0 }}
  - {{ id: Hd, label: Headroom Vin − Vout (keep ≥ 3 V), family: voltage, unit: V }}
  - {{ id: Pd, label: Regulator power dissipation, family: power, unit: W }}
equations:
  - Vo = 1.25 * (1 + R2 / R1) + 0.00005 * R2
  - Hd = Vi - Vo
  - Pd = Hd * IL
faq:
  - q: What is the LM317 output voltage formula?
    a: Vout = 1.25 V × (1 + R2 ÷ R1) + I_ADJ × R2. I_ADJ is about 50 µA, so the second term adds only a few tens of millivolts with R2 below a few kΩ.
  - q: What R2 do I need for 5 V with R1 = 240 Ω?
    a: R2 = R1 × (Vout ÷ 1.25 − 1) = 240 × 3 = 720 Ω. A 715 Ω (E96) resistor gives about 5.01 V once the adjust current is included.
  - q: What is the LM317 dropout voltage?
    a: The datasheet specifies the LM317 for an input–output difference of 3 V to 40 V; the actual dropout is roughly 1.5–2.5 V depending on load current and temperature. Design for at least 3 V of headroom, or use an LDO.
  - q: How hot will the LM317 get?
    a: It dissipates (Vin − Vout) × I_load. 3.5 W in a TO-220 needs a heat sink — without one, the package's roughly 50 °C/W thermal resistance would push the junction far past its limit.
related: [electronics/heat-sink, electronics/voltage-divider, electronics/zener-resistor, electronics/buck-converter]
''', f'''
## How to use the LM317 calculator

Enter **R1** (between the output and adjust pins) and **R2** (between adjust and ground), plus the **input voltage** and **load current**. The calculator returns the output voltage, the headroom between input and output and the power the regulator turns into heat. To design for a target voltage, clear R2 and enter the output voltage you want.

## LM317 formula

<p class="formula">V<sub>out</sub> = 1.25 V × (1 + R2 ÷ R1) + I<sub>ADJ</sub> × R2</p>

<p class="formula">P<sub>D</sub> = (V<sub>in</sub> − V<sub>out</sub>) × I<sub>load</sub></p>

V<sub>REF</sub> = 1.25 V (1.20–1.30 V between parts) and I<sub>ADJ</sub> ≈ 50 µA typical.

## Example

R1 = 240 Ω, R2 = 715 Ω, 12 V input, 0.5 A load:

- V<sub>out</sub> = 1.25 × (1 + 715 ÷ 240) + 50 µA × 715 = **{lm_Vo:.3f} V**
- Headroom = 12 − {lm_Vo:.3f} = **{lm_Vi-lm_Vo:.2f} V** — comfortably above 3 V
- P<sub>D</sub> = {lm_Vi-lm_Vo:.2f} × 0.5 = **{lm_Pd:.2f} W** — needs a heat sink

## R2 for common output voltages (R1 = 240 Ω)

| Target | Exact R2 | Nearest E24 | Output with E24 R2 |
|---|---|---|---|
{lm_rows}
Output includes the 50 µA adjust current; use 1% resistors, or a trimmer in series with a smaller R2, for precise voltages.

## Design tips

- Fit a 0.1 µF input capacitor near the regulator and at least 1 µF on the output; 10 µF from adjust to ground improves ripple rejection.
- Dropping a large voltage wastes power — a 24 V to 5 V regulator at 1 A turns 19 W into heat. Consider a [buck converter](/electronics/buck-converter/) instead.
- Size the heat sink with the [heat sink calculator](/electronics/heat-sink/) using the P<sub>D</sub> above.
''')

# ---------------------------------------------------------------- Air-core coil (Wheeler)
def wheeler(Dm, lm, N):
    d, l = Dm / 0.0254, lm / 0.0254
    return d * d * N * N / (18 * d + 40 * l) * 1e-6
ac_D, ac_l, ac_N = 0.020, 0.030, 25
ac_L = wheeler(ac_D, ac_l, ac_N); ac_w = ac_N * math.pi * ac_D
ac_rows = ''.join(f"| {D*1000:g} mm | " + ' | '.join(f"{wheeler(D, 0.02, N)*1e6:.3g} µH" for N in (10, 20, 40)) + ' |\n' for D in (0.01, 0.015, 0.02, 0.03, 0.05))
page('electronics', 'air-core-inductor', f'''
title: Air Core Inductor Calculator (Wheeler's Formula)
description: Calculate the inductance of a single-layer air-core coil from diameter, length and number of turns using Wheeler's formula — plus the wire length needed.
category: electronics
{intro("A single-layer air-core coil has no magnetic core to saturate, which makes it the choice for RF tuned circuits, filters and crossovers. This air core inductor calculator uses Wheeler's formula to find the inductance from coil diameter, length and turns, or the turns for a target inductance — background on [how an inductor works](ib:inductor-working-principle).")}
keywords: [air core inductor calculator, wheeler formula calculator, coil inductance calculator, single layer coil inductance, solenoid inductance, number of turns for inductance, rf coil calculator]
updated: {D}
variables:
  - {{ id: D, label: Coil diameter (to wire centre), family: length, unit: mm, imperialUnit: in, default: 20, min: 0 }}
  - {{ id: l, label: Coil length, family: length, unit: mm, imperialUnit: in, default: 30, min: 0 }}
  - {{ id: N, label: Number of turns, default: 25, min: 0 }}
  - {{ id: L, label: Inductance, family: inductance, unit: uH, min: 0 }}
  - {{ id: w, label: Wire length needed (approx.), family: length, unit: m, imperialUnit: ft, min: 0 }}
equations:
  - L = 1e-6 * (D / 0.0254)^2 * N^2 / (18 * (D / 0.0254) + 40 * (l / 0.0254))
  - w = N * pi * D
faq:
  - q: What is Wheeler's formula for an air-core coil?
    a: L (µH) = d² N² ÷ (18 d + 40 l), with the coil diameter d and length l in inches. The calculator converts millimetres for you.
  - q: How accurate is Wheeler's formula?
    a: About 1% for single-layer coils longer than 0.4 times their diameter. Very short coils, multi-layer windings and widely spaced turns need other formulas.
  - q: How do I find the number of turns for a target inductance?
    a: Clear the turns field and enter the inductance you want. Remember that changing the turns at fixed wire size also changes the coil length.
  - q: Why use an air-core inductor?
    a: There is no core loss or saturation, and the inductance stays constant with current and temperature — ideal for RF circuits and audio crossovers, at the cost of larger size for a given inductance.
related: [electronics/inductor-al-value, electronics/resonant-frequency, electronics/reactance, electronics/inductor-energy]
''', f'''
## How to use the air core inductor calculator

Enter the **coil diameter** measured to the centre of the wire, the **winding length** and the **number of turns**. The calculator returns the inductance and the approximate wire length (ignoring leads). Clear the turns to solve for the turns needed for a target inductance.

## Wheeler's formula

<p class="formula">L (µH) = d² N² ÷ (18 d + 40 l) &nbsp;&nbsp;(d, l in inches)</p>

Equivalent to Wheeler's original L = r² N² ÷ (9 r + 10 l) with radius r. Inductance rises with the square of the turns and roughly with the diameter.

## Example

A coil 20 mm in diameter and 30 mm long with 25 turns:

- d = 20 ÷ 25.4 = 0.787 in, l = 30 ÷ 25.4 = 1.181 in
- L = 0.787² × 25² ÷ (18 × 0.787 + 40 × 1.181) = **{ac_L*1e6:.3f} µH**
- Wire length ≈ 25 × π × 20 mm = **{ac_w:.3f} m**

## Inductance of 20 mm long single-layer coils

| Diameter | 10 turns | 20 turns | 40 turns |
|---|---|---|---|
{ac_rows}
Coils shorter than 0.4 × diameter fall outside the formula's 1% range, so treat those rows as estimates.

## Notes

- Spacing the turns lowers inductance slightly but also lowers self-capacitance, raising the self-resonant frequency.
- Check the tuned frequency with the [LC resonant frequency calculator](/electronics/resonant-frequency/).
- For ferrite or powdered-iron cores, use the core's A<sub>L</sub> value in the [inductor A<sub>L</sub> calculator](/electronics/inductor-al-value/).
''')

# ---------------------------------------------------------------- Inductor turns from AL value
al_AL, al_L = 250.0, 150e-6
al_N = math.sqrt(al_L / (al_AL * 1e-9)); al_Nr = math.ceil(al_N - 1e-9); al_La = al_AL * 1e-9 * al_Nr**2
al_rows = ''.join(f"| {AL:g} nH/N² | " + ' | '.join(f"{math.sqrt(Lt/(AL*1e-9)):.1f}" for Lt in (10e-6, 100e-6, 1e-3, 10e-3)) + ' |\n' for AL in (25, 63, 100, 250, 1000, 2500, 5000))
page('electronics', 'inductor-al-value', f'''
title: Inductor AL Value Calculator (Turns for Inductance, L = AL·N²)
description: Calculate the number of turns for a target inductance from a ferrite or powdered-iron core's AL value, or the inductance of a given number of turns.
category: electronics
{intro("Core manufacturers specify an A<sub>L</sub> value — the inductance per turn squared — so the inductance of a wound core is simply L = A<sub>L</sub> × N². This inductor AL value calculator finds the turns needed for a target inductance, rounds them up and shows the inductance you actually get. Watch the current too: a ferrite core [saturates above its rated current](ib:inductor-saturation-current).")}
keywords: [inductor al value calculator, al value turns calculator, ferrite core turns calculator, l = al n2, toroid turns calculator, inductance factor, number of turns for inductance]
updated: {D}
variables:
  - {{ id: AL, label: Core AL value (nH per turn²), default: 250, min: 0, help: 'Read it from the core datasheet. Values in mH per 1000 turns are the same number.' }}
  - {{ id: L, label: Target inductance, family: inductance, unit: uH, default: 150, min: 0 }}
  - {{ id: N, label: Exact turns needed, min: 0, decimals: 3 }}
  - {{ id: Nr, label: Turns to wind (rounded up), min: 0 }}
  - {{ id: La, label: Inductance with rounded turns, family: inductance, unit: uH, min: 0 }}
equations:
  - N = sqrt(L / (AL * 1e-9))
  - Nr = ceil(N)
  - La = AL * 1e-9 * Nr^2
faq:
  - q: How do I calculate turns from the AL value?
    a: N = √(L ÷ A_L). With A_L in nH/N², 150 µH on a 250 nH/N² core needs √(150,000 ÷ 250) = 24.5, so wind 25 turns for 156 µH.
  - q: What is the AL value of a core?
    a: The inductance one turn would have on that core, in nH per turn². It depends on the core material permeability, its size and any air gap.
  - q: Are AL values in nH/N² and mH/1000 turns the same?
    a: Yes. 1,000 turns squared is 10⁶, and 10⁶ nH is 1 mH, so an A_L of 250 nH/N² is also 250 mH per 1,000 turns. Some datasheets use µH per 100 turns instead — 250 nH/N² is 2,500 µH per 100 turns.
  - q: Why is my measured inductance different?
    a: A_L tolerance is often ±25% for ungapped ferrite and ±3–10% for gapped cores, and permeability changes with temperature, frequency and DC bias. Measure and adjust the turns if needed.
related: [electronics/air-core-inductor, electronics/inductor-energy, electronics/buck-converter, electronics/resonant-frequency]
''', f'''
## How to use the inductor AL value calculator

Enter the core's **A<sub>L</sub> value** in nH per turn² and the **target inductance**. The calculator returns the exact turns, the whole number of turns to wind (rounded up) and the inductance those turns give. To find the inductance of an existing winding, clear the target inductance and enter the turns in the exact-turns field.

## AL value formula

<p class="formula">L = A<sub>L</sub> × N² &nbsp;⇒&nbsp; N = √(L ÷ A<sub>L</sub>)</p>

## Example

A ferrite core with A<sub>L</sub> = 250 nH/N² and a target of 150 µH:

- N = √(150 × 10⁻⁶ ÷ 250 × 10⁻⁹) = √600 = **{al_N:.3f} turns**
- Wind **{al_Nr} turns**
- L = 250 nH × {al_Nr}² = **{al_La*1e6:.2f} µH**

## Turns needed for common inductances

| A<sub>L</sub> | 10 µH | 100 µH | 1 mH | 10 mH |
|---|---|---|---|---|
{al_rows}
## Notes

- Gapped cores have a lower A<sub>L</sub> but store more energy before saturating — check peak current against the core's saturation flux.
- Doubling the turns quadruples the inductance; to change L by 10% change the turns by about 5%.
- For coils without a magnetic core, use the [air core inductor calculator](/electronics/air-core-inductor/).
''')

# ---------------------------------------------------------------- Dipole antenna length
def dip(f, k=0.95): lam = C0 / f; return lam, 0.5 * lam * k, 0.25 * lam * k
an_f, an_k = 433.92e6, 0.95
an_lam, an_h, an_q = dip(an_f, an_k)
bands = [('CB radio', 27.185e6), ('2 m amateur', 146e6), ('ISM 433 MHz', 433.92e6), ('LoRa / ISM 868 MHz (EU)', 868e6),
         ('ISM 915 MHz (US)', 915e6), ('GPS L1', 1575.42e6), ('Wi-Fi / Bluetooth 2.4 GHz', 2.44e9), ('Wi-Fi 5 GHz', 5.5e9)]
def _cm(x): return f"{x:.3f} m" if x >= 1 else f"{x*100:.2f} cm"
an_rows = ''.join(f"| {nm} | {f/1e6:g} MHz | {_cm(C0/f)} | {_cm(dip(f)[1])} | {_cm(dip(f)[2])} |\n" for nm, f in bands)
page('electronics', 'antenna-length', f'''
title: Antenna Length Calculator (Half-Wave Dipole & Quarter-Wave)
description: Calculate half-wave dipole and quarter-wave antenna lengths from frequency with a velocity (end-effect) factor — for 433 MHz, 868 MHz, 2.4 GHz and more.
category: electronics
intro: "A resonant antenna is cut to a fraction of the wavelength — half a wavelength for a dipole, a quarter for a ground-plane whip — shortened slightly because of end effects and conductor thickness. This antenna length calculator gives the free-space wavelength and the practical dipole, dipole leg and quarter-wave lengths for any frequency."
keywords: [antenna length calculator, dipole antenna calculator, half wave dipole length, quarter wave antenna length, 433 mhz antenna length, 868 mhz antenna length, 468 / f formula]
updated: {D}
variables:
  - {{ id: f, label: Frequency, family: frequency, unit: MHz, default: 433.92, min: 0 }}
  - {{ id: k, label: Velocity / end-effect factor, default: 0.95, min: 0, max: 1, decimals: 3, help: 'About 0.95 for thin wire dipoles; lower for thick elements or insulated wire.' }}
  - {{ id: lam, label: Free-space wavelength, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: Lh, label: Half-wave dipole (total length), family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: Lg, label: Each dipole leg, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: Lq, label: Quarter-wave monopole / whip, family: length, unit: cm, imperialUnit: in, min: 0 }}
equations:
  - lam = 299792458 / f
  - Lh = 0.5 * lam * k
  - Lg = Lh / 2
  - Lq = 0.25 * lam * k
faq:
  - q: How long should a half-wave dipole be?
    a: About 0.95 × λ ÷ 2. In feet that is the familiar 468 ÷ f (MHz); in metres, 142.5 ÷ f (MHz). At 433.92 MHz that is about 32.8 cm tip to tip.
  - q: How long is a 433 MHz quarter-wave antenna?
    a: About 16.4 cm with a 0.95 factor (17.3 cm for a full free-space quarter wavelength). Trim while watching SWR or range for the best result.
  - q: What does the velocity factor do?
    a: Currents near the ends of a real conductor make it behave electrically longer, so the physical length is a few percent shorter than the free-space fraction of a wavelength. Thicker elements need a lower factor.
  - q: Does a quarter-wave antenna need a ground plane?
    a: Yes. A monopole uses a ground plane (a metal surface, PCB copper or radials about λ/4 long) as the other half of the dipole; without it, performance and matching suffer.
related: [physics/wavelength-frequency, electronics/free-space-path-loss, electronics/resonant-frequency, electronics/dbm-to-watts]
''', f'''
## How to use the antenna length calculator

Enter the **operating frequency** and a **velocity (end-effect) factor** — 0.95 suits a thin bare-wire dipole. The calculator gives the free-space wavelength, the total half-wave dipole length, the length of each dipole leg and the quarter-wave whip or monopole length.

## Antenna length formulas

<p class="formula">λ = c ÷ f &nbsp;·&nbsp; L<sub>dipole</sub> = k × λ ÷ 2 &nbsp;·&nbsp; L<sub>monopole</sub> = k × λ ÷ 4</p>

c = 299,792,458 m/s. With k = 0.95 the dipole formula becomes L (m) = 142.5 ÷ f (MHz), or L (ft) ≈ 468 ÷ f (MHz).

## Example

A dipole for 433.92 MHz with k = 0.95:

- λ = 299,792,458 ÷ 433.92 × 10⁶ = **{an_lam*100:.2f} cm**
- Half-wave dipole = 0.5 × {an_lam*100:.2f} × 0.95 = **{an_h*100:.2f} cm** ({an_h*50:.2f} cm per leg)
- Quarter-wave whip = **{an_q*100:.2f} cm**

## Antenna lengths for common bands (k = 0.95)

| Band | Frequency | Wavelength | Half-wave dipole | Quarter-wave |
|---|---|---|---|---|
{an_rows}
## Notes

- Cut slightly long and trim — it is easier to shorten an antenna than to lengthen it.
- PCB trace antennas and helical or ceramic chip antennas follow their own design notes, not these formulas.
- Estimate the range of the link with the [free-space path loss calculator](/electronics/free-space-path-loss/).
''')

# ---------------------------------------------------------------- Free-space path loss
def fspl(d, f): return 20 * math.log10(4 * math.pi * d * f / C0)
fs_d, fs_f, fs_Pt, fs_Gt, fs_Gr = 2000.0, 868e6, 14.0, 2.0, 2.0
fs_L = fspl(fs_d, fs_f); fs_Pr = fs_Pt + fs_Gt + fs_Gr - fs_L
fs_rows = ''.join(f"| {d/1000:g} km | {fspl(d, 433.92e6):.1f} dB | {fspl(d, 868e6):.1f} dB | {fspl(d, 2.44e9):.1f} dB |\n" for d in (10, 100, 500, 1000, 2000, 5000, 10000, 20000))
fs_rows = fs_rows.replace('| 0.01 km', '| 10 m').replace('| 0.1 km', '| 100 m').replace('| 0.5 km', '| 500 m')
page('electronics', 'free-space-path-loss', f'''
title: Free Space Path Loss Calculator (FSPL in dB) & Link Budget
description: Calculate free-space path loss in dB from distance and frequency, and the received power from transmit power and antenna gains — for LoRa, Wi-Fi and RF links.
category: electronics
{intro("Free-space path loss is how much a radio signal weakens as it spreads out over distance in a clear line of sight. This free space path loss calculator gives the FSPL in dB and a simple link budget — received power from transmit power and antenna gains — for [LoRaWAN sensor networks](ib:lorawan-industrial-iot-guide), [wireless transmitters](ib:wireless-pressure-transmitters-iiot-systems), Wi-Fi and point-to-point links.")}
keywords: [free space path loss calculator, fspl calculator, path loss formula db, link budget calculator, received signal strength calculator, rf path loss, lora range calculator]
updated: {D}
variables:
  - {{ id: d, label: Distance, family: length, unit: km, imperialUnit: mi, default: 2, min: 0 }}
  - {{ id: f, label: Frequency, family: frequency, unit: MHz, default: 868, min: 0 }}
  - {{ id: Pt, label: Transmit power, suffix: dBm, default: 14 }}
  - {{ id: Gt, label: Transmit antenna gain, suffix: dBi, default: 2 }}
  - {{ id: Gr, label: Receive antenna gain, suffix: dBi, default: 2 }}
  - {{ id: L, label: Free-space path loss, suffix: dB, decimals: 2 }}
  - {{ id: Pr, label: Received power, suffix: dBm, decimals: 2 }}
equations:
  - L = 20 * log10(4 * pi * d * f / 299792458)
  - Pr = Pt + Gt + Gr - L
faq:
  - q: What is the free-space path loss formula?
    a: FSPL = 20 log₁₀(4π d f ÷ c). In practical units, FSPL (dB) = 20 log₁₀ d (km) + 20 log₁₀ f (MHz) + 32.44.
  - q: How much does path loss increase with distance?
    a: 6 dB every time the distance doubles, and 20 dB for every tenfold increase. Doubling the frequency also adds 6 dB.
  - q: Why is real-world loss higher than FSPL?
    a: FSPL assumes clear line of sight with an unobstructed Fresnel zone. Walls, terrain, foliage, rain and multipath add tens of dB, so leave a fade margin of 10–20 dB or more.
  - q: How do I check whether a link will work?
    a: Compare the received power with the receiver's sensitivity. For example, LoRa at SF12 can decode about −137 dBm, while Wi-Fi at high data rates needs about −65 to −70 dBm.
related: [electronics/antenna-length, electronics/dbm-to-watts, electronics/snr, physics/wavelength-frequency]
''', f'''
## How to use the free space path loss calculator

Enter the **distance** and **frequency** of the link. The calculator returns the free-space path loss in dB. Add the **transmit power** and both **antenna gains** to get the received power, and compare it with the receiver sensitivity. To find the maximum free-space range, clear the distance and enter the minimum received power.

## Free-space path loss formula

<p class="formula">FSPL = 20 log₁₀(4π d f ÷ c)</p>

<p class="formula">FSPL (dB) = 20 log₁₀ d<sub>km</sub> + 20 log₁₀ f<sub>MHz</sub> + 32.44</p>

<p class="formula">P<sub>r</sub> = P<sub>t</sub> + G<sub>t</sub> + G<sub>r</sub> − FSPL</p>

## Example

A LoRa sensor at 868 MHz, 2 km from the gateway, 14 dBm transmit power and 2 dBi antennas at both ends:

- FSPL = 20 log₁₀(4π × 2000 × 868 × 10⁶ ÷ 299,792,458) = **{fs_L:.2f} dB**
- P<sub>r</sub> = 14 + 2 + 2 − {fs_L:.2f} = **{fs_Pr:.2f} dBm** — far above LoRa sensitivity, leaving a large margin for obstacles

## Free-space path loss by distance and frequency

| Distance | 433.92 MHz | 868 MHz | 2.44 GHz |
|---|---|---|---|
{fs_rows}
## Notes

- FSPL uses isotropic antennas; real antenna gains are added separately in the link budget.
- Keep the first Fresnel zone clear — at 868 MHz over 2 km its radius at mid-path is about {math.sqrt(C0/868e6*1000*1000/2000):.0f} m, so mount antennas high.
- Convert dBm to milliwatts with the [dBm to watts calculator](/electronics/dbm-to-watts/).
''')

# ---------------------------------------------------------------- Shunt resistor
sh_If, sh_Vf, sh_I = 50.0, 0.075, 30.0
sh_R = sh_Vf / sh_If; sh_Pf = sh_Vf * sh_If; sh_V = sh_I * sh_R; sh_P = sh_I**2 * sh_R
sh_rows = ''.join(f"| {I:g} A | {0.075/I*1000:.4g} mΩ | {0.075*I:.3g} W | {0.05/I*1000:.4g} mΩ | {0.05*I:.3g} W |\n" for I in (5, 10, 20, 50, 100, 200, 500, 1000))
page('electronics', 'shunt-resistor', f'''
title: Shunt Resistor Calculator — Resistance, Voltage Drop & Power
description: Calculate current shunt resistance from full-scale current and millivolt rating (75 mV, 50 mV), plus the voltage drop and power at any measured current.
category: electronics
{intro("A current shunt is a precise low-value resistor whose small voltage drop is proportional to the current through it. This shunt resistor calculator finds the resistance for a given full-scale current and millivolt rating, the drop and power at any current, and the reading you should expect — see [shunt resistors in instrumentation](ib:shunt-resistors-in-instrumentation), and [Hall-effect current sensors](ib:hall-effect-current-sensor-acs712) for an isolated alternative.")}
keywords: [shunt resistor calculator, current shunt calculator, 75mv shunt calculator, shunt resistance formula, current sense resistor, ammeter shunt, shunt power dissipation]
updated: {D}
variables:
  - {{ id: If, label: Full-scale (rated) current, family: current, unit: A, default: 50, min: 0 }}
  - {{ id: Vf, label: Full-scale voltage drop, family: voltage, unit: mV, default: 75, min: 0, help: 'Standard ratings: 50, 60, 75 and 100 mV.' }}
  - {{ id: I, label: Measured current, family: current, unit: A, default: 30, min: 0 }}
  - {{ id: R, label: Shunt resistance, family: resistance, unit: mohm, min: 0 }}
  - {{ id: Pf, label: Power at full-scale current, family: power, unit: W, min: 0 }}
  - {{ id: V, label: Voltage drop at measured current, family: voltage, unit: mV, min: 0 }}
  - {{ id: P, label: Power at measured current, family: power, unit: W, min: 0 }}
equations:
  - R = Vf / If
  - Pf = Vf * If
  - V = I * R
  - P = I^2 * R
faq:
  - q: How do I calculate shunt resistance?
    a: R = full-scale voltage ÷ full-scale current. A 50 A, 75 mV shunt is 0.075 ÷ 50 = 1.5 mΩ.
  - q: How do I convert the shunt voltage back to current?
    a: I = V ÷ R. On a 50 A / 75 mV shunt, every 1.5 mV is 1 A — a 45 mV reading means 30 A. Clear the current and enter the measured millivolts.
  - q: How much power does a shunt dissipate?
    a: P = I² R = V × I. The 50 A / 75 mV shunt dissipates 3.75 W at full current. Many manufacturers rate shunts for continuous use at about two-thirds of nameplate current to limit heating and drift.
  - q: Why do shunts have four terminals?
    a: The large terminals carry the current; the small sense screws measure the voltage across the calibrated section only (Kelvin connection), so contact and lead resistance do not add error.
related: [physics/ohms-law, electrical/wire-resistance, electronics/heat-sink, electronics/adc-resolution]
''', f'''
## How to use the shunt resistor calculator

Enter the shunt's **rated current** and **full-scale millivolt drop** (from the nameplate, for example 50 A / 75 mV), and the **current** you are measuring. The calculator returns the shunt resistance, its power at full scale, and the voltage drop and power at your current. To design a current-sense resistor, enter the current and the drop your amplifier or ADC needs.

## Shunt resistor formulas

<p class="formula">R = V<sub>FS</sub> ÷ I<sub>FS</sub> &nbsp;·&nbsp; V = I × R &nbsp;·&nbsp; P = I² × R</p>

## Example

A 50 A / 75 mV DC shunt carrying 30 A:

- R = 0.075 ÷ 50 = **{sh_R*1000:.2f} mΩ**
- Voltage drop = 30 × {sh_R*1000:.2f} mΩ = **{sh_V*1000:.0f} mV**
- Power = 30² × 0.0015 = **{sh_P:.2f} W** (full scale: **{sh_Pf:.2f} W**)

## Resistance and full-scale power of standard shunts

| Rated current | 75 mV shunt | Power at 75 mV | 50 mV shunt | Power at 50 mV |
|---|---|---|---|---|
{sh_rows}
## Notes

- Low-side shunts are easy to read but lift the load's ground; high-side shunts need a current-sense amplifier with enough common-mode range.
- Manganin shunts have a very low temperature coefficient (about 15 ppm/°C), which keeps the reading stable as they warm.
- Check the ADC resolution against the small shunt signal with the [ADC resolution calculator](/electronics/adc-resolution/).
''')

print('done')
