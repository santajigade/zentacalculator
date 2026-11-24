"""Part C expansion (2026-11-24): 30 pages from the top of tools/upgrade-backlog.txt (priority list empty; featured electronics/led-resistor and physics/ideal-gas-law skipped). Assembled from six sections; edits applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-24), slice 1: rc-snubber, inclined-plane, decibel, rotational-kinetic-energy, spring-mass-frequency.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-24'
G = 9.80665


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- RC snubber
f0, Ca, f1, k, V, fsw = 80e6, 220e-12, 40e6, 4, 48, 200e3
Cp = Ca / ((f0 / f1) ** 2 - 1)
Lp = 1 / ((2 * math.pi * f0) ** 2 * Cp)
Z0 = math.sqrt(Lp / Cp)
Cs = k * Cp
Ps = Cs * V ** 2 * fsw
assert abs(Cp * 1e12 - 73.33) < 0.01 and abs(Z0 - 27.13) < 0.01 and abs(Ps - 0.135) < 0.001
# effect of k on loss and on the time constant
k_rows = ''
for kk in (2, 3, 4, 6):
    csk = kk * Cp
    k_rows += f"| {kk} | {csk*1e12:.0f} pF | {csk*V**2*fsw*1000:.0f} mW | {Z0*csk*1e9:.2f} ns |\n"
# peak current at each edge with the chosen 27 ohm resistor
Ipk = V / 27
# energy dumped in the loop inductance at 10 A turn off
E_L = 0.5 * Lp * 10 ** 2
# ratio sensitivity: if f1 read as 41 MHz instead of 40 MHz
Cp_err = Ca / ((f0 / 41e6) ** 2 - 1)
err_pct = (Cp_err / Cp - 1) * 100
# poor ratio: 80 to 76 MHz, 1 MHz reading error
Cp_a = Ca / ((80 / 76) ** 2 - 1)
Cp_b = Ca / ((80 / 77) ** 2 - 1)

edit('electronics/rc-snubber', date=U, phrase='RC snubber calculator',
     intro=("An RC snubber is a resistor and capacitor in series across a switch or diode that damps the high frequency ringing set off by each fast edge. "
            "This RC snubber calculator finds the parasitic capacitance and loop inductance from two ringing measurements, then sizes the resistor, capacitor and resistor power.\n\n"
            "Power electronics engineers and EMC technicians use it when bringing up converters, motor drives and flyback supplies, following this [RC snubber circuit design](https://www.instrumentationblog.in/snubber-circuit-rc-design/) method."),
     body_add=f'''
## Choosing the capacitor multiplier k

The multiplier trades damping against loss. With the default measurement (C<sub>p</sub> = {Cp*1e12:.2f} pF, R<sub>s</sub> = {Z0:.2f} Ω, 48 V at 200 kHz):

| k | C<sub>s</sub> | Resistor loss | R<sub>s</sub>C<sub>s</sub> |
|---|---|---|---|
{k_rows}
Below about k = 2 the capacitor starts to limit the damping and the ringing comes back as a smaller, slower oscillation. Above 4 the extra loss buys very little. A useful rule is that R<sub>s</sub>C<sub>s</sub> should be several times shorter than the shortest on or off time, so the capacitor fully charges and discharges every cycle.

## Measuring the ringing properly

- Use the probe tip and ground spring, not the 15 cm ground clip: the clip adds its own loop of roughly 100 nH, which rings with the probe capacitance near the frequency you are trying to measure.
- Read the frequency from several cycles of the first ringing burst after the edge, for example the time across five peaks divided by five.
- Take both readings at the same load current and input voltage, because MOSFET output capacitance falls as the drain voltage rises.
- Solder the test capacitor directly across the drain and source pins; leads of a few centimetres add inductance and spoil the ratio.

## Why the 2:1 frequency drop matters

With a 2:1 drop, reading f<sub>1</sub> as 41 MHz instead of 40 MHz changes C<sub>p</sub> to {Cp_err*1e12:.1f} pF, an error of {err_pct:.1f}%. If the test capacitor were so small that the frequency only fell from 80 MHz to 76 MHz, the same 1 MHz reading error (77 MHz) would move C<sub>p</sub> from {Cp_a*1e12:.0f} pF to {Cp_b*1e12:.0f} pF. A big frequency shift makes the method robust.

## Peak current and energy

When the switch turns on, the charged snubber capacitor discharges through R<sub>s</sub>, so with a 27 Ω part the peak current is about 48 ÷ 27 = **{Ipk:.2f} A** for a few nanoseconds. That pulse flows through the MOSFET too and adds slightly to its turn on loss. For comparison, a 10 A current through the {Lp*1e9:.2f} nH loop stores ½ L I² = **{E_L*1e9:.0f} nJ** at turn off, which is the energy the snubber has to absorb to stop the overshoot.

## Common mistakes

- **Measuring with a long ground lead**, which reads the probe resonance instead of the circuit resonance.
- **Using a wirewound resistor.** Its inductance can be larger than the loop inductance being damped.
- **Placing the snubber far from the device**, so the snubber loop has its own inductance and rings at a new frequency.
- **Sizing the resistor for average power only.** The {Ps:.3f} W average comes as {Ipk:.1f} A pulses; pick a pulse rated part and at least twice the average rating.
- **Forgetting the capacitor voltage rating.** It sees the full switched voltage plus the overshoot, so a 100 V part is the minimum for a 48 V rail.
''',
     faq_add=[('Can an RC snubber reduce the efficiency of a converter?',
               f'Yes. The resistor dissipates C V² f every cycle, {Ps:.3f} W in the default 48 V, 200 kHz example. At high voltage or high switching frequency this loss can reach watts, so a lower k, a better layout or an RCD snubber may be a better choice.'),
              ('Where should the snubber go, across the MOSFET or the diode?',
               'Across the device whose node rings: in a synchronous buck that is usually the low side MOSFET, and in a flyback the secondary rectifier. Measure the ringing on each device and snub the one with the highest overshoot.')])

# ---------------------------------------------------------------- Inclined plane
m, th, mu = 10, math.radians(30), 0.2
Fp = m * G * math.sin(th)
N = m * G * math.cos(th)
Ff = mu * N
a = G * (math.sin(th) - mu * math.cos(th))
Fu = m * G * (math.sin(th) + mu * math.cos(th))
assert abs(Fp - 49.03) < 0.01 and abs(a - 3.205) < 0.001 and abs(Fu - 66.02) < 0.01
# slide 2 m from rest
L = 2.0
v_end = math.sqrt(2 * a * L)
t_end = math.sqrt(2 * L / a)
h = L * math.sin(th)
v_nofric = math.sqrt(2 * G * h)
W_fric = Ff * L
# ramp work comparison: lift 500 mm with 10 kg
h2 = 0.5
ramp_rows = ''
for deg in (10, 20, 30, 45):
    t = math.radians(deg)
    Ld = h2 / math.sin(t)
    F = m * G * (math.sin(t) + mu * math.cos(t))
    ramp_rows += f"| {deg}° | {Ld:.2f} m | {F:.1f} N | {F*Ld:.1f} J |\n"
W_lift = m * G * h2
repose = {mm: math.degrees(math.atan(mm)) for mm in (0.1, 0.3, 0.5, 0.8)}

edit('physics/inclined-plane', date=U, phrase='inclined plane calculator',
     intro=("An inclined plane is a flat surface set at an angle, where gravity splits into a pull along the slope and a push into the surface. "
            "This inclined plane calculator resolves those forces, adds friction, and gives the sliding acceleration and the push needed to move a load up at steady speed.\n\n"
            "Physics students use it for homework and exam checks, while engineers and riggers use it to size ramps, conveyors and winches for moving loads up a slope."),
     replace=[('''## Example

A 10 kg block on a 30° slope with μ = 0.2:''', '''## Worked example

A 10 kg block on a 30° slope with μ = 0.2 (g = 9.80665 m/s², sin 30° = 0.5, cos 30° = 0.8660):''')],
     body_add=f'''
### Following the block down the slope

If the block starts from rest and slides {L:.0f} m along the incline at {a:.3f} m/s², it reaches v = √(2 a L) = **{v_end:.2f} m/s** after t = √(2 L ÷ a) = **{t_end:.2f} s**. It has dropped {h:.1f} m vertically, and without friction it would arrive at √(2 g h) = {v_nofric:.2f} m/s. The difference is the {W_fric:.1f} J that friction turned into heat over the {L:.0f} m (friction force {Ff:.2f} N × {L:.0f} m).

## Trading force for distance on a ramp

A ramp lowers the force but not the work. Raising the same 10 kg load by 0.5 m with μ = 0.2:

| Ramp angle | Ramp length | Push force | Work done |
|---|---|---|---|
{ramp_rows}
Lifting straight up needs {m*G:.1f} N and {W_lift:.1f} J. Every ramp needs less force, but friction makes the total work higher, and the shallowest ramp wastes the most because the load rubs over the longest distance.

## Measuring the friction coefficient

Put the block on a board and raise one end slowly until it just starts to slide. The angle at that moment gives the static coefficient, μ<sub>s</sub> = tan θ. Keep tilting until the block slides at a steady speed after a light tap: tan θ at that angle is the kinetic coefficient this calculator uses. Repose angles for a few coefficients are μ = 0.1: {repose[0.1]:.1f}°, 0.3: {repose[0.3]:.1f}°, 0.5: {repose[0.5]:.1f}° and 0.8: {repose[0.8]:.1f}°.

## Common mistakes

- **Swapping sin and cos.** The pull along the slope uses sin θ and the normal force uses cos θ; at 0° the parallel force must be zero.
- **Using the static coefficient for a sliding block.** Static friction only sets whether the block starts to move; once it slides, use the kinetic value, which is usually lower.
- **Reading a negative acceleration as motion uphill.** It means friction would stop the block; a block at rest simply stays put.
- **Entering the slope as a percentage grade.** A 30% grade is arctan 0.30 = {math.degrees(math.atan(0.3)):.1f}°, not 30°.
- **Forgetting the friction direction when pushing up.** Friction always opposes the motion, so it adds to the push uphill and reduces the pull when lowering.
''',
     faq_add=[('How long will it take an object to slide down a ramp?',
               f'From rest, t = √(2 L ÷ a) with a = g (sin θ − μ cos θ). A block on a 30° slope with μ = 0.2 takes {t_end:.2f} s to slide {L:.0f} m and reaches {v_end:.2f} m/s.'),
              ('Does a ramp reduce the work needed to lift a load?',
               f'No. It reduces the force, but friction adds work. Raising 10 kg by 0.5 m takes {W_lift:.1f} J straight up but more along any ramp with friction, for example {m*G*(math.sin(math.radians(30))+mu*math.cos(math.radians(30)))*h2/math.sin(math.radians(30)):.1f} J on a 30° ramp with μ = 0.2.')])

# ---------------------------------------------------------------- Decibel
P1, P2, V1, V2 = 1, 100, 1, 10
dbp = 10 * math.log10(P2 / P1)
dbv = 20 * math.log10(V2 / V1)
assert dbp == 20 and dbv == 20
# chain: preamp +26, cable -2.5, splitter -3.5, amp +14
chain = [('Preamplifier', 26.0), ('Cable', -2.5), ('Splitter', -3.5), ('Power amplifier', 14.0)]
total = sum(x for _, x in chain)
ratio_total = 10 ** (total / 10)
# 0.5 W into 8 ohm: voltage and dBW, dBm
Pa, R = 0.5, 8
Va = math.sqrt(Pa * R)
dBm_a = 10 * math.log10(Pa / 1e-3)
dBV_a = 20 * math.log10(Va)
dBu_a = 20 * math.log10(Va / 0.7746)
# two equal sources add 3 dB, two 80 dB sources
two = 10 * math.log10(2 * 10 ** 8)
three90 = 10 * math.log10(10 ** 9 + 10 ** 8.5)
rows_conv = ''
for dbm in (-30, 0, 10, 20, 30, 40):
    p = 1e-3 * 10 ** (dbm / 10)
    v50 = math.sqrt(p * 50)
    rows_conv += f"| {dbm} dBm | {p*1000:g} mW | {dbm-30} dBW | {v50:.4g} V |\n"

edit('physics/decibel', date=U, phrase='decibel calculator',
     intro=("A decibel is ten times the base 10 logarithm of a power ratio, so huge ranges become small numbers and gains along a signal chain simply add. "
            "This decibel calculator converts power ratios with 10 log and voltage ratios with 20 log, and works backwards from dB to a value.\n\n"
            "Audio, RF and instrumentation engineers use it for amplifier gain, cable loss and link budgets; see [decibels in electronics: dB and dBm](https://www.instrumentationblog.in/decibel-in-electronics-db-dbm/) for practical examples."),
     replace=[('''## Signal chains

In RF and audio systems, gains and losses in dB simply add, which is why engineers prefer them to multiplying ratios.''',
               f'''## Worked example with the default values

- Power: P₂ ÷ P₁ = 100 ÷ 1 = 100, and 10 × log₁₀(100) = 10 × 2 = **{dbp:.2f} dB**
- Voltage: V₂ ÷ V₁ = 10 ÷ 1 = 10, and 20 × log₁₀(10) = 20 × 1 = **{dbv:.2f} dB**

Both give 20 dB because a tenfold voltage across the same resistance delivers a hundredfold power. The two results only agree like this when both voltages are measured across equal impedances.

## Adding gains along a signal chain

| Stage | Gain |
|---|---|
''' + ''.join(f"| {n} | {g:+.1f} dB |\n" for n, g in chain) + f'''| **Total** | **{total:+.1f} dB** |

The overall power gain is 10<sup>{total/10:.1f}</sup> = {ratio_total:,.0f} times. Working the same chain with plain ratios needs four multiplications ({10**2.6:.1f} × {10**-0.25:.3f} × {10**-0.35:.3f} × {10**1.4:.2f}); in decibels it is one sum.

## From watts to dBm, dBV and dBu

An amplifier delivering {Pa} W into an {R} Ω speaker produces V = √(P R) = {Va:.2f} V RMS. That is 10 log(500 mW ÷ 1 mW) = **{dBm_a:.1f} dBm** (or {dBm_a-30:.1f} dBW), 20 log({Va:.2f} ÷ 1 V) = **{dBV_a:.2f} dBV** and 20 log({Va:.2f} ÷ 0.7746 V) = **{dBu_a:.2f} dBu**.

| Power | In mW | In dBW | Voltage across 50 Ω |
|---|---|---|---|
{rows_conv}
## Adding sound levels

Decibel levels of separate sources do not add arithmetically. Two machines at 80 dB each give 10 log(10<sup>8</sup> + 10<sup>8</sup>) = **{two:.1f} dB**, not 160 dB. A 90 dB source plus an 85 dB source gives {three90:.1f} dB, so the quieter one barely changes the total.

## How decibels are measured

RF engineers read dBm directly on spectrum analysers and power meters, audio engineers read dBu or dBFS on mixing desk meters, and sound level meters show dB SPL with A weighting (dBA) to match human hearing. In each case the instrument does the 10 log or 20 log against its own fixed reference.

## Common mistakes

- **Using 20 log for power.** Power and energy ratios use 10 log; only field quantities such as voltage, current and sound pressure use 20 log.
- **Comparing voltages across different impedances.** 1 V across 600 Ω and 1 V across 50 Ω are very different powers, so a 20 log voltage ratio is not a power ratio there.
- **Dropping the reference.** "+10 dB" is only a ratio; dBm, dBV and dBu each name a reference, and 0 dBu is 0.7746 V, not 1 V.
- **Adding dB SPL of separate sources** as plain numbers instead of adding their powers.
- **Treating 3 dB as "a bit".** It is double or half the power, which is a big change in a link budget.''')],
     faq_add=[('How do I convert dB back to a ratio?',
               'Power ratio = 10^(dB ÷ 10) and voltage ratio = 10^(dB ÷ 20). For example 13 dB is a power ratio of about 19.95 and a voltage ratio of about 4.47.'),
              ('What is the total level of two equal sound sources?',
               f'Two equal sources are 3 dB louder than one: two 80 dB machines give {two:.1f} dB. Ten equal sources add 10 dB.')])

# ---------------------------------------------------------------- Rotational kinetic energy
kk, m, r, Nrpm = 0.5, 20, 0.25, 1000
I = kk * m * r ** 2
w = 2 * math.pi * Nrpm / 60
E = 0.5 * I * w ** 2
assert abs(I - 0.625) < 1e-9 and abs(E - 3427) < 1
# same mass as ring
E_ring = 0.5 * (m * r ** 2) * w ** 2
E_sph = 0.5 * (0.4 * m * r ** 2) * w ** 2
# coast down from 1000 to 600 rpm: energy released, and average power over 2 s
w2 = 2 * math.pi * 600 / 60
dE = E - 0.5 * I * w2 ** 2
P_avg = dE / 2
# rim speed
v_rim = w * r
# rolling disc: translational part at same rim speed
E_trans = 0.5 * m * v_rim ** 2
# stopping torque: 5 N m friction, time to stop
alpha = 5 / I
t_stop = w / alpha
turns = (w ** 2 / (2 * alpha)) / (2 * math.pi)
shape_rows = ''
for nm, kf in (('Solid disc', 0.5), ('Thin ring', 1.0), ('Solid sphere', 0.4), ('Thin hollow sphere', 2 / 3)):
    Ik = kf * m * r ** 2
    shape_rows += f"| {nm} | {Ik:.4f} kg·m² | {0.5*Ik*w**2:,.0f} J |\n"

edit('physics/rotational-kinetic-energy', date=U, phrase='rotational kinetic energy calculator',
     intro=("Rotational kinetic energy is the energy a body stores by spinning, set by its moment of inertia and the square of its angular velocity. "
            "This rotational kinetic energy calculator finds the moment of inertia of a disc, ring or sphere from mass and radius, then the stored energy from rpm.\n\n"
            "Mechanical engineers, students and machine designers use it to size flywheels, estimate rotor coast down, check grinding wheel energy and work out braking loads."),
     replace=[('''## Example

A 20 kg solid steel disc''', '''## Worked example

A 20 kg solid steel disc''')],
     body_add=f'''
The rim of this disc moves at ω r = 104.72 × 0.25 = **{v_rim:.2f} m/s**. If the same disc rolled along the floor at that speed, its straight line energy ½ m v² would be {E_trans:,.0f} J on top of the {E:,.0f} J of spin.

## Same mass, different shape

At 1,000 rpm with 20 kg and a 250 mm radius:

| Shape | Moment of inertia | Stored energy |
|---|---|---|
{shape_rows}
Moving the mass from a solid disc to a thin rim doubles the energy ({E_ring:,.0f} J against {E:,.0f} J) without adding a kilogram.

## Using the energy in practice

**Coast down.** If the example disc slows from 1,000 to 600 rpm, it releases {dE:,.0f} J. Delivered over 2 s that is an average of {P_avg:,.0f} W, which is how a press flywheel supplies a short punching stroke from a small motor.

**Braking.** A constant friction torque of 5 N·m gives an angular deceleration of 5 ÷ {I:.3f} = {alpha:.0f} rad/s², so the disc stops in {t_stop:.1f} s after about {turns:.0f} revolutions. All {E:,.0f} J end up as heat in the brake or bearings.

**Measuring the moment of inertia.** For irregular parts, hang the part on a thin wire (torsion pendulum) or let a known falling mass spin it up and time the acceleration, then enter I directly instead of shape, mass and radius.

## Common mistakes

- **Using rpm instead of rad/s.** E = ½ I ω² needs ω in rad/s; putting 1,000 in directly gives an answer about 91 times too large.
- **Diameter for radius.** Entering 500 mm for a 500 mm diameter disc makes I and E four times too large.
- **Treating a spoked or webbed flywheel as a solid disc.** Most of its mass sits in the rim, so it is closer to a thick ring.
- **Ignoring the shaft, hub and coupling.** On small rotors they can add a noticeable share of the total inertia.
- **Forgetting the stress limit.** Stored energy rises with speed squared, but so does rim stress; check the rated maximum speed before raising rpm to store more energy.
''',
     faq_add=[('How much energy does a flywheel release when it slows down?',
               f'The difference ½ I (ω₁² − ω₂²). The 20 kg, 250 mm disc going from 1,000 to 600 rpm releases about {dE:,.0f} J, which is why flywheels can deliver short bursts of high power.'),
              ('What is the difference between rotational and translational kinetic energy?',
               'Translational energy ½ m v² comes from the whole body moving along a path; rotational energy ½ I ω² comes from spinning about an axis. A rolling wheel has both, and they add.')])

# ---------------------------------------------------------------- Spring-mass frequency
ks, ms = 2000, 5
w = math.sqrt(ks / ms)
f = w / (2 * math.pi)
T = 1 / f
d = ms * G / ks
assert abs(w - 20) < 1e-9 and abs(f - 3.183) < 0.001 and abs(d * 1000 - 24.52) < 0.01
f_from_d = math.sqrt(G / d) / (2 * math.pi)
# double mass, double stiffness
f_2m = math.sqrt(ks / (2 * ms)) / (2 * math.pi)
f_4k = math.sqrt(4 * ks / ms) / (2 * math.pi)
# transmissibility for undamped isolator at forcing ratios
tr_rows = ''
for rr in (0.5, 1.2, 1.414, 2, 3, 5):
    Tr = 1 / abs(1 - rr ** 2)
    tr_rows += f"| {rr:g} | {rr*f:.2f} Hz | {Tr:.2f} | {('amplified' if Tr > 1.001 else 'isolated') if abs(Tr-1)>0.01 else 'no change'} |\n"
# design: machine at 25 Hz (1500 rpm) on mounts, want ratio 3 -> fn 8.33 Hz, static deflection
fn_t = 25 / 3
d_t = G / (2 * math.pi * fn_t) ** 2
# series springs
k_series = 1 / (1 / ks + 1 / ks)
f_series = math.sqrt(k_series / ms) / (2 * math.pi)
# spring mass correction: spring of 0.6 kg
f_corr = math.sqrt(ks / (ms + 0.6 / 3)) / (2 * math.pi)

edit('physics/spring-mass-frequency', date=U, phrase='spring-mass frequency calculator',
     intro=("A mass on a spring oscillates at a natural frequency fixed only by the stiffness and the mass, f = (1/2π)√(k/m). "
            "This spring-mass frequency calculator gives the natural frequency, angular frequency, period and static deflection under gravity.\n\n"
            "Mechanical and vibration engineers use it to choose isolation mounts and avoid resonance in machines, and physics students use it to check simple harmonic motion problems."),
     replace=[('''## Example

A 5 kg mass on a 2,000 N/m spring:''', '''## Worked example

A 5 kg mass on a 2,000 N/m spring (g = 9.80665 m/s²):''')],
     body_add=f'''
Check from the deflection alone: f = (1 ÷ 2π) √(9.80665 ÷ {d:.5f}) = **{f_from_d:.3f} Hz**, the same answer, which is why mount catalogues often quote deflection instead of stiffness.

Because f depends on √(k ÷ m), doubling the mass to 10 kg lowers the frequency only to {f_2m:.3f} Hz, and it takes four times the stiffness (8,000 N/m) to double it to {f_4k:.3f} Hz. Two of these springs in series give 1,000 N/m and {f_series:.3f} Hz.

## Vibration isolation with this spring

For an undamped mount the transmissibility is 1 ÷ |1 − r²|, where r is the forcing frequency divided by the natural frequency ({f:.3f} Hz here):

| Ratio r | Forcing frequency | Transmissibility | Effect |
|---|---|---|---|
{tr_rows}
Near r = 1 the response grows without limit in this ideal case; real mounts have damping that caps it, typically at 5 to 15 times. Isolation only starts above r = √2.

## Sizing a mount in practice

A fan running at 1,500 rpm (25 Hz) needs r = 3, so the target natural frequency is 25 ÷ 3 = {fn_t:.2f} Hz. Rearranging f = (1/2π)√(g/δ), the mounts must deflect δ = g ÷ (2π f)² = **{d_t*1000:.2f} mm** under the machine weight. Pick a mount whose rated load gives about that deflection, and divide the weight evenly between mounts.

To measure k on the bench, hang known weights and record the extension, or tap the loaded system and count oscillations with a phone accelerometer app; the measured frequency then gives k = m (2π f)².

## Common mistakes

- **Confusing ω and f.** ω = 20 rad/s is not 20 Hz; f is ω ÷ 2π, here {f:.3f} Hz.
- **Entering the weight in newtons as the mass.** 5 kg weighs {ms*G:.2f} N; using 49 as the mass lowers the frequency by a factor of about 3.1.
- **Ignoring the spring's own mass.** Add one third of the spring mass to m; a 0.6 kg spring moves this example to {f_corr:.3f} Hz.
- **Choosing a mount that is too stiff.** Any forcing ratio below √2 amplifies vibration instead of isolating it, and the worst case is close to r = 1.
- **Using the catalogue stiffness of rubber mounts for dynamic work.** Rubber is stiffer under vibration than in a static test, so the real natural frequency is often 10 to 40% higher.
''',
     faq_add=[('How do I choose a spring for a target natural frequency?',
               'Rearrange to k = m (2π f)². For a 5 kg mass and a target of 5 Hz, k = 5 × (2π × 5)² ≈ 4,935 N/m.'),
              ('Why does my measured frequency differ from the calculated one?',
               "Common causes are the spring's own mass (add one third of it to m), damping, extra stiffness from the mounting and the difference between static and dynamic stiffness in rubber springs.")])

print('done')

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-24), slice 2: de-broglie-wavelength, thin-lens, weight, work-and-power, wavelength-frequency.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-24'
g0 = 9.80665


def c(x, d=0):
    return f"{x:,.{d}f}"


def sci(x, d=3):
    m, e = f"{x:.{d}e}".split('e')
    e = int(e)
    sup = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
    return f"{m} × 10{str(e).translate(sup)}"


# ---------------------------------------------------------------- de Broglie wavelength
h = 6.62607015e-34
qe = 1.602176634e-19
cl = 299792458
me, mp, mn, ma = 9.1093837015e-31, 1.67262192369e-27, 1.67492749804e-27, 6.6446573357e-27
v = 1e6
p = me * v
lam = h / p
KE = 0.5 * me * v ** 2 / qe
assert abs(lam * 1e9 - 0.7274) < 1e-4 and abs(KE - 2.843) < 1e-3
lam_check = h / math.sqrt(2 * me * KE * qe)
beta = v / cl
gamma = 1 / math.sqrt(1 - beta ** 2)
rel_err = (gamma - 1) * 100
rows_same_v = ''
for name, m in (('Electron', me), ('Proton', mp), ('Neutron', mn), ('Alpha particle', ma)):
    l = h / (m * v)
    k = 0.5 * m * v * v / qe
    rows_same_v += f"| {name} | {l*1e12:,.4g} pm | {c(k) if k > 100 else f'{k:.3f}'} eV |\n"
# Davisson and Germer: 54 V electrons, nickel, d = 0.215 nm, peak at 50 degrees
V_dg = 54
lam_dg = h / math.sqrt(2 * me * qe * V_dg)
d_ni = 0.215e-9
lam_bragg = d_ni * math.sin(math.radians(50))
# velocity for 0.1 nm electron
v_01 = h / (me * 0.1e-9)
# thermal neutron
lam_n = h / (mn * 2200)

edit('physics/de-broglie-wavelength', date=U, phrase='de Broglie wavelength calculator',
     intro=("Every moving particle also behaves as a wave, and its wavelength is Planck's constant divided by its momentum, λ = h ÷ p. "
            "This de Broglie wavelength calculator gives the matter wavelength, momentum and kinetic energy of an electron, proton, neutron or alpha particle at a chosen speed.\n\n"
            "Physics students use it for quantum mechanics problems, and microscopists and crystallographers use it to judge whether an electron or neutron beam can resolve atomic spacings."),
     replace=[('''## Example

An electron (9.109 × 10⁻³¹ kg) moving at 1 × 10⁶ m/s:

- p = 9.109 × 10⁻³¹ × 10⁶ = **9.1094 × 10⁻²⁵ kg·m/s**
- λ = 6.626 × 10⁻³⁴ ÷ 9.1094 × 10⁻²⁵ = **0.7274 nm**
- KE = ½ × 9.109 × 10⁻³¹ × (10⁶)² = **2.843 eV**''',
               f'''## Worked example with the default values

An electron (m = 9.109 × 10⁻³¹ kg) moving at 1 × 10⁶ m/s:

1. Momentum p = m v = 9.109 × 10⁻³¹ × 1 × 10⁶ = **{sci(p, 4)} kg·m/s**
2. Wavelength λ = h ÷ p = 6.626 × 10⁻³⁴ ÷ {sci(p, 4)} = {sci(lam, 4)} m = **{lam*1e9:.4f} nm**
3. Kinetic energy = ½ m v² = {sci(0.5*me*v*v, 4)} J, and dividing by 1.602 × 10⁻¹⁹ J/eV gives **{KE:.3f} eV**

Check: λ = h ÷ √(2 m KE) with KE in joules gives {lam_check*1e9:.4f} nm again. The speed is only {beta*100:.2f}% of the speed of light, so the relativistic factor γ = {gamma:.7f} changes the momentum by about {rel_err:.4f}%, far below the precision shown.''')],
     body_add=f'''
## Same speed, different particles

At the default 1 × 10⁶ m/s, the heavier particles have far shorter wavelengths and far more energy:

| Particle | Wavelength | Kinetic energy |
|---|---|---|
{rows_same_v}
A proton and a neutron at the same speed have almost the same wavelength because only momentum matters, not charge.

## How matter waves are measured

The first direct proof came from the Davisson and Germer experiment in 1927. Electrons accelerated through {V_dg} V have λ = h ÷ √(2 m e V) = **{lam_dg*1e9:.4f} nm**. Scattered from a nickel crystal with a surface row spacing of 0.215 nm, they showed a strong peak at 50°, and the grating condition d sin θ = λ gives 0.215 × sin 50° = {lam_bragg*1e9:.4f} nm, within about {abs(lam_bragg-lam_dg)/lam_dg*100:.0f}% of the prediction.

Today the same idea is used every day. Electron diffraction in a transmission electron microscope reveals crystal structure, low energy electron diffraction (LEED) maps surfaces, and neutron diffraction uses reactor neutrons near 2,200 m/s ({lam_n*1e9:.3f} nm) to locate light atoms such as hydrogen that X-rays barely see. To get a 0.1 nm electron, roughly one atomic spacing, the electron needs a speed of {v_01:.3e} m/s, which you can check by clearing the velocity box and entering 0.1 nm.

## Common mistakes

- **Using the photon formula.** λ = h c ÷ E is only for light. For a particle with mass, use λ = h ÷ p or h ÷ √(2 m KE).
- **Putting energy in eV straight into the formula.** Convert eV to joules first by multiplying by 1.602 × 10⁻¹⁹, or the answer is out by a factor of about 2.5 × 10⁹.
- **Ignoring relativity at high voltage.** Above about 10 kV for electrons the non-relativistic λ is noticeably too long, as the voltage table shows.
- **Mixing up nm and pm.** 0.7274 nm is 727.4 pm; electron microscope wavelengths are normally quoted in picometres.
- **Using grams.** Masses must be in kilograms; the particle menu already supplies them in kg.
''',
     faq_add=[('Does the de Broglie wavelength depend on the charge of the particle?',
               'No. It depends only on momentum. A proton and a neutron moving at the same speed have almost identical wavelengths, even though one is charged and the other is not. Charge only matters for how you accelerate the particle.'),
              ('What wavelength did the Davisson and Germer electrons have?',
               f'Electrons accelerated through {V_dg} V have a de Broglie wavelength of about {lam_dg*1e9:.3f} nm, which matched the diffraction peak they measured from a nickel crystal.')])

# ---------------------------------------------------------------- Thin lens
f_, do_ = 10.0, 30.0


def img(f, d):
    return 1 / (1 / f - 1 / d)


di_ = img(f_, do_)
m_ = -di_ / do_
P_ = 1 / (f_ / 100)
assert abs(di_ - 15) < 1e-9 and abs(m_ + 0.5) < 1e-9 and abs(P_ - 10) < 1e-9
h_obj = 2.0
h_img = m_ * h_obj
div_rows = ''
for d in (50, 30, 20, 10, 5):
    dd = img(-10, d)
    div_rows += f"| {d} cm | {dd:.2f} cm | {-dd/d:.3f} |\n"
# Bessel displacement method, screen 50 cm from object
D = 50.0
disc = math.sqrt(D * D - 4 * D * f_)
u1, u2 = (D + disc) / 2, (D - disc) / 2
sep = u1 - u2
f_bessel = (D * D - sep * sep) / (4 * D)
assert abs(f_bessel - f_) < 1e-9
# camera focusing a 50 mm lens at 3 m
cam = img(50, 3000)

edit('physics/thin-lens', date=U, phrase='thin lens equation calculator',
     intro=("Lenses and curved mirrors form images at distances set by their focal length. "
            "This thin lens equation calculator uses 1/f = 1/dₒ + 1/dᵢ to find the image distance, magnification and lens power from the focal length and object distance, for both lenses and mirrors.\n\n"
            "Students use it for optics homework and lab reports, and photographers, optometry trainees and hobbyists use it to see where an image will form and how big it will be."),
     replace=[('| 20 cm | 20.0 cm | -1.00 | real, inverted, reduced |', '| 20 cm | 20.0 cm | -1.00 | real, inverted, same size |')],
     body_add=f'''
## Worked example with the default values

A converging lens with f = 10 cm and an object 30 cm away:

1. 1/dᵢ = 1/f − 1/dₒ = 1/10 − 1/30 = 3/30 − 1/30 = 2/30, so **dᵢ = {di_:.1f} cm** (positive, so a real image on the far side of the lens)
2. m = −dᵢ ÷ dₒ = −{di_:.0f} ÷ {do_:.0f} = **{m_:.3f}**, so the image is inverted and half size
3. P = 1 ÷ f = 1 ÷ 0.10 m = **{P_:.2f} dioptres** (the focal length must be in metres for dioptres)

A 2 cm tall object therefore gives an image {h_img:.1f} cm tall, the minus sign showing it is upside down.

## Diverging lens, f = −10 cm

A diverging lens always gives a virtual, upright, reduced image, whatever the object distance:

| Object distance | Image distance | Magnification |
|---|---|---|
{div_rows}
## Measuring the focal length of a real lens

The quickest method is to focus a distant window or tree onto a wall: the object is effectively at infinity, so the lens to wall distance is the focal length. For a better result use the displacement (Bessel) method. Fix an object and a screen D = {D:.0f} cm apart; a {f_:.0f} cm lens gives a sharp image at two positions, dₒ = {u1:.2f} cm and dₒ = {u2:.2f} cm, which are {sep:.2f} cm apart. Then f = (D² − s²) ÷ 4D = (2,500 − {sep*sep:.0f}) ÷ 200 = **{f_bessel:.1f} cm**. It only works when D is more than 4f, and it avoids measuring from the centre of a thick lens.

The same equation explains camera focusing. A 50 mm lens focused at 3 m needs dᵢ = {cam:.2f} mm, so the lens moves only {cam-50:.2f} mm forward from its infinity position.

## Common mistakes

- **Mixing sign conventions.** This calculator uses real is positive. Textbooks using the Cartesian convention write 1/f = 1/v − 1/u with u negative, so do not copy signs between the two.
- **Using centimetres for dioptres.** P = 1 ÷ f only gives dioptres with f in metres: 10 cm is 0.1 m and +10 D, not +0.1 D.
- **Putting the object exactly at the focal point.** With dₒ = f the rays leave parallel and the image distance is infinite, so the calculator cannot return a finite value.
- **Forgetting that a convex mirror is diverging.** Enter a negative focal length for car wing mirrors and shop security mirrors.
- **Applying it to thick lenses.** For thick lenses and multi element camera lenses, distances are measured from the principal planes, not from the glass surface.
''',
     faq_add=[('How do I measure the focal length of a lens at home?',
               'Focus a distant object such as a window onto a wall or sheet of paper and measure from the lens to the sharp image. Because the object is very far away, that distance is the focal length.'),
              ('Why does the image distance become infinite?',
               'When the object sits exactly at the focal point, 1/f − 1/dₒ is zero, the rays leave the lens parallel and no image forms at any finite distance. Move the object slightly inside or outside f to get a virtual or real image.')])

# ---------------------------------------------------------------- Weight
m_w = 70.0
W_e = m_w * g0
W_m = m_w * 1.62
sc_m = W_m / g0
LBF = 4.4482216152605
assert abs(W_e - 686.4655) < 1e-3
R = 6371.0
alt_rows = ''
for name, hkm in (('Sea level', 0), ('Everest summit', 8.849), ('Airliner cruise', 11), ('Edge of space (100 km)', 100),
                  ('ISS orbit', 400), ('Geostationary orbit', 35786)):
    k = (R / (R + hkm)) ** 2
    alt_rows += f"| {name} | {c(hkm*1000)+' m' if hkm < 100 else c(hkm)+' km'} | {g0*k:.3f} | {m_w*g0*k:.1f} |\n"
g_eq, g_pole = 9.780, 9.832
W_eq, W_pole = m_w * g_eq, m_w * g_pole
read_eq = W_eq / g0

edit('physics/weight', date=U, phrase='weight calculator',
     intro=("Weight is the force of gravity acting on a mass, so it changes from planet to planet while the mass itself stays the same. "
            "This weight calculator multiplies mass by the local gravity to give weight in newtons and the reading an Earth bathroom scale would show.\n\n"
            "Students use it to learn the difference between mass and weight, and engineers and science teachers use it for load calculations, space examples and scale problems."),
     replace=[('''## Worked example (70 kg person)

| Location | Weight (N) | Scale reading |
|---|---|---|
| Earth | 686 | 70 kg |
| Moon | 113 | 11.6 kg |
| Mars | 260 | 26.5 kg |
| Jupiter | 1735 | 177.0 kg |''',
               f'''## Worked example (70 kg person)

With the default 70 kg mass on Earth:

1. W = m × g = 70 × 9.80665 = **{W_e:.2f} N**, which is {W_e/LBF:.1f} lbf
2. Equivalent scale reading = W ÷ 9.80665 = **{m_w:.0f} kg**, as expected on Earth

Choose the Moon instead and the weight drops to 70 × 1.62 = **{W_m:.1f} N**. The same Earth calibrated scale divides by 9.80665 and shows **{sc_m:.2f} kg**, although the person still has 70 kg of mass.'''),
              ('| Earth | 9.81 | 687 | 70.0 |', '| Earth | 9.81 | 686 | 70.0 |')],
     body_add=f'''
## Weight at altitude

Gravity falls with the square of the distance from Earth's centre, g = g₀ × (R ÷ (R + h))², with R = 6,371 km. For the same 70 kg person:

| Location | Height | g (m/s²) | Weight (N) |
|---|---|---|---|
{alt_rows}
Even at geostationary height the weight is not zero; satellites stay up because they are falling around the Earth, not because gravity has vanished.

## How weight is measured in practice

A spring scale or electronic scale measures force. Most electronic platforms use a strain gauge [load cell](https://www.instrumentationblog.in/load-cell-working-principle/) whose output is proportional to the force on it, and the display divides by an assumed g to show kilograms. That is why commercial scales are calibrated with test masses at their place of use. A 70 kg person weighs {W_eq:.1f} N at the equator (g ≈ {g_eq}) and {W_pole:.1f} N near the poles (g ≈ {g_pole}). A scale set up with standard gravity would read {read_eq:.2f} kg at the equator. A beam balance compares two masses directly, so it reads the same anywhere, even on the Moon.

## Common mistakes

- **Quoting weight in kilograms.** In physics, weight is a force in newtons; 70 kg is the mass, {W_e:.0f} N is the weight.
- **Confusing lb and lbf.** A 70 kg mass is {m_w/0.45359237:.1f} lb of mass, and on Earth it weighs {W_e/LBF:.1f} lbf; the two numbers only match under standard gravity.
- **Multiplying a scale reading by g twice.** The scale reading is already a mass equivalent; multiply it by 9.80665 once to get newtons.
- **Using Earth's g on another planet.** The Moon's 1.62 m/s² gives a weight about one sixth of Earth's; picking the right location matters more than the decimals.
- **Expecting zero weight in orbit.** At 400 km, gravity is still about {(R/(R+400))**2*100:.0f}% of the surface value.
''',
     faq_add=[('How do I convert newtons to pounds-force?',
               f'Divide by 4.448. A {W_e:.1f} N weight is {W_e/LBF:.1f} lbf. To go the other way, multiply pounds-force by 4.448 to get newtons.'),
              ('Does my weight change with altitude?',
               f'Yes, slightly. At an airliner cruising height of 11 km gravity is about {(1-(R/(R+11))**2)*100:.2f}% lower, so a 70 kg person weighs about {m_w*g0*(1-(R/(R+11))**2):.1f} N less than at sea level.')])

# ---------------------------------------------------------------- Work and power
F, d, t = 500.0, 10.0, 20.0
W = F * d
P = W / t
HPM = 745.69987158227
HPMET = 735.49875
assert W == 5000 and P == 250
vel = d / t
kwh = W / 3.6e6
kcal = W / 4184
lift_rows = ''
mL, hL = 100.0, 10.0
WL = mL * g0 * hL
for tt in (60, 30, 10, 5, 2):
    lift_rows += f"| {tt} s | {c(WL/tt)} W | {WL/tt/HPM:.2f} hp |\n"
Fcar, vcar = 600.0, 25.0
Pcar = Fcar * vcar

edit('physics/work-and-power', date=U, phrase='work and power calculator',
     intro=("Work is done when a force moves something through a distance, and power is how fast that work is done. "
            "This work and power calculator finds work in joules from force and distance, then power in watts or horsepower from the time taken, and solves for whichever value you leave blank.\n\n"
            "Students use it for mechanics problems, and engineers, coaches and DIY builders use it to size motors, compare machines and estimate human effort."),
     body_add=f'''
## Checking the default answer with P = F × v

The default case moves {d:.0f} m in {t:.0f} s, an average speed of {vel:.1f} m/s. Power can also be written as force times speed: P = {F:.0f} N × {vel:.1f} m/s = **{F*vel:.0f} W**, the same as {W:,.0f} J ÷ {t:.0f} s. In horsepower that is {P/HPM:.3f} mechanical hp or {P/HPMET:.3f} metric hp (PS). The {W:,.0f} J of work equals {kwh:.6f} kWh or {kcal:.2f} kcal, a reminder of how small a joule is.

The P = F × v form is handy for vehicles. A car at {vcar:.0f} m/s (90 km/h) pushing against {Fcar:.0f} N of drag and rolling resistance needs {Pcar/1000:.0f} kW at the wheels just to hold its speed.

## Power to lift 100 kg by 10 m

Lifting {mL:.0f} kg through {hL:.0f} m always takes {mL:.0f} × 9.80665 × {hL:.0f} = {c(WL)} J of work; only the power changes with time:

| Time taken | Power | Horsepower |
|---|---|---|
{lift_rows}
This is how a hoist or lift motor is sized: work from the load and height, power from the required speed, then divide by the drive efficiency.

## How power is measured

Engine and motor power is measured on a dynamometer, which loads the shaft and records torque and speed (P = torque × angular speed). Cyclists use crank or pedal power meters with strain gauges, and sports labs use the stair climb test shown below. For electrical loads, a plug in energy meter reads watts directly, though that is input power, not mechanical output.

## Common mistakes

- **Counting distance that is not along the force.** Carrying a bag across a level floor does almost no work against gravity, because the lifting force is vertical and the motion is horizontal.
- **Entering mass instead of force.** A 50 kg load needs about {50*g0:.0f} N to lift; typing 50 into the force box understates the work by a factor of 9.8.
- **Using minutes for time.** Power in watts needs time in seconds; 20 minutes is 1,200 s.
- **Mixing horsepower types.** Mechanical hp is {HPM:.1f} W, metric hp (PS) is {HPMET:.1f} W, and electrical hp is 746 W.
- **Confusing W for work with W for watts.** Work is in joules; the watt is the unit of power, one joule per second.
''',
     faq_add=[('How many joules are in a kilowatt hour?',
               f'One kilowatt hour is 3,600,000 J (1,000 W for 3,600 s). The default {W:,.0f} J of work is only {kwh:.5f} kWh.'),
              ('How is power related to force and speed?',
               f'For a steady push, power equals force times speed in the direction of the force, P = F v. {F:.0f} N at {vel:.1f} m/s is {F*vel:.0f} W.')])

# ---------------------------------------------------------------- Wavelength and frequency
fq = 1e8
lam_d = cl / fq
assert abs(lam_d - 2.99792458) < 1e-12
FT = 0.3048
T_ns = 1 / fq * 1e9
dip = lam_d / 2
dip_prac = dip * 0.95
media = (('Air, 20 °C', 343), ('Water', 1481), ('Steel', 5960))
med_rows = ''
for name, vv in media:
    med_rows += f"| {name} | {vv:,} m/s | {vv/1000*100:.1f} cm |\n"
vf_rows = ''
for name, vf in (('Free space', 1.0), ('Foam PE coax', 0.85), ('Solid PE coax (RG58, RG213)', 0.66), ('PTFE coax', 0.70)):
    vf_rows += f"| {name} | {vf:.2f} | {lam_d*vf:.3f} m |\n"
lam_mw = cl / 2.45e9
T_air = 30
v_air30 = 331.3 + 0.606 * T_air
lam_glass = 500 / 1.5

edit('physics/wavelength-frequency', date=U, phrase='wavelength calculator',
     intro=("For any wave, speed equals frequency times wavelength, v = f λ. "
            "This wavelength calculator converts frequency to wavelength and back for light and radio in vacuum and for sound in air, water and steel.\n\n"
            "Radio amateurs and RF engineers use it to cut antennas and feed lines, audio and acoustics designers use it for room and speaker work, and students use it for wave problems."),
     body_add=f'''
## Worked example with the default values

The default is a 100 MHz radio signal in vacuum:

1. λ = c ÷ f = 299,792,458 ÷ 100,000,000 = **{lam_d:.4f} m**, or {lam_d/FT:.2f} ft
2. The period is T = 1 ÷ f = **{T_ns:.0f} ns** per cycle
3. A half wave dipole for this frequency is λ ÷ 2 = {dip:.3f} m from tip to tip; real dipoles are cut about 5% shorter, close to {dip_prac:.2f} m, because the wire ends add capacitance

## The same 1 kHz tone in different media

Frequency is set by the source and does not change when a wave crosses into another medium; the wavelength does:

| Medium | Wave speed | Wavelength at 1 kHz |
|---|---|---|
{med_rows}
## Wavelength inside a cable

Radio waves travel slower in coaxial cable than in air. The ratio is the velocity factor, and a quarter wave matching section must be cut to the shorter wavelength:

| Medium | Velocity factor | Wavelength at 100 MHz |
|---|---|---|
{vf_rows}
## Measuring wavelength in practice

For sound, a resonance tube or a pair of microphones on an oscilloscope shows the distance between points in phase. For microwaves, a classic kitchen check is to remove the turntable, heat a plate of chocolate briefly and measure between melted spots: they are half a wavelength apart, about {lam_mw/2*100:.1f} cm for a 2.45 GHz oven. RF engineers measure frequency with a counter or spectrum analyser and calculate the wavelength, while optical wavelengths are measured with a spectrometer and a diffraction grating.

## Common mistakes

- **Typing MHz or GHz as Hz.** The frequency box is in hertz, so 2.4 GHz must be entered as 2,400,000,000.
- **Using 343 m/s at every temperature.** The speed of sound in air is about 331.3 + 0.606 T m/s, so at {T_air} °C it is {v_air30:.1f} m/s and every wavelength is about {(v_air30/343-1)*100:.1f}% longer.
- **Cutting coax to the free space wavelength.** Multiply by the cable's velocity factor first, or a stub for 100 MHz will be far too long.
- **Forgetting refractive index for light.** Inside glass with n = 1.5, 500 nm light has a wavelength of {lam_glass:.0f} nm, while its colour and frequency stay the same.
''',
     faq_add=[('Does frequency change when a wave enters another medium?',
               'No. The frequency is fixed by the source, so when the wave slows down in a new medium its wavelength gets shorter in proportion to the speed.'),
              ('What is the wavelength of 100 MHz inside a coaxial cable?',
               f'Multiply the free space wavelength by the velocity factor. Solid polyethylene coax with a factor of 0.66 gives {lam_d*0.66:.2f} m instead of {lam_d:.2f} m.')])

if __name__ == '__main__':
    from inplace import DONE, body_words
    for cid in DONE:
        print(cid, body_words(cid))

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-24), slice 3: rc-time-constant, pendulum, liquid-thermal-expansion, lorentz-force,
parallel-plate-capacitor. Numbers computed here from each page's default inputs and equations.
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-24'
G0 = 9.80665

# ---------------------------------------------------------------- RC time constant
R, C = 10e3, 100e-6
tau = R * C
t5 = 5 * tau
fc = 1 / (2 * math.pi * tau)
assert abs(tau - 1) < 1e-12 and abs(fc - 0.159155) < 1e-5
Vs = 12.0
v_rows = ''
for t in (0.5, 1, 2, 3, 5):
    v_rows += f"| {t:g} s | {Vs*(1-math.exp(-t/tau)):.2f} V | {Vs*math.exp(-t/tau):.2f} V |\n"
t9 = -tau * math.log(1 - 9 / Vs)
# source resistance of 1 k in series
tau_src = (R + 1e3) * C
# electrolytic -20/+20 %
tau_lo, tau_hi = tau * 0.8, tau * 1.2
# common parts table
tc_rows = ''
for (rl, rv) in (('1 kΩ', 1e3), ('10 kΩ', 10e3), ('100 kΩ', 100e3), ('1 MΩ', 1e6)):
    cells = []
    for cv in (1e-9, 100e-9, 1e-6, 100e-6):
        t = rv * cv
        if t < 1e-3:
            cells.append(f"{t*1e6:g} µs")
        elif t < 1:
            cells.append(f"{t*1e3:g} ms")
        else:
            cells.append(f"{t:g} s")
    tc_rows += f"| {rl} | " + ' | '.join(cells) + ' |\n'
# 1 k and 100 nF filter
fc_filter = 1 / (2 * math.pi * 1e3 * 100e-9)

edit('physics/rc-time-constant', date=U, phrase='rc time constant calculator',
     intro=("The time constant τ = RC sets how fast a capacitor charges or discharges through a resistor, as explained in "
            "[RC and RL time constants explained](https://www.instrumentationblog.in/rc-and-rl-time-constant-explained/). "
            "This RC time constant calculator gives τ, the 5τ settling time and the matching cut-off frequency.\n\n"
            "Electronics students, hobbyists and design engineers use it to size timing networks, sensor filters, switch debouncers and "
            "[RC snubbers](https://www.instrumentationblog.in/snubber-circuit-rc-design/) without working through exponentials by hand."),
     replace=[('''## Charging curve

| Time | Charge (% of supply) |
|---|---|
| 1τ | 63.2% |
| 2τ | 86.5% |
| 3τ | 95.0% |
| 4τ | 98.2% |
| 5τ | 99.3% |

The same percentages apply in reverse when discharging. RC networks are used for timers, debouncing switches and simple signal filters.''',
               f'''## Time constants for common part values

Kilohms multiplied by microfarads give milliseconds, which makes quick estimates easy:

| Resistance | 1 nF | 100 nF | 1 µF | 100 µF |
|---|---|---|---|---|
{tc_rows}''')],
     body_add=f'''
## Voltages for the default circuit on a 12 V supply

With 10 kΩ and 100 µF (τ = {tau:g} s, cut-off {fc:.4f} Hz) connected to a {Vs:g} V source:

| Time after switching | Charging voltage | Discharging voltage (from 12 V) |
|---|---|---|
{v_rows}
To reach 9 V while charging takes t = −1 s × ln(1 − 9 ÷ 12) = **{t9:.3f} s**. If the 12 V source itself has 1 kΩ of internal resistance, the real time constant is (10 kΩ + 1 kΩ) × 100 µF = {tau_src:.1f} s, so every time in the table stretches by 10%.

## Measuring τ in practice

Drive the circuit with a slow square wave and watch the capacitor on an oscilloscope. Measure the time from the step to 63.2% of the final value, or for a discharge the time to fall to 36.8%. A quicker way is to measure the 10% to 90% rise time, which equals 2.197τ for a single RC stage. A general purpose electrolytic with ±20% tolerance means the default network can measure anywhere from {tau_lo:.1f} s to {tau_hi:.1f} s, so check the real part before trimming resistor values.

## Common mistakes

- **Mixing unit prefixes.** 10 kΩ × 100 µF is 1 s, but 10 kΩ × 100 nF is 1 ms; a slip of a thousand is the most common error.
- **Treating 5τ as exactly full.** At 5τ the capacitor is at 99.3%; precision sample and hold circuits wait 7τ to 9τ for 12 bit accuracy.
- **Forgetting the source and load resistance.** Driver output resistance adds to R, and a load across the capacitor forms a divider that lowers the final voltage and shortens τ.
- **Assuming the cut-off frequency removes the signal.** A 1 kΩ and 100 nF low pass filter cuts off at {fc_filter:.0f} Hz but only attenuates by 3 dB there and by 20 dB per decade above.
- **Ignoring leakage in large electrolytics.** With megohm resistors, leakage current can stop the capacitor ever reaching the expected voltage.
''',
     faq_add=[('Why do kilohms times microfarads give milliseconds?',
               'Because kΩ is 10³ and µF is 10⁻⁶, so their product is 10⁻³ seconds. For example 4.7 kΩ with 10 µF gives 47 ms.'),
              ('How can I measure the time constant with an oscilloscope?',
               'Apply a step or square wave and read the time for the capacitor voltage to reach 63.2% of its final value, or measure the 10% to 90% rise time and divide it by 2.197.')])

# ---------------------------------------------------------------- Pendulum
L = 1.0


def per(L, g=G0):
    return 2 * math.pi * math.sqrt(L / g)


T = per(L)
f = 1 / T
assert abs(T - 2.0064) < 1e-4
t20 = 20 * T
# timing error of 0.2 s over 20 swings
T_err = (t20 + 0.2) / 20
g_err = 4 * math.pi ** 2 * L / T_err ** 2
# length measured to the bottom of a 5 cm bob instead of the centre: 2.5 cm too long
T_long = per(L + 0.025)
# uniform rod pivoted at one end, 1 m
T_rod = 2 * math.pi * math.sqrt(2 * L / (3 * G0))
bodies = (('Equator (sea level)', 9.780), ('Standard gravity', G0), ('Poles (sea level)', 9.832),
          ('Moon', 1.62), ('Mars', 3.71), ('Jupiter (cloud tops)', 24.79))
g_rows = ''
for name, g in bodies:
    g_rows += f"| {name} | {g:.3f} m/s² | {per(L, g):.3f} s | {g / math.pi ** 2:.3f} m |\n"
T_moon = per(L, 1.62)
daily_eq = (per(1.0, 9.780) / per(1.0, G0) - 1) * 86400

edit('physics/pendulum', date=U, phrase='pendulum period calculator',
     intro=("A simple pendulum swings with a period set by its length and the local gravity, not by the mass of the bob. "
            "This pendulum period calculator finds the period and frequency from the length, or the length needed for a chosen period.\n\n"
            "Physics students use it to check lab results and measure g, clock restorers use it to regulate pendulums, and engineers use it for swinging loads such as crane hooks and hanging signs."),
     replace=[('''## Period vs length

| Length | Period |
|---|---|
| 0.25 m | 1.00 s |
| 0.5 m | 1.42 s |
| 1 m | 2.01 s |
| 2 m | 2.84 s |
| 4 m | 4.01 s |

Four times the length doubles the period. This is why grandfather clocks are tall \u2014 a ~1 m pendulum ticks once per second.''',
               f'''## The same 1 m pendulum on other worlds

The period scales with 1 ÷ √g, so the same pendulum is a simple gravity meter. The last column is the length that would beat seconds (a 2 s period) in that gravity:

| Location | g | Period of a 1 m pendulum | Seconds pendulum length |
|---|---|---|---|
{g_rows}
Even on Earth the difference matters to a clock: a seconds pendulum regulated for standard gravity loses about {abs(daily_eq):.0f} seconds a day if moved to the equator.''')],
     body_add=f'''
## Lab worked example

Using the calculator default of L = 1 m and g = {G0} m/s²: T = 2π × √(1 ÷ {G0}) = **{T:.4f} s** and f = **{f:.4f} Hz**. Twenty full swings should therefore take {t20:.2f} s. If your stopwatch reads 0.2 s long over those 20 swings, the measured period becomes {T_err:.4f} s and g = 4π² × 1 ÷ {T_err:.4f}² = {g_err:.3f} m/s², an error of {abs(g_err-G0)/G0*100:.1f}%. Timing more swings divides that error further.

## Measuring a real pendulum

Measure the length from the pivot point to the centre of mass of the bob, not to its bottom. Use a light, inextensible string, keep the amplitude below about 10°, and start timing as the bob passes the lowest point, where it moves fastest and the instant is easiest to judge. A light gate or a phone camera at 240 frames per second beats hand timing.

## Common mistakes

- **Measuring to the bottom of the bob.** With a 5 cm bob that adds 2.5 cm to L and the predicted period becomes {T_long:.4f} s instead of {T:.4f} s.
- **Timing one way swings.** The period is a full there and back cycle; a one way swing is half of it.
- **Counting the first pass as one.** Say zero when you start the stopwatch, otherwise you time one swing fewer than you count.
- **Using the formula for a rigid rod.** A uniform 1 m rod pivoted at one end has T = 2π√(2L ÷ 3g) = {T_rod:.3f} s, not {T:.3f} s, because its mass is spread along its length.
- **Large release angles.** At 45° the period is already 4% longer than the formula gives.
''',
     faq_add=[('What is the period of a 1 m pendulum on the Moon?',
               f'About {T_moon:.2f} s, because lunar gravity is only about 1.62 m/s². The period grows with 1 ÷ √g, so it is about 2.5 times the Earth value.'),
              ('Why does a swinging rod have a shorter period than a string pendulum of the same length?',
               f'Its mass is spread along its length, so its centre of oscillation sits at two thirds of the length. A 1 m uniform rod swings with a period of about {T_rod:.2f} s instead of {T:.2f} s.')])

# ---------------------------------------------------------------- Liquid thermal expansion
b, V0, T1, T2 = 950e-6, 1000.0, 15.0, 35.0
dT = T2 - T1
dV = b * V0 * dT
V1 = V0 + dV
assert abs(dV - 19) < 1e-9 and abs(V1 - 1019) < 1e-9
a_steel = 12e-6
dV_app = (b - 3 * a_steel) * V0 * dT
rho15 = 745.0
rho35 = rho15 / (1 + b * dT)
mass = rho15 * V0 / 1000
fill = 1 / (1 + b * dT) * 100
# blocked in water, near 20 C: compressibility 4.6e-10 1/Pa
kap_w = 4.6e-10
dp_bar = 207e-6 / kap_w / 1e5
# fill table
fill_rows = ''
for name, bb in (('Water (20 °C)', 207e-6), ('Diesel', 830e-6), ('Petrol', 950e-6), ('Ethanol', 1090e-6)):
    fill_rows += f"| {name} | " + ' | '.join(f"{100/(1+bb*d):.2f}%" for d in (10, 20, 30, 40)) + ' |\n'

edit('physics/liquid-thermal-expansion', date=U, phrase='liquid thermal expansion calculator',
     intro=("Liquids expand much more than solids when they warm up, so a full tank or a closed pipe needs space or relief for the extra volume. "
            "This liquid thermal expansion calculator applies ΔV = β V₀ ΔT to give the volume increase, final volume and percentage change.\n\n"
            "Tank designers, fuel depot staff, plumbers and process engineers use it to set safe fill levels, size expansion vessels and correct delivered fuel volumes to a reference temperature."),
     body_add=f'''
## Beyond the basic result: the default petrol tank

The default case is 1,000 L of petrol (β = 950 × 10⁻⁶/K) warming from 15 °C to 35 °C, giving **{dV:.1f} L** of extra volume and **{V1:,.0f} L** in total. Three follow on figures matter in practice:

- **Apparent expansion in a steel tank.** The tank grows too, by about 3 × 12 × 10⁻⁶ per K, so the level rises by the equivalent of (950 − 36) × 10⁻⁶ × 1,000 × {dT:g} = **{dV_app:.2f} L**, not {dV:.0f} L.
- **Density falls, mass stays.** {mass:.0f} kg of petrol at {rho15:.0f} kg/m³ is still {mass:.0f} kg at 35 °C, but the density drops to {rho15:.0f} ÷ {1+b*dT:.3f} = **{rho35:.1f} kg/m³**. That is why fuel is sold at a 15 °C reference volume.
- **Maximum fill.** To leave room for the 20 K rise, the tank may be filled to at most 1 ÷ {1+b*dT:.3f} = **{fill:.2f}%** of its capacity at 15 °C, before any safety margin.

## Maximum fill level for a temperature rise

Fill fraction that just reaches 100% after the rise, ignoring tank expansion:

| Liquid | +10 K | +20 K | +30 K | +40 K |
|---|---|---|---|---|
{fill_rows}
Regulations for road tankers and storage tanks usually add a margin on top, often filling to 95% or 97% at most.

## Where it is used

Hot water systems are fitted with expansion vessels sized from the system volume and the temperature rise. Liquid pipelines that can be isolated between two valves get thermal relief valves, because a trapped liquid that warms in the sun cannot expand. Custody transfer meters apply volume correction factors from API or ISO tables, which are a more exact form of the same β calculation.

## Common mistakes

- **Using the linear coefficient α.** For a liquid only the volumetric β exists; for a solid β ≈ 3α.
- **Dropping the 10⁻⁶.** Enter β as 950, not 0.00095, because the field is already in units of 10⁻⁶ per kelvin.
- **Using water's 20 °C value over a large range.** Water heated from 20 °C to 80 °C expands about 2.7%, roughly 6 times what β = 207 × 10⁻⁶ predicts; use densities instead.
- **Taking a β quoted per °F as per K.** A coefficient per °F must be multiplied by 1.8 before use here.
- **Ignoring pressure in a closed space.** A trapped liquid does not expand, it builds pressure, see the FAQ below.
''',
     faq_add=[('How much pressure builds up in a full, closed pipe when the liquid warms?',
               f'A lot. For water near 20 °C, β divided by the compressibility of about 4.6 × 10⁻¹⁰ per Pa gives roughly {dp_bar:.1f} bar for every 1 °C rise in a rigid pipe. Pipe stretch reduces it somewhat, but a few degrees can exceed the rating of the pipe, which is why thermal relief valves are fitted.'),
              ('How full can I fill a tank to allow for expansion?',
               f'Divide 1 by (1 + β ΔT). For petrol and a 20 K rise that is {fill:.1f}% of the tank volume, and most rules then add a margin so tanks are filled to about 95%.')])

# ---------------------------------------------------------------- Lorentz force
e, u = 1.602176634e-19, 1.66053906660e-27
z, v, B, mu_, I, Lc = 1, 2e6, 0.5, 1.007276, 5.0, 0.2
F = e * v * B
r = mu_ * u * v / (e * B)
fcy = e * B / (2 * math.pi * mu_ * u)
Fc = B * I * Lc
assert abs(F - 1.6022e-13) < 1e-17 and abs(r * 1000 - 41.76) < 0.01 and abs(fcy / 1e6 - 7.623) < 0.001
# electron same speed and field
me = 0.00054858
r_e = me * u * v / (e * B)
fc_e = e * B / (2 * math.pi * me * u)
# angle 30 deg
F30 = F * math.sin(math.radians(30))
r30 = r * math.sin(math.radians(30))
pitch30 = mu_ * u * v * math.cos(math.radians(30)) / (e * B) * 2 * math.pi
# isotope separation, 1e5 m/s, 0.5 T
v_i = 1e5
r12 = 12 * u * v_i / (e * B)
r13 = 13.00335 * u * v_i / (e * B)
dsep = 2 * (r13 - r12)
# earth field electron cyclotron
fc_e_earth = e * 50e-6 / (2 * math.pi * me * u)
# conductor table
c_rows = ''
for Ii in (1, 10, 100, 1000):
    c_rows += f"| {Ii:,} A | " + ' | '.join(f"{BB*Ii:.3g} N" for BB in (50e-6, 0.1, 0.5, 1.5)) + ' |\n'

edit('physics/lorentz-force', date=U, phrase='lorentz force calculator',
     intro=("A charge moving through a magnetic field is pushed sideways, at right angles to both its velocity and the field, and a current carrying wire feels the same push. "
            "This Lorentz force calculator gives the force on a charge, its orbit radius and cyclotron frequency, and the force on a conductor.\n\n"
            "Physics students, motor and actuator designers and people working with mass spectrometers or beam lines use it to check forces, path radii and frequencies quickly."),
     body_add=f'''
## Default case taken further

The default proton (2 × 10⁶ m/s across 0.5 T) gives F = **{F/1e-13:.4f} × 10⁻¹³ N**, r = **{r*1000:.2f} mm** and f<sub>c</sub> = **{fcy/1e6:.3f} MHz**, and the 0.2 m wire with 5 A feels **{Fc:.2f} N**. Changing one thing at a time shows how the formulas behave:

- **Swap in an electron** (0.00054858 u, charge −1) at the same speed: the force has the same size but the opposite direction, the radius shrinks to {r_e*1e6:.1f} µm and the cyclotron frequency rises to {fc_e/1e9:.1f} GHz.
- **Tilt the velocity to 30° from the field**: the force halves to {F30/1e-14:.4f} × 10⁻¹⁴ N and the circle radius halves to {r30*1000:.2f} mm, while the particle drifts along B by {pitch30*1000:.0f} mm per turn, tracing a helix.
- **Double the speed**: the force and the radius double, but the cyclotron frequency does not change, which is what lets a cyclotron use a fixed RF frequency.

## Mass spectrometer example

Singly charged carbon ions of 12 u and 13.00335 u enter a 0.5 T field at 1 × 10⁵ m/s. Their radii are {r12*1000:.2f} mm and {r13*1000:.2f} mm, so after a half circle they land {dsep*1000:.2f} mm apart on the detector. Heavier ions bend less, which is how isotopes are separated and identified.

## Force on a 1 m conductor

| Current | Earth field, 50 µT | 0.1 T | 0.5 T | 1.5 T |
|---|---|---|---|---|
{c_rows}
Fields of 0.5 T to 1.5 T are typical of the air gap in motors and loudspeakers; the Earth's field produces only tiny forces even on heavy cables.

## Common mistakes

- **Measuring the angle from the wrong reference.** θ is between the velocity (or current) and the field; motion parallel to B gives zero force.
- **Entering mass in kilograms.** The mass field is in atomic mass units, so a proton is 1.007276, not 1.67 × 10⁻²⁷.
- **Forgetting the sign of the charge.** The size of the force uses |q|, but an electron is pushed the opposite way to a proton.
- **Using a length of wire outside the field.** Only the length actually inside the field region counts in F = B I L.
- **Applying it near light speed.** Above about 0.1c use the relativistic momentum, or the radius comes out too small.
''',
     faq_add=[('Does the magnetic force do work on a moving charge?',
               'No. The force is always perpendicular to the velocity, so it changes the direction of motion but not the speed or kinetic energy. Only an electric field can speed a charge up.'),
              ("What is the cyclotron frequency of an electron in the Earth's magnetic field?",
               f'About {fc_e_earth/1e6:.1f} MHz in a 50 µT field. Electrons spiralling around field lines in the upper atmosphere emit and absorb radio waves near this frequency.')])

# ---------------------------------------------------------------- Parallel plate capacitor
e0 = 8.8541878128e-12
er, A, d, V = 1.0, 100e-4, 1e-3, 100.0
Cp = e0 * er * A / d
Q = Cp * V
W = 0.5 * Cp * V ** 2
Ef = V / d / 1e6
assert abs(Cp * 1e12 - 88.54) < 0.01 and abs(W * 1e6 - 0.4427) < 1e-4
# design 1 nF with 0.1 mm PTFE
A_need = 1e-9 * 1e-4 / (e0 * 2.1)
# two layer dielectric: 0.5 mm glass (6) + 0.5 mm air
C_two = e0 * A / (0.5e-3 / 6 + 0.5e-3 / 1)
E_air_two = V / (0.5e-3 + 0.5e-3 / 6) * 1 / 1e6  # field in air layer, kV/mm
# level probe: half immersed in oil er 2.2
C_half = e0 * A / d * (0.5 * 2.2 + 0.5 * 1)
gap_rows = ''
for gmm in (0.1, 0.5, 1, 2, 5):
    cg = e0 * A / (gmm * 1e-3)
    gap_rows += f"| {gmm:g} mm | {cg*1e12:,.1f} pF | {3*gmm:g} kV | {0.5*cg*(3e3*gmm)**2*1e6:,.1f} µJ |\n"
W_max = 0.5 * Cp * 3000 ** 2

edit('physics/parallel-plate-capacitor', date=U, phrase='parallel plate capacitor calculator',
     intro=("Two conducting plates separated by an insulator form a capacitor set only by the plate area, the gap and the dielectric. "
            "This parallel plate capacitor calculator gives the capacitance, charge, stored energy and field; see [what capacitance is](https://www.instrumentationblog.in/what-is-capacitance/).\n\n"
            "Students, sensor designers and PCB engineers use it to estimate plane capacitance, design touch pads and check probes for "
            "[capacitance level measurement](https://www.instrumentationblog.in/capacitance-level-measurement/)."),
     body_add=f'''
## Designing for a target value

To get 1 nF with a 0.1 mm PTFE film (εr = 2.1), rearrange to A = C d ÷ (ε<sub>0</sub> ε<sub>r</sub>) = 1 × 10⁻⁹ × 0.0001 ÷ (8.854 × 10⁻¹² × 2.1) = **{A_need*1e4:.1f} cm²**, a square about {math.sqrt(A_need)*1000:.0f} mm on a side. Thinner film or a higher εr shrinks the area in direct proportion.

## Air gap, capacitance and breakdown

For the default 100 cm² plates in dry air, taking a breakdown strength of about 3 kV/mm:

| Gap | Capacitance | Approximate breakdown voltage | Energy at breakdown |
|---|---|---|---|
{gap_rows}
Halving the gap doubles C but also halves the voltage the gap can hold, so the maximum stored energy falls. At the default 1 mm gap the plates hold at most about {W_max*1e3:.2f} mJ before arcing.

## Two dielectrics in one gap

If the 1 mm gap is half glass (εr = 6) and half air, the layers act as two capacitors in series: C = ε<sub>0</sub> A ÷ (d<sub>1</sub>/ε<sub>r1</sub> + d<sub>2</sub>/ε<sub>r2</sub>) = **{C_two*1e12:.1f} pF**, not the average of the two. The air layer then carries most of the voltage, with a field of {E_air_two:.3f} kV/mm at 100 V instead of 0.1 kV/mm, which is why air pockets in insulation are where partial discharge starts.

## How it is used in level sensing

A probe with plates half immersed in oil (εr ≈ 2.2) works like two capacitors in parallel, one in oil and one in air: C = 88.54 pF × (0.5 × 2.2 + 0.5 × 1) = **{C_half*1e12:.1f} pF**. The transmitter measures that change and scales it linearly from empty (88.5 pF) to full ({e0*A/d*2.2*1e12:.1f} pF). Conductive liquids such as water need an insulated probe, because the liquid itself becomes one plate.

## Common mistakes

- **Converting area wrongly.** 100 cm² is 0.01 m², not 0.1 m²; an area error is squared compared with a length error.
- **Using total plate area.** Only the overlapping area counts, so offset plates have less capacitance.
- **Ignoring fringing for wide gaps.** When the gap is more than about a tenth of the plate width, the real value is noticeably higher than the formula.
- **Taking εr as constant.** Water, ceramics and many plastics change permittivity with frequency and temperature.
- **Averaging two dielectrics.** Layers stacked across the gap are in series, layers side by side are in parallel.
''',
     faq_add=[('How do I calculate capacitance with two dielectric layers in the gap?',
               f'Treat the layers as capacitors in series: C = ε₀ A ÷ (d₁/εr₁ + d₂/εr₂). For 100 cm² plates with 0.5 mm of glass and 0.5 mm of air this gives about {C_two*1e12:.0f} pF.'),
              ('Why does capacitance increase when the plates are closer?',
               'The same voltage across a smaller gap gives a stronger field, which holds more charge on each plate. Capacitance is inversely proportional to the gap, so halving it doubles C.')])

print('done')

# ======================================================================= SECTION _expand_c4.py
"""Expand (2026-11-24), slice 4: density, stokes-law, drag-force, force, pressure.
Numbers computed here from each page's default inputs and equations (g0 = 9.80665). Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-24'
g0 = 9.80665
LBF = 4.4482216152605


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- density
m, V_L = 7.85, 1.0
rho = m / (V_L / 1000)
assert abs(rho - 7850) < 1e-9
units_rows = (f"| kg/m³ | {c(rho)} |\n"
              f"| g/cm³ (= kg/L = t/m³) | {rho/1000:.2f} |\n"
              f"| lb/ft³ | {rho*0.0624279606:.1f} |\n"
              f"| lb/in³ | {rho*0.0624279606/1728:.4f} |\n"
              f"| lb/US gal | {rho*0.00834540445:.2f} |\n")
# Archimedes weighing of a ring
w_air, w_wat, rho_w = 10.50, 9.50, 0.998
V_ring = (w_air - w_wat) / rho_w
rho_ring = w_air / V_ring
# brass block from dimensions
Vb = 50 * 40 * 30 * 1e-9
rho_b = 0.510 / Vb
assert abs(rho_b - 8500) < 1e-6
# bulk vs grain density of sand
bulk, grain = 1600, 2650
porosity = 1 - bulk / grain

edit('physics/density', date=U, phrase='density calculator',
     intro=("Density is mass per unit volume, a measure of how tightly matter is packed. "
            "This density calculator finds density and specific gravity from mass and volume, or mass or volume from a known density, in kg/m³, g/cm³ or lb/ft³.\n\n"
            "Students, lab technicians and process engineers use it to identify materials, predict floating, and turn volume into mass; see [what specific gravity is](https://www.instrumentationblog.in/what-is-specific-gravity/) "
            "and [Coriolis density measurement](https://www.instrumentationblog.in/coriolis-density-measurement/)."),
     replace=[('''## Common densities

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
''', f'''## The default result in other units

The default {m} kg in {V_L:.0f} L gives {c(rho)} kg/m³. The same density in the units you will meet on data sheets:

| Unit | Value |
|---|---|
{units_rows}
A quick check: g/cm³, kg/L and specific gravity are numerically the same (to within the 0.2% difference between water at 4 °C and 20 °C), and kg/m³ is always 1,000 times larger.
''')],
     body_add=f'''
## Second example: a block measured with a ruler

A brass block measures 50 mm × 40 mm × 30 mm and weighs 510 g on a kitchen scale.

1. Volume = 0.050 × 0.040 × 0.030 = {Vb*1e6:.0f} × 10⁻⁶ m³ ({Vb*1e6:.0f} cm³)
2. Density = 0.510 kg ÷ {Vb:.6f} m³ = **{c(rho_b)} kg/m³**, specific gravity {rho_b/1000:.2f}

That sits inside the 8,400 to 8,700 kg/m³ range of common brasses, so the part is very likely brass rather than bronze or plated steel.

## How density is measured in practice

- **Archimedes weighing.** Weigh the object in air, then hanging in water. The loss of weight equals the mass of displaced water. A ring that reads {w_air:.2f} g in air and {w_wat:.2f} g in water has a volume of {w_air - w_wat:.2f} ÷ {rho_w} = {V_ring:.3f} cm³ and a density of **{rho_ring:.2f} g/cm³**, close to pure silver (10.49) and above sterling silver (about 10.36).
- **Hydrometer.** A weighted glass float sinks until it displaces its own mass of liquid; the stem scale reads density or specific gravity directly. Used for battery acid, brewing and fuels.
- **Pycnometer.** A glass bottle of exactly known volume is weighed empty and full, which gives liquid density to about 0.01%.
- **Oscillating U-tube and Coriolis meters.** The natural frequency of a vibrating tube falls as the fluid inside gets heavier, so the instrument reports density continuously in a pipeline.

## Common mistakes

- **Forgetting the litre factor.** 1 L is 0.001 m³, so 7.85 kg in 1 L is 7,850 kg/m³, not 7.85 kg/m³.
- **Confusing bulk and particle density.** Dry sand in a heap is about {c(bulk)} kg/m³ while each quartz grain is {c(grain)} kg/m³; the {porosity*100:.0f}% difference is air between the grains. Use bulk density for silos and trucks, particle density for settling.
- **Entering weight in newtons as mass.** A scale reading in kg is already mass; a force gauge reading in N must be divided by 9.81 first.
- **Ignoring temperature for liquids.** Diesel loses roughly 0.07% of its density per °C, so a fuel density quoted at 15 °C does not match a hot tank reading.
- **Measuring hollow or porous parts by their outside size.** A casting with internal voids gives a lower apparent density than the solid alloy.
''',
     faq_add=[('Why is ice less dense than water?',
               'Water molecules lock into an open hexagonal lattice when they freeze, which takes about 9% more space. Ice is about 917 kg/m³ against 1,000 kg/m³ for liquid water, so it floats.'),
              ('How can I check if a metal object is solid gold?',
               f'Weigh it in air and in water and divide the air weight by the loss. Pure gold gives about 19.3 g/cm³ and 18 carat yellow gold roughly 15 to 16 g/cm³; a result near 10.5 g/cm³, like the {rho_ring:.2f} g/cm³ ring above, points to silver.')])

# ---------------------------------------------------------------- stokes law
d, rp, rf, mu = 50e-6, 2650, 998, 1.0e-3
v = (rp - rf) * g0 * d ** 2 / (18 * mu)
Re = rf * v * d / mu
Fd = 3 * math.pi * mu * d * v
assert abs(v - 0.00225008) < 1e-7 and abs(Re - 0.1123) < 1e-4
Wsub = (rp - rf) * g0 * math.pi / 6 * d ** 3
assert abs(Wsub - Fd) < 1e-15
t_tank = 3.0 / v  # 3 m deep clarifier
# temperature effect, water properties (viscosity mPa s, density)
trows = ''
for T, muT, rfT in ((5, 1.519, 1000.0), (10, 1.306, 999.7), (20, 1.002, 998.2), (30, 0.797, 995.7), (40, 0.653, 992.2)):
    vv = (rp - rfT) * g0 * d ** 2 / (18 * muT * 1e-3)
    trows += f"| {T} °C | {muT:.3f} mPa·s | {vv*1000:.2f} mm/s | {1/vv/60:.1f} min |\n"
# falling ball viscometer
db, rb, rg = 2e-3, 7800, 1260
L, t = 0.100, 9.89
vb = L / t
mu_g = (rb - rg) * g0 * db ** 2 / (18 * vb)
Re_b = rg * vb * db / mu_g
# dust in air
vd = (2000 - 1.2) * g0 * (10e-6) ** 2 / (18 * 1.8e-5)
t_room = 2.5 / vd

edit('physics/stokes-law', date=U, phrase="stokes' law calculator",
     intro=("Stokes' law describes how fast a small sphere sinks or rises through a viscous fluid once drag balances its weight and buoyancy. "
            "This Stokes' law calculator gives the terminal settling velocity, the drag force and the particle Reynolds number that tells you whether the law applies.\n\n"
            "Water treatment engineers size settling tanks with it, lab staff run falling ball tests for [viscosity measurement](https://www.instrumentationblog.in/viscosity-measurement-explained/), "
            "and formulators use it to predict creaming in emulsions."),
     body_add=f'''
## Sizing a settling tank from the result

The default {d*1e6:.0f} µm sand grain settles at {v*1000:.3f} mm/s. In a clarifier 3 m deep it needs 3 ÷ {v:.6f} = {t_tank:.0f} s, about **{t_tank/60:.0f} minutes**, to reach the floor from the surface. Designers turn that velocity into a surface overflow rate: any particle that settles faster than the flow rate divided by the tank plan area is captured. For {v*1000:.2f} mm/s that is {v*3600:.2f} m³ per m² of tank area per hour, so a flow of 50 m³/h needs at least {50/(v*3600):.1f} m² of surface, before a safety factor of 1.5 to 2 for turbulence and short circuiting.

## Temperature changes the answer

Viscosity of water falls quickly as it warms, and settling speed rises in proportion. The same 50 µm quartz grain:

| Water temperature | Viscosity | Settling velocity | Time to fall 1 m |
|---|---|---|---|
{trows}
A plant that settles well in summer can carry fines over the weir in winter for this reason alone.

## Measuring viscosity with a falling ball

A {db*1000:.0f} mm steel ball ({c(rb)} kg/m³) dropped in glycerol ({c(rg)} kg/m³) takes {t} s to fall between two marks {L*1000:.0f} mm apart, so v = {vb*1000:.2f} mm/s. Rearranged, μ = (ρp − ρf) g d² ÷ (18 v) = **{mu_g:.2f} Pa·s**, and Re = {Re_b:.3f}, safely in the Stokes range. Start timing only after the ball has fallen a few centimetres so it is at terminal speed, and use a tube at least 10 times the ball diameter, or apply a wall correction, because nearby walls slow the ball.

## Common mistakes

- **Mixing up mPa·s and Pa·s.** Water is 1.0 mPa·s, which is 0.001 Pa·s; entering 1 Pa·s makes the velocity 1,000 times too small.
- **Using radius in the 18 μ form.** The equation here uses diameter. The radius form is v = 2 (ρp − ρf) g r² ÷ (9 μ); swapping one for the other gives a factor of 4 error.
- **Skipping the Reynolds check.** Above Re ≈ 1 the true drag is higher than 3πμdv, so Stokes' law overstates the speed of coarse sand and gravel.
- **Treating flocs as solid grains.** A floc of fine particles holds a lot of water, so its effective density may be only 1,010 to 1,100 kg/m³.
- **Forgetting that air is a fluid too.** A 10 µm dust particle (2,000 kg/m³) in air settles at only {vd*1000:.1f} mm/s, taking about {t_room/60:.0f} minutes to fall 2.5 m, which is why fine dust hangs in a room.
''',
     faq_add=[('Why does fine dust stay in the air so long?',
               f'Settling speed falls with the square of size. A 10 µm dust particle settles at about {vd*1000:.1f} mm/s and takes roughly {t_room/60:.0f} minutes to fall 2.5 m in still air, and any air current easily outruns that.'),
              ('Does Stokes\' law work for bubbles and droplets?',
               'Approximately. Small rigid looking bubbles and droplets follow it, but clean fluid droplets with an internally circulating surface can move up to 1.5 times faster (the Hadamard and Rybczynski result). Surfactants usually make them behave like solid spheres again.')])

# ---------------------------------------------------------------- drag force
rho_a, kmh, Cd, A = 1.225, 100, 0.30, 2.2


def drag(r, k, cd, a):
    vv = k / 3.6
    return 0.5 * r * vv * vv * cd * a, 0.5 * r * vv ** 3 * cd * a


Fd0, P0 = drag(rho_a, kmh, Cd, A)
assert abs(Fd0 - 311.92) < 0.01 and abs(P0 - 8664.5) < 0.5
srows = ''
for k in (50, 80, 100, 120, 130, 150):
    f, p = drag(rho_a, k, Cd, A)
    srows += f"| {k} km/h | {c(f, 1)} N | {p/1000:.2f} kW | {f*1e5/3.6e6:.1f} kWh |\n"
F_alt, _ = drag(1.007, kmh, Cd, A)
F_hw, _ = drag(rho_a, 120, Cd, A)
P_hw = F_hw * kmh / 3.6
Cd_meas = 400 / (0.5 * rho_a * (120 / 3.6) ** 2 * A)
F_cyc, P_cyc = drag(rho_a, 36, 0.9, 0.36)
F_tt, P_tt = drag(rho_a, 36, 0.7, 0.30)
vt = math.sqrt(2 * 80 * g0 / (rho_a * 1.0 * 0.7))

edit('physics/drag-force', date=U, phrase='drag force calculator',
     intro=("Drag is the resistance a fluid exerts on an object moving through it, and it grows with the square of speed. "
            "This drag force calculator applies the drag equation F = ½ρv²C<sub>d</sub>A to give the force and the power needed to push through air or water.\n\n"
            "Vehicle engineers, cyclists, structural designers checking wind load and instrument engineers sizing probes in a flowing pipe use it to see how speed, shape and area change resistance."),
     body_add=f'''
## How speed changes force, power and energy

For the default car (C<sub>d</sub> {Cd:.2f}, {A} m², sea level air), drag force rises with v² and drag power with v³. The last column is the energy spent on air drag alone per 100 km driven, which is force × distance:

| Speed | Drag force | Drag power | Drag energy per 100 km |
|---|---|---|---|
{srows}
At 100 km/h the car spends {Fd0*1e5/3.6e6:.1f} kWh per 100 km on air; at 130 km/h that rises to {drag(rho_a,130,Cd,A)[0]*1e5/3.6e6:.1f} kWh, because energy per distance follows the force, not the power.

## Wind, altitude and other real conditions

- **Headwind.** Drag uses speed relative to the air. Driving at 100 km/h into a 20 km/h headwind, the air speed is 120 km/h, so the force is {c(F_hw, 1)} N and the power at the wheels is {c(F_hw, 1)} × 27.78 = {P_hw/1000:.2f} kW, against {P0/1000:.2f} kW in still air.
- **Altitude.** At about 2,000 m, air density is near 1.007 kg/m³ and the same car at 100 km/h meets only {c(F_alt, 1)} N.
- **Cyclists.** An upright rider (C<sub>d</sub> 0.9, 0.36 m²) at 36 km/h needs {P_cyc:.0f} W against air; a time trial position (C<sub>d</sub> 0.7, 0.30 m²) cuts that to {P_tt:.0f} W.
- **Terminal velocity.** An 80 kg skydiver in a belly position (C<sub>d</sub> ≈ 1.0, A ≈ 0.7 m²) stops accelerating at √(2 × 80 × 9.807 ÷ (1.225 × 1.0 × 0.7)) = {vt:.1f} m/s, about {vt*3.6:.0f} km/h.

## Finding C<sub>d</sub> from a measurement

C<sub>d</sub> values come from wind tunnel balances, coast down tests (the car rolls in neutral and the deceleration is logged) or CFD. If a coast down test shows 400 N of aerodynamic force at 120 km/h on a 2.2 m² car, then C<sub>d</sub> = 400 ÷ (0.5 × 1.225 × 33.33² × 2.2) = **{Cd_meas:.3f}**. In the calculator, enter the force and clear C<sub>d</sub> to get the same result.

## Common mistakes

- **Entering km/h as if it were m/s.** The formula needs m/s; 100 km/h is 27.78 m/s. The calculator converts for you, but hand calculations often skip it and come out 13 times too high.
- **Using the wrong reference area.** A C<sub>d</sub> quoted for a wing uses plan area, a car uses frontal area; mixing them can be off by a factor of 5 or more.
- **Ignoring rolling resistance.** Drag is only part of the road load. Below about 60 km/h, tyre rolling resistance is often larger than air drag for a car.
- **Applying one C<sub>d</sub> at every Reynolds number.** A sphere drops from about 0.47 to roughly 0.1 past the drag crisis, which is why dimpled golf balls fly further.
- **Forgetting water is 800 times denser than air.** The same shape and speed in water feels about 816 times the force, so marine sensors and pipe probes see large loads at low speeds.
''',
     faq_add=[('How much fuel does air drag cost?',
               f'Air drag on the default car takes {Fd0*1e5/3.6e6:.1f} kWh of work at the wheels per 100 km at 100 km/h. Petrol engines turn roughly a quarter to a third of fuel energy into wheel work, so that is around 3 litres of petrol per 100 km for drag alone.'),
              ('Does a headwind increase drag?',
               f'Yes, because drag depends on speed relative to the air. At 100 km/h into a 20 km/h headwind the car meets {c(F_hw, 0)} N instead of {c(Fd0, 0)} N, about 44% more force.')])

# ---------------------------------------------------------------- force
mf, af = 1200, 3
Ff = mf * af
assert Ff == 3600
F_lbf = Ff / LBF
t100 = (100 / 3.6) / af
Frr = mf * g0 * 0.012
Fdr = 0.5 * 1.225 * 10 ** 2 * 0.30 * 2.2
Fengine = Ff + Frr + Fdr
T_lift = 800 * (g0 + 1)
W_lift = 800 * g0
trows_f = ''
for t in (4, 6, 8, 10, 12, 15):
    a = 100 / 3.6 / t
    trows_f += f"| {t} s | {a:.2f} m/s² | {a/g0:.2f} g | {c(mf*a)} N |\n"

edit('physics/force', date=U, phrase='force calculator',
     intro=("Newton's second law says the net force on an object equals its mass times its acceleration, F = m × a. "
            "This force calculator finds the force from mass and acceleration, or solves for mass or acceleration when the force is known, in N, kN, kgf or lbf.\n\n"
            "Students use it for mechanics problems, and engineers use it to size motors, brakes, cables and fixings that must speed up, slow down or hold a load."),
     replace=[('''## Worked example

A 1,200 kg car accelerating at 3 m/s² needs a net force of 1,200 × 3 = **3,600 N** (3.6 kN, about 809 lbf).''',
               f'''## Worked example

A {c(mf)} kg car accelerating at {af} m/s² needs a net force of {c(mf)} × {af} = **{c(Ff)} N**, which is {Ff/1000:.1f} kN or {F_lbf:.0f} lbf. At that steady rate it would reach 100 km/h (27.78 m/s) in 27.78 ÷ {af} = {t100:.2f} s.''')],
     body_add=f'''
## From net force to the force the engine must supply

The {c(Ff)} N above is what is left over to accelerate the car. At 36 km/h (10 m/s), the tyres and the air also push back:

1. Rolling resistance with C<sub>rr</sub> = 0.012: {c(mf)} × 9.807 × 0.012 = {Frr:.1f} N
2. Air drag (C<sub>d</sub> 0.30, 2.2 m²): 0.5 × 1.225 × 10² × 0.30 × 2.2 = {Fdr:.1f} N
3. Driving force at the wheels = {c(Ff)} + {Frr:.1f} + {Fdr:.1f} = **{c(Fengine, 1)} N**

So the drivetrain must deliver about {(Fengine/Ff-1)*100:.0f}% more than F = ma alone suggests, and the share grows as speed rises.

## Force for a target 0 to 100 km/h time

Assuming constant acceleration of the default {c(mf)} kg car:

| 0 to 100 km/h | Acceleration | In g | Net force |
|---|---|---|---|
{trows_f}
Real cars accelerate harder at low speed and less near the top, so these are average forces.

## Lifting: when gravity is part of the sum

For vertical motion the weight must be added. A lift car of 800 kg accelerating upward at 1 m/s² needs a cable tension of 800 × (9.807 + 1) = **{c(T_lift, 1)} N**, against {c(W_lift, 1)} N when it hangs still. That extra {c(T_lift-W_lift)} N is the F = ma part, and it is why cranes and hoists are rated with dynamic factors.

## How force is measured

Load cells are the standard tool: strain gauges bonded to a steel element change resistance as it flexes, and a bridge circuit turns that into a signal proportional to force. Spring balances and handheld force gauges do the same job mechanically for small loads, and piezoelectric sensors capture fast impacts such as a kick or a hammer blow. Force plates under a sprinter measure the push against the ground directly.

## Common mistakes

- **Using the applied force instead of the net force.** F = ma uses the sum of all forces; a 500 N push against 200 N of friction accelerates the object with 300 N.
- **Entering mass in kgf or weight in kg.** Mass is in kg; a force written as 50 kgf is 490 N.
- **Using km/h per second as m/s².** 10 km/h per second is only 2.78 m/s².
- **Leaving out the weight in vertical problems.** A lifting cable carries m (g + a), not just m a.
- **Mixing lb and lbf.** In imperial units, 1 lbf accelerates 1 lb at 32.17 ft/s², not 1 ft/s².
''',
     faq_add=[('How much force does it take to lift something while accelerating it upward?',
               f'The force is m × (g + a). An 800 kg lift car accelerating up at 1 m/s² needs {c(T_lift)} N of cable tension, {c(T_lift-W_lift)} N more than its static weight of {c(W_lift)} N.')])

# ---------------------------------------------------------------- pressure
Fp, Ap = 700, 400e-4
P = Fp / Ap
assert P == 17500
Wt = 1200 * g0 / 4
patch = Wt / 220e3
dpist = 0.050
Ar = math.pi * dpist ** 2 / 4
Fr = 6e5 * Ar
Fwrong = 6e5 * dpist ** 2

edit('physics/pressure', date=U, phrase='pressure calculator',
     intro=("Pressure is force spread over an area, P = F ÷ A, which is why sharp knives cut and wide tyres do not sink. "
            "This pressure calculator finds the pressure from a force and an area, or the force or area needed for a target pressure, in Pa, kPa, bar, psi or MPa.\n\n"
            "Students, technicians and engineers use it for hydraulics, tyres, foundations and gauges; see [absolute vs gauge pressure](https://www.instrumentationblog.in/absolute-vs-gauge-pressure/) "
            "and [Pascal's law in pressure instruments](https://www.instrumentationblog.in/understanding-pascals-law-pressure-instruments/)."),
     body_add=f'''
## Common mistakes

- **Using cm² as if it were m².** The default 400 cm² is 0.04 m²; leaving it as 400 gives 1.75 Pa instead of {c(P)} Pa, an error of 10,000 times.
- **Squaring the diameter without π ÷ 4.** A 50 mm piston has an area of π × 0.05² ÷ 4 = {Ar*1e4:.2f} cm², not 25 cm². At 6 bar the force is {c(Fr)} N; using d² alone would claim {c(Fwrong)} N.
- **Putting a mass where a force belongs.** 70 kg is not 70 N; multiply by 9.81 to get 687 N before dividing by the area.
- **Mixing gauge and absolute readings.** A tyre at 220 kPa gauge is about 321 kPa absolute; gas law calculations need the absolute value.
- **Assuming pressure depends on container shape.** In a liquid, pressure at a depth depends only on depth and density, not on how wide the vessel is (the hydrostatic paradox).

## Reverse calculation: tyre contact patch

A {c(1200)} kg car puts about {c(Wt)} N on each wheel. At 220 kPa gauge, the contact patch settles at roughly {c(Wt)} ÷ 220,000 = {patch:.5f} m², or **{patch*1e4:.0f} cm²** per tyre. Drop the pressure to 180 kPa and the patch grows to {Wt/180e3*1e4:.0f} cm², which is why soft tyres feel heavy and heat up. Sidewall stiffness carries some load too, so real patches are slightly smaller.
''',
     faq_add=[('Does the shape of the contact area change the pressure?',
               'Not for the average value. P = F ÷ A depends only on the size of the area, so 700 N on a 400 cm² square or a 400 cm² circle gives the same 17.5 kPa. Shape matters only for how the pressure is distributed, for example the peak under a sharp corner.'),
              ('What is the difference between pressure and stress?',
               'Both are force per area and use the same units. Pressure is the normal push of a fluid or a contact load and acts equally in all directions in a fluid, while stress inside a solid has a direction and can be tension, compression or shear.')])

print('done')

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-24), slice 5: resistors-series-parallel, photon-energy, projectile-motion,
kinetic-energy, simple-harmonic-motion. Numbers computed here from each page's default inputs
and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-24'
g0 = 9.80665


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- resistors in series and parallel
R = (100.0, 220.0, 470.0)
Rs = sum(R)
G = [1 / r for r in R]
Rp = 1 / sum(G)
assert Rs == 790 and abs(Rp - 59.98) < 0.01
V = 12.0
Is = V / Rs
Ps = [Is ** 2 * r for r in R]
Ip = [V / r for r in R]
Pp = [V ** 2 / r for r in R]
# 5% tolerance band
tol = 0.05
Rs_lo, Rs_hi = Rs * (1 - tol), Rs * (1 + tol)
Rp_lo, Rp_hi = Rp * (1 - tol), Rp * (1 + tol)
# n equal 1 k resistors in parallel and power share
eq_rows = ''
for n in (2, 3, 4, 5, 10):
    eq_rows += f"| {n} | {1000/n:,.1f} Ω | {1000*n/1000:,.0f} kΩ | {n*0.25:.2f} W |\n"
# drop R3 (set to 1e12)
Rp2 = 1 / (1 / 100 + 1 / 220 + 1 / 1e12)
Rs2 = 100 + 220 + 1e12

edit('physics/resistors-series-parallel', date=U, phrase='resistors in series and parallel calculator',
     intro=("Resistors in series add up, while resistors in parallel always give a total lower than the smallest one. "
            "This resistors in series and parallel calculator finds the equivalent resistance of up to three resistors both ways; see "
            "[series vs parallel circuits explained](https://www.instrumentationblog.in/series-vs-parallel-circuits-explained/) for the background.\n\n"
            "Students, hobbyists and repair technicians use it to build a value they do not have in the drawer, check a measured reading and size the power rating of each part."),
     replace=[('''## Worked example

100 Ω, 220 Ω and 470 Ω:

- Series = **790 Ω**
- Parallel = 1 ÷ (1/100 + 1/220 + 1/470) = **60.0 Ω**''',
               f'''## Worked example

With the default 100 Ω, 220 Ω and 470 Ω:

- Series: 100 + 220 + 470 = **{Rs:.0f} Ω**
- Parallel: the conductances are 1/100 = {G[0]*1000:.3f} mS, 1/220 = {G[1]*1000:.3f} mS and 1/470 = {G[2]*1000:.3f} mS. They add to {sum(G)*1000:.3f} mS, so R = 1 ÷ {sum(G):.6f} = **{Rp:.2f} Ω**

The parallel total is below the smallest resistor (100 Ω), as it must be. Adding the 470 Ω part lowers the parallel result from 68.75 Ω (100 Ω and 220 Ω alone) to {Rp:.2f} Ω but adds 470 Ω to the series total: in parallel the smallest resistor dominates, while in series the largest one does.

### Current and power at 12 V

Put the same three resistors across a 12 V supply:

| Connection | Resistor | Current | Power |
|---|---|---|---|
| Series | 100 Ω | {Is*1000:.2f} mA | {Ps[0]*1000:.1f} mW |
| Series | 220 Ω | {Is*1000:.2f} mA | {Ps[1]*1000:.1f} mW |
| Series | 470 Ω | {Is*1000:.2f} mA | {Ps[2]*1000:.1f} mW |
| Parallel | 100 Ω | {Ip[0]*1000:.1f} mA | {Pp[0]*1000:.0f} mW |
| Parallel | 220 Ω | {Ip[1]*1000:.1f} mA | {Pp[1]*1000:.0f} mW |
| Parallel | 470 Ω | {Ip[2]*1000:.1f} mA | {Pp[2]*1000:.0f} mW |

In series the largest resistor gets the most heat; in parallel the smallest one does. The 100 Ω resistor in parallel dissipates {Pp[0]:.2f} W, so a common 0.25 W part would overheat and a 2 W part is the sensible choice.''')],
     body_add=f'''
## Using only two resistors

Leave R3 at a huge value such as 1e12 Ω. The parallel result becomes {Rp2:.2f} Ω, exactly the 100 Ω and 220 Ω product over sum value, but the series total then includes the dummy 1e12 Ω, so read only the parallel answer in that case (or set R3 to 0 Ω for a two resistor series total).

## Equal resistors in parallel

Paralleling identical resistors is a cheap way to get a low value with a higher power rating. With 1 kΩ, 0.25 W parts:

| Number in parallel | Total resistance | Same parts in series | Power rating |
|---|---|---|---|
{eq_rows}
## Tolerance of the result

If all three parts are 5% types, the series total can sit anywhere from {Rs_lo:.1f} Ω to {Rs_hi:.1f} Ω and the parallel total from {Rp_lo:.2f} Ω to {Rp_hi:.2f} Ω. Combining resistors never makes the percentage tolerance worse than that of the parts, and random errors partly cancel, which is why a series string of matched parts is used in precision dividers.

## Measuring a combination with a multimeter

Switch off the power and lift one leg of a resistor before measuring it in a circuit, otherwise parallel paths through other components make the reading too low. Touching both probe tips with your fingers adds your body resistance in parallel and pulls high value readings down, which matters above about 100 kΩ.

## Common mistakes

- **Adding parallel values directly.** 100 Ω and 220 Ω in parallel is {1/(1/100+1/220):.2f} Ω, not 320 Ω; add the reciprocals, then take the reciprocal of the sum.
- **Forgetting the last reciprocal.** The sum 1/100 + 1/220 + 1/470 = {sum(G):.5f} is a conductance in siemens, not the answer in ohms.
- **Mixing Ω and kΩ.** Writing 4.7 instead of 4,700 for a 4.7 kΩ part gives a parallel result that is a thousand times too small.
- **Sizing power from the total.** The total dissipation does not tell you the share each part takes; check the hottest resistor, as in the table above.
- **Ignoring a short.** A 0 Ω link or a solder bridge across any parallel branch makes the whole combination 0 Ω.
''',
     faq_add=[('Which resistor gets hottest in a parallel circuit?',
               f'The smallest one, because every branch has the same voltage and power is V² ÷ R. At 12 V the 100 Ω resistor takes {Pp[0]:.2f} W while the 470 Ω one takes only {Pp[2]:.2f} W.'),
              ('How do I make a 60 Ω resistor from standard values?',
               f'100 Ω, 220 Ω and 470 Ω in parallel give {Rp:.2f} Ω, within 0.1% of 60 Ω. Two 120 Ω resistors in parallel give exactly 60 Ω.')])

# ---------------------------------------------------------------- photon energy
h, cc, qe, NA = 6.62607015e-34, 299792458.0, 1.602176634e-19, 6.02214076e23
lam, P = 532.0, 1e-3
fT = 299792.458 / lam
EJ = h * fT * 1e12
eV = EJ / qe
Em = EJ * 6.02214076e20
N = P / EJ
assert abs(fT - 563.52) < 0.01 and abs(eV - 2.3305) < 0.0001 and abs(N - 2.678e15) < 0.001e15
hc_eVnm = h * cc / qe * 1e9
Rideal = qe / EJ  # A/W at 100% QE
QE = 0.8
Iph = P * Rideal * QE
# Si band gap cutoff
lam_si = hc_eVnm / 1.12
resp_rows = ''
for l in (400, 532, 650, 850, 940, 1550):
    r = l / hc_eVnm
    resp_rows += f"| {l} nm | {hc_eVnm/l:.3f} eV | {r:.3f} A/W | {P/(h*cc/(l*1e-9)):.3e} |\n"
resp_rows = resp_rows.replace('e+15', ' × 10¹⁵')
# 1 W 405 nm vs 1550 nm photon count ratio
edit('physics/photon-energy', date=U, phrase='photon energy calculator',
     intro=("A photon's energy depends only on its frequency, E = hf, or equivalently on its wavelength, E = hc/λ. "
            "This photon energy calculator converts a wavelength into energy in eV and joules, frequency, energy per mole and photons emitted per second.\n\n"
            "Laser and LED engineers, photochemists and people working with "
            "[photodiodes and phototransistors](https://www.instrumentationblog.in/photodiode-vs-phototransistor-key-differences/) use it to check band gaps, detector response and photon counts."),
     replace=[('''## Example

A 532 nm green laser with 1 mW output:''', '''## Worked example

A 532 nm green laser with 1 mW output, the calculator defaults:''')],
     body_add=f'''
Each step uses the exact SI constants: f = c ÷ λ = 299,792,458 ÷ (532 × 10⁻⁹) Hz, then E = h f, then the result is divided by the elementary charge for eV and multiplied by Avogadro's number for the molar value. The shortcut 1239.84 ÷ 532 gives the same {eV:.4f} eV.

## From photons to detector current

A photodiode turns each absorbed photon into at most one electron. Its ideal responsivity is therefore the electron charge divided by the photon energy, R = q ÷ E = λ (nm) ÷ 1239.84 A/W. For the 532 nm laser:

- Ideal responsivity = 1.602 × 10⁻¹⁹ ÷ {EJ/1e-19:.4f} × 10⁻¹⁹ = **{Rideal:.3f} A/W**
- With a quantum efficiency of {QE*100:.0f}%, a typical silicon value in the green, the photocurrent from 1 mW is {P*1000:.0f} mW × {Rideal:.3f} × {QE} = **{Iph*1e6:.0f} µA**

The same 1 mW gives a larger current at longer wavelengths, because each photon carries less energy and so there are more of them:

| Wavelength | Photon energy | Ideal responsivity | Photons per second in 1 mW |
|---|---|---|---|
{resp_rows}
Silicon stops responding near {lam_si:.0f} nm, where the photon energy falls below its 1.12 eV band gap, so the 1550 nm row needs an InGaAs or germanium detector.

## How light power is measured in practice

Laser power meters use either a calibrated photodiode head, which reads in amps and divides by the responsivity at the wavelength you select, or a thermal head that absorbs the beam and measures the temperature rise. That is why a photodiode meter set to the wrong wavelength reads wrongly while a thermal head does not care. Spectrometers report wavelength directly, and this calculator converts that to energy.

## Common mistakes

- **Entering metres or micrometres in the nanometre box.** 1.55 µm must be typed as 1550, otherwise the energy is a thousand times too large.
- **Confusing photon energy with beam power.** A brighter 532 nm laser emits more photons per second; each photon still carries {eV:.3f} eV.
- **Using vacuum wavelength rules inside glass.** The photon energy is fixed by frequency; the wavelength shortens in a medium but the energy does not change.
- **Mixing kJ/mol with eV per photon.** 1 eV per photon equals about 96.49 kJ/mol, so {eV:.3f} eV is {Em:.1f} kJ/mol, not {eV:.3f} kJ/mol.
- **Assuming LED voltage equals photon energy exactly.** Real forward voltage is higher because of series resistance and the junction design.
''',
     faq_add=[('What is the responsivity of a photodiode at 532 nm?',
               f'An ideal detector gives {Rideal:.3f} A/W at 532 nm (λ in nm ÷ 1239.84). A real silicon photodiode with about 80% quantum efficiency gives roughly {Rideal*QE:.2f} A/W, so 1 mW produces about {Iph*1e6:.0f} µA.')])

# ---------------------------------------------------------------- projectile motion
v, thd = 20.0, 45.0
th = math.radians(thd)
Rr = v ** 2 * math.sin(2 * th) / g0
H = v ** 2 * math.sin(th) ** 2 / (2 * g0)
T = 2 * v * math.sin(th) / g0
vx, vy = v * math.cos(th), v * math.sin(th)
tap = vy / g0
assert abs(Rr - 40.79) < 0.01 and abs(H - 10.20) < 0.01 and abs(T - 2.884) < 0.001
ang_rows = ''
for a in (15, 30, 45, 60, 75, 90):
    t_ = math.radians(a)
    ang_rows += f"| {a}° | {v**2*math.sin(t_)**2/(2*g0):.2f} m | {2*v*math.sin(t_)/g0:.2f} s | {v*math.cos(t_):.2f} m/s |\n"
# doubling speed
R40 = 40 ** 2 * math.sin(2 * th) / g0
# 9.81 vs 9.80665 difference tiny; moon
Rmoon = v ** 2 * math.sin(2 * th) / 1.62
# height at x = 30 m
x30 = 30.0
y30 = x30 * math.tan(th) - g0 * x30 ** 2 / (2 * v ** 2 * math.cos(th) ** 2)

edit('physics/projectile-motion', date=U, phrase='projectile motion calculator',
     intro=("A thrown ball, a cricket shot or a water jet all follow a curved path called a parabola, because the horizontal speed stays steady while gravity changes the vertical speed. "
            "This projectile motion calculator gives the range, maximum height and flight time from launch speed and angle.\n\n"
            "Physics students use it to check homework, coaches and players use it to see why launch angle matters, and engineers use it for first estimates of jets and thrown objects."),
     replace=[('''## Worked example

Launched at 20 m/s and 45°:

- Range = 400 × 1 ÷ 9.81 = **40.8 m**
- Maximum height = **10.2 m**
- Flight time = **2.88 s**''',
               f'''## Worked example

Launched at the default 20 m/s and 45°, with g = 9.80665 m/s²:

1. Split the velocity: v<sub>x</sub> = 20 × cos 45° = {vx:.2f} m/s and v<sub>y</sub> = 20 × sin 45° = {vy:.2f} m/s
2. Time to the top: {vy:.2f} ÷ 9.80665 = {tap:.3f} s, so the time of flight is **{T:.3f} s**
3. Maximum height: {vy:.2f}² ÷ (2 × 9.80665) = **{H:.2f} m**
4. Range: {vx:.2f} m/s × {T:.3f} s = **{Rr:.2f} m**, the same as 20² × sin 90° ÷ 9.80665

At x = 30 m the ball is still {y30:.2f} m up, from y = x tan θ − g x² ÷ (2 v² cos² θ). Doubling the launch speed to 40 m/s multiplies the range by four, to {R40:.1f} m, and on the Moon (g = 1.62 m/s²) the same throw would travel {Rmoon:.0f} m.''')],
     body_add=f'''
## Height, flight time and horizontal speed by angle (20 m/s)

| Angle | Maximum height | Time of flight | Horizontal speed |
|---|---|---|---|
{ang_rows}
Range is shared by complementary angles, but height and time are not: a 75° lob stays in the air {2*v*math.sin(math.radians(75))/g0/(2*v*math.sin(math.radians(15))/g0):.1f} times longer than a 15° shot that lands at the same spot.

## Measuring a real trajectory

The simplest method is slow motion video against a background with marked distances: step through the frames, note the position every few frames and fit a parabola. Radar guns give launch speed directly, and launch monitors in golf and baseball measure speed, angle and spin together. Comparing those measurements with this calculator shows how much air drag removes.

## Common mistakes

- **Using the level ground formulas from a height.** A ball thrown from a cliff or a shot put released at shoulder height needs the launch height formula above, or the range comes out short.
- **Entering speed in km/h as m/s.** 72 km/h is 20 m/s; typing 72 gives a range almost 13 times too large.
- **Thinking the ball stops at the top.** Only the vertical velocity is zero at the peak; it still moves sideways at {vx:.2f} m/s.
- **Splitting with the wrong trig function.** The horizontal part is v cos θ and the vertical part v sin θ when θ is measured from the ground.
- **Trusting 45° for real balls.** With drag, the best angle for a long throw or a golf drive is well below 45°.
''',
     faq_add=[('What is the speed of a projectile at the top of its path?',
               f'Only the horizontal component remains, v cos θ. For 20 m/s at 45° that is {vx:.2f} m/s; the vertical velocity is zero at the peak.')])

# ---------------------------------------------------------------- kinetic energy
m, vk = 1200.0, 100.0
vms = vk / 3.6
KE = 0.5 * m * vms ** 2
assert abs(KE / 1000 - 462.963) < 0.001
hdrop = vms ** 2 / (2 * g0)
p = m * vms
d_stop = 40.0
F_stop = KE / d_stop
kwh = KE / 3.6e6
# brake disc temperature rise: 4 discs of 6 kg steel, c = 460 J/kg K
disc_m, c_steel = 4 * 6.0, 460.0
dT = KE / (disc_m * c_steel)
drop_rows = ''
for s in (30, 50, 80, 100, 120, 150):
    u = s / 3.6
    drop_rows += f"| {s} km/h | {u:.2f} m/s | {0.5*m*u**2/1000:,.0f} kJ | {u**2/(2*g0):.1f} m |\n"

edit('physics/kinetic-energy', date=U, phrase='kinetic energy calculator',
     intro=("Kinetic energy is the energy an object has because it is moving, KE = ½mv². "
            "This kinetic energy calculator finds the energy from mass and speed, or the speed or mass from a known energy, with automatic unit conversion. Because energy grows with the square of speed, doubling speed quadruples it.\n\n"
            "Students use it for mechanics problems, road safety trainers use it to show why speed matters, and engineers use it to size brakes, buffers and crash barriers."),
     replace=[('''## Worked example

A 1,200 kg car at 100 km/h (27.78 m/s):

KE = 0.5 × 1,200 × 27.78² = **463 kJ**''',
               f'''## Worked example

A 1,200 kg car at 100 km/h, the calculator defaults:

1. Convert the speed: 100 ÷ 3.6 = {vms:.3f} m/s
2. Square it: {vms:.3f}² = {vms**2:.1f} m²/s²
3. KE = 0.5 × 1,200 × {vms**2:.1f} = {KE:,.0f} J = **{KE/1000:.1f} kJ**

That is {kwh:.3f} kWh, about the same energy as dropping the car from a height of {hdrop:.1f} m (v² ÷ 2g). To stop it in {d_stop:.0f} m the brakes must apply an average force of {KE/1000:.1f} kJ ÷ {d_stop:.0f} m = {F_stop/1000:.2f} kN.''')],
     body_add=f'''
## Equivalent drop height by speed (1,200 kg car)

| Speed | Speed in m/s | Kinetic energy | Same as falling from |
|---|---|---|---|
{drop_rows}
The drop height does not depend on mass, which makes it a useful way to picture a crash: hitting a wall at 50 km/h is like driving off a {(50/3.6)**2/(2*g0):.1f} m high roof.

## Where the energy goes in a stop

In a normal stop almost all of the {KE/1000:.0f} kJ ends up as heat in the brakes. If four steel discs of 6 kg each absorb it (specific heat about 460 J/kg·K), they warm by roughly {dT:.0f} °C in one stop from 100 km/h, which is why repeated hard braking on a long descent causes brake fade. Regenerative braking in electric cars returns part of that energy to the battery instead.

## Kinetic energy and momentum

The same car has a momentum of {p:,.0f} kg·m/s. Momentum grows with speed, energy with speed squared, so KE = p² ÷ 2m. Collisions conserve momentum, but kinetic energy is usually lost to deformation and heat; see the [momentum calculator](/physics/momentum/).

## Common mistakes

- **Leaving speed in km/h.** Using 100 instead of {vms:.2f} m/s gives {0.5*m*100**2/1000:,.0f} kJ, about 13 times too much.
- **Forgetting to square the speed.** ½ × 1,200 × {vms:.2f} = {0.5*m*vms:,.0f}, which is half the momentum, not the energy.
- **Dropping the ½.** m v² alone is twice the kinetic energy.
- **Mixing weight and mass.** Use the mass in kg; a weight in newtons must first be divided by 9.81.
- **Adding energies of objects moving in different directions as vectors.** Kinetic energy is a scalar; just add the values.
''',
     faq_add=[('How high would a car have to fall to match its crash energy?',
               f'Use h = v² ÷ 2g. At 100 km/h ({vms:.2f} m/s) the height is {hdrop:.1f} m, whatever the mass of the car; at 50 km/h it is {(50/3.6)**2/(2*g0):.1f} m.')])

# ---------------------------------------------------------------- simple harmonic motion
A, f, t, ph = 0.1, 2.0, 0.1, 0.0
w = 2 * math.pi * f
x = A * math.cos(w * t + ph)
vv = -A * w * math.sin(w * t + ph)
acc = -(w ** 2) * x
vm, am = A * w, A * w ** 2
assert abs(x - 0.0309) < 0.0001 and abs(vv + 1.1951) < 0.0001 and abs(acc + 4.880) < 0.001
# energy for a 0.5 kg mass
ms = 0.5
k = ms * w ** 2
Etot = 0.5 * k * A ** 2
KEt = 0.5 * ms * vv ** 2
PEt = 0.5 * k * x ** 2
assert abs(KEt + PEt - Etot) < 1e-9
# vibration: 1 g peak acceleration at various frequencies
vib_rows = ''
for fr in (5, 10, 50, 100, 500, 1000):
    ww = 2 * math.pi * fr
    vib_rows += f"| {fr} Hz | {g0/ww*1000:.2f} mm/s | {g0/ww/math.sqrt(2)*1000:.2f} mm/s | {g0/ww**2*1e3:.4f} mm |\n"
rms_v = vm / math.sqrt(2)

edit('physics/simple-harmonic-motion', date=U, phrase='simple harmonic motion calculator',
     intro=("Simple harmonic motion is the back and forth motion of a spring, pendulum or vibrating machine, where the restoring force is proportional to displacement. "
            "This simple harmonic motion calculator gives the displacement, velocity and acceleration at any instant, plus the period, angular frequency and peak values.\n\n"
            "Physics students use it to check oscillation problems, and vibration engineers use it to convert between displacement, velocity and acceleration readings at a known frequency."),
     body_add=f'''
## Energy in the worked example

Give the oscillating body a mass of {ms} kg. For SHM at ω = {w:.4f} rad/s the spring constant must be k = m ω² = {k:.2f} N/m, and the total energy is ½ k A² = **{Etot:.4f} J**. At t = 0.1 s the split is:

- Kinetic energy ½ m v² = 0.5 × {ms} × ({vv:.4f})² = {KEt:.4f} J
- Potential energy ½ k x² = 0.5 × {k:.2f} × {x:.4f}² = {PEt:.4f} J
- Sum = {KEt+PEt:.4f} J, the same as the total, as it must be without damping

## Vibration readings: the same motion three ways

Machine vibration is close to SHM at each frequency, so the peak values follow v = a ÷ ω and x = a ÷ ω². For a peak acceleration of 1 g (9.81 m/s²):

| Frequency | Peak velocity | RMS velocity | Peak displacement |
|---|---|---|---|
{vib_rows}
The same 1 g means large movement at low frequency and almost none at high frequency. That is why displacement probes suit slow shafts, velocity in mm/s RMS is used for general machine condition (ISO 10816 and ISO 20816) and accelerometers are used for bearing and gear faults at high frequency.

## How SHM is measured

An accelerometer gives a(t) directly, and the frequency is read from the spectrum; integrating once gives velocity and twice gives displacement. In a lab, a motion sensor or a video of a mass on a spring gives x(t), and the period is timed over 10 or 20 cycles to reduce reaction time error.

## Common mistakes

- **Using degrees inside cos with ω t in radians.** ωt = {w*t:.4f} rad is {math.degrees(w*t):.0f}°; mixing the two gives a wrong phase.
- **Confusing f and ω.** At 2 Hz, ω is {w:.3f} rad/s, not 2; using f in place of ω makes v<sub>max</sub> and a<sub>max</sub> far too small.
- **Mixing peak, peak to peak and RMS.** The {vm:.4f} m/s peak velocity here is {rms_v:.4f} m/s RMS, and the displacement is {2*A:.1f} m peak to peak.
- **Reading a negative value as an error.** A negative velocity or displacement only means the motion is on, or heading to, the negative side.
- **Applying SHM to large pendulum swings.** Above about 15° the pendulum period grows with amplitude and the simple formulas drift.
''',
     faq_add=[('How do I convert vibration acceleration to velocity and displacement?',
               f'For a single frequency, divide the acceleration by ω = 2πf to get velocity and by ω² to get displacement. 1 g at 100 Hz is {g0/(2*math.pi*100)*1000:.2f} mm/s peak and {g0/(2*math.pi*100)**2*1000:.3f} mm peak.')])

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-24), slice 6: youngs-modulus, momentum, latent-heat, bernoulli-equation, acceleration.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-24'
g0 = 9.80665


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Young's modulus
F, A, L0, dL = 10e3, 78.5398e-6, 2.0, 1.25e-3
s = F / A
ep = dL / L0
E = s / ep
assert abs(s / 1e6 - 127.32) < 0.01 and abs(E / 1e9 - 203.72) < 0.01
k_bar = A * E / L0                    # N/m
yield_s275 = 275e6
sf = yield_s275 / s
# same rod, same load, different materials
mat_rows = ''
for name, Eg, sy in (('Structural steel', 200, 275), ('Stainless steel 304', 193, 215), ('Aluminium 6061-T6', 69, 276),
                     ('Copper (annealed)', 117, 70), ('Titanium Ti-6Al-4V', 114, 880)):
    ext = F * L0 / (A * Eg * 1e9)
    ok = 'yes' if s / 1e6 < sy else 'no, it yields'
    mat_rows += f"| {name} | {Eg} GPa | {ext*1000:.2f} mm | {sy} MPa | {ok} |\n"
# effect of a 0.1 mm error in diameter
d_true = math.sqrt(4 * A / math.pi)
A_wrong = math.pi * (d_true - 0.1e-3) ** 2 / 4
E_wrong = (F / A_wrong) / ep
err_pct = (E_wrong / E - 1) * 100
# gauge length mistake: extension measured over a 50 mm extensometer
ext50 = s / E * 0.050

edit('physics/youngs-modulus', date=U, phrase="Young's modulus calculator",
     intro=("Young's modulus is the ratio of stress to strain while a material is still elastic, so it tells you how much a bar stretches or shortens under load. "
            "This Young's modulus calculator works out stress, strain, modulus and extension for a rod, wire or bar.\n\n"
            "Students check tensile test results with it, designers predict how far a tie rod or bolt will stretch, and instrument engineers use the same relation in a "
            "[strain gauge](https://www.instrumentationblog.in/strain-gauge-working-principle/) load cell."),
     body_add=f'''
## Stiffness and safety of the default rod

The default bar is more than a modulus test: it is also a spring. Its axial stiffness is k = A E ÷ L<sub>0</sub> = 78.54 mm² × {E/1e9:.1f} GPa ÷ 2 m = **{k_bar/1e6:.2f} kN/mm**, so every extra kilonewton stretches it by another {1000/k_bar*1000:.3f} mm. At {s/1e6:.1f} MPa it is working at {s/yield_s275*100:.0f}% of the 275 MPa yield strength of S275 steel, a safety factor of {sf:.2f}, which is why it springs back fully when the load is removed.

## Same rod and load in other materials

A 10 kN pull on a 10 mm diameter bar, 2 m long, gives {s/1e6:.1f} MPa in every material, but the extension depends on E:

| Material | E | Extension | Typical yield strength | Still elastic? |
|---|---|---|---|---|
{mat_rows}
Copper shows why the modulus alone is not enough: the formula predicts a small extension, but annealed copper has already yielded at this stress, so the real stretch is larger and permanent.

## How Young's modulus is measured

In a tensile test (ASTM E8 for the strength values, ASTM E111 for the modulus itself) a machined specimen is pulled while a clip on extensometer records the extension over a fixed gauge length, often 50 mm. E is the slope of the straight part of the stress strain curve, fitted between roughly 10% and 40% of yield rather than read from a single point. Bonded strain gauges give the same slope on parts that cannot be cut into specimens. Dynamic methods such as impulse excitation (ASTM E1876) tap a bar and work E out from its resonant frequency, which suits brittle ceramics and glass.

## Common mistakes

- **Mixing mm² and m².** 78.54 mm² is 78.54 × 10⁻⁶ m²; dropping the 10⁻⁶ makes the stress a million times too small.
- **Using diameter as radius.** A = π d² ÷ 4. Even a 0.1 mm error on the 10 mm rod shifts the calculated E by {err_pct:.1f}%, so measure the diameter with a micrometer.
- **Dividing by the wrong length.** Strain uses the length the extension was measured over. Over a 50 mm extensometer the same rod only moves {ext50*1000:.4f} mm, not 1.25 mm.
- **Reading the modulus past yield.** Points beyond the proportional limit give a falling apparent E that is not a material property.
- **Ignoring grip slip.** Crosshead movement includes slack in the grips and machine frame, so a modulus worked out from it is usually far too low.
''',
     faq_add=[("What is the difference between Young's modulus and stiffness?",
               f"Young's modulus is a material property in pascals. Stiffness, k = A E ÷ L, also depends on the shape: the default 10 mm, 2 m steel rod has k = {k_bar/1e6:.2f} kN/mm, and a rod twice as long would have half that."),
              ("Why does my tensile test give a much lower modulus than the handbook?",
               "Usually because the extension was taken from crosshead travel, which includes grip slip and frame flexing. Use an extensometer or strain gauge on the specimen and fit the straight part of the curve.")])

# ---------------------------------------------------------------- Momentum
m, v_kmh = 0.16, 140
v = v_kmh / 3.6
p = m * v
ke = 0.5 * m * v * v
assert abs(p - 6.222) < 0.001 and abs(ke - 120.99) < 0.05
# catching: stop in 0.01 s vs 0.1 s
F_hard = p / 0.01
F_soft = p / 0.1
# p from KE
p_from_ke = math.sqrt(2 * m * ke)
# ballistic pendulum: 8 g bullet into 2 kg block, rises 0.10 m
mb, M, hh = 0.008, 2.0, 0.10
vb_block = math.sqrt(2 * g0 * hh)
vb = (mb + M) / mb * vb_block
# same KE, different masses
ke_cmp = 100.0
cmp_rows = ''
for name, mm in (('Golf ball', 0.0459), ('Cricket ball', 0.16), ('Football', 0.43), ('Shot put', 7.26)):
    vv = math.sqrt(2 * ke_cmp / mm)
    cmp_rows += f"| {name} | {mm:g} kg | {vv:.1f} m/s | {mm*vv:.2f} kg·m/s |\n"

edit('physics/momentum', date=U, phrase='momentum calculator',
     intro=("Linear momentum is mass multiplied by velocity: a measure of how hard a moving object is to stop, and a quantity conserved in every collision. "
            "This momentum calculator finds p = mv from a mass and speed, or the speed or mass from a known momentum, and shows the kinetic energy beside it.\n\n"
            "Physics students use it for collision and recoil problems, coaches compare balls and players, and engineers start crash and impact force estimates from it."),
     before='## Practical notes',
     body_add=f'''
## Stopping the ball: why catching time matters

The cricket ball's {p:.2f} kg·m/s must all be removed to stop it. Stopped against a rigid surface in 0.01 s the average force is {p:.2f} ÷ 0.01 = **{F_hard:,.0f} N**; a fielder who draws the hands back so the catch takes 0.1 s feels only **{F_soft:.0f} N**. Same momentum change, one tenth of the force.

## Equal energy is not equal momentum

For the same 100 J of kinetic energy, the heavier object carries much more momentum, because p = √(2 m KE):

| Object | Mass | Speed for 100 J | Momentum |
|---|---|---|---|
{cmp_rows}
This is why a slow, heavy object is harder to stop by hand than a fast, light one with the same energy.

## How momentum is measured

Momentum is not read directly; mass and velocity are measured separately. Balls are weighed and timed with a radar gun, light gates or high speed video. In school labs two light gates on an air track give the velocities before and after a collision. For bullets the classic method is the ballistic pendulum: an {mb*1000:.0f} g bullet that lodges in a {M:.0f} kg block and lifts it {hh*100:.0f} cm gives the block {vb_block:.3f} m/s, so the bullet was moving at about **{vb:.0f} m/s**. Momentum is conserved in the impact, then energy in the swing.

## Common mistakes

- **Leaving speed in km/h.** 6.22 kg·m/s needs 38.89 m/s; using 140 directly gives a momentum 3.6 times too big.
- **Entering grams as kilograms.** A 160 g ball is 0.16 kg.
- **Adding momenta without signs.** Two equal cars meeting head on at the same speed have a total momentum of zero, not double.
- **Using kinetic energy conservation for a crash.** Only momentum is conserved when objects stick or crumple.
- **Adding 2D momenta as plain numbers.** Resolve into x and y components first, then combine.
''',
     faq_add=[('How do you find momentum from kinetic energy?',
               f'Use p = √(2 m KE). For the default ball, √(2 × 0.16 × {ke:.1f}) = {p_from_ke:.2f} kg·m/s, matching m × v.'),
              ('Can an object have kinetic energy but zero total momentum?',
               'A single moving object cannot, but a system can: two identical balls moving apart at the same speed have zero total momentum and plenty of kinetic energy. That is what happens in an explosion from rest.')])

# ---------------------------------------------------------------- Latent heat
m, L = 2.0, 2257e3
Q = m * L
Qk = Q / 3.6e6
assert abs(Q / 1e3 - 4514) < 1e-6 and abs(Qk - 1.2539) < 0.0001
# kettle 2 kW, 90% of heat into water
P_k, eff = 2000, 0.9
t_boil = Q / (P_k * eff)
# full path for 2 kg from ice at -20 C to steam at 100 C
c_ice, c_w = 2.09e3, 4.186e3
Lf = 334e3
q1 = m * c_ice * 20
q2 = m * Lf
q3 = m * c_w * 100
q4 = Q
qt = q1 + q2 + q3 + q4
path_rows = ''
for name, q in (('Warm ice from −20 °C to 0 °C', q1), ('Melt the ice at 0 °C', q2),
                ('Heat water from 0 °C to 100 °C', q3), ('Boil off at 100 °C', q4)):
    path_rows += f"| {name} | {q/1e3:,.1f} kJ | {q/qt*100:.1f}% |\n"
# ice for 1 kWh
ice_kwh = 3.6e6 / Lf
# steam tables (saturated, approximate) h_fg kJ/kg
steam = ((1, 99.6, 2257.5), (2, 120.2, 2201.6), (5, 151.8, 2107.4), (10, 179.9, 2014.6), (20, 212.4, 1889.8), (40, 250.4, 1714.1))
steam_rows = ''.join(f"| {pb} bar(a) | {T:.1f} °C | {h:,.1f} kJ/kg | {m*h:,.0f} kJ |\n" for pb, T, h in steam)

edit('physics/latent-heat', date=U, phrase='latent heat calculator',
     intro=("Latent heat is the energy a substance takes in or gives out while it changes phase at a constant temperature: melting, freezing, boiling or condensing. "
            "This latent heat calculator applies Q = mL to find that energy for a given mass, or the mass a given amount of heat can melt or evaporate.\n\n"
            "Students use it for calorimetry problems, while HVAC, refrigeration and steam engineers use it to size heaters, evaporators, condensers and ice storage."),
     body_add=f'''
## From ice to steam: where the energy goes

The default 2 kg of boiling water is only the last step. Starting from ice at −20 °C (c<sub>ice</sub> = 2.09 kJ/kg·K, c<sub>water</sub> = 4.186 kJ/kg·K):

| Step | Heat | Share |
|---|---|---|
{path_rows}
The total is **{qt/1e3:,.0f} kJ** ({qt/3.6e6:.3f} kWh), and the two phase changes together take {(q2+q4)/qt*100:.0f}% of it while the temperature barely moves.

## How long a kettle takes to boil it dry

A 2 kW kettle delivering about 90% of its power to the water needs {Q/1e3:,.0f} kJ ÷ ({P_k*eff/1000:.1f} kW) = **{t_boil:,.0f} s**, roughly {t_boil/60:.0f} minutes, to evaporate the 2 kg once it is boiling. That is why a kettle switches off at boiling point: the latent heat is far larger than the energy needed to reach 100 °C.

## Latent heat of steam at higher pressure

Boilers rarely run at atmospheric pressure, and h<sub>fg</sub> falls as pressure rises. Approximate saturated steam table values:

| Pressure | Saturation temperature | h<sub>fg</sub> | Heat released by 2 kg condensing |
|---|---|---|---|
{steam_rows}
Use the value at the steam pressure in the heater shell, not the 2,257 kJ/kg of the dropdown, when sizing a steam heat exchanger.

## How latent heat is measured

The classic method is mixing calorimetry: drop a weighed piece of ice into warm water in an insulated cup and work out L<sub>f</sub> from the temperature fall. Laboratories now use differential scanning calorimetry (DSC), which measures the heat flow into a few milligrams of sample as it melts. In a plant, the latent heat duty is usually found from the condensate flow: every kilogram of condensate collected has given up h<sub>fg</sub>. For ice storage cooling, 1 kWh of heat melts {ice_kwh:.1f} kg of ice.

## Common mistakes

- **Mixing J and kJ.** Tables give L in kJ/kg; the calculator multiplies by 1,000 so Q comes out in joules.
- **Forgetting the sensible heat.** Water at 20 °C needs warming to 100 °C first; add m c ΔT.
- **Picking fusion for a boiling problem.** 334 kJ/kg is for melting; boiling water needs 2,257 kJ/kg.
- **Using 100 °C values for pressurised steam.** At 10 bar(a) only about 2,015 kJ/kg is released per kg.
- **Assuming all heater power reaches the substance.** Kettles, pans and vessels lose heat to their surroundings, so real times are longer.
''',
     faq_add=[('How much ice does it take to absorb 1 kWh of heat?',
               f'About {ice_kwh:.1f} kg. 1 kWh is 3,600 kJ, and melting ice absorbs 334 kJ per kg, so 3,600 ÷ 334 = {ice_kwh:.1f} kg, not counting any warming of the meltwater.'),
              ('What is the difference between latent heat and specific heat?',
               'Specific heat is the energy to change the temperature of 1 kg by 1 K without a change of phase. Latent heat is the energy to change phase at a constant temperature, and it is usually much larger.')])

# ---------------------------------------------------------------- Bernoulli
rho, P1, v1, h1, v2, h2 = 1000, 200e3, 2.0, 0.0, 5.0, 3.0


def p2(v2, h2):
    return P1 + 0.5 * rho * (v1 ** 2 - v2 ** 2) + rho * g0 * (h1 - h2)


P2 = p2(v2, h2)
H = P1 / (rho * g0) + v1 ** 2 / (2 * g0) + h1
assert abs(P2 / 1e3 - 160.08) < 0.01 and abs(H - 20.598) < 0.001
# check point 2 head equals H
H2 = P2 / (rho * g0) + v2 ** 2 / (2 * g0) + h2
assert abs(H2 - H) < 1e-9
# continuity: D2 for D1 = 100 mm
D1 = 100.0
D2 = D1 * math.sqrt(v1 / v2)
Qflow = v1 * math.pi * (D1 / 1000) ** 2 / 4
# table P2 vs v2 and h2
tab_rows = ''
for vv in (2, 4, 5, 8, 10):
    tab_rows += f"| {vv} m/s | " + ' | '.join(f"{p2(vv, hh)/1e3:.1f} kPa" for hh in (0, 3, 10)) + ' |\n'
# max height with v2 = 5 at which P2 would reach 0 gauge
h_zero = (P1 + 0.5 * rho * (v1 ** 2 - v2 ** 2)) / (rho * g0) + h1
# psi of P2
P2_psi = P2 / 6894.757

edit('physics/bernoulli-equation', date=U, phrase='Bernoulli equation calculator',
     intro=("Bernoulli's equation says that along a streamline the sum of pressure, kinetic energy per volume and potential energy per volume stays constant in steady, frictionless, incompressible flow. "
            "This Bernoulli equation calculator finds the pressure at a second point from conditions at the first; see "
            "[Bernoulli's equation and its formula](https://www.instrumentationblog.in/bernoullis-equation-formula/).\n\n"
            "Students, pump and piping engineers and flow meter specialists use it for venturi, pitot and nozzle problems."),
     before='## Practical notes',
     body_add=f'''
## Checking the example with heads

Bernoulli's equation can be read as energy per unit weight. At point 1 the pressure head is {P1/1e3:.0f} kPa ÷ (1,000 × 9.80665) = {P1/(rho*g0):.3f} m and the velocity head is 2² ÷ (2 × 9.80665) = {v1**2/(2*g0):.3f} m, so H = {H:.3f} m. At point 2 the pressure head is {P2/(rho*g0):.3f} m, the velocity head {v2**2/(2*g0):.3f} m and the elevation 3 m, which add back to **{H2:.3f} m**. If your two totals differ, an input or unit is wrong. P<sub>2</sub> = {P2/1e3:.2f} kPa is also {P2_psi:.2f} psi.

## Where the second velocity comes from

In a real pipe v<sub>2</sub> is set by continuity, v<sub>1</sub>A<sub>1</sub> = v<sub>2</sub>A<sub>2</sub>. If point 1 is a 100 mm bore carrying {Qflow*1000:.2f} L/s, a speed of 5 m/s at point 2 means a bore of 100 × √(2 ÷ 5) = **{D2:.1f} mm**. Work out the speed from the diameters first, then use this calculator for the pressure.

## Pressure at point 2 for other speeds and heights

Same water, P<sub>1</sub> = 200 kPa and v<sub>1</sub> = 2 m/s:

| v<sub>2</sub> | h<sub>2</sub> = 0 m | h<sub>2</sub> = 3 m | h<sub>2</sub> = 10 m |
|---|---|---|---|
{tab_rows}
With v<sub>2</sub> = 5 m/s the gauge pressure would reach zero at a height of {h_zero:.2f} m, so a pipe climbing higher than that would need more inlet pressure.

## Measuring the terms in practice

Static pressure is read with a gauge or transmitter on a wall tapping flush with the pipe bore, never one that pokes into the stream. Elevation differences come from drawings or a level survey of the tapping points. Velocity is found from the volumetric flow rate divided by the bore area, or with a pitot tube that senses static plus dynamic pressure. A differential pressure transmitter across two tappings measures P<sub>1</sub> − P<sub>2</sub> directly, which is how venturi and orifice meters turn this equation into a flow reading.

## Common mistakes

- **Mixing gauge and absolute pressure.** Either works, but both points must use the same reference.
- **Getting the elevation sign wrong.** Point 2 above point 1 lowers P<sub>2</sub>; measure both heights from one datum.
- **Applying it across a pump or turbine.** Add the pump head or subtract the turbine head, or the result is meaningless.
- **Picking v<sub>2</sub> freely.** It is fixed by the flow rate and bore, so check it with continuity.
- **Ignoring friction on long runs.** Over many metres of pipe the head loss can be bigger than the velocity term.
''',
     faq_add=[('How do I find the velocity at point 2 from the pipe diameters?',
               f'Use continuity: v2 = v1 × (D1 ÷ D2)². Water at 2 m/s in a 100 mm bore speeds up to 5 m/s in a {D2:.1f} mm bore. Enter that v2 here to get the pressure.'),
              ('Why is my measured pressure lower than the Bernoulli result?',
               'Real pipes lose head to wall friction, bends, valves and sudden changes in bore. Bernoulli gives the ideal value; subtract the friction loss ρ g hL to get what a gauge will read.')])

# ---------------------------------------------------------------- Acceleration
u, vk, t = 0.0, 100.0, 8.0
vms = vk / 3.6
a = (vms - u) / t
gs = a / g0
assert abs(a - 3.4722) < 0.0001 and abs(gs - 0.354) < 0.0005
s_run = (u + vms) / 2 * t
m_car = 1500
F_car = m_car * a
P_end = F_car * vms
# distance for other 0-100 times
dist_rows = ''
for tt in (3.5, 5, 8, 12, 15):
    aa = vms / tt
    dist_rows += f"| {tt:g} s | {aa:.2f} m/s² | {vms/2*tt:.1f} m | {m_car*aa:,.0f} N |\n"
# braking from 100 at 0.8 g
a_br = 0.8 * g0
s_br = vms ** 2 / (2 * a_br)
t_br = vms / a_br
# 50 to 80 km/h overtake in 4 s
a_ov = (80 - 50) / 3.6 / 4

edit('physics/acceleration', date=U, phrase='acceleration calculator',
     intro=("Acceleration is how quickly velocity changes, whether an object speeds up, slows down or changes direction. "
            "This acceleration calculator works it out from the initial speed, final speed and time, in m/s² and in g, or finds the time or final speed from a known acceleration.\n\n"
            "Students use it in motion problems, drivers and car testers compare 0 to 100 km/h times, and engineers check the loads that people and equipment feel."),
     replace=[('''## Related equations

For distance covered while accelerating, use the [SUVAT calculator](/physics/suvat-equations/).''',
               f'''## Distance and force during the default run

With constant acceleration the average speed is (0 + 27.78) ÷ 2 = {vms/2:.2f} m/s, so the car covers {vms/2:.2f} × 8 = **{s_run:.1f} m** while reaching 100 km/h. For a {m_car:,} kg car, F = m a = {m_car:,} × {a:.3f} = **{F_car:,.0f} N** of net forward force, and at the moment it reaches 100 km/h that force needs F × v = {P_end/1000:.0f} kW at the wheels. Real cars accelerate harder at low speed and less near the top, so 3.47 m/s² is an average.

| 0 to 100 km/h time | Average acceleration | Distance covered | Net force for {m_car:,} kg |
|---|---|---|---|
{dist_rows}
For other distance problems use the [SUVAT calculator](/physics/suvat-equations/).

## Overtaking and braking examples

Going from 50 to 80 km/h in 4 s is (80 − 50) ÷ 3.6 ÷ 4 = **{a_ov:.2f} m/s²**. Braking from 100 km/h at 0.8 g ({a_br:.2f} m/s²) takes {t_br:.2f} s and {s_br:.1f} m, before adding the distance covered during the driver's reaction time.

## How acceleration is measured

Phones, car data loggers and crash test dummies use MEMS accelerometers, tiny silicon masses on springs whose deflection is read capacitively. Vibration engineers use piezoelectric accelerometers that respond to thousands of hertz. Performance testers more often log GPS speed many times a second and differentiate it, which avoids the tilt error an accelerometer picks up on a sloping road. In a school lab, two light gates and a timer give the speed at two points and the time between them.

## Common mistakes

- **Leaving speeds in km/h.** Divide by 3.6 first; 100 ÷ 8 = 12.5 is in km/h per second, not m/s².
- **Dropping the sign.** Slowing from 100 to 50 km/h gives a negative a; keep it so later calculations stay consistent.
- **Treating the average as the peak.** A car that averages 0.35 g may pull 0.6 g in first gear.
- **Using total time with a reaction delay.** If the timer includes a pause before moving, the acceleration comes out too low.
- **Quoting g as a force.** g is an acceleration ratio; multiply by mass and 9.80665 to get newtons.''')],
     faq_add=[('How far does a car travel while accelerating from 0 to 100 km/h?',
               f'At constant acceleration it is the average speed times the time. For 8 s that is {vms/2:.2f} m/s × 8 s = {s_run:.1f} m; a 5 s car covers {vms/2*5:.1f} m.'),
              ('How is acceleration measured in a car or phone?',
               'With a MEMS accelerometer, a tiny sprung silicon mass whose movement is sensed electrically, or by logging GPS speed many times a second and working out how fast it changes.')])

if __name__ == '__main__':
    from inplace import body_words
    for cid in ('physics/youngs-modulus', 'physics/momentum', 'physics/latent-heat', 'physics/bernoulli-equation', 'physics/acceleration'):
        print(cid, body_words(cid))
