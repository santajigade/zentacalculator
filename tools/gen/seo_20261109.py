"""Enrich the 11 'Crawled, currently not indexed' calculator pages (Search Console, 2026-11-09) with unique reference tables and FAQs."""
import sys, os, math, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import expand as X
X.BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'content', 'calculators')
U = '2026-11-09'
def g(x, d=2):
    s = f'{x:,.{d}f}'
    return s.rstrip('0').rstrip('.') if '.' in s else s

# 1 Angle converter ---------------------------------------------------------
rows = ''.join(f'| {a}° | {g(math.radians(a),4)} rad | {g(a*400/360,2)} gon | {g(a*6400/360,1)} NATO mil | {g(a/360,4)} turn |\n' for a in [0,1,5,10,15,30,45,60,90,120,135,150,180,210,225,270,300,315,360])
def dms(x):
    d = int(x); m = (x - d) * 60; s = (m - int(m)) * 60
    return f"{d}° {int(m)}′ {s:.1f}″"
drows = ''.join(f'| {x}° | {dms(x)} |\n' for x in [12.5, 18.75, 33.333, 45.5, 51.4778, 73.9857, 90.125])
X.expand('math/angle-converter', f'''
## Degrees to radians, gradians, mils and turns

| Degrees | Radians | Gradians | Mils | Turns |
|---|---|---|---|---|
{rows}
## Decimal degrees to degrees, minutes and seconds

| Decimal degrees | DMS |
|---|---|
{drows}
To convert, keep the whole degrees, multiply the decimal part by 60 for minutes, then multiply the remaining decimal by 60 for seconds.
''', faq=[('How many degrees is 1 radian?', '1 radian is 57.2958°, because 180° equals π radians.'),
          ('How do I convert 45.5° to degrees, minutes and seconds?', '45.5° is 45° 30′ 0″. The decimal 0.5 × 60 gives 30 minutes.'),
          ('How many mils are in a circle?', 'NATO uses 6,400 mils in a full circle, so 1° is about 17.78 mils. Some other armies use 6,000 or 6,300.')], before='', updated=U)

# 2 Dilution ------------------------------------------------------------------
rows = ''.join(f'| 1:{f} | {g(100/f,2)} mL | {g(100-100/f,2)} mL | {g(1000/f,1)} mL | {g(1000-1000/f,1)} mL |\n' for f in [2,4,5,10,20,25,50,100,200,500,1000])
pct = ''.join(f'| {c1}% | {c2}% | {g(c2*100/c1,1)} mL | {g(100-c2*100/c1,1)} mL |\n' for c1, c2 in [(95,70),(99.9,70),(100,10),(37,10),(30,3),(50,25),(10,1)])
X.expand('chemistry/dilution', f'''
## Dilution chart: stock and diluent volumes

| Dilution | Stock for 100 mL | Diluent for 100 mL | Stock for 1 L | Diluent for 1 L |
|---|---|---|---|---|
{rows}
A 1:10 dilution means 1 part stock in 10 parts **total**, so 10 mL stock plus 90 mL diluent.

## Percent dilutions for 100 mL

| Stock | Target | Stock volume | Water |
|---|---|---|---|
{pct}
''', faq=[('How do I make 70% ethanol from 95% ethanol?', 'Use C₁V₁ = C₂V₂: 70 × 100 ÷ 95 = 73.7 mL of 95% ethanol, made up to 100 mL with water.'),
          ('What does a 1:10 dilution mean?', 'One part of stock in a total of ten parts, for example 1 mL stock plus 9 mL diluent.'),
          ('Is a 1:10 dilution the same as 1+10?', 'No. 1+10 means 1 part stock plus 10 parts diluent, which is a 1:11 dilution.')], before='', updated=U)

# 3 DNA concentration ---------------------------------------------------------
rows = ''.join(f'| {a:.2f} | {g(a*50,1)} | {g(a*33,1)} | {g(a*40,1)} |\n' for a in [0.05,0.1,0.2,0.25,0.5,0.75,1.0,1.25,1.5,2.0])
X.expand('biology/dna-concentration', f'''
## A260 to concentration table (undiluted, 1 cm path)

| A260 | dsDNA (ng/µL) | ssDNA (ng/µL) | RNA (ng/µL) |
|---|---|---|---|
{rows}
If you diluted the sample before reading, multiply by the dilution factor. A 1:10 dilution reading A260 = 0.5 means dsDNA at 25 × 10 = **250 ng/µL**.

## How much DNA do you have?

Total yield = concentration × volume. 120 ng/µL in 50 µL is **6 µg** of DNA.
''', faq=[('What concentration is an A260 of 1.0?', 'About 50 ng/µL for dsDNA, 33 ng/µL for ssDNA and 40 ng/µL for RNA.'),
          ('What is a good 260/230 ratio?', 'Between 2.0 and 2.2 for pure nucleic acid. Lower values suggest salt, phenol or carbohydrate carry-over.'),
          ('Why does my NanoDrop concentration differ from Qubit?', 'Absorbance measures all nucleic acid and some contaminants, while dye-based Qubit assays measure only the target type, so Qubit is often lower.')], before='', updated=U)

# 4 Due date ------------------------------------------------------------------
rows = ''.join(f'| {dt.date(2026,m,1).strftime("%d %b %Y")} | {(dt.date(2026,m,1)+dt.timedelta(280)).strftime("%d %b %Y")} | {(dt.date(2026,m,1)+dt.timedelta(13*7)).strftime("%d %b %Y")} | {(dt.date(2026,m,1)+dt.timedelta(27*7)).strftime("%d %b %Y")} |\n' for m in range(1, 13))
X.expand('other/due-date', f'''
## Due date chart (2026)

| First day of last period | Estimated due date | End of 1st trimester | End of 2nd trimester |
|---|---|---|---|
{rows}
The due date is 280 days (40 weeks) after the first day of your last period. Only about 4% of babies arrive on the exact day; most are born within two weeks either side.
''', faq=[('If my last period was on 1 January, when is my due date?', 'About 8 October, which is 280 days later.'),
          ('How many weeks is a full-term pregnancy?', 'A full-term pregnancy is 39 to 40 weeks. Babies born from 37 weeks are considered term.'),
          ('Can the due date change after an ultrasound?', 'Yes. An early dating scan is more accurate than the period date, so your doctor may adjust the due date after it.')], before='', updated=U)

# 5 4-20 mA -------------------------------------------------------------------
pv = lambda i, lo, hi: lo + (i - 4) / 16 * (hi - lo)
rows = ''.join(f'| {i} mA | {g((i-4)/16*100,2)}% | {g(pv(i,0,10),3)} bar | {g(pv(i,0,100),2)} °C | {g(pv(i,-50,150),1)} °C | {g(pv(i,0,250),2)} m³/h |\n' for i in range(4, 21))
X.expand('engineering/4-20ma-scaling', f'''
## 4 to 20 mA conversion chart for common ranges

| Current | % of span | 0 to 10 bar | 0 to 100 °C | −50 to 150 °C | 0 to 250 m³/h |
|---|---|---|---|---|---|
{rows}
Each 1 mA is 6.25% of span. For any other range, multiply the % of span by the span and add the lower range value.
''', faq=[('What is 12 mA in a 4 to 20 mA loop?', '12 mA is exactly 50% of span. On a 0 to 10 bar transmitter that is 5 bar.'),
          ('What does each mA represent in 4 to 20 mA?', 'Each 1 mA is 6.25% of the measuring span, because the 16 mA span covers 100%.'),
          ('How do I convert 4 to 20 mA to 1 to 5 V?', 'Pass the loop current through a 250 Ω resistor. 4 mA gives 1 V and 20 mA gives 5 V.')], before='', updated=U)

# 6 Sample size ---------------------------------------------------------------
def ss(N, e, z=1.96):
    n0 = z * z * 0.25 / (e * e)
    return math.ceil(n0 / (1 + (n0 - 1) / N)) if N else math.ceil(n0)
pops = [100, 200, 500, 1000, 2000, 5000, 10000, 50000, 100000, 1000000, 0]
rows = ''.join(f'| {"Unlimited" if not N else f"{N:,}"} | {ss(N,0.10):,} | {ss(N,0.05):,} | {ss(N,0.03):,} | {ss(N,0.01):,} |\n' for N in pops)
rows99 = ''.join(f'| {"Unlimited" if not N else f"{N:,}"} | {ss(N,0.05,2.5758):,} | {ss(N,0.03,2.5758):,} |\n' for N in [500, 1000, 5000, 10000, 100000, 0])
X.expand('statistics/sample-size', f'''
## Sample size table by population (95% confidence)

| Population | ±10% | ±5% | ±3% | ±1% |
|---|---|---|---|---|
{rows}
Based on p = 50% (the most conservative case) with the finite population correction.

## Sample size at 99% confidence

| Population | ±5% | ±3% |
|---|---|---|
{rows99}''', faq=[('What sample size do I need for a population of 1,000?', f'{ss(1000,0.05)} responses for a ±5% margin of error at 95% confidence.'),
          ('Why does sample size stop growing for large populations?', f'Above about 20,000 people the population barely matters. You need about {ss(0,0.05)} responses at ±5% whether the population is 100,000 or 10 million.'),
          ('Is 100 responses enough for a survey?', 'For a large population, 100 responses gives a margin of error of about ±10% at 95% confidence, which is fine for a rough estimate only.')], before='', updated=U)

# 7 Horizontal tank -----------------------------------------------------------
def frac(h):
    th = 2 * math.acos(1 - 2 * h)
    return (th - math.sin(th)) / (2 * math.pi)
rows = ''.join(f'| {p}% | {g(frac(p/100)*100,1)}% |\n' for p in range(5, 100, 5))
cap = ''.join(f'| {D} m | {L} m | {g(math.pi*D*D/4*L*1000,0)} L | {g(math.pi*D*D/4*L*264.172,0)} US gal |\n' for D, L in [(1,2),(1.2,3),(1.5,4),(2,5),(2,6),(2.5,6),(2.5,8),(3,8),(3,10),(3.5,12)])
X.expand('engineering/horizontal-tank-volume', f'''
## Tank level to volume chart (every 5%)

| Level (% of diameter) | Volume (% full) |
|---|---|
{rows}
Use it with any flat-ended horizontal cylinder: multiply the % full by the full tank volume.

## Full capacity of common horizontal tanks

| Diameter | Length | Capacity | US gallons |
|---|---|---|---|
{cap}''', faq=[('How full is a horizontal tank at 50% level?', 'Exactly 50% full. Above and below the middle, volume and level are not proportional.'),
          ('What volume is in a horizontal tank at 25% level?', 'About 19.6% of the full volume, because the rounded bottom holds less liquid.'),
          ('How much does a 2 m diameter, 6 m long tank hold?', f'About {g(math.pi*6*1000,0)} litres with flat ends. Dished ends add extra volume.')], before='', updated=U)

# 8 Standard deviation --------------------------------------------------------
X.expand('statistics/standard-deviation', '''
## How much data falls within 1, 2 and 3 standard deviations?

| Range | Share of data (normal distribution) | Outside the range |
|---|---|---|
| Mean ± 1 SD | 68.27% | 1 in 3 |
| Mean ± 2 SD | 95.45% | 1 in 22 |
| Mean ± 3 SD | 99.73% | 1 in 370 |
| Mean ± 4 SD | 99.994% | 1 in 15,787 |
| Mean ± 6 SD | 99.9999998% | 1 in 507 million |

## Standard deviation functions in software

| Tool | Sample SD | Population SD |
|---|---|---|
| Excel / Google Sheets | STDEV.S(range) | STDEV.P(range) |
| Python (statistics) | stdev(data) | pstdev(data) |
| NumPy | np.std(x, ddof=1) | np.std(x) |
| R | sd(x) | sqrt(mean((x − mean(x))²)) |
| Casio calculator | sx or σn−1 | σx or σn |
''', faq=[('What is the standard deviation of 2, 4, 4, 4, 5, 5, 7, 9?', 'The population standard deviation is 2 and the sample standard deviation is 2.14. The mean is 5.'),
          ('What is a good standard deviation?', 'It depends on the data. Compare it with the mean using the coefficient of variation: below about 10% is usually considered low spread.'),
          ('Can standard deviation be negative?', 'No. It is a square root of an average squared distance, so it is always zero or positive.')], before='', updated=U)

# 9 Cell doubling time --------------------------------------------------------
rows = ''.join(f'| {f}× | {g(math.log2(f),2)} | {g(24/math.log2(f),1)} h | {g(48/math.log2(f),1)} h | {g(72/math.log2(f),1)} h |\n' for f in [1.5,2,3,4,5,8,10,16,20,32])
X.expand('biology/cell-doubling-time', f'''
## Fold increase to doubling time chart

| Fold increase | Doublings | Over 24 h | Over 48 h | Over 72 h |
|---|---|---|---|---|
{rows}
Read across: cells that grew 4× in 48 hours went through 2 doublings, so the doubling time is **24 hours**.
''', faq=[('What is the doubling time if cells grow 10-fold in 72 hours?', f'About {g(72/math.log2(10),1)} hours. 10-fold is {g(math.log2(10),2)} doublings.'),
          ('How many cells will I have after 3 days?', 'Multiply the starting count by 2 to the power of (hours ÷ doubling time). With a 24 hour doubling time, 1 × 10⁵ cells become 8 × 10⁵.'),
          ('Is doubling time the same as generation time?', 'For cultures where every cell divides, yes. Generation time usually refers to bacteria, doubling time to mammalian cell lines.')], before='', updated=U)

# 10 Combinations -------------------------------------------------------------
tri = ''.join(f'| {n} | ' + ' | '.join(str(math.comb(n, r)) if r <= n else '' for r in range(0, 11)) + ' |\n' for n in range(0, 11))
lot = ''.join(f'| {name} | {n} | {r} | {math.comb(n,r):,} |\n' for name, n, r in [('Pick 3 from 10', 10, 3), ('5 from 35', 35, 5), ('5 from 50', 50, 5), ('6 from 45', 45, 6), ('6 from 49', 49, 6), ('5 from 69 (main numbers)', 69, 5), ('5 from 70 (main numbers)', 70, 5), ('Keno 10 from 80', 80, 10)])
X.expand('statistics/combinations', f'''
## nCr table (n up to 10)

| n \\ r | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
{tri}
## Lottery combinations

| Game format | n | r | Combinations |
|---|---|---|---|
{lot}''', faq=[('What is 5 choose 2?', '10. There are 10 ways to choose 2 items from 5.'),
          ('How many combinations of 2 cards from a 52-card deck?', '1,326.'),
          ('How many combinations does a 4-digit code have?', '10,000 (0000 to 9999). Order matters and digits repeat, so it is 10⁴, not a combination.')], before='', updated=U)
print('done')
