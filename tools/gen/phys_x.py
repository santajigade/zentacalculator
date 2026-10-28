import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
g0 = 9.80665; pi = math.pi

expand('physics/acceleration', '''
## 0–100 km/h times and acceleration

| 0–100 km/h time | Average acceleration | In g |
|---|---|---|
''' + ''.join(f"| {t} s | {100/3.6/t:.2f} m/s² | {100/3.6/t/g0:.2f} g |\n" for t in [2.5, 3.5, 5, 7, 9, 12, 15]) + '''
## Deceleration and braking

Deceleration is negative acceleration. A car braking from 100 km/h to 0 in 3 seconds decelerates at about −9.26 m/s², close to 1 g — the limit for good tyres on dry roads. Distance travelled while braking is s = v² ÷ (2a); see the [SUVAT calculator](/physics/suvat-equations/).

## Units of acceleration

| Unit | In m/s² |
|---|---|
| 1 m/s² | 1 |
| 1 ft/s² | 0.3048 |
| 1 g (standard gravity) | 9.80665 |
| 1 km/h per second | 0.2778 |

## Acceleration in two or three dimensions

Acceleration is a vector. If an object speeds up and turns at the same time, its total acceleration combines the forward part (change in speed) and the sideways part (centripetal). Use the [centripetal force calculator](/physics/centripetal-force/) for the turning part.

## How much g can people take?

- Everyday driving: under 0.3 g.
- Roller coasters: up to about 4–5 g briefly.
- Fighter pilots with g-suits: about 9 g for short periods.
''', [
 ('What is the acceleration of a car going 0–100 km/h in 10 seconds?', '27.78 m/s ÷ 10 s = 2.78 m/s², about 0.28 g.'),
 ('Can acceleration be negative?', 'Yes. Negative acceleration means the object is slowing down in the chosen direction, often called deceleration.'),
], before='## Related equations')

expand('physics/centripetal-force', '''
## Centripetal acceleration on curves

| Speed | Radius 50 m | Radius 100 m | Radius 250 m |
|---|---|---|---|
''' + ''.join(f"| {v} km/h | {(v/3.6)**2/50:.2f} m/s² ({(v/3.6)**2/50/g0:.2f} g) | {(v/3.6)**2/100:.2f} m/s² | {(v/3.6)**2/250:.2f} m/s² |\n" for v in [30, 50, 80, 100, 120]) + '''
Doubling the speed **quadruples** the force needed, which is why speed limits drop on tight bends.

## Banked curves

Roads and racetracks are banked so that part of the normal force supplies the turning force. With no friction, the ideal banking angle is:

<p class="formula">tan θ = v² ÷ (r × g)</p>

For 80 km/h on a 200 m curve, θ = atan(493.8 ÷ 1961) = about **14°**.

## Angular speed form

If you know revolutions per minute instead of speed:

<p class="formula">a = ω² × r, with ω = 2π × rpm ÷ 60</p>

A centrifuge spinning at 3,000 rpm with a 10 cm radius produces about 9,870 m/s², or roughly **1,006 g**.

## Centripetal vs centrifugal

Centripetal force is the real force pointing **towards** the centre (friction, tension, gravity). Centrifugal force is the outward push you feel in a turning car, which comes from your body's inertia in a rotating frame of reference.
''', [
 ('What provides centripetal force for a car turning?', 'Friction between the tyres and the road. On ice there is little friction, so the car slides outward.'),
 ('What is the centripetal force formula?', 'F = m × v² ÷ r, where m is mass, v is speed and r is the radius of the circular path.'),
], before='## Grip limit')

expand('physics/density', '''
## Density of common materials

| Material | kg/m³ | g/cm³ |
|---|---|---|
| Air (20 °C, sea level) | 1.2 | 0.0012 |
| Petrol | 720–750 | 0.72–0.75 |
| Ice | 917 | 0.917 |
| Water (4 °C) | 1,000 | 1.000 |
| Seawater | 1,025 | 1.025 |
| Concrete | 2,300–2,400 | 2.3–2.4 |
| Aluminium | 2,700 | 2.70 |
| Steel | 7,850 | 7.85 |
| Copper | 8,960 | 8.96 |
| Lead | 11,340 | 11.34 |
| Gold | 19,320 | 19.32 |

## Will it float?

An object floats in water if its average density is less than 1,000 kg/m³. Ice (917) floats with about 92% of its volume under water. Steel ships float because their hollow hulls make the average density lower than water.

## Density and temperature

Most materials expand when heated, so density falls. Water is unusual: it is densest at about 4 °C, which is why lakes freeze from the top down. Use [thermal expansion](/engineering/thermal-expansion/) to estimate the change for solids.

## Finding volume by displacement

For irregular objects, drop them in a measuring jug and read the rise in water level. A stone that raises the level by 120 mL has a volume of 120 cm³. Weigh it and divide to get the density.

## Specific gravity

Specific gravity is density compared with water, with no units. It is used for liquids such as acids, fuels and syrups, and for gemstones and minerals.
''', [
 ('What is the density of water?', 'About 1,000 kg/m³ (1 g/cm³) at 4 °C, and 998 kg/m³ at 20 °C.'),
 ('How do I find mass from density and volume?', 'Mass = density × volume. 2 litres of steel weighs 7,850 × 0.002 = 15.7 kg.'),
])

expand('physics/force', '''
## Force examples

| Situation | Mass | Acceleration | Force |
|---|---|---|---|
| Pushing a shopping trolley | 30 kg | 0.5 m/s² | 15 N |
| Car accelerating | 1,200 kg | 3 m/s² | 3,600 N |
| Lift starting upward | 800 kg | 1 m/s² | 800 N (plus weight) |
| Sprinter starting | 75 kg | 6 m/s² | 450 N |
| Football kick | 0.43 kg | 2,000 m/s² (briefly) | 860 N |

## Newton's three laws

1. **Inertia**: an object stays at rest or keeps moving at a constant speed unless a net force acts on it.
2. **F = ma**: the net force equals mass times acceleration.
3. **Action and reaction**: every force has an equal and opposite force on the other object.

## Weight is a force

Weight is the force of gravity: W = m × g. A 70 kg person weighs about 686 N on Earth. See the [weight calculator](/physics/weight/) for other planets.

## Friction

Friction resists sliding. The maximum friction force is μ × N, where μ is the coefficient of friction and N is the normal force. Rubber on dry concrete has μ ≈ 0.7–0.8; steel on ice is under 0.05.
''', [
 ('What is 1 newton?', 'The force that accelerates 1 kg at 1 m/s². It is roughly the weight of a small apple (about 100 g).'),
 ('How do I convert kgf to newtons?', 'Multiply by 9.80665. 10 kgf is about 98 N.'),
], before='## Units of force')

expand('physics/free-fall', '''
## Air resistance and terminal velocity

Real objects do not keep accelerating. Air resistance grows with speed until it balances weight, and the object falls at **terminal velocity**:

| Object | Approximate terminal velocity |
|---|---|
| Raindrop | 9 m/s (32 km/h) |
| Skydiver, belly down | 55 m/s (200 km/h) |
| Skydiver, head down | 80–90 m/s (300 km/h) |
| Feather | under 1 m/s |

The calculator ignores air resistance, so it is accurate for short drops of dense objects, but overestimates speed for long falls.

## Time and speed for each second

| Time | Distance fallen | Speed |
|---|---|---|
''' + ''.join(f"| {t} s | {g0*t*t/2:.1f} m | {g0*t:.1f} m/s ({g0*t*3.6:.0f} km/h) |\n" for t in [0.5, 1, 1.5, 2, 3, 4, 5]) + '''
Distance grows with the square of time: in 2 seconds an object falls four times as far as in 1 second.

## Galileo's insight

Without air resistance, all objects fall at the same rate regardless of mass. Astronaut David Scott demonstrated this on the Moon in 1971 by dropping a hammer and a feather, which landed together.
''', [
 ('How long does it take to fall 100 m?', 'About 4.5 seconds, ignoring air resistance, reaching about 44 m/s.'),
 ('Does a heavier object fall faster?', 'Not in a vacuum. In air, heavier dense objects are less slowed by air resistance, so they can reach the ground sooner.'),
], before="## Measuring a well's depth")

expand('physics/ideal-gas-law', '''
## Molar volume at different conditions

The volume of 1 mole of an ideal gas:

| Conditions | Temperature | Pressure | Volume |
|---|---|---|---|
| STP (IUPAC) | 0 °C | 100 kPa | 22.71 L |
| Older STP | 0 °C | 101.325 kPa | 22.41 L |
| Room conditions | 25 °C | 101.325 kPa | 24.47 L |

Always check which standard a textbook or datasheet uses.

## The gas constant R

| Units | Value of R |
|---|---|
| J/(mol·K) or kPa·L/(mol·K) | 8.314 |
| L·atm/(mol·K) | 0.08206 |
| L·bar/(mol·K) | 0.08314 |

## Using mass instead of moles

n = mass ÷ molar mass. For 64 g of oxygen (O₂, 32 g/mol), n = 2 mol. Common molar masses: N₂ 28, O₂ 32, CO₂ 44, air about 28.97 g/mol.

## Density of a gas

Rearranging gives gas density: ρ = P × M ÷ (R × T). Air at 20 °C and 101.325 kPa has a density of about **1.204 kg/m³**.

## Always use absolute values

Temperature must be in kelvin (or entered in °C so the calculator converts it) and pressure must be absolute, not gauge. A tyre at 2.2 bar gauge is about 3.2 bar absolute.
''', [
 ('What is the ideal gas law?', 'PV = nRT: pressure × volume = moles × gas constant × absolute temperature.'),
 ('What volume does 1 mole of gas occupy?', 'About 22.4 L at 0 °C and 1 atm, and about 24.5 L at 25 °C and 1 atm.'),
], before='## When it is less accurate')

expand('physics/kinetic-energy', '''
## Kinetic energy of everyday objects

| Object | Mass | Speed | Kinetic energy |
|---|---|---|---|
''' + ''.join(f"| {n} | {m} kg | {v} km/h | {0.5*m*(v/3.6)**2:,.0f} J |\n" for n, m, v in [('Cricket ball (fast bowl)', 0.16, 140), ('Cyclist with bike', 85, 25), ('Sprinter', 75, 36), ('Motorbike and rider', 250, 100), ('Car', 1200, 50), ('Car', 1200, 100), ('Truck', 20000, 80)]) + '''
## Kinetic energy and braking distance

The brakes must remove all the kinetic energy as heat. Since energy rises with speed squared, braking distance does too: at 100 km/h a car needs about **four times** the braking distance it needs at 50 km/h.

## Work–energy theorem

The work done on an object equals its change in kinetic energy:

<p class="formula">W = ½mv₂² − ½mv₁²</p>

This lets you find the average force needed to stop something over a given distance: F = KE ÷ d.

## Rotational kinetic energy

Spinning objects such as flywheels and wheels also store energy: KE = ½ × I × ω², where I is the moment of inertia and ω the angular speed in rad/s.
''', [
 ('What happens to kinetic energy if speed doubles?', 'It becomes four times larger, because kinetic energy depends on speed squared.'),
 ('Is kinetic energy ever negative?', 'No. Mass and speed squared are always positive, so kinetic energy is zero or positive.'),
], before='## Speed and safety')

expand('physics/momentum', '''
## Momentum examples

| Object | Mass | Speed | Momentum |
|---|---|---|---|
''' + ''.join(f"| {n} | {m} kg | {v} km/h | {m*v/3.6:,.1f} kg·m/s |\n" for n, m, v in [('Tennis serve', 0.058, 200), ('Cricket ball', 0.16, 140), ('Footballer running', 75, 30), ('Car', 1200, 50), ('Loaded truck', 30000, 60)]) + '''
## Conservation of momentum

In a collision with no outside forces, the total momentum before equals the total after:

<p class="formula">m₁u₁ + m₂u₂ = m₁v₁ + m₂v₂</p>

**Example**: a 1,000 kg car at 20 m/s hits a stationary 1,500 kg car and they move off together. Final speed = 20,000 ÷ 2,500 = **8 m/s**.

## Elastic vs inelastic collisions

| Type | Momentum conserved? | Kinetic energy conserved? |
|---|---|---|
| Elastic (billiard balls, nearly) | Yes | Yes |
| Inelastic (most real collisions) | Yes | No — some becomes heat and sound |
| Perfectly inelastic (objects stick) | Yes | Largest loss |

## Recoil

When a gun fires, the bullet's forward momentum equals the gun's backward momentum. A heavier gun recoils more slowly, which is why recoil feels softer in heavier firearms. Rockets work the same way: exhaust is pushed backward, the rocket moves forward.
''', [
 ('What are the units of momentum?', 'Kilogram-metres per second (kg·m/s), which is the same as newton-seconds (N·s).'),
 ('What is the difference between momentum and kinetic energy?', 'Momentum (mv) is a vector and is always conserved in collisions. Kinetic energy (½mv²) is a scalar and is only conserved in elastic collisions.'),
], before='## Impulse and safety')

expand('physics/ohms-law', '''
## Ohm's law wheel: all twelve formulas

| Find | From V and I | From V and R | From I and R | From P and … |
|---|---|---|---|---|
| Voltage V | — | — | I × R | √(P × R) or P ÷ I |
| Current I | — | V ÷ R | — | P ÷ V or √(P ÷ R) |
| Resistance R | V ÷ I | — | — | V² ÷ P or P ÷ I² |
| Power P | V × I | V² ÷ R | I² × R | — |

The calculator uses all of these automatically — fill any two fields.

## Resistor power ratings

A resistor must handle the power it dissipates. Pick a rating at least twice the calculated value:

| Calculated power | Choose at least |
|---|---|
| Up to 0.1 W | 1/4 W |
| Up to 0.25 W | 1/2 W |
| Up to 0.5 W | 1 W |
| Up to 1 W | 2 W |

## Household examples (230 V)

| Appliance | Power | Current | Effective resistance |
|---|---|---|---|
| LED bulb | 10 W | 0.043 A | 5,290 Ω |
| Laptop charger | 65 W | 0.28 A | 814 Ω |
| Kettle | 2,000 W | 8.7 A | 26.5 Ω |
| Room heater | 2,000 W | 8.7 A | 26.5 Ω |

At 120 V the same appliances draw about twice the current.

## When Ohm's law does not apply

Ohm's law holds for resistors and metal wires at constant temperature. It does not apply directly to diodes, LEDs, transistors or gas-discharge lamps, whose resistance changes with current. For LEDs, use the [LED resistor calculator](/other/led-resistor/).
''', [
 ('What is the formula for current?', 'I = V ÷ R. 24 V across 250 Ω gives 0.096 A (96 mA).'),
 ('How do I calculate power from voltage and resistance?', 'P = V² ÷ R. 12 V across 6 Ω dissipates 24 W.'),
], before='## Practical tips')

expand('physics/pendulum', '''
## Period for different lengths

| Length | Period | Swings per minute |
|---|---|---|
''' + ''.join(f"| {L} m | {2*pi*math.sqrt(L/g0):.3f} s | {60/(2*pi*math.sqrt(L/g0)):.1f} |\n" for L in [0.1, 0.25, 0.5, 0.994, 1, 2, 5, 10, 67]) + '''
A length of 0.994 m gives a period of 2 seconds — the classic **seconds pendulum**, where each one-way swing takes 1 second. The 67 m row is about the length of Foucault's famous pendulum in the Panthéon, Paris.

## Small-angle assumption

The formula is accurate for swings up to about 15°. At larger angles the period is longer:

| Amplitude | Period increase |
|---|---|
| 10° | +0.2% |
| 20° | +0.8% |
| 45° | +4.0% |
| 90° | +18.0% |

## Measuring g with a pendulum

Rearrange the formula: g = 4π² × L ÷ T². Time 20 full swings to reduce timing error, then divide by 20. With L = 1.000 m and T = 2.006 s, g = 9.81 m/s².

## Pendulum clocks

A pendulum clock that runs slow has a pendulum that is too long. Raising the bob by just 1 mm on a seconds pendulum speeds it up by about 43 seconds a day.
''', [
 ('Does the mass of the bob change the period?', 'No. For a simple pendulum the period depends only on length and gravity, not on mass.'),
 ('How long is a pendulum with a 1-second period?', 'About 24.8 cm.'),
], before='## Period vs length')

expand('physics/potential-energy', '''
## Potential energy examples

| Situation | Mass | Height | Energy |
|---|---|---|---|
''' + ''.join(f"| {n} | {m:,} kg | {h} m | {m*g0*h:,.0f} J ({m*g0*h/3.6e6:.4f} kWh) |\n" for n, m, h in [('Book on a shelf', 1, 2), ('Person climbing a floor', 70, 3), ('Water in a rooftop tank', 1000, 15), ('Lift car with passengers', 1500, 30), ('Water behind a 100 m dam (1 m³)', 1000, 100)]) + '''
## Hydroelectric power

Hydro plants turn water's potential energy into electricity:

<p class="formula">P = ρ × g × Q × h × η</p>

with Q the flow in m³/s, h the head in metres and η the efficiency (often 0.85–0.9). A flow of 10 m³/s through a 50 m head at 88% efficiency gives about **4.3 MW**.

## Pumped storage

Pumped-storage hydro stores energy by pumping water uphill when electricity is cheap and releasing it through turbines when demand is high. 1 m³ of water raised 100 m stores only about 0.27 kWh, so these schemes move very large volumes.

## Elastic potential energy

Springs store energy too: E = ½ × k × x², where k is the spring constant and x the stretch or compression. A spring with k = 2,000 N/m compressed by 5 cm stores 2.5 J.
''', [
 ('What is the formula for potential energy?', 'PE = m × g × h: mass × gravitational acceleration (9.81 m/s²) × height.'),
 ('How much energy is needed to lift 1 kg by 1 m?', 'About 9.81 joules.'),
], before='## Energy conservation')

expand('physics/pressure', '''
## Pressure examples

| Situation | Force | Area | Pressure |
|---|---|---|---|
| Person standing (two feet) | 700 N | 400 cm² | 17.5 kPa |
| Person on one stiletto heel | 700 N | 1 cm² | 7,000 kPa |
| Elephant (four feet) | 50,000 N | 4,000 cm² | 125 kPa |
| Car tyre contact (each) | 3,000 N | 150 cm² | 200 kPa |
| Drawing pin point | 20 N | 0.0001 cm² | 2,000,000 kPa |

Small areas create huge pressures, which is why knives cut and pins pierce, and why snowshoes stop you sinking.

## Pressure in fluids

In a liquid, pressure increases with depth:

<p class="formula">P = ρ × g × h</p>

10 m of water adds about 98 kPa — roughly one atmosphere. See the [hydrostatic pressure calculator](/engineering/hydrostatic-pressure/).

## Hydraulics

Pressure applied to an enclosed liquid is transmitted equally (Pascal's principle). A small force on a small piston creates a large force on a large piston. Car brakes, jacks and excavators use this. See the [hydraulic cylinder force calculator](/engineering/hydraulic-cylinder-force/).

## Gauge vs absolute

Most gauges read pressure above atmospheric (gauge pressure). Add about 101.3 kPa to get absolute pressure at sea level.
''', [
 ('What is the SI unit of pressure?', 'The pascal (Pa), equal to one newton per square metre.'),
 ('How do I convert kPa to psi?', 'Divide by 6.895. 200 kPa is about 29 psi. Use the pressure converter for other units.'),
], before='## Units')

expand('physics/projectile-motion', '''
## Projectile from a height

If launched from height h₀ above the landing point, the time of flight becomes:

<p class="formula">t = [v sin θ + √((v sin θ)² + 2 g h₀)] ÷ g</p>

and the range is v cos θ × t. From a height, the best angle for maximum range is **less than 45°**.

## Real-world effects

| Effect | Result |
|---|---|
| Air resistance | Shorter range, lower peak, steeper descent |
| Spin (Magnus effect) | Backspin lifts the ball; topspin makes it dip |
| Wind | Changes range and drift |

For a well-hit golf ball or a long throw, real range can be 30–50% less than the formula predicts.

## Sports examples

- **Long jump**: athletes take off at about 18–22°, lower than 45°, because they cannot generate as much speed at steeper angles.
- **Shot put**: the best angle is about 37–40° because the shot is released above the ground.
- **Football goal kicks**: typical angles are 30–45°.

## Horizontal launch

For something thrown or rolled horizontally off a table (θ = 0), time to land is √(2h ÷ g), and range is v × √(2h ÷ g). A ball rolling off a 1 m table at 2 m/s lands 0.90 m away.
''', [
 ('Why is 45° the best angle?', 'Range depends on sin 2θ, which is largest when 2θ = 90°. This holds only on level ground without air resistance.'),
 ('Do complementary angles give the same range?', 'Yes. On level ground, 30° and 60° (or 20° and 70°) give the same range, but the steeper angle goes higher and takes longer.'),
], before='## Range at different angles (20 m/s)')

expand('physics/rc-time-constant', '''
## Charge and discharge levels

| Time | Charging (% of supply) | Discharging (% remaining) |
|---|---|---|
''' + ''.join(f"| {k}τ | {(1-math.exp(-k))*100:.1f}% | {math.exp(-k)*100:.1f}% |\n" for k in [0.5, 1, 2, 3, 4, 5]) + '''
## Voltage at any time

- Charging: V(t) = V<sub>s</sub> × (1 − e<sup>−t/τ</sup>)
- Discharging: V(t) = V<sub>0</sub> × e<sup>−t/τ</sup>

To find the time to reach a given voltage while charging: t = −τ × ln(1 − V ÷ V<sub>s</sub>).

## Applications

- **Timers and delays**: the classic 555 timer uses RC charging to set its period.
- **Filters**: RC low-pass filters remove high-frequency noise from sensor signals; the cut-off frequency is 1 ÷ (2πRC).
- **Debouncing switches**: a small RC network smooths mechanical switch bounce.
- **Power supply smoothing**: capacitors hold up the voltage between rectifier peaks.

## Safety with large capacitors

Large capacitors in power supplies can stay charged after power is removed. Always discharge them through a suitable resistor before touching, and allow at least 5τ.
''', [
 ('What is a time constant?', 'τ = R × C, the time for a charging capacitor to reach about 63.2% of the supply voltage.'),
 ('How long does a capacitor take to fully charge?', 'About 5 time constants, when it reaches 99.3% of the supply voltage.'),
], before='## Charging curve')

expand('physics/resistors-series-parallel', '''
## Two resistors in parallel: shortcut

For two resistors, the parallel value is the **product over the sum**:

<p class="formula">R = R₁ × R₂ ÷ (R₁ + R₂)</p>

100 Ω and 220 Ω in parallel = 22,000 ÷ 320 = **68.75 Ω**.

## Making a value you do not have

| Target | Combination | Result |
|---|---|---|
| 50 Ω | Two 100 Ω in parallel | 50 Ω |
| 150 Ω | 100 Ω + 47 Ω in series | 147 Ω |
| 330 Ω | 220 Ω + 100 Ω + 10 Ω in series | 330 Ω |
| 4.7 kΩ | 10 kΩ ∥ 8.2 kΩ (close) | 4.51 kΩ |

## Voltage divider

Two resistors in series divide a voltage:

<p class="formula">V<sub>out</sub> = V<sub>in</sub> × R₂ ÷ (R₁ + R₂)</p>

With 12 V, R₁ = 10 kΩ and R₂ = 4.7 kΩ, V<sub>out</sub> = **3.84 V**. Dividers are used to scale sensor and battery voltages to a microcontroller's input range. See the [voltage divider calculator](/other/voltage-divider/).

## Current in parallel branches

In parallel, current splits in inverse proportion to resistance. With 100 Ω and 220 Ω across 12 V, the branches carry 120 mA and 54.5 mA, totalling 174.5 mA.

## Colour codes

Four-band resistors: two digit bands, a multiplier and a tolerance. Brown-black-red-gold is 1, 0, ×100 = 1,000 Ω (1 kΩ) ±5%.
''', [
 ('Is the parallel resistance always smaller?', 'Yes. The total resistance of parallel resistors is always less than the smallest one.'),
 ('What is the total of 10 kΩ resistors in series?', 'In series they add: three 10 kΩ resistors make 30 kΩ.'),
], before='## Standard values (E12 series)')

expand('physics/speed-distance-time', '''
## Journey time table

| Distance | At 40 km/h | At 60 km/h | At 80 km/h | At 100 km/h |
|---|---|---|---|---|
''' + ''.join(f"| {d} km | " + ' | '.join(f"{int(d/v)} h {round(d/v%1*60):02d} min" for v in [40, 60, 80, 100]) + " |\n" for d in [10, 25, 50, 100, 200, 500]) + '''
## Average speed over several legs

Average speed is **total distance ÷ total time**, not the average of the speeds. Driving 60 km at 60 km/h (1 h) and 60 km at 120 km/h (0.5 h) gives 120 km in 1.5 h — an average of **80 km/h**, not 90.

## Relative speed

- Moving in the **same direction**: subtract speeds. A car at 100 km/h overtaking a truck at 80 km/h closes at 20 km/h.
- Moving **towards each other**: add speeds. Two trains 300 km apart at 80 and 70 km/h meet after 300 ÷ 150 = **2 hours**.

## Pace

Runners and walkers often use pace (minutes per km), which is the inverse of speed. 12 km/h = 5 min/km. See the [pace calculator](/sports/pace-calculator/).
''', [
 ('How long does it take to travel 150 km at 60 km/h?', '2.5 hours, or 2 hours 30 minutes.'),
 ('How do I find speed from distance and time?', 'Speed = distance ÷ time. 120 km in 1.5 hours is 80 km/h.'),
], before='## Keep units consistent')

expand('physics/suvat-equations', '''
## Which equation to use

Each SUVAT equation leaves out one of the five quantities:

| Equation | Missing |
|---|---|
| v = u + at | s |
| s = ½(u + v)t | a |
| s = ut + ½at² | v |
| s = vt − ½at² | u |
| v² = u² + 2as | t |

Pick the one that omits the quantity you neither know nor need. The calculator handles this automatically.

## Stopping distance table

Reaction time 1.5 s, deceleration 7 m/s² (dry road):

| Speed | Thinking distance | Braking distance | Total |
|---|---|---|---|
''' + ''.join(f"| {v} km/h | {v/3.6*1.5:.1f} m | {(v/3.6)**2/14:.1f} m | {v/3.6*1.5+(v/3.6)**2/14:.1f} m |\n" for v in [30, 50, 70, 100, 120]) + '''
On wet roads deceleration may drop to about 4–5 m/s², increasing braking distance by 40–75%.

## Vertical motion

For objects thrown upward, use a = −9.81 m/s² (taking up as positive). A ball thrown up at 15 m/s reaches a maximum height of v² ÷ 2g = **11.5 m** after 1.53 s.

## Limits

SUVAT applies only when acceleration is **constant**. For changing acceleration, such as a car with varying throttle or an object with significant air resistance, use calculus or a numerical method.
''', [
 ('What does SUVAT stand for?', 's (displacement), u (initial velocity), v (final velocity), a (acceleration) and t (time).'),
 ('How do I find acceleration from distance and time?', 'If starting from rest, a = 2s ÷ t². A car covering 100 m in 10 s from rest accelerates at 2 m/s².'),
], before='## Sign convention')

expand('physics/wavelength-frequency', '''
## Radio and wireless frequencies

| Use | Frequency | Wavelength |
|---|---|---|
''' + ''.join(f"| {n} | {fs} | {299792458/fv:.3g} m |\n" for n, fs, fv in [('AM radio', '1 MHz', 1e6), ('FM radio', '100 MHz', 1e8), ('Mobile (4G band)', '1.8 GHz', 1.8e9), ('Wi-Fi 2.4 GHz', '2.4 GHz', 2.4e9), ('Microwave oven', '2.45 GHz', 2.45e9), ('Wi-Fi 5 GHz', '5 GHz', 5e9), ('5G mmWave', '28 GHz', 28e9)]) + '''
A quarter-wave antenna for 2.4 GHz Wi-Fi is about 3.1 cm long — a quarter of the 12.5 cm wavelength.

## Sound waves

For sound, use the speed of sound instead of light:

| Medium | Speed of sound |
|---|---|
| Air, 20 °C | 343 m/s |
| Water | about 1,480 m/s |
| Steel | about 5,900 m/s |

Middle A (440 Hz) in air has a wavelength of 343 ÷ 440 = **0.78 m**.

## Photon energy

The energy of a photon is E = h × f, where h = 6.626 × 10<sup>−34</sup> J·s. Higher frequency means more energy — which is why ultraviolet can damage skin and X-rays can pass through tissue.

## Visible light

| Colour | Wavelength |
|---|---|
| Violet | 380–450 nm |
| Blue | 450–495 nm |
| Green | 495–570 nm |
| Yellow | 570–590 nm |
| Orange | 590–620 nm |
| Red | 620–750 nm |
''', [
 ('What is the wavelength of 100 MHz?', 'About 3 metres.'),
 ('How are frequency and wavelength related?', 'They are inversely proportional: wavelength = speed ÷ frequency. Double the frequency and the wavelength halves.'),
], before='## The electromagnetic spectrum')

expand('physics/weight', '''
## Your weight on other worlds

For a 70 kg person:

| Body | Gravity (m/s²) | Weight (N) | Feels like (kg on Earth) |
|---|---|---|---|
''' + ''.join(f"| {n} | {gg} | {70*gg:.0f} | {70*gg/g0:.1f} |\n" for n, gg in [('Moon', 1.62), ('Mercury', 3.70), ('Mars', 3.71), ('Venus', 8.87), ('Earth', 9.81), ('Uranus', 8.69), ('Neptune', 11.15), ('Saturn', 10.44), ('Jupiter', 24.79), ('Sun (surface)', 274)]) + '''
Values for the gas giants are at the cloud tops; there is no solid surface to stand on.

## Mass vs weight

| | Mass | Weight |
|---|---|---|
| What it is | Amount of matter | Force of gravity on that matter |
| Unit | kilogram (kg) | newton (N) |
| Changes with location? | No | Yes |
| Measured by | Balance | Spring scale |

Bathroom scales measure force but display it as kilograms by assuming Earth's gravity.

## Weightlessness

Astronauts on the International Space Station are not beyond gravity — at about 400 km up, gravity is still around 90% of Earth's. They feel weightless because they are in continuous free fall around the planet.
''', [
 ('How much would I weigh on the Moon?', 'About one-sixth of your Earth weight. A 70 kg person would feel like 11.6 kg.'),
 ('Is weight measured in kg or N?', 'Strictly, weight is a force measured in newtons. In everyday language, “weight” in kg means mass.'),
], before='## Gravity on Earth varies slightly')

expand('physics/work-and-power', '''
## Human power output

| Activity | Typical power |
|---|---|
| Sitting at rest | about 100 W (body heat) |
| Walking | 250–350 W total metabolic |
| Climbing stairs briskly | 300–500 W useful |
| Cycling, recreational | 75–150 W at the pedals |
| Trained cyclist, 1 hour | 250–400 W |
| Sprint (seconds) | 1,000–2,000 W |

## Work done against gravity

Lifting an object at constant speed: W = m × g × h. Lifting a 20 kg box onto a 1.5 m shelf takes 20 × 9.81 × 1.5 = **294 J**. Done in 2 seconds, that is 147 W.

## Efficiency

No machine converts all its input energy into useful work:

<p class="formula">Efficiency = useful output ÷ total input × 100%</p>

| Machine | Typical efficiency |
|---|---|
| Large electric motor | 90–97% |
| Car petrol engine | 20–35% |
| Human muscle | about 20–25% |
| LED lighting | 30–50% (light vs heat) |

## Work at an angle

If the force is at an angle θ to the movement, only the part along the movement does work: W = F × d × cos θ. Pulling a suitcase with 100 N at 30° over 50 m does 100 × 50 × 0.866 = **4,330 J** of work.
''', [
 ('What is the unit of work?', 'The joule (J): 1 newton of force moving 1 metre.'),
 ('What is the difference between work and power?', 'Work is energy transferred. Power is how fast it is transferred: power = work ÷ time.'),
], before='## Climbing stairs')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/physics/*.mdx')):
    c = 'physics/' + os.path.basename(p)[:-4]; print(c, words(c))
