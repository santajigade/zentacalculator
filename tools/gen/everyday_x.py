import sys, math, datetime as dt; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
f = lambda x, d=0: f"{x:,.{d}f}"

expand('everyday-life/age-calculator', '''
## Age in different units

| Age | Months | Weeks (approx.) | Days (approx.) | Hours (approx.) |
|---|---|---|---|---|
''' + ''.join(f"| {y} years | {y*12:,} | {y*365.25/7:,.0f} | {y*365.25:,.0f} | {y*365.25*24:,.0f} |\n" for y in [1, 5, 10, 18, 21, 30, 40, 50, 60, 75]) + '''
Exact days depend on how many leap years fall in the period. The calculator counts the real calendar days between the two dates.

## Birthdays on 29 February

People born on 29 February have a real birthday only in leap years. In common years most countries treat **1 March** as the legal birthday for age-based rules, though some use 28 February. The calculator counts a completed year on 1 March in non-leap years.

## Age for forms and eligibility

Many rules depend on age on a specific date, not today:

- **School admission**: age on a cut-off date, such as 1 April or 31 March.
- **Exams and government jobs**: age limits on a notified date, often 1 January or 1 August.
- **Retirement and pensions**: the month you reach the retirement age.
- **Insurance**: age last birthday or age next birthday, depending on the insurer.

Change the “Age on this date” field to the cut-off date to check.

## Age difference between two people

Enter the older person's date of birth and set the second date to the younger person's date of birth. The result is the exact age gap in years, months and days.

## Ages around the world

Most countries count age from zero at birth. Traditional East Asian age reckoning added a year at birth and at each New Year, but South Korea officially switched to the international method for legal purposes in 2023.
''', [
 ('How old am I in days?', 'Enter your date of birth and the calculator shows your age in days. A 30-year-old is roughly 10,950 days old, depending on leap years.'),
 ('How is age calculated exactly?', 'Completed years are counted when the birthday date is reached. Months are counted the same way, and days are the exact number of calendar days between the dates.'),
])

expand('everyday-life/commute-time', '''
## Yearly commute time

46 working weeks, 5 days a week:

| One-way commute | Hours per year | Full days per year | Working weeks (40 h) |
|---|---|---|---|
''' + ''.join(f"| {m} min | {m*2*5*46/60:,.0f} | {m*2*5*46/60/24:.1f} | {m*2*5*46/60/40:.1f} |\n" for m in [10, 20, 30, 45, 60, 90]) + '''
A one-hour commute each way adds up to more than **11 working weeks** a year.

## The real cost of commuting

Time is only part of it. Add:

- **Fuel or fares**: use the [fuel cost calculator](/everyday-life/fuel-cost/) for driving.
- **Vehicle wear**: maintenance, tyres and depreciation, often more than fuel per kilometre.
- **Parking and tolls**.
- **Health**: long commutes are linked with less sleep and less exercise.

## Comparing a job offer or a move

A higher salary with a longer commute may not be better. Divide your pay by the hours you spend **working plus commuting** to get your effective hourly rate:

- 50,000 a year, 40 h/week work + 5 h/week commute → about **21.4 per hour**
- 54,000 a year, 40 h/week work + 12.5 h/week commute → about **19.8 per hour**

The higher salary actually pays less for each hour of your time.

## Making commute time useful

- Public transport lets you read, learn or rest.
- Audiobooks and podcasts turn driving time into learning time.
- Cycling or walking part of the way adds exercise.
- Remote or hybrid days cut the total quickly — each home day saves 20% of a five-day commute.
''', [
 ('How many hours a year do I spend commuting?', 'Multiply your one-way time by 2, then by your commuting days. A 30-minute commute for 230 days is 230 hours a year.'),
 ('Is commuting time counted as work?', 'Usually not. Normal travel between home and your regular workplace is generally unpaid, though rules differ by country and contract.'),
])

expand('everyday-life/cost-per-use', '''
## Cheap vs quality: an example

| Item | Price | Lasts | Uses | Cost per use |
|---|---|---|---|---|
| Budget shoes | 40 | 6 months | 150 | 0.27 |
| Quality shoes | 120 | 3 years | 900 | 0.13 |
| Budget jacket | 60 | 2 winters | 120 | 0.50 |
| Quality jacket | 250 | 8 winters | 480 | 0.52 |

Quality pays off when it lasts much longer **and** you use it. The quality jacket is not cheaper per use unless it lasts 9 winters or more.

## Including running costs

For appliances and vehicles, upkeep often matters more than the purchase price:

- **Coffee machine**: price + capsules or beans + descaling.
- **Printer**: price + ink per page. Cheap printers often have the most expensive ink.
- **Car**: purchase + insurance + servicing + fuel, divided by kilometres driven.

Add the running costs over the item's life in the second field.

## Subscriptions

Subscriptions are easy to underuse. Divide the yearly cost by how many times you actually used it:

| Subscription | Yearly cost | Uses | Cost per use |
|---|---|---|---|
| Streaming service | 120 | 100 evenings | 1.20 |
| Gym | 480 | 30 visits | 16.00 |
| Language app | 80 | 200 sessions | 0.40 |

If the cost per use is higher than paying each time, switch to pay-as-you-go.

## Cost per wear for clothes

Fashion advisers often suggest aiming for a cost per wear under 1–2 in your currency for everyday items. Classic pieces that go with many outfits reach this quickly.
''', [
 ('What is cost per use?', 'The total cost of owning something divided by the number of times you use it. It shows the real value of a purchase.'),
 ('Should I include resale value?', 'Yes. If you can sell the item later, subtract the expected resale price from the total cost before dividing.'),
])

expand('everyday-life/date-plus-days', '''
## Common date offsets

Starting from 1 January:

| Add | Result |
|---|---|
''' + ''.join(f"| {n} days | {(dt.date(2027,1,1)+dt.timedelta(days=n)).strftime('%-d %B')} |\n" for n in [7, 14, 30, 45, 60, 90, 100, 180, 270, 365]) + '''
In a leap year, dates after 28 February shift by one day.

## Working days vs calendar days

Many deadlines count only **working days** (Monday to Friday, sometimes excluding public holidays). 10 working days is two calendar weeks; 30 working days is about six weeks. Use the [days between dates calculator](/everyday-life/days-between-dates/) to count working days.

## Notice periods and deadlines

- **Notice period**: a 30-day or 90-day notice starts from the day after you give notice in many contracts. Check your agreement.
- **Return windows**: “within 30 days of purchase” usually includes the purchase day.
- **Payment terms**: “net 30” means payment is due 30 days after the invoice date.
- **Visa stays**: some countries count the arrival day as day 1, so a 90-day stay ends on day 90, not 90 days later.

## Pregnancy and due dates

A typical due date is 280 days (40 weeks) after the first day of the last menstrual period. Your doctor or midwife will confirm it with a scan.
''', [
 ('What date is 90 days from today?', 'Enter today as the start date and 90 as the number of days. The calculator shows the exact date, accounting for month lengths and leap years.'),
 ('How do I subtract days from a date?', 'Enter a negative number of days, such as −30, to count backwards.'),
])

expand('everyday-life/days-between-dates', '''
## Days in each month

| Month | Days | Month | Days |
|---|---|---|---|
| January | 31 | July | 31 |
| February | 28 (29 in leap years) | August | 31 |
| March | 31 | September | 30 |
| April | 30 | October | 31 |
| May | 31 | November | 30 |
| June | 30 | December | 31 |

A year has 365 days, or 366 in a leap year. Leap years are divisible by 4, except century years not divisible by 400 — so 2000 was a leap year but 2100 will not be.

## Inclusive or exclusive?

The calculator counts the days **between** the two dates, so 1 to 2 January is 1 day. If you need to include both the start and end date — for hotel nights or leave days, for example — add 1.

## Business uses

- **Interest**: deposits and loans often charge interest by the exact number of days.
- **Invoices**: check whether a payment is late.
- **Project planning**: count working days to a delivery date.
- **Leave**: count the working days in a holiday.

## Public holidays

The working-days figure excludes Saturdays and Sundays only. Subtract any public holidays in the period yourself, as they differ by country and region.
''', [
 ('How many days are there between two dates?', 'Enter both dates and the calculator gives the exact number of calendar days, weeks, completed months and working days.'),
 ('How many working days are in a year?', 'About 260–262 weekdays, minus public holidays — typically 245–255 working days, depending on the country.'),
])

expand('everyday-life/days-until', '''
## How to count down

The countdown is the number of calendar days from today to the event date. If the event has already passed, the result is negative, showing how many days ago it was.

## Countdown milestones

| Days to go | Roughly |
|---|---|
| 365 | 1 year, or 52 weeks |
| 180 | 6 months, or about 26 weeks |
| 100 | just over 14 weeks |
| 30 | about 4 weeks, around 21–22 working days |
| 7 | 1 week, 5 working days |

## Planning backwards from an event

For a wedding, exam, trip or product launch, list the tasks and work back from the date:

| Time before | Typical tasks |
|---|---|
| 6–12 months | Book venues, flights and major suppliers |
| 3 months | Confirm details, send invitations, start revision |
| 1 month | Final payments, practise tests, packing list |
| 1 week | Confirm times, check documents, rest |

Use the [date plus days calculator](/everyday-life/date-plus-days/) to set each milestone date.

## Working days to go

Deadlines at work usually depend on working days rather than calendar days. The working-days figure counts Monday to Friday, so remove public holidays and planned leave for a realistic estimate.
''', [
 ('How many days until Christmas?', 'Set the event date to 25 December and the calculator shows the days, weeks and working days left.'),
 ('Does the countdown include today?', 'No. It counts full days from today to the event date. On the day before the event it shows 1.'),
])

apps = [('LED bulb', 10, 6), ('Ceiling fan', 75, 10), ('Wi-Fi router', 10, 24), ('Laptop', 60, 6), ('Desktop PC', 200, 6), ('Television (55-inch LED)', 100, 4), ('Refrigerator (average draw)', 150, 24), ('Washing machine', 500, 1), ('Electric kettle', 2000, 0.25), ('Air conditioner (1.5 ton)', 1500, 8), ('Space heater', 2000, 4), ('Electric water heater (geyser)', 2000, 1)]
rows = ''.join(f"| {n} | {w} W | {h} h | {w*h/1000:.2f} | {w*h/1000*30:.1f} |\n" for n, w, h in apps)
expand('everyday-life/electricity-cost', f'''
## Monthly energy use of common appliances

| Appliance | Power | Hours/day | kWh/day | kWh/month |
|---|---|---|---|---|
{rows}
Multiply the kWh per month by your electricity price to get the cost. Real power varies by model — check the label or use a plug-in energy meter.

## Appliances that cycle on and off

Refrigerators, air conditioners and water heaters do not run at full power all the time. Their **average** power is lower than the rating:

- A fridge rated 150 W may use 1–1.5 kWh a day.
- An inverter AC uses much less once the room reaches the set temperature.

For these, use the yearly energy figure on the energy label: kWh per year ÷ 365 = kWh per day.

## Tiered and time-of-use tariffs

Many utilities charge more per unit as you use more (slabs), or more at peak times. Use your **average** price per kWh — total bill ÷ total units — for a realistic estimate.

## Ways to cut your bill

- Replace old bulbs with LEDs — about 80% less energy for the same light.
- Set the AC to 24–26 °C; each degree lower adds roughly 5–10% to cooling energy.
- Switch off standby devices at the wall.
- Run washing machines and dishwashers full, on eco programmes.
- Choose appliances with a higher energy-efficiency star rating.
''', [
 ('How do I calculate electricity cost?', 'Power in watts × hours used ÷ 1,000 gives kWh. Multiply kWh by your price per kWh.'),
 ('How many units does a 1.5 ton AC use per hour?', 'About 1–1.5 kWh (units) per hour at full power. An inverter AC typically averages less once the room is cool.'),
], before='## Typical appliance power')

expand('everyday-life/fuel-cost', '''
## Fuel cost per 100 km

| Consumption | At 1.20 per litre | At 1.60 per litre | At 2.00 per litre |
|---|---|---|---|
''' + ''.join(f"| {c} L/100 km ({100/c:.1f} km/L) | {c*1.2:.2f} | {c*1.6:.2f} | {c*2.0:.2f} |\n" for c in [4, 5, 6, 7, 8, 10, 12]) + '''
## Converting fuel economy

If your car shows **km per litre** or **miles per gallon**, convert first:

- L/100 km = 100 ÷ km per litre
- L/100 km = 235.2 ÷ mpg (US)
- L/100 km = 282.5 ÷ mpg (UK)

Or use the [fuel economy converter](/everyday-life/fuel-economy/).

## Electric vehicles

For an EV, replace litres with kWh: consumption in kWh/100 km × electricity price. A typical EV uses 14–20 kWh per 100 km. At 0.15 per kWh, that is 2.10–3.00 per 100 km — often far cheaper than petrol.

## Round trips and real-world use

- Double the distance for a return trip.
- Motorway driving at high speed, air conditioning, heavy loads and roof boxes can raise consumption by 10–30%.
- City driving with lots of stopping uses more fuel than steady driving for most petrol and diesel cars.

## Splitting costs fairly

The “people sharing” field divides fuel equally. For long trips, many groups also add tolls and parking, and some include a small amount for vehicle wear.
''', [
 ('How do I calculate fuel cost for a trip?', 'Distance ÷ 100 × consumption (L/100 km) × price per litre. A 350 km trip at 7 L/100 km and 1.60 per litre costs about 39.20.'),
 ('How much fuel does a car use per km?', 'Divide L/100 km by 100. A car using 7 L/100 km uses 0.07 litres per kilometre.'),
], before='## Save fuel')

expand('everyday-life/fuel-economy', '''
## Why L/100 km and mpg feel different

Fuel use per distance (L/100 km) and distance per fuel (mpg, km/L) are inverses, so improvements look very different:

| Change | Fuel saved per 100 km |
|---|---|
| 10 → 15 km/L | 3.33 L |
| 20 → 25 km/L | 1.00 L |
| 15 → 20 mpg (US) | 3.92 L |
| 40 → 50 mpg (US) | 1.18 L |

Improving a thirsty car saves far more fuel than improving an already efficient one. This is why many countries use L/100 km.

## Measuring your real fuel economy

1. Fill the tank completely and reset the trip meter.
2. Drive normally until the tank is at least half empty.
3. Fill up again and note the litres added and the distance driven.
4. L/100 km = litres ÷ km × 100.

Repeat over a few tanks for a reliable average. Car trip computers can be optimistic by 3–10%.

## Typical values

| Vehicle | L/100 km | km/L | mpg (US) |
|---|---|---|---|
| Small petrol hatchback | 5–6 | 17–20 | 39–47 |
| Mid-size petrol sedan | 6–8 | 12.5–17 | 29–39 |
| Diesel SUV | 6–9 | 11–17 | 26–39 |
| Large petrol SUV / pickup | 10–14 | 7–10 | 17–24 |
| Hybrid | 4–5 | 20–25 | 47–59 |
''', [
 ('How do I convert km/L to L/100 km?', 'Divide 100 by km/L. 15 km/L is 6.67 L/100 km.'),
 ('What is 30 mpg in L/100 km?', '7.84 L/100 km for US gallons, or 9.42 L/100 km for UK gallons.'),
])

expand('everyday-life/grade-needed', '''
## Score needed on the final

Current grade 78%, final worth 30%:

| Target course grade | Score needed |
|---|---|
''' + ''.join(f"| {t}% | {(t-78*0.7)/0.3:.1f}% |\n" for t in [70, 75, 80, 85, 90]) + '''
A result over 100% means the target cannot be reached with this exam alone.

## How weighted grades work

Each part of a course counts for its weight. With coursework at 70% and a final exam at 30%:

<p class="formula">Course grade = Coursework × 0.70 + Final × 0.30</p>

Rearranging gives the score you need on the final:

<p class="formula">Needed = (Target − Current × (1 − w)) ÷ w</p>

## Several components left

If more than one assessment remains, combine them: treat the remaining work as one block with their total weight, and the score needed is the average you must achieve across them.

## Letter grades

Many schools map percentages to letters, for example:

| Percentage | Letter | GPA (4.0 scale) |
|---|---|---|
| 90–100 | A | 4.0 |
| 80–89 | B | 3.0 |
| 70–79 | C | 2.0 |
| 60–69 | D | 1.0 |
| Below 60 | F | 0 |

Scales vary by institution, and some use plus and minus grades. Check your syllabus.
''', [
 ('What do I need on my final to pass?', 'Set the target to the pass mark, for example 50% or 60%, and the calculator shows the minimum score needed.'),
 ('Is my current grade already weighted?', 'Use your average across the work completed so far, as a percentage. If your school reports a running weighted grade, use that.'),
], before='## Study planning')

expand('everyday-life/habit-cost', '''
## What daily habits cost

| Habit | Cost each time | Times/week | Per year | 10 years |
|---|---|---|---|---|
''' + ''.join(f"| {n} | {c:.2f} | {t} | {c*t*52:,.0f} | {c*t*52*10:,.0f} |\n" for n, c, t in [('Takeaway coffee', 4.5, 5), ('Lunch out', 12, 5), ('Food delivery', 25, 2), ('Energy drink', 2.5, 7), ('Cigarettes (pack)', 12, 7), ('Ride-hailing trip', 15, 4)]) + '''
## What if you invested it instead?

Money saved from a habit can grow. 4.50 a day, five days a week, is about 97 a month. Invested at 8% a year:

| Years | Total saved | Value at 8% |
|---|---|---|
''' + ''.join(f"| {y} | {97.5*12*y:,.0f} | {97.5*((1+.08/12)**(12*y)-1)/(.08/12):,.0f} |\n" for y in [5, 10, 20, 30]) + '''
See the [SIP calculator](/finance/sip/) to try your own numbers.

## Cutting back without quitting

- **Reduce frequency**: going from 5 to 3 times a week cuts the cost by 40%.
- **Swap**: make coffee at home on most days and keep the café for Fridays.
- **Batch**: cook once and take lunch for several days.
- **Pause subscriptions** you rarely use.

## Spending you value

Not every habit needs cutting. If a daily coffee genuinely improves your day, keep it and cut something you value less. The point is to choose consciously.
''', [
 ('How much does a daily coffee cost per year?', 'At 4.50 a day on 5 working days a week, about 1,170 a year.'),
 ('How do I work out the cost of a habit?', 'Multiply the cost each time by how often you do it per week, then by 52 for the year.'),
])

expand('everyday-life/hours-worked', '''
## Weekly hours from daily shifts

| Shift | Break | Hours per day | 5 days | 6 days |
|---|---|---|---|---|
''' + ''.join(f"| {a}–{b} | {br} min | {h:.2f} | {h*5:.2f} | {h*6:.2f} |\n" for a, b, br, h in [('9:00', '17:00', 30, 7.5), ('9:00', '17:30', 30, 8), ('8:00', '17:00', 60, 8), ('7:00', '15:30', 30, 8), ('10:00', '19:00', 60, 8), ('22:00', '06:00', 30, 7.5)]) + '''
## Night shifts

Shifts that cross midnight are handled automatically: 22:00 to 06:00 is 8 hours, not −16. Enter the times in 24-hour format or with AM/PM.

## Rounding time

Some employers round clock-in and clock-out times to the nearest 5, 10 or 15 minutes. Rounding rules must usually be applied fairly in both directions. Keep your own record so you can check your pay.

## Weekly timesheet

To total a week, calculate each day and add them up, or use the decimal hours:

| Day | Start | End | Break | Hours |
|---|---|---|---|---|
| Mon | 9:00 | 17:30 | 30 min | 8.00 |
| Tue | 9:00 | 18:15 | 45 min | 8.50 |
| Wed | 8:30 | 17:00 | 30 min | 8.00 |
| Thu | 9:00 | 17:30 | 30 min | 8.00 |
| Fri | 9:00 | 15:00 | 0 min | 6.00 |
| **Total** | | | | **38.50** |
''', [
 ('How do I calculate hours worked with a lunch break?', 'Subtract the start time from the end time, then subtract the unpaid break. 9:00 to 17:30 with 30 minutes off is 8 hours.'),
 ('How do I convert 7 hours 45 minutes to decimal?', 'Divide the minutes by 60: 45 ÷ 60 = 0.75, so 7.75 hours.'),
], before='## Overtime')

expand('everyday-life/reading-time', '''
## Reading time for common lengths

| Words | Example | At 200 wpm | At 238 wpm | At 300 wpm |
|---|---|---|---|---|
''' + ''.join(f"| {w:,} | {n} | {w/200:.0f} min | {w/238:.0f} min | {w/300:.0f} min |\n" for w, n in [(500, 'Short blog post'), (1500, 'Long article'), (5000, 'Report or long-read'), (20000, 'Short e-book'), (80000, 'Typical novel'), (180000, 'Long novel')]) + '''
238 words per minute is the average for silent reading of non-fiction in English, from a 2019 review of 190 studies (Brysbaert).

## Reading speed by purpose

| Purpose | Typical speed |
|---|---|
| Studying difficult material | 100–200 wpm |
| Average adult reading | 200–260 wpm |
| Skimming | 400–700 wpm |
| Reading aloud / speaking | 130–160 wpm |

Very high “speed-reading” rates usually come at the cost of understanding.

## Estimating words in a book

Multiply pages by words per page. A typical paperback has about 250–300 words per page, so a 320-page book is roughly 80,000–96,000 words.

## Reading time on websites

Showing “5 min read” at the top of an article helps readers decide whether to start. Most publishers use 200–250 wpm and round up to the nearest minute.
''', [
 ('How long does it take to read 1,000 words?', 'About 4–5 minutes at an average reading speed of 200–238 words per minute.'),
 ('How long is a 2,000-word speech?', 'About 13–15 minutes at a speaking pace of 130–150 words per minute.'),
], before='## Speech planning')

expand('everyday-life/rent-split', '''
## Other fair ways to split rent

| Method | How it works | Best for |
|---|---|---|
| Equal split | Total ÷ number of people | Similar rooms |
| By room size (this calculator) | Common share split equally, private share by area | Rooms of different sizes |
| By features | Add premiums for an en-suite, balcony or parking | Rooms with different amenities |
| By income | Each pays a share in proportion to income | Couples |

## Adjusting for features

After the size-based split, you can move a fixed amount between rooms for extras. For example, if Room 1 has a private bathroom, it might pay 5–10% more of the rent, taken off the other rooms equally.

## Couples sharing a room

If two people share one room, decide whether the room pays one share or whether common areas are split per person. Splitting common areas per person is usually fairer, since two people use the kitchen and living room more.

## Bills and utilities

Electricity, internet and water are usually split **equally per person**, not by room size, because use depends on people. Add them separately from rent.

## Put it in writing

Agree the split before moving in and write it down, including how bills are paid, what happens when someone leaves and how the deposit is shared.
''', [
 ('How do you split rent fairly with different room sizes?', 'Split a share of the rent for common areas equally, then split the rest in proportion to each private room’s floor area.'),
 ('What share should I use for common areas?', 'Often 30–50%. Use more if the kitchen and living room are large and used a lot; less if people mostly stay in their rooms.'),
])

expand('everyday-life/sleep-calculator', '''
## Bedtimes for common wake-up times

Including 15 minutes to fall asleep:

| Wake-up time | 6 cycles (9 h) | 5 cycles (7.5 h) | 4 cycles (6 h) |
|---|---|---|---|
''' + ''.join(f"| {w} | {b6} | {b5} | {b4} |\n" for w, b6, b5, b4 in [('5:30', '20:15', '21:45', '23:15'), ('6:00', '20:45', '22:15', '23:45'), ('6:30', '21:15', '22:45', '0:15'), ('7:00', '21:45', '23:15', '0:45'), ('7:30', '22:15', '23:45', '1:15'), ('8:00', '22:45', '0:15', '1:45')]) + '''
## How much sleep do you need?

| Age group | Recommended hours per night |
|---|---|
| Teenagers (13–18) | 8–10 |
| Adults (18–64) | 7–9 |
| Older adults (65+) | 7–8 |

These ranges come from the US National Sleep Foundation and the American Academy of Sleep Medicine. Five cycles (7.5 hours) suits many adults.

## Cycles are an average

Sleep cycles last about 80–110 minutes and change through the night. Treat the 90-minute cycle as a guide. If you often wake before the alarm feeling refreshed, your body has found its own rhythm.

## When to seek help

Talk to a doctor if you snore loudly, stop breathing during sleep, feel very sleepy in the day despite enough hours, or have trouble sleeping most nights for weeks.
''', [
 ('What time should I go to bed to wake up at 6 AM?', 'Around 10:15 PM for five 90-minute cycles, or 8:45 PM for six, allowing 15 minutes to fall asleep.'),
 ('Is 6 hours of sleep enough?', 'For most adults, no. The recommended range is 7–9 hours a night.'),
], before='## Better sleep habits')

expand('everyday-life/time-duration', '''
## Minutes to decimal hours

| Minutes | Decimal hours | Minutes | Decimal hours |
|---|---|---|---|
''' + ''.join(f"| {m} | {m/60:.2f} | {m+30} | {(m+30)/60:.2f} |\n" for m in [5, 10, 15, 20, 25, 30]) + '''
## Adding and subtracting times

To add times, add the hours and minutes separately and carry over every 60 minutes:

- 2 h 45 min + 1 h 30 min = 3 h 75 min = **4 h 15 min**

To subtract, borrow 60 minutes from the hours if needed:

- 5 h 10 min − 2 h 40 min = 4 h 70 min − 2 h 40 min = **2 h 30 min**

## Durations across midnight

The calculator assumes the end time is after the start time on a 24-hour clock. From 22:30 to 06:45 is 8 h 15 min. For periods longer than 24 hours, use the [days between dates calculator](/everyday-life/days-between-dates/).

## Uses

- Shift lengths and timesheets — see the [hours worked calculator](/everyday-life/hours-worked/).
- Flight and travel times (watch for time zones).
- Sleep duration.
- Parking and rental periods.
''', [
 ('How many hours are between 10:30 PM and 6:45 AM?', '8 hours 15 minutes, or 8.25 hours.'),
 ('How do I convert decimal hours to minutes?', 'Multiply the decimal part by 60. 3.4 hours is 3 hours and 24 minutes.'),
], before='## Converting decimal hours')

expand('everyday-life/tip-calculator', '''
## Tipping customs around the world

| Country / region | Restaurants | Notes |
|---|---|---|
| United States | 15–20% | Tips are a large part of servers' pay |
| Canada | 15–20% | Similar to the US |
| United Kingdom | 10–12.5% | Often added as a service charge |
| Europe (most) | Round up to 5–10% | Service is often included |
| India | 5–10% | Check for a service charge first |
| Australia, New Zealand | Optional | Wages do not rely on tips |
| Japan | Not expected | Tipping can cause confusion |

Customs change, so check locally.

## Tip before or after tax?

Etiquette guides usually suggest tipping on the **pre-tax** amount. Tipping on the total is more generous and simpler. The difference is small: on an 85 bill with 8% tax, 15% before tax is 12.75 and after tax is 13.77.

## Service charge already included?

Check the bill for “service charge”, “gratuity” or “service included”. If it is there, an extra tip is not expected unless the service was exceptional.

## Splitting unevenly

If some people ordered much more, split the bill by what each ordered first, then apply the tip percentage to each person's share.

## Other services

| Service | Common tip (US) |
|---|---|
| Taxi / ride-hailing | 10–20% |
| Hairdresser | 15–20% |
| Food delivery | 10–20% or a fixed amount |
| Hotel housekeeping | A small amount per night |
''', [
 ('How much is a 20% tip on 50?', '10, making the total 60.'),
 ('How do I calculate a 15% tip quickly?', 'Find 10% by moving the decimal point one place, then add half of it. On 60: 6 + 3 = 9.'),
])

expand('everyday-life/tv-size', '''
## Screen dimensions by size (16:9)

| Diagonal | Width | Height | 4K viewing distance | 1080p viewing distance |
|---|---|---|---|---|
''' + ''.join(f"| {d}″ | {d*16/math.hypot(16,9)*2.54:.0f} cm ({d*16/math.hypot(16,9):.1f}″) | {d*9/math.hypot(16,9)*2.54:.0f} cm ({d*9/math.hypot(16,9):.1f}″) | {1.2*d*2.54/100:.1f} m | {1.6*d*2.54/100:.1f} m |\n" for d in [32, 43, 50, 55, 65, 75, 85]) + '''
## Choosing a size for your room

Work backwards from your seating distance:

| Viewing distance | Suggested size (4K) |
|---|---|
| 1.5 m (5 ft) | 50″ |
| 2.0 m (6.5 ft) | 65″ |
| 2.5 m (8 ft) | 75–85″ |
| 3.0 m (10 ft) | 85″ or larger |

These follow the common guideline of sitting about 1–1.5 times the screen diagonal away for 4K. Cinema fans often sit closer for a more immersive view.

## Wall mounting height

The centre of the screen should be close to eye level when seated, typically **100–110 cm** from the floor. Mounting high above a fireplace often causes neck strain.

## Will it fit?

Measure the space and compare it with the **width** and **height** above, then add the bezel and stand. Many TV stands also need extra width beyond the screen.
''', [
 ('How wide is a 55-inch TV?', 'About 121.8 cm (47.9 inches) for the screen, plus a small bezel.'),
 ('How far should I sit from a 65-inch TV?', 'About 2–2.5 m (6.5–8 ft) for 4K content.'),
])

expand('everyday-life/typing-speed', '''
## Typing speed benchmarks

| Level | Net WPM |
|---|---|
| Beginner | Under 30 |
| Average adult | 35–45 |
| Good / office work | 50–70 |
| Fast | 70–90 |
| Professional typist | 90+ |

Many data-entry and transcription jobs ask for 50–60 WPM with high accuracy.

## Accuracy

<p class="formula">Accuracy = (characters − errors) ÷ characters × 100</p>

1,250 characters with 5 errors is 99.6% accuracy. Aim for 95% or more before trying to type faster.

## Words per minute vs keystrokes per hour

Data-entry tests sometimes use **keystrokes per hour (KPH)**: KPH = characters per minute × 60. 250 characters per minute is 15,000 KPH.

## Practice plan

- Learn proper finger placement on the home row (ASDF JKL;).
- Practise 10–15 minutes a day rather than one long session.
- Focus on accuracy first; speed follows.
- Use real text that matches your work, such as emails or code.
''', [
 ('What is a good typing speed?', 'Around 40 WPM is average; 60 WPM or more is considered good for most office jobs.'),
 ('Why is one word counted as five characters?', 'It standardises results so that long and short words count fairly. Spaces and punctuation are included in the five.'),
], before='## Improve your speed')

expand('everyday-life/unit-price', '''
## Bulk vs small packs: examples

| Product | Small pack | Large pack | Saving per unit |
|---|---|---|---|
| Rice | 1 kg for 2.40 | 5 kg for 10.50 | 12.5% |
| Shampoo | 250 ml for 3.20 | 750 ml for 8.10 | 15.6% |
| Coffee | 200 g for 5.50 | 500 g for 12.00 | 12.7% |
| Detergent | 1 L for 4.00 | 3 L for 13.50 | none — 12.5% more expensive |

Bigger is not always cheaper. Always check the unit price.

## Converting units before comparing

Make sure both products use the same unit:

- 1 kg = 1,000 g, 1 L = 1,000 ml
- 1 lb = 453.6 g, 1 oz = 28.35 g
- 1 US fl oz = 29.57 ml

If one pack is in grams and the other in ounces, convert first with the [kg to lb converter](/conversion/kg-to-lb/).

## When the bulk deal is not worth it

- **It will spoil** before you use it.
- **You do not have space** to store it.
- **Multi-buy offers** (“3 for 2”) only help if you would have bought three anyway.
- **Concentrated products** may give more uses per ml — compare cost per wash or per serving.

## Price per use

For detergents, dishwasher tablets and similar items, compare cost per wash rather than per gram. A pricier concentrate can be cheaper per use.
''', [
 ('How do I calculate unit price?', 'Divide the price by the quantity. 4.50 for 750 g is 0.006 per gram, or 0.60 per 100 g.'),
 ('Is the shelf label unit price reliable?', 'Usually, but check that both products use the same unit (per 100 g vs per kg) and that the label matches the current price.'),
], before='## Tips')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/everyday-life/*.mdx')):
    c = 'everyday-life/' + os.path.basename(p)[:-4]; print(c, words(c))
