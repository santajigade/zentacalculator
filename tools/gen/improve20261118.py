"""Improve pass (2026-11-18) for three thin pages from the first batch (2026-10-27):
electrical/braking-resistor, ecology/population-density, biology/pcr-amplification.
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples built from the calculator defaults, reference tables computed here,
practical notes, FAQ fixes (dash-free rewrites, a duplicate question and an outdated figure) and
better related ids. Slug, category, variables, equations and published are unchanged (asserted by
inplace.edit). Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, BASE
U = '2026-11-18'


def set_related(cid, old, new):
    p = os.path.join(BASE, cid + '.mdx')
    s = open(p).read()
    a = 'related: [' + ', '.join(old) + ']'
    assert s.count(a) == 1, (cid, 'related line')
    for r in new:
        assert os.path.exists(os.path.join(BASE, r + '.mdx')), r
    open(p, 'w').write(s.replace(a, 'related: [' + ', '.join(new) + ']'))


EN, EM = chr(0x2013), chr(0x2014)

# ---------------------------------------------------------------- Braking resistor
Vdc, Pb, dc = 760.0, 15.0, 0.10
R = Vdc ** 2 / (Pb * 1000)
Pr = Pb * dc
Ipk = Vdc / R
Rstd = 33.0
Pstd = Vdc ** 2 / Rstd / 1000
Istd = Vdc / Rstd
# inertia example: 5 kg m2 flywheel from 1,500 rpm to stop in 5 s, once every 50 s
J, rpm, tb, cyc = 5.0, 1500.0, 5.0, 50.0
w = rpm * 2 * math.pi / 60
Ek = 0.5 * J * w ** 2
Pavg_stop = Ek / tb
Ppk_stop = J * w ** 2 / tb
duty_fw = tb / cyc
Pcont_fw = Ek / cyc
brows = ''
for p in (2.2, 5.5, 7.5, 15, 30, 55):
    brows += (f"| {p:g} kW | {390**2/(p*1000):,.1f} Ω | {760**2/(p*1000):,.1f} Ω | {800**2/(p*1000):,.1f} Ω |"
              f" {p*1000/760:,.1f} A |\n")

edit('electrical/braking-resistor', date=U, phrase='braking resistor calculator',
     title='Braking Resistor Calculator for VFDs (Ohms, Power and Peak Current)',
     description='Size a VFD dynamic braking resistor: maximum ohms from DC bus voltage and braking power, average watts from duty cycle, and peak chopper current.',
     intro=("When a motor on a variable frequency drive slows down, it works as a generator and pushes energy back into the DC bus. "
            "This braking resistor calculator finds the largest resistance that can absorb that power, as covered in this "
            "[VFD braking resistor sizing](https://www.instrumentationblog.in/vfd-braking-resistor-sizing/) guide.\n\n"
            "Drive commissioning engineers and panel builders use it to choose a resistor value, its continuous power rating "
            "and the chopper current before ordering parts."),
     replace=[
         ('| 230 V | 375' + EN + '400 V DC |', '| 230 V | 375 to 400 V DC |'),
         ('| 400' + EN + '415 V | 750' + EN + '800 V DC |', '| 400 to 415 V | 750 to 800 V DC |'),
         ('| 480 V | 800' + EN + '850 V DC |', '| 480 V | 800 to 850 V DC |'),
         ('| 690 V | 1,100' + EN + '1,200 V DC |', '| 690 V | 1,100 to 1,200 V DC |'),
         ('For a flywheel or conveyor: P ≈ J × ω × Δω ÷ t (J in kg·m², ω in rad/s, t in s). Kinetic energy to dissipate is ½Jω².',
          'For a flywheel or conveyor stopped at constant torque, the peak braking power at the start of the stop is P ≈ J × ω² ÷ t and the average over the stop is half of that, ½Jω² ÷ t (J in kg·m², ω in rad/s, t in s). The kinetic energy to dissipate is ½Jω².'),
         ('For long or frequent braking ' + EM + ' cranes, centrifuges, downhill conveyors ' + EM + ' a regenerative',
          'For long or frequent braking, such as cranes, centrifuges and downhill conveyors, a regenerative'),
     ],
     body_add=f'''
## Worked example with the default values

A 400 V drive whose chopper switches on at {Vdc:g} V DC, braking {Pb:g} kW for {dc*100:g}% of the time:

- Maximum resistance = {Vdc:g}² ÷ {Pb*1000:,.0f} = {Vdc**2:,.0f} ÷ {Pb*1000:,.0f} = **{R:.1f} Ω**
- Average resistor power = {Pb:g} × {dc:g} = **{Pr:.1f} kW**
- Peak chopper current = {Vdc:g} ÷ {R:.1f} = **{Ipk:.1f} A** (the same as {Pb*1000:,.0f} ÷ {Vdc:g})

If you fit a standard **{Rstd:g} Ω** resistor instead, it can absorb up to {Vdc:g}² ÷ {Rstd:g} = **{Pstd:.1f} kW** at the threshold and draws **{Istd:.1f} A** through the chopper. That is fine as long as {Rstd:g} Ω is above the drive's minimum resistance and {Istd:.1f} A is within the chopper rating.

## Worked example: braking power from a flywheel

A {J:g} kg·m² flywheel spinning at {rpm:,.0f} rpm (ω = {w:.2f} rad/s) is stopped in {tb:g} s, once every {cyc:g} s:

1. Kinetic energy = ½ × {J:g} × {w:.2f}² = **{Ek/1000:.1f} kJ** per stop.
2. Peak braking power at the start of the stop = {J:g} × {w:.2f}² ÷ {tb:g} = **{Ppk_stop/1000:.1f} kW**; average over the stop = **{Pavg_stop/1000:.1f} kW**.
3. Duty cycle = {tb:g} ÷ {cyc:g} = **{duty_fw*100:.0f}%**, and the continuous resistor power is {Ek/1000:.1f} kJ ÷ {cyc:g} s = **{Pcont_fw/1000:.2f} kW**.

Size the resistance from the peak power and the rating from the average power; motor and drive losses absorb a few percent, which adds margin.

## Maximum resistance by braking power

| Peak braking power | At 390 V DC (230 V drive) | At 760 V DC (400 V drive) | At 800 V DC (480 V drive) | Current at 760 V |
|---|---|---|---|---|
{brows}
## Practical notes

- **Respect both limits.** The resistor must be at or below R<sub>max</sub> to absorb the peak power, and at or above the drive's minimum resistance to protect the chopper transistor.
- **Use the resistor's duty rating.** Catalogue resistors are often rated for a short duty (for example 10% over 120 s). For long stops, size on the energy per stop and check the resistor's thermal time constant.
- **Fit a thermal switch.** Wire the resistor's thermostat or a thermal overload into the drive's external fault input so a stuck chopper cannot overheat it.
- **Mount it safely.** Resistors can exceed 200 °C; place them where airflow is free and away from cable trays, and use cable rated for the full DC bus voltage.
''',
     faq_replace=[
         ('How do I size a braking resistor?', 'How do I size a braking resistor?',
          'Keep the resistance low enough to absorb the peak braking power, R ≤ Vdc² ÷ P, but not below the drive minimum. Then rate it for the average power, P × duty cycle. For 760 V and 15 kW, R ≤ 38.5 Ω and the rating is 1.5 kW.'),
         ('What is the duty cycle?', 'What is the duty cycle?',
          'The fraction of time spent braking. A 10 second stop every 100 seconds is 10%. Cranes, lifts and downhill conveyors can run at 20 to 50%.'),
     ],
     faq_add=[('What is the peak current through a braking resistor?',
               f'Peak current is the DC bus voltage divided by the resistance. With the default 760 V across {R:.1f} Ω it is {Ipk:.1f} A, which must not exceed the braking chopper current rating.')])
set_related('electrical/braking-resistor',
            ['engineering/torque-power-speed', 'physics/ohms-law', 'electrical/three-phase-motor-power', 'physics/kinetic-energy'],
            ['engineering/torque-power-speed', 'physics/rotational-kinetic-energy', 'electrical/three-phase-motor-power', 'physics/ohms-law', 'electrical/motor-starting-current'])

# ---------------------------------------------------------------- Population density
n, A = 1250000.0, 450.0
dk = n / A
dm = dk * 2.589988
dh = dk / 100
dac = dk / 247.105
m2pp = 1e6 / dk
# ecological example
deer, reserve, wood = 84, 12.0, 7.5
crude, eco = deer / reserve, deer / wood
# quadrats
quads = (12, 8, 15, 10, 9)
qmean = sum(quads) / len(quads)
qsd = math.sqrt(sum((x - qmean) ** 2 for x in quads) / (len(quads) - 1))
qha = qmean * 1e4
drows = ''
for d in (1, 10, 100, 500, 1000, round(dk), 10000):
    drows += f"| {d:,} | {d*2.589988:,.1f} | {d/100:,.2f} | {d/247.105:,.2f} | {1e6/d:,.0f} m² |\n"

edit('ecology/population-density', date=U, phrase='population density calculator',
     title='Population Density Calculator (per km², Hectare and Square Mile)',
     description='Calculate population density per km², per square mile and per hectare from a count and an area, with worked examples, unit tables and ecology tips.',
     intro=("Population density tells you how many people, animals or plants share each unit of area. This population density calculator "
            "divides a count by its area and gives the result per square kilometre, per square mile and per hectare at once.\n\n"
            "Geography students compare cities and countries with it, planners use it for housing and services, and ecologists "
            "use it to compare species between habitats and survey plots."),
     replace=[
         ('| India | about 480 per km² |', '| India | about 440 per km² |'),
         ('| Australia | about 3' + EN + '4 per km² |', '| Australia | about 3.5 per km² |'),
     ],
     body_add=f'''
## Worked example with the default values

A city of {n:,.0f} people on {A:g} km²:

- Density per km² = {n:,.0f} ÷ {A:g} = **{dk:,.1f} per km²**
- Density per square mile = {dk:,.1f} × 2.589988 = **{dm:,.1f} per square mile**
- Density per hectare = {dk:,.1f} ÷ 100 = **{dh:.2f} per hectare** (or {dac:.2f} per acre)

Turned around, each person has on average 1,000,000 ÷ {dk:,.1f} = **{m2pp:,.0f} m²** of land, which includes roads, parks and workplaces as well as homes.

## Worked example: crude and ecological density

A survey counts {deer} deer in a {reserve:g} km² reserve, of which {wood:g} km² is woodland they actually use:

- Crude density = {deer} ÷ {reserve:g} = **{crude:.1f} per km²**
- Ecological density = {deer} ÷ {wood:g} = **{eco:.1f} per km²**

The ecological figure is the one to compare with other woodlands, because open fields and water in the reserve hold almost no deer.

## Worked example: scaling up from quadrats

Five 1 m² quadrats contain {', '.join(str(q) for q in quads)} plants. The mean is **{qmean:.1f} per m²** (standard deviation {qsd:.1f}), which scales to {qmean:.1f} × 10,000 = **{qha:,.0f} plants per hectare**. Place quadrats at random or on a grid, and use more of them when counts vary a lot between plots.

## Density conversion table

| Per km² | Per square mile | Per hectare | Per acre | Area per individual |
|---|---|---|---|---|
{drows}
## Practical notes

- Use land area, not total area, for countries with large lakes or coastal waters; the two can differ by several percent.
- City figures depend on where the boundary is drawn. A city proper and its wider metropolitan area can differ in density by a factor of five or more.
- For mobile animals, density from a single count is a snapshot. Repeat surveys, or estimate the population with the mark and recapture method before dividing by area.
''',
     faq_replace=[
         ('How is population density calculated?', 'What is the difference between crude and ecological density?',
          'Crude density divides the population by the whole area. Ecological density divides it only by the habitat the species can use. 84 deer in a 12 km² reserve is 7.0 per km² crude, but 11.2 per km² across its 7.5 km² of woodland.'),
         ('Is density the same everywhere in an area?', 'Is density the same everywhere in an area?',
          'No. It is an average, and people, animals and plants are usually clustered. City centres and rich habitat patches are often far denser than the overall figure.'),
     ],
     faq_add=[('How do I convert density per hectare to per km²?',
               'Multiply by 100, because one square kilometre holds 100 hectares. The default city has 27.78 people per hectare, which is 2,777.8 per km².')])
set_related('ecology/population-density', ['ecology/mark-recapture', 'conversion/area-converter'],
            ['ecology/mark-recapture', 'conversion/area-converter', 'biology/exponential-population-growth', 'biology/logistic-growth'])

# ---------------------------------------------------------------- PCR amplification
N0, cyc_n, E = 1000.0, 30, 0.90
fold = (1 + E) ** cyc_n
N = N0 * fold
fold100 = 2.0 ** cyc_n
N100 = N0 * fold100
ratio = N100 / N
target = 1e10
ncyc_t = math.log(target / N0) / math.log(1 + E)
ncyc_t100 = math.log(target / N0) / math.log(2)
erows = ''
for s in (-3.1, -3.2, -3.32, -3.4, -3.5, -3.6):
    e = 10 ** (-1 / s) - 1
    erows += f"| {s:g} | {e*100:.1f}% | {(1+e):.3f} |\n"
def sci(x, d=2):
    m, e = f"{x:.{d}e}".split('e')
    return f"{m} × 10<sup>{int(e)}</sup>"


crows = ''
for c in (10, 15, 20, 25, 30, 35):
    crows += f"| {c} | {sci(N0*2**c)} | {sci(N0*1.95**c)} | {sci(N0*1.9**c)} | {sci(N0*1.8**c)} |\n"

edit('biology/pcr-amplification', date=U, phrase='PCR amplification calculator',
     title='PCR Amplification Calculator (DNA Copies, Cycles and Efficiency)',
     description='Estimate DNA copies and fold amplification after PCR from starting copies, cycle number and efficiency, with worked examples and qPCR efficiency tables.',
     intro=("Each PCR cycle can copy every target molecule once, so the amount of DNA grows exponentially. This PCR amplification calculator "
            "applies N = N₀ × (1 + E)ⁿ to give the theoretical copies and fold amplification for any efficiency.\n\n"
            "Molecular biology students and lab scientists use it to plan cycle numbers, see why efficiency matters so much "
            "and check whether a reaction is likely to reach the plateau."),
     replace=[
         ('showing how much efficiency matters.', 'which shows how much efficiency matters.'),
         ('copies ' + EM + ' which shows', 'copies, which shows'),
         ('somewhere around 10¹¹' + EN + '10¹² copies', 'somewhere around 10¹¹ to 10¹² copies'),
         ('Acceptable assays are usually 90' + EN + '110% (slope', 'Acceptable assays are usually 90% to 110% (slope'),
     ],
     body_add=f'''
## Worked example with the default values

{N0:,.0f} starting copies, {cyc_n} cycles at {E*100:.0f}% efficiency:

- Fold amplification = (1 + {E:g})<sup>{cyc_n}</sup> = {1+E:g}<sup>{cyc_n}</sup> = **{sci(fold, 3)}**
- Copies after PCR = {N0:,.0f} × {sci(fold, 3)} = **{sci(N, 3)} copies**

At 100% efficiency the same reaction would give 2<sup>{cyc_n}</sup> = {sci(fold100, 3)} fold and {sci(N100, 3)} copies, {ratio:.1f} times more. In a real 25 to 50 µL reaction the default result is already near the plateau, so the true yield will be lower than the theoretical figure.

## How many cycles to reach a target?

Rearranging the formula gives n = log(N ÷ N₀) ÷ log(1 + E). To reach 10¹⁰ copies from {N0:,.0f} starting copies takes log(10⁷) ÷ log({1+E:g}) = **{ncyc_t:.1f} cycles** at {E*100:.0f}% efficiency, or {ncyc_t100:.1f} cycles at 100%.

## Copies after each cycle from 1,000 starting copies

| Cycles | 100% | 95% | 90% | 80% |
|---|---|---|---|---|
{crows}
These are theoretical values; real reactions stop growing once they reach roughly 10¹¹ to 10¹² copies.

## qPCR efficiency from the standard curve slope

| Slope | Efficiency | Amplification factor per cycle |
|---|---|---|
{erows}
## Practical notes

- Use the fewest cycles that give enough product. Extra cycles past the plateau mostly add primer dimers and non-specific bands.
- For cloning or sequencing, start from more template rather than adding cycles, which also lowers the chance of copying polymerase errors.
- Count starting copies from DNA mass and length with a copy number calculation before planning a reaction.
''',
     faq_replace=[
         ('What is PCR efficiency?', 'What is PCR efficiency?',
          'The fraction of templates copied in each cycle. 100% means every molecule is copied, so the DNA doubles. Good qPCR assays run at about 90% to 110%.'),
         ('Does amplification continue forever?', 'Does amplification continue forever?',
          'No. After about 25 to 35 cycles the reaction plateaus as primers and nucleotides run out and the polymerase loses activity.'),
     ],
     faq_add=[('How many cycles do I need to reach a set number of copies?',
               f'Use n = log(N ÷ N₀) ÷ log(1 + E). Going from 1,000 to 10¹⁰ copies at 90% efficiency takes about {ncyc_t:.1f} cycles, or {ncyc_t100:.1f} cycles at 100%.')])
set_related('biology/pcr-amplification',
            ['biology/dna-concentration', 'biology/exponential-population-growth', 'biology/dna-copy-number', 'biology/primer-tm'],
            ['biology/dna-copy-number', 'biology/dna-concentration', 'biology/primer-tm', 'biology/serial-dilution'])
print('done')
