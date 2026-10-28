import math, statistics as st
from page import page
C='statistics'; U='updated: 2026-10-27'
D=[4,8,6,5,3,7,9,5]
def Phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))

page(C,'standard-deviation',f'''
title: Standard Deviation Calculator
description: Paste your data to get sample and population standard deviation, variance, mean and count — with steps.
category: statistics
keywords: [standard deviation calculator, sample standard deviation, population standard deviation, variance, sd, stdev]
{U}
featured: true
dataset:
  label: Your data
  default: '4, 8, 6, 5, 3, 7, 9, 5'
variables:
  - {{ id: sd, label: Sample standard deviation (s) }}
  - {{ id: sdp, label: Population standard deviation (σ) }}
  - {{ id: v, label: Sample variance (s²) }}
  - {{ id: vp, label: Population variance (σ²) }}
  - {{ id: mean, label: Mean }}
  - {{ id: n, label: Count (n) }}
equations:
  - sd = data_sd
  - sdp = data_sdp
  - v = data_var
  - vp = data_varp
  - mean = data_mean
  - n = data_n
faq:
  - q: Should I use sample or population standard deviation?
    a: Use the sample formula (divide by n − 1) when your data is a sample from a larger group — the usual case. Use the population formula (divide by n) only when you have every member of the group.
  - q: What does standard deviation tell me?
    a: How spread out the values are around the mean. A small value means the data is tightly clustered.
  - q: How is variance related?
    a: Variance is the square of the standard deviation.
related: [statistics/mean-median-mode, statistics/z-score, statistics/standard-error]
''',f'''
## How to use this calculator

Paste or type your numbers, separated by commas, spaces or new lines — you can paste a column from Excel. All results update instantly.

## Formulas

<p class="formula">s = √( Σ(x − x̄)² ÷ (n − 1) )   σ = √( Σ(x − μ)² ÷ n )</p>

## Worked example

Data: 4, 8, 6, 5, 3, 7, 9, 5 (n = 8)

- Mean = 47 ÷ 8 = **{st.mean(D):.3f}**
- Sum of squared deviations = {sum((x-st.mean(D))**2 for x in D):.3f}
- Sample variance = {st.variance(D):.4f} → **s = {st.stdev(D):.4f}**
- Population variance = {st.pvariance(D):.4f} → **σ = {st.pstdev(D):.4f}**

## Interpreting standard deviation

For roughly bell-shaped data, about 68% of values fall within 1 SD of the mean and 95% within 2 SD. See the [empirical rule calculator](/statistics/empirical-rule/).

## In Excel

Sample: `=STDEV.S(range)` · Population: `=STDEV.P(range)`
''')

page(C,'mean-median-mode',f'''
title: Mean, Median & Mode Calculator
description: Find the mean, median, mode and range of any list of numbers — paste data from a spreadsheet.
category: statistics
keywords: [mean median mode, mode calculator, median calculator, central tendency, average, range]
{U}
featured: true
dataset:
  label: Your data
  default: '3, 7, 7, 2, 9, 7, 4, 5, 2'
variables:
  - {{ id: mean, label: Mean }}
  - {{ id: median, label: Median }}
  - {{ id: mode, label: Mode (most frequent value) }}
  - {{ id: mc, label: Mode appears (times) }}
  - {{ id: rng, label: Range }}
  - {{ id: n, label: Count }}
equations:
  - mean = data_mean
  - median = data_median
  - mode = data_mode
  - mc = data_modecount
  - rng = data_range
  - n = data_n
faq:
  - q: What is the difference between mean, median and mode?
    a: The mean is the arithmetic average, the median is the middle value when sorted, and the mode is the most frequent value.
  - q: What if no number repeats?
    a: Then there is no mode. The calculator shows the count as 1 to indicate every value appears once.
  - q: What if two values are equally common?
    a: The data is bimodal. The calculator shows the smaller of the most frequent values.
related: [math/average, statistics/standard-deviation, statistics/quartiles]
''',f'''
## How to use this calculator

Enter your numbers separated by commas, spaces or new lines. The mean, median, mode and range update as you type.

## Definitions

- **Mean** = sum ÷ count
- **Median** = middle value of the sorted list (average of the two middle values if the count is even)
- **Mode** = the value that appears most often
- **Range** = maximum − minimum

## Worked example

Data: 3, 7, 7, 2, 9, 7, 4, 5, 2 → sorted: 2, 2, 3, 4, **5**, 7, 7, 7, 9

- Mean = 46 ÷ 9 = **{46/9:.3f}**
- Median = **5**
- Mode = **7** (appears 3 times)
- Range = 9 − 2 = **7**

## When to use each

- **Mean** — symmetric data without extreme values.
- **Median** — skewed data such as incomes or house prices.
- **Mode** — categories or the most popular choice (sizes, ratings).
''')

Q=[1,3,5,6,7,8,9,12,15,21]
import numpy as np
q1,q2,q3=np.percentile(Q,[25,50,75])
page(C,'quartiles',f'''
title: Quartile & IQR Calculator (Five-Number Summary)
description: Calculate quartiles Q1, Q2, Q3, the interquartile range and outlier fences — the five-number summary for a box plot.
category: statistics
keywords: [quartile calculator, iqr, interquartile range, five number summary, box plot, outliers]
{U}
dataset:
  label: Your data
  default: '1, 3, 5, 6, 7, 8, 9, 12, 15, 21'
variables:
  - {{ id: mn, label: Minimum }}
  - {{ id: q1, label: Q1 (25th percentile) }}
  - {{ id: q2, label: Median (Q2) }}
  - {{ id: q3, label: Q3 (75th percentile) }}
  - {{ id: mx, label: Maximum }}
  - {{ id: iqr, label: Interquartile range (IQR) }}
  - {{ id: lf, label: Lower outlier fence (Q1 − 1.5 IQR) }}
  - {{ id: uf, label: Upper outlier fence (Q3 + 1.5 IQR) }}
equations:
  - mn = data_min
  - q1 = data_q1
  - q2 = data_median
  - q3 = data_q3
  - mx = data_max
  - iqr = q3 - q1
  - lf = q1 - 1.5 * iqr
  - uf = q3 + 1.5 * iqr
faq:
  - q: What is the interquartile range?
    a: Q3 − Q1, the spread of the middle 50% of the data. It is not affected by extreme values.
  - q: How are outliers identified?
    a: A common rule flags values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR.
  - q: Why do calculators give different quartiles?
    a: There are several methods. This one uses linear interpolation, the same as Excel's QUARTILE.INC and PERCENTILE.INC.
related: [statistics/mean-median-mode, statistics/standard-deviation]
''',f'''
## How to use this calculator

Paste your data. You get the five-number summary (min, Q1, median, Q3, max), the IQR and the outlier fences.

## Method

Quartiles are found by linear interpolation between sorted values — the method used by Excel's `QUARTILE.INC`.

## Worked example

Data: 1, 3, 5, 6, 7, 8, 9, 12, 15, 21

- Q1 = **{q1:g}**, median = **{q2:g}**, Q3 = **{q3:g}**
- IQR = **{q3-q1:g}**
- Fences: {q1-1.5*(q3-q1):g} and {q3+1.5*(q3-q1):g} → **21 is an outlier**

## Box plots

A box plot draws a box from Q1 to Q3 with a line at the median, and "whiskers" to the smallest and largest values inside the fences. Points beyond the fences are drawn individually as outliers.
''')

page(C,'z-score',f'''
title: Z-Score Calculator
description: Calculate the z-score of a value from the mean and standard deviation — plus its percentile under a normal distribution.
category: statistics
keywords: [z score calculator, standard score, z table, percentile, normal distribution, standardize]
{U}
featured: true
variables:
  - {{ id: x, label: Value (x), default: 85 }}
  - {{ id: mu, label: Mean (μ), default: 70 }}
  - {{ id: s, label: Standard deviation (σ), default: 10, min: 0.0000001 }}
  - {{ id: z, label: Z-score }}
  - {{ id: p, label: Percentile (area to the left), family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - z = (x - mu) / s
  - p = normcdf(z)
chart: {{ x: x, y: p, from: 40, to: 100 }}
faq:
  - q: What is a z-score?
    a: How many standard deviations a value is above or below the mean. z = 0 is exactly average; z = 2 is two SDs above.
  - q: How do I find a percentile from a z-score?
    a: Use the normal distribution — the calculator gives the share of values below x, assuming the data is normally distributed.
  - q: What z-score is unusual?
    a: Values beyond about ±2 occur roughly 5% of the time; beyond ±3, about 0.3% of the time.
related: [statistics/normal-distribution, statistics/standard-deviation, statistics/empirical-rule]
''',f'''
## How to use this calculator

Enter the **value**, the **mean** and the **standard deviation**. The z-score and percentile appear instantly. To find the value at a given percentile, press × on Value and type the percentile.

## Formula

<p class="formula">z = (x − μ) ÷ σ</p>

## Worked example

An exam score of 85 when the class mean is 70 and SD is 10:

- z = (85 − 70) ÷ 10 = **1.5**
- Percentile = **{Phi(1.5)*100:.1f}%** — better than about 93% of the class

## Common z-scores

| z | Percentile |
|---|---|
| −2 | {Phi(-2)*100:.1f}% |
| −1 | {Phi(-1)*100:.1f}% |
| 0 | 50% |
| 1 | {Phi(1)*100:.1f}% |
| 1.645 | 95% |
| 1.96 | 97.5% |
| 2 | {Phi(2)*100:.1f}% |
''')

page(C,'confidence-interval',f'''
title: Confidence Interval Calculator (Mean)
description: Calculate a confidence interval for a mean from the sample mean, standard deviation and sample size.
category: statistics
keywords: [confidence interval calculator, 95% confidence interval, margin of error, sample mean, z interval]
{U}
variables:
  - id: zc
    label: Confidence level
    default: 1.959964
    options:
      - {{ label: 90%, value: 1.644854 }}
      - {{ label: 95%, value: 1.959964 }}
      - {{ label: 98%, value: 2.326348 }}
      - {{ label: 99%, value: 2.575829 }}
  - {{ id: xb, label: Sample mean, default: 50 }}
  - {{ id: s, label: Standard deviation, default: 12, min: 0 }}
  - {{ id: n, label: Sample size (n), default: 100, min: 1 }}
  - {{ id: E, label: Margin of error, min: 0 }}
  - {{ id: lo, label: Lower bound }}
  - {{ id: hi, label: Upper bound }}
equations:
  - E = zc * s / sqrt(n)
  - lo = xb - E
  - hi = xb + E
faq:
  - q: What does a 95% confidence interval mean?
    a: If you repeated the sampling many times, about 95% of the intervals built this way would contain the true population mean.
  - q: How do I make the interval narrower?
    a: Increase the sample size (quadrupling n halves the width) or accept a lower confidence level.
  - q: Should I use z or t?
    a: This uses z, which is accurate for samples of about 30 or more. For small samples, a t-interval is wider.
related: [statistics/margin-of-error, statistics/sample-size, statistics/standard-error]
''',f'''
## How to use this calculator

Choose a **confidence level**, then enter the **sample mean**, **standard deviation** and **sample size**. The margin of error and interval bounds are calculated.

## Formula

<p class="formula">CI = x̄ ± z × s ÷ √n</p>

## Worked example

Mean 50, SD 12, n = 100, 95% confidence:

- Margin of error = 1.96 × 12 ÷ 10 = **{1.959964*12/10:.2f}**
- Interval = **{50-1.959964*1.2:.2f} to {50+1.959964*1.2:.2f}**

## z values

| Confidence | z |
|---|---|
| 90% | 1.645 |
| 95% | 1.960 |
| 98% | 2.326 |
| 99% | 2.576 |
''')

page(C,'sample-size',f'''
title: Sample Size Calculator (Surveys)
description: Find how many survey responses you need for a given margin of error and confidence level — with finite population correction.
category: statistics
keywords: [sample size calculator, survey sample size, margin of error, confidence level, population size, how many respondents]
{U}
featured: true
variables:
  - id: zc
    label: Confidence level
    default: 1.959964
    options:
      - {{ label: 90%, value: 1.644854 }}
      - {{ label: 95%, value: 1.959964 }}
      - {{ label: 99%, value: 2.575829 }}
  - {{ id: E, label: Margin of error, family: percent, unit: '%', default: 5, min: 0.0001, max: 0.5 }}
  - {{ id: p, label: Expected proportion (use 50% if unsure), family: percent, unit: '%', default: 50, min: 0.0001, max: 0.9999 }}
  - {{ id: N, label: Population size, default: 10000, min: 1 }}
  - {{ id: n0, label: Sample size (infinite population), min: 0, decimals: 0 }}
  - {{ id: n, label: Sample size needed, min: 0, decimals: 0 }}
equations:
  - n0 = ceil(zc^2 * p * (1 - p) / E^2)
  - n = ceil(zc^2 * p * (1 - p) / E^2 / (1 + (zc^2 * p * (1 - p) / E^2 - 1) / N))
faq:
  - q: How many people do I need to survey?
    a: For a large population, 95% confidence and ±5% margin, about 385 responses. For ±3%, about 1,068.
  - q: Why use 50% for the proportion?
    a: It gives the largest (safest) sample size when you don't know the expected result.
  - q: Does population size matter much?
    a: Only for small populations. Above about 20,000, the required sample barely changes.
related: [statistics/margin-of-error, statistics/confidence-interval]
''',f'''
## How to use this calculator

Choose the **confidence level**, set the **margin of error** and the **population size**. Leave the expected proportion at 50% unless you have a prior estimate. Round the result **up**.

## Formulas

<p class="formula">n₀ = z² p(1 − p) ÷ E²   n = n₀ ÷ (1 + (n₀ − 1) ÷ N)</p>

## Worked example

95% confidence, ±5%, p = 50%, population 10,000:

- n₀ = 1.96² × 0.25 ÷ 0.0025 = 384.1 → **{math.ceil(1.959964**2*0.25/0.0025)}**
- With the population correction: **{math.ceil((1.959964**2*0.25/0.0025)/(1+((1.959964**2*0.25/0.0025)-1)/10000))}** responses

## Typical sample sizes (large population, 95%)

| Margin of error | Sample size |
|---|---|
| ±10% | {math.ceil(1.959964**2*0.25/0.01)} |
| ±5% | {math.ceil(1.959964**2*0.25/0.0025)} |
| ±3% | {math.ceil(1.959964**2*0.25/0.0009)} |
| ±2% | {math.ceil(1.959964**2*0.25/0.0004)} |
| ±1% | {math.ceil(1.959964**2*0.25/0.0001)} |

Account for non-responses: if you expect a 20% response rate, invite five times as many people.
''')

page(C,'margin-of-error',f'''
title: Margin of Error Calculator
description: Calculate the margin of error for a survey or poll from sample size, proportion and confidence level.
category: statistics
keywords: [margin of error calculator, poll margin of error, survey accuracy, plus or minus, confidence level]
{U}
variables:
  - id: zc
    label: Confidence level
    default: 1.959964
    options:
      - {{ label: 90%, value: 1.644854 }}
      - {{ label: 95%, value: 1.959964 }}
      - {{ label: 99%, value: 2.575829 }}
  - {{ id: n, label: Sample size, default: 1000, min: 1 }}
  - {{ id: p, label: Observed proportion, family: percent, unit: '%', default: 50, min: 0, max: 1 }}
  - {{ id: E, label: Margin of error (±), family: percent, unit: '%', min: 0 }}
equations:
  - E = zc * sqrt(p * (1 - p) / n)
chart: {{ x: n, y: E, from: 100, to: 3000 }}
faq:
  - q: What does "±3%" mean in a poll?
    a: If 52% support a policy with a ±3% margin at 95% confidence, the true value is likely between 49% and 55%.
  - q: How does sample size affect it?
    a: The margin shrinks with the square root of n. Quadrupling the sample halves the margin of error.
  - q: Does it cover all poll errors?
    a: No — only random sampling error. Biased samples, poor question wording and non-response can add more.
related: [statistics/sample-size, statistics/confidence-interval]
''',f'''
## How to use this calculator

Choose the **confidence level** and enter the **sample size** and **observed proportion**. The margin of error appears as ± percentage points.

## Formula

<p class="formula">E = z × √( p(1 − p) ÷ n )</p>

## Worked example

A poll of 1,000 people finds 50% support, at 95% confidence:

E = 1.96 × √(0.25 ÷ 1000) = **±{1.959964*math.sqrt(0.25/1000)*100:.1f}%**

## Margin by sample size (p = 50%, 95%)

| Sample size | Margin of error |
|---|---|
| 100 | ±{1.959964*math.sqrt(0.25/100)*100:.1f}% |
| 400 | ±{1.959964*math.sqrt(0.25/400)*100:.1f}% |
| 1,000 | ±{1.959964*math.sqrt(0.25/1000)*100:.1f}% |
| 2,500 | ±{1.959964*math.sqrt(0.25/2500)*100:.1f}% |
''')

page(C,'permutations',f'''
title: Permutation Calculator (nPr)
description: Calculate the number of permutations — ordered arrangements of r items chosen from n.
category: statistics
keywords: [permutation calculator, npr, arrangements, order matters, factorial, combinatorics]
{U}
variables:
  - {{ id: n, label: Total items (n), default: 10, min: 0 }}
  - {{ id: r, label: Items chosen (r), default: 3, min: 0 }}
  - {{ id: P, label: Permutations (nPr), min: 0 }}
equations:
  - P = nPr(n, r)
faq:
  - q: What is a permutation?
    a: An arrangement where order matters. Choosing a 1st, 2nd and 3rd place from 10 runners is a permutation.
  - q: What is the formula?
    a: nPr = n! ÷ (n − r)!. For 10 and 3, 10 × 9 × 8 = 720.
  - q: How is it different from combinations?
    a: Combinations ignore order. nPr = nCr × r!, so there are always more permutations than combinations.
related: [statistics/combinations, statistics/probability]
''',f'''
## How to use this calculator

Enter the **total number of items** and how many are **chosen**. The number of ordered arrangements is calculated.

## Formula

<p class="formula">nPr = n! ÷ (n − r)!</p>

## Worked example

Gold, silver and bronze from 10 runners:

10P3 = 10 × 9 × 8 = **{math.perm(10,3)}**

## More examples

| Situation | Calculation | Result |
|---|---|---|
| 4-digit PIN, no repeated digits | 10P4 | {math.perm(10,4):,} |
| Arrange 5 books on a shelf | 5P5 | {math.perm(5,5)} |
| President, VP, secretary from 20 | 20P3 | {math.perm(20,3):,} |
''')

page(C,'combinations',f'''
title: Combination Calculator (nCr)
description: Calculate the number of combinations — ways to choose r items from n when order doesn't matter. Lottery odds included.
category: statistics
keywords: [combination calculator, ncr, n choose r, binomial coefficient, lottery odds, combinatorics]
{U}
featured: true
variables:
  - {{ id: n, label: Total items (n), default: 49, min: 0 }}
  - {{ id: r, label: Items chosen (r), default: 6, min: 0 }}
  - {{ id: Cn, label: Combinations (nCr), min: 0 }}
  - {{ id: odds, label: Chance of picking one specific combination, family: percent, unit: '%', min: 0 }}
equations:
  - Cn = nCr(n, r)
  - odds = 1 / Cn
faq:
  - q: What is a combination?
    a: A selection where order doesn't matter, such as choosing 3 toppings from 10.
  - q: What is the formula?
    a: nCr = n! ÷ (r! (n − r)!).
  - q: What are the odds of winning a 6/49 lottery?
    a: 1 in 13,983,816 for the jackpot.
related: [statistics/permutations, statistics/binomial-probability, statistics/probability]
''',f'''
## How to use this calculator

Enter the **total items** and how many are **chosen**. You get the number of possible combinations and the chance of picking one specific combination.

## Formula

<p class="formula">nCr = n! ÷ ( r! × (n − r)! )</p>

## Worked examples

- **6/49 lottery:** 49C6 = **{math.comb(49,6):,}**
- **Pizza:** choose 3 toppings from 10 → **{math.comb(10,3)}** combinations
- **Teams:** pick 5 players from 12 → **{math.comb(12,5)}** teams

## Pascal's triangle

nCr values form Pascal's triangle — each number is the sum of the two above it. They are also the coefficients in (a + b)ⁿ.
''')

page(C,'probability',f'''
title: Probability Calculator (Two Events)
description: Calculate the probability of A and B, A or B, not A, and neither — for two independent events.
category: statistics
keywords: [probability calculator, independent events, a and b, a or b, complement, probability of both]
{U}
variables:
  - {{ id: pa, label: Probability of A, family: percent, unit: '%', default: 50, min: 0, max: 1 }}
  - {{ id: pb, label: Probability of B, family: percent, unit: '%', default: 30, min: 0, max: 1 }}
  - {{ id: pand, label: P(A and B), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: por, label: P(A or B), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: pnota, label: P(not A), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: pnone, label: P(neither A nor B), family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - pand = pa * pb
  - por = pa + pb - pand
  - pnota = 1 - pa
  - pnone = 1 - por
faq:
  - q: How do I find the probability of two events both happening?
    a: For independent events, multiply — P(A and B) = P(A) × P(B).
  - q: How do I find the probability of either event?
    a: P(A or B) = P(A) + P(B) − P(A and B), so the overlap isn't counted twice.
  - q: What does independent mean?
    a: One event doesn't change the chance of the other, like two separate coin flips.
related: [statistics/combinations, statistics/binomial-probability, statistics/odds-probability]
''',f'''
## How to use this calculator

Enter the probabilities of two **independent** events A and B (as percentages). All combined probabilities are calculated.

## Formulas

<p class="formula">P(A and B) = P(A) × P(B)<br/>P(A or B) = P(A) + P(B) − P(A)P(B)<br/>P(not A) = 1 − P(A)</p>

## Worked example

P(A) = 50%, P(B) = 30%:

- Both = **15%**
- Either = 50 + 30 − 15 = **65%**
- Neither = **35%**

## At least once in several tries

The chance of at least one six in four dice rolls is 1 − (5/6)⁴ = **{(1-(5/6)**4)*100:.1f}%** — a classic gambling puzzle.
''')

n,k,p=10,3,0.5
page(C,'binomial-probability',f'''
title: Binomial Probability Calculator
description: Calculate the probability of exactly k successes in n independent trials with success probability p.
category: statistics
keywords: [binomial probability, binomial distribution, exactly k successes, bernoulli trials, coin flip probability]
{U}
variables:
  - {{ id: n, label: Number of trials (n), default: 10, min: 0 }}
  - {{ id: k, label: Number of successes (k), default: 3, min: 0 }}
  - {{ id: p, label: Probability of success per trial, family: percent, unit: '%', default: 50, min: 0, max: 1 }}
  - {{ id: P, label: P(exactly k successes), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: mu, label: Expected successes (n × p), min: 0 }}
equations:
  - P = nCr(n, k) * p^k * (1 - p)^(n - k)
  - mu = n * p
faq:
  - q: When does the binomial distribution apply?
    a: When there is a fixed number of independent trials, each with the same two outcomes (success/failure) and the same probability.
  - q: What is the probability of exactly 3 heads in 10 coin flips?
    a: About 11.7%.
  - q: How do I get "at most" or "at least" probabilities?
    a: Add the exact probabilities for each value of k in the range.
related: [statistics/combinations, statistics/probability, statistics/poisson-probability]
''',f'''
## How to use this calculator

Enter the **number of trials**, the **number of successes** you want and the **probability of success** in one trial. The probability of exactly that many successes is calculated, plus the expected number.

## Formula

<p class="formula">P(X = k) = C(n, k) × p<sup>k</sup> × (1 − p)<sup>n − k</sup></p>

## Worked example

3 heads in 10 fair coin flips:

P = 120 × 0.5³ × 0.5⁷ = **{math.comb(10,3)*0.5**10*100:.2f}%**

## Quality-control example

If 2% of parts are faulty, the chance a box of 50 has **no** faulty parts is 0.98⁵⁰ = **{0.98**50*100:.1f}%**.
''')

page(C,'normal-distribution',f'''
title: Normal Distribution Probability Calculator
description: Find the probability that a normally distributed value is below, above or between limits — from mean and standard deviation.
category: statistics
keywords: [normal distribution calculator, bell curve, probability, normal cdf, between two values, percentile]
{U}
variables:
  - {{ id: mu, label: Mean (μ), default: 100 }}
  - {{ id: s, label: Standard deviation (σ), default: 15, min: 0.0000001 }}
  - {{ id: a, label: Lower limit (a), default: 85 }}
  - {{ id: b, label: Upper limit (b), default: 115 }}
  - {{ id: pbelow, label: P(X < b), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: pabove, label: P(X > b), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: pbetween, label: P(a < X < b), family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - pbelow = normcdf((b - mu) / s)
  - pabove = 1 - pbelow
  - pbetween = pbelow - normcdf((a - mu) / s)
faq:
  - q: What is the normal distribution?
    a: The symmetric bell-shaped curve that describes many natural measurements, such as heights, test scores and measurement errors.
  - q: What is the probability within one standard deviation?
    a: About 68.3%. Within two SDs about 95.4%, and within three about 99.7%.
  - q: Can I find a value from a probability?
    a: Yes. Press × on the upper limit and type the probability below it.
related: [statistics/z-score, statistics/empirical-rule]
''',f'''
## How to use this calculator

Enter the **mean** and **standard deviation**, and the **lower** and **upper limits**. You get the probability below the upper limit, above it, and between the two limits.

## Formulas

<p class="formula">P(X &lt; b) = Φ((b − μ) ÷ σ)<br/>P(a &lt; X &lt; b) = Φ((b − μ) ÷ σ) − Φ((a − μ) ÷ σ)</p>

## Worked example — IQ scores (μ = 100, σ = 15)

- P(85 < IQ < 115) = **{(Phi(1)-Phi(-1))*100:.1f}%**
- P(IQ > 115) = **{(1-Phi(1))*100:.1f}%**
- P(IQ > 130) = **{(1-Phi(2))*100:.2f}%**

## Manufacturing example

Bolts have a mean length of 50.0 mm with σ = 0.1 mm and a tolerance of 49.8–50.2 mm. The share within tolerance is {(Phi(2)-Phi(-2))*100:.1f}%, so about {(1-(Phi(2)-Phi(-2)))*100:.1f}% are rejected.
''')

page(C,'coefficient-of-variation',f'''
title: Coefficient of Variation Calculator
description: Calculate the coefficient of variation (relative standard deviation) of a data set to compare variability.
category: statistics
keywords: [coefficient of variation, cv, relative standard deviation, rsd, variability, precision]
{U}
dataset:
  label: Your data
  default: '98.2, 101.5, 99.8, 100.4, 100.9, 99.1'
variables:
  - {{ id: cv, label: Coefficient of variation (sample), family: percent, unit: '%' }}
  - {{ id: sd, label: Standard deviation (sample) }}
  - {{ id: mean, label: Mean }}
equations:
  - cv = data_sd / data_mean
  - sd = data_sd
  - mean = data_mean
faq:
  - q: What is the coefficient of variation?
    a: The standard deviation divided by the mean, as a percentage. It shows variability relative to the size of the values.
  - q: When is it useful?
    a: Comparing the spread of data sets with different units or very different means, such as lab precision or investment risk.
  - q: Is there a good CV value?
    a: It depends on the field. In analytical labs, a CV under 2–5% often indicates good precision.
related: [statistics/standard-deviation, statistics/standard-error]
''',f'''
## How to use this calculator

Paste your measurements. The coefficient of variation, standard deviation and mean are calculated.

## Formula

<p class="formula">CV = s ÷ x̄ × 100%</p>

## Worked example

Six repeat measurements: 98.2, 101.5, 99.8, 100.4, 100.9, 99.1

- Mean = **{st.mean([98.2,101.5,99.8,100.4,100.9,99.1]):.3f}**
- s = **{st.stdev([98.2,101.5,99.8,100.4,100.9,99.1]):.3f}**
- CV = **{st.stdev([98.2,101.5,99.8,100.4,100.9,99.1])/st.mean([98.2,101.5,99.8,100.4,100.9,99.1])*100:.2f}%**

## Comparing different scales

A bolt varying by ±0.1 mm on 10 mm (CV 1%) is relatively less consistent than a beam varying by ±5 mm on 6 m (CV 0.08%), even though 5 mm is a bigger number.
''')

SE=[12,15,11,14,13,16,12,14,15,13]
page(C,'standard-error',f'''
title: Standard Error of the Mean Calculator
description: Calculate the standard error of the mean (SEM) from your data — or from standard deviation and sample size.
category: statistics
keywords: [standard error, sem, standard error of the mean, sample size, precision of mean]
{U}
dataset:
  label: Your data
  default: '12, 15, 11, 14, 13, 16, 12, 14, 15, 13'
variables:
  - {{ id: se, label: Standard error of the mean }}
  - {{ id: sd, label: Standard deviation (sample) }}
  - {{ id: n, label: Sample size }}
  - {{ id: mean, label: Mean }}
equations:
  - se = data_sd / sqrt(data_n)
  - sd = data_sd
  - n = data_n
  - mean = data_mean
faq:
  - q: What is the standard error?
    a: The standard deviation of the sample mean — how much the mean would vary if you repeated the sampling.
  - q: How is it different from standard deviation?
    a: SD describes spread in the data; SE describes uncertainty in the mean. SE = SD ÷ √n, so it shrinks as the sample grows.
  - q: How is SE used?
    a: To build confidence intervals — roughly, mean ± 2 SE gives a 95% interval.
related: [statistics/standard-deviation, statistics/confidence-interval]
''',f'''
## How to use this calculator

Paste your sample data. The standard error, standard deviation, sample size and mean are calculated.

## Formula

<p class="formula">SE = s ÷ √n</p>

## Worked example

Data: 12, 15, 11, 14, 13, 16, 12, 14, 15, 13

- Mean = **{st.mean(SE):g}**, s = **{st.stdev(SE):.3f}**
- SE = {st.stdev(SE):.3f} ÷ √10 = **{st.stdev(SE)/math.sqrt(10):.3f}**
- Approximate 95% interval: {st.mean(SE):g} ± {2*st.stdev(SE)/math.sqrt(10):.2f}

## Sample size effect

To halve the standard error you need **four times** as many observations.
''')

G=[1.05,1.10,0.95,1.20]
page(C,'geometric-mean',f'''
title: Geometric Mean Calculator
description: Calculate the geometric mean of positive numbers — the correct average for growth rates, ratios and returns.
category: statistics
keywords: [geometric mean calculator, average growth rate, average return, compound average, multiplicative mean]
{U}
dataset:
  label: Your positive numbers
  default: '1.05, 1.10, 0.95, 1.20'
variables:
  - {{ id: gm, label: Geometric mean }}
  - {{ id: am, label: Arithmetic mean (for comparison) }}
  - {{ id: n, label: Count }}
equations:
  - gm = data_gmean
  - am = data_mean
  - n = data_n
faq:
  - q: What is the geometric mean?
    a: The nth root of the product of n numbers. It is the right average for quantities that multiply together, such as growth factors.
  - q: Why can't I use the normal average for returns?
    a: Returns compound. +50% then −50% averages 0% arithmetically, but you actually lose 25%. The geometric mean shows the true rate.
  - q: Can I use zero or negative numbers?
    a: No. Convert percentage returns to growth factors first (+5% → 1.05, −5% → 0.95).
related: [finance/cagr, math/average]
''',f'''
## How to use this calculator

Enter positive numbers. For percentage changes, enter **growth factors**: +5% → 1.05, −5% → 0.95.

## Formula

<p class="formula">GM = (x₁ × x₂ × … × xₙ)<sup>1/n</sup></p>

## Worked example — four years of returns

Returns of +5%, +10%, −5%, +20% → factors 1.05, 1.10, 0.95, 1.20

- Geometric mean = **{math.prod(G)**0.25:.4f}** → average growth **{(math.prod(G)**0.25-1)*100:.2f}% per year**
- Arithmetic mean = {st.mean(G):.4f} → overstates growth at {(st.mean(G)-1)*100:.2f}%

## When to use it

- Investment returns and CAGR
- Population or sales growth rates
- Averaging ratios and indexes
''')

page(C,'odds-probability',f'''
title: Odds to Probability Converter
description: Convert betting or statistical odds to probability and back — fractional odds, decimal odds and percentage chance.
category: statistics
keywords: [odds to probability, probability to odds, odds converter, implied probability, decimal odds, odds ratio]
{U}
variables:
  - {{ id: w, label: Odds in favour — "for" part (e.g. 1 in 1:4), default: 1, min: 0 }}
  - {{ id: l, label: Odds — "against" part (e.g. 4 in 1:4), default: 4, min: 0 }}
  - {{ id: p, label: Probability, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: dec, label: Decimal odds (bookmaker style), min: 1 }}
equations:
  - p = w / (w + l)
  - dec = 1 / p
faq:
  - q: How do I convert odds to probability?
    a: For odds of a to b in favour, probability = a ÷ (a + b). Odds of 1:4 mean a 20% chance.
  - q: What are decimal odds?
    a: The total return per unit staked, including the stake. Decimal odds of 5.0 imply a 20% chance.
  - q: Are bookmaker odds true probabilities?
    a: No. Bookmakers build in a margin, so the implied probabilities of all outcomes add up to more than 100%.
related: [statistics/probability, statistics/relative-risk]
''',f'''
## How to use this calculator

Enter the odds as two numbers — **for** and **against** (1:4 means 1 for, 4 against). The probability and decimal odds are calculated. Or type a probability to get the odds.

## Formulas

<p class="formula">p = a ÷ (a + b)   decimal odds = 1 ÷ p</p>

## Examples

| Odds (for:against) | Probability | Decimal |
|---|---|---|
| 1:1 | 50% | 2.00 |
| 1:4 | 20% | 5.00 |
| 3:1 | 75% | 1.33 |
| 1:99 | 1% | 100 |

## Odds against

Fractional betting odds such as "4/1" usually mean 4 **against** 1 for — a 20% implied chance.
''')

a_,b_,c_,d_=30,70,10,90
page(C,'relative-risk',f'''
title: Relative Risk & Odds Ratio Calculator
description: Calculate relative risk, odds ratio and absolute risk difference from a 2×2 table of exposed and unexposed groups.
category: statistics
keywords: [relative risk, odds ratio, risk ratio, 2x2 table, epidemiology, absolute risk reduction, nnt]
{U}
variables:
  - {{ id: a, label: Exposed — with outcome (a), default: 30, min: 0 }}
  - {{ id: b, label: Exposed — without outcome (b), default: 70, min: 0 }}
  - {{ id: c, label: Unexposed — with outcome (c), default: 10, min: 0 }}
  - {{ id: d, label: Unexposed — without outcome (d), default: 90, min: 0 }}
  - {{ id: rr, label: Relative risk (RR), min: 0, decimals: 3 }}
  - {{ id: orr, label: Odds ratio (OR), min: 0, decimals: 3 }}
  - {{ id: ard, label: Absolute risk difference, family: percent, unit: '%' }}
equations:
  - rr = (a / (a + b)) / (c / (c + d))
  - orr = (a * d) / (b * c)
  - ard = a / (a + b) - c / (c + d)
faq:
  - q: What is relative risk?
    a: The risk of the outcome in the exposed group divided by the risk in the unexposed group. RR = 3 means three times the risk.
  - q: What is the difference between RR and OR?
    a: RR compares probabilities; OR compares odds. They are similar when the outcome is rare, but OR exaggerates the effect when the outcome is common.
  - q: What is the number needed to treat (NNT)?
    a: 1 ÷ absolute risk difference. If a treatment reduces risk by 20 percentage points, NNT = 5.
related: [statistics/odds-probability, statistics/probability]
''',f'''
## How to use this calculator

Fill in the 2×2 table: how many people in the **exposed** and **unexposed** groups had or did not have the outcome.

| | Outcome | No outcome |
|---|---|---|
| Exposed | a | b |
| Unexposed | c | d |

## Formulas

<p class="formula">RR = [a/(a+b)] ÷ [c/(c+d)]   OR = ad ÷ bc</p>

## Worked example

30 of 100 exposed and 10 of 100 unexposed people developed the outcome:

- Risk exposed = 30%, risk unexposed = 10%
- RR = **{(30/100)/(10/100):.2f}**
- OR = 30 × 90 ÷ (70 × 10) = **{30*90/(70*10):.2f}**
- Absolute risk difference = **20 percentage points** (NNH = 5)
''')

S=[2,4,4,4,5,5,7,9]
page(C,'sum-of-squares',f'''
title: Sum of Squares Calculator
description: Calculate the total sum of squares (squared deviations from the mean) and the sum of squared values for a data set.
category: statistics
keywords: [sum of squares, ss, squared deviations, total sum of squares, anova, variance]
{U}
dataset:
  label: Your data
  default: '2, 4, 4, 4, 5, 5, 7, 9'
variables:
  - {{ id: ss, label: Sum of squared deviations Σ(x − x̄)² }}
  - {{ id: sq, label: Sum of squares of values Σx² }}
  - {{ id: mean, label: Mean }}
  - {{ id: n, label: Count }}
equations:
  - ss = data_sumsq - data_n * data_mean^2
  - sq = data_sumsq
  - mean = data_mean
  - n = data_n
faq:
  - q: What is the sum of squares?
    a: In statistics it usually means the sum of squared deviations from the mean, Σ(x − x̄)² — the basis of variance and ANOVA.
  - q: How does it relate to variance?
    a: Sample variance = SS ÷ (n − 1); population variance = SS ÷ n.
  - q: Why square the deviations?
    a: So negative and positive deviations don't cancel out, and so larger deviations count more.
related: [statistics/standard-deviation, statistics/coefficient-of-variation]
''',f'''
## How to use this calculator

Paste your data to get the sum of squared deviations, the sum of squared values, the mean and the count.

## Formulas

<p class="formula">SS = Σ(x − x̄)² = Σx² − n x̄²</p>

## Worked example

Data: 2, 4, 4, 4, 5, 5, 7, 9 (mean = 5)

- Σx² = {sum(x*x for x in S)}
- SS = {sum(x*x for x in S)} − 8 × 25 = **{sum((x-5)**2 for x in S)}**
- Population variance = 32 ÷ 8 = 4 → σ = 2
''')

lam=3
page(C,'poisson-probability',f'''
title: Poisson Probability Calculator
description: Calculate the probability of exactly k events in an interval when events occur at an average rate λ.
category: statistics
keywords: [poisson distribution, poisson probability, events per hour, lambda, rare events, queueing]
{U}
variables:
  - {{ id: lam, label: Average number of events (λ), default: 3, min: 0 }}
  - {{ id: k, label: Number of events (k), default: 5, min: 0 }}
  - {{ id: P, label: P(exactly k events), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: P0, label: P(no events), family: percent, unit: '%', min: 0, max: 1 }}
equations:
  - P = lam^k * exp(-lam) / fact(k)
  - P0 = exp(-lam)
faq:
  - q: When is the Poisson distribution used?
    a: For counts of independent events happening at a constant average rate — calls per hour, defects per metre, arrivals per minute.
  - q: What is λ?
    a: The expected (average) number of events in the interval.
  - q: How is it related to the binomial distribution?
    a: It approximates the binomial when trials are many and the success probability is small, with λ = n × p.
related: [statistics/binomial-probability, statistics/probability]
''',f'''
## How to use this calculator

Enter the **average rate** λ for your interval and the **number of events** k. The probability of exactly k events and of none are calculated.

## Formula

<p class="formula">P(X = k) = λ<sup>k</sup> e<sup>−λ</sup> ÷ k!</p>

## Worked example

A help desk averages 3 calls per hour. The chance of exactly 5 calls in an hour:

P = 3⁵ × e⁻³ ÷ 120 = **{lam**5*math.exp(-lam)/120*100:.2f}%**

The chance of a quiet hour with no calls is e⁻³ = **{math.exp(-3)*100:.2f}%**.

## Distribution for λ = 3

| k | P(X = k) |
|---|---|
| 0 | {math.exp(-3)*100:.1f}% |
| 1 | {3*math.exp(-3)*100:.1f}% |
| 2 | {9*math.exp(-3)/2*100:.1f}% |
| 3 | {27*math.exp(-3)/6*100:.1f}% |
| 4 | {81*math.exp(-3)/24*100:.1f}% |
| 5 | {243*math.exp(-3)/120*100:.1f}% |
''')

page(C,'empirical-rule',f'''
title: Empirical Rule Calculator (68–95–99.7)
description: Find the ranges containing 68%, 95% and 99.7% of values in a normal distribution from the mean and standard deviation.
category: statistics
keywords: [empirical rule, 68 95 99.7 rule, three sigma rule, normal distribution ranges, standard deviation]
{U}
variables:
  - {{ id: mu, label: Mean (μ), default: 170 }}
  - {{ id: s, label: Standard deviation (σ), default: 8, min: 0 }}
  - {{ id: l1, label: 68% range — lower (μ − σ) }}
  - {{ id: u1, label: 68% range — upper (μ + σ) }}
  - {{ id: l2, label: 95% range — lower (μ − 2σ) }}
  - {{ id: u2, label: 95% range — upper (μ + 2σ) }}
  - {{ id: l3, label: 99.7% range — lower (μ − 3σ) }}
  - {{ id: u3, label: 99.7% range — upper (μ + 3σ) }}
equations:
  - l1 = mu - s
  - u1 = mu + s
  - l2 = mu - 2 * s
  - u2 = mu + 2 * s
  - l3 = mu - 3 * s
  - u3 = mu + 3 * s
faq:
  - q: What is the empirical rule?
    a: For a normal distribution, about 68% of values lie within 1 standard deviation of the mean, 95% within 2, and 99.7% within 3.
  - q: Does it work for any data?
    a: Only for roughly bell-shaped (normal) data. For skewed data, the percentages can be very different.
  - q: What is "six sigma"?
    a: A quality approach aiming for processes so consistent that defects are extremely rare — about 3.4 per million opportunities under its conventions.
related: [statistics/normal-distribution, statistics/z-score, statistics/standard-deviation]
''',f'''
## How to use this calculator

Enter the **mean** and **standard deviation**. The 68%, 95% and 99.7% ranges are calculated.

## The rule

<p class="formula">μ ± 1σ ≈ 68%   μ ± 2σ ≈ 95%   μ ± 3σ ≈ 99.7%</p>

## Worked example — adult heights

Mean 170 cm, SD 8 cm:

- 68% are between **162 and 178 cm**
- 95% are between **154 and 186 cm**
- 99.7% are between **146 and 194 cm**

## Exact values

The precise percentages are {(Phi(1)-Phi(-1))*100:.2f}%, {(Phi(2)-Phi(-2))*100:.2f}% and {(Phi(3)-Phi(-3))*100:.2f}%. For other ranges, use the [normal distribution calculator](/statistics/normal-distribution/).
''')
print('statistics ok')
