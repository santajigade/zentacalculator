"""Part C expansion (2026-11-20): 25 priority pages (crawled, not indexed) plus 5 from the top of the backlog, brought to the api-gravity standard. Assembled from six sections; edits are applied in place by inplace.edit. Run once on the original files."""

# ======================================================================= SECTION _expand_c1.py
"""Expand (2026-11-20), slice 1: lpg-cylinder, wallpaper, sales-tax-vat, retirement-corpus, hourly-to-salary.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-20'


def edit_keep_featured(cid, **kw):
    """The page is already featured. Lift the flag around the edit and restore it unchanged."""
    path = os.path.join(inplace.BASE, cid + '.mdx')
    s = open(path).read()
    line = 'featured: true\n'
    assert s.count(line) == 1, cid
    open(path, 'w').write(s.replace(line, '', 1))
    try:
        n = edit(cid, **kw)
    except Exception:
        open(path, 'w').write(s)
        raise
    t = open(path).read()
    k = t.index('\nupdated: ')
    k = t.index('\n', k + 1) + 1
    open(path, 'w').write(t[:k] + line + t[k:])
    return n


def c(x, d=0):
    return f"{x:,.{d}f}"


# ---------------------------------------------------------------- LPG cylinder
kg, hrs, rate = 14.2, 2.0, 150.0
per = hrs * rate / 1000
days = kg / per
LHV = 46.0  # MJ/kg, typical LPG net calorific value
E_MJ = kg * LHV
E_kWh = E_MJ / 3.6
gph_per_kW = 3600 / LHV  # g/h per kW of heat input
k_rows = ''
for kw in (1.0, 1.5, 2.0, 2.5, 3.0):
    g = kw * gph_per_kW
    d = kg / (hrs * g / 1000)
    k_rows += f"| {kw:.1f} kW | {g:.0f} g/h | {hrs * g:.0f} g | {d:.0f} days |\n"
# weighing check: gross 27.0 kg, tare 15.5 kg (example values stamped on a cylinder)
gross, tare = 27.0, 15.5
left = gross - tare
left_days = left / per
# family with two burners: 1.5 h big at 200 g/h + 1 h small at 100 g/h
mix = (1.5 * 200 + 1.0 * 100) / 1000
mix_days = kg / mix
# 19 kg commercial cylinder in a small eatery: 8 h a day at 250 g/h
com = 19 / (8 * 250 / 1000)

edit('other/lpg-cylinder', date=U, phrase='lpg gas cylinder duration calculator',
     intro=("How long an LPG cylinder lasts depends on how much gas it holds and how many grams your burners burn each day. "
            "This LPG gas cylinder duration calculator turns burner hours and consumption into daily use and the number of days until the cylinder is empty.\n\n"
            "Households use it to plan the next refill booking, and small restaurants and canteens use it to compare cylinder sizes and spot a burner that is using more gas than it should."),
     body_add=f'''
## Worked example with the default values

The defaults are a **{kg} kg** domestic cylinder, **{hrs:g} burner hours a day** and a burner that uses **{rate:g} g per hour**:

- Gas used per day = {hrs:g} × {rate:g} ÷ 1,000 = **{per:.1f} kg** ({per*1000:.0f} g)
- Days the cylinder lasts = {kg} ÷ {per:.1f} = {days:.2f}, shown as **{days:.0f} days**

Most kitchens run more than one burner. If the big burner runs 1.5 hours a day at 200 g/h and the small one 1 hour at 100 g/h, daily use is {mix*1000:.0f} g and the same cylinder lasts about **{mix_days:.0f} days**. Enter the combined grams per hour and 1 hour a day, or work out each burner and add them.

## Burner rating and days per cylinder

Stove makers often state heat input in kW rather than grams per hour. LPG releases roughly {LHV:g} MJ per kg, so each kW of heat input burns about {gph_per_kW:.0f} g per hour. A full {kg} kg cylinder holds about {E_MJ:,.0f} MJ, or {E_kWh:.0f} kWh of heat. At {hrs:g} hours a day of full flame:

| Burner heat input | Gas per hour | Gas per day | {kg} kg lasts |
|---|---|---|---|
{k_rows}
A commercial 19 kg cylinder feeding a 250 g/h burner for 8 hours a day lasts only about **{com:.1f} days**, which is why eateries keep a spare cylinder connected through a changeover valve.

## Checking how much gas is left

The only reliable way is to weigh the cylinder. The tare (empty) weight is stamped on the collar or handle. For example, a cylinder that weighs {gross:g} kg on a bathroom scale with a stamped tare of {tare:g} kg holds {left:.1f} kg of gas, enough for about {left_days:.0f} more days at {per*1000:.0f} g a day. Weighing it again after a week gives your real consumption, which is a better input than any rating plate: enter the grams used per day directly and leave the burner fields as they are.

## Common mistakes

- **Using the full rated consumption for simmering.** A burner on low flame may use a third of its rated gas, so rating plate figures overstate use for slow cooking.
- **Counting burner hours once when two burners run together.** Twenty minutes on two burners is forty burner minutes.
- **Mixing up gross and gas weight.** The {kg} kg figure is the gas only; a full domestic cylinder weighs far more because of the steel shell.
- **Expecting the same days in winter.** Cold weather slows vaporisation, so the flame weakens near the end and some liquid can stay in the cylinder, especially with butane-rich gas.
- **Ignoring a dirty or mis-set burner.** A yellow, lazy flame burns gas without heating the pan well, so cooking takes longer and daily use rises.
''',
     faq_add=[('How do I check how much gas is left in my cylinder?',
               f'Weigh the cylinder and subtract the tare weight stamped on its collar. A reading of {gross:g} kg with a tare of {tare:g} kg means {left:.1f} kg of gas, about {left_days:.0f} days at {per*1000:.0f} g a day.'),
              ('How do I convert a burner kW rating to grams per hour?',
               f'Multiply the kW by about {gph_per_kW:.0f}. LPG gives roughly {LHV:g} MJ per kg, so a 2 kW burner on full flame uses about {2*gph_per_kW:.0f} g of gas per hour.')])

# ---------------------------------------------------------------- Wallpaper
P, H, rw, rl, rep = 14.0, 2.5, 0.53, 10.0, 0.0


def wp(P, H, rw, rl, rep):
    drops = math.ceil(P / rw)
    pr = math.floor(rl / (H + rep + 0.1))
    return drops, pr, math.ceil(drops / pr) if pr else None


d0, pr0, r0 = wp(P, H, rw, rl, rep)
cut0 = H + rep + 0.1
# with a 64 cm repeat on a 2.7 m wall
H2, rep2 = 2.7, 0.64
d2, pr2, r2 = wp(P, H2, rw, rl, rep2)
cut2 = H2 + rep2 + 0.1
d2b, pr2b, r2b = wp(P, H2, rw, rl, 0)
# feature wall 3.6 m
df, prf, rf = wp(3.6, H, rw, rl, 0)
# table: rolls by perimeter and height, plain paper
heights = (2.4, 2.5, 2.7, 3.0)
t_rows = ''
for per_m in (8, 12, 16, 20):
    t_rows += f"| {per_m} m | " + ' | '.join(str(wp(per_m, h, rw, rl, 0)[2]) for h in heights) + ' |\n'
# repeat table at 2.5 m
rep_rows = ''
for rp in (0, 0.53, 0.64, 0.75):
    dd, pp, rr = wp(P, H, rw, rl, rp)
    rep_rows += f"| {rp*100:.0f} cm | {H + rp + 0.1:.2f} m | {pp} | {rr} |\n"
# room example: 4.2 m x 3.4 m room
Pr = 2 * (4.2 + 3.4)

edit('construction/wallpaper', date=U, phrase='wallpaper calculator',
     intro=("Wallpaper is sold in rolls of fixed width and length, so the job is really counting full-height strips, called drops, and how many fit in each roll. "
            "This wallpaper calculator works out drops, drops per roll and rolls needed from the wall length, height, roll size and pattern repeat.\n\n"
            "Homeowners use it before ordering so every roll comes from one batch, and decorators use it to quote materials and check how much a large repeat adds."),
     body_add=f'''
## Worked example with the default values

The defaults are **{P:g} m of wall**, **{H:g} m high**, standard **{rw*100:.0f} cm × {rl:g} m** rolls and no pattern repeat:

- Drops = {P:g} ÷ {rw} = {P/rw:.2f}, rounded up to **{d0}**
- Each drop is cut {H:g} + 0.1 = {cut0:.1f} m long, so a roll gives {rl:g} ÷ {cut0:.1f} = {rl/cut0:.2f}, rounded down to **{pr0} drops**
- Rolls = {d0} ÷ {pr0} = {d0/pr0:.1f}, rounded up to **{r0} rolls**

For a room, the wall length is the perimeter: a 4.2 m × 3.4 m bedroom has 2 × (4.2 + 3.4) = {Pr:.1f} m of wall. A single 3.6 m feature wall at {H:g} m needs {df} drops and **{rf} rolls**.

## How the pattern repeat changes the order

Take a {H2} m wall with a {rep2*100:.0f} cm repeat. Each drop is cut {H2} + {rep2} + 0.1 = {cut2:.2f} m, so a {rl:g} m roll gives only **{pr2} drops** and {P:g} m of wall needs **{r2} rolls**, against {r2b} rolls for plain paper. The calculator adds one full repeat to every drop, which is a safe allowance; a careful hanger who matches each new drop to the last can sometimes save a roll on a big job.

At {H:g} m wall height, {P:g} m of wall:

| Pattern repeat | Cut length per drop | Drops per roll | Rolls |
|---|---|---|---|
{rep_rows}
## Rolls needed by perimeter and wall height

Plain paper, {rw*100:.0f} cm × {rl:g} m rolls:

| Wall length | 2.4 m | 2.5 m | 2.7 m | 3.0 m |
|---|---|---|---|---|
{t_rows}
The big step is between 2.4 m and 2.5 m. A 2.4 m wall is cut at exactly 2.5 m, so a {rl:g} m roll gives {wp(1, 2.4, rw, rl, 0)[1]} drops with nothing to spare, and one miscut costs a drop. From 2.5 m up to about 3.2 m a roll gives {wp(1, 3.0, rw, rl, 0)[1]} drops, and above that only {wp(1, 3.3, rw, rl, 0)[1]}, so the number of rolls climbs in steps rather than smoothly with height.

## Measuring a room for wallpaper

Measure each wall along the skirting with a tape, and the height from the top of the skirting to the ceiling or coving at two or three points, using the largest. Walls in older houses are rarely the same height all round. Measure chimney breasts and alcoves along every face, because each return needs its own drops. Read the roll width, length and repeat from the label: the repeat is printed as a figure in cm next to a match symbol.

## Common mistakes

- **Dividing wall area by roll area.** That ignores the offcut left on every roll and usually under-orders by one or two rolls.
- **Using the room width instead of the perimeter.** Enter the total length of every wall to be papered, including returns into window reveals.
- **Forgetting the repeat on an offset (half drop) match.** Use the full repeat printed on the label, not half of it.
- **Ordering exact numbers from different batches.** A later roll from another print run can differ in shade; order a spare from the same batch.
- **Leaving no trim allowance on uneven ceilings.** The 10 cm in the calculator covers normal trimming; add more height if the ceiling line slopes.
''',
     faq_add=[('How many rolls do I need for one feature wall?',
               f'For a 3.6 m wide wall, 2.5 m high, with standard 53 cm by 10 m rolls and no repeat, you need {df} drops at {prf} drops per roll, so {rf} rolls.'),
              ('Does a large pattern repeat always mean more rolls?',
               f'Not always. At 2.5 m height a 10 m roll still gives 3 drops with a repeat of up to 73 cm, so the order stays at {r0} rolls for 14 m of wall. On a 2.7 m wall the same 64 cm repeat drops it to {pr2} drops per roll and {r2} rolls.')])

# ---------------------------------------------------------------- Sales tax / VAT / GST
N, r = 100.0, 0.18
G = N * (1 + r)
T = G - N
wrong = G * (1 - r)
frac_rows = ''
for rr in (0.05, 0.10, 0.18, 0.20, 0.25):
    frac_rows += f"| {rr*100:.0f}% | {1+rr:.2f} | {rr/(1+rr)*100:.2f}% | {100/(1+rr):.4f} |\n"
# invoice: 3 lines at 18%, line rounding vs total rounding
lines = [(3, 12.35), (7, 4.99), (2, 19.95)]
line_tax = [round(q * p * r + 1e-9, 2) for q, p in lines]
net_tot = sum(q * p for q, p in lines)
tax_line = sum(line_tax)
tax_total = round(net_tot * r + 1e-9, 2)
# discount then tax
list_p, disc = 2500.0, 0.10
after = list_p * (1 - disc)
tax_after = after * r
# reverse at 20%: 59.99 inclusive
gi = 59.99
ni = gi / 1.2
vi = gi - ni

edit_keep_featured('finance/sales-tax-vat', date=U, phrase='sales tax / vat / gst calculator',
     intro=("Sales tax, VAT and GST are percentages charged on the price of goods and services, either added at the till or already built into the shelf price. "
            "This sales tax / VAT / GST calculator adds tax to a net price or strips it out of a gross price, and shows the tax amount.\n\n"
            "Shop owners and freelancers use it to price products and write invoices, and buyers use it to check receipts and compare prices quoted with and without tax."),
     body_add=f'''
## Worked example with the default values

The defaults are a net price of **{N:g}** and a tax rate of **{r*100:g}%**:

- Gross = {N:g} × (1 + {r}) = **{G:.2f}**
- Tax = {G:.2f} − {N:g} = **{T:.2f}**

Removing tax works the other way. A price of {gi} including 20% VAT has a net value of {gi} ÷ 1.2 = **{ni:.2f}** and VAT of **{vi:.2f}**. Leave the net price blank and type {gi} into the gross field to get the same split.

## How much of a tax-inclusive price is tax

When a price already includes tax, the tax share of that price is rate ÷ (1 + rate), which is always smaller than the rate itself. Accountants call it the tax fraction; for 20% VAT it is exactly one sixth.

| Tax rate | Multiplier to add tax | Tax share of the gross price | Net for a gross of 100 |
|---|---|---|---|
{frac_rows}
## Discounts and invoices in practice

Tax is normally charged on the price actually paid, so apply the discount first. An item listed at {list_p:,.0f} with a {disc*100:.0f}% discount costs {after:,.0f} before tax, then {tax_after:,.2f} of tax at {r*100:g}%, for a total of **{after+tax_after:,.2f}**.

On invoices, the rounding rule matters. Take three lines at {r*100:g}%: 3 × 12.35, 7 × 4.99 and 2 × 19.95, a net total of {net_tot:.2f}. Rounding the tax on each line gives {' + '.join(f'{t:.2f}' for t in line_tax)} = **{tax_line:.2f}**, while rounding once on the total gives **{tax_total:.2f}**. Both are accepted in most systems, but an invoice must use one rule consistently and the tax figure must match the sum shown.

## Common mistakes

- **Taking the rate off the gross price.** {G:.0f} less {r*100:g}% is {wrong:.2f}, not {N:g}; divide by {1+r:.2f} instead.
- **Applying tax before a discount.** Unless local rules say otherwise, tax follows the discounted price.
- **Entering 18 instead of 18% in a spreadsheet.** A rate of 18 multiplies the price by 19; the calculator takes the percent sign for you.
- **Charging tax on a price that already includes it.** Adding {r*100:g}% to a gross of {G:.0f} gives {G*(1+r):.2f}, taxing the tax; check which price you start from.
- **Treating a tax-inclusive quote as net.** Check whether a supplier quote says "plus VAT" or "incl. GST" before comparing two offers.
''',
     faq_add=[('If I add 18% and then take 18% off, why do I not get back to the same price?',
               f'Because the second 18% is taken from a bigger number. 100 plus 18% is {G:.0f}, but {G:.0f} less 18% is {wrong:.2f}. To undo the tax, divide {G:.0f} by 1.18, which gives 100 exactly.'),
              ('What fraction of a VAT-inclusive price is VAT?',
               'The tax share is rate divided by (1 + rate). At 20% VAT that is 0.2 / 1.2, exactly one sixth of the gross price; at 18% GST it is about 15.25%.')])

# ---------------------------------------------------------------- Retirement corpus
E, inf, t, w = 600000.0, 0.06, 25, 0.04
Er = E * (1 + inf) ** t
K = Er / w
K_today = K / (1 + inf) ** t
mult = 1 / w
# monthly SIP to build K at 12% a year, monthly compounding as the SIP page
ra = 0.12
i = ra / 12
n = 12 * t
fv1 = ((1 + i) ** n - 1) / i * (1 + i)
sip = K / fv1
# with existing savings of 20,00,000 growing at 10% for 25 years
S0, gs = 2000000.0, 0.10
S_fv = S0 * (1 + gs) ** t
gap = K - S_fv
sip_gap = gap / fv1
# sensitivity table: inflation 5/6/7%, withdrawal 3/3.5/4%
s_rows = ''
for f in (0.05, 0.06, 0.07):
    e_ = E * (1 + f) ** t
    s_rows += f"| {f*100:.0f}% | {c(e_)} | " + ' | '.join(c(e_ / ww) for ww in (0.04, 0.035, 0.03)) + ' |\n'
K7 = E * 1.07 ** t / w
K5 = E * 1.05 ** t / w

edit('finance/retirement-corpus', date=U, phrase='retirement corpus calculator',
     intro=("Your retirement corpus is the sum you need saved on the day you stop working, so that withdrawals can pay your living costs for the rest of your life. "
            "This retirement corpus calculator inflates today's annual expenses to your retirement year and divides them by a safe withdrawal rate.\n\n"
            "Salaried savers and people planning early retirement use it to set a savings target, and financial planners use it to show clients how inflation and the withdrawal rate change that target."),
     body_add=f'''
## What the default answer means

With the defaults (600,000 a year of expenses, {inf*100:g}% inflation, {t} years, {w*100:g}% withdrawal) the calculator shows expenses at retirement of **{c(Er)}** a year and a corpus of **{c(K)}**. That looks enormous, but in today's money it is {c(K)} ÷ {1+inf}^{t} = **{c(K_today)}**, exactly {mult:.0f} times today's expenses. The rest of the number is inflation, not extra spending.

## From corpus to monthly saving

A target is only useful once it becomes a monthly figure. Using the same formula as the [SIP calculator](/finance/sip/), building {c(K)} over {t} years at an assumed {ra*100:g}% a year needs about **{c(sip)} a month**. If you already hold {c(S0)} that grows at {gs*100:g}% a year, it reaches {c(S_fv)} by retirement, the gap falls to {c(gap)}, and the monthly saving drops to about **{c(sip_gap)}**. These returns are assumptions for illustration, not forecasts.

## How sensitive the corpus is

Corpus needed for 600,000 of expenses today, {t} years to retirement:

| Inflation | Expenses at retirement | Corpus at 4% | Corpus at 3.5% | Corpus at 3% |
|---|---|---|---|---|
{s_rows}
One point of inflation either way moves the 4% corpus from {c(K5)} to {c(K7)}, a bigger swing than most people expect. Choosing the withdrawal rate matters just as much: going from 4% to 3% raises the target by a third.

## Building a realistic expense figure

Planners usually start from 12 months of bank and card statements rather than a guess. Split spending into essentials (food, utilities, insurance, rent or maintenance), lifestyle (travel, dining) and one-off items such as a car or a wedding. Remove costs that end at retirement, add expected medical cover, and treat big one-off goals as separate targets rather than folding them into the yearly figure.

## Common mistakes

- **Using today's expenses as the final figure.** The corpus must be built on expenses in the retirement year, which is what the inflation step does.
- **Mixing real and nominal returns.** If you plan with inflated expenses, compare them with nominal investment returns, not returns after inflation.
- **Counting EPF or pension twice.** Either subtract the pension from yearly expenses or subtract its value from the corpus, not both.
- **Treating 4% as guaranteed.** It is a historical guideline from US markets; a poor run of returns early in retirement can shorten the life of the corpus.
- **Leaving out healthcare.** Medical costs and insurance premiums often rise faster than general inflation and grow with age.
''',
     faq_add=[('What is the retirement corpus worth in today\'s money?',
               f'Divide the corpus by (1 + inflation) to the power of the years. The default corpus of {c(K)} is worth {c(K_today)} today, which is simply 25 times the current 600,000 of expenses at a 4% withdrawal rate.'),
              ('How much does a 1% change in inflation change the corpus?',
               f'A lot, because it compounds over every year to retirement. For 600,000 of expenses and 25 years at a 4% withdrawal rate, 5% inflation needs {c(K5)} while 7% needs {c(K7)}.')])

# ---------------------------------------------------------------- Hourly to salary
h, hpw, wpy = 25.0, 40.0, 52.0
W = h * hpw
A = W * wpy
M = A / 12
bi = A / 26
semi = A / 24
daily = h * 8
hours_yr = hpw * wpy
four_weeks = 4 * W
# salaried 52,000 but 48 paid weeks equivalent: effective hourly when 4 weeks unpaid
eff = A / (hpw * 48)
# 60,000 salary, 45 h actual week -> real hourly
S2, h2 = 60000.0, 45.0
real_h = S2 / (h2 * 52)
nom_h = S2 / (40 * 52)
p_rows = ''
for hr in (15, 20, 25, 35, 50):
    a = hr * hpw * wpy
    p_rows += f"| {hr} | {c(hr*8)} | {c(hr*hpw)} | {c(a/26, 2)} | {c(a/24, 2)} | {c(a/12, 2)} |\n"

edit_keep_featured('finance/hourly-to-salary', date=U, phrase='hourly to salary calculator',
     intro=("An hourly wage and an annual salary describe the same pay in different units, linked by the hours you work each week and the weeks you are paid each year. "
            "This hourly to salary calculator converts an hourly rate to weekly, monthly and yearly pay, or a salary back to an hourly figure.\n\n"
            "Job seekers use it to compare hourly and salaried offers, and freelancers and employers use it to set rates and budget payroll."),
     body_add=f'''
## Pay per period at the default 40 hours and 52 weeks

The defaults ({h:g} an hour, {hpw:g} hours, {wpy:g} weeks) give **{c(W)}** a week, **{c(A)}** a year and **{c(M, 2)}** a month, over {c(hours_yr)} paid hours. Payroll rarely runs monthly everywhere, so the same salary splits differently by pay schedule:

| Hourly | Daily (8 h) | Weekly | Biweekly (26 pays) | Semi-monthly (24 pays) | Monthly |
|---|---|---|---|---|---|
{p_rows}
At {h:g} an hour, a biweekly cheque is {c(bi, 2)} and a semi-monthly one is {c(semi, 2)}. Both add up to {c(A)} over the year; the difference is only the number of pay days.

## Real hourly pay from a salary

A salary hides the hours behind it. A salary of {c(S2)} looks like {c(nom_h, 2)} an hour on a 40-hour week, but if the job really takes {h2:g} hours every week it pays **{c(real_h, 2)}** an hour. To check, type the salary into Annual salary, set hours per week to what you actually work, and press × on Hourly rate.

Unpaid leave works the same way. If {c(A)} is earned in 48 working weeks, set weeks to 48 and the hourly equivalent rises to {c(eff, 2)}; if the 4 weeks off are unpaid, keep the hourly rate and the annual pay falls to {c(h*hpw*48)}.

## Common mistakes

- **Treating a month as four weeks.** A year has about 4.33 weeks per month, so {h:g} an hour for 40 hours is {c(M, 2)} a month, not {c(four_weeks)}.
- **Comparing gross salary with take-home hourly pay.** Convert both offers before tax, or both after tax, never one of each.
- **Using contracted hours when you work longer.** Regular unpaid overtime lowers the real hourly rate of a salaried job.
- **Forgetting paid holidays in an hourly job.** If holidays are unpaid, reduce the weeks worked; at 48 weeks, {h:g} an hour is {c(h*hpw*48)} a year.
- **Ignoring benefits.** Pension contributions, health cover and bonuses can be worth a large share of base pay and are not in this conversion.
''',
     faq_add=[('Why is my monthly pay not four times my weekly pay?',
               f'Most months are longer than four weeks. A year of 52 weeks spread over 12 months is about 4.33 weeks a month, so {c(W)} a week is {c(M, 2)} a month rather than {c(four_weeks)}.'),
              ('How do I find my real hourly rate on a salary?',
               f'Divide the salary by the hours you actually work in a year. A {c(S2)} salary for {h2:g} hours a week over 52 weeks is {c(real_h, 2)} an hour, against {c(nom_h, 2)} on a 40-hour week.')])

print('slice 1 done')

# ======================================================================= SECTION _expand_c2.py
"""Expand (2026-11-20), slice 2: buoyancy, cgpa-to-percentage, concrete-mix, coffee-ratio, protein-intake.
Numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-20'
g0 = 9.80665


def edit_keep_featured(cid, **kw):
    """The page is already featured. Lift the flag around the edit and restore it unchanged."""
    path = os.path.join(inplace.BASE, cid + '.mdx')
    s = open(path).read()
    line = 'featured: true\n'
    assert s.count(line) == 1, cid
    open(path, 'w').write(s.replace(line, '', 1))
    try:
        n = edit(cid, **kw)
    except Exception:
        open(path, 'w').write(s)
        raise
    t = open(path).read()
    k = t.index('\nupdated: ')
    k = t.index('\n', k + 1) + 1
    open(path, 'w').write(t[:k] + line + t[k:])
    return n


# ---------------------------------------------------------------- Buoyancy
V, rf, m = 0.010, 1000.0, 8.0
Fb = rf * g0 * V
W = m * g0
Wa = W - Fb
ro = m / V
# extra load before the default object sinks: displaced water mass minus its mass
spare = rf * V - m
# rock weighed in air and water
ma, mw = 2.65, 1.65
Vr = (ma - mw) / 1.0  # litres, fresh water 1 kg/L
rho_r = ma / Vr * 1000
# lift bag for a 50 kg steel anchor in seawater
ms, rs, rsw = 50.0, 7850.0, 1025.0
Vs = ms / rs
Fs = rsw * g0 * Vs
Ws = ms * g0
app = Ws - Fs
Vbag = app / (rsw * g0)
# raft: 4 drums of 200 L, empty mass 18 kg each, raft deck 40 kg
nd, vd, md, deck = 4, 0.200, 18.0, 40.0
cap = nd * vd * 1000 - nd * md - deck
b_rows = ''
for name, rho in (('Fresh water', 1000.0), ('Seawater', 1025.0), ('Dead Sea brine', 1240.0)):
    disp = rho * nd * vd
    b_rows += f"| {name} | {rho:,.0f} kg/m³ | {disp:,.0f} kg | {disp - nd*md - deck:,.0f} kg |\n"

edit('physics/buoyancy', date=U, phrase='buoyancy calculator',
     intro=("Any object in a fluid is pushed upward by a force equal to the weight of the fluid it displaces, which is Archimedes' principle. "
            "This buoyancy calculator gives that buoyant force, the weight and apparent weight, the average density and, for a floating object, the share of its volume below the surface.\n\n"
            "Students use it for physics problems, divers and boat builders use it to size weights, floats and lift bags, and engineers use it for displacer level instruments."),
     body_add=f'''
## Reading the default result

With the defaults the object displaces {V*1000:g} L of fresh water, so the water pushes up with **{Fb:.2f} N** while gravity pulls down with **{W:.2f} N**. The apparent weight of **{Wa:.2f} N** is negative, which means a hand would have to push down with {-Wa:.2f} N to hold it under. Let go and it rises until only {ro/rf*100:.0f}% of its volume, {ro/rf*V*1000:g} L, is below the surface. The same object could carry another **{spare:.0f} kg** before it sank completely.

## Finding density by weighing in water

A rock reads {ma} kg on a hanging scale in air and {mw} kg fully under fresh water. The loss of {ma-mw:.2f} kg is the mass of water displaced, so its volume is {Vr:.2f} L and its density is {ma} ÷ {Vr/1000:.3f} = **{rho_r:,.0f} kg/m³**, typical of quartz and granite. Enter a volume of {Vr:g} L, a fluid density of 1,000 and a mass of {ma} kg to check it: the apparent weight comes out at {mw*g0:.2f} N, which is {mw} kg × g.

## Sizing a lift bag

A {ms:g} kg steel anchor lies on the seabed. Its volume is {ms:g} ÷ {rs:,.0f} = {Vs*1000:.2f} L, so seawater supports only {Fs:.1f} N of its {Ws:.1f} N weight and it still pulls down with **{app:.1f} N**. A lift bag must displace at least {app:.1f} ÷ ({rsw:,.0f} × 9.81) = **{Vbag*1000:.1f} L** of seawater to make it neutral, so divers use a 50 L or larger bag and let air out as it rises, because the air in the bag expands as the pressure falls.

## Payload of a drum raft

Four {vd*1000:.0f} L drums ({md:g} kg each) under a {deck:g} kg deck can displace {nd*vd*1000:.0f} kg of fresh water when fully submerged. Subtracting the raft's own mass leaves the load it can carry before the drums go under:

| Water | Density | Mass displaced (drums under) | Payload before sinking |
|---|---|---|---|
{b_rows}
In practice keep the drums no more than about half submerged, which roughly halves the payload, so the raft keeps freeboard and stability in waves.

## Buoyancy in level and density instruments

A [displacer level transmitter](https://www.instrumentationblog.in/displacer-level-transmitter-working-principle/) hangs a long cylinder in the vessel; as the liquid rises the buoyant force on it grows, and a torque tube or spring measures the drop in apparent weight. Hydrometers use the opposite idea: a fixed weight floats deeper in a lighter liquid, and the stem scale reads density or specific gravity directly.

## Common mistakes

- **Entering the object's mass in place of its displaced volume.** Buoyancy depends only on the volume below the surface, not on what the object is made of.
- **Using the whole volume for a floating object.** A partly floating body displaces only its submerged part; enter that volume to get the force actually acting.
- **Forgetting the fluid changes.** Seawater gives about 2.5% more lift than fresh water, so ballast trimmed in a lake is too light at sea.
- **Mixing litres and cubic metres.** 1 L is 0.001 m³; a slip here makes the force 1,000 times wrong.
- **Treating hollow objects by their material density.** A steel tank floats if its average density, including the air inside, is below the fluid's, which is what the calculator's mass and volume give.
''',
     faq_add=[('Does buoyant force increase with depth?',
               'Not for a rigid object in water, because water is nearly incompressible and the displaced volume stays the same. Compressible things such as a diver\'s wetsuit, lungs or an air-filled bag shrink with depth, so their buoyancy falls as they go deeper.'),
              ('How much weight can a floating object carry?',
               f'The extra load is the mass of fluid it would displace fully submerged minus its own mass. The default 10 L, 8 kg object displaces 10 kg of fresh water, so it can carry about {spare:.0f} kg before it sinks.')])

# ---------------------------------------------------------------- CGPA to percentage
gd = 8.2
conv = {
    'CBSE': lambda c: 9.5 * c,
    'AICTE': lambda c: (c - 0.75) * 10,
    'Mumbai University': lambda c: 7.1 * c + 11,
    'Simple': lambda c: 10 * c,
}
d_res = {k: f(gd) for k, f in conv.items()}
# SGPA to CGPA
sems = [(7.8, 22), (8.4, 24), (8.1, 20), (8.9, 24)]
cg = sum(s * c for s, c in sems) / sum(c for _, c in sems)
cg_simple = sum(s for s, _ in sems) / len(sems)
cg_pct = (round(cg, 2) - 0.75) * 10
r_rows = ''
for pct in (55, 60, 65, 70, 75, 80, 85, 90):
    r_rows += f"| {pct}% | {pct/9.5:.2f} | {pct/10+0.75:.2f} | {(pct-11)/7.1:.2f} | {pct/10:.2f} |\n"
need60 = 60 / 10 + 0.75

edit_keep_featured('everyday-life/cgpa-to-percentage', date=U, phrase='cgpa to percentage calculator',
     intro=("CBSE and many Indian universities report results as a CGPA on a 10-point scale, while forms for jobs, admissions and scholarships often ask for a percentage. "
            "This CGPA to percentage calculator applies the CBSE, AICTE, Mumbai University or simple formula, and works backwards from a percentage too.\n\n"
            "Students and graduates use it when filling placement and higher-study forms, and recruiters use it to compare candidates graded on different scales."),
     body_add=f'''
## Worked example: CGPA {gd} with each formula

The default CGPA of {gd} gives a different answer under each rule, which is why the formula matters more than the number:

| Formula | Calculation | Percentage |
|---|---|---|
| CBSE | {gd} × 9.5 | **{d_res['CBSE']:.1f}%** |
| AICTE | ({gd} − 0.75) × 10 | **{d_res['AICTE']:.1f}%** |
| Mumbai University | 7.1 × {gd} + 11 | **{d_res['Mumbai University']:.2f}%** |
| Simple | {gd} × 10 | **{d_res['Simple']:.0f}%** |

The spread between the lowest and highest result is {d_res['Simple']-d_res['Mumbai University']:.1f} percentage points, enough to cross a 75% or 80% eligibility line.

## From SGPA to CGPA to percentage

An engineering student has four semesters: SGPA 7.8 (22 credits), 8.4 (24), 8.1 (20) and 8.9 (24). The credit-weighted CGPA is (7.8 × 22 + 8.4 × 24 + 8.1 × 20 + 8.9 × 24) ÷ 90 = **{cg:.2f}**. A plain average of the four SGPAs gives {cg_simple:.2f}, slightly off because the semesters carry different credits. Under the AICTE rule, {cg:.2f} becomes ({cg:.2f} − 0.75) × 10 = **{cg_pct:.1f}%**.

## Percentage back to CGPA

| Percentage | CBSE | AICTE | Mumbai | Simple |
|---|---|---|---|---|
{r_rows}
A common placement cut-off of 60% therefore means a CGPA of at least {need60:.2f} where the AICTE formula is used, but only {60/9.5:.2f} under the CBSE rule.

## When you are asked for a percentage

Check the bottom of your marksheet or the university's grading notice first: many universities print their own conversion and will issue a conversion certificate on request. CBSE returned to marks for Class 10 board results from 2018, so the 9.5 rule applies to older CCE marksheets. When a form asks for a percentage and your institution has no published rule, state the CGPA as well and name the formula you used, so nobody thinks you inflated the figure.

## Common mistakes

- **Using CBSE's 9.5 for a university CGPA.** It was set for the CBSE CCE scheme only; engineering colleges under AICTE use (CGPA − 0.75) × 10.
- **Averaging SGPAs without credits.** Weight each semester by its credits, as in the example above.
- **Converting a 4-point GPA with a 10-point formula.** Convert to the correct scale first, or use the evaluator's own method for study abroad.
- **Rounding the CGPA before converting.** 8.249 rounded to 8.2 loses almost half a percentage point under the CBSE rule.
- **Quoting a converted figure as official.** Unless your marksheet or a university certificate states it, call it an equivalent percentage.
''',
     faq_add=[('What CGPA is 60 percent?',
               f'Under the AICTE formula 60% is a CGPA of {need60:.2f}; under the CBSE rule it is {60/9.5:.2f}; under the simple rule it is 6.0. Use the rule your institution publishes.'),
              ('How do I calculate CGPA from SGPA?',
               'Multiply each semester SGPA by that semester\'s credits, add the products and divide by the total credits. If every semester has the same credits, the plain average of the SGPAs gives the same answer.')])

# ---------------------------------------------------------------- Concrete mix
Vw, mix = 1.0, 5.5
Vd = Vw * 1.54
bags = Vd / mix * 1440 / 50
sand = Vd / mix * (mix - 1) / 3
agg = Vd / mix * (mix - 1) * 2 / 3
cem_kg = bags * 50
water = cem_kg * 0.5
CFT = 35.3147
bag_L = 50 / 1440 * 1000
# slab example 4 m x 3 m x 125 mm, M20
sl = 4 * 3 * 0.125
s_bags = sl * 1.54 / mix * 1440 / 50
s_sand = sl * 1.54 / mix * (mix - 1) / 3
s_agg = sl * 1.54 / mix * (mix - 1) * 2 / 3
w5 = 1.05
c_rows = ''
for lab, mx, wc in (('M10', 10, 0.6), ('M15', 7, 0.55), ('M20', 5.5, 0.5), ('M25', 4, 0.45)):
    vd = 1.54 / mx
    b = vd * 1440 / 50
    sa = vd * (mx - 1) / 3 * CFT
    ag = vd * (mx - 1) * 2 / 3 * CFT
    c_rows += f"| {lab} | {b:.2f} | {sa:.1f} cft | {ag:.1f} cft | {b*50*wc:.0f} L ({wc}) |\n"

edit('construction/concrete-mix', date=U, phrase='concrete mix calculator',
     intro=("A nominal mix ratio such as 1 : 1.5 : 3 tells you the parts of cement, sand and coarse aggregate in each batch. "
            "This concrete mix calculator turns a wet volume into cement bags, sand and aggregate for M10 to M25, using the usual 1.54 dry volume factor.\n\n"
            "Site engineers, contractors and home builders use it to order materials and plan batches for slabs, footings and floors before the trucks are booked."),
     body_add=f'''
## Worked example: the default 1 m³ of M20

- Dry volume = {Vw:g} × 1.54 = **{Vd:.2f} m³**, split into {mix} parts of {Vd/mix:.3f} m³
- Cement = {Vd/mix:.3f} m³ × 1,440 kg/m³ = {cem_kg:.0f} kg = **{bags:.2f} bags**
- Sand = {Vd/mix:.3f} × 1.5 = **{sand:.2f} m³** ({sand*CFT:.1f} cft)
- Aggregate = {Vd/mix:.3f} × 3 = **{agg:.2f} m³** ({agg*CFT:.1f} cft)
- Water at a water-cement ratio of 0.5 = {cem_kg:.0f} × 0.5 = about **{water:.0f} litres**

## Slab example

A 4 m × 3 m roof slab 125 mm thick holds {sl:.2f} m³ of concrete. In M20 it needs {s_bags:.2f} bags of cement, {s_sand:.3f} m³ of sand and {s_agg:.3f} m³ of 20 mm aggregate. With 5% for spillage and uneven formwork, order **{math.ceil(s_bags*w5)} bags**, {s_sand*w5:.2f} m³ ({s_sand*w5*CFT:.1f} cft) of sand and {s_agg*w5:.2f} m³ ({s_agg*w5*CFT:.1f} cft) of aggregate.

## Materials per cubic metre in cubic feet

Sand and aggregate are often sold by the cubic foot (cft) or by the tractor or truck load, so here are the same quantities in cft, with the water for a typical water-cement ratio for each grade:

| Grade | Cement bags | Sand | Aggregate | Water (w/c) |
|---|---|---|---|---|
{c_rows}
## Batching on site with a measuring box

One 50 kg bag of cement has a loose volume of about 50 ÷ 1,440 = {bag_L:.1f} litres, so sites use a wooden box of about 35 litres (for example 300 × 300 × 390 mm) to measure sand and aggregate. For M20 that means 1 bag, 1.5 boxes of sand and 3 boxes of aggregate per batch. Measuring by headpans or shovels instead varies by 20% or more and is the main reason site concrete misses its grade.

If the sand is damp it bulks by 20% to 30%, so a box of wet sand holds less actual sand; add roughly a quarter more or check the bulking with a measuring jar test.

## Common mistakes

- **Skipping the dry volume factor.** Ordering 1 m³ of materials for 1 m³ of concrete leaves you about a third short.
- **Adding water for workability.** Each extra 5 litres per bag lowers strength noticeably; use a plasticiser instead.
- **Ignoring bulking of sand.** Wet sand measured by volume gives a lean, harsh mix.
- **Using nominal mixes above M25.** IS 456 expects design mixes for higher grades, proportioned from trial batches.
- **Ordering exact quantities.** Allow 3% to 5% wastage and keep a spare bag for the last batch.
''',
     faq_add=[('How many cubic feet of sand and aggregate are needed for 1 m³ of M20?',
               f'About {sand*CFT:.1f} cft of sand and {agg*CFT:.1f} cft of coarse aggregate, with {bags:.1f} bags of cement, using the 1.54 dry volume factor.'),
              ('How much concrete does one bag of cement make in M20?',
               f'One bag makes about {1/bags:.3f} m³ ({CFT/bags:.1f} cft) of finished M20 concrete, mixed with 1.5 boxes of sand and 3 boxes of aggregate measured in a 35 L box.')])

# ---------------------------------------------------------------- Coffee ratio
w, r = 500.0, 16
c = w / r
absorb = 2.0
bev = w - absorb * c
tds = 0.0135
ey = tds * bev / c * 100
k_rows = ''
for name, rr in (('Espresso style concentrate', 2), ('Cold brew concentrate', 8), ('AeroPress', 12), ('French press', 15), ('Pour-over', 16), ('Drip machine', 17)):
    k_rows += f"| {name} | 1 : {rr} | {250/rr:.1f} g | {500/rr:.1f} g | {1000/rr:.1f} g |\n"
cb_w, cb_r = 1000.0, 8
cb_c = cb_w / cb_r
cb_yield = cb_w - 2.5 * cb_c

edit('food/coffee-ratio', date=U, phrase='coffee ratio calculator',
     intro=("The brew ratio is the weight of ground coffee compared with the weight of water, and it largely sets how strong the cup tastes. "
            "This coffee ratio calculator gives the grams of coffee for any amount of water, or the water for the coffee you have, at ratios from 1:2 to 1:17.\n\n"
            "Home brewers use it to repeat a cup they liked, and cafes use it to scale a recipe from one mug to a full batch brewer."),
     body_add=f'''
## Worked example with the defaults

At the default pour-over ratio of 1:16, {w:g} mL of water needs {w:g} ÷ {r} = **{c:.2f} g** of coffee, which most people round to 31 g. The grounds hold back about {absorb:g} g of water per gram, so the cup ends up at roughly {w:g} − {absorb:g} × {c:.2f} = **{bev:.0f} mL** of coffee. If a refractometer reads {tds*100:.2f}% total dissolved solids, the extraction yield is {tds:.4f} × {bev:.0f} ÷ {c:.2f} = **{ey:.1f}%**, inside the 18% to 22% range the Specialty Coffee Association treats as balanced.

## Dose for common batch sizes

| Method | Ratio | 250 mL | 500 mL | 1 L |
|---|---|---|---|---|
{k_rows}
For espresso the 1:2 ratio describes coffee in to drink out, for example 18 g of coffee giving 36 g of espresso, not 1:2 with water poured in.

## Cold brew and dilution

Cold brew is made strong and diluted later. {cb_w:,.0f} mL of water at 1:{cb_r} takes {cb_c:.0f} g of coarse coffee; after steeping 12 to 18 hours the grounds keep about 2.5 g of water per gram, leaving roughly {cb_yield:.0f} mL of concentrate. Mixing it 1:1 with water or milk brings the cup back to about a 1:16 strength.

## Getting the ratio right in practice

Weigh both coffee and water on a kitchen scale reading to 0.1 g and tare between steps. Grind just before brewing, because ground coffee loses aroma within minutes. Change one thing at a time: keep the ratio fixed while you adjust grind, and only then move the ratio a step, say from 1:16 to 1:15, if the cup is still thin.

## Common mistakes

- **Scooping instead of weighing.** A level tablespoon of a light, coarse grind can weigh 30% less than one of a dark, fine grind.
- **Counting the water that boils off or stays in the kettle.** Weigh the water that actually goes onto the coffee.
- **Fixing sourness with more coffee.** Sour usually means under-extraction; grind finer or brew longer before changing the ratio.
- **Reading the ratio by cup volume.** Machines rate a cup at 125 to 150 mL, so a 10 cup carafe is not 10 mugs.
- **Applying a pour-over ratio to cold brew concentrate.** Brewing at 1:16 cold gives a weak, flat result.
''',
     faq_add=[('Why does my coffee yield less than the water I poured?',
               f'Ground coffee soaks up about twice its weight in water. With {c:.2f} g of coffee and {w:g} mL of water, about {absorb*c:.0f} mL stays in the bed, so you get roughly {bev:.0f} mL in the cup.')])

# ---------------------------------------------------------------- Protein intake
mb, f = 70.0, 1.6
p = mb * f
pm = p / 4
lb = 2.20462
# 85 kg person losing fat, 2.0 g/kg; 30% of 2000 kcal from protein
p2 = 85 * 2.0
kcal = 2000
p_pct = 112 * 4 / kcal * 100
# leucine threshold-ish meal guide: 0.4 g/kg per meal
pmeal = 0.4 * mb
fd = [('Chicken breast, cooked', 31, 165), ('Paneer', 18, 265), ('Firm tofu', 14, 145), ('Eggs (2 large, 100 g)', 13, 155),
      ('Cooked lentils', 9, 116), ('Greek yogurt, plain', 10, 59), ('Milk, toned', 3.3, 58), ('Peanuts', 26, 567)]
f_rows = ''
for name, pr, kc in fd:
    f_rows += f"| {name} | {pr:g} g | {pr/kc*100:.1f} g | {p/pr*100:,.0f} g |\n"

edit('health/protein-intake', date=U, phrase='protein intake calculator',
     intro=("Daily protein needs scale with body weight and rise with training, ageing and dieting. "
            "This protein intake calculator multiplies your weight by a grams-per-kilogram factor for your activity or goal and splits the total across four meals.\n\n"
            "Gym goers, endurance athletes, older adults and people planning vegetarian meals use it to set a realistic daily target and check whether their usual meals reach it."),
     body_add=f'''
## Reading the default result

The defaults are a {mb:g} kg adult ({mb*lb:.0f} lb) who lifts weights, so the factor is 1.6 g/kg: {mb:g} × 1.6 = **{p:.0f} g a day**, or **{pm:.0f} g** in each of four meals. On a {kcal:,} kcal diet those {p:.0f} g supply {p*4:.0f} kcal, about {p_pct:.0f}% of energy, well inside the 10% to 35% range the US Dietary Reference Intakes give for adults.

## Food needed to reach the default target

How much of a single food would supply the whole {p:.0f} g shows why most people mix sources:

| Food (per 100 g) | Protein | Protein per 100 kcal | Amount for {p:.0f} g |
|---|---|---|---|
{f_rows}
Lean animal foods and tofu give the most protein per calorie; nuts and paneer bring a lot of fat with it, which matters on a calorie-limited diet.

## Spreading protein over the day

Research on muscle protein synthesis suggests roughly 0.4 g/kg per meal, about {pmeal:.0f} g for a {mb:g} kg person, eaten three to four times a day. A typical Indian vegetarian day of tea with milk, two rotis with dal, rice with sambar and a small curd bowl often lands near 45 g to 55 g, so adding paneer, soy chunks, extra curd or a second dal is the usual way to close the gap.

## Choosing the right factor

Use your current weight unless you carry a lot of body fat; in that case many dietitians base the target on a goal or lean body weight, otherwise the number comes out very high. An 85 kg person cutting fat at 2.0 g/kg would get {p2:.0f} g, which is hard to eat and rarely necessary. The lean body mass calculator helps estimate that alternative base weight.

## Common mistakes

- **Counting the weight of the food as protein.** 100 g of chicken holds about 31 g of protein, not 100 g.
- **Using raw and cooked values interchangeably.** Cooking drives off water, so 100 g of cooked lentils has far less protein than 100 g dry.
- **Eating most of it at dinner.** A 10 g breakfast and a 70 g dinner reaches the total but spreads it poorly.
- **Picking the highest factor by default.** 1.6 g/kg covers most people who train; more mainly helps during a calorie deficit.
- **Ignoring medical advice.** People with kidney disease, and pregnant or breastfeeding women, should set their target with a doctor or dietitian.
''',
     faq_add=[('How much protein is in a typical vegetarian Indian diet?',
               'A day of dal, rice, roti, vegetables and some milk or curd often provides about 45 g to 55 g. That meets 0.8 g/kg for a 60 kg adult, but active people usually need extra paneer, soy, curd, legumes or eggs.'),
              ('Should I use my current weight or goal weight?',
               'Use current weight if you are near a healthy weight. If you carry a lot of body fat, a target based on goal or lean body weight gives a more realistic number.')])

print('done')

# ======================================================================= SECTION _expand_c3.py
"""Expand (2026-11-20), slice 3: volume-converter, cagr, age-calculator, car-carbon-footprint, pump-power.
Numbers computed here from each page's default inputs and equations. Run once on the original files."""
import sys, os, math, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-20'


def edit_keep_featured(cid, **kw):
    """The page is already featured. Lift the flag around the edit and restore it unchanged."""
    path = os.path.join(inplace.BASE, cid + '.mdx')
    s = open(path).read()
    line = 'featured: true\n'
    assert s.count(line) == 1, cid
    open(path, 'w').write(s.replace(line, '', 1))
    try:
        n = edit(cid, **kw)
    except Exception:
        open(path, 'w').write(s)
        raise
    t = open(path).read()
    k = t.index('\nupdated: ')
    k = t.index('\n', k + 1) + 1
    open(path, 'w').write(t[:k] + line + t[k:])
    return n


# ---------------------------------------------------------------- Volume converter
L = 0.001  # m3 per litre
GUS = 3.785411784e-3
GUK = 4.54609e-3
FT3 = 0.3048 ** 3
IN3 = 0.0254 ** 3
v1 = 1 * L
d_ml, d_m3, d_gus, d_guk, d_ft3, d_in3 = v1 / 1e-6, v1, v1 / GUS, v1 / GUK, v1 / FT3, v1 / IN3
# rectangular tank example
tl, tw, th = 2.0, 1.5, 1.2
tv = tl * tw * th
tank_L, tank_gus, tank_guk, tank_ft3 = tv / L, tv / GUS, tv / GUK, tv / FT3
# fill time with a garden hose at 15 L/min
hose = 15.0
fill_h = tank_L / hose / 60
containers = [
    ('Standard oil barrel (42 US gal)', 42 * GUS),
    ('Steel drum (55 US gal)', 55 * GUS),
    ('IBC tote', 1.0),
    ('Small overhead tank (500 L)', 0.5),
    ('Road tanker (30,000 L)', 30.0),
    ('20 ft shipping container (inside)', 5.898 * 2.352 * 2.393),
    ('Olympic pool (50 × 25 × 2 m)', 50 * 25 * 2.0),
]
c_rows = ''
for name, v in containers:
    c_rows += f"| {name} | {v/L:,.0f} L | {v:,.3f} m³ | {v/GUS:,.1f} | {v/GUK:,.1f} | {v/FT3:,.1f} |\n"
# US fl oz vs UK fl oz
floz_us = GUS / 128 / 1e-6
floz_uk = GUK / 160 / 1e-6

edit_keep_featured('conversion/volume-converter', date=U, phrase='volume converter',
     intro=("Volume is the space a liquid, gas or solid takes up, and it is quoted in litres, millilitres, cubic metres, US and UK gallons, cubic feet and cubic inches. "
            "This volume converter changes a value typed into any one field into all the others at once.\n\n"
            "Plumbers and tank installers use it to rate tanks and pumps, cooks and brewers use it to scale recipes, and engineers use it to move between metric data sheets and imperial drawings."),
     body_add=f'''
## Worked example with the default value

The converter opens with **1 litre**. Because 1 L is exactly 0.001 m³, every other field follows from one division:

- Millilitres: 0.001 ÷ 10⁻⁶ = **{d_ml:,.0f} mL**
- Cubic metres: **{d_m3:g} m³**
- US gallons: 0.001 ÷ 0.003785411784 = **{d_gus:.6f} US gal**
- UK gallons: 0.001 ÷ 0.00454609 = **{d_guk:.6f} UK gal**
- Cubic feet: 0.001 ÷ 0.0283168 = **{d_ft3:.7f} ft³**
- Cubic inches: 0.001 ÷ 0.000016387 = **{d_in3:.4f} in³**

## Sizing a water tank

A rectangular tank measuring {tl:g} m × {tw:g} m × {th:g} m holds {tl:g} × {tw:g} × {th:g} = **{tv:.2f} m³**. Typing 3.6 into the cubic metre field gives **{tank_L:,.0f} L**, **{tank_gus:,.0f} US gallons**, **{tank_guk:,.0f} UK gallons** or **{tank_ft3:,.1f} ft³**. Filled from a garden hose delivering {hose:g} L/min, it takes {tank_L:,.0f} ÷ {hose:g} = {tank_L/hose:,.0f} minutes, about **{fill_h:.1f} hours**. Measure the inside dimensions, not the outside: a 50 mm wall on a plastic tank of this size cuts the usable volume by several percent.

## Common containers in every unit

| Container | Litres | m³ | US gal | UK gal | ft³ |
|---|---|---|---|---|---|
{c_rows}
## Where the definitions come from

The litre is defined as exactly one cubic decimetre. The US gallon is defined as exactly 231 cubic inches, and the inch as exactly 25.4 mm, which fixes the US gallon at 3.785411784 L. The UK gallon is defined directly as exactly 4.54609 L. Fluid ounces also differ: a US fluid ounce is {floz_us:.3f} mL (1/128 US gal), while a UK fluid ounce is {floz_uk:.3f} mL (1/160 UK gal), so the US fluid ounce is the larger of the two even though the UK gallon is bigger.

## Common mistakes

- **Mixing up US and UK gallons.** Product labels in the UK, Canada (older documents) and some Gulf countries may use imperial gallons; US data sheets always mean US gallons. The error is about 20%.
- **Converting cubic metres as if they were linear.** 1 m is 100 cm, but 1 m³ is 1,000,000 cm³. Cube the length factor whenever you convert a volume.
- **Treating litres of any liquid as kilograms.** Only water near 4 °C is close to 1 kg/L. Diesel is about 0.83 kg/L and honey about 1.4 kg/L, so convert by mass with the density.
- **Using nominal tank capacity.** Tanks are sold by brim or nominal volume; the working volume below the overflow is often 5% to 10% less.
- **Confusing gas volumes at different conditions.** A cubic metre of gas at 10 bar holds ten times the gas of a cubic metre at 1 bar. Normal or standard cubic metres need the pressure and temperature stated.
''',
     faq_add=[('How many cubic feet are in 1,000 litres?',
               f'1,000 litres is 1 m³, which is {1/FT3:.2f} ft³. That is also {1/GUS:.1f} US gallons or {1/GUK:.1f} UK gallons.'),
              ('Why is a US fluid ounce bigger than a UK fluid ounce?',
               f'They are defined from different gallons and different fractions. A US fluid ounce is 1/128 of a US gallon, {floz_us:.2f} mL; a UK fluid ounce is 1/160 of a UK gallon, {floz_uk:.2f} mL.')])

# ---------------------------------------------------------------- CAGR
s0, ev0, t0 = 10000.0, 18000.0, 5.0
g0 = (ev0 / s0) ** (1 / t0) - 1
path_rows = ''
val = s0
for yr in range(0, 6):
    v = s0 * (1 + g0) ** yr
    gain = v - s0
    path_rows += f"| {yr} | {v:,.2f} | {gain:,.2f} |\n"
# years to double at the default CAGR: exact vs rule of 72
dbl = math.log(2) / math.log(1 + g0)
r72 = 72 / (g0 * 100)
# revenue example: 4 yearly values
rev = [120.0, 150.0, 138.0, 171.0, 210.0]
g_rev = (rev[-1] / rev[0]) ** (1 / 4) - 1
yoy = [(rev[i + 1] / rev[i] - 1) for i in range(4)]
avg_yoy = sum(yoy) / 4
# target: how long to reach 50,000 from 10,000 at 12%
t_target = math.log(5) / math.log(1.12)
# months case
g_18m = (11500 / 10000) ** (1 / 1.5) - 1
# rate table: years to grow 1 -> 2, 3, 5 at different CAGRs
rt_rows = ''
for r in (0.04, 0.06, 0.08, 0.10, 0.12, 0.15, 0.20):
    rt_rows += f"| {r*100:.0f}% | {math.log(2)/math.log(1+r):.1f} | {math.log(3)/math.log(1+r):.1f} | {math.log(5)/math.log(1+r):.1f} |\n"

edit('finance/cagr', date=U, phrase='cagr calculator',
     intro=("CAGR, the compound annual growth rate, is the single steady yearly rate that would take a value from its starting figure to its ending figure. "
            "This CAGR calculator finds that rate, or projects a future value or the years needed when you know the rate.\n\n"
            "Investors use it to compare funds and shares held for different periods, and business owners and analysts use it to report revenue, profit or user growth over several years."),
     replace=[('- **Ignoring dividends.** For stocks, include reinvested dividends in the ending value to get total-return CAGR.\n',
               '- **Ignoring dividends.** For stocks, include reinvested dividends in the ending value to get total-return CAGR.\n'
               '- **Counting the wrong number of years.** Five yearly figures from 2021 to 2025 span 4 years of growth, not 5.\n'
               '- **Computing CAGR across a sign change.** If the start is zero or the values go from a loss to a profit, CAGR has no meaning; report the absolute change instead.\n')],
     body_add=f'''
## Year-by-year path of the default example

At the default CAGR of {g0*100:.2f}%, the 10,000 grows like this. The final year lands exactly on 18,000, which is the definition of CAGR:

| Year | Value | Gain so far |
|---|---|---|
{path_rows}
The real investment almost certainly took a bumpier route; CAGR only fixes the two ends. At this rate money doubles in ln 2 ÷ ln({1+g0:.4f}) = **{dbl:.2f} years**, close to the rule of 72 estimate of 72 ÷ {g0*100:.2f} = {r72:.2f} years.

## Business example: revenue over four years

A company reports revenue of 120, 150, 138, 171 and 210 (in lakh or millions) for five consecutive years. That is 4 years of growth, so CAGR = (210 ÷ 120)<sup>1/4</sup> − 1 = **{g_rev*100:.2f}%**. The four year-on-year changes are {', '.join(f'{x*100:+.1f}%' for x in yoy)}, whose simple average is {avg_yoy*100:.2f}%, higher than the CAGR because the dip and recovery inflate the average.

## Years to multiply your money

Set the CAGR and leave the period blank to find how long a target takes. The table shows years needed to double, triple and five-fold a value:

| CAGR | 2× | 3× | 5× |
|---|---|---|---|
{rt_rows}
For example, growing 10,000 to 50,000 at 12% takes ln 5 ÷ ln 1.12 = **{t_target:.1f} years**.

## Periods shorter than a year

CAGR annualises, so a short period is scaled up. A gain from 10,000 to 11,500 in 18 months is a 15% total return but a CAGR of {g_18m*100:.2f}%. Fund factsheets in India show absolute returns for periods under one year for exactly this reason: annualising a few weeks of movement gives misleading figures.
''',
     faq_add=[('How many years should I use for CAGR from yearly figures?',
               'Count the gaps, not the values. Figures for 2021, 2022, 2023, 2024 and 2025 cover 4 years of growth, so use t = 4.'),
              ('How long does money take to double at a given CAGR?',
               f'Divide ln 2 by ln(1 + CAGR). At {g0*100:.2f}% it takes {dbl:.2f} years; the rule of 72 gives a quick estimate of 72 divided by the rate in percent.')])

# ---------------------------------------------------------------- Age calculator
DOB_DAYS = 12784
D = datetime.date


def ymd(b, o):
    y = o.year - b.year - ((o.month, o.day) < (b.month, b.day))
    m = (o.year - b.year) * 12 + o.month - b.month - (o.day < b.day)
    return y, m


b = D(1990, 3, 15)
on = D(2026, 11, 20)
ey, em = ymd(b, on)
edays = (on - b).days
eweeks = edays / 7
erem_m = em - ey * 12
# day remainder: from the last monthly anniversary
last = D(b.year + em // 12 + (b.month - 1 + em % 12) // 12, (b.month - 1 + em % 12) % 12 + 1, b.day)
erem_d = (on - last).days
nextbd = D(2027, 3, 15)
to_next = (nextbd - on).days
# leap days in the period
leaps = sum(1 for yy in range(1990, 2027)
            if ((yy % 4 == 0 and yy % 100 != 0) or yy % 400 == 0) and b < D(yy, 2, 29) <= on)
# cut-off table for one child: born 20 Sep 2020
kid = D(2020, 9, 20)
cut_rows = ''
for lab, cd in (('31 March 2026', D(2026, 3, 31)), ('1 April 2026', D(2026, 4, 1)), ('1 June 2026', D(2026, 6, 1)),
                ('30 September 2026', D(2026, 9, 30)), ('31 December 2026', D(2026, 12, 31))):
    yy, mm = ymd(kid, cd)
    cut_rows += f"| {lab} | {yy} years {mm - yy*12} months | {(cd - kid).days:,} |\n"
# inclusive vs exclusive
incl = edays + 1

edit_keep_featured('everyday-life/age-calculator', date=U, phrase='age calculator',
     intro=("Your exact age is the time from your date of birth to a chosen date, counted in completed years, months, weeks and days. "
            "This age calculator gives all four, for today or for any past or future date you pick.\n\n"
            "Parents use it to check school admission cut-offs, job and exam applicants use it to confirm age limits on a notified date, and anyone can use it to find milestones or anniversaries."),
     body_add=f'''
## What the defaults show

When the page opens, the date of birth is set {DOB_DAYS:,} days before today and the second date is today, so the days field always reads **{DOB_DAYS:,} days** and the weeks field **{DOB_DAYS/7:,.1f} weeks**. That is about 35 years; the completed years and months depend on how many 29 Februarys fall inside the window, so they can shift by one around the boundary.

## Worked example on fixed dates

Take a birth date of **15 March 1990** and an "age on" date of **20 November 2026**. These dates are fixed so the example does not change with today's date:

- Completed years: the 2026 birthday (15 March) has passed, so **{ey} years**
- Completed months: {ey} × 12 + {erem_m} = **{em} months**, the last monthly anniversary being {last.day} {last.strftime('%B %Y')}
- Days since that anniversary: **{erem_d} days**, so the age reads {ey} years, {erem_m} months and {erem_d} days
- Total days: **{edays:,}**, which is {eweeks:,.1f} weeks; {leaps} leap days fall in the period
- Days to the next birthday on 15 March 2027: **{to_next}**

## Age on admission and recruitment cut-off dates

The same child, born on 20 September 2020, can fall either side of an age rule depending on the cut-off the school or board uses:

| Cut-off date | Age on that date | Days since birth |
|---|---|---|
{cut_rows}
A rule of "6 years on 31 March 2026" excludes this child, while a 31 December cut-off includes them. Always read the age limit together with its date.

## How the counting works in practice

Completed years and months are counted the way people and most laws count them: a year is complete when the birthday is reached, and a month is complete when the same day number comes round. When the birth day number does not exist in a shorter month, such as the 31st in April, this calculator completes that month on the 1st of the following month, the same rule it uses for 29 February birthdays. The day total is the plain calendar difference and does not include the birth day itself; counting both end dates, as some leave and contract rules do, adds one, giving {incl:,} days in the example above.

## Common mistakes

- **Subtracting birth year from current year.** On 14 March 2026, 2026 − 1990 gives 36, but someone born on 15 March 1990 is still 35 until the next day; the month and day must be compared too.
- **Using 365 days a year.** {edays:,} ÷ 365 gives {edays/365:.2f}, which overstates age slightly because of the {leaps} leap days; use calendar dates, not division.
- **Checking age on the application date.** Exam and job notices fix age on a stated date, often 1 January or 1 August; entering today can put you on the wrong side of the limit.
- **Mixing day and month order.** 04/05/2010 is 4 May in India and the UK but 5 April in the US. Pick the date from the calendar rather than typing it.
- **Forgetting time zones for very recent births.** A baby born late at night in one country may have a different birth date abroad; use the date on the birth certificate.
''',
     faq_add=[('Does the age in days include the birth day?',
               f'No. It is the number of days between the two dates. Born 15 March 1990, on 20 November 2026 you are {edays:,} days old; counting both the first and last day gives {incl:,}.'),
              ('How do I check my age for a job or exam age limit?',
               'Set the "Age on this date" field to the date stated in the notification, such as 1 August of the exam year, and read the completed years and months. Relaxations for categories are added to the limit, not to your age.')])

# ---------------------------------------------------------------- Car carbon footprint
d0, c0, ef0 = 12000.0, 7.0, 2.31
fuel0 = d0 * c0 / 100
co20 = fuel0 * ef0 / 1000
gkm0 = c0 * ef0 * 10
# where 2.31 comes from: density 0.745 kg/L, carbon fraction 0.86 -> roughly
dens_p, cf_p = 0.745, 0.86
ef_calc = dens_p * cf_p * 44.01 / 12.011
dens_d, cf_d = 0.835, 0.865
ef_calc_d = dens_d * cf_d * 44.01 / 12.011
# fuel comparison at same distance with typical consumptions
cmp_rows = ''
for name, c, ef in (('Petrol hatchback', 6.0, 2.31), ('Petrol SUV', 9.0, 2.31), ('Diesel sedan', 5.0, 2.68),
                    ('Diesel SUV', 7.5, 2.68), ('LPG car', 8.5, 1.51)):
    cmp_rows += f"| {name} | {c:g} L/100 km | {c*ef*10:.0f} g/km | {d0*c/100*ef/1000:.2f} t |\n"
# brim-to-brim: drove 642 km, refilled 41.3 L
bk, bl = 642.0, 41.3
bc = bl / bk * 100
# mpg conversions
def mpg_us(lp100):
    return 235.215 / lp100
def mpg_uk(lp100):
    return 282.481 / lp100
# lifetime: 15 years
life = co20 * 15
# well-to-wheel uplift 20%
wtw = co20 * 1.20

edit_keep_featured('ecology/car-carbon-footprint', date=U, phrase='car carbon footprint calculator',
     intro=("Every litre of fuel a car burns turns its carbon into carbon dioxide, so tailpipe CO₂ follows directly from distance and fuel economy. "
            "This car carbon footprint calculator gives fuel used, tonnes of CO₂ a year and grams per kilometre for petrol, diesel and LPG.\n\n"
            "Drivers use it to see what a new car or a longer commute adds, and companies use it to report fleet emissions and set reduction targets."),
     body_add=f'''
## Worked example with the default values

The defaults are a petrol car using {c0:g} L/100 km over {d0:,.0f} km a year:

- Fuel used = {d0:,.0f} × {c0:g} ÷ 100 = **{fuel0:,.0f} L**
- CO₂ = {fuel0:,.0f} × {ef0} = {fuel0*ef0:,.1f} kg = **{co20:.2f} t**
- CO₂ per km = {c0:g} × {ef0} × 10 = **{gkm0:.0f} g/km**

Over a 15-year life at the same use, that car emits about {life:.0f} tonnes from the tailpipe. Adding roughly 20% for producing and delivering the fuel raises one year to about {wtw:.2f} t.

## Where the emission factor comes from

The factor is set by chemistry. Petrol has a density of about {dens_p} kg/L and is about {cf_p*100:.0f}% carbon by mass; each kilogram of carbon becomes 44.01 ÷ 12.011 = 3.664 kg of CO₂. So one litre gives {dens_p} × {cf_p} × 3.664 = **{ef_calc:.2f} kg**, close to the 2.31 used here (blends with ethanol come in a little lower). Diesel is denser, {dens_d} kg/L at about {cf_d*100:.1f}% carbon, giving {ef_calc_d:.2f} kg/L. That is why a diesel can burn less fuel yet emit a similar mass of CO₂.

## Same distance, different cars

{d0:,.0f} km a year with typical real-world consumption:

| Car | Consumption | CO₂ per km | CO₂ per year |
|---|---|---|---|
{cmp_rows}
## Measuring your own fuel consumption

Dashboard figures are often 5% to 10% optimistic, and official WLTP or ARAI ratings are measured on a test cycle without traffic, air conditioning or roof loads. The brim-to-brim method gives a real number: fill the tank until the pump clicks off, reset the trip meter, drive normally, then fill again at the same pump. If you drove {bk:g} km and the second fill took {bl} L, consumption is {bl} ÷ {bk:g} × 100 = **{bc:.2f} L/100 km**. Repeat over two or three tanks and average them.

If your figures are in miles per gallon, convert first: L/100 km = 235.2 ÷ US mpg, or 282.5 ÷ UK mpg. The default {c0:g} L/100 km is {mpg_us(c0):.1f} US mpg or {mpg_uk(c0):.1f} UK mpg.

## Common mistakes

- **Entering km per litre as L/100 km.** Indian buyers often think in km/L. 15 km/L is 100 ÷ 15 = 6.67 L/100 km, not 15.
- **Using the official rating instead of real use.** Short trips, idling in traffic and air conditioning can push real consumption 20% to 40% above the brochure figure.
- **Mixing US and UK mpg.** A UK mpg figure is about 20% higher than the US figure for the same car, because the imperial gallon is larger.
- **Counting CNG or electricity as zero.** CNG is not in the list above but still emits about 2.7 kg CO₂ per kg of gas, and an EV's footprint depends on the grid that charges it.
- **Comparing tailpipe figures with life-cycle figures.** Published life-cycle numbers include fuel production and car manufacture, so they are always higher than this tank-to-wheel result.
''',
     faq_add=[('Why does diesel emit more CO₂ per litre than petrol?',
               f'Diesel is denser and contains more carbon in each litre, about {dens_d*cf_d:.2f} kg against {dens_p*cf_p:.2f} kg for petrol. A diesel car usually burns fewer litres per km, so its CO₂ per km can still be lower.'),
              ('How do I convert km per litre to L/100 km?',
               'Divide 100 by the km per litre figure. A car doing 18 km/L uses 100 ÷ 18 = 5.56 L/100 km, which is the value to enter.')])

# ---------------------------------------------------------------- Pump power
G = 9.80665
Q0, H0, rho0, eta0 = 50 / 3600, 30.0, 998.0, 0.70
Ph0 = rho0 * G * Q0 * H0
Ps0 = Ph0 / eta0
# electrical input with 90% motor, cost at 8 per kWh for 6000 h
etam = 0.90
Pe0 = Ps0 / etam
hours, tariff = 6000, 8.0
energy = Pe0 / 1000 * hours
cost = energy * tariff
# field test: suction -0.3 bar g, discharge 2.6 bar g, gauge height difference 0.5 m, flow 45 m3/h, motor input 5.9 kW
ps, pd, dz, Qf, Pin = -0.3e5, 2.6e5, 0.5, 45 / 3600, 5900.0
Hf = (pd - ps) / (rho0 * G) + dz
Phf = rho0 * G * Qf * Hf
wtw = Phf / Pin
# power table, water at 998, eta 70%
heads = (10, 20, 30, 50, 80)
flows = (5, 10, 25, 50, 100, 200)
p_rows = ''
for q in flows:
    p_rows += f"| {q} m³/h | " + ' | '.join(f"{rho0*G*q/3600*h/0.70/1000:.2f}" for h in heads) + ' |\n'
# brine density change at same flow/head
rho_b = 1200.0
Ps_b = rho_b * G * Q0 * H0 / eta0
# pressure to head
bar_head = 1e5 / (rho0 * G)

edit('engineering/pump-power', date=U, phrase='pump power calculator',
     intro=("Pump power is the energy per second a pump adds to a liquid, set by flow, total head, density and efficiency. "
            "This pump power calculator gives the hydraulic power and the shaft power the motor must supply, or the flow and head a given motor can deliver.\n\n"
            "Process, HVAC and water engineers use it to size motors and estimate running costs; the pump type also matters, as compared in [centrifugal vs positive displacement pumps](https://www.instrumentationblog.in/centrifugal-vs-positive-displacement-pump/)."),
     body_add=f'''
## Default result in detail

With the defaults (50 m³/h, 30 m, 998 kg/m³, 70%), the calculator works in SI units: Q = 50 ÷ 3,600 = {Q0:.5f} m³/s, and with g = 9.80665 m/s²:

- P<sub>h</sub> = 998 × 9.80665 × {Q0:.5f} × 30 = **{Ph0/1000:.3f} kW**
- P<sub>shaft</sub> = {Ph0/1000:.3f} ÷ 0.70 = **{Ps0/1000:.3f} kW** ({Ps0/745.7:.2f} hp)

With a {etam*100:.0f}% efficient motor the electrical input is {Pe0/1000:.2f} kW. Running {hours:,} hours a year at {tariff:g} per kWh, the pump uses {energy:,.0f} kWh and costs about **{cost:,.0f}** a year to run. If the same pump handles brine at {rho_b:,.0f} kg/m³ at the same flow and head, shaft power rises in proportion to density, to {Ps_b/1000:.2f} kW, so check the motor for the densest fluid it will see.

## Shaft power table for water

Shaft power in kW for water (998 kg/m³) at 70% pump efficiency:

| Flow | 10 m | 20 m | 30 m | 50 m | 80 m |
|---|---|---|---|---|---|
{p_rows}
## Checking a pump in the field

On site you rarely know the head directly; you measure it. Fit gauges on the suction and discharge flanges, read the flow from a flowmeter, and log the motor input with a power analyser. In a test with suction at −0.3 bar g, discharge at 2.6 bar g, the discharge gauge {dz} m above the suction gauge and 45 m³/h of water:

- Head = (2.6 − (−0.3)) × 10⁵ ÷ (998 × 9.80665) + {dz} = **{Hf:.2f} m**
- Hydraulic power = 998 × 9.80665 × {Qf:.4f} × {Hf:.2f} = **{Phf/1000:.2f} kW**
- With {Pin/1000:.1f} kW measured at the motor terminals, wire-to-water efficiency is **{wtw*100:.1f}%**

Compare this with the curve value at the measured flow. A drop of more than 5 to 10 points usually means impeller wear, internal recirculation or a worn wear ring. One bar of pressure on water is {bar_head:.2f} m of head, a useful figure when reading gauges.

## Common mistakes

- **Using pressure instead of head for a dense liquid.** Head in metres of liquid is what the pump curve shows; convert pressure with the actual density, not the water figure.
- **Leaving flow in m³/h.** The formula needs m³/s; forgetting to divide by 3,600 makes the power 3,600 times too large.
- **Sizing on the duty point only.** A centrifugal pump running further out on its curve at low system head draws more power than at duty; check the end-of-curve power.
- **Taking motor nameplate kW as power drawn.** The nameplate is the shaft output rating; a lightly loaded motor draws much less, and efficiency falls at low load.
- **Forgetting viscosity.** Oils above about 20 cSt reduce centrifugal pump head and efficiency; use the corrected efficiency, not the water curve.
''',
     faq_add=[('How do I measure the actual head of a running pump?',
               f'Read the discharge and suction pressures, subtract, convert to metres of liquid with the density (1 bar is {bar_head:.2f} m of water) and add the height difference between the gauges.'),
              ('Does pump power change with liquid density?',
               f'Yes, at the same flow and head it rises in proportion. The default duty needs {Ps0/1000:.2f} kW for water and {Ps_b/1000:.2f} kW for brine at 1,200 kg/m³.')])

print('done', inplace.DONE)

# ======================================================================= SECTION _expand_c4.py
"""Expand (2026-11-20), slice 4: control-valve-kv-cv, acres-to-hectares, power-converter, slope,
dna-concentration. Numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
U = '2026-11-20'


def edit_keep_featured(cid, **kw):
    """The page is already featured. Lift the flag around the edit and restore it unchanged."""
    path = os.path.join(inplace.BASE, cid + '.mdx')
    s = open(path).read()
    line = 'featured: true\n'
    assert s.count(line) == 1, cid
    open(path, 'w').write(s.replace(line, '', 1))
    try:
        n = edit(cid, **kw)
    except Exception:
        open(path, 'w').write(s)
        raise
    t = open(path).read()
    k = t.index('\nupdated: ')
    k = t.index('\n', k + 1) + 1
    open(path, 'w').write(t[:k] + line + t[k:])
    return n


# ---------------------------------------------------------------- Control valve Kv / Cv
GPM = 3.785411784e-3 / 60      # m3/s per US gpm
PSI = 6894.757293168           # Pa per psi
KV2CV = 1.156
Q0, dP0, SG0 = 10.0, 1.0, 1.0
Kv0 = Q0 / math.sqrt(dP0 / SG0)
Cv0 = KV2CV * Kv0
# cooling water duty, then a 30% glycol duty on the same valve
Qc, dPc = 45.0, 0.8
Kvc = Qc / math.sqrt(dPc)
Cvc = KV2CV * Kvc
Q_gpm = Qc / 3600 / GPM
dP_psi = dPc * 1e5 / PSI
Cv_check = Q_gpm / math.sqrt(dP_psi)
Kvs = 63.0
Qmax = Kvs * math.sqrt(dPc)
lin_open = Kvc / Kvs * 100
SGg = 1.04
Kvg = Qc / math.sqrt(dPc / SGg)
# required Kv table
kv_rows = ''
for Q in (2, 5, 10, 20, 50, 100, 200):
    r = [Q / math.sqrt(d) for d in (0.25, 0.5, 1.0, 2.0)]
    kv_rows += f"| {Q} m³/h | " + ' | '.join(f"{x:.2f}" for x in r) + ' |\n'

edit_keep_featured('engineering/control-valve-kv-cv', date=U, phrase='control valve Kv / Cv calculator',
    intro=("The flow coefficient, Kv in metric units or Cv in US units, tells you how much liquid a valve passes at a given pressure drop. "
           "This control valve Kv / Cv calculator solves for flow, pressure drop or the coefficient, whichever you leave blank. "
           "Read about the [control valve flow coefficient](https://www.instrumentationblog.in/control-valve-flow-coefficient/).\n\n"
           "Instrument and process engineers use it to size a new valve, check whether an installed valve can pass more flow, "
           "and apply the [basic requirements for control valve sizing](https://www.instrumentationblog.in/control-valve-sizing-basic-requirements/) before ordering."),
    body_add=f'''
## Worked example: sizing a cooling water valve

The calculator opens with {Q0:g} m³/h of water (SG {SG0:g}) across a {dP0:g} bar drop, which gives Kv = {Q0:g} × √({dP0:g} ÷ {SG0:g}) = **{Kv0:.2f} m³/h** and Cv = {KV2CV} × {Kv0:g} = **{Cv0:.2f}**.

A more realistic duty: a heat exchanger needs **{Qc:g} m³/h** of cooling water at maximum load, and the pump curve and pipe losses leave **{dPc:g} bar** for the valve.

- Required Kv = {Qc:g} ÷ √{dPc:g} = **{Kvc:.2f} m³/h**, so Cv = **{Cvc:.1f}**
- Check in US units: {Qc:g} m³/h is {Q_gpm:.1f} gpm and {dPc:g} bar is {dP_psi:.2f} psi, so Cv = {Q_gpm:.1f} ÷ √{dP_psi:.2f} = {Cv_check:.1f}, the same answer
- The next valve in the preferred series is **Kvs {Kvs:g}**, which passes {Kvs:g} × √{dPc:g} = {Qmax:.1f} m³/h fully open
- With a linear trim the valve would sit near {lin_open:.0f}% open at maximum load, inside the usual control band

If the loop is later filled with 30% glycol (SG about {SGg}), the same flow needs Kv = {Qc:g} ÷ √({dPc:g} ÷ {SGg}) = {Kvg:.2f}, only {(Kvg/Kvc-1)*100:.0f}% more, so the selected valve still has margin.

## Required Kv for water at different pressure drops

| Flow | ΔP 0.25 bar | ΔP 0.5 bar | ΔP 1 bar | ΔP 2 bar |
|---|---|---|---|---|
{kv_rows}
Halving the allowed pressure drop raises the required Kv by about 41%, because flow varies with the square root of ΔP.

## How Kv is measured

Valve makers find Kv on a flow test rig, following IEC 60534-2-3 or ANSI/ISA-75.02. Water between 5 and 40 °C flows through the valve at set travel positions, with pressure taps 2 pipe diameters upstream and 6 diameters downstream. The measured flow and pressure drop give Kv at each opening, and the value at rated travel is published as Kvs (or rated Cv). The full curve of Kv against travel is the inherent characteristic: linear, equal percentage or quick opening.

## Common mistakes

- **Using the whole system pressure drop.** Only the drop across the valve body belongs in the formula; pipe, exchanger and strainer losses are separate.
- **Picking the valve size from the line size.** A valve sized by Kv is often one or two sizes smaller than the pipe, with reducers either side.
- **Treating the calculated Kv as the Kvs to order.** The calculated figure is what the duty needs; the catalogue Kvs must be larger so the valve still controls.
- **Leaving SG at 1 for brine, glycol or oil.** Denser liquids need a larger Kv for the same flow and pressure drop.
- **Mixing m³/h with litres per minute.** Kv is defined in m³/h; 100 L/min is 6 m³/h, not 100.
''',
    faq_add=[('What is the difference between Kv and Kvs?',
              'Kv is the flow coefficient at any valve opening, while Kvs is the value at full rated travel published in the catalogue. You calculate the Kv your duty needs, then choose a valve whose Kvs is larger.'),
             ('Can I size a glycol or brine valve with this calculator?',
              f'Yes, as long as the liquid does not flash or cavitate. Enter its specific gravity: {Qc:g} m³/h at {dPc:g} bar needs Kv {Kvc:.1f} for water but {Kvg:.1f} for a glycol mix of SG {SGg}.')])

# ---------------------------------------------------------------- Acres to hectares
ACRE = 4046.8564224
SURVEY_ACRE = 43560 * (1200 / 3937) ** 2
a0 = 1.0
ha0, m20, ft20 = a0 * ACRE / 1e4, a0 * ACRE, a0 * ACRE / 0.09290304
farm = 12.5
farm_ha = farm * ACRE / 1e4
farm_are = farm_ha * 100
plot_m = (120.0, 85.0)
plot_ha = plot_m[0] * plot_m[1] / 1e4
plot_ac = plot_m[0] * plot_m[1] / ACRE
rule = 100 * 2.5
exact = 100 * 1e4 / ACRE
rule_err = (rule - exact) / exact * 100
diff_ppm = (SURVEY_ACRE - ACRE) / ACRE * 1e6
sq_rows = ''
for ac in (0.25, 0.5, 1, 2, 5, 10, 25):
    s_m = math.sqrt(ac * ACRE)
    sq_rows += f"| {ac:g} acre | {ac*ACRE/1e4:.4f} ha | {s_m:.1f} m | {s_m/0.3048:.0f} ft |\n"

edit('conversion/acres-to-hectares', date=U, phrase='acres to hectares calculator',
    intro=("Acres measure land in the US, UK and India, while the hectare is the metric land unit used in most of the world. "
           "One hectare is about 2.47 acres. This acres to hectares calculator converts in both directions and also shows square metres and square feet.\n\n"
           "Farmers, land buyers, surveyors and agronomists use it to compare land records, sale listings, crop yields per hectare and subsidy limits that are quoted in different units."),
    body_add=f'''
## Worked example with the default value

The default is **{a0:g} acre**. Because one acre is exactly {ACRE:,.7f} m²:

- Hectares = {ACRE:,.4f} ÷ 10,000 = **{ha0:.6f} ha**
- Square metres = **{m20:,.2f} m²**
- Square feet = {ACRE:,.4f} ÷ 0.09290304 = **{ft20:,.0f} ft²**

A **{farm:g} acre** farm is {farm:g} × 0.4046856 = **{farm_ha:.4f} ha**, which a land record written in hectares and ares (1 are = 100 m²) shows as about {farm_are:.0f} ares. Going the other way, a rectangular field of {plot_m[0]:g} m by {plot_m[1]:g} m covers {plot_m[0]*plot_m[1]:,.0f} m², which is **{plot_ha:.2f} ha** or **{plot_ac:.4f} acres**.

## Side of a square plot for a given area

| Area | Hectares | Side of square (m) | Side of square (ft) |
|---|---|---|---|
{sq_rows}
This helps you picture a listing: a 1 acre square plot is about 64 m on each side, and a 10 acre square is roughly 200 m across.

## How land area is measured in practice

Land is rarely a neat rectangle, so surveyors split a plot into triangles or use the coordinate (shoelace) method on corner points taken with a total station or a survey grade GNSS receiver. The area is computed in square metres on the projected map grid and then expressed in hectares, acres or local units. Handheld phone GPS apps are fine for a rough check but can be off by several percent on a small plot, since each corner can be a few metres out. In many Indian states the official record, such as the Maharashtra 7/12 extract, states area in hectares and ares, so converting a seller's acre figure is the first step in checking it.

## Common mistakes

- **Using 2.5 acres per hectare.** The shortcut is {rule_err:.1f}% high: 100 ha is {exact:.1f} acres, not {rule:.0f}.
- **Confusing ares with acres.** An are is 100 m², about one fortieth of an acre, so "20 are" is 0.2 ha, not 20 acres.
- **Comparing gross and net area.** A layout's gross acreage includes roads and open space; the plots for sale may cover only 60% to 70% of it.
- **Converting a side length with the area factor.** To convert plot dimensions, convert each side in metres or feet first, then multiply.
- **Worrying about the US survey acre.** Older US deeds use the survey acre, {SURVEY_ACRE:,.3f} m², only {diff_ppm:.0f} parts per million larger, which matters for nothing but very large tracts.
''',
    faq_add=[('Is the rule of 2.5 acres per hectare accurate enough?',
              f'For a quick estimate, yes, but it overstates by about {rule_err:.1f}%. On 100 ha that is {rule - exact:.1f} acres too many, so use 2.47105 for anything you buy, sell or report.'),
             ('What is an are and how does it relate to a hectare?',
              'An are is 100 m², a square 10 m on each side. One hectare is 100 ares, and one acre is about 40.47 ares. Land records in several countries and Indian states list area in hectares and ares.')])

# ---------------------------------------------------------------- Power converter
HP, PS, BTUH, TR = 745.69987158, 735.49875, 0.29307107, 3516.8528
p0 = 1000.0
d_hp, d_ps, d_btu, d_tr, d_mw = p0 / HP, p0 / PS, p0 / BTUH, p0 / TR, p0 / 1e6
# chiller example
tr_c = 7.5
kw_c = tr_c * TR / 1000
btu_c = tr_c * TR / BTUH
cop = 3.2
kw_in = kw_c / cop
hp_in = kw_in * 1000 / HP
# chilled water capacity check
vflow, dT, rho, cp = 4.5, 5.0, 1000.0, 4.186
q_w = vflow / 3600 * rho * cp * dT
q_tr = q_w * 1000 / TR
# heater
heater = 2000.0
heater_btu = heater / BTUH
# AC 1.5 TR electrical
ac_kw = 1.5 * TR / 1000
ac_in = ac_kw / 3.5
others = [('Boiler horsepower', 9809.5), ('kcal per hour', 1.163), ('Foot-pound per second', 1.3558179483),
          ('Electrical horsepower', 746.0), ('Calorie per second (thermochemical)', 4.184)]
o_rows = ''.join(f"| {n} | {w:,.4g} W | {1000/w:,.4g} |\n" for n, w in others)

edit('conversion/power-converter', date=U, phrase='power converter calculator',
    intro=("Power ratings come in watts, kilowatts, horsepower, metric PS, BTU per hour and tons of refrigeration. "
           "This power converter calculator turns a figure in any one of them into all the others at once, using exact conversion factors.\n\n"
           "HVAC technicians, mechanical engineers and buyers use it to compare chillers, heaters, motors and air conditioners that are rated in different units, "
           "and to check cooling capacity against electrical input."),
    body_add=f'''
## Worked example with the default value

The calculator starts at **1 kW**, which is {p0:g} W:

- {p0:g} ÷ {HP:.4f} = **{d_hp:.4f} hp**
- {p0:g} ÷ {PS:.4f} = **{d_ps:.4f} PS**
- {p0:g} ÷ {BTUH} = **{d_btu:,.1f} BTU/h**
- {p0:g} ÷ {TR:.2f} = **{d_tr:.5f} TR**, and {d_mw:g} MW

## Example: a small chiller, from tons to kW and back

A cold store uses a **{tr_c:g} TR** chiller. Its cooling output is {tr_c:g} × {TR/1000:.4f} = **{kw_c:.2f} kW**, or {btu_c:,.0f} BTU/h. With a coefficient of performance (COP) of {cop}, the compressor draws about {kw_c:.2f} ÷ {cop} = **{kw_in:.2f} kW** of electricity, roughly {hp_in:.1f} hp, so the motor and cable are sized for about a third of the cooling figure.

To check what the chiller actually delivers, measure the chilled water flow and temperature drop. With {vflow:g} m³/h and a {dT:g} K difference, cooling = {vflow:g} ÷ 3600 × {rho:g} × {cp} × {dT:g} = **{q_w:.2f} kW**, which is {q_tr:.2f} TR. That is close to the rating, so the unit is working near full capacity. A {heater:,.0f} W fan heater in the same room adds {heater_btu:,.0f} BTU/h of load.

## Other power units you may meet

| Unit | Equal to | Units per kW |
|---|---|---|
{o_rows}
Boiler horsepower is a steam rating, about 13 times a mechanical horsepower, so never mix the two.

## How power is measured

Electrical input is read with a power analyser or a clamp wattmeter that measures voltage, current and power factor together. Shaft power is measured with a torque transducer or dynamometer and the speed, using P = 2π × N × T. Heating and cooling capacity is worked out from mass flow, specific heat and temperature change, as in the chiller check above, which is why air conditioner ratings are given in BTU/h or TR rather than watts of electricity.

## Common mistakes

- **Writing BTU when you mean BTU/h.** BTU is energy; BTU/h is power. A "12,000 BTU" air conditioner is 12,000 BTU/h.
- **Treating cooling capacity as electrical load.** A 1.5 TR unit gives {ac_kw:.2f} kW of cooling but, at a COP of 3.5, draws only about {ac_in:.2f} kW.
- **Using kVA as kW.** Generator and UPS ratings in kVA must be multiplied by the power factor before comparing with kW loads.
- **Mixing hp and PS.** Metric PS is 1.4% smaller than mechanical hp, so 100 PS is 98.6 hp.
- **Confusing boiler horsepower with engine horsepower.** One boiler hp is 9.81 kW, not 0.746 kW.
''',
    faq_add=[('How do I convert kcal/h to kW?',
              'Multiply by 1.163 and divide by 1,000. One kW is about 859.8 kcal/h, so a 50,000 kcal/h burner is 58.15 kW.'),
             ('How much electricity does a 1.5 ton air conditioner use?',
              f'Its cooling output is {ac_kw:.2f} kW. Divide by the COP to get the input: at a COP of 3.5 it draws about {ac_in:.2f} kW while the compressor runs. Inverter units draw less at part load.')])

# ---------------------------------------------------------------- Slope
x1, y1, x2, y2 = 1.0, 2.0, 4.0, 6.0
m = (y2 - y1) / (x2 - x1)
# swapped order gives the same slope
m_sw = (y1 - y2) / (x1 - x2)
# drain example in metres
dx, z1, z2 = 25.0, 100.00, 99.50
md = (z2 - z1) / dx
ang_d = math.degrees(math.atan(md))
slope_len = math.hypot(dx, z2 - z1)
# ramp example: 600 mm rise at 1:12
rise_r = 0.6
run_r = rise_r * 12
len_r = math.hypot(run_r, rise_r)
r_rows = ''
for n in (1, 1.5, 2, 3, 4, 12, 20, 50, 100):
    sl = 1 / n
    r_rows += f"| 1 : {n:g} | {sl:.4g} | {sl*100:.3g}% | {math.degrees(math.atan(sl)):.2f}° |\n"
# common wrong answer: run over rise
wrong = (x2 - x1) / (y2 - y1)

edit('math/slope', date=U, phrase='slope calculator', before='## Related calculators',
    intro=("Slope measures how steep a line is: the rise divided by the run between two points. "
           "This slope calculator finds it from two points and also returns the y-intercept, the line equation y = mx + b, the percent grade, the angle and the distance.\n\n"
           "Students use it to check algebra and graphing homework, while builders, surveyors and plumbers use the same rise over run to set ramps, drains and road grades."),
    body_add=f'''
## Does the order of the points matter?

No. Taking the points the other way round gives ({y1:g} − {y2:g}) ÷ ({x1:g} − {x2:g}) = {m_sw:.4f}, the same {m:.4f} as before, because both the rise and the run change sign. What matters is that you subtract in the **same order** on the top and the bottom.

## Second example: the fall of a drain pipe

A site level reads the pipe invert at **{z1:.2f} m** at the manhole and **{z2:.2f} m** at a point {dx:g} m downstream. Take x as distance and y as level, so the points are (0, {z1:.2f}) and ({dx:g}, {z2:.2f}):

- Slope m = ({z2:.2f} − {z1:.2f}) ÷ {dx:g} = **{md:.3f}**, a fall of {abs(md)*100:.0f}% or 1 in {abs(1/md):.0f}
- Angle = tan⁻¹({md:.3f}) = **{ang_d:.3f}°**
- Length along the pipe = √({dx:g}² + {abs(z2-z1):.2f}²) = {slope_len:.3f} m, almost the same as the plan distance

The negative sign simply says the pipe falls in the direction of flow, which is what you want.

## Slope ratios, grade and angle

| Ratio (rise : run) | Slope | Grade | Angle |
|---|---|---|---|
{r_rows}
Ratios are common on drawings: embankments are written as 1 : 2 or 1 : 3, and access ramps as 1 : 12. A ramp rising {rise_r*1000:.0f} mm at 1 : 12 needs {run_r:.1f} m of run and a sloping length of {len_r:.2f} m.

## How slope is measured on site

Surveyors find slope with a level and staff: they read the height at two points, measure the horizontal distance between them, and divide. Laser levels and digital inclinometers show the angle or percent grade directly, and road designers take grades from the vertical profile of a survey. On a graph, pick two points far apart on the line so reading errors in the coordinates have less effect on the slope.

## Common mistakes

- **Dividing run by rise.** For the default points that gives {wrong:.2f} instead of {m:.3f}; slope is always change in y over change in x.
- **Mixing the order of subtraction.** Using y₂ − y₁ on top but x₁ − x₂ underneath flips the sign of the answer.
- **Reading percent grade as degrees.** A 10% grade is only {math.degrees(math.atan(0.1)):.2f}°, and a 100% grade is 45°.
- **Using the sloping length as the run.** The run is the horizontal distance; on steep ground the length along the surface is noticeably longer.
- **Expecting a number for a vertical line.** When x₁ equals x₂ the run is zero and the slope is undefined, so the calculator cannot return a value.
''',
    faq_add=[('How do I convert a slope ratio like 1:12 into a percentage?',
              'Divide the rise by the run and multiply by 100. A 1:12 ramp has a slope of 1 ÷ 12 = 0.0833, which is an 8.33% grade or 4.76°.'),
             ('Does it matter which point I call the first point?',
              f'No. Swapping the points changes the sign of both the rise and the run, so the slope stays the same. For (1, 2) and (4, 6) it is {m:.3f} either way.')])

# ---------------------------------------------------------------- DNA / RNA concentration
f0, a260, a280, dil = 50, 0.45, 0.24, 10
c0 = a260 * f0 * dil
r0 = a260 / a280
vol = 50.0
yield0 = c0 * vol / 1000
# RNA example on a micro-volume instrument
fr, ar260, ar280 = 40, 0.62, 0.30
cr = ar260 * fr
rr = ar260 / ar280
need_ng = 1000.0
v_need = need_ng / cr
# loading volume table from default stock
l_rows = ''
for ng in (50, 100, 250, 500, 1000, 2000):
    l_rows += f"| {ng:,} ng | {ng / c0:.2f} µL |\n"
# 1 mm path reading
a_1mm = 0.30
c_1mm = a_1mm * 10 * 50

edit_keep_featured('biology/dna-concentration', date=U, phrase='DNA / RNA concentration calculator',
    intro=("DNA and RNA absorb ultraviolet light at 260 nm, so a spectrophotometer reading gives their concentration directly, and the A260/A280 ratio shows how pure the sample is. "
           "This DNA / RNA concentration calculator applies the right factor for dsDNA, ssDNA or RNA.\n\n"
           "Molecular biologists use it after every extraction or clean-up to work out how much sample to add to a PCR, a ligation, cDNA synthesis or a sequencing library."),
    body_add=f'''
## From concentration to pipetting volume

At the default result of **{c0:g} ng/µL**, a {vol:g} µL elution holds {c0:g} × {vol:g} ÷ 1,000 = **{yield0:.2f} µg**. The volume to pipette for a set mass is mass ÷ concentration:

| DNA needed | Volume of {c0:g} ng/µL stock |
|---|---|
{l_rows}
Volumes below about 1 µL are hard to pipette accurately, so dilute the stock first when you need small amounts.

## Second example: RNA for cDNA synthesis

An RNA prep measured undiluted on a micro-volume instrument reads A260 = {ar260} and A280 = {ar280}:

- Concentration = {ar260} × {fr} × 1 = **{cr:.1f} ng/µL** (choose the RNA factor)
- A260/A280 = {ar260} ÷ {ar280} = **{rr:.2f}**, normal for clean RNA

A reverse transcription that takes 1 µg of RNA would need {need_ng:,.0f} ÷ {cr:.1f} = {v_need:.1f} µL, more than most 20 µL reactions allow. The choice is to use less RNA, which is fine for many kits, or to concentrate the sample by precipitation or a column with a small elution volume.

## Readings from a short path length

The factors on this page assume a 1 cm path. A reading of {a_1mm} taken through a 1 mm path, if the instrument does not normalise it, corresponds to {a_1mm} × 10 = {a_1mm*10:g} at 1 cm, which is {c_1mm:g} ng/µL of dsDNA. Enter the 1 cm equivalent as the A260, or put 10 in the dilution box.
''',
    faq_add=[('How do I correct a reading taken with a 1 mm path length?',
              f'Multiply the absorbance by 10 to get the 1 cm equivalent before applying the factor. A dsDNA reading of {a_1mm} at 1 mm is {a_1mm*10:g} at 1 cm, or {c_1mm:g} ng/µL. Most micro-volume instruments do this for you.'),
             ('How much sample volume do I need for a set mass of DNA?',
              f'Divide the mass by the concentration. For 500 ng from a {c0:g} ng/µL stock you need 500 ÷ {c0:g} = {500/c0:.2f} µL.')])

for cid in ('engineering/control-valve-kv-cv', 'conversion/acres-to-hectares', 'conversion/power-converter', 'math/slope', 'biology/dna-concentration'):
    print(cid, inplace.body_words(cid))

# ======================================================================= SECTION _expand_c5.py
"""Expand (2026-11-20), slice 5: due-date, sample-size, standard-deviation, cell-doubling-time,
combinations. All five are featured, so the flag is lifted around the edit and restored unchanged.
Numbers computed here from each page's default inputs. Run once on the original files."""
import sys, os, math, datetime as dt, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import inplace
from inplace import edit
from scipy.stats import norm
from scipy.integrate import quad
U = '2026-11-20'


def edit_keep_featured(cid, **kw):
    """The page is already featured. Lift the flag around the edit and restore it unchanged."""
    path = os.path.join(inplace.BASE, cid + '.mdx')
    s = open(path).read()
    line = 'featured: true\n'
    assert s.count(line) == 1, cid
    open(path, 'w').write(s.replace(line, '', 1))
    try:
        n = edit(cid, **kw)
    except Exception:
        open(path, 'w').write(s)
        raise
    t = open(path).read()
    k = t.index('\nupdated: ')
    k = t.index('\n', k + 1) + 1
    open(path, 'w').write(t[:k] + line + t[k:])
    return n


def fd(x):
    return x.strftime('%d %b %Y').lstrip('0')


# ---------------------------------------------------------------- Due date
# Defaults: LMP 70 days before today, 28-day cycle
d_wk = (70 - 0) / 7
d_left = 280 - 70
# Fixed example: LMP 3 March 2026, 31-day cycle, checked on 1 June 2026
lmp = dt.date(2026, 3, 3)
cyc = 31
due = lmp + dt.timedelta(280 + cyc - 28)
chk = dt.date(2026, 6, 1)
ga_days = (chk - lmp).days - (cyc - 28)
ga_w, ga_d = divmod(ga_days, 7)
left = (due - chk).days
conc = lmp + dt.timedelta(14 + cyc - 28)
assert (due - conc).days == 266
term37 = due - dt.timedelta(21)
c_rows = ''
for c in (24, 26, 28, 30, 32, 35):
    dd = lmp + dt.timedelta(280 + c - 28)
    ov = lmp + dt.timedelta(c - 14)
    c_rows += f"| {c} days | {fd(ov)} | {fd(dd)} | {c - 28:+d} days |\n"
# milestone dates for the fixed example (gestational weeks counted from the cycle-adjusted LMP)
adj = lmp + dt.timedelta(cyc - 28)
m_rows = ''
for w, what in ((12, 'End of week 12, typical dating scan window closes'), (20, 'Week 20, midpoint, around the anatomy scan'),
                (28, 'Week 28, start of the third trimester'), (37, 'Week 37, early term begins'),
                (40, 'Week 40, estimated due date'), (42, 'Week 42, late term ends')):
    m_rows += f"| {w} | {fd(adj + dt.timedelta(7 * w))} | {what} |\n"
assert adj + dt.timedelta(280) == due

edit_keep_featured('other/due-date', date=U, phrase='pregnancy due date calculator',
     intro=("A pregnancy due date is usually estimated as 280 days, or 40 weeks, from the first day of the last menstrual period. "
            "This pregnancy due date calculator applies that rule, adjusts it for longer or shorter cycles, and shows how many weeks pregnant you are today.\n\n"
            "Expectant parents use it to plan leave and appointments, and it gives a quick cross-check of the date a midwife or doctor sets, "
            "which is often refined later by an early ultrasound scan."),
     before='## Common mistakes',
     body_add=f'''
## What the default values show

The calculator opens with a last period that started 70 days before today and a 28-day cycle. Seventy days is exactly **{d_wk:.1f} weeks**, so the result reads 10.0 weeks pregnant, and the due date falls 280 − 70 = **{d_left} days** from today. Change the date to your own and the three results update together.

## Worked example with a longer cycle

Suppose the last period began on **{fd(lmp)}** and cycles are usually **{cyc} days**. Ovulation is then expected about 3 days later than in a 28-day cycle, so:

- Due date = {fd(lmp)} + 280 + ({cyc} − 28) days = **{fd(due)}**
- Likely conception, about 14 days before the next period: **{fd(conc)}**, which is 266 days before the due date
- On {fd(chk)}: ({(chk - lmp).days} − {cyc - 28}) days ÷ 7 = **{ga_days / 7:.1f} weeks**, or {ga_w} weeks {ga_d} days, with **{left} days** to go
- 37 weeks (early term) is reached on {fd(term37)}, three weeks before the due date

## How cycle length moves the date

Same last period ({fd(lmp)}), different cycle lengths:

| Cycle length | Expected ovulation | Estimated due date | Shift from 28 days |
|---|---|---|---|
{c_rows}
## Milestone dates for the worked example

| Week | Date | What it marks |
|---|---|---|
{m_rows}
## How the date is confirmed in practice

At the first scan, usually between about 8 and 14 weeks, the sonographer measures the crown to rump length of the embryo. In the first trimester this length tracks age closely, to within about 5 to 7 days, which is better than a period date that relies on memory and a regular cycle. Professional guidance such as that from ACOG suggests keeping the period-based date unless the scan differs by more than a set margin (about 5 to 7 days in the first trimester), so a small difference usually leaves the date unchanged. After that point the agreed date is not normally moved again, even if later scans measure the baby larger or smaller.
''',
     replace=[('- **Keeping the period-based date after a dating scan.** If an early ultrasound gives a different date, your doctor or midwife will usually use the scan date. Always follow their advice.',
               '- **Keeping the period-based date after a dating scan.** If an early ultrasound gives a different date, your doctor or midwife will usually use the scan date. Always follow their advice.\n'
               '- **Taking a light bleed in early pregnancy for a period.** Spotting around the time a period was due can make the last period look 4 weeks later than it was, so the scan then measures much larger than expected.\n'
               '- **Adding the cycle correction to an IVF pregnancy.** With IVF the transfer date fixes the embryo age, so the cycle length you enter here does not apply.')],
     faq_add=[('How many weeks pregnant am I if my last period started 70 days ago?',
               'Exactly 10 weeks 0 days by gestational age, with a 28-day cycle. The due date is then 210 days away. Gestational age counts from the period, so the embryo itself is about 8 weeks old.'),
              ('What date am I 37 weeks pregnant?',
               f'Take 21 days off the due date. With a due date of {fd(due)}, 37 weeks is reached on {fd(term37)}. From then on a birth is counted as term.')])

# ---------------------------------------------------------------- Sample size
z95, z80 = norm.ppf(0.975), norm.ppf(0.80)
E, p, N = 0.05, 0.5, 10000
n0 = math.ceil(z95 ** 2 * p * (1 - p) / E ** 2)
n_fpc = math.ceil(z95 ** 2 * p * (1 - p) / E ** 2 / (1 + (z95 ** 2 * p * (1 - p) / E ** 2 - 1) / N))
assert (n0, n_fpc) == (385, 370), (n0, n_fpc)
p_rows = ''
for pp in (0.05, 0.10, 0.20, 0.30, 0.40, 0.50):
    a = z95 ** 2 * pp * (1 - pp) / E ** 2
    inf = math.ceil(a)
    fin = math.ceil(a / (1 + (a - 1) / N))
    a3 = z95 ** 2 * pp * (1 - pp) / 0.03 ** 2
    p_rows += f"| {pp*100:g}%{'' if pp == 0.5 else f' or {100-pp*100:g}%'} | {inf:,} | {fin:,} | {math.ceil(a3):,} |\n"
p10 = math.ceil(z95 ** 2 * 0.1 * 0.9 / E ** 2)
# A/B test: 10% vs 12% conversion, alpha 0.05 two-sided, 80% power
p1, p2 = 0.10, 0.12
pb = (p1 + p2) / 2
nab = math.ceil((z95 * math.sqrt(2 * pb * (1 - pb)) + z80 * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2)
p3 = 0.13
nab3 = math.ceil((z95 * math.sqrt(2 * ((p1 + p3) / 2) * (1 - (p1 + p3) / 2)) + z80 * math.sqrt(p1 * (1 - p1) + p3 * (1 - p3))) ** 2 / (p3 - p1) ** 2)
# Staff survey: N = 600, target 95% +-5%, 60% response rate
Ns = 600
a = z95 ** 2 * 0.25 / E ** 2
ns = math.ceil(a / (1 + (a - 1) / Ns))
inv = math.ceil(ns / 0.6)

edit_keep_featured('statistics/sample-size', date=U, phrase='sample size calculator',
     intro=("Sample size is the number of completed responses a survey needs so that its results land within a chosen margin of error at a chosen confidence level. "
            "This sample size calculator uses the standard formula for a proportion and applies the finite population correction for smaller groups.\n\n"
            "Market researchers, students writing a thesis, HR teams running staff surveys and quality engineers use it before fieldwork starts, "
            "to set a target that is large enough to trust without wasting effort on extra responses."),
     before='## Common mistakes',
     body_add=f'''
## When you already know roughly what the answer will be

The 50% default gives the largest sample. If an earlier survey showed that about 10% of customers use a feature, p(1 − p) falls from 0.25 to 0.09 and the sample needed drops sharply. Values for ±5% and ±3% margins at 95% confidence:

| Expected proportion | ±5%, large population | ±5%, population 10,000 | ±3%, large population |
|---|---|---|---|
{p_rows}
A proportion of 10% and 90% need the same sample, because p(1 − p) is symmetric. Only use a value below 50% when it comes from real prior data; guessing low makes the survey too small.

## Worked example: a staff survey in a company of {Ns}

An HR team wants ±5% at 95% confidence from {Ns} employees, with no prior estimate (p = 50%). The large-population figure is 385, but the population is small, so the correction applies: n = 384.15 ÷ (1 + 383.15 ÷ {Ns}) = **{ns} completed responses**. Past surveys got a 60% response rate, so the team invites {ns} ÷ 0.6 = **{inv} people**, which is almost everyone. In small groups it is often simpler to invite the whole population.

## A/B test sample size per group

Comparing two conversion rates needs a power calculation, not the formula above. To detect a lift from **10% to 12%** with a two-sided 5% significance level and 80% power, each group needs

<p class="formula">n = (z<sub>α/2</sub>√(2p̄q̄) + z<sub>β</sub>√(p₁q₁ + p₂q₂))² ÷ (p₂ − p₁)²</p>

which gives **{nab:,} visitors per group** (z = 1.960 and 0.842, p̄ = 0.11). Detecting a bigger lift, 10% to 13%, needs only {nab3:,} per group: the sample grows with the inverse square of the difference you want to see.

## Drawing the sample in practice

The formula assumes every member of the population had the same chance of being picked. In practice that means starting from a complete list (the sampling frame), such as an employee register or customer database, and selecting at random from it, or using stratified sampling so each region or department is represented in proportion. Send reminders, track who has replied, and compare the profile of respondents with the population before trusting the margin of error.
''',
     replace=[('- **Forgetting the design effect** when sampling in clusters.',
               '- **Forgetting the design effect** when sampling in clusters.\n'
               '- **Rounding down.** 384.15 means 385 responses; stopping at 384 leaves the margin slightly wider than the target.')],
     faq_add=[('Can I use a smaller sample if I expect a low percentage?',
               f'Yes, if the estimate comes from real data. With an expected 10%, ±5% at 95% confidence needs {p10} responses instead of 385. If you are unsure, keep 50%, which is the safe choice.'),
              ('How many visitors does an A/B test need?',
               f'It depends on the lift you want to detect. To see 10% rise to 12% with 80% power at a 5% significance level, you need about {nab:,} visitors in each group.')])

# ---------------------------------------------------------------- Standard deviation
data = [4, 8, 6, 5, 3, 7, 9, 5]
m = st.mean(data); s = st.stdev(data); sp = st.pstdev(data)
assert (round(s, 4), round(sp, 4)) == (2.031, 1.8998)
cv = s / m * 100
se = s / math.sqrt(len(data))


def d2(n):
    f = lambda x: 1 - (1 - norm.cdf(x)) ** n - norm.cdf(x) ** n
    return quad(f, -12, 12)[0]


d_rows = ''
for k in (2, 3, 4, 5, 6, 8, 10):
    d_rows += f"| {k} | {d2(k):.3f} |\n"
# repeatability: 10 readings of a pressure gauge at a fixed 6.000 bar
rd = [6.02, 5.98, 6.01, 6.03, 5.99, 6.00, 6.04, 5.97, 6.01, 6.02]
rm, rs = st.mean(rd), st.stdev(rd)
rr = max(rd) - min(rd)
rse = rs / math.sqrt(len(rd))
rest = rr / d2(10)
dr = max(data) - min(data)
dest = dr / d2(8)

edit_keep_featured('statistics/standard-deviation', date=U, phrase='standard deviation calculator',
     intro=("Standard deviation measures how far values typically sit from their mean; a small value means the data are tightly clustered. "
            "This standard deviation calculator takes a pasted list and returns the sample and population results, variance, mean and count together.\n\n"
            "Students check homework with it, analysts use it to describe spread in survey and sales data, and engineers rely on it "
            "to judge the repeatability of measurements and the capability of a process."),
     before='## Common mistakes',
     body_add=f'''
## Reading the default results

For the default list the calculator shows s = {s:.4f}, σ = {sp:.4f} and a mean of {m}. Two more useful figures follow directly. The coefficient of variation is {s:.4f} ÷ {m} = **{cv:.1f}%**, so the values vary by about a third of their average. The standard error of the mean is {s:.4f} ÷ √8 = **{se:.3f}**, which tells you how uncertain the mean of 5.875 is, rather than how scattered the individual values are.

## Worked example: repeatability of a pressure gauge

A technician applies a steady 6.000 bar from a dead-weight tester and records ten readings: {', '.join(f'{x:.2f}' for x in rd)} bar.

- Mean = **{rm:.3f} bar**, so the average error is {(rm - 6) * 1000:+.0f} mbar
- Sample standard deviation s = **{rs * 1000:.1f} mbar**, the repeatability of the gauge
- Standard error of the mean = {rs * 1000:.1f} ÷ √10 = {rse * 1000:.1f} mbar
- About 95% of single readings fall within ±2s = ±{2 * rs * 1000:.0f} mbar of the mean

If the gauge is specified as ±0.5% of a 10 bar span (±50 mbar), the ±{2 * rs * 1000:.0f} mbar scatter plus the {(rm - 6) * 1000:+.0f} mbar bias already reaches about {(2 * rs + rm - 6) * 1000:.0f} mbar, right at the edge of the tolerance, so the gauge is a candidate for recalibration or replacement.

## Quick estimate from the range

On a shop floor, σ is often estimated from the range of a small subgroup: σ ≈ R ÷ d₂. The d₂ constants below are computed as the expected range of n values from a standard normal distribution.

| Subgroup size n | d₂ |
|---|---|
{d_rows}
For the ten gauge readings, R = {rr * 1000:.0f} mbar gives σ ≈ {rr * 1000:.0f} ÷ {d2(10):.3f} = **{rest * 1000:.1f} mbar**, close to the {rs * 1000:.1f} mbar from the full calculation. For the default list, R = {dr} and n = 8 give {dest:.2f}, against s = {s:.2f}. The range method wastes information, so use it only for quick checks and control charts with small subgroups.
''',
     replace=[('- **Letting one outlier decide the result.** Check the data for typing errors before you report it.',
               '- **Letting one outlier decide the result.** Check the data for typing errors before you report it.\n'
               '- **Using the shortcut Σx² − n x̄² with rounded numbers.** For large values close together, such as 1,000.12 and 1,000.15, the two terms nearly cancel and small rounding wipes out the answer; work from deviations about the mean and keep full precision.')],
     faq_add=[('How can I estimate standard deviation from the range?',
               f'Divide the range by the d₂ constant for your sample size: 1.128 for 2 values, 2.326 for 5 and {d2(10):.3f} for 10. It is a quick estimate used on control charts; the full calculation is more precise.'),
              ('What is the coefficient of variation of my data?',
               f'Divide the standard deviation by the mean and multiply by 100. For the default data it is {s:.4f} ÷ {m} = {cv:.1f}%. It only makes sense for data measured from a true zero, such as length or weight.')])

# ---------------------------------------------------------------- Cell doubling time
N0, Nf, t = 1e5, 8e5, 72.0
nd = math.log2(Nf / N0); td = t / nd
assert (nd, td) == (3.0, 24.0)
mu = math.log(2) / td
# Multi-point fit: counts at 0, 24, 48, 72 h
tp = [0, 24, 48, 72]
cnt = [1.00e5, 1.85e5, 4.10e5, 7.60e5]
y = [math.log(c) for c in cnt]
tb, yb = st.mean(tp), st.mean(y)
slope = sum((a - tb) * (b - yb) for a, b in zip(tp, y)) / sum((a - tb) ** 2 for a in tp)
td_fit = math.log(2) / slope
td_2pt = 72 / math.log2(cnt[-1] / cnt[0])
g_rows = ''
for T in (0.33, 1, 6, 12, 18, 24, 36, 48):
    mu_h = math.log(2) / T
    week = 2 ** (168 / T)
    lbl = '20 min' if T == 0.33 else f'{T:g} h'
    g_rows += f"| {lbl} | {mu_h:.4f} | {mu_h * 24:.2f} | {week:.3g} |\n" if T >= 6 else f"| {lbl} | {mu_h:.4f} | {mu_h * 24:.1f} | very large |\n"
# Population doublings across passages at 1:4 and 1:3 splits
pd4 = math.log2(4); pd3 = math.log2(3)
pdl = 5 * pd4

edit_keep_featured('biology/cell-doubling-time', date=U, phrase='cell doubling time calculator',
     intro=("Doubling time is how long a cell population takes to double in number during steady, exponential growth. "
            "This cell doubling time calculator works it out from a starting count, a final count and the time between them, and also gives the number of doublings.\n\n"
            "Cell culture scientists use it to plan seeding and passaging, compare media or treatments, and spot slow or stressed lines early; "
            "microbiologists use the same maths for bacterial generation time."),
     before='## Common mistakes',
     body_add=f'''
## Growth rate from doubling time

Doubling time and the specific growth rate μ are two views of the same exponential curve: μ = ln 2 ÷ T<sub>d</sub>. The default result of {td:g} h is a growth rate of **{mu:.4f} per hour** ({mu * 24:.3f} per day). The table also shows how many times one cell would multiply in a week of unchecked growth, which explains why cultures must be split long before that.

| Doubling time | μ (per hour) | μ (per day) | Fold increase in 7 days |
|---|---|---|---|
{g_rows}
## Worked example: fitting more than two counts

A culture is counted every 24 hours: {', '.join(f'{c:,.0f}' for c in cnt)} cells at 0, 24, 48 and 72 h. Using only the first and last counts gives 72 ÷ log₂({cnt[-1] / cnt[0]:.1f}) = **{td_2pt:.1f} h**. A least-squares line through ln(count) against time has a slope of {slope:.5f} per hour, so T<sub>d</sub> = 0.6931 ÷ {slope:.5f} = **{td_fit:.1f} h**. The fit uses all four counts, so one noisy count moves it less. Plot ln(count) against time first: a straight line confirms exponential growth, while a curve flattening at the end shows the culture is reaching confluence.

## Tracking population doublings across passages

When cells are split at a fixed ratio and allowed to regrow to the same density, each passage adds log₂(split ratio) doublings. A 1:4 split adds {pd4:.0f} doublings and a 1:3 split adds {pd3:.2f}. Five passages at 1:4 therefore add **{pdl:.0f} population doublings** to the culture's PDL. Recording this alongside passage number matters for primary cells, which slow down and stop as they approach their limit.

## How the counts are made

Viable cells are usually counted after trypsinising a sample flask, either with a hemocytometer and trypan blue or with an automated counter that images stained cells. Count replicate flasks rather than one, mix the suspension well before loading, and keep the counting method the same at every time point. For bacteria, optical density at 600 nm or colony counts on plates take the place of direct counts.
''',
     replace=[('- **Using only two time points.** Count at three or more times and fit a line to ln(count) against time for a more reliable result.',
               '- **Using only two time points.** Count at three or more times and fit a line to ln(count) against time for a more reliable result.\n'
               '- **Mixing up doubling time and growth rate.** A higher growth rate means a shorter doubling time; convert with μ = 0.693 ÷ T<sub>d</sub> before comparing values from different papers.')],
     faq_add=[('How do I convert doubling time to specific growth rate?',
               f'Divide ln 2 (0.693) by the doubling time. A 24 hour doubling time is {mu:.4f} per hour, or {mu * 24:.3f} per day.'),
              ('How many population doublings is a 1:3 split?',
               f'log₂(3) = {pd3:.2f} doublings each time the cells regrow to the density they were split from. A 1:2 split is 1 doubling and a 1:8 split is 3.')])

# ---------------------------------------------------------------- Combinations
C = math.comb
c496 = C(49, 6)
assert c496 == 13983816
num = 49 * 48 * 47 * 46 * 45 * 44
pct = 100 / c496
t_rows = ''
for k in (6, 5, 4, 3, 2):
    w = C(6, k) * C(43, 6 - k)
    t_rows += f"| {k} | C(6,{k}) × C(43,{6 - k}) | {w:,} | 1 in {c496 / w:,.0f} |\n"
w3 = C(6, 3) * C(43, 3)
# Acceptance sampling: lot of 50 with 3 defectives, inspect 5
p_none = C(47, 5) / C(50, 5)
p_none10 = C(47, 10) / C(50, 10)
p_one = C(3, 1) * C(47, 4) / C(50, 5)

edit_keep_featured('statistics/combinations', date=U, phrase='combination calculator',
     intro=("A combination counts the ways to choose items from a set when order does not matter, such as lottery numbers, a committee or a sample of parts. "
            "This combination calculator works out nCr for any n and r and also gives the chance of picking one particular combination.\n\n"
            "Students use it for probability homework, players use it to understand lottery odds, "
            "and quality inspectors and researchers use it to work out how likely a random sample is to catch a problem."),
     before='## Common mistakes',
     body_add=f'''
## Worked example: the default 6 from 49

The defaults are n = 49 and r = 6. Writing out the factorials is not needed, because most of 49! cancels against 43!:

- 49C6 = (49 × 48 × 47 × 46 × 45 × 44) ÷ (6 × 5 × 4 × 3 × 2 × 1) = {num:,} ÷ 720 = **{c496:,}**
- Chance of one ticket matching all six = 1 ÷ {c496:,} = **{pct:.8f}%**, the value the calculator shows in percent

## Odds of each prize tier in a 6/49 lottery

To match exactly k of the 6 drawn numbers, choose k from the 6 winners and the rest from the 43 losers:

| Numbers matched | Calculation | Winning tickets | Odds |
|---|---|---|---|
{t_rows}
Matching 3 numbers happens about once in {c496 / w3:.0f} tickets, which is why the smallest prizes are paid so often while the jackpot rarely is.

## Using combinations in acceptance sampling

An inspector draws 5 parts at random from a lot of 50 that, unknown to them, contains 3 defective parts. The chance that the sample contains no defects is the number of all-good samples divided by all samples:

- P(no defect found) = C(47,5) ÷ C(50,5) = {C(47, 5):,} ÷ {C(50, 5):,} = **{p_none * 100:.1f}%**
- P(exactly one defect found) = C(3,1) × C(47,4) ÷ C(50,5) = **{p_one * 100:.1f}%**
- Doubling the sample to 10 parts lowers the miss chance to {p_none10 * 100:.1f}%

This is the hypergeometric distribution, and the same counting answers questions about card hands, jury selection and drawing coloured balls without replacement.
''',
     replace=[('- **Double counting** in "at least one" problems. It is usually easier to work out 1 − P(none).',
               '- **Double counting** in "at least one" problems. It is usually easier to work out 1 − P(none).\n'
               '- **Computing huge factorials on a basic calculator.** 49! has 63 digits and overflows many calculators; cancel the common factors first, as in the worked example.\n'
               '- **Treating r larger than n as valid.** You cannot choose 7 items from 5 without repetition, so nCr is 0; use combinations with repetition if items can be reused.')],
     faq_add=[('What are the odds of matching exactly 3 numbers in a 6/49 lottery?',
               f'C(6,3) × C(43,3) = {w3:,} winning tickets out of {c496:,}, so about 1 in {c496 / w3:.0f}.'),
              ('What is the chance a sample of 5 misses all 3 defects in a lot of 50?',
               f'C(47,5) ÷ C(50,5) = {p_none * 100:.1f}%. A sample that small passes a lot with 6% defective most of the time.')])

print('done', inplace.DONE)

# ======================================================================= SECTION _expand_c6.py
"""Expand (2026-11-20), slice 6: weibull-reliability, plc-analog-scaling, loop-resistance,
rtd-lead-wire-error, thermal-expansion. Numbers computed here from each page's default inputs
and its own equations. Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-20'
IB = 'https://www.instrumentationblog.in/'

# ---------------------------------------------------------------- Weibull reliability
b, eta, t = 1.5, 10000.0, 5000.0


def R(t, b=b, eta=eta):
    return math.exp(-(t / eta) ** b)


R0 = R(t)
hz = 1e6 * b / eta * (t / eta) ** (b - 1)
mttf = eta * math.gamma(1 + 1 / b)
b10 = eta * (-math.log(0.9)) ** (1 / b)
# conditional (mission) reliability: survived 5,000 h, chance of lasting another 1,000 h
Rc = R(6000) / R(5000)
Rnew = R(1000)
# time for 99% reliability (B1)
b1 = eta * (-math.log(0.99)) ** (1 / b)
# fitting example: 6 seal failures (h), median ranks (Benard), least squares of ln(-ln(1-F)) on ln t
fails = [2100, 3900, 5600, 7300, 9800, 13500]
n = len(fails)
xs, ys = [], []
mr_rows = ''
for i, tf in enumerate(fails, 1):
    F = (i - 0.3) / (n + 0.4)
    xs.append(math.log(tf)); ys.append(math.log(-math.log(1 - F)))
    mr_rows += f"| {i} | {tf:,} h | {F*100:.1f}% |\n"
mx, my = sum(xs) / n, sum(ys) / n
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
beta_fit = slope
eta_fit = math.exp(mx - my / slope)
# life table: B1, B10, B50 as fraction of eta for several beta
bl_rows = ''
for bb in (0.7, 1.0, 1.5, 2.0, 3.0, 4.0):
    q = [(-math.log(1 - p)) ** (1 / bb) for p in (0.01, 0.10, 0.50)]
    bl_rows += f"| {bb:g} | {q[0]:.4f} η | {q[1]:.4f} η | {q[2]:.4f} η | {math.gamma(1+1/bb):.4f} η |\n"
assert abs(R0 - 0.7022) < 1e-4 and abs(hz - 106.07) < 0.01 and round(mttf) == 9027 and round(b10) == 2231

edit('engineering/weibull-reliability', date=U, phrase='Weibull reliability calculator',
     intro=("The Weibull distribution models component life with two numbers: the shape parameter β, which tells early failures from random failures and wear-out, and the characteristic life η. "
            "This Weibull reliability calculator gives the reliability, failure probability, hazard rate, mean life and B10 life at any operating time.\n\n"
            "Reliability and maintenance engineers use it to set replacement intervals, compare suppliers and size spare part stocks from field or test failure data."),
     body_add=f'''
## Reliability over the next mission, not from new

Reliability from new is not the same as the chance that a unit already in service survives a little longer. For the default seal (β = {b:g}, η = {eta:,.0f} h) that has run {t:,.0f} h, the chance of lasting a further 1,000 h is

- R(6,000) ÷ R(5,000) = {R(6000):.4f} ÷ {R0:.4f} = **{Rc*100:.2f}%**

A new seal over its first 1,000 h has R(1,000) = **{Rnew*100:.2f}%**. The older seal is less likely to finish the next 1,000 h because β > 1 means the hazard rate climbs with age. With β = 1 the two numbers would be identical, which is the memoryless property of the exponential model. To reach 99% reliability from new (B1 life), the seal must be replaced by {b1:,.0f} h.

## Estimating β and η from failure records

Six seals from the same pump type failed at the hours below. Rank them, give each a median rank F = (i − 0.3) ÷ (n + 0.4) (Benard's approximation) and fit a straight line of ln(−ln(1 − F)) against ln(t).

| Order i | Failure time | Median rank F |
|---|---|---|
{mr_rows}
The least squares slope is **β ≈ {beta_fit:.2f}** and the line crosses 63.2% at **η ≈ {eta_fit:,.0f} h**. Those two numbers go straight into the calculator. With only six points the β estimate has a wide confidence band, so treat a value near 1 with caution before deciding whether failures are random or age related. Units removed for other reasons while still working are suspensions and need a rank adjustment (Johnson's method) or a maximum likelihood fit; leaving them out makes η look shorter than it is.

## Life at 1%, 10% and 50% failed

The B lives below are fractions of η, from B<sub>p</sub> = η (−ln(1 − p))<sup>1/β</sup>. Multiply by your η to get hours.

| β | B1 | B10 | B50 (median) | MTTF |
|---|---|---|---|---|
{bl_rows}
For β below about 3.6 the mean life sits above the median, because a few long survivors pull the average up. For a small β the B1 life is a tiny fraction of η, which is why early failures dominate the warranty cost of such parts.

## Common mistakes

- **Reading η as the mean life.** η is the 63.2% failure point. The mean is η Γ(1 + 1/β), which is {mttf:,.0f} h for the defaults, not {eta:,.0f} h.
- **Mixing failure modes in one fit.** Seal leaks and bearing seizures on the same pump have different β values. Fitting them together gives a bent plot and a β that describes neither.
- **Using calendar time for a part that ages with running hours or cycles.** Standby hours on a spare pump do not wear the seal the same way, so use operating hours, starts or cycles as the time axis.
- **Quoting the hazard rate at one time as a constant failure rate.** With β = {b:g} the rate at {t:,.0f} h is {hz:.1f} per 10⁶ h, but at 1,000 h it is only {1e6*b/eta*(0.1)**(b-1):.1f}. A single λ is valid only when β is close to 1.
- **Replacing parts with β ≤ 1 on a fixed schedule.** It adds early failures instead of removing wear-out ones, and costs parts and downtime for no gain.
''',
     faq_add=[('What is the chance a part that has already run for a while survives longer?',
               f'Use conditional reliability, R(t + Δt) ÷ R(t). For β = 1.5 and η = 10,000 h, a seal that has run 5,000 h has a {Rc*100:.1f}% chance of lasting another 1,000 h, compared with {Rnew*100:.1f}% for a new one.'),
              ('How many failures do I need to estimate the Weibull parameters?',
               'A rough β and η can come from 3 to 5 failures, but the estimate of β is uncertain until you have about 10 to 20. Include the units that are still running as suspensions, or η will be underestimated.')])

# ---------------------------------------------------------------- PLC analog scaling
Cmin, Cmax, Emin, Emax, C = 0, 27648, 0.0, 10.0, 20736
P = (C - Cmin) / (Cmax - Cmin)
EU = Emin + P * (Emax - Emin)
Res = (Emax - Emin) / (Cmax - Cmin)
wrong = Emin + (C - 0) / 32767 * (Emax - Emin)
# temperature transmitter -50 to 150 C, reverse direction: 85 C -> counts
tE = 85.0
tc = 0 + (tE - (-50)) / (150 - (-50)) * 27648
# live zero card: 6400 at 4 mA, 32000 at 20 mA, 0-6 m level, raw 19200
lz = 0 + (19200 - 6400) / (32000 - 6400) * 6.0
# signal table for 4-20 mA mapped to 0..27648, 0-10 bar
s_rows = ''
for I, note in ((3.6, 'NE 43 low fault'), (3.8, 'under range limit'), (4.0, '0%'), (8.0, '25%'), (12.0, '50%'),
                (16.0, '75%'), (20.0, '100%'), (20.5, 'over range limit'), (21.0, 'NE 43 high fault')):
    cnt = (I - 4) / 16 * 27648
    bar = (cnt - 0) / 27648 * 10
    s_rows += f"| {I:.1f} mA | {cnt:,.0f} | {bar:.4f} bar | {note} |\n"
assert abs(EU - 7.5) < 1e-9 and abs(P - 0.75) < 1e-12

edit('engineering/plc-analog-scaling', date=U, phrase='PLC analog scaling calculator',
     intro=("A PLC analog input card converts a 4 to 20 mA or 0 to 10 V signal into a raw integer, and the program must scale it to bar, °C or m³/h. "
            "This PLC analog scaling calculator converts raw counts to engineering units and back, with percent of range and the resolution of one count.\n\n"
            "Controls engineers use it when writing scaling blocks, and technicians use it during [PLC analog scaling from raw counts]("
            + IB + "plc-analog-scaling-raw-count/) checks and loop testing. See also [analog signal resolution in PLCs](" + IB + "analog-signal-resolution-in-plc/)."),
     body_add=f'''
## Going the other way: engineering units to counts

A temperature transmitter ranged −50 to 150 °C feeds the same 0 to 27,648 input. To find the count the PLC should show at **{tE:g} °C**, clear the raw count and enter {tE:g} as the value:

- Raw = 0 + ({tE:g} − (−50)) ÷ (150 − (−50)) × 27,648 = **{tc:,.0f} counts**

This is the number to compare with the PLC watch table while a calibrator simulates {tE:g} °C at the transmitter, and the value to type into a test sequence that writes simulated inputs.

## Cards with a live zero

Some cards report a non-zero count at 4 mA. Suppose a card is configured so 4 mA reads 6,400 and 20 mA reads 32,000, and it carries a 0 to 6 m level signal. Set raw low to 6,400 and raw high to 32,000; a reading of 19,200 counts is then (19,200 − 6,400) ÷ 25,600 × 6 = **{lz:.2f} m**. Entering 0 as raw low by mistake would show {19200/32000*6:.2f} m instead, an error of {19200/32000*6-lz:.2f} m that is largest at the bottom of the range.

## 4 to 20 mA on a 0 to 27,648 input, 0 to 10 bar

| Loop current | Raw count | Scaled value | Meaning |
|---|---|---|---|
{s_rows}
Counts below zero and above 27,648 are real readings on Siemens cards, which report down to about −4,864 and up to 32,511 before flagging under or overflow (32,767 or −32,768). Use them for fault alarms instead of clamping them away.

## Checking the scaling during commissioning

Disconnect the transmitter and drive the input with a loop calibrator in source mode, or put the calibrator in simulate mode in series with a loop powered input. Step through 4, 8, 12, 16 and 20 mA and record the raw count and the scaled value from the PLC watch table. Every point should land within a few counts of the values in the table above. A constant offset points to a wrong raw low value; an error that grows with signal points to a wrong raw high value or a wrong engineering span.

## Common mistakes

- **Using 32,767 as raw high on a Siemens card.** The default reading of {C:,} counts would then show {wrong:.3f} bar instead of {EU:g} bar, about {(EU-wrong)/EU*100:.0f}% low across the whole range.
- **Doing the division in integers.** (20,736 ÷ 27,648) in integer maths is 0, so the result sticks at the bottom of the range until the count reaches full scale. Convert to REAL before dividing.
- **Scaling the transmitter range twice.** If the transmitter or the card already outputs engineering units (HART variable or a card set to scale internally), scaling again in the program distorts the value.
- **Mismatching the range in the PLC and the transmitter.** A transmitter re-ranged to 0 to 16 bar in the field while the PLC still scales 0 to 10 bar reads 37.5% low everywhere.
- **Clamping before alarming.** Limiting the value to 0 to 100% first hides the 3.6 mA and 21 mA fault currents that the diagnostics need to see.
''',
     faq_add=[('What does the PLC show if I scale with 32767 instead of 27648?',
               f'Every reading is low by the ratio 27,648 ÷ 32,767, about 15.6%. A 0 to 10 bar signal at {C:,} counts would display {wrong:.3f} bar instead of {EU:g} bar.'),
              ('How do I scale a range that starts below zero?',
               f'Enter the negative value as engineering units at range low. For −50 to 150 °C on a 0 to 27,648 input, 85 °C corresponds to {tc:,.0f} counts and zero counts is −50 °C.')])

# ---------------------------------------------------------------- 4-20 mA loop resistance
Vs, Vt, Im, Rin, Rb, Ln, rc = 24.0, 10.5, 0.022, 250.0, 0.0, 500.0, 12.1
Rmax = (Vs - Vt) / Im
Rl = Rin + Rb + 2 * Ln / 1000 * rc
M = Rmax - Rl
Vtx = Vs - Im * Rl
Vneed = Vt + Im * Rl
Lmax = (Rmax - Rin) / (2 * rc / 1000)
# add a Zener barrier of 340 ohm and a loop indicator of 2 V (91 ohm equivalent at 22 mA)
Rz = 340.0
Rl_z = Rl + Rz
M_z = Rmax - Rl_z
Vtx_z = Vs - Im * Rl_z
# supply tolerance: 24 V -10%
Vlow = 21.6
Rmax_low = (Vlow - Vt) / Im
M_low = Rmax_low - Rl_z
# table: maximum one-way cable length for supply voltages, 250 ohm input, no barrier
l_rows = ''
for V in (18, 20, 24, 26, 30):
    rm = (V - Vt) / Im
    cells = []
    for r in (36.0, 18.1, 12.1):
        lm = (rm - Rin) / (2 * r / 1000)
        cells.append('not possible' if lm < 0 else f'{lm/1000:,.2f} km')
    l_rows += f"| {V} V | {rm:,.0f} Ω | " + ' | '.join(cells) + ' |\n'
assert abs(Rmax - 613.636) < 0.01 and abs(Rl - 262.1) < 1e-9 and abs(Vtx - 18.2338) < 1e-3

edit('engineering/loop-resistance', date=U, phrase='4 to 20 mA loop resistance calculator',
     intro=("A loop powered transmitter needs a minimum voltage at its terminals, and every resistor, barrier and cable in the [4 to 20 mA loop](" + IB + "4-to-20-ma-current-loop-explained/) uses part of the supply. "
            "This 4 to 20 mA loop resistance calculator gives the maximum allowed load, the actual load, the margin and the voltage left at the transmitter.\n\n"
            "Instrument designers use it to check [instrument loop impedance](" + IB + "instrument-loop-impedance-4-20ma-accuracy/) before choosing supplies, barriers and cable, so loops still work at [NAMUR NE 43](" + IB + "namur-ne43-standard-explained/) fault currents."),
     body_add=f'''
## Voltage left at the transmitter

The margin in ohms is easier to judge as volts at the transmitter terminals. With the default loop drawing {Im*1000:g} mA through {Rl:.1f} Ω, the receiver and cable drop {Im*Rl:.3f} V, so the transmitter sees

- V = {Vs:g} − {Im:.3f} × {Rl:.1f} = **{Vtx:.2f} V**, comfortably above its {Vt:g} V minimum

Turned around, the smallest supply this loop could run on is {Vt:g} + {Im:.3f} × {Rl:.1f} = **{Vneed:.2f} V**.

## Adding an intrinsic safety barrier

Put a shunt diode (Zener) barrier of about {Rz:g} Ω end to end into the same loop and the load becomes {Rl:.1f} + {Rz:g} = **{Rl_z:.1f} Ω**. The margin shrinks to **{M_z:.1f} Ω** and the transmitter is left with {Vtx_z:.2f} V. That still works on a full 24 V, but a supply at its −10% tolerance ({Vlow:g} V) allows only {Rmax_low:.0f} Ω, giving a margin of **{M_low:.0f} Ω**: the loop fails at high current. A galvanic isolator with a powered input, or a 26 V supply, fixes it.

## Maximum one-way cable length by supply voltage

Transmitter minimum {Vt:g} V, 22 mA, 250 Ω input, no barrier. Lengths are one way, for the conductor resistance of 0.5, 1.0 and 1.5 mm² copper.

| Supply | R<sub>max</sub> | 0.5 mm² (36 Ω/km) | 1.0 mm² (18.1 Ω/km) | 1.5 mm² (12.1 Ω/km) |
|---|---|---|---|---|
{l_rows}
Cable is rarely the limit in a plain loop; the receiver resistor and series devices use most of the budget. On an 18 V supply the 250 Ω input alone already exceeds what the transmitter can drive at 22 mA.

## Checking the loop on site

With the loop running, use the transmitter's loop test or HART command to force 22 mA (or 20.5 mA if 22 is not available). Measure the voltage across the transmitter terminals with a multimeter. It must stay at or above the datasheet minimum. Then measure across the receiver input; 250 Ω should show 5.5 V at 22 mA, and a much higher figure means a wrong resistor or a second receiver wired in series.

## Common mistakes

- **Using 20 mA as the design current.** The loop may pass at 20 mA and still collapse at the 21 mA or more used for fault signalling, so the alarm never reaches the DCS.
- **Taking the lift-off voltage for the basic model.** Display, HART and explosion proof options often raise the minimum voltage by 1 to 2 V; read the figure for the exact ordered version.
- **Forgetting series devices added later.** A field indicator, a trip amplifier or a second recorder each takes 1 to 5 V.
- **Designing on the nominal supply.** Use the lowest supply voltage after tolerance and diode drops from redundant supply modules.
- **Removing the 250 Ω to gain margin on a HART loop.** HART needs roughly 230 to 600 Ω of loop resistance; below that the handheld cannot communicate.
''',
     faq_add=[('How long can a 4 to 20 mA cable run be?',
               f'With a 24 V supply, a 10.5 V transmitter, 22 mA and a 250 Ω input, the budget left for cable is {Rmax-Rin:.0f} Ω. On 1.5 mm² copper (12.1 Ω/km per conductor) that allows about {Lmax/1000:.0f} km one way, so length is limited by noise and installation rather than resistance.'),
              ('What supply voltage does my loop need?',
               f'V supply = transmitter minimum voltage + maximum current × total loop resistance. For the default loop that is 10.5 + 0.022 × {Rl:.1f} = {Vneed:.2f} V; add the supply tolerance on top.')])

# ---------------------------------------------------------------- RTD lead wire error
rho, a, L, A, mm = 1.724e-8, 0.00385, 50.0, 0.5e-6, 0.05
Rw = rho * L / A
E2 = 2 * Rw
dT2 = E2 / (100 * a)
E3 = Rw * mm
dT3 = E3 / (100 * a)
dT2_1000 = E2 / (1000 * a)
# hot cable: cable at 60 C instead of 20 C
Rw_hot = Rw * (1 + 0.00393 * 40)
dT2_hot = 2 * Rw_hot / (100 * a)
# Pt100 sensitivity from Callendar-Van Dusen above 0 C
CA, CB = 3.9083e-3, -5.775e-7
sens = {T: 100 * (CA + 2 * CB * T) for T in (0, 100, 200, 400, 600)}
sens_rows = ''
for T, s in sens.items():
    sens_rows += f"| {T} °C | {s:.4f} Ω/°C | {E2/s:.2f} °C |\n"
# 3-wire mismatch table
m_rows = ''
for m in (0.01, 0.02, 0.05, 0.10):
    c1 = rho * 50 / 0.5e-6 * m / (100 * a)
    c2 = rho * 100 / 1.0e-6 * m / (100 * a)
    c3 = rho * 200 / 0.5e-6 * m / (100 * a)
    m_rows += f"| {m*100:g}% | {c1:.3f} °C | {c2:.3f} °C | {c3:.3f} °C |\n"
assert abs(Rw - 1.724) < 1e-9 and abs(dT2 - 8.9558) < 1e-3 and abs(dT3 - 0.22390) < 1e-4

edit('engineering/rtd-lead-wire-error', date=U, phrase='RTD lead wire error calculator',
     intro=("Every metre of copper between an RTD and its transmitter adds resistance that the instrument reads as extra temperature. "
            "This RTD lead wire error calculator shows the error for 2-wire and 3-wire Pt100 or Pt1000 circuits from cable length, conductor size and lead mismatch.\n\n"
            "Instrument engineers use it to choose the wiring method and cable size, and technicians use it to explain offsets. See the [difference between 2-wire, 3-wire and 4-wire RTDs]("
            + IB + "difference-between-2-wire-rtd-3-wire-rtd-and-4-wire-rtd/) and [how to test an RTD](" + IB + "how-to-test-an-rtd-pt100/)."),
     body_add=f'''
## What changes with a Pt1000 or a hot cable

Keep the default 50 m of 0.5 mm² cable but fit a Pt1000. Its sensitivity is 3.85 Ω/°C, so the same {E2:.3f} Ω of lead resistance reads only **{dT2_1000:.3f} °C** high in 2-wire, which many applications can accept without a third wire.

Lead resistance also follows the cable temperature. If the run passes over a furnace and averages 60 °C instead of 20 °C, one lead rises to {Rw:.3f} × (1 + 0.00393 × 40) = {Rw_hot:.3f} Ω, and the 2-wire Pt100 error becomes **{dT2_hot:.2f} °C** instead of {dT2:.2f} °C. Because the cable temperature changes with weather and process, this part of the error cannot be trimmed out with a fixed offset.

## The error is larger at high temperature

The calculator uses the mean coefficient 0.00385, i.e. 0.385 Ω/°C. The real Pt100 slope from the Callendar-Van Dusen equation falls as temperature rises, so the same lead resistance is worth more degrees on a hot process. For the default {E2:.3f} Ω 2-wire lead resistance:

| Process temperature | Pt100 slope dR/dT | 2-wire error |
|---|---|---|
{sens_rows}
## 3-wire error from lead mismatch

A 3-wire circuit leaves only the difference between two leads. The table gives the temperature error for a Pt100 at several mismatch levels.

| Mismatch | 50 m, 0.5 mm² | 100 m, 1.0 mm² | 200 m, 0.5 mm² |
|---|---|---|---|
{m_rows}
Mismatch of 1% to 2% is normal along one multicore cable. Each screw terminal, fuse terminal or marshalling link can add 5 to 20 mΩ to one lead only, which on short runs is a larger share than the cable itself.

## Measuring lead resistance on site

Isolate the RTD at the transmitter. On a 3-wire sensor, measure between the two wires of the same colour (usually two reds or two whites): the sensor element is not in that path, so the reading is the resistance of two leads in series. Half of it is one lead. Then measure from each of those wires to the third wire; the difference between the two readings is the lead mismatch. For a 2-wire sensor, short the leads at the sensor head and measure the loop from the transmitter end.

## Common mistakes

- **Using one-way length for the 2-wire error.** Current flows out and back, so both leads add; the calculator doubles R<sub>lead</sub> for that reason.
- **Assuming 3-wire cancels everything.** It cancels only equal leads. Different core sizes, a corroded terminal or a junction box splice break the balance.
- **Wiring a 4-wire sensor as 3-wire and leaving one core loose.** The spare core should be cut back and insulated at both ends, not landed on a terminal it shares with another lead.
- **Applying a lead offset trim to a 3-wire input.** The transmitter already compensates, so a manual trim of the measured lead resistance subtracts it twice.
- **Mixing Pt100 and Pt1000 settings.** A Pt1000 read on a Pt100 input shows about 10 times the resistance and the reading goes far over range; the reverse reads near −200 °C.
''',
     faq_add=[('How do I measure the lead resistance of an installed RTD?',
               'Disconnect the sensor at the transmitter and measure between the two same colour wires of a 3-wire RTD. That path does not include the element, so it is the resistance of two leads; half is one lead.'),
              ('Does a hot cable increase the RTD lead error?',
               f'Yes. Copper rises about 0.39% per °C, so 50 m of 0.5 mm² cable at 60 °C gives a 2-wire Pt100 error of about {dT2_hot:.1f} °C instead of {dT2:.1f} °C at 20 °C.')])

# ---------------------------------------------------------------- Thermal expansion
al, Lt, dTt = 12.0, 50.0, 60.0
dL = al * 1e-6 * Lt * dTt * 1000
assert abs(dL - 36.0) < 1e-9
hd = 200e-6 * 50 * (-30) * 1000
# restrained DN100 schedule 40 carbon steel pipe, 60 K rise
E = 200e9
Do, Di = 114.3, 102.26
Ap = math.pi / 4 * (Do ** 2 - Di ** 2)  # mm2
sig = E * al * 1e-6 * dTt / 1e6  # MPa
Fr = sig * Ap / 1000  # kN
# design range example: installed at 10 C, operating 180 C, winter shutdown -5 C
L2 = 80.0
up = al * 1e-6 * L2 * (180 - 10) * 1000
down = al * 1e-6 * L2 * (10 - (-5)) * 1000
tot = al * 1e-6 * L2 * (180 - (-5)) * 1000
mats = [('Carbon steel', 12), ('Stainless steel 304/316', 17.3), ('Copper', 16.5), ('Aluminium', 23.1),
        ('Cast iron', 10.5), ('PVC', 52), ('HDPE', 200), ('Glass', 9)]
t_rows = ''
for nm, aa in mats:
    t_rows += f"| {nm} | " + ' | '.join(f"{aa*1e-6*100*d*1000:,.0f} mm" for d in (20, 50, 100, 150)) + ' |\n'

edit('engineering/thermal-expansion', date=U, phrase='thermal expansion calculator',
     intro=("Most materials grow when heated and shrink when cooled, by an amount set by the coefficient of linear expansion, the length and the temperature change. "
            "This thermal expansion calculator works out that movement for steel, stainless steel, copper, aluminium, PVC, HDPE and glass.\n\n"
            "Piping designers use it to size expansion loops and bellows, while maintenance and installation teams use it to set gaps, guides and anchor points on hot lines."),
     body_add=f'''
## Design for the full temperature range

Pipe stress work uses the whole swing from the coldest to the hottest condition, not the difference from installation. Take an {L2:g} m carbon steel line installed at 10 °C, operating at 180 °C and shut down in winter at −5 °C:

- Growth from installation to operating: 12 × 10⁻⁶ × {L2:g} × 170 = **{up:.1f} mm**
- Shrinkage from installation to winter shutdown: 12 × 10⁻⁶ × {L2:g} × 15 = **{down:.1f} mm**
- Total movement the loop or bellows must take: **{tot:.1f} mm**

Contraction matters as much as growth for plastics. A 50 m HDPE water main laid in summer and cooled by 30 K shortens by **{abs(hd):.0f} mm** (enter ΔT = −30), which is enough to pull a push-fit joint apart if the pipe is not anchored or snaked in the trench. For steam lines, the layout of loops and anchors is covered in [pipe expansion loops in steam piping]({IB}pipe-expansion-loop-in-steam-piping/).

## Force from a fully restrained pipe

If the default 60 K rise is fully prevented, the stress is σ = E α ΔT = 200,000 MPa × 12 × 10⁻⁶ × 60 = **{sig:.0f} MPa**, independent of the pipe length. For a DN100 schedule 40 steel pipe (114.3 mm OD, 102.26 mm ID, metal area {Ap:,.0f} mm²) that stress pushes on the anchors with about **{Fr:,.0f} kN**. Anchors and nozzle connections are rarely designed for such loads, which is why the movement is allowed to happen and guided instead.

## Expansion of a 100 m run

| Material | ΔT 20 K | ΔT 50 K | ΔT 100 K | ΔT 150 K |
|---|---|---|---|---|
{t_rows}
## How expansion is measured

Coefficients are measured with a push rod dilatometer (ASTM E228), which heats a small sample in a furnace and records its length change with a displacement transducer, or with interferometry for low expansion materials such as glass and Invar. On a running plant, movement is checked with travel indicators on spring hangers and with marks on pipe shoes at guides, read cold and hot. The readings are compared with the stress analysis; a shoe that has walked off its support or a hanger at the end of its travel points to a blocked guide or a missing anchor.

## Common mistakes

- **Using installation to operating ΔT only.** The lowest ambient or shutdown temperature adds contraction, and the loop must absorb the full range.
- **Taking α at room temperature for a hot line.** The mean coefficient of carbon steel rises from about 11.7 × 10⁻⁶ near 20 °C to about 13 × 10⁻⁶ at 300 °C, so tables of mean α to the operating temperature give better answers for steam and hot oil.
- **Converting a °F difference with the temperature formula.** A 100 °F rise is 55.6 K, not 37.8 °C.
- **Treating plastics like metal.** HDPE moves more than 16 times as much as carbon steel and also creeps, so supports and anchors follow different rules.
- **Ignoring differential expansion.** A stainless liner in a carbon steel shell, or an aluminium cover on a steel frame, moves by the difference in α, which loosens bolts or bows the assembly.
''',
     faq_add=[('How much force does a restrained steel pipe produce when heated?',
               f'The stress is E × α × ΔT, about {sig:.0f} MPa for a 60 K rise in carbon steel, whatever the length. On a DN100 schedule 40 pipe that is about {Fr:,.0f} kN on each anchor.'),
              ('Which temperature difference should I use for pipe expansion?',
               'Use the difference between the coldest and hottest metal temperatures the line will see, including winter shutdown and steam out or cleaning cycles, not just installation to normal operation.')])

print('slice 6 done')
