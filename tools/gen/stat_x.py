import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
C = math.comb
def Phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))

rows = ''.join(f"| {k} | {C(10,k)*0.5**10*100:.2f}% | {sum(C(10,j)*0.5**10 for j in range(k+1))*100:.2f}% | {sum(C(10,j)*0.5**10 for j in range(k,11))*100:.2f}% |\n" for k in range(11))
expand('statistics/binomial-probability', f'''
## Full distribution: 10 coin tosses (p = 0.5)

| Heads (k) | P(exactly k) | P(k or fewer) | P(k or more) |
|---|---|---|---|
{rows}
## “At least” and “at most”

The calculator gives the probability of **exactly** k successes. For cumulative questions, add the exact probabilities:

- P(at most k) = P(0) + P(1) + … + P(k)
- P(at least k) = 1 − P(at most k − 1)
- P(at least 1) = 1 − (1 − p)<sup>n</sup>

## Mean and spread

| Measure | Formula |
|---|---|
| Mean | n × p |
| Variance | n × p × (1 − p) |
| Standard deviation | √(n × p × (1 − p)) |

## When to use the binomial distribution

All four conditions must hold:

1. A fixed number of trials, n.
2. Each trial has two outcomes (success or failure).
3. The probability p is the same on every trial.
4. Trials are independent.

Drawing cards without replacement breaks condition 3 — use the hypergeometric distribution instead.

## Normal approximation

When n × p and n × (1 − p) are both at least about 10, the binomial is close to a normal distribution with the mean and standard deviation above. Use the [normal distribution calculator](/statistics/normal-distribution/) for quick estimates.
''', [
 ('What is the probability of getting exactly 5 heads in 10 tosses?', '24.61%.'),
 ('What does nCr mean in the binomial formula?', 'The number of ways to choose which k of the n trials are successes. See the combinations calculator.'),
], before='## Quality-control example')

expand('statistics/coefficient-of-variation', '''
## Interpreting CV

| CV | Typical interpretation |
|---|---|
| Below 10% | Low variability |
| 10–20% | Moderate |
| 20–30% | High |
| Above 30% | Very high |

These bands are rough guides; acceptable CV depends on the field.

## CV in laboratories

Labs report CV to describe the precision of an assay. Many clinical assays aim for an intra-assay CV under 10% and an inter-assay CV under 15%. Run the same sample several times, enter the results and check the CV.

## CV in finance

In investing, CV = standard deviation of returns ÷ mean return shows risk per unit of return. A fund with a mean return of 12% and a standard deviation of 18% has a CV of 1.5; one with 8% and 9% has a CV of 1.13 — less risk per unit of return.

## When not to use CV

- When the mean is close to zero, CV becomes huge and meaningless.
- For data with negative values or on interval scales such as °C, where zero is arbitrary. Convert temperatures to kelvin first, or use the standard deviation.
- Only use CV for ratio data, where zero means “none”.

## Sample vs population CV

The calculator uses the **sample** standard deviation (n − 1). For a complete population, use the population standard deviation from the [standard deviation calculator](/statistics/standard-deviation/).
''', [
 ('Is a lower coefficient of variation better?', 'It means less relative variability, which is usually better for precision, quality and consistency.'),
 ('Can CV be more than 100%?', 'Yes, when the standard deviation is larger than the mean, which happens with skewed data or means near zero.'),
], before='## Comparing different scales')

expand('statistics/combinations', '''
## Common combinations

| Situation | n | r | Combinations |
|---|---|---|---|
''' + ''.join(f"| {s} | {n} | {r} | {C(n,r):,} |\n" for s, n, r in [('Pick 2 from 5', 5, 2), ('Poker hand', 52, 5), ('Lottery 6 from 49', 49, 6), ('Lottery 5 from 50', 50, 5), ('Team of 11 from 15', 15, 11), ('Committee of 3 from 10', 10, 3), ('Toppings: 3 from 12', 12, 3)]) + '''
## Combinations vs permutations

| | Combinations (nCr) | Permutations (nPr) |
|---|---|---|
| Order matters? | No | Yes |
| Example | A team of 3 | Gold, silver and bronze |
| Formula | n! ÷ (r! (n − r)!) | n! ÷ (n − r)! |
| 3 from 10 | 120 | 720 |

See the [permutations calculator](/statistics/permutations/).

## Combinations with repetition

When items can be chosen more than once (such as scoops of ice cream from flavours):

<p class="formula">C(n + r − 1, r)</p>

3 scoops from 10 flavours, repeats allowed: C(12, 3) = **220**.

## Total subsets

The number of all possible subsets of n items (choosing any number, including none) is 2<sup>n</sup>. With 10 toppings, there are 1,024 possible pizzas.

## Symmetry

C(n, r) = C(n, n − r). Choosing 3 items to include from 10 is the same as choosing 7 to leave out — both give 120.
''', [
 ('How many combinations of 3 from 10 are there?', '120.'),
 ('How many 5-card poker hands are there?', '2,598,960.'),
], before="## Pascal's triangle")

expand('statistics/confidence-interval', '''
## Confidence levels and z-values

| Confidence | z* |
|---|---|
| 80% | 1.282 |
| 90% | 1.645 |
| 95% | 1.960 |
| 98% | 2.326 |
| 99% | 2.576 |
| 99.9% | 3.291 |

## Small samples: use t instead of z

For small samples (n below about 30) with an unknown population standard deviation, use the t-distribution with n − 1 degrees of freedom:

| n | t* for 95% |
|---|---|
| 5 | 2.776 |
| 10 | 2.262 |
| 15 | 2.145 |
| 20 | 2.093 |
| 30 | 2.045 |
| 60 | 2.001 |
| Large | 1.960 |

Replace z* with t* in the formula to get a wider, more honest interval.

## What a 95% interval means

If you repeated the study many times, about 95% of the intervals built this way would contain the true mean. It does **not** mean there is a 95% probability that the true mean lies in this particular interval.

## Narrowing the interval

- **Larger sample**: the margin shrinks with √n — four times the sample halves the margin.
- **Lower confidence**: 90% gives a narrower interval than 99%, at the cost of more risk.
- **Less variable data**: better measurement reduces the standard deviation.

## Proportions

For percentages (such as survey results) use the [margin of error calculator](/statistics/margin-of-error/), which uses the standard error of a proportion.
''', [
 ('What is a 95% confidence interval?', 'A range, built from sample data, that would contain the true population value in about 95% of repeated samples.'),
 ('Should I use z or t?', 'Use t when the sample is small and the population standard deviation is estimated from the sample. For large samples they give almost the same result.'),
], before='## z values')

expand('statistics/empirical-rule', '''
## Beyond three standard deviations

| Range | Share inside | Share outside | About 1 in … outside |
|---|---|---|---|
''' + ''.join(f"| μ ± {k}σ | {(2*Phi(k)-1)*100:.5g}% | {(2-2*Phi(k))*100:.3g}% | {1/(2-2*Phi(k)):,.0f} |\n" for k in [1, 2, 3, 4, 5, 6]) + '''
“Six sigma” quality aims for so few defects that they lie beyond 6σ from the target; in practice the methodology allows a 1.5σ drift and quotes 3.4 defects per million.

## Chebyshev's inequality

For **any** distribution, not just normal ones, at least 1 − 1/k² of the data lies within k standard deviations:

| k | Normal distribution | Any distribution (at least) |
|---|---|---|
| 2 | 95.4% | 75% |
| 3 | 99.7% | 88.9% |
| 4 | 99.994% | 93.75% |

Use the empirical rule only when the data are roughly bell-shaped.

## Spotting outliers

Values more than 3σ from the mean are rare in normal data (about 0.3%) and worth checking for errors. For skewed data, the [quartile and IQR method](/statistics/quartiles/) is more robust.

## Checking for normality

Before applying the rule, look at a histogram. Data that are skewed, have long tails or have two peaks will not follow 68–95–99.7.
''', [
 ('What is the 68-95-99.7 rule?', 'In a normal distribution, about 68% of values are within 1 standard deviation of the mean, 95% within 2 and 99.7% within 3.'),
 ('Does the empirical rule work for all data?', 'No, only for data that are approximately normally distributed. For other data, Chebyshev’s inequality gives guaranteed minimums.'),
], before='## Exact values')

expand('statistics/geometric-mean', '''
## Arithmetic vs geometric mean for returns

| Year | Return | Growth factor |
|---|---|---|
| 1 | +50% | 1.50 |
| 2 | −50% | 0.50 |

- Arithmetic mean return: 0% — suggests you broke even.
- Geometric mean: √(1.5 × 0.5) − 1 = **−13.4%** a year.
- Actual result: 100 → 150 → 75, a 25% loss.

The geometric mean tells the truth about compound growth.

## Using growth factors

For percentage changes, enter **growth factors** (1 + rate), find the geometric mean and subtract 1. For returns of 10%, −5% and 20%, enter 1.10, 0.95 and 1.20. The geometric mean is 1.0784, so the average yearly return is **7.84%**.

## The AM–GM inequality

For positive numbers, the geometric mean is always less than or equal to the arithmetic mean. They are equal only when all values are the same. The more volatile the data, the bigger the gap.

## Harmonic mean

For rates such as speeds over equal distances, use the harmonic mean: n ÷ Σ(1/x). For the same positive data: harmonic ≤ geometric ≤ arithmetic.

## Other uses

- Average growth of populations, sales or prices.
- Comparing items rated on different scales (indices).
- Aspect ratios and image scaling.
- Bacterial counts and other log-normally distributed data.
''', [
 ('Why can’t the geometric mean use zero or negative numbers?', 'It multiplies the values and takes a root. A zero makes the product zero, and negative values can make it undefined. Use growth factors (1 + rate) for returns.'),
 ('Is CAGR a geometric mean?', 'Yes. CAGR is the geometric mean of the yearly growth factors, minus 1.'),
], before='## When to use it')

expand('statistics/margin-of-error', '''
## Margin of error at different proportions

n = 1,000, 95% confidence:

| Observed proportion | Margin of error |
|---|---|
''' + ''.join(f"| {p}% | ±{1.96*math.sqrt(p/100*(1-p/100)/1000)*100:.2f}% |\n" for p in [5, 10, 20, 30, 50, 70, 90]) + '''
The margin is largest at 50%, which is why planners use 50% when they do not know the result in advance.

## Finite population correction

When the sample is a large share of the population (more than about 5%), multiply the margin by:

<p class="formula">√((N − n) ÷ (N − 1))</p>

A sample of 500 from a population of 2,000 has its margin reduced by about 13%.

## What the margin of error does not cover

- **Biased samples**: surveying only people online or only volunteers.
- **Non-response**: people who refuse may differ from those who answer.
- **Question wording** and order effects.
- **Small subgroups**: a poll of 1,000 has a much larger margin for a subgroup of 150.

## Comparing two results

If two candidates poll 48% and 45% with a ±3.1% margin each, the margin on the **difference** is larger — roughly 1.7 to 2 times the single margin. A 3-point lead is within the margin of error.

## Planning a survey

To find the sample size for a target margin, use the [sample size calculator](/statistics/sample-size/).
''', [
 ('What is the margin of error for a sample of 1,000?', 'About ±3.1% at 95% confidence for a proportion near 50%.'),
 ('Does a bigger population need a bigger sample?', 'Hardly. For large populations the margin depends almost entirely on the sample size, not the population size.'),
], before='## Margin by sample size (p = 50%, 95%)')

expand('statistics/mean-median-mode', '''
## Skewed data

The relationship between the three averages shows the shape of the data:

| Shape | Typical order | Example |
|---|---|---|
| Symmetric | Mean ≈ median ≈ mode | Heights, test scores |
| Right-skewed (long tail to the right) | Mode < median < mean | Incomes, house prices |
| Left-skewed (long tail to the left) | Mean < median < mode | Age at retirement, easy test scores |

## Multiple modes

A data set can have:

- **No mode**: every value appears once.
- **One mode** (unimodal).
- **Two modes** (bimodal), which may mean two groups are mixed — such as the heights of men and women together.

The calculator shows the most frequent value; if several values tie, check the data for more than one mode.

## Grouped data

For data in classes (such as 10–19, 20–29), estimate:

- **Mean** = Σ(midpoint × frequency) ÷ total frequency
- **Median class**: the class containing the middle value
- **Modal class**: the class with the highest frequency

## Trimmed mean

A trimmed mean removes a fixed share of the highest and lowest values (often 5–10%) before averaging. Sports judging often drops the top and bottom scores for this reason.
''', [
 ('What is the mean, median and mode of 2, 3, 3, 5, 7?', 'Mean 4, median 3, mode 3.'),
 ('Which average should I use for income data?', 'The median, because a few very high incomes pull the mean upward.'),
], before='## When to use each')

expand('statistics/normal-distribution', '''
## Standard normal table (selected values)

| z | P(Z < z) | z | P(Z < z) |
|---|---|---|---|
''' + ''.join(f"| {a:+.1f} | {Phi(a):.4f} | {b:+.1f} | {Phi(b):.4f} |\n" for a, b in zip([-3.0, -2.5, -2.0, -1.5, -1.0, -0.5], [0.5, 1.0, 1.5, 2.0, 2.5, 3.0])) + '''
## Finding a value from a percentile

To find the value below which a given percentage lies, use x = μ + z × σ. For the top 10% of IQ scores (z = 1.2816): x = 100 + 1.2816 × 15 = **119.2**.

## Properties of the normal curve

- Symmetric around the mean; mean = median = mode.
- About 68%, 95% and 99.7% of values lie within 1, 2 and 3 standard deviations — see the [empirical rule](/statistics/empirical-rule/).
- The tails never reach zero, but become tiny beyond 4σ.

## Where normal distributions appear

- Measurement errors.
- Heights and many biological measurements within a group.
- Manufacturing dimensions around a target.
- Averages of many independent values (the central limit theorem).

## When not to assume normality

Incomes, waiting times, insurance claims and many financial returns are skewed or have heavy tails. Assuming normality there underestimates extreme events.
''', [
 ('What percentage is above one standard deviation?', 'About 15.9% of values lie more than one standard deviation above the mean.'),
 ('How do I find the probability between two values?', 'Enter both limits. The calculator gives P(a < X < b) = P(X < b) − P(X < a).'),
], before='## Manufacturing example')

expand('statistics/odds-probability', '''
## Odds, probability and decimal odds

| Fractional odds (against) | Probability | Decimal odds |
|---|---|---|
''' + ''.join(f"| {a}/{b} | {b/(a+b)*100:.1f}% | {(a+b)/b:.2f} |\n" for a, b in [(1, 4), (1, 2), (4, 5), (1, 1), (6, 4), (2, 1), (3, 1), (5, 1), (10, 1), (100, 1)]) + '''
## American (moneyline) odds

| American | Meaning | Probability |
|---|---|---|
| +200 | Win 200 on a 100 stake | 33.3% |
| +100 | Even money | 50% |
| −150 | Stake 150 to win 100 | 60% |
| −300 | Stake 300 to win 100 | 75% |

Positive: p = 100 ÷ (odds + 100). Negative: p = −odds ÷ (−odds + 100).

## The bookmaker's margin

Add up the implied probabilities for all outcomes in a market. If they total more than 100% — for example 52.4% + 52.4% = 104.8% — the extra 4.8% is the bookmaker's margin (overround). Fair odds would add to exactly 100%.

## Odds in medicine and research

In studies, odds compare people with and without an outcome, and the **odds ratio** compares two groups. Odds and probability are similar only when the outcome is rare. See the [relative risk calculator](/statistics/relative-risk/).
''', [
 ('What does 3 to 1 odds mean?', 'Odds of 3 to 1 against mean 1 win for every 3 losses — a 25% probability.'),
 ('How do I convert probability to odds?', 'Odds in favour = p ÷ (1 − p). A 20% probability is 0.25, or 1 to 4.'),
], before='## Odds against')

expand('statistics/permutations', '''
## Common permutations

| Situation | n | r | Permutations |
|---|---|---|---|
''' + ''.join(f"| {s} | {n} | {r} | {math.perm(n,r):,} |\n" for s, n, r in [('Podium: 3 from 8 runners', 8, 3), ('4-digit PIN, no repeated digits', 10, 4), ('Arrange 5 books on a shelf', 5, 5), ('President, VP, secretary from 20', 20, 3), ('Order of 52 cards', 52, 52)]) + '''
52! is about 8.07 × 10<sup>67</sup>: every well-shuffled deck is almost certainly an order never seen before.

## Permutations with repetition

If items can repeat, there are n<sup>r</sup> arrangements. A 4-digit PIN with repeats allowed has 10<sup>4</sup> = **10,000** possibilities, compared with 5,040 without repeats.

## Arranging letters with duplicates

For words with repeated letters, divide by the factorial of each repeat count. MISSISSIPPI has 11 letters (4 S, 4 I, 2 P):

<p class="formula">11! ÷ (4! × 4! × 2!) = 34,650</p>

## Circular arrangements

Seating n people around a round table, where rotations are the same, gives (n − 1)! arrangements. Six people can sit in 5! = **120** distinct ways.

## Factorials grow fast

| n | n! |
|---|---|
| 5 | 120 |
| 10 | 3,628,800 |
| 15 | 1,307,674,368,000 |
| 20 | 2,432,902,008,176,640,000 |
''', [
 ('How many ways can 3 people finish first, second and third out of 10?', '10 × 9 × 8 = 720.'),
 ('What is the difference between nPr and nCr?', 'nPr counts ordered arrangements; nCr counts unordered selections. nPr = nCr × r!.'),
], before='## More examples')

expand('statistics/poisson-probability', '''
## Cumulative probabilities for λ = 3

| k | P(exactly k) | P(k or fewer) | P(more than k) |
|---|---|---|---|
''' + ''.join(f"| {k} | {3**k*math.exp(-3)/math.factorial(k)*100:.2f}% | {sum(3**j*math.exp(-3)/math.factorial(j) for j in range(k+1))*100:.2f}% | {(1-sum(3**j*math.exp(-3)/math.factorial(j) for j in range(k+1)))*100:.2f}% |\n" for k in range(9)) + '''
## When to use the Poisson distribution

- Events happen independently.
- The average rate (λ) is constant over the interval.
- Two events cannot happen at exactly the same instant.

Examples: calls to a help desk per hour, defects per metre of cable, arrivals at a counter, typos per page.

## Changing the interval

λ scales with the interval. If a shop averages 12 customers an hour, use λ = 3 for a 15-minute window and λ = 24 for two hours.

## Mean and variance

For a Poisson distribution, the mean and variance are both equal to λ. If your data's variance is much larger than its mean, events are clustered and the Poisson model will underestimate extremes.

## Poisson approximation to the binomial

When n is large and p is small (such as n ≥ 50 and n × p ≤ 5), the [binomial](/statistics/binomial-probability/) is well approximated by Poisson with λ = n × p.
''', [
 ('What is λ in the Poisson formula?', 'The average number of events in the interval you are studying.'),
 ('What is the probability of at least one event?', 'P(at least 1) = 1 − e^(−λ). For λ = 3, it is about 95%.'),
], before='## Distribution for λ = 3')

expand('statistics/probability', '''
## Independent vs mutually exclusive

| | Independent | Mutually exclusive |
|---|---|---|
| Meaning | One does not affect the other | Cannot both happen |
| P(A and B) | P(A) × P(B) | 0 |
| P(A or B) | P(A) + P(B) − P(A)P(B) | P(A) + P(B) |
| Example | Two coin tosses | Rolling a 2 or a 5 on one die |

The calculator assumes **independent** events.

## Conditional probability

When events are not independent:

<p class="formula">P(A and B) = P(A) × P(B given A)</p>

Drawing two aces from a deck without replacement: 4/52 × 3/51 = **0.45%**.

## Bayes' theorem

<p class="formula">P(A given B) = P(B given A) × P(A) ÷ P(B)</p>

**Example**: a test is 99% sensitive and 95% specific for a condition affecting 1% of people. If you test positive, the chance you have it is 0.99 × 0.01 ÷ (0.99 × 0.01 + 0.05 × 0.99) ≈ **16.7%** — surprisingly low, because false positives from the 99% without the condition outnumber true positives.

## Dice probabilities (two dice)

| Total | Ways | Probability |
|---|---|---|
| 2 or 12 | 1 | 2.78% |
| 3 or 11 | 2 | 5.56% |
| 4 or 10 | 3 | 8.33% |
| 5 or 9 | 4 | 11.11% |
| 6 or 8 | 5 | 13.89% |
| 7 | 6 | 16.67% |
''', [
 ('What is the probability of rolling a 6 on a die?', '1 in 6, or about 16.7%.'),
 ('What is the probability of two independent events both happening?', 'Multiply them: P(A) × P(B). Two heads in a row is 0.5 × 0.5 = 25%.'),
], before='## At least once in several tries')

expand('statistics/quartiles', '''
## Different quartile methods

Software packages use several slightly different methods, which can give different Q1 and Q3 for small data sets:

| Method | Used by |
|---|---|
| Exclusive median (Tukey) | Many textbooks, TI calculators |
| Inclusive median | Some textbooks |
| Linear interpolation (type 7) | Excel QUARTILE.INC, R default, NumPy |
| Type 6 | Excel QUARTILE.EXC, Minitab, SPSS |

For large data sets the methods agree closely. Note which method you used in reports.

## Percentiles

Quartiles are special percentiles: Q1 = 25th, Q2 = 50th (median), Q3 = 75th. Deciles split data into tenths. The 90th percentile is often used for response times and growth charts.

## Five-number summary

Minimum, Q1, median, Q3 and maximum together describe the spread and skew of the data, and are what a box plot draws.

## Outliers

Values below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR are flagged as possible outliers. Using 3 × IQR marks “extreme” outliers. Always check outliers rather than deleting them automatically — they may be errors or the most interesting points.

## IQR vs standard deviation

The IQR ignores extreme values, so it is a robust measure of spread for skewed data. For roughly normal data, IQR ≈ 1.35 × standard deviation.
''', [
 ('What is the interquartile range?', 'Q3 − Q1: the range of the middle 50% of the data.'),
 ('How do I find Q1?', 'Sort the data and find the median of the lower half. The calculator does this automatically.'),
], before='## Box plots')

expand('statistics/relative-risk', '''
## Interpreting relative risk

| RR | Meaning |
|---|---|
| 1 | No difference in risk |
| Above 1 | Higher risk in the exposed group |
| Below 1 | Lower risk in the exposed group (protective) |

An RR of 3 means the exposed group is three times as likely to have the outcome.

## Number needed to treat (NNT)

For treatments, the absolute risk difference converts into a practical number:

<p class="formula">NNT = 1 ÷ absolute risk reduction</p>

If a treatment cuts risk from 10% to 6%, the absolute reduction is 4%, so NNT = 25: on average, 25 people must be treated to prevent one event. For harms, the same calculation gives the number needed to harm (NNH).

## Relative vs absolute risk

A headline saying “risk doubled” (RR = 2) sounds alarming, but if the baseline risk is 1 in 10,000, it rises only to 2 in 10,000 — an absolute increase of 0.01%. Always look at both.

## Odds ratio vs relative risk

- **Cohort studies and trials**: use relative risk.
- **Case-control studies**: only the odds ratio can be calculated.
- When the outcome is rare (under about 10%), OR ≈ RR. When common, the OR exaggerates the effect.

## Confidence interval

The 95% CI for RR is usually calculated on the log scale: exp(ln RR ± 1.96 × SE), with SE = √(1/a − 1/(a+b) + 1/c − 1/(c+d)). If the interval includes 1, the difference may be due to chance.
''', [
 ('What is a relative risk of 0.5?', 'The exposed group has half the risk of the unexposed group — a 50% relative reduction.'),
 ('When is odds ratio close to relative risk?', 'When the outcome is rare, typically under about 10% in both groups.'),
])

expand('statistics/sample-size', '''
## Sample size for different confidence levels

Large population, p = 50%:

| Margin | 90% confidence | 95% confidence | 99% confidence |
|---|---|---|---|
''' + ''.join(f"| ±{e}% | {math.ceil(1.645**2*0.25/(e/100)**2):,} | {math.ceil(1.96**2*0.25/(e/100)**2):,} | {math.ceil(2.576**2*0.25/(e/100)**2):,} |\n" for e in [1, 2, 3, 4, 5, 10]) + '''
## Allow for non-response

If you expect only 40% of people to reply, divide the needed sample by 0.4. To get 385 completed surveys with a 40% response rate, invite about **963 people**.

## Sample size for a mean

When estimating a mean rather than a proportion:

<p class="formula">n = (z × σ ÷ E)²</p>

To estimate average weight within ±2 kg (σ ≈ 12 kg) at 95%: n = (1.96 × 12 ÷ 2)² = **139**.

## Subgroups

If you need results for subgroups (such as each region), each subgroup needs its own adequate sample. A national poll of 1,000 might have only 100 people in a small region, with a margin of about ±10%.

## Experiments and A/B tests

Comparing two groups needs a power calculation, which accounts for the smallest effect worth detecting and the chance of missing it (usually 80% power). Detecting a small difference needs a much larger sample than estimating a single proportion.
''', [
 ('Why is 385 a common sample size?', 'It gives a ±5% margin of error at 95% confidence for a large population with p = 50%.'),
 ('Does population size matter?', 'Only when the sample is a sizeable fraction of the population. Above about 20,000 people, the required sample barely changes.'),
], before='## Typical sample sizes (large population, 95%)')

expand('statistics/standard-deviation', '''
## Step-by-step example

Data: 4, 8, 6, 5, 7.

| x | x − mean (6) | (x − mean)² |
|---|---|---|
| 4 | −2 | 4 |
| 8 | 2 | 4 |
| 6 | 0 | 0 |
| 5 | −1 | 1 |
| 7 | 1 | 1 |
| | **Sum** | **10** |

- Sample variance = 10 ÷ (5 − 1) = 2.5, sample SD = **1.581**
- Population variance = 10 ÷ 5 = 2, population SD = **1.414**

## Sample or population?

- Use **sample** SD (n − 1) when your data are a sample from a larger group — the usual case.
- Use **population** SD (n) when you have every member of the group.

Dividing by n − 1 (Bessel's correction) makes the sample variance an unbiased estimate of the population variance.

## Standard deviation vs standard error

The SD describes the spread of individual values. The standard error (SD ÷ √n) describes how precisely the mean is estimated. See the [standard error calculator](/statistics/standard-error/).

## Units

The SD has the same units as the data; the variance has squared units. That is why SD is easier to interpret: “heights vary by about 7 cm” rather than “49 cm²”.
''', [
 ('What is a good standard deviation?', 'There is no universal value — it depends on the data. Compare it with the mean (see coefficient of variation) or with a target tolerance.'),
 ('Why divide by n − 1?', 'Because the mean is estimated from the same data, which makes deviations slightly smaller. Dividing by n − 1 corrects this bias.'),
], before='## In Excel')

expand('statistics/standard-error', '''
## Standard error shrinks with sample size

SD = 10:

| n | Standard error |
|---|---|
''' + ''.join(f"| {n} | {10/math.sqrt(n):.3f} |\n" for n in [4, 9, 16, 25, 100, 400, 1000]) + '''
To halve the standard error, you need **four times** the sample.

## Error bars in charts

| Error bar | Shows |
|---|---|
| ±1 SD | Spread of individual values |
| ±1 SE | Precision of the mean (about a 68% CI) |
| 95% CI (≈ ±2 SE) | Range likely to contain the true mean |

Always state which one a chart uses — SE bars look much smaller than SD bars.

## Standard error of a proportion

For percentages: SE = √(p × (1 − p) ÷ n). For 40% of 500 people, SE = √(0.4 × 0.6 ÷ 500) = **2.19%**.

## Standard error of a difference

For two independent means: SE<sub>diff</sub> = √(SE₁² + SE₂²). This is the basis of the two-sample t-test.

## From SE to confidence interval

95% CI ≈ mean ± 1.96 × SE for large samples. See the [confidence interval calculator](/statistics/confidence-interval/).
''', [
 ('What is the difference between standard deviation and standard error?', 'SD measures the spread of the data; SE measures how precisely the sample mean estimates the population mean.'),
 ('How do I reduce standard error?', 'Increase the sample size or reduce variability in measurements.'),
], before='## Sample size effect')

expand('statistics/sum-of-squares', '''
## Where sums of squares are used

| Use | How |
|---|---|
| Variance and SD | Variance = SS ÷ (n − 1) |
| Regression | Total SS = explained SS + residual SS |
| R² | R² = 1 − residual SS ÷ total SS |
| ANOVA | Splits total SS into between-group and within-group parts |
| Least squares | Fits the line that minimises residual SS |

## Two ways to compute

**Definition formula**: SS = Σ(x − x̄)². Clear and numerically stable.

**Computational formula**: SS = Σx² − (Σx)² ÷ n. Faster by hand, but can lose precision when values are large and close together.

Example with 2, 4, 6, 8: Σx = 20, Σx² = 120, so SS = 120 − 400 ÷ 4 = **20**. By definition: (−3)² + (−1)² + 1² + 3² = 20.

## Regression example

For a fitted line, the **residual sum of squares** adds up the squared vertical distances between the points and the line. A smaller residual SS relative to the total SS means a better fit (higher R²).

## Degrees of freedom

Each SS comes with degrees of freedom: n − 1 for total SS around the mean, n − 2 for residuals in simple linear regression. Mean squares (SS ÷ df) are what F-tests compare.
''', [
 ('What is the sum of squares used for?', 'It measures total variation around the mean and is the basis for variance, standard deviation, regression and ANOVA.'),
 ('How do I get variance from the sum of squares?', 'Divide by n − 1 for a sample or by n for a population.'),
])

expand('statistics/z-score', '''
## Z-score to percentile table

| z | Percentile | z | Percentile |
|---|---|---|---|
''' + ''.join(f"| {a:+.2f} | {Phi(a)*100:.1f}% | {b:+.2f} | {Phi(b)*100:.1f}% |\n" for a, b in zip([-2.33, -1.96, -1.645, -1.28, -1.0, -0.5], [0.5, 1.0, 1.28, 1.645, 1.96, 2.33])) + '''
## Comparing scores on different tests

Z-scores put different scales on a common footing:

| Test | Your score | Mean | SD | z |
|---|---|---|---|---|
| Maths | 78 | 65 | 10 | +1.30 |
| English | 85 | 80 | 4 | +1.25 |

Although the English score is higher, the maths result is slightly better relative to other students.

## Finding a raw score from z

x = μ + z × σ. To reach the 90th percentile (z = 1.28) on a test with mean 70 and SD 10, you need 70 + 12.8 = **82.8**.

## Z-scores in practice

- **Growth charts**: children's height and weight are reported as z-scores against WHO standards.
- **Bone density**: T-scores and Z-scores compare bone density with reference populations.
- **Quality control**: process measurements beyond ±3 are investigated.
- **Finance**: the Altman Z-score combines ratios to assess bankruptcy risk (a different formula with the same name).
''', [
 ('What does a negative z-score mean?', 'The value is below the mean. A z of −1 is one standard deviation below.'),
 ('What z-score is the top 5%?', 'About 1.645. Values above it are in the top 5% of a normal distribution.'),
], before='## Common z-scores')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/statistics/*.mdx')):
    c = 'statistics/' + os.path.basename(p)[:-4]; print(c, words(c))
