"""Improve pass (2026-11-23) for thin pages from the first batch (2026-10-27):
sports/bowling-handicap, sports/pace-speed-converter and sports/effective-field-goal.
(math/weighted-average was also queued but is a featured page, which inplace.edit refuses to touch.)
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples built from the calculator defaults, reference tables computed here,
practical notes, common mistakes, dash-free rewrites of edited text.
Slug, category, variables, equations, related and published are unchanged (asserted by inplace.edit).
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-23'


def mmss(m):
    s = round(m * 60)
    return f"{s // 60}:{s % 60:02d}"


# ---------------------------------------------------------------- Bowling handicap
pins, g, basis, pct = 2610, 15, 220, 0.90


def avg_of(p, n):
    return math.floor(p / n)


def hc_of(a, b=basis, q=pct):
    return max(0, math.floor((b - a) * q))


avg = avg_of(pins, g)
hc = hc_of(avg)
assert avg == 174 and hc == 41
raw = (basis - avg) * pct
# truncation: 14 more pins still leaves the average at 174
avg_trunc = (pins + 14) / g
assert avg_of(pins + 14, g) == 174
# match example: opponent averages 205
opp = 205
hc_opp = hc_of(opp)
a_s, b_s = 180, 198
a_t, b_t = a_s + hc, b_s + hc_opp
# above the basis
hc_high = hc_of(228)
assert hc_high == 0
# table of systems for the default 174 average
sys_rows = ''
for b in (200, 210, 220, 230):
    cells = ' | '.join(str(hc_of(avg, b, q)) for q in (0.8, 0.9, 1.0))
    sys_rows += f"| {b} | {cells} |\n"
# three game series handicap
series_hc = 3 * hc
assert all(hc_of(a) == v for a, v in ((120, 90), (150, 63), (200, 18), (210, 9), (220, 0)))

edit('sports/bowling-handicap', date=U, phrase='bowling handicap calculator',
     title='Bowling Handicap Calculator: Average and League Handicap',
     description='Bowling handicap calculator: enter total pins, games, league basis and percentage to get your ten pin average and handicap per game, with a worked example.',
     intro=("A bowling handicap is a pin allowance added to each scratch game so bowlers of different ability can compete on equal terms. "
            "This bowling handicap calculator works out your league average from total pins and games, then your handicap from the basis and percentage.\n\n"
            "League bowlers, secretaries and tournament organisers use it to check standing sheets, set handicaps for new bowlers and see how a rising average changes the pins they receive."),
     replace=[('''## How to use the ten-pin bowling average & handicap calculator

Enter your **total pins**, **games played**, the league's **basis** and **percentage**. Your average and handicap are calculated.''',
               '''## How to use the bowling handicap calculator

Enter your **total pins** (scratch, without handicap), **games played**, the league's **basis** score and the handicap **percentage**. The calculator truncates the average to a whole pin, then takes the chosen percentage of the gap between the basis and the average, dropping any fraction. A bowler at or above the basis gets a handicap of 0.'''),
              ('''## Example

2,610 pins in 15 games → average **174**. With a 220 basis at 90%: (220 − 174) × 0.9 = 41.4 → handicap **41**.''',
               f'''## Worked example

A bowler has knocked down {pins:,} pins in {g} league games, in a league that uses a {basis} basis at {pct*100:.0f}%:

- Average = {pins:,} ÷ {g} = **{avg}** (any fraction would be dropped)
- Gap to basis = {basis} - {avg} = {basis - avg}
- Handicap = {basis - avg} × {pct:.2f} = {raw:.1f}, truncated to **{hc} pins per game**

Over a three game series that is {series_hc} extra pins. If the same bowler had {pins + 14:,} pins, the average would be {avg_trunc:.2f}, which still truncates to {avg}, so the handicap stays at {hc}.

### A handicap match

Our {avg} average bowler meets a {opp} average bowler, who gets ({basis} - {opp}) × {pct:.2f} = {(basis-opp)*pct:.1f}, so **{hc_opp} pins**. If the scratch games are {a_s} and {b_s}, the handicap totals are {a_s} + {hc} = **{a_t}** and {b_s} + {hc_opp} = **{b_t}**, so the lower average bowler wins the game by {abs(a_t - b_t)} pins after losing it by {b_s - a_s} on scratch.'''),
              ('''## Common handicap systems

| Basis | Percentage | Typical use |
|---|---|---|
| 200 | 90% | Casual leagues |
| 210 | 90% | Mixed leagues |
| 220 | 90% | Common standard |
| 230 | 80% or 100% | Competitive leagues |

Check your league rules \u2014 some use 100% of the difference.''',
               f'''## Common handicap systems

| Basis | Percentage | Typical use |
|---|---|---|
| 200 | 90% | Casual leagues |
| 210 | 90% | Mixed leagues |
| 220 | 90% | Common standard |
| 230 | 80% or 100% | Competitive leagues |

Check your league rules, because some use 100% of the difference. The same {avg} average gets a very different handicap under each system:

| Basis | 80% | 90% | 100% |
|---|---|---|---|
{sys_rows}'''),
              ('''## Establishing an average

Most leagues need at least 3 games (often 9\u201321) to set a reliable average. Until then, a temporary or previous-season average may be used.''',
               '''## Establishing an average

Leagues set a minimum number of games before an average counts, often 9, 12 or 21, and some accept 3 games at the start of a season. Until then a bowler may use last season's book average, an average from another sanctioned league, or the league's entering average for new bowlers. Many leagues recalculate handicaps every week, so check whether your sheet uses this week's average or the one carried from the previous week.''')],
     body_add=f'''
## Practical notes

- **Use scratch pins only.** Total pins must be your actual pin count without handicap, otherwise the average is inflated and the next handicap shrinks.
- **Bowlers above the basis.** A {228} average bowler in a {basis} league gets a handicap of {hc_high}; the calculator never returns a negative handicap, and most leagues do not take pins away.
- **Absent bowlers.** Leagues usually score an absent bowler as their average minus 10 pins (or a set blind score) plus handicap; that score does not go into the average.
- **Team handicap.** Team handicap is normally worked out from the sum of the members' averages against a team basis, rather than by adding individual handicaps, so the totals can differ by a pin or two.

## Common mistakes

- **Rounding instead of truncating.** A 41.6 handicap is 41, not 42, and a 174.9 average is 174.
- **Dividing by the wrong number of games.** Count only games actually bowled; vacancy, absent and blind scores are left out.
- **Entering the percentage as a whole number on paper.** 90% means multiplying by 0.90, so (220 - 174) × 90 is wrong by a factor of 100.
- **Mixing league rules.** A {avg} average gets {hc_of(avg, 200, 0.8)} pins at 200 and 80% but {hc_of(avg, 230, 1.0)} pins at 230 and 100%, so always copy the basis and percentage from the league rules.
- **Using a tournament average in a league.** Tournaments often require your highest recent book average, which can be higher than your current league average.
''',
     faq_replace=[('How is a bowling handicap calculated?', 'How is a bowling handicap calculated?',
                   f'Subtract your average from the league basis, multiply by the handicap percentage and drop the fraction. For example ({basis} - {avg}) × 90% = {raw:.1f}, so the handicap is {hc}.'),
                  ('What basis and percentage are common?', 'What basis and percentage are common?',
                   'A basis between 200 and 230 with a percentage between 80% and 100% is most common, and 220 at 90% is a popular standard. Always check your own league rules.')],
     faq_add=[('Do I get a handicap if my average is above the basis?',
               f'No. If your average is at or above the basis the handicap is 0. A {228} average in a {basis} basis league gets no pins, and most leagues never use negative handicaps.')])

# ---------------------------------------------------------------- Pace to speed
MI = 1.609344
pk = 6.0
kmh = 60 / pk
pm = pk * MI
mph = 60 / pm
assert abs(kmh - 10) < 1e-9 and mmss(pm) == '9:39' and abs(mph - 6.2137) < 1e-4
# 10 km and half marathon at the default pace
t10 = pk * 10
thm = pk * 21.0975
# decimal minute trap: 5.3 typed for 5:30
right = 60 / 5.5
wrong = 60 / 5.3


def pk_row(p):
    return f"| {mmss(p)} | {60/p:.1f} | {mmss(p*MI)} | {60/(p*MI):.1f} |\n"


quick_rows = ''.join(pk_row(p) for p in (4, 4.5, 5, 5.5, 6, 6.5, 7, 8))
assert mmss(5 * MI) == '8:03' and abs(60 / (5 * MI) - 7.456) < 1e-3
assert mmss(10 / MI) == '6:13'
# treadmill mph settings
mph_rows = ''
for s in (4.0, 5.0, 6.0, 6.5, 7.0, 7.5, 8.0, 9.0, 10.0):
    p_mi = 60 / s
    p_km = p_mi / MI
    mph_rows += f"| {s:.1f} | {s*MI:.1f} | {mmss(p_mi)} | {mmss(p_km)} | {mmss(p_km*5)} |\n"
# activity table, computed
act = (('Casual walk', 15, 12), ('Brisk walk', 10, 9), ('Easy jog', 8, 7),
       ('Recreational run', 6.5, 5.5), ('Competitive club runner', 5, 4))
act_rows = ''.join(f"| {n} | {mmss(a)} to {mmss(b)} min/km | {60/a:.1f} to {60/b:.1f} km/h |\n" for n, a, b in act)
elite = 2 + 55 / 60
act_rows += f"| Elite marathon pace | about {mmss(elite)} min/km | about {60/elite:.1f} km/h |\n"

edit('sports/pace-speed-converter', date=U, phrase='pace to speed calculator',
     title='Pace to Speed Converter: min/km, min/mile, km/h and mph',
     description='Pace to speed converter for running and treadmills: turn min/km or min/mile into km/h or mph and back, with a worked example and treadmill tables.',
     intro=("Running plans give pace in minutes per kilometre or mile, while treadmills and watches often show speed. "
            "This pace to speed calculator converts min/km, min/mile, km/h and mph in either direction, so you can type any one and read the other three.\n\n"
            "Runners, walkers, coaches and treadmill users rely on it to set a machine for a planned workout, compare metric and imperial plans, and check race pace targets."),
     replace=[('''## How to use the pace to speed converter

Type into **any** field \u2014 pace per km, pace per mile, km/h or mph. Pace is in decimal minutes (6.5 = 6:30).''',
               '''## How to use the pace to speed converter

Type into **any** field: pace per km, pace per mile, km/h or mph. The other three are worked out from it. Pace is entered in decimal minutes, so 6.5 means 6:30.'''),
              ('''## Running and walking paces

| Activity | Typical pace | Speed |
|---|---|---|
| Casual walk | 12\u201315 min/km | 4\u20135 km/h |
| Brisk walk | 9\u201310 min/km | 6\u20136.5 km/h |
| Easy jog | 7\u20138 min/km | 7.5\u20138.5 km/h |
| Recreational run | 5:30\u20136:30 min/km | 9\u201311 km/h |
| Competitive club runner | 4\u20135 min/km | 12\u201315 km/h |
| Elite marathon pace | about 2:55 min/km | about 20.5 km/h |''',
               f'''## Worked example

The default pace is {pk:g} minutes per kilometre:

- Speed = 60 ÷ {pk:g} = **{kmh:g} km/h**
- Pace per mile = {pk:g} × {MI} = {pm:.3f} minutes, which is **{mmss(pm)} per mile**
- Speed in mph = 60 ÷ {pm:.3f} = **{mph:.2f} mph**

So a treadmill set to {kmh:g} km/h, or about {mph:.1f} mph, holds a {mmss(pk)} per km pace. At that pace a 10 km run takes {t10:g} minutes and a half marathon about {int(thm//60)} hours {thm%60:.0f} minutes.

## Running and walking paces

| Activity | Typical pace | Speed |
|---|---|---|
{act_rows}'''),
              ('''## Decimal minutes

The calculator uses decimal minutes: 5.5 min/km means 5:30 per km, not 5:50.''',
               f'''## Decimal minutes

The calculator uses decimal minutes: 5.5 min/km means 5:30 per km, not 5:50. To convert, divide the seconds by 60, so 5:45 is 5.75 and 4:20 is 4.333. Typing 5.3 for a 5:30 pace gives {wrong:.2f} km/h instead of {right:.2f} km/h, which is {(wrong/right-1)*100:.1f}% too fast on the treadmill.'''),
              ('''## Quick table

| min/km | km/h | min/mile | mph |
|---|---|---|---|
| 4:00 | 15.0 | 6:26 | 9.3 |
| 5:00 | 12.0 | 8:03 | 7.5 |
| 6:00 | 10.0 | 9:39 | 6.2 |
| 7:00 | 8.6 | 11:16 | 5.3 |
| 8:00 | 7.5 | 12:52 | 4.7 |''',
               f'''## Quick table

| min/km | km/h | min/mile | mph |
|---|---|---|---|
{quick_rows}''')],
     body_add=f'''
## Treadmill settings in mph

Many treadmills in the US and UK show mph only. These are the paces for common settings, with the time for a 5 km run:

| mph | km/h | Pace per mile | Pace per km | 5 km time |
|---|---|---|---|---|
{mph_rows}
## Practical notes

- **Treadmill calibration.** Belt speed can be a few percent off the display, especially on older machines, so treat the converted pace as a guide and check effort or heart rate.
- **GPS pace outdoors.** Watch pace jumps around under trees and between buildings; average pace over a whole lap is more reliable than the instant reading.
- **Incline.** A 1% incline is often used to make treadmill running feel closer to flat outdoor running, mainly at faster paces. It does not change the speed conversion.

## Common mistakes

- **Reading decimal minutes as seconds.** 6.5 min/km is 6:30, not 6:50.
- **Inverting the conversion.** Speed is 60 divided by pace, not pace divided by 60; a smaller pace number means a faster speed.
- **Using 1.6 for a mile.** A mile is {MI} km. Using 1.6 makes a {mmss(pk)} per km pace {mmss(pk*1.6)} per mile instead of {mmss(pm)}.
- **Mixing km/h and mph on the treadmill.** Setting 10 on an mph machine is a {mmss(6)} per mile sprint, not a {mmss(pk)} per km jog.
- **Converting average speed from split speeds.** Average the times, not the speeds: 1 km at 10 km/h plus 1 km at 15 km/h averages {2/(1/10+1/15):.0f} km/h, not 12.5.
''')

# ---------------------------------------------------------------- Effective field goal
def pc(x, d=1):
    return f"{x * 100:.{d}f}%"


fg, fga, tp, ft, fta = 8, 17, 3, 5, 6
pts = 2 * fg + tp + ft
fgp = fg / fga
efg = (fg + 0.5 * tp) / fga
ts = pts / (2 * (fga + 0.44 * fta))
assert pts == 24 and pc(fgp) == '47.1%' and pc(efg) == '55.9%' and pc(ts) == '61.1%'
two = fg - tp
# eFG% is points from field goals per shot divided by 2
fg_pts = 2 * fg + tp
assert abs(fg_pts / fga / 2 - efg) < 1e-12
tsa = fga + 0.44 * fta
# mistake: entering only two pointers as fg
efg_wrong = (two + 0.5 * tp) / fga
# mistake: using 3PA (say 7) instead of 3PM
tpa = 7
efg_tpa = (fg + 0.5 * tpa) / fga
# shooter comparison: 10 of 20 all twos vs 8 of 20 with 5 threes
a_fg, a_tp, b_fg, b_tp, n = 10, 0, 8, 5, 20
a_e, b_e = (a_fg + 0.5 * a_tp) / n, (b_fg + 0.5 * b_tp) / n
assert b_e > a_e and 2 * a_fg + a_tp < 2 * b_fg + b_tp
# break even: three point % equal in value to a two point %
be_rows = ''
for p3 in (0.30, 0.33, 0.35, 0.36, 0.38, 0.40, 0.45):
    be_rows += f"| {p3*100:.0f}% | {pc(p3*1.5)} | {p3*3:.2f} |\n"
assert pc(0.40 * 1.5) == '60.0%'
# reference grid on 20 attempts
grid = ''
for made in (6, 8, 10, 12):
    cells = ' | '.join(pc((made + 0.5 * t3) / n) if t3 <= made else 'n/a' for t3 in (0, 2, 4, 6))
    grid += f"| {made} of {n} ({pc(made / n, 0)}) | {cells} |\n"
assert pc((10 + 0.5 * 4) / 20) == '60.0%'

edit('sports/effective-field-goal', date=U, phrase='effective field goal percentage calculator',
     title='Effective Field Goal Percentage Calculator (eFG%, TS%, FG%)',
     description='Effective field goal percentage calculator: enter makes, attempts, threes and free throws to get eFG%, true shooting %, FG% and points, with examples.',
     intro=("Effective field goal percentage gives a three pointer 1.5 times the credit of a two, so shooters who take different shot mixes can be compared fairly. "
            "This effective field goal percentage calculator also returns plain FG%, true shooting percentage and points from one box score line.\n\n"
            "Coaches, scouts, fantasy players and fans use it to judge shooting efficiency after a game or season and to see whether more threes or more free throws would help."),
     replace=[('''## How to use the basketball shooting calculator

Enter **field goals made and attempted**, **three-pointers made** and **free throws made and attempted**. Points and the three shooting percentages are calculated.''',
               '''## How to use the effective field goal percentage calculator

Enter **field goals made and attempted**, **three pointers made** and **free throws made and attempted**. Field goals made must include the threes, exactly as a box score shows FGM. The calculator returns points, FG%, eFG% and TS%, and you can also leave an input blank and type a target percentage to solve for it.'''),
              ('''## Example

8/17 FG (3 threes), 5/6 FT:

- Points = **24**
- FG% = **47.1%**, eFG% = **55.9%**, TS% = **61.1%**''',
               f'''## Worked example

The default line is {fg} of {fga} from the field with {tp} threes, and {ft} of {fta} free throws:

- Points = 2 × {fg} + {tp} + {ft} = **{pts}** ({two} twos, {tp} threes and {ft} free throws)
- FG% = {fg} ÷ {fga} = **{pc(fgp)}**
- eFG% = ({fg} + 0.5 × {tp}) ÷ {fga} = {fg + 0.5 * tp:g} ÷ {fga} = **{pc(efg)}**
- TS% = {pts} ÷ (2 × ({fga} + 0.44 × {fta})) = {pts} ÷ {2 * tsa:.2f} = **{pc(ts)}**

The {fg_pts} field goal points on {fga} shots are {fg_pts / fga:.3f} points per shot, and half of that is exactly the {pc(efg)} eFG%. The free throws then lift true shooting to {pc(ts)}.'''),
              ('''## Why eFG% and TS% matter

Plain field-goal percentage treats a three-pointer like a two. Effective FG% adds 50% extra credit for threes, and true shooting % also includes free throws, giving the best single measure of scoring efficiency.''',
               f'''## Why eFG% and TS% matter

Plain field goal percentage treats a three pointer like a two. Effective FG% adds 50% extra credit for each made three, and true shooting % also counts free throws, which makes it the best single measure of scoring efficiency. A player who goes {a_fg} of {n} on twos shoots {pc(a_fg / n)} FG and {pc(a_e)} eFG for {2 * a_fg} points, while one who goes {b_fg} of {n} with {b_tp} threes shoots only {pc(b_fg / n)} FG but {pc(b_e)} eFG and scores {2 * b_fg + b_tp}.'''),
              ('''## Benchmarks (NBA, approximate)

| Rating | FG% | eFG% | TS% |
|---|---|---|---|
| Excellent | 50%+ | 57%+ | 62%+ |
| Above average | 47\u201350% | 54\u201357% | 58\u201362% |
| League average (recent seasons) | about 47% | about 54% | about 58% |
| Below average | under 44% | under 50% | under 54% |

Averages shift as teams take more threes.''',
               '''## Benchmarks (NBA, approximate)

| Rating | FG% | eFG% | TS% |
|---|---|---|---|
| Excellent | 50% or more | 57% or more | 62% or more |
| Above average | 47% to 50% | 55% to 57% | 58% to 62% |
| League average (recent seasons) | about 47% | about 54% to 55% | about 57% to 58% |
| Below average | under 44% | under 50% | under 54% |

Averages shift as teams take more threes, and college, high school and women's leagues run lower, so compare players within the same level and season.'''),
              ('''## The 0.44 factor

TS% uses 0.44 × free-throw attempts to estimate the number of possessions used by free throws, since and-ones and technical fouls do not use a full possession.''',
               '''## The 0.44 factor

TS% uses 0.44 × free throw attempts to estimate the shooting possessions used by free throws. A two shot foul uses one possession for two attempts, while and ones and technical free throws use none, so each attempt counts as a little less than half a possession.'''),
              ('''## Example

8 FG on 17 attempts, 3 threes, 5 of 6 free throws:

- Points = 2 × 8 + 3 + 5 = **24**
- FG% = 8 ÷ 17 = 47.1%
- eFG% = (8 + 1.5) ÷ 17 = **55.9%**
- TS% = 24 ÷ (2 × (17 + 2.64)) = **61.1%**
''', '')],
     body_add=f'''
## eFG% reference table

eFG% on {n} field goal attempts for different makes and numbers of made threes:

| Makes | 0 threes | 2 threes | 4 threes | 6 threes |
|---|---|---|---|---|
{grid}
### Three point percentage as a two point equivalent

Because a three is worth 1.5 twos, a three point percentage times 1.5 gives the two point percentage with the same value per shot:

| 3P% | Equal value 2P% (eFG%) | Points per three attempt |
|---|---|---|
{be_rows}
So a 40% three point shooter produces the same points per attempt as a 60% shooter on twos.

## Practical notes

- **Small samples swing hard.** Turning one miss into a made three in the example game adds {1.5 / fga * 100:.1f} percentage points of eFG%, so judge players over many games.
- **eFG% ignores free throws.** A player who draws many fouls can have an ordinary eFG% and an excellent TS%, as in the example ({pc(efg)} against {pc(ts)}).
- **Team stats work the same way.** Enter team totals to get team eFG%, one of Dean Oliver's four factors along with turnover rate, offensive rebounding and free throw rate.
- **Maximum value.** eFG% can exceed 100%: a player who makes every attempt and all are threes reaches 150%.

## Common mistakes

- **Leaving threes out of field goals made.** FGM already includes threes. Entering only the {two} twos as FG gives an eFG% of {pc(efg_wrong)} instead of {pc(efg)}.
- **Using three point attempts instead of makes.** Only made threes earn the bonus. Typing {tpa} attempts in place of {tp} makes inflates eFG% to {pc(efg_tpa)}.
- **Adding free throws to eFG%.** Free throws belong only in points and TS%; adding them to FGM or FGA breaks the eFG% formula.
- **Comparing eFG% with someone else's FG%.** eFG% is always equal to or higher than FG%, so compare like with like.
- **Forgetting the factor of 2 in TS%.** TS% divides points by 2 × (FGA + 0.44 × FTA); without the 2 the example would show {pc(ts * 2)}.
''',
     faq_replace=[('What is effective field goal percentage?', 'What is effective field goal percentage?',
                   f'It is FG% adjusted for the extra point a three is worth: (FG + 0.5 × 3PM) ÷ FGA. For example ({fg} + 0.5 × {tp}) ÷ {fga} = {pc(efg)}.'),
                  ('What is true shooting percentage?', 'What is true shooting percentage?',
                   'It is points per shooting possession, including free throws: PTS ÷ (2 × (FGA + 0.44 × FTA)), expressed as a percentage.'),
                  ('What is a good TS%?', 'What is a good TS%?',
                   'Around 57% to 58% is roughly NBA league average in recent seasons, above 60% is very good and above 62% is excellent.'),
                  ('What is a good true shooting percentage?', 'What is a good eFG%?',
                   'In the NBA about 54% to 55% is league average in recent seasons, and 57% or higher is excellent. College and high school averages are lower.')])

print('improve 2026-11-23 done')
