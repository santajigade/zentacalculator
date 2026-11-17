"""Part C expansion (2026-11-17): 32 priority pages (crawled, not indexed) brought to the api-gravity standard. Assembled from seven sections; edits are applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Part C expand (2026-11-17), slice 1: ntc-thermistor, compound-interest, ohms-law, weir-flow,
stock-average, transformer-current. Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-17'
pi = math.pi


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
    # put it back right after the updated: line, where it sat originally (after updated)
    k = t.index('\nupdated: ')
    k = t.index('\n', k + 1) + 1
    open(path, 'w').write(t[:k] + line + t[k:])
    return n


# ---------------------------------------------------------------- NTC thermistor
R25, B, T = 10.0, 3950.0, 60.0
TK = T + 273.15
RT = R25 * math.exp(B * (1 / TK - 1 / 298.15))
alp = -B / TK ** 2 * 100
Rmeas = 4.0
Tm = 1 / (1 / 298.15 + math.log(Rmeas / R25) / B) - 273.15
# divider: 10k fixed to ground, NTC to 3.3 V, Vout across fixed resistor
Vcc, Rf = 3.3, 10.0
div_rows = ''
for tc in (0, 25, 40, 60, 80, 100):
    r = R25 * math.exp(B * (1 / (tc + 273.15) - 1 / 298.15))
    v = Vcc * Rf / (Rf + r)
    cnt = round(v / Vcc * 4095)
    div_rows += f"| {tc} °C | {r:.2f} kΩ | {v:.3f} V | {cnt:,} |\n"
# self heating: dissipation constant 1.5 mW/°C typical bead
I_sh = 3.3 / (Rf + RT)  # mA (kohm)
P_sh = I_sh ** 2 * RT  # mW
dT_sh = P_sh / 1.5
# beta mismatch error: B 3950 vs 3435 at 60 °C
R3435 = R25 * math.exp(3435 * (1 / TK - 1 / 298.15))
Tmis = 1 / (1 / 298.15 + math.log(R3435 / R25) / 3950) - 273.15

edit('electronics/ntc-thermistor', date=U, phrase='NTC thermistor calculator',
     intro=("An NTC thermistor is a resistor whose value falls sharply as it warms, so it makes a cheap and sensitive temperature sensor. "
            "This NTC thermistor calculator uses the beta equation and the datasheet R25 and B values to convert temperature to resistance and back.\n\n"
            "Electronics designers, HVAC technicians and 3D printer builders use it to choose divider resistors and set firmware lookup tables. "
            "See [NTC and PTC thermistor working](https://www.instrumentationblog.in/ntc-ptc-thermistor-working/)."),
     body_add=f'''
## Worked example: 10 kΩ, B 3950 thermistor at 60 °C

With the default inputs (R25 = {R25:g} kΩ, B = {B:,.0f} K, T = {T:g} °C):

- T = {T:g} + 273.15 = **{TK:.2f} K**
- 1/T − 1/298.15 = {1/TK:.6f} − {1/298.15:.6f} = {1/TK-1/298.15:.6f} K⁻¹
- R = {R25:g} × e^({B:,.0f} × {1/TK-1/298.15:.6f}) = {R25:g} × {math.exp(B*(1/TK-1/298.15)):.4f} = **{RT:.2f} kΩ**
- Sensitivity = −{B:,.0f} ÷ {TK:.2f}² × 100 = **{alp:.2f} %/°C**

Going the other way, a reading of {Rmeas:g} kΩ gives T = 1 ÷ (1/298.15 + ln({Rmeas:g}/{R25:g}) ÷ {B:,.0f}) − 273.15 = **{Tm:.1f} °C**.

## Divider output with a 10 kΩ fixed resistor and a 12 bit ADC

With the thermistor from 3.3 V to the ADC pin and a 10 kΩ resistor from the pin to ground, V = 3.3 × 10 ÷ (10 + R<sub>T</sub>):

| Temperature | R<sub>T</sub> | ADC pin voltage | 12 bit count |
|---|---|---|---|
{div_rows}
The counts change fastest near 25 °C, where the two resistors are equal. If the range of interest is 60 to 100 °C, a smaller fixed resistor (around 2.2 kΩ) puts the steepest part of the curve where it is needed.

## Self-heating in practice

At {T:g} °C the example divider passes {I_sh*1000:.0f} µA and the thermistor dissipates {P_sh:.3f} mW. With a typical bead dissipation constant of 1.5 mW/°C, that warms the sensor by about **{dT_sh:.2f} °C** above the air it is measuring. In still air or with a lower value thermistor this error grows quickly, so firmware often powers the divider only while sampling.

## Common mistakes

- **Using the wrong B value.** B25/50 and B25/85 differ by 1 to 2%. Reading a {3435:,} K part as {B:,.0f} K turns a true {T:g} °C into an indicated {Tmis:.1f} °C.
- **Forgetting kelvin.** The exponent needs absolute temperature; plugging in °C gives nonsense.
- **Trusting the beta model far from 25 °C.** Beyond about 0 to 100 °C, fit Steinhart-Hart coefficients or use the maker's R-T table.
- **Ignoring lead and connector resistance.** It is small next to 10 kΩ at room temperature, but at 125 °C the thermistor is only a few hundred ohms.
- **Mounting without thermal contact.** A thermistor taped loosely to a heatsink reads the air gap, not the metal. Use thermal paste or a lug.
''',
     faq_add=[('What value of fixed resistor should I pair with an NTC thermistor?',
               'Choose a resistor equal to the thermistor resistance at the middle of the range you care about. For a 10 kΩ, B 3950 part read around 60 °C that is about 2.5 kΩ, so a 2.2 kΩ or 2.7 kΩ resistor gives the best resolution there.')])

# ---------------------------------------------------------------- Compound interest
P, r, n, t = 10000.0, 0.075, 4, 5
A = P * (1 + r / n) ** (n * t)
yr_rows = ''
prev = P
for y in range(1, 6):
    a = P * (1 + r / n) ** (n * y)
    yr_rows += f"| {y} | {prev:,.2f} | {a-prev:,.2f} | {a:,.2f} |\n"
    prev = a
infl = 0.05
real = A / (1 + infl) ** t
tax = 0.30
A_tax = P * (1 + r * (1 - tax) / n) ** (n * t)
dbl = math.log(2) / (n * math.log(1 + r / n))

edit_keep_featured('finance/compound-interest', date=U, phrase='compound interest calculator',
     intro=("Compound interest is interest earned on earlier interest as well as on the original deposit, so savings grow faster each year. "
            "This compound interest calculator finds the maturity amount, interest, rate or time for yearly to daily compounding.\n\n"
            "Savers comparing fixed deposits, CDs and savings accounts use it to see what a rate really earns, "
            "and borrowers use it to understand how unpaid interest builds up on a loan or card."),
     body_add=f'''
## Year by year growth of the default deposit

For 10,000 at 7.5% compounded quarterly, each year adds a little more than the last because the interest base keeps rising:

| Year | Opening balance | Interest in the year | Closing balance |
|---|---|---|---|
{yr_rows}
The fifth year earns noticeably more than the first even though the rate never changes. That widening gap is the whole effect of compounding.

## Real return after tax and inflation

Interest on deposits is normally taxed as it is credited. If 30% tax is paid from each quarterly credit, the effective rate falls to 7.5 × 0.70 = 5.25% and the 5 year balance is **{A_tax:,.2f}** instead of {A:,.2f}. With 5% inflation, the untaxed {A:,.2f} buys only what **{real:,.2f}** buys today. Comparing the post-tax rate with inflation shows whether a deposit is actually growing your purchasing power.

## Common mistakes

- **Entering the rate as a decimal.** Type 7.5 for 7.5%, not 0.075.
- **Mixing up time units.** Time is in years; 18 months is 1.5, not 18.
- **Comparing quoted rates with different compounding.** Convert both to an effective annual rate before choosing between offers.
- **Assuming payouts compound.** A deposit that pays interest out monthly does not compound at all; only reinvested interest grows.
- **Using the rule of 72 at high rates.** It drifts above about 20%; at 7.5% quarterly the exact doubling time is {dbl:.2f} years.
''',
     faq_add=[('How is compound interest taxed?',
               f'In most countries deposit interest is taxed in the year it is credited, even if it stays in the account. At 7.5% quarterly with 30% tax, 10,000 grows to about {A_tax:,.0f} after 5 years instead of {A:,.0f}.')])

# ---------------------------------------------------------------- Ohm's law
V, R = 24.0, 250.0
I = V / R
Pw = V * I
# 4-20 mA loop budget: 24 V supply, 250 ohm, transmitter min 12 V
Vmin_tx = 12.0
Rmax = (V - Vmin_tx) / 0.020
wire = 2 * 200 * 0.0175 / 1.0  # 200 m of 1 mm² copper, two cores
loop_rows = ''
for rl in (0, 250, 500, 600, 750):
    vt = V - 0.020 * (rl + wire)
    loop_rows += f"| {rl} Ω | {0.020*(rl+wire):.2f} V | {vt:.2f} V | {'OK' if vt >= Vmin_tx else 'Too low'} |\n"

edit_keep_featured('physics/ohms-law', date=U, phrase="Ohm's law calculator",
     intro=("Ohm's law, V = I × R, ties voltage, current and resistance together, and adding P = V × I brings in power. "
            "This Ohm's law calculator solves any two of the four values from the other two, with unit conversion. "
            "Start with the [basics of Ohm's law](https://www.instrumentationblog.in/basics-of-ohms-law/).\n\n"
            "Students, electricians and instrument technicians use it to check resistor values, loop loads, "
            "heater currents and fuse sizes before power is applied."),
     body_add=f'''
## Worked example with the default values

The calculator opens with {V:g} V across {R:g} Ω:

- I = V ÷ R = {V:g} ÷ {R:g} = **{I:.3f} A ({I*1000:.0f} mA)**
- P = V × I = {V:g} × {I:.3f} = **{Pw:.3f} W**

A standard 1/4 W resistor would burn out here; it needs at least a 5 W part to keep a 2× margin. This is the case of a 250 Ω resistor connected straight across a 24 V supply by mistake, instead of in series with a transmitter.

## Loop load check for a 4 to 20 mA circuit

A 24 V loop must leave enough voltage for the transmitter at 20 mA. With 200 m of 1 mm² copper ({wire:.1f} Ω for both cores) and a transmitter that needs {Vmin_tx:g} V:

| Load resistance | Drop at 20 mA | Left for transmitter | Result |
|---|---|---|---|
{loop_rows}
The largest total loop resistance is ({V:g} − {Vmin_tx:g}) ÷ 0.020 = **{Rmax:.0f} Ω**, including cable.

## Measuring to confirm the numbers

Measure resistance only with the circuit de-energised, because a meter on the ohms range in a live circuit reads wrong and can be damaged. Measure current by breaking the circuit and putting the meter in series, or by reading the voltage across a known resistor and dividing. Comparing a measured voltage drop with V = I × R is the quickest way to spot a corroded terminal or a wrong resistor.

## Common mistakes

- **Forgetting to convert milliamps.** 96 mA is 0.096 A; using 96 gives a resistance a thousand times too small.
- **Using cold resistance for a lamp or heater.** Filament resistance rises many times when hot, so a cold ohmmeter reading overstates the current.
- **Applying V = IR to an LED or diode.** Their current is not proportional to voltage; use the forward voltage and a series resistor.
- **Using RMS and peak values together.** In AC work, keep voltage and current both in RMS when calculating power.
- **Ignoring resistor tolerance.** A 5% resistor can be 237.5 to 262.5 Ω, which moves the current by the same 5%.
''',
     faq_add=[("What size resistor should carry 24 V and 96 mA?",
               f"It dissipates {Pw:.2f} W, so choose a 5 W resistor to keep at least a 2× power margin. A 1/4 W or 1 W part would overheat.")])

# ---------------------------------------------------------------- Weir flow
g = 9.80665
h, th, cd = 0.150, math.radians(90), 0.585
Qv = 8 / 15 * cd * math.sqrt(2 * g) * math.tan(th / 2) * h ** 2.5
L = 0.5
Qr = 1.84 * (L - 0.2 * h) * h ** 1.5
# sensitivity: 1 mm head error at 150 mm
Qv1 = 8 / 15 * cd * math.sqrt(2 * g) * h ** 2.5 * 0 + 8 / 15 * cd * math.sqrt(2 * g) * (h + 0.001) ** 2.5
err = (Qv1 / Qv - 1) * 100
ang_rows = ''
for deg in (22.5, 30, 45, 60, 90, 120):
    q = 8 / 15 * cd * math.sqrt(2 * g) * math.tan(math.radians(deg) / 2) * h ** 2.5
    ang_rows += f"| {deg:g}° | {math.tan(math.radians(deg)/2):.4f} | {q*3600:.2f} m³/h |\n"
hl = 0.050
Qlow = 8 / 15 * cd * math.sqrt(2 * g) * hl ** 2.5
errlow = ((hl + 0.001) ** 2.5 / hl ** 2.5 - 1) * 100

edit('engineering/weir-flow', date=U, phrase='weir flow calculator',
     intro=("A weir is a notch or plate across an open channel, and the height of water above it sets the flow. "
            "This weir flow calculator works out flow for a V-notch or a contracted rectangular weir from the measured head.\n\n"
            "Effluent plant operators, irrigation engineers and environmental inspectors use it to check flow meters and discharge permits. "
            "See [measuring flow rate with level sensors](https://www.instrumentationblog.in/measure-flow-rate-level-sensors/)."),
     body_add=f'''
## Worked example: 90° V-notch at 150 mm head

The default inputs are a 90° V-notch, C<sub>d</sub> = {cd}, and h = 150 mm:

- √(2g) = √(2 × 9.80665) = {math.sqrt(2*g):.4f} m^0.5/s
- tan(90° ÷ 2) = 1
- h^2.5 = 0.150^2.5 = {h**2.5:.6f} m^2.5
- Q = 8/15 × {cd} × {math.sqrt(2*g):.4f} × 1 × {h**2.5:.6f} = **{Qv:.5f} m³/s = {Qv*3600:.2f} m³/h ({Qv*1000:.2f} L/s)**

Switching the type to rectangular with the default 0.5 m crest gives Q = 1.84 × (0.5 − 0.2 × 0.15) × 0.15^1.5 = **{Qr*3600:.1f} m³/h**, about {Qr/Qv:.1f} times as much at the same head.

## Effect of notch angle at 150 mm head

| Notch angle | tan(θ/2) | Flow |
|---|---|---|
{ang_rows}
Narrow notches suit small effluent flows; a 120° notch passes more water before overtopping.

## How accurately must the head be measured?

Because flow goes with h^2.5, a 1 mm head error at 150 mm shifts the V-notch flow by **{err:.1f}%**. At 50 mm head the same 1 mm error is **{errlow:.1f}%** of a flow of only {Qlow*3600:.2f} m³/h. That is why the head is read in a stilling well with a hook gauge or an ultrasonic sensor that has been zeroed against the notch bottom, not against the channel floor.

## Common mistakes

- **Measuring head at the plate.** The surface draws down near the weir; read it 4 to 5 heads upstream.
- **Zeroing to the wrong point.** Head is measured from the notch vertex or crest, so survey that level into the sensor zero.
- **A submerged or clinging nappe.** If tailwater rises above the crest or the nappe sticks to the plate, the free discharge formulas no longer apply.
- **Using the Francis formula for a full width weir.** A suppressed weir without end contractions needs the 0.2h term removed.
- **Letting silt build up upstream.** A filled approach pool raises approach velocity and makes the weir read low.
''',
     faq_add=[('How much does a 1 mm error in head change V-notch flow?',
               f'Flow follows h^2.5, so the error is about 2.5 times the relative head error. At 150 mm head, 1 mm is {err:.1f}% of flow; at 50 mm it is {errlow:.1f}%.')])

# ---------------------------------------------------------------- Stock average
q1, p1, q2, p2 = 100, 250.0, 50, 200.0
inv = q1 * p1 + q2 * p2
avg = inv / (q1 + q2)
cost_pct = 0.001  # 0.1% charges each buy
inv_c = inv * (1 + cost_pct)
avg_c = inv_c / (q1 + q2)
drop = (avg - p2) / avg * 100
# sell 60 at 240: realised on average cost
sell_q, sell_p = 60, 240.0
gain_avg = sell_q * (sell_p - avg)
gain_fifo = sell_q * (sell_p - p1)
pl_rows = ''
for px in (180, 200, 220, 233.33, 250, 280):
    pl = (q1 + q2) * px - inv
    pl_rows += f"| {px:,.2f} | {(q1+q2)*px:,.2f} | {pl:+,.2f} | {pl/inv*100:+.1f}% |\n"

edit_keep_featured('finance/stock-average', date=U, phrase='stock average calculator',
     intro=("Buying more of a share at a different price changes your average cost, which is also your break-even price. "
            "This stock average calculator combines up to three purchases into total shares, total invested and average price per share.\n\n"
            "Retail investors use it before averaging down or up, to see how many shares a target average needs "
            "and how much extra money that ties up in one stock."),
     body_add=f'''
## Worked example with the default purchases

- First buy: {q1} × {p1:,.0f} = {q1*p1:,.0f}
- Second buy: {q2} × {p2:,.0f} = {q2*p2:,.0f}
- Total shares = {q1+q2}; total invested = **{inv:,.2f}**
- Average = {inv:,.0f} ÷ {q1+q2} = **{avg:,.2f}** per share

The average fell by only {(p1-avg):,.2f} even though the second price was 50 lower, because the second lot was half the size of the first. If brokerage and charges of 0.1% are added to each buy, the true cost basis is {inv_c:,.2f} and the average becomes **{avg_c:,.2f}**.

## Profit or loss at different market prices

For the 150 shares held at an average of {avg:,.2f}:

| Market price | Holding value | Profit or loss | Return |
|---|---|---|---|
{pl_rows}
## Average cost against FIFO when you sell part

Selling {sell_q} shares at {sell_p:,.0f} shows a gain of {gain_avg:,.2f} against the average cost, but under FIFO those shares come from the first lot at {p1:,.0f}, giving a tax loss of {gain_fifo:,.2f}. Brokers' portfolio screens usually show the average, while contract notes and tax statements may follow FIFO, so keep both views.

## Common mistakes

- **Leaving out charges.** Brokerage, exchange fees, stamp duty and tax change the real break-even price.
- **Averaging across a split or bonus.** Adjust old quantities and prices for the split ratio before adding new buys.
- **Treating the average as a target price.** The market does not know your cost; judge the stock on its prospects.
- **Ignoring position size.** Each average down raises the share of money in one stock; set a cap before you start.
- **Mixing currencies or exchanges.** Convert purchases made in different currencies at the rate on each trade date.
''',
     faq_add=[('How do I adjust my average price after a stock split?',
               'Multiply the shares held by the split ratio and divide the old price by the same ratio. After a 1 for 2 split, 100 shares at 250 become 200 shares at 125, and the total invested does not change.')])

# ---------------------------------------------------------------- Transformer current
S, Vp, Vs = 500.0, 11000.0, 433.0
s3 = math.sqrt(3)
Ip = S * 1000 / (s3 * Vp)
Is = S * 1000 / (s3 * Vs)
nr = Vp / Vs
# CT selection: 800/5 on LV; secondary at full load
ct_sec = Is / 800 * 5
# loading: measured 480 A
Imeas = 480.0
load = Imeas / Is * 100
kva_meas = s3 * Vs * Imeas / 1000
# inrush estimate 10x for HV
inr = 10 * Ip
z = 0.0475
Isc = Is / z
sp_rows = ''
for kva in (5, 10, 15, 25, 50, 100):
    sp_rows += f"| {kva} kVA | {kva*1000/230:.1f} A | {kva*1000/240:.1f} A | {kva*1000/120:.1f} A |\n"

edit('electrical/transformer-current', date=U, phrase='transformer current calculator',
     intro=("A transformer's kVA rating and line voltages set the full-load current on each winding. "
            "This transformer current calculator gives primary and secondary full-load amps and the voltage ratio for single-phase and three-phase units. "
            "Learn [how to calculate transformer kVA rating](https://www.instrumentationblog.in/how-to-calculate-transformer-kva-rating/).\n\n"
            "Electrical engineers, contractors and substation staff use it to size breakers, fuses, cables, busbars and current transformers, and to check how heavily a unit is loaded."),
     body_add=f'''
## Worked example: 500 kVA, 11 kV to 433 V

With the default three-phase inputs:

- Primary: I = 500 × 1,000 ÷ (√3 × 11,000) = 500,000 ÷ {s3*Vp:,.0f} = **{Ip:.2f} A**
- Secondary: I = 500 × 1,000 ÷ (√3 × 433) = 500,000 ÷ {s3*Vs:,.1f} = **{Is:.1f} A**
- Voltage ratio = 11,000 ÷ 433 = **{nr:.2f}**

The current ratio is the inverse of the voltage ratio: {Is:.1f} ÷ {Ip:.2f} = {Is/Ip:.2f}.

## Using the result on site

- **Checking load.** A clamp meter reading of {Imeas:.0f} A per phase on the LV side means {Imeas:.0f} ÷ {Is:.1f} = **{load:.0f}%** loading, or about {kva_meas:.0f} kVA.
- **Choosing LV current transformers.** An 800/5 A CT gives {ct_sec:.2f} A on its secondary at full load, leaving headroom for overload without saturating.
- **HV fuse selection.** Magnetising inrush of around 10 times rated current, about {inr:.0f} A for a few cycles, must not blow the HV fuse.
- **Fault level.** With 4.75% impedance the LV short-circuit current is roughly {Is:.1f} ÷ 0.0475 = **{Isc/1000:.1f} kA**, which sets the breaker breaking capacity.

## Single-phase transformer currents

| Rating | 230 V | 240 V | 120 V |
|---|---|---|---|
{sp_rows}
## Common mistakes

- **Using phase voltage with the √3 formula.** Three-phase full-load current uses line voltage; using 250 V instead of 433 V inflates the answer by √3.
- **Applying power factor to kVA.** Rating current depends only on kVA; power factor matters only when converting a kW load to kVA.
- **Sizing on 433 V and running at 400 V.** A lower secondary voltage means more current for the same kVA.
- **Forgetting delta winding current.** Inside a delta winding the current is line current ÷ √3, which matters for winding and internal CT checks.
- **Ignoring harmonics.** Non-linear loads heat a transformer more than the RMS current suggests; derate using the K factor.
''',
     faq_add=[('How do I check transformer loading with a clamp meter?',
               f'Measure the LV phase currents, take the highest, and divide by the full-load current. For a 500 kVA, 433 V unit, {Imeas:.0f} A is {load:.0f}% of the {Is:.0f} A rating.')])

print('done', inplace.DONE)
for c in inplace.DONE:
    print(c, inplace.body_words(c))

# ======================================================================= SECTION _expand_c2.py
"""Part C expand (2026-11-17), slice 2: pfd-avg, tds-conductivity, scientific-notation,
safe-failure-fraction, angle-converter. Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-17'
HR = 8760

def sci(x, d=2):
    e = math.floor(math.log10(abs(x))); m = x / 10 ** e
    sup = str(e).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))
    return f'{m:.{d}f} × 10{sup}'

# ---------------------------------------------------------------- PFDavg
lam, TI = 500, 1
PFD = lam * 1e-9 * TI * HR / 2
RRF = 1 / PFD
SIL = max(0, min(4, math.floor(math.log10(RRF))))
dem = 0.1
haz = dem * PFD
lmax2 = 2 * 1e-2 / (1 * HR) * 1e9
rows = ''
for ti in (0.5, 1, 2, 3, 5):
    c = [2 * p / (ti * HR) * 1e9 for p in (1e-1, 1e-2, 1e-3)]
    lab = '6 months' if ti == 0.5 else (f'{ti:g} year' + ('s' if ti != 1 else ''))
    rows += f'| {lab} | {c[0]:,.0f} FIT | {c[1]:,.0f} FIT | {c[2]:,.1f} FIT |\n'

edit('engineering/pfd-avg', date=U, phrase='PFDavg calculator',
     intro=("PFDavg is the average probability that a safety instrumented function fails to act when a demand arrives, and it sets the SIL band the function reaches. "
            "This PFDavg calculator works out the 1oo1 value from the [PFDavg calculation formula](https://www.instrumentationblog.in/pfdavg-calculation-formula/).\n\n"
            "Functional safety engineers use it during [SIL verification](https://www.instrumentationblog.in/sil-verification/) to check a loop against its target, "
            "choose a proof test interval and see which device dominates the result."),
     body_add=f'''
## Checking the default inputs

With the calculator's starting values, a single channel with λ<sub>DU</sub> = {lam} FIT tested once a year:

- PFD<sub>avg</sub> = {lam} × 10⁻⁹ × {HR:,} ÷ 2 = **{sci(PFD)}**
- RRF = 1 ÷ {PFD:.5f} = **{RRF:.0f}**
- log₁₀({RRF:.0f}) = {math.log10(RRF):.2f}, so PFD<sub>avg</sub> alone supports **SIL {SIL}**

## Largest λDU allowed for each SIL

Rearranging the 1oo1 formula gives the highest total λ<sub>DU</sub> a loop can have and still meet the upper PFD<sub>avg</sub> limit of a band: λ<sub>DU,max</sub> = 2 × PFD<sub>limit</sub> ÷ TI.

| Proof test interval | SIL 1 (PFD < 10⁻¹) | SIL 2 (PFD < 10⁻²) | SIL 3 (PFD < 10⁻³) |
|---|---|---|---|
{rows}
This table is a quick screening tool: if the sum of the device λ<sub>DU</sub> values from the safety manuals is above the figure for your test interval, a single channel cannot meet the target and redundancy or a better final element is needed.

## From PFDavg to hazard frequency

PFD<sub>avg</sub> becomes meaningful when it is combined with how often the process actually challenges the function. In a LOPA study the hazardous event frequency is the demand rate times PFD<sub>avg</sub>. If the high pressure condition is expected {dem:g} times a year, the default loop leaves a residual frequency of {dem:g} × {PFD:.5f} = **{sci(haz)} per year**, roughly once in {1/haz:,.0f} years. The formula on this page assumes low demand mode, which IEC 61511 defines as no more than one demand per year; above that, the function is in high demand mode and must be judged on its dangerous failure frequency (PFH) instead.

## Where λDU values come from

Use the λ<sub>DU</sub> printed in each device's IEC 61508 certificate or safety manual, which is normally derived from an FMEDA. Where a device is justified by prior use, the rate should come from your own maintenance records over enough operating hours to be credible. Generic databases are acceptable for early screening but tend to give higher rates than certified data, so the final calculation should state which source was used for each element.
''',
     faq_add=[('What is the maximum λDU for SIL 2 with annual proof testing?',
               f'For a 1oo1 function, PFDavg must stay below 10⁻², so λDU must be below 2 × 0.01 ÷ 8,760 h = {lmax2:,.0f} FIT in total across the sensor, logic solver and final element.'),
              ('How does the demand rate affect the risk with a given PFDavg?',
               f'The residual hazard frequency is the demand rate times PFDavg. With PFDavg = {PFD:.5f} and {dem:g} demands per year, the hazard is expected about once every {1/haz:,.0f} years.')])

# ---------------------------------------------------------------- Safe failure fraction
lS, lDD, lDU = 300, 450, 50
lt = lS + lDD + lDU
SFF = (lS + lDD) / lt; DC = lDD / (lDD + lDU); mttf = 1e9 / lt / 8766
def typeb0(s):
    return 'Not allowed' if s < 0.6 else ('SIL 1' if s < 0.9 else ('SIL 2' if s < 0.99 else 'SIL 3'))
srows = ''
for dc in (0.0, 0.5, 0.6, 0.8, 0.9, 0.95, 0.99):
    dd = dc * 500; du = 500 - dd; s = (lS + dd) / lt
    srows += f'| {dc*100:.0f}% | {dd:.0f} FIT | {du:.0f} FIT | {s*100:.2f}% | {typeb0(s)} |\n'
pfd_dev = lDU * 1e-9 * HR / 2

edit('engineering/safe-failure-fraction', date=U, phrase='safe failure fraction calculator',
     intro=("Safe failure fraction is the share of a device's failures that are safe or dangerous but detected, and with hardware fault tolerance it caps the SIL a subsystem may claim. "
            "This safe failure fraction calculator gives SFF and diagnostic coverage from FMEDA failure rates.\n\n"
            "Safety engineers and device assessors use it to check a transmitter or valve against the [hardware fault tolerance and SFF](https://www.instrumentationblog.in/hardware-fault-tolerance-sff-iec-61508/) "
            "tables of IEC 61508 before it is accepted into a safety function."),
     body_add=f'''
## How diagnostic coverage moves SFF

Keeping the example device's λ<sub>S</sub> = {lS} FIT and its total dangerous rate of 500 FIT, but changing how much of that dangerous rate the diagnostics catch:

| Diagnostic coverage | λ<sub>DD</sub> | λ<sub>DU</sub> | SFF | Type B, HFT 0 limit |
|---|---|---|---|---|
{srows}
The safe failures alone give this device a floor of {lS/lt*100:.1f}% SFF. Each step in diagnostic coverage then converts undetected dangerous failures into detected ones, and the jump from 90% to 99% DC is what lifts a Type B single channel from SIL 2 to SIL 3 territory.

## Where the numbers come from: the FMEDA

A failure modes, effects and diagnostic analysis lists every component of the device, its failure rate and each failure mode, then classifies the effect of each mode on the safety function as safe, dangerous detected, dangerous undetected or no effect. The FMEDA must be done for the exact configuration used: the same transmitter can have a different λ<sub>DU</sub> when its output is set to fail low instead of fail high, or when the logic solver is not set to trip on an out of range current below 3.6 mA or above 21 mA.

## SFF and PFDavg are separate checks

A high SFF does not by itself give a low PFD<sub>avg</sub>. The example transmitter's λ<sub>DU</sub> of {lDU} FIT, proof tested yearly, contributes {lDU} × 10⁻⁹ × {HR:,} ÷ 2 = **{sci(pfd_dev)}** to the loop's PFD<sub>avg</sub> on its own. A safety function has to meet the SIL target for both the architectural constraint and the PFD<sub>avg</sub>, and the weaker of the two sets the SIL that can be claimed.

## Common mistakes

- **Counting "no effect" failures as safe.** IEC 61508 Edition 2 excludes them, and including them inflates the SFF of devices with many passive parts.
- **Treating λ<sub>DD</sub> as safe when nothing acts on the diagnostic.** If a detected fault only raises an alarm that nobody responds to within the assumed repair time, it behaves as dangerous.
- **Using a single device's SFF for a whole subsystem.** The architectural limit applies per subsystem: sensor, logic solver and final element are each checked with their own HFT.
- **Applying the Type A table to a smart transmitter.** Any device with a microprocessor or software is normally Type B, which has stricter limits.
- **Mixing data from different FMEDA reports.** Failure rates from different sources often use different assumptions about operating stress, so take λ<sub>S</sub>, λ<sub>DD</sub> and λ<sub>DU</sub> for one device from the same report.
''',
     faq_add=[('Where do I find the λS, λDD and λDU values for a device?',
               'In the IEC 61508 certificate, the safety manual or the FMEDA report supplied by the manufacturer. Use the values for the configuration you actually install, such as fail low output and the trip settings of your logic solver.'),
              ('Does IEC 61511 still use SFF?',
               'The 2016 edition of IEC 61511 dropped SFF from its own hardware fault tolerance table, which sets minimum HFT by SIL instead. SFF remains part of IEC 61508 Route 1H, which device manufacturers use for certification.')])

# ---------------------------------------------------------------- TDS conductivity
EC, T, a, k = 750, 20, 2.0, 0.65
EC25 = EC / (1 + a / 100 * (T - 25)); TDS = k * EC25
trows = ''
for t in (5, 10, 15, 20, 25, 30, 35):
    f = 1 / (1 + a / 100 * (t - 25))
    trows += f'| {t} °C | {f:.4f} | {EC*f:,.1f} µS/cm | {k*EC*f:,.0f} mg/L |\n'
tgt = 500; ec_t = tgt / k; raw = ec_t * (1 + a / 100 * (T - 25))

edit('chemistry/tds-conductivity', date=U, phrase='TDS to conductivity calculator',
     intro=("Total dissolved solids can be estimated from electrical conductivity because dissolved salts carry current. "
            "This TDS to conductivity calculator corrects a reading to 25 °C and converts EC in µS/cm to TDS in mg/L (ppm) with an adjustable factor, or works back from a target TDS.\n\n"
            "Water treatment operators, RO plant technicians, aquarists and growers use it to read [conductivity sensor](https://www.instrumentationblog.in/conductivity-sensor-working/) "
            "results as TDS and to set alarm points."),
     body_add=f'''
## Temperature correction at 2 %/°C

Conductivity readings change by about 2% for every degree away from 25 °C. The table shows the correction factor 1 ÷ [1 + 0.02 (T − 25)] and what a raw reading of {EC} µS/cm means at each sample temperature with k = {k}:

| Sample temperature | Factor | EC at 25 °C | TDS |
|---|---|---|---|
{trows}
A reading taken on a cold winter sample can therefore understate the TDS by a quarter or more if no compensation is applied.

## Working back from a TDS limit

To set an alarm at {tgt} mg/L with k = {k}, the conductivity at 25 °C must be {tgt} ÷ {k} = **{ec_t:.1f} µS/cm**. An uncompensated meter reading a {T} °C sample would show {ec_t:.1f} × [1 + 0.02 × ({T} − 25)] = **{raw:.1f} µS/cm** at that point, so the alarm in the raw units has to be lower than the compensated value.

## How conductivity is measured in practice

A conductivity cell applies an AC voltage between two or four electrodes and measures the current. The cell constant K (in cm⁻¹) relates the measured conductance to conductivity, and it is chosen for the range: about 0.01 to 0.1 cm⁻¹ for RO permeate and boiler feed water, 1.0 cm⁻¹ for drinking and process water, and 10 cm⁻¹ or an inductive (toroidal) sensor for brines and sea water. Calibrate with a potassium chloride standard close to the working range, such as 84, 1,413 or 12,880 µS/cm at 25 °C, and rinse the cell with sample before reading.

## Common mistakes

- **Applying compensation twice.** Most handheld meters already show a 25 °C value; entering the sample temperature again with α = 2 corrects it a second time.
- **Comparing ppm from two meters with different factors.** A meter set to 0.5 and one set to 0.7 differ by 40% on the same water. Compare EC instead.
- **Using 0.65 for RO permeate or brine.** Very pure water and concentrated salt solutions follow different factors; calibrate k against a gravimetric TDS for those waters.
- **Using a low cell constant on brackish water.** A K = 0.1 cell saturates or polarises at high conductivity and reads low.
- **Measuring with air bubbles in the cell.** Bubbles on the electrodes block current paths and give a falsely low reading, common on fresh tap samples.
''',
     faq_add=[('What conductivity corresponds to 500 ppm TDS?',
               f'With a factor of 0.65 it is about {ec_t:.0f} µS/cm at 25 °C; with 0.5 it is 1,000 µS/cm and with 0.7 about {tgt/0.7:.0f} µS/cm. The factor depends on the ions in your water.'),
              ('Which cell constant should I use for my conductivity sensor?',
               'Use about 0.01 to 0.1 cm⁻¹ for ultrapure and RO water, 1.0 cm⁻¹ for drinking and general process water and 10 cm⁻¹ or a toroidal sensor for brines and sea water.')])

# ---------------------------------------------------------------- Scientific notation
x = 4.56e7
ex = math.floor(math.log10(abs(x))); m = x / 10 ** ex; ee = 3 * math.floor(ex / 3); me = x / 10 ** ee
y = 3.2e5; s = x + y
q = x / 1.2e-3; qe = math.floor(math.log10(q))
pr = x * 6.5e-4; pe = math.floor(math.log10(pr))
srows = ''
for sf in (1, 2, 3, 4):
    srows += f'| {sf} | {m:.{sf-1}f} × 10⁷ | {float(f"{x:.{sf-1}e}"):,.0f} |\n'
srows = srows.replace('| 1 | 5 × 10⁷', '| 1 | 5 × 10⁷')

edit('math/scientific-notation', date=U, phrase='scientific notation calculator',
     intro=("Scientific notation writes a number as a coefficient from 1 to just under 10 times a power of ten, so 45,600,000 becomes 4.56 × 10⁷. "
            "This scientific notation calculator gives the coefficient, exponent and engineering form, and converts back to a decimal.\n\n"
            "Students use it to check homework in physics and chemistry, while engineers and lab staff use it to read E notation from instruments and spreadsheets and to keep track of very large or very small values."),
     body_add=f'''
## Default example check

The calculator starts with {x:,.0f}. Its exponent is ⌊log₁₀ {x:,.0f}⌋ = ⌊{math.log10(x):.4f}⌋ = **{ex}**, the coefficient is **{m:g}**, the engineering exponent is **{ee}** and the engineering coefficient is **{me:g}**.

## Arithmetic in scientific notation

- **Adding or subtracting:** rewrite both numbers with the same exponent first. 4.56 × 10⁷ + 3.2 × 10⁵ = 4.56 × 10⁷ + 0.032 × 10⁷ = **{s/1e7:g} × 10⁷**.
- **Dividing:** divide the coefficients and subtract the exponents. (4.56 × 10⁷) ÷ (1.2 × 10⁻³) = 3.8 × 10⁷⁻⁽⁻³⁾ = **{q/10**qe:g} × 10¹⁰**.
- **Multiplying with renormalising:** (4.56 × 10⁷) × (6.5 × 10⁻⁴) = 29.64 × 10³, which is not normalised, so move the point once to get **{pr/10**pe:g} × 10⁴**.

## Rounding to significant figures

The coefficient carries the precision. Rounding {x:,.0f} to fewer significant figures:

| Significant figures | Scientific notation | Decimal value |
|---|---|---|
{srows}
Trailing zeros in the coefficient are meaningful: 4.560 × 10⁷ claims a precision of ±5,000, while 4.56 × 10⁷ claims ±50,000.

## Where you meet it

Spreadsheets switch to E notation when a number is too wide for the column, showing 4.56E+07. Spreadsheet programs keep only 15 significant digits, so a 16 digit card or account number typed as a number is stored in scientific form and its last digit becomes 0; format such columns as text before pasting. Instruments and data loggers often export readings like 1.23E-06 A, which is 1.23 µA in engineering terms.

## Common mistakes

- **Writing 10E7 for 10⁷.** On calculators and in code, 10E7 means 10 × 10⁷ = 10⁸. Type 1E7 for ten million.
- **Leaving the coefficient above 10.** 45.6 × 10⁶ is valid engineering notation but not normalised scientific notation; it should be 4.56 × 10⁷.
- **Getting the exponent sign backwards for small numbers.** 0.00045 needs the point moved four places right, so the exponent is −4, not +4.
- **Adding exponents when adding numbers.** Exponents add only when multiplying; for sums, match the exponents first.
- **Dropping significant zeros.** Writing 4.5 × 10⁷ for a value measured as 4.50 × 10⁷ throws away a digit of precision.
''',
     faq_add=[('Why does my spreadsheet show 4.56E+07?',
               'The column is too narrow for the full number, so the spreadsheet shows it in E notation: 4.56E+07 means 4.56 × 10⁷ = 45,600,000. Widen the column or apply a number format to see all digits.'),
              ('What does 10E7 mean?',
               '10E7 means 10 × 10⁷, which is 10⁸ or 100,000,000. To enter ten million in E notation, type 1E7.')])

# ---------------------------------------------------------------- Angle converter
dg = 52.3725
D = math.floor(dg); M = math.floor((dg - D) * 60); S = ((dg - D) * 60 - M) * 60
back = 52 + 22 / 60 + 21 / 3600
sd, sm, ss = 33, 51, 54
sdec = -(sd + sm / 60 + ss / 3600)
R = 6371000
mdeg = 2 * math.pi * R / 360
prows = ''
for lab, ang in (('0.1°', 0.1), ('0.01°', 0.01), ('0.001°', 0.001), ('0.0001°', 0.0001), ('0.00001°', 0.00001), ('1′', 1/60), ('1″', 1/3600), ('0.1″', 0.1/3600)):
    d = mdeg * ang
    prows += f'| {lab} | {d/1000:,.2f} km |\n' if d >= 1000 else f'| {lab} | {d:,.2f} m |\n'
lat_c = math.cos(math.radians(dg))
lon1s = mdeg / 3600 * lat_c

edit('math/angle-converter', date=U, phrase='angle converter calculator',
     intro=("Angles are written in degrees for everyday work, radians in mathematics and physics, gradians on some survey instruments and degrees, minutes and seconds for map coordinates. "
            "This angle converter calculator converts between all of them at once.\n\n"
            "Students, surveyors, GIS users, machinists and programmers use it to move between calculator modes, read coordinates from maps or GPS units and feed radians into software trig functions."),
     body_add=f'''
## Degrees, minutes and seconds back to decimal

Reverse the split by dividing minutes by 60 and seconds by 3,600:

- 52° 22′ 21″ = 52 + 22 ÷ 60 + 21 ÷ 3,600 = **{back:.4f}°**, the calculator's starting value
- A southern latitude of {sd}° {sm}′ {ss}″ S is written as a negative decimal: −({sd} + {sm} ÷ 60 + {ss} ÷ 3,600) = **{sdec:.4f}°**

North and east are positive; south and west are negative in decimal degree coordinates.

## Coordinate precision on the ground

Along a meridian, using a mean Earth radius of 6,371 km, one degree of latitude is about {mdeg/1000:.2f} km:

| Angle | Distance on the ground |
|---|---|
{prows}
Longitude lines converge toward the poles, so at latitude {dg}° one arcsecond of longitude is only {mdeg/3600:.2f} × cos {dg}° = **{lon1s:.2f} m**. Five decimal places of degrees, about 1 m, is enough for most GPS work.

## Common mistakes

- **Reading 52.30° as 52° 30′.** The decimal part is a fraction of a degree, so 52.30° is 52° 18′.
- **Leaving the calculator in the wrong mode.** sin 30 gives 0.5 in DEG mode, −0.988 in RAD mode and 0.454 in GRAD mode.
- **Splitting a negative angle directly.** The floor of −52.3725 is −53, which gives wrong minutes and seconds; convert 52.3725 and put the minus sign or the S or W letter in front.
- **Showing 60″ after rounding.** 59.996″ rounded to two places is 60.00″; carry it to the next minute instead.
- **Confusing milliradians with NATO mils.** A turn is 6,283.2 mrad but 6,400 mil, so the two differ by about 1.9% and should not be mixed on sights or maps.
''',
     faq_add=[('How do I convert degrees, minutes and seconds to decimal degrees?',
               f'Add the degrees, the minutes divided by 60 and the seconds divided by 3,600. For 52° 22′ 21″ that is 52 + 0.36667 + 0.00583 = {back:.4f}°. Make the result negative for south or west.'),
              ('How accurate is a coordinate with five decimal places?',
               f'0.00001° of latitude is about {mdeg*1e-5:.2f} m on the ground, so five decimal places locate a point to roughly a metre. Six decimal places give about 11 cm.')])

print('done')

# ======================================================================= SECTION _expand_c3.py
"""Part C expand (2026-11-17), slice 3: capacitors-series-parallel, geometric-distribution,
birthday-paradox, schmitt-trigger, crystal-load-capacitance, transistor-base-resistor.
Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-17'
G_OLD = '## Example\n\nA sales call succeeds 20% of the time. The chance that the first sale comes on the 3rd call:\n\n- P(X = 3) = 0.8² × 0.2 = **12.8%**\n- P(X ≤ 3) = 1 − 0.8³ = **48.8%**, P(X > 3) = 0.8³ = **51.2%**\n- Expected calls = 1 ÷ 0.2 = **5**, standard deviation = √0.8 ÷ 0.2 = **4.4721**\n\n'
B_OLD = '## Example\n\nA group of 23 people:\n\n- P(all different) = 365 × 364 × … × 343 ÷ 365²³ = **49.27%**\n- P(at least one shared birthday) = 1 − 0.4927 = **50.73%**\n- P(someone shares your birthday) = 1 − (364/365)²² = **5.86%**\n- Pairs = 23 × 22 ÷ 2 = **253**\n\n'
pi = math.pi

# ---------------------------------------------------------------- Capacitors in series and parallel
Cs_ = 10 * 22 / 32  # uF, default series pair
Cp_ = 32.0
def xc(f, c_uF): return 1 / (2 * pi * f * c_uF * 1e-6)
xr = ''
for f, lab in ((50, '50 Hz'), (120, '120 Hz'), (1e3, '1 kHz'), (10e3, '10 kHz'), (100e3, '100 kHz')):
    xr += f"| {lab} | {xc(f,10):,.2f} Ω | {xc(f,22):,.2f} Ω | {xc(f,Cs_):,.2f} Ω | {xc(f,Cp_):,.3f} Ω |\n"
tol_lo = (10*0.8) * (22*0.8) / (10*0.8 + 22*0.8)
tol_hi = (10*1.2) * (22*1.2) / (10*1.2 + 22*1.2)
V1w = 50 * (22*0.8) / (10*1.2 + 22*0.8)  # worst case: C1 high? smaller C takes more V; C1 low, C2 high
V1w = 50 * (22*1.2) / (10*0.8 + 22*1.2)

edit('electronics/capacitors-series-parallel', date=U,
     body_add=f'''
## Reactance of the combination on AC

On AC each capacitor behaves as a reactance X<sub>C</sub> = 1 ÷ (2πfC). Series reactances add like series resistors, so the series pair always has more reactance than either part. For the default 10 µF and 22 µF pair:

| Frequency | 10 µF alone | 22 µF alone | Series ({Cs_:.3f} µF) | Parallel ({Cp_:g} µF) |
|---|---|---|---|---|
{xr}
At 50 Hz, {xc(50,10):,.1f} Ω + {xc(50,22):,.1f} Ω = {xc(50,10)+xc(50,22):,.1f} Ω, which is exactly the reactance of a single {Cs_:.3f} µF capacitor. This is a quick way to check a series result by hand.

## Tolerance on the total

With ±20% electrolytics the default series pair can measure anywhere from **{tol_lo:.2f} µF** (both parts low) to **{tol_hi:.2f} µF** (both high). The voltage split is worse: if the 10 µF part is 20% low and the 22 µF part 20% high, the 10 µF part sees **{V1w:.1f} V** of the 50 V instead of 34.4 V. Measure the parts with an LCR meter before building a series stack for high voltage.
''',
     faq_add=[('What is the reactance of capacitors in series?',
               f'The reactances add: X = X₁ + X₂. At 50 Hz a 10 µF part is {xc(50,10):.1f} Ω and a 22 µF part {xc(50,22):.1f} Ω, so the series pair is {xc(50,10)+xc(50,22):.1f} Ω, the same as one {Cs_:.3f} µF capacitor.')])

# ---------------------------------------------------------------- Geometric distribution
p, k = 0.20, 3
P = (1 - p) ** (k - 1) * p
Pc = 1 - (1 - p) ** k
Pg = (1 - p) ** k
mu = 1 / p
sd = math.sqrt(1 - p) / p
def need(pp, c): return math.ceil(math.log(1 - c) / math.log(1 - pp))
nr = ''
for pp in (0.5, 0.2, 0.1, 0.05, 0.02, 0.01):
    nr += f"| {pp*100:g}% | {1/pp:g} | {need(pp,0.5)} | {need(pp,0.9)} | {need(pp,0.95)} | {need(pp,0.99)} |\n"
# memoryless: after 5 failures, P(success within next 3)
mem = 1 - (1 - p) ** 3
k95 = need(p, 0.95)
P95 = 1 - (1 - p) ** k95
# median
med = math.ceil(math.log(0.5) / math.log(1 - p))
# rule of three style: defect rate 2%, inspection
pd = 0.02
first_by_50 = 1 - (1 - pd) ** 50

edit('statistics/geometric-distribution', date=U, replace=[(G_OLD, '')], phrase='geometric distribution calculator',
     intro=("The geometric distribution counts how many independent tries it takes to get the first success when every try has the same chance p. "
            "This geometric distribution calculator gives the probability that the first success lands exactly on trial k, by trial k or only after it.\n\n"
            "Students use it for probability coursework, quality engineers for the first defect in an inspection run, "
            "and sales or reliability teams to plan how many attempts are needed before a result is likely."),
     body_add=f'''
## Worked example with the default inputs

A sales call succeeds 20% of the time (p = 20%). For the first sale to come on the third call (k = 3), two failures must be followed by a success:

- P(X = 3) = 0.8 × 0.8 × 0.2 = **{P*100:.1f}%**
- P(X ≤ 3) = 1 − 0.8³ = 1 − {0.8**3:.3f} = **{Pc*100:.1f}%**
- P(X > 3) = 0.8³ = **{Pg*100:.1f}%**
- Mean = 1 ÷ 0.2 = **{mu:g} trials**, standard deviation = √0.8 ÷ 0.2 = **{sd:.4f}**

The median is only **{med} trials**, lower than the mean of 5, because the distribution has a long right tail: a few long runs of failures pull the average up.

## How many trials for a given confidence

Solving 1 − (1 − p)<sup>n</sup> ≥ c for n gives the number of attempts needed to be c sure of at least one success:

<p class="formula">n = ⌈ ln(1 − c) ÷ ln(1 − p) ⌉</p>

For p = 20% and 95% confidence, n = ln(0.05) ÷ ln(0.8) rounded up = **{k95}** trials, giving {P95*100:.1f}%.

| Success rate p | Mean trials | 50% sure | 90% sure | 95% sure | 99% sure |
|---|---|---|---|---|---|
{nr}
## Where it is used

- **Inspection and testing.** If 2% of parts are defective, the chance the first defect turns up within 50 parts is 1 − 0.98⁵⁰ = {first_by_50*100:.1f}%.
- **Retries in communications.** The number of transmissions until a packet gets through, when each attempt fails independently, is geometric. The mean is the expected retry cost.
- **Games and draws.** The number of rolls until a six (p = 1/6) has a mean of 6, but there is still a {(5/6)**10*100:.1f}% chance of no six in 10 rolls.

## The memoryless property in numbers

Suppose the first five calls all failed. The chance of a sale in the next three is still 1 − 0.8³ = **{mem*100:.1f}%**, exactly the same as P(X ≤ 3) from a fresh start. Past failures carry no information when trials are independent, so there is no such thing as being "due" a success.

## Common mistakes

- **Mixing up the two definitions.** Counting failures before the first success shifts k by one and changes the mean from 1/p to (1 − p)/p. Check which one a textbook or exam uses.
- **Using it when p changes.** Learning effects, fatigue or sampling without replacement from a small batch break the constant p assumption. A small batch needs the hypergeometric approach instead.
- **Reading the mean as a typical value.** With p = 20% the mean is 5 trials but the median is {med}; one run in ten needs {need(p,0.9)} or more trials.
- **Expecting a success by trial 1/p.** P(X ≤ 5) is only {(1-(0.8)**5)*100:.1f}%, not 100%.
- **Confusing P(X = k) with P(X ≤ k).** "First success on the third try" and "a success within three tries" are different questions with different answers.
''',
     faq_add=[('How many trials do I need to be 95% sure of at least one success?',
               f'Use n = ln(0.05) ÷ ln(1 − p) and round up. With p = 20% that is {k95} trials, and with p = 5% it is {need(0.05,0.95)} trials.'),
              ('How is the geometric distribution related to the negative binomial?',
               'The geometric distribution is the negative binomial with r = 1. The negative binomial counts the trials needed for r successes, so it is the sum of r independent geometric variables.')])

# ---------------------------------------------------------------- Birthday paradox
def shared(n, d):
    q = 1.0
    for i in range(n):
        q *= (d - i) / d
    return 1 - q
def approx(n, d): return 1 - math.exp(-n * (n - 1) / (2 * d))
n, d = 23, 365
Pn = 1 - shared(n, d)
P = shared(n, d)
Py = 1 - ((d - 1) / d) ** (n - 1)
pairs = n * (n - 1) // 2
ar = ''
for m in (10, 20, 23, 30, 40, 50, 70):
    ar += f"| {m} | {shared(m,d)*100:.2f}% | {approx(m,d)*100:.2f}% |\n"
def need_n(target, dd):
    m = 1
    while shared(m, dd) < target:
        m += 1
    return m
tr = ''
for t in (0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99):
    tr += f"| {t*100:g}% | {need_n(t,365)} | {need_n(t,12)} | {need_n(t,10000)} |\n"
h32 = math.sqrt(2 * 2 ** 32 * math.log(2))
h64 = math.sqrt(2 * 2 ** 64 * math.log(2))
# 4-digit PIN among 100 people
pin100 = shared(100, 10000)
# p with 29 Feb approximated by d=365.25? Simple: d=366
p366 = shared(23, 366)

edit('statistics/birthday-paradox', date=U, replace=[(B_OLD, '')], phrase='birthday paradox calculator',
     intro=("In a room of only 23 people there is a better than even chance that two share a birthday, which surprises most people because a year has 365 days. "
            "This birthday paradox calculator gives the exact probability of a shared birthday for any group size.\n\n"
            "Teachers use it to show how intuition fails with pairs, and software engineers use the same maths "
            "to size hash values, random IDs and coupon codes so that collisions stay rare."),
     body_add=f'''
## Worked example with the default inputs

For n = 23 people and d = 365 days:

- Pairs = 23 × 22 ÷ 2 = **{pairs}**
- P(all different) = 365 × 364 × … × 343 ÷ 365²³ = **{Pn*100:.2f}%**
- P(at least one shared birthday) = **{P*100:.2f}%**
- P(someone shares your birthday) = 1 − (364 ÷ 365)²² = **{Py*100:.2f}%**

Each of the {pairs} pairs has only a 1 in 365 chance of matching, but there are so many pairs that a match becomes more likely than not. Your own birthday is involved in just 22 of them, which is why the personal figure is so much lower.

## The quick approximation

For mental arithmetic, treat each pair as an independent 1/d chance:

<p class="formula">P(shared) ≈ 1 − e<sup>−n(n−1) ÷ 2d</sup> &nbsp;·&nbsp; n(50%) ≈ 1.1774 √d</p>

| People | Exact | Approximation |
|---|---|---|
{ar}
The approximation slightly underestimates the exact figure but is close enough for design work, and for 365 days it predicts {1.1774*math.sqrt(365):.1f} people for a 50% chance.

## Group size needed for a target probability

| Target probability | 365 days | 12 months | 10,000 values (4 digit PIN) |
|---|---|---|---|
{tr}
## Collisions in computing

The same formula applies to any set of equally likely values. A 32 bit hash has d = 2³² values, yet a 50% chance of a collision arrives after only about √(2 × 2³² × ln 2) = **{h32:,.0f}** items. A 64 bit hash pushes that to about {h64/1e9:,.1f} billion. Among 100 people choosing random 4 digit PINs, the chance that two pick the same one is **{pin100*100:.1f}%**. This is why identifiers and checksums are sized with the birthday bound, not the number of possible values.

## Trying it in a class

A group of 30 to 40 students is the classic demonstration: the calculator gives {shared(30,365)*100:.0f}% for 30 and {shared(40,365)*100:.0f}% for 40, so a match usually appears. Ask people to call out birthdays month by month; the first repeat ends the experiment.

## Common mistakes

- **Answering the personal question.** "Does anyone share my birthday?" needs 253 other people for 50%. "Do any two people share?" needs only 23.
- **Dividing n by 365.** 23 ÷ 365 = 6.3% ignores that every pair is a chance for a match.
- **Adding probabilities across pairs.** 253 ÷ 365 = 69% overcounts; the pairs overlap, so multiply the "all different" chances instead.
- **Forgetting 29 February.** Using 366 days changes the result for 23 people only to {p366*100:.2f}%, so it rarely matters.
- **Assuming uniform birthdays is conservative for the wrong side.** Real birth dates cluster by season, which makes a match slightly more likely, not less.
''',
     faq_add=[('What is the approximation formula for the birthday problem?',
               f'P ≈ 1 − e^(−n(n − 1) ÷ 2d). For 23 people and 365 days it gives {approx(23,365)*100:.1f}%, close to the exact {P*100:.1f}%. The group size for a 50% chance is about 1.1774 × √d.'),
              ('How does the birthday problem apply to hash collisions?',
               f'Set d to the number of possible hash values. For a 32 bit hash a collision becomes likely (50%) after only about {h32:,.0f} items, far fewer than the 4.3 billion possible values.')])

# ---------------------------------------------------------------- Schmitt trigger
Vr, R1, R2, Voh, Vol = 2.5, 10e3, 100e3, 5.0, 0.0
VTH = (Vr * R2 + Voh * R1) / (R1 + R2)
VTL = (Vr * R2 + Vol * R1) / (R1 + R2)
Vh = VTH - VTL
# Reference from a 10k/10k divider: Thevenin 5k adds to R1
R1e = R1 + 5e3
VTHe = (Vr * R2 + Voh * R1e) / (R1e + R2)
VTLe = (Vr * R2 + Vol * R1e) / (R1e + R2)
# Output swing loaded: Voh 4.8 V, Vol 0.2 V
VTHl = (Vr * R2 + 4.8 * R1) / (R1 + R2)
VTLl = (Vr * R2 + 0.2 * R1) / (R1 + R2)
# feedback current
Ifb = (Voh - VTH) / R2
sr = ''
for r2 in (47e3, 100e3, 220e3, 470e3, 1e6):
    h = 5 * R1 / (R1 + r2)
    sr += f"| {r2/1e3:,.0f} kΩ | {h*1000:,.1f} mV | {(Vr*r2+5*R1)/(R1+r2):.4f} V | {(Vr*r2)/(R1+r2):.4f} V |\n"

edit('electronics/schmitt-trigger', date=U, phrase='Schmitt trigger calculator',
     intro=("A Schmitt trigger adds positive feedback to a comparator so it switches at two different input levels, which stops noisy or slow signals from making the output chatter. "
            "This Schmitt trigger calculator gives the upper and lower thresholds and the [hysteresis](https://www.instrumentationblog.in/schmitt-trigger-hysteresis/) band.\n\n"
            "Electronics designers and students use it to set trip points for level switches, thermostats, "
            "zero crossing detectors and button inputs, where a clean single transition matters."),
     before='## Common mistakes',
     body_add=f'''
## Standard R₂ values with R₁ = 10 kΩ

With V<sub>ref</sub> = 2.5 V and a 0 to 5 V output:

| R₂ | Hysteresis | V<sub>TH</sub> | V<sub>TL</sub> |
|---|---|---|---|
{sr}
## Effect of a real reference and a real output

The default case gives {VTH:.4f} V and {VTL:.4f} V. Two practical effects move these numbers:

- **Divider reference.** If the 2.5 V comes from two 10 kΩ resistors across 5 V, their Thevenin resistance of 5 kΩ adds to R₁. The thresholds become **{VTHe:.4f} V** and **{VTLe:.4f} V**, so the hysteresis grows to **{(VTHe-VTLe)*1000:.1f} mV**. Buffer the reference or include the 5 kΩ in R₁.
- **Output that does not reach the rails.** With V<sub>OH</sub> = 4.8 V and V<sub>OL</sub> = 0.2 V under load, the thresholds are **{VTHl:.4f} V** and **{VTLl:.4f} V**, a hysteresis of **{(VTHl-VTLl)*1000:.1f} mV**.

The feedback resistor itself draws only ({Voh:g} − {VTH:.3f}) ÷ 100 kΩ = {Ifb*1e6:.1f} µA from the output, so loading by R₂ is rarely a problem.

## Checking the thresholds on the bench

Drive the input with a slow triangle wave that sweeps a little beyond both thresholds, put the input on channel 1 and the output on channel 2 of an oscilloscope, and use XY mode. The trace draws a rectangular loop whose left and right edges sit at V<sub>TL</sub> and V<sub>TH</sub>. Without a scope, ramp a bench supply slowly and note the input voltage at each output change with a multimeter. Do the test at the operating temperature if the threshold matters, because comparator offset drifts.
''',
     faq_add=[('Can I build a Schmitt trigger with an op amp instead of a comparator?',
               'Yes, but an op amp is slower to come out of saturation and its output may not reach the rails. Use the op amp\'s measured output swing for V_OH and V_OL, and prefer a comparator when edges must be fast.')])

# ---------------------------------------------------------------- Crystal load capacitance
C1, C2, Cs = 22.0, 22.0, 5.0
CL = C1 * C2 / (C1 + C2) + Cs
# pulling with assumed motional C1m and shunt C0
Cm, C0 = 0.015, 5.0  # pF
def ppm(cl_act, cl_spec): return Cm / 2 * (1 / (C0 + cl_act) - 1 / (C0 + cl_spec)) * 1e6
pr = ''
for cl in (10, 12, 14, 16, 18, 20, 22):
    pr += f"| {cl} pF | {ppm(cl,16):+.1f} ppm | {ppm(cl,16)*16e6/1e6:+,.0f} Hz |\n"
sh12 = ppm(16, 12)
# critical gm for 16 MHz, ESR 40 ohm
F, ESR = 16e6, 40.0
gm = 4 * ESR * (2 * pi * F) ** 2 * ((C0 + CL) * 1e-12) ** 2
# probe effect: 10 pF probe on XOUT in parallel with C2
C2p = C2 + 10
CLp = C1 * C2p / (C1 + C2p) + Cs

edit('electronics/crystal-load-capacitance', date=U, phrase='crystal load capacitance calculator',
     intro=("A quartz crystal only runs at its marked frequency when the circuit presents the load capacitance it was cut for. "
            "This crystal load capacitance calculator finds the effective load from the two capacitors of a Pierce oscillator plus board stray capacitance. "
            "See how a [crystal oscillator works](https://www.instrumentationblog.in/crystal-oscillator-working-principle/).\n\n"
            "Hardware designers use it to pick capacitors for microcontroller, RTC and radio clocks, "
            "where a wrong load shifts the frequency or stops the oscillator starting."),
     body_add=f'''
## Worked example with the default inputs

With C1 = C2 = {C1:g} pF and {Cs:g} pF of stray capacitance, the two capacitors appear in series across the crystal: {C1:g} × {C2:g} ÷ {C1+C2:g} = {C1*C2/(C1+C2):g} pF. Adding the stray gives **C<sub>L</sub> = {CL:g} pF**, so this layout suits a crystal specified for 16 pF.

If the same board is fitted with a 12 pF crystal, the circuit loads it with 4 pF too much. Using typical values for a fundamental mode AT cut crystal (motional capacitance C<sub>1</sub> ≈ {Cm*1000:g} fF, shunt capacitance C<sub>0</sub> ≈ {C0:g} pF), the pulling is:

<p class="formula">Δf/f ≈ (C<sub>1</sub> ÷ 2) × [1 ÷ (C<sub>0</sub> + C<sub>L,actual</sub>) − 1 ÷ (C<sub>0</sub> + C<sub>L,spec</sub>)]</p>

That gives **{sh12:+.0f} ppm**, which is larger than the ±20 ppm tolerance of many crystals. The equal capacitor fix is 2 × (12 − 5) = 14 pF; the nearest standard value is 15 pF.

## Frequency pulling around a 16 pF crystal

Using the same typical C<sub>1</sub> and C<sub>0</sub>, for a 16 MHz crystal specified at 16 pF:

| Actual load | Frequency error | At 16 MHz |
|---|---|---|
{pr}
Look up C<sub>1</sub> and C<sub>0</sub> on the crystal datasheet for exact figures; small 32.768 kHz tuning fork crystals pull far more per picofarad.

## Will the oscillator start?

More load capacitance makes the oscillator harder to start. A common check (from microcontroller oscillator application notes) is the critical transconductance:

<p class="formula">g<sub>m,crit</sub> = 4 × ESR × (2πf)² × (C<sub>0</sub> + C<sub>L</sub>)²</p>

For 16 MHz, ESR = {ESR:g} Ω, C<sub>0</sub> = {C0:g} pF and C<sub>L</sub> = {CL:g} pF, g<sub>m,crit</sub> = **{gm*1e3:.2f} mA/V**. The oscillator's transconductance from the datasheet should be at least 5 times this for a safe gain margin.

## Measuring the frequency

Do not hang an oscilloscope probe on the crystal pins: a 10 pF probe on XOUT turns C2 into {C2p:g} pF and the load into {CLp:.2f} pF, which pulls the frequency while you watch. Route the clock to an output pin (many microcontrollers have a clock output or a timer toggle) and read it with a frequency counter, or use a near field probe.

## Common mistakes

- **Setting C1 and C2 equal to C<sub>L</sub>.** The caps are in series, so each must be about twice C<sub>L</sub> minus the stray.
- **Ignoring stray capacitance.** Pin capacitance and traces add 2 to 7 pF, which matters most for 6 pF and 7 pF watch crystals.
- **Copying 22 pF from an old design.** It suits only 16 to 20 pF crystals.
- **Using high tolerance or Y5V capacitors.** Use C0G (NP0) ceramics so the load does not drift with temperature.
- **Long traces or vias under the crystal.** They add stray capacitance and pick up noise; keep the crystal close to the chip with a ground guard.
''',
     faq_add=[('How do I measure crystal frequency without disturbing it?',
               f'Output the clock on a spare pin and use a frequency counter. A 10 pF scope probe on XOUT raises the load in the example from {CL:g} pF to {CLp:.2f} pF and shifts the frequency.'),
              ('What is the critical transconductance of a crystal oscillator?',
               f'g_m,crit = 4 × ESR × (2πf)² × (C0 + CL)². It is the minimum gain needed to sustain oscillation. For 16 MHz, 40 Ω ESR, 5 pF C0 and 16 pF CL it is {gm*1e3:.2f} mA/V; aim for 5 times margin.')])

# ---------------------------------------------------------------- Transistor base resistor
Vin, Vbe, Ic, hfe, k = 5.0, 0.7, 0.100, 100, 5
Ib = Ic / hfe * k
Rb = (Vin - Vbe) / Ib
Rstd = 820
Ib2 = (Vin - Vbe) / Rstd
fb = Ic / Ib2
Pq = Ic * 0.2
PRb = (Vin - Vbe) * Ib2
# 3.3 V
Rb33 = (3.3 - Vbe) / Ib
# with 10k pull-down
Ipd = Vbe / 10e3
Rb_pd = (Vin - Vbe) / (Ib + Ipd)
tr = ''
for ic in (0.020, 0.050, 0.100, 0.200, 0.500):
    ib = ic / hfe * k
    tr += f"| {ic*1000:g} mA | {ib*1000:g} mA | {(3.3-Vbe)/ib:,.0f} Ω | {(Vin-Vbe)/ib:,.0f} Ω |\n"

edit('electronics/transistor-base-resistor', date=U, phrase='transistor base resistor calculator',
     intro=("To use a bipolar transistor as a switch for a relay, LED strip or buzzer, the base must get enough current to saturate it fully. "
            "This transistor base resistor calculator works out the resistor from the load current, gain and drive voltage. "
            "See the [basics of transistors](https://www.instrumentationblog.in/basics-of-transistors/).\n\n"
            "Hobbyists, students and embedded engineers use it when a microcontroller pin must drive a load "
            "that needs more current or voltage than the pin can supply."),
     body_add=f'''
## Worked example with the default inputs

A 5 V pin drives a 100 mA load through an NPN transistor with minimum hFE 100, V<sub>BE</sub> 0.7 V and 5 times overdrive:

- Minimum base current = 100 mA ÷ 100 = 1 mA; with overdrive I<sub>B</sub> = **{Ib*1000:g} mA**
- R<sub>B</sub> = ({Vin:g} − {Vbe:g}) ÷ {Ib*1000:g} mA = **{Rb:,.0f} Ω**

Rounding down to the standard **820 Ω** gives I<sub>B</sub> = 4.3 ÷ 820 = **{Ib2*1000:.2f} mA**, a forced beta of {Ic*1000:g} ÷ {Ib2*1000:.2f} = **{fb:.1f}**. The resistor dissipates 4.3 V × {Ib2*1000:.2f} mA = {PRb*1000:.1f} mW, so any 0.125 W part is fine. With V<sub>CE(sat)</sub> ≈ 0.2 V the transistor dissipates about {Pq*1000:.0f} mW.

From a 3.3 V pin the same load needs (3.3 − 0.7) ÷ 5 mA = **{Rb33:,.0f} Ω**, so use 510 Ω. If you add a 10 kΩ base to emitter resistor, it steals 0.7 ÷ 10 kΩ = {Ipd*1000:.2f} mA; to keep 5 mA into the base the 5 V resistor becomes {Rb_pd:,.0f} Ω, which still rounds to 820 Ω.

## Base resistor for common loads (hFE 100, 5 times overdrive)

| Load current | Base current | R<sub>B</sub> from 3.3 V | R<sub>B</sub> from 5 V |
|---|---|---|---|
{tr}
At 500 mA the 25 mA base current exceeds most microcontroller pins. Use a Darlington, a two stage driver or a logic level MOSFET for loads that large.

## Checking saturation in the circuit

With the load connected and the pin high, measure collector to emitter with a multimeter. A saturated small signal transistor reads about 0.05 to 0.3 V. A reading of 1 V or more means it is in the active region: increase the base current, or the transistor will heat and the load will see less voltage. Also check the pin voltage under load; if it sags well below the supply, the pin is overloaded.

## Common mistakes

- **Using the typical hFE.** Design with the minimum gain at your collector current, which can be a third of the headline figure.
- **Forgetting V<sub>BE</sub>.** Dividing the full 5 V by the base current gives a resistor about 16% too large.
- **Driving a PNP high side switch from a low voltage pin.** A 3.3 V pin cannot turn off a PNP whose emitter sits at 12 V; add an NPN stage to pull its base.
- **No flyback diode on a relay or solenoid.** The turn off spike can exceed the transistor's V<sub>CEO</sub> and destroy it.
- **Leaving the base floating at reset.** Pins are inputs during power up, so a pull down keeps the load off.
''',
     faq_add=[('How do I check that the transistor is saturated?',
               'Measure V_CE with the load on. Below about 0.3 V for a small signal BJT means it is saturated. If it is near 1 V or more, increase the base current by lowering R_B.'),
              ('What base resistor do I need from a 3.3 V microcontroller?',
               f'For a 100 mA load with hFE 100 and 5 times overdrive, R_B = (3.3 − 0.7) ÷ 5 mA = {Rb33:,.0f} Ω, so use 510 Ω. Check the pin can source 5 mA.')])

print('done')

# ======================================================================= SECTION _expand_c4.py
"""Part C expand (2026-11-17), slice 4: dissolved-oxygen-saturation, i2c-pull-up-resistor, modulo,
bomb-calorimeter, system-of-3-equations, limiting-reagent. Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-17'

# ---------------------------------------------------------------- Dissolved oxygen saturation
def do_c0(t, S=0.0):
    T = t + 273.15
    return math.exp(-139.34411 + 1.575701e5 / T - 6.642308e7 / T ** 2 + 1.2438e10 / T ** 3 - 8.621949e11 / T ** 4
                    - S * (1.7674e-2 - 10.754 / T + 2140.7 / T ** 2))


def do_cs(t, P_kpa, S=0.0):
    T = t + 273.15
    p = P_kpa / 101.325
    pw = math.exp(11.8571 - 3840.7 / T - 216961 / T ** 2)
    th = 0.000975 - 1.426e-5 * t + 6.436e-8 * t * t
    return do_c0(t, S) * p * (1 - pw / p) * (1 - th * p) / ((1 - pw) * (1 - th))


def patm(h):
    return 101.325 * (1 - 2.25577e-5 * h) ** 5.25588


c20 = do_c0(20)
sat20 = 7.5 / c20 * 100
# field example: 1,200 m site, 12 degC river, reading 9.6 mg/L
hF, tF, rF = 1200, 12.0, 9.6
PF = patm(hF)
csF = do_cs(tF, PF)
sea12 = do_cs(tF, 101.325)
satF = rF / csF * 100
satF_wrong = rF / sea12 * 100
# mmHg for the station pressure
PF_mmHg = PF * 1000 / 133.322
# warm-up: same sample warmed from 12 to 25 degC loses capacity
c25 = do_cs(25, PF)
alt_rows = ''
for h in (0, 500, 1000, 1500, 2000, 3000):
    P = patm(h)
    alt_rows += f"| {h:,} m | {P:.1f} kPa | {do_cs(10, P):.2f} | {do_cs(20, P):.2f} | {do_cs(30, P):.2f} |\n"

edit('chemistry/dissolved-oxygen-saturation', date=U, phrase='dissolved oxygen saturation calculator',
     intro=("Water in contact with air holds a fixed amount of oxygen that falls as temperature and salinity rise and as barometric pressure drops. "
            "This dissolved oxygen saturation calculator uses the Benson and Krause equations from Standard Methods to give the saturation value in mg/L and a sample's percent saturation.\n\n"
            "Water quality technicians, aquaculture operators and wastewater engineers use it to calibrate an "
            "[optical dissolved oxygen sensor](https://www.instrumentationblog.in/how-do-optical-dissolved-oxygen-sensors-work/), "
            "judge aeration and report results."),
     body_add=f'''
## Dissolved oxygen saturation against altitude

Using the standard atmosphere to estimate station pressure, fresh water saturation (mg/L) falls with elevation:

| Elevation | Station pressure | 10 °C | 20 °C | 30 °C |
|---|---|---|---|---|
{alt_rows}
Real pressure varies a few kPa with the weather, so use a barometer reading when you have one rather than the elevation estimate.

## Field example: river sample at altitude

A river sampled at {hF:,} m elevation is at {tF:g} °C and the probe reads {rF:g} mg/L. The standard atmosphere gives a station pressure of about **{PF:.1f} kPa** ({PF_mmHg:.0f} mmHg).

- Saturation at that pressure = **{csF:.2f} mg/L**
- Percent saturation = {rF:g} ÷ {csF:.2f} × 100 = **{satF:.1f}%**
- Using the sea level value of {sea12:.2f} mg/L instead would report only {satF_wrong:.1f}%, wrongly suggesting an oxygen deficit

The sample is slightly supersaturated, which is normal for a turbulent mountain stream or for water with algae photosynthesising in daylight. If the same water warmed to 25 °C its capacity would drop to {c25:.2f} mg/L, so warm afternoon stretches of a river are the first to stress fish.

## How DO probes use the saturation value

- **Air calibration.** The probe is held in water saturated air (a damp sponge in the calibration cup). The meter reads the barometer and temperature and sets its 100% point to the saturation value from this equation.
- **Salinity compensation.** Optical and membrane probes respond to oxygen partial pressure, not concentration. The meter converts to mg/L with the salinity you enter, so a seawater sample read with salinity left at 0 is overstated by about 20%.
- **Zero check.** A fresh sodium sulfite solution removes all oxygen and should read below about 0.2 mg/L.
- **BOD bottles.** Dilution water is aerated to near saturation before the five day biochemical oxygen demand test, and the starting DO is checked against this value.

## Common mistakes

- **Using sea level corrected pressure.** Weather reports adjust pressure to sea level. A DO meter needs the actual station pressure, which can be 10 to 20 kPa lower at a hill site.
- **Mixing up mg/L and percent saturation.** Fish tolerance limits are usually set in mg/L, while aeration control often uses percent. A reading of 100% at 30 °C is only {do_c0(30):.2f} mg/L.
- **Ignoring temperature equilibrium.** The probe and the sample must be at the same temperature; reading a cold sample with a warm probe during the first minute gives a drifting value.
- **Leaving salinity at zero in brackish water.** Estuaries and cooling towers with high dissolved solids need the salinity entered, or the saturation is overstated.
- **Treating supersaturation as a fault.** Values over 100% are real when water is aerated under pressure, downstream of dams or during algal blooms.
''',
     faq_add=[('Why does my DO meter read above 100% saturation?',
               f'Water can hold more oxygen than its air equilibrium value for a while, for example below a weir, in a pressurised aeration line or when algae photosynthesise. A stream at {tF:g} °C and {hF:,} m reading {rF:g} mg/L is {satF:.1f}% saturated.'),
              ('Does dissolved oxygen saturation depend on the oxygen content of air only?',
               'It depends on the oxygen partial pressure above the water. Air is 20.95% oxygen everywhere, so saturation changes with total barometric pressure, temperature and salinity. Water in contact with pure oxygen holds nearly five times as much.')])

# ---------------------------------------------------------------- I2C pull-up resistor
Vdd, tr, Vol, Iol, Cb, Rp = 3.3, 300e-9, 0.4, 3e-3, 200e-12, 2.2e3
k = math.log(0.7 / 0.3)
Rmin = (Vdd - Vol) / Iol
Rmax = tr / (k * Cb)
trp = k * Rp * Cb
Is = (Vdd - Vol) / Rp
# power while low
Plow = Vdd ** 2 / Rp
Iavg = Vdd / Rp * 0.5
# three breakout boards each with 10k pull-ups plus a 4.7k on the main board
Rpar = 1 / (3 / 10e3 + 1 / 4.7e3)
tr_par = k * Rpar * Cb
R8 = 1 / (9 / 10e3 + 1 / 4.7e3)
assert R8 < Rmin
# E12 table at default bus
e_rows = ''
passing = []
for r in (1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 4.7):
    R = r * 1e3
    t = k * R * Cb
    i = (Vdd - Vol) / R
    ok = 'Yes' if (R >= Rmin and t <= tr) else 'No'
    if ok == 'Yes':
        passing.append(f'{r:g} kΩ')
    e_rows += f"| {r:g} kΩ | {t*1e9:.0f} ns | {i*1e3:.2f} mA | {ok} |\n"
# 5 V bus
Rmin5 = (5.0 - 0.4) / 3e-3
Rmax100 = 1e-6 / (k * 200e-12)

edit('electronics/i2c-pull-up-resistor', date=U, phrase='I2C pull-up resistor calculator',
     intro=("I²C lines are open drain, so the pull-up resistors set both the current a device must sink when it pulls a line low and the rise time of every edge. "
            "This I2C pull-up resistor calculator finds the allowed range from the I²C specification.\n\n"
            "Embedded and hardware designers use it when adding sensors to a bus or debugging corrupted data. "
            "See [pull-up and pull-down resistor values](https://www.instrumentationblog.in/pull-up-pull-down-resistor-values/) and "
            "[SPI vs I²C](https://www.instrumentationblog.in/spi-vs-i2c-protocol-comparison/)."),
     body_add=f'''
## Standard resistor values on the example bus

For the default bus (3.3 V, Fast mode, 200 pF, 3 mA sink), the window is {Rmin:,.0f} Ω to {Rmax:,.0f} Ω:

| Pull-up | Rise time (30 to 70%) | Sink current | Within limits |
|---|---|---|---|
{e_rows}
Only {', '.join(passing[:-1])} and {passing[-1]} pass. The default 2.2 kΩ gives {trp*1e9:.0f} ns, above the 300 ns limit, and 1.8 kΩ just misses at {k*1.8e3*Cb*1e9:.0f} ns.

## Pull-ups on breakout boards add in parallel

Many sensor modules carry their own 10 kΩ pull-ups. With three such modules and a 4.7 kΩ on the main board, the line sees 1 ÷ (3/10 kΩ + 1/4.7 kΩ) = **{Rpar:,.0f} Ω**, a {tr_par*1e9:.0f} ns rise time at 200 pF, fine for 100 kHz but too slow for 400 kHz. Keep adding modules and the problem flips: with nine of them the total is **{R8:,.0f} Ω**, below the {Rmin:,.0f} Ω minimum, and a 3 mA driver can no longer pull the line under 0.4 V. Remove the extra resistors with a solder jumper so the bus has one deliberate pull-up per line.

## Power and supply voltage

While a line is held low the pull-up burns V² ÷ R. For 2.2 kΩ on 3.3 V that is {Plow*1e3:.2f} mW, or roughly {Iavg*1e3:.2f} mA average per line at a 50% low duty. Battery designs therefore pick the highest value that still meets the rise time, often at 100 kHz.

On a 5 V bus the minimum rises to (5.0 − 0.4) ÷ 3 mA = **{Rmin5:,.0f} Ω**, while the maximum at 100 kHz and 200 pF is {Rmax100:,.0f} Ω, so 2.2 kΩ to 4.7 kΩ is a common choice there.

## Checking the bus with an oscilloscope

Probe SDA or SCL with a 10x probe and trigger on a rising edge. Measure from 30% to 70% of V<sub>DD</sub> (0.99 V to 2.31 V on a 3.3 V bus) and compare with the mode limit. You can then work backwards: C<sub>b</sub> = t<sub>r</sub> ÷ (0.8473 × R<sub>p</sub>). Also check the low level stays under 0.4 V when the weakest device pulls down.

## Common mistakes

- **Copying 4.7 kΩ from an Arduino example.** That suits 100 kHz and short wiring; at 400 kHz with a few modules it is usually too slow.
- **Forgetting module pull-ups.** Three or four boards in parallel can drop the total below R<sub>min</sub> and the low level fails.
- **Measuring rise time 10% to 90%.** The I²C specification uses 30% to 70%; the 10% to 90% time is about 2.6 times longer and would wrongly suggest a failure.
- **Pulling up to the wrong rail.** A 5 V pull-up on a 3.3 V only device can damage it; use a level shifter or a 3.3 V pull-up when all devices accept it.
- **Long cables without a buffer.** Over about 1 m of cable the capacitance passes 400 pF; use a bus extender or differential I²C.
''',
     faq_add=[('What happens if the I2C pull-up resistor is too small?',
               f'The devices cannot sink enough current to bring the line under V_OL, so a low may read as high. On a 3.3 V bus with 3 mA drivers anything under about {Rmin:,.0f} Ω risks this, and it also wastes power.'),
              ('Do SDA and SCL need the same pull-up value?',
               'Usually yes, since both lines see similar capacitance. If SCL is driven push-pull by a single master it can tolerate a weaker pull-up, but most designs fit equal values for simplicity.')])

# ---------------------------------------------------------------- Modulo
a, b = 17, 5
q = math.floor(a / b)
m = a % b
# day of week: 100 days after a Tuesday
d100 = 100 % 7
# modular exponentiation 7^100 mod 13
pw = pow(7, 100, 13)
ph = 100 % 12  # Fermat: 7^12 = 1 mod 13
# ISBN-10 check digit for 0-306-40615-?
digits = [0, 3, 0, 6, 4, 0, 6, 1, 5]
s = sum((10 - i) * d for i, d in enumerate(digits))
chk = (11 - s % 11) % 11
# Luhn for 7992739871
luhn = '7992739871'
tot = 0
for i, ch in enumerate(reversed(luhn)):
    dd = int(ch)
    if i % 2 == 0:
        dd *= 2
        if dd > 9:
            dd -= 9
    tot += dd
lchk = (10 - tot % 10) % 10
# table of powers of 2 mod 7 and residues
mod_rows = ''
for n in (2, 3, 7, 9, 10, 11, 12):
    mod_rows += f"| {n} | {2026 % n} | {(-2026) % n} | {pow(2, 2026, n)} |\n"

edit('math/modulo', date=U, phrase='modulo calculator',
     intro=("The modulo operation gives the remainder left after dividing one number by another, the basis of clock arithmetic, check digits and cyclic counters. "
            "This modulo calculator returns a mod b, the integer quotient and the remainder.\n\n"
            "Programmers, maths students and anyone working with schedules use it to check remainders, wrap indexes and see why negative numbers give "
            "different answers in Python and in C, Java or JavaScript."),
     body_add=f'''
## Rules of modular arithmetic

Remainders can be taken at every step of a sum or product without changing the final remainder, which keeps numbers small:

<p class="formula">(x + y) mod n = [(x mod n) + (y mod n)] mod n &nbsp;·&nbsp; (x × y) mod n = [(x mod n) × (y mod n)] mod n</p>

For example (17 × 23) mod 5 = (2 × 3) mod 5 = **{(17*23) % 5}**, and 391 ÷ 5 leaves the same remainder.

## Worked examples in daily use

- **Day of the week.** 100 days after a Tuesday: 100 mod 7 = **{d100}**, so it falls {d100} days after Tuesday, on a Thursday.
- **Large powers.** 7¹⁰⁰ mod 13 is found by repeated squaring, reducing mod 13 at every step. Because 13 is prime, Fermat's little theorem gives 7¹² ≡ 1, so 7¹⁰⁰ ≡ 7^(100 mod 12) = 7⁴ = 2,401 ≡ **{pw}** (mod 13).
- **ISBN-10 check digit.** For 0-306-40615-?, the weighted sum 10×0 + 9×3 + 8×0 + 7×6 + 6×4 + 5×0 + 4×6 + 3×1 + 2×5 = {s}. The check digit is (11 − {s} mod 11) mod 11 = **{chk}**.
- **Luhn check for card numbers.** For the payload 7992739871, doubling every second digit from the right and summing gives {tot}; the check digit is (10 − {tot} mod 10) mod 10 = **{lchk}**.

## Residues of 2026

| Modulus n | 2026 mod n | −2026 mod n (floored) | 2²⁰²⁶ mod n |
|---|---|---|---|
{mod_rows}
## Modulo in code

- Python: `-17 % 5` gives 3 (floored); `math.fmod(-17, 5)` gives −2.0 (truncated).
- C, Java, JavaScript: `-17 % 5` gives −2. For a non-negative index use `((a % b) + b) % b`.
- Excel and Google Sheets: `=MOD(-17, 5)` gives 3, the floored result.
- For powers of 2, `x % 8` equals `x & 7` for non-negative integers, which compilers use as a fast shortcut.

## Common mistakes

- **Assuming % is always positive.** A ring buffer index of `(i − 1) % size` in C or Java goes negative when i = 0 and reads outside the array.
- **Dividing by zero.** a mod 0 is undefined; the calculator returns no result rather than a remainder.
- **Using floating point for big integers.** In JavaScript, numbers above 2⁵³ lose precision, so a large mod gives a wrong answer; use BigInt.
- **Mixing up quotient direction.** For −17 ÷ 5 the floored quotient is −4, not −3; the remainder only works out if the quotient matches the convention used.
- **Reducing too late.** Computing 7¹⁰⁰ first and then taking mod 13 overflows; reduce after every multiplication.
''',
     faq_add=[('How do I calculate mod on a normal calculator?',
               'Divide a by b, take the whole number part of the result, multiply it by b and subtract from a. For 17 mod 5: 17 ÷ 5 = 3.4, 3 × 5 = 15 and 17 − 15 = 2. For negative a, round the quotient down rather than towards zero to get the floored result.'),
              ('What does congruent modulo n mean?',
               'Two numbers are congruent modulo n when they leave the same remainder on division by n, written a ≡ b (mod n). For example 38 ≡ 14 (mod 12) because both leave 2, which is why 38 hours after midnight a clock reads 2.')])

# ---------------------------------------------------------------- Bomb calorimeter
C, dT, qf, mm, M, dn, T = 10.0, 2.648, 50.0, 1.0, 122.12, -0.5, 298.15
qk = C * dT - qf / 1000
Ug = -qk / mm
Um = Ug * M
Hm = Um + dn * 8.314462618e-3 * T
# calibration run: 0.9875 g benzoic acid, rise 2.6158 K, 48 J fuse, 26.434 kJ/g
mb, rb, fb = 0.9875, 2.6158, 48.0
Ccal = (mb * 26.434 + fb / 1000) / rb
# coal sample: 1.0250 g, rise 2.9120 K, fuse 45 J, acid 62 J, H 5.0 %, moisture ignored
mc, rc, fc, ac, Hc = 1.0250, 2.9120, 45.0, 62.0, 0.050
qc = Ccal * rc - (fc + ac) / 1000
gcv = qc / mc
water = 9 * Hc  # g water per g fuel
ncv = gcv - water * 2.442  # latent heat at 25 degC, kJ/g
# delta n table
fuels = (('Methane CH₄', 'CH₄ + 2O₂ → CO₂ + 2H₂O', 1 - 3),
         ('Ethanol C₂H₅OH(l)', 'C₂H₅OH + 3O₂ → 2CO₂ + 3H₂O', 2 - 3),
         ('Glucose C₆H₁₂O₆(s)', 'C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O', 6 - 6),
         ('Naphthalene C₁₀H₈(s)', 'C₁₀H₈ + 12O₂ → 10CO₂ + 4H₂O', 10 - 12),
         ('Octane C₈H₁₈(l)', 'C₈H₁₈ + 12.5O₂ → 8CO₂ + 9H₂O', 8 - 12.5))
dn_rows = ''
for nm, eq, d in fuels:
    dn_rows += f"| {nm} | {eq} | {d:g} | {d*8.314462618e-3*T:+.2f} kJ/mol |\n"

edit('chemistry/bomb-calorimeter', date=U, phrase='bomb calorimeter calculator',
     intro=("In a bomb calorimeter a sample burns in oxygen inside a sealed steel vessel, so the heat released raises the temperature of the calorimeter at constant volume. "
            "This bomb calorimeter calculator turns the calorimeter constant and temperature rise into the heat released, ΔcU and ΔcH.\n\n"
            "Fuel laboratories, food scientists and chemistry students use it to find calorific values of coal, oils and biomass, "
            "check calibrations and work through thermochemistry practicals."),
     body_add=f'''
## Calibrating the calorimeter constant

Before testing unknowns, burn a pellet of certified benzoic acid (26.434 kJ/g). With a {mb} g pellet, a corrected rise of {rb} K and {fb:g} J of fuse wire:

<p class="formula">C<sub>cal</sub> = (m × 26.434 + q<sub>fuse</sub>) ÷ ΔT</p>

- C<sub>cal</sub> = ({mb} × 26.434 + 0.{int(fb):03d}) ÷ {rb} = **{Ccal:.3f} kJ/K**

Laboratories repeat this five or more times and accept the mean when the relative standard deviation is below about 0.1%.

## Fuel example: gross and net calorific value of coal

A {mc} g coal sample in the calorimeter above gives a corrected rise of {rc} K. The fuse correction is {fc:g} J and titrating the bomb washings shows {ac:g} J from nitric and sulfuric acid.

- q = {Ccal:.3f} × {rc} − ({fc:g} + {ac:g}) ÷ 1000 = **{qc:.2f} kJ**
- Gross calorific value = {qc:.2f} ÷ {mc} = **{gcv:.2f} kJ/g** ({gcv:.2f} MJ/kg)
- With {Hc*100:g}% hydrogen, each gram forms 9 × {Hc:.3f} = {water:.2f} g of water. Subtracting its latent heat (2.442 kJ/g at 25 °C) gives a net value of about **{ncv:.2f} MJ/kg**

Boiler efficiency in Europe and India is usually quoted on the net value, while the bomb measures the gross value, so always state which basis a figure uses.

## Δn(g) and the ΔH correction for common fuels

Water is taken as liquid, the state it ends in inside the bomb. At 25 °C:

| Fuel | Balanced combustion | Δn(g) | Δn·RT |
|---|---|---|---|
{dn_rows}
The correction is a few kJ/mol at most, under 0.3% of the energy of combustion, but it must be included for tabulated enthalpies.

## Test procedure in brief

1. Press the sample into a pellet, weigh it to 0.1 mg and place it in the crucible with a measured length of fuse wire touching it.
2. Add 1 mL of water to the bomb so acids dissolve, seal it and fill with oxygen to about 30 bar.
3. Immerse the bomb in a weighed quantity of water in the bucket, let the temperature drift settle and record it.
4. Fire, record the temperature until it rises and levels off, and correct the rise for heat leak.
5. Release the gas slowly, wash the interior and titrate for acid, and measure any unburnt wire.

## Common mistakes

- **Leaving out the minus sign.** Heat released by the sample is positive q, but ΔcU and ΔcH are negative.
- **Using the raw temperature rise.** Without correcting for heat exchange during the run the result can be 0.5% to 1% off.
- **Including water vapour in Δn(g).** Water condenses in the bomb, so it counts as liquid.
- **Changing the bucket water mass.** The calorimeter constant only applies to the same water mass used in calibration, usually weighed to 0.1 g.
- **Incomplete combustion.** Soot in the crucible means not all carbon burnt; the run must be rejected, not corrected.
''',
     faq_add=[('How do I convert gross calorific value to net calorific value?',
               f'Subtract the latent heat of the water formed: NCV ≈ GCV − 2.442 × (9H + W), with H the hydrogen and W the moisture mass fractions, in MJ/kg. A coal at {gcv:.2f} MJ/kg gross with 5% hydrogen is about {ncv:.2f} MJ/kg net.')])

# ---------------------------------------------------------------- System of 3 equations
A = [[1, 1, 1], [2, -1, 3], [1, 2, -1]]
d = [6, 9, 2]


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


D = det3(A)
sol = []
for j in range(3):
    Mj = [row[:] for row in A]
    for i in range(3):
        Mj[i][j] = d[i]
    sol.append(det3(Mj) / D)
x, y, z = sol
# elimination steps: R2 - 2R1, R3 - R1
r2 = [A[1][k] - 2 * A[0][k] for k in range(3)] + [d[1] - 2 * d[0]]
r3 = [A[2][k] - A[0][k] for k in range(3)] + [d[2] - d[0]]
# r2 = [0,-3,1,-3]; r3 = [0,1,-2,-4]; r3 + r2/3
f = r3[1] / r2[1]
r3b = [r3[k] - f * r2[k] for k in range(4)]
zE = r3b[3] / r3b[2]
yE = (r2[3] - r2[2] * zE) / r2[1]
xE = d[0] - yE - zE
assert r2 == [0, -3, 1, -3] and r3 == [0, 1, -2, -4] and (x, y, z) == (1, 2, 3) and zE == 3
# mesh circuit example: 3 loop currents
Mc = [[15, -5, 0], [-5, 25, -10], [0, -10, 20]]
Vc = [10, 0, -5]
Dc = det3(Mc)
Ic = []
for j in range(3):
    Mj = [row[:] for row in Mc]
    for i in range(3):
        Mj[i][j] = Vc[i]
    Ic.append(det3(Mj) / Dc)
# singular example
S1 = [[1, 2, 3], [2, 4, 6], [1, 1, 1]]
DS = det3(S1)

edit('math/system-of-3-equations', date=U, phrase='3 variable system of equations calculator',
     intro=("Three linear equations in three unknowns describe three planes, and when they meet at a single point the system has one solution. "
            "This 3 variable system of equations calculator finds that point with Cramer's rule, showing D, Dx, Dy and Dz.\n\n"
            "Students use it to check homework and exam working, and engineers use it for small problems such as mesh currents in a circuit, "
            "mixture blends and fitting a parabola through three points."),
     body_add=f'''
## The same system by Gaussian elimination

Elimination reaches the same answer and shows why D matters. Starting from x + y + z = 6, 2x − y + 3z = 9 and x + 2y − z = 2:

1. Equation 2 − 2 × equation 1 gives **−3y + z = −3**.
2. Equation 3 − equation 1 gives **y − 2z = −4**.
3. Three times the second new equation plus the first removes y: **−5z = −15**, so z = **{zE:g}**.
4. Back substitution: −3y + {zE:g} = −3 gives y = **{yE:g}**, and x = 6 − {yE:g} − {zE:g} = **{xE:g}**.

## Engineering example: three mesh currents

A resistor network has three loops. Kirchhoff's voltage law gives, with currents in amps:

- 15I₁ − 5I₂ = 10
- −5I₁ + 25I₂ − 10I₃ = 0
- −10I₂ + 20I₃ = −5

Enter a₁ = 15, b₁ = −5, c₁ = 0, d₁ = 10 and so on. D = **{Dc:,.0f}**, giving I₁ = **{Ic[0]:.4f} A**, I₂ = **{Ic[1]:.4f} A** and I₃ = **{Ic[2]:.4f} A**. The negative I₃ means that loop current flows the other way round from the direction assumed.

## What the determinant tells you

| Result | Geometry | Number of solutions |
|---|---|---|
| D ≠ 0 | Three planes meet at one point | Exactly one |
| D = 0 and all of Dx, Dy, Dz = 0 | Planes share a line, or two or three coincide | None or infinitely many, check by elimination |
| D = 0 and any of Dx, Dy, Dz ≠ 0 | Planes do not have a common point | None |

For example x + 2y + 3z, 2x + 4y + 6z and x + y + z have D = **{DS:g}** because the second row is twice the first, so the system cannot have a unique solution whatever the right-hand sides.

## Common mistakes

- **Not lining up the variables.** Rewrite each equation as a·x + b·y + c·z = d before entering; 3z + x = 4 means a = 1, b = 0, c = 3.
- **Moving a term without changing its sign.** x + y = 6 − z must become x + y + z = 6, with c = +1.
- **Replacing the wrong column.** Dy replaces the y column with the right-hand sides, not the y row.
- **Trusting tiny determinants.** If D is very small compared with the coefficients, rounding in the inputs causes large changes in x, y and z; the system is ill conditioned.
- **Skipping the check.** Substitute the answers back into all three original equations; it catches typing errors at once.
''',
     faq_add=[('Can this calculator fit a parabola through three points?',
               'Yes. For y = ax² + bx + c through (x₁, y₁), (x₂, y₂) and (x₃, y₃), each point gives one equation: x₁²·a + x₁·b + 1·c = y₁. Enter x², x and 1 as the three coefficients and y as the right-hand side, and the solution gives a, b and c.')])

# ---------------------------------------------------------------- Limiting reagent
mA, MA, ca, mB, MB, cb, cp, MP = 50.0, 28.014, 1, 10.0, 2.016, 3, 2, 17.031
xA = mA / MA / ca
xB = mB / MB / cb
xi = min(xA, xB)
mP = xi * cp * MP
mAx = (xA - xi) * ca * MA
excess_pct = (xA / xB - 1) * 100
# second example: 2H2 + O2 -> 2H2O, 4.0 g H2, 40.0 g O2
h2, o2 = 4.0, 40.0
xh = h2 / 2.016 / 2
xo = o2 / 31.998 / 1
xi2 = min(xh, xo)
w = xi2 * 2 * 18.015
o2left = (xo - xi2) * 31.998
# percent yield link: 48.0 g NH3 recovered
act = 48.0
py = act / mP * 100
# table: H2 mass varied with 50 g N2
rows = ''
for h in (6, 8, 10, 10.79, 12, 15):
    xb = h / MB / 3
    lim = 'H₂' if xb < xA else ('both' if abs(xb - xA) < 1e-3 else 'N₂')
    prod = min(xA, xb) * 2 * MP
    exN = (xA - min(xA, xb)) * MA
    exH = (xb - min(xA, xb)) * 3 * MB
    rows += f"| {h:g} g | {lim} | {prod:.2f} g | {exN:.2f} g | {exH:.2f} g |\n"
h_stoich = xA * 3 * MB

edit('chemistry/limiting-reagent', date=U, phrase='limiting reagent calculator',
     intro=("In a reaction the limiting reagent is the reactant that runs out first, so it alone fixes how much product can form while the other reactant is left in excess. "
            "This limiting reagent calculator converts both masses to moles and divides by the coefficients to find it.\n\n"
            "Chemistry students use it to check stoichiometry problems, and lab and process chemists use it to plan batch charges, "
            "predict theoretical yield and decide how much excess reagent is worth adding."),
     body_add=f'''
## Changing the hydrogen charge

With 50 g of N₂ fixed, the reactant that limits the ammonia yield depends on how much H₂ is charged. The exact stoichiometric amount is {xA:.4f} × 3 × {MB} = **{h_stoich:.2f} g** H₂:

| H₂ charged | Limiting reagent | NH₃ theoretical yield | N₂ left | H₂ left |
|---|---|---|---|---|
{rows}
Above the stoichiometric point extra hydrogen does not raise the yield; it only ends up as excess.

## Second example: 2H₂ + O₂ → 2H₂O

Burning {h2:g} g of hydrogen in {o2:g} g of oxygen:

- H₂: {h2:g} ÷ 2.016 ÷ 2 = **{xh:.4f}**
- O₂: {o2:g} ÷ 31.998 ÷ 1 = **{xo:.4f}**, so hydrogen is limiting even though it is the smaller mass by a factor of ten
- Water formed = {xi2:.4f} × 2 × 18.015 = **{w:.2f} g**
- Oxygen left = ({xo:.4f} − {xi2:.4f}) × 31.998 = **{o2left:.2f} g**

## Percent excess and percent yield

In the default ammonia example nitrogen is supplied at {xA:.4f} ÷ {xB:.4f} = {xA/xB:.3f} times the amount needed, which is **{excess_pct:.1f}% excess** N₂. If the run recovers {act:g} g of NH₃, the percent yield is {act:g} ÷ {mP:.2f} × 100 = **{py:.1f}%**. Yield is always based on the limiting reagent.

## Why industry uses an excess on purpose

Plants rarely feed reactants in exact proportions. Combustion runs with 10 to 20% excess air so every bit of fuel burns. In esterification an excess of the cheaper alcohol pushes the equilibrium towards the ester. The expensive or hazardous reactant is made the limiting one, so it is used up and does not need recovering.

## Common mistakes

- **Comparing grams instead of moles.** The smaller mass is often not limiting, as the hydrogen examples show.
- **Forgetting to divide by the coefficient.** Comparing 1.78 mol N₂ with 4.96 mol H₂ directly would wrongly make N₂ limiting.
- **Using an unbalanced equation.** Every coefficient feeds the result, so balance first and check atoms on both sides.
- **Using atomic instead of molecular mass.** Hydrogen gas is H₂ at 2.016 g/mol, not 1.008; oxygen gas is 31.998 g/mol.
- **Ignoring purity.** A reagent that is 95% pure supplies only 95% of its weighed mass; correct the mass before entering it.
''',
     faq_add=[('How do I find the limiting reagent with more than two reactants?',
               'Work out moles ÷ coefficient for every reactant. The smallest value is the limiting reagent and also the reaction extent. Run this calculator for each pair if needed; the reactant that is limiting in every pair it appears in is the overall limiting reagent.')])

print('done')

# ======================================================================= SECTION _expand_c5.py
"""Part C expand (2026-11-17), slice 5: frustum-volume, solution-preparation, absolute-gauge-pressure,
water-hardness, generator-frequency. Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-17'
pi = math.pi

# ---------------------------------------------------------------- Frustum volume
R, r, h = 5.0, 3.0, 4.0
V = pi * h / 3 * (R * R + R * r + r * r)
# partly filled bucket: top diameter 30, bottom 25, depth 30 cm, filled to 20 cm
Rb, Rt, H = 12.5, 15.0, 30.0
def fr(a, b, hh): return pi * hh / 3 * (a * a + a * b + b * b)
Vfull = fr(Rb, Rt, H)
y = 20.0
ry = Rb + (Rt - Rb) * y / H
Vy = fr(Rb, ry, y)
fill_rows = ''
for f in (0.25, 0.5, 0.75, 0.9, 1.0):
    yy = H * f
    rr = Rb + (Rt - Rb) * f
    vv = fr(Rb, rr, yy)
    fill_rows += f"| {yy:g} cm ({f*100:.0f}% of depth) | {rr:.2f} cm | {vv/1000:.2f} L | {vv/Vfull*100:.1f}% |\n"
# hopper (inverted frustum, square vs round) example: round hopper top D 2 m, outlet D 0.3 m, cone height 1.5 m
hR, hr, hh = 1.0, 0.15, 1.5
hV = fr(hR, hr, hh)
half = math.degrees(math.atan((hR - hr) / hh))
dens = 750
hm = hV * dens
# cone approximation error with average radius
Vavg = pi * ((R + r) / 2) ** 2 * h
err = (V - Vavg) / V * 100

edit('math/frustum-volume', date=U, phrase='frustum volume calculator',
     intro=("A frustum is a cone with its top cut off parallel to the base, the shape of buckets, flower pots, lampshades and hopper outlets. "
            "This frustum volume calculator gives the volume, slant height, lateral area and total surface area from the two radii and the height.\n\n"
            "Students use it to check geometry homework, while cooks, gardeners and plant engineers use it to find how much a tapered "
            "tub, planter or bin holds before filling or ordering material."),
     body_add=f'''
## Volume of a partly filled bucket

A tapered bucket holds less in its lower half than in its upper half, so the fill level is not proportional to volume. Take a bucket with a {2*Rt:g} cm top, a {2*Rb:g} cm bottom and a depth of {H:g} cm. Full, it holds (π × {H:g} ÷ 3)({Rb:g}² + {Rb:g} × {Rt:g} + {Rt:g}²) = **{Vfull/1000:.2f} L**.

Filled to {y:g} cm, the liquid surface radius is {Rb:g} + ({Rt:g} − {Rb:g}) × {y:g} ÷ {H:g} = **{ry:.3f} cm**, so the liquid is a smaller frustum:

- V = (π × {y:g} ÷ 3)({Rb:g}² + {Rb:g} × {ry:.3f} + {ry:.3f}²) = **{Vy/1000:.2f} L**
- That is {Vy/Vfull*100:.1f}% of the full volume at {y/H*100:.1f}% of the depth.

| Fill depth | Radius at surface | Liquid volume | Share of full |
|---|---|---|---|
{fill_rows}
## Hoppers and silo cones

The outlet cone of a round hopper is an upside down frustum. A hopper with a {2*hR:g} m top, a {2*hr:g} m outlet and a {hh:g} m tall cone holds (π × {hh:g} ÷ 3)({hR:g}² + {hR:g} × {hr:g} + {hr:g}²) = **{hV:.3f} m³**. Filled with grain at about {dens} kg/m³ that is roughly **{hm:,.0f} kg**. The wall makes an angle of atan(({hR:g} − {hr:g}) ÷ {hh:g}) = **{half:.1f}°** with the vertical, which matters because steep walls are needed for mass flow of sticky powders.

## Why averaging the radii is not good enough

A quick estimate uses a cylinder with the mean radius. For the default frustum (R = {R:g} cm, r = {r:g} cm, h = {h:g} cm) that gives π × {(R+r)/2:g}² × {h:g} = {Vavg:.2f} cm³, which is {err:.1f}% below the true {V:.2f} cm³. The error grows as the two ends differ more, so use the exact formula for anything you will pay for by volume.

## Common mistakes

- **Entering diameters as radii.** Buckets and pots are usually sold by diameter; entering 30 cm instead of 15 cm makes the volume four times too large.
- **Measuring the slant side as the height.** h is the vertical distance between the two flat faces. Measuring down the sloping wall overstates it.
- **Using outside dimensions.** For capacity, use the inside radii and depth. A thick plastic or concrete wall can cut the usable volume by 10% or more.
- **Assuming half depth means half full.** In a bucket wider at the top, filling to half depth gives well under half the volume, as the table shows.
- **Forgetting the unit conversion.** 1,000 cm³ is 1 litre and 1 m³ is 1,000 litres; mixing cm and m in one calculation gives wrong powers of ten.
''',
     faq_add=[('How do I find the volume of a partly filled frustum?',
               f'Find the radius at the liquid surface by straight-line interpolation between the bottom and top radii, then apply the frustum formula with that radius and the liquid depth. A {2*Rt:g} cm by {2*Rb:g} cm bucket {H:g} cm deep filled to {y:g} cm holds about {Vy/1000:.2f} L.'),
              ('Is a frustum the same as a truncated pyramid?',
               'Both are solids cut by a plane parallel to the base. A conical frustum has circular ends; a pyramidal frustum has polygon ends. Both follow V = (h/3)(A₁ + A₂ + √(A₁A₂)) with A₁ and A₂ the end areas.')])

# ---------------------------------------------------------------- Solution preparation
c, Vml, M, pur = 0.1, 500.0, 58.44, 0.995
m = c * Vml / 1000 * M / pur
mw = 2.9412  # actual weighed mass
cact = mw * pur / M / (Vml / 1000)
dev = (cact - c) / c * 100
# balance resolution effect
bal_rows = ''
for res, lab in ((0.1, '0.1 g (top pan)'), (0.01, '0.01 g'), (0.001, '1 mg'), (0.0001, '0.1 mg (analytical)')):
    bal_rows += f"| {lab} | ±{res/2:g} g | ±{res/2/m*100:.3f}% |\n"

edit('chemistry/solution-preparation', date=U, phrase='solution preparation calculator',
     intro=("To make a solution of known molarity you weigh moles × molar mass of the solid, dissolve it and make up to volume. "
            "This solution preparation calculator gives the mass of solid needed for any concentration and volume, corrected for reagent purity.\n\n"
            "Lab technicians, chemistry students and quality control analysts use it to prepare reagents, buffers and standards "
            "quickly and to record how the weighed mass was worked out."),
     body_add=f'''
## Recalculating from the mass you actually weighed

You will rarely hit the target mass exactly. Weigh close to it, record the real figure and work out the true concentration. For the default recipe the target is {m:.4f} g. If the balance shows **{mw:.4f} g**:

- Actual moles = {mw:.4f} × {pur:g} ÷ {M:g} = {mw*pur/M:.6f} mol
- Actual concentration = {mw*pur/M:.6f} ÷ {Vml/1000:g} L = **{cact:.5f} mol/L**, which is {dev:+.2f}% from 0.1 M

Label the bottle with this value rather than the nominal 0.1 M. It is usually quicker and more accurate than adding or removing a few milligrams of solid.

## How balance resolution limits accuracy

Rounding on the balance display adds an error of half the last digit. For the {m:.3f} g weighing above:

| Balance readability | Rounding error | Error in concentration |
|---|---|---|
{bal_rows}
For standard solutions aim for an error below 0.1%, which here needs at least a 1 mg balance. Weighing a larger amount into a larger flask also reduces the relative error.
''',
     faq_add=[('What do I do if I weigh slightly more or less than the calculated mass?',
               f'Keep the mass you weighed and recalculate the concentration from it: c = mass × purity ÷ (molar mass × volume in L). For {mw:.4f} g of 99.5% NaCl in 500 mL that is {cact:.5f} mol/L.')])

# ---------------------------------------------------------------- Absolute / gauge pressure
pg, z = 2.0, 0.0
pa = 101325 * (1 - 2.25577e-5 * z) ** 5.25588 / 1e5
pabs = pg + pa
vac_rows = ''
for g in (-0.2, -0.5, -0.8, -0.9, -0.95, -0.99):
    a = pa + g  # bar abs
    vac_rows += f"| {g:g} bar(g) | {a*1000:,.0f} mbar(a) | {a*1e5/133.322:,.1f} torr | {-g*1e5/3386.39:.2f} inHg vacuum | {-g/pa*100:.1f}% |\n"

edit('engineering/absolute-gauge-pressure', date=U, phrase='absolute to gauge pressure calculator',
     intro=("Gauge pressure is measured relative to the surrounding air, absolute pressure relative to a perfect vacuum, and the difference is local atmospheric pressure. "
            "This absolute to gauge pressure calculator converts between them, with vacuum as negative gauge pressure, as explained in [absolute vs gauge pressure](https://www.instrumentationblog.in/absolute-vs-gauge-pressure/).\n\n"
            "Instrument engineers, process operators and HVAC technicians use it when a transmitter, datasheet or gas calculation "
            "uses a different reference from the gauge on the pipe."),
     body_add=f'''
## Vacuum readings in other units

Vacuum equipment is specified in several ways. At sea level ({pa*1000:,.2f} mbar atmosphere) the same gauge readings convert as follows:

| Gauge reading | Absolute | Absolute in torr | Vacuum in inHg | Vacuum as % of atmosphere |
|---|---|---|---|---|
{vac_rows}
A rough vacuum pump that pulls 50 mbar(a) is already at about 95% vacuum, while the last few percent down to 1 mbar(a) take a much better pump and tight seals. This is why vacuum below about 100 mbar is always specified in absolute units.

## Checking a gauge against a barometer

To check that a gauge transmitter and an absolute transmitter agree, read a local barometer and add its value to the gauge reading. With the default {pg:g} bar(g) and a barometer showing 1,005 mbar, the absolute transmitter should read {pg+1.005:.3f} bar(a), not the {pabs:.5f} bar(a) the standard atmosphere predicts. The {(pabs-pg-1.005)*1000:.1f} mbar difference is weather, not a calibration fault.
''',
     before='## Common mistakes',
     replace=[('Always check which one a datasheet means.\n', 'Always check which one a datasheet means.\n- **Calibrating a vacuum gauge against an absolute reference without a barometer.** Weather alone can shift the expected gauge reading by 20 to 30 mbar.\n')],
     faq_add=[('How do I convert inches of mercury vacuum to absolute pressure?',
               'Multiply the vacuum reading by 33.864 to get mbar, then subtract it from atmospheric pressure. At sea level, 25 inHg vacuum is 25 × 33.864 = 846.6 mbar below 1,013.25 mbar, so the absolute pressure is about 166.7 mbar(a).')])

# ---------------------------------------------------------------- Water hardness
Ca, Mg = 60.0, 15.0
Hc = 2.49730 * Ca
Hm = 4.11796 * Mg
Ht = Hc + Hm
# EDTA titration example: 50 mL sample, 0.01 M EDTA
Vs, cE = 50.0, 0.01
VE = Ht / 100.0869 / 1000 * Vs / cE * 1000  # mL; mmol hardness = Ht/100.0869 mmol/L
# alkalinity example
alk = 150.0
carb = min(alk, Ht)
noncarb = Ht - carb
# softener sizing: 4 person household 150 L/person/day
use = 4 * 150
gpg = Ht / 17.118
grains_day = gpg * use / 3.78541
cap = 32000
days = cap / grains_day
tit_rows = ''
for hh in (50, 100, 150, 200, 300, 400):
    tit_rows += f"| {hh} mg/L | {hh/100.0869:.3f} mmol/L | {hh/100.0869*Vs/cE/1000*1000/1000:.2f} mL |\n"

edit('chemistry/water-hardness', date=U, phrase='water hardness calculator',
     intro=("Water hardness comes mainly from dissolved calcium and magnesium and is reported as the equivalent amount of calcium carbonate. "
            "This water hardness calculator converts Ca and Mg results into mg/L (ppm) as CaCO₃, °dH, °fH and grains per gallon, and rates the water.\n\n"
            "Water treatment operators, boiler engineers and homeowners comparing a lab report use it to decide whether a softener, "
            "scale inhibitor or reverse osmosis unit is needed."),
     body_add=f'''
## Measuring hardness by EDTA titration

Most labs measure total hardness by titrating the sample with EDTA at pH 10 using Eriochrome Black T, which turns from wine red to blue when all the Ca and Mg have been complexed. One mole of EDTA binds one mole of Ca or Mg, so:

<p class="formula">Hardness (mg/L CaCO₃) = V<sub>EDTA</sub> (mL) × M<sub>EDTA</sub> × 100,087 ÷ V<sub>sample</sub> (mL)</p>

For the default water ({Ht:.1f} mg/L) and a {Vs:g} mL sample titrated with {cE} M EDTA, the endpoint should come at about **{VE:.2f} mL**. Doing the titration again at pH 12 to 13 with murexide or calcon indicator gives calcium alone; magnesium is the difference.

| Total hardness | mmol/L | Expected 0.01 M EDTA for 50 mL sample |
|---|---|---|
{tit_rows}
## Carbonate and non-carbonate hardness

The alkalinity result on the same report splits hardness into two parts. With an alkalinity of {alk:g} mg/L as CaCO₃ and total hardness of {Ht:.1f} mg/L:

- Carbonate (temporary) hardness = the smaller of the two = **{carb:.1f} mg/L**
- Non-carbonate (permanent) hardness = {Ht:.1f} − {carb:.1f} = **{noncarb:.1f} mg/L**

The carbonate part forms scale in kettles, heaters and cooling towers. Lime softening removes it, but the non-carbonate part needs soda ash, ion exchange or membranes.

## Sizing a water softener

A softener is rated by how many grains of hardness it removes between regenerations. At {Ht:.1f} mg/L the water carries {gpg:.2f} grains per US gallon. A household using {use} L a day treats {use/3.78541:.0f} gallons, which is **{grains_day:,.0f} grains per day**. A {cap:,} grain softener would therefore regenerate about every **{days:.1f} days**. Iron in the water adds to the load, so add about 4 gpg of extra hardness for each mg/L of iron.

## Common mistakes

- **Adding Ca and Mg directly.** 60 mg/L Ca plus 15 mg/L Mg is not 75 mg/L hardness. Each must be converted to CaCO₃ with its own factor first.
- **Mixing up Ca as the ion and Ca as CaCO₃.** Some reports give "calcium hardness as CaCO₃"; multiplying that by 2.497 again counts it twice.
- **Reading ppm on a TDS meter as hardness.** TDS includes sodium, chloride and sulfate, so it is always higher than hardness and cannot replace a titration.
- **Confusing UK and US grains.** A Clark degree (UK) is 14.25 mg/L CaCO₃, while a US grain per gallon is 17.12 mg/L.
- **Ignoring magnesium.** Gram for gram, magnesium adds 65% more hardness than calcium, so a calcium-only test underestimates scaling.
''',
     faq_add=[('How do I measure water hardness at home?',
               'Test strips give a rough band in a minute. A drop count titration kit is more accurate: each drop usually equals 1 gpg or 1 °dH, so counting the drops to the colour change gives the hardness directly. For a softener design, use a lab report with Ca and Mg.'),
              ('How often will my water softener regenerate?',
               f'Divide the softener capacity in grains by the daily load: hardness in gpg × gallons used per day. At {Ht:.1f} mg/L ({gpg:.2f} gpg) and {use} L a day, a {cap:,} grain unit regenerates about every {days:.1f} days.')])

# ---------------------------------------------------------------- Generator frequency
p, N = 4, 1500
f = p * N / 120
# droop: 4% droop governor, 50 Hz rated, no load speed
droop = 0.04
fnl = f * (1 + droop)
dr_rows = ''
for L in (0, 0.25, 0.5, 0.75, 1.0):
    ff = fnl - droop * f * L
    dr_rows += f"| {L*100:.0f}% | {ff:.2f} Hz | {ff*120/p:,.0f} rpm |\n"
# hydro: turbine 214.3 rpm -> poles
Nt = 214.3
Pexact = 120 * 50 / Nt
Pc = 28
Ns = 120 * 50 / Pc
# tachometer error
Nm = 1488
fm = p * Nm / 120

edit('electrical/generator-frequency', date=U, phrase='generator frequency calculator',
     intro=("A synchronous generator's output frequency is set by how fast its rotor turns and how many magnetic poles it has. "
            "This generator frequency calculator applies f = P × N ÷ 120 to find the frequency, or the speed for 50 Hz or 60 Hz; see [how an alternator works](https://www.instrumentationblog.in/alternator-working-principle-explained/).\n\n"
            "Genset technicians, power plant engineers and students use it to set governor speed, match a prime mover "
            "to an alternator and check readings before synchronising."),
     body_add=f'''
## Frequency under governor droop

The default {p} pole set at {N:,} rpm gives {p} × {N:,} ÷ 120 = **{f:g} Hz**. Most gensets that share load use a droop governor, so speed and frequency fall slightly as load rises. With {droop*100:g}% droop set to give {f:g} Hz at full load, the no load frequency is {f:g} × (1 + {droop:g}) = {fnl:g} Hz:

| Load | Frequency | Rotor speed |
|---|---|---|
{dr_rows}
An isochronous governor holds {f:g} Hz at every load, which suits a single set running alone but makes load sharing between parallel sets unstable without a load sharing controller.

## Choosing the pole count for a hydro turbine

A water turbine has a best efficiency speed set by head and flow, and the generator must use a whole number of pole pairs. If the turbine runs best at about {Nt:g} rpm, the ideal pole count is 120 × 50 ÷ {Nt:g} = {Pexact:.2f}. Choosing **{Pc} poles** gives a synchronous speed of 120 × 50 ÷ {Pc} = **{Ns:.1f} rpm**, the nearest standard speed, and the runner is then designed for that speed.

## Measuring frequency and speed on site

Frequency is read from the generator control panel, a clamp meter with a Hz range or a portable power analyser. Speed is checked with an optical tachometer on a reflective mark on the shaft or from the magnetic pickup on the flywheel teeth. If a tachometer reads **{Nm:,} rpm** on the {p} pole set, the expected frequency is {p} × {Nm:,} ÷ 120 = **{fm:.1f} Hz**; a panel reading of exactly {f:g} Hz would then point to a tachometer or meter error.

## Common mistakes

- **Using pole pairs instead of poles.** f = P N ÷ 120 uses the total number of poles. With pole pairs the formula is f = p N ÷ 60.
- **Counting the engine's cylinders or the alternator's terminal leads.** Neither tells you the pole count; use the nameplate rated speed and frequency.
- **Expecting a 60 Hz alternator to work at 50 Hz with the same voltage.** At 5/6 of rated speed the voltage, cooling fan airflow and output kVA all drop, so the set must be derated.
- **Confusing generator speed with induction motor speed.** A 4 pole motor runs at about 1,440 to 1,480 rpm because of slip, but a 4 pole synchronous generator must turn at exactly 1,500 rpm for 50 Hz.
''',
     faq_add=[('Why does generator frequency drop when load is added?',
               f'Extra load slows the engine until the governor adds fuel. A droop governor lets it settle at a lower speed on purpose: with 4% droop a set adjusted to {f:g} Hz at full load runs at {fnl:g} Hz with no load.')])

print('done')

# ======================================================================= SECTION _expand_c6.py
"""Part C expand (2026-11-17), slice 6: health/bmi and chemistry/dilution (both featured; the flag is lifted
around the edit and restored unchanged). Worked examples use each page's default inputs; all numbers computed here."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-17'


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


# ---------------------------------------------------------------- BMI (defaults m = 70 kg, h = 172 cm)
m, h = 70.0, 1.72
h2 = h * h
bmi = m / h2
prime = bmi / 25
w185, w229, w249 = 18.5 * h2, 22.9 * h2, 24.9 * h2
to229 = m - w229
# effect of measurement error at the default
b_h1 = m / (h - 0.01) ** 2
b_w1 = (m + 1.5) / h2
rows = ''
for bm in (18.5, 20, 22, 22.9, 24.9, 27.5, 30):
    rows += f"| {bm:g} | {bm*h2:.1f} kg | {bm*h2-m:+.1f} kg |\n"

n_bmi = edit_keep_featured('health/bmi', date=U, phrase='BMI calculator',
    intro=("Body Mass Index divides weight in kilograms by the square of height in metres to give one number for comparing weight with height. "
           "This BMI calculator works in kg, lb, cm or inches and can also give the weight for a target BMI.\n\n"
           "Adults use it to check whether their weight sits in the healthy range, and doctors, dietitians and fitness coaches use it "
           "as a first screening step before measuring waist size, body fat or blood tests."),
    body_add=f'''
## Worked example at the default values

The calculator opens with 70 kg and 172 cm:

- Height in metres squared: 1.72 × 1.72 = **{h2:.4f} m²**
- BMI = 70 ÷ {h2:.4f} = **{bmi:.1f} kg/m²**
- BMI Prime = {bmi:.2f} ÷ 25 = **{prime:.2f}**

Under the WHO table this is normal weight (18.5 to 24.9). Under the Asian cut-offs it falls in the 23 to 24.9 overweight band. At 172 cm the WHO healthy range is **{w185:.1f} kg to {w249:.1f} kg**, and reaching the top of the Asian normal range (22.9) would mean a weight of {w229:.1f} kg, about {to229:.1f} kg less.

## Target weights at 172 cm

| Target BMI | Weight at 1.72 m | Change from 70 kg |
|---|---|---|
{rows}
## Measuring weight and height properly

A BMI is only as good as the two numbers behind it. Measure height barefoot, standing straight against a wall with heels together, and mark the top of the head with a flat object held level. Weigh in light clothing on a flat, hard floor, ideally in the morning after using the toilet and before eating.

The sensitivity is larger than most people expect. At the default values, a height entered 1 cm too short gives a BMI of {b_h1:.1f} instead of {bmi:.1f}, and weighing 1.5 kg heavier after a meal and clothes gives {b_w1:.1f}. Near a category boundary either error can flip the result, so use measured rather than remembered figures.

## What BMI is used for in practice

Clinics record BMI at routine visits because it is quick and needs only a scale and a stadiometer. It is used to flag people who may need a check for blood pressure, blood sugar and cholesterol, to set eligibility for some treatments such as bariatric surgery, and to adjust doses or anaesthesia plans. Public health surveys use it to track population trends. For an individual, a change in BMI over months is often more informative than a single reading.
''',
    faq_add=[('What is a good BMI for my height?',
              f'Any weight that gives a BMI from 18.5 to 24.9 is in the WHO healthy range, or 18.5 to 22.9 under Asian cut-offs. At 172 cm that is {w185:.1f} kg to {w249:.1f} kg (WHO) or {w185:.1f} kg to {w229:.1f} kg (Asian).'),
             ('Is BMI valid for older adults?',
              'BMI uses the same formula, but older adults often lose muscle and height, so the same BMI can hide more body fat. Large studies of people over 65 find that mortality risk rises below a BMI of about 23 and is lowest at around 25 to 28, so results should be read with a doctor.')])

# ---------------------------------------------------------------- Dilution (defaults C1 = 10, C2 = 0.5, V2 = 200 mL)
C1, C2, V2 = 10.0, 0.5, 200.0
V1 = C2 * V2 / C1
Vd = V2 - V1
DF = C1 / C2
# concentrated HCl to 1 M
w, rho, M = 0.37, 1.19, 36.46
cHCl = w * rho * 1000 / M
vHCl = 1.0 * 1000 / cHCl
stock_rows = ''
for name, wf, d, mm in (('Hydrochloric acid 37%', 0.37, 1.19, 36.46), ('Sulfuric acid 98%', 0.98, 1.84, 98.08),
                        ('Nitric acid 70%', 0.70, 1.42, 63.01), ('Acetic acid (glacial) 99.8%', 0.998, 1.05, 60.05),
                        ('Ammonia solution 28%', 0.28, 0.90, 17.03), ('Phosphoric acid 85%', 0.85, 1.685, 98.00)):
    c = wf * d * 1000 / mm
    stock_rows += f"| {name} | {d:g} g/mL | {c:.1f} M | {1000/c:.1f} mL |\n"
# serial dilution of the 10 M stock, four 1:10 steps
ser = ''
c = C1
for step in range(1, 5):
    c = c / 10
    ser += f"| {step} | 1 mL into 9 mL | {c:g} M |\n"

n_dil = edit_keep_featured('chemistry/dilution', date=U, phrase='dilution calculator',
    intro=("Diluting a solution lowers its concentration while the amount of solute stays the same, so C₁V₁ = C₂V₂. "
           "This dilution calculator gives the volume of stock and of solvent needed for a target concentration and volume, or the final concentration of a mix.\n\n"
           "Lab technicians, students, pharmacists and water treatment operators use it to prepare working standards, reagents "
           "and cleaning solutions from concentrated stock without wasting chemicals."),
    body_add=f'''
## Checking the default example step by step

With the default inputs (C₁ = 10, C₂ = 0.5, V₂ = 200 mL) the calculator returns V₁ = {V1:g} mL and {Vd:g} mL of solvent. The dilution factor is {C1:g} ÷ {C2:g} = **{DF:g}**, so the stock volume is always the final volume divided by {DF:g}: 200 ÷ {DF:g} = {V1:g} mL. In practice, pipette the {V1:g} mL of stock into a 200 mL volumetric flask that already holds some water, then fill to the mark rather than measuring {Vd:g} mL separately.

## Diluting concentrated acids and bases

Bottles of concentrated reagent are labelled in % by mass, not mol/L, so first convert the label to molarity:

<p class="formula">C (mol/L) = w × ρ (g/mL) × 1000 ÷ M</p>

For 37% hydrochloric acid with a density of {rho} g/mL and M = {M} g/mol: C = {w} × {rho} × 1000 ÷ {M} = **{cHCl:.2f} M**. To make 1 L of 1 M HCl, V₁ = 1 × 1000 ÷ {cHCl:.2f} = **{vHCl:.1f} mL** of the concentrated acid, added slowly to about 800 mL of water and then made up to 1 L.

| Concentrated reagent | Density | Molarity | Volume for 1 L of 1 M |
|---|---|---|---|
{stock_rows}
Label densities vary slightly between suppliers, so use the figure on your bottle or certificate of analysis.

## Serial dilution from the 10 M stock

Four 1:10 steps take the default 10 M stock down by 10,000 times with ordinary pipettes:

| Step | Transfer | Concentration |
|---|---|---|
{ser}
Mix each tube fully before taking the next aliquot, and use a fresh tip each time so stock carried on the outside of the tip does not raise the next concentration.
''',
    faq_add=[('How do I dilute concentrated hydrochloric acid to 1 M?',
              f'37% HCl is about {cHCl:.1f} M. Add {vHCl:.1f} mL of it slowly to about 800 mL of water, stir, let it cool, then make up to 1 L. Always add acid to water.'),
             ('How do I find the concentration after a serial dilution?',
              'Multiply the dilution factors of each step and divide the stock concentration by the total. Four 1:10 steps give a factor of 10,000, so 10 M becomes 0.001 M.')])

print('bmi body words', n_bmi, 'dilution body words', n_dil)

# ======================================================================= SECTION _expand_c7.py
"""Part C expand (2026-11-17), slice 7: busbar-size, skin-depth. Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-17'
pi = math.pi
mu0 = 1.25663706212e-6

# ---------------------------------------------------------------- Busbar size
I, rc, ra, J, t, nb = 1600.0, 1.724e-8, 2.826e-8, 1.6, 10.0, 1
A = I / J
w = A / (nb * t)
Pm = I ** 2 * rc / (A * 1e-6)
a_cu = 0.00393
f90 = 1 + a_cu * 70
P90 = Pm * f90
Ja = 0.8
Aa = I / Ja
Pa = I ** 2 * ra / (Aa * 1e-6)
Isc, tsc, k = 50000.0, 1.0, 143
Asc = Isc * math.sqrt(tsc) / k
rows = ''
for j in (1.0, 1.2, 1.4, 1.6, 2.0):
    a = I / j
    p = I ** 2 * rc / (a * 1e-6)
    rows += f"| {j:.1f} A/mm² | {a:,.0f} mm² | {p:.1f} W/m | {3*p:.1f} W/m | {a*8.96e-3:.2f} kg/m |\n"

edit('electrical/busbar-size', date=U, phrase='busbar size calculator',
     intro=("A first estimate of busbar size divides the current by a safe current density, typically 1.2 to 1.6 A/mm² for copper and 0.8 to 1.0 A/mm² for aluminium in switchboards. "
            "This busbar size calculator gives the cross-section, bar width and resistive loss per metre.\n\n"
            "Panel builders and electrical designers use it to pick a starting bar size before checking it against the "
            "[busbar sizing calculation guide](https://www.instrumentationblog.in/busbar-sizing-calculation-guide/) for temperature rise and short circuit."),
     body_add=f'''
## Worked example: copper against aluminium for the default 1,600 A board

With the default inputs (1,600 A, copper, {J:g} A/mm², {t:g} mm bars, one bar per phase) the calculator gives A = 1,600 ÷ {J:g} = **{A:,.0f} mm²**, a width of **{w:.0f} mm** and **{Pm:.1f} W/m** per phase at 20 °C.

The bars do not run at 20 °C. Copper resistance rises by about 0.393% per kelvin, so at a 90 °C working temperature the loss is {Pm:.1f} × (1 + 0.00393 × 70) = **{P90:.1f} W/m** per phase, or {3*P90:.0f} W for every metre of a three phase run. That heat has to leave the enclosure, which is why ventilation matters.

Switching to aluminium at 0.8 A/mm² needs 1,600 ÷ 0.8 = **{Aa:,.0f} mm²**, for example two 100 × 10 mm bars per phase. Because the section doubles while resistivity rises only by {ra/rc:.2f} times, the loss falls to **{Pa:.1f} W/m** per phase at 20 °C.

## Short circuit check

The thermal withstand of a bare copper bar is roughly A ≥ I<sub>sc</sub> × √t ÷ k with k ≈ {k}. For a 50 kA fault cleared in 1 s, A ≥ 50,000 × √1 ÷ {k} = **{Asc:.0f} mm²**, so the {A:,.0f} mm² bar passes the thermal test easily. The mechanical force between phases is usually the harder limit: it rises with the square of the peak fault current and falls with phase spacing, so support spacing must be checked against the maker's tested arrangement.

## Current density, loss and copper weight at 1,600 A

| Current density | Cross-section | Loss per phase (20 °C) | Three phase loss | Copper per phase |
|---|---|---|---|---|
{rows}
Lower densities cost more copper but cut the running loss; over a 20 year life the energy saved often pays for the extra metal in heavily loaded boards.

## Common mistakes

- **Using one thick bar for high AC current.** Beyond about 10 mm the centre of a copper bar carries little current at 50 Hz; two 10 mm bars with a 10 mm gap beat one 20 mm bar.
- **Applying small-bar densities to large bars.** A 20 × 5 mm bar can run near 2 A/mm², but a 200 × 10 mm bar has far less surface per mm² and must run lower.
- **Ignoring the neutral.** Harmonic loads (drives, LED lighting, IT equipment) can push neutral current above phase current, so a half size neutral may overheat.
- **Sizing on 20 °C loss only.** Real bars run 30 to 50 K above a 35 to 40 °C panel ambient, which adds roughly a quarter to the loss.
- **Mixing copper and aluminium joints without treatment.** Bare Cu to Al joints corrode; use bimetallic washers or tin plated bars and torque the bolts to the specified value.
''',
     faq_add=[('How much heat does a busbar produce?',
               f'Loss per metre per phase is I² ρ ÷ A. A 1,600 A copper bar of 1,000 mm² loses {Pm:.1f} W/m at 20 °C and about {P90:.0f} W/m at 90 °C, so a three phase run produces about {3*P90:.0f} W per metre at full load.'),
              ('Can I use the same busbar size for 60 Hz?',
               'Almost. The skin depth of copper falls from about 9.2 mm at 50 Hz to 8.4 mm at 60 Hz, so thick bars have slightly higher AC resistance. For bars up to 10 mm thick the difference is small; for thicker or multiple bars use the maker\'s 60 Hz ratings.')])

# ---------------------------------------------------------------- Skin depth
def delta(rho, f, mur=1.0):
    return math.sqrt(rho / (pi * f * mu0 * mur))

rho_cu, f0 = 1.678e-8, 50.0
d50 = delta(rho_cu, f0)
c1 = pi * f0 * mu0
rho90 = rho_cu * (1 + 0.00393 * 70)
d90 = delta(rho90, f0)
# 1.0 mm wire at 100 kHz
dw, fw = 1.0e-3, 100e3
dsw = delta(rho_cu, fw)
r = dw / 2
Aeff = pi * (r ** 2 - (r - dsw) ** 2)
Afull = pi * r ** 2
ratio = Afull / Aeff
frac_rows = ''
for x in (0.5, 1, 2, 3, 5):
    frac_rows += f"| {x:g} δ | {math.exp(-x)*100:.1f}% | {(1-math.exp(-x))*100:.1f}% |\n"
mu_rows = ''
for m in (1, 10, 100, 500, 1000):
    mu_rows += f"| {m:,} | {1/math.sqrt(m):.3f} | {delta(1.0e-7, 50, m)*1e3:.2f} mm |\n"

edit('electrical/skin-depth', date=U, phrase='skin depth calculator',
     intro=("Alternating current crowds towards the surface of a conductor, so at high frequency only a thin outer layer carries it and AC resistance rises. "
            "This skin depth calculator finds the depth of that layer for copper, aluminium and other metals at any frequency.\n\n"
            "Power engineers use it to size busbars and large cables, and electronics designers use it for transformer windings and RF traces; "
            "see [skin effect in conductors](https://www.instrumentationblog.in/skin-effect-in-conductors/) for the physics."),
     replace=[('about 86% of the current flows within the outer δ of a thick conductor.',
               'about 63% of the current flows within the outer δ of a thick conductor and about 86% within 2δ.')],
     body_add=f'''
## Worked example: copper at the default 50 Hz, cold and hot

With the defaults (copper, μr = 1, 50 Hz), π × f × μ₀ = π × 50 × 1.25663706 × 10⁻⁶ = {c1:.4e} and δ = √(1.678 × 10⁻⁸ ÷ {c1:.4e}) = **{d50*1e3:.2f} mm**.

At a 90 °C conductor temperature copper resistivity rises to 1.678 × 10⁻⁸ × (1 + 0.00393 × 70) = {rho90:.3e} Ω·m, so the skin depth grows to **{d90*1e3:.2f} mm**. A hot bar is slightly less affected by skin effect, but its DC resistance is {rho90/rho_cu:.2f} times higher, so the total loss still rises.

## AC resistance of a winding wire at 100 kHz

A 1.0 mm copper wire in a switch-mode transformer at 100 kHz has δ = **{dsw*1e3:.3f} mm**. If the current flows mainly in an outer ring one skin depth thick, the useful area is π × (0.5² − {r*1e3-dsw*1e3:.3f}²) = **{Aeff*1e6:.3f} mm²** against {Afull*1e6:.3f} mm² for the full wire, so R<sub>AC</sub> ÷ R<sub>DC</sub> is roughly **{ratio:.2f}**. This ring model is only an estimate when the radius is close to δ; Dowell's method gives a better answer for multilayer windings, where the proximity effect usually adds more loss than the skin effect. A Litz bundle of strands well below 2δ (about {2*dsw*1e3:.2f} mm here), such as 0.1 mm strands, keeps the ratio close to 1.

## How current falls with depth

For a thick flat conductor the current density at depth x is J₀ e<sup>−x/δ</sup>:

| Depth | Current density left | Share of current carried above this depth |
|---|---|---|
{frac_rows}
## Effect of magnetic permeability

Skin depth falls with the square root of μr. For a steel with ρ = 1.0 × 10⁻⁷ Ω·m at 50 Hz:

| μr | Factor 1/√μr | Skin depth |
|---|---|---|
{mu_rows}
This is why steel conduit, steel wire armour and steel enclosures heat up when single core cables pass through them separately, and why induction heating works so well on carbon steel.

## Common mistakes

- **Saying all the current flows within δ.** Only about 63% flows in the first skin depth; a conductor needs a thickness of about 3δ to carry 95% as if it were infinitely thick.
- **Treating proximity effect as skin effect.** In coils and closely spaced bars, the field of nearby conductors pushes current to one side and often causes more loss than skin effect alone.
- **Setting μr = 1 for carbon steel.** Mild steel has μr of 100 or more, which shrinks δ to around a millimetre at 50 Hz.
- **Using Litz wire at several MHz.** Strand capacitance and imperfect twisting cancel the benefit above about 1 to 2 MHz; use foil, tubing or plated conductors there.
- **Plating thinner than the skin depth.** A silver or gold layer only lowers RF loss if it is at least 2 to 3δ thick at the working frequency.
''',
     faq_add=[('What percentage of current flows within one skin depth?',
               'About 63% (1 − 1/e) in a thick flat conductor, about 86% within 2δ and 95% within 3δ. The current density at depth δ is 37% of its surface value.'),
              ('How thick should a conductor be to avoid skin effect losses?',
               f'A thickness of about 2δ to 3δ uses the material well. For copper at 50 Hz (δ = {d50*1e3:.2f} mm) that is about 18 to 28 mm for a bar cooled from both sides; thicker sections add little and are better split into several bars.')])
print('done')

# Backlog and priority list lines for the 32 expanded pages and the 4 improved pages were removed after the run.
