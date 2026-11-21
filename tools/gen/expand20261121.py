"""Part C expansion (2026-11-21): 30 pages from the top of tools/upgrade-backlog.txt (priority list was empty), brought to the api-gravity standard. Assembled from six sections; edits are applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-21), slice 1: acceleration-factor, beam-deflection, minor-losses, hydraulic-cylinder-force, mass-flow-rate.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-21'
IB = 'https://www.instrumentationblog.in/'
g0 = 9.80665


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Arrhenius acceleration factor
kB = 8.617333262e-5


def AF(Ea, Tu, Ts):
    return math.exp(Ea / kB * (1 / (Tu + 273.15) - 1 / (Ts + 273.15)))


Ea, Tu, Ts, N, th, CL = 0.7, 55.0, 125.0, 77, 1000.0, 0.60
af0 = AF(Ea, Tu, Ts)
heq0 = N * th * af0
chi60 = -math.log(1 - CL)
fit0 = chi60 / heq0 * 1e9
assert abs(af0 - 77.65) < 0.01 and abs(fit0 - 153.26) < 0.01
# planning: hours needed to show 50 FIT at 60% with 0 failures
target = 50.0
heq_need = chi60 / (target * 1e-9)
dev_h_need = heq_need / af0
hrs_77 = dev_h_need / N
n_1000 = math.ceil(dev_h_need / 1000)
# self heating: 0.5 W at theta_JA 40 K/W raises Tj by 20 K
Tj_test = 125 + 0.5 * 40
af_tj = AF(Ea, Tu, Tj_test)
fit_tj = chi60 / (N * th * af_tj) * 1e9
# field runs hotter than assumed
af_65 = AF(Ea, 65, 125)
fit_65 = chi60 / (N * th * af_65) * 1e9
# confidence table for the default test
cl_rows = ''
for cl in (0.50, 0.60, 0.90, 0.95):
    x = -math.log(1 - cl)
    f = x / heq0 * 1e9
    cl_rows += f"| {cl*100:.0f}% | {x:.3f} | {f:.0f} FIT | {1e9/f/8766:,.0f} years |\n"

edit('engineering/acceleration-factor', date=U, phrase='acceleration factor calculator',
     intro=("Accelerated life tests run parts hot so that a few weeks represent years of field use. "
            "This acceleration factor calculator applies the Arrhenius model to the activation energy and the use and stress temperatures, then turns a zero-failure test into a FIT rate and MTTF.\n\n"
            "Reliability and quality engineers use it to plan HTOL and burn-in tests, to check supplier qualification reports and to quote failure rates for electronics in reliability predictions."),
     body_add=f'''
## Planning a test to prove a FIT target

The calculator can be run backwards to size a test. Suppose a customer asks for no more than **{target:g} FIT** at 60% confidence, with the same 55 °C use temperature, 125 °C stress and E<sub>a</sub> = 0.7 eV:

- Required equivalent device-hours = {chi60:.3f} ÷ ({target:g} × 10⁻⁹) = **{c(heq_need)} h**
- Real device-hours in the oven = {c(heq_need)} ÷ {af0:.2f} = **{c(dev_h_need)} h**
- With 77 devices that is about **{c(hrs_77)} h** of testing, or about **{n_1000} devices** for a standard 1,000 h run

The default test of 77 devices for 1,000 h only reaches {fit0:.0f} FIT, so either the sample, the duration or the stress temperature has to rise.

## How confidence level changes the result

For the default 77 × 1,000 h test with zero failures:

| Confidence | −ln(1 − CL) | FIT upper bound | MTTF lower bound |
|---|---|---|---|
{cl_rows}
Reports often quote 60% because it gives a smaller number; customers in automotive and medical work usually ask for 90%.

## How the test is run in practice

HTOL (high temperature operating life, JEDEC JESD22-A108) parts are biased and exercised inside a chamber, normally at 125 °C ambient, and taken out at read points such as 168, 500 and 1,000 hours for electrical testing at room and hot temperature. The acceleration factor must use the **junction** temperature. If each device dissipates 0.5 W with θ<sub>JA</sub> = 40 K/W, the junction sits at {Tj_test:.0f} °C, the acceleration factor rises to **{af_tj:.0f}** and the same test demonstrates **{fit_tj:.0f} FIT**. Ignoring that self heating understates the stress, while claiming it without measuring it overstates the result.

## Common mistakes

- **Entering temperatures in °C inside the formula.** The Arrhenius term needs kelvin; the calculator converts, but hand calculations with 55 and 125 give nonsense.
- **Assuming a cool field temperature.** If the product actually runs at 65 °C instead of 55 °C, AF falls from {af0:.1f} to {af_65:.1f} and the same test only supports {fit_65:.0f} FIT.
- **Picking a high E<sub>a</sub> to flatter the numbers.** Moving from 0.7 eV to 1.0 eV multiplies AF several times, so the value must come from the failure mechanism, not from the target.
- **Pooling tests with different conditions.** Device-hours from 125 °C and 150 °C runs must each be multiplied by their own AF before adding.
- **Reading MTTF as product life.** A demonstrated MTTF of hundreds of years describes the random failure rate, not how long a single part lasts before wear-out.
''',
     faq_add=[('How many devices and hours do I need to demonstrate a FIT target?',
               f'Divide −ln(1 − CL) by the target failure rate to get equivalent device-hours, then divide by the acceleration factor. For {target:g} FIT at 60% confidence with AF = {af0:.1f}, that is about {c(dev_h_need)} device-hours, roughly {n_1000} parts for 1,000 h.'),
              ('Should I use ambient or junction temperature for the acceleration factor?',
               f'Junction temperature, for both the test and the field. A device dissipating 0.5 W at 40 K/W in a 125 °C oven has a {Tj_test:.0f} °C junction, which raises AF from {af0:.0f} to about {af_tj:.0f}.')])

# ---------------------------------------------------------------- Beam deflection
P, L, E, I = 5e3, 3.0, 200000e6, 1943e-8
dss = P * L ** 3 / (48 * E * I) * 1000
dc = P * L ** 3 / (3 * E * I) * 1000
assert abs(dss - 0.7237) < 0.001 and abs(dc - 11.58) < 0.01
# IPE 200 self weight 22.4 kg/m as a uniform load
w_sw = 22.4 * g0
d_sw = 5 * w_sw * L ** 4 / (384 * E * I) * 1000
d_tot = dss + d_sw
# timber joist 75 x 200 mm, E = 11,000 MPa, 3.6 m span, 2 kN at mid-span
b, h = 75.0, 200.0
It_mm4 = b * h ** 3 / 12
It_cm4 = It_mm4 / 1e4
Et = 11000e6
Pt, Lt = 2e3, 3.6
dt = Pt * Lt ** 3 / (48 * Et * It_mm4 * 1e-12) * 1000
lim360 = Lt * 1000 / 360
# same timber laid flat
If_mm4 = h * b ** 3 / 12
dflat = Pt * Lt ** 3 / (48 * Et * If_mm4 * 1e-12) * 1000
# deflection limits for the default 3 m span
lim_rows = ''
for name, r in (('Floors with brittle finishes', 360), ('General floors', 250), ('Roofs', 180), ('Cantilevers (common rule)', 180)):
    lim = L * 1000 / r
    Pmax_ss = lim / 1000 * 48 * E * I / L ** 3 / 1000
    lim_rows += f"| {name} | L/{r} | {lim:.1f} mm | {Pmax_ss:,.0f} kN |\n"

edit('engineering/beam-deflection', date=U, phrase='beam deflection calculator',
     intro=("How much a beam sags depends on the load, the cube of its span and its flexural stiffness E·I. "
            "This beam deflection calculator gives the maximum deflection and bending moment for a simply supported beam with a central point load and for a cantilever loaded at its tip.\n\n"
            "Structural engineers, fabricators and students use it for quick serviceability checks, and the same elastic bending is what a [beam-type load cell](https://www.instrumentationblog.in/load-cell-working-principle/) uses to measure force."),
     body_add=f'''
## Adding the beam's own weight

The calculator covers the point load only. An IPE 200 weighs about 22.4 kg/m, a uniform load of {w_sw:.0f} N/m. Over the default 3 m simple span it adds 5wL⁴ ÷ (384EI) = **{d_sw:.3f} mm**, so the total mid-span sag is about **{d_tot:.2f} mm**. Because the maximum deflections of both cases occur at mid-span, they can simply be added (superposition holds for elastic, small deflections).

## Second example: a timber floor joist

A 75 × 200 mm softwood joist (I = b h³ ÷ 12 = {It_cm4:,.0f} cm⁴, E = 11,000 MPa) spans 3.6 m with a 2 kN point load at mid-span:

- δ = 2,000 × 3.6³ ÷ (48 × 11 × 10⁹ × {It_mm4*1e-7:.1f} × 10⁻⁵ m⁴) = **{dt:.1f} mm**
- The L/360 limit for a floor is {lim360:.0f} mm, so the joist passes for this load
- Laid flat (I = {If_mm4/1e4:,.0f} cm⁴) the same joist would sag **{dflat:.0f} mm**, which shows why joists are always set on edge

Enter E = 11,000 MPa and I = {It_cm4:,.0f} cm⁴ to reproduce it.

## Deflection limits for the default 3 m beam

| Use | Limit | Allowed δ | Largest centre load on the IPE 200 |
|---|---|---|---|
{lim_rows}
The load column comes from P = 48EIδ ÷ L³; bending stress usually governs long before these loads are reached, so check both.

## How deflection is measured

On a load test the beam is loaded in steps, often with water bags or calibrated weights, and the mid-span sag is read with a dial gauge or LVDT on a stand fixed to the ground, not to the structure. Support settlement is measured at each end and subtracted. Recovery is checked after unloading: a beam that does not return close to zero has yielded or slipped at its connections.

## Common mistakes

- **Entering I in mm⁴ or m⁴.** The field expects cm⁴; 1 cm⁴ = 10,000 mm⁴, so a value from a mm⁴ table is 10,000 times too large.
- **Using the strong axis for a load that bends the weak axis.** An IPE 200 has I<sub>y</sub> ≈ 142 cm⁴ about its minor axis, 14 times less stiff.
- **Using the clear span instead of the span between bearing centres.** Because δ grows with L³, a 5% longer span gives about 16% more deflection.
- **Ignoring long term creep in timber and concrete.** Sustained loads can double timber deflection over time; design codes apply a creep factor.
- **Treating a partly fixed end as fully fixed.** Bolted end plates rarely give full fixity, so the PL³ ÷ (192EI) case is optimistic.
''',
     faq_add=[('How do I include a uniformly distributed load and a point load together?',
               f'Work out each deflection separately and add them, because both peak at mid-span on a simply supported beam. For the default IPE 200 the 5 kN point load gives {dss:.2f} mm and its own weight adds {d_sw:.3f} mm.'),
              ('How do I find I for a rectangular timber or steel section?',
               f'Use I = b h³ ÷ 12 with h the depth in the direction of bending. A 75 × 200 mm joist on edge has {It_cm4:,.0f} cm⁴; laid flat it has only {If_mm4/1e4:,.0f} cm⁴.')])

# ---------------------------------------------------------------- Minor losses
K0, V0, rho0, f0, D0 = 0.9, 2.0, 998.0, 0.02, 0.05
hL0 = K0 * V0 ** 2 / (2 * g0)
dp0 = rho0 * g0 * hL0 / 1000
Le0 = K0 * D0 / f0
assert abs(hL0 - 0.1835) < 0.0005 and abs(dp0 - 1.796) < 0.002
# pump discharge skid: entrance 0.5, 4 standard elbows 0.75, gate 0.15, swing check 2, tee branch 1, exit 1
items = [('Pipe entrance, sharp edged', 1, 0.5), ('90° standard elbow', 4, 0.75), ('Gate valve, open', 1, 0.15),
         ('Swing check valve', 1, 2.0), ('Tee, flow through branch', 1, 1.0), ('Exit into tank', 1, 1.0)]
Ksum = sum(n * k for _, n, k in items)
hK = Ksum * V0 ** 2 / (2 * g0)
dpK = rho0 * g0 * hK / 1000
Lpipe = 12.0
hf = f0 * Lpipe / D0 * V0 ** 2 / (2 * g0)
LeK = Ksum * D0 / f0
skid_rows = ''.join(f"| {nm} | {n} | {k:g} | {n*k:g} |\n" for nm, n, k in items)
# velocity sensitivity
v_rows = ''
for v in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
    h = Ksum * v ** 2 / (2 * g0)
    v_rows += f"| {v:.1f} m/s | {v**2/(2*g0)*1000:.0f} mm | {h:.3f} m | {rho0*g0*h/1000:.2f} kPa |\n"

edit('engineering/minor-losses', date=U, phrase='minor losses calculator',
     intro=("Valves, elbows, tees, entrances and exits each add a pressure loss proportional to the velocity head, described by a resistance coefficient K. "
            "This minor losses calculator adds them up, converts the loss to pressure and gives the equivalent length of straight pipe.\n\n"
            "Process and HVAC engineers use it when sizing pumps and checking skids, and it pairs with [how to calculate pressure drop in pipes](https://www.instrumentationblog.in/calculate-pressure-drop-in-pipes/) for the straight runs."),
     body_add=f'''
## Second example: a pump discharge skid

A 50 mm water line at 2 m/s leaves a tank, passes a pump skid and enters a second tank, with 12 m of straight pipe and these fittings:

| Fitting | Count | K each | K total |
|---|---|---|---|
{skid_rows}
- Total K = **{Ksum:g}**, so fitting head loss = {Ksum:g} × 2² ÷ (2 × 9.807) = **{hK:.2f} m** ({dpK:.1f} kPa)
- Straight pipe friction = 0.02 × (12 ÷ 0.05) × 2² ÷ (2 × 9.807) = **{hf:.2f} m**
- Equivalent length of the fittings = {Ksum:g} × 0.05 ÷ 0.02 = **{LeK:.1f} m**, more than the 12 m of real pipe

On compact skids the "minor" losses are often the major part of the system curve, which is why they are worth adding item by item.

## Effect of velocity on the skid loss

Loss rises with the square of velocity. For the skid above (K = {Ksum:g}):

| Velocity | Velocity head | Head loss | Pressure loss |
|---|---|---|---|
{v_rows}
Halving the velocity, for example by stepping up one pipe size, cuts the fitting loss to a quarter.

## How K values are obtained

K is measured on a test rig by fitting pressure tappings far enough upstream and downstream that the flow is fully developed, measuring the differential pressure at several flow rates and subtracting the friction of the straight pipe between the tappings. Crane TP-410 expresses many fittings as K = f<sub>T</sub> × (L/D), where f<sub>T</sub> is the fully turbulent friction factor for that pipe size, so K for a given elbow is higher in small pipes. The 2-K and 3-K methods (Hooper, Darby) add a Reynolds number term for viscous or low velocity flow.

## Common mistakes

- **Using the wrong velocity at a reducer.** K is tied to a reference diameter, usually the smaller one; using the velocity in the larger pipe can understate the loss by a factor of 5 or more.
- **Counting the exit twice.** The exit K of 1 is the kinetic energy thrown away into the tank; if the outlet velocity head is already counted as lost elsewhere, do not add it again.
- **Using fully open K for a throttled valve.** A butterfly valve at 30° open has a K many times its open value; use the valve's Cv or Kv at the actual opening.
- **Applying turbulent K values to laminar flow.** Below a Reynolds number of about 2,000, losses depend on viscosity and the simple K table underestimates them.
- **Forgetting strainers and instruments.** Y strainers, orifice plates and flow meters add their own losses, which can exceed all the elbows put together.
''',
     faq_add=[('Does the K value of a fitting change with flow rate?',
               'In fully turbulent flow K is close to constant, so the loss grows with velocity squared. At low Reynolds numbers K rises, which the 2-K and 3-K methods model with an extra term that falls as flow increases.'),
              ('Which pipe diameter should I use for the velocity at a reducer or enlargement?',
               'Use the diameter the K value is referenced to, normally the smaller pipe. Published sudden contraction and expansion coefficients are almost always given for the velocity in the small bore.')])

# ---------------------------------------------------------------- Hydraulic cylinder force
Pc, d, r = 160e5, 0.050, 0.028
Acap = math.pi * d ** 2 / 4
Aann = math.pi * (d ** 2 - r ** 2) / 4
Fp = Pc * Acap / 1000
Fpl = Pc * Aann / 1000
assert abs(Fp - 31.42) < 0.01 and abs(Fpl - 21.56) < 0.01
phi = Acap / Aann
# pressure for a 25 kN load with a 25% margin, 50 mm bore
load = 25e3
Freq = load * 1.25
p_req = Freq / Acap / 1e5
# retract speed with 20 L/min
Q = 20e-3 / 60
v_ext = Q / Acap
v_ret = Q / Aann
# intensification if the rod port is blocked
p_int = 160 * phi
# 3.5 tonne press with 210 bar: bore needed
Fpress = 10e3 * g0
bore_need = math.sqrt(4 * Fpress / (210e5 * math.pi)) * 1000
# psi table for common pressures on the default cylinder
p_rows = ''
for bar in (70, 100, 160, 210, 250):
    p_rows += f"| {bar} bar ({bar*14.5038:,.0f} psi) | {bar*1e5*Acap/1000:.1f} kN | {bar*1e5*Aann/1000:.1f} kN | {bar*1e5*Acap/g0/1000:.2f} t |\n"

edit('engineering/hydraulic-cylinder-force', date=U, phrase='hydraulic cylinder force calculator',
     intro=("A hydraulic cylinder turns oil pressure into a large straight-line force, equal to pressure times piston area. "
            "This hydraulic cylinder force calculator gives the push force on the full bore and the pull force on the smaller annulus left beside the rod, or the pressure needed for a load.\n\n"
            "Machine designers, maintenance fitters and press operators use it to size cylinders, set relief valves and check whether a cylinder can still lift its load."),
     replace=[('''
## Quick sizing tips

- Add a safety margin of **20–30%** over the calculated load.
- Check the rod for **buckling** on long strokes — slender rods can fail before the force limit is reached.
- Cylinder speed depends on pump flow: speed = flow ÷ effective area.
''', '')],
     body_add=f'''
## Pressure needed for a load

To lift a 25 kN load with the default 50 mm cylinder and a 25% margin, the cylinder must produce {Freq/1000:.2f} kN. The pressure is F ÷ A = {Freq:,.0f} N ÷ {Acap*1e4:.3f} cm² = **{p_req:.0f} bar**. In the calculator, clear Working pressure and enter {Freq/1000:.2f} kN as the push force.

For a 10 tonne press at 210 bar the minimum bore is √(4F ÷ πP) = **{bore_need:.1f} mm**, so the next standard size, 80 mm, is chosen.

## Extend and retract speed

With 20 L/min from the pump the default cylinder extends at {v_ext:.3f} m/s and retracts at **{v_ret:.3f} m/s**, because the annulus is only {Aann*1e4:.2f} cm² against {Acap*1e4:.2f} cm² for the full bore. The area ratio φ = {phi:.2f} also means the cap end returns {phi:.2f} times the oil the pump supplies during retraction, so the return line and filter must be sized for that larger flow.

## Force of the default cylinder at common pressures

| Pressure | Push | Pull | Push in tonnes |
|---|---|---|---|
{p_rows}
## Pressure intensification on the rod side

If the rod port is blocked while full pressure acts on the cap end, the oil trapped on the rod side is squeezed by the area ratio. At 160 bar on the default cylinder the rod side can reach **{p_int:.0f} bar**, enough to burst a hose or blow a seal rated for system pressure. Meter-out flow controls and pilot operated check valves on the rod port need this checked.

## Measuring the real force

Fit a gauge or pressure transducer at the cylinder port, not at the pump, because hoses and valves drop pressure during motion. The force on the load is then the port pressure times area minus seal friction, typically 2 to 5% of rated force. A load cell under the rod end gives the true force for press calibration.

## Common mistakes

- **Mixing bar and MPa.** 160 bar is 16 MPa; entering 160 MPa gives a force ten times too high.
- **Using the rod diameter as the annulus.** The pull area is π(d² − r²) ÷ 4, not π r² ÷ 4.
- **Reading pressure at the pump.** Pressure at the cylinder is lower while moving, so the force is less than the pump gauge suggests.
- **Assuming a single rod cylinder pulls as hard as it pushes.** Only a through rod (double rod) cylinder has equal areas on both sides; the default one pulls {Fpl/Fp*100:.0f}% of its push force.
- **Ignoring back pressure.** Pressure in the return line acts against the piston and reduces the net force.
''',
     faq_add=[('Can the rod side pressure be higher than the pump pressure?',
               f'Yes. If the rod port is blocked, cap end pressure is multiplied by the area ratio. The default cylinder at 160 bar can build about {p_int:.0f} bar on the rod side, which is why rod side components need a relief or a higher rating.'),
              ('How fast does a hydraulic cylinder retract?',
               f'Retract speed is flow divided by the annulus area. With 20 L/min the default 50/28 mm cylinder retracts at about {v_ret:.2f} m/s, faster than its {v_ext:.2f} m/s extend speed.')])

# ---------------------------------------------------------------- Mass flow rate
Qm, rhom = 50.0, 998.0
mm = Qm * rhom
assert mm == 49900.0
# compressed air: 500 Nm3/h, normal density 1.293 kg/m3
Qn = 500.0
rho_n = 101325 / (287.05 * 273.15)
m_air = Qn * rho_n
p_abs = 7e5 + 101325
T_act = 303.15
rho_act = p_abs / (287.05 * T_act)
Q_act = m_air / rho_act
# diesel: 2,000 kg/h at 835 kg/m3
m_d, rho_d = 2000.0, 835.0
Q_d = m_d / rho_d
Lmin_d = Q_d * 1000 / 60
# hot water check: same volume at 80 C, density 971.8
rho80 = 971.8
m80 = Qm * rho80
err = (mm - m80) / m80 * 100
u_rows = ''
for unit, fac, dd in (('kg/s', 1 / 3600, 2), ('kg/min', 1 / 60, 1), ('kg/h', 1, 0), ('t/h', 1e-3, 1), ('lb/h', 1 / 0.45359237, 0), ('t/day', 24e-3, 1)):
    u_rows += f"| {unit} | {mm*fac:,.{dd}f} |\n"

edit('engineering/mass-flow-rate', date=U, phrase='mass flow rate calculator',
     intro=("Mass flow is the amount of material passing per unit time, and unlike volume it does not change with temperature or pressure. "
            "This mass flow rate calculator converts volumetric flow to mass flow and back using density, in kg/h, t/h, lb/h, m³/h and L/min.\n\n"
            "Process, utility and billing engineers use it for energy balances, dosing and custody transfer; see the [difference between mass flow and volumetric flow](https://www.instrumentationblog.in/difference-between-mass-flow-and-volumetric-flow/) and how a [thermal mass flow meter works](https://www.instrumentationblog.in/thermal-mass-flow-meter-working/)."),
     faq_replace=[('Why is mass flow preferred over volume flow?',
                   'How do I convert Nm³/h of air to kg/h?',
                   f'Multiply by the normal density, about {rho_n:.3f} kg/m³ for dry air at 0 °C and 1.01325 bar(a). 500 Nm³/h is about {m_air:.0f} kg/h.')],
     body_add=f'''
## The default result in other units

The default 50 m³/h of water at 998 kg/m³ is 49,900 kg/h, which is:

| Unit | Mass flow |
|---|---|
{u_rows}
## Gas example: normal flow to actual flow

A compressor delivers **{Qn:g} Nm³/h** of air. Dry air at 0 °C and 1.01325 bar(a) has a density of p ÷ (R T) = 101,325 ÷ (287.05 × 273.15) = {rho_n:.3f} kg/m³, so the mass flow is **{m_air:.0f} kg/h**. In the 7 barg header at 30 °C the density is 801,325 ÷ (287.05 × 303.15) = {rho_act:.2f} kg/m³, so the same mass occupies only **{Q_act:.1f} m³/h** of actual volume. Pipe velocity and meter sizing use the actual figure; compressor ratings and billing use the normal one.

## Liquid fuel example

A burner needs **{m_d:,.0f} kg/h** of diesel at 835 kg/m³. Enter the mass flow and density and clear the volume: Q = 2,000 ÷ 835 = **{Q_d:.3f} m³/h**, or {Lmin_d:.1f} L/min, which is the figure for choosing a gear pump or a positive displacement meter.

## How mass flow is measured

A [Coriolis flow meter]({IB}coriolis-flow-meter-working-principle/) measures mass directly from the twist of vibrating tubes and also reports density. Most other meters (magnetic, vortex, turbine, differential pressure) measure volume or velocity, and the flow computer multiplies by a density calculated from temperature and pressure or from a densitometer. That density value is where most mass flow errors come from.

## Common mistakes

- **Using 998 kg/m³ for hot water.** At 80 °C water is about {rho80} kg/m³; using the cold value overstates the mass by {err:.1f}% on a volumetric meter.
- **Taking gauge pressure in the gas density.** p ÷ (R T) needs absolute pressure; 7 barg is 8.01 bar(a), not 7.
- **Mixing Nm³ and Sm³.** Normal (0 °C) and standard (15 °C or 60 °F) conditions differ by about 5% in density.
- **Converting specific gravity with 1,000 kg/m³ when the reference is 15 °C water.** SG values for oils are referenced to water at 15 °C or 60 °F (999.0 to 999.1 kg/m³), a small but real offset in custody transfer.
- **Confusing kg/h and kg/s.** A factor of 3,600 error is common when copying results into energy balances that need kg/s.
''',
     faq_add=[('How do I convert kg/h of diesel to litres per minute?',
               f'Divide by the density to get m³/h, multiply by 1,000 for L/h and divide by 60. {m_d:,.0f} kg/h at 835 kg/m³ is {Q_d:.3f} m³/h, about {Lmin_d:.1f} L/min.')])

print('slice 1 done')

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-21), slice 2: reynolds-number, pitot-tube-velocity, heat-duty, darcy-weisbach-head-loss, orifice-flow.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-21'
G = 9.80665
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Reynolds number
rho, v, D, mu = 998.0, 2.0, 0.1, 1.002e-3
Re0 = rho * v * D / mu
# air in a rectangular duct 400 x 200 mm at 6 m/s, 20 C
ra, mua, va = 1.204, 1.81e-5, 6.0
a_, b_ = 0.4, 0.2
Dh = 2 * a_ * b_ / (a_ + b_)
Rea = ra * va * Dh / mua
# velocity at which water in a 25 mm tube reaches Re 2300
vcrit = 2300 * mu / (rho * 0.025)
# laminar entrance length for 100 cP oil, 1 m/s, 50 mm (density 880)
Reo = 880 * 1.0 * 0.05 / 0.1
Le = 0.05 * Reo * 0.05
water = [(0, 999.8, 1.792), (20, 998.2, 1.002), (40, 992.2, 0.653), (60, 983.2, 0.467), (80, 971.8, 0.355), (100, 958.4, 0.282)]
w_rows = ''
for T, r, m in water:
    w_rows += f"| {T} °C | {r:g} | {m:g} | {c(r * 1.0 * 0.05 / (m / 1000))} |\n"
Re60 = 983.2 * 1.0 * 0.05 / 0.467e-3
Re0c = 999.8 * 1.0 * 0.05 / 1.792e-3

edit('engineering/reynolds-number', date=U, phrase='reynolds number calculator',
     intro=("The Reynolds number compares inertial and viscous forces in a moving fluid and tells you whether pipe flow is laminar, transitional or turbulent. "
            "This Reynolds number calculator works it out from density, velocity, inner diameter and dynamic viscosity, and shows the flow regime at once.\n\n"
            "Process and instrument engineers use it to choose friction factor correlations and to check that a flow meter is working inside its Reynolds limits. "
            "See [what Reynolds number is](https://www.instrumentationblog.in/what-is-reynolds-number/) for the background."),
     body_add=f'''
## Result with the default values

The defaults describe water at about 20 °C (998 kg/m³, 1.002 cP) at 2 m/s in a 100 mm bore. Re = 998 × 2 × 0.1 ÷ 0.001002 = **{c(Re0)}**, well into the turbulent band.

## Example: air in a rectangular duct

For a duct that is not round, use the hydraulic diameter D<sub>h</sub> = 4A ÷ P. A 400 × 200 mm duct has D<sub>h</sub> = 2 × 0.4 × 0.2 ÷ (0.4 + 0.2) = **{Dh*1000:.1f} mm**. With air at 20 °C (1.204 kg/m³, 0.0181 cP) moving at {va:g} m/s:

Re = 1.204 × {va:g} × {Dh:.4f} ÷ 0.0000181 = **{c(Rea)}**, turbulent. Enter {Dh*1000:.1f} mm as the diameter and 0.0181 cP as the viscosity to get the same figure.

Laminar flow in water needs very low speeds. In a 25 mm tube, water at 20 °C stays laminar only below about **{vcrit*1000:.0f} mm/s**. Viscous oils are the opposite case: a 100 cP oil (880 kg/m³) at 1 m/s in a 50 mm pipe gives Re = {Reo:.0f}, and the laminar velocity profile takes about 0.05 × Re × D = **{Le:.1f} m** of straight pipe to develop fully.

## Water temperature and Reynolds number

Viscosity falls quickly as water warms, so the same flow becomes more turbulent. Water at 1 m/s in a 50 mm bore:

| Temperature | Density (kg/m³) | Viscosity (cP) | Re |
|---|---|---|---|
{w_rows}
Between 0 °C and 60 °C the Reynolds number rises from {c(Re0c)} to {c(Re60)}, more than three and a half times, with no change in flow.

## How it is used in practice

Plant engineers rarely measure Reynolds number directly. They calculate it at minimum, normal and maximum flow from the process data sheet, using viscosity at operating temperature from the fluid supplier or a laboratory viscometer. The minimum flow case is the one that decides whether a vortex meter will keep counting or whether an orifice coefficient is still valid, so meter sizing tools print Re for each flow case.

## Common mistakes

- **Typing kinematic viscosity into the dynamic field.** Centistokes and centipoise are equal only when density is 1,000 kg/m³; for an oil at 880 kg/m³, 100 cSt is 88 cP.
- **Using nominal pipe size as the diameter.** A DN100 schedule 80 pipe has a bore of about 97 mm, not 100 mm, and the difference grows on small lines.
- **Taking viscosity at the wrong temperature.** Lube oil can change viscosity by a factor of ten between a cold start and normal running.
- **Using 2,300 for a non-circular duct without the hydraulic diameter.** The regime limits apply only when D<sub>h</sub> is used.
- **Using standard density for gas at line pressure.** Compressed air at 7 bar(g) is about eight times denser than free air, so its Reynolds number is about eight times higher at the same velocity.
''',
     faq_add=[('What diameter should I use for a rectangular duct?',
               f'Use the hydraulic diameter, four times the flow area divided by the wetted perimeter. A 400 by 200 mm duct has a hydraulic diameter of {Dh*1000:.1f} mm.'),
              ('Does warming water change its Reynolds number?',
               f'Yes, because viscosity drops. Water at 1 m/s in a 50 mm pipe has Re of about {c(Re0c, 0)} at 0 °C and about {c(Re60, 0)} at 60 °C.')])

# ---------------------------------------------------------------- Pitot tube
dP, rho_a, C = 500.0, 1.2, 1.0
v0 = C * math.sqrt(2 * dP / rho_a)
# S-type probe in a 150 C stack
R, M = 8.314462618, 0.02897
rho_s = 101325 * M / (R * 423.15)
dPs, Cs = 120.0, 0.84
vs = Cs * math.sqrt(2 * dPs / rho_s)
Ds = 1.2
As = math.pi / 4 * Ds ** 2
Qs = vs * As * 3600
vs_wrong = Cs * math.sqrt(2 * dPs / 1.2)
# traverse readings
trav = [410, 480, 520, 495, 430]
vels = [math.sqrt(2 * p / 1.2) for p in trav]
v_avg = sum(vels) / len(vels)
v_from_pavg = math.sqrt(2 * (sum(trav) / len(trav)) / 1.2)
inwc = 249.0889
i_rows = ''
for vp in (0.05, 0.1, 0.25, 0.5, 1.0, 2.0):
    vv = math.sqrt(2 * vp * inwc / 1.2)
    i_rows += f"| {vp:g} inH₂O | {vp*inwc:.1f} Pa | {vv:.2f} m/s | {c(vv / 0.3048 * 60)} ft/min |\n"
mm5 = 5 * 9.80665

edit('engineering/pitot-tube-velocity', date=U, phrase='pitot tube velocity calculator',
     intro=("A Pitot tube measures flow velocity from the difference between the total pressure facing the flow and the static pressure. "
            "This Pitot tube velocity calculator turns that velocity pressure, the fluid density and the probe coefficient into velocity, or works back to the expected pressure.\n\n"
            "HVAC balancing technicians, stack testers and flow engineers use it on ducts, chimneys and pipes, and an [averaging Pitot tube](https://www.instrumentationblog.in/averaging-pitot-tube-working-principle/) extends the idea to pipe flow."),
     body_add=f'''
## Example: S-type probe in a hot stack

Stack testing uses S-type probes, which need a coefficient of about 0.84, and the gas is far lighter than room air. Flue gas close to the molar mass of air at 150 °C and 101.325 kPa has a density of 101,325 × 0.02897 ÷ (8.314 × 423.15) = **{rho_s:.3f} kg/m³**. With a reading of {dPs:g} Pa:

- v = 0.84 × √(2 × {dPs:g} ÷ {rho_s:.3f}) = **{vs:.2f} m/s**
- Stack area for a {Ds:g} m diameter = {As:.3f} m², so the flow is about **{c(Qs)} m³/h** at stack conditions

Had the default 1.2 kg/m³ been left in, the velocity would read {vs_wrong:.2f} m/s, about {100*(1-vs_wrong/vs):.0f}% low.

## Average the velocities, not the pressures

Five readings across a duct of 410, 480, 520, 495 and 430 Pa give velocities that average **{v_avg:.3f} m/s**. Averaging the pressures first and then taking the square root gives {v_from_pavg:.3f} m/s. The gap is small here, but it grows when the profile is uneven near dampers and bends, and the pressure average always reads high.

## Inches of water to velocity

US gauges and balancing reports often use inches of water column. For standard air (1.2 kg/m³), velocity in ft/min is close to 4,005 × √(inH₂O):

| Velocity pressure | Pascal | Velocity | Velocity |
|---|---|---|---|
{i_rows}
## How it is measured in practice

The probe's total port faces upstream and the static ports sit on the side of the stem. Both connect to an inclined manometer or a digital micromanometer that reads the difference directly. Test points are drilled at least 7.5 duct diameters downstream of a bend or fan where possible, and the traverse positions follow the log-Tchebycheff or equal-area pattern. On wet or dusty stacks the lines are purged between readings and checked for leaks before and after the run.

## Common mistakes

- **Using room air density for hot or humid gas.** Correct density for temperature, static pressure and moisture, as in the stack example.
- **Leaving C at 1.0 for an S-type probe.** S-type probes read a larger differential than a Prandtl tube and need their calibration coefficient, usually 0.82 to 0.86.
- **Mixing pressure units.** 5 mm of water is {mm5:.1f} Pa, not 5 Pa; enter the value in the unit shown on the gauge.
- **Swapping the tubing.** Total and static lines reversed give a negative or near zero reading, and on an S-type probe a wrong orientation gives a different coefficient.
- **Reading in swirling flow.** Behind a fan or an elbow the flow is not parallel to the probe, so the tip sees only part of the dynamic pressure.
''',
     faq_add=[('How do I correct a Pitot reading for hot flue gas?',
               f'Use the gas density at stack temperature and pressure. At 150 °C and atmospheric pressure, air-like flue gas is about {rho_s:.3f} kg/m³, so 120 Pa on an S-type probe (C = 0.84) means {vs:.2f} m/s.'),
              ('How do I convert inches of water to air velocity in feet per minute?',
               f'For standard air, velocity in ft/min is about 4,005 × √(velocity pressure in inH₂O). A reading of 0.5 inH₂O gives about {c(math.sqrt(2*0.5*inwc/1.2)/0.3048*60)} ft/min.')])

# ---------------------------------------------------------------- Heat duty
m, cp, dT = 2.0, 4.186, 10.0
Q0 = m * cp * dT
# chilled water energy meter
Vh, rw, cpw = 36.0, 999.7, 4.192
mw = Vh * rw / 3600
Qc = mw * cpw * 5
TRc = Qc / 3.517
err01 = 0.1 / 5 * 100
# heat balance: thermal oil heating water
mo, cpo, To1, To2 = 3.0, 2.3, 220.0, 180.0
Qo = mo * cpo * (To1 - To2)
dTw = Qo / (2.0 * 4.186)
fl = [('Water', 4.186, 998), ('Glycol 30%', 3.7, 1040), ('Thermal oil', 2.2, 850)]
f_rows = ''
for nm, cc, rr in fl:
    f_rows += f"| {nm} | " + ' | '.join(f"{100 / (cc * d) / rr * 3600:.1f}" for d in (5, 10, 15, 20)) + ' |\n'

edit('engineering/heat_duty'.replace('_', '-'), date=U, phrase='heat duty calculator',
     intro=("Heat duty is the rate at which heat is added to or removed from a fluid stream, set by its mass flow, specific heat and temperature change. "
            "This heat duty calculator applies Q = ṁ × cp × ΔT and gives the result in kW or hp.\n\n"
            "Process and HVAC engineers use it to size heat exchangers, chillers, heaters and boilers, and to check energy meter readings against the design load."),
     body_add=f'''
## Result with the default values

The defaults are {m:g} kg/s of water, c<sub>p</sub> = {cp} kJ/kg·K and a {dT:g} K change, so Q = {m:g} × {cp} × {dT:g} = **{Q0:.2f} kW**.

## Example: checking a chilled water energy meter

A chilled water branch carries {Vh:g} m³/h of water supplied at 7 °C and returned at 12 °C. At about 10 °C water has a density of {rw} kg/m³ and c<sub>p</sub> of {cpw} kJ/kg·K:

- Mass flow = {Vh:g} × {rw} ÷ 3,600 = **{mw:.3f} kg/s**
- Q = {mw:.3f} × {cpw} × 5 = **{Qc:.1f} kW**, or {TRc:.1f} TR

Because the ΔT is only 5 K, a 0.1 K error between the two temperature sensors changes the duty by {err01:.0f}%. That is why energy meters use matched sensor pairs and why low ΔT loops are hard to bill accurately.

## Example: hot and cold side balance

A thermal oil heater circuit delivers {mo:g} kg/s of oil (c<sub>p</sub> about {cpo} kJ/kg·K) that cools from {To1:g} °C to {To2:g} °C in an exchanger. The oil gives up {mo:g} × {cpo} × {To1-To2:g} = **{Qo:.0f} kW**. If that heat goes into {m:g} kg/s of water, the water warms by {Qo:.0f} ÷ ({m:g} × 4.186) = **{dTw:.1f} K**. Measured duties on the two sides usually agree within a few percent; a larger gap points to a bad flow or temperature reading, or heat lost through poor insulation.

## Flow needed to carry 100 kW

Volumetric flow in m³/h for each fluid and design temperature difference:

| Fluid | ΔT 5 K | ΔT 10 K | ΔT 15 K | ΔT 20 K |
|---|---|---|---|---|
{f_rows}
Lower specific heat and density both push the flow up, so a glycol or oil system needs bigger pumps and pipes for the same load.

## Common mistakes

- **Entering volumetric flow as mass flow.** 2 m³/h is not 2 kg/s; convert with density first ({c(2*998/3600, 3)} kg/s for water).
- **Mixing kJ and kW.** With mass flow in kg/s and c<sub>p</sub> in kJ/kg·K the result is kW; with kg/h it is kJ/h, 3,600 times larger.
- **Using the water c<sub>p</sub> for glycol mixtures.** A 30% glycol solution has about 12% less heat capacity, so the duty is overstated.
- **Applying the formula across a phase change.** Boiling or condensing duty is mass flow times latent heat, which c<sub>p</sub> × ΔT does not capture.
- **Converting a °F difference like a temperature.** An 18 °F rise is 10 K, not −7.8 °C.
''',
     faq_add=[('Why does a small temperature difference make heat duty readings inaccurate?',
               f'The duty is directly proportional to ΔT, so a fixed sensor error is a larger share of a small difference. At 5 K, a 0.1 K mismatch between sensors is a {err01:.0f}% error in duty.'),
              ('How do I check that both sides of a heat exchanger agree?',
               'Work out ṁ × cp × ΔT for the hot stream and for the cold stream. They should match within a few percent; a bigger difference means a faulty flow or temperature reading, or heat loss to the surroundings.')])

# ---------------------------------------------------------------- Darcy-Weisbach
f, L, Dd, vd, rd = 0.02, 100.0, 0.1, 1.77, 998.0
hf0 = f * (L / Dd) * vd ** 2 / (2 * G)
dP0 = rd * G * hf0 / 1e5
mu_w = 1.002e-3
Re_d = rd * vd * Dd / mu_w
eps = 0.045e-3


def sj(Re, eps, D):
    return 0.25 / math.log10(eps / (3.7 * D) + 5.74 / Re ** 0.9) ** 2


f_sj = sj(Re_d, eps, Dd)
hf_sj = f_sj * (L / Dd) * vd ** 2 / (2 * G)
Ksum = 6 * 0.75 + 0.15 + 1.0
hk = Ksum * vd ** 2 / (2 * G)
htot = hf_sj + hk
# flow +20%
v12 = vd * 1.2
f12 = sj(rd * v12 * Dd / mu_w, eps, Dd)
ratio12 = (f12 * v12 ** 2) / (f_sj * vd ** 2)
t_rows = ''
for dn, Di in (('DN25', 0.0266), ('DN50', 0.0525), ('DN80', 0.0779), ('DN100', 0.1023), ('DN150', 0.1541)):
    cells = []
    for vv in (1.0, 1.5, 2.0):
        ff = sj(998 * vv * Di / mu_w, eps, Di)
        cells.append(f"{998 * ff * (100 / Di) * vv ** 2 / 2 / 1e5:.3f}")
    t_rows += f"| {dn} ({Di*1000:.1f} mm) | " + ' | '.join(cells) + ' |\n'

edit('engineering/darcy-weisbach-head-loss', date=U, phrase='pipe pressure drop calculator',
     intro=("Friction between a moving fluid and the pipe wall causes a pressure drop that pumps must overcome. "
            "This pipe pressure drop calculator uses the Darcy Weisbach equation with your friction factor, length, bore, velocity and density, as explained in [how to calculate pressure drop in pipes](https://www.instrumentationblog.in/calculate-pressure-drop-in-pipes/).\n\n"
            "Piping and pump engineers use it to size lines and pumps, and the equation builds on [Bernoulli's equation](https://www.instrumentationblog.in/bernoullis-equation-formula/)."),
     body_add=f'''
## Friction factor for the default case

The default f = 0.02 is a round figure. For water at 20 °C in the same 100 mm new steel pipe at 1.77 m/s, Re = 998 × 1.77 × 0.1 ÷ 0.001002 = {c(Re_d)}. With ε = 0.045 mm the Swamee Jain equation gives **f = {f_sj:.4f}**, so the straight pipe loss is {hf_sj:.2f} m instead of the {hf0:.2f} m shown with the default ({dP0:.3f} bar).

Now add six standard elbows (K = 0.75 each), an open gate valve (0.15) and the pipe exit (1.0). ΣK = {Ksum:.2f} and the fitting loss is {Ksum:.2f} × 1.77² ÷ (2 × 9.807) = **{hk:.2f} m**. The total for pump sizing is about **{htot:.2f} m**, so the fittings add {100*hk/hf_sj:.0f}% to the straight run.

## Pressure drop per 100 m of new steel pipe

Water at 20 °C, ε = 0.045 mm, friction factor from Swamee Jain, result in bar per 100 m:

| Pipe (bore) | 1.0 m/s | 1.5 m/s | 2.0 m/s |
|---|---|---|---|
{t_rows}
At the same velocity, small pipes lose much more per metre because L ÷ D is larger and their relative roughness is higher.

## Measuring friction loss on site

Fit two pressure gauges or a DP transmitter on a straight run with no fittings between them, ideally 50 diameters or more apart. Correct the reading for any height difference between the tappings (9.81 kPa per metre of water), then divide by ρg to get h<sub>f</sub>. Back-calculating f from a measured drop and a known flow shows how much an old line has scaled up compared with its design.

## Common mistakes

- **Using the Fanning factor.** A Fanning value of 0.005 is a Darcy value of 0.02; using it here underestimates the loss four times.
- **Using nominal size for the bore.** DN100 schedule 40 has a 102.3 mm bore, and the loss is very sensitive to diameter.
- **Counting elevation as friction.** Static head from a height change is separate from h<sub>f</sub> and must be added on its own.
- **Keeping f fixed when the flow changes.** In turbulent flow f falls slightly as Re rises; a 20% increase in flow raises the loss by a factor of {ratio12:.2f}, not exactly 1.44.
- **Designing with new pipe roughness for an old system.** Scaled or tuberculated steel can be several times rougher than new pipe.
''',
     faq_add=[('Can I measure pipe friction loss with two pressure gauges?',
               'Yes, on a straight run without fittings. Subtract the downstream reading from the upstream one, correct for any height difference between the gauges, and divide by ρg to get the friction head.'),
              ('How much does pressure drop rise if flow increases by 20%?',
               f'Roughly with the square of flow, so about 1.44 times. Because the friction factor falls a little as Re rises, the default 100 mm steel case gives {ratio12:.2f} times.')])

# ---------------------------------------------------------------- Orifice flow
Do, do, Cd, dPo, ro = 0.1, 0.05, 0.61, 25000.0, 998.0
bo = do / Do
Ao = math.pi * do ** 2 / 4
k = Cd * Ao * math.sqrt(2 / (ro * (1 - bo ** 4)))
Qo0 = k * math.sqrt(dPo) * 3600
# range for 40 m3/h max
Qmax = 40.0
dPmax = (Qmax / 3600 / k) ** 2
Re_o = ro * (Qo0 / 3600) / (math.pi * Do ** 2 / 4) * Do / 1.002e-3
loss = (1 - bo ** 1.9) * dPo
p_rows = ''
for pct in (1, 4, 10, 25, 50, 100):
    q = math.sqrt(pct / 100)
    p_rows += f"| {pct}% | {dPmax*pct/100/100:.1f} mbar | {q*100:.1f}% | {Qmax*q:.1f} m³/h |\n"

edit('engineering/orifice-flow', date=U, phrase='orifice plate flow calculator',
     intro=("The orifice plate is a thin plate with a bore that creates a differential pressure proportional to the square of flow. "
            "This orifice plate flow calculator gives liquid flow from that DP, the bore, the pipe size and density, as covered in [orifice plate flow measurement](https://www.instrumentationblog.in/orifice-plate-flow-measurement/).\n\n"
            "Instrument engineers use it to check plates, set DP transmitter ranges and compare elements, using the [orifice plate sizing guide](https://www.instrumentationblog.in/orifice-plate-sizing-guide/) and [flow nozzle vs orifice plate vs Venturi](https://www.instrumentationblog.in/flow-nozzle-vs-orifice-plate-vs-venturi/)."),
     body_add=f'''
## Example: setting the transmitter range

With the default plate ({do*1000:.0f} mm bore in a {Do*1000:.0f} mm pipe, β = {bo:g}, C<sub>d</sub> = {Cd}) and water at {ro:g} kg/m³, 250 mbar gives **{Qo0:.2f} m³/h**. Suppose the line must read up to {Qmax:g} m³/h. Because flow follows √ΔP, the DP at maximum flow is 250 × ({Qmax:g} ÷ {Qo0:.2f})² = **{dPmax/100:.0f} mbar**, so a 0 to {dPmax/100:.0f} mbar transmitter range (or the next round value above it) suits this plate.

At the default flow the pipe Reynolds number is about {c(Re_o)}, comfortably in the range where a fixed C<sub>d</sub> of 0.61 is reasonable. The permanent loss at 250 mbar is about (1 − 0.5<sup>1.9</sup>) × 250 = **{loss/100:.0f} mbar**.

## Square root relationship for this plate

| DP (% of range) | DP | Flow (% of max) | Flow |
|---|---|---|---|
{p_rows}
The bottom of the table shows the turndown problem: the first 10% of the DP range covers almost a third of the flow, so small DP errors near zero become large flow errors. Most systems apply a low flow cutoff near 5 to 10% of flow.

## How it is installed and read

The plate sits between flanges with its sharp, square edge facing upstream and the bevel downstream. Impulse lines run from the taps to a DP transmitter through a three-valve or five-valve manifold, sloped so that gas vents back to the pipe on liquid service. The square root is extracted once, either in the transmitter or in the control system, and the zero is checked by opening the equalising valve.

## Common mistakes

- **Taking the square root twice.** If the transmitter output is already linear in flow, the DCS input must be set to linear, or the reading is badly low across the range.
- **Fitting the plate backwards.** With the bevel facing upstream the discharge coefficient rises and the meter reads several percent low.
- **Gas trapped in liquid impulse lines.** A bubble in one leg adds a false head and shifts the zero.
- **Using design density at a different temperature.** Hot water at 90 °C is about 965 kg/m³, which changes the flow by about 1.7% for the same DP.
- **Ignoring a worn or dirty edge.** A rounded edge or deposits on the upstream face raise C<sub>d</sub>, so an old plate reads low.
''',
     faq_add=[('What happens if an orifice plate is installed backwards?',
               'With the bevelled side facing upstream the jet contracts less, the discharge coefficient rises and the meter reads low by several percent. Check the tab marking, which normally shows the upstream side and the bore.'),
              ('How do I choose the DP range for an orifice transmitter?',
               f'Scale the known flow and DP to the maximum flow: DP_max = DP × (Q_max ÷ Q)². For the default plate, 40 m³/h needs about {dPmax/100:.0f} mbar.')])

print('slice 2 done')

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-21), slice 3: pt100-resistance, flow-meter-k-factor, pipe-flow-velocity, dew-point, npsh-available.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-21'
IB = 'https://www.instrumentationblog.in/'
G = 9.80665

# ---------------------------------------------------------------- Pt100 resistance
A, B = 3.9083e-3, -5.775e-7


def rtd(t, r0=100.0):
    return r0 * (1 + A * t + B * t * t)


def rtd_inv(r, r0=100.0):
    return (-A + math.sqrt(A * A - 4 * B * (1 - r / r0))) / (2 * B)


R100 = rtd(100)
R1000 = rtd(100, 1000)
r_read = 175.00
t_read = rtd_inv(r_read)
# same reading, 2-wire with 1.4 ohm loop lead resistance
lead = 1.4
t_2w = rtd_inv(r_read - lead)
# excitation voltage at 1 mA
I_ex = 1e-3
V100 = R100 * I_ex * 1000  # mV
# sensitivity table
s_rows = ''
for t in (0, 100, 200, 300, 400, 600, 850):
    s = 100 * (A + 2 * B * t)
    tolA = 0.15 + 0.002 * t
    s_rows += f"| {t} °C | {rtd(t):.2f} Ω | {s:.4f} Ω/°C | {10*s:.3f} Ω/°C | ±{tolA:.2f} °C = ±{tolA*s:.3f} Ω |\n"
s0 = 100 * A
s400 = 100 * (A + 2 * B * 400)

edit('engineering/pt100-resistance', date=U, phrase='pt100 resistance calculator',
     intro=("A Pt100 is a platinum resistance thermometer with 100 Ω at 0 °C, and its resistance rises in a known way as it gets hotter. "
            "This Pt100 resistance calculator converts temperature to ohms and back for Pt100, Pt500 and Pt1000 sensors using the "
            f"[Callendar Van Dusen equation]({IB}callendar-van-dusen-equation-rtd/).\n\n"
            f"Instrument technicians use it to check a sensor with a multimeter, as in [how to test an RTD]({IB}how-to-test-an-rtd-pt100/), "
            f"and to simulate a temperature with a decade box. The [Pt100 vs Pt1000 differences]({IB}rtd-pt100-vs-pt1000-differences/) matter when choosing one."),
     body_add=f'''
## Worked example: resistance reading to temperature

The default case is a Pt100 at 100 °C, which the calculator gives as **{R100:.2f} Ω** (a Pt1000 at the same temperature reads {R1000:.1f} Ω). Going the other way needs the quadratic solved for t:

<p class="formula">t = [−A + √(A² − 4B(1 − R/R₀))] ÷ (2B)</p>

Suppose a 4-wire meter reads **{r_read:.2f} Ω** across a Pt100. Then t = **{t_read:.2f} °C**. If the same sensor is wired 2-wire through cable with {lead} Ω of loop resistance, the instrument sees the extra ohms as heat; correcting for them gives {t_2w:.2f} °C, so the uncorrected reading is about **{t_read - t_2w:.1f} °C high**.

## Sensitivity and tolerance in ohms

The slope dR/dt = R₀(A + 2Bt) falls slowly with temperature because B is negative, so one ohm means a little more temperature at the hot end. Class A tolerance converted to ohms is what you compare with a resistance check on the bench.

| Temperature | Pt100 resistance | Pt100 slope | Pt1000 slope | Class A tolerance |
|---|---|---|---|---|
{s_rows}
At 0 °C a Pt100 changes {s0:.4f} Ω per degree; at 400 °C only {s400:.4f} Ω, about {100*(1-s400/s0):.0f}% less.

## How the resistance is measured in practice

A transmitter or PLC RTD card pushes a small constant current through the element and reads the voltage across it. At 1 mA a Pt100 at 100 °C develops only {V100:.1f} mV, so the input must resolve microvolts, and thermocouple effects at dissimilar terminals can matter on low-level signals. For a field check, disconnect the sensor, measure the element with a 4-wire ohmmeter or a calibrator, and compare with the table. To test the transmitter instead, connect a decade box or RTD simulator in place of the sensor and dial in the resistance for each test point; a [Pt100 calibration guide]({IB}pt100-rtd-calibration-guide/) covers the full procedure.

## Common mistakes

- **Setting a Pt1000 input and connecting a Pt100.** The transmitter reads about one tenth of the expected resistance and shows a temperature near −200 °C or an underrange fault.
- **Using the 0.385 Ω/°C average for precise work.** It is the mean slope from 0 to 100 °C; at 400 °C the real slope is {s400:.3f} Ω/°C, so linear estimates drift by several degrees at high temperature.
- **Measuring with a cheap 2-wire multimeter.** The probe leads and contact resistance add a few tenths of an ohm, which is already close to 1 °C on a Pt100.
- **Forgetting the alpha of the sensor.** Some older or US sensors use α = 0.003916 or 0.003920 instead of the IEC 0.00385, and their resistance at 100 °C differs by about 0.6 Ω.
- **Checking a hot sensor while it is still in the process.** Remove it or read it at a known reference such as an ice bath; otherwise you cannot tell sensor drift from a real temperature change.
''',
     faq_add=[('How do I convert a Pt100 resistance reading to temperature?',
               f'Solve the IEC 60751 quadratic: t = [−A + √(A² − 4B(1 − R/100))] ÷ 2B, with A = 3.9083 × 10⁻³ and B = −5.775 × 10⁻⁷. A reading of {r_read:.2f} Ω gives {t_read:.2f} °C. Enter the resistance and press × on Temperature to let the calculator do it.'),
              ('What voltage does a Pt100 give at 1 mA?',
               f'V = I × R, so {V100:.1f} mV at 100 °C and 100 mV at 0 °C. The change is only about 0.39 mV per °C, which is why RTD inputs need high resolution and good shielding.')])

# ---------------------------------------------------------------- Flow meter K-factor
K, Qlm = 450.0, 6.0
f0 = K * Qlm / 60
assert abs(f0 - 45) < 1e-9
# bucket / prover test
pulses_test, vol_test = 22610, 50.0
K_test = pulses_test / vol_test
err = (K - K_test) / K_test * 100  # positive: nominal K too high => indicated volume low
ind_vol = pulses_test / K
# batch: 200 L batch, preset counts
batch = 200.0
counts = batch * K
# PLC scan: max flow 20 L/min
fmax = K * 20 / 60
period_ms = 1000 / fmax
# gpm meter: K = 1,700 pulses/US gal at 25 gpm
Kg, gpm = 1700.0, 25.0
f_g = Kg * gpm / 60
K_L = Kg / 3.785411784
f_rows = ''
for k in (1.0, 5.0, 50.0, 450.0, 1000.0):
    f_rows += f"| {k:g} pulse{'s' if k != 1 else ''}/L | " + ' | '.join(f"{k*q/60:,.2f} Hz" if k*q/60 < 100 else f"{k*q/60:,.0f} Hz" for q in (1, 10, 100, 1000)) + ' |\n'

edit('engineering/flow-meter-k-factor', date=U, phrase='flow meter k-factor calculator',
     intro=("Pulse output flow meters such as turbine, vortex, paddle wheel and gear meters send a fixed number of pulses for each litre that passes. "
            "This flow meter K-factor calculator converts that K-factor and the flow rate into pulse frequency, or a measured frequency back into flow.\n\n"
            f"Instrument and PLC engineers use it to set up counters and scaling, check a meter against a test volume, and confirm an input card can follow the maximum frequency, as covered in these [flow meter K-factor calculations]({IB}flow-meter-k-factor-calculations/)."),
     body_add=f'''
## Second example: checking K with a test volume

The default case gives **{f0:.0f} Hz** at {Qlm:g} L/min with K = {K:g} pulses/L. On site you rarely trust the nameplate alone. Run the meter into a calibrated {vol_test:g} L vessel and count the pulses: say the counter shows **{pulses_test:,}** pulses.

- Measured K = {pulses_test:,} ÷ {vol_test:g} = **{K_test:.1f} pulses/L**
- With the nominal {K:g} pulses/L the PLC would have shown {ind_vol:.2f} L, which is {abs(err):.2f}% {'low' if err > 0 else 'high'}
- Entering {K_test:.1f} in the scaling (or a meter factor of {K/K_test:.4f}) removes that error

For a {batch:g} L batch the counter preset is {batch:g} × {K_test:.1f} = **{batch*K_test:,.0f} pulses**, not the {counts:,.0f} pulses the nominal K gives.

## Frequency at different K-factors and flows

| K-factor | 1 L/min | 10 L/min | 100 L/min | 1,000 L/min |
|---|---|---|---|---|
{f_rows}
A meter rated in US gallons works the same way: K = {Kg:,.0f} pulses/gal at {gpm:g} gpm gives {f_g:,.1f} Hz, and the same K is {K_L:.1f} pulses/L.

## How the pulses are counted in practice

A PLC can only count pulses in its normal digital input logic if each pulse lasts longer than one scan. At the 20 L/min maximum of this meter the frequency is {fmax:.0f} Hz, a period of {period_ms:.1f} ms, so a 10 ms scan would miss pulses. Wire the meter to a high speed counter input and read the accumulated count instead. Also check the input filter: many digital inputs have a default 3 to 10 ms debounce that silently drops fast pulses. Reed switch outputs on water meters are the opposite case and need debounce, because contact bounce creates extra counts. For the meter itself, [how a turbine flow meter works]({IB}turbine-flow-meter-working-principle/) explains why the rotor speed and therefore the pulse rate is proportional to velocity.

## Common mistakes

- **Mixing pulses per gallon with pulses per litre.** The error is a factor of 3.785, which is too big to miss on a total but easy to miss on a rate display nobody checks.
- **Reading the rate in a normal scan.** Missed pulses make the meter read low only at high flow, which looks like a meter fault.
- **Calculating rate from too short a gate time.** At 1 pulse per litre and 10 L/min there is one pulse every 6 s, so a 1 s rate window jumps between 0 and 60 L/min. Measure the time between pulses instead.
- **Keeping the water K-factor for a viscous liquid.** Turbine meters slow down in oil, so K can shift by several percent; calibrate on the real product.
- **Ignoring flow below the linear range.** Under the minimum rated flow, bearing friction makes K fall sharply and the totaliser under-registers.
''',
     faq_add=[('Why does my PLC count fewer pulses than the flow meter sends?',
               f'Usually because the pulses are read by a normal input in the PLC scan or blocked by the input filter. At {fmax:.0f} Hz each pulse lasts {period_ms:.1f} ms, shorter than a typical scan, so use a high speed counter input with the filter set below the pulse width.'),
              ('What is a meter factor and how is it different from the K-factor?',
               f'The K-factor is pulses per unit volume. A meter factor is a small correction, actual volume divided by indicated volume, found by proving the meter. In the test above the meter factor is {K/K_test:.4f}.')])

# ---------------------------------------------------------------- Pipe flow velocity
Qh, Dm = 50.0, 0.100
Q = Qh / 3600
Ar = math.pi * Dm ** 2 / 4
v0 = Q / Ar
# suction line sizing at 1.5 m/s
vs = 1.5
Dreq = math.sqrt(4 * Q / (math.pi * vs)) * 1000
ID125 = 128.2  # DN125 schedule 40 inner diameter, mm
v125 = Q / (math.pi * (ID125 / 1000) ** 2 / 4)
ID100 = 102.26
v100 = Q / (math.pi * (ID100 / 1000) ** 2 / 4)
# reducer continuity DN100 -> DN50 (ID 52.5)
v50 = v100 * (ID100 / 52.5) ** 2
# PE100 SDR11 table
pe_rows = ''
for OD in (63, 90, 110, 160, 225):
    e = OD / 11
    ID = OD - 2 * e
    a = math.pi * (ID / 1000) ** 2 / 4
    pe_rows += f"| {OD} mm | {e:.1f} mm | {ID:.1f} mm | " + ' | '.join(f"{q/3600/a:.2f} m/s" for q in (10, 30, 60)) + ' |\n'
hv0 = v0 ** 2 / (2 * G)

edit('engineering/pipe-flow-velocity', date=U, phrase='pipe flow velocity calculator',
     intro=("Fluid velocity in a pipe sets the pressure drop, noise, erosion and the size of a water hammer surge. "
            "This pipe flow velocity calculator finds the average velocity from the flow rate and inner diameter, or the flow or diameter for a target velocity.\n\n"
            "Piping and process engineers use it to size suction and discharge lines, while instrument engineers use it to check that a flow meter will run inside its velocity range."),
     body_add=f'''
## Sizing a pump suction line from the default flow

The default case, {Qh:g} m³/h through a 100 mm bore, gives **{v0:.2f} m/s** and a cross-section of {Ar*1e4:.2f} cm², which is fine for a discharge line but too fast for a pump suction. Targeting {vs:g} m/s:

- D = √(4 × {Q:.5f} ÷ (π × {vs:g})) = **{Dreq:.1f} mm** minimum bore
- DN100 schedule 40 ({ID100} mm bore) would run at {v100:.2f} m/s, so the next size up is used
- DN125 schedule 40 ({ID125} mm bore) gives **{v125:.2f} m/s**, comfortably inside the suction range

The same flow squeezed through a DN50 reducer (52.5 mm bore) speeds up to {v50:.2f} m/s, since velocity scales with the inverse square of the bore. The velocity head v²/2g at the default {v0:.2f} m/s is {hv0:.3f} m, which is the head lost at a pipe exit into a tank.

## Velocity in PE100 SDR11 plastic pipe

Polyethylene pipe is sold by outside diameter, and the wall is the OD divided by the SDR, so the bore is much smaller than the nominal size suggests.

| Outside diameter | Wall | Bore | 10 m³/h | 30 m³/h | 60 m³/h |
|---|---|---|---|---|---|
{pe_rows}
## How velocity is measured in practice

The calculator gives the mean velocity, flow divided by area. A clamp on ultrasonic meter measures it directly from transit time across the pipe, but you must type the real outside diameter and wall thickness into it, or the flow it reports is wrong by the same area error. A pitot tube or insertion probe reads a point velocity; in fully developed turbulent flow the centreline velocity is roughly 1.2 times the mean, so a single centre reading overstates flow unless a profile factor is applied. To find the true wall thickness on an old line, use an ultrasonic thickness gauge rather than the schedule tables, because corrosion and scale change the bore.

## Common mistakes

- **Using the nominal size as the bore.** DN100 schedule 80 has a 97.2 mm bore, and a cement lined ductile iron pipe of the same DN is smaller still.
- **Mixing m³/h with m³/s.** A factor of 3,600 error usually shows up as an impossible velocity of thousands of metres per second.
- **Applying the full bore area to a partly full drain.** Gravity drains and sewers seldom run full, so the wetted area is smaller and the real velocity differs.
- **Using normal m³/h for a gas line.** Compressors and gas meters often quote flow at reference conditions; at 7 bar gauge the actual volume is about one eighth, and so is the velocity.
- **Sizing on average flow only.** Check the peak flow too, because noise and erosion follow the highest velocity the line will see.
''',
     faq_add=[('How do I find the inner diameter of a pipe?',
               'Subtract twice the wall thickness from the outside diameter. A DN100 schedule 40 steel pipe is 114.3 mm OD with a 6.02 mm wall, so the bore is 102.26 mm. For plastic pipe, the wall is the OD divided by the SDR.'),
              ('What happens to velocity when a pipe reduces in size?',
               f'The flow stays the same, so velocity rises with the square of the diameter ratio. Going from a 102.3 mm to a 52.5 mm bore raises {v100:.2f} m/s to {v50:.2f} m/s, nearly four times faster.')])

# ---------------------------------------------------------------- Dew point
b, cc = 17.625, 243.04


def es_kpa(t):
    return 0.61094 * math.exp(b * t / (t + cc))


def dew(t, rh):
    g = math.log(rh) + b * t / (cc + t)
    return cc * g / (b - g)


def dew_from_ea(ea):
    g = math.log(ea / 0.61094)
    return cc * g / (b - g)


Td0 = dew(25, 0.6)
assert abs(Td0 - 16.70) < 0.01
# chilled water pipe at 14 C in plant room 28 C 55% RH
Tp = dew(28, 0.55)
# painting: steel 18 C, air 20 C, RH 85%
Tpaint = dew(20, 0.85)
# compressed air: pressure dew point 3 C at 8 bar abs, expanded to 1.013 bar abs
pdp, P2, P1 = 3.0, 8.0, 1.01325
ea_line = es_kpa(pdp)
adp = dew_from_ea(ea_line * P1 / P2)
# warming air: 10 C 80% heated to 22 C
Td_w = dew(10, 0.8)
rh_w = es_kpa(Td_w) / es_kpa(22) * 100

edit('engineering/dew-point', date=U, phrase='dew point calculator',
     intro=("The dew point is the temperature at which air becomes saturated and water starts to condense on a surface. "
            "This dew point calculator finds it from the dry bulb temperature and relative humidity with the Magnus formula, and also gives the vapour pressure, absolute humidity and the margin to condensation.\n\n"
            f"HVAC engineers, coating inspectors and instrument technicians use it to stop sweating pipes, approve painting conditions and check [dew point in instrument air]({IB}dew-point-in-instrument-air-risks/), or to read a [capacitive RH sensor]({IB}humidity-sensor-capacitive-rh/) as a dew point."),
     body_add=f'''
## More examples from site work

**Sweating chilled water pipe.** A plant room is at 28 °C and 55% RH, and an uninsulated chilled water line runs at 14 °C. The dew point of the room air is {Tp:.1f} °C, so the pipe surface is {Tp-14:.1f} °C below it and will drip. Insulation must keep the outer surface above {Tp:.1f} °C, with a vapour barrier so moist air cannot reach the cold metal.

**Painting a tank in the morning.** Air at 20 °C and 85% RH has a dew point of {Tpaint:.1f} °C. A steel surface at 18 °C is only {18-Tpaint:.1f} °C above it, below the 3 °C margin most coating specifications need, so the work waits until the steel warms up or the humidity falls.

**Compressed air dew point at atmosphere.** A refrigerated dryer delivering a pressure dew point of {pdp:g} °C at {P2:g} bar absolute holds water vapour at {ea_line:.4f} kPa. When that air expands to atmospheric pressure the vapour pressure falls in proportion to the total pressure, to {ea_line*P1/P2:.4f} kPa, which is an atmospheric dew point of about **{adp:.1f} °C**. Quoting {adp:.0f} °C as if it were the line dew point is a common way to oversell a dryer.

## How dew point is measured

A chilled mirror hygrometer cools a small polished mirror until dew forms and measures its temperature directly, which makes it the reference instrument for calibration labs. Most field transmitters are capacitive polymer RH sensors combined with a temperature sensor; the transmitter computes the dew point from the two with a Magnus type formula, just as this page does. For very dry compressed air and gases, aluminium oxide and silicon based sensors read trace moisture down to around −80 °C dew point, where RH sensors lose resolution. Handheld coating inspection gauges measure air temperature, RH and steel surface temperature together and show the spread.

## Common mistakes

- **Typing 60 as a fraction.** The calculator takes 60% in the percent field; in your own spreadsheet the Magnus formula needs 0.60, and ln(60) gives nonsense.
- **Thinking heating air removes moisture.** Air at 10 °C and 80% RH heated to 22 °C drops to {rh_w:.0f}% RH, but its dew point stays at {Td_w:.1f} °C because no water was taken out.
- **Mixing pressure dew point and atmospheric dew point.** Dryer data sheets and ISO 8573-1 classes refer to the pressure dew point at line pressure.
- **Measuring air temperature beside a warm wall or in sunlight.** The RH sensor and thermometer must see the same air; a 1 °C error in the air temperature moves the dew point almost as much.
- **Using the dew point below 0 °C as the frost point.** Over ice, frost forms at a slightly higher temperature than the dew point given here.
''',
     faq_add=[('Does the dew point change when air is heated or cooled?',
               f'Not while no water is added or removed. Heating air from 10 °C at 80% RH to 22 °C lowers the RH to about {rh_w:.0f}%, but the dew point stays at {Td_w:.1f} °C. It changes only when air is dried, humidified or condenses water.'),
              ('How do I convert a pressure dew point to an atmospheric dew point?',
               f'Find the vapour pressure at the pressure dew point, scale it by atmospheric pressure divided by line pressure (both absolute), then find the dew point of that vapour pressure. A {pdp:g} °C pressure dew point at {P2:g} bar absolute is about {adp:.0f} °C at atmosphere.')])

# ---------------------------------------------------------------- NPSH available
rho = 992.22
Hp = 101325 / (rho * G)
Hv = 7384 / (rho * G)
NPSHa0 = Hp - Hv - 3 - 1.2
assert abs(NPSHa0 - 5.45) < 0.01
# deaerator: saturated, flooded 6 m, losses 0.8 m, NPSHr 3.5 m
hz_d, hf_d, nr_d = 6.0, 0.8, 3.5
npsh_d = hz_d - hf_d
# field check with suction gauge: -35 kPa(g), gauge 0.5 m above centreline, 50 m3/h in 102.26 mm bore
Pg = -35.0
vel = 50 / 3600 / (math.pi * 0.10226 ** 2 / 4)
hvel = vel ** 2 / (2 * G)
npsh_f = (Pg * 1000 + 101325 - 7384) / (rho * G) + hvel + 0.5
# lower level 1 m further: default with hz = -4
npsh_low = NPSHa0 - 1
# flow increase 20%: friction 1.2 * 1.44
hf_hi = 1.2 * 1.2 ** 2
npsh_hi = Hp - Hv - 3 - hf_hi

edit('engineering/npsh-available', date=U, phrase='npsh available calculator',
     intro=("A centrifugal pump cavitates when the pressure at its impeller eye falls to the vapour pressure of the liquid, so the suction system must supply more head than the pump needs. "
            "This NPSH available calculator works out NPSHa and compares it with the pump's NPSHr.\n\n"
            f"Process and mechanical engineers use it when laying out tanks, sumps and suction pipes, and when a noisy pump points to the problems explained in [NPSH and cavitation]({IB}npsh-and-cavitation-explained/)."),
     body_add=f'''
## Second example: boiler feed pump under a deaerator

A deaerator holds water at its boiling point, so the surface pressure equals the vapour pressure and the first two terms cancel. With the water level {hz_d:g} m above the pump centreline and {hf_d:g} m of suction loss, NPSHa = {hz_d:g} − {hf_d:g} = **{npsh_d:.1f} m**, whatever the deaerator pressure. Against an NPSHr of {nr_d:g} m the ratio is {npsh_d/nr_d:.2f}. This is why deaerators sit high on a structure: every metre of elevation is a metre of NPSH, and nothing else in the system adds any.

## How the default case reacts to changes

Starting from the default NPSHa of {NPSHa0:.2f} m:

- Sump level 1 m lower: NPSHa falls to {npsh_low:.2f} m and the ratio to {npsh_low/4:.2f}
- Flow 20% higher: friction rises roughly with the square of flow to {hf_hi:.2f} m, so NPSHa drops to {npsh_hi:.2f} m while NPSHr also rises on the pump curve
- Water at 60 °C instead of 40 °C: the vapour head grows from {Hv:.2f} m to about 2.07 m and almost all of the margin disappears

## Checking NPSHa on a running pump

Fit a calibrated compound gauge on the suction nozzle. Suppose it reads {Pg:g} kPa gauge, it sits 0.5 m above the centreline, and the pump moves 50 m³/h of 40 °C water through a 102.26 mm suction bore (velocity {vel:.2f} m/s, velocity head {hvel:.3f} m). Then NPSHa = ({Pg:g} + 101.325 − 7.384) kPa ÷ (ρg) + {hvel:.3f} + 0.5 = **{npsh_f:.2f} m**. A test like this catches blocked strainers and collapsed suction hoses that a desk calculation misses. Listen as well: cavitation sounds like gravel passing through the pump and often comes with a drop in discharge pressure.

## Common mistakes

- **Using gauge pressure for the surface.** An open tank has 101.325 kPa absolute at sea level, not zero; a closed vessel needs its gauge pressure plus atmospheric.
- **Taking vapour pressure at the normal temperature.** Use the highest temperature the liquid can reach, such as summer cooling water or a hot condensate return.
- **Forgetting the strainer.** A clean suction strainer may lose 0.2 m, a half blocked one several metres.
- **Comparing NPSHa with NPSH3 and calling it safe.** NPSHr is the point where head has already dropped 3%, so cavitation and erosion begin before it.
- **Checking only the duty point.** Run out on a parallel pump trip or an open bypass moves the pump to the right of its curve, where NPSHr climbs.
''',
     faq_add=[('Why is NPSHa from a deaerator independent of its pressure?',
               'The water is saturated, so the surface pressure equals the vapour pressure and the two pressure heads cancel. NPSHa is then just the static height of the water above the pump minus the suction losses.'),
              ('How do I check NPSHa on an installed pump?',
               f'Read a suction gauge at the pump inlet, convert gauge plus atmospheric minus vapour pressure into head, then add the velocity head and the gauge height above the centreline. The example on this page gives {npsh_f:.2f} m.')])

print('slice 3 done')

# ======================================================================= SECTION _expand_c4.py
"""Expand (2026-11-21), slice 4: pressure-vessel-thickness, air-receiver-size, air-changes-per-hour,
tank-drain-time, cone-bottom-tank-volume. Numbers computed here from each page's default inputs and
equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-21'
IB = 'https://www.instrumentationblog.in/'
G = 9.80665

# ---------------------------------------------------------------- Pressure vessel thickness
P, Di, S, E, CA, tn = 1.0, 1500.0, 138.0, 0.85, 3.0, 10.0
R = Di / 2 + CA
tc = P * R / (S * E - 0.6 * P)
treq = tc + CA
# joint efficiency table at the default vessel
e_rows = ''
for ee, nm in ((1.0, 'Full radiography or seamless'), (0.85, 'Spot radiography'), (0.7, 'No radiography')):
    t1 = P * R / (S * ee - 0.6 * P) + CA
    mw = S * ee * (tn - CA) / (R + 0.6 * (tn - CA))
    e_rows += f"| {ee:.2f} | {nm} | {t1:.2f} mm | {mw:.3f} MPa ({mw*10:.2f} bar g) |\n"
# static head at the bottom of a tall vertical vessel full of water
hw = 10.0
Ps = 1000 * G * hw / 1e6
P2 = P + Ps
tc2 = P2 * R / (S * E - 0.6 * P2)
treq2 = tc2 + CA
# remaining life from thickness survey
t_meas, yrs = 9.2, 8
rate = (tn - t_meas) / yrs
life = (t_meas - tc) / rate
assert abs(rate - 0.1) < 1e-9

edit('engineering/pressure-vessel-thickness', date=U, phrase='pressure vessel thickness calculator',
     intro=("Internal pressure loads a cylindrical shell with a hoop stress twice the longitudinal stress, so the circumferential formula nearly always sets the wall thickness. "
            "This pressure vessel thickness calculator applies the ASME VIII Division 1 formulas for the shell and for hemispherical, ellipsoidal and torispherical heads.\n\n"
            "Mechanical engineers use it for early sizing and plate ordering, and inspection engineers use it to check the minimum required thickness and MAWP of a vessel in service."),
     body_add=f'''
## Effect of weld joint efficiency

The joint efficiency comes from the extent of radiography on the welds. For the default vessel (1,500 mm, 1 MPa, S = 138 MPa, 3 mm corrosion allowance, 10 mm plate):

| E | Inspection of the long seam | Minimum shell thickness | MAWP of 10 mm plate |
|---|---|---|---|
{e_rows}
Full radiography costs more in the shop but saves plate on every course of a large vessel, and it also raises the MAWP of a given plate by about 18% compared with spot radiography.

## Static head in a tall vessel

The design pressure at any course is the pressure at the top plus the liquid head above that course. A vertical vessel with the same 1 MPa at the top and {hw:g} m of water above the bottom course sees an extra 1000 × 9.80665 × {hw:g} = **{Ps:.4f} MPa** there, so the bottom shell course needs:

- P = 1 + {Ps:.4f} = **{P2:.4f} MPa**
- t = {P2:.4f} × {R:g} ÷ (138 × 0.85 − 0.6 × {P2:.4f}) = **{tc2:.2f} mm**, plus 3 mm = **{treq2:.2f} mm**

That is above the 10 mm plate that suits the top of the vessel, which is why tall columns and storage vessels often step up in thickness towards the bottom.

## Thickness checks in service

Inspectors measure the wall with an ultrasonic thickness gauge on a grid of fixed points, then compare each reading with the minimum required thickness without corrosion allowance, here **{tc:.2f} mm**. Suppose the 10 mm shell reads **{t_meas:g} mm** after {yrs} years. The corrosion rate is (10 − {t_meas:g}) ÷ {yrs} = **{rate:.2f} mm per year**, and the remaining life is ({t_meas:g} − {tc:.2f}) ÷ {rate:.2f} = **{life:.1f} years**. Inspection intervals are usually set at half the remaining life or less, and local pitting is assessed separately from general wall loss.

## Common mistakes

- **Using the new radius.** The formulas use the corroded inside radius, D/2 + CA, so the result stays valid at the end of the corrosion life.
- **Taking E from the wrong seam.** Hoop stress acts across the longitudinal seams, so the hoop formula uses the joint efficiency of the long seam; the circumferential seams govern only the longitudinal stress formula.
- **Leaving out static head.** On tall liquid filled vessels the bottom course can need noticeably more thickness than the top, as shown above.
- **Reading the allowable stress at room temperature.** S falls as the design metal temperature rises, so take it from Section II Part D at the design temperature, not the ambient value.
- **Rounding the plate down.** Always pick the next standard plate at or above the required thickness, after allowing for mill under-tolerance and forming thinning on heads.
''',
     faq_add=[('How do I estimate the remaining life of a corroded vessel shell?',
               f'Divide the measured wall loss by the years in service to get the corrosion rate, then divide the margin above the required thickness by that rate. A 10 mm shell reading {t_meas:g} mm after {yrs} years with a required {tc:.2f} mm has about {life:.0f} years left.'),
              ('Should liquid static head be added to the design pressure?',
               f'Yes, at each course you check. {hw:g} m of water adds about {Ps:.3f} MPa, so the bottom course of a tall vessel needs more thickness than the top course at the same top pressure.')])

# ---------------------------------------------------------------- Air receiver size
Qc, Qd, t, Pa, P1, P2b, f = 0.1, 0.15, 120.0, 101325.0, 7.5e5, 6e5, 60.0
dP = P1 - P2b
Vs = t * max(Qd - Qc, 0) * Pa / dP
Vc = 0.25 * Qc * Pa / ((f / 3600) * dP)
V = max(Vs, Vc)
# altitude 1,500 m
Pa_alt = 101325 * (1 - 2.25577e-5 * 1500) ** 5.25588
Vs_alt = t * (Qd - Qc) * Pa_alt / dP
# drawdown test on a 5 m3 receiver
Vr, d1, d2, tdd = 5.0, 7.5, 6.5, 90.0
fad = Vr * (d1 - d2) * 1e5 / Pa
Qdd = fad / tdd
# wider band
Vs_band = t * (Qd - Qc) * Pa / 2.0e5
edit('engineering/air-receiver-size', date=U, phrase='air receiver size calculator',
     intro=("A compressed air receiver stores air between the compressor's unload and load pressures, covering short demand peaks and keeping the compressor from cycling too often. "
            "This air receiver size calculator gives the volume needed for a demand event and for load/unload cycling, then recommends the larger.\n\n"
            "Plant and utility engineers use it when adding a compressor or a large intermittent user, and maintenance teams use it to check whether an existing tank is too small."),
     body_add=f'''
## Measuring real demand with a drawdown test

The receiver itself can be used as a flow meter. Stop the compressor (or isolate it) with the plant running and time how long the pressure takes to fall. For a {Vr:g} m³ receiver falling from {d1:g} to {d2:g} bar g in {tdd:g} s:

- Free air drawn from storage = {Vr:g} × ({d1:g} − {d2:g}) × 100 ÷ 101.325 = **{fad:.3f} m³**
- Average demand = {fad:.3f} ÷ {tdd:g} = **{Qdd*1000:.1f} L/s**

Repeat the test with production stopped and the result is the leakage rate of the system. Include the volume of the main headers in V if they are large, or the demand is overstated.

## Altitude and pressure band

Free air delivery is referred to the intake pressure, so the same flows need less stored volume at altitude. At 1,500 m the standard atmosphere is about **{Pa_alt/1000:.1f} kPa**, and the demand event in the worked example needs {Vs_alt:.3f} m³ instead of {Vs:.3f} m³. Widening the usable band from 1.5 to 2 bar cuts the event volume to {Vs_band:.3f} m³, but every extra bar of compressor discharge pressure adds energy cost, so a wider band is only worth it when the users can genuinely tolerate the lower pressure.

## Common mistakes

- **Entering compressed flow instead of free air.** The formulas use flows at intake conditions (FAD, Nm³ or scfm); a flow at 7 bar is about eight times smaller and gives an undersized tank.
- **Setting P2 to the tool pressure.** Dryers, filters and pipework take 0.5 to 1 bar between the receiver and the users, so P2 is the receiver pressure needed to keep the farthest tool supplied, not the tool's own rating.
- **Using gauge pressure for P_atm.** Atmospheric pressure converts free air into stored volume and must be absolute; only P1 and P2 may both be gauge.
- **Sizing only for cycling.** A large intermittent user such as a blast pot or a baghouse pulse system usually needs its own receiver close to it, because the main receiver cannot refill through a long, small header fast enough.
- **Ignoring the drain.** Condensate collecting in the bottom reduces the working volume and corrodes the shell; a blocked automatic drain slowly turns a correctly sized receiver into a small one.
''',
     faq_add=[('How can I measure my actual compressed air demand with the receiver?',
               f'Isolate the compressor and time the pressure drop. Free air used = V × ΔP ÷ P_atm, so a {Vr:g} m³ receiver falling {d1-d2:g} bar in {tdd:g} s supplies about {Qdd*1000:.0f} L/s. With production stopped the same test gives the leakage rate.'),
              ('Does altitude change the receiver size?',
               f'Yes, slightly. Lower atmospheric pressure means each litre of free air takes less space when compressed. At 1,500 m (about {Pa_alt/1000:.1f} kPa) the example demand event needs {Vs_alt:.2f} m³ instead of {Vs:.2f} m³.')])

# ---------------------------------------------------------------- Air changes per hour
L, W, H, Q = 5.0, 4.0, 2.7, 300.0
Vroom = L * W * H
ach = Q / Vroom
# tracer gas decay
c0, c1, cout, tmin = 1800.0, 900.0, 420.0, 20.0
ach_tr = math.log((c0 - cout) / (c1 - cout)) / (tmin / 60)
# grille anemometer reading
vg, ag, free = 2.1, 0.3 * 0.3, 0.8
Qg = vg * ag * free * 3600
ach_g = Qg / Vroom
# suspended ceiling: true height 3.3 m vs 2.7 m when plenum is open return
V33 = L * W * 3.3
ach33 = Q / V33
edit('engineering/air-changes-per-hour', date=U, phrase='air changes per hour calculator',
     intro=("Air changes per hour (ACH) is how many times the air in a room is replaced each hour by ventilation or air cleaning. "
            "This air changes per hour calculator gives the ACH from room size and airflow, the airflow for a target ACH, and the time to clear 99% of an airborne contaminant.\n\n"
            "HVAC designers, facility managers and safety officers use it to check offices, labs, workshops and clean rooms, and to confirm a fan or [HVAC system](https://www.instrumentationblog.in/what-is-an-hvac-system/) meets the required rate."),
     body_add=f'''
## Measuring the air change rate of a real room

Design airflow and installed airflow are rarely the same, so ACH is checked on site in one of two ways.

**At the grilles.** A flow hood (balometer) placed over each diffuser reads the airflow directly. Without one, a vane anemometer swept across the grille face gives an average velocity, which is multiplied by the free area. A 300 × 300 mm grille with about {free*100:.0f}% free area and an average face velocity of {vg:g} m/s passes {vg:g} × {ag:.2f} × {free:g} × 3600 = **{Qg:.0f} m³/h**, which alone gives the 54 m³ office **{ach_g:.1f} ACH**.

**By tracer gas decay.** Raise the CO₂ level (people or a small cylinder), stop the source and log the concentration. With outdoor air at {cout:.0f} ppm and the room falling from {c0:,.0f} to {c1:,.0f} ppm in {tmin:g} minutes, ACH = ln[({c0:,.0f} − {cout:.0f}) ÷ ({c1:,.0f} − {cout:.0f})] ÷ ({tmin:g} ÷ 60) = **{ach_tr:.2f}**. This measures outdoor air exchange only, including infiltration, and it ignores recirculated air entirely, which is exactly what matters for diluting CO₂ and odours.

## Common mistakes

- **Using floor area instead of volume.** ACH depends on the volume, so a hall with a 6 m ceiling needs more than twice the airflow of an office with the same floor area.
- **Adding supply and exhaust together.** In a balanced room the same air enters and leaves; count one of them, normally the larger.
- **Taking the fan catalogue figure.** A fan rated at free air delivers less once it works against ducts, filters and grilles; measure the installed flow or read it from the fan curve at the system pressure.
- **Ignoring an open ceiling plenum.** If the void above a suspended ceiling is part of the return path, the mixed volume grows. Treating the same office as 3.3 m high gives {V33:.0f} m³ and only **{ach33:.2f} ACH** from 300 m³/h.
- **Counting unfiltered recirculation as clean air.** A fan coil that just stirs room air adds no contaminant removal; only outdoor air or air through an effective filter (or a purifier's CADR) counts.
''',
     faq_add=[('How can I measure the air change rate in an existing room?',
               f'Use a flow hood on each supply grille and divide the total by the room volume, or run a CO₂ decay test. A fall from {c0:,.0f} to {c1:,.0f} ppm in {tmin:g} minutes with {cout:.0f} ppm outdoors means about {ach_tr:.1f} outdoor air changes per hour.'),
              ('Should I count both the supply and the exhaust airflow?',
               'No. In a balanced room the air that is supplied is the air that leaves, so use one of them. If they differ, use the larger flow for the air change rate and expect the room to be slightly pressurised or depressurised.')])

# ---------------------------------------------------------------- Tank drain time
D, d, Cd, h1, h2 = 2.0, 0.05, 0.61, 3.0, 0.2
A = math.pi * D ** 2 / 4
a = math.pi * d ** 2 / 4


def tdrain(D, d, Cd, h1, h2):
    return (math.pi * D ** 2 / 4) / (Cd * math.pi * d ** 2 / 4) * math.sqrt(2 / G) * (math.sqrt(h1) - math.sqrt(h2))


t0 = tdrain(D, d, Cd, h1, h2)
# measured 30 minutes instead
tm = 30 * 60
Cd_m = Cd * t0 / tm
# outlet for 15 min target
d15 = d * math.sqrt(t0 / (15 * 60))
# naive linear estimate using the starting flow
Q1 = Cd * a * math.sqrt(2 * G * h1)
Vd = A * (h1 - h2)
t_lin = Vd / Q1
# nozzle Cd 0.82
t_noz = tdrain(D, d, 0.82, h1, h2)
c_rows = ''
for cc, nm in ((0.5, 'Re-entrant tube'), (0.61, 'Sharp-edged hole'), (0.82, 'Short nozzle'), (0.97, 'Bell-mouth')):
    c_rows += f"| {nm} | {cc:.2f} | {tdrain(D, d, cc, h1, h2)/60:.1f} min | {tdrain(D, d, cc, h1, 0)/60:.1f} min |\n"
edit('engineering/tank-drain-time', date=U, phrase='tank drain time calculator',
     intro=("A tank emptying through a bottom outlet slows down as it drains, because the outflow velocity follows the square root of the liquid head. "
            "This tank drain time calculator applies Torricelli's law to give the time between two levels, the start and end outflow, and the time to refill at a set flow.\n\n"
            "Process and maintenance engineers use it to plan tank cleaning and batch transfers, and to choose an outlet size that empties a vessel within the time available."),
     body_add=f'''
## Outlet type and drain time

The discharge coefficient changes the time in direct proportion. For the default 2 m tank and 50 mm outlet:

| Outlet | C<sub>d</sub> | 3 m to 0.2 m | 3 m to empty |
|---|---|---|---|
{c_rows}
Swapping a sharp-edged hole for a short nozzle of the same bore cuts the drain time from {t0/60:.1f} to {t_noz/60:.1f} minutes without any change to the tank.

## Sizing an outlet for a target time

Drain time is inversely proportional to the outlet area, so the bore scales with the square root of the time ratio. To bring the default tank from 3 m to 0.2 m in 15 minutes instead of {t0/60:.2f}, the outlet must be 50 × √({t0/60:.2f} ÷ 15) = **{d15*1000:.1f} mm**, so a standard DN65 nozzle does the job.

## Checking the outlet on site

Timing a real drain is a quick check of the outlet. If the default tank takes 30 minutes instead of the calculated {t0/60:.2f}, the effective coefficient is 0.61 × {t0/60:.2f} ÷ 30 = **{Cd_m:.3f}**. A value well below the table suggests a partly closed valve, a strainer, debris in the nozzle or a drain line long enough for friction to control the flow. Level can be read from a sight glass, a dip tape or the level transmitter trend, using two readings well apart so the timing error stays small.

## Common mistakes

- **Assuming the flow stays at its starting value.** Dividing the volume by the initial outflow gives {Vd:.2f} m³ ÷ {Q1*3600:.2f} m³/h × 60 = {Vd/(Q1*3600)*60:.1f} min, far short of the real {t0/60:.1f} min.
- **Measuring levels from the tank floor.** The head is measured from the outlet centre; for a side nozzle 300 mm above the floor, the liquid below the nozzle never drains and the levels entered must be reduced by 0.3 m.
- **Using C<sub>d</sub> 0.61 for a drain line.** Once the liquid passes through a pipe, valve and bends, friction controls the flow and the effective coefficient may be 0.2 to 0.4.
- **Applying water figures to viscous liquids.** Oils, syrups and slurries have lower coefficients, especially at low head near the end of draining.
- **Leaving an inflow running.** Any feed still entering the tank extends the drain time, and if it exceeds the outflow at the final head, the level never reaches it.
''',
     faq_add=[('Can I use this for viscous liquids like oil or syrup?',
               'Only as a first estimate. Viscous liquids discharge with a lower coefficient, and it drops further as the head falls, so the real time is longer. Time a test drain and back-calculate the coefficient for the liquid you handle.'),
              ('How can I check the discharge coefficient of my tank outlet?',
               f'Time the level fall between two marks and scale the coefficient by calculated time over measured time. If the default tank takes 30 minutes instead of {t0/60:.1f}, the effective coefficient is about {Cd_m:.2f}.')])

# ---------------------------------------------------------------- Cone bottom tank
D, H, hc, d, h = 2.0, 3.0, 1.0, 0.1, 2.5


def vol(h, D=D, H=H, hc=hc, d=d):
    hh = min(h, hc)
    Ds = d + (D - d) * hh / hc
    return math.pi * hh / 12 * (d ** 2 + d * Ds + Ds ** 2) + math.pi * D ** 2 / 4 * min(max(h - hc, 0), H)


Vcone = math.pi * hc / 12 * (d ** 2 + d * D + D ** 2)
Vt = Vcone + math.pi * D ** 2 / 4 * H
Vpt = math.pi * hc / 12 * (D ** 2)
# transmitter tapping 0.15 m above outlet, reading 1.2 m
tap, rd = 0.15, 1.2
hl = tap + rd
Vtx = vol(hl)
Vwrong = vol(rd)
sg = 1.1
Vtx, Vwrong = Vtx * 1000, Vwrong * 1000
Vcone, Vt, Vpt = Vcone * 1000, Vt * 1000, Vpt * 1000
mass = Vtx / 1000 * sg * 1000
# slant height mistake
slant = math.hypot((D - d) / 2, hc)
Vslant = math.pi * slant / 12 * (d ** 2 + d * D + D ** 2) * 1000
edit('engineering/cone-bottom-tank-volume', date=U, phrase='cone bottom tank volume calculator',
     intro=("Many process tanks, silos and hoppers have a conical bottom so they drain fully, which makes level and volume non-linear near the outlet. "
            "This cone bottom tank volume calculator gives the liquid volume for any level from the outlet, plus total capacity, percent full, cone volume and cone angle.\n\n"
            "Instrument and process engineers use it to build strapping tables for [automatic tank gauging](https://www.instrumentationblog.in/automatic-tank-gauging-explained/) or a level transmitter, and operators use it to check stock and batch quantities."),
     body_add=f'''
## From a transmitter reading to volume and mass

A level transmitter rarely sits at the outlet. On the default tank, a [DP transmitter used for level measurement](https://www.instrumentationblog.in/dp-transmitter-level-measurement/) has its lower tapping {tap*1000:.0f} mm above the outlet and reads {rd:g} m:

- Level from the outlet = {tap:g} + {rd:g} = **{hl:.2f} m**, above the 1 m cone
- Volume = {Vcone:,.1f} + π × 2² × ({hl:.2f} − 1) ÷ 4 × 1000 = **{Vtx:,.1f} L**
- For a liquid with relative density {sg:g}, the stock is **{mass:,.0f} kg**

Entering the raw {rd:g} m reading would give only {Vwrong:,.1f} L, an error of {Vtx - Vwrong:,.0f} L that comes from the offset in the cone alone. On a DP transmitter the reading also depends on the density set in the transmitter, so a change of product needs a new range as well as a new table.

## Checking the table by water strapping

For custody or batching duties the calculated table is confirmed by filling the empty tank with water through a calibrated flow meter in steps, recording the level at each step. The calculated and measured figures usually differ in the cone, where dished welds, a sloping outlet nozzle or an internal agitator foot take up volume. The measured table then replaces the calculated one in the gauging system.

## Common mistakes

- **Using the slant height of the cone.** The formula needs the vertical height. Entering the {slant:.3f} m slant length of the default cone would give a cone volume of {Vslant:,.0f} L instead of {Vcone:,.0f} L.
- **Ignoring the outlet diameter.** Treating the 100 mm outlet as a point with the same 1 m cone height gives {Vpt:,.0f} L in the cone, {Vcone - Vpt:,.0f} L too little.
- **Using the outside diameter.** Drawings often give the shell OD; subtract twice the wall thickness, since 6 mm of wall on a 2 m tank changes the volume by about 1.2%.
- **Reading percent level as percent volume.** At 0.5 m the tank is 12.5% of its height but holds only 1.5% of its capacity.
- **Forgetting the transmitter offset.** Add the height of the lower tapping or sensor above the outlet before entering the level, as in the example above.
''',
     faq_add=[('How do I convert the tank volume to mass?',
               f'Multiply the volume by the liquid density. {Vtx:,.0f} L of a liquid with relative density {sg:g} is about {mass:,.0f} kg. Use the density at the actual temperature, since many liquids change by 0.1% or more per 10 °C.'),
              ('Should I use the slant height or the vertical height of the cone?',
               f'The vertical height, measured from the outlet to the joint with the straight side. The slant length is always longer; on the default tank it is {slant:.3f} m against 1 m and would overstate the cone volume.')])

print('slice 4 done', inplace.DONE)

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-21), slice 5: chain-length, cooling-tower, hydrostatic-test-pressure, tank-heater-sizing, compressed-air-leak.
Each page already has a worked example on its defaults; this slice adds a second scenario, field practice, common mistakes and new FAQs.
Every number is computed here from the page's own equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-21'
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Chain length
def chain(p, N1, N2, C, n1):
    Lp = 2 * C / p + (N1 + N2) / 2 + ((N2 - N1) / (2 * math.pi)) ** 2 * p / C
    Lr = 2 * math.ceil(Lp / 2)
    k = Lr - (N1 + N2) / 2
    Ca = p / 4 * (k + math.sqrt(k ** 2 - 8 * ((N2 - N1) / (2 * math.pi)) ** 2))
    v = N1 * p / 1000 * n1 / 60
    return Lp, Lr, Lr * p, Ca, n1 * N1 / N2, v


# defaults (checked against the page's own example)
d0 = chain(12.7, 17, 34, 500, 500)
assert d0[1] == 106 and abs(d0[3] - 510.0) < 0.1
# second scenario: ANSI 50 reduction drive from a 960 rpm motor, 19 T to 57 T at 640 mm
p2, a1, a2, C2, r2 = 15.875, 19, 57, 640.0, 960.0
Lp2, Lr2, Lm2, Ca2, n22, v2 = chain(p2, a1, a2, C2, r2)
take2 = Ca2 - C2
Dp_a = p2 / math.sin(math.pi / a1)
Dp_b = p2 / math.sin(math.pi / a2)
# wrap angle on the small sprocket for the rounded chain
wrap2 = 180 - 2 * math.degrees(math.asin((Dp_b - Dp_a) / (2 * Ca2)))
# elongation gauge lengths over 12 pitches of ANSI 40
L12 = 12 * 12.7
e_rows = ''
for pc in (0.0, 1.0, 1.5, 2.0, 3.0):
    e_rows += f"| {pc:.1f}% | {L12 * (1 + pc / 100):.1f} mm | {L12 * (1 + pc / 100) / 25.4:.3f} in |\n"
# a 106-link chain stretched 1.5 % grows by
grow = d0[2] * 0.015

edit('engineering/chain-length', date=U, phrase='chain length calculator',
     intro=("A roller chain drive is set by three things: the chain pitch, the tooth count of each sprocket and the distance between the shaft centres. "
            "This chain length calculator gives the length in pitches, rounds it up to an even number of links and finds the exact centre distance that chain needs.\n\n"
            "Maintenance fitters use it to order replacement chain and set the motor base, and machine designers use it to check speed ratio, chain speed and sprocket diameters."),
     body_add=f'''
## Second example: a reduction drive from a motor

An ANSI 50 chain ({p2} mm pitch) takes a {r2:.0f} rpm motor down through a {a1}-tooth sprocket to a {a2}-tooth sprocket, with the shafts planned at {C2:.0f} mm:

- Exact length = 2 × {C2:.0f} ÷ {p2} + ({a1} + {a2}) ÷ 2 + [({a2} − {a1}) ÷ 2π]² × {p2} ÷ {C2:.0f} = **{Lp2:.2f} pitches**
- Order **{Lr2} links**, a chain **{c(Lm2, 1)} mm** long
- The shafts must then sit at **{Ca2:.1f} mm**, {take2:.1f} mm further apart than planned, so the motor base needs at least that much slot travel
- Ratio 3:1, driven speed **{n22:.0f} rpm**, chain speed **{v2:.2f} m/s**
- Pitch diameters {Dp_a:.1f} mm and {Dp_b:.1f} mm, giving about **{wrap2:.0f}°** of wrap on the small sprocket, comfortably above the 120° minimum

At {v2:.1f} m/s an ANSI 50 chain is past the range where hand oiling is enough; most makers ask for drip or oil bath lubrication at this speed.

## Measuring chain wear in the field

Chain stretch comes from wear of the pins and bushes, not from the plates stretching. Lay the chain flat under light tension and measure across 12 pitches from the centre of one pin to the centre of the pin 12 pitches away. For ANSI 40 the new length is {L12:.1f} mm:

| Elongation | Length over 12 pitches | In inches |
|---|---|---|
{e_rows}
Replace the chain at about 1.5% on drives with large sprockets or timing duty and at 3% on slow, general drives. The {d0[1]}-link chain in the default example grows by about {grow:.0f} mm at 1.5% wear, which is most of the adjustment a normal tensioner offers. Replace worn sprockets with the chain, because hooked teeth wear a new chain out quickly.

## Common mistakes

- **Rounding the link count down.** A chain shorter than the calculated length cannot be fitted at the planned centres; always round up to the next even number and move the shaft.
- **Counting rollers instead of pitches.** A 106-link chain has 106 pitches including the connecting link; counting rollers on an open length is easy to get wrong by one.
- **Measuring a slack chain for wear.** Without tension the joints sit at random in their clearances and the reading means little.
- **Mixing ANSI and ISO chain.** ANSI 40 and ISO 08B are both 12.7 mm pitch, but the roller diameter and inner width differ, so they do not run well on each other's sprockets.
- **Ignoring tooth counts below 17 at speed.** A 12-tooth sprocket at high speed gives noticeable chordal speed variation, vibration and short chain life.
''',
     faq_add=[('How do I measure a roller chain for wear?',
               f'Measure across 12 pitches under light tension, pin centre to pin centre. New ANSI 40 measures {L12:.1f} mm; replace it at about {L12 * 1.015:.1f} mm (1.5%) for precise drives or {L12 * 1.03:.1f} mm (3%) for slow, general drives.'),
              ('How far must I move the motor after fitting a new chain?',
               f'Set the shafts to the exact centre distance for the rounded link count. In the ANSI 50 example the planned {C2:.0f} mm becomes {Ca2:.1f} mm for {Lr2} links, a {take2:.1f} mm move.')])

# ---------------------------------------------------------------- Cooling tower
def tower(Th, Tc, Twb, Q, coc, dr):
    R = Th - Tc
    A = Tc - Twb
    eff = R / (R + A)
    H = 1000 * 4186 * Q / 3600 * R / 1000  # kW with Q in m3/h
    E = 0.00153 * Q * R
    Dr = dr / 100 * Q
    B = E / (coc - 1) - Dr
    return R, A, eff, H, E, Dr, B, E + B + Dr


t0 = tower(37, 32, 28, 500, 4, 0.02)
assert abs(t0[7] - 5.10) < 0.001
# conductivity based cycles
ec_m, ec_b = 250.0, 1200.0
coc_m = ec_b / ec_m
tm = tower(37, 32, 28, 500, coc_m, 0.02)
t6 = tower(37, 32, 28, 500, 6, 0.02)
save_day = (t0[7] - t6[7]) * 24
# hot humid day: wet bulb 30 C, the tower keeps a 4 K approach only if it has margin
th = tower(39, 34, 30, 500, 4, 0.02)
# kW per m3/h and TR
kW_TR = 3.51685

edit('engineering/cooling-tower', date=U, phrase='cooling tower calculator',
     intro=("A cooling tower removes heat from condenser or process water by evaporating a small part of it into a moving air stream. "
            "This cooling tower calculator finds the range, approach and effectiveness, the heat rejected, and the evaporation, drift, blowdown and makeup flows.\n\n"
            "Utility engineers and HVAC operators use it to check tower performance against design, plan makeup water supply and set the blowdown that keeps dissolved solids under control."),
     body_add=f'''
## Finding the cycles from conductivity readings

Cycles of concentration are rarely known directly; they are read from conductivity. If the makeup water measures **{ec_m:.0f} µS/cm** and the basin **{ec_b:.0f} µS/cm**, the tower runs at {ec_b:.0f} ÷ {ec_m:.0f} = **{coc_m:.1f} cycles**. Entered with the other default values, that gives:

- Blowdown = {tm[4]:.3f} ÷ ({coc_m:.1f} − 1) − {tm[5]:.2f} = **{tm[6]:.3f} m³/h**
- Makeup = **{tm[7]:.3f} m³/h**, against {t0[7]:.2f} m³/h at 4 cycles

Pushing on to 6 cycles cuts the makeup to {t6[7]:.2f} m³/h, a saving of about **{save_day:.0f} m³ a day**. Whether that is safe depends on the makeup water's hardness, alkalinity and silica, which set the scaling limit for the treatment programme.

## Checking a tower against its design

A tower test needs four readings taken together at steady load: hot water temperature at the inlet header, cold water temperature at the basin outlet, wet bulb temperature at the air inlet (an aspirated psychrometer, not a dry bulb sensor) and circulating flow. Flow is often checked with a clamp-on meter on the riser; see [how an ultrasonic flow meter works]({IB}how-ultrasonic-flow-meter-works/) for its limits on lined or corroded pipe.

On a humid day with a 30 °C wet bulb, a tower holding the same {th[1]:.0f} K approach delivers {30 + th[1]:.0f} °C water, and with a {th[0]:.0f} to 34 °C duty it still rejects {th[3]:,.0f} kW. The chiller now sees condenser water 2 K warmer, which typically costs it a few percent more compressor power per kelvin. A tower that drifts from a 4 K to a 6 K approach at the same wet bulb and load needs its fill, nozzles and fan checked.

## Common mistakes

- **Using the dry bulb temperature.** Evaporative cooling is limited by the wet bulb; using the dry bulb makes the approach look far better than it is.
- **Reading cold water temperature in the basin surface.** Measure in the outlet pipe or at the pump suction, where the water is mixed.
- **Treating effectiveness as the main performance figure.** Effectiveness changes with range; the approach at a known wet bulb, load and flow is what tower suppliers guarantee.
- **Counting drift as blowdown.** Drift does remove dissolved solids, but modern eliminators keep it so small that it cannot replace controlled blowdown.
- **Setting blowdown by a fixed timer.** Load and weather change the evaporation through the day; conductivity controlled blowdown holds the cycles steady.
''',
     faq_add=[('How do I find cycles of concentration from conductivity?',
               f'Divide the basin water conductivity by the makeup water conductivity. {ec_b:.0f} µS/cm in the basin with {ec_m:.0f} µS/cm makeup is {coc_m:.1f} cycles. Chloride or silica ratios give the same figure and are not upset by acid dosing.'),
              ('What happens to the cold water temperature on a more humid day?',
               'It rises with the wet bulb. A tower that holds a 4 K approach gives 32 °C water at a 28 °C wet bulb but about 34 °C at a 30 °C wet bulb, for the same load and flow.')])

# ---------------------------------------------------------------- Hydrostatic test pressure
g0 = 9.80665


def hydro(P, k, St, Sd, h, rho):
    r = St / Sd
    Pt = k * P * r
    Pb = Pt + rho * g0 * h / 1e5
    return r, Pt, Pb, 1.5 * Pt, 2 * Pt, 4 * Pt


h0 = hydro(10, 1.3, 138, 125, 6, 1000)
assert abs(h0[1] - 14.352) < 0.001
# B31.3 piping loop: 20 bar g design, S at design temperature 118 MPa, ambient 138 MPa, low point 15 m below the gauge
hp = hydro(20, 1.5, 138, 118, 15, 1000)
# pneumatic test of the same vessel
hn = hydro(10, 1.1, 138, 125, 6, 0)
# stored energy comparison, 2 m3 volume at 14.35 bar g: gas (isentropic expansion) vs water (compressibility)
Vv = 2.0
Pa = 1.01325e5
Pabs = h0[1] * 1e5 + Pa
gam = 1.4
E_gas = Pabs * Vv / (gam - 1) * (1 - (Pa / Pabs) ** ((gam - 1) / gam))
K_w = 2.2e9
E_wat = (h0[1] * 1e5) ** 2 * Vv / (2 * K_w)
# inspection pressure after the 1.3x hold
Pinsp = h0[1] / 1.3

edit('engineering/hydrostatic-test-pressure', date=U, phrase='hydrostatic test pressure calculator',
     intro=("A hydrostatic test proves a new pressure vessel or pipe system by filling it with water and holding it above design pressure, as described in [hydrostatic testing in the oil and gas industry](https://www.instrumentationblog.in/hydrostatic-testing-in-oil-gas-industry/). "
            "This hydrostatic test pressure calculator applies the ASME VIII and B31.3 factors with the stress ratio.\n\n"
            "QA engineers and test supervisors use it to write test packs, add the head at the low point and pick a gauge range."),
     body_add=f'''
## Second example: a B31.3 piping test with a tall riser

A process line designed for 20 bar g has an allowable stress of 118 MPa at design temperature and 138 MPa at the ambient test temperature. The test gauge is at grade and the lowest point is a drain 15 m below it on a pipe rack riser:

- Stress ratio = 138 ÷ 118 = **{hp[0]:.4f}**
- Test pressure = 1.5 × 20 × {hp[0]:.4f} = **{hp[1]:.2f} bar g** at the gauge
- At the low point: {hp[1]:.2f} + 1000 × 9.807 × 15 ÷ 10⁵ = **{hp[2]:.2f} bar g**
- Gauge range between {hp[3]:.1f} and {hp[5]:.1f} bar, preferably about {hp[4]:.1f} bar, so a 0 to 60 bar gauge suits

The {hp[2] - hp[1]:.2f} bar of head at the drain is added to the pressure the low point sees. Check that the flanges and valves down there are rated for {hp[2]:.1f} bar g, and that the hoop stress there stays below yield, as B31.3 requires.

## Why a pneumatic test needs extra care

A pneumatic test of the default vessel needs only {hn[1]:.2f} bar g, but compressed air stores far more energy than water. For a 2 m³ vessel at the hydrotest pressure of {h0[1]:.2f} bar g, the water stores about **{E_wat / 1000:.1f} kJ** (from its compressibility), while air at the same pressure would release about **{E_gas / 1e6:.1f} MJ** if the vessel failed, over {E_gas / E_wat:,.0f} times as much. That is why pneumatic tests use a lower factor, staged pressurisation, a hold at half the test pressure and an exclusion zone.

## How the test is run

Fill from the low point while venting at every high point until water runs clear of air. Raise the pressure slowly with a test pump, with a calibrated gauge or recorder at the top and a second gauge on the pump. Hold the full test pressure for the specified time, then on an ASME VIII-1 vessel lower it to at least {Pinsp:.2f} bar g (test pressure ÷ 1.3) for the close visual inspection of every weld and joint. Keep watch on the water temperature: in a rigid, completely full system, warming by the sun can raise the pressure by several bar for each degree.

## Common mistakes

- **Setting the test pressure at the low point gauge.** ASME VIII-1 defines the test pressure at the top; a gauge at the bottom reads high by the water head.
- **Leaving out the stress ratio.** For hot services S<sub>T</sub> ÷ S is above 1, and a test at plain 1.3 or 1.5 times design pressure is too low.
- **Testing against closed valves or relief valves.** Valve seats and relief valves are not test boundaries; use blinds and remove or isolate the relief devices.
- **Choosing a gauge far over range.** A 0 to 100 bar gauge on a 14 bar test reads in the bottom seventh of the scale, where small errors and pointer friction dominate.
- **Draining without venting.** Opening the drain with the high point vent shut can pull a vacuum and collapse thin tanks or large thin wall pipe.
''',
     faq_add=[('Why is a pneumatic test more dangerous than a hydrostatic test?',
               f'Gas stores energy as it compresses and releases it all if the vessel fails. A 2 m³ vessel at {h0[1]:.1f} bar g holds about {E_gas / 1e6:.1f} MJ as air but only about {E_wat / 1000:.0f} kJ as water.'),
              ('Why does the pressure rise during a hydrotest when nothing is added?',
               'Water expands as it warms, and a full, rigid system has no room for it. Sunshine on a pipeline or vessel can raise the gauge reading by several bar per degree, so monitor temperature and keep a bleed valve ready.')])

# ---------------------------------------------------------------- Tank heater sizing
def heater(V_L, rho, cp, T1, T2, th, Uw, A, Ta, eff, Vs, ph):
    m = V_L / 1000 * rho
    E = m * cp * (T2 - T1) / 3600  # kWh
    Ph = E / th
    Pl = Uw * A * ((T1 + T2) / 2 - Ta) / 1000
    Pr = (Ph + Pl) / eff
    Phold = Uw * A * (T2 - Ta) / 1000 / eff
    I = Pr * 1000 / (Vs * ph)
    return m, E, Ph, Pl, Pr, Phold, I


s3 = math.sqrt(3)
k0 = heater(2000, 1000, 4.186, 15, 60, 3, 0.8, 10, 15, 1.0, 415, s3)
assert abs(k0[4] - 35.06) < 0.01
# bare steel fuel oil day tank: 5,000 L, 870 kg/m3, 1.9 kJ/kgK, 20 to 70 C in 4 h, U = 8, 18 m2, ambient 20 C
ko = heater(5000, 870, 1.9, 20, 70, 4, 8.0, 18, 20, 1.0, 415, s3)
ko_ins = heater(5000, 870, 1.9, 20, 70, 4, 0.8, 18, 20, 1.0, 415, s3)
loss_share = ko[3] / ko[4] * 100
# voltage drop effect on a 36 kW, 415 V heater
P36_394 = 36 * (394 / 415) ** 2
# check measured current: a 36 kW 415 V heater should draw
I36 = 36000 / (s3 * 415)
# heat-up time with a 36 kW heater on the default tank
t36 = k0[1] / (36 - k0[3])

edit('engineering/tank-heater-sizing', date=U, phrase='tank heater sizing calculator',
     intro=("A heater for a process tank, hot water cylinder or oil tank has to supply the sensible heat of the liquid in the heat-up time and cover the heat lost through the walls. "
            "This tank heater sizing calculator gives the energy, heat-up power, heat loss, heater kW, holding power and supply current.\n\n"
            "Electrical and process engineers use it to choose immersion heater ratings and cable sizes, and plant teams use it to check why a tank takes too long to reach temperature."),
     body_add=f'''
## Second example: an uninsulated fuel oil day tank

A 5,000 L bare steel tank of light fuel oil (870 kg/m³, c<sub>p</sub> 1.9 kJ/kg·K, 18 m² of surface, U about 8 W/m²·K in still air) must go from 20 °C to 70 °C in 4 hours in a 20 °C room:

- Mass = {ko[0]:,.0f} kg; heat = {ko[0]:,.0f} × 1.9 × 50 ÷ 3,600 = **{ko[1]:.1f} kWh**
- Heat-up power = {ko[1]:.1f} ÷ 4 = **{ko[2]:.2f} kW**
- Average loss = 8 × 18 × (45 − 20) ÷ 1,000 = **{ko[3]:.2f} kW**
- Heater power = **{ko[4]:.2f} kW**, drawing **{ko[6]:.1f} A** at 415 V three-phase
- Holding at 70 °C needs **{ko[5]:.2f} kW**

Losses are {loss_share:.0f}% of the heater rating here. Insulating the tank to U = 0.8 cuts the holding power to {ko_ins[5]:.2f} kW, which matters more than the heater rating because the tank is held hot for most of the day.

## Checking a heater in service

Measure the phase currents with a clamp meter while the heater is on and compare them with the rating. A 36 kW heater at 415 V three-phase should draw about **{I36:.1f} A** per line; a much lower current on one phase points to a failed element. Low supply voltage has the same effect on all phases: at 394 V the same heater gives only {P36_394:.1f} kW. With a healthy 36 kW heater the default 2,000 L tank should reach 60 °C in about **{t36:.2f} hours**; log the temperature during heat-up and compare. A slower rise means scale on the elements, a lower supply voltage or losses larger than assumed, often from an open lid.

## Common mistakes

- **Sizing for the holding load only.** The holding power is small; the heat-up duty sets the heater rating.
- **Leaving out the steel of the tank.** A heavy steel tank or a tank full of parts also has to be heated; add its mass × 0.49 kJ/kg·K to the liquid energy.
- **Forgetting evaporation from an open surface.** A hot open tank can lose more heat from the surface than through the walls; a lid or floating balls cut it sharply.
- **Using single phase current formulas on a three-phase heater.** Divide by √3 × line voltage, not by the line voltage.
- **Choosing high watt density elements for oil.** Oil carries heat away slowly, so a water heater element can coke the oil and burn out.
''',
     faq_add=[('How much current should a three-phase immersion heater draw?',
               f'Line current is kW × 1,000 ÷ (√3 × line voltage). A 36 kW heater on 415 V draws about {I36:.1f} A per phase; a lower reading on one phase usually means a failed element.'),
              ('Does insulating the tank reduce the heater size?',
               f'Only a little for the heat-up duty, but a lot for the running cost. On a 5,000 L bare oil tank, insulation cuts the heater rating from {ko[4]:.1f} kW to {ko_ins[4]:.1f} kW and the holding power from {ko[5]:.2f} kW to {ko_ins[5]:.2f} kW.')])

# ---------------------------------------------------------------- Compressed air leak
def leak(d, p_bar, T, Cd, n, SP, H, price):
    Ah = math.pi / 4 * (d / 1000) ** 2
    m = Cd * Ah * (p_bar * 1e5 + 101325) * math.sqrt(1.4 / (287.05 * (T + 273.15))) * 0.578704
    Qf = m / 1.20412  # m3/s
    Pw = SP * Qf * 60  # kW
    E = Pw * n * H
    return m * 3600, Qf * 60000, Pw, E, E * price


l0 = leak(3, 7, 20, 0.65, 1, 6.5, 8000, 8)
assert abs(l0[1] - 433) < 1
# effect of dropping header pressure to 6 bar
l6 = leak(3, 6, 20, 0.65, 1, 6.5, 8000, 8)
cut = (1 - l6[1] / l0[1]) * 100
# plant survey: 25 leaks of about 1.5 mm and 5 of about 3 mm at 7 bar
ls = leak(1.5, 7, 20, 0.65, 25, 6.5, 8000, 8)
lb = leak(3, 7, 20, 0.65, 5, 6.5, 8000, 8)
surv_Q = 25 * ls[1] + 5 * lb[1]
surv_kW = 25 * ls[2] + 5 * lb[2]
surv_cost = ls[4] + lb[4]
# load / unload test: 10 m3/min compressor, loaded 18 s of every 60 s with all users off
Qc = 10.0
frac = 18 / 60
leak_lu = Qc * frac
# pressure decay test: 3 m3 of receiver and pipe, 7.0 to 6.0 bar g in 60 s
Vs, dp, tt = 3.0, 1.0, 1.0
leak_pd = Vs * dp / 1.01325 / tt

edit('engineering/compressed-air-leak', date=U, phrase='compressed air leak calculator',
     intro=("Leaks are usually the largest single waste in a compressed air system, and many plants lose a fifth or more of their compressor output through fittings, hoses, drains and worn seals. "
            "This compressed air leak calculator estimates the free air lost through a leak, the compressor power it wastes and the yearly energy cost.\n\n"
            "Energy auditors and maintenance teams use it to rank leaks found in a survey and to justify repairs, ultrasonic detectors and lower header pressure."),
     body_add=f'''
## Second example: pricing a leak survey

An ultrasonic survey on a 7 bar g system tags 25 small leaks of about 1.5 mm equivalent diameter and 5 larger ones of about 3 mm. With the same compressor and tariff as the default example:

- Each 1.5 mm leak loses {ls[1]:.0f} L/min; the 25 together lose {25 * ls[1]:,.0f} L/min
- The 5 larger leaks lose {5 * lb[1]:,.0f} L/min
- Total **{surv_Q:,.0f} L/min** ({surv_Q / 1000:.2f} m³/min), wasting **{surv_kW:.1f} kW** of compressor power
- Yearly cost about **{surv_cost:,.0f}** at 8 per kWh over 8,000 hours

The five large leaks are only a sixth of the count but cost almost half the money, so they go to the top of the repair list. Enter each group with its own diameter and count to get these figures.

## Measuring the total leakage

Two simple tests give the plant total before any leak is found. In the **load and unload test**, all air users are stopped and the compressor cycles only to feed leaks. A {Qc:.0f} m³/min compressor loaded for 18 seconds of every minute is feeding leaks of {frac:.0%} of its output, about **{leak_lu:.1f} m³/min**. In the **pressure decay test**, the compressor is stopped and the time for the pressure to fall is recorded. If {Vs:.0f} m³ of receiver and pipe falls from 7 to 6 bar g in one minute, the leakage is {Vs:.0f} × 1 ÷ 1.013 ÷ 1 = **{leak_pd:.2f} m³/min** of free air. Repeat either test after the repairs to confirm the saving.

Lowering the header pressure also cuts leakage. The default 3 mm leak drops from {l0[1]:.0f} L/min at 7 bar g to {l6[1]:.0f} L/min at 6 bar g, about {cut:.0f}% less, before counting the compressor energy saved.

## Common mistakes

- **Using the gauge pressure in the flow equation.** Choked flow follows the absolute pressure, gauge plus 1.013 bar.
- **Guessing leak size from the noise.** A small leak at a sharp edge can be loud; ultrasonic detectors with a calibrated distance give better size estimates.
- **Running the leak test with users still connected.** Machines left on standby, open blow-off nozzles or cooling air make the leakage look larger than it is.
- **Applying full load specific power to a compressor that modulates.** Inlet throttled machines waste nearly as much power at part load, so the true saving depends on the control type.
- **Fixing leaks and leaving the pressure set high.** Once leaks are repaired the header pressure can often be lowered, which adds a second saving.
''',
     faq_add=[('How do I measure total air leakage with a pressure decay test?',
               f'Stop the compressor with all users off and time the pressure fall. Leakage in m³/min of free air = system volume (m³) × pressure drop (bar) ÷ 1.013 ÷ time (min). {Vs:.0f} m³ falling 1 bar in a minute is about {leak_pd:.2f} m³/min.'),
              ('How much leakage does lowering the header pressure save?',
               f'Leak flow follows absolute pressure, so a 3 mm leak drops from {l0[1]:.0f} L/min at 7 bar g to {l6[1]:.0f} L/min at 6 bar g, about {cut:.0f}% less.')])

print('slice 5 done')

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-21), slice 6: lumen-method, polarization-index, ferranti-effect, ct-burden, earth-conductor-size.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-21'
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Lumen method
E, Lr, Wr, F, UF, MF = 500.0, 10.0, 8.0, 4000.0, 0.6, 0.8
A = Lr * Wr
N = E * A / (F * UF * MF)
Nr = math.ceil(N)
Ea = Nr * F * UF * MF / A
# room index for a 2.8 m ceiling and a 0.8 m work plane, fittings surface mounted
Hm = 2.8 - 0.8
K = Lr * Wr / (Hm * (Lr + Wr))
# grid options
g20 = 20 * F * UF * MF / A
g24 = 24 * F * UF * MF / A
# spacing for a 4 x 6 grid: 6 along the 10 m length, 4 across the 8 m width
sx, sy = Lr / 6, Wr / 4
shr = max(sx, sy) / Hm
# lighting power density at 120 lm/W
eff = 120.0
P_fit = F / eff
P_tot = 24 * P_fit
LPD = P_tot / A
# table: lumen package vs fixtures for 500 lux in this room
f_rows = ''
for fl in (2000, 3000, 4000, 5000, 6000):
    n = E * A / (fl * UF * MF)
    nr = math.ceil(n)
    f_rows += f"| {fl:,} lm | {n:.1f} | {nr} | {nr * fl * UF * MF / A:.0f} lux | {nr * fl / eff:,.0f} W |\n"

edit('electrical/lumen-method', date=U, phrase='lumen method calculator',
     intro=("The lumen method is the standard hand calculation for general lighting: the lumens needed equal the target illuminance times the floor area, corrected for the share of light that reaches the work plane and for ageing and dirt. "
            "This lumen method calculator gives the number of fixtures and the lux they deliver.\n\n"
            "Electrical designers and contractors use it to size office, classroom and plant room lighting before layout software, following the steps of a [lighting design calculation](https://www.instrumentationblog.in/lighting-design-calculation/)."),
     body_add=f'''
## From the result to a real grid

The default room needs **{N:.2f}** fixtures, so the calculator rounds up to **{Nr}** and reports **{Ea:.0f} lux**. Twenty one panels rarely fit a ceiling grid, so check the neighbouring layouts with the same formula:

- 4 × 5 = 20 fixtures: 20 × 4,000 × 0.6 × 0.8 ÷ 80 = **{g20:.0f} lux**, just under target
- 4 × 6 = 24 fixtures: **{g24:.0f} lux**, comfortably above target and easy to dim back

With 6 rows along the 10 m length and 4 across the 8 m width, the spacing is {sx:.2f} m by {sy:.2f} m. For panels mounted on a 2.8 m ceiling above a 0.8 m desk height, the mounting height over the work plane is {Hm:.1f} m, giving a spacing to height ratio of {shr:.2f}, inside the 1.0 to 1.5 that most panel datasheets allow. Keep the outer row about half a spacing from the walls.

## Where the utilisation factor comes from

Manufacturers publish UF tables against the room index K = L × W ÷ [H<sub>m</sub> × (L + W)] and the ceiling, wall and floor reflectances. For this room K = 80 ÷ ({Hm:.1f} × 18) = **{K:.2f}**. A large, low room (K above 2) wastes little light on the walls and typically reaches UF 0.6 to 0.7 with light finishes; a narrow corridor or a tall plant room (K below 1) may fall to 0.35 to 0.45, which can almost double the fixture count for the same lux.

## Lumen package and fixture count for 500 lux in 80 m²

UF 0.6, MF 0.8, and an LED efficacy of {eff:.0f} lm/W for the installed load:

| Lumens per fixture | Exact N | Fixtures | Achieved | Connected load |
|---|---|---|---|---|
{f_rows}
The 4 × 6 layout of 4,000 lm panels draws about {P_tot:.0f} W, a lighting power density of **{LPD:.1f} W/m²**, which is the figure energy codes and green building ratings check.

## Checking the installation with a lux meter

Measure at the work plane height on a regular grid of points, with daylight excluded (at night or with blinds closed) and the LEDs run for at least 20 minutes so their output is stable. The average of the grid is the maintained illuminance once the room is old and dirty only if you divide by the maintenance factor: a new installation should read about E ÷ MF, here around {E / MF:.0f} lux, so a reading of {E:.0f} lux on day one means the room will fall short later. Uniformity is the minimum reading divided by the average; EN 12464-1 asks for at least 0.6 on office task areas.

## Common mistakes

- **Entering lamp lumens for a fitting with a diffuser.** Use the luminaire output from the datasheet, which already includes optic losses, or the count comes out too low.
- **Using the floor to ceiling height for the room index.** The relevant height is from the fitting to the work plane, not to the floor.
- **Taking MF as 1 for LED.** Even long life LEDs lose 10 to 20% of their output by L80 or L90, and dust on the diffuser adds to it.
- **Rounding 20.8 down to 20 to save a fitting.** The average then falls below the target before any ageing.
- **Applying an office UF to a dark warehouse.** Low reflectance walls and racking absorb far more light, so take the UF from the table at the real reflectances.
''',
     faq_add=[('What is the room index and how does it affect the UF?',
               f'Room index K = L × W ÷ [Hm × (L + W)], with Hm the height of the fittings above the work plane. A 10 m × 8 m room with fittings {Hm:.0f} m above the desks has K = {K:.2f}. Higher K means less light lost on the walls and a higher UF from the manufacturer table.'),
              ('What lux should a new lighting installation measure?',
               f'About the design illuminance divided by the maintenance factor. With 500 lux and MF 0.8, a new room should read around {E / MF:.0f} lux on average, falling to 500 lux by the end of the maintenance period.')])

# ---------------------------------------------------------------- Polarization index
R30, R1, R10 = 800.0, 1000.0, 2500.0
PI = R10 / R1
DAR = R1 / R30
# wet winding readings
w30, w1, w10 = 40.0, 45.0, 50.0
wPI, wDAR = w10 / w1, w1 / w30
# temperature correction to 40 C, halving per 10 C (IEEE 43 approximation)
Tw = 20.0
Kt = 0.5 ** ((40 - Tw) / 10)
R1_40 = R1 * Kt
# minimum IR1 at 40 C (IEEE 43-2013)
kV = 6.6
IR_old = kV + 1
iv = [('Below 1,000 V', '500 V'), ('1,000 to 2,500 V', '500 to 1,000 V'), ('2,501 to 5,000 V', '1,000 to 2,500 V'),
      ('5,001 to 12,000 V', '2,500 to 5,000 V'), ('Above 12,000 V', '5,000 to 10,000 V')]
v_rows = ''.join(f"| {a} | {b} DC |\n" for a, b in iv)
t_rows = ''
for T in (10, 20, 30, 40, 50, 60):
    k = 0.5 ** ((40 - T) / 10)
    t_rows += f"| {T} °C | {k:.3f} | {R1 * k:,.0f} MΩ |\n"

edit('electrical/polarization-index', date=U, phrase='polarization index calculator',
     intro=("A healthy insulation's resistance keeps rising during a megger test as the dielectric polarizes, while moist or contaminated insulation levels off quickly. "
            "This polarization index calculator turns the 30 second, 1 minute and 10 minute readings into the PI and the DAR, using the [insulation resistance test with a megger](https://www.instrumentationblog.in/insulation-resistance-test-megger/).\n\n"
            "Maintenance electricians and motor repair shops use it to decide whether a motor, generator or transformer winding is dry and clean enough to energise or needs drying out first."),
     body_add=f'''
## A wet winding for comparison

The defaults give PI = **{PI:.2f}** and DAR = **{DAR:.2f}**: the current falls steadily over ten minutes, which is what clean, dry insulation does. Compare a pump motor that stood in a flooded pit and reads {w30:.0f} MΩ at 30 s, {w1:.0f} MΩ at 1 min and {w10:.0f} MΩ at 10 min:

- PI = {w10:.0f} ÷ {w1:.0f} = **{wPI:.2f}**, questionable and close to the 1.0 danger line
- DAR = {w1:.0f} ÷ {w30:.0f} = **{wDAR:.2f}**, poor

The leakage current through the moisture is so large that it swamps the slowly decaying absorption current, so the reading hardly moves. Dry the winding with heaters or low voltage current and repeat the test; a rising PI over successive tests shows the drying is working.

## Test voltage by winding rating (IEEE 43)

| Winding rated voltage (line to line) | DC test voltage |
|---|---|
{v_rows}
Use the same voltage every time you test a machine, because the readings at different voltages are not directly comparable.

## Correcting the 1 minute reading to 40 °C

Insulation resistance falls as the winding warms. IEEE 43 gives a rough rule that it halves for every 10 °C, so the factor to 40 °C is K<sub>T</sub> = 0.5<sup>(40 − T)/10</sup>. A winding tested at {Tw:.0f} °C has K<sub>T</sub> = {Kt:.2f}, so the default {R1:,.0f} MΩ becomes **{R1_40:,.0f} MΩ** at 40 °C. That corrected figure is compared with the IEEE 43 minimum: 100 MΩ for form wound stator windings built after 1970, 5 MΩ for random wound windings below 1 kV, and kV + 1 MΩ for older windings ({IR_old:.1f} MΩ for a {kV:g} kV machine). The PI itself is a ratio of two readings at the same temperature and needs no correction.

| Winding temperature | K<sub>T</sub> to 40 °C | 1,000 MΩ corrected |
|---|---|---|
{t_rows}
## Common mistakes

- **Testing straight after a previous test.** Charge left in the winding makes the next readings climb too fast; ground the winding for at least four times the previous test time first.
- **Leaving the cable and VFD connected.** The cable adds its own capacitance and leakage, and drive electronics can be damaged by the test voltage, so disconnect at the motor terminal box where possible.
- **Ignoring the guard terminal on dirty terminals.** Surface leakage across a contaminated terminal board can make good insulation look poor; guard it out to see the winding alone.
- **Trusting a PI on very high readings.** When the 1 minute value is above about 5,000 MΩ the meter is near its noise floor and a PI below 2 does not mean the insulation is bad.
- **Comparing readings taken hot and cold.** A motor tested just after running reads far lower than the same motor cold, so always record the winding temperature.
''',
     faq_add=[('What test voltage should I use for a PI test?',
               'Follow IEEE 43: 500 V DC for windings rated below 1,000 V, 500 to 1,000 V for 1,000 to 2,500 V, 1,000 to 2,500 V up to 5 kV, 2,500 to 5,000 V up to 12 kV and 5,000 to 10,000 V above that.'),
              ('How do I correct insulation resistance to 40 °C?',
               f'Multiply the reading by 0.5 raised to (40 − T) ÷ 10, where T is the winding temperature in °C. A {R1:,.0f} MΩ reading at {Tw:.0f} °C corrects to about {R1_40:,.0f} MΩ at 40 °C.')])

# ---------------------------------------------------------------- Ferranti effect
Vs, l, L, C, f = 400.0, 300.0, 1.0, 11.5, 50.0
beta = 2 * math.pi * f * math.sqrt(L * 1e-6 * C * 1e-12) * 1000  # rad/km (L, C per km in SI per m, l in km)
bl = beta * l
Vr = Vs / math.cos(bl)
rise = Vr / Vs - 1
approx = (bl ** 2) / 2
w = 2 * math.pi * f
Qc = (Vs * 1e3) ** 2 * w * C * 1e-9 * l / 1e6  # Mvar, three phase
Zc = math.sqrt(L * 1e-3 / (C * 1e-9))
SIL = (Vs * 1e3) ** 2 / Zc / 1e6
v = 1 / math.sqrt(L * 1e-3 * C * 1e-9)  # km/s
lam = v / f
# same line at 60 Hz
bl60 = 2 * math.pi * 60 * math.sqrt(L * 1e-3 * C * 1e-9) * l
rise60 = 1 / math.cos(bl60) - 1
# 132 kV XLPE cable: 0.4 mH/km, 250 nF/km
Lc, Cc = 0.4, 250.0
c_rows = ''
for lc in (10, 25, 50, 75, 100):
    b = 2 * math.pi * f * math.sqrt(Lc * 1e-3 * Cc * 1e-9) * lc
    q = (132e3) ** 2 * w * Cc * 1e-9 * lc / 1e6
    c_rows += f"| {lc} km | {(1 / math.cos(b) - 1) * 100:.2f}% | {132 / math.cos(b):.1f} kV | {q:.0f} Mvar |\n"
assert abs(rise * 100 - 5.33) < 0.01

edit('electrical/ferranti-effect', date=U, phrase='ferranti effect calculator',
     intro=("On a long, lightly loaded transmission line the charging current flowing through the line inductance makes the receiving end voltage rise above the sending end voltage. "
            "This Ferranti effect calculator uses the lossless line equation Vr = Vs ÷ cos(βl) to find that rise, as explained in the [Ferranti effect in transmission lines](https://www.instrumentationblog.in/ferranti-effect-transmission-line/).\n\n"
            "Power system planners and substation engineers use it to check open line voltages during energisation and to judge how much shunt reactor compensation a long line or cable needs."),
     body_add=f'''
## Charging power and shunt reactors

The default line rises by **{rise * 100:.2f}%** to **{Vr:.1f} kV** when open at the far end. The reactive power it generates is roughly Q<sub>c</sub> = V² × ω × C × l = (400 kV)² × {w:.1f} × 11.5 nF/km × 300 km ≈ **{Qc:.0f} Mvar**. Utilities usually compensate 60 to 80% of this with shunt reactors at one or both ends, for example two {Qc * 0.35:.0f} Mvar reactors, which pulls the open end voltage back close to the sending end value.

The same constants give a surge impedance of √(L ÷ C) = **{Zc:.0f} Ω** and a surge impedance loading of V² ÷ Z<sub>c</sub> = **{SIL:.0f} MW**. Below SIL the line generates more reactive power than it absorbs and the voltage profile rises along the line; above SIL it falls. The Ferranti effect is the extreme case of zero load.

## Why the rise grows so fast with length

The small angle form V<sub>r</sub> ÷ V<sub>s</sub> ≈ 1 + (βl)² ÷ 2 gives {approx * 100:.2f}% for the default line, close to the exact {rise * 100:.2f}%. The rise goes with the square of length and of frequency, so doubling the line from 300 to 600 km roughly quadruples it, and the same line on a 60 Hz system rises by **{rise60 * 100:.2f}%**. The wave travels at 1 ÷ √(LC) ≈ {v:,.0f} km/s, a wavelength of {lam:,.0f} km at 50 Hz; a line a quarter wavelength long ({lam / 4:,.0f} km) would in theory give an infinite open end voltage, which is why very long AC lines are split into compensated sections or replaced by HVDC.

## Underground cable: 132 kV, 0.4 mH/km, 250 nF/km, 50 Hz

| Cable length | Rise | Open end voltage | Charging power |
|---|---|---|---|
{c_rows}
The voltage rise on a cable stays modest, but the charging current is the real limit: a long cable can use up most of its own thermal rating carrying reactive current, which is why long AC cable routes have reactors at intermediate points.

## How it shows up in operation

Operators see the effect when a line is energised from one end: the voltage transformer at the open end reads above the sending end bus. Switching studies check this before the event, adding the rise caused by the source impedance, because charging current flowing through a weak source raises the sending end voltage too. The usual practice is to energise long lines from the stronger end and close the far end breaker within seconds.

## Common mistakes

- **Entering capacitance in µF/km as nF/km.** Overhead lines are about 0.011 µF/km, which is 11 nF/km; a factor of 1,000 error gives a nonsense electrical length.
- **Using cable constants for an overhead line or the reverse.** Cable capacitance is 20 to 50 times higher and inductance about a third.
- **Treating the rise as linear in length.** It grows roughly with the square of length, so halving a section cuts the rise by about four.
- **Ignoring the source.** The calculator assumes a stiff sending end; a weak source adds its own rise on top.
- **Forgetting that load removes the effect.** At loads near SIL the receiving end voltage is close to the sending end, so the open line case is the one to design for.
''',
     faq_add=[('How much shunt reactor compensation does a long line need?',
               f'Start from the charging power Qc ≈ V² × ω × C × l. For a 400 kV, 300 km line with 11.5 nF/km at 50 Hz that is about {Qc:.0f} Mvar, and 60 to 80% of it is commonly installed as shunt reactors.'),
              ('Is the Ferranti effect worse on a 60 Hz system?',
               f'Yes. βl is proportional to frequency and the rise roughly to its square, so the default 300 km line rises {rise * 100:.2f}% at 50 Hz but about {rise60 * 100:.2f}% at 60 Hz.')])

# ---------------------------------------------------------------- CT burden
Is, Lm, Amm, Rd = 5.0, 50.0, 2.5, 2.0
rho = 1.72e-8


def burden(Is, Lm, Amm, Rd):
    Rl = 2 * Lm * rho / (Amm * 1e-6)
    Bl = Is ** 2 * Rl
    return Rl, Bl, Bl + Rd


Rl, Bl, B = burden(Is, Lm, Amm, Rd)
Rl1, Bl1, B1 = burden(1.0, Lm, Amm, Rd)
Rl4, Bl4, B4 = burden(5.0, Lm, 4.0, Rd)
Rl6, Bl6, B6 = burden(5.0, Lm, 6.0, Rd)
# hot leads at 75 C
Rl_hot = Rl * (1 + 0.00393 * (75 - 20))
B_hot = Is ** 2 * Rl_hot + Rd
# effective ALF of a 5P20 15 VA CT with Rct 0.3 ohm (5 A secondary)
ALF, VAr, Rct = 20, 15.0, 0.3
Rb_rated = VAr / Is ** 2
Rb_act = B / Is ** 2
ALFe = ALF * (Rct + Rb_rated) / (Rct + Rb_act)
# injection test voltage for the default burden
Vinj = B / Is
assert abs(B - 19.2) < 1e-9

edit('electrical/ct-burden', date=U, phrase='ct burden calculator',
     intro=("A current transformer (CT) only holds its accuracy while the load on its secondary, the burden, stays within its VA rating, and long leads with thin cable add more burden than people expect on 5 A secondaries. "
            "This CT burden calculator adds up leads and devices; see the [CT burden calculation](https://www.instrumentationblog.in/ct-burden-calculation-va/).\n\n"
            "Protection and metering engineers use it to choose the CT rating, cable size and 1 A or 5 A secondary before ordering switchgear or extending a panel."),
     body_add=f'''
## Worked example with the default values

A 5 A CT feeds a relay and meter with a combined burden of 2 VA through 50 m of 2.5 mm² copper:

- Lead loop resistance = 2 × 50 × 1.72 × 10⁻⁸ ÷ 2.5 × 10⁻⁶ = **{Rl:.3f} Ω**
- Lead burden = 5² × {Rl:.3f} = **{Bl:.1f} VA**
- Total burden = {Bl:.1f} + 2 = **{B:.1f} VA**

The leads use almost 90% of the total. A 15 VA CT is overloaded, and the options are clear when you rerun the numbers:

| Change | Loop resistance | Total burden |
|---|---|---|
| As designed, 5 A, 2.5 mm² | {Rl:.3f} Ω | {B:.1f} VA |
| 5 A, 4 mm² cable | {Rl4:.3f} Ω | {B4:.2f} VA |
| 5 A, 6 mm² cable | {Rl6:.3f} Ω | {B6:.2f} VA |
| 1 A secondary, 2.5 mm² | {Rl1:.3f} Ω | {B1:.2f} VA |

Switching to a 1 A CT cuts the total to **{B1:.2f} VA** without touching the cable, which is why remote panels and long switchyard runs nearly always use 1 A secondaries. Check that the relay input is also set or rated for 1 A.

## Effect on a protection CT

For a 5P20 CT the accuracy limit factor holds only at rated burden. With a secondary winding resistance of {Rct} Ω, a 15 VA rating means {Rb_rated:.2f} Ω of external burden, while the default circuit is {Rb_act:.3f} Ω. The effective factor falls to 20 × ({Rct} + {Rb_rated:.2f}) ÷ ({Rct} + {Rb_act:.3f}) ≈ **{ALFe:.1f}**, so the CT saturates at about {ALFe:.0f} times rated current instead of 20. For a feeder with high fault levels that can delay an overcurrent relay or make a differential scheme unstable.

## Measuring the burden on site

Short and isolate the CT at its test block, then inject rated secondary current into the burden side with a secondary injection set and read the voltage across it. Burden in VA is V × I: for the default circuit you should read about {Vinj:.2f} V at 5 A. Alternatively measure the loop resistance with a low resistance ohmmeter and add the device burdens from their datasheets. Leads warm up in a hot panel or cable tray; at 75 °C copper is about 21% higher, which takes the default total to {B_hot:.1f} VA.

## Common mistakes

- **Using the one way length.** Current goes out on one core and back on another, so the loop is twice the route length.
- **Forgetting the earth fault case with star connected CTs.** Under balanced load the common return carries almost nothing, but for a phase to earth fault the full current flows out and back, so size for 2 × L.
- **Adding device VA quoted at 1 A to a 5 A circuit.** A relay burden of 0.1 VA at 1 A is a resistance of 0.1 Ω, which is 2.5 VA at 5 A; convert to ohms first.
- **Leaving out test blocks, terminals and links.** Each joint adds a few milliohms; on 5 A circuits a dozen joints add noticeable VA.
- **Choosing a CT rated far above the burden for metering.** Metering accuracy is specified from 25% to 100% of rated burden, so a 30 VA CT on a 2 VA meter circuit can read outside its class.
''',
     faq_add=[('How does extra burden affect a protection CT?',
               f'It lowers the effective accuracy limit factor: ALF × (Rct + Rrated) ÷ (Rct + Ractual). A 5P20 15 VA CT with 0.3 Ω winding resistance on the default {B:.1f} VA circuit drops to about {ALFe:.1f}.'),
              ('How do I measure CT burden on site?',
               f'Short the CT at its test block, inject rated current into the secondary wiring and read the voltage. VA = V × I, so about {Vinj:.2f} V at 5 A means {B:.1f} VA.')])

# ---------------------------------------------------------------- Earth conductor size
I, t, k = 10e3, 0.4, 143.0
S = I * math.sqrt(t) / k
std = [1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]


def nxt(s):
    return next(x for x in std if x >= s)


assert abs(S - 44.2) < 0.05
opts = [('Copper, separate, PVC', 143), ('Copper, separate, XLPE/EPR', 176), ('Copper, core of PVC cable', 115),
        ('Bare copper, no fire risk', 159), ('Aluminium, separate, PVC', 95), ('Aluminium, separate, XLPE', 116),
        ('Steel, separate, PVC', 52)]
k_rows = ''
for nm, kk in opts:
    s = I * math.sqrt(t) / kk
    k_rows += f"| {nm} | {kk} | {s:.1f} mm² | {nxt(s):g} mm² |\n"


# k from IEC 60364-5-54 Annex A, copper: Qc 3.45e-3 J/(C mm3), B 234.5 C, rho20 17.241e-6 ohm mm
def kcu(ti, tf):
    return math.sqrt(3.45e-3 * (234.5 + 20) / 17.241e-6 * math.log((234.5 + tf) / (234.5 + ti)))


k143, k115 = kcu(30, 160), kcu(70, 160)
# lower fault current with a slower trip: 3 kA cleared in 2 s
S2 = 3e3 * math.sqrt(2) / k

edit('electrical/earth-conductor-size', date=U, phrase='earth conductor size calculator',
     intro=("A protective earth conductor must carry the full fault current for the time a breaker or fuse takes to trip, without overheating its insulation. "
            "This earth conductor size calculator applies the adiabatic equation, as explained in this [earth conductor size calculation](https://www.instrumentationblog.in/earth-conductor-size-calculation/).\n\n"
            "Electrical designers and installers use it to size circuit protective conductors, armour and bonding for sub mains and motor feeders, taking the fault current from a [short circuit current calculation](https://www.instrumentationblog.in/short-circuit-current-calculation/)."),
     body_add=f'''
## Worked example with the default values

A 10 kA earth fault is cleared in 0.4 s and the protective conductor is a separate PVC insulated copper wire (k = 143):

- I²t = 10,000² × 0.4 = 4.0 × 10⁷ A²s
- S = √(4.0 × 10⁷) ÷ 143 = 6,325 ÷ 143 = **{S:.1f} mm²**
- Next standard size: **{nxt(S):g} mm²**

The same fault needs a different size for each conductor and insulation:

| Conductor | k | Minimum S | Standard size |
|---|---|---|---|
{k_rows}
## Where k comes from

IEC 60364-5-54 Annex A derives k from the conductor's heat capacity, resistivity and the allowed temperature rise: k = √[Q<sub>c</sub>(B + 20) ÷ ρ<sub>20</sub> × ln((B + θ<sub>f</sub>) ÷ (B + θ<sub>i</sub>))]. For copper (Q<sub>c</sub> = 3.45 × 10⁻³ J/°C mm³, B = 234.5 °C, ρ<sub>20</sub> = 17.241 × 10⁻⁶ Ω mm) and PVC with a final 160 °C, starting at 30 °C gives **{k143:.0f}** for a separate conductor, while starting at 70 °C, because a core inside a loaded cable is already warm, gives **{k115:.0f}**. That is why the same copper has two very different k values.

## Lower fault current is not always easier

The equation rewards a short disconnection time much more than a low current. A 3 kA fault that a slow fuse clears in 2 s needs √(3,000² × 2) ÷ 143 = **{S2:.1f} mm²**, not far below the 10 kA case, and at even lower currents the device may not trip in time at all. Always read t from the device's time current curve at the actual earth fault current. For devices that clear in under 0.1 s, such as MCBs and current limiting fuses in their instantaneous region, use the let through I²t from the manufacturer instead of I² × t.

## Checking it on site

After installation the protective conductor is verified by a continuity test (R1 + R2) and an earth fault loop impedance test. The measured Zs gives the real fault current, I = U<sub>0</sub> ÷ Z<sub>s</sub>, which should be at least the value used in the sizing so the trip time assumed in the calculation holds.

## Common mistakes

- **Using the three phase fault level.** The earth fault current is usually lower because of the earth return impedance, which can mean a longer trip time.
- **Taking the breaker's nominal 0.4 s instead of its curve.** The real clearing time at the calculated current may be longer or much shorter.
- **Choosing k for a separate conductor when it is a cable core.** A core in a PVC cable has k = 115, needing about 24% more copper than k = 143.
- **Rounding down to the nearest size.** {S:.1f} mm² means {nxt(S):g} mm², not 35 mm².
- **Ignoring steel armour and conduit k values.** Steel has k around 46 to 52, so armour used as the protective conductor needs about three times the copper area.
''',
     faq_add=[('Why does a lower fault current sometimes need a bigger earth conductor?',
               f'Because the protective device trips more slowly at low current and S depends on √t. A 3 kA fault cleared in 2 s needs about {S2:.1f} mm² of PVC copper, close to the {S:.1f} mm² for 10 kA at 0.4 s.'),
              ('How is the k factor for an earth conductor calculated?',
               f'From IEC 60364-5-54 Annex A using the conductor heat capacity, resistivity and the initial and final temperatures. For copper and PVC to 160 °C, starting at 30 °C gives about {k143:.0f} and starting at 70 °C gives about {k115:.0f}.')])

print('slice 6 done')
