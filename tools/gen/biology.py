import math
from page import page
C='biology'; U='updated: 2026-10-27'

page(C,'dna-concentration',f'''
title: DNA / RNA Concentration Calculator (A260)
description: Calculate nucleic acid concentration from A260 absorbance for dsDNA, ssDNA and RNA, including dilution and purity ratio.
category: biology
keywords: [dna concentration, a260, rna concentration, nanodrop, 260/280 ratio, nucleic acid quantification]
{U}
featured: true
variables:
  - id: f
    label: Nucleic acid type
    default: 50
    options:
      - {{ label: Double-stranded DNA (50 µg/mL per A260), value: 50 }}
      - {{ label: RNA (40 µg/mL per A260), value: 40 }}
      - {{ label: Single-stranded DNA (33 µg/mL per A260), value: 33 }}
  - {{ id: a260, label: A260 reading, default: 0.45, min: 0 }}
  - {{ id: a280, label: A280 reading, default: 0.24, min: 0 }}
  - {{ id: dil, label: Dilution factor, default: 10, min: 1 }}
  - {{ id: c, label: Concentration, suffix: µg/mL (= ng/µL), min: 0 }}
  - {{ id: ratio, label: A260/A280 purity ratio, min: 0, decimals: 2 }}
equations:
  - c = a260 * f * dil
  - ratio = a260 / a280
faq:
  - q: How do I calculate DNA concentration from A260?
    a: Concentration (µg/mL) = A260 × 50 × dilution factor for double-stranded DNA. Use 40 for RNA and 33 for single-stranded DNA.
  - q: What is a good 260/280 ratio?
    a: About 1.8 for pure DNA and about 2.0 for pure RNA. Lower values suggest protein or phenol contamination.
  - q: Are µg/mL and ng/µL the same?
    a: Yes, they are equal.
related: [biology/dna-copy-number, biology/protein-concentration-a280, chemistry/beer-lambert]
''',f'''
## How to use this calculator

Choose the **nucleic acid type**, enter the **A260** and **A280** readings and the **dilution factor**. The concentration and purity ratio are calculated.

## Formula

<p class="formula">c (µg/mL) = A260 × conversion factor × dilution</p>

## Example

dsDNA diluted 1:10 with A260 = 0.45 and A280 = 0.24:

- Concentration = 0.45 × 50 × 10 = **225 µg/mL**
- A260/A280 = **{0.45/0.24:.2f}** → acceptable purity

## Reliable readings

Spectrophotometers are most accurate for A260 between about 0.1 and 1.0. Dilute concentrated samples and multiply back with the dilution factor.
''')

N0,N,t=1e5,8e5,6
page(C,'cell-doubling-time',f'''
title: Cell Doubling Time Calculator
description: Calculate population doubling time and growth rate from starting and final cell counts over a time interval.
category: biology
keywords: [doubling time, cell doubling time, population doubling, cell culture growth, generation time]
{U}
featured: true
variables:
  - {{ id: N0, label: Initial cell count, default: 100000, min: 0 }}
  - {{ id: N, label: Final cell count, default: 800000, min: 0 }}
  - {{ id: t, label: Time elapsed, family: time, unit: h, default: 72, min: 0 }}
  - {{ id: td, label: Doubling time, family: time, unit: h, min: 0 }}
  - {{ id: nd, label: Number of doublings, min: 0, decimals: 2 }}
equations:
  - nd = log2(N / N0)
  - td = t / nd
faq:
  - q: How is doubling time calculated?
    a: Doubling time = time × ln 2 ÷ ln(final ÷ initial), which is the same as time divided by the number of doublings.
  - q: Should I use cells in log phase?
    a: Yes. Doubling time is only meaningful during exponential (log-phase) growth.
  - q: What is a typical doubling time?
    a: E. coli can double in about 20 minutes in rich media; many mammalian cell lines take 18–36 hours.
related: [biology/bacterial-growth, biology/specific-growth-rate, biology/hemocytometer]
''',f'''
## How to use this calculator

Enter the **initial** and **final cell counts** and the **time** between them. The number of doublings and the doubling time are calculated.

## Formulas

<p class="formula">doublings = log₂(N ÷ N₀)   T<sub>d</sub> = t ÷ doublings</p>

## Example

Cells grow from 100,000 to 800,000 in 72 hours:

- Doublings = log₂(8) = **3**
- Doubling time = 72 ÷ 3 = **24 hours**
''')

page(C,'bacterial-growth',f'''
title: Bacterial Growth Calculator
description: Predict bacterial population after a given time from the starting count and generation (doubling) time.
category: biology
keywords: [bacterial growth calculator, generation time, exponential growth bacteria, bacteria population, microbiology]
{U}
variables:
  - {{ id: N0, label: Starting population, default: 1000, min: 0 }}
  - {{ id: td, label: Generation (doubling) time, family: time, unit: min, default: 20, min: 0 }}
  - {{ id: t, label: Time, family: time, unit: h, default: 4, min: 0 }}
  - {{ id: g, label: Generations, min: 0, decimals: 1 }}
  - {{ id: N, label: Final population, min: 0 }}
equations:
  - g = t / td
  - N = N0 * 2^g
chart: {{ x: t, y: N, from: 0, to: 6 }}
faq:
  - q: How fast do bacteria grow?
    a: Under ideal conditions E. coli divides about every 20 minutes. Many other bacteria take hours.
  - q: Does growth continue forever?
    a: No. Nutrients run out and waste builds up, so growth slows into a stationary phase. This calculator models the exponential phase only.
  - q: Why does food left out become unsafe so quickly?
    a: Starting from 1,000 bacteria with a 20-minute generation time, there are over 4 million after 4 hours.
related: [biology/cell-doubling-time, biology/logistic-growth]
''',f'''
## How to use this calculator

Enter the **starting population**, the **generation time** and the **time** elapsed. The number of generations and the final population are calculated.

## Formula

<p class="formula">N = N₀ × 2<sup>t ÷ T<sub>d</sub></sup></p>

## Example

1,000 bacteria with a 20-minute generation time, after 4 hours:

- Generations = 240 ÷ 20 = **12**
- N = 1,000 × 2¹² = **{1000*2**12:,}**
''')

page(C,'hardy-weinberg',f'''
title: Hardy–Weinberg Equilibrium Calculator
description: Calculate allele and genotype frequencies (p, q, p², 2pq, q²) from the frequency of the recessive phenotype.
category: biology
keywords: [hardy weinberg, allele frequency, genotype frequency, p2 + 2pq + q2, population genetics, carrier frequency]
{U}
variables:
  - {{ id: qq, label: Recessive phenotype frequency (q²), family: percent, unit: '%', default: 4, min: 0, max: 1 }}
  - {{ id: q, label: Recessive allele frequency (q), min: 0, max: 1, decimals: 4 }}
  - {{ id: p, label: Dominant allele frequency (p), min: 0, max: 1, decimals: 4 }}
  - {{ id: pp, label: Homozygous dominant (p²), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: het, label: Heterozygous carriers (2pq), family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - q = sqrt(qq)
  - p = 1 - q
  - pp = p^2
  - het = 2 * p * q
faq:
  - q: What is Hardy–Weinberg equilibrium?
    a: A model where allele and genotype frequencies stay constant between generations, given random mating and no selection, mutation, migration or genetic drift.
  - q: How do I find carrier frequency?
    a: Take the square root of the affected (recessive) frequency to get q, then calculate 2pq.
  - q: Do p² + 2pq + q² always add to 1?
    a: Yes — they cover every genotype in the population.
related: [statistics/probability, biology/exponential-population-growth]
''',f'''
## How to use this calculator

Enter the share of the population showing the **recessive phenotype** (q²). Allele frequencies and all genotype frequencies are calculated.

## Equations

<p class="formula">p + q = 1   p² + 2pq + q² = 1</p>

## Example

If 4% of a population shows a recessive trait:

- q = √0.04 = **0.2**, p = **0.8**
- Homozygous dominant = **64%**
- Carriers (2pq) = **32%**
''')

page(C,'exponential-population-growth',f'''
title: Exponential Population Growth Calculator
description: Calculate future population with continuous exponential growth from an initial size, growth rate and time.
category: biology
keywords: [exponential growth, population growth calculator, n = n0 e^rt, growth rate, population projection]
{U}
variables:
  - {{ id: N0, label: Initial population, default: 500, min: 0 }}
  - {{ id: r, label: Growth rate per year, family: percent, unit: '%', default: 5 }}
  - {{ id: t, label: Time, family: time, unit: yr, default: 10, min: 0 }}
  - {{ id: N, label: Final population, min: 0, decimals: 0 }}
  - {{ id: td, label: Doubling time, family: time, unit: yr, min: 0 }}
equations:
  - N = N0 * exp(r * t)
  - td = ln(2) / r
chart: {{ x: t, y: N, from: 0, to: 50 }}
faq:
  - q: What is exponential growth?
    a: Growth where the increase is proportional to the current size, so the population doubles at regular intervals.
  - q: Is it realistic?
    a: Only while resources are plentiful. Real populations slow down as they approach the carrying capacity — see the logistic growth calculator.
  - q: What is the rule of 70?
    a: Doubling time ≈ 70 ÷ growth rate (%). At 5% per year, a population doubles in about 14 years.
related: [biology/logistic-growth, biology/bacterial-growth, finance/doubling-time]
''',f'''
## How to use this calculator

Enter the **initial population**, **growth rate** and **time**. The final population and doubling time are calculated.

## Formula

<p class="formula">N = N₀ × e<sup>rt</sup></p>

## Example

500 animals growing at 5% per year for 10 years:

- N = 500 × e<sup>0.5</sup> = **{500*math.exp(0.5):.0f}**
- Doubling time = ln 2 ÷ 0.05 = **{math.log(2)/0.05:.1f} years**
''')

K,N0,r,t=1000,50,0.4,10
page(C,'logistic-growth',f'''
title: Logistic Growth Calculator (Carrying Capacity)
description: Model population growth that slows as it approaches the environment's carrying capacity (K).
category: biology
keywords: [logistic growth, carrying capacity, population model, s curve, ecology growth, verhulst]
{U}
variables:
  - {{ id: N0, label: Initial population, default: 50, min: 0 }}
  - {{ id: K, label: Carrying capacity (K), default: 1000, min: 0.0001 }}
  - {{ id: r, label: Intrinsic growth rate (per time unit), default: 0.4 }}
  - {{ id: t, label: Time (same units as r), default: 10, min: 0 }}
  - {{ id: N, label: Population at time t, min: 0, decimals: 1 }}
equations:
  - N = K / (1 + (K - N0) / N0 * exp(-r * t))
chart: {{ x: t, y: N, from: 0, to: 30 }}
faq:
  - q: What is carrying capacity?
    a: The maximum population an environment can support indefinitely with its available resources.
  - q: When is growth fastest?
    a: At half the carrying capacity (N = K/2), where the S-shaped curve is steepest.
  - q: Where is the logistic model used?
    a: Ecology, fisheries management, the spread of innovations and epidemics in their early stages.
related: [biology/exponential-population-growth, ecology/mark-recapture]
''',f'''
## How to use this calculator

Enter the **initial population**, **carrying capacity**, **growth rate** and **time**. The population at that time is calculated; the chart shows the S-shaped curve.

## Formula

<p class="formula">N(t) = K ÷ (1 + ((K − N₀) ÷ N₀) e<sup>−rt</sup>)</p>

## Example

N₀ = 50, K = 1,000, r = 0.4 per year, after 10 years:

N = 1,000 ÷ (1 + 19 × e⁻⁴) = **{K/(1+(K-N0)/N0*math.exp(-r*t)):.0f}**
''')

page(C,'magnification',f'''
title: Magnification Calculator (Microscopy)
description: Calculate magnification, image size or actual specimen size using image size ÷ actual size.
category: biology
keywords: [magnification calculator, image size, actual size, microscope magnification, specimen size, i am formula]
{U}
variables:
  - {{ id: I, label: Image size (measured), family: length, unit: mm, default: 40, min: 0 }}
  - {{ id: A, label: Actual size, family: length, unit: um, default: 100, min: 0 }}
  - {{ id: M, label: Magnification (×), min: 0 }}
equations:
  - M = I / A
faq:
  - q: What is the magnification formula?
    a: Magnification = image size ÷ actual size. Both sizes must be in the same unit — the calculator converts mm, µm and nm for you.
  - q: How do I find actual size?
    a: Divide the image size by the magnification. Press × on Actual size and type the magnification.
  - q: How do I calculate total microscope magnification?
    a: Multiply eyepiece and objective magnifications — a 10× eyepiece with a 40× objective gives 400×.
related: [biology/field-of-view, conversion/mm-to-inches]
''',f'''
## How to use this calculator

Enter any **two** of image size, actual size and magnification. Choose units for each size (mm, µm, nm and more).

## Formula

<p class="formula">Magnification = image size ÷ actual size</p>

## Example

A cell 100 µm across appears 40 mm wide in a photo:

M = 40,000 µm ÷ 100 µm = **400×**

## Remember the units

1 mm = 1,000 µm · 1 µm = 1,000 nm
''')

page(C,'field-of-view',f'''
title: Microscope Field of View Calculator
description: Calculate the diameter of a microscope's field of view from the eyepiece field number and objective magnification.
category: biology
keywords: [field of view, microscope fov, field number, field diameter, objective magnification]
{U}
variables:
  - {{ id: fn, label: Eyepiece field number, suffix: mm, default: 20, min: 0 }}
  - {{ id: obj, label: Objective magnification, default: 40, min: 0.01 }}
  - {{ id: ep, label: Eyepiece magnification, default: 10, min: 0.01 }}
  - {{ id: fov, label: Field of view diameter, family: length, unit: um, min: 0 }}
  - {{ id: tot, label: Total magnification, min: 0 }}
equations:
  - fov = fn / obj / 1000
  - tot = obj * ep
faq:
  - q: What is the field number?
    a: The diameter of the eyepiece's field stop in mm, usually printed on the eyepiece (for example "10×/20").
  - q: Why does field of view shrink with higher magnification?
    a: The objective magnifies a smaller region, so FOV = field number ÷ objective magnification.
  - q: How do I estimate cell size from FOV?
    a: If 5 cells fit across a 500 µm field, each is about 100 µm long.
related: [biology/magnification, biology/hemocytometer]
''',f'''
## How to use this calculator

Enter the eyepiece's **field number** and the **objective magnification**. The field of view diameter is calculated, plus the total magnification.

## Formula

<p class="formula">FOV = field number ÷ objective magnification</p>

## Example

Field number 20 mm with a 40× objective: FOV = 20 ÷ 40 = 0.5 mm = **500 µm**.

## Typical fields of view (FN 20)

| Objective | FOV |
|---|---|
| 4× | 5 mm |
| 10× | 2 mm |
| 40× | 0.5 mm |
| 100× | 0.2 mm |
''')

page(C,'protein-molecular-weight',f'''
title: Protein Molecular Weight Estimator
description: Estimate a protein's molecular weight in kDa from its number of amino acids.
category: biology
keywords: [protein molecular weight, kda calculator, amino acids to kda, protein size, average amino acid mass]
{U}
variables:
  - {{ id: aa, label: Number of amino acids, default: 350, min: 0 }}
  - {{ id: avg, label: Average residue mass, suffix: Da, default: 110, min: 0 }}
  - {{ id: kda, label: Estimated molecular weight, suffix: kDa, min: 0, decimals: 1 }}
equations:
  - kda = aa * avg / 1000
faq:
  - q: Why use 110 Da per amino acid?
    a: It is the average mass of an amino acid residue in proteins, a widely used estimate.
  - q: How accurate is this?
    a: Usually within about 10%. Exact values need the actual sequence; glycosylation and other modifications add more mass.
  - q: How many amino acids is a 50 kDa protein?
    a: About 455 amino acids.
related: [biology/protein-concentration-a280, biology/dna-copy-number]
''',f'''
## How to use this calculator

Enter the **number of amino acids**. The estimated molecular weight is shown in kDa. Or enter the kDa (for example from a gel) to estimate the length.

## Formula

<p class="formula">MW (kDa) ≈ amino acids × 110 ÷ 1000</p>

## Example

A 350-residue protein: 350 × 110 = 38,500 Da = **38.5 kDa**.

## Gene length

Each amino acid is coded by 3 nucleotides, so a 350-residue protein needs a coding sequence of 1,053 bp (including the stop codon).
''')

ng,bp=10,5000
page(C,'dna-copy-number',f'''
title: DNA Copy Number Calculator
description: Calculate the number of DNA molecules (copies) from mass in ng and length in base pairs — for qPCR standards and cloning.
category: biology
keywords: [dna copy number, copies per ul, qpcr standard, plasmid copy number, ng to copies, molecules of dna]
{U}
variables:
  - {{ id: m, label: DNA amount, suffix: ng, default: 10, min: 0 }}
  - {{ id: bp, label: Length, suffix: bp, default: 5000, min: 1 }}
  - {{ id: cp, label: Number of copies, min: 0 }}
  - {{ id: pmol, label: Amount, suffix: pmol, min: 0, decimals: 5 }}
equations:
  - cp = m * 6.02214076e23 / (bp * 650 * 1e9)
  - pmol = m * 1000 / (bp * 650)
faq:
  - q: How do I convert ng of DNA to copies?
    a: Copies = ng × 6.022 × 10²³ ÷ (length in bp × 650 × 10⁹). 650 g/mol is the average mass of one base pair.
  - q: Does it work for single-stranded DNA?
    a: Use about 330 g/mol per nucleotide instead of 650 per base pair.
  - q: How do I make a qPCR standard curve?
    a: Calculate copies per µL of your stock, then make 10-fold serial dilutions.
related: [biology/dna-concentration, biology/ligation-ratio, biology/pcr-amplification]
''',f'''
## How to use this calculator

Enter the **amount of DNA** in ng and its **length** in base pairs. The number of copies and pmol are calculated.

## Formula

<p class="formula">copies = ng × N<sub>A</sub> ÷ (bp × 650 × 10⁹)</p>

## Example

10 ng of a 5,000 bp plasmid:

copies = 10 × 6.022 × 10²³ ÷ (5,000 × 650 × 10⁹) = **{ng*6.02214076e23/(bp*650*1e9):.3g}**
''')

page(C,'ligation-ratio',f'''
title: Ligation Calculator (Insert : Vector Ratio)
description: Calculate how many ng of insert to use for a ligation at a chosen molar ratio of insert to vector.
category: biology
keywords: [ligation calculator, insert vector ratio, molar ratio, cloning, 3:1 ratio, ng insert]
{U}
variables:
  - {{ id: vng, label: Vector amount, suffix: ng, default: 50, min: 0 }}
  - {{ id: vbp, label: Vector length, suffix: bp, default: 3000, min: 1 }}
  - {{ id: ibp, label: Insert length, suffix: bp, default: 1000, min: 1 }}
  - {{ id: r, label: Insert to vector molar ratio, default: 3, min: 0 }}
  - {{ id: ing, label: Insert needed, suffix: ng, min: 0, decimals: 2 }}
equations:
  - ing = vng * ibp / vbp * r
faq:
  - q: What molar ratio should I use?
    a: 3:1 insert to vector is a common starting point. Use 5:1 to 10:1 for short inserts and 1:1 for long ones.
  - q: Why not just use equal masses?
    a: Ligation depends on the number of DNA ends (molecules), not mass. A smaller insert has more molecules per ng.
  - q: How much vector should I use?
    a: Typically 20–100 ng in a standard ligation reaction.
related: [biology/dna-copy-number, biology/dna-concentration]
''',f'''
## How to use this calculator

Enter the **vector amount** and **length**, the **insert length** and the desired **molar ratio**. The mass of insert to use is calculated.

## Formula

<p class="formula">ng insert = ng vector × (insert bp ÷ vector bp) × ratio</p>

## Example

50 ng of a 3,000 bp vector, 1,000 bp insert, 3:1 ratio:

ng insert = 50 × (1,000 ÷ 3,000) × 3 = **50 ng**
''')

page(C,'pcr-amplification',f'''
title: PCR Amplification Calculator
description: Estimate how many DNA copies a PCR produces from the starting copies, number of cycles and efficiency.
category: biology
keywords: [pcr calculator, pcr cycles, amplification efficiency, dna copies after pcr, exponential amplification, qpcr]
{U}
variables:
  - {{ id: N0, label: Starting copies, default: 1000, min: 0 }}
  - {{ id: n, label: Number of cycles, default: 30, min: 0 }}
  - {{ id: E, label: Efficiency, family: percent, unit: '%', default: 90, min: 0, max: 1 }}
  - {{ id: N, label: Copies after PCR (theoretical), min: 0 }}
  - {{ id: fold, label: Fold amplification, min: 0 }}
equations:
  - fold = (1 + E)^n
  - N = N0 * fold
faq:
  - q: How many copies does PCR make?
    a: In theory each cycle doubles the DNA (100% efficiency), so 30 cycles give about 10⁹-fold amplification.
  - q: What is PCR efficiency?
    a: The fraction of templates copied each cycle. Good qPCR assays run at about 90–105%.
  - q: Does amplification continue forever?
    a: No — after 25–35 cycles it plateaus as primers and nucleotides run out.
related: [biology/dna-copy-number, biology/primer-tm]
''',f'''
## How to use this calculator

Enter the **starting copies**, **number of cycles** and **efficiency**. The theoretical number of copies and fold amplification are calculated.

## Formula

<p class="formula">N = N₀ × (1 + E)<sup>n</sup></p>

## Example

1,000 copies, 30 cycles at 90% efficiency:

- Fold = 1.9³⁰ = **{1.9**30:.3g}**
- Copies = **{1000*1.9**30:.3g}**

At 100% efficiency the same reaction would reach {1000*2**30:.3g} copies — showing how much efficiency matters.
''')

page(C,'centrifuge-rcf',f'''
title: Centrifuge RPM ↔ RCF (g-force) Calculator
description: Convert centrifuge speed between RPM and relative centrifugal force (× g) using the rotor radius.
category: biology
keywords: [rpm to g, rcf calculator, centrifuge, g force, relative centrifugal force, rotor radius]
{U}
featured: true
variables:
  - {{ id: rpm, label: Speed, suffix: rpm, default: 12000, min: 0 }}
  - {{ id: r, label: Rotor radius, family: length, unit: cm, imperialUnit: in, default: 8.5, min: 0 }}
  - {{ id: rcf, label: Relative centrifugal force, suffix: × g, min: 0, decimals: 0 }}
equations:
  - rcf = 0.00001118 * r * 100 * rpm^2
faq:
  - q: Why use RCF instead of RPM?
    a: The force on samples depends on both speed and rotor radius. RCF (× g) is the same on any centrifuge, so protocols specify it.
  - q: Where do I find the rotor radius?
    a: In the rotor manual — use the maximum radius (rmax) measured from the centre to the bottom of the tube.
  - q: What speed gives 10,000 × g?
    a: Press × on Speed and enter 10,000 as RCF. With an 8.5 cm rotor that is about 10,260 rpm.
related: [physics/centripetal-force, biology/serial-dilution]
''',f'''
## How to use this calculator

Enter the **speed** in rpm and the **rotor radius**. The RCF is calculated. To convert a protocol's × g to rpm, press × on Speed and type the RCF.

## Formula

<p class="formula">RCF = 1.118 × 10⁻⁵ × r (cm) × rpm²</p>

## Example

12,000 rpm with an 8.5 cm rotor:

RCF = 1.118 × 10⁻⁵ × 8.5 × 12,000² = **{1.118e-5*8.5*12000**2:,.0f} × g**
''')

page(C,'protein-concentration-a280',f'''
title: Protein Concentration Calculator (A280)
description: Calculate protein concentration from A280 absorbance using the molar extinction coefficient and molecular weight.
category: biology
keywords: [protein concentration, a280, extinction coefficient, protein quantification, beer lambert protein, mg/ml]
{U}
variables:
  - {{ id: A, label: A280 reading, default: 0.8, min: 0 }}
  - {{ id: eps, label: Molar extinction coefficient, suffix: M⁻¹cm⁻¹, default: 43824, min: 0.0001 }}
  - {{ id: mw, label: Molecular weight, suffix: Da, default: 66463, min: 0 }}
  - {{ id: l, label: Path length, suffix: cm, default: 1, min: 0.0001 }}
  - {{ id: um, label: Concentration, suffix: µM, min: 0 }}
  - {{ id: mg, label: Concentration, suffix: mg/mL, min: 0, decimals: 3 }}
equations:
  - um = A / (eps * l) * 1000000
  - mg = um * mw / 1000000
faq:
  - q: How do I calculate protein concentration from A280?
    a: c (M) = A280 ÷ (ε × l). Multiply by the molecular weight to get g/L, which equals mg/mL.
  - q: Where do I get the extinction coefficient?
    a: From the amino-acid sequence (tryptophan, tyrosine and cystine content) using a tool such as ExPASy ProtParam.
  - q: What is the default protein?
    a: Bovine serum albumin (BSA), with ε ≈ 43,824 M⁻¹cm⁻¹ and MW ≈ 66,463 Da.
related: [biology/dna-concentration, chemistry/beer-lambert, biology/protein-molecular-weight]
''',f'''
## How to use this calculator

Enter the **A280** reading, the protein's **extinction coefficient** and **molecular weight**, and the **path length**. The concentration is given in µM and mg/mL.

## Formula

<p class="formula">c = A280 ÷ (ε × l)</p>

## Example — BSA

A280 = 0.8, ε = 43,824 M⁻¹cm⁻¹, 1 cm:

- c = 0.8 ÷ 43,824 = **{0.8/43824*1e6:.2f} µM**
- × 66,463 g/mol = **{0.8/43824*66463:.3f} mg/mL**
''')

page(C,'primer-tm',f'''
title: Primer Melting Temperature (Tm) Calculator
description: Estimate a DNA primer's melting temperature from its base composition using the Wallace rule, and a suggested annealing temperature.
category: biology
keywords: [primer tm, melting temperature, wallace rule, annealing temperature, pcr primer, oligo tm]
{U}
variables:
  - {{ id: a, label: Number of A, default: 5, min: 0 }}
  - {{ id: t, label: Number of T, default: 5, min: 0 }}
  - {{ id: g, label: Number of G, default: 5, min: 0 }}
  - {{ id: c, label: Number of C, default: 5, min: 0 }}
  - {{ id: tm, label: Melting temperature (Wallace rule), suffix: °C, decimals: 1 }}
  - {{ id: ta, label: Suggested annealing temperature, suffix: °C, decimals: 1 }}
  - {{ id: gc, label: GC content, family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - tm = 2 * (a + t) + 4 * (g + c)
  - ta = tm - 5
  - gc = (g + c) / (a + t + g + c)
faq:
  - q: What is the Wallace rule?
    a: Tm = 2 °C × (A + T) + 4 °C × (G + C). It is a quick estimate for short primers (about 14–20 bases).
  - q: What annealing temperature should I use?
    a: Start about 3–5 °C below the lower primer Tm, then optimise with a gradient PCR.
  - q: What is an ideal primer?
    a: Typically 18–25 bases, 40–60% GC, Tm of 55–65 °C, and primer pairs within about 5 °C of each other.
related: [biology/gc-content, biology/pcr-amplification]
''',f'''
## How to use this calculator

Count the **A, T, G and C** bases in your primer and enter them. The melting temperature, a suggested annealing temperature and GC content are calculated.

## Formula (Wallace rule)

<p class="formula">Tm = 2(A + T) + 4(G + C)</p>

## Example

A 20-mer with 5 of each base:

- Tm = 2 × 10 + 4 × 10 = **60 °C**
- Annealing ≈ **55 °C**
- GC = **50%**

For longer primers or exact work, nearest-neighbour methods that account for salt concentration are more accurate.
''')

page(C,'gc-content',f'''
title: GC Content Calculator
description: Calculate the GC content (percentage of guanine and cytosine) of a DNA or RNA sequence from base counts.
category: biology
keywords: [gc content, gc percentage, dna composition, guanine cytosine, sequence analysis]
{U}
variables:
  - {{ id: g, label: G count, default: 120, min: 0 }}
  - {{ id: c, label: C count, default: 110, min: 0 }}
  - {{ id: a, label: A count, default: 140, min: 0 }}
  - {{ id: t, label: T (or U) count, default: 130, min: 0 }}
  - {{ id: n, label: Total length, suffix: bases, min: 0, decimals: 0 }}
  - {{ id: gc, label: GC content, family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - n = g + c + a + t
  - gc = (g + c) / n
faq:
  - q: What is GC content?
    a: The percentage of bases in a sequence that are guanine (G) or cytosine (C).
  - q: Why does GC content matter?
    a: G–C pairs have three hydrogen bonds versus two for A–T, so GC-rich DNA is more stable and melts at a higher temperature.
  - q: What is a typical GC content?
    a: About 40–42% for the human genome; bacteria range from under 25% to over 70%.
related: [biology/primer-tm, biology/dna-copy-number]
''',f'''
## How to use this calculator

Enter the counts of **G, C, A and T** (use T for U in RNA). The total length and GC content are calculated.

## Formula

<p class="formula">GC% = (G + C) ÷ (A + T + G + C) × 100</p>

## Example

G = 120, C = 110, A = 140, T = 130 → total 500 bases → GC = **{230/500*100:.0f}%**
''')

page(C,'water-potential',f'''
title: Water Potential Calculator
description: Calculate solute potential and total water potential of plant cells or solutions (Ψ = Ψs + Ψp).
category: biology
keywords: [water potential, solute potential, pressure potential, osmosis plants, psi, plant cells]
{U}
variables:
  - {{ id: i, label: Ionisation constant (i), default: 1, min: 0, help: 1 for sucrose, about 2 for NaCl }}
  - {{ id: c, label: Molar concentration, suffix: mol/L, default: 0.3, min: 0 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, default: 22, min: 0 }}
  - {{ id: pp, label: Pressure potential (Ψp), suffix: MPa, default: 0 }}
  - {{ id: ps, label: Solute potential (Ψs), suffix: MPa }}
  - {{ id: psi, label: Water potential (Ψ), suffix: MPa }}
equations:
  - ps = -i * c * 0.0083145 * T
  - psi = ps + pp
faq:
  - q: What is water potential?
    a: A measure of water's tendency to move. Water moves from higher (less negative) to lower (more negative) water potential.
  - q: What is the formula for solute potential?
    a: Ψs = −iCRT, with R = 0.0083145 L·MPa/(mol·K) and T in kelvin.
  - q: What is the water potential of pure water?
    a: Zero at atmospheric pressure. Adding solutes makes it negative.
related: [chemistry/osmotic-pressure, biology/serial-dilution]
''',f'''
## How to use this calculator

Enter the **ionisation constant**, **concentration**, **temperature** and **pressure potential** (0 for an open beaker). Solute potential and total water potential are calculated in MPa.

## Formulas

<p class="formula">Ψs = −i C R T   Ψ = Ψs + Ψp</p>

## Example

0.3 M sucrose at 22 °C in an open beaker:

Ψs = −1 × 0.3 × 0.0083145 × 295.15 = **{-0.3*0.0083145*295.15:.3f} MPa** = Ψ
''')

page(C,'specific-growth-rate',f'''
title: Specific Growth Rate Calculator (µ)
description: Calculate the specific growth rate of a culture from two measurements, plus the doubling time.
category: biology
keywords: [specific growth rate, mu, growth rate constant, microbial growth, od600, biomass growth]
{U}
variables:
  - {{ id: X1, label: Biomass / OD at time 1, default: 0.1, min: 0 }}
  - {{ id: X2, label: Biomass / OD at time 2, default: 0.8, min: 0 }}
  - {{ id: dt, label: Time between measurements, family: time, unit: h, default: 6, min: 0 }}
  - {{ id: mu, label: Specific growth rate (µ), suffix: per hour, min: 0, decimals: 4 }}
  - {{ id: td, label: Doubling time, family: time, unit: h, min: 0 }}
equations:
  - mu = ln(X2 / X1) / (dt * 8766)
  - td = ln(2) / mu / 8766
faq:
  - q: What is specific growth rate?
    a: The rate of increase in biomass per unit of biomass, µ = ln(X₂/X₁) ÷ (t₂ − t₁), usually in h⁻¹.
  - q: How is it related to doubling time?
    a: Doubling time = ln 2 ÷ µ.
  - q: Can I use optical density?
    a: Yes, OD600 readings in the linear range of the spectrophotometer are proportional to biomass.
related: [biology/cell-doubling-time, biology/bacterial-growth]
''',f'''
## How to use this calculator

Enter two **biomass or OD** readings and the **time** between them. The specific growth rate (per hour) and doubling time are calculated.

## Formula

<p class="formula">µ = ln(X₂ ÷ X₁) ÷ Δt   T<sub>d</sub> = ln 2 ÷ µ</p>

## Example

OD600 rises from 0.1 to 0.8 in 6 hours:

- µ = ln 8 ÷ 6 = **{math.log(8)/6:.4f} h⁻¹**
- Doubling time = **{math.log(2)/(math.log(8)/6):.1f} h**
''')

page(C,'serial-dilution',f'''
title: Serial Dilution Calculator
description: Calculate the final concentration after a series of dilution steps, and the total dilution factor.
category: biology
keywords: [serial dilution, dilution series, 10 fold dilution, dilution factor, colony counting, cfu]
{U}
variables:
  - {{ id: C0, label: Starting concentration, default: 100000000, min: 0 }}
  - {{ id: f, label: Dilution factor per step (e.g. 10 for 1:10), default: 10, min: 1 }}
  - {{ id: n, label: Number of steps, default: 6, min: 0 }}
  - {{ id: DF, label: Total dilution factor, min: 1 }}
  - {{ id: C, label: Final concentration, min: 0 }}
equations:
  - DF = f^n
  - C = C0 / DF
faq:
  - q: What is a serial dilution?
    a: A series of step-by-step dilutions, each by the same factor, to reach very low concentrations accurately.
  - q: How do I make a 1:10 dilution?
    a: Mix 1 part sample with 9 parts diluent — for example 100 µL into 900 µL.
  - q: How do I count CFU from a plate?
    a: CFU/mL = colonies ÷ (volume plated in mL × total dilution).
related: [chemistry/dilution, biology/hemocytometer]
''',f'''
## How to use this calculator

Enter the **starting concentration**, the **dilution factor per step** and the **number of steps**. The total dilution and final concentration are calculated (any concentration unit works).

## Formulas

<p class="formula">Total dilution = f<sup>n</sup>   C = C₀ ÷ f<sup>n</sup></p>

## Example

10⁸ cells/mL diluted 1:10 six times:

- Total dilution = 10⁶
- Final concentration = **100 cells/mL**

Plating 100 µL gives about 10 colonies — easy to count.
''')

page(C,'hemocytometer',f'''
title: Hemocytometer Cell Count Calculator
description: Calculate cells per mL from hemocytometer counts, squares counted and dilution — plus total cells.
category: biology
keywords: [hemocytometer, cell count, cells per ml, neubauer chamber, trypan blue, cell counting]
{U}
variables:
  - {{ id: cnt, label: Total cells counted, default: 180, min: 0 }}
  - {{ id: sq, label: Large squares counted, default: 4, min: 1 }}
  - {{ id: dil, label: Dilution factor (e.g. 2 for 1:1 trypan blue), default: 2, min: 1 }}
  - {{ id: vol, label: Total sample volume, family: volume, unit: mL, default: 10, min: 0 }}
  - {{ id: cml, label: Cells per mL, min: 0 }}
  - {{ id: tot, label: Total cells in sample, min: 0 }}
equations:
  - cml = cnt / sq * dil * 10000
  - tot = cml * vol * 1000000
faq:
  - q: How do I calculate cells per mL with a hemocytometer?
    a: Cells/mL = average count per large square × dilution factor × 10⁴. Each large square holds 0.1 µL (10⁻⁴ mL).
  - q: How many squares should I count?
    a: Usually the four corner squares (and sometimes the centre), aiming for 100–300 cells in total for accuracy.
  - q: What dilution does trypan blue add?
    a: Mixing equal volumes of cells and trypan blue gives a dilution factor of 2.
related: [biology/serial-dilution, biology/cell-doubling-time]
''',f'''
## How to use this calculator

Enter the **total cells counted**, the **number of large squares**, the **dilution factor** and your **sample volume**. Cells per mL and total cells are calculated.

## Formula

<p class="formula">cells/mL = (cells counted ÷ squares) × dilution × 10⁴</p>

## Example

180 cells in 4 squares, 1:1 trypan blue, 10 mL sample:

- Cells/mL = 45 × 2 × 10⁴ = **9.0 × 10⁵**
- Total = **9.0 × 10⁶ cells**
''')
print('biology ok')
