import math
from page import page
C='food'; U='updated: 2026-10-27'

page(C,'recipe-scaler',f'''
title: Recipe Scaler (Servings Converter)
description: Scale any recipe ingredient up or down for a different number of servings.
category: food
keywords: [recipe scaler, recipe converter, servings calculator, double a recipe, halve a recipe, adjust recipe]
{U}
featured: true
variables:
  - {{ id: s0, label: Original servings, default: 4, min: 0.01 }}
  - {{ id: s1, label: New servings, default: 10, min: 0 }}
  - {{ id: q0, label: Ingredient amount in the original recipe, default: 250, min: 0 }}
  - {{ id: k, label: Scaling factor, min: 0, decimals: 3 }}
  - {{ id: q1, label: New ingredient amount (same unit), min: 0 }}
equations:
  - k = s1 / s0
  - q1 = q0 * k
faq:
  - q: How do I scale a recipe?
    a: Divide the new number of servings by the original to get a scaling factor, then multiply every ingredient by it.
  - q: Do baking times change when I scale a recipe?
    a: Often. A larger cake in a deeper pan bakes longer; smaller portions bake faster. Check doneness early.
  - q: Should spices and salt be scaled exactly?
    a: When scaling up a lot, start with about 75% of the scaled amount of strong spices and salt, then adjust to taste.
related: [food/cooking-converter, food/grams-to-cups, food/cake-pan]
''','''
## How to use this calculator

Enter the **original** and **new** number of servings, then type each **ingredient amount** in turn. The scaling factor and new amount are calculated — the unit stays the same as you entered it.

## Formula

<p class="formula">new amount = original amount × (new servings ÷ original servings)</p>

## Example

A recipe for 4 uses 250 g of pasta. For 10 people: factor 2.5 → **625 g**.

## Tips

- Eggs: round to whole eggs, or beat an egg and use part of it.
- Pans: a scaled recipe may need a bigger pan — see the [cake pan converter](/food/cake-pan/).
- Liquids reduce more slowly in larger pots, so simmer a little longer.
''')

page(C,'cooking-converter',f'''
title: Cooking Measurement Converter (Cups, Tbsp, ml)
description: Convert kitchen volume measurements — cups, tablespoons, teaspoons, fluid ounces and millilitres.
category: food
keywords: [cups to ml, tablespoon to ml, teaspoon to ml, cooking converter, kitchen conversion, fl oz to ml]
{U}
featured: true
variables:
  - {{ id: v0, label: US cups, family: volume, unit: cup, default: 1, min: 0 }}
  - {{ id: v1, label: Millilitres, family: volume, unit: mL, min: 0 }}
  - {{ id: v2, label: Tablespoons, family: volume, unit: tbsp, min: 0 }}
  - {{ id: v3, label: Teaspoons, family: volume, unit: tsp, min: 0 }}
  - {{ id: v4, label: US fluid ounces, family: volume, unit: floz, min: 0 }}
  - {{ id: v5, label: Metric cups (250 ml), family: volume, unit: cupM, min: 0 }}
equations:
  - v0 = v1
  - v1 = v2
  - v2 = v3
  - v3 = v4
  - v4 = v5
faq:
  - q: How many ml is a cup?
    a: A US cup is 236.6 ml. A metric cup (Australia, NZ, Canada, often India) is 250 ml.
  - q: How many tablespoons are in a cup?
    a: 16 US tablespoons. A tablespoon is 3 teaspoons (about 14.8 ml).
  - q: Is an Australian tablespoon different?
    a: Yes — it is 20 ml (4 teaspoons), compared with about 15 ml elsewhere.
related: [food/grams-to-cups, food/recipe-scaler, conversion/volume-converter]
''','''
## How to use this converter

Type a value into **any** field — cups, ml, tablespoons, teaspoons, fluid ounces or metric cups. The others update instantly.

## Quick reference (US measures)

| Measure | ml |
|---|---|
| 1 teaspoon | 4.93 |
| 1 tablespoon | 14.79 |
| 1 fl oz | 29.57 |
| ¼ cup | 59.15 |
| ½ cup | 118.29 |
| 1 cup | 236.59 |

## Equivalents

1 cup = 16 tbsp = 48 tsp = 8 fl oz

For dry ingredients by weight, use the [grams to cups converter](/food/grams-to-cups/) — a cup of flour and a cup of sugar weigh very different amounts.
''')

D={'Flour (all-purpose)':120,'Sugar (granulated)':200,'Brown sugar (packed)':220,'Butter':227,'Rice (uncooked)':185,'Rolled oats':90,'Cocoa powder':85,'Honey':340,'Milk':245,'Water':240}
opts="\n".join(f"      - {{ label: {k} ({v} g per cup), value: {v} }}" for k,v in D.items())
page(C,'grams-to-cups',f'''
title: Grams to Cups Converter (Baking)
description: Convert grams to US cups and cups to grams for flour, sugar, butter, rice, oats and other common ingredients.
category: food
keywords: [grams to cups, cups to grams, flour grams to cups, sugar cups to grams, baking conversion, butter grams]
{U}
featured: true
variables:
  - id: d
    label: Ingredient
    default: 120
    options:
{opts}
  - {{ id: g, label: Grams, default: 250, min: 0 }}
  - {{ id: c, label: US cups, min: 0, decimals: 3 }}
  - {{ id: tb, label: Tablespoons, min: 0, decimals: 1 }}
equations:
  - c = g / d
  - tb = c * 16
faq:
  - q: How many grams is a cup of flour?
    a: About 120–125 g for spooned and levelled all-purpose flour. Scooping straight from the bag packs it to 140 g or more.
  - q: Why weigh instead of using cups?
    a: Weight is far more accurate. The same cup of flour can vary by 20% depending on how it is filled.
  - q: How much is a stick of butter?
    a: One US stick is ½ cup, 8 tablespoons or about 113 g.
related: [food/cooking-converter, food/butter-converter, food/recipe-scaler]
''','''
## How to use this converter

Choose the **ingredient**, then enter **grams** or **cups**. The other value and the equivalent in tablespoons are calculated.

## Grams per US cup

| Ingredient | Grams per cup |
|---|---|
''' + "\n".join(f"| {k} | {v} |" for k,v in D.items()) + '''

Values are typical averages; brands and how you fill the cup vary. For best baking results, use a kitchen scale.
''')

page(C,'butter-converter',f'''
title: Butter Converter (Sticks, Grams, Cups, Tbsp)
description: Convert butter between US sticks, grams, cups, tablespoons and ounces.
category: food
keywords: [butter converter, stick of butter in grams, butter cups to grams, tablespoons of butter, butter conversion]
{U}
variables:
  - {{ id: st, label: US sticks, default: 1, min: 0 }}
  - {{ id: g, label: Grams, min: 0, decimals: 1 }}
  - {{ id: cup, label: Cups, min: 0, decimals: 3 }}
  - {{ id: tb, label: Tablespoons, min: 0, decimals: 1 }}
  - {{ id: oz, label: Ounces (weight), min: 0, decimals: 2 }}
equations:
  - g = st * 113.4
  - cup = st / 2
  - tb = st * 8
  - oz = g / 28.3495
faq:
  - q: How many grams is a stick of butter?
    a: One US stick is 4 oz, which is 113.4 g (often rounded to 113 or 115 g).
  - q: How much butter is in a cup?
    a: One cup is 2 sticks or about 227 g.
  - q: What about European butter blocks?
    a: They are usually 250 g — about 2.2 US sticks.
related: [food/grams-to-cups, food/cooking-converter]
''','''
## How to use this converter

Type an amount in **any** field — sticks, grams, cups, tablespoons or ounces.

## Butter equivalents

| Sticks | Grams | Cups | Tbsp |
|---|---|---|---|
| ½ | 57 | ¼ | 4 |
| 1 | 113 | ½ | 8 |
| 2 | 227 | 1 | 16 |
| 4 | 454 | 2 | 32 |

A 250 g block equals about 2.2 sticks or 1.1 cups.
''')

page(C,'oven-temperature',f'''
title: Oven Temperature Converter (°C, °F, Gas Mark)
description: Convert oven temperatures between Celsius, Fahrenheit, gas mark and fan-oven settings.
category: food
keywords: [oven temperature converter, celsius to fahrenheit oven, gas mark, fan oven, 180c in f, baking temperature]
{U}
variables:
  - {{ id: c, label: Conventional oven, family: temperature, unit: C, default: 180 }}
  - {{ id: f, label: Fahrenheit, family: temperature, unit: F }}
  - {{ id: fan, label: Fan / convection oven, family: temperature, unit: C }}
  - {{ id: gm, label: Gas mark (approx.), decimals: 1 }}
equations:
  - c = f
  - fan = c - 20
  - gm = ((c - 273.15) * 9 / 5 + 32 - 250) / 25
faq:
  - q: What is 180 °C in Fahrenheit?
    a: 356 °F — recipes usually round it to 350 °F (gas mark 4).
  - q: How do I adjust for a fan oven?
    a: Reduce the temperature by about 20 °C (25 °F) and check food a little earlier.
  - q: What gas mark is 200 °C?
    a: About gas mark 6.
related: [conversion/temperature-converter, food/turkey-cooking-time]
''','''
## How to use this converter

Enter a temperature in **°C** or **°F**. The fan-oven equivalent and approximate gas mark are calculated.

## Oven temperature chart

| Description | °C | °F | Gas | Fan °C |
|---|---|---|---|---|
| Very low | 120 | 250 | ½ | 100 |
| Low | 150 | 300 | 2 | 130 |
| Moderate | 180 | 350 | 4 | 160 |
| Moderately hot | 200 | 400 | 6 | 180 |
| Hot | 220 | 425 | 7 | 200 |
| Very hot | 240 | 475 | 9 | 220 |

Ovens vary — an oven thermometer shows the real temperature.
''')

page(C,'turkey-cooking-time',f'''
title: Turkey & Roast Cooking Time Calculator
description: Estimate roasting time for turkey, chicken, beef, pork and lamb from weight — plus resting time.
category: food
keywords: [turkey cooking time, roast chicken time, how long to cook turkey, roasting time per kg, roast beef time]
{U}
featured: true
variables:
  - id: rate
    label: Meat (oven ~180 °C / 350 °F)
    default: 40
    options:
      - {{ label: Turkey, unstuffed (~40 min per kg), value: 40 }}
      - {{ label: Turkey, stuffed (~44 min per kg), value: 44 }}
      - {{ label: Whole chicken (~50 min per kg), value: 50 }}
      - {{ label: Beef, medium (~45 min per kg), value: 45 }}
      - {{ label: Pork (~65 min per kg), value: 65 }}
      - {{ label: Lamb leg, medium (~55 min per kg), value: 55 }}
  - {{ id: m, label: Weight, family: mass, unit: kg, imperialUnit: lb, default: 6, min: 0 }}
  - {{ id: t, label: Approximate cooking time, family: time, unit: h, min: 0 }}
  - {{ id: rest, label: Resting time, suffix: minutes, min: 0, decimals: 0 }}
equations:
  - t = m * rate / 60 / 8766
  - rest = 15 + m * 3
faq:
  - q: How long does a turkey take to cook?
    a: As a guide, about 40 minutes per kg (18–20 min per lb) at 180 °C for an unstuffed bird. Always check the internal temperature.
  - q: What temperature should cooked poultry reach?
    a: 74 °C (165 °F) in the thickest part of the thigh and the stuffing.
  - q: Why rest the meat?
    a: Juices redistribute and the temperature evens out, so the meat is juicier and easier to carve.
related: [food/turkey-thawing, food/oven-temperature, food/meat-per-person]
''','''
## How to use this calculator

Choose the **meat**, then enter its **weight**. The approximate cooking time and suggested resting time are calculated.

## Example

A 6 kg unstuffed turkey: 6 × 40 = 240 minutes = **4 hours**, then rest about 30 minutes.

## Safe internal temperatures

| Meat | Minimum internal temperature |
|---|---|
| Poultry | 74 °C (165 °F) |
| Pork | 63 °C (145 °F) + 3 min rest |
| Beef/lamb steaks and roasts | 63 °C (145 °F) + 3 min rest |
| Minced meat | 71 °C (160 °F) |

Source: US FoodSafety.gov. Times are estimates — ovens, shapes and starting temperatures vary, so use a meat thermometer.
''')

page(C,'turkey-thawing',f'''
title: Turkey Thawing Time Calculator
description: Calculate how long to thaw a frozen turkey in the fridge or in cold water based on its weight.
category: food
keywords: [turkey thawing time, how long to thaw turkey, defrost turkey, thaw in fridge, cold water thawing]
{U}
variables:
  - {{ id: m, label: Turkey weight, family: mass, unit: kg, imperialUnit: lb, default: 7, min: 0 }}
  - {{ id: fr, label: In the fridge, family: time, unit: d, min: 0 }}
  - {{ id: cw, label: In cold water, family: time, unit: h, min: 0 }}
equations:
  - fr = m / 0.45359237 / 4 / 365.25
  - cw = m / 0.45359237 * 0.5 / 8766
faq:
  - q: How long does a turkey take to thaw in the fridge?
    a: About 24 hours for every 4–5 lb (1.8–2.3 kg).
  - q: How long in cold water?
    a: About 30 minutes per lb (about 1 hour per kg). Change the water every 30 minutes and cook immediately after.
  - q: Can I thaw a turkey on the counter?
    a: No. The outside can reach unsafe temperatures while the inside is still frozen.
related: [food/turkey-cooking-time]
''','''
## How to use this calculator

Enter the turkey's **weight**. Thawing times for the fridge and for cold water are calculated.

## Rules used (US Department of Agriculture guidance)

- **Fridge (4 °C / 40 °F or below):** about 24 hours per 4 lb (1.8 kg).
- **Cold water:** about 30 minutes per lb, in a leak-proof bag, changing the water every 30 minutes.

## Example

A 7 kg (15.4 lb) turkey needs about **3.9 days** in the fridge or about **7.7 hours** in cold water.
''')

page(C,'pizza-size',f'''
title: Pizza Size & Value Calculator
description: Compare two pizzas by area and price per square inch to see which one is the better deal.
category: food
keywords: [pizza size calculator, pizza area, which pizza is better value, price per square inch, two medium vs one large]
{U}
variables:
  - {{ id: d1, label: Pizza A diameter, family: length, unit: in, default: 12, min: 0 }}
  - {{ id: p1, label: Pizza A price, family: currency, default: 12, min: 0, decimals: 2 }}
  - {{ id: d2, label: Pizza B diameter, family: length, unit: in, default: 16, min: 0 }}
  - {{ id: p2, label: Pizza B price, family: currency, default: 18, min: 0, decimals: 2 }}
  - {{ id: a1, label: Pizza A area, family: area, unit: in2, min: 0 }}
  - {{ id: a2, label: Pizza B area, family: area, unit: in2, min: 0 }}
  - {{ id: more, label: B has more pizza than A by, family: percent, unit: '%' }}
  - {{ id: v, label: B is cheaper per area by, family: percent, unit: '%' }}
equations:
  - a1 = pi * (d1 / 2)^2
  - a2 = pi * (d2 / 2)^2
  - more = a2 / a1 - 1
  - v = 1 - (p2 / a2) / (p1 / a1)
faq:
  - q: Is one large pizza better than two mediums?
    a: Often yes. One 18-inch pizza (254 in²) has more than two 12-inch pizzas (226 in² together).
  - q: Why does a small increase in size matter so much?
    a: Area grows with the square of the diameter — a 16-inch pizza is 78% bigger than a 12-inch.
  - q: Is crust included?
    a: Yes, the calculation uses the full diameter.
related: [math/circle, everyday-life/unit-price]
''',f'''
## How to use this calculator

Enter the **diameter** and **price** of two pizzas. Their areas are calculated, plus how much more pizza B gives and how much cheaper it is per square inch.

## Example

12-inch for 12 vs 16-inch for 18:

- Areas: **{math.pi*36:.0f} in²** vs **{math.pi*64:.0f} in²** — B is **{(64/36-1)*100:.0f}%** bigger
- B is **{(1-(18/(math.pi*64))/(12/(math.pi*36)))*100:.1f}%** cheaper per square inch
''')

page(C,'cake-pan',f'''
title: Cake Pan Size Converter
description: Scale a recipe for a different round or square cake tin by comparing pan areas.
category: food
keywords: [cake pan converter, baking tin size, round to square pan, scale cake recipe, pan size calculator]
{U}
variables:
  - id: s1
    label: Original pan shape
    default: 0.785398
    options:
      - {{ label: Round, value: 0.785398 }}
      - {{ label: Square, value: 1 }}
  - {{ id: d1, label: Original pan size (diameter or side), family: length, unit: cm, imperialUnit: in, default: 20, min: 0 }}
  - id: s2
    label: New pan shape
    default: 0.785398
    options:
      - {{ label: Round, value: 0.785398 }}
      - {{ label: Square, value: 1 }}
  - {{ id: d2, label: New pan size (diameter or side), family: length, unit: cm, imperialUnit: in, default: 25, min: 0 }}
  - {{ id: k, label: Multiply ingredients by, min: 0, decimals: 2 }}
equations:
  - k = s2 * d2^2 / (s1 * d1^2)
faq:
  - q: How do I convert a recipe to a bigger cake tin?
    a: Compare the pan areas. A 25 cm round tin is about 1.56 times the area of a 20 cm one, so multiply ingredients by 1.56.
  - q: Can I swap a round pan for a square one?
    a: Yes. A 20 cm square pan holds about 27% more than a 20 cm round pan.
  - q: Do baking times change?
    a: Usually — check a few minutes early and use a skewer test.
related: [food/recipe-scaler, math/circle]
''','''
## How to use this calculator

Choose the **shape** and **size** of the original and new tins. The factor to multiply all ingredients by is calculated (assuming the same depth).

## Example

20 cm round → 25 cm round: factor = 25² ÷ 20² = **1.56**

## Equivalent tins (similar area)

| Round | Square |
|---|---|
| 20 cm (8 in) | 18 cm (7 in) |
| 23 cm (9 in) | 20 cm (8 in) |
| 25 cm (10 in) | 23 cm (9 in) |
''')

page(C,'coffee-ratio',f'''
title: Coffee Ratio Calculator (Coffee to Water)
description: Find the right amount of coffee and water for any brew ratio — pour-over, French press, drip or cold brew.
category: food
keywords: [coffee ratio, coffee to water ratio, how much coffee, 1:16 ratio, french press ratio, pour over]
{U}
variables:
  - id: r
    label: Brew method / ratio
    default: 16
    options:
      - {{ label: Pour-over (1:16), value: 16 }}
      - {{ label: Drip machine (1:17), value: 17 }}
      - {{ label: French press (1:15), value: 15 }}
      - {{ label: AeroPress (1:12), value: 12 }}
      - {{ label: Cold brew concentrate (1:8), value: 8 }}
      - {{ label: Espresso (1:2), value: 2 }}
  - {{ id: w, label: Water, family: volume, unit: mL, default: 500, min: 0 }}
  - {{ id: c, label: Ground coffee, family: mass, unit: g, min: 0 }}
equations:
  - c = w * 1000 / r
faq:
  - q: What is the golden coffee ratio?
    a: About 1:15 to 1:18 (coffee to water by weight). 1:16 is a popular starting point.
  - q: How many grams of coffee per cup?
    a: For a 250 ml mug at 1:16, about 15–16 g (roughly 2–3 tablespoons).
  - q: Should I measure by weight?
    a: Yes — scoops vary with grind size and roast.
related: [food/cooking-converter]
''','''
## How to use this calculator

Choose a **brew method** and enter the **water** amount. The grams of ground coffee are calculated. Or enter the coffee you have to find how much water to use.

## Example

500 ml of water at 1:16 → **31 g** of coffee.

1 ml of water weighs about 1 g, so ratios work with either.
''')

page(C,'rice-water',f'''
title: Rice to Water Ratio Calculator
description: Find how much water to use for white, basmati, jasmine, brown rice and more — by cups or grams.
category: food
keywords: [rice water ratio, how much water for rice, basmati rice water, brown rice water, cooking rice]
{U}
variables:
  - id: r
    label: Rice type (water per cup of rice)
    default: 1.5
    options:
      - {{ label: Basmati (1.5 cups water), value: 1.5 }}
      - {{ label: Jasmine (1.25 cups water), value: 1.25 }}
      - {{ label: Long-grain white (2 cups water), value: 2 }}
      - {{ label: Short-grain / sushi (1.2 cups water), value: 1.2 }}
      - {{ label: Brown rice (2.25 cups water), value: 2.25 }}
      - {{ label: Wild rice (3 cups water), value: 3 }}
  - {{ id: rc, label: Rice, family: volume, unit: cup, default: 2, min: 0 }}
  - {{ id: wc, label: Water, family: volume, unit: cup, min: 0 }}
  - {{ id: serv, label: Servings (about ½ cup dry each), min: 0, decimals: 0 }}
equations:
  - wc = rc * r
  - serv = rc / 0.0001182941
faq:
  - q: How much water for 1 cup of rice?
    a: It depends on the variety — about 1.5 cups for basmati, 2 for long-grain white and 2.25 for brown rice (absorption method).
  - q: Should I rinse rice?
    a: Rinsing removes surface starch for fluffier grains. Soaked basmati may need a little less water.
  - q: How much rice per person?
    a: About ½ cup (around 90 g) uncooked rice for a main-course portion.
related: [food/recipe-scaler, food/cooking-converter]
''','''
## How to use this calculator

Choose the **rice type** and enter the amount of **rice**. The water needed and approximate servings are calculated. Switch units to ml or metric cups if you prefer.

## Example

2 cups of basmati → **3 cups of water**, about 4 servings.

Ratios are for the absorption method on a stovetop with a tight lid. Rice cookers and pressure cookers may need slightly less water.
''')

page(C,'food-cost',f'''
title: Food Cost & Menu Price Calculator
description: Calculate cost per serving and the menu price needed to hit a target food cost percentage.
category: food
keywords: [food cost calculator, menu pricing, food cost percentage, cost per serving, restaurant pricing, plate cost]
{U}
variables:
  - {{ id: tc, label: Total ingredient cost of the recipe, family: currency, default: 36, min: 0, decimals: 2 }}
  - {{ id: n, label: Servings the recipe makes, default: 12, min: 1 }}
  - {{ id: fc, label: Target food cost, family: percent, unit: '%', default: 30, min: 0.01, max: 1 }}
  - {{ id: cps, label: Cost per serving, family: currency, min: 0, decimals: 2 }}
  - {{ id: price, label: Menu price, family: currency, min: 0, decimals: 2 }}
  - {{ id: gp, label: Gross profit per serving, family: currency, decimals: 2 }}
equations:
  - cps = tc / n
  - price = cps / fc
  - gp = price - cps
faq:
  - q: What is food cost percentage?
    a: Ingredient cost divided by selling price. Many restaurants aim for about 25–35%.
  - q: How do I price a dish?
    a: Menu price = cost per serving ÷ target food cost %. A 3.00 plate cost at 30% gives a price of 10.00.
  - q: What else affects the price?
    a: Labour, rent, overheads and the local market. Food cost is only part of the picture.
related: [finance/profit-margin, food/recipe-scaler]
''','''
## How to use this calculator

Enter the **total ingredient cost**, how many **servings** it makes and your **target food cost %**. The cost per serving, menu price and gross profit are calculated.

## Example

Ingredients cost 36 for 12 servings, target 30%:

- Cost per serving = **3.00**
- Menu price = 3.00 ÷ 0.30 = **10.00**
- Gross profit = **7.00** per plate
''')

page(C,'brine',f'''
title: Brine Calculator (Salt Percentage)
description: Calculate how much salt (and sugar) to add for a brine of any strength — for meat, pickles and fermentation.
category: food
keywords: [brine calculator, salt percentage, wet brine, pickling brine, fermentation brine, equilibrium brine]
{U}
variables:
  - {{ id: w, label: Water, family: mass, unit: g, default: 1000, min: 0 }}
  - {{ id: p, label: Salt concentration, family: percent, unit: '%', default: 5, min: 0, max: 0.3 }}
  - {{ id: s, label: Salt to add, family: mass, unit: g, min: 0 }}
  - {{ id: sg, label: Sugar (optional, half the salt), family: mass, unit: g, min: 0 }}
equations:
  - s = w * p
  - sg = s / 2
faq:
  - q: What brine strength should I use?
    a: About 5–6% for brining poultry and pork, 2–3% for fermented vegetables like sauerkraut and pickles, and 8–10% for olives.
  - q: Does 1 litre of water weigh 1,000 g?
    a: Very nearly. Weighing water and salt gives the most accurate brine.
  - q: Which salt should I use?
    a: Non-iodised salt by weight. Different salts have very different crystal sizes, so volume measures vary a lot.
related: [chemistry/mass-percent, food/cooking-converter]
''','''
## How to use this calculator

Enter the **water** weight and the **salt percentage**. The salt to add is calculated, plus an optional sugar amount.

This calculator measures salt as a percentage of the water weight, which is common in cooking.

## Example

1 litre (1,000 g) of water at 5% → **50 g** of salt (and 25 g of sugar if wanted).

## Typical strengths

| Use | Salt |
|---|---|
| Fermented vegetables | 2–3% |
| Poultry and pork brine | 5–6% |
| Olives | 8–10% |
''')

page(C,'bakers-percentage',f'''
title: Baker's Percentage Calculator (Dough Hydration)
description: Calculate dough ingredients from flour weight and baker's percentages — water (hydration), salt, yeast and more.
category: food
keywords: [bakers percentage, dough hydration, bread calculator, pizza dough, flour water ratio, sourdough hydration]
{U}
variables:
  - {{ id: f, label: Flour, family: mass, unit: g, default: 500, min: 0 }}
  - {{ id: hp, label: Hydration (water), family: percent, unit: '%', default: 70, min: 0 }}
  - {{ id: sp, label: Salt, family: percent, unit: '%', default: 2, min: 0 }}
  - {{ id: yp, label: Instant yeast, family: percent, unit: '%', default: 1, min: 0 }}
  - {{ id: w, label: Water, family: mass, unit: g, min: 0 }}
  - {{ id: s, label: Salt, family: mass, unit: g, min: 0 }}
  - {{ id: y, label: Yeast, family: mass, unit: g, min: 0 }}
  - {{ id: tot, label: Total dough weight, family: mass, unit: g, min: 0 }}
equations:
  - w = f * hp
  - s = f * sp
  - y = f * yp
  - tot = f + w + s + y
faq:
  - q: What is baker's percentage?
    a: Each ingredient expressed as a percentage of the flour weight. Flour is always 100%.
  - q: What is dough hydration?
    a: Water ÷ flour. Sandwich bread is often 60–65%, ciabatta and focaccia 75–80%.
  - q: How much salt is typical?
    a: About 1.8–2.2% of the flour weight.
related: [food/yeast-converter, food/recipe-scaler]
''','''
## How to use this calculator

Enter the **flour** weight and the percentages for **water**, **salt** and **yeast**. Ingredient weights and the total dough weight are calculated.

## Example

500 g flour at 70% hydration, 2% salt, 1% instant yeast:

- Water **350 g**, salt **10 g**, yeast **5 g**
- Total dough **865 g**

## Typical hydration

| Bread | Hydration |
|---|---|
| Bagels | 55–58% |
| Sandwich loaf | 60–65% |
| Neapolitan pizza | 60–65% |
| Rustic sourdough | 70–80% |
| Ciabatta / focaccia | 75–85% |
''')

page(C,'yeast-converter',f'''
title: Yeast Converter (Instant, Active Dry, Fresh)
description: Convert between instant yeast, active dry yeast and fresh (cake) yeast amounts.
category: food
keywords: [yeast converter, instant yeast to active dry, fresh yeast conversion, cake yeast, dry yeast grams]
{U}
variables:
  - {{ id: inst, label: Instant yeast, family: mass, unit: g, default: 7, min: 0 }}
  - {{ id: act, label: Active dry yeast, family: mass, unit: g, min: 0 }}
  - {{ id: fresh, label: Fresh (cake) yeast, family: mass, unit: g, min: 0 }}
equations:
  - act = inst * 1.25
  - fresh = inst * 3
faq:
  - q: How do I convert instant yeast to active dry?
    a: Use about 25% more active dry yeast — 7 g instant ≈ 9 g active dry.
  - q: How much fresh yeast replaces dry yeast?
    a: About 3 times the weight of instant yeast (or 2.5 times active dry).
  - q: How much is one sachet?
    a: A standard sachet is 7 g (¼ oz, about 2¼ teaspoons).
related: [food/bakers-percentage, food/recipe-scaler]
''','''
## How to use this converter

Type an amount for **any** yeast type and the equivalent amounts of the others are calculated.

## Conversion ratios

<p class="formula">active dry ≈ 1.25 × instant   fresh ≈ 3 × instant</p>

## Example

One 7 g sachet of instant yeast ≈ **8.75 g** active dry ≈ **21 g** fresh yeast.

Active dry yeast is traditionally dissolved in warm water first; instant yeast can be mixed straight into the flour.
''')

page(C,'sugar-to-honey',f'''
title: Sugar to Honey Substitution Calculator
description: Replace sugar with honey or maple syrup in recipes — with the liquid reduction and oven adjustment.
category: food
keywords: [sugar to honey, honey substitute for sugar, replace sugar with honey, maple syrup substitution, baking with honey]
{U}
variables:
  - {{ id: s, label: Sugar in recipe, family: volume, unit: cup, default: 1, min: 0 }}
  - {{ id: h, label: Honey to use, family: volume, unit: cup, min: 0 }}
  - {{ id: lr, label: Reduce other liquids by, family: volume, unit: cup, min: 0 }}
  - {{ id: soda, label: Baking soda to add, suffix: tsp, min: 0, decimals: 2 }}
equations:
  - h = s * 0.75
  - lr = s * 0.25
  - soda = s / 0.0002365882365 * 0.25
faq:
  - q: How much honey replaces a cup of sugar?
    a: About ¾ cup of honey, because honey is sweeter. Reduce other liquids by about ¼ cup.
  - q: Why add baking soda?
    a: Honey is slightly acidic. About ¼ teaspoon of baking soda per cup of honey balances it in baked goods.
  - q: Do I need to change the oven temperature?
    a: Yes, lower it by about 15 °C (25 °F) — honey browns faster.
related: [food/grams-to-cups, food/recipe-scaler]
''','''
## How to use this calculator

Enter the amount of **sugar** in the recipe. The honey to use, the reduction in other liquids and the baking soda to add are calculated.

## Rules of thumb

- Use **¾ cup honey** per cup of sugar.
- **Reduce liquids** by ¼ cup per cup of honey used.
- Add **¼ tsp baking soda** per cup.
- **Lower the oven** by about 15 °C (25 °F).

Maple syrup works similarly, at roughly the same ¾ substitution.
''')

page(C,'calories-from-macros',f'''
title: Calories from Macros Calculator
description: Calculate total calories from grams of protein, carbohydrate, fat and alcohol — as shown on nutrition labels.
category: food
keywords: [calories from macros, calorie calculator, protein carbs fat calories, nutrition label, kcal from grams]
{U}
variables:
  - {{ id: p, label: Protein, suffix: g, default: 25, min: 0 }}
  - {{ id: c, label: Carbohydrate, suffix: g, default: 40, min: 0 }}
  - {{ id: f, label: Fat, suffix: g, default: 15, min: 0 }}
  - {{ id: a, label: Alcohol, suffix: g, default: 0, min: 0 }}
  - {{ id: kcal, label: Total calories, suffix: kcal, min: 0, decimals: 0 }}
  - {{ id: fpct, label: Calories from fat, family: percent, unit: '%', min: 0 }}
equations:
  - kcal = 4 * p + 4 * c + 9 * f + 7 * a
  - fpct = 9 * f / kcal
faq:
  - q: How many calories are in a gram of each macronutrient?
    a: Protein 4 kcal, carbohydrate 4 kcal, fat 9 kcal and alcohol 7 kcal (Atwater factors).
  - q: Why doesn't my label add up exactly?
    a: Labels round values, and fibre provides fewer calories than other carbohydrates.
  - q: How do I convert kcal to kJ?
    a: Multiply by 4.184.
related: [health/macros, health/bmr, conversion/energy-converter]
''','''
## How to use this calculator

Enter grams of **protein**, **carbohydrate**, **fat** and **alcohol**. Total calories and the share from fat are calculated.

## Formula

<p class="formula">kcal = 4P + 4C + 9F + 7A</p>

## Example

25 g protein, 40 g carbohydrate, 15 g fat:

- kcal = 100 + 160 + 135 = **395 kcal**
- Calories from fat = 135 ÷ 395 = **34%**
''')

page(C,'meat-per-person',f'''
title: Meat per Person Calculator (BBQ & Parties)
description: Calculate how much meat to buy for a barbecue or party based on the number of guests and appetite.
category: food
keywords: [meat per person, bbq calculator, how much meat for party, brisket per person, pulled pork per person]
{U}
variables:
  - {{ id: a, label: Adults, default: 12, min: 0 }}
  - {{ id: k, label: Children, default: 4, min: 0 }}
  - id: per
    label: Appetite / menu
    default: 0.25
    options:
      - {{ label: Several sides (about 200 g per adult), value: 0.2 }}
      - {{ label: Standard (about 250 g per adult), value: 0.25 }}
      - {{ label: Big eaters / meat-focused (about 340 g per adult), value: 0.34 }}
  - {{ id: y, label: Cooked yield of raw meat, family: percent, unit: '%', default: 60, min: 0.01, max: 1 }}
  - {{ id: ck, label: Cooked meat needed, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
  - {{ id: raw, label: Raw meat to buy, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - ck = (a + k / 2) * per
  - raw = ck / y
faq:
  - q: How much meat per person?
    a: About 200–250 g (½ lb) of cooked meat per adult with several sides, and about half that for children.
  - q: Why buy more raw meat?
    a: Meat loses weight when cooked. Brisket and pulled pork can lose 40–50%; boneless chicken about 25%.
  - q: Should I plan for leftovers?
    a: Many hosts add 10–20% extra.
related: [food/turkey-cooking-time, food/party-drinks]
''','''
## How to use this calculator

Enter the number of **adults** and **children**, choose the **appetite**, and set the **cooked yield** of your meat. The cooked meat needed and the raw meat to buy are calculated.

## Example

12 adults and 4 children at 250 g per adult, 60% yield (e.g. brisket):

- Cooked = 14 × 0.25 = **3.5 kg**
- Raw to buy = 3.5 ÷ 0.6 = **5.8 kg**

## Typical cooked yields

| Meat | Yield |
|---|---|
| Brisket | 50–60% |
| Pork shoulder | 50–60% |
| Bone-in chicken | 60–65% |
| Boneless chicken | 75% |
| Burgers | 75% |
''')

page(C,'liquid-weight',f'''
title: Liquid Volume to Weight Converter
description: Convert millilitres or cups of water, milk, oil, honey and other liquids to grams — and back.
category: food
keywords: [ml to grams, cups to grams liquid, oil ml to grams, honey weight, milk grams, liquid density]
{U}
variables:
  - id: rho
    label: Liquid (density)
    default: 1
    options:
      - {{ label: Water (1.00 g/ml), value: 1 }}
      - {{ label: Milk (1.03 g/ml), value: 1.03 }}
      - {{ label: Vegetable oil (0.92 g/ml), value: 0.92 }}
      - {{ label: Honey (1.42 g/ml), value: 1.42 }}
      - {{ label: Maple syrup (1.32 g/ml), value: 1.32 }}
      - {{ label: Cream, heavy (0.99 g/ml), value: 0.99 }}
  - {{ id: v, label: Volume, family: volume, unit: mL, default: 250, min: 0 }}
  - {{ id: m, label: Weight, family: mass, unit: g, min: 0 }}
equations:
  - m = v * rho * 1000
faq:
  - q: Is 1 ml of water 1 gram?
    a: Yes, very nearly at room temperature.
  - q: Why does honey weigh more than water?
    a: It is much denser — about 1.4 g per ml — because of its high sugar content.
  - q: How many grams is a cup of oil?
    a: About 218 g for a US cup (236.6 ml × 0.92 g/ml).
related: [food/grams-to-cups, food/cooking-converter, physics/density]
''','''
## How to use this converter

Choose the **liquid**, then enter the **volume** (ml, cups, tbsp…) or the **weight**. The other is calculated.

## Formula

<p class="formula">weight = volume × density</p>

## Examples

- 250 ml of water = **250 g**
- 250 ml of oil = **230 g**
- 250 ml of honey = **355 g**
''')

page(C,'party-drinks',f'''
title: Party Drinks Calculator
description: Estimate how many drinks, bottles and ice to buy for a party based on guests and hours.
category: food
keywords: [party drinks calculator, how many drinks per guest, wedding drinks, ice per person, beverage planner]
{U}
variables:
  - {{ id: g, label: Number of guests, default: 50, min: 0 }}
  - {{ id: h, label: Party length, suffix: hours, default: 4, min: 0 }}
  - {{ id: d, label: Total drinks, min: 0, decimals: 0 }}
  - {{ id: ice, label: Ice, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
  - {{ id: wat, label: Water (also offer), family: volume, unit: L, imperialUnit: galUS, min: 0 }}
equations:
  - d = ceil(g * (2 + (h - 1)))
  - ice = g * 0.7
  - wat = g * 0.5 / 1000
faq:
  - q: How many drinks per guest?
    a: A common rule is 2 drinks in the first hour and 1 per hour after that.
  - q: How much ice do I need?
    a: About 0.7 kg (1.5 lb) per guest for drinks, more in hot weather or if chilling bottles in ice.
  - q: How should I split drinks?
    a: It depends on your guests. Always offer plenty of water and non-alcoholic choices.
related: [food/meat-per-person, food/recipe-scaler]
''','''
## How to use this calculator

Enter the **number of guests** and the **length of the party**. Total drinks, ice and water are estimated.

## Rule used

<p class="formula">drinks = guests × (2 + 1 per extra hour)</p>

## Example

50 guests for 4 hours:

- Drinks = 50 × 5 = **250**
- Ice ≈ **35 kg**
- Water ≈ **25 L**

Plan non-alcoholic options and arrange safe transport home for guests.
''')
print('food ok')
