C = []
C.append(dict(slug='length-converter', title='Length Converter', featured=True,
 desc='Convert between metres, feet, inches, centimetres, kilometres, miles, yards and millimetres — type in any field.',
 keywords=['length converter','unit converter','meters to feet','feet to meters','distance converter','inches to cm'],
 family='length', default=1, units=[('m','Metres'),('ft','Feet'),('in','Inches'),('cm','Centimetres'),('mm','Millimetres'),('km','Kilometres'),('yd','Yards'),('mi','Miles')],
 how='Type a length into **any** field and every other unit updates instantly. Each field is linked, so you can start from feet, miles or millimetres just as easily as from metres.',
 formula='1 in = 2.54 cm (exact)   1 ft = 12 in = 0.3048 m   1 yd = 3 ft   1 mi = 1,760 yd = 1.609344 km',
 example='All imperial lengths are defined from the inch, which has been exactly 2.54 cm since the 1959 international yard and pound agreement — so these conversions are exact, not approximations.',
 table=dict(pair=('m','ft'),h=('Metres','Feet'),values=[0.5,1,2,5,10,100,1000]),
 table2=dict(pair=('ft','m'),h=('Feet','Metres'),values=[1,3,6,10,100,5280]),
 extra='''## Which unit to use

- **Metric (mm, cm, m, km)** — used for almost all science, engineering and everyday life worldwide.
- **Imperial / US customary (in, ft, yd, mi)** — everyday use in the United States; feet and inches are also common for heights and screen sizes elsewhere.

## Quick mental shortcuts

- 1 metre ≈ 3 ft 3 in
- 30 cm ≈ 1 foot
- 1 km ≈ 0.62 miles; 8 km ≈ 5 miles''',
 faq=[('How many feet are in a metre?','One metre is 3.28084 feet.'),('How many centimetres are in an inch?','Exactly 2.54 cm.'),('How do I convert 5 ft 10 in to cm?','First convert to inches — 5 × 12 + 10 = 70 in — then multiply by 2.54 to get 177.8 cm.')],
 related=['conversion/cm-to-inches','conversion/feet-to-meters','conversion/km-to-miles']))

C.append(dict(slug='cm-to-inches', title='CM to Inches Converter',
 desc='Convert centimetres to inches and inches to centimetres instantly, with a handy conversion table.',
 keywords=['cm to inches','inches to cm','centimeters to inches','cm in inches','height in inches'],
 family='length', default=10, units=[('cm','Centimetres'),('in','Inches'),('mm','Millimetres'),('ft','Feet')],
 how='Type a value in **centimetres** or **inches** (or mm or feet) and the others update as you type.',
 formula='inches = cm ÷ 2.54   cm = inches × 2.54',
 example='**Example:** a 30 cm ruler is 30 ÷ 2.54 = **11.81 inches**. A 15.6-inch laptop screen is 15.6 × 2.54 = **39.6 cm** across the diagonal.',
 table=dict(pair=('cm','in'),h=('Centimetres','Inches'),values=[1,2,5,10,15,20,30,50,100]),
 table2=dict(pair=('in','cm'),h=('Inches','Centimetres'),values=[1,2,6,12,24,32,55,65]),
 extra='''## Fractions of an inch

Imperial tools often show fractions: 1/16″ = 1.5875 mm, 1/8″ = 3.175 mm, 1/4″ = 6.35 mm, 1/2″ = 12.7 mm. Use the [fraction to decimal converter](/math/fraction-to-decimal/) to turn a fraction into a decimal inch first.

## Screen and TV sizes

Screen sizes are measured diagonally in inches: a 55″ TV is about 140 cm, and a 6.1″ phone screen is about 15.5 cm.''',
 faq=[('How many inches is 1 cm?','1 cm is 0.3937 inches.'),('Is 2.54 exact?','Yes. One inch is defined as exactly 2.54 cm.'),('How many cm is 6 inches?','6 × 2.54 = 15.24 cm.')],
 related=['conversion/length-converter','conversion/mm-to-inches','conversion/feet-to-meters']))

C.append(dict(slug='feet-to-meters', title='Feet to Meters Converter',
 desc='Convert feet to metres and metres to feet — including heights in feet and inches.',
 keywords=['feet to meters','meters to feet','ft to m','height converter','feet and inches to cm'],
 family='length', default=6, units=[('ft','Feet'),('m','Metres'),('cm','Centimetres'),('in','Inches')],
 how='Type a value in **feet** or **metres** and the rest update instantly. For a height like 5 ft 9 in, type it in inches (69) or as decimal feet (5.75).',
 formula='metres = feet × 0.3048   feet = metres ÷ 0.3048',
 example='**Example:** 6 ft = 6 × 0.3048 = **1.829 m** (182.9 cm). A ceiling height of 2.7 m is 2.7 ÷ 0.3048 = **8.86 ft**.',
 table=dict(pair=('ft','m'),h=('Feet','Metres'),values=[1,2,3,5,6,8,10,20,50,100]),
 table2=dict(pair=('in','cm'),h=('Height (inches)','Height (cm)'),values=[60,63,66,69,72,75]),
 extra='''## Heights in feet and inches

| Height | cm |
|---|---|
| 5′ 0″ | 152.4 |
| 5′ 4″ | 162.6 |
| 5′ 8″ | 172.7 |
| 6′ 0″ | 182.9 |
| 6′ 4″ | 193.0 |

## Square feet are different

For areas, 1 m² = 10.764 ft² — not 3.28. Use the [square feet to square metres converter](/conversion/sq-ft-to-sq-m/).''',
 faq=[('How many metres is 1 foot?','Exactly 0.3048 metres.'),('How tall is 1.75 m in feet?','1.75 ÷ 0.3048 = 5.74 ft, which is about 5 ft 9 in.'),('How many feet are in 100 metres?','328.08 feet.')],
 related=['conversion/length-converter','conversion/cm-to-inches','conversion/sq-ft-to-sq-m']))

C.append(dict(slug='km-to-miles', title='KM to Miles Converter',
 desc='Convert kilometres to miles and miles to kilometres — for running, driving and travel distances.',
 keywords=['km to miles','miles to km','kilometers to miles','5k in miles','marathon distance','distance converter'],
 family='length', default=10, units=[('km','Kilometres'),('mi','Miles'),('m','Metres'),('nmi','Nautical miles')],
 how='Type a distance in **kilometres** or **miles** (or metres, or nautical miles) and the other units update instantly.',
 formula='miles = km × 0.621371   km = miles × 1.609344',
 example='**Example:** a 10 km run is 10 × 0.621371 = **6.21 miles**. A 26.2-mile marathon is 26.2 × 1.609344 = **42.2 km**.',
 table=dict(pair=('km','mi'),h=('Kilometres','Miles'),values=[1,5,10,21.0975,42.195,50,100,500]),
 table2=dict(pair=('mi','km'),h=('Miles','Kilometres'),values=[1,5,10,26.2188,60,100]),
 extra='''## Running race distances

| Race | km | miles |
|---|---|---|
| 5K | 5 | 3.11 |
| 10K | 10 | 6.21 |
| Half marathon | 21.1 | 13.1 |
| Marathon | 42.195 | 26.2 |

## Mental trick

Use the Fibonacci numbers: 3 miles ≈ 5 km, 5 miles ≈ 8 km, 8 miles ≈ 13 km. Or multiply km by 0.6 for a quick estimate.

## Nautical miles

Sea and air navigation use the nautical mile (1,852 m), based on one minute of latitude. Speed in nautical miles per hour is a knot.''',
 faq=[('How many miles is 1 km?','0.621371 miles.'),('How many km is 1 mile?','Exactly 1.609344 km.'),('How far is a 5K in miles?','3.107 miles.')],
 related=['conversion/length-converter','conversion/speed-converter']))

C.append(dict(slug='mm-to-inches', title='MM to Inches Converter',
 desc='Convert millimetres to inches (decimal) and inches to millimetres for engineering, tools and pipe sizes.',
 keywords=['mm to inches','inches to mm','millimeters to inches','mm to in','drill size','bolt size'],
 family='length', default=25, units=[('mm','Millimetres'),('in','Inches'),('cm','Centimetres'),('um','Micrometres (µm)')],
 how='Type a value in **millimetres** or **inches** and the others update instantly. Useful for drawings, drill bits, fasteners and machining tolerances.',
 formula='inches = mm ÷ 25.4   mm = inches × 25.4',
 example='**Example:** 25 mm = 25 ÷ 25.4 = **0.984 in**. A 1/2″ bolt = 0.5 × 25.4 = **12.7 mm**.',
 table=dict(pair=('mm','in'),h=('Millimetres','Inches'),values=[1,3,5,6,8,10,12,16,20,25,50]),
 table2=dict(pair=('in','mm'),h=('Inches','Millimetres'),values=[0.0625,0.125,0.25,0.375,0.5,0.75,1]),
 extra='''## Thousandths of an inch (thou / mil)

Machinists often work in thousandths: 0.001″ = 0.0254 mm = 25.4 µm. A human hair is about 0.003″ (70–80 µm).

## Pipe sizes are nominal

A ½″ pipe does not measure 12.7 mm outside — nominal pipe sizes are trade names. A ½″ NPS steel pipe has an outside diameter of 21.3 mm. Always check the pipe standard.''',
 faq=[('How many inches is 1 mm?','0.03937 inches.'),('How many mm is 1 inch?','Exactly 25.4 mm.'),('What is 3/8 inch in mm?','3/8 = 0.375 in × 25.4 = 9.525 mm.')],
 related=['conversion/cm-to-inches','math/fraction-to-decimal']))

C.append(dict(slug='area-converter', title='Area Converter', featured=True,
 desc='Convert square metres, square feet, acres, hectares, square yards and more — type in any field.',
 keywords=['area converter','square feet to square meters','acres to hectares','sq ft','sq m','land area converter'],
 family='area', default=100, units=[('m2','Square metres (m²)'),('ft2','Square feet (ft²)'),('yd2','Square yards (yd²)'),('acre','Acres'),('ha','Hectares'),('km2','Square kilometres (km²)'),('in2','Square inches (in²)'),('cm2','Square centimetres (cm²)')],
 how='Type an area in **any** unit and every other field updates. Perfect for property sizes, land, flooring and plans.',
 formula='1 m² = 10.7639 ft²   1 acre = 4,046.86 m² = 43,560 ft²   1 ha = 10,000 m² = 2.471 acres',
 example='**Example:** a 100 m² apartment is **1,076 ft²**. A 2-acre plot is **0.809 hectares** or 8,094 m².',
 table=dict(pair=('m2','ft2'),h=('Square metres','Square feet'),values=[1,10,50,100,150,200,500,1000]),
 table2=dict(pair=('acre','ha'),h=('Acres','Hectares'),values=[0.25,0.5,1,2,5,10,100]),
 extra='''## Why area conversions square the factor

1 m = 3.28 ft, but 1 m² = 3.28 × 3.28 = **10.76 ft²**. Always convert areas with area units — multiplying square metres by 3.28 is a very common mistake.

## Land units around the world

- **Acre** — USA, UK and many Commonwealth countries.
- **Hectare** — metric countries and international agriculture.
- **Local units** such as the bigha, guntha, cent or marla vary by region — check the local definition before converting.''',
 faq=[('How many square feet are in a square metre?','10.7639 square feet.'),('How many square feet are in an acre?','Exactly 43,560 square feet.'),('How many acres are in a hectare?','2.4711 acres.')],
 related=['conversion/sq-ft-to-sq-m','conversion/acres-to-hectares','math/rectangle']))

C.append(dict(slug='sq-ft-to-sq-m', title='Square Feet to Square Meters Converter',
 desc='Convert square feet (sq ft) to square metres (m²) and back — for flats, houses, offices and flooring.',
 keywords=['sq ft to sq m','square feet to square meters','sqft to m2','carpet area','property size'],
 family='area', default=1000, units=[('ft2','Square feet (sq ft)'),('m2','Square metres (m²)'),('yd2','Square yards')],
 how='Type the area in **square feet** or **square metres** and the other updates instantly.',
 formula='m² = ft² × 0.092903   ft² = m² × 10.7639',
 example='**Example:** a 1,000 sq ft flat is 1,000 × 0.092903 = **92.9 m²**. A 50 m² office is **538 sq ft**.',
 table=dict(pair=('ft2','m2'),h=('Square feet','Square metres'),values=[100,250,500,750,1000,1200,1500,2000,3000]),
 extra='''## Carpet, built-up and super built-up area

Property listings may quote different areas. **Carpet area** is the usable floor inside the walls. **Built-up area** adds wall thickness and balconies, and **super built-up area** adds a share of common areas. Always check which one a price is based on before comparing.

## Calculating floor area

Multiply length × width for each rectangular room and add them up. The [rectangle calculator](/math/rectangle/) handles mixed units.''',
 faq=[('How many m² is 1 sq ft?','0.092903 m².'),('How many sq ft is 100 m²?','1,076.4 sq ft.'),('Is 1,000 sq ft a big flat?','At about 93 m², it is a typical two-bedroom flat in many cities.')],
 related=['conversion/area-converter','conversion/feet-to-meters','math/rectangle']))

C.append(dict(slug='acres-to-hectares', title='Acres to Hectares Converter',
 desc='Convert acres to hectares and hectares to acres — plus square metres and square feet.',
 keywords=['acres to hectares','hectares to acres','acre to ha','land measurement','farm size'],
 family='area', default=1, units=[('acre','Acres'),('ha','Hectares'),('m2','Square metres'),('ft2','Square feet')],
 how='Type a land area in **acres** or **hectares** and the other units update instantly.',
 formula='hectares = acres × 0.404686   acres = hectares × 2.47105',
 example='**Example:** a 10-acre farm is 10 × 0.404686 = **4.05 hectares**. A 3-hectare field is **7.41 acres**.',
 table=dict(pair=('acre','ha'),h=('Acres','Hectares'),values=[0.5,1,2,5,10,20,50,100,640]),
 table2=dict(pair=('ha','acre'),h=('Hectares','Acres'),values=[0.5,1,2,5,10,100]),
 extra='''## How big is an acre?

An acre is 43,560 ft² or about 4,047 m² — about 57% of a full-size (105 × 68 m) football pitch, or a square about 63.6 m on each side. A hectare is a 100 m × 100 m square.

## Where each is used

Hectares are the international standard for agriculture and forestry. Acres remain common in the USA, the UK, Canada, Australia and India.''',
 faq=[('How many hectares is 1 acre?','0.404686 hectares.'),('How many acres is 1 hectare?','2.47105 acres.'),('How many acres are in a square mile?','640 acres.')],
 related=['conversion/area-converter','conversion/sq-ft-to-sq-m']))

C.append(dict(slug='volume-converter', title='Volume Converter', featured=True,
 desc='Convert litres, gallons (US and UK), millilitres, cubic metres, cubic feet and cubic inches — type in any field.',
 keywords=['volume converter','liters to gallons','cubic meters','cubic feet','ml to liters','gallon converter'],
 family='volume', default=1, units=[('L','Litres'),('mL','Millilitres'),('m3','Cubic metres (m³)'),('galUS','US gallons'),('galUK','UK (imperial) gallons'),('ft3','Cubic feet (ft³)'),('in3','Cubic inches (in³)')],
 how='Type a volume in **any** unit and every other field updates instantly.',
 formula='1 m³ = 1,000 L   1 US gal = 3.785 L   1 UK gal = 4.546 L   1 ft³ = 28.32 L',
 example='**Example:** a 1,000-litre water tank holds **1 m³**, **264 US gallons** or **220 UK gallons**.',
 table=dict(pair=('L','galUS'),h=('Litres','US gallons'),values=[1,5,10,20,50,100,1000]),
 table2=dict(pair=('m3','ft3'),h=('Cubic metres','Cubic feet'),values=[0.1,0.5,1,2,5,10]),
 extra='''## US vs UK gallons

They are different. A **US gallon** is 3.785 litres; a **UK (imperial) gallon** is 4.546 litres — about 20% larger. Fuel-economy figures in miles per gallon are therefore not directly comparable between the two countries.

## Handy equivalents

- 1 litre = 1,000 cm³ = 1 kg of water (approximately)
- 1 m³ of water weighs about 1 tonne
- 1 barrel of oil = 42 US gallons ≈ 159 litres''',
 faq=[('How many litres are in a US gallon?','3.78541 litres.'),('How many litres are in a cubic metre?','1,000 litres.'),('Is a millilitre the same as a cubic centimetre?','Yes, 1 mL = 1 cm³.')],
 related=['conversion/liters-to-gallons','math/cylinder-volume','engineering/horizontal-tank-volume']))

C.append(dict(slug='liters-to-gallons', title='Liters to Gallons Converter',
 desc='Convert litres to US or UK gallons and gallons to litres — for fuel, water tanks and liquids.',
 keywords=['liters to gallons','gallons to liters','litres to gallons','fuel converter','l to gal'],
 family='volume', default=10, units=[('L','Litres'),('galUS','US gallons'),('galUK','UK gallons')],
 how='Type a value in **litres**, **US gallons** or **UK gallons** — the other two update instantly.',
 formula='US gal = L ÷ 3.78541   UK gal = L ÷ 4.54609',
 example='**Example:** filling a 50-litre fuel tank = **13.2 US gallons** = **11.0 UK gallons**.',
 table=dict(pair=('L','galUS'),h=('Litres','US gallons'),values=[1,4,10,20,40,50,60,100]),
 table2=dict(pair=('galUS','L'),h=('US gallons','Litres'),values=[1,5,10,15,20,55]),
 extra='''## Fuel economy conversions

- **km/L to US mpg:** multiply by 2.352
- **L/100 km to US mpg:** 235.2 ÷ (L/100 km)
- **US mpg to UK mpg:** multiply by 1.201

Example: a car using 6 L/100 km does about 39.2 US mpg or 47.1 UK mpg.

## Common container sizes

A standard oil drum holds 55 US gallons (about 208 L). A typical IBC tote holds 1,000 L (about 264 US gallons).''',
 faq=[('How many gallons is 1 litre?','0.264172 US gallons or 0.219969 UK gallons.'),('How many litres is 5 gallons?','18.93 L (US) or 22.73 L (UK).'),('Which gallon does the US use?','The US gallon of 3.785 L. The UK, Canada (historically) and some Caribbean countries use the larger imperial gallon.')],
 related=['conversion/volume-converter','conversion/flow-rate-converter']))

C.append(dict(slug='speed-converter', title='Speed Converter (km/h, mph, m/s, knots)',
 desc='Convert speeds between km/h, mph, m/s, ft/s and knots instantly — type in any field.',
 keywords=['speed converter','km/h to mph','mph to km/h','m/s to km/h','knots to mph','velocity converter'],
 family='velocity', default=100, units=[('kmh','Kilometres per hour (km/h)'),('mph','Miles per hour (mph)'),('ms','Metres per second (m/s)'),('kn','Knots'),('fts','Feet per second (ft/s)')],
 how='Type a speed in **any** unit and the others update instantly.',
 formula='mph = km/h × 0.621371   m/s = km/h ÷ 3.6   1 knot = 1.852 km/h',
 example='**Example:** 100 km/h = **62.1 mph** = **27.8 m/s** = **54.0 knots**.',
 table=dict(pair=('kmh','mph'),h=('km/h','mph'),values=[30,50,60,80,100,120,130]),
 table2=dict(pair=('mph','kmh'),h=('mph','km/h'),values=[20,30,40,55,65,70,80]),
 extra='''## Quick conversions

- **km/h → m/s:** divide by 3.6 (36 km/h = 10 m/s)
- **km/h → mph:** multiply by 0.6 for an estimate (100 km/h ≈ 60 mph)
- **Knots** are used at sea and in aviation; 1 knot = 1 nautical mile per hour.

## Reference speeds

| | km/h |
|---|---|
| Walking | 5 |
| Cycling | 15–25 |
| Sprinting (elite) | ~37 |
| Commercial jet cruise | ~900 |
| Speed of sound (sea level, 20 °C) | ~1,235 |''',
 faq=[('How do I convert km/h to mph?','Multiply by 0.621371. 80 km/h ≈ 49.7 mph.'),('How do I convert m/s to km/h?','Multiply by 3.6. 10 m/s = 36 km/h.'),('What is a knot?','One nautical mile (1,852 m) per hour, about 1.15 mph.')],
 related=['conversion/km-to-miles','engineering/pipe-flow-velocity']))

C.append(dict(slug='pressure-converter', title='Pressure Converter', featured=True,
 desc='Convert bar, psi, kPa, MPa, atm, mbar, mmHg, inH₂O and mH₂O — for instruments, tyres, hydraulics and weather.',
 keywords=['pressure converter','bar to psi','psi to bar','kpa to psi','mbar','inh2o','pressure unit conversion','mmhg'],
 family='pressure', default=1, units=[('bar','Bar'),('psi','PSI (lbf/in²)'),('kPa','Kilopascals (kPa)'),('MPa','Megapascals (MPa)'),('mbar','Millibar (mbar)'),('atm','Atmospheres (atm)'),('mmHg','mmHg (Torr)'),('inH2O','Inches of water (inH₂O)'),('mH2O','Metres of water (mH₂O)')],
 how='Type a pressure in **any** unit and every other field updates instantly — ideal for checking transmitter ranges, gauge readings and datasheets.',
 formula='1 bar = 100 kPa = 14.5038 psi   1 atm = 1.01325 bar   1 mH₂O = 98.0665 mbar',
 example='**Example:** a 0–10 bar pressure transmitter covers **0–145 psi** or **0–1 MPa**. A tyre at 32 psi is **2.21 bar**.',
 table=dict(pair=('bar','psi'),h=('bar','psi'),values=[0.1,0.5,1,2,5,10,16,25,40,100,400]),
 table2=dict(pair=('psi','bar'),h=('psi','bar'),values=[1,10,15,30,32,50,100,150,300,1000,3000]),
 extra='''## Gauge vs absolute pressure

Most gauges read **gauge pressure** (barg, psig) — relative to the surrounding atmosphere. **Absolute pressure** (bara, psia) includes the atmosphere: bara ≈ barg + 1.013. Always check which a datasheet means.

## Units by industry

| Industry | Common units |
|---|---|
| Process instrumentation | bar, mbar, kPa, psi, inH₂O |
| Hydraulics | bar, MPa, psi |
| Medicine (blood pressure) | mmHg |
| Weather | hPa (= mbar) |
| HVAC and draft | Pa, inH₂O |

The inH₂O value here uses water at 4 °C (the conventional reference); some industries use 60 °F or 68 °F, which differ by about 0.2%.''',
 faq=[('How many psi is 1 bar?','14.5038 psi.'),('How many bar is 100 psi?','6.895 bar.'),('Is mbar the same as hPa?','Yes. 1 mbar = 1 hPa = 100 Pa.')],
 related=['conversion/psi-to-bar','engineering/hydrostatic-pressure','engineering/4-20ma-scaling']))

C.append(dict(slug='psi-to-bar', title='PSI to Bar Converter',
 desc='Convert psi to bar and bar to psi instantly — for tyres, compressors, hydraulics and pressure gauges.',
 keywords=['psi to bar','bar to psi','tyre pressure','tire pressure converter','psi bar conversion'],
 family='pressure', default=32, units=[('psi','PSI'),('bar','Bar'),('kPa','Kilopascals (kPa)')],
 how='Type a value in **psi**, **bar** or **kPa** and the others update instantly.',
 formula='bar = psi × 0.0689476   psi = bar × 14.5038',
 example='**Example:** a car tyre at 32 psi is **2.21 bar** (221 kPa). A 10 bar compressor delivers **145 psi**.',
 table=dict(pair=('psi','bar'),h=('psi','bar'),values=[1,5,10,14.5,20,26,30,32,35,40,50,80,100,120]),
 table2=dict(pair=('bar','psi'),h=('bar','psi'),values=[1,1.5,2,2.2,2.5,3,6,8,10]),
 extra='''## Tyre pressures

Car tyres usually run at about 30–36 psi (2.1–2.5 bar). Check the label in your door frame or the owner's manual, and measure when the tyres are cold.

## Quick estimate

Divide psi by 14.5 to get bar, or multiply bar by 14.5 to get psi. Roughly, **1 bar ≈ 14.5 psi** and **100 psi ≈ 7 bar**.''',
 faq=[('How many bar is 30 psi?','30 psi = 2.07 bar.'),('How many psi is 2.5 bar?','2.5 bar = 36.3 psi.'),('What does psi stand for?','Pounds-force per square inch.')],
 related=['conversion/pressure-converter','engineering/hydraulic-cylinder-force']))

C.append(dict(slug='energy-converter', title='Energy Converter (kWh, J, kcal, BTU)',
 desc='Convert energy between joules, kilojoules, kWh, Wh, calories, kilocalories, BTU and therms.',
 keywords=['energy converter','kwh to joules','kcal to kj','btu to kwh','calories to joules','energy units'],
 family='energy', default=1, units=[('kWh','Kilowatt-hours (kWh)'),('MJ','Megajoules (MJ)'),('kJ','Kilojoules (kJ)'),('J','Joules (J)'),('Wh','Watt-hours (Wh)'),('kcal','Kilocalories (kcal / Calories)'),('BTU','BTU'),('therm','Therms')],
 how='Type an energy value in **any** unit and the others update instantly — useful for electricity bills, food labels, heating and engineering.',
 formula='1 kWh = 3.6 MJ = 3,412 BTU   1 kcal = 4.184 kJ   1 therm = 100,000 BTU',
 example='**Example:** **1 kWh** = 3,600 kJ = 860 kcal = 3,412 BTU. A 2,000 kcal daily diet is about **2.3 kWh** of energy.',
 table=dict(pair=('kWh','MJ'),h=('kWh','MJ'),values=[0.1,1,10,100,1000]),
 table2=dict(pair=('kcal','kJ'),h=('kcal (food Calories)','kJ'),values=[1,100,250,500,2000]),
 extra='''## Food calories

On food labels, "Calories" with a capital C are kilocalories (kcal). Many countries also print kJ: 1 kcal = 4.184 kJ.

## Energy vs power

**Energy** (kWh, J) is an amount. **Power** (kW, W) is the rate of using it. A 2 kW heater running for 3 hours uses 2 × 3 = **6 kWh**. Use the [power converter](/conversion/power-converter/) for kW, hp and BTU/h.''',
 faq=[('How many joules are in 1 kWh?','3.6 million joules (3.6 MJ).'),('How many kJ are in a kcal?','4.184 kJ.'),('How many BTU are in a kWh?','About 3,412 BTU.')],
 related=['conversion/power-converter','engineering/heat-duty','health/calories-burned']))

C.append(dict(slug='power-converter', title='Power Converter (kW to HP, BTU/h)',
 desc='Convert power between kW, W, horsepower (hp and metric PS), BTU/h and tons of refrigeration.',
 keywords=['kw to hp','hp to kw','power converter','btu/h to kw','tons of refrigeration','horsepower converter'],
 family='power', default=1, units=[('kW','Kilowatts (kW)'),('hp','Horsepower (hp, mechanical)'),('PS','Metric horsepower (PS)'),('W','Watts (W)'),('BTUh','BTU per hour'),('TR','Tons of refrigeration (TR)'),('MW','Megawatts (MW)')],
 how='Type a power in **any** unit and the others update instantly. Useful for motors, engines, air conditioners and heaters.',
 formula='1 kW = 1.341 hp = 1.360 PS = 3,412 BTU/h   1 TR = 3.517 kW = 12,000 BTU/h',
 example='**Example:** an 11 kW motor is **14.75 hp**. A 1.5-ton air conditioner is 1.5 × 3.517 = **5.28 kW** of cooling (18,000 BTU/h).',
 table=dict(pair=('kW','hp'),h=('kW','hp'),values=[0.75,1.5,2.2,4,5.5,7.5,11,15,22,37,55,75,110]),
 table2=dict(pair=('TR','kW'),h=('Tons (AC)','kW cooling'),values=[0.75,1,1.5,2,3,5]),
 extra='''## hp vs PS

Mechanical (imperial) horsepower is 745.7 W. Metric horsepower (PS, CV, pk) is 735.5 W — about 1.4% smaller. Car brochures in Europe and Asia often quote PS.

## Air conditioner sizes

AC capacity is often given in tons or BTU/h of **cooling**. The electrical power drawn is much lower — divide the cooling kW by the unit's efficiency (EER/COP, often 3–4).''',
 faq=[('How many hp is 1 kW?','1.341 mechanical hp (1.360 metric PS).'),('How many kW is 1 hp?','0.7457 kW.'),('How many BTU/h is 1 ton of AC?','12,000 BTU/h, or 3.517 kW.')],
 related=['conversion/energy-converter','engineering/three-phase-motor-power','engineering/pump-power']))

C.append(dict(slug='flow-rate-converter', title='Flow Rate Converter',
 desc='Convert volumetric flow between m³/h, L/min, L/s, US gpm, CFM and m³/s — for pumps, pipes and flow meters.',
 keywords=['flow rate converter','m3/h to l/min','gpm to m3/h','cfm converter','l/s to m3/h','flow unit conversion'],
 family='flow', default=10, units=[('m3h','Cubic metres per hour (m³/h)'),('Lmin','Litres per minute (L/min)'),('Ls','Litres per second (L/s)'),('gpm','US gallons per minute (gpm)'),('cfm','Cubic feet per minute (CFM)'),('m3s','Cubic metres per second (m³/s)')],
 how='Type a flow rate in **any** unit and the others update instantly — handy for pump curves, flow meter ranges and datasheets.',
 formula='1 m³/h = 16.667 L/min = 4.403 US gpm = 0.5886 CFM',
 example='**Example:** a pump rated 10 m³/h delivers **166.7 L/min** or **44.0 US gpm**.',
 table=dict(pair=('m3h','Lmin'),h=('m³/h','L/min'),values=[0.1,0.5,1,2,5,10,25,50,100]),
 table2=dict(pair=('gpm','m3h'),h=('US gpm','m³/h'),values=[1,5,10,20,50,100,500]),
 extra='''## Liquids vs gases

For liquids, volumetric flow is straightforward. For gases, volume changes with pressure and temperature, so flows are often quoted at reference conditions — **Nm³/h** (normal) or **SCFM** (standard). This converter changes units only; it does not correct for pressure or temperature.

## Need mass flow?

Multiply by density to get kg/h — use the [mass flow rate calculator](/engineering/mass-flow-rate/).''',
 faq=[('How many L/min is 1 m³/h?','16.667 L/min.'),('How many m³/h is 1 US gpm?','0.2271 m³/h.'),('What does CFM mean?','Cubic feet per minute, common for air flow in HVAC and compressors.')],
 related=['engineering/pipe-flow-velocity','engineering/mass-flow-rate','conversion/volume-converter']))

C.append(dict(slug='torque-converter', title='Torque Converter (N·m to lb·ft)',
 desc='Convert torque between N·m, kN·m, lbf·ft, lbf·in and kgf·m — for bolts, engines and motors.',
 keywords=['torque converter','nm to lb ft','ft lbs to nm','torque wrench','kgf m to nm','torque units'],
 family='torque', default=100, units=[('Nm','Newton-metres (N·m)'),('lbft','Pound-force feet (lbf·ft)'),('lbin','Pound-force inches (lbf·in)'),('kgfm','Kilogram-force metres (kgf·m)'),('kNm','Kilonewton-metres (kN·m)')],
 how='Type a torque value in **any** unit and the others update instantly — useful for torque wrench settings, bolt specs and motor data.',
 formula='1 N·m = 0.73756 lbf·ft = 8.8507 lbf·in   1 kgf·m = 9.80665 N·m',
 example='**Example:** a wheel nut spec of 110 N·m = **81.1 lbf·ft**. 25 lbf·in for a small fastener = **2.82 N·m**.',
 table=dict(pair=('Nm','lbft'),h=('N·m','lbf·ft'),values=[5,10,25,50,80,100,120,150,200,300]),
 table2=dict(pair=('lbft','Nm'),h=('lbf·ft','N·m'),values=[10,20,50,75,100,150,250]),
 extra='''## lbf·ft vs "ft-lbs"

Torque is often written "ft-lbs" on wrenches and manuals; strictly, foot-pounds is a unit of energy, but in torque specs the two mean the same thing.

## Torque and motors

For motors, torque links power and speed: T (N·m) = 9549 × P (kW) ÷ rpm. Use the [torque, power & speed calculator](/engineering/torque-power-speed/).''',
 faq=[('How many lbf·ft is 1 N·m?','0.737562 lbf·ft.'),('How many N·m is 1 lbf·ft?','1.35582 N·m.'),('How do I convert lbf·in to lbf·ft?','Divide by 12.')],
 related=['engineering/torque-power-speed','conversion/power-converter']))
