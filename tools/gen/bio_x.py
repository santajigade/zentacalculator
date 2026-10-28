import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
pi = math.pi

expand('biology/bacterial-growth', '''
## Typical generation times

| Organism | Conditions | Generation time |
|---|---|---|
| *Escherichia coli* | Rich medium, 37 °C | about 20 min |
| *Bacillus subtilis* | Rich medium, 37 °C | about 25–30 min |
| *Staphylococcus aureus* | Optimal | about 30 min |
| *Saccharomyces cerevisiae* (yeast) | 30 °C | about 90 min |
| *Mycobacterium tuberculosis* | Optimal | about 15–20 h |

## Growth from one cell (20-minute doubling)

| Time | Generations | Cells |
|---|---|---|
''' + ''.join(f"| {h} h | {h*3} | {2**(h*3):,} |\n" for h in [1, 2, 4, 6, 8, 10]) + '''
Unchecked growth would be astronomical, but nutrients run out and waste builds up long before.

## The four growth phases

| Phase | What happens |
|---|---|
| Lag | Cells adapt to the medium; little division |
| Exponential (log) | Steady doubling — this calculator applies here |
| Stationary | Growth equals death as nutrients run out |
| Death | Cells die faster than they divide |

## Food safety

The “danger zone” for food is roughly 5–60 °C, where many bacteria multiply quickly. Food left at room temperature for a few hours can reach risky levels, which is why guidelines say to refrigerate within 2 hours.

## Measuring growth

Labs track growth by optical density (OD600), colony counts (CFU/mL) or cell counters. Use the [specific growth rate calculator](/biology/specific-growth-rate/) to get µ and doubling time from OD readings.
''', [
 ('How many bacteria after 24 hours?', 'In theory, 72 doublings at 20 minutes — about 4.7 × 10²¹ cells from one. In reality, growth stops at the stationary phase, often around 10⁹ cells per mL.'),
 ('What is generation time?', 'The time it takes for a bacterial population to double during exponential growth.'),
])

expand('biology/cell-doubling-time', '''
## Typical doubling times of cell lines

| Cell line | Approximate doubling time |
|---|---|
| HEK293 | 24–36 h |
| HeLa | about 24 h |
| CHO | 14–24 h |
| Jurkat | 25–50 h |
| Primary human fibroblasts | 24–72 h, slows with passages |
| Mouse embryonic stem cells | 12–16 h |

Doubling time depends on medium, serum, confluence and passage number.

## Fold change and doublings

| Fold increase | Doublings |
|---|---|
''' + ''.join(f"| {f}× | {math.log2(f):.2f} |\n" for f in [2, 4, 8, 10, 16, 100, 1000]) + '''
## Population doubling level (PDL)

For primary cells, track the cumulative population doublings across passages. Normal human fibroblasts typically stop dividing after about 40–60 doublings (the Hayflick limit).

## Planning experiments

To have 5 million cells from 500,000 with a 24-hour doubling time: log₂(10) = 3.32 doublings, so about **80 hours**. Add time for the lag phase after seeding.

## Tips for accurate counts

- Count in the exponential phase, not when cells are confluent.
- Use the same counting method each time — see the [hemocytometer calculator](/biology/hemocytometer/).
- Exclude dead cells with trypan blue.
''', [
 ('How do I calculate doubling time?', 'Doubling time = time × ln 2 ÷ ln(final ÷ initial). From 100,000 to 800,000 in 72 hours is 3 doublings, so 24 hours.'),
 ('Why is my doubling time longer than expected?', 'Common causes are over-confluence, old medium, high passage number, contamination or a long lag phase after passaging.'),
])

expand('biology/centrifuge-rcf', '''
## RCF at common speeds

| rpm | Radius 6 cm | Radius 8 cm | Radius 10 cm | Radius 15 cm |
|---|---|---|---|---|
''' + ''.join(f"| {r:,} | " + ' | '.join(f"{1.118e-5*rad*r*r:,.0f}" for rad in [6, 8, 10, 15]) + " |\n" for r in [1000, 2000, 3000, 5000, 10000, 13000, 15000]) + '''
## rpm from RCF

<p class="formula">rpm = √(RCF ÷ (1.118 × 10⁻⁵ × r))</p>

To get 1,500 × g in a rotor with a 10 cm radius: rpm = √(1,500 ÷ 0.0001118) ≈ **3,663 rpm**. Press × on Speed in the calculator and type the RCF.

## Why protocols use × g

Different centrifuges have different rotor radii, so the same rpm gives different forces. Always report and follow **× g** rather than rpm so results are reproducible.

## Typical spins

| Task | Typical force |
|---|---|
| Pelleting mammalian cells | 200–400 × g, 5 min |
| Separating plasma from blood | 1,000–2,000 × g, 10–15 min |
| Pelleting bacteria | 3,000–5,000 × g |
| Microcentrifuge DNA spins | 12,000–16,000 × g |
| Ultracentrifugation | 100,000 × g and above |

## Which radius?

Use the radius to the bottom of the tube (r<sub>max</sub>) for the maximum force, or the average radius (r<sub>av</sub>) to compare rotors. The rotor manual lists both.
''', [
 ('How do I convert rpm to g?', 'RCF = 1.118 × 10⁻⁵ × radius (cm) × rpm². At 12,000 rpm and 8 cm, RCF ≈ 12,880 × g.'),
 ('What radius should I use?', 'Use r_max (centre of rotation to the tube bottom) from the rotor manual unless your protocol says otherwise.'),
])

expand('biology/dna-concentration', '''
## Conversion factors

| Nucleic acid | 1 A260 unit equals |
|---|---|
| Double-stranded DNA | 50 µg/mL |
| Single-stranded DNA | 33 µg/mL |
| RNA | 40 µg/mL |
| Oligonucleotides | about 20–33 µg/mL (sequence-dependent) |

## Purity ratios

| Ratio | Pure DNA | Pure RNA | Low values suggest |
|---|---|---|---|
| A260/A280 | about 1.8 | about 2.0 | Protein or phenol contamination |
| A260/A230 | 2.0–2.2 | 2.0–2.2 | Salts, guanidine, carbohydrates |

## From concentration to copies

Once you know the mass, convert to copy number with the [DNA copy number calculator](/biology/dna-copy-number/) — essential for qPCR standards and cloning.

## Other quantification methods

| Method | Advantage |
|---|---|
| UV absorbance (A260) | Fast, no reagents |
| Fluorescent dyes (e.g. dsDNA-specific) | More sensitive, ignores RNA and free nucleotides |
| Gel electrophoresis | Shows size and integrity |

Fluorometric assays are preferred for low concentrations and for next-generation sequencing library preparation.

## Micro-volume spectrophotometers

Instruments that measure 1–2 µL drops use short path lengths and automatically normalise to 1 cm. Enter the reading as shown and set the dilution factor to 1 if you did not dilute.
''', [
 ('What is a good A260/A280 ratio?', 'About 1.8 for DNA and 2.0 for RNA.'),
 ('Is ng/µL the same as µg/mL?', 'Yes, they are numerically identical.'),
], before='## Reliable readings')

expand('biology/dna-copy-number', '''
## Copies per ng for common templates

| Template | Size | Copies per ng |
|---|---|---|
''' + ''.join(f"| {n} | {bp:,} bp | {6.022e23/(bp*650*1e9):.3g} |\n" for n, bp in [('PCR product', 200), ('PCR product', 1000), ('Plasmid', 3000), ('Plasmid', 5000), ('Lambda phage genome', 48502), ('E. coli genome', 4.6e6), ('Human genome (haploid)', 3.1e9)]) + '''
## The formula

<p class="formula">Copies = mass (ng) × 6.022 × 10²³ ÷ (length (bp) × 650 × 10⁹)</p>

650 g/mol is the average mass of one base pair of double-stranded DNA (about 618 for the sodium salt without water; 650 is the common working value). For single-stranded DNA use about 330 g/mol per base.

## Making a qPCR standard curve

1. Quantify the plasmid or PCR product accurately.
2. Calculate copies per µL.
3. Dilute to a top standard, for example 10⁷ copies per µL.
4. Make 10-fold serial dilutions down to about 10 copies per µL — see the [serial dilution calculator](/biology/serial-dilution/).

## Human genome copies

One haploid human genome weighs about 3.3 pg. So 10 ng of human genomic DNA contains roughly 3,000 haploid genome copies — a useful check for single-copy gene assays.
''', [
 ('How many copies are in 1 ng of a 3 kb plasmid?', 'About 3.1 × 10⁸ copies.'),
 ('What molecular weight per base pair should I use?', '650 g/mol for double-stranded DNA is the common value; some calculators use 660.'),
])

expand('biology/exponential-population-growth', '''
## Growth rates and doubling times

| Yearly growth rate | Doubling time |
|---|---|
''' + ''.join(f"| {r}% | {math.log(2)/(r/100):.1f} years |\n" for r in [0.5, 1, 2, 3, 5, 10]) + '''
## Discrete vs continuous growth

- **Continuous** (this calculator): N = N₀ × e<sup>rt</sup>, for populations that reproduce throughout the year.
- **Discrete**: N = N₀ × (1 + r)<sup>t</sup>, for populations that breed once a year.

For small r they give similar answers. At 5% for 10 years, continuous gives 1.649× and discrete 1.629×.

## Finding r from data

If a population grew from N₀ to N in t years: r = ln(N ÷ N₀) ÷ t. From 500 to 800 in 10 years, r = ln 1.6 ÷ 10 = **4.7% per year**.

## Limits to growth

Exponential growth cannot continue forever. Food, space and disease eventually slow it, producing an S-shaped curve. See the [logistic growth calculator](/biology/logistic-growth/).

## Human population

The world population took until about 1804 to reach 1 billion, but only about 12 years to go from 7 to 8 billion (2011–2022). The growth rate has since fallen below 1% a year, so doubling now takes much longer than in the 1960s, when the rate peaked above 2%.
''', [
 ('What is the doubling time at 2% growth?', 'About 34.7 years (ln 2 ÷ 0.02).'),
 ('Can r be negative?', 'Yes. A negative r means the population is shrinking; the calculator then gives the half-life instead of a doubling time.'),
])

expand('biology/field-of-view', '''
## Estimating cell size

Estimate a cell's size by comparing it with the field of view:

<p class="formula">Cell size ≈ field of view ÷ number of cells that fit across</p>

If about 20 cells fit across a 500 µm field, each is about **25 µm**.

## Magnification and field of view

| Objective | Total magnification (10× eyepiece) | Field of view (FN 18) | Field of view (FN 22) |
|---|---|---|---|
''' + ''.join(f"| {o}× | {o*10}× | {18/o*1000:.0f} µm | {22/o*1000:.0f} µm |\n" for o in [4, 10, 20, 40, 60, 100]) + '''
Higher magnification shows more detail but a smaller area.

## Resolution limit

Magnification alone does not show more detail beyond a point. The resolution of a light microscope is about:

<p class="formula">d ≈ 0.61 × λ ÷ NA</p>

With green light (550 nm) and a 1.25 NA oil objective, d ≈ 0.27 µm. Details closer together than this blur into one.

## Calibrating with a stage micrometer

For accurate measurements, use an eyepiece graticule and calibrate it against a stage micrometer at each objective. Divisions per µm differ for each magnification.
''', [
 ('What is the field of view at 400×?', 'With a 40× objective and a field number of 20, about 500 µm (0.5 mm).'),
 ('Why does the field of view get smaller at higher magnification?', 'Because the objective enlarges a smaller area of the specimen to fill the same eyepiece view.'),
], before='## Typical fields of view (FN 20)')

expand('biology/gc-content', '''
## GC content across organisms

| Organism | GC content (approx.) |
|---|---|
| *Plasmodium falciparum* (malaria parasite) | about 19% |
| *Saccharomyces cerevisiae* (yeast) | about 38% |
| Human | about 41% |
| *Escherichia coli* | about 51% |
| *Streptomyces coelicolor* | about 72% |

## Why GC content matters

- **Stability**: G–C pairs form three hydrogen bonds and stack more strongly than A–T pairs, raising the melting temperature.
- **PCR primers**: aim for 40–60% GC, with a G or C at the 3′ end (a “GC clamp”). See the [primer Tm calculator](/biology/primer-tm/).
- **Sequencing**: very high or low GC regions are harder to sequence and amplify evenly.
- **Gene density**: in mammals, GC-rich regions tend to be gene-rich.

## Melting temperature of long DNA

For DNA longer than about 50 bp, a common estimate is:

<p class="formula">Tm ≈ 64.9 + 41 × (G + C − 16.4) ÷ N</p>

For a 500 bp fragment with 46% GC: Tm ≈ 64.9 + 41 × (230 − 16.4) ÷ 500 = **82.4 °C**.

## Codon usage

Organisms with high GC content tend to use G or C in the third position of codons. This affects how well a gene from one organism expresses in another, which is why genes are often codon-optimised.
''', [
 ('What is a good GC content for primers?', '40–60%.'),
 ('Does high GC content make DNA more stable?', 'Yes. Higher GC content generally raises the melting temperature.'),
])

expand('biology/hardy-weinberg', '''
## Carrier frequency examples

| Condition frequency (q²) | q | Carriers (2pq) | About 1 in … carriers |
|---|---|---|---|
''' + ''.join(f"| 1 in {n:,} | {math.sqrt(1/n):.4f} | {2*(1-math.sqrt(1/n))*math.sqrt(1/n)*100:.2f}% | {1/(2*(1-math.sqrt(1/n))*math.sqrt(1/n)):.0f} |\n" for n in [100, 1000, 2500, 10000, 40000, 100000]) + '''
Even very rare recessive conditions have many more carriers than affected people.

## The five assumptions

Hardy–Weinberg equilibrium holds only when:

1. No mutation.
2. Random mating.
3. No natural selection.
4. A very large population (no genetic drift).
5. No migration (gene flow).

Real populations break some of these, so differences from the predicted frequencies can reveal evolution in action.

## Testing for equilibrium

Compare observed genotype counts with expected counts using a chi-square test with 1 degree of freedom. A chi-square value above 3.84 suggests the population is not in equilibrium at the 5% level.

## Sex-linked traits

For X-linked recessive traits, the frequency in males equals q directly (males have one X). In females it is q². Colour blindness affecting about 8% of men of northern European descent gives q ≈ 0.08 and about 0.64% of women affected.
''', [
 ('If 1 in 2,500 people has a recessive condition, how many are carriers?', 'q = 0.02, so 2pq ≈ 3.9% — about 1 in 26.'),
 ('What is p + q?', 'p + q = 1, because the two allele frequencies add up to all alleles at that gene.'),
])

expand('biology/hemocytometer', '''
## Hemocytometer grid

A standard Neubauer chamber has nine large squares, each 1 mm × 1 mm, with a depth of 0.1 mm. Each large square holds **0.1 µL** (10⁻⁴ mL), which is where the 10,000 factor comes from.

## Viability

With trypan blue, count live (clear) and dead (blue) cells separately:

<p class="formula">Viability = live cells ÷ (live + dead) × 100%</p>

Healthy cultures are usually above 90% viable. Many protocols require above 80–85% before experiments.

## How many cells to count

For good accuracy, count at least **100–200 cells** in total across the squares. If there are more than about 100 cells per large square, dilute further; if fewer than 10, concentrate or count more squares.

## Seeding density

To seed a plate, find the volume of cell suspension needed:

<p class="formula">Volume = target cells ÷ cells per mL</p>

To seed 300,000 cells from a suspension at 900,000 cells/mL, use **0.33 mL**.

## Counting rules

Count cells touching the top and left borders of each square, but not those touching the bottom and right. This avoids double-counting cells on shared lines.
''', [
 ('Why multiply by 10,000?', 'Each large square holds 0.0001 mL, so cells per square × 10,000 gives cells per mL.'),
 ('What dilution should I use with trypan blue?', 'A 1:1 mix (equal volumes of cells and 0.4% trypan blue) is common, giving a dilution factor of 2.'),
])

expand('biology/ligation-ratio', '''
## Insert amounts for common ratios

50 ng of 3,000 bp vector:

| Insert size | 1:1 | 3:1 | 5:1 |
|---|---|---|---|
''' + ''.join(f"| {i:,} bp | {50*i/3000:.1f} ng | {150*i/3000:.1f} ng | {250*i/3000:.1f} ng |\n" for i in [100, 250, 500, 1000, 2000, 5000]) + '''
## Choosing a ratio

| Situation | Typical insert : vector ratio |
|---|---|
| Standard sticky-end cloning | 3:1 |
| Blunt-end cloning | 3:1 to 5:1 |
| Very small inserts (under 200 bp) | 5:1 to 10:1 |
| Large inserts (similar to vector size) | 1:1 |

## Controls

- **Vector only** (no insert): shows background from uncut or self-ligated vector.
- **No ligase**: shows uncut vector.
- **Positive control**: a known insert that works.

## Improving ligation

- Dephosphorylate the vector to stop self-ligation.
- Gel-purify the vector and insert to remove small fragments.
- Use fresh ligase buffer — ATP degrades with freeze–thaw cycles.
- Keep total DNA around 50–200 ng in a 10–20 µL reaction.
''', [
 ('What insert-to-vector ratio should I use?', 'Start with 3:1 for most cloning, and try 1:1 and 5:1 if colonies are few.'),
 ('Why use molar ratios instead of mass?', 'Because ligation depends on the number of DNA ends, not their mass. A small insert has many more molecules per ng.'),
])

expand('biology/logistic-growth', '''
## Logistic vs exponential

| Feature | Exponential | Logistic |
|---|---|---|
| Shape | J-curve | S-curve |
| Limit | None | Carrying capacity K |
| Fastest growth | At the end | At N = K ÷ 2 |
| Best for | Early growth, plenty of resources | Populations reaching resource limits |

## Population over time (N₀ = 50, K = 1,000, r = 0.4)

| Time | Population |
|---|---|
''' + ''.join(f"| {t} | {1000/(1+(950/50)*math.exp(-0.4*t)):.0f} |\n" for t in [0, 2, 4, 6, 8, 10, 12, 15, 20]) + '''
## Maximum growth rate

The population grows fastest when it reaches half the carrying capacity, at a rate of r × K ÷ 4 individuals per time unit. Fisheries use this idea for “maximum sustainable yield”: harvest at the level that keeps the population near K/2.

## Time to reach a level

<p class="formula">t = ln[(K − N₀) × N ÷ (N₀ × (K − N))] ÷ r</p>

## Beyond biology

The logistic curve also models technology adoption, the spread of rumours and some epidemics in their early stages.
''', [
 ('What is carrying capacity?', 'The maximum population size an environment can support indefinitely with its available resources.'),
 ('When is logistic growth fastest?', 'When the population is at half the carrying capacity.'),
])

expand('biology/magnification', '''
## Unit conversions

| Unit | In metres | In millimetres |
|---|---|---|
| millimetre (mm) | 10⁻³ | 1 |
| micrometre (µm) | 10⁻⁶ | 0.001 |
| nanometre (nm) | 10⁻⁹ | 0.000001 |

Convert both sizes to the same unit before dividing. 1 mm = 1,000 µm; 1 µm = 1,000 nm.

## Sizes of biological structures

| Structure | Typical size |
|---|---|
| Human egg cell | about 100 µm |
| Plant cell | 10–100 µm |
| Animal cell | 10–30 µm |
| Red blood cell | about 7–8 µm |
| Bacterium (E. coli) | about 2 µm long |
| Mitochondrion | 0.5–1 µm |
| Virus (influenza) | about 100 nm |
| Ribosome | about 25 nm |

## Microscope types

| Microscope | Useful magnification | Resolution |
|---|---|---|
| Light microscope | up to about 1,500× | about 200 nm |
| Scanning electron (SEM) | up to about 500,000× | about 1–10 nm |
| Transmission electron (TEM) | up to about 1,000,000× or more | below 1 nm |

## Scale bars

Micrographs often include a scale bar instead of a magnification figure. Measure the bar in mm, then magnification = bar length on image ÷ the length it represents.
''', [
 ('How do I calculate actual size?', 'Actual size = image size ÷ magnification. Press × on Actual size and enter the image size and magnification.'),
 ('What is the magnification formula?', 'Magnification = image size ÷ actual size (in the same units).'),
], before='## Remember the units')

expand('biology/pcr-amplification', '''
## Fold amplification by efficiency

| Cycles | 100% efficiency | 90% | 80% |
|---|---|---|---|
''' + ''.join(f"| {n} | {2**n:.3g} | {1.9**n:.3g} | {1.8**n:.3g} |\n" for n in [10, 20, 25, 30, 35]) + '''
A small drop in efficiency makes a big difference after 30 cycles.

## Plateau phase

In practice, PCR slows and stops (plateau) as primers and nucleotides run out and the polymerase loses activity. Most reactions plateau somewhere around 10¹¹–10¹² copies, regardless of the theoretical number.

## qPCR efficiency from a standard curve

Run a 10-fold dilution series and plot Ct against log₁₀(copies). The slope gives efficiency:

<p class="formula">E = 10<sup>−1/slope</sup> − 1</p>

A slope of −3.32 means 100% efficiency. Acceptable assays are usually 90–110% (slope −3.6 to −3.1).

## Ct and starting amount

Each cycle difference in Ct means about a 2-fold difference in starting template (at 100% efficiency). A sample with a Ct 3.3 cycles lower has about 10 times more template.
''', [
 ('How many copies after 30 cycles?', 'In theory 2³⁰ ≈ 1.07 × 10⁹ times the starting amount at 100% efficiency, but reactions plateau earlier in practice.'),
 ('What is a good qPCR efficiency?', 'Between 90% and 110%, with a standard curve R² above 0.98.'),
])

expand('biology/primer-tm', '''
## Primer design guidelines

| Property | Recommended |
|---|---|
| Length | 18–25 nucleotides |
| GC content | 40–60% |
| Tm | 52–65 °C |
| Tm difference between primers | Within 2–5 °C |
| 3′ end | End in G or C (GC clamp), avoid more than 3 G/C in the last 5 bases |
| Repeats | Avoid runs of 4+ identical bases |

## Other Tm methods

| Method | Best for |
|---|---|
| Wallace rule (this calculator) | Primers under about 14–20 nt, quick estimates |
| Basic GC formula: 64.9 + 41(GC − 16.4)/N | Longer oligos |
| Nearest-neighbour thermodynamics | Most accurate; accounts for salt and primer concentration |

The Wallace rule tends to overestimate Tm for longer primers. Many polymerase suppliers provide nearest-neighbour Tm calculators tuned to their buffers.

## Annealing temperature

Start about 3–5 °C below the lower primer Tm. If you see non-specific bands, raise it; if there is no product, lower it or run a gradient PCR.

## Primer problems to avoid

- **Self-dimers and hairpins**: primers binding to themselves.
- **Primer-dimers**: forward and reverse primers binding each other at the 3′ ends.
- **Off-target binding**: check specificity against the genome with a sequence search tool.
''', [
 ('What is the Wallace rule?', 'Tm = 2 × (A + T) + 4 × (G + C) °C, a quick estimate for short primers.'),
 ('How far below Tm should I anneal?', 'Usually 3–5 °C below the lower of the two primer Tms.'),
])

expand('biology/protein-concentration-a280', '''
## Extinction coefficients of common proteins

| Protein | MW (Da) | ε₂₈₀ (M⁻¹cm⁻¹) | A280 of 1 mg/mL |
|---|---|---|---|
''' + ''.join(f"| {n} | {mw:,} | {e:,} | {e/mw:.2f} |\n" for n, mw, e in [('BSA', 66463, 43824), ('Lysozyme (hen egg)', 14313, 37970), ('IgG (typical)', 150000, 210000), ('GFP', 26900, 21890), ('Insulin', 5808, 5960)]) + '''
## Calculating ε from sequence

ε₂₈₀ can be estimated from the amino acid composition:

<p class="formula">ε = (number of Trp × 5,500) + (number of Tyr × 1,490) + (number of cystines × 125)</p>

Proteins without tryptophan or tyrosine absorb very little at 280 nm and need another method.

## Other protein assays

| Assay | Range | Notes |
|---|---|---|
| A280 | about 0.1–100 mg/mL | Fast, non-destructive; needs pure protein |
| Bradford | 1–1,500 µg/mL | Simple; sensitive to detergents |
| BCA | 20–2,000 µg/mL | Tolerates detergents; sensitive to reducing agents |

## Nucleic acid contamination

Nucleic acids absorb strongly at 260 nm and also at 280 nm. An A260/A280 ratio around 0.57 suggests pure protein; higher values indicate nucleic acid contamination.
''', [
 ('What is the A280 of 1 mg/mL BSA?', 'About 0.66.'),
 ('Why use A280 to measure protein?', 'Tryptophan and tyrosine absorb UV light at 280 nm, so absorbance is proportional to concentration.'),
])

expand('biology/protein-molecular-weight', '''
## Estimates for different lengths

| Amino acids | Approximate MW |
|---|---|
''' + ''.join(f"| {n:,} | {n*110/1000:.1f} kDa |\n" for n in [50, 100, 200, 300, 500, 1000, 2000]) + '''
## From DNA to protein size

Each amino acid is coded by 3 nucleotides. A 1,500 bp open reading frame (including the stop codon) encodes 499 amino acids — about **55 kDa**.

## Why 110 Da?

The average mass of an amino acid in proteins is about 128 Da, but each peptide bond releases one water molecule (18 Da), giving an average residue mass of about 110 Da. Proteins rich in heavy residues (Trp, Tyr, Arg) are heavier than estimated.

## Measured vs predicted size

On SDS-PAGE gels, proteins may run at a different apparent size than predicted because of:

- Post-translational modifications (glycosylation adds mass).
- Unusual charge or shape.
- Incomplete denaturation.

Mass spectrometry gives the most accurate molecular weight.

## Daltons and kilodaltons

1 kDa = 1,000 Da. A dalton is about the mass of one hydrogen atom (1 g/mol).
''', [
 ('How heavy is a 500 amino acid protein?', 'About 55 kDa.'),
 ('How many amino acids in a 30 kDa protein?', 'About 270 (30,000 ÷ 110).'),
])

expand('biology/serial-dilution', '''
## 10-fold dilution series

Starting at 10⁸ per mL:

| Tube | Total dilution | Concentration |
|---|---|---|
''' + ''.join(f"| {n} | 10<sup>{n}</sup> | {1e8/10**n:.0e} per mL |\n" for n in range(1, 9)) + '''
## Plate counts (CFU)

To count bacteria, plate dilutions and choose the plate with **30–300 colonies**:

<p class="formula">CFU/mL = colonies ÷ (volume plated in mL × dilution)</p>

If 150 colonies grow from 0.1 mL of the 10⁻⁶ dilution: 150 ÷ (0.1 × 10⁻⁶) = **1.5 × 10⁹ CFU/mL**.

## 2-fold dilutions

Two-fold series are used for antibiotic MIC tests and antibody titres. After n steps the dilution is 2ⁿ: 10 steps give 1:1,024.

## Making each step

For a 1:10 step with a final volume of 1 mL, transfer 100 µL into 900 µL of diluent. Mix well and use a fresh tip for each transfer to avoid carry-over errors.

## Error build-up

Small pipetting errors multiply across steps. Use calibrated pipettes and, for critical work, make the dilution in fewer, larger steps.
''', [
 ('What is a 1:10 serial dilution?', 'Each step dilutes the previous one tenfold, for example 100 µL into 900 µL.'),
 ('What is the total dilution after 6 tenfold steps?', '10⁶, or one million-fold.'),
])

expand('biology/specific-growth-rate', '''
## µ and doubling time

| µ (per hour) | Doubling time |
|---|---|
''' + ''.join(f"| {mu} | {math.log(2)/mu:.2f} h ({math.log(2)/mu*60:.0f} min) |\n" for mu in [0.1, 0.2, 0.35, 0.5, 0.693, 1.0, 2.0]) + '''
## Measuring µ correctly

- Use two points in the **exponential phase**, where ln(OD) rises in a straight line.
- Better still, take several readings and fit a straight line to ln(OD) against time. The slope is µ.
- Keep OD600 readings in the linear range of the spectrophotometer (often below 0.4–0.8); dilute dense cultures before reading.

## µ in bioprocesses

In a chemostat at steady state, the specific growth rate equals the dilution rate D (flow ÷ volume). Running D above the maximum µ washes the culture out.

## Monod equation

Growth rate depends on the limiting nutrient concentration S:

<p class="formula">µ = µ<sub>max</sub> × S ÷ (K<sub>s</sub> + S)</p>

K<sub>s</sub> is the nutrient level at which µ is half of µ<sub>max</sub>.
''', [
 ('What is the specific growth rate?', 'The rate of increase of biomass per unit of biomass, µ = ln(X₂ ÷ X₁) ÷ Δt, in units of 1/time.'),
 ('How is µ related to doubling time?', 'Doubling time = ln 2 ÷ µ ≈ 0.693 ÷ µ.'),
])

expand('biology/water-potential', '''
## Solute potential of sucrose solutions (22 °C)

| Molarity | Ψs |
|---|---|
''' + ''.join(f"| {c} M | {-c*0.0083145*295.15:.3f} MPa |\n" for c in [0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.0]) + '''
## Direction of water movement

Water always moves from **higher** (less negative) to **lower** (more negative) water potential:

| Cell Ψ vs solution Ψ | Result |
|---|---|
| Cell higher | Water leaves the cell (plasmolysis in plants) |
| Equal | No net movement |
| Cell lower | Water enters the cell (turgid in plants) |

## The potato core experiment

Place potato cores in sucrose solutions of different molarities and measure the change in mass. Plot percentage change against molarity; where the line crosses zero, the solution's water potential equals the potato's. Typical values are around 0.25–0.35 M sucrose.

## Typical water potentials

| Location | Ψ (approx.) |
|---|---|
| Pure water | 0 MPa |
| Moist soil | −0.01 to −0.3 MPa |
| Leaf cells | −0.5 to −1.5 MPa |
| Air at 50% humidity | about −95 MPa |

The steep drop from soil to air drives water up through plants.
''', [
 ('Why is water potential usually negative?', 'Pure water is defined as 0. Adding solutes lowers it, so solutions and cells have negative values.'),
 ('What is the pressure potential?', 'The pressure exerted on water by the cell wall in plant cells. It is positive in turgid cells.'),
])

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/biology/*.mdx')):
    c = 'biology/' + os.path.basename(p)[:-4]; print(c, words(c))
