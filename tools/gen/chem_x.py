import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
R = 8.314462618

expand('chemistry/arrhenius-equation', '''
## How temperature changes the rate

For Ea = 50 kJ/mol, the rate constant relative to 25 °C:

| Temperature | Relative rate |
|---|---|
''' + ''.join(f"| {t} °C | {math.exp(-50000/R*(1/(t+273.15)-1/298.15)):.2f}× |\n" for t in [0, 10, 25, 35, 50, 75, 100]) + '''
The old rule of thumb that “rates double every 10 °C” holds roughly for activation energies around 50 kJ/mol near room temperature.

## Two-temperature form

If you know the rate constants at two temperatures, find Ea without A:

<p class="formula">ln(k₂ ÷ k₁) = −Ea ÷ R × (1 ÷ T₂ − 1 ÷ T₁)</p>

If a reaction is 3 times faster at 40 °C than at 20 °C, Ea = R × ln 3 ÷ (1/293.15 − 1/313.15) ≈ **41.9 kJ/mol**.

## Arrhenius plot

Plotting ln k against 1/T gives a straight line with slope −Ea/R and intercept ln A. This is the standard way to find activation energy from experimental data.

## Catalysts

A catalyst lowers the activation energy. Cutting Ea from 50 to 40 kJ/mol at 25 °C speeds the reaction up by a factor of about **56** — a huge effect from a modest change.

## Real-world uses

- **Food storage**: refrigeration slows spoilage reactions.
- **Shelf-life testing**: accelerated ageing at high temperature predicts room-temperature stability.
- **Industrial chemistry**: choosing reactor temperatures.
''', [
 ('What are the units of the rate constant?', 'They depend on the reaction order. The calculator gives k in the same units as A.'),
 ('Why does a small temperature rise speed reactions so much?', 'Because the fraction of molecules with energy above Ea grows exponentially with temperature.'),
], before='## Why it matters')

expand('chemistry/beer-lambert', '''
## Absorbance to transmittance table

| Absorbance | Transmittance | Light absorbed |
|---|---|---|
''' + ''.join(f"| {a} | {10**-a*100:.1f}% | {100-10**-a*100:.1f}% |\n" for a in [0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0]) + '''
Most spectrophotometers are most accurate between about **A = 0.1 and 1.0**. Dilute samples that read above this range.

## Building a calibration curve

1. Prepare standards of known concentration.
2. Measure absorbance at the chosen wavelength (λ<sub>max</sub>).
3. Plot absorbance against concentration — it should be a straight line through the origin.
4. Use the slope (ε × l) to find unknown concentrations.

## Common molar absorptivities

| Substance | Wavelength | ε (L/mol·cm) |
|---|---|---|
| NADH | 340 nm | 6,220 |
| DNA (per base, approx.) | 260 nm | about 6,600 |
| Potassium permanganate | 525 nm | about 2,400 |
| p-Nitrophenolate | 405 nm | about 18,000 |

## When Beer–Lambert breaks down

- **High concentrations** (above about 0.01 M): molecules interact and the line curves.
- **Scattering**: cloudy or turbid samples.
- **Stray light** and non-monochromatic light in the instrument.
- **Chemical changes**: equilibria that shift with dilution.

For nucleic acid samples, see the [DNA concentration calculator](/biology/dna-concentration/).
''', [
 ('What does an absorbance of 1 mean?', 'Only 10% of the light passes through; 90% is absorbed.'),
 ('Why is absorbance unitless?', 'It is a logarithm of a ratio of light intensities, so the units cancel.'),
], before='## Absorbance vs transmittance')

expand('chemistry/boyles-law', '''
## Pressure–volume table

Starting at 100 kPa and 10 L, at constant temperature:

| Pressure | Volume |
|---|---|
''' + ''.join(f"| {p} kPa | {1000/p:.2f} L |\n" for p in [50, 100, 150, 200, 300, 500, 1000]) + '''
Double the pressure and the volume halves; the product P × V stays at 1,000 kPa·L.

## Everyday examples

- **Syringes**: pulling the plunger increases volume, lowering pressure, so liquid is drawn in.
- **Breathing**: your diaphragm enlarges the chest, lowering lung pressure so air flows in.
- **Bicycle pumps**: pushing the handle compresses air until its pressure exceeds the tyre's.
- **Aerosol cans**: gas expands as it leaves the higher-pressure can.

## Why temperature must be constant

Compressing a gas quickly heats it (think of a bicycle pump getting warm). Boyle's law applies to slow changes where heat can escape, keeping the temperature steady. If temperature changes too, use the [combined gas law](/chemistry/combined-gas-law/).

## Gauge vs absolute pressure

Always use **absolute** pressure. A tyre gauge reading of 200 kPa is about 301 kPa absolute at sea level. Using gauge pressure gives wrong answers.
''', [
 ('What is Boyle’s law?', 'At constant temperature, the pressure of a fixed amount of gas is inversely proportional to its volume: P₁V₁ = P₂V₂.'),
 ('Who discovered Boyle’s law?', 'Robert Boyle published it in 1662, based on experiments with air trapped in a J-shaped tube.'),
], before='## Diving example')

expand('chemistry/charles-law', '''
## Volume–temperature table

Starting at 2 L and 25 °C, at constant pressure:

| Temperature | Volume |
|---|---|
''' + ''.join(f"| {t} °C | {2*(t+273.15)/298.15:.3f} L |\n" for t in [-50, -20, 0, 25, 50, 100, 200]) + '''
## Absolute zero

Extend the volume–temperature line backwards and it reaches zero volume at **−273.15 °C** (0 K). This was one of the first clues to the existence of absolute zero.

## Everyday examples

- **Hot-air balloons**: heating the air inside expands it, lowering its density so the balloon rises.
- **Balloons in the cold**: a party balloon shrinks when taken outside on a cold day.
- **Tyres**: on a hot day tyre pressure rises (pressure and temperature together — see [Gay-Lussac's law](/chemistry/combined-gas-law/)).
- **Baking**: gas bubbles in dough expand in the oven, helping bread rise.

## Gay-Lussac's law

At constant volume, pressure is proportional to absolute temperature: P₁ ÷ T₁ = P₂ ÷ T₂. A sealed can at 1 atm and 20 °C reaches about 1.27 atm at 100 °C.
''', [
 ('What is Charles’s law?', 'At constant pressure, the volume of a gas is directly proportional to its absolute temperature: V₁ ÷ T₁ = V₂ ÷ T₂.'),
 ('Why must temperature be in kelvin?', 'Because volume is proportional to absolute temperature. Using °C gives wrong results, and fails completely below 0 °C.'),
], before='## A common mistake')

expand('chemistry/combined-gas-law', '''
## Standard conditions

Gas volumes are often reported at standard conditions so they can be compared:

| Standard | Temperature | Pressure |
|---|---|---|
| STP (IUPAC, since 1982) | 0 °C (273.15 K) | 100 kPa |
| STP (older) | 0 °C | 101.325 kPa (1 atm) |
| NTP | 20 °C | 101.325 kPa |
| Normal (industrial Nm³) | 0 °C | 101.325 kPa |

## Correcting gas volume to standard conditions

A gas meter reads 10 m³ at 2 bar(g) (3.013 bar absolute) and 30 °C. At normal conditions:

<p class="formula">V<sub>N</sub> = 10 × (3.013 ÷ 1.01325) × (273.15 ÷ 303.15) = 26.8 Nm³</p>

This is how gas flow is billed and compared in industry.

## Adding the amount of gas

If the amount of gas changes too, use the full [ideal gas law](/physics/ideal-gas-law/): PV = nRT. The combined gas law is the special case where n is constant.

## Common errors

- Using **gauge pressure** instead of absolute.
- Using **°C instead of kelvin**.
- Mixing units — keep P₁ and P₂ in the same unit, and V₁ and V₂ in the same unit. The calculator handles this for you.
''', [
 ('What is the combined gas law?', 'P₁V₁ ÷ T₁ = P₂V₂ ÷ T₂ for a fixed amount of gas, combining Boyle’s, Charles’s and Gay-Lussac’s laws.'),
 ('Can I use it for real gases?', 'Yes for most gases near room conditions. At very high pressure or low temperature, real-gas corrections are needed.'),
], before='## Special cases')

expand('chemistry/dilution', '''
## Common dilutions

| Stock | Final | Ratio | For 100 mL final: stock + solvent |
|---|---|---|---|
''' + ''.join(f"| {c1} | {c2} | 1 : {c1/c2:g} | {100*c2/c1:g} mL + {100-100*c2/c1:g} mL |\n" for c1, c2 in [(10, 1), (10, 0.5), (5, 1), (1, 0.1), (6, 1), (12, 0.5)]) + '''
## Dilution factor

<p class="formula">Dilution factor = V₂ ÷ V₁ = C₁ ÷ C₂</p>

A 1 : 10 dilution has a factor of 10. Note that “1 : 10” usually means 1 part in 10 total, but some fields use it to mean 1 part plus 10 parts. Check the convention in your protocol.

## Percent solutions

The C₁V₁ = C₂V₂ rule works for any concentration unit — mol/L, % (w/v), mg/mL or ppm — as long as C₁ and C₂ use the same one. To make 500 mL of 70% ethanol from 95% stock: V₁ = 70 × 500 ÷ 95 = **368 mL** of stock, made up to 500 mL with water.

## Mixing volumes are not always additive

Mixing ethanol and water gives slightly less volume than the sum of the parts. For accurate work, add solvent **up to** the final volume mark in a volumetric flask rather than adding a calculated volume of solvent.
''', [
 ('How do I make a 1:10 dilution?', 'Mix 1 part stock with 9 parts solvent, for example 1 mL stock plus 9 mL water for 10 mL total.'),
 ('What is C1V1 = C2V2?', 'The dilution equation: the amount of solute before (C₁ × V₁) equals the amount after (C₂ × V₂).'),
], before='## Serial dilutions')

expand('chemistry/gibbs-free-energy', '''
## Crossover temperature

When ΔH and ΔS have the same sign, the reaction switches between spontaneous and non-spontaneous at:

<p class="formula">T = ΔH ÷ ΔS</p>

For ammonia synthesis (ΔH = −92.2 kJ/mol, ΔS = −198.7 J/mol·K), T = 92,200 ÷ 198.7 = **464 K (191 °C)**. Below this temperature the forward reaction is favoured; above it, the reverse.

## Gibbs energy and equilibrium

ΔG° is linked to the equilibrium constant:

<p class="formula">ΔG° = −R × T × ln K</p>

| ΔG° (kJ/mol, 25 °C) | K |
|---|---|
''' + ''.join(f"| {g} | {math.exp(-g*1000/(R*298.15)):.3g} |\n" for g in [-40, -20, -10, 0, 10, 20, 40]) + '''
Every 5.7 kJ/mol change in ΔG° at 25 °C changes K by a factor of 10.

## Spontaneous is not the same as fast

A negative ΔG means a reaction can proceed, not that it will be quick. Diamond turning into graphite has a negative ΔG at room conditions but takes an immeasurably long time. Speed depends on activation energy — see the [Arrhenius calculator](/chemistry/arrhenius-equation/).

## Units

ΔH is usually in kJ/mol and ΔS in J/mol·K. Divide ΔS by 1,000 before combining them, as the calculator does.
''', [
 ('What does a negative ΔG mean?', 'The reaction is thermodynamically favourable (spontaneous) under those conditions.'),
 ('What is the Gibbs free energy equation?', 'ΔG = ΔH − TΔS, where T is the absolute temperature in kelvin.'),
], before='## The four cases')

expand('chemistry/half-life', '''
## Fraction remaining after each half-life

| Half-lives passed | Fraction remaining |
|---|---|
''' + ''.join(f"| {n} | {0.5**n*100:.3g}% |\n" for n in [1, 2, 3, 4, 5, 7, 10]) + '''
After about 10 half-lives, less than 0.1% remains.

## Decay constant

The half-life and the decay constant λ are related:

<p class="formula">λ = ln 2 ÷ T<sub>½</sub>, &nbsp; N = N₀ × e<sup>−λt</sup></p>

## Radiocarbon dating

To find age from the fraction remaining:

<p class="formula">t = T<sub>½</sub> × log₂(N₀ ÷ N)</p>

A sample with 25% of its original carbon-14 is 2 half-lives old: about **11,460 years**. Carbon dating works up to roughly 50,000 years.

## Half-life in medicine

Drug half-lives determine dosing intervals. A medicine with a 6-hour half-life falls to about 6% of its peak after 24 hours (4 half-lives). It takes about 4–5 half-lives to reach a steady state with regular doses.

## Other uses

- **First-order chemical reactions** have a constant half-life, independent of concentration.
- **Biological half-life**: how long the body takes to eliminate half of a substance.
- **Radioactive waste**: long half-lives mean safe storage for very long periods.
''', [
 ('How long until only 1% remains?', 'About 6.64 half-lives, because 0.5^6.64 ≈ 0.01.'),
 ('Is half-life the same as average lifetime?', 'No. The mean lifetime is half-life ÷ ln 2, about 1.44 times the half-life.'),
], before='## Common half-lives')

expand('chemistry/henderson-hasselbalch', '''
## Base-to-acid ratio and pH

| [A⁻] ÷ [HA] | pH − pKa |
|---|---|
''' + ''.join(f"| {r} | {math.log10(r):+.2f} |\n" for r in [0.1, 0.25, 0.5, 1, 2, 4, 10]) + '''
A buffer works best within **±1 pH unit** of its pKa, where the ratio is between 0.1 and 10.

## Preparing a buffer of a given pH

Rearrange to find the ratio needed:

<p class="formula">[A⁻] ÷ [HA] = 10<sup>(pH − pKa)</sup></p>

For an acetate buffer at pH 5.00 (pKa 4.76), the ratio is 10<sup>0.24</sup> = **1.74**. With a total buffer concentration of 0.1 M, use 0.0635 M acetate and 0.0365 M acetic acid.

## Buffer capacity

Capacity is how much acid or base a buffer can absorb before the pH changes significantly. It is highest when [A⁻] = [HA] (pH = pKa) and rises with total concentration.

## The blood buffer

Blood pH (about 7.4) is held mainly by the bicarbonate system:

<p class="formula">pH = 6.1 + log([HCO₃⁻] ÷ (0.03 × pCO₂))</p>

with pCO₂ in mmHg. Doctors use this to interpret blood gas results.

## Limits of the equation

It assumes concentrations are not too dilute and activity effects are small. For very dilute buffers or extreme pH, a full equilibrium calculation is more accurate.
''', [
 ('What pH does a buffer have when acid and base are equal?', 'pH = pKa, because log(1) = 0.'),
 ('How do I make a phosphate buffer at pH 7.4?', 'Use the H₂PO₄⁻/HPO₄²⁻ pair (pKa about 7.2). The base-to-acid ratio is about 10^0.2 ≈ 1.6.'),
], before='## Common buffer systems')

expand('chemistry/mass-percent', '''
## Mass percent, molarity and ppm

| Concentration | What it means |
|---|---|
| 1% (w/w) | 1 g solute in 100 g solution |
| 1% (w/v) | 1 g solute in 100 mL solution |
| 1% (v/v) | 1 mL solute in 100 mL solution |
| 1 ppm | 1 mg per kg (or about 1 mg/L in water) |
| 10,000 ppm | 1% (w/w) |

Always state which kind of percent you mean.

## Converting mass percent to molarity

<p class="formula">Molarity = (w × ρ × 1,000) ÷ M</p>

with w the mass fraction, ρ the solution density in g/mL and M the molar mass. Concentrated hydrochloric acid at 37% (ρ = 1.19 g/mL, M = 36.46): 0.37 × 1.19 × 1000 ÷ 36.46 = **12.1 M**.

## Common concentrated reagents

| Reagent | Mass percent | Density (g/mL) | Molarity (approx.) |
|---|---|---|---|
| Hydrochloric acid | 37% | 1.19 | 12.1 M |
| Sulphuric acid | 98% | 1.84 | 18.4 M |
| Nitric acid | 70% | 1.42 | 15.8 M |
| Ammonia solution | 28% | 0.90 | 14.8 M |

## Finding solute needed

To make 500 g of a 5% salt solution: solute = 0.05 × 500 = 25 g, solvent = 475 g.
''', [
 ('How do I calculate mass percent?', 'Mass percent = mass of solute ÷ total mass of solution × 100.'),
 ('Is mass percent the same as weight percent?', 'Yes. Mass percent, weight percent and % w/w all mean the same thing.'),
], before='## Common uses')

expand('chemistry/molality', '''
## Molality vs molarity

| | Molality (b) | Molarity (c) |
|---|---|---|
| Definition | mol solute per kg solvent | mol solute per L solution |
| Changes with temperature? | No | Yes (volume changes) |
| Used for | Colligative properties | Everyday lab work |

For dilute aqueous solutions, molality and molarity are nearly equal.

## Colligative properties

| Property | Formula | Constant for water |
|---|---|---|
| Freezing point depression | ΔT = i × K<sub>f</sub> × b | K<sub>f</sub> = 1.86 K·kg/mol |
| Boiling point elevation | ΔT = i × K<sub>b</sub> × b | K<sub>b</sub> = 0.512 K·kg/mol |

A 1 mol/kg NaCl solution (i ≈ 2) freezes at about −3.7 °C and boils at about 101.0 °C.

## Road salt and antifreeze

Salt lowers the freezing point of water on roads. Ethylene glycol in car antifreeze works the same way; a 50% mixture protects down to about −37 °C, far below what the simple dilute formula predicts, because the solution is very concentrated.

## Converting molarity to molality

<p class="formula">b = c ÷ (ρ − c × M ÷ 1,000)</p>

with ρ the solution density in kg/L and M in g/mol.
''', [
 ('What is molality used for?', 'Calculating freezing point depression, boiling point elevation and other colligative properties, because it does not change with temperature.'),
 ('Is molality the same as molarity?', 'No. Molality uses kilograms of solvent; molarity uses litres of solution. They are close for dilute water solutions.'),
], before='## Freezing point depression')

expand('chemistry/molarity', '''
## Mass needed for common solutions

For 1 L of solution:

| Compound | Molar mass (g/mol) | 0.1 M | 0.5 M | 1 M |
|---|---|---|---|---|
''' + ''.join(f"| {n} | {m} | {m*0.1:.2f} g | {m*0.5:.2f} g | {m:.2f} g |\n" for n, m in [('NaCl', 58.44), ('NaOH', 40.00), ('KCl', 74.55), ('Glucose (C₆H₁₂O₆)', 180.16), ('CuSO₄·5H₂O', 249.69), ('Na₂CO₃', 105.99)]) + '''
## Molarity units

| Unit | Meaning |
|---|---|
| M (mol/L) | moles per litre |
| mM | millimoles per litre (0.001 M) |
| µM | micromoles per litre (10⁻⁶ M) |
| nM | nanomoles per litre (10⁻⁹ M) |

## Molarity from mass percent

If you have a percent solution and its density, see the [mass percent calculator](/chemistry/mass-percent/) for the conversion formula.

## Normality

Normality (N) counts reactive equivalents rather than moles: N = M × number of equivalents. 1 M H₂SO₄ is 2 N for acid–base reactions because each molecule gives two H⁺ ions.

## Hydrates

When using a hydrated salt, include the water in the molar mass. Copper sulphate pentahydrate (CuSO₄·5H₂O, 249.69 g/mol) needs much more mass than anhydrous CuSO₄ (159.61 g/mol) for the same molarity.
''', [
 ('How do I make a 1 M NaCl solution?', 'Dissolve 58.44 g of NaCl in water and make the volume up to exactly 1 litre.'),
 ('What is the difference between mM and µM?', '1 mM = 1,000 µM. Millimolar is a thousand times more concentrated than micromolar.'),
], before='## Preparing a solution')

expand('chemistry/moles', '''
## Moles from mass for common substances

| Substance | Molar mass (g/mol) | 10 g = | 100 g = |
|---|---|---|---|
''' + ''.join(f"| {n} | {m} | {10/m:.3f} mol | {100/m:.3f} mol |\n" for n, m in [('Water (H₂O)', 18.015), ('Carbon dioxide (CO₂)', 44.01), ('Sodium chloride (NaCl)', 58.44), ('Glucose (C₆H₁₂O₆)', 180.16), ('Calcium carbonate (CaCO₃)', 100.09), ('Iron (Fe)', 55.845)]) + '''
## Calculating molar mass

Add the atomic masses of every atom in the formula:

- H₂SO₄ = 2 × 1.008 + 32.06 + 4 × 16.00 = **98.08 g/mol**
- Ca(OH)₂ = 40.08 + 2 × (16.00 + 1.008) = **74.09 g/mol**

## Moles of a gas

At 0 °C and 1 atm, 1 mole of any ideal gas occupies about 22.4 L. At 25 °C and 1 atm, about 24.5 L. For other conditions, use the [ideal gas law](/physics/ideal-gas-law/).

## Moles in reactions

Balanced equations give mole ratios. In 2H₂ + O₂ → 2H₂O, 4 g of hydrogen (2 mol) reacts with 32 g of oxygen (1 mol) to give 36 g of water (2 mol).

## Avogadro's number

Since 2019, the mole is defined by fixing Avogadro's number at exactly 6.022 140 76 × 10²³ particles per mole.
''', [
 ('How many moles are in 36 g of water?', '36 ÷ 18.015 = 2.0 mol.'),
 ('How many molecules are in a mole?', '6.022 × 10²³ — Avogadro’s number.'),
], before='## Common molar masses')

expand('chemistry/osmotic-pressure', '''
## Osmotic pressure of common solutions at 37 °C

| Solution | i × c (osmol/L) | Osmotic pressure |
|---|---|---|
''' + ''.join(f"| {n} | {ic} | {ic*1000*R*310.15/101325:.2f} atm |\n" for n, ic in [('0.9% saline (0.154 M NaCl)', 0.308), ('5% glucose (0.278 M)', 0.278), ('Seawater (approx.)', 1.1), ('0.1 M sucrose', 0.1)]) + '''
## Isotonic, hypotonic and hypertonic

| Term | Compared with cells | Effect on red blood cells |
|---|---|---|
| Isotonic | Same osmolarity (about 0.29 osmol/L) | No change |
| Hypotonic | Lower | Swell and may burst |
| Hypertonic | Higher | Shrink |

0.9% saline and 5% glucose are approximately isotonic, which is why they are used for intravenous drips.

## Reverse osmosis

Desalination plants push seawater through a membrane at a pressure higher than its osmotic pressure (about 27 atm), forcing water through and leaving the salt behind. Typical operating pressures are 55–80 bar.

## The van 't Hoff factor

i is the number of particles each formula unit produces in solution: about 1 for sugars, about 2 for NaCl, about 3 for CaCl₂. Real values are slightly lower because of ion pairing.

## Finding molar mass of proteins

Osmotic pressure can measure molar masses of large molecules: M = mass ÷ (Π × V ÷ RT). Even dilute protein solutions give measurable pressures.
''', [
 ('What is the osmotic pressure of blood?', 'About 7.4 atm at body temperature, from an osmolarity of about 0.29 osmol/L.'),
 ('Why does salt water dehydrate cells?', 'It is hypertonic, so water moves out of cells by osmosis towards the higher solute concentration.'),
])

expand('chemistry/percent-composition', '''
## Percent composition examples

| Compound | Element | Percent by mass |
|---|---|---|
''' + ''.join(f"| {c} | {e} | {k*a/M*100:.2f}% |\n" for c, e, k, a, M in [('H₂O', 'O', 1, 16.00, 18.015), ('CO₂', 'C', 1, 12.011, 44.01), ('NaCl', 'Na', 1, 22.99, 58.44), ('CaCO₃', 'Ca', 1, 40.08, 100.09), ('Fe₂O₃', 'Fe', 2, 55.845, 159.69), ('C₆H₁₂O₆', 'C', 6, 12.011, 180.16), ('NH₄NO₃', 'N', 2, 14.007, 80.04)]) + '''
## Empirical formula from percent composition

1. Assume 100 g of compound so percentages become grams.
2. Divide each by its atomic mass to get moles.
3. Divide all by the smallest number of moles.
4. Multiply to get whole numbers if needed.

**Example**: 40.0% C, 6.7% H, 53.3% O → 3.33 mol C, 6.65 mol H, 3.33 mol O → ratio 1 : 2 : 1 → empirical formula **CH₂O**.

## Fertiliser labels

Fertiliser grades such as 46-0-0 (urea) give nitrogen, phosphate (as P₂O₅) and potash (as K₂O) percentages. Urea (CO(NH₂)₂, 60.06 g/mol) contains 2 × 14.007 ÷ 60.06 = **46.6% nitrogen**.

## Hydrates

Water of crystallisation counts in the mass. Copper sulphate pentahydrate is 36.1% water by mass.
''', [
 ('What percent of water is oxygen?', '88.8% by mass.'),
 ('How do I find the empirical formula from percentages?', 'Convert percentages to moles (assuming 100 g), divide by the smallest, and round to whole-number ratios.'),
], before='## More examples')

expand('chemistry/percent-yield', '''
## Why yields are below 100%

- **Incomplete reactions**: equilibrium or slow reactions stop before all reactants are used.
- **Side reactions** produce unwanted by-products.
- **Losses** during filtration, transfer, washing and purification.
- **Impure reactants** mean less starting material than you think.

A yield above 100% usually means the product is wet or impure.

## Atom economy

Atom economy shows how much of the reactants end up in the desired product, even with perfect yield:

<p class="formula">Atom economy = M(desired product) ÷ M(all reactants) × 100%</p>

Green chemistry aims for high atom economy as well as high yield.

## Multi-step synthesis

The overall yield is the product of each step's yield:

| Steps | Yield per step | Overall yield |
|---|---|---|
''' + ''.join(f"| {n} | {y}% | {(y/100)**n*100:.1f}% |\n" for n, y in [(3, 90), (5, 90), (5, 80), (10, 90), (10, 80)]) + '''
This is why pharmaceutical routes with many steps work hard to improve each one.

## Limiting reagent example

2H₂ + O₂ → 2H₂O with 4 g H₂ (2 mol) and 48 g O₂ (1.5 mol): hydrogen is limiting, giving a theoretical yield of 2 mol water (36.0 g). If you collect 30.6 g, the percent yield is **85%**.
''', [
 ('What is a good percent yield?', 'It depends on the reaction. In teaching labs, 70–90% is often good; in industry, optimised processes may exceed 95%.'),
 ('How do I find the theoretical yield?', 'Find the limiting reagent, convert it to moles, use the balanced equation’s ratio, and convert the product moles to mass.'),
], before='## Typical yields')

expand('chemistry/ph', '''
## pH and [H⁺] table

| pH | [H⁺] (mol/L) | Compared with pH 7 |
|---|---|---|
''' + ''.join(f"| {p} | 1 × 10<sup>−{p}</sup> | {(f"{10**(7-p):g}× more H⁺" if p<7 else (f"{10**(p-7):g}× less H⁺" if p>7 else "—"))} |\n" for p in [1, 3, 5, 7, 9, 11, 13]) + '''
Each pH unit is a **tenfold** change in hydrogen ion concentration.

## pH of strong acids and bases

- Strong acid: pH = −log₁₀(concentration). 0.01 M HCl has pH 2.
- Strong base: pOH = −log₁₀([OH⁻]), then pH = 14 − pOH. 0.01 M NaOH has pH 12.

## Weak acids

For a weak acid of concentration C with dissociation constant Ka:

<p class="formula">[H⁺] ≈ √(Ka × C)</p>

0.1 M acetic acid (Ka = 1.8 × 10⁻⁵) has [H⁺] ≈ 1.34 × 10⁻³ M, so pH ≈ **2.87**.

## pH and temperature

The value 14 for pH + pOH applies at 25 °C. At higher temperatures, water ionises more, so neutral pH falls — about 6.14 at 100 °C. A neutral solution is one where [H⁺] = [OH⁻], not necessarily pH 7.

## Measuring pH

| Method | Accuracy |
|---|---|
| Universal indicator paper | ±0.5–1 pH |
| Indicator solutions | ±0.2–0.5 pH |
| Calibrated pH meter | ±0.01–0.05 pH |

Calibrate pH meters with at least two buffers (often pH 4 and 7, or 7 and 10) bracketing your sample.
''', [
 ('What pH is neutral?', 'pH 7 at 25 °C, where hydrogen and hydroxide ions are equal.'),
 ('How much more acidic is pH 3 than pH 5?', '100 times, because each pH unit is a tenfold difference.'),
], before='## pH of everyday substances')

expand('chemistry/ppm', '''
## ppm, mg/L and percent

| ppm | mg/L (in water) | Percent |
|---|---|---|
''' + ''.join(f"| {p:,} | {p:,} | {p/10000:g}% |\n" for p in [1, 10, 100, 500, 1000, 5000, 10000]) + '''
For dilute water solutions, 1 ppm ≈ 1 mg/L because 1 L of water weighs about 1 kg.

## Drinking water guidelines (WHO)

| Substance | Guideline value |
|---|---|
| Fluoride | 1.5 mg/L |
| Nitrate (as NO₃⁻) | 50 mg/L |
| Arsenic | 0.01 mg/L (10 ppb) |
| Lead | 0.01 mg/L (10 ppb) |

Local standards may be stricter. Many countries also set limits for total dissolved solids (TDS) for taste, often around 500–1,000 mg/L.

## ppm in gases

In air, ppm is usually by **volume** (ppmv). Carbon dioxide in outdoor air is now above 420 ppm. Indoor CO₂ above about 1,000 ppm suggests poor ventilation.

## Dosing chlorine

To dose a 10,000 L tank to 2 ppm free chlorine with 10% sodium hypochlorite: chlorine needed = 10,000 × 2 = 20,000 mg = 20 g, so about **200 mL** of 10% solution (assuming a density close to 1 g/mL; real bleach is slightly denser).
''', [
 ('How many ppm is 1%?', '10,000 ppm.'),
 ('Is ppm the same as mg/L?', 'For dilute water solutions, yes, approximately. For other solvents or concentrated solutions, convert using density.'),
], before='## Conversions')

expand('chemistry/specific-heat', '''
## Specific heat of common substances

| Substance | c (J/g·K) |
|---|---|
| Water | 4.186 |
| Ice | 2.09 |
| Steam | 2.01 |
| Ethanol | 2.44 |
| Olive oil | about 1.97 |
| Air (constant pressure) | 1.005 |
| Aluminium | 0.897 |
| Glass | about 0.84 |
| Iron / steel | 0.45–0.49 |
| Copper | 0.385 |
| Lead | 0.129 |

## Phase changes need extra energy

When a substance melts or boils, energy goes into the phase change without raising temperature:

| Change (water) | Latent heat |
|---|---|
| Melting ice at 0 °C | 334 J/g |
| Boiling water at 100 °C | 2,257 J/g |

Turning 1 kg of ice at 0 °C into steam at 100 °C takes 334 + 418.6 + 2,257 = **3,010 kJ**.

## Calorimetry

When two substances at different temperatures mix, heat lost by one equals heat gained by the other:

<p class="formula">m₁c₁(T₁ − T<sub>f</sub>) = m₂c₂(T<sub>f</sub> − T₂)</p>

200 g of iron at 100 °C dropped into 500 g of water at 20 °C reaches about **23.3 °C**.

## Heating time

Time = energy ÷ power. Heating 1.5 L of water from 20 °C to 100 °C needs 502 kJ; a 2 kW kettle does it in about 4.2 minutes, ignoring losses.
''', [
 ('Why does water have such a high specific heat?', 'Hydrogen bonds between water molecules absorb energy, so more heat is needed to raise the temperature.'),
 ('What is the difference between specific heat and heat capacity?', 'Specific heat is per gram (or kg). Heat capacity is for a whole object: mass × specific heat.'),
], before="## Why water's high specific heat matters")

expand('chemistry/titration', '''
## Titration curve shapes

| Titration | pH at equivalence | Good indicator |
|---|---|---|
| Strong acid + strong base | 7 | Bromothymol blue, phenolphthalein |
| Weak acid + strong base | Above 7 (8–9) | Phenolphthalein |
| Strong acid + weak base | Below 7 (4–6) | Methyl orange, methyl red |
| Weak acid + weak base | Poorly defined | Use a pH meter |

## Mole ratios from the equation

| Reaction | Ratio (analyte per titrant) |
|---|---|
| HCl + NaOH | 1 |
| H₂SO₄ + 2NaOH | 0.5 (analyte H₂SO₄) |
| Na₂CO₃ + 2HCl | 0.5 (analyte Na₂CO₃) |
| 5Fe²⁺ + MnO₄⁻ | 5 (analyte Fe²⁺) |

Enter the ratio as moles of analyte per mole of titrant.

## Good titration practice

- Rinse the burette with titrant and the pipette with analyte before use.
- Read the burette at eye level, at the bottom of the meniscus.
- Do a rough titration first, then at least two accurate ones agreeing within 0.10 mL.
- Add titrant drop by drop near the endpoint, swirling continuously.

## Back titration

For substances that react slowly or are insoluble (such as calcium carbonate in antacids), add a known excess of acid, then titrate the leftover acid with base. The difference gives the amount that reacted.
''', [
 ('What is the titration formula?', 'C_analyte = C_titrant × V_titrant × ratio ÷ V_analyte, where ratio is moles of analyte per mole of titrant.'),
 ('What is the difference between endpoint and equivalence point?', 'The equivalence point is where reactants are exactly balanced. The endpoint is where the indicator changes colour — ideally very close to it.'),
], before='## Choosing an indicator')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/chemistry/*.mdx')):
    c = 'chemistry/' + os.path.basename(p)[:-4]; print(c, words(c))
