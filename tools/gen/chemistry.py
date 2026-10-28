import math
from page import page
C='chemistry'; U='updated: 2026-10-27'; NA=6.02214076e23; R=8.314462618

page(C,'moles',f'''
title: Moles Calculator (Mass ↔ Moles ↔ Particles)
description: Convert between grams, moles and number of particles using molar mass and Avogadro's number.
category: chemistry
keywords: [moles calculator, grams to moles, moles to grams, avogadro number, molar mass, number of molecules]
{U}
featured: true
variables:
  - {{ id: m, label: Mass, family: mass, unit: g, default: 36, min: 0 }}
  - {{ id: M, label: Molar mass, suffix: g/mol, default: 18.015, min: 0 }}
  - {{ id: n, label: Amount, suffix: mol, min: 0 }}
  - {{ id: N, label: Number of particles, min: 0 }}
equations:
  - n = m * 1000 / M
  - N = n * 6.02214076e23
faq:
  - q: How do I convert grams to moles?
    a: Divide the mass in grams by the molar mass in g/mol. 36 g of water ÷ 18.015 g/mol = 2.0 mol.
  - q: What is Avogadro's number?
    a: 6.02214076 × 10²³ — the number of particles (atoms, molecules or ions) in one mole.
  - q: Where do I find the molar mass?
    a: Add the atomic masses from the periodic table. Water, H₂O, is 2 × 1.008 + 16.00 = 18.015 g/mol.
related: [chemistry/molarity, chemistry/percent-composition, physics/ideal-gas-law]
''',f'''
## How to use this calculator

Enter the **mass** and the substance's **molar mass** to get moles and the number of particles. Or enter moles to find the mass to weigh out.

## Formulas

<p class="formula">n = m ÷ M   N = n × N<sub>A</sub></p>

## Worked example

36 g of water (M = 18.015 g/mol):

- n = 36 ÷ 18.015 = **{36/18.015:.3f} mol**
- N = {36/18.015:.3f} × 6.022 × 10²³ = **{36/18.015*NA:.3e}** molecules

## Common molar masses

| Substance | Formula | g/mol |
|---|---|---|
| Water | H₂O | 18.015 |
| Carbon dioxide | CO₂ | 44.01 |
| Sodium chloride | NaCl | 58.44 |
| Glucose | C₆H₁₂O₆ | 180.16 |
| Sulfuric acid | H₂SO₄ | 98.08 |
| Ethanol | C₂H₅OH | 46.07 |
''')

page(C,'molarity',f'''
title: Molarity Calculator
description: Calculate molarity (mol/L), the mass of solute needed, or the solution volume for any substance.
category: chemistry
keywords: [molarity calculator, molar concentration, mol/l, how to make a solution, grams needed, solution preparation]
{U}
featured: true
variables:
  - {{ id: m, label: Mass of solute, family: mass, unit: g, default: 5.844, min: 0 }}
  - {{ id: M, label: Molar mass of solute, suffix: g/mol, default: 58.44, min: 0 }}
  - {{ id: V, label: Solution volume, family: volume, unit: mL, default: 100, min: 0 }}
  - {{ id: n, label: Amount of solute, suffix: mol, min: 0 }}
  - {{ id: c, label: Molarity, suffix: mol/L, min: 0 }}
equations:
  - n = m * 1000 / M
  - c = n / (1000 * V)
faq:
  - q: What is molarity?
    a: Moles of solute per litre of solution, written M or mol/L.
  - q: How do I make 1 L of 0.1 M NaCl?
    a: Weigh 0.1 mol × 58.44 g/mol = 5.844 g of NaCl, dissolve it, then add water up to a final volume of 1 L.
  - q: Is the volume of solvent or of solution?
    a: Of the final solution. Dissolve the solute first, then top up to the mark in a volumetric flask.
related: [chemistry/dilution, chemistry/moles, chemistry/molality]
''',f'''
## How to use this calculator

Enter the **mass of solute**, its **molar mass** and the **solution volume** to get molarity. To prepare a solution, press × on Mass and type the molarity you want — the mass to weigh out is calculated.

## Formula

<p class="formula">c = n ÷ V = m ÷ (M × V)</p>

## Worked example

5.844 g of NaCl (58.44 g/mol) in 100 mL of solution:

- n = 5.844 ÷ 58.44 = 0.1 mol
- c = 0.1 ÷ 0.100 L = **1.0 mol/L**

## Preparing a solution

1. Calculate the mass needed.
2. Weigh it accurately and dissolve in less water than the final volume.
3. Transfer to a volumetric flask and fill to the mark.
4. Mix thoroughly.

To make a weaker solution from a stock, use the [dilution calculator](/chemistry/dilution/).
''')

page(C,'dilution',f'''
title: Dilution Calculator (C₁V₁ = C₂V₂)
description: Calculate how much stock solution and solvent you need to make a diluted solution — or the final concentration.
category: chemistry
keywords: [dilution calculator, c1v1 = c2v2, stock solution, dilute, serial dilution, concentration]
{U}
featured: true
variables:
  - {{ id: C1, label: Stock concentration (C₁), default: 10, min: 0 }}
  - {{ id: V1, label: Stock volume needed (V₁), family: volume, unit: mL, min: 0 }}
  - {{ id: C2, label: Final concentration (C₂), default: 0.5, min: 0 }}
  - {{ id: V2, label: Final volume (V₂), family: volume, unit: mL, default: 200, min: 0 }}
  - {{ id: Vd, label: Solvent to add, family: volume, unit: mL, min: 0 }}
equations:
  - C1 * V1 = C2 * V2
  - Vd = V2 - V1
faq:
  - q: What is the dilution formula?
    a: C₁V₁ = C₂V₂ — the amount of solute stays the same, only the volume changes.
  - q: Which concentration units can I use?
    a: Any, as long as C₁ and C₂ use the same unit — mol/L, %, mg/mL or ppm all work.
  - q: What is a dilution factor?
    a: C₁ ÷ C₂. Diluting 10 M to 0.5 M is a 20-fold dilution.
related: [chemistry/molarity, chemistry/ppm]
''',f'''
## How to use this calculator

Enter the **stock concentration**, the **final concentration** and **final volume**. You get the volume of stock to use and how much solvent to add. Any concentration unit works as long as both are the same.

## Formula

<p class="formula">C₁ V₁ = C₂ V₂</p>

## Worked example

Make 200 mL of 0.5 M solution from a 10 M stock:

- V₁ = 0.5 × 200 ÷ 10 = **10 mL** of stock
- Add **190 mL** of water

## Safety tip

When diluting strong acids, always add **acid to water**, slowly and with stirring — never water to acid.

## Serial dilutions

For very large dilutions, dilute in steps (for example 1:10 four times for 1:10,000). Each step is more accurate than one huge dilution.
''')

page(C,'ph',f'''
title: pH Calculator
description: Convert between pH, pOH, hydrogen ion and hydroxide ion concentration — with acidic or basic classification.
category: chemistry
keywords: [ph calculator, poh, hydrogen ion concentration, h+, acidic, basic, ph scale]
{U}
variables:
  - {{ id: pH, label: pH, default: 4.5 }}
  - {{ id: H, label: 'Hydrogen ion concentration [H⁺]', suffix: mol/L, min: 0 }}
  - {{ id: pOH, label: pOH }}
  - {{ id: OH, label: 'Hydroxide concentration [OH⁻]', suffix: mol/L, min: 0 }}
  - id: cls
    label: Classification (pH copy)
    bands:
      - {{ max: 6.99, label: Acidic, color: '#dc2626' }}
      - {{ max: 7.01, label: Neutral, color: '#16a34a' }}
      - {{ max: 20, label: Basic (alkaline), color: '#2563eb' }}
equations:
  - pH = -log10(H)
  - pOH = 14 - pH
  - OH = 10^(-pOH)
  - cls = pH
faq:
  - q: What is pH?
    a: A measure of acidity — the negative base-10 logarithm of hydrogen ion concentration. pH 7 is neutral at 25 °C.
  - q: How do I calculate pH from H⁺ concentration?
    a: pH = −log₁₀[H⁺]. A concentration of 1 × 10⁻³ mol/L gives pH 3.
  - q: Why does pH + pOH = 14?
    a: Because water's ion product Kw is 1.0 × 10⁻¹⁴ at 25 °C. At other temperatures the sum changes slightly.
related: [chemistry/henderson-hasselbalch, chemistry/molarity]
''',f'''
## How to use this calculator

Enter **any one** of pH, [H⁺], pOH or [OH⁻] — the rest are calculated (at 25 °C). For a strong acid like HCl, [H⁺] equals the acid concentration.

## Formulas

<p class="formula">pH = −log₁₀[H⁺]   pOH = 14 − pH   [OH⁻] = 10<sup>−pOH</sup></p>

## Worked example

pH 4.5:

- [H⁺] = 10⁻⁴·⁵ = **{10**-4.5:.2e} mol/L**
- pOH = **9.5**, [OH⁻] = **{10**-9.5:.2e} mol/L**

## pH of everyday substances

| Substance | pH |
|---|---|
| Battery acid | ~0–1 |
| Lemon juice | ~2 |
| Coffee | ~5 |
| Pure water | 7 |
| Sea water | ~8 |
| Baking soda solution | ~9 |
| Household bleach | ~12–13 |

Each pH unit is a **tenfold** change: pH 3 is ten times more acidic than pH 4.
''')

page(C,'mass-percent',f'''
title: Mass Percent (w/w) Concentration Calculator
description: Calculate mass percent concentration of a solution from solute and solvent mass — or the solute needed for a target percent.
category: chemistry
keywords: [mass percent, weight percent, w/w, percent concentration, solution concentration, percent by mass]
{U}
variables:
  - {{ id: ms, label: Mass of solute, family: mass, unit: g, default: 25, min: 0 }}
  - {{ id: mw, label: Mass of solvent, family: mass, unit: g, default: 475, min: 0 }}
  - {{ id: mt, label: Total solution mass, family: mass, unit: g, min: 0 }}
  - {{ id: w, label: Mass percent, family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - mt = ms + mw
  - w = ms / mt
faq:
  - q: What is mass percent?
    a: The mass of solute divided by the total mass of the solution, × 100. A 5% w/w salt solution has 5 g salt per 100 g of solution.
  - q: How is w/w different from w/v?
    a: w/v uses grams per 100 mL of solution instead of per 100 g. For dilute water solutions they are close; for dense solutions they differ.
  - q: How do I make 500 g of a 5% solution?
    a: Use 25 g of solute and 475 g of solvent. Press × on solute mass, set the percent and total mass.
related: [chemistry/ppm, chemistry/dilution, chemistry/molarity]
''',f'''
## How to use this calculator

Enter the **solute** and **solvent** masses to get the mass percent. To make a solution of a given strength, enter the percent and total mass — the masses of solute and solvent are calculated.

## Formula

<p class="formula">mass % = m<sub>solute</sub> ÷ (m<sub>solute</sub> + m<sub>solvent</sub>) × 100</p>

## Worked example

25 g of salt dissolved in 475 g of water:

mass % = 25 ÷ 500 = **5%**

## Common uses

- Food labels and recipes (sugar or salt content)
- Cleaning products and disinfectants
- Fertiliser and pesticide mixing
- Lab reagents where weighing is more accurate than measuring volume

For very small concentrations, use [ppm](/chemistry/ppm/) instead.
''')

page(C,'ppm',f'''
title: PPM Calculator (Parts per Million)
description: Calculate concentration in ppm from solute and solution mass — and convert ppm to percent and mg/L.
category: chemistry
keywords: [ppm calculator, parts per million, mg/l, ppm to percent, ppb, water quality, tds]
{U}
variables:
  - {{ id: ms, label: Mass of substance, family: mass, unit: mg, default: 50, min: 0 }}
  - {{ id: mt, label: Mass of sample (solution), family: mass, unit: kg, default: 1, min: 0 }}
  - {{ id: ppm, label: Concentration, suffix: ppm, min: 0 }}
  - {{ id: pct, label: As a percentage, family: percent, unit: '%', min: 0 }}
  - {{ id: ppb, label: In parts per billion, suffix: ppb, min: 0 }}
equations:
  - ppm = ms / mt * 1000000
  - pct = ppm / 1000000
  - ppb = ppm * 1000
faq:
  - q: What does ppm mean?
    a: Parts per million — 1 part of a substance in 1,000,000 parts of the whole. 1 ppm = 0.0001%.
  - q: Is ppm the same as mg/L?
    a: For dilute water solutions, yes — 1 litre of water weighs about 1 kg, so 1 mg/L ≈ 1 ppm.
  - q: How do I convert ppm to percent?
    a: Divide by 10,000. 5,000 ppm = 0.5%.
related: [chemistry/mass-percent, chemistry/dilution]
''',f'''
## How to use this calculator

Enter the **mass of the substance** and the **mass of the sample**. You get ppm, percent and ppb. For water, 1 kg ≈ 1 L, so mg/kg ≈ mg/L ≈ ppm.

## Formula

<p class="formula">ppm = m<sub>substance</sub> ÷ m<sub>sample</sub> × 10⁶</p>

## Worked example

50 mg of chlorine in 1 kg (1 L) of water:

ppm = 0.050 g ÷ 1,000 g × 10⁶ = **50 ppm** = 0.005%

## Typical values

| Example | Concentration |
|---|---|
| Drinking-water chlorine (typical) | 0.2–1 ppm |
| WHO drinking-water fluoride limit | 1.5 ppm |
| CO₂ in air | ~420 ppm |
| Sea-water salt | ~35,000 ppm |

## Conversions

1% = 10,000 ppm · 1 ppm = 1,000 ppb · 1 ppm = 1 mg/kg
''')

page(C,'percent-yield',f'''
title: Percent Yield Calculator
description: Calculate the percent yield of a chemical reaction from the actual and theoretical yield.
category: chemistry
keywords: [percent yield, theoretical yield, actual yield, reaction yield, chemistry yield calculator]
{U}
variables:
  - {{ id: a, label: Actual yield, family: mass, unit: g, default: 8.5, min: 0 }}
  - {{ id: t, label: Theoretical yield, family: mass, unit: g, default: 10, min: 0 }}
  - {{ id: y, label: Percent yield, family: percent, unit: '%', min: 0 }}
equations:
  - y = a / t
faq:
  - q: What is percent yield?
    a: How much product you actually obtained compared with the maximum possible, × 100.
  - q: Why is yield usually below 100%?
    a: Incomplete reactions, side reactions, and product lost during filtering, transfer or purification.
  - q: Can yield be over 100%?
    a: Only through error — usually the product is still wet or contains impurities.
related: [chemistry/moles, chemistry/percent-composition]
''',f'''
## How to use this calculator

Enter the **actual yield** you obtained and the **theoretical yield** calculated from stoichiometry. Or enter an expected percent yield to see how much product to expect.

## Formula

<p class="formula">% yield = actual ÷ theoretical × 100</p>

## Worked example

Theoretical yield 10.0 g, actual product 8.5 g:

% yield = 8.5 ÷ 10.0 = **85%**

## Finding the theoretical yield

1. Convert the limiting reagent's mass to moles (use the [moles calculator](/chemistry/moles/)).
2. Use the balanced equation's mole ratio to find moles of product.
3. Multiply by the product's molar mass.

## Typical yields

Simple one-step lab reactions often give 70–95%. Multi-step syntheses multiply losses: five steps at 80% each give an overall yield of only 33%.
''')

page(C,'half-life',f'''
title: Half-Life Calculator (Radioactive Decay)
description: Calculate the amount remaining after radioactive decay — or the half-life or time elapsed.
category: chemistry
keywords: [half life calculator, radioactive decay, decay calculator, carbon dating, exponential decay]
{U}
variables:
  - {{ id: N0, label: Initial amount, default: 100, min: 0 }}
  - {{ id: T, label: Half-life, family: time, unit: yr, default: 5730, min: 0 }}
  - {{ id: t, label: Time elapsed, family: time, unit: yr, default: 10000, min: 0 }}
  - {{ id: N, label: Amount remaining, min: 0 }}
  - {{ id: pct, label: Fraction remaining, family: percent, unit: '%', min: 0 }}
equations:
  - N = N0 * 0.5^(t / T)
  - pct = N / N0
chart: {{ x: t, y: N, from: 0, to: 30000 }}
faq:
  - q: What is half-life?
    a: The time it takes for half of a radioactive substance to decay. After two half-lives a quarter remains, after three an eighth, and so on.
  - q: How does carbon dating work?
    a: Living things keep a steady level of carbon-14. After death it decays with a half-life of about 5,730 years, so the remaining fraction gives the age.
  - q: Can this be used for medicines?
    a: Yes — drug elimination half-lives follow the same maths. Enter hours instead of years.
related: [chemistry/arrhenius-equation, math/logarithm]
''',f'''
## How to use this calculator

Enter the **initial amount**, **half-life** and **time elapsed** to get the amount remaining. Or enter the remaining amount to find the age (time elapsed) or the half-life. Time units can be years, days, hours, minutes or seconds.

## Formula

<p class="formula">N = N₀ × (½)<sup>t / T½</sup></p>

## Worked example — carbon-14

Half-life 5,730 years. After 10,000 years, of 100 units:

N = 100 × 0.5<sup>10,000/5,730</sup> = **{100*0.5**(10000/5730):.1f}** units remaining ({0.5**(10000/5730)*100:.1f}%)

## Common half-lives

| Isotope | Half-life |
|---|---|
| Iodine-131 | 8.0 days |
| Cobalt-60 | 5.27 years |
| Caesium-137 | 30.1 years |
| Carbon-14 | 5,730 years |
| Uranium-238 | 4.47 billion years |
''')

page(C,'boyles-law',f'''
title: Boyle's Law Calculator (P₁V₁ = P₂V₂)
description: Calculate new pressure or volume of a gas at constant temperature using Boyle's law.
category: chemistry
keywords: [boyles law, p1v1 = p2v2, gas pressure volume, constant temperature, gas law calculator]
{U}
variables:
  - {{ id: P1, label: Initial pressure (absolute), family: pressure, unit: kPa, imperialUnit: psi, default: 100, min: 0 }}
  - {{ id: V1, label: Initial volume, family: volume, unit: L, default: 10, min: 0 }}
  - {{ id: P2, label: Final pressure (absolute), family: pressure, unit: kPa, imperialUnit: psi, default: 250, min: 0 }}
  - {{ id: V2, label: Final volume, family: volume, unit: L, min: 0 }}
equations:
  - P1 * V1 = P2 * V2
chart: {{ x: P2, y: V2, from: 50, to: 500 }}
faq:
  - q: What is Boyle's law?
    a: At constant temperature, the pressure of a fixed amount of gas is inversely proportional to its volume — P₁V₁ = P₂V₂.
  - q: Do I need absolute pressure?
    a: Yes. Add atmospheric pressure (about 101.3 kPa) to gauge readings.
  - q: Where is Boyle's law seen in daily life?
    a: Syringes, bicycle pumps, scuba diving (air spaces shrink with depth) and air compressors.
related: [chemistry/charles-law, chemistry/combined-gas-law, physics/ideal-gas-law]
''',f'''
## How to use this calculator

Enter **any three** of the initial and final pressure and volume. The fourth is calculated. Temperature and the amount of gas must stay constant.

## Formula

<p class="formula">P₁ V₁ = P₂ V₂</p>

## Worked example

10 L of gas at 100 kPa is compressed to 250 kPa:

V₂ = 100 × 10 ÷ 250 = **4 L**

## Diving example

At 10 m depth, the absolute pressure is about 2 atm, so a lungful of air from the surface shrinks to half its volume — which is why divers must never hold their breath while ascending.
''')

page(C,'charles-law',f'''
title: Charles's Law Calculator (V₁/T₁ = V₂/T₂)
description: Calculate new volume or temperature of a gas at constant pressure using Charles's law.
category: chemistry
keywords: [charles law, v1/t1 = v2/t2, gas volume temperature, constant pressure, gas law calculator]
{U}
variables:
  - {{ id: V1, label: Initial volume, family: volume, unit: L, default: 2, min: 0 }}
  - {{ id: T1, label: Initial temperature, family: temperature, unit: C, imperialUnit: F, default: 20, min: 0 }}
  - {{ id: V2, label: Final volume, family: volume, unit: L, min: 0 }}
  - {{ id: T2, label: Final temperature, family: temperature, unit: C, imperialUnit: F, default: 80, min: 0 }}
equations:
  - V1 / T1 = V2 / T2
faq:
  - q: What is Charles's law?
    a: At constant pressure, a gas's volume is proportional to its absolute temperature — V₁/T₁ = V₂/T₂.
  - q: Why must temperatures be in kelvin?
    a: The law is based on absolute zero. The calculator converts °C and °F to kelvin for you.
  - q: Where is it seen in daily life?
    a: Hot-air balloons rising, balloons shrinking in a freezer, and tyre pressure warnings in cold weather.
related: [chemistry/boyles-law, chemistry/combined-gas-law, physics/ideal-gas-law]
''',f'''
## How to use this calculator

Enter **any three** of the initial and final volume and temperature. The fourth is calculated. Pressure and amount of gas stay constant.

## Formula

<p class="formula">V₁ ÷ T₁ = V₂ ÷ T₂   (T in kelvin)</p>

## Worked example

A 2 L balloon is warmed from 20 °C (293.15 K) to 80 °C (353.15 K):

V₂ = 2 × 353.15 ÷ 293.15 = **{2*353.15/293.15:.2f} L**

## A common mistake

Using °C directly would suggest the volume quadruples (80 ÷ 20) — completely wrong. Always use absolute temperature.
''')

page(C,'combined-gas-law',f'''
title: Combined Gas Law Calculator
description: Solve P₁V₁/T₁ = P₂V₂/T₂ for any unknown — pressure, volume or temperature of a fixed amount of gas.
category: chemistry
keywords: [combined gas law, p1v1/t1 = p2v2/t2, gas law calculator, pressure volume temperature]
{U}
variables:
  - {{ id: P1, label: Initial pressure (absolute), family: pressure, unit: kPa, imperialUnit: psi, default: 101.325, min: 0 }}
  - {{ id: V1, label: Initial volume, family: volume, unit: L, default: 10, min: 0 }}
  - {{ id: T1, label: Initial temperature, family: temperature, unit: C, imperialUnit: F, default: 25, min: 0 }}
  - {{ id: P2, label: Final pressure (absolute), family: pressure, unit: kPa, imperialUnit: psi, default: 200, min: 0 }}
  - {{ id: V2, label: Final volume, family: volume, unit: L, min: 0 }}
  - {{ id: T2, label: Final temperature, family: temperature, unit: C, imperialUnit: F, default: 60, min: 0 }}
equations:
  - P1 * V1 / T1 = P2 * V2 / T2
faq:
  - q: What is the combined gas law?
    a: It combines Boyle's, Charles's and Gay-Lussac's laws — P₁V₁/T₁ = P₂V₂/T₂ for a fixed amount of gas.
  - q: When should I use the ideal gas law instead?
    a: When you need the amount of gas (moles). The combined law only compares two states of the same gas sample.
  - q: Which units must I use?
    a: Absolute pressure and absolute temperature. The calculator converts units automatically.
related: [chemistry/boyles-law, chemistry/charles-law, physics/ideal-gas-law]
''',f'''
## How to use this calculator

Enter **five** of the six values (initial and final pressure, volume and temperature) to get the sixth.

## Formula

<p class="formula">P₁V₁ ÷ T₁ = P₂V₂ ÷ T₂</p>

## Worked example

10 L of air at 101.325 kPa and 25 °C is compressed to 200 kPa and warms to 60 °C:

V₂ = 101.325 × 10 × 333.15 ÷ (298.15 × 200) = **{101.325*10*333.15/(298.15*200):.2f} L**

## Special cases

- Constant temperature → Boyle's law (P₁V₁ = P₂V₂)
- Constant pressure → Charles's law (V₁/T₁ = V₂/T₂)
- Constant volume → Gay-Lussac's law (P₁/T₁ = P₂/T₂)
''')

page(C,'specific-heat',f'''
title: Specific Heat Calculator (q = mcΔT)
description: Calculate heat energy needed to change a substance's temperature — or the temperature change from added heat.
category: chemistry
keywords: [specific heat capacity, q = mc delta t, heat energy, calorimetry, joules, temperature change]
{U}
variables:
  - {{ id: m, label: Mass, family: mass, unit: g, default: 500, min: 0 }}
  - id: c
    label: Substance (specific heat)
    default: 4.186
    options:
      - {{ label: Water (4.186 J/g·K), value: 4.186 }}
      - {{ label: Ice (2.09 J/g·K), value: 2.09 }}
      - {{ label: Aluminium (0.897 J/g·K), value: 0.897 }}
      - {{ label: Copper (0.385 J/g·K), value: 0.385 }}
      - {{ label: Iron / steel (0.45 J/g·K), value: 0.45 }}
      - {{ label: Glass (0.84 J/g·K), value: 0.84 }}
      - {{ label: Olive oil (1.97 J/g·K), value: 1.97 }}
      - {{ label: Air (1.005 J/g·K), value: 1.005 }}
  - {{ id: dT, label: Temperature change, family: tempdiff, unit: K, imperialUnit: F, default: 80 }}
  - {{ id: q, label: Heat energy, family: energy, unit: kJ }}
equations:
  - q = m * 1000 * c * dT
faq:
  - q: What is specific heat capacity?
    a: The energy needed to raise 1 gram of a substance by 1 °C (or 1 K). Water's is unusually high at 4.186 J/g·K.
  - q: How much energy to boil water for tea?
    a: Heating 500 g of water from 20 °C to 100 °C needs about 167 kJ — about 0.046 kWh.
  - q: Does this include melting or boiling?
    a: No. Phase changes need extra latent heat (334 J/g to melt ice, 2,257 J/g to boil water).
related: [engineering/heat-duty, conversion/energy-converter]
''',f'''
## How to use this calculator

Choose the **substance**, then enter the **mass** and **temperature change**. The heat energy needed is calculated. Or enter the energy to find the temperature rise.

## Formula

<p class="formula">q = m × c × ΔT</p>

## Worked example

Heating 500 g of water from 20 °C to 100 °C (ΔT = 80 K):

q = 500 × 4.186 × 80 = **{500*4.186*80/1000:.1f} kJ** ({500*4.186*80/3.6e6:.3f} kWh)

A 2 kW kettle would take about {500*4.186*80/2000:.0f} s (plus losses).

## Why water's high specific heat matters

Water absorbs a lot of heat with only a small temperature rise — which is why it is used in cooling systems, central heating and why coastal climates are milder.
''')

page(C,'molality',f'''
title: Molality Calculator
description: Calculate molality (mol/kg) from the mass of solute, its molar mass and the mass of solvent.
category: chemistry
keywords: [molality calculator, mol/kg, molal concentration, solute solvent, colligative properties]
{U}
variables:
  - {{ id: ms, label: Mass of solute, family: mass, unit: g, default: 11.69, min: 0 }}
  - {{ id: M, label: Molar mass of solute, suffix: g/mol, default: 58.44, min: 0 }}
  - {{ id: mw, label: Mass of solvent, family: mass, unit: kg, default: 0.5, min: 0 }}
  - {{ id: n, label: Moles of solute, suffix: mol, min: 0 }}
  - {{ id: b, label: Molality, suffix: mol/kg, min: 0 }}
equations:
  - n = ms * 1000 / M
  - b = n / mw
faq:
  - q: What is molality?
    a: Moles of solute per kilogram of solvent (mol/kg), written m.
  - q: How is molality different from molarity?
    a: Molarity uses litres of solution; molality uses kilograms of solvent. Molality does not change with temperature, because mass does not.
  - q: Where is molality used?
    a: In colligative properties — boiling point elevation, freezing point depression and osmotic pressure.
related: [chemistry/molarity, chemistry/moles]
''',f'''
## How to use this calculator

Enter the **mass of solute**, its **molar mass** and the **mass of solvent** (not solution). The moles of solute and molality are calculated.

## Formula

<p class="formula">b = n<sub>solute</sub> ÷ m<sub>solvent</sub> (kg)</p>

## Worked example

11.69 g of NaCl (58.44 g/mol) in 0.5 kg of water:

- n = 11.69 ÷ 58.44 = 0.2 mol
- b = 0.2 ÷ 0.5 = **0.4 mol/kg**

## Freezing point depression

ΔT<sub>f</sub> = i × K<sub>f</sub> × b. For water, K<sub>f</sub> = 1.86 K·kg/mol; NaCl gives i ≈ 2. This solution freezes about 2 × 1.86 × 0.4 = **1.5 °C** below 0 °C — the principle behind salting roads.
''')

page(C,'percent-composition',f'''
title: Percent Composition Calculator
description: Calculate the mass percent of an element in a compound from atom count, atomic mass and molar mass.
category: chemistry
keywords: [percent composition, mass percent of element, element percentage, compound composition, empirical formula]
{U}
variables:
  - {{ id: k, label: Number of atoms of the element in the formula, default: 2, min: 0 }}
  - {{ id: Ar, label: Atomic mass of the element, suffix: g/mol, default: 1.008, min: 0 }}
  - {{ id: M, label: Molar mass of the compound, suffix: g/mol, default: 18.015, min: 0 }}
  - {{ id: p, label: Percent by mass, family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - p = k * Ar / M
faq:
  - q: How do I find the percent composition of an element?
    a: Multiply the number of atoms by the atomic mass, divide by the compound's molar mass, and multiply by 100.
  - q: What is the percent of oxygen in water?
    a: 16.00 ÷ 18.015 = 88.8%. Hydrogen makes up the other 11.2%.
  - q: Do the percentages add to 100?
    a: Yes — the percentages of all elements in a compound total 100% (within rounding).
related: [chemistry/moles, chemistry/percent-yield]
''',f'''
## How to use this calculator

Enter how many **atoms** of the element are in the formula, the element's **atomic mass** and the compound's **molar mass**. Repeat for each element to get the full composition.

## Formula

<p class="formula">% element = (atoms × atomic mass) ÷ molar mass × 100</p>

## Worked example — water (H₂O)

- Hydrogen: 2 × 1.008 ÷ 18.015 = **{2*1.008/18.015*100:.1f}%**
- Oxygen: 1 × 15.999 ÷ 18.015 = **{15.999/18.015*100:.1f}%**

## More examples

| Compound | Element | % by mass |
|---|---|---|
| CO₂ (44.01) | C | {12.011/44.01*100:.1f}% |
| NaCl (58.44) | Na | {22.99/58.44*100:.1f}% |
| C₆H₁₂O₆ (180.16) | C | {6*12.011/180.16*100:.1f}% |
| Fe₂O₃ (159.69) | Fe | {2*55.845/159.69*100:.1f}% |
''')

pka=4.76
page(C,'henderson-hasselbalch',f'''
title: Buffer pH Calculator (Henderson–Hasselbalch)
description: Calculate buffer pH from pKa and the concentrations of weak acid and conjugate base — or the ratio needed for a target pH.
category: chemistry
keywords: [henderson hasselbalch, buffer ph, pka, buffer calculator, acetate buffer, conjugate base]
{U}
variables:
  - {{ id: pKa, label: pKa of the weak acid, default: 4.76 }}
  - {{ id: A, label: 'Conjugate base concentration [A⁻]', suffix: mol/L, default: 0.15, min: 0 }}
  - {{ id: HA, label: 'Weak acid concentration [HA]', suffix: mol/L, default: 0.10, min: 0 }}
  - {{ id: pH, label: Buffer pH }}
equations:
  - pH = pKa + log10(A / HA)
faq:
  - q: What is the Henderson–Hasselbalch equation?
    a: pH = pKa + log₁₀([A⁻]/[HA]). It estimates the pH of a buffer made from a weak acid and its conjugate base.
  - q: When is a buffer most effective?
    a: When pH is close to pKa (within about ±1), where the acid and base concentrations are similar.
  - q: What is the pKa of acetic acid?
    a: About 4.76 at 25 °C.
related: [chemistry/ph, chemistry/molarity]
''',f'''
## How to use this calculator

Enter the acid's **pKa** and the concentrations of the **conjugate base** and **weak acid**. The buffer pH is calculated. To design a buffer, enter the target pH and one concentration to find the other.

## Formula

<p class="formula">pH = pK<sub>a</sub> + log₁₀([A⁻] ÷ [HA])</p>

## Worked example — acetate buffer

pKa 4.76, [acetate] = 0.15 M, [acetic acid] = 0.10 M:

pH = 4.76 + log₁₀(1.5) = **{pka+math.log10(1.5):.2f}**

## Common buffer systems

| Buffer | pKa (25 °C) | Useful pH range |
|---|---|---|
| Acetate | 4.76 | 3.8–5.8 |
| Phosphate (H₂PO₄⁻/HPO₄²⁻) | 7.21 | 6.2–8.2 |
| Tris | 8.07 | 7.1–9.1 |
| Bicarbonate (blood) | 6.35 | 5.4–7.4 |
''')

Ea=50; T1=298.15; A=1e10
k1=A*math.exp(-Ea*1000/(R*T1)); k2=A*math.exp(-Ea*1000/(R*308.15))
page(C,'arrhenius-equation',f'''
title: Arrhenius Equation Calculator
description: Calculate the reaction rate constant from activation energy, temperature and pre-exponential factor.
category: chemistry
keywords: [arrhenius equation, activation energy, rate constant, reaction rate temperature, kinetics]
{U}
variables:
  - {{ id: A, label: Pre-exponential factor (A), default: 10000000000, min: 0 }}
  - {{ id: Ea, label: Activation energy, suffix: kJ/mol, default: 50, min: 0 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, imperialUnit: F, default: 25, min: 0 }}
  - {{ id: k, label: Rate constant (same units as A), min: 0 }}
equations:
  - k = A * exp(-Ea * 1000 / (8.314462618 * T))
chart: {{ x: T, y: k, from: 0, to: 100 }}
faq:
  - q: What does the Arrhenius equation show?
    a: How the rate of a reaction increases with temperature, depending on the activation energy.
  - q: Is it true that reactions double every 10 °C?
    a: Roughly, for activation energies around 50 kJ/mol near room temperature. It is a rule of thumb, not a law.
  - q: What units does k have?
    a: The same as A, which depends on the reaction order (for example s⁻¹ for first-order reactions).
related: [chemistry/half-life, chemistry/gibbs-free-energy]
''',f'''
## How to use this calculator

Enter the **pre-exponential factor**, **activation energy** and **temperature**. The rate constant is calculated. The chart shows how sharply k rises with temperature.

## Formula

<p class="formula">k = A × e<sup>−Ea / (RT)</sup>   (R = 8.314 J/mol·K)</p>

## Worked example

A = 1 × 10¹⁰ s⁻¹, Ea = 50 kJ/mol:

- At 25 °C: k = **{k1:.3g} s⁻¹**
- At 35 °C: k = **{k2:.3g} s⁻¹** — about **{k2/k1:.2f}×** faster

## Why it matters

- Food spoils more slowly in a fridge.
- Industrial reactors are heated to speed up production.
- Catalysts work by lowering Ea, raising k without extra heat.
''')

page(C,'gibbs-free-energy',f'''
title: Gibbs Free Energy Calculator (ΔG = ΔH − TΔS)
description: Calculate Gibbs free energy change to predict whether a reaction is spontaneous at a given temperature.
category: chemistry
keywords: [gibbs free energy, delta g, spontaneous reaction, enthalpy, entropy, thermodynamics]
{U}
variables:
  - {{ id: dH, label: Enthalpy change ΔH, suffix: kJ/mol, default: -92.2 }}
  - {{ id: dS, label: Entropy change ΔS, suffix: J/mol·K, default: -198.7 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, imperialUnit: F, default: 25, min: 0 }}
  - id: dG
    label: Gibbs free energy ΔG
    suffix: kJ/mol
    bands:
      - {{ max: -0.0001, label: Spontaneous (favourable), color: '#16a34a' }}
      - {{ max: 0.0001, label: At equilibrium, color: '#eab308' }}
      - {{ max: 1e12, label: Non-spontaneous, color: '#dc2626' }}
equations:
  - dG = dH - T * dS / 1000
chart: {{ x: T, y: dG, from: 0, to: 600 }}
faq:
  - q: What does a negative ΔG mean?
    a: The reaction is thermodynamically favourable (spontaneous) at that temperature. It says nothing about how fast it happens.
  - q: At what temperature does a reaction become spontaneous?
    a: Where ΔG = 0, so T = ΔH ÷ ΔS. Press × on Temperature and set ΔG to 0.
  - q: Why are units mixed?
    a: ΔH is usually given in kJ/mol and ΔS in J/mol·K. The calculator divides ΔS by 1,000 for you.
related: [chemistry/arrhenius-equation, chemistry/specific-heat]
''',f'''
## How to use this calculator

Enter **ΔH** (kJ/mol), **ΔS** (J/mol·K) and the **temperature**. ΔG is calculated and labelled spontaneous or not.

## Formula

<p class="formula">ΔG = ΔH − T ΔS</p>

## Worked example — ammonia synthesis

N₂ + 3H₂ → 2NH₃, ΔH = −92.2 kJ/mol, ΔS = −198.7 J/mol·K, at 25 °C:

ΔG = −92.2 − 298.15 × (−0.1987) = **{-92.2+298.15*0.1987:.1f} kJ/mol** → spontaneous

It stops being spontaneous above T = 92.2 ÷ 0.1987 ≈ {92.2/0.1987:.0f} K ({92.2/0.1987-273.15:.0f} °C).

## The four cases

| ΔH | ΔS | Spontaneous? |
|---|---|---|
| − | + | Always |
| + | − | Never |
| − | − | At low temperatures |
| + | + | At high temperatures |
''')

page(C,'beer-lambert',f'''
title: Beer–Lambert Law Calculator (Absorbance)
description: Calculate absorbance, concentration or molar absorptivity using A = εlc, plus transmittance.
category: chemistry
keywords: [beer lambert law, absorbance calculator, spectrophotometry, molar absorptivity, transmittance, a = elc]
{U}
variables:
  - {{ id: eps, label: Molar absorptivity ε, suffix: L/(mol·cm), default: 6220, min: 0 }}
  - {{ id: l, label: Path length, suffix: cm, default: 1, min: 0 }}
  - {{ id: c, label: Concentration, suffix: mol/L, default: 0.0001, min: 0 }}
  - {{ id: A, label: Absorbance, min: 0, decimals: 4 }}
  - {{ id: T, label: Transmittance, family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - A = eps * l * c
  - T = 10^(-A)
faq:
  - q: What is the Beer–Lambert law?
    a: Absorbance is proportional to concentration and path length — A = ε × l × c.
  - q: How do I find concentration from absorbance?
    a: Divide absorbance by (ε × l). Press × on Concentration and type the measured absorbance.
  - q: What absorbance range is reliable?
    a: Usually about 0.1–1.0. Above roughly 1.5–2, very little light gets through and readings become inaccurate.
related: [chemistry/molarity, chemistry/dilution]
''',f'''
## How to use this calculator

Enter the **molar absorptivity**, **path length** and **concentration** to get absorbance and transmittance — or enter a measured absorbance to find the concentration.

## Formulas

<p class="formula">A = ε l c   T = 10<sup>−A</sup></p>

## Worked example — NADH at 340 nm

ε = 6,220 L/(mol·cm), 1 cm cuvette, c = 1 × 10⁻⁴ mol/L:

- A = 6,220 × 1 × 0.0001 = **0.622**
- T = 10⁻⁰·⁶²² = **{10**-0.622*100:.1f}%**

## Absorbance vs transmittance

| Absorbance | Light transmitted |
|---|---|
| 0 | 100% |
| 0.3 | 50% |
| 1 | 10% |
| 2 | 1% |
''')

page(C,'titration',f'''
title: Titration Calculator
description: Calculate the unknown concentration of an acid or base from titration volumes and the mole ratio.
category: chemistry
keywords: [titration calculator, acid base titration, unknown concentration, equivalence point, mavb, neutralisation]
{U}
variables:
  - {{ id: Ct, label: Titrant concentration, suffix: mol/L, default: 0.1, min: 0 }}
  - {{ id: Vt, label: Titrant volume used, family: volume, unit: mL, default: 23.4, min: 0 }}
  - {{ id: r, label: Mole ratio (analyte per titrant), default: 1, min: 0, help: From the balanced equation. NaOH + HCl → 1; NaOH with H₂SO₄ → 0.5 }}
  - {{ id: Va, label: Analyte volume, family: volume, unit: mL, default: 25, min: 0 }}
  - {{ id: Ca, label: Analyte concentration, suffix: mol/L, min: 0 }}
equations:
  - Ca * Va = r * Ct * Vt
faq:
  - q: How do I calculate concentration from a titration?
    a: Moles of titrant = concentration × volume. Use the mole ratio from the balanced equation to get moles of analyte, then divide by the analyte volume.
  - q: What is the mole ratio for sulfuric acid with NaOH?
    a: H₂SO₄ + 2NaOH → products, so 1 mol acid reacts with 2 mol NaOH. The ratio of analyte (acid) per titrant (NaOH) is 0.5.
  - q: How many titrations should I do?
    a: Repeat until you get at least two concordant results (within about 0.1 mL) and average them.
related: [chemistry/molarity, chemistry/ph]
''',f'''
## How to use this calculator

Enter the **titrant concentration** and **volume used**, the **mole ratio** from the balanced equation and the **analyte volume**. The analyte's concentration is calculated.

## Formula

<p class="formula">C<sub>a</sub> V<sub>a</sub> = r × C<sub>t</sub> V<sub>t</sub></p>

## Worked example

23.4 mL of 0.1 M NaOH neutralises 25.0 mL of HCl (ratio 1):

C<sub>HCl</sub> = 0.1 × 23.4 ÷ 25.0 = **{0.1*23.4/25:.4f} mol/L**

For 25.0 mL of H₂SO₄ instead (ratio 0.5): **{0.5*0.1*23.4/25:.4f} mol/L**.

## Choosing an indicator

| Titration | Indicator |
|---|---|
| Strong acid – strong base | Phenolphthalein or methyl orange |
| Weak acid – strong base | Phenolphthalein |
| Strong acid – weak base | Methyl orange |
''')

page(C,'osmotic-pressure',f'''
title: Osmotic Pressure Calculator
description: Calculate osmotic pressure from molarity, van 't Hoff factor and temperature using π = iMRT.
category: chemistry
keywords: [osmotic pressure, van't hoff, pi = imrt, osmosis, reverse osmosis, colligative properties]
{U}
variables:
  - {{ id: i, label: van 't Hoff factor (i), default: 2, min: 0, help: 1 for sugar, about 2 for NaCl, about 3 for CaCl₂ }}
  - {{ id: c, label: Molarity, suffix: mol/L, default: 0.15, min: 0 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, imperialUnit: F, default: 37, min: 0 }}
  - {{ id: P, label: Osmotic pressure, family: pressure, unit: atm, imperialUnit: psi, min: 0 }}
equations:
  - P = i * c * 1000 * 8.314462618 * T
faq:
  - q: What is osmotic pressure?
    a: The pressure needed to stop water flowing through a semi-permeable membrane into a more concentrated solution.
  - q: What is the van 't Hoff factor?
    a: The number of particles a substance forms in solution. Sugar stays as one molecule (i = 1); NaCl splits into Na⁺ and Cl⁻ (i ≈ 2).
  - q: Why does reverse osmosis need high pressure?
    a: Sea water has an osmotic pressure of about 27 bar, so desalination plants apply 50–80 bar to push fresh water through the membrane.
related: [chemistry/molarity, chemistry/molality]
''',f'''
## How to use this calculator

Enter the **van 't Hoff factor**, **molarity** and **temperature**. The osmotic pressure appears in atm, bar, kPa or psi.

## Formula

<p class="formula">π = i M R T</p>

## Worked example — saline at body temperature

0.15 M NaCl (i = 2) at 37 °C (310.15 K):

π = 2 × 150 mol/m³ × 8.314 × 310.15 = {2*150*R*310.15/1000:.0f} kPa = **{2*150*R*310.15/101325:.2f} atm**

This is close to the osmotic pressure of blood, which is why 0.9% saline is used for IV fluids.
''')
print('chemistry ok')
