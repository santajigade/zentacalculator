import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
def g(x, d=4):
    s = f"{x:,.{d}f}".rstrip('0').rstrip('.')
    return s
def table2(h1, h2, vals, fn, d=4):
    rows = ''
    half = (len(vals) + 1) // 2
    for i in range(half):
        a = vals[i]; r = f"| {g(a)} | {g(fn(a), d)} |"
        if i + half < len(vals):
            b = vals[i + half]; r += f" {g(b)} | {g(fn(b), d)} |"
        else: r += " | |"
        rows += r + "\n"
    return f"| {h1} | {h2} | {h1} | {h2} |\n|---|---|---|---|\n" + rows

AC = 0.40468564224
expand('conversion/acres-to-hectares', f'''
## Acres to hectares chart

{table2('Acres', 'Hectares', [0.25, 0.5, 1, 2, 2.5, 3, 4, 5, 10, 15, 20, 25, 40, 50, 100, 160, 250, 500, 640, 1000], lambda a: a*AC, 3)}
## Hectares to acres chart

{table2('Hectares', 'Acres', [0.1, 0.25, 0.5, 1, 2, 3, 4, 5, 10, 20, 25, 50, 75, 100, 200, 500], lambda h: h/AC, 2)}
## Definitions

- **Acre**: exactly 4,046.8564224 m², or 43,560 square feet. Historically the area a team of oxen could plough in a day.
- **Hectare**: exactly 10,000 m², a square 100 m × 100 m. It is the standard land unit in the metric system.
- **1 hectare = 2.4711 acres**, and **1 acre = 0.4047 hectares**.

## Converting to local land units in India

Land in India is often measured in local units whose size varies by state:

| Unit | Approximate size |
|---|---|
| Guntha (Maharashtra, Karnataka) | 101.17 m² (40 per acre) |
| Cent (South India) | 40.47 m² (100 per acre) |
| Bigha | Varies widely — from about 1,300 m² to over 6,700 m² by state |
| Kanal (Punjab, Haryana) | 505.86 m² (8 per acre) |

Always confirm the local definition in the land record before buying or selling.
''', [
 ('How many acres is 1 hectare?', '1 hectare is 2.4711 acres.'),
 ('How many hectares is 10 acres?', '10 acres is 4.047 hectares.'),
 ('How many square feet are in an acre?', '43,560 square feet.'),
], before='## How big is an acre?')

expand('conversion/area-converter', f'''
## Square metres to square feet chart

{table2('m²', 'ft²', [1, 2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80, 100, 120, 150, 200, 250, 500, 1000], lambda a: a*10.7639104, 2)}
## Area unit definitions

| Unit | In square metres |
|---|---|
| Square inch | 0.00064516 |
| Square foot | 0.09290304 |
| Square yard | 0.83612736 |
| Acre | 4,046.856 |
| Hectare | 10,000 |
| Square kilometre | 1,000,000 |
| Square mile | 2,589,988 |

## Converting room dimensions

It is often easier to convert **lengths** first and then multiply. A room 4.2 m × 3.6 m:

- In metres: 15.12 m²
- In feet: 13.78 ft × 11.81 ft = 162.7 ft²

Both give the same area, because 15.12 × 10.764 = 162.7.

## Common mistakes

- **Multiplying by 3.28** instead of 10.764. That converts length, not area.
- **Mixing units**, such as feet for length and metres for width.
- **Forgetting walls and columns** when comparing carpet area with built-up area in property listings.
''', [
 ('How many square feet is 100 square metres?', '100 m² is 1,076.39 sq ft.'),
 ('How many square metres is 1,000 square feet?', '1,000 sq ft is 92.9 m².'),
], before='## Why area conversions square the factor')

expand('conversion/cm-to-inches', f'''
## Centimetres to inches chart (1–100 cm)

{table2('cm', 'inches', list(range(1, 21)) + [25, 30, 40, 50, 60, 70, 75, 80, 90, 100], lambda c: c/2.54, 3)}
## Body measurements

Clothing sizes often use centimetres or inches:

| Measurement | cm | inches |
|---|---|---|
| Waist | 76 | 29.9 |
| Waist | 81 | 31.9 |
| Waist | 86 | 33.9 |
| Chest | 96 | 37.8 |
| Chest | 102 | 40.2 |
| Inseam | 81 | 31.9 |

## Height in feet and inches

To convert a height in cm to feet and inches, divide by 2.54 to get inches, then divide by 12: 170 cm = 66.93 in = **5 ft 6.9 in**. See the [feet to metres converter](/conversion/feet-to-meters/) for a full height table.

## Definition

Since 1959 the inch has been defined as **exactly 2.54 cm**, so conversions between them are exact.
''', [
 ('How many inches is 30 cm?', '30 cm is 11.81 inches.'),
 ('How many cm is 12 inches?', '12 inches (1 foot) is 30.48 cm.'),
], before='## Fractions of an inch')

expand('conversion/energy-converter', '''
## Energy unit equivalents

| Unit | In joules | In kWh |
|---|---|---|
| 1 joule (J) | 1 | 0.000000278 |
| 1 calorie (cal) | 4.184 | 0.00000116 |
| 1 kilocalorie (kcal, food Calorie) | 4,184 | 0.00116 |
| 1 BTU | 1,055.06 | 0.000293 |
| 1 watt-hour (Wh) | 3,600 | 0.001 |
| 1 kilowatt-hour (kWh) | 3,600,000 | 1 |
| 1 therm | 105,505,585 | 29.31 |

## Energy in everyday terms

| Example | Energy |
|---|---|
| Phone battery (15 Wh) | 0.015 kWh, 54 kJ |
| Boiling 1 L of water from 20 °C | about 0.093 kWh, 335 kJ |
| A 2,000 kcal daily diet | 2.32 kWh, 8.37 MJ |
| 1 litre of petrol | about 9.1 kWh, 32.8 MJ |
| Typical home per day (varies widely) | 5–30 kWh |

## Fuel energy content

| Fuel | Energy (approx.) |
|---|---|
| Petrol | 32–34 MJ/L |
| Diesel | 36–38 MJ/L |
| LPG | 46 MJ/kg |
| Natural gas | 36–40 MJ/m³ |
| Firewood (dry) | 15–16 MJ/kg |

These help compare heating and cooking costs. See the [electricity cost calculator](/everyday-life/electricity-cost/).
''', [
 ('How many joules are in 1 kWh?', '3,600,000 joules (3.6 MJ).'),
 ('How many BTU are in 1 kWh?', 'About 3,412 BTU.'),
], before='## Food calories')

expand('conversion/feet-to-meters', f'''
## Feet to metres chart

{table2('Feet', 'Metres', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 40, 50, 75, 100, 1000], lambda x: x*0.3048, 3)}
## Height chart: feet and inches to cm

| Height | cm | Height | cm |
|---|---|---|---|
''' + ''.join(f"| {a//12}′{a%12}″ | {a*2.54:.1f} | {b//12}′{b%12}″ | {b*2.54:.1f} |\n" for a, b in zip(range(58, 68), range(68, 78))) + '''
## Metres to feet

Multiply metres by 3.2808 to get feet. 1.75 m = 5.74 ft. To split into feet and inches: 0.74 ft × 12 = 8.9 in, so **5 ft 9 in**.

## Altitude and building heights

| Example | Feet | Metres |
|---|---|---|
| One storey of a house | about 10 | about 3 |
| Typical cruising altitude | 35,000 | 10,668 |
| Mount Everest | 29,032 | 8,849 |

Aviation uses feet for altitude almost everywhere, while most maps use metres.
''', [
 ('How many metres is 6 feet?', '6 feet is 1.8288 metres.'),
 ('What is 5′8″ in cm?', '5 ft 8 in is 172.7 cm.'),
], before='## Square feet are different')

expand('conversion/flow-rate-converter', '''
## Flow rate equivalents

| m³/h | L/min | L/s | US gpm | ft³/min |
|---|---|---|---|---|
''' + ''.join(f"| {q} | {q*1000/60:.2f} | {q/3.6:.3f} | {q*1000/60/3.785411784:.2f} | {q/0.028316846592/60:.3f} |\n" for q in [0.5, 1, 2, 5, 10, 20, 50, 100, 250, 500]) + '''
## Flow, velocity and pipe size

Flow rate equals velocity times pipe area:

<p class="formula">Q = v × A = v × π × d² ÷ 4</p>

10 m³/h in a 50 mm pipe flows at about 1.41 m/s. Typical design velocities are 1–3 m/s for water pipes. Use the [pipe flow calculator](/engineering/pipe-flow-velocity/) to size pipes.

## Filling and emptying times

Time = volume ÷ flow rate. A 1,000-litre tank filled at 20 L/min takes **50 minutes**. At 10 m³/h (167 L/min) it takes about 6 minutes.

## Units by industry

- **Water and process plants**: m³/h, L/s.
- **US plumbing and pumps**: gallons per minute (gpm).
- **HVAC airflow**: cubic feet per minute (CFM) or m³/h.
- **Gas**: normal or standard m³/h (Nm³/h, Sm³/h), corrected to reference conditions.
''', [
 ('How many litres per minute is 1 m³/h?', '1 m³/h is 16.67 L/min.'),
 ('How do I convert gpm to m³/h?', 'Multiply US gpm by 0.2271. 100 gpm is 22.71 m³/h.'),
], before='## Liquids vs gases')

expand('conversion/kg-to-lb', f'''
## Kilograms to pounds chart

{table2('kg', 'lb', [1, 2, 5, 10, 15, 20, 25, 30, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100], lambda k: k/0.45359237, 2)}
## Pounds to kilograms chart

{table2('lb', 'kg', [1, 5, 10, 20, 50, 100, 110, 120, 130, 140, 150, 160, 170, 180, 200, 220, 250, 300], lambda p: p*0.45359237, 2)}
## Body weight in stone

The UK and Ireland often give body weight in stone and pounds (1 stone = 14 lb = 6.35 kg):

| kg | Stone and pounds |
|---|---|
''' + ''.join(f"| {k} | {int(k/0.45359237//14)} st {round(k/0.45359237%14)} lb |\n" for k in [50, 60, 70, 80, 90, 100]) + '''
## Definition

Since 1959 the international pound has been defined as **exactly 0.45359237 kg**.
''', [
 ('How many pounds is 50 kg?', '50 kg is 110.23 lb.'),
 ('How many kg is 150 lb?', '150 lb is 68.04 kg.'),
], before='## Mental shortcut')

expand('conversion/km-to-miles', f'''
## Kilometres to miles chart

{table2('km', 'miles', [1, 2, 3, 5, 8, 10, 15, 16, 20, 25, 30, 40, 50, 60, 80, 100, 120, 160, 200, 500], lambda k: k/1.609344, 2)}
## Speed limits

| km/h | mph |
|---|---|
| 30 | 18.6 |
| 50 | 31.1 |
| 80 | 49.7 |
| 100 | 62.1 |
| 120 | 74.6 |

See the [speed converter](/conversion/speed-converter/) for more.

## Definition

One international mile is **exactly 1,609.344 metres** (5,280 feet). One kilometre is 0.621371 miles.
''', [
 ('How many miles is 5 km?', '5 km is 3.11 miles.'),
 ('How many km is 26.2 miles?', 'A marathon of 26.2 miles is 42.195 km.'),
], before='## Mental trick')

expand('conversion/length-converter', '''
## Length unit definitions

| Unit | In metres |
|---|---|
| Micrometre (µm) | 0.000001 |
| Millimetre (mm) | 0.001 |
| Centimetre (cm) | 0.01 |
| Inch (in) | 0.0254 |
| Foot (ft) | 0.3048 |
| Yard (yd) | 0.9144 |
| Metre (m) | 1 |
| Kilometre (km) | 1,000 |
| Mile (mi) | 1,609.344 |
| Nautical mile (nmi) | 1,852 |

## Imperial relationships

- 12 inches = 1 foot
- 3 feet = 1 yard
- 1,760 yards = 1 mile = 5,280 feet

## Very small and very large lengths

| Unit | Size | Used for |
|---|---|---|
| Nanometre (nm) | 10<sup>−9</sup> m | Wavelengths of light, chip features |
| Micron (µm) | 10<sup>−6</sup> m | Filters, hair (about 70 µm), dust |
| Astronomical unit (AU) | about 149.6 million km | Distances in the solar system |
| Light-year | about 9.46 trillion km | Distances to stars |

## Accuracy in practice

Builders typically measure to the nearest millimetre, machinists to 0.01 mm or less, and surveyors to a few millimetres over long distances. Round your converted values to match the precision of the original measurement.
''', [
 ('How many feet are in a metre?', '1 metre is 3.2808 feet.'),
 ('How many inches are in a metre?', '1 metre is 39.37 inches.'),
], before='## Quick mental shortcuts')

expand('conversion/liters-to-gallons', f'''
## Litres to US gallons chart

{table2('Litres', 'US gal', [1, 2, 4, 5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 100, 150, 200, 500, 1000], lambda l: l/3.785411784, 3)}
## Gallons to litres

| Gallons | US gallons → litres | UK gallons → litres |
|---|---|---|
''' + ''.join(f"| {n} | {n*3.785411784:.2f} | {n*4.54609:.2f} |\n" for n in [1, 2, 5, 10, 15, 20, 50, 100]) + '''
## US vs UK gallons

- **US gallon** = 3.785 L, used in the United States.
- **UK (imperial) gallon** = 4.546 L, used in the UK for fuel economy and some liquids.

A UK gallon is about 20% larger, which is why the same car has a higher mpg figure in the UK than in the US.
''', [
 ('How many litres are in a gallon?', '3.785 litres in a US gallon, or 4.546 litres in a UK gallon.'),
 ('How many gallons is 20 litres?', '20 litres is 5.28 US gallons or 4.40 UK gallons.'),
], before='## Fuel economy conversions')

expand('conversion/mm-to-inches', f'''
## Millimetres to inches chart

{table2('mm', 'inches', [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 19, 20, 22, 25, 30, 32, 40, 50, 100], lambda m: m/25.4, 4)}
## Inch fractions to mm

| Inch | mm | Inch | mm |
|---|---|---|---|
''' + ''.join(f"| {a} | {ea*25.4:.3f} | {b} | {eb*25.4:.3f} |\n" for (a, ea), (b, eb) in zip([('1/16', 1/16), ('1/8', 1/8), ('3/16', 3/16), ('1/4', 1/4), ('5/16', 5/16), ('3/8', 3/8)], [('1/2', 1/2), ('5/8', 5/8), ('3/4', 3/4), ('7/8', 7/8), ('1', 1), ('2', 2)])) + '''
## Drill bits and spanners

Metric and imperial sizes are close but rarely identical. A 13 mm spanner fits a 1/2-inch nut (12.7 mm) loosely; a 19 mm spanner and a 3/4-inch nut (19.05 mm) are nearly interchangeable. For accuracy, use the size the fastener was designed in.

## Rainfall

Rainfall is measured in mm in most countries and inches in the US. 25 mm of rain is about 1 inch.
''', [
 ('How many inches is 10 mm?', '10 mm is 0.3937 inches, just over 3/8 inch.'),
 ('How many mm is 1/4 inch?', '1/4 inch is 6.35 mm.'),
], before='## Thousandths of an inch (thou / mil)')

expand('conversion/number-to-million', '''
## Number names table

| Number | International | Indian |
|---|---|---|
| 1,000 | One thousand | One thousand |
| 1,00,000 / 100,000 | One hundred thousand | One lakh |
| 10,00,000 / 1,000,000 | One million | Ten lakh |
| 1,00,00,000 / 10,000,000 | Ten million | One crore |
| 10,00,00,000 / 100,000,000 | One hundred million | Ten crore |
| 1,00,00,00,000 / 1,000,000,000 | One billion | One hundred crore (one arab) |
| 1,000,000,000,000 | One trillion | One lakh crore |

## Quick conversions

| Indian | International |
|---|---|
| 1 lakh | 0.1 million |
| 10 lakh | 1 million |
| 25 lakh | 2.5 million |
| 1 crore | 10 million |
| 50 crore | 500 million |
| 100 crore | 1 billion |
| 1,000 crore | 10 billion |
| 1 lakh crore | 1 trillion |

## Short scale vs long scale

Modern English uses the **short scale**, where a billion is 1,000 million (10<sup>9</sup>). Some European languages use the **long scale**, where a billion (milliard in some languages) means a million million (10<sup>12</sup>). Check the context when reading older British or European texts.

## Reading large numbers in reports

Company results in India are usually reported in crore, while global reports use million and billion. Converting ₹45,000 crore: 45,000 × 10 million = 450 billion rupees.
''', [
 ('How many lakhs make a million?', '10 lakh = 1 million.'),
 ('How many crores make a billion?', '100 crore = 1 billion.'),
], before='## Where this conversion matters')

expand('conversion/power-converter', '''
## Power conversion table

| kW | hp | PS | BTU/h | Tons of refrigeration |
|---|---|---|---|---|
''' + ''.join(f"| {k} | {k*1000/745.69987158:.2f} | {k*1000/735.49875:.2f} | {k*1000/0.29307107:,.0f} | {k*1000/3516.8528:.3f} |\n" for k in [0.5, 0.75, 1, 1.5, 2.2, 3.5, 5, 7.5, 11, 15, 37, 75, 100]) + '''
## Motor sizes

Electric motors are often sold in standard kW ratings with an hp equivalent: 0.75 kW (1 hp), 1.5 kW (2 hp), 2.2 kW (3 hp), 3.7 kW (5 hp), 7.5 kW (10 hp), 11 kW (15 hp). The power on the nameplate is the **output** at the shaft; the electrical input is higher because of losses.

## Car engine power

Car brochures may list kW, hp or PS. 100 kW = 134 hp = 136 PS. In the US, “hp” usually means mechanical horsepower; in Europe and Asia, “hp” on a brochure often means PS.

## Electrical power

For electrical loads, power in watts = volts × amps (× power factor for AC). See the [Ohm's law calculator](/physics/ohms-law/) for related calculations.
''', [
 ('How many hp is 1 kW?', '1 kW is 1.341 mechanical horsepower or 1.36 PS.'),
 ('How many kW is a 5 hp motor?', '5 hp is 3.73 kW.'),
], before='## hp vs PS')

expand('conversion/pressure-converter', '''
## Pressure conversion table

| bar | psi | kPa | atm | mmHg | mH₂O |
|---|---|---|---|---|---|
''' + ''.join(f"| {b} | {b*1e5/6894.757293168:.2f} | {b*100:g} | {b*1e5/101325:.4f} | {b*1e5/133.322387415:.1f} | {b*1e5/9806.65:.2f} |\n" for b in [0.01, 0.1, 0.5, 1, 2, 2.5, 5, 10, 16, 25, 40, 100]) + '''
## Pressure in everyday life

| Example | Typical pressure |
|---|---|
| Atmosphere at sea level | 1.013 bar, 14.7 psi |
| Car tyre | 2.0–2.5 bar, 29–36 psi |
| Bicycle tyre (road) | 6–8 bar, 80–120 psi |
| Domestic water supply | 1.5–4 bar |
| Pressure cooker | about 1 bar above atmospheric |
| Scuba tank | 200–300 bar |

## Water column

10 metres of water exerts about 1 bar. That is why pressure in a tank rises by about 0.1 bar for every metre of depth. See the [hydrostatic pressure calculator](/engineering/hydrostatic-pressure/).
''', [
 ('How many psi is 1 bar?', '1 bar is 14.504 psi.'),
 ('How many kPa is 1 atm?', '1 standard atmosphere is 101.325 kPa.'),
], before='## Units by industry')

expand('conversion/psi-to-bar', f'''
## PSI to bar chart

{table2('psi', 'bar', [1, 5, 10, 14.7, 20, 25, 28, 30, 32, 35, 40, 50, 60, 80, 100, 150, 200, 500, 1000, 3000], lambda p: p*0.0689475729, 3)}
## Bar to psi chart

{table2('bar', 'psi', [0.5, 1, 1.5, 2, 2.2, 2.5, 3, 4, 5, 6, 7, 8, 10, 16, 20, 100], lambda b: b/0.0689475729, 2)}
## psi vs psig vs psia

- **psig** (gauge) is pressure above atmospheric. Tyre gauges read psig.
- **psia** (absolute) includes atmospheric pressure: psia = psig + 14.7 at sea level.
- The same applies to bar(g) and bar(a).
''', [
 ('How many bar is 30 psi?', '30 psi is 2.07 bar.'),
 ('How many psi is 2.5 bar?', '2.5 bar is 36.26 psi.'),
], before='## Quick estimate')

expand('conversion/speed-converter', f'''
## km/h to mph chart

{table2('km/h', 'mph', [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 200], lambda k: k/1.609344, 1)}
## Speed unit definitions

| Unit | In m/s |
|---|---|
| 1 km/h | 0.2778 |
| 1 mph | 0.44704 |
| 1 ft/s | 0.3048 |
| 1 knot | 0.5144 |
| Mach 1 (at sea level, 15 °C) | about 340 |

## Pace for runners

Runners often think in pace (time per distance) rather than speed:

| Speed | Pace per km | Pace per mile |
|---|---|---|
| 8 km/h | 7:30 | 12:04 |
| 10 km/h | 6:00 | 9:39 |
| 12 km/h | 5:00 | 8:03 |
| 15 km/h | 4:00 | 6:26 |

See the [running pace calculator](/sports/pace-calculator/).
''', [
 ('What is 100 km/h in mph?', '100 km/h is 62.14 mph.'),
 ('How many km/h is 1 m/s?', '1 m/s is 3.6 km/h.'),
], before='## Reference speeds')

expand('conversion/sq-ft-to-sq-m', f'''
## Square feet to square metres chart

{table2('sq ft', 'm²', [100, 200, 300, 400, 500, 600, 750, 800, 900, 1000, 1200, 1500, 1800, 2000, 2400, 2500, 3000, 5000], lambda s: s*0.09290304, 2)}
## Typical flat sizes

| Flat type (India, typical) | sq ft | m² |
|---|---|---|
| 1 BHK | 450–650 | 42–60 |
| 2 BHK | 750–1,100 | 70–102 |
| 3 BHK | 1,200–1,800 | 111–167 |

Sizes vary widely by city and builder. Check whether the listed area is carpet, built-up or super built-up area.

## Price per square foot

To compare properties, divide the price by the area. A ₹75,00,000 flat of 1,000 sq ft costs ₹7,500 per sq ft, or about ₹80,730 per m².
''', [
 ('How many square metres is 1,000 sq ft?', '1,000 sq ft is 92.9 m².'),
 ('How many sq ft is 1 square metre?', '1 m² is 10.764 sq ft.'),
], before='## Calculating floor area')

expand('conversion/temperature-converter', '''
## Celsius to Fahrenheit chart

| °C | °F | °C | °F |
|---|---|---|---|
''' + ''.join(f"| {a} | {a*9/5+32:g} | {b} | {b*9/5+32:g} |\n" for a, b in zip([-40, -20, -10, 0, 5, 10, 15, 20, 25, 30], [35, 36.6, 37, 38, 40, 50, 60, 100, 180, 200])) + '''
## Oven temperatures

| Description | °C | °F | Gas mark |
|---|---|---|---|
| Low | 140 | 275 | 1 |
| Moderate | 180 | 350 | 4 |
| Moderately hot | 200 | 400 | 6 |
| Hot | 220 | 425 | 7 |
| Very hot | 240 | 475 | 9 |

For fan ovens, reduce the temperature by about 20 °C.

## Body temperature

| Reading | °C | °F |
|---|---|---|
| Normal (average) | 36.5–37.5 | 97.7–99.5 |
| Fever (common threshold) | 38.0 or above | 100.4 or above |

## Temperature differences

A **change** of 1 °C equals a change of 1.8 °F, with no +32. If the temperature rises by 10 °C, it rises by 18 °F.
''', [
 ('What is 0 °C in Fahrenheit?', '32 °F — the freezing point of water.'),
 ('At what temperature are Celsius and Fahrenheit equal?', 'At −40°: −40 °C = −40 °F.'),
], before='## Mental shortcut')

expand('conversion/torque-converter', '''
## Torque conversion table

| N·m | lbf·ft | lbf·in | kgf·m |
|---|---|---|---|
''' + ''.join(f"| {t} | {t/1.3558179483314:.2f} | {t/0.1129848290276:.1f} | {t/9.80665:.3f} |\n" for t in [1, 5, 10, 20, 25, 50, 80, 100, 150, 200, 300, 500]) + '''
## Typical tightening torques

| Application | Typical torque |
|---|---|
| Car wheel nuts | 80–140 N·m (59–103 lbf·ft) |
| Spark plugs | 20–30 N·m |
| Bicycle stem bolts | 4–6 N·m |
| Engine head bolts | Varies — follow the manual |

Always use the value from the manufacturer's manual and a calibrated torque wrench.

## Torque and power

Power = torque × angular speed. In practical units:

<p class="formula">P (kW) = T (N·m) × rpm ÷ 9,549</p>

An engine producing 300 N·m at 4,000 rpm delivers about 126 kW.
''', [
 ('How many lbf·ft is 100 N·m?', '100 N·m is 73.76 lbf·ft.'),
 ('How many N·m is 50 ft-lbs?', '50 lbf·ft is 67.79 N·m.'),
], before='## Torque and motors')

expand('conversion/volume-converter', '''
## Volume conversion table

| Litres | mL | m³ | US gal | UK gal | ft³ |
|---|---|---|---|---|---|
''' + ''.join(f"| {l} | {l*1000:,.0f} | {l/1000:g} | {l/3.785411784:.3f} | {l/4.54609:.3f} | {l/28.316846592:.4f} |\n" for l in [0.25, 0.5, 1, 2, 5, 10, 20, 50, 100, 1000]) + '''
## Kitchen volumes

| Measure | mL (US) |
|---|---|
| 1 teaspoon | 4.93 |
| 1 tablespoon | 14.79 |
| 1 fluid ounce | 29.57 |
| 1 cup | 236.6 |
| 1 pint (US) | 473.2 |
| 1 quart (US) | 946.4 |

Metric recipes often use a 250 mL cup and a 15 mL tablespoon. See the [cooking converter](/food/grams-to-cups/) for ingredients by weight.

## Cubic measures

- 1 m³ = 1,000 litres
- 1 cm³ = 1 mL
- 1 ft³ = 28.32 litres
- 1 in³ = 16.39 mL
''', [
 ('How many litres are in a cubic metre?', '1,000 litres.'),
 ('How many mL are in a cup?', '236.6 mL in a US cup; 250 mL in a metric cup.'),
], before='## Handy equivalents')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/conversion/*.mdx')):
    c = 'conversion/' + os.path.basename(p)[:-4]; print(c, words(c))
