import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
D = '2026-10-27'
g0 = 9.80665; G = 6.6743e-11; pi = math.pi

# ============================ PHYSICS ============================
page('physics', 'hookes-law', f'''
title: Hooke's Law Calculator (Spring Force)
description: Calculate spring force, spring constant or extension with Hooke's law (F = kx), plus the elastic energy stored in the spring.
category: physics
keywords: [hookes law calculator, spring constant calculator, spring force, f = kx, elastic potential energy, spring extension, stiffness]
updated: {D}
variables:
  - {{ id: k, label: Spring constant (k), suffix: N/m, default: 500, min: 0 }}
  - {{ id: x, label: Extension or compression, family: length, unit: cm, imperialUnit: in, default: 4, min: 0 }}
  - {{ id: F, label: Spring force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: E, label: Stored energy, family: energy, unit: J, min: 0 }}
equations:
  - F = k * x
  - E = 0.5 * k * x^2
faq:
  - q: What is Hooke's law?
    a: The force needed to stretch or compress a spring is proportional to the distance — F = kx — as long as the spring stays within its elastic limit.
  - q: How do I find the spring constant?
    a: Hang a known weight from the spring and measure the extension. k = F ÷ x. A 10 N weight stretching a spring by 2 cm gives k = 500 N/m.
  - q: What happens beyond the elastic limit?
    a: The spring deforms permanently and no longer returns to its original length, so Hooke's law stops applying.
  - q: How much energy does a spring store?
    a: E = ½kx². A 500 N/m spring compressed 4 cm stores 0.4 J.
related: [physics/force, physics/potential-energy, physics/work-and-power, physics/pendulum]
''', f'''
## How to use this calculator

Enter the **spring constant** and the **extension or compression**. The calculator gives the force and the elastic energy stored. Fill any two fields to solve for the others — for example, force and extension to find k.

## The formulas

<p class="formula">F = k × x &nbsp;·&nbsp; E = ½ × k × x²</p>

- **k** = spring constant (stiffness), N/m
- **x** = change in length from the natural length, m

## Example

A spring with k = 500 N/m stretched by 4 cm (0.04 m):

- Force = 500 × 0.04 = **20 N**
- Energy = ½ × 500 × 0.04² = **0.4 J**

## Springs in series and parallel

| Arrangement | Combined stiffness |
|---|---|
| Parallel (side by side) | k = k₁ + k₂ |
| Series (end to end) | 1/k = 1/k₁ + 1/k₂ |

Two identical springs in parallel are twice as stiff; in series they are half as stiff.

## Typical spring constants

| Spring | Approximate k |
|---|---|
| Ballpoint pen spring | 100–500 N/m |
| Kitchen scale spring | 1,000–5,000 N/m |
| Car suspension spring | 20,000–60,000 N/m |
| Railway buffer | over 1,000,000 N/m |

## Mass on a spring

A mass m on a spring oscillates with period T = 2π√(m ÷ k). A 0.5 kg mass on a 500 N/m spring bounces with a period of **{2*pi*math.sqrt(0.5/500):.3f} s**.

## Beyond springs

Hooke's law also describes small stretches of solid materials, where stress = Young's modulus × strain. Steel has a Young's modulus of about 200 GPa.
''')

page('physics', 'snells-law', f'''
title: Snell's Law Calculator (Refraction and Critical Angle)
description: Calculate the angle of refraction, refractive index or critical angle when light passes between two materials, using Snell's law.
category: physics
keywords: [snells law calculator, refraction calculator, angle of refraction, refractive index, critical angle, total internal reflection, n1 sin theta1]
updated: {D}
variables:
  - {{ id: n1, label: Refractive index of first medium (n₁), default: 1.0003, min: 1 }}
  - {{ id: t1, label: Angle of incidence (θ₁), family: angle, unit: deg, default: 30, min: 0, max: 1.5708 }}
  - {{ id: n2, label: Refractive index of second medium (n₂), default: 1.333, min: 1 }}
  - {{ id: t2, label: Angle of refraction (θ₂), family: angle, unit: deg, min: 0, max: 1.5708 }}
equations:
  - n1 * sin(t1) = n2 * sin(t2)
faq:
  - q: What is Snell's law?
    a: n₁ sin θ₁ = n₂ sin θ₂. Light bends towards the normal when it enters a denser medium (higher n) and away from it when it leaves.
  - q: What is the critical angle?
    a: The angle of incidence beyond which light cannot leave a denser medium and is totally reflected. sin θc = n₂ ÷ n₁. For glass to air (n 1.5), θc ≈ 41.8°.
  - q: Why does the calculator show no solution?
    a: When going from a denser to a less dense medium above the critical angle, no refracted ray exists — this is total internal reflection.
  - q: What is the refractive index of water?
    a: About 1.333 for visible light at 20 °C.
related: [physics/thin-lens, physics/wavelength-frequency, physics/projectile-motion, math/right-triangle-trig]
''', f'''
## How to use this calculator

Enter the **refractive indices** of the two materials and the **angle of incidence** (measured from the normal — the line perpendicular to the surface). The calculator finds the angle of refraction. Fill any three values to solve for the fourth.

## The formula

<p class="formula">n₁ sin θ₁ = n₂ sin θ₂</p>

## Refractive indices (visible light)

| Material | n |
|---|---|
| Vacuum | 1 (exactly) |
| Air | 1.0003 |
| Water | 1.333 |
| Ethanol | 1.36 |
| Acrylic (PMMA) | 1.49 |
| Crown glass | 1.52 |
| Flint glass | 1.62 |
| Diamond | 2.42 |

## Critical angles

| From → to air | Critical angle |
|---|---|
''' + ''.join(f"| {m} (n = {n}) | {math.degrees(math.asin(1.0003/n)):.1f}° |\n" for m, n in [('Water', 1.333), ('Acrylic', 1.49), ('Crown glass', 1.52), ('Flint glass', 1.62), ('Diamond', 2.42)]) + f'''
Diamond's small critical angle traps light inside, making it sparkle.

## Example

Light from air into water at 30°: sin θ₂ = 1.0003 × sin 30° ÷ 1.333 = 0.3752, so θ₂ = **{math.degrees(math.asin(1.0003*0.5/1.333)):.1f}°**.

## Applications

- **Optical fibres** carry light by total internal reflection.
- **Lenses** in glasses, cameras and microscopes bend light to focus it.
- **Prisms** split white light because n varies slightly with wavelength (dispersion).
- **Mirages** form when air layers of different temperature bend light.
''')

def lens(f, do): return 1/(1/f - 1/do)
page('physics', 'thin-lens', f'''
title: Thin Lens Equation Calculator (Lens and Mirror Formula)
description: Find focal length, object distance, image distance and magnification for lenses and mirrors using 1/f = 1/dₒ + 1/dᵢ.
category: physics
keywords: [thin lens equation, lens formula calculator, mirror equation, focal length calculator, image distance, magnification calculator, 1/f = 1/u + 1/v]
updated: {D}
variables:
  - {{ id: f, label: Focal length, family: length, unit: cm, imperialUnit: in, default: 10, help: Positive for converging lenses and concave mirrors; negative for diverging lenses and convex mirrors. }}
  - {{ id: do, label: Object distance, family: length, unit: cm, imperialUnit: in, default: 30, min: 0 }}
  - {{ id: di, label: Image distance, family: length, unit: cm, imperialUnit: in }}
  - {{ id: m, label: Magnification, decimals: 3 }}
  - {{ id: P, label: Lens power, suffix: dioptres, decimals: 2 }}
equations:
  - 1 / f = 1 / do + 1 / di
  - m = -di / do
  - P = 1 / f
faq:
  - q: What is the thin lens equation?
    a: 1/f = 1/dₒ + 1/dᵢ, where f is the focal length, dₒ the object distance and dᵢ the image distance. The same formula works for curved mirrors.
  - q: What does a negative image distance mean?
    a: The image is virtual — on the same side as the object for a lens — and cannot be projected on a screen. Magnifying glasses produce virtual images.
  - q: What does negative magnification mean?
    a: The image is upside down (inverted). Positive magnification means upright.
  - q: What is a dioptre?
    a: Lens power in reciprocal metres: P = 1 ÷ f. A +2.5 dioptre reading lens has a focal length of 40 cm.
related: [physics/snells-law, biology/magnification, biology/field-of-view, physics/wavelength-frequency]
''', f'''
## How to use this calculator

Enter the **focal length** and **object distance**. The calculator finds the image distance, magnification and lens power. Use the sign convention below. Any two of f, dₒ and dᵢ determine the third.

## The equations

<p class="formula">1/f = 1/dₒ + 1/dᵢ &nbsp;·&nbsp; m = −dᵢ ÷ dₒ &nbsp;·&nbsp; P = 1 ÷ f</p>

## Sign convention (real-is-positive)

| Quantity | Positive | Negative |
|---|---|---|
| f | Converging lens, concave mirror | Diverging lens, convex mirror |
| dᵢ | Real image | Virtual image |
| m | Upright image | Inverted image |

## Converging lens, f = 10 cm

| Object distance | Image distance | Magnification | Image |
|---|---|---|---|
''' + ''.join(f"| {do} cm | {lens(10,do):.1f} cm | {-lens(10,do)/do:.2f} | {'real, inverted' if lens(10,do)>0 else 'virtual, upright'}{', enlarged' if abs(lens(10,do)/do)>1 else ', reduced'} |\n" for do in [50, 30, 20, 15, 12, 8, 5]) + '''
- Object beyond 2f: real, inverted, smaller image (cameras, eyes).
- Object at 2f: same-size inverted image.
- Object between f and 2f: enlarged inverted image (projectors).
- Object inside f: virtual, upright, enlarged (magnifying glass).

## Lenses in contact

Powers add: P = P₁ + P₂. Two +5 D lenses together make a +10 D lens with a 10 cm focal length.

## Spectacles

Short-sighted (myopic) people wear diverging lenses with negative dioptres; long-sighted people and reading glasses use positive lenses.
''')

def dop(f, v, vo, vs): return f*(v+vo)/(v-vs)
page('physics', 'doppler-effect', f'''
title: Doppler Effect Calculator (Sound)
description: Calculate the frequency heard from a moving sound source or by a moving observer using the Doppler effect formula — sirens, trains and more.
category: physics
keywords: [doppler effect calculator, doppler shift, observed frequency, moving source frequency, siren frequency, doppler formula]
updated: {D}
variables:
  - {{ id: f, label: Source frequency, suffix: Hz, default: 700, min: 0 }}
  - {{ id: v, label: Speed of sound, family: velocity, unit: ms, default: 343, min: 1 }}
  - {{ id: vo, label: Observer speed (towards the source is positive), family: velocity, unit: kmh, imperialUnit: mph, default: 0 }}
  - {{ id: vs, label: Source speed (towards the observer is positive), family: velocity, unit: kmh, imperialUnit: mph, default: 72 }}
  - {{ id: fo, label: Observed frequency, suffix: Hz, min: 0, decimals: 1 }}
  - {{ id: sh, label: Shift, family: percent, unit: '%' }}
equations:
  - fo = f * (v + vo) / (v - vs)
  - sh = fo / f - 1
faq:
  - q: What is the Doppler effect?
    a: The change in frequency heard when a sound source and listener move relative to each other — higher when approaching, lower when moving apart.
  - q: Why does a siren drop in pitch as it passes?
    a: While the ambulance approaches, sound waves are squeezed together (higher pitch); after it passes, they are stretched out (lower pitch).
  - q: How do I calculate a receding source?
    a: Enter the source speed as a negative number. A source moving away at 72 km/h makes a 700 Hz siren sound about 660 Hz.
  - q: Does the Doppler effect apply to light?
    a: Yes. Light from galaxies moving away is shifted towards red (redshift), which is how astronomers know the universe is expanding. Light uses a relativistic formula.
related: [physics/wavelength-frequency, physics/speed-distance-time, conversion/speed-converter, physics/decibel]
''', f'''
## How to use this calculator

Enter the **source frequency**, the **speed of sound** (343 m/s in air at 20 °C) and the speeds of the **observer** and **source**. Use positive speeds when moving **towards** each other and negative when moving **apart**.

## The formula

<p class="formula">f′ = f × (v + v<sub>o</sub>) ÷ (v − v<sub>s</sub>)</p>

## Siren passing at 72 km/h (700 Hz)

| Situation | Frequency heard |
|---|---|
| Approaching | {dop(700,343,0,20):.0f} Hz |
| At the moment it passes | 700 Hz |
| Moving away | {dop(700,343,0,-20):.0f} Hz |

The drop of about 80 Hz — roughly a whole tone — is what you hear as the siren goes by.

## Speed of sound in different media

| Medium | Speed |
|---|---|
| Air, 0 °C | 331 m/s |
| Air, 20 °C | 343 m/s |
| Water | about 1,480 m/s |
| Steel | about 5,900 m/s |

Speed of sound in air rises about 0.6 m/s for each °C.

## Uses of the Doppler effect

- **Radar speed guns** measure the frequency shift of reflected radio waves.
- **Doppler ultrasound** measures blood flow in arteries and in pregnancy scans.
- **Weather radar** detects wind speeds inside storms.
- **Astronomy** measures how fast stars and galaxies move towards or away from us.

## Sonic booms

If a source moves faster than sound, the formula breaks down — waves pile up into a shock wave heard as a sonic boom.
''')

def coul(q1, q2, r): return 8.9875517923e9*q1*q2/r**2
page('physics', 'coulombs-law', f'''
title: Coulomb's Law Calculator (Electric Force)
description: Calculate the electrostatic force between two point charges, or the distance or charge needed for a given force, using Coulomb's law.
category: physics
keywords: [coulombs law calculator, electric force calculator, electrostatic force, point charges, coulomb constant, force between charges]
updated: {D}
variables:
  - {{ id: q1, label: Charge 1, suffix: µC, default: 2 }}
  - {{ id: q2, label: Charge 2, suffix: µC, default: -3 }}
  - {{ id: r, label: Distance between charges, family: length, unit: cm, imperialUnit: in, default: 10, min: 0 }}
  - {{ id: F, label: Force (negative = attraction), family: force, unit: N, imperialUnit: lbf }}
equations:
  - F = 8.9875517923e9 * q1 * 1e-6 * q2 * 1e-6 / r^2
faq:
  - q: What is Coulomb's law?
    a: F = k q₁q₂ ÷ r², where k ≈ 8.99 × 10⁹ N·m²/C². Like charges repel and opposite charges attract.
  - q: What does a negative force mean?
    a: The charges have opposite signs, so the force is attractive.
  - q: How does distance affect the force?
    a: Force falls with the square of distance. Doubling the distance cuts the force to a quarter.
  - q: How big is one coulomb?
    a: Very large for static charges — about 6.24 × 10¹⁸ electrons. Everyday static charges are usually nanocoulombs to microcoulombs.
related: [physics/gravitational-force, physics/ohms-law, physics/force, physics/rc-time-constant]
''', f'''
## How to use this calculator

Enter the two **charges** in microcoulombs (use a minus sign for negative charges) and the **distance** between them. The calculator gives the force in newtons. A negative result means attraction; positive means repulsion.

## The formula

<p class="formula">F = k × q₁ × q₂ ÷ r²</p>

with k = 8.9875 × 10⁹ N·m²/C² (1 ÷ 4πε₀).

## Example

+2 µC and −3 µC, 10 cm apart:

F = 8.99 × 10⁹ × (2 × 10⁻⁶) × (−3 × 10⁻⁶) ÷ 0.1² = **{coul(2e-6,-3e-6,0.1):.2f} N** (attractive)

## Force vs distance (+1 µC and +1 µC)

| Distance | Force |
|---|---|
''' + ''.join(f"| {r} cm | {coul(1e-6,1e-6,r/100):.3g} N |\n" for r in [1, 2, 5, 10, 20, 50, 100]) + '''
## Electric vs gravitational force

Between a proton and an electron, the electric force is about **10³⁹ times** stronger than gravity. Gravity dominates on large scales only because matter is usually electrically neutral.

## In a material

In a medium other than vacuum, divide by the relative permittivity εᵣ. In water (εᵣ ≈ 80) the force between ions is about 80 times weaker, which is why salts dissolve.

## Practical charges

| Situation | Typical charge |
|---|---|
| Rubbed balloon | 0.1–1 µC |
| Van de Graaff dome | 1–10 µC |
| Lightning strike | 5–20 C |
''')

page('physics', 'gravitational-force', f'''
title: Gravitational Force Calculator (Newton's Law of Gravitation)
description: Calculate the gravitational force between two masses with F = Gm₁m₂/r² — from everyday objects to planets and moons.
category: physics
keywords: [gravitational force calculator, newtons law of gravitation, universal gravitation, gravity between two objects, gravitational constant, force of gravity]
updated: {D}
variables:
  - {{ id: m1, label: Mass 1, suffix: kg, default: 5.972e24, min: 0 }}
  - {{ id: m2, label: Mass 2, suffix: kg, default: 7.342e22, min: 0 }}
  - {{ id: r, label: Distance between centres, family: length, unit: km, imperialUnit: mi, default: 384400, min: 0 }}
  - {{ id: F, label: Gravitational force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
equations:
  - F = 6.6743e-11 * m1 * m2 / r^2
faq:
  - q: What is Newton's law of universal gravitation?
    a: Every mass attracts every other mass with a force F = Gm₁m₂ ÷ r², where G = 6.674 × 10⁻¹¹ N·m²/kg².
  - q: What is the force between the Earth and the Moon?
    a: About 1.98 × 10²⁰ N.
  - q: Why don't I feel gravity from people near me?
    a: Because G is tiny. Two 70 kg people 1 m apart attract each other with about 3.3 × 10⁻⁷ N — far too small to notice.
  - q: Do I use the surface distance?
    a: No — use the distance between the centres of mass. For a person on Earth, that is Earth's radius.
related: [physics/weight, physics/escape-velocity, physics/orbital-period, physics/coulombs-law]
''', f'''
## How to use this calculator

Enter the two **masses** in kilograms (scientific notation like 5.972e24 works) and the **distance between their centres**. The default values are the Earth and the Moon.

## The formula

<p class="formula">F = G × m₁ × m₂ ÷ r²</p>

with G = 6.6743 × 10⁻¹¹ N·m²/kg².

## Examples

| Pair | Masses | Distance | Force |
|---|---|---|---|
| Earth–Moon | 5.97 × 10²⁴ and 7.34 × 10²² kg | 384,400 km | {G*5.972e24*7.342e22/3.844e8**2:.3g} N |
| Earth–Sun | 5.97 × 10²⁴ and 1.99 × 10³⁰ kg | 149.6 million km | {G*5.972e24*1.989e30/1.496e11**2:.3g} N |
| Person on Earth | 70 kg and Earth | 6,371 km | {G*70*5.972e24/6.371e6**2:.0f} N |
| Two people | 70 kg each | 1 m | {G*70*70:.2g} N |

## Inverse-square law

Double the distance and the force falls to a quarter; triple it and it falls to a ninth. At the International Space Station's altitude (about 400 km), gravity is still about 90% of its surface value.

## Gravity at the surface

Setting m₂ as a small object gives the gravitational acceleration: g = G × M ÷ r². For Earth this gives about 9.82 m/s², close to the standard 9.81 m/s². See the [weight calculator](/physics/weight/) for other planets.

## Measuring G

Henry Cavendish first measured G in 1798 with a torsion balance, using lead spheres. It remains one of the least precisely known fundamental constants.
''')

page('physics', 'escape-velocity', f'''
title: Escape Velocity Calculator
description: Calculate the escape velocity from any planet, moon or star from its mass and radius — with values for the Earth, Moon, Mars and more.
category: physics
keywords: [escape velocity calculator, escape velocity of earth, escape speed, 11.2 km/s, planet escape velocity, sqrt 2gm/r]
updated: {D}
variables:
  - {{ id: M, label: Mass of the body, suffix: kg, default: 5.972e24, min: 0 }}
  - {{ id: R, label: Radius (or distance from centre), family: length, unit: km, imperialUnit: mi, default: 6371, min: 0 }}
  - {{ id: v, label: Escape velocity, family: velocity, unit: kmh, imperialUnit: mph, min: 0 }}
  - {{ id: g, label: Surface gravity, suffix: m/s², min: 0, decimals: 3 }}
equations:
  - v = sqrt(2 * 6.6743e-11 * M / R)
  - g = 6.6743e-11 * M / R^2
faq:
  - q: What is the escape velocity of Earth?
    a: About 11.2 km/s (40,300 km/h) from the surface, ignoring air resistance.
  - q: Does escape velocity depend on the mass of the rocket?
    a: No. It depends only on the mass and radius of the planet. A heavier rocket needs more energy, but the same speed.
  - q: Do rockets really travel at escape velocity?
    a: Not necessarily — rockets keep firing their engines, so they can escape at lower speeds. Escape velocity is the speed needed for an unpowered object launched once.
  - q: What has an escape velocity faster than light?
    a: A black hole, inside its event horizon.
related: [physics/orbital-period, physics/gravitational-force, physics/weight, physics/kinetic-energy]
''', f'''
## How to use this calculator

Enter the **mass** of the planet or moon and its **radius**. The calculator gives the escape velocity and the surface gravity. Defaults are for the Earth. Choose km/s by switching to m/s and dividing by 1,000, or read km/h directly.

## The formula

<p class="formula">v<sub>esc</sub> = √(2GM ÷ R)</p>

It comes from setting kinetic energy equal to the gravitational energy needed to reach infinity: ½mv² = GMm ÷ R.

## Escape velocities in the solar system

| Body | Mass (kg) | Radius (km) | Escape velocity |
|---|---|---|---|
''' + ''.join(f"| {n} | {m:.3g} | {r:,} | {math.sqrt(2*G*m/(r*1000))/1000:.2f} km/s |\n" for n, m, r in [('Moon', 7.342e22, 1737), ('Mercury', 3.301e23, 2440), ('Mars', 6.417e23, 3390), ('Venus', 4.867e24, 6052), ('Earth', 5.972e24, 6371), ('Neptune', 1.024e26, 24622), ('Saturn', 5.683e26, 58232), ('Jupiter', 1.898e27, 69911), ('Sun', 1.989e30, 696340)]) + '''
## Escape vs orbital velocity

Escape velocity is √2 (about 1.414) times the circular orbital velocity at the same distance. Low Earth orbit needs about 7.8 km/s; escaping from that altitude needs about 11 km/s. See the [orbital period calculator](/physics/orbital-period/).

## Why the Moon has no atmosphere

Gas molecules move at hundreds of metres per second. On the Moon, with an escape velocity of only 2.4 km/s, the fastest molecules eventually escape, so it cannot hold a thick atmosphere.
''')

def orb(M, a): return 2*pi*math.sqrt(a**3/(G*M))
page('physics', 'orbital-period', f'''
title: Orbital Period Calculator (Kepler's Third Law)
description: Calculate the orbital period and speed of a satellite or planet from the central mass and orbit radius — ISS, GPS, geostationary orbits and more.
category: physics
keywords: [orbital period calculator, keplers third law, satellite orbit calculator, orbital speed, geostationary orbit, iss orbit period, orbital velocity]
updated: {D}
variables:
  - {{ id: M, label: Central mass, suffix: kg, default: 5.972e24, min: 0 }}
  - {{ id: a, label: Orbit radius (from centre), family: length, unit: km, imperialUnit: mi, default: 6779, min: 0 }}
  - {{ id: T, label: Orbital period, family: seconds, unit: min, min: 0 }}
  - {{ id: v, label: Orbital speed, family: velocity, unit: kmh, imperialUnit: mph, min: 0 }}
equations:
  - T = 2 * pi * sqrt(a^3 / (6.6743e-11 * M))
  - v = sqrt(6.6743e-11 * M / a)
faq:
  - q: What is Kepler's third law?
    a: The square of the orbital period is proportional to the cube of the orbit's semi-major axis: T² = 4π²a³ ÷ (GM).
  - q: How long does the ISS take to orbit Earth?
    a: About 92–93 minutes at roughly 400–420 km altitude, travelling at about 27,600 km/h.
  - q: What is a geostationary orbit?
    a: A circular orbit 35,786 km above the equator with a period of one sidereal day (23 h 56 min), so the satellite stays above one point on Earth.
  - q: Should I enter altitude or radius?
    a: Radius from the centre — add the planet’s radius to the altitude. For Earth, add 6,371 km.
related: [physics/escape-velocity, physics/gravitational-force, physics/centripetal-force, physics/weight]
''', f'''
## How to use this calculator

Enter the **central mass** (Earth by default) and the **orbit radius** measured from the centre (altitude + planet radius). You get the period and the orbital speed for a circular orbit.

## The formulas

<p class="formula">T = 2π √(a³ ÷ GM) &nbsp;·&nbsp; v = √(GM ÷ a)</p>

## Earth orbits

| Orbit | Altitude | Period | Speed |
|---|---|---|---|
''' + ''.join(f"| {n} | {h:,} km | {(lambda t: f'{int(t//3600)} h {int(t%3600//60)} min')(orb(5.972e24,(h+6371)*1000))} | {math.sqrt(G*5.972e24/((h+6371)*1000))*3.6:,.0f} km/h |\n" for n, h in [('Low Earth orbit (ISS)', 420), ('Starlink shell', 550), ('Polar weather satellites', 850), ('GPS (MEO)', 20200), ('Geostationary', 35786), ('Moon', 378029)]) + '''
## Kepler's law for planets

For bodies orbiting the Sun, T² (in years) ≈ a³ (in astronomical units). Mars at 1.52 AU has a period of √(1.52³) ≈ **1.88 years**.

## Higher orbits are slower

Satellites in higher orbits move more slowly and take longer to go round. To catch up with a satellite ahead, a spacecraft actually drops to a lower orbit first.

## Elliptical orbits

For an elliptical orbit, use the semi-major axis (average of the closest and farthest distances from the centre) as a. The period depends only on a, not on how elongated the orbit is.
''')

page('physics', 'buoyancy', f'''
title: Buoyancy Calculator (Archimedes' Principle)
description: Calculate the buoyant force on an object in water or another fluid, its apparent weight and whether it will float — using Archimedes' principle.
category: physics
keywords: [buoyancy calculator, buoyant force, archimedes principle, will it float, apparent weight, displacement calculator, upthrust]
updated: {D}
variables:
  - {{ id: V, label: Volume submerged, family: volume, unit: L, imperialUnit: ft3, default: 10, min: 0 }}
  - {{ id: rf, label: Fluid density, family: density, unit: kgm3, imperialUnit: lbft3, default: 1000, min: 0 }}
  - {{ id: m, label: Object mass, family: mass, unit: kg, imperialUnit: lb, default: 8, min: 0 }}
  - {{ id: Fb, label: Buoyant force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: W, label: Weight, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: Wa, label: Apparent weight (negative = floats up), family: force, unit: N, imperialUnit: lbf }}
equations:
  - Fb = rf * g0 * V
  - W = m * g0
  - Wa = W - Fb
faq:
  - q: What is Archimedes' principle?
    a: An object immersed in a fluid is pushed up by a force equal to the weight of fluid it displaces.
  - q: How do I know if something will float?
    a: If its average density is less than the fluid’s, it floats. In the calculator, a negative apparent weight when fully submerged means it will float up.
  - q: How much of a floating object is underwater?
    a: The fraction submerged equals object density ÷ fluid density. Ice (917 kg/m³) floats with about 90% underwater in seawater.
  - q: Why do ships made of steel float?
    a: Their hollow hulls displace a large volume of water, so their average density is less than water.
related: [physics/density, physics/pressure, engineering/hydrostatic-pressure, physics/weight]
''', '''
## How to use this calculator

Enter the **volume** of the object under the fluid, the **fluid density** and the object's **mass**. You get the buoyant force, the object's weight and its apparent weight while submerged. A negative apparent weight means the object would rise and float.

## The formula

<p class="formula">F<sub>b</sub> = ρ<sub>fluid</sub> × g × V<sub>submerged</sub></p>

## Fluid densities

| Fluid | Density (kg/m³) |
|---|---|
| Fresh water | 1,000 |
| Seawater | 1,025 |
| Dead Sea water | about 1,240 |
| Olive oil | 910 |
| Mercury | 13,534 |
| Air (20 °C) | 1.2 |

## Example

A 10 L object weighing 8 kg, fully submerged in fresh water:

- Buoyant force = 1,000 × 9.81 × 0.01 = **98.1 N**
- Weight = 8 × 9.81 = **78.5 N**
- Apparent weight = **−19.6 N** → it floats, with 80% of its volume underwater.

## Weighing in water

Apparent weight lets you find density without measuring volume: density = ρ<sub>water</sub> × weight in air ÷ (weight in air − weight in water). Archimedes is said to have used this to test whether a crown was pure gold.

## Hot-air balloons

Balloons float in air for the same reason. Heating the air inside lowers its density; the difference in density times the balloon volume gives the lift.
''')

page('physics', 'heat-conduction', f'''
title: Heat Conduction Calculator (Fourier's Law)
description: Calculate heat flow through a wall, window or insulation layer using Fourier's law — with thermal conductivity, U-values and R-values.
category: physics
keywords: [heat conduction calculator, fouriers law, heat transfer through wall, thermal conductivity, u value calculator, r value, heat loss calculator]
updated: {D}
variables:
  - {{ id: k, label: Thermal conductivity (k), suffix: W/m·K, default: 0.04, min: 0 }}
  - {{ id: A, label: Area, family: area, unit: m2, imperialUnit: ft2, default: 10, min: 0 }}
  - {{ id: dT, label: Temperature difference, family: tempdiff, unit: K, imperialUnit: F, default: 20, min: 0 }}
  - {{ id: d, label: Thickness, family: length, unit: mm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: Q, label: Heat flow, family: power, unit: W, min: 0 }}
  - {{ id: U, label: U-value, suffix: W/m²·K, min: 0, decimals: 3 }}
  - {{ id: Rv, label: R-value, suffix: m²·K/W, min: 0, decimals: 2 }}
equations:
  - Q = k * A * dT / d
  - U = k / d
  - Rv = d / k
faq:
  - q: What is Fourier's law?
    a: Heat flow through a material is proportional to its conductivity, area and temperature difference, and inversely proportional to its thickness — Q = kAΔT ÷ d.
  - q: What is the difference between U-value and R-value?
    a: R-value measures resistance to heat flow (higher is better insulation). U-value is its inverse, heat flow per m² per degree (lower is better).
  - q: How do I combine layers?
    a: Add the R-values of each layer, then U = 1 ÷ total R. Include surface resistances for walls and windows.
  - q: How much heat does a wall lose in a day?
    a: Multiply heat flow in watts by 24 and divide by 1,000 for kWh per day.
related: [chemistry/specific-heat, engineering/heat-duty, engineering/thermal-expansion, everyday-life/electricity-cost]
''', '''
## How to use this calculator

Enter the material's **thermal conductivity**, the **area**, the **temperature difference** across it and its **thickness**. You get the heat flow, U-value and R-value of that layer.

## Fourier's law

<p class="formula">Q = k × A × ΔT ÷ d</p>

## Thermal conductivity of materials

| Material | k (W/m·K) |
|---|---|
| Copper | 385–400 |
| Aluminium | 205–237 |
| Steel | 45–50 |
| Concrete | 1.0–1.8 |
| Brick | 0.6–1.0 |
| Glass | about 1.0 |
| Water | 0.6 |
| Wood (softwood) | 0.12–0.15 |
| Mineral wool | 0.032–0.040 |
| Expanded polystyrene (EPS) | 0.033–0.038 |
| Polyurethane (PIR) foam | 0.022–0.028 |
| Still air | 0.026 |

## Example

10 m² of 100 mm mineral wool (k = 0.04) with a 20 °C difference:

- Q = 0.04 × 10 × 20 ÷ 0.1 = **80 W**
- U = 0.4 W/m²·K, R = 2.5 m²·K/W

The same area of 100 mm concrete would lose 3,600 W — 45 times more.

## Windows

| Glazing | Typical U-value (W/m²·K) |
|---|---|
| Single glazing | 5.0–5.8 |
| Double glazing | 2.6–2.8 |
| Double, low-e, argon | 1.2–1.6 |
| Triple glazing | 0.6–0.8 |

## Imperial R-values

US R-values use ft²·°F·h/BTU. Multiply SI R-values by 5.678 to convert: R 2.5 SI ≈ R-14 US.
''')

page('physics', 'torque', f'''
title: Torque Calculator (Force × Lever Arm)
description: Calculate torque from force and lever length at any angle — or the force needed to reach a target torque with a spanner or wrench.
category: physics
keywords: [torque calculator, torque formula, force times distance, moment of force, wrench torque, lever arm, newton metre]
updated: {D}
variables:
  - {{ id: F, label: Force, family: force, unit: N, imperialUnit: lbf, default: 200, min: 0 }}
  - {{ id: r, label: Lever arm length, family: length, unit: m, imperialUnit: ft, default: 0.3, min: 0 }}
  - {{ id: th, label: Angle between force and lever, family: angle, unit: deg, default: 90, min: 0, max: 3.1416 }}
  - {{ id: T, label: Torque, family: torque, unit: Nm, imperialUnit: lbft, min: 0 }}
equations:
  - T = F * r * sin(th)
faq:
  - q: What is the torque formula?
    a: τ = F × r × sin θ, where F is the force, r the distance from the pivot and θ the angle between them.
  - q: Why is a longer spanner easier to use?
    a: Torque is force × distance. Doubling the handle length halves the force needed for the same torque.
  - q: What is the difference between torque and work?
    a: Both use newton-metres, but torque is a turning effect (a vector), while work is energy (a scalar), usually written in joules.
  - q: How do I convert N·m to ft-lb?
    a: Multiply by 0.7376. 100 N·m ≈ 73.8 lbf·ft.
related: [conversion/torque-converter, engineering/torque-power-speed, physics/force, physics/work-and-power]
''', '''
## How to use this calculator

Enter the **force**, the **lever arm length** (distance from the pivot to where the force acts) and the **angle** between them (90° for a push at right angles). The calculator gives the torque. To find the force needed for a given torque, press × on Force.

## The formula

<p class="formula">τ = F × r × sin θ</p>

Torque is greatest when the force is perpendicular to the lever (θ = 90°) and zero when pushing along the lever.

## Force needed for common torques

| Torque | 20 cm spanner | 30 cm spanner | 50 cm breaker bar |
|---|---|---|---|
''' + ''.join(f"| {t} N·m | {t/0.2:.0f} N ({t/0.2/9.81:.1f} kgf) | {t/0.3:.0f} N ({t/0.3/9.81:.1f} kgf) | {t/0.5:.0f} N ({t/0.5/9.81:.1f} kgf) |\n" for t in [25, 50, 100, 150, 250]) + '''
## Levers and balance

A lever balances when torques on both sides are equal: F₁ × r₁ = F₂ × r₂. A 50 kg child 2 m from a see-saw pivot balances a 100 kg adult 1 m from it.

## Torque in everyday life

| Task | Typical torque |
|---|---|
| Opening a jar lid | 1–3 N·m |
| Bicycle pedal (hard effort) | 50–100 N·m |
| Car wheel nuts | 80–140 N·m |
| Small car engine (peak) | 100–250 N·m |

## Torque wrenches

Use a calibrated torque wrench for bolts with a specified torque. Hold the handle at its marked grip point — pulling elsewhere changes the effective lever length.
''')

page('physics', 'decibel', f'''
title: Decibel Calculator (dB Power and Voltage Ratios)
description: Convert power and voltage ratios to decibels and back — dB gain and loss for audio, RF and signal chains, plus sound levels.
category: physics
keywords: [decibel calculator, db calculator, power ratio to db, voltage ratio to db, db gain, 3 db, 10 log, 20 log, sound level]
updated: {D}
variables:
  - {{ id: P1, label: Reference power (P₁), family: power, unit: W, default: 1, min: 0 }}
  - {{ id: P2, label: Power (P₂), family: power, unit: W, default: 100, min: 0 }}
  - {{ id: dbp, label: Power ratio in dB, suffix: dB, decimals: 2 }}
  - {{ id: V1, label: Reference voltage (V₁), family: voltage, unit: V, default: 1, min: 0 }}
  - {{ id: V2, label: Voltage (V₂), family: voltage, unit: V, default: 10, min: 0 }}
  - {{ id: dbv, label: Voltage ratio in dB, suffix: dB, decimals: 2 }}
equations:
  - dbp = 10 * log10(P2 / P1)
  - dbv = 20 * log10(V2 / V1)
faq:
  - q: Why is power 10 log but voltage 20 log?
    a: Power is proportional to voltage squared, so 10 log(V²) = 20 log(V). A tenfold voltage increase is a hundredfold power increase — both 20 dB.
  - q: What does 3 dB mean?
    a: A doubling of power (or halving for −3 dB). For voltage, doubling is about 6 dB.
  - q: How do I add gains in a signal chain?
    a: Add the dB values. An amplifier of +20 dB followed by a cable loss of −3 dB gives +17 dB overall.
  - q: What is dBm?
    a: Power relative to 1 mW. 0 dBm = 1 mW, 30 dBm = 1 W.
related: [math/logarithm, physics/wavelength-frequency, physics/ohms-law, physics/doppler-effect]
''', '''
## How to use this calculator

Use the top section for **power** ratios and the bottom for **voltage** (or current, or sound pressure) ratios. Enter the reference and the measured value to get decibels, or enter dB and a reference to find the other value.

## The formulas

<p class="formula">dB = 10 log₁₀(P₂ ÷ P₁) &nbsp;·&nbsp; dB = 20 log₁₀(V₂ ÷ V₁)</p>

## dB reference table

| dB | Power ratio | Voltage ratio |
|---|---|---|
''' + ''.join(f"| {d:+d} | {10**(d/10):.4g}× | {10**(d/20):.4g}× |\n" for d in [-20, -10, -6, -3, 0, 3, 6, 10, 20, 30, 40, 60]) + '''
## dB units with references

| Unit | Reference |
|---|---|
| dBm | 1 mW |
| dBW | 1 W |
| dBV | 1 V |
| dBu | 0.775 V |
| dB SPL | 20 µPa sound pressure |

## Sound levels (dB SPL)

| Sound | Level |
|---|---|
| Threshold of hearing | 0 dB |
| Quiet room | 30 dB |
| Normal conversation | 60 dB |
| Busy traffic | 80 dB |
| Hearing damage risk with long exposure | 85 dB and above |
| Rock concert | 110 dB |
| Pain threshold | 120–130 dB |

Every 10 dB increase sounds roughly twice as loud and carries ten times the sound power.

## Signal chains

In RF and audio systems, gains and losses in dB simply add, which is why engineers prefer them to multiplying ratios.
''')

# ============================ ENGINEERING ============================
def vnotch(h, th=90, cd=0.585): return 8/15*cd*math.sqrt(2*g0)*math.tan(math.radians(th)/2)*h**2.5
def rect(h, L): return 1.84*(L-0.2*h)*h**1.5
page('engineering', 'weir-flow', f'''
title: Weir Flow Calculator (V-Notch and Rectangular)
description: Calculate open-channel flow over a V-notch or rectangular weir from the head — for effluent, irrigation and flow measurement.
category: engineering
keywords: [weir flow calculator, v notch weir, rectangular weir, francis formula, open channel flow, weir head flow, thomson weir]
updated: {D}
variables:
  - id: t
    label: Weir type
    default: 1
    options:
      - {{ label: V-notch (triangular), value: 1 }}
      - {{ label: Rectangular (contracted, Francis), value: 0 }}
  - {{ id: h, label: Head above crest or notch, family: length, unit: mm, imperialUnit: in, default: 150, min: 0 }}
  - {{ id: th, label: V-notch angle, family: angle, unit: deg, default: 90, min: 0.1, max: 3.1 }}
  - {{ id: cd, label: Discharge coefficient (V-notch), default: 0.585, min: 0.1, max: 1 }}
  - {{ id: L, label: Crest length (rectangular), family: length, unit: m, imperialUnit: ft, default: 0.5, min: 0 }}
  - {{ id: Q, label: Flow rate, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
equations:
  - Q = t * (8/15) * cd * sqrt(2*g0) * tan(th/2) * h^2.5 + (1 - t) * 1.84 * (L - 0.2*h) * h^1.5
faq:
  - q: What is a V-notch weir used for?
    a: Measuring small and varying flows accurately — the triangular shape gives good resolution at low heads. 90° V-notches are common for effluent and wastewater.
  - q: Where should I measure the head?
    a: Upstream of the weir, at a distance of about 4–5 times the maximum head, where the water surface is level and unaffected by drawdown.
  - q: What is the Francis formula?
    a: Q = 1.84 (L − 0.2h) h^1.5 in SI units, for a rectangular weir with end contractions on both sides.
  - q: How accurate are weir formulas?
    a: Typically within 2–5% when the weir is installed to standard (sharp crest, free fall, ventilated nappe, adequate approach channel).
related: [engineering/orifice-flow, engineering/pipe-flow-velocity, engineering/hydrostatic-pressure, conversion/flow-rate-converter]
''', f'''
## How to use this calculator

Choose the **weir type** and enter the **head** — the height of the water surface above the bottom of the notch or the crest. For a V-notch, set the notch angle and discharge coefficient; for a rectangular weir, set the crest length.

## The formulas

**V-notch (Kindsvater–Shen form)**

<p class="formula">Q = (8/15) × C<sub>d</sub> × √(2g) × tan(θ/2) × h<sup>5/2</sup></p>

**Rectangular, contracted (Francis)**

<p class="formula">Q = 1.84 × (L − 0.2h) × h<sup>3/2</sup></p>

with Q in m³/s and L and h in metres.

## 90° V-notch flow table

| Head | Flow |
|---|---|
''' + ''.join(f"| {h} mm | {vnotch(h/1000)*3600:.2f} m³/h ({vnotch(h/1000)*1000:.2f} L/s) |\n" for h in [25, 50, 75, 100, 150, 200, 250, 300]) + f'''
Flow rises with h<sup>2.5</sup>, so doubling the head increases flow about 5.7 times.

## Rectangular weir, 0.5 m crest

| Head | Flow |
|---|---|
''' + ''.join(f"| {h} mm | {rect(h/1000,0.5)*3600:.1f} m³/h |\n" for h in [25, 50, 100, 150, 200]) + '''
## Installation guidelines

- Sharp, thin crest (bevelled downstream).
- Free-falling, aerated nappe — the water must spring clear of the weir plate.
- Head measured at 4–5 × h<sub>max</sub> upstream with a stilling well or level sensor.
- Approach channel straight and wide enough for low approach velocity.
- Minimum head about 50 mm for V-notches to avoid surface-tension errors.

## Automating with level sensors

Ultrasonic or radar level transmitters above the weir measure head continuously. The flow computer then applies the weir equation — a common setup for effluent flow monitoring.
''')

def venturi(D, d, dp, rho, cd=0.985):
    b = d/D; A = pi*d*d/4; return cd*A*math.sqrt(2*dp/(rho*(1-b**4)))
page('engineering', 'venturi-flow', f'''
title: Venturi Meter Flow Calculator
description: Calculate liquid flow through a Venturi tube from the differential pressure, inlet and throat diameters — with permanent pressure loss.
category: engineering
keywords: [venturi meter calculator, venturi flow, venturi tube, differential pressure flow, throat diameter, beta ratio, venturi coefficient]
updated: {D}
variables:
  - {{ id: D, label: Inlet (pipe) diameter, family: length, unit: mm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: d, label: Throat diameter, family: length, unit: mm, imperialUnit: in, default: 60, min: 0 }}
  - {{ id: b, label: Beta ratio (d/D), min: 0, max: 0.99, decimals: 3 }}
  - {{ id: cd, label: Discharge coefficient, default: 0.985, min: 0.5, max: 1 }}
  - {{ id: dP, label: Differential pressure, family: pressure, unit: mbar, imperialUnit: inH2O, default: 200, min: 0 }}
  - {{ id: rho, label: Liquid density, family: density, unit: kgm3, imperialUnit: lbft3, default: 998, min: 0 }}
  - {{ id: Q, label: Flow rate, family: flow, unit: m3h, imperialUnit: gpm, min: 0 }}
  - {{ id: v, label: Throat velocity, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
equations:
  - b = d / D
  - Q = cd * (pi * d^2 / 4) * sqrt(2 * dP / (rho * (1 - b^4)))
  - v = Q / (pi * d^2 / 4)
faq:
  - q: What is a typical Venturi discharge coefficient?
    a: About 0.98–0.995 for classical Venturi tubes, much higher than the 0.6 of an orifice plate, because flow follows the smooth contraction.
  - q: Why use a Venturi instead of an orifice plate?
    a: Venturis recover most of the pressure drop (permanent loss typically 5–20% of the DP), saving pumping energy, and handle dirty or slurry flows better.
  - q: What beta ratio is typical?
    a: Between about 0.4 and 0.75 under ISO 5167-4.
  - q: How does a Venturi measure flow?
    a: Fluid speeds up in the throat, lowering its pressure (Bernoulli). The pressure difference between inlet and throat is proportional to flow squared.
related: [engineering/orifice-flow, engineering/dp-flow-square-root, engineering/pitot-tube-velocity, engineering/pipe-flow-velocity]
''', f'''
## How to use this calculator

Enter the **inlet diameter**, **throat diameter**, **discharge coefficient**, **differential pressure** and **liquid density**. You get the flow rate and the throat velocity. Press × on Differential pressure to find the DP for a given flow.

## The formula

<p class="formula">Q = C<sub>d</sub> × (πd²/4) × √[2ΔP ÷ (ρ(1 − β⁴))]</p>

## Example

D = 100 mm, d = 60 mm, ΔP = 200 mbar, water:

- β = 0.6, Q = **{venturi(0.1,0.06,20000,998)*3600:.1f} m³/h**

## Flow vs DP (100/60 mm, water)

| DP | Flow |
|---|---|
''' + ''.join(f"| {p} mbar | {venturi(0.1,0.06,p*100,998)*3600:.1f} m³/h |\n" for p in [10, 25, 50, 100, 200, 400, 600]) + '''
## Venturi vs other DP meters

| Element | Typical C<sub>d</sub> | Permanent pressure loss | Straight run needed |
|---|---|---|---|
| Classical Venturi | 0.98–0.995 | 5–20% of DP | Short |
| Flow nozzle | 0.93–0.99 | 30–60% | Medium |
| Orifice plate | 0.60–0.62 | 50–90% | Long |

## Where Venturis are used

- Large water and wastewater mains, where pumping energy matters.
- Slurries and dirty liquids, as the smooth shape does not trap solids.
- Irrigation and cooling-water systems.

For a 4–20 mA DP transmitter on a Venturi, use the [square-root flow calculator](/engineering/dp-flow-square-root/) to scale the signal.
''')

page('engineering', 'reactance', f'''
title: Reactance and Impedance Calculator (XL, XC and Z)
description: Calculate inductive reactance, capacitive reactance and series RLC impedance at any frequency — with phase angle.
category: engineering
keywords: [reactance calculator, inductive reactance, capacitive reactance, impedance calculator, rlc impedance, xl xc, phase angle]
updated: {D}
variables:
  - {{ id: f, label: Frequency, suffix: Hz, default: 50, min: 0 }}
  - {{ id: L, label: Inductance, suffix: mH, default: 100, min: 0 }}
  - {{ id: C, label: Capacitance, family: capacitance, unit: uF, default: 100, min: 0 }}
  - {{ id: R, label: Resistance (series), family: resistance, unit: ohm, default: 20, min: 0 }}
  - {{ id: XL, label: Inductive reactance (XL), family: resistance, unit: ohm, min: 0 }}
  - {{ id: XC, label: Capacitive reactance (XC), family: resistance, unit: ohm, min: 0 }}
  - {{ id: Z, label: Series RLC impedance (Z), family: resistance, unit: ohm, min: 0 }}
  - {{ id: ph, label: Phase angle, family: angle, unit: deg }}
equations:
  - XL = 2 * pi * f * L / 1000
  - XC = 1 / (2 * pi * f * C)
  - Z = sqrt(R^2 + (XL - XC)^2)
  - ph = atan((XL - XC) / R)
faq:
  - q: What is inductive reactance?
    a: The opposition of an inductor to AC current, XL = 2πfL. It rises with frequency.
  - q: What is capacitive reactance?
    a: The opposition of a capacitor to AC current, XC = 1 ÷ (2πfC). It falls with frequency.
  - q: What does the phase angle mean?
    a: Positive means the circuit is inductive (current lags voltage); negative means capacitive (current leads voltage).
  - q: When is impedance lowest?
    a: At resonance, when XL = XC. The impedance then equals R alone. See the resonant frequency calculator.
related: [engineering/resonant-frequency, physics/ohms-law, physics/rc-time-constant, engineering/kva-to-kw]
''', '''
## How to use this calculator

Enter the **frequency**, **inductance**, **capacitance** and series **resistance**. You get both reactances, the total impedance of the series RLC circuit and the phase angle. Set L or C to zero to analyse an RC or RL circuit (for an RL circuit, set C very large).

## The formulas

| Quantity | Formula |
|---|---|
| Inductive reactance | XL = 2πfL |
| Capacitive reactance | XC = 1 ÷ (2πfC) |
| Series impedance | Z = √(R² + (XL − XC)²) |
| Phase angle | φ = atan((XL − XC) ÷ R) |

## Reactance vs frequency

| Frequency | XL of 100 mH | XC of 100 µF |
|---|---|---|
''' + ''.join(f"| {f} Hz | {2*pi*f*0.1:.2f} Ω | {1/(2*pi*f*100e-6):.2f} Ω |\n" for f in [10, 50, 60, 100, 1000, 10000]) + '''
## Current in an AC circuit

Ohm's law works with impedance: I = V ÷ Z. With 230 V across the default circuit, the current is 230 ÷ Z.

## Power factor

For a series circuit, power factor = cos φ = R ÷ Z. Inductive loads such as motors have lagging power factor; capacitors are added to correct it — see the [kVA to kW converter](/engineering/kva-to-kw/).

## Applications

- **Filters**: reactance changes with frequency, letting RC and LC circuits pass or block certain frequencies.
- **Motors and transformers**: their inductance limits current and sets power factor.
- **Speaker crossovers**: inductors send bass to woofers; capacitors send treble to tweeters.
''')

def res(L, C): return 1/(2*pi*math.sqrt(L*C))
page('engineering', 'resonant-frequency', f'''
title: LC Resonant Frequency Calculator
description: Calculate the resonant frequency of an LC circuit — or the inductance or capacitance needed to tune to a frequency — for filters, oscillators and radios.
category: engineering
keywords: [resonant frequency calculator, lc resonance, lc circuit, tank circuit, resonance frequency formula, tuning circuit, 1/2pi sqrt lc]
updated: {D}
variables:
  - {{ id: L, label: Inductance, suffix: µH, default: 10, min: 0 }}
  - {{ id: C, label: Capacitance, family: capacitance, unit: nF, default: 100, min: 0 }}
  - {{ id: f, label: Resonant frequency, suffix: Hz, min: 0 }}
  - {{ id: w, label: Angular frequency, suffix: rad/s, min: 0 }}
equations:
  - f = 1 / (2 * pi * sqrt(L * 1e-6 * C))
  - w = 2 * pi * f
faq:
  - q: What is the resonant frequency formula?
    a: f = 1 ÷ (2π√(LC)), with L in henries and C in farads.
  - q: What happens at resonance?
    a: Inductive and capacitive reactances are equal and cancel. A series LC circuit has minimum impedance; a parallel LC circuit has maximum impedance.
  - q: How do I find the capacitor for a frequency?
    a: Enter the target frequency and inductance, then press × on Capacitance. C = 1 ÷ ((2πf)² L).
  - q: What limits real LC circuits?
    a: Resistance in the coil and capacitor losses, described by the quality factor Q. Higher Q gives a sharper resonance.
related: [engineering/reactance, physics/rc-time-constant, physics/wavelength-frequency, physics/ohms-law]
''', '''
## How to use this calculator

Enter the **inductance** in microhenries and the **capacitance**. The calculator gives the resonant frequency and angular frequency. To design a circuit for a target frequency, enter the frequency and one component and press × on the other.

## The formula

<p class="formula">f₀ = 1 ÷ (2π√(LC))</p>

## Resonant frequencies

| L | C | f₀ |
|---|---|---|
''' + ''.join(f"| {l} | {c} | {(lambda x: f'{x/1e6:.3f} MHz' if x>=1e6 else (f'{x/1e3:.2f} kHz' if x>=1e3 else f'{x:.1f} Hz'))(res(lv,cv))} |\n" for l, c, lv, cv in [('1 µH', '100 pF', 1e-6, 100e-12), ('10 µH', '100 pF', 10e-6, 100e-12), ('100 µH', '1 nF', 100e-6, 1e-9), ('10 µH', '100 nF', 10e-6, 100e-9), ('1 mH', '1 µF', 1e-3, 1e-6), ('100 mH', '100 µF', 0.1, 100e-6)]) + '''
## Series vs parallel resonance

| | Series LC | Parallel LC (tank) |
|---|---|---|
| Impedance at f₀ | Minimum (≈ R) | Maximum |
| Current at f₀ | Maximum | Minimum from source |
| Use | Band-pass in series path, notch filters | Oscillators, tuned amplifiers |

## Quality factor

For a series RLC circuit, Q = (1 ÷ R)√(L ÷ C), and bandwidth = f₀ ÷ Q. A higher Q gives a narrower, sharper response — important in radio tuning.

## Applications

- **AM/FM radio tuning**: a variable capacitor changes f₀ to select stations.
- **Oscillators**: LC tanks set the frequency in many RF circuits.
- **Harmonic filters**: tuned LC filters remove specific harmonics in power systems.
- **Wireless charging**: transmitter and receiver coils are tuned to the same resonant frequency.
''')

page('engineering', 'transformer-current', f'''
title: Transformer Current Calculator (Full-Load Amps)
description: Calculate primary and secondary full-load current of single-phase and three-phase transformers from kVA and voltages.
category: engineering
keywords: [transformer current calculator, transformer full load current, kva to amps transformer, primary current, secondary current, 3 phase transformer current]
updated: {D}
variables:
  - {{ id: S, label: Transformer rating, suffix: kVA, default: 500, min: 0 }}
  - id: ph
    label: Phases
    default: 1.7320508
    options:
      - {{ label: Three-phase, value: 1.7320508 }}
      - {{ label: Single-phase, value: 1 }}
  - {{ id: Vp, label: Primary voltage (line), family: voltage, unit: kV, default: 11, min: 0 }}
  - {{ id: Vs, label: Secondary voltage (line), family: voltage, unit: V, default: 433, min: 0 }}
  - {{ id: Ip, label: Primary full-load current, family: current, unit: A, min: 0 }}
  - {{ id: Is, label: Secondary full-load current, family: current, unit: A, min: 0 }}
  - {{ id: n, label: Voltage ratio, min: 0, decimals: 2 }}
equations:
  - Ip = S * 1000 / (ph * Vp)
  - Is = S * 1000 / (ph * Vs)
  - n = Vp / Vs
faq:
  - q: How do I calculate transformer full-load current?
    a: Three-phase I = kVA × 1,000 ÷ (√3 × V); single-phase I = kVA × 1,000 ÷ V, using line voltage.
  - q: What is the full-load current of a 500 kVA, 11 kV/433 V transformer?
    a: About 26.2 A on the 11 kV side and 667 A on the 433 V side.
  - q: Why is distribution secondary voltage 433 V, not 415 V?
    a: The no-load secondary is set slightly higher to allow for voltage drop under load, so customers receive close to 415 V.
  - q: Does power factor affect transformer current?
    a: Not the rating calculation — transformers are rated in kVA, so full-load current depends only on kVA and voltage.
related: [engineering/transformer-short-circuit, engineering/kva-to-kw, engineering/kw-to-amps, engineering/cable-voltage-drop]
''', '''
## How to use this calculator

Enter the **transformer rating** in kVA, choose **three-phase** or **single-phase** and enter the **primary** and **secondary line voltages**. You get the full-load current on each side and the voltage ratio.

## The formulas

| Supply | Full-load current |
|---|---|
| Three-phase | I = kVA × 1,000 ÷ (√3 × V<sub>L</sub>) |
| Single-phase | I = kVA × 1,000 ÷ V |

## Full-load currents (three-phase)

| kVA | 11 kV side | 433 V side | 415 V side |
|---|---|---|---|
''' + ''.join(f"| {s} | {s*1000/(math.sqrt(3)*11000):.1f} A | {s*1000/(math.sqrt(3)*433):.0f} A | {s*1000/(math.sqrt(3)*415):.0f} A |\n" for s in [25, 63, 100, 160, 250, 315, 400, 500, 630, 1000, 1600, 2000, 2500]) + '''
A useful shortcut at 415–433 V three-phase: full-load current ≈ 1.33–1.39 × kVA.

## Selecting protection

- **LV breaker**: rated at or just above the secondary full-load current.
- **HV fuse or breaker**: sized for full-load current while riding through magnetising inrush (often 8–12 × rated current for a few cycles).
- **Cables and busbars**: rated for full-load current with installation derating factors.

## Loading

Distribution transformers are most efficient at about 40–60% load. Continuous overloading shortens insulation life; follow the manufacturer's loading guide (IEC 60076-7).

## Fault current

Short-circuit current depends on the transformer's impedance. See the [transformer short-circuit calculator](/engineering/transformer-short-circuit/).
''')

page('engineering', 'transformer-short-circuit', f'''
title: Transformer Short-Circuit Current Calculator
description: Estimate the maximum fault current on a transformer secondary from kVA, voltage and percentage impedance (infinite-bus method).
category: engineering
keywords: [transformer short circuit current, fault current calculator, transformer impedance, percent impedance, fault level, breaking capacity, short circuit mva]
updated: {D}
variables:
  - {{ id: S, label: Transformer rating, suffix: kVA, default: 1000, min: 0 }}
  - {{ id: V, label: Secondary line voltage, family: voltage, unit: V, default: 415, min: 0 }}
  - {{ id: Z, label: Impedance, family: percent, unit: '%', default: 5, min: 0.001, max: 0.5 }}
  - {{ id: Ifl, label: Full-load current, family: current, unit: A, min: 0 }}
  - {{ id: Isc, label: Short-circuit current (3-phase), family: current, unit: kA, min: 0 }}
  - {{ id: MVA, label: Fault level, suffix: MVA, min: 0, decimals: 2 }}
equations:
  - Ifl = S * 1000 / (sqrt(3) * V)
  - Isc = Ifl / Z
  - MVA = S / Z / 1000
faq:
  - q: How do I calculate transformer fault current?
    a: Isc = full-load current ÷ (percentage impedance ÷ 100). A 1,000 kVA, 415 V, 5% transformer gives about 27.8 kA.
  - q: Why is this the maximum fault current?
    a: The method assumes an infinite source with zero impedance upstream. Real upstream impedance, cables and arc resistance reduce the actual fault current.
  - q: Where do I find the impedance?
    a: On the transformer nameplate, usually 4–6% for distribution transformers and higher for large units.
  - q: Why does fault current matter?
    a: Breakers and switchgear must have a breaking capacity higher than the prospective fault current, and cables must withstand it until protection operates.
related: [engineering/transformer-current, engineering/kva-to-kw, engineering/cable-voltage-drop, engineering/kw-to-amps]
''', '''
## How to use this calculator

Enter the **transformer rating**, **secondary voltage** and **percentage impedance** from the nameplate. You get the full-load current, the maximum symmetrical three-phase short-circuit current and the fault level in MVA.

## The formulas

<p class="formula">I<sub>FL</sub> = kVA × 1,000 ÷ (√3 × V) &nbsp;·&nbsp; I<sub>sc</sub> = I<sub>FL</sub> ÷ (Z% ÷ 100)</p>

<p class="formula">Fault MVA = kVA ÷ (Z% ÷ 100) ÷ 1,000</p>

## Fault current at 415 V

| kVA | Z% | Full-load current | Short-circuit current |
|---|---|---|---|
''' + ''.join(f"| {s} | {z}% | {s*1000/(math.sqrt(3)*415):.0f} A | {s*1000/(math.sqrt(3)*415)/(z/100)/1000:.1f} kA |\n" for s, z in [(100, 4), (250, 4), (500, 4.5), (630, 4.5), (1000, 5), (1600, 6.25), (2000, 6.25), (2500, 6.25)]) + '''
Typical impedances follow IEC 60076-5 guidance for distribution transformers.

## Choosing breaker breaking capacity

Select LV breakers with a rated short-circuit breaking capacity (Icu/Ics) above the prospective fault current at their location — for example, 36 kA or 50 kA breakers for a 1,000 kVA, 5% transformer.

## Reducing fault current

- Choose transformers with higher impedance (at the cost of more voltage regulation).
- Split loads across multiple smaller transformers instead of paralleling.
- Use current-limiting fuses or reactors.

## Beyond this estimate

A full short-circuit study (IEC 60909) includes source impedance, motor contribution, cable impedance and X/R ratios. Use this calculator for quick, conservative checks.
''')

def gascorr(qa, pg, tc, tn=0): return qa*((pg+1.01325)/1.01325)*((tn+273.15)/(tc+273.15))
page('engineering', 'gas-flow-correction', f'''
title: Gas Flow Correction Calculator (Actual to Normal m³/h)
description: Convert actual gas flow (Am³/h) to normal or standard flow (Nm³/h, Sm³/h) using line pressure and temperature — for flow meters and compressors.
category: engineering
keywords: [actual to normal flow, nm3/h to am3/h, gas flow correction, standard cubic meters, pressure temperature compensation, scfm to acfm, gas volume correction]
updated: {D}
variables:
  - {{ id: Qa, label: Actual flow (at line conditions), family: flow, unit: m3h, imperialUnit: cfm, default: 100, min: 0 }}
  - {{ id: Pg, label: Line pressure (gauge), family: pressure, unit: bar, imperialUnit: psi, default: 5, min: -1 }}
  - {{ id: T, label: Line temperature, family: temperature, unit: C, imperialUnit: F, default: 30 }}
  - id: Tn
    label: Reference conditions
    default: 273.15
    options:
      - {{ label: 'Normal: 0 °C, 1.01325 bar(a)', value: 273.15 }}
      - {{ label: 'Standard: 15 °C, 1.01325 bar(a)', value: 288.15 }}
      - {{ label: 'Standard: 20 °C, 1.01325 bar(a)', value: 293.15 }}
  - {{ id: Qn, label: Flow at reference conditions, family: flow, unit: m3h, imperialUnit: cfm, min: 0 }}
  - {{ id: k, label: Correction factor, min: 0, decimals: 4 }}
equations:
  - k = ((Pg + 101325) / 101325) * (Tn / T)
  - Qn = Qa * k
faq:
  - q: What is the difference between Am³/h and Nm³/h?
    a: Am³/h is the volume flow at actual line pressure and temperature. Nm³/h converts it to normal reference conditions (0 °C and 1.01325 bar absolute) so flows at different conditions can be compared.
  - q: How do I convert actual flow to normal flow?
    a: Qn = Qa × (P_actual ÷ P_ref) × (T_ref ÷ T_actual), using absolute pressures and temperatures in kelvin.
  - q: Why does compressed gas show a higher normal flow?
    a: At 5 bar(g), gas is compressed about six times, so each actual cubic metre contains about six normal cubic metres.
  - q: Does this include compressibility?
    a: No. It assumes ideal gas behaviour. At high pressures, divide by the compressibility factor Z for accuracy.
related: [physics/ideal-gas-law, chemistry/combined-gas-law, engineering/mass-flow-rate, conversion/flow-rate-converter]
''', f'''
## How to use this calculator

Enter the **actual flow** at line conditions, the **gauge pressure** and the **temperature** in the pipe, and choose the **reference conditions**. You get the flow at reference conditions and the correction factor. To go from Nm³/h to actual flow, press × on Actual flow.

## The formula

<p class="formula">Q<sub>N</sub> = Q<sub>A</sub> × (P<sub>A</sub> ÷ P<sub>N</sub>) × (T<sub>N</sub> ÷ T<sub>A</sub>)</p>

Pressures must be **absolute** (gauge + atmospheric) and temperatures in **kelvin**.

## Correction factors (to 0 °C, 1.01325 bar a)

| Gauge pressure | 0 °C | 20 °C | 40 °C |
|---|---|---|---|
''' + ''.join(f"| {p} bar(g) | {gascorr(1,p,0):.3f} | {gascorr(1,p,20):.3f} | {gascorr(1,p,40):.3f} |\n" for p in [0, 0.5, 1, 2, 4, 6, 7, 10, 16]) + '''
Multiply actual flow by the factor to get Nm³/h.

## Which reference?

| Term | Typical reference |
|---|---|
| Nm³ (normal) | 0 °C, 1.01325 bar(a) — common in Europe and Asia |
| Sm³ (standard, ISO 13443) | 15 °C, 1.01325 bar(a) — natural gas |
| SCF (US) | 60 °F (15.6 °C), 14.696 psia |
| Compressed air (ISO 1217 FAD) | Inlet conditions, often 20 °C, 1 bar(a) |

Always state the reference conditions with a standard flow figure.

## Flow meter compensation

Volumetric gas meters (vortex, turbine, ultrasonic) measure actual flow. Flow computers or multivariable transmitters add pressure and temperature inputs to report normal flow or mass flow in real time.
''')

def pul(n1, d1, d2): return n1*d1/d2
page('engineering', 'pulley-speed', f'''
title: Pulley Speed and Belt Length Calculator
description: Calculate driven pulley rpm, speed ratio, belt speed and belt length for two-pulley belt drives — or the pulley size for a target speed.
category: engineering
keywords: [pulley speed calculator, pulley rpm calculator, belt length calculator, pulley ratio, v belt calculator, belt speed, driven pulley diameter]
updated: {D}
variables:
  - {{ id: N1, label: Driver speed, suffix: rpm, default: 1440, min: 0 }}
  - {{ id: D1, label: Driver pulley diameter, family: length, unit: mm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: D2, label: Driven pulley diameter, family: length, unit: mm, imperialUnit: in, default: 250, min: 0 }}
  - {{ id: C, label: Centre distance, family: length, unit: mm, imperialUnit: in, default: 500, min: 0 }}
  - {{ id: N2, label: Driven speed, suffix: rpm, min: 0, decimals: 0 }}
  - {{ id: i, label: Speed ratio (D2 ÷ D1), min: 0, decimals: 3 }}
  - {{ id: v, label: Belt speed, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: Lb, label: Belt length (pitch), family: length, unit: mm, imperialUnit: in, min: 0 }}
equations:
  - N2 = N1 * D1 / D2
  - i = D2 / D1
  - v = pi * D1 * N1 / 60
  - Lb = 2*C + pi * (D1 + D2) / 2 + (D2 - D1)^2 / (4*C)
faq:
  - q: How do I calculate pulley rpm?
    a: Driven rpm = driver rpm × driver diameter ÷ driven diameter. A 1,440 rpm motor with a 100 mm pulley driving a 250 mm pulley gives 576 rpm.
  - q: What size pulley do I need for a target speed?
    a: Enter the target as Driven speed and press × on Driven pulley diameter.
  - q: What is a good belt speed for V-belts?
    a: Classical V-belts work best at about 5–25 m/s, with around 20 m/s often most efficient. Very low speeds need high tension; very high speeds cause centrifugal losses.
  - q: Does torque change with pulley size?
    a: Yes. Torque increases by the same ratio that speed decreases (ignoring losses). A 2.5:1 reduction gives about 2.5 times the torque.
related: [engineering/torque-power-speed, sports/cycling-gear-speed, physics/torque, engineering/three-phase-motor-power]
''', f'''
## How to use this calculator

Enter the **driver speed**, **driver pulley diameter**, **driven pulley diameter** and **centre distance** between shafts. You get the driven speed, speed ratio, belt speed and approximate belt length.

## The formulas

| Quantity | Formula |
|---|---|
| Driven speed | N₂ = N₁ × D₁ ÷ D₂ |
| Belt speed | v = π × D₁ × N₁ ÷ 60 |
| Belt length | L ≈ 2C + π(D₁ + D₂)/2 + (D₂ − D₁)²/(4C) |

Use pitch diameters for V-belts.

## Example

1,440 rpm motor, 100 mm → 250 mm, 500 mm centres:

- Driven speed = **{pul(1440,100,250):.0f} rpm**
- Belt speed = π × 0.1 × 1,440 ÷ 60 = **{pi*0.1*1440/60:.2f} m/s**
- Belt length ≈ **{2*500+pi*350/2+150**2/2000:.0f} mm**

## Driven speeds from a 1,440 rpm motor

| Driver / driven (mm) | Ratio | Driven speed |
|---|---|---|
''' + ''.join(f"| {a} / {b} | {b/a:.2f} | {pul(1440,a,b):.0f} rpm |\n" for a, b in [(100, 100), (100, 150), (100, 200), (100, 250), (80, 300), (150, 100), (200, 100)]) + '''
## Belt drive tips

- Keep the speed ratio below about 6:1 for single V-belt stages to maintain wrap angle on the small pulley.
- Do not go below the minimum recommended pulley diameter for the belt section — small pulleys shorten belt life.
- Check alignment and tension; misalignment is a leading cause of belt failure.
- Real speed is 1–3% lower than calculated because of belt slip and creep.

## Choosing a standard belt

Round the calculated length to the nearest standard belt size, then adjust the centre distance with the motor slide rails to set tension.
''')

# ============================ CHEMISTRY ============================
page('chemistry', 'freezing-point-depression', f'''
title: Freezing Point Depression Calculator
description: Calculate how much a solute lowers the freezing point of a solvent with ΔTf = i·Kf·m — for water, benzene, cyclohexane and more.
category: chemistry
keywords: [freezing point depression calculator, delta tf, kf constant, colligative properties, van t hoff factor, molality freezing point, antifreeze]
updated: {D}
variables:
  - id: Kf
    label: Solvent
    default: 1.86
    options:
      - {{ label: 'Water (Kf 1.86, mp 0 °C)', value: 1.86 }}
      - {{ label: 'Benzene (Kf 5.12, mp 5.5 °C)', value: 5.12 }}
      - {{ label: 'Acetic acid (Kf 3.90, mp 16.6 °C)', value: 3.9 }}
      - {{ label: 'Cyclohexane (Kf 20.0, mp 6.5 °C)', value: 20.0 }}
      - {{ label: 'Camphor (Kf 37.7, mp 179 °C)', value: 37.7 }}
  - {{ id: i, label: Van 't Hoff factor (i), default: 2, min: 0, help: '1 for sugars, about 2 for NaCl, about 3 for CaCl₂.' }}
  - {{ id: m, label: Molality, suffix: mol/kg, default: 0.5, min: 0 }}
  - {{ id: Tf0, label: Normal freezing point of solvent, suffix: °C, default: 0 }}
  - {{ id: dT, label: Freezing point depression (ΔTf), suffix: °C, min: 0, decimals: 3 }}
  - {{ id: Tf, label: New freezing point, suffix: °C, decimals: 2 }}
equations:
  - dT = i * Kf * m
  - Tf = Tf0 - dT
faq:
  - q: What is freezing point depression?
    a: Dissolving a solute lowers the temperature at which a solvent freezes. The drop depends on the number of solute particles, not their identity.
  - q: Why does salt melt ice on roads?
    a: Salt dissolves in the thin layer of water on ice, lowering its freezing point so the ice melts at temperatures below 0 °C — down to about −10 °C in practice for rock salt.
  - q: How can I find the molar mass of an unknown solute?
    a: Measure ΔTf, calculate molality m = ΔTf ÷ (i·Kf), then molar mass = grams of solute ÷ (m × kg of solvent).
  - q: Does the formula work for concentrated solutions?
    a: It is accurate for dilute solutions. At high concentrations, ions interact and the effective i falls, so measured depressions are smaller.
related: [chemistry/boiling-point-elevation, chemistry/molality, chemistry/osmotic-pressure, chemistry/molarity]
''', '''
## How to use this calculator

Choose the **solvent** (which sets Kf), enter the **van 't Hoff factor** and the **molality** of the solution, and the solvent's normal freezing point. You get the freezing point depression and the new freezing point.

## The formula

<p class="formula">ΔT<sub>f</sub> = i × K<sub>f</sub> × m</p>

- **i** = particles per formula unit (van 't Hoff factor)
- **K<sub>f</sub>** = cryoscopic constant of the solvent (°C·kg/mol)
- **m** = molality (mol solute per kg solvent)

## Salt water freezing points (ideal estimate)

| NaCl (g per kg water) | Molality | Freezing point |
|---|---|---|
''' + ''.join(f"| {g} | {g/58.44:.3f} | {-2*1.86*g/58.44:.2f} °C |\n" for g in [10, 20, 35, 50, 100]) + '''
Seawater (about 35 g/kg of salts) actually freezes at about −1.9 °C; the ideal formula slightly overestimates the effect at higher concentrations.

## Van 't Hoff factors

| Solute | Ideal i | Typical measured i (dilute) |
|---|---|---|
| Glucose, sucrose, urea | 1 | 1.0 |
| NaCl, KCl | 2 | 1.8–1.9 |
| CaCl₂, MgCl₂ | 3 | 2.5–2.7 |
| AlCl₃ | 4 | about 3.2 |

## Uses

- **Road de-icing** with NaCl or CaCl₂ (calcium chloride works to lower temperatures).
- **Antifreeze**: ethylene glycol in car radiators.
- **Ice cream making**: salt and ice reach about −10 to −20 °C to freeze the mix.
- **Molar mass determination** in the lab (cryoscopy).
''')

page('chemistry', 'boiling-point-elevation', f'''
title: Boiling Point Elevation Calculator
description: Calculate how much a dissolved solute raises the boiling point of a solvent using ΔTb = i·Kb·m — for water, ethanol, benzene and more.
category: chemistry
keywords: [boiling point elevation calculator, delta tb, kb constant, ebullioscopic constant, colligative properties, salt in water boiling point]
updated: {D}
variables:
  - id: Kb
    label: Solvent
    default: 0.512
    options:
      - {{ label: 'Water (Kb 0.512, bp 100 °C)', value: 0.512 }}
      - {{ label: 'Ethanol (Kb 1.22, bp 78.4 °C)', value: 1.22 }}
      - {{ label: 'Benzene (Kb 2.53, bp 80.1 °C)', value: 2.53 }}
      - {{ label: 'Chloroform (Kb 3.63, bp 61.2 °C)', value: 3.63 }}
      - {{ label: 'Acetic acid (Kb 3.07, bp 118 °C)', value: 3.07 }}
  - {{ id: i, label: Van 't Hoff factor (i), default: 2, min: 0 }}
  - {{ id: m, label: Molality, suffix: mol/kg, default: 1, min: 0 }}
  - {{ id: Tb0, label: Normal boiling point of solvent, suffix: °C, default: 100 }}
  - {{ id: dT, label: Boiling point elevation (ΔTb), suffix: °C, min: 0, decimals: 3 }}
  - {{ id: Tb, label: New boiling point, suffix: °C, decimals: 2 }}
equations:
  - dT = i * Kb * m
  - Tb = Tb0 + dT
faq:
  - q: Does adding salt to pasta water make it boil hotter?
    a: Only slightly. A tablespoon of salt (about 18 g) in 4 litres of water raises the boiling point by less than 0.1 °C. Salt is for flavour.
  - q: What is the ebullioscopic constant?
    a: Kb, the boiling point rise for a 1 mol/kg solution of a non-dissociating solute. For water it is 0.512 °C·kg/mol.
  - q: Why is boiling point elevation smaller than freezing point depression?
    a: Because Kb for most solvents is smaller than Kf. For water, Kf is 1.86 but Kb is only 0.512.
  - q: Does altitude affect boiling point?
    a: Yes, much more than solutes do. Water boils at about 95 °C at 1,500 m and about 90 °C at 3,000 m because air pressure is lower.
related: [chemistry/freezing-point-depression, chemistry/molality, chemistry/osmotic-pressure, chemistry/specific-heat]
''', '''
## How to use this calculator

Choose the **solvent**, enter the **van 't Hoff factor**, the **molality** and the solvent's normal boiling point. The calculator gives the rise in boiling point and the new boiling point.

## The formula

<p class="formula">ΔT<sub>b</sub> = i × K<sub>b</sub> × m</p>

## Salt in water

| Salt (g per kg water) | Boiling point rise (ideal) |
|---|---|
''' + ''.join(f"| {g} g | {2*0.512*g/58.44:.3f} °C |\n" for g in [5, 10, 30, 58.44, 100, 200]) + '''
Even very salty water boils only a degree or two above 100 °C.

## Boiling point and altitude

| Altitude | Approximate boiling point of water |
|---|---|
| Sea level | 100 °C |
| 1,000 m | 96.7 °C |
| 2,000 m | 93.4 °C |
| 3,000 m | 90.0 °C |
| 5,000 m | 83.3 °C |

Pressure cookers raise the pressure so water boils at about 120 °C, speeding up cooking.

## Molar mass from boiling point

Ebullioscopy works like cryoscopy: m = ΔTb ÷ (i × Kb), then molar mass = mass of solute ÷ (m × kg of solvent). Freezing point depression is usually preferred because the effect is larger.

## Colligative properties

Freezing point depression, boiling point elevation, vapour pressure lowering and [osmotic pressure](/chemistry/osmotic-pressure/) all depend on the number of dissolved particles, not their identity.
''')

page('chemistry', 'daltons-law', f'''
title: Dalton's Law Calculator (Partial Pressure)
description: Calculate the partial pressure of a gas in a mixture from mole fraction and total pressure — for air, diving gases and gas mixtures.
category: chemistry
keywords: [daltons law calculator, partial pressure calculator, mole fraction, total pressure, oxygen partial pressure, gas mixture, ppo2]
updated: {D}
variables:
  - {{ id: nA, label: Moles (or %) of gas A, default: 21, min: 0 }}
  - {{ id: nT, label: Total moles (or 100%), default: 100, min: 0.0001 }}
  - {{ id: P, label: Total pressure, family: pressure, unit: atm, imperialUnit: psi, default: 1, min: 0 }}
  - {{ id: x, label: Mole fraction of A, min: 0, max: 1, decimals: 4 }}
  - {{ id: pA, label: Partial pressure of A, family: pressure, unit: atm, imperialUnit: psi, min: 0 }}
equations:
  - x = nA / nT
  - pA = x * P
faq:
  - q: What is Dalton's law of partial pressures?
    a: The total pressure of a gas mixture equals the sum of the partial pressures of each gas. Each partial pressure = mole fraction × total pressure.
  - q: What is the partial pressure of oxygen in air?
    a: About 0.21 atm (21 kPa) at sea level, since oxygen is about 21% of dry air.
  - q: Why does partial pressure matter in diving?
    a: Breathing oxygen at a partial pressure above about 1.4–1.6 atm risks oxygen toxicity. At 30 m depth (4 atm), air has an oxygen partial pressure of 0.84 atm.
  - q: Can I use percentages instead of moles?
    a: Yes. For gases, volume percent equals mole percent, so enter the percentage and 100 as the total.
related: [physics/ideal-gas-law, chemistry/combined-gas-law, chemistry/grahams-law, chemistry/boyles-law]
''', '''
## How to use this calculator

Enter the **moles** (or volume percent) of the gas you are interested in, the **total moles** (or 100) and the **total pressure**. You get the mole fraction and the partial pressure.

## The formulas

<p class="formula">x<sub>A</sub> = n<sub>A</sub> ÷ n<sub>total</sub> &nbsp;·&nbsp; p<sub>A</sub> = x<sub>A</sub> × P<sub>total</sub></p>

<p class="formula">P<sub>total</sub> = p₁ + p₂ + p₃ + …</p>

## Composition of dry air (sea level)

| Gas | Volume % | Partial pressure |
|---|---|---|
| Nitrogen | 78.08 | 0.781 atm (79.1 kPa) |
| Oxygen | 20.95 | 0.210 atm (21.2 kPa) |
| Argon | 0.93 | 0.0093 atm |
| Carbon dioxide | about 0.042 | 0.00042 atm |

## Oxygen partial pressure with depth (air)

| Depth in seawater | Absolute pressure | pO₂ |
|---|---|---|
''' + ''.join(f"| {d} m | {1+d/10:.1f} atm | {0.21*(1+d/10):.2f} atm |\n" for d in [0, 10, 20, 30, 40, 56, 66]) + '''
Recreational dive limits on air keep pO₂ below 1.4 atm, which is around 56 m — well beyond typical recreational depth limits for other reasons such as narcosis.

## Altitude

At 5,000 m, total air pressure is about 0.53 atm, so oxygen partial pressure drops to about 0.11 atm — roughly half its sea-level value, which is why altitude sickness occurs.

## Collecting gas over water

When gas is collected over water, subtract the water vapour pressure: p<sub>gas</sub> = P<sub>atm</sub> − p<sub>H₂O</sub>. At 25 °C, water vapour pressure is about 3.17 kPa.
''')

def gr(m1, m2): return math.sqrt(m2/m1)
page('chemistry', 'grahams-law', f'''
title: Graham's Law Calculator (Effusion Rate)
description: Compare effusion or diffusion rates of two gases from their molar masses using Graham's law — or find an unknown molar mass.
category: chemistry
keywords: [grahams law calculator, rate of effusion, diffusion rate, molar mass from effusion, grahams law of effusion, gas diffusion]
updated: {D}
variables:
  - {{ id: M1, label: Molar mass of gas 1, suffix: g/mol, default: 2.016, min: 0.0001 }}
  - {{ id: M2, label: Molar mass of gas 2, suffix: g/mol, default: 32.00, min: 0.0001 }}
  - {{ id: r, label: Rate ratio (gas 1 ÷ gas 2), min: 0, decimals: 4 }}
  - {{ id: tr, label: Time ratio (gas 1 ÷ gas 2), min: 0, decimals: 4 }}
equations:
  - r = sqrt(M2 / M1)
  - tr = 1 / r
faq:
  - q: What is Graham's law?
    a: The rate of effusion of a gas is inversely proportional to the square root of its molar mass — lighter gases escape faster.
  - q: How much faster does hydrogen effuse than oxygen?
    a: About 3.98 times faster, since √(32 ÷ 2.016) ≈ 3.98.
  - q: How do I find an unknown molar mass?
    a: Measure the rate ratio against a known gas, enter it with the known molar mass, and press × on the unknown molar mass.
  - q: Why do helium balloons deflate faster than air balloons?
    a: Helium atoms are light (4 g/mol) and escape through the balloon material much faster than nitrogen and oxygen.
related: [chemistry/daltons-law, physics/ideal-gas-law, chemistry/moles, chemistry/combined-gas-law]
''', '''
## How to use this calculator

Enter the **molar masses** of two gases. The calculator gives how many times faster gas 1 effuses than gas 2, and the ratio of times taken for the same amount to escape.

## The formula

<p class="formula">Rate₁ ÷ Rate₂ = √(M₂ ÷ M₁)</p>

## Effusion relative to air (29 g/mol)

| Gas | Molar mass | Speed relative to air |
|---|---|---|
''' + ''.join(f"| {n} | {m} | {gr(m,28.97):.2f}× |\n" for n, m in [('Hydrogen (H₂)', 2.016), ('Helium (He)', 4.003), ('Methane (CH₄)', 16.04), ('Ammonia (NH₃)', 17.03), ('Nitrogen (N₂)', 28.01), ('Oxygen (O₂)', 32.00), ('Carbon dioxide (CO₂)', 44.01), ('Sulphur hexafluoride (SF₆)', 146.06)]) + '''
## Effusion vs diffusion

- **Effusion**: gas escaping through a tiny hole into a vacuum — Graham's law applies closely.
- **Diffusion**: gas spreading through another gas — Graham's law gives the right trend but collisions make it approximate.

## The classic demonstration

Cotton wool soaked in ammonia (17 g/mol) and hydrochloric acid (HCl, 36.5 g/mol) at opposite ends of a glass tube produce a white ring of ammonium chloride closer to the HCl end, because ammonia diffuses about 1.47 times faster.

## Uranium enrichment

Gaseous diffusion plants separated uranium-235 from uranium-238 as UF₆. The masses differ so little (349 vs 352 g/mol) that each stage enriched by only a factor of about 1.004, requiring thousands of stages.
''')

def nernst(e0, n, T, Q): return e0 - 8.314462618*T/(n*96485.33212)*math.log(Q)
page('chemistry', 'nernst-equation', f'''
title: Nernst Equation Calculator
description: Calculate the cell potential under non-standard conditions with the Nernst equation, from E°, electrons transferred, temperature and reaction quotient.
category: chemistry
keywords: [nernst equation calculator, cell potential, electrode potential, reaction quotient, electrochemistry, nernst potential, emf calculator]
updated: {D}
variables:
  - {{ id: E0, label: Standard potential (E°), suffix: V, default: 1.10 }}
  - {{ id: n, label: Electrons transferred (n), default: 2, min: 1 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, default: 25, min: 0 }}
  - {{ id: Q, label: Reaction quotient (Q), default: 0.01, min: 1e-30 }}
  - {{ id: E, label: Cell potential (E), suffix: V, decimals: 4 }}
equations:
  - E = E0 - 8.314462618 * T / (n * 96485.33212) * ln(Q)
faq:
  - q: What is the Nernst equation?
    a: E = E° − (RT ÷ nF) ln Q. It gives the electrode or cell potential when concentrations are not 1 M.
  - q: What is the simplified form at 25 °C?
    a: E = E° − (0.05916 ÷ n) log₁₀ Q.
  - q: What happens at equilibrium?
    a: The cell potential falls to zero and Q equals the equilibrium constant K. Then E° = (RT ÷ nF) ln K.
  - q: How is the Nernst equation used in pH meters?
    a: A glass electrode’s potential changes by about 59 mV per pH unit at 25 °C, as the Nernst equation predicts for hydrogen ions.
related: [chemistry/ph, chemistry/gibbs-free-energy, chemistry/henderson-hasselbalch, chemistry/molarity]
''', f'''
## How to use this calculator

Enter the **standard potential** E°, the number of **electrons transferred**, the **temperature** and the **reaction quotient** Q (products over reactants, each raised to its coefficient). The calculator gives the cell potential.

## The Nernst equation

<p class="formula">E = E° − (RT ÷ nF) × ln Q</p>

with R = 8.314 J/(mol·K) and F = 96,485 C/mol. At 25 °C this becomes E = E° − (0.05916 ÷ n) log₁₀ Q.

## Example: Daniell cell (Zn/Cu, E° = 1.10 V)

Zn | Zn²⁺ (0.01 M) ∥ Cu²⁺ (1 M) | Cu, so Q = [Zn²⁺] ÷ [Cu²⁺] = 0.01:

E = 1.10 − (0.05916 ÷ 2) × log₁₀(0.01) = **{nernst(1.10,2,298.15,0.01):.3f} V**

## How Q changes the potential (n = 2, 25 °C)

| Q | E − E° |
|---|---|
''' + ''.join(f"| {q:g} | {-(8.314462618*298.15/(2*96485.33212))*math.log(q)*1000:+.1f} mV |\n" for q in [1e-4, 1e-2, 0.1, 1, 10, 100, 1e4]) + '''
Each tenfold change in Q shifts E by 59.16 ÷ n mV at 25 °C.

## pH electrodes

For the hydrogen electrode, n = 1 and the Nernst slope is 59.16 mV per pH unit at 25 °C, rising with temperature (about 61.5 mV at 37 °C). pH meters use temperature compensation for this reason.

## Membrane potentials

In biology, the Nernst equation gives the equilibrium potential for an ion across a cell membrane. For potassium (about 140 mM inside, 5 mM outside) at 37 °C, it is about −89 mV.
''')
print('batchC done')
