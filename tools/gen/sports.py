import math
from page import page
C='sports'; U='updated: 2026-10-27'

page(C,'pace-calculator',f'''
title: Running Pace Calculator
description: Calculate running pace per km or mile, finish time or distance — enter any two.
category: sports
keywords: [pace calculator, running pace, min per km, min per mile, race time, 5k pace, marathon pace]
{U}
featured: true
variables:
  - {{ id: d, label: Distance, family: length, unit: km, imperialUnit: mi, default: 10, min: 0 }}
  - {{ id: t, label: Finish time, family: seconds, unit: min, default: 55, min: 0 }}
  - {{ id: pk, label: Pace per km, suffix: min/km, min: 0, decimals: 2 }}
  - {{ id: pm, label: Pace per mile, suffix: min/mile, min: 0, decimals: 2 }}
  - {{ id: v, label: Average speed, family: velocity, unit: kmh, imperialUnit: mph, min: 0 }}
equations:
  - pk = t / 60 / (d / 1000)
  - pm = pk * 1.609344
  - v = d / t
faq:
  - q: How do I calculate running pace?
    a: Divide your time by the distance. 55 minutes for 10 km is 5.5 minutes per km — 5:30 per km.
  - q: How do I read decimal pace?
    a: Multiply the decimal part by 60. 5.5 min/km = 5 min 30 s per km.
  - q: What pace do I need for a sub-2-hour half marathon?
    a: About 5:41 per km (9:09 per mile).
related: [sports/race-time-predictor, sports/pace-speed-converter, physics/speed-distance-time]
''','''
## How to use this calculator

Enter any **two** of distance, finish time and pace. Time is entered in minutes (or switch to hours or seconds). Pace is shown as decimal minutes — 5.5 = 5:30.

## Formula

<p class="formula">pace = time ÷ distance</p>

## Example

10 km in 55 minutes:

- Pace = **5.50 min/km** (5:30 per km) = **8.85 min/mile** (8:51 per mile)
- Speed = **10.9 km/h**

## Popular goal paces

| Goal | Pace per km | Pace per mile |
|---|---|---|
| 5K in 25:00 | 5:00 | 8:03 |
| 10K in 50:00 | 5:00 | 8:03 |
| Half marathon in 2:00 | 5:41 | 9:09 |
| Marathon in 4:00 | 5:41 | 9:09 |
| Marathon in 3:30 | 4:59 | 8:01 |
''')

T1=25;D1=5;D2=21.0975
page(C,'race-time-predictor',f'''
title: Race Time Predictor (Riegel Formula)
description: Predict your finish time for a 5K, 10K, half marathon or marathon from a recent race result.
category: sports
keywords: [race time predictor, riegel formula, marathon predictor, half marathon time, running predictor]
{U}
variables:
  - {{ id: d1, label: Recent race distance, family: length, unit: km, imperialUnit: mi, default: 5, min: 0 }}
  - {{ id: t1, label: Recent race time, family: seconds, unit: min, default: 25, min: 0 }}
  - {{ id: d2, label: Target race distance, family: length, unit: km, imperialUnit: mi, default: 21.0975, min: 0 }}
  - {{ id: t2, label: Predicted time, family: seconds, unit: min, min: 0 }}
equations:
  - t2 = t1 * (d2 / d1)^1.06
faq:
  - q: What is the Riegel formula?
    a: T₂ = T₁ × (D₂ ÷ D₁)^1.06, published by Peter Riegel in 1977. It assumes you slow slightly as distance increases.
  - q: How accurate is it?
    a: Reasonably good for well-trained runners between about 3 and 50 km. Marathon predictions are often optimistic for runners with low weekly mileage.
  - q: Which race should I use?
    a: A recent, all-out effort over a distance close to your target gives the best prediction.
related: [sports/pace-calculator, sports/pace-speed-converter]
''',f'''
## How to use this calculator

Enter a **recent race distance and time** and your **target distance**. The predicted finish time is calculated in minutes (switch to hours if you prefer).

## Formula

<p class="formula">T₂ = T₁ × (D₂ ÷ D₁)<sup>1.06</sup></p>

## Example

A 25:00 5K predicts:

| Race | Predicted time |
|---|---|
| 10K | {T1*(10/5)**1.06:.1f} min |
| Half marathon | {T1*(21.0975/5)**1.06:.1f} min ({T1*(21.0975/5)**1.06/60:.2f} h) |
| Marathon | {T1*(42.195/5)**1.06:.1f} min ({T1*(42.195/5)**1.06/60:.2f} h) |
''')

page(C,'pace-speed-converter',f'''
title: Pace to Speed Converter (Treadmill)
description: Convert running pace (min/km or min/mile) to speed in km/h or mph — and back. Ideal for treadmills.
category: sports
keywords: [pace to speed, min per km to km/h, treadmill speed, mph to pace, pace converter]
{U}
variables:
  - {{ id: pk, label: Pace per km, suffix: min/km, default: 6, min: 0.01 }}
  - {{ id: pm, label: Pace per mile, suffix: min/mile, min: 0.01 }}
  - {{ id: kmh, label: Speed, suffix: km/h, min: 0 }}
  - {{ id: mph, label: Speed, suffix: mph, min: 0 }}
equations:
  - kmh = 60 / pk
  - pm = pk * 1.609344
  - mph = 60 / pm
faq:
  - q: How do I convert pace to km/h?
    a: Divide 60 by your pace in minutes per km. A 6:00 min/km pace is 10 km/h.
  - q: What treadmill speed is a 5:00 pace?
    a: 12 km/h, or 7.46 mph.
  - q: Should I set an incline on the treadmill?
    a: Many runners use a 1% incline to better match the effort of running outdoors.
related: [sports/pace-calculator, conversion/speed-converter]
''','''
## How to use this converter

Type into **any** field — pace per km, pace per mile, km/h or mph. Pace is in decimal minutes (6.5 = 6:30).

## Quick table

| min/km | km/h | min/mile | mph |
|---|---|---|---|
| 4:00 | 15.0 | 6:26 | 9.3 |
| 5:00 | 12.0 | 8:03 | 7.5 |
| 6:00 | 10.0 | 9:39 | 6.2 |
| 7:00 | 8.6 | 11:16 | 5.3 |
| 8:00 | 7.5 | 12:52 | 4.7 |
''')

page(C,'one-rep-max',f'''
title: One-Rep Max (1RM) Calculator
description: Estimate your one-rep max from the weight and reps you can lift, with training percentages.
category: sports
keywords: [one rep max, 1rm calculator, max lift, epley formula, bench press max, squat max, strength training]
{U}
featured: true
variables:
  - {{ id: w, label: Weight lifted, family: mass, unit: kg, imperialUnit: lb, default: 80, min: 0 }}
  - {{ id: r, label: Reps completed, default: 6, min: 1, max: 15 }}
  - {{ id: rm, label: Estimated 1RM, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
  - {{ id: w80, label: 80% of 1RM (about 8 reps), family: mass, unit: kg, imperialUnit: lb, min: 0 }}
  - {{ id: w70, label: 70% of 1RM (about 12 reps), family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - rm = w * (1 + r / 30)
  - w80 = rm * 0.8
  - w70 = rm * 0.7
faq:
  - q: How is one-rep max estimated?
    a: This uses the Epley formula, 1RM = weight × (1 + reps ÷ 30). It is most accurate for sets of 2–10 reps.
  - q: Is it safe to test a true 1RM?
    a: Maximal lifts carry injury risk. Estimating from a submaximal set is safer, especially for beginners. Always use a spotter.
  - q: What percentage for strength vs hypertrophy?
    a: Roughly 80–90% of 1RM for strength (3–6 reps) and 65–80% for muscle growth (6–12 reps).
related: [health/calories-burned, sports/jump-height]
''',f'''
## How to use this calculator

Enter the **weight** and the number of **reps** you completed with good form. Your estimated 1RM and common training weights are calculated.

## Formula (Epley)

<p class="formula">1RM = weight × (1 + reps ÷ 30)</p>

## Example

80 kg for 6 reps: 1RM = 80 × 1.2 = **96 kg**

## Training percentages

| % of 1RM | Typical reps |
|---|---|
| 95% | 2 |
| 90% | 3–4 |
| 85% | 5–6 |
| 80% | 7–8 |
| 75% | 9–10 |
| 70% | 11–12 |
''')

page(C,'cricket-run-rate',f'''
title: Cricket Run Rate Calculator
description: Calculate a cricket team's run rate (runs per over) from runs scored and overs or balls faced.
category: sports
keywords: [run rate calculator, cricket run rate, runs per over, crr, current run rate, t20 run rate]
{U}
featured: true
variables:
  - {{ id: runs, label: Runs scored, default: 168, min: 0 }}
  - {{ id: balls, label: Balls faced, default: 120, min: 1 }}
  - {{ id: ov, label: Overs (decimal), min: 0, decimals: 3 }}
  - {{ id: rr, label: Run rate (runs per over), min: 0, decimals: 2 }}
equations:
  - ov = balls / 6
  - rr = runs / ov
faq:
  - q: How is run rate calculated?
    a: Run rate = runs ÷ overs. Overs must be decimal — 15.3 overs (15 overs and 3 balls) is 15.5 overs, so enter the balls (93) to avoid errors.
  - q: What is a good T20 run rate?
    a: A rate of 8–9 runs per over is competitive in many T20 matches today; above 10 is very strong.
  - q: How do I convert overs to balls?
    a: Balls = completed overs × 6 + extra balls. 15.3 overs = 93 balls.
related: [sports/required-run-rate, sports/net-run-rate, sports/cricket-batting]
''','''
## How to use this calculator

Enter the **runs scored** and **balls faced** (or overs × 6). The overs and run rate are calculated.

## Formula

<p class="formula">Run rate = runs ÷ (balls ÷ 6)</p>

## Example

168 runs in 20 overs (120 balls) → run rate **8.40**.

## Overs notation

In cricket, "15.3 overs" means 15 overs and 3 balls — not 15.3 as a decimal. It equals 93 balls or 15.5 decimal overs.
''')

page(C,'required-run-rate',f'''
title: Required Run Rate Calculator (Cricket)
description: Calculate the runs per over needed to chase a target with the balls remaining.
category: sports
keywords: [required run rate, rrr, cricket chase, runs needed per over, target calculator]
{U}
variables:
  - {{ id: tgt, label: Target, default: 181, min: 0 }}
  - {{ id: runs, label: Current score, default: 92, min: 0 }}
  - {{ id: bl, label: Balls remaining, default: 54, min: 1 }}
  - {{ id: need, label: Runs needed, min: 0, decimals: 0 }}
  - {{ id: rrr, label: Required run rate, min: 0, decimals: 2 }}
  - {{ id: rpb, label: Runs needed per ball, min: 0, decimals: 2 }}
equations:
  - need = tgt - runs
  - rrr = need / (bl / 6)
  - rpb = need / bl
faq:
  - q: How is the required run rate calculated?
    a: Required run rate = runs still needed ÷ overs remaining.
  - q: What is the target?
    a: One more than the opposition's total — the score needed to win.
  - q: What about rain-reduced matches?
    a: Revised targets use the DLS method, which is not covered by this calculator.
related: [sports/cricket-run-rate, sports/net-run-rate]
''','''
## How to use this calculator

Enter the **target**, the **current score** and the **balls remaining**. Runs needed, required run rate and runs per ball are calculated.

## Formula

<p class="formula">RRR = (target − score) ÷ (balls remaining ÷ 6)</p>

## Example

Chasing 181, the team is 92 with 9 overs (54 balls) left:

- Need **89** runs
- Required rate = 89 ÷ 9 = **9.89** per over
''')

page(C,'cricket-batting',f'''
title: Cricket Batting Average & Strike Rate Calculator
description: Calculate a batter's average, strike rate and boundary percentage from runs, dismissals and balls faced.
category: sports
keywords: [batting average, strike rate, cricket batting, batting stats, runs per dismissal]
{U}
variables:
  - {{ id: runs, label: Runs scored, default: 1240, min: 0 }}
  - {{ id: outs, label: Times dismissed, default: 28, min: 0.0001 }}
  - {{ id: balls, label: Balls faced, default: 980, min: 1 }}
  - {{ id: avg, label: Batting average, min: 0, decimals: 2 }}
  - {{ id: sr, label: Strike rate, min: 0, decimals: 2 }}
equations:
  - avg = runs / outs
  - sr = runs / balls * 100
faq:
  - q: How is batting average calculated?
    a: Total runs divided by the number of times the batter was out. Not-out innings add runs but not dismissals.
  - q: What is strike rate?
    a: Runs scored per 100 balls faced — a measure of scoring speed.
  - q: What is a good batting average?
    a: In Test cricket, an average above 40 is very good and above 50 is world class.
related: [sports/cricket-run-rate, sports/bowling-economy]
''','''
## How to use this calculator

Enter **runs**, **dismissals** and **balls faced**. The batting average and strike rate are calculated.

## Formulas

<p class="formula">Average = runs ÷ dismissals   Strike rate = runs ÷ balls × 100</p>

## Example

1,240 runs, 28 dismissals, 980 balls:

- Average = **44.29**
- Strike rate = **126.53**
''')

page(C,'bowling-economy',f'''
title: Cricket Bowling Economy, Average & Strike Rate
description: Calculate a bowler's economy rate, bowling average and strike rate from runs, wickets and balls bowled.
category: sports
keywords: [bowling economy, bowling average, bowling strike rate, cricket bowling stats, economy rate]
{U}
variables:
  - {{ id: runs, label: Runs conceded, default: 480, min: 0 }}
  - {{ id: wk, label: Wickets taken, default: 20, min: 0.0001 }}
  - {{ id: balls, label: Balls bowled, default: 432, min: 1 }}
  - {{ id: econ, label: Economy rate (runs per over), min: 0, decimals: 2 }}
  - {{ id: avg, label: Bowling average (runs per wicket), min: 0, decimals: 2 }}
  - {{ id: sr, label: Strike rate (balls per wicket), min: 0, decimals: 1 }}
equations:
  - econ = runs / (balls / 6)
  - avg = runs / wk
  - sr = balls / wk
faq:
  - q: What is economy rate?
    a: Runs conceded per over bowled. Lower is better.
  - q: What is bowling average?
    a: Runs conceded per wicket. Lower is better — under 25 is excellent in Test cricket.
  - q: What is bowling strike rate?
    a: Balls bowled per wicket taken — how often a bowler takes a wicket.
related: [sports/cricket-batting, sports/cricket-run-rate]
''','''
## How to use this calculator

Enter **runs conceded**, **wickets** and **balls bowled**. Economy, average and strike rate are calculated.

## Example

480 runs, 20 wickets, 432 balls (72 overs):

- Economy = **6.67**
- Average = **24.00**
- Strike rate = **21.6** balls per wicket
''')

page(C,'baseball-era',f'''
title: ERA Calculator (Earned Run Average)
description: Calculate a baseball pitcher's earned run average (ERA) and WHIP from innings pitched.
category: sports
keywords: [era calculator, earned run average, baseball pitching stats, whip, innings pitched]
{U}
variables:
  - {{ id: er, label: Earned runs, default: 45, min: 0 }}
  - {{ id: ip, label: Innings pitched (decimal), default: 150, min: 0.0001 }}
  - {{ id: h, label: Hits allowed, default: 130, min: 0 }}
  - {{ id: bb, label: Walks allowed, default: 40, min: 0 }}
  - {{ id: era, label: ERA, min: 0, decimals: 2 }}
  - {{ id: whip, label: WHIP, min: 0, decimals: 2 }}
equations:
  - era = 9 * er / ip
  - whip = (h + bb) / ip
faq:
  - q: How is ERA calculated?
    a: ERA = 9 × earned runs ÷ innings pitched — the earned runs a pitcher allows per nine innings.
  - q: How do I enter partial innings?
    a: Each out is one third of an inning. 150⅓ innings = 150.333 and 150⅔ = 150.667. Scorebooks often write these as 150.1 and 150.2.
  - q: What is a good ERA?
    a: In Major League Baseball, an ERA under 3.00 is excellent and around 4.00 is roughly average.
related: [sports/baseball-batting, sports/win-percentage]
''','''
## How to use this calculator

Enter **earned runs**, **innings pitched** (decimal), **hits** and **walks**. ERA and WHIP are calculated.

## Formulas

<p class="formula">ERA = 9 × ER ÷ IP   WHIP = (H + BB) ÷ IP</p>

## Example

45 earned runs in 150 innings, 130 hits and 40 walks:

- ERA = **2.70**
- WHIP = **1.13**
''')

ab,hh,bb,hbp,sf=500,150,60,5,5
page(C,'baseball-batting',f'''
title: Baseball Batting Average & OBP Calculator
description: Calculate batting average, on-base percentage (OBP) and more from hits, at-bats and walks.
category: sports
keywords: [batting average calculator, obp, on base percentage, baseball stats, hits at bats]
{U}
variables:
  - {{ id: ab, label: At-bats (AB), default: 500, min: 1 }}
  - {{ id: h, label: Hits (H), default: 150, min: 0 }}
  - {{ id: bb, label: Walks (BB), default: 60, min: 0 }}
  - {{ id: hbp, label: Hit by pitch (HBP), default: 5, min: 0 }}
  - {{ id: sf, label: Sacrifice flies (SF), default: 5, min: 0 }}
  - {{ id: avg, label: Batting average, min: 0, decimals: 3 }}
  - {{ id: obp, label: On-base percentage, min: 0, decimals: 3 }}
equations:
  - avg = h / ab
  - obp = (h + bb + hbp) / (ab + bb + hbp + sf)
faq:
  - q: How is batting average calculated?
    a: Hits divided by at-bats. Walks, hit-by-pitches and sacrifices do not count as at-bats.
  - q: What is OBP?
    a: On-base percentage — how often a batter reaches base by a hit, walk or hit by pitch.
  - q: What is a good batting average?
    a: .300 or higher is excellent in professional baseball; around .250 is roughly average.
related: [sports/baseball-era, sports/win-percentage]
''',f'''
## How to use this calculator

Enter **at-bats**, **hits**, **walks**, **hit by pitch** and **sacrifice flies**. Batting average and on-base percentage are calculated.

## Formulas

<p class="formula">AVG = H ÷ AB   OBP = (H + BB + HBP) ÷ (AB + BB + HBP + SF)</p>

## Example

150 hits in 500 at-bats, 60 walks, 5 HBP, 5 sacrifice flies:

- AVG = **.300**
- OBP = **{(hh+bb+hbp)/(ab+bb+hbp+sf):.3f}**
''')

page(C,'golf-handicap',f'''
title: Golf Score Differential Calculator (Handicap)
description: Calculate a golf score differential from your adjusted score, course rating and slope rating — the basis of the World Handicap System.
category: sports
keywords: [golf handicap calculator, score differential, slope rating, course rating, world handicap system, whs]
{U}
variables:
  - {{ id: s, label: Adjusted gross score, default: 92, min: 0 }}
  - {{ id: cr, label: Course rating, default: 71.2, min: 0 }}
  - {{ id: sl, label: Slope rating, default: 128, min: 55, max: 155 }}
  - {{ id: pcc, label: Playing conditions adjustment (PCC), default: 0 }}
  - {{ id: sd, label: Score differential, decimals: 1 }}
equations:
  - sd = 113 / sl * (s - cr - pcc)
faq:
  - q: What is a score differential?
    a: A measure of how well you played relative to the course's difficulty, adjusted to a standard slope of 113.
  - q: How is the Handicap Index calculated?
    a: Under the World Handicap System, it is the average of the best 8 of your most recent 20 score differentials.
  - q: Where do I find course and slope rating?
    a: On the scorecard or the club's website, for the tees you played.
related: [sports/win-percentage]
''',f'''
## How to use this calculator

Enter your **adjusted gross score**, the **course rating** and **slope rating** for your tees, and any **PCC** adjustment (usually 0). The score differential is calculated.

## Formula

<p class="formula">Score differential = (113 ÷ slope) × (score − course rating − PCC)</p>

## Example

Score 92 on a course rated 71.2 with slope 128:

Differential = 113 ÷ 128 × 20.8 = **{113/128*20.8:.1f}**

Average your best 8 differentials from the last 20 rounds for your Handicap Index.
''')

page(C,'swim-pace',f'''
title: Swim Pace Calculator (per 100 m)
description: Calculate swimming pace per 100 m or 100 yd, total time or distance.
category: sports
keywords: [swim pace, pace per 100m, swimming calculator, swim time, triathlon swim, css]
{U}
variables:
  - {{ id: d, label: Distance, family: length, unit: m, imperialUnit: yd, default: 1500, min: 0 }}
  - {{ id: t, label: Total time, family: seconds, unit: min, default: 30, min: 0 }}
  - {{ id: p, label: Pace per 100 m, family: seconds, unit: s, min: 0 }}
equations:
  - p = t / (d / 100)
faq:
  - q: How do I calculate swim pace?
    a: Divide total time by the distance in hundreds. 30 minutes for 1,500 m is 2:00 per 100 m.
  - q: What is a good swim pace?
    a: Many adult fitness swimmers swim 2:00–2:30 per 100 m; competitive age-group triathletes are often under 1:45.
  - q: What is CSS?
    a: Critical Swim Speed — a threshold pace estimated from 400 m and 200 m time trials, used to set training intensity.
related: [sports/pace-calculator, sports/race-time-predictor]
''','''
## How to use this calculator

Enter the **distance** and **total time**. The pace per 100 m (or 100 yd if you switch units) is shown in seconds. Or enter a pace to predict your time.

## Example

1,500 m in 30 minutes → **120 s per 100 m** (2:00/100 m).

## Pool lengths

25 m and 50 m pools are common; US pools are often 25 yd. 100 yd ≈ 91.4 m.
''')

page(C,'cycling-gear-speed',f'''
title: Cycling Gear & Speed Calculator
description: Calculate bike speed from cadence, chainring, cog and wheel size — plus gear ratio and development.
category: sports
keywords: [bike gear calculator, cycling speed cadence, gear ratio, chainring cog, gear inches, development]
{U}
variables:
  - {{ id: cad, label: Cadence, suffix: rpm, default: 90, min: 0 }}
  - {{ id: cr, label: Chainring teeth, default: 50, min: 1 }}
  - {{ id: cg, label: Cog (sprocket) teeth, default: 15, min: 1 }}
  - id: wc
    label: Wheel / tyre size (circumference)
    default: 2.105
    options:
      - {{ label: 700×25c road (2.105 m), value: 2.105 }}
      - {{ label: 700×28c road (2.136 m), value: 2.136 }}
      - {{ label: 700×32c gravel (2.155 m), value: 2.155 }}
      - {{ label: 29×2.2 MTB (2.326 m), value: 2.326 }}
      - {{ label: 27.5×2.2 MTB (2.169 m), value: 2.169 }}
      - {{ label: 26×2.1 MTB (2.068 m), value: 2.068 }}
  - {{ id: gr, label: Gear ratio, min: 0, decimals: 2 }}
  - {{ id: dev, label: Development (distance per pedal turn), family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: v, label: Speed, family: velocity, unit: kmh, imperialUnit: mph, min: 0 }}
equations:
  - gr = cr / cg
  - dev = gr * wc
  - v = dev * cad / 60
faq:
  - q: How is cycling speed calculated from cadence?
    a: Speed = cadence × (chainring ÷ cog) × wheel circumference.
  - q: What is a good cadence?
    a: Many riders spin at 80–95 rpm on flat roads; climbing is often slower.
  - q: What is gear development?
    a: The distance the bike travels for one full turn of the pedals.
related: [sports/pace-speed-converter, conversion/speed-converter]
''',f'''
## How to use this calculator

Enter your **cadence**, **chainring** and **cog** teeth and choose your **wheel size**. The gear ratio, development and speed are calculated.

## Formula

<p class="formula">speed = cadence × (chainring ÷ cog) × wheel circumference</p>

## Example

50 × 15 gear, 700×25c wheel, 90 rpm:

- Ratio = **3.33**
- Development = **{50/15*2.105:.2f} m**
- Speed = **{50/15*2.105*90/60*3.6:.1f} km/h**
''')

page(C,'win-percentage',f'''
title: Win Percentage Calculator
description: Calculate a team's or player's win percentage from wins, losses and ties.
category: sports
keywords: [win percentage, winning percentage, win loss ratio, team record, standings]
{U}
variables:
  - {{ id: w, label: Wins, default: 42, min: 0 }}
  - {{ id: l, label: Losses, default: 28, min: 0 }}
  - {{ id: t, label: Ties / draws, default: 2, min: 0 }}
  - {{ id: pct, label: Win percentage (ties count as half), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: wl, label: Win–loss ratio, min: 0, decimals: 2 }}
equations:
  - pct = (w + t / 2) / (w + l + t)
  - wl = w / l
faq:
  - q: How is win percentage calculated?
    a: Wins (plus half of ties) divided by games played. US sports often show it as a decimal such as .583.
  - q: How are ties counted?
    a: Usually as half a win and half a loss, as here. Some leagues ignore ties — check your league's rules.
  - q: How many wins do I need for a target percentage?
    a: Press × on Wins and type the target percentage.
related: [sports/football-points, math/percentage]
''','''
## How to use this calculator

Enter **wins**, **losses** and **ties**. Win percentage and win–loss ratio are calculated.

## Formula

<p class="formula">Win % = (W + T/2) ÷ (W + L + T)</p>

## Example

42 wins, 28 losses, 2 ties: (42 + 1) ÷ 72 = **59.7%** (.597).
''')

page(C,'effective-field-goal',f'''
title: Basketball Shooting Calculator (FG%, eFG%, TS%)
description: Calculate field goal percentage, effective field goal percentage and true shooting percentage.
category: sports
keywords: [effective field goal percentage, efg, true shooting, ts%, fg%, basketball stats, shooting efficiency]
{U}
variables:
  - {{ id: fg, label: Field goals made (incl. 3-pointers), default: 8, min: 0 }}
  - {{ id: fga, label: Field goal attempts, default: 17, min: 1 }}
  - {{ id: tp, label: 3-pointers made, default: 3, min: 0 }}
  - {{ id: ft, label: Free throws made, default: 5, min: 0 }}
  - {{ id: fta, label: Free throw attempts, default: 6, min: 0 }}
  - {{ id: pts, label: Points, min: 0, decimals: 0 }}
  - {{ id: fgp, label: Field goal %, family: percent, unit: '%', min: 0 }}
  - {{ id: efg, label: Effective FG %, family: percent, unit: '%', min: 0 }}
  - {{ id: ts, label: True shooting %, family: percent, unit: '%', min: 0 }}
equations:
  - pts = 2 * fg + tp + ft
  - fgp = fg / fga
  - efg = (fg + 0.5 * tp) / fga
  - ts = pts / (2 * (fga + 0.44 * fta))
faq:
  - q: What is effective field goal percentage?
    a: FG% adjusted for the extra value of three-pointers — (FG + 0.5 × 3PM) ÷ FGA.
  - q: What is true shooting percentage?
    a: Points per shooting possession, including free throws — PTS ÷ (2 × (FGA + 0.44 × FTA)).
  - q: What is a good TS%?
    a: Around 57–58% is roughly NBA average in recent seasons; above 62% is excellent.
related: [sports/win-percentage]
''','''
## How to use this calculator

Enter **field goals made and attempted**, **three-pointers made** and **free throws made and attempted**. Points and the three shooting percentages are calculated.

## Example

8/17 FG (3 threes), 5/6 FT:

- Points = **24**
- FG% = **47.1%**, eFG% = **55.9%**, TS% = **61.1%**
''')

page(C,'football-points',f'''
title: League Points Calculator (Football / Soccer)
description: Calculate league points, points per game and goal difference from wins, draws and losses.
category: sports
keywords: [league points calculator, football points, soccer table, points per game, goal difference, 3 points for a win]
{U}
variables:
  - {{ id: w, label: Wins, default: 18, min: 0 }}
  - {{ id: d, label: Draws, default: 8, min: 0 }}
  - {{ id: l, label: Losses, default: 6, min: 0 }}
  - {{ id: gf, label: Goals scored, default: 55, min: 0 }}
  - {{ id: ga, label: Goals conceded, default: 30, min: 0 }}
  - {{ id: pts, label: Points (3 for a win, 1 for a draw), min: 0, decimals: 0 }}
  - {{ id: ppg, label: Points per game, min: 0, decimals: 2 }}
  - {{ id: gd, label: Goal difference, decimals: 0 }}
equations:
  - pts = 3 * w + d
  - ppg = pts / (w + d + l)
  - gd = gf - ga
faq:
  - q: How are league points calculated?
    a: Most football leagues award 3 points for a win, 1 for a draw and 0 for a loss.
  - q: What is points per game?
    a: Total points divided by matches played — useful for comparing teams with games in hand.
  - q: How many points to avoid relegation in a 38-game league?
    a: Often around 35–40, but it varies by season.
related: [sports/win-percentage]
''','''
## How to use this calculator

Enter **wins**, **draws**, **losses** and **goals for and against**. Points, points per game and goal difference are calculated.

## Example

18 wins, 8 draws, 6 losses, 55–30 goals:

- Points = **62**
- Points per game = **1.94**
- Goal difference = **+25**
''')

page(C,'bowling-handicap',f'''
title: Ten-Pin Bowling Average & Handicap Calculator
description: Calculate your bowling average and league handicap from total pins, games played and the league basis.
category: sports
keywords: [bowling handicap calculator, bowling average, ten pin bowling, league handicap, handicap basis]
{U}
variables:
  - {{ id: pins, label: Total pins (scratch), default: 2610, min: 0 }}
  - {{ id: g, label: Games played, default: 15, min: 1 }}
  - {{ id: basis, label: Handicap basis, default: 220, min: 0 }}
  - {{ id: pct, label: Handicap percentage, family: percent, unit: '%', default: 90, min: 0, max: 1 }}
  - {{ id: avg, label: Average, min: 0, decimals: 0 }}
  - {{ id: hc, label: Handicap per game, min: 0, decimals: 0 }}
equations:
  - avg = floor(pins / g)
  - hc = max(0, floor((basis - avg) * pct))
faq:
  - q: How is a bowling handicap calculated?
    a: Handicap = (basis − average) × percentage, rounded down. For example (220 − 174) × 90% = 41.
  - q: Why are fractions dropped?
    a: Most leagues truncate both the average and the handicap to whole pins.
  - q: What basis and percentage are common?
    a: 200–230 basis with 80–100% are common; check your league rules.
related: [sports/win-percentage, math/average]
''','''
## How to use this calculator

Enter your **total pins**, **games played**, the league's **basis** and **percentage**. Your average and handicap are calculated.

## Example

2,610 pins in 15 games → average **174**. With a 220 basis at 90%: (220 − 174) × 0.9 = 41.4 → handicap **41**.
''')

page(C,'running-cadence',f'''
title: Running Cadence & Stride Length Calculator
description: Calculate running speed from cadence and stride length — or the stride length from your pace and cadence.
category: sports
keywords: [running cadence, stride length, steps per minute, running form, 180 cadence, step length]
{U}
variables:
  - {{ id: cad, label: Cadence, suffix: steps/min, default: 170, min: 0 }}
  - {{ id: sl, label: Step length, family: length, unit: m, imperialUnit: ft, default: 1.1, min: 0 }}
  - {{ id: v, label: Speed, family: velocity, unit: kmh, imperialUnit: mph, min: 0 }}
  - {{ id: pk, label: Pace, suffix: min/km, min: 0, decimals: 2 }}
equations:
  - v = cad * sl / 60
  - pk = 1000 / v / 60
faq:
  - q: What is a good running cadence?
    a: Many recreational runners run at 160–175 steps per minute; elite runners often exceed 180 at race pace. The ideal depends on height and speed.
  - q: Should I increase my cadence?
    a: A small increase (5–10%) can reduce overstriding and impact for some runners. Change gradually.
  - q: Is step length the same as stride length?
    a: Not exactly — a stride is two steps (left and right). Here, step length is per step.
related: [sports/pace-calculator, health/steps-to-distance]
''','''
## How to use this calculator

Enter your **cadence** and **step length** to get speed and pace. Or press × on step length and enter your pace to work out your step length.

## Formula

<p class="formula">speed = cadence × step length</p>

## Example

170 steps/min with 1.1 m steps → speed 187 m/min = **11.2 km/h**, pace **5.35 min/km** (about 5:21).
''')

page(C,'jump-height',f'''
title: Vertical Jump Height Calculator (Hang Time)
description: Calculate vertical jump height from flight (hang) time — or the hang time for a given jump height.
category: sports
keywords: [vertical jump calculator, jump height, hang time, flight time, jump test, physics of jumping]
{U}
variables:
  - {{ id: t, label: Flight (hang) time, family: seconds, unit: ms, default: 550, min: 0 }}
  - {{ id: h, label: Jump height, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: v, label: Take-off speed, family: velocity, unit: ms, min: 0 }}
equations:
  - h = g0 * t^2 / 8
  - v = g0 * t / 2
faq:
  - q: How is jump height calculated from hang time?
    a: h = g × t² ÷ 8. The body rises for half the flight time and falls for the other half.
  - q: How do I measure hang time?
    a: Use a jump mat, force plate or slow-motion video — count the time from take-off to landing.
  - q: What is a good vertical jump?
    a: Around 40–50 cm is typical for active adult men and 30–40 cm for women; elite basketball players can exceed 75 cm.
related: [physics/free-fall, sports/one-rep-max]
''',f'''
## How to use this calculator

Enter your **flight time** (in milliseconds or seconds). Jump height and take-off speed are calculated.

## Formula

<p class="formula">h = g t² ÷ 8</p>

## Example

A hang time of 550 ms: h = 9.81 × 0.55² ÷ 8 = **{9.80665*0.55**2/8*100:.1f} cm**.

Bending the knees on landing makes flight time look longer and overstates height — land with straight legs for accurate tests.
''')

page(C,'net-run-rate',f'''
title: Net Run Rate (NRR) Calculator
description: Calculate a cricket team's net run rate for tournament standings from runs scored and conceded.
category: sports
keywords: [net run rate, nrr calculator, cricket nrr, ipl nrr, world cup net run rate, tournament standings]
{U}
variables:
  - {{ id: rf, label: Total runs scored, default: 1650, min: 0 }}
  - {{ id: bf, label: Total balls faced, default: 1140, min: 1 }}
  - {{ id: ra, label: Total runs conceded, default: 1580, min: 0 }}
  - {{ id: bb, label: Total balls bowled, default: 1200, min: 1 }}
  - {{ id: nrr, label: Net run rate, decimals: 3 }}
equations:
  - nrr = rf / (bf / 6) - ra / (bb / 6)
faq:
  - q: How is net run rate calculated?
    a: NRR = (runs scored ÷ overs faced) − (runs conceded ÷ overs bowled), using totals across all matches.
  - q: What if a team is bowled out?
    a: The full quota of overs (e.g. 20 in a T20) counts as overs faced, even if the innings ended early.
  - q: Why is NRR important?
    a: It separates teams level on points in tournament tables.
related: [sports/cricket-run-rate, sports/required-run-rate]
''','''
## How to use this calculator

Enter the **total runs scored** and **balls faced**, and the **total runs conceded** and **balls bowled**, across all matches. NRR is calculated.

## Formula

<p class="formula">NRR = runs scored ÷ overs faced − runs conceded ÷ overs bowled</p>

## Example

1,650 runs from 190 overs; 1,580 conceded in 200 overs:

NRR = 8.684 − 7.900 = **+0.784**
''')
print('sports ok')
