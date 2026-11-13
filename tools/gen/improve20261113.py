"""Improve pass (2026-11-13) for thin physics pages from the first batches (2026-10-27/29):
physics/angular-velocity, physics/friction-force, physics/impulse.
Keyword-first titles, 120-160 char descriptions, intros with the "<topic> calculator" phrase,
worked examples and reference tables computed here, practical notes, re-checked FAQs and related links.
No instrumentationblog.in links are added. Slugs, categories and existing variable ids are unchanged
(asserted); a few output variables are added. Re-running regenerates the same files."""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from page import page, BASE
U = '2026-11-13'
DONE = []
pi = math.pi
g0 = 9.80665

def ids_of(cid):
    fm = open(os.path.join(BASE, cid + '.mdx')).read().split('---')[1]
    d = yaml.safe_load(fm); return [v['id'] for v in d['variables']], d['category'], d.get('featured')

def W(cid, fm, body):
    cat, slug = cid.split('/')
    old_ids, old_cat, old_feat = ids_of(cid)
    assert not old_feat, cid
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (cid, len(d))
    assert 'featured' not in fm
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    page(cat, slug, fm, body)
    new_ids, new_cat, _ = ids_of(cid)
    assert new_cat == old_cat == cat, cid
    assert all(i in new_ids for i in old_ids), (cid, old_ids, new_ids)
    DONE.append(cid)

# ---------------------------------------------------------------- Angular velocity
aN, ar = 1450.0, 0.1
aw = 2 * pi * aN / 60; af = aN / 60; av = aw * ar; aT = 1 / af
ac_rows = ''.join(f"| {N:,} rpm | {2*pi*N/60:,.2f} rad/s | {N/60:,.2f} Hz | {360*N/60:,.0f} °/s | {60/N*1000:,.2f} ms |\n"
                  for N in (1, 10, 60, 100, 500, 750, 1000, 1450, 1500, 2900, 3000, 3600, 10000))
av_rows = ''
for Dmm in (50, 100, 150, 200, 300, 500, 1000):
    av_rows += f"| {Dmm} mm | " + ' | '.join(f"{pi*Dmm/1000*N/60:,.2f}" for N in (500, 1000, 1450, 1500, 2900, 3000)) + " |\n"
ms_rows = ''
for poles in (2, 4, 6, 8, 10, 12):
    n50 = 120 * 50 / poles; n60 = 120 * 60 / poles
    ms_rows += f"| {poles} | {n50:,.0f} rpm ({2*pi*n50/60:,.1f} rad/s) | {n60:,.0f} rpm ({2*pi*n60/60:,.1f} rad/s) |\n"
W('physics/angular-velocity', f'''
title: Angular Velocity Calculator (rpm to rad/s & Rim Speed)
description: Convert rpm to rad/s, Hz and degrees per second, and calculate the tangential (rim) speed at any radius for motors, wheels, pulleys and rotating shafts.
category: physics
intro: "Rotating machines are rated in revolutions per minute, but physics and engineering formulas use angular velocity in radians per second. This angular velocity calculator converts between rpm, rad/s and Hz, gives the time per revolution and works out the tangential speed at any radius, v = ωr — handy for motor shafts, wheels, grinding discs, fans and pulleys."
keywords: [angular velocity calculator, rpm to rad/s, rad/s to rpm, tangential velocity calculator, rpm to linear speed, rotational speed converter, angular speed formula, rim speed calculator]
updated: {U}
variables:
  - {{ id: N, label: Rotational speed, suffix: rpm, default: {aN:g}, min: 0 }}
  - {{ id: r, label: Radius, family: length, unit: mm, imperialUnit: in, default: {ar*1000:g}, min: 0 }}
  - {{ id: w, label: Angular velocity (ω), suffix: rad/s, min: 0 }}
  - {{ id: f, label: Rotational frequency, family: frequency, unit: Hz, min: 0 }}
  - {{ id: v, label: Tangential (rim) speed, family: velocity, unit: ms, imperialUnit: fts, min: 0 }}
  - {{ id: T, label: Time per revolution, family: seconds, unit: ms, min: 0 }}
  - {{ id: wd, label: Angular velocity in degrees per second, suffix: °/s, min: 0, decimals: 1 }}
equations:
  - w = 2 * pi * N / 60
  - f = N / 60
  - v = w * r
  - T = 1 / f
  - wd = 360 * N / 60
faq:
  - q: How do I convert rpm to rad/s?
    a: Multiply by 2π and divide by 60, so ω = rpm × 0.10472. 1,450 rpm is {aw:.2f} rad/s. To go back, rpm = rad/s × 60 ÷ 2π = rad/s × 9.549.
  - q: How do I find linear speed from rpm?
    a: v = ω × r = π × D × rpm ÷ 60. A 200 mm diameter disc at 1,450 rpm has a rim speed of π × 0.2 × 1,450 ÷ 60 = {av:.2f} m/s.
  - q: What is the difference between angular velocity and frequency?
    a: Frequency counts revolutions per second (Hz); angular velocity counts radians per second. One revolution is 2π radians, so ω = 2πf — 50 revolutions per second is 314.16 rad/s.
  - q: Why does rim speed matter?
    a: Grinding wheels, saw blades and fans have a maximum safe peripheral speed marked on them, belt and conveyor speeds are set by the pulley rim speed, and cutting speeds in machining are specified as surface speed at the tool or workpiece diameter.
related: [engineering/pulley-speed, physics/centripetal-force, physics/rotational-kinetic-energy, engineering/torque-power-speed, engineering/gear-ratio, electrical/induction-motor-slip]
''', f'''
## How to use the angular velocity calculator

Enter the **speed in rpm** and a **radius**. You get the angular velocity in rad/s and degrees per second, the rotational frequency in Hz, the tangential speed at that radius and the time for one revolution. Every field can be the unknown — enter rad/s or a rim speed instead and clear rpm to convert the other way, or enter a rim speed and rpm to find the radius.

## Angular velocity formulas

<p class="formula">ω = 2π × N ÷ 60 &nbsp;·&nbsp; f = N ÷ 60 &nbsp;·&nbsp; v = ω × r = π D N ÷ 60 &nbsp;·&nbsp; T = 1 ÷ f</p>

N is the speed in rpm, ω the angular velocity in rad/s, r the radius and D the diameter. Angular velocity is the same everywhere on a rigid rotating body; the tangential speed grows in proportion to the distance from the axis.

## Worked example

A 4-pole motor at {aN:,.0f} rpm driving a 200 mm diameter disc (r = {ar*1000:g} mm):

- ω = 2π × {aN:,.0f} ÷ 60 = **{aw:.2f} rad/s** ({360*aN/60:,.0f} °/s)
- f = {aN:,.0f} ÷ 60 = **{af:.2f} Hz**, so one turn takes **{aT*1000:.2f} ms**
- Rim speed v = {aw:.2f} × {ar:g} = **{av:.2f} m/s** ({av*3.6:.1f} km/h)

## rpm to rad/s conversion table

| Speed | Angular velocity | Frequency | Degrees per second | Time per revolution |
|---|---|---|---|---|
{ac_rows}
## Rim speed by diameter and rpm (m/s)

| Diameter | 500 rpm | 1,000 rpm | 1,450 rpm | 1,500 rpm | 2,900 rpm | 3,000 rpm |
|---|---|---|---|---|---|---|
{av_rows}
## Synchronous speed of AC motors

N<sub>s</sub> = 120 f ÷ poles; induction motors run a few percent slower (for example 1,450 rpm instead of 1,500 rpm):

| Poles | 50 Hz | 60 Hz |
|---|---|---|
{ms_rows}
## Practical notes

- **Gears and belts** keep the rim speed equal on both sides of a belt or at the pitch circle of a gear mesh, so the angular velocities are in the inverse ratio of the diameters — see the [pulley speed calculator](/engineering/pulley-speed/) and the [gear ratio calculator](/engineering/gear-ratio/).
- **Power and torque:** P = T × ω, so a 15 kW motor at {aw:.2f} rad/s delivers {15000/aw:.1f} N·m — use the [torque, power and speed calculator](/engineering/torque-power-speed/).
- **Centripetal acceleration** at the rim is a = ω² r ({aw**2*ar:,.0f} m/s², about {aw**2*ar/g0:,.0f} g, in the example), which sets the stress in rotating discs and the force on any unbalance; see the [centripetal force calculator](/physics/centripetal-force/).
''')

# ---------------------------------------------------------------- Friction force
fmu, fm = 0.4, 10.0
fN = fm * g0; fF = fmu * fN; fth = math.degrees(math.atan(fmu)); fa = fmu * g0
COEF = (('Steel on steel (dry)', 0.74, 0.57), ('Aluminium on steel', 0.61, 0.47), ('Copper on steel', 0.53, 0.36),
        ('Rubber tyre on dry concrete', 1.0, 0.8), ('Rubber tyre on wet concrete', 0.7, 0.5), ('Wood on wood', 0.4, 0.2),
        ('Glass on glass', 0.94, 0.4), ('Steel on steel (lubricated)', 0.16, 0.08), ('Waxed ski on snow', 0.14, 0.1),
        ('PTFE on steel', 0.04, 0.04), ('Ice on ice', 0.1, 0.03))
fc_rows = ''.join(f"| {nm} | {s:g} | {k:g} | {math.degrees(math.atan(s)):.1f}° |\n" for nm, s, k in COEF)
ff_rows = ''
for m in (1, 5, 10, 25, 50, 100, 500, 1000):
    ff_rows += f"| {m:,} kg ({m*g0:,.1f} N) | " + ' | '.join(f"{mu*m*g0:,.1f} N" for mu in (0.05, 0.1, 0.2, 0.4, 0.6, 0.8)) + " |\n"
fmeas_F, fmeas_m = 147.1, 25.0
fmeas_mu = fmeas_F / (fmeas_m * g0)
W('physics/friction-force', f'''
title: Friction Force Calculator (F = μN, Coefficient of Friction)
description: Calculate friction force from the coefficient of friction and the normal force or mass, find μ from a measured force, and get the angle of repose.
category: physics
intro: "Friction opposes sliding between two surfaces and is proportional to how hard they are pressed together. This friction force calculator uses F = μN to find the friction force, the normal force or the coefficient of friction for an object on a level surface or under any known normal force, and also gives the angle of repose and the deceleration of an object sliding to a stop."
keywords: [friction force calculator, coefficient of friction calculator, static friction calculator, kinetic friction formula, normal force friction, friction coefficient table, angle of repose calculator, how to calculate friction force]
updated: {U}
variables:
  - {{ id: mu, label: Coefficient of friction (μ), default: {fmu:g}, min: 0 }}
  - {{ id: m, label: Mass (on a level surface), family: mass, unit: kg, imperialUnit: lb, default: {fm:g}, min: 0 }}
  - {{ id: N, label: Normal force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: Ff, label: Friction force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: th, label: Angle of repose (slope at which sliding starts), family: angle, unit: deg, min: 0 }}
  - {{ id: ad, label: Deceleration when sliding on a level surface (μ × g), suffix: m/s², min: 0, decimals: 3 }}
equations:
  - N = m * g0
  - Ff = mu * N
  - th = atan(mu)
  - ad = mu * g0
faq:
  - q: What is the formula for friction force?
    a: F = μ × N, where μ is the coefficient of friction and N the normal force pressing the surfaces together. On a level surface N = m × g, so a 10 kg crate with μ = 0.4 needs {fF:.2f} N to slide.
  - q: What is the difference between static and kinetic friction?
    a: Static friction is the maximum force the contact can resist before an object starts to slide; kinetic friction acts while it is sliding and is usually 20–50% lower. That is why it takes more force to start pushing a box than to keep it moving.
  - q: Does friction depend on contact area?
    a: For dry, rigid surfaces, no — the classical (Amontons–Coulomb) law says friction depends only on μ and the normal force. Tyres, rubber seals and soft materials deviate from this, and lubricated contacts also depend on speed and viscosity.
  - q: How do I find the coefficient of friction?
    a: Pull the object at a steady speed with a spring balance or force gauge and divide the force by the normal force, μ = F ÷ N — or tilt the surface until the object just starts to slide; then μ_s = tan θ. Enter the force and mass and clear μ to let the calculator do it.
related: [physics/inclined-plane, physics/force, physics/weight, physics/work-and-power, engineering/bolt-torque]
''', f'''
## How to use the friction force calculator

Enter the **coefficient of friction** and the **mass** of an object on a level surface — the normal force N = mg is calculated for you — and you get the friction force, the angle of repose and the deceleration of the object if it slides freely to a stop. For a sloped surface or an extra pressing force, clear the mass and enter the **normal force** directly, or use the [inclined plane calculator](/physics/inclined-plane/). To find μ, enter the measured friction force and the mass and clear the coefficient.

## Friction formula

<p class="formula">F<sub>f</sub> = μ × N &nbsp;·&nbsp; N = m × g (level surface) &nbsp;·&nbsp; θ<sub>repose</sub> = arctan μ<sub>s</sub> &nbsp;·&nbsp; a = μ<sub>k</sub> × g</p>

Use the static coefficient μ<sub>s</sub> for the force needed to start an object moving and the kinetic coefficient μ<sub>k</sub> for the force needed to keep it moving. g = 9.80665 m/s².

## Worked example

A {fm:g} kg crate on a floor with μ = {fmu:g}:

- Normal force N = {fm:g} × 9.80665 = **{fN:.2f} N**
- Friction force F<sub>f</sub> = {fmu:g} × {fN:.2f} = **{fF:.2f} N** — the force needed to keep it sliding
- Angle of repose θ = arctan {fmu:g} = **{fth:.2f}°** — a ramp steeper than this lets the crate slide on its own
- If pushed and released, it decelerates at {fmu:g} × 9.80665 = **{fa:.3f} m/s²**

**Finding μ:** a force gauge reads {fmeas_F:g} N while dragging a {fmeas_m:g} kg box at a steady speed, so μ<sub>k</sub> = {fmeas_F:g} ÷ ({fmeas_m:g} × 9.80665) = **{fmeas_mu:.3f}**.

## Typical coefficients of friction (approximate)

| Surfaces | Static μ<sub>s</sub> | Kinetic μ<sub>k</sub> | Angle of repose |
|---|---|---|---|
{fc_rows}
Values vary widely with surface finish, contamination and lubrication — use measured values for design.

## Friction force by mass and coefficient (level surface)

| Mass (weight) | μ = 0.05 | μ = 0.1 | μ = 0.2 | μ = 0.4 | μ = 0.6 | μ = 0.8 |
|---|---|---|---|---|---|---|
{ff_rows}
## Practical notes

- **Rolling is much easier than sliding:** the rolling resistance coefficient of a steel wheel on a rail is about 0.001 and a car tyre on asphalt about 0.01, compared with 0.3–0.8 for sliding.
- **Stopping distance:** an object sliding at speed v stops in v² ÷ (2 μ g) — a car at 50 km/h (13.9 m/s) with locked wheels on dry concrete (μ ≈ 0.8) needs about {13.889**2/(2*0.8*g0):.1f} m.
- **Bolted joints:** friction under the nut and in the threads absorbs about 90% of the tightening torque, which is why the friction factor matters so much in the [bolt torque calculator](/engineering/bolt-torque/).
- To include the work done against friction over a distance, use the [work and power calculator](/physics/work-and-power/).
''')

# ---------------------------------------------------------------- Impulse
iF, it, im = 500.0, 0.1, 2.0
iJ = iF * it; idv = iJ / im; iag = idv / it / g0
st_rows = ''
for t in (0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0):
    F = 70 * 15 / t
    st_rows += f"| {t:g} s | {F:,.0f} N | {F/(70*g0):,.1f} g |\n"
SP = (('Golf ball struck by a driver', 0.0459, 70, 0.0005), ('Football (soccer) kick', 0.43, 25, 0.009),
      ('Tennis serve', 0.058, 50, 0.005), ('Baseball hit by a bat', 0.145, 45, 0.0007), ('Cricket ball hit by a bat', 0.16, 40, 0.001))
sp_rows = ''.join(f"| {nm} | {m*1000:g} g | {v:g} m/s | {t*1000:g} ms | {m*v:.2f} N·s | {m*v/t:,.0f} N |\n" for nm, m, v, t in SP)
W('physics/impulse', f'''
title: Impulse Calculator (Impulse–Momentum Theorem)
description: Calculate impulse from force and contact time, and the change in velocity or momentum it causes, with J = F·Δt = m·Δv, average force and deceleration in g.
category: physics
intro: "Impulse is the product of a force and the time it acts, and it equals the change in an object's momentum. This impulse calculator applies the impulse–momentum theorem to find the impulse, the change in velocity, the average force or the contact time, and shows the average acceleration in g — useful for collisions, kicks, drops, airbags and rocket burns."
keywords: [impulse calculator, impulse momentum theorem, impulse formula, change in momentum calculator, force time calculator, impulse physics, average force calculator, impulse equation]
updated: {U}
variables:
  - {{ id: F, label: Average force, family: force, unit: N, imperialUnit: lbf, default: {iF:g} }}
  - {{ id: t, label: Contact time, family: seconds, unit: s, default: {it:g}, min: 0 }}
  - {{ id: m, label: Mass, family: mass, unit: kg, imperialUnit: lb, default: {im:g}, min: 0 }}
  - {{ id: J, label: Impulse (= change in momentum), suffix: N·s }}
  - {{ id: dv, label: Change in velocity, family: velocity, unit: ms, imperialUnit: fts }}
  - {{ id: ag, label: Average acceleration during the impact, suffix: g, decimals: 2 }}
equations:
  - J = F * t
  - dv = J / m
  - ag = dv / t / g0
faq:
  - q: What is the formula for impulse?
    a: J = F × Δt, the average force multiplied by the time it acts. By the impulse–momentum theorem it also equals the change in momentum, m × Δv. A 500 N force acting for 0.1 s gives an impulse of 50 N·s.
  - q: What are the units of impulse?
    a: Newton-seconds (N·s), which are the same as kg·m/s — the units of momentum. In US units impulse is given in lbf·s; 1 lbf·s = 4.448 N·s.
  - q: Why do airbags and crumple zones reduce injury?
    a: The change in momentum in a crash is fixed by the mass and speed, so stretching the stopping time lowers the average force by the same factor. Stopping a 70 kg person from 15 m/s in 0.1 s instead of 0.01 s cuts the average force from 105,000 N to 10,500 N.
  - q: How do I find the force from a change in velocity?
    a: Enter the mass, the change in velocity and the contact time, and clear the force — F = m × Δv ÷ Δt. Remember that Δv is a vector change: a ball arriving at 20 m/s and leaving at 20 m/s in the opposite direction has Δv = 40 m/s.
related: [physics/momentum, physics/force, physics/elastic-collision, physics/acceleration, physics/kinetic-energy, physics/free-fall]
''', f'''
## How to use the impulse calculator

Enter the **average force**, the **contact time** and the **mass** of the object. You get the impulse, the change in velocity it produces and the average acceleration in g. Any field can be the unknown: enter the mass, the change in velocity and the time to find the average force, or the impulse and force to find the contact time.

## Impulse formula

<p class="formula">J = F × Δt = m × Δv = Δp &nbsp;·&nbsp; F<sub>avg</sub> = m Δv ÷ Δt &nbsp;·&nbsp; a = Δv ÷ Δt</p>

F is the average force over the contact time; the peak force in a real impact is usually 1.5–2 times higher. For a force that varies with time, impulse is the area under the force–time graph.

## Worked example

A {iF:g} N average force acts on a {im:g} kg ball for {it:g} s:

- Impulse J = {iF:g} × {it:g} = **{iJ:g} N·s**
- Change in velocity Δv = {iJ:g} ÷ {im:g} = **{idv:g} m/s**
- Average acceleration = {idv:g} ÷ {it:g} = {idv/it:g} m/s² = **{iag:.2f} g**

## Same impulse, different stopping times

Stopping a 70 kg person moving at 15 m/s (Δp = 1,050 N·s):

| Stopping time | Average force | Average deceleration |
|---|---|---|
{st_rows}
## Impulse in sport (typical values)

Ball starting from rest (or with the incoming speed neglected); force is the average over the contact:

| Impact | Ball mass | Speed after impact | Contact time | Impulse | Average force |
|---|---|---|---|---|---|
{sp_rows}
## Practical notes

- **Bounces double the impulse:** impulse and momentum are vectors, so a ball that rebounds at the same speed has a change in velocity of twice its speed.
- **Drop tests:** an object dropped from height h hits the ground at √(2gh) — use the [free fall calculator](/physics/free-fall/) for the speed, then this calculator with the measured stopping time for the force.
- **Rockets:** total impulse (N·s) is the standard rating of a rocket motor; the change in velocity is the total impulse divided by the mass, ignoring gravity and the mass of propellant burnt.
- For the momentum of a moving object, use the [momentum calculator](/physics/momentum/); for collisions between two bodies, use the [elastic collision calculator](/physics/elastic-collision/).
''')

print(len(DONE), 'improved:', ' '.join(DONE))
