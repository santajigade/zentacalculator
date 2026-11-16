"""Part C expansion (2026-11-16): 20 thin pages from tools/upgrade-backlog.txt, brought to the api-gravity standard. Assembled from two sections; edits are applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Part C expand (2026-11-16), slice 1: pulley-speed, compressor-power, low-flow-cutoff,
vortex-shedding-frequency, pump-affinity-laws, fopdt-step-test, gear-ratio, rotameter-correction,
calibration-error, weld-size. Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-16'
pi = math.pi

# ---------------------------------------------------------------- Pulley speed
N1, D1, D2, C = 1440, 100.0, 250.0, 500.0
N2 = N1 * D1 / D2
Lb = 2 * C + pi * (D1 + D2) / 2 + (D2 - D1) ** 2 / (4 * C)
wrap = 180 - 2 * math.degrees(math.asin((D2 - D1) / (2 * C)))
T_in = 9550 * 5.5 / N1  # 5.5 kW motor torque
T_out = T_in * D2 / D1
Lstd = 1600.0
b = 2 * Lstd - pi * (D1 + D2)
Cstd = (b + math.sqrt(b * b - 8 * (D2 - D1) ** 2)) / 8
Dt = D1 * N1 / 720
wr_rows = ''
for c in (250, 300, 400, 500, 750, 1000):
    w = 180 - 2 * math.degrees(math.asin((D2 - D1) / (2 * c)))
    L = 2 * c + pi * (D1 + D2) / 2 + (D2 - D1) ** 2 / (4 * c)
    wr_rows += f"| {c:,} mm | {L:,.0f} mm | {w:.1f}° |\n"
bs_rows = ''
for d in (80, 100, 125, 160, 200, 250):
    bs_rows += f"| {d} mm | {pi*d/1000*960/60:.2f} m/s | {pi*d/1000*1440/60:.2f} m/s | {pi*d/1000*2900/60:.2f} m/s |\n"

edit('engineering/pulley-speed', date=U, phrase='pulley speed and belt length calculator',
     intro=("Belt and pulley drives change the speed and torque between a motor and a machine: the pulley diameters set the speed ratio "
            "and the shaft centre distance sets the belt length. This pulley speed and belt length calculator gives driven rpm, ratio, belt speed and belt length.\n\n"
            "Maintenance fitters, millwrights and machine designers use it to change a fan or pump speed, pick a replacement pulley "
            "and order the right belt before taking a drive apart."),
     body_add=f'''
## Centre distance for a standard belt

Belts come in fixed lengths, so after choosing a size you usually work back to the centre distance. Rearranging the belt length formula gives:

<p class="formula">C = [b + √(b² − 8 (D₂ − D₁)²)] ÷ 8, where b = 2L − π (D₁ + D₂)</p>

For the example drive with a standard {Lstd:,.0f} mm pitch length belt:

- b = 2 × {Lstd:,.0f} − π × ({D1:g} + {D2:g}) = **{b:,.1f} mm**
- C = [{b:,.1f} + √({b:,.1f}² − 8 × {D2-D1:g}²)] ÷ 8 = **{Cstd:.1f} mm**

So the motor must sit about {Cstd-C:.0f} mm further away than the {C:g} mm assumed above, which is within the travel of normal slide rails.

## Wrap angle and torque

The belt wraps less than half way round the small pulley, and grip depends on that arc:

<p class="formula">Wrap angle on the small pulley = 180° − 2 × asin[(D₂ − D₁) ÷ (2C)]</p>

For the example, wrap = 180 − 2 × asin({D2-D1:g} ÷ {2*C:g}) = **{wrap:.1f}°**. A 5.5 kW motor at {N1:,} rpm gives 9,550 × 5.5 ÷ {N1:,} = {T_in:.1f} N·m on its shaft, and the {D2/D1:g}:1 ratio raises that to about **{T_out:.1f} N·m** on the driven shaft before belt losses. To run the driven shaft at 720 rpm instead, the driven pulley must be {D1:g} × {N1:,} ÷ 720 = **{Dt:.0f} mm**.

## Belt length and wrap angle against centre distance

For the {D1:g} mm and {D2:g} mm pulleys:

| Centre distance | Belt length | Wrap on small pulley |
|---|---|---|
{wr_rows}
## Belt speed by driver pulley diameter

| Driver pitch diameter | 960 rpm (6 pole) | 1,440 rpm (4 pole) | 2,900 rpm (2 pole) |
|---|---|---|---|
{bs_rows}
## Common mistakes

- **Using the outside diameter of a V-belt pulley.** Speed ratio and belt length use the pitch diameter, which is smaller than the rim diameter; using the rim figure gives a belt that is too long.
- **Using synchronous speed.** A 4 pole motor on 50 Hz turns at about 1,440 rpm under load, not 1,500 rpm. Use the nameplate speed.
- **Ignoring a short centre distance.** Below about 120° of wrap the small pulley slips; increase the centre distance or use an idler on the slack side.
- **Exceeding the pulley rim speed.** A large pulley on a 2 pole motor can pass the maker's maximum rim speed for cast iron. Check before speeding up a drive.
- **Fitting one new belt on a multi-belt drive.** Old belts have stretched, so the new one carries most of the load. Replace matched sets together.
''',
     faq_add=[('How do I find the centre distance for a standard belt length?',
               f'Use C = [b + √(b² − 8(D₂ − D₁)²)] ÷ 8 with b = 2L − π(D₁ + D₂). For 100 mm and 250 mm pulleys and a 1,600 mm belt, b = {b:,.1f} mm and C = {Cstd:.1f} mm.'),
              ('What is the wrap angle of a belt drive?',
               f'It is the arc of contact on the small pulley, 180° − 2 asin((D₂ − D₁) ÷ 2C). For 100 mm and 250 mm pulleys at 500 mm centres it is {wrap:.1f}°. Below about 120° the belt tends to slip.')])

# ---------------------------------------------------------------- Compressor power
V, p1, p2, T1, k, eta = 600 / 3600, 1.01325e5, 8e5, 293.15, 1.4, 0.75
ex = (k - 1) / k
def cpow(p1, p2, V, T1=293.15):
    return k / (k - 1) * p1 * V * ((p2 / p1) ** ex - 1)
Pis = cpow(p1, p2, V)
Ps = Pis / eta
T2 = T1 * (p2 / p1) ** ex
T2act = T1 + (T2 - T1) / eta
Piso = p1 * V * math.log(p2 / p1)
r2 = math.sqrt(p2 / p1)
pm = p1 * r2
Pst = 2 * cpow(p1, pm, V) / eta  # intercooled to 20 °C: second stage inlet volume = V p1/pm, p V same
T2s = T1 * r2 ** ex
cs_rows = ''
for pd in (4e5, 6e5, 8e5, 10e5, 13e5, 16e5):
    one = cpow(p1, pd, V) / eta
    rr = math.sqrt(pd / p1)
    two = 2 * cpow(p1, p1 * rr, V) / eta
    iso = p1 * V * math.log(pd / p1)
    cs_rows += f"| {pd/1e5:g} bar(a) | {one/1000:.1f} kW | {two/1000:.1f} kW | {(1-two/one)*100:.0f}% | {iso/1000:.1f} kW |\n"

edit('engineering/compressor-power', date=U, phrase='compressor power calculator',
     intro=("The ideal work to compress a gas follows the isentropic relation, and a real machine needs more by the inverse of its isentropic efficiency. "
            "This compressor power calculator gives shaft power and ideal discharge temperature for one stage.\n\n"
            "Utility, process and energy engineers use it to size compressor motors, check a vendor's power figure and see when staging pays off, "
            "as explained in [single-stage vs multi-stage compressors](https://www.instrumentationblog.in/single-stage-and-multi-stage-compressor/)."),
     body_add=f'''
## Real discharge temperature

The ideal T₂ assumes no losses. The extra work of an inefficient stage also ends up as heat in the gas, so a better estimate is T₂ ≈ T₁ + (T₂,ideal − T₁) ÷ η. For the example, T₂ ≈ 20 + ({T2-273.15:.0f} − 20) ÷ {eta:g} = **{T2act-273.15:.0f} °C**. That is far above the limit for most lubricants and seals, which is why single-stage dry compression to 8 bar is rare and oil-injected screws cool the gas with the oil.

## Two stages with intercooling

Splitting the same duty into two stages with equal pressure ratios and cooling back to 20 °C between them:

- Ratio per stage = √{p2/p1:.3f} = **{r2:.3f}**, so the intermediate pressure is {pm/1e5:.3f} bar(a)
- Each stage handles the same p × V, so each needs the same power: {cpow(p1, pm, V)/1000:.2f} ÷ {eta:g} = {cpow(p1, pm, V)/eta/1000:.2f} kW
- Total shaft power = **{Pst/1000:.1f} kW** against {Ps/1000:.1f} kW for one stage, a saving of {(1-Pst/Ps)*100:.0f}%
- Ideal discharge temperature of each stage = **{T2s-273.15:.0f} °C**

The isothermal limit, p₁V₁ ln(p₂/p₁) = **{Piso/1000:.1f} kW** of ideal work, is the floor that more stages approach.

## One stage, two stages and the isothermal limit

600 m³/h of air at 1.01325 bar(a) and 20 °C, η = {eta*100:.0f}% per stage, intercooled to 20 °C:

| Discharge | One stage | Two stages | Saving | Isothermal ideal |
|---|---|---|---|---|
{cs_rows}
## Using the result in practice

The inlet flow must be the **actual** volume at suction conditions. Vendors often quote free air delivery (FAD) or normal m³/h; convert those to actual inlet flow with the [gas flow correction calculator](/engineering/gas-flow-correction/) first. Add the motor efficiency (typically 94 to 96% for this size) and any belt or gearbox loss to get the electrical input, and leave a margin for filter fouling and higher summer inlet temperature.

## Common mistakes

- **Entering gauge pressure.** 7 bar(g) is 8.013 bar(a); using 7 and 0 bar gives a ratio that is meaningless.
- **Using normal or standard flow as inlet flow.** At a hot or low pressure inlet the actual volume is larger than the normal volume, and the power scales with it.
- **Confusing isentropic and isothermal efficiency.** Screw and reciprocating data usually quote isentropic efficiency; turbo compressor maps may quote polytropic efficiency, which is higher for the same machine.
- **Sizing the motor on shaft power alone.** Motor, drive and transmission losses add several percent, and the motor should not run continuously above its rating.
- **Ignoring inlet temperature.** Power is proportional to absolute inlet temperature for a given mass flow, so warm intake air costs energy.
''',
     faq_add=[('How much power does two-stage compression save?',
               f'With equal pressure ratios and intercooling to the inlet temperature, compressing 600 m³/h of air to 8 bar(a) needs {Pst/1000:.1f} kW instead of {Ps/1000:.1f} kW at 75% efficiency, a saving of about {(1-Pst/Ps)*100:.0f}%. The saving grows with the overall pressure ratio.'),
              ('What is isothermal compressor power?',
               f'It is the ideal work if the gas is kept at inlet temperature: P = p₁V₁ ln(p₂/p₁). For 600 m³/h from 1.01325 to 8 bar(a) it is {Piso/1000:.1f} kW, against {Pis/1000:.1f} kW ideal isentropic work. No real machine reaches it, but intercooled stages get closer.')])

# ---------------------------------------------------------------- Low flow cutoff
q, Qmax, DPmax = 0.05, 100.0, 250.0
noise = 0.0005  # 0.05% of DP span
fn5 = math.sqrt(q * q + noise) - q
z_rows = ''
for z in (0.0001, 0.0005, 0.001, 0.0025, 0.005, 0.01):
    z_rows += f"| {z*100:g}% | {z*DPmax:.3f} mbar | {math.sqrt(z)*100:.2f}% | {math.sqrt(z)*Qmax:.2f} m³/h |\n"
zf = math.sqrt(0.001)

edit('engineering/low-flow-cutoff', date=U, phrase='low flow cutoff calculator',
     intro=("With square-root extraction, flow = √DP, so tiny DP noise near zero becomes a large, jumping flow reading, and a cutoff forces the output to zero below a set point. "
            "This low flow cutoff calculator converts the cutoff between flow and DP and shows the noise gain.\n\n"
            "Instrument and DCS engineers use it when configuring orifice and other DP flow loops, as described in "
            "[square-root extraction in DP flow measurement](https://www.instrumentationblog.in/square-root-extraction-dp-flow/)."),
     body_add=f'''
## How a small zero error becomes false flow

With the pipe blocked in and no flow, any zero offset in the transmitter is square rooted too. A zero shift of only 0.1% of the {DPmax:g} mbar span ({0.001*DPmax:.2f} mbar) reads as √0.001 = **{zf*100:.2f}%** flow, or {zf*Qmax:.2f} m³/h on a {Qmax:g} m³/h meter, and the totalizer keeps counting it. With the {q*100:g}% cutoff in this example that error is hidden, which is the purpose of the cutoff. Noise behaves the same way: at the cutoff, a DP disturbance of 0.05% of span moves the flow reading by √({q:g}² + 0.0005) − {q:g} = **{fn5*100:.2f}%** of flow.

## False flow from a zero offset

For a {DPmax:g} mbar span and {Qmax:g} m³/h maximum flow:

| Zero offset (% of DP span) | Offset | Apparent flow | Apparent flow |
|---|---|---|---|
{z_rows}
## Setting the cutoff in practice

Re-zero the transmitter at line pressure with the equalising valve open, then watch the flow reading with the meter blocked in. The cutoff should sit comfortably above the noise band seen there, but below the lowest flow the process needs to see. Many smart transmitters offer a **linear section** below a break point instead of a hard cutoff, so the output follows DP in a straight line near zero rather than jumping. In a DCS, add a little hysteresis (for example cut out at 5% and back in at 6%) so the reading does not chatter around the set point.

## Common mistakes

- **Entering the cutoff as a DP percentage.** A setting of 5% in a field marked DP is about 22% of flow (√0.05), which hides a large part of the range.
- **Square rooting twice.** If the transmitter is set to square root output, the DCS input must be linear, or the reading will follow the fourth root of DP.
- **Applying the cutoff in two places.** Two cutoffs with different settings make it hard to tell why the reading drops to zero.
- **Using the cutoff to hide a bad zero.** A cutoff masks drift but does not fix it; recalibrate when the blocked-in reading wanders.
- **Forgetting the totalizer.** Flow below the cutoff is not counted, so batch and custody totals read low on long low-flow periods.
''',
     faq_add=[('How much false flow does a DP zero error cause?',
               f'Flow reading = √(zero error as a fraction of DP span). A 0.1% zero offset reads as {zf*100:.2f}% of flow and a 1% offset as 10% of flow, which is why the zero must be checked at line pressure before a cutoff is chosen.')])

# ---------------------------------------------------------------- Vortex shedding
Vv, dv, St, Dp = 3.0, 0.020, 0.2, 0.100
nu = 1.0e-6
Re = Vv * Dp / nu
f = St * Vv / dv
vmin = 20000 * nu / Dp
fmin = St * vmin / dv
Qmin = vmin * pi * Dp ** 2 / 4 * 3600
vk_rows = ''
for dn, d_mm in ((25, 25), (50, 50), (80, 80), (100, 100), (150, 150), (200, 200)):
    Dm = d_mm / 1000
    bb = 0.2 * Dm
    fq = St * 3.0 / bb
    Qq = 3.0 * pi * Dm ** 2 / 4
    vk_rows += f"| DN{dn} | {bb*1000:.0f} mm | {fq:.1f} Hz | {Qq*3600:.1f} m³/h | {fq/(Qq*1000):.3f} |\n"

edit('engineering/vortex-shedding-frequency', date=U, phrase='vortex shedding frequency calculator',
     intro=("Fluid flowing past a bluff body sheds vortices from alternate sides at a frequency proportional to velocity. "
            "This vortex shedding frequency calculator uses f = St × V ÷ d, the principle explained in [how a vortex shedding flowmeter works](https://www.instrumentationblog.in/vortex-shedding-flowmeter-working/).\n\n"
            "Instrument engineers use it to size vortex meters and estimate K-factors, and mechanical engineers use it to check thermowells for resonance. "
            "For field problems see [vortex flow meter troubleshooting](https://www.instrumentationblog.in/vortex-flow-meter-troubleshooting/)."),
     body_add=f'''
## Checking the Reynolds number and low flow limit

The Strouhal number only stays near 0.2 when the flow is turbulent. For water (ν ≈ 1.0 × 10⁻⁶ m²/s) at {Vv:g} m/s in the {Dp*1000:.0f} mm pipe, Re = {Vv:g} × {Dp:g} ÷ 1.0 × 10⁻⁶ = **{Re:,.0f}**, well inside the linear range. If the meter needs Re ≥ 20,000 to shed reliably, the lowest usable velocity is 20,000 × 1.0 × 10⁻⁶ ÷ {Dp:g} = **{vmin:.2f} m/s**, which is {Qmin:.2f} m³/h and a shedding frequency of only {fmin:.1f} Hz. Below that the meter cuts off to zero. A viscous liquid raises this limit in direct proportion to its kinematic viscosity.

## Approximate frequency and K-factor by meter size

At 3 m/s with St = 0.2 and a bluff body about 0.2 times the bore. Real meters differ by design, so use the stamped K-factor:

| Size | Bluff body | Frequency | Flow | Pulses per litre |
|---|---|---|---|---|
{vk_rows}
The K-factor falls roughly with the cube of the bore, so large meters give few pulses per litre and need a longer gate time for a stable reading.

## Thermowells and other immersed bodies

The same formula gives the forcing frequency on a thermowell, with d equal to the tip diameter. ASME PTC 19.3 TW compares that frequency with the well's natural frequency and requires the ratio to stay below set limits, so a short, stiff well or a smaller tip may be needed at high gas or steam velocities. A velocity collar is no longer recommended as a fix.

## Common mistakes

- **Using the pipe velocity at low Reynolds number.** Below the meter's minimum Reynolds number, shedding becomes irregular and stops, so a viscous fluid can read zero at flows the frequency formula says are measurable.
- **Ignoring blockage.** The bluff body narrows the flow area, so the velocity at the body is higher than the pipe velocity and the real K-factor differs from this estimate.
- **Mounting on a vibrating pipe.** Pump or compressor vibration near the shedding frequency can be counted as flow, even with no flow at all.
- **Too little straight pipe.** Elbows and valves upstream distort the vortex street; follow the maker's upstream and downstream run lengths.
- **Measuring two-phase flow.** Gas in liquid or liquid droplets in steam change the shedding pattern and give unreliable readings.
''',
     faq_add=[('What is the minimum flow a vortex meter can measure?',
               f'It is set by the minimum Reynolds number, often about 20,000. For water in a 100 mm pipe that is about {vmin:.2f} m/s, or {Qmin:.2f} m³/h. A smaller meter or a higher velocity lowers the cutoff in m³/h.')])

# ---------------------------------------------------------------- Pump affinity laws
Q1, H1, P1, n1, n2, d1 = 100.0, 50.0, 18.5, 1450, 1160, 250.0
P2 = P1 * (n2 / n1) ** 3
hours = 6000
save = (P1 - P2) * hours
d2t = 235.0
rt = d2t / d1
Qt, Ht, Pt = Q1 * rt, H1 * rt ** 2, P1 * rt ** 3
Htarget = 45.0
dneed = d1 * math.sqrt(Htarget / H1)
tr_rows = ''
for r in (1.0, 0.97, 0.95, 0.92, 0.90, 0.88, 0.85):
    tr_rows += f"| {d1*r:.0f} mm ({r*100:.0f}%) | {Q1*r:.1f} m³/h | {H1*r*r:.1f} m | {P1*r**3:.2f} kW |\n"
Hs = 20.0

edit('engineering/pump-affinity-laws', date=U, phrase='pump affinity laws calculator',
     intro=("The affinity laws predict how a centrifugal pump's flow, head and power change with speed or impeller diameter: flow follows the ratio, head its square and power its cube. "
            "This pump affinity laws calculator applies them for a VFD speed change or an impeller trim.\n\n"
            "Process, maintenance and energy engineers use it to estimate VFD savings, predict a trimmed duty and compare options, for example when sizing a "
            "[VFD](https://www.instrumentationblog.in/vfd-sizing-selection-guide/)."),
     body_add=f'''
## Impeller trim example

At constant speed the diameter ratio works the same way. Trimming the {d1:g} mm impeller to {d2t:g} mm (ratio {rt:.2f}):

- Flow = {Q1:g} × {rt:.2f} = **{Qt:.1f} m³/h**
- Head = {H1:g} × {rt:.2f}² = **{Ht:.1f} m**
- Power = {P1:g} × {rt:.2f}³ = **{Pt:.2f} kW**

To reach a target head of {Htarget:g} m at the same flow ratio, the diameter must be {d1:g} × √({Htarget:g} ÷ {H1:g}) = **{dneed:.1f} mm**. Trim a little less than calculated and test, because metal cannot be put back.

## Impeller trim table ({d1:g} mm, {Q1:g} m³/h, {H1:g} m, {P1:g} kW)

| Trimmed diameter | Flow | Head | Power |
|---|---|---|---|
{tr_rows}
## Energy saving with a VFD

In the speed example, power falls from {P1:g} kW to {P2:.2f} kW. Over {hours:,} running hours a year that is ({P1:g} − {P2:.2f}) × {hours:,} = **{save:,.0f} kWh** of shaft energy, before motor and VFD losses. The saving is this large only when the system is mostly friction head. If the system has, say, {Hs:g} m of static head, the pump cannot deliver any flow once its shutoff head falls below {Hs:g} m, and the real duty point must be found where the scaled pump curve crosses the system curve H = H<sub>static</sub> + kQ².

## Common mistakes

- **Applying the laws to a system with high static head.** The new duty point is not on the affinity parabola; flow falls faster than speed and savings are smaller.
- **Slowing below the minimum continuous flow.** Low flow causes recirculation, heating and vibration; check the pump's minimum flow and the motor's cooling at low speed.
- **Trimming too far.** Beyond about 10 to 15% of diameter, efficiency drops and the laws overpredict flow and head.
- **Forgetting NPSH.** Speeding a pump up raises the NPSH it requires roughly with the square of speed, which can start cavitation.
- **Using power at a different duty.** P₁ must be the shaft power at the same operating point as Q₁ and H₁, not the motor rating.
''',
     faq_add=[('How do I find the impeller diameter for a target head?',
               f'Rearrange the head law: D₂ = D₁ × √(H₂ ÷ H₁). For a {d1:g} mm impeller giving {H1:g} m, a target of {Htarget:g} m needs {dneed:.1f} mm. Flow then falls by the same diameter ratio.')])

# ---------------------------------------------------------------- FOPDT step test
du, dy, t28, t63 = 10.0, 20.0, 25.0, 40.0
K = dy / du
tau = 1.5 * (t63 - t28)
th = t63 - tau
lam = max(tau, 3 * th)
Kc = tau / (K * (lam + th))
settle = th + 4 * tau
span_eu = 200.0
fo_rows = ''
for t in (0, th, t28, t63, th + 2 * tau, th + 3 * tau, th + 5 * tau):
    y = 0 if t <= th else dy * (1 - math.exp(-(t - th) / tau))
    fo_rows += f"| {t:.1f} s | {y:.2f}% | {y/dy*100:.1f}% | {y/100*span_eu:.1f} °C |\n"

edit('engineering/fopdt-step-test', date=U, phrase='fopdt step test calculator',
     intro=("An open-loop step test, changing the controller output in manual and watching the process variable, is the standard way to model a process before tuning. "
            "This FOPDT step test calculator turns the step and the 28.3% and 63.2% times into gain, time constant and dead time.\n\n"
            "Control engineers and technicians use it before PID tuning and auto-tune checks, as described in "
            "[step-test and auto-tune methods in DCS PID controllers](https://www.instrumentationblog.in/dcs-pid-auto-tune-step-test-relay-feedback-ziegler-nichols/)."),
     body_add=f'''
## From the model to controller settings

With K = {K:g}, τ = {tau:g} s and θ = {th:g} s, lambda tuning gives a robust PI controller. Choose λ as the larger of τ and 3θ, here λ = max({tau:g}, {3*th:g}) = **{lam:g} s**:

- Kc = τ ÷ (K × (λ + θ)) = {tau:g} ÷ ({K:g} × ({lam:g} + {th:g})) = **{Kc:.3f}**
- Ti = τ = **{tau:g} s**

Because θ/τ is high, the loop is dead-time heavy and should not be tuned aggressively. The [lambda tuning calculator](/engineering/lambda-tuning/) compares this with Cohen-Coon.

## Checking the fit

The fitted model predicts PV change = K × ΔOP × (1 − e<sup>−(t − θ)/τ</sup>) after the dead time. Compare it with the recorded trend; the temperature column assumes a 0 to {span_eu:g} °C transmitter span:

| Time after step | Predicted PV change | Share of final | In °C |
|---|---|---|---|
{fo_rows}
If the recorded curve rises later and then faster than this, the process is higher order and the two-point model is only an approximation. Hold the output steady for at least θ + 4τ = **{settle:.1f} s** after the step, when the response is 98% complete.

## Running the test in practice

Put the loop in manual at a steady operating point, record the PV with fast sampling (at least 10 samples per time constant) and step the output once. Note the exact time of the step from the trend or the event log. Make the step 5 to 10% of output if the process allows, large enough to stand clear of noise and valve deadband. Repeat the step back down to check that gain and timing are similar in both directions; a big difference points to a nonlinear valve or process.

## Common mistakes

- **Timing from the start of the PV movement.** Both t28 and t63 must be measured from the output step; timing from the first PV movement loses the dead time.
- **Mixing engineering units and percent.** The gain is in % of PV span per % of output. A 40 °C change on a 0 to 200 °C span is 20%, not 40.
- **Stopping before the PV settles.** If the final value is guessed too early, the 28.3% and 63.2% levels are wrong and so are τ and θ.
- **Testing during a disturbance.** A feed or load change during the test shows up as part of the response; repeat the test.
- **Using the method on an integrating loop.** Most level loops never settle after a step, so the FOPDT model does not apply.
''',
     faq_add=[('How long should I wait after the step?',
               f'Until the PV is steady, which for a first-order process is about θ + 4τ (98% of the change). For K = 2, τ = 22.5 s and θ = 17.5 s that is {settle:.1f} s. Slow loops such as large temperature processes may need hours.')])

# ---------------------------------------------------------------- Gear ratio
z1, z2, gN1, gT1, geta = 20, 60, 1450, 50.0, 0.98
gi = z2 / z1
gN2 = gN1 / gi
gT2 = gT1 * gi * geta
Pin = gT1 * gN1 * 2 * pi / 60
Pout = gT2 * gN2 * 2 * pi / 60
i2 = 54 / 18
Nt = gN1 / (gi * i2)
Tt = gT1 * gi * i2 * geta ** 2
m = 3
dp1, dp2 = m * z1, m * z2
a = m * (z1 + z2) / 2
vp = pi * dp1 / 1000 * gN1 / 60
md_rows = ''
for mm in (1, 1.5, 2, 2.5, 3, 4, 5, 6):
    md_rows += f"| {mm:g} mm | {mm*z1:g} mm | {mm*z2:g} mm | {mm*(z1+z2)/2:g} mm | {pi*mm*z1/1000*gN1/60:.2f} m/s |\n"

edit('engineering/gear-ratio', date=U, phrase='gear ratio calculator',
     intro=("A gear pair trades speed for torque in proportion to its tooth counts: a small pinion driving a large gear slows the output and multiplies the torque. "
            "This gear ratio calculator gives the ratio, output speed and output torque after mesh losses.\n\n"
            "Mechanical designers, maintenance engineers and students use it to select gearbox stages, check a drive's torque and "
            "verify that a replacement gear set gives the speed the machine needs."),
     body_add=f'''
## Power balance check

Power in must equal power out plus the loss in the mesh, which is a good check on any result:

- Input power = {gT1:g} N·m × {gN1:,} rpm × 2π ÷ 60 = **{Pin/1000:.2f} kW**
- Output power = {gT2:g} N·m × {gN2:.1f} rpm × 2π ÷ 60 = **{Pout/1000:.2f} kW**
- Loss = {(Pin-Pout)/1000:.2f} kW, about {(1-geta)*100:.0f}%, which leaves the gearbox as heat

## Two-stage example and gear geometry

Adding a second stage of 18 : 54 (3 : 1) after the first gives an overall ratio of {gi:g} × {i2:g} = **{gi*i2:g} : 1**. The output turns at {gN1:,} ÷ {gi*i2:g} = **{Nt:.1f} rpm** with {gT1:g} × {gi*i2:g} × {geta:g}² = **{Tt:.1f} N·m**.

For spur gears the tooth size is set by the **module** m, and the pitch diameter is d = m × z. With m = {m} mm the {z1}-tooth pinion is {dp1} mm and the {z2}-tooth gear {dp2} mm across the pitch circle, the centre distance is a = m (z₁ + z₂) ÷ 2 = **{a:g} mm**, and the pitch line velocity is π × {dp1/1000:g} × {gN1:,} ÷ 60 = **{vp:.2f} m/s**.

## Pitch diameter and centre distance for {z1} : {z2} teeth

| Module | Pinion pitch diameter | Gear pitch diameter | Centre distance | Pitch line speed at {gN1:,} rpm |
|---|---|---|---|---|
{md_rows}
Two gears only mesh if they have the same module and pressure angle (usually 20°).

## Common mistakes

- **Inverting the ratio.** The ratio is driven teeth ÷ driving teeth; swapping them turns a reduction into a speed-up.
- **Applying efficiency to speed.** Losses reduce torque and power, not speed; the output speed of a gear pair is fixed by the tooth counts.
- **Assuming high efficiency for worm gears.** A worm set can be 50% efficient or less at high ratios, so the output torque is far below T₁ × i.
- **Forgetting the service factor.** Shock loads, frequent starts and long running hours need a gearbox rated above the calculated torque.
- **Meshing gears of different module or pressure angle.** They will not run together even if the tooth counts give the right ratio.
''',
     faq_add=[('How do I calculate the centre distance of spur gears?',
               f'Centre distance = module × (z₁ + z₂) ÷ 2. A {z1}-tooth pinion and {z2}-tooth gear with a {m} mm module sit {a:g} mm apart. For imperial gears use (N₁ + N₂) ÷ (2 × diametral pitch) in inches.')])

# ---------------------------------------------------------------- Rotameter correction
Qs, r1, r2, rf = 10.0, 998.0, 800.0, 8000.0
CF = lambda rf, r2, r1=998.0: math.sqrt((rf - r2) * r1 / ((rf - r1) * r2))
cf = CF(rf, r2)
want = 12.0
scale = want / cf
cf_al = CF(2700, r2)
rt_rows = ''
for nm, d in (('Stainless steel 316', 8000), ('Hastelloy C', 8890), ('Titanium', 4500), ('Aluminium', 2700), ('PTFE', 2170), ('PVDF', 1780)):
    rt_rows += f"| {nm} | {d:,} kg/m³ | {CF(d, 800):.4f} | {CF(d, 1200):.4f} |\n"
r2h = 790.0
cfh = CF(rf, r2h)

edit('engineering/rotameter-correction', date=U, phrase='rotameter correction calculator',
     intro=("A rotameter is calibrated for one fluid, usually water, and reads wrong on a liquid of different density because the float settles at a different height. "
            "This rotameter correction calculator converts the scale reading to actual flow using the float density, as covered in the [metal tube rotameter working principle](https://www.instrumentationblog.in/metal-tube-rotameter-working/).\n\n"
            "Operators and instrument technicians use it when a meter is moved to a new liquid; see also "
            "[10 factors in rotameter selection](https://www.instrumentationblog.in/rotameter-selection-10-factors/)."),
     body_add=f'''
## Setting a target flow on the scale

To deliver a required actual flow, divide by the correction factor. For {want:g} L/min of the {r2:g} kg/m³ liquid through the same meter, set the float at {want:g} ÷ {cf:.4f} = **{scale:.2f} L/min** on the water scale. The float material matters: with an aluminium float (2,700 kg/m³) the same liquid gives a factor of **{cf_al:.4f}**, a larger correction, because a light float is more sensitive to the liquid's buoyancy.

Temperature counts too. If the liquid warms and its density falls to {r2h:g} kg/m³, the factor rises to {cfh:.4f}, so the same scale reading means {(cfh/cf-1)*100:.1f}% more flow.

## Correction factor by float material

For a water-calibrated meter (998 kg/m³), measuring a light liquid of 800 kg/m³ and a heavy liquid of 1,200 kg/m³:

| Float material | Float density | Factor at 800 kg/m³ | Factor at 1,200 kg/m³ |
|---|---|---|---|
{rt_rows}
## Reading a rotameter in practice

The meter must be truly vertical, with flow upward, and the reading taken at the edge the manufacturer marks, usually the widest part of a shaped float or the centre of a ball float. Read at eye level to avoid parallax on glass tubes. On metal tube meters the float position is shown by a magnetic follower and indicator, which can also give a 4 to 20 mA output; the same density correction applies to that signal.

## Common mistakes

- **Mixing SG and kg/m³.** All three densities must be in the same unit; entering the float density in kg/m³ and the liquids as SG gives a nonsense factor.
- **Correcting a meter already scaled for the fluid.** Many meters are ordered with a scale for the actual liquid; correcting them again doubles the error.
- **Ignoring viscosity.** The density correction assumes viscosity close to the calibration fluid. Thick oils need the manufacturer's viscosity correction or a new scale.
- **Reading the wrong part of the float.** Using the top of a float that should be read at its widest edge shifts every reading by the float height.
- **Using it on pulsating flow.** A bouncing float from a reciprocating pump gives an unreliable average; add a damper or use another meter type.
''',
     faq_add=[('Which part of the rotameter float should I read?',
               'Read at the reading edge marked by the manufacturer. For most shaped floats this is the widest part (the top edge of the float body); for a ball float read the centre of the ball, at eye level.')])

# ---------------------------------------------------------------- Calibration error
Lo, Hi, X, Y, Tol = 4.0, 20.0, 12.0, 12.05, 0.0025
span = Hi - Lo
err = Y - X
ps = err / span
bar_span = 10.0
err_bar = err / span * bar_span
tolmA = Tol * span
tur_ref = tolmA / 4
pt_rows = ''
for pc in (0, 0.25, 0.5, 0.75, 1.0):
    e = Lo + pc * span
    pt_rows += f"| {pc*100:.0f}% | {pc*bar_span:.2f} bar | {e:.3f} mA | {e-tolmA:.3f} mA | {e+tolmA:.3f} mA |\n"
gb = 0.8 * tolmA

edit('engineering/calibration-error', date=U, phrase='calibration error calculator',
     intro=("Calibration compares an instrument's reading with a reference standard and decides whether the error is inside tolerance. "
            "This calibration error calculator gives the error in units, percent of span and percent of reading, as explained in [how to calculate calibration error](https://www.instrumentationblog.in/calibration-error-calculation/).\n\n"
            "Instrument technicians and quality engineers use it to record as-found and as-left results and decide on adjustment; see "
            "[as-found and as-left on calibration certificates](https://www.instrumentationblog.in/calibration-certificate-as-found-as-left/)."),
     body_add=f'''
## Converting the error to process units

If the transmitter in the example is ranged 0 to {bar_span:g} bar, the {err:.3f} mA error is {err:.3f} ÷ {span:g} × {bar_span:g} = **{err_bar:.5f} bar** ({err_bar*1000:.2f} mbar). Percent of span is the same whichever unit you use, so {ps*100:.4f}% of span is also {ps*100:.4f}% of the 0 to {bar_span:g} bar range. The tolerance of ±{Tol*100:g}% of span is ±{tolmA:.3f} mA, so the reference used to test it should be accurate to about {tolmA:.3f} ÷ 4 = **±{tur_ref:.3f} mA** or better.

## Pass band at each test point

For a 4 to 20 mA, 0 to {bar_span:g} bar transmitter with a ±{Tol*100:g}% of span tolerance:

| Input | Pressure | Expected | Lowest pass | Highest pass |
|---|---|---|---|---|
{pt_rows}
## Calibration in practice

Let the instrument and reference stabilise at the test temperature, exercise a pressure transmitter to full range once or twice, and then record the as-found readings at each point before adjusting anything. If any point fails, adjust zero and span, repeat the full run and record the as-left results. Many sites apply a **guard band**, for example adjusting whenever the error is above 80% of tolerance (here ±{gb:.3f} mA), so the instrument is unlikely to drift out before the next calibration.

## Common mistakes

- **Dividing by the reading instead of the span.** Percent of reading makes the same error look several times larger near the bottom of the scale; most tolerances are in percent of span.
- **Losing the sign.** A positive error means the instrument reads high. Keep the sign on the record so drift trends can be seen over several calibrations.
- **Adjusting before recording as-found.** Without as-found data there is no way to tell whether the process was measured correctly since the last calibration.
- **Using a reference that is too coarse.** A calibrator with uncertainty close to the tolerance cannot prove a pass or a fail.
- **Mixing units across inputs.** Range, expected and measured values must all be in mA, or all in bar; mixing them gives a meaningless result.
''',
     faq_add=[('How do I convert a mA calibration error into process units?',
               f'Divide the mA error by the 16 mA span and multiply by the process range. A 0.05 mA error on a 0 to 10 bar transmitter is 0.05 ÷ 16 × 10 = {err_bar:.5f} bar, or {err_bar*1000:.2f} mbar.'),
              ('What is a guard band in calibration?',
               f'It is a tighter adjust limit inside the tolerance, used so an instrument is reset before it drifts out. With a ±0.25% of span tolerance on 4 to 20 mA (±{tolmA:.3f} mA), an 80% guard band means adjusting any point beyond ±{gb:.3f} mA.')])

# ---------------------------------------------------------------- Weld size
s, L, F, ta = 6.0, 100.0, 50.0, 145.0
aw = 0.70710678 * s
tau_w = F * 1000 / (aw * L)
Freq = 80.0
a_need = Freq * 1000 / (ta * L)
s_need = a_need / 0.70710678
s1, s2 = 6.0, 10.0
a_un = s1 * s2 / math.sqrt(s1 ** 2 + s2 ** 2)
ec_rows = ''
for gr, fu, bw in (('S235', 360, 0.80), ('S275', 430, 0.85), ('S355', 510, 0.90)):
    fv = fu / (math.sqrt(3) * bw * 1.25)
    ec_rows += f"| {gr} | {fu} MPa | {bw:.2f} | {fv:.1f} MPa | {fv*aw/1000:.3f} kN/mm |\n"

edit('engineering/weld-size', date=U, phrase='fillet weld size calculator',
     intro=("A fillet weld carries load through its throat, the shortest distance from root to face, which for an equal-leg weld is 0.707 times the leg size. "
            "This fillet weld size calculator finds the throat, the shear stress and the load the weld can carry.\n\n"
            "Structural and mechanical engineers, fabricators and welding inspectors use it to size brackets, lugs and stiffeners, "
            "and to check that a drawing's weld callout can take the design load."),
     body_add=f'''
## Sizing a weld for a load

To find the leg needed for {Freq:g} kN on the same {L:g} mm of weld at {ta:g} MPa:

- Required throat a = {Freq:g} × 1,000 ÷ ({ta:g} × {L:g}) = **{a_need:.2f} mm**
- Required leg s = {a_need:.2f} ÷ 0.707 = **{s_need:.2f} mm**, so specify an **8 mm** fillet

If the joint is welded on both sides, each weld line counts, so two {L:g} mm runs of {s:g} mm fillet give {2*ta*aw*L/1000:.1f} kN. For an unequal-leg fillet the throat is s₁ s₂ ÷ √(s₁² + s₂²); a {s1:g} × {s2:g} mm fillet has a throat of **{a_un:.2f} mm**, only a little more than a {s1:g} mm equal-leg weld.

## Eurocode 3 simplified design strength

EN 1993-1-8 gives a design shear strength f<sub>vw,d</sub> = f<sub>u</sub> ÷ (√3 × β<sub>w</sub> × γ<sub>M2</sub>) with γ<sub>M2</sub> = 1.25. These are design values for factored loads, not allowable stresses, so do not mix them with the AWS figure above:

| Steel grade | f<sub>u</sub> | β<sub>w</sub> | f<sub>vw,d</sub> | Resistance per mm of {s:g} mm fillet |
|---|---|---|---|---|
{ec_rows}
## Inspection and practice

The leg size is checked with a fillet weld gauge after welding, and a concave weld face reduces the true throat below 0.707 × leg, so inspectors check the throat too. Effective length excludes the start and stop craters; many codes deduct about twice the leg size from each run and set a minimum length of around four times the leg. Intermittent welds carry load only over their weld lengths, not the gaps between them.

## Common mistakes

- **Using the leg as the throat.** Designing with the leg size overstates capacity by about 41%.
- **Counting the full run as effective length.** Craters at each end carry little load; deduct them, especially on short welds.
- **Ignoring eccentric loads.** A load offset from the weld group adds bending and torsion stress; the simple F ÷ (aL) check is then unsafe.
- **Mixing factored and working loads.** Allowable stresses (AWS) go with service loads; Eurocode design strengths go with factored loads.
- **Forgetting the parent metal.** The plate next to the weld can fail in shear before the weld does, so check its capacity as well.
''',
     faq_add=[('How do I calculate the throat of an unequal-leg fillet weld?',
               f'Throat = s₁ × s₂ ÷ √(s₁² + s₂²), the height of the right-angled triangle measured to its long side. A {s1:g} × {s2:g} mm fillet has a throat of {a_un:.2f} mm, compared with {0.70710678*s1:.2f} mm for a {s1:g} mm equal-leg fillet.')])

print('done slice 1')

# ======================================================================= SECTION _expand_c2.py
"""Part C expand (2026-11-16), slice 2: bending-stress, five-point-calibration, manning-equation,
lambda-tuning, ziegler-nichols-pid-tuning, shaft-diameter, gas-flow-correction, factor-of-safety,
spring-rate, lmtd. Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-16'
g = 9.80665
pi = math.pi

# ---------------------------------------------------------------- Bending stress
bM, bZ, bSy = 15.0, 194.0, 250.0
bs = bM * 1e3 / (bZ * 1e-6) / 1e6
bF = bSy / bs
# second example: simply supported flat bar with a uniform load
wL, wl, rb, rh = 10.0, 3.0, 50.0, 150.0
wM = wL * wl ** 2 / 8
rZ = rb * rh ** 2 / 6 / 1000  # cm3
rs = wM * 1e3 / (rZ * 1e-6) / 1e6
eps = bs * 1e6 / 200e9 * 1e6  # microstrain at E = 200 GPa
def zrect(b, h): return b * h ** 2 / 6 / 1000
def zround(d): return pi * d ** 3 / 32 / 1000
def ztube(D, t): d = D - 2 * t; return pi * (D ** 4 - d ** 4) / (32 * D) / 1000
bz_rows = ''
for name, form, z in (('Rectangle 50 × 100 mm (on edge)', 'b·h² ÷ 6', zrect(50, 100)),
                      ('Rectangle 100 × 50 mm (flat)', 'b·h² ÷ 6', zrect(100, 50)),
                      ('Solid round 50 mm', 'π d³ ÷ 32', zround(50)),
                      ('Solid round 80 mm', 'π d³ ÷ 32', zround(80)),
                      ('Tube 60.3 × 3.91 mm (2 in Sch 40)', 'π (D⁴ − d⁴) ÷ 32D', ztube(60.3, 3.91)),
                      ('Tube 114.3 × 6.02 mm (4 in Sch 40)', 'π (D⁴ − d⁴) ÷ 32D', ztube(114.3, 6.02))):
    bz_rows += f"| {name} | {form} | {z:.2f} cm³ | {z*1e-6*bSy*1e6/1e3:.2f} kN·m |\n"

edit('engineering/bending-stress', date=U, phrase='bending stress calculator',
     intro=("A bending moment stretches one face of a beam and compresses the other, and the stress is greatest at the outer fibres. "
            "This bending stress calculator applies σ = M ÷ Z (the same as M·y ÷ I) to find that peak stress and compares it with the yield strength.\n\n"
            "Structural and mechanical engineers use it to check beams, brackets and shafts, and test engineers use it to predict the strain that "
            "[strain gauges](https://www.instrumentationblog.in/strain-gauge-working-principle/) will read on a loaded beam."),
     body_add=f'''
## Worked example: flat bar on two supports

A {rb:g} × {rh:g} mm steel flat bar, standing on edge, spans **{wl:g} m** between two simple supports and carries a uniform load of **{wL:g} kN/m**:

- Bending moment at mid span = w L² ÷ 8 = {wL:g} × {wl:g}² ÷ 8 = **{wM:.2f} kN·m**
- Section modulus = b h² ÷ 6 = {rb:g} × {rh:g}² ÷ 6 = {rZ*1000:,.0f} mm³ = **{rZ:.1f} cm³**
- σ = {wM*1000:,.0f} N·m ÷ {rZ:.1f} × 10⁻⁶ m³ = **{rs:.1f} MPa**
- Factor of safety against 250 MPa yield = 250 ÷ {rs:.1f} = **{bSy/rs:.2f}**

Laid flat, the same bar has Z = {rh:g} × {rb:g}² ÷ 6 = {zrect(rh, rb):.1f} cm³, so the stress triples to {wM*1e3/(zrect(rh, rb)*1e-6)/1e6:.0f} MPa and the bar yields. Orientation matters as much as size.

## Section modulus of common shapes

Moment at first yield uses S<sub>y</sub> = {bSy:g} MPa:

| Section | Formula | Z | Moment at first yield |
|---|---|---|---|
{bz_rows}
## How bending stress is measured in practice

On a real structure the stress is checked with a strain gauge bonded to the outer fibre, aligned with the beam axis. In the elastic range σ = E × ε, so the IPE 200 example above at {bs:.1f} MPa on steel (E = 200 GPa) shows about **{eps:.0f} µε**. A quarter bridge picks up this strain, and a half bridge with one gauge on the top face and one on the bottom doubles the signal and cancels temperature and axial effects. Load cells of the bending beam type work on exactly this principle.

## Common mistakes

- **Mixing cm³ and mm³.** Steel tables list Z in cm³; 194 cm³ is 194,000 mm³. A factor of 1,000 error is the most common slip.
- **Using I instead of Z.** I (cm⁴) must be divided by the distance to the outer fibre before it gives stress.
- **Taking the wrong axis.** An IPE 200 has Z ≈ 194 cm³ about its strong axis but only about 28.5 cm³ about its weak axis.
- **Leaving out self-weight and point loads.** Add every load to the bending moment at the critical section, not just the main one.
- **Comparing with ultimate strength.** For ductile steel the outer fibre yielding is the usual limit; ultimate strength gives a falsely high factor of safety.
''',
     faq_add=[('How is bending stress related to strain?',
               f'In the elastic range σ = E × ε at the outer fibre. A steel beam (E = 200 GPa) stressed to {bs:.1f} MPa has a surface strain of about {eps:.0f} microstrain, which is what a strain gauge on the top or bottom face reads.')])

# ---------------------------------------------------------------- Five point calibration
fL, fH = 50.0, 250.0
fexp = [4 + 16 * p for p in (0, .25, .5, .75, 1)]
fin = [fL + p * (fH - fL) for p in (0, .25, .5, .75, 1)]
fup = [4.006, 8.012, 12.018, 16.014, 19.994]
fdn = [4.010, 8.022, 12.026, 16.020, 19.994]
f_rows = ''
worst = 0
hmax = (0, -1)
for p, i, e, u, d in zip((0, 25, 50, 75, 100), fin, fexp, fup, fdn):
    eu = (u - e) / 16 * 100; ed = (d - e) / 16 * 100; hy = abs(d - u) / 16 * 100
    worst = max(worst, abs(eu), abs(ed))
    hmax = max(hmax, (hy, p))
    f_rows += f"| {p}% | {i:g} °C | {e:.3f} mA | {u:.3f} mA | {d:.3f} mA | {eu:+.3f}% | {ed:+.3f}% | {hy:.3f}% |\n"
assert 0.1 < worst < 0.25, worst
tol_rows = ''
for t in (0.1, 0.25, 0.5, 1.0):
    tol_rows += f"| ±{t:g}% | ±{16*t/100:.3f} mA | ±{4*t/100:.3f} V | ±{10*t/100:.3f} V |\n"

edit('engineering/five-point-calibration', date=U, phrase='5-point calibration calculator',
     intro=("A 5-point check at 0, 25, 50, 75 and 100% of range is the standard way to calibrate a transmitter and reveal zero, span and linearity errors. "
            "This 5-point calibration calculator builds the table of input values and expected outputs for any range.\n\n"
            "Instrument technicians use it to prepare calibration sheets before going to the field, as in the "
            "[calibration process for a DP transmitter](https://www.instrumentationblog.in/calibration-process-differential-pressure-transmitter/)."),
     body_add=f'''
## Worked example: temperature transmitter with as-found errors

A temperature transmitter is ranged **{fL:g} to {fH:g} °C** with a 4 to 20 mA output. Entering LRV {fL:g}, URV {fH:g}, 4 and 20 gives the 25, 50 and 75% inputs of **{fin[1]:g}, {fin[2]:g} and {fin[3]:g} °C**, with expected outputs of 8, 12 and 16 mA. The technician applies each point from a dry block, upscale and then downscale. Error is (measured − expected) ÷ 16 mA × 100:

| Point | Input | Expected | Upscale | Downscale | Error up | Error down | Hysteresis |
|---|---|---|---|---|---|---|---|
{f_rows}
The worst error is **{worst:.3f}% of span** and the largest hysteresis is at {hmax[1]}%. Against a ±0.25% tolerance the transmitter passes as found; against ±0.1% it fails and needs a zero and span trim, followed by a fresh as-left record.

## Tolerance in output units

| Tolerance (% of span) | 4 to 20 mA | 1 to 5 V | 0 to 10 V |
|---|---|---|---|
{tol_rows}
## Good practice

- Choose a reference standard at least **4 times** more accurate than the tolerance being checked (a 4:1 test accuracy ratio).
- Let each point settle before reading, and approach it from one direction only. If you overshoot on the way up, go back below the point and approach it again, otherwise you hide hysteresis.
- Exercise pressure transmitters to full range two or three times before recording, so the sensor and seals settle.
- Record the as-found data before you touch anything, then the as-left data after adjustment. Trend the as-found error from one calibration to the next to set the interval.

## Common mistakes

- **Adjusting before recording as-found data.** The as-found result is what tells you whether the loop was within tolerance in service.
- **Ignoring damping.** A transmitter with several seconds of damping needs time to settle; reading too early looks like a span error.
- **Using a gauge reference on an absolute transmitter.** Atmospheric pressure then appears as a zero error of about 1.013 bar.
- **Calibrating a DP flow transmitter in flow units.** The table here is linear in DP; the square-root output is a separate check.
- **Skipping the downscale run.** Hysteresis only shows when you compare upscale and downscale readings at the same point.
''',
     faq_add=[('What test accuracy ratio do I need for calibration?',
               'A common rule is 4:1, meaning the reference is at least four times more accurate than the tolerance being checked. To verify a transmitter to ±0.25% of span, the calibrator should be good to about ±0.06% of that span or better.'),
              ('What is the difference between as-found and as-left data?',
               'As-found readings are taken before any adjustment and show how the instrument performed in service. As-left readings are taken after adjustment and show the state it was returned in. Both are recorded on the calibration sheet.')])

# ---------------------------------------------------------------- Manning equation
mn, mb, my, mS = 0.013, 2.0, 0.5, 0.001
def man(y, S=mS, n=mn, b=mb):
    A = b * y; P = b + 2 * y; R = A / P; V = R ** (2 / 3) * math.sqrt(S) / n
    return A, P, R, V, V * A
mA, mP, mR, mV, mQ = man(my)
Fr = mV / math.sqrt(g * my)
Qt = 2.0
lo, hi = 0.01, 5.0
for _ in range(80):
    mid = (lo + hi) / 2
    if man(mid)[4] < Qt: lo = mid
    else: hi = mid
yn = (lo + hi) / 2
_, _, _, Vn, _ = man(yn)
ms_rows = ''
for S in (0.0005, 0.001, 0.002, 0.005, 0.01):
    _, _, _, V, Q = man(my, S)
    ms_rows += f"| {S*100:g}% (1 in {1/S:,.0f}) | {V:.3f} m/s | {Q:.3f} m³/s | {V/math.sqrt(g*my):.2f} |\n"

edit('engineering/manning-equation', date=U, phrase='Manning equation calculator',
     intro=("The Manning equation is the standard formula for uniform flow in open channels, ditches and part-full gravity drains, linking velocity to roughness, hydraulic radius and slope. "
            "This Manning equation calculator works in SI units for a rectangular channel.\n\n"
            "Civil, drainage and wastewater engineers use it to size channels and check capacity, alongside "
            "[open channel flow measurement](https://www.instrumentationblog.in/open-channel-flow-measurement/) with a "
            "[Parshall flume](https://www.instrumentationblog.in/parshall-flume-open-channel-flow/)."),
     before='## Notes', min_words=0,
     body_add=f'''
## Worked example: normal depth for a design flow

The same {mb:g} m concrete channel (n = {mn}, slope {mS*100:g}%) must carry **{Qt:g} m³/s**. Clear the depth, enter the flow and the calculator solves for the depth at which Manning gives exactly that flow:

- Normal depth y = **{yn:.3f} m**
- Area = {mb:g} × {yn:.3f} = {mb*yn:.3f} m², velocity = {Qt:g} ÷ {mb*yn:.3f} = **{Vn:.3f} m/s**
- Check the default case too: Froude number Fr = V ÷ √(g y) = {mV:.3f} ÷ √(9.80665 × {my:g}) = **{Fr:.2f}**, so the flow is subcritical (Fr below 1) and calm.

## Effect of slope (2 m wide, 0.5 m deep, n = 0.013)

| Slope | Velocity | Flow | Froude number |
|---|---|---|---|
{ms_rows}
Velocity rises with the square root of slope, so doubling the slope gives only 41% more flow. Steep channels quickly become supercritical (Fr above 1), with standing waves and hydraulic jumps where the slope eases.

## How it is used in practice

Manning is a design and estimating tool. Engineers use it to size storm drains, irrigation canals and plant effluent channels, and to estimate flow from a measured depth where no flume exists (the slope-area method). For flow that must be measured accurately, a primary device such as a weir or Parshall flume with an ultrasonic or radar level sensor is installed, because a flume's depth to flow relation is fixed by its geometry and does not depend on an estimated n.
''')
edit('engineering/manning-equation', date=U,
     body_add='''
## Common mistakes

- **Entering slope as a whole number.** A fall of 1 m in 1,000 m is 0.1%, or 0.001 as a fraction. Entering 0.1 as a fraction makes the flow ten times too high.
- **Using the US form with metric data.** The 1.486 factor belongs only with feet; mixing systems gives a 49% error.
- **Choosing n for a new surface.** Weed growth, sediment and joint deterioration raise n over time; design with a value that reflects the channel as it will be maintained.
- **Applying Manning near structures.** Flow approaching a weir, gate or bend is not uniform, so the depth there is not the normal depth.
- **Ignoring the minimum velocity.** Channels running below about 0.6 m/s at normal flow tend to collect silt, which changes both the area and the roughness.
''',
     faq_add=[('What is the Froude number and why check it?',
               f'Fr = V ÷ √(g y) compares flow velocity with the speed of a surface wave. Below 1 the flow is subcritical and calm; above 1 it is supercritical and fast. The default channel has Fr = {Fr:.2f}. Designs close to Fr = 1 are avoided because the surface becomes unstable and wavy.'),
              ('What velocity keeps a channel from silting up?',
               'A common design rule is a self-cleansing velocity of at least about 0.6 to 0.9 m/s at normal flow for sewers and storm drains. Unlined earth channels also have an upper limit, often around 0.6 to 1.0 m/s, above which the bed starts to erode.')])

# ---------------------------------------------------------------- Lambda tuning
lK, lt, lth, ll = 2.0, 60.0, 10.0, 30.0
lKc = lt / (lK * (ll + lth)); lTi = lt
lKcc = (1 / lK) * (lt / lth) * (0.9 + lth / (12 * lt))
lTicc = lth * (30 + 3 * lth / lt) / (9 + 20 * lth / lt)
# integrating process (level): Kc = (2 lam + th) / (Ki (lam + th)^2), Ti = 2 lam + th
Ki, ith = 0.01, 20.0
li_rows = ''
for lam in (100, 200, 300, 600, 900):
    kc = (2 * lam + ith) / (Ki * (lam + ith) ** 2); ti = 2 * lam + ith
    li_rows += f"| {lam} s | {kc:.2f} | {100/kc:.0f}% | {ti:.0f} s ({ti/60:.1f} min) |\n"
lam_i = 300.0
kci = (2 * lam_i + ith) / (Ki * (lam_i + ith) ** 2); tii = 2 * lam_i + ith

edit('engineering/lambda-tuning', date=U, phrase='lambda tuning calculator',
     intro=("Lambda tuning sets a PI controller so the closed loop responds like a first order lag with a time constant λ that you choose, fast or gentle, with no overshoot. "
            "This lambda tuning calculator uses process gain, time constant and dead time from a step test and compares the result with Cohen-Coon.\n\n"
            "Control engineers use it to tune flow, pressure and temperature loops predictably, as covered in "
            "[PID controller tuning parameters](https://www.instrumentationblog.in/pid-controller-tuning-parameters/) and "
            "[how to tune a PID controller](https://www.instrumentationblog.in/how-to-tune-a-pid-controller/)."),
     body_add=f'''
## Worked example: entering the settings in a controller

For the default process (K = {lK:g}, τ = {lt:g} s, θ = {lth:g} s) and λ = {ll:g} s the calculator gives K<sub>c</sub> = **{lKc:.3f}** and T<sub>i</sub> = **{lTi:g} s**. Controllers use different units, so convert before typing:

- Proportional band = 100 ÷ {lKc:.3f} = **{100/lKc:.0f}%**
- Integral time = {lTi:g} s = **{lTi/60:g} min per repeat**, or **{60/lTi:g} repeat per minute**
- Expected response: after a set point step, the PV starts to move after the {lth:g} s dead time and reaches 63% of the change about λ + θ = **{ll+lth:g} s** after the step, with no overshoot.

Cohen-Coon for the same process gives K<sub>c</sub> = {lKcc:.3f} and T<sub>i</sub> = {lTicc:.1f} s, a far more aggressive loop.

## Integrating processes such as tank level

A level loop has no steady state gain; instead the PV ramps at a rate K<sub>i</sub> (% per second for each % of output). The integrating lambda rule, with λ as the arrest time, is:

<p class="formula">K<sub>c</sub> = (2λ + θ) ÷ [K<sub>i</sub> (λ + θ)²] &nbsp;·&nbsp; T<sub>i</sub> = 2λ + θ</p>

For a tank with K<sub>i</sub> = {Ki:g} %/s per % and θ = {ith:g} s:

| Arrest time λ | K<sub>c</sub> | PB | T<sub>i</sub> |
|---|---|---|---|
{li_rows}
A surge tank is tuned slowly (large λ) so the outlet flow stays smooth; a reactor level that must stay tight uses a short λ. With λ = {lam_i:g} s the settings are K<sub>c</sub> = {kci:.2f} and T<sub>i</sub> = {tii:.0f} s.

## Common mistakes

- **Using K in engineering units.** K must be % of PV span per % of output. A gain of 4 °C per % output on a 0 to 200 °C span is 2% per %.
- **Mixing integral time units.** Typing 60 into a controller that expects minutes per repeat sets T<sub>i</sub> to an hour.
- **Choosing λ shorter than the dead time.** The loop then loses robustness quickly; λ of at least 3θ is a safer start.
- **Applying the self-regulating rule to a level loop.** Integrating processes need the separate rule above.
- **Testing once at one operating point.** Valve characteristics change K across the range, so step test at low and high loads and tune for the worst case.
''',
     faq_add=[('How do I tune a level loop with lambda tuning?',
               'Use the integrating rule: Kc = (2λ + θ) ÷ (Ki (λ + θ)²) and Ti = 2λ + θ, where Ki is the ramp rate of the level in % per second per % of output and λ is the arrest time you want after a disturbance.'),
              ('How do I check that the loop responds as designed?',
               f'Make a small set point step in automatic. The PV should start to move after the dead time, reach about 63% of the step at λ + θ (here {ll+lth:g} s) and settle without overshoot. A faster or oscillating response means the process gain or dead time was underestimated.')])

# ---------------------------------------------------------------- Ziegler-Nichols
zKu, zPu = 2.0, 60.0
rd, ra = 5.0, 3.2
rKu = 4 * rd / (pi * ra)
zKc, zTi, zTd = 0.6 * zKu, zPu / 2, zPu / 8
x = 1 - 4 * zTd / zTi
sKc = zKc / 2 * (1 + math.sqrt(x)); sTi = zTi / 2 * (1 + math.sqrt(x)); sTd = zTi / 2 * (1 - math.sqrt(x))
zr_rows = ''
for name, a, b, c in (('Classic PID', 0.6, 2.0, 8.0), ('Pessen integral rule', 0.7, 2.5, 1 / 0.15),
                      ('Some overshoot', 0.33, 2.0, 3.0), ('No overshoot', 0.2, 2.0, 3.0)):
    kc = a * zKu
    zr_rows += f"| {name} | {a:g} K<sub>u</sub> | {kc:.3f} | {100/kc:.0f}% | {zPu/b:.1f} s | {zPu/c:.1f} s |\n"

edit('engineering/ziegler-nichols-pid-tuning', date=U, phrase='Ziegler-Nichols PID tuning calculator',
     intro=("The Ziegler-Nichols closed loop method finds the gain at which a loop just oscillates steadily (Ku) and the period of that oscillation (Pu), then sets the controller from simple ratios. "
            "This Ziegler-Nichols PID tuning calculator gives P, PI and PID settings.\n\n"
            "Control and commissioning engineers use it as a quick first tuning, as in the [PID controller tuning guide](https://www.instrumentationblog.in/pid-controller-tuning-guide/) and "
            "[step-test, relay and Ziegler-Nichols auto-tuning in a DCS](https://www.instrumentationblog.in/dcs-pid-auto-tune-step-test-relay-feedback-ziegler-nichols/)."),
     body_add=f'''
## Worked example: from a relay test to PID settings

Driving a loop to steady oscillation with a P-only controller is risky, so many DCS auto-tuners use a **relay test** instead: the output is switched ±d around its working value and the PV settles into a limit cycle of amplitude a. The describing function gives the ultimate gain:

<p class="formula">K<sub>u</sub> = 4d ÷ (π a)</p>

With a relay step of d = ±{rd:g}% and a measured PV amplitude of a = {ra:g}% (peak), K<sub>u</sub> = 4 × {rd:g} ÷ (π × {ra:g}) = **{rKu:.3f}**, and the period of the cycle is P<sub>u</sub>. Taking the calculator defaults K<sub>u</sub> = {zKu:g} and P<sub>u</sub> = {zPu:g} s, the classic PID settings are:

- K<sub>c</sub> = 0.6 × {zKu:g} = **{zKc:g}** (PB {100/zKc:.0f}%)
- T<sub>i</sub> = {zPu:g} ÷ 2 = **{zTi:g} s** ({zTi/60:g} min, or {60/zTi:g} repeats per minute)
- T<sub>d</sub> = {zPu:g} ÷ 8 = **{zTd:g} s** ({zTd/60:g} min)

## Settings for a series (interacting) PID

Many controllers use the series form. The classic rule has T<sub>i</sub> = 4 T<sub>d</sub> exactly, which is the limit for converting ideal settings to series ones:

<p class="formula">K<sub>c</sub>′ = (K<sub>c</sub>/2)(1 + √(1 − 4T<sub>d</sub>/T<sub>i</sub>)) &nbsp;·&nbsp; T<sub>i</sub>′ = (T<sub>i</sub>/2)(1 + √…) &nbsp;·&nbsp; T<sub>d</sub>′ = (T<sub>i</sub>/2)(1 − √…)</p>

For the example the root is zero, so the series settings are K<sub>c</sub>′ = **{sKc:g}**, T<sub>i</sub>′ = **{sTi:g} s** and T<sub>d</sub>′ = **{sTd:g} s**. Typing the ideal values into a series controller gives a different, more aggressive loop.

## Variations on the closed loop rules (K<sub>u</sub> = {zKu:g}, P<sub>u</sub> = {zPu:g} s)

| Rule | K<sub>c</sub> rule | K<sub>c</sub> | PB | T<sub>i</sub> | T<sub>d</sub> |
|---|---|---|---|---|---|
{zr_rows}
## Common mistakes

- **Leaving integral action on during the test.** Ku and Pu must come from a proportional-only loop or a relay test; integral action shortens the period.
- **Testing with a saturating valve.** If the output hits 0 or 100% during the oscillation, the measured Ku is wrong.
- **Ignoring the controller form.** Ideal, series and parallel PID forms need different numbers for the same response.
- **Using derivative on a noisy PV.** Flow and liquid pressure loops are noisy; use PI there and keep derivative for slow temperature loops.
- **Keeping the settings without a check.** Ziegler-Nichols aims for quarter amplitude decay; most process loops need the gain reduced after a set point test.
''',
     faq_add=[('What is the relay auto-tune method?',
               f'The controller output is switched up and down by a fixed amount d around its normal value, which makes the PV cycle at the ultimate period. The ultimate gain is Ku = 4d ÷ (π a), where a is the PV amplitude. A ±{rd:g}% relay giving a {ra:g}% PV amplitude means Ku = {rKu:.2f}.'),
              ('Do Ziegler-Nichols settings work in a series PID?',
               f'Yes, after conversion. Because the classic rule has Ti = 4 Td, the series equivalents are Kc = 0.3 Ku, Ti = Td = Pu ÷ 4. For Ku = {zKu:g} and Pu = {zPu:g} s that is a gain of {sKc:g} with Ti and Td both {sTi:g} s.')])

# ---------------------------------------------------------------- Shaft diameter
sP, sN, stau = 15.0, 1450.0, 40.0
sT = sP * 1e3 / (2 * pi * sN / 60)
sd = (16 * sT / (pi * stau * 1e6)) ** (1 / 3) * 1000
sM = 60.0
sTe = math.sqrt(sM ** 2 + sT ** 2)
sde = (16 * sTe / (pi * stau * 1e6)) ** (1 / 3) * 1000
kr = 0.6
sdo = (16 * sT / (pi * stau * 1e6 * (1 - kr ** 4))) ** (1 / 3) * 1000
sdi = kr * sdo
mass_ratio = (sdo ** 2 - sdi ** 2) / sd ** 2
Gs = 79.3e9; Ls = 1.0; ds = 0.025
Js = pi * ds ** 4 / 32
twist = sT * Ls / (Gs * Js) * 180 / pi
sc_rows = ''
for d in (20, 25, 30, 35, 40, 50, 60, 80):
    T = stau * 1e6 * pi * (d / 1000) ** 3 / 16
    sc_rows += f"| {d} mm | {T:,.0f} N·m | {T*2*pi*1450/60/1000:,.1f} kW | {T*2*pi*960/60/1000:,.1f} kW |\n"

edit('engineering/shaft-diameter', date=U, phrase='shaft diameter calculator',
     intro=("A rotating shaft must carry its torque without the torsional shear stress at its surface exceeding a safe limit. "
            "This shaft diameter calculator converts power and speed into torque and sizes a solid round shaft from τ = 16T ÷ (πd³), using an allowable shear stress that already includes your margin.\n\n"
            "Mechanical and maintenance engineers use it to size pump, fan and gearbox shafts, check couplings and confirm that a replacement shaft is strong enough."),
     body_add=f'''
## Worked example: adding bending from a belt pulley

The {sP:g} kW, {sN:,.0f} rpm drive above gives T = **{sT:.2f} N·m** and a pure torsion diameter of **{sd:.1f} mm**. If an overhung pulley also puts a bending moment of {sM:g} N·m on the shaft, use the equivalent torque:

- T<sub>e</sub> = √(M² + T²) = √({sM:g}² + {sT:.2f}²) = **{sTe:.1f} N·m**
- d = ∛(16 × {sTe:.1f} ÷ (π × {stau:g} × 10⁶)) = **{sde:.1f} mm**, so a 25 mm shaft still works but with less margin

Enter T<sub>e</sub> as the torque (or the matching power) to size a shaft for combined loading.

## Hollow shafts and twist

A hollow shaft with bore = {kr:g} × outside diameter carries the same torque with d<sub>o</sub> = ∛(16T ÷ (πτ(1 − {kr:g}⁴))) = **{sdo:.1f} mm** outside and {sdi:.1f} mm bore. It is only {sdo/sd*100-100:.0f}% larger in diameter but uses **{mass_ratio*100:.0f}%** of the material of the solid shaft.

Stiffness can govern instead of strength. A {ds*1000:g} mm solid steel shaft (G = 79.3 GPa) carrying {sT:.1f} N·m twists by θ = T L ÷ (G J) = **{twist:.2f}° per metre**, against a common machinery limit of 0.25° per metre, so a long line shaft would need to be larger than the stress check suggests.

## Torque and power capacity of solid shafts at τ = {stau:g} MPa

| Diameter | Torque capacity | Power at 1450 rpm | Power at 960 rpm |
|---|---|---|---|
{sc_rows}
## Common mistakes

- **Using rpm as angular velocity.** Torque is P ÷ ω with ω in rad/s; ω = 2πN ÷ 60.
- **Sizing on average power.** Use the maximum torque, including motor starting torque and any service factor for shock loads.
- **Entering yield strength as the allowable.** The allowable shear stress must already include the safety margin and keyway allowance.
- **Forgetting bending.** Pulleys, sprockets and gears on the shaft add bending that often exceeds the torsion.
- **Not rounding up.** Choose the next standard size above the result, then check that the keyway and bearing seats still leave enough section.
''',
     faq_add=[('How much lighter is a hollow shaft for the same torque?',
               f'With a bore of 0.6 times the outside diameter, the outside diameter grows by only about {sdo/sd*100-100:.0f}% but the cross section, and so the weight, drops to about {mass_ratio*100:.0f}% of a solid shaft. Material near the centre carries little torsional stress.'),
              ('How do I check shaft twist?',
               f'Use θ = T L ÷ (G J) with J = π d⁴ ÷ 32. A 25 mm steel shaft carrying {sT:.1f} N·m twists about {twist:.2f}° per metre. Many machinery guidelines limit twist to about 0.25° per metre.')])

# ---------------------------------------------------------------- Gas flow correction
gQa, gPg, gT, gTn = 100.0, 5.0, 30.0, 273.15
gPa = gPg * 1e5 + 101325
gk = gPa / 101325 * gTn / (gT + 273.15)
gQn = gQa * gk
gZ = 0.985
gQnz = gQn / gZ
nm_to_sm = 288.15 / 273.15
def patm(h): return 101325 * (1 - 2.25577e-5 * h) ** 5.25588
alt_rows = ''
for h in (0, 500, 1000, 1500, 2000, 3000):
    pa = patm(h)
    k_true = (gPg * 1e5 + pa) / 101325 * gTn / (gT + 273.15)
    alt_rows += f"| {h:,} m | {pa/1e5:.4f} bar(a) | {k_true:.4f} | {gQa*k_true:.1f} Nm³/h | {(gk/k_true-1)*100:+.2f}% |\n"

edit('engineering/gas-flow-correction', date=U, phrase='gas flow correction calculator',
     intro=("Gas volume changes with pressure and temperature, so the same mass of gas can occupy very different volumes. "
            "This gas flow correction calculator converts actual flow at line conditions to normal or standard flow, as explained in "
            "[actual flow vs standard flow vs normal flow](https://www.instrumentationblog.in/actual-flow-standard-flow-normal-flow/).\n\n"
            "Instrument, process and utility engineers use it to compare meter readings, compressor ratings and gas consumption on one basis, "
            "and to set up pressure and temperature compensation in flow computers."),
     body_add=f'''
## Worked example

A vortex meter on a compressed gas line reads **{gQa:g} m³/h** at **{gPg:g} bar(g)** and **{gT:g} °C**. Converting to normal conditions (0 °C, 1.01325 bar(a)):

- Absolute pressure = {gPg:g} + 1.01325 = **{gPa/1e5:.5f} bar(a)**
- Absolute temperature = {gT:g} + 273.15 = **{gT+273.15:.2f} K**
- Correction factor = ({gPa/1e5:.5f} ÷ 1.01325) × (273.15 ÷ {gT+273.15:.2f}) = **{gk:.4f}**
- Normal flow = {gQa:g} × {gk:.4f} = **{gQn:.1f} Nm³/h**

If the gas compressibility at line conditions is Z = {gZ} (and 1 at reference conditions), divide by Z: {gQn:.1f} ÷ {gZ} = **{gQnz:.1f} Nm³/h**, a {(1/gZ-1)*100:.1f}% correction that matters for billing.

## Effect of site altitude on the correction

The calculator adds standard atmospheric pressure to the gauge reading. At altitude the real atmosphere is lower, so the true absolute pressure is lower too. For the example ({gPg:g} bar(g), {gT:g} °C, {gQa:g} m³/h actual):

| Site altitude | Local atmosphere | True factor | True normal flow | Error using 1.01325 bar |
|---|---|---|---|---|
{alt_rows}
At high altitude, enter the gauge pressure plus the local atmosphere minus 1.01325 bar, or use an absolute pressure transmitter for compensation.

## How compensation is done in practice

A flow computer or DCS block takes the meter's actual flow, a pressure transmitter (preferably absolute) and a temperature sensor, and calculates normal flow every scan with the formula above, often with a Z factor from AGA 8 or a fixed value for air. Pressure and temperature should be measured close to the meter: pressure at the meter body and temperature a few diameters downstream, so the sensor does not disturb the flow profile.

## Common mistakes

- **Using gauge pressure in the ratio.** The formula needs absolute pressures; 5 bar(g) is about 6.01 bar(a).
- **Using °C instead of kelvin.** 30 °C ÷ 0 °C has no meaning; 303.15 K ÷ 273.15 K does.
- **Mixing normal and standard.** One Nm³ (0 °C) equals {nm_to_sm:.4f} Sm³ at 15 °C, a {(nm_to_sm-1)*100:.1f}% difference that often appears in contract disputes.
- **Applying the correction to a mass flow meter.** Coriolis and thermal mass meters already measure mass or normal flow; correcting again doubles the effect.
- **Leaving out Z at high pressure.** Natural gas at 50 bar can deviate from ideal behaviour by several percent.
''',
     faq_add=[('How do I convert Nm³/h to Sm³/h?',
               f'Both are at 1.01325 bar(a), so only the temperature differs. Multiply Nm³/h (0 °C) by 288.15 ÷ 273.15 = {nm_to_sm:.4f} to get Sm³/h at 15 °C, or by 293.15 ÷ 273.15 = {293.15/273.15:.4f} for 20 °C.'),
              ('How does altitude affect gas flow correction?',
               f'The local atmosphere falls with altitude, about {patm(1000)/1e5:.3f} bar(a) at 1,000 m. Adding 1.01325 bar to a gauge reading there overstates the absolute pressure and the normal flow; at 5 bar(g) the error is about {(gk/((gPg*1e5+patm(1000))/101325*gTn/(gT+273.15))-1)*100:.1f}%.')])

# ---------------------------------------------------------------- Factor of safety
fS, fs, fnr = 250.0, 100.0, 2.0
rd_, rF, rSy = 20.0, 30.0, 235.0
rA = pi * (rd_ / 1000) ** 2 / 4
rs_ = rF * 1e3 / rA / 1e6
rn = rSy / rs_
dmin = math.sqrt(4 * rF * 1e3 / (pi * rSy * 1e6 / fnr)) * 1000
# Eurocode style partial factors
Gk, Qk = 10.0, 20.0
Ed = 1.35 * Gk + 1.5 * Qk
eff = Ed / (Gk + Qk)
asme_s = min(485 / 3.5, 260 * 2 / 3)

edit('engineering/factor-of-safety', date=U, phrase='factor of safety calculator',
     intro=("A factor of safety tells you how many times stronger a part is than it needs to be for the load it carries. "
            "This factor of safety calculator divides the material strength by the working stress, gives the margin of safety and finds the allowable stress for the factor you need.\n\n"
            "Mechanical, structural and maintenance engineers use it to check brackets, rods, lifting points and machine parts against a design code or company standard."),
     body_add=f'''
## Worked example: a rod in tension

A {rd_:g} mm diameter S235 steel rod (yield {rSy:g} MPa) hangs a load of **{rF:g} kN**. The required factor of safety is {fnr:g}:

- Area = π × {rd_:g}² ÷ 4 = **{rA*1e6:.1f} mm²**
- Working stress = {rF*1000:,.0f} N ÷ {rA*1e6:.1f} mm² = **{rs_:.1f} MPa**
- Factor of safety = {rSy:g} ÷ {rs_:.1f} = **{rn:.2f}**, margin of safety **{(rn-1)*100:.0f}%**
- Smallest rod for FoS {fnr:g}: allowable stress {rSy/fnr:.1f} MPa, so d = √(4F ÷ (π σ<sub>allow</sub>)) = **{dmin:.1f} mm**

## Typical design factors by application

| Application | Typical factor | Basis |
|---|---|---|
| Aircraft structure | 1.5 | Ultimate load ÷ limit load |
| Structural steel (allowable stress design) | about 1.67 | Yield |
| Pressure vessels, ASME VIII Div. 1 | 3.5 on ultimate, 1.5 on yield | Lower allowable governs |
| General machine parts, known loads | 2 to 3 | Yield |
| Chain slings, grade 80 | 4 | Breaking load ÷ working load limit |
| Wire rope slings | 5 | Breaking load ÷ working load limit |
| Brittle materials, shock loads | 4 to 8 | Ultimate |

For example, a pressure vessel steel with 485 MPa ultimate and 260 MPa yield gets an allowable of min(485 ÷ 3.5, 260 × 2/3) = **{asme_s:.1f} MPa**.

## Partial factors in limit state design

Modern structural codes split the safety factor between loads and materials. In Eurocode the design load is 1.35 × permanent + 1.5 × variable. For {Gk:g} kN permanent and {Qk:g} kN variable load, the design load is 1.35 × {Gk:g} + 1.5 × {Qk:g} = **{Ed:.1f} kN**, an overall factor of **{eff:.2f}** on the actual load, while steel uses a material factor of 1.0 on yield. The effective factor of safety therefore depends on the mix of loads.

## Common mistakes

- **Applying the factor twice.** If the allowable stress from a code already includes a safety factor, comparing it with the working stress again with another factor of 2 is overly conservative.
- **Ignoring stress concentrations.** Holes, threads and sharp corners raise the local stress by 2 to 3 times; use the peak stress, not the nominal one.
- **Using static strength for fatigue loads.** A part with FoS 3 on yield can still fail by fatigue under millions of cycles.
- **Mixing yield and ultimate.** State which strength you used; FoS 2 on ultimate can be close to FoS 1.2 on yield for some steels.
- **Forgetting dynamic and shock loads.** A load dropped or started suddenly can double the stress compared with the same load applied slowly.
''',
     faq_add=[('Is a factor of safety of 1 enough?',
               'No. A factor of 1 means the part reaches its strength limit under the working load, so any extra load, material variation or wear causes failure. Even aircraft, where weight is critical, use at least 1.5 on ultimate load.'),
              ('What is the difference between a safety factor and a load factor?',
               f'A safety factor is applied once, to the strength. Load factors in limit state design multiply the loads instead (1.35 for permanent and 1.5 for variable load in Eurocode), and a separate material factor reduces the strength. For {Gk:g} kN permanent plus {Qk:g} kN variable load the combined load factor is {eff:.2f}.')])

# ---------------------------------------------------------------- Spring rate
kd, kD, kn, kG, kF = 2.0, 20.0, 10.0, 79300.0, 20.0
kk = kG * 1e6 * (kd / 1000) ** 4 / (8 * (kD / 1000) ** 3 * kn) / 1000
kx = kF / kk
kC = kD / kd
kKw = (4 * kC - 1) / (4 * kC - 4) + 0.615 / kC
ktau = kKw * 8 * kF * (kD / 1000) / (pi * (kd / 1000) ** 3) / 1e6
ntot = kn + 2
Hs = ntot * kd
L0 = 50.0
xs = L0 - Hs
Fs = kk * xs
taus = kKw * 8 * Fs * (kD / 1000) / (pi * (kd / 1000) ** 3) / 1e6
slender = L0 / kD
# measured rate from two load points
x1, F1, x2, F2 = 5.0, 9.8, 15.0, 29.6
km = (F2 - F1) / (x2 - x1)
km_err = (km / kk - 1) * 100
mat_rows = ''
for name, G in (('Music wire (ASTM A228)', 79300), ('Oil tempered or chrome silicon', 77200), ('Stainless 302 / 304', 69000),
                ('Beryllium copper', 48300), ('Phosphor bronze', 41400)):
    k = G * 1e6 * (kd / 1000) ** 4 / (8 * (kD / 1000) ** 3 * kn) / 1000
    mat_rows += f"| {name} | {G:,} MPa | {k:.3f} N/mm | {kF/k:.2f} mm |\n"

edit('engineering/spring-rate', date=U, phrase='spring rate calculator',
     intro=("The stiffness of a coil spring comes from twisting its wire, so it depends strongly on the wire diameter and the coil diameter. "
            "This spring rate calculator uses k = G d⁴ ÷ (8 D³ n) for a helical compression or extension spring, then finds the deflection under load and the Wahl corrected wire stress.\n\n"
            "Mechanical designers use it to choose springs for valves, actuators and machines, and maintenance teams use it to check a replacement spring before fitting it."),
     body_add=f'''
## Worked example: checking the spring at solid height

Take the default spring (d = {kd:g} mm, D = {kD:g} mm, {kn:g} active coils, music wire) with squared and ground ends and a free length of **{L0:g} mm**:

- Rate k = **{kk:.3f} N/mm**, so the {kF:g} N load compresses it **{kx:.2f} mm**
- Total coils = {kn:g} + 2 = {ntot:g}, solid height ≈ {ntot:g} × {kd:g} = **{Hs:g} mm**
- Travel to solid = {L0:g} − {Hs:g} = {xs:g} mm, needing F = {kk:.3f} × {xs:g} = **{Fs:.1f} N**
- Wire stress at solid = {kKw:.4f} × 8 × {Fs:.1f} × {kD/1000:g} ÷ (π × {kd/1000:g}³) = **{taus:.0f} MPa**

Music wire of this size has a tensile strength of roughly 2,000 MPa, so {taus:.0f} MPa at solid is within the usual static limit of about 45% of tensile strength and the spring will not take a permanent set if it is closed fully. The slenderness L<sub>0</sub> ÷ D = {slender:.1f} is low enough that buckling is not a concern (it becomes one above about 4 with fixed ends).

## Rate for the same geometry in other materials

| Wire material | Shear modulus G | Rate k | Deflection at {kF:g} N |
|---|---|---|---|
{mat_rows}
## How spring rate is measured

A spring tester compresses the spring and records load against deflection. Because the first and last coils seat unevenly, the rate is taken between two points in the middle of the travel, typically 20% and 80% of the usable deflection: k = (F₂ − F₁) ÷ (x₂ − x₁). For example, {F1:g} N at {x1:g} mm and {F2:g} N at {x2:g} mm give k = ({F2:g} − {F1:g}) ÷ ({x2:g} − {x1:g}) = **{km:.2f} N/mm**, which is {km_err:+.1f}% from the calculated {kk:.3f} N/mm and within a typical ±10% commercial tolerance.

## Common mistakes

- **Using the outside diameter as D.** The formula needs the mean coil diameter (outside diameter minus wire diameter). Using OD = {kD+kd:g} mm here would give a rate {(1-(kD/(kD+kd))**3)*100:.0f}% too low.
- **Counting all coils as active.** Closed end coils do not deflect; with squared ends use total coils minus 2.
- **Entering Young's modulus instead of shear modulus.** E for steel is about 200 GPa, more than twice G, which would double the calculated rate.
- **Ignoring solid height.** If the installed travel closes the spring fully, the stress at solid may exceed the wire's limit.
- **Small wire tolerances.** Because k depends on d⁴, a 2% oversize wire makes the spring about 8% stiffer.
''',
     faq_add=[('How do I measure the rate of a spring?',
               f'Compress it on a spring tester and read the load at two deflections in the middle of the travel, then divide the load difference by the deflection difference. {F1:g} N at {x1:g} mm and {F2:g} N at {x2:g} mm gives {km:.2f} N/mm.')])

# ---------------------------------------------------------------- LMTD
Thi, Tho, Tci, Tco, LU, LQ = 150.0, 90.0, 30.0, 70.0, 500.0, 250.0
d1, d2 = Thi - Tco, Tho - Tci
LM = (d1 - d2) / math.log(d1 / d2)
LA = LQ * 1e3 / (LU * LM)
cpw, cpo = 4.18, 2.1
mw = LQ / (cpw * (Tco - Tci)); mo = LQ / (cpo * (Thi - Tho))
def F12(R, P):
    s = math.sqrt(R * R + 1)
    num = s * math.log((1 - P) / (1 - R * P))
    den = (R - 1) * math.log((2 - P * (R + 1 - s)) / (2 - P * (R + 1 + s)))
    return num / den
R0 = (Thi - Tho) / (Tco - Tci); P0 = (Tco - Tci) / (Thi - Tci)
F0 = F12(R0, P0)
AF = LQ * 1e3 / (LU * F0 * LM)
f_rows = ''
for P in (0.1, 0.2, 0.3, 0.333, 0.4, 0.45, 0.5):
    try:
        f = F12(R0, P); fs = f'{f:.3f}' if f > 0 else 'not possible'
    except ValueError:
        fs = 'not possible'
    f_rows += f"| {P:g} | {fs} |\n"
# fouling check: same exchanger later only reaches Tco2
Tco2 = 64.0
Q2 = mw * cpw * (Tco2 - Tci)
Tho2 = Thi - Q2 / (mo * cpo)
d1b, d2b = Thi - Tco2, Tho2 - Tci
LM2 = (d1b - d2b) / math.log(d1b / d2b)
U2 = Q2 * 1e3 / (LA * LM2)
Rf = 1 / U2 - 1 / LU

edit('engineering/lmtd', date=U, phrase='LMTD calculator',
     intro=("The log mean temperature difference is the true average driving force for heat transfer between two fluids in a heat exchanger. "
            "This LMTD calculator finds it from the four terminal temperatures for counterflow or parallel flow, then sizes the exchanger with Q = U·A·LMTD.\n\n"
            "Process and HVAC engineers use it to size and rate [types of heat exchangers](https://www.instrumentationblog.in/types-of-heat-exchangers/), "
            "including how a [plate heat exchanger works](https://www.instrumentationblog.in/plate-heat-exchanger-working-principle/)."),
     body_add=f'''
## Checking the duty from the fluid flows

The {LQ:g} kW duty in the worked example must match both streams, Q = ṁ c<sub>p</sub> ΔT:

- Water, c<sub>p</sub> = {cpw} kJ/kg·K, heated {Tco-Tci:g} K: ṁ = {LQ:g} ÷ ({cpw} × {Tco-Tci:g}) = **{mw:.3f} kg/s** ({mw*3.6:.2f} t/h)
- Hot oil, c<sub>p</sub> = {cpo} kJ/kg·K, cooled {Thi-Tho:g} K: ṁ = {LQ:g} ÷ ({cpo} × {Thi-Tho:g}) = **{mo:.3f} kg/s** ({mo*3.6:.2f} t/h)

## Shell and tube correction factor (1 shell pass, 2 or more tube passes)

For a 1-2 exchanger the counterflow LMTD is multiplied by F, which depends on R = (T<sub>hi</sub> − T<sub>ho</sub>) ÷ (T<sub>co</sub> − T<sub>ci</sub>) and P = (T<sub>co</sub> − T<sub>ci</sub>) ÷ (T<sub>hi</sub> − T<sub>ci</sub>). For the example R = {R0:.2f} and P = {P0:.3f}, giving **F = {F0:.3f}** and a required area of {LQ*1e3:,.0f} ÷ ({LU:g} × {F0:.3f} × {LM:.2f}) = **{AF:.2f} m²** instead of {LA:.2f} m² in pure counterflow.

| P (at R = {R0:.2f}) | F |
|---|---|
{f_rows}
F falls steeply as P rises. Values below about 0.8 mean a single shell is a poor choice and two shells in series are needed.

## Using LMTD to monitor fouling

With four temperature transmitters and one flow meter, the overall U of an operating exchanger can be tracked: U = Q ÷ (A × LMTD). Suppose that months later, at the same flows and inlet temperatures, the water only reaches {Tco2:g} °C. Then Q = {Q2:.1f} kW, the oil leaves at {Tho2:.1f} °C, the LMTD is {LM2:.2f} K and U = {Q2*1e3:,.0f} ÷ ({LA:.2f} × {LM2:.2f}) = **{U2:.0f} W/m²·K**. The added fouling resistance is 1/{U2:.0f} − 1/{LU:g} = **{Rf*1e4:.2f} × 10⁻⁴ m²·K/W**, a useful trigger for cleaning.

## Common mistakes

- **Pairing the wrong ends.** In counterflow, ΔT₁ is hot inlet minus cold outlet; using hot inlet minus cold inlet gives a parallel flow LMTD.
- **Converting ΔT in °F with an offset.** A temperature difference converts by 1.8 only (1 K = 1.8 °F), with no 32 offset.
- **Leaving out F for multipass exchangers.** A 1-2 shell and tube unit sized on the counterflow LMTD alone is undersized.
- **Ignoring a temperature cross.** If the cold outlet rises above the hot outlet in a 1-2 exchanger, F drops sharply or no solution exists.
- **Using a clean U for design.** Add fouling resistances from TEMA or experience, or the exchanger will fall short after a few months.
''',
     faq_add=[('How do I calculate the actual U value of an operating exchanger?',
               'Measure the four terminal temperatures and one flow, calculate the duty Q = ṁ cp ΔT, find the LMTD here and divide: U = Q ÷ (A × LMTD). Trending this U over time shows fouling before the process is affected.')])

print('done')

from inplace import drop_backlog
print('backlog lines removed:', drop_backlog(['engineering/pulley-speed','engineering/compressor-power','engineering/low-flow-cutoff','engineering/vortex-shedding-frequency','engineering/pump-affinity-laws','engineering/fopdt-step-test','engineering/gear-ratio','engineering/rotameter-correction','engineering/calibration-error','engineering/weld-size','engineering/bending-stress','engineering/five-point-calibration','engineering/manning-equation','engineering/lambda-tuning','engineering/ziegler-nichols-pid-tuning','engineering/shaft-diameter','engineering/gas-flow-correction','engineering/factor-of-safety','engineering/spring-rate','engineering/lmtd']))
