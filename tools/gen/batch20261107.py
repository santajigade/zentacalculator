import sys, math, os, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
from scipy import stats as SS
D = '2026-11-07'
pi = math.pi
DESC = []
def P(cat, slug, phrase, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    t = re.search(r'^intro: (.*)$', fm, re.M).group(1)
    assert phrase + ' calculator' in t.lower(), (slug, phrase)
    assert 'featured' not in fm
    DESC.append(slug)
    page(cat, slug, fm, body)

def p2t(t, df): return 2 * SS.t.sf(abs(t), df)
def pfmt(p): return f'{p:.4f}' if p >= 0.0001 else f'{p:.2e}'

# ======================================================================= STATISTICS

# ---------------------------------------------------------------- One-sample t-test
o_n, o_x, o_s, o_mu = 25, 103.2, 8.5, 100.0
o_se = o_s / math.sqrt(o_n); o_t = (o_x - o_mu) / o_se; o_df = o_n - 1
o_p2 = p2t(o_t, o_df); o_pR = SS.t.sf(o_t, o_df); o_pL = SS.t.cdf(o_t, o_df); o_d = (o_x - o_mu) / o_s
crit_rows = ''
for df in (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120):
    crit_rows += f"| {df} | {SS.t.ppf(0.95, df):.3f} | {SS.t.ppf(0.975, df):.3f} | {SS.t.ppf(0.995, df):.3f} |\n"
crit_rows += f"| ∞ (normal) | {SS.norm.ppf(0.95):.3f} | {SS.norm.ppf(0.975):.3f} | {SS.norm.ppf(0.995):.3f} |\n"
P('statistics', 'one-sample-t-test', 'one-sample t-test', f'''
title: One-Sample t-Test Calculator (t Statistic & p-Value)
description: Run a one-sample t-test from the sample mean, standard deviation and size — get the t statistic, degrees of freedom, p-values and effect size.
category: statistics
{intro("A one-sample t-test checks whether the mean of a sample differs from a hypothesised population mean when the population standard deviation is unknown. This one-sample t-test calculator turns the sample mean, standard deviation and sample size into the t statistic, degrees of freedom, two-tailed and one-tailed p-values and Cohen's d.")}
keywords: [one sample t test calculator, t test calculator, t statistic calculator, one sample t test p value, t test from mean and standard deviation, student t test, hypothesis test mean]
updated: {D}
variables:
  - {{ id: xbar, label: Sample mean x̄, default: {o_x:g} }}
  - {{ id: mu0, label: Hypothesised mean μ₀, default: {o_mu:g} }}
  - {{ id: s, label: Sample standard deviation s, default: {o_s:g}, min: 0 }}
  - {{ id: n, label: Sample size n, default: {o_n}, min: 2, decimals: 0 }}
  - {{ id: se, label: Standard error s/√n, min: 0, decimals: 4 }}
  - {{ id: t, label: t statistic, decimals: 4 }}
  - {{ id: df, label: Degrees of freedom, decimals: 0 }}
  - {{ id: p2, label: p-value (two-tailed) }}
  - {{ id: pR, label: p-value (right-tailed μ > μ₀) }}
  - {{ id: pL, label: p-value (left-tailed μ < μ₀) }}
  - {{ id: d, label: "Effect size (Cohen's d)", decimals: 3 }}
equations:
  - se = s / sqrt(n)
  - t = (xbar - mu0) / se
  - df = n - 1
  - p2 = 2 * (1 - tcdf(abs(t), df))
  - pR = 1 - tcdf(t, df)
  - pL = tcdf(t, df)
  - d = (xbar - mu0) / s
faq:
  - q: What is the formula for a one-sample t-test?
    a: t = (x̄ − μ₀) ÷ (s ÷ √n), with n − 1 degrees of freedom. The p-value is the probability of a t value at least this extreme if the true mean were μ₀.
  - q: When should I use a t-test instead of a z-test?
    a: Use the t-test when the population standard deviation is unknown and you estimate it from the sample — which is almost always. For large samples (n above about 30) the two give nearly the same answer.
  - q: What are the assumptions of a one-sample t-test?
    a: The observations are independent and come from a roughly normal population. The test is fairly robust to non-normality for n of 30 or more, but small samples with strong skew or outliers call for a non-parametric test such as the Wilcoxon signed-rank test.
  - q: Should I use the one-tailed or two-tailed p-value?
    a: Use the two-tailed p-value unless you decided before seeing the data that only one direction matters. A one-tailed p-value is half the two-tailed one when the effect is in the predicted direction.
related: [statistics/two-sample-t-test, statistics/p-value, statistics/standard-error, statistics/confidence-interval]
''', f'''
## How to use the one-sample t-test calculator

Enter the **sample mean**, the **hypothesised mean** μ₀ you are testing against, the **sample standard deviation** and the **sample size**. The calculator returns the standard error, the t statistic, the degrees of freedom and three p-values. Compare the p-value with your significance level α (usually 0.05): if p < α, reject the null hypothesis that the population mean equals μ₀. If you have raw data, get the mean and standard deviation first with the [standard deviation calculator](/statistics/standard-deviation/).

## One-sample t-test formula

<p class="formula">t = (x̄ − μ₀) ÷ (s / √n) &nbsp;·&nbsp; df = n − 1</p>

<p class="formula">p (two-tailed) = 2 × P(T<sub>df</sub> ≥ |t|) &nbsp;·&nbsp; Cohen's d = (x̄ − μ₀) ÷ s</p>

## Worked example

A filling machine should deliver 100 g. A sample of n = {o_n} packs has a mean of {o_x:g} g and a standard deviation of {o_s:g} g. Is the mean different from 100 g?

- Standard error = {o_s:g} ÷ √{o_n} = **{o_se:.4f} g**
- t = ({o_x:g} − {o_mu:g}) ÷ {o_se:.4f} = **{o_t:.4f}**, with **{o_df}** degrees of freedom
- Two-tailed p-value = **{o_p2:.4f}**; right-tailed p = **{o_pR:.4f}**
- Cohen's d = {o_x - o_mu:.1f} ÷ {o_s:g} = **{o_d:.3f}** (a small-to-medium effect)

At α = 0.05 the two-tailed test does **not** reject μ = 100 g (p = {o_p2:.3f} > 0.05), but a one-tailed test of "mean above 100 g" would (p = {o_pR:.3f}). This is why the direction must be chosen before looking at the data.

## Critical values of t

| df | one-tailed 0.05 / two-tailed 0.10 | two-tailed 0.05 | two-tailed 0.01 |
|---|---|---|---|
{crit_rows}
Reject the null hypothesis when |t| exceeds the critical value for your df and α. Values computed from the Student t distribution.

## Practical notes

- **Statistical vs practical significance** — with a large n even a tiny difference gives a small p-value. Report the effect size (Cohen's d ≈ 0.2 small, 0.5 medium, 0.8 large) and a [confidence interval](/statistics/confidence-interval/) alongside p.
- **Paired data** — for before/after measurements on the same items, compute the differences and run a one-sample t-test on them with μ₀ = 0. That is exactly a paired t-test.
- **Outliers** — one extreme value inflates s and can hide a real difference; check the data with a [box-plot or quartiles](/statistics/quartiles/) first.
''')

# ---------------------------------------------------------------- Two-sample t-test (Welch / pooled)
w1n, w1x, w1s = 30, 78.4, 6.2
w2n, w2x, w2s = 25, 74.1, 8.9
def two(pool, x1, s1, n1, x2, s2, n2):
    if pool:
        sp2 = ((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2)
        se = math.sqrt(sp2 * (1/n1 + 1/n2)); df = n1 + n2 - 2
    else:
        a, b = s1**2 / n1, s2**2 / n2
        se = math.sqrt(a + b); df = (a + b)**2 / (a**2 / (n1 - 1) + b**2 / (n2 - 1))
    t = (x1 - x2) / se
    return se, df, t, p2t(t, df), SS.t.sf(t, df), SS.t.cdf(t, df)
wse, wdf, wt, wp2, wpR, wpL = two(0, w1x, w1s, w1n, w2x, w2s, w2n)
pse, pdf_, pt, pp2, ppR, ppL = two(1, w1x, w1s, w1n, w2x, w2s, w2n)
cmp_rows = ''
for nm, r in (('Welch (unequal variances)', (wse, wdf, wt, wp2)), ('Pooled (equal variances)', (pse, pdf_, pt, pp2))):
    cmp_rows += f"| {nm} | {r[0]:.4f} | {r[1]:.2f} | {r[2]:.4f} | {r[3]:.4f} |\n"
ss_rows = ''
for nn in (5, 10, 20, 30, 50, 100):
    se_, df_, t_, p_, _, _ = two(0, w1x, w1s, nn, w2x, w2s, nn)
    ss_rows += f"| {nn} | {nn} | {t_:.3f} | {df_:.1f} | {pfmt(p_)} |\n"
P('statistics', 'two-sample-t-test', 'two-sample t-test', f'''
title: Two-Sample t-Test Calculator (Welch & Pooled)
description: Compare two means with a two-sample t-test from summary statistics — Welch or pooled — and get the t statistic, degrees of freedom and p-values.
category: statistics
{intro("A two-sample t-test asks whether two independent groups have different population means, using each group's mean, standard deviation and size. This two-sample t-test calculator runs Welch's unequal-variance test by default, or the classic pooled Student's t-test, and returns the t statistic, degrees of freedom and two-tailed and one-tailed p-values.")}
keywords: [two sample t test calculator, independent t test calculator, welch t test calculator, pooled t test, compare two means, t test from summary statistics, unequal variance t test]
updated: {D}
variables:
  - id: pool
    label: Test
    default: 0
    options:
      - {{ label: "Welch's t-test (unequal variances)", value: 0 }}
      - {{ label: "Student's pooled t-test (equal variances)", value: 1 }}
  - {{ id: x1, label: Mean of group 1, default: {w1x:g} }}
  - {{ id: s1, label: Standard deviation of group 1, default: {w1s:g}, min: 0 }}
  - {{ id: n1, label: Size of group 1, default: {w1n}, min: 2, decimals: 0 }}
  - {{ id: x2, label: Mean of group 2, default: {w2x:g} }}
  - {{ id: s2, label: Standard deviation of group 2, default: {w2s:g}, min: 0 }}
  - {{ id: n2, label: Size of group 2, default: {w2n}, min: 2, decimals: 0 }}
  - {{ id: dm, label: Difference in means x̄₁ − x̄₂, decimals: 4 }}
  - {{ id: se, label: Standard error of the difference, min: 0, decimals: 4 }}
  - {{ id: df, label: Degrees of freedom, decimals: 2 }}
  - {{ id: t, label: t statistic, decimals: 4 }}
  - {{ id: p2, label: p-value (two-tailed) }}
  - {{ id: pR, label: p-value (right-tailed μ₁ > μ₂) }}
  - {{ id: pL, label: p-value (left-tailed μ₁ < μ₂) }}
equations:
  - dm = x1 - x2
  - se = (1 - pool) * sqrt(s1^2 / n1 + s2^2 / n2) + pool * sqrt(((n1 - 1) * s1^2 + (n2 - 1) * s2^2) / (n1 + n2 - 2) * (1 / n1 + 1 / n2))
  - df = (1 - pool) * (s1^2 / n1 + s2^2 / n2)^2 / ((s1^2 / n1)^2 / (n1 - 1) + (s2^2 / n2)^2 / (n2 - 1)) + pool * (n1 + n2 - 2)
  - t = dm / se
  - p2 = 2 * (1 - tcdf(abs(t), df))
  - pR = 1 - tcdf(t, df)
  - pL = tcdf(t, df)
faq:
  - q: Should I use Welch's t-test or the pooled t-test?
    a: Welch's test is the safer default. It does not assume equal variances, loses almost no power when the variances are equal, and avoids misleading p-values when they are not — especially with unequal group sizes. Use the pooled test only when equal variances are justified.
  - q: How are the Welch degrees of freedom calculated?
    a: With the Welch–Satterthwaite equation, df = (s₁²/n₁ + s₂²/n₂)² ÷ [(s₁²/n₁)²/(n₁ − 1) + (s₂²/n₂)²/(n₂ − 1)]. It is usually not a whole number and lies between the smaller n − 1 and n₁ + n₂ − 2.
  - q: Can I use this for before-and-after measurements?
    a: No. Measurements on the same subjects are paired, not independent. Take the difference for each subject and use the one-sample t-test on the differences with a hypothesised mean of 0.
  - q: What does the p-value mean here?
    a: It is the probability of seeing a difference in means at least as large as yours if the two population means were actually equal. It is not the probability that the null hypothesis is true.
related: [statistics/one-sample-t-test, statistics/p-value, statistics/standard-error, statistics/sample-size]
''', f'''
## How to use the two-sample t-test calculator

Choose **Welch** or **pooled**, then enter the mean, standard deviation and size of each group. The calculator returns the difference in means, its standard error, the degrees of freedom, the t statistic and the p-values. If p is below your significance level α (commonly 0.05), the difference between the group means is statistically significant.

## Two-sample t-test formulas

<p class="formula">Welch: t = (x̄₁ − x̄₂) ÷ √(s₁²/n₁ + s₂²/n₂)</p>

<p class="formula">df = (s₁²/n₁ + s₂²/n₂)² ÷ [ (s₁²/n₁)²/(n₁−1) + (s₂²/n₂)²/(n₂−1) ]</p>

<p class="formula">Pooled: s<sub>p</sub>² = [(n₁−1)s₁² + (n₂−1)s₂²] ÷ (n₁+n₂−2) &nbsp;·&nbsp; t = (x̄₁ − x̄₂) ÷ √(s<sub>p</sub>²(1/n₁ + 1/n₂)) &nbsp;·&nbsp; df = n₁+n₂−2</p>

## Worked example

Group 1: n = {w1n}, mean {w1x:g}, SD {w1s:g}. Group 2: n = {w2n}, mean {w2x:g}, SD {w2s:g}. Welch's test:

- Difference in means = {w1x:g} − {w2x:g} = **{w1x - w2x:.1f}**
- Standard error = √({w1s:g}²/{w1n} + {w2s:g}²/{w2n}) = **{wse:.4f}**
- t = {w1x - w2x:.1f} ÷ {wse:.4f} = **{wt:.4f}**, df = **{wdf:.2f}**
- Two-tailed p-value = **{wp2:.4f}**, so the difference is significant at α = 0.05

## Welch vs pooled for the same data

| Method | SE | df | t | p (two-tailed) |
|---|---|---|---|---|
{cmp_rows}
Here group 2 has the larger SD but the smaller n, so the pooled test understates the standard error and gives a smaller p-value than Welch's test.

## Effect of sample size (same means and SDs as the example)

| n₁ | n₂ | t | Welch df | p (two-tailed) |
|---|---|---|---|---|
{ss_rows}
The same 4.3-point difference is not significant with 5 per group but highly significant with 100 per group — plan the [sample size](/statistics/sample-size/) before collecting data.

## Practical notes

- Groups must be **independent** — different people, batches or machines in each.
- Each group should be roughly normal, or large enough (about 30+) for the central limit theorem to help.
- For more than two groups use ANOVA rather than repeated t-tests, which inflate the false-positive rate.
''')

# ---------------------------------------------------------------- p-value from z or t
pv_x, pv_df = 1.96, 20
pz2 = 2 * SS.norm.sf(pv_x); pzR = SS.norm.sf(pv_x)
pt2_ = p2t(pv_x, pv_df)
z_rows = ''
for z in (1.0, 1.282, 1.645, 1.96, 2.0, 2.326, 2.576, 3.0, 3.291, 4.0):
    z_rows += f"| {z:g} | {pfmt(SS.norm.sf(z))} | {pfmt(2*SS.norm.sf(z))} |\n"
tdf_rows = ''
for df in (2, 5, 10, 20, 30, 60, 120):
    tdf_rows += f"| {df} | {pfmt(p2t(2.0, df))} | {pfmt(p2t(2.5, df))} | {pfmt(p2t(3.0, df))} |\n"
tdf_rows += f"| ∞ (z) | {pfmt(2*SS.norm.sf(2.0))} | {pfmt(2*SS.norm.sf(2.5))} | {pfmt(2*SS.norm.sf(3.0))} |\n"
P('statistics', 'p-value', 'p-value', f'''
title: P-Value Calculator (from z-Score or t-Score)
description: Convert a z-score or t-score into a p-value — two-tailed, left-tailed and right-tailed — using the normal or Student t distribution with any df.
category: statistics
{intro("A p-value is the probability of getting a test statistic at least as extreme as the one observed if the null hypothesis were true. This p-value calculator converts a z-score (normal distribution) or a t-score with its degrees of freedom (Student t distribution) into two-tailed, left-tailed and right-tailed p-values.")}
keywords: [p value calculator, p value from z score, p value from t score, z score to p value, t score to p value, two tailed p value, one tailed p value]
updated: {D}
variables:
  - id: dist
    label: Distribution of the test statistic
    default: 0
    options:
      - {{ label: Standard normal (z-score), value: 0 }}
      - {{ label: Student t (t-score), value: 1 }}
  - {{ id: x, label: Test statistic (z or t), default: {pv_x:g} }}
  - {{ id: df, label: Degrees of freedom (t only), default: {pv_df}, min: 0.000001 }}
  - {{ id: p2, label: p-value (two-tailed) }}
  - {{ id: pL, label: p-value (left-tailed) }}
  - {{ id: pR, label: p-value (right-tailed) }}
equations:
  - pL = (1 - dist) * normcdf(x) + dist * tcdf(x, df)
  - pR = 1 - pL
  - p2 = 2 * min(pL, pR)
faq:
  - q: How do I get a p-value from a z-score?
    a: For a right-tailed test p = 1 − Φ(z), for a left-tailed test p = Φ(z), and for a two-tailed test p = 2 × (1 − Φ(|z|)), where Φ is the standard normal cumulative distribution. z = 1.96 gives a two-tailed p of 0.05.
  - q: Why does the t distribution give a bigger p-value?
    a: The t distribution has heavier tails than the normal, reflecting the extra uncertainty of estimating the standard deviation from the sample. As degrees of freedom grow, t approaches the normal distribution.
  - q: What is a significant p-value?
    a: By convention p < 0.05, but the threshold α should be chosen before the test. Fields such as particle physics use far stricter thresholds (5σ, about p < 3×10⁻⁷).
  - q: Is the p-value the probability that the null hypothesis is true?
    a: No. It is the probability of data this extreme assuming the null hypothesis is true. A small p-value says the data are surprising under the null, not how likely the null is.
related: [statistics/z-score, statistics/one-sample-t-test, statistics/two-sample-t-test, statistics/normal-distribution]
''', f'''
## How to use the p-value calculator

Choose the **distribution** of your test statistic — standard normal for a z-test, Student t for a t-test — then enter the **statistic** and, for t, its **degrees of freedom**. The calculator returns the two-tailed, left-tailed and right-tailed p-values. Use the two-tailed value when the alternative hypothesis is "not equal", the right-tailed value for "greater than" and the left-tailed value for "less than".

## P-value formulas

<p class="formula">left-tailed p = F(x) &nbsp;·&nbsp; right-tailed p = 1 − F(x) &nbsp;·&nbsp; two-tailed p = 2 × min(F(x), 1 − F(x))</p>

F is the cumulative distribution function of the standard normal (Φ) or of Student's t with df degrees of freedom.

## Worked example

A z-test gives z = {pv_x:g}:

- Right-tailed p = 1 − Φ({pv_x:g}) = **{pzR:.4f}**
- Two-tailed p = 2 × {pzR:.4f} = **{pz2:.4f}** — right on the 5% threshold

If the same value were a t-score with {pv_df} degrees of freedom, the two-tailed p-value would be **{pt2_:.4f}** — not significant at 5%, because the t distribution has heavier tails.

## z-score to p-value table

| z | one-tailed p | two-tailed p |
|---|---|---|
{z_rows}
## Two-tailed p-value for a t-score by degrees of freedom

| df | t = 2.0 | t = 2.5 | t = 3.0 |
|---|---|---|---|
{tdf_rows}
## Practical notes

- Report the exact p-value (for example p = 0.031) rather than just "p < 0.05".
- A two-tailed p-value is twice the smaller one-tailed value — never halve it after seeing which way the result went.
- Running many tests inflates false positives; with m tests a Bonferroni correction compares each p-value with α ÷ m.
''')

# ======================================================================= MATH

# ---------------------------------------------------------------- Hemisphere
hr = 5.0
hV = 2/3 * pi * hr**3; hC = 2 * pi * hr**2; hB = pi * hr**2; hT = 3 * pi * hr**2
he_rows = ''
for r in (1, 2, 5, 10, 15, 20, 30, 50):
    V = 2/3 * pi * r**3
    he_rows += f"| {r} cm | {V:,.2f} cm³ | {V/1000:,.4g} L | {2*pi*r*r:,.2f} cm² | {3*pi*r*r:,.2f} cm² |\n"
P('math', 'hemisphere', 'hemisphere volume', f'''
title: Hemisphere Volume Calculator (Surface Area & Radius)
description: Calculate the volume, curved surface area, base area and total surface area of a hemisphere from its radius or diameter — or find the radius from a volume.
category: math
{intro("A hemisphere is exactly half of a sphere, cut through its centre — the shape of a bowl, a dome or a tank head. This hemisphere volume calculator gives the volume, curved surface area, flat base area and total surface area from the radius, and works backwards from any of them to the radius.")}
keywords: [hemisphere volume calculator, volume of a hemisphere, hemisphere surface area, curved surface area of hemisphere, total surface area hemisphere, dome volume calculator, bowl volume]
updated: {D}
variables:
  - {{ id: r, label: Radius, family: length, unit: cm, imperialUnit: in, default: {hr:g}, min: 0 }}
  - {{ id: d, label: Diameter, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: cm3, imperialUnit: in3, min: 0 }}
  - {{ id: Ac, label: Curved surface area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
  - {{ id: Ab, label: Base (circle) area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
  - {{ id: At, label: Total surface area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
equations:
  - d = 2 * r
  - V = 2 / 3 * pi * r^3
  - Ac = 2 * pi * r^2
  - Ab = pi * r^2
  - At = 3 * pi * r^2
faq:
  - q: What is the formula for the volume of a hemisphere?
    a: V = (2/3)πr³ — half the volume of a sphere of the same radius. A hemisphere with a 5 cm radius holds about 261.8 cm³.
  - q: What is the total surface area of a hemisphere?
    a: 3πr². It is the curved surface 2πr² (half of a sphere's 4πr²) plus the flat circular base πr².
  - q: How do I find the radius from the volume?
    a: r = ∛(3V ÷ 2π). Enter the volume in the calculator and it solves for the radius.
  - q: How much does a hemispherical bowl hold?
    a: Use the inner radius. A bowl with a 10 cm inner radius holds 2,094 cm³, about 2.1 litres, when filled to the brim.
related: [math/sphere, math/cylinder-volume, math/cone, math/capsule]
''', f'''
## How to use the hemisphere volume calculator

Enter the **radius** (or the diameter) and choose your units. The calculator returns the volume, the curved surface area, the flat base area and the total surface area. To go backwards — for example the radius of a dome that encloses a given volume — enter the known value and leave the radius blank.

## Hemisphere formulas

<p class="formula">V = ⅔ π r³ &nbsp;·&nbsp; curved area = 2π r² &nbsp;·&nbsp; base = π r² &nbsp;·&nbsp; total area = 3π r²</p>

<p class="formula">r = ∛(3V ÷ 2π)</p>

## Worked example

A hemisphere with radius r = {hr:g} cm:

- Volume = ⅔ × π × {hr:g}³ = **{hV:.2f} cm³** ({hV/1000:.4f} L)
- Curved surface area = 2 × π × {hr:g}² = **{hC:.2f} cm²**
- Base area = π × {hr:g}² = **{hB:.2f} cm²**
- Total surface area = 3 × π × {hr:g}² = **{hT:.2f} cm²**

## Hemisphere volume and area table

| Radius | Volume | Litres | Curved area | Total area |
|---|---|---|---|---|
{he_rows}
## Practical notes

- **Domes and roofs** — paint or cladding covers only the curved area 2πr²; the base is the floor.
- **Tank heads** — a hemispherical head adds ⅔πr³ to a cylindrical tank; two heads add a full sphere. See the [capsule calculator](/math/capsule/) for a cylinder with two hemispherical ends.
- **Partly filled bowls** — the liquid forms a spherical cap of height h with volume πh²(3r − h)/3; at h = r this equals the hemisphere volume.
''')

# ---------------------------------------------------------------- Capsule
cr, ca = 3.0, 10.0
cV = pi * cr**2 * ca + 4/3 * pi * cr**3; cS = 2 * pi * cr * (2 * cr + ca); cL = ca + 2 * cr
cap_rows = ''
for r, a in ((1, 0), (1, 2), (2, 5), (3, 10), (5, 20), (10, 30), (25, 100), (50, 200)):
    V = pi * r * r * a + 4/3 * pi * r**3; S = 2 * pi * r * (2*r + a)
    cap_rows += f"| {r:g} cm | {a:g} cm | {a+2*r:g} cm | {V:,.2f} cm³ | {V/1000:,.4g} L | {S:,.2f} cm² |\n"
P('math', 'capsule', 'capsule volume', f'''
title: Capsule Volume Calculator (Cylinder with Hemisphere Ends)
description: Calculate the volume, surface area and overall length of a capsule (stadium of revolution) — a cylinder with two hemispherical ends — from radius and length.
category: math
{intro("A capsule is a cylinder capped with a hemisphere at each end — the shape of a medicine capsule, a propane bullet tank or a pressure vessel with hemispherical heads. This capsule volume calculator gives the volume, surface area and overall length from the radius and the length of the straight cylindrical section.")}
keywords: [capsule volume calculator, volume of a capsule, capsule surface area, cylinder with hemispherical ends volume, pill shape volume, tank with hemispherical heads volume, stadium of revolution]
updated: {D}
variables:
  - {{ id: r, label: Radius, family: length, unit: cm, imperialUnit: in, default: {cr:g}, min: 0 }}
  - {{ id: a, label: Length of cylindrical section, family: length, unit: cm, imperialUnit: in, default: {ca:g}, min: 0 }}
  - {{ id: L, label: Overall length a + 2r, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: cm3, imperialUnit: in3, min: 0 }}
  - {{ id: S, label: Surface area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
equations:
  - L = a + 2 * r
  - V = pi * r^2 * a + 4 / 3 * pi * r^3
  - S = 2 * pi * r * (2 * r + a)
faq:
  - q: What is the formula for the volume of a capsule?
    a: V = πr²a + (4/3)πr³ — a cylinder of radius r and length a plus one full sphere made by the two hemispherical ends.
  - q: What is the surface area of a capsule?
    a: S = 2πr(2r + a) = 4πr² + 2πra — the sphere's surface plus the side of the cylinder. The flat circles of the cylinder are hidden inside the joints.
  - q: What length should I measure?
    a: The calculator needs the straight cylindrical length a. If you measured the overall tip-to-tip length L, use a = L − 2r, or enter L and the radius and let it solve for a.
  - q: Does this work for tanks with dished (torispherical) heads?
    a: No — dished heads hold much less than hemispherical ones. Use this only for true hemispherical heads; for flat-ended tanks use the cylinder volume calculator.
related: [math/hemisphere, math/cylinder-volume, math/sphere, engineering/horizontal-tank-volume]
''', f'''
## How to use the capsule volume calculator

Enter the **radius** of the capsule and the **length of the straight cylindrical part** between the two hemispherical ends. The calculator returns the overall length, the volume and the surface area. If you know the overall length instead, enter it with the radius and leave the cylinder length blank.

## Capsule formulas

<p class="formula">V = π r² a + ⁴⁄₃ π r³ &nbsp;·&nbsp; S = 2π r (2r + a) &nbsp;·&nbsp; L = a + 2r</p>

## Worked example

r = {cr:g} cm, cylindrical length a = {ca:g} cm:

- Cylinder part = π × {cr:g}² × {ca:g} = {pi*cr*cr*ca:.2f} cm³
- Two hemispheres = ⁴⁄₃ × π × {cr:g}³ = {4/3*pi*cr**3:.2f} cm³
- Volume = **{cV:.2f} cm³** ({cV/1000:.4f} L)
- Surface area = 2π × {cr:g} × (2 × {cr:g} + {ca:g}) = **{cS:.2f} cm²**
- Overall length = **{cL:g} cm**

## Capsule volume table

| Radius r | Cylinder length a | Overall length | Volume | Litres | Surface area |
|---|---|---|---|---|---|
{cap_rows}
The first row (a = 0) is a sphere of radius 1 cm.

## Practical notes

- Pressure vessels use hemispherical heads because they need only about half the wall thickness of the cylindrical shell for the same pressure.
- For a horizontal capsule tank that is partly full, the liquid volume is not proportional to depth — use the [horizontal tank volume calculator](/engineering/horizontal-tank-volume/) for the cylindrical part.
- With a = 0 the capsule becomes a [sphere](/math/sphere/).
''')

# ---------------------------------------------------------------- Angle converter
ag = 52.3725
ar = ag * pi / 180
dd = math.floor(ag); mm = math.floor((ag - dd) * 60); sc = ((ag - dd) * 60 - mm) * 60
ang_rows = ''
for dgr, frac in ((0, '0'), (30, 'π/6'), (45, 'π/4'), (60, 'π/3'), (90, 'π/2'), (120, '2π/3'), (135, '3π/4'), (180, 'π'), (270, '3π/2'), (360, '2π')):
    ang_rows += f"| {dgr}° | {frac} | {dgr*pi/180:.6f} | {dgr*10/9:g} | {dgr/360:g} | {dgr*6400/360:g} |\n"
P('math', 'angle-converter', 'angle converter', f'''
title: Angle Converter (Degrees, Radians, Gradians & DMS)
description: Convert angles between degrees, radians, gradians, turns, arcminutes, arcseconds, milliradians and mils, and split decimal degrees into degrees-minutes-seconds.
category: math
{intro("Angles are measured in degrees in everyday work, in radians in mathematics and physics, in gradians on some surveying instruments and in degrees–minutes–seconds for map coordinates. This angle converter calculator converts between all of them at once and splits decimal degrees into degrees, minutes and seconds.")}
keywords: [angle converter, degrees to radians, radians to degrees, degrees to gradians, decimal degrees to dms, degrees minutes seconds converter, arcseconds to degrees, mrad to degrees]
updated: {D}
variables:
  - {{ id: deg, label: Degrees, suffix: °, default: {ag:g} }}
  - {{ id: rad, label: Radians, suffix: rad }}
  - {{ id: pirad, label: Multiples of π radians, suffix: × π rad }}
  - {{ id: grad, label: Gradians (gon), suffix: grad }}
  - {{ id: turn, label: Turns (revolutions), suffix: turns }}
  - {{ id: amin, label: Arcminutes, suffix: "′" }}
  - {{ id: asec, label: Arcseconds, suffix: "″" }}
  - {{ id: mrad, label: Milliradians, suffix: mrad }}
  - {{ id: mil, label: NATO mils (6400 per turn), suffix: mil }}
  - {{ id: D, label: DMS — whole degrees, suffix: °, decimals: 0 }}
  - {{ id: M, label: DMS — minutes, suffix: "′", decimals: 0 }}
  - {{ id: S, label: DMS — seconds, suffix: "″", decimals: 2 }}
equations:
  - rad = deg * pi / 180
  - pirad = deg / 180
  - grad = deg * 10 / 9
  - turn = deg / 360
  - amin = deg * 60
  - asec = deg * 3600
  - mrad = rad * 1000
  - mil = deg * 6400 / 360
  - D = floor(deg)
  - M = floor((deg - D) * 60)
  - S = ((deg - D) * 60 - M) * 60
faq:
  - q: How do I convert degrees to radians?
    a: Multiply by π/180. For example 90° × π/180 = π/2 ≈ 1.5708 rad. To convert radians to degrees, multiply by 180/π ≈ 57.2958.
  - q: How do I convert decimal degrees to degrees, minutes and seconds?
    a: The whole number is the degrees. Multiply the decimal part by 60 — the whole number is the minutes. Multiply the remaining decimal by 60 again for the seconds. 52.3725° = 52° 22′ 21″.
  - q: What is a gradian?
    a: A gradian (gon) is 1/400 of a turn, so a right angle is exactly 100 grad. It is used in surveying in some European countries. Check that a calculator is not in GRAD mode by mistake.
  - q: What is the difference between a milliradian and a mil?
    a: A milliradian is exactly 1/1000 rad, so a full turn is about 6283.2 mrad. The NATO mil rounds this to 6400 per turn so that it divides evenly. Both are used for sights and rangefinding, where 1 mrad subtends about 1 m at 1 km.
related: [math/right-triangle-trig, math/arc-length, physics/angular-velocity, math/circle]
''', f'''
## How to use the angle converter

Type an angle into **any** field — degrees, radians, gradians, turns, arcminutes, arcseconds, milliradians or mils — and all the others update. The last three fields split the angle into **degrees, minutes and seconds** (DMS), the format used for latitude and longitude. For a negative angle, convert its absolute value to DMS and put the minus sign in front.

## Angle conversion formulas

<p class="formula">rad = deg × π/180 &nbsp;·&nbsp; grad = deg × 10/9 &nbsp;·&nbsp; turns = deg/360 &nbsp;·&nbsp; ′ = deg × 60 &nbsp;·&nbsp; ″ = deg × 3600</p>

<p class="formula">DMS: D = ⌊deg⌋ &nbsp;·&nbsp; M = ⌊(deg − D) × 60⌋ &nbsp;·&nbsp; S = ((deg − D) × 60 − M) × 60</p>

## Worked example

Convert a latitude of {ag:g}°:

- Radians = {ag:g} × π/180 = **{ar:.6f} rad** ({ag/180:.6f} π rad)
- Gradians = {ag:g} × 10/9 = **{ag*10/9:.4f} grad**
- Milliradians = **{ar*1000:.4f} mrad**
- DMS: 0.3725 × 60 = 22.35′ → **22′**; 0.35 × 60 = **21″** → **{dd}° {mm}′ {sc:.0f}″**

## Common angles

| Degrees | Radians (π) | Radians | Gradians | Turns | NATO mils |
|---|---|---|---|---|---|
{ang_rows}
## Practical notes

- Spreadsheet and programming trig functions (SIN, COS, Math.sin) expect **radians** — convert with RADIANS() or × π/180 first.
- One arcsecond of latitude is about 30.9 m on the ground; 0.0001° is about 11 m.
- Small-angle rule: for angles under about 10°, sin θ ≈ tan θ ≈ θ in radians — so 1 mrad ≈ 1 m at 1 km.
''')

# ---------------------------------------------------------------- Scientific notation
sx = 45600000.0
sex = math.floor(math.log10(abs(sx))); sm = sx / 10**sex; see = 3 * math.floor(sex / 3); sme = sx / 10**see
SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')
def sci(x):
    e = math.floor(math.log10(abs(x))); m = x / 10**e
    ee = 3 * math.floor(e / 3); me = x / 10**ee
    return f'{m:.10g} × 10{str(e).translate(SUP)}', f'{m:.10g}e{e}', f'{me:.10g} × 10{str(ee).translate(SUP)}'
sci_rows = ''
for nm, x in (('Speed of light (m/s)', 299792458), ('Avogadro constant (1/mol)', 6.02214076e23), ('Earth–Sun distance (m)', 1.496e11), ('Elementary charge (C)', 1.602176634e-19), ('1 µF in farads', 1e-6), ('Hydrogen atom radius (m)', 5.29e-11), ('World population (approx.)', 8.1e9), ('0.00045', 0.00045)):
    a_, b_, c_ = sci(x); sci_rows += f"| {nm} | {a_} | {b_} | {c_} |\n"
P('math', 'scientific-notation', 'scientific notation', f'''
title: Scientific Notation Calculator (Standard & Engineering Form)
description: Convert any number to scientific notation (a × 10ⁿ) and engineering notation (exponent a multiple of 3), and back to decimal — with coefficient and exponent.
category: math
{intro("Scientific notation writes a number as a coefficient between 1 and 10 multiplied by a power of ten, so 45,600,000 becomes 4.56 × 10⁷. This scientific notation calculator splits any number into its coefficient and exponent, gives the engineering-notation form whose exponent is a multiple of three, and converts back to an ordinary decimal.")}
keywords: [scientific notation calculator, convert to scientific notation, standard form calculator, engineering notation calculator, e notation, powers of 10, decimal to scientific notation]
updated: {D}
variables:
  - {{ id: x, label: Number (decimal form), default: {sx:g} }}
  - {{ id: ex, label: Exponent n (scientific), decimals: 0 }}
  - {{ id: m, label: Coefficient a (1 ≤ |a| < 10) }}
  - {{ id: ee, label: Exponent (engineering — multiple of 3), decimals: 0 }}
  - {{ id: me, label: Coefficient (engineering — 1 to 999) }}
equations:
  - ex = floor(log10(abs(x)))
  - m = x / 10^ex
  - ee = 3 * floor(ex / 3)
  - me = x / 10^ee
faq:
  - q: How do I write a number in scientific notation?
    a: Move the decimal point until one non-zero digit is left of it; the number of places moved is the exponent — positive if you moved left, negative if you moved right. 0.00045 becomes 4.5 × 10⁻⁴.
  - q: What is engineering notation?
    a: Like scientific notation, but the exponent is always a multiple of 3 so it matches SI prefixes — 45.6 × 10⁶ is 45.6 mega. The coefficient is between 1 and 999.
  - q: What does 4.56E7 mean on a calculator?
    a: E notation is scientific notation for screens and spreadsheets — 4.56E7 means 4.56 × 10⁷ = 45,600,000. A negative exponent such as 2E-3 means 0.002.
  - q: How do I multiply numbers in scientific notation?
    a: Multiply the coefficients and add the exponents, then renormalise. (3 × 10⁴) × (5 × 10³) = 15 × 10⁷ = 1.5 × 10⁸.
related: [math/exponent, math/logarithm, conversion/number-to-million, math/square-root]
''', f'''
## How to use the scientific notation calculator

Enter a **number** in ordinary decimal form (you can also type E notation such as 6.02e23). The calculator returns the **exponent** and **coefficient** of its scientific notation and the matching **engineering notation**. To convert back, enter a coefficient and exponent and the decimal number is filled in.

## Scientific notation formula

<p class="formula">x = a × 10ⁿ &nbsp;with&nbsp; n = ⌊log₁₀|x|⌋ &nbsp;and&nbsp; a = x ÷ 10ⁿ</p>

<p class="formula">Engineering: n<sub>eng</sub> = 3 × ⌊n ÷ 3⌋ &nbsp;·&nbsp; a<sub>eng</sub> = x ÷ 10<sup>n<sub>eng</sub></sup></p>

## Worked example

Convert {sx:,.0f}:

- log₁₀({sx:,.0f}) = {math.log10(sx):.4f}, so the exponent is **{sex}**
- Coefficient = {sx:,.0f} ÷ 10⁷ = **{sm:g}** → **{sm:g} × 10⁷** (E notation {sm:g}E7)
- Engineering exponent = 3 × ⌊7 ÷ 3⌋ = **{see}**, coefficient **{sme:g}** → {sme:g} × 10⁶ = {sme:g} mega

For a small number, 0.00045 → log₁₀ = −3.35, exponent **−4**, coefficient **4.5** → 4.5 × 10⁻⁴ (engineering 450 × 10⁻⁶ = 450 micro).

## Examples in scientific and engineering notation

| Quantity | Scientific | E notation | Engineering |
|---|---|---|---|
{sci_rows}
## Practical notes

- Zero has no scientific-notation exponent; it is written simply as 0.
- **Significant figures** are the digits in the coefficient: 4.560 × 10⁷ states four, 4.56 × 10⁷ three.
- Engineering exponents map to SI prefixes: 10³ kilo, 10⁶ mega, 10⁹ giga, 10⁻³ milli, 10⁻⁶ micro, 10⁻⁹ nano, 10⁻¹² pico.
''')

# ======================================================================= ELECTRONICS

# ---------------------------------------------------------------- Inverting buck-boost converter
bVi, bVo, bIo, beta, bf, br, bdV = 12.0, 12.0, 0.5, 0.85, 500e3, 0.30, 0.05
bD = bVo / (bVi * beta + bVo); bIi = bVo * bIo / (bVi * beta); bIL = bIo / (1 - bD)
bL = bVi * bD / (bf * br * bIL); bIpk = bIL * (1 + br / 2); bC = bIo * bD / (bf * bdV); bVsw = bVi + bVo
bb_rows = ''
for vo in (3.3, 5, 9, 12, 15, 24):
    Dd = vo / (bVi * beta + vo); IL = bIo / (1 - Dd)
    bb_rows += f"| −{vo:g} V | {Dd*100:.1f}% | {IL:.3f} A | {bVi*Dd/(bf*br*IL)*1e6:.1f} µH | {bVi+vo:g} V |\n"
P('electronics', 'buck-boost-converter', 'buck-boost converter', f'''
title: Buck-Boost Converter Calculator (Inverting, L & C)
description: Calculate duty cycle, inductor current, inductance, peak switch current, switch voltage and output capacitance for an inverting buck-boost DC-DC converter.
category: electronics
{intro("An inverting buck-boost converter makes a negative output voltage that can be larger or smaller in magnitude than the input — for example −12 V from a +12 V rail for an op-amp or LCD bias. This buck-boost converter calculator gives the duty cycle, average and peak inductor current, required inductance, switch voltage stress and minimum output capacitance; for a positive output use the related [SEPIC converter](ib:sepic-converter-working-design).")}
keywords: [buck boost converter calculator, inverting buck boost calculator, buck boost duty cycle, buck boost inductor calculation, negative voltage converter design, buck boost formula, dc dc converter calculator]
updated: {D}
variables:
  - {{ id: Vi, label: Input voltage, family: voltage, unit: V, default: {bVi:g}, min: 0 }}
  - {{ id: Vo, label: Output voltage magnitude |Vout|, family: voltage, unit: V, default: {bVo:g}, min: 0 }}
  - {{ id: Io, label: Output current, family: current, unit: A, default: {bIo:g}, min: 0 }}
  - {{ id: eta, label: Efficiency, family: percent, unit: '%', default: {beta*100:g}, min: 0.01, max: 1 }}
  - {{ id: f, label: Switching frequency, family: frequency, unit: kHz, default: {bf/1e3:g}, min: 0 }}
  - {{ id: r, label: Inductor ripple (of inductor current), family: percent, unit: '%', default: {br*100:g}, min: 0.01 }}
  - {{ id: dV, label: Allowed output ripple, family: voltage, unit: mV, default: {bdV*1e3:g}, min: 0 }}
  - {{ id: D, label: Duty cycle, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: Ii, label: Average input current, family: current, unit: A, min: 0 }}
  - {{ id: IL, label: Average inductor current, family: current, unit: A, min: 0 }}
  - {{ id: L, label: Inductance required, family: inductance, unit: uH, min: 0 }}
  - {{ id: Ipk, label: Peak switch / inductor current, family: current, unit: A, min: 0 }}
  - {{ id: Vsw, label: Switch and diode voltage stress, family: voltage, unit: V, min: 0 }}
  - {{ id: C, label: Output capacitance (min.), family: capacitance, unit: uF, min: 0 }}
equations:
  - D = Vo / (Vi * eta + Vo)
  - Ii = Vo * Io / (Vi * eta)
  - IL = Io / (1 - D)
  - L = Vi * D / (f * r * IL)
  - Ipk = IL * (1 + r / 2)
  - Vsw = Vi + Vo
  - C = Io * D / (f * dV)
faq:
  - q: What is the duty cycle of a buck-boost converter?
    a: Ideally D = |Vout| ÷ (Vin + |Vout|), so 50% gives |Vout| = Vin, below 50% steps down and above 50% steps up. Including efficiency, D ≈ |Vout| ÷ (Vin × η + |Vout|).
  - q: Why is the inductor current higher than the output current?
    a: The inductor delivers current to the output only during the off-time, so its average current is Iout ÷ (1 − D). At D = 54% a 0.5 A load needs about 1.09 A of inductor current.
  - q: What voltage rating does the switch need?
    a: The MOSFET and diode both see Vin + |Vout| when off — 24 V for +12 V to −12 V. Choose parts rated at least 20–30% higher to allow for ringing.
  - q: How is a SEPIC different from a buck-boost?
    a: A SEPIC has the same duty-cycle relation but gives a positive output, at the cost of a second inductor and a coupling capacitor. A 4-switch buck-boost also gives a positive output with higher efficiency.
related: [electronics/buck-converter, electronics/boost-converter, electronics/inductor-energy, electronics/mosfet-power-loss]
''', f'''
## How to use the buck-boost converter calculator

Enter the **input voltage**, the **magnitude** of the negative output voltage, the **output current**, the expected **efficiency**, the **switching frequency**, the inductor **ripple ratio** (20–40% of the inductor current is typical) and the allowed **output ripple**. The calculator returns the duty cycle, the average input and inductor currents, the minimum inductance, the peak current the switch and inductor must handle, the voltage stress on the switch and diode, and the minimum output capacitance.

## Buck-boost converter formulas (continuous conduction)

<p class="formula">D = |V<sub>o</sub>| ÷ (V<sub>i</sub> η + |V<sub>o</sub>|) &nbsp;·&nbsp; I<sub>L</sub> = I<sub>o</sub> ÷ (1 − D) &nbsp;·&nbsp; L = V<sub>i</sub> D ÷ (f · ΔI<sub>L</sub>)</p>

<p class="formula">I<sub>pk</sub> = I<sub>L</sub> (1 + r/2) &nbsp;·&nbsp; V<sub>sw</sub> = V<sub>i</sub> + |V<sub>o</sub>| &nbsp;·&nbsp; C ≥ I<sub>o</sub> D ÷ (f · ΔV)</p>

The output capacitor alone supplies the load while the switch is on, so — as in a [boost converter](/electronics/boost-converter/) — the output current is pulsed and the capacitor's ESR matters as much as its capacitance.

## Worked example

+{bVi:g} V in, −{bVo:g} V at {bIo:g} A out, η = {beta*100:g}%, f = {bf/1e3:g} kHz, 30% ripple, 50 mV output ripple:

- D = {bVo:g} ÷ ({bVi:g} × {beta:g} + {bVo:g}) = **{bD*100:.2f}%**
- Average input current = **{bIi:.3f} A**; average inductor current = {bIo:g} ÷ (1 − {bD:.4f}) = **{bIL:.4f} A**
- L = {bVi:g} × {bD:.4f} ÷ ({bf/1e3:g} kHz × 0.3 × {bIL:.4f} A) = **{bL*1e6:.2f} µH** — choose a standard 47 µH
- Peak current = **{bIpk:.4f} A**; switch voltage = **{bVsw:g} V**
- Output capacitance ≥ **{bC*1e6:.2f} µF** (plus margin for ESR and DC-bias derating)

## Output voltage vs duty cycle and inductor (12 V in, 0.5 A, 500 kHz, 30% ripple, η = 85%)

| Output | Duty cycle | Inductor current | L | Switch voltage |
|---|---|---|---|---|
{bb_rows}
## Design notes

- Rate the inductor's **saturation current** above the peak current, not the average.
- Use low-ESR ceramic output capacitors; ESR ripple = I<sub>pk</sub> × ESR adds to the capacitive ripple.
- The control loop has a right-half-plane zero, as in a boost, which limits loop bandwidth — follow the controller datasheet's compensation guide.
''')

# ---------------------------------------------------------------- Peukert's law
kC, kH, kI, kk = 100.0, 20.0, 10.0, 1.2
kt = kH * (kC / (kI * kH))**kk; kCe = kI * kt; kti = kC / kI
pk_rows = ''
for I in (2.5, 5, 10, 20, 50, 100):
    pk_rows += f"| {I:g} A | {kC/I:.2f} h | " + ' | '.join(f"{kH*(kC/(I*kH))**k:.2f} h" for k in (1.05, 1.1, 1.2, 1.3)) + " |\n"
P('electronics', 'peukerts-law', "peukert's law", f'''
title: Peukert's Law Calculator (Battery Runtime at High Current)
description: Estimate real battery runtime and effective capacity at any discharge current with Peukert's law, from the rated Ah, rated hours and Peukert exponent.
category: electronics
{intro("A battery's amp-hour rating is measured at a specific discharge time — usually 20 hours for lead-acid — and it delivers less capacity when discharged faster. This Peukert's law calculator corrects the simple Ah ÷ A estimate for the discharge rate, giving the realistic runtime and effective capacity; for overall [battery backup time](ib:calculate-battery-backup-time) planning, also allow for depth of discharge and inverter losses.")}
keywords: [peukert's law calculator, peukert calculator, battery runtime calculator, peukert exponent, battery discharge time, effective battery capacity, lead acid battery runtime]
updated: {D}
variables:
  - {{ id: C, label: Rated capacity, suffix: Ah, default: {kC:g}, min: 0 }}
  - {{ id: H, label: Rated discharge time (C-rating hours), family: seconds, unit: h, default: {kH:g}, min: 0 }}
  - {{ id: I, label: Actual discharge current, family: current, unit: A, default: {kI:g}, min: 0.000001 }}
  - {{ id: k, label: Peukert exponent k, default: {kk:g}, min: 1, decimals: 3 }}
  - {{ id: Ir, label: Rated discharge current C/H, family: current, unit: A, min: 0 }}
  - {{ id: t, label: Runtime (Peukert), family: seconds, unit: h, min: 0 }}
  - {{ id: t0, label: Runtime without Peukert (Ah ÷ A), family: seconds, unit: h, min: 0 }}
  - {{ id: Ce, label: Effective capacity at this current, suffix: Ah, min: 0 }}
equations:
  - Ir = C / (H / 3600)
  - t = H * (C / (I * H / 3600))^k
  - t0 = C / I * 3600
  - Ce = I * t / 3600
faq:
  - q: What is Peukert's law?
    a: An empirical rule for lead-acid batteries, t = H × (C ÷ (I × H))^k, where C is the rated capacity at the rated discharge time H and k is the Peukert exponent. With k = 1 the battery would give its full rated Ah at any current.
  - q: What is a typical Peukert exponent?
    a: Roughly 1.05–1.15 for AGM, 1.1–1.25 for gel and 1.2–1.4 for flooded lead-acid batteries; lithium-ion cells are close to 1.0–1.05. The battery datasheet's capacity-vs-rate table gives the exact value.
  - q: How do I calculate the Peukert exponent from a datasheet?
    a: Take two ratings, for example the 20 h and 5 h capacities. Convert each to a current (I = Ah ÷ h), then k = ln(t₂/t₁) ÷ ln(I₁/I₂).
  - q: Does Peukert's law apply at low currents?
    a: Below the rated current it predicts more than the rated capacity, which real batteries do not reliably deliver because of self-discharge. Treat the rated Ah as the ceiling.
related: [ecology/battery-storage, electrical/battery-bank-size, everyday-life/inverter-battery-backup, other/battery-life]
''', f'''
## How to use the Peukert's law calculator

Enter the **rated capacity** in amp-hours, the **rated discharge time** it was measured at (C20 = 20 h, C10 = 10 h, C5 = 5 h), the **load current** and the **Peukert exponent** from the datasheet. The calculator gives the rated current, the realistic runtime, the naive Ah ÷ A runtime for comparison and the effective capacity at your current. These are times to 100% discharge at a constant current and room temperature.

## Peukert's law formula

<p class="formula">t = H × ( C ÷ (I × H) )<sup>k</sup> &nbsp;·&nbsp; effective capacity = I × t</p>

<p class="formula">k = ln(t₂ ÷ t₁) ÷ ln(I₁ ÷ I₂)</p>

## Worked example

A {kC:g} Ah battery rated at the {kH:g}-hour rate (k = {kk:g}) supplies a {kI:g} A load:

- Rated current = {kC:g} ÷ {kH:g} = **{kC/kH:g} A**
- Runtime = {kH:g} × ({kC:g} ÷ ({kI:g} × {kH:g}))^{kk:g} = {kH:g} × 0.5^{kk:g} = **{kt:.2f} h**
- Naive estimate {kC:g} ÷ {kI:g} = {kti:g} h — about {(1-kt/kti)*100:.0f}% too optimistic
- Effective capacity = {kI:g} × {kt:.4f} = **{kCe:.2f} Ah**

## Runtime of a 100 Ah (C20) battery by current and Peukert exponent

| Current | Ah ÷ A | k = 1.05 | k = 1.1 | k = 1.2 | k = 1.3 |
|---|---|---|---|---|---|
{pk_rows}
## Practical notes

- **Usable depth of discharge** — lead-acid batteries last much longer if discharged only to 50%; multiply the runtime by the depth of discharge you plan to use.
- **Temperature** — capacity falls by roughly 0.5–1% per °C below 25 °C for lead-acid; allow extra margin in cold locations.
- **Varying loads** — Peukert's law assumes a constant current. For mixed loads, apply it to each period or use the average current as an approximation.
''')

# ---------------------------------------------------------------- Hall-effect current sensor
hVq, hS, hI, hVr, hN = 2.5, 185.0, 2.0, 5.0, 10
hVo = hVq + hS / 1000 * hI; hcnt = hVo / hVr * 2**hN; hres = hVr / (2**hN * hS / 1000)
hs_rows = ''
for nm, S, rng in (('ACS712 ±5 A', 185, 5), ('ACS712 ±20 A', 100, 20), ('ACS712 ±30 A', 66, 30)):
    hs_rows += f"| {nm} | {S} mV/A | {hVq - S/1000*rng:.3f} V | {hVq + S/1000*rng:.3f} V | {5/(1024*S/1000)*1000:.1f} mA | {5/(4096*S/1000)*1000:.1f} mA |\n"
P('electronics', 'hall-effect-current-sensor', 'hall-effect current sensor', f'''
title: Hall-Effect Current Sensor Calculator (Vout, I & ADC)
description: Convert current to output voltage and back for a Hall-effect current sensor such as the ACS712, with ADC counts and current resolution per count.
category: electronics
{intro("A Hall-effect current sensor outputs a voltage proportional to the current through it, centred on a zero-current offset — usually half the supply for ratiometric parts. This Hall-effect current sensor calculator converts current to output voltage and back, and gives the ADC reading and current resolution for a microcontroller; see how the [ACS712 Hall-effect current sensor](ib:hall-effect-current-sensor-acs712) works.")}
keywords: [hall effect current sensor calculator, acs712 calculator, acs712 voltage to current, current sensor sensitivity mv/a, hall sensor output voltage, acs712 adc conversion, arduino current sensor formula]
updated: {D}
variables:
  - {{ id: Vq, label: Zero-current output (offset), family: voltage, unit: V, default: {hVq:g} }}
  - {{ id: S, label: Sensitivity, suffix: mV/A, default: {hS:g}, min: 0.000001 }}
  - {{ id: I, label: Current through sensor, family: current, unit: A, default: {hI:g} }}
  - {{ id: Vref, label: ADC reference voltage, family: voltage, unit: V, default: {hVr:g}, min: 0 }}
  - {{ id: N, label: ADC resolution, suffix: bits, default: {hN}, min: 1, decimals: 0 }}
  - {{ id: Vout, label: Sensor output voltage, family: voltage, unit: V }}
  - {{ id: cnt, label: ADC reading (counts), decimals: 1 }}
  - {{ id: res, label: Current per ADC count, family: current, unit: mA, min: 0 }}
equations:
  - Vout = Vq + S / 1000 * I
  - cnt = Vout / Vref * 2^N
  - res = Vref / (2^N * S / 1000)
faq:
  - q: How do I convert ACS712 output voltage to current?
    a: I = (Vout − Vq) ÷ S. With a 5 V supply Vq ≈ 2.5 V, so the ±5 A version (185 mV/A) reading 2.87 V means (2.87 − 2.5) ÷ 0.185 = 2.0 A.
  - q: What are the ACS712 sensitivities?
    a: 185 mV/A for the ±5 A version, 100 mV/A for ±20 A and 66 mV/A for ±30 A, all at a 5 V supply. The output is ratiometric, so the offset and sensitivity scale with the supply voltage.
  - q: How do I get the current from an Arduino ADC reading?
    a: Voltage = reading × Vref ÷ 1024 for a 10-bit ADC, then I = (voltage − Vq) ÷ sensitivity. Calibrate Vq by reading the sensor with no current flowing.
  - q: Why is my reading noisy?
    a: With a 10-bit ADC one count is about 26 mA on the 5 A sensor, and the sensor itself has noise of a few tens of mA. Average many samples, add the recommended filter capacitor, and use the smallest range that covers your current.
related: [electronics/shunt-resistor, electronics/adc-resolution, electronics/op-amp-gain, electrical/ct-burden]
''', f'''
## How to use the Hall-effect current sensor calculator

Enter the sensor's **zero-current output** (Vcc/2 for ratiometric sensors such as the ACS712), its **sensitivity** in mV/A, the **current** and your ADC's **reference voltage** and **resolution**. You get the sensor output voltage, the ADC reading you should expect and the current represented by one ADC count. To go from a measured voltage to current, enter the voltage in the output field and leave the current blank. Negative current gives an output below the offset.

## Hall-effect current sensor formulas

<p class="formula">V<sub>out</sub> = V<sub>q</sub> + S × I &nbsp;·&nbsp; I = (V<sub>out</sub> − V<sub>q</sub>) ÷ S</p>

<p class="formula">ADC counts = V<sub>out</sub> ÷ V<sub>ref</sub> × 2<sup>N</sup> &nbsp;·&nbsp; resolution = V<sub>ref</sub> ÷ (2<sup>N</sup> × S)</p>

## Worked example

ACS712 ±5 A (185 mV/A) on a 5 V supply, measuring {hI:g} A with a 10-bit ADC and a 5 V reference:

- V<sub>out</sub> = {hVq:g} + 0.185 × {hI:g} = **{hVo:.2f} V**
- ADC reading = {hVo:.2f} ÷ 5 × 1024 = **{hcnt:.1f}** counts
- One count = 5 ÷ (1024 × 0.185) = **{hres*1000:.1f} mA**

## ACS712 output range and resolution (5 V supply)

| Sensor | Sensitivity | Output at −full scale | Output at +full scale | 10-bit resolution | 12-bit resolution |
|---|---|---|---|---|---|
{hs_rows}
## Practical notes

- Hall sensors are **isolated** — the current path is separate from the signal side — which makes them safer than a [shunt resistor](/electronics/shunt-resistor/) on high-side or mains circuits. Read how a [Hall-effect sensor works](https://www.instrumentationblog.in/how-a-hall-effect-sensor-works/).
- Zero the offset in firmware at start-up with no current flowing; offset drift with temperature is often the largest error at low current.
- Keep strong magnetic fields and high-current wires away from the sensor package; they shift the reading.
- For AC current, sample fast and compute RMS from the samples after subtracting the offset.
''')

print(len(DESC), 'pages:', ' '.join(DESC))
