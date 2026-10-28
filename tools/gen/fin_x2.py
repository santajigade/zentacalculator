import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
f = lambda x, d=0: f"{x:,.{d}f}"
def pmt(P, r, y): i = r/12; n = 12*y; return P*i*(1+i)**n/((1+i)**n-1)

# ---------------- hourly to salary
rows = ''.join(f"| {f(h)} | {f(h*37.5*52)} | {f(h*40*52)} | {f(h*40*50)} |\n" for h in [15, 20, 25, 30, 40, 50, 75])
expand('finance/hourly-to-salary', f'''
## Hours per week compared

| Hourly rate | 37.5 h × 52 wk | 40 h × 52 wk | 40 h × 50 wk |
|---|---|---|---|
{rows}
## Salary to hourly for contractors

If you switch from a salaried job to contracting, do not just divide your old salary by 2,080 hours. A salary comes with paid leave, holidays and benefits that a contractor must cover:

- **Unpaid time off**: holidays and sick days, often 4–6 weeks a year.
- **Non-billable hours**: admin, sales and training, often 20–30% of working time.
- **Benefits and taxes**: health insurance, pension contributions and employer-side taxes.

A common rule of thumb is that a contract rate needs to be **1.5 to 2 times** the equivalent salaried hourly rate to give the same income.

## Overtime

Many jobs pay overtime at 1.5× the normal rate above 40 hours a week. To include it, work out the overtime pay separately:

<p class="formula">Weekly pay = rate × 40 + rate × 1.5 × overtime hours</p>

At 25 an hour with 5 hours of overtime, that is 1,000 + 187.50 = **1,187.50** a week.

## Gross vs take-home pay

The results are **gross** pay, before income tax, social security and other deductions. Take-home pay is usually 15–35% lower depending on your country, income and tax choices.
''', [
 ('How many working hours are in a year?', '2,080 for a 40-hour week over 52 weeks. With 37.5-hour weeks it is 1,950. Subtract unpaid leave and public holidays for a more realistic figure.'),
 ('Is 25 an hour a good salary?', 'At 40 hours a week for 52 weeks, 25 an hour is 52,000 a year before tax. Whether that is good depends on local living costs and the typical pay for the role.'),
], before='## Remember')

# ---------------- inflation
rows = ''.join(f"| {r}% | {f(100*(1+r/100)**10,2)} | {f(100*(1+r/100)**20,2)} | {f(100/(1+r/100)**20,2)} |\n" for r in [2, 3, 4, 6, 8])
expand('finance/inflation', f'''
## 100 today at different inflation rates

| Inflation | Cost in 10 years | Cost in 20 years | Buying power of 100 in 20 years |
|---|---|---|---|
{rows}
## Real return: beating inflation

What matters for savings is the **real return**, the growth after inflation:

<p class="formula">Real return = (1 + nominal return) ÷ (1 + inflation) − 1</p>

A deposit paying 7% when inflation is 6% gives a real return of only about 0.94%. After tax on the interest, it may even be negative. Equity and property have historically beaten inflation over long periods, though with more ups and downs.

## Lifestyle inflation vs official inflation

Official figures such as the Consumer Price Index (CPI) track an average basket of goods. Your own inflation may be higher if you spend more on:

- **Education**, which has often risen faster than general prices.
- **Healthcare and insurance**.
- **Housing and rent** in growing cities.

For long-term goals like a child's education, many planners use 8–10% rather than the headline CPI rate.

## Using this for goal planning

1. Enter today's cost of the goal, the inflation rate and the years until you need it.
2. The **future cost** is the amount you must save for.
3. Plug that into the [SIP calculator](/finance/sip/) or the [savings goal calculator](/finance/savings-goal/) to find the monthly saving needed.
''', [
 ('What is the difference between CPI and WPI?', 'CPI (Consumer Price Index) tracks prices that households pay. WPI (Wholesale Price Index) tracks prices at the wholesale level. For personal planning, CPI is the relevant measure.'),
 ('Can inflation be negative?', 'Yes, that is deflation, when average prices fall. Enter a negative rate, for example −1%, to model it.'),
], before='## Why it matters')

# ---------------- loan payment
P, r = 200000, .09; M = pmt(P, r, 5)
bal = P; sched = ''
for y in range(1, 6):
    i_y = 0; p_y = 0
    for _ in range(12):
        it = bal*r/12; pr = M-it; bal -= pr; i_y += it; p_y += pr
    sched += f"| {y} | {f(p_y)} | {f(i_y)} | {f(max(bal,0))} |\n"
expand('finance/loan-payment', f'''
## Amortization: where each payment goes

200,000 at 9% for 5 years (payment {f(M,2)} a month):

| Year | Principal repaid | Interest paid | Balance at year end |
|---|---|---|---|
{sched}
Early payments are mostly interest. As the balance falls, more of each payment repays the loan. This is why extra payments in the first years save the most.

## Fixed vs floating rate

| | Fixed rate | Floating (variable) rate |
|---|---|---|
| Payment | Same for the whole term | Changes with a benchmark rate |
| Risk | You know the cost upfront | Can rise or fall |
| Typical use | Car and personal loans | Home loans, business loans |

With a floating rate, recalculate whenever the rate changes to see your new payment.

## Flat rate vs reducing balance

Some lenders quote a **flat rate**, charging interest on the full original amount for the whole term. A 9% flat rate is far more expensive than 9% on a reducing balance — roughly equal to 16% on a reducing balance over 5 years. Always ask for the reducing-balance rate or the APR when comparing offers.
''', [
 ('What is an amortization schedule?', 'A table showing each payment split into interest and principal, and the balance left after it. The table above summarises it by year.'),
 ('Is it better to take a shorter or longer loan?', 'A shorter loan has higher payments but much lower total interest. Choose the shortest term whose payment you can comfortably afford.'),
], before='## Tips before you borrow')

# ---------------- mortgage
rows = ''
for rr in [5, 5.5, 6, 6.5, 7, 7.5]:
    m = pmt(320000, rr/100, 30); rows += f"| {rr}% | {f(m,2)} | {f(m*360-320000)} |\n"
m30 = pmt(320000, .065, 30)
expand('finance/mortgage', f'''
## How the rate changes the payment

Loan of 320,000 over 30 years:

| Rate | Monthly payment | Total interest |
|---|---|---|
{rows}
Each half-point change in rate moves the payment by roughly 100 a month on this loan and the total interest by tens of thousands.

## The full monthly cost of owning

The calculator shows principal and interest only. A typical full payment (often called **PITI**) also includes:

- **Property tax**, often 0.5–2% of the home value a year.
- **Home insurance**.
- **Mortgage insurance** if your down payment is below 20%.
- **HOA or maintenance fees** for flats and gated communities.

Add these to the result to see your real monthly cost.

## How much income do you need?

Many lenders use the **28/36 rule**: housing costs no more than 28% of gross monthly income, and all debt payments no more than 36%. For a principal-and-interest payment of {f(m30)} plus about 500 of tax and insurance, you would need a gross income of roughly {f((m30+500)/0.28)} a month.

## Extra payments

Paying one extra monthly payment a year on a 30-year loan at 6.5% shortens it by about 5–6 years and saves a large share of the interest. Check that your lender has no prepayment penalty first.
''', [
 ('What is PMI?', 'Private mortgage insurance protects the lender when your down payment is under 20%. It usually costs 0.3–1.5% of the loan a year and can be removed once you reach 20% equity.'),
 ('Should I choose 15 or 30 years?', 'A 15-year loan has a higher payment but a lower rate and far less interest. A 30-year loan gives a lower payment and more flexibility. You can take 30 years and prepay to get some of the benefit of both.'),
], before='## Ways to pay less')

# ---------------- present value
rows = ''.join(f"| {r}% | {f(10000/(1+r/100)**5,2)} | {f(10000/(1+r/100)**10,2)} | {f(10000/(1+r/100)**20,2)} |\n" for r in [3, 5, 8, 10, 12])
expand('finance/present-value', f'''
## Present value of 10,000 received later

| Discount rate | In 5 years | In 10 years | In 20 years |
|---|---|---|---|
{rows}
The higher the rate and the longer the wait, the less a future amount is worth today.

## Present value of a series of payments

For equal payments every year (an annuity), the present value is:

<p class="formula">PV = PMT × [1 − (1 + r)<sup>−n</sup>] ÷ r</p>

1,000 a year for 10 years at 8% is worth {f(1000*(1-1.08**-10)/.08,2)} today, not 10,000. This is how pensions, lottery payouts and lease payments are valued.

## Net present value (NPV)

Businesses compare projects with NPV: the present value of all future cash inflows minus the cost today. A positive NPV means the project earns more than the discount rate.

Example: spend 20,000 today to receive 6,000 a year for 5 years, discount rate 10%. PV of inflows = {f(6000*(1-1.1**-5)/.1,2)}, so NPV = **{f(6000*(1-1.1**-5)/.1-20000,2)}**. The project is worth doing.

## Choosing a discount rate

- **Personal decisions**: the return you could earn elsewhere, such as a deposit or index fund.
- **Inflation-adjusted value**: use the inflation rate to see a future amount in today's money.
- **Business projects**: the company's cost of capital, plus a premium for risk.
''', [
 ('Is a lump sum today better than payments over time?', 'Compare the lump sum with the present value of the payments at a realistic discount rate. If the lump sum is higher, take it.'),
 ('What is the difference between discount rate and interest rate?', 'They use the same maths in opposite directions. An interest rate grows money forward in time; a discount rate brings future money back to today.'),
], before='## Uses')

# ---------------- profit margin
rows = ''.join(f"| {m}% | {f(c/(1-m/100),2)} | {m/(100-m)*100:.1f}% |\n" for m, c in [(10, 60), (20, 60), (30, 60), (40, 60), (50, 60), (60, 60)])
expand('finance/profit-margin', f'''
## Price needed for a target margin (cost 60)

| Target margin | Selling price | Equivalent markup |
|---|---|---|
{rows}
<p class="formula">Price = Cost ÷ (1 − margin)</p>

## Typical margins by industry

| Industry | Typical net margin |
|---|---|
| Grocery retail | 1–3% |
| Restaurants | 3–9% |
| Manufacturing | 5–10% |
| Professional services | 10–20% |
| Software | 15–30% |

Gross margins are much higher than net margins, because net margin also subtracts rent, salaries, marketing and taxes.

## Margin with GST or VAT

Calculate margin on prices **before** tax. Sales tax is collected for the government and is not revenue. If your selling price includes 18% tax, divide it by 1.18 first, or use the [GST calculator](/finance/gst/).

## Common mistakes

- **Pricing with margin but thinking in markup.** A 50% markup is only a 33% margin.
- **Forgetting discounts and returns.** A 10% sale cuts a 30% margin to about 22%.
- **Leaving out shipping and payment fees** from cost, which can quietly erase thin margins.
''', [
 ('What is a good profit margin?', 'It varies widely by industry. As a rough guide, a net margin of 10% is healthy for many small businesses, 20% is high, and under 5% is thin.'),
 ('How do I convert markup to margin?', 'Margin = markup ÷ (1 + markup). A 50% markup gives a margin of 0.5 ÷ 1.5 = 33.3%.'),
], before='## Gross vs net margin')

# ---------------- retirement corpus
rows = ''.join(f"| {y} | {f(600000*1.06**y)} | {f(600000*1.06**y/.04)} | {f(600000*1.06**y/.035)} |\n" for y in [10, 15, 20, 25, 30])
expand('finance/retirement-corpus', f'''
## Corpus by years to retirement

Expenses of 6,00,000 a year today, 6% inflation:

| Years to retire | Yearly expenses then | Corpus at 4% | Corpus at 3.5% |
|---|---|---|---|
{rows}
## How to reach the corpus

1. Note the corpus from the calculator.
2. Subtract what your existing savings, EPF, PPF or pension will be worth by then.
3. Use the [SIP calculator](/finance/sip/) to find the monthly investment for the gap, or the [step-up SIP calculator](/finance/step-up-sip/) if you will raise it every year.

## Expenses that change in retirement

- **Lower**: commuting, work clothes, home loan EMI (if paid off), children's costs.
- **Higher**: healthcare and insurance, travel in the early years, help at home later.

A common shortcut is 70–80% of current expenses, but listing actual costs gives a better estimate.

## Sources of retirement income

| Source | Inflation-linked? |
|---|---|
| Withdrawals from investments (SWP) | Only if you increase them |
| Annuity / pension plan | Usually not |
| Government pension | Often partly |
| Rental income | Usually rises over time |

Combining several sources reduces the risk of any one falling short. See the [SWP calculator](/finance/swp/) to plan withdrawals.
''', [
 ('Why use a lower withdrawal rate in India?', 'The 4% rule comes from US data with about 2–3% inflation. With higher inflation, many Indian planners prefer 3–3.5%, which means a larger corpus.'),
 ('Should I include my house in the corpus?', 'Only if you plan to sell it or rent it out. A house you live in does not pay your bills.'),
], before='## Important assumptions')

# ---------------- ROI
expand('finance/roi', '''
## ROI vs annualized ROI

Two investments both return 50%:

| Investment | Total ROI | Held for | Annualized ROI |
|---|---|---|---|
| A | 50% | 2 years | 22.5% |
| B | 50% | 8 years | 5.2% |

Total ROI makes them look equal. Annualized ROI shows A is far better. Always compare investments with the annualized figure.

## ROI in marketing

Marketing ROI compares the profit a campaign generates with its cost:

<p class="formula">Marketing ROI = (Gross profit from campaign − Campaign cost) ÷ Campaign cost</p>

Use **gross profit**, not revenue. A campaign costing 5,000 that brings in 20,000 of sales at a 40% gross margin earns 8,000 of profit, an ROI of 60% — not 300%.

## ROI for property

For a rental property, include all costs and income:

- **Costs**: purchase price, stamp duty, registration, renovation, maintenance and loan interest.
- **Returns**: rent received after vacancies, plus the gain when you sell.

Rental yield (yearly rent ÷ price) gives the income part. Add expected price growth for the total return.

## Common mistakes

- Ignoring **fees, taxes and inflation**, which can turn a positive ROI into a loss in real terms.
- Comparing ROI over **different time periods** without annualizing.
- Counting **revenue instead of profit** for business decisions.
''', [
 ('What is a good ROI?', 'It depends on the risk and time. A safe deposit might give 5–7% a year, while equities have averaged around 10–12% over long periods. Riskier investments should offer a higher expected ROI.'),
 ('Can ROI be negative?', 'Yes. If the final value is less than what you invested, ROI is negative, showing a loss.'),
], before='## Limits')

# ---------------- salary increase
rows = ''.join(f"| {p}% | {f(60000*(1+p/100))} | {f(60000*p/100)} | {f(60000*p/100/12,2)} |\n" for p in [3, 5, 8, 10, 15, 20, 30])
expand('finance/salary-increase', f'''
## Raises on a 60,000 salary

| Raise | New salary | Extra per year | Extra per month |
|---|---|---|---|
{rows}
## Typical raises

- **Annual increment**: often 3–10%, depending on country, industry and performance.
- **Promotion**: commonly 10–20%.
- **Job switch**: often 15–30% or more, which is why many people see the biggest jumps when they change employers.

## Raises compound

A raise is applied to your already-raised salary. Five years of 8% raises lift 60,000 to {f(60000*1.08**5)}, a total increase of {(1.08**5-1)*100:.1f}%, not 40%. Over a career, small differences in yearly raises add up to a large difference in lifetime earnings.

## Fixed vs variable pay

When an offer quotes a total package, check the split:

- **Fixed pay** is guaranteed every month.
- **Variable pay or bonus** depends on performance and may not be paid in full.
- **Benefits** such as insurance, retirement contributions or stock options add value but are not cash in hand.

Calculate the raise on fixed pay to compare offers fairly.
''', [
 ('How do I calculate a percentage raise from two salaries?', 'Raise % = (new salary − old salary) ÷ old salary × 100. In the calculator, type both salaries and the raise is calculated.'),
 ('What raise do I need to keep up with inflation?', 'At least the inflation rate. With 6% inflation, a 6% raise keeps your buying power the same; anything above it is a real increase.'),
], before='## Negotiation tips')

# ---------------- sales tax
expand('finance/sales-tax-vat', '''
## Tax on common prices

| Net price | 5% | 10% | 18% | 20% |
|---|---|---|---|---|
''' + ''.join(f"| {f(n)} | {f(n*1.05,2)} | {f(n*1.10,2)} | {f(n*1.18,2)} | {f(n*1.20,2)} |\n" for n in [10, 50, 100, 250, 1000]) + '''
## Sales tax vs VAT vs GST

| | Sales tax (e.g. USA) | VAT (e.g. UK, EU) | GST (e.g. India, Australia) |
|---|---|---|---|
| Charged | Only at the final sale | At every stage of the supply chain | At every stage |
| Shown in prices | Usually added at the till | Usually included in shelf prices | Included in retail prices |
| Credit for business purchases | No | Yes (input VAT) | Yes (input tax credit) |

For India-specific GST rates and the CGST/SGST split, use the [GST calculator](/finance/gst/).

## Combined state and local rates

In the United States, the rate you pay is the state rate plus any county and city rates. Add them together and enter the total — for example, a 6% state rate plus 2.25% local is 8.25%.

## Invoices and rounding

Businesses often round tax per line item, while shops may round on the total. The difference is usually a few cents but can matter for accounting. Follow the rule your tax authority or accounting software uses.
''', [
 ('Is tax charged before or after a discount?', 'Usually after. Tax is calculated on the price you actually pay, so apply the discount first.'),
 ('How do I find the tax rate from two prices?', 'Rate = (gross − net) ÷ net. Enter both prices in the calculator and the rate is worked out.'),
], before='## Typical standard rates (check current local rules)')

# ---------------- savings goal
expand('finance/savings-goal', '''
## Starting early vs saving more

To reach 50,000 with nothing saved yet, at 7% a year:

| Time to goal | Monthly saving needed |
|---|---|
''' + ''.join(f"| {y} years | {f(50000*(.07/12)/((1+.07/12)**(12*y)-1),2)} |\n" for y in [2, 3, 5, 8, 10]) + '''
Doubling the time more than halves the monthly amount, because interest does more of the work.

## Where to keep goal savings

| Time to goal | Suitable options |
|---|---|
| Under 1 year | Savings account, liquid fund, short FD |
| 1–3 years | FDs, RDs, short-term debt funds |
| 3–5 years | Mix of debt and hybrid funds |
| Over 5 years | Mostly diversified equity funds |

The closer the goal, the less risk you can take, because there is no time to recover from a market fall.

## The 50/30/20 budget

A simple way to find money for goals: spend about 50% of take-home pay on needs, 30% on wants and put **20% into savings** and debt repayment. Automate the transfer on payday so you save before you spend.

## Emergency fund first

Before saving for a holiday or a car, build an emergency fund of 3–6 months of expenses. Use this calculator with that amount as your first goal.
''', [
 ('Should I save or pay off debt first?', 'Pay off high-interest debt such as credit cards first, while keeping a small emergency fund. Low-interest debt like a home loan can be paid alongside saving.'),
 ('What if I can only save irregularly?', 'Use the monthly figure as your target and top up when you can. Even partial progress compounds.'),
], before='## Tips')

# ---------------- simple interest
expand('finance/simple-interest', '''
## Simple interest table (per 10,000)

| Rate | 1 year | 3 years | 5 years |
|---|---|---|---|
''' + ''.join(f"| {r}% | {f(10000*r/100)} | {f(10000*r/100*3)} | {f(10000*r/100*5)} |\n" for r in [4, 6, 8, 10, 12, 18]) + '''
## Interest for days

For short periods, banks use the number of days:

<p class="formula">I = P × r × days ÷ 365</p>

Some use 360 days instead. 50,000 at 6% for 90 days is 50,000 × 0.06 × 90 ÷ 365 = **739.73**. Switch the time unit to days in the calculator.

## Finding rate or time

The same formula solves for any value:

- **Rate** = I ÷ (P × t)
- **Time** = I ÷ (P × r)
- **Principal** = I ÷ (r × t)

In the calculator, just press × on the value you want and fill in the others.

## Simple interest in exams

Questions often ask how long money takes to double at simple interest. Since doubling means interest equals principal, **t = 1 ÷ r**. At 8% simple interest, money doubles in 12.5 years. At compound interest it takes only about 9 years.
''', [
 ('How do I calculate monthly simple interest?', 'Divide the yearly interest by 12. 50,000 at 6% earns 3,000 a year, or 250 a month.'),
 ('Is simple interest better for borrowers?', 'Yes. On the same rate and term, simple interest costs less than compound interest because interest is never charged on interest.'),
], before='## Where simple interest is used')

# ---------------- SIP
expand('finance/sip', '''
## SIP vs lump sum

| | SIP | Lump sum |
|---|---|---|
| Invests | A fixed amount every month | Everything at once |
| Best when | You invest from monthly income | You already have the money |
| Market timing risk | Low — buys at many prices | High — one entry price |
| Rupee cost averaging | Yes | No |

Use the [lumpsum calculator](/finance/lumpsum/) to compare, or combine both: invest a lump sum and run a SIP alongside it.

## Rupee cost averaging

A SIP buys more units when prices are low and fewer when they are high. Over time your average cost per unit is lower than the average price over the same period. It does not guarantee a profit, but it removes the stress of timing the market.

## How much to invest for common goals

12% expected return:

| Goal | Years | Monthly SIP |
|---|---|---|
''' + ''.join(f"| {f(g)} | {y} | {f(g/(((1+.01)**(12*y)-1)/.01*1.01))} |\n" for g, y in [(1000000, 5), (1000000, 10), (5000000, 15), (10000000, 20), (10000000, 25)]) + '''
## Raise your SIP every year

Increasing your SIP by 10% every year can nearly double the final corpus over 20 years. See the [step-up SIP calculator](/finance/step-up-sip/).

## When to stop or pause

- Do **not** stop a SIP just because markets fall — that is when it buys the most units.
- Review the fund once a year against its benchmark.
- Shift to safer funds 2–3 years before you need the money.
''', [
 ('What is the minimum SIP amount?', 'Many mutual funds allow SIPs from 100 to 500 a month, so you can start small and increase later.'),
 ('Can I withdraw from a SIP anytime?', 'Yes, for most open-ended funds, though an exit load may apply in the first year. ELSS tax-saving funds have a 3-year lock-in for each instalment.'),
], before='## Keep in mind')

for c in ['hourly-to-salary', 'inflation', 'loan-payment', 'mortgage', 'present-value', 'profit-margin', 'retirement-corpus', 'roi', 'salary-increase', 'sales-tax-vat', 'savings-goal', 'simple-interest', 'sip']:
    print(c, words('finance/' + c))
