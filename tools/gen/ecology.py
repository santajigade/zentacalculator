import math
from page import page
C='ecology'; U='updated: 2026-10-27'

page(C,'car-carbon-footprint',f'''
title: Car Carbon Footprint Calculator
description: Estimate CO₂ emissions from driving based on distance, fuel consumption and fuel type.
category: ecology
keywords: [car carbon footprint, co2 emissions car, driving emissions, petrol co2 per litre, diesel emissions, g co2 per km]
{U}
featured: true
variables:
  - id: ef
    label: Fuel
    default: 2.31
    options:
      - {{ label: Petrol / gasoline (2.31 kg CO₂ per litre), value: 2.31 }}
      - {{ label: Diesel (2.68 kg CO₂ per litre), value: 2.68 }}
      - {{ label: LPG (1.51 kg CO₂ per litre), value: 1.51 }}
  - {{ id: d, label: Distance per year, family: length, unit: km, imperialUnit: mi, default: 12000, min: 0 }}
  - {{ id: c, label: Fuel consumption, suffix: L/100 km, default: 7, min: 0 }}
  - {{ id: fuel, label: Fuel used, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: co2, label: CO₂ emitted, family: mass, unit: t, imperialUnit: lb, min: 0 }}
  - {{ id: gkm, label: CO₂ per km, suffix: g/km, min: 0, decimals: 0 }}
equations:
  - fuel = d / 1000 * c / 100 / 1000
  - co2 = fuel * 1000 * ef
  - gkm = c * ef * 10
faq:
  - q: How much CO₂ does a litre of petrol produce?
    a: Burning one litre of petrol releases about 2.3 kg of CO₂; diesel about 2.7 kg. This calculator covers tailpipe emissions only.
  - q: What is a typical car's footprint?
    a: A car using 7 L/100 km for 12,000 km a year emits about 1.9 tonnes of CO₂.
  - q: How can I reduce it?
    a: Drive less, combine trips, keep tyres inflated, drive smoothly, and choose a more efficient or electric vehicle.
related: [ecology/ev-vs-petrol, ecology/tree-offset, everyday-life/fuel-cost]
''','''
## How to use this calculator

Choose the **fuel**, then enter your **yearly distance** and **fuel consumption**. Fuel used, total CO₂ and grams of CO₂ per km are calculated.

## Formulas

<p class="formula">Fuel = distance × consumption ÷ 100<br/>CO₂ = fuel × emission factor</p>

## Example

12,000 km a year at 7 L/100 km (petrol):

- Fuel = **840 L**
- CO₂ = 840 × 2.31 = **1.94 t**
- About **162 g CO₂/km**

Factors are for fuel combustion only; the full life cycle (fuel production, car manufacture) adds more.
''')

page(C,'electricity-co2',f'''
title: Electricity CO₂ Emissions Calculator
description: Calculate the carbon emissions from your electricity use with your grid's emission factor.
category: ecology
keywords: [electricity carbon footprint, kwh to co2, grid emission factor, carbon emissions electricity, home energy co2]
{U}
variables:
  - {{ id: kwh, label: Electricity used per month, suffix: kWh, default: 300, min: 0 }}
  - {{ id: ef, label: Grid emission factor, suffix: kg CO₂/kWh, default: 0.7, min: 0 }}
  - {{ id: m, label: CO₂ per month, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
  - {{ id: y, label: CO₂ per year, family: mass, unit: t, imperialUnit: lb, min: 0 }}
equations:
  - m = kwh * ef
  - y = m * 12
faq:
  - q: What is a grid emission factor?
    a: The average CO₂ released per kWh of electricity generated in a region. It depends on how much coal, gas, nuclear and renewable power is used.
  - q: What factor should I use?
    a: Use your utility's or national figure. Coal-heavy grids are around 0.7–0.9 kg/kWh; grids with lots of renewables or nuclear can be below 0.1.
  - q: Does rooftop solar count as zero?
    a: Solar electricity has very low operating emissions, so exported or self-used solar reduces your grid footprint.
related: [ecology/solar-output, ecology/led-savings, everyday-life/electricity-cost]
''','''
## How to use this calculator

Enter your **monthly electricity use** (from your bill) and your **grid emission factor**. Monthly and yearly CO₂ are calculated.

## Example

300 kWh a month at 0.7 kg/kWh → **210 kg** per month, **2.5 t** per year.

## Approximate grid factors (recent years)

| Grid | kg CO₂ per kWh |
|---|---|
| India | ~0.7 |
| World average | ~0.45–0.5 |
| United States | ~0.35–0.4 |
| United Kingdom | ~0.2 |
| France | ~0.05 |

Factors change every year as grids decarbonise — check your national energy agency for the latest value.
''')

page(C,'flight-emissions',f'''
title: Flight Carbon Emissions Calculator
description: Estimate CO₂ emissions per passenger for a flight from distance, cabin class and non-CO₂ effects.
category: ecology
keywords: [flight emissions calculator, flight carbon footprint, co2 per flight, air travel emissions, radiative forcing]
{U}
variables:
  - {{ id: d, label: Flight distance (one way), family: length, unit: km, imperialUnit: mi, default: 6000, min: 0 }}
  - {{ id: trips, label: Number of one-way flights, default: 2, min: 0 }}
  - {{ id: ef, label: Emission factor (economy), suffix: kg CO₂ per passenger-km, default: 0.15, min: 0 }}
  - id: cls
    label: Cabin class
    default: 1
    options:
      - {{ label: Economy (×1), value: 1 }}
      - {{ label: Premium economy (×1.6), value: 1.6 }}
      - {{ label: Business (×2.9), value: 2.9 }}
      - {{ label: First (×4), value: 4 }}
  - id: rf
    label: Include non-CO₂ warming effects?
    default: 1
    options:
      - {{ label: No (CO₂ only), value: 1 }}
      - {{ label: Yes (×1.9 multiplier), value: 1.9 }}
  - {{ id: co2, label: Emissions, family: mass, unit: t, imperialUnit: lb, min: 0 }}
equations:
  - co2 = d / 1000 * trips * ef * cls * rf
faq:
  - q: How much CO₂ does a flight produce per passenger?
    a: Roughly 0.1–0.25 kg of CO₂ per passenger-km in economy, depending on distance, aircraft and load factor.
  - q: Why does cabin class matter?
    a: Premium seats take more cabin space, so each passenger is responsible for a bigger share of the plane's fuel.
  - q: What is the non-CO₂ multiplier?
    a: Contrails and nitrogen oxides at altitude add extra warming. Some methods multiply CO₂ by about 1.9 to include them; the exact effect is still debated.
related: [ecology/tree-offset, ecology/carbon-offset-cost]
''','''
## How to use this calculator

Enter the **distance** and **number of one-way flights**, an **emission factor**, your **cabin class**, and whether to include **non-CO₂ effects**. Your share of the emissions is calculated.

## Example

A 6,000 km return trip (2 flights) in economy at 0.15 kg/pkm:

- CO₂ only: 6,000 × 2 × 0.15 = **1.8 t**
- With non-CO₂ effects (×1.9): **3.4 t**

Emission factors depend on the method and source; government conversion factors (such as the UK's DESNZ) are updated yearly.
''')

page(C,'tree-offset',f'''
title: Trees to Offset CO₂ Calculator
description: Estimate how many trees it would take to absorb a given amount of CO₂ per year.
category: ecology
keywords: [trees to offset co2, carbon offset trees, how many trees, tree co2 absorption, carbon sequestration]
{U}
variables:
  - {{ id: co2, label: CO₂ to offset per year, family: mass, unit: t, imperialUnit: lb, default: 2, min: 0 }}
  - {{ id: per, label: CO₂ absorbed per tree per year, family: mass, unit: kg, imperialUnit: lb, default: 21, min: 0.0001 }}
  - {{ id: n, label: Trees needed, min: 0, decimals: 0 }}
equations:
  - n = ceil(co2 / per)
faq:
  - q: How much CO₂ does a tree absorb?
    a: A commonly quoted average is about 21 kg per year for a mature tree, but it varies hugely with species, age, climate and soil.
  - q: Do newly planted trees absorb that much?
    a: No. Young trees absorb much less; it can take decades to reach mature rates.
  - q: Is planting trees enough?
    a: Trees help, but reducing emissions at the source is far more effective. Offsets work best as a complement.
related: [ecology/car-carbon-footprint, ecology/flight-emissions]
''','''
## How to use this calculator

Enter the **CO₂ you want to offset each year** and the **CO₂ absorbed per tree**. The number of mature trees needed is calculated.

## Example

2 tonnes of CO₂ per year at 21 kg per tree → **96 trees**.

The 21 kg figure is a rough average for a mature tree; fast-growing tropical trees can absorb more, and young trees much less.
''')

page(C,'rainwater-harvesting',f'''
title: Rainwater Harvesting Calculator
description: Calculate how much rainwater you can collect from a roof based on area, rainfall and runoff coefficient.
category: ecology
keywords: [rainwater harvesting calculator, roof rainwater, rainwater collection, tank size, runoff coefficient]
{U}
featured: true
variables:
  - {{ id: A, label: Roof (catchment) area, family: area, unit: m2, imperialUnit: ft2, default: 100, min: 0 }}
  - {{ id: R, label: Annual rainfall, family: length, unit: mm, imperialUnit: in, default: 800, min: 0 }}
  - id: k
    label: Roof type (runoff coefficient)
    default: 0.85
    options:
      - {{ label: Metal sheet (0.9), value: 0.9 }}
      - {{ label: Tiles / concrete (0.85), value: 0.85 }}
      - {{ label: Asphalt shingles (0.8), value: 0.8 }}
      - {{ label: Gravel / green roof (0.5), value: 0.5 }}
  - {{ id: V, label: Water collected per year, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: day, label: Average per day, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
equations:
  - V = A * R * k
  - day = V / 365
faq:
  - q: How much rainwater can I collect?
    a: About 1 litre per m² of roof for every mm of rain, multiplied by a runoff coefficient. 100 m² with 800 mm of rain gives about 68,000 litres a year.
  - q: What is a runoff coefficient?
    a: The share of rain that actually reaches the gutters after splash, evaporation and absorption.
  - q: How big should my tank be?
    a: It depends on rainfall pattern and use. In monsoon climates, size the tank for the dry months you need to cover.
related: [ecology/garden-irrigation, construction/rectangular-tank]
''','''
## How to use this calculator

Enter the **roof area**, **annual rainfall** and choose the **roof type**. Yearly and average daily collection are calculated.

## Formula

<p class="formula">Volume = area × rainfall × runoff coefficient</p>

## Example

100 m² concrete roof, 800 mm annual rain: 100 × 0.8 × 0.85 = 68 m³ = **68,000 litres** a year (about 186 L per day on average).

Discard the "first flush" of each rain to keep debris out of the tank, and check local rules on using rainwater.
''')

page(C,'solar-output',f'''
title: Solar Panel Output Calculator
description: Estimate daily, monthly and yearly energy from a solar PV system based on size, sun hours and system losses.
category: ecology
keywords: [solar panel output, solar kwh per day, solar energy calculator, peak sun hours, pv generation]
{U}
featured: true
variables:
  - {{ id: kw, label: System size, suffix: kWp, default: 3, min: 0 }}
  - {{ id: psh, label: Peak sun hours per day, suffix: hours, default: 5, min: 0, max: 12 }}
  - {{ id: pr, label: Performance ratio (after losses), family: percent, unit: '%', default: 75, min: 0, max: 1 }}
  - {{ id: d, label: Energy per day, suffix: kWh, min: 0, decimals: 1 }}
  - {{ id: m, label: Energy per month, suffix: kWh, min: 0, decimals: 0 }}
  - {{ id: y, label: Energy per year, suffix: kWh, min: 0, decimals: 0 }}
equations:
  - d = kw * psh * pr
  - m = d * 30
  - y = d * 365
faq:
  - q: How much energy does a 1 kW solar system produce?
    a: About 3–5 kWh per day in many places — roughly 1,100–1,800 kWh per year depending on location.
  - q: What are peak sun hours?
    a: The equivalent hours of full 1,000 W/m² sunshine per day. Northern Europe has about 2–3; India, Australia and the US Southwest often 5–6.
  - q: What reduces output?
    a: Heat, dust, shading, wiring and inverter losses. A performance ratio of 75–85% is typical.
related: [ecology/solar-system-size, ecology/battery-storage, ecology/electricity-co2]
''','''
## How to use this calculator

Enter the **system size** in kWp, your location's **peak sun hours** and a **performance ratio**. Daily, monthly and yearly energy are estimated.

## Formula

<p class="formula">kWh/day = kWp × peak sun hours × performance ratio</p>

## Example

A 3 kWp system with 5 peak sun hours at 75%:

- **11.3 kWh/day**
- **338 kWh/month**
- **4,106 kWh/year**
''')

page(C,'solar-system-size',f'''
title: Solar System Size Calculator
description: Work out the solar PV system size (kWp) and number of panels needed to cover your electricity use.
category: ecology
keywords: [solar system size, how many solar panels, solar sizing, kw solar needed, rooftop solar calculator]
{U}
variables:
  - {{ id: use, label: Monthly electricity use, suffix: kWh, default: 400, min: 0 }}
  - {{ id: psh, label: Peak sun hours per day, suffix: hours, default: 5, min: 0.1 }}
  - {{ id: pr, label: Performance ratio, family: percent, unit: '%', default: 75, min: 0.01, max: 1 }}
  - {{ id: pw, label: Panel rating, suffix: W, default: 450, min: 1 }}
  - {{ id: kw, label: System size needed, suffix: kWp, min: 0, decimals: 2 }}
  - {{ id: n, label: Number of panels, min: 0, decimals: 0 }}
  - {{ id: area, label: Approx. roof area (panels only), family: area, unit: m2, imperialUnit: ft2, min: 0 }}
equations:
  - kw = use / 30 / (psh * pr)
  - n = ceil(kw * 1000 / pw)
  - area = n * 2.2
faq:
  - q: How many solar panels do I need?
    a: Divide daily use by (peak sun hours × performance ratio) to get kWp, then divide by the panel rating.
  - q: How much roof space does a panel need?
    a: A typical 400–450 W panel is about 2 m² (around 2.0 × 1.1 m).
  - q: Should I cover 100% of my use?
    a: It depends on local net-metering rules and budget. Many systems are sized to cover 70–100% of yearly use.
related: [ecology/solar-output, ecology/battery-storage]
''','''
## How to use this calculator

Enter your **monthly electricity use**, local **peak sun hours**, **performance ratio** and **panel rating**. The system size, panel count and approximate roof area are calculated.

## Example

400 kWh a month, 5 sun hours, 75% PR, 450 W panels:

- System = 13.3 ÷ 3.75 = **3.56 kWp**
- Panels = **8**
- Roof area ≈ **17.6 m²**
''')

page(C,'shower-water',f'''
title: Shower Water & Energy Calculator
description: Calculate how much water and energy your showers use — and what a low-flow head or shorter shower saves.
category: ecology
keywords: [shower water usage, litres per shower, water saving, low flow shower head, shower energy cost]
{U}
variables:
  - {{ id: t, label: Shower length, suffix: minutes, default: 8, min: 0 }}
  - {{ id: f, label: Flow rate, family: flow, unit: Lmin, imperialUnit: gpm, default: 10, min: 0 }}
  - {{ id: n, label: Showers per week (household), default: 21, min: 0 }}
  - {{ id: per, label: Water per shower, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: yr, label: Water per year, family: volume, unit: m3, imperialUnit: galUS, min: 0 }}
  - {{ id: kwh, label: Energy to heat it (per year, ΔT 25 °C), suffix: kWh, min: 0, decimals: 0 }}
equations:
  - per = f * t * 60
  - yr = per * n * 52
  - kwh = yr * 1000 * 4.186 * 25 / 3600
faq:
  - q: How much water does a shower use?
    a: About 8–12 litres per minute for a standard shower head and 6–8 for a low-flow head.
  - q: How much energy does heating shower water take?
    a: Raising water by 25 °C takes about 0.03 kWh per litre — about 2.3 kWh for an 80-litre shower.
  - q: How do I measure my flow rate?
    a: Time how long it takes to fill a 5-litre bucket. 30 seconds means 10 L/min.
related: [ecology/water-leak, everyday-life/electricity-cost, chemistry/specific-heat]
''','''
## How to use this calculator

Enter the **shower length**, **flow rate** and **showers per week**. Water per shower, per year and the energy to heat it are calculated.

## Example

8-minute showers at 10 L/min, 21 per week:

- **80 L** per shower
- **87 m³** per year
- About **2,530 kWh** a year to heat (25 °C rise)

Switching to a 7 L/min head cuts water and heating energy by 30%.
''')

page(C,'mark-recapture',f'''
title: Mark–Recapture Population Estimator (Lincoln–Petersen)
description: Estimate an animal population size from mark and recapture counts using the Lincoln–Petersen and Chapman methods.
category: ecology
keywords: [mark recapture, lincoln petersen, population estimate, capture recapture, chapman estimator, wildlife survey]
{U}
featured: true
variables:
  - {{ id: M, label: Animals marked in first sample, default: 50, min: 0 }}
  - {{ id: Cc, label: Animals caught in second sample, default: 40, min: 0 }}
  - {{ id: R, label: Marked animals recaptured, default: 8, min: 0.0001 }}
  - {{ id: N, label: Population estimate (Lincoln–Petersen), min: 0, decimals: 0 }}
  - {{ id: Nc, label: Population estimate (Chapman), min: 0, decimals: 0 }}
equations:
  - N = M * Cc / R
  - Nc = (M + 1) * (Cc + 1) / (R + 1) - 1
faq:
  - q: How does mark–recapture work?
    a: Mark a sample, release it, then take a second sample. The share of marked animals in the second sample estimates the share marked in the whole population.
  - q: Why use the Chapman estimator?
    a: It is less biased when the number recaptured is small.
  - q: What assumptions are made?
    a: A closed population (no births, deaths or migration between samples), marks are not lost, and marked animals are equally likely to be caught.
related: [ecology/population-density, biology/logistic-growth]
''','''
## How to use this calculator

Enter the number **marked** in the first sample, the number **caught** in the second, and how many of those were **recaptured** (already marked). Both population estimates are calculated.

## Formulas

<p class="formula">Lincoln–Petersen: N = M C ÷ R<br/>Chapman: N = (M + 1)(C + 1) ÷ (R + 1) − 1</p>

## Example

50 marked, 40 caught later, 8 recaptured:

- Lincoln–Petersen = **250**
- Chapman = 51 × 41 ÷ 9 − 1 = **231**
''')

page(C,'population-density',f'''
title: Population Density Calculator
description: Calculate population density (individuals per km², hectare or square mile) from count and area.
category: ecology
keywords: [population density, people per square km, density calculator, animals per hectare, density per area]
{U}
variables:
  - {{ id: n, label: Population (count), default: 1250000, min: 0 }}
  - {{ id: A, label: Area, family: area, unit: km2, imperialUnit: acre, default: 450, min: 0 }}
  - {{ id: dk, label: Density per km², min: 0, decimals: 1 }}
  - {{ id: dm, label: Density per square mile, min: 0, decimals: 1 }}
  - {{ id: dh, label: Density per hectare, min: 0, decimals: 2 }}
equations:
  - dk = n / A * 1000000
  - dm = dk * 2.589988
  - dh = dk / 100
faq:
  - q: How is population density calculated?
    a: Divide the number of individuals by the area they occupy.
  - q: How do I convert per km² to per square mile?
    a: Multiply by 2.59.
  - q: Is density the same everywhere in an area?
    a: No — it is an average. Cities and habitats are often much denser in some places than others.
related: [ecology/mark-recapture, conversion/area-converter]
''','''
## How to use this calculator

Enter the **population** and the **area**. Density per km², per square mile and per hectare are calculated.

## Example

1,250,000 people in 450 km²:

- **2,778 per km²**
- **7,194 per square mile**
- **27.8 per hectare**
''')

page(C,'led-savings',f'''
title: LED Bulb Savings Calculator
description: Calculate energy, money and CO₂ saved by replacing old bulbs with LEDs.
category: ecology
keywords: [led savings calculator, led vs incandescent, light bulb energy savings, cfl vs led, lighting cost]
{U}
variables:
  - {{ id: ow, label: Old bulb power, family: power, unit: W, default: 60, min: 0 }}
  - {{ id: nw, label: LED power, family: power, unit: W, default: 9, min: 0 }}
  - {{ id: n, label: Number of bulbs, default: 10, min: 0 }}
  - {{ id: h, label: Hours on per day, suffix: hours, default: 5, min: 0, max: 24 }}
  - {{ id: r, label: Electricity price per kWh, family: currency, default: 0.15, min: 0, decimals: 3 }}
  - {{ id: ef, label: Grid emission factor, suffix: kg CO₂/kWh, default: 0.5, min: 0 }}
  - {{ id: kwh, label: Energy saved per year, suffix: kWh, min: 0, decimals: 0 }}
  - {{ id: sav, label: Money saved per year, family: currency, min: 0, decimals: 2 }}
  - {{ id: co2, label: CO₂ avoided per year, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - kwh = (ow - nw) * n * h * 365 / 1000
  - sav = kwh * r
  - co2 = kwh * ef
faq:
  - q: How much energy do LEDs save?
    a: About 80–90% compared with incandescent bulbs for the same light output.
  - q: What LED replaces a 60 W bulb?
    a: An LED of about 8–10 W gives similar brightness (around 800 lumens).
  - q: How long do LEDs last?
    a: Typically 15,000–25,000 hours, versus about 1,000 for incandescent bulbs.
related: [ecology/electricity-co2, everyday-life/electricity-cost]
''','''
## How to use this calculator

Enter the **old** and **LED** wattages, **number of bulbs**, **hours per day**, **electricity price** and **grid emission factor**. Yearly energy, money and CO₂ savings are calculated.

## Example

10 bulbs, 60 W → 9 W, 5 hours a day:

- Energy saved = **931 kWh/year**
- Money saved at 0.15/kWh = **139.62**
- CO₂ avoided at 0.5 kg/kWh = **465 kg**
''')

page(C,'water-leak',f'''
title: Water Leak (Dripping Tap) Calculator
description: Estimate how much water a dripping tap or leak wastes per day and per year.
category: ecology
keywords: [dripping tap water waste, water leak calculator, drips per minute, leaking faucet, water wastage]
{U}
variables:
  - {{ id: dpm, label: Drips per minute, default: 30, min: 0 }}
  - {{ id: ml, label: Volume per drip, suffix: ml, default: 0.25, min: 0 }}
  - {{ id: day, label: Water wasted per day, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: yr, label: Water wasted per year, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
equations:
  - day = dpm * ml * 1440 / 1000000
  - yr = day * 365
faq:
  - q: How much water does a dripping tap waste?
    a: At one drip every two seconds (30 per minute), about 10 litres a day or over 3,900 litres a year.
  - q: How big is a drip?
    a: Commonly estimated at about 0.25 ml (around 4,000 drips per litre), though it varies.
  - q: How do I fix a dripping tap?
    a: Most drips are caused by a worn washer or cartridge, which is an inexpensive fix.
related: [ecology/shower-water, ecology/rainwater-harvesting]
''','''
## How to use this calculator

Count the **drips per minute** and enter an estimated **volume per drip**. Water wasted per day and per year is calculated.

## Example

30 drips per minute at 0.25 ml: **10.8 L/day**, **3,942 L/year**.
''')

page(C,'compost-ratio',f'''
title: Compost C:N Ratio Calculator
description: Calculate the carbon-to-nitrogen ratio of a mix of two compost materials — greens and browns.
category: ecology
keywords: [compost calculator, carbon nitrogen ratio, c:n ratio, greens and browns, compost mix]
{U}
variables:
  - {{ id: m1, label: Brown material weight (e.g. dry leaves), family: mass, unit: kg, imperialUnit: lb, default: 10, min: 0 }}
  - {{ id: c1, label: Brown carbon content, family: percent, unit: '%', default: 50, min: 0, max: 1 }}
  - {{ id: n1, label: Brown nitrogen content, family: percent, unit: '%', default: 0.8, min: 0, max: 1 }}
  - {{ id: m2, label: Green material weight (e.g. food scraps), family: mass, unit: kg, imperialUnit: lb, default: 15, min: 0 }}
  - {{ id: c2, label: Green carbon content, family: percent, unit: '%', default: 40, min: 0, max: 1 }}
  - {{ id: n2, label: Green nitrogen content, family: percent, unit: '%', default: 2.5, min: 0, max: 1 }}
  - {{ id: cn, label: Mix C:N ratio (x : 1), min: 0, decimals: 1 }}
equations:
  - cn = (m1 * c1 + m2 * c2) / (m1 * n1 + m2 * n2)
faq:
  - q: What is the ideal C:N ratio for compost?
    a: About 25–30 : 1. Too much carbon composts slowly; too much nitrogen can smell of ammonia.
  - q: What are greens and browns?
    a: Greens (food scraps, grass) are nitrogen-rich; browns (dry leaves, straw, cardboard) are carbon-rich.
  - q: Where do I find carbon and nitrogen content?
    a: Use published tables for common materials. Dry leaves are often 40–80 : 1, food scraps about 15 : 1.
related: [ecology/garden-irrigation]
''','''
## How to use this calculator

Enter the **weight**, **carbon %** and **nitrogen %** of a brown and a green material. The C:N ratio of the mix is calculated. Adjust the weights until you reach about 25–30.

## Formula

<p class="formula">C:N = (m₁C₁ + m₂C₂) ÷ (m₁N₁ + m₂N₂)</p>

## Example

10 kg leaves (50% C, 0.8% N) + 15 kg food scraps (40% C, 2.5% N):

C:N = (5 + 6) ÷ (0.08 + 0.375) = **24.2 : 1**
''')

page(C,'ev-vs-petrol',f'''
title: EV vs Petrol Car Running Cost Calculator
description: Compare the energy cost per km and per year of an electric car against a petrol or diesel car.
category: ecology
keywords: [ev vs petrol cost, electric car running cost, cost per km ev, ev savings calculator, charging cost]
{U}
featured: true
variables:
  - {{ id: d, label: Distance per year, family: length, unit: km, imperialUnit: mi, default: 12000, min: 0 }}
  - {{ id: ev, label: EV consumption, suffix: kWh/100 km, default: 16, min: 0 }}
  - {{ id: pe, label: Electricity price per kWh, family: currency, default: 0.15, min: 0, decimals: 3 }}
  - {{ id: ic, label: Petrol car consumption, suffix: L/100 km, default: 7, min: 0 }}
  - {{ id: pf, label: Fuel price per litre, family: currency, default: 1.6, min: 0, decimals: 3 }}
  - {{ id: cev, label: EV energy cost per year, family: currency, min: 0, decimals: 2 }}
  - {{ id: cic, label: Petrol cost per year, family: currency, min: 0, decimals: 2 }}
  - {{ id: sav, label: Yearly saving with EV, family: currency, decimals: 2 }}
equations:
  - cev = d / 1000 / 100 * ev * pe
  - cic = d / 1000 / 100 * ic * pf
  - sav = cic - cev
faq:
  - q: Is an electric car cheaper to run?
    a: Usually, per km — especially when charging at home. Public fast charging can cost several times more.
  - q: What is typical EV efficiency?
    a: About 14–20 kWh per 100 km for most cars, more in winter or at high speed.
  - q: Does this include maintenance and purchase price?
    a: No — energy cost only. EVs often have lower maintenance but may cost more to buy.
related: [ecology/car-carbon-footprint, everyday-life/fuel-cost]
''','''
## How to use this calculator

Enter yearly **distance**, the EV's **consumption** and **electricity price**, and the petrol car's **consumption** and **fuel price**. Yearly energy costs and savings are calculated.

## Example

12,000 km a year; EV at 16 kWh/100 km and 0.15/kWh; petrol at 7 L/100 km and 1.60/L:

- EV = **288**
- Petrol = **1,344**
- Saving = **1,056** per year

Charging losses (about 10%) are not included — add them to the EV consumption for a closer estimate.
''')

A=math.pi*40**2
page(C,'wind-turbine-power',f'''
title: Wind Turbine Power Calculator
description: Calculate wind turbine power from rotor diameter, wind speed, air density and power coefficient.
category: ecology
keywords: [wind turbine power, wind power calculator, p = 1/2 rho a v3, betz limit, wind energy, rotor diameter]
{U}
variables:
  - {{ id: D, label: Rotor diameter, family: length, unit: m, imperialUnit: ft, default: 80, min: 0 }}
  - {{ id: v, label: Wind speed, family: velocity, unit: ms, imperialUnit: mph, default: 8, min: 0 }}
  - {{ id: rho, label: Air density, family: density, unit: kgm3, default: 1.225, min: 0 }}
  - {{ id: cp, label: Power coefficient (Cp), default: 0.4, min: 0, max: 0.593 }}
  - {{ id: P, label: Power output, family: power, unit: kW, imperialUnit: hp, min: 0 }}
equations:
  - P = 0.5 * rho * pi * (D / 2)^2 * v^3 * cp
chart: {{ x: v, y: P, from: 0, to: 15 }}
faq:
  - q: How is wind power calculated?
    a: P = ½ ρ A v³ Cp — the power rises with the cube of wind speed and the square of rotor diameter.
  - q: What is the Betz limit?
    a: No turbine can capture more than 59.3% (16/27) of the wind's energy. Modern turbines reach about 40–50%.
  - q: Why does wind speed matter so much?
    a: Doubling the wind speed gives eight times the power, which is why turbine siting is crucial.
related: [ecology/solar-output, physics/kinetic-energy]
''',f'''
## How to use this calculator

Enter the **rotor diameter**, **wind speed**, **air density** and **power coefficient**. The power output is calculated (before generator limits).

## Formula

<p class="formula">P = ½ ρ A v³ C<sub>p</sub></p>

## Example

80 m rotor, 8 m/s wind, ρ = 1.225, Cp = 0.4:

P = 0.5 × 1.225 × {A:.0f} × 512 × 0.4 = **{0.5*1.225*A*512*0.4/1000:.0f} kW**

Real turbines cap output at their rated power (for example 2 MW) above the rated wind speed.
''')

page(C,'carbon-offset-cost',f'''
title: Carbon Offset Cost Calculator
description: Calculate the cost of offsetting your emissions at a given carbon price per tonne.
category: ecology
keywords: [carbon offset cost, carbon credit price, offset calculator, cost per tonne co2, carbon pricing]
{U}
variables:
  - {{ id: t, label: Emissions to offset, family: mass, unit: t, imperialUnit: lb, default: 5, min: 0 }}
  - {{ id: p, label: Price per tonne CO₂, family: currency, default: 15, min: 0, decimals: 2 }}
  - {{ id: cost, label: Offset cost, family: currency, min: 0, decimals: 2 }}
  - {{ id: m, label: Per month, family: currency, min: 0, decimals: 2 }}
equations:
  - cost = t / 1000 * p
  - m = cost / 12
faq:
  - q: How much does a carbon offset cost?
    a: Voluntary offsets range widely — from a few to over 100 per tonne — depending on the project type and quality.
  - q: Are all offsets equal?
    a: No. Look for independently verified projects (for example Gold Standard or Verra) and check permanence and additionality.
  - q: Should I offset or reduce?
    a: Reduce first, then offset what you cannot avoid.
related: [ecology/flight-emissions, ecology/tree-offset, ecology/car-carbon-footprint]
''','''
## How to use this calculator

Enter the **emissions** to offset (yearly) and the **price per tonne**. The total and monthly cost are calculated.

## Example

5 tonnes at 15 per tonne → **75** a year (**6.25** a month).
''')

page(C,'pond-liner',f'''
title: Pond Liner Size & Volume Calculator
description: Calculate the pond liner size you need and the pond's water volume from length, width and depth.
category: ecology
keywords: [pond liner calculator, pond volume, garden pond, liner size, pond litres, wildlife pond]
{U}
variables:
  - {{ id: L, label: Pond length, family: length, unit: m, imperialUnit: ft, default: 3, min: 0 }}
  - {{ id: W, label: Pond width, family: length, unit: m, imperialUnit: ft, default: 2, min: 0 }}
  - {{ id: D, label: Maximum depth, family: length, unit: m, imperialUnit: ft, default: 0.6, min: 0 }}
  - {{ id: o, label: Overlap at each edge, family: length, unit: m, imperialUnit: ft, default: 0.3, min: 0 }}
  - {{ id: ll, label: Liner length, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: lw, label: Liner width, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: V, label: Approx. water volume (sloped sides), family: volume, unit: L, imperialUnit: galUS, min: 0 }}
equations:
  - ll = L + 2 * D + 2 * o
  - lw = W + 2 * D + 2 * o
  - V = L * W * D * 0.6
faq:
  - q: How do I calculate pond liner size?
    a: Liner length = pond length + 2 × depth + 2 × overlap; liner width = pond width + 2 × depth + 2 × overlap.
  - q: Why multiply volume by 0.6?
    a: Ponds have sloping sides and shelves, so they hold less than a rectangular box. 0.5–0.7 is a typical factor.
  - q: How deep should a wildlife pond be?
    a: Include shallow edges for wildlife and a deeper zone of about 60 cm so part of the pond stays ice-free in winter.
related: [construction/rectangular-tank, ecology/rainwater-harvesting]
''','''
## How to use this calculator

Enter the pond's **length**, **width**, **maximum depth** and the **overlap** you want around the edge. The liner size and approximate volume are calculated.

## Example

A 3 × 2 m pond, 0.6 m deep, 0.3 m overlap:

- Liner = **4.8 × 3.8 m**
- Volume ≈ **2,160 litres**
''')

page(C,'garden-irrigation',f'''
title: Garden Watering Calculator
description: Calculate how much water a lawn or garden needs per week and how long to run a sprinkler or hose.
category: ecology
keywords: [garden watering calculator, lawn water needs, irrigation calculator, how long to water, sprinkler time]
{U}
variables:
  - {{ id: A, label: Garden or lawn area, family: area, unit: m2, imperialUnit: ft2, default: 50, min: 0 }}
  - {{ id: mm, label: Water needed per week, family: length, unit: mm, imperialUnit: in, default: 25, min: 0 }}
  - {{ id: rain, label: Rainfall this week, family: length, unit: mm, imperialUnit: in, default: 5, min: 0 }}
  - {{ id: f, label: Hose or sprinkler flow, family: flow, unit: Lmin, imperialUnit: gpm, default: 12, min: 0.000001 }}
  - {{ id: V, label: Water to apply, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: t, label: Watering time, suffix: minutes, min: 0, decimals: 0 }}
equations:
  - V = A * max(0, mm - rain)
  - t = V / f / 60
faq:
  - q: How much water does a lawn need?
    a: About 25 mm (1 inch) per week in warm weather, including rainfall.
  - q: When is the best time to water?
    a: Early morning, when evaporation is lowest and leaves dry during the day.
  - q: How do I measure sprinkler output?
    a: Place a few straight-sided cans on the lawn and time how long it takes to collect 25 mm.
related: [ecology/rainwater-harvesting, ecology/shower-water]
''','''
## How to use this calculator

Enter the **area**, the **water needed per week**, this week's **rainfall** and your hose or sprinkler **flow rate**. The water to apply and the watering time are calculated.

## Example

50 m² lawn needing 25 mm, 5 mm of rain, 12 L/min hose:

- Water = 50 × 20 = **1,000 L**
- Time = **83 minutes** per week (for example, two sessions of about 40 minutes)
''')

page(C,'bike-vs-car',f'''
title: Bike vs Car Commute Savings Calculator
description: Calculate the money, CO₂ and calories saved by cycling instead of driving to work.
category: ecology
keywords: [bike vs car, cycling savings, commute by bike, co2 saved cycling, cycle to work calculator]
{U}
variables:
  - {{ id: d, label: One-way commute distance, family: length, unit: km, imperialUnit: mi, default: 8, min: 0 }}
  - {{ id: n, label: Days cycled per week, default: 3, min: 0, max: 7 }}
  - {{ id: ck, label: Car cost per km (fuel, wear, parking), family: currency, default: 0.25, min: 0, decimals: 3 }}
  - {{ id: g, label: Car CO₂ per km, suffix: g/km, default: 160, min: 0 }}
  - {{ id: km, label: Km cycled per year, family: length, unit: km, imperialUnit: mi, min: 0 }}
  - {{ id: sav, label: Money saved per year, family: currency, min: 0, decimals: 2 }}
  - {{ id: co2, label: CO₂ avoided per year, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
  - {{ id: kcal, label: Calories burned per year (≈30 kcal/km), suffix: kcal, min: 0, decimals: 0 }}
equations:
  - km = d * 2 * n * 46
  - sav = km / 1000 * ck
  - co2 = km / 1000 * g / 1000
  - kcal = km / 1000 * 30
faq:
  - q: How much can I save by cycling to work?
    a: An 8 km commute cycled 3 days a week saves about 2,200 km of driving a year — often hundreds in fuel, parking and wear.
  - q: How many calories does cycling burn?
    a: Roughly 25–40 kcal per km at a moderate pace, depending on weight and speed.
  - q: Why 46 weeks?
    a: To allow for holidays and bad-weather days. Adjust the days per week to fit your routine.
related: [ecology/car-carbon-footprint, health/calories-burned, sports/cycling-gear-speed]
''','''
## How to use this calculator

Enter your **one-way distance**, **days cycled per week**, the car's **cost per km** and **CO₂ per km**. Yearly distance, savings, CO₂ avoided and calories burned are calculated (46 working weeks).

## Example

8 km each way, 3 days a week:

- **2,208 km** cycled per year
- Saving at 0.25/km = **552**
- CO₂ avoided = **353 kg**
- About **66,000 kcal** burned
''')

page(C,'battery-storage',f'''
title: Solar Battery Storage Size Calculator
description: Calculate the battery capacity needed for backup or off-grid solar from daily load, autonomy days and depth of discharge.
category: ecology
keywords: [battery size calculator, solar battery storage, kwh battery needed, off grid battery, depth of discharge, inverter battery]
{U}
variables:
  - {{ id: load, label: Daily energy to cover, suffix: kWh, default: 6, min: 0 }}
  - {{ id: days, label: Days of autonomy, default: 1, min: 0 }}
  - {{ id: dod, label: Usable depth of discharge, family: percent, unit: '%', default: 90, min: 0.01, max: 1 }}
  - {{ id: eff, label: Round-trip efficiency, family: percent, unit: '%', default: 90, min: 0.01, max: 1 }}
  - {{ id: V, label: Battery bank voltage, family: voltage, unit: V, default: 48, min: 0.1 }}
  - {{ id: kwh, label: Battery capacity needed, suffix: kWh, min: 0, decimals: 1 }}
  - {{ id: ah, label: Capacity at bank voltage, suffix: Ah, min: 0, decimals: 0 }}
equations:
  - kwh = load * days / (dod * eff)
  - ah = kwh * 1000 / V
faq:
  - q: How big a battery do I need?
    a: Daily load × days of backup, divided by usable depth of discharge and efficiency.
  - q: What depth of discharge should I use?
    a: About 80–95% for lithium iron phosphate (LFP) batteries and about 50% for lead-acid to protect battery life.
  - q: How do I convert kWh to Ah?
    a: Ah = kWh × 1,000 ÷ battery voltage.
related: [ecology/solar-output, ecology/solar-system-size]
''','''
## How to use this calculator

Enter the **daily energy** you want covered, **days of autonomy**, usable **depth of discharge**, **round-trip efficiency** and the **battery bank voltage**. Capacity in kWh and Ah is calculated.

## Example

6 kWh a day, 1 day of backup, 90% DoD, 90% efficiency, 48 V bank:

- Capacity = 6 ÷ 0.81 = **7.4 kWh**
- = **154 Ah** at 48 V
''')
print('ecology ok')
