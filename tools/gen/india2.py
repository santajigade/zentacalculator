import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
from inr import inr, lakh
D = '2026-10-27'
step = lambda x: 1 if x > 1e-9 else 0

# ---------------------------------------------------------------- Income tax
SN = "(0.05*max(0, min(X, 800000) - 400000) + 0.10*max(0, min(X, 1200000) - 800000) + 0.15*max(0, min(X, 1600000) - 1200000) + 0.20*max(0, min(X, 2000000) - 1600000) + 0.25*max(0, min(X, 2400000) - 2000000) + 0.30*max(0, X - 2400000))"
SO = "(0.05*max(0, min(X, 500000) - 250000) + 0.20*max(0, min(X, 1000000) - 500000) + 0.30*max(0, X - 1000000))"
def new_tax(G, sal=1):
    X = max(0, G - 75000 * sal)
    s = .05*max(0,min(X,8e5)-4e5)+.10*max(0,min(X,12e5)-8e5)+.15*max(0,min(X,16e5)-12e5)+.20*max(0,min(X,20e5)-16e5)+.25*max(0,min(X,24e5)-20e5)+.30*max(0,X-24e5)
    r = min(s, max(0, X - 12e5)); sc = r*(.10*step(X-5e6)+.05*step(X-1e7)+.10*step(X-2e7))
    return X, (r + sc) * 1.04
def old_tax(G, Dd, sal=1):
    X = max(0, G - 50000 * sal - Dd)
    s = .05*max(0,min(X,5e5)-2.5e5)+.20*max(0,min(X,1e6)-5e5)+.30*max(0,X-1e6)
    r = s*step(X-5e5); sc = r*(.10*step(X-5e6)+.05*step(X-1e7)+.10*step(X-2e7)+.12*step(X-5e7))
    return X, (r + sc) * 1.04
Xn = "max(0, G - 75000*sal)"; Xo = "max(0, G - 50000*sal - Dd)"
sn = SN.replace('X', Xn); so = SO.replace('X', Xo)
eq_new = f"Tn = (min({sn}, max(0, {Xn} - 1200000))) * (1 + 0.10*step({Xn} - 5000000) + 0.05*step({Xn} - 10000000) + 0.10*step({Xn} - 20000000)) * 1.04"
eq_old = f"To = {so} * step({Xo} - 500000) * (1 + 0.10*step({Xo} - 5000000) + 0.05*step({Xo} - 10000000) + 0.10*step({Xo} - 20000000) + 0.12*step({Xo} - 50000000)) * 1.04"
X1, t1 = new_tax(1500000); Xo1, to1 = old_tax(1500000, 200000)
rows = ''
for G in [700000, 1000000, 1275000, 1500000, 2000000, 2500000, 3000000, 5000000]:
    X, t = new_tax(G); rows += f"| {inr(G)} | {inr(X)} | {inr(t)} | {inr(t/12)} | {t/G*100:.1f}% |\n"
cmp = ''
for G, Dd in [(1000000, 150000), (1500000, 200000), (1500000, 450000), (2500000, 375000), (2500000, 600000)]:
    _, a = new_tax(G); _, b = old_tax(G, Dd)
    cmp += f"| {inr(G)} | {inr(Dd)} | {inr(a)} | {inr(b)} | {'New' if a < b else 'Old' if b < a else 'Same'} |\n"
# marginal relief demo
_, mr = new_tax(1300000 + 75000)
page('finance', 'income-tax-india', f'''
title: Income Tax Calculator India (FY 2026-27, New vs Old Regime)
description: Calculate income tax for FY 2026-27 under the new and old regime — with standard deduction, ₹12 lakh rebate, marginal relief, surcharge and 4% cess.
category: finance
keywords: [income tax calculator, income tax calculator india, new tax regime calculator, old vs new regime, fy 2026-27, ay 2027-28, tax year 2026-27, salary tax calculator, 87a rebate, income tax slab]
updated: {D}
featured: true
variables:
  - {{ id: G, label: Gross annual income, family: currency, prefix: '₹', default: 1500000, min: 0, decimals: 0 }}
  - id: sal
    label: Income type
    default: 1
    options:
      - {{ label: Salary or pension (standard deduction), value: 1 }}
      - {{ label: Other income only, value: 0 }}
  - {{ id: Dd, label: Deductions claimed (old regime only), family: currency, prefix: '₹', default: 200000, min: 0, decimals: 0, help: '80C, 80D, home loan interest, HRA exemption and so on. Ignored in the new regime.' }}
  - {{ id: Tn, label: Tax — new regime, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: To, label: Tax — old regime, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: Sv, label: You save with the new regime, family: currency, prefix: '₹', decimals: 0, help: 'Negative means the old regime is cheaper.' }}
  - {{ id: Mn, label: Monthly tax (new regime), family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - {eq_new}
  - {eq_old}
  - Sv = To - Tn
  - Mn = Tn / 12
faq:
  - q: What are the new regime tax slabs for FY 2026-27?
    a: Up to ₹4 lakh nil, ₹4–8 lakh 5%, ₹8–12 lakh 10%, ₹12–16 lakh 15%, ₹16–20 lakh 20%, ₹20–24 lakh 25% and above ₹24 lakh 30%. Budget 2026 kept the same slabs as FY 2025-26.
  - q: Is income up to ₹12 lakh tax-free?
    a: Yes, under the new regime a rebate makes tax nil when taxable income is up to ₹12 lakh. For salaried people the ₹75,000 standard deduction takes this to ₹12.75 lakh of salary.
  - q: What is marginal relief?
    a: If taxable income is just above ₹12 lakh, the tax cannot be more than the income above ₹12 lakh. At ₹12.5 lakh taxable, slab tax is ₹67,500 but you pay only ₹50,000 (plus cess). The relief ends at about ₹12.71 lakh.
  - q: Which regime is better for me?
    a: Enter your deductions. The old regime wins only when deductions are large — typically ₹4 lakh or more at ₹15 lakh income. The calculator shows the saving directly.
  - q: What is the standard deduction?
    a: ₹75,000 in the new regime and ₹50,000 in the old regime, for salaried employees and pensioners.
  - q: Does the Income-tax Act 2025 change my tax?
    a: The new Act replaced the 1961 Act from 1 April 2026 and uses the term “tax year”. The slab rates for 2026-27 stayed the same.
related: [finance/hra-exemption, finance/gratuity, finance/salary-increase, finance/gst, finance/ppf]
''', f'''
## How to use this calculator

1. Enter your **gross annual income** — salary before deductions, plus interest and other income.
2. Choose **salary or pension** to apply the standard deduction (₹75,000 new, ₹50,000 old).
3. Enter the **deductions** you can claim under the old regime: 80C (PPF, ELSS, EPF, life insurance), 80D (health insurance), home loan interest, HRA exemption and so on.

You see the tax under both regimes, including the 4% health and education cess, and how much the new regime saves you.

## New regime slabs (FY 2026-27)

| Taxable income | Rate |
|---|---|
| Up to ₹4,00,000 | Nil |
| ₹4,00,001 – ₹8,00,000 | 5% |
| ₹8,00,001 – ₹12,00,000 | 10% |
| ₹12,00,001 – ₹16,00,000 | 15% |
| ₹16,00,001 – ₹20,00,000 | 20% |
| ₹20,00,001 – ₹24,00,000 | 25% |
| Above ₹24,00,000 | 30% |

- **Standard deduction**: ₹75,000 for salary and pension.
- **Rebate**: tax is nil if taxable income is up to ₹12,00,000 (rebate up to ₹60,000), with marginal relief just above it.
- **Cess**: 4% on tax plus surcharge.
- The new regime is the **default**. You must opt out to use the old regime.

## Old regime slabs (below 60 years)

| Taxable income | Rate |
|---|---|
| Up to ₹2,50,000 | Nil |
| ₹2,50,001 – ₹5,00,000 | 5% |
| ₹5,00,001 – ₹10,00,000 | 20% |
| Above ₹10,00,000 | 30% |

Rebate makes tax nil up to ₹5,00,000 of taxable income. Senior citizens have higher exemption limits (₹3 lakh, or ₹5 lakh above 80), which this calculator does not apply.

## Worked example

Salary of **₹15,00,000**, deductions of ₹2,00,000:

**New regime**

- Taxable = 15,00,000 − 75,000 = {inr(X1)}
- Tax = 20,000 + 40,000 + {inr(.15*(X1-12e5))[1:]} = {inr(t1/1.04)}
- Plus 4% cess = **{inr(t1)}**

**Old regime**

- Taxable = 15,00,000 − 50,000 − 2,00,000 = {inr(Xo1)}
- Tax = 12,500 + 1,00,000 + {inr(.3*(Xo1-1e6))[1:]} = {inr(to1/1.04)}
- Plus 4% cess = **{inr(to1)}**

The new regime saves **{inr(to1-t1)}** here.

## Tax at different salaries (new regime)

| Salary | Taxable | Tax incl. cess | Per month | Effective rate |
|---|---|---|---|---|
{rows}
## New vs old regime — who wins?

| Salary | Deductions | New regime | Old regime | Better |
|---|---|---|---|---|
{cmp}
The old regime pays off only if you claim large deductions, usually home loan interest plus full 80C, 80D and HRA.

## Marginal relief explained

Without marginal relief, earning ₹1 above ₹12 lakh of taxable income would suddenly cost ₹60,000 in tax. The law caps the tax (before cess) at the **lower** of the slab tax and the income above ₹12 lakh:

| Taxable income | Slab tax | Income above ₹12 lakh | Tax payable (before cess) |
|---|---|---|---|
| ₹12,00,000 | ₹60,000 | ₹0 | ₹0 |
| ₹12,25,000 | ₹63,750 | ₹25,000 | ₹25,000 |
| ₹12,50,000 | ₹67,500 | ₹50,000 | ₹50,000 |
| ₹12,70,000 | ₹70,500 | ₹70,000 | ₹70,000 |
| ₹13,00,000 | ₹75,000 | ₹1,00,000 | ₹75,000 |

From about ₹12.71 lakh onward the normal slab tax applies. The calculator handles this automatically.

## Surcharge

Above ₹50 lakh a surcharge is added: 10% (₹50 lakh–1 crore), 15% (₹1–2 crore) and 25% above ₹2 crore in the new regime. The old regime goes up to 37% above ₹5 crore. The calculator adds surcharge but does not apply marginal relief on surcharge, so results just above these thresholds may be slightly high.

## Keep in mind

- This is an estimate for resident individuals below 60. Capital gains, lottery income and other special-rate income are taxed differently.
- Employers deduct TDS each month based on the regime you declare.
- Check the final figure with your Form 16 or a tax professional before filing.
''')

# ---------------------------------------------------------------- HRA
def hra(B, H, R, m): return max(0, min(H, R - .1 * B, m * B))
e1 = hra(600000, 240000, 240000, .5)
page('finance', 'hra-exemption', f'''
title: HRA Exemption Calculator
description: Work out how much of your house rent allowance is tax-exempt under Section 10(13A) — metro and non-metro — and how much is taxable.
category: finance
keywords: [hra calculator, hra exemption calculator, house rent allowance, section 10(13a), hra tax exemption, hra metro, rent receipts, old regime hra]
updated: {D}
variables:
  - {{ id: B, label: Basic salary + DA (per year), family: currency, prefix: '₹', default: 600000, min: 0, decimals: 0 }}
  - {{ id: H, label: HRA received (per year), family: currency, prefix: '₹', default: 240000, min: 0, decimals: 0 }}
  - {{ id: R, label: Rent paid (per year), family: currency, prefix: '₹', default: 240000, min: 0, decimals: 0 }}
  - id: m
    label: City
    default: 0.5
    options:
      - {{ label: 'Metro (Delhi, Mumbai, Kolkata, Chennai) — 50%', value: 0.5 }}
      - {{ label: Other city — 40%, value: 0.4 }}
  - {{ id: E, label: HRA exempt from tax, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: Tx, label: Taxable HRA, family: currency, prefix: '₹', decimals: 0 }}
equations:
  - E = max(0, min(H, R - 0.1*B, m*B))
  - Tx = H - E
faq:
  - q: How is HRA exemption calculated?
    a: The exemption is the lowest of three amounts — actual HRA received, rent paid minus 10% of basic + DA, and 50% of basic + DA in a metro (40% elsewhere).
  - q: Can I claim HRA in the new tax regime?
    a: No. HRA exemption is available only under the old regime.
  - q: Which cities count as metro for HRA?
    a: Only Delhi, Mumbai, Kolkata and Chennai. Bengaluru, Hyderabad, Pune and others use the 40% limit.
  - q: Do I need my landlord’s PAN?
    a: Yes, if the rent you pay is more than ₹1 lakh a year. Keep rent receipts or a rent agreement as proof.
  - q: Can I claim HRA if I pay rent to my parents?
    a: Yes, if you genuinely pay rent and they own the house. They must show it as rental income.
related: [finance/income-tax-india, finance/salary-increase, finance/gratuity, finance/emi]
''', f'''
## How to use this calculator

Enter your yearly **basic salary plus dearness allowance**, the **HRA** your employer pays, the **rent** you pay and choose your **city**. The calculator shows the tax-exempt part of your HRA and the part added to your taxable income.

If your salary or rent changed during the year, calculate each period separately and add the results.

## The HRA rule

The exempt amount is the **lowest** of:

1. Actual HRA received
2. Rent paid − 10% of (basic + DA)
3. 50% of (basic + DA) in a metro, or 40% in other cities

<p class="formula">Exempt HRA = min(HRA, Rent − 0.1 × Basic, 0.5 or 0.4 × Basic)</p>

## Worked example

Basic + DA ₹6,00,000, HRA ₹2,40,000, rent ₹20,000 a month (₹2,40,000), living in Mumbai:

1. Actual HRA = ₹2,40,000
2. Rent − 10% of basic = 2,40,000 − 60,000 = **₹1,80,000**
3. 50% of basic = ₹3,00,000

The lowest is **{inr(e1)}**, so that much is exempt and ₹60,000 is taxable.

## How rent changes the exemption

Same salary (basic ₹6,00,000, HRA ₹2,40,000), metro:

| Monthly rent | Exempt HRA | Taxable HRA |
|---|---|---|
''' + ''.join(f"| {inr(r)} | {inr(hra(6e5,2.4e5,r*12,.5))} | {inr(2.4e5-hra(6e5,2.4e5,r*12,.5))} |\n" for r in [5000, 10000, 15000, 20000, 25000, 30000]) + f'''
Below ₹5,000 a month (10% of basic) there is no exemption at all. Above ₹25,000 the exemption is capped by the HRA itself.

## Documents you need

- Rent receipts or a rent agreement.
- Landlord’s PAN if rent is above ₹1,00,000 a year.
- Submit proofs to your employer during the year so TDS is reduced.

## Keep in mind

- HRA exemption applies only in the **old regime**. Use the [income tax calculator](/finance/income-tax-india/) to see if the old regime still saves you tax.
- If you do not receive HRA but pay rent, you may be able to claim a smaller deduction under section 80GG in the old regime.
- You cannot claim HRA for a house you own and live in.
''')

# ---------------------------------------------------------------- Gratuity
def grat(S, y, cov=1):
    import math
    return 15/26*S*round(y) if cov else 15/30*S*math.floor(y)
g1 = grat(50000, 10.67)
page('finance', 'gratuity', f'''
title: Gratuity Calculator
description: Calculate gratuity from last drawn basic + DA and years of service using the 15/26 formula — with the ₹20 lakh tax-exempt limit.
category: finance
keywords: [gratuity calculator, gratuity formula, 15/26 formula, gratuity calculation india, gratuity tax exemption, payment of gratuity act, gratuity eligibility, gratuity 5 years]
updated: {D}
variables:
  - {{ id: S, label: Last drawn monthly basic + DA, family: currency, prefix: '₹', default: 50000, min: 0, decimals: 0 }}
  - {{ id: y, label: Years of service, family: none, suffix: years, default: 10.67, min: 0, help: 'Use decimals for months, for example 10 years 8 months = 10.67.' }}
  - id: cov
    label: Employer
    default: 1
    options:
      - {{ label: 'Covered by gratuity law (15/26)', value: 1 }}
      - {{ label: 'Not covered (15/30)', value: 0 }}
  - {{ id: Gr, label: Gratuity amount, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: Ex, label: Tax-exempt (up to ₹20 lakh), family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: Tx, label: Taxable gratuity, family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - Gr = cov * 15/26 * S * round(y) + (1 - cov) * 15/30 * S * floor(y)
  - Ex = min(Gr, 2000000)
  - Tx = Gr - Ex
faq:
  - q: What is the gratuity formula?
    a: For employers covered by the law, gratuity = 15 × last drawn basic + DA × years of service ÷ 26. The 15 stands for 15 days’ wages per year and 26 for working days in a month.
  - q: How much gratuity for 10 years with ₹50,000 basic?
    a: 15 × 50,000 × 10 ÷ 26 = ₹2,88,462. With 10 years 8 months, service rounds up to 11 years and gratuity is about {inr(g1)}.
  - q: How are years of service rounded?
    a: Under the gratuity law, a final part-year of more than 6 months counts as a full year. 7 years 8 months becomes 8 years; 7 years 5 months stays 7.
  - q: Who is eligible for gratuity?
    a: Permanent employees after 5 years of continuous service. Under the new labour codes, fixed-term employees become eligible after 1 year. There is no minimum on death or disability.
  - q: Is gratuity taxable?
    a: For private employees gratuity is tax-free up to ₹20 lakh over your whole career. Government employees get up to ₹25 lakh. Anything above is taxed at your slab rate.
related: [finance/epf, finance/income-tax-india, finance/retirement-corpus, finance/hra-exemption]
''', f'''
## How to use this calculator

Enter your **last drawn monthly basic salary plus dearness allowance** and your **years of service**. Choose whether your employer is covered by the gratuity law — almost all organisations with 10 or more employees are. You see the gratuity amount, the tax-exempt part and any taxable part.

## The gratuity formula

**Employers covered by the law**

<p class="formula">Gratuity = 15 × last drawn (basic + DA) × years of service ÷ 26</p>

Years of service are rounded: more than 6 months in the final year counts as a full year.

**Employers not covered**

<p class="formula">Gratuity = 15 × average (basic + DA) × completed years ÷ 30</p>

Only completed years count, and the average salary of the last 10 months is used.

## Worked example

Basic + DA of **₹50,000** a month, **10 years 8 months** of service, covered employer:

- Years counted = **11** (8 months is more than 6)
- Gratuity = 15 × 50,000 × 11 ÷ 26 = **{inr(g1)}**
- Fully tax-free, as it is below ₹20 lakh.

## Gratuity by salary and service

| Basic + DA | 5 years | 10 years | 20 years | 30 years |
|---|---|---|---|---|
''' + ''.join(f"| {inr(S)} | {inr(grat(S,5))} | {inr(grat(S,10))} | {inr(grat(S,20))} | {inr(grat(S,30))} |\n" for S in [25000, 50000, 100000, 150000]) + f'''
## Eligibility

- **Permanent employees**: 5 years of continuous service.
- **Fixed-term employees**: 1 year, under the Code on Social Security.
- **Death or disability**: no minimum service. Gratuity goes to the nominee.
- Gratuity is paid on retirement, resignation, termination (except for misconduct) or death.

## Wages under the new labour codes

The labour codes require basic pay plus DA to be at least **50% of total pay**. If your employer restructures your salary to meet this, your basic rises and so does your gratuity.

## Tax on gratuity

- **Private-sector employees**: exempt up to ₹20,00,000 across your career.
- **Government employees**: exempt up to ₹25,00,000.
- Any amount above the limit is added to income and taxed at slab rates.

## Keep in mind

Employers must pay gratuity within 30 days of it becoming due, or pay interest on the delay. Check your appointment letter for any gratuity scheme more generous than the law.
''')

# ---------------------------------------------------------------- EPF
def epf(B, A, bal, g, r, ret=58):
    Y = ret - A; C = 0.12*B + 0.12*B - min(1250, 0.0833*B)
    F = bal*(1+r)**Y + C*(12+5.5*r)*((1+r)**Y-(1+g)**Y)/(r-g)
    inv = C*12*((1+g)**Y-1)/g
    return F, inv, C
f1, i1, c1 = epf(30000, 30, 200000, .05, .0825)
page('finance', 'epf', f'''
title: EPF Calculator (Provident Fund Maturity)
description: Estimate your EPF balance at retirement from basic salary, age, yearly salary increase and the current 8.25% EPF interest rate.
category: finance
keywords: [epf calculator, pf calculator, provident fund calculator, epf interest rate, epf maturity, epfo, pf balance at retirement, employee provident fund]
updated: {D}
variables:
  - {{ id: B, label: Monthly basic + DA, family: currency, prefix: '₹', default: 30000, min: 0, decimals: 0 }}
  - {{ id: A, label: Your age, family: none, suffix: years, default: 30, min: 15, max: 57 }}
  - {{ id: bal, label: Current EPF balance, family: currency, prefix: '₹', default: 200000, min: 0, decimals: 0 }}
  - {{ id: g, label: Yearly salary increase, family: percent, unit: '%', default: 5, min: 0.0001, max: 0.5 }}
  - {{ id: r, label: EPF interest rate, family: percent, unit: '%', default: 8.25, min: 0.0001, max: 0.3 }}
  - {{ id: C, label: Monthly contribution to EPF (you + employer), family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: F, label: EPF balance at 58, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: inv, label: Total contributions, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: I, label: Total interest earned, family: currency, prefix: '₹', decimals: 0 }}
equations:
  - C = 0.24*B - min(1250, 0.0833*B)
  - F = bal*(1 + r)^(58 - A) + C*(12 + 5.5*r)*((1 + r)^(58 - A) - (1 + g)^(58 - A))/(r - g)
  - inv = C*12*((1 + g)^(58 - A) - 1)/g
  - I = F - bal - inv
faq:
  - q: What is the EPF interest rate?
    a: 8.25% a year for 2025-26, the same as the previous year. EPFO declares the rate every year after the financial year ends.
  - q: How much goes into my EPF every month?
    a: You contribute 12% of basic + DA. Your employer also contributes 12%, but 8.33% (up to ₹1,250 a month) goes to the pension scheme (EPS) and only the rest goes to EPF.
  - q: How is EPF interest calculated?
    a: Interest is worked out monthly on the running balance at the annual rate ÷ 12, and credited to your account once a year. It then compounds yearly.
  - q: Is EPF interest tax-free?
    a: Mostly. Interest on your own contributions above ₹2.5 lakh a year (₹5 lakh if the employer does not contribute) is taxable. Withdrawals after 5 years of continuous service are tax-free.
  - q: When can I withdraw my EPF?
    a: In full at retirement (58), or after 2 months of unemployment. Partial withdrawals are allowed for a house, education, marriage and medical needs.
related: [finance/ppf, finance/gratuity, finance/nps, finance/retirement-corpus, finance/income-tax-india]
''', f'''
## How to use this calculator

Enter your **monthly basic salary plus DA**, your **age**, your **current EPF balance** (from the EPFO passbook), the **yearly salary increase** you expect and the **interest rate**. The calculator estimates your EPF balance at age 58, the total contributions and the interest earned.

## How EPF contributions work

| Contribution | Share of basic + DA | Goes to |
|---|---|---|
| Employee | 12% | EPF |
| Employer | 3.67% (or 12% minus ₹1,250 above ₹15,000 basic) | EPF |
| Employer | 8.33%, capped at ₹1,250 a month | EPS (pension) |

So on a basic of ₹30,000 the monthly EPF credit is 3,600 + 2,350 = **{inr(c1)}**.

## The formula

Within a year, interest is simple — each month's deposit earns interest for the months left in the year. That makes a year's deposits worth about C × (12 + 5.5 × r) at year end. The balance then compounds yearly, and contributions grow with your salary at rate g:

<p class="formula">F = Bal × (1 + r)<sup>Y</sup> + C × (12 + 5.5r) × [(1 + r)<sup>Y</sup> − (1 + g)<sup>Y</sup>] ÷ (r − g)</p>

where Y = 58 − your age.

## Worked example

Age 30, basic + DA ₹30,000, balance ₹2,00,000, 5% yearly raise, 8.25% interest:

- Monthly EPF contribution = **{inr(c1)}**
- Total contributions to 58 = **{inr(i1)}**
- EPF at 58 = **{inr(f1)}**
- Interest earned = **{inr(f1-i1-200000)}**

## EPF at 58 by starting age

Basic ₹30,000, no current balance, 5% raises, 8.25%:

| Age now | Years | EPF at 58 |
|---|---|---|
''' + ''.join(f"| {A} | {58-A} | {inr(epf(30000,A,0,.05,.0825)[0])} |\n" for A in [25, 30, 35, 40, 45, 50]) + f'''
## Boost your EPF with VPF

You can contribute more than 12% through the **Voluntary Provident Fund (VPF)**. It earns the same 8.25% rate and is just as safe. Remember that interest on employee contributions above ₹2.5 lakh a year is taxable.

## Keep in mind

- This is an estimate. The interest rate is set every year and your salary may grow faster or slower.
- EPS gives a separate monthly pension and is not included here.
- Do not withdraw EPF when you change jobs — transfer it with your UAN so it keeps compounding.
''')

# ---------------------------------------------------------------- NPS
def nps(M, A, r, a=.2, ar=.06):
    Y = 60 - A; i = r/12; F = M*((1+i)**(12*Y)-1)/i*(1+i)
    return F, (1-a)*F, a*F*ar/12, M*12*Y
n1 = nps(5000, 30, .10)
page('finance', 'nps', f'''
title: NPS Calculator (National Pension System)
description: Estimate your NPS corpus at 60, the lump sum you can withdraw and the monthly pension from the annuity — using current exit rules.
category: finance
keywords: [nps calculator, national pension system calculator, nps pension calculator, nps returns, nps annuity, nps lump sum, nps tier 1, nps 80% withdrawal]
updated: {D}
variables:
  - {{ id: M, label: Monthly contribution, family: currency, prefix: '₹', default: 5000, min: 0, decimals: 0 }}
  - {{ id: A, label: Your age, family: none, suffix: years, default: 30, min: 18, max: 59 }}
  - {{ id: r, label: Expected return (per year), family: percent, unit: '%', default: 10, min: 0.0001, max: 0.5 }}
  - {{ id: a, label: Share used to buy annuity, family: percent, unit: '%', default: 20, min: 0, max: 1, help: 'At least 20% for most non-government subscribers with a corpus above ₹12 lakh.' }}
  - {{ id: ar, label: Annuity rate (per year), family: percent, unit: '%', default: 6, min: 0, max: 0.2 }}
  - {{ id: F, label: Corpus at 60, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: L, label: Lump sum you can withdraw, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: P, label: Monthly pension, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: inv, label: Total contributed, family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - F = M*((1 + r/12)^(12*(60 - A)) - 1)/(r/12)*(1 + r/12)
  - L = (1 - a)*F
  - P = a*F*ar/12
  - inv = M*12*(60 - A)
chart: {{ x: A, y: F, from: 20, to: 55 }}
faq:
  - q: How much pension will I get from NPS?
    a: It depends on the corpus and the share you put into an annuity. ₹5,000 a month from age 30 at 10% builds about {inr(n1[0])}. Using 20% for an annuity at 6% gives about {inr(n1[2])} a month; using 40% doubles it.
  - q: How much of my NPS can I withdraw at 60?
    a: Since the December 2025 rule change, non-government subscribers can take up to 80% as a lump sum when the corpus is above ₹12 lakh, and must use at least 20% for an annuity. Smaller corpuses have more flexible options.
  - q: Is the NPS lump sum tax-free?
    a: Up to 60% of the corpus is tax-free on exit. If you withdraw more than 60%, the excess may be taxable. The annuity income is taxed at your slab rate.
  - q: What return does NPS give?
    a: It depends on your equity share. Equity schemes have historically returned around 10–12% a year over long periods, government bond schemes around 8–9%. Returns are not guaranteed.
  - q: What tax benefits does NPS give?
    a: Your own contribution qualifies under 80C and an extra ₹50,000 under 80CCD(1B) in the old regime. Employer contributions up to 14% of basic are deductible in the new regime too.
related: [finance/epf, finance/ppf, finance/sip, finance/retirement-corpus, finance/swp]
''', f'''
## How to use this calculator

Enter your **monthly contribution**, your **age**, the **expected return**, the **share of the corpus you will use to buy an annuity** and the **annuity rate**. The calculator shows your corpus at 60, the lump sum you can take and the monthly pension.

## The formula

The corpus grows like a monthly SIP:

<p class="formula">Corpus = M × [((1 + i)<sup>n</sup> − 1) ÷ i] × (1 + i)</p>

with i = annual return ÷ 12 and n = months until 60. Then:

- **Lump sum** = (1 − annuity share) × corpus
- **Monthly pension** = annuity share × corpus × annuity rate ÷ 12

## Worked example

₹5,000 a month from age 30 to 60 at 10%:

- Total contributed = **{inr(n1[3])}**
- Corpus at 60 = **{inr(n1[0])}**
- Lump sum (80%) = **{inr(n1[1])}**
- Pension from 20% annuity at 6% = **{inr(n1[2])} a month**

## Corpus by starting age

₹5,000 a month at 10%:

| Start age | Years | Corpus at 60 | Pension (40% annuity) |
|---|---|---|---|
''' + ''.join(f"| {A} | {60-A} | {inr(nps(5000,A,.10)[0])} | {inr(nps(5000,A,.10,.4)[2])} |\n" for A in [25, 30, 35, 40, 45]) + f'''
## NPS exit rules at 60 (non-government subscribers)

| Corpus | What you can do |
|---|---|
| Up to ₹8 lakh | Withdraw everything, no annuity needed |
| ₹8–12 lakh | Up to ₹6 lakh lump sum; rest as annuity or systematic withdrawal |
| Above ₹12 lakh | Up to 80% lump sum; at least 20% in an annuity |

You can also defer withdrawal and stay invested up to age 85. Government employees follow different rules (40% minimum annuity).

## Choosing your asset mix

- **Active choice**: pick your own split across equity (up to 75%), corporate bonds and government securities.
- **Auto choice**: equity is reduced automatically as you get older.

Younger investors can usually afford more equity for higher long-term growth.

## Keep in mind

- Annuity rates change with interest rates. Check current quotes from annuity providers before you retire.
- Pension from an annuity does not rise with inflation unless you choose a rising annuity.
- Returns are market-linked and not guaranteed.
''')

# ---------------------------------------------------------------- SSY
def ssy(P, r): return P*((1+r)**15-1)/r*(1+r)*(1+r)**6
s1 = ssy(150000, .082)
page('finance', 'sukanya-samriddhi', f'''
title: Sukanya Samriddhi Yojana Calculator (SSY)
description: Calculate Sukanya Samriddhi maturity at the current 8.2% rate — 15 years of deposits, maturity at 21 years, fully tax-free.
category: finance
keywords: [sukanya samriddhi calculator, ssy calculator, sukanya samriddhi yojana, ssy interest rate, ssy maturity, girl child savings scheme, post office ssy]
updated: {D}
variables:
  - {{ id: P, label: Yearly deposit, family: currency, prefix: '₹', default: 150000, min: 0, decimals: 0, help: '₹250 to ₹1,50,000 per financial year.' }}
  - {{ id: r, label: Interest rate, family: percent, unit: '%', default: 8.2, min: 0.0001, max: 0.3 }}
  - {{ id: age, label: Daughter's age at opening, family: none, suffix: years, default: 1, min: 0, max: 10 }}
  - {{ id: F, label: Maturity value, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: inv, label: Total deposited, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: I, label: Interest earned, family: currency, prefix: '₹', decimals: 0 }}
  - {{ id: mat, label: Daughter's age at maturity, family: none, suffix: years }}
equations:
  - F = P*((1 + r)^15 - 1)/r*(1 + r)*(1 + r)^6
  - inv = 15*P
  - I = F - inv
  - mat = age + 21
faq:
  - q: What is the Sukanya Samriddhi interest rate?
    a: 8.2% a year, compounded annually, for October–December 2026. The rate is reviewed every quarter.
  - q: How much will I get if I deposit ₹1.5 lakh a year?
    a: About {inr(s1)} at maturity. You deposit ₹22,50,000 over 15 years and earn about {inr(s1-2250000)} of tax-free interest.
  - q: For how many years do I deposit?
    a: For 15 years from opening. The account then keeps earning interest until it matures 21 years after opening.
  - q: Who can open an SSY account?
    a: A parent or legal guardian, for a girl child below 10 years. One account per girl and up to two per family (three for twins or triplets).
  - q: Can I withdraw before maturity?
    a: Up to 50% of the balance after the girl turns 18, for higher education. The account can be closed early for her marriage after 18.
related: [finance/ppf, finance/sip, finance/savings-goal, finance/nsc, finance/inflation]
''', f'''
## How to use this calculator

Enter the amount you will deposit **each year**, the **interest rate** (currently 8.2%) and your daughter's **age** when you open the account. The calculator shows the maturity value, the total deposited, the interest and her age at maturity.

## The SSY formula

Deposits are made for 15 years. The balance then grows for 6 more years without deposits until maturity at 21 years:

<p class="formula">F = P × [((1 + r)<sup>15</sup> − 1) ÷ r] × (1 + r) × (1 + r)<sup>6</sup></p>

This assumes each year's deposit is made at the start of the financial year (by 5 April) so it earns a full year's interest.

## Worked example

₹1,50,000 a year at 8.2%:

- Deposited = 1,50,000 × 15 = **₹22,50,000**
- Balance after 15 years = **{inr(150000*((1.082**15-1)/.082)*1.082)}**
- Maturity after 21 years = **{inr(s1)}**
- Tax-free interest = **{inr(s1-2250000)}**

## Maturity for different deposits (8.2%)

| Yearly deposit | Monthly equivalent | Total deposited | Maturity |
|---|---|---|---|
''' + ''.join(f"| {inr(P)} | {inr(P/12)} | {inr(15*P)} | {inr(ssy(P,.082))} |\n" for P in [12000, 25000, 50000, 100000, 150000]) + f'''
## Key SSY rules

- **Deposit**: minimum ₹250, maximum ₹1,50,000 per financial year.
- **Deposit period**: 15 years. **Maturity**: 21 years from opening.
- **Missed deposit**: ₹50 penalty per year to revive the account.
- **Tax**: EEE — deposits qualify under 80C (old regime), interest and maturity are tax-free.
- **Where**: any post office or authorised bank.

## SSY vs PPF

| | SSY | PPF |
|---|---|---|
| Rate (Oct–Dec 2026) | 8.2% | 7.1% |
| Who | Girl child below 10 | Any resident individual |
| Deposits | 15 years | 15 years |
| Maturity | 21 years | 15 years (extendable) |
| Tax | EEE | EEE |

SSY pays more than PPF, so it is usually the better choice when saving for a daughter's education or marriage.

## Keep in mind

The rate can change every quarter, so the actual maturity may differ. Deposit early in the financial year to earn the most interest.
''')

# ---------------------------------------------------------------- NSC
def nsc(P, r): return P*(1+r)**5
page('finance', 'nsc', f'''
title: NSC Calculator (National Savings Certificate)
description: Calculate NSC maturity value and interest at the current 7.7% rate for the 5-year post office National Savings Certificate.
category: finance
keywords: [nsc calculator, national savings certificate calculator, nsc interest rate, nsc maturity, post office nsc, nsc 7.7, nsc tax benefit]
updated: {D}
variables:
  - {{ id: P, label: Investment amount, family: currency, prefix: '₹', default: 100000, min: 0, decimals: 0 }}
  - {{ id: r, label: Interest rate, family: percent, unit: '%', default: 7.7, min: 0.0001, max: 0.3 }}
  - {{ id: n, label: Tenure, family: none, suffix: years, default: 5, min: 1 }}
  - {{ id: F, label: Maturity value, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: I, label: Interest earned, family: currency, prefix: '₹', decimals: 0 }}
equations:
  - F = P*(1 + r)^n
  - I = F - P
faq:
  - q: What is the current NSC interest rate?
    a: 7.7% a year, compounded annually and paid at maturity, for October–December 2026. The rate on the day you buy is locked for 5 years.
  - q: What will ₹1 lakh in NSC become?
    a: About {inr(nsc(1e5,.077))} after 5 years at 7.7%, earning about {inr(nsc(1e5,.077)-1e5)} in interest.
  - q: Is NSC interest taxable?
    a: Yes, at maturity it is taxed at your slab rate. Under the old regime, the yearly accrued interest for the first 4 years counts as reinvested and qualifies for 80C.
  - q: Can I withdraw NSC early?
    a: Only on the holder’s death, a court order or forfeiture by a pledgee. Otherwise it is locked for 5 years.
related: [finance/fd, finance/ppf, finance/post-office-mis, finance/compound-interest, finance/sukanya-samriddhi]
''', f'''
## How to use this calculator

Enter the **amount** you will invest in NSC and the **interest rate** (currently 7.7%). The tenure is fixed at 5 years. The calculator shows the maturity value and the interest earned.

## The NSC formula

<p class="formula">F = P × (1 + r)<sup>5</sup></p>

Interest compounds annually but is paid only at maturity.

## Worked example

₹1,00,000 at 7.7% for 5 years:

| Year | Interest for the year | Balance |
|---|---|---|
''' + ''.join(f"| {y} | {inr(nsc(1e5,.077)**0 * 1e5*1.077**(y-1)*.077)} | {inr(1e5*1.077**y)} |\n" for y in range(1, 6)) + f'''
Maturity = **{inr(nsc(1e5,.077))}**, interest = **{inr(nsc(1e5,.077)-1e5)}**.

## NSC at a glance

- **Minimum**: ₹1,000, in multiples of ₹100. **No maximum.**
- **Tenure**: 5 years.
- **Tax**: deposit up to ₹1.5 lakh qualifies under 80C (old regime). Interest is taxable at maturity, but the yearly accrued interest for years 1–4 also qualifies for 80C.
- **Safety**: backed by the Government of India.
- **Where**: any post office, online through India Post internet banking.

## NSC vs tax-saving FD vs PPF

| | NSC | Tax-saving FD | PPF |
|---|---|---|---|
| Lock-in | 5 years | 5 years | 15 years |
| Rate | 7.7% | Bank rate | 7.1% |
| Interest taxable | Yes | Yes | No |

## Keep in mind

NSC suits people in the old regime who want a guaranteed return with a 5-year lock-in. In the new regime, the 80C benefit does not apply.
''')

# ---------------------------------------------------------------- POMIS
page('finance', 'post-office-mis', f'''
title: Post Office Monthly Income Scheme Calculator (POMIS)
description: Calculate monthly income from the Post Office MIS at the current 7.4% rate, plus total interest over 5 years.
category: finance
keywords: [post office mis calculator, pomis calculator, monthly income scheme, post office monthly income, mis interest rate, mis 7.4, post office scheme]
updated: {D}
variables:
  - {{ id: P, label: Deposit amount, family: currency, prefix: '₹', default: 900000, min: 0, max: 1500000, decimals: 0, help: 'Up to ₹9 lakh in a single account or ₹15 lakh in a joint account.' }}
  - {{ id: r, label: Interest rate, family: percent, unit: '%', default: 7.4, min: 0.0001, max: 0.3 }}
  - {{ id: Mi, label: Monthly income, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: Yi, label: Yearly income, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: Ti, label: Total interest in 5 years, family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - Mi = P*r/12
  - Yi = P*r
  - Ti = P*r*5
faq:
  - q: What is the Post Office MIS interest rate?
    a: 7.4% a year, paid monthly, for October–December 2026. The rate is fixed for the full 5 years once you invest.
  - q: How much monthly income do I get on ₹9 lakh?
    a: ₹9,00,000 × 7.4% ÷ 12 = ₹5,550 a month, or ₹66,600 a year.
  - q: What is the maximum investment in POMIS?
    a: ₹9 lakh in a single account and ₹15 lakh in a joint account (up to 3 adults).
  - q: Is MIS interest taxable?
    a: Yes, at your slab rate. There is no TDS, so include it in your tax return.
  - q: Can I close MIS early?
    a: After 1 year. Closing between 1 and 3 years costs 2% of the deposit; between 3 and 5 years, 1%.
related: [finance/fd, finance/swp, finance/nsc, finance/rd, finance/simple-interest]
''', f'''
## How to use this calculator

Enter the **deposit amount** and the **interest rate** (currently 7.4%). The calculator shows the monthly income, the yearly income and the total interest over the 5-year term. You get your deposit back at maturity.

To find the deposit needed for a target monthly income, press × on Deposit amount and type the monthly income you want.

## The formula

<p class="formula">Monthly income = Deposit × Rate ÷ 12</p>

POMIS pays **simple interest** every month. It does not compound unless you reinvest the payouts yourself, for example into a post office RD.

## Monthly income at 7.4%

| Deposit | Monthly income | Yearly income | 5-year interest |
|---|---|---|---|
''' + ''.join(f"| {inr(P)} | {inr(P*.074/12)} | {inr(P*.074)} | {inr(P*.074*5)} |\n" for P in [100000, 300000, 500000, 900000, 1500000]) + '''
## Key POMIS rules

- **Minimum**: ₹1,000. **Maximum**: ₹9 lakh single, ₹15 lakh joint.
- **Tenure**: 5 years.
- **Payout**: monthly, to your post office savings account.
- **Premature closure**: allowed after 1 year with a 1–2% penalty.
- **Tax**: interest taxable at slab rate, no 80C benefit.

## POMIS vs SCSS vs FD for regular income

| | POMIS | SCSS | Bank FD (non-cumulative) |
|---|---|---|---|
| Rate (Oct–Dec 2026) | 7.4% | 8.2% | Varies |
| Who | Any resident adult | Age 60+ (55+ for some retirees) | Anyone |
| Payout | Monthly | Quarterly | Monthly / quarterly |
| Limit | ₹9 / ₹15 lakh | ₹30 lakh | No limit |

Senior citizens usually earn more in SCSS. POMIS suits younger people who want a guaranteed monthly income.

## Keep in mind

- The monthly payout does not rise with inflation.
- Reinvesting the payouts into an [RD](/finance/rd/) turns POMIS into a compounding investment.
''')
print('india2 done')
