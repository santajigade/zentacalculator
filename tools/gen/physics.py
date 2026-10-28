import math
from page import page
C='physics'; U='updated: 2026-10-27'; g=9.80665

page(C,'speed-distance-time',f'''
title: Speed, Distance & Time Calculator
description: Calculate speed, distance or travel time — enter any two and get the third, in km/h, mph, m/s, km or miles.
category: physics
keywords: [speed distance time, speed calculator, travel time, average speed, distance calculator, how long will it take]
{U}
featured: true
variables:
  - {{ id: d, label: Distance, family: length, unit: km, imperialUnit: mi, default: 150, min: 0 }}
  - {{ id: v, label: Speed, family: velocity, unit: kmh, imperialUnit: mph, default: 60, min: 0 }}
  - {{ id: t, label: Time, family: seconds, unit: h, min: 0 }}
equations:
  - d = v * t
chart: {{ x: v, y: t, from: 10, to: 150 }}
faq:
  - q: What is the formula for speed?
    a: Speed = distance ÷ time. Distance = speed × time, and time = distance ÷ speed.
  - q: How long does 150 km take at 60 km/h?
    a: 150 ÷ 60 = 2.5 hours, which is 2 hours 30 minutes.
  - q: What is average speed?
    a: Total distance divided by total time, including stops. It is usually lower than your cruising speed.
related: [physics/acceleration, conversion/speed-converter, conversion/km-to-miles]
''','''
## How to use this calculator

Enter any **two** of distance, speed and time — the third is calculated. Each field has its own unit, so you can mix kilometres with mph or minutes with hours.

## The formula

<p class="formula">distance = speed × time   speed = distance ÷ time   time = distance ÷ speed</p>

## Worked examples

- **Travel time:** 150 km at 60 km/h → 150 ÷ 60 = **2.5 h** (2 h 30 min).
- **Average speed:** 42.195 km marathon in 3 h 30 min → 42.195 ÷ 3.5 = **12.06 km/h**.
- **Distance:** walking at 5 km/h for 45 minutes → 5 × 0.75 = **3.75 km**.

## Converting decimal hours

0.5 h = 30 min · 0.25 h = 15 min · 0.1 h = 6 min. Switch the Time unit to minutes to avoid conversions.

## Keep units consistent

The most common mistake is mixing units by hand, such as metres with km/h. The calculator converts every field automatically — just pick the unit you have.
''')

page(C,'acceleration',f'''
title: Acceleration Calculator
description: Calculate acceleration from change in speed and time — or the final speed or time needed — in m/s², g and more.
category: physics
keywords: [acceleration calculator, a = (v-u)/t, 0-100 km/h, change in velocity, m/s2, g force]
{U}
variables:
  - {{ id: u, label: Initial speed, family: velocity, unit: kmh, imperialUnit: mph, default: 0 }}
  - {{ id: v, label: Final speed, family: velocity, unit: kmh, imperialUnit: mph, default: 100 }}
  - {{ id: t, label: Time, family: seconds, unit: s, default: 8, min: 0 }}
  - {{ id: a, label: Acceleration, suffix: m/s² }}
  - {{ id: gs, label: Acceleration in g, decimals: 3 }}
equations:
  - a = (v - u) / t
  - gs = a / g0
faq:
  - q: What is the formula for acceleration?
    a: Acceleration = (final speed − initial speed) ÷ time. Its SI unit is metres per second squared (m/s²).
  - q: What is 1 g?
    a: The acceleration due to gravity at Earth's surface, 9.80665 m/s².
  - q: What does negative acceleration mean?
    a: Slowing down (deceleration) — the final speed is lower than the initial speed.
related: [physics/suvat-equations, physics/force, physics/speed-distance-time]
''',f'''
## How to use this calculator

Enter the **initial speed**, **final speed** and **time** to get the acceleration in m/s² and in g. Or enter the acceleration to find the time or speed.

## The formula

<p class="formula">a = (v − u) ÷ t</p>

## Worked example

A car goes from 0 to 100 km/h in 8 seconds:

- Change in speed = 100 km/h = 27.78 m/s
- a = 27.78 ÷ 8 = **{27.7778/8:.2f} m/s²** = **{27.7778/8/g:.3f} g**

## Typical accelerations

| Situation | Acceleration |
|---|---|
| Family car, 0–100 km/h in 12 s | 2.3 m/s² |
| Sports car, 0–100 km/h in 3.5 s | 7.9 m/s² |
| Free fall | 9.81 m/s² (1 g) |
| Emergency braking (dry road) | about −8 m/s² |

## Related equations

For distance covered while accelerating, use the [SUVAT calculator](/physics/suvat-equations/).
''')

u,a,t=5,2,10; v=u+a*t; s=u*t+a*t*t/2
page(C,'suvat-equations',f'''
title: SUVAT Equations Calculator (Kinematics)
description: Solve constant-acceleration motion problems — initial velocity, final velocity, acceleration, time and displacement.
category: physics
keywords: [suvat, kinematics calculator, equations of motion, displacement, constant acceleration, v = u + at]
{U}
variables:
  - {{ id: u, label: Initial velocity (u), family: velocity, unit: ms, imperialUnit: fts, default: 5 }}
  - {{ id: v, label: Final velocity (v), family: velocity, unit: ms, imperialUnit: fts }}
  - {{ id: a, label: Acceleration (a), suffix: m/s², default: 2 }}
  - {{ id: t, label: Time (t), family: seconds, unit: s, default: 10, min: 0 }}
  - {{ id: s, label: Displacement (s), family: length, unit: m, imperialUnit: ft }}
equations:
  - v = u + a * t
  - s = (u + v) / 2 * t
chart: {{ x: t, y: s, from: 0, to: 20 }}
faq:
  - q: What are the SUVAT equations?
    a: Five equations linking displacement (s), initial velocity (u), final velocity (v), acceleration (a) and time (t) for constant acceleration.
  - q: How many values do I need?
    a: Any three. The other two can then be calculated.
  - q: When do they not apply?
    a: When acceleration changes, for example with air resistance at high speed. Then calculus or numerical methods are needed.
related: [physics/acceleration, physics/free-fall, physics/projectile-motion]
''',f'''
## How to use this calculator

Enter **any three** of u, v, a, t and s. The other two are solved automatically — press × on a field to choose which values are calculated.

## The equations

<p class="formula">v = u + at<br/>s = ½(u + v)t<br/>s = ut + ½at²<br/>v² = u² + 2as<br/>s = vt − ½at²</p>

## Worked example

u = 5 m/s, a = 2 m/s², t = 10 s:

- v = 5 + 2 × 10 = **{v} m/s**
- s = 5 × 10 + ½ × 2 × 10² = **{s:g} m**

## Braking distance example

A car at 20 m/s (72 km/h) brakes at −8 m/s². Set u = 20, v = 0, a = −8: it stops in **2.5 s** over **25 m**. Doubling the speed to 40 m/s quadruples the distance to 100 m.

## Sign convention

Pick one direction as positive. Velocities and accelerations in the opposite direction are negative — for example, a = −9.81 m/s² for an object thrown upwards.
''')

page(C,'force',f'''
title: Force Calculator (F = ma)
description: Calculate force, mass or acceleration using Newton's second law, F = m × a, in newtons, kN or lbf.
category: physics
keywords: [force calculator, f = ma, newton's second law, newtons, mass acceleration, lbf]
{U}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 1200, min: 0 }}
  - {{ id: a, label: Acceleration, suffix: m/s², default: 3 }}
  - {{ id: F, label: Force, family: force, unit: N, imperialUnit: lbf }}
equations:
  - F = m * a
chart: {{ x: a, y: F, from: 0, to: 10 }}
faq:
  - q: What is Newton's second law?
    a: The net force on an object equals its mass times its acceleration — F = ma.
  - q: What is a newton?
    a: The force needed to accelerate 1 kg at 1 m/s². It is roughly the weight of a small apple.
  - q: Is force the same as weight?
    a: Weight is a specific force — the pull of gravity, m × g. Use the weight calculator for that.
related: [physics/weight, physics/acceleration, physics/momentum]
''',f'''
## How to use this calculator

Enter any **two** of mass, acceleration and force. The third is calculated, in newtons, kN, kgf or lbf.

## The formula

<p class="formula">F = m × a</p>

## Worked example

A 1,200 kg car accelerating at 3 m/s² needs a net force of 1,200 × 3 = **3,600 N** (3.6 kN, about {3600/4.4482216:.0f} lbf).

## Net force

F is the **net** force — the total after friction, drag and other forces are taken into account. A car's engine must provide more than 3,600 N to overcome rolling resistance and air drag as well.

## Units of force

| Unit | In newtons |
|---|---|
| 1 kN | 1,000 N |
| 1 kgf | 9.81 N |
| 1 lbf | 4.448 N |
| 1 dyne | 0.00001 N |
''')

page(C,'weight',f'''
title: Weight Calculator (Mass to Weight on Planets)
description: Convert mass to weight (force) on Earth, the Moon, Mars and other planets using W = m × g.
category: physics
keywords: [weight calculator, mass vs weight, weight on moon, weight on mars, w = mg, gravity]
{U}
variables:
  - id: gg
    label: Location
    default: 9.80665
    options:
      - {{ label: Earth (9.81 m/s²), value: 9.80665 }}
      - {{ label: Moon (1.62 m/s²), value: 1.62 }}
      - {{ label: Mars (3.71 m/s²), value: 3.71 }}
      - {{ label: Venus (8.87 m/s²), value: 8.87 }}
      - {{ label: Jupiter (24.79 m/s²), value: 24.79 }}
      - {{ label: Saturn (10.44 m/s²), value: 10.44 }}
      - {{ label: Mercury (3.7 m/s²), value: 3.7 }}
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 70, min: 0 }}
  - {{ id: W, label: Weight (force), family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: eq, label: Equivalent Earth scale reading, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - W = m * gg
  - eq = W / g0
faq:
  - q: What is the difference between mass and weight?
    a: Mass is the amount of matter (kg) and is the same everywhere. Weight is the force of gravity on that mass (newtons), and changes from planet to planet.
  - q: How much would I weigh on the Moon?
    a: About one-sixth of your Earth weight. A 70 kg person would read about 11.6 kg on an Earth-calibrated scale.
  - q: Why do scales show kilograms?
    a: Bathroom scales measure force but are calibrated for Earth's gravity, so they display mass directly.
related: [physics/force, physics/free-fall]
''',f'''
## How to use this calculator

Choose a **location**, then enter a **mass**. You get the weight in newtons (or lbf) and what an Earth-calibrated bathroom scale would show there.

## The formula

<p class="formula">W = m × g</p>

## Worked example (70 kg person)

| Location | Weight (N) | Scale reading |
|---|---|---|
| Earth | {70*g:.0f} | 70 kg |
| Moon | {70*1.62:.0f} | {70*1.62/g:.1f} kg |
| Mars | {70*3.71:.0f} | {70*3.71/g:.1f} kg |
| Jupiter | {70*24.79:.0f} | {70*24.79/g:.1f} kg |

## Gravity on Earth varies slightly

Standard gravity is 9.80665 m/s², but the real value ranges from about 9.78 at the equator to 9.83 at the poles — a difference of about 0.5% in your weight.
''')

m,v=1200,100/3.6
page(C,'kinetic-energy',f'''
title: Kinetic Energy Calculator
description: Calculate kinetic energy from mass and speed (KE = ½mv²) — or the speed or mass from a known energy.
category: physics
keywords: [kinetic energy, ke = 1/2 mv2, energy of motion, joules, kinetic energy formula]
{U}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 1200, min: 0 }}
  - {{ id: v, label: Speed, family: velocity, unit: kmh, imperialUnit: mph, default: 100, min: 0 }}
  - {{ id: KE, label: Kinetic energy, family: energy, unit: kJ, min: 0 }}
equations:
  - KE = 0.5 * m * v^2
chart: {{ x: v, y: KE, from: 0, to: 150 }}
faq:
  - q: What is the kinetic energy formula?
    a: KE = ½ × m × v², with mass in kg and speed in m/s giving energy in joules.
  - q: Why does speed matter so much?
    a: Energy depends on the square of speed. Doubling speed means four times the energy — and roughly four times the braking distance.
  - q: Where does kinetic energy go when a car brakes?
    a: Mostly into heat in the brakes. Electric and hybrid cars recover part of it with regenerative braking.
related: [physics/potential-energy, physics/momentum, physics/suvat-equations]
''',f'''
## How to use this calculator

Enter **mass** and **speed** to get the kinetic energy, or enter the energy to find the speed. Units convert automatically (km/h, mph, m/s; J, kJ, kWh).

## The formula

<p class="formula">KE = ½ m v²</p>

## Worked example

A 1,200 kg car at 100 km/h (27.78 m/s):

KE = 0.5 × 1,200 × 27.78² = **{0.5*m*v*v/1000:.0f} kJ**

At 50 km/h the same car has only {0.5*m*(v/2)**2/1000:.0f} kJ — one quarter.

## Speed and safety

| Speed | Kinetic energy (1,200 kg car) |
|---|---|
| 30 km/h | {0.5*m*(30/3.6)**2/1000:.0f} kJ |
| 50 km/h | {0.5*m*(50/3.6)**2/1000:.0f} kJ |
| 80 km/h | {0.5*m*(80/3.6)**2/1000:.0f} kJ |
| 120 km/h | {0.5*m*(120/3.6)**2/1000:.0f} kJ |

This is why small speed increases make crashes much more severe.
''')

page(C,'potential-energy',f'''
title: Potential Energy Calculator (PE = mgh)
description: Calculate gravitational potential energy from mass and height — or the height for a given energy.
category: physics
keywords: [potential energy, pe = mgh, gravitational potential energy, joules, energy calculator, height]
{U}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 1000, min: 0 }}
  - {{ id: h, label: Height, family: length, unit: m, imperialUnit: ft, default: 50 }}
  - {{ id: PE, label: Potential energy, family: energy, unit: kJ }}
equations:
  - PE = m * g0 * h
chart: {{ x: h, y: PE, from: 0, to: 100 }}
faq:
  - q: What is gravitational potential energy?
    a: The energy an object has because of its height. Lifting it stores energy that is released when it falls.
  - q: Why is it m × g × h?
    a: Lifting a mass m against gravity g through height h takes force mg over distance h, and work = force × distance.
  - q: Can it be converted to electricity?
    a: Yes. Hydropower and pumped-storage plants turn falling water's potential energy into electricity at around 80–90% efficiency.
related: [physics/kinetic-energy, physics/work-and-power, engineering/pump-power]
''',f'''
## How to use this calculator

Enter the **mass** and **height** to get the potential energy, or enter the energy to find the height. Choose J, kJ, kWh or other energy units.

## The formula

<p class="formula">PE = m × g × h   (g = 9.80665 m/s²)</p>

## Worked example

1,000 kg (1 m³) of water held 50 m above a turbine:

PE = 1,000 × 9.81 × 50 = **{1000*g*50/1000:.0f} kJ** = {1000*g*50/3.6e6:.3f} kWh

## Energy conservation

If dropped, the object's potential energy turns into kinetic energy. Ignoring air resistance, its speed at the bottom is v = √(2gh) — for 50 m that is {math.sqrt(2*g*50):.1f} m/s. Check it with the [free fall calculator](/physics/free-fall/).

## Height is measured from a reference

Potential energy is always relative to a chosen zero level, such as the floor or the turbine.
''')

page(C,'work-and-power',f'''
title: Work & Power Calculator
description: Calculate work done (W = F × d) and power (P = W ÷ t) from force, distance and time.
category: physics
keywords: [work calculator, power calculator, work = force x distance, watts, joules, physics power]
{U}
variables:
  - {{ id: F, label: Force, family: force, unit: N, imperialUnit: lbf, default: 500 }}
  - {{ id: d, label: Distance moved (in direction of force), family: length, unit: m, imperialUnit: ft, default: 10 }}
  - {{ id: t, label: Time taken, family: seconds, unit: s, default: 20, min: 0 }}
  - {{ id: W, label: Work done, family: energy, unit: J }}
  - {{ id: P, label: Power, family: power, unit: W, imperialUnit: hp }}
equations:
  - W = F * d
  - P = W / t
faq:
  - q: What is work in physics?
    a: Work is done when a force moves something. Work = force × distance moved in the direction of the force, measured in joules.
  - q: What is the difference between work and power?
    a: Work is the amount of energy transferred. Power is how fast it is transferred — work divided by time, in watts.
  - q: What if the force is at an angle?
    a: Use only the part of the force along the direction of motion, F × cos θ.
related: [physics/potential-energy, physics/force, conversion/power-converter]
''',f'''
## How to use this calculator

Enter the **force**, the **distance** it moves and the **time** taken. You get the work done in joules and the power in watts (or hp).

## Formulas

<p class="formula">W = F × d   P = W ÷ t</p>

## Worked example

Pushing a cart with 500 N over 10 m in 20 s:

- Work = 500 × 10 = **5,000 J**
- Power = 5,000 ÷ 20 = **250 W** ({250/745.7:.2f} hp)

## Climbing stairs

A 70 kg person climbs 3 m of stairs in 4 s: work = 70 × 9.81 × 3 = {70*g*3:.0f} J, power = {70*g*3/4:.0f} W — similar to a bright old-style light bulb.
''')

page(C,'momentum',f'''
title: Momentum Calculator (p = mv)
description: Calculate momentum from mass and velocity, or find velocity or mass from momentum.
category: physics
keywords: [momentum calculator, p = mv, linear momentum, impulse, kg m/s, conservation of momentum]
{U}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 0.16, min: 0 }}
  - {{ id: v, label: Velocity, family: velocity, unit: kmh, imperialUnit: mph, default: 140 }}
  - {{ id: p, label: Momentum, suffix: kg·m/s }}
equations:
  - p = m * v
faq:
  - q: What is momentum?
    a: The quantity of motion an object has — its mass times its velocity. It has direction as well as size.
  - q: What is conservation of momentum?
    a: In a collision with no outside forces, the total momentum before equals the total after.
  - q: What is impulse?
    a: The change in momentum, equal to force × time. Spreading a stop over a longer time (air bags, crumple zones) reduces the force.
related: [physics/kinetic-energy, physics/force]
''',f'''
## How to use this calculator

Enter **mass** and **velocity** to get momentum in kg·m/s. You can also solve for velocity or mass.

## The formula

<p class="formula">p = m × v</p>

## Worked example

A 160 g cricket ball bowled at 140 km/h (38.9 m/s):

p = 0.16 × 38.89 = **{0.16*140/3.6:.2f} kg·m/s**

A 1,200 kg car at just 0.5 km/h has a similar momentum: {1200*0.5/3.6:.0f} kg·m/s.

## Impulse and safety

Force = change in momentum ÷ time. Catching a ball by pulling your hands back extends the stopping time and reduces the force on your hands — the same principle behind helmets, air bags and crumple zones.
''')

page(C,'density',f'''
title: Density Calculator (ρ = m/V)
description: Calculate density from mass and volume — or mass or volume from density — in kg/m³, g/cm³ and lb/ft³.
category: physics
keywords: [density calculator, density formula, mass volume, kg/m3, g/cm3, specific gravity]
{U}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 7.85, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: L, imperialUnit: ft3, default: 1, min: 0 }}
  - {{ id: rho, label: Density, family: density, unit: kgm3, imperialUnit: lbft3, min: 0 }}
  - {{ id: sg, label: Specific gravity (vs water), min: 0, decimals: 4 }}
equations:
  - rho = m / V
  - sg = rho / 1000
faq:
  - q: What is the density formula?
    a: Density = mass ÷ volume. Its SI unit is kg/m³; 1 g/cm³ = 1,000 kg/m³.
  - q: What is specific gravity?
    a: Density relative to water (about 1,000 kg/m³). Steel has a specific gravity of about 7.85.
  - q: Will it float?
    a: In water, objects with specific gravity below 1 float and those above 1 sink.
related: [engineering/mass-flow-rate, engineering/hydrostatic-pressure, physics/pressure]
''',f'''
## How to use this calculator

Enter **mass** and **volume** to get density and specific gravity, or enter density to find mass or volume.

## The formula

<p class="formula">ρ = m ÷ V</p>

## Worked example

A 1-litre block of steel has a mass of 7.85 kg:

ρ = 7.85 kg ÷ 0.001 m³ = **7,850 kg/m³** (specific gravity 7.85)

## Common densities

| Material | kg/m³ |
|---|---|
| Air (20 °C) | 1.2 |
| Wood (pine) | 500 |
| Ice | 917 |
| Water | 998 |
| Concrete | 2,400 |
| Aluminium | 2,700 |
| Steel | 7,850 |
| Copper | 8,960 |
| Gold | 19,300 |
''')

page(C,'pressure',f'''
title: Pressure Calculator (P = F/A)
description: Calculate pressure from force and area — or the force or area — in Pa, kPa, bar or psi.
category: physics
keywords: [pressure calculator, p = f/a, force over area, pascal, psi, stress]
{U}
variables:
  - {{ id: F, label: Force, family: force, unit: N, imperialUnit: lbf, default: 700, min: 0 }}
  - {{ id: A, label: Area, family: area, unit: cm2, imperialUnit: in2, default: 400, min: 0 }}
  - {{ id: P, label: Pressure, family: pressure, unit: kPa, imperialUnit: psi, min: 0 }}
equations:
  - P = F / A
faq:
  - q: What is the pressure formula?
    a: Pressure = force ÷ area. One pascal is one newton per square metre.
  - q: Why do sharp knives cut better?
    a: The same force on a much smaller area creates much higher pressure.
  - q: Why do snowshoes work?
    a: They spread your weight over a larger area, lowering the pressure so you don't sink.
related: [conversion/pressure-converter, physics/force, engineering/hydraulic-cylinder-force]
''',f'''
## How to use this calculator

Enter the **force** and the **area** it acts on. The pressure appears in kPa, bar, psi or any pressure unit. You can also find the area needed to keep pressure below a limit.

## The formula

<p class="formula">P = F ÷ A</p>

## Worked example

A 70 kg person (about 700 N) standing on two feet covering 400 cm²:

P = 700 ÷ 0.04 = **17,500 Pa** = 17.5 kPa

On stiletto heels with 1 cm² each carrying half the weight, the pressure under each heel is 350 N ÷ 0.0001 m² = **3,500 kPa** — 200 times higher.

## Units

1 Pa = 1 N/m² · 1 kPa = 1,000 Pa · 1 bar = 100 kPa · 1 psi = 6.895 kPa
''')

h=20; tt=math.sqrt(2*h/g)
page(C,'free-fall',f'''
title: Free Fall Calculator
description: Calculate fall time, impact speed and fall height for an object dropped from rest, ignoring air resistance.
category: physics
keywords: [free fall calculator, falling object, fall time, impact velocity, gravity, drop height]
{U}
variables:
  - {{ id: h, label: Fall height, family: length, unit: m, imperialUnit: ft, default: 20, min: 0 }}
  - {{ id: t, label: Fall time, family: seconds, unit: s, min: 0 }}
  - {{ id: v, label: Impact speed, family: velocity, unit: ms, imperialUnit: mph, min: 0 }}
equations:
  - h = g0 * t^2 / 2
  - v = g0 * t
chart: {{ x: h, y: v, from: 0, to: 100 }}
faq:
  - q: How long does it take to fall 20 m?
    a: About 2.02 seconds, reaching about 19.8 m/s (71 km/h), ignoring air resistance.
  - q: Do heavy objects fall faster?
    a: Not in a vacuum — all objects accelerate at the same rate. In air, drag slows light or large objects more.
  - q: What is terminal velocity?
    a: The speed at which air resistance balances gravity. For a skydiver in a belly-down position it is about 200 km/h.
related: [physics/suvat-equations, physics/projectile-motion, physics/potential-energy]
''',f'''
## How to use this calculator

Enter the **height**, the **fall time** or the **impact speed** — the other two are calculated. Results ignore air resistance, which is accurate for short drops of dense objects.

## Formulas

<p class="formula">h = ½ g t²   v = g t   v = √(2gh)</p>

## Worked example

A stone dropped from 20 m:

- t = √(2 × 20 ÷ 9.81) = **{tt:.2f} s**
- v = 9.81 × {tt:.2f} = **{g*tt:.1f} m/s** ({g*tt*3.6:.0f} km/h)

## Measuring a well's depth

Drop a stone and time the splash. If it takes 2 s, the depth is about 19.6 m (a little less once you allow for the time sound takes to travel back up).

## Fall distances

| Time | Distance | Speed |
|---|---|---|
| 1 s | 4.9 m | 9.8 m/s |
| 2 s | 19.6 m | 19.6 m/s |
| 3 s | 44.1 m | 29.4 m/s |
| 4 s | 78.5 m | 39.2 m/s |
''')

v0,th=20,math.radians(45)
page(C,'projectile-motion',f'''
title: Projectile Motion Calculator
description: Calculate range, maximum height and flight time of a projectile from launch speed and angle.
category: physics
keywords: [projectile motion, range calculator, launch angle, maximum height, time of flight, trajectory]
{U}
variables:
  - {{ id: v, label: Launch speed, family: velocity, unit: ms, imperialUnit: fts, default: 20, min: 0 }}
  - {{ id: th, label: Launch angle, family: angle, unit: deg, default: 45, min: 0, max: 1.5708 }}
  - {{ id: R, label: Range (horizontal distance), family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: H, label: Maximum height, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: T, label: Time of flight, family: seconds, unit: s, min: 0 }}
equations:
  - R = v^2 * sin(2 * th) / g0
  - H = v^2 * sin(th)^2 / (2 * g0)
  - T = 2 * v * sin(th) / g0
chart: {{ x: th, y: R, from: 0, to: 90 }}
faq:
  - q: What angle gives the maximum range?
    a: 45° on level ground, ignoring air resistance. Complementary angles such as 30° and 60° give the same range.
  - q: Does this include air resistance?
    a: No. Real projectiles such as balls fall shorter, and the best angle is usually a little below 45°.
  - q: Does this assume level ground?
    a: Yes — the projectile lands at the same height it was launched from.
related: [physics/free-fall, physics/suvat-equations]
''',f'''
## How to use this calculator

Enter the **launch speed** and **angle** to get the range, maximum height and flight time. The chart shows how range changes with angle — note the peak at 45°.

## Formulas (level ground, no air resistance)

<p class="formula">R = v² sin(2θ) ÷ g<br/>H = v² sin²θ ÷ 2g<br/>T = 2v sin θ ÷ g</p>

## Worked example

Launched at 20 m/s and 45°:

- Range = 400 × 1 ÷ 9.81 = **{v0**2*math.sin(2*th)/g:.1f} m**
- Maximum height = **{v0**2*math.sin(th)**2/(2*g):.1f} m**
- Flight time = **{2*v0*math.sin(th)/g:.2f} s**

## Range at different angles (20 m/s)

| Angle | Range |
|---|---|
| 15° | {400*math.sin(math.radians(30))/g:.1f} m |
| 30° | {400*math.sin(math.radians(60))/g:.1f} m |
| 45° | {400/g:.1f} m |
| 60° | {400*math.sin(math.radians(120))/g:.1f} m |
| 75° | {400*math.sin(math.radians(150))/g:.1f} m |
''')

Rg=8.314462618
page(C,'ideal-gas-law',f'''
title: Ideal Gas Law Calculator (PV = nRT)
description: Solve the ideal gas law for pressure, volume, amount of gas (moles) or temperature.
category: physics
keywords: [ideal gas law, pv = nrt, gas law calculator, moles of gas, gas constant, stp]
{U}
featured: true
variables:
  - {{ id: P, label: Pressure (absolute), family: pressure, unit: kPa, imperialUnit: psi, default: 101.325, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: L, imperialUnit: ft3, min: 0 }}
  - {{ id: n, label: Amount of gas, suffix: mol, default: 1, min: 0 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, imperialUnit: F, default: 0, min: 0 }}
equations:
  - P * V = n * 8.314462618 * T
chart: {{ x: T, y: V, from: -50, to: 200 }}
faq:
  - q: What is the ideal gas law?
    a: PV = nRT, linking pressure, volume, amount of gas and absolute temperature. R = 8.314 J/(mol·K).
  - q: What volume does one mole of gas occupy?
    a: About 22.41 L at 0 °C and 1 atm, and about 24.47 L at 25 °C and 1 atm.
  - q: Why must pressure and temperature be absolute?
    a: The law is based on absolute zero and zero pressure. The calculator converts °C and °F to kelvin automatically; enter absolute pressure (gauge + atmospheric).
related: [chemistry/moles, physics/density, conversion/pressure-converter]
''',f'''
## How to use this calculator

Enter **any three** of pressure, volume, moles and temperature to find the fourth. Pressure must be **absolute** (not gauge); temperature can be in °C, °F or K.

## The formula

<p class="formula">P V = n R T   (R = 8.314 J/mol·K)</p>

## Worked example

1 mol of gas at 0 °C (273.15 K) and 101.325 kPa:

V = nRT ÷ P = 1 × 8.314 × 273.15 ÷ 101,325 = **{Rg*273.15/101325*1000:.2f} L**

At 25 °C it expands to {Rg*298.15/101325*1000:.2f} L.

## Combined gas law

For a fixed amount of gas, P₁V₁/T₁ = P₂V₂/T₂. A tyre at 220 kPa absolute and 20 °C warms to 50 °C: P₂ = 220 × 323.15 ÷ 293.15 ≈ **243 kPa**.

## When it is less accurate

Real gases deviate at very high pressures and low temperatures, close to condensing. For air and most gases at everyday conditions, the error is well under 1%.
''')

page(C,'wavelength-frequency',f'''
title: Wavelength & Frequency Calculator
description: Convert between wavelength, frequency and wave speed for light, radio and sound (v = fλ).
category: physics
keywords: [wavelength calculator, frequency to wavelength, wave speed, v = f lambda, speed of light, radio wavelength]
{U}
variables:
  - id: c
    label: Wave type / medium
    default: 299792458
    options:
      - {{ label: Light or radio in vacuum (299,792,458 m/s), value: 299792458 }}
      - {{ label: Sound in air, 20 °C (343 m/s), value: 343 }}
      - {{ label: Sound in water (1,481 m/s), value: 1481 }}
      - {{ label: Sound in steel (5,960 m/s), value: 5960 }}
  - {{ id: f, label: Frequency, suffix: Hz, default: 100000000, min: 0 }}
  - {{ id: lam, label: Wavelength, family: length, unit: m, imperialUnit: ft, min: 0 }}
equations:
  - c = f * lam
faq:
  - q: How do I convert frequency to wavelength?
    a: Wavelength = wave speed ÷ frequency. For radio, divide 300,000,000 by the frequency in Hz to get metres.
  - q: What is the wavelength of 2.4 GHz Wi-Fi?
    a: About 12.5 cm.
  - q: What is the wavelength of middle A (440 Hz) in air?
    a: About 78 cm at 20 °C.
related: [physics/speed-distance-time]
''',f'''
## How to use this calculator

Choose the **type of wave**, then enter the **frequency** (in Hz) or the **wavelength**. The other is calculated.

## The formula

<p class="formula">v = f × λ</p>

## Worked examples

- **FM radio at 100 MHz:** λ = 299,792,458 ÷ 100,000,000 = **{299792458/1e8:.2f} m**
- **Wi-Fi at 2.4 GHz:** λ = **{299792458/2.4e9*100:.1f} cm**
- **Sound at 440 Hz in air:** λ = 343 ÷ 440 = **{343/440*100:.0f} cm**

## The electromagnetic spectrum

| Band | Wavelength |
|---|---|
| AM radio | ~200–600 m |
| FM radio | ~3 m |
| Microwaves / Wi-Fi | 1 mm – 30 cm |
| Visible light | 380–750 nm |
| X-rays | 0.01–10 nm |

Tip: for MHz, enter the value × 1,000,000 Hz (100 MHz = 100000000).
''')

L=1
page(C,'pendulum',f'''
title: Pendulum Period Calculator
description: Calculate the period and frequency of a simple pendulum from its length — or the length for a given period.
category: physics
keywords: [pendulum calculator, pendulum period, simple pendulum, t = 2 pi sqrt(l/g), seconds pendulum]
{U}
variables:
  - {{ id: L, label: Pendulum length, family: length, unit: m, imperialUnit: ft, default: 1, min: 0 }}
  - {{ id: T, label: Period (one full swing), family: seconds, unit: s, min: 0 }}
  - {{ id: f, label: Frequency, suffix: Hz, min: 0 }}
equations:
  - T = 2 * pi * sqrt(L / g0)
  - f = 1 / T
chart: {{ x: L, y: T, from: 0, to: 5 }}
faq:
  - q: What is the formula for a pendulum's period?
    a: T = 2π √(L/g), where L is the length to the centre of the bob and g is gravity. It does not depend on mass.
  - q: How long is a seconds pendulum?
    a: About 0.994 m. Its full period is 2 s, so each swing in one direction takes 1 second.
  - q: Does the swing size matter?
    a: For small angles (under about 15°) hardly at all. Larger swings take slightly longer.
related: [physics/free-fall, physics/wavelength-frequency]
''',f'''
## How to use this calculator

Enter the **length** (pivot to the centre of the bob) to get the period and frequency. Or enter a period to find the length needed.

## The formula

<p class="formula">T = 2π √(L ÷ g)</p>

## Worked example

A 1 m pendulum:

T = 2π √(1 ÷ 9.81) = **{2*math.pi*math.sqrt(1/g):.3f} s**, frequency **{1/(2*math.pi*math.sqrt(1/g)):.3f} Hz**

## Period vs length

| Length | Period |
|---|---|
| 0.25 m | {2*math.pi*math.sqrt(0.25/g):.2f} s |
| 0.5 m | {2*math.pi*math.sqrt(0.5/g):.2f} s |
| 1 m | {2*math.pi*math.sqrt(1/g):.2f} s |
| 2 m | {2*math.pi*math.sqrt(2/g):.2f} s |
| 4 m | {2*math.pi*math.sqrt(4/g):.2f} s |

Four times the length doubles the period. This is why grandfather clocks are tall — a ~1 m pendulum ticks once per second.
''')

page(C,'centripetal-force',f'''
title: Centripetal Force Calculator
description: Calculate centripetal force and acceleration for an object moving in a circle from mass, speed and radius.
category: physics
keywords: [centripetal force, circular motion, centripetal acceleration, f = mv2/r, g force in turns]
{U}
variables:
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: 1200, min: 0 }}
  - {{ id: v, label: Speed, family: velocity, unit: kmh, imperialUnit: mph, default: 60, min: 0 }}
  - {{ id: r, label: Radius of the circle, family: length, unit: m, imperialUnit: ft, default: 50, min: 0 }}
  - {{ id: ac, label: Centripetal acceleration, suffix: m/s², min: 0 }}
  - {{ id: F, label: Centripetal force, family: force, unit: kN, imperialUnit: lbf, min: 0 }}
equations:
  - ac = v^2 / r
  - F = m * ac
faq:
  - q: What is centripetal force?
    a: The inward force needed to keep an object moving in a circle. For a car, it is supplied by tyre friction.
  - q: Why is taking a bend fast dangerous?
    a: Force rises with the square of speed. Doubling speed needs four times the grip.
  - q: What is centrifugal force?
    a: The outward push you feel inside a turning car. It is an effect of your inertia, not a real outward force.
related: [physics/force, physics/kinetic-energy]
''',f'''
## How to use this calculator

Enter the **mass**, **speed** and **radius** to get the centripetal acceleration and force. Or find the maximum safe speed for a given radius and force.

## Formulas

<p class="formula">a = v² ÷ r   F = m v² ÷ r</p>

## Worked example

A 1,200 kg car takes a 50 m radius bend at 60 km/h (16.67 m/s):

- a = 16.67² ÷ 50 = **{(60/3.6)**2/50:.2f} m/s²** ({(60/3.6)**2/50/g:.2f} g)
- F = 1,200 × {(60/3.6)**2/50:.2f} = **{1200*(60/3.6)**2/50/1000:.2f} kN**

## Grip limit

On a dry road, tyres can typically provide around 0.7–0.9 g of sideways acceleration; on wet roads much less. At 0.7 g, the maximum speed for a 50 m bend is about √(0.7 × 9.81 × 50) = {math.sqrt(0.7*g*50)*3.6:.0f} km/h.
''')

R1,R2,R3=100,220,470
page(C,'resistors-series-parallel',f'''
title: Resistors in Series & Parallel Calculator
description: Calculate total resistance of up to three resistors connected in series or in parallel.
category: physics
keywords: [resistors in parallel, resistors in series, equivalent resistance, parallel resistance calculator, ohms]
{U}
variables:
  - {{ id: R1, label: Resistor R1, family: resistance, unit: ohm, default: 100, min: 0 }}
  - {{ id: R2, label: Resistor R2, family: resistance, unit: ohm, default: 220, min: 0 }}
  - {{ id: R3, label: Resistor R3 (use a huge value like 1e12 if not used), family: resistance, unit: ohm, default: 470, min: 0 }}
  - {{ id: Rs, label: Total in series, family: resistance, unit: ohm, min: 0 }}
  - {{ id: Rp, label: Total in parallel, family: resistance, unit: ohm, min: 0 }}
equations:
  - Rs = R1 + R2 + R3
  - Rp = 1 / (1/R1 + 1/R2 + 1/R3)
faq:
  - q: How do resistors add in series?
    a: Simply add them — R = R1 + R2 + R3. The same current flows through each one.
  - q: How do resistors combine in parallel?
    a: Add the reciprocals — 1/R = 1/R1 + 1/R2 + 1/R3. The total is always less than the smallest resistor.
  - q: What about only two resistors in parallel?
    a: Use R = (R1 × R2) ÷ (R1 + R2). For two equal resistors, the result is half of one.
related: [physics/ohms-law, physics/rc-time-constant]
''',f'''
## How to use this calculator

Enter up to **three resistor values** (Ω, kΩ or MΩ). You get the total for both a series and a parallel connection. For just two resistors, set R3 to a very large value such as 1e12 Ω.

## Formulas

<p class="formula">Series: R = R₁ + R₂ + R₃<br/>Parallel: 1/R = 1/R₁ + 1/R₂ + 1/R₃</p>

## Worked example

100 Ω, 220 Ω and 470 Ω:

- Series = **{R1+R2+R3} Ω**
- Parallel = 1 ÷ (1/100 + 1/220 + 1/470) = **{1/(1/R1+1/R2+1/R3):.1f} Ω**

## Quick rules

- Two equal resistors in parallel → half the value (2 × 1 kΩ = 500 Ω).
- n equal resistors in parallel → R ÷ n.
- Parallel total is always smaller than the smallest single resistor.

## Standard values (E12 series)

10 · 12 · 15 · 18 · 22 · 27 · 33 · 39 · 47 · 56 · 68 · 82 (× 1, 10, 100, 1k …)
''')

page(C,'rc-time-constant',f'''
title: RC Time Constant Calculator
description: Calculate the RC time constant, charging time and cut-off frequency of a resistor–capacitor circuit.
category: physics
keywords: [rc time constant, rc circuit, capacitor charging time, tau = rc, cutoff frequency, low pass filter]
{U}
variables:
  - {{ id: R, label: Resistance, family: resistance, unit: kohm, default: 10, min: 0 }}
  - {{ id: Cc, label: Capacitance, family: capacitance, unit: uF, default: 100, min: 0 }}
  - {{ id: tau, label: Time constant (τ), family: seconds, unit: s, min: 0 }}
  - {{ id: t5, label: Time to ~99% charge (5τ), family: seconds, unit: s, min: 0 }}
  - {{ id: fc, label: Cut-off frequency, suffix: Hz, min: 0 }}
equations:
  - tau = R * Cc
  - t5 = 5 * tau
  - fc = 1 / (2 * pi * tau)
faq:
  - q: What is the RC time constant?
    a: τ = R × C, the time for a capacitor to charge to about 63.2% of the supply voltage through a resistor.
  - q: How long does a capacitor take to charge fully?
    a: About 5 time constants (5RC) to reach 99.3%.
  - q: What is the cut-off frequency of an RC filter?
    a: fc = 1 ÷ (2πRC) — the frequency at which the output falls to 70.7% (−3 dB).
related: [physics/resistors-series-parallel, physics/ohms-law]
''',f'''
## How to use this calculator

Enter the **resistance** and **capacitance** to get the time constant, approximate full-charge time and filter cut-off frequency. You can also solve for the capacitor needed for a target time.

## Formulas

<p class="formula">τ = R C   t(≈99%) = 5τ   f<sub>c</sub> = 1 ÷ (2π R C)</p>

## Worked example

10 kΩ and 100 µF:

- τ = 10,000 × 0.0001 = **1 s**
- Full charge ≈ **5 s**
- Cut-off frequency = **{1/(2*math.pi):.3f} Hz**

## Charging curve

| Time | Charge (% of supply) |
|---|---|
| 1τ | 63.2% |
| 2τ | 86.5% |
| 3τ | 95.0% |
| 4τ | 98.2% |
| 5τ | 99.3% |

The same percentages apply in reverse when discharging. RC networks are used for timers, debouncing switches and simple signal filters.
''')
print('physics ok')
