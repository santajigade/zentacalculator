"""Part B improve (2026-11-17): star-delta-transformation, boiling-point-elevation, heat-sink, hemocytometer.
Oldest batch (2026-10-27) pages below the current standard. Worked examples use each page's default inputs;
every number is computed here. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, BASE
U = '2026-11-17'


def set_related(cid, old, new):
    p = os.path.join(BASE, cid + '.mdx')
    s = open(p).read()
    a = 'related: [' + ', '.join(old) + ']'
    assert s.count(a) == 1, (cid, 'related line')
    for r in new:
        assert os.path.exists(os.path.join(BASE, r + '.mdx')), r
    open(p, 'w').write(s.replace(a, 'related: [' + ', '.join(new) + ']'))


# ---------------------------------------------------------------- Star-delta transformation
Rab, Rbc, Rca = 30.0, 60.0, 90.0
S = Rab + Rbc + Rca
Ra, Rb, Rc = Rab * Rca / S, Rab * Rbc / S, Rbc * Rca / S
P = Ra * Rb + Rb * Rc + Rc * Ra
back = (P / Rc, P / Ra, P / Rb)
# bridge: delta a-b-c on top, legs b-d = 40, c-d = 50; resistance seen from a to d
Lb, Lc = 40.0, 50.0
p1, p2 = Rb + Lb, Rc + Lc
Rpar = p1 * p2 / (p1 + p2)
Rad = Ra + Rpar
V = 12.0
I = V / Rad
Ib, Ic = I * p2 / (p1 + p2), I * p1 / (p1 + p2)
rows = ''
for d in ((10, 10, 10), (30, 60, 90), (100, 100, 50), (1, 1, 1000), (47, 220, 330), (1000, 2200, 4700)):
    s = sum(d)
    rows += f"| {d[0]:,} / {d[1]:,} / {d[2]:,} Ω | {d[0]*d[2]/s:,.2f} Ω | {d[0]*d[1]/s:,.2f} Ω | {d[1]*d[2]/s:,.2f} Ω |\n"

edit('electrical/star-delta-transformation', date=U, phrase='star-delta transformation calculator',
     title='Star-Delta Transformation Calculator (Delta to Star and Star to Delta)',
     description='Convert delta (Δ) resistances to an equivalent star (Y) network and back, with formulas, a bridge circuit worked example and a conversion table.',
     intro=("Some resistor and impedance networks cannot be reduced with series and parallel rules alone. This star-delta transformation calculator "
            "swaps a three-terminal delta for its equivalent star, or a star for its delta, as explained in this "
            "[star-delta transformation formula](https://www.instrumentationblog.in/star-delta-transformation-formula/) guide.\n\n"
            "Electrical students, test engineers and circuit designers use it to solve bridge networks, "
            "find per-phase values for delta loads and check hand calculations quickly."),
     body_add=f'''
## Checking the default conversion in reverse

Starting from the star values {Ra:g}, {Rb:g} and {Rc:g} Ω, the sum of pairwise products is {Ra:g} × {Rb:g} + {Rb:g} × {Rc:g} + {Rc:g} × {Ra:g} = **{P:,.0f} Ω²**. Dividing by the opposite star resistor returns the original delta:

- R<sub>ab</sub> = {P:,.0f} ÷ {Rc:g} = **{back[0]:g} Ω**
- R<sub>bc</sub> = {P:,.0f} ÷ {Ra:g} = **{back[1]:g} Ω**
- R<sub>ca</sub> = {P:,.0f} ÷ {Rb:g} = **{back[2]:g} Ω**

Running the conversion both ways like this is a quick way to catch a value typed into the wrong field.

## Worked example: solving an unbalanced bridge

Take the default delta ({Rab:g}, {Rbc:g} and {Rca:g} Ω) as the top half of a bridge, add {Lb:g} Ω from b to d and {Lc:g} Ω from c to d, and apply {V:g} V between a and d. No resistor pair is in series or parallel, so convert the delta to star first:

1. The star gives R<sub>a</sub> = {Ra:g} Ω in the feed, then two branches: {Rb:g} + {Lb:g} = {p1:g} Ω and {Rc:g} + {Lc:g} = {p2:g} Ω.
2. The branches are now in parallel: {p1:g} × {p2:g} ÷ ({p1:g} + {p2:g}) = **{Rpar:.3f} Ω**.
3. Total resistance a to d = {Ra:g} + {Rpar:.3f} = **{Rad:.3f} Ω**, so the supply current is {V:g} ÷ {Rad:.3f} = **{I*1000:.1f} mA**.
4. The current divides {Ib*1000:.1f} mA through the b branch and {Ic*1000:.1f} mA through the c branch.

## Delta to star conversion table

| R<sub>ab</sub> / R<sub>bc</sub> / R<sub>ca</sub> | R<sub>a</sub> | R<sub>b</sub> | R<sub>c</sub> |
|---|---|---|---|
{rows}
Notice that a delta with one very large resistor (the 1 / 1 / 1,000 Ω row) gives a star with one very small arm, which is why the transformation can turn an awkward network into a simple one.

## Practical notes

- In three-phase work, a balanced delta load of Z per phase behaves exactly like a star load of Z ÷ 3, so per-phase current and power can be found from line voltage ÷ √3.
- For AC networks with different phase angles, apply the same formulas with complex impedances; using magnitudes alone gives wrong answers.
- In measurement bridges, converting the ratio arms to star shows how lead and contact resistance add to the detector branch.

## Common mistakes

- **Mixing up which resistors touch a node.** R<sub>a</sub> uses the two delta resistors connected to terminal a (R<sub>ab</sub> and R<sub>ca</sub>), not R<sub>bc</sub>.
- **Dividing by the wrong resistor in star to delta.** Each delta resistor is divided by the star arm opposite to it, the one not connected to either of its terminals.
- **Losing the terminals.** The star centre is a new internal node; the three outer terminals must stay connected to the rest of the circuit exactly as before.
- **Treating the star centre as the neutral of a supply.** It is a mathematical node, and its voltage is not zero unless the network is balanced.
''',
     faq_add=[('Can a star-delta transformation be used to solve a Wheatstone bridge?',
               f'Yes. Convert one triangle of the bridge to a star and the rest becomes series and parallel. With the default 30, 60 and 90 Ω delta and legs of 40 and 50 Ω, the resistance from a to d is {Rad:.2f} Ω.')])

# ---------------------------------------------------------------- Boiling point elevation
Kb, i, m, Tb0 = 0.512, 2.0, 1.0, 100.0
dT = i * Kb * m
Tb = Tb0 + dT
gNaCl = m * 58.44 * 0.5  # grams in 500 g water for 1 mol/kg
R = 8.314
Kb_w = R * 373.15 ** 2 * 0.018015 / 40660
# molar mass from ebullioscopy: 10 g unknown in 200 g benzene, rise 0.80 K
mu, ws, dTu, Kbb = 10.0, 0.200, 0.80, 2.53
mol_u = dTu / Kbb
Mu = mu / (mol_u * ws)
srows = ''
for name, Kbs, bp in (('Water', 0.512, 100.0), ('Ethanol', 1.22, 78.4), ('Acetic acid', 3.07, 118.0), ('Benzene', 2.53, 80.1), ('Chloroform', 3.63, 61.2)):
    srows += f"| {name} | {bp:g} °C | {Kbs:g} | {Kbs*0.5:.3f} °C | {Kbs*1.0:.3f} °C |\n"
irows = ''
for name, ideal, real in (('Sucrose, glucose, urea', 1, '1.0'), ('NaCl, KCl', 2, 'about 1.9'), ('MgSO₄', 2, 'about 1.3'), ('CaCl₂, MgCl₂', 3, 'about 2.7'), ('FeCl₃', 4, 'about 3.4')):
    irows += f"| {name} | {ideal} | {real} |\n"

edit('chemistry/boiling-point-elevation', date=U, phrase='boiling point elevation calculator',
     title='Boiling Point Elevation Calculator (ΔTb = i·Kb·m)',
     description='Calculate the rise in boiling point from molality, van \'t Hoff factor and solvent Kb, with worked examples, solvent constants and molar mass checks.',
     intro=("Dissolving a solute raises a liquid's boiling point by an amount set by how many particles are dissolved, not by what they are. "
            "This boiling point elevation calculator applies ΔTb = i × Kb × m and gives the rise and the new boiling point.\n\n"
            "Chemistry students use it for colligative property problems, and lab chemists use it to estimate the molar mass of an unknown "
            "or to check how much a dissolved salt shifts a solvent's boiling point."),
     body_add=f'''
## Worked example with the default values

A 1 mol/kg solution of sodium chloride in water (i = {i:g}, K<sub>b</sub> = {Kb} °C·kg/mol):

- ΔT<sub>b</sub> = {i:g} × {Kb} × {m:g} = **{dT:.3f} °C**
- New boiling point = {Tb0:g} + {dT:.3f} = **{Tb:.2f} °C**

To make this solution, dissolve {gNaCl:.2f} g of NaCl (58.44 g/mol) in 500 g of water. Note that molality is per kilogram of solvent, so the water is weighed, not made up to a volume.

## Where Kb comes from

The ebullioscopic constant follows from the solvent's own properties: K<sub>b</sub> = R × T<sub>b</sub>² × M ÷ ΔH<sub>vap</sub>. For water, 8.314 × 373.15² × 0.018015 ÷ 40,660 = **{Kb_w:.3f} °C·kg/mol**, which matches the tabulated 0.512. Solvents with a high boiling point and a low heat of vaporisation per mole have large K<sub>b</sub> values.

## Solvent constants and the rise they give

| Solvent | Normal bp | K<sub>b</sub> (°C·kg/mol) | Rise at 0.5 mol/kg (i = 1) | Rise at 1 mol/kg (i = 1) |
|---|---|---|---|---|
{srows}
## Ideal and measured van 't Hoff factors

| Solute | Ideal i | Measured i (dilute, about 0.05 mol/kg) |
|---|---|---|
{irows}
Ion pairing makes real electrolytes behave as if they release fewer particles, so the ideal i overstates the rise, especially above about 0.1 mol/kg.

## Finding molar mass by ebullioscopy

10 g of an unknown non-electrolyte in 200 g of benzene raises the boiling point by {dTu:.2f} °C. The molality is {dTu:.2f} ÷ {Kbb} = {mol_u:.4f} mol/kg, so the moles dissolved are {mol_u:.4f} × {ws:g} = {mol_u*ws:.5f} mol and the molar mass is 10 ÷ {mol_u*ws:.5f} = **{Mu:.0f} g/mol**. Measure the rise with a Beckmann or digital thermometer reading to 0.01 °C, and record barometric pressure, because a small pressure change moves the boiling point more than the solute does.

## Common mistakes

- **Using molarity instead of molality.** K<sub>b</sub> is defined per kilogram of solvent; mol/L gives a small error in water and a larger one in dense or light solvents.
- **Dividing by the mass of solution.** Only the solvent mass goes in the denominator of molality.
- **Forgetting the van 't Hoff factor.** Salts split into ions; using i = 1 for NaCl halves the predicted rise.
- **Applying the formula to concentrated solutions.** The linear law is for dilute, ideal solutions; strong brines deviate noticeably.
- **Ignoring a volatile solute.** The formula assumes the solute does not evaporate; ethanol in water lowers, not raises, the boiling point.
''',
     faq_add=[('How do I find the van \'t Hoff factor from a boiling point measurement?',
               'Rearrange the formula: i = ΔTb ÷ (Kb × m). For example, a 0.10 mol/kg NaCl solution that boils 0.097 °C above pure water gives i = 0.097 ÷ (0.512 × 0.10) = 1.89, slightly below the ideal 2 because of ion pairing.')])
set_related('chemistry/boiling-point-elevation',
            ['chemistry/freezing-point-depression', 'chemistry/molality', 'chemistry/osmotic-pressure', 'chemistry/specific-heat'],
            ['chemistry/freezing-point-depression', 'chemistry/molality', 'chemistry/osmotic-pressure', 'chemistry/raoults-law'])

# ---------------------------------------------------------------- Heat sink
Ph, Tj, Ta, Rjc, Rcs = 10.0, 125.0, 40.0, 1.5, 0.5
Rt = (Tj - Ta) / Ph
Rsa = Rt - Rjc - Rcs
Rpick = 5.0
Tj_act = Ta + Ph * (Rjc + Rcs + Rpick)
Ts_act = Ta + Ph * Rpick
Tc_act = Ts_act + Ph * Rcs
Rmica = 1.2
Rsa_mica = Rt - Rjc - Rmica
hrows = ''
for p in (2, 5, 10, 15, 20, 30):
    r = (Tj - Ta) / p - Rjc - Rcs
    hrows += f"| {p} W | {(Tj-Ta)/p:.2f} °C/W | {r:.2f} °C/W |" + (" not possible |\n" if r <= 0 else f" {Ta + p*(Rjc+Rcs):.0f} °C |\n")

edit('electronics/heat-sink', date=U, phrase='heat sink calculator',
     title='Heat Sink Calculator (Required Thermal Resistance Rθsa)',
     description='Find the maximum heat sink thermal resistance for a MOSFET, transistor or regulator from power, junction and ambient temperatures, with a worked example.',
     intro=("Power transistors, MOSFETs and regulators turn part of their energy into heat, and too much heat shortens their life. "
            "This heat sink calculator finds the highest sink thermal resistance that keeps the junction below your design limit, "
            "as described in this [heat sink calculation](https://www.instrumentationblog.in/heat-sink-calculation/) guide.\n\n"
            "Electronics designers and repair technicians use it to choose a heat sink, compare insulating pads and "
            "decide early whether a design needs forced air cooling."),
     body_add=f'''
## Checking a chosen heat sink

With the default inputs the sink must be at most {Rsa:.1f} °C/W. Suppose you pick a profile rated **{Rpick:g} °C/W**. Working back up the thermal circuit at {Ph:g} W:

- Heat sink temperature = {Ta:g} + {Ph:g} × {Rpick:g} = **{Ts_act:.0f} °C**
- Case temperature = {Ts_act:.0f} + {Ph:g} × {Rcs:g} = **{Tc_act:.0f} °C**
- Junction temperature = {Tc_act:.0f} + {Ph:g} × {Rjc:g} = **{Tj_act:.0f} °C**, leaving {Tj-Tj_act:.0f} °C of margin below the {Tj:g} °C target.

If the drain tab must be insulated from the sink with a mica or silicone pad of about {Rmica:g} °C/W instead of {Rcs:g} °C/W, the allowed sink resistance falls to {Rt:.1f} − {Rjc:g} − {Rmica:g} = **{Rsa_mica:.1f} °C/W**.

## Required heat sink against power

For the default {Tj:g} °C junction target, {Ta:g} °C ambient, R<sub>θjc</sub> {Rjc:g} and R<sub>θcs</sub> {Rcs:g} °C/W:

| Power | Total allowed | Max R<sub>θsa</sub> | Junction with an ideal sink |
|---|---|---|---|
{hrows}
The last column is the junction temperature with an ideal (zero resistance) heat sink. Once it passes the target, no passive heat sink is enough.

## Measuring temperatures in practice

Fix a fine thermocouple to the device tab or to the sink right beside the package with a dab of thermal epoxy, run the circuit at full load until readings stop changing (often 20 to 40 minutes), and measure the air inside the enclosure, not the room. The junction temperature is then T<sub>case</sub> + P × R<sub>θjc</sub>. Measure the power from voltage and current, because datasheet loss estimates often miss switching losses.

## Common mistakes

- **Using room temperature as ambient.** Air inside a closed enclosure is often 10 to 20 °C warmer than the room, which can halve the allowed R<sub>θsa</sub>.
- **Reading R<sub>θja</sub> as the heat sink figure.** R<sub>θja</sub> is for the bare package with no heat sink and is not used once a sink is fitted.
- **Ignoring the insulating pad.** A pad can add more resistance than the device itself; include it in R<sub>θcs</sub>.
- **Trusting the catalogue figure at any power.** Natural convection ratings are quoted at a stated temperature rise and fin orientation; a horizontal sink or a smaller rise performs worse.
- **Forgetting other devices on the same sink.** Add all the power that flows into a shared heat sink before calculating its temperature.
''',
     faq_add=[('How do I calculate the junction temperature with a given heat sink?',
               f'Add up the thermal resistances and multiply by the power: Tj = Ta + P × (Rθjc + Rθcs + Rθsa). For 10 W, 40 °C ambient, 1.5 and 0.5 °C/W and a 5 °C/W sink, Tj = 40 + 10 × 7 = {Tj_act:.0f} °C.')])
set_related('electronics/heat-sink',
            ['electronics/mosfet-power-loss', 'electronics/ntc-thermistor', 'physics/heat-conduction', 'electronics/capacitor-lifetime', 'electrical/three-phase-motor-power', 'physics/ohms-law'],
            ['electronics/mosfet-power-loss', 'electronics/lm317', 'physics/heat-conduction', 'electronics/ntc-thermistor', 'electronics/capacitor-lifetime', 'electronics/buck-converter'])

# ---------------------------------------------------------------- Hemocytometer
cnt, sq, dil, vol = 180, 4, 2, 10.0
avg = cnt / sq
cml = avg * dil * 1e4
tot = cml * vol
dead = 20
viab = cnt / (cnt + dead) * 100
cv = 100 / math.sqrt(cnt)
lo, hi = cml * (1 - 1.96 / math.sqrt(cnt)), cml * (1 + 1.96 / math.sqrt(cnt))
seed = 2e5
vseed = seed / cml
wells = 6
vmix = wells * vseed * 1000
crows = ''
for n in (25, 50, 100, 200, 400, 800):
    crows += f"| {n} | {100/math.sqrt(n):.1f}% | ±{196/math.sqrt(n):.1f}% |\n"
trows = ''
for a in (10, 25, 45, 75, 100):
    trows += f"| {a} | {a*1e4:,.0f} | {a*2e4:,.0f} | {a*1e5:,.0f} |\n"

edit('biology/hemocytometer', date=U, phrase='hemocytometer cell count calculator',
     title='Hemocytometer Calculator (Cells per mL and Total Cell Count)',
     description='Calculate cells per mL and total cells from hemocytometer counts, squares counted and dilution, with viability, counting error and seeding examples.',
     intro=("A hemocytometer is a counting chamber with a grid of known volume, so the number of cells seen in its squares gives the cell "
            "concentration of a suspension. This hemocytometer cell count calculator turns your count into cells per mL and total cells.\n\n"
            "Cell culture technicians and biology students use it every time they passage cells, check viability with trypan blue "
            "or need the volume of suspension to seed plates and flasks."),
     body_add=f'''
## Worked example with the default values

{cnt} cells counted in {sq} large squares, mixed 1:1 with trypan blue (dilution {dil}), from a {vol:g} mL suspension:

- Average per square = {cnt} ÷ {sq} = **{avg:g} cells**
- Cells per mL = {avg:g} × {dil} × 10⁴ = **{cml:,.0f} cells/mL** ({cml:.1e})
- Total cells = {cml:,.0f} × {vol:g} = **{tot:,.0f} cells** ({tot:.1e})

If {dead} blue (dead) cells were also seen in the same squares, viability = {cnt} ÷ ({cnt} + {dead}) × 100 = **{viab:.0f}%**, and the {cnt} clear cells are the live count used above.

## How precise is a count?

Cells settle at random, so the count follows Poisson statistics and its relative standard deviation is 1 ÷ √N. Counting {cnt} cells gives about {cv:.1f}%, so the true default concentration lies roughly between {lo:,.0f} and {hi:,.0f} cells/mL (95%).

| Cells counted | Coefficient of variation | 95% range |
|---|---|---|
{crows}
Doubling the number of squares counted is the easiest way to tighten the result.

## Cells per mL by average count per square

| Average per large square | Dilution 1 | Dilution 2 (1:1 trypan) | Dilution 10 |
|---|---|---|---|
{trows}
## Seeding from the count

To seed {seed:,.0f} cells per well in a {wells} well plate from the default suspension, each well needs {seed:,.0f} ÷ {cml:,.0f} = **{vseed:.3f} mL** ({vseed*1000:.0f} µL). For all {wells} wells, take {vmix:.0f} µL and top up with medium to the final volume.

## Common mistakes

- **Forgetting the trypan blue dilution.** Equal volumes of cells and dye halve the concentration; leaving out the factor of 2 underestimates the culture by half.
- **Counting clumps as one cell.** Pipette gently but thoroughly before loading; clumps make counts low and uneven between squares.
- **Overfilling or underfilling the chamber.** Liquid that flows into the moats or a coverslip that is not seated changes the 0.1 mm depth the 10⁴ factor relies on.
- **Waiting too long before counting.** Trypan blue slowly stains live cells too, so count within about 5 minutes of mixing.
- **Mixing up large and small squares.** The 10⁴ factor is for the 1 mm² corner squares; the small central squares need a different factor.
''',
     faq_add=[('How accurate is a hemocytometer count?',
               f'The counting error is about 1 ÷ √N of the cells counted. Counting {cnt} cells gives roughly {cv:.1f}% relative error, while 50 cells gives about 14%, so aim for 100 to 300 cells in total.')])
set_related('biology/hemocytometer', ['biology/serial-dilution', 'biology/cell-doubling-time'],
            ['biology/serial-dilution', 'biology/cell-doubling-time', 'biology/centrifuge-rcf', 'biology/specific-growth-rate'])
print('done')
