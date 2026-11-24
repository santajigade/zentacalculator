"""Improve pass (2026-11-24) for thin pages from the first batch (2026-10-27):
ecology/carbon-offset-cost, sports/baseball-batting and food/food-cost.
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples from the calculator defaults, reference tables computed here,
practical notes and common mistakes. The baseball page had the same example twice; the second
copy is replaced by a new section. Slug, category, variables, equations, related and published
are unchanged (asserted by inplace.edit). Run once on the original files."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-24'


def m2(x):
    return f"{x:,.2f}"


# ---------------------------------------------------------------- Carbon offset cost
t, p = 5, 15
cost = t * p
mon = cost / 12
assert cost == 75 and abs(mon - 6.25) < 1e-9
price_rows = ''
for pp in (5, 15, 30, 50, 100, 600):
    price_rows += f"| {pp} | {m2(t*pp)} | {m2(t*pp/12)} | {m2(t*pp/365)} |\n"
fp_rows = ''
for name, tt in (('India average (about 2 t)', 2), ('Global average (about 4.7 t)', 4.7),
                 ('EU average (about 6 t)', 6), ('US average (about 14.5 t)', 14.5)):
    fp_rows += f"| {name} | {m2(tt*15)} | {m2(tt*30)} | {m2(tt*100)} |\n"
flight = 2 * p
fee = cost * 1.10
half_cost = (t / 2) * p
kg_cost = 800 / 1000 * p

edit('ecology/carbon-offset-cost', date=U, phrase='carbon offset cost calculator',
     title='Carbon Offset Cost Calculator: Price to Offset CO2 Emissions',
     description='Carbon offset cost calculator: enter tonnes of CO2 and the price per tonne to get the yearly and monthly cost of offsetting, with prices and examples.',
     intro=("A carbon offset is a credit for one tonne of CO2 that a verified project has avoided or removed, bought to balance emissions you cannot cut yet. "
            "This carbon offset cost calculator multiplies the tonnes you want to cover by the price per tonne and spreads the total over twelve months.\n\n"
            "Households, small businesses and event organisers use it to budget for offsetting flights, fuel and electricity, and to compare how much a cheap credit and a high quality removal credit would cost."),
     replace=[('''## Example

5 tonnes at 15 per tonne → **75** a year (**6.25** a month).''',
               f'''## Worked example with the default values

You want to offset {t} tonnes of CO2 a year and the provider charges {p} per tonne:

1. Yearly cost = {t} t × {p} per tonne = **{m2(cost)}**
2. Monthly cost = {m2(cost)} ÷ 12 = **{m2(mon)}**

The calculator stores mass in kilograms, so 5 t is treated as 5,000 kg and divided by 1,000 before it is multiplied by the price. The currency is whatever you type: the price and the result are always in the same unit.

## Cost of offsetting 5 tonnes at different prices

| Price per tonne | Per year | Per month | Per day |
|---|---|---|---|
{price_rows}
The spread is the main point: the same 5 tonnes can cost less than a cinema ticket a month with cheap avoidance credits or several hundred a month with engineered removals such as direct air capture.''')],
     body_add=f'''
## Offsetting a typical footprint

Using the per person averages from the table above, here is what a full year of emissions would cost to offset at three price levels:

| Footprint | At 15 per t | At 30 per t | At 100 per t |
|---|---|---|---|
{fp_rows}
A single return long haul flight of about 2 t costs {m2(flight)} to offset at {p} per tonne. Work out the tonnes first with the [flight emissions calculator](/ecology/flight-emissions/), then bring the figure here.

## Practical notes

- **Check what one credit covers.** One credit is normally one tonne of CO2 equivalent. If a site sells offsets "per flight" or "per month", divide its price by the tonnes it claims to cover to compare it with other providers.
- **Expect fees.** Retail providers often add a service margin. A 10% fee turns the {m2(cost)} example into {m2(fee)}.
- **Small amounts.** For 800 kg enter 0.8 t; at {p} per tonne that is {m2(kg_cost)}.
- **Reduce, then offset the remainder.** Cutting the footprint in half before buying credits halves the bill, so 2.5 t at {p} costs {m2(half_cost)} instead of {m2(cost)}.
- **Ask for retirement proof.** A good provider retires the credits on a public registry and gives you the serial numbers.

## Common mistakes

- **Mixing kilograms and tonnes.** Footprint tools often report kilograms; 5,000 kg is 5 t, not 5,000 t.
- **Comparing prices of different credit types.** Avoidance credits and removal credits are different products, so a lower price per tonne does not mean a better deal.
- **Offsetting CO2 only when the figure is CO2e.** Some footprints include methane and other gases as CO2 equivalent; buy credits for the CO2e total.
- **Forgetting it is a yearly figure.** The monthly value is the yearly cost divided by 12, so enter a full year of emissions to get a correct monthly budget.
- **Buying unverified credits.** Credits without an independent standard and registry can be double counted or never delivered.
''',
     faq_replace=[('How much does a carbon offset cost?', 'How much does a carbon offset cost?',
                   'Voluntary credits range from a few units of currency per tonne for renewable energy and some avoidance projects to several hundred per tonne for engineered carbon removal. Quality, project type and the year all move the price.'),
                  ('How much does it cost to offset a flight?', 'How much does it cost to offset a flight?',
                   f'A return long haul economy flight emits roughly 1 to 3 tonnes of CO2. At {p} per tonne that is about 15 to 45; at 100 per tonne it is 100 to 300.')],
     faq_add=[('How many carbon credits do I need?',
               'One credit usually covers one tonne of CO2 equivalent, so you need as many credits as tonnes you want to offset. Round up, because most registries do not sell fractions of a credit.')])

# ---------------------------------------------------------------- Baseball batting
ab, h, bb, hbp, sf = 500, 150, 60, 5, 5
avg = h / ab
num = h + bb + hbp
den = ab + bb + hbp + sf
obp = num / den
assert abs(avg - 0.3) < 1e-12 and num == 215 and den == 570 and f"{obp:.3f}" == '0.377'


def r3(x):
    s = f"{x:.3f}"
    return s[1:] if s.startswith('0') else s


hit_rows = ''
for hh in (100, 115, 125, 135, 150, 165):
    hit_rows += f"| {hh} | {r3(hh/ab)} | {r3((hh+bb+hbp)/den)} |\n"
walk_rows = ''
for w in (0, 30, 60, 90, 120):
    walk_rows += f"| {w} | {r3(h/ab)} | {r3((h+w+hbp)/(ab+w+hbp+sf))} |\n"
# hits needed for .300 from 140 in 480, with 20 AB left
need = 0.3 * 500 - 140
pa = ab + bb + hbp + sf
edit('sports/baseball-batting', date=U, phrase='batting average calculator',
     title='Batting Average Calculator: AVG and OBP for Baseball',
     description='Batting average calculator for baseball: enter at-bats, hits, walks, HBP and sacrifice flies to get AVG and on-base percentage (OBP) with a worked example.',
     intro=("Batting average shows how often a hitter turns an at-bat into a hit, and on-base percentage adds walks and hit by pitches to show how often he reaches base. "
            "This batting average calculator works out both from at-bats, hits, walks, HBP and sacrifice flies.\n\n"
            "Players, coaches, scorekeepers and fantasy baseball managers use it to check box score totals, compare hitters and see how a few extra hits or walks change a season line."),
     replace=[('''## Example

150 hits in 500 at-bats, 60 walks, 5 HBP, 5 sacrifice flies:

- AVG = **.300**
- OBP = **0.377**''',
               f'''## Worked example with the default values

A hitter has {h} hits in {ab} at-bats, with {bb} walks, {hbp} hit by pitches and {sf} sacrifice flies:

1. AVG = {h} ÷ {ab} = **{r3(avg)}**
2. OBP numerator = {h} + {bb} + {hbp} = {num}
3. OBP denominator = {ab} + {bb} + {hbp} + {sf} = {den}
4. OBP = {num} ÷ {den} = {obp:.5f}, shown as **{r3(obp)}**

So he reached base in about {obp*100:.1f}% of the {den} plate appearances that count for OBP, even though he hit safely in exactly 30% of his at-bats. The calculator shows OBP with a leading zero; box scores drop it and write {r3(obp)}.'''),
              ('''## Example season

500 AB, 150 H, 60 BB, 5 HBP, 5 SF:

- AVG = 150 ÷ 500 = **.300**
- OBP = 215 ÷ 570 = **.377**''',
               f'''## How hits change the line (500 AB, 60 BB, 5 HBP, 5 SF)

| Hits | AVG | OBP |
|---|---|---|
{hit_rows}
Each 5 hits in 500 at-bats moves the average by 10 points (.010), which is why a .290 and a .300 season differ by only one hit every two weeks.

## How walks change OBP (150 H in 500 AB)

| Walks | AVG | OBP |
|---|---|---|
{walk_rows}
Walks leave batting average untouched but lift OBP, which is why patient hitters are often more valuable than their average suggests.''')],
     body_add=f'''
## Chasing .300 late in the season

A hitter with 140 hits in 480 at-bats is at {r3(140/480)}. To finish at .300 in 500 at-bats he needs 150 hits, so {need:.0f} hits in his last 20 at-bats. Working backwards like this is easier than adding hits by trial: target hits = target average × final at-bats.

## Practical notes

- **Take totals from the official line.** Box scores list AB, H, BB, HBP and SF separately; plate appearances also include sacrifice bunts and catcher's interference, which neither formula uses.
- **Sacrifice flies count only in OBP.** They are left out of at-bats, so they do not hurt batting average, but they are in the OBP denominator.
- **Small samples swing wildly.** In 20 at-bats one hit moves the average by 50 points; wait for a few hundred at-bats before judging a hitter.
- **Qualifying for titles.** Major League Baseball batting titles need 3.1 plate appearances per team game, about 502 in a 162 game season.

## Common mistakes

- **Counting walks as at-bats.** That lowers the average; walks, HBP and sacrifices are not at-bats.
- **Forgetting HBP in OBP.** Being hit by a pitch is a time on base and belongs in both the top and bottom of the formula.
- **Writing OBP as a percentage.** .377 is a rate of 0.377; it is spoken as "three seventy seven", not 37.7 points.
- **Comparing across eras without context.** A .270 average in a low scoring season can be better than .290 in a high scoring one.
- **Rounding before dividing.** Divide the raw totals and round only the final result to three decimals.
''',
     faq_replace=[('What is OBP?', 'What is OBP?',
                   'On-base percentage is how often a batter reaches base by a hit, walk or hit by pitch, divided by at-bats plus walks, HBP and sacrifice flies. Reaching on an error or a fielder\'s choice does not count.')],
     faq_add=[('Do sacrifice bunts count in OBP?',
               'No. Sacrifice bunts are left out of both at-bats and the OBP denominator, while sacrifice flies are left out of at-bats but are included in the OBP denominator.')])

# ---------------------------------------------------------------- Food cost
tc, n, fc = 36, 12, 0.30
cps = tc / n
price = cps / fc
gp = price - cps
assert cps == 3 and abs(price - 10) < 1e-9 and abs(gp - 7) < 1e-9
mult = 1 / fc
mark = (price - cps) / cps
batch_rows = ''
for nn in (8, 10, 12, 15, 18):
    c_ = tc / nn
    batch_rows += f"| {nn} | {m2(c_)} | {m2(c_/fc)} | {m2(c_/fc - c_)} |\n"
lost = tc / 11
lost_price = lost / fc
market = 9.0
fc_market = cps / market
wrong = cps * 1.30

edit('food/food-cost', date=U, phrase='food cost calculator',
     title='Food Cost Calculator: Cost per Serving and Menu Price',
     description='Food cost calculator for restaurants: enter recipe cost, servings and target food cost % to get the cost per serving, menu price and gross profit per plate.',
     intro=("Food cost percentage is the share of a dish's selling price that goes on ingredients. "
            "This food cost calculator divides the recipe cost by the servings it makes, then sets the menu price that hits your target percentage and shows the gross profit per plate.\n\n"
            "Chefs, restaurant owners, caterers and home bakers selling at markets use it to price new dishes, check old prices after supplier increases and keep margins steady."),
     replace=[('''## Example

Ingredients cost 36 for 12 servings, target 30%:

- Cost per serving = **3.00**
- Menu price = 3.00 ÷ 0.30 = **10.00**
- Gross profit = **7.00** per plate''',
               f'''## Worked example with the default values

A tray of lasagne costs {m2(tc)} in ingredients and is cut into {n} portions. The target food cost is {fc*100:.0f}%:

1. Cost per serving = {m2(tc)} ÷ {n} = **{m2(cps)}**
2. Menu price = {m2(cps)} ÷ {fc:.2f} = **{m2(price)}**
3. Gross profit = {m2(price)} - {m2(cps)} = **{m2(gp)}** per plate

Dividing by a {fc*100:.0f}% food cost is the same as multiplying the plate cost by {mult:.2f}. Expressed as a markup on cost, that is {mark*100:.0f}%.

## Batch size and price (recipe cost {m2(tc)}, 30% target)

| Servings | Cost per serving | Menu price | Gross profit |
|---|---|---|---|
{batch_rows}
Portion size is a pricing decision: cutting the same tray into 15 instead of 12 lowers the price you need by {m2(price - tc/15/fc)}.''')],
     body_add=f'''
## Checking an existing price

The formula also works backwards. If the local market will only pay {m2(market)} for the dish, the food cost becomes {m2(cps)} ÷ {m2(market)} = {fc_market*100:.1f}%. Decide whether that is acceptable, cut the plate cost, or change the portion.

## Practical notes

- **Allow for waste.** If one portion out of 12 is lost to trimming, tasting or a dropped plate, the real cost per serving is {m2(tc)} ÷ 11 = {m2(lost)}, and the 30% price rises to {m2(lost_price)}.
- **Use edible portion cost.** Price meat, fish and vegetables at their yield after trimming and cooking, not their bought weight.
- **Recost regularly.** Re-enter the recipe cost whenever a main ingredient changes price; a 10% rise in a key item can push a dish several points over target.
- **Price sides and sauces too.** A dish that includes bread, dips or a side salad must carry their cost as well.

## Common mistakes

- **Confusing food cost with markup.** Adding 30% to the plate cost gives {m2(wrong)}, not {m2(price)}; a 30% food cost means dividing by 0.30.
- **Using the recipe cost as the serving cost.** Always divide by the number of portions first.
- **Including tax in the menu price.** Compare food cost with the price before sales tax or VAT.
- **Forgetting labour and overheads.** A healthy food cost does not guarantee profit if prep is slow or rent is high.
- **Setting one target for every item.** Drinks and desserts usually run lower food costs than steaks, so judge the menu as a whole.
''',
     faq_replace=[('What is food cost percentage?', 'What is food cost percentage?',
                   'Ingredient cost per serving divided by the selling price, times 100. Many restaurants aim for roughly 25 to 35%, depending on the style of service.'),
                  ('What is a good food cost percentage?', 'What is a good food cost percentage?',
                   'Most full service restaurants aim for about 28 to 35%, quick service for 25 to 30%, and pizza and drinks can run lower. Your own rent and labour costs decide what works.')],
     faq_add=[('What is the difference between food cost percentage and markup?',
               f'Food cost percentage is cost divided by price; markup is profit divided by cost. A {m2(cps)} plate sold at {m2(price)} has a {fc*100:.0f}% food cost and a {mark*100:.0f}% markup.')])

# Related links on ecology/carbon-offset-cost were changed by hand (sed) after this script ran:
# water-leak and finance/stock-average replaced with ecology/electricity-co2 (closer topic).
