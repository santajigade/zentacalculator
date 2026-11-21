"""Improve pass (2026-11-21) for three thin pages from the first batch (2026-10-27):
sports/bowling-economy, other/battery-life, food/calories-from-macros.
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples built from the calculator defaults, reference tables computed here,
practical notes, common mistakes, dash-free rewrites of edited text, removal of a duplicated
example section, a near-duplicate FAQ replaced, and better related ids.
Slug, category, variables, equations and published are unchanged (asserted by inplace.edit).
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, BASE
U = '2026-11-21'


def set_related(cid, old, new):
    p = os.path.join(BASE, cid + '.mdx')
    s = open(p).read()
    a = 'related: [' + ', '.join(old) + ']'
    assert s.count(a) == 1, (cid, 'related line')
    for r in new:
        assert os.path.exists(os.path.join(BASE, r + '.mdx')), r
    open(p, 'w').write(s.replace(a, 'related: [' + ', '.join(new) + ']'))


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- Bowling economy
runs, wk, balls = 480.0, 20.0, 432.0
overs = balls / 6
econ = runs / overs
avg = runs / wk
sr = balls / wk
assert abs(econ - avg / sr * 6) < 1e-9
# one ODI spell written 10-1-42-3 (overs, maidens, runs, wickets)
o1, r1, w1 = 10, 42, 3
e1, a1, s1 = r1 / o1, r1 / w1, o1 * 6 / w1
# overs notation table
def ob(txt):
    o, b = txt.split('.')
    return int(o) * 6 + int(b)
on_rows = ''
for txt in ('3.2', '8.3', '9.5', '19.4', '71.5'):
    n = ob(txt)
    on_rows += f"| {txt} | {n} | {n/6:.3f} |\n"
# T20 spells, 4 overs each
t_rows = ''
for r_, w_ in ((24, 1), (28, 2), (32, 0), (36, 3), (45, 1)):
    e_ = r_ / 4
    a_ = f"{r_/w_:.1f}" if w_ else 'no wickets'
    s_ = f"{24/w_:.1f}" if w_ else 'none'
    t_rows += f"| 4-0-{r_}-{w_} | {e_:.2f} | {a_} | {s_} |\n"

old_tail = '''## Example

480 runs, 20 wickets, 432 balls (72 overs):

- Economy = 480 ÷ 72 = **6.67**
- Average = 480 ÷ 20 = **24.00**
- Strike rate = 432 ÷ 20 = **21.6**
'''
old_first = '''## Example

480 runs, 20 wickets, 432 balls (72 overs):

- Economy = **6.67**
- Average = **24.00**
- Strike rate = **21.6** balls per wicket
'''
new_first = f'''## Worked example with the default values

A bowler has conceded **{runs:.0f} runs**, taken **{wk:.0f} wickets** and bowled **{balls:.0f} balls** in a season:

- Overs bowled = {balls:.0f} ÷ 6 = **{overs:.0f} overs**
- Economy rate = {runs:.0f} ÷ {overs:.0f} = **{econ:.2f}** runs per over
- Bowling average = {runs:.0f} ÷ {wk:.0f} = **{avg:.2f}** runs per wicket
- Strike rate = {balls:.0f} ÷ {wk:.0f} = **{sr:.1f}** balls per wicket

The three numbers are tied together: economy = average ÷ strike rate × 6, here {avg:.0f} ÷ {sr} × 6 = {econ:.2f}. Knowing any two gives the third.

## One spell from a scorecard

Scorecards write bowling figures as overs, maidens, runs and wickets. A 10 over ODI spell of **{o1}-1-{r1}-{w1}** means {o1 * 6} balls, {r1} runs and {w1} wickets: economy **{e1:.2f}**, average **{a1:.0f}** and strike rate **{s1:.0f}**. Maidens do not enter any of the formulas; they are already counted in the balls and the runs.
'''
body_bowl = f'''
## T20 spells compared

Four overs is the maximum a bowler can bowl in a T20 innings, so a full spell is 24 balls:

| Figures | Economy | Average | Strike rate |
|---|---|---|---|
{t_rows}
A wicketless spell has no average or strike rate, because both divide by wickets. In the calculator, entering 0 wickets is not allowed for that reason.

## Overs to balls

| Overs written | Balls | Overs as a decimal |
|---|---|---|
{on_rows}
## Practical notes

- **Wides and no balls count against the bowler** in runs conceded, but they are not legal deliveries, so they do not add to the balls bowled.
- **Byes and leg byes are not charged to the bowler.** Use the bowler's runs column on the scorecard, not the runs scored while he was bowling.
- **Compare like with like.** A T20 economy of 7.5 is good, while the same figure in a Test match would be expensive. Use the benchmarks for the format being played.
- **Small samples mislead.** One spell of 3 wickets for 12 runs gives a superb average, but career averages only settle after a few hundred overs.

## Common mistakes

- **Dividing runs by the overs notation.** 8.3 overs is 51 balls, or 8.5 overs as a decimal, not 8.3.
- **Including byes and leg byes** in runs conceded, which makes the economy and average look worse than the official figures.
- **Counting wides and no balls as balls bowled,** which inflates the balls and flatters the economy and strike rate.
- **Judging a bowler on economy alone in Tests.** A miserly bowler who rarely takes wickets can have a fine economy and a poor strike rate.
- **Averaging averages across seasons.** Add up all runs and all wickets first, then divide, or a short season counts as much as a long one.
'''
edit('sports/bowling-economy', date=U, phrase='bowling economy calculator',
     title='Bowling Economy Calculator: Cricket Average and Strike Rate',
     description="Bowling economy calculator for cricket: find economy rate, bowling average and strike rate from runs conceded, wickets taken and balls bowled.",
     intro=("Economy rate, bowling average and strike rate are the three numbers that sum up a cricket bowler's work. "
            "This bowling economy calculator turns runs conceded, wickets taken and balls bowled into all three, using the same definitions as official scorecards.\n\n"
            "Players, coaches, selectors and fantasy league fans use it to compare bowlers across matches and seasons, and to judge whether a spell kept the runs down or took wickets."),
     replace=[(old_tail, ''), (old_first, new_first)],
     body_add=body_bowl,
     faq_replace=[('What is bowling average?', 'What is bowling average?',
                   'Runs conceded per wicket taken. Lower is better, and an average under 25 is excellent in Test cricket.'),
                  ('What is bowling strike rate?', 'What is bowling strike rate?',
                   'Balls bowled per wicket taken, which shows how often a bowler takes a wicket. Lower is better.')],
     faq_add=[('How do I convert 8.3 overs to balls?',
               'Multiply the completed overs by 6 and add the extra balls: 8 × 6 + 3 = 51 balls. As a decimal that is 8.5 overs, which is the figure to divide runs by.'),
              ('Can a bowler have a good economy but a poor average?',
               f'Yes. A bowler who concedes 3 runs per over but takes a wicket only every 120 balls has an economy of 3.00 and an average of 60. Average = economy × strike rate ÷ 6.')])
set_related('sports/bowling-economy', ['sports/cricket-batting', 'sports/cricket-run-rate'],
            ['sports/cricket-batting', 'sports/cricket-run-rate', 'sports/net-run-rate', 'sports/required-run-rate'])

# ---------------------------------------------------------------- Battery life
cap, I, ef = 2000.0, 50.0, 0.85
t = cap * ef / I
assert abs(t - 34) < 1e-9
# duty cycled sensor: 20 mA for 1 s every 60 s, 10 uA asleep
Ia, ta, Is, ts = 20.0, 1.0, 0.010, 59.0
Iavg = (Ia * ta + Is * ts) / (ta + ts)
t_sleep = cap * ef / Iavg
t_awake = cap * ef / Ia
# runtime table for 2,000 mAh at 85%
r_rows = ''
for i_ in (0.1, 1, 10, 50, 100, 250, 500):
    h = cap * ef / i_
    r_rows += f"| {i_:g} mA | {c(h, 0) if h >= 10 else f'{h:.1f}'} h | {h/24:,.1f} days |\n"
# coin cell
cr, Icr = 225.0, 0.010
t_cr = cr * ef / Icr
# energy of a phone battery
wh = 5000 * 3.85 / 1000
cells = [('AA alkaline', '2,000 to 2,800', '1.5'), ('AA NiMH rechargeable', '1,900 to 2,500', '1.2'),
         ('AAA alkaline', '1,000 to 1,200', '1.5'), ('CR2032 coin cell', '220 to 240', '3.0'),
         ('18650 Li-ion', '2,500 to 3,500', '3.6 to 3.7'), ('Smartphone battery', '3,000 to 5,000', '3.85')]
cell_rows = ''.join(f"| {a} | {b} mAh | {v} V |\n" for a, b, v in cells)

old_table = '''| AA alkaline | 2,000–2,800 mAh | 1.5 V |
| AA NiMH rechargeable | 1,900–2,500 mAh | 1.2 V |
| AAA alkaline | 1,000–1,200 mAh | 1.5 V |
| CR2032 coin cell | 220–240 mAh | 3 V |
| 18650 Li-ion | 2,500–3,500 mAh | 3.6–3.7 V |
| Smartphone battery | 3,000–5,000 mAh | 3.85 V |
'''
old_sleep = 'A sensor drawing 20 mA for 1 second every minute and 10 µA in sleep averages about 0.34 mA — a 2,000 mAh battery could last around **8 months** instead of 4 days.'
new_sleep = (f'A sensor drawing {Ia:g} mA for {ta:g} second every minute and 10 µA asleep averages ({Ia:g} × {ta:g} + 0.01 × {ts:g}) ÷ 60 = **{Iavg:.3f} mA**. '
             f'With 85% usable capacity a 2,000 mAh battery then lasts about {c(t_sleep)} h, roughly **{t_sleep/24/30.44:.1f} months**, instead of {t_awake:.0f} h ({t_awake/24:.1f} days) if it stayed awake.')
old_pb = '''A 10,000 mAh power bank (at 3.7 V) delivers less at 5 V USB output after conversion losses — typically 60–70% of its rating, about 6,000–7,000 mAh at the phone's battery voltage.'''
new_pb = '''A 10,000 mAh power bank is rated at its internal cell voltage of 3.7 V, which is 37 Wh. Boosting to 5 V for USB and then charging the phone both lose energy, so a phone typically receives about 60 to 70 percent of the rated mAh, or 6,000 to 7,000 mAh.'''
old_ex = 'Example\n\n2,000 mAh at 50 mA average with 85% usable: 2,000 × 0.85 ÷ 50 = **34 hours**.'
new_ex = f'''Worked example with the default values

A **{cap:,.0f} mAh** battery powers a device that draws **{I:g} mA** on average, and **{ef*100:.0f}%** of the rated capacity is usable before the device cuts out:

- Usable capacity = {cap:,.0f} × {ef} = {cap*ef:,.0f} mAh
- Runtime = {cap*ef:,.0f} ÷ {I:g} = **{t:.0f} hours** (about {t/24:.1f} days)

Without the 85% factor the same battery would be quoted at {cap/I:.0f} hours, which few real batteries achieve.'''
body_bat = f'''
## Runtime of a 2,000 mAh battery at different loads

Usable capacity 85%, constant current:

| Average current | Runtime | Days |
|---|---|---|
{r_rows}
At high currents the real figure is lower again, because alkaline and NiMH cells deliver less of their rated capacity when discharged fast. At very low currents, self discharge takes over: a CR2032 coin cell of {cr:.0f} mAh at 10 µA would last {c(t_cr)} h, or {t_cr/8766:.1f} years, on paper, but lithium coin cells lose around 1% a year and seals age, so plan for less.

## How to measure the average current

A multimeter on its mA range in series with the battery reads steady loads well. Devices that sleep and wake in bursts need a current logger, a shunt resistor with an oscilloscope, or a power profiler that integrates charge over a full cycle. Measure at least one complete wake and sleep cycle, including radio transmissions, which are usually the largest pulses.

## Practical notes

- Use the **cut-off voltage** of the device to choose the usable factor. A device that stops at 1.3 V per AA cell leaves much more charge unused than one that runs down to 0.9 V.
- **Cold reduces capacity.** Alkaline cells near 0 °C can deliver half their room temperature capacity; Li-ion and lithium primary cells fare better.
- **Ageing matters for rechargeables.** A Li-ion pack after a few hundred cycles may hold 80% of its new capacity, so lower the factor for an old pack.

## Common mistakes

- **Comparing mAh across voltages.** A 3.7 V 3,000 mAh cell holds about 2.5 times the energy of a 1.5 V 3,000 mAh cell; compare in Wh.
- **Using peak current instead of average current.** A radio that draws 120 mA for a few milliseconds per minute averages far less.
- **Forgetting regulator losses.** A linear regulator draws the full load current from the battery whatever the output voltage, and its quiescent current adds to sleep current.
- **Assuming the full rated capacity is usable.** Ratings are measured at low current and room temperature down to a low cut-off voltage.
- **Ignoring self discharge on multi year designs.** It can use more charge than the device itself in very low power sensors.
'''
edit('other/battery-life', date=U, phrase='battery life calculator',
     title='Battery Life Calculator: mAh Runtime in Hours',
     description='Battery life calculator: estimate runtime in hours from battery capacity in mAh, average current draw and usable capacity, with sleep mode examples.',
     intro=("A battery's runtime depends on how much charge it holds and how much current the device draws on average. "
            "This battery life calculator divides the usable capacity in mAh by the average current to give the expected runtime in hours.\n\n"
            "Electronics hobbyists, IoT and sensor designers and gadget buyers use it to pick a battery size, estimate how long a device will run between charges and check the effect of sleep modes."),
     replace=[(old_table, cell_rows), (old_sleep, new_sleep), (old_pb, new_pb), (old_ex, new_ex)],
     body_add=body_bat,
     faq_replace=[('How long will a 10,000 mAh power bank charge a phone?', 'How long will a 10,000 mAh power bank charge a phone?',
                   'Voltage conversion and charging losses mean a typical power bank delivers about 60 to 70 percent of its rated mAh to a phone, so a 10,000 mAh bank gives roughly one and a half to two charges of a 4,000 mAh phone.'),
                  ('How is battery life calculated?', 'How is battery life calculated?',
                   'Runtime in hours = capacity in mAh × usable fraction ÷ average current in mA. The usable fraction allows for losses, temperature and the cut-off voltage of the device.')],
     faq_add=[('How do I convert mAh to Wh?',
               f'Multiply mAh by the nominal voltage and divide by 1,000. A 5,000 mAh phone battery at 3.85 V holds {wh:.2f} Wh.')])
set_related('other/battery-life', ['other/due-date', 'other/grade-percentage', 'ecology/battery-storage', 'electronics/led-resistor'],
            ['electronics/battery-charge-time', 'everyday-life/inverter-battery-backup', 'electrical/ups-sizing', 'ecology/battery-storage', 'electronics/led-resistor'])

# ---------------------------------------------------------------- Calories from macros
p, cb, f, al = 25.0, 40.0, 15.0, 0.0
kcal = 4 * p + 4 * cb + 9 * f + 7 * al
fpct = 9 * f / kcal
kj = kcal * 4.184
# meal split table: grams for a 500 kcal meal
m_rows = ''
for P_, C_, F_ in ((30, 40, 30), (25, 50, 25), (40, 30, 30), (20, 30, 50), (15, 55, 30)):
    E = 500
    m_rows += f"| {P_} / {C_} / {F_} | {E*P_/100/4:.0f} g | {E*C_/100/4:.0f} g | {E*F_/100/9:.0f} g |\n"
# drink: standard 14 g alcohol plus 10 g carbohydrate
drink = 7 * 14 + 4 * 10
# fibre correction: 40 g carbs of which 8 g fibre counted at 2 kcal
fib = 8
kcal_fib = 4 * p + 4 * (cb - fib) + 2 * fib + 9 * f

old_ex = '''## Example

25 g protein, 40 g carbohydrate, 15 g fat:

- kcal = 100 + 160 + 135 = **395 kcal**
- Calories from fat = 135 ÷ 395 = **34%**
'''
new_ex = f'''## Worked example with the default values

A meal with **{p:.0f} g protein**, **{cb:.0f} g carbohydrate**, **{f:.0f} g fat** and no alcohol:

- Protein: {p:.0f} × 4 = {4*p:.0f} kcal
- Carbohydrate: {cb:.0f} × 4 = {4*cb:.0f} kcal
- Fat: {f:.0f} × 9 = {9*f:.0f} kcal
- Total = {4*p:.0f} + {4*cb:.0f} + {9*f:.0f} = **{kcal:.0f} kcal** ({kj:,.0f} kJ)
- Calories from fat = {9*f:.0f} ÷ {kcal:.0f} = **{fpct*100:.1f}%**

The same meal gets {4*p/kcal*100:.1f}% of its energy from protein and {4*cb/kcal*100:.1f}% from carbohydrate. If 8 of the 40 g of carbohydrate is fibre counted at 2 kcal per gram, the total drops to {kcal_fib:.0f} kcal.
'''
body_cal = f'''
## Grams for a 500 kcal meal at common splits

The split is the share of calories from protein, carbohydrate and fat. Grams = calories × share ÷ kcal per gram:

| Protein / carbs / fat (%) | Protein | Carbohydrate | Fat |
|---|---|---|---|
{m_rows}
## Alcohol counts too

Alcohol is not a nutrient but it supplies 7 kcal per gram. A drink with 14 g of alcohol (one US standard drink) and 10 g of sugar provides 7 × 14 + 4 × 10 = **{drink} kcal**, before any mixer. Enter the alcohol grams to see how much of a meal's energy comes from drinks.

## Practical notes

- Use the **grams per serving** from the label and multiply by the number of servings you actually eat.
- In the EU, labels list carbohydrate without fibre and give fibre separately at 2 kcal per gram; US labels include fibre in total carbohydrate. Subtract fibre when comparing.
- Sugar alcohols such as erythritol provide little or no energy, so a low sugar product can show fewer calories than 4 kcal per gram of total carbohydrate suggests.

## Common mistakes

- **Using 9 kcal per gram for all macros.** Only fat is 9; protein and carbohydrate are 4.
- **Adding sugar on top of carbohydrate.** Sugar is part of total carbohydrate on the label, so counting it twice inflates the total.
- **Mixing cooked and raw weights.** Rice, pasta and meat change weight on cooking, so take grams from the same state as the nutrition data.
- **Expecting an exact match with the label.** Rounding to the nearest 5 or 10 kcal and different fibre factors cause small differences.
- **Reading the percentage as grams.** 34% of calories from fat is not 34% of the food's weight.
'''
edit('food/calories-from-macros', date=U, phrase='calories from macros calculator',
     title='Calories from Macros Calculator: Protein, Carbs and Fat',
     description='Calories from macros calculator: add up kcal from grams of protein, carbohydrate, fat and alcohol and see the share of calories that comes from fat.',
     intro=("Every food's energy comes from its protein, carbohydrate, fat and alcohol, which supply about 4, 4, 9 and 7 kcal per gram. "
            "This calories from macros calculator adds those up to give total calories and the share coming from fat.\n\n"
            "Dieters, athletes, nutrition students and cooks use it to check a nutrition label, plan meals to a macro split, or work out the calories in a home recipe from its ingredients."),
     replace=[(old_ex, new_ex)],
     body_add=body_cal,
     faq_replace=[('How many calories are in a gram of fat?', 'How many calories are in an alcoholic drink?',
                   f'Alcohol gives 7 kcal per gram. A drink with 14 g of alcohol and 10 g of sugar provides about {drink} kcal, before any mixer.')],
     faq_add=[('How do I find the percentage of calories from protein?',
               f'Multiply protein grams by 4 and divide by total calories. For {p:.0f} g protein in a {kcal:.0f} kcal meal: {4*p:.0f} ÷ {kcal:.0f} = {4*p/kcal*100:.1f}%.')])
set_related('food/calories-from-macros', ['health/macros', 'health/bmr', 'conversion/energy-converter'],
            ['health/macros', 'health/bmr', 'health/protein-intake', 'health/alcohol-units', 'conversion/energy-converter'])
print('improve done')
