import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
D = '2026-11-02'
G = 9.80665
C0 = 299792458.0         # speed of light, m/s
QE = 1.602176634e-19     # elementary charge, C
NA = 6.02214076e23       # Avogadro constant, 1/mol
MU0 = 1.25663706212e-6   # vacuum permeability, H/m
EPS0 = 8.8541878128e-12  # vacuum permittivity, F/m
SIGMA = 5.670374419e-8   # Stefan–Boltzmann constant, W/(m²·K⁴)
WIEN = 2.897771955e-3    # Wien displacement constant, m·K
WIENF = 5.878925757e10   # Wien frequency constant, Hz/K
U = 1.66053906660e-27    # atomic mass unit, kg
YR = 31557600.0          # Julian year, s

SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
def sci(x, d=3):
    m, e = f"{x:.{d}e}".split('e')
    return f"{m} × 10{str(int(e)).translate(SUP)}"

# ================================================================ PHYSICS

# ---------------------------------------------------------------- Bernoulli equation
be_rho, be_P1, be_v1, be_h1, be_v2, be_h2 = 1000.0, 200000.0, 2.0, 0.0, 5.0, 3.0
be_dyn = 0.5 * be_rho * (be_v1**2 - be_v2**2)
be_hyd = be_rho * G * (be_h1 - be_h2)
be_P2 = be_P1 + be_dyn + be_hyd
be_H1 = be_P1 / (be_rho * G) + be_v1**2 / (2 * G) + be_h1
be_rows = ''.join(f"| {v:g} m/s | {0.5*1000*v**2/1000:.3f} kPa | {v**2/(2*G):.3f} m | {0.5*1.2*v**2:.1f} Pa |\n" for v in (0.5, 1, 2, 3, 5, 10, 20, 30))
page('physics', 'bernoulli-equation', f'''
title: Bernoulli Equation Calculator (Pressure, Velocity & Height)
description: Solve Bernoulli's equation for pressure, velocity or elevation at a second point in a pipe — with total head, velocity head and a worked example.
category: physics
{intro("Bernoulli's equation says that along a streamline the sum of pressure, kinetic energy per volume and potential energy per volume stays constant for a steady, frictionless, incompressible flow. This Bernoulli equation calculator finds the pressure, velocity or height at a second point from conditions at the first — see [Bernoulli's equation and its formula](ib:bernoullis-equation-formula) for the derivation.")}
keywords: [bernoulli equation calculator, bernoulli's principle calculator, bernoulli pressure calculator, total head calculator, velocity head, p1 + 1/2 rho v^2 + rho g h, fluid pressure velocity]
updated: {D}
variables:
  - {{ id: rho, label: Fluid density, family: density, unit: kgm3, imperialUnit: lbft3, default: 1000, min: 0 }}
  - {{ id: P1, label: Pressure at point 1, family: pressure, unit: kPa, imperialUnit: psi, default: 200 }}
  - {{ id: v1, label: Velocity at point 1, family: velocity, unit: ms, imperialUnit: fts, default: 2, min: 0 }}
  - {{ id: h1, label: Elevation of point 1, family: length, unit: m, imperialUnit: ft, default: 0 }}
  - {{ id: v2, label: Velocity at point 2, family: velocity, unit: ms, imperialUnit: fts, default: 5, min: 0 }}
  - {{ id: h2, label: Elevation of point 2, family: length, unit: m, imperialUnit: ft, default: 3 }}
  - {{ id: P2, label: Pressure at point 2, family: pressure, unit: kPa, imperialUnit: psi }}
  - {{ id: H, label: Total head, family: length, unit: m, imperialUnit: ft }}
equations:
  - P2 = P1 + 0.5 * rho * (v1^2 - v2^2) + rho * g0 * (h1 - h2)
  - H = P1 / (rho * g0) + v1^2 / (2 * g0) + h1
faq:
  - q: What is Bernoulli's equation?
    a: P + ½ρv² + ρgh = constant along a streamline. P is static pressure, ½ρv² the dynamic pressure and ρgh the hydrostatic term, all in pascals (J/m³).
  - q: Why does pressure drop when velocity increases?
    a: Energy is conserved. If the fluid speeds up through a narrower section, its kinetic energy rises, so its pressure energy must fall — the principle behind venturi meters, carburettors and aspirators.
  - q: When is Bernoulli's equation not valid?
    a: It assumes steady, incompressible, inviscid flow with no pumps or turbines between the points. For real pipes add the friction head loss, and for gases above about Mach 0.3 use compressible-flow relations.
  - q: What is total head?
    a: The Bernoulli sum expressed as a height of fluid — pressure head P/ρg plus velocity head v²/2g plus elevation z. Without losses it is the same at every point.
related: [engineering/venturi-flow, engineering/pitot-tube-velocity, engineering/darcy-weisbach-head-loss, physics/pressure]
''', f'''
## How to use the Bernoulli equation calculator

Enter the **fluid density**, the **pressure**, **velocity** and **elevation** at point 1, and the velocity and elevation at point 2. The calculator returns the pressure at point 2 and the total head of the flow. To find a velocity or height instead, enter P2 and clear the field you want. Use absolute or gauge pressure consistently at both points.

## Bernoulli equation formula

<p class="formula">P<sub>1</sub> + ½ρv<sub>1</sub>² + ρgh<sub>1</sub> = P<sub>2</sub> + ½ρv<sub>2</sub>² + ρgh<sub>2</sub></p>

<p class="formula">H = P ÷ (ρg) + v² ÷ (2g) + h</p>

## Example

Water (1,000 kg/m³) flows at 2 m/s and 200 kPa at ground level, then rises 3 m into a narrower pipe where it moves at 5 m/s:

- Velocity term: ½ × 1000 × (2² − 5²) = **−{abs(be_dyn)/1000:.1f} kPa**
- Elevation term: 1000 × 9.80665 × (0 − 3) = **−{abs(be_hyd)/1000:.2f} kPa**
- P<sub>2</sub> = 200 − 10.5 − 29.42 = **{be_P2/1000:.2f} kPa**
- Total head H = {be_P1/(be_rho*G):.3f} + {be_v1**2/(2*G):.3f} + 0 = **{be_H1:.3f} m**

## Dynamic pressure and velocity head

| Velocity | Dynamic pressure (water) | Velocity head v²/2g | Dynamic pressure (air, 1.2 kg/m³) |
|---|---|---|---|
{be_rows}
## Practical notes

- Real pipe flow loses head to friction and fittings: P<sub>2</sub> is lower than this ideal value by ρg·h<sub>L</sub>. Estimate h<sub>L</sub> with the [Darcy–Weisbach calculator](/engineering/darcy-weisbach-head-loss/).
- Flow meters such as the [venturi](/engineering/venturi-flow/) and the [pitot tube](/engineering/pitot-tube-velocity/) are direct applications of Bernoulli's equation.
- If P<sub>2</sub> falls below the liquid's vapour pressure, the liquid flashes or cavitates and the equation no longer applies.
''')

# ---------------------------------------------------------------- Lift force
lf_rho, lf_v, lf_S, lf_CL = 1.225, 50.0, 16.0, 0.5
lf_L = 0.5 * lf_rho * lf_v**2 * lf_S * lf_CL
def isa_rho(h): return 1.225 * (1 - 2.25577e-5 * h) ** 4.25588
lf_rows = ''.join(f"| {h:,} m | {isa_rho(h):.4f} kg/m³ | {isa_rho(h)/1.225*100:.1f}% | {0.5*isa_rho(h)*lf_v**2*lf_S*lf_CL/1000:.2f} kN | {math.sqrt(1.225/isa_rho(h))*lf_v:.1f} m/s |\n"
                  for h in (0, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000))
page('physics', 'lift-force', f'''
title: Lift Force Calculator (Lift Equation L = ½ρv²SC_L)
description: Calculate aerodynamic lift force from air density, airspeed, wing area and lift coefficient — or the speed needed to lift a given mass.
category: physics
intro: "The lift equation relates the upward force on a wing to air density, the square of airspeed, wing area and a lift coefficient that captures the wing's shape and angle of attack. This lift force calculator gives the lift in newtons and the mass it can support, and can solve backwards for the take-off speed or wing area you need."
keywords: [lift force calculator, lift equation calculator, lift coefficient calculator, wing lift calculator, aerodynamic lift formula, l = 1/2 rho v^2 s cl, takeoff speed calculator]
updated: {D}
variables:
  - {{ id: rho, label: Air density, family: density, unit: kgm3, imperialUnit: lbft3, default: 1.225, min: 0, help: '1.225 kg/m³ is sea-level standard air at 15 °C.' }}
  - {{ id: v, label: Airspeed, family: velocity, unit: ms, imperialUnit: kn, default: 50, min: 0 }}
  - {{ id: S, label: Wing area, family: area, unit: m2, imperialUnit: ft2, default: 16, min: 0 }}
  - {{ id: CL, label: Lift coefficient (C_L), default: 0.5, min: 0 }}
  - {{ id: L, label: Lift force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: m, label: Mass that can be supported, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - L = 0.5 * rho * v^2 * S * CL
  - m = L / g0
faq:
  - q: What is the lift equation?
    a: L = ½ ρ v² S C_L, where ρ is air density, v the true airspeed, S the wing area and C_L the lift coefficient. Doubling the speed quadruples the lift.
  - q: What is a typical lift coefficient?
    a: Cruise values are about 0.3–0.6. A clean wing reaches a maximum of roughly 1.2–1.6 just before stalling, and flaps raise C_L,max to about 2–3.
  - q: How do I find the take-off or stall speed?
    a: Set the lift equal to the weight and solve v = √(2mg ÷ (ρ S C_L,max)). Enter the mass, clear the airspeed field and the calculator solves for it.
  - q: Why do aircraft need longer runways at high altitude?
    a: Thinner air means less lift at the same speed, so the aircraft must reach a higher true airspeed — about 16% higher at 3,000 m — before it can lift off.
related: [physics/drag-force, physics/bernoulli-equation, physics/density, physics/weight]
''', f'''
## How to use the lift force calculator

Enter the **air density**, the **airspeed**, the **wing (reference) area** and the **lift coefficient**. The calculator returns the lift force and the mass that lift can hold up against gravity. To find the speed needed to fly, enter the mass and clear the airspeed. The same equation works for hydrofoils — use water's density.

## Lift equation

<p class="formula">L = ½ ρ v² S C<sub>L</sub> &nbsp;·&nbsp; m = L ÷ g</p>

## Example

A light aircraft with 16 m² of wing flies at 50 m/s (97 knots) in sea-level air with C<sub>L</sub> = 0.5:

- L = 0.5 × 1.225 × 50² × 16 × 0.5 = **{lf_L:,.0f} N**
- Mass supported = {lf_L:,.0f} ÷ 9.80665 = **{lf_L/G:,.0f} kg**

## Air density and lift with altitude (ISA)

Same wing, speed and C<sub>L</sub> as the example; the last column is the true airspeed that restores sea-level lift.

| Altitude | Density | % of sea level | Lift at 50 m/s | Speed for equal lift |
|---|---|---|---|---|
{lf_rows}
Densities follow the International Standard Atmosphere troposphere model; hot days reduce density further.

## Notes

- C<sub>L</sub> rises roughly linearly with angle of attack (about 0.1 per degree for a typical wing) until the stall.
- Lift always comes with induced drag; estimate the parasitic part with the [drag force calculator](/physics/drag-force/).
- Use true airspeed, not indicated airspeed, with the actual air density.
''')

# ---------------------------------------------------------------- Liquid thermal expansion
le_b, le_V0, le_T1, le_T2 = 950.0, 1000.0, 15.0, 35.0
le_dV = le_b * 1e-6 * le_V0 * (le_T2 - le_T1)
liq = [('Water (at 20 °C)', 207), ('Mercury', 181), ('Glycerine', 505), ('Petrol (gasoline)', 950), ('Kerosene / jet fuel', 990), ('Ethanol', 1090), ('Acetone', 1430)]
le_rows = ''.join(f"| {nm} | {b:g} | {b*1e-6*1000*10:.2f} L | {b*1e-6*1000*20:.2f} L | {b*1e-6*1000*40:.2f} L |\n" for nm, b in liq)
page('physics', 'liquid-thermal-expansion', f'''
title: Liquid Thermal Expansion Calculator (Volumetric)
description: Calculate how much a liquid's volume increases when heated, using the volumetric expansion coefficient β — for fuel, water, oil and solvent tanks.
category: physics
intro: "Liquids expand far more than solids when heated, which is why fuel tanks, hot-water systems and closed pipelines need expansion space or thermal relief valves. This liquid thermal expansion calculator applies ΔV = β V₀ ΔT to find the volume change, the final volume and the percentage increase."
keywords: [liquid thermal expansion calculator, volumetric expansion calculator, coefficient of volume expansion, fuel expansion calculator, water expansion calculator, delta v = beta v delta t, volume expansion formula]
updated: {D}
variables:
  - {{ id: b, label: Volumetric expansion coefficient β (×10⁻⁶ per K), default: 950, min: 0, help: 'Petrol ≈ 950, water at 20 °C ≈ 207, ethanol ≈ 1090. See the table below.' }}
  - {{ id: V0, label: Initial volume, family: volume, unit: L, imperialUnit: galUS, default: 1000, min: 0 }}
  - {{ id: T1, label: Initial temperature, family: temperature, unit: C, imperialUnit: F, default: 15 }}
  - {{ id: T2, label: Final temperature, family: temperature, unit: C, imperialUnit: F, default: 35 }}
  - {{ id: dV, label: Volume increase, family: volume, unit: L, imperialUnit: galUS }}
  - {{ id: V1, label: Final volume, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: pct, label: Percentage increase, family: percent, unit: '%' }}
equations:
  - dV = b * 1e-6 * V0 * (T2 - T1)
  - V1 = V0 + dV
  - pct = b * 1e-6 * (T2 - T1)
faq:
  - q: What is the formula for thermal expansion of a liquid?
    a: ΔV = β × V₀ × ΔT, where β is the volumetric expansion coefficient (per K), V₀ the initial volume and ΔT the temperature rise. The final volume is V₀ (1 + β ΔT).
  - q: How much does petrol expand when it warms up?
    a: About 0.095% per °C. 1,000 L delivered at 15 °C becomes about 1,019 L at 35 °C, which is why fuel is traded at a reference temperature of 15 °C.
  - q: Why does water expand differently?
    a: Water's β changes strongly with temperature — it is zero at 4 °C (maximum density), about 207 × 10⁻⁶/K at 20 °C and about 750 × 10⁻⁶/K near 100 °C. For large temperature changes use densities from a steam table instead of a single β.
  - q: Does the container expansion matter?
    a: Yes. A steel tank's volume grows by about 3α ≈ 36 × 10⁻⁶ per K, so the apparent expansion of the liquid is β − 3α. For most liquids this is a small correction.
related: [engineering/thermal-expansion, physics/density, engineering/vertical-tank-volume, physics/latent-heat]
''', f'''
## How to use the liquid thermal expansion calculator

Enter the liquid's **volumetric expansion coefficient β** in units of 10⁻⁶ per kelvin, the **initial volume** and the **initial and final temperatures**. The calculator returns the volume increase, the final volume and the percentage change. A negative result means the liquid contracts on cooling.

## Volumetric expansion formula

<p class="formula">ΔV = β × V<sub>0</sub> × (T<sub>2</sub> − T<sub>1</sub>) &nbsp;·&nbsp; V<sub>1</sub> = V<sub>0</sub> + ΔV</p>

## Example

A tank is filled with 1,000 L of petrol at 15 °C, which then warms to 35 °C in the sun (β = 950 × 10⁻⁶/K):

- ΔT = 35 − 15 = 20 K
- ΔV = 950 × 10⁻⁶ × 1000 × 20 = **{le_dV:.1f} L**
- Final volume = **{le_V0+le_dV:,.0f} L**, an increase of **{le_dV/le_V0*100:.1f}%**

## Expansion coefficients and volume change per 1,000 L

| Liquid | β (×10⁻⁶/K, near 20 °C) | ΔT = 10 K | ΔT = 20 K | ΔT = 40 K |
|---|---|---|---|---|
{le_rows}
Coefficients are typical values near room temperature; they vary with temperature and composition.

## Why it matters

- **Blocked-in liquid**: a full, closed pipe that warms up builds pressure very quickly because liquids are nearly incompressible — fit a thermal relief valve.
- **Tank ullage**: leave enough free space for the expansion over the full storage temperature range.
- **Custody transfer**: fuel volumes are corrected to 15 °C (or 60 °F) using expansion tables.
- For solids (pipes, rails), use the linear [thermal expansion calculator](/engineering/thermal-expansion/).
''')

# ---------------------------------------------------------------- Stefan–Boltzmann law
sb_eps, sb_A, sb_T, sb_Ts = 0.9, 1.0, 100.0, 20.0
sb_TK, sb_TsK = sb_T + 273.15, sb_Ts + 273.15
sb_E = sb_eps * SIGMA * sb_TK**4
sb_P = sb_E * sb_A
sb_Pn = sb_eps * SIGMA * sb_A * (sb_TK**4 - sb_TsK**4)
sb_rows = ''.join(f"| {t:,} °C | {t+273.15:,.2f} K | {SIGMA*(t+273.15)**4:,.1f} W/m² | {0.9*SIGMA*((t+273.15)**4-293.15**4):,.0f} W/m² |\n"
                  for t in (0, 50, 100, 200, 300, 500, 800, 1000, 1500))
page('physics', 'stefan-boltzmann-law', f'''
title: Stefan–Boltzmann Law Calculator (Radiation Heat Transfer)
description: Calculate thermal radiation power from a surface with the Stefan–Boltzmann law, and the net radiant heat exchange with its surroundings.
category: physics
intro: "Every surface above absolute zero radiates energy in proportion to the fourth power of its absolute temperature. This Stefan–Boltzmann law calculator gives the emitted power, the radiant flux per square metre and the net radiation heat transfer between a hot surface and cooler surroundings."
keywords: [stefan boltzmann law calculator, radiation heat transfer calculator, thermal radiation calculator, emissive power calculator, q = εσa(t⁴ − ts⁴), black body radiation power, emissivity calculator]
updated: {D}
variables:
  - {{ id: eps, label: Emissivity (ε), default: 0.9, min: 0, max: 1, help: '1 for a black body; about 0.9 for paint, 0.05 for polished aluminium.' }}
  - {{ id: A, label: Surface area, family: area, unit: m2, imperialUnit: ft2, default: 1, min: 0 }}
  - {{ id: T, label: Surface temperature, family: temperature, unit: C, imperialUnit: F, default: 100 }}
  - {{ id: Ts, label: Surroundings temperature, family: temperature, unit: C, imperialUnit: F, default: 20 }}
  - {{ id: E, label: Emitted flux (εσT⁴), suffix: W/m², min: 0 }}
  - {{ id: P, label: Total power emitted, family: power, unit: W, imperialUnit: BTUh, min: 0 }}
  - {{ id: Pn, label: Net radiation heat loss, family: power, unit: W, imperialUnit: BTUh }}
equations:
  - E = eps * 5.670374419e-8 * T^4
  - P = E * A
  - Pn = eps * 5.670374419e-8 * A * (T^4 - Ts^4)
faq:
  - q: What is the Stefan–Boltzmann law?
    a: The power radiated by a surface is P = ε σ A T⁴, where σ = 5.670 × 10⁻⁸ W/(m²·K⁴), ε is the emissivity and T the absolute temperature in kelvin.
  - q: How do I calculate net radiation heat transfer?
    a: For a small object inside large surroundings, Q = ε σ A (T⁴ − T_s⁴). The object also absorbs radiation from its surroundings, so only the difference is lost.
  - q: Why must temperatures be in kelvin?
    a: The law uses absolute temperature raised to the fourth power. The calculator converts °C or °F to kelvin for you.
  - q: When is radiation more important than convection?
    a: At high temperatures. Near room temperature a painted surface loses heat by radiation and by natural convection at similar rates (each roughly 5 W/m²·K), but radiation grows with T⁴ and dominates in furnaces and above a few hundred °C.
related: [physics/heat-conduction, physics/newtons-law-of-cooling, physics/wiens-law, engineering/heat-duty]
''', f'''
## How to use the Stefan–Boltzmann law calculator

Enter the surface's **emissivity**, its **area**, its **temperature** and the **temperature of the surroundings**. The calculator returns the radiant flux, the total power the surface emits and the net heat it loses by radiation once the radiation it absorbs from the surroundings is subtracted. A negative net value means the surface is gaining heat.

## Stefan–Boltzmann formula

<p class="formula">P = ε σ A T⁴ &nbsp;·&nbsp; Q<sub>net</sub> = ε σ A (T⁴ − T<sub>s</sub>⁴)</p>

σ = 5.670374419 × 10⁻⁸ W/(m²·K⁴), with T in kelvin.

## Example

A painted steel surface (ε = 0.9) of 1 m² at 100 °C in a room at 20 °C:

- T = 373.15 K, T<sub>s</sub> = 293.15 K
- Emitted: 0.9 × 5.670 × 10⁻⁸ × 373.15⁴ = **{sb_P:.1f} W**
- Net loss: 0.9 × 5.670 × 10⁻⁸ × 1 × (373.15⁴ − 293.15⁴) = **{sb_Pn:.1f} W**

## Radiation from a surface vs temperature

Black-body flux σT⁴ and the net loss of an ε = 0.9 surface to 20 °C surroundings, per square metre:

| Surface temperature | Absolute | Black-body flux | Net loss (ε = 0.9) |
|---|---|---|---|
{sb_rows}
## Typical emissivities

| Surface | ε |
|---|---|
| Polished aluminium / silver | 0.03–0.05 |
| Galvanised steel (new) | 0.2–0.3 |
| Oxidised steel | 0.8 |
| Paint (any colour), brick, concrete | 0.9–0.95 |
| Water, human skin | 0.95–0.98 |

The wavelength at which a hot body radiates most is given by [Wien's law](/physics/wiens-law/).
''')

# ---------------------------------------------------------------- Wien's displacement law
wi_T = 5778.0
wi_l = WIEN / wi_T * 1e9
wi_f = WIENF * wi_T / 1e12
objs = [('Liquid nitrogen', 77), ('Ice / water at 0 °C', 273.15), ('Human body', 310.15), ('Boiling water', 373.15), ('Red-hot iron', 1000),
        ('Incandescent filament', 2800), ('Red dwarf star', 3200), ('Sun (photosphere)', 5778), ('Sirius A', 9940)]
def band(nm):
    if nm < 380: return 'Ultraviolet'
    if nm <= 750: return 'Visible'
    if nm < 3000: return 'Near infrared'
    if nm < 50000: return 'Infrared'
    return 'Far infrared'
wi_rows = ''.join(f"| {nm} | {t:,.0f} K | {WIEN/t*1e9:,.0f} nm ({WIEN/t*1e6:.3g} µm) | {band(WIEN/t*1e9)} |\n" for nm, t in objs)
page('physics', 'wiens-law', f'''
title: Wien's Law Calculator (Peak Wavelength from Temperature)
description: Find the peak wavelength of black-body radiation from temperature with Wien's displacement law — or estimate a star's or hot object's temperature.
category: physics
intro: "Wien's displacement law says the wavelength at which a black body radiates most strongly is inversely proportional to its absolute temperature. This Wien's law calculator gives the peak wavelength and peak frequency for any temperature, and solves backwards to estimate temperature from the colour of a star or a glowing object."
keywords: [wiens law calculator, wien's displacement law calculator, peak wavelength calculator, black body peak wavelength, lambda max = b / t, star temperature from wavelength, wien constant]
updated: {D}
variables:
  - {{ id: T, label: Temperature, family: temperature, unit: K, imperialUnit: F, default: 5778, min: 0 }}
  - {{ id: lam, label: Peak wavelength (λ_max), suffix: nm, min: 0 }}
  - {{ id: lum, label: Peak wavelength in micrometres, suffix: µm, min: 0 }}
  - {{ id: fp, label: Peak frequency (per unit frequency), suffix: THz, min: 0 }}
equations:
  - lam = 2897771.955 / T
  - lum = lam / 1000
  - fp = 0.05878925757 * T
faq:
  - q: What is Wien's displacement law?
    a: λ_max = b ÷ T, with b = 2.897771955 × 10⁻³ m·K. A body at 5,778 K (the Sun) peaks at about 501 nm; one at 310 K (a person) peaks at about 9.3 µm in the infrared.
  - q: How do I find a star's temperature from its peak wavelength?
    a: T = b ÷ λ_max. Enter the peak wavelength in nanometres and clear the temperature field — a peak at 290 nm means about 10,000 K.
  - q: Why don't the peak wavelength and peak frequency match?
    a: They describe the spectrum per unit wavelength and per unit frequency, which have different shapes. The frequency peak, ν_max = 5.879 × 10¹⁰ Hz/K × T, corresponds to a wavelength about 1.76 times longer than λ_max.
  - q: Why do infrared thermometers work at 8–14 µm?
    a: Objects near room temperature radiate most strongly around 10 µm, and the atmosphere is transparent in the 8–14 µm window.
related: [physics/stefan-boltzmann-law, physics/photon-energy, physics/wavelength-frequency, physics/doppler-effect]
''', f'''
## How to use the Wien's law calculator

Enter the **temperature** of the radiating body (switch the unit to °C or °F if you prefer). The calculator returns the peak wavelength in nanometres and micrometres and the peak frequency of the spectrum. To estimate a temperature, enter the peak wavelength and clear the temperature field.

## Wien's displacement law formula

<p class="formula">λ<sub>max</sub> = b ÷ T &nbsp;·&nbsp; b = 2.897771955 × 10⁻³ m·K</p>

<p class="formula">ν<sub>max</sub> = 5.878925757 × 10¹⁰ Hz/K × T</p>

## Example

The Sun's photosphere is about 5,778 K:

- λ<sub>max</sub> = 2.897772 × 10⁻³ ÷ 5778 = **{wi_l:.1f} nm** (blue-green light)
- ν<sub>max</sub> = 5.879 × 10¹⁰ × 5778 = **{wi_f:.1f} THz** — a wavelength of {C0/(wi_f*1e12)*1e9:.0f} nm in the per-frequency spectrum

## Peak wavelength of common sources

| Source | Temperature | Peak wavelength | Band |
|---|---|---|---|
{wi_rows}
## Notes

- Only ideal black bodies follow the law exactly; real surfaces have emissivity below 1, but their peak position is usually close.
- The total power radiated rises with T⁴ — see the [Stefan–Boltzmann law calculator](/physics/stefan-boltzmann-law/).
- To convert the peak wavelength to photon energy, use the [photon energy calculator](/physics/photon-energy/).
''')

# ---------------------------------------------------------------- E = mc²
mc_m = 0.001
mc_E = mc_m * C0**2
parts = [('Electron', 9.1093837015e-31), ('Proton', 1.67262192369e-27), ('Neutron', 1.67492749804e-27), ('Atomic mass unit (1 u)', U)]
mc_prow = ''.join(f"| {nm} | {sci(mm, 4)} kg | {mm*C0**2/QE/1e6:,.3f} MeV |\n" for nm, mm in parts)
ens = [('1 kWh of electricity', 3.6e6), ('1 kg of petrol burned (≈ 46 MJ)', 46e6), ('1 tonne of TNT', 4.184e9), ('1 kg of U-235 fully fissioned (≈ 8.2 × 10¹³ J)', 8.2e13)]
mc_erow = ''.join(f"| {nm} | {sci(e, 3)} J | {sci(e/C0**2, 3)} kg |\n" for nm, e in ens)
page('physics', 'mass-energy-equivalence', f'''
title: E = mc² Calculator (Mass–Energy Equivalence)
description: Convert mass to energy with Einstein's E = mc² — in joules, kWh and tonnes of TNT — or find the mass equivalent of any amount of energy.
category: physics
intro: "Einstein's equation E = mc² says that mass and energy are two forms of the same thing, linked by the square of the speed of light. This E = mc² calculator converts a mass into its rest energy in joules, kilowatt-hours and TNT equivalent, and works backwards to find the tiny mass change behind chemical and nuclear energy."
keywords: [e=mc2 calculator, mass energy equivalence calculator, mass to energy calculator, einstein equation calculator, rest energy calculator, energy to mass calculator, e = mc squared]
updated: {D}
variables:
  - {{ id: m, label: Mass, family: mass, unit: g, imperialUnit: oz, default: 1, min: 0 }}
  - {{ id: E, label: Energy (E = mc²), family: energy, unit: kWh, min: 0 }}
  - {{ id: Ej, label: Energy in terajoules, suffix: TJ, min: 0 }}
  - {{ id: tnt, label: TNT equivalent, suffix: kilotonnes, min: 0 }}
equations:
  - E = m * 299792458^2
  - Ej = E / 1e12
  - tnt = E / 4.184e12
faq:
  - q: How much energy is in 1 gram of mass?
    a: E = 0.001 kg × (299,792,458 m/s)² ≈ 8.99 × 10¹³ J — about 25 million kWh, or 21.5 kilotonnes of TNT.
  - q: Does burning fuel convert mass into energy?
    a: Yes, but the mass change is tiny. Burning 1 kg of petrol releases about 46 MJ, which corresponds to only about 5 × 10⁻¹⁰ kg of mass.
  - q: How much mass is converted in a nuclear reactor?
    a: Fission of uranium-235 converts roughly 0.09% of the fuel's mass into energy, millions of times more per kilogram than chemical reactions.
  - q: What units does E = mc² use?
    a: With mass in kilograms and c in metres per second, energy comes out in joules. The calculator converts grams, ounces and other units automatically.
related: [physics/photon-energy, physics/kinetic-energy, physics/de-broglie-wavelength, physics/radioactive-activity]
''', f'''
## How to use the E = mc² calculator

Enter a **mass** in grams, kilograms or another unit. The calculator returns the equivalent rest energy in kWh (switch to J, MJ or BTU), in terajoules and in kilotonnes of TNT. To find the mass equivalent of an energy, enter the energy and clear the mass field.

## Mass–energy equivalence formula

<p class="formula">E = m c² &nbsp;·&nbsp; c = 299,792,458 m/s</p>

## Example

Converting 1 gram of mass entirely into energy:

- E = 0.001 × 299,792,458² = **{sci(mc_E, 4)} J**
- = **{mc_E/3.6e6:,.0f} kWh** ({mc_E/3.6e12:.2f} GWh)
- = **{mc_E/4.184e12:.2f} kilotonnes of TNT**

## Rest energy of particles

| Particle | Mass | Rest energy |
|---|---|---|
{mc_prow}
## Mass equivalent of everyday energies

| Energy source | Energy | Equivalent mass |
|---|---|---|
{mc_erow}
## Notes

- 1 kilotonne of TNT is defined as 4.184 × 10¹² J.
- In nuclear reactions the energy released equals the mass defect × c²; in radioactive decay this energy is carried by the emitted particles — see the [radioactive activity calculator](/physics/radioactive-activity/).
''')

# ---------------------------------------------------------------- Radioactive activity
ra_m, ra_M, ra_th, ra_t = 1e-6, 59.9338, 5.2714, 10.0
ra_lam = math.log(2) / (ra_th * YR)
ra_N = ra_m * 1000 / ra_M * NA
ra_A = ra_lam * ra_N
ra_At = ra_A * 2 ** (-ra_t / ra_th)
iso = [('Cobalt-60', 59.9338, 5.2714 * YR), ('Caesium-137', 136.9071, 30.08 * YR), ('Strontium-90', 89.9077, 28.79 * YR),
       ('Americium-241', 241.0568, 432.6 * YR), ('Radium-226', 226.0254, 1600 * YR), ('Carbon-14', 14.0032, 5700 * YR),
       ('Iodine-131', 130.9061, 8.0252 * 86400), ('Technetium-99m', 98.9063, 6.0067 * 3600), ('Uranium-238', 238.0508, 4.468e9 * YR)]
def ci_g(M, ts): return math.log(2) / ts * NA / M / 3.7e10
def hl(ts):
    if ts < 86400 * 2: return f"{ts/3600:.4g} h"
    if ts < YR: return f"{ts/86400:.4g} d"
    return f"{ts/YR:,.5g} y"
ra_rows = ''.join(f"| {nm} | {hl(ts)} | {sci(ci_g(M, ts)*3.7e10, 3)} Bq/g | {ci_g(M, ts):.3g} Ci/g |\n" for nm, M, ts in iso)
page('physics', 'radioactive-activity', f'''
title: Radioactive Activity Calculator (Bq & Ci from Mass)
description: Calculate the activity of a radioactive sample in becquerels and curies from its mass, molar mass and half-life — and the activity left after time.
category: physics
{intro("Activity is the number of nuclei that decay per second, A = λN, and is measured in becquerels (Bq) or curies (Ci). This radioactive activity calculator works out the decay constant, the number of atoms and the activity of a sample from its mass and half-life, plus how much activity remains later — useful for the sealed Cs-137 and Co-60 sources used in [nuclear level measurement](ib:types-of-nuclear-level-measurement).")}
keywords: [radioactive activity calculator, becquerel calculator, curie calculator, specific activity calculator, a = lambda n, decay constant calculator, activity from half life]
updated: {D}
variables:
  - {{ id: m, label: Mass of the radionuclide, family: mass, unit: mg, default: 1, min: 0 }}
  - {{ id: M, label: Molar mass (g/mol), default: 59.9338, min: 0, help: 'Close to the mass number: Co-60 = 59.93, Cs-137 = 136.91, Am-241 = 241.06.' }}
  - {{ id: th, label: Half-life, family: time, unit: yr, default: 5.2714, min: 0 }}
  - {{ id: t, label: Elapsed time, family: time, unit: yr, default: 10, min: 0 }}
  - {{ id: lam, label: Decay constant (λ), suffix: 1/s, min: 0 }}
  - {{ id: N, label: Number of atoms, min: 0 }}
  - {{ id: A0, label: Activity now, suffix: Bq, min: 0 }}
  - {{ id: Ci, label: Activity now in curies, suffix: Ci, min: 0 }}
  - {{ id: At, label: Activity after elapsed time, suffix: Bq, min: 0 }}
  - {{ id: Cit, label: Activity after elapsed time in curies, suffix: Ci, min: 0 }}
equations:
  - lam = ln(2) / (th * 31557600)
  - N = m * 1000 / M * 6.02214076e23
  - A0 = lam * N
  - Ci = A0 / 3.7e10
  - At = A0 * 2^(-t / th)
  - Cit = At / 3.7e10
faq:
  - q: How do you calculate radioactive activity?
    a: A = λN, with the decay constant λ = ln 2 ÷ t½ (in seconds) and the number of atoms N = (mass ÷ molar mass) × Avogadro's number. The result is in becquerels.
  - q: What is the difference between a becquerel and a curie?
    a: 1 Bq is one decay per second. 1 Ci = 3.7 × 10¹⁰ Bq, originally the activity of 1 g of radium-226, so 1 mCi = 37 MBq.
  - q: How does activity change with time?
    a: It halves every half-life, A(t) = A₀ × 2^(−t/t½). After 10 half-lives about 0.1% of the original activity is left.
  - q: What is specific activity?
    a: Activity per unit mass, usually Bq/g or Ci/g. Short half-lives give high specific activity — 1 g of Co-60 is about 1,100 Ci, while 1 g of U-238 is only 12 kBq.
related: [chemistry/half-life, physics/mass-energy-equivalence, chemistry/moles, physics/photon-energy]
''', f'''
## How to use the radioactive activity calculator

Enter the **mass** of the radioactive isotope itself (not the whole source capsule), its **molar mass**, its **half-life** and, optionally, an **elapsed time**. The calculator returns the decay constant, the number of atoms and the activity now and after that time, in becquerels and curies. To find the mass of isotope in a source of known activity, enter the activity and clear the mass field.

## Activity formula

<p class="formula">λ = ln 2 ÷ t<sub>½</sub> &nbsp;·&nbsp; N = (m ÷ M) × N<sub>A</sub> &nbsp;·&nbsp; A = λN</p>

<p class="formula">A(t) = A<sub>0</sub> × 2<sup>−t/t½</sup> &nbsp;·&nbsp; 1 Ci = 3.7 × 10¹⁰ Bq</p>

## Example

1 mg of cobalt-60 (M = 59.9338 g/mol, t<sub>½</sub> = 5.2714 years):

- λ = 0.693147 ÷ (5.2714 × 31,557,600 s) = **{sci(ra_lam, 4)} s⁻¹**
- N = 0.001 ÷ 59.9338 × 6.022 × 10²³ = **{sci(ra_N, 4)} atoms**
- A = λN = **{sci(ra_A, 4)} Bq** = **{ra_A/3.7e10:.3f} Ci**
- After 10 years: A = {sci(ra_A, 4)} × 2<sup>−10/5.2714</sup> = **{sci(ra_At, 4)} Bq** ({ra_At/3.7e10:.3f} Ci)

## Specific activity of common radionuclides

| Isotope | Half-life | Specific activity | Ci per gram |
|---|---|---|---|
{ra_rows}
Specific activity here is for the pure isotope; real sources contain carrier material and encapsulation.

## Notes

- The half-life field accepts years, days, hours, minutes or seconds.
- Activity alone does not give dose — that also depends on the radiation type, its energy, distance and shielding.
- For half-life arithmetic without atoms or masses, use the [half-life calculator](/chemistry/half-life/).
''')

# ---------------------------------------------------------------- Magnetic field (wire & solenoid)
mf_I, mf_r, mf_N, mf_Ls, mf_mur = 10.0, 0.010, 500, 0.10, 1.0
mf_Bw = MU0 * mf_I / (2 * math.pi * mf_r)
mf_Bs = MU0 * mf_mur * mf_N * mf_I / mf_Ls
mf_H = mf_N * mf_I / mf_Ls
mf_rows = ''.join(f"| {r*1000:g} mm | {MU0*1/(2*math.pi*r)*1e6:,.2f} µT | {MU0*10/(2*math.pi*r)*1e6:,.1f} µT | {MU0*100/(2*math.pi*r)*1e6:,.0f} µT | {MU0*1000/(2*math.pi*r)*1e6:,.0f} µT |\n"
                  for r in (0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0))
page('physics', 'magnetic-field', f'''
title: Magnetic Field Calculator (Straight Wire & Solenoid)
description: Calculate the magnetic flux density B around a straight current-carrying wire and inside a solenoid coil, plus the field strength H in A/m.
category: physics
{intro("An electric current creates a magnetic field: it circles a straight wire and becomes strong and uniform inside a coil. This magnetic field calculator gives the flux density around a long straight conductor and inside a solenoid — the same field that pulls the plunger in a [solenoid valve](ib:solenoid-valve-working-principle) and that a [Hall-effect sensor](ib:how-a-hall-effect-sensor-works) measures.")}
keywords: [magnetic field calculator, magnetic field of a wire calculator, solenoid magnetic field calculator, b = mu0 i / 2 pi r, b = mu0 n i / l, flux density calculator, ampere's law calculator]
updated: {D}
variables:
  - {{ id: I, label: Current, family: current, unit: A, default: 10, min: 0 }}
  - {{ id: r, label: Distance from the wire, family: length, unit: mm, imperialUnit: in, default: 10, min: 0 }}
  - {{ id: N, label: Number of turns (solenoid), default: 500, min: 0 }}
  - {{ id: Ls, label: Solenoid length, family: length, unit: cm, imperialUnit: in, default: 10, min: 0 }}
  - {{ id: mur, label: Relative permeability of the core (μr), default: 1, min: 0, help: '1 for an air core. A closed iron core can be 1,000 or more but saturates near 1.5–2 T.' }}
  - {{ id: Bw, label: Field around the wire, suffix: mT, min: 0 }}
  - {{ id: Bs, label: Field inside the solenoid, suffix: mT, min: 0 }}
  - {{ id: H, label: Field strength inside the solenoid (H), suffix: A/m, min: 0 }}
equations:
  - Bw = 1.25663706212e-6 * I / (2 * pi * r) * 1000
  - Bs = 1.25663706212e-6 * mur * N * I / Ls * 1000
  - H = N * I / Ls
faq:
  - q: What is the magnetic field around a straight wire?
    a: B = μ₀ I ÷ (2π r), with μ₀ = 4π × 10⁻⁷ H/m. A 10 A current gives 0.2 mT (200 µT) at 10 mm — about four times the Earth's field.
  - q: What is the magnetic field inside a solenoid?
    a: B = μ₀ μr N I ÷ L for a long coil (length much greater than diameter). 500 turns on a 10 cm air-core coil with 10 A give about 62.8 mT.
  - q: How do I convert tesla to gauss?
    a: 1 T = 10,000 G, so 1 mT = 10 G and 1 µT = 0.01 G. The Earth's field is about 25–65 µT (0.25–0.65 G).
  - q: Why is the field at the end of a solenoid weaker?
    a: At each open end of a long solenoid the flux density drops to about half the central value, because the field lines spread out.
related: [physics/lorentz-force, physics/faradays-law, electronics/air-core-inductor, physics/coulombs-law]
''', f'''
## How to use the magnetic field calculator

For a **straight wire**, enter the **current** and the **distance** from the conductor's centre. For a **solenoid**, enter the same current, the **number of turns**, the **coil length** and the **relative permeability** of the core. The calculator returns both flux densities in millitesla and the solenoid's field strength H.

## Magnetic field formulas

<p class="formula">Straight wire: B = μ<sub>0</sub> I ÷ (2π r)</p>

<p class="formula">Solenoid: B = μ<sub>0</sub> μ<sub>r</sub> N I ÷ L &nbsp;·&nbsp; H = N I ÷ L</p>

μ<sub>0</sub> = 1.25663706212 × 10⁻⁶ H/m (≈ 4π × 10⁻⁷).

## Example

10 A flowing in a long straight wire, measured 10 mm away; and the same current through a 500-turn, 10 cm air-core solenoid:

- Wire: B = 1.2566 × 10⁻⁶ × 10 ÷ (2π × 0.01) = **{mf_Bw*1000:.3f} mT** ({mf_Bw*1e6:.0f} µT)
- Solenoid: H = 500 × 10 ÷ 0.1 = **{mf_H:,.0f} A/m**
- Solenoid: B = 1.2566 × 10⁻⁶ × 500 × 10 ÷ 0.1 = **{mf_Bs*1000:.2f} mT**

## Field around a straight wire

| Distance | 1 A | 10 A | 100 A | 1,000 A |
|---|---|---|---|---|
{mf_rows}
For comparison, the Earth's magnetic field is about 50 µT and a fridge magnet about 5–10 mT.

## Notes

- The wire formula assumes a long, straight conductor and a point outside it. Inside a round conductor, B rises linearly from zero at the centre.
- The field of two conductors carrying equal and opposite currents (a cable's live and neutral) largely cancels, which is why twisted pairs pick up little interference.
- The force on a conductor or a moving charge in this field is given by the [Lorentz force calculator](/physics/lorentz-force/).
''')

# ---------------------------------------------------------------- Lorentz force
lo_z, lo_v, lo_B, lo_th, lo_mu, lo_I, lo_Lc = 1, 2e6, 0.5, 90.0, 1.007276, 5.0, 0.2
lo_mass = lo_mu * U
lo_F = abs(lo_z) * QE * lo_v * lo_B * math.sin(math.radians(lo_th))
lo_r = lo_mass * lo_v * math.sin(math.radians(lo_th)) / (abs(lo_z) * QE * lo_B)
lo_f = abs(lo_z) * QE * lo_B / (2 * math.pi * lo_mass)
lo_Fc = lo_B * lo_I * lo_Lc * math.sin(math.radians(lo_th))
pt = [('Electron', -1, 0.000548579909), ('Proton', 1, 1.007276467), ('Alpha particle', 2, 4.001506179), ('Deuteron', 1, 2.013553213)]
lo_rows = ''.join(f"| {nm} | {z:+d} | {abs(z)*QE*1/(2*math.pi*mu*U)/1e6:,.4g} MHz | {mu*U*1e6/(abs(z)*QE*1)*1000:,.4g} mm |\n" for nm, z, mu in pt)
page('physics', 'lorentz-force', f'''
title: Lorentz Force Calculator (F = qvB & F = BIL)
description: Calculate the magnetic Lorentz force on a moving charge (F = qvB sin θ), its radius of curvature and cyclotron frequency, and the force on a wire.
category: physics
intro: "A charged particle moving through a magnetic field feels a force at right angles to both its velocity and the field, and a current-carrying wire feels the same force — the principle behind electric motors, loudspeakers and mass spectrometers. This Lorentz force calculator gives the force on a moving charge, the radius of its circular path and its cyclotron frequency, plus the force on a conductor."
keywords: [lorentz force calculator, magnetic force calculator, f = qvb calculator, force on a moving charge, force on current carrying wire, f = bil calculator, cyclotron frequency calculator, gyroradius calculator]
updated: {D}
variables:
  - {{ id: z, label: Charge number (multiples of e), default: 1, help: '+1 for a proton, −1 for an electron, +2 for an alpha particle.' }}
  - {{ id: v, label: Particle speed, family: velocity, unit: ms, default: 2000000, min: 0 }}
  - {{ id: B, label: Magnetic flux density, suffix: T, default: 0.5, min: 0 }}
  - {{ id: th, label: Angle between velocity (or current) and field, family: angle, unit: deg, default: 90 }}
  - {{ id: mu, label: Particle mass (atomic mass units), suffix: u, default: 1.007276, min: 0, help: 'Proton 1.007276 u, electron 0.00054858 u, alpha 4.001506 u.' }}
  - {{ id: I, label: Current in a conductor, family: current, unit: A, default: 5, min: 0 }}
  - {{ id: Lc, label: Conductor length in the field, family: length, unit: m, imperialUnit: in, default: 0.2, min: 0 }}
  - {{ id: F, label: Force on the charge, family: force, unit: N, min: 0 }}
  - {{ id: r, label: Radius of the circular path, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: fc, label: Cyclotron frequency, family: frequency, unit: MHz, min: 0 }}
  - {{ id: Fc, label: Force on the conductor (F = BIL sin θ), family: force, unit: N, imperialUnit: lbf }}
equations:
  - F = abs(z) * 1.602176634e-19 * v * B * sin(th)
  - r = mu * 1.66053906660e-27 * v * sin(th) / (abs(z) * 1.602176634e-19 * B)
  - fc = abs(z) * 1.602176634e-19 * B / (2 * pi * mu * 1.66053906660e-27)
  - Fc = B * I * Lc * sin(th)
faq:
  - q: What is the Lorentz force formula?
    a: F = q(E + v × B). With no electric field the magnitude is F = |q| v B sin θ, where θ is the angle between the velocity and the magnetic field.
  - q: What is the force on a current-carrying wire?
    a: F = B I L sin θ. A 0.2 m conductor carrying 5 A at right angles to a 0.5 T field feels 0.5 N — the basic force in every electric motor.
  - q: Why do charged particles move in circles in a magnetic field?
    a: The magnetic force is always perpendicular to the velocity, so it changes the direction but not the speed. The radius is r = m v⊥ ÷ (|q| B).
  - q: Which way does the force act?
    a: Use the right-hand rule for positive charges (or conventional current) — fingers along v, curl towards B, thumb gives F. The force on an electron is in the opposite direction.
related: [physics/magnetic-field, physics/faradays-law, physics/centripetal-force, physics/coulombs-law]
''', f'''
## How to use the Lorentz force calculator

For a **moving charge**, enter its **charge number**, **speed**, **mass** in atomic mass units, the **magnetic flux density** and the **angle** between velocity and field. You get the force, the radius of the circular (or helical) path and the cyclotron frequency. For a **wire**, enter the **current** and the **length** inside the field; the same B and angle are used.

## Lorentz force formulas

<p class="formula">F = |q| v B sin θ &nbsp;·&nbsp; r = m v sin θ ÷ (|q| B) &nbsp;·&nbsp; f<sub>c</sub> = |q| B ÷ (2π m)</p>

<p class="formula">Conductor: F = B I L sin θ</p>

## Example

A proton (1.007276 u, charge +e) moving at 2 × 10⁶ m/s at right angles to a 0.5 T field:

- F = 1.602 × 10⁻¹⁹ × 2 × 10⁶ × 0.5 = **{sci(lo_F, 4)} N**
- r = 1.6726 × 10⁻²⁷ × 2 × 10⁶ ÷ (1.602 × 10⁻¹⁹ × 0.5) = **{lo_r*1000:.2f} mm**
- f<sub>c</sub> = **{lo_f/1e6:.3f} MHz**

A 0.2 m wire carrying 5 A across the same field: F = 0.5 × 5 × 0.2 = **{lo_Fc:.2f} N**.

## Cyclotron frequency and radius in a 1 T field

The radius column is for a speed of 10⁶ m/s perpendicular to the field.

| Particle | Charge | Cyclotron frequency | Radius at 10⁶ m/s |
|---|---|---|---|
{lo_rows}
## Notes

- The formulas are non-relativistic; above about 10% of the speed of light use the relativistic momentum γmv.
- A velocity component parallel to B is unaffected, so the particle spirals along the field lines.
- Find the field of a coil or wire first with the [magnetic field calculator](/physics/magnetic-field/).
''')

# ---------------------------------------------------------------- Faraday's law
fa_N, fa_A, fa_B1, fa_B2, fa_dt, fa_R = 200, 0.005, 0.0, 0.4, 0.020, 10.0
fa_dPhi = fa_A * (fa_B2 - fa_B1)
fa_emf = fa_N * abs(fa_dPhi) / fa_dt
fa_rows = ''.join(f"| {N} | {N*0.001/0.01:g} V | {N*0.001/0.1:g} V | {N*0.001/1:g} V |\n" for N in (1, 10, 50, 100, 500, 1000))
page('physics', 'faradays-law', f'''
title: Faraday's Law Calculator (Induced EMF)
description: Calculate the EMF induced in a coil by a changing magnetic flux with Faraday's law, ε = N ΔΦ/Δt — plus the flux change and induced current.
category: physics
{intro("Faraday's law of induction says that a changing magnetic flux through a coil induces a voltage proportional to the number of turns and the rate of change. This Faraday's law calculator works out the change in flux, the average induced EMF and the resulting current — see [Faraday's law of electromagnetic induction](ib:faradays-law-electromagnetic-induction) and [Lenz's law](ib:lenzs-law-electromagnetic-induction) for the direction of the induced current.")}
keywords: [faradays law calculator, induced emf calculator, electromagnetic induction calculator, emf = n dphi/dt, magnetic flux calculator, induced voltage in a coil, lenz's law]
updated: {D}
variables:
  - {{ id: N, label: Number of turns, default: 200, min: 0 }}
  - {{ id: A, label: Coil area, family: area, unit: cm2, imperialUnit: in2, default: 50, min: 0 }}
  - {{ id: B1, label: Initial flux density, suffix: T, default: 0 }}
  - {{ id: B2, label: Final flux density, suffix: T, default: 0.4 }}
  - {{ id: dt, label: Time for the change, family: seconds, unit: ms, default: 20, min: 0 }}
  - {{ id: R, label: Circuit resistance, family: resistance, unit: ohm, default: 10, min: 0 }}
  - {{ id: dPhi, label: Change in flux (ΔΦ), suffix: Wb }}
  - {{ id: emf, label: Average induced EMF, family: voltage, unit: V, min: 0 }}
  - {{ id: Ii, label: Induced current, family: current, unit: A, min: 0 }}
equations:
  - dPhi = A * (B2 - B1)
  - emf = N * abs(dPhi) / dt
  - Ii = emf / R
faq:
  - q: What is Faraday's law?
    a: The induced EMF equals the rate of change of magnetic flux linkage, ε = −N dΦ/dt. The minus sign (Lenz's law) means the induced current opposes the change that caused it.
  - q: What is magnetic flux?
    a: Φ = B × A × cos θ, in webers (1 Wb = 1 T·m²), where θ is the angle between the field and the normal to the coil. This calculator assumes the field is perpendicular to the coil (cos θ = 1).
  - q: How can I increase the induced voltage?
    a: Use more turns, a larger coil area, a stronger field or a faster change. Doubling any one of them doubles the EMF.
  - q: What about a conductor moving through a field?
    a: A straight conductor of length L moving at speed v across a field B has a motional EMF ε = B L v — the same law applied to the area it sweeps.
related: [physics/magnetic-field, physics/lorentz-force, electronics/inductor-energy, electrical/transformer-turns-ratio]
''', f'''
## How to use the Faraday's law calculator

Enter the coil's **number of turns** and **area**, the **initial** and **final** magnetic flux density through it, the **time** over which the change happens and the **resistance** of the circuit. The calculator returns the change in flux, the average induced EMF (magnitude) and the current that flows.

## Faraday's law formula

<p class="formula">ε = −N × ΔΦ ÷ Δt &nbsp;·&nbsp; ΔΦ = A × (B<sub>2</sub> − B<sub>1</sub>) &nbsp;·&nbsp; I = ε ÷ R</p>

## Example

A 200-turn coil of 50 cm² is placed in a field that rises from 0 to 0.4 T in 20 ms; the circuit resistance is 10 Ω:

- ΔΦ = 0.005 m² × 0.4 T = **{fa_dPhi:.4f} Wb**
- ε = 200 × {fa_dPhi:.4f} ÷ 0.02 = **{fa_emf:.0f} V**
- I = {fa_emf:.0f} ÷ 10 = **{fa_emf/fa_R:.0f} A**

## Induced EMF for a 1 mWb flux change

| Turns | in 10 ms | in 100 ms | in 1 s |
|---|---|---|---|
{fa_rows}
## Where Faraday's law is used

- **Generators and alternators**: a rotating coil sees a sinusoidal flux, giving an EMF of N Φ<sub>max</sub> ω.
- **Transformers**: the same changing flux links both windings, so the voltages divide in the turns ratio — see the [transformer turns ratio calculator](/electrical/transformer-turns-ratio/).
- **Magnetic flow meters**: a conducting liquid moving through a magnetic field produces a voltage proportional to its velocity (ε = B D v).
- **Inductive kick**: switching off a coil collapses its flux quickly and induces a large voltage spike.
''')

# ---------------------------------------------------------------- Parallel-plate capacitor
pp_er, pp_A, pp_d, pp_V = 1.0, 0.01, 0.001, 100.0
pp_C = EPS0 * pp_er * pp_A / pp_d
diel = [('Vacuum / air', 1.0), ('PTFE (Teflon)', 2.1), ('Polypropylene', 2.2), ('Paper (dry)', 3.5), ('FR-4 PCB laminate', 4.4), ('Glass', 6), ('Mica', 6.5), ('Water (20 °C)', 80)]
pp_rows = ''.join(f"| {nm} | {er:g} | {EPS0*er*pp_A/pp_d*1e12:,.1f} pF |\n" for nm, er in diel)
page('physics', 'parallel-plate-capacitor', f'''
title: Parallel Plate Capacitor Calculator (C = ε₀εrA/d)
description: Calculate the capacitance of a parallel plate capacitor from plate area, gap and dielectric constant — plus stored charge, energy and electric field.
category: physics
{intro("Two conducting plates separated by an insulator form a capacitor whose value depends only on the plate area, the gap and the permittivity of the material between them. This parallel plate capacitor calculator gives the capacitance, charge, stored energy and electric field — see [what capacitance is](ib:what-is-capacitance), and how the same principle is used in [capacitance level measurement](ib:capacitance-level-measurement).")}
keywords: [parallel plate capacitor calculator, capacitance calculator, c = e0 er a / d, dielectric constant calculator, plate capacitor formula, capacitance of two plates, electric field between plates]
updated: {D}
variables:
  - {{ id: er, label: Relative permittivity (dielectric constant εr), default: 1, min: 0 }}
  - {{ id: A, label: Plate area (overlap), family: area, unit: cm2, imperialUnit: in2, default: 100, min: 0 }}
  - {{ id: d, label: Plate separation, family: length, unit: mm, imperialUnit: in, default: 1, min: 0 }}
  - {{ id: V, label: Applied voltage, family: voltage, unit: V, default: 100, min: 0 }}
  - {{ id: C, label: Capacitance, family: capacitance, unit: pF, min: 0 }}
  - {{ id: Q, label: Stored charge, suffix: nC, min: 0 }}
  - {{ id: W, label: Stored energy, suffix: µJ, min: 0 }}
  - {{ id: Ef, label: Electric field between the plates, suffix: kV/mm, min: 0 }}
equations:
  - C = 8.8541878128e-12 * er * A / d
  - Q = C * V * 1e9
  - W = 0.5 * C * V^2 * 1e6
  - Ef = V / d / 1e6
faq:
  - q: What is the formula for a parallel plate capacitor?
    a: C = ε₀ εr A ÷ d, with ε₀ = 8.854 × 10⁻¹² F/m, A the overlapping plate area in m² and d the gap in metres. 100 cm² plates 1 mm apart in air give 88.5 pF.
  - q: How does the dielectric change the capacitance?
    a: Capacitance is multiplied by the relative permittivity εr. Filling the same gap with FR-4 (εr ≈ 4.4) gives about 390 pF instead of 88.5 pF.
  - q: What limits the voltage of a capacitor?
    a: The dielectric strength. Dry air breaks down at about 3 kV/mm, so a 1 mm air gap arcs at around 3 kV; good film dielectrics withstand hundreds of kV/mm.
  - q: Does the formula include fringing?
    a: No. It assumes the gap is small compared with the plate size. Fringing fields at the edges add a little extra capacitance when the gap is not small.
related: [electronics/capacitor-energy, electronics/capacitors-series-parallel, physics/coulombs-law, electronics/reactance]
''', f'''
## How to use the parallel plate capacitor calculator

Enter the **dielectric constant** of the material between the plates (1 for air), the **overlapping plate area**, the **separation** and the **applied voltage**. The calculator returns the capacitance, the charge on each plate, the stored energy and the electric field in the gap. To design for a target value, enter the capacitance and clear the area or the gap.

## Parallel plate capacitor formulas

<p class="formula">C = ε<sub>0</sub> ε<sub>r</sub> A ÷ d &nbsp;·&nbsp; Q = C V &nbsp;·&nbsp; W = ½ C V² &nbsp;·&nbsp; E = V ÷ d</p>

ε<sub>0</sub> = 8.8541878128 × 10⁻¹² F/m.

## Example

Two 100 cm² plates 1 mm apart in air, charged to 100 V:

- C = 8.854 × 10⁻¹² × 1 × 0.01 ÷ 0.001 = **{pp_C*1e12:.2f} pF**
- Q = {pp_C*1e12:.2f} pF × 100 V = **{pp_C*pp_V*1e9:.3f} nC**
- W = ½ × {pp_C*1e12:.2f} pF × 100² = **{0.5*pp_C*pp_V**2*1e6:.4f} µJ**
- E = 100 V ÷ 1 mm = **{pp_V/pp_d/1e6:.1f} kV/mm** — well below air's breakdown of about 3 kV/mm

## Capacitance with different dielectrics

Same plates as the example (100 cm², 1 mm gap):

| Dielectric | εr | Capacitance |
|---|---|---|
{pp_rows}
Dielectric constants are typical values; they vary with frequency, temperature and grade.

## Applications

- **Capacitive level probes** measure the change in capacitance as a liquid with higher εr replaces air between a probe and the tank wall.
- **Touch sensors and proximity switches** detect the extra capacitance of a finger or object.
- **PCB planes**: a power–ground plane pair 0.2 mm apart in FR-4 gives about 19 pF per cm².
''')

# ================================================================ ELECTRICAL

# ---------------------------------------------------------------- Capacitor bank kVAr ↔ µF
cb_Q, cb_V, cb_f = 50.0, 415.0, 50.0
cb_w = 2 * math.pi * cb_f
cb_Cd = cb_Q * 1000 / (3 * cb_w * cb_V**2)
cb_Cs = cb_Q * 1000 / (cb_w * cb_V**2)
cb_I = cb_Q * 1000 / (math.sqrt(3) * cb_V)
cb_rows = ''.join(f"| {q:g} kVAr | {q*1000/(3*cb_w*415**2)*1e6:,.1f} µF | {q*1000/(cb_w*415**2)*1e6:,.1f} µF | {q*1000/(math.sqrt(3)*415):,.1f} A |\n" for q in (5, 10, 25, 50, 75, 100, 150, 200))
cb_der = ''.join(f"| {vr:g} V | {vs:g} V | {(vs/vr)**2*100:.1f}% | {50*(vs/vr)**2:.1f} kVAr |\n" for vr, vs in ((415, 400), (440, 415), (440, 400), (480, 415), (525, 415), (480, 440)))
page('electrical', 'capacitor-bank-kvar', f'''
title: Capacitor Bank kVAr to µF Calculator (3-Phase)
description: Convert capacitor bank kVAr to microfarads per phase for delta or star connection, and find the line current — or the kVAr of a given capacitance.
category: electrical
{intro("Power factor correction capacitors are rated in kVAr, but the capacitance inside each phase is what you measure and replace. This capacitor bank kVAr calculator converts between kVAr and µF for delta and star banks and gives the line current — see [how to calculate capacitor bank kVAr](ib:how-to-calculate-capacitor-bank-kvar-formula) and the guide to [capacitor bank sizing for power factor correction](ib:capacitor-bank-sizing-power-factor-correction).")}
keywords: [capacitor bank kvar calculator, kvar to uf calculator, kvar to microfarad, capacitor bank current calculator, uf to kvar, delta capacitor bank capacitance, power factor capacitor calculation]
updated: {D}
variables:
  - {{ id: Q, label: Bank rating, suffix: kVAr, default: 50, min: 0 }}
  - {{ id: V, label: Line voltage, family: voltage, unit: V, default: 415, min: 0 }}
  - {{ id: f, label: Supply frequency, family: frequency, unit: Hz, default: 50, min: 0 }}
  - id: k
    label: Connection
    default: 3
    options:
      - {{ label: 'Delta (capacitor sees line voltage)', value: 3 }}
      - {{ label: 'Star / wye (capacitor sees phase voltage)', value: 1 }}
  - {{ id: C, label: Capacitance per phase, family: capacitance, unit: uF, min: 0 }}
  - {{ id: I, label: Line current, family: current, unit: A, min: 0 }}
  - {{ id: Xc, label: Reactance per capacitor, family: resistance, unit: ohm, min: 0 }}
equations:
  - C = Q * 1000 / (k * 2 * pi * f * V^2)
  - I = Q * 1000 / (sqrt(3) * V)
  - Xc = 1 / (2 * pi * f * C)
faq:
  - q: How do I convert kVAr to µF?
    a: For a delta bank, C per phase = Q ÷ (3 × 2πf × V_L²). A 50 kVAr bank at 415 V, 50 Hz needs about 308 µF in each phase. For a star bank, C = Q ÷ (2πf × V_L²), three times larger.
  - q: How do I calculate capacitor bank current?
    a: I = Q ÷ (√3 × V_L) for a three-phase bank. 50 kVAr at 415 V draws about 69.6 A per line, whether it is delta or star connected.
  - q: What happens if a 440 V capacitor runs at 415 V?
    a: Its output falls with the square of voltage — (415 ÷ 440)² = 89%, so a 50 kVAr unit delivers about 44.5 kVAr. Over-rating the voltage is common to allow for harmonics and overvoltage.
  - q: How do I find kVAr from a measured capacitance?
    a: Enter the measured µF per phase and clear the kVAr field. A drop of more than about 5–10% from nameplate usually means the capacitor should be replaced.
related: [electrical/power-factor-correction, electrical/kva-to-kw, electronics/reactance, electrical/thd]
''', f'''
## How to use the capacitor bank kVAr calculator

Enter the bank's **kVAr rating**, the **line voltage** it is connected to, the **frequency** and whether the capacitors are connected in **delta** or **star**. The calculator returns the capacitance needed in each phase, the line current and the reactance of each capacitor. To work out the kVAr of an existing bank, enter the measured µF per phase and clear the kVAr field.

## kVAr to µF formulas

<p class="formula">Delta: C = Q ÷ (3 × 2πf × V<sub>L</sub>²) &nbsp;·&nbsp; Star: C = Q ÷ (2πf × V<sub>L</sub>²)</p>

<p class="formula">I<sub>L</sub> = Q ÷ (√3 × V<sub>L</sub>) &nbsp;·&nbsp; X<sub>C</sub> = 1 ÷ (2πf C)</p>

For a single-phase capacitor, C = Q ÷ (2πf × V²) and I = Q ÷ V.

## Example

A 50 kVAr delta-connected bank on a 415 V, 50 Hz supply:

- C = 50,000 ÷ (3 × 314.16 × 415²) = **{cb_Cd*1e6:.1f} µF** per phase (a star bank would need {cb_Cs*1e6:.1f} µF)
- I = 50,000 ÷ (1.732 × 415) = **{cb_I:.1f} A**
- X<sub>C</sub> = 1 ÷ (314.16 × {cb_Cd*1e6:.1f} µF) = **{1/(cb_w*cb_Cd):.2f} Ω**

## Capacitance and current at 415 V, 50 Hz

| Bank rating | µF per phase (delta) | µF per phase (star) | Line current |
|---|---|---|---|
{cb_rows}
## Output at reduced voltage

Capacitor output varies with V². For a bank rated 50 kVAr at its rated voltage:

| Rated voltage | Supply voltage | Output | Actual kVAr |
|---|---|---|---|
{cb_der}
## Practical notes

- Size cables and switchgear for about 1.3–1.5 × rated current to allow for harmonics and capacitance tolerance.
- Where the [THD](/electrical/thd/) is high, use detuned (reactor) banks to avoid resonance.
- Find the kVAr you need from the load and power factors with the [power factor correction calculator](/electrical/power-factor-correction/).
''')

# ---------------------------------------------------------------- Busbar size
bb_I, bb_J, bb_t, bb_n, bb_rho = 1600.0, 1.6, 10.0, 1, 1.724e-8
bb_A = bb_I / bb_J
bb_w = bb_A / (bb_n * bb_t)
bb_P = bb_I**2 * bb_rho / (bb_A * 1e-6)
sizes = [(20, 5), (30, 5), (40, 5), (40, 10), (50, 10), (60, 10), (80, 10), (100, 10), (120, 10), (160, 10), (200, 10)]
bb_rows = ''.join(f"| {w} × {t} mm | {w*t:,} mm² | {w*t*1.2:,.0f} A | {w*t*1.6:,.0f} A | {w*t*0.8:,.0f} A |\n" for w, t in sizes)
page('electrical', 'busbar-size', f'''
title: Busbar Size Calculator (Current Density Method)
description: Estimate copper or aluminium busbar cross-section and width from current and a design current density, with the resistive loss per metre.
category: electrical
{intro("A first estimate of busbar size divides the current by a safe current density, typically about 1.2–1.6 A/mm² for copper and 0.8–1.0 A/mm² for aluminium inside switchboards. This busbar size calculator gives the cross-section, the bar width for a chosen thickness and the resistive loss per metre — see the [busbar sizing calculation guide](ib:busbar-sizing-calculation-guide) for temperature-rise and short-circuit checks.")}
keywords: [busbar size calculator, busbar sizing calculation, copper busbar current capacity, busbar current density, aluminium busbar size, busbar cross section calculator, panel busbar calculation]
updated: {D}
variables:
  - {{ id: I, label: Rated current, family: current, unit: A, default: 1600, min: 0 }}
  - id: rho
    label: Material
    default: 1.724e-8
    options:
      - {{ label: 'Copper (ρ = 1.724 × 10⁻⁸ Ω·m)', value: 1.724e-8 }}
      - {{ label: 'Aluminium (ρ = 2.826 × 10⁻⁸ Ω·m)', value: 2.826e-8 }}
  - {{ id: J, label: Design current density, suffix: A/mm², default: 1.6, min: 0, help: 'Typical: copper 1.2–1.6 A/mm², aluminium 0.8–1.0 A/mm² in enclosed panels.' }}
  - {{ id: t, label: Bar thickness, family: length, unit: mm, imperialUnit: in, default: 10, min: 0 }}
  - {{ id: nb, label: Bars per phase, default: 1, min: 1 }}
  - {{ id: A, label: Required cross-section, family: area, unit: mm2, imperialUnit: in2, min: 0 }}
  - {{ id: w, label: Width of each bar, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: Pm, label: Resistive loss per metre per phase (DC, 20 °C), suffix: W/m, min: 0 }}
equations:
  - A = I / (J * 1e6)
  - w = A / (nb * t)
  - Pm = I^2 * rho / A
faq:
  - q: How do I calculate busbar size?
    a: Cross-section = current ÷ current density. For 1,600 A at 1.6 A/mm², a copper busbar needs 1,000 mm² — for example one 100 × 10 mm bar per phase.
  - q: What current density should I use for a copper busbar?
    a: About 1.2–1.6 A/mm² for enclosed switchboards and up to about 2 A/mm² for small, well-ventilated bars. Large bars need lower densities because their surface area per mm² is smaller.
  - q: Why is aluminium busbar larger than copper?
    a: Aluminium has about 1.6 times the resistivity of copper, so it needs roughly 60% more cross-section for the same loss and temperature rise — but it is much lighter and cheaper.
  - q: Is the current density method enough for final design?
    a: No. Final sizing should be verified by temperature-rise tests or tables (IEC 61439, DIN 43671), and the bars and supports checked for short-circuit thermal and mechanical stress.
related: [electrical/cable-voltage-drop, electrical/wire-resistance, electrical/skin-depth, electrical/transformer-current]
''', f'''
## How to use the busbar size calculator

Enter the **rated current**, choose **copper** or **aluminium**, set the **design current density**, the **bar thickness** and the number of **bars per phase**. The calculator returns the cross-section required, the width of each bar and the resistive loss per metre of each phase at 20 °C DC. Round up to the next standard bar size.

## Busbar sizing formulas

<p class="formula">A = I ÷ J &nbsp;·&nbsp; w = A ÷ (n × t) &nbsp;·&nbsp; P/L = I² ρ ÷ A</p>

## Example

1,600 A copper busbar at 1.6 A/mm², 10 mm thick bars, one bar per phase:

- A = 1600 ÷ 1.6 = **{bb_A:,.0f} mm²**
- w = 1000 ÷ (1 × 10) = **{bb_w:.0f} mm** → one 100 × 10 mm bar per phase
- Loss = 1600² × 1.724 × 10⁻⁸ ÷ 0.001 = **{bb_P:.1f} W/m** per phase

## Current estimate for standard flat bars

| Size | Area | Copper at 1.2 A/mm² | Copper at 1.6 A/mm² | Aluminium at 0.8 A/mm² |
|---|---|---|---|---|
{bb_rows}
These are current-density estimates, not certified ratings — large bars carry less per mm² than small ones.

## Design notes

- **AC effects**: above about 10 mm thickness the [skin effect](/electrical/skin-depth/) means the centre of a copper bar carries little current at 50 Hz, so use several thinner bars with gaps rather than one thick bar.
- **Multiple bars per phase** do not share current perfectly; derate by about 10–20% for 2–4 bars.
- **Painting** bars matt black improves heat dissipation by radiation; enclosure ventilation and ambient temperature matter as much as cross-section.
- Check the short-circuit withstand: copper needs about A ≥ I<sub>sc</sub> × √t ÷ 143 mm² for a 1 s fault from 90 °C to 250 °C (k ≈ 143).
''')

# ---------------------------------------------------------------- Battery bank size
bt_P, bt_t, bt_V, bt_eta, bt_dod, bt_k, bt_Vb = 500.0, 4.0, 48.0, 0.90, 0.80, 1.25, 12.0
bt_E = bt_P * bt_t
bt_Ah = bt_E / (bt_V * bt_eta * bt_dod) * bt_k
bt_rows = ''.join(f"| {p:,} W | " + ' | '.join(f"{p*h/(48*0.9*0.8)*1.25:,.0f} Ah" for h in (1, 2, 4, 8)) + " |\n" for p in (250, 500, 1000, 2000, 3000, 5000))
page('electrical', 'battery-bank-size', f'''
title: Battery Bank Size Calculator (Ah for Backup Time)
description: Calculate battery bank capacity in Ah for a load and backup time, allowing for inverter efficiency, depth of discharge and an ageing margin.
category: electrical
{intro("Sizing a battery bank starts with the energy the load needs, then allows for inverter losses, how deeply the batteries may be discharged and their loss of capacity with age. This battery bank size calculator gives the amp-hour capacity and the number of batteries in series — see [how to calculate battery backup time](ib:calculate-battery-backup-time) and the [IEEE 485 approach to substation battery sizing](ib:substation-battery-sizing-ieee-485).")}
keywords: [battery bank size calculator, battery ah calculator, battery backup calculator, inverter battery size, solar battery bank sizing, ups battery ah calculation, how many batteries do i need]
updated: {D}
variables:
  - {{ id: P, label: Load power, family: power, unit: W, default: 500, min: 0 }}
  - {{ id: tb, label: Backup time required, family: seconds, unit: h, default: 4, min: 0 }}
  - {{ id: V, label: Battery bank voltage, family: voltage, unit: V, default: 48, min: 0 }}
  - {{ id: eta, label: Inverter efficiency, family: percent, unit: '%', default: 90, min: 0, max: 100, help: 'Use 100% for a DC load fed directly from the battery.' }}
  - {{ id: dod, label: Allowed depth of discharge, family: percent, unit: '%', default: 80, min: 0, max: 100, help: 'Lead-acid 50–80%, lithium (LiFePO₄) 80–90%.' }}
  - {{ id: k, label: Ageing / design margin factor, default: 1.25, min: 1, help: '1.25 allows for capacity falling to 80% at end of life (IEEE 485). Add a temperature factor for cold rooms.' }}
  - {{ id: Vb, label: Voltage of one battery, family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: E, label: Energy delivered to the load, family: energy, unit: Wh, min: 0 }}
  - {{ id: Ah, label: Required battery capacity, suffix: Ah, min: 0, decimals: 1 }}
  - {{ id: ns, label: Batteries in series, min: 0, decimals: 1 }}
equations:
  - E = P * tb
  - Ah = E / 3600 / (V * eta * dod) * k
  - ns = V / Vb
faq:
  - q: How do I calculate battery Ah for backup?
    a: Ah = (load W × hours) ÷ (bank voltage × inverter efficiency × depth of discharge) × margin. A 500 W load for 4 h on a 48 V bank at 90% efficiency, 80% DoD and a 1.25 margin needs about 72 Ah.
  - q: How many batteries do I need?
    a: Batteries in series = bank voltage ÷ battery voltage (48 V ÷ 12 V = 4). If one string's Ah is not enough, add parallel strings; total batteries = series × parallel.
  - q: Why is the Ah rating at a high discharge rate lower?
    a: Lead-acid capacity is usually quoted at the 10- or 20-hour rate. Discharging in 1–2 hours can deliver only 60–75% of the nameplate Ah, so check the manufacturer's constant-power discharge tables for short backups.
  - q: Should I use a higher bank voltage?
    a: For loads above about 1–2 kW, yes. A higher voltage halves the current for the same power, which reduces cable size and losses.
related: [electrical/ups-sizing, electronics/battery-charge-time, electrical/cable-voltage-drop, electrical/amps-to-watts]
''', f'''
## How to use the battery bank size calculator

Enter the **load power**, the **backup time**, the **bank voltage**, the **inverter efficiency**, the **allowed depth of discharge**, a **design margin** and the **voltage of one battery**. The calculator returns the energy the load uses, the amp-hour capacity the bank must have and how many batteries to connect in series. Choose the next standard Ah size above the result.

## Battery sizing formula

<p class="formula">Ah = (P × t) ÷ (V<sub>bank</sub> × η × DoD) × k &nbsp;·&nbsp; N<sub>series</sub> = V<sub>bank</sub> ÷ V<sub>battery</sub></p>

## Example

A 500 W load must run for 4 hours from a 48 V lead-acid bank through a 90% efficient inverter, discharging to 80% with a 1.25 ageing margin:

- Energy = 500 × 4 = **{bt_E:,.0f} Wh**
- Ah = 2000 ÷ (48 × 0.9 × 0.8) × 1.25 = **{bt_Ah:.1f} Ah**
- Series batteries = 48 ÷ 12 = **{bt_V/bt_Vb:.0f}** → four 12 V, 75 Ah (or larger) batteries

## Capacity needed on a 48 V bank

90% inverter efficiency, 80% depth of discharge, 1.25 margin:

| Load | 1 h | 2 h | 4 h | 8 h |
|---|---|---|---|---|
{bt_rows}
## Practical notes

- Lead-acid batteries last much longer when discharged to only 50%; LiFePO₄ tolerates 80–90% routinely.
- At 0–10 °C, lead-acid capacity falls by 10–20% — add a temperature correction factor.
- The charger must be able to recharge the bank in a reasonable time; see the [battery charge time calculator](/electronics/battery-charge-time/).
- For the UPS kVA rating itself, use the [UPS sizing calculator](/electrical/ups-sizing/).
''')

# ---------------------------------------------------------------- Generator frequency & poles
gf_p, gf_N = 4, 1500
gf_f = gf_p * gf_N / 120
gf_rows = ''.join(f"| {p} | {p//2} | {120*50/p:,.1f} rpm | {120*60/p:,.1f} rpm | {typ} |\n".replace('.0 rpm', ' rpm')
                  for p, typ in ((2, 'Steam / gas turbine generators'), (4, 'Diesel gensets, turbo sets'), (6, 'Medium-speed diesel'), (8, 'Medium-speed diesel, small hydro'),
                                 (12, 'Gas engines, hydro'), (16, 'Low-speed engines, hydro'), (24, 'Hydro'), (48, 'Low-head hydro'), (96, 'Very low-head hydro')))
page('electrical', 'generator-frequency', f'''
title: Generator Frequency Calculator (Poles & RPM, f = PN/120)
description: Calculate the output frequency of an alternator from its number of poles and speed — or the speed in rpm needed for 50 Hz or 60 Hz.
category: electrical
{intro("A synchronous generator's output frequency is fixed by how fast its rotor turns and how many magnetic poles it has. This generator frequency calculator applies f = P × N ÷ 120 to find the frequency from the speed, or the speed a prime mover must run at for 50 Hz or 60 Hz — see [how an alternator works](ib:alternator-working-principle-explained).")}
keywords: [generator frequency calculator, alternator frequency formula, f = pn/120 calculator, generator rpm calculator, number of poles calculator, synchronous speed generator, 50 hz generator speed]
updated: {D}
variables:
  - {{ id: p, label: Number of poles, default: 4, min: 2, help: 'Always an even number — poles come in north–south pairs.' }}
  - {{ id: N, label: Rotor speed, suffix: rpm, default: 1500, min: 0 }}
  - {{ id: f, label: Output frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: pp, label: Pole pairs, min: 0 }}
equations:
  - f = p * N / 120
  - pp = p / 2
faq:
  - q: How do you calculate generator frequency?
    a: f = P × N ÷ 120, with P the number of poles and N the speed in rpm. A 4-pole alternator at 1,500 rpm gives 50 Hz; at 1,800 rpm it gives 60 Hz.
  - q: Why is the formula divided by 120?
    a: Each pole pair produces one electrical cycle per revolution, so f = (P ÷ 2) × (N ÷ 60) = P N ÷ 120.
  - q: What speed does a 2-pole generator run at?
    a: 3,000 rpm for 50 Hz and 3,600 rpm for 60 Hz — the usual speed of steam- and gas-turbine generators.
  - q: Why do hydro generators have so many poles?
    a: Water turbines turn slowly (often 100–500 rpm), so the generator needs many poles to reach 50 or 60 Hz. A 48-pole machine runs at 125 rpm for 50 Hz.
related: [electrical/induction-motor-slip, electrical/generator-size, electrical/generator-power-angle, physics/angular-velocity]
''', f'''
## How to use the generator frequency calculator

Enter the **number of poles** and the **rotor speed** in rpm to get the output frequency. To find the speed for a target frequency, enter the frequency and clear the speed field; to find the pole count for a turbine speed, clear the poles field.

## Generator frequency formula

<p class="formula">f = P × N ÷ 120 &nbsp;·&nbsp; N = 120 f ÷ P</p>

## Example

A 4-pole diesel generator set running at 1,500 rpm:

- f = 4 × 1500 ÷ 120 = **{gf_f:.0f} Hz**
- At 1,800 rpm the same machine gives 4 × 1800 ÷ 120 = **{4*1800/120:.0f} Hz**

## Synchronous speed by number of poles

| Poles | Pole pairs | Speed for 50 Hz | Speed for 60 Hz | Typical machines |
|---|---|---|---|---|
{gf_rows}
## Notes

- The governor holds speed — and therefore frequency — constant as load changes; a 2% droop governor lets a 50 Hz set fall to 49 Hz at full load.
- Induction motors run slightly slower than synchronous speed; see the [induction motor slip calculator](/electrical/induction-motor-slip/).
- Before paralleling with the grid, a generator must match its frequency, voltage and phase angle.
''')

# ---------------------------------------------------------------- Generator power angle
ga_E, ga_V, ga_X, ga_d = 12000.0, 11000.0, 10.0, 20.0
ga_Pmax = ga_E * ga_V / ga_X
ga_P = ga_Pmax * math.sin(math.radians(ga_d))
ga_Q = (ga_E * ga_V * math.cos(math.radians(ga_d)) - ga_V**2) / ga_X
ga_rows = ''.join(f"| {d}° | {math.sin(math.radians(d)):.3f} | {ga_Pmax*math.sin(math.radians(d))/1e6:.2f} MW | {(ga_E*ga_V*math.cos(math.radians(d))-ga_V**2)/ga_X/1e6:+.2f} MVAr |\n"
                  for d in (0, 10, 20, 30, 45, 60, 75, 90))
page('electrical', 'generator-power-angle', f'''
title: Generator Power Angle Calculator (P = EV sin δ / Xs)
description: Calculate the active and reactive power of a synchronous generator from its internal EMF, terminal voltage, synchronous reactance and load angle δ.
category: electrical
{intro("The power a synchronous generator delivers to the grid depends on the angle δ between its internal EMF and the terminal voltage, while its excitation decides the reactive power. This generator power angle calculator gives the active power, the steady-state stability limit and the reactive power for a round-rotor machine — see how the [excitation system and AVR](ib:generator-excitation-system-avr) control the EMF.")}
keywords: [generator power angle calculator, power angle equation, load angle calculator, p = ev sin delta / x, synchronous generator power, steady state stability limit, torque angle calculator]
updated: {D}
variables:
  - {{ id: E, label: Internal EMF E (line-to-line), family: voltage, unit: kV, default: 12, min: 0 }}
  - {{ id: V, label: Terminal / bus voltage (line-to-line), family: voltage, unit: kV, default: 11, min: 0 }}
  - {{ id: X, label: Synchronous reactance per phase, family: resistance, unit: ohm, default: 10, min: 0 }}
  - {{ id: d, label: Power (load) angle δ, family: angle, unit: deg, default: 20 }}
  - {{ id: P, label: Active power (3-phase), family: power, unit: MW }}
  - {{ id: Pmax, label: Maximum power (δ = 90°), family: power, unit: MW, min: 0 }}
  - {{ id: Q, label: Reactive power delivered, suffix: MVAr }}
equations:
  - P = E * V / X * sin(d)
  - Pmax = E * V / X
  - Q = (E * V * cos(d) - V^2) / X / 1e6
faq:
  - q: What is the power angle equation?
    a: P = (E × V ÷ X_s) × sin δ for a round-rotor machine with armature resistance neglected. With line-to-line voltages it gives the total three-phase power.
  - q: What is the steady-state stability limit?
    a: The maximum power E V ÷ X_s, reached at δ = 90°. Beyond that, more mechanical input makes the machine slip poles, so generators normally run at δ = 20–40°.
  - q: How does excitation affect reactive power?
    a: Q = (E V cos δ − V²) ÷ X_s. Raising the field current raises E and the generator exports more reactive power (over-excited, lagging PF); weakening it makes the machine absorb reactive power.
  - q: Does this apply to salient-pole machines?
    a: Only approximately. Salient-pole generators add a reluctance term, V² (1/X_q − 1/X_d) sin 2δ ÷ 2, which this calculator does not include.
related: [electrical/generator-frequency, electrical/generator-size, electrical/per-unit, electrical/kva-to-kw]
''', f'''
## How to use the generator power angle calculator

Enter the generator's **internal EMF** and the **terminal (bus) voltage**, both line-to-line, the **synchronous reactance per phase** and the **power angle δ**. The calculator returns the three-phase active power, the maximum (pull-out) power and the reactive power delivered — negative Q means the machine is absorbing reactive power. To find the load angle for a given output, enter P and clear δ.

## Power angle equations

<p class="formula">P = (E × V ÷ X<sub>s</sub>) × sin δ &nbsp;·&nbsp; P<sub>max</sub> = E × V ÷ X<sub>s</sub></p>

<p class="formula">Q = (E × V × cos δ − V²) ÷ X<sub>s</sub></p>

## Example

An 11 kV generator with E = 12 kV, X<sub>s</sub> = 10 Ω per phase, running at δ = 20°:

- P<sub>max</sub> = 12,000 × 11,000 ÷ 10 = **{ga_Pmax/1e6:.1f} MW**
- P = 13.2 × sin 20° = **{ga_P/1e6:.3f} MW**
- Q = (12,000 × 11,000 × cos 20° − 11,000²) ÷ 10 = **{ga_Q/1e6:.3f} MVAr** (exporting)

## Power and reactive power vs load angle

Same machine (E = 12 kV, V = 11 kV, X<sub>s</sub> = 10 Ω):

| δ | sin δ | Active power | Reactive power |
|---|---|---|---|
{ga_rows}
## Notes

- Armature resistance is neglected — typically less than 1% of X<sub>s</sub> for large machines.
- In per-unit, P = E V sin δ ÷ X<sub>s</sub> with E, V and X<sub>s</sub> in pu; see the [per-unit calculator](/electrical/per-unit/).
- During a fault the transient reactance X′<sub>d</sub> replaces X<sub>s</sub> in transient-stability studies.
''')

# ---------------------------------------------------------------- Skin depth
def skin(rho, f, mur=1): return math.sqrt(rho / (math.pi * f * MU0 * mur))
sk_rho, sk_f = 1.678e-8, 50.0
sk_d = skin(sk_rho, sk_f)
def fstr(f):
    for v, u in ((1e9, 'GHz'), (1e6, 'MHz'), (1e3, 'kHz')):
        if f >= v: return f"{f/v:g} {u}"
    return f"{f:g} Hz"
def dstr(d):
    return f"{d*1000:.3g} mm" if d >= 1e-3 else f"{d*1e6:.3g} µm"
sk_rows = ''.join(f"| {fstr(f)} | {dstr(skin(1.678e-8, f))} | {dstr(skin(2.65e-8, f))} | {dstr(skin(7.2e-7, f))} |\n" for f in (50, 60, 400, 1e3, 10e3, 100e3, 1e6, 10e6, 100e6, 1e9))
page('electrical', 'skin-depth', f'''
title: Skin Depth Calculator (Skin Effect in Conductors)
description: Calculate the skin depth of copper, aluminium and other conductors at any frequency — the depth where AC current density falls to 37% of the surface value.
category: electrical
{intro("Alternating current crowds towards the surface of a conductor, so at high frequency only a thin outer layer carries it and the AC resistance rises. This skin depth calculator finds that layer's depth for copper, aluminium and other metals at any frequency — see [skin effect in conductors](ib:skin-effect-in-conductors) for why it matters in busbars, cables and RF circuits.")}
keywords: [skin depth calculator, skin effect calculator, skin depth formula, copper skin depth, skin depth at 50 hz, ac resistance skin effect, rf skin depth]
updated: {D}
variables:
  - id: rho
    label: Conductor
    default: 1.678e-8
    options:
      - {{ label: 'Copper (1.678 × 10⁻⁸ Ω·m)', value: 1.678e-8 }}
      - {{ label: 'Aluminium (2.65 × 10⁻⁸ Ω·m)', value: 2.65e-8 }}
      - {{ label: 'Silver (1.59 × 10⁻⁸ Ω·m)', value: 1.59e-8 }}
      - {{ label: 'Gold (2.44 × 10⁻⁸ Ω·m)', value: 2.44e-8 }}
      - {{ label: 'Stainless steel 304 (7.2 × 10⁻⁷ Ω·m)', value: 7.2e-7 }}
  - {{ id: mur, label: Relative permeability (μr), default: 1, min: 0, help: '1 for copper, aluminium and austenitic stainless steel; mild steel is 100 or more.' }}
  - {{ id: f, label: Frequency, family: frequency, unit: Hz, default: 50, min: 0 }}
  - {{ id: dl, label: Skin depth (δ), family: length, unit: mm, imperialUnit: in, min: 0 }}
equations:
  - dl = sqrt(rho / (pi * f * 1.25663706212e-6 * mur))
faq:
  - q: What is the skin depth formula?
    a: δ = √(ρ ÷ (π f μ₀ μr)), where ρ is the resistivity, f the frequency and μ₀μr the permeability. It is the depth at which current density falls to 1/e (about 37%) of its surface value.
  - q: What is the skin depth of copper at 50 Hz?
    a: About 9.2 mm (8.4 mm at 60 Hz). Copper conductors thicker than about 2δ — roughly 18 mm — gain little from extra thickness at power frequency.
  - q: How does skin depth change with frequency?
    a: It falls with the square root of frequency. Copper's skin depth is about 2.1 mm at 1 kHz, 65 µm at 1 MHz and 2.1 µm at 1 GHz.
  - q: How do I reduce skin effect losses?
    a: Use flat or hollow conductors, several smaller conductors in parallel, or Litz wire (many insulated, twisted strands) for kHz-range transformers and inductors.
related: [electrical/busbar-size, electrical/wire-resistance, electronics/pcb-trace-width, electronics/reactance]
''', f'''
## How to use the skin depth calculator

Choose the **conductor material**, enter its **relative permeability** (1 for non-magnetic metals) and the **frequency**. The calculator returns the skin depth δ. At depth δ the current density is 37% of its surface value; about 86% of the current flows within the outer δ of a thick conductor.

## Skin depth formula

<p class="formula">δ = √(ρ ÷ (π f μ<sub>0</sub> μ<sub>r</sub>))</p>

μ<sub>0</sub> = 1.25663706212 × 10⁻⁶ H/m; resistivities are at 20 °C.

## Example

Copper (ρ = 1.678 × 10⁻⁸ Ω·m, μ<sub>r</sub> = 1) at 50 Hz:

- π × 50 × 1.2566 × 10⁻⁶ = 1.974 × 10⁻⁴
- δ = √(1.678 × 10⁻⁸ ÷ 1.974 × 10⁻⁴) = **{sk_d*1000:.2f} mm**

## Skin depth vs frequency

| Frequency | Copper | Aluminium | Stainless steel 304 |
|---|---|---|---|
{sk_rows}
## Practical consequences

- **Busbars and large cables**: at 50/60 Hz, bars thicker than about 10 mm (copper) gain little capacity; large cables use segmented (Milliken) conductors — see the [busbar size calculator](/electrical/busbar-size/).
- **Switch-mode power supplies**: at 100 kHz copper's δ is about 0.2 mm, so windings use Litz wire or copper foil.
- **RF and PCB traces**: above about 100 MHz current flows in a few micrometres, so surface roughness and plating matter.
- Resistivity rises with temperature, so hot conductors have a slightly larger skin depth.
''')

# ---------------------------------------------------------------- Energy meter constant
em_C, em_n, em_t, em_Pr = 3200.0, 32, 30.0, 1190.0
em_P = em_n * 3.6e6 / (em_C * em_t)
em_E = em_n * 3.6e6 / em_C
em_err = (em_P - em_Pr) / em_Pr
em_ti = 3.6e6 / (em_C * em_Pr)
em_rows = ''.join(f"| {int(c):,} imp/kWh | " + ' | '.join(f"{3.6e6/(c*p):,.3g} s" for p in (100, 1000, 5000)) + " |\n" for c in (100, 400, 800, 1000, 1600, 3200, 6400, 10000))
page('electrical', 'energy-meter-constant', f'''
title: Energy Meter Constant Calculator (imp/kWh to Load kW)
description: Calculate load power from an energy meter's pulse LED or disc using its meter constant (imp/kWh or rev/kWh), and check the meter's percentage error.
category: electrical
{intro("Every electricity meter has a constant, printed as imp/kWh (pulses) or rev/kWh (disc turns), that says how many pulses mean one kilowatt-hour. This energy meter constant calculator converts pulses counted over a time into load power and energy, and compares it with a reference load to give the meter error — useful alongside an [electrical energy consumption calculation](ib:electrical-energy-consumption-calculation).")}
keywords: [energy meter constant calculator, imp/kwh calculator, meter pulse to kw, energy meter testing, rev/kwh calculator, meter error calculation, kwh meter pulse calculation]
updated: {D}
variables:
  - {{ id: C, label: Meter constant, suffix: imp/kWh, default: 3200, min: 0, help: 'For a disc meter, enter the rev/kWh value and count revolutions.' }}
  - {{ id: n, label: Pulses (or revolutions) counted, default: 32, min: 0 }}
  - {{ id: t, label: Counting time, family: seconds, unit: s, default: 30, min: 0 }}
  - {{ id: Pr, label: Reference (actual) load, family: power, unit: kW, default: 1.19, min: 0, help: 'From a calibrated wattmeter or a known load.' }}
  - {{ id: P, label: Load power indicated by the meter, family: power, unit: kW, min: 0 }}
  - {{ id: E, label: Energy recorded, family: energy, unit: Wh, min: 0 }}
  - {{ id: err, label: Meter error, family: percent, unit: '%' }}
  - {{ id: ti, label: Time between pulses at reference load, family: seconds, unit: s, min: 0 }}
equations:
  - P = n * 3600000 / (C * t)
  - E = n * 3600000 / C
  - err = (P - Pr) / Pr
  - ti = 3600000 / (C * Pr)
faq:
  - q: How do I calculate load from the meter's pulse LED?
    a: P (kW) = 3,600 × pulses ÷ (meter constant × seconds). With 3,200 imp/kWh, 32 pulses in 30 s means 1.2 kW.
  - q: What does 3200 imp/kWh mean?
    a: The LED flashes 3,200 times for every kilowatt-hour recorded, so each pulse is 1 ÷ 3,200 kWh = 0.3125 Wh.
  - q: How do I check if my energy meter is accurate?
    a: Run a known, steady load (a heater measured with a calibrated wattmeter), count pulses for at least a minute and compare. Error = (meter reading − actual) ÷ actual. Class 1 meters must be within ±1%.
  - q: What about CT-operated meters?
    a: For a meter on current and voltage transformers, the constant refers to the secondary side. Multiply the result by the CT ratio × PT ratio to get the primary power.
related: [electrical/load-factor, electrical/amps-to-watts, electrical/kw-to-amps, electrical/power-factor-correction]
''', f'''
## How to use the energy meter constant calculator

Enter the **meter constant** from the nameplate, the number of **pulses** (or disc revolutions) you counted and the **time** you counted for. The calculator returns the load power the meter is registering and the energy recorded. Add a **reference load** from a calibrated instrument to see the meter's percentage error and the expected time between pulses.

## Meter constant formulas

<p class="formula">P (kW) = 3600 × n ÷ (C × t) &nbsp;·&nbsp; E (kWh) = n ÷ C</p>

<p class="formula">Error = (P<sub>meter</sub> − P<sub>actual</sub>) ÷ P<sub>actual</sub> × 100%</p>

## Example

A 3,200 imp/kWh meter flashes 32 times in 30 s while a reference wattmeter reads 1.19 kW:

- P = 3600 × 32 ÷ (3200 × 30) = **{em_P/1000:.2f} kW**
- Energy recorded = 32 ÷ 3200 kWh = **{em_E/3600:.0f} Wh**
- Error = (1.20 − 1.19) ÷ 1.19 = **{em_err*100:+.2f}%** (the meter reads high)
- At 1.19 kW the LED should flash every **{em_ti:.3f} s**

## Time between pulses

| Meter constant | at 100 W | at 1 kW | at 5 kW |
|---|---|---|---|
{em_rows}
## Testing tips

- Count for at least 60 s or 20 pulses to keep timing error below about 1%.
- Use a purely resistive, steady load; motor or switching loads fluctuate.
- For three-phase meters, apply a balanced load or test each element separately.
- To turn monthly kWh into load factor and demand figures, use the [load factor calculator](/electrical/load-factor/).
''')

# ---------------------------------------------------------------- Load factor & maximum demand
lfa_E, lfa_t, lfa_MD, lfa_Pc = 216000.0, 720.0, 500.0, 800.0
lfa_avg = lfa_E / lfa_t
lfa_LF = lfa_avg / lfa_MD
lfa_DF = lfa_MD / lfa_Pc
lfa_rows = ''.join(f"| {lf*100:.0f}% | {500*lf*720:,.0f} kWh | {500*lf*8760/1000:,.0f} MWh | {lf*24:.1f} h |\n" for lf in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9))
page('electrical', 'load-factor', f'''
title: Load Factor Calculator (Maximum Demand & Demand Factor)
description: Calculate load factor from energy consumed and maximum demand, plus average load and demand factor — for monthly electricity bills and plant studies.
category: electrical
{intro("Load factor compares the average load over a period with the peak, or maximum demand, so it shows how steadily a plant uses its electrical capacity. This load factor calculator works out average load, load factor and demand factor from a bill's kWh and kW figures — see [maximum demand calculation with diversity](ib:maximum-demand-calculation-diversity) for estimating the peak at design stage.")}
keywords: [load factor calculator, maximum demand calculator, demand factor calculator, load factor formula, average load calculation, electricity load factor, kwh to load factor]
updated: {D}
variables:
  - {{ id: E, label: Energy consumed in the period, family: energy, unit: kWh, default: 216000, min: 0 }}
  - {{ id: tp, label: Length of the period, family: seconds, unit: h, default: 720, min: 0, help: '720 h = 30 days; 8,760 h = one year.' }}
  - {{ id: MD, label: Maximum demand, family: power, unit: kW, default: 500, min: 0 }}
  - {{ id: Pc, label: Connected load, family: power, unit: kW, default: 800, min: 0 }}
  - {{ id: Pa, label: Average load, family: power, unit: kW, min: 0 }}
  - {{ id: LF, label: Load factor, family: percent, unit: '%', min: 0 }}
  - {{ id: DF, label: Demand factor (MD ÷ connected load), family: percent, unit: '%', min: 0 }}
equations:
  - Pa = E / tp
  - LF = Pa / MD
  - DF = MD / Pc
faq:
  - q: How do you calculate load factor?
    a: Load factor = energy consumed ÷ (maximum demand × hours in the period). 216,000 kWh in a 30-day month (720 h) with a 500 kW maximum demand gives 216,000 ÷ 360,000 = 60%.
  - q: What is a good load factor?
    a: Higher is better — continuous process plants reach 70–90%, while offices and single-shift factories are often 20–40%. A high load factor means fixed demand charges are spread over more kWh.
  - q: What is the difference between load factor and demand factor?
    a: Load factor is average ÷ peak load over time. Demand factor is maximum demand ÷ total connected load, and shows how much of the installed equipment runs at the same time.
  - q: How can I improve load factor?
    a: Reduce the peak rather than the energy — stagger motor starts, shift batch loads to off-peak hours and use demand controllers or energy storage.
related: [electrical/energy-meter-constant, electrical/kw-to-amps, electrical/transformer-size, electrical/power-factor-correction]
''', f'''
## How to use the load factor calculator

Enter the **energy consumed** (kWh) and the **length of the period** from your electricity bill or meter readings, the **maximum demand** recorded in that period and, optionally, the total **connected load**. The calculator returns the average load, the load factor and the demand factor.

## Load factor formulas

<p class="formula">Average load = E ÷ t &nbsp;·&nbsp; Load factor = Average load ÷ Maximum demand</p>

<p class="formula">Demand factor = Maximum demand ÷ Connected load</p>

## Example

A factory used 216,000 kWh in a 30-day month with a recorded maximum demand of 500 kW and 800 kW of connected load:

- Average load = 216,000 ÷ 720 = **{lfa_avg:.0f} kW**
- Load factor = 300 ÷ 500 = **{lfa_LF*100:.0f}%**
- Demand factor = 500 ÷ 800 = **{lfa_DF*100:.1f}%**

## Energy for a 500 kW maximum demand

| Load factor | kWh per 30 days | MWh per year | Equivalent full-load hours per day |
|---|---|---|---|
{lfa_rows}
## Notes

- Utilities measure maximum demand as the highest average over a 15- or 30-minute window, not the instantaneous peak.
- With kVA-based demand tariffs, improving power factor also cuts the billed maximum demand.
- The transformer only needs to be sized for the diversified maximum demand, not the connected load — see the [transformer size calculator](/electrical/transformer-size/).
''')

# ---------------------------------------------------------------- Autotransformer
at_S, at_Vh, at_Vl = 10.0, 240.0, 200.0
at_Ih = at_S * 1000 / at_Vh; at_Il = at_S * 1000 / at_Vl
at_Ic = at_Il - at_Ih
at_Si = at_S * (1 - at_Vl / at_Vh); at_Sc = at_S * at_Vl / at_Vh
at_rows = ''.join(f"| {vh:g} / {vl:g} V | {vl/vh:.3f} | {(1-vl/vh)*100:.1f}% | {vl/vh*100:.1f}% |\n"
                  for vh, vl in ((240, 220), (240, 200), (415, 380), (480, 415), (400, 230), (240, 120), (400, 100)))
page('electrical', 'autotransformer', f'''
title: Autotransformer Calculator (Currents, kVA & Copper Saving)
description: Calculate autotransformer primary, secondary and common-winding currents, the kVA transformed vs conducted, and the copper saved over a two-winding unit.
category: electrical
{intro("An autotransformer uses a single tapped winding, so part of the power passes straight through by conduction and only the rest is transformed magnetically. This autotransformer calculator gives the line and common-winding currents and the split between transformed and conducted kVA — see the [autotransformer working principle](ib:autotransformer-working-principle) for how the shared winding works.")}
keywords: [autotransformer calculator, autotransformer current calculation, autotransformer kva calculation, copper saving in autotransformer, transformed and conducted power, auto transformer formula, variac calculator]
updated: {D}
variables:
  - {{ id: S, label: Load rating, suffix: kVA, default: 10, min: 0 }}
  - {{ id: Vh, label: High-voltage side, family: voltage, unit: V, default: 240, min: 0 }}
  - {{ id: Vl, label: Low-voltage side, family: voltage, unit: V, default: 200, min: 0 }}
  - {{ id: Ih, label: High-side current, family: current, unit: A, min: 0 }}
  - {{ id: Il, label: Low-side current, family: current, unit: A, min: 0 }}
  - {{ id: Ic, label: Current in the common winding, family: current, unit: A, min: 0 }}
  - {{ id: Si, label: Power transformed (inductively), suffix: kVA, min: 0, decimals: 3 }}
  - {{ id: Sc, label: Power conducted directly, suffix: kVA, min: 0, decimals: 3 }}
  - {{ id: cs, label: Copper saved vs a two-winding transformer, family: percent, unit: '%', min: 0 }}
equations:
  - Ih = S * 1000 / Vh
  - Il = S * 1000 / Vl
  - Ic = Il - Ih
  - Si = S * (1 - Vl / Vh)
  - Sc = S * Vl / Vh
  - cs = Vl / Vh
faq:
  - q: How do you calculate autotransformer current?
    a: I_high = S ÷ V_high and I_low = S ÷ V_low, as for any transformer. The common part of the winding carries only the difference, I_low − I_high.
  - q: How much power is transformed in an autotransformer?
    a: Only S × (1 − V_low ÷ V_high). The rest, S × V_low ÷ V_high, is conducted straight through the shared winding. A 240/200 V, 10 kVA unit transforms just 1.67 kVA.
  - q: How much copper does an autotransformer save?
    a: Copper needed = (1 − K) × that of a two-winding transformer, with K = V_low ÷ V_high, so the saving is K. The closer the two voltages, the bigger the saving.
  - q: What is the main disadvantage of an autotransformer?
    a: There is no electrical isolation between primary and secondary, and if the common winding opens, the full input voltage can appear at the output. It also has lower impedance, so fault currents are higher.
related: [electrical/transformer-turns-ratio, electrical/transformer-current, electrical/transformer-size, electrical/transformer-efficiency]
''', f'''
## How to use the autotransformer calculator

Enter the **load rating** in kVA and the **high-** and **low-voltage** sides of the autotransformer (it works the same for step-up and step-down). The calculator returns the current on each side, the current in the common section of the winding, how much of the power is transformed magnetically versus conducted directly, and the copper saved compared with a two-winding transformer of the same rating.

## Autotransformer formulas

<p class="formula">I<sub>H</sub> = S ÷ V<sub>H</sub> &nbsp;·&nbsp; I<sub>L</sub> = S ÷ V<sub>L</sub> &nbsp;·&nbsp; I<sub>common</sub> = I<sub>L</sub> − I<sub>H</sub></p>

<p class="formula">S<sub>transformed</sub> = S (1 − K) &nbsp;·&nbsp; S<sub>conducted</sub> = S K &nbsp;·&nbsp; K = V<sub>L</sub> ÷ V<sub>H</sub></p>

## Example

A 10 kVA, 240 V to 200 V step-down autotransformer:

- I<sub>H</sub> = 10,000 ÷ 240 = **{at_Ih:.2f} A**, I<sub>L</sub> = 10,000 ÷ 200 = **{at_Il:.2f} A**
- Common winding current = 50 − 41.67 = **{at_Ic:.2f} A**
- Transformed = 10 × (1 − 200/240) = **{at_Si:.3f} kVA**; conducted = **{at_Sc:.3f} kVA**
- Copper saved ≈ **{at_Vl/at_Vh*100:.1f}%** of a 10 kVA two-winding transformer

## Transformed power and copper saving by voltage ratio

| Ratio | K | Share of kVA transformed | Copper saving |
|---|---|---|---|
{at_rows}
## Where autotransformers are used

- **Motor starting**: autotransformer starters apply 50–80% voltage taps, cutting line current to K² of the direct-on-line value.
- **Grid interconnection**: large 400/220 kV and 220/132 kV interbus transformers, where the ratio is close to 1.
- **Variacs**: variable autotransformers for test benches.
- Not suitable where isolation is required, or for large ratios such as 11 kV/415 V.
''')
print('ok')
