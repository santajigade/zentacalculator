"""Improve pass (2026-11-19) for three thin pages from the first batch (2026-10-27):
math/ellipse, electrical/ups-sizing, chemistry/freezing-point-depression.
(math/weighted-average was considered but is a featured page, which inplace.edit refuses to touch.)
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples built from the calculator defaults, reference tables computed here,
practical notes, common mistakes, dash-free rewrites of edited text and better related ids.
Slug, category, variables, equations and published are unchanged (asserted by inplace.edit).
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, BASE
U = '2026-11-19'
EN, EM = chr(0x2013), chr(0x2014)


def set_related(cid, old, new):
    p = os.path.join(BASE, cid + '.mdx')
    s = open(p).read()
    a = 'related: [' + ', '.join(old) + ']'
    assert s.count(a) == 1, (cid, 'related line')
    for r in new:
        assert os.path.exists(os.path.join(BASE, r + '.mdx')), r
    open(p, 'w').write(s.replace(a, 'related: [' + ', '.join(new) + ']'))


# ---------------------------------------------------------------- Ellipse
def ram1(a, b):
    return math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))


def ram2(a, b):
    h = ((a - b) / (a + b)) ** 2
    return math.pi * (a + b) * (1 + 3 * h / (10 + math.sqrt(4 - 3 * h)))


def exact(a, b, n=200000):
    # numerical integral of 4a * int_0^{pi/2} sqrt(1 - e^2 sin^2 t) dt (midpoint rule)
    e2 = 1 - (b / a) ** 2
    s = 0.0
    for k in range(n):
        t = (k + 0.5) * (math.pi / 2) / n
        s += math.sqrt(1 - e2 * math.sin(t) ** 2)
    return 4 * a * s * (math.pi / 2) / n


a, b = 10.0, 6.0
A = math.pi * a * b
s1 = 3 * (a + b)
s2 = math.sqrt((3 * a + b) * (a + 3 * b))
P = math.pi * (s1 - s2)
ec = math.sqrt(1 - b * b / (a * a))
fc = math.sqrt(a * a - b * b)
Pex = exact(a, b)
Pnaive = 2 * math.pi * math.sqrt((a * a + b * b) / 2)
Pavg = math.pi * (a + b)
erows = ''
for bb in (10, 8, 6, 4, 2, 1, 0.1):
    pe = exact(10, bb)
    erows += (f"| {bb:g} | {pe:.3f} | {ram1(10, bb):.3f} | {abs(ram1(10, bb) - pe) / pe * 100:.4f}% |"
              f" {math.pi * (10 + bb):.3f} | {abs(math.pi * (10 + bb) - pe) / pe * 100:.2f}% |\n")
# oval table: 1.8 m x 1.0 m top, edge banding
TL, TW = 1.8, 1.0
ta, tb = TL / 2, TW / 2
tA = math.pi * ta * tb
tP = ram1(ta, tb)
rect = TL * TW
# orbit: Earth
ae, ee = 149.598e6, 0.0167
peri, aph = ae * (1 - ee), ae * (1 + ee)

edit('math/ellipse', date=U, phrase='ellipse calculator',
     title='Ellipse Calculator: Area, Perimeter, Eccentricity and Foci',
     description='Find the area, perimeter, eccentricity and focus distance of an ellipse from its semi-axes, with worked steps and accuracy tables for oval shapes.',
     intro=("An ellipse is a closed curve that looks like a stretched circle, set by its semi-major axis a and semi-minor axis b. "
            "This ellipse calculator gives the area, the perimeter by Ramanujan's approximation, the eccentricity and the distance from the centre to each focus.\n\n"
            "Students use it for geometry and orbit problems, while carpenters, landscapers and fabricators use it to size oval tables, flower beds, tanks and gaskets."),
     replace=[('about 0.017 ' + EM + ' almost a circle.', 'about 0.017, almost a circle.')],
     body_add=f'''
## Worked example with the default values

For a = {a:g} cm and b = {b:g} cm:

1. Area = π × {a:g} × {b:g} = **{A:.2f} cm²**
2. Perimeter: 3(a + b) = {s1:g}; √((3a + b)(a + 3b)) = √({3*a+b:g} × {a+3*b:g}) = {s2:.4f}; P = π × ({s1:g} − {s2:.4f}) = **{P:.2f} cm**
3. Eccentricity = √(1 − {b:g}² ÷ {a:g}²) = √({1 - b*b/(a*a):.2f}) = **{ec:.4f}**
4. Centre to each focus = √({a:g}² − {b:g}²) = √{a*a-b*b:g} = **{fc:.2f} cm**, so the foci are {2*fc:.0f} cm apart.

The exact perimeter, found by numerical integration of the elliptic integral, is {Pex:.4f} cm, so Ramanujan's result is off by only {abs(P-Pex):.5f} cm.

## How accurate are the perimeter shortcuts?

Exact perimeter (numerical integral) for a = 10 compared with Ramanujan's first formula, used here, and the rough shortcut π(a + b):

| b | Exact | Ramanujan | Error | π(a + b) | Error |
|---|---|---|---|---|---|
{erows}
Ramanujan's formula stays within a small fraction of a percent even for a very flat ellipse, while π(a + b) underestimates by several percent once b drops below about half of a. For extreme shapes his second formula, π(a + b)[1 + 3h ÷ (10 + √(4 − 3h))] with h = ((a − b) ÷ (a + b))², is better still: at b = 1 it gives {ram2(10, 1):.4f} against the exact {exact(10, 1):.4f}.

## Practical example: an oval dining table

A table top {TL:g} m long and {TW:g} m wide has a = {ta:g} m and b = {tb:g} m. Its area is π × {ta:g} × {tb:g} = **{tA:.3f} m²**, about {tA/rect*100:.1f}% of the {rect:.2f} m² rectangle it is cut from (always π ÷ 4). The edge banding needed is the perimeter, **{tP:.3f} m**; order a little extra for the joint and trimming. The same steps size an oval rug, a pond liner outline or an elliptical manway gasket.

## Ellipses in orbits

With the Sun at one focus, a planet's closest distance is a(1 − e) and its farthest is a(1 + e). For Earth, a = 149.6 million km and e = {ee}, giving about {peri/1e6:.1f} million km at perihelion and {aph/1e6:.1f} million km at aphelion.

## Common mistakes

- **Entering full axes instead of semi-axes.** A 1.8 m by 1.0 m oval has a = 0.9 m and b = 0.5 m; using the full widths gives four times the area.
- **Swapping a and b.** a must be the longer semi-axis. With b larger than a, the eccentricity and focus distance become meaningless.
- **Using 2π√((a² + b²) ÷ 2) as exact.** That common shortcut gives {Pnaive:.2f} cm for the default ellipse, {abs(Pnaive-Pex)/Pex*100:.2f}% high; it is only an estimate.
- **Treating any oval as an ellipse.** Egg shapes and racetrack ovals (two semicircles joined by straight lines) have different area and perimeter formulas.
''',
     faq_add=[('Why does the area of an ellipse have a simple formula but the perimeter does not?',
               'Area is a circle of radius a squashed by the factor b ÷ a, so it scales to π a b exactly. The perimeter needs an elliptic integral, which has no closed form, so approximations such as Ramanujan\'s are used.'),
              ('How do I find the foci of an ellipse?',
               f'Each focus lies on the major axis at c = √(a² − b²) from the centre. For a = 10 cm and b = 6 cm, c = {fc:.0f} cm, so the foci are {2*fc:.0f} cm apart.')])
set_related('math/ellipse', ['math/circle', 'math/arc-length', 'math/sphere', 'math/polygon'],
            ['math/circle', 'math/arc-length', 'physics/orbital-period', 'math/rectangle', 'math/torus'])

# ---------------------------------------------------------------- UPS sizing
Pl, pf, m = 4000.0, 0.9, 0.25
Pw = Pl * (1 + m)
S = Pw / pf / 1000
stds = [1, 2, 3, 5, 6, 10, 15, 20, 30, 40, 60, 80, 100, 120, 160, 200]
pick = next(x for x in stds if x >= S - 1e-9)
load_pct = Pl / (pick * 1000 * pf) * 100
# office rack example
rack = [('1U servers', 4, 350), ('24-port switch', 2, 45), ('Firewall', 1, 60), ('Storage array', 1, 500), ('Monitor and KVM', 1, 40)]
rack_W = sum(n * w for _, n, w in rack)
rack_rows = ''.join(f"| {nm} | {n} | {w:,} W | {n*w:,} W |\n" for nm, n, w in rack)
rS = rack_W * 1.25 / 0.9 / 1000
rS08 = rack_W * 1.25 / 0.8 / 1000
rpick = next(x for x in stds if x >= rS)
srows = ''
for w in (500, 1000, 2000, 4000, 8000, 15000, 30000):
    k = []
    for p in (0.8, 0.9, 1.0):
        k.append(w * 1.25 / p / 1000)
    pk = next(x for x in stds if x >= k[1])
    srows += f"| {w:,} W | {w*1.25/1000:.2f} kW | {k[0]:.2f} kVA | {k[1]:.2f} kVA | {k[2]:.2f} kVA | {pk} kVA |\n"
# runtime energy hint for 15 min at default load
E15 = Pl * 0.25 / 0.9  # Wh from battery at 90% inverter efficiency

edit('electrical/ups-sizing', date=U, phrase='ups size calculator',
     title='UPS Size Calculator: kVA and kW Rating for Your Load',
     description='Find the UPS kVA and kW rating for your load from total watts, UPS power factor and a growth margin, with worked examples and a standard size table.',
     intro=("A UPS has two limits, its kVA (apparent power) and its kW (real power), and the load must stay within both. "
            "This UPS size calculator adds a growth margin to your load and divides by the UPS output power factor to give the minimum kVA and kW rating. "
            "See [UPS capacity (kVA) calculation](https://www.instrumentationblog.in/ups-capacity-kva-calculation/).\n\n"
            "IT managers, electrical contractors and panel designers use it to choose a UPS for server racks, offices, control panels and home setups."),
     replace=[
         ('For more background, read [How to Calculate Battery Backup Time](https://www.instrumentationblog.in/calculate-battery-backup-time/).\n\n', ''),
         ('| Desktop PC with monitor | 150' + EN + '300 W |', '| Desktop PC with monitor | 150 to 300 W |'),
         ('| Laptop | 45' + EN + '100 W |', '| Laptop | 45 to 100 W |'),
         ('| Network switch (24-port) | 30' + EN + '60 W |', '| Network switch (24-port) | 30 to 60 W |'),
         ('| Wi-Fi router | 10' + EN + '20 W |', '| Wi-Fi router | 10 to 20 W |'),
         ('| 1U server | 250' + EN + '500 W |', '| 1U server | 250 to 500 W |'),
         ('| Laser printer (printing) | 400' + EN + '800 W |', '| Laser printer (printing) | 400 to 800 W |'),
         ('| PLC control panel | 100' + EN + '500 W |', '| PLC control panel | 100 to 500 W |'),
         ('| LED lighting per room | 30' + EN + '60 W |', '| LED lighting per room | 30 to 60 W |'),
         ('small UPSs ' + EM + ' their inrush', 'small UPSs, because their inrush'),
         ('network racks ' + EM + ' handles voltage swings', 'network racks; handles voltage swings'),
     ],
     body_add=f'''
## Worked example with the default values

A {Pl/1000:g} kW load, a UPS output power factor of {pf} and a {m*100:.0f}% margin:

- Design load = {Pl:,.0f} × (1 + {m:g}) = **{Pw/1000:.1f} kW**, the minimum watt rating
- Minimum kVA = {Pw:,.0f} ÷ {pf} ÷ 1,000 = **{S:.2f} kVA**

The next standard size is **{pick} kVA**, which at PF {pf} is rated {pick*pf:.1f} kW. The present {Pl/1000:g} kW load then uses {load_pct:.0f}% of the UPS, leaving room for growth.

## Example: sizing for a server rack

| Equipment | Qty | Each | Total |
|---|---|---|---|
{rack_rows}
The rack draws **{rack_W:,} W**. With a 25% margin and a PF 0.9 UPS the minimum is {rS:.2f} kVA, so a {rpick} kVA unit fits. An older PF 0.8 UPS would need {rS08:.2f} kVA for the same load, which shows why the power factor rating matters as much as the kVA figure.

## UPS size by load (25% margin)

| Load | Design kW | PF 0.8 | PF 0.9 | PF 1.0 | Size at PF 0.9 |
|---|---|---|---|---|---|
{srows}
## Practical notes

- **Measure where you can.** A clamp meter or a PDU with metering shows real running watts, which are often 50 to 70% of nameplate figures for IT equipment.
- **Check inrush and start-up loads.** Motors, compressors, laser printers and transformers can draw several times their running power for a moment; a UPS overloaded at switch-on drops to bypass or shuts down.
- **Three-phase UPS.** For units above about 10 kVA, also check that the load is balanced across phases so no single phase exceeds one third of the rating.
- **Battery is separate.** At the default {Pl/1000:g} kW load, 15 minutes of backup needs roughly {E15/1000:.2f} kWh from the battery allowing for 90% inverter efficiency; size it with the [battery backup calculator](/everyday-life/inverter-battery-backup/).

## Common mistakes

- **Adding VA ratings of power supplies.** A PC power supply labelled 500 W rarely draws 500 W; use measured or typical input power, or the sum is far too high.
- **Sizing by kVA alone.** A 6 kVA UPS rated at PF 0.8 supplies only 4.8 kW, less than a 5 kW load even though the kVA looks ample.
- **Running at 100% from day one.** A fully loaded UPS has no room for growth, runs hotter and gives shorter battery runtime.
- **Ignoring redundancy.** For N+1 designs, the load must fit on the remaining modules after one fails, not on the total installed capacity.
''',
     faq_replace=[
         ('How do I calculate UPS size?', 'How do I calculate UPS size?',
          f'Add up the load in watts, add a 20 to 30% margin for growth, and divide by the UPS power factor. 4 kW × 1.25 ÷ 0.9 = {S:.2f} kVA, so choose a {pick} kVA UPS.'),
         ('How much margin should I add?', 'How much margin should I add?',
          '20 to 30% is common. It allows for future loads and keeps the UPS from running near full load, which improves reliability and battery runtime.'),
     ],
     faq_add=[('Can I run a UPS at full load?',
               'It can carry its rated load, but continuous operation near 100% leaves no room for inrush or new equipment and shortens battery runtime. Planning for 70 to 80% loading is a common rule.')])
set_related('electrical/ups-sizing',
            ['electrical/ct-burden', 'electrical/generator-size', 'everyday-life/inverter-battery-backup', 'electrical/kva-to-kw', 'electrical/amps-to-watts', 'everyday-life/electricity-cost'],
            ['everyday-life/inverter-battery-backup', 'electrical/battery-bank-size', 'electrical/kva-to-kw', 'electrical/generator-size', 'electrical/amps-to-watts', 'other/battery-life'])

# ---------------------------------------------------------------- Freezing point depression
Kf, i, mo, T0 = 1.86, 2.0, 0.5, 0.0
dT = i * Kf * mo
Tf = T0 - dT
g_nacl = mo * 58.44
# molar mass by cryoscopy: 2.50 g unknown in 50.0 g benzene, dT 1.28
gu, ks, Kb, dTb = 2.50, 0.0500, 5.12, 1.28
mu = dTb / Kb
Mu = gu / (mu * ks)
# antifreeze ethylene glycol 30% by mass ideal
rows_eg = ''
for wpct in (10, 20, 30, 40):
    gEG = wpct / (100 - wpct) * 1000
    mol = gEG / 62.07
    rows_eg += f"| {wpct}% | {mol:.2f} | {-1.86*mol:.1f} °C |\n"
solv = [('Water', 1.86, 0.0), ('Benzene', 5.12, 5.5), ('Acetic acid', 3.90, 16.6), ('Cyclohexane', 20.0, 6.5), ('Camphor', 37.7, 179.0)]
srows = ''.join(f"| {n} | {k:g} | {t:g} °C | {k*0.1:.3f} °C | {t - k*0.1:.2f} °C |\n" for n, k, t in solv)

edit('chemistry/freezing-point-depression', date=U, phrase='freezing point depression calculator',
     title='Freezing Point Depression Calculator (ΔTf = i Kf m)',
     description='Calculate how far a dissolved solute lowers a solvent\'s freezing point with ΔTf = i × Kf × m, with Kf values, worked examples and salt and glycol tables.',
     intro=("Dissolving a solute in a solvent lowers its freezing point by an amount that depends on how many particles are dissolved, not on what they are. "
            "This freezing point depression calculator applies ΔTf = i × Kf × m for water, benzene, cyclohexane and other solvents.\n\n"
            "Chemistry students use it for colligative property problems and molar mass by cryoscopy, and it helps with de-icing, antifreeze and ice cream work."),
     replace=[
         ('| NaCl, KCl | 2 | 1.8' + EN + '1.9 |', '| NaCl, KCl | 2 | 1.8 to 1.9 |'),
         ('| CaCl₂, MgCl₂ | 3 | 2.5' + EN + '2.7 |', '| CaCl₂, MgCl₂ | 3 | 2.5 to 2.7 |'),
     ],
     body_add=f'''
## Worked example with the default values

Water (K<sub>f</sub> = {Kf} °C·kg/mol), i = {i:g} for NaCl and a molality of {mo} mol/kg, which is about {g_nacl:.1f} g of NaCl per kg of water:

- ΔT<sub>f</sub> = {i:g} × {Kf} × {mo} = **{dT:.3f} °C**
- New freezing point = {T0:g} − {dT:.2f} = **{Tf:.2f} °C**

Using the measured i of about 1.85 for NaCl at this concentration gives a depression nearer {1.85*Kf*mo:.2f} °C, slightly less than the ideal figure.

## Worked example: molar mass by cryoscopy

{gu:.2f} g of an unknown non-electrolyte (i = 1) dissolved in {ks*1000:.1f} g of benzene lowers its freezing point by {dTb} °C:

1. Molality m = ΔT<sub>f</sub> ÷ K<sub>f</sub> = {dTb} ÷ {Kb} = **{mu:.4f} mol/kg**
2. Moles of solute = {mu:.4f} × {ks:.4f} kg = {mu*ks:.5f} mol
3. Molar mass = {gu:.2f} ÷ {mu*ks:.5f} = **{Mu:.0f} g/mol**

Solvents with a large K<sub>f</sub>, such as camphor or cyclohexane, give bigger, easier to measure depressions, which is why they are chosen for this method.

## Effect of 0.1 mol/kg of a non-electrolyte in each solvent

| Solvent | K<sub>f</sub> (°C·kg/mol) | Normal freezing point | ΔT<sub>f</sub> | New freezing point |
|---|---|---|---|---|
{srows}
## Ethylene glycol antifreeze (ideal estimate)

| Glycol by mass | Molality | Ideal freezing point |
|---|---|---|
{rows_eg}
Real mixtures freeze lower than this at higher concentrations (a 40% mix reaches about −24 °C) because glycol solutions deviate from ideal behaviour, so use the coolant maker's chart for engine protection.

## Common mistakes

- **Using molarity instead of molality.** The formula needs moles per kilogram of solvent, not per litre of solution.
- **Forgetting the van 't Hoff factor.** Salts split into ions; NaCl gives about twice the depression of sugar at the same molality.
- **Entering the new freezing point as ΔT<sub>f</sub>.** ΔT<sub>f</sub> is a positive drop; the new freezing point is the normal value minus it.
- **Picking the wrong K<sub>f</sub>.** K<sub>f</sub> belongs to the solvent, not the solute; switching from water to benzene almost triples the effect.
- **Applying it to concentrated brines.** Ion pairing lowers the effective i, so the ideal result overstates the depression above about 1 mol/kg.
''',
     faq_replace=[
         ('Why does salt melt ice on roads?', 'Why does salt melt ice on roads?',
          'Salt dissolves in the thin film of water on ice and lowers its freezing point, so the ice melts below 0 °C. Rock salt works down to about −10 °C in practice; calcium chloride works at lower temperatures.'),
     ],
     faq_add=[('What is the Kf of water?',
               'The cryoscopic constant of water is 1.86 °C·kg/mol, so each mole of dissolved particles per kilogram of water lowers the freezing point by about 1.86 °C.')])
set_related('chemistry/freezing-point-depression',
            ['chemistry/boiling-point-elevation', 'chemistry/molality', 'chemistry/osmotic-pressure', 'chemistry/molarity'],
            ['chemistry/boiling-point-elevation', 'chemistry/molality', 'chemistry/osmotic-pressure', 'chemistry/raoults-law', 'chemistry/moles'])
print('done')
