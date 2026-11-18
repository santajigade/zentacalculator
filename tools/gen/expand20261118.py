"""Part C expansion (2026-11-18): 30 priority pages (crawled, not indexed) brought to the api-gravity standard. Assembled from six sections; edits are applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-18), slice 1: bearing-life, autotransformer, battery-bank-size, bayes-theorem,
electric-field. Numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-18'

# ---------------------------------------------------------------- Bearing life
p, C, P, N = 3, 32.5, 4.0, 1500.0
L10 = (C / P) ** p
L10h = L10 * 1e6 / (60 * N)
a1 = [(90, 1.0), (95, 0.64), (96, 0.55), (97, 0.47), (98, 0.37), (99, 0.25)]
a1_rows = ''.join(f"| {r}% | {a:.2f} | {L10 * a:,.1f} | {L10h * a:,.0f} h |\n" for r, a in a1)
Lreq_h = 20000
Lreq = Lreq_h * 60 * N / 1e6
Creq = P * Lreq ** (1 / p)
fd = 1.3
L10h_fd = (C / (P * fd)) ** p * 1e6 / (60 * N)
L10h_3000 = L10 * 1e6 / (60 * 3000)

edit('engineering/bearing-life', date=U, phrase='bearing life calculator',
     intro=("Rolling bearings wear out by fatigue of the raceways and rolling elements, so their life is stated statistically as L10, the life that 90% of identical bearings reach or exceed. "
            "This bearing life calculator applies the ISO 281 equation L10 = (C ÷ P)^p and converts the result to operating hours at the shaft speed.\n\n"
            "Machine designers use it to select a bearing size, and maintenance engineers use it to judge whether a replacement bearing suits a new duty."),
     body_add=f'''
## Life at higher reliability (factor a<sub>1</sub>)

L10 accepts that 1 bearing in 10 fails first. For aerospace, medical or hard-to-reach equipment a higher survival rate is specified, and ISO 281 scales the life by a reliability factor a<sub>1</sub>. For the default 6208-size bearing (C = {C:g} kN, P = {P:g} kN, {N:,.0f} rpm):

| Reliability | a<sub>1</sub> | Life (million rev) | Life at {N:,.0f} rpm |
|---|---|---|---|
{a1_rows}
Asking for 99% survival instead of 90% cuts the usable life to a quarter, from {L10h:,.0f} h to {L10h*0.25:,.0f} h.

## Choosing a bearing for a target life

Work backwards from the hours the machine needs. For 20,000 h at {N:,.0f} rpm the bearing must survive {Lreq_h:,} × 60 × {N:,.0f} ÷ 10⁶ = **{Lreq:,.0f} million revolutions**. The required rating is then C = P × L<sub>10</sub><sup>1/p</sup> = {P:g} × {Lreq:,.0f}<sup>1/3</sup> = **{Creq:.1f} kN**. The default bearing at {C:g} kN falls short, so the designer moves to a wider series or a larger bore, or reduces the load.

## Getting the load right in practice

The load P in the equation is the equivalent dynamic load, not the static weight. Gear meshing, belt pull, unbalance and shock all add to it, so catalogues multiply the calculated load by a service factor, commonly 1.0 to 1.2 for smooth electric motor drives and 1.5 or more for crushers and vibrating screens. Applying a factor of {fd} to the default case drops the life from {L10h:,.0f} h to **{L10h_fd:,.0f} h**, because life falls with the cube of load. Speed matters linearly: the same bearing at 3,000 rpm lasts only {L10h_3000:,.0f} h.

## Common mistakes

- **Using the static rating C<sub>0</sub>.** C<sub>0</sub> limits permanent deformation under a stationary load; the life equation needs the dynamic rating C.
- **Using p = 3 for a roller bearing.** Cylindrical, taper and spherical roller bearings use 10/3, which gives noticeably longer life at the same C/P.
- **Ignoring the axial load.** A thrust component can raise P well above the radial load; use P = X F<sub>r</sub> + Y F<sub>a</sub> with the catalogue factors.
- **Reading L10 as a guaranteed minimum.** One bearing in ten is expected to fail before L10, so stock spares accordingly.
- **Mixing N and kN.** C and P must be in the same unit; a 32.5 kN rating against a 4,000 N load gives a life a billion times too small.
''',
     faq_add=[('How do I find the bearing size needed for a target life?',
               f'Convert the target hours to revolutions (hours × 60 × rpm ÷ 10⁶), then C = P × L10^(1/p). For 20,000 h at 1,500 rpm under 4 kN, a ball bearing needs C of at least {Creq:.1f} kN.')])

# ---------------------------------------------------------------- Autotransformer
S, Vh, Vl = 10.0, 240.0, 200.0
Ih = S * 1000 / Vh
Il = S * 1000 / Vl
Ic = Il - Ih
K = Vl / Vh
Si = S * (1 - K)
Sc = S * K
Sser = Ih * (Vh - Vl) / 1000
Scom = Ic * Vl / 1000
tap_rows = ''
for t in (0.50, 0.65, 0.80):
    tap_rows += f"| {t*100:.0f}% | {t*100:.0f}% of DOL | {t*t*100:.1f}% of DOL | {t*t*100:.1f}% of DOL |\n"
cur_rows = ''
for v in (220, 200, 180, 160, 120):
    ih, il = S * 1000 / Vh, S * 1000 / v
    cur_rows += f"| {Vh:.0f} / {v} V | {ih:.2f} A | {il:.2f} A | {il-ih:.2f} A | {S*(1-v/Vh):.3f} kVA |\n"
Zpu = 4.0
Zauto = Zpu * (1 - K)

edit('electrical/autotransformer', date=U, phrase='autotransformer calculator',
     intro=("An autotransformer uses one tapped winding for both sides, so part of the power flows straight through by conduction and only the rest is transformed magnetically. "
            "This autotransformer calculator gives the line and common-winding currents, the transformed and conducted kVA and the copper saving. "
            "See the [autotransformer working principle](https://www.instrumentationblog.in/autotransformer-working-principle/).\n\n"
            "Electrical engineers use it to size voltage boosters, motor starters and interbus transformers where isolation is not needed."),
     body_add=f'''
## Checking the two winding sections

An autotransformer is really two windings in series. In the default 10 kVA, 240/200 V unit:

- The **series section** spans {Vh-Vl:.0f} V and carries the high-side current: {Ih:.2f} A × {Vh-Vl:.0f} V = **{Sser:.3f} kVA**
- The **common section** spans {Vl:.0f} V and carries the difference current: {Ic:.2f} A × {Vl:.0f} V = **{Scom:.3f} kVA**

Both equal the transformed power of {Si:.3f} kVA, which is why the core and copper are sized for about a sixth of the load. The common section can use wire rated for only {Ic:.2f} A, while the series section must carry {Ih:.2f} A.

## Winding currents for a 10 kVA unit fed at 240 V

| Ratio | High-side current | Low-side current | Common winding | Transformed kVA |
|---|---|---|---|---|
{cur_rows}
## Autotransformer motor starter taps

On a starter, the motor sees the tap voltage, its current falls in proportion and the line current falls by the square, as does torque:

| Tap | Motor current | Line current | Starting torque |
|---|---|---|---|
{tap_rows}
The 65% tap is the usual compromise when the driven load needs at least 40% of full-voltage torque to break away.

## Fault level

Because only the series section separates the two systems, the per-unit impedance on the throughput rating is (1 − K) times that of the same core connected as a two-winding transformer. A {Zpu:g}% impedance becomes about **{Zauto:.2f}%**, so downstream fault current can be six times higher. Breakers and fuses on the low side must be rated for it.

## Common mistakes

- **Buying on transformed kVA.** The nameplate rating is the throughput load, {S:g} kVA here, not the {Si:.3f} kVA transformed.
- **Expecting isolation.** The output is bonded to the input, so it cannot be used to create a separately derived system or a safe low-voltage supply.
- **Using a large ratio.** At 400/100 V the copper saving is only 25% and an open common winding would put 400 V on 100 V equipment.
- **Leaving the neutral unconnected in a three-phase star unit.** The star point must be tied to the supply neutral or the phase voltages float.
''',
     faq_add=[('Is the nameplate kVA of an autotransformer the transformed power or the load power?',
               f'The nameplate states the load (throughput) power. A 10 kVA, 240/200 V autotransformer supplies a 10 kVA load, though only {Si:.3f} kVA of it passes through the magnetic circuit.')])

# ---------------------------------------------------------------- Battery bank size
Pl, tb, V, eta, dod, k, Vb = 500.0, 4.0, 48.0, 0.90, 0.80, 1.25, 12.0
E = Pl * tb
Ah = E / (V * eta * dod) * k
ns = V / Vb
Idc = Pl / (V * eta)
Ah50 = E / (V * eta * 0.5) * k
Ah90 = E / (V * eta * 0.9) * k
volt_rows = ''
for v in (12, 24, 48):
    a = E / (v * eta * dod) * k
    volt_rows += f"| {v} V | {v//12} | {Pl/(v*eta):.1f} A | {a:.1f} Ah |\n"
dod_rows = ''
for name, d in (('Flooded lead-acid, long life', 0.5), ('AGM or gel', 0.6), ('Lead-acid, occasional use', 0.8), ('LiFePO₄', 0.9)):
    dod_rows += f"| {name} | {d*100:.0f}% | {E/(V*eta*d)*k:.1f} Ah |\n"
idle = 25.0
Ah_idle = (E + idle * tb) / (V * eta * dod) * k
t100 = V * 100 * eta * dod / k / Pl
strings50 = math.ceil(Ah / 50)

edit('electrical/battery-bank-size', date=U, phrase='battery bank size calculator',
     intro=("Sizing a battery bank starts with the energy the load needs, then allows for inverter losses, safe depth of discharge and capacity lost with age. "
            "This battery bank size calculator gives the amp-hour capacity and the number of batteries in series. See [how to calculate battery backup time](https://www.instrumentationblog.in/calculate-battery-backup-time/) "
            "and [IEEE 485 substation battery sizing](https://www.instrumentationblog.in/substation-battery-sizing-ieee-485/).\n\n"
            "Solar installers, UPS designers and substation engineers use it to choose a bank that still covers the load at end of life."),
     body_add=f'''
## Building the bank from real batteries

The default case needs {Ah:.1f} Ah at 48 V, which is {ns:.0f} batteries of 12 V in series. Two common ways to meet it:

- **One string of 100 Ah batteries:** 4 batteries. Backup = 48 × 100 × {eta} × {dod} ÷ {k} ÷ {Pl:.0f} = **{t100:.2f} h**, comfortably above the 4 h target.
- **50 Ah batteries:** {Ah:.1f} ÷ 50 rounds up to {strings50} parallel strings, so {strings50 * int(ns)} batteries in total.

Fewer, larger cells are better. Each extra parallel string adds connections and lets current share unevenly between strings, so most makers advise no more than three or four.

## Same load on different bank voltages

The energy stays at {E:,.0f} Wh, but the Ah and the battery current change with voltage:

| Bank voltage | 12 V batteries in series | Battery current | Capacity needed |
|---|---|---|---|
{volt_rows}
On a 12 V bank the cables carry four times the current of a 48 V bank, which is why anything above a few hundred watts is better built at 24 or 48 V.

## Effect of battery chemistry

Depth of discharge has the largest effect after the load itself. For the default 500 W, 4 h load on 48 V:

| Battery type | Typical DoD | Capacity needed |
|---|---|---|
{dod_rows}
A long-life flooded bank needs {Ah50:.0f} Ah where LiFePO₄ needs {Ah90:.0f} Ah, which narrows the price gap between the two.

## Common mistakes

- **Leaving out the inverter's own consumption.** A {idle:.0f} W idle draw adds {idle*tb:.0f} Wh over 4 h and raises the requirement to {Ah_idle:.1f} Ah.
- **Adding Ah across a series string.** Four 12 V, 100 Ah batteries in series make 48 V, 100 Ah, not 400 Ah.
- **Mixing old and new batteries.** The weakest unit sets the string capacity and is driven into deep discharge first.
- **Sizing for the rated load instead of the actual load.** Measure the real average power; a nominal 500 W inverter rarely runs at 500 W for hours.
- **Skipping the margin for lithium.** LiFePO₄ also loses capacity with cycles, so keep a factor of at least 1.1 to 1.25.
''',
     faq_add=[('How long will an existing battery bank last?',
               f'Rearrange the same formula: hours = bank V × Ah × efficiency × DoD ÷ margin ÷ load W. Four 12 V, 100 Ah batteries in series at 90% efficiency and 80% DoD with a 1.25 margin run a 500 W load for about {t100:.1f} h.')])

# ---------------------------------------------------------------- Bayes' theorem
pA, pBA, pBnA = 0.01, 0.95, 0.05
pB = pBA * pA + pBnA * (1 - pA)
pAB = pBA * pA / pB
pAnB = (1 - pBA) * pA / (1 - pB)
n = 10000
TP, FN = n * pA * pBA, n * pA * (1 - pBA)
FP, TN = n * (1 - pA) * pBnA, n * (1 - pA) * (1 - pBnA)
LRp = pBA / pBnA
LRn = (1 - pBA) / (1 - pBnA)
odds0 = pA / (1 - pA)
odds1 = odds0 * LRp
seq_rows = ''
pr = pA
for i in range(1, 5):
    post = pBA * pr / (pBA * pr + pBnA * (1 - pr))
    seq_rows += f"| {i} | {pr*100:.2f}% | {post*100:.2f}% |\n"
    pr = post
NPV = TN / (TN + FN)

edit('statistics/bayes-theorem', date=U, phrase="Bayes' theorem calculator",
     intro=("Bayes' theorem updates a prior belief with new evidence, turning the chance of a positive result given a condition into the chance of the condition given a positive result. "
            "This Bayes' theorem calculator works from the prior, the true-positive rate and the false-positive rate.\n\n"
            "Doctors, data scientists and reliability engineers use it to judge test results, spam filters and alarms, "
            "where rare events mean that most positives can be false."),
     body_add=f'''
## The default case as counts

Probabilities are easier to read as people. With the default 1% prior, 95% sensitivity and 5% false-positive rate, out of {n:,} people:

| | Test positive | Test negative | Total |
|---|---|---|---|
| Has A | {TP:.0f} (true positive) | {FN:.0f} (false negative) | {TP+FN:.0f} |
| Does not have A | {FP:.0f} (false positive) | {TN:,.0f} (true negative) | {FP+TN:,.0f} |
| Total | {TP+FP:.0f} | {FN+TN:,.0f} | {n:,} |

The posterior is the first column read downwards: {TP:.0f} ÷ {TP+FP:.0f} = **{pAB*100:.2f}%**, matching the calculator. A negative result is very reliable here: {TN:,.0f} of {FN+TN:,.0f} negatives are correct, a negative predictive value of {NPV*100:.2f}%.

## Odds and likelihood ratios

Clinicians often use the odds form, posterior odds = prior odds × likelihood ratio. The positive likelihood ratio is {pBA} ÷ {pBnA} = **{LRp:.0f}**. Prior odds of 1 : 99 = {odds0:.4f} become {odds1:.4f}, and converting back, {odds1:.4f} ÷ (1 + {odds1:.4f}) = {odds1/(1+odds1)*100:.2f}%. The negative likelihood ratio is {1-pBA:.2f} ÷ {1-pBnA:.2f} = {LRn:.4f}, so a negative result cuts the odds about nineteenfold. Likelihood ratios are handy because they do not depend on prevalence and can be quoted for a test once.

## Repeated positive results

If a second test is truly independent, the first posterior becomes the new prior:

| Positive tests in a row | Prior before the test | Posterior after it |
|---|---|---|
{seq_rows}
Two positives take the probability from 1% to about {pBA*pAB/(pBA*pAB+pBnA*(1-pAB))*100:.0f}%, which is why screening programmes confirm a positive with a second, different test.

## Common mistakes

- **Swapping P(A|B) and P(B|A).** A 95% chance of a positive given the condition is not a 95% chance of the condition given a positive. This is the prosecutor's fallacy.
- **Entering specificity as the false-positive rate.** A 95% specific test has a false-positive rate of 5%, not 95%.
- **Repeating the same test and treating it as independent.** A sample that cross-reacts once will usually cross-react again, so the second result adds little.
- **Using population prevalence for a selected group.** Someone sent for testing because of symptoms has a much higher prior than the general population.
- **Entering percentages as fractions or the reverse.** Check that 1% is entered as 1% and not as 0.01%.
''',
     faq_add=[('What is the likelihood ratio form of Bayes\' theorem?',
               f'Posterior odds = prior odds × likelihood ratio, where the positive likelihood ratio is sensitivity ÷ false-positive rate. For 95% and 5% it is {LRp:.0f}, so prior odds of 1 : 99 become about 1 : {1/odds1:.1f}, a posterior of {pAB*100:.1f}%.')])

# ---------------------------------------------------------------- Electric field
kC = 8.9875517923e9
q, r, q0 = 5e-6, 0.5, 1e-6
Ef = kC * q / r ** 2
Vp = kC * q / r
F = Ef * q0
W = q0 * Vp
Ebd = 3e6
rmin = math.sqrt(kC * q / Ebd)
e = 1.602176634e-19
a0 = 5.29177210903e-11
E_H = kC * e / a0 ** 2
E_mem = 0.070 / 7e-9
ref_rows = (f"| Fair-weather atmosphere near the ground | about 100 V/m |\n"
            f"| ICNIRP public limit, 50 Hz | 5,000 V/m |\n"
            f"| Default 5 µC charge at 0.5 m | {Ef:,.0f} V/m |\n"
            f"| Breakdown of dry air | about 3 × 10⁶ V/m |\n"
            f"| Across a cell membrane (70 mV over 7 nm) | {E_mem/1e7:.0f} × 10⁷ V/m |\n"
            f"| At the Bohr radius of hydrogen | {E_H/1e11:.2f} × 10¹¹ V/m |\n")
E1 = kC * q / 1.0 ** 2

edit('physics/electric-field', date=U, phrase='electric field calculator',
     intro=("A point charge creates an electric field that weakens with the square of distance and a potential that falls with distance itself. "
            "This electric field calculator applies Coulomb's law to give the field strength E, the potential V and the force on a test charge, "
            "the same field a [capacitor uses to store energy](https://www.instrumentationblog.in/capacitor-working-principle/).\n\n"
            "Physics students use it for electrostatics problems, and engineers use it to estimate fields near charged electrodes and conductors."),
     body_add=f'''
## Work done on the test charge

The potential tells you the energy per coulomb. Bringing the default 1 µC test charge in from far away to 0.5 m from the 5 µC charge takes W = q<sub>0</sub> V = 1 × 10⁻⁶ × {Vp:,.0f} = **{W:.4f} J**. Both charges are positive, so this work is stored as potential energy and released if the test charge is let go. With a negative test charge the sign flips and the charges attract.

Doubling the distance to 1 m cuts the field to a quarter, {E1:,.0f} V/m, but the potential only to half, {kC*q/1.0:,.0f} V.

## How large can the source be?

The field at the surface of a charged sphere of radius a is kq ÷ a². Air breaks down near 3 × 10⁶ V/m, so a sphere holding 5 µC must have a radius of at least √(kq ÷ E) = √({kC*q:,.0f} ÷ 3 × 10⁶) = **{rmin*100:.1f} cm**. A smaller ball would leak charge by corona discharge. This is why Van de Graaff generators use large, smooth domes.

## Typical field strengths

| Situation | Field strength |
|---|---|
{ref_rows}
In practice, static and low-frequency fields are measured with a field mill, which uses a rotating shutter to chop the field over a sensing plate, or with a small probe meter around power lines and substations. Near real conductors the field is set by their shape, so the point-charge formula is a far-field estimate.

## Common mistakes

- **Forgetting the micro prefix.** 5 µC is 5 × 10⁻⁶ C; leaving it as 5 C gives a field a million times too large.
- **Entering distance in centimetres.** r must be in metres, and because it is squared, a cm error is a factor of 10,000.
- **Adding fields from several charges as plain numbers.** Fields are vectors; add their x and y components. Only potentials add as scalars.
- **Dropping the sign of the potential.** A negative charge gives a negative potential, which matters when computing work.
- **Using the formula inside a conductor.** The static field inside a conductor is zero; the 1/r² law applies outside the charge.
''',
     faq_add=[('How much work does it take to bring a test charge to a point near a charge?',
               f'The work equals the test charge times the potential at that point, W = q0 × V. For a 1 µC charge moved to 0.5 m from a 5 µC charge, W = 10⁻⁶ × {Vp:,.0f} V = {W:.4f} J.')])

print('done', __import__('inplace').DONE)

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-18), slice 2: final-temperature, exponential-distribution, energy-meter-constant,
string-frequency, bolt-torque. All numbers computed here from each page's default inputs."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-18'
pi = math.pi

# ---------------------------------------------------------------- Final temperature
m1, c1, T1, m2, c2, T2 = 0.5, 897.0, 150.0, 2.0, 4186.0, 20.0
C1, C2 = m1 * c1, m2 * c2
Tf = (C1 * T1 + C2 * T2) / (C1 + C2)
Q = C1 * (T1 - Tf) / 1000
# with a 0.3 kg aluminium calorimeter cup starting at the water temperature
Ccup = 0.3 * 897
Tf_cup = (C1 * T1 + (C2 + Ccup) * T2) / (C1 + C2 + Ccup)
# method of mixtures: unknown metal 0.5 kg at 150 C into 2 kg water at 20 C reaches 23.5 C
Tm = 23.5
c_unk = C2 * (Tm - T2) / (m1 * (T1 - Tm))
# sensitivity: 0.1 C error in Tm
c_unk2 = C2 * (Tm + 0.1 - T2) / (m1 * (T1 - Tm - 0.1))
mix_rows = ''
for mb in (0.1, 0.25, 0.5, 1.0, 2.0, 5.0):
    tf = (mb * c1 * T1 + C2 * T2) / (mb * c1 + C2)
    q = mb * c1 * (T1 - tf) / 1000
    mix_rows += f"| {mb:g} kg | {mb*c1:,.1f} J/K | {tf:.2f} °C | {q:.2f} kJ |\n"

edit('physics/final-temperature', date=U, phrase='final temperature calculator',
     intro=("When a hot and a cold substance share an insulated container, heat flows until both settle at one temperature, and the heat lost equals the heat gained. "
            "This final temperature calculator solves that balance from each substance's mass, specific heat and starting temperature.\n\n"
            "Physics students use it for calorimetry problems, lab technicians for method of mixtures tests, "
            "and engineers and cooks for quenching parts or blending hot and cold liquids."),
     body_add=f'''
## Why the result sits close to the water temperature

The final temperature is a weighted average, and the weights are the heat capacities m × c. In the default example the water holds {C2:,.0f} J/K against the aluminium block's {C1:,.1f} J/K, so the water carries {C2/(C1+C2)*100:.1f}% of the weight. That is why a block at {T1:g} °C only lifts the water from {T2:g} °C to {Tf:.2f} °C. The table keeps the 2 kg of water at {T2:g} °C and changes the mass of the aluminium block at {T1:g} °C:

| Aluminium mass | Heat capacity m·c | Final temperature | Heat given to water |
|---|---|---|---|
{mix_rows}
Doubling the block mass does not double the temperature rise, because a bigger block also stops at a higher temperature and gives up less heat per kilogram.

## Allowing for the container

A real calorimeter cup warms up too. If the 2 kg of water sits in a 0.3 kg aluminium cup that starts at {T2:g} °C, the cup adds {Ccup:.1f} J/K to the cold side and the equilibrium drops to **{Tf_cup:.2f} °C** instead of {Tf:.2f} °C. Add the vessel's heat capacity (its water equivalent) to substance 2, or measure it once by mixing known masses of hot and cold water.

## Finding an unknown specific heat

The method of mixtures runs the equation backwards. Drop 0.5 kg of an unknown metal at {T1:g} °C into 2 kg of water at {T2:g} °C and record a steady {Tm:g} °C. Then c = m<sub>2</sub>c<sub>2</sub>(T<sub>f</sub> − T<sub>2</sub>) ÷ (m<sub>1</sub>(T<sub>1</sub> − T<sub>f</sub>)) = {C2:,.0f} × {Tm-T2:g} ÷ (0.5 × {T1-Tm:g}) = **{c_unk:.0f} J/kg·K**, which points to steel or iron. The temperature rise is small, so a thermometer error of only 0.1 °C shifts the answer to {c_unk2:.0f} J/kg·K. Use a fine resolution thermometer, stir well, and transfer the hot sample quickly so it does not cool in the air.

## Common mistakes

- **Mixing kJ and J.** Specific heats here are in J/kg·K; entering 4.186 for water (the kJ value) makes water look a thousand times easier to heat than it is.
- **Using a final temperature outside the two starting values.** Without a phase change or a chemical reaction, T<sub>f</sub> must lie between T<sub>1</sub> and T<sub>2</sub>. Anything else means a typing error.
- **Ignoring steam or ice.** Metal hotter than 100 °C dropped into a little water can boil some of it off, and ice must absorb 334 kJ/kg to melt before its temperature rises.
- **Reading the thermometer too early.** Wait for the reading to peak and hold before recording it.
- **Leaving out the container.** A metal cup or beaker can absorb several percent of the heat in a small experiment.
''',
     faq_add=[('How do I find the final temperature of three or more substances?',
               'Extend the same weighted average: T_f = (Σ m·c·T) ÷ (Σ m·c). Add a term for every substance, including the container, as long as nothing melts, boils or reacts.')])

# ---------------------------------------------------------------- Exponential distribution
lam, x = 0.5, 3.0
Pl = 1 - math.exp(-lam * x)
Pg = math.exp(-lam * x)
fx = lam * math.exp(-lam * x)
mu = 1 / lam
med = math.log(2) / lam
# memoryless: already waited 2 min, chance of waiting 3 more
P_more = math.exp(-lam * 3)
# between 1 and 3 minutes
P_13 = math.exp(-lam * 1) - math.exp(-lam * 3)
pct_rows = ''
for p in (0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99):
    tq = -math.log(1 - p) / lam
    pct_rows += f"| {p*100:.0f}% | {tq:.3f} min | {tq/mu:.3f} × mean |\n"
# reliability: MTBF 50,000 h, one year 8,760 h
mtbf, tm = 50000.0, 8760.0
R1 = math.exp(-tm / mtbf)
# estimating lambda: 12 failures in 240,000 unit hours
lam_hat = 12 / 240000.0

edit('statistics/exponential-distribution', date=U, phrase='exponential distribution calculator',
     intro=("The exponential distribution describes the waiting time between random, independent events that occur at a steady average rate. "
            "This exponential distribution calculator gives P(X ≤ x), P(X > x), the density, the mean and the median from the rate λ.\n\n"
            "Queueing analysts use it for arrival gaps, reliability engineers for constant rate failures and MTBF, "
            "and physicists for radioactive decay, wherever the chance of an event does not depend on elapsed time."),
     body_add=f'''
## Reading the default result

With λ = {lam:g} per minute and x = {x:g} minutes, the calculator gives P(X ≤ {x:g}) = **{Pl*100:.2f}%**, P(X > {x:g}) = **{Pg*100:.2f}%**, f({x:g}) = **{fx:.5f}**, a mean of **{mu:g} min** and a median of **{med:.4f} min**. The median is shorter than the mean because a few very long gaps pull the mean up: half of all waits are under {med:.2f} minutes even though the average is {mu:g}.

The density value {fx:.5f} is not a probability. It is a rate per minute, and multiplying it by a short interval gives an approximate probability, for example about {fx*0.1*100:.2f}% for an arrival in the 0.1 minute window just after 3 minutes.

## Percentile waiting times at λ = {lam:g}

Solving 1 − e<sup>−λx</sup> = p gives x = −ln(1 − p) ÷ λ. This is the time by which a given share of waits have ended:

| Share of waits finished | Time x | In multiples of the mean |
|---|---|---|
{pct_rows}
Planners use the 90% or 95% row to size staffing or buffer time, because designing to the mean leaves {math.exp(-1)*100:.1f}% of waits longer than planned.

## Using it with real data

- **Interval probabilities.** The chance that the next arrival comes between 1 and 3 minutes is e<sup>−0.5</sup> − e<sup>−1.5</sup> = **{P_13*100:.2f}%**.
- **Memoryless waits.** If nobody has arrived for 2 minutes, the chance of waiting at least 3 more is still e<sup>−1.5</sup> = {P_more*100:.2f}%, the same as from the start.
- **Reliability.** A unit with an MTBF of {mtbf:,.0f} h running for one year ({tm:,.0f} h) has R = e<sup>−{tm:,.0f}/{mtbf:,.0f}</sup> = **{R1*100:.1f}%** chance of no failure.
- **Estimating λ.** From test data, λ = failures ÷ total operating time. Twelve failures in 240,000 unit hours gives λ = 5 × 10⁻⁵ per hour, an MTBF of {1/lam_hat:,.0f} h.

## Common mistakes

- **Entering the mean instead of the rate.** A mean wait of 2 minutes is λ = 0.5, not λ = 2. Swapping them turns {Pl*100:.2f}% into {(1-math.exp(-2*3))*100:.2f}%.
- **Mixing time units.** λ per hour with x in minutes gives a result 60 times off; convert both to the same unit first.
- **Treating f(x) as P(X = x).** For a continuous variable the chance of any exact value is zero.
- **Applying it to wear-out.** Bearings, belts and batteries fail more often as they age, so a constant λ understates late-life risk.
- **Assuming independence that is not there.** Arrivals that come in bursts, such as customers off the same bus, are not exponential.
''',
     faq_add=[('How do I estimate the rate λ from observed data?',
               'Divide the number of events by the total observation time. For waiting times, λ is 1 ÷ (average observed gap). With 12 failures in 240,000 unit hours, λ = 5 × 10⁻⁵ per hour and the MTBF is 20,000 hours.')])

# ---------------------------------------------------------------- Energy meter constant
C, n, t, Pr = 3200.0, 32.0, 30.0, 1.19
P = n * 3600000 / (C * t) / 1000  # kW
E = n * 3600000 / C / 1000  # Wh
err = (P - Pr) / Pr * 100
ti = 3600000 / (C * Pr * 1000)  # s
res_err = 1 / n * 100
monthly = 300.0
over = monthly * err / 100
# disc meter
Cd, nd, td = 600.0, 10.0, 60.0
Pd = nd * 3600 / (Cd * td)
# CT/PT meter
ctr, ptr = 200 / 5, 11000 / 110
mult = ctr * ptr
cnt_rows = ''
for nn in (5, 10, 20, 32, 50, 100):
    cnt_rows += f"| {nn} | {nn*ti:.1f} s | ±{100/nn:.1f}% |\n"

edit('electrical/energy-meter-constant', date=U, phrase='energy meter constant calculator',
     intro=("Every electricity meter carries a constant, printed as imp/kWh for a pulse LED or rev/kWh for a disc, that says how many pulses make one kilowatt-hour. "
            "This energy meter constant calculator turns a pulse count over time into load power, energy and meter error.\n\n"
            "Electricians, utility testers and homeowners use it to check a disputed bill, alongside an "
            "[electrical energy consumption calculation](https://www.instrumentationblog.in/electrical-energy-consumption-calculation/)."),
     body_add=f'''
## How long to count

A stopwatch count is only as good as its resolution. Starting the watch on a flash and stopping on a flash removes the half pulse at each end, but a miscount of one pulse in the default {n:.0f} still shifts the result by {res_err:.1f}%, much more than the {err:.2f}% error being measured. At {Pr:g} kW on a {C:,.0f} imp/kWh meter, each pulse takes {ti:.3f} s:

| Pulses counted | Time needed | Effect of a one pulse miscount |
|---|---|---|
{cnt_rows}
To separate a class 1 meter from a faulty one, count at least 100 pulses, or use a photo head and a meter test set that times the pulses electronically.

## Disc meters and CT operated meters

On an electromechanical meter, count the black mark on the disc instead of LED flashes. A {Cd:.0f} rev/kWh meter turning {nd:.0f} times in {td:.0f} s is carrying {nd:.0f} × 3,600 ÷ ({Cd:.0f} × {td:.0f}) = **{Pd:.2f} kW**.

For a meter fed from a {200}/5 A CT and an {11000:,}/110 V PT, the pulses measure secondary power. Multiply by {ctr:.0f} × {ptr:.0f} = **{mult:,.0f}**, so a secondary reading of {P:.2f} kW is {P*mult/1000:,.1f} MW on the primary side.

## What the default error means on a bill

The default test shows the meter reading {err:.2f}% high. On a household using {monthly:.0f} kWh a month, that is about {over:.1f} kWh of extra recorded energy each month. It is still inside the ±1% limit of a class 1 meter, so it would pass an accuracy test, although the single 30 s count is too short to prove it.

## Common mistakes

- **Counting the first flash.** Start timing on a flash and call it zero; counting it as one adds a pulse and inflates the power.
- **Using the kvarh LED.** Many static meters have separate kWh and kvarh pulse outputs. Check the label next to the LED you are watching.
- **Testing on a varying load.** Fridges, inverters and motors change power during the count; use a resistive heater or kettle.
- **Forgetting other loads.** Anything else on the circuit adds pulses. Switch off the rest of the installation, or measure the reference at the meter itself.
- **Leaving out the CT and PT ratios.** On HT and large LT services the raw pulse result is secondary power only.
''',
     faq_add=[('Why does my meter LED keep flashing with everything switched off?',
               'Something is still drawing power: standby loads, a water heater, an outside light or a neighbour fault. A healthy meter must not creep; IEC 62053-21 includes a no-load test in which the test output may give no more than one pulse in a set time with voltage applied and no current.')])

# ---------------------------------------------------------------- String frequency
L, T, mu_g, k = 648.0, 70.0, 0.4, 1
Lm, mu_s = L / 1000, mu_g / 1000
v = math.sqrt(T / mu_s)
f1 = k / (2 * Lm) * v
lam_s = 2 * Lm / k
fE4 = 329.63
T_E4 = mu_s * (2 * Lm * fE4) ** 2
cents = 1200 * math.log2(fE4 / f1)
# linear density from diameter, steel 7850 kg/m3, 0.010 in (0.254 mm)
dia = 0.254e-3
mu_d = 7850 * pi * dia ** 2 / 4
# stay cable by vibration
mc, Lc, fc = 5.0, 40.0, 2.0
Tc = 4 * mc * Lc ** 2 * fc ** 2
fret_rows = ''
for fr in (0, 1, 2, 3, 5, 7, 12):
    lf = L / 2 ** (fr / 12)
    fret_rows += f"| {fr} | {lf:.1f} mm | {L - lf:.1f} mm | {f1 * 2 ** (fr/12):.1f} Hz |\n"

edit('physics/string-frequency', date=U, phrase='string frequency calculator',
     intro=("A string fixed at both ends vibrates in standing waves that fit a whole number of half-wavelengths into its length. "
            "This string frequency calculator applies f = (n ÷ 2L) √(T ÷ μ) to find harmonic frequencies, wave speed and wavelength.\n\n"
            "Guitar and piano builders use it to choose string gauges and tensions, physics students for standing wave labs, "
            "and engineers to estimate cable and wire tension from a measured natural frequency."),
     body_add=f'''
## Tuning the default string to pitch

The default string gives f<sub>1</sub> = **{f1:.1f} Hz** with a wave speed of **{v:.1f} m/s** and a wavelength of **{lam_s:.3f} m**. That is {abs(cents):.0f} cents flat of E<sub>4</sub> at {fE4} Hz. Solving T = μ(2Lf)² for the target note gives {mu_s:g} × (2 × {Lm:g} × {fE4})² = **{T_E4:.1f} N**, about {T_E4/9.80665:.2f} kgf, so the player needs {T_E4-T:.1f} N more tension. A small change in tension is a large change in cents because frequency follows the square root.

## Linear density from the wire size

For a plain solid string, μ = ρ × π d² ÷ 4. A steel string with ρ = 7,850 kg/m³ and d = 0.254 mm (a 0.010 in gauge) gives μ = **{mu_d*1000:.3f} g/m**, matching the default 0.4 g/m. Wound strings have a core plus a wrap, so weigh a measured length or use the maker's unit weight table instead of the diameter.

## Fret positions on a {L:.0f} mm scale

Each fret shortens the vibrating length by a factor of 2<sup>1/12</sup>, raising the pitch one semitone at the same tension:

| Fret | Vibrating length | Distance from nut | Fundamental |
|---|---|---|---|
{fret_rows}
At the 12th fret the length halves and the frequency doubles to {2*f1:.1f} Hz, one octave up.

## Measuring cable tension by vibration

Rearranged as T = 4 μ L² f<sub>1</sub>², the equation turns an accelerometer reading into a tension. A stay cable with μ = {mc:g} kg/m and a free length of {Lc:g} m vibrating at {fc:g} Hz carries about 4 × {mc:g} × {Lc:g}² × {fc:g}² = **{Tc/1000:.0f} kN**. Bridge and mast inspectors use this because it needs no load cell. Sag, bending stiffness and end dampers all shift the result, so long or heavy cables need correction factors.

## Common mistakes

- **Entering μ in kg/m.** This calculator expects g/m; 0.0004 typed as kg/m is treated as 0.0004 g/m and gives a frequency 31.6 times too high.
- **Using total string length.** Only the part between the nut and the saddle vibrates.
- **Entering tension in kgf.** Convert to newtons by multiplying by 9.81.
- **Expecting harmonics to stay exact.** Thick, stiff strings run sharp in their upper partials, which is why pianos are stretch tuned.
- **Forgetting the harmonic number.** n = 2 does not give a different string; it gives the second mode of the same one at twice f<sub>1</sub>.
''',
     faq_add=[('How do I work out linear density from the string diameter?',
               'For a solid wire, μ = density × π × diameter² ÷ 4. A 0.254 mm steel wire at 7,850 kg/m³ gives about 0.398 g/m. For wound strings, weigh a known length instead.')])

# ---------------------------------------------------------------- Bolt torque
K, d, F, At = 0.2, 12.0, 30.0, 84.3
Tq = K * d / 1000 * F * 1000
s = F * 1000 / At
# same torque, lubricated
K2 = 0.15
F2 = Tq / (K2 * d / 1000) / 1000
s2 = F2 * 1000 / At
# elongation, grip 40 mm, E 200 GPa
grip, Es = 40.0, 200e3
dl = F * 1000 * grip / (Es * At)
k_rows = ''
for kk in (0.10, 0.12, 0.15, 0.18, 0.20, 0.25):
    tq = kk * d / 1000 * F * 1000
    fp = Tq / (kk * d / 1000) / 1000
    k_rows += f"| {kk:.2f} | {tq:.1f} N·m | {fp:.1f} kN | {fp*1000/At:.0f} MPa |\n"

edit('engineering/bolt-torque', date=U, phrase='bolt torque calculator',
     intro=("Tightening torque is the everyday way to set a bolt's clamp force, yet most of the torque is spent on friction under the nut and in the threads. "
            "This bolt torque calculator uses T = K × D × F, with the nut factor K standing in for that friction, and checks the bolt stress.\n\n"
            "Mechanics, maintenance fitters and design engineers use it to set wrench values for flanges, machine frames and structural joints."),
     body_add=f'''
## Where the torque goes

In a typical dry steel joint only about 10% of the applied torque stretches the bolt. Roughly 50% is lost to friction under the nut or head and about 40% to thread friction. So a modest change in surface condition changes the preload far more than a change in the wrench setting. For the default {d:g} mm bolt at {F:g} kN, the {Tq:.0f} N·m from the calculator assumes K = {K:g}. The table shows the torque needed for the same {F:g} kN at other nut factors, and the preload the same {Tq:.0f} N·m would give instead:

| Nut factor K | Torque for {F:g} kN | Preload at {Tq:.0f} N·m | Stress at {Tq:.0f} N·m |
|---|---|---|---|
{k_rows}
Oiling the threads to K = {K2:g} and keeping the dry {Tq:.0f} N·m value raises the preload to **{F2:.1f} kN** and the stress to **{s2:.0f} MPa**, {s2/580*100:.0f}% of the 580 MPa proof stress of class 8.8. With MoS₂ paste the same wrench setting would take the bolt past proof.

## How much the bolt stretches

Preload is just elastic stretch. Over a 40 mm grip the default bolt lengthens by about F × L ÷ (E × A<sub>t</sub>) = {F*1000:,.0f} × {grip:g} ÷ ({Es:,.0f} × {At:g}) = **{dl:.3f} mm** (with E = 200 GPa for steel and the tensile stress area used for the whole length, a simple estimate). Ultrasonic bolt gauges and bolt-length micrometers measure this stretch directly, which removes friction from the result.

## Tightening in practice

- Use a calibrated torque wrench; ISO 6789 allows about ±4% on most hand wrenches, much smaller than the friction scatter.
- Tighten flanges and multi-bolt joints in a star pattern in stages, for example 30%, 70% then 100% of the final torque, then a check pass.
- Apply torque to the nut where possible, since turning the head adds under-head friction you may not have allowed for.
- Add the prevailing torque of nylon insert or all-metal locknuts to the calculated value; it produces no preload.

## Common mistakes

- **Mixing mm and m in a hand calculation.** The calculator converts units, but working T = K × D × F by hand with D = 12 instead of 0.012 m gives 1,000 times the torque.
- **Using a dry torque chart for lubricated or plated bolts.** It is the most common cause of stripped threads and snapped studs.
- **Reusing torque-to-yield bolts.** Cylinder head and similar bolts are stretched past yield and must be replaced.
- **Ignoring joint relaxation.** Gaskets and paint creep, so critical joints are retorqued after the first heat cycle or a set time.
- **Fitting extensions or crowfoot adapters without correction.** An adapter that lengthens the wrench changes the torque actually delivered.
''',
     faq_add=[('How much does a bolt stretch when it is tightened?',
               'Stretch = F × L ÷ (E × A). An M12 steel bolt at 30 kN over a 40 mm grip stretches about 0.071 mm. Measuring this elongation directly is more accurate than relying on torque.')])

print('done')

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-18), slice 3: inverse-square-law, beat-frequency, speed-of-sound, time-dilation,
carnot-efficiency. Every number is computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-18'
log10 = math.log10
R = 8.314462618
c = 299792458.0

# ---------------------------------------------------------------- Inverse square law
I1, d1, d2 = 100.0, 1.0, 3.0
I2 = I1 * (d1 / d2) ** 2
dB = 20 * log10(d2 / d1)
# target distance for a dose rate limit
D1, Dlim = 100.0, 2.5  # uSv/h at 1 m, target uSv/h
d_safe = d1 * math.sqrt(D1 / Dlim)
# reference point offset error: emitting point 0.1 m behind the face
off = 0.1
r_true = ((d1 + off) / (d2 + off)) ** 2 * 100
r_naive = (d1 / d2) ** 2 * 100
isl_rows = ''
for m in (2, 4, 8, 10, 100):
    isl_rows += f"| {m} × | {100/m**2:.4g}% | {20*log10(m):.2f} dB | {100/m:.4g}% | {10*log10(m):.2f} dB |\n"

edit('physics/inverse-square-law', date=U, phrase='inverse square law calculator',
     intro=("Energy spreading from a point source covers a sphere whose area grows with the square of distance, so its intensity falls as 1/d². "
            "This inverse square law calculator scales a measured light level, sound intensity or radiation dose rate from one distance to another and gives the drop in decibels.\n\n"
            "Radiation safety officers use it to set barrier distances, lighting designers to estimate lux on a work surface, and sound engineers to predict how loud a speaker is at the audience."),
     body_add=f'''
## Finding a safe distance for a target level

Rearranging the law gives d₂ = d₁ × √(I₁ ÷ I₂). A gamma source reading {D1:g} µSv/h at {d1:g} m falls to a chosen limit of {Dlim:g} µSv/h at

- d₂ = {d1:g} × √({D1:g} ÷ {Dlim:g}) = {d1:g} × √{D1/Dlim:g} = **{d_safe:.2f} m**

So a rope barrier at about {math.ceil(d_safe*10)/10:.1f} m keeps anyone outside it below the limit, before any shielding is counted. Halving the limit only moves the barrier out by a factor of √2, which is why distance alone becomes impractical for strong sources and shielding takes over.

## How it is measured in practice

Photometry benches check the law by moving a lux meter along a rail away from a small lamp. Radiographers survey a site by taking one dose rate reading close in and scaling it outward, then confirming at the barrier. In acoustics the same idea is the familiar 6 dB drop per doubling of distance, measured outdoors or in an anechoic room where reflections do not top up the level.

Distances must be taken from the effective centre of the source, not its front face. If a lamp's emitting point sits {off*100:.0f} cm behind the face, readings at {d1:g} m and {d2:g} m from the face are really at {d1+off:.1f} m and {d2+off:.1f} m, and the measured ratio is {r_true:.2f}% instead of the {r_naive:.2f}% the formula predicts. Taking readings at several distances and fitting a line to 1/√I against distance reveals the true origin.

## Point source versus line source

A long road, pipe rack or conveyor behaves as a line source, whose intensity falls as 1/d rather than 1/d². Close to a wide area source the level hardly falls at all.

| Distance multiple | Point source remaining | Point source drop | Line source remaining | Line source drop |
|---|---|---|---|---|
{isl_rows}
## Common mistakes

- **Using 10 log for a distance ratio.** The drop is 20 log₁₀(d₂/d₁) because intensity goes with distance squared; 10 log applies to the intensity ratio itself.
- **Measuring from the housing instead of the source centre.** The offset error is largest at short distances, as the example above shows.
- **Applying it to beams.** Lasers, spotlights with reflectors and horn loudspeakers concentrate energy and fall off far more slowly in their near field.
- **Mixing distance units.** Both distances must be in the same unit; only their ratio matters, so metres against feet gives a wrong answer silently.
- **Ignoring absorption.** Air absorbs high frequency sound, and shielding, fog or water absorb light and radiation on top of the geometric spreading.
''',
     faq_add=[('How far away do I need to be to halve the intensity?',
               f'Multiply the distance by √2, about 1.414. A reading taken at 1 m halves at 1.41 m, a 3.01 dB drop. To cut intensity to one tenth, move to √10 = 3.16 times the distance.')])

# ---------------------------------------------------------------- Beat frequency
f1, f2 = 440.0, 444.0
fb = abs(f1 - f2)
Tb = 1 / fb
fa = (f1 + f2) / 2
cents = 1200 * math.log2(f2 / f1)
# two pumps on one header
n1, n2 = 1480.0, 1490.0
pb = abs(n1 - n2) / 60
# equal tempered interval beat rates from A3 = 220 Hz
A3 = 220.0
iv = [('Perfect fifth (A3 to E4)', 7, 3, 2), ('Perfect fourth (A3 to D4)', 5, 4, 3),
      ('Major third (A3 to C♯4)', 4, 5, 4), ('Major sixth (A3 to F♯4)', 9, 5, 3)]
bt_rows = ''
for name, semis, p_low, p_high in iv:
    fu = A3 * 2 ** (semis / 12)
    a, b2 = p_low * A3, p_high * fu
    bt_rows += f"| {name} | {fu:.2f} Hz | {a:.2f} Hz vs {b2:.2f} Hz | {abs(a-b2):.2f} Hz |\n"
fifth_b = abs(3 * A3 - 2 * A3 * 2 ** (7 / 12))

edit('physics/beat-frequency', date=U, phrase='beat frequency calculator',
     intro=("When two tones of slightly different frequency overlap, their combined loudness swells and fades at a rate equal to the difference between them. "
            "This beat frequency calculator gives the beats per second, the time between beats and the average pitch you actually hear.\n\n"
            "Musicians and piano tuners use beats to tune by ear, physics students use them to measure an unknown frequency, "
            "and vibration engineers use them to explain the slow throbbing of two machines running at nearly the same speed."),
     body_add=f'''
## Which side of the reference is the unknown tone?

With the default 440 Hz fork and 4 beats per second, the string could be at 444 Hz or 436 Hz. Tighten the string slightly: if the beats speed up, it was already sharp (444 Hz moving to about 445 Hz); if they slow down, it was flat. In pitch terms, the default {fb:g} Hz beat at A440 is {cents:.1f} cents, roughly one sixth of a semitone, which most listeners hear clearly as out of tune when the two notes are played together.

## Beats in piano tuning

Tuners do not only zero out beats. Equal temperament makes most intervals slightly impure, so the coincident partials of two notes beat at a known rate that the tuner counts. For a fifth the third partial of the lower note meets the second partial of the upper note; for a major third it is the fifth and fourth partials. From A3 = 220 Hz:

| Interval | Upper note | Coincident partials | Beat rate |
|---|---|---|---|
{bt_rows}
The fifth beats slowly, about {fifth_b:.2f} Hz or one beat every {1/fifth_b:.1f} s, while the major third beats several times a second. Counting these rates against a stopwatch is how a temperament octave is set before the rest of the piano is tuned to it. Real piano strings are slightly inharmonic, so the exact rates shift a little from these ideal figures.

## Beats from machines

Two pumps on a common header running at {n1:,.0f} and {n2:,.0f} rpm vibrate at {n1/60:.2f} Hz and {n2/60:.2f} Hz. Their vibrations add to a level that rises and falls {pb:.4f} times per second, a slow throb every **{1/pb:.0f} s** that can be felt in the pipework and seen on a vibration trend as a regular amplitude swing. Twin engine aircraft and ships show the same effect, and synchronisers adjust one engine until the throb stops.

## Common mistakes

- **Forgetting the two possible answers.** A beat count gives only the size of the difference, not its sign.
- **Counting for too short a time.** At 0.5 Hz one beat takes 2 s; count over at least 10 s and divide to get a reliable rate.
- **Expecting complete silence between beats.** With unequal amplitudes A₁ and A₂ the envelope only dips to |A₁ − A₂|, so the beats are shallow.
- **Confusing the envelope period with the beat period.** The cos(πΔf t) term repeats at Δf/2, but loudness peaks twice per cycle, so beats occur at Δf.
- **Using beats for widely separated tones.** Beyond roughly 15 to 20 Hz the ear hears roughness, then two notes, not counted beats.
''',
     faq_add=[('How many cents out of tune is a 4 Hz beat at A440?',
               f'About {cents:.1f} cents if the second tone is at 444 Hz, using 1200 × log₂(444 ÷ 440). The same 4 Hz beat at a lower pitch is a bigger error in cents, because cents measure the frequency ratio, not the difference.')])

# ---------------------------------------------------------------- Speed of sound
gam, M, T, f = 1.4, 28.965, 20.0, 1000.0
TK = T + 273.15
v = math.sqrt(gam * R * TK / (M * 1e-3))
lam = v / f
# ultrasonic level gauge echo
dist = 2.0
t_echo = 2 * dist / v
v60 = math.sqrt(gam * R * (60 + 273.15) / (M * 1e-3))
d60 = v60 * t_echo / 2
# biogas 60% CH4 / 40% CO2 at 35 C, cp in J/(mol K) at 25 C
x1, x2, cp1, cp2 = 0.6, 0.4, 35.69, 37.14
Mmix = x1 * 16.043 + x2 * 44.01
cpm = x1 * cp1 + x2 * cp2
gmix = cpm / (cpm - R)
vbio = math.sqrt(gmix * R * (35 + 273.15) / (Mmix * 1e-3))
lin_rows = ''
for tc in (-40, 0, 40, 100, 200, 400):
    ve = math.sqrt(gam * R * (tc + 273.15) / (M * 1e-3))
    vl = 331.3 + 0.606 * tc
    lin_rows += f"| {tc} °C | {ve:.1f} m/s | {vl:.1f} m/s | {(round((vl-ve)/ve*100, 1) or 0.0):+.1f}% |\n"
lin_rows = lin_rows.replace('-', '−').replace('+', '+')
km_s = 1000 / v

edit('physics/speed-of-sound', date=U, phrase='speed of sound calculator',
     intro=("Sound travels faster in warm gas and in light gas, because its speed depends on temperature and molar mass rather than pressure. "
            "This speed of sound calculator uses v = √(γRT/M) for air, nitrogen, CO₂, helium and other ideal gases, and gives the wavelength at any frequency.\n\n"
            "Instrument engineers apply the same temperature correction in [ultrasonic level transmitters](https://www.instrumentationblog.in/how-does-an-ultrasonic-level-transmitter-work/) "
            "and [ultrasonic flow meters](https://www.instrumentationblog.in/how-ultrasonic-flow-meter-works/), while acousticians use it to size rooms and speaker arrays."),
     body_add=f'''
## Time of flight measurement

An ultrasonic level transmitter times an echo from the liquid surface and halves the round trip: distance = v × t ÷ 2. In {T:g} °C air at {v:.1f} m/s, a surface {dist:g} m below the sensor returns its echo after {t_echo*1000:.3f} ms. If the tank headspace is really at 60 °C, sound travels at {v60:.1f} m/s, so the same {t_echo*1000:.3f} ms echo means the surface is {d60:.3f} m away. A gauge that ignored the temperature would report {dist:g} m, an error of {(d60-dist)*1000:.0f} mm. Vapour that is not air, such as solvent or CO₂ over a fermenter, changes γ and M too, which a single temperature sensor cannot correct.

## Gas mixtures

For a mixture, average the molar mass by mole fraction and work out γ from the mole-weighted molar heat capacity, not by averaging γ directly. Biogas of {x1*100:.0f}% methane and {x2*100:.0f}% CO₂ has M = {Mmix:.2f} g/mol and c<sub>p</sub> = {cpm:.2f} J/(mol·K), so γ = {cpm:.2f} ÷ ({cpm:.2f} − 8.314) = {gmix:.3f}. At 35 °C sound travels at **{vbio:.0f} m/s**, which is why ultrasonic gas meters and biogas analysers can infer methane content from sound speed.

## Linear rule of thumb against the exact formula

The common approximation v ≈ 331.3 + 0.606 T (T in °C) is fine near room temperature but drifts in hot gas:

| Temperature | Exact (dry air) | Linear rule | Error |
|---|---|---|---|
{lin_rows}
## Common mistakes

- **Entering molar mass in kg/mol into a g/mol field.** 0.028965 instead of 28.965 gives a speed about 32 times too high.
- **Using Celsius in the formula by hand.** T must be in kelvin; the calculator converts it, but a spreadsheet will not.
- **Averaging γ by mole fraction.** It is the heat capacities that average, as in the biogas example above.
- **Expecting frequency to change the speed.** In ordinary gases sound is non-dispersive; frequency changes only the wavelength.
- **Using the gas formula for liquids or solids.** Those depend on bulk or elastic modulus and density instead.
''',
     faq_add=[('How do I estimate the distance to a lightning strike?',
               f'Count the seconds between the flash and the thunder. At 20 °C sound covers 1 km in {km_s:.1f} s, so divide the count by 3 for kilometres, or by 5 for miles.')])

# ---------------------------------------------------------------- Time dilation
t0, b = 1.0, 0.90
g = 1 / math.sqrt(1 - b ** 2)
t = g * t0
dt = t - t0
vv = b * c
# muons
tau, bm = 2.197e-6, 0.998
gm = 1 / math.sqrt(1 - bm ** 2)
L0 = bm * c * tau
Lg = gm * L0
# GPS velocity term
vgps = 3874.0
gps_us = (vgps / c) ** 2 / 2 * 86400 * 1e6
# ISS
viss = 7660.0
half = 182.5 * 86400
iss_sr = (viss / c) ** 2 / 2 * half * 1e3
iss_gr = 9.81 * 400e3 / c ** 2 * half * 1e3
yr_s = 365.25 * 86400
ev = [('Passenger jet', 250), ('ISS in orbit', 7660), ('GPS satellite', 3874), ('Earth around the Sun', 29780), ('Parker Solar Probe at perihelion', 191700)]
ev_rows = ''
for name, sp in ev:
    lag = 0.5 * (sp / c) ** 2 * yr_s
    if lag < 1e-6:
        s = f'{lag*1e9:.2f} ns'
    elif lag < 1e-3:
        s = f'{lag*1e6:.2f} µs'
    elif lag < 1:
        s = f'{lag*1e3:.2f} ms'
    else:
        s = f'{lag:.2f} s'
    ev_rows += f"| {name} | {sp:,} m/s | {(sp/c)**2/2:.3e} | {s} |\n"
ev_rows = ev_rows.replace('e-', 'e−')

edit('physics/time-dilation', date=U, phrase='time dilation calculator',
     intro=("Special relativity predicts that a moving clock ticks slower than one at rest, by the Lorentz factor γ = 1/√(1 − v²/c²). "
            "This time dilation calculator turns the proper time on board into the time a stationary observer measures, and gives γ, the extra time and the speed.\n\n"
            "Physics students use it to check textbook problems, science fiction writers to plan believable journeys, and anyone curious about the twin paradox or GPS corrections can see the numbers directly."),
     body_add=f'''
## Default result in full

With the default inputs (t₀ = {t0:g} year, v = {b*100:g}% of c), the calculator returns γ = **{g:.4f}**, a stationary observer time of **{t:.4f} years**, an extra {dt:.4f} years and a speed of **{vv:,.0f} m/s** ({vv/1000:,.0f} km/s).

## Evidence from muons

Cosmic ray muons are made about 10 to 15 km up and live only {tau*1e6:.3f} µs at rest. Moving at {bm*100:g}% of c, a muon without time dilation would travel just {L0:.0f} m on average before decaying. With γ = {gm:.2f}, its lifetime in the Earth frame stretches to {gm*tau*1e6:.1f} µs and the mean path to **{Lg/1000:.1f} km**, so a large fraction reach detectors at sea level, exactly as measured. In the muon's own frame the same result appears as the atmosphere being length contracted by γ.

## Atomic clocks and satellites

At everyday speeds γ − 1 is tiny, and it is well approximated by v²/(2c²). Precise atomic clocks still detect it: flights around the world in 1971 (the Hafele and Keating experiment) found time shifts of tens to hundreds of nanoseconds, and GPS must allow for it.

| Moving clock | Speed | γ − 1 | Clock falls behind per year |
|---|---|---|---|
{ev_rows}
A GPS satellite at {vgps:,.0f} m/s loses about **{gps_us:.1f} µs per day** from its speed. General relativity makes it gain about 45.7 µs per day from the weaker gravity at its altitude, so the net correction built into the satellite clocks is roughly 38 µs per day, which would otherwise grow into kilometres of position error within a day.

## Common mistakes

- **Swapping proper and observed time.** t₀ is measured by the clock that is present at both events, the moving one; the longer time belongs to the observer who sees it move.
- **Entering speed as a fraction in a percent field.** Type 90 for 90%, not 0.9.
- **Losing precision near c.** At 99.9999% of c, 1 − b² is about 2 × 10⁻⁶; rounding b early in a spreadsheet changes γ noticeably.
- **Treating the twin paradox as symmetric.** The travelling twin changes frame on turning round, which is why only that twin ends up younger.
- **Ignoring gravity for orbiting clocks.** For GPS the gravitational effect is larger than the speed effect and has the opposite sign.
''',
     faq_add=[('How much younger does an astronaut on the ISS get?',
               f'Over a 6 month stay at {viss:,.0f} m/s, speed alone slows the astronaut\'s clock by about {iss_sr:.1f} ms. Weaker gravity at 400 km speeds it up by about {iss_gr:.1f} ms, so the net result is roughly {iss_sr-iss_gr:.1f} ms younger than people on the ground.')])

# ---------------------------------------------------------------- Carnot efficiency
Th, Tc, Qh = 500.0, 30.0, 100.0
ThK, TcK = Th + 273.15, Tc + 273.15
eta = 1 - TcK / ThK
W = eta * Qh
COPr = TcK / (ThK - TcK)
COPh = ThK / (ThK - TcK)
ca = 1 - math.sqrt(TcK / ThK)
Qc = Qh - W
# heat pump with exchanger approach temperatures
hp_out, hp_in, appr, cop_meas = 35.0, 0.0, 5.0, 3.5
cop_air = (hp_out + 273.15) / (hp_out - hp_in)
cop_ref = (hp_out + appr + 273.15) / ((hp_out + appr) - (hp_in - appr))
sys_rows = ''
for name, h, cl, act in [('Supercritical steam plant', 600, 30, 45), ('Subcritical steam plant', 540, 35, 38),
                         ('Geothermal binary plant', 150, 25, 12), ('Combined cycle gas plant', 1400, 25, 60)]:
    ec = 1 - (cl + 273.15) / (h + 273.15)
    sys_rows += f"| {name} | {h} °C / {cl} °C | {ec*100:.1f}% | about {act}% | {act/(ec*100)*100:.0f}% |\n"

edit('physics/carnot-efficiency', date=U, phrase='Carnot efficiency calculator',
     intro=("No heat engine working between two temperatures can beat an ideal reversible Carnot cycle, η = 1 − T_c/T_h, and no refrigerator or heat pump can beat the Carnot COP. "
            "This Carnot efficiency calculator gives all three limits and the maximum work from a heat input.\n\n"
            "Power plant, HVAC and refrigeration engineers use it as the benchmark for judging real machines, such as "
            "[chiller capacity and COP](https://www.instrumentationblog.in/calculate-industrial-chiller-capacity/), and students use it to check thermodynamics problems."),
     body_add=f'''
## Where the rest of the heat goes

In the default case only {W:.2f} kW of the {Qh:g} kW can become work, even in an ideal engine, so at least **{Qc:.2f} kW** must be rejected to the {Tc:g} °C sink. That rejected heat is why power stations need cooling towers or river water, and why the cold side matters as much as the hot side: each degree lower at the sink raises the limit.

The Carnot engine produces its maximum efficiency only at zero speed, because heat must flow across vanishing temperature differences. An engine run for maximum power with finite heat exchangers has the Curzon and Ahlborn efficiency, 1 − √(T<sub>c</sub>/T<sub>h</sub>), which for the defaults is **{ca*100:.1f}%**. This lower figure is much closer to what real plants achieve.

## Real plants against the Carnot limit

The ratio of actual to Carnot efficiency, called the second law efficiency, shows how much room for improvement is left:

| System | Hot / cold temperature | Carnot limit | Typical actual | Fraction of Carnot |
|---|---|---|---|---|
{sys_rows}
## Heat pumps: use refrigerant temperatures

A heat pump delivering {hp_out:g} °C water from {hp_in:g} °C outdoor air has an ideal COP of {cop_air:.2f} based on those two temperatures. The refrigerant, however, must evaporate below the air and condense above the water. With {appr:g} K approach on each exchanger, the cycle really works between −{appr-hp_in:g} °C and {hp_out+appr:g} °C, and the Carnot COP falls to **{cop_ref:.2f}**. A unit measured at COP {cop_meas:g} is therefore achieving {cop_meas/cop_ref*100:.0f}% of its realistic limit, not {cop_meas/cop_air*100:.0f}%.

## Common mistakes

- **Entering Celsius into the ratio by hand.** 30 ÷ 500 gives 94% instead of the correct {eta*100:.2f}%; only kelvin ratios are meaningful.
- **Treating the limit as a target.** Real engines reach about half to three quarters of it, and well below at small scale.
- **Using air and water temperatures for a heat pump.** The refrigerant temperatures set the limit, as the example above shows.
- **Mixing up COP and efficiency.** A COP above 1 is normal because a heat pump moves heat rather than creating it.
- **Forgetting that COP<sub>HP</sub> = COP<sub>ref</sub> + 1.** Heating output includes the compressor work as well as the heat lifted.
''',
     faq_add=[('Why is the heat pump COP always one more than the refrigerator COP?',
               f'A heat pump delivers the heat taken from the cold side plus the compressor work, so Q_h = Q_c + W and Q_h/W = Q_c/W + 1. For the default temperatures that is {COPh:.3f} = {COPr:.3f} + 1.')])

print('done')

# ======================================================================= SECTION _expand_c4.py
"""Part C expand (2026-11-18), slice 4: area-moment-of-inertia, capacitor-bank-kvar, mass-energy-equivalence,
load-factor, magnetic-field. All numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-18'
pi = math.pi
c = 299792458.0
mu0 = 1.25663706212e-6

# ---------------------------------------------------------------- Area moment of inertia
b, h, Do, Di = 100.0, 200.0, 60.0, 0.0
Ir = b * h ** 3 / 12 / 1e4          # cm^4
Zr = b * h ** 2 / 6 / 1e3           # cm^3
Ic = pi * (Do ** 4 - Di ** 4) / 64 / 1e4
Zc = pi * (Do ** 4 - Di ** 4) / (32 * Do) / 1e3
Ir_flat = h * b ** 3 / 12 / 1e4
Zr_flat = h * b ** 2 / 6 / 1e3
# beam check: simply supported 3 m span, 2 kN/m UDL, C24 timber E = 11,000 MPa
L, w, E_t = 3000.0, 2.0, 11000.0     # mm, N/mm, MPa
M = w * L ** 2 / 8                   # N mm
sig = M / (Zr * 1e3)
dfl = 5 * w * L ** 4 / (384 * E_t * Ir * 1e4)
sig_flat = M / (Zr_flat * 1e3)
dfl_flat = 5 * w * L ** 4 / (384 * E_t * Ir_flat * 1e4)
tube_rows = ''
for di in (0, 20, 30, 40, 50):
    A = pi * (Do ** 2 - di ** 2) / 4
    I_ = pi * (Do ** 4 - di ** 4) / 64 / 1e4
    Z_ = pi * (Do ** 4 - di ** 4) / (32 * Do) / 1e3
    tube_rows += f"| {Do:g} × {di:g} mm | {A:,.0f} mm² | {I_:.2f} cm⁴ | {Z_:.2f} cm³ | {I_*1e4/A:,.0f} mm² |\n"
Zpl_r = b * h ** 2 / 4 / 1e3
Zpl_c = Do ** 3 / 6 / 1e3
J_c = 2 * Ic
in4 = 2.54 ** 4

edit('engineering/area-moment-of-inertia', date=U, phrase='area moment of inertia calculator',
     intro=("The second moment of area I measures how a cross-section's material is spread about its bending axis, which sets how stiff a beam is. "
            "This area moment of inertia calculator returns I and the elastic section modulus Z for a rectangle and a solid or hollow round section, in cm⁴ and cm³.\n\n"
            "Structural and mechanical engineers, fabricators and students use it to size joists, shafts, brackets and pipe supports "
            "before checking stress and deflection."),
     body_add=f'''
## From I and Z to a real beam check

Take the default {b:g} × {h:g} mm section as a C24 timber beam (E = {E_t:,.0f} MPa) spanning {L/1000:g} m, simply supported, with a uniform load of {w:g} kN/m:

- Maximum moment M = wL² ÷ 8 = {w:g} × {L/1000:g}² ÷ 8 = **{M/1e6:.2f} kN·m**
- Bending stress σ = M ÷ Z = {M:,.0f} N·mm ÷ {Zr*1e3:,.0f} mm³ = **{sig:.2f} MPa**
- Midspan deflection = 5wL⁴ ÷ (384 E I) = **{dfl:.2f} mm**, which is span ÷ {L/dfl:,.0f}

Laid flat, the same plank has I = {Ir_flat:,.1f} cm⁴ and Z = {Zr_flat:,.1f} cm³. The stress doubles to {sig_flat:.2f} MPa and the deflection quadruples to {dfl_flat:.2f} mm, because Z follows h² and I follows h³.

## Why hollow sections are efficient

Boring out the centre of the default 60 mm bar removes material that sits close to the neutral axis and contributes little to I:

| Section (D × d) | Area | I | Z | I per unit area |
|---|---|---|---|---|
{tube_rows}
A 60 × 40 mm tube keeps about {(1-(40/60)**4)*100:.0f}% of the solid bar's stiffness with only {(1-(40/60)**2)*100:.0f}% of its weight. The limit is wall buckling: very thin walls fail locally before the section reaches its bending capacity.

## Elastic and plastic section modulus

Z here is the elastic modulus, the value that gives the stress when the outer fibre first reaches yield. Once the whole section yields, the plastic modulus applies: b h² ÷ 4 = {Zpl_r:,.1f} cm³ for the default rectangle (1.5 times Z) and D³ ÷ 6 = {Zpl_c:.2f} cm³ for the 60 mm bar (1.70 times Z). Eurocode tables list these as W<sub>el</sub> and W<sub>pl</sub>, while AISC tables use S for elastic and Z for plastic, so always check which one a table means.

## Common mistakes

- **Swapping b and h.** h is the depth in the direction of the load. Getting it backwards on the default section understates I by a factor of four.
- **Mixing mm⁴ and cm⁴.** 1 cm⁴ = 10,000 mm⁴, so a 66,666,667 mm⁴ result is {Ir:,.1f} cm⁴, not 6.7 million.
- **Using radius in a diameter formula.** π D⁴ ÷ 64 and π r⁴ ÷ 4 are the same thing; mixing them gives an error of 16 times.
- **Using I for torsion of a rectangle.** The polar moment J = 2I holds only for round sections. Rectangles and open shapes need a separate torsion constant.
- **Adding parts without the parallel-axis term.** Each flange of a built-up section must include A d² about the common neutral axis, which usually dominates the total.
''',
     faq_add=[('What is the polar moment of inertia of a round shaft?',
               f'For a circular section J = π D⁴ ÷ 32, exactly twice the bending I. The default 60 mm solid bar has J = {J_c:.2f} cm⁴, the value used for shaft torsion stress and twist.'),
              ('How do I convert cm⁴ to in⁴?',
               f'1 in⁴ = 2.54⁴ = {in4:.3f} cm⁴. The default 100 × 200 mm rectangle with I = {Ir:,.1f} cm⁴ is about {Ir/in4:,.1f} in⁴.')])

# ---------------------------------------------------------------- Capacitor bank kVAr
Q, V, f, k = 50.0, 415.0, 50.0, 3
w_ = 2 * pi * f
C = Q * 1000 / (k * w_ * V ** 2)          # F
Il = Q * 1000 / (math.sqrt(3) * V)
Xc = 1 / (w_ * C)
# effect on a 200 kW, 0.80 PF load
P = 200.0
pf1 = 0.80
Q1 = P * math.tan(math.acos(pf1))
Q2 = Q1 - Q
S1, S2 = P / pf1, math.hypot(P, Q2)
pf2 = P / S2
I1, I2 = S1 * 1000 / (math.sqrt(3) * V), S2 * 1000 / (math.sqrt(3) * V)
# meter reading across two terminals of a delta unit
Cpair = 1.5 * C
# discharge resistor: 75 V within 3 min (IEC 60831-1)
V0 = math.sqrt(2) * V
Rdis = 180 / (C * math.log(V0 / 75))
# 7% detuning
fr = f / math.sqrt(0.07)
Vcap = V / (1 - 0.07)
v_rows = ''
for vv, ff in ((380, 50), (400, 50), (415, 50), (440, 50), (480, 60), (600, 60), (690, 50)):
    cc = Q * 1000 / (3 * 2 * pi * ff * vv ** 2) * 1e6
    ii = Q * 1000 / (math.sqrt(3) * vv)
    v_rows += f"| {vv} V, {ff} Hz | {cc:,.1f} µF | {ii:.1f} A |\n"

edit('electrical/capacitor-bank-kvar', date=U, phrase='capacitor bank kVAr calculator',
     intro=("Power factor correction capacitors are rated in kVAr, but the capacitance in each phase is what you measure and replace. "
            "This capacitor bank kVAr calculator converts between kVAr and µF for delta and star banks and gives the line current. "
            "See [how to calculate capacitor bank kVAr](https://www.instrumentationblog.in/how-to-calculate-capacitor-bank-kvar-formula/).\n\n"
            "Electrical engineers and maintenance staff use it to order replacement units, test banks and size feeders. "
            "Read about [capacitor bank sizing for power factor correction](https://www.instrumentationblog.in/capacitor-bank-sizing-power-factor-correction/)."),
     body_add=f'''
## What the default bank does to a real load

Connect the default {Q:g} kVAr, {V:g} V delta bank to a {P:g} kW load running at {pf1:.2f} power factor:

- Load reactive power = {P:g} × tan(cos⁻¹ {pf1:.2f}) = **{Q1:.1f} kVAr**
- After correction: {Q1:.1f} − {Q:g} = {Q2:.1f} kVAr, so apparent power falls from {S1:.1f} kVA to **{S2:.1f} kVA**
- Power factor rises from {pf1:.2f} to **{pf2:.3f}**
- Supply current drops from {I1:.1f} A to **{I2:.1f} A**, freeing about {I1-I2:.0f} A of cable and transformer capacity

## Testing a bank in the field

A healthy bank draws close to its calculated current, so a clamp meter reading near {Il:.1f} A on each line at {V:g} V is the quickest check. Readings that are unequal by more than about 10% point to a failed element in one phase.

With the bank isolated and discharged, a capacitance meter across two terminals of a three-terminal delta unit does not read C. It reads one capacitor in parallel with the other two in series, so the expected value is 1.5 × {C*1e6:.1f} = **{Cpair*1e6:.0f} µF** for each pair. Compare all three pairs; they should agree within a few percent.

IEC 60831-1 requires each unit to discharge to 75 V or less within 3 minutes. From a peak of {V0:.0f} V, that needs a discharge resistance no greater than 180 ÷ ({C*1e6:.0f} µF × ln({V0:.0f} ÷ 75)) = **{Rdis/1000:,.0f} kΩ** per phase. Always wait the full time and short the terminals before touching them.

## Capacitance for a 50 kVAr delta bank at other supplies

| Supply | µF per phase | Line current |
|---|---|---|
{v_rows}
On 60 Hz systems the same kVAr needs {50/60*100:.0f}% of the capacitance it would need at 50 Hz, so never fit a 50 Hz replacement value into a 60 Hz bank without recalculating.

## Detuned banks

Where drives create harmonics, each step gets a series reactor. A 7% reactor tunes the circuit to {f:g} ÷ √0.07 = **{fr:.0f} Hz**, below the 5th harmonic, but it lifts the voltage across the capacitor to {V:g} ÷ (1 − 0.07) = {Vcap:.0f} V. That is why detuned banks on {V:g} V systems use capacitors rated 480 V or more.

## Common mistakes

- **Using the star formula for a delta bank.** It gives three times the capacitance needed, and the bank would deliver three times the kVAr.
- **Entering phase voltage instead of line voltage.** The formulas take V<sub>L</sub>; using 240 V instead of {V:g} V inflates the result by a factor of three.
- **Measuring a delta unit pair and calling it C.** The meter shows 1.5 C, so a good {C*1e6:.0f} µF phase can look like an oversized one.
- **Over-compensating a motor at its terminals.** Fixed capacitors switched with a motor should not exceed about 90% of its no-load reactive power, or the motor can self-excite after disconnection.
- **Ignoring the rated voltage on the nameplate.** A unit marked 440 V gives less than its nameplate kVAr on {V:g} V, so read the output at the actual supply.
''',
     faq_add=[('What should a capacitance meter read across two terminals of a delta capacitor?',
               f'1.5 times the capacitance per phase, because one capacitor sits in parallel with the other two in series. For the default 50 kVAr, 415 V, 50 Hz bank that is about {Cpair*1e6:.0f} µF.'),
              ('How quickly must a power factor capacitor discharge?',
               f'IEC 60831-1 requires 75 V or less within 3 minutes of disconnection. For 308 µF charged to the {V0:.0f} V peak of a 415 V supply, that needs a discharge resistor of about {Rdis/1000:,.0f} kΩ or less.')])

# ---------------------------------------------------------------- Mass-energy equivalence
m = 0.001
E = m * c ** 2
E_kwh = E / 3.6e6
E_tj = E / 1e12
E_kt = E / 4.184e12
MeV = 1.602176634e-13
uMeV = 931.49410242
mp, mn, md = 1.007276467, 1.008664916, 2.013553212
Bd = (mp + mn - md) * uMeV
mD, mT, mHe, mN = 2.014101778, 3.016049281, 4.002603254, 1.008664916
dDT = mD + mT - mHe - mN
Q_DT = dDT * uMeV
fr_DT = dDT / (mD + mT) * 100
fr_fis = 200 / (235.0439 * uMeV) * 100
Lsun = 3.828e26
msun = Lsun / c ** 2
# 1 GW(e) reactor, 33% efficient, one year
Eth = 1e9 * 8760 * 3600 / 0.33
m_reac = Eth / c ** 2
bat = 100 * 3.6e6 / c ** 2
ratio = 8.2e13 / 46e6
m_rows = ''
for lab, mm in (('1 µg', 1e-9), ('1 mg', 1e-6), ('1 g', 1e-3), ('1 kg', 1.0), ('1 tonne', 1000.0)):
    e = mm * c ** 2
    m_rows += f"| {lab} | {e:.4e} J | {e/3.6e6:,.4g} kWh | {e/4.184e12:.4g} kt |\n"
m_rows = m_rows.replace('e+', ' × 10^').replace('e-', ' × 10^−')


def fixexp(s):
    # turn "10^−09" into 10⁻⁹ and "10^13" into 10¹³
    import re
    def r(mo):
        sign, digits = mo.group(1), mo.group(2).lstrip('0') or '0'
        tbl = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
        return '10' + ('⁻' if sign else '') + digits.translate(tbl)
    return re.sub(r'10\^(−?)(\d+)', r, s)


m_rows = fixexp(m_rows)


def sci(x, d):
    return fixexp(f'{x:.{d}e}'.replace('e+', ' × 10^').replace('e-', ' × 10^−'))



edit('physics/mass-energy-equivalence', date=U, phrase='E = mc² calculator',
     intro=("Einstein's E = mc² states that mass and energy are equivalent, linked by the square of the speed of light, 299,792,458 m/s. "
            "This E = mc² calculator turns a mass into its rest energy in joules, kilowatt-hours and TNT equivalent, or finds the mass behind an energy.\n\n"
            "Physics students, nuclear engineers and science writers use it to compare chemical, fission and fusion energy "
            "and to check textbook binding energy figures."),
     body_add=f'''
## Rest energy of everyday masses

| Mass | Energy | Energy | TNT equivalent |
|---|---|---|---|
{m_rows}
The 1 g row is the calculator's default: {sci(E,4)} J, or {E_kwh:,.0f} kWh, {E_tj:.2f} TJ and {E_kt:.2f} kilotonnes of TNT.

## Where mass really turns into energy

No practical process converts a whole gram. Real reactions convert only the mass defect, the difference between the masses before and after:

- **Deuteron binding.** A proton ({mp} u) and a neutron ({mn} u) together outweigh a deuteron ({md} u) by {mp+mn-md:.9f} u. Multiplying by {uMeV:.3f} MeV/u gives **{Bd:.3f} MeV**, the energy of the gamma ray released when the two fuse.
- **Fusion of deuterium and tritium.** D + T → ⁴He + n loses {dDT:.6f} u, releasing **{Q_DT:.1f} MeV**, about {fr_DT:.2f}% of the fuel mass.
- **Fission of U-235.** About 200 MeV per split nucleus is {fr_fis:.3f}% of its mass.
- **The Sun.** Radiating {sci(Lsun,3)} W, it loses L ÷ c² = **{sci(msun,2)} kg** of mass every second.

A 1 GW electric reactor at 33% efficiency releases {sci(Eth,3)} J of heat in a year, which corresponds to only **{m_reac:.2f} kg** of mass, spread across tonnes of fuel. Per kilogram, fission releases about {ratio/1e6:.1f} million times more energy than burning petrol.

## Converting between units

Nuclear physics works in MeV and atomic mass units rather than joules. 1 MeV = {sci(MeV,9)} J, and 1 u × c² = {uMeV:.3f} MeV. To use the calculator with particle data, convert the mass in u to kilograms (1 u = 1.66054 × 10⁻²⁷ kg), or convert the result in joules back to MeV by dividing by {sci(MeV,4)}.

## Common mistakes

- **Leaving mass in grams when working by hand.** E = mc² needs kilograms for joules; 1 g written as 1 gives a result 1,000 times too large. The calculator converts units for you.
- **Confusing rest energy with kinetic energy.** mc² is the energy of a body at rest. Motion adds (γ − 1) mc², which at everyday speeds is just ½mv².
- **Assuming fission converts all the fuel.** Only about {fr_fis:.2f}% of a U-235 nucleus becomes energy; the rest remains as fission products.
- **Rounding c to 3 × 10⁸ m/s for precise work.** It overstates c² by {((3e8/c)**2-1)*100:.2f}%, enough to spoil MeV level comparisons.
- **Mixing tonnes and kilotonnes of TNT.** 1 g of mass is {E_kt:.2f} kilotonnes, which is {E_kt*1000:,.0f} tonnes.
''',
     faq_add=[('Is a charged battery heavier than a flat one?',
               f'Yes, but immeasurably. Storing 100 kWh adds E ÷ c² = {sci(bat,2)} kg, about {bat*1e9:.0f} micrograms, far below what any scale can detect on a battery pack.'),
              ('How much mass does the Sun lose each second?',
               f'The Sun radiates about {sci(Lsun,3)} W, so it loses {sci(msun,2)} kg, roughly {msun/1e9:.1f} million tonnes, every second through fusion in its core.')])

# ---------------------------------------------------------------- Load factor
E_l, tp, MD, Pc = 216000.0, 720.0, 500.0, 800.0
Pa = E_l / tp
LF = Pa / MD
DF = MD / Pc
dem, en = 10.0, 0.08   # illustrative tariff: 10 per kW per month, 0.08 per kWh
cost = MD * dem + E_l * en
uc = cost / E_l
t_rows = ''
for lf in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9):
    e = MD * tp * lf
    cc = MD * dem + e * en
    t_rows += f"| {lf*100:.0f}% | {e:,.0f} kWh | {cc:,.0f} | {cc/e:.4f} |\n"
LsF = 0.3 * LF + 0.7 * LF ** 2
MD2 = 400.0
LF2 = Pa / MD2
cost2 = MD2 * dem + E_l * en
LF31 = E_l / (MD * 744)
pf_b = 0.9
MDkva = MD / pf_b
CF_gen = 0.30

edit('electrical/load-factor', date=U, phrase='load factor calculator',
     intro=("Load factor is the average load over a billing period divided by the maximum demand, so it shows how steadily a site uses its electrical capacity. "
            "This load factor calculator finds average load, load factor and demand factor from bill kWh and kW figures. "
            "See [maximum demand calculation with diversity](https://www.instrumentationblog.in/maximum-demand-calculation-diversity/).\n\n"
            "Energy managers, plant engineers and consultants use it to understand demand charges, plan peak shaving and size transformers."),
     body_add=f'''
## How load factor sets the average price per kWh

On a two-part tariff the demand charge is fixed by the peak, so the more kWh that peak is spread over, the cheaper each unit becomes. With an illustrative tariff of {dem:g} per kW of maximum demand per month plus {en:g} per kWh, the default month costs {MD:g} × {dem:g} + {E_l:,.0f} × {en:g} = **{cost:,.0f}**, an average of **{uc:.4f} per kWh**.

| Load factor | Energy at 500 kW MD | Monthly bill | Average per kWh |
|---|---|---|---|
{t_rows}
Cutting the peak from {MD:g} kW to {MD2:g} kW with the same energy lifts the load factor from {LF*100:.0f}% to **{LF2*100:.0f}%** and saves {cost-cost2:,.0f} a month, without using a single kWh less.

## Reading the figures from a bill or meter

The kWh figure is the difference between the opening and closing energy register readings, multiplied by the meter constant or CT ratio where the bill does not do it. The maximum demand is the highest average power over one integration window, commonly 15 or 30 minutes, so a 2 second motor inrush barely moves it. If interval data is available, the peak window and the time it occurred show which loads to reschedule.

Many tariffs bill demand in kVA. At {pf_b:.1f} power factor the default {MD:g} kW peak is {MDkva:.0f} kVA, and a kVA based load factor would be {Pa:.0f} ÷ {MDkva:.0f} = {Pa/MDkva*100:.0f}% unless the kWh are also converted. Keep both quantities on the same basis.

## Load factor and losses

Copper losses in cables and transformers follow the square of current, so they depend on the shape of the load curve, not just the average. Distribution planners often estimate the loss factor with the empirical relation 0.3 LF + 0.7 LF². At {LF*100:.0f}% load factor that gives {LsF:.3f}: average losses are {LsF*100:.1f}% of the losses at maximum demand.

## Common mistakes

- **Using the wrong number of hours.** A 31 day month has 744 h; the same bill over 744 h gives {LF31*100:.2f}%, not {LF*100:.0f}%.
- **Taking an instantaneous peak as maximum demand.** Utilities bill the highest integrated window, which is lower than a spot reading from a clamp meter.
- **Confusing demand factor with diversity factor.** Demand factor is MD ÷ connected load (below 1); diversity factor is the sum of individual maximum demands ÷ the combined maximum (above 1).
- **Mixing kVA demand with kWh energy.** The result understates load factor by the power factor.
- **Averaging monthly load factors for a year.** The annual figure uses the single highest peak of the year, so it is normally lower than the average of the twelve monthly values.
''',
     faq_add=[('What is the difference between load factor and capacity factor?',
               f'Load factor compares average load with the actual peak demand. Capacity factor compares average output with the rated capacity of a generator or plant. A solar farm may run at a {CF_gen*100:.0f}% capacity factor simply because the sun sets, while load factor describes how flat a consumer demand profile is.'),
              ('What is loss factor?',
               f'Loss factor is the average power loss divided by the loss at peak load. It is commonly estimated as 0.3 LF + 0.7 LF², so a {LF*100:.0f}% load factor gives a loss factor of about {LsF:.2f}.')])

# ---------------------------------------------------------------- Magnetic field
I, r, N, Ls, mur = 10.0, 0.010, 500, 0.10, 1.0
Bw = mu0 * I / (2 * pi * r) * 1000
Bs = mu0 * mur * N * I / Ls * 1000
H = N * I / Ls
s_rows = ''
for D in (0.01, 0.02, 0.03, 0.05, 0.10):
    fac = Ls / math.sqrt(Ls ** 2 + D ** 2)
    s_rows += f"| {D*100:g} cm | {Ls/D:.2f} | {fac*100:.1f}% | {Bs*fac:.2f} mT | {Bs*Ls/(2*math.sqrt(Ls**2+(D/2)**2)):.2f} mT |\n"
fac2 = Ls / math.sqrt(Ls ** 2 + 0.02 ** 2)
ued = (Bs / 1000) ** 2 / (2 * mu0)
earth = 0.050
r_ref100 = mu0 * 100 / (2 * pi * 200e-6)
B_iron = Bs * 1000 / 1000  # T with mur 1000

edit('physics/magnetic-field', date=U, phrase='magnetic field calculator',
     intro=("An electric current produces a magnetic field that circles a straight wire and becomes strong and nearly uniform inside a coil. "
            "This magnetic field calculator gives the flux density around a long conductor and inside a solenoid, plus the field strength H.\n\n"
            "Students, coil designers and instrument technicians use it to size [solenoid valve](https://www.instrumentationblog.in/solenoid-valve-working-principle/) coils, "
            "check stray fields near busbars and set the range of a [Hall-effect sensor](https://www.instrumentationblog.in/how-a-hall-effect-sensor-works/)."),
     body_add=f'''
## Short coils: correcting the long solenoid formula

B = μ<sub>0</sub> N I ÷ L assumes the coil is much longer than it is wide. At the centre of a real coil of diameter D the field is reduced by the factor L ÷ √(L² + D²). For the default {N}-turn, {Ls*100:g} cm coil carrying {I:g} A:

| Coil diameter | L ÷ D | Centre factor | B at centre | B at each end |
|---|---|---|---|---|
{s_rows}
A slim 2 cm coil reaches {fac2*100:.1f}% of the ideal {Bs:.2f} mT, but a coil as wide as it is long gives only about 71%. For short coils, use the corrected value or measure it.

## Measuring the field

A Hall-effect gaussmeter is the usual instrument: its probe gives a voltage proportional to the field component perpendicular to the sensor face, so it must be held square to the field lines. A search coil connected to an integrating meter measures AC fields. As a reference, the Earth contributes about {earth*1000:.0f} µT, which is {earth/Bw*100:.0f}% of the default wire reading of {Bw*1000:.0f} µT and must be subtracted when measuring weak DC fields.

## Energy stored in the field

The energy density of a magnetic field is B² ÷ (2μ<sub>0</sub>). Inside the default air-core solenoid at {Bs:.2f} mT that is **{ued:,.0f} J/m³**. The same expression, read as a pressure, is the force per unit area that pulls a solenoid plunger into the coil, which is why doubling the current gives about four times the pull.

## Exposure reference level

The ICNIRP 2010 guidelines set a general public reference level of 200 µT for 50 Hz fields. The default case, {I:g} A at {r*1000:g} mm, sits right at that value, but the field falls with distance: 100 A drops to 200 µT at {r_ref100*1000:.0f} mm. In a cable the live and neutral fields largely cancel, so real readings are far lower.

## Common mistakes

- **Measuring r from the conductor surface.** The formula uses the distance to the centre; for a 4 mm² wire at 10 mm from the surface, r is about {(0.010+0.00113)*1000:.1f} mm.
- **Applying the long solenoid formula to a short coil.** It overstates the centre field, as the table above shows.
- **Trusting a large μr.** μr = 1,000 on the default coil predicts {B_iron:.1f} T, but iron saturates near 1.5 to 2 T and an open core gives far less gain than its material μr.
- **Using total wire length for L.** L is the length of the winding along the axis, not the length of copper in the coil.
- **Adding fields from several conductors as plain numbers.** Fields are vectors; opposite currents subtract.
''',
     faq_add=[('Is the magnetic field near a current-carrying cable a health concern?',
               f'At mains frequency the ICNIRP 2010 general public reference level is 200 µT. A single conductor with {I:g} A reaches that at {r*1000:g} mm, but in a normal cable the opposing currents cancel most of the field, so typical household exposure is well under 1 µT.')])

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-18), slice 5: lift-force, radioactive-activity, faradays-law, wiens-law,
stefan-boltzmann-law. Every number is computed here from each page's default inputs."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-18'
pi = math.pi
g0 = 9.80665

# ---------------------------------------------------------------- Lift force
rho, v, S, CL = 1.225, 50.0, 16.0, 0.5
q = 0.5 * rho * v ** 2
L = q * S * CL
m = L / g0
vs_clean = math.sqrt(2 * L / (rho * S * 1.5))
vs_flap = math.sqrt(2 * L / (rho * S * 2.1))
cl_rows = ''
for c in (0.3, 0.5, 0.8, 1.0, 1.2, 1.5):
    vv = math.sqrt(2 * L / (rho * S * c))
    cl_rows += f"| {c:g} | {vv:.1f} m/s | {vv/0.514444:.0f} kn |\n"
bank_rows = ''
for phi in (0, 15, 30, 45, 60):
    n = 1 / math.cos(math.radians(phi))
    bank_rows += f"| {phi}° | {n:.3f} | {n*L:,.0f} N | {vs_clean*math.sqrt(n):.1f} m/s |\n"
n60 = 2.0

edit('physics/lift-force', date=U, phrase='lift force calculator',
     intro=("Lift is the aerodynamic force a wing produces at right angles to the oncoming air, and it grows with air density, wing area, lift coefficient and the square of speed. "
            "This lift force calculator applies L = ½ρv²SC_L and converts the result to the mass it can hold up.\n\n"
            "Pilots, aeronautics students, drone builders and model aircraft designers use it to size wings, estimate stall and take-off speeds and see how altitude or heavy loads change performance."),
     body_add=f'''
## Dynamic pressure: the part the pilot controls

The product ½ρv² is the dynamic pressure q, the quantity a pitot-static system actually senses. With the default inputs q = 0.5 × {rho:g} × {v:g}² = **{q:,.2f} Pa**. Lift is then simply q × S × C<sub>L</sub> = {q:,.2f} × {S:g} × {CL:g} = {L:,.0f} N. In a wind tunnel the process runs backwards: a force balance measures L, the tunnel instruments give q, and the lift coefficient is found as C<sub>L</sub> = L ÷ (q S). That is how published airfoil and wing C<sub>L</sub> curves are produced.

## Speed needed to carry {m:,.0f} kg at different lift coefficients

Holding lift at the default {L:,.0f} N in sea-level air, the wing must fly slower as C<sub>L</sub> (angle of attack) rises:

| C<sub>L</sub> | Airspeed for level flight | In knots |
|---|---|---|
{cl_rows}
Taking C<sub>L,max</sub> = 1.5 for the clean wing gives a stall speed of **{vs_clean:.1f} m/s**; with flaps raising C<sub>L,max</sub> to 2.1 it drops to **{vs_flap:.1f} m/s**. Lift-off is normally planned at about 1.1 to 1.2 times the stall speed in the take-off configuration.

## Extra lift needed in a turn

In a level turn the lift vector tilts, so the wing must produce W ÷ cos φ to keep the vertical component equal to the weight. The ratio is the load factor n, and the stall speed rises with √n:

| Bank angle | Load factor n | Lift required | Clean stall speed |
|---|---|---|---|
{bank_rows}
At 60° of bank the wing carries {n60:g} g, so a turn flown near the stall speed in level flight will stall long before the bank is reached.

## Common mistakes

- **Using knots or km/h as m/s.** 50 knots is only 25.7 m/s, and because speed is squared the lift comes out almost four times too high.
- **Using the wrong reference area.** S is the planform wing area quoted by the manufacturer, not the wetted surface area of both sides of the wing.
- **Using a 2D airfoil coefficient for the whole wing.** Section data (c<sub>l</sub>) from airfoil catalogues is higher than the finite wing C<sub>L</sub>, especially for low aspect ratio wings.
- **Assuming C<sub>L</sub> keeps rising with angle of attack.** Past the stall the flow separates and C<sub>L</sub> falls, so the equation with a large C<sub>L</sub> gives lift the wing cannot make.
- **Forgetting that lift must exceed weight in manoeuvres.** Turns and pull-ups need load factors above 1, as the bank table shows.
''',
     faq_add=[('What is dynamic pressure and how does it relate to lift?',
               f'Dynamic pressure is q = ½ρv², the pressure rise when moving air is brought to rest. Lift is q × S × C_L. At 50 m/s in sea-level air q is {q:,.0f} Pa, so each square metre of wing at C_L = 0.5 carries {q*0.5:,.0f} N.'),
              ('How much more lift does a wing need in a banked turn?',
               f'Lift must equal weight ÷ cos(bank angle). At 30° of bank that is 1.155 times the weight, and at 60° it is twice the weight, which also raises the stall speed by √2, about 41%.')])

# ---------------------------------------------------------------- Radioactive activity
NA = 6.02214076e23
yr = 31557600
mm, M, th, t = 1.0, 59.9338, 5.2714, 10.0
lam = math.log(2) / (th * yr)
N = mm / 1000 / M * NA
A0 = lam * N
Ci0 = A0 / 3.7e10
At = A0 * 2 ** (-t / th)
Cit = At / 3.7e10
loss_co = 1 - 2 ** (-1 / th)
loss_cs = 1 - 2 ** (-1 / 30.08)
t10 = th * math.log2(10)
t10cs = 30.08 * math.log2(10)
dec_rows = ''
for y in (0, 1, 2, 5, 10, 15, 20, 30):
    a = A0 * 2 ** (-y / th)
    dec_rows += f"| {y} yr | {a/1e10:.4f} × 10¹⁰ Bq | {a/3.7e10:.3f} Ci | {a/A0*100:.1f}% |\n"
# Cs-137 source mass for 100 mCi
lam_cs = math.log(2) / (30.08 * yr)
N_cs = 0.1 * 3.7e10 / lam_cs
m_cs = N_cs / NA * 136.9071 * 1000  # mg
# counting example: 1 kBq check source, 5% efficiency, 600 s
cnt = 1000 * 0.05 * 600
rel = 1 / math.sqrt(cnt) * 100


def sci(x):
    e = math.floor(math.log10(x))
    return f"{x/10**e:.3f} × 10^{e}"


edit('physics/radioactive-activity', date=U, phrase='radioactive activity calculator',
     intro=("Activity is the number of nuclei in a sample that decay each second, A = λN, measured in becquerels or curies. "
            "This radioactive activity calculator finds the decay constant, atom count and activity from mass, molar mass and half-life, then decays it over time.\n\n"
            "Radiation safety officers, nuclear medicine staff and instrument technicians use it to license sources, plan replacements and check the sealed Cs-137 and Co-60 sources in "
            "[nuclear level measurement](https://www.instrumentationblog.in/types-of-nuclear-level-measurement/)."),
     body_add=f'''
## Decay of the default 1 mg Co-60 source

Starting from A<sub>0</sub> = {A0/1e10:.4f} × 10¹⁰ Bq ({Ci0:.3f} Ci), the activity after each period is A<sub>0</sub> × 2<sup>−t/{th:g}</sup>:

| Elapsed time | Activity | Curies | Remaining |
|---|---|---|---|
{dec_rows}
A Co-60 source loses **{loss_co*100:.1f}% of its activity every year**, so it falls to 10% after {t10:.1f} years. A Cs-137 source loses only {loss_cs*100:.2f}% per year and takes {t10cs:.0f} years to reach 10%, which is why Cs-137 is the usual choice for level and density gauges that must stay calibrated for decades.

## How activity is measured in practice

A detector never sees every decay. A Geiger-Müller tube or scintillation probe records counts per second, and the activity is the net count rate divided by the counting efficiency, after subtracting background. Efficiency depends on the radiation type, energy, geometry and window, and is set by counting a certified reference source. Counting is statistical: a 1 kBq check source read at 5% efficiency for 600 s gives about {cnt:,.0f} counts, with a one-sigma uncertainty of √N, or **{rel:.1f}%**. Hospitals measure patient doses in a dose calibrator, an ionisation chamber with nuclide-specific settings that reads activity directly in MBq or mCi.

The calculator also works in reverse for licensing paperwork. A 100 mCi (3.7 GBq) Cs-137 gauge source contains only about **{m_cs:.2f} mg** of the isotope itself; the rest of the capsule is carrier and stainless steel.

## Common mistakes

- **Entering the capsule or compound mass.** Only the mass of the radioactive isotope counts. In CsCl, caesium is about 79% of the mass, and the Cs-137 is only a fraction of that.
- **Treating activity as dose.** Becquerels count decays; dose in grays or sieverts also depends on the emitted energy, distance and shielding.
- **Ignoring short-lived daughters.** Cs-137 gamma rays actually come from Ba-137m, which is in equilibrium with its parent; gamma yield is about 85 photons per 100 Cs-137 decays.
- **Mixing up mCi and MBq.** 1 mCi is 37 MBq, so a factor of 37 error is easy when reading certificates from different countries.
- **Using the activity on the certificate as today's value.** Always decay it from the certificate reference date before calibrating an instrument.
''',
     faq_add=[('How often should a Co-60 gauge source be replaced?',
               f'Co-60 loses about {loss_co*100:.1f}% of its activity each year and falls to half in 5.27 years. Many users replace or recalibrate when the count rate margin is gone, typically after one to two half-lives. A Cs-137 source decays only {loss_cs*100:.1f}% per year.'),
              ('How do I convert a detector count rate into activity?',
               'Subtract the background count rate, then divide the net counts per second by the detector efficiency for that nuclide and geometry. For example, 50 net counts per second at 5% efficiency means an activity of 1,000 Bq.')])

# ---------------------------------------------------------------- Faraday's law
Nt, Acm, B1, B2, dt_ms, R = 200, 50.0, 0.0, 0.4, 20.0, 10.0
A = Acm * 1e-4
dPhi = A * (B2 - B1)
dt = dt_ms / 1000
emf = Nt * abs(dPhi) / dt
Ii = emf / R
vs = Nt * abs(dPhi)
Q = vs / R
dt_rows = ''
for d in (1, 5, 10, 20, 50, 100, 1000):
    e = Nt * abs(dPhi) / (d / 1000)
    dt_rows += f"| {d:,} ms | {e:,.4g} V | {e/R:,.4g} A |\n"
f_ac = 50
w = 2 * pi * f_ac
e_pk = Nt * B2 * A * w
e_rms = e_pk / math.sqrt(2)
emf_rev = Nt * A * 2 * B2 / dt
th45 = Nt * A * B2 * math.cos(math.radians(60)) / dt

edit('physics/faradays-law', date=U, phrase="Faraday's law calculator",
     intro=("Faraday's law of induction says a changing magnetic flux through a coil induces a voltage proportional to the number of turns and the rate of change. "
            "This Faraday's law calculator finds the flux change, average EMF and current. See [Faraday's law of electromagnetic induction](https://www.instrumentationblog.in/faradays-law-electromagnetic-induction/).\n\n"
            "Physics students, electrical engineers and instrument technicians use it for search coils, generators, sensors and switching spikes; "
            "[Lenz's law](https://www.instrumentationblog.in/lenzs-law-electromagnetic-induction/) gives the current direction."),
     body_add=f'''
## Speed of the change for the default coil

The default coil sees the same flux change of {dPhi*1000:.1f} mWb every time; only the time it takes changes the result:

| Time for the change | Average EMF | Current in {R:g} Ω |
|---|---|---|
{dt_rows}
The EMF and the current scale inversely with Δt, but the product ε × Δt stays at N ΔΦ = **{vs:.2f} V·s**. That means the total charge driven round the circuit is fixed too: Q = N ΔΦ ÷ R = {vs:.2f} ÷ {R:g} = **{Q:.3f} C**, whether the change takes 1 ms or 1 s.

## Measuring flux with a search coil

That fixed volt-second product is the basis of flux measurement. A small search coil is connected to an integrating fluxmeter, the coil is pulled out of the field (or the field is switched off), and the meter integrates the voltage. Dividing the integral by the number of turns gives the flux, and dividing again by the coil area gives B. For the default coil, an integral of {vs:.2f} V·s means ΔΦ = {vs:.2f} ÷ {Nt} = {dPhi:.4f} Wb and B = {dPhi:.4f} ÷ {A:g} m² = {B2:g} T. The same principle is used in Rogowski coils, which integrate the EMF from a changing current to measure large AC or pulsed currents without a magnetic core.

## Sinusoidal flux: the generator case

If the same coil rotates in the {B2:g} T field at {f_ac} Hz, the flux varies sinusoidally and the peak EMF is N B A ω = {Nt} × {B2:g} × {A:g} × {w:.2f} = **{e_pk:.1f} V**, or {e_rms:.1f} V rms. That is more than six times the 20 V average from the 20 ms ramp, because the flux swings from +BA to −BA every half cycle and does so in 10 ms.

## Common mistakes

- **Leaving the area in cm².** 50 cm² is 0.005 m²; using 50 gives an EMF 10,000 times too large.
- **Missing a field reversal.** Going from +{B2:g} T to −{B2:g} T is a change of {2*B2:g} T, so the EMF doubles to {emf_rev:.0f} V for the same 20 ms.
- **Ignoring the angle.** If the field is 60° from the coil normal, only cos 60° = 0.5 of it links the coil and the EMF falls to {th45:.0f} V.
- **Treating the average as the peak.** The calculator gives the average over Δt. A fast, non-linear change can have a much higher instantaneous peak.
- **Forgetting the coil's own resistance and inductance.** R must include the winding, and a coil with a large L/R time constant will not reach ε ÷ R during a short pulse.
''',
     faq_add=[('Why does the total induced charge not depend on how fast the flux changes?',
               f'Charge is current times time, Q = (N ΔΦ ÷ Δt ÷ R) × Δt = N ΔΦ ÷ R. A faster change gives a higher EMF for a shorter time. For 200 turns, 2 mWb and 10 Ω the charge is always {Q:.2f} C.'),
              ('What happens if the magnetic field reverses direction?',
               f'The flux change is the full swing from +B to −B, twice the change from zero to B. With the default coil, reversing 0.4 T in 20 ms induces {emf_rev:.0f} V instead of 20 V.')])

# ---------------------------------------------------------------- Wien's law
b = 2.897771955e-3
T = 5778.0
lam_nm = b / T * 1e9
fp = 0.05878925757 * T
hc_eVnm = 1239.841984
E_pk = hc_eVnm / lam_nm
c = 299792458.0
lam_f = c / (fp * 1e12) * 1e9
# fraction of black-body power below lambda_max, by numerical integration in x = hc/(lambda k T)
# x at peak = 4.965114231744276
xp = 4.965114231744276


def frac_above_x(x0):
    # integral of x^3/(e^x - 1) from x0 to inf, divided by pi^4/15
    s, n = 0.0, 200000
    hi = 60.0
    h = (hi - x0) / n
    for i in range(n + 1):
        x = x0 + i * h
        f = x ** 3 / math.expm1(x)
        wgt = 1 if i in (0, n) else (4 if i % 2 else 2)
        s += wgt * f
    return s * h / 3 / (pi ** 4 / 15)


f_below = frac_above_x(xp)  # short wavelengths = large x
pyro_rows = ''
for tc in (100, 300, 500, 800, 1000, 1200, 1500):
    tk = tc + 273.15
    pyro_rows += f"| {tc:,} °C | {tk:,.2f} K | {b/tk*1e6:.2f} µm |\n"
dT_err = T * 0.01

edit('physics/wiens-law', date=U, phrase="Wien's law calculator",
     intro=("Wien's displacement law states that the wavelength at which a black body radiates most strongly is inversely proportional to its absolute temperature. "
            "This Wien's law calculator returns the peak wavelength and peak frequency for any temperature, or the temperature for a measured peak.\n\n"
            "Astronomers use it to estimate star temperatures, while engineers and technicians use it to pick the wavelength band of infrared thermometers, pyrometers and thermal cameras."),
     body_add=f'''
## What the Sun's peak means

At the default 5,778 K the peak sits at {lam_nm:.1f} nm, and a photon at that wavelength carries E = 1,239.84 ÷ {lam_nm:.1f} = **{E_pk:.2f} eV**. The per-frequency peak of {fp:.1f} THz corresponds to {lam_f:.0f} nm, in the near infrared, which shows how much the "peak" depends on how the spectrum is plotted. Integrating Planck's law shows that only **{f_below*100:.1f}%** of a black body's power is emitted at wavelengths shorter than λ<sub>max</sub>; the long tail toward the infrared carries the other {100-f_below*100:.1f}%. The Sun looks white rather than green because its spectrum is broad and our eyes respond to the whole visible band.

## Choosing the band for an infrared thermometer

Industrial pyrometers are built around the shift in peak wavelength with process temperature:

| Process temperature | Absolute | Peak wavelength |
|---|---|---|
{pyro_rows}
General purpose handheld thermometers work in the 8 to 14 µm atmospheric window, which suits objects from below 0 °C to a few hundred °C. Instruments for molten metal and glass use short bands near 1 µm or 1.6 µm, on the short-wavelength side of the peak. There the signal changes very steeply with temperature, so an error in the emissivity setting causes a much smaller temperature error. Ratio (two-colour) pyrometers compare two nearby short wavelengths to cancel emissivity and dust effects.

## Sensitivity to measurement error

Since T = b ÷ λ<sub>max</sub>, a relative error in the peak wavelength gives the same relative error in temperature. Locating the solar peak 1% too long would put the temperature about {dT_err:.0f} K too low. Broad, flat peaks make the exact maximum hard to find, which is why astronomers usually fit the whole spectrum or use colour indices instead.

## Common mistakes

- **Entering degrees Celsius as kelvin.** 1,000 °C is 1,273.15 K; treating it as 1,000 K shifts the peak from {b/1273.15*1e6:.2f} µm to 2.90 µm.
- **Mixing the wavelength and frequency peaks.** Converting ν<sub>max</sub> with λ = c ÷ ν gives about 1.76 × λ<sub>max</sub>, not the same wavelength.
- **Assuming the visible colour is the peak colour.** A body with a peak in the green still looks white.
- **Applying it to line sources.** Neon signs, LEDs and sodium lamps emit lines, not a thermal spectrum, so their colour gives no temperature.
- **Measuring through glass.** Ordinary window glass blocks most radiation beyond about 4 to 5 µm, so a thermal camera cannot see a room-temperature object behind it.
''',
     faq_add=[("What fraction of black-body radiation is emitted below the peak wavelength?",
               f"About {f_below*100:.0f}%, at any temperature. Planck's law is skewed, with a steep fall on the short-wavelength side and a long tail into the infrared that carries roughly {100-f_below*100:.0f}% of the power.")])

# ---------------------------------------------------------------- Stefan-Boltzmann
sig = 5.670374419e-8
eps, Aa, Tc, Tsc = 0.9, 1.0, 100.0, 20.0
Tk, Tsk = Tc + 273.15, Tsc + 273.15
E = eps * sig * Tk ** 4
P = E * Aa
Pn = eps * sig * Aa * (Tk ** 4 - Tsk ** 4)
hr = eps * sig * (Tk ** 2 + Tsk ** 2) * (Tk + Tsk)
hr2 = Pn / (Tk - Tsk)
kwh = Pn * 8760 / 1000
eps_rows = ''
for e in (0.05, 0.1, 0.3, 0.6, 0.9, 0.95):
    pn = e * sig * Aa * (Tk ** 4 - Tsk ** 4)
    eps_rows += f"| {e:g} | {pn:,.1f} W | {pn*8760/1000:,.0f} kWh |\n"
# pipe example: 1 m of 114.3 mm OD (DN100) bare painted pipe vs aluminium jacket at the default temperatures
D = 0.1143
Ap = pi * D * 1.0
Pp = eps * sig * Ap * (Tk ** 4 - Tsk ** 4)
Pal = 0.05 * sig * Ap * (Tk ** 4 - Tsk ** 4)
# parallel plates eps 0.9 each
epp = 1 / (1 / 0.9 + 1 / 0.9 - 1)
Ppl = epp * sig * Aa * (Tk ** 4 - Tsk ** 4)
# IR thermometer emissivity error: surface at 100 C, eps 0.9, instrument set to 0.95, ignoring reflected term
# W measured = 0.9 sig T^4 + 0.1 sig Ts^4; instrument solves 0.95 sig Ti^4 + 0.05 sig Ts^4 = W
Wm = 0.9 * sig * Tk ** 4 + 0.1 * sig * Tsk ** 4
Ti = ((Wm - 0.05 * sig * Tsk ** 4) / (0.95 * sig)) ** 0.25 - 273.15

edit('physics/stefan-boltzmann-law', date=U, phrase='Stefan-Boltzmann law calculator',
     intro=("The Stefan-Boltzmann law says every surface above absolute zero radiates power in proportion to its emissivity, its area and the fourth power of its absolute temperature. "
            "This Stefan-Boltzmann law calculator gives the emitted flux, total power and net radiant heat loss to cooler surroundings.\n\n"
            "Heat transfer engineers, HVAC and insulation designers, furnace operators and physics students use it to size heat losses, choose surface finishes and compare radiation with convection."),
     body_add=f'''
## Radiation heat transfer coefficient

Engineers often fold radiation into a coefficient that can be added to the convection coefficient: h<sub>r</sub> = εσ(T² + T<sub>s</sub>²)(T + T<sub>s</sub>). With the default 373.15 K surface and 293.15 K room:

- h<sub>r</sub> = {eps:g} × 5.670 × 10⁻⁸ × ({Tk:.2f}² + {Tsk:.2f}²) × ({Tk:.2f} + {Tsk:.2f}) = **{hr:.2f} W/(m²·K)**
- Check: {Pn:.1f} W ÷ ({Tc:g} − {Tsc:g}) K = {hr2:.2f} W/(m²·K)

Natural convection from a warm vertical surface in still air is typically 3 to 10 W/(m²·K), so at only 100 °C radiation already carries about half of the total heat loss. Over a year of continuous operation the default square metre radiates away **{kwh:,.0f} kWh** net.

## Effect of surface finish

Same 1 m² at 100 °C in 20 °C surroundings, with only the emissivity changed:

| Emissivity | Net radiation loss | Per year |
|---|---|---|
{eps_rows}
This is why insulated hot pipes are clad in aluminium or stainless steel sheet. One metre of bare painted DN100 pipe (114.3 mm outside diameter, {Ap:.3f} m² of surface) at these temperatures radiates **{Pp:.0f} W**; the same area of clean aluminium at ε = 0.05 radiates only {Pal:.1f} W.

## Using emissivity with infrared thermometers

A non-contact thermometer measures radiated power and inverts the same law, so it needs the right emissivity. If the default ε = 0.9 surface at 100 °C is read with the instrument set to 0.95, the reading is about **{Ti:.1f} °C**, a little low, because the instrument assumes more of the signal is emitted and less reflected from the room. On shiny metals with ε near 0.1 the error can be tens of degrees, so technicians apply black tape or paint of known emissivity before measuring.

## Common mistakes

- **Using °C inside T⁴.** 100⁴ and 373.15⁴ differ by a factor of almost 200.
- **Forgetting the surroundings.** The emitted 989 W is not the heat loss; the surface absorbs radiation from the room, leaving a net {Pn:.0f} W.
- **Using the small-body formula between two large plates.** For parallel plates both emissivities matter: ε<sub>eff</sub> = 1 ÷ (1/ε<sub>1</sub> + 1/ε<sub>2</sub> − 1), which is {epp:.3f} for two ε = 0.9 plates and gives {Ppl:.0f} W per m² instead of {Pn:.0f} W.
- **Taking emissivity from the wrong condition.** Polished and oxidised versions of the same metal can differ tenfold; check the actual surface.
- **Ignoring dirt and ageing.** Aluminium jacketing that is dusty or weathered radiates far more than the 0.05 quoted for a clean sheet.
''',
     faq_add=[('What is the radiation heat transfer coefficient?',
               f'It is h_r = εσ(T² + T_s²)(T + T_s), the net radiant loss per square metre per kelvin of temperature difference. For ε = 0.9 at 100 °C in a 20 °C room it is about {hr:.1f} W/(m²·K), comparable to natural convection.')])

print('done')

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-18), slice 6: faraday-electrolysis, lm317, newtons-law-of-cooling, elastic-collision,
transformer-size. Worked examples use each page's default inputs; all numbers computed here. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-18'
F = 96485.33212

# ---------------------------------------------------------------- Faraday electrolysis
I, th, Me, eta = 2.0, 1.0, 31.773, 1.0
Q = I * th * 3600
ne = Q / F
m = ne * Me * eta
# target thickness: 10 um nickel on 200 cm2 at 2 A, 95 % efficiency
A_ni, thk_um, rho_ni, Me_ni, eta_ni = 200.0, 10.0, 8.908, 29.3467, 0.95
m_ni = thk_um * 1e-4 * A_ni * rho_ni
t_ni = m_ni * F / (I * Me_ni * eta_ni)
J_ni = I / (A_ni / 100)  # A/dm2
rate_rows = ''
for name, me, rho in (('Copper, Cu²⁺', 31.773, 8.96), ('Silver, Ag⁺', 107.8682, 10.49), ('Nickel, Ni²⁺', 29.3467, 8.908),
                      ('Zinc, Zn²⁺', 32.69, 7.14), ('Tin, Sn²⁺', 59.355, 7.265), ('Gold, Au⁺', 196.96657, 19.32),
                      ('Chromium, Cr³⁺', 17.332033, 7.19)):
    # 1 A/dm2 = 0.01 A/cm2; thickness rate in um/min
    r = 0.01 * 60 / F * me / rho * 1e4
    rate_rows += f"| {name} | {rho:g} g/cm³ | {r:.3f} µm/min | {60/r:.1f} min |\n"
eff_lo = m * 0.92

edit('chemistry/faraday-electrolysis', date=U, phrase="Faraday's law of electrolysis calculator",
     intro=("Faraday's laws of electrolysis state that the mass deposited or dissolved at an electrode is proportional to the charge passed "
            "and to the molar mass per electron transferred. This Faraday's law of electrolysis calculator returns charge, moles of electrons and mass for common plating metals.\n\n"
            "Electroplaters, anodizing and refining engineers, and chemistry students use it to set rectifier current and plating time, "
            "check bath efficiency and predict hydrogen output."),
     body_add=f'''
## Plating time for a target thickness

The default case (2 A for 1 h on copper at 100%) gives Q = {Q:,.0f} C, n<sub>e</sub> = {ne:.5f} mol and **{m:.4f} g** of copper. In the shop the question usually runs the other way: how long to reach a specified thickness. Take a {thk_um:g} µm nickel layer on {A_ni:g} cm² at {I:g} A from a Watts bath running at {eta_ni*100:.0f}% efficiency:

- Mass needed = {thk_um:g} × 10⁻⁴ cm × {A_ni:g} cm² × {rho_ni} g/cm³ = **{m_ni:.4f} g**
- Current density = {I:g} A ÷ {A_ni/100:g} dm² = {J_ni:g} A/dm², a modest value for a Watts nickel bath
- Time = m × F ÷ (I × M/z × η) = {m_ni:.4f} × 96,485 ÷ ({I:g} × {Me_ni} × {eta_ni}) = **{t_ni:,.0f} s ({t_ni/60:.1f} min)**

Enter the mass, the current and the efficiency with the time field cleared and the calculator gives the same result.

## Deposition rate at 1 A/dm²

Platers think in current density rather than total current, because thickness depends on amps per unit area. At 1 A/dm² and 100% efficiency the average build-up rate is (0.01 A/cm² × 60 s × M/z) ÷ (F × density):

| Metal and ion | Density | Thickness rate | Time for 10 µm |
|---|---|---|---|
{rate_rows}
Divide the time by the current density in A/dm² and by the efficiency. Hard chromium is far slower than the Cr³⁺ figure suggests, because chromic acid baths work at z = 6 and only 10 to 25% efficiency.

## How it is used in practice

Plating rectifiers carry an ampere-hour meter, and the line controller stops each load once the ampere-hours calculated from Faraday's law are reached. Bath efficiency is checked by plating a weighed test panel or by a copper coulometer in series: if the panel gains {eff_lo:.3f} g where {m:.3f} g was expected, the bath is running at 92%. Electrowinning and copper refining tanks use the same figure to report current efficiency to management, since every lost percent is wasted energy.

## Common mistakes

- **Using hours instead of seconds.** Q in coulombs needs time in seconds; 1 A·h is 3,600 C.
- **Wrong ion charge.** Copper from a cyanide bath is Cu⁺ (z = 1) and deposits twice the mass per coulomb of an acid Cu²⁺ bath.
- **Using total current for one part.** On a loaded rack the current divides between parts by area, so compute per part with its own share.
- **Ignoring hidden area.** Racks, hooks and the inside of tubes take current too, which lowers the thickness on the area you measure.
- **Assuming average thickness is the minimum.** Specifications set a minimum at significant surfaces, so plate long enough that recesses reach it.
''',
     faq_add=[('How do I convert plating current density to total current?',
               f'Multiply the current density by the area being plated. {A_ni:g} cm² is {A_ni/100:g} dm², so {J_ni:g} A/dm² needs {I:g} A. Include the rack contacts and any back faces that are exposed to the solution.')])

# ---------------------------------------------------------------- LM317
R1, R2, Vi, IL = 240.0, 715.0, 12.0, 0.5
Vo = 1.25 * (1 + R2 / R1) + 50e-6 * R2
Hd = Vi - Vo
Pd = Hd * IL
th_ja, th_jc, th_cs, Tj_max, Ta = 50.0, 4.0, 0.5, 125.0, 40.0
Tj_bare = 25 + Pd * th_ja
th_tot = (Tj_max - Ta) / Pd
th_sa = th_tot - th_jc - th_cs
I_div = 1.25 / R1
vin_rows = ''
for v in (8, 9, 12, 15, 24):
    h = v - Vo
    p = h * IL
    vin_rows += f"| {v} V | {h:.2f} V | {p:.2f} W | {Vo/v*100:.0f}% | {'Marginal' if h < 3 else 'OK'} |\n"
I_led = 0.35
R_led = 1.25 / I_led
P_led = 1.25 * I_led

edit('electronics/lm317', date=U, phrase='LM317 calculator',
     intro=("The LM317 is an adjustable linear regulator that keeps 1.25 V between its output and adjust pins, so a two resistor divider sets the output. "
            "This LM317 calculator finds the output voltage, headroom and heat to remove. See [linear vs switching voltage regulators](https://www.instrumentationblog.in/linear-vs-switching-voltage-regulators/).\n\n"
            "Hobbyists, test engineers and instrument designers use it for bench supplies and clean low-noise rails. "
            "Also read [LDO dropout voltage](https://www.instrumentationblog.in/ldo-regulator-dropout-voltage/)."),
     body_add=f'''
## Heat sink check for the default design

The default circuit (R1 = {R1:g} Ω, R2 = {R2:g} Ω, {Vi:g} V in, {IL:g} A) gives V<sub>out</sub> = **{Vo:.3f} V**, headroom **{Hd:.3f} V** and P<sub>D</sub> = **{Pd:.3f} W**. Using the classic TO-220 figures of about {th_ja:g} °C/W junction to air and {th_jc:g} °C/W junction to case:

- Without a heat sink at 25 °C: T<sub>J</sub> = 25 + {Pd:.3f} × {th_ja:g} = **{Tj_bare:.0f} °C**, far above the {Tj_max:g} °C limit, so the thermal shutdown will cycle
- Allowed total thermal resistance at {Ta:g} °C ambient: ({Tj_max:g} − {Ta:g}) ÷ {Pd:.3f} = {th_tot:.1f} °C/W
- Heat sink needed: {th_tot:.1f} − {th_jc:g} (junction to case) − {th_cs:g} (pad) = **{th_sa:.1f} °C/W or lower**

A small clip-on TO-220 heat sink of about 20 °C/W is therefore right at the limit; a larger extruded one with some margin is the safer choice.

## Effect of input voltage on dissipation

For the same {Vo:.2f} V output at {IL:g} A, every extra volt of input is burned in the regulator:

| Input | Headroom | Dissipation | Efficiency | Headroom check |
|---|---|---|---|---|
{vin_rows}
Feeding a 5 V LM317 rail from 24 V wastes more power than it delivers. Pick the lowest input that still keeps 3 V of headroom at the bottom of the ripple and at minimum mains voltage.

## Using the LM317 as a current source

With a single resistor between OUT and ADJ and the load from ADJ to ground, the LM317 regulates current instead of voltage: I = 1.25 V ÷ R. A {I_led*1000:.0f} mA LED driver needs R = 1.25 ÷ {I_led} = **{R_led:.2f} Ω** (use 3.6 Ω), and that resistor dissipates {P_led:.3f} W, so a 1 W part is appropriate. Add about 3 V of overhead plus the LED string voltage to find the minimum input.

## Common mistakes

- **Making R1 too large.** The divider current must cover the minimum load current (up to 10 mA on some datasheets). With R1 = {R1:g} Ω it is {I_div*1000:.1f} mA; with 1 kΩ only 1.25 mA, and the output can drift up at no load.
- **Putting R1 at the far end of a long wire.** Connect R1 directly at the output and adjust pins; resistance in the output lead adds to the 1.25 V reference error.
- **Leaving out protection diodes.** With a large output capacitor or a 10 µF adjust capacitor, a diode from output to input and another from adjust to output stop the capacitors discharging through the chip when input is shorted.
- **Forgetting ripple valleys.** Headroom must be met at the lowest point of the rectifier ripple, not at the average DC input.
- **Using the reference as exact.** V<sub>REF</sub> varies from 1.20 to 1.30 V between parts, so a fixed divider can be 4% off; trim if the rail must be precise.
''',
     faq_add=[('Why does my LM317 output voltage rise when nothing is connected?',
               f'The LM317 needs a minimum load current, typically 3.5 mA and up to 10 mA, to stay in regulation. The R1 and R2 divider supplies it: 1.25 V ÷ {R1:g} Ω = {I_div*1000:.1f} mA. If R1 is several hundred ohms higher, add a bleed resistor across the output.')])

# ---------------------------------------------------------------- Newton's law of cooling
T0, Ta_c, k, t = 90.0, 20.0, 0.05, 10.0
Tt = Ta_c + (T0 - Ta_c) * math.exp(-k * t)
thalf = math.log(2) / k
tau = 1 / k
Tdrink = 60.0
t60 = math.log((T0 - Ta_c) / (Tdrink - Ta_c)) / k
k_rows = ''
for kk in (0.02, 0.03, 0.05, 0.08, 0.12):
    tt = math.log((T0 - Ta_c) / (Tdrink - Ta_c)) / kk
    k_rows += f"| {kk:g} /min | {1/kk:.1f} min | {math.log(2)/kk:.1f} min | {tt:.1f} min |\n"
# k from two readings taken mid-way (not starting at T0)
ta1, Ta1, ta2, Ta2 = 4.0, 77.0, 12.0, 58.0
k2 = math.log((Ta1 - Ta_c) / (Ta2 - Ta_c)) / (ta2 - ta1)
# lumped estimate for a 100 g aluminium block
mb, cb, Ab, hb, kal, rho_al = 0.1, 897.0, 0.006, 15.0, 205.0, 2700.0
k_blk = hb * Ab / (mb * cb) * 60
Lc = mb / rho_al / Ab
Bi = hb * Lc / kal

edit('physics/newtons-law-of-cooling', date=U, phrase="Newton's law of cooling calculator",
     intro=("Newton's law of cooling says an object's rate of temperature change is proportional to its difference from the surroundings, so it approaches ambient exponentially. "
            "This Newton's law of cooling calculator finds the temperature after a given time, the cooling constant and the half-time.\n\n"
            "Students, food safety staff, process engineers and instrument technicians use it to predict cooling times and to understand a "
            "[temperature sensor's response time](https://www.instrumentationblog.in/temperature-sensor-response-time/)."),
     body_add=f'''
## Time to reach a target temperature

Rearranging the law gives t = ln[(T<sub>0</sub> − T<sub>a</sub>) ÷ (T − T<sub>a</sub>)] ÷ k. With the default inputs ({T0:g} °C, {Ta_c:g} °C room, k = {k:g} per minute) the calculator shows **{Tt:.2f} °C** after {t:g} min, a half-time of **{thalf:.2f} min** and a time constant of **{tau:g} min**. The same coffee reaches a comfortable {Tdrink:g} °C after ln({T0-Ta_c:g} ÷ {Tdrink-Ta_c:g}) ÷ {k:g} = **{t60:.2f} min**.

How fast it gets there depends entirely on k:

| k | Time constant | Half-time | Time from {T0:g} to {Tdrink:g} °C |
|---|---|---|---|
{k_rows}
A lid, an insulated mug or a larger volume lowers k; stirring, a draught or a thin metal cup raises it.

## Finding k from two readings

The starting temperature does not have to be known. If a probe reads {Ta1:g} °C at {ta1:g} min and {Ta2:g} °C at {ta2:g} min in a {Ta_c:g} °C room, then k = ln[({Ta1:g} − {Ta_c:g}) ÷ ({Ta2:g} − {Ta_c:g})] ÷ ({ta2:g} − {ta1:g}) = **{k2:.4f} per minute**. Take the readings well apart, because the logarithm magnifies small errors when the two differences are nearly equal.

## Estimating k from the physics

For a solid with a uniform temperature, k = hA ÷ (mc). A {mb*1000:.0f} g aluminium block (c = {cb:g} J/kg·K) with {Ab*1e4:.0f} cm² of surface in still air (h ≈ {hb:g} W/m²·K including radiation) gives k = {hb:g} × {Ab} ÷ ({mb} × {cb:g}) × 60 = **{k_blk:.4f} per minute**. The lumped model is valid when the Biot number hL<sub>c</sub>/k<sub>solid</sub> is below 0.1; here L<sub>c</sub> = V/A = {Lc*1000:.2f} mm and Bi = {Bi:.1e}, so the block is effectively uniform. A thick block of plastic or food is not, and its centre lags the surface.

## Common mistakes

- **Mixing units of k.** This calculator uses k per minute. A k quoted per second must be multiplied by 60 first.
- **Using the temperature itself instead of the difference.** The exponential applies to T − T<sub>a</sub>; percentages of the starting temperature are meaningless.
- **Assuming k is constant over a wide range.** Natural convection and radiation both strengthen at large differences, so fit k over the range you actually care about.
- **Ignoring evaporation.** An open cup of hot liquid loses a large share of its heat by evaporation, so it cools faster at first than the law predicts.
- **Applying it during a phase change.** While water freezes or wax solidifies the temperature stays flat; use the [latent heat calculator](/physics/latent-heat/) for that stage.
''',
     faq_add=[('Does an object ever reach exactly the ambient temperature?',
               'In the model, no: the difference only approaches zero. In practice it is treated as finished after about five time constants, when less than 0.7% of the original difference remains, which is smaller than most thermometers can resolve.')])

# ---------------------------------------------------------------- Elastic collision
m1, u1, m2, u2 = 2.0, 3.0, 1.0, -1.0
M = m1 + m2
v1 = ((m1 - m2) * u1 + 2 * m2 * u2) / M
v2 = ((m2 - m1) * u2 + 2 * m1 * u1) / M
vc = (m1 * u1 + m2 * u2) / M
KE0 = 0.5 * m1 * u1 ** 2 + 0.5 * m2 * u2 ** 2
KEel = 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2
dKE = KE0 - 0.5 * M * vc ** 2
mu = m1 * m2 / M
dKE_mu = 0.5 * mu * (u1 - u2) ** 2
p0 = m1 * u1 + m2 * u2
e_rows = ''
for e in (0.0, 0.25, 0.5, 0.75, 1.0):
    a = (p0 - m2 * e * (u1 - u2)) / M
    b = (p0 + m1 * e * (u1 - u2)) / M
    lost = KE0 - 0.5 * m1 * a ** 2 - 0.5 * m2 * b ** 2
    e_rows += f"| {e:g} | {a:.3f} m/s | {b:.3f} m/s | {lost:.3f} J | {lost/KE0*100:.1f}% |\n"
r_rows = ''
for r in (0.1, 0.5, 1.0, 2.0, 12.0, 100.0):
    a = (1 - r) / (1 + r) * u1
    b = 2 / (1 + r) * u1
    fr = 4 * r / (1 + r) ** 2
    r_rows += f"| {r:g} | {a:.3f} m/s | {b:.3f} m/s | {fr*100:.1f}% |\n"
fC = 4 * 12 / 13 ** 2

edit('physics/elastic-collision', date=U, phrase='elastic collision calculator',
     intro=("Momentum is conserved in every collision; in an elastic collision kinetic energy is conserved too, while in a perfectly inelastic one the bodies stick together. "
            "This elastic collision calculator gives the final velocities for both cases in one dimension and the energy lost on sticking.\n\n"
            "Physics students, lab instructors and engineers use it to check air track experiments, "
            "crash and impact estimates, and the limits any real collision must fall between."),
     body_add=f'''
## Checking the default result

The default carts ({m1:g} kg at {u1:g} m/s and {m2:g} kg at {u2:g} m/s) give elastic final velocities of **{v1:.3f} m/s** and **{v2:.3f} m/s**, a common velocity of **{vc:.3f} m/s** if they stick, and **{dKE:.3f} J** lost. Three quick checks confirm the elastic answer:

- Momentum after = {m1:g} × {v1:.3f} + {m2:g} × {v2:.3f} = {m1*v1+m2*v2:.3f} kg·m/s, equal to the {p0:g} kg·m/s before
- Kinetic energy after = {KEel:.3f} J, equal to the {KE0:g} J before
- Relative velocity reverses: u<sub>1</sub> − u<sub>2</sub> = {u1-u2:g} m/s before, v<sub>2</sub> − v<sub>1</sub> = {v2-v1:.3f} m/s after

The energy lost when sticking also follows from the reduced mass μ = m<sub>1</sub>m<sub>2</sub> ÷ (m<sub>1</sub> + m<sub>2</sub>) = {mu:.4f} kg: ΔKE = ½ μ (u<sub>1</sub> − u<sub>2</sub>)² = 0.5 × {mu:.4f} × {(u1-u2)**2:g} = **{dKE_mu:.3f} J**.

## Partially elastic collisions

Real impacts fall between the two limits and are described by the coefficient of restitution e. The final velocities are v<sub>1</sub> = [p − m<sub>2</sub>e(u<sub>1</sub> − u<sub>2</sub>)] ÷ (m<sub>1</sub> + m<sub>2</sub>) and v<sub>2</sub> = [p + m<sub>1</sub>e(u<sub>1</sub> − u<sub>2</sub>)] ÷ (m<sub>1</sub> + m<sub>2</sub>). For the default carts:

| e | v<sub>1</sub> | v<sub>2</sub> | Energy lost | Share of initial KE |
|---|---|---|---|---|
{e_rows}
The loss scales with 1 − e², so a ball with e = 0.5 still loses three quarters of the energy available in the centre of mass frame.

## Mass ratio and energy transfer

When mass 1 at {u1:g} m/s hits a stationary mass 2 elastically, the share of kinetic energy handed over is 4m<sub>1</sub>m<sub>2</sub> ÷ (m<sub>1</sub> + m<sub>2</sub>)²:

| m<sub>2</sub> ÷ m<sub>1</sub> | v<sub>1</sub> | v<sub>2</sub> | Energy transferred |
|---|---|---|---|
{r_rows}
Transfer is complete only for equal masses. This is why nuclear reactors slow neutrons with light nuclei: a neutron loses up to all of its energy to a hydrogen nucleus but at most {fC*100:.1f}% to carbon 12, which is the ratio of 12 in the table.

## Measuring collisions in the lab

Air tracks with photogates or ultrasonic motion sensors remove most friction, so carts with magnetic bumpers come close to e = 1 and carts with Velcro pads give e = 0. Measure each velocity just before and just after contact, because the carts slow over longer distances.

## Common mistakes

- **Dropping the sign.** Velocities are vectors along the line; a body moving the other way must be entered as negative.
- **Expecting kinetic energy to be conserved when objects stick.** Only momentum is; the loss goes into heat, sound and deformation.
- **Using the 1D formulas for glancing impacts.** Off-centre collisions need momentum conserved in two directions.
- **Mixing units.** Enter both masses in the same unit and both velocities in the same unit before comparing results.
''',
     faq_add=[('Is there a quick formula for the energy lost in a perfectly inelastic collision?',
               f'Yes. ΔKE = ½ μ (u1 − u2)², where μ = m1m2 ÷ (m1 + m2) is the reduced mass. For the default 2 kg and 1 kg carts closing at 4 m/s, μ = 0.667 kg and ΔKE = {dKE_mu:.3f} J, the same as the calculator.')])

# ---------------------------------------------------------------- Transformer size
P, df, pf, g = 500.0, 0.7, 0.9, 0.25
Pd_kw = P * df
S = Pd_kw / pf * (1 + g)
S0 = Pd_kw / pf
Sr = 500.0
P0, Pk = 0.9, 6.0  # illustrative no-load and full-load load losses for 500 kVA, kW
x0 = S0 / Sr
loss0 = P0 + Pk * x0 ** 2
eff0 = Pd_kw / (Pd_kw + loss0) * 100
xmax = math.sqrt(P0 / Pk)
e_rows = ''
for x in (0.25, xmax, 0.5, 0.75, 1.0):
    out = x * Sr * pf
    l = P0 + Pk * x ** 2
    e_rows += f"| {x*100:.0f}% | {out:.0f} kW | {l:.2f} kW | {out/(out+l)*100:.2f}% |\n"
yr_kwh = loss0 * 8760
meas = 330.0
S_meas = meas * (1 + g)

edit('electrical/transformer-size', date=U, phrase='transformer size calculator',
     intro=("Sizing a transformer means turning the connected load into a kVA rating after allowing for demand factor, power factor and future growth. "
            "This transformer size calculator gives the maximum demand and the kVA to specify.\n\n"
            "Electrical engineers, contractors and plant planners use it at the design stage, since an undersized unit overheats and an oversized one costs more and wastes no-load losses. "
            "See [how to calculate transformer kVA rating](https://www.instrumentationblog.in/how-to-calculate-transformer-kva-rating/)."),
     body_add=f'''
## Losses and efficiency at the day one load

The default inputs give a required rating of **{S:.0f} kVA** ({Pd_kw:g} kW maximum demand), so a {Sr:.0f} kVA unit is chosen. Before growth it carries {S0:.1f} kVA, a loading of {x0*100:.1f}%. Taking illustrative losses for a {Sr:.0f} kVA oil-filled unit of {P0} kW no-load (core) and {Pk:g} kW load (copper) loss at full load, with load loss scaling with the square of loading:

| Loading | Output at PF {pf} | Total losses | Efficiency |
|---|---|---|---|
{e_rows}
Efficiency peaks at √({P0} ÷ {Pk:g}) = {xmax*100:.1f}% load, where copper loss equals core loss, and the curve is flat between about 30% and 80%. At the day one load the losses are {P0} + {Pk:g} × {x0:.3f}² = **{loss0:.2f} kW**, an efficiency of {eff0:.2f}%. Held at that load all year, the losses come to about {yr_kwh:,.0f} kWh, which is why buyers compare tender offers on capitalised losses rather than price alone. Use the maker's tested figures, or the [transformer efficiency calculator](/electrical/transformer-efficiency/), for a real unit.

## Sizing from measured demand

For an existing plant, measured data beats an estimated demand factor. A utility bill or a power analyser logging 15 minute demand gives the real peak in kVA, already including diversity and power factor. If the highest recorded demand is {meas:g} kVA, adding the {g*100:.0f}% growth margin gives {S_meas:.1f} kVA, so a 500 kVA unit still fits. Log for at least a full production cycle, including any seasonal peak such as summer chiller load.
''',
     faq_add=[('Why are transformers rated in kVA rather than kW?',
               'Transformer heating depends on current and voltage, not on how much of that current does real work. Copper loss follows current and core loss follows voltage, so the limit is apparent power in kVA, whatever the load power factor.')])

print('done')
