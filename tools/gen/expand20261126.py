"""Part C expansion (2026-11-26): 30 engineering, electrical and electronics pages (body under 800 words; priority list empty; featured and recently updated pages skipped). Assembled from six sections; edits applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-26), section c1: availability-mtbf, manometer, turndown-ratio, mass-balance, pressure-to-head.
Every number is computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-26'
G = 9.80665


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Availability (MTBF, MTTR)
mtbf, mttr, tm = 87600.0, 8.0, 8760.0
A = mtbf / (mtbf + mttr)
assert abs(A - 0.9999087) < 1e-7
# control loop in series: transmitter, I/O card, control valve
parts = [('Pressure transmitter', 87600.0, 8.0), ('PLC analogue I/O card', 200000.0, 4.0), ('Control valve and positioner', 50000.0, 24.0)]
prow = ''
A_ser = 1.0
lam_ser = 0.0
for nm, mb, mr in parts:
    a = mb / (mb + mr)
    A_ser *= a
    lam_ser += 8760 / mb
    prow += f"| {nm} | {c(mb)} h | {mr:g} h | {a*100:.4f}% | {(1-a)*8760*60:.1f} min |\n"
dt_ser = (1 - A_ser) * 8760
mtbf_ser = 8760 / lam_ser
# 1oo2 on the valve (two valves in parallel, either can do the job)
av = 50000.0 / (50000.0 + 24.0)
A_v2 = 1 - (1 - av) ** 2
A_ser2 = A_ser / av * A_v2
dt_ser2 = (1 - A_ser2) * 8760
# reliability over mission time for the default MTBF
rrow = ''
for lbl, t in (('1 month', 730), ('6 months', 4380), ('1 year', 8760), ('5 years', 43800), ('10 years', 87600), ('20 years', 175200)):
    R = math.exp(-t / mtbf)
    rrow += f"| {lbl} | {c(t)} h | {R*100:.2f}% | {(1-R)*100:.2f}% |\n"
t_half = mtbf * math.log(2)

edit('engineering/availability-mtbf', date=U,
     before='## Common mistakes',
     body_add=f'''## Second example: a complete control loop

A flow loop works only if every element works, so the availabilities of the parts in series multiply. Typical figures for one loop:

| Element | MTBF | MTTR | Availability | Downtime per year |
|---|---|---|---|---|
{prow}
- Loop availability = product of the three = **{A_ser*100:.4f}%**
- Expected loop downtime = {dt_ser:.2f} h a year, about {dt_ser*60:.0f} minutes
- Failure rates add in series: {lam_ser:.4f} failures a year, so the loop MTBF is {c(mtbf_ser)} h ({mtbf_ser/8760:.1f} years)

The valve, with the lowest MTBF and the longest repair, causes most of the outage. Fitting a second valve in parallel that can take over raises its availability to {A_v2*100:.6f}% and the loop to {A_ser2*100:.4f}%, cutting downtime to {dt_ser2*60:.0f} minutes a year. Spending on the weakest element gives the biggest return.

## Chance of surviving longer missions

For the default MTBF of 87,600 h, with a constant failure rate:

| Mission time | Hours | Probability of no failure | Probability of at least one failure |
|---|---|---|---|
{rrow}
Half of a population has failed at least once by MTBF × ln 2 = {c(t_half)} h, about {t_half/8760:.1f} years, well before the MTBF itself.

''', faq_add=[('How do I calculate the availability of components in series?',
               f'Multiply their availabilities, because the system is down whenever any one part is down. A transmitter at 99.9909%, an I/O card at 99.9980% and a valve at 99.9520% give a loop availability of {A_ser*100:.4f}%, about {dt_ser:.2f} h of downtime a year.'),
              ('After how long will half of my units have failed?',
               f'With a constant failure rate, at MTBF × ln 2, which is 69.3% of the MTBF. For an MTBF of 87,600 h that is {c(t_half)} h, about {t_half/8760:.1f} years.')],
     min_words=800)

# ---------------------------------------------------------------- Manometer
rm, rf, L, th = 1000.0, 1.2, 0.150, math.radians(30)
h = L * math.sin(th)
dp = (rm - rf) * G * h
assert abs(dp - 734.62) < 0.01
mmwc = 1000 * G * h
air = rf * G * h
dp_hg = (13546 - 998) * G * 0.2
dp_hg_wrong = 13546 * G * 0.2
assert abs(dp_hg / 1000 - 24.61) < 0.01 and abs(dp_hg_wrong / 1000 - 26.57) < 0.01
# furnace draft on a 10 degree red oil gauge
SGo = 0.826
rho_o = SGo * 999.97
th2 = math.radians(10)
L2 = 0.072
h2 = L2 * math.sin(th2)
dp2 = (rho_o - 1.2) * G * h2
mm_w2 = dp2 / (999.97 * G) * 1000
# well-type inclined gauge: 6 mm bore tube, 60 mm reservoir
d_t, D_r = 6.0, 60.0
ar = (d_t / D_r) ** 2
h_true = L * (math.sin(th) + ar)
dp_well = (rm - rf) * G * h_true
err_well = (dp_well / dp - 1) * 100
# water density vs temperature, 100 mm vertical reading
wrows = ''
for T, rho in ((4, 999.97), (10, 999.70), (20, 998.21), (30, 995.65), (40, 992.22), (60, 983.20)):
    p = (rho - 1.2) * G * 0.1
    wrows += f"| {T} °C | {rho:.2f} kg/m³ | {p:.1f} Pa | {(p/((999.97-1.2)*G*0.1)-1)*100:+.2f}% |\n"

edit('engineering/manometer', date=U,
     replace=[('Check the default result: 75 mm of water is 75 × 9.79 ≈ 734616.2 Pa, or 74910.0 mm H₂O once the air above the water is allowed for.',
               f'Check the default result: 75 mm of water column is 75 × 9.80665 = {mmwc:.1f} Pa, and the column of air above the water ({air:.2f} Pa) is subtracted, leaving {dp:.1f} Pa.'),
              ('- Δp = (13,546 − 998) × 9.80665 × 0.2 = **24610.77 kPa**',
               f'- Δp = (13,546 {chr(0x2212)} 998) × 9.80665 × 0.2 = {c(dp_hg)} Pa = **{dp_hg/1000:.2f} kPa**')],
     before='## Notes',
     body_add=f'''## Second example: furnace draft on an oil gauge

Boiler draft is read on an inclined gauge filled with red oil (SG {SGo}, {rho_o:.1f} kg/m³) set at 10°. The meniscus has moved {L2*1000:.0f} mm along the scale:

- h = {L2*1000:.0f} × sin 10° = {h2*1000:.2f} mm
- Δp = ({rho_o:.1f} {chr(0x2212)} 1.2) × 9.80665 × {h2:.5f} = **{dp2:.1f} Pa**, which is {mm_w2:.2f} mm of water column

On a vertical water tube the same draft would move the level only {mm_w2:.1f} mm, too little to read to the precision needed for burner tuning.

## Reservoir drop in a well-type gauge

Most portable inclined gauges have one leg as a reservoir. As liquid rises in the tube, the reservoir falls by the tube area ÷ reservoir area times the scale movement, so the true height is h = L (sin θ + a ÷ A). With a {d_t:.0f} mm bore and a {D_r:.0f} mm reservoir, a ÷ A = {ar:.4f}. At the default 150 mm and 30° the true height is {h_true*1000:.2f} mm and the pressure {dp_well:.1f} Pa, {err_well:.1f}% more than the plain L sin θ figure. Commercial scales already include this correction; it matters when you make your own scale or calculate from a ruler.

## Effect of water temperature (100 mm vertical reading, air above)

| Water temperature | Density | Pressure | Change from 4 °C |
|---|---|---|---|
{wrows}
''', faq_add=[('Does temperature affect a manometer reading?',
               'Yes, through the density of the filling liquid. Water at 40 °C is about 0.8% less dense than at 4 °C, so the same reading means about 0.8% less pressure. Gauge oils expand more, so oil-filled gauges are often marked with the temperature their scale assumes.')],
     min_words=800)

# ---------------------------------------------------------------- Turndown ratio
Qmax, Qmin = 100.0, 10.0
TD = Qmax / Qmin
dpr = (Qmin / Qmax) ** 2
assert TD == 10 and abs(dpr - 0.01) < 1e-12
# flow error from a DP transmitter error of 0.1% of span, on a square root meter
e_span = 0.001
frow = ''
for fq in (1.0, 0.5, 0.3, 0.2, 0.1):
    dpf = fq ** 2
    ef = (math.sqrt(dpf + e_span) - fq) / fq * 100
    frow += f"| {fq*100:.0f}% | {dpf*100:.2f}% | {e_span/dpf*100:.2f}% | ±{ef:.2f}% |\n"
# stacked transmitters: high range 0 to 250 mbar, low range 0 to 25 mbar
dp_hi = 250.0
dp_lo = 25.0
sw = math.sqrt(dp_lo / dp_hi)
e_lo = 0.001 * dp_lo
f10 = 0.1
ef_hi = (math.sqrt(f10 ** 2 * dp_hi + e_span * dp_hi) / math.sqrt(f10 ** 2 * dp_hi) - 1) * 100
ef_lo = (math.sqrt(f10 ** 2 * dp_hi + e_lo) / math.sqrt(f10 ** 2 * dp_hi) - 1) * 100
# meter sized too large
Qmeter = 200.0
td_cat = 100.0
Qmin_meter = Qmeter / td_cat
td_used = Qmax / Qmin_meter

edit('engineering/turndown-ratio', date=U,
     before='## Getting more turndown in practice',
     body_add=f'''## How transmitter error grows at low flow

A DP transmitter with an error of 0.1% of its span, on an orifice meter where flow is proportional to √DP:

| Flow (% of max) | DP (% of span) | Transmitter error as % of the DP | Resulting flow error |
|---|---|---|---|
{frow}
The flow error roughly quadruples each time the flow halves, because it varies as 1 ÷ flow². Below about 10% flow, the reading is dominated by transmitter error, zero drift and noise, which is why the square root output is usually cut off there.

## Second example: stacking two transmitters

The default 10:1 range is put on an orifice with a 0 to {dp_hi:.0f} mbar transmitter and a second one ranged 0 to {dp_lo:.0f} mbar. The system switches to the low range transmitter below √({dp_lo:.0f} ÷ {dp_hi:.0f}) = **{sw*100:.1f}%** of maximum flow. At the 10 m³/h minimum, the DP is 2.5 mbar: the high range unit (error ±{e_span*dp_hi:.2f} mbar) gives about ±{ef_hi:.1f}% flow error, while the low range unit (error ±{e_lo:.3f} mbar) gives about ±{ef_lo:.2f}%.

## Catalogue turndown versus usable turndown

A Coriolis meter rated {td_cat:.0f}:1 with a maximum of {Qmeter:.0f} m³/h measures down to {Qmin_meter:.0f} m³/h. On a duty of 10 to 100 m³/h the process needs only 10:1 and the meter could reach {td_used:.0f}:1 of the process maximum, so it has margin. Turn the problem round when choosing: divide the meter's maximum by its rated turndown and check that the result is below your lowest flow.

''', faq_add=[('How accurate is a DP flow meter at low flow?',
               'Much less accurate than at full flow, because flow varies with the square root of DP. A transmitter error of 0.1% of span becomes about 0.05% of flow at full scale but about 5% of flow at 10% of maximum flow.')],
     min_words=800)

# ---------------------------------------------------------------- Mass balance
m1, x1, m2, x2, xt = 1200.0, 0.32, 800.0, 0.05, 0.20
m3 = m1 + m2
mc = m1 * x1 + m2 * x2
x3 = mc / m3
m2r = m1 * (x1 - xt) / (xt - x2)
assert m3 == 2000 and abs(mc - 424) < 1e-9 and abs(x3 - 0.212) < 1e-12 and abs(m2r - 960) < 1e-9
# evaporator: 5000 kg/h of 12% juice concentrated to 60%
F, xF, xP = 5000.0, 0.12, 0.60
P = F * xF / xP
W = F - P
# plant data check
mm1, mm2, xm1, xm2, xa = 1200.0, 800.0, 0.32, 0.05, 0.226
mc_in = mm1 * xm1 + mm2 * xm2
mc_out = (mm1 + mm2) * xa
gap = mc_out - mc_in
gap_pct = gap / mc_in * 100
# what stream 1 flow would need to be to explain the analyser
m1_implied = (mm2 * (xa - xm2)) / (xm1 - xa)
# evaporation table
erow = ''
for xp in (0.20, 0.30, 0.40, 0.50, 0.60, 0.65):
    p = F * xF / xp
    erow += f"| {xp*100:.0f}% | {c(p)} kg/h | {c(F-p)} kg/h | {(F-p)/F*100:.1f}% |\n"

edit('engineering/mass-balance', date=U,
     before='## Mass balances in practice',
     body_add=f'''## Second example: concentrating by evaporation

Removing solvent is a mass balance with one stream leaving instead of joining. An evaporator takes {c(F)} kg/h of fruit juice at {xF*100:.0f}% dissolved solids and produces a {xP*100:.0f}% concentrate. The solids pass through unchanged, so:

- Concentrate flow = {c(F)} × {xF} ÷ {xP} = **{c(P)} kg/h**
- Water evaporated = {c(F)} {chr(0x2212)} {c(P)} = **{c(W)} kg/h**

| Product strength | Product flow | Water removed | Share of feed evaporated |
|---|---|---|---|
{erow}
Most of the water goes in the early stages: reaching 30% already removes 60% of the feed, while going from 50% to 60% removes only a further 4% of it.

## Third example: checking plant data

On the default mixer, the outlet analyser reads {xa*100:.1f}% while the inlet meters and grab samples still give 1,200 kg/h at 32% and 800 kg/h at 5%. NaOH in = {c(mc_in)} kg/h; NaOH out = 2,000 × {xa} = {c(mc_out)} kg/h. The {gap:.0f} kg/h gap is {gap_pct:.1f}% of the input, far outside normal meter uncertainty. If the analyser were right, stream 1 would have to be about {c(m1_implied)} kg/h, so the next step is to check the stream 1 flow meter and recalibrate the analyser against a laboratory sample.

''', faq_add=[('How much water must be evaporated to concentrate a solution?',
               f'Water removed = F × (1 {chr(0x2212)} x_feed ÷ x_product), because the dissolved solids are conserved. Concentrating {c(F)} kg/h of 12% solution to 60% removes {c(W)} kg/h of water and leaves {c(P)} kg/h of product.'),
              ('How do I use a mass balance to check plant instruments?',
               'Calculate the component flow in and out from the meters and analysers. If they differ by more than the combined uncertainty, usually 1 to 2%, one of the instruments is wrong; working out which value would close the balance shows where to look first.')],
     min_words=800)

# ---------------------------------------------------------------- Pressure to head
dp_, rho_ = 5e5, 998.0
H = dp_ / (rho_ * G)
assert abs(H - 51.09) < 0.01
# NPSH available: open tank, water at 60 C
Patm, Pv, rho60 = 101325.0, 19946.0, 983.2
z, hf = 2.0, 0.8
H_atm = Patm / (rho60 * G)
H_v = Pv / (rho60 * G)
NPSHa = H_atm - H_v + z - hf
NPSHr = 4.5
margin = NPSHa - NPSHr
# same pump on cold water at 20 C
Pv20, rho20 = 2339.0, 998.2
NPSHa20 = Patm / (rho20 * G) - Pv20 / (rho20 * G) + z - hf
# velocity head: 60 m3/h, suction DN150, discharge DN100
Q = 60 / 3600
vs = Q / (math.pi * 0.15 ** 2 / 4)
vd = Q / (math.pi * 0.10 ** 2 / 4)
hv = (vd ** 2 - vs ** 2) / (2 * G)
# hot water table, head of 1 bar
trow = ''
for T, rho in ((20, 998.2), (40, 992.2), (60, 983.2), (80, 971.8), (90, 965.3), (100, 958.4)):
    trow += f"| {T} °C | {rho:.1f} kg/m³ | {1e5/(rho*G):.3f} m | {(1e5/(rho*G))/(1e5/(998.2*G))*100-100:+.2f}% |\n"

edit('engineering/pressure-to-head', date=U,
     before='## Notes',
     body_add=f'''## NPSH available from pressures

Net positive suction head is the same conversion applied to the suction side. A pump draws water at 60 °C ({rho60} kg/m³) from an open tank whose level is {z:.0f} m above the pump centreline, with {hf} m of friction loss in the suction line:

- Atmospheric pressure as head: 101,325 ÷ ({rho60} × 9.80665) = {H_atm:.2f} m
- Vapour pressure of water at 60 °C (19.95 kPa) as head: {H_v:.2f} m
- NPSH available = {H_atm:.2f} {chr(0x2212)} {H_v:.2f} + {z:.1f} {chr(0x2212)} {hf} = **{NPSHa:.2f} m**

Against a pump needing {NPSHr} m, the margin is {margin:.2f} m. The same system on 20 °C water gives {NPSHa20:.2f} m, so heating the water has cost about {NPSHa20-NPSHa:.1f} m of suction margin.

## Velocity head when pipe sizes differ

When suction and discharge pipes differ, total head also includes (v<sub>d</sub>² {chr(0x2212)} v<sub>s</sub>²) ÷ 2g. At 60 m³/h, a 150 mm suction carries {vs:.2f} m/s and a 100 mm discharge {vd:.2f} m/s, adding {hv:.2f} m. That is under 1% of the 51 m example head, but on a low head pump it can be several percent.

## Head of 1 bar of water at higher temperatures

| Water temperature | Density | Head per bar | Change from 20 °C |
|---|---|---|---|
{trow}
''', faq_add=[('How do I calculate NPSH available from pressure readings?',
               f'Convert absolute suction pressure and vapour pressure to head with H = p ÷ (ρg), then NPSHa = (p_abs {chr(0x2212)} p_vapour) ÷ (ρg) + static height {chr(0x2212)} suction friction. For 60 °C water from an open tank 2 m above the pump with 0.8 m of friction, NPSHa is about {NPSHa:.1f} m.')],
     min_words=800)

print('done', __import__('inplace').DONE)

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-26), section c2: valve-authority, weir-flow, residence-time, rotameter-correction, hazen-williams.
Every number is computed here from correct formulas and each page's defaults. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-26'
G = 9.80665
MINUS = chr(0x2212)


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Valve authority
N0 = 0.5 / (0.5 + 1.0)
assert abs(N0 - 0.3333) < 1e-3
# sizing a valve for a coil branch: 3.6 m3/h, coil 25 kPa, branch pipe and fittings 15 kPa
Qv, dp_coil, dp_pipe = 3.6, 0.25, 0.15
dp_circ = dp_coil + dp_pipe
Kv_ideal = Qv / math.sqrt(dp_circ)          # valve takes as much as the circuit, N = 0.5
kv_rows = ''
kv_pick = {}
for Kv in (2.5, 4.0, 6.3, 10.0):
    dpv = (Qv / Kv) ** 2
    N = dpv / (dpv + dp_circ)
    kv_pick[Kv] = (dpv, N)
    kv_rows += f"| {Kv:g} | {dpv:.3f} bar ({dpv*100:.1f} kPa) | {N:.2f} | {(dpv+dp_circ)*100:.1f} kPa |\n"
dpv63, N63 = kv_pick[6.3]
dpv40, N40 = kv_pick[4.0]
# pump energy cost of the extra 0.48 bar for Kv 4.0 versus 6.3, 8000 h/yr, pump+motor 60%
d_dp = (dpv40 - dpv63) * 1e5
P_extra = (Qv / 3600) * d_dp / 0.60
E_extra = P_extra * 8000 / 1000
# part load drift: branch available pressure rises from 0.73 to 1.0 bar when other branches close
avail_design = dpv63 + dp_circ
avail_low = 1.0
N_eff = dpv63 / avail_low

edit('engineering/valve-authority', date=U, before='## How to get the pressure drops',
     body_add=f'''## Second example: choosing a Kv for a coil branch

A heating coil needs {Qv} m³/h of water. The coil drops {dp_coil*100:.0f} kPa and the branch pipe and fittings another {dp_pipe*100:.0f} kPa, so the circuit drop is {dp_circ*100:.0f} kPa. For N = 0.5 the valve must also drop {dp_circ*100:.0f} kPa, which needs Kv = Q ÷ √Δp = {Qv} ÷ √{dp_circ:.2f} = **{Kv_ideal:.2f}**. Valves come in a stepped Kv series, so check the neighbours:

| Kv | Valve Δp at {Qv} m³/h | Authority N | Branch Δp needed |
|---|---|---|---|
{kv_rows}
Kv 6.3 gives N = {N63:.2f}, just under the target; Kv 4.0 gives {N40:.2f} but asks the pump for {(dpv40-dpv63)*100:.0f} kPa more at this branch. Running {8000:,} h a year with a 60% efficient pump set, that extra pressure costs about {P_extra:.0f} W, or {E_extra:.0f} kWh a year for this one branch, so most designers would take the Kv 6.3 valve.

## Authority changes at part load

The calculation assumes the branch sees {avail_design*100:.0f} kPa at design flow. When other branches close on a constant speed pump, the pressure across this branch can rise to, say, {avail_low*100:.0f} kPa. The valve then has to throttle the extra pressure as well, and the effective authority based on what it really controls becomes {dpv63*100:.1f} ÷ {avail_low*100:.0f} = **{N_eff:.2f}**. A differential pressure controller on the branch, or variable speed pumping on a remote sensor, keeps the design figure close to the real one.

''',
     faq_add=[('How do I choose a valve Kv for a target authority?',
               f'Work out the circuit pressure drop at design flow, decide the valve drop from N (for N = 0.5 it equals the circuit drop), then use Kv = Q ÷ √Δp with Q in m³/h and Δp in bar. For {Qv} m³/h against a {dp_circ*100:.0f} kPa circuit that is Kv {Kv_ideal:.2f}; pick the nearest standard size and recheck N, here {N63:.2f} with Kv 6.3.'),
              ('Why does valve authority get worse when other zones shut?',
               f'Closing branches raises the differential pressure across the ones still open, and the valve must absorb that rise as well. A valve sized for N = {N63:.2f} at {avail_design*100:.0f} kPa effectively controls with N = {N_eff:.2f} if the branch pressure climbs to {avail_low*100:.0f} kPa.')],
     min_words=800)

# ---------------------------------------------------------------- Weir flow
k = 8 / 15 * 0.585 * math.sqrt(2 * G)
Qdef = k * 1 * 0.150 ** 2.5 * 3600
assert abs(Qdef - 43.35) < 0.01


def vq(h, th=90):
    return k * math.tan(math.radians(th) / 2) * h ** 2.5


def v_head(Q_m3h, th=90):
    return (Q_m3h / 3600 / (k * math.tan(math.radians(th) / 2))) ** 0.4


def r_head(Q_m3h, L=0.5):
    q = Q_m3h / 3600
    h = (q / (1.84 * L)) ** (2 / 3)
    for _ in range(60):
        h = (q / (1.84 * (L - 0.2 * h))) ** (2 / 3)
    return h


hrows = ''
for Qt in (2, 5, 10, 25, 50, 100):
    hrows += f"| {Qt} m³/h | {v_head(Qt,60)*1000:.0f} mm | {v_head(Qt)*1000:.0f} mm | {r_head(Qt)*1000:.0f} mm |\n"
# daily volume from logged heads (90 degree notch)
log = [(6, 0.060), (6, 0.095), (8, 0.120), (4, 0.080)]
vol = sum(hrs * vq(h) * 3600 for hrs, h in log)
avg_h = sum(hrs * h for hrs, h in log) / 24
vol_wrong = vq(avg_h) * 86400
# permit limit check: 30 m3/h maximum, what head?
h30 = v_head(30)

edit('engineering/weir-flow', date=U, before='## Common mistakes',
     body_add=f'''## Head needed for a target flow

Turning the formulas round gives the head that a chosen flow will produce, which is how a weir is sized: pick the notch so the normal flow gives at least 50 mm of head and the peak stays below the plate height. For the V-notch, h = [Q ÷ ((8/15) C<sub>d</sub> √(2g) tan(θ/2))]<sup>0.4</sup>; the rectangular case is solved by iteration because L − 0.2h also depends on h.

| Flow | 60° V-notch | 90° V-notch | Rectangular, 0.5 m crest |
|---|---|---|---|
{hrows}
A 2 m³/h flow gives only {r_head(2)*1000:.0f} mm on the 0.5 m rectangular weir, too little to read reliably, while the 60° notch lifts it to {v_head(2,60)*1000:.0f} mm. A discharge permit capped at 30 m³/h corresponds to a head of {h30*1000:.0f} mm on a 90° notch, a useful alarm setpoint for the level transmitter.

## Second example: daily volume from logged heads

Flow over a 90° notch is logged as four steady periods in one day: 6 h at 60 mm, 6 h at 95 mm, 8 h at 120 mm and 4 h at 80 mm. Converting each head to flow and multiplying by its duration gives **{vol:,.0f} m³** for the day. Averaging the heads first ({avg_h*1000:.1f} mm) and converting once gives {vol_wrong:,.0f} m³, {100*(1-vol_wrong/vol):.1f}% low, because flow rises with h<sup>2.5</sup>. Totalisers must convert every sample to flow before summing.

''',
     faq_add=[('How do I find the head a weir will give at a certain flow?',
               f'Rearrange the weir equation for h. For a 90° V-notch with Cd 0.585, h = [Q ÷ (1.3816 × tan 45°)]^0.4 with Q in m³/s, so 30 m³/h gives about {h30*1000:.0f} mm. For a rectangular weir solve iteratively, since the contraction term depends on h.'),
              ('Can I average the head over a day to get the daily flow?',
               f'No. Flow is proportional to h^2.5, so the flow at the average head is lower than the average flow. In the example on this page averaging the heads under-reads the daily volume by {100*(1-vol_wrong/vol):.1f}%. Convert each reading to flow first, then total.')],
     min_words=800)

# ---------------------------------------------------------------- Residence time
tau0 = 10 / 5
assert tau0 == 2
t90 = tau0 * math.log(10)
t99 = tau0 * math.log(100)
# two tanks in series (5 m3 each), 90% response to a step: solve 1 - e^-x(1+x) = 0.9, x = t/(tau/2)
x = 2.0
for _ in range(100):
    f = 1 - math.exp(-x) * (1 + x) - 0.9
    fp = x * math.exp(-x)
    x -= f / fp
t90_2 = x * tau0 / 2
# contact tank: T10 = BF x tau, required T10 30 min at peak 120 m3/h
T10, Qpk = 30, 120
bf = [('Unbaffled, mixed', 0.1), ('Poor (single inlet baffle)', 0.3), ('Average (some intra basin baffles)', 0.5),
      ('Superior (serpentine baffles)', 0.7), ('Perfect plug flow (pipeline)', 1.0)]
bf_rows = ''
for nm, b in bf:
    tau_need = T10 / b
    bf_rows += f"| {nm} | {b:.1f} | {tau_need:.0f} min | {Qpk*tau_need/60:,.0f} m³ |\n"
V_avg = Qpk * (T10 / 0.5) / 60

edit('engineering/residence-time', date=U, before='## Common mistakes',
     body_add=f'''## How long a change at the inlet takes to show

When the feed composition steps to a new value, a mixed tank's outlet follows 1 − e<sup>−t/τ</sup>. For the 10 m³ tank at 5 m³/h the outlet is 90% of the way to the new value after τ ln 10 = **{t90:.2f} h** and 99% after {t99:.2f} h. Splitting the volume into two 5 m³ tanks in series gives a short initial delay but reaches 90% at {t90_2:.2f} h. These times decide how long to wait before sampling after a recipe change, and how far a buffer tank smooths a spike in an upstream stream.

## Sizing a chlorine contact tank with a baffle factor

Drinking water disinfection rules credit the time by which only 10% of the water has passed, T<sub>10</sub>, not the average. T<sub>10</sub> = baffle factor × τ, with tracer-based factors from the US EPA guidance manual. For a required T<sub>10</sub> of {T10} min at a peak flow of {Qpk} m³/h:

| Tank design | Baffle factor | Residence time needed | Working volume |
|---|---|---|---|
{bf_rows}
An average baffled tank needs {V_avg:,.0f} m³, five times less than a single unbaffled tank. Size on peak hourly flow and the minimum operating level, because both shorten the real contact time.

''',
     faq_add=[('How long does a tank take to respond to a change in feed?',
               f'For a well mixed tank the outlet reaches 63% of a step change after one residence time, 90% after 2.30 τ and 99% after 4.61 τ. A 10 m³ tank with 5 m³/h through it takes {t90:.2f} h to reach 90%.'),
              ('What is T10 and the baffle factor in contact tanks?',
               f'T10 is the time by which 10% of the water has left the tank, found by tracer testing, and the baffle factor is T10 ÷ τ. It ranges from 0.1 for an unbaffled tank to 1.0 for a pipeline, so a tank needing {T10} min of T10 with a factor of 0.5 must have a residence time of {T10/0.5:.0f} min.')],
     min_words=800)

# ---------------------------------------------------------------- Rotameter correction


def cf(r1, r2, rf):
    return math.sqrt((rf - r2) * r1 / ((rf - r1) * r2))


CF0 = cf(998, 800, 8000)
assert abs(CF0 - 1.1326) < 1e-4
# set point from a mass flow target: 600 kg/h of 870 kg/m3 oil, stainless float, water scale
mt, rho_o = 600.0, 870.0
Qa = mt / rho_o / 60 * 1000          # L/min actual
CFo = cf(998, rho_o, 8000)
Qs = Qa / CFo
# range check: 2 to 20 L/min water scale
lo, hi = 2, 20
# float force balance: weight - buoyancy for a 5 cm3 stainless float in water and in 800 kg/m3 liquid
Vf = 5e-6
Fw = Vf * (8000 - 998) * G
Fl = Vf * (8000 - 800) * G

edit('engineering/rotameter-correction', date=U, before='## Reading a rotameter in practice',
     body_add=f'''## Why the square root appears

At a steady reading the float hangs where the fluid drag balances its weight less buoyancy, V<sub>f</sub> (ρ<sub>f</sub> − ρ) g. Drag at a given annulus opening scales with ρ v², so the velocity, and with it the flow, scales with √[(ρ<sub>f</sub> − ρ) ÷ ρ]. The correction factor is just this term for the actual liquid divided by the term for the calibration fluid. A 5 cm³ stainless float carries a net downward force of {Fw*1000:.1f} mN in water and {Fl*1000:.1f} mN in the 800 kg/m³ liquid; the lighter liquid also has less density to push with, so it must flow faster to hold the same float height.

## Second example: setting a mass flow target

A dosing line needs {mt:.0f} kg/h of an oil at {rho_o:.0f} kg/m³ through a water scaled meter with a stainless float:

- Actual volume flow = {mt:.0f} ÷ {rho_o:.0f} = {mt/rho_o:.4f} m³/h = **{Qa:.2f} L/min**
- Correction factor = √[(8000 − {rho_o:.0f}) × 998 ÷ ((8000 − 998) × {rho_o:.0f})] = **{CFo:.4f}**
- Set the float at {Qa:.2f} ÷ {CFo:.4f} = **{Qs:.2f} L/min** on the water scale

The corrected range also moves. A {lo} to {hi} L/min water scale now spans {lo*CFo:.2f} to {hi*CFo:.2f} L/min of oil, so check the maximum process flow against the corrected top of scale, not the printed one.

''',
     faq_add=[('How do I set a rotameter for a mass flow in kg/h?',
               f'Divide the mass flow by the liquid density to get the actual volume flow, then divide by the correction factor to get the scale reading. For {mt:.0f} kg/h of {rho_o:.0f} kg/m³ oil on a water scaled meter with a stainless float, that is {Qa:.2f} L/min actual and {Qs:.2f} L/min on the scale.'),
              ('Does the correction change the full scale range of the meter?',
               f'Yes, every point on the scale is multiplied by the same factor. A 2 to 20 L/min water scale reads {lo*CFo:.2f} to {hi*CFo:.2f} L/min on an {rho_o:.0f} kg/m³ oil with a stainless float.')],
     min_words=800)

# ---------------------------------------------------------------- Hazen-Williams


def hw(Q_m3h, d_m, L=100, C=130):
    return 10.67 * L * (Q_m3h / 3600) ** 1.852 / (C ** 1.852 * d_m ** 4.8704)


assert abs(hw(50, 0.1) - 3.498) < 1e-3


def d_for(Q_m3h, L, hf, C=130):
    return (10.67 * L * (Q_m3h / 3600) ** 1.852 / (C ** 1.852 * hf)) ** (1 / 4.8704)


def q_for(d_m, S, C=130):
    # flow (m3/h) giving head loss S metres per metre
    return (S * C ** 1.852 * d_m ** 4.8704 / 10.67) ** (1 / 1.852) * 3600


Ls, hlim = 500, 5.0
dmin = d_for(50, Ls, hlim)
d_next = 0.150
hf_next = hw(50, d_next, Ls)
d_prev = 0.125
hf_prev = hw(50, d_prev, Ls)
assert hf_prev > hlim > hf_next
hf_100 = hw(50, 0.100, Ls)
cap_rows = ''
for dm in (50, 80, 100, 150, 200, 300):
    q1 = q_for(dm / 1000, 0.01)
    q2 = q_for(dm / 1000, 0.01, 100)
    v = q1 / 3600 / (math.pi * (dm / 1000) ** 2 / 4)
    cap_rows += f"| {dm} mm | {q1:,.1f} m³/h | {v:.2f} m/s | {q2:,.1f} m³/h |\n"
# exponent check: ratio of flows for C 100 vs 130 at same gradient
ratio_c = 100 / 130

edit('engineering/hazen-williams', date=U, before='## The US customary form',
     body_add=f'''## Sizing a pipe for an allowed head loss

Solving the equation for diameter gives d = [10.67 L Q<sup>1.852</sup> ÷ (C<sup>1.852</sup> h<sub>f</sub>)]<sup>1/4.87</sup>. Suppose 50 m³/h must travel {Ls} m with no more than {hlim:.0f} m of friction loss, C = 130:

- Minimum bore d = **{dmin*1000:.1f} mm**
- A 100 mm bore would lose {hf_100:.2f} m, more than three times the limit
- A 125 mm bore loses {hf_prev:.2f} m, still just over
- A 150 mm bore loses **{hf_next:.2f} m**, so it is the size to choose

## Carrying capacity at 1 m per 100 m

Many water mains are laid out for a friction gradient near 1 m of head per 100 m. Solving for Q at that gradient gives each bore's capacity:

| Pipe ID | Flow at C = 130 | Velocity | Flow at C = 100 |
|---|---|---|---|
{cap_rows}
At a fixed gradient flow is proportional to C, so an old main at C = 100 carries {ratio_c*100:.0f}% of the flow it did when new, whatever its size.

''',
     faq_add=[('How do I size a water pipe for a maximum head loss?',
               f'Rearrange Hazen-Williams for the diameter: d = [10.67 L Q^1.852 ÷ (C^1.852 hf)]^(1/4.87) in SI units, then pick the next standard bore above the result. For 50 m³/h over {Ls} m with {hlim:.0f} m allowed at C = 130 the minimum is {dmin*1000:.1f} mm, so a 150 mm bore ({hf_next:.2f} m loss) is chosen.'),
              ('How much flow can a pipe carry at a given friction gradient?',
               f'Solve for Q: Q = [S C^1.852 d^4.87 ÷ 10.67]^(1/1.852), where S is head loss per metre. At 1 m per 100 m and C = 130 a 100 mm bore carries about {q_for(0.1,0.01):.1f} m³/h and a 150 mm bore about {q_for(0.15,0.01):.1f} m³/h.')],
     min_words=800)

print('done', len(__import__('inplace').DONE))

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-26), section c3: heat-sink, calibration-error, fan-affinity-laws, spherical-tank-volume, weld-size.
Every number is computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-26'
MINUS = chr(0x2212)


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Heat sink
P, Tj, Ta, Rjc, Rcs = 10, 125, 40, 1.5, 0.5
Rsa = (Tj - Ta) / P - Rjc - Rcs
assert abs(Rsa - 6.5) < 1e-9
# linear regulator example
Vin, Vout, I = 12.0, 5.0, 0.8
Pr = (Vin - Vout) * I
Ta_r, Rjc_r, Rcs_r, Rja_r = 50, 3.0, 0.5, 60
Rt_r = (Tj - Ta_r) / Pr
Rsa_r = Rt_r - Rjc_r - Rcs_r
Tj_bare = Ta_r + Pr * Rja_r
P_bare = (Tj - Ta_r) / Rja_r
I_bare = P_bare / (Vin - Vout)
# 9 V input instead of 12 V
Pr9 = (9.0 - Vout) * I
Rsa_r9 = (Tj - Ta_r) / Pr9 - Rjc_r - Rcs_r
# two MOSFETs sharing one sink, 10 W each
n2 = 2
Rsa_shared = (Tj - Ta - P * (Rjc + Rcs)) / (n2 * P)
Ts_shared = Ta + n2 * P * Rsa_shared
assert abs(Ts_shared + P * (Rjc + Rcs) - Tj) < 1e-9

edit('electronics/heat-sink', date=U,
     before='## Measuring temperatures in practice',
     body_add=f'''## Second example: a linear regulator

Linear regulators waste the whole voltage drop as heat. A 5 V regulator fed from {Vin:.0f} V and supplying {I} A dissipates ({Vin:.0f} {MINUS} {Vout:.0f}) × {I} = **{Pr:.1f} W**. With a TO-220 package of R<sub>θjc</sub> {Rjc_r:.0f} °C/W, a {Rcs_r} °C/W pad, {Ta_r} °C inside the box and the same 125 °C target:

- Total allowed = ({Tj} {MINUS} {Ta_r}) ÷ {Pr:.1f} = {Rt_r:.2f} °C/W
- R<sub>θsa</sub> ≤ {Rt_r:.2f} {MINUS} {Rjc_r:.0f} {MINUS} {Rcs_r} = **{Rsa_r:.2f} °C/W**, a medium extruded sink
- With no sink at all (R<sub>θja</sub> about {Rja_r} °C/W) the junction would head for {Ta_r} + {Pr:.1f} × {Rja_r} = {Tj_bare:.0f} °C; the bare package can only shed {P_bare:.2f} W, which limits the current to about {I_bare*1000:.0f} mA

Lowering the input to 9 V cuts the loss to {Pr9:.1f} W and relaxes the sink to {Rsa_r9:.2f} °C/W, which is often cheaper than a bigger heat sink.

## Several devices on one heat sink

When two of the default 10 W MOSFETs share one sink, the sink carries {n2*P} W while each junction still sits {P * (Rjc + Rcs):.0f} °C above it through its own R<sub>θjc</sub> + R<sub>θcs</sub>. The limit becomes R<sub>θsa</sub> ≤ ({Tj} {MINUS} {Ta} {MINUS} {P} × {Rjc + Rcs:.0f}) ÷ {n2*P} = **{Rsa_shared:.2f} °C/W**, half of what a separate sink for each device could be, with the sink running at {Ts_shared:.0f} °C.

''', min_words=800,
     faq_add=[('How do I size a heat sink shared by two or more devices?',
               f'Subtract each device\'s own rise P × (Rθjc + Rθcs) from Tj − Ta, then divide by the total power into the sink. Two 10 W MOSFETs with 2 °C/W each, 40 °C ambient and a 125 °C limit need Rθsa ≤ (125 − 40 − 20) ÷ 20 = {Rsa_shared:.2f} °C/W.'.replace(chr(0x2212), MINUS)),
              ('Why does a linear regulator need such a large heat sink?',
               f'It dissipates the full input to output voltage difference times the load current. Dropping 12 V to 5 V at 0.8 A wastes {Pr:.1f} W, so with 50 °C ambient the sink must be {Rsa_r:.2f} °C/W or better; a switching regulator or a lower input voltage cuts the heat.')])

# ---------------------------------------------------------------- Calibration error
Lo, Hi, X, Y, Tol = 4, 20, 12, 12.05, 0.0025
Ps = (Y - X) / (Hi - Lo)
assert abs(Ps - 0.003125) < 1e-12
# temperature transmitter example
tLo, tHi, tX, tY, tTol = 0.0, 200.0, 150.0, 150.6, 0.005
tErr = tY - tX
tPs = tErr / (tHi - tLo)
tPr = tErr / tX
tU = abs(tPs) / tTol
# five-point as-found run
xs = [4, 8, 12, 16, 20]
ys = [4.008, 8.017, 12.027, 16.036, 20.046]
n = len(xs)
mx, my = sum(xs) / n, sum(ys) / n
b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
a0 = my - b * mx
zero_err = a0 + b * 4 - 4
span_err = (a0 + b * 20) - (a0 + b * 4) - 16
rows = ''
for x, y in zip(xs, ys):
    e = y - x
    ps = e / 16
    rows += f"| {100*(x-4)/16:.0f}% | {x:.3f} mA | {y:.3f} mA | +{e:.3f} mA | {ps*100:.4f}% | {abs(ps)/Tol*100:.0f}% |\n"
fails = sum(1 for x, y in zip(xs, ys) if abs((y - x) / 16) / Tol > 1)
# calibrator uncertainty and TUR at 12 mA
cal_unc = 0.0001 * 12 + 0.002
tol_mA = Tol * 16
TUR = tol_mA / cal_unc

edit('engineering/calibration-error', date=U,
     before='## Calibration in practice',
     body_add=f'''## Second example: a temperature transmitter

The calculator works in any unit. A temperature transmitter ranged {tLo:.0f} to {tHi:.0f} °C is checked in a dry block at {tX:.0f} °C and reads {tY} °C, with a tolerance of ±{tTol*100:.1f}% of span:

- Error = {tY} {MINUS} {tX:.0f} = **+{tErr:.1f} °C**
- % of span = {tErr:.1f} ÷ {tHi-tLo:.0f} = **{tPs*100:.2f}%**, % of reading = {tErr:.1f} ÷ {tX:.0f} = {tPr*100:.2f}%
- Tolerance used = {tPs*100:.2f} ÷ {tTol*100:.1f} = **{tU*100:.0f}%**, so this point passes as found

## Reading a five-point run: zero error or span error?

A single point cannot tell you what to adjust. This as-found run on a 4 to 20 mA transmitter with ±0.25% of span tolerance shows an error that grows up the scale:

| Input | Expected | Measured | Error | % of span | Tolerance used |
|---|---|---|---|---|---|
{rows}
A straight-line fit through the five points gives a zero error of **+{zero_err:.4f} mA** at 4 mA and a span error of **+{span_err:.4f} mA** over the 16 mA span ({span_err/16*100:.3f}% of span). {fails} point{'s' if fails != 1 else ''} fail{'' if fails != 1 else 's'}, and the pattern says the span adjustment is the main fix, with a small zero trim. An error that is the same at every point would be a pure zero shift.

## Is the calibrator good enough?

A typical loop calibrator specified at ±(0.01% of reading + 2 µA) has an uncertainty of 0.0001 × 12 + 0.002 = **{cal_unc*1000:.1f} µA** at 12 mA. Against the ±{tol_mA*1000:.0f} µA tolerance that is a test uncertainty ratio of {tol_mA*1000:.0f} ÷ {cal_unc*1000:.1f} = **{TUR:.1f}:1**, comfortably above the 4:1 rule.

''', min_words=800,
     faq_add=[('How do I tell a zero error from a span error?',
               f'Look at the error across several test points. A zero error is the same at every point; a span error grows in proportion to the input. In a run reading 4.008, 8.017, 12.027, 16.036 and 20.046 mA, the fitted zero error is +{zero_err:.4f} mA and the span error +{span_err:.4f} mA, so the span needs adjusting.'),
              ('How do I calculate the test uncertainty ratio?',
               f'Divide the tolerance by the reference uncertainty at the same point. A ±0.25% of span tolerance on 4 to 20 mA is ±40 µA; a calibrator good to ±(0.01% of reading + 2 µA) is ±{cal_unc*1000:.1f} µA at 12 mA, so TUR = {TUR:.1f}:1.')])

# ---------------------------------------------------------------- Fan affinity laws
Q, dp, eta, N1, N2 = 10000 / 3600, 1000, 0.70, 1450, 1160
Pa = Q * dp
Ps = Pa / eta
assert abs(Ps / 1000 - 3.968) < 1e-3
# speeding up for more air
Qt = 12000
N_up = N1 * Qt / 10000
r_up = N_up / N1
dp_up = dp * r_up ** 2
Ps_up = Ps * r_up ** 3
tip_old = math.pi * 0.63 * N1 / 60
# impeller diameter change at constant speed
D1, D2 = 630, 560
rd = D2 / D1
Qd, pd, Pd = rd ** 3, rd ** 2, rd ** 5
# imperial example
cfm, inwg, eta_i = 5000, 2.0, 0.65
bhp = cfm * inwg / (6356 * eta_i)
Q_si = cfm * 0.3048 ** 3 / 60
dp_si = inwg * 249.0889
bhp_check = Q_si * dp_si / eta_i / 745.69987
assert abs(bhp - bhp_check) / bhp < 5e-3

edit('engineering/fan-affinity-laws', date=U,
     before='## Common mistakes',
     body_add=f'''## Speeding a fan up for more airflow

The laws work just as well upwards, and the cube term is what catches people out. To raise the default fan from 10,000 to {Qt:,} m³/h the speed must rise to 1,450 × {Qt:,} ÷ 10,000 = **{N_up:,.0f} rpm**. Pressure then climbs to {dp_up:,.0f} Pa and shaft power to 3.968 × {r_up:.1f}³ = **{Ps_up/1000:.2f} kW**, {Ps_up/Ps:.2f} times the original, so a 20% airflow increase usually means a bigger motor. Check the fan's maximum rated speed and the belt or pulley ratio before relying on a VFD to overspeed it.

## Changing the impeller diameter

For geometrically similar fans at the same speed, flow scales with the diameter cubed, pressure with its square and power with its fifth power. Trimming from {D1} mm to {D2} mm (ratio {rd:.4f}) gives:

| Quantity | Law | Ratio | Default fan |
|---|---|---|---|
| Airflow | (D₂/D₁)³ | {Qd:.3f} | {10000*Qd:,.0f} m³/h |
| Pressure | (D₂/D₁)² | {pd:.3f} | {dp*pd:,.0f} Pa |
| Shaft power | (D₂/D₁)⁵ | {Pd:.3f} | {Ps*Pd/1000:.2f} kW |

The diameter laws are less exact than the speed laws because a smaller impeller in the same casing has larger clearances.

## Imperial example

A fan moving {cfm:,} CFM against {inwg:.0f} in. w.g. total pressure at {eta_i*100:.0f}% efficiency needs {cfm:,} × {inwg:.0f} ÷ (6,356 × {eta_i}) = **{bhp:.2f} bhp**. In SI that is {Q_si:.3f} m³/s × {dp_si:.0f} Pa ÷ {eta_i} = {Q_si*dp_si/eta_i/1000:.2f} kW, the same answer within rounding of the 6,356 constant.

''', min_words=800,
     faq_add=[('How much more power does a fan need if I speed it up 20%?',
               f'Power rises with the cube of speed, so 1.2³ = {1.2**3:.3f} times. The default fan goes from 3.97 kW to {Ps_up/1000:.2f} kW to deliver {Qt:,} m³/h, while pressure rises 44%.'),
              ('What happens to fan performance with a smaller impeller?',
               f'At the same speed, flow falls with the diameter ratio cubed, pressure with its square and power with its fifth power. Going from {D1} to {D2} mm cuts flow to {Qd*100:.1f}%, pressure to {pd*100:.1f}% and power to {Pd*100:.1f}% of the original.')])

# ---------------------------------------------------------------- Spherical tank
D, h = 10.0, 4.0
R = D / 2


def capV(hh, DD=D):
    return math.pi * hh ** 2 * (1.5 * DD - hh) / 3


V = capV(h)
Vt = math.pi * D ** 3 / 6
assert abs(V - 184.31) < 0.01


def level_for(frac):
    lo, hi = 0.0, D
    for _ in range(100):
        mid = (lo + hi) / 2
        if capV(mid) / Vt < frac:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


lv_rows = ''
for fr in (0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95):
    hl = level_for(fr)
    lv_rows += f"| {fr*100:.0f}% | {hl/D*100:.1f}% of D | {hl:.2f} m |\n"
# level sensitivity: surface area at level
area_rows = ''
for hh in (0.5, 2.0, 4.0, 5.0, 8.0, 9.5):
    A = math.pi * hh * (D - hh)
    area_rows += f"| {hh:.1f} m | {A:.1f} m² | {A:.1f} L |\n"
A4 = math.pi * h * (D - h)
A5 = math.pi * R ** 2
# radar accuracy 3 mm at 4 m with propane 500 kg/m3
acc = 0.003
dm = A4 * acc * 500
# level for 300 m3
h300 = level_for(300 / Vt)

edit('engineering/spherical-tank-volume', date=U,
     before='## Common mistakes',
     body_add=f'''## Level for a chosen volume

The fraction of the diameter needed for a given percent of volume is the same for every sphere, so this table can be scaled to any size (the last column is for the 10 m example):

| Volume filled | Level | Level in a 10 m sphere |
|---|---|---|
{lv_rows}
For example, to hold 300 m³ in the 10 m sphere the level must reach **{h300:.2f} m**. The calculator solves the same cubic when you clear the level and enter a volume.

## How much volume one millimetre of level represents

The liquid surface is a circle of area π h (D {MINUS} h), so a small level change Δh changes the volume by that area times Δh. It is largest at the equator ({A5:.1f} m² for a 10 m sphere) and shrinks to nothing at the top and bottom:

| Level | Surface area | Volume per mm of level |
|---|---|---|
{area_rows}
At the 4 m example level a radar gauge with ±{acc*1000:.0f} mm accuracy leaves an uncertainty of {A4:.1f} × {acc} = {A4*acc*1000:.0f} L, or about {dm:.0f} kg of propane. Near the top the same gauge error is worth far less volume, which helps when setting fill limits.

''', min_words=800,
     faq_add=[('How much volume does one millimetre of level represent in a sphere?',
               f'It equals the liquid surface area π h (D − h) times 1 mm. In a 10 m sphere that is {A4:.1f} L at 4 m of level, {A5:.1f} L at the 5 m equator and only {math.pi*9.5*0.5:.1f} L at 9.5 m.'.replace(chr(0x2212), MINUS)),
              ('What level gives 25% of the volume in a spherical tank?',
               f'{level_for(0.25)/D*100:.1f}% of the inside diameter for any sphere, which is {level_for(0.25):.2f} m in a 10 m sphere. 75% of the volume is reached at {level_for(0.75)/D*100:.1f}% of the diameter.')])

# ---------------------------------------------------------------- Weld size
s, L, F, ta = 6.0, 100.0, 50.0, 145.0
a = 0.70710678 * s
Fmax = ta * a * L / 1000
assert abs(Fmax - 61.52) < 0.01
# AWS / AISC directional strength factor
dir_rows = ''
for th in (0, 30, 45, 60, 90):
    k = 1 + 0.5 * math.sin(math.radians(th)) ** 1.5
    dir_rows += f"| {th}° | {k:.3f} | {Fmax*k:.1f} kN |\n"
k90 = 1.5
# imperial rule of thumb
q16 = 21 * 0.70710678 / 16
s_in, L_in = 0.25, 4.0
Fi = 21 * 0.70710678 * s_in * L_in
# weld metal per metre
rho = 7850
mass_rows = ''
for leg in (4, 6, 8, 10, 12):
    A_mm2 = leg ** 2 / 2
    mass = A_mm2 * 1e-6 * rho
    mass_rows += f"| {leg} mm | {A_mm2:.0f} mm² | {mass:.3f} kg/m |\n"
r_6_12 = (12 / 6) ** 2

edit('engineering/weld-size', date=U,
     before='## Inspection and practice',
     body_add=f'''## Transverse welds are stronger

AWS D1.1 and AISC 360 allow the strength of a linear fillet weld to rise with the angle θ between the load and the weld axis, by the factor 1 + 0.5 sin<sup>1.5</sup> θ. For the 6 mm × 100 mm default weld (61.5 kN when loaded along its length):

| Load angle θ | Factor | Capacity |
|---|---|---|
{dir_rows}
A weld loaded straight across its length can carry {k90:.1f} times the longitudinal value. The increase applies only to welds loaded in plane through their centroid; when longitudinal and transverse welds share a load, the codes limit how much of the bonus may be used.

## Imperial rule of thumb

With E70 electrodes, 0.30 × 70 ksi = 21 ksi on the throat gives 21 × 0.7071 ÷ 16 = **{q16:.3f} kips per inch for each sixteenth of an inch of leg**. A 1/4 in fillet is four sixteenths, so 4 in of it carries 4 × 4 × {q16:.3f} = {Fi:.2f} kips, the same as 21 × 0.177 × 4.

## Weld metal per metre

The cross section of an equal-leg fillet is s² ÷ 2, so deposited steel (7,850 kg/m³, no reinforcement) per metre is:

| Leg size | Section area | Weld metal |
|---|---|---|
{mass_rows}
Doubling the leg from 6 to 12 mm doubles the capacity but needs {r_6_12:.0f} times the weld metal and welding time, so two smaller runs on both sides of a joint are often cheaper than one large fillet.

''', min_words=800,
     faq_add=[('Does a transversely loaded fillet weld carry more load?',
               f'Yes. AWS D1.1 and AISC 360 multiply the strength by 1 + 0.5 sin^1.5 θ, so a weld loaded at 90° to its axis carries 1.5 times its longitudinal capacity: {Fmax*1.5:.1f} kN instead of {Fmax:.1f} kN for a 6 mm fillet 100 mm long at 145 MPa.'),
              ('How much weld metal does a fillet weld need per metre?',
               f'The section area is leg² ÷ 2, so a 6 mm fillet holds 18 mm² and about {18*1e-6*rho:.3f} kg of steel per metre, before reinforcement and spatter. A 10 mm fillet needs {50*1e-6*rho:.3f} kg/m.')])

print('done', len(__import__('inplace').DONE))

# ======================================================================= SECTION _expand_c4.py
"""Expand (2026-11-26), section c4: low-flow-cutoff, transformer-current, ziegler-nichols-pid-tuning,
transistor-base-resistor, pump-affinity-laws. Every number is computed here. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-26'
G = 9.80665
MINUS = chr(0x2212)


def c(x, d=0):
    return f"{x:,.{d}f}"


# ================================================================ Low flow cutoff
q, Qmax, DPmax = 0.05, 100.0, 250.0
x = q ** 2
assert abs(x * DPmax - 0.625) < 1e-12 and abs(1 / (2 * q) - 10) < 1e-12
# transmitter accuracy versus cutoff DP for different calibrated spans
acc = 0.00065  # 0.065% of calibrated span, a common smart DP transmitter class
span_rows = ''
for span in (62.5, 250, 1000, 2500):
    row = f"| {span:g} mbar | {acc*span:.3f} mbar |"
    for qq in (0.03, 0.05, 0.10):
        dp = qq ** 2 * span
        row += f" {dp:.3f} mbar ({dp/(acc*span):.1f}×) |"
    span_rows += row + '\n'
# linear section below a 5% break point
q0 = 0.05
dp_test = 0.001
lin = dp_test / q0          # slope 1/q0 on DP fraction, meets the root curve at q0
root = math.sqrt(dp_test)
assert abs(q0 ** 2 / q0 - q0) < 1e-12
# totalizer loss: 4 m3/h for 6 h per day below the 5 m3/h cutoff
q_low, h_low = 4.0, 6.0
lost_day = q_low * h_low
lost_year = lost_day * 365
# hysteresis band in DP terms: 5% out, 6% in
dp_out, dp_in = 0.05 ** 2 * DPmax, 0.06 ** 2 * DPmax

edit('engineering/low-flow-cutoff', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Is the cutoff above the transmitter's own error?

A cutoff only works if the DP it corresponds to is clearly larger than what the transmitter can resolve. Taking a reference accuracy of ±0.065% of calibrated span, the table compares the cutoff DP with that error band (the multiple in brackets) for four spans:

| DP span | Error band | 3% flow | 5% flow | 10% flow |
|---|---|---|---|---|
{span_rows}
The ratio does not depend on the span, because both the cutoff DP and the error scale with it: a 3% cutoff sits only {0.03**2/acc:.1f} times above the error band, while 5% gives {0.05**2/acc:.1f} times and 10% gives {0.10**2/acc:.1f} times. Zero drift with static pressure and ambient temperature adds to the reference figure in service, which is why settings below about 5% of flow often chatter.

## Linear section instead of a hard cutoff

With a linear section the output follows a straight line from zero up to a break point q₀, where it joins the root curve. The line has slope 1 ÷ q₀ on the DP fraction, so with q₀ = 5% a DP of 0.1% of span reads 0.001 ÷ 0.05 = **{lin*100:.1f}%** flow instead of √0.001 = {root*100:.2f}% on the pure root curve. The noise gain below the break is a constant {1/q0:.0f}, twice the root curve's gain at the break but far below the {1/(2*0.01):.0f} it reaches at 1% flow, and there is no step from zero.

## What the cutoff costs the totalizer

Suppose a line runs at {q_low:g} m³/h for {h_low:g} hours each night, just under the {q*Qmax:g} m³/h cutoff in the example. The flow reads zero, so the totalizer misses {lost_day:g} m³ a day, about {c(lost_year)} m³ a year. If the plant needs that flow measured, a smaller orifice, a second low range transmitter or a meter with wider turndown is the fix, not a lower cutoff. When hysteresis is used, the 5% cut out and 6% cut in points correspond to {dp_out:.3f} mbar and {dp_in:.3f} mbar on the 250 mbar span.
''',
     faq_add=[('What is a linear section below the cutoff?',
               f'Instead of forcing zero, the transmitter outputs flow proportional to DP below a break point and switches to the square root above it. With a 5% break, 0.1% DP reads {lin*100:.1f}% flow rather than {root*100:.2f}%, and the noise gain stays at a constant {1/q0:.0f} instead of climbing without limit near zero.'),
              ('How much flow does the totalizer lose below the cutoff?',
               f'Everything below the cutoff is counted as zero. A line running at {q_low:g} m³/h for {h_low:g} hours a day under a {q*Qmax:g} m³/h cutoff loses {lost_day:g} m³ a day, about {c(lost_year)} m³ a year.')])

# ================================================================ Transformer current
S, ph, Vp, Vs = 500.0, math.sqrt(3), 11000.0, 433.0
Ip = S * 1000 / (ph * Vp)
Is = S * 1000 / (ph * Vs)
assert abs(Ip - 26.24) < 0.005 and abs(Is - 666.7) < 0.05
# Dyn11: HV delta winding, LV star winding
Iw_hv = Ip / math.sqrt(3)
Vph_lv = Vs / math.sqrt(3)
# unbalanced measured LV currents
Ia, Ib, Ic_ = 520.0, 470.0, 430.0
Iavg = (Ia + Ib + Ic_) / 3
S_meas = math.sqrt(3) * Vs * Iavg / 1000
load_max = Ia / Is
# single phase pole mounted 25 kVA, 11 kV line to line primary, 240 V secondary
s1 = 25.0
Ip1 = s1 * 1000 / 11000
Is1 = s1 * 1000 / 240
# other voltages table
volts = [(400, '400 V'), (690, '690 V'), (3300, '3.3 kV'), (6600, '6.6 kV'), (33000, '33 kV')]
vrows = ''
for kva in (250, 500, 1000, 2000, 5000):
    vrows += f"| {kva:,} kVA |" + ''.join(f" {kva*1000/(math.sqrt(3)*v):,.1f} A |" for v, _ in volts) + '\n'

edit('electrical/transformer-current', date=U, before='## Common mistakes', min_words=800,
     description='Calculate primary and secondary full-load current of single-phase and three-phase transformers from the kVA rating and line voltages, with sizing notes.',
     body_add=f'''## Winding currents in a Dyn11 transformer

The calculator gives line currents. Inside the windings they differ with the connection. In the common Dyn11 distribution unit the 11 kV side is delta, so each HV winding carries {Ip:.2f} ÷ √3 = **{Iw_hv:.2f} A** while the line carries {Ip:.2f} A. The 433 V side is star, so the winding current equals the line current of {Is:.1f} A, and each winding sees the phase voltage 433 ÷ √3 = {Vph_lv:.0f} V. Winding temperature indicators and internal CTs are rated on these winding values.

## Loading from unbalanced phase currents

Real loads are rarely balanced. If the LV phases read {Ia:.0f} A, {Ib:.0f} A and {Ic_:.0f} A, the supplied power is about √3 × 433 × {Iavg:.1f} A = **{S_meas:.0f} kVA** using the average current, but the worst phase is at {Ia:.0f} ÷ {Is:.1f} = **{load_max*100:.0f}%** of its rating. Winding heating follows the most loaded phase, so judge thermal loading by the highest current and use the average only for energy and kVA.

## A single-phase unit on a three-phase line

A {s1:g} kVA pole mounted transformer connected between two 11 kV lines has an 11 kV primary and a 240 V secondary. It draws {s1*1000:,.0f} ÷ 11,000 = **{Ip1:.2f} A** from the line and delivers up to {s1*1000:,.0f} ÷ 240 = **{Is1:.1f} A**. Set the calculator to single phase and enter the voltage actually across the winding.

## Full-load current at other line voltages (three-phase)

| Rating |''' + ''.join(f" {lab} |" for _, lab in volts) + '''
|---|---|---|---|---|---|
''' + vrows,
     faq_add=[('What current flows inside a delta winding?',
               f'The line current divided by √3. For a 500 kVA, 11 kV delta primary the line current is {Ip:.2f} A and each winding carries {Iw_hv:.2f} A.'),
              ('How do I find the kVA being supplied when phase currents are unequal?',
               f'Multiply √3 by the line voltage and the average of the three currents. Readings of 520, 470 and 430 A at 433 V give about {S_meas:.0f} kVA, but the 520 A phase sets the heating at {load_max*100:.0f}% of rating.')])

# ================================================================ Ziegler-Nichols
Ku, Pu = 2.0, 60.0
assert 0.6 * Ku == 1.2 and Pu / 2 == 30 and Pu / 8 == 7.5


def ultimate(K, tau, theta):
    """Phase crossover of a FOPDT process: atan(w tau) + w theta = pi."""
    lo, hi = 1e-9, math.pi / theta
    for _ in range(200):
        w = (lo + hi) / 2
        if math.atan(w * tau) + w * theta < math.pi:
            lo = w
        else:
            hi = w
    w = (lo + hi) / 2
    return math.sqrt(1 + (w * tau) ** 2) / K, 2 * math.pi / w


Kp_, tau_, th_ = 1.5, 120.0, 20.0
Ku_f, Pu_f = ultimate(Kp_, tau_, th_)
# ratio table for K = 1
fr = ''
for r in (0.05, 0.1, 0.2, 0.5, 1.0, 2.0):
    ku1, pu1 = ultimate(1.0, 1.0, r)
    fr += f"| {r:g} | {ku1:.2f} | {pu1/r:.2f} |\n"
# slow temperature loop, minutes
Ku_t, Pu_t = 8.0, 12.0
Kc_t, Ti_t, Td_t = 0.6 * Ku_t, Pu_t / 2, Pu_t / 8

edit('engineering/ziegler-nichols-pid-tuning', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Estimating Ku and Pu from a step test model

If a step test has already given a first order plus dead time model (gain K, time constant τ, dead time θ), the ultimate values can be calculated instead of measured. The loop is at the stability limit at the frequency ω where the process phase lag reaches 180°, atan(ωτ) + ωθ = π, and the ultimate gain is K<sub>u</sub> = √(1 + (ωτ)²) ÷ K. For K = {Kp_:g}, τ = {tau_:.0f} s and θ = {th_:.0f} s, solving numerically gives **K<sub>u</sub> = {Ku_f:.2f}** and **P<sub>u</sub> = {Pu_f:.1f} s**, so the classic PID settings would be K<sub>c</sub> = {0.6*Ku_f:.2f}, T<sub>i</sub> = {Pu_f/2:.1f} s and T<sub>d</sub> = {Pu_f/8:.1f} s.

How the ultimate values depend on the dead time ratio (for a process gain of 1; divide K<sub>u</sub> by the real gain):

| θ ÷ τ | K<sub>u</sub> × K | P<sub>u</sub> ÷ θ |
|---|---|---|
{fr}
Lag dominant loops (small θ ÷ τ) tolerate high gain and cycle at about four dead times or less; in dead time dominant loops K<sub>u</sub> × K falls towards 1 and P<sub>u</sub> towards 2θ, which is where Ziegler-Nichols settings are least robust.

## A slow temperature loop in minutes

A jacketed reactor temperature loop cycles steadily at K<sub>u</sub> = {Ku_t:g} with P<sub>u</sub> = {Pu_t:g} min. The classic PID settings are K<sub>c</sub> = **{Kc_t:.1f}** (PB {100/Kc_t:.1f}%), T<sub>i</sub> = **{Ti_t:g} min** ({1/Ti_t:.3f} repeats per minute) and T<sub>d</sub> = **{Td_t:g} min**. With a period this long, wait several cycles before reading P<sub>u</sub>, because a single peak to peak time can be distorted by load changes.
''',
     faq_add=[('Can I get Ku and Pu without an oscillation test?',
               f'Yes, from a step test model. Solve atan(ωτ) + ωθ = π for ω, then Ku = √(1 + (ωτ)²) ÷ K and Pu = 2π ÷ ω. A process with K = {Kp_:g}, τ = {tau_:.0f} s and θ = {th_:.0f} s gives Ku = {Ku_f:.2f} and Pu = {Pu_f:.1f} s.')])

# ================================================================ Transistor base resistor
Vin, Vbe, Ic, hfe, k = 5.0, 0.7, 0.100, 100.0, 5.0
Ib = Ic / hfe * k
Rb = (Vin - Vbe) / Ib
assert abs(Ib - 0.005) < 1e-12 and abs(Rb - 860) < 1e-9
# worst case with 820 ohm 5%, pin high 4.5 to 5.0 V, Vbe 0.6 to 0.85 V
R = 820.0
Ib_min = (4.5 - 0.85) / (R * 1.05)
Ib_max = (5.0 - 0.6) / (R * 0.95)
fb_worst = Ic / Ib_min
corner_rows = ''
for vpin in (4.5, 5.0):
    for vbe in (0.6, 0.85):
        for tol in (0.95, 1.05):
            ib = (vpin - vbe) / (R * tol)
            corner_rows += f"| {vpin:.1f} V | {vbe:.2f} V | {R*tol:.0f} Ω | {ib*1000:.2f} mA | {Ic/ib:.1f} |\n"
# PNP high side, 12 V, 200 mA, driven by NPN level shifter with Vce(sat) 0.2 V
Vcc, Ic2, h2, k2, vsat = 12.0, 0.200, 100.0, 5.0, 0.2
Ib2 = Ic2 / h2 * k2
Rb2 = (Vcc - Vbe - vsat) / Ib2
P2 = (Vcc - Vbe - vsat) * Ib2
# NPN driver for that base current from 3.3 V, hFE 100, overdrive 5
Ib3 = Ib2 / 100 * 5
Rb3 = (3.3 - 0.7) / Ib3

edit('electronics/transistor-base-resistor', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Worst case check of the 820 Ω choice

The design should still saturate when every tolerance goes the wrong way. A loaded 5 V pin may only reach 4.5 V, V<sub>BE</sub> in saturation can be as high as about 0.85 V at 100 mA, and the resistor is ±5%. All eight corners for the 100 mA load:

| Pin voltage | V<sub>BE</sub> | R<sub>B</sub> | I<sub>B</sub> | Forced beta |
|---|---|---|---|---|
{corner_rows}
Even the worst corner gives {Ib_min*1000:.2f} mA, a forced beta of {fb_worst:.1f}, well below the minimum hFE of 100, so the switch stays saturated. The highest base current, {Ib_max*1000:.2f} mA, is what the pin must be able to source.

## Second example: PNP high side switch on 12 V

A 200 mA, 12 V load must be switched on its supply side. A PNP with minimum hFE 100 and 5 times overdrive needs I<sub>B</sub> = 200 ÷ 100 × 5 = **{Ib2*1000:.0f} mA**. A small NPN pulls the PNP base down to its own V<sub>CE(sat)</sub> of about {vsat} V, so the PNP base resistor drops 12 − 0.7 − 0.2 = {Vcc-Vbe-vsat:.1f} V and R<sub>B</sub> = {Vcc-Vbe-vsat:.1f} ÷ {Ib2*1000:.0f} mA = **{Rb2:,.0f} Ω**; use 1.1 kΩ. It dissipates {P2*1000:.0f} mW, so choose a 0.25 W part rather than a 0.125 W one. The NPN only switches {Ib2*1000:.0f} mA, so from a 3.3 V pin its own base resistor is (3.3 − 0.7) ÷ {Ib3*1000:.1f} mA = **{Rb3:,.0f} Ω** with the same overdrive. Add a 10 kΩ resistor from the PNP base to 12 V so it turns off firmly.
''',
     faq_add=[('How do I size the base resistor for a PNP high side switch?',
               f'Use the voltage from the supply to the driver: R_B = (V_supply − V_EB − V_CE(sat) of the driver) ÷ I_B. For a 200 mA load on 12 V with hFE 100 and 5 times overdrive, I_B = {Ib2*1000:.0f} mA and R_B = {Rb2:,.0f} Ω, so use 1.1 kΩ rated 0.25 W.'),
              ('Does resistor tolerance matter for a transistor switch?',
               f'Only a little when the overdrive is generous. With an 820 Ω ±5% resistor, a pin between 4.5 and 5 V and V_BE between 0.6 and 0.85 V, the base current ranges from {Ib_min*1000:.2f} to {Ib_max*1000:.2f} mA, still far more than the 1 mA needed for 100 mA at hFE 100.')])

# ================================================================ Pump affinity laws
Q1, H1, P1, N1, N2 = 100.0, 50.0, 18.5, 1450.0, 1160.0
rr = N2 / N1
assert abs(Q1 * rr - 80) < 1e-9 and abs(H1 * rr ** 2 - 32) < 1e-9 and abs(P1 * rr ** 3 - 9.472) < 1e-3
H0 = 65.0                        # shutoff head at full speed
a = (H0 - H1) / Q1 ** 2          # pump curve H = H0 r^2 - a Q^2
Hs = 20.0                        # static head
kf = (H1 - Hs) / Q1 ** 2         # system curve H = Hs + kf Q^2 through the duty point
Phyd = 1000 * G * (Q1 / 3600) * H1 / 1000
eta = Phyd / P1


def duty(r):
    num = H0 * r ** 2 - Hs
    if num <= 0:
        return 0.0, Hs
    Qd = math.sqrt(num / (a + kf))
    return Qd, Hs + kf * Qd ** 2


rows = ''
for r in (1.0, 0.9, 0.8, 0.7, 0.6):
    Qd, Hd = duty(r)
    Pd = 1000 * G * (Qd / 3600) * Hd / 1000 / eta
    rows += f"| {r*100:.0f}% ({N1*r:.0f} rpm) | {Q1*r:.1f} m³/h | {Qd:.1f} m³/h | {Hd:.1f} m | {Pd:.2f} kW | {P1*r**3:.2f} kW |\n"
Q8, H8 = duty(0.8)
P8 = 1000 * G * (Q8 / 3600) * H8 / 1000 / eta
r_min = math.sqrt(Hs / H0)
assert abs(duty(1.0)[0] - Q1) < 1e-9

edit('engineering/pump-affinity-laws', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Worked example with 20 m of static head

To see how static head changes the answer, model the pump curve at full speed as H = {H0:.0f} − {a:.4f} Q² (shutoff head {H0:.0f} m, passing through 100 m³/h at 50 m). At speed ratio r the curve scales to H = {H0:.0f} r² − {a:.4f} Q². The system needs {Hs:.0f} m of static lift plus friction, H = {Hs:.0f} + {kf:.3f} Q², which also passes through the original duty. The duty point is where the two curves cross: Q = √(({H0:.0f} r² − {Hs:.0f}) ÷ {a+kf:.4f}).

At 80% speed this gives Q = **{Q8:.1f} m³/h** at **{H8:.1f} m**, not the 80 m³/h and 32 m the affinity laws predict. The original duty has an efficiency of ρ g Q H ÷ P = {Phyd:.2f} ÷ {P1} = {eta*100:.1f}%; holding that efficiency, the shaft power is about **{P8:.2f} kW**.

| Speed | Affinity flow | Real flow | Real head | Estimated power | Affinity power |
|---|---|---|---|---|---|
{rows}
Below r = √({Hs:.0f} ÷ {H0:.0f}) = {r_min:.3f}, or {N1*r_min:.0f} rpm, the shutoff head is lower than the static lift and the pump delivers nothing while still absorbing power. Set the VFD minimum speed well above this point.
''',
     faq_add=[('What is the minimum speed before a pump stops delivering against static head?',
               f'The speed at which the scaled shutoff head equals the static head: N_min = N₁ × √(H_static ÷ H_shutoff). A pump with {H0:.0f} m shutoff head at 1,450 rpm lifting {Hs:.0f} m stops delivering at about {N1*r_min:.0f} rpm.')])

print('done', __import__('inplace').DONE)

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-26), section c5: snr, lambda-tuning, ntc-thermistor, convection-heat-transfer,
motor-winding-resistance-unbalance. Every number is computed here. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-26'

# ================================================================ SNR
Vs, Vn = 1.0, 1e-3
snr0 = 20 * math.log10(Vs / Vn)
assert abs(snr0 - 60) < 1e-9
# noise budget: sensor 1 mV, amp 0.5 mV, 12 bit ADC on 2.5 V range
n_s, n_a = 1.0e-3, 0.5e-3
lsb = 2.5 / 4096
n_q = lsb / math.sqrt(12)
n_tot = math.sqrt(n_s**2 + n_a**2 + n_q**2)
snr_tot = 20 * math.log10(Vs / n_tot)
n_half = math.sqrt(n_s**2 + (n_a / 2)**2 + n_q**2)
snr_half = 20 * math.log10(Vs / n_half)
# op amp noise density
en, gain, sig_in = 10e-9, 100, 10e-3
rows = ''
for fc in (100, 1000, 10000, 100000):
    nbw = 1.57 * fc
    vo = en * math.sqrt(nbw) * gain
    s = 20 * math.log10(sig_in * gain / vo)
    rows += f"| {fc:,} Hz | {nbw:,.0f} Hz | {vo*1e6:,.1f} µV | {s:.1f} dB | {(s-1.76)/6.02:.1f} |\n"
vo10k = en * math.sqrt(1.57 * 10000) * gain
snr10k = 20 * math.log10(sig_in * gain / vo10k)
# ADC below full scale
snr16 = 6.02 * 16 + 1.76

edit('electronics/snr', date=U, before='## How noise is measured in practice', min_words=800,
     body_add=f'''## Adding noise from several sources

Uncorrelated noise sources add as the root of the sum of squares, not arithmetically. Suppose the default signal (1,000 mV RMS) has 1 mV of sensor noise, a preamplifier adds 0.5 mV, and a 12 bit ADC on a 2.5 V range adds quantisation noise of one LSB ÷ √12 = {lsb*1e3:.4f} ÷ 3.464 = {n_q*1e3:.3f} mV:

- Total noise = √(1² + 0.5² + {n_q*1e3:.3f}²) = **{n_tot*1e3:.3f} mV**
- SNR = 20 log₁₀(1,000 ÷ {n_tot*1e3:.3f}) = **{snr_tot:.2f} dB**, {snr0-snr_tot:.2f} dB below the sensor alone
- Halving the amplifier noise to 0.25 mV only recovers the SNR to {snr_half:.2f} dB

The largest source dominates, so effort is best spent on the sensor here, not on a quieter amplifier or a bigger ADC.

## SNR from an amplifier noise density

Datasheets give voltage noise density in nV/√Hz. Multiply by the square root of the noise bandwidth, which is 1.57 times the −3 dB frequency for a single pole filter, then by the gain. For an op amp with 10 nV/√Hz, a gain of 100 and a 10 mV input signal (1 V out):

| −3 dB bandwidth | Noise bandwidth | Output noise | SNR | ENOB |
|---|---|---|---|---|
{rows}
Every tenfold cut in bandwidth gains 10 dB. Resistor and current noise add on top of this, so treat the figures as the best case.

''',
     faq_add=[('Why does my ADC give a lower SNR than the datasheet?',
               f'Datasheet SNR is measured with a signal near full scale. An ideal 16 bit ADC reaches {snr16:.2f} dB at full scale, but a signal at 1/10 of full scale (−20 dBFS) gets only {snr16-20:.2f} dB, because the noise floor stays put while the signal shrinks. Scale the input to use most of the range.'),
              ('How do I combine noise from several sources?',
               f'Add uncorrelated noise as √(n₁² + n₂² + ...). 1 mV and 0.5 mV combine to {math.sqrt(1.25):.3f} mV, not 1.5 mV. Correlated noise such as hum from a common source adds directly, which is why it is treated separately.')])

# ================================================================ Lambda tuning
K, tau, th, lam = 2.0, 60.0, 10.0, 30.0
Kc = tau / (K * (lam + th))
assert abs(Kc - 0.75) < 1e-12


def cc(K, tau, th):
    return (1 / K) * (tau / th) * (0.9 + th / (12 * tau)), th * (30 + 3 * th / tau) / (9 + 20 * th / tau)


rows = ''
for t in (5, 10, 30, 60, 120):
    l = 3 * t
    kl = tau / (K * (l + t))
    kc, ti = cc(K, tau, t)
    rows += f"| {t} s | {t/tau:.2f} | {l} s | {kl:.3f} | {kc:.3f} | {ti:.1f} s | {kc/kl:.1f} × |\n"
# heat exchanger temperature loop
K2, tau2, th2 = 1.5, 180.0, 30.0
lam2 = tau2
Kc2 = tau2 / (K2 * (lam2 + th2))
PB2 = 100 / Kc2
kcc2, ticc2 = cc(K2, tau2, th2)
# gain error
Kc_true = Kc
lam_eff = tau / (2 * K * Kc) - th  # if true gain is 2K, behaves as λ' with Kc = τ/(2K(λ'+θ))

edit('engineering/lambda-tuning', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Second example: heat exchanger outlet temperature

A steam heated exchanger is step tested: the outlet temperature moves {K2} % of span per % of valve, with τ = {tau2:.0f} s and θ = {th2:.0f} s. Temperature loops are usually tuned for robustness, so take λ = τ = {lam2:.0f} s:

- K<sub>c</sub> = {tau2:.0f} ÷ ({K2} × ({lam2:.0f} + {th2:.0f})) = **{Kc2:.3f}**, a proportional band of **{PB2:.0f}%**
- T<sub>i</sub> = τ = **{tau2:.0f} s** (3.0 min per repeat)
- After a set point step the outlet should reach 63% of the change about {lam2+th2:.0f} s later, without overshoot
- Cohen-Coon would give K<sub>c</sub> = {kcc2:.3f} and T<sub>i</sub> = {ticc2:.1f} s, a loop that would fight the slow steam valve

## How dead time changes the comparison

Same process gain (2) and time constant (60 s), λ set to 3θ in each case:

| Dead time θ | θ ÷ τ | λ = 3θ | Lambda K<sub>c</sub> | Cohen-Coon K<sub>c</sub> | Cohen-Coon T<sub>i</sub> | Ratio |
|---|---|---|---|---|---|---|
{rows}
The lambda gain falls with dead time while T<sub>i</sub> stays at τ; Cohen-Coon stays nearly four times more aggressive across the range.

## Robustness to a wrong process gain

If the real process gain is twice the step test value, the loop with K<sub>c</sub> = 0.750 behaves as if λ had been set to {lam_eff:.0f} s instead of 30 s: faster, with less margin. Choosing λ of 3θ or more leaves room for that kind of error, which is common when valve gain varies across the stroke.

''',
     faq_add=[('Does lambda tuning work when dead time is longer than the time constant?',
               f'Yes. The gain falls automatically because λ + θ grows. For K = 2, τ = 60 s and θ = 120 s with λ = 360 s, Kc = 60 ÷ (2 × 480) = {60/(2*480):.4f}. Keep λ at least equal to θ; for strongly dead time dominant loops some engineers also set Ti a little above τ.')])

# ================================================================ NTC thermistor
R25, B, T0 = 10.0, 3950.0, 298.15
Rt = R25 * math.exp(B * (1 / 333.15 - 1 / T0))
assert abs(Rt - 2.486) < 0.001
# B from two measurements
Ra, Ta, Rb, Tb = 10.05, 25.0, 1.452, 85.0
Bm = math.log(Ra / Rb) / (1 / (Ta + 273.15) - 1 / (Tb + 273.15))
R_fit = Ra * math.exp(Bm * (1 / 333.15 - 1 / (Ta + 273.15)))


def T_of(R, R25=10.0, B=3950.0):
    return 1 / (1 / T0 + math.log(R / R25) / B) - 273.15


rows = ''
for tc in (0, 25, 50, 75, 100):
    R = R25 * math.exp(B * (1 / (tc + 273.15) - 1 / T0))
    e_r = T_of(R, R25 * 1.01, B) - tc
    e_b = T_of(R, R25, B * 1.01) - tc
    rows += f"| {tc} °C | {R:,.2f} kΩ | {e_r:+.2f} °C | {e_b:+.2f} °C |\n"
e25 = T_of(10.0, 10.1, B) - 25

edit('electronics/ntc-thermistor', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Finding B from two measured points

When the datasheet is missing, measure the resistance at two known temperatures and solve B = ln(R₁ ÷ R₂) ÷ (1/T₁ − 1/T₂) with T in kelvin. A part reading {Ra} kΩ at {Ta:.0f} °C and {Rb} kΩ at {Tb:.0f} °C gives:

- 1/298.15 − 1/358.15 = {1/298.15-1/358.15:.7f} K⁻¹
- ln({Ra} ÷ {Rb}) = {math.log(Ra/Rb):.4f}
- B = **{Bm:,.0f} K**, so the part is most likely a 3,435 K type

With that B and R25 = {Ra} kΩ, the model gives {R_fit:.3f} kΩ at 60 °C. Use a stirred water bath and a reference thermometer, and pick points that bracket the range you will measure.

## How tolerance turns into temperature error

Datasheets quote R25 tolerance (often ±1%) and B tolerance separately. For a 10 kΩ, B 3,950 part, each 1% error alone shifts the reading by:

| True temperature | Resistance | R25 1% high | B 1% high |
|---|---|---|---|
{rows}
An R25 error is almost constant at about {abs(e25):.2f} °C, while a B error is zero at 25 °C and grows away from it. A one point calibration at the working temperature removes most of both.

''',
     faq_add=[('How do I find the B value of an unknown thermistor?',
               f'Measure its resistance at two known temperatures and use B = ln(R₁ ÷ R₂) ÷ (1/T₁ − 1/T₂) with T in kelvin. Readings of 10.05 kΩ at 25 °C and 1.452 kΩ at 85 °C give B = {Bm:,.0f} K.'),
              ('How much temperature error does a 1% thermistor cause?',
               f'For a 10 kΩ, B 3,950 part a 1% error in R25 shifts the reading by about {abs(e25):.2f} °C at any temperature. A 1% error in B adds nothing at 25 °C but grows to about {abs(T_of(R25*math.exp(B*(1/373.15-1/T0)),R25,B*1.01)-100):.1f} °C at 100 °C.')])

# ================================================================ Convection
h, A, Ts, Tf = 25.0, 2.0, 80.0, 25.0
Q = h * A * (Ts - Tf)
assert abs(Q - 2750) < 1e-9
sig, eps = 5.670374e-8, 0.9


def hr(ts, tf, e=eps):
    a, b = ts + 273.15, tf + 273.15
    return e * sig * (a * a + b * b) * (a + b)


rows = ''
for ts in (40, 60, 80, 120, 200):
    r = hr(ts, 25)
    rows += f"| {ts} °C | {r:.1f} W/m²·K | {r*2*(ts-25):,.0f} W |\n"
hr80 = hr(80, 25)
Qr80 = hr80 * A * 55
# enclosure: 120 W, 0.8 m2, h_conv 4, ambient 35
Qe, Ae, hc = 120.0, 0.8, 4.0
dT_conv = Qe / (hc * Ae)
# iterate with radiation
Tsx = 35 + 10
for _ in range(50):
    Tsx = 35 + Qe / ((hc + hr(Tsx, 35)) * Ae)
dT_both = Tsx - 35

edit('engineering/convection-heat-transfer', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Adding radiation as a second coefficient

Radiation can be written in the same form, Q<sub>r</sub> = h<sub>r</sub> A (T<sub>s</sub> − T<sub>∞</sub>), with h<sub>r</sub> = εσ(T<sub>s</sub>² + T<sub>∞</sub>²)(T<sub>s</sub> + T<sub>∞</sub>) in kelvin. Then the two coefficients simply add. For a painted surface (ε = {eps}) in surroundings at 25 °C and the 2 m² area of the worked example:

| Surface temperature | h<sub>r</sub> | Radiated heat from 2 m² |
|---|---|---|
{rows}
At 80 °C, h<sub>r</sub> = {hr80:.1f} W/m²·K, which adds {Qr80:,.0f} W to the convective result. Bare polished aluminium (ε near 0.05) radiates almost nothing, which is why it is used as an outer jacket on insulation.

## Second example: how hot will an enclosure run?

A sealed control panel with {Ae} m² of exposed surface dissipates {Qe:.0f} W in a {35} °C plant room. Solving the formula for the temperature difference, ΔT = Q ÷ (hA):

- Natural convection alone with h = {hc:.0f} W/m²·K: ΔT = {Qe:.0f} ÷ ({hc:.0f} × {Ae}) = **{dT_conv:.1f} K**, a surface at {35+dT_conv:.1f} °C
- Including radiation (ε = 0.9, solved by iteration because h<sub>r</sub> depends on T<sub>s</sub>): ΔT = **{dT_both:.1f} K**, a surface at {Tsx:.1f} °C

The air inside runs hotter than the skin, so with a skin near 49 °C this panel is already at the usual 40 to 50 °C limit for electronics and would need a filter fan or a cooler.

''',
     faq_add=[('How do I include radiation in a convection calculation?',
               f'Convert it to a radiation coefficient h_r = εσ(Ts² + T∞²)(Ts + T∞) using kelvin, then add it to the convective h. For a painted surface at 80 °C in a 25 °C room, h_r is about {hr80:.1f} W/m²·K.'),
              ('How do I find the surface temperature for a known heat load?',
               f'Rearrange to ΔT = Q ÷ (h A). A {Qe:.0f} W panel with {Ae} m² of surface and h = {hc:.0f} W/m²·K runs {dT_conv:.1f} K above ambient on convection alone, or about {dT_both:.1f} K once radiation is included.')])

# ================================================================ Motor winding resistance
R = (0.512, 0.508, 0.521)
Ra = sum(R) / 3
Rc25 = Ra * (234.5 + 25) / (234.5 + 32)
assert abs(Rc25 - 0.5002) < 1e-4
# copper loss at 75 C, star connected, rated current 30 A
Rll75 = Ra * (234.5 + 75) / (234.5 + 32)
Rph75 = Rll75 / 2
I = 30.0
Pcu = 3 * I**2 * Rph75
# temperature rise by resistance
Rcold, Tcold, Rhot = Rc25, 25.0, 0.6105
Thot = Rhot / Rcold * (234.5 + Tcold) - 234.5
amb = 25.0
rows = ''
for ratio in (1.05, 1.10, 1.20, 1.30, 1.40):
    t = ratio * (234.5 + 25) - 234.5
    rows += f"| {ratio:.2f} | {t:.1f} °C | {t-25:.1f} K |\n"

edit('electrical/motor-winding-resistance-unbalance', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Using the readings for copper loss

The corrected resistance also gives the stator copper loss used in efficiency calculations. For the worked example, wound in star with a rated current of {I:.0f} A:

- Line to line at 75 °C = 0.5137 × (234.5 + 75) ÷ (234.5 + 32) = **{Rll75:.4f} Ω**
- Phase resistance in star = half of that = {Rph75:.4f} Ω
- Copper loss = 3 × I² × R<sub>phase</sub> = 3 × {I:.0f}² × {Rph75:.4f} = **{Pcu:,.0f} W**

## Measuring winding temperature by resistance

Because copper resistance tracks temperature so closely, the resistance method is the standard way to find the average winding temperature after a heat run: T<sub>hot</sub> = (R<sub>hot</sub> ÷ R<sub>cold</sub>) × (234.5 + T<sub>cold</sub>) − 234.5. If the motor above reads {Rcold:.4f} Ω cold at 25 °C and {Rhot} Ω immediately after shutdown, the winding averaged **{Thot:.1f} °C**, a rise of {Thot-amb:.1f} K over a 25 °C ambient. Measure within a minute or two of stopping, or take several readings and extrapolate back to the moment of shutdown.

| Hot ÷ cold resistance (cold at 25 °C) | Average winding temperature | Rise over 25 °C |
|---|---|---|
{rows}
A class F insulation system is commonly limited to a 105 K rise by resistance, so a ratio near 1.40 is close to the limit.

''',
     faq_add=[('How can winding resistance tell me the winding temperature?',
               f'Use T_hot = (R_hot ÷ R_cold) × (234.5 + T_cold) − 234.5 for copper. A winding reading {Rcold:.4f} Ω at 25 °C and {Rhot} Ω after a heat run averaged {Thot:.1f} °C. This gives the average temperature; the hot spot is higher.'),
              ('How do I work out stator copper loss from the readings?',
               f'Correct the line to line average to the rated temperature, convert to phase resistance (half for star, 1.5 times for delta) and use 3 I² R. The example motor at 30 A loses about {Pcu:,.0f} W in the stator copper at 75 °C.')])

print('done', __import__('inplace').DONE)

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-26), section c6: absolute-gauge-pressure, manning-equation, barlow-formula,
vortex-shedding-frequency, bubbler-level. Every number is computed here. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-26'
G = 9.80665
MINUS = chr(0x2212)


def patm(z):
    return 101325 * (1 - 2.25577e-5 * z) ** 5.25588


# ================================================================ Absolute to gauge pressure
assert abs((2e5 + patm(0)) / 1e5 - 3.01325) < 1e-9
# compressor: suction 0.2 bar(g), discharge 6 bar(g)
ps_g, pd_g = 0.2, 6.0
cr_gauge = pd_g / ps_g
pa0 = patm(0) / 1e5
pa15 = patm(1500) / 1e5
cr0 = (pd_g + pa0) / (ps_g + pa0)
cr15 = (pd_g + pa15) / (ps_g + pa15)
# isentropic discharge temperature for air, k = 1.4, suction 30 C
k = 1.4
Ts = 303.15
Td0 = Ts * cr0 ** ((k - 1) / k) - 273.15
Td15 = Ts * cr15 ** ((k - 1) / k) - 273.15


# water boiling point under vacuum (Antoine, 1 to 100 C, P in mmHg)
def tsat(p_pa):
    mmhg = p_pa / 133.322
    return 1730.63 / (8.07131 - math.log10(mmhg)) - 233.426


assert abs(tsat(101325) - 100) < 0.1
brow = ''
for vac in (0.3, 0.5, 0.6, 0.7, 0.8):
    p0 = patm(0) - vac * 1e5
    p15 = patm(1500) - vac * 1e5
    brow += f"| {MINUS}{vac:g} bar(g) | {p0/100:.0f} mbar(a), {tsat(p0):.1f} °C | {p15/100:.0f} mbar(a), {tsat(p15):.1f} °C |\n"

edit('engineering/absolute-gauge-pressure', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Pressure ratios need absolute values

A ratio of pressures is meaningless in gauge units. An air compressor drawing at {ps_g} bar(g) and discharging at {pd_g:g} bar(g) would appear to have a ratio of {cr_gauge:.0f}. In absolute terms at sea level it is ({pd_g:g} + {pa0:.3f}) ÷ ({ps_g} + {pa0:.3f}) = **{cr0:.2f}**. The same gauge readings on a plant at 1,500 m, where the atmosphere is {pa15:.4f} bar, give a ratio of **{cr15:.2f}**, because the absolute suction pressure is lower. With air drawn in at 30 °C, the ideal (isentropic) discharge temperature T₂ = T₁ × r<sup>0.286</sup> rises from {Td0:.0f} °C at sea level to {Td15:.0f} °C at altitude, which is why compressor and blower ratings are always quoted against absolute inlet conditions.

## Boiling point of water at a vacuum reading

The temperature at which water boils depends on the absolute pressure, so a vacuum gauge alone does not fix it. Saturation temperatures from the Antoine equation:

| Gauge reading | At sea level | At 1,500 m |
|---|---|---|
{brow}
At {MINUS}0.8 bar(g) the two sites differ by {tsat(patm(0)-0.8e5)-tsat(patm(1500)-0.8e5):.0f} °C, enough to decide whether an evaporator boils or a pump suction flashes.

''',
     faq_add=[('Does a compression ratio use gauge or absolute pressure?',
               f'Absolute. A compressor from {ps_g} bar(g) to {pd_g:g} bar(g) at sea level has a ratio of ({pd_g:g} + {pa0:.3f}) ÷ ({ps_g} + {pa0:.3f}) = {cr0:.2f}, not {cr_gauge:.0f}. At 1,500 m the same gauge readings give {cr15:.2f}.'),
              ('At what temperature does water boil under vacuum?',
               f'It depends on the absolute pressure. At sea level a reading of {MINUS}0.8 bar(g) is about {(patm(0)-0.8e5)/100:.0f} mbar(a), where water boils near {tsat(patm(0)-0.8e5):.0f} °C; at 1,500 m the same gauge reading is only {(patm(1500)-0.8e5)/100:.0f} mbar(a) and water boils near {tsat(patm(1500)-0.8e5):.0f} °C.')])

# ================================================================ Manning equation
def manning(n, b, y, S):
    A = b * y
    R = A / (b + 2 * y)
    V = R ** (2 / 3) * math.sqrt(S) / n
    return V, V * A, R


V0, Q0, R0 = manning(0.013, 2, 0.5, 0.001)
assert abs(V0 - 1.169) < 1e-3
# best hydraulic rectangle of the same 1 m2 area: b = 2y
yb = math.sqrt(1 / 2)
bb = 2 * yb
Vb, Qb, Rb = manning(0.013, bb, yb, 0.001)
Pd, Pb_ = 3.0, bb + 2 * yb
# shape table, area 1 m2
srow = ''
for bw in (1.0, bb, 2.0, 3.0, 4.0):
    yy = 1 / bw
    v, q, rr = manning(0.013, bw, yy, 0.001)
    srow += f"| {bw:.3f} m × {yy:.3f} m | {bw/yy:.2f} | {bw+2*yy:.3f} m | {rr:.4f} m | {q:.3f} m³/s |\n"
# roughness table
nrow = ''
for n_, lab in ((0.011, 'Smooth plastic lining'), (0.013, 'Finished concrete'), (0.016, 'Rough or worn concrete'),
                (0.022, 'Clean earth'), (0.030, 'Earth with weeds'), (0.040, 'Heavy weed growth')):
    v, q, _ = manning(n_, 2, 0.5, 0.001)
    nrow += f"| {lab} | {n_:.3f} | {v:.3f} m/s | {q:.3f} m³/s | {100*q/Q0:.0f}% |\n"
_, Qweed, _ = manning(0.030, 2, 0.5, 0.001)


def ydepth(Q, n, b, S):
    lo, hi = 1e-6, 50
    for _ in range(200):
        m = (lo + hi) / 2
        if manning(n, b, m, S)[1] < Q:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


y_weed = ydepth(Q0, 0.030, 2, 0.001)

edit('engineering/manning-equation', date=U, before='## How it is used in practice', min_words=800,
     body_add=f'''## Best width to depth ratio

For a fixed flow area, the channel carries the most water when the wetted perimeter is smallest, because that gives the largest hydraulic radius. For a rectangle this happens when the width is twice the depth. The default channel (2 m × 0.5 m, area 1 m²) has a perimeter of {Pd:.1f} m. Reshaping the same 1 m² to {bb:.3f} m wide by {yb:.3f} m deep cuts the perimeter to {Pb_:.3f} m, raises R to {Rb:.4f} m and lifts the flow to **{Qb:.3f} m³/s**, {100*(Qb/Q0-1):.1f}% more for the same excavation area:

| Width × depth | b/y | Wetted perimeter | R | Flow |
|---|---|---|---|---|
{srow}
The curve is flat near the optimum, so practical designs often choose a wider, shallower section for easier maintenance and a lower water level, at a small cost in capacity.

## How roughness changes capacity

Same 2 m × 0.5 m section at 0.1% slope, with the share of the clean concrete flow:

| Surface condition | n | Velocity | Flow | Share |
|---|---|---|---|---|
{nrow}
Flow is inversely proportional to n. A concrete channel that has silted and grown weeds to n = 0.030 carries only {Qweed:.3f} m³/s at the same depth; to pass the original {Q0:.3f} m³/s the water must rise to {y_weed:.3f} m, which can overtop a channel built with little freeboard.

''',
     faq_add=[('What width to depth ratio gives the most flow in a rectangular channel?',
               f'A width of twice the depth, which gives the smallest wetted perimeter for the area. Reshaping a 2 m × 0.5 m concrete channel at 0.1% slope to {bb:.3f} m × {yb:.3f} m raises the flow from {Q0:.3f} to {Qb:.3f} m³/s with the same 1 m² of area.'),
              ('How much does weed growth reduce channel capacity?',
               f'Flow falls in proportion to 1/n. If a concrete channel (n = 0.013) becomes weedy with n = 0.030, the flow at the same depth drops to {100*Qweed/Q0:.0f}% of the clean value, and the depth for the original flow rises from 0.5 m to about {y_weed:.2f} m in the default channel.')])

# ================================================================ Barlow's formula
Pb0 = 2 * 290 * 7.11 / 168.3
assert abs(Pb0 - 24.50) < 0.01
# MAOP by location class
crow = ''
for cls, F in ((1, 0.72), (2, 0.60), (3, 0.50), (4, 0.40)):
    p = Pb0 * F
    crow += f"| Class {cls} | {F:.2f} | {p:.2f} MPa | {p*10:.0f} bar | {p*145.0377:,.0f} psi |\n"
# minimum wall incl. 12.5% tolerance and 1.5 mm corrosion allowance; choose schedule
sch = [('Sch 10', 3.40), ('Sch 40', 7.11), ('Sch 80', 10.97), ('Sch 120', 14.27), ('Sch 160', 18.26)]
wrow = ''
for P in (5, 10, 15, 20):
    tmin = P * 168.3 / (2 * 290 * 0.72)
    tnom = (tmin + 1.5) / 0.875
    pick = next((nm + f' ({tt} mm)' for nm, tt in sch if tt >= tnom), 'thicker than Sch 160')
    wrow += f"| {P} MPa | {tmin:.2f} mm | {tnom:.2f} mm | {pick} |\n"
# temperature derating example, T = 0.967 (B31.8 at 121 C), E = 1
T_ = 0.967
p_hot = Pb0 * 0.72 * T_

edit('engineering/barlow-formula', date=U, before="## Where Barlow's formula is used", min_words=800,
     body_add=f'''## Maximum operating pressure by location class

ASME B31.8 sets the gas pipeline design pressure as P = (2 S t ÷ D) × F × E × T, where E is the longitudinal joint factor and T the temperature derating factor. For the default 6" X42 pipe, seamless (E = 1) and below 121 °C (T = 1), the design pressure falls as the location class rises with population density:

| Location class | F | Design pressure | bar | psi |
|---|---|---|---|---|
{crow}
If the gas runs at 121 °C, T = {T_} and the class 1 figure drops to {p_hot:.2f} MPa.

## Choosing a schedule for a design pressure

For the same 168.3 mm X42 line at F = 0.72, the minimum Barlow wall is increased for a 1.5 mm corrosion allowance and divided by 0.875 for the 12.5% mill under-tolerance, then the next standard schedule is picked:

| Design pressure | Barlow wall | Nominal wall needed | Lightest schedule |
|---|---|---|---|
{wrow}
The allowances dominate at low pressure: at 5 MPa the pressure wall is barely 2 mm, yet the order wall is more than twice that.

''',
     faq_add=[('How do location class and temperature change a pipeline pressure rating?',
               f'ASME B31.8 multiplies the Barlow pressure by a design factor F, a joint factor E and a temperature factor T. The default 6" X42 pipe gives {Pb0*0.72:.2f} MPa in class 1 (F = 0.72) but only {Pb0*0.40:.2f} MPa in class 4 (F = 0.40), and at 121 °C (T = 0.967) the class 1 value falls to {p_hot:.2f} MPa.')])

# ================================================================ Vortex shedding frequency
f0 = 0.2 * 3 / 0.020
assert abs(f0 - 30) < 1e-9
# thermowell: straight well, tip 19 mm OD, bore 6.6 mm, stainless E 193 GPa, 8000 kg/m3, gas 25 m/s
Dw, dw, Ew, rw, Vg, St = 0.019, 0.0066, 193e9, 8000, 25.0, 0.2
I = math.pi * (Dw ** 4 - dw ** 4) / 64
Aw = math.pi * (Dw ** 2 - dw ** 2) / 4
fs = St * Vg / Dw


def fn(L):
    return 1.875104 ** 2 / (2 * math.pi * L ** 2) * math.sqrt(Ew * I / (rw * Aw))


trow = ''
for Lmm in (150, 200, 250, 300, 400):
    f_n = fn(Lmm / 1000)
    r = fs / f_n
    trow += f"| {Lmm} mm | {f_n:,.0f} Hz | {r:.2f} | {'below' if r < 0.8 else 'above'} 0.8 |\n"
Lmax = math.sqrt(1.875104 ** 2 / (2 * math.pi * fs / 0.8) * math.sqrt(Ew * I / (rw * Aw)))
fn250 = fn(0.25)

edit('engineering/vortex-shedding-frequency', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Worked example: is a thermowell too long?

A straight stainless thermowell with a {Dw*1000:.0f} mm tip and {dw*1000:.1f} mm bore sits in gas flowing at {Vg:.0f} m/s. With St = 0.2 the shedding frequency is f = 0.2 × {Vg:.0f} ÷ {Dw:.3f} = **{fs:.0f} Hz**. A simple cantilever estimate of the well's first natural frequency is f<sub>n</sub> = (1.875² ÷ 2πL²) × √(E I ÷ ρ A), with E = 193 GPa, ρ = 8,000 kg/m³, I = π(D⁴ − d⁴) ÷ 64 = {I*1e12:,.0f} mm⁴ and A = {Aw*1e6:.1f} mm². For a 250 mm well f<sub>n</sub> = {fn250:,.0f} Hz, so the ratio is {fs/fn250:.2f}. A common screening limit keeps f<sub>s</sub> below 0.8 f<sub>n</sub>:

| Immersion length | Natural frequency | f<sub>s</sub> ÷ f<sub>n</sub> | Screening |
|---|---|---|---|
{trow}
The natural frequency falls with the square of the length, so the longest well that meets the 0.8 ratio here is about **{Lmax*1000:.0f} mm**. PTC 19.3 TW also corrects for the mounting flexibility and the added mass of the fluid, which lower f<sub>n</sub>, so treat this estimate as an upper bound and run the full calculation before ordering.

''',
     faq_add=[('How long can a thermowell be before vortex shedding becomes a problem?',
               f'Compare the shedding frequency with the well natural frequency. A straight {Dw*1000:.0f} mm stainless well in {Vg:.0f} m/s gas sheds at {fs:.0f} Hz; a cantilever estimate puts the 0.8 frequency ratio limit at about {Lmax*1000:.0f} mm immersion, before the PTC 19.3 TW corrections for mounting and fluid mass, which shorten it further.')])

# ================================================================ Bubbler level
rho = 1.05 * 1000
h0 = 25000 / (rho * G)
L0 = h0 + 0.1
Pmax = rho * G * 2.9 / 100   # mbar
assert abs(L0 - 2.528) < 1e-3 and abs(Pmax - 298.6) < 0.05
mA = 4 + 16 * 250 / Pmax
# density change: hot liquor SG 1.02, transmitter configured for 1.05; true level 2.528 m
sg_hot = 1.02
p_true = sg_hot * 1000 * G * h0 / 100   # back pressure from the same head at SG 1.02
L_ind = p_true * 100 / (rho * G) + 0.1
err_mm = (L0 - L_ind) * 1000
# mA table
mrow = ''
for lv in (0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
    p = rho * G * (lv - 0.1) / 100
    mrow += f"| {lv:.1f} m | {p:.1f} mbar | {100*lv/3:.1f}% | {4+16*p/Pmax:.2f} mA |\n"
# purge gas use at 0.5 L/min
lpm = 0.5
m3_day = lpm * 60 * 24 / 1000
m3_yr = m3_day * 365

edit('engineering/bubbler-level', date=U, before='## Common mistakes', min_words=800,
     body_add=f'''## Transmitter output across the range

With the transmitter ranged 0 to {Pmax:.1f} mbar, 4 mA corresponds to the level at the tube end (0.1 m) and 20 mA to the 3 m maximum. The default reading of 250 mbar gives 4 + 16 × 250 ÷ {Pmax:.1f} = **{mA:.2f} mA**:

| Level from bottom | Back pressure | Percent of 3 m | Output |
|---|---|---|---|
{mrow}
Below 0.1 m the tube end is uncovered, the back pressure stays at zero and the output sits at 4 mA, so a bubbler cannot tell 0.1 m from an empty tank.

## Second example: density drift with temperature

The same liquor is heated and its SG falls to {sg_hot}. The level is still {L0:.3f} m, but the head of {h0:.3f} m now produces only {p_true:.1f} mbar. A transmitter or DCS block still configured for SG 1.05 reports {L_ind:.3f} m, **{err_mm:.0f} mm low**. If the density varies this much in service, add a second dip tube and compensate, or configure the density at the normal operating temperature.

## Purge gas consumption

A steady {lpm} L/min of free air is {m3_day:.2f} m³ a day, or about {m3_yr:,.0f} m³ a year per tank. That is small for instrument air but worth counting when nitrogen is bought in cylinders, and a reason to fit a constant flow regulator rather than leaving a needle valve wide open.

''',
     faq_add=[('What mA output should a bubbler transmitter give at a known level?',
               f'Output = 4 + 16 × back pressure ÷ URV. For SG 1.05, a tube end 0.1 m above the bottom and a 3 m maximum, the URV is {Pmax:.1f} mbar, so a reading of 250 mbar (level {L0:.3f} m) gives {mA:.2f} mA.'),
              ('How much purge gas does a bubbler use in a year?',
               f'At {lpm} L/min a bubbler uses {m3_day:.2f} m³ of free gas a day, about {m3_yr:,.0f} m³ a year. Instrument air makes this trivial, but on bottled nitrogen it decides how often cylinders are changed.')])

print('done', len(__import__('inplace').DONE))
