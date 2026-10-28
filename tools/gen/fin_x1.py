import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
f = lambda x, d=0: f"{x:,.{d}f}"

# ---------------- break-even
rows = ''.join(f"| {f(p)} | {f(p-15)} | {f(math.ceil(50000/(p-15)))} | {f(math.ceil(50000/(p-15))*p)} |\n" for p in [25, 30, 40, 50, 60, 80])
expand('finance/break-even', f'''
## How price changes the break-even point

Fixed costs of 50,000 and a variable cost of 15 per unit:

| Selling price | Contribution per unit | Break-even units | Break-even revenue |
|---|---|---|---|
{rows}
A higher price cuts the number of units you must sell sharply, because every extra unit of price goes straight to contribution. It may also reduce demand, so test prices carefully.

## Break-even for a target profit

To find the sales needed to earn a target profit, add the profit to fixed costs:

<p class="formula">Units = (Fixed costs + Target profit) ÷ (Price − Variable cost)</p>

With fixed costs of 50,000, a price of 40, a variable cost of 15 and a target profit of 25,000: (50,000 + 25,000) ÷ 25 = **3,000 units**. In the calculator, simply type 75,000 as the fixed costs.

## Break-even for a service business

Services rarely have “units”. Use **hours** or **clients** instead:

- **Price** = your hourly rate or the average fee per client.
- **Variable cost** = costs that rise with each hour or client (materials, travel, payment fees).
- **Fixed costs** = rent, software, insurance and your own salary target for the month.

A consultant with 3,000 of monthly fixed costs, charging 60 an hour with 5 of variable cost per hour, breaks even at 3,000 ÷ 55 ≈ **55 billable hours** a month.

## Common mistakes

- **Leaving out your own pay.** If you plan to draw a salary, it is a fixed cost.
- **Mixing periods.** Monthly fixed costs need monthly sales figures.
- **Ignoring semi-variable costs.** Electricity or staff overtime rise with volume only above a point. Split them into fixed and variable parts.
- **Assuming one product.** With several products, use a weighted average contribution margin.
''', [
 ('How do I calculate break-even in revenue directly?', 'Divide fixed costs by the contribution margin ratio, (price − variable cost) ÷ price. With fixed costs of 50,000 and a 62.5% margin ratio, break-even revenue is 80,000.'),
 ('What is a good margin of safety?', 'Above 20–30% is comfortable for most small businesses. It means sales could fall that much before you start making a loss.'),
], before='## Margin of safety')

# ---------------- CAGR
def cagr(s, e, t): return (e/s)**(1/t)-1
rows = ''.join(f"| {f(s)} → {f(e)} | {t} years | {cagr(s,e,t)*100:.2f}% |\n" for s, e, t in [(10000, 20000, 5), (10000, 20000, 10), (50000, 150000, 8), (100, 80, 3), (1000, 5000, 15)])
expand('finance/cagr', f'''
## CAGR examples

| Start → End | Period | CAGR |
|---|---|---|
{rows}
A negative CAGR means the value shrank on average each year.

## Where CAGR is used

- **Investments**: comparing mutual funds, stocks or property bought at different times.
- **Business growth**: revenue, users or profit growth over several years in annual reports.
- **Economics**: GDP and population growth rates.
- **Planning**: projecting a value forward at a steady growth rate — press × on Ending value and enter a CAGR.

## CAGR vs absolute return vs XIRR

| Measure | What it tells you | Best for |
|---|---|---|
| Absolute return | Total % gain, ignoring time | Holdings under a year |
| CAGR | Steady yearly rate from start to end | One lump sum, held for years |
| XIRR | Yearly rate with many cash flows | SIPs, top-ups, withdrawals |

If you invested through a SIP, CAGR on the total invested understates or overstates the true return. Use XIRR instead.

## Common mistakes

- **Using months as years.** Enter 18 months as 1.5 years, or switch the unit to months.
- **Dividing the total return by years.** A 100% gain over 10 years is a 7.18% CAGR, not 10% a year.
- **Ignoring dividends.** For stocks, include reinvested dividends in the ending value to get total-return CAGR.
''', [
 ('What is a good CAGR?', 'It depends on the asset. Over long periods, 6–8% is typical for bonds and deposits, and 10–12% for diversified equity funds. Compare against a relevant benchmark rather than a fixed number.'),
 ('Can CAGR be negative?', 'Yes. If the ending value is below the starting value the CAGR is negative, showing the average yearly decline.'),
], before='## Limits of CAGR')

# ---------------- compound interest
P = 10000
rows = ''.join(f"| {t} | {f(P*1.075**t,2)} | {f(P*(1+.075*t),2)} | {f(P*1.075**t-P*(1+.075*t),2)} |\n" for t in [1, 5, 10, 20, 30])
expand('finance/compound-interest', f'''
## Compound vs simple interest

10,000 at 7.5% a year, compounded yearly versus simple interest:

| Years | Compound | Simple | Extra from compounding |
|---|---|---|---|
{rows}
For the first few years the difference is small. Over decades, interest on interest becomes the larger part of the total.

## Adding regular deposits

This calculator handles a single deposit. If you also add money every month, use the [SIP calculator](/finance/sip/) for the monthly part and add the two results together. For a goal-based plan, try the [savings goal calculator](/finance/savings-goal/).

## Continuous compounding

As compounding becomes more frequent, the result approaches a limit called continuous compounding:

<p class="formula">A = P × e<sup>r × t</sup></p>

10,000 at 7.5% for 5 years gives {f(P*math.exp(.075*5),2)}, only slightly more than daily compounding. In practice, monthly or daily compounding is close enough.

## Effective annual rate (EAR)

Banks may quote the same nominal rate with different compounding. Compare them with the effective annual rate:

<p class="formula">EAR = (1 + r ÷ n)<sup>n</sup> − 1</p>

7.5% compounded monthly is an EAR of {((1+.075/12)**12-1)*100:.3f}%. Quarterly gives {((1+.075/4)**4-1)*100:.3f}%.
''', [
 ('What is the difference between APR and APY?', 'APR is the nominal yearly rate. APY (or EAR) includes compounding, so it shows what you actually earn in a year. A 7.5% APR compounded monthly is about a 7.76% APY.'),
 ('Does compound interest work against me on loans?', 'Yes. Credit cards and many loans compound interest, so unpaid interest itself starts earning interest. Paying more than the minimum stops this.'),
], before='## Things to keep in mind')

# ---------------- credit card
expand('finance/credit-card-payoff', '''
## Avalanche vs snowball

If you have several cards, choose an order to pay them off:

| Method | Pay extra on | Advantage |
|---|---|---|
| **Avalanche** | Highest APR first | Lowest total interest |
| **Snowball** | Smallest balance first | Quick wins keep you motivated |

Make the minimum payment on every card and put every extra amount on the target card. When it is paid off, roll its payment into the next one.

## How minimum payments trap you

Card issuers usually set the minimum at 1–3% of the balance plus interest. As the balance falls, so does the minimum, which stretches repayment over many years. Paying a **fixed amount** each month, as this calculator assumes, clears the debt much faster.

## Is a balance transfer worth it?

A 0% balance transfer can save a lot of interest, but check:

- The **transfer fee**, often 3–5% of the balance.
- How long the **0% period** lasts and the APR after it ends.
- Whether you can clear the balance **within** the promotional period. Set the APR to 0 and the time to the promo length to see the monthly payment needed.

## Warning signs

- You only ever pay the minimum.
- Your balance grows even though you are paying.
- You use one card to pay another.

If this sounds familiar, speak to a not-for-profit debt advice service before taking on new credit.
''', [
 ('Should I pay off my credit card or save?', 'Usually pay the card first. Card interest of 20% or more is far higher than savings rates. Keep a small emergency fund so you do not need the card again.'),
 ('Does paying twice a month help?', 'Slightly. Interest is often charged on the average daily balance, so paying earlier in the month reduces it. The bigger win is paying more in total.'),
])

# ---------------- discount
rows = ''.join(f"| {f(p)} | {f(p*.9,2)} | {f(p*.8,2)} | {f(p*.75,2)} | {f(p*.6,2)} | {f(p*.5,2)} |\n" for p in [20, 50, 80, 100, 250, 500])
expand('finance/discount', f'''
## Discount table

| Price | 10% off | 20% off | 25% off | 40% off | 50% off |
|---|---|---|---|---|---|
{rows}
## Discount plus sales tax

Tax is usually charged on the **discounted** price. An 80 item at 25% off with 8% tax:

- Discounted price = 80 × 0.75 = 60
- Tax = 60 × 0.08 = 4.80
- Total = **64.80**

Use the [sales tax calculator](/finance/sales-tax-vat/) for the second step.

## Quick mental maths

- **10% off**: move the decimal point one place left and subtract. 10% of 80 is 8.
- **20% off**: double the 10% figure. **25% off**: divide by 4.
- **15% off**: 10% plus half of 10%.
- **“Buy one, get one 50% off”** is 25% off the pair.
- **“Buy 2, get 1 free”** is 33.3% off three items.

## Is it really a deal?

- Compare the **final price** with other shops, not the claimed original price.
- Check the **unit price** for multi-packs with the [unit price calculator](/everyday-life/unit-price/).
- A coupon worth a fixed amount beats a percentage off on cheaper items, and the reverse on expensive ones.
''', [
 ('How do I find the original price from the sale price?', 'Divide the sale price by (1 − discount). An item selling for 60 after 25% off was originally 60 ÷ 0.75 = 80. In the calculator, press × on Original price and type the sale price.'),
 ('Is 30% off better than a 25-off coupon?', 'It depends on the price. On items above about 83, 30% off saves more; below that the fixed 25 saves more.'),
], before='## Discount vs markup')

# ---------------- dividend yield
rows = ''.join(f"| {y}% | {f(100000*y/100)} | {f(100000*y/100/12,2)} |\n" for y in [2, 3, 4, 5, 6])
expand('finance/dividend-yield', f'''
## Income from 100,000 invested

| Dividend yield | Yearly income | Per month |
|---|---|---|
{rows}
## Typical yields by sector

| Sector | Usual yield range |
|---|---|
| Technology, growth stocks | 0–1.5% |
| Consumer goods | 1–3% |
| Banks and financials | 2–5% |
| Utilities, energy, REITs | 3–7% |

Ranges change with markets. A yield far above its sector often means the share price has fallen because the market expects a dividend cut.

## Payout ratio

The payout ratio shows how much of the profit is paid out:

<p class="formula">Payout ratio = Dividend per share ÷ Earnings per share</p>

A ratio of 30–60% is usually sustainable. Above 80–100% the company is paying more than it earns, which cannot last.

## Dividend growth

A lower yield that grows every year can beat a high flat yield over time. A 2% yield growing 10% a year pays more than a flat 4% yield after about 8 years, and the share price usually rises with the dividend.

## Tax on dividends

Dividends are usually taxable as income in the year you receive them. Rates and allowances differ by country, so check local rules before comparing yields with tax-free options.
''', [
 ('What is forward vs trailing dividend yield?', 'Trailing yield uses dividends paid over the last 12 months. Forward yield uses the expected dividends for the next 12 months. Use the same type when comparing shares.'),
 ('Why did my dividend yield change when the dividend did not?', 'Because yield is dividend ÷ price. When the share price rises the yield falls, and when the price falls the yield rises.'),
], before='## Things to check')

# ---------------- doubling time
rows = ''.join(f"| {r}% | {math.log(2)/math.log(1+r/100):.1f} | {math.log(3)/math.log(1+r/100):.1f} | {math.log(10)/math.log(1+r/100):.1f} |\n" for r in [3, 5, 7, 9, 12, 15])
expand('finance/doubling-time', f'''
## Time to double, triple and grow 10×

| Return | Double (years) | Triple | 10× |
|---|---|---|---|
{rows}
For tripling there is a similar shortcut, the **rule of 114** (114 ÷ rate). For 10× growth use about 230 ÷ rate.

## Rule of 69 and 70

The rule of 72 is easiest to use because 72 divides evenly by many numbers. For other cases:

- **Rule of 70**: slightly more accurate for low rates (1–5%), often used for population and GDP growth.
- **Rule of 69.3**: exact for continuous compounding, because ln 2 ≈ 0.693.

## Inflation halves your money too

At 6% inflation, prices double in about 12 years, which means your money's buying power **halves** in that time. If your savings earn less than inflation, they are losing value even as the balance grows.

## Real-life uses

- **Investing**: how long until a lump sum doubles at a given return.
- **Debt**: a credit card at 24% APR doubles an unpaid balance in about 3 years.
- **Business**: how long until sales double at a given growth rate.
- **Population**: a 2% yearly growth rate doubles a population in about 35 years.
''', [
 ('How many years does it take to double money at 7%?', 'Exactly 10.24 years with yearly compounding. The rule of 72 gives 72 ÷ 7 ≈ 10.3 years.'),
 ('What return do I need to double my money in 5 years?', 'About 14.87% a year. The rule of 72 gives 72 ÷ 5 = 14.4%.'),
], before='## Doubling again and again')

for c in ['break-even', 'cagr', 'compound-interest', 'credit-card-payoff', 'discount', 'dividend-yield', 'doubling-time']:
    print(c, words('finance/' + c))
