import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
from inr import inr, lakh
D = '2026-10-27'

# ---------------------------------------------------------------- EMI
def emi(P, r, y):
    i = r / 12; n = 12 * y
    return P * i * (1 + i) ** n / ((1 + i) ** n - 1)
e1 = emi(3_000_000, 0.085, 20); rows = ''
for P, r, y, name in [(3_000_000, .085, 20, 'Home loan'), (800_000, .095, 5, 'Car loan'), (500_000, .12, 3, 'Personal loan'), (1_000_000, .10, 7, 'Education loan')]:
    m = emi(P, r, y); rows += f"| {name} | {inr(P)} | {r*100:g}% | {y} years | {inr(m)} | {inr(m*12*y-P)} |\n"
tenure = ''
for y in [10, 15, 20, 25, 30]:
    m = emi(3_000_000, .085, y); tenure += f"| {y} years | {inr(m)} | {inr(m*12*y-3_000_000)} | {inr(m*12*y)} |\n"
page('finance', 'emi', f'''
title: EMI Calculator (Home, Car and Personal Loan)
description: Calculate your loan EMI, total interest and total payment for home, car, personal or education loans — in rupees, with a chart.
category: finance
keywords: [emi calculator, home loan emi calculator, car loan emi, personal loan emi, loan emi, emi formula, sbi home loan emi, monthly installment]
updated: {D}
featured: true
variables:
  - {{ id: P, label: Loan amount, family: currency, prefix: '₹', default: 3000000, min: 0, decimals: 0 }}
  - {{ id: r, label: Interest rate (per year), family: percent, unit: '%', default: 8.5, min: 0.0001, max: 1 }}
  - {{ id: t, label: Loan tenure, family: time, unit: yr, default: 20, min: 0.0833 }}
  - {{ id: E, label: Monthly EMI, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: I, label: Total interest payable, family: currency, prefix: '₹', decimals: 0 }}
  - {{ id: T, label: Total payment (principal + interest), family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - E = P * (r/12) * (1 + r/12)^(12*t) / ((1 + r/12)^(12*t) - 1)
  - T = E * 12 * t
  - I = T - P
chart: {{ x: t, y: E, from: 1, to: 30 }}
faq:
  - q: What is the formula for EMI?
    a: EMI = P × r × (1 + r)ⁿ ÷ ((1 + r)ⁿ − 1), where P is the loan amount, r the monthly interest rate (annual rate ÷ 12 ÷ 100) and n the number of monthly instalments.
  - q: What is the EMI on a ₹30 lakh home loan for 20 years?
    a: At 8.5% a year the EMI is about {inr(e1)} per month. Over 20 years you pay about {inr(e1*240-3e6)} in interest.
  - q: Does a longer tenure reduce EMI?
    a: Yes, but it increases the total interest. Going from 20 to 30 years on ₹30 lakh at 8.5% cuts the EMI by about {inr(e1-emi(3e6,.085,30))} but adds about {inr(emi(3e6,.085,30)*360-e1*240)} of interest.
  - q: How much loan can I get for a given EMI?
    a: Press × on Loan amount, then type the EMI you can afford along with the rate and tenure. The calculator works out the loan amount.
  - q: Does prepayment reduce EMI or tenure?
    a: Banks usually keep the EMI the same and shorten the tenure, which saves the most interest. You can ask them to reduce the EMI instead.
  - q: Are processing fees included?
    a: No. Processing fees, insurance and GST on fees are extra. Add them to compare the real cost of different offers.
related: [finance/loan-payment, finance/mortgage, finance/simple-interest, finance/compound-interest, finance/sip]
''', f'''
## How to use this calculator

Enter the **loan amount**, the **interest rate** your bank quotes and the **tenure** in years. The calculator shows your monthly EMI, the total interest and the total amount you will repay. Change any value and the results update instantly.

It works in every direction. To find the loan you can afford, press × on Loan amount and type the EMI you are comfortable with. To check what rate a lender is really charging, enter the loan, EMI and tenure and press × on the rate.

## The EMI formula

<p class="formula">EMI = P × r × (1 + r)<sup>n</sup> ÷ ((1 + r)<sup>n</sup> − 1)</p>

- **P** = loan amount (principal)
- **r** = monthly interest rate = annual rate ÷ 12 ÷ 100
- **n** = number of monthly instalments = years × 12

Each EMI has two parts: interest on the outstanding balance and a repayment of principal. In the early years most of the EMI goes to interest. As the balance falls, more of each EMI repays the loan.

## Worked example

A home loan of **₹30,00,000** at **8.5%** for **20 years**:

- Monthly rate r = 8.5 ÷ 12 ÷ 100 = 0.007083
- Number of EMIs n = 20 × 12 = 240
- EMI = **{inr(e1)}**
- Total payment = {inr(e1)} × 240 = **{inr(e1*240)}**
- Total interest = **{inr(e1*240-3e6)}**

The interest is more than the loan itself, which is normal for a 20-year home loan.

## EMI for common loans

| Loan type | Amount | Rate | Tenure | EMI | Total interest |
|---|---|---|---|---|---|
{rows}
## How tenure changes your EMI

₹30 lakh at 8.5%:

| Tenure | EMI | Total interest | Total payment |
|---|---|---|---|
{tenure}
A longer tenure lowers the EMI but the total interest climbs steeply. Choose the shortest tenure whose EMI fits comfortably in your budget.

## How to reduce your loan cost

- **Prepay early.** A prepayment in the first few years saves far more interest than the same amount later. Floating-rate home loans for individuals have no prepayment penalty in India.
- **Increase the EMI with your salary.** Raising the EMI by 5–10% each year can cut a 20-year loan by several years.
- **Compare the rate, not just the EMI.** A small difference of 0.5% on ₹30 lakh over 20 years is worth roughly {inr((emi(3e6,.09,20)-e1)*240)}.
- **Check the reset clause.** Floating rates move with the repo rate, so your EMI or tenure can change.

## Keep in mind

- Most lenders want total EMIs below about 40–50% of your take-home pay.
- Interest on a home loan may be deductible under the old tax regime. Check current rules with a tax adviser.
- This is an estimate. Your bank's schedule may differ slightly because of rounding and the date the loan starts.
''')

# ---------------------------------------------------------------- GST
g18 = 10000 * .18
page('finance', 'gst', f'''
title: GST Calculator (Add or Remove GST)
description: Add GST to a price or remove GST from an inclusive amount. Shows CGST, SGST and the total at 5%, 18%, 40% and other GST rates.
category: finance
keywords: [gst calculator, gst calculation, gst inclusive, gst exclusive, reverse gst, cgst sgst, igst, gst 18 percent, gst 5 percent, gst 2.0]
updated: {D}
featured: true
variables:
  - {{ id: A, label: Amount, family: currency, prefix: '₹', default: 10000, min: 0, decimals: 2 }}
  - id: g
    label: GST rate
    default: 0.18
    options:
      - {{ label: '5%', value: 0.05 }}
      - {{ label: '18%', value: 0.18 }}
      - {{ label: '40%', value: 0.4 }}
      - {{ label: '3% (gold, silver, jewellery)', value: 0.03 }}
      - {{ label: '12% (specified items)', value: 0.12 }}
      - {{ label: '28% (specified items)', value: 0.28 }}
      - {{ label: '0.25% (rough diamonds)', value: 0.0025 }}
  - id: m
    label: The amount is
    default: 1
    options:
      - {{ label: Before GST (add GST), value: 1 }}
      - {{ label: Including GST (remove GST), value: 0 }}
  - {{ id: B, label: Price before GST, family: currency, prefix: '₹', min: 0, decimals: 2 }}
  - {{ id: G, label: GST amount, family: currency, prefix: '₹', min: 0, decimals: 2 }}
  - {{ id: C, label: CGST (half), family: currency, prefix: '₹', min: 0, decimals: 2 }}
  - {{ id: S, label: SGST / UTGST (half), family: currency, prefix: '₹', min: 0, decimals: 2 }}
  - {{ id: T, label: Price including GST, family: currency, prefix: '₹', min: 0, decimals: 2 }}
equations:
  - B = m * A + (1 - m) * A / (1 + g)
  - G = B * g
  - C = G / 2
  - S = G / 2
  - T = B + G
faq:
  - q: How do I calculate GST on an amount?
    a: Multiply the price before GST by the rate. ₹10,000 at 18% gives GST of ₹1,800 and a total of ₹11,800.
  - q: How do I remove GST from an inclusive price?
    a: Divide the inclusive price by (1 + rate). ₹11,800 ÷ 1.18 = ₹10,000, so the GST in it is ₹1,800. Choose “Including GST” in the calculator to do this.
  - q: What are the GST rates in India now?
    a: Since GST 2.0 took effect on 22 September 2025 the main slabs are 5% and 18%, with 40% for luxury and sin goods. Special rates such as 3% for gold and 0.25% for rough diamonds still apply, and some items are exempt.
  - q: What is the difference between CGST, SGST and IGST?
    a: Within a state, GST is split equally into CGST (central) and SGST (state). For sales between states the full amount is charged as IGST.
  - q: Is 18% GST split as 9% CGST and 9% SGST?
    a: Yes, for an intra-state sale. For an inter-state sale it is 18% IGST.
related: [finance/sales-tax-vat, finance/discount, finance/profit-margin, finance/income-tax-india]
''', f'''
## How to use this calculator

1. Enter the **amount**.
2. Pick the **GST rate** that applies to the product or service.
3. Choose whether the amount is **before GST** (you want to add GST) or **including GST** (you want to find the GST inside it).

You get the price before GST, the GST amount, the CGST and SGST split and the final price.

## GST formulas

**Adding GST**

<p class="formula">GST = Price × Rate &nbsp;·&nbsp; Total = Price × (1 + Rate)</p>

**Removing GST (reverse calculation)**

<p class="formula">Price before GST = Inclusive price ÷ (1 + Rate)</p>

A common mistake is to take 18% of the inclusive price. On ₹11,800 that gives ₹2,124, which is wrong. The GST inside ₹11,800 is only ₹1,800.

## Worked examples

**Adding 18% GST to ₹10,000**

- GST = 10,000 × 0.18 = **₹1,800**
- CGST = ₹900, SGST = ₹900
- Total = **₹11,800**

**Removing 5% GST from ₹2,100**

- Price before GST = 2,100 ÷ 1.05 = **₹2,000**
- GST = **₹100** (₹50 CGST + ₹50 SGST)

## GST on ₹10,000 at each rate

| Rate | GST | Total price |
|---|---|---|
| 5% | ₹500 | ₹10,500 |
| 18% | ₹1,800 | ₹11,800 |
| 40% | ₹4,000 | ₹14,000 |
| 3% | ₹300 | ₹10,300 |

## Current GST slabs in India

GST 2.0, effective **22 September 2025**, simplified the structure:

- **0% (exempt)**: many essentials, education and healthcare services, individual life and health insurance.
- **5%**: everyday essentials and many key inputs.
- **18%**: the standard rate for most goods and services.
- **40%**: luxury and sin goods.
- **Special rates**: 3% on gold, silver and jewellery, 0.25% on rough diamonds and a few others.

Rates for a specific item depend on its HSN or SAC code. Check the CBIC rate notifications or your accountant for the exact rate.

## CGST, SGST and IGST

- **Intra-state sale** (seller and buyer in the same state): GST is split equally, half CGST and half SGST (or UTGST in a union territory).
- **Inter-state sale** or import: the full rate is charged as **IGST**.

The total tax is the same either way. Only the split and who receives the tax change.

## Keep in mind

- Registered businesses can usually claim input tax credit for GST paid on purchases.
- Round the final invoice as your billing software requires.
- This calculator is for estimates. Use official notifications for filing and compliance.
''')

# ---------------------------------------------------------------- PPF
def ppf(P, r, n): return P * ((1 + r) ** n - 1) / r * (1 + r)
p15 = ppf(150000, .071, 15); rows = ''
for P in [12000, 50000, 100000, 150000]:
    f = ppf(P, .071, 15); rows += f"| {inr(P)} | {inr(P*15)} | {inr(f)} | {inr(f-P*15)} |\n"
ext = ''
for n in [15, 20, 25, 30]:
    f = ppf(150000, .071, n); ext += f"| {n} years | {inr(150000*n)} | {inr(f)} |\n"
page('finance', 'ppf', f'''
title: PPF Calculator (Public Provident Fund)
description: Calculate PPF maturity value and interest for yearly deposits at the current 7.1% rate — including 5-year extensions after 15 years.
category: finance
keywords: [ppf calculator, public provident fund calculator, ppf interest rate, ppf maturity, ppf 15 years, ppf extension, post office ppf, sbi ppf]
updated: {D}
featured: true
variables:
  - {{ id: P, label: Yearly deposit, family: currency, prefix: '₹', default: 150000, min: 0, decimals: 0, help: 'Between ₹500 and ₹1,50,000 per financial year.' }}
  - {{ id: r, label: Interest rate, family: percent, unit: '%', default: 7.1, min: 0.0001, max: 0.5 }}
  - {{ id: n, label: Duration, family: time, unit: yr, default: 15, min: 1, help: '15 years, extendable in blocks of 5 years.' }}
  - {{ id: F, label: Maturity value, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: inv, label: Total deposited, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: I, label: Total interest earned, family: currency, prefix: '₹', decimals: 0 }}
equations:
  - F = P * ((1 + r)^n - 1) / r * (1 + r)
  - inv = P * n
  - I = F - inv
chart: {{ x: n, y: F, from: 15, to: 40 }}
faq:
  - q: What is the current PPF interest rate?
    a: 7.1% a year, compounded annually, for the October–December 2026 quarter. The government reviews small savings rates every quarter.
  - q: What will ₹1.5 lakh a year in PPF become in 15 years?
    a: At 7.1% it grows to about {inr(p15)}. You deposit ₹22,50,000 and earn about {inr(p15-2250000)} in interest, all tax-free.
  - q: What is the PPF lock-in period?
    a: 15 full financial years from the end of the year you open it. Partial withdrawals are allowed from the 7th year and loans from the 3rd to 6th year.
  - q: Is PPF interest taxable?
    a: No. PPF has EEE status — deposits qualify for deduction under the old regime (up to ₹1.5 lakh), and interest and maturity are tax-free.
  - q: When should I deposit to earn the most interest?
    a: Before the 5th of the month. Interest is calculated on the lowest balance between the 5th and the end of each month, so a deposit by 5 April earns interest for the full year.
  - q: Can I extend PPF after 15 years?
    a: Yes, in blocks of 5 years, with or without further deposits. Set Duration to 20, 25 or 30 years to see the effect.
related: [finance/sukanya-samriddhi, finance/epf, finance/nsc, finance/sip, finance/compound-interest]
''', f'''
## How to use this calculator

Enter the amount you will deposit **each financial year**, the **interest rate** (currently 7.1%) and the **duration** (15 years, or 20, 25 or 30 with extensions). The calculator shows the maturity value, the total you deposited and the interest earned.

To find the yearly deposit needed for a goal, press × on Yearly deposit and type the maturity value you want.

## The PPF formula

<p class="formula">F = P × [((1 + r)<sup>n</sup> − 1) ÷ r] × (1 + r)</p>

- **P** = yearly deposit
- **r** = annual interest rate (7.1% = 0.071)
- **n** = number of years

The formula assumes you deposit at the **start** of each financial year (by 5 April), so every deposit earns a full year of interest. Interest is compounded once a year, on 31 March.

## Worked example

₹1,50,000 every year for 15 years at 7.1%:

- Total deposited = 1,50,000 × 15 = **₹22,50,000**
- Maturity value = **{inr(p15)}**
- Interest earned = **{inr(p15-2250000)}** (tax-free)

## Maturity for different deposits (15 years, 7.1%)

| Yearly deposit | Total deposited | Maturity value | Interest |
|---|---|---|---|
{rows}
## The power of extending

Depositing ₹1.5 lakh a year at 7.1%:

| Duration | Total deposited | Maturity value |
|---|---|---|
{ext}
The last 15 years of a 30-year PPF earn far more than the first 15. If you do not need the money at maturity, extending is one of the best risk-free, tax-free options.

## PPF rules at a glance

- **Minimum deposit**: ₹500 a year. **Maximum**: ₹1,50,000 a year.
- **Tenure**: 15 years, extendable in blocks of 5 years.
- **Loan**: from the 3rd to the 6th year, up to 25% of the balance.
- **Partial withdrawal**: from the 7th year, once a year.
- **Tax**: EEE — deduction under the old regime, tax-free interest and maturity.
- **Who can open**: resident Indian individuals, one account per person. NRIs cannot open a new account.

## Keep in mind

- The rate can change every quarter. The calculator uses one rate for the whole period, so treat the result as an estimate.
- Monthly deposits made after the 5th earn less than this calculator shows.
- Compare with the [SIP calculator](/finance/sip/) for market-linked growth and the [Sukanya Samriddhi calculator](/finance/sukanya-samriddhi/) if you are saving for a daughter.
''')

# ---------------------------------------------------------------- FD
def fd(P, r, k, t): return P * (1 + r / k) ** (k * t)
f1 = fd(100000, .07, 4, 5); rows = ''
for t in [1, 2, 3, 5, 10]:
    f = fd(100000, .07, 4, t); rows += f"| {t} year{'s' if t>1 else ''} | {inr(f)} | {inr(f-100000)} |\n"
page('finance', 'fd', f'''
title: FD Calculator (Fixed Deposit)
description: Calculate fixed deposit maturity amount and interest with quarterly, monthly or yearly compounding — for SBI, HDFC, post office and other bank FDs.
category: finance
keywords: [fd calculator, fixed deposit calculator, fd interest calculator, fd maturity, sbi fd calculator, post office fd, quarterly compounding, term deposit]
updated: {D}
featured: true
variables:
  - {{ id: P, label: Deposit amount, family: currency, prefix: '₹', default: 100000, min: 0, decimals: 0 }}
  - {{ id: r, label: Interest rate (per year), family: percent, unit: '%', default: 7, min: 0, max: 0.5 }}
  - {{ id: t, label: Tenure, family: time, unit: yr, default: 5, min: 0 }}
  - id: k
    label: Compounding
    default: 4
    options:
      - {{ label: Quarterly (most banks), value: 4 }}
      - {{ label: Monthly, value: 12 }}
      - {{ label: Half-yearly, value: 2 }}
      - {{ label: Yearly, value: 1 }}
  - {{ id: A, label: Maturity amount, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: I, label: Interest earned, family: currency, prefix: '₹', decimals: 0 }}
  - {{ id: y, label: Effective annual yield, family: percent, unit: '%' }}
equations:
  - A = P * (1 + r/k)^(k*t)
  - I = A - P
  - y = (1 + r/k)^k - 1
chart: {{ x: t, y: A, from: 0, to: 10 }}
faq:
  - q: How is FD interest calculated?
    a: Most Indian banks compound FD interest quarterly. Maturity = P × (1 + r/4)^(4t), where P is the deposit, r the annual rate and t the tenure in years.
  - q: How much will ₹1 lakh become in an FD in 5 years?
    a: At 7% compounded quarterly it becomes about {inr(f1)}, earning about {inr(f1-1e5)} in interest.
  - q: Is FD interest taxable?
    a: Yes. FD interest is added to your income and taxed at your slab rate. Banks deduct TDS when interest crosses the yearly threshold, unless you submit Form 15G or 15H if eligible.
  - q: What is the effective yield of an FD?
    a: It is the true annual return after compounding. A 7% FD compounded quarterly yields about 7.19% a year.
  - q: Which is better, cumulative or non-cumulative FD?
    a: A cumulative FD reinvests the interest and gives the most at maturity. A non-cumulative FD pays interest out monthly or quarterly, which suits people who need regular income.
related: [finance/rd, finance/compound-interest, finance/nsc, finance/post-office-mis, finance/simple-interest]
''', f'''
## How to use this calculator

Enter the **deposit amount**, the **interest rate** offered by your bank and the **tenure**. Pick the **compounding** frequency — quarterly is standard for most Indian bank FDs. You see the maturity amount, the interest earned and the effective annual yield.

For tenures under a year, change the unit to months or days.

## The FD formula

<p class="formula">A = P × (1 + r ÷ k)<sup>k × t</sup></p>

- **P** = deposit amount
- **r** = annual interest rate (7% = 0.07)
- **k** = compounding periods per year (4 for quarterly)
- **t** = tenure in years

This is the formula for a **cumulative** FD, where interest is added back to the deposit and earns interest itself.

## Worked example

₹1,00,000 at 7% for 5 years, compounded quarterly:

- Quarterly rate = 7% ÷ 4 = 1.75%
- Number of quarters = 5 × 4 = 20
- Maturity = 1,00,000 × 1.0175<sup>20</sup> = **{inr(f1)}**
- Interest = **{inr(f1-1e5)}**

## ₹1 lakh FD at 7% (quarterly)

| Tenure | Maturity | Interest |
|---|---|---|
{rows}
## Cumulative vs non-cumulative FD

| | Cumulative | Non-cumulative |
|---|---|---|
| Interest | Reinvested, paid at maturity | Paid out monthly, quarterly or yearly |
| Best for | Growing savings | Regular income, retirees |
| Return | Higher (compounding) | Lower (no compounding) |

## Tax and TDS on FDs

- FD interest is **fully taxable** at your income tax slab rate.
- Banks deduct **TDS** when interest from one bank crosses the yearly threshold. Submit Form 15G (or 15H for senior citizens) if your income is below the taxable limit.
- A **tax-saving FD** has a 5-year lock-in and qualifies for deduction under the old regime only.

## Tips to earn more

- **Senior citizens** usually get 0.25–0.75% extra.
- **Ladder your FDs** across different tenures so some money matures every year and you can reinvest at better rates.
- Compare the **effective yield**, not just the headline rate, when banks use different compounding.

## Keep in mind

Premature withdrawal usually attracts a penalty of 0.5–1% on the rate. Deposits are insured by DICGC up to ₹5 lakh per depositor per bank.
''')

# ---------------------------------------------------------------- RD
def rd(R, r, n):
    i = r / 4; return R * ((1 + i) ** (n / 3) - 1) / (1 - (1 + i) ** (-1 / 3))
r1 = rd(5000, .07, 60); rows = ''
for n in [12, 24, 36, 60, 120]:
    m = rd(5000, .07, n); rows += f"| {n} months | {inr(5000*n)} | {inr(m)} | {inr(m-5000*n)} |\n"
page('finance', 'rd', f'''
title: RD Calculator (Recurring Deposit)
description: Calculate recurring deposit maturity and interest for monthly deposits with quarterly compounding — for banks and post office RD.
category: finance
keywords: [rd calculator, recurring deposit calculator, post office rd calculator, sbi rd calculator, rd interest, rd maturity, monthly deposit]
updated: {D}
featured: true
variables:
  - {{ id: R, label: Monthly deposit, family: currency, prefix: '₹', default: 5000, min: 0, decimals: 0 }}
  - {{ id: r, label: Interest rate (per year), family: percent, unit: '%', default: 7, min: 0.0001, max: 0.5 }}
  - {{ id: n, label: Tenure, family: none, suffix: months, default: 60, min: 1 }}
  - {{ id: M, label: Maturity amount, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: inv, label: Total deposited, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: I, label: Interest earned, family: currency, prefix: '₹', decimals: 0 }}
equations:
  - M = R * ((1 + r/4)^(n/3) - 1) / (1 - (1 + r/4)^(-1/3))
  - inv = R * n
  - I = M - inv
chart: {{ x: n, y: M, from: 6, to: 120 }}
faq:
  - q: How is RD interest calculated?
    a: Indian banks compound RD interest quarterly. Maturity = R × [(1 + i)ⁿ − 1] ÷ [1 − (1 + i)^(−1/3)], where R is the monthly deposit, i the quarterly rate (annual ÷ 4) and n the number of quarters.
  - q: What is the maturity of ₹5,000 a month RD for 5 years?
    a: At 7% it is about {inr(r1)}. You deposit ₹3,00,000 and earn about {inr(r1-300000)} in interest.
  - q: What is the post office RD interest rate?
    a: 6.7% a year for the 5-year post office RD in the October–December 2026 quarter. Enter 6.7% and 60 months.
  - q: Is RD interest taxable?
    a: Yes, at your slab rate, and TDS applies above the yearly threshold, the same as for FDs.
  - q: What happens if I miss an RD instalment?
    a: Banks charge a small penalty per missed month, and after several missed instalments the account may be closed early.
  - q: RD or SIP — which is better?
    a: RD gives a fixed, guaranteed return. A SIP in an equity fund can earn more over long periods but the return is not guaranteed.
related: [finance/fd, finance/sip, finance/savings-goal, finance/compound-interest, finance/ppf]
''', f'''
## How to use this calculator

Enter your **monthly deposit**, the **interest rate** and the **tenure in months**. The calculator shows the maturity amount, the total you deposited and the interest earned.

To save for a goal, press × on Monthly deposit and type the maturity amount you need.

## The RD formula

Banks in India compound recurring deposits **quarterly**. The standard formula is:

<p class="formula">M = R × [(1 + i)<sup>n</sup> − 1] ÷ [1 − (1 + i)<sup>−1/3</sup>]</p>

- **R** = monthly deposit
- **i** = quarterly interest rate = annual rate ÷ 4
- **n** = number of quarters = months ÷ 3

Each monthly deposit earns compound interest from the month it is paid until maturity, so the first instalment earns the most.

## Worked example

₹5,000 a month for 5 years (60 months) at 7%:

- Quarterly rate = 7% ÷ 4 = 1.75%
- Number of quarters = 60 ÷ 3 = 20
- Total deposited = 5,000 × 60 = **₹3,00,000**
- Maturity = **{inr(r1)}**
- Interest earned = **{inr(r1-300000)}**

## ₹5,000 a month at 7%

| Tenure | Deposited | Maturity | Interest |
|---|---|---|---|
{rows}
## RD vs FD

| | RD | FD |
|---|---|---|
| Deposit | Fixed amount every month | One lump sum |
| Best for | Saving from monthly income | Money you already have |
| Interest | Lower total (later deposits earn less) | Higher on the same total |
| Rate | Usually same as FD for the tenure | — |

## Bank RD vs post office RD

- **Bank RD**: tenure from 6 months to 10 years, rates vary by bank, extra for senior citizens.
- **Post office RD**: fixed 5-year tenure, government-backed, currently 6.7% compounded quarterly.

## Keep in mind

- Interest is taxable at your slab rate.
- Pay on time. Late instalments attract a penalty.
- The calculator assumes the rate stays the same for the whole tenure, which it does for a bank RD once opened.
''')

# ---------------------------------------------------------------- Lumpsum
def ls(P, r, t): return P * (1 + r) ** t
l1 = ls(100000, .12, 10); rows = ''
for t in [5, 10, 15, 20, 25]:
    rows += f"| {t} years | {inr(ls(100000,.08,t))} | {inr(ls(100000,.10,t))} | {inr(ls(100000,.12,t))} |\n"
page('finance', 'lumpsum', f'''
title: Lumpsum Calculator (One-Time Investment)
description: See how a one-time mutual fund investment grows over time — maturity value, gains and CAGR — or find the lump sum needed for a goal.
category: finance
keywords: [lumpsum calculator, lump sum investment calculator, mutual fund lumpsum, one time investment, lumpsum returns, lumpsum vs sip]
updated: {D}
variables:
  - {{ id: P, label: Investment amount, family: currency, prefix: '₹', default: 100000, min: 0, decimals: 0 }}
  - {{ id: r, label: Expected return (per year), family: percent, unit: '%', default: 12, min: -0.99, max: 1 }}
  - {{ id: t, label: Time period, family: time, unit: yr, default: 10, min: 0 }}
  - {{ id: F, label: Estimated value, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: G, label: Estimated gain, family: currency, prefix: '₹', decimals: 0 }}
  - {{ id: X, label: Growth multiple, family: none, suffix: '×', decimals: 2 }}
equations:
  - F = P * (1 + r)^t
  - G = F - P
  - X = F / P
chart: {{ x: t, y: F, from: 1, to: 30 }}
faq:
  - q: How is lumpsum return calculated?
    a: Future value = P × (1 + r)^t, where P is the amount invested, r the expected annual return and t the number of years.
  - q: What will ₹1 lakh become in 10 years at 12%?
    a: About {inr(l1)} — a gain of about {inr(l1-1e5)}, or {l1/1e5:.2f} times the money.
  - q: Lumpsum or SIP — which is better?
    a: A lump sum earns more when markets rise steadily after you invest. A SIP spreads purchases over time and reduces the risk of investing everything at a market peak.
  - q: How long will it take to double my money?
    a: Press × on Time and set Estimated value to twice the investment. At 12% it takes about 6.1 years. The rule of 72 gives a quick estimate — 72 ÷ 12 = 6.
related: [finance/sip, finance/step-up-sip, finance/cagr, finance/compound-interest, finance/doubling-time]
''', f'''
## How to use this calculator

Enter the **amount** you will invest once, the **expected annual return** and the **time period**. You see the estimated value, the gain and how many times your money has grown.

To find how much to invest today for a future goal, press × on Investment amount and type the target value.

## The formula

<p class="formula">F = P × (1 + r)<sup>t</sup></p>

- **P** = amount invested
- **r** = expected annual return (12% = 0.12)
- **t** = years

The return **r** is the compound annual growth rate (CAGR). Mutual fund factsheets show past CAGR over 1, 3, 5 and 10 years.

## Worked example

₹1,00,000 invested for 10 years at 12% a year:

- Value = 1,00,000 × 1.12<sup>10</sup> = **{inr(l1)}**
- Gain = **{inr(l1-1e5)}**
- Growth multiple = **{l1/1e5:.2f}×**

## ₹1 lakh at different returns

| Years | 8% | 10% | 12% |
|---|---|---|---|
{rows}
Small differences in return make a large difference over long periods. That is why fund costs (expense ratio) matter.

## Typical return assumptions

| Investment | Long-term return (assumption) |
|---|---|
| Large-cap equity fund | 10–12% |
| Flexi-cap / mid-cap fund | 11–14% |
| Hybrid fund | 8–10% |
| Debt fund | 6–8% |

These are rough planning figures, not promises. Past returns do not guarantee future returns.

## Lumpsum vs SIP

- **Lumpsum** suits money you already have, such as a bonus or maturity proceeds, especially for long horizons.
- **SIP** suits monthly income and reduces timing risk. Compare with the [SIP calculator](/finance/sip/).
- A middle path is an **STP** — park the lump sum in a liquid fund and transfer it into equity over 6–12 months.

## Keep in mind

Gains are taxed as capital gains when you sell. Equity fund gains held over a year are long-term and taxed at a lower rate above an annual exemption limit.
''')

# ---------------------------------------------------------------- Step-up SIP
def ssip(M, s, r, Y):
    i = r / 12; A = ((1 + i) ** 12 - 1) / i * (1 + i); R = (1 + i) ** 12
    return M * A * (R ** Y - (1 + s) ** Y) / (R - (1 + s))
def sip(M, r, Y):
    i = r / 12; return M * ((1 + i) ** (12 * Y) - 1) / i * (1 + i)
s1 = ssip(10000, .10, .12, 20); p1 = sip(10000, .12, 20); inv1 = 12 * 10000 * ((1.1) ** 20 - 1) / .1
rows = ''
for s in [0.0001, .05, .10, .15]:
    f = ssip(10000, s, .12, 20); iv = 12 * 10000 * ((1 + s) ** 20 - 1) / s
    rows += f"| {round(s*100)}% | {inr(iv)} | {inr(f)} |\n"
page('finance', 'step-up-sip', f'''
title: Step-Up SIP Calculator (Top-Up SIP)
description: See how increasing your SIP amount every year boosts your corpus. Compare step-up SIP vs regular SIP with total invested and returns.
category: finance
keywords: [step up sip calculator, top up sip calculator, sip with annual increase, incremental sip, step-up sip vs sip, sip step up]
updated: {D}
variables:
  - {{ id: M, label: Starting monthly SIP, family: currency, prefix: '₹', default: 10000, min: 0, decimals: 0 }}
  - {{ id: s, label: Annual step-up, family: percent, unit: '%', default: 10, min: 0.0001, max: 1 }}
  - {{ id: r, label: Expected return (per year), family: percent, unit: '%', default: 12, min: 0.0001, max: 1 }}
  - {{ id: Y, label: Investment period, family: none, suffix: years, default: 20, min: 1 }}
  - {{ id: F, label: Estimated corpus, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: inv, label: Total invested, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: G, label: Estimated returns, family: currency, prefix: '₹', decimals: 0 }}
  - {{ id: last, label: Monthly SIP in final year, family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - F = M * ((1 + r/12)^12 - 1) / (r/12) * (1 + r/12) * (((1 + r/12)^(12*Y) - (1 + s)^Y) / ((1 + r/12)^12 - (1 + s)))
  - inv = 12 * M * ((1 + s)^Y - 1) / s
  - G = F - inv
  - last = M * (1 + s)^(Y - 1)
chart: {{ x: Y, y: F, from: 1, to: 30 }}
faq:
  - q: What is a step-up SIP?
    a: A SIP where you raise the monthly amount by a fixed percentage every year, usually in line with your salary increase. It is also called a top-up SIP.
  - q: How much more does a step-up SIP give?
    a: ₹10,000 a month for 20 years at 12% gives about {inr(p1)} as a flat SIP. With a 10% yearly step-up it grows to about {inr(s1)}.
  - q: What step-up percentage should I choose?
    a: Match it to your expected salary growth — 5–10% is common. Even 5% makes a big difference over 15–20 years.
  - q: How is the step-up SIP corpus calculated?
    a: Each year's 12 monthly instalments are valued like a normal SIP, then grown to the end of the period. Adding up all years gives a geometric series, which the calculator sums exactly.
related: [finance/sip, finance/lumpsum, finance/swp, finance/retirement-corpus, finance/inflation]
''', f'''
## How to use this calculator

Enter your **starting monthly SIP**, the **annual step-up** (how much you will raise it each year), the **expected return** and the **period in years**. The calculator shows the final corpus, how much you invested in total, the returns and what your SIP will be in the final year.

## The formula

Each year's 12 instalments are worth, at the end of that year:

<p class="formula">A = M<sub>k</sub> × [((1 + i)<sup>12</sup> − 1) ÷ i] × (1 + i)</p>

where M<sub>k</sub> = M × (1 + s)<sup>k</sup> is the SIP in year k and i = annual return ÷ 12. Growing each year's value to the end and summing gives:

<p class="formula">F = M × A₁ × [(1 + i)<sup>12Y</sup> − (1 + s)<sup>Y</sup>] ÷ [(1 + i)<sup>12</sup> − (1 + s)]</p>

## Worked example

Start at ₹10,000 a month, step up 10% a year, 12% return, 20 years:

- Final-year SIP = 10,000 × 1.1<sup>19</sup> = **{inr(10000*1.1**19)}** a month
- Total invested = **{inr(inv1)}**
- Corpus = **{inr(s1)}**

A flat ₹10,000 SIP for the same 20 years gives only **{inr(p1)}** from ₹24,00,000 invested.

## Effect of the step-up rate

₹10,000 starting SIP, 12% return, 20 years:

| Annual step-up | Total invested | Corpus |
|---|---|---|
{rows}
## Why step-up works

- **Your income grows**, so a fixed SIP becomes a smaller share of your salary every year.
- **Inflation erodes a fixed SIP.** ₹10,000 today buys much less in 15 years.
- **More money goes in while there is still time to compound**, especially in the middle years.

## Keep in mind

- Most fund houses let you set an automatic top-up when you start the SIP, by amount or percentage.
- Returns are not guaranteed. Use a conservative return such as 10–12% for equity funds.
- Adjust your goal for inflation with the [inflation calculator](/finance/inflation/).
''')

# ---------------------------------------------------------------- SWP
def swp(P, W, r, t):
    i = r / 12; n = 12 * t; return P * (1 + i) ** n - W * ((1 + i) ** n - 1) / i
import math
b1 = swp(5000000, 30000, .08, 15)
def lasts(P, W, r):
    i = r / 12
    if W <= P * i: return None
    return -math.log(1 - P * i / W) / math.log(1 + i) / 12
rows = ''
for W in [25000, 35000, 45000, 55000]:
    L = lasts(5000000, W, .08); rows += f"| {inr(W)} | {inr(W*12)} | {'forever' if L is None else f'{L:.1f} years'} |\n"
page('finance', 'swp', f'''
title: SWP Calculator (Systematic Withdrawal Plan)
description: Plan monthly withdrawals from a mutual fund corpus — see the balance left, total withdrawn and how long your money will last.
category: finance
keywords: [swp calculator, systematic withdrawal plan, swp mutual fund, monthly income from mutual fund, retirement withdrawal, how long will my money last]
updated: {D}
variables:
  - {{ id: P, label: Total investment (corpus), family: currency, prefix: '₹', default: 5000000, min: 0, decimals: 0 }}
  - {{ id: W, label: Monthly withdrawal, family: currency, prefix: '₹', default: 30000, min: 0, decimals: 0 }}
  - {{ id: r, label: Expected return (per year), family: percent, unit: '%', default: 8, min: 0.0001, max: 1 }}
  - {{ id: t, label: Time period, family: time, unit: yr, default: 15, min: 0 }}
  - {{ id: B, label: Balance at the end, family: currency, prefix: '₹', decimals: 0 }}
  - {{ id: Tw, label: Total withdrawn, family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - B = P * (1 + r/12)^(12*t) - W * ((1 + r/12)^(12*t) - 1) / (r/12)
  - Tw = W * 12 * t
chart: {{ x: t, y: B, from: 1, to: 30 }}
faq:
  - q: What is SWP?
    a: A Systematic Withdrawal Plan lets you withdraw a fixed amount from a mutual fund every month while the rest stays invested and keeps earning.
  - q: How long will my money last?
    a: Set Balance at the end to 0, then press × on Time period. With ₹50 lakh, ₹45,000 a month and an 8% return, the money lasts about {lasts(5e6,45000,.08):.1f} years. If you withdraw less than the monthly return, it never runs out.
  - q: What is a safe withdrawal rate?
    a: If you withdraw less than the monthly return, the corpus never runs out. At 8% that is about 0.64% of the corpus a month — ₹32,000 on ₹50 lakh — though returns vary.
  - q: How is SWP taxed?
    a: Each withdrawal is partly your own capital and partly gains. Only the gain portion is taxed as capital gains, which often makes SWP more tax-efficient than FD interest.
related: [finance/sip, finance/step-up-sip, finance/retirement-corpus, finance/post-office-mis, finance/lumpsum]
''', f'''
## How to use this calculator

Enter your **corpus**, the **monthly withdrawal** you want, the **expected return** and the **period**. The calculator shows the balance left at the end and the total you will have withdrawn.

To see how long the money lasts, type **0** in Balance at the end and press × on Time period. To find a sustainable withdrawal, set the balance you want to leave and press × on Monthly withdrawal.

## The formula

<p class="formula">B = P × (1 + i)<sup>n</sup> − W × [((1 + i)<sup>n</sup> − 1) ÷ i]</p>

- **P** = starting corpus
- **W** = monthly withdrawal
- **i** = monthly return = annual return ÷ 12
- **n** = number of months

The first term is what the corpus would grow to with no withdrawals. The second is the future value of everything you withdrew.

## Worked example

₹50,00,000 corpus, ₹30,000 a month, 8% return, 15 years:

- Total withdrawn = 30,000 × 180 = **{inr(30000*180)}**
- Balance after 15 years = **{inr(b1)}**

Because ₹30,000 is less than the monthly return on ₹50 lakh at 8% (about ₹33,333), the corpus actually grows.

## How long does ₹50 lakh last at 8%?

| Monthly withdrawal | Per year | Money lasts |
|---|---|---|
{rows}
## SWP vs FD interest vs annuity

| | SWP | FD interest | Annuity |
|---|---|---|---|
| Income | You choose | Depends on rate | Fixed for life |
| Capital | Stays yours | Stays yours | Given up |
| Tax | Only on gains | Full interest at slab rate | Full annuity at slab rate |
| Risk | Market-linked | Low | Low |

## Keep in mind

- Market returns are not steady. A fall in the early years of withdrawal hurts more than a fall later. Keep 1–2 years of withdrawals in a liquid or debt fund.
- Raise the withdrawal only gradually for inflation.
- Exit loads may apply to withdrawals made soon after investing.
''')
print('india1 done')
