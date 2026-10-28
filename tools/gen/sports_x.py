import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
g0 = 9.80665
def mmss(minutes):
    s = round(minutes * 60); return f"{s//60}:{s%60:02d}"
def hms(minutes):
    s = round(minutes * 60); return f"{s//3600}:{s%3600//60:02d}:{s%60:02d}"

expand('sports/baseball-batting', '''
## What's a good average and OBP?

| Rating | Batting average | On-base percentage |
|---|---|---|
| Excellent | .300+ | .390+ |
| Above average | .270–.299 | .340–.389 |
| Average | .250–.269 | .310–.339 |
| Below average | .230–.249 | .290–.309 |
| Poor | below .230 | below .290 |

Ranges are rough guides for modern Major League Baseball; league averages change from season to season.

## Slugging and OPS

Slugging percentage (SLG) weights extra-base hits:

<p class="formula">SLG = (1B + 2 × 2B + 3 × 3B + 4 × HR) ÷ AB</p>

**OPS** = OBP + SLG. An OPS of .800 is good; .900 or more is excellent.

## What counts as an at-bat

At-bats exclude walks, hit-by-pitch, sacrifice bunts, sacrifice flies and catcher's interference. That is why on-base percentage uses a different denominator from batting average.

## Example season

500 AB, 150 H, 60 BB, 5 HBP, 5 SF:

- AVG = 150 ÷ 500 = **.300**
- OBP = 215 ÷ 570 = **.377**
''', [
 ('What is a .300 hitter?', 'A batter who gets a hit in 30% of at-bats — traditionally the mark of an excellent hitter.'),
 ('Why is OBP higher than batting average?', 'OBP also counts walks and hit-by-pitches, which batting average ignores.'),
])

expand('sports/baseball-era', '''
## ERA and WHIP benchmarks

| Rating | ERA | WHIP |
|---|---|---|
| Excellent | under 3.00 | under 1.10 |
| Above average | 3.00–3.75 | 1.10–1.25 |
| Average | 3.75–4.50 | 1.25–1.35 |
| Below average | 4.50–5.25 | 1.35–1.45 |
| Poor | over 5.25 | over 1.45 |

Rough guides for modern MLB; league scoring levels vary by year.

## Innings notation

Innings are recorded in thirds: “6.1” means 6⅓ innings and “6.2” means 6⅔. Convert to decimals before calculating — 6.1 becomes 6.333 and 6.2 becomes 6.667.

## Earned vs unearned runs

Runs that score because of fielding errors or passed balls are **unearned** and do not count towards ERA. Only earned runs reflect the pitcher's performance.

## Shorter games

For leagues with 7-inning games, ERA is sometimes scaled to 7 innings: ERA = 7 × ER ÷ IP. State which version you use.

## FIP

Fielding Independent Pitching focuses on strikeouts, walks, hit batters and home runs, which the pitcher controls most directly. It is scaled to look like ERA and often predicts future ERA better.
''', [
 ('What is a good ERA?', 'Under about 3.50 is very good in modern professional baseball; under 3.00 is excellent.'),
 ('How do I enter 6⅔ innings?', 'Enter 6.667, not 6.2.'),
])

expand('sports/bowling-economy', '''
## Benchmarks by format

| Format | Good economy | Good average | Good strike rate |
|---|---|---|---|
| Test cricket | under 3.0 | under 30 | under 60 |
| ODI | under 5.0 | under 30 | under 35 |
| T20 | under 7.5 | under 25 | under 20 |

Rough guides; conditions and eras vary.

## Which stat matters most?

- **Economy rate** matters most in limited-overs cricket, where stopping runs wins games.
- **Strike rate** shows how often a bowler takes wickets, key in Test cricket.
- **Average** combines both: runs per wicket.

## Converting overs notation

Overs are written as completed overs plus balls: 8.3 means 8 overs and 3 balls (51 balls), not 8.3 overs. Enter balls bowled for exact results.

## Example

480 runs, 20 wickets, 432 balls (72 overs):

- Economy = 480 ÷ 72 = **6.67**
- Average = 480 ÷ 20 = **24.00**
- Strike rate = 432 ÷ 20 = **21.6**
''', [
 ('What is bowling economy rate?', 'Runs conceded per over (6 balls).'),
 ('What is a bowling strike rate?', 'Balls bowled per wicket taken — lower is better.'),
])

expand('sports/bowling-handicap', '''
## Handicap table (basis 220, 90%)

| Average | Handicap |
|---|---|
''' + ''.join(f"| {a} | {max(0, math.floor((220-a)*0.9))} |\n" for a in [120, 140, 150, 160, 170, 180, 190, 200, 210, 220]) + '''
## Common handicap systems

| Basis | Percentage | Typical use |
|---|---|---|
| 200 | 90% | Casual leagues |
| 210 | 90% | Mixed leagues |
| 220 | 90% | Common standard |
| 230 | 80% or 100% | Competitive leagues |

Check your league rules — some use 100% of the difference.

## Establishing an average

Most leagues need at least 3 games (often 9–21) to set a reliable average. Until then, a temporary or previous-season average may be used.

## Why use handicaps?

Handicaps let bowlers of different skill levels compete fairly. A 150-average bowler gets enough extra pins to have a real chance against a 200-average bowler.
''', [
 ('How is bowling handicap calculated?', 'Handicap = (basis − average) × percentage, rounded down. With 220 basis and 90%, a 174 average gets 41 pins.'),
 ('Is handicap added to every game?', 'Yes, it is added to your scratch score each game.'),
])

expand('sports/cricket-batting', '''
## Batting benchmarks

| Format | Good average | Good strike rate |
|---|---|---|
| Test | 40+ (50+ is elite) | 50–60 |
| ODI | 35+ (45+ is elite) | 85–100 |
| T20 | 25–30+ | 130–150+ |

Strike rate matters more in shorter formats; average matters more in Tests.

## Not-outs and average

Batting average divides by **dismissals**, not innings. A batter with many not-outs can have an average higher than their typical score. 1,240 runs in 35 innings with 7 not-outs = 1,240 ÷ 28 = **44.29**.

## Balls faced

Strike rate counts legal deliveries faced. Wides do not count as balls faced; no-balls do.

## Other useful batting stats

| Stat | Meaning |
|---|---|
| Boundary % | Share of runs from fours and sixes |
| Dot ball % | Share of balls with no run |
| Conversion rate | 50s turned into 100s |
| Highest score | Best single innings |
''', [
 ('How is batting average calculated in cricket?', 'Runs scored ÷ number of times dismissed.'),
 ('What is a good strike rate in T20?', 'Around 130–150 or higher for top-order batters.'),
])

expand('sports/cricket-run-rate', '''
## Overs and balls

| Overs notation | Balls | Decimal overs |
|---|---|---|
''' + ''.join(f"| {o}.{b} | {o*6+b} | {o+b/6:.3f} |\n" for o, b in [(5, 0), (5, 1), (5, 3), (10, 4), (19, 5), (49, 2)]) + '''
Never use “10.4 overs” as 10.4 in calculations — it means 10 overs and 4 balls, which is 10.667 overs.

## Projected score

<p class="formula">Projected total = current runs + run rate × overs remaining</p>

At 85 for 2 after 10 overs in a T20 (run rate 8.5), the projected total is 85 + 8.5 × 10 = **170**.

## Typical run rates

| Format | Typical scoring rate |
|---|---|
| Test | 3–3.5 runs per over |
| ODI | 5.5–6.5 runs per over |
| T20 | 8–9 runs per over |

## Required run rate

When chasing, compare the current run rate with the required rate — see the [required run rate calculator](/sports/required-run-rate/).
''', [
 ('What is the run rate for 168 in 20 overs?', '8.40 runs per over.'),
 ('How do I convert 15.3 overs to decimal?', '15 + 3/6 = 15.5 overs.'),
], before='## Overs notation')

expand('sports/cycling-gear-speed', '''
## Speed at 90 rpm (700×25c wheel, 2.1 m circumference)

| Chainring / cog | Ratio | Speed |
|---|---|---|
''' + ''.join(f"| {c}/{s} | {c/s:.2f} | {c/s*2.105*90*60/1000:.1f} km/h |\n" for c, s in [(34, 28), (34, 17), (50, 25), (50, 17), (50, 13), (53, 11)]) + '''
## Wheel circumferences

| Tyre | Circumference (approx.) |
|---|---|
| 700×23c | 2.096 m |
| 700×25c | 2.105 m |
| 700×28c | 2.136 m |
| 29″ × 2.2 MTB | 2.30 m |
| 26″ × 2.0 MTB | 2.07 m |

For accuracy, roll the bike one full wheel turn and measure.

## Gear inches

An older measure still used in the US: gear inches = ratio × wheel diameter (inches). A 50/17 on a 27-inch wheel is about 79 gear inches.

## Cadence

Most recreational riders pedal at 70–90 rpm; trained cyclists often prefer 85–100 rpm. Shifting to keep cadence steady is more efficient than grinding a big gear.
''', [
 ('How fast is 50/15 at 90 rpm?', 'About 37.9 km/h on a 700×25c wheel.'),
 ('What is a good cycling cadence?', '80–95 rpm for most road riding.'),
])

expand('sports/effective-field-goal', '''
## Why eFG% and TS% matter

Plain field-goal percentage treats a three-pointer like a two. Effective FG% adds 50% extra credit for threes, and true shooting % also includes free throws, giving the best single measure of scoring efficiency.

## Benchmarks (NBA, approximate)

| Rating | FG% | eFG% | TS% |
|---|---|---|---|
| Excellent | 50%+ | 57%+ | 62%+ |
| Above average | 47–50% | 54–57% | 58–62% |
| League average (recent seasons) | about 47% | about 54% | about 58% |
| Below average | under 44% | under 50% | under 54% |

Averages shift as teams take more threes.

## The 0.44 factor

TS% uses 0.44 × free-throw attempts to estimate the number of possessions used by free throws, since and-ones and technical fouls do not use a full possession.

## Example

8 FG on 17 attempts, 3 threes, 5 of 6 free throws:

- Points = 2 × 8 + 3 + 5 = **24**
- FG% = 8 ÷ 17 = 47.1%
- eFG% = (8 + 1.5) ÷ 17 = **55.9%**
- TS% = 24 ÷ (2 × (17 + 2.64)) = **61.1%**
''', [
 ('What is the difference between eFG% and TS%?', 'eFG% adjusts for three-pointers; TS% also includes free throws.'),
 ('What is a good true shooting percentage?', 'Above about 60% is very good in the NBA.'),
])

expand('sports/football-points', '''
## Points per game benchmarks

| PPG | Typical outcome (38-game league) |
|---|---|
| 2.3+ | Title contenders (87+ points) |
| 1.8–2.2 | Top-four / European places |
| 1.3–1.7 | Mid-table |
| 1.0–1.2 | Relegation fight |
| under 1.0 | Likely relegation |

About 40 points is often quoted as the target for Premier League safety, though fewer is usually enough.

## Tie-breakers

When teams are level on points, leagues use tie-breakers in a set order. Common ones:

1. Goal difference
2. Goals scored
3. Head-to-head results
4. Away goals or fair play

The order varies by competition — check the rules.

## Maximum possible points

To see if a team can still be caught: maximum points = current points + 3 × games remaining.

## Historical systems

Before the 1980s–90s, many leagues gave 2 points for a win. The switch to 3 points was meant to reward attacking play.
''', [
 ('How are football league points calculated?', '3 points for a win, 1 for a draw, 0 for a loss.'),
 ('What is goal difference?', 'Goals scored minus goals conceded.'),
])

expand('sports/golf-handicap', '''
## How the World Handicap System works

1. Calculate a **score differential** for each round (this calculator).
2. Your **Handicap Index** is the average of the best 8 differentials from your most recent 20 rounds.
3. Your **Course Handicap** for a given course and tee is:

<p class="formula">Course Handicap = Handicap Index × (Slope ÷ 113) + (Course Rating − Par)</p>

With a Handicap Index of 15.0 on a course with slope 128, rating 71.2 and par 72: 15 × 128 ÷ 113 + (71.2 − 72) = **16.2**, rounded to 16.

## Adjusted gross score

Before calculating, cap each hole at **net double bogey**: par + 2 + any handicap strokes you receive on that hole. This stops one disaster hole from distorting your handicap.

## Fewer than 20 rounds

| Rounds | Differentials used |
|---|---|
| 3 | Lowest 1, minus 2.0 |
| 5 | Lowest 1 |
| 6 | Average of lowest 2, minus 1.0 |
| 8 | Average of lowest 2 |
| 10 | Average of lowest 3 |
| 15 | Average of lowest 5 |
| 20 | Average of lowest 8 |

## Slope rating

Slope rating measures how much harder a course is for a bogey golfer than for a scratch golfer. 113 is the standard; courses range from 55 to 155.
''', [
 ('What is a good golf handicap?', 'The average handicap index for men is around 14–16. Single figures (under 10) is good; under 5 is excellent.'),
 ('How many rounds do I need for a handicap?', 'Under the World Handicap System, 54 holes (three 18-hole rounds) are enough to get an initial index.'),
])

expand('sports/jump-height', '''
## Hang time vs height

| Hang time | Jump height |
|---|---|
''' + ''.join(f"| {t} ms | {g0*(t/1000)**2/8*100:.1f} cm ({g0*(t/1000)**2/8/0.0254:.1f} in) |\n" for t in [400, 450, 500, 550, 600, 650, 700, 800, 900]) + '''
## Vertical jump benchmarks

| Group | Typical countermovement jump |
|---|---|
| Untrained adult | 30–45 cm |
| Recreational athlete | 40–55 cm |
| Trained athlete (team sports) | 55–70 cm |
| Elite basketball / volleyball | 70–90+ cm |

## Measuring hang time

Phone apps can measure flight time from slow-motion video: count frames from take-off to landing and divide by the frame rate. At 240 fps, 132 frames = 550 ms.

## Errors to avoid

The formula assumes you land in the same body position you took off from. Tucking the legs or landing with bent knees lengthens the flight time and overestimates height.

## Power from jump height

The Sayers equation estimates peak power: P (W) = 60.7 × jump height (cm) + 45.3 × body mass (kg) − 2,055.
''', [
 ('How high is a 600 ms jump?', 'About 44 cm (17.4 inches).'),
 ('How do I measure jump height without equipment?', 'Film the jump in slow motion, measure the flight time and enter it here.'),
])

expand('sports/net-run-rate', '''
## Rules for overs in NRR

- If a team is **bowled out**, its innings counts as the full quota of overs (for example 20 or 50), not the overs actually faced.
- In rain-affected matches, the revised overs under the DLS method are used.
- Overs must be converted to balls or decimal overs correctly (10.3 overs = 63 balls).

## Example over a tournament

| Match | Runs for / overs | Runs against / overs |
|---|---|---|
| 1 | 180 / 20 | 160 / 20 |
| 2 | 145 / 18.2 (won chasing) | 142 / 20 |
| 3 | 130 / 20 (all out) | 131 / 17.4 |
| **Total** | 455 / 58.333 | 433 / 57.667 |

NRR = 455 ÷ 58.333 − 433 ÷ 57.667 = 7.800 − 7.509 = **+0.291**

## Why NRR changes so much

Winning big chases quickly or bowling teams out cheaply moves NRR sharply. Late in a tournament, teams often aim to win by a specific margin to overtake a rival's NRR.

## NRR vs run rate

Run rate is a single team's scoring speed. NRR compares a team's scoring rate with the rate it concedes across all matches.
''', [
 ('What does a positive NRR mean?', 'The team scores faster than its opponents on average across the tournament.'),
 ('Is a bowled-out innings counted as full overs?', 'Yes. If a team is all out, its innings counts as the full allocation of overs for NRR.'),
])

expand('sports/one-rep-max', '''
## Rep max chart (Epley, 1RM = 100 kg)

| Reps | Weight | % of 1RM |
|---|---|---|
''' + ''.join(f"| {r} | {100/(1+r/30):.1f} kg | {100/(1+r/30):.0f}% |\n" for r in [1, 2, 3, 4, 5, 6, 8, 10, 12, 15]) + '''
## Other 1RM formulas

| Formula | Equation |
|---|---|
| Epley (this calculator) | w × (1 + r ÷ 30) |
| Brzycki | w × 36 ÷ (37 − r) |
| Lombardi | w × r<sup>0.1</sup> |

For 100 kg × 6 reps: Epley 120 kg, Brzycki 116 kg, Lombardi 120 kg. They agree best at 2–6 reps.

## Accuracy

1RM estimates are most accurate from sets of **2–6 reps** taken close to failure. Above 10 reps, estimates become less reliable because endurance plays a larger role.

## Training zones

| Goal | % of 1RM | Reps |
|---|---|---|
| Strength | 85–100% | 1–5 |
| Hypertrophy (muscle size) | 65–85% | 6–12 |
| Muscular endurance | under 65% | 15+ |

## Safety

Testing a true 1RM carries injury risk. Use a spotter or safety bars, warm up properly, and consider estimating from a heavy set of 3–5 instead.
''', [
 ('How do I estimate my 1RM?', 'Lift a weight for as many good reps as possible (ideally 2–6), then enter the weight and reps. The calculator uses the Epley formula.'),
 ('What percentage of 1RM is 10 reps?', 'About 75% using the Epley formula.'),
], before='## Training percentages')

expand('sports/pace-calculator', '''
## Finish times by pace

| Pace (min/km) | 5K | 10K | Half marathon | Marathon |
|---|---|---|---|---|
''' + ''.join(f"| {mmss(p)} | {hms(p*5)} | {hms(p*10)} | {hms(p*21.0975)} | {hms(p*42.195)} |\n" for p in [4, 4.5, 5, 5.5, 6, 6.5, 7, 8]) + '''
## Pacing strategies

- **Even pacing**: run the same pace throughout — usually best for most runners.
- **Negative split**: run the second half slightly faster than the first. Many world records are set this way.
- Avoid starting too fast; the first kilometre in a race often feels easy because of adrenaline.

## Training paces

| Run type | Relative to 5K race pace |
|---|---|
| Easy / recovery | 60–90 s per km slower |
| Long run | 45–75 s per km slower |
| Tempo (threshold) | 15–25 s per km slower |
| Intervals | about 5K pace or slightly faster |

## Course and weather

Hills, heat, humidity and wind all slow you down. In hot weather, expect to run several seconds per km slower than in cool conditions.
''', [
 ('What pace do I need for a sub-2-hour half marathon?', 'About 5:41 per km (9:09 per mile).'),
 ('What pace is a 4-hour marathon?', 'About 5:41 per km (9:09 per mile).'),
], before='## Popular goal paces')

expand('sports/pace-speed-converter', '''
## Running and walking paces

| Activity | Typical pace | Speed |
|---|---|---|
| Casual walk | 12–15 min/km | 4–5 km/h |
| Brisk walk | 9–10 min/km | 6–6.5 km/h |
| Easy jog | 7–8 min/km | 7.5–8.5 km/h |
| Recreational run | 5:30–6:30 min/km | 9–11 km/h |
| Competitive club runner | 4–5 min/km | 12–15 km/h |
| Elite marathon pace | about 2:55 min/km | about 20.5 km/h |

## Treadmills

Treadmills display speed (km/h or mph), while running plans usually use pace. Convert with:

<p class="formula">Pace (min/km) = 60 ÷ speed (km/h)</p>

Setting the treadmill incline to 1% roughly matches the effort of running outdoors on flat ground.

## Pace per km to pace per mile

Multiply min/km by 1.609. 5:00 per km is 8:03 per mile.

## Decimal minutes

The calculator uses decimal minutes: 5.5 min/km means 5:30 per km, not 5:50.
''', [
 ('What is 10 km/h in pace?', '6:00 per km, or 9:39 per mile.'),
 ('What pace is 6 mph?', '10:00 per mile, or about 6:13 per km.'),
], before='## Quick table')

expand('sports/race-time-predictor', '''
## Equivalent race times (Riegel, exponent 1.06)

| 5K time | 10K | Half marathon | Marathon |
|---|---|---|---|
''' + ''.join(f"| {hms(t)} | {hms(t*2**1.06)} | {hms(t*(21.0975/5)**1.06)} | {hms(t*(42.195/5)**1.06)} |\n" for t in [18, 20, 22, 25, 28, 30, 35]) + '''
## Limits of the prediction

- Predictions assume you have **trained for the longer distance**. Without enough long runs, marathon predictions from a 5K are usually too optimistic.
- Use the closest race you have run: a half marathon predicts a marathon better than a 5K does.
- Course, weather and pacing affect results.

## The fatigue exponent

Riegel's 1.06 suits most trained runners. Some coaches use 1.07–1.08 for marathon predictions for less experienced runners, which gives slower, often more realistic times.

## Using predictions for training

Predicted times give target paces for longer races and help set training zones. Re-test with a short race every few months to track progress.
''', [
 ('What marathon time does a 25-minute 5K predict?', 'Just under 4 hours (about 3:59:46), assuming marathon-specific training.'),
 ('How accurate are race predictors?', 'Usually within a few percent for well-trained runners at similar distances; less accurate for big jumps in distance.'),
])

expand('sports/required-run-rate', '''
## Required rate table

| Runs needed | 6 overs left | 10 overs left | 15 overs left | 20 overs left |
|---|---|---|---|---|
''' + ''.join(f"| {r} | {r/6:.2f} | {r/10:.2f} | {r/15:.2f} | {r/20:.2f} |\n" for r in [40, 60, 80, 100, 120, 150]) + '''
## Chasing in T20

A required rate above about 12 an over is very hard to sustain for long, though modern T20 batting has made rates of 10–12 more achievable, especially with wickets in hand.

## Wickets in hand matter

Run rate alone ignores wickets. 60 off 30 balls with 8 wickets left is a very different chase from 60 off 30 with 2 wickets left. Win-probability models combine both.

## Rain and DLS

In rain-affected matches, the Duckworth–Lewis–Stern method sets a revised target based on resources (overs and wickets) remaining. The required run rate is then calculated against the revised target.

## Example

Target 181, score 92 after 11 overs (54 balls left): 89 runs needed at **9.89 per over**, or 1.65 runs per ball.
''', [
 ('How is required run rate calculated?', 'Runs needed ÷ overs remaining. 89 needed off 9 overs is 9.89 per over.'),
 ('What is the difference between current and required run rate?', 'Current run rate is how fast a team has scored so far; required run rate is how fast it must score from now on to win.'),
])

expand('sports/running-cadence', '''
## Cadence and speed

At a step length of 1.1 m:

| Cadence | Speed | Pace |
|---|---|---|
''' + ''.join(f"| {c} spm | {c*1.1*60/1000:.1f} km/h | {mmss(1000/(c*1.1))} /km |\n" for c in [150, 160, 170, 180, 190]) + '''
## The 180 steps per minute myth

180 spm is often quoted as ideal, based on observations of elite runners at race pace. In reality, cadence rises with speed and varies with height and leg length. Most recreational runners run at 155–175 spm at easy paces.

## Should you increase cadence?

Raising cadence by about **5–10%** can reduce overstriding and impact loading at the knee and hip, which some studies link to fewer injuries. Larger jumps feel unnatural and waste energy.

## How to increase cadence

- Use a metronome app set 5% above your current cadence.
- Focus on quick, light steps landing under your body.
- Practise on short runs first, then extend.

## Measuring cadence

Count steps for 30 seconds and double it, or count one foot for 60 seconds and double that. Many watches measure cadence automatically.
''', [
 ('What is a good running cadence?', 'Typically 160–180 steps per minute, depending on speed and height.'),
 ('Does a higher cadence make you faster?', 'Speed = cadence × step length, so either can increase speed. Raising cadence slightly often helps form more than speed.'),
])

expand('sports/swim-pace', '''
## Swim pace benchmarks (per 100 m, freestyle)

| Level | Pace per 100 m |
|---|---|
| Beginner | 2:30–3:00+ |
| Recreational | 2:00–2:30 |
| Fitness / triathlete | 1:40–2:00 |
| Competitive masters | 1:20–1:40 |
| Elite | under 1:10 |

## Finish times by pace

| Pace /100 m | 400 m | 750 m | 1,500 m | 3,800 m |
|---|---|---|---|---|
''' + ''.join(f"| {mmss(p)} | {mmss(p*4)} | {mmss(p*7.5)} | {hms(p*15)} | {hms(p*38)} |\n" for p in [1.5, 1.75, 2.0, 2.25, 2.5]) + '''
750 m, 1,500 m and 3,800 m are the sprint, Olympic and full-distance triathlon swim lengths.

## Critical swim speed (CSS)

CSS estimates your threshold pace from a 400 m and a 200 m time trial:

<p class="formula">CSS (per 100 m) = (T400 − T200) ÷ 2</p>

If you swim 400 m in 7:20 and 200 m in 3:30, CSS = 230 s ÷ 2 = **1:55 per 100 m**.

## Open water

Expect to swim slower in open water than in a pool because there are no walls to push off and sighting interrupts your stroke. A wetsuit can make you faster through added buoyancy.
''', [
 ('What is a good 100 m swim time?', 'Around 2:00 is good for recreational swimmers; under 1:30 is strong for adults.'),
 ('How do I convert yards to metres pace?', 'Multiply pace per 100 yards by 1.094 to get pace per 100 metres.'),
])

expand('sports/win-percentage', '''
## Win percentage benchmarks

| Win % | Typical result (82-game NBA season) |
|---|---|
| 70%+ | Title contender (57+ wins) |
| 60% | Strong playoff team (49 wins) |
| 50% | Average (41 wins) |
| 40% | Missing the playoffs (33 wins) |

## How ties are counted

Different leagues treat ties differently:

- **Half a win** (this calculator): common in the NFL and many school sports.
- **Ignored**: some sports calculate win % from wins and losses only.
- **Points systems**: football (soccer) uses league points instead — see the [football points calculator](/sports/football-points/).

## Games behind

In standings, “games behind” compares two teams:

<p class="formula">GB = ((leader wins − team wins) + (team losses − leader losses)) ÷ 2</p>

## Pythagorean expectation

In baseball and other sports, expected win % can be estimated from points scored (S) and allowed (A): S² ÷ (S² + A²). Teams winning more than expected may have been lucky in close games.
''', [
 ('How do I calculate win percentage?', 'Wins ÷ total games × 100. With ties counted as half, (wins + ties ÷ 2) ÷ games.'),
 ('What is a .500 record?', 'Winning exactly half your games.'),
])

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/sports/*.mdx')):
    c = 'sports/' + os.path.basename(p)[:-4]; print(c, words(c))
