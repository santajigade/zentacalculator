import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
pi = math.pi

expand('ecology/battery-storage', '''
## Battery chemistries compared

| Chemistry | Usable depth of discharge | Cycle life (approx.) | Round-trip efficiency |
|---|---|---|---|
| Lead-acid (flooded) | 50% | 500–1,500 | 75–85% |
| AGM / gel lead-acid | 50–60% | 500–1,500 | 80–85% |
| Lithium iron phosphate (LFP) | 80–100% | 3,000–6,000+ | 90–95% |
| Lithium NMC | 80–90% | 1,000–3,000 | 90–95% |

LFP is now the most common choice for home solar storage because of its long life and safety.

## Capacity by daily load

1 day of autonomy, 80% DoD, 90% efficiency:

| Daily load | Battery needed | At 48 V |
|---|---|---|
''' + ''.join(f"| {l} kWh | {l/0.72:.1f} kWh | {l/0.72*1000/48:,.0f} Ah |\n" for l in [2, 4, 6, 10, 15, 20]) + '''
## Essential loads only

For backup during outages, many homes size the battery for **essential loads** only: lights, fridge, internet, fans and a few sockets. This can cut the battery size by half or more.

## Inverter size

The inverter must handle the highest power drawn at once, not the daily energy. A home with a 3 kW peak load needs at least a 3–4 kW inverter, with extra surge capacity for motor starts.

## Battery life in years

Cycle life ÷ cycles per year gives a rough lifetime. An LFP battery rated for 6,000 cycles, used once a day, could last over 15 years, though calendar ageing also reduces capacity.
''', [
 ('How many kWh battery do I need for my home?', 'Divide your daily energy need by DoD × efficiency. For 6 kWh a day with LFP (80% DoD, 90% efficiency), about 8.3 kWh.'),
 ('How do I convert kWh to Ah?', 'Ah = kWh × 1,000 ÷ battery voltage. 10 kWh at 48 V is about 208 Ah.'),
])

expand('ecology/bike-vs-car', '''
## Yearly impact by commute

3 days a week, 46 weeks, car at 0.30 per km and 160 g CO₂/km:

| One-way distance | Km cycled per year | Money saved | CO₂ avoided |
|---|---|---|---|
''' + ''.join(f"| {d} km | {d*2*3*46:,} | {d*2*3*46*0.3:,.0f} | {d*2*3*46*0.16:,.0f} kg |\n" for d in [3, 5, 8, 10, 15]) + '''
## The real cost of driving

The cost per km of a car is much more than fuel. Include:

- Fuel or electricity
- Maintenance and tyres
- Insurance and registration
- Depreciation
- Parking and tolls

Many estimates put the total at 3–5 times the fuel cost alone.

## Health benefits

Regular cycling counts towards the WHO's recommended 150–300 minutes of moderate activity a week. Studies of commuters have linked cycling with lower rates of heart disease and better mental health.

## E-bikes

E-bikes extend comfortable commuting range to 15–25 km each way and handle hills easily. They use roughly 1 kWh per 50–100 km, which costs very little to charge.

## Getting started

- Try the route on a weekend first.
- Check whether your workplace has showers and secure parking.
- Start with 1–2 days a week and build up.
''', [
 ('How much CO₂ does cycling to work save?', 'About 160 g per km a typical petrol car would have driven. A 10 km round trip saves about 1.6 kg each day.'),
 ('Is cycling cheaper than driving?', 'Almost always. Even including the bike, maintenance and gear, cycling costs a small fraction of car running costs per km.'),
])

expand('ecology/car-carbon-footprint', '''
## CO₂ per litre of fuel

| Fuel | kg CO₂ per litre (tank-to-wheel) |
|---|---|
| Petrol | about 2.31 |
| Diesel | about 2.68 |
| LPG | about 1.51 |

These come from the carbon content of the fuel. Including production and transport of the fuel (well-to-wheel) adds roughly 15–25%.

## Yearly emissions by consumption

12,000 km a year, petrol:

| Consumption | CO₂ per km | CO₂ per year |
|---|---|---|
''' + ''.join(f"| {c} L/100 km | {c*2.31*10:.0f} g | {12000*c/100*2.31/1000:.2f} t |\n" for c in [4, 5, 6, 7, 8, 10, 12]) + '''
## Ways to cut car emissions

- **Drive smoothly**: gentle acceleration and braking can save 10–20% fuel.
- **Check tyre pressure**: under-inflated tyres raise consumption.
- **Remove roof racks and extra weight** when not needed.
- **Combine trips** and avoid short cold-engine journeys.
- **Choose a more efficient car** or an EV for your next purchase — compare with the [EV vs petrol calculator](/ecology/ev-vs-petrol/).

## Putting it in context

A typical petrol car driven 12,000 km a year emits about 2 tonnes of CO₂. Global average emissions are roughly 4–5 tonnes per person per year from all sources.
''', [
 ('How much CO₂ does a litre of petrol produce?', 'About 2.31 kg when burned.'),
 ('How do I convert g/km to kg per year?', 'Multiply g/km by kilometres driven and divide by 1,000.'),
])

expand('ecology/carbon-offset-cost', '''
## Typical offset prices

| Offset type | Typical price per tonne CO₂ (voluntary market) |
|---|---|
| Renewable energy credits | low, often under 5 |
| Cookstoves and community projects | about 5–15 |
| Forestry and nature-based | about 5–30 |
| Engineered removals (e.g. direct air capture) | often 300–1,000 |

Prices vary widely by project, standard and year.

## What makes a good offset

- **Additional**: the reduction would not have happened anyway.
- **Permanent**: the carbon stays out of the atmosphere (a risk for forests that may burn).
- **Verified**: certified by a recognised standard.
- **No double counting**: credits are retired in a public registry.

## Reduce first, then offset

Offsets are most credible as a complement to cutting emissions, not a replacement. Measure your footprint, cut what you can with the [car](/ecology/car-carbon-footprint/), [flight](/ecology/flight-emissions/) and [electricity](/ecology/electricity-co2/) calculators, then offset the rest.

## Average footprints

| Region | Approximate CO₂ per person per year |
|---|---|
| Global average | 4–5 t |
| European Union | 6–7 t |
| United States | 14–15 t |
| India | about 2 t |

Figures are territorial emissions from fossil fuels and industry; consumption-based footprints can differ.
''', [
 ('How much does it cost to offset a flight?', 'A return long-haul economy flight emits roughly 1–3 tonnes of CO₂; at 15 per tonne that is about 15–45.'),
 ('Are carbon offsets worth it?', 'High-quality, verified offsets can help, but reducing your own emissions first has the most reliable impact.'),
])

expand('ecology/compost-ratio', '''
## C:N ratios of common materials

| Material | Type | Typical C:N |
|---|---|---|
| Food scraps | Green | 15–20 : 1 |
| Grass clippings | Green | 15–25 : 1 |
| Coffee grounds | Green | about 20 : 1 |
| Cow manure | Green | about 20 : 1 |
| Chicken manure | Green | 5–10 : 1 |
| Dry leaves | Brown | 40–80 : 1 |
| Straw | Brown | 50–100 : 1 |
| Cardboard | Brown | about 350 : 1 |
| Wood chips | Brown | 100–500 : 1 |

The target for a hot compost pile is about **25–30 : 1**.

## Signs your ratio is off

| Problem | Likely cause | Fix |
|---|---|---|
| Smells of ammonia | Too much nitrogen (greens) | Add browns |
| Slimy, wet pile | Too much greens, too wet | Add browns, turn the pile |
| Pile stays cold, breaks down slowly | Too much carbon (browns) | Add greens, check moisture |

## Moisture and air

Compost should feel like a wrung-out sponge — about 40–60% moisture. Turning the pile every 1–2 weeks adds oxygen and speeds decomposition.

## Volume rule of thumb

Because browns are bulky and light, a ratio of roughly **2–3 buckets of browns to 1 bucket of greens** by volume often gives a good C:N balance.
''', [
 ('What is the best C:N ratio for compost?', 'About 25–30 parts carbon to 1 part nitrogen.'),
 ('Are coffee grounds green or brown?', 'Green — they are rich in nitrogen despite their colour.'),
])

expand('ecology/electricity-co2', '''
## Footprint of common appliances

At 0.7 kg CO₂ per kWh:

| Appliance | kWh per month (typical) | CO₂ per year |
|---|---|---|
''' + ''.join(f"| {n} | {k} | {k*12*0.7:,.0f} kg |\n" for n, k in [('Refrigerator', 35), ('Air conditioner (6 h/day, summer avg)', 200), ('Ceiling fans (3)', 50), ('LED lighting (whole home)', 15), ('Television', 15), ('Electric water heater', 60), ('Washing machine', 10)]) + '''
## Why grid factors vary

The emission factor depends on how electricity is generated:

| Source | Lifecycle g CO₂e per kWh (median, IPCC) |
|---|---|
| Coal | about 820 |
| Natural gas (combined cycle) | about 490 |
| Solar PV (utility) | about 48 |
| Hydro | about 24 |
| Nuclear | about 12 |
| Wind (onshore) | about 11 |

Grids rich in coal have factors around 0.7–0.9 kg/kWh, while grids dominated by hydro, nuclear or wind can be below 0.1.

## Reducing electricity emissions

- Cut use with efficient appliances and LEDs — see the [LED savings calculator](/ecology/led-savings/).
- Shift flexible loads to times when the grid is cleaner (often midday where solar is high).
- Install rooftop solar — see the [solar system size calculator](/ecology/solar-system-size/).
''', [
 ('What is a grid emission factor?', 'The average kg of CO₂ released per kWh of electricity supplied by a grid, based on its mix of power stations.'),
 ('How much CO₂ does 1 kWh produce?', 'Anywhere from under 0.05 kg in very clean grids to over 0.8 kg in coal-heavy grids.'),
], before='## Approximate grid factors (recent years)')

expand('ecology/ev-vs-petrol', '''
## Cost per 100 km

| Vehicle | Consumption | Energy price | Cost per 100 km |
|---|---|---|---|
| EV (home charging) | 16 kWh | 0.15 per kWh | 2.40 |
| EV (fast charging) | 16 kWh | 0.45 per kWh | 7.20 |
| Petrol car | 7 L | 1.60 per L | 11.20 |
| Diesel car | 5.5 L | 1.50 per L | 8.25 |

Home charging, especially at off-peak rates, gives the biggest savings.

## Beyond fuel costs

| Cost | EV vs petrol |
|---|---|
| Purchase price | Usually higher for EVs, gap narrowing |
| Maintenance | Lower — no oil changes, less brake wear |
| Insurance | Varies; can be higher |
| Taxes and incentives | Often favour EVs |
| Resale value | Depends on battery health and market |

## Payback period

If an EV costs 5,000 more and saves 1,000 a year in running costs, the payback period is about **5 years**. Use the yearly saving from this calculator with your own price difference.

## Emissions

Even on grids with significant coal, most life-cycle studies find EVs emit less CO₂ over their lifetime than comparable petrol cars, and the gap grows as grids get cleaner. Battery production adds emissions up front that are typically paid back within 1–3 years of driving.
''', [
 ('How much does it cost to charge an EV?', 'Battery size × electricity price. A 60 kWh battery at 0.15 per kWh costs about 9 for a full charge from empty, plus charging losses of around 10%.'),
 ('How far does an EV go per kWh?', 'Typically 5–8 km per kWh.'),
])

expand('ecology/flight-emissions', '''
## Typical flight emissions (economy, one way)

| Route type | Distance | CO₂ per passenger (approx.) |
|---|---|---|
''' + ''.join(f"| {n} | {d:,} km | {d*ef:.0f} kg |\n" for n, d, ef in [('Short domestic', 500, 0.15), ('Medium domestic', 1200, 0.13), ('Short international', 2500, 0.11), ('Long-haul', 7000, 0.10), ('Ultra long-haul', 12000, 0.10)]) + '''
Short flights emit more per km because take-off and climb use a lot of fuel.

## Why class matters

Business and first-class seats take up more space, so they account for a larger share of the aircraft's emissions — often 2–4 times an economy seat on long-haul flights.

## Non-CO₂ effects

Contrails and nitrogen oxides at altitude add warming beyond CO₂. Some calculators apply a multiplier of about 1.7–2 to account for this. The calculator's radiative forcing option lets you include it.

## Flying less, flying better

- Take the train for short trips where possible.
- Fly economy and choose direct flights (take-off and landing are the most fuel-intensive phases).
- Pack light.
- Combine trips and use video calls for some meetings.

## Comparison with other transport (per passenger-km)

| Mode | g CO₂ (approx.) |
|---|---|
| Domestic flight | 150–250 |
| Petrol car (1 person) | 150–200 |
| Bus | 30–100 |
| Train (electric) | 5–40 |
''', [
 ('How much CO₂ does a flight from Delhi to London produce?', 'About 6,700 km, so roughly 0.6–0.8 tonnes per economy passenger one way, before non-CO₂ effects.'),
 ('Is flying worse than driving?', 'Per passenger-km they are similar for a solo driver, but flights cover much longer distances, so total emissions per trip are usually far higher.'),
])

expand('ecology/garden-irrigation', '''
## Water needs by plant type (per week)

| Plants | Typical water need |
|---|---|
| Established lawn (cool climate) | 25 mm |
| Lawn (hot, dry weather) | 30–50 mm |
| Vegetable garden | 25–40 mm |
| Established shrubs | 10–25 mm |
| Drought-tolerant plants | 0–10 mm |

1 mm of water on 1 m² equals 1 litre.

## Measuring your sprinkler

Place a few straight-sided containers (such as tuna cans) across the area, run the sprinkler for 15 minutes and measure the average depth. If it collects 6 mm, the sprinkler applies **24 mm per hour**.

## Best time to water

- **Early morning**: less evaporation and wind, leaves dry quickly.
- Avoid evening watering where fungal disease is a problem.
- Water deeply and less often to encourage deep roots.

## Drip vs sprinkler

| | Drip irrigation | Sprinkler |
|---|---|---|
| Efficiency | 85–95% | 60–80% |
| Best for | Beds, trees, rows | Lawns |
| Weed growth | Less | More |

## Rainwater

Use collected rainwater to cut mains water use — see the [rainwater harvesting calculator](/ecology/rainwater-harvesting/).
''', [
 ('How long should I water my lawn?', 'Long enough to apply about 25 mm a week. A sprinkler applying 24 mm/hour needs about an hour a week, split into one or two sessions.'),
 ('How many litres is 1 mm of water on 100 m²?', '100 litres.'),
])

expand('ecology/led-savings', '''
## Bulb equivalents

| Old incandescent | LED equivalent | Light output (approx.) |
|---|---|---|
| 25 W | 3–4 W | 250 lumens |
| 40 W | 5–6 W | 450 lumens |
| 60 W | 8–10 W | 800 lumens |
| 75 W | 11–13 W | 1,100 lumens |
| 100 W | 14–17 W | 1,600 lumens |

Choose bulbs by **lumens**, not watts.

## Payback period

An LED costing 3 that saves 51 W for 5 hours a day saves about 93 kWh a year. At 0.15 per kWh that is about 14 a year, so it pays for itself in about **3 months**.

## Lifespan

| Bulb type | Typical rated life |
|---|---|
| Incandescent | about 1,000 hours |
| Halogen | 2,000–3,000 hours |
| CFL | 8,000–10,000 hours |
| LED | 15,000–50,000 hours |

At 5 hours a day, a 25,000-hour LED lasts over 13 years.

## Colour temperature

| Kelvin | Appearance | Good for |
|---|---|---|
| 2,700 K | Warm white | Living rooms, bedrooms |
| 3,000 K | Soft white | Kitchens, dining |
| 4,000 K | Neutral white | Offices, workspaces |
| 5,000–6,500 K | Daylight | Workshops, task lighting |
''', [
 ('How much does switching to LED save?', 'About 80–85% of lighting energy compared with incandescent bulbs.'),
 ('What LED replaces a 60 W bulb?', 'An LED of about 8–10 W producing roughly 800 lumens.'),
])

expand('ecology/mark-recapture', '''
## How the estimate changes with recaptures

M = 50 marked, C = 40 caught in the second sample:

| Recaptured (R) | Lincoln–Petersen | Chapman |
|---|---|---|
''' + ''.join(f"| {r} | {50*40/r:.0f} | {(51*41)/(r+1)-1:.0f} |\n" for r in [2, 4, 8, 12, 20]) + '''
Few recaptures give large, uncertain estimates. Aim for at least 7–10 recaptures for a reasonable estimate.

## Assumptions

1. The population is **closed** — no births, deaths or migration between samples.
2. Marks are not lost and do not harm the animal.
3. Marked animals mix randomly back into the population.
4. Every animal has an equal chance of being caught in each sample.

If animals become trap-shy or trap-happy, the estimate will be biased.

## Confidence interval

An approximate 95% interval for the Chapman estimate uses its variance:

<p class="formula">Var = (M + 1)(C + 1)(M − R)(C − R) ÷ [(R + 1)²(R + 2)]</p>

The interval is roughly N ± 1.96 × √Var.

## Field examples

- **Fish** in a pond, marked with fin clips or tags.
- **Butterflies** marked with a small dot of paint.
- **Snails** marked with nail varnish on the shell.
''', [
 ('Why use the Chapman estimator?', 'It is less biased than Lincoln–Petersen when the number of recaptures is small, and it works even when no marked animals are recaptured.'),
 ('How long should I wait between samples?', 'Long enough for marked animals to mix back in, but short enough that births, deaths and migration are minimal — often a day to a week.'),
])

expand('ecology/pond-liner', '''
## Liner sizes for common ponds

0.3 m overlap each side:

| Pond (L × W × D) | Liner size | Water volume (approx.) |
|---|---|---|
''' + ''.join(f"| {l} × {w} × {d} m | {l+2*d+0.6:.1f} × {w+2*d+0.6:.1f} m | {l*w*d*0.6*1000:,.0f} L |\n" for l, w, d in [(2, 1.5, 0.6), (3, 2, 0.6), (3, 2, 0.8), (4, 3, 1.0), (5, 4, 1.2)]) + '''
## Liner materials

| Material | Lifespan | Notes |
|---|---|---|
| PVC | 10–20 years | Cheaper, less UV-resistant |
| EPDM rubber | 20+ years | Flexible, fish-safe, popular |
| Butyl rubber | 20–30+ years | Very durable, more expensive |
| HDPE | 20+ years | Stiff, used for large ponds and lagoons |

Use an underlay (geotextile or old carpet) to protect the liner from stones and roots.

## Depth for fish

For fish that overwinter outdoors, many keepers aim for at least **0.8–1 m** in one area so the water does not freeze solid and stays cooler in summer.

## Pump size

Circulate the full pond volume at least once every 1–2 hours for ponds with fish. A 3,000 L pond needs a pump delivering about 1,500–3,000 L/h at the required head.
''', [
 ('How do I calculate pond liner size?', 'Length = pond length + 2 × depth + 2 × overlap; width = pond width + 2 × depth + 2 × overlap.'),
 ('How deep should a fish pond be?', 'At least 0.8–1 m in part of the pond for fish such as koi and goldfish in cold climates.'),
])

expand('ecology/population-density', '''
## Population density examples

| Place | Approximate density |
|---|---|
| World (land area) | about 60 per km² |
| India | about 480 per km² |
| United Kingdom | about 280 per km² |
| United States | about 37 per km² |
| Australia | about 3–4 per km² |
| Singapore | about 8,000 per km² |
| Monaco | about 19,000 per km² |

Figures are approximate and change with population estimates.

## Density units

| Unit | Equals |
|---|---|
| 1 per km² | 2.59 per square mile |
| 1 per hectare | 100 per km² |
| 1 per acre | 247 per km² |

## Ecological density

In ecology, population density helps compare species abundance between habitats:

- **Crude density**: individuals per total area.
- **Ecological density**: individuals per area of **suitable** habitat.

Plant ecologists often count individuals in quadrats (for example 1 m²) and scale up.

## Physiological density

For countries, physiological density divides population by **arable** land only. Egypt has a moderate crude density but a very high physiological density because most people live along the Nile.
''', [
 ('How do I calculate population density?', 'Divide the population by the area. 1.25 million people on 450 km² is about 2,778 per km².'),
 ('How do I convert per km² to per square mile?', 'Multiply by 2.59.'),
])

expand('ecology/rainwater-harvesting', '''
## Runoff coefficients by surface

| Surface | Coefficient (k) |
|---|---|
| Metal or glazed tile roof | 0.85–0.95 |
| Concrete or asphalt roof | 0.80–0.90 |
| Clay tile roof | 0.75–0.85 |
| Paved yard | 0.60–0.80 |
| Lawn or garden | 0.10–0.30 |

## Water collected per 100 m² of roof

| Annual rainfall | Water collected (k = 0.85) |
|---|---|
''' + ''.join(f"| {r} mm | {100*r*0.85:,.0f} L |\n" for r in [300, 600, 800, 1000, 1500, 2500]) + '''
## Sizing the tank

A tank does not need to hold a whole year's rain. A common approach is to store enough for the **longest dry spell** you want to cover, balanced against the rain you can catch. In monsoon climates, larger tanks or recharge pits capture more of the heavy rainfall.

## First-flush diverters

The first few millimetres of rain wash dust, leaves and bird droppings off the roof. A first-flush diverter discards this dirty water before the rest flows to the tank. A common rule is about 1–2 L per m² of roof.

## Uses

- Garden watering and toilet flushing need little treatment.
- Drinking requires filtration and disinfection.
- Groundwater recharge through pits or wells helps raise local water tables.
''', [
 ('How much rainwater can I collect from my roof?', 'Area (m²) × rainfall (mm) × runoff coefficient gives litres. 100 m² with 800 mm a year gives about 68,000 L.'),
 ('Is rainwater safe to drink?', 'Not without treatment. Filter and disinfect it, and test regularly, before drinking.'),
])

expand('ecology/shower-water', '''
## Water per shower

| Flow rate | 5 min | 8 min | 10 min | 15 min |
|---|---|---|---|---|
''' + ''.join(f"| {f} L/min | {f*5} L | {f*8} L | {f*10} L | {f*15} L |\n" for f in [6, 8, 10, 12, 15]) + '''
Typical flow rates: low-flow heads 6–8 L/min, standard 9–12 L/min, power showers 15 L/min or more.

## Shower vs bath

A typical bath uses about 80–150 L. A short shower with a low-flow head uses a fraction of that, but a long power shower can use more than a bath.

## Saving water and energy

- Install a **low-flow shower head** — often cuts water by 30–50% without much change in feel.
- Cut shower time by 2 minutes.
- Lower the water heater setting slightly (keep it at least 60 °C in storage tanks to control Legionella).
- Fix dripping taps — see the [water leak calculator](/ecology/water-leak/).

## Heating energy

Heating water takes about 4.186 kJ per litre per °C. Warming 80 L by 25 °C uses about 2.3 kWh. With an electric heater at 0.15 per kWh, that is about 0.35 per shower.
''', [
 ('How much water does a 10-minute shower use?', 'About 60–120 litres, depending on the shower head flow rate.'),
 ('How do I measure my shower flow rate?', 'Time how long it takes to fill a 5 L bucket. If it takes 30 seconds, the flow is 10 L/min.'),
])

expand('ecology/solar-output', '''
## Peak sun hours by location (annual average)

| Location | Peak sun hours per day (approx.) |
|---|---|
| Northern Europe (e.g. UK, Germany) | 2.5–3.5 |
| Southern Europe | 4–5 |
| India (most regions) | 4.5–6 |
| Middle East | 5.5–6.5 |
| Australia (most cities) | 4.5–6 |
| Southern US | 5–6 |

Use a solar resource tool for your exact location; values vary by season.

## Yearly output per kWp

| Peak sun hours | kWh per kWp per year (PR 0.75) |
|---|---|
''' + ''.join(f"| {p} | {p*0.75*365:,.0f} |\n" for p in [3, 4, 4.5, 5, 5.5, 6]) + '''
## Performance losses

The performance ratio (PR) accounts for:

- Inverter losses (2–4%)
- Temperature losses (hot panels lose 0.3–0.5% per °C above 25 °C)
- Dust and soiling
- Wiring losses and shading

A PR of 0.75–0.85 is typical for well-installed systems.

## Panel orientation

In the northern hemisphere, panels facing south at a tilt close to the latitude give the most yearly energy. East–west layouts produce less in total but spread generation across the day.
''', [
 ('How much electricity does a 1 kW solar system produce?', 'About 3.5–5 kWh a day in sunny regions, or roughly 1,300–1,600 kWh a year.'),
 ('What are peak sun hours?', 'The number of hours per day the sun would need to shine at 1,000 W/m² to deliver the same energy as the actual daylight.'),
])

expand('ecology/solar-system-size', '''
## System size by monthly use

5 peak sun hours, PR 0.75, 450 W panels:

| Monthly use | System size | Panels | Roof area |
|---|---|---|---|
''' + ''.join(f"| {u} kWh | {u/30/3.75:.2f} kWp | {math.ceil(u/30/3.75*1000/450)} | {math.ceil(u/30/3.75*1000/450)*2.2:.0f} m² |\n" for u in [150, 250, 400, 600, 800, 1000]) + '''
## On-grid, off-grid or hybrid

| Type | Battery | Works in power cuts? | Cost |
|---|---|---|---|
| On-grid (grid-tied) | No | No (shuts off for safety) | Lowest |
| Hybrid | Yes | Yes, for backed-up loads | Higher |
| Off-grid | Yes, larger | Yes | Highest |

## Net metering

With net metering, excess daytime energy is exported to the grid and credited against what you import at night. This lets you size the system for your total monthly use without batteries. Rules and tariffs vary by country and utility.

## Shadow-free area

Allow about **8–10 m² of shadow-free roof per kWp** including spacing and walkways, more on flat roofs where panels are tilted on frames.

## Payback

Payback years ≈ installed cost ÷ yearly savings. Use the energy per year from the [solar output calculator](/ecology/solar-output/) × your electricity price to estimate savings.
''', [
 ('What size solar system do I need for 400 units a month?', 'With 5 peak sun hours and a 0.75 performance ratio, about 3.6 kWp.'),
 ('How much roof space does 1 kW of solar need?', 'About 5–6 m² of panels, or 8–10 m² of shadow-free area including spacing.'),
])

expand('ecology/tree-offset', '''
## CO₂ absorbed by trees

| Tree type and age | CO₂ per year (approx.) |
|---|---|
| Young tree (first 5–10 years) | 5–10 kg |
| Mature temperate tree | 10–25 kg |
| Fast-growing tropical tree | 20–50 kg |
| Hectare of growing forest | 5–20 tonnes |

Absorption varies widely with species, climate, soil and age. A commonly used average is about **20–25 kg per tree per year** over its growing life.

## Why trees are a slow fix

- Most CO₂ is absorbed as trees grow, over decades.
- Trees can die, burn or be cut, releasing their carbon.
- Planting the wrong species in the wrong place can harm ecosystems.

Trees are valuable for biodiversity, shade, soil and water, but they work best alongside cutting emissions, not as a replacement.

## Land needed

At around 400–1,000 trees per hectare, offsetting 5 tonnes a year at 20 kg per tree needs 250 trees — roughly 0.25–0.6 hectares of land that stays forested.

## Protecting existing forests

Keeping existing forests standing prevents large carbon releases and protects species. Protection is often more effective per unit of money than planting new trees.
''', [
 ('How many trees offset 1 tonne of CO₂?', 'About 40–50 trees absorbing 20–25 kg each per year.'),
 ('How much CO₂ does one tree absorb?', 'Typically 10–25 kg per year for a mature tree, depending on species and climate.'),
])

expand('ecology/water-leak', '''
## Water wasted by leak size

| Leak | Approx. per day | Per year |
|---|---|---|
''' + ''.join(f"| {n} | {d:,.0f} L | {d*365:,.0f} L |\n" for n, d in [('10 drips per minute', 10*0.25*1440/1000), ('30 drips per minute', 30*0.25*1440/1000), ('60 drips per minute', 60*0.25*1440/1000), ('Thin stream (1/16 inch)', 400), ('Running toilet (silent leak)', 200), ('Running toilet (visible)', 1000)]) + '''
Figures are rough; toilet leaks in particular vary from a trickle to hundreds of litres a day.

## Finding hidden leaks

- **Water meter test**: turn off all taps and appliances and read the meter. If it moves over 30–60 minutes, there is a leak.
- **Toilet dye test**: put a few drops of food colouring in the cistern. If colour appears in the bowl without flushing, the flapper is leaking.
- **Check outside taps, hoses and irrigation** connections.

## Common fixes

| Leak | Usual fix |
|---|---|
| Dripping tap | Replace washer or cartridge |
| Running toilet | Replace flapper or fill valve |
| Leaking shower head | Re-seal with thread tape |
| Pipe joint | Tighten or replace fitting |

Most of these are cheap and quick, and save both water and money.
''', [
 ('How much water does a dripping tap waste?', 'At 30 drips a minute, about 10–11 litres a day or nearly 4,000 litres a year.'),
 ('How much water is in one drip?', 'About 0.25 mL is a common estimate, though it varies with the tap.'),
])

expand('ecology/wind-turbine-power', '''
## Power vs wind speed

2 m rotor, Cp 0.4, air density 1.225 kg/m³:

| Wind speed | Power |
|---|---|
''' + ''.join(f"| {v} m/s ({v*3.6:.0f} km/h) | {0.5*1.225*pi*1*v**3*0.4:,.0f} W |\n" for v in [3, 4, 5, 6, 8, 10, 12]) + '''
Doubling the wind speed gives **8 times** the power, because power depends on the cube of speed.

## The Betz limit

No turbine can capture more than 16/27 (59.3%) of the wind's energy. Modern utility turbines reach about 45–50% at their best operating point.

## Capacity factor

A turbine rarely runs at full power. Capacity factor = actual yearly energy ÷ (rated power × 8,760 hours).

| Turbine type | Typical capacity factor |
|---|---|
| Small urban turbine | 5–15% |
| Small rural turbine, good site | 15–25% |
| Onshore wind farm | 25–40% |
| Offshore wind farm | 40–50% |

## Siting small turbines

- Mount the turbine well above obstacles — ideally 10 m higher than anything within 100 m.
- Average wind speed of at least 5 m/s is usually needed for a worthwhile output.
- Rooftop turbines in towns often produce far less than expected because of turbulence.
''', [
 ('How much power does a wind turbine produce?', 'P = ½ × ρ × A × v³ × Cp. A 2 m rotor in 6 m/s wind produces about 170 W at Cp 0.4.'),
 ('What is the Betz limit?', 'The theoretical maximum share of wind energy a turbine can extract: 59.3%.'),
])

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/ecology/*.mdx')):
    c = 'ecology/' + os.path.basename(p)[:-4]; print(c, words(c))
