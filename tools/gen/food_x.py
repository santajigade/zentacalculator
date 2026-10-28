import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
pi = math.pi

expand('food/bakers-percentage', '''
## Common bread formulas

| Bread | Hydration | Salt | Yeast (instant) | Other |
|---|---|---|---|---|
| Sandwich loaf | 60–65% | 2% | 1–1.5% | 5–8% sugar, 5–10% butter |
| French baguette | 65–70% | 2% | 0.5–1% | — |
| Pizza (Neapolitan style) | 58–65% | 2.5–3% | 0.1–0.3% | — |
| Ciabatta | 75–85% | 2% | 0.5–1% | — |
| Sourdough | 70–80% | 2% | — | 15–25% levain |
| Bagels | 55–60% | 2% | 1% | Malt |

## Scaling with baker's percentages

To make 4 loaves of 900 g dough at 70% hydration, 2% salt and 1% yeast:

- Total percentage = 100 + 70 + 2 + 1 = 173%
- Flour = 3,600 g ÷ 1.73 = **2,081 g**
- Water = 1,457 g, salt = 42 g, yeast = 21 g

## Hydration and flour type

Whole-wheat and high-protein flours absorb more water, so the same dough feels stiffer. Add 5–10% more water when swapping in whole-wheat flour.

## Sourdough levain

When the formula includes a levain (starter), remember it contains flour and water. For precise hydration, add the levain's flour and water to the totals.

## Weighing matters

Baker's percentages work best by weight. A cup of flour can weigh 120–150 g depending on how it is scooped. See the [grams to cups converter](/food/grams-to-cups/) if a recipe uses cups.
''', [
 ('What is 70% hydration?', 'The water weighs 70% of the flour weight — 350 g of water for 500 g of flour.'),
 ('How much salt should bread have?', 'Usually 1.8–2.2% of the flour weight.'),
], before='## Typical hydration')

expand('food/brine', '''
## Salt for common brine strengths

| Strength | Salt per litre of water | Use |
|---|---|---|
''' + ''.join(f"| {p}% | {p*10:g} g | {u} |\n" for p, u in [(2, 'Lacto-fermented vegetables (light)'), (3, 'Sauerkraut, fermented pickles'), (5, 'Poultry and pork brining'), (6, 'Turkey, chicken (shorter time)'), (10, 'Quick brine, olives'), (20, 'Curing, preserving')]) + '''
## Brining times (5–6% brine)

| Food | Time |
|---|---|
| Chicken breasts or pork chops | 1–2 hours |
| Whole chicken | 4–12 hours |
| Turkey breast | 6–12 hours |
| Whole turkey | 12–24 hours |
| Shrimp | 15–30 minutes |

Over-brining makes meat too salty and spongy. Keep brining food in the fridge at 4 °C or below.

## Weight percentage vs salt in water

This calculator uses salt as a percentage of the water weight, which most recipes use. Some fermenting guides use percentage of the total (water + salt); the difference is small for weak brines.

## Measuring salt by volume

Salt crystals differ in size, so a tablespoon of table salt weighs about twice as much as a tablespoon of flaky kosher salt. Weigh salt for accurate brines.
''', [
 ('How much salt is in a 5% brine?', '50 g of salt per litre (1,000 g) of water.'),
 ('Can I reuse brine?', 'Not brine used for raw meat. Discard it after use for food safety.'),
], before='## Typical strengths')

expand('food/butter-converter', '''
## Butter conversion table

| Sticks | Grams | Cups | Tablespoons |
|---|---|---|---|
''' + ''.join(f"| {s:g} | {s*113.4:.0f} g | {s/2:g} | {s*8:g} |\n" for s in [0.25, 0.5, 1, 1.5, 2, 3, 4]) + '''
## Butter around the world

| Region | Common pack |
|---|---|
| United States | 1 lb box of 4 sticks (113 g each) |
| UK, Europe | 250 g block |
| Australia | 250 g block |
| India | 100 g and 500 g packs |

A 250 g block is about 2.2 US sticks.

## Substitutes

| Instead of 1 cup (227 g) butter | Use |
|---|---|
| Oil (in cakes and muffins) | about ¾ cup (180 mL) |
| Ghee or clarified butter | about 200 g (less water) |
| Margarine (at least 80% fat) | 1 cup |

Butter is about 80–82% fat and 16–18% water, so substitutes change texture.

## Salted vs unsalted

Salted butter has about 1.5–2% salt. If a recipe calls for unsalted, reduce added salt by about 1/4 teaspoon per stick when using salted butter.
''', [
 ('How many grams is one stick of butter?', 'About 113 g (4 oz).'),
 ('How many tablespoons are in a stick of butter?', '8 tablespoons.'),
])

expand('food/cake-pan', '''
## Pan areas

| Pan | Area |
|---|---|
''' + ''.join(f"| {n} | {a:.0f} cm² |\n" for n, a in [('15 cm round (6 in)', pi*7.5**2), ('20 cm round (8 in)', pi*10**2), ('23 cm round (9 in)', pi*11.5**2), ('25 cm round (10 in)', pi*12.5**2), ('20 cm square (8 in)', 400), ('23 cm square (9 in)', 529), ('23 × 33 cm (9 × 13 in)', 23*33), ('Loaf 23 × 13 cm', 23*13)]) + '''
## Baking time adjustments

- **Larger, shallower pan**: batter is thinner, so bake for less time — check 5–10 minutes early.
- **Smaller, deeper pan**: batter is thicker, so bake longer at the same or slightly lower temperature (about 10–15 °C lower) to avoid a dark crust.
- Test with a skewer in the centre: it should come out clean or with a few moist crumbs.

## Depth matters

The calculator compares areas, assuming the same batter depth. If your new pan is deeper, fill it to the same depth (usually half to two-thirds full) rather than filling it to the top.

## Eggs when scaling

When the multiplier gives a fraction of an egg, beat the eggs and weigh them: one large egg is about 50 g without the shell.
''', [
 ('How do I convert an 8-inch round recipe to a 9-inch round?', 'Multiply by (9 ÷ 8)² ≈ 1.27, so make about 27% more batter.'),
 ('Can I use a square pan instead of a round one?', 'Yes. An 8-inch square has about the same area as a 9-inch round.'),
])

expand('food/calories-from-macros', '''
## Energy per gram

| Nutrient | kcal per gram | kJ per gram |
|---|---|---|
| Carbohydrate | 4 | 17 |
| Protein | 4 | 17 |
| Fat | 9 | 37 |
| Alcohol | 7 | 29 |
| Fibre | about 2 | 8 |

These Atwater factors are the basis of most food labels.

## Reading a nutrition label

If a snack has 10 g protein, 30 g carbohydrate and 8 g fat per serving:

- Protein: 40 kcal
- Carbohydrate: 120 kcal
- Fat: 72 kcal
- **Total: 232 kcal**, with 31% of calories from fat

Labels may differ slightly because of rounding and fibre.

## Why labels and calculators differ

- Labels often round to the nearest 5 or 10 kcal.
- Fibre provides fewer calories than other carbohydrates.
- Some countries list total carbohydrate including fibre; others list available carbohydrate.

## Kilojoules

Australia, New Zealand and parts of Europe use kJ. Multiply kcal by 4.184 to convert: 232 kcal ≈ 971 kJ.
''', [
 ('How many calories are in a gram of fat?', '9 kcal.'),
 ('How many calories in 30 g of protein?', '120 kcal.'),
])

expand('food/coffee-ratio', '''
## Ratios by brew method

| Method | Typical ratio (coffee : water) | Grind |
|---|---|---|
| Espresso | 1 : 2 (by weight of drink) | Very fine |
| AeroPress | 1 : 12–16 | Fine to medium |
| Pour-over (V60, Chemex) | 1 : 15–17 | Medium-fine to medium |
| Drip machine | 1 : 16–18 | Medium |
| French press | 1 : 12–15 | Coarse |
| Cold brew (concentrate) | 1 : 4–8 | Coarse |

## Coffee for common amounts (1 : 16)

| Water | Coffee |
|---|---|
''' + ''.join(f"| {w} mL | {w/16:.1f} g |\n" for w in [200, 250, 350, 500, 750, 1000]) + '''
## Water temperature

Most brewing guides recommend 90–96 °C, just off the boil. Too hot extracts bitterness; too cool gives a sour, weak cup.

## Adjusting taste

| Taste | Try |
|---|---|
| Weak, watery | More coffee (lower ratio) |
| Too strong | More water |
| Sour | Finer grind or hotter water |
| Bitter | Coarser grind or shorter brew time |

## Scoops

A standard coffee scoop holds about 2 tablespoons, roughly 10 g of ground coffee. Weighing is more consistent.
''', [
 ('How much coffee for 1 litre?', 'About 60–65 g at a 1:16 ratio.'),
 ('What is the golden ratio for coffee?', 'Around 1:15 to 1:18 for filter coffee; 1:16 is a popular starting point.'),
])

expand('food/cooking-converter', '''
## US vs metric vs UK measures

| Measure | US | Metric (AU/NZ/Canada etc.) | UK (traditional) |
|---|---|---|---|
| Cup | 236.6 mL | 250 mL | 284 mL (½ imperial pint) |
| Tablespoon | 14.8 mL | 15 mL (20 mL in Australia) | 15 mL |
| Teaspoon | 4.9 mL | 5 mL | 5 mL |
| Pint | 473 mL | — | 568 mL |

Check where a recipe comes from before converting.

## Liquids vs dry ingredients

This converter handles **volume**. For dry ingredients like flour and sugar, a cup's weight depends on the ingredient — see the [grams to cups converter](/food/grams-to-cups/).

## Handy kitchen equivalents

- 3 teaspoons = 1 tablespoon
- 4 tablespoons = ¼ cup
- 16 tablespoons = 1 cup
- 2 cups = 1 US pint
- 4 cups = 1 US quart

## Measuring tips

- Use clear jugs for liquids and read at eye level.
- Use nested cups for dry ingredients and level them off with a knife.
- Spoon flour into the cup rather than scooping, or it packs and weighs more.
''', [
 ('How many mL in a cup?', '236.6 mL in a US cup; 250 mL in a metric cup.'),
 ('How many tablespoons in a cup?', '16 US tablespoons.'),
], before='## Equivalents')

expand('food/food-cost', '''
## Typical food cost percentages

| Business | Target food cost |
|---|---|
| Fine dining | 28–35% |
| Casual dining | 28–32% |
| Quick service / fast food | 25–30% |
| Pizza | 20–25% |
| Bar food and drinks | 18–24% (drinks often lower) |

## Menu prices for different food costs

Cost per serving 3.00:

| Target food cost | Menu price |
|---|---|
''' + ''.join(f"| {p}% | {3/(p/100):.2f} |\n" for p in [20, 25, 28, 30, 33, 35]) + '''
## Beyond food cost

Food cost does not include:

- **Labour** — often 25–35% of sales.
- **Rent, utilities, packaging and marketing**.
- **Waste and spoilage**, which raise the real food cost.

A common rule is that food plus labour (prime cost) should stay under about 60–65% of sales.

## Plate costing tips

- Cost **every** ingredient, including oil, garnish and sauces.
- Use the **yield** after trimming and cooking, not the raw weight.
- Update costs when supplier prices change.
- Round menu prices to psychologically comfortable figures.
''', [
 ('What is a good food cost percentage?', 'Most restaurants aim for 28–35%, depending on the type of restaurant.'),
 ('How do I calculate menu price from food cost?', 'Menu price = cost per serving ÷ target food cost. A 3.00 cost at 30% gives a price of 10.00.'),
])

expand('food/grams-to-cups', '''
## Ingredient weights per US cup

| Ingredient | Grams per cup |
|---|---|
| All-purpose flour (spooned and levelled) | 120–125 |
| Bread flour | 127–130 |
| Whole-wheat flour | 120 |
| Granulated sugar | 200 |
| Brown sugar (packed) | 200–220 |
| Icing / powdered sugar | 120 |
| Butter | 227 |
| Rolled oats | 80–90 |
| Uncooked rice | 185–200 |
| Cocoa powder | 85–100 |
| Honey | 340 |
| Water / milk | 236–245 |

Values vary with brand and how you fill the cup.

## Why weighing is better

A cup of flour scooped straight from the bag can weigh 150 g or more, while spooned and levelled it may weigh 120 g. That 25% difference can turn a cake dense. Most professional recipes use grams.

## Tablespoons and teaspoons

| Ingredient | 1 tbsp | 1 tsp |
|---|---|---|
| Flour | 8 g | 2.6 g |
| Sugar | 12.5 g | 4.2 g |
| Salt (table) | 18 g | 6 g |
| Baking powder | 12–14 g | 4–4.6 g |

## Metric cups

A metric cup (250 mL) holds about 6% more than a US cup. Multiply US cup weights by 1.06 for metric cups.
''', [
 ('How many grams is 1 cup of flour?', 'About 120–125 g for all-purpose flour, spooned and levelled.'),
 ('How many grams is 1 cup of sugar?', 'About 200 g of granulated sugar.'),
], before='## Grams per US cup')

expand('food/liquid-weight', '''
## Density of kitchen liquids

| Liquid | Density (g/mL) | 1 cup (237 mL) weighs |
|---|---|---|
''' + ''.join(f"| {n} | {r} | {237*r:.0f} g |\n" for n, r in [('Water', 1.00), ('Milk (whole)', 1.03), ('Cream (heavy)', 0.99), ('Vegetable oil', 0.92), ('Olive oil', 0.91), ('Honey', 1.42), ('Maple syrup', 1.32), ('Golden syrup / treacle', 1.40), ('Vinegar', 1.01), ('Soy sauce', 1.15)]) + '''
## Oil weighs less than water

Because oil is less dense, 1 litre of oil weighs only about 920 g. When a recipe gives oil in grams, measuring by volume as if it were water adds about 8% too much.

## Sticky liquids

Honey and syrups are heavy and cling to cups. Weigh them directly into the bowl on a scale, or oil the measuring cup first so they slide out.

## Temperature

Density changes slightly with temperature. For cooking, the differences are too small to matter.
''', [
 ('How much does 1 litre of milk weigh?', 'About 1.03 kg.'),
 ('How much does a cup of honey weigh?', 'About 340 g.'),
])

expand('food/meat-per-person', '''
## Portion guide (cooked weight per adult)

| Situation | Per adult |
|---|---|
| Main course with sides | 150–180 g |
| Main course, hearty eaters | 200–250 g |
| Buffet with several mains | 100–150 g of each |
| Barbecue / grill party | 200–250 g |
| Canapés or appetisers | 50–75 g |

Children typically eat about half an adult portion.

## Raw weight to buy per adult (boneless)

| Meat | Cooked yield | Raw per 170 g cooked |
|---|---|---|
''' + ''.join(f"| {n} | {y}% | {170/(y/100):.0f} g |\n" for n, y in [('Chicken breast', 75), ('Beef steak', 70), ('Ground beef', 70), ('Pork shoulder (slow-cooked)', 60), ('Brisket', 55), ('Fish fillet', 80)]) + '''
## Bone-in cuts

For bone-in meat, buy more:

- **Bone-in chicken pieces**: about 300–350 g raw per person.
- **Whole chicken**: about 400–500 g raw per person.
- **Bone-in ribs**: 400–600 g raw per person.
- **Whole turkey**: about 0.5–0.7 kg raw per person — see the [turkey cooking time calculator](/food/turkey-cooking-time/).

## Leftovers

If you want leftovers, add 20–30% to the total.
''', [
 ('How much meat per person for a barbecue?', 'About 200–250 g cooked per adult, or 300–350 g raw boneless.'),
 ('How much chicken for 10 people?', 'About 2.3 kg raw boneless chicken for 170 g cooked each.'),
], before='## Typical cooked yields')

expand('food/oven-temperature', '''
## Air fryers

Air fryers cook faster than conventional ovens. A common conversion is to reduce the temperature by about 20 °C (25 °F) and the time by about 20%, checking food early.

## Altitude

At high altitude (above about 900 m / 3,000 ft), water boils at a lower temperature and batters rise faster. Bakers often raise the oven temperature by 10–15 °C and shorten baking time slightly.

## Checking your oven

Many ovens run 10–25 °C hotter or cooler than the dial. An inexpensive oven thermometer placed in the centre shows the real temperature so you can adjust.

## Doneness temperatures

| Food | Safe internal temperature |
|---|---|
| Poultry | 74 °C (165 °F) |
| Ground meat | 71 °C (160 °F) |
| Pork, beef, lamb steaks and roasts | 63 °C (145 °F) + 3 min rest |
| Fish | 63 °C (145 °F) |

These are US food-safety guidelines; use a probe thermometer to check.
''', [
 ('What is 180 °C in a fan oven?', 'About 160 °C.'),
 ('What gas mark is 200 °C?', 'About gas mark 6.'),
], before='## Oven temperature chart')

expand('food/party-drinks', '''
## Drinks by party size and length

| Guests | 2 hours | 3 hours | 4 hours | 5 hours |
|---|---|---|---|---|
''' + ''.join(f"| {g} | {g*3} | {g*4} | {g*5} | {g*6} |\n" for g in [10, 20, 30, 50, 100]) + '''
## Splitting by drink type

A common mix for adult parties:

| Drink | Share |
|---|---|
| Beer | 40% |
| Wine | 30% |
| Spirits / cocktails | 15% |
| Soft drinks | 15% |

Adjust for your guests — some events skew heavily to one type.

## Servings per container

| Container | Servings |
|---|---|
| Wine bottle (750 mL) | 5 glasses of 150 mL |
| Spirits bottle (750 mL) | about 16 shots of 45 mL |
| Beer keg (50 L) | about 88 pints |
| 2 L soft drink | 8 glasses of 250 mL |

## Ice

Plan about 0.5–1 kg of ice per guest, more in hot weather or if you are chilling drinks in tubs.

## Non-alcoholic options

Always offer water and appealing alcohol-free choices. Drivers and non-drinkers appreciate more than just soft drinks.
''', [
 ('How many drinks per guest per hour?', 'About 2 in the first hour and 1 per hour after that.'),
 ('How many bottles of wine for 50 guests?', 'If 30% of 250 drinks are wine, that is 75 glasses — about 15 bottles.'),
])

expand('food/pizza-size', '''
## Pizza area by size

| Diameter | Area | Equals how many 10-inch pizzas |
|---|---|---|
''' + ''.join(f"| {d} in ({d*2.54:.0f} cm) | {pi*(d/2)**2:.0f} in² | {(d/10)**2:.2f} |\n" for d in [8, 10, 12, 14, 16, 18]) + '''
## Why the big pizza is usually better value

Area grows with the square of the diameter. A 16-inch pizza has 78% more pizza than a 12-inch, but is rarely priced 78% higher.

## Slices per person

| Size | Slices | Feeds (approx.) |
|---|---|---|
| Small (10 in) | 6 | 1–2 |
| Medium (12 in) | 8 | 2–3 |
| Large (14 in) | 8–10 | 3–4 |
| Extra large (16–18 in) | 10–12 | 4–6 |

## Crust matters

A larger pizza has proportionally less crust, so more of the area is topped. For crust lovers, smaller pizzas give more crust per person.
''', [
 ('Is one 16-inch pizza more than two 12-inch pizzas?', 'No. One 16-inch pizza is about 201 in², while two 12-inch pizzas are about 226 in².'),
 ('How much bigger is a 14-inch than a 12-inch pizza?', 'About 36% more area.'),
])

expand('food/recipe-scaler', '''
## Ingredients that do not scale linearly

| Ingredient | Scaling tip |
|---|---|
| Salt and spices | Scale to about 75% when doubling, then taste and adjust |
| Baking powder / soda | Scale normally for small changes; for large batches, bake in several pans |
| Yeast | Large dough batches may need slightly less yeast |
| Liquids in braises | Less evaporation in a big pot, so reduce slightly |
| Cooking time | Depends on depth and pan size, not just quantity |

## Converting to a different unit while scaling

Scale first, then convert. For example, 250 g × 2.5 = 625 g, which is about 5 cups of flour (at 125 g per cup).

## Odd quantities

When the scaled amount is awkward, such as 1.6 eggs:

- Beat the eggs and measure by weight (a large egg is about 50 g).
- Round small spice amounts to the nearest ¼ teaspoon.
- For cans, round to the nearest whole can if the recipe is forgiving.

## Equipment

Doubling a cake recipe does not mean doubling the pan count automatically — check pan sizes with the [cake pan calculator](/food/cake-pan/). Make sure your pot or mixer can hold the larger volume.
''', [
 ('How do I halve a recipe?', 'Set the new servings to half the original. The scaling factor is 0.5; multiply every ingredient by it.'),
 ('Do cooking times change when scaling?', 'Often, yes. Larger quantities in deeper pans take longer; spread across more pans, times stay similar.'),
])

expand('food/rice-water', '''
## Water ratios by rice type (absorption method)

| Rice | Water per cup of rice | Cooking time |
|---|---|---|
| Long-grain white | 1.5–1.75 cups | 15–18 min |
| Basmati (rinsed, soaked) | 1.5 cups | 12–15 min |
| Jasmine | 1.25–1.5 cups | 12–15 min |
| Short-grain / sushi | 1.1–1.25 cups | 15 min + rest |
| Brown rice | 2–2.5 cups | 40–45 min |
| Wild rice | 3–4 cups | 45–55 min |
| Parboiled | 2–2.25 cups | 20 min |

## Cooked yield

1 cup of uncooked white rice makes about **3 cups** cooked. Brown rice makes about 3–3.5 cups.

## Rice cookers and pressure cookers

- **Rice cooker**: follow the marks inside the bowl; they assume the cooker's own cup (about 180 mL).
- **Pressure cooker (Indian style)**: 1 : 2 for white rice is common for softer rice; 1 : 1.25 for an electric pressure cooker.

## Rinsing and soaking

Rinsing removes surface starch for fluffier rice. Soaking basmati for 20–30 minutes helps long, separate grains and reduces the water needed slightly.

## Resting

Let rice stand covered for 5–10 minutes after cooking. Steam finishes the grains and makes them easier to fluff.
''', [
 ('How much water for 2 cups of rice?', 'About 3–3.5 cups for long-grain white rice using the absorption method.'),
 ('How much uncooked rice per person?', 'About ½ cup (90–100 g) uncooked for a main-course portion.'),
])

expand('food/sugar-to-honey', '''
## Other sugar substitutes

| Replace 1 cup sugar with | Amount | Reduce liquid by |
|---|---|---|
| Honey | ¾ cup | ¼ cup |
| Maple syrup | ¾ cup | 3 tbsp |
| Agave syrup | ⅔ cup | ¼ cup |
| Brown sugar | 1 cup (packed) | — |
| Coconut sugar | 1 cup | — |
| Jaggery (grated) | 1 cup | — |

## Baking with honey

- Lower the oven temperature by about 15 °C (25 °F) because honey browns faster.
- Add about ¼ teaspoon of baking soda per cup of honey to balance its acidity.
- Honey keeps baked goods moist longer.

## Sweetness

Honey is about 1–1.5 times as sweet as sugar by weight, which is why less is used. Fructose-rich syrups like agave are sweeter still.

## Calories

| Sweetener | kcal per tablespoon |
|---|---|
| Granulated sugar | about 48 |
| Honey | about 64 |
| Maple syrup | about 52 |

Honey has more calories per tablespoon because it is denser, but you use less of it.

## When not to swap

Recipes that rely on sugar crystals, like meringues and some biscuits, do not work well with liquid sweeteners.
''', [
 ('How much honey replaces 1 cup of sugar?', 'About ¾ cup, reducing other liquids by ¼ cup.'),
 ('Should I lower the oven temperature when using honey?', 'Yes, by about 15 °C (25 °F), as honey browns faster.'),
], before='## Rules of thumb')

expand('food/turkey-cooking-time', '''
## Roasting times at 160–165 °C (325 °F), unstuffed

| Turkey weight | Approximate time |
|---|---|
| 3.5–5.5 kg (8–12 lb) | 2¾–3 hours |
| 5.5–6.5 kg (12–14 lb) | 3–3¾ hours |
| 6.5–8 kg (14–18 lb) | 3¾–4¼ hours |
| 8–9 kg (18–20 lb) | 4¼–4½ hours |
| 9–11 kg (20–24 lb) | 4½–5 hours |

Times follow US Department of Agriculture guidance. A stuffed turkey takes about 15–45 minutes longer.

## Checking doneness

Use a meat thermometer in the thickest part of the thigh, the wing and the thickest part of the breast. All should read at least **74 °C (165 °F)**. Pop-up timers are not reliable on their own.

## Resting

Rest the turkey under loose foil for 20–40 minutes. Juices settle and the temperature rises a few degrees, making carving easier.

## Spatchcocked turkey

Removing the backbone and flattening the bird cuts roasting time roughly in half and cooks the breast and legs more evenly.

## Planning the day

Work back from serving time: cooking time + resting time + 30 minutes for the oven to heat and the bird to come out of the fridge.
''', [
 ('How long to cook a 6 kg turkey?', 'About 3–3¾ hours at 160–165 °C (325 °F), unstuffed.'),
 ('What temperature should turkey reach?', '74 °C (165 °F) in the thickest parts.'),
])

expand('food/turkey-thawing', '''
## Thawing times

| Turkey weight | In the fridge | In cold water |
|---|---|---|
''' + ''.join(f"| {kg} kg ({kg/0.45359:.0f} lb) | {kg/0.45359/4:.1f} days | {kg/0.45359*0.5:.1f} hours |\n" for kg in [4, 5, 6, 7, 8, 9, 10]) + '''
## Safe thawing methods

1. **Refrigerator** (safest): about 24 hours per 4–5 lb (2 kg) at 4 °C or below. A thawed turkey can stay in the fridge for 1–2 more days.
2. **Cold water**: keep the turkey in its leak-proof wrapping, submerged, and change the water every 30 minutes. Cook immediately after thawing.
3. **Microwave**: only if it fits and the manufacturer allows; cook immediately.

Never thaw a turkey on the counter at room temperature — the outside can reach unsafe temperatures while the inside is still frozen.

## Cooking from frozen

You can roast a turkey from frozen; it takes about 50% longer than a thawed one. Remove the giblet bag once it loosens.

## Plan ahead

Count back from the day you will cook: a 7 kg turkey needs nearly 4 days in the fridge, so start on the Sunday or Monday for a Thursday meal.
''', [
 ('How long does a turkey take to thaw in the fridge?', 'About 1 day for every 4–5 lb (around 2 kg).'),
 ('Can I refreeze a thawed turkey?', 'If thawed in the fridge, yes, though quality may drop. Not if thawed in cold water or the microwave.'),
])

expand('food/yeast-converter', '''
## Yeast types compared

| Type | How to use | Shelf life |
|---|---|---|
| Fresh (cake) yeast | Crumble into flour or dissolve in water | 1–2 weeks refrigerated |
| Active dry yeast | Often dissolved in warm water first | About a year unopened |
| Instant (rapid-rise) yeast | Mix straight into flour | About a year unopened; months in the freezer |

## Common packet sizes

| Packet | Instant | Active dry | Fresh equivalent |
|---|---|---|---|
| US packet | 7 g (2¼ tsp) | 7 g | about 18–21 g |
| UK sachet | 7 g | 7 g | about 18–21 g |

## Testing yeast

Mix the yeast with warm water (about 37–43 °C) and a pinch of sugar. After 5–10 minutes it should foam. If not, the yeast is dead.

## Water temperature

| Yeast | Water temperature |
|---|---|
| Active dry (dissolving) | 40–46 °C |
| Instant (mixed with flour) | up to 50–55 °C in the liquid |
| Fresh | 25–30 °C |

Above about 60 °C, yeast dies.

## Less yeast, more flavour

Using less yeast with a longer, cooler rise (for example overnight in the fridge) develops more flavour in bread and pizza dough.
''', [
 ('How much fresh yeast replaces 7 g of instant yeast?', 'About 21 g (three times the weight).'),
 ('Can I use instant yeast instead of active dry?', 'Yes. Use about 25% less instant yeast and mix it straight into the flour.'),
], before='## Conversion ratios')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/food/*.mdx')):
    c = 'food/' + os.path.basename(p)[:-4]; print(c, words(c))
