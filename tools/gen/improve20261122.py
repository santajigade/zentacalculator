"""Improve pass (2026-11-22) for three thin pages from the first batch (2026-10-27):
sports/win-percentage, sports/baseball-era, everyday-life/typing-speed.
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples built from the calculator defaults, reference tables computed here,
practical notes, common mistakes, dash-free rewrites of edited text and near-duplicate FAQs replaced.
Slug, category, variables, equations, related and published are unchanged (asserted by inplace.edit).
Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-22'


def c(x, d=0):
    return f"{x:,.{d}f}"


def dec3(p):
    s = f"{p:.3f}"
    return s[1:] if s.startswith('0') else s


# ---------------------------------------------------------------- Win percentage
w, l, t = 42, 28, 2
gp = w + l + t
pct = (w + t / 2) / gp
wl = w / l
assert abs(pct * 100 - 59.72) < 0.01 and abs(wl - 1.5) < 1e-9
pct_ignore = w / (w + l)
# target: .600 over an 82 game season with 10 games left
season = 82
left = season - gp
need_pts = 0.600 * season - (w + t / 2)
need_w = math.ceil(need_pts - 1e-9)
# games behind: leader 50-22
lw, ll = 50, 22
gb = ((lw - w) + (l - ll)) / 2
# Pythagorean expectation, 750 scored, 650 allowed, 162 games
S, A = 750, 650
py2 = S ** 2 / (S ** 2 + A ** 2)
py183 = S ** 1.83 / (S ** 1.83 + A ** 1.83)
# records table: ties as half vs ties ignored
rec_rows = ''
for a, b, d in ((10, 6, 0), (9, 6, 1), (8, 5, 3), (42, 28, 2), (12, 3, 2), (25, 25, 4)):
    half = (a + d / 2) / (a + b + d)
    ign = a / (a + b)
    rec_rows += f"| {a}-{b}-{d} | {a+b+d} | {dec3(half)} ({half*100:.1f}%) | {dec3(ign)} ({ign*100:.1f}%) |\n"

edit('sports/win-percentage', date=U, phrase='win percentage calculator',
     title='Win Percentage Calculator: Wins, Losses and Ties',
     description='Win percentage calculator for teams and players: enter wins, losses and ties to get the winning percentage and win to loss ratio, with a worked example.',
     intro=("Win percentage is the share of games won, with a tie usually counted as half a win and half a loss. "
            "This win percentage calculator turns a record of wins, losses and ties into a winning percentage and a win to loss ratio.\n\n"
            "Coaches, league organisers, fantasy players and fans use it to rank teams with different numbers of games played, track a season and work out the wins still needed."),
     replace=[('''## How to use the win percentage calculator

Enter **wins**, **losses** and **ties**. Win percentage and win–loss ratio are calculated.''',
               '''## How to use the win percentage calculator

Enter **wins**, **losses** and **ties**. The calculator returns the win percentage, with each tie counted as half a win, and the win to loss ratio (wins divided by losses).'''),
              ('''## Example

42 wins, 28 losses, 2 ties: (42 + 1) ÷ 72 = **59.7%** (.597).''',
               f'''## Worked example

A team has a record of {w}-{l}-{t} (wins, losses, ties):

- Games played = {w} + {l} + {t} = **{gp}**
- Win % = ({w} + {t} ÷ 2) ÷ {gp} = {w + t/2:g} ÷ {gp} = **{pct*100:.1f}%**, written as **{dec3(pct)}** in US standings
- Win to loss ratio = {w} ÷ {l} = **{wl:.2f}**

If the league ignored ties, the same record would give {w} ÷ {w + l} = {dec3(pct_ignore)} ({pct_ignore*100:.1f}%), so always check which rule a table uses.

### Wins needed for a target

With {left} games left in an {season}-game season, finishing at .600 needs 0.600 × {season} = {0.6*season:.1f} win points. The team already has {w + t/2:g}, so it needs {need_pts:.1f} more, which means **{need_w} wins** from the last {left} games (assuming no more ties).''')],
     body_add=f'''
## Ties counted as half or ignored

The rule for ties matters most when a record has many of them. Both versions for some example records:

| Record (W-L-T) | Games | Ties as half a win | Ties ignored |
|---|---|---|---|
{rec_rows}
The NFL has counted ties as half a win since 1972, and most school and college standings do the same. Records without ties give the same answer either way.

## Games behind example

If the division leader is {lw}-{ll} and this team is {w}-{l}, the team is (({lw} - {w}) + ({l} - {ll})) ÷ 2 = **{gb:g} games behind**. Games behind and win percentage can disagree when teams have played different numbers of games, which is why final standings are ranked by win percentage.

## Pythagorean expectation example

A baseball team that scores {S} runs and allows {A} has an expected win percentage of {S}² ÷ ({S}² + {A}²) = **{dec3(py2)}**, or about {py2*162:.0f} wins over 162 games. Using the refined exponent of 1.83 gives {dec3(py183)} (about {py183*162:.0f} wins). A team far above its expected record has usually won an unusual share of close games, and tends to drift back towards the expectation.

## Common mistakes

- **Dividing wins by losses.** {w} ÷ {l} = {wl:.2f} is the win to loss ratio, not the win percentage of {pct*100:.1f}%.
- **Mixing up the decimal and the percentage.** A record of {dec3(pct)} means {pct*100:.1f}%, not 0.597%.
- **Ranking early season tables by wins.** A 6-2 team ({6/8*100:.0f}%) is ahead of an 8-4 team ({8/12*100:.1f}%) even though it has fewer wins.
- **Treating overtime losses as ties.** Ice hockey leagues award a point for an overtime loss and rank by points percentage (points ÷ twice the games played) instead.
- **Applying the wrong tie rule.** Some competitions ignore ties or use league points, so copy the rule from the league before comparing.
''',
     faq_replace=[('How many wins do I need for a target percentage?', 'How many wins do I need for a target percentage?',
                   f'Multiply the target by the total games, subtract the wins (plus half the ties) you already have and round up. A {w}-{l}-{t} team needs {need_w} wins from its last {left} games to finish an {season}-game season at .600. You can also press × on Wins and type the target percentage.'),
                  ('How do I calculate win percentage?', 'Is win percentage the same as win to loss ratio?',
                   f'No. Win percentage divides wins by all games played, while the win to loss ratio divides wins by losses. A {w}-{l}-{t} record is {pct*100:.1f}% but has a ratio of {wl:.2f}.')],
     faq_add=[('Do overtime losses count as losses in win percentage?',
               'In a plain win percentage, yes: an overtime loss is a loss. Ice hockey leagues give a point for an overtime loss and rank teams by points percentage, which is points divided by twice the games played.')])

# ---------------------------------------------------------------- ERA and WHIP
er, ip, h, bb = 45, 150.0, 130, 40
era = 9 * er / ip
whip = (h + bb) / ip
assert abs(era - 2.70) < 1e-9 and abs(whip - 1.1333) < 1e-4
# innings notation trap: 3 ER in 6 2/3 innings
right = 9 * 3 / (6 + 2 / 3)
wrong = 9 * 3 / 6.2
# one start after the default line
start_rows = ''
for ip_s, er_s in ((7, 0), (6, 2), (5 + 1 / 3, 4), (3, 6), (1 + 2 / 3, 8)):
    era2 = 9 * (er + er_s) / (ip + ip_s)
    whole = int(ip_s)
    thirds = round((ip_s - whole) * 3)
    note = f"{whole}.{thirds}" if thirds else f"{whole}.0"
    start_rows += f"| {note} IP, {er_s} ER | {9*er_s/ip_s:.2f} | {era2:.2f} | {era2-era:+.2f} |\n"
# FIP with an assumed constant of 3.10
hr, hbp, k, cfip = 15, 5, 160, 3.10
fip = (13 * hr + 3 * (bb + hbp) - 2 * k) / ip + cfip
# 7 inning ERA
era7 = 7 * er / ip

edit('sports/baseball-era', date=U, phrase='ERA calculator',
     title='ERA Calculator: Earned Run Average and WHIP',
     description='ERA calculator for baseball pitchers: enter earned runs, innings, hits and walks to get earned run average and WHIP, with innings notation explained.',
     intro=("Earned run average (ERA) is the number of earned runs a pitcher allows per nine innings, the standard way to compare pitching. "
            "This ERA calculator also returns WHIP, the walks plus hits allowed per inning.\n\n"
            "Coaches, scorekeepers, fantasy players and fans use it to rate pitchers over a season, check box score figures and see how one start moves a pitcher's numbers."),
     replace=[('''## Example

45 earned runs in 150 innings, 130 hits and 40 walks:

- ERA = **2.70**
- WHIP = **1.13**''',
               f'''## Worked example

A pitcher has allowed {er} earned runs, {h} hits and {bb} walks in {ip:g} innings:

- ERA = 9 × {er} ÷ {ip:g} = {9*er:g} ÷ {ip:g} = **{era:.2f}**
- WHIP = ({h} + {bb}) ÷ {ip:g} = {h + bb} ÷ {ip:g} = **{whip:.2f}**

So the pitcher allows under three earned runs per nine innings and a little more than one base runner per inning, both well above league average.'''),
              ('''| Rating | ERA | WHIP |
|---|---|---|
| Excellent | under 3.00 | under 1.10 |
| Above average | 3.00–3.75 | 1.10–1.25 |
| Average | 3.75–4.50 | 1.25–1.35 |
| Below average | 4.50–5.25 | 1.35–1.45 |
| Poor | over 5.25 | over 1.45 |''',
               '''| Rating | ERA | WHIP |
|---|---|---|
| Excellent | under 3.00 | under 1.10 |
| Above average | 3.00 to 3.75 | 1.10 to 1.25 |
| Average | 3.75 to 4.50 | 1.25 to 1.35 |
| Below average | 4.50 to 5.25 | 1.35 to 1.45 |
| Poor | over 5.25 | over 1.45 |'''),
              ('''Innings are recorded in thirds: “6.1” means 6⅓ innings and “6.2” means 6⅔. Convert to decimals before calculating — 6.1 becomes 6.333 and 6.2 becomes 6.667.''',
               f'''Innings are recorded in thirds, one for each out: "6.1" means 6⅓ innings and "6.2" means 6⅔. Convert to decimals before calculating, so 6.1 becomes 6.333 and 6.2 becomes 6.667. For 3 earned runs in 6⅔ innings the correct ERA is 27 ÷ 6.667 = **{right:.2f}**; typing 6.2 instead gives {wrong:.2f}, an error of {wrong-right:.2f} runs from a single start.''')],
     body_add=f'''
## How one start moves the ERA

Starting from the {era:.2f} ERA over {ip:g} innings above, this is what different next starts would do:

| Next start | ERA for that start | Season ERA after | Change |
|---|---|---|---|
{start_rows}
A bad short outing does far more damage than a long good one repairs, because the earned runs are spread over very few innings. Early in a season, when a pitcher has only 20 or 30 innings, a single start can move ERA by more than a run.

## FIP example

Fielding Independent Pitching uses only the outcomes a pitcher controls: FIP = (13 × HR + 3 × (BB + HBP) - 2 × K) ÷ IP + constant. With {hr} home runs, {bb} walks, {hbp} hit batters and {k} strikeouts in {ip:g} innings, and a league constant of about {cfip:.2f}, FIP = ({13*hr} + {3*(bb+hbp)} - {2*k}) ÷ {ip:g} + {cfip:.2f} = **{fip:.2f}**. An ERA well below FIP often means good defence or luck on balls in play.

## Seven inning games

High school and many youth leagues play seven innings, so ERA is often scaled by 7: the same {er} earned runs in {ip:g} innings gives 7 × {er} ÷ {ip:g} = **{era7:.2f}**. Compare pitchers only on the same scale.

## Common mistakes

- **Typing scorebook innings as decimals.** 6.2 innings is 6.667, not 6.2, so the ERA comes out too high.
- **Counting unearned runs.** Runs that score after an error that should have ended the inning are left out of ERA, though they still count in runs allowed.
- **Including hit batters in WHIP.** WHIP counts only walks and hits; hit by pitch and errors are not added.
- **Judging small samples.** A reliever with 10 innings and 6 earned runs has a 5.40 ERA that can drop to 3.00 within a few clean outings.
- **Comparing across eras and parks.** League average ERA changes with the era and the ballpark, so adjusted figures such as ERA+ are used for fair comparisons.
''',
     faq_replace=[('What is a good ERA?', 'What is a good ERA?',
                   'In Major League Baseball an ERA under 3.00 is excellent, and the league average has been roughly 4.00 to 4.30 in recent seasons. In youth and amateur leagues averages are usually higher.'),
                  ('How do I enter 6⅔ innings?', 'Can ERA go up after a good start?',
                   f'Yes, if the start is good but still worse than the season so far. A pitcher with a {era:.2f} ERA who allows 2 earned runs in 6 innings (a 3.00 start) sees the season ERA rise slightly, to {9*(er+2)/(ip+6):.2f}.')],
     faq_add=[('What is the difference between ERA and FIP?',
               f'ERA counts every earned run, so it depends partly on the fielders behind the pitcher. FIP uses only home runs, walks, hit batters and strikeouts; for the example pitcher it is {fip:.2f} against an ERA of {era:.2f}.')])

# ---------------------------------------------------------------- Typing speed
ch, err, tm = 1250, 5, 5.0
gross = ch / 5 / tm
net = gross - err / tm
cpm = ch / tm
acc = (ch - err) / ch * 100
kph = cpm * 60
assert abs(gross - 50) < 1e-9 and abs(net - 49) < 1e-9 and abs(cpm - 250) < 1e-9
# one minute test
ch1, e1 = 330, 8
g1 = ch1 / 5
n1 = g1 - e1
a1 = (ch1 - e1) / ch1 * 100
# time to type documents
doc_rows = ''
for wpm in (30, 40, 50, 60, 80, 100):
    doc_rows += f"| {wpm} | {wpm*5*60:,} | {500/wpm:.1f} min | {1000/wpm:.1f} min | {2500/wpm:.0f} min |\n"

edit('everyday-life/typing-speed', date=U, phrase='typing speed calculator',
     description='Typing speed calculator: turn characters typed, errors and test time into gross WPM, net WPM, characters per minute and accuracy, with job benchmarks.',
     intro=("Typing speed is measured in words per minute (WPM), where a word is any 5 characters including spaces, and errors are subtracted to give net WPM. "
            "This typing speed calculator works out gross WPM, net WPM and characters per minute from a test.\n\n"
            "Job seekers, students, teachers and employers use it to score typing tests, check data entry requirements and track practice over weeks."),
     replace=[('''## Example

1,250 characters in 5 minutes with 5 errors:

- Gross = 250 words ÷ 5 = **50 WPM**
- Net = 50 − 1 = **49 WPM**''',
               f'''## Worked example

A 5 minute test produces {ch:,} characters (spaces included) with {err} uncorrected errors:

- Standard words = {ch:,} ÷ 5 = {ch//5}
- Gross WPM = {ch//5} ÷ {tm:g} = **{gross:.1f}**
- Net WPM = {gross:.0f} - {err} ÷ {tm:g} = **{net:.1f}**
- Characters per minute = {ch:,} ÷ {tm:g} = **{cpm:.0f}**
- Accuracy = ({ch:,} - {err}) ÷ {ch:,} = **{acc:.1f}%**

### A one minute test

{ch1} characters in 1 minute with {e1} errors gives a gross speed of {g1:.0f} WPM but a net speed of only **{n1:.0f} WPM**, at {a1:.1f}% accuracy. On a short test every error costs a full word per minute, so accuracy matters more than raw speed.'''),
              ('''## Words per minute vs keystrokes per hour

Data-entry tests sometimes use **keystrokes per hour (KPH)**: KPH = characters per minute × 60. 250 characters per minute is 15,000 KPH.''',
               f'''## Words per minute vs keystrokes per hour

Data entry tests often use **keystrokes per hour (KPH)**: KPH = characters per minute × 60. The example's {cpm:.0f} characters per minute is **{kph:,.0f} KPH**. Numeric keypad tests are scored in KPH because WPM makes little sense for strings of digits.''')],
     body_add=f'''
## How long a document takes at each speed

| Net WPM | Keystrokes per hour | 500 words | 1,000 words | 2,500 words |
|---|---|---|---|---|
{doc_rows}
Real documents take longer than these figures because of thinking, formatting and corrections; the table shows pure typing time.

## How typing tests are scored

Most online and employment tests show a passage, time the typing for 1, 3 or 5 minutes and compare the result with the original text. Gross WPM uses every character typed; net WPM takes off one word per minute for each error left uncorrected. Errors you fix with backspace do not count against net WPM, but the time spent fixing them lowers the gross figure. Results from 1 minute tests usually run a few WPM higher than 5 minute tests, so a job advert asking for 50 WPM normally means a longer, accuracy checked test.

## Common mistakes

- **Counting real words.** Typing tests count every 5 characters as a word, so a passage of long technical words scores the same as one of short words.
- **Leaving out spaces.** Spaces and punctuation are keystrokes; dropping them cuts the result by about a sixth for normal English text.
- **Subtracting the total errors.** Net WPM subtracts errors per minute: 5 errors in 5 minutes costs 1 WPM, not 5.
- **Comparing tests of different lengths.** A 1 minute burst is not comparable with a 10 minute transcription test.
- **Chasing speed with low accuracy.** Below about 95% accuracy the corrections usually cost more time than the extra speed saves.
''',
     faq_replace=[('What is net WPM?', 'What is net WPM?',
                   f'Gross WPM minus uncorrected errors per minute. {err} errors in a {tm:g} minute test cost {err/tm:g} WPM, so a gross {gross:.0f} WPM becomes a net {net:.0f} WPM.')],
     faq_add=[('How many keystrokes per hour is a typing speed in WPM?',
               f'Multiply WPM by 5 characters and by 60 minutes. 50 WPM is 15,000 keystrokes per hour, and 40 WPM is 12,000.')])

print('improve 2026-11-22 done')
