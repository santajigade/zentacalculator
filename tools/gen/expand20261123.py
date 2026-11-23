"""Part C expansion (2026-11-23): 30 pages from the top of tools/upgrade-backlog.txt (priority list was empty; electronics/led-resistor skipped because it is featured, flyback-transformer taken instead), brought to the api-gravity standard. Assembled from seven sections; edits are applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-23), slice 1: 555-timer, pcb-trace-width, voltage-divider, capacitor-lifetime.
electronics/led-resistor is marked featured, which inplace.edit refuses, so it is left unchanged.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-23'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- 555 timer
R1, R2, C = 1e3, 10e3, 10e-6


def t555(R1, R2, C):
    th = 0.693 * (R1 + R2) * C
    tl = 0.693 * R2 * C
    return th, tl, 1 / (th + tl), th / (th + tl)


th, tl, f, D = t555(R1, R2, C)
assert abs(th - 0.07623) < 1e-6 and abs(tl - 0.0693) < 1e-6
assert abs(f - 6.871) < 0.001 and abs(D - 0.5238) < 0.0001
# first cycle: capacitor starts at 0 V and must charge to 2/3 Vcc, ln(3) instead of ln(2)
th_first = math.log(3) * (R1 + R2) * C
# electrolytic tolerance -20% / +20%
tol_rows = ''
for name, k in (('−20%', 0.8), ('−10%', 0.9), ('Nominal', 1.0), ('+10%', 1.1), ('+20%', 1.2)):
    _, _, ff, _ = t555(R1, R2, C * k)
    tol_rows += f"| {name} | {C*k*1e6:.0f} µF | {ff:.2f} Hz | {1000/ff:.1f} ms |\n"
_, _, f_lo, _ = t555(R1, R2, C * 1.2)
_, _, f_hi, _ = t555(R1, R2, C * 0.8)
# design for 1 kHz with C = 10 nF and R1 = 1 k: R2 = (1.44/(f C) - R1)/2
Cd = 10e-9
R2d = (1.44 / (1000 * Cd) - R1) / 2
_, _, f_chk, D_chk = t555(R1, 68e3, Cd)
# discharge current through R1 at 9 V when R1 is too small
I_dis_100 = 9 / 100

edit('electronics/555-timer', date=U, phrase='555 timer calculator',
     intro=("The 555 is a timer chip that compares its capacitor voltage with one third and two thirds of the supply to make square waves, pulses and delays. "
            "This 555 timer calculator works out the astable frequency, high time, low time and duty cycle from R1, R2 and C; see the "
            "[555 timer IC explained](https://www.instrumentationblog.in/555-timer-ic-explained/).\n\n"
            "Hobbyists, students and repair technicians use it to pick parts for LED flashers, buzzers, clock sources and simple PWM without trial and error on the bench."),
     body_add=f'''
## Worked example with the default values

With R1 = 1 kΩ, R2 = 10 kΩ and C = 10 µF:

1. High time t<sub>H</sub> = 0.693 × (1,000 + 10,000) × 0.00001 = **{th*1000:.2f} ms**
2. Low time t<sub>L</sub> = 0.693 × 10,000 × 0.00001 = **{tl*1000:.2f} ms**
3. Period = {th*1000:.2f} + {tl*1000:.2f} = {(th+tl)*1000:.2f} ms, so f = 1 ÷ {th+tl:.5f} s = **{f:.2f} Hz**
4. Duty cycle = {th*1000:.2f} ÷ {(th+tl)*1000:.2f} = **{D*100:.1f}%**

The 0.693 is ln 2: the capacitor charges and discharges between ⅓ and ⅔ of V<sub>cc</sub>, and each half step takes one RC time multiplied by ln 2. That is also why the supply voltage cancels out of the formula.

## Why the first pulse is longer

At power up the capacitor starts at 0 V, not ⅓ V<sub>cc</sub>, so the first high period runs from 0 to ⅔ V<sub>cc</sub> and takes ln 3 × (R1 + R2) × C = **{th_first*1000:.1f} ms** instead of {th*1000:.1f} ms. If a circuit counts pulses from switch on, ignore the first one.

## Effect of capacitor tolerance

Timing scales directly with C, and general purpose electrolytics are often ±20%:

| Capacitor tolerance | Actual C | Frequency | Period |
|---|---|---|---|
{tol_rows}
So the default circuit could run anywhere from {f_lo:.2f} Hz to {f_hi:.2f} Hz before resistor tolerance is even counted. For a repeatable clock, use a 5% film capacitor and 1% resistors.

## Designing for a target frequency

For 1 kHz with C = 10 nF and R1 = 1 kΩ, rearrange f = 1.44 ÷ ((R1 + 2R2) C): R2 = (1.44 ÷ (1,000 × 10 nF) − 1,000) ÷ 2 = {R2d/1000:.1f} kΩ. The nearest E12 value, 68 kΩ, gives {f_chk:.0f} Hz at {D_chk*100:.1f}% duty. Measure the result on pin 3 with an oscilloscope or a multimeter frequency range, and trim with a potentiometer in series with R2 if the exact value matters.

## Common mistakes

- **Making R1 very small.** When the discharge transistor turns on, pin 7 shorts R1 to ground; with 100 Ω on a 9 V supply that is {I_dis_100*1000:.0f} mA through the transistor, well above what it is meant to sink.
- **Using huge resistors with an electrolytic.** Above a few hundred kΩ, capacitor leakage current becomes comparable to the charging current and the period stretches or the timer stops.
- **Leaving reset (pin 4) floating.** It can pick up noise and stop the oscillator at random; tie it to V<sub>cc</sub>.
- **No supply decoupling on the bipolar NE555.** Its output stage draws a current spike at every transition, so put 100 nF close to pins 8 and 1.
- **Expecting below 50% duty from the standard circuit.** t<sub>H</sub> always includes R1, so it is always longer than t<sub>L</sub>.
''',
     faq_add=[('Why is the first 555 output pulse longer than the rest?',
               f'At switch on the capacitor charges from 0 V instead of one third of the supply, so the first high time is ln 3 × (R1 + R2) × C. With the default parts that is {th_first*1000:.1f} ms instead of {th*1000:.1f} ms.'),
              ('Does the supply voltage change the 555 frequency?',
               'Ideally no, because the thresholds are fixed fractions of the supply and the charging current scales with it too. In practice the NE555 datasheet quotes a drift of about 0.1% per volt, unless pin 5 is driven externally.')])

# ---------------------------------------------------------------- PCB trace width
I, dT, oz, k = 3.0, 10.0, 1.0, 0.048


def area(I, dT, k):
    return (I / (k * dT ** 0.44)) ** (1 / 0.725)


A = area(I, dT, k)
wm = A / (1.378 * oz)
w = wm * 0.0000254
assert abs(wm - 53.8) < 0.2 and abs(w * 1000 - 1.367) < 0.005
k_dT = dT ** 0.44
base = I / (k * k_dT)
# internal layer
A_int = area(I, dT, 0.024)
wm_int = A_int / 1.378
ratio_int = wm_int / wm
# resistance and drop for 50 mm of the default trace at 20 C
rho_cu = 1.72e-8
t_m = 35e-6
L_m = 0.050
R_tr = rho_cu * L_m / (w * t_m)
Vdrop = I * R_tr
Ploss = I ** 2 * R_tr
sq = L_m / w
# temperature rise table at 3 A
dt_rows = ''
for d in (5, 10, 20, 30, 45):
    a = area(I, d, k)
    dt_rows += f"| {d} °C | {a/1.378*0.0254:.2f} mm | {a/(1.378*2)*0.0254:.2f} mm | {area(I, d, 0.024)/1.378*0.0254:.2f} mm |\n"
w20 = area(I, 20, k) / 1.378 * 0.0254

edit('electronics/pcb-trace-width', date=U, phrase='pcb trace width calculator',
     intro=("A copper track heats up as current flows through it, so it must be wide enough to stay within a chosen temperature rise. "
            "This PCB trace width calculator applies the IPC-2221 formula to current, temperature rise, copper weight and layer; for vias, see "
            "[PCB via current capacity](https://www.instrumentationblog.in/pcb-via-current-capacity/).\n\n"
            "PCB designers and hardware engineers use it to size power rails, motor and LED drive tracks and heater feeds before routing, so boards do not overheat or drop voltage."),
     body_add=f'''
## Worked example with the default values

For 3 A on an outer layer of 1 oz copper with a 10 °C rise:

1. ΔT<sup>0.44</sup> = 10<sup>0.44</sup> = {k_dT:.3f}
2. A = (3 ÷ (0.048 × {k_dT:.3f}))<sup>1/0.725</sup> = {base:.2f}<sup>{1/0.725:.3f}</sup> = **{A:.1f} mil²**
3. Width = {A:.1f} ÷ (1.378 × 1) = **{wm:.1f} mil**, which is **{w*1000:.2f} mm**

The same current on an inner layer needs {wm_int:.0f} mil ({wm_int*0.0254:.2f} mm), {ratio_int:.1f} times wider. Halving k does not just double the area, because area appears with the exponent 0.725.

## Voltage drop along the trace

A 50 mm run of that {w*1000:.2f} mm, 35 µm trace is {sq:.0f} squares long. Using copper resistivity of 1.72 × 10<sup>−8</sup> Ω·m at 20 °C, R = ρL ÷ (w × t) = **{R_tr*1000:.1f} mΩ**, so 3 A drops {Vdrop*1000:.0f} mV and dissipates {Ploss*1000:.0f} mW. On a 3.3 V rail feeding a processor that drop may matter more than the heating, so check both.

## Width against allowed temperature rise at 3 A

| Rise | External, 1 oz | External, 2 oz | Internal, 1 oz |
|---|---|---|---|
{dt_rows}
Allowing 20 °C instead of 10 °C shrinks the outer 1 oz trace to {w20:.2f} mm. Add the rise to the worst case ambient inside the enclosure and keep the total well below the laminate rating, typically 130 °C for standard FR-4.

## Checking a built board

Run the board at full current and measure the trace with a thermal camera or a thermocouple taped to the copper, after it settles for 10 to 15 minutes. A four wire milliohm measurement across the trace also confirms the copper weight the fabricator delivered.

## Common mistakes

- **Sizing on the wide part and forgetting neck downs.** A trace that narrows to 0.3 mm at a connector or IC pad heats at that point; keep the full width as close to the pad as possible.
- **Assuming outer layer plating.** Fabricators quote base copper; 1 oz base usually finishes thicker on outer layers after plating, but inner layers stay at base thickness.
- **Using IPC-2221 outside its range.** The chart fits currents up to about 35 A, widths up to 400 mil and 10 to 100 °C rise; beyond that use IPC-2152 or thermal simulation.
- **Ignoring thermal reliefs and vias.** Spoke connections to a plane and a single via can carry less than the trace feeding them.
- **Putting parallel high current traces side by side.** Neighbouring hot traces heat each other, so the real rise is higher than the single trace figure.
''',
     faq_add=[('How much voltage does a PCB trace drop?',
               f'Multiply current by trace resistance, R = ρL ÷ (w × t). A 50 mm run of {w*1000:.2f} mm wide 1 oz copper is about {R_tr*1000:.1f} mΩ, so 3 A drops about {Vdrop*1000:.0f} mV.')])

# ---------------------------------------------------------------- Voltage divider
Vin, R1v, R2v = 12.0, 10e3, 4.7e3
Vout = Vin * R2v / (R1v + R2v)
Iv = Vin / (R1v + R2v)
Pv = Vin * Iv
assert abs(Vout - 3.8367) < 1e-3 and abs(Iv * 1000 - 0.8163) < 1e-3 and abs(Pv * 1000 - 9.796) < 1e-2
Rth = R1v * R2v / (R1v + R2v)
P1 = Iv ** 2 * R1v
P2 = Iv ** 2 * R2v
load_rows = ''
for RL in (4.7e3, 47e3, 100e3, 1e6, 10e6):
    v = Vout * RL / (RL + Rth)
    load_rows += f"| {RL/1e3:,.1f} kΩ | {v:.3f} V | {(v/Vout-1)*100:+.2f}% |\n"
RL47 = 47e3
V47 = Vout * RL47 / (RL47 + Rth)
# 1% tolerance worst case
Vmax = Vin * R2v * 1.01 / (R1v * 0.99 + R2v * 1.01)
Vmin = Vin * R2v * 0.99 / (R1v * 1.01 + R2v * 0.99)
# 10x scaled divider
I10 = Vin / (100e3 + 47e3)

edit('electronics/voltage-divider', date=U, phrase='voltage divider calculator',
     intro=("Two resistors in series split a voltage in proportion to their values, giving a smaller output at their junction. "
            "This voltage divider calculator finds that output voltage, the divider current and the power wasted, as set out in the "
            "[voltage divider rule explained](https://www.instrumentationblog.in/voltage-divider-rule-explained/), which follows from "
            "[Kirchhoff's voltage law](https://www.instrumentationblog.in/kirchhoffs-voltage-law-kvl-explained/).\n\n"
            "Electronics designers and students use it to scale sensor and battery voltages for ADC inputs, set regulator feedback and bias transistors."),
     body_add=f'''
## Worked example with the default values

12 V across R1 = 10 kΩ and R2 = 4.7 kΩ:

- Total resistance = 14.7 kΩ, so I = 12 ÷ 14,700 = **{Iv*1000:.3f} mA**
- V<sub>out</sub> = 12 × 4.7 ÷ 14.7 = **{Vout:.3f} V**
- Power = 12 × {Iv*1000:.3f} mA = **{Pv*1000:.2f} mW**, of which R1 takes {P1*1000:.2f} mW and R2 {P2*1000:.2f} mW

Even the larger share is tiny, so 0.125 W parts are fine here. Seen from the output, the divider behaves like a {Vout:.3f} V source with an internal resistance of R1 ∥ R2 = **{Rth/1e3:.2f} kΩ**, which is the number that decides how much a load pulls it down.

## How much a load pulls the output down

Using that {Rth/1e3:.2f} kΩ source resistance:

| Load across R2 | Output | Change |
|---|---|---|
{load_rows}
The common rule of keeping the load at ten times R2 (47 kΩ here) still costs {(V47/Vout-1)*100:.1f}%. For a measurement input, aim for a load at least 100 to 1,000 times the source resistance, or buffer it.

## Resistor tolerance

With 1% resistors the worst case is R1 low and R2 high, or the reverse. The default divider can then give anything from {Vmin:.3f} V to {Vmax:.3f} V, about ±{(Vmax-Vout)/Vout*100:.1f}%. Ratio errors do not cancel unless both resistors come from the same matched network.

## In practice

When feeding a microcontroller ADC, the sampling capacitor charges through the source resistance on every conversion; many datasheets ask for 10 kΩ or less, which the {Rth/1e3:.2f} kΩ default meets. Scaling both resistors up ten times to 100 kΩ and 47 kΩ cuts the current to {I10*1e6:.0f} µA, but then a 10 to 100 nF capacitor from the output to ground is needed to hold the voltage during sampling. Check a built divider by measuring V<sub>out</sub> with the load connected, not with the meter alone.

## Common mistakes

- **Swapping R1 and R2.** The output is taken across the bottom resistor; reversing them gives 12 × 10 ÷ 14.7 = {12*10/14.7:.2f} V, which could damage a 3.3 V input.
- **Powering a load from a divider.** Any load current changes the output, and the resistors waste power continuously.
- **Ignoring resistor voltage rating.** A small SMD resistor is often rated around 50 to 200 V, so a mains or high voltage divider needs several resistors in series.
- **Leaving a divider on a battery permanently.** Even a fraction of a milliamp drains a small battery over months; switch it with a MOSFET or use megohm values.
- **Using very high values near noise sources.** Megohm dividers pick up interference and leakage, so add a filter capacitor across R2.
''',
     faq_add=[('What is the output impedance of a voltage divider?',
               f'It is R1 and R2 in parallel, R1 × R2 ÷ (R1 + R2). For 10 kΩ and 4.7 kΩ that is {Rth/1e3:.2f} kΩ, and any load sees the divider as a {Vout:.3f} V source behind that resistance.')])

# ---------------------------------------------------------------- Capacitor lifetime
L0, T0, T = 2000.0, 105.0, 55.0


def life(L0, T0, T):
    return L0 * 2 ** ((T0 - T) / 10)


Lx = life(L0, T0, T)
y = Lx / 8760
assert abs(Lx - 64000) < 1e-6 and abs(y - 7.306) < 0.001
fac = 2 ** ((T0 - T) / 10)
# ripple self heating: P = I^2 ESR, rise = P x Rth (assumed datasheet thermal resistance)
Irip, esr, rth = 1.5, 0.10, 30.0
Prip = Irip ** 2 * esr
dT_rip = Prip * rth
Tamb = T - dT_rip
# hotter enclosure
L65 = life(L0, T0, 65)
L60 = life(L0, T0, 60)
# duty table: calendar years for different running hours per day
duty_rows = ''
for hpd in (24, 16, 8):
    for LL, lbl in ((Lx, '55 °C'), (L65, '65 °C')):
        duty_rows += f"| {hpd} h/day | {lbl} | {c(LL)} h | {LL/(hpd*365):.1f} years |\n"
# polymer capacitors: 10x per 20 C
Lpoly = L0 * 10 ** ((T0 - T) / 20)

edit('electronics/capacitor-lifetime', date=U, phrase='capacitor life calculator',
     intro=("Aluminium electrolytic capacitors wear out as their electrolyte slowly dries, and heat speeds this up. "
            "This electrolytic capacitor life calculator applies the 10 degree rule to the rated hours and temperature; see this "
            "[electrolytic capacitor lifetime calculation](https://www.instrumentationblog.in/electrolytic-capacitor-lifetime-calculation/) and the "
            "[failure modes of electrolytic, ceramic and tantalum capacitors](https://www.instrumentationblog.in/electrolytic-vs-ceramic-vs-tantalum-capacitor-failure-modes/).\n\n"
            "Power supply designers and maintenance engineers use it to choose capacitor series and plan replacement in drives, UPSs and SMPS units."),
     body_add=f'''
## Worked example with the default values

A 2,000 h, 105 °C capacitor running with its core at 55 °C:

1. Temperature margin = 105 − 55 = 50 °C, which is 5 steps of 10 °C
2. Life factor = 2<sup>5</sup> = **{fac:.0f}**
3. L = 2,000 × {fac:.0f} = **{c(Lx)} h**, or {c(Lx)} ÷ 8,760 = **{y:.1f} years** of continuous running

## Where the core temperature comes from

The core is the ambient around the can plus the heat the ripple current makes in the ESR. Suppose the capacitor carries {Irip} A RMS ripple with an ESR of {esr*1000:.0f} mΩ, and the datasheet gives a thermal resistance of {rth:.0f} °C/W for that can size. It dissipates {Irip}² × {esr} = {Prip:.3f} W, a rise of {Prip:.3f} × {rth:.0f} = **{dT_rip:.2f} °C**. A core of 55 °C therefore means an ambient of about {Tamb:.0f} °C. If the enclosure warms to give a 65 °C core, life halves to {c(L65)} h ({L65/8760:.1f} years).

## Calendar life by running hours

| Operation | Core temperature | Life in hours | Calendar life |
|---|---|---|---|
{duty_rows}
Figures above about 15 years are not reliable, because the rubber seal and the oxide layer age even at low temperature.

## Checking capacitors in service

Measure the can top with a thermocouple or thermal camera at full load; the core is normally a few degrees hotter than the case top. During maintenance, an ESR meter or LCR meter shows wear: datasheets usually define end of life as capacitance falling more than 20%, tan δ rising above twice the initial limit, or leakage exceeding the specification. A bulging vent or electrolyte residue means the part is already past end of life.

## Common mistakes

- **Using room temperature instead of core temperature.** A cabinet at 25 °C can still have capacitors at 60 °C next to a heat sink.
- **Applying the 10 degree rule to polymer capacitors.** Conductive polymer types usually follow a 20 degree rule; for the same rating at 55 °C they would give {c(Lpoly)} h, so use the maker's formula.
- **Counting calendar time when the equipment is mostly off.** Life is consumed only at temperature, so a machine running 8 h a day lasts three times as many years.
- **Extrapolating far below 40 °C.** The doubling rule overstates life at low temperature, where seal ageing dominates.
- **Mixing up load life and shelf life.** Rated hours apply with voltage and ripple applied; capacitors stored unpowered for years may need reforming before use.
''',
     faq_add=[('How much does ripple current shorten capacitor life?',
               f'Ripple heats the core by I² × ESR multiplied by the thermal resistance. For {Irip} A through {esr*1000:.0f} mΩ with {rth:.0f} °C/W the core rises about {dT_rip:.1f} °C, which on its own cuts the estimated life by about {(1-2**(-dT_rip/10))*100:.0f}%.')])

print('done', inplace.DONE)
for cid in inplace.DONE:
    print(cid, inplace.body_words(cid))

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-23), slice 2: air-core-inductor, differential-amplifier, adc-resolution, antenna-length, mosfet-power-loss.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-23'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Air core inductor


def wheeler(D_mm, l_mm, N):
    d, l = D_mm / 25.4, l_mm / 25.4
    return d * d * N * N / (18 * d + 40 * l)  # uH


D, l, N = 20.0, 30.0, 25
L0 = wheeler(D, l, N)
w0 = N * math.pi * D / 1000
assert abs(L0 - 6.309) < 0.001 and abs(w0 - 1.5708) < 1e-3
pitch = l / N
# turns for 10 uH at the same former and length
d_in, l_in = D / 25.4, l / 25.4
N10 = math.sqrt(10 * (18 * d_in + 40 * l_in)) / d_in
N10r = math.ceil(N10)
L10r = wheeler(D, l, N10r)
pitch10 = l / N10r
# resonance with 100 pF
Cp = 100e-12
f_res = 1 / (2 * math.pi * math.sqrt(L0 * 1e-6 * Cp))
# measuring diameter at outside of 1 mm wire
L_out = wheeler(21.0, l, N)
err_out = (L_out / L0 - 1) * 100
# stretching the coil to tune
L_str = wheeler(D, 36.0, N)
len_rows = ''
for ll in (10, 15, 20, 30, 45, 60):
    Lx = wheeler(D, ll, N)
    note = 'yes' if ll >= 0.4 * D else 'no'
    len_rows += f"| {ll} mm | {ll/D:.2f} | {Lx:.2f} µH | {note} |\n"

edit('electronics/air-core-inductor', date=U, phrase='air core inductor calculator',
     intro=("A single-layer air-core coil has no magnetic core to saturate, so its inductance stays fixed with current and temperature. "
            "This air core inductor calculator applies Wheeler's formula to coil diameter, length and turns; see "
            "[how an inductor works](https://www.instrumentationblog.in/inductor-working-principle/).\n\n"
            "Radio amateurs, RF designers and audio builders use it to wind coils for tuned circuits, filters, matching networks and "
            "loudspeaker crossovers, and to work out how much wire to cut before winding."),
     body_add=f'''
## Second example: winding for a target of 10 µH

Keep the default 20 mm former and 30 mm winding length and ask for 10 µH. Rearranging Wheeler's formula gives N = √(L × (18d + 40l)) ÷ d:

- 18 × {d_in:.3f} + 40 × {l_in:.3f} = {18*d_in + 40*l_in:.2f}
- N = √(10 × {18*d_in + 40*l_in:.2f}) ÷ {d_in:.3f} = **{N10:.2f} turns**, so wind **{N10r}**
- {N10r} turns give {L10r:.2f} µH and need about {N10r*math.pi*D/1000:.2f} m of wire

Squeezing {N10r} turns into 30 mm leaves a pitch of {pitch10:.2f} mm, so the wire must be thinner than about {pitch10:.2f} mm including enamel. The default 25 turn coil has a {pitch:.2f} mm pitch, which suits 1.0 mm enamelled wire with a small gap.

## Effect of coil length (20 mm diameter, 25 turns)

| Winding length | l ÷ D | Inductance | Within 1% range |
|---|---|---|---|
{len_rows}
Stretching the default coil from 30 mm to 36 mm drops it from {L0:.2f} µH to {L_str:.2f} µH, which is the usual way to fine tune a coil after winding.

## Checking a wound coil

Measure inductance with an LCR meter at a frequency well below the self-resonant frequency, or resonate the coil with a known capacitor and read the frequency. With 100 pF across the default {L0:.2f} µH coil, resonance should fall at **{f_res/1e6:.2f} MHz**; a lower reading points to extra capacitance from leads and fixture.

## Common mistakes

- **Entering the outside diameter.** With 1 mm wire on a 20 mm centre diameter, typing 21 mm gives {L_out:.2f} µH, {err_out:.0f}% too high.
- **Forgetting the leads.** Straight leads add roughly 1 nH per millimetre, which matters for coils below about 0.5 µH.
- **Using the formula for multilayer or pancake coils.** Wheeler's single layer expression does not apply; those shapes have their own formulas.
- **Mounting the coil against metal.** A nearby chassis or ground plane induces eddy currents and lowers both inductance and Q; keep about one coil diameter of clearance.
- **Cutting the wire to the exact length shown.** The figure excludes leads, so add a few centimetres for each end.
''',
     faq_add=[('How many turns do I need for 10 µH on a 20 mm former?',
               f'With a 30 mm winding length, Wheeler\'s formula gives {N10:.2f} turns, so wind {N10r} turns for about {L10r:.2f} µH. The wire must be thinner than {pitch10:.2f} mm to fit.'),
              ('How do I fine tune an air core coil after winding?',
               f'Spread or compress the turns. Stretching the default 25 turn coil from 30 mm to 36 mm lowers it from {L0:.2f} µH to {L_str:.2f} µH. Compressing the turns raises inductance.')])

# ---------------------------------------------------------------- Differential amplifier


def diff(V1, V2, R1, R2, R3, R4):
    a = R4 / (R3 + R4) * (1 + R2 / R1)
    Vout = a * V2 - R2 / R1 * V1
    Ad = (a + R2 / R1) / 2
    Acm = a - R2 / R1
    return Vout, Ad, Acm


V1, V2, R1, R2, R3, R4 = 1.0, 1.2, 10.0, 100.0, 10.0, 100.0
Vo, Ad, Acm = diff(V1, V2, R1, R2, R3, R4)
assert abs(Vo - 2.0) < 1e-9 and abs(Ad - 10) < 1e-9 and abs(Acm) < 1e-12
Vplus = V2 * R4 / (R3 + R4)
# R4 one percent high
Vo_m, Ad_m, Acm_m = diff(V1, V2, R1, R2, R3, 101.0)
cmrr_m = 20 * math.log10(Ad_m / abs(Acm_m))
# shunt on a 12 V rail: both inputs near 12 V
Vo_hs, _, _ = diff(12.0, 12.2, R1, R2, R3, 101.0)
err_hs = Vo_hs - 2.0
# source impedance of 100 ohm on V1 side
Vo_s, Ad_s, Acm_s = diff(V1, V2, 10.1, R2, R3, R4)
mis_rows = ''
for p in (0.01, 0.1, 0.5, 1.0, 5.0):
    _, a_d, a_c = diff(V1, V2, R1, R2, R3, 100 * (1 + p / 100))
    mis_rows += f"| {p:g}% | {a_c:.5f} | {20*math.log10(a_d/abs(a_c)):.1f} dB | {a_c*12*1000:.1f} mV |\n"

edit('electronics/differential-amplifier', date=U, phrase='differential amplifier calculator',
     intro=("The four-resistor op-amp subtractor amplifies the difference between two voltages while rejecting the voltage they share. "
            "This differential amplifier calculator gives the output, differential gain and common-mode gain for any resistor values; see "
            "[differential amplifier basics and CMRR](https://www.instrumentationblog.in/differential-amplifier-explained-basics-and-cmrr/).\n\n"
            "Circuit designers and instrumentation technicians use it to size current shunt amplifiers, level shifters and bridge interfaces, "
            "and to see how resistor mismatch lets common-mode voltage leak into the output."),
     body_add=f'''
## Second example: one resistor 1% high

Keep the default inputs but let R₄ be 101 kΩ instead of 100 kΩ:

- R₄ ÷ (R₃ + R₄) × (1 + R₂/R₁) = 101/111 × 11 = {101/111*11:.4f}
- V<sub>out</sub> = {101/111*11:.4f} × 1.2 − 10 × 1 = **{Vo_m:.4f} V** instead of 2.0000 V
- A<sub>cm</sub> = {101/111*11:.4f} − 10 = **{Acm_m:.5f}**, A<sub>d</sub> = **{Ad_m:.4f}**
- CMRR = 20 log({Ad_m:.4f} ÷ {Acm_m:.5f}) = **{cmrr_m:.1f} dB**

That is better than the 49 dB worst case in the table above because only one resistor is off; the table assumes all four sit at the edge of tolerance in the worst direction.

## Why mismatch matters on a high-side shunt

Now put the same 0.2 V difference on top of a 12 V rail (V₁ = 12 V, V₂ = 12.2 V). With matched resistors the output is still 2.0 V, but with R₄ 1% high it becomes {Vo_hs:.3f} V, an error of {err_hs*1000:.0f} mV, or {err_hs/2*100:.1f}% of reading. The error scales with common-mode voltage:

| R₄ error | Common-mode gain | CMRR | Output error at 12 V common mode |
|---|---|---|---|
{mis_rows}
## Checking the op-amp input range

With the default values the non-inverting input sits at 1.2 × 100/110 = **{Vplus:.3f} V**, and the inverting input follows it. On a 12 V rail the inputs sit near {12.2*100/110:.2f} V, so the op-amp needs a supply above that or a different resistor ratio. To measure CMRR on the bench, tie both inputs together, drive them with a known voltage, and divide the output change by the input change.

## Common mistakes

- **Ignoring source resistance.** A 100 Ω source on the V₁ side makes R₁ effectively 10.1 kΩ, giving A<sub>cm</sub> = {Acm_s:.4f} even with perfect resistors.
- **Driving the reference pin from a divider.** The bottom of R₄ must see a low impedance, otherwise the divider resistance adds to R₄ and unbalances the ratio; buffer it.
- **Swapping V₁ and V₂.** The output polarity reverses, and on a single supply the op-amp simply sits at the negative rail.
- **Forgetting output swing.** A gain of 10 on a 0.5 V difference needs 5 V of output, which a rail-to-rail op-amp on 5 V cannot quite reach.
- **Mixing tolerances in one circuit.** One 5% resistor among 0.1% parts sets the CMRR on its own.
''',
     faq_add=[('What voltage appears at the op-amp inputs of a differential amplifier?',
               f'The non-inverting input sits at V₂ × R₄ ÷ (R₃ + R₄), and feedback holds the inverting input at the same voltage. With the default values that is {Vplus:.3f} V, which must stay inside the op-amp input range.'),
              ('Can a differential amplifier measure across a shunt above its supply voltage?',
               'Yes, if R₄ ÷ (R₃ + R₄) divides the input down enough. Using R₂/R₁ = R₄/R₃ below 1 attenuates the common-mode voltage at the inputs, at the cost of a lower differential gain that a later stage can restore.')])

# ---------------------------------------------------------------- ADC resolution
n, Vr, Vin = 12, 3.3, 1.65
Nl = 2 ** n
lsb = Vr / Nl
code = min(math.floor(Vin / lsb), Nl - 1)
snr = 6.02 * n + 1.76
assert Nl == 4096 and abs(lsb * 1000 - 0.80566) < 1e-4 and code == 2048 and abs(snr - 74.0) < 1e-9
qn = lsb / math.sqrt(12)
lsb_alt = Vr / (Nl - 1)
# sensor 10 mV per degC
degc_per_count = lsb / 0.010
t_span = Vr / 0.010
# ENOB from a measured SNR of 66 dB
snr_meas = 66.0
enob = (snr_meas - 1.76) / 6.02
# reference error of 1%
ref_err_counts = 0.01 * Vr / lsb
os_rows = ''
for k in (0, 1, 2, 3, 4):
    os_rows += f"| {k} | {4**k:,} | {n+k} | {Vr/2**(n+k)*1e3:.4f} mV |\n"

edit('electronics/adc-resolution', date=U, phrase='adc resolution calculator',
     intro=("An analog-to-digital converter turns a voltage into a number, and its bit depth sets the smallest change it can see. "
            "This ADC resolution calculator gives the levels, step size, output code and ideal SNR; see "
            "[analog-to-digital conversion explained](https://www.instrumentationblog.in/analog-to-digital-conversion-explained/).\n\n"
            "Embedded engineers, PLC programmers and instrument technicians use it to choose converters, scale raw counts and judge "
            "[analog signal resolution in PLCs](https://www.instrumentationblog.in/analog-signal-resolution-in-plc/)."),
     body_add=f'''
## Worked example with the default values

A 12-bit ADC with a 3.3 V reference reading 1.65 V:

1. Levels = 2¹² = **{Nl:,}**
2. LSB = 3.3 ÷ {Nl:,} = **{lsb*1e3:.4f} mV**
3. Code = ⌊1.65 ÷ {lsb*1e3:.4f} mV⌋ = **{code:,}**
4. Ideal SNR = 6.02 × 12 + 1.76 = **{snr:.2f} dB**

Code {code:,} covers every input from {code*lsb:.5f} V up to {(code+1)*lsb:.5f} V, so the reading carries an uncertainty of one LSB, or ±{lsb/2*1e3:.3f} mV about the centre of the step. Treated as noise, that quantisation error has an RMS value of LSB ÷ √12 = {qn*1e3:.4f} mV, which is where the 6.02n + 1.76 dB figure comes from.

## What one count means for a sensor

A temperature sensor with a 10 mV/°C output on this converter resolves {lsb*1e3:.4f} mV ÷ 10 mV = **{degc_per_count:.4f} °C per count** and spans 0 to {t_span:.0f} °C at full scale. If the process only runs 0 to 100 °C, two thirds of the codes go unused; an amplifier gain of about 3 restores the resolution.

## Oversampling for extra bits

| Extra bits | Samples averaged | Effective bits | Effective LSB at 3.3 V |
|---|---|---|---|
{os_rows}
This only works when at least about one LSB of random noise is present; a perfectly quiet input returns the same code every time and averaging gains nothing.

## Common mistakes

- **Dividing by 2ⁿ − 1.** Some datasheets define full scale at code {Nl-1:,}, giving {lsb_alt*1e3:.4f} mV per count; check which convention the part uses.
- **Trusting the reference.** A 1% reference error shifts full scale by {Vr*0.01*1000:.0f} mV, about {ref_err_counts:.0f} counts, far more than the resolution.
- **Confusing resolution with accuracy.** Offset, gain and linearity errors are specified separately and usually exceed 1 LSB.
- **Feeding a SAR ADC from a high source impedance.** The sampling capacitor cannot charge within the acquisition time, so readings sag; buffer the input or lengthen the sample time.
- **Expecting all bits to be useful.** A measured SNR of {snr_meas:.0f} dB means ENOB = ({snr_meas:.0f} − 1.76) ÷ 6.02 = {enob:.2f} bits, not 12.
''',
     faq_add=[('How do I calculate ENOB from SNR?',
               f'ENOB = (SINAD − 1.76) ÷ 6.02, using the measured signal to noise and distortion ratio in dB. A 12-bit ADC measuring {snr_meas:.0f} dB has an ENOB of about {enob:.2f} bits.'),
              ('What is ADC quantisation noise?',
               f'The rounding error of each conversion, spread evenly over one LSB, has an RMS value of LSB ÷ √12. For a 12-bit, 3.3 V converter that is {qn*1e3:.4f} mV.')])

# ---------------------------------------------------------------- Antenna length
f, k = 433.92e6, 0.95
lam = 299792458 / f
Lh = 0.5 * lam * k
Lg = Lh / 2
Lq = 0.25 * lam * k
assert abs(lam * 100 - 69.089) < 0.001 and abs(Lh * 100 - 32.818) < 0.001 and abs(Lq * 100 - 16.409) < 0.001
# trimming: measured resonance at 420 MHz
f_meas = 420e6
Lh_new = Lh * f_meas / f
trim = (Lh - Lh_new) * 100
# insulated wire k = 0.92
Lh_ins = 0.5 * lam * 0.92
sw_rows = ''
for s in (1.1, 1.5, 2.0, 3.0, 5.0):
    g = (s - 1) / (s + 1)
    sw_rows += f"| {s:.1f} | {g:.3f} | {-20*math.log10(g):.1f} dB | {g*g*100:.1f}% | {-10*math.log10(1-g*g):.2f} dB |\n"
g15 = 0.2

edit('electronics/antenna-length', date=U, phrase='antenna length calculator',
     intro=("A resonant antenna is cut to a fraction of a wavelength, half for a dipole and a quarter for a ground-plane whip, then shortened slightly for end effects. "
            "This antenna length calculator gives the wavelength and the practical dipole, leg and quarter-wave lengths for any frequency.\n\n"
            "Radio amateurs, IoT developers and installers of ISM band telemetry use it to cut wire antennas, set a starting length before trimming "
            "and check that a module's whip suits its band."),
     body_add=f'''
## Second example: trimming to resonance

Cut the default 433.92 MHz dipole to {Lh*100:.2f} cm and sweep it with an antenna analyser. Suppose the lowest SWR appears at 420 MHz, so the antenna is electrically long. Length scales inversely with frequency:

- New length = {Lh*100:.2f} × 420 ÷ 433.92 = **{Lh_new*100:.2f} cm**
- Remove **{trim:.2f} cm** in total, about {trim/2:.2f} cm from each leg

Trim in two or three steps rather than all at once, because the first cut also changes how the feed line and nearby objects interact with the antenna. Insulated wire slows the wave slightly; with k = 0.92 the starting length is {Lh_ins*100:.2f} cm.

## Reading SWR from the analyser

| VSWR | Reflection coefficient | Return loss | Power reflected | Mismatch loss |
|---|---|---|---|---|
{sw_rows}
Below 1.5:1 only {g15*g15*100:.0f}% of the power comes back, so chasing a perfect 1.0 is rarely worth the effort. A centre fed half-wave dipole in free space presents about 73 Ω, and a quarter-wave monopole over a good ground plane about 36 Ω; drooping ground-plane radials downward to about 45° raises the monopole toward 50 Ω.

## Practical placement

Mount the antenna clear of metal and away from the circuit board's noisy sections. A plastic enclosure, a hand or a wall within a few centimetres lowers the resonant frequency, so do the final trim with the antenna installed in its housing.

## Common mistakes

- **Using the coax velocity factor.** The 0.66 or 0.82 figure on a cable data sheet applies to the feed line, not the radiating wire.
- **Confusing total length with leg length.** At 433.92 MHz each leg is {Lg*100:.2f} cm; making each leg {Lh*100:.2f} cm gives a full wave dipole with a high feed impedance.
- **Running a quarter-wave whip without a ground plane.** The feed line becomes the missing half and the pattern and match become unpredictable.
- **Trimming in free air, then fitting the case.** The enclosure shifts resonance by several megahertz at UHF.
- **Coiling surplus wire.** A coiled length acts as an inductor and detunes the antenna; cut it instead.
''',
     faq_add=[('How much should I trim if my antenna resonates too low?',
               f'Multiply the present length by the measured resonant frequency divided by the target. A {Lh*100:.2f} cm dipole resonating at 420 MHz needs to become {Lh_new*100:.2f} cm for 433.92 MHz, removing about {trim/2:.2f} cm from each leg.'),
              ('What is the feed impedance of a half-wave dipole?',
               'About 73 Ω at the centre in free space, falling when the dipole is close to the ground. A quarter-wave monopole over a ground plane is about half that, roughly 36 Ω.')])

# ---------------------------------------------------------------- MOSFET power loss
I, Rds, V, fs, tsw, Rth, Ta = 10.0, 0.020, 24.0, 50e3, 100e-9, 40.0, 40.0


def mos(I, Rds, V, fs, tsw, Rth, Ta):
    Pc = I ** 2 * Rds
    Ps = 0.5 * V * I * tsw * fs
    P = Pc + Ps
    return Pc, Ps, P, Ta + P * Rth


Pc, Ps, P, Tj = mos(I, Rds, V, fs, tsw, Rth, Ta)
assert abs(Pc - 2.0) < 1e-9 and abs(Ps - 0.6) < 1e-9 and abs(P - 2.6) < 1e-9 and abs(Tj - 144) < 1e-9
Tj_target = 100.0
Rth_need = (Tj_target - Ta) / P
Rjc, Rcs = 1.0, 0.5
Rsa = Rth_need - Rjc - Rcs
# parallel devices
Pc_each = (I / 2) ** 2 * Rds
# Coss loss
Coss = 500e-12
Pcoss_24 = 0.5 * Coss * V ** 2 * fs
Pcoss_400 = 0.5 * Coss * 400 ** 2 * fs
# gate drive
Qg, Vgs = 30e-9, 10.0
Pg = Qg * Vgs * fs
# PWM rms: 14.14 A peak at 50% duty
Ipk = 10 * math.sqrt(2)
fr_rows = ''
for fk in (20, 50, 100, 200, 500):
    a, b, p, t = mos(I, Rds, V, fk * 1e3, tsw, Rth, Ta)
    fr_rows += f"| {fk} kHz | {a:.2f} W | {b:.2f} W | {p:.2f} W | {t:.0f} °C |\n"

edit('electronics/mosfet-power-loss', date=U, phrase='mosfet power dissipation calculator',
     intro=("A MOSFET used as a switch loses power through its on-resistance while conducting and again during every turn-on and turn-off. "
            "This MOSFET power dissipation calculator estimates both losses and the junction temperature; see "
            "[what a MOSFET is](https://www.instrumentationblog.in/what-is-a-mosfet-working-principle/).\n\n"
            "Power electronics designers use it to choose a device, set the switching frequency and decide on heat sinking, and to check "
            "[MOSFET gate driver ICs](https://www.instrumentationblog.in/mosfet-gate-driver-ics-explained/) switch fast enough."),
     body_add=f'''
## Second example: sizing the heat sink

The default case reaches {Tj:.0f} °C, too hot for a reliable design. To hold the junction at {Tj_target:.0f} °C with {P:.1f} W of loss and {Ta:.0f} °C ambient:

- Total thermal resistance allowed = ({Tj_target:.0f} − {Ta:.0f}) ÷ {P:.1f} = **{Rth_need:.2f} °C/W**
- Subtract junction to case ({Rjc:.1f} °C/W) and the thermal pad ({Rcs:.1f} °C/W)
- The heat sink must be **{Rsa:.2f} °C/W** or better

Enter {Rth_need:.2f} in the thermal resistance field to confirm {Tj_target:.0f} °C. Because R<sub>DS(on)</sub> falls as the device cools, the real loss is slightly lower, so this is a safe answer.

## How frequency shifts the balance

Same 10 A, 20 mΩ, 24 V and 100 ns, with no heat sink (40 °C/W):

| Frequency | Conduction | Switching | Total | T<sub>j</sub> |
|---|---|---|---|---|
{fr_rows}
Conduction dominates up to about {Pc/(0.5*V*I*tsw)/1e3:.0f} kHz, where switching loss equals it. Above that, a faster gate driver is worth more than a lower R<sub>DS(on)</sub>.

## Measuring the real loss

Fit a thermocouple to the tab, run the converter at full load until the temperature settles, then estimate T<sub>j</sub> = T<sub>case</sub> + P × R<sub>θJC</sub>. For the switching loss itself, capture V<sub>DS</sub> and I<sub>D</sub> on an oscilloscope with a current probe, deskew the channels, and integrate their product over each transition.

## Common mistakes

- **Using average current instead of RMS.** A 50% duty PWM drawing {Ipk:.2f} A peak has an RMS of 10 A but an average of only {Ipk/2:.2f} A; squaring the average halves the conduction loss.
- **Using R<sub>θJA</sub> with a heat sink fitted.** The datasheet R<sub>θJA</sub> assumes a small copper pad; with a sink, add R<sub>θJC</sub>, interface and sink values.
- **Forgetting output capacitance loss.** ½C<sub>oss</sub>V²f with 500 pF is only {Pcoss_24*1000:.1f} mW at 24 V but {Pcoss_400:.1f} W at 400 V and 50 kHz.
- **Counting gate charge as MOSFET heat.** Q<sub>g</sub> × V<sub>GS</sub> × f, here {Pg*1000:.0f} mW for 30 nC at 10 V, is dissipated mostly in the driver and gate resistor.
- **Expecting parallel devices to halve every loss.** Two MOSFETs sharing 10 A dissipate {Pc_each:.1f} W conduction each, half the total, but each still switches the full voltage at its share of current.
''',
     faq_add=[('Does paralleling two MOSFETs reduce conduction loss?',
               f'Yes. Each carries half the current, so with 20 mΩ devices sharing 10 A each dissipates {Pc_each:.1f} W and the pair {2*Pc_each:.1f} W, half of the single device {Pc:.1f} W. Gate drive loss doubles because there are two gates.'),
              ('What heat sink do I need to keep the junction at 100 °C?',
               f'Divide the temperature rise by the loss: ({Tj_target:.0f} − {Ta:.0f}) ÷ {P:.1f} W = {Rth_need:.2f} °C/W in total. After a 1.0 °C/W junction to case and 0.5 °C/W pad, the sink must be {Rsa:.2f} °C/W or better.')])

for cid in inplace.DONE:
    print(cid, inplace.body_words(cid))

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-23), slice 3: sallen-key-low-pass, buck-converter, rc-filter, op-amp-integrator, shunt-resistor.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-23'
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Sallen-Key low-pass
R1, R2, C1, C2, fq = 10e3, 10e3, 22e-9, 10e-9, 5000.0


def sk(R1, R2, C1, C2):
    f0 = 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))
    Q = math.sqrt(R1 * R2 * C1 * C2) / (C2 * (R1 + R2))
    return f0, Q


def skH(f, f0, Q):
    return 1 / math.sqrt((1 - (f / f0) ** 2) ** 2 + (f / (f0 * Q)) ** 2)


f0, Q = sk(R1, R2, C1, C2)
H5 = skH(fq, f0, Q)
assert abs(f0 - 1073.0) < 0.1 and abs(Q - 0.7416) < 1e-4 and abs(H5 - 0.0462) < 1e-4
# -3 dB frequency by bisection
lo, hi = f0 * 0.5, f0 * 3
for _ in range(100):
    m = (lo + hi) / 2
    if skH(m, f0, Q) > 1 / math.sqrt(2):
        lo = m
    else:
        hi = m
f3 = lo
# peaking for Q > 0.707
fpk = f0 * math.sqrt(1 - 1 / (2 * Q * Q))
Hpk = Q / math.sqrt(1 - 1 / (4 * Q * Q))
assert abs(skH(fpk, f0, Q) - Hpk) < 1e-9
# capacitors swapped
_, Qsw = sk(R1, R2, C2, C1)
# rescale to about 10 kHz with E24 resistors
Rn = 1.1e3
f0n, Qn = sk(Rn, Rn, C1, C2)
assert abs(Qn - Q) < 1e-12
# op-amp GBW rule
gbw = 100 * f0 * Q
# phase at f0 is -90 degrees
sk_rows = ''
for m in (0.5, 1, 2, 4, 10):
    hh = skH(m * f0, f0, Q)
    sk_rows += f"| {m:g} f₀ | {c(m*f0)} Hz | {hh:.4f} | {20*math.log10(hh):+.2f} dB |\n"

edit('electronics/sallen-key-low-pass', date=U, phrase='Sallen-Key low-pass filter calculator',
     intro=("The Sallen-Key topology builds a second-order active filter from one op-amp, two resistors and two capacitors, rolling off at 40 dB per decade. "
            "This Sallen-Key low-pass filter calculator gives the cutoff frequency, Q factor and gain at any frequency for the unity-gain version; see the "
            "[Sallen and Key active filter](https://www.instrumentationblog.in/active-filter-sallen-and-key/) explained.\n\n"
            "Analogue designers use it for anti-aliasing and sensor smoothing, choosing parts for a target response, and comparing it with a simple "
            "[RC low-pass filter](https://www.instrumentationblog.in/rc-low-pass-high-pass-filter/)."),
     body_add=f'''
## Where the default filter really cuts off

With the default parts Q is {Q:.4f}, a little above the Butterworth value of 0.7071, so f₀ is not quite the −3 dB point. Solving |H| = 0.7071 gives **{c(f3)} Hz**, about {(f3/f0-1)*100:.1f}% above f₀. The response also peaks slightly: the maximum gain is **{Hpk:.4f}** ({20*math.log10(Hpk):+.3f} dB) at {c(fpk)} Hz. That is far too small to hear or see on a scope, but it shows how Q shapes the knee.

| Frequency | Value | Gain | Gain (dB) |
|---|---|---|---|
{sk_rows}
Above about 2 f₀ each doubling of frequency costs close to 12 dB, the second-order slope.

## Scaling the design to a new frequency

To move the same response to about 10 kHz, keep both capacitors and divide both resistors by the same factor. Q depends only on the ratios, so it stays at {Qn:.4f}. The ideal value is 10 kΩ × {c(f0)} ÷ 10,000 = {c(10e3*f0/1e4)} Ω; the nearest E24 value, **1.1 kΩ**, gives f₀ = **{c(f0n)} Hz**. Scaling capacitors instead works the same way, but resistors come in finer steps.

## Checking a built filter

Drive the input from a signal generator at about 1 V and sweep the frequency while a two-channel scope or a Bode analyser compares input and output. The cleanest marker is phase: a second-order low-pass is exactly −90° at f₀ regardless of Q, so it confirms the natural frequency even when the −3 dB point has moved. Then read the gain at f₀, which equals Q, to check the capacitor ratio. Parts with 5% tolerance can move f₀ by several percent.

## Common mistakes

- **Swapping C₁ and C₂.** With 10 nF in the feedback position and 22 nF to ground, Q falls to {Qsw:.3f} and the knee becomes soft and early.
- **Ignoring the source resistance.** The driving impedance adds to R₁, lowering f₀ and changing Q, so drive the filter from a buffer or include it in R₁.
- **Choosing a slow op-amp.** The default needs a gain-bandwidth product of at least {c(gbw/1e3, 1)} kHz by the 100 × f₀ × Q rule; slower parts shift the response.
- **Using the unity-gain Q formula for a gain stage.** Adding gain resistors to the op-amp changes Q, so use the equal-component gain-set equations instead.
- **Expecting endless stop-band rejection.** Output impedance rising with frequency lets signal leak through C₁, so attenuation stops improving well above f₀.
''',
     faq_add=[('What phase shift does a Sallen-Key low-pass filter give at f₀?',
               f'Exactly −90° at the natural frequency, whatever the Q. At low frequencies the phase is near 0° and well above f₀ it approaches −180°. Measuring the −90° point is a reliable way to find f₀ on the bench; with the defaults it is {c(f0)} Hz.'),
              ('Why is the −3 dB frequency different from f₀?',
               f'Only a Butterworth filter (Q = 0.7071) has its −3 dB point at f₀. The defaults give Q = {Q:.4f}, so the gain stays a little higher and falls to −3 dB at {c(f3)} Hz.')])

# ---------------------------------------------------------------- Buck converter
Vi, Vo, Io, fs, r, dV = 24.0, 5.0, 2.0, 500e3, 0.30, 0.020
D = Vo / Vi
dI = r * Io
L = Vo * (Vi - Vo) / (Vi * fs * dI)
Ipk = Io + dI / 2
Cmin = dI / (8 * fs * dV)
assert abs(D - 0.20833) < 1e-5 and abs(L * 1e6 - 13.194) < 1e-3 and abs(Ipk - 2.3) < 1e-9 and abs(Cmin * 1e6 - 7.5) < 1e-9
Lsel = 15e-6
dI15 = Vo * (Vi - Vo) / (Vi * fs * Lsel)
Ipk15 = Io + dI15 / 2
esr_max = dV / dI
v_cer = dI * 0.005
v_el = dI * 0.050
Iin_rms = Io * math.sqrt(D * (1 - D))
ton = D / fs
Vd = 0.5
D_diode = (Vo + Vd) / (Vi + Vd)
I_ccm = dI / 2
ton_1v2m = (1.0 / 24) / 2e6
vin_rows = ''
for v in (8, 12, 18, 24, 36):
    Lv = Vo * (v - Vo) / (v * fs * dI)
    vin_rows += f"| {v} V | {Vo/v*100:.1f}% | {Lv*1e6:.1f} µH | {Vo/v/fs*1e9:.0f} ns |\n"
L36 = Vo * (36 - Vo) / (36 * fs * dI)

edit('electronics/buck-converter', date=U, phrase='buck converter calculator',
     intro=("A buck converter steps a DC voltage down by switching it on and off and smoothing the result with an inductor and capacitor, wasting far less power than a linear regulator. "
            "This buck converter calculator sizes the duty cycle, inductor and output capacitor; see the "
            "[buck converter working principle](https://www.instrumentationblog.in/buck-converter-working-principle/).\n\n"
            "Power supply designers and embedded engineers use it for a first-pass part selection, then check output ripple and "
            "[capacitor ESR](https://www.instrumentationblog.in/capacitor-esr-equivalent-series-resistance/) on the bench."),
     body_add=f'''
## After choosing real parts

The calculation asks for {L*1e6:.1f} µH, so a standard **15 µH** inductor is fitted. Larger inductance means less ripple: ΔI = 5 × 19 ÷ (24 × 500,000 × 15 µH) = **{dI15:.3f} A**, and the peak current falls to **{Ipk15:.3f} A**. The converter stays in continuous conduction down to a load of about ΔI ÷ 2, roughly {dI15/2:.2f} A with 15 µH ({I_ccm:.1f} A with the calculated value); below that it enters discontinuous mode and the simple duty cycle formula no longer holds.

The capacitance formula ignores ESR. To keep 20 mV with 0.6 A of ripple the ESR must be below 0.020 ÷ 0.6 = **{esr_max*1e3:.0f} mΩ**. A ceramic capacitor near 5 mΩ adds only {v_cer*1e3:.0f} mV, while an electrolytic of 50 mΩ adds {v_el*1e3:.0f} mV on its own, which is why ceramics dominate at 500 kHz. The input capacitor must carry about 2 × √({D:.3f} × {1-D:.3f}) = **{Iin_rms:.2f} A RMS**.

With a non-synchronous design and a 0.5 V Schottky diode, the duty cycle rises to (5 + 0.5) ÷ (24 + 0.5) = **{D_diode*100:.1f}%**. The on-time at 500 kHz is {ton*1e9:.0f} ns, comfortably above the minimum on-time of typical controllers.

## Designing across an input range

The inductance needed rises with input voltage, so design at the highest input. For 5 V out, 0.6 A ripple and 500 kHz:

| Input voltage | Duty cycle | Inductance | On-time |
|---|---|---|---|
{vin_rows}
A converter fed from 8 to 36 V needs about {L36*1e6:.1f} µH, not the {L*1e6:.1f} µH found at 24 V.

## Measuring ripple properly

Measure output ripple with the scope probe's ground spring touching the capacitor ground pad, not a long ground clip, and set 20 MHz bandwidth limiting. A long lead picks up switching spikes that look like ripple. Check the switch node for the expected duty cycle, and use a current probe on the inductor to confirm the ripple and that the waveform stays triangular with no sharp rise near the peak, which would mean saturation.

## Common mistakes

- **Designing at nominal input voltage.** At 36 V the same ripple needs {L36*1e6:.1f} µH; a part sized at 24 V gives more ripple and higher peak current at maximum input.
- **Ignoring DC bias on ceramic capacitors.** X5R and X7R parts can lose half or more of their capacitance at rated voltage, so check the derating curve at 5 V.
- **Rating the inductor at the load current.** The saturation rating must exceed the peak current and ideally the controller's current limit.
- **Asking for too short an on-time.** Converting 24 V to 1 V at 2 MHz needs only {ton_1v2m*1e9:.1f} ns, below the 50 to 100 ns minimum of many controllers.
- **Probing with a long ground lead,** which turns switching edges into false ripple readings.
''',
     faq_add=[('What ESR does the output capacitor need?',
               f'ESR ripple is about ESR × ΔI, so the ESR must stay below the allowed ripple divided by the ripple current. For 20 mV and 0.6 A that is {esr_max*1e3:.0f} mΩ, easy for ceramic capacitors but hard for small electrolytics.'),
              ('When does a buck converter go into discontinuous mode?',
               f'When the load current falls below half the inductor ripple, the inductor current reaches zero each cycle. With 15 µH in the default design that happens below about {dI15/2:.2f} A, and the output then depends on load as well as duty cycle.')])

# ---------------------------------------------------------------- RC filter
R, C, ft = 10e3, 100e-9, 1000.0
fc = 1 / (2 * math.pi * R * C)
tau = R * C
Glp = -10 * math.log10(1 + (ft / fc) ** 2)
Ghp = -10 * math.log10(1 + (fc / ft) ** 2)
assert abs(fc - 159.155) < 1e-3 and abs(tau - 1e-3) < 1e-15 and abs(Glp + 16.072) < 0.001 and abs(Ghp + 0.11) < 0.01
amp_lp = 10 ** (Glp / 20)
ph_lp = -math.degrees(math.atan(ft / fc))
wrong = 1 / (R * C)
RL = 10e3
Rth = R * RL / (R + RL)
fc_load = 1 / (2 * math.pi * Rth * C)
k_load = RL / (R + RL)
x2 = math.sqrt(math.sqrt(2) - 1)
f3_two = fc * x2
step_rows = ''
for n in (1, 2, 3, 4, 5):
    step_rows += f"| {n} τ | {n*tau*1e3:.0f} ms | {(1-math.exp(-n))*100:.1f}% |\n"
fc_hum = 5.0
R_hum = 1 / (2 * math.pi * fc_hum * 10e-6)
G50 = -10 * math.log10(1 + (50 / fc_hum) ** 2)

edit('electronics/rc-filter', date=U, phrase='RC filter cutoff frequency calculator',
     intro=("A resistor and capacitor make the simplest filter in electronics, removing noise from sensor signals or blocking DC from audio. "
            "This RC filter cutoff frequency calculator solves for whichever value you leave blank; read about "
            "[RC low-pass and high-pass filters](https://www.instrumentationblog.in/rc-low-pass-high-pass-filter/).\n\n"
            "Instrument technicians and circuit designers use it to smooth transmitter signals, set ADC anti-aliasing and decide when a sharper "
            "[Sallen-Key active filter](https://www.instrumentationblog.in/active-filter-sallen-and-key/) is needed."),
     body_add=f'''
## Worked example with the default values

R = 10 kΩ and C = 100 nF, with a 1 kHz test signal:

1. τ = RC = 10,000 × 100 × 10⁻⁹ = **{tau*1e3:.0f} ms**
2. f<sub>c</sub> = 1 ÷ (2π × 0.001) = **{fc:.2f} Hz**
3. f ÷ f<sub>c</sub> = {ft/fc:.3f}, so the low-pass gain is −10 log₁₀(1 + {(ft/fc)**2:.2f}) = **{Glp:.2f} dB**
4. The high-pass gain at the same frequency is **{Ghp:.2f} dB**

As a low-pass filter the circuit passes {amp_lp*100:.1f}% of a 1 kHz signal with a phase lag of {abs(ph_lp):.1f}°; as a high-pass filter it passes nearly all of it.

## Step response in the time domain

The same RC sets how fast the output follows a step, which matters for sensor signals and digital inputs:

| Time | Default value | Output reached |
|---|---|---|
{step_rows}
Five time constants, 5 ms here, is the usual rule for "settled".

## Filtering mains hum on a slow signal

A 4 to 20 mA loop signal read across 250 Ω often carries 50 Hz pickup. Putting the cutoff at {fc_hum:.0f} Hz with a 10 µF film or tantalum capacitor needs R = 1 ÷ (2π × {fc_hum:.0f} × 10 µF) = **{c(R_hum)} Ω**, and attenuates 50 Hz by {abs(G50):.1f} dB. The default 159 Hz filter would barely touch it, so the cutoff must sit well below the interference, not near it.

## Common mistakes

- **Dropping the 2π.** 1 ÷ RC gives {c(wrong)} rad/s, not hertz; the cutoff is {fc:.1f} Hz.
- **Ignoring the load.** A 10 kΩ load across the capacitor halves the passband level to {k_load:.2f} and moves the cutoff to {fc_load:.0f} Hz, because the source sees R in parallel with the load.
- **Expecting two stages to keep the same cutoff.** Two identical buffered sections are −6 dB at f<sub>c</sub> and −3 dB at {x2:.3f} f<sub>c</sub>, {f3_two:.0f} Hz for the defaults; without a buffer the second stage loads the first and the result is lower still.
- **Mixing nF and µF.** 100 nF is 0.1 µF; entering 100 µF makes the cutoff a thousand times lower.
- **Using a polarised electrolytic in a high-pass filter** where the DC across it can reverse.
''',
     faq_add=[('What is the phase shift of an RC low-pass filter?',
               f'The output lags by arctan(f ÷ f<sub>c</sub>): 45° at the cutoff, approaching 90° far above it. For the defaults at 1 kHz the lag is {abs(ph_lp):.1f}°. A high-pass filter leads by the complementary angle.')])

# ---------------------------------------------------------------- Op-amp integrator
Vin, Ri, Ci, t, V0, fi = 1.0, 10e3, 100e-9, 1e-3, 0.0, 1000.0
RC = Ri * Ci
k = -Vin / RC
Vout = V0 + k * t
f0i = 1 / (2 * math.pi * RC)
G = 1 / (2 * math.pi * fi * RC)
assert abs(k + 1000) < 1e-6 and abs(Vout + 1) < 1e-9 and abs(f0i - 159.155) < 1e-3 and abs(G - 0.15915) < 1e-5
Vsw = 13.0
t_sat = Vsw / abs(k)
Vos = 1e-3
drift_os = Vos / RC
Ib = 100e-9
drift_ib = Ib / Ci
t_sat_os = Vsw / drift_os
Rf = 1e6
gdc = Rf / Ri
vout_os = Vos * (1 + gdc)
f_low = 1 / (2 * math.pi * Rf * Ci)
T = 1e-3
vpp_sq = Vin * T / (2 * RC)
tab_rows = ''
for (rr, cc) in ((10e3, 10e-9), (10e3, 100e-9), (100e3, 100e-9), (100e3, 1e-6), (1e6, 1e-6)):
    kk = Vin / (rr * cc)
    tab_rows += f"| {rr/1e3:g} kΩ | {cc*1e9:g} nF | {c(kk, 1)} V/s | {10/kk*1e3:,.1f} ms |\n"

edit('electronics/op-amp-integrator', date=U, phrase='op-amp integrator calculator',
     intro=("An op-amp integrator charges a feedback capacitor with a current set by the input resistor, so a constant input produces a linear ramp. "
            "This op-amp integrator calculator gives the ramp rate, the output after a chosen time, the unity-gain frequency and the AC gain; see the "
            "[op-amp integrator and differentiator](https://www.instrumentationblog.in/op-amp-integrator-differentiator/) explained.\n\n"
            "Students, analogue designers and control engineers use it for ramp generators, analogue PID integral terms and dual-slope converters."),
     body_add=f'''
## How long until the output saturates

On ±15 V supplies a typical op-amp swings to about ±{Vsw:.0f} V. At the default ramp of {c(abs(k))} V/s the output reaches −{Vsw:.0f} V after {Vsw:.0f} ÷ 1,000 = **{t_sat*1e3:.0f} ms**, and then simply sits at the rail. Any integrator with a steady input must be reset, or placed inside a feedback loop that drives its input back to zero, as in a PID controller.

## Errors that integrate too

The circuit cannot tell signal from error. An input offset voltage of 1 mV integrates at 0.001 ÷ {RC*1e3:.0f} ms = **{drift_os:.0f} V/s**, reaching the rail in about {t_sat_os:.0f} s with no input at all. A bias current of 100 nA, typical of older bipolar op-amps, charges the 100 nF capacitor at I ÷ C = **{drift_ib:.0f} V/s**. A FET-input op-amp with picoamp bias removes the second error, and a resistor equal to R on the non-inverting input cancels much of it for bipolar parts.

Adding R<sub>f</sub> = 1 MΩ across the capacitor limits the DC gain to −{gdc:.0f}, so the 1 mV offset now produces only about {vout_os*1e3:.0f} mV at the output. The price is that the circuit integrates only above {f_low:.2f} Hz.

## Square wave in, triangle out

Feed a ±1 V, 1 kHz square wave. Each half period of 0.5 ms changes the output by 1 × 0.0005 ÷ 0.001 = **{vpp_sq:.1f} V peak to peak**, a triangle wave. Doubling the frequency halves the amplitude, the same 20 dB per decade slope as the sine response.

## Ramp rate for common parts (1 V input)

| R | C | Ramp rate | Time to 10 V |
|---|---|---|---|
{tab_rows}
## Common mistakes

- **Forgetting the inversion.** A positive input gives a falling output; follow with an inverting stage if a rising ramp is needed.
- **Leaving out a DC path.** Without R<sub>f</sub> or a reset switch, offset and bias current drift the output to a rail.
- **Using ceramic X7R or electrolytic capacitors.** Leakage and dielectric absorption bend the ramp and leave residual voltage after reset; polypropylene or C0G parts are better.
- **Mixing time units.** The time input is in milliseconds, so 1 means 0.001 s.
- **Ignoring the initial condition.** A capacitor not discharged at the start shifts the whole ramp by V₀.
''',
     faq_add=[('How fast does input offset voltage drift an integrator?',
               f'The offset is integrated like a signal, at V<sub>os</sub> ÷ RC volts per second. With 1 mV and RC = 1 ms that is {drift_os:.0f} V/s, so an uncorrected integrator reaches a 13 V rail in about {t_sat_os:.0f} s.')])

# ---------------------------------------------------------------- Shunt resistor
If, Vf, I = 50.0, 0.075, 30.0
Rs = Vf / If
Pf = Vf * If
V = I * Rs
P = I ** 2 * Rs
assert abs(Rs - 0.0015) < 1e-12 and abs(Pf - 3.75) < 1e-9 and abs(V - 0.045) < 1e-12 and abs(P - 1.35) < 1e-9
Icont = If * 2 / 3
Pcont = Icont ** 2 * Rs
gain = 20
Vamp = V * gain
Vamp_fs = Vf * gain
lsb = 3.3 / 4096
Ires = lsb / gain / Rs
Rc = 0.5e-3
err2w = (Rs + Rc) / Rs - 1
emf = 10e-6
I1 = 1.0
err_emf = emf / (I1 * Rs)
tc_mang, tc_cu, dT = 15e-6, 3900e-6, 50
read_meter = V / 0.050 * 50
sh_rows = ''
for pct in (10, 25, 50, 2 / 3 * 100, 100, 120):
    ii = If * pct / 100
    sh_rows += f"| {pct:.0f}% | {ii:.1f} A | {ii*Rs*1e3:.1f} mV | {ii**2*Rs:.2f} W |\n"

edit('electronics/shunt-resistor', date=U, phrase='shunt resistor calculator',
     intro=("A current shunt is a precise low-value resistor whose small voltage drop is proportional to the current through it. "
            "This shunt resistor calculator finds the resistance from the full-scale current and millivolt rating, plus the drop and power at any current; see "
            "[shunt resistors in instrumentation](https://www.instrumentationblog.in/shunt-resistors-in-instrumentation/).\n\n"
            "Electricians, battery system designers and panel builders use it to match shunts to meters, or choose an isolated "
            "[Hall-effect current sensor](https://www.instrumentationblog.in/hall-effect-current-sensor-acs712/) instead."),
     body_add=f'''
## Drop and heating across the range (50 A / 75 mV)

| Load | Current | Voltage drop | Power |
|---|---|---|---|
{sh_rows}
Most manufacturers recommend running at no more than about two-thirds of the rating continuously. For this shunt that is {Icont:.1f} A, where it dissipates {Pcont:.2f} W instead of the {Pf:.2f} W at full scale, keeping its temperature rise and drift low.

## Reading the shunt with an ADC

At the default 30 A the shunt gives {V*1e3:.0f} mV, too small to feed an ADC directly. A current-sense amplifier with a gain of {gain} raises it to **{Vamp:.2f} V**, and full scale becomes {Vamp_fs:.1f} V. A 12-bit ADC with a 3.3 V reference has steps of {lsb*1e3:.3f} mV, which corresponds to {lsb*1e3:.3f} mV ÷ {gain} ÷ 1.5 mΩ = **{Ires*1e3:.1f} mA** per count, so 30 A is resolved to better than 0.1%.

## Error sources in practice

- **Contact resistance.** Measuring across the main lugs with a bolted joint of 0.5 mΩ reads {err2w*100:.0f}% high; the sense screws avoid this.
- **Thermal EMF.** Copper to manganin junctions produce a few microvolts per degree. A 10 µV offset at 1 A, where the signal is only 1.5 mV, is a {err_emf*100:.2f}% error, so read low currents with care.
- **Temperature coefficient.** A 50 °C rise changes a manganin shunt by about {tc_mang*dT*100:.3f}%, whereas a length of copper used as a shunt would change by {tc_cu*dT*100:.1f}%.

For AC above a few kilohertz, the shunt's small self-inductance adds a reactive voltage, so use a coaxial or low-inductance shunt for fast current waveforms.

## Common mistakes

- **Mismatching meter and shunt ratings.** A panel meter scaled for 50 A / 50 mV on a 75 mV shunt reads {read_meter:.0f} A when 30 A flows, 50% high.
- **Connecting sense leads under the current bolts.** Take the voltage only from the dedicated sense terminals.
- **Running at 100% continuously.** Heat raises drift and can soften solder joints; derate to about two-thirds.
- **Placing a low-side shunt in a system with other ground paths.** Current bypassing the shunt through chassis or communication grounds is not measured.
- **Using an amplifier without enough common-mode range** on a high-side shunt in a 48 V or higher system.
''',
     faq_add=[('Can a 75 mV shunt be used with a 50 mV meter?',
               f'Only if the meter can be rescaled. A meter set for 50 A at 50 mV reads every 1 mV as 1 A, so on a 50 A / 75 mV shunt carrying 30 A it shows {read_meter:.0f} A. Set the meter input to 75 mV or use a matching shunt.'),
              ('How small a current can a 50 A shunt measure?',
               f'It depends on the amplifier and ADC. With a gain of {gain} and a 12-bit, 3.3 V ADC one count is about {Ires*1e3:.0f} mA, but offset and thermal EMF usually limit useful accuracy to a few hundred milliamps.')])

print('slice 3 done', inplace.DONE)

# ======================================================================= SECTION _expand_c4.py
"""Expand (2026-11-23), slice 4: free-space-path-loss, summing-amplifier, peukerts-law, rl-time-constant, current-divider.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-23'
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Free space path loss
C0 = 299792458.0


def fspl(d_km, f_mhz):
    return 20 * math.log10(4 * math.pi * d_km * 1e3 * f_mhz * 1e6 / C0)


def dist_for(L, f_mhz):
    return 10 ** ((L - fspl(1, f_mhz)) / 20)


d0, f0, Pt, Gt, Gr = 2.0, 868.0, 14.0, 2.0, 2.0
L0 = fspl(d0, f0)
Pr0 = Pt + Gt + Gr - L0
assert abs(L0 - 97.24) < 0.005 and abs(Pr0 + 79.24) < 0.005
S7, S12, fade = -123.0, -137.0, 20.0
m7 = Pr0 - S7
Lmax7 = Pt + Gt + Gr - S7 - fade
Lmax12 = Pt + Gt + Gr - S12 - fade
dmax7 = dist_for(Lmax7, f0)
dmax12 = dist_for(Lmax12, f0)
assert abs(fspl(dmax7, f0) - Lmax7) < 1e-9
pr_pw = 10 ** (Pr0 / 10) * 1e-3 * 1e12  # picowatts
eirp = Pt + Gt
erp = eirp - 2.15
h_ant = 10.0
horizon = 4.12 * 2 * math.sqrt(h_ant)
cable = 5 * 0.5
k1m = fspl(0.001, 1.0)  # constant for d in m, f in MHz
assert abs(fspl(1, 1.0) - 32.45) < 0.005 and abs(k1m - (fspl(1, 1.0) - 60)) < 1e-9
rows = ''
for dk in (0.5, 1, 2, 5, 10, 20):
    L = fspl(dk, f0)
    p = Pt + Gt + Gr - L
    rows += f"| {dk:g} km | {L:.1f} dB | {p:.1f} dBm | {p - S7:.1f} dB | {p - S12:.1f} dB |\n"

edit('electronics/free-space-path-loss', date=U, phrase='free space path loss calculator',
     intro=("Free-space path loss is how much a radio signal weakens as it spreads out over a clear line of sight. "
            "This free space path loss calculator gives the FSPL in dB and a simple link budget, the received power from transmit power and antenna gains.\n\n"
            "RF engineers and IoT installers use it to plan [LoRaWAN sensor networks](https://www.instrumentationblog.in/lorawan-industrial-iot-guide/), "
            "[wireless transmitters](https://www.instrumentationblog.in/wireless-pressure-transmitters-iiot-systems/), Wi-Fi and point-to-point links, "
            "checking that the received signal clears the receiver sensitivity with a safe margin."),
     body_add=f'''
## Link margin and maximum range from the defaults

The default link delivers **{Pr0:.2f} dBm**, which is only about {pr_pw:.1f} pW of real power at the receiver. A LoRa receiver at 125 kHz bandwidth decodes down to roughly {S7:.0f} dBm at SF7 and {S12:.0f} dBm at SF12, so:

- Margin at SF7 = {Pr0:.2f} − ({S7:.0f}) = **{m7:.2f} dB**
- Keeping a {fade:.0f} dB fade margin, the allowed path loss is 14 + 2 + 2 + {-S7:.0f} − {fade:.0f} = **{Lmax7:.0f} dB** at SF7, which free space reaches at **{dmax7:.1f} km**
- At SF12 the allowed loss is {Lmax12:.0f} dB, or {dmax12:.0f} km in free space

Those long distances are rarely achieved on the ground. With both antennas 10 m high, the radio horizon (4.12 × (√h₁ + √h₂) km) is only about **{horizon:.0f} km**, so terrain, Earth curvature and Fresnel zone blockage set the real limit long before free-space loss does.

| Distance | FSPL at 868 MHz | Received power | Margin to SF7 | Margin to SF12 |
|---|---|---|---|---|
{rows}
## Checking a link in the field

Most LoRa gateways and Wi-Fi access points report the RSSI of every packet. Compare it with the predicted received power: the difference is the excess loss from obstacles, cables and multipath. A survey with a portable node at the planned sensor locations, logging RSSI and SNR, is quicker than any model. A spectrum analyser with a calibrated antenna gives a more accurate absolute level when RSSI accuracy (often ±3 to 6 dB) is not enough.

The default transmitter radiates {eirp:.0f} dBm EIRP, or {erp:.2f} dBm ERP since a half-wave dipole has 2.15 dBi of gain. Regulatory limits are often written in ERP, such as the 25 mW (14 dBm) ERP limit in parts of the European 868 MHz band, so check which reference your local rule uses before adding antenna gain.

## Common mistakes

- **Using the wrong unit constant.** The 32.44 dB constant is for kilometres and megahertz; with metres and megahertz it becomes {k1m:.2f} dB, and mixing them puts the answer 60 dB out.
- **Treating dBd as dBi.** An antenna sold as 3 dBd is {3 + 2.15:.2f} dBi; entering dBd figures as dBi understates the gain, while the reverse overstates it.
- **Forgetting cable and connector loss.** Five metres of thin RG58 at 868 MHz loses about {cable:.1f} dB, which comes straight off the link budget at each end.
- **Assuming free space indoors.** Each concrete wall can add 10 to 20 dB, so a calculated indoor margin of 40 dB can vanish behind two or three walls.
- **Ignoring the Fresnel zone.** A clear visual line of sight is not enough; keep at least 60% of the first Fresnel zone free of trees, roofs and ground.
''',
     faq_add=[('Why does path loss increase with frequency if space is the same?',
               'The spreading of power over a sphere is the same at any frequency. The frequency term appears because FSPL assumes isotropic antennas, and the effective capture area of an isotropic receive antenna is λ² ÷ 4π, which shrinks as frequency rises.'),
              ('What is the maximum free-space range of the default LoRa link?',
               f'With 14 dBm, 2 dBi antennas, SF7 sensitivity of about {S7:.0f} dBm and a {fade:.0f} dB fade margin, the allowed loss is {Lmax7:.0f} dB, reached at about {dmax7:.1f} km in free space. On the ground the radio horizon and obstructions usually limit it to much less.')])

# ---------------------------------------------------------------- Summing amplifier
V1, R1, V2, R2, V3, R3, Rf = 1.0, 10.0, 0.5, 10.0, -0.2, 20.0, 10.0  # V, kohm
Iin = V1 / R1 + V2 / R2 + V3 / R3  # mA
Vout = -Rf * Iin
assert abs(Iin - 0.14) < 1e-12 and abs(Vout + 1.4) < 1e-12
parts = [(-Rf / R1, V1, R1), (-Rf / R2, V2, R2), (-Rf / R3, V3, R3)]
contrib = [g * v for g, v, _ in parts]
assert abs(sum(contrib) - Vout) < 1e-12
Rin_par = 1 / (1 / R1 + 1 / R2 + 1 / R3)
Rbias = 1 / (1 / R1 + 1 / R2 + 1 / R3 + 1 / Rf)
noise_gain = 1 + Rf / Rin_par
gbw = 1.0  # MHz
bw = gbw / noise_gain * 1e3  # kHz
# averaging version: three equal 30 kohm inputs, Rf = 30/3
Ra = 30.0
Rf_avg = Ra / 3
Vavg = -Rf_avg * (V1 / Ra + V2 / Ra + V3 / Ra)
assert abs(Vavg + (V1 + V2 + V3) / 3) < 1e-12
# offset: 1 mV input offset multiplied by noise gain
vos_out = 1.0 * noise_gain
# source currents
I_src = [v / r for _, v, r in parts]
crow = ''
names = ['V₁', 'V₂', 'V₃']
for n, (g, v, r), ct, i in zip(names, parts, contrib, I_src):
    crow += f"| {n} | {v:+g} V | {r:g} kΩ | {g:.2f} | {ct:+.2f} V | {i*1000:+.0f} µA |\n"

edit('electronics/summing-amplifier', date=U, phrase='summing amplifier calculator',
     intro=("An inverting summing amplifier adds several input voltages, each weighted by the ratio of the feedback resistor to its own input resistor, because the inverting input sits at a virtual ground. "
            "This summing amplifier calculator gives the output voltage and input current for three inputs.\n\n"
            "Circuit designers and students use it for mixers, offset and scaling stages and simple DACs, building on the "
            "[inverting amplifier gain formula](https://www.instrumentationblog.in/inverting-amplifier-gain-formula/) covered in "
            "[op-amp basics](https://www.instrumentationblog.in/operational-amplifier-op-amp-basics/)."),
     body_add=f'''
## What each default input contributes

Superposition makes the summing amplifier easy to check one input at a time:

| Input | Voltage | Resistor | Gain −R<sub>f</sub>/R<sub>n</sub> | Contribution | Source current |
|---|---|---|---|---|---|
{crow}
The three contributions add to **{Vout:.2f} V**. Note that V₃ is negative and passes through twice the resistance, so it pushes the output up by only {contrib[2]:.2f} V. Each source sees a load equal to its own input resistor, so V₁ must supply {I_src[0]*1000:.0f} µA into 10 kΩ regardless of the other inputs.

## Bias resistor, noise gain and bandwidth

For the defaults, the resistor from the non-inverting input to ground should be R₁ ∥ R₂ ∥ R₃ ∥ R<sub>f</sub> = **{Rbias:.3f} kΩ**; 2.87 kΩ or 2.8 kΩ is a practical value. The signal gain of each input is at most 1, but the op-amp sees a **noise gain** of 1 + R<sub>f</sub> ÷ (R₁ ∥ R₂ ∥ R₃) = 1 + 10 ÷ {Rin_par:.0f} = **{noise_gain:.1f}**. That number, not the signal gain, sets the closed-loop bandwidth and the output offset: a 1 MHz gain-bandwidth op-amp gives about {bw:.0f} kHz, and a 1 mV input offset appears as {vos_out:.1f} mV at the output. Every extra input lowers the bandwidth further.

## A second scenario: averaging the same inputs

To output the average instead of the sum, use equal input resistors of 30 kΩ and R<sub>f</sub> = 30 ÷ 3 = {Rf_avg:.0f} kΩ. The same three voltages then give −(1 + 0.5 − 0.2) ÷ 3 = **{Vavg:.4f} V**. This is how a sensor averager combines three thermocouple amplifier outputs into one reading.

## Testing a built circuit

With the circuit powered and inputs connected, a multimeter between the inverting input and ground should read within a few millivolts of zero; if it does not, the op-amp is saturated or the feedback path is open. Then remove one input at a time (ground it) and confirm the output changes by that input's contribution from the table.

## Common mistakes

- **Forgetting the inversion when chaining stages.** A positive sum needs a second inverting stage with unity gain, which adds its own offset and noise to the result.
- **Designing bandwidth from the signal gain.** With three inputs and equal resistors the noise gain is 4 even though each input has a gain of 1.
- **Driving an input from a high impedance source.** A 10 kΩ sensor output in series with a 10 kΩ input resistor halves that input's weight.
- **Leaving an unused input floating.** Tie it to ground or remove its resistor; a resistor with a floating far end acts as an antenna and couples hum into the summing node.
- **Exceeding the output swing on peaks.** Audio mixers must be checked at the sum of all input peaks, not the average level.
''',
     faq_add=[('What is the input impedance of a summing amplifier?',
               f'Each input sees only its own input resistor, because the inverting node is held at virtual ground. With the defaults, V₁ and V₂ each see 10 kΩ and V₃ sees 20 kΩ.'),
              ('Why does adding inputs reduce the bandwidth?',
               f'Each input resistor lowers the resistance from the inverting node to ground and raises the noise gain, 1 + R_f ÷ (R₁ ∥ R₂ ∥ R₃). For the defaults it is {noise_gain:.1f}, so a 1 MHz op-amp gives about {bw:.0f} kHz of bandwidth.')])

# ---------------------------------------------------------------- Peukert's law
Cp, Hh, Ip, kp = 100.0, 20.0, 10.0, 1.2


def peuk(C, H, I, k):
    return H * (C / (I * H)) ** k


Irated = Cp / Hh
tP = peuk(Cp, Hh, Ip, kp)
t0 = Cp / Ip
Ce = Ip * tP
assert abs(Irated - 5) < 1e-12 and abs(tP - 8.7055) < 1e-4 and abs(Ce - 87.055) < 1e-3 and t0 == 10
t_half = 0.5 * tP
# current for a 5 h runtime
t_target = 5.0
I_for = Cp / (Hh * (t_target / Hh) ** (1 / kp))
assert abs(peuk(Cp, Hh, I_for, kp) - t_target) < 1e-9
# parallel batteries
prow = ''
for n in (1, 2, 3, 4):
    tp = peuk(n * Cp, Hh, Ip, kp)
    cap = min(tp, n * Cp / Ip)
    prow += f"| {n} | {n*Cp:.0f} Ah | {Ip/n:.2f} A | {tp:.2f} h | {cap:.2f} h |\n"
t2 = peuk(2 * Cp, Hh, Ip, kp)
assert abs(t2 - 20) < 1e-9
# C10 rated battery at 10 A
tC10 = peuk(Cp, 10, Ip, kp)
# LiFePO4 k = 1.03
tLi = peuk(Cp, Hh, Ip, 1.03)
# inverter load
P_inv, V_bat, eff = 1000.0, 12.0, 0.9
I_inv = P_inv / (V_bat * eff)
I_inv_low = P_inv / (11.0 * eff)

edit('electronics/peukerts-law', date=U, phrase="peukert's law calculator",
     intro=("A battery's amp-hour rating is measured at one discharge time, usually 20 hours for lead-acid, and it delivers less when discharged faster. "
            "This Peukert's law calculator corrects the simple Ah ÷ A estimate for the discharge rate, giving the realistic runtime and effective capacity.\n\n"
            "Solar installers, UPS designers and RV owners use it to size battery banks; for full [battery backup time](https://www.instrumentationblog.in/calculate-battery-backup-time/) "
            "planning, also allow for depth of discharge and inverter losses."),
     body_add=f'''
## Three practical questions for the default battery

The default 100 Ah C20 battery with k = 1.2 runs a 10 A load for {tP:.2f} h to full discharge. Building on that:

1. **To 50% depth of discharge**, the usual limit for long lead-acid life, the runtime is about 0.5 × {tP:.2f} = **{t_half:.2f} h**, not the 5 h a simple Ah ÷ A estimate suggests.
2. **For a required 5 h runtime**, invert the law: I = C ÷ (H × (t ÷ H)<sup>1/k</sup>) = 100 ÷ (20 × 0.25<sup>0.833</sup>) = **{I_for:.2f} A** is the largest constant load the battery can carry.
3. **With a second battery in parallel**, each battery supplies 5 A, its rated current, so the bank runs for **{t2:.0f} h**, which is {t2/tP:.2f} times the single battery runtime rather than twice it.

## Runtime at 10 A as batteries are added in parallel

| Batteries | Bank capacity | Current per battery | Peukert runtime | Capped at rated Ah |
|---|---|---|---|---|
{prow}
Above two batteries each one discharges below its rated current, where Peukert's law predicts more than the rated capacity. Use the capped column for design, as the existing notes advise.

## Measuring capacity and the exponent

A capacity test discharges a fully charged battery at constant current at 25 °C until the terminal voltage reaches the end voltage, usually 1.75 V per cell (10.5 V for a 12 V block). The rated current for the default battery is {Irated:.0f} A, so a healthy unit should last close to 20 h. Repeat the test at a higher current, such as 20 A, and the two runtimes give the exponent with the formula above. Batteries below 80% of rated capacity are normally due for replacement, and their exponent tends to rise with age.

## Common mistakes

- **Entering the wrong rating hours.** If the same 100 Ah figure were a C10 rating, the 10 A load would be the rated current and the runtime would be {tC10:.0f} h, not {tP:.2f} h.
- **Converting watts to amps at nominal voltage.** A 1,000 W inverter load at 90% efficiency draws {I_inv:.1f} A at 12 V but {I_inv_low:.1f} A as the battery sags to 11 V, so use the lower voltage.
- **Using a lead-acid exponent for lithium.** A LiFePO4 battery with k ≈ 1.03 would run the default load for about {tLi:.2f} h; entering 1.2 understates it by more than an hour.
- **Ignoring temperature.** The exponent and capacity are quoted at 25 °C; a cold battery loses capacity at every current.
- **Applying it to short pulses.** Engine cranking and inrush loads recover between pulses, so the constant current law overstates their effect.
''',
     faq_add=[('Does connecting two batteries in parallel more than double the runtime?',
               f'With lead-acid, yes. At 10 A a single 100 Ah C20 battery with k = 1.2 lasts {tP:.2f} h, while two in parallel each supply 5 A and last {t2:.0f} h, {t2/tP:.2f} times longer, because each battery is discharged at a gentler rate.')])

# ---------------------------------------------------------------- RL time constant
Lh, Rr, Vv, tt = 0.1, 50.0, 24.0, 2e-3
tau = Lh / Rr
If = Vv / Rr
Ir = If * (1 - math.exp(-tt / tau))
Id = If * math.exp(-tt / tau)
assert abs(tau - 2e-3) < 1e-15 and abs(If - 0.48) < 1e-12 and abs(Ir - 0.30341) < 1e-5 and abs(Id - 0.17658) < 1e-5
E = 0.5 * Lh * If ** 2
didt0 = Vv / Lh
# faster release: 200 ohm in series with flyback diode
Rs = 200.0
tau_off = Lh / (Rr + Rs)
Vpk = Vv + If * Rs
t_rel_diode = tau * math.log(If / 0.1)  # time to fall to 0.1 A
t_rel_res = tau_off * math.log(If / 0.1)
# forced drive: 3x voltage, extra 100 ohm
Rx = 100.0
tau_f = Lh / (Rr + Rx)
V_f = If * (Rr + Rx)
t90 = tau * math.log(10)
t90_f = tau_f * math.log(10)
P_x = If ** 2 * Rx
rrow = ''
for tm in (0.5, 1, 2, 4, 6, 10):
    ts = tm * 1e-3
    i = If * (1 - math.exp(-ts / tau))
    vl = Vv * math.exp(-ts / tau)
    rrow += f"| {tm:g} ms | {i:.4f} A | {vl:.2f} V | {i*Rr:.2f} V |\n"

edit('electronics/rl-time-constant', date=U, phrase='rl time constant calculator',
     intro=("When voltage is applied to an inductor through a resistance, current rises exponentially with a time constant τ = L/R, and decays the same way when switched off. "
            "This RL time constant calculator gives τ and the current at any moment.\n\n"
            "Control panel designers, automation technicians and students use it to predict relay and solenoid timing, choose coil suppression and size drive circuits; see "
            "[RC and RL time constants explained](https://www.instrumentationblog.in/rc-and-rl-time-constant-explained/)."),
     body_add=f'''
## Current and voltages over time for the default coil

For the default 100 mH, 50 Ω coil on 24 V, the current starts rising at V ÷ L = **{didt0:.0f} A/s** and the inductor voltage falls as the resistor voltage grows:

| Time | Current | Voltage across L | Voltage across R |
|---|---|---|---|
{rrow}
At every instant the two voltages add to 24 V. At full current the coil stores ½LI² = ½ × 0.1 × 0.48² = **{E*1000:.2f} mJ**, the energy any suppression circuit must absorb at switch-off.

## Scenario 1: making the coil release faster

With a plain flyback diode the current decays through the coil's own 50 Ω with τ = 2 ms, taking about {t_rel_diode*1000:.2f} ms to fall to 0.1 A. Adding a 200 Ω resistor in series with the diode raises the loop resistance to 250 Ω, so τ<sub>off</sub> = 0.1 ÷ 250 = **{tau_off*1000:.1f} ms** and the same drop takes only {t_rel_res*1000:.2f} ms. The cost is a switch voltage of 24 + 0.48 × 200 = **{Vpk:.0f} V** at turn-off (plus the diode drop), so the transistor must be rated well above that.

## Scenario 2: forcing a faster rise

Stepper and solenoid drivers speed up the rise by adding series resistance and raising the voltage in proportion. Tripling the supply to {V_f:.0f} V with an extra 100 Ω keeps the final current at 0.48 A but cuts τ to {tau_f*1000:.3f} ms, so 90% current arrives in {t90_f*1000:.2f} ms instead of {t90*1000:.2f} ms. The extra resistor wastes {P_x:.1f} W continuously, which is why modern drivers use chopper current control instead.

## Measuring τ and L

Put a small sense resistor in series, switch the supply on and watch the current on an oscilloscope: τ is the time to 63.2% of the final value. Then L = τ × R. An LCR meter at 1 kHz gives a quick inductance figure, but for iron-cored coils it can differ from the value at operating current.

## Common mistakes

- **Mixing units.** Millihenries divided by ohms give milliseconds directly; using henries with milliseconds gives an answer 1,000 times off.
- **Using the RC formula.** τ = L × R is wrong for inductors; doubling R halves the RL time constant.
- **Assuming a decay path exists.** If the switch simply opens with no diode or snubber, the current cannot follow the exponential curve and the stored energy appears as an arc or a destroyed transistor.
- **Expecting relay pull-in at the final current.** The armature closes at its pull-in current, often well below V/R, and the inductance rises once it closes.
- **Ignoring supply resistance.** A weak supply or long thin cable adds resistance and lowers both τ and the final current.
''',
     faq_add=[('How do I find the inductance of a coil from its time constant?',
               f'Measure the time for the current to reach 63.2% of its final value, then multiply by the total loop resistance: L = τ × R. A 2 ms time constant in a 50 Ω loop means 100 mH.'),
              ('How much energy does the default coil store?',
               f'½ × L × I² = ½ × 0.1 H × (0.48 A)² = {E*1000:.2f} mJ at full current. A flyback diode, Zener or snubber must absorb this energy every time the coil is switched off.')])

# ---------------------------------------------------------------- Current divider
It, Ra1, Ra2 = 1.0, 100.0, 300.0
I1 = It * Ra2 / (Ra1 + Ra2)
I2 = It * Ra1 / (Ra1 + Ra2)
Req = Ra1 * Ra2 / (Ra1 + Ra2)
Vp = It * Req
assert abs(I1 - 0.75) < 1e-12 and abs(I2 - 0.25) < 1e-12 and abs(Req - 75) < 1e-12 and abs(Vp - 75) < 1e-12
P1 = I1 ** 2 * Ra1
P2 = I2 ** 2 * Ra2
assert abs(P1 + P2 - It ** 2 * Req) < 1e-9
# ammeter burden of 1 ohm in branch 1
Rb = 1.0
I1m = It * Ra2 / (Ra1 + Rb + Ra2)
# tolerance table
trow = ''
for tol1, tol2 in ((0, 0), (5, 0), (-5, 0), (0, 5), (5, -5), (-5, 5)):
    r1 = Ra1 * (1 + tol1 / 100)
    r2 = Ra2 * (1 + tol2 / 100)
    i1 = It * r2 / (r1 + r2)
    trow += f"| {tol1:+d}% | {tol2:+d}% | {i1:.4f} A | {It - i1:.4f} A | {(i1 / I1 - 1) * 100:+.2f}% |\n"
i1_worst = It * Ra2 * 0.95 / (Ra1 * 1.05 + Ra2 * 0.95)
wrong = It * Ra1 / (Ra1 + Ra2)

edit('electronics/current-divider', date=U, phrase='current divider calculator',
     intro=("When current reaches parallel branches it splits between them, with more through the lower resistance. "
            "The [current divider rule](https://www.instrumentationblog.in/current-divider-rule-explained/) follows from "
            "[Kirchhoff's current law](https://www.instrumentationblog.in/kirchhoffs-current-law-kcl-explained/), and this current divider calculator gives each branch current, the equivalent resistance and the voltage.\n\n"
            "Electronics students and instrument technicians use it to analyse parallel loads, check how a meter shunt shares current with the movement and design "
            "[shunt resistors in instrumentation](https://www.instrumentationblog.in/shunt-resistors-in-instrumentation/)."),
     body_add=f'''
## Power in each branch at the default values

The default split also tells you how hot each resistor gets:

- P₁ = 0.75² × 100 = **{P1:.2f} W** and P₂ = 0.25² × 300 = **{P2:.2f} W**
- Total = {P1 + P2:.0f} W, which equals I<sub>T</sub>² × R<sub>eq</sub> = 1² × 75 and V × I<sub>T</sub> = 75 × 1

The smaller resistor carries three times the current and dissipates three times the power, because both resistors share the same 75 V and P = V² ÷ R. Neither value could be an ordinary 0.25 W part; these are power resistors on a heatsink or in free air with derating.

## How resistor tolerance shifts the split

With 1 A into the default pair:

| R₁ change | R₂ change | I₁ | I₂ | Change in I₁ |
|---|---|---|---|---|
{trow}
A 5% error in one resistor moves the split by only about 1.2 to 1.3%, because the error partly cancels in the ratio R₂ ÷ (R₁ + R₂). The worst case, R₁ high and R₂ low, gives {i1_worst:.4f} A. Where an exact split matters, use 0.1% resistors or trim one branch.

## Measuring branch currents

A series ammeter adds its burden resistance to the branch it measures. A meter with 1 Ω burden in the R₁ branch reads {I1m:.4f} A instead of 0.75 A, a small error here but a large one when the branch is a shunt of a few ohms or less. A clamp meter or a voltage reading across a known resistor avoids the problem: 75 V across the 100 Ω branch confirms 0.75 A without breaking the circuit.

## Common mistakes

- **Putting the branch's own resistance in the numerator.** I₁ = I<sub>T</sub> × R₁ ÷ (R₁ + R₂) gives {wrong:.2f} A, the current of the other branch.
- **Using the two-branch formula for three branches.** With three or more paths, work with conductances or combine two branches first.
- **Forgetting the power rating.** Branch currents can look harmless while the resistors dissipate tens of watts.
- **Ignoring temperature coefficient.** Copper wiring rises about 0.39% per °C, so a copper path in parallel with a manganin shunt drifts as it warms.
''',
     faq_add=[('How much power does each branch dissipate?',
               f'Use P = I² × R for each branch. With 1 A into 100 Ω and 300 Ω, the 100 Ω resistor dissipates {P1:.2f} W and the 300 Ω resistor {P2:.2f} W, a total of {P1+P2:.0f} W.'),
              ('Does an ammeter in one branch change the current split?',
               f'Slightly, because its burden resistance adds to that branch. A 1 Ω meter in the 100 Ω branch lowers its current from 0.75 A to about {I1m:.4f} A, so use a low burden meter or a clamp on low resistance branches.')])

for cid in inplace.DONE:
    print(cid, inplace.body_words(cid))

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-23), slice 5: hall-effect-current-sensor, capacitor-energy, buck-boost-converter, resonant-frequency, pwm-duty-cycle.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-23'
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Hall-effect current sensor
Vq, S, I, Vref, N = 2.5, 185.0, 2.0, 5.0, 10


def hall(Vq, S, I, Vref, N):
    Vout = Vq + S / 1000 * I
    cnt = Vout / Vref * 2 ** N
    res = Vref / (2 ** N * S / 1000)
    return Vout, cnt, res


Vout0, cnt0, res0 = hall(Vq, S, I, Vref, N)
assert abs(Vout0 - 2.87) < 1e-9 and abs(cnt0 - 587.776) < 1e-3 and abs(res0 - 0.026394) < 1e-6
# negative current
In = -3.0
Vneg, cneg, _ = hall(Vq, S, In, Vref, N)
assert abs(Vneg - 1.945) < 1e-9
# AC: 2 A RMS sine
Ipk_ac = 2 * math.sqrt(2)
Vlo, Vhi = Vq - S / 1000 * Ipk_ac, Vq + S / 1000 * Ipk_ac
# supply sag to 4.8 V (ratiometric)
Vs = 4.8
Vq_s, S_s = Vq * Vs / 5, S * Vs / 5
Vout_s = Vq_s + S_s / 1000 * I
I_wrong = (Vout_s - Vq) / (S / 1000)          # firmware assumes 2.5 V and 185 mV/A in volts
cnt_s = Vout_s / Vs * 2 ** N                  # ADC referenced to the same 4.8 V rail
assert abs(cnt_s - cnt0) < 1e-9
I_from_counts = (cnt_s / 2 ** N * Vref - Vq) / (S / 1000)
assert abs(I_from_counts - I) < 1e-9
# 3.3 V ADC on a 5 V sensor
Imax33 = (3.3 - Vq) / (S / 1000)
# averaging
navg = 16
res_avg = res0 / math.sqrt(navg)
hall_rows = ''
for s in (400, 185, 100, 66, 40):
    vo, cn, rs = hall(Vq, s, I, Vref, N)
    _, _, rs12 = hall(Vq, s, I, Vref, 12)
    hall_rows += f"| {s} mV/A | {vo:.3f} V | {cn:.1f} | {rs*1000:.1f} mA | {rs12*1000:.2f} mA |\n"

edit('electronics/hall-effect-current-sensor', date=U, phrase='hall-effect current sensor calculator',
     intro=("A Hall-effect current sensor gives an output voltage proportional to the current through it, centred on a zero-current offset that is usually half the supply. "
            "This Hall-effect current sensor calculator converts current to output voltage and back, and gives the ADC reading and current per count; see how the "
            "[ACS712 Hall-effect current sensor](https://www.instrumentationblog.in/hall-effect-current-sensor-acs712/) works.\n\n"
            "Makers, embedded developers and test engineers use it to scale firmware, pick a sensor range and judge how finely a microcontroller can resolve current."),
     body_add=f'''
## Second example: reverse and AC current

With the default 2.5 V offset, 185 mV/A, 5 V reference and 10 bits, a current of **−3 A** gives V<sub>out</sub> = 2.5 − 0.185 × 3 = **{Vneg:.3f} V**, which the ADC reads as {Vneg:.3f} ÷ 5 × 1,024 = **{cneg:.1f} counts**. The sensor is bidirectional, so anything below 512 counts is current flowing the other way.

For an AC load of 2 A RMS, the peak current is 2 × √2 = {Ipk_ac:.3f} A, so the output swings between **{Vlo:.3f} V** and **{Vhi:.3f} V** around the offset. Subtract the offset from every sample before squaring; computing RMS on the raw voltage gives a figure dominated by the 2.5 V DC level.

## Why ratiometric output matters

The ACS712 offset and sensitivity both scale with its supply. If a USB rail sags to {Vs} V, the offset becomes {Vq_s:.2f} V and the sensitivity {S_s:.1f} mV/A, so 2 A gives {Vout_s:.4f} V. Firmware that converts with a fixed 2.5 V and 185 mV/A would report **{I_wrong:.2f} A**. When the ADC reference is the same {Vs} V rail, the reading stays at **{cnt_s:.1f} counts** and converts back to exactly 2.00 A, because both sides scaled together. Reference the ADC to the sensor supply, or measure that supply and correct for it.

## Sensitivity versus resolution at 2 A

Same 2.5 V offset and 5 V reference:

| Sensitivity | V<sub>out</sub> at 2 A | 10-bit counts | Per count, 10-bit | Per count, 12-bit |
|---|---|---|---|---|
{hall_rows}
A higher sensitivity gives finer resolution but a smaller range before the output reaches the supply rail. Averaging {navg} samples cuts random noise by √{navg} = 4, so the effective step on the 185 mV/A part improves from {res0*1000:.1f} mA towards {res_avg*1000:.1f} mA if the noise is enough to dither the readings.

## Common mistakes

- **Feeding a 5 V sensor into a 3.3 V ADC.** The input saturates at 3.3 V, which is only {Imax33:.2f} A on the 185 mV/A part, and higher outputs can exceed the pin's absolute maximum. Use a resistor divider and rescale.
- **Assuming the ADC reference is exactly 5 V.** USB supplies range roughly 4.75 to 5.25 V; a fixed constant in firmware turns that into a gain error.
- **Hard coding the offset as 512 counts.** Each part has its own zero error; read it at start-up with no current flowing.
- **Choosing the wrong variant.** The 5 A, 20 A and 30 A parts look identical; check the marking before trusting 185 mV/A.
- **Leaving the filter pin open.** The bandwidth is then at its maximum and so is the noise; add the datasheet filter capacitor if you do not need fast transients.
''',
     faq_add=[('Can I use a 5 V Hall-effect current sensor with a 3.3 V microcontroller?',
               f'Only with care. The output centres on 2.5 V and reaches 3.3 V at about {Imax33:.2f} A on a 185 mV/A part, so the upper range is lost and the pin can be overdriven. Scale the output with a resistor divider and include the divider ratio in the conversion.'),
              ('Does the sensor supply voltage change the current reading?',
               f'Yes for ratiometric sensors. At a {Vs} V supply the offset is {Vq_s:.2f} V and the sensitivity {S_s:.1f} mV/A, so fixed constants read 2 A as {I_wrong:.2f} A. Using the same rail as the ADC reference cancels the error.')])

# ---------------------------------------------------------------- Capacitor energy
C, V, V2 = 1000e-6, 50.0, 25.0
E = 0.5 * C * V ** 2
Q = C * V
Eu = 0.5 * C * (V ** 2 - V2 ** 2)
fu = Eu / E
assert abs(E - 1.25) < 1e-12 and abs(Q - 0.05) < 1e-12 and abs(Eu - 0.9375) < 1e-12 and abs(fu - 0.75) < 1e-12
P_load, eta_c = 5.0, 0.85
t_hold = Eu / P_load
t_hold_eta = Eu * eta_c / P_load
# tolerance
Eu_tol = 0.5 * 0.8 * C * (V ** 2 - V2 ** 2)
# charging loss from a fixed source
W_src = Q * V
W_lost = W_src - E
assert abs(W_lost - E) < 1e-12
# bleed resistor 1 kohm
Rb = 1000.0
tau = Rb * C
I_pk_b = V / Rb
P_pk_b = V ** 2 / Rb
t_to5 = tau * math.log(V / 5.0)
# supercap measurement by constant current
Icc, dt, dVm = 1.0, 20.0, 1.9
C_meas = Icc * dt / dVm
# units slip
E_wrong = 0.5 * 1000 * V ** 2
hold_rows = ''
for p in (1, 2, 5, 10, 20):
    hold_rows += f"| {p} W | {Eu/p*1000:,.1f} ms | {Eu*eta_c/p*1000:,.1f} ms |\n"

edit('electronics/capacitor-energy', date=U, phrase='capacitor energy calculator',
     intro=("A capacitor stores energy in the electric field between its plates, and the amount rises with the square of the voltage; see the "
            "[capacitor working principle](https://www.instrumentationblog.in/capacitor-working-principle/) and how "
            "[supercapacitors](https://www.instrumentationblog.in/supercapacitor-working-principle/) store far more. "
            "This capacitor energy calculator gives stored energy, charge and usable energy.\n\n"
            "Power electronics designers use it to size hold-up and backup capacitors, and technicians use it to judge how dangerous a charged capacitor is before working on it."),
     body_add=f'''
## Hold-up time from the default capacitor

The default 1,000 µF at 50 V, discharging to 25 V, delivers {Eu:.4f} J. Feeding a converter that draws a steady {P_load:.0f} W from it, the supply rides through for {Eu:.4f} ÷ {P_load:.0f} = **{t_hold*1000:.1f} ms**. If the {P_load:.0f} W is the converter output and it runs at {eta_c*100:.0f}% efficiency, only {Eu*eta_c:.3f} J reaches the load, giving **{t_hold_eta*1000:.1f} ms**. With an electrolytic at its −20% tolerance limit the usable energy falls to {Eu_tol:.2f} J, so design hold-up on the minimum capacitance.

| Load power | Hold-up (ideal) | Hold-up at {eta_c*100:.0f}% efficiency |
|---|---|---|
{hold_rows}
## Charging always costs twice the stored energy

Charging the capacitor to 50 V from a fixed voltage source draws Q × V = 0.05 × 50 = **{W_src:.2f} J** from the source. Only {E:.2f} J ends up stored; the other **{W_lost:.2f} J** is dissipated in the series resistance, whatever its value. A smaller resistor only makes the loss happen faster with a higher current peak. Inductor-based chargers avoid this by limiting the current instead of the voltage.

## Discharging safely

A 1 kΩ bleed resistor across the default capacitor gives a time constant of {tau:.1f} s. The first instant passes {I_pk_b*1000:.0f} mA and dissipates {P_pk_b:.1f} W, and the voltage reaches 5 V after τ × ln(50 ÷ 5) = **{t_to5:.2f} s**. The resistor absorbs the full {E:.2f} J, so a 3 W wirewound part handles it comfortably; a 0.25 W film resistor could fail open on larger banks.

## Measuring capacitance from a discharge

Supercapacitor capacitance is measured by constant-current discharge, as in IEC 62391-1: C = I × Δt ÷ ΔV, taken over the linear part of the curve after the initial ESR step. A cell discharged at {Icc:.0f} A that falls {dVm} V in {dt:.0f} s has C = {Icc:.0f} × {dt:.0f} ÷ {dVm} = **{C_meas:.1f} F**. The sudden drop when the current starts, divided by the current, gives the ESR.

## Common mistakes

- **Entering microfarads as farads.** Using 1,000 F instead of 1,000 µF gives {c(E_wrong)} J, a million times too much.
- **Using E = QV.** That is the energy drawn from the source; the energy stored is half of it, ½QV.
- **Counting all the stored energy as usable.** Below the regulator's minimum input the remaining {(1-fu)*100:.0f}% stays in the capacitor.
- **Ignoring ESR at high discharge current.** The I × ESR drop raises the effective cut-off voltage and reduces usable energy.
- **Exceeding the voltage rating in series banks.** Without balancing, leakage differences can put one cell above its rating.
''',
     faq_add=[('Why is half the energy lost when charging a capacitor from a battery?',
               f'The source delivers charge Q at constant voltage V, so it supplies QV, but the capacitor stores only ½QV. For 1,000 µF charged to 50 V the source gives {W_src:.2f} J, {E:.2f} J is stored and {W_lost:.2f} J is lost as heat in the series resistance, regardless of its value.'),
              ('How do I measure the capacitance of a supercapacitor?',
               f'Discharge it at a constant current and time the voltage fall: C = I × Δt ÷ ΔV. A {Icc:.0f} A discharge falling {dVm} V in {dt:.0f} s means about {C_meas:.1f} F. Ignore the instant ESR drop at the start.')])

# ---------------------------------------------------------------- Buck-boost converter
Vi, Vo, Io, eta, f, r, dV = 12.0, 12.0, 0.5, 0.85, 500e3, 0.30, 0.050


def bb(Vi, Vo=Vo, Io=Io, eta=eta, f=f, r=r, dV=dV):
    D = Vo / (Vi * eta + Vo)
    Ii = Vo * Io / (Vi * eta)
    IL = Io / (1 - D)
    L = Vi * D / (f * r * IL)
    Ipk = IL * (1 + r / 2)
    Vsw = Vi + Vo
    Cc = Io * D / (f * dV)
    return D, Ii, IL, L, Ipk, Vsw, Cc


D0, Ii0, IL0, L0, Ipk0, Vsw0, C0 = bb(Vi)
assert abs(D0 - 0.54054) < 1e-5 and abs(IL0 - 1.08824) < 1e-5 and abs(L0 - 39.74e-6) < 0.01e-6
assert abs(Ipk0 - 1.25147) < 1e-5 and Vsw0 == 24 and abs(C0 - 10.81e-6) < 0.01e-6
Pin = Vo * Io / eta
Ploss = Pin - Vo * Io
# battery input 9 to 16 V with a 47 uH inductor
Lsel = 47e-6
rows_v = []
for v in (9.0, 12.0, 16.0):
    D, Ii, IL, L, Ipk, Vsw, Cc = bb(v)
    dI = v * D / (f * Lsel)
    rows_v.append((v, D, IL, dI, IL + dI / 2, Vsw, Cc))
Dlo, ILlo, dIlo, Ipklo = rows_v[0][1], rows_v[0][2], rows_v[0][3], rows_v[0][4]
Dhi, ILhi, dIhi, Ipkhi, Vswhi = rows_v[2][1], rows_v[2][2], rows_v[2][3], rows_v[2][4], rows_v[2][5]
assert Ipklo > Ipkhi and dIhi > dIlo
vin_rows = ''.join(f"| {v:g} V | {D*100:.1f}% | {IL:.3f} A | {dI:.3f} A | {pk:.3f} A | {sw:g} V | {cc*1e6:.2f} µF |\n" for v, D, IL, dI, pk, sw, cc in rows_v)
# frequency table at default input
f_rows = ''
for ff in (100e3, 250e3, 500e3, 1e6, 2e6):
    D, Ii, IL, L, Ipk, Vsw, Cc = bb(Vi, f=ff)
    f_rows += f"| {ff/1e3:g} kHz | {L*1e6:.1f} µH | {Cc*1e6:.2f} µF |\n"
# ESR ripple
esr = 0.020
v_esr = Ipk0 * esr

edit('electronics/buck-boost-converter', date=U, phrase='buck-boost converter calculator',
     intro=("An inverting buck-boost converter makes a negative output voltage that can be larger or smaller in magnitude than the input, such as −12 V from a +12 V rail. "
            "This buck-boost converter calculator gives the duty cycle, inductor currents, inductance, switch stress and output capacitance; for a positive output see the "
            "[SEPIC converter](https://www.instrumentationblog.in/sepic-converter-working-design/).\n\n"
            "Power supply designers and hardware engineers use it to create negative rails for op-amps, LCD bias and sensor interfaces from a single supply."),
     body_add=f'''
## Second example: a battery input from 9 to 16 V

The default design takes {Pin:.2f} W from the input to deliver 6 W, so about {Ploss:.2f} W is lost in the switch, diode and inductor. Now suppose the input is a vehicle or lead-acid battery that varies from 9 to 16 V while the output stays at −12 V, 0.5 A, and the standard **47 µH** inductor chosen at 12 V is kept. The ripple with a fixed inductor is ΔI = V<sub>i</sub> D ÷ (f L):

| Input | Duty cycle | Inductor current | Ripple ΔI | Peak current | Switch voltage | C (min.) |
|---|---|---|---|---|---|---|
{vin_rows}
The **peak current is highest at the lowest input** ({Ipklo:.3f} A at 9 V), so the inductor saturation rating and the controller current limit are set there. The **ripple and the switch voltage are highest at the highest input** ({dIhi:.3f} A and {Vswhi:g} V at 16 V), so a 40 V MOSFET and diode give sensible margin. The output capacitor is sized at the minimum input, where the duty cycle and so the on-time are longest.

## Effect of switching frequency

Default 12 V to −12 V at 0.5 A, 30% ripple and 50 mV output ripple:

| Frequency | L required | C (min.) |
|---|---|---|
{f_rows}
Higher frequency shrinks both parts in proportion, but switching loss rises with frequency, which is why 300 kHz to 1 MHz is a common compromise at this power level.

## Building it from a buck regulator

Many designs use an ordinary synchronous buck IC as an inverting buck-boost by tying its ground pin to the −12 V output. The IC then sees V<sub>i</sub> + |V<sub>o</sub>| between its input and ground pins, 24 V in the default case, so it must be rated for that sum rather than for the 12 V input. Its enable and logic pins are also referenced to the negative rail and may need level shifting.

## Common mistakes

- **Sizing the inductor at the nominal input only.** At 9 V the peak current rises to {Ipklo:.3f} A, about {(Ipklo/rows_v[1][4]-1)*100:.0f}% above the {rows_v[1][4]:.3f} A at 12 V.
- **Ignoring ESR ripple.** A capacitor with 20 mΩ ESR adds {Ipk0:.4f} × 0.020 = {v_esr*1000:.0f} mV, half of the 50 mV budget on its own.
- **Forgetting DC bias derating.** A 10 µF X7R ceramic can lose half its value at 12 V; check the bias curve.
- **Reversing polarised output capacitors.** The output is negative, so an electrolytic's positive lead goes to ground.
- **Probing with a long ground lead.** The pulsed output current makes the ripple look far worse than it is; use a short ground spring at the capacitor.
''',
     faq_add=[('How does a changing input voltage affect a buck-boost design?',
               f'With the output fixed, low input means a higher duty cycle and a higher peak current ({Ipklo:.3f} A at 9 V for the default load with 47 µH), while high input gives more ripple and more switch voltage ({Vswhi:g} V at 16 V). Check the inductor and capacitor at the minimum input and the switch rating at the maximum.'),
              ('Can I use a buck regulator IC to make a negative voltage?',
               'Yes, many buck ICs are approved by their makers for the inverting buck-boost connection. The IC ground goes to the negative output, so its maximum input rating must exceed the input voltage plus the output magnitude, and the available output current is lower than in buck mode.')])

# ---------------------------------------------------------------- LC resonant frequency
L, Cc, R = 10e-6, 100e-9, 1.0


def res(L, C, R):
    f0 = 1 / (2 * math.pi * math.sqrt(L * C))
    w = 2 * math.pi * f0
    X = w * L
    Qf = X / R
    return f0, w, X, Qf, f0 / Qf


f0, w0, X0, Q0, BW0 = res(L, Cc, R)
assert abs(f0 - 159154.94) < 0.01 and abs(w0 - 1e6) < 1e-3 and abs(X0 - 10) < 1e-9 and abs(Q0 - 10) < 1e-9 and abs(BW0 - 15915.49) < 0.01
# exact -3 dB edges of series RLC
k = math.sqrt(1 + 1 / (4 * Q0 ** 2))
f_lo, f_hi = f0 * (k - 1 / (2 * Q0)), f0 * (k + 1 / (2 * Q0))
assert abs((f_hi - f_lo) - BW0) < 1e-6
# voltage magnification at 1 V drive
Vdrive = 1.0
Vc = Q0 * Vdrive
# parallel tank dynamic resistance
Rd = Q0 * X0
# 50 ohm generator
Q50 = X0 / (R + 50)
# AM band tuning with 240 uH
La = 240e-6


def cfor(fr, L):
    return 1 / ((2 * math.pi * fr) ** 2 * L)


c530, c1700 = cfor(530e3, La), cfor(1700e3, La)
cratio = c530 / c1700
# forgetting 2 pi
f_no2pi = 1 / math.sqrt(L * Cc)
q_rows = ''
for rr in (0.1, 0.5, 1, 2, 5, 10):
    _, _, _, q, bw = res(L, Cc, rr)
    q_rows += f"| {rr:g} Ω | {q:.2f} | {bw:,.0f} Hz | {q*Vdrive:.2f} V |\n"

edit('electronics/resonant-frequency', date=U, phrase='lc resonant frequency calculator',
     intro=("An inductor and a capacitor resonate at the one frequency where their reactances are equal and cancel, as explained in "
            "[LC resonant circuit frequency](https://www.instrumentationblog.in/lc-resonant-circuit-frequency/). "
            "This LC resonant frequency calculator finds that frequency from L and C, or the part needed for a target, with reactance, Q and bandwidth.\n\n"
            "Radio designers, filter designers and electronics students use it to tune oscillators, receivers, wireless chargers and notch filters."),
     body_add=f'''
## Where the default circuit's bandwidth edges fall

For the default 10 µH, 100 nF and 1 Ω, the bandwidth of {BW0:,.0f} Hz is not split exactly evenly around 159,155 Hz. The exact −3 dB frequencies of a series RLC circuit are f₀ × (√(1 + 1/4Q²) ∓ 1/2Q), which gives **{f_lo:,.0f} Hz** and **{f_hi:,.0f} Hz**. Their geometric mean is f₀, which is why resonance curves look symmetrical on a logarithmic frequency axis.

Driven by 1 V at resonance, the current is 1 V ÷ 1 Ω = 1 A and the voltage across the capacitor and the inductor is Q times the drive, **{Vc:.0f} V** each, in antiphase so they cancel. Used as a parallel tank with the same coil, the impedance at resonance is about Q × X = **{Rd:.0f} Ω**.

## Q and bandwidth versus series resistance

Default L and C, 1 V drive:

| Series R | Q | Bandwidth | Voltage across C at f₀ |
|---|---|---|---|
{q_rows}
## Second example: tuning the AM broadcast band

A 240 µH ferrite rod coil covering 530 to 1,700 kHz needs **{c530*1e12:.1f} pF** at the bottom of the band and **{c1700*1e12:.1f} pF** at the top. Because f varies as 1/√C, a frequency ratio of {1700/530:.2f} needs a capacitance ratio of {cratio:.1f}. A classic variable capacitor of about 10 to 365 pF just covers it once wiring and coil stray capacitance are added.

## Measuring resonance on the bench

Drive the circuit from a signal generator through a small coupling capacitor or a high resistance, watch the voltage across the capacitor on an oscilloscope, and sweep for the peak. Note the two frequencies where the amplitude falls to 0.707 of the peak; their difference is the bandwidth and Q = f₀ ÷ BW. A vector network analyser or an LCR meter that sweeps frequency does the same job automatically.

## Common mistakes

- **Leaving out the 2π.** 1 ÷ √(LC) is the angular frequency, {f_no2pi:,.0f} rad/s here; quoting it as hertz is 6.28 times too high.
- **Driving it straight from a 50 Ω generator.** The source resistance adds to R, so Q falls from {Q0:.0f} to {Q50:.2f} and the peak almost disappears; couple in loosely.
- **Rating the capacitor for the supply voltage.** At resonance it sees Q times the drive, {Vc:.0f} V from 1 V in this example.
- **Ignoring the scope probe.** A ×10 probe adds roughly 10 to 15 pF, enough to pull a small-capacitance tank noticeably lower in frequency.
- **Using series-circuit formulas for a parallel tank fed by a resistive source.** The source and load resistances also damp a parallel circuit and lower its Q.
''',
     faq_add=[('Why can the capacitor voltage be higher than the supply at resonance?',
               f'In a series RLC circuit the current at resonance is limited only by R, and the voltages across L and C are each Q times the drive voltage but opposite in phase. With the default values Q = {Q0:.0f}, so a 1 V source puts {Vc:.0f} V across the capacitor.'),
              ('How do I measure the Q of a resonant circuit?',
               f'Sweep the frequency, find the peak at f₀ and the two points where the response is 0.707 of the peak, then divide f₀ by their difference. For the default circuit the edges are about {f_lo:,.0f} Hz and {f_hi:,.0f} Hz, giving Q = 10.')])

# ---------------------------------------------------------------- PWM duty cycle
fp, ton, Vp = 1000.0, 0.25e-3, 12.0
T = 1 / fp
D = ton / T
toff = T - ton
Vav = D * Vp
Vrms = math.sqrt(D) * Vp
assert abs(T - 1e-3) < 1e-15 and abs(D - 0.25) < 1e-12 and abs(toff - 0.75e-3) < 1e-15 and abs(Vav - 3) < 1e-9 and abs(Vrms - 6) < 1e-9


def ripple(tau):
    a, b, cc = math.exp(-ton / tau), math.exp(-toff / tau), math.exp(-T / tau)
    return Vp * (1 - a) * (1 - b) / (1 - cc)


Rf, Cf = 10e3, 1e-6
tau0 = Rf * Cf
fc0 = 1 / (2 * math.pi * tau0)
vpp0 = ripple(tau0)
settle = 5 * tau0
rc_rows = ''
for tau in (1e-3, 2.2e-3, 4.7e-3, 10e-3, 22e-3, 47e-3):
    rc_rows += f"| {tau*1e3:g} ms | {1/(2*math.pi*tau):.1f} Hz | {ripple(tau)*1000:,.0f} mV | {5*tau*1e3:g} ms |\n"
# same on-time at 2 kHz
D2 = ton / (1 / 2000)
# servo
D_servo = 1.5e-3 / 20e-3
# heater 6 ohm
Rh = 6.0
Ph_full = Vp ** 2 / Rh
Ph = Vrms ** 2 / Rh
assert abs(Ph / Ph_full - D) < 1e-12
# rise/fall error: 20 us each with linear edges at 20 kHz, same 25%
tr = 2e-6
f20 = 20e3

edit('electronics/pwm-duty-cycle', date=U, phrase='pwm duty cycle calculator',
     intro=("Pulse width modulation controls power by switching a supply fully on and off very fast and varying the on-time to set the average; see "
            "[pulse width modulation and duty cycle](https://www.instrumentationblog.in/pulse-width-modulation-duty-cycle/). "
            "This PWM duty cycle calculator solves for period, duty, off time and average and RMS voltage.\n\n"
            "Embedded developers, motor and lighting engineers and technicians use it to set timer registers, dim LEDs, control DC motors and understand "
            "[VFDs](https://www.instrumentationblog.in/vfd-working-principle-explained/)."),
     body_add=f'''
## Filtering the default signal into a DC level

Passing the default 1 kHz, 25%, 12 V signal through a 10 kΩ and 1 µF low-pass filter (τ = {tau0*1e3:.0f} ms, cutoff {fc0:.1f} Hz) gives a 3 V average with a steady-state ripple of

V<sub>pp</sub> = V (1 − e<sup>−t<sub>on</sub>/τ</sup>)(1 − e<sup>−t<sub>off</sub>/τ</sup>) ÷ (1 − e<sup>−T/τ</sup>) = **{vpp0*1000:.0f} mV**

and takes about 5τ = **{settle*1e3:.0f} ms** to settle after a duty change. A bigger time constant lowers the ripple but slows the response:

| Time constant | Cutoff | Ripple (p-p) | Settling (5τ) |
|---|---|---|---|
{rc_rows}
Raising the PWM frequency is the better lever: the ripple falls almost in proportion to frequency without slowing the response.

## On-time versus duty register

Timers set either a fixed on-time or a fixed compare value relative to the period. Keeping the 0.25 ms pulse but moving to 2 kHz makes the duty **{D2*100:.0f}%** and the average {D2*Vp:.0f} V, while a fixed compare value keeps 25% at any frequency. Servos are the opposite case: they read the pulse width, so 1.5 ms at 50 Hz is centre position even though the duty is only {D_servo*100:.1f}%.

## Measuring PWM in practice

An oscilloscope shows the duty directly and reveals slow edges. Most digital multimeters on DC volts display the average, {Vav:.0f} V for the default signal, while a true RMS meter set to AC+DC reads {Vrms:.0f} V. Many meters also have a duty-cycle % function, but it needs a clean signal above the meter's trigger level. For a 6 Ω heater the power at 25% is {Vrms:.0f}² ÷ 6 = {Ph:.0f} W, a quarter of the {Ph_full:.0f} W at full on.

## Common mistakes

- **Forgetting inverted drive logic.** A P-channel high-side switch or an active-low driver is on when the pin is low, so the load sees 100% minus the programmed duty.
- **Changing frequency with a fixed on-time.** As shown above, the duty and output double when the frequency doubles.
- **Setting the filter cutoff too close to the PWM frequency.** With τ = 1 ms at 1 kHz the ripple is still {ripple(1e-3)*1000:,.0f} mV, far from a clean DC level.
- **Ignoring edge time at high frequency.** At {f20/1e3:.0f} kHz the period is {1/f20*1e6:.0f} µs, so {tr*1e6:.0f} µs rise and fall edges are a noticeable part of a 25% on-time of {0.25/f20*1e6:.1f} µs.
- **Measuring with an average-responding AC meter.** On a pulse train it reads neither the average nor the RMS correctly.
''',
     faq_add=[('Does changing the PWM frequency change the duty cycle?',
               f'Only if the on-time is held fixed. A 0.25 ms pulse is 25% at 1 kHz but {D2*100:.0f}% at 2 kHz. Microcontroller PWM normally holds the compare value as a fraction of the period, so the duty stays the same when the frequency changes.'),
              ('How much ripple is left after an RC filter on a PWM output?',
               f'For the default 1 kHz, 25%, 12 V signal into 10 kΩ and 1 µF, the ripple is about {vpp0*1000:.0f} mV peak to peak around the 3 V average. Increasing the time constant or the PWM frequency reduces it.')])

print('done', inplace.DONE)

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-23), slice 6: op-amp-gain, transimpedance-amplifier, lc-filter, inductor-energy, wheatstone-bridge.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-23'
IB = 'https://www.instrumentationblog.in/'


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Op-amp gain
t, Rf, Ri, Vin = 1, 100e3, 10e3, 0.100
G = t * (1 + Rf / Ri) - (1 - t) * Rf / Ri
Vout = G * Vin
GdB = 20 * math.log10(abs(G))
assert abs(G - 11) < 1e-12 and abs(Vout - 1.1) < 1e-12 and abs(GdB - 20.83) < 0.005
tol = 0.01
Gmax = 1 + Rf * (1 + tol) / (Ri * (1 - tol))
Gmin = 1 + Rf * (1 - tol) / (Ri * (1 + tol))
errw = (Gmax / G - 1) * 100
# finite bandwidth: GBW 1 MHz, signal 20 kHz
GBW1, fsig = 1e6, 20e3
fc = GBW1 / G
G20 = G / math.sqrt(1 + (fsig / fc) ** 2)
err20 = (1 - G20 / G) * 100
# offset and bias current
Vos, Ib = 1e-3, 100e-9
Voff = Vos * G
Vbias = Ib * Rf
Rcomp = Rf * Ri / (Rf + Ri)
# slew rate limit at 1.1 V peak with 0.5 V/us
SR = 0.5e6
fslew = SR / (2 * math.pi * Vout)
assert abs(fslew - 72.3e3) < 100
# worst-case gain error table


def wc_noninv(g, tl):
    r = g - 1
    return ((1 + r * (1 + tl) / (1 - tl)) / g - 1) * 100


def wc_inv(g, tl):
    return ((1 + tl) / (1 - tl) - 1) * 100


tol_rows = ''
for g in (2, 11, 101):
    tol_rows += f"| {g} | {wc_noninv(g, 0.05):.1f}% | {wc_noninv(g, 0.01):.2f}% | {wc_noninv(g, 0.001):.3f}% | {wc_inv(g, 0.01):.2f}% |\n"

edit('electronics/op-amp-gain', date=U, phrase='op-amp gain calculator',
     intro=("Two resistors set the closed-loop gain of an operational amplifier, in either the inverting or the non-inverting form. "
            "This op-amp gain calculator returns the gain as a ratio and in dB plus the ideal output, and finds Rf or Rin for a target gain.\n\n"
            "Circuit designers, students and instrument technicians use it to scale sensor signals for ADCs and check stages. Start with "
            f"[op-amp basics]({IB}operational-amplifier-op-amp-basics/), the [voltage follower]({IB}voltage-follower-unity-gain-buffer-explained/) "
            f"and how an [instrumentation amplifier differs from an op-amp]({IB}instrumentation-amplifier-vs-op-amp-key-differences/)."),
     body_add=f'''
## How accurate is the default gain of 11 in a real circuit?

The ideal formula gives 11 and 1.1 V out for the default 100 kΩ, 10 kΩ and 100 mV. Four real effects pull it away from that:

1. **Resistor tolerance.** With 1% parts the worst case is 1 + 101 ÷ 9.9 = **{Gmax:.3f}** and 1 + 99 ÷ 10.1 = **{Gmin:.3f}**, about ±{errw:.1f}% of 11.
2. **Bandwidth.** On a 1 MHz GBW op-amp the closed-loop bandwidth is 1 MHz ÷ 11 = {fc/1e3:.1f} kHz. At 20 kHz the gain has already fallen to 11 ÷ √(1 + (20 ÷ {fc/1e3:.1f})²) = **{G20:.3f}**, {err20:.1f}% low, even though 20 kHz is well inside the −3 dB point.
3. **Offset voltage.** A 1 mV input offset is multiplied by the noise gain, so the output sits **{Voff*1e3:.0f} mV** away from zero with no signal, {Voff/Vout*100:.0f}% of the 1.1 V output.
4. **Bias current.** 100 nA of bipolar input bias current flowing through R<sub>f</sub> adds {Vbias*1e3:.0f} mV. A {Rcomp/1e3:.2f} kΩ resistor (R<sub>f</sub> ∥ R<sub>in</sub>) in series with the non-inverting input balances the two inputs so only the much smaller offset current matters.

A 0.5 V/µs slew rate limits a full 1.1 V peak sine to about {fslew/1e3:.0f} kHz before the output turns triangular.

## Worst-case gain error from resistor tolerance

| Gain | Non-inverting, 5% | Non-inverting, 1% | Non-inverting, 0.1% | Inverting, 1% |
|---|---|---|---|---|
{tol_rows}
The inverting stage always carries the full error of both resistors, while in the non-inverting stage the fixed "1" dilutes it at low gain.

## Measuring the gain on the bench

Feed a sine from a signal generator at a frequency at least ten times below the expected bandwidth, with an amplitude that keeps the output well inside the rails, and read input and output on the same scope or true RMS meter. To measure offset, short the input to ground, read the output and divide by the noise gain.

## Common mistakes

- **Confusing the two forms.** With the same pair, the inverting stage gives −10, not −11; the "1 +" belongs only to the non-inverting formula.
- **Expecting full gain right up to GBW ÷ G.** The gain is already 3 dB down at that frequency and a few percent low a decade below it at high gain.
- **Ignoring the output swing.** An input of 1 V at gain 11 asks for 11 V, which a 5 V rail-to-rail part clips at about 4.9 V.
- **Leaving Rin out of the source impedance.** In the inverting stage the source resistance adds to R<sub>in</sub>, so a 1 kΩ source cuts the gain from −10 to −{100/11:.2f}.
- **Using megohm resistors to save current.** Bias current, noise and stray capacitance across R<sub>f</sub> all grow, and a few pF across 1 MΩ forms a pole at tens of kHz.
''',
     faq_add=[('Why is my op-amp output not zero when the input is zero?',
               f'Input offset voltage and bias current are amplified. A 1 mV offset in a gain of 11 stage gives about {Voff*1e3:.0f} mV at the output, and 100 nA of bias current through a 100 kΩ feedback resistor adds about {Vbias*1e3:.0f} mV unless the inputs see matched resistances.'),
              ('How much do 1% resistors change the op-amp gain?',
               f'In the worst case for a non-inverting gain of 11, one resistor high and the other low, the gain ranges from {Gmin:.3f} to {Gmax:.3f}, about ±{errw:.1f}%. Use 0.1% resistors or a matched network when gain accuracy matters.')])

# ---------------------------------------------------------------- Transimpedance amplifier
Ip, Rf, Cin, GBW = 10e-6, 100e3, 20e-12, 10e6
Vo = Ip * Rf
f3 = math.sqrt(GBW / (2 * math.pi * Rf * Cin))
Cfb = math.sqrt(Cin / (math.pi * Rf * GBW))
Cf45 = math.sqrt(Cin / (2 * math.pi * Rf * GBW))
assert abs(Vo - 1) < 1e-12 and abs(f3 - 892.1e3) < 100 and abs(Cfb - 2.523e-12) < 0.005e-12 and abs(Cf45 - 1.784e-12) < 0.005e-12
k, T, q = 1.380649e-23, 300.0, 1.602176634e-19
in_rf = math.sqrt(4 * k * T / Rf)
en_out = in_rf * Rf
in_shot = math.sqrt(2 * q * Ip)
enbw = 1.11 * f3
sq = math.sqrt(enbw)
irms_rf = in_rf * sq
irms_shot = in_shot * sq
irms_tot = math.sqrt(irms_rf ** 2 + irms_shot ** 2)
snr_rf = 20 * math.log10(Ip / irms_rf)
snr_tot = 20 * math.log10(Ip / irms_tot)
vrms_rf = irms_rf * Rf
peak_ng = 1 + Cin / Cfb
fz = 1 / (2 * math.pi * Rf * Cfb)
tr = 0.35 / f3
Imax = 4.5 / Rf
off_fet = 1e-12 * Rf
off_bjt = 100e-9 * Rf
tia_rows = ''
for r in (10e3, 100e3, 1e6, 10e6):
    i_n = math.sqrt(4 * k * T / r)
    tia_rows += (f"| {c(r/1e3)} kΩ | {r*1e-6:g} V/µA | {4.5/r*1e6:g} µA | {i_n*1e12:.3f} pA/√Hz | "
                 f"{i_n*r*1e9:.1f} nV/√Hz | {math.sqrt(GBW/(2*math.pi*r*Cin))/1e3:.1f} kHz |\n")

edit('electronics/transimpedance-amplifier', date=U, phrase='transimpedance amplifier calculator',
     intro=("A transimpedance amplifier converts a photodiode's small current into a voltage, Vout = I × Rf, with speed limited by input capacitance and op-amp GBW. "
            "This transimpedance amplifier calculator gives the output, the achievable bandwidth and the feedback capacitor for a flat or 45° phase margin response.\n\n"
            "Optical sensor, lidar and instrument designers use it to choose Rf and Cf before layout; see how a "
            f"[transimpedance amplifier works with a photodiode]({IB}transimpedance-amplifier-photodiode/)."),
     body_add=f'''
## Noise and signal to noise ratio with the default values

The worked example above stops at bandwidth, but a TIA is usually chosen for its noise. Take the same 10 µA, 100 kΩ, 20 pF and 10 MHz design at 300 K:

1. Thermal noise current of R<sub>f</sub> = √(4kT ÷ R<sub>f</sub>) = **{in_rf*1e12:.3f} pA/√Hz**, which appears at the output as {en_out*1e9:.1f} nV/√Hz.
2. Shot noise of the 10 µA photocurrent = √(2qI) = **{in_shot*1e12:.2f} pA/√Hz**, about {in_shot/in_rf:.1f} times larger.
3. A second-order Butterworth response has a noise bandwidth of about 1.11 × f<sub>−3dB</sub> = {enbw/1e3:.0f} kHz, so √ENBW = {sq:.0f}.
4. Integrated: R<sub>f</sub> noise {irms_rf*1e12:.0f} pA rms ({vrms_rf*1e6:.1f} µV rms at the output), shot noise {irms_shot*1e9:.2f} nA rms, total {irms_tot*1e9:.2f} nA rms.
5. SNR = 20 log₁₀(10 µA ÷ {irms_tot*1e9:.2f} nA) = **{snr_tot:.1f} dB**. Without shot noise it would be {snr_rf:.1f} dB.

At this signal level the light itself sets the noise floor, so a bigger R<sub>f</sub> buys little. At nanoamp currents the balance reverses and R<sub>f</sub> noise dominates, which is why weak-signal receivers use 1 to 10 MΩ.

The op-amp's own voltage noise matters too. Above the feedback zero at 1 ÷ (2π R<sub>f</sub> C<sub>f</sub>) = {fz/1e3:.0f} kHz the noise gain rises to 1 + C<sub>in</sub> ÷ C<sub>f</sub> = **{peak_ng:.2f}**, so an op-amp with 10 nV/√Hz contributes about {10*peak_ng:.0f} nV/√Hz there, more than R<sub>f</sub> does.

## Choosing Rf for the output swing

| R<sub>f</sub> | Gain | Max current for 4.5 V swing | R<sub>f</sub> noise current | Output noise from R<sub>f</sub> | Bandwidth at 10 MHz GBW |
|---|---|---|---|---|---|
{tia_rows}
With the default 100 kΩ the output reaches 4.5 V at {Imax*1e6:.0f} µA, leaving 4.5 times headroom over the 10 µA signal.

## Testing a TIA

Drive a fast LED or laser diode with a square wave and watch the output step. A Butterworth design rises in roughly 0.35 ÷ f<sub>−3dB</sub> = {tr*1e9:.0f} ns with about 4% overshoot; ringing means C<sub>f</sub> is too small or C<sub>in</sub> is larger than you assumed. Cover the photodiode to read the dark offset: a FET-input op-amp with 1 pA bias adds only {off_fet*1e6:.1f} µV, while 100 nA of bipolar bias current would add {off_bjt*1e3:.0f} mV.

## Common mistakes

- **Using the photodiode's zero-bias capacitance in a biased circuit.** Reverse bias can cut junction capacitance by half or more, and the op-amp's input capacitance must be added.
- **Calling f<sub>−3dB</sub> the noise bandwidth.** The noise integrates over about 1.11 times the −3 dB frequency for a Butterworth response, more with peaking.
- **Fitting a Cf below 0.5 pF.** Board and resistor parasitics already provide about that much, so the real response is slower than calculated.
- **Ignoring shot noise at high light levels.** Above a few µA the photocurrent's own shot noise usually exceeds R<sub>f</sub> noise.
- **Picking Rf without checking the rails.** A 10 MΩ resistor saturates a 5 V output at only 0.45 µA.
''',
     faq_add=[('Which noise source dominates in a photodiode TIA?',
               f'It depends on the photocurrent. With 10 µA and Rf = 100 kΩ, shot noise is {in_shot*1e12:.2f} pA/√Hz against {in_rf*1e12:.3f} pA/√Hz from Rf, so the light dominates. At low currents Rf noise dominates, and at high frequency the op-amp voltage noise multiplied by 1 + Cin ÷ Cf often takes over.')])

# ---------------------------------------------------------------- LC filter
L, C, R, f = 33e-6, 22e-6, 1.2, 100e3


def lc(L, C, R, f):
    f0 = 1 / (2 * math.pi * math.sqrt(L * C))
    Z0 = math.sqrt(L / C)
    Q = R / Z0
    x = f / f0
    H = 1 / math.sqrt((1 - x ** 2) ** 2 + (x / Q) ** 2)
    return f0, Z0, Q, x, H, 20 * math.log10(H), 20 * math.log10(Q)


f0, Z0, Q, x, H, AdB, G0 = lc(L, C, R, f)
assert abs(f0 - 5907) < 1 and abs(Q - 0.980) < 0.001 and abs(AdB - (-49.1)) < 0.05


def f3db(f0, Q):
    a = 2 - 1 / Q ** 2
    u = (a + math.sqrt(a * a + 4)) / 2
    return f0 * math.sqrt(u)


fm3 = f3db(f0, Q)
# light load: 10% of the load current, R = 12 ohm
_, _, Ql, _, Hl, AdBl, G0l = lc(L, C, 12.0, f)
# capacitance halved by DC bias
f0b, Z0b, Qb, xb, Hb, AdBb, G0b = lc(L, C / 2, R, f)
lost = AdBb - AdB
# 10 mV ripple input example: input ripple amplitude at the switch node fundamental
Vsw = 5.0
Vr = Vsw * H
Vrb = Vsw * Hb
load_rows = ''
for r in (0.6, 1.2, 2.4, 6.0, 12.0, 60.0):
    _, _, qq, _, hh, ad, g0 = lc(L, C, r, f)
    load_rows += f"| {r:g} Ω | {qq:.3f} | {g0:+.1f} dB | {f3db(f0, qq)/1e3:.2f} kHz | {ad:.1f} dB |\n"

edit('electronics/lc-filter', date=U, phrase='lc filter calculator',
     intro=("A series inductor followed by a shunt capacitor forms a second-order low-pass filter that falls at 40 dB per decade above cutoff. "
            "This LC filter calculator gives the cutoff frequency, characteristic impedance √(L/C), load-set Q factor and attenuation at any frequency.\n\n"
            f"Power electronics engineers use it to size the output filter of a [buck converter]({IB}buck-converter-working-principle/), "
            "and audio and supply designers use it to check ripple rejection and resonant peaking."),
     body_add=f'''
## The same filter at light load and with derated capacitors

The default design is well damped at 1.2 Ω, but a converter rarely runs at one load. Two checks matter:

**Light load.** At 10% load the resistance rises to 12 Ω, so Q = 12 ÷ {Z0:.4f} = **{Ql:.2f}** and the gain at f₀ becomes 20 log₁₀({Ql:.2f}) = **{G0l:+.1f} dB**. Any disturbance near {f0/1e3:.1f} kHz, such as a load step, is amplified almost ten times. The attenuation at 100 kHz hardly changes ({AdBl:.1f} dB), because far above f₀ the load has little effect.

**Ceramic capacitor DC bias.** If the 22 µF ceramic falls to 11 µF at its working voltage, f₀ rises to **{f0b:,.0f} Hz**, Z₀ to {Z0b:.3f} Ω and Q falls to {Qb:.3f}. The gain at 100 kHz becomes {AdBb:.1f} dB, so the filter loses {lost:.1f} dB of ripple rejection. With a 5 V peak ripple component at the switching frequency entering the filter, output ripple rises from about {Vr*1e3:.1f} mV to {Vrb*1e3:.1f} mV.

## Effect of load resistance on the default 33 µH, 22 µF filter

| Load R | Q | Gain at f₀ | −3 dB frequency | Gain at 100 kHz |
|---|---|---|---|---|
{load_rows}
The −3 dB frequency equals f₀ only at Q = 0.707. For the default Q of {Q:.3f} it lies at **{fm3/1e3:.2f} kHz**, above f₀.

## Measuring an LC filter

A frequency response analyser or a network analyser with an injection transformer sweeps the filter and shows the peak directly. On a running converter, measure output ripple with the scope probe's ground spring rather than its long ground lead, which picks up switching edges and exaggerates the ripple. Compare the result with the gain in this calculator times the switch-node voltage at the switching frequency.

## Common mistakes

- **Treating f₀ as the −3 dB point.** At f₀ the gain equals Q; the −3 dB frequency moves with damping.
- **Checking Q only at full load.** The peak at no load can be 20 dB or more and can upset the control loop.
- **Using the capacitor's nominal value.** DC bias, temperature and ageing all lower ceramic capacitance and raise f₀.
- **Expecting 40 dB per decade forever.** Capacitor ESR and ESL and inductor winding capacitance flatten the roll-off above a few MHz.
- **Placing f₀ near the loop crossover.** The filter's 180° phase shift around f₀ can make the regulator unstable.
''',
     faq_add=[('Is the cutoff frequency of an LC filter the same as its −3 dB frequency?',
               f'Only when Q = 0.707. At f₀ the gain equals Q, so with the default Q of {Q:.3f} the response is down only {-G0:.2f} dB at f₀ and reaches −3 dB at about {fm3/1e3:.2f} kHz.'),
              ('What happens to an LC output filter at no load?',
               f'The load resistance rises, so Q rises and the filter peaks at f₀. The default 33 µH and 22 µF filter has Q = {Ql:.2f} and {G0l:+.1f} dB of peaking with a 12 Ω load, against {G0:+.2f} dB at 1.2 Ω.')])

# ---------------------------------------------------------------- Inductor energy
L, I, dt = 10e-3, 2.0, 1e-3
E = 0.5 * L * I ** 2
V = L * I / dt
Pav = E / dt
assert abs(E - 0.02) < 1e-12 and abs(V - 20) < 1e-9 and abs(Pav - 20) < 1e-9
Vz = 24.0
t_z = L * I / Vz
P_z = Vz * I / 2
assert abs(P_z * t_z - E) < 1e-12
Rcoil = 12.0 / I
tau = L / Rcoil
fsw = 50
P_cyc = E * fsw
didt = 12.0 / L
t_rise = I / didt
# 20% lower inductance near saturation
I_sat = 2.0
dt_rows = ''
for d in (10e-3, 1e-3, 100e-6, 10e-6, 1e-6):
    dt_rows += f"| {d*1e3:g} ms | {c(L*I/d)} V | {c(E/d)} W |\n"
E_wrong = 0.5 * 10 * I ** 2

edit('electronics/inductor-energy', date=U, phrase='inductor energy calculator',
     intro=("An inductor stores energy in its magnetic field while current flows and releases it when the current changes, which is why a switched-off coil produces a voltage spike. "
            "This inductor energy calculator gives the stored energy, the induced voltage and the average power released at switch-off.\n\n"
            "Electronics and controls engineers use it to size flyback diodes, snubbers and clamps. Read about the "
            f"[inductor working principle]({IB}inductor-working-principle/) and [inductor saturation current]({IB}inductor-saturation-current/)."),
     body_add=f'''
## Sizing a clamp for the default coil

The default 10 mH coil at 2 A holds {E*1e3:.0f} mJ, and every bit of it must go somewhere when the switch opens. Three common ways to absorb it give very different results:

1. **Plain flyback diode.** The coil voltage is held at about 0.7 V and the current decays through the coil's own resistance. If the coil runs from 12 V at 2 A its resistance is {Rcoil:.0f} Ω, so τ = L ÷ R = {tau*1e3:.2f} ms and the current takes about 5τ = **{5*tau*1e3:.1f} ms** to die away. Most of the {E*1e3:.0f} mJ heats the winding.
2. **Diode plus 24 V Zener.** The coil voltage is clamped at 24 V, so the current falls linearly to zero in L × I ÷ V = **{t_z*1e3:.3f} ms**. The Zener absorbs the full {E*1e3:.0f} mJ at an average of 24 V × 1 A = {P_z:.0f} W during that time.
3. **No suppression.** The voltage rises until something breaks down: the transistor, the contacts or the insulation.

If the coil is switched {fsw} times a second, the clamp must dissipate {E*1e3:.0f} mJ × {fsw} = **{P_cyc:.1f} W** continuously, which rules out a small signal Zener.

## Switch-off time and the induced voltage

For 10 mH and 2 A (energy {E*1e3:.0f} mJ):

| Switch-off time | Average induced voltage | Average power released |
|---|---|---|
{dt_rows}
The energy is the same in every row; only the rate changes. Faster interruption means a higher voltage and a shorter, more intense pulse.

## Measuring inductance under current

An LCR meter measures inductance at a small test signal, which tells you nothing about saturation. To check a choke at its working current, apply a known DC voltage through a switch and capture the current on a scope with a current probe: di/dt = V ÷ L. At 12 V the default 10 mH coil ramps at {didt:,.0f} A/s and should reach 2 A in about {t_rise*1e3:.2f} ms (before resistance flattens the curve). If the slope steepens as the current rises, the core is saturating and the stored energy is less than ½LI² suggests.

## Common mistakes

- **Entering henries as millihenries.** 10 H instead of 10 mH gives {E_wrong:.0f} J, a thousand times too much.
- **Forgetting that energy goes with I².** Running the coil at 1.4 times the current roughly doubles the energy the clamp must take.
- **Rating the clamp only for peak voltage.** The Zener or TVS must also absorb the energy per pulse and the average power at the switching rate.
- **Using a plain diode on a fast-release relay or valve.** The slow decay delays drop-out by several milliseconds; a Zener clamp releases far faster.
- **Using small-signal inductance near saturation.** The real inductance at full current can be much lower than the datasheet value.
''',
     faq_add=[('How long does it take an inductor to release its energy through a Zener clamp?',
               f'The current falls linearly at a rate set by the clamp voltage, so t = L × I ÷ V. A 10 mH coil at 2 A clamped at 24 V reaches zero in about {t_z*1e3:.2f} ms, and the clamp absorbs the full {E*1e3:.0f} mJ.')])

# ---------------------------------------------------------------- Wheatstone bridge
Vs, R1, R2, R3, Rx = 10.0, 1000.0, 1000.0, 1000.0, 1010.0


def bridge(Vs, R1, R2, R3, Rx):
    return Vs * (Rx / (R3 + Rx) - R2 / (R1 + R2))


Vo = bridge(Vs, R1, R2, R3, Rx)
Rth = R1 * R2 / (R1 + R2) + R3 * Rx / (R3 + Rx)
Is = Vs / (R1 + R2) + Vs / (R3 + Rx)
assert abs(Vo - 24.876e-3) < 1e-6 and abs(Rth - 1002.49) < 0.01 and abs(Is - 9.975e-3) < 1e-6
# unknown Rx from a measured output
Vm = 12e-3
a = Vm / Vs + R2 / (R1 + R2)
Rx_m = R3 * a / (1 - a)
assert abs(bridge(Vs, R1, R2, R3, Rx_m) - Vm) < 1e-12
# loading by an amplifier input of 10 kohm
Rin = 10e3
Vload = Vo * Rin / (Rin + Rth)
load_err = (1 - Vload / Vo) * 100
# lead resistance: 2 wire, 10 m of cable at 0.1 ohm/m per conductor
Rlead = 2 * 10 * 0.1
Vo_lead = bridge(Vs, R1, R2, R3, Rx + Rlead)
lead_err = (Vo_lead - Vo) * 1e3
dR_equiv = Rlead
# power in Rx at different excitation
ex_rows = ''
for v in (1.0, 2.5, 5.0, 10.0):
    i_r = v / (R3 + Rx)
    ex_rows += f"| {v:g} V | {bridge(v, R1, R2, R3, Rx)*1e3:.3f} mV | {i_r*1e3:.3f} mA | {i_r**2*Rx*1e3:.2f} mW | {v*(v/(R1+R2)+v/(R3+Rx))*1e3:.1f} mW |\n"
P_rx = (Vs / (R3 + Rx)) ** 2 * Rx

edit('electronics/wheatstone-bridge', date=U, phrase='wheatstone bridge calculator',
     intro=("A Wheatstone bridge measures very small resistance changes by balancing two voltage dividers against each other. "
            "This Wheatstone bridge calculator gives the exact output voltage, the output in mV/V, the balancing resistance, the output resistance and the supply current and power.\n\n"
            "Instrument technicians and sensor designers use it for strain gauges, load cells, pressure sensors and RTDs; see these "
            f"[Wheatstone bridge applications]({IB}wheatstone-bridge-10-applications/)."),
     body_add=f'''
## Working back from a measured output

The page solves forwards from Rx, but in the field you usually know the output and need the resistance. Keep the default 10 V and 1,000 Ω fixed arms and suppose the meter reads **12.000 mV**:

1. Right midpoint ratio = V<sub>out</sub> ÷ V<sub>s</sub> + R₂ ÷ (R₁ + R₂) = 0.0012 + 0.5 = **{a:.4f}**
2. R<sub>x</sub> = R₃ × ratio ÷ (1 − ratio) = 1,000 × {a:.4f} ÷ {1-a:.4f} = **{Rx_m:.2f} Ω**

That is a {(Rx_m/1000-1)*100:.3f}% change, slightly more than the 0.480% the linear rule 4V<sub>out</sub> ÷ V<sub>s</sub> would suggest.

## Errors that the formula does not show

- **Amplifier loading.** The default bridge has an output resistance of {Rth:.2f} Ω. An amplifier with only 10 kΩ input resistance reads {Vload*1e3:.3f} mV instead of {Vo*1e3:.3f} mV, {load_err:.1f}% low. An instrumentation amplifier with gigohm inputs makes this negligible.
- **Lead resistance.** A two-wire quarter bridge with 10 m of cable at 0.1 Ω/m per conductor adds {Rlead:.0f} Ω in series with Rx, shifting the output by **{lead_err:.2f} mV**. That is the same as a {dR_equiv/1000*100:.1f}% change in the gauge, a large error next to the 1% being measured.
- **Self-heating.** With 10 V across each 2,010 Ω half, Rx dissipates {P_rx*1e3:.1f} mW. A strain gauge bonded to steel can tolerate this; a thin-film RTD may warm by a measurable fraction of a degree.

## Output and power against excitation (default arms, Rx = 1,010 Ω)

| Excitation | Output | Current in Rx | Power in Rx | Total bridge power |
|---|---|---|---|---|
{ex_rows}
Output scales directly with excitation while self-heating scales with its square, so halving the excitation halves the signal but quarters the heating.

## Measuring with a bridge

Industrial signal conditioners excite load cells at 5 or 10 V and read the output with a ratiometric ADC that uses the same excitation as its reference, so supply drift cancels. Six-wire load cells add sense leads that measure the excitation at the cell itself, removing the voltage drop in long cables. Before calibration, check the zero by reading the output with no load and the balance of each arm with a four-wire ohmmeter.

## Common mistakes

- **Getting the sign convention wrong.** If Rx sits at the top of the right divider instead of the bottom, the output reverses sign.
- **Using V<sub>s</sub>x ÷ 4 for large changes.** The quarter bridge is 0.5% low at a 1% change and 2.5% low at 5%.
- **Wiring a quarter bridge with two wires.** Lead resistance and its temperature drift appear directly as strain or temperature.
- **Choosing excitation for signal only.** High excitation raises self-heating and drift in the sensing element.
- **Measuring the output with a single-ended meter input.** The output rides on about V<sub>s</sub> ÷ 2 of common-mode voltage and needs a differential input.
''',
     faq_add=[('How do I find the unknown resistance from the measured bridge output?',
               f'Add V_out ÷ V_s to R2 ÷ (R1 + R2) to get the right midpoint ratio k, then Rx = R3 × k ÷ (1 − k). With 1,000 Ω arms, 10 V excitation and 12 mV output, k = {a:.4f} and Rx = {Rx_m:.2f} Ω.')])

print('done', 'electronics/op-amp-gain etc')

# ======================================================================= SECTION _expand_c7.py
"""Expand (2026-11-23), slice 7: flyback-transformer.
Numbers computed here from the page's equations. Run once on the original file."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-23'


def c(x, d=0):
    return f"{x:,.{d}f}"


def fly(Vmin, Vmax, Vo, Vf, D, Po, eta, fs):
    n = Vmin * D / ((1 - D) * (Vo + Vf))
    Vor = n * (Vo + Vf)
    Vds = Vmax + Vor
    Pin = Po / eta
    Ipk = 2 * Pin / (Vmin * D)
    Lp = Vmin * D / (Ipk * fs)
    Isp = n * Ipk
    Dmin = Vor / (Vor + Vmax)
    return dict(n=n, Vor=Vor, Vds=Vds, Pin=Pin, Ipk=Ipk, Lp=Lp, Isp=Isp, Dmin=Dmin)


# defaults (already worked on the page); check they still agree
d0 = fly(18, 32, 5, 0.5, 0.45, 10, 0.80, 100e3)
assert abs(d0['n'] - 2.678) < 0.001 and abs(d0['Ipk'] - 3.086) < 0.001 and abs(d0['Lp'] * 1e6 - 26.24) < 0.01
# stored energy per cycle equals Pin / fs at the boundary
E0 = 0.5 * d0['Lp'] * d0['Ipk'] ** 2
assert abs(E0 - d0['Pin'] / 100e3) < 1e-12

# ---- new scenario: universal AC input, 12 V 24 W, 65 kHz
V1, V2, Vo, Vf, D, Po, eta, fs = 100.0, 375.0, 12.0, 0.7, 0.45, 24.0, 0.85, 65e3
r = fly(V1, V2, Vo, Vf, D, Po, eta, fs)
Vin_D = V1 * D
assert abs(r['n'] - 6.443) < 0.001
assert abs(r['Pin'] - 28.235) < 0.001
assert abs(r['Ipk'] - 1.2549) < 0.0005
Lp_uH = r['Lp'] * 1e6
assert 550 < Lp_uH < 555
E = 0.5 * r['Lp'] * r['Ipk'] ** 2
assert abs(E - r['Pin'] / fs) < 1e-12
Iprms = r['Ipk'] * math.sqrt(D / 3)
Isrms = r['Isp'] * math.sqrt((1 - D) / 3)
Iout = Po / Vo
# turn rounding: Ns = 8, Np = n * Ns rounded
Ns = 8
Np = round(r['n'] * Ns)
n_r = Np / Ns
D_r = n_r * (Vo + Vf) / (V1 + n_r * (Vo + Vf))
Vor_r = n_r * (Vo + Vf)
Vds_r = V2 + Vor_r
spike = 0.5 * Vor_r
Vds_pk = Vds_r + spike
Naux = round(Ns * 15.7 / (Vo + Vf))  # 15 V aux plus 0.7 V diode, same volts per turn
Vaux = Naux * (Vo + Vf) / Ns - 0.7
# wrong: using Vo without Vf
n_wrong = V1 * D / ((1 - D) * Vo)

# ---- reference table at the page defaults: duty cycle sweep
rows = ''
for dd in (0.30, 0.35, 0.40, 0.45, 0.50, 0.55):
    t = fly(18, 32, 5, 0.5, dd, 10, 0.80, 100e3)
    rows += (f"| {dd*100:.0f}% | {t['n']:.3f} | {t['Vor']:.2f} V | {t['Vds']:.2f} V | "
             f"{t['Ipk']:.3f} A | {t['Lp']*1e6:.2f} µH | {t['Isp']:.2f} A |\n")
t30 = fly(18, 32, 5, 0.5, 0.30, 10, 0.80, 100e3)
t55 = fly(18, 32, 5, 0.5, 0.55, 10, 0.80, 100e3)

intro = ("A flyback converter stores energy in a gapped coupled inductor while the switch is on and delivers it to the output when the switch turns off. "
         "This flyback transformer calculator gives the turns ratio, reflected voltage, switch voltage stress, peak currents and primary inductance; see "
         "[how a flyback converter works](https://www.instrumentationblog.in/flyback-converter-working-principle-explained/).\n\n"
         "Power supply designers and hobbyists use it to size the transformer, pick a MOSFET voltage rating and check peak currents before winding a prototype.")

body_add = f'''
## Second example: universal AC input, 12 V at 24 W

An offline adapter with a 100 V to 375 V bulk capacitor, 12 V output, fast silicon rectifier (V<sub>f</sub> = 0.7 V), D<sub>max</sub> = 45%, efficiency 85% and 65 kHz:

1. Turns ratio n = 100 × 0.45 ÷ (0.55 × 12.7) = {Vin_D:.0f} ÷ {0.55*12.7:.3f} = **{r['n']:.3f}**
2. Reflected voltage V<sub>OR</sub> = {r['n']:.3f} × 12.7 = **{r['Vor']:.1f} V**; switch voltage at 375 V = **{r['Vds']:.1f} V** before the leakage spike
3. Input power 24 ÷ 0.85 = **{r['Pin']:.2f} W**; peak primary current = 2 × {r['Pin']:.2f} ÷ {Vin_D:.0f} = **{r['Ipk']:.3f} A**
4. Primary inductance L<sub>p</sub> = {Vin_D:.0f} ÷ ({r['Ipk']:.3f} × 65,000) = **{Lp_uH:.0f} µH**; peak secondary current = **{r['Isp']:.2f} A**
5. Duty cycle at 375 V input = **{r['Dmin']*100:.1f}%**

The energy stored each cycle is ½ L<sub>p</sub> I<sub>pk</sub>² = {E*1e6:.0f} µJ, exactly P<sub>in</sub> ÷ f<sub>s</sub>, which is the figure the gapped core must hold without saturating. The primary RMS current is I<sub>pk</sub> √(D ÷ 3) = **{Iprms:.3f} A** and the secondary RMS current is I<sub>sp</sub> √((1 − D) ÷ 3) = **{Isrms:.2f} A**, against a DC output of only {Iout:.0f} A; use these RMS values for winding wire and capacitor ripple ratings.

## From the result to a real winding

Pick a whole number of secondary turns from the core's volts per turn, then round the primary. With N<sub>s</sub> = {Ns}, the primary is {r['n']:.3f} × {Ns} = {r['n']*Ns:.1f}, rounded to **{Np} turns**, a ratio of {n_r:.3f}. Recalculating, the duty cycle at 100 V becomes {D_r*100:.1f}%, V<sub>OR</sub> becomes {Vor_r:.1f} V and the switch sees {Vds_r:.1f} V. Allowing a leakage spike of half V<sub>OR</sub> brings the peak to about {Vds_pk:.0f} V, comfortable for a 650 V MOSFET with clamp tolerance included. A 15 V auxiliary winding for the controller uses the same volts per turn as the secondary: {Naux} turns give about {Vaux:.1f} V after its diode. Finally, choose a primary inductance slightly below the calculated maximum, typically 10% lower, so that inductance tolerance and low line never push the design into continuous mode.

## Duty cycle trade-off at the page defaults

18 V to 32 V input, 5 V and 0.5 V diode, 10 W, 80% efficiency, 100 kHz:

| D<sub>max</sub> | Turns ratio | V<sub>OR</sub> | V<sub>DS</sub> at 32 V | Primary I<sub>pk</sub> | Max L<sub>p</sub> | Secondary I<sub>pk</sub> |
|---|---|---|---|---|---|---|
{rows}
Raising D<sub>max</sub> from 30% to 55% cuts the primary peak current from {t30['Ipk']:.2f} A to {t55['Ipk']:.2f} A, but the switch voltage climbs from {t30['Vds']:.1f} V to {t55['Vds']:.1f} V and the secondary peak rises from {t30['Isp']:.2f} A to {t55['Isp']:.2f} A because the secondary has less time to deliver the energy. Most designs settle between 40% and 50%.

## Common mistakes

- **Leaving the diode drop out of the turns ratio.** For the 12 V example, using 12 V instead of 12.7 V gives n = {n_wrong:.3f}, and the output then sits low at minimum input.
- **Choosing L<sub>p</sub> above the boundary value.** The converter slips into continuous mode at low line, adding a right half plane zero that a DCM compensation network was not designed for.
- **Sizing the MOSFET on V<sub>in,max</sub> + V<sub>OR</sub> alone.** The leakage spike on top can add 30% to 50% of V<sub>OR</sub>; without a clamp the device avalanches every cycle.
- **Taking the average bulk voltage as V<sub>in,min</sub>.** For AC input, V<sub>in,min</sub> is the valley of the bulk capacitor ripple at low line, not the average; designing on the average undersizes the turns ratio and the duty cycle saturates.
- **Ignoring core saturation at start up.** Current limit and peak flux must be checked at the controller's current limit, not just at the nominal I<sub>pk</sub>, or the core saturates during load steps and short circuits.
'''

faq_add = [
    ('How do I calculate primary RMS current in a DCM flyback?',
     f'The primary current is a triangle from zero to I<sub>pk</sub> during the on time, so I<sub>rms</sub> = I<sub>pk</sub> × √(D ÷ 3). For a 24 W, 100 V minimum input design with I<sub>pk</sub> = {r["Ipk"]:.3f} A at 45% duty that is about {Iprms:.3f} A.'),
    ('How much energy must a flyback transformer store?',
     f'In discontinuous mode it must store the full input energy each cycle, ½ L<sub>p</sub> I<sub>pk</sub>² = P<sub>in</sub> ÷ f<sub>s</sub>. A {r["Pin"]:.1f} W input at 65 kHz needs about {E*1e6:.0f} µJ per cycle, held mainly in the air gap.'),
]

n_words = edit('electronics/flyback-transformer', date=U, intro=intro, phrase='flyback transformer calculator',
               body_add=body_add, faq_add=faq_add)
print('slice 7 done', inplace.DONE, n_words)
