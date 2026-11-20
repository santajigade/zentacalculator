"""Improve pass (2026-11-20) for three thin pages from the first batch (2026-10-27):
electrical/transformer-turns-ratio, electronics/boost-converter, biology/protein-concentration-a280.
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples built from the calculator defaults, reference tables computed here,
practical notes, common mistakes, dash-free rewrites of edited text, one data fix (insulin
extinction coefficient now includes its three cystines) and better related ids.
Slug, category, variables, equations and published are unchanged (asserted by inplace.edit).
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, BASE
U = '2026-11-20'
EN, EM = chr(0x2013), chr(0x2014)


def set_related(cid, old, new):
    p = os.path.join(BASE, cid + '.mdx')
    s = open(p).read()
    a = 'related: [' + ', '.join(old) + ']'
    assert s.count(a) == 1, (cid, 'related line')
    for r in new:
        assert os.path.exists(os.path.join(BASE, r + '.mdx')), r
    open(p, 'w').write(s.replace(a, 'related: [' + ', '.join(new) + ']'))


# ---------------------------------------------------------------- Transformer turns ratio
Vp, Np, Ns, Is = 230.0, 1000.0, 52.0, 5.0
a = Np / Ns
Vs = Vp / a
Ip = Is / a
VA = Vs * Is
# common single-phase ratios with 1,000 primary turns at 230 V (ideal, no load)
rrows = ''
for vs in (6, 9, 12, 18, 24, 48, 110):
    ra = 230 / vs
    ns = 1000 / ra
    rrows += f"| 230 V to {vs} V | {ra:.3f} | {ns:.1f} | 1 A secondary draws {1/ra*1000:.1f} mA |\n"
# distribution transformer 11 kV / 433 V Dyn11 with off-circuit taps
VLp, VLs = 11000.0, 433.0
Vph_s = VLs / math.sqrt(3)
aph = VLp / Vph_s
trows = ''
for t in (5.0, 2.5, 0.0, -2.5, -5.0):
    # tap raises primary turns by t%, supply held at 11 kV
    vs_out = VLs / (1 + t / 100)
    trows += f"| {t:+.1f}% | {aph*(1+t/100):.2f} | {vs_out:.1f} V |\n"
# no-load voltage with 3% regulation design allowance
reg = 0.03
Vs_nl = Vs * (1 + reg)
Ns_comp = Ns * (1 + reg)

edit('electrical/transformer-turns-ratio', date=U, phrase='transformer turns ratio calculator',
     title='Transformer Turns Ratio Calculator: Secondary Voltage and Current',
     description='Find a transformer turns ratio, secondary voltage and primary current from winding turns or voltages, with worked examples, tap and vector group tables.',
     intro=("The turns ratio of a transformer, Np divided by Ns, sets how much it steps voltage down or up, and current changes the opposite way. "
            "This transformer turns ratio calculator gives the ratio, secondary voltage and primary current; see the [turns ratio and secondary voltage](https://www.instrumentationblog.in/transformer-turns-ratio-secondary-voltage/) guide.\n\n"
            "Electricians, panel builders and students use it to check control and supply transformers, and test engineers compare it with the turns ratio reading from [transformer routine tests](https://www.instrumentationblog.in/transformer-routine-and-type-tests/)."),
     replace=[('Fill any consistent set ' + EM + ' for example, both voltages', 'Fill any consistent set: for example, both voltages'),
              ('(regulation, typically 2' + EN + '5%)', '(regulation, typically 2% to 5%)')],
     body_add=f'''
## Worked example with the default values

The defaults are a **{Vp:g} V primary with {Np:,.0f} turns**, a **{Ns:g} turn secondary** and a **{Is:g} A load**:

1. Turns ratio a = {Np:,.0f} ÷ {Ns:g} = **{a:.3f}**
2. Secondary voltage Vs = {Vp:g} ÷ {a:.3f} = **{Vs:.2f} V**
3. Primary current Ip = {Is:g} ÷ {a:.3f} = **{Ip:.3f} A**
4. Power check: {Vs:.2f} V × {Is:g} A = {VA:.1f} VA on the secondary, and {Vp:g} V × {Ip:.3f} A = {Vp*Ip:.1f} VA on the primary, equal as they must be for an ideal transformer.

A real 12 V winding is usually given about 3% extra turns so that it still delivers 12 V on full load. Here that means {Ns_comp:.1f}, rounded to 54 turns, and the no-load voltage then rises to around {Vs_nl:.1f} V with the original 52 turns.

## Common single-phase ratios

Ideal ratios for a 230 V primary wound with 1,000 turns:

| Transformer | Turns ratio | Secondary turns | Primary current |
|---|---|---|---|
{rrows}
## Taps on a distribution transformer

An {VLp/1000:g} kV/{VLs:g} V Dyn11 unit has a secondary phase voltage of {VLs:g} ÷ √3 = {Vph_s:.1f} V, so the phase turns ratio is {aph:.2f}. Off-circuit taps on the HV winding change that ratio. With the supply held at exactly 11 kV, each tap gives:

| HV tap | Phase turns ratio | LV line voltage |
|---|---|---|
{trows}
Raising the HV tap adds primary turns and so lowers the secondary voltage. When the incoming supply is high, the operator moves to a plus tap to bring the LV back to nominal.

## How the turns ratio is measured

A transformer turns ratio (TTR) tester applies a low AC voltage, typically 8 V to 100 V, to the HV winding and measures the voltage induced on the LV winding with a bridge or precision voltmeter. It reports the ratio, the phase angle deviation and the excitation current for each tap and each phase. IEC 60076-1 allows a ratio deviation of 0.5% of the declared ratio (or a tenth of the impedance voltage, whichever is smaller) at the principal tap. A wrong ratio on one phase points to shorted turns or a tap changer contact fault.

## Common mistakes

- **Mixing line and phase voltages.** On a Dy or Yd transformer the winding ratio differs from the line voltage ratio by √3, as the table above shows.
- **Measuring the ratio on load.** Regulation lowers the secondary voltage under load, so a ratio taken from loaded voltages reads a few percent high.
- **Forgetting the current goes the other way.** A 19:1 step-down transformer draws about one nineteenth of the secondary current from the primary, not 19 times more.
- **Using the ratio for a DC supply.** A transformer only works on AC; DC through the primary just heats the winding and saturates the core.
- **Ignoring magnetising current.** Even with no load the primary draws a small current to magnetise the core, so a very light load gives a primary current above Is ÷ a.
''',
     faq_add=[('Does the turns ratio change with frequency?',
               'No. The ratio is fixed by the windings, so the voltage ratio holds at any frequency the core is designed for. Running a 50 Hz transformer at a lower frequency with the same voltage raises the core flux and can saturate it.'),
              ('How many turns do I need for a 12 V secondary from 230 V?',
               f'In the ideal case Ns = Np × 12 ÷ 230. With 1,000 primary turns that is {1000*12/230:.1f} turns, and about 3% extra (54 turns) is usually added to cover the voltage drop on full load.')])
set_related('electrical/transformer-turns-ratio',
            ['electrical/transformer-current', 'electrical/transformer-efficiency', 'electrical/transformer-short-circuit', 'physics/ohms-law'],
            ['electrical/transformer-current', 'electrical/transformer-size', 'electrical/autotransformer', 'electrical/line-phase-voltage', 'electrical/transformer-efficiency'])

# ---------------------------------------------------------------- Boost converter
Vi, Vo, Io, eta, f, r, dV = 5.0, 12.0, 0.5, 0.9, 500e3, 0.30, 0.05
D = 1 - Vi * eta / Vo
Ii = Vo * Io / (Vi * eta)
dI = r * Ii
L = Vi * D / (f * dI)
Ipk = Ii * (1 + r / 2)
C = Io * D / (f * dV)
Pin = Vi * Ii
Ploss = Pin - Vo * Io
esr = 0.010
dV_esr = Ipk * esr
brows = ''
for vo in (6, 9, 12, 15, 24):
    d = 1 - Vi * eta / vo
    ii = vo * Io / (Vi * eta)
    ll = Vi * d / (f * r * ii)
    cc = Io * d / (f * dV)
    brows += f"| {vo} V | {d*100:.1f}% | {ii:.3f} A | {ll*1e6:.1f} µH | {ii*(1+r/2):.3f} A | {cc*1e6:.1f} µF |\n"
# Li-ion 3.7 V to 5 V at 1 A, 92%, 1 MHz, 40% ripple
vi2, vo2, io2, e2, f2, r2 = 3.7, 5.0, 1.0, 0.92, 1e6, 0.4
d2 = 1 - vi2 * e2 / vo2
ii2 = vo2 * io2 / (vi2 * e2)
l2 = vi2 * d2 / (f2 * r2 * ii2)
pk2 = ii2 * (1 + r2 / 2)
vi3 = 3.0
d3 = 1 - vi3 * e2 / vo2
ii3 = vo2 * io2 / (vi3 * e2)

edit('electronics/boost-converter', date=U, phrase='boost converter calculator',
     title='Boost Converter Calculator: Duty Cycle, Inductor and Capacitor',
     description='Design a boost DC-DC converter: find duty cycle, input current, inductor value, peak switch current and output capacitance, with worked examples.',
     intro=("A boost converter steps a DC voltage up, for example from a 5 V USB rail to 12 V, by storing energy in an inductor while a switch is on and releasing it to the output when it turns off. "
            "This boost converter calculator gives the duty cycle, input current, inductance, peak switch current and minimum output capacitance.\n\n"
            "Electronics designers and hobbyists use it to choose parts before simulation; see the [boost converter working principle](https://www.instrumentationblog.in/boost-converter-working-principle/)."),
     replace=[('use 15' + EN + '22 µH', 'use 15 to 22 µH'),
              ('by itself ' + EM + ' current flows', 'by itself: current flows')],
     faq_replace=[('How high can a boost converter step up?', 'How high can a boost converter step up?',
                   'Practically about 5 to 8 times. Above that the duty cycle approaches 90%, the switch and diode losses rise sharply and the control loop becomes hard to stabilise, so a flyback or coupled inductor design is used instead.')],
     body_add=f'''
## Worked example with the default values

The defaults boost **{Vi:g} V to {Vo:g} V at {Io:g} A**, with {eta*100:.0f}% efficiency, {f/1e3:.0f} kHz switching, {r*100:.0f}% inductor ripple and {dV*1000:.0f} mV allowed output ripple:

1. Duty cycle D = 1 − ({Vi:g} × {eta:g}) ÷ {Vo:g} = **{D*100:.1f}%**
2. Input current Ii = ({Vo:g} × {Io:g}) ÷ ({Vi:g} × {eta:g}) = **{Ii:.3f} A**
3. Ripple ΔI = {r:g} × {Ii:.3f} = {dI:.2f} A, so L = ({Vi:g} × {D:.3f}) ÷ ({f:,.0f} × {dI:.2f}) = **{L*1e6:.2f} µH**
4. Peak switch current = {Ii:.3f} × (1 + {r:g} ÷ 2) = **{Ipk:.3f} A**
5. Minimum output capacitance C = ({Io:g} × {D:.3f}) ÷ ({f:,.0f} × {dV:g}) = **{C*1e6:.1f} µF**

The input power is {Pin:.2f} W for {Vo*Io:.0f} W out, so {Ploss:.2f} W is lost as heat in the switch, diode and inductor. A capacitor with {esr*1000:.0f} mΩ ESR adds about {Ipk:.2f} × {esr:g} = {dV_esr*1000:.0f} mV of ripple on top of the capacitive part, which is why low ESR ceramics are preferred at the output.

## Design values for different output voltages

Same {Vi:g} V input, {Io:g} A load, {eta*100:.0f}% efficiency, {f/1e3:.0f} kHz and {r*100:.0f}% ripple:

| Output | Duty cycle | Input current | Inductance | Peak current | Min. C |
|---|---|---|---|---|---|
{brows}
The higher the step-up, the larger the duty cycle and the input current. At 24 V the input current is already {24*Io/(Vi*eta):.2f} A for a 12 W load, and the peak current, not the average, sets the switch and inductor ratings.

## Practical example: a Li-ion cell to 5 V

Boosting a {vi2:g} V cell to {vo2:g} V at {io2:g} A with 92% efficiency at 1 MHz and 40% ripple gives D = {d2*100:.1f}%, an input current of {ii2:.2f} A, L = {l2*1e6:.2f} µH and a peak of {pk2:.2f} A. Design for the end of discharge, not the nominal voltage: at {vi3:g} V the duty cycle rises to {d3*100:.1f}% and the input current to {ii3:.2f} A, so the inductor saturation rating should cover about {ii3*(1+r2/2):.1f} A.

## Choosing the parts

- **Inductor:** pick the next standard value at or above the result and check the saturation current against the peak at the lowest input voltage.
- **Output capacitor:** ceramic capacitors lose much of their capacitance under DC bias; a 22 µF 25 V X5R part may give only 8 µF to 10 µF at 12 V, so check the derating curve.
- **Diode or synchronous switch:** a Schottky diode rated above the output voltage with low forward drop; above a few amps a synchronous MOSFET saves more power.
- **Switch:** rated for the output voltage plus ringing, typically at least 1.3 times Vo.

## Common mistakes

- **Taking the ripple percentage of the output current.** The inductor carries the input current, so the ripple is a percentage of Ii, which is much larger than Io.
- **Designing at nominal input voltage only.** The worst case for current is the lowest input voltage; the worst case for output voltage stress is the highest.
- **Expecting short-circuit protection.** The input is connected to the output through the inductor and diode even with the switch off, so an output short pulls current straight from the source.
- **Ignoring discontinuous mode.** At light load the inductor current falls to zero each cycle and the duty cycle formula above no longer holds.
- **Skipping the input capacitor.** The input current ripple still needs a local ceramic capacitor close to the inductor and switch.
''',
     faq_add=[('Why is my boost converter output lower than the formula predicts?',
               'Usually the efficiency is lower than assumed, the inductor is saturating, or the controller has reached its maximum duty cycle. Measure the input current: if it is much higher than Vo × Io ÷ (Vi × η), losses are higher than expected.'),
              ('Can a boost converter produce an output below its input?',
               'No. With the switch off the input feeds the output through the inductor and diode, so the output never falls below about the input voltage minus a diode drop. Use a buck-boost or SEPIC converter when the output must be both above and below the input.')])
set_related('electronics/boost-converter',
            ['electronics/instrumentation-amplifier-gain', 'electronics/buck-converter', 'electronics/inductor-energy', 'electronics/pwm-duty-cycle', 'electronics/capacitor-energy'],
            ['electronics/buck-converter', 'electronics/buck-boost-converter', 'electronics/inductor-energy', 'electronics/mosfet-power-loss', 'electronics/pwm-duty-cycle'])

# ---------------------------------------------------------------- Protein concentration A280
A, eps, mw, l = 0.8, 43824.0, 66463.0, 1.0
um = A / (eps * l) * 1e6
mg = um * mw / 1e6
e01 = eps / mw  # absorbance of 1 mg/mL
# 1:10 dilution and microvolume path
df = 10
mg_df = mg * df
l_mv = 0.1
A_mv = 0.8 * 0.1  # same undiluted 12.13 mg/mL? computed below
A_mv = mg_df * e01 * l_mv
prow = ''
for av in (0.1, 0.2, 0.4, 0.8, 1.0, 1.5):
    c_um = av / eps * 1e6
    prow += f"| {av:g} | {c_um:.2f} µM | {c_um*mw/1e6:.3f} mg/mL | {av/(37970/14313):.3f} mg/mL |\n"
# insulin: 4 Tyr, 0 Trp, 3 cystines
eps_ins = 4 * 1490 + 3 * 125
ins = eps_ins / 5808
# lysozyme check: 6 Trp, 3 Tyr, 4 cystines
eps_lys = 6 * 5500 + 3 * 1490 + 4 * 125

edit('biology/protein-concentration-a280', date=U, phrase='protein concentration calculator',
     title='Protein Concentration Calculator (A280): mg/mL and µM',
     description='Find protein concentration in µM and mg/mL from A280 absorbance using the extinction coefficient, molecular weight and path length, with BSA examples.',
     intro=("Proteins absorb ultraviolet light at 280 nm because of their tryptophan and tyrosine residues, so one absorbance reading and the extinction coefficient give the amount of protein. "
            "This protein concentration calculator applies the Beer-Lambert law to report molar and mass concentration.\n\n"
            "Biochemists, protein purification labs and core facilities use it to check yields after a column, set up enzyme assays and load gels with a known amount."),
     replace=[('## Example ' + EM + ' BSA', '## Example: BSA'),
              ('| Insulin | 5,808 | 5,960 | 1.03 |', f'| Insulin | 5,808 | {eps_ins:,} | {ins:.2f} |'),
              ('| A280 | about 0.1' + EN + '100 mg/mL |', '| A280 | about 0.1 to 100 mg/mL |'),
              ('| Bradford | 1' + EN + '1,500 µg/mL |', '| Bradford | 1 to 1,500 µg/mL |'),
              ('| BCA | 20' + EN + '2,000 µg/mL |', '| BCA | 20 to 2,000 µg/mL |')],
     body_add=f'''
## Worked example with the default values

The defaults are BSA read at **A280 = {A:g}** in a **{l:g} cm** cuvette, with ε = {eps:,.0f} M⁻¹cm⁻¹ and MW = {mw:,.0f} Da:

1. Molar concentration c = {A:g} ÷ ({eps:,.0f} × {l:g}) = {A/eps:.4e} M = **{um:.2f} µM**
2. Mass concentration = {um:.2f} µM × {mw:,.0f} g/mol ÷ 10⁶ = **{mg:.3f} mg/mL**

The absorbance of a 1 mg/mL solution, often written A₂₈₀(0.1%), is ε ÷ MW = {e01:.3f}, so dividing the reading by {e01:.3f} gives the same {mg:.3f} mg/mL directly.

## Diluted and microvolume readings

If that reading of {A:g} came from a 1 in {df} dilution, the stock is {mg:.3f} × {df} = **{mg_df:.2f} mg/mL**. Microvolume spectrophotometers avoid the dilution by using a short path: the same stock on a 0.1 mm (0.01 cm) pedestal reads about {mg_df*e01*0.01:.3f}, and on a 1 mm path {A_mv:.2f}. Always enter the true path length, or a normalised 1 cm value if the instrument already converts it.

## A280 to concentration for BSA and lysozyme

| A280 (1 cm) | BSA (µM) | BSA (mg/mL) | Lysozyme (mg/mL) |
|---|---|---|---|
{prow}
The same absorbance means very different amounts of protein: lysozyme is rich in tryptophan, so it absorbs about {(37970/14313)/e01:.1f} times more per milligram than BSA. Using a generic factor of 1 A per mg/mL would overstate BSA by about {(1/e01-1)*100:.0f}% here.

The sequence formula above reproduces the table values: lysozyme has 6 Trp, 3 Tyr and 4 cystines, giving 6 × 5,500 + 3 × 1,490 + 4 × 125 = {eps_lys:,} M⁻¹cm⁻¹, and insulin has 4 Tyr and 3 cystines, giving {eps_ins:,}.

## Practical notes

- Blank the instrument with the exact buffer the protein is in; imidazole, some detergents and reducing agents absorb near 280 nm.
- Keep readings between about 0.1 and 1.0 for a standard spectrophotometer; dilute stronger samples.
- Read A320 or A340 as well. Absorbance there comes from light scattered by aggregates, and subtracting it gives a better A280.
- Use the ε for the protein state you have: values computed with all cysteines reduced are slightly lower than those that count disulfide bonds.

## Common mistakes

- **Forgetting the dilution factor.** The calculator gives the concentration in the cuvette; multiply by the dilution to get the stock.
- **Using the extinction coefficient of the wrong construct.** His tags, GFP fusions or missing domains change ε and MW, so compute them from the actual sequence.
- **Reading cloudy samples.** Aggregates scatter light and raise A280, so spin or filter the sample first.
- **Ignoring nucleic acid contamination.** DNA and RNA absorb at 280 nm too; an A260/A280 ratio well above 0.6 means the A280 result is too high.
- **Mixing up M⁻¹cm⁻¹ and mL·mg⁻¹cm⁻¹.** A mass extinction coefficient near 1 entered in the molar box gives a concentration tens of thousands of times too high.
''',
     faq_add=[('What is the difference between the molar and mass extinction coefficient?',
               f'The molar value ε is in M⁻¹cm⁻¹ and gives molarity. The mass value, A₂₈₀ of a 1 mg/mL solution, equals ε ÷ MW: {e01:.3f} for BSA and {37970/14313:.2f} for lysozyme. Either gives the same mg/mL result.'),
              ('Can I use A280 for a protein mixture such as cell lysate?',
               'Only roughly. A mixture has no single extinction coefficient and lysates contain nucleic acids, so a dye assay such as Bradford or BCA with a standard curve is more reliable.')])
set_related('biology/protein-concentration-a280',
            ['biology/hemocytometer', 'biology/dna-concentration', 'chemistry/beer-lambert', 'biology/protein-molecular-weight'],
            ['chemistry/beer-lambert', 'biology/protein-molecular-weight', 'biology/dna-concentration', 'chemistry/dilution', 'chemistry/molarity'])

print('done')
