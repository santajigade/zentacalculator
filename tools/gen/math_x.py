import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
f = lambda x, d=0: f"{x:,.{d}f}"
pi = math.pi

# arc length
rows = ''.join(f"| {a}° | {a*pi/180:.4f} | {10*a*pi/180:.2f} | {100*a*pi/360:.2f} | {20*math.sin(a*pi/360):.2f} |\n" for a in [30, 45, 60, 90, 120, 180, 270, 360])
expand('math/arc-length', f'''
## Arc, sector and chord for radius 10

| Angle | Radians | Arc length | Sector area | Chord |
|---|---|---|---|---|
{rows}
## Degrees and radians

<p class="formula">radians = degrees × π ÷ 180</p>

The arc-length formula L = rθ only works with the angle in **radians**. If you prefer degrees, use L = 2πr × (θ ÷ 360). The calculator converts automatically when you pick degrees.

## Segment area

The area between the chord and the arc (a circular segment) is the sector minus the triangle:

<p class="formula">Segment area = r² ÷ 2 × (θ − sin θ)</p>

For r = 10 and θ = 60°, that is 50 × (1.0472 − 0.8660) = **9.06**.

## Finding the angle or radius

- Angle from arc length: θ = L ÷ r
- Radius from arc length: r = L ÷ θ
- Radius from a chord and height (sagitta s): r = (c² ÷ 4 + s²) ÷ (2s)

The last one is handy for measuring large curves, such as an arch or a curved wall, where you cannot reach the centre.
''', [
 ('How do I find arc length without the angle?', 'If you know the chord c and radius r, the angle is θ = 2 × asin(c ÷ 2r). Then arc length = r × θ.'),
 ('What is the arc length of a semicircle?', 'Half the circumference: π × r. For radius 10 it is about 31.42.'),
], before='## Practical uses')

# average
expand('math/average', '''
## Mean, median and mode compared

For the data 2, 3, 3, 5, 7, 10, 40:

| Measure | Value | How |
|---|---|---|
| Mean | 10 | Sum 70 ÷ 7 values |
| Median | 5 | Middle value when sorted |
| Mode | 3 | Most frequent value |
| Range | 38 | 40 − 2 |

The single large value (40) pulls the mean up to 10, while the median stays at 5. That is why median income and median house prices are often reported instead of the mean.

## Other kinds of average

| Average | Use it for | Example |
|---|---|---|
| Arithmetic mean | Most everyday data | Test scores |
| Weighted mean | Values with different importance | Course grades with credits |
| Geometric mean | Growth rates and ratios | Average yearly investment return |
| Harmonic mean | Rates over the same distance | Average speed for a round trip |

Example: driving 60 km at 60 km/h and back at 40 km/h is **48 km/h** on average (harmonic mean), not 50.

## Finding a missing value for a target average

To reach an average of 80 over 5 tests when the first four average 76, you need 80 × 5 − 76 × 4 = **96** on the last test. The [grade needed calculator](/everyday-life/grade-needed/) does this for exams.

## Pasting data

You can paste numbers separated by commas, spaces or new lines, straight from a spreadsheet column. For spread and variability, see the [standard deviation calculator](/statistics/standard-deviation/).
''', [
 ('What is the average of 10, 20 and 30?', '(10 + 20 + 30) ÷ 3 = 20.'),
 ('Can the average be a value that is not in the data?', 'Yes. The mean of 1 and 2 is 1.5, which is not one of the values. The median of an even number of values can also fall between two values.'),
], before='## Weighted averages')

# circle
rows = ''.join(f"| {r} | {2*r} | {2*pi*r:.2f} | {pi*r*r:.2f} |\n" for r in [1, 2, 5, 10, 15, 20, 50, 100])
expand('math/circle', f'''
## Circle measurements table

| Radius | Diameter | Circumference | Area |
|---|---|---|---|
{rows}
## Finding everything from one value

| You know | Radius = |
|---|---|
| Diameter d | d ÷ 2 |
| Circumference C | C ÷ (2π) |
| Area A | √(A ÷ π) |

Once you have the radius, everything else follows. The calculator does this for you — fill in any one field.

## Area from diameter

A useful shortcut when you measure across a pipe or a round table:

<p class="formula">A = π × d² ÷ 4 ≈ 0.7854 × d²</p>

A 1.2 m round table has an area of 0.7854 × 1.44 = **1.13 m²**.

## Ring (annulus) area

For a washer, pipe wall or circular path, subtract the inner circle from the outer:

<p class="formula">A = π × (R² − r²)</p>

A path 1 m wide around a 4 m-radius pond covers π × (25 − 16) = **28.27 m²**.
''', [
 ('How many square feet is a 10-foot circle?', 'A 10-foot diameter circle has radius 5 ft, so area = π × 25 ≈ 78.5 sq ft.'),
 ('How do I find the diameter from the area?', 'd = 2 × √(A ÷ π). For an area of 100, the diameter is about 11.28.'),
], before='## Useful values')

# cone
expand('math/cone', f'''
## Cone examples

| Radius | Height | Slant height | Volume | Total surface |
|---|---|---|---|---|
''' + ''.join(f"| {r} | {h} | {math.hypot(r,h):.2f} | {pi*r*r*h/3:.2f} | {pi*r*math.hypot(r,h)+pi*r*r:.2f} |\n" for r, h in [(3, 4), (5, 12), (2, 10), (10, 10), (6, 8)]) + f'''
## Cone vs cylinder

A cone holds exactly **one-third** of a cylinder with the same base and height. Fill a cone with water three times and it fills the cylinder.

## Frustum (cut-off cone)

Buckets, lampshades and many hoppers are frustums — cones with the top sliced off:

<p class="formula">V = π × h ÷ 3 × (R² + R·r + r²)</p>

A bucket 30 cm tall with a 15 cm top radius and 10 cm bottom radius holds π × 30 ÷ 3 × (225 + 150 + 100) = **{pi*30/3*475/1000:.2f} litres**.

## Making a cone from paper

To roll a cone from a flat sheet, cut a sector with:

- **Radius** = the cone's slant height s
- **Angle** = 360° × r ÷ s

For a cone with r = 3 and s = 5, cut a sector of 216° from a circle of radius 5.

## Piles of sand and gravel

A loose pile forms a cone. Measure the base circumference and height, find r = C ÷ 2π, then use the volume formula. Multiply by the material density to get its weight.
''', [
 ('How do I find the height of a cone from the slant height?', 'h = √(s² − r²). With s = 5 and r = 3, h = 4.'),
 ('How many litres does a cone hold?', 'Work out the volume in cm³ and divide by 1,000. The calculator can show the volume in litres directly.'),
], before='## Practical uses')

# cylinder
rows = ''.join(f"| {d} cm | {h} cm | {pi*(d/2)**2*h/1000:.2f} L |\n" for d, h in [(10, 20), (30, 50), (60, 100), (100, 120), (150, 150), (200, 200)])
expand('math/cylinder-volume', f'''
## Tank capacity examples

| Diameter | Height | Capacity |
|---|---|---|
{rows}
## Horizontal tank: partly filled

For a cylinder lying on its side and filled to depth h, the liquid volume is the segment area times the length L:

<p class="formula">V = L × [r² × acos((r − h) ÷ r) − (r − h) × √(2rh − h²)]</p>

A tank of radius 50 cm and length 200 cm filled to 25 cm holds about **{200*(2500*math.acos(25/50)-25*math.sqrt(2*50*25-625))/1000:.0f} L** — less than a quarter of its 1,571 L capacity, because the bottom is narrow.

## Pipe volume

Pipes are long cylinders. For the water in a pipe, use the **inner** diameter:

- 25 mm pipe, 10 m long: π × 0.0125² × 10 = **4.9 L**
- 100 mm pipe, 50 m long: π × 0.05² × 50 = **393 L**

## Surface area for painting or insulation

- **Curved surface only** (open both ends): 2πrh
- **One closed end** (open-top tank): 2πrh + πr²
- **Closed cylinder**: 2πr(r + h)
''', [
 ('How many litres in a cylinder 1 m across and 1 m high?', 'π × 0.5² × 1 = 0.785 m³, which is 785 litres.'),
 ('How do I convert cubic inches to gallons?', 'Divide by 231 for US gallons. The calculator shows US gallons automatically when you choose imperial units.'),
], before='## Unit tips')

# exponent
expand('math/exponent', '''
## Powers of 10 and SI prefixes

| Power | Value | Prefix |
|---|---|---|
| 10<sup>12</sup> | 1,000,000,000,000 | tera (T) |
| 10<sup>9</sup> | 1,000,000,000 | giga (G) |
| 10<sup>6</sup> | 1,000,000 | mega (M) |
| 10<sup>3</sup> | 1,000 | kilo (k) |
| 10<sup>0</sup> | 1 | — |
| 10<sup>−3</sup> | 0.001 | milli (m) |
| 10<sup>−6</sup> | 0.000001 | micro (µ) |
| 10<sup>−9</sup> | 0.000000001 | nano (n) |

## Fractional exponents and roots

A fractional exponent is a root:

- x<sup>1/2</sup> = √x, so 16<sup>0.5</sup> = 4
- x<sup>1/3</sup> = ∛x, so 27<sup>1/3</sup> = 3
- x<sup>3/2</sup> = (√x)³, so 4<sup>1.5</sup> = 8

Type 0.5 or 0.3333333 as the exponent to take square or cube roots.

## Scientific notation

Very large and small numbers are written as a × 10<sup>n</sup>, with 1 ≤ a < 10:

- Speed of light ≈ 3 × 10<sup>8</sup> m/s
- Mass of an electron ≈ 9.11 × 10<sup>−31</sup> kg
- World population ≈ 8 × 10<sup>9</sup>

## Common mistakes

- **−2² is −4**, not 4: the exponent applies before the minus sign. Write (−2)² for 4.
- **(a + b)² is not a² + b²**. It is a² + 2ab + b².
- **x<sup>0</sup> = 1** for any non-zero x.
''', [
 ('What is 2 to the power of 10?', '1,024.'),
 ('How do I find the exponent if I know the result?', 'Use logarithms: n = log(y) ÷ log(x). In the calculator, press × on Exponent and enter the result.'),
], before='## Growth')

# fraction to decimal
rows = ''.join(f"| {a}/{b} | {a/b:.6g} | {a/b*100:.4g}% |\n" for a, b in [(1, 3), (2, 3), (1, 6), (5, 6), (1, 7), (1, 9), (1, 12), (7, 16), (11, 16), (3, 32)])
expand('math/fraction-to-decimal', f'''
## More fraction conversions

| Fraction | Decimal | Percent |
|---|---|---|
{rows}
## Decimal back to fraction

1. Write the decimal over 1, e.g. 0.375 ÷ 1.
2. Multiply top and bottom by 10 for each decimal place: 375 ÷ 1000.
3. Simplify by the greatest common factor (125): **3/8**.

## Repeating decimals to fractions

For a repeating decimal like 0.272727…:

- Let x = 0.2727…
- 100x = 27.2727…
- Subtract: 99x = 27, so x = 27/99 = **3/11**

## Mixed numbers

Convert 2 3/4 by dividing the fraction part and adding the whole number: 3 ÷ 4 = 0.75, so 2 3/4 = **2.75**. In the calculator, enter 11 as the numerator and 4 as the denominator (2 × 4 + 3 = 11).

## Terminating or repeating?

A simplified fraction gives a terminating decimal only if its denominator has no prime factors other than 2 and 5. So 3/8 and 7/20 terminate, while 1/3, 1/7 and 5/12 repeat.
''', [
 ('What is 5/8 as a decimal?', '0.625, or 62.5%.'),
 ('What is 1/3 as a percentage?', '33.33…%, usually rounded to 33.3%.'),
], before='## Inch fractions')

# logarithm
expand('math/logarithm', '''
## Common log values

| x | log₁₀ x | ln x | log₂ x |
|---|---|---|---|
''' + ''.join(f"| {x} | {math.log10(x):.4f} | {math.log(x):.4f} | {math.log2(x):.4f} |\n" for x in [0.5, 1, 2, 3, 5, 10, 100, 1000]) + '''
## Change of base

Any logarithm can be found with natural logs (or base-10 logs):

<p class="formula">log<sub>b</sub>(x) = ln(x) ÷ ln(b)</p>

This is exactly what the calculator does.

## Solving exponential equations

Logs undo exponents. To solve 3<sup>x</sup> = 50, take the log of both sides: x = ln 50 ÷ ln 3 = **3.561**. In the calculator, set the base to 3 and the number to 50.

## Log scales in real life

| Scale | What it measures | One step means |
|---|---|---|
| pH | Acidity | 10× change in hydrogen ion concentration |
| Decibels (dB) | Sound level | +10 dB = 10× the intensity |
| Richter / moment magnitude | Earthquakes | +1 = about 32× the energy |
| Octaves in music | Pitch | 2× the frequency |

## Common mistakes

- log(a + b) is **not** log a + log b. The rule is log(a × b) = log a + log b.
- Logs of zero and negative numbers are undefined for real numbers.
- “log” means base 10 on most calculators but base e in many programming languages.
''', [
 ('What is log base 2 of 1024?', '10, because 2¹⁰ = 1,024.'),
 ('What is the natural log of e?', '1, because e¹ = e.'),
], before='## Where logs are used')

# percent error
expand('math/percent-error', '''
## Percent error examples

| Measured | True | Percent error |
|---|---|---|
''' + ''.join(f"| {m} | {t} | {abs(m-t)/abs(t)*100:.2f}% |\n" for m, t in [(9.6, 9.81), (2.48, 2.50), (101, 100), (0.95, 1.0), (343, 340), (1.05, 1.0)]) + '''
## Absolute, relative and percent error

| Error type | Formula | Units |
|---|---|---|
| Absolute error | measured − true | Same as the measurement |
| Relative error | abs(measured − true) ÷ abs(true) | None (a ratio) |
| Percent error | relative error × 100 | % |

## Sources of error in experiments

- **Random errors**: small unpredictable variations, reduced by repeating and averaging.
- **Systematic errors**: consistent bias, such as an uncalibrated scale or reaction time. Repeating does not remove them.
- **Human errors**: misreading a scale or recording a value wrongly.

Discuss which type is likely when you write up a lab report.

## When the true value is zero

Percent error is undefined when the accepted value is zero, because you would divide by zero. Report the absolute error instead.
''', [
 ('Is 5% error good in a lab?', 'For most school and undergraduate experiments, under 5% is considered good and under 10% acceptable, depending on the equipment.'),
 ('What is the difference between accuracy and precision?', 'Accuracy is how close results are to the true value. Precision is how close repeated results are to each other. You can be precise but inaccurate if there is a systematic error.'),
], before='## Accuracy specs in instrumentation')

# percentage change
expand('math/percentage-change', '''
## Percentage change examples

| From | To | Change |
|---|---|---|
''' + ''.join(f"| {a} | {b} | {(b-a)/a*100:+.1f}% |\n" for a, b in [(50, 75), (75, 50), (100, 250), (200, 150), (1200, 1380), (40, 10)]) + '''
## Percentage difference (no “original” value)

When neither value is the starting point — comparing two shops' prices, say — use percentage difference, which divides by the average:

<p class="formula">% difference = |a − b| ÷ ((a + b) ÷ 2) × 100</p>

For 80 and 92 that is 12 ÷ 86 × 100 = **13.95%**.

## Reversing a percentage change

To undo a change, you need a different percentage:

| Change | To get back you need |
|---|---|
| +10% | −9.09% |
| +25% | −20% |
| +50% | −33.3% |
| −20% | +25% |
| −50% | +100% |

This is why a stock that falls 50% must double to recover.
''', [
 ('How do I calculate a percentage increase?', '(new − old) ÷ old × 100. From 80 to 92: 12 ÷ 80 × 100 = 15%.'),
 ('How do I find the original value before a percentage increase?', 'Divide the new value by (1 + change). After a 15% rise to 92, the original was 92 ÷ 1.15 = 80.'),
], before='## Over several years')

# percentage
expand('math/percentage', '''
## Three types of percentage question

| Question | Formula | Example |
|---|---|---|
| What is P% of X? | X × P ÷ 100 | 15% of 240 = 36 |
| Y is what % of X? | Y ÷ X × 100 | 36 is 15% of 240 |
| Y is P% of what? | Y ÷ P × 100 | 36 is 15% of 240 |

The calculator handles all three — fill in any two fields.

## Percentage table

| % | of 50 | of 200 | of 750 | of 1,500 |
|---|---|---|---|---|
''' + ''.join(f"| {p}% | {50*p/100:g} | {200*p/100:g} | {750*p/100:g} | {1500*p/100:g} |\n" for p in [1, 5, 10, 12.5, 15, 20, 25, 33, 50, 75]) + '''
## Percentages in everyday life

- **Shopping**: discounts — see the [discount calculator](/finance/discount/).
- **Tax**: GST, VAT or sales tax — see the [sales tax calculator](/finance/sales-tax-vat/).
- **Marks**: 68 out of 80 is 85%.
- **Tips**: 15% of a restaurant bill — see the [tip calculator](/everyday-life/tip-calculator/).

## Percent vs percentage points

If an interest rate rises from 5% to 6%, it went up by **1 percentage point** but by **20 percent**. News reports often mix these up.
''', [
 ('What is 20% of 500?', '100.'),
 ('How do I calculate marks percentage?', 'Divide marks obtained by total marks and multiply by 100. 425 out of 500 is 85%.'),
], before='## Common mistakes')

# pythagorean
expand('math/pythagorean-theorem', '''
## Distance between two points

The distance formula is the Pythagorean theorem on a grid:

<p class="formula">d = √((x₂ − x₁)² + (y₂ − y₁)²)</p>

From (1, 2) to (7, 10): √(36 + 64) = **10**. In 3D, add a third term: √(Δx² + Δy² + Δz²).

## Is the triangle right-angled?

Check whether a² + b² equals c² (with c the longest side):

| Sides | a² + b² | c² | Result |
|---|---|---|---|
| 5, 12, 13 | 169 | 169 | Right angle |
| 6, 7, 9 | 85 | 81 | Acute (a² + b² > c²) |
| 4, 5, 7 | 41 | 49 | Obtuse (a² + b² < c²) |

## The 3-4-5 rule on site

Builders mark a right angle by measuring 3 units along one line, 4 along the other and checking that the diagonal is exactly 5. Multiples work too: 6-8-10 or 9-12-15 for larger layouts.

## Screen and ladder examples

- A TV 1.2 m wide and 0.68 m tall has a diagonal of √(1.44 + 0.46) = **1.38 m** (about 54 inches).
- A 5 m ladder with its foot 1.5 m from a wall reaches √(25 − 2.25) = **4.77 m** up the wall.
''', [
 ('Does the Pythagorean theorem work for all triangles?', 'No, only right-angled triangles. For other triangles use the law of cosines: c² = a² + b² − 2ab cos C.'),
 ('How do I find the hypotenuse of a 45-45-90 triangle?', 'Multiply a leg by √2 (about 1.414). Legs of 10 give a hypotenuse of 14.14.'),
], before='## Practical uses')

# quadratic
expand('math/quadratic-equation', '''
## Other ways to solve a quadratic

| Method | Best when |
|---|---|
| Factoring | Roots are whole numbers or simple fractions |
| Completing the square | Deriving the vertex form or the formula itself |
| Quadratic formula | Always works |
| Graphing | Seeing roughly where the roots are |

Example by factoring: 2x² − 7x + 3 = (2x − 1)(x − 3), so x = 0.5 or x = 3 — the same as the calculator.

## Vertex of the parabola

The turning point of y = ax² + bx + c is at:

<p class="formula">x = −b ÷ (2a), &nbsp; y = c − b² ÷ (4a)</p>

For 2x² − 7x + 3, the vertex is at x = 1.75, y = −3.125. The parabola opens upward when a > 0 and downward when a < 0.

## Real-world quadratics

- **Projectile motion**: height h = −4.9t² + vt + h₀ (metres, seconds). Set h = 0 to find when it lands.
- **Area problems**: a rectangle with perimeter 20 and area 21 gives x² − 10x + 21 = 0, so the sides are 3 and 7.
- **Profit**: revenue minus cost often forms a quadratic; the vertex gives the maximum profit.

## Complex roots

When the discriminant is negative, the roots are complex: x = −b ÷ 2a ± i√(−D) ÷ 2a. For x² + 2x + 5 = 0, the roots are −1 ± 2i.
''', [
 ('How do I find the roots of x² − 5x + 6 = 0?', 'a = 1, b = −5, c = 6. The discriminant is 1, so x = (5 ± 1) ÷ 2, giving 3 and 2.'),
 ('What is the vertex form of a quadratic?', 'y = a(x − h)² + k, where (h, k) is the vertex. It comes from completing the square.'),
], before='## Sum and product of roots')

# ratio
expand('math/ratio', '''
## Scaling recipes and mixtures

Ratios keep proportions the same when you scale up or down:

| Mix | Ratio | For 10 litres |
|---|---|---|
| Concrete (cement : sand : gravel) | 1 : 2 : 3 | 1.67 : 3.33 : 5 |
| 2-stroke fuel (oil : petrol) | 1 : 50 | 0.2 L oil in 10 L petrol |
| Squash or cordial (concentrate : water) | 1 : 4 | 2 : 8 |
| Paint thinning | 1 : 10 | 0.91 : 9.09 |

To split a total in a ratio, divide by the sum of the parts and multiply by each part.

## Splitting money in a ratio

Sharing 12,000 in the ratio 2 : 3 : 5: the parts sum to 10, so each part is 1,200. The shares are **2,400**, **3,600** and **6,000**.

## Map and model scales

A map at 1 : 50,000 means 1 cm on the map is 50,000 cm (500 m) on the ground. A 7 cm route is 3.5 km. Use A = 1, B = 50,000 and C = your map distance.

## Aspect ratios

Screens and photos use ratios of width to height: 16 : 9 for TVs, 4 : 3 for older screens, 3 : 2 for many cameras. A 16 : 9 image 1,920 pixels wide is 1,080 pixels tall.
''', [
 ('How do I divide 500 in the ratio 3 : 2?', 'Total parts = 5, so one part is 100. The shares are 300 and 200.'),
 ('How do I find a missing number in a proportion?', 'Cross-multiply: if a ÷ b = c ÷ d, then d = b × c ÷ a.'),
], before='## Direct vs inverse proportion')

# rectangle
expand('math/rectangle', '''
## Rectangle examples

| Length | Width | Area | Perimeter | Diagonal |
|---|---|---|---|---|
''' + ''.join(f"| {l} | {w} | {l*w:g} | {2*(l+w):g} | {math.hypot(l,w):.2f} |\n" for l, w in [(3, 2), (4, 4), (8, 5), (10, 6), (12, 9), (20, 15)]) + '''
## Same perimeter, different area

With 40 m of fencing:

| Shape | Area enclosed |
|---|---|
| 15 × 5 | 75 m² |
| 12 × 8 | 96 m² |
| 10 × 10 (square) | 100 m² |

A square gives the most area for a given perimeter.

## Area of an L-shaped room

Split the shape into two rectangles, find each area and add them. A room 6 × 4 m with a 2 × 3 m alcove has an area of 24 + 6 = **30 m²**.

## Rooms with sloped or irregular walls

For a room that is not quite rectangular, measure the length at both ends and the width at both ends, average each pair, then multiply. For larger irregular areas, break them into rectangles and triangles. See the [triangle area calculator](/math/triangle-area/).
''', [
 ('How many square feet is a 12 × 15 room?', '12 × 15 = 180 square feet.'),
 ('How do I convert square metres to square feet?', 'Multiply by 10.764. Or switch the area unit in the calculator.'),
], before='## Unit reminders')

# right triangle trig
expand('math/right-triangle-trig', '''
## Trig values table

| Angle | sin | cos | tan |
|---|---|---|---|
''' + ''.join(f"| {a}° | {math.sin(math.radians(a)):.4f} | {math.cos(math.radians(a)):.4f} | {math.tan(math.radians(a)):.4f} |\n" for a in [0, 10, 15, 20, 30, 40, 45, 50, 60, 70, 75, 80]) + '''
## Finding angles from sides

Use the inverse functions:

- A = asin(a ÷ c) — from opposite and hypotenuse
- A = acos(b ÷ c) — from adjacent and hypotenuse
- A = atan(a ÷ b) — from opposite and adjacent

In the calculator, fill in two sides and press × on the angle.

## Height of a building or tree

Stand a known distance away and measure the angle up to the top. Height = distance × tan(angle), plus your eye height. At 20 m away with a 35° angle and eyes 1.6 m above the ground: 20 × 0.7002 + 1.6 = **15.6 m**.

## Ramps and roofs

- A wheelchair ramp at 1 : 12 has an angle of atan(1/12) = **4.76°**.
- A roof with a 6/12 pitch rises 6 for every 12 across — an angle of **26.57°**. See the [roof pitch calculator](/construction/roof-pitch/).
''', [
 ('What is sin 30°?', '0.5 exactly.'),
 ('Should my calculator be in degrees or radians?', 'For everyday triangles, degrees. The angle unit selector lets you switch.'),
], before='## Special angles')

# slope
expand('math/slope', '''
## Slope, grade and angle

| Slope (m) | Grade | Angle |
|---|---|---|
''' + ''.join(f"| {m:g} | {m*100:g}% | {math.degrees(math.atan(m)):.2f}° |\n" for m in [0.02, 0.05, 0.0833, 0.1, 0.25, 0.5, 1, 2]) + '''
A slope of 1 (100% grade) is 45°, not vertical. A vertical line has an undefined slope.

## Parallel and perpendicular lines

- **Parallel** lines have equal slopes.
- **Perpendicular** lines have slopes that multiply to −1. A line with slope 2 is perpendicular to one with slope −1/2.

## Midpoint

The midpoint between (x₁, y₁) and (x₂, y₂) is ((x₁ + x₂) ÷ 2, (y₁ + y₂) ÷ 2). For (1, 2) and (4, 6) it is (2.5, 4).

## Slope in real life

- **Roads**: steep hills are often 10–15% grade.
- **Drainage pipes**: typically 1–2% fall so water flows.
- **Wheelchair ramps**: maximum 1 : 12 (8.33%) in many building codes.
- **Graphs**: slope shows a rate of change, such as speed on a distance-time graph.
''', [
 ('What does a slope of 0 mean?', 'The line is horizontal — y does not change as x changes.'),
 ('How do I find the y-intercept?', 'b = y₁ − m × x₁. For slope 4/3 through (1, 2), b = 2 − 4/3 = 2/3.'),
], before='## Slope as grade and angle')

# sphere
expand('math/sphere', '''
## Sphere examples

| Object (approx.) | Diameter | Volume | Surface area |
|---|---|---|---|
''' + ''.join(f"| {n} | {d} cm | {4/3*pi*(d/2)**3:,.1f} cm³ | {4*pi*(d/2)**2:,.1f} cm² |\n" for n, d in [('Table-tennis ball', 4.0), ('Golf ball', 4.27), ('Tennis ball', 6.7), ('Cricket ball', 7.2), ('Football (size 5)', 22.0), ('Basketball (size 7)', 24.3)]) + '''
## Finding the radius

- From volume: r = ∛(3V ÷ 4π)
- From surface area: r = √(S ÷ 4π)
- From circumference: r = C ÷ 2π

## Spherical cap

The part of a sphere cut off by a plane, such as liquid in a round flask:

<p class="formula">V = π × h² × (3r − h) ÷ 3</p>

## Why bubbles and drops are round

A sphere has the smallest surface area for a given volume. Surface tension pulls liquids and soap films into that shape, and many tanks are spherical to use the least material for the most storage.
''', [
 ('What is the volume of a sphere with radius 1?', '4/3 × π ≈ 4.19 cubic units.'),
 ('How many litres is a 30 cm diameter sphere?', 'Radius 15 cm, so volume = 4/3 × π × 3,375 = 14,137 cm³ ≈ 14.1 litres.'),
], before='## Hemisphere')

# trapezoid
expand('math/trapezoid-area', '''
## Trapezoid examples

| Side a | Side b | Height | Area |
|---|---|---|---|
''' + ''.join(f"| {a} | {b} | {h} | {(a+b)/2*h:g} |\n" for a, b, h in [(4, 6, 3), (5, 9, 4), (6, 10, 4), (8, 12, 5), (10, 20, 6)]) + '''
## Perimeter

The perimeter is a + b + the two slanted sides. For an isosceles trapezoid, each slanted side is √(h² + ((b − a) ÷ 2)²).

## Irregular plots of land

Many plots are close to a trapezoid. Measure the two parallel boundaries and the distance between them. For less regular shapes, divide the land into several trapezoids and add them up — surveyors call this the **trapezoidal rule**.

## The trapezoidal rule in maths

To estimate the area under a curve, split it into thin strips and treat each as a trapezoid:

<p class="formula">Area ≈ Δx ÷ 2 × (y₀ + 2y₁ + 2y₂ + … + yₙ)</p>

This is how many calculators and spreadsheets estimate integrals and how engineers measure volumes from cross-sections.
''', [
 ('How do I find the height of a trapezoid from its area?', 'h = 2A ÷ (a + b). For an area of 32 with parallel sides 6 and 10, h = 4.'),
 ('What is the area of a trapezoid with sides 5 and 7 and height 4?', '(5 + 7) ÷ 2 × 4 = 24.'),
], before='## Check with a rectangle')

# triangle
expand('math/triangle-area', '''
## Heron's formula: area from three sides

When you know all three sides but not the height:

<p class="formula">s = (a + b + c) ÷ 2, &nbsp; Area = √(s(s − a)(s − b)(s − c))</p>

For sides 7, 8 and 9: s = 12, Area = √(12 × 5 × 4 × 3) = √720 = **26.83**.

## Area from two sides and an angle

<p class="formula">Area = ½ × a × b × sin C</p>

Sides of 10 and 12 with a 40° angle between them: ½ × 10 × 12 × 0.6428 = **38.57**.

## Equilateral triangle

All sides equal to s: Area = √3 ÷ 4 × s² ≈ 0.433 × s². A 10 cm equilateral triangle has an area of **43.3 cm²**.

## Area from coordinates

For points (x₁, y₁), (x₂, y₂), (x₃, y₃):

<p class="formula">Area = |x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)| ÷ 2</p>

For (0, 0), (4, 0) and (0, 3), the area is 6.
''', [
 ('What is the area of a triangle with base 10 and height 6?', '10 × 6 ÷ 2 = 30.'),
 ('Can I find the area with only the three sides?', "Yes, using Heron's formula shown above."),
], before='## Right triangles')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/math/*.mdx')):
    c = 'math/' + os.path.basename(p)[:-4]; print(c, words(c))
