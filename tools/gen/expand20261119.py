"""Part C expansion (2026-11-19): 30 priority pages (crawled, not indexed) brought to the api-gravity standard. Assembled from six sections; edits are applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-19), slice 1: wire-resistance, rainwater-harvesting, required-run-rate, dp-level-range,
torque-power-speed. Numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-19'
pi = math.pi


def edit_keep_featured(cid, **kw):
    """The page is already featured. Lift the flag around the edit and restore it unchanged."""
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


# ---------------------------------------------------------------- Wire resistance
rho_cu, rho_al, a = 1.724e-8, 2.826e-8, 0.00393
L, A = 100.0, 1.5
R20 = rho_cu * L / (A * 1e-6)
R70 = R20 * (1 + a * 50)
rkm20 = R20 / L * 1000
# 4-20 mA loop: 500 m one way, 1.5 mm2 pair -> 1000 m conductor
Lloop = 1000.0
Rloop = rho_cu * Lloop / (A * 1e-6)
Rloop40 = Rloop * (1 + a * 20)
Vloop = 0.020 * Rloop40
# 2.5 mm2 per km table, copper and aluminium at several temperatures
t_rows = ''
for T in (0, 20, 40, 70, 90):
    cu = rho_cu * 1000 / 2.5e-6 * (1 + a * (T - 20))
    al = rho_al * 1000 / 2.5e-6 * (1 + 0.00403 * (T - 20))
    t_rows += f"| {T} °C | {cu:.3f} Ω/km | {al:.3f} Ω/km |\n"
# aluminium size for the same resistance as 16 mm2 copper
A_al = 16 * rho_al / rho_cu

edit('electrical/wire-resistance', date=U, phrase='wire resistance calculator',
     intro=("Every conductor has resistance that rises with length and temperature and falls with cross-section. "
            "This wire resistance calculator works it out for copper, aluminium and other metals at any temperature, and gives the figure per kilometre. "
            "See [what resistance is](https://www.instrumentationblog.in/what-is-resistance/) and [electrical conductivity explained](https://www.instrumentationblog.in/electrical-conductivity-explained/).\n\n"
            "Electricians use it to check voltage drop and cable heating, and instrument engineers use it to budget 4 to 20 mA loops and RTD lead errors."),
     body_add=f'''
## Worked example with the default values

The defaults describe **{L:g} m of 1.5 mm² annealed copper** at 20 °C. Converting the area to SI, 1.5 mm² is 1.5 × 10⁻⁶ m², so:

- R₂₀ = 1.724 × 10⁻⁸ × {L:g} ÷ 1.5 × 10⁻⁶ = **{R20:.4f} Ω**
- Resistance per km = {R20:.4f} ÷ {L:g} × 1,000 = **{rkm20:.2f} Ω/km**

If the same cable runs fully loaded at 70 °C, the resistance becomes {R20:.4f} × (1 + 0.00393 × 50) = **{R70:.4f} Ω**, about 20% higher. That is why voltage drop and loss figures for power cables are usually stated at the maximum conductor temperature, not at 20 °C.

## Loop example: a field transmitter 500 m away

A 4 to 20 mA transmitter 500 m from the control room on a 1.5 mm² copper pair has {Lloop:,.0f} m of conductor in the loop. At 20 °C that is {Rloop:.2f} Ω, and on a hot cable tray at 40 °C it is {Rloop40:.2f} Ω. At the full 20 mA the cable drops {Vloop:.3f} V, which must fit in the supply budget along with the transmitter minimum voltage and the input resistor.

## Resistance of 2.5 mm² conductor at different temperatures

| Temperature | Copper | Aluminium |
|---|---|---|
{t_rows}
To match a 16 mm² copper conductor with aluminium you need 16 × {rho_al:.3e} ÷ {rho_cu:.3e} = **{A_al:.1f} mm²**, so the next standard size, 35 mm², is the usual like-for-like swap once current rating is also checked.

## How conductor resistance is measured

Cable makers test conductor resistance with a DC micro-ohmmeter using a four-wire (Kelvin) connection, so the test lead resistance does not add to the reading. The sample is left to settle at room temperature, and the reading is corrected to 20 °C before comparing it with the IEC 60228 maximum. On site, a low-resistance ohmmeter across a looped pair at the far end gives the round-trip value; an ordinary multimeter is not accurate below about 1 Ω.

## Common mistakes

- **Using the one-way length.** A two-wire circuit has twice the route length of conductor; a three-phase balanced circuit uses the one-way length per phase.
- **Forgetting the mm² to m² conversion.** Leaving the area in mm² while ρ is in Ω·m gives a result a million times too large.
- **Applying the copper coefficient to nichrome.** The calculator uses 0.00393 /°C, which suits copper and aluminium; nichrome changes only about 0.0001 /°C, so its temperature correction here overstates the rise.
- **Ignoring AC effects on large cables.** Skin and proximity effect raise AC resistance noticeably above about 150 mm² at 50 Hz; datasheets list a separate AC value.
- **Comparing a calculated value with the standard limit.** IEC 60228 figures are maximums for stranded conductors, so a real cable can sit a few percent above the solid-wire calculation and still pass.
''',
     faq_add=[('What resistance does a 4 to 20 mA loop cable add?',
               f'Use the total conductor length, out and back. A 1.5 mm² copper pair to a transmitter 500 m away has 1,000 m of conductor, about {Rloop:.1f} Ω at 20 °C, which drops {0.02*Rloop:.2f} V at 20 mA.'),
              ('Why does my measured cable resistance differ from the calculation?',
               'Temperature is the usual cause, at about 0.4% per °C, followed by stranding, which adds a few percent. Also check the meter: below a few ohms you need a four-wire low-resistance ohmmeter, not a multimeter.')])

# ---------------------------------------------------------------- Rainwater harvesting
Ar, Rr, k = 100.0, 800.0, 0.85
V = Ar * Rr * k
day = V / 365
months = [('Jan', 31, 5), ('Feb', 28, 5), ('Mar', 31, 10), ('Apr', 30, 20), ('May', 31, 40), ('Jun', 30, 150),
          ('Jul', 31, 220), ('Aug', 31, 180), ('Sep', 30, 110), ('Oct', 31, 40), ('Nov', 30, 15), ('Dec', 31, 5)]
assert sum(m[2] for m in months) == 800
demand = 150.0  # L per day
m_rows = ''
net = []
for name, d, r in months:
    inflow = Ar * r * k
    use = demand * d
    net.append(inflow - use)
    m_rows += f"| {name} | {r} mm | {inflow:,.0f} L | {use:,.0f} L | {inflow-use:+,.0f} L |\n"
# sequent peak over two cycles: storage needed for no shortfall
peak, s, need_store = 0.0, 0.0, 0.0
cum = 0.0
mx = 0.0
for x in net * 2:
    cum += x
    mx = max(mx, cum)
    need_store = max(need_store, mx - cum)
annual_use = demand * 365
ff_lo, ff_hi = Ar * 1, Ar * 2
dry = V * 0.75

edit_keep_featured('ecology/rainwater-harvesting', date=U, phrase='rainwater harvesting calculator',
     intro=("A roof can collect a surprising amount of rain: every square metre gives about one litre for each millimetre that falls. "
            "This rainwater harvesting calculator multiplies roof area, annual rainfall and a runoff coefficient to give the yearly and average daily yield.\n\n"
            "Homeowners use it to size a storage tank or recharge pit, and architects use it to show compliance where local rules make rooftop harvesting compulsory for new buildings."),
     body_add=f'''
## Sizing a tank from monthly rainfall

An annual total hides the real problem in a monsoon climate: most rain falls in four months. Take the default roof ({Ar:g} m², k = {k}) and an illustrative 800 mm year, with a household using **{demand:g} L a day** for toilets, washing and garden:

| Month | Rain | Collected | Used | Surplus or deficit |
|---|---|---|---|---|
{m_rows}
The roof yields {V:,.0f} L against an annual use of {annual_use:,.0f} L, so supply covers demand over the year. Running the monthly balance through two cycles shows that a tank of about **{need_store/1000:,.1f} m³** ({need_store:,.0f} L) is needed to carry the monsoon surplus into the dry months with no shortfall. Most households settle for a smaller tank, accept municipal top-up from February to May, and send the overflow to a recharge pit.

## How the catchment is measured

Use the **plan area** of the roof, the footprint seen from above, not the sloped surface area: rain falls vertically, so a steep roof catches no more than a flat one of the same footprint. Only count roof sections whose gutters lead to the downpipe that feeds the tank. Take rainfall from the nearest India Meteorological Department or national weather station record, and design on a dry year rather than the average; at 75% of normal rainfall this roof gives about {dry:,.0f} L.

## First flush and filter losses

A first-flush diverter on this roof should hold {ff_lo:,.0f} to {ff_hi:,.0f} L (1 to 2 L per m²). It refills at every storm, so on a roof that sees many small showers the discarded volume adds up. Leaf screens and sand filters also spill water in heavy downpours. The runoff coefficient covers splash and evaporation, but not these losses.

## Common mistakes

- **Using the sloped roof area.** It overstates the yield; the horizontal footprint is the catchment.
- **Sizing the tank for the annual volume.** A {V/1000:,.0f} m³ tank would rarely fill and costs far more than needed; size it on the monthly balance.
- **Designing on average rainfall.** One year in four is well below average, so check the dry year too.
- **Mixing units.** One mm of rain on one m² is one litre; in inches and square feet, one inch on 1,000 ft² is about 623 US gallons.
- **Counting a green or gravel roof as a hard roof.** Their coefficient of about 0.5 can halve the expected yield.
''',
     faq_add=[('Should I use the sloped or flat roof area?',
               'Use the flat plan area, the footprint seen from above. Rain falls vertically, so the slope of the roof does not change how much it collects.'),
              (f'How big a tank does a 100 m² roof need?',
               f'It depends on the rainfall pattern and use. With 800 mm a year concentrated in the monsoon and a demand of 150 L a day, a monthly balance gives about {need_store/1000:,.0f} m³ for no shortfall; a smaller tank with overflow to a recharge pit is a common compromise.')])

# ---------------------------------------------------------------- Required run rate
tgt, runs, bl = 181, 92, 54
need = tgt - runs
rrr = need / (bl / 6)
rpb = need / bl
# asking rate after 3 more overs at a given scoring rate
climb_rows = ''
for r in (6, 8, 10, 12):
    left = need - 3 * r
    b2 = bl - 18
    climb_rows += f"| {r} per over | {left} | {b2 // 6} | {left/(b2/6):.2f} |\n"
# overs notation: 12.4 overs bowled in a T20
bowled = 12 * 6 + 4
remain = 120 - bowled
# ODI example
o_need = 300 - 150
o_rrr = o_need / ((300 - 180) / 6)
# boundaries: 89 off 54 if 20 singles/dots: how many fours/sixes
sixes_rows = ''
for b in (6, 9, 12):
    rest = need - 4 * b
    sixes_rows += f"| {b} fours ({4*b} runs) | {rest} | {bl-b} | {rest/(bl-b):.2f} |\n"

edit('sports/required-run-rate', date=U, phrase='required run rate calculator',
     intro=("The required run rate is the number of runs per over a chasing side must score from now on to reach its target. "
            "This required run rate calculator takes the target, the current score and the balls left, and returns runs needed, the asking rate per over and runs per ball.\n\n"
            "Captains and batters use it to pace a chase, commentators quote it every over, and fantasy and analytics fans use it to judge how a match is turning."),
     replace=[('\n## Example\n\nTarget 181, score 92 after 11 overs (54 balls left): 89 runs needed at **9.89 per over**, or 1.65 runs per ball.\n', '\n')],
     body_add=f'''
## How the asking rate climbs

The defaults (target {tgt}, score {runs}, {bl} balls left) give **{need} runs needed at {rrr:.2f} per over**, or {rpb:.2f} per ball. The next few overs decide whether that stays realistic. Here is the asking rate after three more overs at different scoring speeds:

| Next 3 overs at | Runs still needed | Overs left | New required rate |
|---|---|---|---|
{climb_rows}
Scoring at 6 an over for three overs pushes the target above 11 an over, while matching the asking rate keeps it level. This is why chasing sides try never to let the gap between current and required rate grow.

## Boundaries versus strike rotation

Boundaries take a big share of the load. If the batters hit a number of fours in the remaining {bl} balls, the other balls must supply the rest:

| Boundaries hit | Runs from other balls | Other balls | Runs per other ball |
|---|---|---|---|
{sixes_rows}
Even with 12 fours, the remaining balls still need almost a run each, so dot balls are as costly as missed boundaries.

## Overs notation and balls remaining

Scorecards write overs as overs and balls, so 12.4 overs means 12 overs and 4 balls, which is {bowled} balls, not 12.4 × 6. In a 20 over chase that leaves {remain} balls. In a one-day match a side on 150 after 30 overs chasing 300 needs {o_need} off 120 balls, an asking rate of **{o_rrr:.2f}**. Always enter balls remaining rather than a decimal overs figure.

## Common mistakes

- **Treating 12.4 overs as a decimal.** Four balls is two thirds of an over, not 0.4 of one.
- **Using the opposition total as the target.** The target is their total plus one; their total only ties the match.
- **Counting wides and no-balls as balls used.** Each gives a run and the ball is bowled again, so balls remaining does not fall.
- **Ignoring a revised target.** After a rain break, use the DLS target and the reduced overs, not the original figures.
- **Reading the rate without wickets.** 9.89 an over with eight wickets left is a fair chase; with two left it is a long shot.
''',
     faq_add=[('How do I convert overs like 12.4 into balls?',
               'Multiply the full overs by 6 and add the balls: 12.4 overs is 12 × 6 + 4 = 76 balls. In a 20 over innings that leaves 44 balls.'),
              ('How much does a maiden over raise the required rate?',
               f'With {need} needed off {bl} balls the rate is {rrr:.2f}. A maiden leaves {need} off {bl-6} balls, which lifts it to {need/((bl-6)/6):.2f} an over.')])

# ---------------------------------------------------------------- DP level range
sg, H, h0 = 1.0, 3000.0, 500.0
LRV = sg * h0 * 1
URV = sg * (h0 + H)
span = sg * H
mmH2O = 9.80665  # Pa per mmH2O (conventional)
LRV_kPa, URV_kPa = LRV * mmH2O / 1000, URV * mmH2O / 1000
lvl = 2000.0
dp = sg * (h0 + lvl)
mA = 4 + 16 * (dp - LRV) / span
sg_rows = ''
for s in (0.70, 0.85, 1.00, 1.20, 1.50):
    l, u = s * h0, s * (h0 + H)
    sg_rows += f"| {s:.2f} | {l:,.0f} | {u:,.0f} | {u-l:,.0f} | {u*mmH2O/100:,.1f} mbar |\n"
# density error: transmitter set for SG 1.0, liquid at SG 0.95, true level 2000 mm above min
true_dp = 0.95 * (h0 + lvl)
ind = (true_dp - LRV) / span * H

edit('engineering/dp-level-range', date=U, phrase='DP level range calculator',
     intro=("A DP transmitter measures level as the pressure of a liquid column, so its range depends on liquid density, tap positions and any fill in the impulse lines. "
            "This DP level range calculator works out LRV, URV and span for open tanks, dry legs and wet legs. See [wet leg and dry leg level measurement](https://www.instrumentationblog.in/wet-leg-dry-leg-level-measurement/).\n\n"
            "Instrument engineers use it to write calibration data sheets, and technicians use it to range a transmitter on the bench or by HART."),
     body_add=f'''
## Worked example with the default values

The defaults are an **open tank** with water (SG {sg:g}), a measuring span of {H:,.0f} mm and the minimum level {h0:,.0f} mm above the HP tap:

- LRV = {sg:g} × {h0:,.0f} = **{LRV:,.0f} mmH₂O** ({LRV_kPa:.2f} kPa), a suppressed zero
- URV = {sg:g} × ({h0:,.0f} + {H:,.0f}) = **{URV:,.0f} mmH₂O** ({URV_kPa:.2f} kPa)
- Span = **{span:,.0f} mmH₂O**

With the level {lvl:,.0f} mm above the minimum, the transmitter sees {dp:,.0f} mmH₂O and outputs 4 + 16 × ({dp:,.0f} − {LRV:,.0f}) ÷ {span:,.0f} = **{mA:.2f} mA**, which is {lvl/H*100:.1f}% of range.

## Range for different liquids (same tank)

Open tank, {H:,.0f} mm span, minimum level {h0:,.0f} mm above the HP tap. Values in mmH₂O:

| Liquid SG | LRV | URV | Span | URV in mbar |
|---|---|---|---|---|
{sg_rows}
## Ranging the transmitter in practice

On the bench, connect a calibrator to the HP port with the LP port vented, apply the LRV pressure and set 4 mA, then apply the URV and set 20 mA. With a HART communicator the same values are simply typed in, but a check at both ends against a reference is still good practice. After installation, a wet leg must be filled completely and vented before the zero is checked, and on steam drums the condensate pot must be allowed to fill before commissioning.

## Effect of a density change

The range is only correct at the design SG. If this transmitter is ranged for water but the liquid is actually SG 0.95, a true level {lvl:,.0f} mm above the minimum gives {true_dp:,.0f} mmH₂O, which the transmitter reads as **{ind:,.0f} mm**, an error of {lvl-ind:,.0f} mm. The suppressed zero makes it worse, because the 500 mm below the minimum level is also lighter than assumed.

## Common mistakes

- **Measuring h₀ from the tank bottom.** It must be from the HP tap centreline (or diaphragm centre) to the minimum level.
- **Getting the wet-leg sign wrong.** The filled reference leg pushes on the LP side, so it is subtracted and the LRV goes negative.
- **Using the process SG for capillary seals.** With remote seals the elevation uses the fill fluid SG times the vertical distance between the seals.
- **Mixing pressure units.** Calibrators may read mmH₂O at 4 °C or 20 °C, inH₂O or mbar; 1 mmH₂O is 0.0981 mbar at the conventional reference.
- **Forgetting that the wet leg changes with temperature.** A hot or partly evaporated leg shifts the zero, so check it after start-up.
''',
     faq_add=[('How do I convert the LRV and URV from mmH₂O to kPa or mbar?',
               f'Multiply mmH₂O by 0.00981 for kPa or by 0.0981 for mbar. The default range of {LRV:,.0f} to {URV:,.0f} mmH₂O is {LRV_kPa:.2f} to {URV_kPa:.2f} kPa.'),
              ('What current should the transmitter give at a known level?',
               f'Find the DP at that level, then mA = 4 + 16 × (DP − LRV) ÷ span. For the defaults, a level {lvl:,.0f} mm above the minimum gives {dp:,.0f} mmH₂O and {mA:.2f} mA.')])

# ---------------------------------------------------------------- Torque, power and speed
P, n = 11.0, 1460.0
T = P * 1000 * 60 / (2 * pi * n)
w = 2 * pi * n / 60
T_sync = P * 1000 * 60 / (2 * pi * 1500)
T_kgfm = T / 9.80665
# conveyor drive selection
Td, nd, eta = 1800.0, 40.0, 0.94
Pd = 2 * pi * nd * Td / 60 / 1000
Pm = Pd / eta
ratio = n / nd
Tm = Td / (ratio * eta)
# VFD table, 4-pole 11 kW, base 50 Hz, slip held at 40 rpm
v_rows = ''
for f in (10, 25, 50, 60, 75):
    sp = 30 * f - 40  # 4-pole sync rpm = 120 f / 4 = 30 f
    if f <= 50:
        tq = T
    else:
        tq = T * 50 / f
    pw = 2 * pi * sp * tq / 60 / 1000
    v_rows += f"| {f} Hz | {sp:,.0f} rpm | {tq:.1f} N·m | {pw:.2f} kW |\n"

edit('engineering/torque-power-speed', date=U, phrase='torque calculator',
     intro=("Torque, speed and power are linked for any rotating shaft: power equals torque times angular speed. "
            "This torque calculator finds motor torque from kW and rpm, the power needed to turn a load at a given speed, or the speed for a given torque and power.\n\n"
            "Mechanical and electrical engineers use it to size motors and gearboxes for conveyors, pumps and mixers, and to check that a drive can start and hold its load."),
     body_add=f'''
## The default case step by step

The defaults are an **{P:g} kW motor at {n:,.0f} rpm**. Converting speed to angular velocity, ω = 2π × {n:,.0f} ÷ 60 = {w:.2f} rad/s, and T = P ÷ ω = {P*1000:,.0f} ÷ {w:.2f} = **{T:.2f} N·m**, or {T_kgfm:.2f} kgf·m. Using the synchronous speed of 1,500 rpm instead would give {T_sync:.2f} N·m, about 3% low, so always use the full-load speed from the nameplate.

## Choosing a motor for a conveyor

A belt conveyor drum needs **{Td:,.0f} N·m at {nd:g} rpm**. The power at the drum is 2π × {nd:g} × {Td:,.0f} ÷ 60 = {Pd:.2f} kW. Through a helical gearbox at {eta*100:.0f}% efficiency the motor must deliver {Pm:.2f} kW, so the next standard rating, 11 kW, is chosen. With a {n:,.0f} rpm motor the gear ratio is {n:,.0f} ÷ {nd:g} = {ratio:.1f}:1, and the motor supplies {Td:,.0f} ÷ ({ratio:.1f} × {eta}) = **{Tm:.1f} N·m**, well inside its {T:.1f} N·m rating. Check starting torque as well: a loaded conveyor may need 150% of running torque to break away.

## Torque on a variable frequency drive

Below base speed a VFD holds rated torque and power falls with speed; above base speed it holds power and torque falls. For the default 11 kW, 4-pole motor (slip taken as 40 rpm):

| Frequency | Shaft speed | Available torque | Shaft power |
|---|---|---|---|
{v_rows}
A self-cooled motor run at full torque near 10 Hz may also need derating, because its shaft fan moves little air at low speed.

## How torque is measured

On a test bed, an in-line rotary torque transducer with strain gauges, or a dynamometer, gives torque directly, and power follows from the measured speed. In the plant, most VFDs estimate shaft torque from the motor current and flux model to within a few percent, which is good enough for trending load. A clamp meter reading on a direct-on-line motor only hints at load, because current includes a large magnetising part at light load.

## Common mistakes

- **Using synchronous speed.** 1,500 rpm instead of 1,460 rpm understates torque by about 3%.
- **Mixing rpm and rad/s.** P = T × ω needs ω in rad/s; with rpm the factor 2π ÷ 60 must be included.
- **Treating nameplate kW as input power.** IEC motor ratings are shaft output; electrical input is higher by the motor efficiency.
- **Leaving out gearbox losses.** Worm gearboxes can be only 50% to 85% efficient, far below a helical unit.
- **Confusing horsepower types.** Metric horsepower is 735.5 W and mechanical (imperial) horsepower is 745.7 W.
''',
     faq_add=[('Is the kW on a motor nameplate the input or output power?',
               'For IEC and NEMA motors the rated kW or hp is the mechanical output at the shaft. Electrical input is higher: divide the rating by the efficiency, for example 11 kW ÷ 0.91 is about 12.1 kW.'),
              ('Does a VFD change the torque a motor can give?',
               f'Up to base speed the motor can give rated torque ({T:.1f} N·m for 11 kW at 1,460 rpm) while power falls with speed. Above base speed torque falls in proportion, so power stays at about the rated kW.')])

print('done')

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-19), slice 2: epf, video-file-size, aquarium-volume, hydrostatic-pressure,
loan-payment. All numbers computed here from each page's default inputs. Two of these pages are
featured on the homepage; the featured flag is kept exactly as it is (edit_keep_featured)."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, BASE
U = '2026-11-19'
g0 = 9.80665


def edit_keep_featured(cid, **kw):
    """inplace.edit refuses featured pages (to stop new pages being featured). For a page that is
    already featured, hide the flag during the edit and put the same line back afterwards."""
    p = os.path.join(BASE, cid + '.mdx')
    s = open(p).read()
    line = 'featured: true\n'
    assert s.count(line) == 1, (cid, 'featured line')
    k = s.index(line)
    after = s[k + len(line):].split('\n', 1)[0]
    open(p, 'w').write(s.replace(line, '', 1))
    try:
        n = edit(cid, **kw)
    except Exception:
        open(p, 'w').write(s)
        raise
    t = open(p).read()
    anchor = after + '\n'
    assert t.count(anchor) == 1, (cid, 'anchor', after)
    t = t.replace(anchor, line + anchor, 1)
    open(p, 'w').write(t)
    return n


def inr(x):
    """Indian digit grouping, no decimals."""
    s = f"{round(x):d}"
    neg = s.startswith('-')
    s = s.lstrip('-')
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ','.join(parts) + ',' + tail
    return ('-' if neg else '') + s


# ---------------------------------------------------------------- EPF
def epf(B, A, bal, g, r):
    Y = 58 - A
    C = 0.24 * B - min(1250, 0.0833 * B)
    F = bal * (1 + r) ** Y + C * (12 + 5.5 * r) * ((1 + r) ** Y - (1 + g) ** Y) / (r - g)
    inv = C * 12 * ((1 + g) ** Y - 1) / g
    return C, F, inv, F - bal - inv


B, A, bal, g, r = 30000, 30, 200000, 0.05, 0.0825
C, F, inv, I = epf(B, A, bal, g, r)
Y = 58 - A
emp = 0.12 * B
er_epf = C - emp
eps = min(1250, 0.0833 * B)
bal_only = bal * (1 + r) ** Y
# VPF: extra 3,000 a month (10% of basic) from the employee, growing with salary
vpf = 3000
F_vpf = F + vpf * (12 + 5.5 * r) * ((1 + r) ** Y - (1 + g) ** Y) / (r - g)
vpf_inv = vpf * 12 * ((1 + g) ** Y - 1) / g
rate_rows = ''
for rr in (0.075, 0.08, 0.0825, 0.085):
    _, f, _, _ = epf(B, A, bal, g, rr)
    rate_rows += f"| {rr*100:g}% | ₹{inr(f)} |\n"
# first year interest check, monthly running balance method
run = bal
mi = 0.0
for m in range(12):
    run += C
    mi += run * r / 12
first_int = mi

edit('finance/epf', date=U, phrase='EPF calculator',
     intro=("The Employees' Provident Fund builds a retirement corpus from monthly deposits by you and your employer, and EPFO credits interest on the balance every year. "
            "This EPF calculator projects your balance at age 58 from your basic pay, current balance, salary growth and the declared interest rate.\n\n"
            "Salaried employees use it to see whether EPF alone will fund retirement, and to decide whether extra Voluntary Provident Fund deposits are worth making."),
     body_add=f'''
## Where the ₹{inr(C)} a month comes from

On the default basic + DA of ₹{inr(B)}, you put in 12% = ₹{inr(emp)}. Your employer also pays 12% = ₹{inr(emp)}, but ₹{inr(eps)} of that (8.33%, capped at ₹1,250 because the pension wage ceiling is ₹15,000) goes to the Employees' Pension Scheme. Only ₹{inr(er_epf)} of the employer share reaches EPF, so the monthly credit is {inr(emp)} + {inr(er_epf)} = **₹{inr(C)}**. In the first year, the running balance method gives about ₹{inr(first_int)} of interest on the opening ₹{inr(bal)} plus twelve deposits.

## Worked example: adding VPF, and leaving the balance alone

Take the same 30 year old and add a Voluntary Provident Fund deposit of ₹{inr(vpf)} a month (10% of basic), rising with salary at {g*100:g}% a year. Over {Y} years the extra deposits total ₹{inr(vpf_inv)}, and the projected corpus at 58 rises from ₹{inr(F)} to **₹{inr(F_vpf)}**.

The opening balance matters just as much. Left untouched at {r*100:g}%, today's ₹{inr(bal)} alone grows to **₹{inr(bal_only)}** by 58. Withdrawing it on a job change gives up that growth, which is why a transfer through your UAN is almost always the better choice.

## Corpus at 58 by interest rate

The rate is declared each year, so test a range. Default inputs (₹{inr(B)} basic, age {A}, ₹{inr(bal)} balance, {g*100:g}% raises):

| Interest rate | EPF at 58 |
|---|---|
{rate_rows}
Recent declared rates were 8.50% for 2019-20 and 2020-21, 8.10% for 2021-22, 8.15% for 2022-23 and 8.25% for 2023-24 and 2024-25.

## Checking the estimate against your passbook

Download the passbook from the EPFO member portal with your UAN. It shows the employee share, the employer EPF share and the pension share separately, plus the interest credited for each financial year. If the yearly employee deposits do not equal 12% of the basic on your salary slip, ask HR why. Interest for a year usually appears some months after the rate is announced, so a balance that looks short in April is often just waiting for that credit.

## Common mistakes

- **Using gross or CTC salary.** EPF is 12% of basic plus dearness allowance only; HRA, special allowance and bonus are excluded.
- **Counting the pension share as EPF.** The ₹{inr(eps)} a month that goes to EPS builds a pension entitlement, not a withdrawable balance.
- **Withdrawing before 5 years of service.** The amount becomes taxable, and TDS of 10% applies when the withdrawal is ₹50,000 or more and PAN is linked.
- **Reading the result in today's money.** A crore at 58 buys far less than a crore today; compare it with an inflation-adjusted retirement target.
- **Assuming the rate never changes.** It has moved between 8.10% and 8.50% in recent years, and a 0.25 point shift changes the corpus by several lakh.
''',
     faq_add=[('Is VPF worth it compared with PPF?',
               'VPF earns the EPF rate, which has been well above the PPF rate, and comes straight out of salary. PPF has a ₹1.5 lakh yearly limit but stays fully tax-free, while VPF interest on employee deposits above ₹2.5 lakh a year is taxable.'),
              ('What happens to my EPF if I change jobs?',
               'Transfer it to the new employer through the EPFO portal using the same UAN. The balance and your service period carry over, so interest keeps compounding and the 5 year tax rule counts your total service.')])

# ---------------------------------------------------------------- Video file size
br, t_min = 20.0, 60.0
size_gb = br * 1e6 * t_min * 60 / 8 / 1e9
size_gib = size_gb * 1e9 / 1024 ** 3
# two-camera 4K event
ev_br, ev_h = 100.0, 2.0
ev_gb = ev_br * 1e6 * ev_h * 3600 / 8 / 1e9
aud_mb = 0.32e6 * ev_h * 3600 / 8 / 1e6
up_mbps = 40.0
up_h = 2 * ev_gb * 8e9 / (up_mbps * 1e6) / 3600
card_rows = ''
for cap in (64, 128, 256, 512):
    cells = []
    for b in (20, 50, 100, 150):
        mins = cap * 8000 / b / 60
        cells.append(f"{mins:,.0f} min")
    card_rows += f"| {cap} GB ({cap*1e9/1024**3:.1f} GiB) | " + ' | '.join(cells) + ' |\n'
fat32_min = 4 * 1024 ** 3 * 8 / (br * 1e6) / 60

edit('other/video-file-size', date=U, phrase='video file size calculator',
     intro=("A video file grows with its bitrate, the number of bits recorded each second, multiplied by how long you record. "
            "This video file size calculator turns a bitrate in Mbps and a duration into gigabytes, or works backwards to the bitrate or recording time that fits a given size.\n\n"
            "Videographers use it to buy enough memory cards, editors to plan drive space for a project, and streamers to estimate upload times and storage costs."),
     body_add=f'''
## Default result, in GB and GiB

The defaults ({br:g} Mbps for {t_min:g} minutes) give {br:g} × 10⁶ × {t_min*60:,.0f} ÷ 8 = **{size_gb:.1f} GB**. Your computer may show the same file as {size_gib:.2f} GB, because Windows and many apps divide by 1,024³ (GiB) while card makers and this calculator use 10⁹ bytes.

## Worked example: a two-camera 4K event

A {ev_h:g} hour wedding is filmed on two cameras, each recording 4K at {ev_br:g} Mbps. Each camera writes {ev_br:g} × 10⁶ × {ev_h*3600:,.0f} ÷ 8 = **{ev_gb:.0f} GB**, so the shoot needs {2*ev_gb:.0f} GB plus spare cards. A separate stereo audio recorder at 320 kbps adds only {aud_mb:.0f} MB. Uploading both camera files to a client over a {up_mbps:g} Mbps connection takes about **{up_h:.0f} hours**, which is why many editors deliver a compressed copy and keep the camera originals on a drive.

## Recording time on common cards

Minutes of continuous recording at a constant bitrate (decimal GB as printed on the card):

| Card | 20 Mbps | 50 Mbps | 100 Mbps | 150 Mbps |
|---|---|---|---|---|
{card_rows}
Leave around 5% free; cameras stop when the card reports full and the file system needs some space.

## Finding the real bitrate of a file

Camera manuals list the bitrate for each resolution and frame rate mode. For an existing file, a tool such as MediaInfo or `ffprobe` reports the overall bitrate, which already includes audio and container overhead. Streaming platforms publish recommended upload bitrates; for YouTube these are around 8 Mbps for 1080p at 30 fps and 35 to 45 Mbps for 4K at 30 fps. Variable bitrate files spend more bits on fast motion, so a short busy clip can run well above the stated average.

## Common mistakes

- **Mixing Mbps and MB/s.** 100 Mbps is only 12.5 MB/s; dividing by 8 is the step most often forgotten.
- **Expecting the full card capacity.** A 128 GB card shows about 119 GiB on a computer, and part of it is used by the file system.
- **Using the average for a variable bitrate.** Size cards for the maximum bitrate of the mode if a shoot cannot be interrupted.
- **Forgetting the 4 GiB FAT32 limit.** On FAT32 cards cameras split long recordings; at {br:g} Mbps a new file starts about every {fat32_min:.0f} minutes, which is normal and not lost footage.
- **Planning only for camera files.** Editing proxies, render caches and exports often need as much space again as the original footage.
''',
     faq_add=[('Why is my video file smaller than the calculator says?',
               'Most cameras and encoders use variable bitrate, so static scenes use fewer bits than the stated rate. The calculator gives the size at a constant bitrate, which is the safe figure for planning storage.'),
              ('How long does it take to upload a video file?',
               'Upload time = file size in bits ÷ upload speed. A 9 GB file is 72,000 megabits, so at 20 Mbps it takes 3,600 seconds, about one hour, before any slowdown.')])

# ---------------------------------------------------------------- Aquarium volume
L, W, H = 100.0, 40.0, 45.0
V = L * W * H / 1000
gal_us = V / 3.785411784
gal_uk = V / 4.54609
glass = 1.0  # cm, 10 mm glass
Vin = (L - 2 * glass) * (W - 2 * glass) * H / 1000
sub_h = 5.0
sub_bulk = (L - 2 * glass) * (W - 2 * glass) * sub_h / 1000
sub_disp = sub_bulk * 0.6
Vnet = Vin - sub_disp
heater = V * 1.0
filt_lo, filt_hi = 4 * V, 6 * V
wc = 0.2 * Vnet
total_kg = V * 1.3
foot = (L / 100) * (W / 100)
load = total_kg / foot
foot_rows = ''
for (l, w) in ((60, 30), (80, 35), (100, 40), (120, 45), (150, 50)):
    per_cm = l * w / 1000
    foot_rows += f"| {l} × {w} cm | {per_cm:.2f} L | {per_cm/3.785411784:.3f} US gal | {per_cm*10:.0f} L |\n"

edit('other/aquarium-volume', date=U, phrase='aquarium volume calculator',
     intro=("An aquarium's water volume sets how many fish it can hold, the size of filter and heater it needs and every medicine or conditioner dose. "
            "This aquarium volume calculator works out litres and gallons from the length, width and water height, and the weight of the water.\n\n"
            "Fishkeepers use it before buying a tank or stand, and to dose treatments correctly, since an overdose based on a guessed volume can kill fish."),
     body_add=f'''
## Worked example: from glass size to real water volume

The default tank measures {L:g} × {W:g} cm and is filled to {H:g} cm: {L:g} × {W:g} × {H:g} ÷ 1,000 = **{V:.0f} L**, or {gal_us:.1f} US gallons ({gal_uk:.1f} UK gallons). That figure uses outside dimensions. With 10 mm glass the inside is {L-2*glass:g} × {W-2*glass:g} cm, so the water is {Vin:.1f} L. A {sub_h:g} cm gravel bed occupies {sub_bulk:.1f} L, but water fills about 40% of the gaps between grains, so it displaces roughly {sub_disp:.1f} L. The water you actually dose is about **{Vnet:.0f} L**, around {(1-Vnet/V)*100:.0f}% less than the label volume.

## Equipment for the default tank

- Heater at about 1 W per litre: {heater:.0f} W, so a 200 W heater (or two 100 W units for redundancy).
- Filter turnover of 4 to 6 times per hour: {filt_lo:.0f} to {filt_hi:.0f} L/h rated flow.
- A 20% weekly water change: about {wc:.0f} L, based on the real water volume.

## Litres per centimetre of water height

Useful when topping up or when the water line is below the rim:

| Footprint (inside) | Per cm | Per cm (US gal) | Per 10 cm |
|---|---|---|---|
{foot_rows}
## Weight and the floor

Allowing 1.3 kg per litre of tank volume for water, glass, substrate and rock, the default tank weighs about {total_kg:.0f} kg. Spread over a {L/100:g} × {W/100:g} m stand, that is {load:.0f} kg per square metre, far above the roughly 200 kg/m² (2 kN/m²) that residential floors are typically designed to carry spread evenly. Place large tanks across the floor joists or near a load-bearing wall, and use a stand built for the full weight.

## Common mistakes

- **Using outside dimensions.** Glass thickness, the top rim and bracing reduce the water volume, often by 5 to 10% on mid-sized tanks.
- **Using tank height instead of water height.** Most tanks are filled 2 to 3 cm below the rim.
- **Confusing US and UK gallons.** A UK gallon is 4.546 L and a US gallon 3.785 L; dosing labels from different countries differ by 20%.
- **Dosing on the gross volume.** Substrate, rock and a sump change the real volume; medicines are best dosed on the water actually present.
- **Forgetting the sump.** If the tank drains to a sump, add its running water volume to the total for dosing and heating.
''',
     faq_add=[('Should I dose medicine on the tank volume or the water volume?',
               'Use the real water volume: inside dimensions, actual water height, minus substrate and rock, plus any sump. For the default 180 L tank that is closer to 156 L, so dosing on 180 L would give about 15% too much.')])

# ---------------------------------------------------------------- Hydrostatic pressure
h, rho = 5.0, 1000.0
P_pa = rho * g0 * h
P_bar = P_pa / 1e5
P_psi = P_pa / 6894.757
Patm = 101325.0
P_abs = (P_pa + Patm) / 1e5
d_mount = 1.2
lrv = rho * g0 * d_mount / 1e5
urv = rho * g0 * (d_mount + h) / 1e5
# brine read by a water-calibrated transmitter
rho_b = 1200.0
true_h = P_pa / (rho_b * g0)
depth_rows = ''
for d in (0.5, 1, 2, 5, 10, 20, 50):
    pa = 1000 * g0 * d
    depth_rows += f"| {d:g} m | {pa/1000:,.2f} kPa | {pa/1e5:.4f} bar | {pa/6894.757:.2f} psi | {(pa+Patm)/1e5:.3f} bar |\n"
g_eq, g_pole = 9.780, 9.832
P_eq = rho * g_eq * h
P_pole = rho * g_pole * h

edit_keep_featured('engineering/hydrostatic-pressure', date=U, phrase='hydrostatic pressure calculator',
     intro=("The pressure at the bottom of a liquid column depends only on its height and density, which is how most tank level transmitters work. "
            "This hydrostatic pressure calculator applies P = ρgh to give the pressure for a level, or the level for a measured pressure.\n\n"
            "Instrument engineers use it to range level transmitters and check readings; see [hydrostatic level measurement](https://www.instrumentationblog.in/hydrostatic-level-measurement/) and [zero elevation and zero suppression](https://www.instrumentationblog.in/zero-elevation-and-zero-suppression/)."),
     body_add=f'''
## Default result in other units

The default 5 m of water at 1,000 kg/m³ gives {P_pa:,.0f} Pa = **{P_bar:.4f} bar** = {P_pa/1000:.2f} kPa = {P_psi:.2f} psi gauge. On an absolute scale, adding standard atmospheric pressure of 1.01325 bar gives {P_abs:.3f} bar(a), which is the figure needed for a sealed absolute transmitter or for gas solubility work.

## Worked example: transmitter below the tank nozzle

A gauge transmitter sits {d_mount:g} m below the bottom nozzle of an open water tank, with the impulse line full of water. At empty tank it already sees {d_mount:g} m of head: {rho:,.0f} × {g0} × {d_mount:g} = {lrv*1e5:,.0f} Pa = **{lrv:.4f} bar**. At the 5 m maximum it sees {d_mount+h:g} m, **{urv:.4f} bar**. So the range is set to {lrv:.4f} to {urv:.4f} bar, an elevated zero. Ranging it 0 to {P_bar:.4f} bar instead would make an empty tank read {d_mount/h*100:.0f}% full.

## Wrong density, wrong level

If the same {P_bar:.4f} bar is produced by a brine of {rho_b:,.0f} kg/m³, the true level is {P_pa:,.0f} ÷ ({rho_b:,.0f} × {g0}) = **{true_h:.2f} m**, not 5 m. A transmitter ranged for water over-reads by {(h/true_h-1)*100:.0f}%. Whenever the product changes, recalculate the range with the new density.

## Water depth to pressure table

For water at 1,000 kg/m³ and standard gravity:

| Depth | Gauge pressure | Gauge (bar) | Gauge (psi) | Absolute (bar) |
|---|---|---|---|---|
{depth_rows}
## Does local gravity matter?

Gravity varies from about {g_eq} m/s² at the equator to {g_pole} m/s² at the poles. The 5 m water column gives {P_eq:,.0f} Pa at the equator and {P_pole:,.0f} Pa at the poles, a {(P_pole/P_eq-1)*100:.1f}% spread. That is below the accuracy of most level loops, so standard gravity is used, but custody transfer tank gauging applies local g.

## Common mistakes

- **Measuring from the tank bottom instead of the tapping point.** Level below the transmitter tapping is invisible to it; h is the height above the measuring point.
- **Ignoring the gas pressure in a closed tank.** A gauge transmitter at the bottom of a pressurised vessel reads blanket pressure plus liquid head; use a DP transmitter referenced to the top.
- **Treating mH2O and metres of liquid as the same.** 1 mH2O is defined with water at 1,000 kg/m³; 1 m of diesel produces only about 0.84 mH2O.
- **Mixing gauge and absolute.** Adding or forgetting 1.013 bar shifts the reading by about 10.3 m of apparent water level, double the whole 5 m range.
- **Leaving gas in a liquid filled impulse line.** A bubble in the leg changes the head between tank and transmitter and gives an offset that drifts with temperature.
''',
     faq_add=[('How do I set the range of a level transmitter mounted below the tank?',
               f'Add the liquid head between the tank nozzle and the transmitter to both ends of the range. For water and a {d_mount:g} m drop, a 0 to 5 m tank becomes {lrv:.4f} to {urv:.4f} bar.')])

# ---------------------------------------------------------------- Loan payment
P0, ra, ty = 200000.0, 0.09, 5
i = ra / 12
n = ty * 12


def emi(p, i, n):
    return p * i * (1 + i) ** n / ((1 + i) ** n - 1)


M = emi(P0, i, n)
T = M * n
Itot = T - P0
# balance after 12 payments
b12 = P0 * (1 + i) ** 12 - M * ((1 + i) ** 12 - 1) / i
pre = 20000.0
b_after = b12 - pre
# keep EMI, shorten term
n_left = -math.log(1 - b_after * i / M) / math.log(1 + i)
n_full = math.ceil(n_left)
last = b_after * (1 + i) ** (n_full - 1) - M * ((1 + i) ** (n_full - 1) - 1) / i
last_pay = last * (1 + i)
paid_short = 12 * M + pre + (n_full - 1) * M + last_pay
save_term = T - paid_short
# keep term, cut EMI
M_new = emi(b_after, i, 48)
paid_emi = 12 * M + pre + 48 * M_new
save_emi = T - paid_emi
# processing fee: effective rate
fee = 0.02 * P0
net = P0 - fee


def pv(rate_m):
    return M * (1 - (1 + rate_m) ** -n) / rate_m


lo, hi = 1e-6, 0.05
for _ in range(200):
    mid = (lo + hi) / 2
    if pv(mid) > net:
        lo = mid
    else:
        hi = mid
apr = mid * 12
rate_rows = ''
for rr in (0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.14):
    m_ = emi(P0, rr / 12, n)
    rate_rows += f"| {rr*100:g}% | {m_:,.2f} | {m_*n-P0:,.2f} |\n"

edit_keep_featured('finance/loan-payment', date=U, phrase='loan payment calculator',
     intro=("A loan's monthly payment depends on three things: the amount borrowed, the interest rate and the number of months. "
            "This loan payment calculator gives the equal monthly instalment (EMI) on a reducing balance, the total repaid and the total interest, and can solve for the amount, rate or term instead.\n\n"
            "Borrowers use it to budget before signing for a home, car or personal loan, and to compare offers by their full cost."),
     body_add=f'''
## Worked example: a prepayment after one year

Using the default loan (200,000 at 9% for 5 years, EMI {M:,.2f}), the balance after 12 payments is {b12:,.2f}. A one-time prepayment of {pre:,.0f} at that point lowers it to {b_after:,.2f}. The lender then offers two choices:

- **Keep the EMI, shorten the term.** n = ln(1 ÷ (1 − B × i ÷ EMI)) ÷ ln(1 + i) = {n_left:.2f} months, so the loan ends after {12+n_full} payments instead of 60 (the last one is {last_pay:,.2f}). Interest saved: **{save_term:,.2f}**.
- **Keep the term, cut the EMI.** The remaining 48 payments fall to {M_new:,.2f}. Interest saved: **{save_emi:,.2f}**.

Shortening the term saves more, because the principal is cleared sooner. Cutting the EMI suits someone whose budget is tight.

## How the rate changes the payment

For 200,000 over 5 years:

| Annual rate | Monthly payment | Total interest |
|---|---|---|
{rate_rows}
Each extra percentage point adds roughly 95 to 100 a month on this loan, and about 5,700 to 5,800 in interest over the term.

## Fees change the real rate

A 2% processing fee of {fee:,.0f} means you receive {net:,.0f} but still repay {M:,.2f} for 60 months. Solving for the rate that makes those payments worth {net:,.0f} gives an effective annual rate of **{apr*100:.2f}%**, not 9%. Compare loans on this effective rate (the APR), which also captures insurance or other charges deducted at the start.

## Common mistakes

- **Typing a monthly rate into an annual field.** 0.75% a month is 9% a year; entering 0.75 as the annual rate gives a payment far too small.
- **Assuming a floating rate rise changes the EMI.** Many home lenders keep the EMI and extend the term instead, which can add years of payments; ask which option applies.
- **Ignoring insurance bundled into the loan.** A single premium added to the principal earns interest for the whole term.
- **Prepaying late in the term.** By year five most of each EMI is already principal, so a prepayment then saves little interest.
- **Comparing loans of different terms by EMI alone.** A lower EMI over a longer term can cost more in total; compare total interest and the APR.
''',
     faq_add=[('Is it better to reduce the EMI or the tenure after a prepayment?',
               f'Reducing the tenure saves more interest. On a 200,000 loan at 9% over 5 years, prepaying 20,000 after a year saves about {save_term:,.0f} by shortening the term, against about {save_emi:,.0f} by lowering the EMI.'),
              ('How does a processing fee affect the interest rate?',
               f'The fee reduces the money you receive while the payments stay the same, so the effective rate rises. A 2% fee on a 9% five year loan gives an effective rate of about {apr*100:.2f}%.')])

print('done')

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-19), slice 3: protein-molecular-weight, dp-flow-square-root, ligation-ratio,
water-heater-time, sip. Numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-19'


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


# ---------------------------------------------------------------- Protein molecular weight
aa, avg = 350, 110.0
kda = aa * avg / 1000
res = [('Gly', 'G', 57.0519), ('Ala', 'A', 71.0788), ('Ser', 'S', 87.0782), ('Pro', 'P', 97.1167),
       ('Val', 'V', 99.1326), ('Thr', 'T', 101.1051), ('Cys', 'C', 103.1388), ('Leu / Ile', 'L, I', 113.1594),
       ('Asn', 'N', 114.1038), ('Asp', 'D', 115.0886), ('Gln', 'Q', 128.1307), ('Lys', 'K', 128.1741),
       ('Glu', 'E', 129.1155), ('Met', 'M', 131.1926), ('His', 'H', 137.1411), ('Phe', 'F', 147.1766),
       ('Arg', 'R', 156.1875), ('Tyr', 'Y', 163.1760), ('Trp', 'W', 186.2132)]
rm = {r[1]: r[2] for r in res}
rm['L'] = rm['I'] = 113.1594
water = 18.0153
res_rows = ''.join(f"| {n} ({c}) | {m:.2f} |\n" for n, c, m in res)
pep = 'GAVLK'
pep_mw = sum(rm[c] for c in pep) + water
pep_est = len(pep) * avg
his6 = 6 * rm['H']
tagged = (aa + 20) * avg / 1000
dimer = 2 * kda
sig = 25
mature = (aa - sig) * avg / 1000
conc_rows = ''
for k in (10, 25, kda, 50, 100, 150):
    um = 1e6 / (k * 1000)
    mgml10 = 10e-6 * k * 1000
    conc_rows += f"| {k:g} kDa | {um:.1f} µM | {mgml10:.3f} mg/mL |\n"
um_def = 1e6 / (kda * 1000)

edit('biology/protein-molecular-weight', date=U, phrase='protein molecular weight calculator',
     intro=("A protein's mass can be estimated from its length alone, because the average amino acid residue weighs about 110 daltons once the water lost in each peptide bond is taken off. "
            "This protein molecular weight calculator multiplies the residue count by that average to give the size in kDa.\n\n"
            "Biochemists and students use it to predict where a band should run on an SDS gel, to pick a dialysis cutoff, and to convert mg/mL into molar concentration."),
     body_add=f'''
## Exact mass from the sequence

The 110 Da average is good for whole proteins, but the true mass is the sum of the residue masses plus one water ({water:.2f} Da) for the free ends. Average residue masses (amino acid minus water):

| Residue | Mass (Da) |
|---|---|
{res_rows}
For the short peptide {pep}, the sum is {sum(rm[c] for c in pep):.2f} + {water:.2f} = **{pep_mw:.2f} Da**, while the 110 Da rule gives {pep_est:.0f} Da, {(pep_est/pep_mw-1)*100:.0f}% too high. Short peptides rich in small residues such as glycine and alanine are where the estimate fails; for a full sequence, use a sequence tool such as ExPASy ProtParam.

## Tags, signal peptides and complexes

The default 350 residue protein comes out at **{kda:.1f} kDa**. Real constructs rarely match the bare gene:

- A His<sub>6</sub> tag adds {his6:.0f} Da; with a typical 14 residue linker and protease site the tag region is about 20 residues, giving {tagged:.1f} kDa.
- A secreted protein loses its signal peptide. Removing a {sig} residue signal leaves a mature chain of about {mature:.1f} kDa.
- A homodimer is {dimer:.0f} kDa in native gel filtration, but still runs at {kda:.1f} kDa on a reducing SDS gel because the subunits separate.

## Converting mass concentration to molarity

Assays, binding studies and crystallisation screens need molar concentrations, and the molecular weight is the conversion factor: µM = (mg/mL) ÷ kDa × 1,000. For the default {kda:.1f} kDa protein, 1 mg/mL is **{um_def:.1f} µM**.

| Protein size | 1 mg/mL equals | 10 µM equals |
|---|---|---|
{conc_rows}
The same rule picks a membrane for concentrating or dialysing: choose a molecular weight cutoff of a third to a half of the protein mass, so a 10 kDa cutoff device suits a {kda:.1f} kDa protein.

## Common mistakes

- **Using 128 Da per residue.** That is the average free amino acid; inside a chain each residue has lost a water, so the estimate comes out about 16% high.
- **Counting the stop codon.** A 1,053 bp coding sequence gives 350 residues, not 351; the stop codon codes for no amino acid.
- **Forgetting cleaved and added parts.** Signal peptides, propeptides and the initiator methionine may be removed, while tags and fusion partners such as GST (about 26 kDa) add a lot of mass.
- **Reading native size from an SDS gel.** SDS separates subunits, so oligomers appear at the monomer mass.
- **Expecting glycoproteins to match.** Glycosylation can add 10 to 50% to the mass and makes bands run broad and high.
''',
     faq_add=[('How do I convert a protein concentration from mg/mL to µM?',
               f'Divide mg/mL by the molecular weight in kDa and multiply by 1,000. For a {kda:.1f} kDa protein, 1 mg/mL is about {um_def:.1f} µM.'),
              ('How much mass does a His-tag add?',
               f'Six histidine residues add about {his6:.0f} Da. With the usual linker and protease cleavage site the whole tag region is closer to 2 kDa.')])

# ---------------------------------------------------------------- DP flow square root
dPm, Qm, dP = 250.0, 100.0, 62.5
dPp = dP / dPm
Qp = math.sqrt(dPp)
Q = Qp * Qm
dP2 = 160.0
Qp2 = math.sqrt(dP2 / dPm)
mA_lin = 4 + 16 * dP2 / dPm
mA_sq = 4 + 16 * Qp2
double = math.sqrt(Qp2)
e = 0.001 * dPm  # 0.1% of span
err_rows = ''
for fq in (0.10, 0.20, 0.30, 0.50, 0.70, 1.00):
    d = fq ** 2 * dPm
    q1 = Qm * math.sqrt(d / dPm)
    q2 = Qm * math.sqrt((d + e) / dPm)
    err_rows += f"| {fq*100:.0f}% | {d:.2f} mbar | {q2-q1:.3f} m³/h | {(q2-q1)/q1*100:.2f}% |\n"
rho_ratio = 1.05
err10 = (math.sqrt((0.01 * dPm + e) / dPm) - 0.1) / 0.1 * 100
rd_err = (math.sqrt(rho_ratio) - 1) * 100

edit('engineering/dp-flow-square-root', date=U, phrase='DP flow square root calculator',
     intro=("Orifice plates, venturis and other differential pressure meters produce a DP that rises with the square of flow, so the signal must be square rooted before it reads as flow. "
            "This DP flow square root calculator converts a measured DP into percent and actual flow, or a flow into the DP it should give. "
            "Learn about [square root extraction in DP flow measurement](https://www.instrumentationblog.in/square-root-extraction-dp-flow/).\n\n"
            "Instrument technicians use it during loop checks and calibration, and process engineers to sanity check a flow reading against the transmitter DP."),
     body_add=f'''
## Second example: reading the output current

With the same 0 to {dPm:.0f} mbar, 0 to {Qm:.0f} m³/h range, suppose the transmitter sees **{dP2:.0f} mbar**. DP is {dP2/dPm*100:.0f}% of range, so flow is √{dP2/dPm:.2f} = **{Qp2*100:.0f}%**, or {Qp2*Qm:.0f} m³/h. A transmitter set to linear DP output sends {mA_lin:.2f} mA, while one set to square root output sends {mA_sq:.2f} mA. If the DCS then applies a second square root to the {mA_sq:.2f} mA signal, it displays {double*100:.1f}% flow, {double*Qm-Qp2*Qm:.1f} m³/h too high, which is the classic double extraction error.

## How a small DP error grows at low flow

Take a zero error of only 0.1% of span ({e:.2f} mbar). Its effect on the flow reading depends on where in the range you are:

| Flow | DP at that flow | Flow error | Error as % of reading |
|---|---|---|---|
{err_rows}
The same {e:.2f} mbar that is invisible at full flow becomes a {err10:.2f}% error at 10% flow. This is the reason for low flow cutoff and for keeping the normal operating point above about 30% of the meter range.

## Checking the loop in the field

- Isolate the transmitter on its 3 or 5 valve manifold, open the equalising valve and confirm the output reads zero DP, then zero flow in the DCS.
- Inject DP with a hand pump and calibrator at 0, 25, 50, 75 and 100% of DP and record both the mA and the displayed flow. The displayed flow should be 0, 50, 70.7, 86.6 and 100%.
- Confirm the DP range matches the orifice sizing sheet. If the plate was sized for {dPm:.0f} mbar at {Qm:.0f} m³/h, a transmitter ranged at 0 to 200 mbar would saturate before maximum flow.
- On liquid service vent gas from the impulse lines; on gas service drain liquid, since a trapped leg adds a fixed DP offset.

## Common mistakes

- **Square rooting in two places.** Decide whether the transmitter or the DCS extracts the root, and document it on the loop sheet.
- **Swapping the HP and LP lines.** A reversed DP reads negative or clamps at zero, so the meter shows no flow while the line is running.
- **Ignoring a change in fluid density.** Volumetric flow follows √(ΔP ÷ ρ). A fluid {(rho_ratio-1)*100:.0f}% denser than the design value makes the reading about {rd_err:.1f}% high.
- **Setting the cutoff too high.** A 10% flow cutoff hides real low flow during start up; set it just above the noise level.
- **Ranging the transmitter on site without the orifice calculation.** The DP at maximum flow comes from the plate bore and fluid data, not from a round number.
''',
     faq_add=[('Does fluid density affect the square root flow reading?',
               f'Yes. Volumetric flow is proportional to √(ΔP ÷ ρ), so the meter is only right at its design density. A fluid {(rho_ratio-1)*100:.0f}% denser than design makes the volumetric reading about {rd_err:.1f}% high unless the DCS applies a density correction.')])

# ---------------------------------------------------------------- Ligation ratio
vng, vbp, ibp, r = 50.0, 3000, 1000, 3.0
ing = vng * ibp / vbp * r


def mw_ds(bp):
    return bp * 617.96 + 36.04


v_fmol = vng * 1e-9 / mw_ds(vbp) * 1e15
i_fmol = ing * 1e-9 / mw_ds(ibp) * 1e15
c1, c2 = 25.0, 120.0
vol1 = ing / c1
vol2 = ing / c2
vol2d = ing / (c2 / 10)
vecs = [('pUC19', 2686), ('pET-28a(+)', 5369), ('pcDNA3.1(+)', 5428), ('10 kb backbone', 10000)]
vec_rows = ''
for n, b in vecs:
    f = vng * 1e-9 / mw_ds(b) * 1e15
    vec_rows += f"| {n} | {b:,} bp | {f:.1f} fmol | {vng*ibp/b*r:.1f} ng |\n"

edit('biology/ligation-ratio', date=U, phrase='ligation calculator',
     intro=("Ligation joins an insert to a cut vector, and success depends on how many molecules of each are in the tube rather than on their masses. "
            "This ligation calculator works out how many nanograms of insert give a chosen insert to vector molar ratio, such as 3:1, from the two DNA lengths.\n\n"
            "Molecular biologists and students use it when setting up cloning reactions, so that short inserts are not starved and long inserts do not crowd out the vector."),
     body_add=f'''
## The same example in femtomoles

The defaults (50 ng of a {vbp:,} bp vector, a {ibp:,} bp insert, 3:1) give **{ing:.0f} ng of insert**. Equal masses can be a 3:1 molar ratio because the insert is a third the length. Using the double stranded DNA molar mass of 617.96 g/mol per base pair plus 36.04:

- Vector: 50 ng ÷ {mw_ds(vbp):,.0f} g/mol = **{v_fmol:.1f} fmol**
- Insert: {ing:.0f} ng ÷ {mw_ds(ibp):,.0f} g/mol = **{i_fmol:.1f} fmol**
- Ratio: {i_fmol:.1f} ÷ {v_fmol:.1f} = {i_fmol/v_fmol:.2f}

## Same insert, different vectors

For a 1,000 bp insert at 3:1 with 50 ng of vector, the insert mass falls as the vector gets longer, because 50 ng of a big plasmid is fewer molecules:

| Vector | Length | 50 ng is | Insert for 3:1 |
|---|---|---|---|
{vec_rows}
Use the length of the cut backbone that actually goes into the reaction. If a 600 bp stuffer fragment is removed during digestion, the backbone is shorter than the full plasmid map.

## Setting up the reaction

Convert the mass to a volume from the measured concentration. At {c1:g} ng/µL the {ing:.0f} ng of insert is {vol1:.1f} µL, an easy volume to pipette. At {c2:g} ng/µL it would be only {vol2:.2f} µL, so dilute the insert 1:10 first and add {vol2d:.1f} µL. A typical 20 µL T4 ligation then takes 2 µL of 10× buffer, the vector and insert, 1 µL of ligase and water to volume. Thaw the buffer on ice and mix it well, since its ATP and DTT settle out and break down with repeated thawing.

## Common mistakes

- **Using a 3:1 mass ratio.** Three times the vector mass is a 3:1 molar ratio only when the insert and vector are the same length.
- **Entering the uncut plasmid size.** Remove any fragment cut out during digestion from the vector length.
- **Trusting a UV reading of gel extracted DNA.** Guanidine salts and agarose absorb in the UV and can make concentrations look two or three times higher; check on a gel against a ladder.
- **Adding far too much DNA.** Above about 200 ng in 20 µL, inserts join into concatemers and multiple insert clones appear.
- **Skipping the vector only control.** Without it you cannot tell real recombinants from vector that recircularised.
''',
     faq_add=[('How do I convert ng of DNA to femtomoles?',
               'Divide the mass by the molar mass of the fragment, which is about 617.96 g/mol per base pair plus 36.04 for double stranded DNA. For example, 50 ng of a 3,000 bp vector is about 27 fmol.'),
              ('What insert to vector ratio is used for Gibson or HiFi assembly?',
               'These overlap assembly methods usually use about a 2:1 molar excess of each insert over the vector, rising to about 5:1 for fragments shorter than 200 bp.')])

# ---------------------------------------------------------------- Water heater time
V, t1, t2, P, ef = 25.0, 20.0, 55.0, 2.0, 0.9
cw = 4.186
kwh = V * cw * (t2 - t1) / 3600 / ef
tmin = kwh * 3600 / P / 60
# shower sizing
flow, dur, tmix, tcold = 8.0, 8.0, 40.0, 15.0
frac = (tmix - tcold) / (t2 - tcold)
hot_l = flow * dur * frac
# seasonal inlet table
sea_rows = ''
tariff = 8.0
for ti in (10, 15, 20, 25, 30):
    k = V * cw * (t2 - ti) / 3600 / ef
    sea_rows += f"| {ti} °C | {t2-ti:.0f} °C | {k:.2f} kWh | {k*3600/P/60:.0f} min | {k*tariff:.2f} |\n"
# voltage effect
Vn, Vlow = 230.0, 210.0
R = Vn ** 2 / (P * 1000)
Plow = Vlow ** 2 / R / 1000
tlow = kwh * 3600 / Plow / 60

edit('other/water-heater-time', date=U, phrase='water heater heating time calculator',
     intro=("An electric geyser heats water at a rate set by its element power, so the wait depends on how much water it holds and how far it must be warmed. "
            "This water heater heating time calculator finds the energy and the minutes needed from the tank volume, temperatures, element rating and efficiency.\n\n"
            "Households use it to plan when to switch the geyser on and what it costs, and electricians and plumbers use it to choose between tank sizes and element ratings."),
     body_add=f'''
## Reading the default result

The defaults (a {V:g} L tank from {t1:g} °C to {t2:g} °C, a {P:g} kW element, {ef*100:.0f}% efficiency) give **{kwh:.2f} kWh** and **{tmin:.1f} minutes**. The water itself needs {V:g} × {cw} × {t2-t1:g} ÷ 3,600 = {V*cw*(t2-t1)/3600:.3f} kWh, and the efficiency adds the heat lost from the tank and pipes during heating.

## Seasonal inlet temperature

Mains water is much colder in winter, which is why the same geyser seems slow in January. For the {V:g} L, {P:g} kW heater set to {t2:g} °C, at a tariff of {tariff:g} per kWh:

| Cold water | Rise | Energy | Time | Cost per heat up |
|---|---|---|---|---|
{sea_rows}
## Is the tank big enough for a shower?

Hot water from the tank is mixed with cold at the tap. A shower at {flow:g} L/min for {dur:g} minutes at {tmix:g} °C, with {t2:g} °C stored water and {tcold:g} °C cold water, needs a hot share of ({tmix:g} − {tcold:g}) ÷ ({t2:g} − {tcold:g}) = {frac*100:.1f}%, so it draws **{hot_l:.0f} L of hot water**. A {V:g} L tank runs short, and in practice only about 70 to 80% of a tank comes out hot before mixing with incoming cold water cools it. Either set the thermostat higher (with a mixing valve) or choose a larger tank.

## Low supply voltage

An element is a fixed resistance, so its power falls with the square of voltage. A {P:g} kW element rated at {Vn:.0f} V has R = {Vn:.0f}² ÷ {P*1000:.0f} = {R:.2f} Ω. At {Vlow:.0f} V it delivers only {Plow:.2f} kW, and the default heat up takes **{tlow:.1f} minutes** instead of {tmin:.1f}. The energy used barely changes; only the waiting time grows. To check the real power, switch off everything else and time the energy meter pulses with the [energy meter constant calculator](/electrical/energy-meter-constant/).

## Common mistakes

- **Using the summer inlet temperature all year.** A 10 °C winter supply needs {(t2-10)/(t2-t1)*100-100:.0f}% more energy than the default 20 °C.
- **Typing the element rating in watts.** 2000 entered as kW gives a time a thousand times too short.
- **Treating the whole tank as usable hot water.** Mixing with incoming cold water means only part of the volume comes out at full temperature.
- **Ignoring scale on the element.** In hard water areas a crusted element heats slowly and can burn out; descale or fit a softener.
- **Leaving the geyser on all day.** Standing losses continue whether or not water is used; a timer cuts them.
''',
     faq_add=[('Why does my geyser take longer to heat in winter?',
               f'The cold water is colder, so the temperature rise is bigger. Heating {V:g} L to {t2:g} °C from 10 °C instead of 20 °C takes about {V*cw*(t2-10)/3600/ef*3600/P/60:.0f} minutes instead of {tmin:.0f} with a {P:g} kW element.'),
              ('Does low voltage make a water heater slower?',
               f'Yes. Element power falls with the square of voltage, so a {P:g} kW, {Vn:.0f} V element gives about {Plow:.2f} kW at {Vlow:.0f} V and takes about {(P/Plow-1)*100:.0f}% longer, while using about the same energy.')])

# ---------------------------------------------------------------- SIP
M, rr, yrs = 5000.0, 0.12, 10


def fv(m, r, t):
    i = r / 12
    n = 12 * t
    return m * ((1 + i) ** n - 1) / i * (1 + i)


FV = fv(M, rr, yrs)
inv = M * 12 * yrs
gain = FV - inv
infl = 0.06
real = FV / (1 + infl) ** yrs
rate_rows = ''
for rp in (0.06, 0.08, 0.10, 0.12, 0.14):
    f = fv(M, rp, yrs)
    rate_rows += f"| {rp*100:.0f}% | {f:,.0f} | {f-inv:,.0f} | {f/inv:.2f}× |\n"
fv11 = fv(M, 0.11, yrs)
eff = (1 + rr / 12) ** 12 - 1
ltcg_ex = 125000
tax = (gain - ltcg_ex) * 0.125 * 1.04

edit_keep_featured('finance/sip', date=U, phrase='SIP calculator',
     intro=("A Systematic Investment Plan puts a fixed sum into a mutual fund every month, so each instalment buys units at that month's price and then compounds. "
            "This SIP calculator projects the future value, the total invested and the gain from the monthly amount, expected return and period.\n\n"
            "Salaried investors use it to set a monthly amount for goals such as a home deposit, education or retirement, and to see how much starting earlier helps."),
     body_add=f'''
## How sensitive the result is to the return

The default plan (5,000 a month for {yrs} years at 12%) grows to **{FV:,.0f}** from {inv:,.0f} invested, a gain of {gain:,.0f}. The return is the input you control least, so it is worth seeing the same plan at other rates:

| Annual return | Future value | Gain | Multiple of money invested |
|---|---|---|---|
{rate_rows}
Four percentage points of return separate a plan that grows modestly from one that nearly doubles your money. Use a conservative figure for planning and treat anything above it as a bonus.

## What the corpus is worth in today's money

At 6% inflation, {FV:,.0f} in {yrs} years buys what **{real:,.0f}** buys today, only a little more than the {inv:,.0f} you put in. Real growth is what matters for a goal, so inflate the goal amount first with the [inflation calculator](/finance/inflation/), then solve for the monthly SIP.

## Costs and tax in India

- **Expense ratio.** A regular plan often costs about 1% a year more than the direct plan of the same fund. At 11% instead of 12% the default plan ends at {fv11:,.0f}, {FV-fv11:,.0f} less.
- **Tax on equity funds.** Under the rates in force since July 2024, units held over 12 months are long term, with gains above 1.25 lakh a year taxed at 12.5%; units held 12 months or less are taxed at 20%. Each instalment has its own holding period, so in a redemption the most recent 12 instalments are still short term. If the whole gain of {gain:,.0f} were long term, the tax would be about {tax:,.0f} including 4% cess.
- **Debt funds** bought after 1 April 2023 are taxed at your slab rate whatever the holding period.

Check the current Budget for any change before redeeming a large amount.

## Common mistakes

- **Projecting a recent bull market return.** Trailing 3 year returns after a rally can be far above the long run average.
- **Reading the rate as an annual effective return.** The formula compounds 12% ÷ 12 each month, which is an effective {eff*100:.2f}% a year, so a fund's annual CAGR of 12% corresponds to a slightly lower monthly figure.
- **Judging a SIP by absolute return.** Money invested in the last few months has had little time to grow; compare SIPs by XIRR, which weights each instalment by its time in the market.
- **Forgetting the exit load.** Many equity funds charge about 1% on units redeemed within a year of purchase, which applies to each recent instalment.
''',
     faq_add=[('How are SIP returns measured, XIRR or CAGR?',
               'XIRR. A SIP has many cash flows at different dates, so a single CAGR from the first instalment overstates the time the money was invested. XIRR finds the one annual rate that matches every instalment and the final value.')])

print('done')

# ======================================================================= SECTION _expand_c4.py
"""Expand (2026-11-19), slice 4: emi, pond-liner, paper-weight-gsm, margin-of-error, scss.
Numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-19'


def inr(x):
    """Indian digit grouping, rounded to whole rupees."""
    s = str(int(round(abs(x))))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:]); head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ','.join(parts) + ',' + tail
    return ('-' if x < 0 else '') + '₹' + s


def edit_keep_featured(cid, **kw):
    """Lift the featured flag around the edit and restore it unchanged."""
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


# ---------------------------------------------------------------- EMI (Indian loans)
P, R, Y = 3000000.0, 0.085, 20
r = R / 12
n = Y * 12
E = P * r * (1 + r) ** n / ((1 + r) ** n - 1)


def schedule(P, r, E, months, extra=None):
    bal, rows = P, []
    for m in range(1, months + 1):
        i = bal * r
        pr = min(E - i, bal)
        bal -= pr
        if extra and m in extra:
            bal -= extra[m]
        rows.append((m, i, pr, max(bal, 0)))
        if bal <= 0.005:
            break
    return rows

sch = schedule(P, r, E, n)
yr_rows = ''
for yr in (1, 5, 10, 15, 20):
    seg = sch[(yr - 1) * 12: yr * 12]
    yi = sum(x[1] for x in seg); yp = sum(x[2] for x in seg)
    yr_rows += f"| Year {yr} | {inr(yi)} | {inr(yp)} | {yi/(yi+yp)*100:.0f}% | {inr(seg[-1][3])} |\n"
m1_i = P * r
m1_p = E - m1_i
# crossover month where principal part first exceeds interest part
cross = next(x[0] for x in sch if x[2] > x[1])

# rate reset after 36 EMIs: 8.5% to 9.0%
B36 = sch[35][3]
r2 = 0.09 / 12
left = n - 36
E_new = B36 * r2 * (1 + r2) ** left / ((1 + r2) ** left - 1)
m_new = -math.log(1 - B36 * r2 / E) / math.log(1 + r2)
int_A = E_new * left - B36
int_B = E * m_new - B36

# one-time prepayment of Rs 2 lakh after EMI 12, EMI kept
pre = 200000
sp = schedule(P, r, E, n, extra={12: pre})
months_sp = len(sp)
int_sp = sum(x[1] for x in sp)
int_base = E * n - P
saved = int_base - int_sp

# eligibility at 50% FOIR for net pay 1,00,000 with existing EMI 10,000
pay, other = 100000, 10000
afford = pay * 0.5 - other
loan_ok = afford * ((1 + r) ** n - 1) / (r * (1 + r) ** n)

edit_keep_featured('finance/emi', date=U, phrase='EMI calculator',
     intro=("An EMI (equated monthly instalment) is the fixed amount an Indian bank or NBFC debits every month until a home, car, personal or education loan and its interest are repaid. "
            "This EMI calculator gives the instalment, total interest and total payment from the loan amount, rate and tenure.\n\n"
            "Borrowers use it to compare offers and plan prepayments, and loan advisers use it to check how much EMI a salary can support before a bank sanctions the loan."),
     body_add=f'''
## Where each EMI goes: interest first, principal later

For the default {inr(P)} loan at {R*100:g}% over {Y} years the EMI is **{inr(E)}**. In the first month the interest is {inr(P)} × {R*100:g}% ÷ 12 = {inr(m1_i)}, so only {inr(m1_p)} of the EMI reduces the loan. The principal part overtakes the interest part only in month {cross}, more than {cross // 12} years in.

| Loan year | Interest paid | Principal repaid | Interest share | Balance at year end |
|---|---|---|---|---|
{yr_rows}
This is why a home loan statement after five years can still show most of the original amount outstanding, and why the interest certificate your bank issues each April is largest in the early years.

## When the repo rate moves: higher EMI or longer tenure

Most Indian home loans are floating and linked to an external benchmark such as the RBI repo rate, so the rate is reset when the benchmark changes. Suppose the rate rises from {R*100:g}% to 9.0% after 36 EMIs, when the balance is {inr(B36)}. The bank can do one of two things:

- **Raise the EMI** to {inr(E_new)} for the remaining {left} months. Extra interest over the rest of the loan: {inr(int_A - (E*left - B36))}.
- **Keep the EMI** at {inr(E)} and stretch the loan by {m_new - left:.0f} months. Extra interest: {inr(int_B - (E*left - B36))}.

Stretching the tenure costs more in total, yet many lenders default to it. RBI rules on resetting floating rate EMI loans require the lender to tell you about the reset and let you choose a higher EMI, a longer tenure or a mix of both, and to offer a switch to a fixed rate.

## A small prepayment early on

Floating rate loans taken by individuals carry no foreclosure or part prepayment charges. Paying {inr(pre)} once, just after the 12th EMI, while keeping the EMI unchanged, closes the loan in {months_sp} months instead of {n}, about {(n - months_sp)/12:.1f} years sooner, and saves **{inr(saved)}** of interest. The same amount paid in year 15 saves far less because little interest is left to avoid.

## How banks check what EMI you can afford

Lenders look at the fixed obligation to income ratio (FOIR): all EMIs, including the new one, as a share of net monthly income. Many cap it around 50% for salaried borrowers. With a take home pay of {inr(pay)} and an existing car EMI of {inr(other)}, a 50% FOIR leaves {inr(afford)} for the new EMI, which at {R*100:g}% over {Y} years supports a loan of about **{inr(loan_ok)}**. Your CIBIL score, age and employer category then decide the rate and the final sanction.

## Common mistakes

- **Comparing EMIs at different tenures.** A lower EMI over 25 years can cost lakhs more than a slightly higher EMI over 20; compare total interest instead.
- **Ignoring pre-EMI on an under-construction flat.** Until full disbursement you pay interest only on the amount released, and none of it reduces the principal.
- **Using the flat rate an NBFC or dealer quotes.** A "flat" 7% on a car loan charges interest on the original amount throughout and works out to about 12.5% on the reducing balance this calculator uses.
- **Forgetting loan insurance bundled into the amount.** A single premium policy added to the loan raises the EMI and is charged interest for the full term.
- **Not checking the reset after a rate hike.** If the bank silently extends the tenure, a loan can run past your retirement age; ask for the revised schedule.
''',
     faq_add=[('What happens to my EMI when the RBI repo rate changes?',
               f'For a floating rate loan the bank resets the rate, usually from the next quarter, and either changes the EMI or the tenure. On the default loan, a rise from 8.5% to 9.0% after 3 years lifts the EMI to about {inr(E_new)}, or keeps it at {inr(E)} and adds about {m_new - left:.0f} months.'),
              ('How much home loan can I get on my salary?',
               f'Banks usually allow total EMIs of about 50% of net monthly pay. With {inr(pay)} take home and no other loans, a {inr(pay*0.5)} EMI at 8.5% for 20 years supports a loan of about {inr(pay*0.5*((1+r)**n-1)/(r*(1+r)**n))}.')])

# ---------------------------------------------------------------- Pond liner
L, W, D, o = 3.0, 2.0, 0.6, 0.3
ll = L + 2 * D + 2 * o
lw = W + 2 * D + 2 * o
V = L * W * D * 0.6 * 1000
A_liner = ll * lw
A_pond = L * W
epdm_kg = A_liner * 1.02e-3 * 1150   # 1.02 mm (0.040 in) EPDM, about 1,150 kg/m3
hose = 15.0
fill_min = V / hose
fac_rows = ''
for f, kind in ((0.5, 'Saucer shape, gently sloping all round'), (0.6, 'Typical garden pond with one shelf'), (0.7, 'Steep sides, small marginal shelf'), (0.85, 'Near vertical walls (formal pond)')):
    fac_rows += f"| {f:g} | {kind} | {L*W*D*f*1000:,.0f} L |\n"
roll_rows = ''
for (pl, pw, pd) in ((2, 1.5, 0.45), (3, 2, 0.6), (4, 2.5, 0.75), (4, 3, 0.9), (6, 4, 1.2)):
    a, b = pl + 2 * pd + 2 * o, pw + 2 * pd + 2 * o
    roll_rows += f"| {pl:g} × {pw:g} × {pd:g} m | {a:.1f} × {b:.1f} m | {a*b:.1f} m² | {a*b*1.02e-3*1150:.0f} kg |\n"

edit('ecology/pond-liner', date=U, phrase='pond liner calculator',
     intro=("A flexible pond liner has to drape across the floor, run up both sides and still leave a flap to anchor under the edging, so it is always much bigger than the hole looks. "
            "This pond liner calculator adds twice the depth and twice the overlap to each dimension and estimates the water volume.\n\n"
            "Garden owners use it before ordering EPDM or PVC sheet, and pond builders use the volume to size pumps, filters and water treatment doses."),
     body_add=f'''
## Worked example: ordering for a 3 × 2 m pond

With the default inputs (length {L:g} m, width {W:g} m, maximum depth {D:g} m, overlap {o:g} m):

- Liner length = {L:g} + 2 × {D:g} + 2 × {o:g} = **{ll:.1f} m**
- Liner width = {W:g} + 2 × {D:g} + 2 × {o:g} = **{lw:.1f} m**
- Liner area = {ll:.1f} × {lw:.1f} = **{A_liner:.2f} m²**, about {A_liner/A_pond:.1f} times the {A_pond:g} m² water surface
- Water volume ≈ {L:g} × {W:g} × {D:g} × 0.6 = **{V:,.0f} litres**

A 1 mm EPDM sheet of that size weighs roughly {epdm_kg:.0f} kg, so two people are needed to lay it. Order the same size of underlay. Filling from a garden hose at about {hose:g} L/min takes around {fill_min:.0f} minutes.

## Measuring an irregular pond

Most ponds are kidney or free form rather than rectangles. Dig the hole first, then measure the liner rather than the plan:

1. Run a tape or string across the **longest** part of the hole, pushing it down so it follows the floor and both walls, and add twice the overlap. That is the liner length.
2. Repeat across the **widest** part at right angles for the liner width.
3. Use the deepest point for depth even if most of the pond is shallower; shelves do not change the liner size, because the sheet simply folds onto them.

For the volume of a free form pond, a more reliable figure comes from a water meter reading taken before and after filling.

## Volume factor by pond shape

The calculator uses 0.6 of the box volume. The right factor depends on how steep the sides are; for the default 3 × 2 × 0.6 m hole:

| Factor | Pond shape | Volume |
|---|---|---|
{fac_rows}
Use the measured or best estimated volume when dosing dechlorinator, salt or medicines, since an overdose based on the box volume can harm fish.

## Liner sizes and weights for common ponds

With a {o:g} m overlap and 1 mm EPDM:

| Pond (L × W × max depth) | Liner | Area | Approx. weight |
|---|---|---|---|
{roll_rows}
Liners are sold from standard roll widths, so round both dimensions up to the next size the supplier stocks rather than joining strips.

## Common mistakes

- **Adding the depth only once.** The sheet climbs both walls, so each dimension needs 2 × depth.
- **Skimping on overlap.** Less than about 0.3 m leaves too little to bury or trap under slabs, and the edge can slip in once the water weight pulls it down.
- **Measuring the flat plan of a sloped hole.** A tape laid across the top underestimates the length the liner has to follow; measure along the contour.
- **Filling before trimming.** Partly fill the pond first so the liner settles into folds, then trim the excess edge.
- **Leaving the liner exposed above water.** UV degrades PVC quickly; cover the top band with stones, soil or edging.
''',
     faq_add=[('How do I measure an irregular shaped pond for a liner?',
               'Lay a tape across the longest point of the dug hole so it follows the floor and both sides, then add twice the overlap; repeat across the widest point. Use those two figures as the liner size.'),
              ('How heavy is a pond liner?',
               f'A 1 mm EPDM liner weighs about 1.2 kg per square metre, so the {ll:.1f} × {lw:.1f} m sheet for a 3 × 2 × 0.6 m pond weighs roughly {epdm_kg:.0f} kg.')])

# ---------------------------------------------------------------- Paper weight (GSM)
area, gsm, ns = 0.06237, 80.0, 500
w1 = gsm * area
wt = w1 * ns / 1000
box = wt * 5
# booklet: 24 page A4 saddle stitched = 5 inner A3 sheets at 100 gsm + 1 cover A3 sheet at 250 gsm
A3 = 0.12474
inner = 5 * A3 * 100
cover = 1 * A3 * 250
book = inner + cover
run = 200
run_kg = book * run / 1000
# measuring gsm by weighing
m10 = 62.4
gsm_meas = m10 / (10 * area)
# caliper from bulk: office paper density about 0.8 g/cm3
dens = 0.8
cal_um = gsm / dens
ream_mm = cal_um * ns / 1000
ream_rows = ''
for g in (70, 75, 80, 90, 100, 120, 170, 300):
    ream_rows += f"| {g} | {g*area:.2f} g | {g*area*500/1000:.2f} kg | {g*A3*500/1000:.2f} kg | {g/dens:.0f} µm |\n"

edit('other/paper-weight-gsm', date=U, phrase='paper weight calculator',
     intro=("GSM, or grams per square metre, is the mass of one square metre of a paper or board, so the weight of any sheet is simply its area times its GSM. "
            "This paper weight calculator gives the weight of one sheet and of a stack for A and US sizes.\n\n"
            "Printers use it to estimate job weights and paper orders, while offices and online sellers use it to work out postage and courier charges before packing."),
     body_add=f'''
## Worked example: a ream and a carton

The default inputs are a ream of {ns} A4 sheets ({area} m² each) at {gsm:g} GSM:

- One sheet: {gsm:g} × {area} = **{w1:.2f} g**
- One ream: {w1:.4f} × {ns} ÷ 1000 = **{wt:.3f} kg**
- A carton of 5 reams: {box:.2f} kg of paper, plus about 0.5 kg for the wrappers and box

## Worked example: weight of a printed booklet

A 24 page A4 saddle stitched booklet is printed on A3 sheets folded in half. Each A3 sheet gives 4 pages, so it needs 6 sheets: 5 inner sheets on 100 GSM and 1 cover sheet on 250 GSM.

- Inner: 5 × {A3} × 100 = {inner:.1f} g
- Cover: 1 × {A3} × 250 = {cover:.1f} g
- One booklet: **{book:.1f} g**, so a run of {run} weighs {run_kg:.1f} kg before packing

Count leaves (sheets), not pages: one A4 leaf printed both sides carries 2 pages.

## Finding the GSM of an unknown paper

Weigh 10 sheets on a kitchen or postal scale and divide by the total area. If 10 A4 sheets weigh {m10} g, the paper is {m10} ÷ (10 × {area}) = **{gsm_meas:.0f} GSM**. Weighing 10 or more sheets keeps the 1 g resolution of a cheap scale from spoiling the result.

GSM is not thickness. Thickness (caliper) also depends on how dense the paper is: uncoated office paper is around {dens} g/cm³, so 80 GSM is roughly {cal_um:.0f} µm thick and a ream stands about {ream_mm:.0f} mm tall, while a glossy coated paper of the same GSM is thinner and feels lighter in the hand.

## Weight table for common GSM values

| GSM | A4 sheet | A4 ream (500) | A3 ream (500) | Typical caliper |
|---|---|---|---|---|
{ream_rows}
Caliper assumes {dens} g/cm³; coated papers and boards vary, so check the mill data sheet.

## Common mistakes

- **Treating US "lb" as GSM.** 20 lb bond and 80 lb text are basis weights of a ream in different base sizes; 20 lb bond is about 75 GSM, not 20.
- **Counting pages instead of sheets.** A 100 page document printed double sided uses 50 sheets.
- **Forgetting the cover stock.** Cards and covers at 250 to 350 GSM can weigh as much as several inner sheets.
- **Ignoring packaging.** Envelopes, wrappers and cartons often push a parcel into the next postage band.
- **Expecting exact figures.** Mills allow a GSM tolerance of a few percent, and paper gains weight in humid storage.
''',
     faq_add=[('How can I find the GSM of paper without the packaging?',
               f'Weigh 10 sheets and divide by their total area in square metres. Ten A4 sheets weighing {m10} g give {m10} ÷ 0.6237 = {gsm_meas:.0f} GSM.'),
              ('Is higher GSM paper always thicker?',
               'Usually, but not exactly. Thickness depends on density too, so a coated 100 GSM paper can be thinner than an uncoated 90 GSM bond.')])

# ---------------------------------------------------------------- Margin of error
z95, z90, z99 = 1.959964, 1.644854, 2.575829
nn, p0 = 1000, 0.50
E0 = z95 * math.sqrt(p0 * (1 - p0) / nn)
cl_rows = ''
for lab, z in (('90%', z90), ('95%', z95), ('99%', z99)):
    row = [z * math.sqrt(0.25 / k) * 100 for k in (400, 1000, 2500)]
    cl_rows += f"| {lab} | {z:.3f} | ±{row[0]:.1f}% | ±{row[1]:.1f}% | ±{row[2]:.1f}% |\n"
# lead between two candidates in one poll
p1, p2 = 0.48, 0.45
E_lead = z95 * math.sqrt((p1 + p2 - (p1 - p2) ** 2) / nn)
# subgroup
nsub = 150
E_sub = z95 * math.sqrt(0.25 / nsub)
# design effect from weighting
deff = 1.5
neff = nn / deff
E_deff = z95 * math.sqrt(0.25 / neff)
# rare proportion, small sample: Wald vs Wilson
ns_, ps_ = 100, 0.03
E_wald = z95 * math.sqrt(ps_ * (1 - ps_) / ns_)
zz = z95 ** 2
cen = (ps_ + zz / (2 * ns_)) / (1 + zz / ns_)
half = z95 * math.sqrt(ps_ * (1 - ps_) / ns_ + zz / (4 * ns_ ** 2)) / (1 + zz / ns_)
wl, wu = cen - half, cen + half

edit('statistics/margin-of-error', date=U, phrase='margin of error calculator',
     intro=("The margin of error is the plus or minus figure attached to a survey result: the range around the sample percentage that should contain the true population value at a chosen confidence level. "
            "This margin of error calculator uses z × √(p(1 − p) ÷ n) for a proportion.\n\n"
            "Pollsters, market researchers and students use it to report results honestly and to judge whether a gap between two figures is real or just sampling noise."),
     body_add=f'''
## How the default result is built

The calculator starts at 95% confidence (z = {z95}), n = {nn:,} and p = {p0*100:.0f}%:

- Standard error = √({p0} × {1-p0} ÷ {nn:,}) = {math.sqrt(p0*(1-p0)/nn):.5f}
- Margin = {z95} × {math.sqrt(p0*(1-p0)/nn):.5f} = **±{E0*100:.2f} percentage points**

So a reported 50% means roughly {p0*100-E0*100:.1f}% to {p0*100+E0*100:.1f}%.

## Worked example: the lead and a subgroup

Back to the poll with 48% for A and 45% for B among the same {nn:,} people. The margin on the 3 point lead is not ±3.1 but z × √((p₁ + p₂ − (p₁ − p₂)²) ÷ n) = {z95:.2f} × √(({p1} + {p2} − {p1-p2:.2f}²) ÷ {nn:,}) = **±{E_lead*100:.1f} points**. The lead could be anything from about {(p1-p2-E_lead)*100:.0f} to +{(p1-p2+E_lead)*100:.0f} points.

If the same poll breaks out the {nsub} respondents aged 18 to 24, their margin is {z95:.2f} × √(0.25 ÷ {nsub}) = **±{E_sub*100:.1f} points**, so subgroup findings need far more caution than the headline.

## Confidence level and sample size together

Margin at p = 50%:

| Confidence | z | n = 400 | n = 1,000 | n = 2,500 |
|---|---|---|---|---|
{cl_rows}
Moving from 95% to 99% confidence widens the margin by about a third at any sample size.

## Weighting and the design effect

Real polls are weighted so the sample matches the population by age, sex, region and so on. Weighting makes the estimate less precise, measured by the design effect. With a design effect of {deff}, the {nn:,} interviews behave like {neff:.0f} simple random ones and the margin grows to **±{E_deff*100:.1f} points**. Reputable pollsters publish this adjusted margin; you can reproduce it here by entering n ÷ design effect as the sample size.

## Rare outcomes and small samples

The formula is a normal approximation and breaks down when n × p is below about 10. For {ps_*100:.0f}% in a sample of {ns_}, it gives ±{E_wald*100:.1f} points, implying a lower limit of {(ps_-E_wald)*100:.1f}%, which is impossible. The Wilson score interval gives {wl*100:.1f}% to {wu*100:.1f}% instead, lopsided because the true value cannot go below zero. Use the [confidence interval calculator](/statistics/confidence-interval/) or an exact method for such cases.

## Common mistakes

- **Applying the single margin to a lead.** The gap between two candidates in one poll has a margin close to double the headline figure.
- **Quoting the full sample margin for a subgroup.** Margins depend on the subgroup's own n.
- **Mixing percent and percentage points.** ±3% on a 40% result means 37% to 43%, not 38.8% to 41.2%.
- **Ignoring weighting.** An unweighted margin overstates the precision of a weighted poll.
- **Using it on opt-in online panels.** Without random selection there is no sampling distribution, so a margin of error is not strictly meaningful.
''',
     faq_add=[('How do I calculate the margin of error on the lead between two candidates?',
               f'Within one poll use z × √((p1 + p2 − (p1 − p2)²) ÷ n). For 48% vs 45% with n = 1,000 at 95% confidence that is about ±{E_lead*100:.1f} points, nearly twice the ±3.1 headline margin.'),
              ('What is a design effect in polling?',
               f'It is the loss of precision caused by weighting or clustering. Divide the sample size by the design effect to get the effective sample; a design effect of 1.5 turns 1,000 interviews into about 667 and raises the margin to ±{E_deff*100:.1f} points.')])

# ---------------------------------------------------------------- SCSS
Pd, rs = 1500000.0, 0.082
qi = Pd * rs / 4
mi = qi / 3
yi = qi * 4
ti = yi * 5
days = 52   # deposit on 10 November, first credit on 1 January covers 10 Nov to 31 Dec
first = Pd * rs * days / 365
tds_lim = 100000
tds = 0.10 * yi
p_lim = tds_lim / rs
reinv = (1 + rs / 4) ** 4 - 1
tax_rows = ''
for slab in (0, 0.05, 0.20, 0.30):
    tax = yi * slab * 1.04
    tax_rows += f"| {slab*100:.0f}% | {inr(yi)} | {inr(tax)} | {inr(yi - tax)} | {(yi-tax)/Pd*100:.2f}% |\n"
pen_rows = ''
for lab, pct in (('After 1 year, before 2 years', 0.015), ('After 2 years, before 5 years', 0.01)):
    pen_rows += f"| {lab} | {pct*100:g}% | {inr(Pd*pct)} | {inr(Pd*(1-pct))} |\n"

edit('finance/scss', date=U, phrase='SCSS calculator',
     intro=("The Senior Citizens Savings Scheme (SCSS) is a government backed five year deposit sold through post offices and authorised banks that pays a fixed rate of simple interest every quarter. "
            "This SCSS calculator gives the quarterly, monthly equivalent, yearly and five year interest on a deposit.\n\n"
            "Retirees and their families use it to plan a steady income from a gratuity or provident fund payout and to compare SCSS with bank FDs and the Post Office MIS."),
     body_add=f'''
## Worked example: ₹15 lakh at {rs*100:g}%

With the default deposit of {inr(Pd)}:

- Quarterly interest = {inr(Pd)} × {rs*100:g}% ÷ 4 = **{inr(qi)}**
- Monthly equivalent = {inr(qi)} ÷ 3 = **{inr(mi)}**
- Yearly interest = **{inr(yi)}**, and over 5 years **{inr(ti)}**, with the full {inr(Pd)} returned at maturity

The first credit is usually smaller. A deposit made on 10 November earns interest only from that date to 31 December, about {inr(Pd)} × {rs*100:g}% × {days} ÷ 365 = {inr(first)}, paid on 1 January. Full quarterly credits follow on the first working day of each April, July, October and January.

## Tax and TDS on SCSS interest

SCSS interest is fully taxable at your slab rate. Tax is deducted at source at 10% once the year's interest from the account exceeds the senior citizen threshold of {inr(tds_lim)}. The default deposit earns {inr(yi)} a year, so about {inr(tds)} would be deducted unless you submit Form 15H, which you can do only if your total tax for the year is nil. To keep a single account below the threshold, the deposit must not exceed about {inr(p_lim)} at {rs*100:g}%.

Take home income on the default deposit (tax including 4% cess, ignoring other income and deductions):

| Your slab rate | Yearly interest | Tax | Net income | Net yield |
|---|---|---|---|---|
{tax_rows}
Under the old regime, the deposit itself can be claimed in the ₹1.5 lakh investment deduction and senior citizens can deduct up to ₹50,000 of deposit interest. The new regime allows neither, but its rebate means many retirees with modest total income pay no tax anyway.

## Getting the most from the scheme

- **Split between spouses.** Each spouse aged 60 or more can hold their own account up to ₹30 lakh, doubling the family limit to ₹60 lakh.
- **Reinvest the interest.** SCSS pays simple interest. If each quarterly credit is reinvested at the same rate, the effective yield rises to about {reinv*100:.2f}% a year.
- **Lock in a high rate.** The rate on the date of deposit stays fixed for the whole 5 years, even if later quarters announce a lower rate.
- **Extend on maturity.** The account can be extended in blocks of 3 years at the rate ruling on the maturity date; apply within a year of maturity.

## Premature closure on a {inr(Pd)} deposit

| Closure | Deduction | Amount deducted | Paid out |
|---|---|---|---|
{pen_rows}
Closing before 1 year means any interest already paid is recovered from the deposit. Closure on the holder's death carries no penalty.

## Common mistakes

- **Treating the monthly figure as a monthly payout.** SCSS pays every quarter; the monthly equivalent is only for budgeting.
- **Assuming interest compounds.** Unclaimed quarterly interest earns nothing extra, so link a savings account for automatic credit.
- **Forgetting Form 15H.** Without it, eligible retirees with nil tax still lose 10% to TDS and must claim a refund.
- **Depositing more than ₹30 lakh across banks.** The limit covers all SCSS accounts a person holds together, and the excess is refunded without SCSS interest.
- **Missing the retirement window.** Retirees aged 55 to 60 must invest within three months of receiving their retirement benefits.
''',
     faq_add=[('How much can I deposit in SCSS to avoid TDS?',
               f'TDS applies when interest from the account exceeds {inr(tds_lim)} in a year. At {rs*100:g}% that is a deposit of about {inr(p_lim)}. Above that, submit Form 15H if your total tax is nil.'),
              ('When is the first SCSS interest paid?',
               f'On the first working day of the next quarter (1 April, 1 July, 1 October or 1 January), covering only the days since the deposit. A {inr(Pd)} deposit on 10 November gets about {inr(first)} on 1 January.')])

print('done')

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-19), slice 5: hra-exemption, induction-motor-slip, transformer-efficiency,
rebar-weight (featured, flag kept), commission. Numbers computed here from each page's default inputs.
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-19'


def edit_keep_featured(cid, **kw):
    """Lift the featured flag around the edit and restore it unchanged."""
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


def inr(x):
    """Indian digit grouping, e.g. 1234567 -> 12,34,567."""
    s = f"{round(x):d}"
    neg = s.startswith('-')
    s = s.lstrip('-')
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ','.join(parts) + ',' + tail
    return ('-' if neg else '') + s


def hra(B, H, R, m):
    return max(0, min(H, R - 0.1 * B, m * B))

# ---------------------------------------------------------------- HRA exemption
B, H, R = 600000, 240000, 240000
E0 = hra(B, H, R, 0.5)
# higher salary, high rent: where the 50% vs 40% limit binds
B2, H2, R2 = 1200000, 600000, 660000
E2_40 = hra(B2, H2, R2, 0.4)
E2_50 = hra(B2, H2, R2, 0.5)
gain = E2_50 - E2_40
save30 = gain * 0.30 * 1.04
# mid-year move: 5 months non-metro at 15k rent, 7 months metro at 30k rent, basic 60k/month, HRA 25k/month
bm, hm = 50000, 25000
p1 = hra(bm * 5, hm * 5, 15000 * 5, 0.4)
p2 = hra(bm * 7, hm * 7, 30000 * 7, 0.5)
# salary structure table: rent 40,000 a month, HRA = 50% of basic
hra_rows = ''
for b in (300000, 600000, 900000, 1200000, 1800000):
    h = 0.5 * b
    r = 480000
    e50, e40 = hra(b, h, r, 0.5), hra(b, h, r, 0.4)
    hra_rows += f"| ₹{inr(b)} | ₹{inr(h)} | ₹{inr(e50)} | ₹{inr(e40)} |\n"

edit('finance/hra-exemption', date=U, phrase='HRA exemption calculator',
     description='Work out the tax-exempt part of your house rent allowance under the old regime, with the 50% limit for eight metro cities and 40% elsewhere.',
     intro=("House Rent Allowance paid by an employer is partly tax-free under the old tax regime, and the exempt part is the lowest of three limits set by salary, rent and city. "
            "This HRA exemption calculator finds the exempt and taxable HRA and solves for whichever value you leave blank.\n\n"
            "Salaried employees use it before choosing a regime and submitting rent proofs, and payroll teams use it to set monthly TDS."),
     faq_replace=[('Which cities count as metro for HRA?', 'Which cities get the 50% HRA limit?',
                   'From tax year 2026-27 (1 April 2026), the Income-tax Rules 2026 give the 50% limit to eight cities: Delhi, Mumbai, Kolkata, Chennai, Bengaluru, Hyderabad, Pune and Ahmedabad. Every other city uses 40%. Choose the Metro option for any of the eight.')],
     body_add=f'''
## Which cities use the 50% limit from 2026-27

Until 31 March 2026 only Delhi, Mumbai, Kolkata and Chennai counted as metros for HRA. The Income-tax Act 2025 and the Income-tax Rules 2026, which apply from 1 April 2026, extend the 50% limit to **Bengaluru, Hyderabad, Pune and Ahmedabad** as well. The Metro option in the calculator applies the 50% limit, so select it if you live in any of these eight cities, even though the option label names only the original four. The exemption is still available only under the old regime; the new regime, which is the default, gives no HRA exemption at all.

## Worked example: when the city limit decides the answer

With the default inputs the city does not matter: rent minus 10% of basic (₹{inr(R)} minus ₹{inr(0.1*B)} = ₹{inr(E0)}) is the lowest limit, in a metro or not. The city limit bites only when rent is high compared with salary. Take a Pune employee with basic + DA of ₹{inr(B2)}, HRA of ₹{inr(H2)} and rent of ₹{inr(R2/12)} a month (₹{inr(R2)} a year):

1. Actual HRA = ₹{inr(H2)}
2. Rent minus 10% of basic = {inr(R2)} minus {inr(0.1*B2)} = ₹{inr(R2-0.1*B2)}
3. City limit = 40% of basic = ₹{inr(0.4*B2)} (up to 2025-26), or 50% = ₹{inr(0.5*B2)} (from 2026-27)

The exempt HRA rises from **₹{inr(E2_40)}** to **₹{inr(E2_50)}**, so ₹{inr(gain)} less salary is taxed. In the 30% slab with 4% cess that saves about **₹{inr(save30)}** a year.

## Exemption by salary level

Rent fixed at ₹40,000 a month (₹4,80,000 a year), with HRA at 50% of basic, a common structure in large cities:

| Basic + DA (year) | HRA received | Exempt, 50% city | Exempt, 40% city |
|---|---|---|---|
{hra_rows}
At lower salaries the HRA or the city limit is the cap, so a 40% city exempts less. As salary rises, the 10% of basic taken off the rent grows until rent minus 10% becomes the lowest limit, and from there the city no longer matters.

## Changing city or rent during the year

The rule is applied month by month, so split the year at the change and add the parts. An employee on ₹{inr(bm)} basic and ₹{inr(hm)} HRA a month pays ₹15,000 rent for 5 months in a 40% city, then ₹30,000 for 7 months in a 50% city. The first period gives ₹{inr(p1)} exempt and the second ₹{inr(p2)}, a total of **₹{inr(p1+p2)}**. Running the whole year with the later rent and city would overstate it.

## Common mistakes

- **Claiming HRA in the new regime.** It is not allowed there; compare both regimes first with the [income tax calculator](/finance/income-tax-india/).
- **Using gross salary instead of basic + DA.** Only basic pay and dearness allowance that counts for retirement benefits go into the 10% and 40% or 50% limits.
- **Including months with no rent.** Months spent in your own house or with no rent paid earn no exemption, even if HRA was received.
- **Paying rent to a spouse.** Tax officers routinely reject it; rent to parents is accepted only when they own the house and declare the income, and the 2026 rules ask you to disclose your relationship with the landlord.
- **Submitting proofs late.** If your employer has no rent proof by the cut-off, TDS is deducted on the full HRA and you must claim the exemption in your return.
''',
     faq_add=[('Does the 50% HRA limit for Bengaluru and Pune apply to 2025-26?',
               'No. The four new cities get 50% only from 1 April 2026 (tax year 2026-27). For salary up to 31 March 2026, Bengaluru, Hyderabad, Pune and Ahmedabad still use the 40% limit.')])

# ---------------------------------------------------------------- Induction motor slip
f, P, Nr = 50.0, 4, 1460.0
Ns = 120 * f / P
s = (Ns - Nr) / Ns
fr = s * f
slip_rpm = Ns - Nr
kw = 7.5
T = 9549.3 * kw / Nr
s80 = s / 0.8 ** 2
N80 = Ns * (1 - s80)
vfd_rows = ''
for fq in (10, 20, 25, 35, 50, 60):
    ns = 120 * fq / P
    n = ns - slip_rpm
    vfd_rows += f"| {fq} Hz | {ns:,.0f} rpm | {n:,.0f} rpm | {slip_rpm/ns*100:.2f}% | {slip_rpm*P/120:.2f} Hz |\n"
# MCSA sidebands for broken rotor bars
sb_lo, sb_hi = (1 - 2 * s) * f, (1 + 2 * s) * f

edit('electrical/induction-motor-slip', date=U, phrase='induction motor slip calculator',
     intro=("An induction motor always turns a little slower than its rotating magnetic field, and that difference, called slip, is what induces rotor current and torque. "
            "This induction motor slip calculator gives synchronous speed, slip and rotor frequency. See [induction motor slip explained](https://www.instrumentationblog.in/induction-motor-slip-explained/).\n\n"
            "Electricians use it to read nameplates and identify pole numbers, and maintenance engineers use it to judge motor load and diagnose rotor faults."),
     replace=[("- **Reading speed under a VFD without the output frequency.** Use the drive's output frequency, not the 50 or 60 Hz mains, to work out N<sub>s</sub>.",
               "- **Reading speed under a VFD without the output frequency.** Use the drive's output frequency, not the 50 or 60 Hz mains, to work out N<sub>s</sub>.\n"
               "- **Rounding the measured speed.** At 1,460 rpm a 5 rpm reading error changes the slip by 12.5% of its value, so use a tachometer that resolves 1 rpm.")],
     body_add=f'''
## Slip and rotor frequency on a VFD

A drive changes the synchronous speed, but at the same load torque the motor keeps roughly the same slip in rpm. For the default motor ({slip_rpm:.0f} rpm slip at rated torque), the table shows why slip as a percentage climbs at low frequency while the rotor frequency stays put:

| Drive output | N<sub>s</sub> | Shaft speed | Slip | Rotor frequency |
|---|---|---|---|---|
{vfd_rows}
At 10 Hz the same {slip_rpm:.0f} rpm is a {slip_rpm/(120*10/P)*100:.1f}% slip. This is why sensorless drives use slip compensation: without it a conveyor set for 10 Hz runs noticeably slower than 300 rpm under load.

## Measuring slip in the field

- **Optical tachometer.** Stick reflective tape on the shaft or coupling and read the speed directly. Accuracy of 1 rpm is enough for load estimates.
- **Stroboscope.** Set it to the synchronous flash rate ({Ns:,.0f} per minute here); the mark appears to drift backwards at the slip speed, {slip_rpm:.0f} rpm.
- **Current signature.** A spectrum of one phase current shows broken bar sidebands at (1 ± 2s) × f, which for the default motor are **{sb_lo:.2f} Hz** and **{sb_hi:.2f} Hz** either side of 50 Hz. The spacing itself gives the slip without touching the shaft.
- **Search coil.** A coil held near the motor end picks up the rotor frequency, here {fr:.2f} Hz; counting its beats over a minute gives slip directly.

## Slip, torque and voltage

In the normal running range torque is nearly proportional to slip. A {kw:g} kW version of the default motor delivers T = 9,549 × {kw:g} ÷ {Nr:,.0f} = **{T:.1f} N·m** at {s*100:.2f}% slip, so half that torque needs roughly half the slip. Slip also rises as voltage falls, roughly with 1 ÷ V². At 80% voltage the same load pushes slip to about {s80*100:.2f}% and speed down to {N80:,.0f} rpm, and the extra rotor current raises the winding temperature.
''',
     faq_add=[('What is the rotor frequency when the motor starts?',
               'At standstill the slip is 1 (100%), so the rotor frequency equals the supply frequency, 50 Hz on a 50 Hz supply. It falls to the small running value, 1.33 Hz for a 4-pole motor at 1,460 rpm, as the motor reaches speed.')])

# ---------------------------------------------------------------- Transformer efficiency
S, x, pf, Pi, Pc = 1000.0, 0.75, 0.9, 1.4, 9.5
Po = x * S * pf
Pl = Pi + x ** 2 * Pc
eff = Po / (Po + Pl)
xm = math.sqrt(Pi / Pc)
Pom = xm * S * pf
effm = Pom / (Pom + 2 * Pi)
# all-day efficiency for a daily profile, PF 0.9
prof = [(6, 0.20), (10, 0.75), (6, 0.50), (2, 1.00)]
out_kwh = sum(h * xx * S * pf for h, xx in prof)
cu_kwh = sum(h * xx ** 2 * Pc for h, xx in prof)
core_kwh = 24 * Pi
eff_day = out_kwh / (out_kwh + cu_kwh + core_kwh)
prof_rows = ''.join(f"| {h} h | {xx*100:.0f}% | {h*xx*S*pf:,.0f} kWh | {h*xx**2*Pc:.2f} kWh |\n" for h, xx in prof)
# annual loss cost at Rs 8 per kWh
tariff = 8.0
yr_core = core_kwh * 365
yr_cu = cu_kwh * 365
cost_core = yr_core * tariff
cost_cu = yr_cu * tariff
# low-loss amorphous alternative: 0.5 kW core loss
Pi2 = 0.5
save_kwh = (Pi - Pi2) * 8760
eff2 = Po / (Po + Pi2 + x ** 2 * Pc)

edit('electrical/transformer-efficiency', date=U, phrase='transformer efficiency calculator',
     intro=("A transformer wastes a small, fixed core (iron) loss whenever it is energised and a copper loss that grows with the square of load. "
            "This transformer efficiency calculator gives the efficiency at any load and power factor and the load at which efficiency peaks. See this [transformer efficiency calculation](https://www.instrumentationblog.in/transformer-efficiency-calculation/) guide.\n\n"
            "Utility and plant engineers use it to compare tender offers, check loading and estimate the yearly cost of losses."),
     body_add=f'''
## Worked example with the default values

A {S:,.0f} kVA transformer with {Pi:g} kW no-load loss and {Pc:g} kW full-load copper loss runs at {x*100:.0f}% load and PF {pf}:

- Output = {x:g} × {S:,.0f} × {pf} = **{Po:,.0f} kW**
- Losses = {Pi:g} + {x:g}² × {Pc:g} = {Pi:g} + {x**2*Pc:.4f} = **{Pl:.4f} kW**
- Efficiency = {Po:,.0f} ÷ ({Po:,.0f} + {Pl:.4f}) = **{eff*100:.2f}%**
- Maximum efficiency at x = √({Pi:g} ÷ {Pc:g}) = **{xm*100:.1f}%** load, where it reaches {effm*100:.2f}% at PF {pf}

## Worked example: all-day efficiency for a daily load profile

The same unit feeds a plant whose load follows this pattern each day at PF {pf}:

| Hours | Load | Energy delivered | Copper loss energy |
|---|---|---|---|
{prof_rows}
Delivered energy is {out_kwh:,.0f} kWh, copper loss is {cu_kwh:.2f} kWh and core loss is 24 × {Pi:g} = {core_kwh:.1f} kWh. The all-day efficiency is {out_kwh:,.0f} ÷ ({out_kwh:,.0f} + {cu_kwh:.2f} + {core_kwh:.1f}) = **{eff_day*100:.2f}%**. Over a year at ₹{tariff:g} per kWh the core loss costs about ₹{inr(cost_core)} and the copper loss about ₹{inr(cost_cu)}.

## How the losses are measured

The two loss figures come from routine factory tests to IEC 60076-1 or IS 2026. The **open circuit test** energises one winding at rated voltage with the other open; the input power is the core loss. The **short circuit test** shorts one winding and raises the voltage on the other until rated current flows; the input power, corrected to 75 °C reference temperature, is the full-load copper loss. Both values are printed on the test certificate, and tender specifications cap them with penalties for any excess.

## Choosing a lower loss design

For a lightly loaded or always energised unit, core loss matters most. An amorphous core version with {Pi2:g} kW no-load loss would save {save_kwh:,.0f} kWh a year, and its efficiency at the default load rises to {eff2*100:.2f}%. Buyers compare offers by capitalising each kW of no-load and load loss at a rupee value per kW and adding it to the price.

## Common mistakes

- **Using kVA as output power.** Output in kW is kVA × load × PF; a low power factor lowers efficiency even when the losses stay the same.
- **Scaling copper loss linearly.** Load loss follows the square of current, so at half load it is a quarter of the full-load figure, not half.
- **Forgetting that core loss never stops.** An energised transformer on no load is 0% efficient, still drawing {Pi:g} kW.
- **Taking copper loss at ambient temperature.** Winding resistance rises about 0.4% per °C; use the 75 °C corrected figure.
- **Entering losses in watts with the kW unit selected.** A 1,400 W core loss entered as 1,400 kW gives a nonsense efficiency.
''',
     faq_add=[('How are no-load and full-load losses measured?',
               'No-load (core) loss comes from the open circuit test at rated voltage and frequency. Full-load (copper) loss comes from the short circuit test at rated current, corrected to 75 °C. Both are on the factory test certificate.'),
              ('What is all-day efficiency?',
               'The ratio of energy delivered to energy input over 24 hours. It counts core loss for every hour and copper loss at each actual load, so it suits distribution transformers that run lightly loaded for much of the day.')])

# ---------------------------------------------------------------- Rebar weight
d, L, n = 12, 12.0, 10
wpm = d ** 2 / 162.2
W = wpm * L * n
# slab mesh: 4 m x 5 m slab, 10 mm bars at 150 mm both ways, 25 mm cover
Lx, Ly, sp, cov, db = 4.0, 5.0, 0.150, 0.025, 10
nx = math.floor((Ly - 2 * cov) / sp) + 1   # bars running along x, spaced over y
ny = math.floor((Lx - 2 * cov) / sp) + 1
lx = Lx - 2 * cov
ly = Ly - 2 * cov
tot_len = nx * lx + ny * ly
w10 = db ** 2 / 162.2
mesh_w = tot_len * w10
mesh_w_total = mesh_w * 1.05
# lap: 50 d on a 16 mm bar
lap16 = 50 * 16 / 1000
lapw = lap16 * 16 ** 2 / 162.2
# weight check rows: nominal and IS 1786 batch tolerance
tol = {8: 7, 10: 7, 12: 5, 16: 5, 20: 3, 25: 3, 32: 3}
chk_rows = ''
for dd, t in tol.items():
    w = dd ** 2 / 162.2
    chk_rows += f"| {dd} mm | {w:.3f} | ±{t}% | {w*(1-t/100):.3f} to {w*(1+t/100):.3f} |\n"
# sample check: 12 mm, 1 m piece weighs 0.842 kg
samp = 0.842
dev = (samp - wpm) / wpm * 100

edit_keep_featured('construction/rebar-weight', date=U, phrase='rebar weight calculator',
     intro=("Reinforcement steel is bought and billed by weight, but drawings give bar diameters, lengths and counts. "
            "This rebar weight calculator converts them using the standard D² ÷ 162.2 kg per metre rule, which follows from steel's density of 7,850 kg/m³.\n\n"
            "Site engineers and quantity surveyors use it to prepare bar bending schedules and orders, and contractors use it to check deliveries and bills."),
     body_add=f'''
## Worked example: steel for a slab mesh

A 4 m × 5 m slab has 10 mm bars at 150 mm spacing in both directions with 25 mm end cover. Bars along the 4 m side are spaced over the 5 m width: ({Ly:g} − 0.05) ÷ 0.15 + 1 = **{nx} bars** of {lx:.2f} m. Bars along the 5 m side number ({Lx:g} − 0.05) ÷ 0.15 + 1 = **{ny} bars** of {ly:.2f} m. The total length is {nx} × {lx:.2f} + {ny} × {ly:.2f} = {tot_len:.2f} m, and at {w10:.3f} kg/m the mesh weighs **{mesh_w:.1f} kg**. Adding 5% for bends, chairs and offcuts brings the order to about {mesh_w_total:.0f} kg. Laps add more where bars must be joined: a 50 d lap on a 16 mm bar is {lap16:.2f} m, or {lapw:.2f} kg of extra steel at every joint.

## Checking delivered bars by weight

Mills roll bars to a nominal mass, and IS 1786 allows a batch tolerance on mass per metre. A quick site check is to cut a 1 m piece, weigh it and compare:

| Bar | Nominal kg/m | Batch tolerance | Acceptable kg/m |
|---|---|---|---|
{chk_rows}
For example, a 1 m piece of 12 mm bar weighing {samp} kg is {dev:.1f}% below the nominal {wpm:.3f} kg/m, outside the 5% band, so the batch should be rejected or billed by actual weight. Underweight bars also mean less steel area in the structure.

## Weight by the bundle

The default inputs, 10 bars of 12 mm at 12 m each, give **{W:.1f} kg**. Steel is often priced per tonne, so divide by 1,000 and multiply by the rate. Suppliers may bill on theoretical weight (this formula) or on weighbridge weight; agree which in the order.

## Common mistakes

- **Putting the diameter in cm or inches.** The 162.2 divisor needs millimetres; 1.2 entered for 12 mm gives a weight 100 times too small.
- **Using 162 for big orders.** The rounded divisor overstates the weight by about 0.1%, which is around 1 kg per tonne; small, but worth noting on large bills.
- **Ignoring laps and hooks.** Standard hooks and bends add length beyond the clear span; take cutting lengths from the bar bending schedule.
- **Counting bars as span ÷ spacing.** You need one more bar than the number of gaps.
- **Measuring over the ribs.** TMT bars are sold by nominal diameter; calipers over the ribs read larger and overestimate weight.
''',
     faq_add=[('How do I check if TMT bars are underweight?',
               'Cut a 1 m sample, weigh it and compare with d² ÷ 162.2. IS 1786 batch tolerance is about ±7% up to 10 mm, ±5% for 12 and 16 mm and ±3% above 16 mm. A 12 mm bar should weigh 0.844 to 0.932 kg per metre.')])

# ---------------------------------------------------------------- Commission
S, r, B = 50000.0, 0.05, 2000.0
C = S * r
T = B + C
target = 6000.0
S_need = (target - B) / r
# retroactive vs marginal tier at 80,000: 5% to 50k, 8% above
s2 = 80000.0
marg = 50000 * 0.05 + (s2 - 50000) * 0.08
retro = s2 * 0.08
# commission on margin: sale 50,000, cost 35,000, 20% of margin
margin = S - 35000
cm = margin * 0.20
# discounting: 10% discount at 30% gross margin
need_rows = ''
for rr in (0.02, 0.03, 0.05, 0.08, 0.10, 0.15):
    need_rows += f"| {rr*100:g}% | {(3000)/rr:,.0f} | {(5000)/rr:,.0f} | {(10000)/rr:,.0f} |\n"
# GST: invoice 59,000 incl 18% GST
inv = 59000.0
base_ex = inv / 1.18

edit('finance/commission', date=U, phrase='commission calculator',
     intro=("Sales commission is the share of sales value paid to the person who closed the deal, either as a flat percentage or in tiers that rise with volume. "
            "This commission calculator gives the commission and total pay from sales, rate and base pay, or the sales needed for an earnings target.\n\n"
            "Salespeople use it to plan targets and check payslips, and managers and business owners use it to design and cost incentive plans."),
     body_add=f'''
## Worked example with the default values

Sales of {S:,.0f} at a {r*100:g}% rate with a base of {B:,.0f} for the period:

- Commission = {S:,.0f} × {r:g} = **{C:,.0f}**
- Total earnings = {B:,.0f} + {C:,.0f} = **{T:,.0f}**

To earn {target:,.0f} in total with the same base and rate, the commission must cover {target-B:,.0f}, so sales must reach {target-B:,.0f} ÷ {r:g} = **{S_need:,.0f}**. Enter {target:,.0f} as total earnings and press × on sales amount to get the same answer.

## Sales needed for a commission target

| Rate | For 3,000 commission | For 5,000 | For 10,000 |
|---|---|---|---|
{need_rows}
At low rates the required sales climb steeply, which is why low-rate plans such as property or wholesale usually come with a base salary.

## Marginal versus retroactive tiers

Plans with tiers work in one of two ways, and the difference is large. On {s2:,.0f} of sales with 5% up to 50,000 and 8% above:

- **Marginal (step) tier:** 5% on the first 50,000 and 8% on the next 30,000 = **{marg:,.0f}**.
- **Retroactive tier:** once sales pass 50,000 the 8% applies to everything, {s2:,.0f} × 8% = **{retro:,.0f}**.

A retroactive plan creates a sharp jump at the threshold, so a sale that crosses it can be worth far more than its own value. Read the plan document to see which rule applies.

## When commission is earned and paid

Most plans pay on invoiced sales, but many pay only once the customer has paid, and some claw back commission on returns or cancellations. On a GST invoice, commission is normally calculated on the value before tax: an invoice of {inv:,.0f} including 18% GST has a taxable value of {base_ex:,.0f}, so 5% commission is {base_ex*0.05:,.0f}, not {inv*0.05:,.0f}. Commission on gross margin is another variant: a {S:,.0f} sale costing 35,000 leaves {margin:,.0f} of margin, and 20% of that pays {cm:,.0f}.

## Common mistakes

- **Entering 5 instead of 5%.** The rate field is a percentage; a rate typed as a decimal elsewhere must be converted.
- **Applying the top tier to all sales.** Unless the plan says retroactive, only the sales above the threshold earn the higher rate.
- **Including tax in the sales figure.** Use the net sale value excluding GST or sales tax unless the plan says otherwise.
- **Ignoring returns.** Commission paid on cancelled orders is usually recovered from later pay.
- **Comparing plans on rate alone.** A 3% plan on large invoices with a base salary can pay more than 10% on small ones.
''',
     faq_add=[('What is the difference between a marginal and a retroactive commission tier?',
               f'In a marginal tier the higher rate applies only to sales above the threshold. In a retroactive tier it applies to all sales once the threshold is passed. On 80,000 of sales with 5% to 50,000 and 8% above, that is {marg:,.0f} versus {retro:,.0f}.'),
              ('Is commission calculated before or after GST?',
               'Normally before. Commission is paid on the taxable value of the sale, so divide a GST-inclusive amount by 1.18 (for 18% GST) before applying the rate.')])

print('done', inplace.DONE)

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-19), slice 6: nps, debt-to-income, guntha-to-sq-ft, steel-plate-weight,
heat-conduction. Numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-19'


def inr(x):
    """Indian digit grouping, rounded to whole rupees."""
    s = str(int(round(x)))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ','.join(parts) + ',' + tail


# ---------------------------------------------------------------- NPS
def corpus(M, A, r):
    i, n = r / 12, 12 * (60 - A)
    return M * ((1 + i) ** n - 1) / i * (1 + i)


M0, A0, r0, a0, ar0 = 5000, 30, 0.10, 0.20, 0.06
F0 = corpus(M0, A0, r0)
P0 = a0 * F0 * ar0 / 12
ret_rows = ''
for r in (0.08, 0.09, 0.10, 0.11, 0.12):
    f = corpus(M0, A0, r)
    ret_rows += f"| {r*100:.0f}% | ₹{inr(f)} | ₹{inr(0.8*f)} | ₹{inr(0.2*f*ar0/12)} |\n"
sh_rows = ''
for a in (0.2, 0.4, 0.6, 1.0):
    sh_rows += f"| {a*100:.0f}% | ₹{inr((1-a)*F0)} | ₹{inr(a*F0)} | ₹{inr(a*F0*ar0/12)} |\n"
infl = 0.06
P0_today = P0 / (1 + infl) ** 30
F0_today = F0 / (1 + infl) ** 30
# contribution needed for a 50,000 pension with 40% annuity at 6%
target = 50000
F_need40 = target * 12 / (0.4 * ar0)
fac = corpus(1, A0, r0)
M_need40 = F_need40 / fac
F_need20 = target * 12 / (0.2 * ar0)
M_need20 = F_need20 / fac
tax_saved = 50000 * 0.312

edit('finance/nps', date=U, phrase='NPS calculator',
     intro=("The National Pension System (NPS) is a market-linked retirement scheme regulated by PFRDA. Contributions grow until age 60, when part of the corpus can be withdrawn and the rest must buy an annuity. "
            "This NPS calculator estimates the corpus, the lump sum and the monthly pension.\n\n"
            "Salaried employees and self-employed savers use it to choose a monthly contribution, test return assumptions and see how the annuity share changes the pension before they commit."),
     body_add=f'''
## How the return assumption changes the result

The default plan (₹{inr(M0)} a month from age {A0}, 20% annuity at 6%) is very sensitive to the yearly return, because the money compounds for 30 years:

| Return | Corpus at 60 | 80% lump sum | Pension from 20% |
|---|---|---|---|
{ret_rows}
Two percentage points either side of 10% cuts the corpus by about a third or raises it by more than half. A mix with 50% equity has historically earned less than an equity-heavy mix, so pick the return that matches your asset allocation rather than the best past figure.

## Lump sum or bigger pension

The same ₹{inr(F0)} corpus can be split in different ways at exit:

| Annuity share | Lump sum | Annuity purchase | Monthly pension at 6% |
|---|---|---|---|
{sh_rows}
Putting more into the annuity gives a steady income for life but locks the money in; the lump sum can be invested in a [systematic withdrawal plan](/finance/swp/) instead.

## Reading the result in today's money

All figures are in rupees of the year you retire. At 6% inflation, the ₹{inr(P0)} monthly pension in the default example buys what about **₹{inr(P0_today)}** buys today, and the ₹{inr(F0)} corpus is worth about ₹{inr(F0_today)} in today's terms. That is why the contribution usually needs to rise with salary; check a step-up plan with the [retirement corpus calculator](/finance/retirement-corpus/).

## Working back from a target pension

For a ₹{inr(target)} monthly pension with 40% of the corpus in a 6% annuity, the corpus must be ₹{inr(target)} × 12 ÷ (0.40 × 0.06) = **₹{inr(F_need40)}**. Starting at {A0} with a 10% return, that needs about **₹{inr(M_need40)} a month**. With only the 20% minimum annuity the corpus must double to ₹{inr(F_need20)}, or ₹{inr(M_need20)} a month.

## Tax benefit in practice

Under the old tax regime, ₹50,000 a year put into NPS under section 80CCD(1B), over and above the 80C limit, saves ₹{inr(tax_saved)} for someone in the 30% slab (31.2% with cess). Under the new regime only the employer's contribution under 80CCD(2) is deductible, so ask your employer about routing part of the salary into NPS.

## Common mistakes

- **Treating the annuity rate as fixed.** The 6% default is today's level; the rate you get depends on interest rates in the year you retire.
- **Forgetting inflation.** A pension that looks comfortable in future rupees can be modest in today's money.
- **Assuming the whole lump sum is tax-free.** Up to 60% of the corpus is tax-free; check the tax treatment of any amount above that.
- **Using an equity return with Auto choice.** Auto choice cuts equity steadily after age 35, so the average return over the plan is lower than a pure equity figure.
- **Missing the minimum contribution.** A Tier I account needs at least ₹1,000 a year to stay active.
''',
     faq_add=[('How much should I invest in NPS for a ₹50,000 monthly pension?',
               f'From age 30 at a 10% return, with 40% of the corpus in a 6% annuity, you need a corpus of about ₹{inr(F_need40)}, which takes roughly ₹{inr(M_need40)} a month. With only the 20% minimum annuity the monthly amount doubles.'),
              ('What happens if I miss a year of NPS contributions?',
               'A Tier I account that receives less than ₹1,000 in a financial year becomes inactive (frozen). It is reactivated by paying the minimum amount for the missed years plus a small penalty; the money already invested keeps earning returns meanwhile.')])

# ---------------------------------------------------------------- Debt-to-income
debt, inc = 1500.0, 6000.0
dti = debt / inc
room = 0.36 * inc - debt
mort, car, card = 1100.0, 280.0, 120.0
assert mort + car + card == debt
front = mort / inc
newcar = 450.0
dti_new = (debt + newcar) / inc
room43 = 0.43 * inc - debt
lim_rows = ''
for g in (3000, 5000, 8000, 12000):
    lim_rows += f"| {g:,} | {0.28*g:,.0f} | {0.36*g:,.0f} | {0.43*g:,.0f} | {0.50*g:,.0f} |\n"
# FOIR (India)
gross_in, net_in, emis = 100000, 82000, 15000
foir_now = emis / net_in
cap = 0.50 * net_in
emi_room = cap - emis
i_m, n_m = 0.085 / 12, 240
loan = emi_room * (1 - (1 + i_m) ** -n_m) / i_m

edit('finance/debt-to-income', date=U, phrase='debt-to-income ratio calculator',
     intro=("The debt-to-income ratio (DTI) is the share of your gross monthly income that goes to fixed debt payments such as loan EMIs, car loans and minimum card dues. "
            "This debt-to-income ratio calculator gives the ratio and the payment room left below the common 36% limit.\n\n"
            "Home buyers and loan applicants use it to see how a lender will judge them, and Indian borrowers apply the same arithmetic to take-home pay as FOIR."),
     body_add=f'''
## Worked example: front-end ratio and a new car loan

The default 1,500 of monthly debt is made up of a {mort:,.0f} mortgage payment, a {car:,.0f} car loan and a {card:,.0f} minimum card payment, against 6,000 of gross income:

- Back-end DTI = 1,500 ÷ 6,000 = **{dti*100:.0f}%**
- Front-end (housing) ratio = {mort:,.0f} ÷ 6,000 = **{front*100:.1f}%**, inside the 28% guideline
- Adding a second car loan of {newcar:,.0f} a month raises DTI to {debt+newcar:,.0f} ÷ 6,000 = **{dti_new*100:.1f}%**, still under 36%
- The most a lender capping at 43% would allow in new payments is 0.43 × 6,000 − 1,500 = **{room43:,.0f} a month**

## Maximum total debt payment by income

Monthly payment ceilings for common lender limits (any currency):

| Gross monthly income | 28% | 36% | 43% | 50% |
|---|---|---|---|---|
{lim_rows}
Subtract what you already pay to see the room for a new loan.

## FOIR on take-home pay: an Indian home loan

Indian lenders apply FOIR to net salary after tax and PF. Take a gross salary of ₹{inr(gross_in)} with a take-home of ₹{inr(net_in)} and existing EMIs of ₹{inr(emis)}:

- Current FOIR = {inr(emis)} ÷ {inr(net_in)} = **{foir_now*100:.1f}%**
- At a 50% FOIR cap the total EMI allowed is ₹{inr(cap)}, leaving **₹{inr(emi_room)}** for a new EMI
- At 8.5% for 20 years that EMI supports a home loan of about **₹{inr(loan)}**

Closing the ₹{inr(emis)} of existing EMIs before applying would add roughly ₹{inr(emis*(1-(1+i_m)**-n_m)/i_m)} to the eligible loan.

## What lenders actually count

Lenders work from your credit report and payslips or tax returns. Every EMI and credit card on the report counts, including loans you have guaranteed or co-signed. For self-employed applicants and bonus-heavy salaries they average income over two years, so a single strong year rarely raises eligibility on its own.

## Common mistakes

- **Mixing gross and net income.** US style DTI uses gross pay, while Indian FOIR uses take-home pay; the same debts give a higher FOIR than DTI.
- **Leaving out small or shared debts.** Minimum card payments, buy now pay later plans and co-signed loans all appear on the credit report.
- **Adding living costs.** Groceries, utilities and insurance premiums are not debt payments and do not belong in the ratio.
- **Forgetting the new loan.** The ratio a lender checks includes the EMI of the loan you are applying for.
- **Using one month of variable income.** Commission or freelance income is usually averaged, so use a 12 to 24 month average.
''',
     faq_add=[('Does my debt-to-income ratio affect my credit score?',
               'No. Credit bureaus do not record your income, so DTI is not part of the score. Lenders calculate it separately, while the score looks at repayment history, credit utilisation and similar factors.')])

# ---------------------------------------------------------------- Guntha to sq ft
SQFT, M2_FT2 = 1089.0, 0.09290304
g_m2 = SQFT * M2_FT2
ac, gu = 2, 15
tot_g = ac * 40 + gu
tot_ft = tot_g * SQFT
tot_m2 = tot_ft * M2_FT2
plot_ft = 3000
plot_g = plot_ft / SQFT
L_m, W_m = 40.0, 25.3
rect_g = L_m * W_m / g_m2
ha_g = 10000 / g_m2
are_rows = ''
for g in (1, 5, 10, 20, 40):
    are_rows += f"| {g} | {g*g_m2:,.2f} m² | {g*g_m2/100:.3f} are | {g*g_m2/10000:.4f} ha |\n"
round_err = (1 - 1000 / SQFT) * 100

edit('conversion/guntha-to-sq-ft', date=U, phrase='guntha to sq ft calculator',
     intro=("The guntha (or gunta) is a traditional land unit of Maharashtra, Karnataka, Telangana and Gujarat equal to 1,089 sq ft, and 40 gunthas make one acre. "
            "This guntha to sq ft calculator converts guntha to square feet, square metres, acres and hectares in either direction.\n\n"
            "Farmers, plot buyers and property agents use it to compare land records written in guntha with listings and layout plans quoted in square feet or square metres."),
     body_add=f'''
## Worked example: acres and gunthas on a land record

Land records often write area as acres plus gunthas, for example **{ac} acres {gu} guntha**:

- Total gunthas = {ac} × 40 + {gu} = **{tot_g} guntha**
- Square feet = {tot_g} × 1,089 = **{tot_ft:,.0f} sq ft**
- Square metres = {tot_ft:,.0f} × 0.09290304 = **{tot_m2:,.1f} m²**, or {tot_m2/10000:.4f} ha

Going the other way, a {plot_ft:,} sq ft house plot is {plot_ft:,} ÷ 1,089 = **{plot_g:.3f} guntha**.

## Guntha, are and hectare

Revenue records in Maharashtra and Karnataka increasingly show area in hectares and ares, so it helps to know how close the two systems are:

| Guntha | Square metres | Ares | Hectares |
|---|---|---|---|
{are_rows}
One guntha is {g_m2:.2f} m², about 1.2% more than one are, and one hectare is {ha_g:.2f} guntha.

## Measuring a plot in practice

Government surveyors now measure in metres with a total station or GPS rover, and the area is converted to guntha or hectares for the record. A rectangular plot of {L_m:g} m × {W_m:g} m covers {L_m*W_m:,.0f} m², which is {rect_g:.2f} guntha. Irregular plots are split into triangles, each worked out from its three sides, and the parts added. Before a sale, compare the measured area with the record and the layout plan; small differences of a few square metres are common, but a gap of a guntha or more needs a fresh survey.

## Common mistakes

- **Reading 1 acre 20 guntha as 1.2 acres.** Gunthas are fortieths of an acre, so 20 guntha is half an acre and the total is 1.5 acres.
- **Treating a guntha as 1,000 sq ft.** The shortcut understates the area by {round_err:.1f}%, which matters when land is priced per square foot.
- **Mixing up guntha and are.** They are close but not equal: 1 guntha is 101.17 m² and 1 are is exactly 100 m².
- **Confusing guntha with the Tamil Nadu ground.** A ground is 2,400 sq ft, more than twice a guntha.
- **Using square yards and square feet interchangeably.** One guntha is 121 sq yd (gaj) but 1,089 sq ft; a factor of 9 separates them.
''',
     faq_add=[('Is 1 acre 20 guntha the same as 1.2 acres?',
               'No. There are 40 guntha in an acre, so 20 guntha is 0.5 acre and 1 acre 20 guntha is 1.5 acres, or 65,340 sq ft.'),
              ('How many guntha are in one hectare?',
               f'About {ha_g:.2f} guntha. One hectare is 10,000 m² and one guntha is {g_m2:.2f} m².')])

# ---------------------------------------------------------------- Steel plate weight
rho = 7850.0
Wd = 2.0 * 1.0 * 0.006 * rho
# cut list: base plate 400 x 400 x 20 with four 22 mm holes, four 150 x 150 x 10 triangular gussets
bp = 0.4 * 0.4 * 0.020 * rho
hole = math.pi * 0.011 ** 2 * 0.020 * rho
bp_net = bp - 4 * hole
gus = 0.5 * 0.15 * 0.15 * 0.010 * rho
tot = bp_net + 4 * gus
ss_bp = 0.4 * 0.4 * 0.020 * 8000
sizes = [(1.25, 2.5), (1.5, 3.0), (2.0, 6.0)]
sz_rows = ''
for t in (3, 6, 10, 12, 20):
    sz_rows += f"| {t} mm | " + ' | '.join(f"{a*b*t/1000*rho:,.1f} kg" for a, b in sizes) + ' |\n'
lbft3 = rho / 16.018463
lb_ft2_in = lbft3 / 12
sheet48 = 1.25 * 2.5 * 0.003 * rho

edit('construction/steel-plate-weight', date=U, phrase='steel plate weight calculator',
     intro=("A steel plate's weight is its length × width × thickness multiplied by the material density, 7,850 kg/m³ for mild steel. "
            "This steel plate weight calculator also covers stainless steel, aluminium, copper and brass, and multiplies by the number of identical plates.\n\n"
            "Fabricators, estimators and purchase teams use it to price plate sold by weight, plan crane lifts and transport loads, and check invoices billed on theoretical weight."),
     body_add=f'''
## Worked example: a column base cut list

The default plate, 2,000 × 1,000 × 6 mm in mild steel, weighs 2 × 1 × 0.006 × 7,850 = **{Wd:.1f} kg**. A real job usually mixes sizes and shapes, for example one column base:

- Base plate 400 × 400 × 20 mm: 0.4 × 0.4 × 0.02 × 7,850 = {bp:.2f} kg
- Four 22 mm bolt holes: each removes π × 0.011² × 0.02 × 7,850 = {hole:.3f} kg, so the net plate is **{bp_net:.2f} kg**
- Four triangular gussets 150 × 150 × 10 mm: half of a 150 × 150 rectangle, {gus:.3f} kg each
- Assembly total = {bp_net:.2f} + 4 × {gus:.3f} = **{tot:.2f} kg**

For a triangle, enter the rectangle that encloses it and halve the answer. Made in stainless steel (8,000 kg/m³) the same base plate would weigh {ss_bp:.1f} kg before holes.

## Weight of standard plate sizes (mild steel)

| Thickness | 1,250 × 2,500 mm | 1,500 × 3,000 mm | 2,000 × 6,000 mm |
|---|---|---|---|
{sz_rows}
Use these to check that a delivery or a crane lift is in the right range before looking at the paperwork.

## Theoretical and actual weight

Mills and stockists usually invoice plate on theoretical weight from the nominal thickness, but rolled plate has a thickness tolerance (set by standards such as IS 2062 and EN 10029) and is often slightly over nominal, so a weighbridge figure can be a few percent higher. For lifting, add the weight of slings, shackles and any lifting beam to the plate weight. For costing a cut part, the bought weight is the whole rectangle the part is nested in, not the finished shape, so add the offcut or scrap allowance.

## Common mistakes

- **Mixing millimetres and metres.** Multiplying 2,000 × 1,000 × 6 by 7,850 gives a number a billion times too large; convert to metres first.
- **Using the steel density for other metals.** Aluminium is about a third as heavy and copper about 14% heavier than mild steel.
- **Forgetting the quantity.** A cut list of 24 identical plates needs n = 24, not a single plate weight.
- **Ignoring holes and cut-outs on thick plate.** On 20 mm plate a few large holes can remove several kilograms.
- **Taking chequer plate at its nominal thickness.** The raised pattern adds weight; use the supplier's kg/m² figure.
''',
     faq_add=[('How much does steel plate weigh per square foot?',
               f'Mild steel at 7,850 kg/m³ is {lbft3:.1f} lb/ft³, so plate weighs about {lb_ft2_in:.2f} lb per square foot for each inch of thickness, or {lb_ft2_in/4:.2f} lb/ft² for 1/4 inch plate.'),
              ('What does a 1,250 × 2,500 × 3 mm steel sheet weigh?',
               f'About {sheet48:.1f} kg: 1.25 × 2.5 × 0.003 × 7,850. The same sheet in aluminium is about {1.25*2.5*0.003*2700:.1f} kg.')])

# ---------------------------------------------------------------- Heat conduction
k, A, dT, d = 0.04, 10.0, 20.0, 0.1
Q = k * A * dT / d
Qt = 40.0
d_need = k * A * dT / Qt
# cold store wall
kc, Ac, dTc, dc = 0.023, 50.0, 55.0, 0.1
Qc = kc * Ac * dTc / dc
Ec = Qc * 24 / 1000
dc2 = 0.15
Qc2 = kc * Ac * dTc / dc2
# doubling insulation with surface resistances
Rs = 0.13 + 0.04
U1 = 1 / (Rs + d / k)
U2 = 1 / (Rs + 2 * d / k)
red = (1 - U2 / U1) * 100
th_rows = ''
for mm in (25, 50, 100, 150, 200, 300):
    dd = mm / 1000
    th_rows += f"| {mm} mm | {k*A*dT/dd:,.1f} W | {k/dd:.3f} | {1/(Rs+dd/k):.3f} | {k*A*dT/dd*24/1000:.2f} kWh |\n"

edit('physics/heat-conduction', date=U, phrase='heat conduction calculator',
     intro=("Heat conduction is the flow of heat through a solid from its hot face to its cold face, at a rate set by thermal conductivity, area, temperature difference and thickness. "
            "This heat conduction calculator applies Fourier's law to give heat flow, heat flux, U-value, R-value and energy per day. "
            "See [what thermal conductivity is](https://www.instrumentationblog.in/what-is-thermal-conductivity/).\n\n"
            "Building engineers and insulation contractors use it to size insulation, and process engineers use it on tank, oven and [heat exchanger](https://www.instrumentationblog.in/types-of-heat-exchangers/) walls."),
     body_add=f'''
## Effect of insulation thickness

For the default case (k = {k} W/m·K, {A:g} m², {dT:g} K difference), heat flow falls in proportion to thickness, but the real U-value including the inside and outside surface resistances ({Rs:.2f} m²·K/W) falls a little more slowly:

| Thickness | Heat flow | U of layer (W/m²·K) | U with surfaces | Energy per day |
|---|---|---|---|---|
{th_rows}
Beyond about 200 mm each extra centimetre saves only a small amount, which is where the cost of insulation starts to outweigh the energy saved.

## Solving for thickness: a cold store wall

Leave the thickness blank to size insulation for a heat flow limit. Keeping the default panel to {Qt:g} W needs d = k A ΔT ÷ Q = {k} × {A:g} × {dT:g} ÷ {Qt:g} = **{d_need*1000:.0f} mm**. For a cold room held at −20 °C with 35 °C outside (ΔT = {dTc:g} K), a {Ac:g} m² wall of 100 mm PIR panel (k = {kc}) conducts {kc} × {Ac:g} × {dTc:g} ÷ 0.1 = **{Qc:,.1f} W**, or {Ec:.1f} kWh of heat a day that the refrigeration plant must remove. Moving to 150 mm panel cuts this to {Qc2:,.1f} W.

## Measuring thermal conductivity and U-value

Conductivity of insulation is measured on flat samples between a hot and a cold plate: the guarded hot plate method (ISO 8302) and the faster heat flow meter apparatus (ISO 8301, ASTM C518). Transient hot wire probes suit liquids, powders and quick checks. On a finished building, the in-situ U-value is measured with a heat flux sensor fixed to the inside surface and thermocouples on both faces, logged over at least 72 hours to average out the thermal mass (ISO 9869).

## Common mistakes

- **Adding U-values of layers.** Layers in series add their R-values; U is the inverse of the total R, never the sum of the U-values.
- **Using dry catalogue k for wet insulation.** Water conducts about 20 times better than still air, so damp mineral wool or ice in a cold store panel can raise heat flow sharply.
- **Leaving out thermal bridges.** Studs, steel fixings and slab edges carry heat around the insulation and can add 10% to 30% to the real U-value.
- **Taking the temperature difference from air temperatures without surface resistances.** With air temperatures on each side, include the surface films, or the heat flow is overstated.
- **Converting ΔT as if it were a temperature.** A 20 °C difference is 20 K, not 293 K, and 36 °F rather than 68 °F; only the difference enters Fourier's law.
''',
     faq_add=[('Does doubling insulation thickness halve the heat loss?',
               f'For the layer alone, yes. Including the surface resistances of a wall, doubling 100 mm of k = 0.04 insulation cuts the U-value from {U1:.3f} to {U2:.3f} W/m²·K, a {red:.1f}% reduction. Around pipes the gain is smaller because the outer area grows with radius.')])

print('done')

# ---------------------------------------------------------------- Fix found while checking defaults (t9)
# The old debt-to-income worked example said 2,160 - 1,500 = 540; the calculator (and arithmetic) gives 660.
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'content', 'calculators', 'finance', 'debt-to-income.mdx')
_s = open(_p).read()
_a = '2,160 − 1,500 = **540 a month**'
assert _s.count(_a) == 1
open(_p, 'w').write(_s.replace(_a, '2,160 − 1,500 = **660 a month**'))
print('dti fix done')
