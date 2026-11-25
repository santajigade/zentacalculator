"""Improve pass (2026-11-25), section b: engineering/heat-duty, math/significant-figures and
math/inverse-trig. Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the
"<topic> calculator" phrase, worked examples from the calculator defaults, reference tables
computed here, practical notes and common mistakes. Slug, category, variables, equations,
related and published are unchanged (asserted by inplace.edit). Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-25'
EM = chr(0x2014)
MINUS = chr(0x2212)


def neg_(v):
    return str(v).replace('-', MINUS)


def f2(x):
    return f"{x:,.2f}"


# ---------------------------------------------------------------- Heat duty
m, cp, dT = 2.0, 4.186, 10.0
Q_W = m * cp * 1000 * dT          # calculator equation, watts
Q = Q_W / 1000                    # kW
assert abs(Q - 83.72) < 1e-9
HP = 745.69987                    # W per mechanical hp
q_hp = Q_W / HP
q_kjh = Q * 3600
q_btuh = Q_W * 3.412142
q_tr = Q / 3.517
m_lbh = m * 3600 / 0.45359237
dT_F = dT * 1.8
assert abs(q_hp - 112.27) < 0.01 and abs(m_lbh - 15873) < 1

# flow needed for 100 kW, with stated properties
props = (('Water', 4.186, 998), ('Glycol 30%', 3.7, 1040), ('Thermal oil', 2.2, 870))
flow_rows = ''
for name, c, rho in props:
    cells = []
    for d in (5, 10, 15, 20):
        mm = 100 / (c * d)
        cells.append(f"{mm * 3600 / rho:.1f}")
    flow_rows += f"| {name} (c<sub>p</sub> {c}, ρ {rho} kg/m³) | " + ' | '.join(cells) + ' |\n'
w5 = 100 / (4.186 * 5) * 3600 / 998
assert abs(w5 - 17.2) < 0.05
two_m3h = 2 * 998 / 3600

desc_hd = 'Heat duty calculator: find heating or cooling power in kW from mass flow, specific heat and temperature change, for heat exchangers, chillers and boilers.'

edit('engineering/heat-duty', date=U,
     title='Heat Duty Calculator: Q = ṁ·cp·ΔT in kW and hp',
     description=desc_hd,
     replace=[('''## Worked example

2 kg/s of water cooled by 10 °C in a heat exchanger:

Q̇ = 2 × 4.186 × 10 = **83.7 kW**''',
               f'''## Worked example with the default values

A heat exchanger cools {m:g} kg/s of water (c<sub>p</sub> = {cp} kJ/kg·K) by {dT:g} K:

1. Q̇ = ṁ × c<sub>p</sub> × ΔT = {m:g} × {cp} × {dT:g} = **{Q:.2f} kW**
2. In other units: {q_hp:.1f} hp, {q_kjh:,.0f} kJ/h, {q_btuh:,.0f} Btu/h or {q_tr:.2f} TR

The calculator multiplies c<sub>p</sub> by 1,000 to work in J/kg·K, so the raw result is {Q_W:,.0f} W, shown as {Q:.2f} kW. In imperial mode the same inputs read as {m_lbh:,.0f} lb/h and an {dT_F:g} °F difference; the duty does not change, only the units on screen.'''),
              ('''## Result with the default values

The defaults are 2 kg/s of water, c<sub>p</sub> = 4.186 kJ/kg·K and a 10 K change, so Q = 2 × 4.186 × 10 = **83.72 kW**.

''', ''),
              (f'''## Practical uses

- **Chiller and boiler sizing** {EM} enter design flow and ΔT.
- **Energy metering** {EM} BTU/energy meters calculate exactly this using a flow meter and two temperature sensors (often matched Pt100 or Pt500 pairs).
- **Checking performance** {EM} compare measured duty with the design value to spot fouling.''',
               '''## Practical uses

- **Chiller and boiler sizing:** enter the design flow and ΔT, then convert the duty to tons with the [chiller tonnage calculator](/engineering/chiller-tonnage/).
- **Energy metering:** BTU and thermal energy meters compute exactly this product from a flow meter and two temperature sensors, usually a matched Pt100 or Pt500 pair.
- **Exchanger sizing:** once the duty is known, the [LMTD calculator](/engineering/lmtd/) gives the driving temperature difference for Q = U × A × LMTD.
- **Steam heating:** for a steam heated exchanger, the [steam consumption calculator](/engineering/steam-consumption/) turns the duty into kg/h of steam.
- **Checking performance:** a measured duty falling below the design value at the same flow points to fouling or a control valve that is not opening fully.'''),
              ('''Volumetric flow in m³/h for each fluid and design temperature difference:

| Fluid | ΔT 5 K | ΔT 10 K | ΔT 15 K | ΔT 20 K |
|---|---|---|---|---|
| Water | 17.2 | 8.6 | 5.7 | 4.3 |
| Glycol 30% | 18.7 | 9.4 | 6.2 | 4.7 |
| Thermal oil | 38.5 | 19.3 | 12.8 | 9.6 |
''',
               f'''Volumetric flow in m³/h for each fluid and design temperature difference, from V = Q ÷ (ρ × c<sub>p</sub> × ΔT) with the properties shown (typical values; check your fluid data sheet):

| Fluid | ΔT 5 K | ΔT 10 K | ΔT 15 K | ΔT 20 K |
|---|---|---|---|---|
{flow_rows}'''),
              ('convert with density first (0.554 kg/s for water)',
               f'convert with density first (about {two_m3h:.3f} kg/s for water)')],
     faq_add=[('How do I convert heat duty from kW to Btu/h or tons?',
               f'Multiply kW by 3,412 for Btu/h and divide by 3.517 for tons of refrigeration. The default {Q:.2f} kW is about {q_btuh:,.0f} Btu/h or {q_tr:.1f} TR.')])

# ---------------------------------------------------------------- Significant figures


def sig(x, n):
    """Calculator equations: ex, r, m."""
    ex = math.floor(math.log10(abs(x)))
    r = math.copysign(1, x) * math.floor(abs(x) / 10 ** (ex - n + 1) + 0.5) * 10 ** (ex - n + 1)
    return ex, r, r / 10 ** ex


def dec(x, dp):
    return math.copysign(1, x) * math.floor(abs(x) * 10 ** dp + 0.5) / 10 ** dp


ex0, r0, m0 = sig(1234.5678, 3)
assert ex0 == 3 and abs(r0 - 1230) < 1e-9 and abs(m0 - 1.23) < 1e-12
assert abs(dec(1234.5678, 2) - 1234.57) < 1e-9

xs = -0.0045678
ex1, r1, m1 = sig(xs, 3)
unit1 = 10 ** (ex1 - 3 + 1)
scaled = abs(xs) / unit1
rd1 = dec(xs, 2)
assert ex1 == -3 and abs(r1 + 0.00457) < 1e-12 and abs(m1 + 4.57) < 1e-9 and rd1 == 0
rd1s = '0.00' if rd1 == 0 else f'{rd1:.2f}'


def fmt_sig(v, n):
    ex = math.floor(math.log10(abs(v)))
    d = max(0, n - 1 - ex)
    return f"{v:,.{d}f}"


prec_rows = ''
for n in range(1, 8):
    ex, r, mm = sig(1234.5678, n)
    unit = 10 ** (ex - n + 1)
    half = unit / 2
    rel = half / r * 100
    us = f"{unit:g}"
    hs = f"{half:g}"
    prec_rows += f"| {n} | {fmt_sig(r, n)} | {mm:.{n-1}f} × 10³ | {us} | ±{hs} | {fmt_sig(rel, 2)}% |\n"

# calculations with measured values
a, b = 12.5, 3.2
area = a * b
_, area2, _ = sig(area, 2)
assert abs(area - 40.0) < 1e-9 and area2 == 40
s1, s2 = 12.52, 3.1
tot = s1 + s2
assert f"{tot:.1f}" == '15.6'
dia = 2 * 4.37
assert f"{dia:.2f}" == '8.74'

edit('math/significant-figures', date=U, phrase='significant figures calculator',
     intro=("Significant figures show how precisely a number is known: 1,230 to three significant figures is a different claim from 1,234.5678. "
            "This significant figures calculator rounds any number to the sig figs you choose, gives the power of ten for scientific notation and also rounds to fixed decimal places, rounding halves away from zero.\n\n"
            "Students use it to check chemistry and physics homework, and lab technicians and engineers use it to report measured results without claiming more precision than the instrument gives."),
     body_add=f'''
## Second example: a small negative number

Round {neg_(xs)} to 3 significant figures and to 2 decimal places:

1. e = ⌊log<sub>10</sub> {abs(xs)}⌋ = **{neg_(ex1)}**, because the first significant digit (4) is in the thousandths place
2. Rounding unit = 10<sup>{neg_(ex1)} − 3 + 1</sup> = 10<sup>{neg_(ex1 - 2)}</sup>, and {abs(xs)} ÷ 10<sup>{neg_(ex1 - 2)}</sup> = {scaled:.2f}, which rounds to 457
3. Rounded to 3 sig figs = **{neg_(f"{r1:.5f}")}** = {neg_(f"{m1:.2f}")} × 10<sup>{neg_(ex1)}</sup>
4. Rounded to 2 decimal places = **{rd1s}**

The sign is kept aside and put back at the end, so negative numbers round the same way as positive ones. The decimal place result shows why fixed decimals are a poor choice for very small values: every digit is lost.

## How much precision each figure claims

Rounding 1,234.5678 to more figures shrinks the rounding unit, and the largest error a rounded value can carry is half that unit:

| Sig figs | Rounded | Scientific notation | Rounding unit | Max rounding error | Relative error |
|---|---|---|---|---|---|
{prec_rows}
Each extra figure makes the claim ten times tighter. Three figures already pins this value to within about 0.4%, which is better than most everyday measurements.

## Significant figures in calculations

- **Multiplying:** a plate measured as {a} cm by {b} cm has an area of {a} × {b} = {area:.1f} cm² on a calculator. {b} has only 2 significant figures, so report **{area2:.0f} cm²** (better written 4.0 × 10¹ cm² to show both figures).
- **Adding:** {s1} g + {s2} g = {tot:.2f} g, but {s2} is known only to one decimal place, so report **{tot:.1f} g**.
- **Exact factors:** the diameter of a circle with radius 4.37 cm is 2 × 4.37 = **{dia:.2f} cm**. The 2 is exact and does not limit the answer to one figure.

## Common mistakes

- **Counting leading zeros.** 0.0045678 has five significant figures, not seven; zeros in front of the first non-zero digit only place the decimal point.
- **Rounding in stages.** 1.2449 to 2 significant figures is 1.2. Rounding first to 1.245 and then to 1.25 and 1.3 gives a wrong answer; always round the original value once.
- **Rounding intermediate results.** Keep all digits through a multi step calculation and round only the final answer, or small errors build up.
- **Dropping significant trailing zeros.** A reading of 2.50 V has three figures; writing 2.5 V throws away the information that the last digit was measured.
- **Using the wrong rule for sums.** Addition and subtraction follow decimal places, not significant figures, so 100.2 + 0.0345 is 100.2, not 100.2345 or 100.
- **Entering zero.** Zero has no first significant digit (log<sub>10</sub> 0 is undefined), so the calculator cannot round it; 0 to any number of figures is simply 0.
''',
     faq_add=[('Do exact numbers limit the significant figures of an answer?',
               'No. Counted values and defined constants, such as 12 eggs, the 2 in d = 2r or 100 cm in 1 m, are exact and have unlimited significant figures. Only measured values set how many figures the answer keeps.')])

# ---------------------------------------------------------------- Inverse trig
x = 0.5
asn, ac, at = math.asin(x), math.acos(x), math.atan(x)
act = math.pi / 2 - math.atan(x)
D = math.degrees
assert abs(D(asn) - 30) < 1e-9 and abs(D(ac) - 60) < 1e-9
assert f"{D(at):.4f}" == '26.5651' and f"{D(act):.4f}" == '63.4349'

# ramp at 1:12
rr = 1 / 12
ramp = D(math.atan(rr))
ramp_pct = rr * 100
tri_rows = ''
for o, ad in ((3, 4), (5, 12), (8, 15), (7, 24), (20, 21), (1, 1)):
    h = math.hypot(o, ad)
    hs = f"{h:g}" if h == int(h) else '√2'
    A = D(math.atan2(o, ad))
    assert abs(D(math.asin(o / h)) - A) < 1e-9 and abs(D(math.acos(ad / h)) - A) < 1e-9
    tri_rows += f"| {o}, {ad}, {hs} | {o}/{hs} | {ad}/{hs} | {o}/{ad} | {A:.2f}° | {90 - A:.2f}° |\n"
a345 = D(math.atan2(3, 4))
neg = D(math.pi / 2 - math.atan(-1))
assert abs(neg - 135) < 1e-9
quad = D(math.atan2(-1, -1))
assert abs(quad + 135) < 1e-9

edit('math/inverse-trig', date=U, phrase='inverse trig calculator',
     intro=("The inverse trigonometric functions run sine, cosine and tangent backwards: given a ratio, they return the angle. "
            "This inverse trig calculator finds arcsin, arccos, arctan and arccot of any number in degrees or radians, using the standard principal value ranges, and also works from an angle back to its ratio.\n\n"
            "Students, surveyors, builders and engineers use it to find an angle from the sides of a right triangle, the pitch of a roof or ramp, or the phase angle of a phasor."),
     body_add=f'''
## Example: the angle of a wheelchair ramp

A ramp that rises 1 unit for every 12 units of run has a ratio of 1 ÷ 12 = {rr:.4f}. Enter that as the value and read arctan: **{ramp:.2f}°**, a gradient of {ramp_pct:.2f}%. Going the other way, to keep a ramp below 5°, enter 5° in the arctan box: the value returned is {math.tan(math.radians(5)):.4f}, so the ramp needs at least {1 / math.tan(math.radians(5)):.1f} units of run per unit of rise.

## Angles of right triangles with whole number sides

For a right triangle, arcsin(opposite ÷ hypotenuse), arccos(adjacent ÷ hypotenuse) and arctan(opposite ÷ adjacent) all give the same angle. The other acute angle is 90° minus it:

| Sides (opp, adj, hyp) | sin θ | cos θ | tan θ | θ | 90° − θ |
|---|---|---|---|---|---|
{tri_rows}
The 3, 4, 5 triangle is the one builders use to set out a square corner; its smaller angle is {a345:.2f}°, not the 30° or 45° people often assume.

## Common mistakes

- **Calculator in the wrong angle mode.** arcsin 0.5 is 30 in degrees but {asn:.4f} in radians. Spreadsheets and programming languages always return radians.
- **Asking for arcsin or arccos outside −1 to 1.** No angle has a sine of 1.2, so the result is undefined. A ratio above 1 usually means the opposite and hypotenuse were swapped.
- **Forgetting the second solution.** arcsin 0.5 returns only 30°, but 150° has the same sine. In the law of sines this is the ambiguous case.
- **Using arctan(y/x) for a direction.** The point (−1, −1) gives arctan 1 = 45°, while its real direction is {neg_(f"{quad:.0f}")}° (or {quad + 360:.0f}°). Use atan2(y, x) for vectors and coordinates.
- **Assuming every source defines arccot the same way.** Here arccot x = 90° − arctan x, so arccot(−1) = {neg:.0f}°. Some software uses arctan(1/x) instead, which gives −45° for the same input.
''',
     faq_add=[('Why do I get an error for arcsin of 2?',
               'The sine of a real angle is never larger than 1 or smaller than −1, so arcsin and arccos are undefined outside that range. Check the ratio: opposite ÷ hypotenuse can never exceed 1 because the hypotenuse is the longest side.')])

print('done', __import__('inplace').DONE)
