"""Part C expansion (2026-11-22): 30 pages from the top of tools/upgrade-backlog.txt (priority list was empty), brought to the api-gravity standard. Assembled from six sections; edits are applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-22), slice 1: braking-resistor, earthing-resistance, thd, line-phase-voltage, generator-size.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-22'
IB = 'https://www.instrumentationblog.in/'
s3 = math.sqrt(3)


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Braking resistor
Vdc, Pb, dc = 760.0, 15e3, 0.10
R = Vdc ** 2 / Pb
Pr = Pb * dc
Ipk = Vdc / R
assert abs(R - 38.507) < 0.01 and abs(Pr - 1500) < 1e-9 and abs(Ipk - 19.737) < 0.01
# energy per braking cycle for a 120 s duty period
cyc = 120.0
t_on = cyc * dc
E_cyc = Pb * t_on
# two 75 ohm resistors in parallel
Rp = 75 * 75 / (75 + 75)
P_each_pk = Vdc ** 2 / 75
# resistance tolerance and heating: +10% when hot
R_hot = 37.5 * 1.10
P_hot = Vdc ** 2 / R_hot
# using motor rated voltage instead of bus voltage
R_wrong = 415 ** 2 / Pb
# table: average resistor rating for duty cycles
duty_rows = ''
for d in (0.05, 0.10, 0.20, 0.35, 0.50):
    duty_rows += f"| {d*100:.0f}% | {d*cyc:.0f} s of every {cyc:.0f} s | {Pb*d/1e3:.2f} kW | {Pb*d*cyc/1e3:,.0f} kJ |\n"

edit('electrical/braking-resistor', date=U,
     body_add=f'''
## Rating the resistor for the duty cycle

The average power is only half the thermal story; the resistor also has to absorb the energy of each stop without its element overheating. For the default 15 kW peak and a 120 s duty period:

| Duty cycle | Braking time | Average rating | Energy per cycle |
|---|---|---|---|
{duty_rows}
At 10% the resistor takes **{c(E_cyc/1e3)} kJ** in {t_on:.0f} s, then has {cyc - t_on:.0f} s to cool. Catalogue data quotes both a continuous rating and a short-time overload (for example 10 times continuous for 5 s), and both must cover the application.

## Building the value from standard resistors

Two **75 Ω** units in parallel give {Rp:.1f} Ω, just under the 38.5 Ω limit. Each sees the full bus voltage, so each must handle {c(P_each_pk)} W peak and half the average, {Pr/2/1e3:.2f} kW. Series strings share the voltage instead and suit low-ohm, high-voltage drives. Wire-wound and steel-grid resistors rise roughly 10% in resistance when hot: the {Rp:.1f} Ω pair becomes about {R_hot:.1f} Ω, which absorbs {c(P_hot/1e3, 1)} kW at the threshold, so leave some margin below R<sub>max</sub> rather than sitting exactly on it.

## Common mistakes

- **Using the motor voltage instead of the DC bus voltage.** 415² ÷ 15,000 gives {R_wrong:.1f} Ω, far too low, and would overload the chopper.
- **Rating the resistor at the peak power.** A 15 kW continuous resistor for 10% duty is ten times larger and costlier than needed; size it on 1.5 kW plus the short-time overload check.
- **Ignoring the drive's minimum ohms.** Paralleling extra resistors "for safety" lowers the value and can exceed the chopper current.
- **Forgetting the hot resistance.** If the value is chosen right at R<sub>max</sub>, warming lowers the braking power and the drive trips on DC bus overvoltage at the end of a long stop.
- **Running unscreened cable to a remote resistor.** The chopper switches the full bus voltage at high dv/dt, so use screened cable and keep it short.
''',
     faq_add=[('Can I use two braking resistors in parallel?',
               f'Yes. Two equal resistors in parallel halve the resistance and share the power, so two 75 Ω units make {Rp:.1f} Ω and each needs {Pr/2/1e3:.2f} kW continuous for the default 1.5 kW duty. Each must still be rated for the full DC bus voltage.'),
              ('How much energy does a braking resistor absorb per cycle?',
               f'Peak braking power multiplied by braking time. At 15 kW for 10% of a 120 s cycle that is 15 kW × {t_on:.0f} s = {c(E_cyc/1e3)} kJ per cycle, which the resistor short-time rating must accept.')])

# ---------------------------------------------------------------- Earthing resistance


def rod(rho, L, d):
    return rho / (2 * math.pi * L) * (math.log(8 * L / d) - 1)


rho, L, d = 100.0, 3.0, 0.016
R1 = rod(rho, L, d)
assert abs(R1 - 33.49) < 0.01
k1 = rho / (2 * math.pi * L)
ln_t = math.log(8 * L / d)
# rods in parallel using the page's factors
f2, f3, f4 = 0.58, 0.40, 0.33
R2, R3, R4 = R1 * f2, R1 * f3, R1 * f4
# length for 10 ohm single rod (bisection)
lo, hi = 1.0, 60.0
for _ in range(80):
    mid = (lo + hi) / 2
    if rod(rho, mid, d) > 10:
        lo = mid
    else:
        hi = mid
L10 = hi
# Wenner test reading
a_w, Rw = 3.0, 5.3
rho_w = 2 * math.pi * a_w * Rw
# dry season doubles resistivity
R_dry = rod(2 * rho, L, d)
# diameter table at 3 m, 100 ohm m
dia_rows = ''
for dd in (12.7, 16, 20, 25, 40):
    r = rod(rho, L, dd / 1000)
    dia_rows += f"| {dd:g} mm | {r:.1f} Ω | {(r / R1 - 1) * 100:+.1f}% |\n"
# fault current through one rod at 230 V in TT
If_tt = 230 / R1

edit('electrical/earthing-resistance', date=U, phrase='earthing resistance calculator',
     intro=("An earth electrode is only as good as its resistance to the soil around it, because that resistance sets the fault current and the touch voltage. "
            "This earthing resistance calculator applies the Dwight formula to soil resistivity, rod length and diameter; see this [earthing resistance calculation]"
            "(https://www.instrumentationblog.in/earthing-resistance-calculation/).\n\n"
            "Electrical contractors and plant engineers use it to plan earth pits, estimate how many rods a site needs and check designs for "
            "[TN, TT and IT earthing systems](https://www.instrumentationblog.in/tn-tt-it-earthing-systems/)."),
     body_add=f'''
## Worked example with the default values

A 3 m rod of 16 mm diameter in soil of 100 Ω·m:

1. ρ ÷ (2πL) = 100 ÷ (2π × 3) = **{k1:.3f} Ω**
2. 8L ÷ d = 24 ÷ 0.016 = 1,500, and ln(1,500) = **{ln_t:.3f}**
3. R = {k1:.3f} × ({ln_t:.3f} − 1) = **{R1:.1f} Ω**

That is well above a typical 10 Ω target. Using the spacing factors above, two rods give about {R2:.1f} Ω, three about {R3:.1f} Ω and four about {R4:.1f} Ω. A single rod would need to be about **{L10:.1f} m** long to reach 10 Ω on its own, which is why deep driven rods with couplers are common in poor soil.

## How much the diameter helps

At 3 m length in 100 Ω·m soil:

| Rod diameter | Resistance | Change from 16 mm |
|---|---|---|
{dia_rows}
Going from 16 mm to 40 mm pipe saves only a few ohms; the thicker rod is chosen for mechanical strength and corrosion life, not resistance.

## Measuring soil resistivity first

A Wenner four-pin survey drives four probes in a line at equal spacing a and passes current between the outer pair. Soil resistivity is ρ = 2πaR. With a = 3 m and a meter reading of {Rw} Ω, ρ = 2π × 3 × {Rw} = **{rho_w:.0f} Ω·m**. The probe spacing roughly equals the depth sampled, so repeat at 1.5, 3 and 6 m to see whether a deeper rod will reach better ground.

## Common mistakes

- **Designing on wet-season resistivity.** If the soil dries to 200 Ω·m, the same rod rises to {R_dry:.1f} Ω, double the value measured after rain.
- **Spacing rods too close.** Rods 1 m apart share most of their resistance area; keep spacing at least equal to the rod length.
- **Counting the rod alone in a TT system.** One {R1:.1f} Ω rod passes only about {If_tt:.1f} A at 230 V, far too little to trip a fuse or MCB, so an RCD is essential.
- **Testing with the test spike too close.** If the current probe is inside the rod's resistance area the reading is low; check by moving the potential probe 10% either side of 62% of the distance.
- **Measuring without disconnecting the earth link.** The parallel path through the supply earth makes a poor electrode look good.
''',
     faq_add=[('How do I convert a Wenner test reading into soil resistivity?',
               f'Use ρ = 2πaR, where a is the probe spacing in metres and R the meter reading. A reading of {Rw} Ω at 3 m spacing gives about {rho_w:.0f} Ω·m.'),
              ('How long must an earth rod be to reach 10 ohms?',
               f'It depends mainly on soil resistivity. In 100 Ω·m soil a 16 mm rod needs to be about {L10:.1f} m long to reach 10 Ω, compared with {R1:.1f} Ω for a 3 m rod.')])

# ---------------------------------------------------------------- THD
h = {1: 100.0, 3: 2.0, 5: 4.0, 7: 3.0, 11: 1.5, 13: 1.0}
ss = sum(v ** 2 for k, v in h.items() if k > 1)
thd = math.sqrt(ss) / h[1]
rms = math.sqrt(h[1] ** 2 + ss)
assert abs(thd - 0.056789) < 1e-5 and abs(rms - 100.161) < 0.001
# drive current at 40% THD
thd_i = 0.40
rms_ratio_40 = math.sqrt(1 + thd_i ** 2)
# TDD: 40% THD at 50% load
I1_load, IL_max = 50.0, 100.0
tdd = thd_i * I1_load / IL_max
# table THD vs RMS ratio
tab = ''
for t in (0.05, 0.10, 0.30, 0.50, 0.80, 1.00):
    rr = math.sqrt(1 + t * t)
    pfd = 1 / rr
    tab += f"| {t*100:.0f}% | {rr:.3f} | {pfd:.3f} |\n"
# contribution share of 5th harmonic
share5 = 16 / ss * 100

edit('electrical/thd', date=U, phrase='thd calculator',
     intro=("Drives, UPSs, LED drivers and computers draw distorted current that adds harmonics to the supply. "
            "This THD calculator combines the measured harmonic magnitudes into one total harmonic distortion figure and the true RMS value; see "
            "[power harmonics explained](https://www.instrumentationblog.in/power-harmonics-explained/).\n\n"
            "Power quality engineers and maintenance teams use it to check analyser readings against IEEE 519 limits and follow a "
            "[THD calculation for power systems](https://www.instrumentationblog.in/harmonic-distortion-thd-calculation-power-systems/)."),
     body_add=f'''
## Worked example with the default values

Square each harmonic: 2² + 4² + 3² + 1.5² + 1² = 4 + 16 + 9 + 2.25 + 1 = **{ss:.2f}**.

- THD = √{ss:.2f} ÷ 100 = {math.sqrt(ss):.3f} ÷ 100 = **{thd*100:.2f}%**
- True RMS = √(100² + {ss:.2f}) = **{rms:.2f}**

The 5th harmonic alone supplies {share5:.0f}% of the squared sum, so it is the one to target with a filter. Note that 5.7% distortion raises the RMS by only {(rms/100-1)*100:.2f}%: harmonics add in quadrature, so small amounts barely change the heating value.

## THD, RMS and distortion power factor

| THD | RMS ÷ fundamental | Distortion power factor |
|---|---|---|
{tab}
For a drive drawing current at {thd_i*100:.0f}% THD, the RMS current is {rms_ratio_40:.3f} times the fundamental, so cables and transformers carry about {(rms_ratio_40-1)*100:.0f}% more heating current than the kW suggests, and the true power factor is the displacement power factor multiplied by {1/rms_ratio_40:.3f}.

## THD versus TDD

IEEE 519 current limits use total demand distortion, which divides the harmonic current by the maximum demand current I<sub>L</sub> instead of the present fundamental. A feeder running at 50 A with {thd_i*100:.0f}% current THD and a 100 A maximum demand has TDD = {thd_i*100:.0f}% × 50 ÷ 100 = **{tdd*100:.0f}%**. Judging a lightly loaded feeder by THD makes it look much worse than it is.

## How it is measured

Class A power quality analysers (IEC 61000-4-30) compute harmonics with a 10 cycle (50 Hz) or 12 cycle (60 Hz) FFT window up to the 40th or 50th order, and IEEE 519 assessments use the 95th percentile of 10 minute values over a week. Record at the point of common coupling, and log voltage and current together so you can tell whether distortion comes from your loads or from the grid.

## Common mistakes

- **Entering only the harmonics shown on screen.** Leaving out the 17th, 19th and higher orders underestimates THD for 6-pulse drives.
- **Mixing units.** All inputs must be in the same unit, either all volts, all amps or all percent of the fundamental.
- **Comparing current THD with the voltage limit.** The 8% figure applies to voltage at 1 kV or below; current is judged by TDD.
- **Using a meter that is not true RMS.** An average-responding meter can read 10 to 40% low on distorted current.
- **Confusing THD-F and THD-R.** Some analysers divide by the total RMS (THD-R) instead of the fundamental, which gives a lower number at high distortion.
''',
     faq_add=[('What is the difference between THD and TDD?',
               f'THD divides the harmonic current by the present fundamental; TDD divides it by the maximum demand current. A feeder at half load with {thd_i*100:.0f}% THD has a TDD of {tdd*100:.0f}%, which is the figure IEEE 519 current limits use.'),
              ('Why does the true RMS barely change at low THD?',
               f'Harmonics add as the square root of the sum of squares, so RMS = fundamental × √(1 + THD²). At 5.7% THD the RMS is only {(rms/100-1)*100:.2f}% above the fundamental, while at 40% it is {(rms_ratio_40-1)*100:.0f}% higher.')])

# ---------------------------------------------------------------- Line and phase voltage
VL, IL, pf = 415.0, 10.0, 0.85
Vp_star = VL / s3
Ip_star = IL
P = s3 * VL * IL * pf
assert abs(Vp_star - 239.60) < 0.01 and abs(P - 6109.9) < 0.5
Vp_delta = VL
Ip_delta = IL / s3
P_check_star = 3 * Vp_star * Ip_star * pf
P_check_delta = 3 * Vp_delta * Ip_delta * pf
assert abs(P_check_star - P) < 1e-6 and abs(P_check_delta - P) < 1e-6
# high leg delta 240 V: wild leg to neutral
wild = 240 * s3 / 2
# star connection on wrong supply: delta-rated 415 V windings connected in star at 415 V
pw_ratio = (1 / s3) ** 2
# table: line current per kW at 0.85 pf
cur_rows = ''
for v in (208, 400, 415, 480, 690):
    i_kw = 1000 / (s3 * v * 0.85)
    cur_rows += f"| {v} V | {v/s3:.0f} V | {i_kw:.2f} A | {i_kw/s3:.2f} A |\n"

edit('electrical/line-phase-voltage', date=U, phrase='line and phase voltage calculator',
     intro=("Three-phase line values are measured between two lines, while phase values appear across each winding or load. "
            "This line and phase voltage calculator converts between them for star and delta connections and gives the total power; see "
            "[star vs delta connection](https://www.instrumentationblog.in/star-vs-delta-connection/) explained.\n\n"
            "Electricians, motor technicians and students use it to check nameplate voltages, wire motors correctly and work out the current in each winding or load."),
     body_add=f'''
## Worked example with the default values

A star connected load on a 415 V supply drawing 10 A per line at 0.85 power factor:

- Phase voltage = 415 ÷ √3 = **{Vp_star:.1f} V**
- Phase current = line current = **{Ip_star:.0f} A**
- Power = √3 × 415 × 10 × 0.85 = **{P/1e3:.2f} kW**

Switch the connection to delta with the same line values and each phase sees the full **415 V** but carries only 10 ÷ √3 = **{Ip_delta:.2f} A**. The power is unchanged: 3 × 415 × {Ip_delta:.3f} × 0.85 = {P_check_delta/1e3:.2f} kW, which confirms that the √3 formula with line values works for both.

## Line current per kW at 0.85 power factor

| Line voltage | Phase voltage (star) | Line current per kW | Delta winding current per kW |
|---|---|---|---|
{cur_rows}
## Checking it with a meter

With a true RMS multimeter, measure between each pair of lines (L1 L2, L2 L3, L3 L1) and then from each line to neutral. On a healthy 415 V star supply the line readings sit within about 2% of each other and the line to neutral readings near 240 V. A clamp meter on each line conductor gives the line current; on a delta motor the winding current can only be measured inside the terminal box on the link between winding ends, and it should be about 58% of the line reading.

## The 30 degree shift

In star, each line voltage is the phasor difference of two phase voltages, so it is √3 times larger and leads the first of them by 30°. This shift is why a Dyn11 transformer secondary is 30° ahead of its primary, and why two transformers of different vector groups must never be paralleled.

## Common mistakes

- **Applying √3 twice.** P = √3 × V<sub>L</sub> × I<sub>L</sub> already contains it; using phase voltage in that formula gives a result 1.73 times too small.
- **Looking for a neutral on a delta system.** A plain delta has none; a centre tapped 240 V high leg delta has a "wild leg" at {wild:.0f} V to neutral that must not feed 120 V loads.
- **Wiring a delta rated motor in star on the same supply.** Each winding then gets 1 ÷ √3 of its voltage and the motor develops only {pw_ratio*100:.0f}% of its torque.
- **Sizing delta winding conductors on line current.** Inside a delta the winding carries line current ÷ √3, so internal links can be smaller than the supply cable.
- **Reading line to neutral as line voltage.** A meter showing 240 V on a "415 V" system is normal when one probe is on neutral.
''',
     faq_add=[('What is the phase current in a delta connection?',
               f'Line current divided by √3. With 10 A in each line, each delta winding carries {Ip_delta:.2f} A, while the voltage across it equals the 415 V line voltage.'),
              ('What is the high leg in a delta system?',
               f'In a 240 V delta with one winding centre tapped for 120 V, the third line sits at about {wild:.0f} V to neutral. It is usually marked orange and must not supply single phase 120 V loads.')])

# ---------------------------------------------------------------- Generator size
P_kw, pfg, mg, Pm, ks = 80.0, 0.8, 0.20, 22.0, 2.5


def gen(P_kw, pfg, mg, Pm, ks):
    Sr = P_kw / pfg * (1 + mg)
    Ss = ((P_kw - Pm) / pfg + Pm * ks) / 1.5
    return Sr, Ss, max(Sr, Ss)


Sr, Ss, S = gen(P_kw, pfg, mg, Pm, ks)
assert abs(Sr - 120) < 1e-9 and abs(Ss - 85) < 1e-9 and S == 120
std = [15, 20, 25, 30, 40, 62.5, 82.5, 100, 125, 160, 200, 250, 320, 380, 500, 625, 750, 1010, 1250, 1500, 2000]


def nxt(x):
    return next(v for v in std if v >= x)


pick = nxt(S)
load_pct = P_kw / (pick * 0.8) * 100
st_rows = ''
for name, k in (('DOL', 6.5), ('Autotransformer', 3.5), ('Star-delta', 2.5), ('Soft starter', 2.0), ('VFD', 1.35)):
    a, b, s = gen(P_kw, pfg, mg, Pm, k)
    st_rows += f"| {name} | {k:g} | {b:.1f} kVA | {s:.1f} kVA | {nxt(s):g} kVA |\n"
_, Ss_dol, S_dol = gen(P_kw, pfg, mg, Pm, 6.5)
# starting the 22 kW motor first on an unloaded set
Ss_first = Pm * ks / 1.5
# without margin
Sr0 = P_kw / pfg

edit('electrical/generator-size', date=U, phrase='generator size calculator',
     intro=("A diesel generator must carry the running load and also ride through the surge when the largest motor starts. "
            "This generator size calculator gives the minimum kVA from both checks; see "
            "[how to calculate generator size for industrial load](https://www.instrumentationblog.in/how-to-calculate-generator-size-industrial-load/).\n\n"
            "Electrical consultants, facility managers and DG set suppliers use it to avoid sets that stall on motor starts or run so lightly loaded that they wet-stack, and to plan the "
            "[AMF panel auto start](https://www.instrumentationblog.in/amf-panel-working-dg-auto-start/)."),
     body_add=f'''
## Worked example with the default values

- Running check: 80 ÷ 0.8 = {Sr0:.0f} kVA, plus 20% margin = **{Sr:.0f} kVA**
- Starting check: the other 58 kW need 58 ÷ 0.8 = {58/0.8:.1f} kVA, the star-delta motor needs 22 × 2.5 = {22*2.5:.0f} kVA, total {58/0.8+55:.1f} kVA ÷ 1.5 = **{Ss:.0f} kVA**
- The larger figure is {S:.0f} kVA, so the next standard set is **{pick:g} kVA**

At {pick:g} kVA (a {pick*0.8:g} kW set) the 80 kW load is {load_pct:.0f}% of the kW rating today, a healthy level for a diesel engine, with the margin left for growth.

## How the starter changes the answer

Same 80 kW load and 22 kW motor:

| Starter | kVA per kW | Starting check | Required | Standard set |
|---|---|---|---|---|
{st_rows}
With a DOL starter the motor start, not the running load, decides the size and pushes the set up to {nxt(S_dol):g} kVA. Fitting a star-delta starter, soft starter or VFD on the largest motor is often cheaper than buying the bigger generator.

## Prime, standby and continuous ratings

ISO 8528-1 defines several ratings for the same engine. A **standby** rating covers emergency use for limited hours a year with no overload; a **prime** rating allows unlimited hours at a varying load with a 10% overload for one hour in twelve, and is typically about 10% lower than standby; a **continuous** rating is for constant base load. For a factory that runs on the DG during regular grid outages, size on the prime rating.

## Load testing after installation

A new set is commissioned on a resistive load bank at 25, 50, 75 and 100% for set periods while voltage, frequency, oil pressure and coolant temperature are logged, then the actual largest motor is started with the rest of the load connected while a recorder captures the voltage dip and frequency recovery.

## Common mistakes

- **Adding motor kW to kVA directly.** Convert the running load to kVA with its power factor before adding the starting kVA.
- **Sizing only on the running load.** With a DOL motor the starting check here needs {Ss_dol:.0f} kVA, more than the {Sr:.0f} kVA running figure.
- **Starting the biggest motor last.** Started first on an unloaded set it needs only {Ss_first:.1f} kVA of equivalent capacity, so sequence the large motors first in the AMF logic.
- **Using standby rating for daily running.** A set run for hours every day on its standby rating wears out early and voids warranty.
- **Ignoring UPS and VFD harmonics.** Non-linear loads heat the alternator; many suppliers ask for an oversized alternator on the same engine.
''',
     faq_add=[('What is the difference between prime and standby generator ratings?',
               'Under ISO 8528-1 standby is for emergency use with no overload allowed, while prime allows unlimited hours at varying load with a 10% overload for one hour in twelve. Prime is usually about 10% lower than standby for the same engine.'),
              ('How heavily loaded will the selected generator run?',
               f'Divide the running kW by the set kW rating, which is kVA × 0.8. For the default 80 kW on a {pick:g} kVA set that is {load_pct:.0f}%, inside the 30 to 80% band that diesel engines prefer.')])

print('slice 1 done', inplace.DONE)

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-22), slice 2: transformer-short-circuit, per-unit, earth-fault-loop-impedance, generator-power-angle, motor-starting-current.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-22'
IB = 'https://www.instrumentationblog.in/'
r3 = math.sqrt(3)


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Transformer short-circuit current
S, V, Z = 1000.0, 415.0, 0.05
Ifl = S * 1000 / (r3 * V)
Isc = Ifl / Z
MVA = S / Z / 1000
assert abs(Ifl - 1391.2) < 0.1 and abs(Isc / 1000 - 27.82) < 0.01 and abs(MVA - 20) < 1e-9
# upstream source of finite fault level, referred to the transformer base
src_rows = ''
for Ssrc in (None, 1000, 500, 250, 100):
    zs = 0 if Ssrc is None else (S / 1000) / Ssrc
    i = Ifl / (Z + zs) / 1000
    lab = 'Infinite bus' if Ssrc is None else f'{Ssrc:,} MVA'
    src_rows += f"| {lab} | {zs*100:.2f}% | {(Z+zs)*100:.2f}% | {i:.1f} kA |\n"
zs250 = (S / 1000) / 250
I250 = Ifl / (Z + zs250) / 1000
# impedance tolerance: IEC 60076-1 allows -10% on Z for two winding units
Zlow = Z * 0.9
Ilow = Ifl / Zlow / 1000
# peak current with X/R = 5 (IEC 60909 kappa)
XR = 5.0
kap = 1.02 + 0.98 * math.exp(-3 / XR)
ip = kap * math.sqrt(2) * Isc / 1000
# two identical transformers in parallel
Ipar = 2 * Isc / 1000
# short-circuit test voltage on an 11 kV primary
Vtest = 11000 * Z

edit('electrical/transformer-short-circuit', date=U, phrase='transformer short-circuit current calculator',
     intro=("A transformer's own impedance is the main thing that limits current when a fault strikes its secondary terminals. "
            "This transformer short-circuit current calculator takes the kVA rating, secondary voltage and nameplate impedance and returns the full-load current, the symmetrical three-phase fault current and the fault level in MVA.\n\n"
            "Electrical designers use it to pick breaker breaking capacity, busbar ratings and cable withstand, as explained in this guide to "
            "[short circuit current calculation](https://www.instrumentationblog.in/short-circuit-current-calculation/)."),
     body_add=f'''
## Worked example with a real upstream supply

For the default 1,000 kVA, 415 V, 5% transformer:

- I<sub>FL</sub> = 1,000,000 ÷ (√3 × 415) = **{Ifl:,.1f} A**
- I<sub>sc</sub> = {Ifl:,.1f} ÷ 0.05 = **{Isc/1000:.2f} kA**, a fault level of **{MVA:.0f} MVA**

That assumes the 11 kV network behind the transformer has no impedance. If the utility quotes a fault level of 250 MVA at the primary, its impedance on the 1 MVA transformer base is 1 ÷ 250 = {zs250*100:.2f}%. Adding it to the transformer gives {(Z+zs250)*100:.2f}% and the fault current falls to **{I250:.1f} kA**, only about {(1-I250/(Isc/1000))*100:.0f}% lower. For LV switchgear selection the infinite bus figure is therefore a sensible, slightly conservative number.

## Effect of the upstream fault level

1,000 kVA, 415 V, 5% transformer:

| Source fault level | Source impedance (on 1 MVA) | Total impedance | Fault current |
|---|---|---|---|
{src_rows}
The stronger the grid, the closer the result gets to the simple formula. Weak rural supplies matter more for small transformers on long overhead lines.

## Peak current and making capacity

The calculator gives the symmetrical RMS current. The first peak is higher because of the DC offset. IEC 60909 gives i<sub>p</sub> = κ × √2 × I<sub>k</sub> with κ = 1.02 + 0.98 e<sup>−3R/X</sup>. With X/R = {XR:g}, κ = {kap:.3f} and the peak is **{ip:.1f} kA**. Breakers are rated for this through their making capacity I<sub>cm</sub>, and busbar supports must withstand the force it produces.

## Where the impedance figure comes from

Percentage impedance is measured in the factory short-circuit test: the secondary is shorted and the primary voltage is raised until rated current flows. On an 11 kV primary a 5% unit reaches full-load current at about **{Vtest:.0f} V**. That voltage as a percentage of rated voltage is Z%, which is why a lower Z% always means a higher fault current.

## Common mistakes

- **Ignoring the impedance tolerance.** IEC 60076-1 allows the measured impedance to be 10% below the declared value. At 4.5% the default transformer gives **{Ilow:.1f} kA**, which can push a 30 kA rated board over its limit.
- **Forgetting parallel transformers.** Two 1,000 kVA, 5% units on one busbar give about **{Ipar:.1f} kA**, so the switchboard must be rated for the combined value.
- **Leaving out motor contribution.** Running induction motors feed the fault for the first few cycles, often taken as about 4 times their combined full-load current.
- **Comparing RMS current with a peak rating.** I<sub>cu</sub> and I<sub>cs</sub> are RMS values; I<sub>cm</sub> is a peak value and must be checked against i<sub>p</sub>.
- **Entering phase voltage.** Use the line voltage (415 V, not 240 V); phase voltage overstates the current by √3.
''',
     faq_add=[('How does the upstream grid fault level change transformer fault current?',
               f'Convert the grid fault level to an impedance on the transformer base (kVA ÷ 1,000 ÷ grid MVA) and add it to Z%. For 1,000 kVA, 5% and a 250 MVA grid, the total is {(Z+zs250)*100:.2f}% and the fault current drops from {Isc/1000:.1f} kA to {I250:.1f} kA.'),
              ('What is the peak short-circuit current of a transformer fault?',
               f'Multiply the RMS fault current by κ × √2, where κ depends on the X/R ratio. With X/R = {XR:g}, κ is {kap:.2f}, so a {Isc/1000:.1f} kA fault peaks at about {ip:.0f} kA in the first half cycle.')])

# ---------------------------------------------------------------- Per-unit system
Sb, Vb, Zo, Sn, Vn = 10e6, 11e3, 0.6, 100e6, 11e3
Zb = Vb ** 2 / Sb
Ib = Sb / (r3 * Vb)
Zpu = Zo / Zb
Zpn = Zpu * (Vb / Vn) ** 2 * (Sn / Sb)
assert abs(Zb - 12.1) < 1e-9 and abs(Ib - 524.86) < 0.01 and abs(Zpu - 0.049587) < 1e-6 and abs(Zpn - 0.49587) < 1e-5
# hand fault study on a 100 MVA base
z_grid = 100 / 250.0
z_cab = Zpn
z_tx = 0.0625 * 100 / 2.5
z_tot = z_grid + z_cab + z_tx
Ib_lv = 100e6 / (r3 * 415)
If_lv = Ib_lv / z_tot
# off nominal voltage rating
z_off = 0.06 * (10.5 / 11) ** 2
# base current table on 100 MVA
ib_rows = ''
for kv in (0.415, 3.3, 6.6, 11, 33, 66, 132):
    ib = 100e6 / (r3 * kv * 1e3)
    ib_rows += f"| {kv:g} kV | {c(ib)} A | {c(ib/1000, 2)} kA |\n"

edit('electrical/per-unit', date=U, phrase='per-unit system calculator',
     intro=("The per-unit method expresses impedances, voltages and currents as fractions of chosen base values, so transformer ratios drop out of the maths. "
            "This per-unit system calculator finds base impedance, base current and the per-unit impedance, then converts it to a new MVA or kV base.\n\n"
            "Protection and planning engineers use it to build hand fault studies and to put nameplate data on one system base, as shown in this introduction to the "
            "[per-unit system in power systems](https://www.instrumentationblog.in/per-unit-system-power-system/)."),
     body_add=f'''
## Worked example with the default inputs

An 11 kV cable has an impedance of 0.6 Ω. On a 10 MVA, 11 kV base:

- Z<sub>b</sub> = 11² ÷ 10 = **{Zb:.1f} Ω** and I<sub>b</sub> = 10,000,000 ÷ (√3 × 11,000) = **{Ib:.2f} A**
- Z<sub>pu</sub> = 0.6 ÷ {Zb:.1f} = **{Zpu:.5f} pu**
- Moved to a 100 MVA base at the same voltage: {Zpu:.5f} × (11 ÷ 11)² × (100 ÷ 10) = **{Zpn:.5f} pu**

## A hand fault study on one base

Take a 250 MVA, 11 kV grid feeding that cable, then a 2.5 MVA, 11/0.415 kV, 6.25% transformer, with a fault on the LV busbar. Everything goes on 100 MVA:

| Element | Per-unit impedance (100 MVA) | How it was found |
|---|---|---|
| Grid | {z_grid:.4f} | 100 ÷ 250 |
| 11 kV cable | {z_cab:.4f} | from the calculator above |
| Transformer | {z_tx:.4f} | 0.0625 × 100 ÷ 2.5 |
| **Total** | **{z_tot:.4f}** | series sum |

Base current at 415 V on 100 MVA is {c(Ib_lv)} A, so the fault current is {c(Ib_lv)} ÷ {z_tot:.4f} = **{If_lv/1000:.1f} kA**. No turns ratio was needed because the base voltage changed from 11 kV to 0.415 kV across the transformer, exactly in step with its ratio. (Resistance and reactance are added as plain magnitudes here, which is a common conservative shortcut.)

## Base currents on a 100 MVA base

| Base voltage | Base current | In kA |
|---|---|---|
{ib_rows}
## Equipment rated at a different voltage

Nameplate values are on the equipment's own rating. A 6% transformer rated 10.5 kV used on an 11 kV base becomes 0.06 × (10.5 ÷ 11)² = **{z_off:.4f} pu** before any MVA change. Ignoring the voltage term here is a small but real error.

## Common mistakes

- **Mixing phase and line quantities.** Use three-phase MVA with line kV, or single-phase MVA with phase kV, never one of each.
- **Keeping one base voltage across a transformer.** The voltage base must follow the turns ratio from zone to zone, or the per-unit values are wrong on one side.
- **Inverting the change of base.** Per-unit impedance rises with the new MVA base and falls with a higher new kV base; check that a 100 MVA base gives a bigger pu figure than a 10 MVA base.
- **Forgetting to convert back.** A fault result of 0.3 pu current means nothing until it is multiplied by the base current of that voltage zone.
- **Treating % and pu as different impedances.** 6% and 0.06 pu are the same thing on the same base.
''',
     faq_add=[('Why does the base voltage change across a transformer?',
               'The base voltages on each side are chosen in the ratio of the transformer turns. That way the transformer has the same per-unit impedance seen from either winding and the ideal ratio disappears from the circuit.'),
              ('How do I convert a per-unit fault current back to amps?',
               f'Multiply by the base current of the voltage zone where the fault is. On a 100 MVA base at 415 V the base current is about {c(Ib_lv)} A, so 0.3 pu is about {0.3*Ib_lv/1000:.1f} kA.')])

# ---------------------------------------------------------------- Earth fault loop impedance
U0, Ze, R12, k, In = 230.0, 0.35, 0.4, 5, 32
Zs = Ze + R12
If = 0.95 * U0 / Zs
Zmax = 0.95 * U0 / (k * In)
ok = Zmax - Zs
assert abs(Zs - 0.75) < 1e-9 and abs(If - 291.33) < 0.01 and abs(Zmax - 1.3656) < 1e-4 and abs(ok - 0.6156) < 1e-4
r25 = 19.51  # mOhm/m, 2.5/1.5 mm2 copper at 20 C
L_def = R12 / (r25 / 1000)
R12hot = R12 * 1.20
Zs_hot = Ze + R12hot
Zm80 = 0.8 * Zmax
ZmaxC = 0.95 * U0 / (10 * In)
# maximum length table, 32 A Type B, Ze 0.35, conductors at 70 C (x1.20)
len_rows = ''
for name, r in (('2.5 / 1.5 mm²', 19.51), ('4 / 1.5 mm²', 16.71), ('6 / 2.5 mm²', 10.49), ('10 / 4 mm²', 6.44)):
    Lmax = (Zmax - Ze) / (r * 1.20 / 1000)
    LmaxC = (ZmaxC - Ze) / (r * 1.20 / 1000)
    len_rows += f"| {name} | {r:.2f} mΩ/m | {Lmax:.0f} m | {LmaxC:.0f} m |\n"

edit('electrical/earth-fault-loop-impedance', date=U, phrase='earth fault loop impedance calculator',
     intro=("Earth fault loop impedance (Zs) is the total resistance of the path a fault current follows from the supply, through the line conductor and back along the protective conductor. "
            "This earth fault loop impedance calculator gives Zs, the prospective fault current and the maximum Zs that lets an MCB trip instantly.\n\n"
            "Electricians and inspectors use it to check circuits before testing, as described in "
            "[earth fault loop impedance (Zs) testing](https://www.instrumentationblog.in/earth-fault-loop-impedance-zs-testing/), and designers use it to set cable lengths."),
     body_add=f'''
## Worked example with the default inputs

A 32 A Type B radial circuit on a PME supply with Z<sub>e</sub> = 0.35 Ω and R<sub>1</sub> + R<sub>2</sub> = 0.4 Ω:

- Z<sub>s</sub> = 0.35 + 0.4 = **{Zs:.2f} Ω**
- I<sub>f</sub> = 0.95 × 230 ÷ {Zs:.2f} = **{If:.1f} A**
- Z<sub>s,max</sub> = 0.95 × 230 ÷ (5 × 32) = **{Zmax:.4f} Ω**, so the margin is **{ok:.4f} Ω** and the MCB trips instantly

In 2.5/1.5 mm² twin and earth (19.51 mΩ/m at 20 °C), 0.4 Ω is about {L_def:.1f} m of cable. At its 70 °C operating temperature the conductors are about 20% more resistive, so R<sub>1</sub> + R<sub>2</sub> becomes {R12hot:.2f} Ω and Z<sub>s</sub> {Zs_hot:.2f} Ω, still inside the limit. A measured cold reading should be no more than 80% of {Zmax:.3f} Ω, that is **{Zm80:.2f} Ω**, and {Zs:.2f} Ω passes.

The same circuit on a 32 A **Type C** breaker fails: its limit is {ZmaxC:.3f} Ω, so {If:.0f} A would not reach the 320 A needed for instantaneous tripping.

## Maximum circuit length for a 32 A MCB

Z<sub>e</sub> = 0.35 Ω, copper conductors corrected to 70 °C, 0.4 s disconnection:

| Line / CPC size | R<sub>1</sub> + R<sub>2</sub> at 20 °C | Type B 32 A | Type C 32 A |
|---|---|---|---|
{len_rows}
Voltage drop often limits the length before Zs does, so check both.

## How Zs is tested on site

Z<sub>e</sub> is measured at the origin with the main earthing conductor disconnected, which is only safe with the installation isolated, and reconnected straight after. Z<sub>s</sub> is measured at the furthest point of each circuit with a loop tester, using its no-trip mode on RCD protected circuits. Parallel earth paths through metal pipework can make a live Zs reading lower than Z<sub>e</sub> + R<sub>1</sub> + R<sub>2</sub>, so a reading far below the calculated value is worth questioning rather than celebrating.

## Common mistakes

- **Comparing a cold reading with the full table value.** Conductors heat up in service, which is why the 80% rule exists.
- **Using the Type B column for a Type C or D breaker.** The limit halves each time the trip multiple doubles.
- **Assuming the supplier's declared Ze.** The declared 0.35 Ω is a maximum; measure the real value, but design with the declared one.
- **Adding R1 + R2 for a ring as if it were radial.** On a ring final circuit the end-to-end values are combined as (r1 + r2) ÷ 4.
- **Forgetting the RCD on TT systems.** With a Zs of tens of ohms an MCB can never trip on earth faults and an RCD is the protection.
''',
     faq_add=[('How long can a 32 A Type B radial circuit in 2.5 mm² cable be?',
               f'With Ze = 0.35 Ω and conductors corrected to 70 °C, the Zs limit of {Zmax:.2f} Ω allows about {(Zmax-Ze)/(19.51*1.2/1000):.0f} m of 2.5/1.5 mm² cable. Voltage drop usually becomes the limit first.'),
              ('Why can a measured Zs be lower than Ze plus R1 + R2?',
               'Parallel earth paths such as bonded water and gas pipes or structural steel share the fault current and lower the reading. The design value should still be based on the cable alone, because those paths are not guaranteed.')])

# ---------------------------------------------------------------- Generator power angle
E, Vg, X, d = 12e3, 11e3, 10.0, 20.0
P = E * Vg / X * math.sin(math.radians(d))
Pmax = E * Vg / X
Q = (E * Vg * math.cos(math.radians(d)) - Vg ** 2) / X / 1e6
assert abs(P / 1e6 - 4.5146) < 1e-3 and abs(Pmax / 1e6 - 13.2) < 1e-9 and abs(Q - 0.3040) < 1e-3
# load angle for 9 MW
P9 = 9e6
d9 = math.degrees(math.asin(P9 / Pmax))
Q9 = (E * Vg * math.cos(math.radians(d9)) - Vg ** 2) / X / 1e6
# reactance in per unit on 10 MVA, 11 kV
Xpu = X / (11e3 ** 2 / 10e6)
# excitation table at constant P = default
ex_rows = ''
for Ek in (10, 11, 12, 13, 14):
    Ev = Ek * 1e3
    dd = math.degrees(math.asin(P * X / (Ev * Vg)))
    qq = (Ev * Vg * math.cos(math.radians(dd)) - Vg ** 2) / X / 1e6
    ex_rows += f"| {Ek} kV | {dd:.1f}° | {Ev*Vg/X/1e6:.2f} MW | {qq:+.2f} MVAr |\n"
# phase voltage mistake
P_wrong = (E / r3) * (Vg / r3) / X * math.sin(math.radians(d)) / 1e6
# radians mistake
P_rad = E * Vg / X * math.sin(20) / 1e6

edit('electrical/generator-power-angle', date=U, phrase='generator power angle calculator',
     intro=("A synchronous generator's real power output depends on the load angle δ between its internal EMF and the bus voltage, while its field current sets the reactive power. "
            "This generator power angle calculator gives the three-phase active power, the steady-state pull-out limit and the reactive power of a round-rotor machine.\n\n"
            "Power plant and protection engineers use it to judge stability margins and to see how the "
            "[excitation system and AVR](https://www.instrumentationblog.in/generator-excitation-system-avr/) change MVAr output."),
     body_add=f'''
## Finding the load angle for a set output

Run the equation backwards to see how hard the machine is working. For the default generator to deliver 9 MW:

- sin δ = 9 ÷ 13.2 = {P9/Pmax:.4f}, so δ = **{d9:.1f}°**
- Q = (12,000 × 11,000 × cos {d9:.1f}° − 11,000²) ÷ 10 = **{Q9:.2f} MVAr**

At this point the machine is absorbing reactive power, because 12 kV of EMF is no longer enough to export MVAr at that angle. The operator would raise the excitation, which lowers δ and restores a lagging power factor.

## Raising excitation at constant power

Holding the default {P/1e6:.3f} MW output while the AVR changes the EMF:

| Internal EMF E | Load angle δ | Pull-out power | Reactive power |
|---|---|---|---|
{ex_rows}
Higher excitation gives a smaller load angle and a larger pull-out power, so an over-excited machine is more stable. Running under-excited to absorb MVAr pushes δ up and erodes the margin, which is why under-excitation limiters exist.

## In practice

The synchronous reactance of 10 Ω is {Xpu:.3f} pu on a 10 MVA, 11 kV base, typical of a round-rotor machine. The angle itself is rarely measured directly; the AVR, the capability chart and the pole-slip relay work from terminal voltage, current and power. A power system stabiliser adds damping so that δ does not swing after a disturbance. Real machines also have a step-up transformer and line reactance between them and the grid, which add to X<sub>s</sub> and lower the pull-out power.

## Common mistakes

- **Using phase voltages without multiplying by 3.** With E and V entered as 6.93 kV and 6.35 kV the formula gives {P_wrong:.3f} MW, one third of the real {P/1e6:.3f} MW.
- **Leaving a spreadsheet in radians.** SIN(20) in Excel treats 20 as radians and returns {P_rad:.2f} MW; use SIN(RADIANS(20)).
- **Using sub-transient reactance for steady state.** X″<sub>d</sub> is for fault currents; steady-state power uses X<sub>s</sub>, and transient stability uses X′<sub>d</sub>.
- **Treating P<sub>max</sub> as an operating point.** At 90° any small disturbance causes pole slipping; continuous operation stays well below it.
- **Reading E from the terminals under load.** E is the open-circuit voltage for the present field current, not the measured terminal voltage.
''',
     faq_add=[('How do I find the load angle for a given generator output?',
               f'Use δ = arcsin(P × X_s ÷ (E × V)). For 9 MW from the default machine (E = 12 kV, V = 11 kV, X_s = 10 Ω), δ is about {d9:.0f}°.'),
              ('What happens to the load angle when excitation is reduced?',
               'At constant power the angle increases because a smaller E must deliver the same E V sin δ. The pull-out limit falls at the same time, so a weakly excited machine is closer to losing synchronism.')])

# ---------------------------------------------------------------- Motor starting current
Ifl_m, km, m = 20.0, 6.5, 0.333333
Idol = km * Ifl_m
Is = Idol * m
Ts = m * 100
assert abs(Idol - 130) < 1e-9 and abs(Is - 43.33) < 0.01 and abs(Ts - 33.33) < 0.01
meth = (('Direct-on-line', 1.0), ('Star-delta', 1 / 3), ('Autotransformer 80%', 0.64),
        ('Autotransformer 65%', 0.4225), ('Autotransformer 50%', 0.25))
TstTn = 2.2
m_rows = ''
for name, f in meth:
    m_rows += f"| {name} | {Idol*f:.1f} A | {Idol*f/Ifl_m:.2f} × FLC | {TstTn*f:.2f} × rated |\n"
k_rows = ''
for kk in (5.0, 6.0, 6.5, 7.0, 8.0):
    k_rows += f"| {kk:g} | {kk*Ifl_m:.0f} A | {kk*Ifl_m/3:.1f} A |\n"
Tsd = TstTn / 3
Tat65 = TstTn * 0.4225

edit('electrical/motor-starting-current', date=U, phrase='motor starting current calculator',
     intro=("An induction motor started direct-on-line draws its locked-rotor current, several times full-load current, until it nears full speed. "
            "This motor starting current calculator estimates that inrush and the reduced current and torque with star-delta or autotransformer starting.\n\n"
            "Electrical designers and maintenance engineers use it to size supplies, protection and generators, and to choose a starter, as compared in "
            "[DOL vs star-delta starter](https://www.instrumentationblog.in/dol-vs-star-delta-starter-which-to-use/) and "
            "[motor starting methods compared](https://www.instrumentationblog.in/motor-starting-methods-compared/)."),
     body_add=f'''
## Will the motor still start? A torque check

Cutting current also cuts torque, so the starter must leave enough torque to accelerate the load. Take the default 20 A motor with a 6.5 × current ratio and, from a typical datasheet, a DOL starting torque of {TstTn:g} × rated torque:

| Method | Line current | Current ratio | Starting torque |
|---|---|---|---|
{m_rows}
With star-delta the motor starts with only {Tsd:.2f} × rated torque. That is plenty for a centrifugal pump or fan, whose load torque at standstill is small, but a loaded conveyor needing close to full torque would stall. The 65% autotransformer tap gives {Tat65:.2f} × rated torque for {Idol*0.4225:.1f} A, a useful middle ground.

## Starting current for different motor ratios

20 A full-load current:

| DOL ratio I<sub>A</sub>/I<sub>N</sub> | DOL current | Star-delta current |
|---|---|---|
{k_rows}
Premium efficiency IE3 and IE4 motors tend to sit at the top of this range, so replacing an old motor can raise the inrush on the same supply.

## Measuring starting current

A clamp meter with an inrush function captures the RMS current over the first 100 ms or so and gives a figure that can be compared with k × FLC. A power quality recorder also shows how long the current stays high, which is the run-up time. Heavy, high inertia loads keep the current near locked-rotor value for many seconds, so the protection and the motor's thermal limit must both be checked against that time, not only the peak.

## Common mistakes

- **Fitting star-delta to the wrong winding.** The motor must be rated for delta at the supply voltage, for example 400 V delta / 690 V star on a 400 V system. A 230/400 V motor cannot be started star-delta on 400 V.
- **Ignoring the changeover spike.** In open transition star-delta the motor is briefly disconnected, and reconnecting in delta can draw a current close to DOL if it changes over too early.
- **Using rated torque instead of starting torque.** The one third reduction applies to the DOL starting torque from the datasheet, not to the rated torque.
- **Taking FLC from a different voltage.** A dual voltage nameplate lists two currents; use the one for your supply.
- **Forgetting the first half cycle.** The asymmetrical peak is higher than the RMS locked-rotor current, so instantaneous trips are set with margin above it.
''',
     faq_add=[('Which motor connection do I need for a star-delta starter?',
               'A motor whose delta voltage equals the supply line voltage, with all six winding ends brought out. On a 400 V supply that means a 400 V delta / 690 V star motor.'),
              ('How do I measure motor starting current?',
               f'Use a clamp meter with an inrush mode or a power quality recorder on one phase during a start. For the default motor you would expect about {Idol:.0f} A DOL or {Is:.0f} A in star-delta.')])

print('slice 2 done', inplace.DONE)

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-22), slice 3: amps-to-watts, motor-starting-voltage-dip, kw-to-amps, kva-to-kw, power-factor-correction.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-22'
IB = 'https://www.instrumentationblog.in/'
R3 = math.sqrt(3)


def c(x, d=0):
    return f"{x:,.{d}f}"


def edit_keep_featured(cid, **kw):
    """Some pages are already featured. Lift the flag around the edit and restore it unchanged."""
    path = os.path.join(inplace.BASE, cid + '.mdx')
    s = open(path).read()
    line = 'featured: true\n'
    assert s.count(line) == 1, cid
    open(path, 'w').write(s.replace(line, '', 1))
    try:
        n = edit(cid, **kw)
    except Exception:
        open(path, 'w').write(s)
        raise
    t = open(path).read()
    k = t.index('\nupdated: ')
    k = t.index('\n', k + 1) + 1
    open(path, 'w').write(t[:k] + line + t[k:])
    return n


# ---------------------------------------------------------------- Amps to watts
I0, V0, ph0, pf0 = 10.0, 230.0, 1.0, 1.0
P0 = ph0 * V0 * I0 * pf0
assert abs(P0 - 2300) < 1e-9
# same 10 A on a 400 V three-phase motor circuit at PF 0.85
P3 = R3 * 400 * 10 * 0.85
# a clamp reading of 4.2 A on a 230 V fridge compressor at PF 0.7
Pf = 230 * 4.2 * 0.7
VAf = 230 * 4.2
# 12 V inverter: 1,000 W load, 90% efficient
Iinv = 1000 / 0.9 / 12
# 10 A in different systems
sys_rows = ''
for name, ph, v, pf in (('12 V DC', 1, 12, 1), ('24 V DC', 1, 24, 1), ('48 V DC', 1, 48, 1),
                        ('120 V single-phase, PF 0.9', 1, 120, 0.9), ('230 V single-phase, PF 1', 1, 230, 1),
                        ('230 V single-phase, PF 0.8', 1, 230, 0.8), ('400 V three-phase, PF 0.85', R3, 400, 0.85),
                        ('480 V three-phase, PF 0.85', R3, 480, 0.85)):
    sys_rows += f"| {name} | {c(ph * v * 10 * pf)} W |\n"
# wrong: phase voltage with sqrt3
Pwrong = R3 * 230 * 10 * 0.85

edit('electrical/amps-to-watts', date=U, phrase='amps to watts calculator',
     intro=("Current in amps and power in watts are linked by the supply voltage and, for AC loads, by power factor. "
            "This amps to watts calculator works for DC, single-phase and three-phase circuits and solves for whichever value you leave blank, so it also converts watts to amps.\n\n"
            "Electricians, solar installers and homeowners use it to check what a socket, fuse, inverter or generator can supply and to turn a clamp meter reading into an estimate of real power."),
     body_add=f'''
## Worked example

With the default inputs, a 10 A load on a 230 V single-phase supply at unity power factor:

- P = V × I × PF = 230 × 10 × 1 = **{c(P0)} W**, or 2.3 kW

Switch the system to three-phase, enter 400 V and a power factor of 0.85, and the same 10 A per line gives √3 × 400 × 10 × 0.85 = **{c(P3)} W**. The current is identical, but the three-phase circuit delivers about {P3 / P0:.1f} times the power because three conductors share it.

## What 10 A means on different supplies

| System | Power at 10 A |
|---|---|
{sys_rows}
The table shows why a current rating alone says little about capacity: 10 A is a small car accessory at 12 V and a {c(R3 * 480 * 10 * 0.85 / 1000, 1)} kW motor at 480 V.

## Turning a clamp meter reading into watts

A clamp meter reads RMS current, not power. Multiplying that reading by the supply voltage gives volt-amperes, which equals watts only for resistive loads such as kettles, immersion heaters and incandescent lamps. A fridge compressor drawing 4.2 A on 230 V shows {c(VAf)} VA, but at a typical running power factor of 0.7 it uses only about **{c(Pf)} W**. For an accurate figure on motors, compressors and electronics, use a plug-in energy meter or a power analyser that multiplies voltage and current sample by sample. Read the current once the load has settled, since motors draw several times their running current for the first second or two.

## Battery and inverter currents

On the DC side of an inverter, divide the AC load by the inverter efficiency before converting. A 1,000 W load on a 12 V inverter that is 90% efficient pulls 1,000 ÷ 0.9 ÷ 12 = **{Iinv:.0f} A** from the battery, which sets the cable size and fuse rating.

## Common mistakes

- **Using the phase voltage in the three-phase formula.** √3 × 230 V × 10 A × 0.85 gives {c(Pwrong)} W, far below the real {c(P3)} W on a 400 V line voltage. Use the line-to-line voltage with √3.
- **Leaving power factor at 1 for motors.** Pumps, fans and compressors run at 0.7 to 0.9, so watts are lower than volts × amps.
- **Reading the nameplate current as the running current.** Nameplates often show the maximum or full-load value; actual draw at part load is lower.
- **Forgetting inverter losses on battery systems.** Ignoring a 10% loss underestimates battery current by about 11%.
- **Using peak instead of RMS values.** A 230 V supply peaks at about 325 V, but power formulas use RMS voltage and current.
''',
     faq_add=[('Can I find watts with just a clamp meter?',
               f'Only for resistive loads. A clamp gives amps, and volts × amps is VA. For a motor or compressor you also need the power factor: 4.2 A at 230 V and PF 0.7 is about {c(Pf)} W, not {c(VAf)} W.'),
              ('How many watts is 10 amps on a 400 V three-phase supply?',
               f'About {c(P3)} W at a power factor of 0.85, using P = √3 × 400 × 10 × 0.85. At unity power factor it would be {c(R3 * 4000)} W.')])

# ---------------------------------------------------------------- Motor starting voltage dip
St, z, Pm, eta, pfm, k = 1000.0, 0.06, 110e3, 0.95, 0.87, 6.0
Ssc = St / z
Sst = k * Pm / (eta * pfm) / 1000
dip = Sst / (Ssc + Sst)
assert abs(dip - 0.04572) < 1e-4 and abs(Sst - 798.5) < 0.1
# add a 250 MVA utility fault level at 11 kV and 200 m of 120 mm2 Cu cable
Sutil = 250000.0
Rk, Xk, Lc = 0.19, 0.08, 0.2
Zc = math.hypot(Rk, Xk) * Lc
Scab = 415 ** 2 / Zc / 1000
Ssc_bus = 1 / (1 / Ssc + 1 / Sutil)
dip_bus = Sst / (Ssc_bus + Sst)
Ssc_mot = 1 / (1 / Ssc + 1 / Sutil + 1 / Scab)
dip_mot = Sst / (Ssc_mot + Sst)
# torque at remaining voltage
Tm = (1 - dip_mot) ** 2
# 500 kVA generator, subtransient reactance 15%
Sgen = 500 / 0.15
dip_gen = Sst / (Sgen + Sst)
# minimum transformer for a 10% dip at the bus (infinite grid)
St10 = (Sst * (1 - 0.10) / 0.10) * z
# torque table
tq_rows = ''
for d in (0.05, 0.10, 0.15, 0.20, 0.25):
    tq_rows += f"| {d*100:.0f}% | {(1-d)*100:.0f}% | {(1-d)**2*100:.0f}% |\n"

edit('electrical/motor-starting-voltage-dip', date=U, phrase='motor starting voltage dip calculator',
     intro=("An induction motor draws five to seven times its full-load current when it starts, and that current through the supply impedance pulls the bus voltage down. "
            "This motor starting voltage dip calculator estimates the dip from the motor starting kVA and the transformer short-circuit kVA, using the method in "
            f"[motor starting voltage dip calculation]({IB}motor-starting-voltage-dip-calculation/).\n\n"
            "Electrical designers use it to decide whether a motor can start direct-on-line or needs one of the "
            f"[motor starting methods]({IB}motor-starting-methods-compared/) that limit current."),
     body_add=f'''
## Adding the grid and the motor cable

The default result treats the grid behind the transformer as infinitely strong and ignores the cable. Both are easy to add as extra short-circuit kVA in series, combined like resistors in parallel:

- Utility fault level at the 11 kV side, say 250 MVA = {c(Sutil)} kVA
- 200 m of 120 mm² copper cable at about {Rk} + j{Xk} Ω/km has |Z| = {Zc:.4f} Ω, equal to 415² ÷ {Zc:.4f} = **{c(Scab)} kVA**
- Bus short-circuit capacity = 1 ÷ (1/{c(Ssc)} + 1/{c(Sutil)}) = **{c(Ssc_bus)} kVA**, so the bus dip rises from {dip*100:.2f}% to **{dip_bus*100:.2f}%**
- At the motor terminals, adding the cable gives {c(Ssc_mot)} kVA and a dip of **{dip_mot*100:.1f}%**

The cable more than doubles the dip seen by the motor, which is why long feeders to pump houses and conveyors often need soft starters even when the transformer is large.

## Starting torque at reduced voltage

Induction motor torque varies with the square of the applied voltage, so a modest dip costs much more torque.

| Voltage dip | Voltage remaining | Starting torque remaining |
|---|---|---|
{tq_rows}
In the cable example above the motor keeps about {Tm*100:.0f}% of its rated starting torque. Check that this is still above the load torque at standstill, especially for loaded conveyors, crushers and positive displacement pumps.

## Starting on a generator

A 500 kVA generator with a subtransient reactance of 15% has an effective short-circuit capacity of 500 ÷ 0.15 = {c(Sgen)} kVA. The same 110 kW motor started DOL would dip its output by about **{dip_gen*100:.0f}%**, before the voltage regulator recovers. That is why generator sets feeding large motors are oversized or paired with soft starters.

## Sizing the transformer for a dip limit

Rearranging the formula, the transformer rating that keeps the bus dip at 10% for this motor (infinite grid, Z = 6%) is S<sub>T</sub> = S<sub>start</sub> × (1 − 0.10) ÷ 0.10 × Z% = **{c(St10)} kVA**. Any standard rating above that meets the limit at the bus, but the motor terminal dip must still be checked with the cable included.

## Measuring the dip on site

A power quality analyser set to record half-cycle RMS voltage (the method in IEC 61000-4-30) captures the depth and duration of the dip during a real start. Clamp the current channel on the motor feeder at the same time to confirm the actual starting multiple, which is often lower than the catalogue value on modern high-efficiency motors and higher on older ones.

## Common mistakes

- **Using the motor kW as the starting kVA.** The starting kVA is k × kW ÷ (η × PF), here {c(Sst)} kVA, more than seven times the shaft rating.
- **Comparing the bus dip with a motor terminal limit.** The limit of 10% to 15% applies at the motor; the bus figure leaves out the cable.
- **Ignoring other motors already running.** Running motors slow down and draw more current during the dip, deepening it, and contactors on them may drop out below about 80% voltage.
- **Forgetting the star-delta changeover.** The open transition from star to delta causes a brief current spike that can produce a second dip larger than the first.
- **Using the generator rated power factor of 0.8 as the motor starting PF.** Locked-rotor power factor is only about 0.2 to 0.4.
''',
     faq_add=[('How do I include the cable and the utility fault level in the voltage dip?',
               f'Convert each to short-circuit kVA (cable: V² ÷ |Z|; utility: its fault MVA) and combine them with the transformer as 1 ÷ (1/S₁ + 1/S₂ + 1/S₃). For the default motor, a 250 MVA grid and 200 m of 120 mm² cable raise the motor terminal dip to about {dip_mot*100:.1f}%.'),
              ('How is motor starting voltage dip measured?',
               'With a power quality analyser recording half-cycle RMS voltage at the bus or motor terminals during a start, ideally with a current clamp on the feeder at the same time to record the real starting current.')])

# ---------------------------------------------------------------- kW to amps
Pk, phk, Vk, pfk = 10e3, R3, 415.0, 0.85
Ik = Pk / (phk * Vk * pfk)
assert abs(Ik - 16.367) < 0.001
# motor: 22 kW output, eta 0.92, PF 0.86, 415 V
Pin22 = 22e3 / 0.92
I22 = Pin22 / (R3 * 415 * 0.86)
I22_wrong = 22e3 / (R3 * 415 * 0.86)
# US: 10 kW at 480 V and 208 V three-phase, PF 0.85
I480 = Pk / (R3 * 480 * 0.85)
I208 = Pk / (R3 * 208 * 0.85)
# DC telecom: 3 kW at 48 V
Idc = 3000 / 48
# low voltage on constant power load: 10 kW at 380 V
I380 = Pk / (R3 * 380 * 0.85)
# motor FLC table at 415 V, typical efficiency and PF
mot_rows = ''
for kw, e, p in ((5.5, 0.89, 0.84), (11, 0.91, 0.85), (22, 0.92, 0.86), (37, 0.935, 0.87),
                 (55, 0.94, 0.87), (75, 0.945, 0.88), (110, 0.95, 0.88)):
    i = kw * 1e3 / e / (R3 * 415 * p)
    mot_rows += f"| {kw:g} kW | {e*100:.1f}% | {p:.2f} | {c(kw/e, 1)} kW | {i:.1f} A |\n"

edit_keep_featured('electrical/kw-to-amps', date=U, phrase='kW to amps calculator',
     intro=("The current a load draws decides the breaker, cable and contactor it needs. "
            "This kW to amps calculator converts power to current for DC, single-phase and three-phase supplies, as explained in "
            f"[single-phase vs three-phase power]({IB}single-phase-vs-three-phase-power/).\n\n"
            "Electricians and panel builders use it when they size protection and cables from equipment ratings, following "
            f"[how to calculate three-phase power]({IB}how-to-calculate-three-phase-power/). It also works backwards from a measured current to kW."),
     body_add=f'''
## Worked example

With the default inputs, a 10 kW three-phase load at 415 V and a power factor of 0.85:

- I = P ÷ (√3 × V × PF) = 10,000 ÷ (1.732 × 415 × 0.85) = **{Ik:.2f} A** per line

## Converting a motor rating to amps

A motor nameplate kW is the **shaft output**, so the electrical input is higher by the efficiency. For a 22 kW motor at 415 V with η = 92% and PF = 0.86:

- Electrical input = 22 ÷ 0.92 = {Pin22/1e3:.2f} kW
- Current = {c(Pin22)} ÷ (1.732 × 415 × 0.86) = **{I22:.1f} A**

Entering 22 kW directly would give {I22_wrong:.1f} A, about 8% low. Enter the input kW, or divide the result by the efficiency.

## Typical motor full-load current at 415 V

| Motor output | Efficiency | PF | Input power | Current |
|---|---|---|---|---|
{mot_rows}
These use typical IE2 to IE3 values; the nameplate current of a particular motor can differ by several percent, and it always takes priority.

## North American and DC supplies

The same 10 kW at PF 0.85 draws **{I480:.1f} A** on a 480 V three-phase system and **{I208:.1f} A** on 208 V. On a 48 V DC telecom or battery system, a 3 kW load draws 3,000 ÷ 48 = **{Idc:.1f} A**, which is why DC busbars are so heavy.

## Constant power loads at low voltage

Drives, SMPS and UPS inputs hold their power constant, so current rises when the voltage falls. If the 415 V supply sags to 380 V, the 10 kW load draws {I380:.1f} A instead of {Ik:.1f} A, a {(I380/Ik-1)*100:.0f}% increase. Size cables and breakers for the lowest expected voltage on these loads.

## Common mistakes

- **Taking the motor output kW as input power.** Divide by efficiency first, as shown above.
- **Choosing DC with a power factor below 1.** DC has no power factor; set PF to 1 or the current comes out too high.
- **Using 230 V with the three-phase option on a 400 V system.** The √3 formula needs the line-to-line voltage; 230 V would overstate the current by about 74%.
- **Sizing the breaker exactly at the calculated current.** The breaker must sit above the running current, and the cable must be rated for the breaker, after derating for grouping and temperature.
- **Assuming the result covers starting.** Direct-on-line motors draw 6 to 7 times this current for a few seconds; check the trip curve and voltage dip.
''',
     faq_add=[('How do I convert motor kW to amps?',
               f'Divide the shaft kW by the efficiency to get input power, then use I = P ÷ (√3 × V × PF). A 22 kW motor at 415 V, 92% efficiency and PF 0.86 draws about {I22:.1f} A.'),
              ('Why does current increase when the supply voltage drops?',
               f'For a constant power load such as a drive or UPS, P stays fixed, so I = P ÷ (√3 × V × PF) rises as V falls. A 10 kW load at PF 0.85 draws {Ik:.1f} A at 415 V but {I380:.1f} A at 380 V.')])

# ---------------------------------------------------------------- kVA to kW
S0, pfv = 100.0, 0.8
Pv = S0 * pfv
Qv = math.sqrt(S0 ** 2 - Pv ** 2)
assert abs(Pv - 80) < 1e-9 and abs(Qv - 60) < 1e-9
# current of 100 kVA at 415 V and 400 V
I415 = S0 * 1e3 / (R3 * 415)
I400 = S0 * 1e3 / (R3 * 400)
# adding loads: 50 kVA at 0.8 and 30 kVA at 1.0
P_a, Q_a = 50 * 0.8, 50 * 0.6
P_b, Q_b = 30.0, 0.0
S_sum = math.hypot(P_a + P_b, Q_a + Q_b)
pf_sum = (P_a + P_b) / S_sum
# transformer loading: 1,000 kVA transformer, 720 kW at 0.82
St_tr, P_tr, pf_tr = 1000.0, 720.0, 0.82
S_tr = P_tr / pf_tr
load_tr = S_tr / St_tr
P_tr95 = St_tr * 0.95 * load_tr  # kW at same kVA if pf were 0.95
# kVAr table for 100 kVA
q_rows = ''
for p in (0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99):
    kw = 100 * p
    q = math.sqrt(100 ** 2 - kw ** 2)
    q_rows += f"| {p:.2f} | {math.degrees(math.acos(p)):.1f}° | {kw:g} kW | {q:.1f} kVAr |\n"

edit_keep_featured('electrical/kva-to-kw', date=U, phrase='kVA to kW converter',
     intro=("Apparent power in kVA is what cables, transformers and generators must carry, while real power in kW does the useful work. "
            "This kVA to kW converter applies the power factor to go either way and also gives the reactive power in kVAr, as described in "
            f"[power factor, kW, kVA and kVAr]({IB}power-factor-kw-kva-kvar/).\n\n"
            "Engineers use it to size generators, UPS units and transformers and to read the "
            f"[active, reactive and apparent power]({IB}active-reactive-and-apparent-power/) on a meter."),
     body_add=f'''
## Worked example

With the default inputs, 100 kVA at a power factor of 0.8:

- Real power P = 100 × 0.8 = **{Pv:g} kW**
- Reactive power Q = √(100² − 80²) = **{Qv:g} kVAr**

The 3-4-5 triangle is a handy check: at PF 0.8 the kW, kVAr and kVA are always in the ratio 4 : 3 : 5.

## Reactive power at each power factor (100 kVA)

| PF | Angle φ | kW | kVAr |
|---|---|---|---|
{q_rows}
Below about 0.9 the reactive part grows quickly, which is why a poor power factor loads a transformer far more than its kW suggests.

## From kVA to amps

The current that sets cable and breaker sizes follows from kVA alone, with no power factor: I = S ÷ (√3 × V). For 100 kVA that is **{I415:.0f} A** at 415 V and **{I400:.0f} A** at 400 V.

## Checking transformer loading

A plant drawing {P_tr:g} kW at PF {pf_tr} from a {c(St_tr)} kVA transformer loads it to {c(S_tr)} kVA, or **{load_tr*100:.0f}%**. If the power factor were corrected to 0.95, the same {c(S_tr)} kVA would carry {c(P_tr95)} kW, so correction frees capacity without a new transformer. Read kW, kVA and PF together on the main incomer's multifunction meter or a power analyser; the kVA maximum demand on the electricity bill shows the same thing averaged over the billing period.

## Common mistakes

- **Adding kVA of loads with different power factors directly.** A 50 kVA load at 0.8 PF and a 30 kVA heater at 1.0 PF do not total 80 kVA. Add kW ({P_a + P_b:g}) and kVAr ({Q_a + Q_b:g}) separately: the total is √({P_a + P_b:g}² + {Q_a + Q_b:g}²) = **{S_sum:.1f} kVA** at PF {pf_sum:.2f}.
- **Treating a UPS or inverter VA rating as watts.** A 10 kVA UPS with a 0.9 output PF delivers at most 9 kW.
- **Loading a 0.8 PF generator with unity PF loads up to its kVA.** A 100 kVA set has an engine sized for about 80 kW; heaters totalling 100 kW would overload it.
- **Using displacement PF where harmonics are high.** With drives and rectifiers, true PF is lower than cos φ, so kVA is higher than kW ÷ cos φ suggests.
- **Using the kVAr formula with a PF above 1 or kW above kVA.** Power factor cannot exceed 1; a reading that implies it usually means a wiring or CT polarity error on the meter.
''',
     faq_add=[('How do I add the kVA of loads with different power factors?',
               f'Add the kW and the kVAr separately, then take √(kW² + kVAr²). A 50 kVA load at 0.8 PF plus a 30 kVA load at unity PF totals about {S_sum:.1f} kVA, not 80 kVA.'),
              ('How many amps is 100 kVA?',
               f'On a three-phase supply, I = kVA × 1000 ÷ (√3 × V): about {I415:.0f} A at 415 V or {I400:.0f} A at 400 V. Power factor does not change the current for a given kVA.')])

# ---------------------------------------------------------------- Power factor correction
Pp, pf1, pf2, Vp, fp = 100e3, 0.75, 0.95, 415.0, 50.0
Qc = Pp / 1000 * (math.tan(math.acos(pf1)) - math.tan(math.acos(pf2)))
Cp = Qc * 1000 / 3 / (2 * math.pi * fp * Vp ** 2)
red = 1 - pf1 / pf2
assert abs(Qc - 55.32) < 0.01 and abs(Cp * 1e6 - 340.8) < 0.1 and abs(red - 0.2105) < 1e-4
I1 = Pp / (R3 * Vp * pf1)
I2 = Pp / (R3 * Vp * pf2)
loss_red = 1 - (pf1 / pf2) ** 2
# capacitor rated 440 V used at 415 V
Q440 = 50 * (415 / 440) ** 2
# capacitor needed nameplate at 440 V to give Qc at 415 V
Qname = Qc * (440 / 415) ** 2
# detuned 7%: capacitor voltage rise
Vcap = 415 / (1 - 0.07)
# bill PF
kWh, kVArh = 42000.0, 37000.0
pf_bill = kWh / math.hypot(kWh, kVArh)
# overcorrection at light load: 30 kW at 0.75 with full 55.3 kVAr in service
Ql = 30 * math.tan(math.acos(0.75))
Qnet = Ql - Qc
pf_light = 30 / math.hypot(30, Qnet)
# APFC steps
steps = [5, 10, 15, 15, 20]

edit_keep_featured('electrical/power-factor-correction', date=U, phrase='power factor correction calculator',
     intro=("Motors and other inductive loads draw reactive current that loads cables and transformers without doing useful work. "
            "This power factor correction calculator finds the capacitor kVAr and capacitance needed to raise power factor to a target, using the method in "
            f"[how to calculate capacitor bank kVAr]({IB}how-to-calculate-capacitor-bank-kvar-formula/).\n\n"
            "Plant electrical engineers and panel builders use it to size fixed banks and APFC panels, cut kVA demand charges and avoid low power factor penalties, following "
            f"[capacitor bank sizing for power factor correction]({IB}capacitor-bank-sizing-power-factor-correction/)."),
     body_add=f'''
## Current and loss savings in the example

At 415 V the default 100 kW load draws {I1:.1f} A at PF 0.75 and **{I2:.1f} A** at PF 0.95. Cable and transformer copper losses scale with current squared, so they fall by 1 − (0.75 ÷ 0.95)² = **{loss_red*100:.1f}%**, even though the current itself falls by only {red*100:.0f}%. The capacitance per phase for a delta bank is {Cp*1e6:.1f} µF.

## Finding the present power factor

The best source is the electricity bill or the main incomer meter. Average power factor over a month is kWh ÷ √(kWh² + kVArh²). With {c(kWh)} kWh and {c(kVArh)} kVArh that is **{pf_bill:.3f}**, the default value used here. For kW, take the average demand during working hours rather than the peak, because the bank is sized for the usual operating point.

## Capacitor voltage rating

Capacitor kVAr is quoted at the rated voltage and varies with voltage squared. A 50 kVAr unit rated at 440 V delivers only 50 × (415 ÷ 440)² = **{Q440:.1f} kVAr** on a 415 V system. To get the {Qc:.1f} kVAr calculated here from 440 V units, the total nameplate must be about **{Qname:.1f} kVAr**. In a detuned bank with 7% reactors the capacitor voltage rises to 415 ÷ (1 − 0.07) = {Vcap:.0f} V, so 480 V or higher rated capacitors are used.

## Splitting the bank into APFC steps

An automatic panel switches steps to follow the load. For the {Qname:.0f} kVAr nameplate found above, a five-step panel of {' + '.join(str(s) for s in steps)} = {sum(steps)} kVAr gives {steps[0]} kVAr resolution, fine enough for the relay to hold the target without hunting as machines start and stop. The controller needs a CT on one phase of the incomer, upstream of the capacitor connection, and a voltage reference from the other two phases.

## Common mistakes

- **Leaving a fixed bank on at light load.** If the load drops to 30 kW at PF 0.75 with the full {Qc:.1f} kVAr connected, net reactive power is {Qnet:.1f} kVAr and the power factor becomes {pf_light:.2f} leading, which raises voltage and can be penalised.
- **Ignoring the voltage derating.** Using 440 V capacitors on 415 V without allowing for the {(1-(415/440)**2)*100:.0f}% kVAr loss leaves the bank short.
- **Fitting plain capacitors where drives and UPSs create harmonics.** They can resonate near the 5th or 7th harmonic and fail; use detuned banks.
- **Connecting capacitors to a VFD output.** The switching waveform destroys them and can trip the drive; correct on the supply side only.
- **Placing the APFC CT downstream of the bank.** The relay then never sees the correction and keeps switching steps in.
''',
     faq_add=[('How do I find my power factor from the electricity bill?',
               f'Use kWh ÷ √(kWh² + kVArh²) for the billing period. For {c(kWh)} kWh and {c(kVArh)} kVArh the average power factor is about {pf_bill:.2f}.'),
              ('Does a 440 V capacitor give its full kVAr on a 415 V supply?',
               f'No. kVAr varies with the square of voltage, so a 50 kVAr, 440 V unit gives about {Q440:.1f} kVAr at 415 V. Allow for this when choosing the bank size.')])

print('slice 3 done', inplace.DONE)

# ======================================================================= SECTION _expand_c4.py
"""Expand (2026-11-22), slice 4: cable-voltage-drop, three-phase-motor-power, neutral-current-harmonics,
solar-string-sizing, uart-baud-rate-error. Numbers computed here from each page's default inputs and equations.
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-22'
IB = 'https://www.instrumentationblog.in/'
S3 = math.sqrt(3)


def c(x, d=0):
    return f"{x:,.{d}f}"


def edit_keep_featured(cid, **kw):
    """Lift the featured flag around the edit and restore it unchanged after the updated: line."""
    path = os.path.join(inplace.BASE, cid + '.mdx')
    s = open(path).read()
    line = 'featured: true\n'
    assert s.count(line) == 1, cid
    open(path, 'w').write(s.replace(line, '', 1))
    try:
        n = edit(cid, **kw)
    except Exception:
        open(path, 'w').write(s)
        raise
    t = open(path).read()
    k = t.index('\nupdated: ')
    k = t.index('\n', k + 1) + 1
    open(path, 'w').write(t[:k] + line + t[k:])
    return n


# ---------------------------------------------------------------- Cable voltage drop
k, rho, V, I, L, A = 2.0, 1.72e-8, 230.0, 16.0, 30.0, 2.5
Vd = k * L * I * rho / (A * 1e-6)
pct = Vd / V
assert abs(Vd - 6.605) < 0.001 and abs(pct * 100 - 2.872) < 0.001
# minimum size for 3% and for a 50 m run
Amin = k * L * I * rho / (0.03 * V) * 1e6
Amin50 = k * 50 * I * rho / (0.03 * V) * 1e6
Aal = A * 2.82 / 1.72
# mV/A/m from resistivity versus a 70 degree conductor
mvam20 = k * rho / (A * 1e-6) * 1000
hot = 1 + 0.00393 * 50
Vd70 = Vd * hot
pct70 = Vd70 / V
mvam70 = mvam20 * hot
# maximum one-way length at 16 A, 230 V single phase, copper, at 3% and 5%
len_rows = ''
for a in (1.5, 2.5, 4, 6, 10, 16):
    l3 = 0.03 * V * a * 1e-6 / (k * I * rho)
    l5 = 0.05 * V * a * 1e-6 / (k * I * rho)
    len_rows += f"| {a:g} mm² | {k * rho / (a * 1e-6) * 1000:.2f} | {l3:.0f} m | {l5:.0f} m |\n"
# measured check: load end reads 223.8 V with 230.4 V at the board
Vb, Vl = 230.4, 223.8
dV = Vb - Vl
R_loop = dV / I
R_exp = k * L * rho / (A * 1e-6)

edit_keep_featured('electrical/cable-voltage-drop', date=U, phrase='cable voltage drop calculator',
     intro=("Every cable has resistance, so part of the supply voltage is lost before it reaches the load, and wiring rules usually cap that loss at about 3% to 5%. "
            "This cable voltage drop calculator works out the drop for single phase or three phase copper and aluminium runs, or the smallest cross-section that meets your limit.\n\n"
            "Electricians and designers use it when planning long final circuits and motor feeders, following the method in this "
            f"[voltage drop calculation]({IB}voltage-drop-calculation/) guide."),
     body_add=f'''
## Sizing the cable for a 3% limit

The default circuit, 16 A over 30 m of 2.5 mm² copper at 230 V, drops **{Vd:.2f} V ({pct*100:.2f}%)**. Working backwards for a 3% lighting limit:

- A<sub>min</sub> = 2 × 30 × 16 × 1.72 × 10⁻⁸ ÷ (0.03 × 230) = **{Amin:.2f} mm²**, so 2.5 mm² just passes
- Stretch the same run to 50 m and A<sub>min</sub> becomes **{Amin50:.2f} mm²**, which means 4 mm²
- Current rating is checked separately, as in [choosing cable size for load current]({IB}cable-size-for-load-current/), and the larger of the two sizes wins
- In aluminium the same drop needs 2.5 × 2.82 ÷ 1.72 = **{Aal:.2f} mm²**, so the next standard size, 6 mm²

## Maximum run length at 16 A, 230 V, copper

| Size | Loop mV/A/m at 20 °C | Max length for 3% | Max length for 5% |
|---|---|---|---|
{len_rows}
These lengths scale inversely with current: at 32 A each one halves.

## Why datasheet mV/A/m values are higher

From resistivity alone, 2.5 mm² twin cable gives {mvam20:.2f} mV/A/m. Wiring regulation tables quote about 18 mV/A/m because they assume the conductor is at its 70 °C operating temperature. Correcting the default example by 1 + 0.00393 × 50 = {hot:.3f} raises the drop to **{Vd70:.2f} V ({pct70*100:.2f}%)**, which now fails a 3% limit. Use the hot value for cables that run near their rated current and the 20 °C value only for lightly loaded runs.

## Checking voltage drop on site

Measure the voltage at the distribution board and at the far end at the same moment, with the load running. If the board reads {Vb} V and the socket reads {Vl} V at 16 A, the drop is {dV:.1f} V and the loop resistance is {dV:.1f} ÷ 16 = **{R_loop:.3f} Ω**, against {R_exp:.3f} Ω expected for 60 m of 2.5 mm² conductor. A reading well above the calculated value usually points to a loose terminal or a longer route than drawn. A low-resistance ohmmeter on the dead circuit (an R1 + R2 style test) gives the same figure without load.

## Common mistakes

- **Entering the total conductor length.** L is the one-way route length; the factor 2 or √3 already accounts for the return path.
- **Using 3% from the board instead of from the origin.** The limit usually applies from the supply origin, so the submain drop must be added to the final circuit drop.
- **Using phase voltage for a three phase run.** With the √3 factor, compare the drop against the line voltage (400 V or 415 V), not 230 V.
- **Ignoring motor starting current.** A motor drawing 6 times its running current gives 6 times the drop during start, which can stall contactors.
- **Applying the resistive formula to large cables.** Above about 25 mm² reactance becomes significant and the manufacturer's mV/A/m (r and x) values give a more accurate answer.
''',
     faq_add=[('Why do cable tables give a higher voltage drop than my calculation?',
               f'Tables use resistance at the 70 °C operating temperature, about {hot:.2f} times the 20 °C value used here. For 16 A over 30 m of 2.5 mm² copper the drop rises from {Vd:.2f} V to about {Vd70:.2f} V.'),
              ('How far can I run 2.5 mm² cable at 16 A?',
               f'At 230 V single phase with copper at 20 °C, about {0.03*V*2.5e-6/(k*I*rho):.0f} m one way for a 3% drop and {0.05*V*2.5e-6/(k*I*rho):.0f} m for 5%. Allow less if the cable runs warm.')])

# ---------------------------------------------------------------- Three phase motor power
V, pf, eta, Pout = 415.0, 0.85, 0.90, 11.0
Pin = Pout / eta
Iflc = Pin * 1000 / (S3 * V * pf)
assert abs(Iflc - 20.005) < 0.01
S = S3 * V * Iflc / 1000
Q = math.sqrt(S ** 2 - Pin ** 2)
loss = Pin - Pout
# measured current case: clamp reads 14.2 A, analyser shows pf 0.78
Im, pfm = 14.2, 0.78
Pin_m = S3 * V * Im * pfm / 1000
Pout_m = Pin_m * eta
load_m = Pout_m / Pout
# IE efficiency classes, 11 kW 4 pole 50 Hz (IEC 60034-30-1)
ie = [('IE1', 87.6), ('IE2', 89.8), ('IE3', 91.4), ('IE4', 93.3)]
hours = 6000
ie_rows = ''
for name, e in ie:
    pi_ = Pout / (e / 100)
    ii = pi_ * 1000 / (S3 * V * pf)
    ie_rows += f"| {name} | {e:.1f}% | {pi_:.2f} kW | {ii:.1f} A | {(pi_ - Pout):.2f} kW | {(pi_ - Pout) * hours:,.0f} kWh |\n"
e1 = Pout / 0.876 - Pout
e3 = Pout / 0.914 - Pout
save = (e1 - e3) * hours
hp = Pout / 0.7457

edit_keep_featured('electrical/three-phase-motor-power', date=U, phrase='three-phase motor power calculator',
     intro=("A motor nameplate gives shaft output in kW, but the supply also has to cover the motor's losses and its reactive current, so the line current is higher than the kW figure suggests. "
            "This three-phase motor power calculator links line voltage, current, power factor and efficiency to input and output power.\n\n"
            "Electricians, maintenance engineers and panel designers use it to estimate "
            f"[motor full-load current (FLC)]({IB}motor-full-load-current-flc/) for cables and protection, or to judge how loaded a running motor is."),
     body_add=f'''
## Apparent and reactive power for the default motor

For the 11 kW, 415 V motor at full load the calculator gives P<sub>in</sub> = **{Pin:.2f} kW** and I = **{Iflc:.2f} A**. The same figures give:

- Apparent power S = √3 × 415 × {Iflc:.2f} = **{S:.2f} kVA**
- Reactive power Q = √({S:.2f}² − {Pin:.2f}²) = **{Q:.2f} kVAr**
- Losses inside the motor = {Pin:.2f} − 11 = **{loss:.2f} kW**, all turned into heat

The kVA figure is what a generator or transformer must supply, and the kVAr figure is what a capacitor bank would have to cancel to bring the power factor to unity.

## Estimating load from a measured current

Leave P<sub>out</sub> blank and enter a measured current instead. If a clamp meter reads **{Im} A** and a power analyser shows a power factor of **{pfm}**, the input power is √3 × 415 × {Im} × {pfm} = **{Pin_m:.2f} kW** and the shaft output is about **{Pout_m:.2f} kW**, roughly {load_m*100:.0f}% of rating. Enter the measured power factor rather than the nameplate value, because at part load the power factor falls a lot while current falls only a little. Judging load from current alone with the full-load pf would overstate it.

## Efficiency class and current for an 11 kW, 4-pole motor

| Class (IEC 60034-30-1) | Efficiency | Input power | Current at pf 0.85 | Losses | Losses over {hours:,} h |
|---|---|---|---|---|---|
{ie_rows}
Changing an IE1 motor for IE3 on a {hours:,} h duty saves about **{save:,.0f} kWh** a year. The current changes by well under 1 A from one class to the next, so efficiency upgrades rarely change cable or breaker sizes.

## Measuring motor power on site

A clamp meter on one phase gives current only; to get kW you need voltage and power factor as well, which a three-phase power analyser measures directly on all three phases. Check that the three phase currents agree within a few percent: a larger imbalance usually means unbalanced supply voltages, which heat the motor far more than the current difference suggests. For hp ratings, 11 kW is about {hp:.1f} hp (1 hp = 0.7457 kW).

## Common mistakes

- **Using phase voltage in the √3 formula.** V is the line-to-line voltage (415 V), not the 240 V phase voltage; using 240 V overstates current by √3.
- **Forgetting efficiency.** Dividing 11 kW by √3 × V × pf alone gives {Pout*1000/(S3*V*pf):.1f} A, about 10% low, because the shaft kW is not the electrical input.
- **Taking full-load pf for a lightly loaded motor.** A motor at 40% load may run at pf 0.6, so current based estimates of kW must use the measured pf.
- **Sizing protection on FLC alone.** Direct-on-line starting at 6 to 8 times FLC must ride through the breaker curve without tripping.
- **Reading the hp value as input power.** Nameplate hp, like kW, is shaft output on IEC and NEMA motors.
''',
     faq_add=[('How do I estimate how much load a running motor has?',
               f'Measure line current and power factor, work out P = √3 × V × I × pf, then multiply by efficiency. At 415 V, {Im} A and pf {pfm} give about {Pin_m:.1f} kW input and {Pout_m:.1f} kW at the shaft for this 11 kW motor.'),
              ('Does a higher efficiency motor draw noticeably less current?',
               f'Only slightly. For 11 kW at 415 V and pf 0.85, IE1 draws about {Pout/0.876*1000/(S3*V*pf):.1f} A and IE3 about {Pout/0.914*1000/(S3*V*pf):.1f} A. The real gain is lower losses, around {save:,.0f} kWh over {hours:,} running hours.')])

# ---------------------------------------------------------------- Neutral current with harmonics
I, h3 = 100.0, 0.30
I1 = I / math.sqrt(1 + h3 ** 2)
I3 = h3 * I1
In = 3 * I3
h3r = I3 / I
Ides = I / 0.86
assert abs(In - 86.205) < 0.001 and abs(Ides - 116.28) < 0.01
# crossover where neutral equals phase current
hx = 1 / math.sqrt(8)
# unbalanced example: fundamental 100, 90, 80 A, third harmonic 30% of each fundamental
ph = [100.0, 90.0, 80.0]
ang = [0, -120, 120]
nx = sum(a * math.cos(math.radians(t)) for a, t in zip(ph, ang))
ny = sum(a * math.sin(math.radians(t)) for a, t in zip(ph, ang))
In1_u = math.hypot(nx, ny)
In3_u = 0.30 * sum(ph)
In_u = math.hypot(In1_u, In3_u)
# heating table: neutral I^2R relative to one phase conductor of the same size
heat_rows = ''
for h in (0.10, 0.20, 0.30, 0.3536, 0.40, 0.50, 0.70):
    i1 = I / math.sqrt(1 + h ** 2)
    r = 3 * h * i1 / I
    heat_rows += f"| {h*100:.1f}% | {r:.2f} | {r**2:.2f} |\n"
# total cable heat, four-core: 3 phases + neutral, relative to 3 phases alone
heat_tot = 1 + (In / I) ** 2 / 3

edit('electrical/neutral-current-harmonics', date=U, phrase='neutral current calculator',
     intro=("In a balanced three phase circuit the 50 Hz currents cancel in the neutral, but third harmonic currents are in phase and add, so a neutral feeding LED lighting or IT loads can carry more than the phases. "
            "This neutral current calculator finds that current and the IEC 60364-5-52 design current.\n\n"
            "Electrical designers and power quality engineers use it to size neutrals and four-core cables, as covered in "
            f"[neutral conductor sizing with harmonics]({IB}neutral-conductor-sizing-harmonics/)."),
     body_add=f'''
## When the neutral overtakes the phase

The neutral current equals the phase current when 3h ÷ √(1 + h²) = 1, which solves to h = 1 ÷ √8 = **{hx*100:.1f}%** of the fundamental. Above that the neutral is the most heavily loaded conductor in the cable. In the default case (30%) the neutral carries **{In:.1f} A** against 100 A on each phase, and the total heat in the four-core cable is about {heat_tot:.2f} times that of the three phases alone, which is why the IEC factor of 0.86 raises the design current to **{Ides:.1f} A**.

## Neutral heating relative to a phase conductor

For a neutral of the same cross-section as the phases, its I²R heating compared with one phase conductor:

| 3rd harmonic (% of fundamental) | I<sub>N</sub> ÷ I | Neutral heat ÷ phase heat |
|---|---|---|
{heat_rows}
Heating rises with the square of current, so a neutral carrying 1.34 times phase current runs about 1.8 times as hot in watts.

## Unbalance and harmonics together

Real panels are never perfectly balanced. Suppose the fundamental currents are 100, 90 and 80 A, each with 30% third harmonic. The 50 Hz parts no longer cancel and leave **{In1_u:.1f} A** in the neutral, while the third harmonics add arithmetically to 0.3 × 270 = **{In3_u:.0f} A**. Because the two are at different frequencies they combine as a root sum of squares: √({In1_u:.1f}² + {In3_u:.0f}²) = **{In_u:.1f} A**. The unbalance adds less than you might expect, so the harmonic content dominates the neutral sizing.

## Measuring neutral current

Use a true RMS clamp meter directly on the neutral; an average responding meter can read 30% or more low on distorted current. A power quality analyser logging over a working day shows both the RMS neutral current and the 150 Hz (or 180 Hz) component, and the peak period is the one that matters for cable temperature. A neutral reading higher than any phase is the clearest sign that triplen harmonics are present.

## Common mistakes

- **Entering the harmonic as a share of RMS instead of fundamental.** Analysers normally show % of fundamental; the calculator converts it to the IEC basis for you.
- **Using a half-size neutral on LED or IT circuits.** Reduced neutrals are only acceptable when the third harmonic is low and the load is balanced.
- **Relying on phase overcurrent protection.** Breakers on the phases do not see neutral overload; IEC 60364 may require neutral current detection when it can exceed the phase current.
- **Assuming 5th and 7th harmonics add.** Only triplen orders add in the neutral; the others raise phase RMS but cancel.
- **Measuring at light load.** Percentages look high when the fundamental is small, so size on full load amps.
''',
     faq_add=[('At what third harmonic level does the neutral current exceed the phase current?',
               f'At about {hx*100:.1f}% of the fundamental, which is 33.3% of the phase RMS current. Beyond that the neutral is the most heavily loaded conductor and IEC 60364-5-52 sizes the cable on the neutral current.'),
              ('How do load unbalance and third harmonics combine in the neutral?',
               f'Add the 50 Hz unbalance current and the triplen current as a root sum of squares. Phases of 100, 90 and 80 A with 30% third harmonic give about {In1_u:.1f} A and {In3_u:.0f} A, so roughly {In_u:.0f} A in the neutral.')])

# ---------------------------------------------------------------- Solar string sizing
Voc, Vmp, bv, bm, Tmin, Thot, N = 49.5, 41.6, -0.27, -0.35, 0.0, 70.0, 16
Vmax, Vlo, Vhi = 1000.0, 200.0, 850.0
Vocc = Voc * (1 + bv / 100 * (Tmin - 25))
Vmph = Vmp * (1 + bm / 100 * (Thot - 25))
Vmpc = Vmp * (1 + bm / 100 * (Tmin - 25))
Nmax = math.floor(Vmax / Vocc)
Nmppt = math.floor(Vhi / Vmpc)
Nmin = math.ceil(Vlo / Vmph)
SVoc, SVmp = N * Vocc, N * Vmph
assert (Nmax, Nmppt, Nmin) == (18, 18, 6) and abs(SVoc - 845.46) < 0.01 and abs(SVmp - 560.768) < 0.001
# NOCT estimate of hot cell temperature
Tamb, NOCT, G = 45.0, 45.0, 1000.0
Tcell = Tamb + (NOCT - 20) / 800 * G
Vmp_t = Vmp * (1 + bm / 100 * (Tcell - 25))
# hot cell table for MPPT minimum 200 V and 550 V start
hot_rows = ''
for T in (50, 60, 70, 76.25, 85):
    v = Vmp * (1 + bm / 100 * (T - 25))
    hot_rows += f"| {T:g} °C | {v:.2f} V | {math.ceil(200 / v)} | {math.ceil(550 / v)} | {N * v:.0f} V |\n"
# current check with a datasheet Isc of 13.9 A, two strings on one MPPT, 1.25 factor
Isc, ns, Imax = 13.9, 2, 36.0
Ides = Isc * 1.25 * ns
# field Voc test at 15 degree cell temperature
Tf = 15.0
Vf = N * Voc * (1 + bv / 100 * (Tf - 25))
Vlow = Vf * 0.97

edit('electrical/solar-string-sizing', date=U, phrase='solar string sizing calculator',
     intro=("A PV string must stay below the inverter's maximum DC voltage on the coldest morning and above the MPPT minimum on the hottest afternoon. "
            "This solar string sizing calculator corrects module Voc and Vmp for temperature and gives the longest and shortest allowed string.\n\n"
            "Solar designers and installers use it when matching modules to an inverter, as the voltage check within "
            f"[solar PV system sizing]({IB}solar-pv-system-sizing-calculation/), and when checking a quotation before work starts."),
     body_add=f'''
## Estimating the hot cell temperature

If you only know the site's maximum ambient temperature, the NOCT method gives a cell temperature: T<sub>cell</sub> = T<sub>amb</sub> + (NOCT − 20) ÷ 800 × G. For a 45 °C afternoon, NOCT 45 °C and 1,000 W/m² this gives **{Tcell:.2f} °C**, a little above the default 70 °C. At that temperature the module Vmp falls to **{Vmp_t:.2f} V**, still giving a minimum of {math.ceil(200 / Vmp_t)} modules for the 200 V MPPT floor. Roof mounted arrays with little rear ventilation can run 5 to 10 °C hotter than this estimate.

## Hot cell temperature and minimum string length

| Cell temperature | Module Vmp | Min modules (200 V MPPT) | Min modules (550 V start) | 16-module string Vmp |
|---|---|---|---|---|
{hot_rows}
Some string inverters need several hundred volts before they start or reach full power, so the minimum is often set by the start-up or full-power voltage rather than the MPPT minimum.

## Checking the current side

Voltage is only half the match. With a module I<sub>sc</sub> of {Isc} A and {ns} parallel strings on one MPPT input, the design current is {Isc} × 1.25 × {ns} = **{Ides:.2f} A**. That must not exceed the inverter's maximum short circuit input current per MPPT (for example {Imax:g} A). Extra parallel strings need their own MPPT input or string fuses.

## Testing a string after installation

Before connecting the inverter, measure each string's open circuit voltage with a PV rated meter or string tester and note the module temperature. At a cell temperature of {Tf:g} °C the 16-module default string should read about 16 × 49.5 × (1 + 0.0027 × 10) = **{Vf:.1f} V**. A string reading one module's worth low (about 50 V) has a reversed or missing module; a reading a few percent low across all strings usually means the modules are warmer than you assumed.

## Common mistakes

- **Using the average winter low.** The cold case must use the record or design minimum, because one frosty morning above the inverter limit can damage it.
- **Mixing up the Voc and Pmax coefficients.** β<sub>Voc</sub> (around -0.27 %/°C) is smaller than the Pmax coefficient; using the wrong one changes N<sub>max</sub>.
- **Rounding N<sub>max</sub> up.** {Vmax:g} ÷ {Vocc:.2f} = {Vmax/Vocc:.2f}, so the answer is {Nmax}, never {Nmax+1}.
- **Designing exactly to the MPPT minimum.** Ageing of about 0.5% a year and soiling lower Vmp, so leave a margin on the short-string side.
- **Forgetting the sign of the coefficient.** Entering +0.27 instead of -0.27 makes Voc fall in the cold and gives an unsafe string length.
''',
     faq_add=[('What Voc should a new string read during commissioning?',
               f'The temperature corrected sum of the module Voc values. For 16 modules of 49.5 V at a {Tf:g} °C cell temperature and -0.27 %/°C, expect about {Vf:.0f} V; a string about 50 V low has a faulty or reversed module.'),
              ('How do I estimate cell temperature if I only know ambient?',
               f'Use T_cell = T_amb + (NOCT - 20) ÷ 800 × G. With 45 °C ambient, NOCT 45 °C and 1,000 W/m² the cells reach about {Tcell:.0f} °C.')])

# ---------------------------------------------------------------- UART baud rate error
f, b, os_ = 16e6, 115200.0, 16


def uart(f, b, o):
    n = max(1, round(f / (o * b)))
    a = f / (o * n)
    return n, a, (a - b) / b


Nd, bad, errd = uart(f, b, os_)
assert Nd == 9 and abs(bad - 111111.1) < 0.1 and abs(errd * 100 + 3.55) < 0.01
N8, ba8, e8 = uart(f, b, 8)
# fractional divider (STM32 style BRR with 16x: USARTDIV = f / baud, rounded to 1/16)
div = f / (16 * b)
div_f = round(div * 16) / 16
ba_f = f / (16 * div_f)
e_f = (ba_f - b) / b
# receiver tolerance for 8-N-1 (10 bits, stop bit centre 9.5 bits after start edge)
tol16 = (0.5 - 1 / 16) / 9.5
tol8 = (0.5 - 1 / 8) / 9.5
tbit_ideal = 1e6 / b
tbit_act = 1e6 / bad
drift = 9.5 * (tbit_act - tbit_ideal) / tbit_ideal
# 115,200 baud error for common clocks
clk_rows = ''
for mhz in (1, 4, 8, 12, 14.7456, 16, 20, 24):
    _, _, a16 = uart(mhz * 1e6, b, 16)
    _, _, a8 = uart(mhz * 1e6, b, 8)
    clk_rows += f"| {mhz:g} MHz | {a16*100:+.2f}% | {a8*100:+.2f}% |\n"

edit('electronics/uart-baud-rate-error', date=U, phrase='UART baud rate error calculator',
     intro=("A UART makes its bit clock by dividing the system clock by a whole number, so the real baud rate is rarely exactly the one you asked for. "
            "This UART baud rate error calculator finds the nearest divisor, the actual rate and the percentage error.\n\n"
            "Embedded firmware engineers use it when choosing crystals and register settings, and when debugging garbled serial data, following "
            f"[UART frame format and baud rate]({IB}uart-communication-frame-baud-rate/)."),
     body_add=f'''
## Fixing the default example

With a 16 MHz clock, 115,200 baud and 16× oversampling the calculator gives N = **{Nd}**, an actual rate of **{bad:,.0f} bit/s** and an error of **{errd*100:.2f}%**. Three ways to bring it down:

- **8× double speed mode:** N = round(16,000,000 ÷ (8 × 115,200)) = {N8}, so {ba8:,.0f} bit/s and **{e8*100:+.2f}%** (on AVR, set U2X and UBRR = {N8-1})
- **Fractional divider:** a UART that divides in sixteenths uses {div_f:.4f} instead of {Nd}, giving {ba_f:,.0f} bit/s and **{e_f*100:+.3f}%**
- **Baud rate crystal:** 14.7456 MHz or 11.0592 MHz divides exactly, so the error is 0%

## How much error a receiver tolerates

The receiver syncs on the falling edge of the start bit and then samples each bit in its centre. In an 8-N-1 frame the last sample, in the stop bit, falls 9.5 bit times after that edge. The accumulated timing slip must stay under half a bit, less the uncertainty in detecting the start edge (one sample period). That gives a total budget of (0.5 − 1/16) ÷ 9.5 = **{tol16*100:.2f}%** with 16× oversampling and **{tol8*100:.2f}%** with 8×. The budget is shared by both ends, so a link where the transmitter is +2% and the receiver -2% is already at the edge. The default {errd*100:.2f}% error slips {abs(drift):.2f} of a bit by the stop bit, which leaves little margin for the other device's clock error.

## 115,200 baud error for common clocks

| Clock | 16× oversampling | 8× oversampling |
|---|---|---|
{clk_rows}
## Measuring the real baud rate

Put an oscilloscope or logic analyser on the TX line and send the character 0x55 ('U'), which produces alternating bits. Measure the width of one bit: at 115,200 baud it should be {tbit_ideal:.2f} µs, while the default 16 MHz setting gives {tbit_act:.2f} µs. Measuring across all ten bits of the frame averages out trigger jitter and gives a more precise result.

## Common mistakes

- **Writing N into a register that expects N − 1.** AVR UBRR and many other dividers are offset by one, which shifts the rate by a whole step.
- **Using the core clock instead of the peripheral clock.** On many microcontrollers the UART runs from a prescaled bus clock, so the divisor is wrong by the prescaler ratio.
- **Trusting an internal RC oscillator at high baud rates.** Its own tolerance of 1% to 2% adds to the divisor error.
- **Checking only one end.** A PC USB adapter and a microcontroller each have errors, and only their difference matters.
- **Forgetting longer frames.** With 9 data bits or parity the stop bit sits later in the frame, so the allowed error is smaller.
''',
     faq_add=[('Is 8x double speed mode always more accurate?',
               f'Not always. It halves the divisor step, which can help ({e8*100:+.2f}% instead of {errd*100:.2f}% at 16 MHz and 115,200 baud), but the receiver tolerance falls from about {tol16*100:.1f}% to {tol8*100:.1f}% because each sample covers a larger part of the bit.'),
              ('How can I measure the actual baud rate of a device?',
               f'Send 0x55 and measure one bit width with a scope or logic analyser, then take baud = 1 ÷ bit time. At 115,200 baud a bit lasts {tbit_ideal:.2f} µs; a 16 MHz AVR in normal mode produces {tbit_act:.2f} µs.')])

print('slice 4 done', inplace.DONE)

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-22), slice 5: resistor-color-code, dbm-to-watts, battery-charge-time, strain-gauge, rc-phase-shift-oscillator.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math, cmath
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-22'
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


def ohm(r):
    if r >= 1e6:
        return f"{r/1e6:g} MΩ"
    if r >= 1e3:
        return f"{r/1e3:g} kΩ"
    return f"{r:g} Ω"


# ---------------------------------------------------------------- Resistor colour code
COL = ['Black', 'Brown', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Violet', 'Grey', 'White']
b1, b2, m, tol = 1, 0, 100, 0.05
R0 = (10 * b1 + b2) * m
assert R0 == 1000 and abs(R0 * (1 - tol) - 950) < 1e-9 and abs(R0 * (1 + tol) - 1050) < 1e-9
# worked example: yellow violet orange gold
Rw = (10 * 4 + 7) * 1000
Rw_lo, Rw_hi = Rw * 0.95, Rw * 1.05
# 5-band: brown black black brown brown = 100 x 10 = 1 kOhm 1%
R5 = (100 * 1 + 0 * 10 + 0) * 10
# measured check: 0.987 kOhm reading on a 1 k 5% part
meas = 987.0
dev = (meas - R0) / R0 * 100
# E12 decade 1k to 8.2k with bands
e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]
e12_rows = ''
for v in e12:
    r = v * 1000
    d = round(v * 10)
    e12_rows += f"| {ohm(r)} | {COL[d // 10]}, {COL[d % 10]}, Red | {c(r*0.9)} to {c(r*1.1)} Ω |\n"
# reversed reading trap: brown black red read backwards (red black brown) = 20 x 10 = 200
Rrev = (10 * 2 + 0) * 10

edit('electronics/resistor-color-code', date=U, phrase='resistor color code calculator',
     intro=("Most through-hole resistors are too small to print a value on, so coloured bands show their resistance and tolerance instead. "
            "This resistor color code calculator turns four bands into a value with its tolerance range; the [resistor color code guide](https://www.instrumentationblog.in/resistor-color-code-guide/) explains the system.\n\n"
            "Students, hobbyists and repair technicians use it when sorting parts bins, checking a board against its schematic or confirming a value before soldering it in."),
     body_add=f'''
## Worked example

A resistor reads **yellow, violet, orange, gold**:

- Digits: yellow = 4, violet = 7, giving 47
- Multiplier: orange = × 1,000, so R = 47 × 1,000 = **{ohm(Rw)}**
- Tolerance: gold = ±5%, so the part can measure anywhere from **{c(Rw_lo)} Ω to {c(Rw_hi)} Ω**

With the calculator defaults (brown, black, red, gold) the value is {ohm(R0)} and the range is {c(R0*(1-tol))} Ω to {c(R0*(1+tol))} Ω. A multimeter reading of {c(meas)} Ω is {dev:.1f}% low, well inside the band.

## E12 values in the 1 kΩ decade

Every value below uses a red multiplier band. Move one colour up the multiplier scale (orange) for the 10 kΩ decade, or down (brown) for 100 Ω.

| Value | Bands 1 to 3 | Range at ±10% |
|---|---|---|
{e12_rows}
## Reading 5-band and 6-band parts

Precision resistors use three digit bands. Brown, black, black, brown, brown reads 100 × 10 = **{ohm(R5)}** at ±1%. A sixth band, when present, gives the temperature coefficient: brown is 100 ppm/K, red 50 ppm/K, yellow 25 ppm/K. On a 5-band part the tolerance band is often set slightly apart from the others, which is the most reliable clue to the reading direction.

## Checking a value in practice

Colours fade and shift with heat, so a brown that has been run hot can look orange or red. When in doubt, measure the part out of circuit, or lift one leg, because parallel paths on the board pull an in-circuit reading low. Hold the probes on the leads rather than with your fingers on both, since skin resistance in parallel affects readings above about 100 kΩ. Blue body resistors are usually metal film (±1% or better) and beige bodies are usually carbon film (±5%), which helps you tell a 4-band from a 5-band part at a glance.

## Common mistakes

- **Reading from the wrong end.** Brown, black, red read backwards is red, black, brown, which decodes to {ohm(Rrev)} instead of {ohm(R0)}.
- **Treating a gold third band as a digit.** Gold in the multiplier position means × 0.1, so yellow, violet, gold is 4.7 Ω, not 470 Ω.
- **Confusing red and orange, or violet and grey,** under warm workshop lighting. Use a white light and compare against a known part.
- **Assuming 4 bands means 4 significant figures.** Only the first two bands are digits; the third is always the multiplier.
- **Ignoring tolerance when matching parts.** Two 5% resistors marked 1 kΩ can differ by up to 100 Ω, which matters in dividers and bridges.
''',
     faq_add=[('What does a resistor with a single black band mean?',
               'It is a zero ohm link, used as a jumper that pick-and-place machines can fit like a resistor. It measures a few milliohms and is rated by current, not resistance.'),
              ('What does the sixth band on a resistor mean?',
               'It gives the temperature coefficient, how much the value drifts per kelvin. Brown is 100 ppm/K, red 50 ppm/K and yellow 25 ppm/K, so a 10 kΩ brown-coded part moves about 1 Ω per kelvin.')])

# ---------------------------------------------------------------- dBm to watts
def dbm2w(d):
    return 10 ** (d / 10) / 1000


def w2dbm(p):
    return 10 * math.log10(p * 1000)


d0 = 20.0
P0 = dbm2w(d0)
dbw0 = d0 - 30
V0 = math.sqrt(P0 * 50)
assert abs(P0 - 0.1) < 1e-12 and dbw0 == -10 and abs(V0 - 2.2360680) < 1e-6
# watts to dBm: 4 W radio
P4 = 4.0
d4 = w2dbm(P4)
# link budget with cable losses
tx, gt, cl1, fspl, gr, cl2 = 20.0, 6.0, 1.5, 90.0, 3.0, 1.0
rx = tx + gt - cl1 - fspl + gr - cl2
rx_w = dbm2w(rx)
sens = -85.0
margin = rx - sens
# two equal signals
both = w2dbm(2 * P0)
# 75 ohm voltage at default
V75 = math.sqrt(P0 * 75)
# peak voltage
Vpk = V0 * math.sqrt(2)
# rule of thumb table
rt_rows = ''
for dd in (1, 3, 6, 10, 20, 30):
    rt_rows += f"| +{dd} dB | × {10**(dd/10):,.3g} | {c(dbm2w(d0+dd)*1000, 1)} mW |\n"

edit('electronics/dbm-to-watts', date=U, phrase='dbm to watts converter',
     intro=("dBm expresses power in decibels relative to 1 milliwatt, so RF and optical levels spanning many orders of magnitude become small numbers you can add and subtract. "
            "This dBm to watts converter works both ways and shows the voltage in a 50 Ω system; see [decibels in electronics: dB and dBm](https://www.instrumentationblog.in/decibel-in-electronics-db-dbm/).\n\n"
            "RF engineers, radio amateurs and fibre technicians use it to read power meters, check transmitter ratings and build link budgets."),
     body_add=f'''
## Worked example

At the default **{d0:g} dBm**:

- P = 10<sup>{d0:g}/10</sup> ÷ 1,000 = **{c(P0*1000)} mW** ({P0:g} W)
- dBW = {d0:g} − 30 = **{dbw0:g} dBW**
- V = √({P0:g} × 50) = **{V0:.3f} V RMS**, or {Vpk:.3f} V peak

Going the other way, a handheld radio rated at {P4:g} W puts out 10 × log₁₀({c(P4*1000)}) = **{d4:.2f} dBm**.

## Link budget with cable losses

A 2.4 GHz point to point link: transmitter {tx:g} dBm, antenna gain {gt:g} dBi, cable loss {cl1:g} dB, free space loss {fspl:g} dB, receive antenna {gr:g} dBi, receive cable {cl2:g} dB.

- Received = {tx:g} + {gt:g} − {cl1:g} − {fspl:g} + {gr:g} − {cl2:g} = **{rx:g} dBm**
- That is {rx_w*1e12:,.1f} pW, about {rx_w*1e9:.4f} nW
- Against a receiver sensitivity of {sens:g} dBm the fade margin is **{margin:g} dB**

## Decibel steps from 20 dBm

| Change | Power ratio | Result |
|---|---|---|
{rt_rows}
Every 3 dB doubles the power and every 10 dB multiplies it by ten, so most conversions can be done in your head once these steps are familiar.

## How RF power is measured

A thermal or diode power sensor on an RF power meter reads average power directly in dBm and is the reference for transmitter checks. A spectrum analyser shows the level of each signal on screen, usually in dBm with a 50 Ω input. High power transmitters are measured through a calibrated attenuator or directional coupler, and its value is added back: a meter reading 6 dBm through a 30 dB attenuator means the source delivers 36 dBm, about 4 W.

## Common mistakes

- **Adding two dBm values directly.** Two {d0:g} dBm signals combine to {both:.2f} dBm, not {2*d0:g} dBm; convert to milliwatts, add, then convert back.
- **Mixing dB and dBm.** A gain or loss is in dB; only an absolute power is in dBm.
- **Using the 50 Ω voltage in a 75 Ω system.** Cable TV uses 75 Ω, where {d0:g} dBm is {V75:.3f} V, not {V0:.3f} V.
- **Comparing peak and average power.** Pulsed radar and OFDM signals have peak power several dB above the average a thermal meter shows.
- **Forgetting the attenuator or coupler factor** when reading a transmitter through a test setup.
''',
     faq_add=[('What is the total power of two signals of the same dBm?',
               f'Double the milliwatts, which adds 3.01 dB. Two {d0:g} dBm signals of {c(P0*1000)} mW each total 200 mW, which is {both:.2f} dBm.'),
              ('How do I convert dBm to volts in a 75 Ω system?',
               f'Use V = √(P × 75) with P in watts. At {d0:g} dBm (0.1 W) that gives {V75:.3f} V RMS, compared with {V0:.3f} V in a 50 Ω system.')])

# ---------------------------------------------------------------- Battery charging time
C0, I0, s0, s1, eta0 = 150.0, 15.0, 0.20, 1.00, 0.80
Ah0 = C0 * (s1 - s0)
t0 = Ah0 / (I0 * eta0)
cr0 = I0 / C0
assert abs(Ah0 - 120) < 1e-9 and abs(t0 - 10) < 1e-9 and abs(cr0 - 0.1) < 1e-12
eta_rows = ''
for name, e in (('Flooded / tubular lead-acid', 0.80), ('AGM / gel lead-acid', 0.85), ('LiFePO4 / Li-ion', 0.95)):
    eta_rows += f"| {name} | {e*100:.0f}% | {Ah0/(I0*e):.2f} h | {Ah0/e:.1f} Ah |\n"
# LiFePO4 example: 100 Ah, 20 A, 10% to 90%
Cl, Il, a, b, el = 100.0, 20.0, 0.10, 0.90, 0.95
Ahl = Cl * (b - a)
tl = Ahl / (Il * el)
crl = Il / Cl
# charger size to recharge default battery overnight in 8 h
Ineed = Ah0 / (8 * eta0)
# wall energy for default (12 V nominal lead-acid, charging at about 13.8 V average, charger 85%)
Ein = Ah0 / eta0 * 13.8 / 0.85 / 1000

edit('electronics/battery-charge-time', date=U, phrase='battery charging time calculator',
     intro=("How long a battery takes to charge depends on its capacity, the charger current, how much charge it needs and the losses that make real charging slower than Ah ÷ A. "
            "This battery charging time calculator includes state of charge and efficiency; see [industrial battery charger float and boost charging](https://www.instrumentationblog.in/industrial-battery-charger-float-boost/).\n\n"
            "Inverter and solar installers, UPS technicians and boat or caravan owners use it to size chargers and plan recharge times between outages."),
     body_add=f'''
## Worked example

The defaults describe a {C0:g} Ah tubular inverter battery at {s0*100:.0f}% charge on a {I0:g} A charger:

- Charge needed = {C0:g} × ({s1*100:.0f}% − {s0*100:.0f}%) = **{Ah0:g} Ah**
- Time = {Ah0:g} ÷ ({I0:g} × {eta0:g}) = **{t0:g} h**
- C-rate = {I0:g} ÷ {C0:g} = **{cr0:g}C**

To get the same battery back to full in an 8 hour night, the charger must supply {Ah0:g} ÷ (8 × {eta0:g}) = **{Ineed:.1f} A**, so a 20 A charger is the practical choice.

## The same charge on different chemistries

{Ah0:g} Ah into a battery at {I0:g} A:

| Battery type | Efficiency | Time | Ah drawn from charger |
|---|---|---|---|
{eta_rows}
## A lithium example

A {Cl:g} Ah LiFePO4 battery taken from {a*100:.0f}% to {b*100:.0f}% at {Il:g} A needs {Ahl:g} Ah and takes {Ahl:g} ÷ ({Il:g} × {el:g}) = **{tl:.2f} h** at {crl:g}C. Lithium cells stay in constant current mode until about 95%, so the estimate is close to what you will see, while lead-acid needs the extra absorption time noted above.

## Estimating the starting charge

Measure the open circuit voltage after the battery has rested for a few hours with no load or charger. For a 12 V flooded lead-acid battery, about 12.7 V is full, 12.4 V is about 75%, 12.2 V about 50% and 12.0 V about 25%. LiFePO4 voltage is very flat between 20% and 90%, so its state of charge is better read from a coulomb counting battery monitor than from voltage.

## Energy from the wall

Charging {Ah0:g} Ah at an efficiency of {eta0:g} at an average 13.8 V through an 85% efficient charger takes about **{Ein:.2f} kWh** from the mains, worth knowing when the charger runs from a generator.

## Common mistakes

- **Using rated capacity when the battery is aged.** A battery at 80% of its original capacity holds {C0*0.8:g} Ah, and the charge needed falls with it.
- **Taking the charger's label current as the actual current.** Many chargers fold back when hot or when the battery voltage rises; measure with a clamp meter.
- **Charging lead-acid at too high a C-rate.** Flooded cells above about 0.2C gas heavily and heat up, which shortens life.
- **Ignoring loads connected during charging.** An inverter feeding 3 A of load leaves only 12 A for the battery, stretching {t0:g} h to {Ah0/(12*eta0):.1f} h.
- **Stopping at the bulk stage.** Lead-acid left at 80% to 90% sulphates over time; let the absorption stage finish regularly.
''',
     faq_add=[('Can a bigger charger charge a lead-acid battery much faster?',
               f'Only in the bulk stage. Above about 0.2C ({0.2*C0:g} A for a {C0:g} Ah battery) the battery heats and gasses, and the absorption stage still takes a few hours because the current tapers whatever the charger rating.'),
              ('How do I find the starting state of charge?',
               'For lead-acid, rest the battery for a few hours and read the open circuit voltage: about 12.7 V is full, 12.4 V is 75%, 12.2 V is 50% and 12.0 V is 25% for a 12 V battery. For lithium use the battery monitor.')])

# ---------------------------------------------------------------- Strain gauge
Rg, GF, ue, Vex, n = 350.0, 2.0, 1000.0, 10.0, 1
eps = ue * 1e-6
dR0 = Rg * GF * eps
Vo0 = Vex * n * GF * eps / 4
mvv0 = Vo0 / Vex * 1000
assert abs(dR0 - 0.7) < 1e-12 and abs(Vo0 - 0.005) < 1e-12 and abs(mvv0 - 0.5) < 1e-9
# exact quarter bridge
x = GF * eps
Vo_exact = Vex * (x / 4) / (1 + x / 2)
nl = (Vo0 - Vo_exact) / Vo0 * 100
# lead wire: 2 wire, each lead 0.5 ohm
RL = 0.5
desens = Rg / (Rg + 2 * RL)
read_2w = ue * desens
# lead temp change: copper TCR 0.00393/K, 2 x 0.5 ohm, 10 K
dRL = 2 * RL * 0.00393 * 10
app = dRL / (Rg * GF) * 1e6
# 3-wire desensitisation
desens3 = Rg / (Rg + RL)
# shunt calibration resistor for 1000 ue
Rs = Rg / (GF * eps) - Rg
# check: parallel gives dR/R
Rpar = Rg * Rs / (Rg + Rs)
assert abs((Rg - Rpar) / Rg / GF - eps) < 1e-12
cfg_rows = ''
for name, k in (('Quarter (1 active)', 1), ('Half, bending (2 active)', 2), ('Full (4 active)', 4)):
    v = Vex * k * GF * eps / 4
    cfg_rows += f"| {name} | {k} | {v*1000:.1f} mV | {v/Vex*1000:.2f} mV/V |\n"
# stress in aluminium 6061, E = 68.9 GPa
s_al = 68.9e9 * eps / 1e6
s_st = 200e9 * eps / 1e6

edit('electronics/strain-gauge', date=U, phrase='strain gauge calculator',
     intro=("A strain gauge is a fine foil grid whose resistance changes slightly when it is stretched or compressed, and a Wheatstone bridge turns that into a voltage. "
            "This strain gauge calculator gives the resistance change and bridge output; see the [strain gauge working principle](https://www.instrumentationblog.in/strain-gauge-working-principle/).\n\n"
            "Instrumentation and test engineers use it to choose excitation and amplifier gain for load cells, pressure transmitters and structural tests, and to check that readings make sense."),
     body_add=f'''
## Worked example

The defaults are a {Rg:g} Ω foil gauge, GF = {GF:g}, {c(ue)} µε, {Vex:g} V excitation, quarter bridge:

- ΔR = {Rg:g} × {GF:g} × {eps:g} = **{dR0:.2f} Ω** ({dR0*1000:.0f} mΩ)
- V<sub>out</sub> ≈ {Vex:g} × 1 × {GF:g} × {eps:g} ÷ 4 = **{Vo0*1000:.1f} mV**
- Sensitivity = {Vo0*1000:.1f} ÷ {Vex:g} = **{mvv0:.2f} mV/V**

The exact quarter bridge output is {Vex:g} × (GFε/4) ÷ (1 + GFε/2) = {Vo_exact*1000:.3f} mV, so the linear formula reads {nl:.2f}% high at this strain. For a steel part (E = 200 GPa) that strain means about {s_st:.0f} MPa; in 6061 aluminium (E = 68.9 GPa) it is about {s_al:.1f} MPa.

## Output by bridge type at the defaults

| Configuration | Active arms | Output | Sensitivity |
|---|---|---|---|
{cfg_rows}
## Lead wires and temperature

In a two wire quarter bridge both leads sit in the gauge arm. With {RL:g} Ω per lead the arm becomes {Rg+2*RL:g} Ω, which desensitises the reading by {desens:.4f}, so a true {c(ue)} µε reads about {read_2w:.0f} µε. Worse, if those copper leads warm by 10 K their resistance rises {dRL*1000:.1f} mΩ, which the bridge reports as **{app:.0f} µε** of strain that is not there. A three wire connection puts one lead in each adjacent arm so the changes cancel, and the desensitisation drops to {desens3:.4f}.

## Shunt calibration

To check a channel without loading the part, a precision resistor is switched across one bridge arm to simulate a known strain. The resistor for ε is R<sub>s</sub> = R ÷ (GF × ε) − R. For {c(ue)} µε on a {Rg:g} Ω gauge that is **{c(Rs)} Ω**; the indicator should then show {c(ue)} µε (as compression when shunting the active arm).

## Common mistakes

- **Entering strain in m/m instead of µε.** 0.001 typed into a µε field means 0.001 µε, a millionth of the intended value.
- **Using the half bridge factor for a Poisson arrangement.** A gauge across the grain only adds about 0.3 of the main gauge's signal, so the output is about 1.3 times a quarter bridge, not 2 times.
- **Mismatched gauge and material.** A gauge self compensated for steel (11 ppm/K) bonded to aluminium (23 ppm/K) shows apparent strain with every temperature change.
- **Too much excitation on a small gauge.** Self heating in a 120 Ω gauge on plastic at 10 V causes drift; 2 to 5 V is safer on poor heat sinks.
- **Ignoring zero offset.** Bonding leaves a small initial unbalance; take a zero reading before loading and subtract it.
''',
     faq_add=[('What shunt calibration resistor simulates a given strain?',
               f'R<sub>s</sub> = R ÷ (GF × ε) − R. For a {Rg:g} Ω gauge with GF {GF:g}, simulating {c(ue)} µε needs about {c(Rs)} Ω across the active arm.'),
              ('How much error do lead wires add to a quarter bridge?',
               f'With two wire connection and {RL:g} Ω per lead, a {Rg:g} Ω gauge reads about {(1-desens)*100:.2f}% low, and a 10 K warming of the copper leads appears as roughly {app:.0f} µε of false strain. A three wire connection cancels most of this.')])

# ---------------------------------------------------------------- RC phase shift oscillator
R, C = 10e3, 10e-9
f0 = 1 / (2 * math.pi * R * C * math.sqrt(6))
Rf0 = 29 * R
assert abs(f0 - 649.747) < 0.01 and abs(Rf0 - 290e3) < 1e-6


def ladder(f, R=R, C=C):
    # three section CR high pass ladder (series C, shunt R), unloaded
    xx = 1 / (2 * math.pi * f * R * C)
    return 1 / complex(1 - 5 * xx ** 2, -(6 * xx - xx ** 3))


H0 = ladder(f0)
assert abs(abs(H0) - 1 / 29) < 1e-9 and abs(abs(cmath.phase(H0)) - math.pi) < 1e-6
lad_rows = ''
for k in (0.5, 0.8, 1.0, 1.25, 2.0):
    h = ladder(f0 * k)
    ph = math.degrees(cmath.phase(h))
    if ph < 0:
        ph += 360
    lad_rows += f"| {c(f0*k, 1)} Hz | {abs(h):.4f} | 1/{1/abs(h):.1f} | {ph:.1f}° |\n"
# design for 1 kHz with C = 10 nF
ft = 1000.0
Rt = 1 / (2 * math.pi * ft * C * math.sqrt(6))
Re = 6.8e3
fe = 1 / (2 * math.pi * Re * C * math.sqrt(6))
Rfe = 29 * Re
# capacitor tolerance 5%
f_lo = 1 / (2 * math.pi * R * C * 1.05 * math.sqrt(6))
f_hi = 1 / (2 * math.pi * R * C * 0.95 * math.sqrt(6))
# GBW requirement
gbw_min = 29 * f0
# RC low pass ladder trap
f_lp = math.sqrt(6) / (2 * math.pi * R * C)

edit('electronics/rc-phase-shift-oscillator', date=U, phrase='rc phase shift oscillator calculator',
     intro=("An RC phase shift oscillator uses three RC sections to shift the signal by 180°, and an inverting amplifier supplies the other 180° and makes up the loss. "
            "This RC phase shift oscillator calculator gives the frequency and the gain resistor; it is one of the [types of transistor oscillators](https://www.instrumentationblog.in/types-of-transistor-oscillators/).\n\n"
            "Electronics students build it as a first oscillator lab, and designers use it for simple fixed audio tones, test signals and sensor excitation where a crystal would be overkill."),
     body_add=f'''
## Why the gain has to be 29

The table shows the unloaded three section CR ladder (series C, shunt R) with the default 10 kΩ and 10 nF. Only at {f0:.1f} Hz is the phase shift exactly 180°, and there the ladder passes 1/29 of the signal.

| Frequency | Gain | As a fraction | Phase lead |
|---|---|---|---|
{lad_rows}
## Designing for a target frequency

For a 1 kHz tone with 10 nF capacitors, R = 1 ÷ (2π × {ft:g} × 10 nF × √6) = {c(Rt)} Ω. The nearest E24 value is 6.8 kΩ, which gives **{fe:.1f} Hz**; the feedback resistor must be at least 29 × 6.8 kΩ = {Rfe/1e3:.1f} kΩ, so fit 220 kΩ. If the exact frequency matters, use 1% resistors from the E96 series or trim one resistor.

## Practical build notes

- With ±5% capacitors the default circuit can land anywhere from {f_lo:.0f} Hz to {f_hi:.0f} Hz, so check the frequency with a counter or oscilloscope.
- The op-amp must have plenty of gain left at the operating frequency. A gain of 29 at {f0:.0f} Hz needs at least {c(gbw_min)} Hz of gain bandwidth, and ten times that keeps the phase error small, so a general purpose 1 MHz op-amp is fine at audio frequencies but not at 50 kHz.
- Expect start-up to take several cycles. Set the gain about 5% to 10% above 29 and add back to back diodes in series with a resistor across R<sub>f</sub> to limit the amplitude.
- Take the output from the op-amp output, not from the ladder, and buffer it before driving a load.

## Common mistakes

- **Using the high pass formula for an RC low pass ladder.** With series R and shunt C the frequency is √6 ÷ (2πRC), which is {c(f_lp)} Hz for the defaults, not {f0:.1f} Hz.
- **Forgetting that the last R is the amplifier input resistor.** If a separate input resistor is added, the third section is loaded and both frequency and gain change.
- **Setting the gain to exactly 29.** Tolerances and op-amp limits mean it may never start; aim for 30 to 32.
- **Driving the ladder from a high impedance.** The source impedance adds to the first section and lowers the frequency.
- **Choosing very small R values.** Below about 1 kΩ the ladder loads the op-amp output heavily and distortion rises.
''',
     faq_add=[('How do I choose R and C for a given frequency?',
               f'Pick a convenient capacitor, then R = 1 ÷ (2π f C √6). For 1 kHz with 10 nF, R = {c(Rt)} Ω; 6.8 kΩ from the E24 series gives about {fe:.0f} Hz.'),
              ('What op-amp bandwidth does a phase shift oscillator need?',
               f'Gain bandwidth of at least 29 times the oscillation frequency, and preferably ten times more. At {f0:.0f} Hz that is {c(gbw_min)} Hz minimum, which almost any op-amp provides.')])

print('slice 5 done')

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-22), slice 6: instrumentation-amplifier-gain, microstrip-impedance, zener-resistor, inductor-al-value, reactance.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-22'
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


E96 = [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50,
       1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32,
       2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57,
       3.65, 3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49,
       5.62, 5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45,
       8.66, 8.87, 9.09, 9.31, 9.53, 9.76]


def e96_near(r):
    d = 10 ** math.floor(math.log10(r))
    cands = [v * d for v in E96] + [10 * d]
    return min(cands, key=lambda v: abs(v - r))


# ---------------------------------------------------------------- Instrumentation amplifier gain
k, G, Vd = 50000.0, 100.0, 20e-3
Rg = k / (G - 1)
Vo = G * Vd
assert abs(Rg - 505.05) < 0.01 and abs(Vo - 2.0) < 1e-9
R96 = e96_near(Rg)
G96 = 1 + k / R96
err96 = (G96 / G - 1) * 100
# bridge: 350 ohm, 2 mV/V, 10 V excitation -> 20 mV full scale (the default input)
Vex, sens = 10.0, 2e-3
Vfs = Vex * sens
assert abs(Vfs - Vd) < 1e-12
Vcm = Vex / 2
# tolerance: 0.1% Rg gives gain error (G-1)/G * 0.1%
tol_err = (G - 1) / G * 0.1
# trace resistance at G = 1000
Rg1000 = k / 999
Rtr = 0.1
G1000_tr = 1 + k / (Rg1000 + Rtr)
err_tr = (1 - G1000_tr / 1000) * 100
# tempco mismatch: 50 ppm/K of Rg vs internal over 40 K
tc_err = (G - 1) / G * 50e-6 * 40 * 100
ina_rows = ''
for g in (10, 50, 100, 500, 1000):
    ex = k / (g - 1)
    r = e96_near(ex)
    ga = 1 + k / r
    ina_rows += f"| {g} | {c(ex, 1)} Ω | {c(r, 1 if r < 1000 else 0)} Ω | {ga:,.2f} | {(ga / g - 1) * 100:+.2f}% |\n"

edit('electronics/instrumentation-amplifier-gain', date=U, phrase='instrumentation amplifier gain calculator',
     intro=("An instrumentation amplifier boosts the small difference between two inputs and ignores the voltage they share, with one external resistor setting the gain. "
            "This instrumentation amplifier gain calculator finds that resistor R<sub>G</sub> for the INA128, AD620, INA333 and similar parts, or the gain from a given R<sub>G</sub>.\n\n"
            f"Designers of load cell, strain gauge and thermocouple front ends use it to scale millivolt signals to an ADC range. See [how an instrumentation amplifier works]({IB}instrumentation-amplifier-working/) and how it [differs from an op-amp]({IB}instrumentation-amplifier-vs-op-amp-key-differences/)."),
     body_add=f'''
## Worked example: bridge sensor into an ADC

The default inputs describe a common job: a 350 Ω load cell rated {sens * 1e3:g} mV/V, excited at {Vex:g} V, gives **{Vfs * 1e3:g} mV** at full load. To turn that into {Vo:g} V for a 0 to 2.5 V ADC with headroom, pick the INA128 and a gain of {G:g}:

- R<sub>G</sub> = 50,000 ÷ ({G:g} − 1) = **{Rg:.2f} Ω**
- Output at full load = {G:g} × {Vfs * 1e3:g} mV = **{Vo:.2f} V**
- The nearest 1% E96 value is {R96:g} Ω, which gives G = {G96:.2f}, a gain error of **{err96:+.2f}%**
- Both inputs sit near {Vcm:g} V, half the excitation, so that common mode voltage must lie inside the amplifier's input range at the chosen supply

If {err96:+.2f}% is too much, use a 0.1% E192 value of 505 Ω, or a 499 Ω resistor in series with a small trim resistor, and calibrate with known weights.

## Standard resistor values and the gain you really get (INA128)

| Target gain | Exact R<sub>G</sub> | Nearest E96 | Actual gain | Error |
|---|---|---|---|---|
{ina_rows}
## How it is set up on a real board

The R<sub>G</sub> pins connect to internal nodes of the input stage, so place the resistor right next to the package with short, equal traces. Drive the REF pin from a low impedance source such as a buffered mid-supply voltage; any resistance in series with REF unbalances the internal difference amplifier and degrades common mode rejection. After assembly, check the gain with a precision source or a calibrator by applying two known differential voltages and fitting a straight line, which removes the offset at the same time.

## Common mistakes

- **Leaving no DC path for input bias current.** A floating thermocouple or a transformer coupled signal lets the inputs drift to a rail. Tie each input to ground or REF through a resistor of 10 kΩ to 1 MΩ.
- **Ignoring trace resistance at high gain.** At G = 1000, R<sub>G</sub> is only {Rg1000:.1f} Ω, so an extra {Rtr:g} Ω of copper and solder lowers the gain by about **{err_tr:.2f}%**.
- **Buying R<sub>G</sub> on tolerance alone.** A 0.1% part adds about {tol_err:.2f}% gain error at G = {G:g}, but a 50 ppm/K mismatch to the internal resistors adds another {tc_err:.2f}% over a 40 K swing.
- **Checking only the output swing.** With a high gain the internal nodes can clip before the output does, so read the datasheet's common mode versus output voltage chart for your supply.
- **Expecting the formula to hold for any part.** Some in-amps, such as the INA333 and AD8237, use different constants or two gain resistors, so take k from the exact datasheet.
''',
     faq_add=[('Why is my measured instrumentation amplifier gain slightly off?',
               f'Usually R<sub>G</sub> is a rounded standard value plus PCB resistance. With the INA128 at G = 100, the nearest E96 value {R96:g} Ω gives a gain of {G96:.2f}, about {err96:+.2f}% from target; calibrate with two known inputs to remove it.'),
              ('Do I need a resistor from each input to ground?',
               'Yes, whenever the source has no DC path to the amplifier ground, such as an isolated thermocouple or AC coupled sensor. Without it the input bias current charges the inputs until the amplifier saturates.')])

# ---------------------------------------------------------------- Microstrip impedance


def z0(w, t, h, er):
    return 87 / math.sqrt(er + 1.41) * math.log(5.98 * h / (0.8 * w + t))


def w_for(Z, t, h, er):
    return (5.98 * h / math.exp(Z * math.sqrt(er + 1.41) / 87) - t) / 0.8


w, t, h, er = 0.3, 0.035, 0.2, 4.3
Z0 = z0(w, t, h, er)
tpd = 85 * math.sqrt(0.475 * er + 0.67) / 25.4
assert abs(Z0 - 53.52) < 0.01 and abs(tpd - 5.51) < 0.01
w50 = w_for(50, t, h, er)
# plated outer layer: 35 um + 25 um plating
Zpl = z0(w, 0.060, h, er)
w50pl = w_for(50, 0.060, h, er)
# h mistaken: core 0.2 vs prepreg 0.1 -- show effect if real h is 0.1
Zh1 = z0(w, t, 0.1, er)
# delay for a 100 mm trace and critical length for 1 ns rise time
d100 = tpd * 100
lcrit = 1000 / 6 / tpd
# er at 4.6
Zer = z0(w, t, h, 4.6)
# fabrication tolerance +/- 10 percent
ms_rows = ''
for hh in (0.10, 0.20, 0.36, 1.0, 1.6):
    ww = w_for(50, t, hh, er)
    ms_rows += f"| {hh:.2f} mm | {ww:.3f} mm | {ww / hh:.2f} | {w_for(75, t, hh, er):.3f} mm | {w_for(90, t, hh, er):.3f} mm |\n"

edit('electronics/microstrip-impedance', date=U, phrase='microstrip impedance calculator',
     intro=("A surface microstrip is a trace on an outer PCB layer running over a ground plane, and its impedance is set by trace width, copper thickness, dielectric height and ε<sub>r</sub>. "
            f"This microstrip impedance calculator uses the IPC-2141 formula to size [controlled impedance PCB traces]({IB}controlled-impedance-pcb-traces/).\n\n"
            f"PCB and RF designers use it to choose 50 Ω and 90 Ω trace widths, plan a [PCB layer stackup]({IB}pcb-layer-stackup-design/) and estimate delay before asking the fabricator for a field solver check."),
     body_add=f'''
## Finding the width for 50 Ω

Running the formula backwards gives w = [5.98 h ÷ e<sup>Z₀√(εr + 1.41)/87</sup> − t] ÷ 0.8. For the default stackup (h = 0.2 mm, 35 µm copper, ε<sub>r</sub> = 4.3), a 50 Ω trace is **{w50:.3f} mm** wide, slightly wider than the 0.3 mm default that gives {Z0:.1f} Ω.

Outer layers are plated after drilling, which typically adds about 25 µm. With 60 µm total copper the 0.3 mm trace drops to **{Zpl:.1f} Ω**, and the 50 Ω width becomes {w50pl:.3f} mm. Fabricators adjust etch compensation for this, which is one reason to send them the target impedance rather than a fixed width.

## Trace widths for common impedances (ε<sub>r</sub> 4.3, 35 µm copper)

| Height to plane | 50 Ω width | w/h at 50 Ω | 75 Ω width | 90 Ω width |
|---|---|---|---|---|
{ms_rows}
Widths with w/h below 0.1 fall outside the formula's range; for narrow high impedance lines on thin prepreg use a field solver.

## Delay and when a trace needs controlling

At {tpd:.2f} ps/mm a 100 mm trace delays the signal by about **{d100:.0f} ps**. A common rule of thumb treats a line as a transmission line once its one way delay exceeds about one sixth of the signal rise time. For a 1 ns edge that is about **{lcrit:.0f} mm** on this stackup, so even a short trace from a fast logic driver can ring if it is not terminated or matched.

## How impedance is checked in production

Fabricators place test coupons on the panel edge with the same stackup and trace geometry, then measure them with a time domain reflectometer (TDR). The usual tolerance is ±10%, or ±5% at extra cost. The TDR trace shows the impedance along the coupon, so a change at a via or connector appears as a step, which is also how impedance discontinuities are found on a finished board.

## Common mistakes

- **Measuring h to the wrong plane.** If the real reference is a 0.1 mm prepreg rather than 0.2 mm, the same 0.3 mm trace is about **{Zh1:.1f} Ω**, not {Z0:.1f} Ω.
- **Using the laminate's 1 MHz ε<sub>r</sub>.** FR-4 datasheet values vary with frequency and resin content; moving from 4.3 to 4.6 already lowers Z₀ to {Zer:.1f} Ω.
- **Forgetting plating and solder mask.** Both lower the impedance on outer layers, together often by 3 to 5 Ω.
- **Routing across a plane split.** The return current has to detour around the gap, which adds inductance and turns a 50 Ω trace into a discontinuity.
- **Reusing microstrip widths for inner layers.** An inner trace between two planes is stripline and needs a narrower width for the same impedance.
''',
     faq_add=[('Does copper plating change microstrip impedance?',
               f'Yes. Outer layers gain roughly 25 µm of plating, so a 0.3 mm trace on 0.2 mm FR-4 falls from {Z0:.1f} Ω with 35 µm copper to about {Zpl:.1f} Ω with 60 µm. Specify the target impedance so the fabricator can compensate.'),
              ('How long can a PCB trace be before impedance matters?',
               f'A common rule is when its one way delay exceeds one sixth of the rise time. On FR-4 microstrip at {tpd:.2f} ps/mm that is about {lcrit:.0f} mm for a 1 ns edge and about {lcrit / 4:.0f} mm for a 250 ps edge.')])

# ---------------------------------------------------------------- Zener resistor
Vin, Vz, IL, Iz = 12.0, 5.1, 20e-3, 5e-3
R = (Vin - Vz) / (IL + Iz)
PR = (Vin - Vz) ** 2 / R
Pz = Vz * (Vin - Vz) / R
assert abs(R - 276) < 1e-9 and abs(PR * 1e3 - 172.5) < 1e-6 and abs(Pz * 1e3 - 127.5) < 1e-6
Rs = 270.0
rz = 10.0
par = rz * Rs / (rz + Rs)
dV_load = IL * par
line = rz / (Rs + rz)
dV_line = 2.0 * line
# improvement with emitter follower: base current = 20 mA / hFE 100
hfe = 100
Ib = IL / hfe
Rfol = (Vin - Vz) / (Ib + Iz)
dV_load_f = Ib * rz * Rs / (rz + Rs)
zr_rows = ''
for r_z in (5, 10, 20, 30):
    p = r_z * Rs / (r_z + Rs)
    zr_rows += f"| {r_z} Ω | {IL * p * 1e3:.0f} mV | {r_z / (Rs + r_z) * 100:.1f}% | {2 * r_z / (Rs + r_z) * 1e3:.0f} mV |\n"

edit('electronics/zener-resistor', date=U,
     before='## Practical notes',
     body_add=f'''
## How much the output really moves

A Zener is not a perfect voltage source: above its knee it behaves like the rated voltage in series with a small dynamic resistance r<sub>z</sub>. With the 270 Ω resistor from the example and a typical r<sub>z</sub> of {rz:g} Ω:

- **Load regulation:** when the load goes from 0 to 20 mA, the output falls by about I<sub>L</sub> × (r<sub>z</sub> ∥ R) = 20 mA × {par:.2f} Ω = **{dV_load * 1e3:.0f} mV**
- **Line regulation:** a change in input appears at the output scaled by r<sub>z</sub> ÷ (R + r<sub>z</sub>) = **{line * 100:.1f}%**, so a 2 V rise in supply lifts the output by about **{dV_line * 1e3:.0f} mV**

| Dynamic resistance r<sub>z</sub> | Output drop, 0 to 20 mA load | Line regulation | Output rise for +2 V input |
|---|---|---|---|
{zr_rows}
Read r<sub>z</sub> (often written Z<sub>ZT</sub>) from the datasheet at the test current; it rises sharply near the knee, so a starved Zener regulates far worse than these figures. To measure it, set two Zener currents such as 5 mA and 15 mA with a bench supply and divide the change in Zener voltage by the change in current.

If 0.2 V of load regulation is too much, buffer the Zener with an NPN emitter follower. The Zener then only supplies the base current, about {Ib * 1e3:.1f} mA for a gain of {hfe}, so the series resistor rises to roughly {Rfol:.0f} Ω and the load change seen by the Zener falls to about {dV_load_f * 1e3:.0f} mV, at the cost of the transistor's 0.6 to 0.7 V base emitter drop.
''',
     faq_add=[('How much does the output of a Zener regulator change with load?',
               f'About the load current change times the Zener dynamic resistance in parallel with the series resistor. With 270 Ω and r<sub>z</sub> = 10 Ω, going from no load to 20 mA lowers a 5.1 V output by roughly {dV_load * 1e3:.0f} mV.')],
     min_words=900)

# ---------------------------------------------------------------- Inductor AL value
AL, Lt = 250.0, 150e-6
N = math.sqrt(Lt / (AL * 1e-9))
Nr = math.ceil(N)
La = AL * 1e-9 * Nr ** 2
assert abs(N - 24.495) < 0.001 and Nr == 25 and abs(La * 1e6 - 156.25) < 1e-9
L24 = AL * 1e-9 * 24 ** 2
# measure AL with a test winding
Ntest, Lmeas = 10, 24e-6
ALm = Lmeas / Ntest ** 2 * 1e9
Nm = math.sqrt(Lt / (ALm * 1e-9))
# flux density check: Ae = 25 mm^2, Ipk = 1 A
Ae, Ipk, Bsat = 25e-6, 1.0, 0.30
B = La * Ipk / (Nr * Ae)
Imax = Bsat * Nr * Ae / La
al_rows = ''
for name, tol in (('Ungapped ferrite', 0.25), ('Typical ferrite toroid', 0.20), ('Powdered iron', 0.10), ('Gapped ferrite', 0.05), ('Precision gapped core', 0.03)):
    al_rows += f"| {name} | ±{tol * 100:.0f}% | {La * (1 - tol) * 1e6:.1f} µH | {La * (1 + tol) * 1e6:.1f} µH |\n"

edit('electronics/inductor-al-value', date=U, phrase='inductor AL value calculator',
     intro=("A core's A<sub>L</sub> value is the inductance of one turn on that core, in nH per turn squared, so a winding of N turns gives L = A<sub>L</sub> × N². "
            "This inductor AL value calculator finds the turns needed for a target inductance, rounds them up and shows the inductance you actually get.\n\n"
            f"Power supply designers, RF hobbyists and students use it when winding chokes, filters and toroids, then check that the core will not [saturate above its rated current]({IB}inductor-saturation-current/)."),
     body_add=f'''
## Why the rounded winding is never exact

Turns come in whole numbers, so the achievable inductances are steps. On the default 250 nH/N² core, 24 turns give **{L24 * 1e6:.0f} µH** and 25 turns give **{La * 1e6:.2f} µH**, a step of about {(La / L24 - 1) * 100:.0f}%. Rounding up keeps you at or above the target, which suits filter chokes where too little inductance means more ripple. If you need a value between steps, change the core, add a gap or accept the nearer value.

## Measuring A<sub>L</sub> yourself

When a core has no marking, wind a test coil and measure it with an LCR meter at a low test level. For example, {Ntest} turns reading **{Lmeas * 1e6:g} µH** give A<sub>L</sub> = {Lmeas * 1e6:g} µH ÷ {Ntest}² = **{ALm:.0f} nH/N²**. With that core, 150 µH needs √(150,000 ÷ {ALm:.0f}) = **{Nm:.2f}** turns, so 25 turns again. Use at least 10 turns spread evenly around a toroid so that leakage does not inflate the reading, and measure at a frequency close to the one the inductor will see.

## Inductance spread from A<sub>L</sub> tolerance (25 turns, A<sub>L</sub> = 250 nH/N²)

| Core type | Typical A<sub>L</sub> tolerance | Lowest L | Highest L |
|---|---|---|---|
{al_rows}
## Checking for saturation

The peak flux density is B = L × I ÷ (N × A<sub>e</sub>), where A<sub>e</sub> is the core's effective area. For the 25 turn, {La * 1e6:.2f} µH winding on a core with A<sub>e</sub> = {Ae * 1e6:g} mm² carrying {Ipk:g} A peak, B = **{B:.3f} T**. Power ferrite saturates near {Bsat:g} T when hot, so this winding can only carry about **{Imax:.2f} A** before the inductance collapses. Use a larger core, a gapped core or fewer turns on a higher A<sub>L</sub> core if the peak current is higher.

## Common mistakes

- **Mixing up the A<sub>L</sub> units.** A value of 250 in µH per 100 turns is only 25 nH/N², which needs about 3.2 times as many turns.
- **Counting turns wrongly on a toroid.** Each pass of the wire through the centre hole is one turn; the wire lying along the outside does not count again.
- **Using A<sub>L</sub> under DC bias.** The datasheet value is measured at near zero current; powdered iron and ungapped ferrite lose a large part of it as DC current rises, so check the permeability versus bias curve.
- **Taking A<sub>L</sub> from the wrong material grade.** The same core shape is sold in several ferrite mixes whose A<sub>L</sub> values differ by a factor of five or more.
- **Rounding the turns down.** That leaves the inductance below target, and the tolerance can then push it far lower.
''',
     faq_add=[('How do I find the AL value of an unmarked core?',
               f'Wind about 10 turns, measure the inductance with an LCR meter and divide by the turns squared. A reading of {Lmeas * 1e6:g} µH on {Ntest} turns means A<sub>L</sub> = {ALm:.0f} nH/N².'),
              ('How much current can my wound inductor carry?',
               f'Until the peak flux density B = L × I ÷ (N × A<sub>e</sub>) reaches the core saturation limit. For {La * 1e6:.2f} µH on 25 turns and A<sub>e</sub> = {Ae * 1e6:g} mm², a {Bsat:g} T limit allows about {Imax:.2f} A peak.')])

# ---------------------------------------------------------------- Reactance
f, Lh, C, Rr = 50.0, 0.1, 100e-6, 20.0
XL = 2 * math.pi * f * Lh
XC = 1 / (2 * math.pi * f * C)
Z = math.sqrt(Rr ** 2 + (XL - XC) ** 2)
ph = math.degrees(math.atan((XL - XC) / Rr))
assert abs(XL - 31.416) < 0.001 and abs(XC - 31.831) < 0.001 and abs(Z - 20.004) < 0.001 and abs(ph - (-1.19)) < 0.01
V = 230.0
I = V / Z
VL, VC = I * XL, I * XC
P = I ** 2 * Rr
f0 = 1 / (2 * math.pi * math.sqrt(Lh * C))
# parallel L and C at 50 Hz
Xp = XL * XC / abs(XC - XL)
rx_rows = ''
for ff in (25, 40, 50, f0, 60, 100, 150):
    xl = 2 * math.pi * ff * Lh
    xc = 1 / (2 * math.pi * ff * C)
    zz = math.sqrt(Rr ** 2 + (xl - xc) ** 2)
    pp = math.degrees(math.atan((xl - xc) / Rr))
    rx_rows += f"| {ff:.2f} Hz | {xl:.2f} Ω | {xc:.2f} Ω | {zz:.2f} Ω | {pp:+.1f}° | {V / zz:.2f} A |\n"

edit('electronics/reactance', date=U, phrase='reactance and impedance calculator',
     intro=("Inductors and capacitors oppose alternating current by an amount that changes with frequency, called reactance, and together with resistance this sets the impedance and phase angle. "
            "This reactance and impedance calculator finds X<sub>L</sub>, X<sub>C</sub>, series RLC impedance and phase.\n\n"
            f"Students, electricians and electronics designers use it for filters, motor circuits and resonance checks. See [impedance and reactance in AC circuits]({IB}impedance-reactance-ac-circuits/) and [phase angle in AC circuits]({IB}phase-angle-in-ac-circuits/)."),
     body_add=f'''
## Worked example: the default circuit on 230 V

A 100 mH inductor, a 100 µF capacitor and a 20 Ω resistor in series at 50 Hz:

- X<sub>L</sub> = 2π × 50 × 0.1 = **{XL:.2f} Ω**
- X<sub>C</sub> = 1 ÷ (2π × 50 × 100 × 10⁻⁶) = **{XC:.2f} Ω**
- Z = √(20² + ({XL:.2f} − {XC:.2f})²) = **{Z:.3f} Ω**
- φ = atan({XL - XC:.3f} ÷ 20) = **{ph:.2f}°**, slightly capacitive

The two reactances almost cancel because the circuit's resonant frequency, 1 ÷ (2π√(LC)) = **{f0:.2f} Hz**, is close to 50 Hz. On 230 V the current is {V:g} ÷ {Z:.3f} = **{I:.2f} A** and the resistor dissipates **{P:,.0f} W**. The voltage across the inductor is {I:.2f} × {XL:.2f} = **{VL:.0f} V** and across the capacitor **{VC:.0f} V**, far above the supply, because the two are in antiphase and their voltages mostly cancel.

## Impedance of the default circuit across frequency

| Frequency | X<sub>L</sub> | X<sub>C</sub> | Z | Phase | Current at 230 V |
|---|---|---|---|---|---|
{rx_rows}
Below resonance the circuit is capacitive (negative phase); above it the inductor dominates and the phase turns positive.

## Measuring reactance in practice

An LCR meter applies a small AC test signal at a chosen frequency, commonly 100 Hz, 1 kHz or 10 kHz, and reports inductance or capacitance together with the series resistance (ESR). Measure at a frequency near the one the part will see, because iron cored inductors and electrolytic capacitors change value with frequency and level. In a working mains circuit, reactance can be found from a clamp meter current and a voltage reading as X = V ÷ I, provided the resistance is small or is subtracted.

## Common mistakes

- **Entering inductance in henries.** This calculator expects millihenries, so 0.1 means 0.1 mH and gives a reactance a thousand times too small.
- **Adding the reactances.** In a series circuit X<sub>L</sub> and X<sub>C</sub> subtract, because their voltages are 180° apart.
- **Using the series formula for a parallel circuit.** For L and C in parallel at 50 Hz the combined reactance is X<sub>L</sub>X<sub>C</sub> ÷ |X<sub>C</sub> − X<sub>L</sub>| = **{c(Xp)} Ω**, close to an open circuit, not a short.
- **Rating parts for the supply voltage only.** Near resonance the component voltages can be many times the supply, as the {VL:.0f} V in the example shows.
- **Ignoring harmonics.** At the 5th harmonic (250 Hz) X<sub>L</sub> is five times larger and X<sub>C</sub> five times smaller, so a circuit tuned at 50 Hz behaves very differently for distorted waveforms.
''',
     faq_add=[('Why is the voltage across the capacitor higher than the supply?',
               f'Near resonance the inductor and capacitor voltages are large but opposite in phase, so they cancel in the total. In the default circuit on 230 V, {I:.2f} A flows and each reactive part sees about {VL:.0f} V.'),
              ('How do I calculate the impedance of L and C in parallel?',
               f'Combine the reactances as X<sub>L</sub>X<sub>C</sub> ÷ (X<sub>C</sub> − X<sub>L</sub>). With 100 mH and 100 µF at 50 Hz that is about {c(Xp)} Ω, because the two currents nearly cancel.')])

print('slice 6 done', inplace.DONE)
