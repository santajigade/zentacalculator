"""Part C expansion (2026-11-25): 30 pages from the top of tools/upgrade-backlog.txt (priority list empty; featured pages skipped). Assembled from six sections; edits applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-25), section c1: centripetal-force, potential-energy, free-fall, suvat-equations, orbital-period.
Every number is computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-25'
G = 9.80665
GRAV = 6.6743e-11


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Centripetal force
m, v_kmh, r = 1200, 60, 50
v = v_kmh / 3.6
ac = v ** 2 / r
F = m * ac
assert abs(ac - 5.5556) < 1e-3 and abs(F / 1000 - 6.6667) < 1e-3
ac_g = ac / G
W = m * G
omega = v / r
t_circle = 2 * math.pi * r / v
t_quarter = t_circle / 4
bank = math.degrees(math.atan(v ** 2 / (r * G)))
# vertical loop, radius 10 m, rider 60 kg
rl, mr = 10.0, 60.0
v_top = math.sqrt(G * rl)
v_bot = math.sqrt(5 * G * rl)
N_bot = mr * (G + v_bot ** 2 / rl)
assert abs(N_bot / (mr * G) - 6) < 1e-9
# radius needed to hold lateral acceleration to 0.2 g and 0.4 g
rad_rows = ''
for sp in (40, 60, 80, 100, 120):
    vs = sp / 3.6
    rad_rows += f"| {sp} km/h | {vs:.2f} m/s | {vs**2/(0.2*G):,.0f} m | {vs**2/(0.4*G):,.0f} m |\n"
# whirling bung lab: 20 g bung, 0.80 m string, 2.0 s per rev, hanging mass
mb, Lb, Tb = 0.020, 0.80, 2.0
Fb = mb * 4 * math.pi ** 2 * Lb / Tb ** 2
m_hang = Fb / G
# if speed is entered as m/s by mistake (60 m/s)
F_wrong = m * 60 ** 2 / r

edit('physics/centripetal-force', date=U, phrase='centripetal force calculator',
     intro=("Centripetal force is the inward pull that keeps any object moving along a circle, supplied by friction, tension, gravity or a normal force. "
            "This centripetal force calculator finds the centripetal acceleration and force from mass, speed and the radius of the path.\n\n"
            "Students use it for circular motion problems, while drivers, road designers and ride engineers use it to judge how much grip or structural load a turn demands at a given speed."),
     replace=[('''- F = 1,200 × 5.56 = **6.67 kN**''',
               f'''- F = 1,200 × {ac:.4f} = **{F/1000:.2f} kN**

### What that means for the tyres

The car weighs m g = 1,200 × 9.80665 = {W:,.0f} N, so the {F:,.0f} N sideways force is {ac_g:.3f} of its weight. The tyres therefore need a friction coefficient of at least μ = v² ÷ (r g) = **{ac_g:.3f}** just to hold the line, which dry asphalt can manage but a wet or icy road may not. The car turns at ω = v ÷ r = {omega:.3f} rad/s, so it would take {t_circle:.2f} s to drive a full circle and {t_quarter:.2f} s to get round a 90° corner. A road banked at atan({ac_g:.3f}) = **{bank:.1f}°** would supply the whole force with no friction at all, which is far steeper than public roads are built.''')],
     before='## Banked curves',
     body_add=f'''## Radius needed for a comfortable turn

Highway designers keep the lateral acceleration low so that passengers stay comfortable and tyres keep a large grip margin. Rearranging r = v² ÷ a gives the smallest radius for each speed:

| Design speed | Speed in m/s | Radius for 0.2 g | Radius for 0.4 g |
|---|---|---|---|
{rad_rows}
The radius grows with the square of the speed, so a bend designed for 120 km/h needs four times the radius of one designed for 60 km/h.

## Vertical loops and apparent weight

On a roller coaster loop the track and gravity share the job. At the top of a {rl:.0f} m radius loop, gravity alone provides the centripetal force when v = √(g r) = **{v_top:.2f} m/s**; any slower and the car would leave the track without its upstop wheels. If the car only just makes the top, energy conservation gives v = √(5 g r) = {v_bot:.2f} m/s at the bottom, where the seat must push up with m (g + v² ÷ r). For a {mr:.0f} kg rider that is {N_bot:,.0f} N, six times body weight, which is why real loops use a clothoid (teardrop) shape with a tighter radius at the top.

''', min_words=0)

edit('physics/centripetal-force', date=U, phrase='centripetal force calculator',
     body_add=f'''
## Measuring centripetal force in practice

In a classroom the usual method is the whirling bung: a rubber bung on a string passes through a glass tube, and a hanging mass at the bottom provides the tension. A {mb*1000:.0f} g bung whirled on {Lb:.2f} m of string at one revolution every {Tb:.1f} s needs F = m 4π² r ÷ T² = {Fb:.3f} N, which a hanging mass of {m_hang*1000:.1f} g supplies. In cars, the lateral accelerometer in a data logger or phone reads ac directly, and multiplying by the vehicle mass gives the force the tyres carry. Centrifuges are specified by relative centrifugal force, which is ac divided by g.

## Common mistakes

- **Entering speed in the wrong unit.** Typing 60 m/s when the car does 60 km/h makes the force {F_wrong/1000:.1f} kN instead of {F/1000:.2f} kN, almost thirteen times too large, because the error is squared.
- **Using the diameter.** The formula needs the radius; using a 100 m diameter as r halves the computed force.
- **Drawing centripetal force as an extra force.** It is the net inward result of real forces such as friction or tension, so it must not appear as a separate arrow on a free body diagram.
- **Assuming force scales with speed.** It scales with speed squared; a 20% faster entry speed needs 44% more grip.
- **Confusing ac with g force felt.** On a flat road the occupants feel ac sideways, but on a loop or a hump the seat force also includes gravity.
''',
     faq_add=[('What friction coefficient does a car need to take a bend?',
               f'At least μ = v² ÷ (r g). For 60 km/h on a 50 m radius that is {ac_g:.3f}. Dry asphalt typically offers 0.7 or more, so there is a margin; on ice, with μ near 0.1, the safe speed would be only about {math.sqrt(0.1*G*r)*3.6:.0f} km/h.'),
              ('What is the minimum speed at the top of a vertical loop?',
               f'The speed at which gravity alone supplies the centripetal force, v = √(g r). For a 10 m radius loop that is {v_top:.2f} m/s, about {v_top*3.6:.1f} km/h.')])

# ---------------------------------------------------------------- Potential energy
m, h = 1000, 50
PE = m * G * h
assert abs(PE / 1000 - 490.3325) < 1e-6
kwh = PE / 3.6e6
v_bot = math.sqrt(2 * G * h)
eta = 0.88
kwh_el = kwh * eta
h_1kwh = 3.6e6 / (m * G)
# per unit mass and per metre
e_per_m = m * G
# other worlds
worlds = [('Earth (standard)', G), ('Earth at the equator', 9.780), ('Earth at the poles', 9.832),
          ('Moon', 1.62), ('Mars', 3.71), ('Jupiter', 24.79)]
w_rows = ''
for nm, gg in worlds:
    w_rows += f"| {nm} | {gg:g} m/s² | {m*gg*h/1000:,.1f} kJ |\n"
# mgh versus exact GM m (1/R - 1/(R+h)) at 400 km, using g = GM/R^2 consistently
GM, R = 3.986004e14, 6.371e6
hh = 400e3
ratio = R / (R + hh)
# lift motor: 1000 kg raised 50 m in 40 s at 70% efficiency
t_lift, eta_l = 40, 0.70
P_mech = PE / t_lift
P_elec = P_mech / eta_l
# centre of mass error: 2 m tall crate counted from top
dPE_com = m * G * 1.0

edit('physics/potential-energy', date=U, phrase='potential energy calculator',
     intro=("Gravitational potential energy is the energy a mass gains when it is raised against gravity, equal to mass times g times the height gained. "
            "This potential energy calculator gives PE = m g h in joules, kilojoules or kilowatt hours, or the height needed for a chosen energy.\n\n"
            "Students use it for energy conservation problems, and engineers use it to size lifts, cranes, hoists and pumped storage or small hydro schemes."),
     replace=[('''PE = 1,000 × 9.81 × 50 = **490 kJ** = 0.136 kWh''',
               f'''PE = 1,000 × 9.80665 × 50 = {c(PE)} J = **{PE/1000:.1f} kJ** = {kwh:.4f} kWh

Each metre of height adds m g = {c(e_per_m)} J for this tonne of water. Released through a turbine and generator with {eta*100:.0f}% overall efficiency, the {kwh:.4f} kWh becomes about {kwh_el:.3f} kWh of electricity. Dropped freely, the same water would hit the bottom at √(2 g h) = {v_bot:.2f} m/s, because all of the {PE/1000:.1f} kJ has turned into kinetic energy.

### How high for one kilowatt hour?

Turning the formula round, h = PE ÷ (m g). To store 1 kWh (3.6 MJ) in one tonne you must lift it 3,600,000 ÷ (1,000 × 9.80665) = **{h_1kwh:.1f} m**. That is why gravity storage needs very large masses or very large height differences.''')],
     before='## Potential energy examples',
     body_add=f'''## Energy and power for a lift

The calculator gives energy; dividing by time gives power. Raising the default 1,000 kg through 50 m in {t_lift} s needs {PE/1000:.1f} kJ ÷ {t_lift} s = {P_mech/1000:.2f} kW of mechanical power. With a {eta_l*100:.0f}% efficient motor and gearbox the electrical demand is about {P_elec/1000:.1f} kW. Counterweights in real lifts balance the car and part of the load, so the motor only lifts the difference.

''', min_words=0)

edit('physics/potential-energy', date=U, phrase='potential energy calculator',
     body_add=f'''
## How g changes the answer

The calculator uses standard gravity, 9.80665 m/s². The same 1,000 kg raised 50 m stores:

| Location | g | Potential energy |
|---|---|---|
{w_rows}
Across Earth's surface the spread is only about half a percent, which is smaller than most height measurement errors. On the Moon the same lift takes about a sixth of the energy.

## When m g h stops being accurate

The formula assumes g is constant over the height range, which is excellent for buildings, dams and mountains. For large heights use the exact change G M m (1 ÷ R<sub>1</sub> − 1 ÷ R<sub>2</sub>). Lifting a mass to 400 km altitude, the exact value is only R ÷ (R + h) = {ratio:.3f} of m g h (taking g = G M ÷ R² at the surface), so the simple formula overstates the energy by about {(1/ratio-1)*100:.1f}%.

## Common mistakes

- **Measuring height to the wrong point.** Use the vertical rise of the centre of mass. Counting a 2 m tall, 1 tonne crate from its top instead of its middle adds {dPE_com/1000:.1f} kJ that is not really there.
- **Using the length of a slope.** Only vertical height counts; a 100 m ramp at 30° raises a load 50 m.
- **Entering grams or pounds as kilograms.** The SI formula needs kilograms, metres and m/s² to give joules.
- **Mixing kJ and kWh.** 1 kWh is 3,600 kJ, so {PE/1000:.1f} kJ is only {kwh:.3f} kWh, not 490 kWh.
- **Treating potential energy as absolute.** Only differences matter, so pick one reference level and use it for every height in the problem.
''',
     faq_add=[('Does the path taken change the potential energy?',
               'No. Gravity is a conservative force, so the change in potential energy depends only on the start and end heights. A ramp, a staircase or a straight lift to the same height all give the same m g h, although friction may make the work you do larger.'),
              ('How high must 1 tonne be lifted to store 1 kWh?',
               f'About {h_1kwh:.0f} m, because h = 3,600,000 J ÷ (1,000 kg × 9.80665 m/s²) = {h_1kwh:.1f} m.')])

# ---------------------------------------------------------------- Free fall
h = 20
t = math.sqrt(2 * h / G)
v = G * t
assert abs(h - G * t ** 2 / 2) < 1e-9 and abs(t - 2.0196) < 1e-4 and abs(v - 19.806) < 1e-3
v_kmh = v * 3.6
v_avg = h / t
last_s = h - 0.5 * G * (t - 1) ** 2
half_t = math.sqrt(2 * (h / 2) / G)
# well with sound correction: total 2.0 s, sound 343 m/s
T_tot, c_s = 2.0, 343.0
# sqrt(2h/g) + h/c = T  ->  x = sqrt(h): x^2/c + x*sqrt(2/g) - T = 0
A, B, Cq = 1 / c_s, math.sqrt(2 / G), -T_tot
x = (-B + math.sqrt(B * B - 4 * A * Cq)) / (2 * A)
h_well = x * x
h_naive = 0.5 * G * T_tot ** 2
assert abs(math.sqrt(2 * h_well / G) + h_well / c_s - T_tot) < 1e-9
# other worlds
w_rows = ''
for nm, gg in (('Moon', 1.62), ('Mars', 3.71), ('Earth', G), ('Jupiter', 24.79)):
    tt = math.sqrt(2 * h / gg)
    w_rows += f"| {nm} | {gg:g} m/s² | {tt:.2f} s | {gg*tt:.2f} m/s |\n"
t_moon = math.sqrt(2 * h / 1.62)
# packaging drop test 0.76 m
h_pk = 0.76
v_pk = math.sqrt(2 * G * h_pk)
# with g = 10
t_10 = math.sqrt(2 * h / 10)

edit('physics/free-fall', date=U, phrase='free fall calculator',
     intro=("Free fall is motion under gravity alone, starting from rest, so an object speeds up by about 9.81 m/s every second near Earth's surface. "
            "This free fall calculator links drop height, fall time and impact speed and solves for whichever two you leave blank.\n\n"
            "Students use it for kinematics homework, while engineers, safety officers and testers use it to estimate impact speeds for dropped tools, packaging drop tests and fall protection."),
     replace=[('''A stone dropped from 20 m:

- t = √(2 × 20 ÷ 9.81) = **2.02 s**
- v = 9.81 × 2.02 = **19.8 m/s** (71 km/h)''',
               f'''A stone dropped from 20 m, with g = 9.80665 m/s²:

- t = √(2 × 20 ÷ 9.80665) = **{t:.3f} s**
- v = 9.80665 × {t:.3f} = **{v:.2f} m/s** ({v_kmh:.1f} km/h)

The average speed over the drop is 20 ÷ {t:.3f} = {v_avg:.2f} m/s, exactly half the impact speed, as it must be when the speed rises steadily from zero. The stone covers only {0.5*G:.2f} m in its first second but {last_s:.2f} m in its final second. Halving the drop to 10 m does not halve the time: it still takes {half_t:.3f} s, because time grows with the square root of height.''')],
     min_words=0)

edit('physics/free-fall', date=U, phrase='free fall calculator',
     replace=[('''## Fall distances

| Time | Distance | Speed |
|---|---|---|
| 1 s | 4.9 m | 9.8 m/s |
| 2 s | 19.6 m | 19.6 m/s |
| 3 s | 44.1 m | 29.4 m/s |
| 4 s | 78.5 m | 39.2 m/s |''',
               f'''### Correcting for the sound delay

Suppose the splash is heard {T_tot:.1f} s after release. Ignoring sound, h = ½ g t² = {h_naive:.1f} m. But the total time is the fall time plus the time for sound to climb back at about {c_s:.0f} m/s, so √(2h ÷ g) + h ÷ {c_s:.0f} = {T_tot:.1f}. Solving this as a quadratic in √h gives a depth of **{h_well:.1f} m**: the stone falls for {math.sqrt(2*h_well/G):.3f} s and the sound takes {h_well/c_s:.3f} s.

## A 20 m drop on other worlds

| Body | g | Fall time | Impact speed |
|---|---|---|---|
{w_rows}
## Using free fall in practice

Packaging is tested by dropping it from set heights; a {h_pk} m drop, a common test height for small parcels, means an impact at √(2 g h) = {v_pk:.2f} m/s. Site safety teams use the same formula to show why tool lanyards matter: a spanner falling from a 20 m scaffold arrives at {v_kmh:.0f} km/h. In the laboratory, g itself is measured by timing a ball between two light gates, or by filming a drop against a scale and reading the position frame by frame.

## Common mistakes

- **Using the formulas for an object thrown down or up.** They assume a release from rest; with a starting velocity use the [SUVAT equations calculator](/physics/suvat-equations/).
- **Rounding g to 10 m/s².** That gives {t_10:.3f} s for the 20 m drop instead of {t:.3f} s, an error of about 1%.
- **Applying it to light or long falls.** A sheet of paper or a skydiver after a few seconds is dominated by drag, and the real speed is far below g t.
- **Expecting double the height to double the time.** Time scales with √h, so a 40 m drop takes only √2 times as long.
- **Forgetting that h is measured to the impact point**, not to the ground under the release point when the object lands on something higher.''')],
     faq_add=[('How long would a 20 m fall take on the Moon?',
               f'About {t_moon:.2f} s, with g = 1.62 m/s². The object would land at {1.62*t_moon:.2f} m/s, compared with {t:.2f} s and {v:.2f} m/s on Earth.'),
              ('How far does an object fall in the last second of a 20 m drop?',
               f'The drop takes {t:.3f} s, and in the first {t-1:.3f} s it falls ½ g ({t-1:.3f})² = {h-last_s:.2f} m, so it covers the remaining {last_s:.2f} m in the final second.')])

# ---------------------------------------------------------------- SUVAT
u, a, t = 5, 2, 10
v = u + a * t
s = (u + v) / 2 * t
assert v == 25 and s == 150
chk1 = u ** 2 + 2 * a * s
chk2 = v * t - 0.5 * a * t ** 2
assert chk1 == v ** 2 and chk2 == s
v_mean = s / t
s9 = u * 9 + 0.5 * a * 81
s_tenth = s - s9
assert abs(s_tenth - (u + a * (10 - 0.5))) < 1e-12
# time to reach 100 m with the same u and a: a/2 t^2 + u t - 100 = 0
t100 = (-u + math.sqrt(u ** 2 + 2 * a * 100)) / a
v100 = u + a * t100
# ball thrown up at 15 m/s from a 20 m cliff top, s = -20, a = -g
u2, s2 = 15.0, -20.0
# -g/2 t^2 + u t - s2 = 0  ->  t = (u + sqrt(u^2 + 2 g (-s2))) / g
t_hit = (u2 + math.sqrt(u2 ** 2 + 2 * G * (-s2))) / G
t_neg = (u2 - math.sqrt(u2 ** 2 + 2 * G * (-s2))) / G
v_hit = u2 - G * t_hit
assert abs(u2 * t_hit - 0.5 * G * t_hit ** 2 - s2) < 1e-9
# table for defaults
rows = ''
for tt in (0, 2, 4, 6, 8, 10):
    rows += f"| {tt} s | {u + a*tt:.0f} m/s | {u*tt + 0.5*a*tt**2:.0f} m |\n"
# 0 to 100 km/h in 8 s
vf = 100 / 3.6
a_car = vf / 8
s_car = vf / 2 * 8
# displacement vs distance: u = 10, a = -2, t = 8
u3, a3, t3 = 10, -2, 8
s3 = u3 * t3 + 0.5 * a3 * t3 ** 2
t_turn = -u3 / a3
d3 = (u3 * t_turn + 0.5 * a3 * t_turn ** 2) + abs(s3 - (u3 * t_turn + 0.5 * a3 * t_turn ** 2))
assert s3 == 16 and d3 == 34

edit('physics/suvat-equations', date=U, phrase='SUVAT equations calculator',
     intro=("The SUVAT equations describe straight line motion at constant acceleration, linking displacement s, initial velocity u, final velocity v, acceleration a and time t. "
            "This SUVAT equations calculator solves for the two unknowns once any three are entered.\n\n"
            "Physics students rely on it for mechanics exams, and driving instructors, vehicle testers and lab technicians use it for braking, acceleration and light gate measurements."),
     replace=[('''- s = 5 × 10 + ½ × 2 × 10² = **150 m**''',
               f'''- s = ½ × (5 + 25) × 10 = **{s:.0f} m** (the same as 5 × 10 + ½ × 2 × 10²)

Two quick checks confirm the pair: v² = u² + 2as gives 25 + 2 × 2 × 150 = {chk1:.0f} = 25², and s = vt − ½at² gives 250 − 100 = {chk2:.0f} m. The average velocity is {v_mean:.0f} m/s, midway between u and v. In the tenth second alone the object covers s(10) − s(9) = 150 − {s9:.0f} = **{s_tenth:.0f} m**, which also follows from u + a(n − ½) = 5 + 2 × 9.5.

### Solving for time from displacement

With the same u = 5 m/s and a = 2 m/s², when has the object gone 100 m? Rearranging s = ut + ½at² gives t² + 5t − 100 = 0, and the positive root is t = (−5 + √425) ÷ 2 = **{t100:.3f} s**, at which point v = {v100:.2f} m/s.

### Motion that reverses direction

A ball thrown up at {u2:.0f} m/s from the top of a {-s2:.0f} m cliff lands on the beach below when s = −20 m, with up positive and a = −9.80665 m/s². The quadratic −4.903t² + 15t + 20 = 0 has roots {t_neg:.3f} s and **{t_hit:.3f} s**. The negative root is the time before the throw at which a ball on the same path would have passed the beach level, so it is discarded. The ball lands at {v_hit:.2f} m/s, the minus sign showing it is moving downwards.''')],
     before='## Braking distance example',
     body_add=f'''## Motion table for the default values

| Time | Velocity | Displacement |
|---|---|---|
{rows}
Velocity rises in equal steps of 4 m/s every 2 s, while displacement grows faster and faster because the ½at² term is quadratic in time.

''', min_words=0)

edit('physics/suvat-equations', date=U, phrase='SUVAT equations calculator',
     body_add=f'''
## Using SUVAT with real measurements

Car magazines quote 0 to 100 km/h times. A car that takes 8 s has an average acceleration of {vf:.2f} ÷ 8 = {a_car:.2f} m/s² and covers ½ × {vf:.2f} × 8 = {s_car:.0f} m during the run. Real acceleration falls as the car changes gear and gains speed, so this is the constant acceleration that would give the same time. In school labs, two light gates measure u and v and a timer gives t, so a = (v − u) ÷ t can be checked against a = (v² − u²) ÷ 2s from the gate spacing.

## Common mistakes

- **Mixing up displacement and distance.** With u = 10 m/s, a = −2 m/s² and t = 8 s, s = {s3:.0f} m, but the object went {u3*t_turn+0.5*a3*t_turn**2:.0f} m forward before turning back at t = {t_turn:.0f} s, so the distance travelled is {d3:.0f} m.
- **Using SUVAT across a change in acceleration.** Split the motion into phases, for example thinking time at constant speed and braking at constant deceleration, and use the final v of one phase as the u of the next.
- **Keeping the wrong root.** A quadratic in t gives two answers; keep the one that is positive and physically follows the start of the motion.
- **Leaving speeds in km/h.** Convert to m/s (divide by 3.6) before using a in m/s².
- **Inconsistent signs.** Once up is positive, a thrown ball has a = −9.80665 m/s² on the way up and on the way down.
''',
     faq_add=[('What is the difference between displacement and distance in SUVAT?',
               f'Displacement s is the change in position along the line, with a sign. Distance counts every metre travelled. They differ only if the object reverses: with u = 10 m/s, a = −2 m/s² and t = 8 s, s = {s3:.0f} m but the distance is {d3:.0f} m.'),
              ('How do I find the time when I know s, u and a?',
               f'Solve s = ut + ½at² as a quadratic: t = (−u + √(u² + 2as)) ÷ a. With u = 5 m/s, a = 2 m/s² and s = 100 m, t = {t100:.3f} s.')])

# ---------------------------------------------------------------- Orbital period
M, a_km = 5.972e24, 6779
a_m = a_km * 1e3
GMe = GRAV * M
T = 2 * math.pi * math.sqrt(a_m ** 3 / GMe)
v = math.sqrt(GMe / a_m)
assert abs(T - 5555) < 1 and abs(v - 7668) < 1 and abs(v * 3.6 - 27605) < 2
circ = 2 * math.pi * a_km
per_day = 86400 / T
# GEO from sidereal day and from 24 h
T_sid = 86164.0905
a_geo = (GMe * T_sid ** 2 / (4 * math.pi ** 2)) ** (1 / 3) / 1e3
a_24 = (GMe * 86400 ** 2 / (4 * math.pi ** 2)) ** (1 / 3) / 1e3
# elliptical orbit: perigee 600 km, apogee 39,700 km altitude
Re = 6371
hp, ha = 600, 39700
a_el = Re + (hp + ha) / 2
T_el = 2 * math.pi * math.sqrt((a_el * 1e3) ** 3 / GMe)
rp = (Re + hp) * 1e3
ra = (Re + ha) * 1e3
v_p = math.sqrt(GMe * (2 / rp - 1 / (a_el * 1e3)))
v_a = math.sqrt(GMe * (2 / ra - 1 / (a_el * 1e3)))
# altitude entered by mistake
T_wrong = 2 * math.pi * math.sqrt((408e3) ** 3 / GMe)
# low orbits around other bodies
bodies = [('Moon', 7.342e22, 1737.4, 100), ('Mars', 6.417e23, 3389.5, 400), ('Venus', 4.867e24, 6051.8, 250),
          ('Earth', 5.972e24, 6371.0, 408)]
b_rows = ''
lo = {}
for nm, mm, rr, alt in bodies:
    aa = (rr + alt) * 1e3
    tt = 2 * math.pi * math.sqrt(aa ** 3 / (GRAV * mm))
    vv = math.sqrt(GRAV * mm / aa)
    lo[nm] = (tt, vv)
    b_rows += f"| {nm} | {alt:,} km | {c(rr+alt,1)} km | {tt/60:.1f} min | {vv:,.0f} m/s |\n"
assert abs(lo['Earth'][0] - T) < 0.5

edit('physics/orbital-period', date=U, phrase='orbital period calculator',
     intro=("An orbital period is the time a satellite, moon or planet takes to complete one orbit, and it depends only on the central mass and the orbit's size. "
            "This orbital period calculator applies Kepler's third law, T = 2π√(a³/GM), and also gives the circular orbital speed.\n\n"
            "Students, satellite enthusiasts and mission planners use it to check the ISS, GPS and geostationary orbits, moons and planets."),
     replace=[('''- v = √(GM ÷ a) = **7,668 m/s = 27,605 km/h**''',
               f'''- v = √(GM ÷ a) = **{v:,.0f} m/s = {v*3.6:,.0f} km/h**

Each lap covers 2π × 6,779 = {circ:,.0f} km, and 86,400 s ÷ {T:,.0f} s gives **{per_day:.2f} orbits per day**. Multiplying speed by period gives the same circumference, {v*T/1000:,.0f} km, which is a quick check that the two results agree.

### Working backwards to a geostationary radius

Rearranging Kepler's law gives a = (G M T² ÷ 4π²)<sup>1/3</sup>. With the sidereal day, T = 86,164 s, the radius is **{a_geo:,.0f} km**, an altitude of {a_geo-Re:,.0f} km above the mean radius (35,786 km above the equatorial radius of 6,378 km).''')],
     min_words=0)

edit('physics/orbital-period', date=U, phrase='orbital period calculator',
     body_add=f'''
## Low orbits around other bodies

Using the masses in the field help and mean radii, the period of a low circular orbit is:

| Body | Altitude | Orbit radius | Period | Speed |
|---|---|---|---|---|
{b_rows}
The Moon's low orbit is slower than Earth's mainly because its mass is 81 times smaller, while Venus, almost Earth's twin in mass and size, gives a very similar period.

## Elliptical orbits from perigee and apogee

Orbits are usually published as perigee and apogee altitudes, worked out from radar, optical or GPS tracking. The semi-major axis is the planet radius plus the average of the two: for a highly elliptical orbit at {hp} km by {ha:,} km, a = 6,371 + ({hp} + {ha:,}) ÷ 2 = {a_el:,.0f} km. Entering that gives T = {T_el/3600:.2f} h, close to half a sidereal day. The circular speed output does not apply here; the vis viva equation v = √(GM (2 ÷ r − 1 ÷ a)) gives {v_p:,.0f} m/s at perigee and only {v_a:,.0f} m/s at apogee.

## Common mistakes

- **Entering altitude instead of radius.** Typing 408 km for the ISS gives a period of {T_wrong:.0f} s, an orbit inside the Earth. Add the planet radius first.
- **Using 24 hours for geostationary orbit.** A 24 h period puts the orbit at {a_24:,.0f} km, about {a_24-a_geo:.0f} km too high; the correct period is the sidereal day of 23 h 56 min 4 s.
- **Entering the mass in Earth masses.** The field needs kilograms, so Earth is 5.972 × 10²⁴, not 1.
- **Reading the speed output for an ellipse.** It is the circular orbit speed at radius a; on an elliptical path the speed changes all the way round.
''',
     faq_add=[('How long does a low orbit around the Moon take?',
               f'About {lo["Moon"][0]/60:.0f} minutes at 100 km altitude (radius 1,837 km), at {lo["Moon"][1]:,.0f} m/s, using the Moon mass of 7.342 × 10²² kg.'),
              ('How fast is a satellite at perigee of an elliptical orbit?',
               f'Use the vis viva equation v = √(GM (2 ÷ r − 1 ÷ a)). For a {hp} km by {ha:,} km Earth orbit it gives {v_p:,.0f} m/s at perigee and {v_a:,.0f} m/s at apogee.')])

print('done')

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-25), section c2: coulombs-law, doppler-effect, torque, hookes-law, escape-velocity.
All numbers are computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-25'
G0 = 9.80665


def sci(x, d=3):
    """Format as a × 10ⁿ with Unicode superscripts."""
    if x == 0:
        return '0'
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10 ** e
    sup = str(e).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))
    return f"{m:.{d}f} × 10{sup}"


# ================================================================ Coulomb's law
K = 8.9875517862e9
QE = 1.602176634e-19
q1, q2, r = 2e-6, -3e-6, 0.10
F = K * q1 * q2 / r ** 2
E1 = K * q1 / r ** 2
Ue = K * q1 * q2 / r
assert abs(F + 5.3925) < 1e-3 and abs(E1 - 1.7975e6) < 1e2 and abs(Ue + 0.53925) < 1e-4
# distance at which the pair attracts with exactly 1 N
r1N = math.sqrt(K * abs(q1 * q2) / 1.0)
# work to pull them from 10 cm to 30 cm, and to infinity
U30 = K * q1 * q2 / 0.30
W_10_30 = U30 - Ue
W_inf = -Ue
# electrons
n1 = q1 / QE
n2 = abs(q2) / QE
# smallest sphere that can hold q in air (breakdown about 3 MV/m)
EB = 3e6
a_min_2uC = math.sqrt(K * q1 / EB)
charge_rows = ''
for lab, q in (('1 nC', 1e-9), ('10 nC', 1e-8), ('100 nC', 1e-7), ('1 µC', 1e-6), ('2 µC', 2e-6), ('10 µC', 1e-5)):
    e10 = K * q / 0.1 ** 2
    amin = math.sqrt(K * q / EB)
    charge_rows += f"| {lab} | {sci(q / QE, 2)} | {sci(e10, 2)} N/C | {amin*100:.2f} cm |\n"
# force on q2 with a third charge: +1 µC placed 5 cm beyond q2 on the line (q1 at 0, q2 at 10 cm, q3 at 15 cm)
q3 = 1e-6
F12 = K * q1 * q2 / 0.10 ** 2       # negative: q2 pulled towards q1 (towards x = 0)
F32 = K * q3 * q2 / 0.05 ** 2       # negative magnitude sign: attraction, q2 pulled towards q3 (towards +x)
# along +x: force from q1 on q2 points to -x (attraction) with size |F12|; force from q3 points to +x with size |F32|
Fnet_x = -abs(F12) + abs(F32)
assert abs(F12) < abs(F32)

edit('physics/coulombs-law', date=U, phrase="Coulomb's law calculator",
     intro=("Coulomb's law says two point charges push or pull on each other with a force proportional to the product of the charges and inversely proportional to the square of their separation. "
            "This Coulomb's law calculator returns that force, the field of the first charge and the pair's potential energy.\n\n"
            "Physics students check electrostatics problems with it, and engineers use it to estimate forces in electrostatic precipitators, sensors and static discharge problems, or to solve for a charge or spacing."),
     body_add=f'''
## Second scenario: changing the spacing

With the same +2 µC and −3 µC charges, the attraction falls to exactly 1 N at r = √(k |q₁ q₂| ÷ 1 N) = **{r1N*100:.2f} cm**. Pulling the charges from 10 cm to 30 cm apart raises the potential energy from −{abs(Ue):.4f} J to −{abs(U30):.4f} J, so you must do **{W_10_30:.4f} J** of work. Separating them completely takes **{W_inf:.4f} J**, which is the potential energy with its sign reversed.

### Adding a third charge

Forces from several charges add as vectors. Place a +1 µC charge 5 cm beyond the −3 µC charge on the same line. Charge 1 pulls the −3 µC charge back with {abs(F12):.3f} N, while the +1 µC charge, only 5 cm away, pulls it forward with k × 1 µC × 3 µC ÷ 0.05² = {abs(F32):.3f} N. The net force is **{Fnet_x:.3f} N** towards the third charge, even though its charge is half that of charge 1, because it is twice as close.

## How much charge is realistic

A +2 µC charge means {sci(n1)} electrons removed, and −3 µC means {sci(n2)} electrons added. Air breaks down at roughly 3 MV/m, so a charged sphere can only hold a charge whose surface field k q ÷ a² stays below that. The table shows the field each charge makes 10 cm away and the smallest sphere radius that can hold it in dry air without sparking:

| Charge | Electrons | Field at 10 cm | Smallest sphere radius in air |
|---|---|---|---|
{charge_rows}
So the default +2 µC needs a sphere at least {a_min_2uC*100:.1f} cm in radius. For comparison, a person charged to 10 kV by walking on carpet, with a body capacitance of about 150 pF, carries Q = C V = {150e-12*10e3*1e6:.1f} µC spread over the whole body.

## How electrostatic force is measured

Coulomb found the inverse square law in 1785 with a torsion balance, reading the twist of a fine wire as small charged spheres repelled each other. Today charge is measured with a Faraday cup connected to an electrometer, which collects the whole charge of an object and reads it as a voltage on a known capacitance. Field meters (field mills) measure the field near charged surfaces in clean rooms and powder handling plants, and the force between charges then follows from F = q E.

## Common mistakes

- **Leaving charges in microcoulombs.** Each µC is 10⁻⁶ C, so the product q₁ q₂ carries 10⁻¹²; forgetting it gives a force a million million times too large.
- **Entering the distance in centimetres as metres.** 10 cm is 0.1 m, and because r is squared, using 10 makes the force 10,000 times too small.
- **Reading the sign as a direction on an axis.** Here a negative result only means attraction; to get the direction on a diagram, decide which way each charge is pulled and add the forces as vectors.
- **Using the point charge formula for close conductors.** Charges on nearby metal objects redistribute (induction), so the real force differs from k q₁ q₂ ÷ r² when the gap is similar to the object size.
- **Measuring r from surfaces instead of centres.** For charged spheres the distance is centre to centre, which is the gap plus both radii.
''',
     faq_add=[('How many electrons make up a microcoulomb?',
               f'One microcoulomb is 10⁻⁶ ÷ 1.602 × 10⁻¹⁹ = {sci(1e-6/QE)} electrons. The default +2 µC charge is a shortage of {sci(n1)} electrons.'),
              ('How much work does it take to separate two opposite charges?',
               f'The work equals the change in potential energy. Pulling +2 µC and −3 µC from 10 cm apart to infinity takes {W_inf:.4f} J, and from 10 cm to 30 cm takes {W_10_30:.4f} J.')])

# ================================================================ Doppler effect
f, v, vo, vs = 700, 343, 0 / 3.6, 72 / 3.6
fo = f * (v + vo) / (v - vs)
sh = fo / f - 1
assert abs(fo - 743.344) < 1e-3 and abs(sh * 100 - 6.192) < 1e-3
# moving observer towards a stationary source at the same 20 m/s
fo_obs = f * (v + 20) / v
# both moving towards each other at 20 m/s
fo_both = f * (v + 20) / (v - 20)
# reverse problem: speed of a passing source from the two pitches
fa = f * v / (v - 20)
fr = f * v / (v + 20)
vs_back = v * (fa - fr) / (fa + fr)
assert abs(vs_back - 20) < 1e-9
# cold day, 0 C
v0 = 331.3
fo_cold = f * v0 / (v0 - 20)
# asymmetry table: moving source vs moving observer
asym_rows = ''
for kmh in (36, 72, 144, 288):
    u = kmh / 3.6
    fs_ = f * v / (v - u)
    fob = f * (v + u) / v
    asym_rows += f"| {kmh} km/h ({u:.0f} m/s) | {fs_:.1f} Hz | {fob:.1f} Hz | {fs_-fob:.1f} Hz |\n"
# medical ultrasound example: 5 MHz, blood 0.5 m/s, 60 degree beam angle, c = 1540 m/s
f_us, vb, ang, c_t = 5e6, 0.5, 60, 1540
df_us = 2 * f_us * vb * math.cos(math.radians(ang)) / c_t
# angle error: 60 vs 65 degrees assumed
vb_wrong = df_us * c_t / (2 * f_us * math.cos(math.radians(65)))

edit('physics/doppler-effect', date=U, phrase='Doppler effect calculator',
     intro=("The Doppler effect is the change in frequency heard when a sound source, a listener or both move relative to the air. "
            "This Doppler effect calculator gives the observed frequency for any source and observer speeds, plus the percentage shift.\n\n"
            "Students use it for wave problems, acousticians and sound engineers for passing vehicles, and instrument engineers for radar, medical ultrasound and [Doppler ultrasonic flow meters](https://www.instrumentationblog.in/transit-time-vs-doppler-ultrasonic-flow-meter/)."),
     before='## Speed of sound in air',
     body_add=f'''
## Moving observer versus moving source

With the default 700 Hz source and 343 m/s, the calculator gives **{fo:.1f} Hz** and a shift of **+{sh*100:.2f}%** for a source approaching at 72 km/h. If instead the source stands still and the listener drives towards it at 72 km/h, f′ = 700 × (343 + 20) ÷ 343 = **{fo_obs:.1f} Hz**. The two are not equal: a moving source changes the wavelength in the air, while a moving observer only meets the unchanged waves more often. If both approach each other at 72 km/h, f′ = 700 × 363 ÷ 323 = **{fo_both:.1f} Hz**.

| Speed | Source moving | Observer moving | Difference |
|---|---|---|---|
{asym_rows}
The gap grows quickly with speed, because the source term v ÷ (v − v<sub>s</sub>) blows up as v<sub>s</sub> nears the speed of sound while the observer term grows only in a straight line.

## Working out a speed from a recording

Record a vehicle passing, read the steady pitch before and after it goes by, and solve the two Doppler equations together: v<sub>s</sub> = v × (f<sub>a</sub> − f<sub>r</sub>) ÷ (f<sub>a</sub> + f<sub>r</sub>). For the default siren, {fa:.1f} Hz approaching and {fr:.1f} Hz receding give 343 × {fa-fr:.1f} ÷ {fa+fr:.1f} = **{vs_back:.1f} m/s**, which is 72 km/h. The nice feature is that you do not need to know the siren's true frequency. Temperature still matters: on a 0 °C day, with sound at 331.3 m/s, the same siren approaching at 72 km/h sounds at {fo_cold:.1f} Hz.

## Doppler ultrasound

Medical and industrial ultrasound measures a reflected beam, so the shift is doubled and only the speed along the beam counts: Δf = 2 f v cos θ ÷ c. A 5 MHz probe looking at blood moving at 0.5 m/s, with a 60° angle between beam and flow and c = 1,540 m/s in tissue, sees a shift of **{df_us:.0f} Hz**, conveniently in the audible range, which is why Doppler machines can play blood flow as sound. If the operator sets the angle as 65° instead of 60°, the machine reports {vb_wrong:.2f} m/s instead of 0.50 m/s, so the angle setting matters a lot above about 60°.

## Common mistakes

- **Getting the sign convention backwards.** In this calculator positive speeds mean moving towards the other party; a receding source needs a negative v<sub>s</sub>.
- **Mixing km/h and m/s.** The speed of sound is in m/s while the vehicle speeds are in km/h; 72 km/h is 20 m/s, not 72 m/s.
- **Swapping the source and observer formulas.** As the table shows, the two cases give different answers at high speed.
- **Ignoring the angle.** Only the part of the velocity along the line to the listener counts. A car passing 50 m away on a straight road gives a smooth slide in pitch, and no shift at all at the moment it is closest.
- **Forgetting wind.** The speeds must be measured relative to the air, so a steady wind shifts both v<sub>o</sub> and v<sub>s</sub>.
''',
     faq_add=[('Is a moving listener the same as a moving source?',
               f'No. At 72 km/h towards a 700 Hz source a moving listener hears {fo_obs:.1f} Hz, while a source moving at 72 km/h towards a still listener is heard at {fo:.1f} Hz. The difference grows with speed.'),
              ('Can I find the speed of a passing vehicle from its sound?',
               f'Yes. With the pitch heard while it approaches (f_a) and while it moves away (f_r), the speed is v (f_a − f_r) ÷ (f_a + f_r). {fa:.1f} Hz and {fr:.1f} Hz at 343 m/s give {vs_back:.1f} m/s, or 72 km/h.')])

# ================================================================ Torque
Ft, rt, th = 200, 0.3, math.radians(90)
T = Ft * rt * math.sin(th)
rp = rt * math.sin(th)
LBFFT = 1.3558179483
KGFM = G0
assert abs(T - 60) < 1e-9 and abs(rp - 0.3) < 1e-12
# hanging weight on a tilted bar: 10 kg at 0.3 m, bar 30 degrees above horizontal
mw = 10
Wt = mw * G0
T_flat = Wt * 0.3
ang_force = 60  # gravity is vertical; bar at 30 deg above horizontal, angle between them 60 deg
T_tilt = Wt * 0.3 * math.sin(math.radians(ang_force))
# crowfoot extension on a 0.4 m torque wrench
Lw, ext, target = 0.40, 0.05, 60
actual_if_set = target * (Lw + ext) / Lw
set_for_target = target * Lw / (Lw + ext)
# force at the marked grip for 60 N m on this wrench
F_grip = target / Lw
unit_rows = ''
for tq in (10, 25, 60, 100, 250):
    unit_rows += f"| {tq} N·m | {tq/LBFFT:.2f} lbf·ft | {tq/LBFFT*12:,.1f} lbf·in | {tq/KGFM:.3f} kgf·m |\n"

edit('physics/torque', date=U, phrase='torque calculator',
     intro=("Torque is the turning effect of a force, equal to the force times its perpendicular distance from the pivot. "
            "This torque calculator finds it from the force, lever arm length and the angle between them, and also shows the effective perpendicular lever arm.\n\n"
            "Mechanics use it to check spanner and torque wrench settings, engineers to size levers, cranks and motors, and students to solve moment and lever balance problems in N·m, lbf·ft or kgf·m."),
     before='## Practical notes',
     body_add=f'''
## Second scenario: a weight on a tilted bar

The angle in the formula is between the force and the lever, not between the lever and the ground. Hang a {mw} kg mass ({Wt:.2f} N) at the end of a 0.3 m bar. With the bar horizontal the angle is 90°, so τ = {Wt:.2f} × 0.3 = **{T_flat:.2f} N·m**. Raise the bar to 30° above horizontal and gravity, which still points straight down, now meets the bar at 60°: τ = {Wt:.2f} × 0.3 × sin 60° = **{T_tilt:.2f} N·m**. Entering 30° here would give half the torque, which is the most common error with this formula.

## Torque wrench extensions

A crowfoot or adapter that sticks out {ext*100:.0f} cm in line with a {Lw*100:.0f} cm torque wrench lengthens the lever. Set to {target} N·m, the bolt actually receives {target} × ({Lw:.2f} + {ext:.2f}) ÷ {Lw:.2f} = **{actual_if_set:.1f} N·m**. To deliver {target} N·m, set the wrench to {target} × {Lw:.2f} ÷ {Lw+ext:.2f} = **{set_for_target:.1f} N·m**. An adapter turned at 90° to the handle adds no length and needs no correction. Without any adapter, {target} N·m on this wrench needs {F_grip:.0f} N at the grip.

## Converting torque units

The default answer of {T:.0f} N·m converts as shown in the middle row:

| N·m | lbf·ft | lbf·in | kgf·m |
|---|---|---|---|
{unit_rows}
## How torque is measured

Click type torque wrenches release at a preset value, beam and dial wrenches show the torque as it rises, and electronic wrenches read a strain gauge in the shaft. Workshop wrenches are usually certified to within about 4% of reading and should be checked on a calibrator every year or after a drop. On test benches, rotating torque is measured with an in-line torque transducer between motor and load, and static torque with a reaction sensor or with a known weight hung on a measured arm, exactly as in the scenario above.

## Common mistakes

- **Using the angle to the horizontal** instead of the angle between the force and the lever, as in the tilted bar example.
- **Measuring the lever from the wrong point.** The arm runs from the centre of the bolt or axle to the line of the force, not from the end of the jaw.
- **Confusing lbf·ft with lbf·in.** One lbf·ft is 12 lbf·in, so a spec of 60 lbf·in is only 6.78 N·m.
- **Treating kgf as a mass.** A kgf·m is 9.80665 N·m; entering a mass in kg as the force gives a torque about ten times too small.
- **Forgetting the friction share in bolting.** Most of a tightening torque is spent on thread and head friction, so the same torque gives very different clamp loads with dry and oiled threads.
''',
     faq_add=[('Does the angle in the torque formula mean the angle to the ground?',
               f'No, it is the angle between the force and the lever. A {mw} kg weight on a 0.3 m bar tilted 30° above horizontal meets the bar at 60°, giving {T_tilt:.2f} N·m rather than {T_flat:.2f} N·m on a level bar.'),
              ('How do I correct a torque wrench setting for an extension?',
               f'Set the wrench to target × L ÷ (L + extension), with L measured from the drive to the grip. For {target} N·m with a {Lw*100:.0f} cm wrench and a {ext*100:.0f} cm in-line extension, set {set_for_target:.1f} N·m.')])

# ================================================================ Hooke's law
k, x = 500, 0.04
Fh = k * x
Eh = 0.5 * k * x ** 2
mh = Fh / G0
assert abs(Fh - 20) < 1e-9 and abs(Eh - 0.4) < 1e-9 and abs(mh - 2.0394) < 1e-4
# compression needed to store 1 J
x1J = math.sqrt(2 * 1.0 / k)
# launch of a 50 g ball, all spring energy to kinetic energy
mb = 0.05
v_launch = math.sqrt(2 * Eh / mb)
# extra work from 4 cm to 8 cm
W48 = 0.5 * k * (0.08 ** 2 - 0.04 ** 2)
E8 = 0.5 * k * 0.08 ** 2
assert abs(v_launch - 4.0) < 1e-9 and abs(W48 - 1.2) < 1e-9
# 2 kg mass hung on the spring: static stretch
m2 = 2.0
x_static = m2 * G0 / k
rows_h = ''
for cm in (1, 2, 4, 6, 8, 10):
    xx = cm / 100
    rows_h += f"| {cm} cm | {k*xx:.1f} N | {0.5*k*xx**2:.3f} J | {k*xx/G0:.3f} kg |\n"
# lbf/in conversion
k_lbfin = k / 175.126835

edit('physics/hookes-law', date=U, phrase="Hooke's law calculator",
     intro=("Hooke's law states that, within its elastic limit, a spring's force is proportional to how far it is stretched or compressed from its free length: F = k x. "
            "This Hooke's law calculator returns the force, the elastic energy stored and the equivalent hanging mass.\n\n"
            "Students use it for elasticity problems and lab reports, while designers and technicians use it to pick springs for latches, valves, scales and suspensions, or to solve for stiffness or extension."),
     before='## Practical notes',
     body_add=f'''
## Second scenario: energy and launch speed

The default spring (k = 500 N/m, {k_lbfin:.2f} lbf/in) compressed 4 cm stores {Eh:.1f} J. If it fires a 50 g ball and all of that becomes kinetic energy, the ball leaves at v = √(2 E ÷ m) = √(2 × {Eh:.1f} ÷ 0.05) = **{v_launch:.1f} m/s**. To store a full joule the spring must be compressed √(2 × 1 ÷ 500) = **{x1J*100:.2f} cm**. Pushing on from 4 cm to 8 cm costs ½ × 500 × (0.08² − 0.04²) = **{W48:.1f} J**, three times the work of the first 4 cm, because the force keeps rising along the way. In the other direction, hanging a 2 kg mass from the spring stretches it {x_static*100:.2f} cm at rest.

## Force, energy and mass for the default spring

| Extension | Force | Stored energy | Equivalent mass |
|---|---|---|---|
{rows_h}
Force and mass grow in step with the extension, while energy grows with its square: at 8 cm the spring holds {E8:.1f} J, four times the energy at 4 cm.

## Measuring a spring constant

In a school lab, hang the spring from a clamp, add slotted masses one at a time and read the pointer against a ruler, then plot force against extension and take the slope. The straight part of the line is the spring constant; where the points bend away, the spring has passed its elastic limit or, for close-wound springs, is still overcoming initial tension. Spring makers test compression springs on a load tester that records force at two set lengths, and quote the rate between them, often between about 20% and 80% of the available travel where the coils behave most linearly.

## Common mistakes

- **Using the total length instead of the change in length.** x is measured from the free (unloaded) length, not from the clamp or the floor.
- **Leaving x in centimetres.** With k in N/m, 4 cm must be entered as 0.04 m in a hand calculation, or the force comes out 100 times too large.
- **Entering a mass as a force.** A 2 kg load is {m2*G0:.2f} N; dividing 2 by k instead gives an extension almost ten times too small.
- **Assuming energy doubles with extension.** It rises with x², so the second 4 cm stores three times as much as the first.
- **Ignoring initial tension and preload.** Extension springs need a starting force before they move, and compression springs in a mechanism are usually fitted already compressed, so add the preload length to x.
''',
     faq_add=[('How fast can a compressed spring launch an object?',
               f'If all the stored energy becomes kinetic energy, v = √(k x² ÷ m). A 500 N/m spring compressed 4 cm stores {Eh:.1f} J and launches a 50 g ball at {v_launch:.1f} m/s; friction and the spring\'s own moving mass make the real speed a little lower.'),
              ('Does Hooke\'s law apply to rubber bands?',
               'Only roughly, over a small stretch. Rubber gets stiffer at large extensions and returns less energy than it took to stretch it (hysteresis), so a single spring constant describes it poorly.')])

# ================================================================ Escape velocity
GG = 6.6743e-11
M, R = 5.972e24, 6371e3
ve = math.sqrt(2 * GG * M / R)
vk = ve / 1000
vorb = vk / math.sqrt(2)
gs = GG * M / R ** 2
assert abs(vk - 11.186) < 1e-3 and abs(vorb - 7.910) < 1e-3 and abs(gs - 9.820) < 1e-3
v_kmh = ve * 3.6
# check with sqrt(2 g R)
assert abs(math.sqrt(2 * gs * R) - ve) < 1e-6
# energy per kg and for a 1,000 kg probe
e_kg = 0.5 * ve ** 2
e_probe = 1000 * e_kg
# delta v from a 400 km circular orbit
r400 = R + 400e3
v_esc400 = math.sqrt(2 * GG * M / r400)
v_orb400 = math.sqrt(GG * M / r400)
dv400 = v_esc400 - v_orb400
# compare: from the ground straight from rest in the rotating frame ignored
# Earth's Schwarzschild radius
c = 299792458
rs = 2 * GG * M / c ** 2
# escape from the Sun at Earth's distance
GM_SUN, AU = 1.32712440018e20, 1.495978707e11
v_sun_1au = math.sqrt(2 * GM_SUN / AU)
v_earth_orbit = math.sqrt(GM_SUN / AU)
# gas retention: rms speeds
KB, AMU = 1.380649e-23, 1.66053907e-27
Mm, Rm = 7.342e22, 1737e3
vm = math.sqrt(2 * GG * Mm / Rm)
gas_rows = ''
for name, mu in (('Hydrogen, H₂', 2.016), ('Helium, He', 4.003), ('Water vapour, H₂O', 18.015), ('Nitrogen, N₂', 28.014), ('Carbon dioxide, CO₂', 44.009)):
    vr_e = math.sqrt(3 * KB * 1000 / (mu * AMU))
    vr_m = math.sqrt(3 * KB * 390 / (mu * AMU))
    gas_rows += f"| {name} | {vr_e/1000:.2f} km/s | {ve/vr_e:.1f} | {vr_m/1000:.2f} km/s | {vm/vr_m:.1f} |\n"

edit('physics/escape-velocity', date=U, phrase='escape velocity calculator',
     intro=("Escape velocity is the launch speed an unpowered object needs to coast away from a planet, moon or star and never fall back, about 11.2 km/s at the Earth's surface. "
            "This escape velocity calculator works it out from the body's mass and radius.\n\n"
            "Students and astronomy enthusiasts use it for gravitation problems, and mission planners use the same numbers, with the matching orbital speed and surface gravity, to budget the speed changes needed for spaceflight."),
     before='## Practical notes',
     body_add=f'''
## What the default result means in energy

The default Earth values give v<sub>esc</sub> = **{vk:.3f} km/s** ({v_kmh:,.0f} km/h), v<sub>orbit</sub> = **{vorb:.3f} km/s** and g = **{gs:.3f} m/s²**. As a check, √(2 g R) = √(2 × {gs:.3f} × 6.371 × 10⁶) gives the same {ve:,.0f} m/s. Escaping means supplying kinetic energy ½ v² = GM ÷ R = **{e_kg/1e6:.1f} MJ per kilogram**, so a 1,000 kg probe needs {e_probe/1e9:.1f} GJ, ignoring drag and the rocket's own fuel.

## Second scenario: leaving from orbit

Enter R = 6,771 km (the surface plus 400 km). The escape velocity drops to {v_esc400/1000:.2f} km/s, and a spacecraft already circling there at {v_orb400/1000:.2f} km/s only needs a burn of **{dv400/1000:.2f} km/s** to escape. That is why interplanetary probes start from a parking orbit: the hard part, reaching orbit, has already been done.

## Escape velocity and atmospheres

A planet keeps a gas over billions of years roughly when its escape velocity is at least six times the gas's typical molecular speed, √(3 k T ÷ m). The table compares the Earth's {vk:.2f} km/s with molecular speeds at about 1,000 K, a typical temperature high in the Earth's thin outer atmosphere, and the Moon's {vm/1000:.2f} km/s with speeds at its daytime surface temperature of about 390 K:

| Gas | Speed at 1,000 K | Earth ratio | Speed at 390 K | Moon ratio |
|---|---|---|---|---|
{gas_rows}
Hydrogen and helium fall well below the factor of six for the Earth and leak away slowly, while nitrogen and carbon dioxide are held. On the Moon every gas falls short, which matches its lack of an atmosphere.

## Beyond a single planet

Escaping the Earth does not mean leaving the solar system. At the Earth's distance from the Sun, solar escape velocity is √(2 GM<sub>Sun</sub> ÷ 1 AU) = **{v_sun_1au/1000:.1f} km/s**, and the Earth already orbits at {v_earth_orbit/1000:.1f} km/s, so a probe launched in the direction of the Earth's motion needs {(v_sun_1au-v_earth_orbit)/1000:.1f} km/s on top once it has left the Earth's gravity. At the other extreme, squeezing the Earth's mass until its escape velocity equals the speed of light would need a radius of 2GM ÷ c² = **{rs*1000:.2f} mm**.

## Common mistakes

- **Entering the altitude instead of the distance from the centre.** For 400 km above the Earth, R is 6,771 km, not 400 km.
- **Mixing kilometres and metres in a hand calculation.** G is in SI units, so R must be in metres; using kilometres makes the answer √1000, about 31.6 times, too large.
- **Thinking the launch must point straight up.** Without air drag, any direction that does not hit the ground works, because escape depends on energy, not direction.
- **Confusing it with orbital velocity.** Circular orbit needs only {vorb:.2f} km/s at the surface; escape needs √2 times that.
- **Forgetting the Earth's rotation and the Sun.** The ground at the equator already moves at 0.47 km/s eastward, and escaping the Earth still leaves an object in orbit round the Sun.
''',
     faq_add=[('How much energy does it take to escape the Earth?',
               f'Per kilogram, GM ÷ R = {e_kg/1e6:.1f} MJ from the surface, ignoring air drag. A 1,000 kg spacecraft needs {e_probe/1e9:.1f} GJ of kinetic energy, and far more fuel energy because a rocket also has to lift its own propellant.'),
              ('What is the escape velocity from the solar system?',
               f'At the Earth\'s distance from the Sun it is about {v_sun_1au/1000:.1f} km/s relative to the Sun. Because the Earth moves at {v_earth_orbit/1000:.1f} km/s, a probe launched along the Earth\'s motion needs about {(v_sun_1au-v_earth_orbit)/1000:.1f} km/s extra after escaping the Earth.')])

print('done')

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-25), section c3: snells-law, impulse, gravitational-force, angular-velocity, friction-force.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-25'
G0 = 9.80665
d2r, r2d = math.radians, math.degrees


def c(x, d=0):
    return f"{x:,.{d}f}"


def sci(x, d=3):
    m, e = f"{x:.{d}e}".split('e')
    e = int(e)
    sup = str(e).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))
    return f"{m} × 10{sup}"


# ---------------------------------------------------------------- Snell's law
n1, t1, n2 = 1.0003, 30.0, 1.333
s2 = n1 * math.sin(d2r(t1)) / n2
t2 = r2d(math.asin(s2))
tc = r2d(math.asin(min(n1, n2) / max(n1, n2)))
dv = t1 - t2
v2 = 299792458 / n2
assert abs(s2 - 0.3752) < 1e-4 and abs(t2 - 22.04) < 0.005 and abs(tc - 48.63) < 0.005 and abs(v2 - 224900569) < 1
# effect of taking air as exactly 1
t2_vac = r2d(math.asin(math.sin(d2r(t1)) / n2))
# lab measurement of an unknown block: incidence 40 deg, refraction measured 25.0 deg
ti, tr = 40.0, 25.0
n_block = n1 * math.sin(d2r(ti)) / math.sin(d2r(tr))
n_block_hi = n1 * math.sin(d2r(ti)) / math.sin(d2r(tr - 0.5))
n_block_lo = n1 * math.sin(d2r(ti)) / math.sin(d2r(tr + 0.5))
# lateral shift through a 10 mm crown glass slab from air
ng, tslab = 1.517, 10.0
shift_rows = ''
for a in (10, 20, 30, 45, 60, 75):
    b = math.asin(n1 * math.sin(d2r(a)) / ng)
    sh = tslab * math.sin(d2r(a) - b) / math.cos(b)
    shift_rows += f"| {a}° | {r2d(b):.2f}° | {sh:.2f} mm |\n"
# apparent depth of a 2.0 m pool seen from straight above
pool = 2.0
app = pool * n1 / n2
# Snell's window: full cone angle seen by a diver
window = 2 * tc
# fibre example
nco, ncl = 1.468, 1.462
NA = math.sqrt(nco ** 2 - ncl ** 2)
acc = r2d(math.asin(NA))
tc_fib = r2d(math.asin(ncl / nco))
# wrong angle reference: entering 30 deg measured from the surface means 60 deg from normal
t2_wrong = r2d(math.asin(n1 * math.sin(d2r(60)) / n2))

edit('physics/snells-law', date=U, phrase="Snell's law calculator",
     intro=("Snell's law describes how a ray of light changes direction when it crosses from one transparent material into another, because its speed changes. "
            "This Snell's law calculator applies n₁ sin θ₁ = n₂ sin θ₂ to give the angle of refraction, the critical angle, the deviation and the speed of light in the second medium.\n\n"
            "Physics students check optics problems with it, while lens designers, fibre optic technicians and refractometer users rely on the same relation to predict where light goes."),
     body_add=f'''
## Measuring an unknown refractive index

In the classic ray box experiment a narrow beam strikes a rectangular block and the incident and refracted rays are traced on paper. With an incidence of {ti:.0f}° and a refracted ray measured at {tr:.1f}°, the block has n = 1.0003 × sin {ti:.0f}° ÷ sin {tr:.1f}° = **{n_block:.3f}**, typical of a crown glass. A protractor reading only good to ±0.5° moves this between {n_block_lo:.3f} and {n_block_hi:.3f}, so repeat the trace at several angles and fit sin θ₁ against sin θ₂: the slope of that straight line is n₂ ÷ n₁. Laboratory refractometers avoid the protractor altogether by locating the sharp edge of the critical angle against a prism, which gives four decimal places.

## Sideways shift through a glass plate

A ray passing through a flat plate leaves parallel to its original direction but displaced sideways by t sin(θ₁ − θ₂) ÷ cos θ₂. For a {tslab:.0f} mm crown glass plate (n = {ng}) in air:

| Angle of incidence | Angle inside the glass | Lateral shift |
|---|---|---|
{shift_rows}
This shift is why a thick window or a filter placed in front of a camera or a laser rangefinder moves the image slightly, and why optical designers include plane plates in their ray traces.

## Apparent depth and Snell's window

Seen from straight above, a {pool:.1f} m deep pool looks only {pool:.1f} × 1.0003 ÷ 1.333 = **{app:.2f} m** deep, because the rays bend away from the normal as they leave the water. A diver looking up sees the entire sky squeezed into a cone {window:.1f}° wide (twice the {tc:.2f}° critical angle); outside it the surface acts as a mirror.

## Fibre optic acceptance angle

A step index fibre with a core of n = {nco} and cladding of n = {ncl} has a critical angle of {tc_fib:.2f}° at the core boundary and a numerical aperture of √({nco}² − {ncl}²) = **{NA:.4f}**. Only light arriving within {acc:.2f}° of the fibre axis is guided, which is why connector alignment matters so much.

## Common mistakes

- **Measuring the angle from the surface.** Snell's law uses the angle from the normal. A ray striking water 30° above the surface is at 60° to the normal and refracts to {t2_wrong:.2f}°, not {t2:.2f}°.
- **Looking for a critical angle going into the denser medium.** Total internal reflection only happens when light travels from the higher index to the lower one; from air into water every angle refracts.
- **Mixing up which index is which.** n₁ always belongs to the medium the light starts in; swapping them gives the reverse path, not the same one.
- **Ignoring the wavelength.** Indices are quoted at 589 nm; crown glass is about 1.513 in deep red and 1.530 in violet, enough to shift a refraction angle by a few tenths of a degree.
- **Over trusting the air value.** Taking air as exactly 1 changes the default result from {t2:.3f}° to {t2_vac:.3f}°. That is negligible for homework but not for precision refractometry, where the temperature of the sample matters more still.
''',
     faq_add=[("How deep does a swimming pool really look?",
               f"Viewed from directly above, the apparent depth is the real depth × n(air) ÷ n(water), about 0.75 of the real depth. A {pool:.1f} m pool looks about {app:.2f} m deep, and it looks shallower still when viewed at an angle."),
              ("What is the acceptance angle of an optical fibre?",
               f"It is arcsin of the numerical aperture, NA = √(n_core² − n_cladding²). A fibre with a {nco} core and {ncl} cladding has NA = {NA:.4f}, so it accepts light within about {acc:.1f}° of its axis.")])

# ---------------------------------------------------------------- Impulse
F, t, m = 500.0, 0.1, 2.0
J = F * t
dv_i = J / m
ag = dv_i / t / G0
assert J == 50 and dv_i == 25 and abs(ag - 25.49) < 0.005
# pulse shapes with the same 50 N s over 0.1 s
pk_rect = J / t
pk_tri = 2 * J / t
pk_sine = math.pi / 2 * J / t
# phone drop: 0.2 kg from 1.5 m, stopped on tile (2 ms) vs carpet (15 ms)
mp, hp = 0.2, 1.5
vp = math.sqrt(2 * G0 * hp)
Jp = mp * vp
drop_rows = ''
for surf, ts in (('Ceramic tile', 0.002), ('Wooden floor', 0.005), ('Carpet', 0.015), ('Foam cushion', 0.06)):
    drop_rows += f"| {surf} | {ts*1000:g} ms | {Jp/ts:,.0f} N | {vp/ts/G0:,.0f} g |\n"
# bounce: same phone rebounding at 30 percent of impact speed on tile
Jb = mp * vp * 1.3
# force plate sampling: 1 kHz on a 0.5 ms golf impact gives fewer than 1 sample
samples_golf = 0.0005 * 1000

edit('physics/impulse', date=U, phrase='impulse calculator',
     intro=("Impulse is the product of a force and the time over which it acts, and by the impulse momentum theorem it equals the change in an object's momentum. "
            "This impulse calculator finds the impulse, the change in velocity, the average force or the contact time, and shows the average acceleration in g.\n\n"
            "Students use it for collision and kick problems, while safety engineers, sports scientists and packaging designers use it to estimate impact forces from drops, airbags and padding."),
     body_add=f'''
## Peak force depends on the pulse shape

The calculator works with the average force, but sensors and structures respond to the peak. The default impulse of {J:.0f} N·s delivered over {t} s can arrive in different shapes:

| Pulse shape | Average force | Peak force | Peak ÷ average |
|---|---|---|---|
| Rectangular (constant force) | {J/t:.0f} N | {pk_rect:.0f} N | 1.00 |
| Half sine (typical elastic impact) | {J/t:.0f} N | {pk_sine:.1f} N | {pk_sine/(J/t):.2f} |
| Triangular (sharp rise and fall) | {J/t:.0f} N | {pk_tri:.0f} N | 2.00 |

All three have the same area under the force time curve, so all three give the same {dv_i:.0f} m/s change in velocity of the {m:.0f} kg mass. Design a mount or a fixture for the peak, not the average.

## Dropping a phone: why the floor matters

A {mp} kg phone dropped from {hp} m lands at √(2 g h) = {vp:.2f} m/s, so the floor must remove {Jp:.3f} N·s of momentum whatever it is made of. Only the stopping time changes:

| Surface | Stopping time | Average force | Average deceleration |
|---|---|---|---|
{drop_rows}
If the phone bounces off the tile at 30% of its impact speed, the impulse rises to {Jb:.3f} N·s, because the floor must also send it back up. Protective cases work by adding a few milliseconds of crush, not by absorbing momentum.

## How impulse is measured

Force plates and instrumented hammers sample a load cell or piezoelectric sensor and integrate the force over time to get the impulse directly. The sampling rate must suit the contact: a 1 kHz plate is fine for a jump lasting 0.3 s, but its 1 ms sample interval is longer than a whole 0.5 ms golf strike, so ball impact studies use sensors read at 50 kHz or more. Without a force sensor, high speed video gives the velocities before and after, and m × Δv gives the impulse.

## Common mistakes

- **Using speed instead of velocity change.** A rebound reverses the direction, so Δv is the sum of the two speeds, not their difference.
- **Reading the average force as the peak.** As the table above shows, the peak can be about twice the average for a sharp impact.
- **Entering the contact time in milliseconds as seconds.** 5 ms is 0.005 s; typing 5 underestimates the force a thousand times.
- **Leaving out gravity during a long contact.** When a person lands from a jump over 0.3 s, the floor force is m Δv ÷ Δt plus the body weight m g.
- **Mixing lbf·s and N·s.** 1 lbf·s is 4.448 N·s, so US rocket motor data must be converted before dividing by a mass in kilograms.
''',
     faq_add=[('Why does a falling object hit harder on a hard floor?',
               f'The impulse is the same on any floor, because it equals the momentum lost. A {mp} kg phone dropped {hp} m carries {Jp:.3f} N·s; stopping it in 2 ms on tile needs about {Jp/0.002:,.0f} N, while stopping it in 15 ms on carpet needs about {Jp/0.015:,.0f} N.')])

# ---------------------------------------------------------------- Gravitational force
Gc = 6.6743e-11
m1, m2, r = 5.972e24, 7.342e22, 384400e3
Fg = Gc * m1 * m2 / r ** 2
g1 = Gc * m1 / r ** 2
Ug = -Gc * m1 * m2 / r
assert abs(Fg / 1.980e20 - 1) < 5e-4 and abs(g1 - 0.002697) < 5e-7 and abs(Ug / -7.613e28 - 1) < 5e-4
# perigee and apogee
rp, ra = 363300e3, 405500e3
Fp, Fa = Gc * m1 * m2 / rp ** 2, Gc * m1 * m2 / ra ** 2
# inverse square table for the Earth and Moon pair
inv_rows = ''
for k in (0.5, 1, 2, 3, 10):
    inv_rows += f"| {k:g} × 384,400 km | {sci(Gc*m1*m2/(k*r)**2)} N | {1/k**2:.4g} |\n"
# Sun on Moon
Ms, AU = 1.989e30, 1.496e11
F_sun_moon = Gc * Ms * m2 / AU ** 2
# torsion balance on a Cavendish scale: 158 kg and 0.73 kg spheres 0.23 m apart
Fcav = Gc * 158 * 0.73 / 0.23 ** 2
# Everest: weight change
Re = 6371e3
gs = Gc * m1 / Re ** 2
ge = Gc * m1 / (Re + 8849) ** 2
dpct = (ge / gs - 1) * 100
# energy to raise the Moon to infinity from its orbit (binding) equals minus U; orbit kinetic is half of that
KE_orbit = -Ug / 2

edit('physics/gravitational-force', date=U, phrase='gravitational force calculator',
     intro=("Gravity is the attraction every mass exerts on every other mass, proportional to both masses and falling off with the square of the distance between their centres. "
            "This gravitational force calculator applies Newton's law of universal gravitation to any two bodies and adds the gravitational acceleration and potential energy.\n\n"
            "Students use it for orbit and weight problems, and astronomy enthusiasts, satellite engineers and teachers use it to compare the pulls between planets, moons and spacecraft."),
     body_add=f'''
## The inverse square law in numbers

Moving the Moon to different distances from the Earth (same masses as the default):

| Distance | Force | Share of the default force |
|---|---|---|
{inv_rows}
Halving the distance multiplies the force by four, and ten times the distance leaves one hundredth. The real Moon swings between about 363,300 km at perigee and 405,500 km at apogee, so the force varies from {sci(Fp)} N to {sci(Fa)} N, about {(Fp/Fg-1)*100:.0f}% above and {(1-Fa/Fg)*100:.0f}% below the mean value.

## Who pulls harder on the Moon?

The Sun is much farther away, but its mass more than makes up for it. At 1 AU ({sci(AU, 3)} m) the Sun pulls on the Moon with {sci(F_sun_moon)} N, about {F_sun_moon/Fg:.1f} times the Earth's pull of {sci(Fg)} N. The Moon still orbits the Earth because the Sun accelerates the Earth and the Moon almost equally, so only the small difference, the tidal effect, disturbs the orbit.

## Measuring the gravitational constant

G cannot be found from planets alone, because astronomy gives only the product G M. It is measured in the laboratory with a torsion balance: two large spheres are brought near two small ones hanging on a thin fibre, and the tiny twist is read with a light beam. With 158 kg and 0.73 kg lead spheres 23 cm apart, the attraction is only {sci(Fcav)} N, comparable to the weight of a single medium grain of sand, so air currents, temperature changes and the fibre's own drift all have to be controlled.

## Energy of the Earth and Moon pair

The potential energy of the default pair is {sci(Ug)} J. For a circular orbit the kinetic energy is half its magnitude, about {sci(KE_orbit)} J, so the total energy is negative and the Moon is bound. Freeing it completely would need the remaining {sci(KE_orbit)} J.

## Common mistakes

- **Using surface to surface distance.** r is measured between centres, so a person standing on the Earth is 6,371 km from the centre, not 0 km.
- **Forgetting to square the distance,** or squaring it in kilometres while G is in SI units. Convert r to metres first; the calculator does this for you when you enter kilometres.
- **Mixing up G and g.** G is the universal constant {Gc} N·m²/kg²; g is the local acceleration, 9.81 m/s² at the Earth's surface and {g1:.6f} m/s² at the Moon's distance.
- **Reading the negative potential energy as an error.** U is zero at infinite separation, so every bound pair has a negative value.
- **Applying the formula to irregular shapes at close range.** For two long bars or a person beside a mountain, the masses are not points and the force must be summed over the parts.
''',
     faq_add=[('Does the Sun pull harder on the Moon than the Earth does?',
               f'Yes. The Sun pulls on the Moon with about {sci(F_sun_moon, 2)} N, roughly {F_sun_moon/Fg:.1f} times the Earth\'s {sci(Fg, 2)} N. The Moon stays with the Earth because the Sun accelerates both of them by almost the same amount.'),
              ('How much lighter am I on top of Mount Everest?',
               f'Treating the Earth as a sphere, gravity at 8,849 m above the mean radius is {abs(dpct):.2f}% lower than at sea level, so a 70 kg person weighs about {70*(gs-ge):.1f} N less. Local geology and the Earth\'s bulge change the real figure slightly.')])

# ---------------------------------------------------------------- Angular velocity
N, rr = 1450.0, 0.100
w = 2 * math.pi * N / 60
f = N / 60
v = w * rr
T = 1 / f
wd = 360 * N / 60
assert abs(w - 151.84) < 0.005 and abs(f - 24.17) < 0.005 and abs(v - 15.18) < 0.005 and abs(T * 1000 - 41.38) < 0.005 and wd == 8700
# car wheel at 100 km/h, rolling radius 0.315 m
vc, rw = 100 / 3.6, 0.315
wc = vc / rw
Nc = wc * 60 / (2 * math.pi)
# encoder 1024 ppr at default
ppr = 1024
fenc = ppr * N / 60
# 60 tooth gear with an inductive pickup
fgear = 60 * N / 60
# angular resolution of the encoder
res_deg = 360 / ppr
# Earth's rotation
w_earth = 2 * math.pi / 86164.1
v_eq = w_earth * 6378137
# strobe trap: flash at half the true frequency shows a frozen single image
f_half = f / 2
# rim speed check for a 230 mm grinding disc at 6600 rpm
v_grind = math.pi * 0.230 * 6600 / 60
# measurement table: pulses per second from common sensors at default speed
sens_rows = ''
for nm, n_per in (('Reflective tape, 1 mark', 1), ('Shaft key with proximity sensor', 1), ('60 tooth gear wheel', 60), ('Incremental encoder, 360 ppr', 360), ('Incremental encoder, 1024 ppr', 1024)):
    sens_rows += f"| {nm} | {n_per} | {n_per*N/60:,.2f} Hz |\n"

edit('physics/angular-velocity', date=U, phrase='angular velocity calculator',
     intro=("Angular velocity is how fast something turns, measured as the angle swept per second, while machines are usually rated in revolutions per minute. "
            "This angular velocity calculator converts rpm to rad/s, degrees per second and Hz, gives the time per revolution and finds the rim speed at any radius.\n\n"
            "Maintenance engineers, machinists and students use it for motor shafts, wheels, pulleys, fans and cutting tools, where formulas for power, stress and surface speed need rad/s."),
     body_add=f'''
## Measuring rotational speed

A tachometer counts events per revolution and divides by time. At the default {N:,.0f} rpm, different sensors give these pulse frequencies:

| Sensor | Pulses per revolution | Pulse frequency |
|---|---|---|
{sens_rows}
A 1024 pulse encoder resolves {res_deg:.3f}° per pulse, so it can measure speed accurately in a few milliseconds, while a single reflective mark gives only {f:.2f} readings per second. Handheld optical tachometers read the tape mark; drive controllers and PLC high speed counters read encoders or gear tooth pickups.

## Second example: a car wheel

At 100 km/h ({vc:.2f} m/s) a tyre with a rolling radius of {rw*1000:.0f} mm turns at ω = v ÷ r = {vc:.2f} ÷ {rw} = **{wc:.2f} rad/s**, which is **{Nc:.0f} rpm**. Here the rim speed is known and the angular velocity is the unknown: enter the speed and radius and clear rpm. Speedometers work the same way in reverse, so fitting larger tyres makes the car go faster than the speedometer shows.

## Very slow and very fast rotation

The Earth turns once per sidereal day (86,164 s), only {w_earth:.4e} rad/s, yet the equator moves at {v_eq:.0f} m/s because the radius is 6,378 km. At the other extreme, a 230 mm angle grinder disc at 6,600 rpm has a rim speed of {v_grind:.1f} m/s, which is why such discs carry a maximum speed rating of 80 m/s.

## Common mistakes

- **Using diameter as the radius.** v = ω r uses the radius; entering the diameter doubles the rim speed.
- **Leaving ω in rpm inside a formula.** P = T ω, a = ω² r and E = ½ I ω² all need rad/s; using 1,450 instead of {w:.2f} gives answers about 9.5 times too large for P and 91 times too large for a.
- **Confusing ω with f.** Frequency is revolutions per second ({f:.2f} Hz here), ω is 2π times larger.
- **Trusting a stroboscope at the first frozen image.** A strobe flashing at {f_half:.2f} Hz also freezes a shaft turning at {f:.2f} Hz; start from a high flash rate and come down to the first single steady image.
- **Assuming the motor runs at its synchronous speed.** A 4 pole induction motor on 50 Hz runs near 1,450 rpm under load, not 1,500 rpm; read the nameplate or measure it.
''',
     faq_add=[('How many rpm does a car wheel turn at 100 km/h?',
               f'With a typical rolling radius of {rw*1000:.0f} mm, ω = 27.78 m/s ÷ {rw} m = {wc:.2f} rad/s, or about {Nc:.0f} rpm. Smaller wheels turn faster at the same road speed.'),
              ('How do I find rpm from encoder pulses?',
               f'rpm = pulse frequency × 60 ÷ pulses per revolution. A 1024 ppr encoder giving {fenc:,.0f} Hz is turning at {fenc*60/ppr:,.0f} rpm.')])

# ---------------------------------------------------------------- Friction force
mu, mf = 0.4, 10.0
Nn = mf * G0
Ff = mu * Nn
th = r2d(math.atan(mu))
ad = mu * G0
assert abs(Nn - 98.07) < 0.005 and abs(Ff - 39.23) < 0.005 and abs(th - 21.80) < 0.005 and abs(ad - 3.923) < 0.0005
# pushing down or pulling up at an angle
ang_rows = ''
for a in (0, 10, 20, 30, 45):
    ca, sa = math.cos(d2r(a)), math.sin(d2r(a))
    pull = mu * Nn / (ca + mu * sa)
    push = mu * Nn / (ca - mu * sa)
    ang_rows += f"| {a}° | {pull:.2f} N | {push:.2f} N |\n"
P_min = mu * Nn / math.sqrt(1 + mu ** 2)
# check that the minimum occurs at atan(mu)
assert abs(mu * Nn / (math.cos(math.atan(mu)) + mu * math.sin(math.atan(mu))) - P_min) < 1e-9
push30 = mu * Nn / (math.cos(d2r(30)) - mu * math.sin(d2r(30)))
pull30 = mu * Nn / (math.cos(d2r(30)) + mu * math.sin(d2r(30)))
# jamming angle for pushing: cos a = mu sin a, a = atan(1/mu)
jam = r2d(math.atan(1 / mu))
# crate released at 2 m/s slides to rest
v0 = 2.0
s_stop = v0 ** 2 / (2 * ad)
t_stop = v0 / ad
W_f = 0.5 * mf * v0 ** 2
assert abs(Ff * s_stop - W_f) < 1e-9
# using mass instead of weight
wrong = mu * mf

edit('physics/friction-force', date=U, phrase='friction force calculator',
     intro=("Friction is the force that resists sliding between two surfaces, and for dry contacts it is proportional to how hard they are pressed together. "
            "This friction force calculator applies F = μN to find the friction force, the normal force or the coefficient of friction, and adds the angle of repose and sliding deceleration.\n\n"
            "Students use it for mechanics problems, and engineers use it to size conveyor drives, brakes, clamps and the push needed to move loads by hand."),
     before='## Practical notes',
     body_add=f'''
## Pulling or pushing at an angle

The default crate needs {Ff:.2f} N when the force is horizontal, but tilting the force changes the normal force. Pulling upward at angle α lifts some of the weight, so P = μ m g ÷ (cos α + μ sin α); pushing downward at α presses the crate harder, so P = μ m g ÷ (cos α − μ sin α). For the 10 kg crate with μ = 0.4:

| Angle of the force | Pulling upward | Pushing downward |
|---|---|---|
{ang_rows}
The easiest pull is at α = arctan μ = {th:.2f}°, the same as the angle of repose, where only **{P_min:.2f} N** is needed. Pushing down at 30° takes {push30:.2f} N against {pull30:.2f} N for pulling up at 30°, which is why a sled or a heavy box is easier to pull with a rope than to push. Beyond arctan(1 ÷ μ) = {jam:.1f}° a downward push can never move the crate, however hard you press.

## Sliding to a stop

If the crate is shoved to {v0:.0f} m/s and released, it decelerates at {ad:.3f} m/s² and stops after v² ÷ (2 μ g) = **{s_stop:.3f} m** in {t_stop:.3f} s. Friction does {Ff:.2f} N × {s_stop:.3f} m = {W_f:.0f} J of work, exactly the kinetic energy ½ m v² the crate started with, and that energy ends up as heat in the two surfaces.

## Measuring friction in practice

Testing standards such as ASTM D1894 for plastic films drag a weighted sled across a sample at a fixed speed and record the force: the first peak gives the static coefficient and the steady plateau the kinetic one. On site, a spring balance on a loaded pallet does the same job. Repeat each test a few times, because dust, moisture and surface wear easily change μ by 20% or more.

## Common mistakes

- **Multiplying μ by the mass instead of the weight.** 0.4 × 10 kg gives {wrong:.0f}, which is not a force; the correct friction is 0.4 × {Nn:.2f} N = {Ff:.2f} N.
- **Treating static friction as always equal to μ<sub>s</sub> N.** μ<sub>s</sub> N is only the maximum. A crate pushed with 20 N that does not move feels exactly 20 N of friction.
- **Using the weight as the normal force on a slope or with an angled push.** The normal force changes with the angle, as the table above shows.
- **Assuming μ cannot exceed 1.** Rubber on dry concrete, silicone and clean metals in vacuum can reach 1 or more; it simply means the friction force is larger than the normal force.
- **Using sliding friction for a rolling wheel.** Rolling resistance coefficients are ten to a hundred times smaller than sliding ones.
''',
     faq_add=[('What is the best angle to pull a box?',
               f'Pull at an angle α = arctan μ above the horizontal. For μ = 0.4 that is {th:.1f}°, and a 10 kg box then needs {P_min:.2f} N instead of {Ff:.2f} N with a horizontal pull, because lifting slightly reduces the normal force.'),
              ('Can the coefficient of friction be greater than 1?',
               'Yes. A coefficient above 1 only means the friction force exceeds the normal force. Racing tyres on dry asphalt, rubber on clean glass and some soft polymers commonly show values of 1 to 2.')])

print('done')

# ======================================================================= SECTION _expand_c4.py
"""Expand (2026-11-25), section c4: theoretical-yield, percent-composition, beer-lambert, normality, pka.
Every number is computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-25'

AR = {'H': 1.008, 'C': 12.011, 'N': 14.007, 'O': 15.999, 'Na': 22.990, 'Mg': 24.305, 'P': 30.974,
      'S': 32.06, 'K': 39.098, 'Ca': 40.078, 'Cu': 63.546}


def mm(**f):
    return sum(AR[e] * n for e, n in f.items())


H2O = mm(H=2, O=1)
SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')


def sci(x, d=3):
    a, b = f'{x:.{d}e}'.split('e')
    return a + ' × 10' + str(int(b)).translate(SUP)

# ---------------------------------------------------------------- Theoretical yield
m, MR, r, p, MP, ma = 2.0, 138.12, 1, 1, 180.16, 2.1
nP = m / MR * p / r
mT = nP * MP
Y = ma / mT
assert abs(nP - 0.014480) < 1e-6 and abs(mT - 2.6087) < 1e-4 and abs(Y * 100 - 80.50) < 0.01
# acetic anhydride check: 5.0 mL at 1.08 g/mL
M_ac2o = mm(C=4, H=6, O=3)
n_ac2o = 5.0 * 1.08 / M_ac2o
excess = n_ac2o / nP
# atom economy (by product acetic acid)
AE = MP / (MR + M_ac2o)
# fermentation: C6H12O6 -> 2 C2H5OH + 2 CO2
M_glu = mm(C=6, H=12, O=6)
M_eth = mm(C=2, H=6, O=1)
g_glu = 50.0
n_eth = g_glu / M_glu * 2 / 1
m_eth = n_eth * M_eth
m_eth_wrong = g_glu / M_glu * 1 / 2 * M_eth
# purity
pur = 0.98
mT_pur = m * pur / MR * MP
Y_pur = ma / mT_pur
# multistep table
steps_rows = ''
for n in (1, 2, 3, 5, 8):
    steps_rows += f"| {n} | {0.9**n*100:.1f}% | {0.8**n*100:.1f}% | {0.7**n*100:.1f}% |\n"
over3 = 0.80 * 0.85 * 0.90

edit('chemistry/theoretical-yield', date=U, phrase='theoretical yield calculator',
     intro=("The theoretical yield is the largest mass of product a reaction can give when all of the limiting reagent reacts exactly as the balanced equation says. "
            "This theoretical yield calculator converts the reagent mass to moles, applies the mole ratio and returns grams of product, plus the percent yield.\n\n"
            "Chemistry students use it for lab reports and stoichiometry homework, and process chemists use it to set batch targets and judge how much product a step loses."),
     body_add=f'''
## Checking which reagent is limiting

In the aspirin synthesis the salicylic acid is reacted with acetic anhydride (C₄H₆O₃, {M_ac2o:.2f} g/mol). A typical recipe adds 5.0 mL of anhydride, which at 1.08 g/mL is {5.0*1.08:.2f} g or {n_ac2o:.4f} mol. That is {excess:.2f} times the {nP:.5f} mol of salicylic acid, so the anhydride is in excess and the salicylic acid really is the limiting reagent. Basing the yield on the anhydride would overstate the theoretical yield by the same factor.

## Second example: a 1 : 2 mole ratio

Fermentation turns one glucose into two ethanol: C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂. For {g_glu:.0f} g of glucose ({M_glu:.3f} g/mol), set r = 1, p = 2 and the product molar mass to {M_eth:.3f} g/mol:

- Moles of glucose = {g_glu:.0f} ÷ {M_glu:.3f} = {g_glu/M_glu:.5f} mol
- Moles of ethanol = {g_glu/M_glu:.5f} × 2 ÷ 1 = **{n_eth:.5f} mol**
- Theoretical yield = {n_eth:.5f} × {M_eth:.3f} = **{m_eth:.2f} g** of ethanol

So the theoretical ethanol yield is {m_eth/g_glu*100:.1f}% of the sugar mass; the rest leaves as CO₂. Yeast also burns some sugar for growth, so real fermentations reach only part of this figure.

## Theoretical yield, atom economy and overall yield

Theoretical yield says how much product the limiting reagent can make. **Atom economy** says how much of all the reactant mass can end up in the product. For aspirin it is {MP} ÷ ({MR} + {M_ac2o:.2f}) = **{AE*100:.1f}%**, because one acetic acid is made as a by-product for every aspirin. A reaction can have a 100% yield and still a poor atom economy.

In a multistep synthesis the overall yield is the product of the step yields. Three steps at 80%, 85% and 90% give {over3*100:.1f}% overall:

| Steps | 90% per step | 80% per step | 70% per step |
|---|---|---|---|
{steps_rows}
This is why process chemists fight for every percent in a long route.

## Common mistakes

- **Inverting the mole ratio.** Using r ÷ p instead of p ÷ r in the fermentation example gives {m_eth_wrong:.2f} g instead of {m_eth:.2f} g, a factor of four too low.
- **Ignoring reagent purity.** With 98% pure salicylic acid only {m*pur:.2f} g is reactant, so the theoretical yield drops to {mT_pur:.3f} g and the same 2.10 g gives {Y_pur*100:.1f}%, not {Y*100:.1f}%.
- **Using the wrong molar mass form.** A hydrate or salt (for example sodium salicylate instead of salicylic acid) has a different molar mass; use the form you actually weighed.
- **Weighing a damp product.** Solvent left in the crystals inflates the actual yield, sometimes above 100%. Dry to constant mass before weighing.
- **Basing the calculation on an unbalanced equation.** The coefficients r and p must come from the balanced equation, or the mole ratio is meaningless.
''',
     faq_add=[('How do I include reagent purity in the theoretical yield?',
               f'Multiply the weighed mass by the purity fraction before entering it. 2.00 g of 98% salicylic acid counts as {m*pur:.2f} g, which gives a theoretical yield of {mT_pur:.3f} g of aspirin.'),
              ('How do I calculate the overall yield of a multistep synthesis?',
               f'Multiply the fractional yields of the steps. Steps of 80%, 85% and 90% give 0.80 × 0.85 × 0.90 = {over3:.3f}, an overall yield of {over3*100:.1f}%.')])

# ---------------------------------------------------------------- Percent composition
k, Ar_, M = 2, 1.008, 18.015
pc = k * Ar_ / M
assert abs(pc * 100 - 11.19) < 0.01
mH_kg = pc * 1000
pO = 1 - pc
# glucose full composition
Mg = mm(C=6, H=12, O=6)
gl = [('C', 6), ('H', 12), ('O', 6)]
gl_rows = ''.join(f"| {e} | {n} | {n*AR[e]:.3f} | {n*AR[e]/Mg*100:.2f}% |\n" for e, n in gl)
gl_sum = sum(n * AR[e] / Mg * 100 for e, n in gl)
assert abs(gl_sum - 100) < 1e-9
# calcium hydroxide parentheses trap
M_caoh = mm(Ca=1, O=2, H=2)
pO_caoh = 2 * AR['O'] / M_caoh
pO_caoh_wrong = 1 * AR['O'] / M_caoh
# hydrates
hyd = [('CuSO₄·5H₂O', mm(Cu=1, S=1, O=4) + 5 * H2O, 5),
       ('MgSO₄·7H₂O (Epsom salt)', mm(Mg=1, S=1, O=4) + 7 * H2O, 7),
       ('Na₂CO₃·10H₂O (washing soda)', mm(Na=2, C=1, O=3) + 10 * H2O, 10),
       ('CaSO₄·2H₂O (gypsum)', mm(Ca=1, S=1, O=4) + 2 * H2O, 2)]
hyd_rows = ''.join(f"| {n} | {Mx:.2f} | {w} | {w*H2O/Mx*100:.2f}% |\n" for n, Mx, w in hyd)
# fertiliser oxide factors
fP = 2 * AR['P'] / mm(P=2, O=5)
fK = 2 * AR['K'] / mm(K=2, O=1)
# acceptance window for elemental analysis
c_found_lo, c_found_hi = 40.00 - 0.4, 40.00 + 0.4

edit('chemistry/percent-composition', date=U, phrase='percent composition calculator',
     description='Calculate the mass percent of an element in a compound from its atom count, atomic mass and molar mass, with worked hydrate and fertiliser examples.',
     intro=("Percent composition is the share of a compound's mass that comes from each element, fixed by the chemical formula. "
            "This percent composition calculator multiplies the atom count by the atomic mass and divides by the molar mass of the compound to give the mass percent of one element.\n\n"
            "Students use it to check formulas and find empirical formulas, while analysts compare it with elemental analysis results to confirm the identity and purity of a sample."),
     replace=[('''## More examples

| Compound | Element | % by mass |
|---|---|---|
| CO₂ (44.01) | C | 27.3% |
| NaCl (58.44) | Na | 39.3% |
| C₆H₁₂O₆ (180.16) | C | 40.0% |
| Fe₂O₃ (159.69) | Fe | 69.9% |''',
               f'''## Water of crystallisation in common hydrates

Use k = number of water molecules, "atomic mass" = {H2O:.3f} g/mol for H₂O and the molar mass of the whole hydrate:

| Hydrate | Molar mass (g/mol) | H₂O per formula | Water by mass |
|---|---|---|---|
{hyd_rows}
Heating a weighed hydrate to constant mass and comparing the loss with this percentage is a classic way to find the number of water molecules.''')],
     body_add=f'''
## What the default values give

The calculator opens with hydrogen in water: k = 2, atomic mass 1.008 g/mol and molar mass 18.015 g/mol.

- Mass of hydrogen per mole = 2 × 1.008 = {k*Ar_:.3f} g
- Percent hydrogen = {k*Ar_:.3f} ÷ 18.015 × 100 = **{pc*100:.2f}%**
- Oxygen is the remainder, {pO*100:.2f}%, and 1 kg of water holds {mH_kg:.1f} g of hydrogen

## Full composition of glucose

Run the calculator once per element with M = {Mg:.3f} g/mol:

| Element | Atoms | Mass per mole (g) | Mass percent |
|---|---|---|---|
{gl_rows}
The three percentages add to {gl_sum:.2f}%. If your own total is off by more than a few hundredths, an atom count or atomic mass is wrong.

## How percent composition is used in practice

A CHN combustion analyser burns a few milligrams of sample and measures the CO₂, H₂O and N₂ formed, reporting carbon, hydrogen and nitrogen as mass percent. Chemists compare those numbers with the calculated composition. Many journals accept a new compound when each element is within 0.4 percentage points of theory, so a glucose sample must read between {c_found_lo:.2f}% and {c_found_hi:.2f}% carbon. On fertiliser labels phosphorus and potassium are quoted as oxides: %P = %P₂O₅ × {fP:.4f} and %K = %K₂O × {fK:.4f}, factors that come straight from this formula.

## Common mistakes

- **Missing atoms inside parentheses.** Ca(OH)₂ has two oxygens: {pO_caoh*100:.2f}% O, not the {pO_caoh_wrong*100:.2f}% that k = 1 gives.
- **Leaving out water of crystallisation.** The molar mass of a hydrate includes the water, so the percentages of the other elements fall.
- **Using the molar mass of the element gas.** Oxygen in a formula counts 15.999 g/mol per atom, not 31.998 for O₂.
- **Reading fertiliser grades as elements.** The middle number is P₂O₅, so a 0-46-0 grade holds {46*fP:.1f}% phosphorus, not 46%.
- **Rounding atomic masses to whole numbers.** Using 1 for hydrogen gives 2 ÷ 18 = {2/18*100:.2f}% for water instead of {pc*100:.2f}%, an error of {(pc-2/18)*100:.2f} points before any measurement is made.
''',
     faq_add=[('How do I convert a fertiliser P₂O₅ or K₂O value to the element?',
               f'Multiply by the mass fraction of the element in the oxide: P = P₂O₅ × {fP:.4f} and K = K₂O × {fK:.4f}. A label with 20% P₂O₅ supplies {20*fP:.2f}% phosphorus.'),
              ('Is percent composition the same as the mass percent of a solution?',
               'No. Percent composition is fixed by the chemical formula of a pure compound. Mass percent of a solution or mixture depends on how much of each component was mixed, and is found with the mass percent calculator.')])

# ---------------------------------------------------------------- Beer-Lambert
eps, l, c = 6220, 1, 0.0001
A = eps * l * c
T = 10 ** (-A)
assert abs(A - 0.622) < 1e-9 and abs(T * 100 - 23.88) < 0.01
# reverse: measured A 0.450
A_m = 0.450
c_m = A_m / (eps * l)
# enzyme assay rate
dA = 0.050
rate = dA / (eps * l) * 1e6
# path length table for the default concentration
pl_rows = ''
for L in (0.2, 0.5, 1, 2, 5, 10):
    a = eps * L * c
    pl_rows += f"| {L:g} cm | {a:.3f} | {10**-a*100:.2f}% |\n"
# photometric error for a fixed 0.5 %T reading error
dT = 0.005
err_rows = ''
for a in (0.05, 0.2, 0.4343, 1.0, 2.0):
    t = 10 ** -a
    err_rows += f"| {a:g} | {t*100:.1f}% | {0.4343*dT/(t*a)*100:.2f}% |\n"
e_def = 0.4343 * dT / (T * A) * 100
# stray light 0.1%
s = 0.001
sl_rows = ''
for a in (0.5, 1, 2, 3):
    am = -math.log10((10 ** -a + s) / (1 + s))
    sl_rows += f"| {a:g} | {am:.3f} | {(am/a-1)*100:.1f}% |\n"

edit('chemistry/beer-lambert', date=U, phrase='Beer-Lambert law calculator',
     intro=("The Beer-Lambert law says a solution's absorbance rises in direct proportion to the concentration of the absorbing species and the path length of light through it. "
            "This Beer-Lambert law calculator works out absorbance and transmittance from A = εlc, or the concentration from a measured absorbance.\n\n"
            "Biochemists, analytical chemists and water quality analysts use it to quantify samples on UV-visible spectrophotometers, plate readers and online colorimetric analysers."),
     body_add=f'''
## From a reading back to concentration

Suppose the same NADH assay reads A = {A_m:.3f} in the 1 cm cuvette. Then c = A ÷ (ε l) = {A_m:.3f} ÷ ({eps:,} × {l}) = **{sci(c_m)} mol/L**, or {c_m*1e6:.1f} µmol/L. In a kinetic enzyme assay the same division turns a slope into a rate: a fall of {dA:.3f} absorbance per minute at 340 nm means NADH is used at {rate:.2f} µmol/L per minute.

## Effect of path length at the default concentration

| Path length | Absorbance | Transmittance |
|---|---|---|
{pl_rows}
Long path cells (5 to 10 cm) are used for trace analysis in clean water, while 0.1 to 0.2 cm cells or diluting the sample bring a strong absorber back into range.

## Why mid-range readings are most precise

A photometer's noise is roughly a fixed error in transmittance. For a 0.5% T reading error the relative error in concentration is 0.4343 ΔT ÷ (T A):

| Absorbance | Transmittance | Concentration error |
|---|---|---|
{err_rows}
The minimum sits at A = 0.434 (T = 36.8%). The default reading of A = {A:.3f} gives about {e_def:.2f}%, comfortably inside the good zone.

## How stray light bends the curve

Stray light is light that reaches the detector outside the selected band. With 0.1% stray light the instrument reads A = −log((T + s) ÷ (1 + s)):

| True absorbance | Reading with 0.1% stray light | Error |
|---|---|---|
{sl_rows}
This is why calibration lines flatten at the top even when the chemistry is perfectly linear.

## Measuring in practice

Zero the instrument with a blank of the same solvent and reagents in a matched cuvette, then read at λ<sub>max</sub>, where small wavelength errors matter least. Polystyrene cuvettes absorb strongly in the deep UV, so 260 nm work needs quartz or UV-grade cells. In microplate readers the light passes vertically, so the path length depends on the fill volume; many readers correct it from the water absorbance band near 977 nm.

## Common mistakes

- **Entering percent transmittance as absorbance.** Convert first: A = −log₁₀(T), so 23.9% T is A = {-math.log10(0.239):.3f}, not 23.9.
- **Mixing ε units.** NADH is often quoted as 6.22 mM⁻¹ cm⁻¹, which is {eps:,} L/(mol·cm); using 6.22 with mol/L gives a concentration a thousand times too high.
- **Assuming a 1 cm path in a microplate well.** A partly filled well has a much shorter path, so concentrations come out too low unless you correct it.
- **Skipping the blank.** Reagent colour and cuvette absorbance add to every reading and shift the whole calibration line upward.
- **Reading off the absorption peak.** On a steep shoulder a 1 nm wavelength drift changes ε noticeably and the results drift with it.
''',
     faq_add=[('How do I convert molar absorptivity from mM⁻¹ cm⁻¹ to L/(mol·cm)?',
               f'Multiply by 1,000. NADH at 340 nm is 6.22 mM⁻¹ cm⁻¹, which is {eps:,} L/(mol·cm), the default value in this calculator.'),
              ('At what absorbance is a spectrophotometer most precise?',
               'For a fixed transmittance error the relative concentration error is smallest at A = 0.434, where 36.8% of the light is transmitted. Readings between about 0.2 and 1.0 keep the error within roughly twice that minimum.')])

# ---------------------------------------------------------------- Normality
m_, Mw, neq, V = 4.904, 98.079, 2, 500
cM = m_ / Mw / (V / 1000)
N = cM * neq
EW = Mw / neq
assert abs(cM - 0.1000) < 1e-4 and abs(N - 0.2000) < 1e-4 and abs(EW - 49.0395) < 1e-4
meq25 = N * 25.00
# standardising NaOH
VNaOH = 24.60
N_naoh = N * 25.00 / VNaOH
g_naoh = N_naoh * 39.997
# from concentrated acid 98% w/w, 1.84 g/mL
c_conc = 1840 * 0.98 / Mw
N_conc = c_conc * 2
V_conc = N * V / N_conc
# one molarity, several normalities
mp_rows = (f"| H₃PO₄, 0.1 M | to H₂PO₄⁻ (methyl orange end point) | 1 | {0.1*1:.1f} N |\n"
           f"| H₃PO₄, 0.1 M | to HPO₄²⁻ (phenolphthalein end point) | 2 | {0.1*2:.1f} N |\n"
           f"| KMnO₄, 0.02 M | to Mn²⁺ (acid solution) | 5 | {0.02*5:.2f} N |\n"
           f"| KMnO₄, 0.02 M | to MnO₂ (neutral or weakly alkaline) | 3 | {0.02*3:.2f} N |\n"
           f"| KMnO₄, 0.02 M | to MnO₄²⁻ (strongly alkaline) | 1 | {0.02*1:.2f} N |\n")
# alkalinity titrant 0.02 N
EW_caco3 = mm(Ca=1, C=1, O=3) / 2
mg_per_mL = 0.02 * EW_caco3

edit('chemistry/normality', date=U, phrase='normality calculator', before='## Notes',
     intro=("Normality counts reactive equivalents per litre: protons for an acid, hydroxide ions for a base, electrons for a redox reagent. A 1 N acid exactly neutralises the same volume of a 1 N base. "
            "This normality calculator gives normality, molarity and equivalent weight from the mass you weigh out.\n\n"
            "Analytical chemists and water testing labs use it to prepare and check titrants, where results are reported in equivalents."),
     body_add=f'''
## Using the default solution in a titration

The default solution is {N:.4f} N sulfuric acid, so a 25.00 mL aliquot holds {N:.4f} × 25.00 = **{meq25:.3f} meq** of acid. If it takes {VNaOH:.2f} mL of sodium hydroxide to reach the end point, N₁V₁ = N₂V₂ gives N(NaOH) = {N:.4f} × 25.00 ÷ {VNaOH:.2f} = **{N_naoh:.4f} N**. Since NaOH has n = 1, that is also {N_naoh:.4f} mol/L, or {g_naoh:.2f} g of NaOH per litre.

## Making it from concentrated acid

Nobody weighs out pure sulfuric acid. Concentrated acid is about 98% w/w with a density of 1.84 g/mL, which works out to 1,840 × 0.98 ÷ {Mw} = {c_conc:.2f} mol/L or {N_conc:.2f} N. For 500 mL of {N:.4f} N you need {N:.4f} × 500 ÷ {N_conc:.2f} = **{V_conc:.2f} mL** of concentrated acid, added slowly to about 400 mL of water before making up to the mark. Because the strength of the concentrated acid is never exact, the diluted solution is then standardised against a primary standard such as sodium carbonate.

## One molarity, several normalities

The value of n belongs to the reaction, not to the bottle:

| Solution | Reaction used | n | Normality |
|---|---|---|---|
{mp_rows}
Always write the reaction next to a normality on a label or in a method, or the number cannot be checked.

## Normality in water testing

Standard methods for alkalinity and hardness still use normal solutions because the arithmetic becomes simple. Calcium carbonate has an equivalent weight of {EW_caco3:.2f} g/eq, so each millilitre of 0.02 N acid neutralises 0.02 meq, which is {mg_per_mL:.3f} mg of CaCO₃. Titrating a 100 mL sample therefore gives alkalinity in mg/L as CaCO₃ as ten times the titre in millilitres.

## Common mistakes

- **Taking n from the wrong reaction.** Permanganate is 5 equivalents per mole only in acid solution, as the table shows.
- **Using molarities in N₁V₁ = N₂V₂.** 0.1 M H₂SO₄ needs twice its own volume of 0.1 M NaOH; with normalities (0.2 N against 0.1 N) the equation works directly.
- **Weighing the anhydrous mass for a hydrate.** Oxalic acid dihydrate is 126.065 g/mol, not 90.03 g/mol for the anhydrous acid.
- **Trusting the weighed mass of sodium hydroxide.** NaOH pellets pick up water and CO₂ from the air, so standardise the solution by titration rather than relying on the balance.
- **Adding solute to the full volume of water.** V is the final volume of solution: dissolve, then make up to the mark in a volumetric flask.
''',
     faq_add=[('What is a milliequivalent?',
               f'One thousandth of an equivalent. The number of milliequivalents in a portion of solution is normality × volume in mL, so 25.00 mL of {N:.4f} N acid holds {meq25:.3f} meq.'),
              ('How much concentrated sulfuric acid makes 500 mL of 0.2 N?',
               f'About {V_conc:.2f} mL. Concentrated acid (98% w/w, 1.84 g/mL) is {N_conc:.2f} N, and {N:.4f} × 500 ÷ {N_conc:.2f} = {V_conc:.2f} mL. Add the acid to water, never water to acid, and standardise the result.')])

# ---------------------------------------------------------------- pKa
Ka = 0.000018
pKa = -math.log10(Ka)
Kb = 1e-14 / Ka
pKb = 14 - pKa
assert abs(pKa - 4.7447) < 1e-4 and abs(Kb - 5.5556e-10) < 1e-13 and abs(pKb - 9.2553) < 1e-4
C = 0.10
x_apx = math.sqrt(Ka * C)
x_ex = (-Ka + math.sqrt(Ka ** 2 + 4 * Ka * C)) / 2
ion = x_ex / C
oh = math.sqrt(Kb * C)
pH_ac = 14 + math.log10(oh)
# fraction deprotonated vs pH
fr_rows = ''
for pH in (3.0, 4.0, round(pKa, 2), 5.0, 6.0, 7.0):
    a = 1 / (1 + 10 ** (pKa - pH))
    fr_rows += f"| {pH:.2f} | {(1-a)*100:.1f}% | {a*100:.1f}% |\n"
ln_wrong = -math.log(Ka)
# Davies estimate of apparent pKa at I = 0.1 M
I = 0.1
lg = -0.509 * (math.sqrt(I) / (1 + math.sqrt(I)) - 0.3 * I)
pKa_I = pKa + 2 * lg

edit('chemistry/pka', date=U, phrase='pKa calculator',
     intro=("pKa is the negative base 10 logarithm of an acid's dissociation constant Ka: the lower the pKa, the stronger the acid. "
            "This pKa calculator converts Ka to pKa or back and gives the Kb and pKb of the conjugate base at 25 °C.\n\n"
            "Chemists and lab technicians use these numbers to estimate pH and choose a buffer, as in [pH meter calibration buffers](https://www.instrumentationblog.in/ph-meter-calibration-buffers/)."),
     body_add=f'''
## From pKa to the pH of a solution

The default Ka of 1.8 × 10⁻⁵ also predicts the pH of a 0.10 mol/L acetic acid solution. The quick estimate [H⁺] = √(Ka C) = {sci(x_apx)} mol/L gives pH {-math.log10(x_apx):.3f}. Solving the full quadratic, [H⁺] = (−Ka + √(Ka² + 4 Ka C)) ÷ 2 = {sci(x_ex)} mol/L, gives pH **{-math.log10(x_ex):.3f}**, so only {ion*100:.2f}% of the acid is ionised. For 0.10 mol/L sodium acetate the Kb of {sci(Kb)} gives [OH⁻] = √(Kb C) = {sci(oh)} mol/L and pH **{pH_ac:.2f}**, which is why acetate solutions are mildly basic.

## How much is ionised at each pH

With pKa = {pKa:.4f}, the fraction present as acetate is 1 ÷ (1 + 10<sup>pKa − pH</sup>):

| pH | Acetic acid (HA) | Acetate (A⁻) |
|---|---|---|
{fr_rows}
Each pH unit away from the pKa shifts the ratio tenfold. Chromatographers use this to keep an analyte fully ionised or fully neutral, and formulators use it to predict how a drug will behave at stomach or blood pH.

## How pKa is measured

The usual method is a potentiometric titration with a calibrated pH electrode: titrate the weak acid with strong base and read the pH at the half equivalence point, where [HA] = [A⁻] and pH = pKa. Acids with a chromophore can also be measured by UV-visible spectroscopy, following the absorbance of the two forms across a series of buffers. Tabulated values usually refer to zero ionic strength. In a 0.1 mol/L salt background the Davies equation puts the apparent pKa of acetic acid near {pKa_I:.2f} instead of {pKa:.2f}, so measured values in real media read lower.

## Common mistakes

- **Using the natural log.** −ln(1.8 × 10⁻⁵) is {ln_wrong:.2f}, not a pKa; the definition uses log₁₀.
- **Mistyping the exponent.** 1.8e5 instead of 1.8e-5 gives a negative pKa of {-math.log10(1.8e5):.2f}, which would describe a strong acid.
- **Treating a base's pKb as the pKa.** For ammonia enter its Kb (1.8 × 10⁻⁵) and read the pKa of the ammonium ion, {pKb:.2f}; the two numbers are not interchangeable.
- **Picking the wrong pKa of a polyprotic acid.** A phosphate buffer at pH 7.2 is governed by the second pKa (7.20), not the first (2.15).
- **Comparing values measured in different media.** Ionic strength and solvent shift pKa, so check the conditions before comparing two sources.
''',
     faq_add=[('How do I find pKa from a titration curve?',
               'Locate the equivalence point volume, halve it, and read the pH at that volume. At the half equivalence point the concentrations of the acid and its conjugate base are equal, so pH = pKa.'),
              ('What is the pH of 0.1 M acetic acid?',
               f'With Ka = 1.8 × 10⁻⁵ the exact quadratic gives [H⁺] = {sci(x_ex)} mol/L and pH {-math.log10(x_ex):.2f}. The square root shortcut gives {-math.log10(x_apx):.2f}, close enough because under 2% of the acid ionises.')])

print('done')

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-25), section c5: equilibrium-constant, weak-acid-ph, ppm, gay-lussacs-law, mass-percent.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-25'
R_ATM = 0.0820574      # L atm / (mol K), as in the page equation
R_BAR = 0.0831446      # L bar / (mol K)


def c(x, d=0):
    return f"{x:,.{d}f}"


def sci(x, d=3):
    m, e = f"{x:.{d}e}".split('e')
    e = int(e)
    sup = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    return f"{m} × 10{str(e).translate(sup)}"


# ======================================================================= Equilibrium constant
cA, a, cB, b, cC, cc, cD, d, TC = 0.5, 1, 1.5, 3, 0.1, 2, 1, 0, 500
TK = TC + 273.15
Kc = cC ** cc * cD ** d / (cA ** a * cB ** b)
dn = cc + d - a - b
RT = R_ATM * TK
Kp = Kc * RT ** dn
Kp_bar = Kc * (R_BAR * TK) ** dn
assert abs(Kc - 0.0059259) < 1e-6 and dn == -2 and abs(Kp - 1.472e-6) < 1e-9
# reaction quotient checks
Q_hi = 0.20 ** 2 / (cA * cB ** 3)
Q_lo = 0.05 ** 2 / (cA * cB ** 3)
assert Q_hi > Kc > Q_lo
# ICE table: H2 + I2 = 2HI, Kc = 54.3 at 430 C, start 0.500 M each
K_HI, c0 = 54.3, 0.500
s = math.sqrt(K_HI)
xi = c0 * s / (2 + s)
HI = 2 * xi
left = c0 - xi
assert abs(HI ** 2 / left ** 2 - K_HI) < 1e-9
conv_pct = xi / c0 * 100
# manipulations of the default equation
manip = [
    ('N₂ + 3H₂ ⇌ 2NH₃ (as written)', Kc, Kp, dn),
    ('2NH₃ ⇌ N₂ + 3H₂ (reversed)', 1 / Kc, 1 / Kp, -dn),
    ('½N₂ + 3⁄2H₂ ⇌ NH₃ (halved)', Kc ** 0.5, Kp ** 0.5, dn / 2),
    ('2N₂ + 6H₂ ⇌ 4NH₃ (doubled)', Kc ** 2, Kp ** 2, dn * 2),
]
for name, k1, k2, n in manip:
    assert abs(k1 * RT ** n - k2) / k2 < 1e-9
manip_rows = ''.join(f"| {nm} | {sci(k1, 4)} | {n:g} | {sci(k2, 4)} |\n" for nm, k1, k2, n in manip)

eq_body = f'''
## Checking the direction with the reaction quotient

The reaction quotient Q uses the same expression as K<sub>c</sub> but with the concentrations you have right now. Keep [N₂] = 0.50 M and [H₂] = 1.50 M from the example:

- If [NH₃] is 0.20 M, Q = 0.20² ÷ (0.50 × 1.50³) = **{Q_hi:.5f}**. Q is larger than K<sub>c</sub> = {Kc:.6f}, so ammonia decomposes until the ratio falls back to K.
- If [NH₃] is 0.05 M, Q = 0.05² ÷ 1.6875 = **{Q_lo:.6f}**. Q is smaller than K<sub>c</sub>, so more ammonia forms.

## Finding equilibrium concentrations with an ICE table

Going the other way, from K to concentrations, needs an initial, change, equilibrium (ICE) table. For H₂ + I₂ ⇌ 2HI, K<sub>c</sub> is about {K_HI} at 430 °C. Start with {c0:.3f} M of each reactant and let x react:

| | H₂ | I₂ | HI |
|---|---|---|---|
| Initial (M) | {c0:.3f} | {c0:.3f} | 0 |
| Change (M) | −x | −x | +2x |
| Equilibrium (M) | {c0:.3f} − x | {c0:.3f} − x | 2x |

K<sub>c</sub> = (2x)² ÷ ({c0:.3f} − x)². Taking the square root of both sides gives 2x ÷ ({c0:.3f} − x) = √{K_HI} = {s:.4f}, so x = **{xi:.4f} M**. At equilibrium [H₂] = [I₂] = **{left:.4f} M** and [HI] = **{HI:.4f} M**, which is {conv_pct:.1f}% conversion. Δn = 0 here, so K<sub>p</sub> equals K<sub>c</sub> and pressure has no effect on the position of equilibrium. You can confirm the result by entering these three concentrations with a = b = 1, c = 2, d = 0.

## How K depends on the way the equation is written

K belongs to a particular balanced equation. Using the default mixture at 500 °C (773.15 K):

| Equation | K<sub>c</sub> | Δn | K<sub>p</sub> (atm) |
|---|---|---|---|
{manip_rows}
Reversing the equation inverts K, halving every coefficient takes the square root, and doubling squares it. Quote the equation alongside any K value. With pressures in bar instead of atm, the as written K<sub>p</sub> becomes {sci(Kp_bar, 4)}, because R changes to {R_BAR} L·bar/(mol·K).

## How equilibrium concentrations are measured

Equilibrium concentrations are rarely weighed out; they are measured in a mixture that has stopped changing. Coloured species are followed by spectrophotometry and the Beer-Lambert law, the classic teaching case being the blood red FeSCN²⁺ ion. Acid and base equilibria are followed with a pH electrode. Gas phase equilibria such as ammonia synthesis are sampled at temperature and analysed by gas chromatography, or worked out from the change in total pressure at constant volume. A sample must be measured quickly or quenched by cooling, otherwise the equilibrium shifts as conditions change.

## Common mistakes

- **Including pure solids and liquids.** Solid carbon or liquid water as a solvent have no concentration term; set their coefficients to 0 so they also drop out of Δn.
- **Using initial instead of equilibrium concentrations.** Values before the reaction has settled give Q, not K.
- **Putting °C into RT.** The conversion needs kelvin; 500 °C is 773.15 K, and RT is then {RT:.3f} L·atm/mol.
- **Using R = 8.314.** That value is in J/(mol·K) and gives a meaningless K<sub>p</sub>; with concentrations in mol/L and pressures in atm, R must be 0.08206 L·atm/(mol·K).
- **Forgetting that K changes with temperature.** Ammonia synthesis is exothermic, so its K falls as temperature rises; a K measured at 500 °C cannot be used at 400 °C.
'''

edit('chemistry/equilibrium-constant', date=U, phrase='equilibrium constant calculator',
     intro=("The equilibrium constant K compares product and reactant amounts once a reversible reaction stops changing, with each concentration raised to its coefficient in the balanced equation. "
            "This equilibrium constant calculator finds Kc for aA + bB ⇌ cC + dD and converts it to Kp in atmospheres with Kp = Kc(RT)^Δn.\n\n"
            "Chemistry students use it to check ICE table homework, and process chemists use it to judge how far reactions such as ammonia synthesis can go at a given temperature."),
     replace=[('''- K<sub>c</sub> = 0.10² ÷ (0.50 × 1.50³) = **0.005926**
- Δn = 2 − 4 = **-2**
- K<sub>p</sub> = 0.005926 × (0.0820574 × 773.15)<sup>−2</sup> = **1.472e-06**''',
               f'''- 1.50³ = {cB**3:.4f}, so the denominator is 0.50 × {cB**3:.4f} = {cA*cB**3:.4f}
- K<sub>c</sub> = 0.10² ÷ {cA*cB**3:.4f} = 0.0100 ÷ {cA*cB**3:.4f} = **{Kc:.6f}**
- Δn = 2 − (1 + 3) = **{dn}**
- T = 500 + 273.15 = {TK:.2f} K, so RT = 0.0820574 × {TK:.2f} = {RT:.3f} L·atm/mol
- K<sub>p</sub> = {Kc:.6f} × {RT:.3f}<sup>−2</sup> = {Kc:.6f} ÷ {RT**2:,.1f} = **{sci(Kp, 3)}**

K<sub>p</sub> is far smaller than K<sub>c</sub> because Δn is negative: four moles of gas become two, so each pressure term carries an extra factor of RT.''')],
     before='## Notes', body_add=eq_body,
     faq_add=[('How does K change if I reverse or multiply the equation?',
               f'Reversing the equation gives 1 ÷ K, and multiplying all coefficients by n raises K to the power n. For the default ammonia mixture Kc = {Kc:.6f}, the reversed reaction has Kc = {1/Kc:.2f} and the halved equation has Kc = {Kc**0.5:.5f}.'),
              ('How do I find equilibrium concentrations from K?',
               f'Set up an ICE table, write each equilibrium concentration in terms of x, substitute into the K expression and solve for x. For H₂ + I₂ ⇌ 2HI with Kc = {K_HI} and {c0:.3f} M of each reactant, x = {xi:.4f} M, giving [HI] = {HI:.4f} M.')])

# ======================================================================= Weak acid pH
t, K, C = 1, 0.000018, 0.1


def wa(K, C):
    return (math.sqrt(K ** 2 + 4 * K * C) - K) / 2


x = wa(K, C)
pH = t * (-math.log10(x)) + (1 - t) * (14 + math.log10(x))
al = x / C
assert abs(x - 1.3327e-3) < 1e-7 and abs(pH - 2.875) < 0.001 and abs(al * 100 - 1.333) < 0.001
Ka_back = x ** 2 / (C - x)
assert abs(Ka_back - K) < 1e-12
x_sc = math.sqrt(K * C)
pH_sc = -math.log10(x_sc)
sc_err = (x_sc / x - 1) * 100
acids = [('Hydrofluoric acid, HF', 6.8e-4), ('Formic acid, HCOOH', 1.8e-4), ('Benzoic acid, C₆H₅COOH', 6.3e-5),
         ('Acetic acid, CH₃COOH', 1.8e-5), ('Hypochlorous acid, HOCl', 3.0e-8), ('Hydrocyanic acid, HCN', 6.2e-10)]
acid_rows = ''
for nm, ka in acids:
    xx = wa(ka, 0.1)
    acid_rows += f"| {nm} | {sci(ka, 1)} | {-math.log10(xx):.3f} | {xx/0.1*100:.3g}% | {-math.log10(math.sqrt(ka*0.1)):.3f} |\n"
# Ka from a measured pH
Cu, pHm = 0.050, 3.40
xu = 10 ** -pHm
Ka_u = xu ** 2 / (Cu - xu)
pKa_u = -math.log10(Ka_u)
# sodium acetate 0.1 M as a weak base
Kb_ac = 1e-14 / K
xb = wa(Kb_ac, 0.1)
pH_ac = 14 + math.log10(xb)
assert 8.8 < pH_ac < 8.9
# NH4+ pKa
pKa_nh4 = 14 + math.log10(1.8e-5)

wa_body = f'''
## Checking the default answer

Put the result back into the equilibrium expression: Ka = x² ÷ (C − x) = (1.3327 × 10⁻³)² ÷ (0.1 − 0.0013327) = {sci(Ka_back, 3)}, which returns the Ka you entered. The shortcut x = √(Ka C) = √(1.8 × 10⁻⁶) = {sci(x_sc, 4)} mol/L gives pH {pH_sc:.3f}. It overestimates [H⁺] by {sc_err:.1f}% and moves the pH by only {pH-pH_sc:.3f}, because acetic acid at 0.1 M is barely dissociated.

## Common weak acids at 0.1 mol/L

Ka values are typical 25 °C figures; pH is from the exact quadratic, the last column from the √(Ka C) shortcut.

| Acid | Ka | pH (exact) | Dissociated | pH (shortcut) |
|---|---|---|---|---|
{acid_rows}
The shortcut only fails noticeably for the stronger weak acids. For HF it predicts a pH {(-math.log10(wa(6.8e-4,0.1)))-(-math.log10(math.sqrt(6.8e-5))):.3f} units too low, because about 8% of the acid has dissociated and C − x is no longer close to C.

## Finding Ka from a measured pH

In the lab Ka is usually found the other way round. Suppose a calibrated pH meter reads **{pHm:.2f}** in a {Cu:.3f} mol/L solution of an unknown weak acid. Then [H⁺] = 10<sup>−{pHm:.2f}</sup> = {sci(xu, 3)} mol/L, and Ka = x² ÷ (C − x) = **{sci(Ka_u, 2)}**, so pKa = {pKa_u:.2f}. Calibrate the meter with two buffers that bracket the reading, such as pH 4.01 and 7.00, and measure at the temperature the Ka refers to. A pH electrode responds to hydrogen ion activity, so in concentrated or salty solutions the apparent Ka differs slightly from the tabulated thermodynamic value.

## The pH of a salt such as sodium acetate

The conjugate base of a weak acid is itself a weak base, with Kb = Kw ÷ Ka. For acetate, Kb = 10⁻¹⁴ ÷ (1.8 × 10⁻⁵) = {sci(Kb_ac, 3)}. Choose weak base, enter that Kb and 0.1 mol/L, and the calculator gives [OH⁻] = {sci(xb, 3)} mol/L and **pH {pH_ac:.2f}**. That is why a sodium acetate solution is mildly alkaline, and why the endpoint of an acetic acid titration with sodium hydroxide sits above pH 7.

## Common mistakes

- **Entering pKa instead of Ka.** A pKa of 4.74 typed into the Ka box describes an absurdly strong acid; convert first with Ka = 10<sup>−pKa</sup>.
- **Using the conjugate's constant.** Ammonia has Kb = 1.8 × 10⁻⁵, but the ammonium ion is an acid with pKa {pKa_nh4:.2f}; pick the constant that matches the species you dissolved.
- **Treating a polyprotic acid as one step.** For phosphoric or carbonic acid the first dissociation sets the pH, but the second and third steps matter for speciation and buffering.
- **Applying it after adding base.** Once part of the acid has been neutralised the solution is a buffer, and the Henderson-Hasselbalch equation is the right tool.
- **Assuming pKw = 14 at every temperature.** At 50 °C pKw is about 13.26, so the weak base result from 14 + log x drifts by more than half a unit.
'''

edit('chemistry/weak-acid-ph', date=U, phrase='weak acid pH calculator',
     intro=("A weak acid only partly dissociates in water, so its pH depends on both the concentration and the acid dissociation constant Ka. "
            "This weak acid pH calculator solves the equilibrium exactly with the quadratic formula, also handles weak bases from Kb, and reports [H⁺] or [OH⁻] and the percent dissociated.\n\n"
            "Students use it for ICE table problems, and lab staff use it to predict the reading a [pH sensor](https://www.instrumentationblog.in/what-is-ph-sensor-how-does-it-work/) should give for a prepared solution."),
     before='## Notes', body_add=wa_body,
     faq_add=[('How do I find Ka from a measured pH?',
               f'Convert the pH to [H⁺] = 10^(−pH) and use Ka = [H⁺]² ÷ (C − [H⁺]). A 0.050 mol/L acid reading pH 3.40 has [H⁺] = {sci(xu, 2)} mol/L and Ka = {sci(Ka_u, 2)}.'),
              ('What is the pH of a sodium acetate solution?',
               f'Acetate is a weak base with Kb = Kw ÷ Ka = {sci(Kb_ac, 2)}. A 0.1 mol/L solution has [OH⁻] = {sci(xb, 2)} mol/L and pH {pH_ac:.2f} at 25 °C.')])

# ======================================================================= PPM
ms_mg, mt_kg = 50, 1
ms_kg = ms_mg * 1e-6
ppm = ms_kg / mt_kg * 1e6
pct = ppm / 1e6
ppb = ppm * 1000
assert abs(ppm - 50) < 1e-9 and abs(pct * 100 - 0.005) < 1e-12 and abs(ppb - 50000) < 1e-6
# working backwards: 250 ppm sodium in 20 kg water
tgt, batch = 250, 20
na_mg = tgt * batch
Na, Cl = 22.990, 35.453
f_na = Na / (Na + Cl)
nacl_g = na_mg / 1000 / f_na
# seawater mg/kg vs mg/L
sw_ppm, sw_rho = 35000, 1.025
sw_mgL = sw_ppm * sw_rho
# gas ppm to mg/m3 at 25 C, 1 atm
Vm = R_ATM * 298.15
gases = [('Carbon monoxide, CO', 28.010), ('Ammonia, NH₃', 17.031), ('Hydrogen sulfide, H₂S', 34.08),
         ('Carbon dioxide, CO₂', 44.009), ('Sulfur dioxide, SO₂', 64.06), ('Nitrogen dioxide, NO₂', 46.005)]
gas_rows = ''.join(f"| {nm} | {M:.2f} | {M/Vm:.3f} | {50*M/Vm:.1f} |\n" for nm, M in gases)
# TDS estimate from conductivity
ec, kf = 800, 0.65
tds = ec * kf

ppm_body = f'''
## Working backwards to a mass

To hit a target ppm, multiply the target by the sample mass in kilograms to get milligrams. A {batch} kg batch of water at {tgt} ppm sodium needs {tgt} × {batch} = **{c(na_mg)} mg ({na_mg/1000:.0f} g) of sodium**. Sodium is only {f_na*100:.2f}% of the mass of sodium chloride (22.990 ÷ 58.443), so the salt to weigh out is {na_mg/1000:.0f} ÷ {f_na:.4f} = **{nacl_g:.2f} g of NaCl**. Always check whether a limit is stated for the ion or for the whole compound.

## When ppm and mg/L are not the same

ppm by mass is milligrams per kilogram; mg/L is milligrams per litre. They match only when a litre of the sample weighs 1 kg. Seawater at {c(sw_ppm)} mg/kg with a density of {sw_rho} kg/L holds {c(sw_ppm)} × {sw_rho} = **{c(sw_mgL)} mg/L**, a {(sw_rho-1)*100:.1f}% difference. For brines, acids, oils and soils, report mg/kg and mg/L separately.

## Gas ppm (by volume) to mg/m³

For gases ppm usually means ppmv, a mole fraction. To convert to a mass concentration at 25 °C and 1 atm, use mg/m³ = ppmv × M ÷ {Vm:.2f}, where M is the molar mass in g/mol and {Vm:.2f} L/mol is the molar volume at those conditions.

| Gas | M (g/mol) | mg/m³ per 1 ppmv | mg/m³ at 50 ppmv |
|---|---|---|---|
{gas_rows}
The same 50 ppm is almost four times heavier for sulfur dioxide than for ammonia, so a gas detector set in ppm and an emission limit set in mg/m³ have to be converted per gas. This calculator itself works by mass; use the table for gas readings.

## How ppm is measured in practice

- **Dissolved solids:** a TDS meter measures electrical conductivity and multiplies by a factor of roughly 0.5 to 0.8 that depends on which salts are present. A reading of {ec} µS/cm with a factor of {kf} is reported as about {tds:.0f} mg/L.
- **Chlorine:** handheld kits use the DPD colour reaction, and online analyzers in treatment plants use amperometric or colorimetric cells that read free chlorine continuously in mg/L.
- **Trace metals:** ICP-OES and ICP-MS measure elements such as lead and arsenic down to ppb and below after acid digestion of the sample.
- **Gases:** NDIR sensors read CO₂ in ppm, and electrochemical cells read CO and H₂S for personal gas detectors.

## Common mistakes

- **Mixing units in the ratio.** Grams over kilograms is a factor of 1,000 off; the calculator converts, but hand calculations must put both masses in the same unit before multiplying by 10⁶.
- **Confusing ppm by mass with ppmv.** 50 ppmv of CO₂ in air is not 50 mg/kg; convert with the molar mass.
- **Assuming mg/L equals ppm in dense liquids** such as seawater or concentrated brine.
- **Dividing by 100 instead of 10,000 for percent.** 50 ppm is 0.005%, not 0.5%.
- **Reporting the compound when the limit is for the ion**, for example nitrate as NO₃⁻ versus nitrate nitrogen (NO₃-N), which differ by a factor of about 4.43.
'''

edit('chemistry/ppm', date=U, phrase='ppm calculator',
     description='Calculate concentration in parts per million from solute and sample mass, convert ppm to percent and ppb, and see how ppm relates to mg/L and mg/m³.',
     intro=("Parts per million (ppm) states a very small concentration as the mass of one substance per million mass units of the whole sample, so 1 mg in 1 kg is 1 ppm. "
            "This ppm calculator turns a solute mass and a sample mass into ppm, percent and parts per billion.\n\n"
            "Water treatment operators use it to dose chlorine and check a [residual chlorine analyzer](https://www.instrumentationblog.in/residual-chlorine-analyzer-working/), and laboratories use it to report trace metals and dissolved salts."),
     replace=[('ppm = 0.050 g ÷ 1,000 g × 10⁶ = **50 ppm** = 0.005%',
               f'''- Substance mass: 50 mg = 0.050 g = {ms_kg:.6f} kg
- ppm = {ms_kg:.6f} kg ÷ {mt_kg} kg × 10⁶ = **{ppm:.0f} ppm**
- Percent = {ppm:.0f} ÷ 10,000 = **{pct*100:.3f}%**
- Parts per billion = {ppm:.0f} × 1,000 = **{c(ppb)} ppb**''')],
     body_add=ppm_body,
     faq_add=[('How do I convert ppm of a gas to mg/m³?',
               f'At 25 °C and 1 atm, mg/m³ = ppmv × molar mass ÷ {Vm:.2f}. For carbon monoxide (28.01 g/mol), 1 ppmv is {28.010/Vm:.3f} mg/m³, so 50 ppmv is {50*28.010/Vm:.1f} mg/m³.'),
              ('How much substance do I need for a given ppm?',
               f'Multiply the target ppm by the sample mass in kg to get milligrams. {tgt} ppm in {batch} kg of water needs {c(na_mg)} mg, which is {na_mg/1000:.0f} g.')])

# ======================================================================= Gay-Lussac's law
P1, T1C, T2C = 200.0, 20.0, 80.0
T1, T2 = T1C + 273.15, T2C + 273.15
P2 = P1 * T2 / T1
assert abs(P2 - 240.93) < 0.01
PATM = 101.325
# temperature at a 300 kPa(a) limit
Plim = 300.0
Tlim = T1 * Plim / P1
# gauge trap: 200 kPa gauge entered as absolute
P1abs_g = 200 + PATM
P2_true_g = P1abs_g * T2 / T1 - PATM
P2_wrong_g = P2
# Celsius trap
P2_celsius = P1 * T2C / T1C
# slope and absolute zero extrapolation
slope = (P2 - P1) / (T2C - T1C)
t0 = T1C - P1 / slope
assert abs(t0 + 273.15) < 1e-9
rows = ''
for name, p in (('Jar sealed at atmosphere', PATM), ('Default example', 200.0), ('Small receiver', 500.0),
                ('Air receiver, 10 bar(a)', 1000.0), ('Gas cylinder, 200 bar(a)', 20000.0)):
    rows += f"| {name} | {c(p, 1)} kPa | {p/T1:.3f} kPa | {c(p*(50+273.15)/T1, 1)} kPa |\n"

gl_body = f'''
## Solving for temperature

Leave the final temperature blank and enter a final pressure to find when a vessel reaches a limit. If the default container (200 kPa absolute at 20 °C) has a relief valve set at {Plim:.0f} kPa absolute:

- T<sub>2</sub> = T<sub>1</sub> × P<sub>2</sub> ÷ P<sub>1</sub> = {T1:.2f} × {Plim:.0f} ÷ {P1:.0f} = **{Tlim:.2f} K**
- In Celsius: {Tlim:.2f} − 273.15 = **{Tlim-273.15:.1f} °C**

## The gauge pressure trap

Suppose the 200 kPa in the example was really read on a gauge. The absolute pressure is 200 + {PATM} = {P1abs_g:.3f} kPa, and at 80 °C it becomes {P1abs_g:.3f} × {T2:.2f} ÷ {T1:.2f} = {P1abs_g*T2/T1:.1f} kPa absolute, or **{P2_true_g:.1f} kPa gauge**. Entering the gauge value as if it were absolute gives {P2_wrong_g:.1f} kPa, an underestimate of {P2_true_g-P2_wrong_g:.1f} kPa. When the gas is heated, this error is always on the unsafe side.

## Pressure rise per degree

The pressure changes by P<sub>1</sub> ÷ T<sub>1</sub> for every kelvin, so the rise per degree grows with the fill pressure. For gases sealed at 20 °C:

| Sealed system | Absolute pressure at 20 °C | Rise per °C | At 50 °C |
|---|---|---|---|
{rows}
A cylinder left in the sun gains about {20000/T1:.0f} kPa (0.68 bar) for every degree, which is why cylinders are stored away from heat and their filling pressure is always quoted at a reference temperature, usually 15 °C.

## Absolute zero from two readings

Gay-Lussac's law is the basis of the constant volume gas thermometer. Plot the two default points against Celsius temperature: the slope is ({P2:.2f} − {P1:.0f}) ÷ ({T2C:.0f} − {T1C:.0f}) = {slope:.4f} kPa per °C, and the line reaches zero pressure at {T1C:.0f} − {P1:.0f} ÷ {slope:.4f} = **{t0:.2f} °C**. Guillaume Amontons used the same idea around 1700 to estimate that an absolute zero of temperature must exist.

## Common mistakes

- **Using Celsius directly.** 200 × 80 ÷ 20 gives {P2_celsius:.0f} kPa, a fourfold rise instead of the real {(P2/P1-1)*100:.1f}%.
- **Using gauge pressure.** Add atmospheric pressure first, then subtract it again from the answer if a gauge value is needed.
- **Applying it to a flexible container.** A tyre or balloon expands as it warms, so its pressure rises less than the law predicts; use the combined gas law when volume changes.
- **Applying it to a liquefied gas.** A propane or CO₂ cylinder holding liquid follows the vapour pressure curve, which climbs much faster than P ∝ T.
- **Forgetting temperature gradients.** If only part of a vessel is heated, the gas is not at one temperature, so use the average gas temperature, not the hottest surface.
'''

edit('chemistry/gay-lussacs-law', date=U, phrase="Gay-Lussac's law calculator",
     intro=("Gay-Lussac's law says that the pressure of a fixed amount of gas in a rigid, sealed container is proportional to its absolute temperature. "
            "This Gay-Lussac's law calculator finds the final pressure after heating or cooling, or the temperature that gives a chosen pressure.\n\n"
            "Engineers use it to check gas cylinders, sealed vessels and trapped pipe sections against their pressure ratings, remembering that the law needs [absolute rather than gauge pressure](https://www.instrumentationblog.in/absolute-vs-gauge-pressure/)."),
     before='## Notes', body_add=gl_body,
     faq_add=[('How much does gas pressure rise per degree in a sealed container?',
               f'By P₁ ÷ T₁ per kelvin. A gas at 200 kPa absolute and 20 °C rises by {P1/T1:.3f} kPa for every degree, so heating it by 60 °C adds {P2-P1:.1f} kPa.'),
              ("Does Gay-Lussac's law apply to a propane cylinder?",
               "Not while it contains liquid. The pressure then equals the vapour pressure of propane, which rises much faster with temperature than the gas law predicts. The law applies only to a gas that stays a gas.")])

# ======================================================================= Mass percent
ms, mw = 25.0, 475.0
mt = ms + mw
w = ms / mt
assert mt == 500 and abs(w - 0.05) < 1e-12
AW = {'Na': 22.990, 'Cl': 35.453, 'H': 1.008, 'O': 15.999, 'Cu': 63.546, 'S': 32.06}
M_nacl = AW['Na'] + AW['Cl']
M_h2o = 2 * AW['H'] + AW['O']
n_nacl = ms / M_nacl
n_h2o = mw / M_h2o
molal = n_nacl / (mw / 1000)
xfrac = n_nacl / (n_nacl + n_h2o)
rho5 = 1.0340  # g/mL, 5 % NaCl at 20 C
vol = mt / rho5
molar = n_nacl / (vol / 1000)
wv = ms / vol * 100
# mixing two solutions
mA, wA, mB, wB = 200, 0.10, 300, 0.02
w_mix = (mA * wA + mB * wB) / (mA + mB)
w_avg = (wA + wB) / 2
# dilution by mass of 37 % HCl to 10 %
m_conc, w_conc, w_tgt = 100, 0.37, 0.10
m_final = m_conc * w_conc / w_tgt
m_water = m_final - m_conc
# hydrate
M_cuso4 = AW['Cu'] + AW['S'] + 4 * AW['O']
M_hyd = M_cuso4 + 5 * M_h2o
f_anh = M_cuso4 / M_hyd
need_anh = 0.02 * 500
hyd_g = need_anh / f_anh
# wrong denominator
w_wrong = ms / mw
tab = ''
for wp in (0.5, 1, 2, 5, 10, 20, 26):
    ww = wp / 100
    tab += f"| {wp:g}% | {c(ww*1e6)} | {ww/(1-ww)*1000:.1f} g | {ww/(1-ww)/M_nacl*1000:.3f} |\n"

mp_body = f'''
## The 5% example in other units

The 5% salt solution can be restated without new measurements, except for molarity, which needs a density:

- Moles of NaCl = 25 ÷ {M_nacl:.3f} = {n_nacl:.4f} mol
- Molality = {n_nacl:.4f} mol ÷ 0.475 kg water = **{molal:.4f} mol/kg**
- Mole fraction of NaCl = {n_nacl:.4f} ÷ ({n_nacl:.4f} + 475 ÷ {M_h2o:.3f}) = **{xfrac:.5f}**
- In ppm by mass: 0.05 × 10⁶ = **{c(w*1e6)} ppm**
- With a measured density of {rho5:.4f} g/mL at 20 °C, the 500 g occupy {vol:.1f} mL, so the molarity is **{molar:.4f} mol/L** and the strength is {wv:.2f}% w/v

## Mixing and diluting by mass

Solute mass is conserved, so mass percent mixes by a mass weighted average. Combining {mA} g of {wA*100:.0f}% solution with {mB} g of {wB*100:.0f}% solution gives ({mA} × {wA} + {mB} × {wB}) ÷ {mA+mB} = **{w_mix*100:.1f}%**, not the simple average of {w_avg*100:.0f}%.

To dilute {m_conc} g of {w_conc*100:.0f}% hydrochloric acid to {w_tgt*100:.0f}%, the final mass must be {m_conc} × {w_conc} ÷ {w_tgt} = {m_final:.0f} g, so add **{m_water:.0f} g of water**. Weigh the water first and add the acid to it slowly, never the other way round.

## Salt in water by mass percent

Solute per kilogram of water and molality for sodium chloride (M = {M_nacl:.3f} g/mol). These figures follow from the mass fraction alone and need no density.

| Mass percent | ppm | NaCl per kg water | Molality (mol/kg) |
|---|---|---|---|
{tab}
Sodium chloride saturates at about 26.4% by mass at 20 °C, so stronger brines cannot be made at room temperature.

## Weighing hydrated salts

Many solids are sold as hydrates, and the water of crystallisation counts as solvent. To make 500 g of a 2% copper(II) sulfate solution from CuSO₄·5H₂O, note that the anhydrous salt is {M_cuso4:.2f} ÷ {M_hyd:.2f} = {f_anh*100:.2f}% of the hydrate mass. You need {need_anh:.0f} g of CuSO₄, which means weighing **{hyd_g:.2f} g of the pentahydrate** and making up to 500 g with {500-hyd_g:.2f} g of water. In practice, tare the beaker on a balance, add the solid, then add solvent until the total reaches the target mass.

## Common mistakes

- **Dividing by the solvent mass.** 25 ÷ 475 = {w_wrong*100:.2f}%, not 5%; the denominator is the whole solution.
- **Averaging percentages when mixing.** Weight each percentage by its solution mass, as in the {w_mix*100:.1f}% example above.
- **Treating w/w and w/v as equal.** For dense solutions they differ a lot: 37% w/w hydrochloric acid at 1.19 g/mL is 44.0% w/v.
- **Ignoring water of hydration.** Weighing 10 g of CuSO₄·5H₂O supplies only {10*f_anh:.2f} g of CuSO₄.
- **Using molarity tables at the wrong temperature.** Mass percent does not change with temperature, but the density used to convert it to molarity does.
'''

edit('chemistry/mass-percent', date=U, phrase='mass percent calculator',
     intro=("Mass percent, also called weight percent or % w/w, is the mass of one component divided by the total mass of the mixture, times 100. "
            "This mass percent calculator adds the solute and solvent masses and gives the concentration, or works back to the masses needed for a target strength.\n\n"
            "Lab technicians, pharmacists, food producers and fertiliser mixers use it because weighing is precise and the result does not change with temperature, unlike molarity."),
     replace=[('mass % = 25 ÷ 500 = **5%**',
               f'''- Total solution mass = 25 + 475 = **{mt:.0f} g**
- Mass fraction = 25 ÷ {mt:.0f} = {w:.2f}
- Mass percent = {w:.2f} × 100 = **{w*100:.0f}%**''')],
     before='## Common uses', body_add=mp_body,
     faq_add=[('How do I find the mass percent after mixing two solutions?',
               f'Add the solute masses and divide by the total mass. {mA} g of {wA*100:.0f}% plus {mB} g of {wB*100:.0f}% contains {mA*wA+mB*wB:.0f} g of solute in {mA+mB} g, which is {w_mix*100:.1f}%.'),
              ('How do I convert mass percent to molality?',
               f'Molality = (w ÷ (1 − w)) × 1000 ÷ M, with w the mass fraction and M the solute molar mass. A 5% NaCl solution is {molal:.3f} mol/kg.')])

print('done')

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-25), section c6: osmotic-pressure, combined-gas-law, avogadros-law, van-der-waals, activation-energy.
Every number is computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-25'
R = 8.314462618
G = 9.80665
NA = 6.02214076e23
ATM = 101325.0


def sci(x, d=3):
    m, e = f"{x:.{d}e}".split('e')
    sup = str.maketrans('-0123456789', '\u207b\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079')
    return m + ' × 10' + str(int(e)).translate(sup)

# ================================================================ Osmotic pressure
i0, c0, T0 = 2, 0.15, 37 + 273.15
P0 = i0 * c0 * 1000 * R * T0          # calculator equation, Pa
assert abs(P0 / ATM - 7.635) < 0.001 and abs(P0 / 1000 - 773.6) < 0.1
RT0 = R * T0
h_water = P0 / (1000 * G)
P0_psi = P0 / 6894.757
P0_mmHg = P0 / 133.322
# osmotic coefficient of 0.15 mol/kg NaCl is about 0.93
phi = 0.93
P0_real = phi * P0
osm_real = phi * i0 * c0 * 1000      # mOsm
# hand calculation with Celsius instead of kelvin
P_wrongC = i0 * c0 * 1000 * R * 37 / ATM
# freezing point osmometry
Kf = 1.86
dTf = Kf * 0.290
P_blood = 0.290 * 1000 * R * T0 / ATM
# protein molar mass by membrane osmometry
Tp = 298.15
hp = 0.0760             # m of solution, density taken as 1000 kg/m3
Pp = 1000 * G * hp
cp = Pp / (R * Tp)      # mol/m3
mass_c = 20.0           # kg/m3 (2.00 g in 100.0 mL)
Mp = mass_c / cp        # kg/mol
assert 60 < Mp < 70
dTf_prot = Kf * (cp / 1000)
P_nacl_same_mass = 2 * (mass_c / 58.44) * 1000 * R * Tp / 1e5
# reference table: NaCl solutions at 25 C, ideal i = 2
nacl_rows = ''
for gl, name in ((1, 'Fresh to slightly brackish'), (5, 'Brackish groundwater'), (10, 'Strong brackish'), (35, 'Seawater strength'), (70, 'RO brine reject')):
    cm = gl / 58.44
    pb = 2 * cm * 1000 * R * 298.15 / 1e5
    nacl_rows += f"| {gl} g/L ({name}) | {cm:.4f} mol/L | {2*cm*1000:.0f} mOsm/L | {pb:.2f} bar |\n"

edit('chemistry/osmotic-pressure', date=U, phrase='osmotic pressure calculator',
     intro=("Osmotic pressure is the pressure that must be applied to a solution to stop pure water flowing into it through a semipermeable membrane. "
            "This osmotic pressure calculator applies the van 't Hoff relation π = iMRT to the particle count, molarity and absolute temperature.\n\n"
            "Biology students, pharmacists preparing intravenous fluids and engineers sizing reverse osmosis pumps use it to compare a solution with blood, seawater or brine."),
     replace=[('## Worked example \u2014 saline at body temperature', '## Worked example: saline at body temperature'),
              ('''## Finding molar mass of proteins

Osmotic pressure can measure molar masses of large molecules: M = mass ÷ (Π × V ÷ RT). Even dilute protein solutions give measurable pressures.''',
               f'''## Finding molar mass of proteins

Osmotic pressure can measure molar masses of large molecules: M = mass ÷ (π × V ÷ RT). Even dilute protein solutions give measurable pressures.

Suppose 2.00 g of a purified protein is dissolved to make 100.0 mL of solution at 25 °C, and in a membrane osmometer the solution column rises {hp*100:.2f} cm above the pure water side. Taking the solution density as 1.00 g/cm³:

- π = ρ g h = 1000 × 9.80665 × {hp:.4f} = **{Pp:.1f} Pa**
- Particle concentration = π ÷ RT = {Pp:.1f} ÷ (8.314 × 298.15) = **{cp:.4f} mol/m³**
- Mass concentration = 2.00 g ÷ 0.1000 L = 20.0 g/L = 20.0 kg/m³
- M = 20.0 ÷ {cp:.4f} = **{Mp:.1f} kg/mol**, or about {Mp*1000:,.0f} g/mol, close to haemoglobin

The same 20 g/L of NaCl would give about {P_nacl_same_mass:.1f} bar, over 2,000 times more, because each gram contains far more particles. The protein would lower the freezing point by only {dTf_prot*1000:.2f} mK, which no routine instrument can read, so membrane osmometry is the practical method for macromolecules.''')],
     body_add=f'''
## The default result in every unit

With the default inputs the calculator works in SI units: c = 0.15 mol/L = 150 mol/m³ and T = 37 + 273.15 = 310.15 K, so RT = {RT0:.1f} J/mol.

- π = 2 × 150 × {RT0:.1f} = **{P0:,.0f} Pa** = {P0/1000:.1f} kPa
- = **{P0/ATM:.3f} atm** = {P0/1e5:.3f} bar = {P0_psi:.1f} psi = {P0_mmHg:,.0f} mmHg

That pressure would hold up a column of water about {h_water:.0f} m tall, which shows how strongly a membrane pulls water towards dissolved salt. In real 0.15 M NaCl the ions do not act fully independently: the osmotic coefficient is about {phi}, so the measured value is nearer {P0_real/ATM:.2f} atm, equivalent to about {osm_real:.0f} mOsm/L. That is why 0.9% saline sits close to plasma (275 to 295 mOsm/kg) even though the ideal formula gives slightly more.

## How osmotic pressure is measured in practice

Hospital and research labs rarely measure π directly. A freezing point osmometer supercools a sample of a few tens to a few hundred microlitres and reads the depression, ΔT<sub>f</sub> = K<sub>f</sub> × osmolality with K<sub>f</sub> = 1.86 K·kg/mol for water. Normal serum at 290 mOsm/kg freezes at about −{dTf:.3f} °C, and converting that osmolality with π = c R T gives {P_blood:.2f} atm at body temperature. Vapour pressure osmometers work on the same particle count through the dew point, and membrane osmometers, which do read π as a liquid head, are used for polymers and proteins.

## Ideal osmotic pressure of salt solutions at 25 °C

Values use i = 2 and molarity from NaCl at 58.44 g/mol. They set the minimum pressure a reverse osmosis pump must exceed before any permeate flows.

| NaCl content | Molarity | Osmolarity | Ideal π |
|---|---|---|---|
{nacl_rows}
Natural seawater measures about 27 bar rather than the ideal 29.7 bar because of its osmotic coefficient and mix of ions. As water is removed the brine concentrates, so an RO train has to work against the reject concentration, not the feed.

## Common mistakes

- **Using the Celsius number in a hand calculation.** Putting 37 in place of 310.15 K gives {P_wrongC:.3f} atm, about eight times too low. The calculator converts for you, but written work must use kelvin.
- **Pairing R = 8.314 with mol/L.** That R needs mol/m³, so multiply molarity by 1000, or use R = 0.08206 L·atm/(mol·K) to get atm directly.
- **Treating i as an exact whole number.** Ion pairing makes the effective factor for NaCl about 1.86 at physiological strength and smaller still in strong brines.
- **Counting solutes that cross the membrane.** Urea, ethanol and glycerol pass through cell membranes, so they raise osmolarity without raising tonicity; only impermeant solutes pull water.
- **Applying π = iMRT to concentrated solutions.** The relation is a dilute limit; above about 1 mol/L use molality and measured osmotic coefficients.
''',
     faq_add=[('How do clinical labs measure osmolality?',
               f'Most use a freezing point osmometer. The freezing point falls by 1.86 K for each osmol/kg, so serum at 290 mOsm/kg freezes at about −{dTf:.3f} °C, and the instrument converts that reading back to mOsm/kg.'),
              ("Why does a urea solution as concentrated as blood still make red cells burst?",
               'Urea crosses the red cell membrane, so it equalises on both sides and exerts no lasting osmotic pull. A 0.3 mol/L urea solution is isosmotic with blood but behaves as hypotonic, and water enters the cells until they lyse.')])

# ================================================================ Combined gas law
P1, V1, T1, P2, T2 = 101.325, 10.0, 25 + 273.15, 200.0, 60 + 273.15
V2 = P1 * V1 * T2 / (T1 * P2)
assert abs(V2 - 5.661) < 0.001
fP = P1 / P2
fT = T2 / T1
n_s = P1 * 1000 * V1 / 1000 / (R * T1)
V2_wrongC = P1 * V1 * 60 / (25 * P2)
V2_gauge = P1 * V1 * T2 / (T1 * (P2 + 101.325))
V_stp = V2 * P2 / 100 * 273.15 / T2
assert abs(V_stp - V1 * P1 / 100 * 273.15 / T1) < 1e-9
# weather balloon to about 10 km in the standard atmosphere
Vb1, Pb1, Tb1, Pb2, Tb2 = 5.00, 101.325, 288.15, 26.44, 223.15
Vb2 = Vb1 * Pb1 * Tb2 / (Tb1 * Pb2)
# spirometry: BTPS to STPD
Vbt, Pb, Pw = 5.00, 101.325, 6.27
V_stpd = Vbt * (Pb - Pw) / 101.325 * 273.15 / 310.15
# reference grid: 10 L at 101.325 kPa and 25 C
grid = ''
for p in (50, 101.325, 200, 500):
    cells = ' | '.join(f"{P1*V1*(t+273.15)/(T1*p):.2f} L" for t in (0, 25, 60, 100))
    grid += f"| {p:g} kPa | {cells} |\n"

edit('chemistry/combined-gas-law', date=U, phrase='combined gas law calculator',
     intro=("The combined gas law links pressure, volume and absolute temperature for a fixed amount of gas moving between two states, merging the laws of Boyle, Charles and Gay-Lussac. "
            "This combined gas law calculator solves P₁V₁/T₁ = P₂V₂/T₂ for whichever value is missing.\n\n"
            "Chemistry students, lab technicians correcting gas volumes to standard conditions and engineers working with compressors, balloons and gas meters use it to predict a new volume or pressure."),
     replace=[('''V₂ = 101.325 × 10 × 333.15 ÷ (298.15 × 200) = **5.66 L**''',
               f'''V₂ = 101.325 × 10 × 333.15 ÷ (298.15 × 200) = **{V2:.2f} L**

It helps to split the answer into two factors. The pressure ratio P₁ ÷ P₂ = {fP:.4f} roughly halves the volume, and the temperature ratio T₂ ÷ T₁ = {fT:.4f} expands it again by about 12%, so V₂ = 10 × {fP:.4f} × {fT:.4f} = {V2:.3f} L. The sample holds n = P₁V₁ ÷ (R T₁) = {n_s:.3f} mol throughout, but the combined law never needs that number because it cancels between the two states.'''),
              ('''## Common errors

- Using **gauge pressure** instead of absolute.
- Using **°C instead of kelvin**.
- Mixing units \u2014 keep P₁ and P₂ in the same unit, and V₁ and V₂ in the same unit. The calculator handles this for you.''',
               f'''## Common mistakes

- **Entering gauge pressure.** If the 200 kPa final pressure were a gauge reading, the absolute value is 301.325 kPa and the volume becomes {V2_gauge:.2f} L, not {V2:.2f} L.
- **Dividing by Celsius temperatures.** Using 25 and 60 directly gives {V2_wrongC:.2f} L, more than double the right answer, and 0 °C would mean dividing by zero.
- **Ignoring water vapour.** Gas collected over water or exhaled breath is partly H₂O, which condenses on cooling; correct the dry gas partial pressure, not the total.
- **Letting the amount of gas change.** Leaks, reactions, gas dissolving in a liquid or condensation all break the fixed n assumption; use PV = nRT for each state instead.
- **Reading the temperature too early.** A gas compressed quickly heats up and then cools towards ambient, so the pressure drifts until the gas and vessel reach the same temperature.''')],
     before='## Common mistakes',
     body_add=f'''
## Second example: a weather balloon climbing to 10 km

A sounding balloon is filled with 5.00 m³ of helium at 101.325 kPa and 15 °C. Near 10 km the standard atmosphere is about 26.44 kPa and −50 °C (223.15 K). If the envelope stretches freely so the gas stays at the outside pressure and cools to the outside temperature:

V₂ = 5.00 × 101.325 × 223.15 ÷ (288.15 × 26.44) = **{Vb2:.2f} m³**

The pressure drop alone would almost quadruple the volume; the cold air takes back part of that, leaving a factor of {Vb2/Vb1:.2f}. Balloons are filled loosely for exactly this reason.

## Breathing gas: BTPS to STPD

Lung function labs report volumes in two ways. Exhaled air is at body temperature, ambient pressure and saturated with water vapour (BTPS, 37 °C), while oxygen uptake is quoted dry at 0 °C and 101.325 kPa (STPD). Water vapour at 37 °C exerts 6.27 kPa, so the dry gas pressure is {Pb-Pw:.2f} kPa. A 5.00 L breath at BTPS becomes

V<sub>STPD</sub> = 5.00 × ({Pb-Pw:.2f} ÷ 101.325) × (273.15 ÷ 310.15) = **{V_stpd:.3f} L**

which is {100*(1-V_stpd/Vbt):.1f}% smaller. Gas meters, flow computers and spirometers all apply the same P and T ratios automatically.

## Final volume of 10 L of gas starting at 101.325 kPa and 25 °C

| Final pressure | 0 °C | 25 °C | 60 °C | 100 °C |
|---|---|---|---|---|
{grid}
Reading across a row shows Charles's law, down a column shows Boyle's law, and the default case sits at 200 kPa and 60 °C.
''',
     faq_add=[('How do I convert a gas volume to STP?',
               f'Treat STP as the second state: V = V₁ × (P₁ ÷ 100 kPa) × (273.15 K ÷ T₁). The default sample, {V2:.2f} L at 200 kPa and 60 °C, is {V_stp:.2f} L at IUPAC STP, the same as the original 10 L at 101.325 kPa and 25 °C, since both describe the same moles.'),
              ('Can the combined gas law be used for a closed rigid tank?',
               'Yes. With V₁ = V₂ the volumes cancel and it reduces to P₁ ÷ T₁ = P₂ ÷ T₂, so pressure rises in proportion to absolute temperature. Enter the same value for both volumes and solve for the final pressure.')])

# ================================================================ Avogadro's law
aV1, an1, an2 = 6.0, 0.25, 0.40
aV2 = aV1 * an2 / an1
Vm = aV1 / 1000 / an1 * 1000      # calculator equation with V1 in m3, gives L/mol
assert abs(aV2 - 9.6) < 1e-12 and abs(Vm - 24.0) < 1e-12
T_imp = ATM * Vm / 1000 / R
N1, N2 = an1 * NA, an2 * NA
dn = an2 - an1
dV = dn * Vm
m_He, m_CO2 = dn * 4.0026, dn * 44.009
# ammonia synthesis volume change at constant T and P
nN2, nH2 = 0.25, 0.75
x = 0.20 * nN2
n_after = (nN2 - x) + (nH2 - 3 * x) + 2 * x
V_before, V_after = (nN2 + nH2) * Vm, n_after * Vm
# sccm
mol_per_sccm = 1e-6 / 60 / 0.022414
g_min_N2 = 100 / 22414 * 28.014
ref20 = 1 - 22414 / 24055
Vm25 = R * 298.15 / ATM * 1000
assert abs(Vm25 - 24.465) < 0.001
err224 = (Vm25 / 22.414 - 1) * 100
gas_rows = ''
for name, M in (('Hydrogen (H₂)', 2.016), ('Helium (He)', 4.0026), ('Methane (CH₄)', 16.043), ('Nitrogen (N₂)', 28.014), ('Oxygen (O₂)', 31.998), ('Argon (Ar)', 39.948), ('Carbon dioxide (CO₂)', 44.009)):
    gas_rows += f"| {name} | {M:g} g/mol | {M/Vm25:.4f} g/L | {Vm25/M:.3f} L |\n"

edit('chemistry/avogadros-law', date=U, phrase="Avogadro's law calculator",
     intro=("Avogadro's law says that at fixed temperature and pressure, the volume of a gas is proportional to the number of moles it contains. "
            "This Avogadro's law calculator finds the new volume after gas is added or removed and the molar volume implied by the first state.\n\n"
            "Students use it for gas stoichiometry, and lab staff use it when filling balloons, gas bags and reactors or converting standard flow rates into moles."),
     before='## Notes',
     body_add=f'''
## Reading more from the default example

The default molar volume of {Vm:.1f} L/mol is itself a clue to the conditions. At 1 atm, V<sub>m</sub> = RT ÷ P gives T = 101325 × 0.0240 ÷ 8.314 = **{T_imp:.1f} K**, about {T_imp-273.15:.1f} °C, so the balloon is at a cool room temperature.

- Molecules before: 0.25 × 6.022 × 10²³ = **{sci(N1)}**
- Molecules after: 0.40 × 6.022 × 10²³ = **{sci(N2)}**
- Gas added: {dn:.2f} mol, which takes up {dn:.2f} × {Vm:.1f} = {dV:.1f} L, exactly the 9.6 − 6.0 L increase

Avogadro's law cares only about moles, so those {dn:.2f} mol could be {m_He:.3f} g of helium or {m_CO2:.2f} g of carbon dioxide and the balloon would grow by the same {dV:.1f} L.

## Following a gas reaction by its volume

When gases react at constant temperature and pressure, the volume tracks the total moles. Mix 0.25 mol N₂ with 0.75 mol H₂ at the default {Vm:.1f} L/mol: the mixture fills {V_before:.1f} L. In N₂ + 3H₂ → 2NH₃ four molecules become two, so if 20% of the nitrogen reacts the gas holds {nN2-x:.2f} mol N₂, {nH2-3*x:.2f} mol H₂ and {2*x:.2f} mol NH₃, {n_after:.2f} mol in all, and shrinks to **{V_after:.1f} L**. Watching that contraction in a gas syringe or a pressure controlled reactor is a simple way to measure conversion.

## Standard flow rates are really molar flows

Mass flow controllers in labs and semiconductor fabs are set in sccm, standard cubic centimetres per minute. Because one standard volume always holds the same number of moles, 1 sccm referenced to 0 °C and 1 atm is 1 ÷ 22,414 mol per minute, or {sci(mol_per_sccm)} mol/s. A 100 sccm nitrogen flow therefore delivers {g_min_N2:.4f} g/min. Some suppliers reference 20 °C instead, which makes the same reading {ref20*100:.1f}% fewer moles, so always check the reference conditions.

## Density of common gases at 25 °C and 1 atm

With V<sub>m</sub> = {Vm25:.3f} L/mol, density is molar mass ÷ V<sub>m</sub>:

| Gas | Molar mass | Density | Volume of 1 g |
|---|---|---|---|
{gas_rows}
Every row holds the same number of molecules per litre; only the mass of each molecule changes.

## Common mistakes

- **Using 22.4 L/mol at room temperature.** At 25 °C and 1 atm the molar volume is {Vm25:.3f} L/mol, so 22.4 understates volumes by about {err224:.1f}%.
- **Assuming equal volumes have equal mass.** Equal volumes hold equal moles; a litre of CO₂ is {44.009/2.016:.1f} times heavier than a litre of H₂.
- **Counting condensed products as gas.** Water formed in combustion is liquid at room temperature and contributes almost nothing to the final gas volume.
- **Letting temperature or pressure drift.** Adding gas to a rigid vessel raises the pressure instead of the volume, and a warm reaction expands the gas before it cools.
- **Applying it to dense or easily condensed gases.** CO₂ and NH₃ deviate by about 0.5 to 1% at 1 atm and room temperature and far more at high pressure; use a real gas model there.
''',
     faq_add=[('Why do equal volumes of different gases weigh different amounts?',
               f'Equal volumes contain equal numbers of molecules, but the molecules have different masses. At 25 °C and 1 atm a litre of hydrogen weighs {2.016/Vm25:.4f} g and a litre of carbon dioxide {44.009/Vm25:.3f} g.'),
              ('What is an sccm in moles?',
               f'One standard cubic centimetre per minute referenced to 0 °C and 1 atm is 1 ÷ 22,414 mol/min, about {sci(mol_per_sccm)} mol/s. A 100 sccm nitrogen flow carries {g_min_N2:.3f} g/min.')])

# ================================================================ Van der Waals
vn, vT, vV, va, vb = 1, 25 + 273.15, 1e-3, 3.64, 0.04267
vP = vn * R * vT / (vV - vn * vb * 1e-3) - va * 0.1 * vn ** 2 / vV ** 2
vPi = vn * R * vT / vV
vZ = vP / vPi
assert abs(vP / 1e5 - 22.25) < 0.01 and abs(vPi / 1e5 - 24.79) < 0.01 and abs(vZ - 0.8977) < 0.0001
Rb = R / 100            # L bar/(mol K)
rep = vn * Rb * vT / (1 - vn * vb)
att = va * vn ** 2 / 1 ** 2
assert abs(rep - att - vP / 1e5) < 1e-9
Tc = 8 * va / (27 * Rb * vb)
Pc = va / (27 * vb ** 2)
Vc = 3 * vb
TB = va / (Rb * vb)
# CO2 at 25 C, 1 mol, different volumes
zrows = ''
for VL in (20, 10, 5, 2, 1, 0.5):
    p = Rb * vT / (VL - vb) - va / VL ** 2
    pi = Rb * vT / VL
    zrows += f"| {VL:g} L | {pi:.3f} bar | {p:.3f} bar | {p/pi:.4f} |\n"
# 2 mol in 1 L
P2mol = 2 * Rb * vT / (1 - 2 * vb) - va * 4
Z2mol = P2mol / (2 * Rb * vT)
# a in atm units entered as bar
a_atm = va / 1.01325
# air by simple mixing rules
a_air = (0.79 * math.sqrt(1.37) + 0.21 * math.sqrt(1.382)) ** 2
b_air = 0.79 * 0.0387 + 0.21 * 0.03186

edit('chemistry/van-der-waals', date=U, phrase='van der Waals calculator',
     intro=("The van der Waals equation corrects the ideal gas law for two real effects: molecules attract one another and they occupy a finite volume. "
            "This van der Waals calculator uses the constants a and b to give the real gas pressure, the ideal pressure and the compressibility factor Z.\n\n"
            "Chemistry and chemical engineering students use it to see when a gas stops behaving ideally, and engineers use it for quick estimates of dense gases such as CO₂."),
     before='## Notes',
     body_add=f'''
## What each correction does in the default case

The calculator works in SI: a = 3.64 L²·bar/mol² becomes {va*0.1:.3f} Pa·m⁶/mol², b = 0.04267 L/mol becomes {sci(vb*1e-3)} m³/mol, and V = 1 L = 0.001 m³. The two corrections pull in opposite directions:

- Excluded volume alone: n R T ÷ (V − n b) = {rep:.3f} bar, which is {100*(rep*1e5/vPi-1):.1f}% above ideal because the molecules have only {1-vb:.5f} L of free space
- Attraction: a n² ÷ V² = {att:.3f} bar subtracted from that
- Net: {rep:.3f} − {att:.3f} = **{vP/1e5:.3f} bar**, ideal **{vPi/1e5:.3f} bar**, Z = **{vZ:.4f}**

For CO₂ at this density attraction wins by a wide margin. Doubling the amount to 2 mol in the same litre doubles the excluded volume and quadruples the attraction term, giving {P2mol:.2f} bar and Z = {Z2mol:.4f}, the same state as 1 mol in 0.5 L in the table below.

## Carbon dioxide at 25 °C as it is compressed

One mole of CO₂ squeezed into smaller volumes at 25 °C:

| Volume | Ideal P | Van der Waals P | Z |
|---|---|---|---|
{zrows}
Z stays within 1% of ideal down to about 5 L, then falls quickly. CO₂ at 25 °C is below its critical temperature and condenses at about 64 bar, so pushing the volume much below 0.5 L takes the equation into the region where its cubic shape gives loops instead of a real liquid and vapour balance.

## Critical point and Boyle temperature from a and b

The same two constants predict the critical point, above which the gas cannot be liquefied by pressure alone: T<sub>c</sub> = 8a ÷ (27 R b), P<sub>c</sub> = a ÷ (27 b²) and V<sub>c</sub> = 3b. For the default CO₂ constants these give T<sub>c</sub> = **{Tc:.1f} K**, P<sub>c</sub> = **{Pc:.1f} bar** and V<sub>c</sub> = {Vc:.3f} L/mol. The measured values are 304.1 K and 73.8 bar, which agree because tabulated a and b are usually fitted to them, but the real critical volume is 0.094 L/mol, showing the model's weakness at liquid like densities. The Boyle temperature, where Z stays near 1 over a wide range of pressure, is T<sub>B</sub> = a ÷ (R b) = {TB:.0f} K in the model against roughly 715 K measured.

## Common mistakes

- **Mixing units for a.** Tables give a in L²·atm/mol², L²·bar/mol² or Pa·m⁶/mol². The CO₂ value 3.592 L²·atm/mol² is {a_atm*1.01325:.3f} L²·bar/mol²; entering an SI value such as 0.364 here would cut the attraction term tenfold.
- **Treating b as a total volume.** b is per mole, so the excluded volume is n b; with 2 mol in 1 L it is {2*vb:.4f} L, not {vb:.5f} L.
- **Using it inside the two phase region.** Below T<sub>c</sub> at high density the equation can give three volumes for one pressure or even negative pressures; those are not physical states.
- **Expecting design accuracy.** Van der Waals is qualitative near and above the critical density; use Peng Robinson, Soave Redlich Kwong or measured Z charts for engineering.
- **Using pure gas constants for a mixture.** Combine them with mixing rules, for example a<sub>mix</sub> = (Σ y<sub>i</sub>√a<sub>i</sub>)² and b<sub>mix</sub> = Σ y<sub>i</sub> b<sub>i</sub>; for 79% N₂ and 21% O₂ this gives a = {a_air:.4f} and b = {b_air:.5f}.
''',
     faq_add=[('How do I find the critical point from van der Waals constants?',
               f'Use T_c = 8a ÷ (27Rb), P_c = a ÷ (27b²) and V_c = 3b with R = 0.08314 L·bar/(mol·K). For CO₂ (a = 3.640, b = 0.04267) that gives {Tc:.1f} K, {Pc:.1f} bar and {Vc:.3f} L/mol.'),
              ('What is the Boyle temperature of a van der Waals gas?',
               f'T_B = a ÷ (R b), the temperature at which attraction and excluded volume cancel at low pressure so Z stays close to 1. For CO₂ the model gives {TB:.0f} K; the measured Boyle temperature is about 715 K.')])

# ================================================================ Activation energy
k1, eT1, k2, eT2 = 0.001, 25 + 273.15, 0.004, 45 + 273.15
r = k2 / k1
Ea = R * math.log(r) / (1 / eT1 - 1 / eT2) / 1000
assert abs(Ea - 54.67) < 0.01
EaR = Ea * 1000 / R
Ea_kcal = Ea / 4.184
Q10 = math.exp(EaR * (1 / eT1 - 1 / 308.15))
k60 = k1 * math.exp(EaR * (1 / eT1 - 1 / 333.15))
A = k1 * math.exp(EaR / eT1)
assert abs(A * math.exp(-EaR / eT2) - k2) < 1e-12
# accelerated stability: 150 days at 45 C, 40 days at 60 C to the same limit
tA, TA, tB, TB_ = 150, 318.15, 40, 333.15
Ea_s = R * math.log(tA / tB) / (1 / TA - 1 / TB_) / 1000
t25 = tA * math.exp(Ea_s * 1000 / R * (1 / 298.15 - 1 / TA))
t5 = tA * math.exp(Ea_s * 1000 / R * (1 / 278.15 - 1 / TA))
# hand mistakes
Ea_C = R * math.log(r) / (1 / 25 - 1 / 45) / 1000
Ea_log10 = R * math.log10(r) / (1 / eT1 - 1 / eT2) / 1000
# sensitivity table: true Ea, k2 read 5% high, or T2 read 0.5 K high
srows = ''
for t2c in (30, 35, 45, 75):
    T2s = t2c + 273.15
    k2t = k1 * math.exp(EaR * (1 / eT1 - 1 / T2s))
    e_k = R * math.log(1.05 * k2t / k1) / (1 / eT1 - 1 / T2s) / 1000
    e_T = R * math.log(k2t / k1) / (1 / eT1 - 1 / (T2s + 0.5)) / 1000
    srows += f"| 25 to {t2c} °C | {k2t/k1:.3f} | {e_k:.2f} kJ/mol ({100*(e_k/Ea-1):+.1f}%) | {e_T:.2f} kJ/mol ({100*(e_T/Ea-1):+.1f}%) |\n"

edit('chemistry/activation-energy', date=U, phrase='activation energy calculator',
     intro=("Activation energy is the energy barrier reacting molecules must cross, and it sets how strongly a reaction speeds up as temperature rises. "
            "This activation energy calculator applies the two-point Arrhenius equation to rate constants measured at two temperatures, or predicts a rate constant once Ea is known.\n\n"
            "Kinetics students, process chemists and stability scientists use it to compare catalysts, choose reactor temperatures and estimate shelf life from accelerated ageing tests."),
     before='## Notes',
     body_add=f'''
## What the default result tells you

The default answer, E<sub>a</sub> = **{Ea:.2f} kJ/mol** (or {Ea_kcal:.2f} kcal/mol), can be turned straight into predictions:

- E<sub>a</sub> ÷ R = {Ea*1000:,.0f} ÷ 8.314 = **{EaR:,.0f} K**, the slope magnitude of the ln k against 1/T line
- Heating from 25 °C to 35 °C multiplies k by **{Q10:.2f}**, so the old doubling rule fits this reaction well
- At 60 °C the rate constant becomes 0.001 × exp[{EaR:,.0f} × (1/298.15 − 1/333.15)] = **{k60:.4f}**, {k60/k1:.1f} times the 25 °C value
- Back calculating the pre-exponential factor gives A = k₁ × exp(E<sub>a</sub> ÷ RT₁) = {sci(A)} in the same units as k

## Second example: estimating shelf life from accelerated ageing

A drug solution loses 5% of its potency in 150 days at 45 °C and in 40 days at 60 °C. Time to the same conversion is inversely proportional to k, so k₂ ÷ k₁ = 150 ÷ 40 = {tA/tB:.2f}:

- E<sub>a</sub> = 8.314 × ln {tA/tB:.2f} ÷ (1/318.15 − 1/333.15) = **{Ea_s:.1f} kJ/mol**
- Predicted time at 25 °C = 150 × exp[(E<sub>a</sub> ÷ R)(1/298.15 − 1/318.15)] = **{t25:,.0f} days**, about {t25/365.25:.1f} years
- In a refrigerator at 5 °C the estimate stretches to {t5:,.0f} days

Stability guidelines treat such extrapolations as provisional until real time data confirm them, because a second degradation route can take over at lower temperature.

## How activation energy is measured

Rate constants come from following concentration against time at a carefully held temperature, by UV/visible absorbance, conductivity, gas evolution or chromatography. Good practice uses four or more temperatures and fits ln k against 1/T: the slope is −E<sub>a</sub> ÷ R and the scatter shows whether a single E<sub>a</sub> describes the data. Thermal analysis offers a shortcut: in the Kissinger method, differential scanning calorimetry peaks at several heating rates give E<sub>a</sub> for curing resins and decomposing solids. Temperature control matters more than people expect, as the table below shows.

## How measurement errors move the result

True E<sub>a</sub> = {Ea:.2f} kJ/mol and k₁ = 0.001 at 25 °C; each row changes one input:

| Temperature span | True k₂ ÷ k₁ | k₂ read 5% high | T₂ read 0.5 K high |
|---|---|---|---|
{srows}
A 5 K span turns small errors into large ones, while a 50 K span keeps both under about 2%.

## Common mistakes

- **Using Celsius in a hand calculation.** With 1/25 − 1/45 the default data give {Ea_C:.3f} kJ/mol, wrong by a factor of about {Ea/Ea_C:.0f}.
- **Taking log₁₀ instead of ln.** log₁₀ 4 in the formula gives {Ea_log10:.2f} kJ/mol, low by the factor 2.303; with log₁₀ the constant must be 2.303 R.
- **Entering reaction times as rate constants.** Times fall as rates rise, so uninverted times give −{Ea:.2f} kJ/mol; use 1/t or swap them.
- **Mixing J and kJ when predicting k.** E<sub>a</sub> ÷ R needs E<sub>a</sub> in J/mol; using 54.67 instead of 54,670 makes the predicted change almost vanish.
- **Comparing rates measured at different concentrations.** An initial rate depends on concentration as well as k, so both runs must start from the same composition or be converted to rate constants first.
''',
     faq_add=[('Why did I get a negative activation energy?',
               f'Usually because k₁ and k₂ are swapped or reaction times were entered without inverting them; the default data entered that way give −{Ea:.2f} kJ/mol. Genuine negative values are rare and occur in some radical recombinations and multistep reactions with a pre-equilibrium.'),
              ('How is activation energy used to estimate shelf life?',
               f'Store samples at two or more raised temperatures, find the time to a set potency loss, and get Ea from the time ratio. For a product reaching the limit in 150 days at 45 °C and 40 days at 60 °C, Ea is {Ea_s:.1f} kJ/mol and the predicted time at 25 °C is about {t25:,.0f} days.')])

print('done', len(__import__('inplace').DONE))
