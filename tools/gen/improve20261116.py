"""Improve pass (2026-11-16) for three thin pages from the first batch (2026-10-28):
electronics/zener-resistor, electrical/transformer-size, electronics/capacitors-series-parallel.
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples built from the calculator defaults, reference tables computed here,
practical notes, common mistakes and new FAQs. Formulas and FAQ facts were re-checked; the Zener
example quoted the resistor and Zener power for the rounded 270 ohm resistor without saying so, and
is rewritten to show both the calculated and the standard value. Existing instrumentationblog.in
links are kept; none are added. Slugs, categories, variables, equations and related ids are
unchanged (asserted by inplace.edit). Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, DONE
U = '2026-11-16'
IB = 'https://www.instrumentationblog.in'
E24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]


def e24_below(x):
    best = 0
    for dec in range(-1, 7):
        for m in E24:
            v = m * 10 ** dec
            if v <= x * (1 + 1e-9):
                best = max(best, v)
    return best


# ======================================================================= Zener resistor
Vin, Vz, IL, Iz = 12.0, 5.1, 0.020, 0.005
R = (Vin - Vz) / (IL + Iz)
PR = (Vin - Vz) ** 2 / R
Pz = Vz * (Vin - Vz) / R
Rs = e24_below(R)
PRs = (Vin - Vz) ** 2 / Rs
Pzs = Vz * (Vin - Vz) / Rs
Vmax = 14.0
Pz_hi = Vz * (Vmax - Vz) / Rs
PR_hi = (Vmax - Vz) ** 2 / Rs
Iz_actual = (Vin - Vz) / Rs - IL
z_rows = ''
for vz in (3.3, 3.9, 4.7, 5.1, 5.6, 6.2, 6.8, 8.2, 9.1, 10.0):
    r = (Vin - vz) / (IL + Iz)
    rs = e24_below(r)
    z_rows += f"| {vz:g} V | {r:.0f} Ω | {rs:g} Ω | {(Vin-vz)**2/rs*1000:.0f} mW | {vz*(Vin-vz)/rs*1000:.0f} mW |\n"

edit('electronics/zener-resistor', date=U,
     title='Zener Diode Resistor Calculator (Series Resistor and Power)',
     description='Calculate the series resistor for a Zener diode voltage regulator, plus resistor and Zener power, from input voltage, Zener voltage and load current.',
     phrase='zener diode resistor calculator',
     intro=('A Zener diode with a series resistor is the simplest voltage regulator: the Zener holds a fixed voltage while the resistor drops the rest and limits current. '
            'This Zener diode resistor calculator sizes that resistor and checks the power in both parts.'
            '\n\n'
            'Electronics hobbyists, students and circuit designers use it for references, clamps and small supplies. '
            f'For the device itself, see [what a Zener diode is]({IB}/what-is-a-zener-diode/).'),
     replace=[(
         '## Example\n\n12 V in, 5.1 V Zener, 20 mA load, 5 mA minimum Zener current:\n\n- R = 6.9 ÷ 0.025 = **276 Ω** → use 270 Ω\n- Resistor power ≈ **176 mW** → 0.5 W resistor\n- Zener power with no load ≈ **130 mW** → 0.5 W Zener\n',
         f'''## Worked example

A {Vz:g} V Zener must supply a load of up to {IL*1000:g} mA from a supply that never falls below {Vin:g} V, keeping at least {Iz*1000:g} mA in the Zener:

- Voltage across the resistor = {Vin:g} − {Vz:g} = **{Vin-Vz:.1f} V**
- R = {Vin-Vz:.1f} ÷ ({IL*1000:g} + {Iz*1000:g}) mA = {Vin-Vz:.1f} ÷ {IL+Iz:g} A = **{R:.0f} Ω**
- Resistor power = {Vin-Vz:.1f}² ÷ {R:.0f} = **{PR*1000:.1f} mW**
- Zener power with the load removed = {Vz:g} × {Vin-Vz:.1f} ÷ {R:.0f} = **{Pz*1000:.1f} mW**

Choose the next lower E24 value, **{Rs:g} Ω**, so the Zener current only rises: it becomes {(Vin-Vz)/Rs*1000:.1f} mA in total, leaving {Iz_actual*1000:.1f} mA in the Zener at full load. With {Rs:g} Ω the resistor dissipates {PRs*1000:.0f} mW and the unloaded Zener {Pzs*1000:.0f} mW, so 0.5 W parts give a safe 2 to 3 times margin.
''')],
     body_add=f'''
## Resistor values for a {Vin:g} V supply

Load {IL*1000:g} mA and minimum Zener current {Iz*1000:g} mA, with the standard value rounded down to E24 and the powers computed for that standard value:

| Zener voltage | Calculated R | E24 resistor | Resistor power | Zener power, no load |
|---|---|---|---|---|
{z_rows}
## Design for the highest input voltage too

The resistor is sized at the lowest input voltage, but the Zener dissipates the most at the highest input with no load. If the {Vin:g} V supply in the example can rise to {Vmax:g} V, the {Rs:g} Ω resistor passes {(Vmax-Vz)/Rs*1000:.1f} mA, the unloaded Zener dissipates **{Pz_hi*1000:.0f} mW** and the resistor **{PR_hi*1000:.0f} mW**. Always check the power at the maximum input, and derate the Zener above 25 °C ambient as its datasheet shows (often about 4 mW per °C for a 0.5 W glass part).

## Practical notes

- **Regulation is modest.** The Zener's dynamic resistance (typically 5 to 30 Ω for small parts) means the output moves by tens of millivolts as the load current changes. Add an emitter follower transistor or use a regulator IC for tighter control.
- **Choose the Zener test current.** The datasheet voltage is quoted at a test current, often 5 mA for 0.5 W parts. Running far below it gives a lower, softer voltage.
- **Add a capacitor.** A 100 nF to 10 µF capacitor across the Zener reduces its noise, which is significant in avalanche diodes above about 6 V.

## Common mistakes

- **Sizing at the nominal input voltage.** If the supply sags below the design value, the Zener current falls to zero and the output drops out of regulation.
- **Rounding the resistor up.** A higher standard value reduces the current and can starve the Zener at full load; round down instead.
- **Forgetting the no-load case.** When the load is disconnected all the current flows into the Zener, which is when it overheats.
- **Using a Zener for large currents.** Above roughly 50 mA the wasted power grows quickly; a linear regulator or a switching converter is more efficient.
- **Ignoring tolerance.** A 5.1 V Zener with 5% tolerance can be anywhere from about 4.85 to 5.36 V, which matters when it is used as a reference.
''',
     faq_add=[('What wattage Zener diode do I need?',
               f'At least twice the no-load Zener power at the highest input voltage. In the example, {Pzs*1000:.0f} mW at {Vin:g} V rises to {Pz_hi*1000:.0f} mW at {Vmax:g} V, so a 0.5 W Zener is suitable and a 0.25 W part is not.'),
              ('Can I connect two Zener diodes in series?',
               'Yes, two Zeners in series give the sum of their voltages and share the power, for example 5.1 V plus 6.8 V for 11.9 V. Do not connect Zeners in parallel to share current, because the one with the lower voltage takes nearly all of it.')])

# ======================================================================= Transformer size
P0, df0, pf0, g0 = 500.0, 0.7, 0.9, 0.25
Pd0 = P0 * df0
S0 = Pd0 / pf0 * (1 + g0)
STD = [16, 25, 63, 100, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500]
nxt = lambda s: next(x for x in STD if x >= s - 1e-9)
V = 415.0
Ifl = lambda kva: kva * 1000 / (math.sqrt(3) * V)
load_now = Pd0 / pf0 / nxt(S0) * 100
t_rows = ''
for kw in (100, 200, 300, 500, 750, 1000, 1500, 2000):
    s = kw * df0 / pf0 * (1 + g0)
    n = nxt(s)
    t_rows += f"| {kw:,} kW | {kw*df0:,.0f} kW | {s:,.0f} kVA | {n:,} kVA | {Ifl(n):,.0f} A |\n"
pf_rows = ''
for pf in (0.7, 0.8, 0.85, 0.9, 0.95, 1.0):
    s = Pd0 / pf * (1 + g0)
    pf_rows += f"| {pf:.2f} | {s:,.0f} kVA | {nxt(s):,} kVA |\n"

edit('electrical/transformer-size', date=U,
     title='Transformer Size Calculator (kVA from Connected Load)',
     description='Calculate the transformer kVA rating for a connected load from kW, demand factor, power factor and growth margin, then pick the next standard size.',
     phrase='transformer size calculator',
     intro=('Choosing a transformer means turning the connected load into a kVA figure, allowing for demand factor, power factor and future growth. '
            'This transformer size calculator gives the maximum demand and the kVA rating to buy.'
            '\n\n'
            'Electrical engineers, contractors and plant planners use it at the design stage, because too small a unit overheats and too large a one wastes money and no-load losses. '
            f'See [how to calculate transformer kVA rating]({IB}/how-to-calculate-transformer-kva-rating/).'),
     replace=[(
         '## Example\n\n500 kW connected, 0.7 demand factor, 0.9 PF, 25% growth:\n\n- Maximum demand = 350 kW\n- kVA = 350 ÷ 0.9 × 1.25 = **486 kVA** → choose **500 kVA**\n',
         f'''## Worked example

A factory has **{P0:g} kW** of connected load, a demand factor of **{df0:g}**, a corrected power factor of **{pf0:g}** and allows **{g0*100:.0f}%** for growth:

- Maximum demand = {P0:g} × {df0:g} = **{Pd0:g} kW**
- Apparent power today = {Pd0:g} ÷ {pf0:g} = {Pd0/pf0:.1f} kVA
- Required rating = {Pd0/pf0:.1f} × (1 + {g0:g}) = **{S0:.0f} kVA**
- Next standard size: **{nxt(S0)} kVA**, whose full-load current at {V:g} V is {nxt(S0):,} × 1,000 ÷ (√3 × {V:g}) = **{Ifl(nxt(S0)):.0f} A**

On day one the {nxt(S0)} kVA unit runs at {load_now:.0f}% load, close to the 50 to 80% band where distribution transformers are most efficient.
''')],
     body_add=f'''
## Transformer size for common loads

Demand factor {df0:g}, power factor {pf0:g}, {g0*100:.0f}% growth, and full-load secondary current at {V:g} V for the chosen standard size:

| Connected load | Maximum demand | Required rating | Standard size | Full-load current |
|---|---|---|---|---|
{t_rows}
## Effect of power factor

For the example's {Pd0:g} kW maximum demand with {g0*100:.0f}% growth, a poor power factor pushes the rating up by one or two sizes:

| Power factor | Required rating | Standard size |
|---|---|---|
{pf_rows}
## Practical checks after sizing

- **Motor starting.** A large direct-on-line motor draws 6 to 7 times its full-load current. If the largest motor is more than about 20 to 30% of the transformer rating, check the voltage dip with the [motor starting voltage dip calculator](/electrical/motor-starting-voltage-dip/).
- **Harmonic loads.** Drives, UPS systems and LED lighting raise eddy losses; use a K-rated unit or derate by 10 to 20% when they make up much of the load.
- **Ambient and altitude.** Ratings assume about 40 °C maximum ambient and up to 1,000 m altitude; hotter or higher sites need derating.
- **Parallel or standby units.** Critical plants often split the load across two transformers, each able to carry the essential load alone.

## Common mistakes

- **Adding kW and kVA together.** Convert every load to the same basis before summing, and apply the power factor once.
- **Skipping the demand factor entirely or using a very low one.** Without measured data, an optimistic factor is the commonest cause of undersized transformers.
- **Using the power factor before correction when a capacitor bank is planned,** or after correction when it is not. The rating must match the power factor the transformer will actually see.
- **Counting standby equipment.** Duty and standby pumps do not run together; include only one of each pair.
- **Rounding down to a standard size.** A {S0:.0f} kVA requirement needs {nxt(S0)} kVA, never the size below it.
''',
     faq_add=[('What size transformer do I need for a 100 kW load?',
               f'At unity diversity and 0.9 power factor, 100 kW is 111 kVA, so 160 kVA with a growth margin. With the default 0.7 demand factor and 25% growth, 100 kW connected needs {100*df0/pf0*(1+g0):.0f} kVA, which is a 100 kVA unit.'),
              ('Can a transformer be loaded above its kVA rating?',
               'For short periods, yes: IEC 60076-7 allows cyclic overloads if the hot-spot temperature stays within limits, typically after a light-load period. Continuous overload ages the insulation quickly, roughly halving its life for every 6 to 7 °C of extra hot-spot temperature.')])

# ======================================================================= Capacitors in series and parallel
C1, C2 = 10e-6, 22e-6
Cs = 1 / (1 / C1 + 1 / C2)
Cp = C1 + C2
Vt = 50.0
V1 = Vt * C2 / (C1 + C2)
V2 = Vt * C1 / (C1 + C2)
Q = Cs * Vt
u = lambda c: f'{c*1e6:.3g} µF' if c >= 1e-6 else f'{c*1e9:.3g} nF'
combos = [(47e-6, 47e-6), (100e-9, 47e-9), (10e-6, 4.7e-6), (220e-9, 330e-9), (1e-6, 2.2e-6), (100e-6, 100e-6)]
c_rows = ''
for a, b in combos:
    c_rows += f"| {u(a)} and {u(b)} | {u(1/(1/a+1/b))} | {u(a+b)} |\n"
n_rows = ''
for n in (2, 3, 4):
    n_rows += f"| {n} × 100 µF, 50 V | {100/n:.1f} µF | {50*n} V | {100*n} µF | 50 V |\n"

edit('electronics/capacitors-series-parallel', date=U,
     title='Capacitors in Series and Parallel Calculator (Total C)',
     description='Calculate the total capacitance of up to four capacitors in series or parallel, with worked examples, voltage sharing and voltage rating guidance.',
     phrase='capacitors in series and parallel calculator',
     intro=('Capacitors combine the opposite way to resistors: in parallel their capacitances add, while in series the total is smaller than the smallest one. '
            'This capacitors in series and parallel calculator gives the equivalent capacitance of up to four parts.'
            '\n\n'
            'Students, technicians and designers use it to make odd values from stock parts or to raise a voltage rating. '
            f'See the [capacitor working principle]({IB}/capacitor-working-principle/) and [series vs parallel circuits]({IB}/series-vs-parallel-circuits-explained/).'),
     before='## Voltage ratings', min_words=0,
     body_add=f'''
## Worked example

A {C1*1e6:g} µF and a {C2*1e6:g} µF capacitor are connected in series across **{Vt:g} V**:

- 1/C = 1/{C1*1e6:g} + 1/{C2*1e6:g} = {1/(C1*1e6)+1/(C2*1e6):.5f} per µF, so **C = {Cs*1e6:.3f} µF** (or {C1*1e6:g} × {C2*1e6:g} ÷ ({C1*1e6:g} + {C2*1e6:g}))
- Both capacitors carry the same charge: Q = {Cs*1e6:.3f} µF × {Vt:g} V = **{Q*1e6:.1f} µC**
- Voltage on the {C1*1e6:g} µF part = Q ÷ C1 = **{V1:.1f} V**, and on the {C2*1e6:g} µF part **{V2:.1f} V**

The smaller capacitor takes the larger share: the {C1*1e6:g} µF part needs a rating above {V1:.1f} V (a 50 V part), while the {C2*1e6:g} µF part would manage with 25 V. Connected in parallel instead, the same two parts give **{Cp*1e6:g} µF** and each sees the full {Vt:g} V.
''')
edit('electronics/capacitors-series-parallel', date=U,
     body_add=f'''
## More combinations

| Capacitors | Series | Parallel |
|---|---|---|
{c_rows}
## Equal capacitors in series and parallel

Identical capacitors divide the capacitance by the number in series and multiply the voltage rating; in parallel the capacitance multiplies and the rating stays the same:

| Bank | Series C | Series rating | Parallel C | Parallel rating |
|---|---|---|---|---|
{n_rows}
## Practical notes

- **Balancing resistors.** Leakage current, not capacitance, sets the DC voltage split in a series stack over time. A resistor of equal value across each capacitor, passing roughly 5 to 10 times the leakage current, keeps the voltages equal.
- **Electrolytic tolerance.** Aluminium electrolytics are often ±20%, so two nominally equal parts in series may share the voltage 55:45. Leave margin on the rating.
- **Parallel for low ESR.** Several smaller capacitors in parallel have lower ESR and ESL than one large one, which is why decoupling and power supply output stages use banks of them.
- **Mixed values for decoupling.** Paralleling a 100 nF ceramic with a 10 µF capacitor covers a wider frequency range than either alone.

## Common mistakes

- **Adding series capacitors directly.** Two 10 µF capacitors in series make 5 µF, not 20 µF.
- **Assuming the voltage splits equally between unequal capacitors.** It splits in inverse proportion to capacitance, so the smallest part sees the most voltage.
- **Using the highest voltage rating in a parallel bank.** All parallel parts see the full voltage, so the lowest rating limits the bank.
- **Mixing units.** Entering one value in nF and another in µF without converting gives an answer off by a factor of 1,000.
- **Putting polarised electrolytics in series the wrong way.** For a non-polar pair, connect them back to back (negative to negative), and remember that only half the capacitance remains.
''',
     faq_add=[('How do I make a non-standard capacitance?',
               'Combine standard values. Two 47 µF capacitors in parallel give 94 µF, and 220 nF in series with 330 nF gives 132 nF. Parallel combinations are usually easier because the total is simply the sum.'),
              ('Does connecting capacitors in series increase the stored energy?',
               f'No. For the same voltage, energy is ½CV², and a series pair has less capacitance than either part. In the example, {u(Cs)} at {Vt:g} V stores {0.5*Cs*Vt**2*1000:.1f} mJ, while the parallel pair at the same voltage stores {0.5*Cp*Vt**2*1000:.1f} mJ.')])

print('done', DONE)
