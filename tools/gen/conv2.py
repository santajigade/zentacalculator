"""Rich unit-conversion pages (batch A)."""
import sys; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
D = '2026-10-27'
F = {
 'length': {'m':1,'mm':1e-3,'cm':1e-2,'km':1e3,'in':0.0254,'ft':0.3048,'yd':0.9144,'mi':1609.344,'nmi':1852},
 'mass': {'kg':1,'g':1e-3,'mg':1e-6,'t':1e3,'lb':0.45359237,'oz':0.028349523125,'st':6.35029318},
 'volume': {'m3':1,'L':1e-3,'mL':1e-6,'galUS':0.003785411784,'galUK':0.00454609,'floz':0.0000295735295625,'cup':0.0002365882365,'tbsp':0.00001478676478125,'tsp':0.00000492892159375,'ft3':0.028316846592},
 'velocity': {'ms':1,'kmh':1/3.6,'mph':0.44704,'kn':1852/3600,'fts':0.3048},
 'power': {'W':1,'kW':1e3,'hp':745.69987158,'PS':735.49875,'BTUh':0.29307107},
 'area': {'m2':1,'ft2':0.09290304,'yd2':0.83612736,'acre':4046.8564224,'ha':1e4,'cm2':1e-4,'in2':0.00064516},
 'land': {'m2':1,'ft2':0.09290304,'yd2':0.83612736,'acre':4046.8564224,'ha':1e4,'cent':40.468564224,'guntha':101.17141056,'kanal':505.857053,'marla':25.2928526},
}
LAB = {'m':'m','mm':'mm','cm':'cm','km':'km','in':'in','ft':'ft','yd':'yd','mi':'mi','nmi':'nmi','kg':'kg','g':'g','mg':'mg','t':'t','lb':'lb','oz':'oz','st':'st',
 'L':'L','mL':'mL','m3':'m³','galUS':'US gal','galUK':'UK gal','floz':'US fl oz','cup':'US cup','tbsp':'tbsp','tsp':'tsp','ft3':'ft³','ms':'m/s','kmh':'km/h','mph':'mph','kn':'knots','fts':'ft/s',
 'W':'W','kW':'kW','hp':'hp','PS':'PS','BTUh':'BTU/h','m2':'m²','ft2':'sq ft','yd2':'sq yd','acre':'acre','ha':'ha','cm2':'cm²','in2':'in²','cent':'cent','guntha':'guntha','kanal':'kanal','marla':'marla'}

def fmt(x):
    if x == 0: return '0'
    a = abs(x)
    if a >= 1e7 or a < 1e-4: return f'{x:.4g}'
    if a >= 1000: return f'{x:,.2f}'.rstrip('0').rstrip('.')
    return f'{x:.6g}'

def cv(fam, v, a, b): return v * F[fam][a] / F[fam][b]

def chart(fam, a, b, vals):
    half = (len(vals) + 1) // 2
    out = f"| {LAB[a]} | {LAB[b]} | {LAB[a]} | {LAB[b]} |\n|---|---|---|---|\n"
    for i in range(half):
        x = vals[i]; r = f"| {fmt(x)} | {fmt(cv(fam, x, a, b))} |"
        if i + half < len(vals):
            y = vals[i + half]; r += f" {fmt(y)} | {fmt(cv(fam, y, a, b))} |"
        else: r += " | |"
        out += r + "\n"
    return out

def make(slug, title, desc, kw, fam, units, default, a, b, vals, vals2, formula, defs, body, faq, related, featured=False):
    vs = []
    for i, (u, label) in enumerate(units):
        d = f', default: {default}' if i == 0 else ''
        vs.append(f'  - {{ id: u{i}, label: "{label}", family: {fam}, unit: {u}{d}, min: 0 }}')
    eqs = '\n'.join(f'  - u{i} = u{i+1}' for i in range(len(units) - 1))
    fq = ''.join(f'  - q: "{q}"\n    a: "{x}"\n' for q, x in faq)
    one = cv(fam, 1, a, b)
    page('conversion', slug, f'''
title: {title}
description: {desc}
category: conversion
keywords: [{", ".join(kw)}]
updated: {D}
{"featured: true" if featured else ""}
variables:
{chr(10).join(vs)}
equations:
{eqs}
faq:
{fq.rstrip()}
related: [{", ".join(related)}]
''', f'''
## How to use this converter

Type a value in **{units[0][1]}** and the other units update instantly. Every field is live, so you can just as easily start from {units[1][1].lower()} or any other unit and convert back.

## The formula

<p class="formula">{formula}</p>

1 {LAB[a]} = {fmt(one)} {LAB[b]}, and 1 {LAB[b]} = {fmt(1/one)} {LAB[a]}.

## {LAB[a]} to {LAB[b]} chart

{chart(fam, a, b, vals)}
## {LAB[b]} to {LAB[a]} chart

{chart(fam, b, a, vals2)}
## Definitions

{defs}

{body}
''')

# ---------------------------------------------------------------- pages
make('inches-to-cm', 'Inches to CM Converter', 'Convert inches to centimetres (and cm to inches) instantly, with charts for common sizes, heights and fractions of an inch.',
 ['inches to cm', 'inch to cm', 'in to cm', 'inches to centimeters', 'convert inches to cm', 'how many cm in an inch'],
 'length', [('in', 'Inches'), ('cm', 'Centimetres'), ('mm', 'Millimetres'), ('ft', 'Feet')], 12, 'in', 'cm',
 [0.25, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 18, 20, 24, 30, 36, 40, 48, 50], [1, 2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 90, 100],
 'cm = inches × 2.54',
 '- **Inch**: exactly 2.54 cm, by international agreement in 1959. 12 inches make a foot.\n- **Centimetre**: one hundredth of a metre. 10 mm = 1 cm.',
 '''## Fractions of an inch in cm

| Inch | cm | Inch | cm |
|---|---|---|---|
| 1/16 | 0.159 | 1/2 | 1.27 |
| 1/8 | 0.318 | 5/8 | 1.588 |
| 1/4 | 0.635 | 3/4 | 1.905 |
| 3/8 | 0.953 | 7/8 | 2.223 |

## Everyday sizes

- **Phone screens**: a 6.1-inch screen is 15.5 cm diagonally.
- **TVs**: a 55-inch TV is 139.7 cm diagonally — see the [TV size calculator](/everyday-life/tv-size/).
- **Clothing**: a 32-inch waist is 81.3 cm.
- **Paper**: US Letter is 8.5 × 11 in (21.6 × 27.9 cm).

## Mental shortcut

Multiply inches by 2.5 for a quick estimate, then add a little. 10 in ≈ 25 cm (exact: 25.4 cm).''',
 [('How many cm is 1 inch?', 'Exactly 2.54 cm.'), ('How many cm is 12 inches?', '30.48 cm, which is 1 foot.'), ('How many inches is 100 cm?', '39.37 inches.')],
 ['conversion/cm-to-inches', 'conversion/feet-to-inches', 'conversion/mm-to-inches', 'conversion/length-converter'], True)

make('lbs-to-kg', 'Pounds to Kilograms Converter (lbs to kg)', 'Convert pounds to kilograms and kg to lbs instantly, with charts for body weights, luggage and gym plates.',
 ['lbs to kg', 'pounds to kg', 'lb to kg', 'pounds to kilograms', 'convert lbs to kg', 'weight converter'],
 'mass', [('lb', 'Pounds (lb)'), ('kg', 'Kilograms'), ('oz', 'Ounces'), ('st', 'Stone'), ('g', 'Grams')], 150, 'lb', 'kg',
 [1, 2, 5, 10, 20, 25, 30, 40, 45, 50, 60, 75, 100, 110, 120, 130, 140, 150, 160, 180, 200, 220, 250, 300], [1, 5, 10, 20, 25, 50, 60, 70, 80, 90, 100, 120],
 'kg = lb × 0.45359237',
 '- **Pound (lb)**: exactly 0.45359237 kg (international pound, 1959). 1 lb = 16 oz.\n- **Kilogram**: the SI base unit of mass, about 2.20462 lb.',
 '''## Luggage allowances

| Allowance | Pounds |
|---|---|
| 7 kg cabin bag | 15.4 lb |
| 15 kg checked bag | 33.1 lb |
| 23 kg checked bag | 50.7 lb |
| 32 kg heavy bag | 70.5 lb |

## Gym plates

Plates are sold in kg or lb: a 20 kg plate is 44.1 lb, and a 45 lb plate is 20.4 kg. A standard Olympic bar is 20 kg (44 lb).

## Mental shortcut

Divide pounds by 2.2: 150 lb ÷ 2.2 ≈ 68 kg. For a quick estimate, halve and take away 10%: 150 → 75 → 67.5 kg.''',
 [('How many kg is 1 lb?', '0.4536 kg.'), ('How many kg is 150 lbs?', '68.04 kg.'), ('How many lbs is 1 kg?', '2.2046 lb.')],
 ['conversion/kg-to-lb', 'conversion/stone-to-kg', 'conversion/oz-to-grams', 'health/bmi'], True)

make('miles-to-km', 'Miles to KM Converter', 'Convert miles to kilometres and km to miles instantly, with charts for running distances, speed limits and road trips.',
 ['miles to km', 'mile to km', 'miles to kilometers', 'convert miles to km', 'mi to km'],
 'length', [('mi', 'Miles'), ('km', 'Kilometres'), ('m', 'Metres'), ('ft', 'Feet')], 10, 'mi', 'km',
 [0.25, 0.5, 1, 2, 3, 3.1, 5, 6.2, 10, 13.1, 15, 20, 25, 26.2, 30, 50, 60, 100, 200, 500], [1, 2, 5, 8, 10, 16, 21.1, 25, 42.2, 50, 80, 100, 160, 1000],
 'km = miles × 1.609344',
 '- **Mile (statute)**: exactly 1,609.344 m, or 5,280 ft.\n- **Kilometre**: 1,000 m, about 0.6214 miles.\n- **Nautical mile**: 1,852 m — used at sea and in aviation, not on roads.',
 '''## Running distances

| Race | Miles | Kilometres |
|---|---|---|
| 5K | 3.11 | 5 |
| 10K | 6.21 | 10 |
| Half marathon | 13.11 | 21.0975 |
| Marathon | 26.22 | 42.195 |

## The Fibonacci trick

Consecutive Fibonacci numbers (3, 5, 8, 13, 21, 34…) are close to the miles-to-km ratio: 5 miles ≈ 8 km, 8 miles ≈ 13 km, 13 miles ≈ 21 km.

## Driving

Distances on UK and US road signs are in miles; most other countries use km. A 300-mile road trip is about 483 km.''',
 [('How many km is 1 mile?', '1.609 km.'), ('How many km is 26.2 miles?', '42.195 km — the marathon distance.'), ('How many miles is 100 km?', '62.14 miles.')],
 ['conversion/km-to-miles', 'conversion/mph-to-kmh', 'sports/pace-calculator', 'conversion/length-converter'], True)

# temperature (custom: offsets)
rowsF = ''.join(f"| {f:g} °F | {(f-32)*5/9:.1f} °C | {g:g} °F | {(g-32)*5/9:.1f} °C |\n" for f, g in zip([-40, 0, 10, 20, 32, 40, 50, 60, 70], [80, 90, 98.6, 100, 104, 212, 300, 350, 400, 450][:9]))
page('conversion', 'fahrenheit-to-celsius', f'''
title: Fahrenheit to Celsius Converter (°F to °C)
description: Convert Fahrenheit to Celsius and Celsius to Fahrenheit instantly — with charts for weather, body temperature, cooking and ovens.
category: conversion
keywords: [fahrenheit to celsius, f to c, °f to °c, convert fahrenheit to celsius, celsius to fahrenheit, temperature conversion]
updated: {D}
featured: true
variables:
  - {{ id: f, label: Fahrenheit, family: temperature, unit: F, default: 98.6 }}
  - {{ id: c, label: Celsius, family: temperature, unit: C }}
  - {{ id: k, label: Kelvin, family: temperature, unit: K, min: 0 }}
equations:
  - f = c
  - c = k
faq:
  - q: "How do I convert Fahrenheit to Celsius?"
    a: "Subtract 32, then multiply by 5/9. 98.6 °F − 32 = 66.6; × 5/9 = 37 °C."
  - q: "What is 100 °F in Celsius?"
    a: "37.8 °C."
  - q: "What is 350 °F in Celsius?"
    a: "176.7 °C — usually rounded to 180 °C for ovens."
  - q: "Is there a quick way to estimate?"
    a: "Subtract 30 and halve. 80 °F → 50 → 25 °C (exact: 26.7 °C)."
related: [conversion/temperature-converter, food/oven-temperature, health/heart-rate-zones, everyday-life/sleep-calculator]
''', f'''
## How to use this converter

Type a temperature in **Fahrenheit**, **Celsius** or **Kelvin** — the others update instantly.

## The formula

<p class="formula">°C = (°F − 32) × 5 ÷ 9 &nbsp;·&nbsp; °F = °C × 9 ÷ 5 + 32</p>

## Fahrenheit to Celsius chart

| °F | °C | °F | °C |
|---|---|---|---|
{rowsF}
## Celsius to Fahrenheit chart

| °C | °F | °C | °F |
|---|---|---|---|
''' + ''.join(f"| {c:g} °C | {c*9/5+32:.1f} °F | {d:g} °C | {d*9/5+32:.1f} °F |\n" for c, d in zip([-20, -10, 0, 5, 10, 15, 20], [25, 30, 35, 37, 40, 100, 200])) + '''
## Key reference points

| Event | °F | °C |
|---|---|---|
| Water freezes | 32 | 0 |
| Room temperature | 68–72 | 20–22 |
| Normal body temperature | 98.6 (average) | 37 |
| Fever (common threshold) | 100.4 | 38 |
| Water boils (sea level) | 212 | 100 |
| Fahrenheit and Celsius equal | −40 | −40 |

## Weather

- Below 32 °F (0 °C): freezing — watch for ice.
- 50–68 °F (10–20 °C): cool to mild.
- 68–77 °F (20–25 °C): comfortable.
- Above 95 °F (35 °C): very hot — stay hydrated.

## Ovens

Common oven settings: 325 °F = 160 °C, 350 °F = 180 °C, 400 °F = 200 °C, 425 °F = 220 °C. See the [oven temperature converter](/food/oven-temperature/) for gas marks and fan ovens.

## Temperature differences

A change of 1 °C equals a change of 1.8 °F. If a forecast says it will be 10 °F warmer, that is about 5.6 °C warmer — do not subtract 32 for differences.
''')

make('meters-to-feet', 'Meters to Feet Converter', 'Convert metres to feet (and feet and inches) instantly, with charts for heights, rooms and buildings.',
 ['meters to feet', 'm to ft', 'metres to feet', 'meter to feet and inches', 'convert meters to feet'],
 'length', [('m', 'Metres'), ('ft', 'Feet'), ('in', 'Inches'), ('cm', 'Centimetres'), ('yd', 'Yards')], 1, 'm', 'ft',
 [0.5, 1, 1.5, 1.6, 1.7, 1.75, 1.8, 2, 2.5, 3, 4, 5, 6, 8, 10, 15, 20, 25, 50, 100], [1, 2, 3, 5, 6, 8, 10, 12, 15, 20, 30, 50, 100, 1000],
 'ft = m ÷ 0.3048 ≈ m × 3.28084',
 '- **Metre**: the SI base unit of length.\n- **Foot**: exactly 0.3048 m, or 12 inches.',
 '''## Heights in feet and inches

| Metres | Feet and inches |
|---|---|
''' + ''.join(f"| {m} m | {int(m/0.3048)}′ {round((m/0.3048 % 1)*12,1)}″ |\n" for m in [1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9]) + '''
## Converting to feet and inches

Multiply metres by 3.28084 to get feet. Take the whole number as feet, then multiply the decimal part by 12 for inches. 1.75 m = 5.741 ft → 5 ft + 0.741 × 12 = **5 ft 8.9 in**.

## Buildings and rooms

- One storey is roughly 3 m (about 10 ft).
- A 4 × 5 m room is about 13.1 × 16.4 ft.
- For floor area, convert square metres with the [sq m to sq ft converter](/conversion/sq-m-to-sq-ft/), not by multiplying by 3.28.''',
 [('How many feet is 1 metre?', '3.281 feet (3 ft 3.4 in).'), ('What is 1.8 m in feet?', '5.91 ft, or 5 ft 10.9 in.'), ('How many metres is 6 feet?', '1.829 m.')],
 ['conversion/feet-to-meters', 'conversion/inches-to-cm', 'conversion/length-converter', 'conversion/sq-m-to-sq-ft'], True)

make('gallons-to-liters', 'Gallons to Liters Converter', 'Convert US and UK gallons to litres instantly, with charts for fuel, water tanks and cooking.',
 ['gallons to liters', 'gallon to litre', 'gal to l', 'us gallons to liters', 'uk gallons to litres', 'how many liters in a gallon'],
 'volume', [('galUS', 'US gallons'), ('L', 'Litres'), ('galUK', 'UK (imperial) gallons'), ('mL', 'Millilitres'), ('m3', 'Cubic metres')], 1, 'galUS', 'L',
 [0.25, 0.5, 1, 2, 3, 5, 10, 13, 15, 20, 25, 30, 40, 50, 55, 75, 100, 500, 1000], [1, 2, 4, 5, 10, 20, 25, 50, 60, 100, 200, 1000],
 'litres = US gallons × 3.785411784',
 '- **US gallon**: exactly 3.785411784 L (231 cubic inches).\n- **UK (imperial) gallon**: exactly 4.54609 L, about 20% larger.\n- **Litre**: 1,000 mL, or one cubic decimetre.',
 '''## US vs UK gallons

| Gallons | US gallons in litres | UK gallons in litres |
|---|---|---|
''' + ''.join(f"| {g} | {g*3.785411784:.2f} | {g*4.54609:.2f} |\n" for g in [1, 5, 10, 20, 50]) + '''
Fuel economy figures in the UK (mpg) use imperial gallons, which is why UK mpg numbers look higher than US numbers for the same car.

## Common uses

- **Fuel tanks**: a 15-gallon US tank holds about 57 L.
- **Water heaters**: a 50-gallon heater holds about 189 L.
- **Drums**: a standard 55 US gallon drum holds about 208 L.
- **Aquariums**: see the [aquarium volume calculator](/other/aquarium-volume/).''',
 [('How many litres are in a gallon?', '3.785 L in a US gallon; 4.546 L in a UK gallon.'), ('How many litres is 5 gallons?', '18.93 L (US) or 22.73 L (UK).'), ('How many gallons is 100 litres?', '26.42 US gallons or 22 UK gallons.')],
 ['conversion/liters-to-gallons', 'conversion/volume-converter', 'everyday-life/fuel-economy', 'conversion/ml-to-oz'])

make('oz-to-grams', 'Ounces to Grams Converter (oz to g)', 'Convert ounces to grams and grams to ounces instantly — for cooking, postage, jewellery and nutrition labels.',
 ['oz to grams', 'ounces to grams', 'oz to g', 'grams to ounces', 'convert oz to grams'],
 'mass', [('oz', 'Ounces (oz)'), ('g', 'Grams'), ('lb', 'Pounds'), ('kg', 'Kilograms')], 1, 'oz', 'g',
 [0.25, 0.5, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 20, 24, 32], [1, 5, 10, 25, 28, 50, 100, 125, 200, 250, 454, 500, 1000],
 'grams = ounces × 28.349523125',
 '- **Ounce (avoirdupois)**: exactly 28.349523125 g. 16 oz = 1 lb.\n- **Troy ounce**: 31.1035 g — used only for precious metals.\n- **Fluid ounce**: a unit of volume, not weight. See the [mL to oz converter](/conversion/ml-to-oz/).',
 '''## Cooking

| Ingredient amount | Grams |
|---|---|
| 1 oz butter | 28 g (2 tbsp) |
| 4 oz (¼ lb) | 113 g — one US stick of butter |
| 8 oz (½ lb) | 227 g |
| 16 oz (1 lb) | 454 g |

## Gold and silver: troy ounces

Precious metals are priced per **troy ounce** (31.1035 g), which is about 10% heavier than a regular ounce. A 1 oz gold coin contains 31.1 g of gold.

## Postage

Letter and parcel rates are often set in ounces in the US: a 1 oz letter is about 28 g.''',
 [('How many grams is 1 oz?', '28.35 g.'), ('How many grams is 8 oz?', '226.8 g.'), ('How many ounces is 100 g?', '3.53 oz.')],
 ['conversion/lbs-to-kg', 'food/grams-to-cups', 'food/butter-converter', 'conversion/kg-to-lb'])

make('ml-to-oz', 'ML to Oz Converter (Fluid Ounces)', 'Convert millilitres to US fluid ounces and fl oz to mL instantly — for drinks, baby bottles, cosmetics and recipes.',
 ['ml to oz', 'ml to fl oz', 'milliliters to ounces', 'oz to ml', 'fluid ounces to ml'],
 'volume', [('mL', 'Millilitres'), ('floz', 'US fluid ounces'), ('cup', 'US cups'), ('tbsp', 'Tablespoons'), ('L', 'Litres')], 100, 'mL', 'floz',
 [5, 10, 15, 30, 50, 60, 100, 120, 150, 200, 240, 250, 300, 330, 355, 375, 500, 750, 1000], [0.5, 1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 32],
 'US fl oz = mL ÷ 29.5735',
 '- **US fluid ounce**: 29.5735 mL. 8 fl oz = 1 US cup.\n- **UK (imperial) fluid ounce**: 28.4131 mL, slightly smaller.\n- **Millilitre**: one thousandth of a litre, equal to 1 cm³.',
 '''## Common container sizes

| Container | mL | US fl oz |
|---|---|---|
| Espresso shot | 30 | 1.0 |
| Baby bottle (small) | 120–150 | 4–5 |
| Soda can | 330–355 | 11.2–12 |
| Wine bottle | 750 | 25.4 |
| Water bottle | 500 | 16.9 |

## Travel liquids

Many airports limit cabin liquids to containers of **100 mL** (3.4 fl oz) each, in a single clear bag. Check current rules for your airport.

## Fluid ounces vs ounces

Fluid ounces measure volume; ounces measure weight. One US fl oz of water weighs about 1.04 oz (29.6 g), but a fluid ounce of honey weighs much more.''',
 [('How many oz is 100 mL?', '3.38 US fl oz.'), ('How many mL is 8 oz?', '236.6 mL — one US cup.'), ('How many oz is 500 mL?', '16.9 US fl oz.')],
 ['conversion/oz-to-grams', 'food/cooking-converter', 'conversion/gallons-to-liters', 'conversion/volume-converter'])

make('mph-to-kmh', 'MPH to KM/H Converter', 'Convert miles per hour to kilometres per hour (and km/h to mph) instantly, with speed-limit and driving charts.',
 ['mph to kmh', 'mph to km/h', 'miles per hour to km per hour', 'kmh to mph', 'speed conversion'],
 'velocity', [('mph', 'Miles per hour'), ('kmh', 'Kilometres per hour'), ('ms', 'Metres per second'), ('kn', 'Knots')], 60, 'mph', 'kmh',
 [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 90, 100, 120, 150], [10, 20, 30, 40, 50, 60, 80, 90, 100, 110, 120, 130],
 'km/h = mph × 1.609344',
 '- **Miles per hour (mph)**: used for road speeds in the US and UK.\n- **Kilometres per hour (km/h)**: used in most other countries.\n- **Knot**: one nautical mile per hour (1.852 km/h), used at sea and in aviation.',
 '''## Speed limits

| Typical limit | mph | km/h |
|---|---|---|
| School zone (US) | 20–25 | 32–40 |
| UK town | 30 | 48 |
| UK single carriageway | 60 | 97 |
| US interstate (many states) | 65–75 | 105–121 |
| UK motorway | 70 | 113 |

## Stopping distance grows fast

Doubling speed roughly quadruples braking distance. At 60 mph (97 km/h), total stopping distance is about 73 m in good conditions. See the [SUVAT calculator](/physics/suvat-equations/).

## Quick estimate

Multiply mph by 1.6: 50 mph × 1.6 = 80 km/h (exact 80.5).''',
 [('What is 60 mph in km/h?', '96.56 km/h.'), ('What is 100 km/h in mph?', '62.14 mph.'), ('What is 70 mph in km/h?', '112.65 km/h.')],
 ['conversion/speed-converter', 'conversion/miles-to-km', 'physics/speed-distance-time', 'everyday-life/fuel-cost'])

make('kw-to-hp', 'kW to HP Converter (Kilowatts to Horsepower)', 'Convert kilowatts to horsepower and hp to kW for motors, engines, pumps and generators — mechanical hp and metric PS.',
 ['kw to hp', 'kilowatts to horsepower', 'hp to kw', 'horsepower to kw', 'motor hp to kw', 'ps to kw'],
 'power', [('kW', 'Kilowatts'), ('hp', 'Horsepower (mechanical)'), ('PS', 'Metric horsepower (PS)'), ('W', 'Watts')], 1, 'kW', 'hp',
 [0.37, 0.55, 0.75, 1, 1.1, 1.5, 2.2, 3, 3.7, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45, 55, 75, 90, 110], [0.5, 1, 1.5, 2, 3, 5, 7.5, 10, 15, 20, 25, 50, 100, 150],
 'hp = kW ÷ 0.7457 ≈ kW × 1.341',
 '- **Mechanical horsepower (hp)**: 745.7 W. Used in the US and on many motor nameplates.\n- **Metric horsepower (PS, CV)**: 735.5 W. Common in European and Asian car specifications.\n- **Kilowatt**: 1,000 W, the SI unit used on IEC motor ratings.',
 '''## Standard motor sizes

IEC motor ratings and their usual hp labels:

| kW | hp label |
|---|---|
| 0.75 | 1 hp |
| 1.5 | 2 hp |
| 2.2 | 3 hp |
| 3.7 | 5 hp |
| 5.5 | 7.5 hp |
| 7.5 | 10 hp |
| 11 | 15 hp |
| 15 | 20 hp |

Labels are rounded; 7.5 kW is exactly 10.06 hp.

## Electrical input vs output

A motor's kW or hp rating is its **shaft output**. Electrical input is higher because of losses: a 7.5 kW motor at 90% efficiency draws about 8.3 kW. See the [three-phase motor power calculator](/engineering/three-phase-motor-power/).

## Car engines

Car brochures may use kW, hp or PS. 100 kW = 134 hp = 136 PS.''',
 [('How many hp is 1 kW?', '1.341 hp (mechanical) or 1.36 PS.'), ('How many kW is a 5 hp motor?', '3.73 kW.'), ('Is PS the same as hp?', 'Nearly: 1 PS = 0.986 hp.')],
 ['conversion/power-converter', 'engineering/three-phase-motor-power', 'engineering/torque-power-speed', 'engineering/pump-power'])

make('sq-m-to-sq-ft', 'Square Meters to Square Feet Converter (m² to sq ft)', 'Convert square metres to square feet and sq ft to m² instantly — for flats, rooms, plots and flooring.',
 ['sq m to sq ft', 'square meters to square feet', 'm2 to sq ft', 'sqm to sqft', 'square metre to square feet'],
 'area', [('m2', 'Square metres'), ('ft2', 'Square feet'), ('yd2', 'Square yards'), ('acre', 'Acres')], 100, 'm2', 'ft2',
 [1, 2, 5, 9, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75, 80, 90, 100, 120, 150, 200, 250, 500], [10, 50, 100, 200, 300, 500, 750, 1000, 1500, 2000, 2500, 5000],
 'sq ft = m² × 10.7639',
 '- **Square metre**: the area of a square 1 m on each side.\n- **Square foot**: the area of a square 1 ft on each side, 0.0929 m². 1 m² = 10.764 sq ft.',
 '''## Why not multiply by 3.28?

A square metre is 3.28 ft **by** 3.28 ft, so it equals 3.28 × 3.28 = 10.76 sq ft. Multiplying by 3.28 is a common mistake that undercounts area by more than two-thirds.

## Property sizes

| Flat or room | m² | sq ft |
|---|---|---|
| Single bedroom | 10–12 | 108–129 |
| Living room | 18–25 | 194–269 |
| 1 BHK flat | 40–60 | 430–646 |
| 2 BHK flat | 70–100 | 753–1,076 |
| 3 BHK flat | 110–160 | 1,184–1,722 |

Listings may quote carpet, built-up or super built-up area, which can differ by 20–30%.

## Price per area

₹7,500 per sq ft equals about ₹80,730 per m². Multiply price per sq ft by 10.764 to get price per m².''',
 [('How many sq ft is 1 square metre?', '10.764 sq ft.'), ('How many sq ft is 100 m²?', '1,076.4 sq ft.'), ('How many m² is 1,000 sq ft?', '92.9 m².')],
 ['conversion/sq-ft-to-sq-m', 'conversion/area-converter', 'construction/square-footage', 'conversion/gaj-to-sq-ft'], True)

make('feet-to-inches', 'Feet to Inches Converter', 'Convert feet to inches and inches to feet instantly — including feet-and-inches heights and lumber lengths.',
 ['feet to inches', 'ft to in', 'how many inches in a foot', 'inches to feet', 'feet and inches'],
 'length', [('ft', 'Feet'), ('in', 'Inches'), ('cm', 'Centimetres'), ('yd', 'Yards')], 5, 'ft', 'in',
 [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 5.5, 6, 6.5, 7, 8, 10, 12, 16, 20, 25, 50, 100], [6, 12, 18, 24, 30, 36, 48, 60, 66, 72, 84, 96, 120, 144],
 'inches = feet × 12',
 '- **Foot**: 12 inches, or 0.3048 m.\n- **Inch**: 2.54 cm. 36 inches make a yard.',
 '''## Feet-and-inches heights in inches

| Height | Inches | cm |
|---|---|---|
''' + ''.join(f"| {f}′{i}″ | {f*12+i} | {(f*12+i)*2.54:.1f} |\n" for f, i in [(4, 10), (5, 0), (5, 2), (5, 4), (5, 6), (5, 8), (5, 10), (6, 0), (6, 2), (6, 4)]) + '''
## Decimal feet

Surveying and engineering drawings often use decimal feet. 5.75 ft = 5 ft 9 in, because 0.75 × 12 = 9. To convert inches to decimal feet, divide by 12: 8 in = 0.667 ft.

## Lumber lengths

Boards are sold in standard lengths: 8 ft (96 in), 10 ft (120 in), 12 ft (144 in) and 16 ft (192 in). See the [board feet calculator](/construction/board-feet/).''',
 [('How many inches are in a foot?', '12 inches.'), ('How many inches is 5 feet 6 inches?', '66 inches.'), ('How many feet is 100 inches?', '8.33 feet (8 ft 4 in).')],
 ['conversion/inches-to-cm', 'conversion/meters-to-feet', 'conversion/feet-to-meters', 'conversion/length-converter'])

make('stone-to-kg', 'Stone to KG Converter', 'Convert stone (and stone and pounds) to kilograms and kg to stone instantly — the UK way of stating body weight.',
 ['stone to kg', 'st to kg', 'stones to kilograms', 'kg to stone', 'stone and pounds to kg'],
 'mass', [('st', 'Stone'), ('kg', 'Kilograms'), ('lb', 'Pounds')], 11, 'st', 'kg',
 [5, 6, 7, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 14, 15, 16, 18, 20], [40, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100, 110, 120],
 'kg = stone × 6.35029318',
 '- **Stone**: exactly 14 lb, or 6.35029318 kg. Used for body weight in the UK and Ireland.\n- **Kilogram**: about 0.1575 stone.',
 '''## Stone and pounds to kg

| Weight | kg |
|---|---|
''' + ''.join(f"| {s} st {p} lb | {(s*14+p)*0.45359237:.1f} |\n" for s, p in [(8, 7), (9, 0), (9, 7), (10, 0), (10, 7), (11, 0), (11, 7), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0)]) + '''
## How to convert stone and pounds

Multiply the stone by 14, add the pounds, then multiply by 0.4536. 11 st 7 lb = 161 lb = **73.0 kg**.

## Using kg for health calculators

Most health calculators use kg or lb. Convert here first, then check your [BMI](/health/bmi/) or [daily calories](/health/bmr/).''',
 [('How many kg is 1 stone?', '6.35 kg.'), ('How many kg is 10 stone?', '63.5 kg.'), ('How many stone is 70 kg?', '11.02 stone, or 11 st 0.3 lb.')],
 ['conversion/lbs-to-kg', 'conversion/kg-to-lb', 'health/bmi', 'health/ideal-weight'])

# land units
make('gaj-to-sq-ft', 'Gaj to Sq Ft Converter (Square Yards)', 'Convert gaj (square yards) to square feet, square metres and other land units — the plot measure used across North India.',
 ['gaj to sq ft', 'gaj to square feet', 'square yard to sq ft', 'sq yd to sq ft', '1 gaj in sq ft', 'gaj to sq meter'],
 'land', [('yd2', 'Gaj (square yards)'), ('ft2', 'Square feet'), ('m2', 'Square metres'), ('acre', 'Acres'), ('marla', 'Marla')], 100, 'yd2', 'ft2',
 [1, 10, 25, 50, 60, 100, 111, 120, 150, 200, 250, 300, 400, 500, 1000, 4840], [9, 100, 450, 500, 900, 1000, 1350, 1800, 2250, 2700, 4500, 9000],
 'sq ft = gaj × 9',
 '- **Gaj**: one square yard — 9 sq ft or 0.8361 m². Common for residential plots in Delhi, Uttar Pradesh, Rajasthan, Haryana and Punjab.\n- **Square foot**: 0.0929 m².\n- **Acre**: 4,840 square yards.',
 '''## Common plot sizes

| Plot | Gaj | Sq ft | m² |
|---|---|---|---|
| Small plot | 50 | 450 | 41.8 |
| Standard | 100 | 900 | 83.6 |
| Medium | 200 | 1,800 | 167.2 |
| Large | 500 | 4,500 | 418.1 |

## Is gaj always a square yard?

In most of North India, 1 gaj means 1 square yard (9 sq ft). In some regions, older records use different local definitions. Always confirm the unit used in the sale deed or revenue record.

## Price per gaj

To compare prices quoted per gaj and per sq ft: price per sq ft = price per gaj ÷ 9. ₹45,000 per gaj is ₹5,000 per sq ft.''',
 [('How many sq ft is 1 gaj?', '9 sq ft.'), ('How many sq ft is 100 gaj?', '900 sq ft.'), ('How many gaj is 1,000 sq ft?', '111.1 gaj.')],
 ['conversion/sq-m-to-sq-ft', 'conversion/cent-to-sq-ft', 'conversion/guntha-to-sq-ft', 'conversion/acres-to-hectares'])

make('cent-to-sq-ft', 'Cent to Sq Ft Converter', 'Convert cents to square feet, square metres and acres — the land unit used in Kerala, Tamil Nadu, Karnataka and Andhra Pradesh.',
 ['cent to sq ft', 'cent to square feet', '1 cent in sq ft', 'cents to acres', 'cent to sq meter', 'land measurement kerala'],
 'land', [('cent', 'Cents'), ('ft2', 'Square feet'), ('m2', 'Square metres'), ('acre', 'Acres'), ('ha', 'Hectares')], 5, 'cent', 'ft2',
 [1, 2, 2.5, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 50, 100], [100, 435.6, 500, 1000, 1200, 1500, 2000, 2400, 3000, 5000, 10000, 43560],
 'sq ft = cents × 435.6',
 '- **Cent**: one hundredth of an acre — 435.6 sq ft or 40.47 m².\n- **Acre**: 100 cents, or 43,560 sq ft.\n- **Hectare**: 247.1 cents.',
 '''## Common house plots

| Plot | Sq ft | m² |
|---|---|---|
| 3 cents | 1,306.8 | 121.4 |
| 5 cents | 2,178 | 202.3 |
| 10 cents | 4,356 | 404.7 |
| 20 cents | 8,712 | 809.4 |

## Where cents are used

Cents are standard in land records and property listings in Kerala and widely used in Tamil Nadu, Karnataka and Andhra Pradesh, often alongside acres and square feet.

## Price per cent

Price per sq ft = price per cent ÷ 435.6. A plot at ₹6,00,000 per cent works out to about ₹1,377 per sq ft.''',
 [('How many sq ft is 1 cent?', '435.6 sq ft.'), ('How many cents make an acre?', '100 cents.'), ('How many cents is 2,400 sq ft?', '5.51 cents.')],
 ['conversion/guntha-to-sq-ft', 'conversion/gaj-to-sq-ft', 'conversion/acres-to-hectares', 'conversion/sq-ft-to-sq-m'])

make('guntha-to-sq-ft', 'Guntha to Sq Ft Converter', 'Convert guntha to square feet, square metres and acres — the land unit used in Maharashtra, Karnataka, Telangana and Gujarat.',
 ['guntha to sq ft', 'guntha to square feet', '1 guntha in sq ft', 'guntha to acre', 'gunta to sq ft', 'guntha to sq meter'],
 'land', [('guntha', 'Guntha'), ('ft2', 'Square feet'), ('m2', 'Square metres'), ('acre', 'Acres'), ('ha', 'Hectares')], 1, 'guntha', 'ft2',
 [0.5, 1, 2, 3, 4, 5, 10, 11, 15, 20, 25, 30, 40, 80], [1089, 2000, 2178, 5000, 10000, 10890, 21780, 43560],
 'sq ft = guntha × 1,089',
 '- **Guntha (gunta)**: 1/40 of an acre — 1,089 sq ft (33 ft × 33 ft) or 101.17 m².\n- **Acre**: 40 guntha, or 43,560 sq ft.\n- **Are** (in some records): 100 m², close to one guntha.',
 '''## Guntha to acres

| Guntha | Acres | Sq ft |
|---|---|---|
| 10 | 0.25 | 10,890 |
| 20 | 0.5 | 21,780 |
| 30 | 0.75 | 32,670 |
| 40 | 1 | 43,560 |

## Where guntha is used

Guntha appears on 7/12 extracts and other land records in Maharashtra, in Karnataka and Telangana (as gunta) and in parts of Gujarat. It is also common in property listings for farm and NA plots.

## Old measuring chain

The guntha comes from the surveyor's chain of 33 feet: one guntha is one square chain of 33 × 33 ft.''',
 [('How many sq ft is 1 guntha?', '1,089 sq ft.'), ('How many guntha make an acre?', '40 guntha.'), ('How many guntha is 5,000 sq ft?', '4.59 guntha.')],
 ['conversion/cent-to-sq-ft', 'conversion/gaj-to-sq-ft', 'conversion/acres-to-hectares', 'conversion/sq-m-to-sq-ft'])
print('conv2 done')
