"""Improve pass (2026-11-26): chemistry/gibbs-free-energy, chemistry/half-life and chemistry/boyles-law
(thin pages from the first batch). The originally named pages (electronics/led-resistor, physics/ideal-gas-law,
physics/speed-distance-time) are featured and were improved earlier, so the next non-featured backlog pages
were taken. New 120-160 char descriptions, two-paragraph intros with the "<topic> calculator" phrase,
second worked examples, reference tables computed here, practical notes, common mistakes and new FAQs.
Slug, category, variables, equations, related and published are unchanged (asserted by inplace.edit).
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, drop_backlog
U = '2026-11-26'
MINUS = chr(0x2212)
R = 8.314462618
F = 96485.33212


def m_(x, d=1):
    s = f"{x:,.{d}f}"
    return s.replace('-', MINUS)


def sci(x, d=3):
    a, b = f"{x:.{d-1}e}".split('e')
    return f"{a} × 10<sup>{int(b)}</sup>".replace('-', MINUS)


# ======================================================================= Gibbs free energy
dH, dS, Tc = -92.2, -198.7, 25.0
T = Tc + 273.15
dG = dH - T * dS / 1000
assert abs(dG - (-32.96)) < 0.01
Tx = dH * 1000 / dS
K25 = math.exp(-dG * 1000 / (R * T))
g_rows = ''
for tc in (25, 100, 200, 300, 400, 450, 500):
    tk = tc + 273.15
    g = dH - tk * dS / 1000
    k = math.exp(-g * 1000 / (R * tk))
    g_rows += f"| {tc} °C | {tk:.2f} K | {m_(g, 1)} kJ/mol | {sci(k)} |\n"
g450 = dH - (450 + 273.15) * dS / 1000
# limestone decomposition CaCO3 -> CaO + CO2
lH, lS = 178.3, 160.6
lTx = lH * 1000 / lS
lG25 = lH - 298.15 * lS / 1000
lG900 = lH - (900 + 273.15) * lS / 1000
# mistakes
g_joule = dH - T * dS                  # dS left in J
g_celsius = dH - Tc * dS / 1000
g_per_nh3 = dG / 2
# electrochemistry
E_dan, n_dan = 1.10, 2
G_dan = -n_dan * F * E_dan / 1000
# non-standard: Q = 1e-4 (low NH3 partial pressure), 25 C
Q = 1e-4
G_Q = dG + R * T * math.log(Q) / 1000

edit('chemistry/gibbs-free-energy', date=U, phrase='Gibbs free energy calculator',
     description='Gibbs free energy calculator: find ΔG = ΔH ' + MINUS + ' TΔS at any temperature, see whether a reaction is spontaneous and find the crossover temperature.',
     intro=("Gibbs free energy combines the enthalpy change ΔH and the entropy change ΔS of a reaction into one number that says whether it can run on its own at a given temperature. "
            "This Gibbs free energy calculator works out ΔG = ΔH " + MINUS + " TΔS and labels the result spontaneous or not.\n\n"
            "Chemistry students use it for thermodynamics problems, and process chemists and metallurgists use it to choose operating temperatures and check whether a reaction is worth pursuing."),
     before='## Spontaneous is not the same as fast',
     body_add=f'''## Ammonia synthesis at plant temperatures

Treating ΔH and ΔS as constant, the calculator equation gives ΔG for N₂ + 3H₂ → 2NH₃ at higher temperatures, and K = e<sup>{MINUS}ΔG/RT</sup> shows how the equilibrium constant falls:

| Temperature | T | ΔG | K |
|---|---|---|---|
{g_rows}
At 25 °C, K is about {sci(K25)}, so the equilibrium lies far towards ammonia, but the reaction is too slow without a catalyst. Industrial Haber plants run near 450 °C, where ΔG is {m_(g450)} kJ/mol and K is below 1, and they compensate with pressures of 150 to 300 bar and an iron catalyst, recycling the unreacted gas. This trade between thermodynamics and rate is the classic use of ΔG in process design.

## Second example: when does limestone decompose?

CaCO₃ → CaO + CO₂ has ΔH = +{lH} kJ/mol and ΔS = +{lS} J/mol·K, both positive, so it becomes favourable only when hot:

- At 25 °C: ΔG = {lH} {MINUS} 298.15 × {lS/1000:.4f} = **+{lG25:.1f} kJ/mol**, so limestone is stable
- Crossover: T = {lH*1000:,.0f} ÷ {lS} = **{lTx:,.0f} K** ({lTx-273.15:,.0f} °C)
- At 900 °C: ΔG = {lH} {MINUS} 1,173.15 × {lS/1000:.4f} = **{m_(lG900)} kJ/mol**, so lime kilns run above about 900 °C

## Where ΔH and ΔS come from

Values are usually built from tables of standard enthalpies of formation (ΔH<sub>f</sub>°) and standard molar entropies (S°): ΔH = Σ ΔH<sub>f</sub>°(products) {MINUS} Σ ΔH<sub>f</sub>°(reactants), and ΔS the same way with S°, each multiplied by its stoichiometric coefficient. ΔH can also be measured directly in a calorimeter. For redox reactions ΔG is measured electrically from the cell voltage, ΔG = {MINUS}nFE, and for others it comes from a measured equilibrium constant through ΔG° = {MINUS}RT ln K.

''', min_words=0)

edit('chemistry/gibbs-free-energy', date=U, phrase='Gibbs free energy calculator',
     body_add=f'''
## Common mistakes

- **Leaving ΔS in J/mol·K when combining by hand.** {m_(dH)} {MINUS} 298.15 × ({m_(dS)}) gives {m_(g_joule, 0)}, which mixes kJ and J; dividing ΔS by 1,000 gives the correct {m_(dG, 2)} kJ/mol.
- **Using Celsius for T.** Putting 25 instead of 298.15 gives {m_(g_celsius, 1)} kJ/mol, far too negative; the formula needs kelvin.
- **Forgetting that ΔG is per mole of reaction as written.** The ammonia value is for 2 mol of NH₃; per mole of ammonia it is {m_(g_per_nh3, 1)} kJ/mol. Doubling every coefficient doubles ΔG.
- **Confusing ΔG with ΔG°.** Tables give standard values (1 bar, 1 mol/L). At other compositions ΔG = ΔG° + RT ln Q; with Q = 10<sup>{MINUS}4</sup> the ammonia reaction at 25 °C has ΔG = {m_(G_Q)} kJ/mol.
- **Extrapolating too far.** ΔH and ΔS drift with temperature and phase changes, so values from 25 °C give estimates, not exact figures, hundreds of degrees away.
''',
     faq_add=[('How is Gibbs free energy related to cell voltage?',
               f'ΔG = {MINUS}nFE, where n is the electrons transferred and F = 96,485 C/mol. A Daniell cell with E = {E_dan} V and n = {n_dan} has ΔG = {m_(G_dan)} kJ/mol, so a positive cell voltage always means a negative ΔG.'),
              ('Does ΔG depend on how the reaction equation is written?',
               f'Yes. ΔG, ΔH and ΔS are per mole of reaction as written. For N₂ + 3H₂ → 2NH₃ at 25 °C ΔG is {m_(dG)} kJ/mol; written per mole of ammonia it is {m_(g_per_nh3)} kJ/mol, and the reverse reaction has the opposite sign.')],
     min_words=520)

# ======================================================================= Half-life
N0, Th, t = 100.0, 5730.0, 10000.0
N = N0 * 0.5 ** (t / Th)
assert abs(N - 29.83) < 0.01
lam = math.log(2) / Th
tau = Th / math.log(2)
# age from 40 % remaining
f40 = 0.40
age40 = Th * math.log2(1 / f40)
age40_libby = 5568 * math.log2(1 / f40)
# half-life from two readings: 100 -> 80 in 3 days
T_two = 3 * math.log(2) / math.log(100 / 80)
# I-131 therapy: 3.7 GBq, after 30 days
A0, Ti, ti = 3.7, 8.02, 30
Ai = A0 * 0.5 ** (ti / Ti)
iso = [('Technetium-99m', 6.01, 'h'), ('Iodine-131', 8.02, 'd'), ('Cobalt-60', 5.27, 'yr'),
       ('Caesium-137', 30.1, 'yr'), ('Carbon-14', 5730, 'yr')]
i_rows = ''
for nm, h, u in iso:
    lm = math.log(2) / h
    lam_s = f"{lm:.4f}" if lm >= 0.01 else sci(lm)
    tt, t1 = h / math.log(2), h * math.log2(100)
    fm = (lambda x: f"{x:,.0f}") if h > 100 else (lambda x: f"{x:,.1f}")
    i_rows += f"| {nm} | {h:,g} {u} | {lam_s} per {u} | {fm(tt)} {u} | {fm(t1)} {u} |\n"
# mistakes
N_unit = N0 * 0.5 ** (t / 365.25 / Th)   # elapsed time entered as days by mistake
lin2 = 0
N_decayed = N0 - N

edit('chemistry/half-life', date=U, phrase='half-life calculator',
     description='Half-life calculator for radioactive decay, drugs and first-order reactions: find the amount left, the time elapsed or the half-life itself, step by step.',
     intro=("Half-life is the time it takes for half of a radioactive sample, a drug in the body or a first-order reactant to disappear, and it stays the same however much is left. "
            "This half-life calculator finds the amount remaining, the time elapsed or the half-life from the other values.\n\n"
            "Students use it for decay and dating problems, while radiographers, nuclear medicine staff, pharmacists and archaeologists use it to plan doses, storage times and sample ages."),
     before='## Radiocarbon dating',
     body_add=f'''## Decay constants and lifetimes of common isotopes

From λ = ln 2 ÷ T<sub>½</sub>, the mean lifetime τ = T<sub>½</sub> ÷ ln 2 and the time to fall to 1%, T<sub>½</sub> × log₂ 100:

| Isotope | Half-life | Decay constant λ | Mean lifetime τ | Time to 1% |
|---|---|---|---|---|
{i_rows}
For the default carbon-14 case, λ = {sci(lam)} per year and τ = {tau:,.0f} years.

## Second example: activity of a medical source

A patient receives {A0} GBq of iodine-131 (half-life {Ti} days). After {ti} days the activity is {A0} × 0.5<sup>{ti}/{Ti}</sup> = **{Ai:.3f} GBq**, about {100*Ai/A0:.1f}% of the original. Activity in becquerels falls by the same fraction as the number of atoms, because activity = λN, so the calculator works with either.

## Finding the half-life from two measurements

If a count rate falls from 100 to 80 in 3 days, the half-life is T<sub>½</sub> = t × ln 2 ÷ ln(N₀ ÷ N) = 3 × 0.6931 ÷ ln 1.25 = **{T_two:.2f} days**. Enter 100, 80 and 3 days and solve for the half-life to get the same figure.

## How half-lives are measured

Short half-lives are measured by counting decays with a Geiger tube or scintillation detector at regular intervals, subtracting the background count, and fitting a straight line to ln(count rate) against time; the slope is {MINUS}λ. Very long half-lives such as uranium-238 cannot be watched directly, so they come from the specific activity: count the decays per second from a weighed sample and use λ = A ÷ N. Radiocarbon laboratories now count carbon-14 atoms directly by accelerator mass spectrometry, which needs only milligrams of carbon.

''', min_words=0)

edit('chemistry/half-life', date=U, phrase='half-life calculator',
     body_add=f'''
## Common mistakes

- **Mixing time units.** The half-life and elapsed time must be in the same unit; each field here has its own unit selector. Entering the elapsed time as 10,000 days while the half-life stays at 5,730 years shows {N_unit:.1f} units remaining instead of {N:.1f}.
- **Subtracting linearly.** Two half-lives do not remove everything; they leave 25%. Decay is exponential, so some always remains.
- **Reporting the decayed amount as the remainder.** After 10,000 years {N:.1f} units remain and {N_decayed:.1f} have decayed; check which one a question asks for.
- **Using the wrong half-life convention for radiocarbon.** Conventional radiocarbon ages use the Libby value of 5,568 years, then a calibration curve; 40% remaining gives {age40_libby:,.0f} years with 5,568 and {age40:,.0f} years with 5,730.
- **Applying one half-life to every drug situation.** Elimination half-life describes the falling phase; during absorption or infusion, or when the liver is saturated, levels do not follow a single exponential.
''',
     faq_add=[('How do I find the half-life from two measurements?',
               f'Use T½ = t × ln 2 ÷ ln(N₀ ÷ N). A reading that falls from 100 to 80 in 3 days gives a half-life of {T_two:.2f} days. The two readings must be corrected for background in the same way.'),
              ('Why do radiocarbon labs quote ages with a 5,568 year half-life?',
               f'By convention, conventional radiocarbon ages use the original Libby half-life of 5,568 years so results stay comparable, and calibration curves then convert them to calendar years. A sample with 40% carbon-14 left has a conventional age of {age40_libby:,.0f} years, against {age40:,.0f} years with 5,730.')],
     min_words=520)

# ======================================================================= Boyle's law
P1, V1, P2 = 100.0, 10.0, 250.0
V2 = P1 * V1 / P2
assert abs(V2 - 4.0) < 1e-12
PV = P1 * V1                     # kPa L = J
Patm = 101.325
# gauge mistake: inputs read as gauge
V2_abs = (P1 + Patm) * V1 / (P2 + Patm)
# adiabatic comparison, gamma 1.4
gam = 1.4
V2_ad = V1 * (P1 / P2) ** (1 / gam)
T2_ad = 293.15 * (P2 / P1) ** ((gam - 1) / gam)
# receiver free air
Vr, Pg = 50.0, 700.0
free = (Pg + Patm) * Vr / Patm
usable = Pg * Vr / Patm        # air released down to atmospheric
# diving table: 6 L at surface, seawater 1025 kg/m3
rho, g = 1025.0, 9.80665
d_rows = ''
for d in (0, 5, 10, 20, 30, 40):
    pa = Patm + rho * g * d / 1000
    d_rows += f"| {d} m | {pa:.1f} kPa | {pa/Patm:.2f} | {6*Patm/pa:.2f} L |\n"
p10 = Patm + rho * g * 10 / 1000
v10 = 6 * Patm / p10

edit('chemistry/boyles-law', date=U, phrase="Boyle's law calculator",
     description="Boyle's law calculator: find the new pressure or volume of a gas at constant temperature from P1V1 = P2V2, with absolute pressure tips and examples.",
     intro=("Boyle's law says that at constant temperature the pressure of a fixed amount of gas is inversely proportional to its volume, so halving the volume doubles the pressure. "
            "This Boyle's law calculator solves P₁V₁ = P₂V₂ for whichever pressure or volume you leave blank.\n\n"
            "Students use it for gas law problems, and divers, compressed air technicians and lab staff use it to estimate gas volumes in cylinders, receivers, syringes and lungs."),
     replace=[('V₂ = 100 × 10 ÷ 250 = **4 L**',
               f'''V₂ = 100 × 10 ÷ 250 = **4 L**

The product P V stays at {PV:,.0f} kPa·L before and after, which is also {PV:,.0f} J, because 1 kPa·L = 1 J. If the 100 kPa and 250 kPa were gauge readings rather than absolute pressures, the correct answer would be (100 + 101.325) × 10 ÷ (250 + 101.325) = **{V2_abs:.2f} L**, not 4 L.''')],
     before='## Everyday examples',
     body_add=f'''## Second example: free air in a compressed air receiver

A {Vr:.0f} L receiver is charged to {Pg/100:.0f} bar gauge ({Pg+Patm:.1f} kPa absolute). Expanded to atmospheric pressure at the same temperature, the air would occupy ({Pg+Patm:.1f} × {Vr:.0f}) ÷ {Patm} = **{free:,.0f} L** of free air. Only the part above atmospheric can leave the tank, so emptying it to 0 bar gauge releases {Pg:.0f} × {Vr:.0f} ÷ {Patm} = {usable:,.0f} L. Compressor capacities are quoted in free air delivery for exactly this reason.

''', min_words=0)

edit('chemistry/boyles-law', date=U, phrase="Boyle's law calculator",
     replace=[('''At 10 m depth, the absolute pressure is about 2 atm, so a lungful of air from the surface shrinks to half its volume ''' + chr(0x2014) + ''' which is why divers must never hold their breath while ascending.''',
               f'''In seawater (1,025 kg/m³) the absolute pressure at depth d is 101.325 kPa + ρ g d. A 6 L lungful of air taken at the surface shrinks as the diver descends:

| Depth | Absolute pressure | Atmospheres | Volume of 6 L of surface air |
|---|---|---|---|
{d_rows}
At 10 m the pressure is {p10:.1f} kPa and the air occupies {v10:.2f} L. The reverse is the danger: air breathed at depth expands on the way up, which is why divers must never hold their breath while ascending.''')],
     body_add=f'''
## Measuring Boyle's law in the lab

The classic school method traps air in a sealed syringe or a glass tube connected to a pressure gauge or electronic sensor. The plunger is moved in small steps, waiting each time for the gas to return to room temperature, and pressure and volume are recorded. A graph of P against V is a curve, but P against 1/V is a straight line through the origin whose slope is the constant P V. Readings from the syringe scale should include the dead volume of the tubing and sensor, or the line will not pass through zero.

## Common mistakes

- **Using gauge pressure.** With the default numbers read as gauge values the true answer is {V2_abs:.2f} L, not 4 L, an error of {100*(V2_abs-4)/V2_abs:.0f}%.
- **Compressing quickly.** A fast, adiabatic squeeze from 100 to 250 kPa leaves {V2_ad:.2f} L, not 4 L, and heats air from 20 °C to about {T2_ad-273.15:.0f} °C; Boyle's law only holds once the gas has cooled back.
- **Letting the amount of gas change.** Leaks, gas dissolving in liquid or water vapour condensing all change n, so P V is no longer constant.
- **Applying it to liquids.** Liquids are almost incompressible; Boyle's law describes gases only.
- **Forgetting dead volume.** Tubing, valves and gauges add trapped volume that must be counted in V₁ and V₂.
''',
     faq_add=[("How much air does a compressed air tank hold at atmospheric pressure?",
               f"Multiply the absolute pressure by the tank volume and divide by atmospheric pressure. A {Vr:.0f} L receiver at {Pg/100:.0f} bar gauge holds about {free:,.0f} L of free air, of which {usable:,.0f} L can be released before the tank reaches 0 bar gauge."),
              ("Does Boyle's law work if the gas is compressed quickly?",
               f"Not exactly. Fast compression heats the gas, so the pressure rises more than Boyle's law predicts. Compressing air quickly from 100 to 250 kPa gives {V2_ad:.2f} L instead of 4 L; once it cools to the starting temperature, the volume settles at 4 L.")],
     min_words=520)

print('dropped', drop_backlog(['chemistry/gibbs-free-energy', 'chemistry/half-life', 'chemistry/boyles-law']))
import inplace
for c in inplace.DONE:
    pass
for c in ['chemistry/gibbs-free-energy', 'chemistry/half-life', 'chemistry/boyles-law']:
    print(c, inplace.body_words(c))
