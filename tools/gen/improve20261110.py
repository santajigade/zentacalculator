"""Improve pass (2026-11-10) for thin pages from the first batch (2026-10-27):
physics/coulombs-law, physics/gravitational-force, chemistry/nernst-equation, physics/snells-law.
Keyword-first titles, 120-160 char descriptions, intros with the "<topic> calculator" phrase,
worked examples and reference tables computed here, practical notes, re-checked FAQs and constants
(Coulomb constant updated to CODATA 2018). Slugs, categories and existing variable ids are unchanged (asserted).
Re-running regenerates the same files."""
import sys, os, re, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import yaml
from page import page, BASE
from ib import intro
U = '2026-11-10'
pi = math.pi
KE = 8.9875517862e9      # 1/(4π ε0), CODATA 2018
G = 6.6743e-11           # CODATA 2018
QE = 1.602176634e-19
ME, MP = 9.1093837015e-31, 1.67262192369e-27
A0 = 5.29177210903e-11
R_, F_ = 8.314462618, 96485.33212
C0 = 299792458.0
DONE = []

def ids_of(cid):
    fm = open(os.path.join(BASE, cid + '.mdx')).read().split('---')[1]
    d = yaml.safe_load(fm); return [v['id'] for v in d['variables']], d['category']

def W(cid, fm, body):
    cat, slug = cid.split('/')
    old_ids, old_cat = ids_of(cid)
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (cid, len(d))
    assert 'featured' not in fm
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    page(cat, slug, fm, body)
    new_ids, new_cat = ids_of(cid)
    assert new_cat == old_cat == cat, cid
    assert all(i in new_ids for i in old_ids), (cid, old_ids, new_ids)
    DONE.append(cid)

def sci(x, d=3):
    """scientific notation with superscript exponent, e.g. 1.98 × 10²⁰"""
    if x == 0: return '0'
    e = int(math.floor(math.log10(abs(x)))); m = x / 10 ** e
    if -3 <= e <= 4:
        return f"{x:,.{max(0, d - 1 - e)}f}" if e < d else f"{x:,.0f}"
    sup = str(e).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))
    return f"{m:.{d-1}f} × 10{sup}".replace('-', '−')

# ---------------------------------------------------------------- Coulomb's law
kq1, kq2, kr = 2.0, -3.0, 0.10
kF = KE * kq1 * 1e-6 * kq2 * 1e-6 / kr ** 2; kE1 = KE * kq1 * 1e-6 / kr ** 2; kU = KE * kq1 * 1e-6 * kq2 * 1e-6 / kr
kd_rows = ''
for rc in (1, 2, 5, 10, 20, 50, 100):
    r = rc / 100
    kd_rows += f"| {rc} cm | {KE*1e-12/r**2:.4g} N | {sci(KE*1e-18/r**2, 4)} N |\n"
km_rows = ''
for nm, er in (('Vacuum', 1.0), ('Air (dry, 20 °C)', 1.00059), ('Transformer oil', 2.2), ('Ethanol (25 °C)', 24.3), ('Water (20 °C)', 80.1)):
    km_rows += f"| {nm} | {er:g} | {KE*1e-12/0.01**2/er:.4g} N |\n"
kH = KE * QE ** 2 / A0 ** 2; kratio = KE * QE ** 2 / (G * ME * MP)
W('physics/coulombs-law', f'''
title: Coulomb's Law Calculator (Electric Force Between Charges)
description: Calculate the electrostatic force between two point charges with Coulomb's law, plus the electric field and potential energy, and solve for charge or distance.
category: physics
{intro("Electric charges push or pull on each other with a force that grows with the product of the charges and falls with the square of the distance between them. This Coulomb's law calculator gives that force for two point charges in vacuum or air, shows whether it is attractive or repulsive, and also returns the electric field of the first charge and the potential energy of the pair — or solves for the charge or distance needed for a given force.")}
keywords: [coulombs law calculator, coulomb's law calculator, electric force calculator, electrostatic force calculator, force between two charges, coulomb constant, point charge force]
updated: {U}
variables:
  - {{ id: q1, label: Charge 1 (q₁), suffix: µC, default: {kq1:g}, help: 'Use a minus sign for a negative charge. 1 µC = 10⁻⁶ C; 1 nC = 0.001 µC.' }}
  - {{ id: q2, label: Charge 2 (q₂), suffix: µC, default: {kq2:g} }}
  - {{ id: r, label: Distance between charges, family: length, unit: cm, imperialUnit: in, default: {kr*100:g}, min: 0 }}
  - {{ id: F, label: Force (negative = attraction), family: force, unit: N, imperialUnit: lbf }}
  - {{ id: E1, label: Electric field of charge 1 at distance r, suffix: N/C (V/m) }}
  - {{ id: U, label: Electric potential energy of the pair, family: energy, unit: J }}
equations:
  - F = 8.9875517862e9 * q1 * 1e-6 * q2 * 1e-6 / r^2
  - E1 = 8.9875517862e9 * q1 * 1e-6 / r^2
  - U = 8.9875517862e9 * q1 * 1e-6 * q2 * 1e-6 / r
faq:
  - q: What is Coulomb's law?
    a: The force between two point charges is F = k q₁ q₂ ÷ r², where k = 1 ÷ (4π ε₀) ≈ 8.988 × 10⁹ N·m²/C². Like charges repel and opposite charges attract, and the force acts along the line joining them.
  - q: What does a negative force mean?
    a: The charges have opposite signs, so the force is attractive. A positive result means the charges have the same sign and repel each other.
  - q: How does distance affect the electric force?
    a: The force falls with the square of the distance. Doubling the distance cuts the force to a quarter, and ten times the distance cuts it to one hundredth.
  - q: Does Coulomb's law work in water or oil?
    a: In a uniform insulating medium, divide the vacuum force by the relative permittivity εᵣ. Water (εᵣ ≈ 80) weakens the force between ions about 80 times, which is why salts dissolve in it. Air (εᵣ ≈ 1.0006) is practically the same as vacuum.
related: [physics/electric-field, physics/parallel-plate-capacitor, physics/gravitational-force, physics/force]
''', f'''
## How to use the Coulomb's law calculator

Enter the two **charges** in microcoulombs (use a minus sign for a negative charge) and the **distance** between their centres. The calculator gives the **force** in newtons — negative for attraction, positive for repulsion — the **electric field** that charge 1 produces at the position of charge 2, and the **potential energy** of the pair. To find the distance for a given force, enter the force and press × on Distance; the same works for either charge.

## Coulomb's law formula

<p class="formula">F = k q₁ q₂ ÷ r² &nbsp;·&nbsp; E = k q₁ ÷ r² &nbsp;·&nbsp; U = k q₁ q₂ ÷ r</p>

with k = 1 ÷ (4π ε₀) = 8.9875517862 × 10⁹ N·m²/C², charges in coulombs and r in metres. The formula is exact for point charges and for spheres with a uniform charge, measured between centres.

## Worked example

+{kq1:g} µC and {kq2:g} µC, {kr*100:g} cm apart:

- F = 8.988 × 10⁹ × ({kq1:g} × 10⁻⁶) × ({kq2:g} × 10⁻⁶) ÷ {kr:g}² = **{kF:.4f} N** — attractive, about the weight of a {abs(kF)/9.80665:.2f} kg mass
- Field of charge 1 at {kr*100:g} cm: E = 8.988 × 10⁹ × {kq1:g} × 10⁻⁶ ÷ {kr:g}² = **{sci(kE1, 4)} N/C**
- Potential energy: U = 8.988 × 10⁹ × ({kq1:g} × 10⁻⁶) × ({kq2:g} × 10⁻⁶) ÷ {kr:g} = **{kU:.4f} J** (negative: work is needed to pull them apart)

## Force versus distance

| Distance | Two 1 µC charges | Two 1 nC charges |
|---|---|---|
{kd_rows}
## Force in different materials

Two 1 µC charges 1 cm apart, surrounded by the material:

| Medium | Relative permittivity εᵣ | Force |
|---|---|---|
{km_rows}
## Electric force versus gravity

In a hydrogen atom the electron and proton, {A0*1e12:.1f} pm apart, attract each other with **{sci(kH, 3)} N**. The electric force between them is about **{sci(kratio, 2)}** times their gravitational attraction — gravity dominates on large scales only because matter is almost exactly neutral.

## Practical notes

- **1 coulomb is a huge static charge** — about 6.24 × 10¹⁸ electrons. Charges from rubbing or static build-up are usually nanocoulombs to a few microcoulombs.
- For charges spread over large or close conductors, the point-charge formula is only approximate; use the [electric field calculator](/physics/electric-field/) or a capacitance model instead.
- Electrostatic forces drive dust precipitators, laser printers, powder coating and the ESD that damages electronic parts.
''')

# ---------------------------------------------------------------- Gravitational force
gm1, gm2, gr = 5.972e24, 7.342e22, 384400e3
gF = G * gm1 * gm2 / gr ** 2; gg1 = G * gm1 / gr ** 2; gU = -G * gm1 * gm2 / gr
PAIRS = (('Earth–Moon', 5.972e24, 7.342e22, 384400e3, '384,400 km'), ('Sun–Earth', 1.989e30, 5.972e24, 149.6e9, '149.6 million km'),
         ('Person (70 kg) on Earth', 5.972e24, 70, 6371e3, '6,371 km'), ('Two people (70 kg each)', 70, 70, 1.0, '1 m'),
         ('Two 1 kg masses', 1, 1, 0.1, '10 cm'))
gp_rows = ''.join(f"| {nm} | {sci(a) if a >= 1e4 else f"{a:g}"} kg and {sci(b) if b >= 1e4 else f"{b:g}"} kg | {d} | {sci(G*a*b/r**2)} N |\n" for nm, a, b, r, d in PAIRS)
BODIES = (('Mercury', 3.3011e23, 2439.7e3), ('Venus', 4.8675e24, 6051.8e3), ('Earth', 5.972e24, 6371.0e3), ('Moon', 7.342e22, 1737.4e3),
          ('Mars', 6.4171e23, 3389.5e3), ('Jupiter', 1.8982e27, 69911e3), ('Saturn', 5.6834e26, 58232e3))
gb_rows = ''.join(f"| {nm} | {sci(M)} kg | {R/1e3:,.1f} km | {G*M/R**2:.3f} m/s² | {G*M*70/R**2:,.0f} N |\n" for nm, M, R in BODIES)
ga_rows = ''
for nm, h in (('Surface', 0), ('Airliner, 10 km', 10e3), ('Kármán line, 100 km', 100e3), ('ISS, 400 km', 400e3), ('GPS orbit, 20,200 km', 20200e3), ('Geostationary, 35,786 km', 35786e3)):
    g_ = G * 5.972e24 / (6371e3 + h) ** 2
    ga_rows += f"| {nm} | {g_:.4g} m/s² | {g_/(G*5.972e24/6371e3**2)*100:.1f}% |\n"
giss = (6371 / 6771) ** 2 * 100
W('physics/gravitational-force', f'''
title: Gravitational Force Calculator (Newton's Law of Gravitation)
description: Calculate the gravitational force between two masses with F = Gm₁m₂/r², plus the gravitational acceleration and potential energy — from people to planets.
category: physics
{intro("Every mass attracts every other mass with a force proportional to both masses and inversely proportional to the square of the distance between their centres. This gravitational force calculator applies Newton's law of universal gravitation to any two bodies, and also gives the gravitational acceleration the first mass produces at that distance and the potential energy of the pair. It solves for whichever value you leave blank.")}
keywords: [gravitational force calculator, newtons law of gravitation calculator, universal gravitation calculator, force of gravity between two objects, gravitational constant, gravitational acceleration, f = gmm/r2]
updated: {U}
variables:
  - {{ id: m1, label: Mass 1 (m₁), suffix: kg, default: {gm1:g}, min: 0, help: 'Scientific notation works: Earth = 5.972e24, Moon = 7.342e22, Sun = 1.989e30.' }}
  - {{ id: m2, label: Mass 2 (m₂), suffix: kg, default: {gm2:g}, min: 0 }}
  - {{ id: r, label: Distance between centres, family: length, unit: km, imperialUnit: mi, default: {gr/1e3:g}, min: 0 }}
  - {{ id: F, label: Gravitational force, family: force, unit: N, imperialUnit: lbf, min: 0 }}
  - {{ id: g1, label: Gravitational acceleration due to mass 1 at distance r, suffix: m/s², min: 0, decimals: 6 }}
  - {{ id: U, label: Gravitational potential energy (zero at infinity), family: energy, unit: J }}
equations:
  - F = 6.6743e-11 * m1 * m2 / r^2
  - g1 = 6.6743e-11 * m1 / r^2
  - U = -6.6743e-11 * m1 * m2 / r
faq:
  - q: What is Newton's law of universal gravitation?
    a: Every mass attracts every other mass with a force F = G m₁ m₂ ÷ r², where G = 6.6743 × 10⁻¹¹ N·m²/kg² and r is the distance between the centres of mass. The force on each body is equal and opposite.
  - q: What is the gravitational force between the Earth and the Moon?
    a: About {sci(gF)} N, using 5.972 × 10²⁴ kg, 7.342 × 10²² kg and the mean distance of 384,400 km. It varies by about 10–12% either way over the Moon's elliptical orbit.
  - q: Why don't I feel the gravity of people near me?
    a: Because G is tiny. Two 70 kg people 1 m apart attract each other with about {sci(G*70*70)} N, roughly the weight of a few hundredths of a milligram.
  - q: Which distance do I use?
    a: The distance between the centres of mass, not between the surfaces. For an object on the Earth's surface, use the Earth's radius (about 6,371 km); for a satellite, add its altitude.
related: [physics/weight, physics/escape-velocity, physics/orbital-period, physics/coulombs-law]
''', f'''
## How to use the gravitational force calculator

Enter the two **masses** in kilograms (scientific notation such as 5.972e24 is accepted) and the **distance between their centres**. The defaults are the Earth and the Moon. The calculator gives the **force** on each body, the **gravitational acceleration** that mass 1 produces at that distance (the "g" felt by mass 2) and the **potential energy** of the pair. Leave any one input blank and enter the force to solve for it.

## Gravitational force formula

<p class="formula">F = G m₁ m₂ ÷ r² &nbsp;·&nbsp; g = G m₁ ÷ r² &nbsp;·&nbsp; U = −G m₁ m₂ ÷ r</p>

with G = 6.6743 × 10⁻¹¹ N·m²/kg² (CODATA 2018). The formula is exact for point masses and for spherically symmetric bodies, measured between centres.

## Worked example

The Earth ({sci(gm1, 4)} kg) and the Moon ({sci(gm2, 4)} kg) at their mean distance of {gr/1e3:,.0f} km:

- F = 6.6743 × 10⁻¹¹ × {sci(gm1, 4)} × {sci(gm2, 4)} ÷ ({sci(gr, 4)} m)² = **{sci(gF, 4)} N**
- Earth's gravitational acceleration at the Moon: g = 6.6743 × 10⁻¹¹ × {sci(gm1, 4)} ÷ ({sci(gr, 4)})² = **{gg1:.6f} m/s²** — about 1/{9.80665/gg1:,.0f} of g at the surface
- Potential energy U = −G m₁ m₂ ÷ r = **{sci(gU, 4)} J**

## Gravitational force examples

| Pair | Masses | Distance | Force |
|---|---|---|---|
{gp_rows}
## Surface gravity of the planets

Computed with g = G M ÷ R² from the mean radius (ignoring rotation). The last column is the weight of a 70 kg person.

| Body | Mass | Mean radius | Surface gravity | Weight of 70 kg |
|---|---|---|---|---|
{gb_rows}
## Gravity above the Earth

| Height | g | Share of surface value |
|---|---|---|
{ga_rows}
Astronauts on the International Space Station are still pulled by about {giss:.0f}% of surface gravity — they float because they are in free fall around the Earth, not because gravity is absent.

## Practical notes

- **Weight on Earth** is usually calculated with the standard g = 9.80665 m/s²; the actual value ranges from about 9.78 m/s² at the equator to 9.83 m/s² at the poles because of the Earth's rotation and shape — see the [weight calculator](/physics/weight/).
- For orbits, the same law gives the [orbital period](/physics/orbital-period/) and the [escape velocity](/physics/escape-velocity/).
- G was first measured by Henry Cavendish in 1798 with a torsion balance; it is still known only to about 22 parts per million, far less precisely than the other fundamental constants.
''')

# ---------------------------------------------------------------- Nernst equation
nE0, nn, nT, nQ = 1.10, 2, 298.15, 0.01
nk = R_ * nT / (nn * F_); nE = nE0 - nk * math.log(nQ); nS = math.log(10) * R_ * nT / (nn * F_) * 1000
ndG = -nn * F_ * nE / 1000; nK = math.exp(nn * F_ * nE0 / (R_ * nT))
nq_rows = ''
for Q in (1e-4, 1e-2, 0.1, 1, 10, 100, 1e4):
    dE = -R_ * 298.15 / (2 * F_) * math.log(Q) * 1000
    dE = 0.0 if abs(dE) < 1e-9 else dE
    nq_rows += f"| {Q:g} | {'0.0' if dE == 0 else f'{dE:+.1f}'} mV |\n"
ns_rows = ''
for Tc in (0, 10, 20, 25, 30, 37, 50, 80):
    s1 = math.log(10) * R_ * (Tc + 273.15) / F_ * 1000
    ns_rows += f"| {Tc} °C | {s1:.2f} mV | {s1/2:.2f} mV | {s1/3:.2f} mV |\n"
nmem = R_ * 310.15 / F_ * math.log(5 / 140) * 1000
W('chemistry/nernst-equation', f'''
title: Nernst Equation Calculator (Cell & Electrode Potential)
description: Calculate cell or electrode potential under non-standard conditions with the Nernst equation, plus the Nernst slope, Gibbs energy and equilibrium constant.
category: chemistry
{intro("The Nernst equation gives the voltage of an electrode or electrochemical cell when the concentrations are not standard, and it explains how a [pH sensor works](https://www.instrumentationblog.in/what-is-ph-sensor-how-does-it-work/) — and why its slope matters when [troubleshooting pH sensors](https://www.instrumentationblog.in/ph-sensor-troubleshooting/). This Nernst equation calculator returns the cell potential from E°, the electrons transferred, the temperature and the reaction quotient, together with the Nernst slope per decade, the Gibbs free energy and the equilibrium constant.")}
keywords: [nernst equation calculator, nernst potential calculator, cell potential calculator, electrode potential calculator, reaction quotient, nernst slope, emf calculator]
updated: {U}
variables:
  - {{ id: E0, label: Standard potential (E°), suffix: V, default: {nE0:g} }}
  - {{ id: n, label: Electrons transferred (n), default: {nn}, min: 1 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, imperialUnit: F, default: {nT-273.15:g}, min: 0 }}
  - {{ id: Q, label: Reaction quotient (Q), default: {nQ:g}, min: 1e-30, help: 'Products over reactants, each raised to its stoichiometric coefficient; solids and pure liquids count as 1.' }}
  - {{ id: E, label: Cell potential (E), suffix: V, decimals: 4 }}
  - {{ id: dE, label: Shift from the standard potential (E − E°), suffix: mV, decimals: 2 }}
  - {{ id: S, label: Nernst slope per tenfold change in Q, suffix: mV/decade, decimals: 3 }}
  - {{ id: dG, label: Gibbs free energy change ΔG = −nFE, suffix: kJ/mol, decimals: 2 }}
  - {{ id: K, label: Equilibrium constant K (from E°), min: 0 }}
  - {{ id: lgK, label: log₁₀ K, decimals: 3 }}
equations:
  - E = E0 - 8.314462618 * T / (n * 96485.33212) * ln(Q)
  - dE = (E - E0) * 1000
  - S = 2.302585093 * 8.314462618 * T / (n * 96485.33212) * 1000
  - dG = -n * 96485.33212 * E / 1000
  - K = exp(n * 96485.33212 * E0 / (8.314462618 * T))
  - lgK = n * 96485.33212 * E0 / (2.302585093 * 8.314462618 * T)
faq:
  - q: What is the Nernst equation?
    a: E = E° − (RT ÷ nF) ln Q, where R = 8.314 J/(mol·K), T is the absolute temperature, n the number of electrons transferred, F = 96,485 C/mol and Q the reaction quotient. It gives the electrode or cell potential when concentrations are not 1 mol/L.
  - q: What is the simplified form of the Nernst equation at 25 °C?
    a: E = E° − (0.05916 V ÷ n) log₁₀ Q. Each tenfold change in Q shifts the potential by 59.16 ÷ n mV at 25 °C.
  - q: What happens at equilibrium?
    a: The cell potential falls to zero and Q equals the equilibrium constant K, so E° = (RT ÷ nF) ln K and ΔG° = −nFE° = −RT ln K. A large positive E° means a very large K — the reaction goes essentially to completion.
  - q: How is the Nernst equation used in pH meters?
    a: A glass pH electrode behaves as a hydrogen-ion electrode with n = 1, so its potential changes by about 59.16 mV per pH unit at 25 °C. The slope rises with temperature (61.5 mV at 37 °C), which is why pH meters have temperature compensation, and a calibrated slope well below about 95% of theoretical indicates an ageing electrode.
related: [chemistry/cell-potential, chemistry/gibbs-free-energy, chemistry/ph, chemistry/equilibrium-constant]
''', f'''
## How to use the Nernst equation calculator

Enter the **standard potential** E° of the cell or half-cell, the number of **electrons transferred** in the balanced reaction, the **temperature** and the **reaction quotient** Q. The calculator gives the cell potential E, its shift from E°, the Nernst slope (millivolts per tenfold change in Q), the Gibbs free energy of the reaction at these conditions and the equilibrium constant implied by E°. To find the Q at which the cell reaches a given voltage, enter E and press × on Q.

## The Nernst equation

<p class="formula">E = E° − (RT ÷ nF) ln Q = E° − (2.303 RT ÷ nF) log₁₀ Q</p>

<p class="formula">ΔG = −nFE &nbsp;·&nbsp; K = exp(nFE° ÷ RT)</p>

with R = 8.314462618 J/(mol·K) and F = 96,485.33212 C/mol. At 25 °C, 2.303RT/F = 59.16 mV. Strictly, Q uses activities; for dilute solutions concentrations in mol/L are a good approximation.

## Worked example: Daniell cell

Zn | Zn²⁺ (0.01 mol/L) ∥ Cu²⁺ (1 mol/L) | Cu, with E° = {nE0:g} V and n = {nn}, at 25 °C, so Q = [Zn²⁺] ÷ [Cu²⁺] = {nQ:g}:

- RT ÷ nF = 8.314 × {nT:g} ÷ ({nn} × 96,485) = **{nk*1000:.3f} mV**
- E = {nE0:g} − {nk:.6f} × ln({nQ:g}) = {nE0:g} + {-nk*math.log(nQ):.5f} = **{nE:.4f} V** (a shift of {(nE-nE0)*1000:+.2f} mV)
- Nernst slope = 2.303 × {nk*1000:.3f} = **{nS:.3f} mV per decade**
- ΔG = −{nn} × 96,485 × {nE:.4f} ÷ 1000 = **{ndG:.2f} kJ/mol** (spontaneous)
- K = exp({nn} × 96,485 × {nE0:g} ÷ (8.314 × {nT:g})) ≈ **{sci(nK, 3)}** (log₁₀ K = {math.log10(nK):.3f}) — the reaction goes to completion

## How Q changes the potential (n = 2, 25 °C)

| Q | E − E° |
|---|---|
{nq_rows}
## Nernst slope versus temperature

| Temperature | n = 1 (e.g. pH, Ag⁺) | n = 2 (e.g. Cu²⁺, Zn²⁺) | n = 3 (e.g. Fe³⁺/Fe) |
|---|---|---|---|
{ns_rows}
## Membrane potentials

In physiology the Nernst equation gives the equilibrium potential of an ion across a cell membrane, E = (RT ÷ zF) ln(c_out ÷ c_in). For potassium, about 140 mmol/L inside and 5 mmol/L outside at 37 °C, E<sub>K</sub> = **{nmem:.1f} mV**.

## Practical notes

- **Sign convention:** write Q for the cell reaction as written (oxidation at the anode on the left). If E comes out negative, the reaction runs spontaneously in the reverse direction.
- **pH electrodes** read about 59.16 mV per pH at 25 °C; a two-buffer calibration measures the actual slope, and values of roughly 95–102% of theoretical are normal for a healthy electrode.
- Ion-selective electrodes (fluoride, ammonium, nitrate) and ORP probes follow the same equation, so they also need temperature compensation and periodic slope checks.
''')

# ---------------------------------------------------------------- Snell's law
sn1, st1, sn2 = 1.0003, 30.0, 1.333
st2 = math.degrees(math.asin(sn1 * math.sin(math.radians(st1)) / sn2)); stc = math.degrees(math.asin(min(sn1, sn2) / max(sn1, sn2)))
sdv = st1 - st2; sv2 = C0 / sn2
MAT = (('Vacuum', 1.0), ('Air (20 °C, 1 atm)', 1.0003), ('Water (20 °C)', 1.333), ('Ethanol', 1.361), ('Acrylic (PMMA)', 1.49),
       ('Crown glass (BK7)', 1.517), ('Flint glass', 1.62), ('Sapphire', 1.77), ('Diamond', 2.417))
sm_rows = ''.join(f"| {nm} | {n:g} | {C0/n/1e8:.4f} × 10⁸ m/s | " + (f"{math.degrees(math.asin(1.0003/n)):.1f}°" if n > 1.0003 else '—') + " |\n" for nm, n in MAT)
sa_rows = ''
for t in (0, 10, 20, 30, 40, 50, 60, 70, 80, 89):
    cells = [f"{math.degrees(math.asin(1.0003*math.sin(math.radians(t))/n)):.1f}°" for n in (1.333, 1.517, 2.417)]
    sa_rows += f"| {t}° | " + ' | '.join(cells) + " |\n"
sw_rows = ''
for t in (10, 20, 30, 40, 45, 48, 50, 60):
    s = 1.333 * math.sin(math.radians(t)) / 1.0003
    sw_rows += f"| {t}° | " + (f"{math.degrees(math.asin(s)):.1f}°" if s <= 1 else 'total internal reflection') + " |\n"
W('physics/snells-law', f'''
title: Snell's Law Calculator (Angle of Refraction & Critical Angle)
description: Find the angle of refraction, a refractive index or the critical angle for total internal reflection when light passes between two media, using Snell's law.
category: physics
{intro("Light bends when it crosses from one transparent material into another because its speed changes. This Snell's law calculator uses n₁ sin θ₁ = n₂ sin θ₂ to find the angle of refraction — or the angle of incidence or a refractive index — and also gives the critical angle for total internal reflection at the interface, the deviation of the ray and the speed of light in the second medium.")}
keywords: [snells law calculator, snell's law calculator, refraction calculator, angle of refraction calculator, critical angle calculator, total internal reflection, refractive index calculator]
updated: {U}
variables:
  - {{ id: n1, label: Refractive index of the first medium (n₁), default: {sn1:g}, min: 1, help: 'Vacuum 1, air 1.0003, water 1.333, crown glass 1.517, diamond 2.417.' }}
  - {{ id: t1, label: Angle of incidence (θ₁, from the normal), family: angle, unit: deg, default: {st1:g}, min: 0, max: 1.5708 }}
  - {{ id: n2, label: Refractive index of the second medium (n₂), default: {sn2:g}, min: 1 }}
  - {{ id: t2, label: Angle of refraction (θ₂, from the normal), family: angle, unit: deg, min: 0, max: 1.5708 }}
  - {{ id: tc, label: Critical angle at this interface (inside the denser medium), family: angle, unit: deg, min: 0 }}
  - {{ id: dv, label: Deviation of the ray (θ₁ − θ₂), family: angle, unit: deg }}
  - {{ id: v2, label: Speed of light in the second medium, family: velocity, unit: ms, min: 0 }}
equations:
  - n1 * sin(t1) = n2 * sin(t2)
  - tc = asin(min(n1, n2) / max(n1, n2))
  - dv = t1 - t2
  - v2 = 299792458 / n2
faq:
  - q: What is Snell's law?
    a: n₁ sin θ₁ = n₂ sin θ₂, where n is the refractive index of each medium and θ is measured from the normal (the line perpendicular to the surface). Light bends towards the normal when it enters a medium with a higher index and away from it when it enters a lower one.
  - q: What is the critical angle?
    a: The angle of incidence inside the denser medium at which the refracted ray just grazes the surface (θ₂ = 90°). sin θc = n₂ ÷ n₁. Beyond it no light escapes and the ray is totally internally reflected — about 48.6° for water to air and 41.3° for crown glass to air.
  - q: Why does the calculator show no solution?
    a: Going from a denser to a less dense medium at an angle larger than the critical angle, n₁ sin θ₁ ÷ n₂ is greater than 1, so no refracted ray exists — this is total internal reflection.
  - q: What is the refractive index of water and glass?
    a: About 1.333 for water at 20 °C and 1.517 for common crown glass (BK7), measured with yellow sodium light (589 nm). The index is slightly higher for blue light and lower for red, which is why prisms split white light.
related: [physics/thin-lens, physics/wavelength-frequency, physics/speed-of-sound, math/right-triangle-trig]
''', f'''
## How to use the Snell's law calculator

Enter the **refractive index** of the material the light comes from, the **angle of incidence** measured from the normal, and the **refractive index** of the material it enters. The calculator gives the **angle of refraction**, the **critical angle** of that interface, the **deviation** of the ray and the **speed of light** in the second medium. Fill in any three of n₁, θ₁, n₂ and θ₂ to solve for the fourth — for example, measure both angles to find an unknown refractive index.

## Snell's law formula

<p class="formula">n₁ sin θ₁ = n₂ sin θ₂ &nbsp;·&nbsp; sin θ<sub>c</sub> = n<sub>low</sub> ÷ n<sub>high</sub> &nbsp;·&nbsp; v = c ÷ n</p>

with c = 299,792,458 m/s. The refractive index is the ratio of the speed of light in vacuum to its speed in the material.

## Worked example

Light passes from air (n₁ = {sn1:g}) into water (n₂ = {sn2:g}) at {st1:g}° to the normal:

- sin θ₂ = {sn1:g} × sin {st1:g}° ÷ {sn2:g} = **{sn1*math.sin(math.radians(st1))/sn2:.4f}**, so θ₂ = **{st2:.2f}°**
- The ray bends {sdv:.2f}° towards the normal
- Critical angle for light leaving the water: sin θ<sub>c</sub> = {sn1:g} ÷ {sn2:g}, θ<sub>c</sub> = **{stc:.2f}°**
- Speed of light in water = 299,792,458 ÷ {sn2:g} = **{sv2:,.0f} m/s**

## Refraction from air into water, glass and diamond

| Angle of incidence | Water (1.333) | Crown glass (1.517) | Diamond (2.417) |
|---|---|---|---|
{sa_rows}
Even at grazing incidence, light entering water bends to less than the critical angle — which is why a diver looking up sees the whole sky compressed into a cone (Snell's window).

## Light leaving water into air

| Angle in the water | Angle in the air |
|---|---|
{sw_rows}
## Refractive indices and critical angles (to air)

| Material | n (589 nm) | Speed of light | Critical angle to air |
|---|---|---|---|
{sm_rows}
## Practical notes

- **Optical fibres** guide light by total internal reflection between a core and a slightly lower-index cladding; the numerical aperture is NA = √(n<sub>core</sub>² − n<sub>clad</sub>²).
- **Refractometers** measure the critical angle of a sample against a prism to find its refractive index — the basis of sugar (°Brix) and concentration measurement.
- **Dispersion:** n changes with wavelength, so quote the index at a wavelength (usually 589 nm) when precision matters.
- Part of the light is always reflected at the interface; at normal incidence the reflected fraction is ((n₁ − n₂) ÷ (n₁ + n₂))², about 4% for air to glass.
''')

print(len(DONE), 'improved:', ' '.join(DONE))
