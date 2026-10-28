import math
from page import page
C='everyday-life'; U='updated: 2026-10-27'

page(C,'age-calculator',f'''
title: Age Calculator
description: Calculate exact age in years, months and days from a date of birth — or age on any date.
category: everyday-life
keywords: [age calculator, how old am i, date of birth, age in days, age in months, birthday calculator]
{U}
featured: true
variables:
  - {{ id: dob, label: Date of birth, family: date, default: -12784 }}
  - {{ id: on, label: Age on this date, family: date, default: 0 }}
  - {{ id: y, label: Age in completed years, decimals: 0 }}
  - {{ id: mo, label: Age in completed months, decimals: 0 }}
  - {{ id: wk, label: Age in weeks, decimals: 1 }}
  - {{ id: dd, label: Age in days, decimals: 0 }}
equations:
  - y = yearsBetween(dob, on)
  - mo = monthsBetween(dob, on)
  - dd = on - dob
  - wk = dd / 7
faq:
  - q: How is age calculated?
    a: Age is the number of full years since the date of birth. The calculator compares the actual calendar dates, so leap years are handled correctly.
  - q: Can I find my age on a future date?
    a: Yes. Change "Age on this date" to any past or future date.
  - q: How are people born on 29 February handled?
    a: Their age increases on 1 March in non-leap years in this calculator; legal rules vary by country.
related: [everyday-life/days-between-dates, everyday-life/days-until, other/dog-age]
''','''
## How to use this calculator

Pick the **date of birth**. "Age on this date" starts at today — change it to find your age on any other date. You get completed years and months, plus total weeks and days.

## How it works

The calculator counts full calendar months between the two dates and divides by 12 for years. A birthday has to be reached before the year counts — just as people normally count age.

## Example

Born 15 March 1990, on 14 March 2026 → **35 years** (the 36th birthday is the next day).

## Fun facts

- You turn 10,000 days old at about 27 years and 5 months.
- One billion seconds is about 31 years and 8 months.
- The number of days is the most precise measure — try it for anniversaries too.
''')

page(C,'days-between-dates',f'''
title: Days Between Dates Calculator
description: Count the days, weeks, months and working days between two dates.
category: everyday-life
keywords: [days between dates, date difference, how many days until, working days, business days, date calculator]
{U}
featured: true
variables:
  - {{ id: d1, label: Start date, family: date, default: 0 }}
  - {{ id: d2, label: End date, family: date, default: 100 }}
  - {{ id: dd, label: Days between, decimals: 0 }}
  - {{ id: wk, label: Weeks, decimals: 2 }}
  - {{ id: mo, label: Completed months, decimals: 0 }}
  - {{ id: wd, label: Working days (Mon–Fri), decimals: 0 }}
equations:
  - dd = d2 - d1
  - wk = dd / 7
  - mo = monthsBetween(d1, d2)
  - wd = workdays(d1, d2)
faq:
  - q: Does the count include the end date?
    a: No. The number of days is end minus start — like counting nights in a hotel. Add 1 if you want to include both days.
  - q: Are public holidays excluded from working days?
    a: No. Working days counts Monday to Friday only. Subtract holidays in your country yourself.
  - q: Can the start date be after the end date?
    a: Yes — the result will be negative.
related: [everyday-life/date-plus-days, everyday-life/days-until, everyday-life/age-calculator]
''','''
## How to use this calculator

Choose a **start date** and an **end date**. You get the number of days, weeks, completed months and working days (Monday to Friday) between them.

## How days are counted

The result is end date − start date, so 1 Jan to 2 Jan is 1 day. To include both the first and last day (for example for a holiday booking that counts days, not nights), add 1.

## Working days

Working days count Monday to Friday from the start date up to (but not including) the end date. Public holidays vary by country and are not removed automatically.

## Uses

- Notice periods and contract lengths
- Project timelines and deadlines
- Interest periods for invoices
''')

page(C,'date-plus-days',f'''
title: Add Days to a Date Calculator
description: Add or subtract days from a date to find the resulting date and day of the week.
category: everyday-life
keywords: [add days to date, date calculator, days from today, subtract days, date after, deadline calculator]
{U}
variables:
  - {{ id: d1, label: Start date, family: date, default: 0 }}
  - {{ id: n, label: Days to add (negative to subtract), default: 90 }}
  - {{ id: d2, label: Resulting date, family: date }}
equations:
  - d2 = d1 + n
faq:
  - q: What date is 90 days from today?
    a: Leave the start date as today and enter 90 — the resulting date and weekday are shown.
  - q: How do I subtract days?
    a: Enter a negative number, such as −30.
  - q: Can I find how many days are between two dates here?
    a: Yes — press × on Days and set both dates. Or use the days between dates calculator.
related: [everyday-life/days-between-dates, everyday-life/days-until]
''','''
## How to use this calculator

Choose a **start date** (today by default) and the **number of days** to add. Use a negative number to go back in time. The resulting date is shown with its day of the week.

## Common uses

- **Deadlines:** "within 30 days of the invoice date"
- **Notice periods:** 60 or 90 days
- **Medication or treatment courses**
- **Warranty and return windows**

## Weeks and months

To add weeks, multiply by 7 (6 weeks = 42 days). Months have different lengths, so "3 months" is not always 90 days — check the exact date your contract means.
''')

page(C,'days-until',f'''
title: Days Until Calculator (Countdown)
description: Count down the days, weeks and working days until any date — a birthday, holiday, exam or event.
category: everyday-life
keywords: [days until, countdown, how many days until, days left, days to go, event countdown]
{U}
variables:
  - {{ id: t, label: Today, family: date, default: 0 }}
  - {{ id: ev, label: Event date, family: date, default: 60 }}
  - {{ id: dd, label: Days to go, decimals: 0 }}
  - {{ id: wk, label: Weeks to go, decimals: 1 }}
  - {{ id: wd, label: Working days to go, decimals: 0 }}
  - {{ id: hh, label: Hours to go (approx.), decimals: 0 }}
equations:
  - dd = ev - t
  - wk = dd / 7
  - wd = workdays(t, ev)
  - hh = dd * 24
faq:
  - q: How many days until my event?
    a: Choose the event date — the number of days from today is shown instantly.
  - q: Why might the hours be slightly off?
    a: Hours are counted from midnight today, not from the current time.
  - q: Can I share the countdown?
    a: Yes. Use Share link — the event date is saved in the link.
related: [everyday-life/days-between-dates, everyday-life/age-calculator]
''','''
## How to use this calculator

Set the **event date**. The days, weeks, working days and approximate hours remaining are shown. Share the link with friends — the date is saved in it.

## Ideas

- Birthdays and anniversaries
- Exams and deadlines
- Holidays and festivals
- Weddings and trips
- Retirement day

## Planning tip

Working days to go is useful for project deadlines: a "2-month" deadline might leave only about 43 working days.
''')

page(C,'hours-worked',f'''
title: Hours Worked Calculator (Time Card)
description: Calculate hours worked from start and end time minus breaks — plus your pay for the shift.
category: everyday-life
keywords: [hours worked calculator, time card, timesheet, work hours, shift hours, overtime, payroll]
{U}
featured: true
variables:
  - {{ id: st, label: Start time, family: clock, default: 9 }}
  - {{ id: en, label: End time, family: clock, default: 17.5 }}
  - {{ id: br, label: Unpaid break, suffix: minutes, default: 30, min: 0 }}
  - {{ id: rate, label: Hourly rate, family: currency, default: 20, min: 0, decimals: 2 }}
  - {{ id: h, label: Hours worked, decimals: 2 }}
  - {{ id: pay, label: Pay for this shift, family: currency, decimals: 2 }}
equations:
  - h = mod(en - st, 24) - br / 60
  - pay = h * rate
faq:
  - q: How do I calculate hours worked?
    a: Subtract the start time from the end time, then subtract unpaid breaks. 9:00 to 17:30 with a 30-minute break is 8 hours.
  - q: Does it work for night shifts?
    a: Yes. If the end time is earlier than the start time, the calculator assumes the shift ends the next day.
  - q: How do I convert minutes to decimal hours?
    a: Divide by 60. 45 minutes = 0.75 hours.
related: [everyday-life/time-duration, finance/hourly-to-salary]
''','''
## How to use this calculator

Enter your **start time**, **end time** and **unpaid break** in minutes. Add your **hourly rate** to see the pay for the shift. Night shifts that pass midnight are handled automatically.

## Example

9:00 to 17:30 with a 30-minute break: 8.5 − 0.5 = **8 hours**. At 20 per hour, pay = **160**.

## Minutes to decimal hours

| Minutes | Decimal hours |
|---|---|
| 15 | 0.25 |
| 20 | 0.33 |
| 30 | 0.5 |
| 45 | 0.75 |

## Overtime

Many employers pay overtime above 8 hours a day or 40 hours a week, often at 1.5× the normal rate. Check your contract and local labour law.
''')

page(C,'time-duration',f'''
title: Time Duration Calculator
description: Find the time between two clock times in hours and minutes — works across midnight.
category: everyday-life
keywords: [time duration, time between two times, hours between times, time difference, elapsed time]
{U}
variables:
  - {{ id: a, label: Start time, family: clock, default: 22.5 }}
  - {{ id: b, label: End time, family: clock, default: 6.75 }}
  - {{ id: h, label: Duration in hours (decimal), decimals: 2 }}
  - {{ id: m, label: Duration in minutes, decimals: 0 }}
equations:
  - h = mod(b - a, 24)
  - m = h * 60
faq:
  - q: How do I calculate the time between two times?
    a: Subtract the start from the end. If the end is earlier on the clock, add 24 hours because it is the next day.
  - q: What is 8.25 hours in hours and minutes?
    a: 8 hours 15 minutes — multiply the decimal part by 60.
  - q: Can it handle more than 24 hours?
    a: No — for longer periods, use the days between dates calculator.
related: [everyday-life/hours-worked, everyday-life/sleep-calculator]
''','''
## How to use this calculator

Enter a **start time** and an **end time**. The duration appears in decimal hours and minutes. If the end time is earlier than the start, it is treated as the next day.

## Example

22:30 to 06:45 = **8.25 hours** = 8 h 15 min (495 minutes).

## Converting decimal hours

Multiply the decimal part by 60: 7.6 h = 7 h + 0.6 × 60 min = **7 h 36 min**.
''')

page(C,'sleep-calculator',f'''
title: Sleep Calculator (Bedtime & Wake-Up Time)
description: Find the best time to wake up or go to bed based on 90-minute sleep cycles.
category: everyday-life
keywords: [sleep calculator, sleep cycles, when to wake up, bedtime calculator, 90 minute sleep cycle]
{U}
featured: true
variables:
  - {{ id: bed, label: Bedtime, family: clock, default: 22.75 }}
  - id: cyc
    label: Number of sleep cycles
    default: 6
    options:
      - {{ label: 4 cycles (6 h of sleep), value: 4 }}
      - {{ label: 5 cycles (7.5 h of sleep), value: 5 }}
      - {{ label: 6 cycles (9 h of sleep), value: 6 }}
  - {{ id: fall, label: Time to fall asleep, suffix: minutes, default: 15, min: 0 }}
  - {{ id: wake, label: Wake-up time, family: clock }}
equations:
  - wake = bed + fall / 60 + cyc * 1.5
faq:
  - q: How long is a sleep cycle?
    a: About 90 minutes on average, though it varies between 70 and 120 minutes from person to person and through the night.
  - q: How much sleep do adults need?
    a: Health organisations recommend 7 or more hours for adults — usually 5 or 6 cycles.
  - q: How do I find when to go to bed?
    a: Press × on Bedtime and enter the time you need to wake up.
related: [everyday-life/time-duration, health/bmr]
''','''
## How to use this calculator

Enter your **bedtime**, choose the number of **sleep cycles** and how long you usually take to **fall asleep**. The best wake-up time is calculated. To plan a bedtime, press × on Bedtime and type the time your alarm must ring.

## Why cycles?

Sleep moves through light, deep and REM stages in cycles of roughly 90 minutes. Waking at the end of a cycle — rather than in deep sleep — usually feels easier.

## Example

Bed at 22:45, 15 minutes to fall asleep, 5 cycles: wake at **06:30** (7.5 hours of sleep).

## Better sleep habits

- Keep a regular schedule, even at weekends.
- Avoid caffeine late in the day.
- Keep the bedroom dark, quiet and cool.
- Put screens away 30–60 minutes before bed.
''')

page(C,'tip-calculator',f'''
title: Tip Calculator (Split the Bill)
description: Calculate the tip, total bill and amount per person when splitting a restaurant bill.
category: everyday-life
keywords: [tip calculator, split bill, gratuity, restaurant tip, how much to tip, per person]
{U}
featured: true
variables:
  - {{ id: b, label: Bill amount, family: currency, default: 85, min: 0, decimals: 2 }}
  - {{ id: tp, label: Tip, family: percent, unit: '%', default: 15, min: 0 }}
  - {{ id: n, label: Number of people, default: 4, min: 1 }}
  - {{ id: t, label: Tip amount, family: currency, min: 0, decimals: 2 }}
  - {{ id: tot, label: Total including tip, family: currency, min: 0, decimals: 2 }}
  - {{ id: pp, label: Each person pays, family: currency, min: 0, decimals: 2 }}
equations:
  - t = b * tp
  - tot = b + t
  - pp = tot / n
faq:
  - q: How much should I tip?
    a: Customs vary. In the US 15–20% is usual at restaurants; in many European countries rounding up or about 5–10% is common; in some countries service is included.
  - q: Should I tip on the amount before or after tax?
    a: Traditionally on the pre-tax amount, though many people tip on the total for simplicity.
  - q: How do I quickly work out 15%?
    a: Take 10% (move the decimal point) and add half of it again.
related: [everyday-life/unit-price, math/percentage, finance/sales-tax-vat]
''','''
## How to use this calculator

Enter the **bill**, the **tip percentage** and the **number of people**. The tip, total and amount per person are calculated.

## Example

A bill of 85 with a 15% tip, split 4 ways:

- Tip = **12.75**
- Total = **97.75**
- Each person pays **24.44**

## Quick tip table (bill of 50)

| Tip | Amount |
|---|---|
| 10% | 5.00 |
| 15% | 7.50 |
| 18% | 9.00 |
| 20% | 10.00 |

Check the bill first — some restaurants already add a service charge.
''')

page(C,'unit-price',f'''
title: Unit Price Comparison Calculator
description: Compare two products by price per unit (per kg, litre or item) to find the better deal.
category: everyday-life
keywords: [unit price calculator, price per kg, better deal, price comparison, grocery comparison, price per unit]
{U}
variables:
  - {{ id: pa, label: Price of product A, family: currency, default: 4.5, min: 0, decimals: 2 }}
  - {{ id: qa, label: Quantity of A (g, ml or items), default: 750, min: 0 }}
  - {{ id: pb, label: Price of product B, family: currency, default: 6.2, min: 0, decimals: 2 }}
  - {{ id: qb, label: Quantity of B (same unit), default: 1200, min: 0 }}
  - {{ id: ua, label: A — price per 100 units, family: currency, min: 0, decimals: 3 }}
  - {{ id: ub, label: B — price per 100 units, family: currency, min: 0, decimals: 3 }}
  - {{ id: sav, label: B is cheaper per unit by, family: percent, unit: '%' }}
equations:
  - ua = pa / qa * 100
  - ub = pb / qb * 100
  - sav = 1 - ub / ua
faq:
  - q: How do I compare prices of different sizes?
    a: Divide each price by its quantity to get the price per unit, then compare.
  - q: What does a negative saving mean?
    a: Product A is cheaper per unit than B.
  - q: Is the bigger pack always cheaper?
    a: No. Special offers on smaller packs can beat bulk sizes — always check the unit price.
related: [everyday-life/tip-calculator, finance/discount]
''','''
## How to use this calculator

Enter the **price** and **quantity** of two products, using the same unit for both (grams, millilitres or items). You get the price per 100 units and how much cheaper B is than A.

## Example

- A: 750 g for 4.50 → **0.600** per 100 g
- B: 1,200 g for 6.20 → **0.517** per 100 g
- B is **13.9%** cheaper per gram

## Tips

- Convert units first: 1 kg = 1,000 g; 1 L = 1,000 ml.
- Consider waste — a bulk pack that goes off before you use it is not a saving.
''')

page(C,'fuel-cost',f'''
title: Fuel Cost Calculator (Trip Cost)
description: Calculate the fuel needed and the cost of a trip from distance, fuel consumption and fuel price — and split it between passengers.
category: everyday-life
keywords: [fuel cost calculator, trip cost, petrol cost, gas cost, road trip, fuel consumption, l/100km]
{U}
featured: true
variables:
  - {{ id: d, label: Trip distance, family: length, unit: km, imperialUnit: mi, default: 350, min: 0 }}
  - {{ id: c, label: Fuel consumption, suffix: L/100 km, default: 7, min: 0 }}
  - {{ id: p, label: Fuel price per litre, family: currency, default: 1.6, min: 0, decimals: 3 }}
  - {{ id: n, label: People sharing, default: 1, min: 1 }}
  - {{ id: f, label: Fuel needed, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: cost, label: Total fuel cost, family: currency, min: 0, decimals: 2 }}
  - {{ id: pp, label: Cost per person, family: currency, min: 0, decimals: 2 }}
equations:
  - f = d / 1000 * c / 100 / 1000
  - cost = f * 1000 * p
  - pp = cost / n
faq:
  - q: How do I calculate fuel cost?
    a: Fuel needed = distance × consumption ÷ 100. Cost = fuel needed × price per litre.
  - q: My car shows mpg — what do I enter?
    a: Convert with the fuel economy converter. 30 US mpg ≈ 7.84 L/100 km.
  - q: Should I include the return journey?
    a: Yes — enter the total distance for a round trip.
related: [everyday-life/fuel-economy, everyday-life/electricity-cost, physics/speed-distance-time]
''','''
## How to use this calculator

Enter the **distance**, your car's **consumption** in L/100 km and the **fuel price**. Add the number of people sharing to split the cost.

## Formula

<p class="formula">Fuel = distance × consumption ÷ 100   Cost = fuel × price</p>

## Example

350 km at 7 L/100 km, fuel at 1.60 per litre:

- Fuel = 350 × 7 ÷ 100 = **24.5 L**
- Cost = 24.5 × 1.60 = **39.20**

## Save fuel

- Keep tyres at the correct pressure.
- Drive smoothly — harsh acceleration uses much more fuel.
- Reduce speed on motorways: drag rises sharply above about 90 km/h.
- Remove roof racks when not in use.
''')

page(C,'fuel-economy',f'''
title: Fuel Economy Converter (L/100 km ↔ mpg)
description: Convert fuel consumption between L/100 km, km/L, US mpg and UK mpg.
category: everyday-life
keywords: [fuel economy converter, l/100km to mpg, mpg to l/100km, km per litre, mileage converter]
{U}
variables:
  - {{ id: l, label: Litres per 100 km, default: 7, min: 0.01 }}
  - {{ id: kml, label: Kilometres per litre, min: 0 }}
  - {{ id: us, label: Miles per US gallon (mpg US), min: 0 }}
  - {{ id: uk, label: Miles per UK gallon (mpg UK), min: 0 }}
equations:
  - kml = 100 / l
  - us = 235.2146 / l
  - uk = 282.4809 / l
faq:
  - q: How do I convert L/100 km to mpg?
    a: US mpg = 235.21 ÷ L/100 km; UK mpg = 282.48 ÷ L/100 km.
  - q: Why are US and UK mpg different?
    a: A UK (imperial) gallon is about 20% bigger than a US gallon, so the same car shows a higher UK mpg figure.
  - q: Why does lower L/100 km mean better economy?
    a: L/100 km measures fuel used, so smaller is better. km/L and mpg measure distance per fuel, so bigger is better.
related: [everyday-life/fuel-cost, conversion/liters-to-gallons]
''','''
## How to use this converter

Type a value in **any** field — L/100 km, km/L, US mpg or UK mpg — and the others update.

## Formulas

<p class="formula">km/L = 100 ÷ (L/100 km)<br/>mpg (US) = 235.21 ÷ (L/100 km)<br/>mpg (UK) = 282.48 ÷ (L/100 km)</p>

## Conversion table

| L/100 km | km/L | US mpg | UK mpg |
|---|---|---|---|
| 4 | 25.0 | 58.8 | 70.6 |
| 5 | 20.0 | 47.0 | 56.5 |
| 6 | 16.7 | 39.2 | 47.1 |
| 8 | 12.5 | 29.4 | 35.3 |
| 10 | 10.0 | 23.5 | 28.2 |
| 12 | 8.3 | 19.6 | 23.5 |
''')

page(C,'electricity-cost',f'''
title: Electricity Cost Calculator (Appliance Running Cost)
description: Calculate how much an appliance costs to run per day, month and year from its wattage, hours of use and electricity rate.
category: everyday-life
keywords: [electricity cost calculator, appliance running cost, kwh cost, power consumption, energy bill, watts to kwh]
{U}
featured: true
variables:
  - {{ id: P, label: Appliance power, family: power, unit: W, default: 1500, min: 0 }}
  - {{ id: h, label: Hours used per day, suffix: hours, default: 3, min: 0, max: 24 }}
  - {{ id: r, label: Electricity price per kWh, family: currency, default: 0.15, min: 0, decimals: 3 }}
  - {{ id: en, label: Energy per day, suffix: kWh, min: 0 }}
  - {{ id: cd, label: Cost per day, family: currency, min: 0, decimals: 2 }}
  - {{ id: cm, label: Cost per month (30 days), family: currency, min: 0, decimals: 2 }}
  - {{ id: cy, label: Cost per year, family: currency, min: 0, decimals: 2 }}
equations:
  - en = P * h / 1000
  - cd = en * r
  - cm = cd * 30
  - cy = cd * 365
faq:
  - q: How do I calculate electricity cost?
    a: kWh = watts × hours ÷ 1,000. Cost = kWh × price per kWh.
  - q: Where do I find the wattage?
    a: On the appliance label or in the manual. For fridges and other cycling appliances, use the yearly kWh figure from the energy label instead.
  - q: What is a unit of electricity?
    a: In most countries one "unit" on the bill is 1 kWh.
related: [everyday-life/fuel-cost, conversion/energy-converter, conversion/power-converter]
''','''
## How to use this calculator

Enter the appliance's **power** in watts (or kW), how many **hours per day** you use it, and your **electricity price per kWh**. The daily, monthly and yearly running costs are calculated.

## Formula

<p class="formula">kWh/day = watts × hours ÷ 1000   Cost = kWh × price</p>

## Example

A 1,500 W heater used 3 hours a day at 0.15 per kWh:

- Energy = **4.5 kWh/day**
- Cost = **0.675/day** — about **20.25/month** and **246.38/year**

## Typical appliance power

| Appliance | Typical power |
|---|---|
| LED bulb | 8–12 W |
| Ceiling fan | 50–75 W |
| Laptop | 45–65 W |
| TV (LED) | 60–150 W |
| Air conditioner (1.5 ton) | 1,200–1,800 W |
| Electric kettle | 1,500–2,200 W |
| Water heater (geyser) | 2,000–3,000 W |
''')

page(C,'reading-time',f'''
title: Reading Time Calculator
description: Estimate how long it takes to read (or speak) a text from its word count and reading speed.
category: everyday-life
keywords: [reading time calculator, words per minute, how long to read, speech time, word count to minutes]
{U}
variables:
  - {{ id: w, label: Number of words, default: 1500, min: 0 }}
  - id: wpm
    label: Speed
    default: 238
    options:
      - {{ label: Silent reading, average adult (238 wpm), value: 238 }}
      - {{ label: Slow / careful reading (150 wpm), value: 150 }}
      - {{ label: Fast reading (350 wpm), value: 350 }}
      - {{ label: Speaking / presentation (130 wpm), value: 130 }}
      - {{ label: Reading aloud (183 wpm), value: 183 }}
  - {{ id: t, label: Time, suffix: minutes, min: 0, decimals: 1 }}
equations:
  - t = w / wpm
faq:
  - q: What is the average reading speed?
    a: A 2019 review of studies found adults read non-fiction silently at about 238 words per minute on average.
  - q: How long is a 1,000-word speech?
    a: About 7–8 minutes at a natural speaking pace of 130 words per minute.
  - q: How many words is a page?
    a: Roughly 250–300 words for a typical double-spaced or book page, 500 for single-spaced.
related: [everyday-life/typing-speed]
''','''
## How to use this calculator

Enter the **word count** and choose a **speed**. The reading or speaking time is shown in minutes. To find how many words fit in a time slot, press × on the word count and enter the minutes.

## Formula

<p class="formula">Time (minutes) = words ÷ words per minute</p>

## Example

A 1,500-word blog post at 238 wpm takes about **6.3 minutes** to read. As a presentation at 130 wpm it would take about **11.5 minutes**.

## Speech planning

| Talk length | Approx. words (130 wpm) |
|---|---|
| 3 minutes | 390 |
| 5 minutes | 650 |
| 10 minutes | 1,300 |
| 20 minutes | 2,600 |
''')

page(C,'grade-needed',f'''
title: Final Exam Grade Calculator
description: Find the score you need on your final exam to reach a target course grade.
category: everyday-life
keywords: [final grade calculator, what do i need on my final, exam score needed, grade calculator, course grade]
{U}
variables:
  - {{ id: cur, label: Current grade, family: percent, unit: '%', default: 78, min: 0 }}
  - {{ id: w, label: Final exam weight, family: percent, unit: '%', default: 30, min: 0.0001, max: 1 }}
  - {{ id: tg, label: Target course grade, family: percent, unit: '%', default: 80, min: 0 }}
  - {{ id: need, label: Score needed on the final, family: percent, unit: '%' }}
equations:
  - tg = cur * (1 - w) + need * w
faq:
  - q: How is the score needed on the final calculated?
    a: Needed = (target − current × (1 − weight)) ÷ weight.
  - q: What if the result is above 100%?
    a: The target can't be reached with this final alone — consider a lower target or ask about extra credit.
  - q: Can I find my final grade from an exam score?
    a: Yes. Press × on Target and enter your exam score.
related: [math/average, math/percentage]
''','''
## How to use this calculator

Enter your **current grade**, the **weight of the final exam** and your **target** course grade. The score you need on the final is calculated.

## Formula

<p class="formula">Needed = (target − current × (1 − w)) ÷ w</p>

## Example

Current grade 78%, final worth 30%, target 80%:

Needed = (80 − 78 × 0.7) ÷ 0.3 = **84.7%**

## Study planning

If you need a high score, focus first on topics with the most marks and past-paper practice under timed conditions.
''')

page(C,'rent-split',f'''
title: Rent Split Calculator (By Room Size)
description: Split rent fairly between roommates based on bedroom size, with shared space divided equally.
category: everyday-life
keywords: [rent split calculator, roommate rent, split rent by room size, fair rent, shared apartment]
{U}
variables:
  - {{ id: R, label: Total monthly rent, family: currency, default: 2400, min: 0, decimals: 2 }}
  - {{ id: sh, label: Share of rent for common areas, family: percent, unit: '%', default: 40, min: 0, max: 1 }}
  - {{ id: a1, label: Room 1 size, family: area, unit: m2, imperialUnit: ft2, default: 14, min: 0 }}
  - {{ id: a2, label: Room 2 size, family: area, unit: m2, imperialUnit: ft2, default: 11, min: 0 }}
  - {{ id: a3, label: Room 3 size, family: area, unit: m2, imperialUnit: ft2, default: 9, min: 0 }}
  - {{ id: p1, label: Room 1 pays, family: currency, decimals: 2 }}
  - {{ id: p2, label: Room 2 pays, family: currency, decimals: 2 }}
  - {{ id: p3, label: Room 3 pays, family: currency, decimals: 2 }}
equations:
  - p1 = R * sh / 3 + R * (1 - sh) * a1 / (a1 + a2 + a3)
  - p2 = R * sh / 3 + R * (1 - sh) * a2 / (a1 + a2 + a3)
  - p3 = R * sh / 3 + R * (1 - sh) * a3 / (a1 + a2 + a3)
faq:
  - q: What is a fair way to split rent?
    a: A common approach divides part of the rent equally (for shared spaces) and the rest by bedroom size.
  - q: What percentage should be for shared space?
    a: Often 30–50%, depending on how much of the home is shared living area.
  - q: What about a private bathroom or balcony?
    a: Add its area to that room, or agree an extra amount on top.
related: [everyday-life/tip-calculator, math/rectangle]
''','''
## How to use this calculator

Enter the **total rent**, the share that covers **common areas** (split equally) and the size of each **bedroom**. Each person's share is calculated.

## Formula

<p class="formula">Share = rent × common% ÷ 3 + rent × (1 − common%) × room area ÷ total room area</p>

## Example

Rent 2,400, 40% for common areas, rooms of 14, 11 and 9 m²:

- Room 1: 320 + 1,440 × 14/34 = **912.94**
- Room 2: 320 + 1,440 × 11/34 = **785.88**
- Room 3: 320 + 1,440 × 9/34 = **701.18**

For two roommates, set one room size to 0 and adjust — or agree on the split you all find fair.
''')

page(C,'typing-speed',f'''
title: Typing Speed Calculator (WPM)
description: Calculate typing speed in words per minute (WPM) and characters per minute from your test results.
category: everyday-life
keywords: [typing speed, wpm calculator, words per minute, cpm, typing test, net wpm]
{U}
variables:
  - {{ id: ch, label: Characters typed (including spaces), default: 1250, min: 0 }}
  - {{ id: er, label: Uncorrected errors, default: 5, min: 0 }}
  - {{ id: t, label: Time, suffix: minutes, default: 5, min: 0.01 }}
  - {{ id: gross, label: Gross WPM, min: 0, decimals: 1 }}
  - {{ id: net, label: Net WPM, decimals: 1 }}
  - {{ id: cpm, label: Characters per minute, min: 0, decimals: 0 }}
equations:
  - gross = ch / 5 / t
  - net = gross - er / t
  - cpm = ch / t
faq:
  - q: How is WPM calculated?
    a: By convention, one "word" is 5 characters including spaces. WPM = characters ÷ 5 ÷ minutes.
  - q: What is net WPM?
    a: Gross WPM minus uncorrected errors per minute — a fairer measure of useful speed.
  - q: What is a good typing speed?
    a: About 40 WPM is average; 60–70 WPM is good for office work; professional typists exceed 80 WPM.
related: [everyday-life/reading-time]
''','''
## How to use this calculator

Enter the number of **characters typed**, any **uncorrected errors** and the **time** in minutes. Gross WPM, net WPM and characters per minute are calculated.

## Formulas

<p class="formula">Gross WPM = (characters ÷ 5) ÷ minutes<br/>Net WPM = gross WPM − errors ÷ minutes</p>

## Example

1,250 characters in 5 minutes with 5 errors:

- Gross = 250 words ÷ 5 = **50 WPM**
- Net = 50 − 1 = **49 WPM**

## Improve your speed

Use all ten fingers, keep your eyes on the screen, and practise accuracy first — speed follows.
''')

page(C,'cost-per-use',f'''
title: Cost Per Use Calculator
description: Work out the true cost per use of a purchase — clothing, gadgets, gym memberships and more.
category: everyday-life
keywords: [cost per use, cost per wear, value for money, is it worth it, gym membership cost per visit]
{U}
variables:
  - {{ id: p, label: Purchase price, family: currency, default: 120, min: 0, decimals: 2 }}
  - {{ id: run, label: Running or upkeep costs (total), family: currency, default: 0, min: 0, decimals: 2 }}
  - {{ id: u, label: Number of uses, default: 60, min: 1 }}
  - {{ id: cpu, label: Cost per use, family: currency, min: 0, decimals: 2 }}
equations:
  - cpu = (p + run) / u
faq:
  - q: What is cost per use?
    a: The total cost of owning something divided by how many times you use it. It shows real value better than the price tag.
  - q: Is a gym membership worth it?
    a: Divide the yearly cost by your visits. If it costs more per visit than a day pass, it isn't saving you money.
  - q: How many uses do I need for a target cost?
    a: Press × on Number of uses and type the cost per use you'd be happy with.
related: [everyday-life/unit-price, everyday-life/habit-cost]
''','''
## How to use this calculator

Enter the **price**, any **running costs** (cleaning, repairs, subscriptions) and how many times you expect to **use** it. The cost per use is calculated.

## Formula

<p class="formula">Cost per use = (price + running costs) ÷ number of uses</p>

## Example

A 120 pair of shoes worn 60 times costs **2.00 per wear**. A 40 pair worn only 5 times costs **8.00 per wear** — the "cheaper" option is far more expensive per use.

## Gym membership

A 600 yearly membership used 30 times = 20 per visit. Used 120 times = 5 per visit.
''')

page(C,'habit-cost',f'''
title: Daily Habit Cost Calculator
description: See how much a daily habit — coffee, snacks, cigarettes, subscriptions — costs per month, year and decade.
category: everyday-life
keywords: [habit cost, latte factor, daily coffee cost, how much do i spend, savings, small expenses]
{U}
variables:
  - {{ id: c, label: Cost each time, family: currency, default: 4.5, min: 0, decimals: 2 }}
  - {{ id: f, label: Times per week, default: 5, min: 0 }}
  - {{ id: m, label: Per month, family: currency, min: 0, decimals: 2 }}
  - {{ id: y, label: Per year, family: currency, min: 0, decimals: 2 }}
  - {{ id: dec, label: Over 10 years, family: currency, min: 0, decimals: 2 }}
equations:
  - y = c * f * 52
  - m = y / 12
  - dec = y * 10
faq:
  - q: Why do small daily costs add up?
    a: Something bought 5 days a week happens about 260 times a year.
  - q: What if I invested the money instead?
    a: Put the monthly amount into the SIP calculator to see how it could grow.
  - q: Does this include price rises?
    a: No. With inflation, the 10-year total would be higher.
related: [everyday-life/cost-per-use, finance/sip, finance/savings-goal]
''','''
## How to use this calculator

Enter the **cost** of the habit and how many **times per week** you do it. The monthly, yearly and ten-year totals are calculated.

## Example

A 4.50 coffee 5 times a week:

- **97.50 per month**
- **1,170 per year**
- **11,700 over 10 years**

## Putting it to work

Invested monthly at 8% a year instead, 97.50 a month grows to roughly 17,800 over 10 years. Try different amounts in the [SIP calculator](/finance/sip/).
''')

r=16/9
page(C,'tv-size',f'''
title: TV Size & Viewing Distance Calculator
description: Find a screen's width and height from its diagonal and aspect ratio — plus the recommended viewing distance.
category: everyday-life
keywords: [tv size calculator, screen dimensions, viewing distance, tv width height, 55 inch tv size, aspect ratio]
{U}
variables:
  - {{ id: d, label: Screen diagonal, family: length, unit: in, default: 55, min: 0 }}
  - id: r
    label: Aspect ratio
    default: 1.7777778
    options:
      - {{ label: 16:9 (TVs, monitors), value: 1.7777778 }}
      - {{ label: 21:9 (ultrawide), value: 2.3333333 }}
      - {{ label: 4:3 (older screens), value: 1.3333333 }}
      - {{ label: 16:10 (laptops), value: 1.6 }}
  - {{ id: w, label: Screen width, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: h, label: Screen height, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: vd, label: Recommended viewing distance (4K), family: length, unit: m, imperialUnit: ft, min: 0 }}
equations:
  - w = d * r / sqrt(r^2 + 1)
  - h = d / sqrt(r^2 + 1)
  - vd = 1.2 * d
faq:
  - q: How wide is a 55-inch TV?
    a: A 16:9 55-inch screen is about 121.8 cm (47.9 in) wide and 68.5 cm (27 in) tall — the frame adds a little more.
  - q: How far should I sit from a TV?
    a: For 4K, around 1–1.5 times the diagonal gives an immersive view; for HD, 1.5–2.5 times.
  - q: What size TV for my room?
    a: Press × on the diagonal and enter your viewing distance to find a matching screen size.
related: [conversion/cm-to-inches, math/pythagorean-theorem]
''',f'''
## How to use this calculator

Enter the **diagonal** and choose the **aspect ratio**. The screen's width, height and a recommended viewing distance for 4K content are calculated.

## Formulas

<p class="formula">width = d × r ÷ √(r² + 1)   height = d ÷ √(r² + 1)</p>

## Common 16:9 sizes

| Diagonal | Width | Height |
|---|---|---|
| 32″ | {32*r/math.sqrt(r*r+1)*2.54:.1f} cm | {32/math.sqrt(r*r+1)*2.54:.1f} cm |
| 43″ | {43*r/math.sqrt(r*r+1)*2.54:.1f} cm | {43/math.sqrt(r*r+1)*2.54:.1f} cm |
| 55″ | {55*r/math.sqrt(r*r+1)*2.54:.1f} cm | {55/math.sqrt(r*r+1)*2.54:.1f} cm |
| 65″ | {65*r/math.sqrt(r*r+1)*2.54:.1f} cm | {65/math.sqrt(r*r+1)*2.54:.1f} cm |
| 75″ | {75*r/math.sqrt(r*r+1)*2.54:.1f} cm | {75/math.sqrt(r*r+1)*2.54:.1f} cm |

Measurements are for the visible screen; the bezel and stand add a few centimetres. Check the manufacturer's dimensions before buying furniture.
''')
print('everyday ok')

page(C,'commute-time',f'''
title: Commute Time Calculator (Hours per Year)
description: See how many hours and days per year you spend commuting — and what that time is worth.
category: everyday-life
keywords: [commute time calculator, hours commuting per year, travel time to work, commute cost, time value]
{U}
variables:
  - {{ id: m, label: One-way commute, suffix: minutes, default: 40, min: 0 }}
  - {{ id: d, label: Commuting days per week, default: 5, min: 0, max: 7 }}
  - {{ id: w, label: Working weeks per year, default: 46, min: 0, max: 52 }}
  - {{ id: v, label: Value of your time per hour, family: currency, default: 15, min: 0, decimals: 2 }}
  - {{ id: h, label: Hours per year, min: 0, decimals: 0 }}
  - {{ id: days, label: Full 24-hour days per year, min: 0, decimals: 1 }}
  - {{ id: val, label: Value of that time, family: currency, min: 0, decimals: 2 }}
equations:
  - h = m * 2 * d * w / 60
  - days = h / 24
  - val = h * v
faq:
  - q: How much time do I spend commuting?
    a: A 40-minute each-way commute, 5 days a week for 46 weeks, adds up to about 307 hours — nearly 13 full days a year.
  - q: How does remote work change this?
    a: Reduce the commuting days per week — two home-working days cut commuting time by 40%.
  - q: What value should I give my time?
    a: Your hourly pay is a common benchmark, or what you would pay to get that time back.
related: [everyday-life/fuel-cost, ecology/bike-vs-car, finance/hourly-to-salary]
''','''
## How to use this calculator

Enter your **one-way commute** in minutes, **days per week**, **working weeks** and an optional **value of your time**. Yearly hours, days and the value of that time are calculated.

## Example

40 minutes each way, 5 days a week, 46 weeks:

- **307 hours** per year
- **12.8 full days**
- Worth **4,600** at 15 per hour
''')
