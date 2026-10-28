import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
from inr import inr
D = '2026-10-27'
f = lambda x, d=0: f"{x:,.{d}f}"

# ---------------- Debt-to-income
page('finance', 'debt-to-income', f'''
title: Debt-to-Income Ratio Calculator (DTI and FOIR)
description: Calculate your debt-to-income ratio (DTI or FOIR) from monthly debts and income — and see how lenders judge it for home and personal loans.
category: finance
keywords: [debt to income ratio, dti calculator, foir calculator, debt to income, loan eligibility, mortgage dti, emi to income ratio]
updated: {D}
variables:
  - {{ id: debt, label: Total monthly debt payments (EMIs), family: currency, default: 1500, min: 0, decimals: 2 }}
  - {{ id: inc, label: Gross monthly income, family: currency, default: 6000, min: 0.01, decimals: 2 }}
  - {{ id: dti, label: Debt-to-income ratio, family: percent, unit: '%', min: 0, bands: [{{ max: 0.36, label: Healthy, color: '#16a34a' }}, {{ max: 0.43, label: Manageable, color: '#ca8a04' }}, {{ max: 0.5, label: High, color: '#ea580c' }}, {{ max: 10, label: Very high, color: '#dc2626' }}] }}
  - {{ id: room, label: Room for new payments at 36%, family: currency, decimals: 2 }}
equations:
  - dti = debt / inc
  - room = 0.36 * inc - debt
faq:
  - q: What is a good debt-to-income ratio?
    a: Under 36% is generally considered healthy. Many lenders accept up to 43% for mortgages, and some go higher with strong credit.
  - q: What is FOIR?
    a: Fixed Obligation to Income Ratio — the term Indian banks use. It is the share of your net monthly income going to EMIs and other fixed obligations. Many lenders cap it at 40–55%.
  - q: Which debts are included?
    a: Monthly payments on home, car, personal and education loans, minimum credit card payments and other regular obligations. Everyday living expenses are not included.
  - q: How can I lower my DTI?
    a: Pay off small loans or credit cards, avoid new debt before applying, and include all regular income such as rent received or a co-applicant’s salary.
related: [finance/emi, finance/loan-payment, finance/mortgage, finance/credit-card-payoff]
''', '''
## How to use this calculator

Add up **all monthly debt payments** — loan EMIs, minimum credit-card payments and other fixed obligations — and enter your **gross monthly income** (before tax). The calculator shows your debt-to-income ratio and how much more you could borrow each month while staying at 36%.

## The formula

<p class="formula">DTI = total monthly debt payments ÷ gross monthly income × 100</p>

## How lenders read DTI

| DTI | What it usually means |
|---|---|
| Below 20% | Excellent — plenty of room |
| 20–36% | Healthy — most lenders are comfortable |
| 36–43% | Acceptable for many mortgages, with fewer options |
| 43–50% | High — approval harder, higher rates likely |
| Above 50% | Very high — little room for new credit |

## Front-end and back-end ratios

US mortgage lenders often look at two ratios:

- **Front-end (housing) ratio**: housing payment ÷ income, often 28% or less.
- **Back-end ratio**: all debts including housing ÷ income — this calculator.

The well-known **28/36 rule** combines both.

## FOIR in India

Indian banks use FOIR on **net** (take-home) income:

| Net monthly income | Typical maximum FOIR |
|---|---|
| Lower incomes | 40–50% |
| Higher incomes | 50–65% |

So with a take-home of ₹1,00,000 and a 50% FOIR, total EMIs can be up to ₹50,000 a month. Use the [EMI calculator](/finance/emi/) to see what loan that supports.

## Example

Monthly EMIs of 1,500 and a gross income of 6,000:

- DTI = 1,500 ÷ 6,000 = **25%**
- Room at 36% = 2,160 − 1,500 = **540 a month** for new payments
''')

# ---------------- Annuity payout
def pmt(pv, r, y): i = r/12; n = 12*y; return pv*i/(1-(1+i)**-n)
a1 = pmt(5000000, .07, 20)
page('finance', 'annuity-payout', f'''
title: Annuity Payout Calculator
description: Find the monthly income a lump sum can pay for a fixed number of years — or the lump sum needed for a target monthly payout.
category: finance
keywords: [annuity calculator, annuity payout, monthly income from lump sum, pension calculator, present value of annuity, retirement income, how much will my annuity pay]
updated: {D}
variables:
  - {{ id: PV, label: Lump sum invested, family: currency, default: 5000000, min: 0, decimals: 0 }}
  - {{ id: r, label: Annual interest rate, family: percent, unit: '%', default: 7, min: 0.0001, max: 0.5 }}
  - {{ id: t, label: Payout period, family: time, unit: yr, default: 20, min: 0.0833 }}
  - {{ id: M, label: Monthly payout, family: currency, min: 0, decimals: 2 }}
  - {{ id: T, label: Total received, family: currency, min: 0, decimals: 0 }}
  - {{ id: I, label: Interest earned, family: currency, decimals: 0 }}
equations:
  - M = PV * (r/12) / (1 - (1 + r/12)^(-12*t))
  - T = M * 12 * t
  - I = T - PV
faq:
  - q: How much monthly income does 50 lakh give?
    a: "At 7% for 20 years, about {inr(a1)} a month, after which the money is fully used up."
  - q: Is this the same as an insurance annuity?
    a: It is a fixed-term annuity that runs the money down to zero. Life annuities from insurers pay for life and use mortality tables, so their rates differ.
  - q: How much do I need for a given monthly income?
    a: Press × on Lump sum and type the monthly payout you want.
  - q: Does the payout rise with inflation?
    a: Not in this calculation. To keep up with inflation, start lower and increase withdrawals over time, or use a growing annuity.
related: [finance/swp, finance/retirement-corpus, finance/nps, finance/present-value]
''', f'''
## How to use this calculator

Enter the **lump sum**, the **interest rate** it earns and the **payout period**. You get the level monthly payout that uses up the money exactly over that time. To find the lump sum needed for a target income, press × on Lump sum.

## The formula

<p class="formula">M = PV × i ÷ (1 − (1 + i)<sup>−n</sup>)</p>

- **PV** = lump sum
- **i** = monthly rate (annual ÷ 12)
- **n** = number of monthly payments

This is the same maths as a loan EMI, seen from the lender's side.

## Monthly payout per 10,00,000 (or 1,000,000)

| Rate | 10 years | 15 years | 20 years | 25 years |
|---|---|---|---|---|
''' + ''.join(f"| {r}% | {f(pmt(1e6,r/100,10))} | {f(pmt(1e6,r/100,15))} | {f(pmt(1e6,r/100,20))} | {f(pmt(1e6,r/100,25))} |\n" for r in [5, 6, 7, 8, 9]) + '''
## Fixed-term vs life annuity

| | Fixed-term (this calculator) | Life annuity (insurer) |
|---|---|---|
| Pays for | A set number of years | As long as you live |
| Money left at end | None | None (unless return-of-purchase option) |
| Longevity risk | You bear it | Insurer bears it |
| Flexibility | High | Low — usually irreversible |

## SWP as an alternative

A [systematic withdrawal plan](/finance/swp/) from mutual funds works similarly but with market-linked returns and the option to change withdrawals.

## Taxes

Annuity and interest income are usually taxable at your slab rate. Only the interest part of each payment is income; the rest is return of your own capital.
''')

# ---------------- Future value
def fv(pv, pm, r, y): i = r/12; n = 12*y; return pv*(1+i)**n + pm*((1+i)**n-1)/i
fv1 = fv(10000, 500, .08, 20)
page('finance', 'future-value', f'''
title: Future Value Calculator
description: Calculate the future value of a lump sum plus regular monthly deposits, with compound interest — or find the deposit needed for a goal.
category: finance
keywords: [future value calculator, fv calculator, future value of investment, future value with monthly contributions, compound interest with deposits, time value of money]
updated: {D}
featured: true
variables:
  - {{ id: PV, label: Starting amount, family: currency, default: 10000, min: 0, decimals: 2 }}
  - {{ id: PMT, label: Monthly deposit, family: currency, default: 500, min: 0, decimals: 2 }}
  - {{ id: r, label: Annual return, family: percent, unit: '%', default: 8, min: 0.0001, max: 1 }}
  - {{ id: t, label: Years, family: time, unit: yr, default: 20, min: 0 }}
  - {{ id: FV, label: Future value, family: currency, min: 0, decimals: 2 }}
  - {{ id: C, label: Total contributed, family: currency, min: 0, decimals: 2 }}
  - {{ id: G, label: Growth (interest earned), family: currency, decimals: 2 }}
equations:
  - FV = PV * (1 + r/12)^(12*t) + PMT * ((1 + r/12)^(12*t) - 1) / (r/12)
  - C = PV + PMT * 12 * t
  - G = FV - C
chart: {{ x: t, y: FV, from: 1, to: 40 }}
faq:
  - q: What is future value?
    a: The amount an investment grows to after a period of time at a given rate of return, including interest on interest.
  - q: How much will 10,000 plus 500 a month grow to in 20 years at 8%?
    a: "About {f(fv1)}, from {f(10000+500*240)} contributed."
  - q: Are deposits made at the start or end of each month?
    a: This calculator assumes the end of each month (an ordinary annuity). Deposits at the start of each month grow slightly more.
  - q: How do I find the monthly deposit for a goal?
    a: Press × on Monthly deposit and type the future value you want.
related: [finance/compound-interest, finance/sip, finance/present-value, finance/savings-goal]
''', f'''
## How to use this calculator

Enter a **starting amount**, a **monthly deposit**, the **expected annual return** and the **number of years**. You get the future value, how much you put in and how much came from growth. It works in reverse: press × on any field to solve for it.

## The formula

<p class="formula">FV = PV × (1 + i)<sup>n</sup> + PMT × [((1 + i)<sup>n</sup> − 1) ÷ i]</p>

- **PV** = starting amount, **PMT** = monthly deposit
- **i** = annual return ÷ 12, **n** = months

The first part grows the lump sum; the second adds up every monthly deposit with its interest.

## Worked example

10,000 to start, 500 a month, 8% a year, 20 years:

- Lump sum grows to {f(10000*(1+.08/12)**240)}
- Deposits grow to {f(500*((1+.08/12)**240-1)/(.08/12))}
- **Future value = {f(fv1)}**, from {f(130000)} contributed

## How time and rate change the result

500 a month, nothing to start:

| Years | 5% | 8% | 10% |
|---|---|---|---|
''' + ''.join(f"| {y} | {f(fv(0,500,.05,y))} | {f(fv(0,500,.08,y))} | {f(fv(0,500,.10,y))} |\n" for y in [5, 10, 20, 30, 40]) + '''
Doubling the time more than doubles the result, because growth compounds on itself.

## Real (inflation-adjusted) value

A future value is in future money. To see what it is worth in today's money, divide by (1 + inflation)<sup>years</sup>, or use the [real return calculator](/finance/real-return/) with your expected inflation.

## Related calculators

- [SIP calculator](/finance/sip/) — monthly investing with deposits at the start of each month.
- [Present value](/finance/present-value/) — the reverse: what a future amount is worth today.
''')

# ---------------- Commission
page('finance', 'commission', f'''
title: Commission Calculator
description: Calculate sales commission and total pay from sales, commission rate and base salary — or the sales needed to reach an earnings target.
category: finance
keywords: [commission calculator, sales commission, commission rate, real estate commission, broker commission, how to calculate commission, commission percentage]
updated: {D}
variables:
  - {{ id: S, label: Sales amount, family: currency, default: 50000, min: 0, decimals: 2 }}
  - {{ id: r, label: Commission rate, family: percent, unit: '%', default: 5, min: 0, max: 1 }}
  - {{ id: B, label: Base pay (for the period), family: currency, default: 2000, min: 0, decimals: 2 }}
  - {{ id: C, label: Commission earned, family: currency, min: 0, decimals: 2 }}
  - {{ id: T, label: Total earnings, family: currency, min: 0, decimals: 2 }}
equations:
  - C = S * r
  - T = B + C
faq:
  - q: How do I calculate commission?
    a: Multiply the sale amount by the commission rate. 5% of 50,000 is 2,500.
  - q: How do I find the commission rate?
    a: Divide the commission by the sale amount. 1,500 on 30,000 is a 5% rate.
  - q: How much do I need to sell to earn a target?
    a: Enter your target as Total earnings, then press × on Sales amount.
  - q: What is a typical real estate commission?
    a: It varies by country. In India brokers often charge 1–2% of the property price; in the US total commissions have traditionally been around 5–6%, split between agents.
related: [finance/profit-margin, finance/salary-increase, finance/break-even, finance/roas]
''', '''
## How to use this calculator

Enter the **sales amount**, the **commission rate** and any **base pay** for the period. The calculator shows the commission and total earnings. To find the sales needed for a target income, enter the target in Total earnings and press × on Sales amount.

## The formulas

<p class="formula">Commission = Sales × Rate &nbsp;·&nbsp; Total pay = Base + Commission</p>

## Commission chart

| Sales | 2% | 5% | 8% | 10% | 15% |
|---|---|---|---|---|---|
''' + ''.join(f"| {f(s)} | {f(s*.02)} | {f(s*.05)} | {f(s*.08)} | {f(s*.10)} | {f(s*.15)} |\n" for s in [1000, 5000, 10000, 25000, 50000, 100000, 500000]) + '''
## Common commission structures

| Structure | How it works |
|---|---|
| Straight commission | Pay is only commission — no base |
| Base + commission | Fixed salary plus a percentage of sales |
| Tiered | Rate rises above targets (e.g. 5% up to 50,000, 8% above) |
| Gross margin commission | Paid on profit, not revenue |
| Draw against commission | Advance paid, then deducted from later commission |

## Tiered example

5% on the first 50,000 and 8% above it, on sales of 80,000:

- First tier: 50,000 × 5% = 2,500
- Second tier: 30,000 × 8% = 2,400
- **Total commission = 4,900** (an effective 6.1%)

For tiers, run the calculator once per tier and add the results.

## Commission on margin

Paying on gross margin rather than revenue stops salespeople discounting heavily to close deals. Check whether your plan pays on invoice value, collected cash or margin.
''')

# ---------------- ROAS
page('finance', 'roas', f'''
title: ROAS Calculator (Return on Ad Spend)
description: Calculate ROAS, ad profit and break-even ROAS from ad spend, revenue and margin — for Google, Meta and other paid campaigns.
category: finance
keywords: [roas calculator, return on ad spend, break even roas, roas formula, ad spend calculator, google ads roas, facebook ads roas, marketing roi]
updated: {D}
featured: true
variables:
  - {{ id: sp, label: Ad spend, family: currency, default: 1000, min: 0.01, decimals: 2 }}
  - {{ id: rev, label: Revenue from ads, family: currency, default: 4000, min: 0, decimals: 2 }}
  - {{ id: m, label: Gross margin, family: percent, unit: '%', default: 40, min: 0.001, max: 1 }}
  - {{ id: roas, label: ROAS, suffix: '×', min: 0, decimals: 2 }}
  - {{ id: pr, label: Profit after ad spend, family: currency, decimals: 2 }}
  - {{ id: be, label: Break-even ROAS, suffix: '×', min: 0, decimals: 2 }}
  - {{ id: roi, label: Marketing ROI, family: percent, unit: '%' }}
equations:
  - roas = rev / sp
  - pr = rev * m - sp
  - be = 1 / m
  - roi = pr / sp
faq:
  - q: What is a good ROAS?
    a: It depends on your margin. A common benchmark is 4× (400%), but a business with 25% margins needs at least 4× just to break even, while one with 60% margins breaks even at 1.67×.
  - q: How is ROAS calculated?
    a: ROAS = revenue from ads ÷ ad spend. 4,000 of revenue from 1,000 of spend is a ROAS of 4× (400%).
  - q: What is break-even ROAS?
    a: The ROAS at which gross profit exactly covers ad spend: 1 ÷ gross margin. At a 40% margin, break-even ROAS is 2.5×.
  - q: What is the difference between ROAS and ROI?
    a: ROAS uses revenue; ROI uses profit. A campaign can have a 3× ROAS and still lose money if margins are thin.
related: [finance/customer-lifetime-value, finance/ad-metrics, finance/profit-margin, finance/roi]
''', '''
## How to use this calculator

Enter your **ad spend**, the **revenue** attributed to those ads and your **gross margin** (the share of revenue left after the cost of goods). You get ROAS, profit after ad spend, the break-even ROAS and marketing ROI.

## The formulas

<p class="formula">ROAS = Revenue ÷ Ad spend &nbsp;·&nbsp; Break-even ROAS = 1 ÷ Margin</p>

<p class="formula">Profit = Revenue × Margin − Ad spend &nbsp;·&nbsp; ROI = Profit ÷ Ad spend</p>

## Break-even ROAS by margin

| Gross margin | Break-even ROAS | Target ROAS for 20% ROI |
|---|---|---|
''' + ''.join(f"| {m}% | {1/(m/100):.2f}× | {1.2/(m/100):.2f}× |\n" for m in [20, 25, 30, 40, 50, 60, 70, 80]) + '''
## Example

1,000 spent, 4,000 revenue, 40% margin:

- ROAS = 4,000 ÷ 1,000 = **4×**
- Gross profit = 1,600; after ad spend = **600**
- Break-even ROAS = **2.5×**
- Marketing ROI = **60%**

## Beyond the first order

ROAS looks only at the first purchase. If customers buy again, the true return is higher. Compare acquisition cost with [customer lifetime value](/finance/customer-lifetime-value/) for a fuller picture.

## Attribution caveats

- Ad platforms often over-attribute sales (several platforms may claim the same order).
- View-through conversions can inflate ROAS.
- Use consistent attribution windows when comparing campaigns.

## Improving ROAS

- Raise conversion rate with better landing pages and offers.
- Increase average order value with bundles and upsells.
- Cut spend on keywords, audiences and placements below break-even.
- Track ad metrics such as CTR and CPC with the [ad metrics calculator](/finance/ad-metrics/).
''')

# ---------------- Ad metrics
page('finance', 'ad-metrics', f'''
title: CPM, CPC, CTR and CPA Calculator
description: Calculate CPM, CPC, CTR, conversion rate and cost per acquisition from ad spend, impressions, clicks and conversions — all in one place.
category: finance
keywords: [cpm calculator, cpc calculator, ctr calculator, cpa calculator, conversion rate calculator, cost per click, cost per thousand impressions, ad metrics]
updated: {D}
variables:
  - {{ id: sp, label: Ad spend, family: currency, default: 500, min: 0, decimals: 2 }}
  - {{ id: im, label: Impressions, default: 100000, min: 1, decimals: 0 }}
  - {{ id: cl, label: Clicks, default: 1500, min: 1, decimals: 0 }}
  - {{ id: cv, label: Conversions, default: 45, min: 0.0001, decimals: 0 }}
  - {{ id: cpm, label: CPM (cost per 1,000 impressions), family: currency, min: 0, decimals: 2 }}
  - {{ id: cpc, label: CPC (cost per click), family: currency, min: 0, decimals: 2 }}
  - {{ id: ctr, label: CTR (click-through rate), family: percent, unit: '%', min: 0 }}
  - {{ id: cvr, label: Conversion rate, family: percent, unit: '%', min: 0 }}
  - {{ id: cpa, label: CPA (cost per acquisition), family: currency, min: 0, decimals: 2 }}
equations:
  - cpm = sp / im * 1000
  - cpc = sp / cl
  - ctr = cl / im
  - cvr = cv / cl
  - cpa = sp / cv
faq:
  - q: How do I calculate CPM?
    a: CPM = ad spend ÷ impressions × 1,000. 500 spent for 100,000 impressions is a CPM of 5.
  - q: What is a good CTR?
    a: It varies by platform and industry. Search ads often see 3–6%, while display and social ads are commonly under 1–2%.
  - q: How are CPC, CTR and CPM related?
    a: CPC = CPM ÷ (CTR × 1,000). A 5 CPM with a 1.5% CTR gives a CPC of about 0.33.
  - q: What is the difference between CPA and CAC?
    a: CPA is the ad cost per conversion (which may be a lead or a sale). CAC includes all sales and marketing costs to win a paying customer.
related: [finance/roas, finance/customer-lifetime-value, math/percentage, finance/break-even]
''', '''
## How to use this calculator

Enter **ad spend**, **impressions**, **clicks** and **conversions** from your ad platform. The calculator gives CPM, CPC, CTR, conversion rate and CPA together. You can also work backwards — for example, enter a target CPA and press × on Ad spend to see the budget for a number of conversions.

## The formulas

| Metric | Formula |
|---|---|
| CPM | Spend ÷ Impressions × 1,000 |
| CPC | Spend ÷ Clicks |
| CTR | Clicks ÷ Impressions |
| Conversion rate | Conversions ÷ Clicks |
| CPA | Spend ÷ Conversions |

## The ad funnel

Each metric is one step in the funnel:

<p class="formula">Impressions → (CTR) → Clicks → (Conversion rate) → Conversions</p>

Improving any step lowers CPA. A 20% better CTR and a 20% better conversion rate together cut CPA by about **31%**.

## Typical ranges (rough guide)

| Channel | CTR | Conversion rate |
|---|---|---|
| Search ads | 3–6% | 3–8% |
| Social feed ads | 0.5–1.5% | 1–5% |
| Display banners | 0.1–0.5% | 0.5–2% |
| Email | 1–4% | 1–5% |

Benchmarks vary widely by industry, country and offer — compare against your own history first.

## Example

500 spent, 100,000 impressions, 1,500 clicks, 45 conversions:

- CPM = **5.00**, CPC = **0.33**, CTR = **1.5%**
- Conversion rate = **3%**, CPA = **11.11**

## From CPA to profit

A campaign is profitable when CPA is below the profit from each conversion. Use the [ROAS calculator](/finance/roas/) for revenue-based campaigns and the [customer lifetime value calculator](/finance/customer-lifetime-value/) when customers buy repeatedly.
''')

# ---------------- CLV
page('finance', 'customer-lifetime-value', f'''
title: Customer Lifetime Value Calculator (CLV and LTV:CAC)
description: Calculate customer lifetime value from order value, purchase frequency, margin and retention — and compare it with acquisition cost (LTV:CAC).
category: finance
keywords: [customer lifetime value calculator, clv calculator, ltv calculator, ltv cac ratio, lifetime value, churn rate, customer value, cac payback]
updated: {D}
variables:
  - {{ id: aov, label: Average order value, family: currency, default: 60, min: 0, decimals: 2 }}
  - {{ id: fq, label: Purchases per year, default: 4, min: 0 }}
  - {{ id: m, label: Gross margin, family: percent, unit: '%', default: 40, min: 0, max: 1 }}
  - {{ id: ch, label: Annual churn rate, family: percent, unit: '%', default: 30, min: 0.001, max: 1, help: Share of customers lost each year. Lifespan = 1 ÷ churn. }}
  - {{ id: cac, label: Customer acquisition cost (CAC), family: currency, default: 80, min: 0.01, decimals: 2 }}
  - {{ id: life, label: Average customer lifespan, family: time, unit: yr, min: 0 }}
  - {{ id: clv, label: Customer lifetime value (gross profit), family: currency, min: 0, decimals: 2 }}
  - {{ id: ratio, label: LTV:CAC ratio, suffix: ': 1', min: 0, decimals: 2 }}
  - {{ id: pb, label: CAC payback period, family: time, unit: mo, min: 0 }}
equations:
  - life = 1 / ch
  - clv = aov * fq * m * life
  - ratio = clv / cac
  - pb = cac / (aov * fq * m)
faq:
  - q: What is a good LTV to CAC ratio?
    a: A ratio of about 3:1 is a widely used benchmark. Below 1:1 you lose money on each customer; far above 5:1 may mean you are under-investing in growth.
  - q: How is customer lifetime value calculated?
    a: CLV = average order value × purchases per year × gross margin × customer lifespan in years. Lifespan can be estimated as 1 ÷ annual churn rate.
  - q: Should CLV use revenue or profit?
    a: Profit (gross margin) is better for comparing with acquisition cost. Revenue-based LTV overstates what you can afford to spend.
  - q: What is CAC payback?
    a: How long it takes for gross profit from a customer to repay the cost of acquiring them. Under 12 months is generally considered healthy.
related: [finance/roas, finance/ad-metrics, finance/profit-margin, finance/break-even]
''', '''
## How to use this calculator

Enter the **average order value**, **purchases per year**, **gross margin**, **annual churn rate** and your **customer acquisition cost**. You get the average customer lifespan, lifetime value (in gross profit), the LTV:CAC ratio and the CAC payback period.

## The formulas

<p class="formula">Lifespan = 1 ÷ churn &nbsp;·&nbsp; CLV = AOV × frequency × margin × lifespan</p>

<p class="formula">LTV:CAC = CLV ÷ CAC &nbsp;·&nbsp; Payback = CAC ÷ yearly gross profit per customer</p>

## Example

AOV 60, 4 orders a year, 40% margin, 30% churn, CAC 80:

- Yearly gross profit per customer = 60 × 4 × 0.4 = 96
- Lifespan = 1 ÷ 0.3 = 3.33 years
- CLV = 96 × 3.33 = **320**
- LTV:CAC = 320 ÷ 80 = **4.0 : 1**
- Payback = 80 ÷ 96 × 12 = **10 months**

## How churn changes CLV

| Annual churn | Lifespan | CLV (96 profit a year) |
|---|---|---|
''' + ''.join(f"| {c}% | {100/c:.1f} years | {96*100/c:,.0f} |\n" for c in [10, 20, 30, 40, 50, 70]) + '''
Cutting churn is often the fastest way to raise lifetime value.

## Subscription businesses

For subscriptions, use monthly figures: monthly revenue per user × margin ÷ monthly churn. A 20 monthly plan at 80% margin with 4% monthly churn has a CLV of 20 × 0.8 ÷ 0.04 = **400**.

## Improving LTV:CAC

- **Raise CLV**: upsells, loyalty programmes, better onboarding, lower churn.
- **Lower CAC**: improve conversion rates, focus on efficient channels, referrals.
- Track CAC by channel with the [ad metrics calculator](/finance/ad-metrics/).
''')

# ---------------- Stock average
page('finance', 'stock-average', f'''
title: Stock Average Calculator (Average Down Calculator)
description: Calculate the average buy price of shares after buying at different prices — and how many more shares you need to reach a target average.
category: finance
keywords: [stock average calculator, average down calculator, share average calculator, average buy price, average cost per share, averaging shares]
updated: {D}
featured: true
variables:
  - {{ id: q1, label: First purchase — shares, default: 100, min: 0 }}
  - {{ id: p1, label: First purchase — price per share, family: currency, default: 250, min: 0, decimals: 2 }}
  - {{ id: q2, label: Second purchase — shares, default: 50, min: 0 }}
  - {{ id: p2, label: Second purchase — price per share, family: currency, default: 200, min: 0, decimals: 2 }}
  - {{ id: q3, label: Third purchase — shares (optional), default: 0, min: 0 }}
  - {{ id: p3, label: Third purchase — price per share, family: currency, default: 0, min: 0, decimals: 2 }}
  - {{ id: Q, label: Total shares, min: 0, decimals: 0 }}
  - {{ id: inv, label: Total invested, family: currency, min: 0, decimals: 2 }}
  - {{ id: avg, label: Average price per share, family: currency, min: 0, decimals: 2 }}
equations:
  - Q = q1 + q2 + q3
  - inv = q1 * p1 + q2 * p2 + q3 * p3
  - avg = inv / Q
faq:
  - q: How do I calculate the average price of shares?
    a: Total amount invested ÷ total shares. 100 shares at 250 plus 50 at 200 is 35,000 ÷ 150 = 233.33.
  - q: How many shares do I need to buy to reach a target average?
    a: Enter the target as the average price and press × on the second purchase quantity. The calculator solves for the shares needed at the new price.
  - q: Is averaging down a good idea?
    a: Only if your reasons for owning the stock still hold. Averaging down lowers your break-even price but increases your exposure to a falling share.
  - q: Do brokerage and taxes change the average?
    a: Yes. Add brokerage, exchange charges and stamp duty to the price paid for an accurate cost basis.
related: [finance/cagr, finance/roi, finance/dividend-yield, finance/pe-ratio]
''', '''
## How to use this calculator

Enter the **number of shares** and **price** for each purchase (up to three). The calculator shows total shares, total invested and the average price per share. Leave the third purchase at zero if you only bought twice.

To plan a purchase, type your **target average** in Average price and press × on the second purchase shares — the calculator finds how many to buy at the new price.

## The formula

<p class="formula">Average price = (q₁p₁ + q₂p₂ + q₃p₃) ÷ (q₁ + q₂ + q₃)</p>

## Example: averaging down

| Purchase | Shares | Price | Cost |
|---|---|---|---|
| First | 100 | 250 | 25,000 |
| Second | 50 | 200 | 10,000 |
| **Total** | **150** | **233.33** | **35,000** |

The share now needs to rise only to 233.33 to break even, instead of 250.

## Shares needed to reach a target average

Starting with 100 shares at 250, buying at 200:

| Target average | Extra shares needed |
|---|---|
''' + ''.join(f"| {t} | {round(100*(250-t)/(t-200)):,} |\n" for t in [240, 235, 230, 225, 220, 210]) + '''
The closer the target is to the new price, the more shares you need — the cost rises steeply.

## Averaging down vs averaging up

- **Averaging down**: buying more as the price falls, lowering your average.
- **Averaging up**: buying more as the price rises, often used by momentum investors.

Both increase your position size. Set a maximum allocation per stock before you start.

## Tax lots

For capital gains tax, many systems use **first in, first out** (FIFO) to decide which shares were sold. Your average cost and your tax cost basis may differ — check local rules.
''')

# ---------------- P/E ratio
page('finance', 'pe-ratio', f'''
title: P/E Ratio Calculator (Price to Earnings)
description: Calculate the price-to-earnings ratio, earnings yield and PEG ratio of a stock from its share price, EPS and growth rate.
category: finance
keywords: [pe ratio calculator, price to earnings ratio, p/e ratio, earnings yield, peg ratio, eps calculator, stock valuation]
updated: {D}
variables:
  - {{ id: P, label: Share price, family: currency, default: 1500, min: 0, decimals: 2 }}
  - {{ id: eps, label: Earnings per share (EPS, last 12 months), family: currency, default: 60, min: 0.0001, decimals: 2 }}
  - {{ id: g, label: Expected annual EPS growth, family: percent, unit: '%', default: 15, min: 0.0001 }}
  - {{ id: pe, label: P/E ratio, suffix: '×', min: 0, decimals: 2 }}
  - {{ id: ey, label: Earnings yield, family: percent, unit: '%', min: 0 }}
  - {{ id: peg, label: PEG ratio, min: 0, decimals: 2 }}
equations:
  - pe = P / eps
  - ey = eps / P
  - peg = pe / (g * 100)
faq:
  - q: What is a good P/E ratio?
    a: There is no single good number. Compare with the company’s history, its industry and the market. Fast-growing companies usually trade at higher P/Es.
  - q: How is EPS calculated?
    a: EPS = net profit attributable to shareholders ÷ number of shares outstanding.
  - q: What is the PEG ratio?
    a: P/E divided by the expected earnings growth rate (in %). A PEG near 1 is often seen as fair value; below 1 may suggest the stock is cheap relative to its growth.
  - q: What is a negative P/E?
    a: When a company has losses, EPS is negative and P/E is not meaningful. Analysts usually show it as “n/a”.
related: [finance/dividend-yield, finance/stock-average, finance/cagr, finance/roi]
''', '''
## How to use this calculator

Enter the **share price**, the **earnings per share** for the last twelve months (trailing EPS) and, optionally, the **expected EPS growth rate**. The calculator gives the P/E ratio, earnings yield and PEG ratio. To find the price at a target P/E, press × on Share price.

## The formulas

<p class="formula">P/E = Price ÷ EPS &nbsp;·&nbsp; Earnings yield = EPS ÷ Price &nbsp;·&nbsp; PEG = P/E ÷ growth (%)</p>

## Example

Price 1,500, EPS 60, growth 15%:

- P/E = 1,500 ÷ 60 = **25×** — investors pay 25 for each 1 of yearly earnings
- Earnings yield = **4%**
- PEG = 25 ÷ 15 = **1.67**

## What P/E tells you

| P/E | Often suggests |
|---|---|
| Under 10 | Low growth, cyclical business, or the market sees risk |
| 10–20 | Mature, steady companies |
| 20–40 | Strong growth expected |
| Above 40 | Very high growth expectations or temporarily low earnings |

## Trailing vs forward P/E

- **Trailing P/E** uses the last 12 months of actual earnings.
- **Forward P/E** uses analysts' estimates for the next 12 months.

Forward P/E is lower for growing companies but relies on forecasts that may be wrong.

## Earnings yield vs bond yields

Earnings yield (the inverse of P/E) lets you compare stocks with bonds and deposits. A P/E of 25 means a 4% earnings yield — though earnings can grow, unlike a fixed coupon.

## Limits

P/E ignores debt, cash, cyclicality and one-off gains or losses. Compare it with other measures such as price-to-book, EV/EBITDA and [dividend yield](/finance/dividend-yield/).
''')

# ---------------- Payback period
def dpb(c, a, r): return -math.log(1 - c*r/a)/math.log(1+r)
page('finance', 'payback-period', f'''
title: Payback Period Calculator
description: Calculate how long an investment takes to pay for itself from yearly savings or cash flow — simple and discounted payback.
category: finance
keywords: [payback period calculator, payback period, discounted payback, break even time, solar payback, investment payback, roi years]
updated: {D}
variables:
  - {{ id: C, label: Initial investment, family: currency, default: 300000, min: 0, decimals: 2 }}
  - {{ id: A, label: Yearly savings or cash flow, family: currency, default: 60000, min: 0.01, decimals: 2 }}
  - {{ id: r, label: Discount rate (for discounted payback), family: percent, unit: '%', default: 8, min: 0.0001, max: 1 }}
  - {{ id: pb, label: Simple payback, family: time, unit: yr, min: 0 }}
  - {{ id: dpb, label: Discounted payback, family: time, unit: yr, min: 0 }}
equations:
  - pb = C / A
  - dpb = -ln(1 - C * r / A) / ln(1 + r)
faq:
  - q: How do I calculate payback period?
    a: Divide the initial cost by the yearly savings or cash flow. 3,00,000 ÷ 60,000 = 5 years.
  - q: What is discounted payback?
    a: The time to recover the investment when future savings are discounted to today’s value. It is always longer than simple payback.
  - q: What is a good payback period?
    a: Many businesses look for 2–5 years. Home solar systems commonly pay back in 4–8 years depending on sunshine and tariffs.
  - q: Why does discounted payback show no result?
    a: If yearly savings never exceed the interest on the investment (C × r ≥ A), the project never pays back in present-value terms.
related: [finance/roi, finance/present-value, ecology/solar-system-size, ecology/led-savings]
''', '''
## How to use this calculator

Enter the **initial investment**, the **yearly savings or cash flow** it produces and a **discount rate** (your cost of money or alternative return). You get the simple and discounted payback periods.

## The formulas

<p class="formula">Simple payback = Investment ÷ Yearly cash flow</p>

<p class="formula">Discounted payback = −ln(1 − C × r ÷ A) ÷ ln(1 + r)</p>

The discounted formula assumes equal yearly cash flows.

## Payback at different discount rates

Investment 3,00,000, savings 60,000 a year:

| Discount rate | Discounted payback |
|---|---|
''' + ''.join(f"| {r}% | {dpb(300000,60000,r/100):.1f} years |\n" for r in [0.01, 4, 6, 8, 10, 12, 15]) + '''
The first row is effectively the simple payback (5 years).

## Typical payback periods

| Investment | Typical payback |
|---|---|
| LED lighting upgrade | under 1 year |
| Variable-speed drive on a pump or fan | 1–3 years |
| Rooftop solar (sunny regions) | 4–8 years |
| Building insulation | 3–10 years |
| Industrial machinery | 2–5 years |

## Limits of payback

Payback ignores everything **after** the payback point. A project that pays back in 3 years but stops earning in year 4 can look better than one that pays back in 5 years and earns for 20. Use payback alongside [ROI](/finance/roi/) or net present value.

## Uneven cash flows

If savings vary year to year, subtract each year's cash flow from the investment until it reaches zero. The year in which the running balance turns positive is the payback year.
''')

# ---------------- Real return
page('finance', 'real-return', f'''
title: Real Rate of Return Calculator (Inflation-Adjusted)
description: Calculate your real return after inflation (and tax) from a nominal interest rate or investment return — see if your money is really growing.
category: finance
keywords: [real rate of return, inflation adjusted return, real return calculator, fisher equation, real interest rate, after tax return, nominal vs real]
updated: {D}
variables:
  - {{ id: n, label: Nominal return, family: percent, unit: '%', default: 7, min: -0.99 }}
  - {{ id: tx, label: Tax on returns, family: percent, unit: '%', default: 0, min: 0, max: 1 }}
  - {{ id: i, label: Inflation rate, family: percent, unit: '%', default: 5, min: -0.5 }}
  - {{ id: at, label: After-tax return, family: percent, unit: '%' }}
  - {{ id: rr, label: Real return, family: percent, unit: '%' }}
equations:
  - at = n * (1 - tx)
  - rr = (1 + at) / (1 + i) - 1
faq:
  - q: What is the real rate of return?
    a: The return after removing the effect of inflation — how much your purchasing power actually grows.
  - q: Why not just subtract inflation from the return?
    a: Subtraction is a close approximation for small rates. The exact Fisher formula is (1 + nominal) ÷ (1 + inflation) − 1. 7% with 5% inflation is 1.90%, not 2%.
  - q: Can the real return be negative?
    a: Yes. If inflation is higher than your after-tax return, your money is losing purchasing power even though the balance grows.
  - q: How does tax affect the real return?
    a: Tax reduces the nominal return first. A 7% FD taxed at 30% gives 4.9% after tax; with 5% inflation the real return is slightly negative.
related: [finance/inflation, finance/fd, finance/compound-interest, finance/cagr]
''', '''
## How to use this calculator

Enter the **nominal return** (interest rate or investment return), the **tax rate** on those returns (0 if tax-free) and the **inflation rate**. You get the after-tax return and the real return.

## The Fisher equation

<p class="formula">Real return = (1 + nominal) ÷ (1 + inflation) − 1</p>

With tax, use the after-tax return as the nominal: nominal × (1 − tax rate).

## Real returns at a glance

| Nominal | Inflation 3% | Inflation 5% | Inflation 7% |
|---|---|---|---|
''' + ''.join(f"| {n}% | {((1+n/100)/1.03-1)*100:+.2f}% | {((1+n/100)/1.05-1)*100:+.2f}% | {((1+n/100)/1.07-1)*100:+.2f}% |\n" for n in [4, 6, 7, 8, 10, 12]) + '''
## After-tax examples (5% inflation)

| Investment | Nominal | Tax | After tax | Real |
|---|---|---|---|---|
| FD at 7%, 30% slab | 7% | 30% | 4.9% | −0.10% |
| FD at 7%, 10% slab | 7% | 10% | 6.3% | +1.24% |
| PPF at 7.1% (tax-free) | 7.1% | 0% | 7.1% | +2.00% |
| Equity at 12%, 12.5% LTCG (approx.) | 12% | 12.5% | 10.5% | +5.24% |

Equity tax is simplified here; actual tax depends on holding period and exemptions.

## Why real return matters

A goal planned in today's money needs a real return to reach it. Saving for something that costs 10 lakh today in 15 years at 6% inflation actually needs about 24 lakh — see the [inflation calculator](/finance/inflation/).

## Real vs nominal growth over time

At a 2% real return, money doubles in purchasing power in about 35 years. At 5% real, it doubles in about 14 years.
''')

# ---------------- SCSS
page('finance', 'scss', f'''
title: SCSS Calculator (Senior Citizens Savings Scheme)
description: Calculate quarterly interest and total returns from the Senior Citizens Savings Scheme at the current 8.2% rate — with the ₹30 lakh limit.
category: finance
keywords: [scss calculator, senior citizen savings scheme calculator, scss interest rate, scss quarterly interest, post office scss, scss 8.2]
updated: {D}
variables:
  - {{ id: P, label: Deposit amount, family: currency, prefix: '₹', default: 1500000, min: 1000, max: 3000000, decimals: 0, help: '₹1,000 to ₹30,00,000 per individual.' }}
  - {{ id: r, label: Interest rate, family: percent, unit: '%', default: 8.2, min: 0.0001, max: 0.3 }}
  - {{ id: q, label: Quarterly interest, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: m, label: Monthly equivalent, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: y, label: Yearly interest, family: currency, prefix: '₹', min: 0, decimals: 0 }}
  - {{ id: tot, label: Total interest over 5 years, family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - q = P * r / 4
  - m = q / 3
  - y = q * 4
  - tot = y * 5
faq:
  - q: What is the SCSS interest rate?
    a: 8.2% a year for the October–December 2026 quarter, paid quarterly. The rate on the date of deposit applies for the full 5 years.
  - q: What is the maximum investment in SCSS?
    a: ₹30 lakh per individual. A married couple can each open an account.
  - q: Who can invest in SCSS?
    a: Residents aged 60 and above. Retirees aged 55–60 (and some defence retirees aged 50–60) can invest retirement benefits within a set period of retirement.
  - q: Is SCSS interest taxable?
    a: Yes, at your slab rate, with TDS above the yearly threshold. Deposits qualify for deduction under section 80C in the old regime.
related: [finance/post-office-mis, finance/fd, finance/annuity-payout, finance/swp]
''', '''
## How to use this calculator

Enter the **deposit amount** (up to ₹30 lakh) and the **interest rate** (currently 8.2%). You get the interest paid every quarter, its monthly equivalent, the yearly total and the total interest over the 5-year term. The deposit is returned at maturity.

## The formula

<p class="formula">Quarterly interest = Deposit × Rate ÷ 4</p>

Interest is paid on the first working day of April, July, October and January. It is simple interest — it does not compound unless you reinvest it.

## Quarterly income at 8.2%

| Deposit | Quarterly | Monthly equivalent | Yearly |
|---|---|---|---|
''' + ''.join(f"| {inr(p)} | {inr(p*.082/4)} | {inr(p*.082/12)} | {inr(p*.082)} |\n" for p in [500000, 1000000, 1500000, 2000000, 3000000]) + '''
## Key rules

- **Tenure**: 5 years, which can be extended by a further 3 years.
- **Premature closure**: after 1 year with 1.5% penalty; after 2 years with 1% penalty.
- **Joint account**: allowed with spouse only; the deposit limit applies to the first holder.
- **Where**: post offices and authorised banks.

## SCSS vs other income options

| | SCSS | POMIS | Bank senior FD |
|---|---|---|---|
| Rate (Oct–Dec 2026) | 8.2% | 7.4% | Varies by bank |
| Payout | Quarterly | Monthly | Monthly / quarterly |
| Limit | ₹30 lakh | ₹9 / 15 lakh | No limit |
| 80C benefit | Yes (old regime) | No | Only 5-year tax saver |

Compare monthly income options with the [Post Office MIS calculator](/finance/post-office-mis/).
''')

# ---------------- KVP
page('finance', 'kvp', f'''
title: KVP Calculator (Kisan Vikas Patra)
description: Calculate Kisan Vikas Patra maturity — your money doubles in 115 months at the current 7.5% rate. See the maturity value for any amount.
category: finance
keywords: [kvp calculator, kisan vikas patra calculator, kvp interest rate, kvp maturity, kvp 115 months, post office kvp, money double scheme]
updated: {D}
variables:
  - {{ id: P, label: Investment amount, family: currency, prefix: '₹', default: 100000, min: 1000, decimals: 0 }}
  - {{ id: r, label: Interest rate (compounded yearly), family: percent, unit: '%', default: 7.5, min: 0.0001, max: 0.3 }}
  - {{ id: mo, label: Months to double, suffix: months, min: 0, decimals: 0 }}
  - {{ id: F, label: Maturity value, family: currency, prefix: '₹', min: 0, decimals: 0 }}
equations:
  - mo = ln(2) / ln(1 + r) * 12
  - F = 2 * P
faq:
  - q: How long does KVP take to double money?
    a: 115 months (9 years 7 months) at the current 7.5% rate.
  - q: What is the minimum and maximum investment in KVP?
    a: Minimum ₹1,000, in multiples of ₹100. There is no maximum, though PAN and income proof are needed for larger amounts.
  - q: Is KVP interest taxable?
    a: Yes. Interest is taxable at your slab rate, either yearly on an accrual basis or at maturity. KVP has no 80C benefit.
  - q: Can I withdraw KVP early?
    a: After 2 years and 6 months, with a reduced rate. Earlier withdrawal is allowed only in special cases such as the holder’s death.
related: [finance/nsc, finance/doubling-time, finance/fd, finance/ppf]
''', '''
## How to use this calculator

Enter the **amount** you will invest and the **interest rate** (7.5% for October–December 2026). The calculator shows how many months it takes to double and the maturity value.

## How KVP works

Kisan Vikas Patra is a government-backed savings certificate sold at post offices. The amount invested **doubles** after a fixed period, which the government sets from the interest rate:

<p class="formula">Months = ln 2 ÷ ln(1 + r) × 12</p>

At 7.5% compounded yearly, that is 115 months.

## Maturity values

| Investment | Maturity after 115 months |
|---|---|
''' + ''.join(f"| {inr(p)} | {inr(2*p)} |\n" for p in [10000, 50000, 100000, 500000, 1000000]) + '''
## Interest rate and doubling period

| Interest rate | Months to double |
|---|---|
''' + ''.join(f"| {r}% | {math.log(2)/math.log(1+r/100)*12:.0f} |\n" for r in [6.9, 7.0, 7.2, 7.5, 7.7, 8.0]) + '''
## KVP vs NSC vs FD

| | KVP | NSC | Bank FD |
|---|---|---|---|
| Rate (Oct–Dec 2026) | 7.5% | 7.7% | Varies |
| Tenure | 115 months | 5 years | 7 days–10 years |
| 80C benefit | No | Yes (old regime) | Only 5-year tax saver |
| Early exit | After 2.5 years | Restricted | Usually allowed with penalty |

## Who KVP suits

KVP suits conservative savers who want a guaranteed, government-backed return and do not need the money for about 10 years. For tax savings, [NSC](/finance/nsc/) or [PPF](/finance/ppf/) may be better.
''')
print('batchB finance done')
