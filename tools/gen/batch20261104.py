import sys, math, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
D = '2026-11-04'
R = 8.314462618          # gas constant, J/(mol·K)
def Phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
def deg(x): return x * 180 / math.pi
def rad(x): return x * math.pi / 180

# ================================================================ MATH

# ---------------------------------------------------------------- Distance & midpoint
dm = (1, 2, 7, 10)
def dist(x1, y1, x2, y2): return math.hypot(x2 - x1, y2 - y1)
dm_d = dist(*dm)
dm_pairs = [((0, 0), (3, 4)), ((1, 2), (7, 10)), ((-3, 5), (4, -2)), ((2, -1), (-6, 3)), ((0, 0), (5, 12)), ((-4, -4), (4, 4)), ((1.5, 2.5), (4, 8))]
dm_rows = ''.join(f"| ({a[0]:g}, {a[1]:g}) | ({b[0]:g}, {b[1]:g}) | {dist(a[0], a[1], b[0], b[1]):.4g} | ({(a[0]+b[0])/2:g}, {(a[1]+b[1])/2:g}) | {((b[1]-a[1])/(b[0]-a[0])):.4g} |\n" for a, b in dm_pairs)
page('math', 'distance-midpoint', f'''
title: Distance & Midpoint Calculator (Two Points)
description: Calculate the distance between two points, the midpoint and the slope of the line joining them from (x₁, y₁) and (x₂, y₂), with the formula and steps.
category: math
{intro("The distance between two points on a graph comes from the Pythagorean theorem, and the midpoint is simply the average of their coordinates. This distance and midpoint calculator takes two points (x₁, y₁) and (x₂, y₂) and returns the straight-line distance, the midpoint and the slope of the line through them.")}
keywords: [distance calculator, midpoint calculator, distance between two points calculator, distance formula, midpoint formula, distance and midpoint calculator, coordinate geometry]
updated: {D}
variables:
  - {{ id: x1, label: Point 1 — x₁, default: {dm[0]} }}
  - {{ id: y1, label: Point 1 — y₁, default: {dm[1]} }}
  - {{ id: x2, label: Point 2 — x₂, default: {dm[2]} }}
  - {{ id: y2, label: Point 2 — y₂, default: {dm[3]} }}
  - {{ id: d, label: Distance between the points, min: 0 }}
  - {{ id: xm, label: Midpoint — x }}
  - {{ id: ym, label: Midpoint — y }}
  - {{ id: m, label: Slope of the line (Δy ÷ Δx) }}
equations:
  - d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
  - xm = (x1 + x2) / 2
  - ym = (y1 + y2) / 2
  - m = (y2 - y1) / (x2 - x1)
faq:
  - q: What is the distance formula?
    a: d = √((x₂ − x₁)² + (y₂ − y₁)²). It is the Pythagorean theorem applied to the horizontal and vertical differences between the two points.
  - q: What is the midpoint formula?
    a: The midpoint is ((x₁ + x₂) ÷ 2, (y₁ + y₂) ÷ 2) — the average of the x-coordinates and the average of the y-coordinates.
  - q: How do I find a missing endpoint from the midpoint?
    a: Rearrange the midpoint formula — x₂ = 2xₘ − x₁ and y₂ = 2yₘ − y₁. In this calculator, clear x₂ and y₂ and enter the midpoint instead.
  - q: How do I find the distance between two points in 3D?
    a: Add the z term — d = √(Δx² + Δy² + Δz²). The vector calculator gives the magnitude of a 3D difference vector directly.
related: [math/slope, math/pythagorean-theorem, math/vector, math/linear-interpolation]
''', f'''
## How to use the distance and midpoint calculator

Enter the coordinates of the two points. The calculator returns the straight-line (Euclidean) distance between them, the midpoint, and the slope of the line joining them. Any of the inputs can be solved for instead — for example, clear y₂ and enter a distance to find where the second point must lie.

## Distance and midpoint formulas

<p class="formula">d = √((x₂ − x₁)² + (y₂ − y₁)²) &nbsp;·&nbsp; M = ((x₁ + x₂) ÷ 2, (y₁ + y₂) ÷ 2) &nbsp;·&nbsp; m = (y₂ − y₁) ÷ (x₂ − x₁)</p>

## Example

Points (1, 2) and (7, 10):

- Δx = 7 − 1 = 6, Δy = 10 − 2 = 8
- Distance = √(6² + 8²) = √100 = **{dm_d:g}**
- Midpoint = ((1 + 7) ÷ 2, (2 + 10) ÷ 2) = **(4, 6)**
- Slope = 8 ÷ 6 = **{8/6:.4f}**

## Worked distances and midpoints

| Point 1 | Point 2 | Distance | Midpoint | Slope |
|---|---|---|---|---|
{dm_rows}
## Notes

- Distance is always positive and does not depend on which point you call "1".
- A vertical line (x₁ = x₂) has an undefined slope; the distance and midpoint are still valid.
- For the full equation of the line, use the [slope calculator](/math/slope/).
''')

# ---------------------------------------------------------------- Law of sines
ls_a, ls_A, ls_B = 10.0, 30.0, 45.0
ls_C = 180 - ls_A - ls_B
ls_b = ls_a * math.sin(rad(ls_B)) / math.sin(rad(ls_A))
ls_c = ls_a * math.sin(rad(ls_C)) / math.sin(rad(ls_A))
ls_area = 0.5 * ls_a * ls_b * math.sin(rad(ls_C))
ls_rows = ''
for B in (15, 30, 45, 60, 75, 90, 105, 120):
    C = 180 - ls_A - B
    b = ls_a * math.sin(rad(B)) / math.sin(rad(ls_A)); c = ls_a * math.sin(rad(C)) / math.sin(rad(ls_A))
    ls_rows += f"| {B}° | {C:g}° | {b:.3f} | {c:.3f} | {0.5*ls_a*b*math.sin(rad(C)):.2f} |\n"
page('math', 'law-of-sines', f'''
title: Law of Sines Calculator (Solve a Triangle, AAS & ASA)
description: Solve any triangle with the law of sines — enter one side and two angles to get the third angle, the missing sides and the area, with the formula and steps.
category: math
{intro("The law of sines says that each side of a triangle divided by the sine of its opposite angle gives the same ratio. This law of sines calculator uses that rule to solve a triangle from one side and two angles (AAS or ASA), returning the third angle, both missing sides and the area.")}
keywords: [law of sines calculator, sine rule calculator, solve triangle calculator, law of sines formula, aas triangle, asa triangle, missing side of a triangle]
updated: {D}
variables:
  - {{ id: a, label: Side a, default: {ls_a:g}, min: 0 }}
  - {{ id: A, label: Angle A (opposite side a), family: angle, unit: deg, default: {ls_A:g}, min: 0, max: 3.14159265 }}
  - {{ id: B, label: Angle B (opposite side b), family: angle, unit: deg, default: {ls_B:g}, min: 0, max: 3.14159265 }}
  - {{ id: C, label: Angle C, family: angle, unit: deg, min: 0, max: 3.14159265 }}
  - {{ id: b, label: Side b, min: 0 }}
  - {{ id: c, label: Side c, min: 0 }}
  - {{ id: K, label: Area of the triangle, min: 0 }}
equations:
  - C = pi - A - B
  - b = a * sin(B) / sin(A)
  - c = a * sin(C) / sin(A)
  - K = 0.5 * a * b * sin(C)
faq:
  - q: What is the law of sines?
    a: a ÷ sin A = b ÷ sin B = c ÷ sin C. In any triangle, the ratio of a side to the sine of the angle opposite it is the same for all three sides (and equals the diameter of the circumscribed circle).
  - q: When should I use the law of sines instead of the law of cosines?
    a: Use the law of sines when you know two angles and a side (AAS, ASA) or two sides and a non-included angle (SSA). Use the law of cosines when you know three sides (SSS) or two sides and the included angle (SAS).
  - q: What is the ambiguous case of the law of sines?
    a: With two sides and a non-included angle (SSA) there can be two different triangles, because sin B = sin(180° − B). Check whether 180° − B also leaves a positive third angle; if it does, both triangles are valid.
  - q: Do the sides need units?
    a: Any length unit works — the missing sides come out in the same unit you used for side a, and the area in that unit squared.
related: [math/law-of-cosines, math/right-triangle-trig, math/triangle-area, math/pythagorean-theorem]
''', f'''
## How to use the law of sines calculator

Enter one **side a** and the two angles **A** (opposite a) and **B**. The calculator finds the third angle C = 180° − A − B, then sides b and c from the law of sines, and the area. For the SSA case, clear angle B and enter side b instead — the calculator solves sin B and returns the acute solution (see the ambiguous case below).

## Law of sines formula

<p class="formula">a ÷ sin A = b ÷ sin B = c ÷ sin C &nbsp;·&nbsp; Area = ½ a b sin C</p>

## Example

Side a = 10, angle A = 30°, angle B = 45°:

- C = 180° − 30° − 45° = **{ls_C:g}°**
- b = 10 × sin 45° ÷ sin 30° = 10 × 0.7071 ÷ 0.5 = **{ls_b:.3f}**
- c = 10 × sin 105° ÷ sin 30° = 10 × 0.9659 ÷ 0.5 = **{ls_c:.3f}**
- Area = ½ × 10 × {ls_b:.3f} × sin 105° = **{ls_area:.2f}**

## Same triangle, different angle B (a = 10, A = 30°)

| Angle B | Angle C | Side b | Side c | Area |
|---|---|---|---|---|
{ls_rows}
## The ambiguous case (SSA)

When you know a, b and A, sin B = b sin A ÷ a. If that value is above 1 there is no triangle; if it equals 1 there is one right triangle; if it is below 1, B can be acute or 180° minus that angle, and both give a valid triangle whenever A + B stays below 180°. For three known sides use the [law of cosines calculator](/math/law-of-cosines/).
''')

# ---------------------------------------------------------------- Arithmetic sequence
as_a1, as_d, as_n = 3, 4, 10
as_an = as_a1 + (as_n - 1) * as_d
as_S = as_n * (as_a1 + as_an) / 2
as_rows = ''.join(f"| {k} | {as_a1+(k-1)*as_d} | {k*(2*as_a1+(k-1)*as_d)//2} |\n" for k in range(1, 13))
page('math', 'arithmetic-sequence', f'''
title: Arithmetic Sequence Calculator (nth Term & Sum)
description: Find the nth term and the sum of the first n terms of an arithmetic sequence from the first term and common difference, or solve for any missing value.
category: math
{intro("An arithmetic sequence adds the same common difference d to get from one term to the next — 3, 7, 11, 15 and so on. This arithmetic sequence calculator finds the nth term and the sum of the first n terms, and can solve backwards for the first term, the difference or the number of terms.")}
keywords: [arithmetic sequence calculator, arithmetic series calculator, nth term calculator, sum of arithmetic sequence, arithmetic progression calculator, common difference, ap formula]
updated: {D}
variables:
  - {{ id: a1, label: First term (a₁), default: {as_a1} }}
  - {{ id: d, label: Common difference (d), default: {as_d} }}
  - {{ id: n, label: Term number (n), default: {as_n}, min: 1 }}
  - {{ id: an, label: nth term (aₙ) }}
  - {{ id: S, label: Sum of the first n terms (Sₙ) }}
equations:
  - an = a1 + (n - 1) * d
  - S = n * (a1 + an) / 2
faq:
  - q: What is the formula for the nth term of an arithmetic sequence?
    a: aₙ = a₁ + (n − 1)d, where a₁ is the first term and d the common difference.
  - q: How do I find the sum of an arithmetic series?
    a: Sₙ = n(a₁ + aₙ) ÷ 2 — the number of terms times the average of the first and last term. Equivalently Sₙ = n[2a₁ + (n − 1)d] ÷ 2.
  - q: How do I find the common difference?
    a: Subtract any term from the next one — d = a₂ − a₁. From two known terms, d = (aₙ − aₘ) ÷ (n − m).
  - q: What is the sum of the numbers 1 to 100?
    a: 5,050 — with a₁ = 1, d = 1 and n = 100, Sₙ = 100 × (1 + 100) ÷ 2.
related: [math/geometric-sequence, math/average, math/exponent, math/quadratic-equation]
''', f'''
## How to use the arithmetic sequence calculator

Enter the **first term**, the **common difference** and the **term number n**. The calculator returns the nth term and the sum of the first n terms. To work backwards, clear any field and fill in the nth term or the sum — for example, find which term of a sequence equals a given value.

## Arithmetic sequence formulas

<p class="formula">aₙ = a₁ + (n − 1) d &nbsp;·&nbsp; Sₙ = n (a₁ + aₙ) ÷ 2</p>

## Example

First term 3, common difference 4, n = 10:

- a₁₀ = 3 + (10 − 1) × 4 = **{as_an}**
- S₁₀ = 10 × (3 + {as_an}) ÷ 2 = **{as_S:g}**

## Terms and running sums (a₁ = 3, d = 4)

| n | aₙ | Sₙ |
|---|---|---|
{as_rows}
## Notes

- A negative common difference gives a decreasing sequence.
- The terms of an arithmetic sequence grow linearly; for terms that grow by a constant *ratio*, use the [geometric sequence calculator](/math/geometric-sequence/).
''')

# ---------------------------------------------------------------- Geometric sequence
gs_a1, gs_r, gs_n = 2, 3, 6
gs_an = gs_a1 * gs_r ** (gs_n - 1)
gs_S = gs_a1 * (1 - gs_r ** gs_n) / (1 - gs_r)
gs_rows = ''.join(f"| {k} | {gs_a1*gs_r**(k-1):,} | {gs_a1*(gs_r**k-1)//(gs_r-1):,} | {0.5**(k-1):g} | {2*(1-0.5**k):.6g} |\n" for k in range(1, 11))
page('math', 'geometric-sequence', f'''
title: Geometric Sequence Calculator (nth Term & Series Sum)
description: Find the nth term and the sum of a geometric sequence or series from the first term and common ratio, with the infinite-series sum for ratios between −1 and 1.
category: math
{intro("A geometric sequence multiplies each term by the same common ratio r — 2, 6, 18, 54 and so on. This geometric sequence calculator returns the nth term and the sum of the first n terms (the geometric series), and solves backwards for the first term, the ratio or the number of terms.")}
keywords: [geometric sequence calculator, geometric series calculator, sum of geometric series, nth term geometric sequence, common ratio calculator, geometric progression calculator, infinite geometric series]
updated: {D}
variables:
  - {{ id: a1, label: First term (a₁), default: {gs_a1} }}
  - {{ id: r, label: Common ratio (r), default: {gs_r}, help: 'Any value except 1. For r = 1 every term equals a₁ and Sₙ = n × a₁.' }}
  - {{ id: n, label: Term number (n), default: {gs_n}, min: 1 }}
  - {{ id: an, label: nth term (aₙ) }}
  - {{ id: S, label: Sum of the first n terms (Sₙ) }}
equations:
  - an = a1 * r^(n - 1)
  - S = a1 * (1 - r^n) / (1 - r)
faq:
  - q: What is the formula for the nth term of a geometric sequence?
    a: aₙ = a₁ × rⁿ⁻¹, where a₁ is the first term and r the common ratio.
  - q: How do I find the sum of a geometric series?
    a: Sₙ = a₁(1 − rⁿ) ÷ (1 − r) for r ≠ 1. For r = 1 the sum is simply n × a₁.
  - q: When does an infinite geometric series converge?
    a: Only when −1 < r < 1. The sum is then S∞ = a₁ ÷ (1 − r) — for example 1 + ½ + ¼ + … = 1 ÷ (1 − 0.5) = 2.
  - q: How do I find the common ratio?
    a: Divide any term by the one before it — r = a₂ ÷ a₁. From two terms n − m places apart, r = (aₙ ÷ aₘ)^(1/(n − m)).
related: [math/arithmetic-sequence, math/exponent, math/logarithm, finance/compound-interest]
''', f'''
## How to use the geometric sequence calculator

Enter the **first term**, the **common ratio** and the **term number n**. The calculator returns the nth term and the sum of the first n terms. Clear a field to solve for it instead — for example, enter the nth term to find the ratio, or a target sum to find how many terms are needed.

## Geometric sequence formulas

<p class="formula">aₙ = a₁ rⁿ⁻¹ &nbsp;·&nbsp; Sₙ = a₁ (1 − rⁿ) ÷ (1 − r) &nbsp;·&nbsp; S∞ = a₁ ÷ (1 − r) for |r| &lt; 1</p>

## Example

First term 2, common ratio 3, n = 6:

- a₆ = 2 × 3⁵ = 2 × 243 = **{gs_an:g}**
- S₆ = 2 × (1 − 3⁶) ÷ (1 − 3) = 2 × (−728) ÷ (−2) = **{gs_S:g}**

## Terms and partial sums

| n | aₙ (a₁ = 2, r = 3) | Sₙ (a₁ = 2, r = 3) | aₙ (a₁ = 1, r = 0.5) | Sₙ (a₁ = 1, r = 0.5) |
|---|---|---|---|---|
{gs_rows}
The second pair of columns shows a converging series: the partial sums approach S∞ = 1 ÷ (1 − 0.5) = 2.

## Notes

- A negative ratio makes the terms alternate in sign.
- Compound interest is a geometric sequence with r = 1 + the interest rate per period — see the [compound interest calculator](/finance/compound-interest/).
''')

# ---------------------------------------------------------------- Vector
va, vb = (3, -2, 1), (1, 4, 2)
def mag(v): return math.sqrt(sum(x * x for x in v))
def dot(u, v): return sum(x * y for x, y in zip(u, v))
def cross(u, v): return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
v_ma, v_mb, v_dot, v_cr = mag(va), mag(vb), dot(va, vb), cross(va, vb)
v_th = deg(math.acos(v_dot / (v_ma * v_mb)))
vpairs = [((1, 0, 0), (0, 1, 0)), ((1, 2, 3), (4, 5, 6)), ((3, -2, 1), (1, 4, 2)), ((2, 2, 0), (1, 0, 0)), ((1, 1, 1), (-1, -1, -1)), ((0, 3, 4), (0, 4, -3))]
v_rows = ''.join(f"| ({u[0]}, {u[1]}, {u[2]}) | ({v[0]}, {v[1]}, {v[2]}) | {dot(u, v)} | ({cross(u, v)[0]}, {cross(u, v)[1]}, {cross(u, v)[2]}) | {deg(math.acos(max(-1, min(1, dot(u, v)/(mag(u)*mag(v)))))):.2f}° |\n" for u, v in vpairs)
page('math', 'vector', f'''
title: Vector Calculator (Magnitude, Dot & Cross Product)
description: Calculate the magnitude of two 3D vectors, their dot product, cross product and the angle between them from the x, y and z components, with steps.
category: math
{intro("Vectors have both size and direction, and two products combine them: the dot product (a number) and the cross product (a new vector at right angles to both). This vector calculator takes the x, y and z components of vectors a and b and returns each magnitude, a · b, a × b and the angle between them.")}
keywords: [vector calculator, dot product calculator, cross product calculator, vector magnitude calculator, angle between two vectors, 3d vector calculator, vector length]
updated: {D}
variables:
  - {{ id: ax, label: Vector a — x, default: {va[0]} }}
  - {{ id: ay, label: Vector a — y, default: {va[1]} }}
  - {{ id: az, label: Vector a — z, default: {va[2]}, help: 'Enter 0 for 2D vectors.' }}
  - {{ id: bx, label: Vector b — x, default: {vb[0]} }}
  - {{ id: by, label: Vector b — y, default: {vb[1]} }}
  - {{ id: bz, label: Vector b — z, default: {vb[2]} }}
  - {{ id: ma, label: Magnitude |a|, min: 0 }}
  - {{ id: mb, label: Magnitude |b|, min: 0 }}
  - {{ id: dt, label: Dot product a · b }}
  - {{ id: cx, label: Cross product a × b — x }}
  - {{ id: cy, label: Cross product a × b — y }}
  - {{ id: cz, label: Cross product a × b — z }}
  - {{ id: mc, label: Magnitude |a × b|, min: 0 }}
  - {{ id: th, label: Angle between a and b, family: angle, unit: deg, min: 0, max: 3.14159265 }}
equations:
  - ma = sqrt(ax^2 + ay^2 + az^2)
  - mb = sqrt(bx^2 + by^2 + bz^2)
  - dt = ax*bx + ay*by + az*bz
  - cx = ay*bz - az*by
  - cy = az*bx - ax*bz
  - cz = ax*by - ay*bx
  - mc = sqrt(cx^2 + cy^2 + cz^2)
  - th = acos(dt / (ma * mb))
faq:
  - q: How do I calculate the magnitude of a vector?
    a: The magnitude is |a| = √(aₓ² + a_y² + a_z²) — the 3D version of the Pythagorean theorem.
  - q: What is the dot product used for?
    a: a · b = |a||b| cos θ, so it gives the angle between two vectors and tests whether they are perpendicular (dot product zero). In physics, work = force · displacement.
  - q: What does the cross product give?
    a: A vector perpendicular to both a and b, with length |a||b| sin θ — the area of the parallelogram they span. Its direction follows the right-hand rule, and a × b = −(b × a).
  - q: How do I use this for 2D vectors?
    a: Set both z components to 0. The cross product then points purely along z, and its z component equals aₓb_y − a_ybₓ.
related: [math/pythagorean-theorem, math/distance-midpoint, physics/torque, physics/force]
''', f'''
## How to use the vector calculator

Enter the **x, y and z components** of the two vectors (use 0 for z with 2D vectors). The calculator returns both magnitudes, the dot product, the three components and the length of the cross product, and the angle between the vectors.

## Vector formulas

<p class="formula">|a| = √(aₓ² + a_y² + a_z²) &nbsp;·&nbsp; a · b = aₓbₓ + a_yb_y + a_zb_z &nbsp;·&nbsp; θ = arccos(a · b ÷ (|a||b|))</p>

<p class="formula">a × b = (a_yb_z − a_zb_y, a_zbₓ − aₓb_z, aₓb_y − a_ybₓ)</p>

## Example

a = (3, −2, 1) and b = (1, 4, 2):

- |a| = √(9 + 4 + 1) = **{v_ma:.4f}**, |b| = √(1 + 16 + 4) = **{v_mb:.4f}**
- a · b = 3 × 1 + (−2) × 4 + 1 × 2 = **{v_dot}**
- a × b = ((−2)(2) − (1)(4), (1)(1) − (3)(2), (3)(4) − (−2)(1)) = **({v_cr[0]}, {v_cr[1]}, {v_cr[2]})**
- |a × b| = √{v_cr[0]**2 + v_cr[1]**2 + v_cr[2]**2} = **{mag(v_cr):.4f}**
- θ = arccos({v_dot} ÷ ({v_ma:.4f} × {v_mb:.4f})) = **{v_th:.2f}°**

## Worked vector products

| a | b | a · b | a × b | Angle |
|---|---|---|---|---|
{v_rows}
## Notes

- A dot product of zero means the vectors are perpendicular; a cross product of zero means they are parallel.
- The torque on a lever is the cross product r × F — see the [torque calculator](/physics/torque/).
''')

# ---------------------------------------------------------------- Complex numbers polar <-> rectangular
cn_re, cn_im = 3.0, 4.0
cn_r, cn_th = math.hypot(cn_re, cn_im), deg(math.atan2(cn_im, cn_re))
cn_rows = ''.join(f"| {t}° | {math.cos(rad(t)):.4f} | {math.sin(rad(t)):.4f} |\n" for t in (0, 30, 45, 60, 90, 120, 135, 150, 180, -90, -45))
page('math', 'complex-number', f'''
title: Complex Number Calculator (Polar ↔ Rectangular Form)
description: Convert a complex number between rectangular form a + bi and polar form r∠θ — get the magnitude (modulus) and angle (argument), or the real and imaginary parts.
category: math
{intro("A complex number can be written in rectangular form a + bi or in polar form r∠θ, where r is the magnitude and θ the angle from the real axis. This complex number calculator converts either way — the same conversion used for phasors when working with [impedance and reactance in AC circuits](ib:impedance-reactance-ac-circuits).")}
keywords: [complex number calculator, polar to rectangular calculator, rectangular to polar calculator, complex number to polar form, modulus and argument calculator, phasor conversion, magnitude and angle]
updated: {D}
variables:
  - {{ id: re, label: Real part (a), default: {cn_re:g} }}
  - {{ id: im, label: Imaginary part (b), default: {cn_im:g} }}
  - {{ id: r, label: Magnitude (modulus) r, min: 0 }}
  - {{ id: th, label: Angle (argument) θ, family: angle, unit: deg }}
equations:
  - r = sqrt(re^2 + im^2)
  - th = atan2(im, re)
  - re = r * cos(th)
  - im = r * sin(th)
freedom: 2
faq:
  - q: How do I convert a complex number to polar form?
    a: r = √(a² + b²) and θ = atan2(b, a). For 3 + 4i, r = 5 and θ = 53.13°, so 3 + 4i = 5∠53.13°.
  - q: How do I convert polar form to rectangular form?
    a: a = r cos θ and b = r sin θ. In this calculator, clear the real and imaginary parts and enter r and θ instead.
  - q: Why use atan2 instead of arctan(b/a)?
    a: arctan(b/a) cannot tell 1 + i from −1 − i, because both give b/a = 1. atan2 uses the signs of both parts and returns the angle in the correct quadrant, from −180° to +180°.
  - q: Where are polar complex numbers used?
    a: In AC circuit analysis, voltages, currents and impedances are phasors — a magnitude and a phase angle. Multiplying and dividing is easiest in polar form (multiply magnitudes, add angles), adding is easiest in rectangular form.
related: [math/pythagorean-theorem, math/right-triangle-trig, math/vector, electrical/kva-to-kw]
''', f'''
## How to use the complex number calculator

To convert **rectangular to polar**, enter the real part a and imaginary part b; the calculator returns the magnitude r and the angle θ. To convert **polar to rectangular**, clear a and b and enter r and θ instead. The angle can be shown in degrees, radians or other units.

## Complex number conversion formulas

<p class="formula">r = √(a² + b²) &nbsp;·&nbsp; θ = atan2(b, a) &nbsp;·&nbsp; a = r cos θ &nbsp;·&nbsp; b = r sin θ</p>

In exponential form, a + bi = r e<sup>iθ</sup> (Euler's formula).

## Example

z = 3 + 4i:

- r = √(3² + 4²) = **{cn_r:g}**
- θ = atan2(4, 3) = **{cn_th:.2f}°** ({math.radians(cn_th):.4f} rad)
- So 3 + 4i = 5∠{cn_th:.2f}°

## Unit phasors (r = 1)

| Angle θ | Real part cos θ | Imaginary part sin θ |
|---|---|---|
{cn_rows}
## Notes

- An angle and that angle ± 360° describe the same complex number.
- In electrical work, an impedance Z = R + jX has magnitude |Z| = √(R² + X²) and phase angle θ = atan(X/R); cos θ is the power factor — see the [kVA to kW calculator](/electrical/kva-to-kw/).
''')

# ---------------------------------------------------------------- Linear interpolation
li = (20.0, 0.99821, 30.0, 0.99565, 25.0)
def lin(x1, y1, x2, y2, x): return y1 + (x - x1) * (y2 - y1) / (x2 - x1)
li_y = lin(*li)
li_true = 0.99705
li_rows = ''.join(f"| {x:g} °C | {lin(20, 0.99821, 30, 0.99565, x):.5f} g/cm³ |\n" for x in range(20, 31, 2))
page('math', 'linear-interpolation', f'''
title: Linear Interpolation Calculator (Find y Between Two Points)
description: Interpolate a value between two known data points with y = y₁ + (x − x₁)(y₂ − y₁)/(x₂ − x₁) — for steam tables, calibration charts and any table lookup.
category: math
{intro("Engineering tables only list values at fixed steps, so values in between are found by drawing a straight line between the two nearest points. This linear interpolation calculator does that for any table — steam tables, density charts or sensor calibration points, where the error depends on how well the curve follows a straight line, the [sensor linearity](ib:what-is-sensor-linearity).")}
keywords: [linear interpolation calculator, interpolation calculator, interpolate between two points, linear interpolation formula, extrapolation calculator, table interpolation, double interpolation]
updated: {D}
variables:
  - {{ id: x1, label: Known point 1 — x₁, default: {li[0]:g} }}
  - {{ id: y1, label: Known point 1 — y₁, default: {li[1]:g} }}
  - {{ id: x2, label: Known point 2 — x₂, default: {li[2]:g} }}
  - {{ id: y2, label: Known point 2 — y₂, default: {li[3]:g} }}
  - {{ id: x, label: x value to interpolate at, default: {li[4]:g} }}
  - {{ id: y, label: Interpolated y value }}
equations:
  - y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
faq:
  - q: What is the linear interpolation formula?
    a: y = y₁ + (x − x₁)(y₂ − y₁) ÷ (x₂ − x₁). It assumes a straight line between the two known points (x₁, y₁) and (x₂, y₂).
  - q: What is the difference between interpolation and extrapolation?
    a: Interpolation estimates a value between the known points; extrapolation extends the line beyond them. The same formula works for both, but extrapolation is much less reliable.
  - q: How accurate is linear interpolation?
    a: It is exact for straight-line data. For curved data the error grows with the curvature and the spacing between table rows — use the closest bracketing rows, or a closer-spaced table.
  - q: How do I interpolate in a two-way table?
    a: Use double (bilinear) interpolation — interpolate along one variable in two rows, then interpolate between those two results along the other variable.
related: [math/slope, math/distance-midpoint, engineering/five-point-calibration, engineering/4-20ma-scaling]
''', f'''
## How to use the linear interpolation calculator

Enter the two known points that bracket your value — (x₁, y₁) and (x₂, y₂) — and the **x value** you want. The calculator returns the interpolated y. To find x for a known y (inverse interpolation), clear x and enter y.

## Linear interpolation formula

<p class="formula">y = y₁ + (x − x₁) × (y₂ − y₁) ÷ (x₂ − x₁)</p>

## Example

The density of water is 0.99821 g/cm³ at 20 °C and 0.99565 g/cm³ at 30 °C. At 25 °C:

- y = 0.99821 + (25 − 20) × (0.99565 − 0.99821) ÷ (30 − 20)
- y = 0.99821 + 5 × (−0.000256) = **{li_y:.5f} g/cm³**

The tabulated value at 25 °C is {li_true} g/cm³, so the straight-line estimate is off by {abs(li_true-li_y):.5f} g/cm³ — water density is slightly curved over this range.

## Interpolated water density between 20 °C and 30 °C

| Temperature | Interpolated density |
|---|---|
{li_rows}
## Notes

- Always interpolate between the two closest table rows.
- A 4–20 mA signal is converted to engineering units with exactly this formula — see the [4–20 mA scaling calculator](/engineering/4-20ma-scaling/).
''')

# ================================================================ CHEMISTRY

# ---------------------------------------------------------------- Raoult's law
def antoine(A, B, C, T): return 10 ** (A - B / (C + T)) * 0.133322387415  # mmHg -> kPa
BENZ, TOL = (6.90565, 1211.033, 220.790), (6.95464, 1344.8, 219.482)
ra_PA0, ra_PB0 = round(antoine(*BENZ, 80), 1), round(antoine(*TOL, 80), 1)
ra_x = 0.4
ra_PA, ra_PB = ra_x * ra_PA0, (1 - ra_x) * ra_PB0
ra_P = ra_PA + ra_PB
ra_rows = ''.join(f"| {x:.1f} | {x*ra_PA0:.1f} kPa | {(1-x)*ra_PB0:.1f} kPa | {x*ra_PA0+(1-x)*ra_PB0:.1f} kPa | {x*ra_PA0/(x*ra_PA0+(1-x)*ra_PB0):.3f} |\n" for x in (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0))
ra_trows = ''.join(f"| {t} °C | {antoine(*BENZ, t):.1f} kPa | {antoine(*TOL, t):.1f} kPa |\n" for t in (20, 40, 60, 80, 100))
page('chemistry', 'raoults-law', f'''
title: Raoult's Law Calculator (Vapour Pressure of a Mixture)
description: Calculate the partial and total vapour pressure of an ideal binary liquid mixture with Raoult's law, P = x_A·P°_A + x_B·P°_B, and the vapour composition.
category: chemistry
{intro("In an ideal liquid mixture each component contributes a vapour pressure in proportion to its mole fraction. This Raoult's law calculator gives the partial pressures, the total vapour pressure and the mole fraction of each component in the vapour — the basis of distillation and of vapour-pressure lowering by a dissolved solute.")}
keywords: [raoults law calculator, raoult's law calculator, vapour pressure of mixture, vapor pressure calculator, partial pressure raoults law, vapour pressure lowering, ideal solution]
updated: {D}
variables:
  - {{ id: xA, label: Mole fraction of A in the liquid (x_A), default: {ra_x:g}, min: 0, max: 1, help: 'Mole fraction of B is 1 − x_A.' }}
  - {{ id: PA0, label: Vapour pressure of pure A (P°_A), family: pressure, unit: kPa, default: {ra_PA0:g}, min: 0 }}
  - {{ id: PB0, label: Vapour pressure of pure B (P°_B), family: pressure, unit: kPa, default: {ra_PB0:g}, min: 0, help: 'Enter 0 for a non-volatile solute (vapour pressure lowering).' }}
  - {{ id: PA, label: Partial pressure of A, family: pressure, unit: kPa, min: 0 }}
  - {{ id: PB, label: Partial pressure of B, family: pressure, unit: kPa, min: 0 }}
  - {{ id: P, label: Total vapour pressure, family: pressure, unit: kPa, min: 0 }}
  - {{ id: yA, label: Mole fraction of A in the vapour (y_A), min: 0, max: 1, decimals: 4 }}
equations:
  - PA = xA * PA0
  - PB = (1 - xA) * PB0
  - P = PA + PB
  - yA = PA / P
faq:
  - q: What is Raoult's law?
    a: The partial vapour pressure of a component in an ideal solution equals its mole fraction in the liquid times the vapour pressure of the pure component — Pᵢ = xᵢ P°ᵢ. The total pressure is the sum of the partial pressures.
  - q: How does Raoult's law explain vapour pressure lowering?
    a: With a non-volatile solute (P°_B = 0), P = x_solvent × P°_solvent. Dissolving a solute lowers the solvent's mole fraction, so the vapour pressure drops — which is why solutions boil at a higher temperature.
  - q: Why is the vapour richer in the more volatile component?
    a: The component with the higher pure vapour pressure contributes more partial pressure per mole, so y_A = x_A P°_A ÷ P is larger than x_A. Distillation exploits this difference.
  - q: When does Raoult's law not apply?
    a: For non-ideal mixtures with strong attraction or repulsion between unlike molecules (ethanol–water, acetone–chloroform). These show positive or negative deviations and can form azeotropes. Dilute dissolved gases follow Henry's law instead.
related: [chemistry/henrys-law, chemistry/daltons-law, chemistry/boiling-point-elevation, chemistry/freezing-point-depression]
''', f'''
## How to use the Raoult's law calculator

Enter the **mole fraction of component A** in the liquid and the **vapour pressures of the pure components** at the mixture temperature. The calculator returns each partial pressure, the total vapour pressure and the composition of the vapour. For a solvent with a non-volatile solute, set P°_B to 0.

## Raoult's law formula

<p class="formula">P_A = x_A P°_A &nbsp;·&nbsp; P_B = (1 − x_A) P°_B &nbsp;·&nbsp; P = P_A + P_B &nbsp;·&nbsp; y_A = P_A ÷ P</p>

## Example

A benzene (A) – toluene (B) liquid with x_A = 0.4 at 80 °C, where P°_benzene = {ra_PA0:g} kPa and P°_toluene = {ra_PB0:g} kPa:

- P_A = 0.4 × {ra_PA0:g} = **{ra_PA:.2f} kPa**
- P_B = 0.6 × {ra_PB0:g} = **{ra_PB:.2f} kPa**
- P = {ra_PA:.2f} + {ra_PB:.2f} = **{ra_P:.2f} kPa**
- y_A = {ra_PA:.2f} ÷ {ra_P:.2f} = **{ra_PA/ra_P:.4f}** — the vapour is {ra_PA/ra_P*100:.0f}% benzene although the liquid is only 40%.

## Benzene–toluene at 80 °C

| x benzene (liquid) | P benzene | P toluene | Total P | y benzene (vapour) |
|---|---|---|---|---|
{ra_rows}
## Pure-component vapour pressures (Antoine equation)

| Temperature | Benzene | Toluene |
|---|---|---|
{ra_trows}
Calculated with the Antoine equation (log₁₀P[mmHg] = A − B ÷ (C + T[°C])), benzene A = 6.90565, B = 1211.033, C = 220.79; toluene A = 6.95464, B = 1344.8, C = 219.482.

## Notes

- Benzene–toluene is close to ideal; most real mixtures deviate somewhat.
- In the vapour, the partial pressures add up by [Dalton's law](/chemistry/daltons-law/).
''')

# ---------------------------------------------------------------- Henry's law
hk_k, hk_p, hk_M = 1.3e-3, 0.2095, 31.998
hk_c = hk_k * hk_p
gases_h = [('Oxygen (O₂)', 1.3e-3, 31.998, 0.2095), ('Nitrogen (N₂)', 6.1e-4, 28.014, 0.7808), ('Carbon dioxide (CO₂)', 3.4e-2, 44.009, 0.00042),
           ('Argon (Ar)', 1.4e-3, 39.948, 0.00934), ('Hydrogen (H₂)', 7.8e-4, 2.016, None), ('Helium (He)', 3.7e-4, 4.003, None), ('Carbon monoxide (CO)', 9.5e-4, 28.010, None)]
hk_rows = ''.join(f"| {nm} | {k:.2g} | {1/k:,.0f} | {k*M*1000:,.1f} mg/L | {(f'{k*x*M*1000:.3g} mg/L') if x else '—'} |\n" for nm, k, M, x in gases_h)
page('chemistry', 'henrys-law', f'''
title: Henry's Law Calculator (Gas Solubility in Water)
description: Calculate how much gas dissolves in a liquid with Henry's law, c = k_H·p, in mmol/L and mg/L — for oxygen, nitrogen, CO₂ and other gases in water.
category: chemistry
{intro("The amount of gas that dissolves in a liquid is proportional to the partial pressure of that gas above it. This Henry's law calculator turns a Henry's constant and a partial pressure into a dissolved concentration — the same relationship that sets the saturation value an [optical dissolved oxygen sensor](ib:how-do-optical-dissolved-oxygen-sensors-work) reads against.")}
keywords: [henrys law calculator, henry's law calculator, gas solubility calculator, henry's law constant, dissolved gas concentration, oxygen solubility in water, co2 solubility]
updated: {D}
variables:
  - {{ id: kH, label: Henry's law constant k_H, suffix: mol/(L·atm), default: {hk_k:g}, min: 0, help: 'At 25 °C in water — O₂ 1.3e-3 · N₂ 6.1e-4 · CO₂ 3.4e-2 · Ar 1.4e-3 · H₂ 7.8e-4' }}
  - {{ id: p, label: Partial pressure of the gas, family: pressure, unit: atm, default: {hk_p:g}, min: 0, help: 'Partial pressure = mole fraction in the gas × total pressure (O₂ in air at sea level ≈ 0.2095 atm).' }}
  - {{ id: M, label: Molar mass of the gas, suffix: g/mol, default: {hk_M:g}, min: 0 }}
  - {{ id: c, label: Dissolved concentration, suffix: mmol/L, min: 0 }}
  - {{ id: cm, label: Dissolved concentration, suffix: mg/L, min: 0 }}
equations:
  - c = kH * p / 101325 * 1000
  - cm = c * M
faq:
  - q: What is Henry's law?
    a: At constant temperature, the concentration of a gas dissolved in a liquid is proportional to its partial pressure above the liquid — c = k_H × p. Doubling the partial pressure doubles the dissolved amount.
  - q: Why are there different forms of Henry's constant?
    a: Some tables give solubility constants k_H = c/p (mol/(L·atm), used here); others give volatility constants k_H = p/c (L·atm/mol) or p/x (atm). The volatility form is simply the reciprocal, so check the units before using a table value.
  - q: How does temperature affect gas solubility?
    a: Most gases become less soluble as water warms — k_H for oxygen falls by roughly a third from 10 °C to 30 °C. That is why warm water holds less dissolved oxygen.
  - q: Why does a soda fizz when opened?
    a: It is bottled under several atmospheres of CO₂. Opening it drops the CO₂ partial pressure to about 0.0004 atm, so the dissolved CO₂ is far above its new equilibrium and comes out as bubbles.
related: [chemistry/raoults-law, chemistry/daltons-law, chemistry/ppm, chemistry/molarity]
''', f'''
## How to use the Henry's law calculator

Enter the gas's **Henry's law constant** (solubility form, mol/(L·atm)), its **partial pressure** above the liquid and its **molar mass**. The calculator returns the equilibrium dissolved concentration in mmol/L and mg/L. Clear the partial pressure and enter a concentration to find the pressure needed instead.

## Henry's law formula

<p class="formula">c = k<sub>H</sub> × p &nbsp;·&nbsp; c[mg/L] = c[mmol/L] × M</p>

## Example

Oxygen from air (p = 0.2095 atm) dissolving in water at 25 °C, k_H = 1.3 × 10⁻³ mol/(L·atm):

- c = 1.3 × 10⁻³ × 0.2095 = {hk_c*1e4:.3f} × 10⁻⁴ mol/L = **{hk_c*1000:.4f} mmol/L**
- c = {hk_c*1000:.4f} × {hk_M:g} = **{hk_c*1000*hk_M:.2f} mg/L**

Measured air-saturation values for fresh water at 25 °C are about 8.3 mg/L; the difference comes from the rounded constant and the water vapour that slightly lowers the O₂ partial pressure.

## Henry's law constants in water at 25 °C

| Gas | k_H (mol/(L·atm)) | 1/k_H (L·atm/mol) | Solubility at 1 atm partial pressure | In equilibrium with air |
|---|---|---|---|---|
{hk_rows}
Constants from standard compilations (Sander); the air column uses sea-level partial pressures (CO₂ at 420 ppm).

## Notes

- Henry's law holds for dilute solutions of gases that do not react with the solvent. CO₂ partly reacts to carbonic acid, so total dissolved carbon is higher at high pH.
- Partial pressures in a gas mixture follow [Dalton's law](/chemistry/daltons-law/).
''')

# ---------------------------------------------------------------- Van der Waals
vw_n, vw_T, vw_V, vw_a, vw_b = 1.0, 25.0, 1.0, 3.640, 0.04267
def vdw(n_, Tk, V_L, a, b): return (n_ * R * Tk / (V_L * 1e-3 - n_ * b * 1e-3) - a * 0.1 * n_**2 / (V_L * 1e-3)**2)
vw_P = vdw(vw_n, vw_T + 273.15, vw_V, vw_a, vw_b)
vw_Pi = vw_n * R * (vw_T + 273.15) / (vw_V * 1e-3)
vgases = [('Helium (He)', 0.0346, 0.0238), ('Hydrogen (H₂)', 0.2476, 0.02661), ('Nitrogen (N₂)', 1.370, 0.0387), ('Oxygen (O₂)', 1.382, 0.03186),
          ('Argon (Ar)', 1.355, 0.03201), ('Methane (CH₄)', 2.283, 0.04278), ('Carbon dioxide (CO₂)', 3.640, 0.04267)]
vw_rows = ''.join(f"| {nm} | {a:g} | {b:g} | {vdw(1, 298.15, 1, a, b)/1e5:.2f} bar | {vdw(1, 298.15, 1, a, b)/vw_Pi:.3f} |\n" for nm, a, b in vgases)
page('chemistry', 'van-der-waals', f'''
title: Van der Waals Equation Calculator (Real Gas Pressure)
description: Calculate the pressure of a real gas with the van der Waals equation, (P + an²/V²)(V − nb) = nRT, and compare it with the ideal gas law and compressibility Z.
category: chemistry
{intro("Real gas molecules attract each other and take up space, so at high pressure they stop behaving like an ideal gas. This van der Waals calculator corrects the ideal gas law with the attraction constant a and the excluded volume b, and shows how far the real pressure departs from PV = nRT.")}
keywords: [van der waals calculator, van der waals equation calculator, real gas calculator, van der waals constants, real gas pressure, compressibility factor, non-ideal gas]
updated: {D}
variables:
  - {{ id: nm, label: Amount of gas, suffix: mol, default: {vw_n:g}, min: 0 }}
  - {{ id: T, label: Temperature, family: temperature, unit: C, default: {vw_T:g}, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: L, default: {vw_V:g}, min: 0 }}
  - {{ id: a, label: Van der Waals constant a, suffix: L²·bar/mol², default: {vw_a:g}, min: 0, help: 'CO₂ 3.640 · N₂ 1.370 · O₂ 1.382 · CH₄ 2.283 · He 0.0346' }}
  - {{ id: b, label: Van der Waals constant b, suffix: L/mol, default: {vw_b:g}, min: 0, help: 'CO₂ 0.04267 · N₂ 0.0387 · O₂ 0.03186 · CH₄ 0.04278 · He 0.0238' }}
  - {{ id: P, label: Pressure (van der Waals), family: pressure, unit: bar }}
  - {{ id: Pi, label: Pressure (ideal gas law), family: pressure, unit: bar, min: 0 }}
  - {{ id: Z, label: Compressibility factor Z = P ÷ P_ideal, decimals: 4 }}
equations:
  - P = nm * 8.314462618 * T / (V - nm * b * 1e-3) - a * 0.1 * nm^2 / V^2
  - Pi = nm * 8.314462618 * T / V
  - Z = P / Pi
faq:
  - q: What is the van der Waals equation?
    a: (P + a n² ÷ V²)(V − n b) = n R T. The a term adds back the pressure lost to attraction between molecules, and the b term subtracts the volume the molecules themselves occupy.
  - q: What do the constants a and b mean?
    a: a measures how strongly the molecules attract (large for polar or big molecules such as CO₂ and water), b is the volume excluded per mole of molecules. Both are found from the gas's critical point — a = 27R²T_c² ÷ (64P_c), b = RT_c ÷ (8P_c).
  - q: When is the ideal gas law good enough?
    a: At low pressure and high temperature — below a few bar near room temperature most gases are within 1% of ideal. The van der Waals correction matters at high pressure, low temperature or near condensation.
  - q: Which units do a and b use here?
    a: a in L²·bar/mol² and b in L/mol, the most common table units. To convert a from L²·atm/mol², multiply by 1.01325.
related: [physics/ideal-gas-law, chemistry/combined-gas-law, chemistry/boyles-law, chemistry/daltons-law]
''', f'''
## How to use the van der Waals calculator

Enter the **amount of gas**, the **temperature**, the **volume** and the gas's **van der Waals constants a and b** (see the table). The calculator returns the real-gas pressure, the ideal-gas pressure for comparison and the compressibility factor Z. Clear the volume and enter a pressure to solve for volume instead.

## Van der Waals equation

<p class="formula">P = n R T ÷ (V − n b) − a n² ÷ V²</p>

R = 8.314 J/(mol·K), T in kelvin. With a in L²·bar/mol² and b in L/mol, use V in litres and R = 0.08314 L·bar/(mol·K) to get P in bar.

## Example

1 mol of CO₂ in 1 L at 25 °C (a = 3.640, b = 0.04267):

- Ideal: P = 0.08314 × 298.15 ÷ 1 = **{vw_Pi/1e5:.2f} bar**
- Van der Waals: P = 0.08314 × 298.15 ÷ (1 − 0.04267) − 3.640 × 1² ÷ 1² = {vw_Pi/1e5/(1-vw_b):.2f} − 3.64 = **{vw_P/1e5:.2f} bar**
- Z = {vw_P/1e5:.2f} ÷ {vw_Pi/1e5:.2f} = **{vw_P/vw_Pi:.4f}** — attraction lowers the pressure about {(1-vw_P/vw_Pi)*100:.0f}% below ideal.

## Van der Waals constants and pressure of 1 mol in 1 L at 25 °C

| Gas | a (L²·bar/mol²) | b (L/mol) | Van der Waals P | Z |
|---|---|---|---|---|
{vw_rows}
The ideal-gas pressure under the same conditions is {vw_Pi/1e5:.2f} bar. Light gases (He, H₂) have Z above 1 because the excluded volume outweighs the weak attraction.

## Notes

- The van der Waals equation is a teaching model; for accurate design work use Peng–Robinson or tabulated Z values.
- For an ideal gas, use the [ideal gas law calculator](/physics/ideal-gas-law/).
''')

# ---------------------------------------------------------------- Normality
no_m, no_Mw, no_neq, no_V = 4.904, 98.079, 2, 500.0
no_M = no_m / no_Mw / (no_V / 1000)
reag = [('Hydrochloric acid (HCl)', 36.46, 1, 'acid–base'), ('Sulfuric acid (H₂SO₄)', 98.079, 2, 'acid–base'), ('Phosphoric acid (H₃PO₄)', 97.994, 3, 'full neutralisation'),
        ('Sodium hydroxide (NaOH)', 39.997, 1, 'acid–base'), ('Calcium hydroxide (Ca(OH)₂)', 74.093, 2, 'acid–base'), ('Sodium carbonate (Na₂CO₃)', 105.988, 2, 'to CO₂'),
        ('Oxalic acid dihydrate (H₂C₂O₄·2H₂O)', 126.065, 2, 'acid–base or redox'), ('Potassium permanganate (KMnO₄)', 158.034, 5, 'redox, acid solution'), ('Potassium dichromate (K₂Cr₂O₇)', 294.185, 6, 'redox, acid solution')]
no_rows = ''.join(f"| {nm} | {Mw:g} | {k} ({why}) | {Mw/k:.3f} | {Mw/k:.3f} g |\n" for nm, Mw, k, why in reag)
page('chemistry', 'normality', f'''
title: Normality Calculator (Equivalents per Litre, N)
description: Calculate the normality of a solution from the mass of solute, molar mass, equivalents per mole and volume — or the grams needed for a target normality.
category: chemistry
{intro("Normality counts reactive equivalents per litre — protons for an acid, hydroxide ions for a base, electrons for a redox reagent — so a 1 N acid exactly neutralises the same volume of a 1 N base. This normality calculator works out normality and molarity from the mass you weigh out, or the mass needed for a target N.")}
keywords: [normality calculator, normality formula, equivalent weight calculator, gram equivalent, normality to molarity, how to calculate normality, 0.1 n solution]
updated: {D}
variables:
  - {{ id: m, label: Mass of solute, family: mass, unit: g, imperialUnit: g, default: {no_m:g}, min: 0 }}
  - {{ id: Mw, label: Molar mass of solute, suffix: g/mol, default: {no_Mw:g}, min: 0 }}
  - {{ id: neq, label: Equivalents per mole (n), default: {no_neq}, min: 0, help: 'H⁺ per acid molecule, OH⁻ per base, or electrons per formula unit in a redox reaction.' }}
  - {{ id: V, label: Solution volume, family: volume, unit: mL, imperialUnit: mL, default: {no_V:g}, min: 0 }}
  - {{ id: c, label: Molarity, suffix: mol/L, min: 0 }}
  - {{ id: N, label: Normality, suffix: eq/L (N), min: 0 }}
  - {{ id: EW, label: Equivalent weight, suffix: g/eq, min: 0 }}
equations:
  - c = m * 1000 / Mw / (1000 * V)
  - N = c * neq
  - EW = Mw / neq
faq:
  - q: What is the formula for normality?
    a: N = (mass ÷ equivalent weight) ÷ volume in litres, where equivalent weight = molar mass ÷ n. Equivalently, N = molarity × n.
  - q: What is the difference between normality and molarity?
    a: Molarity counts moles per litre; normality counts reacting equivalents per litre. 1 M H₂SO₄ is 2 N because each molecule gives two H⁺ ions, while 1 M HCl is 1 N.
  - q: How do I make 1 L of 0.1 N H₂SO₄?
    a: The equivalent weight is 98.079 ÷ 2 = 49.04 g/eq, so 0.1 N needs 4.904 g per litre. In practice it is made by diluting concentrated acid and standardised by titration.
  - q: Why is normality used less today?
    a: Because n depends on the reaction — KMnO₄ transfers 5 electrons in acid but 3 in neutral solution — the same solution can have two normalities. IUPAC recommends molarity, but normality remains common in titration and water-testing methods.
related: [chemistry/molarity, chemistry/titration, chemistry/dilution, chemistry/water-hardness]
''', f'''
## How to use the normality calculator

Enter the **mass of solute**, its **molar mass**, the **equivalents per mole** and the final **solution volume**. The calculator returns the molarity, normality and equivalent weight. To find how much to weigh out, clear the mass and enter the normality you want.

## Normality formula

<p class="formula">N = M × n = (m ÷ EW) ÷ V &nbsp;·&nbsp; EW = molar mass ÷ n</p>

## Example

4.904 g of sulfuric acid (98.079 g/mol, n = 2) made up to 500 mL:

- Molarity = 4.904 ÷ 98.079 ÷ 0.500 = **{no_M:.4f} mol/L**
- Normality = {no_M:.4f} × 2 = **{no_M*2:.4f} N**
- Equivalent weight = 98.079 ÷ 2 = **{no_Mw/2:.3f} g/eq**

## Equivalent weights of common reagents

| Reagent | Molar mass (g/mol) | n (basis) | Equivalent weight (g/eq) | Mass for 1 L of 1 N |
|---|---|---|---|---|
{no_rows}
## Notes

- In a titration at the end point, N₁V₁ = N₂V₂ — see the [titration calculator](/chemistry/titration/).
- To dilute a stock solution, the [dilution calculator](/chemistry/dilution/) works the same way with normality as with molarity.
''')

# ---------------------------------------------------------------- Water hardness
MCaCO3, MCa, MMg = 100.0869, 40.078, 24.305
fCa, fMg = MCaCO3 / MCa, MCaCO3 / MMg
wh_Ca, wh_Mg = 60.0, 15.0
wh_H = fCa * wh_Ca + fMg * wh_Mg
wh_rows = ''.join(f"| {lo}–{hi if hi else '…'} mg/L | {cls} | {lo/17.848:.1f}–{(hi/17.848) if hi else 0:.1f} °dH | {lo/17.118:.1f}–{(hi/17.118) if hi else 0:.1f} gpg |\n".replace('–0.0 °dH', '+ °dH').replace('–0.0 gpg', '+ gpg') for lo, hi, cls in ((0, 60, 'Soft'), (61, 120, 'Moderately hard'), (121, 180, 'Hard'), (181, None, 'Very hard')))
wh_crows = ''.join(f"| {ca} mg/L | {mg} mg/L | {fCa*ca+fMg*mg:.0f} mg/L | {(fCa*ca+fMg*mg)/17.848:.1f} °dH |\n" for ca, mg in ((10, 2), (20, 5), (40, 10), (60, 15), (80, 20), (100, 30), (150, 40)))
page('chemistry', 'water-hardness', f'''
title: Water Hardness Calculator (ppm CaCO₃, °dH, gpg)
description: Calculate total water hardness as mg/L (ppm) CaCO₃ from calcium and magnesium, with °dH, °fH, grains per gallon and a soft-to-very-hard rating.
category: chemistry
{intro("Water hardness comes mainly from dissolved calcium and magnesium, and is reported as the equivalent amount of calcium carbonate. This water hardness calculator converts Ca and Mg results from a lab report into mg/L (ppm) as CaCO₃, German and French degrees and grains per gallon, and rates the water from soft to very hard.")}
keywords: [water hardness calculator, total hardness calculator, hardness as caco3, ppm caco3, german degrees hardness, grains per gallon hardness, calcium magnesium hardness]
updated: {D}
variables:
  - {{ id: Ca, label: Calcium (Ca²⁺), suffix: mg/L, default: {wh_Ca:g}, min: 0 }}
  - {{ id: Mg, label: Magnesium (Mg²⁺), suffix: mg/L, default: {wh_Mg:g}, min: 0 }}
  - id: H
    label: Total hardness as CaCO₃
    suffix: mg/L (ppm)
    min: 0
    bands:
      - {{ max: 60, label: Soft, color: '#16a34a' }}
      - {{ max: 120, label: Moderately hard, color: '#84cc16' }}
      - {{ max: 180, label: Hard, color: '#eab308' }}
      - {{ max: 1e12, label: Very hard, color: '#dc2626' }}
  - {{ id: dH, label: German degrees (°dH), min: 0, decimals: 2 }}
  - {{ id: fH, label: French degrees (°fH), min: 0, decimals: 2 }}
  - {{ id: gpg, label: Grains per US gallon (gpg), min: 0, decimals: 2 }}
  - {{ id: mmol, label: Hardness, suffix: mmol/L, min: 0, decimals: 3 }}
equations:
  - H = {fCa:.5f} * Ca + {fMg:.5f} * Mg
  - dH = H / 17.848
  - fH = H / 10
  - gpg = H / 17.118
  - mmol = H / 100.0869
faq:
  - q: How is total hardness calculated from calcium and magnesium?
    a: Hardness (mg/L as CaCO₃) = 2.497 × Ca + 4.118 × Mg, with Ca and Mg in mg/L. The factors are the molar mass of CaCO₃ (100.09) divided by the molar masses of Ca (40.08) and Mg (24.31).
  - q: What is a good water hardness?
    a: Below 60 mg/L is soft, 61–120 moderately hard, 121–180 hard and above 180 very hard (USGS classification). Hardness is not a health concern, but above about 120 mg/L scale builds up in kettles, boilers and pipes.
  - q: How do I convert ppm hardness to °dH or grains per gallon?
    a: 1 °dH = 17.848 mg/L CaCO₃, 1 °fH = 10 mg/L CaCO₃ and 1 grain per US gallon = 17.118 mg/L CaCO₃. Divide the ppm value by these factors.
  - q: What is the difference between temporary and permanent hardness?
    a: Temporary (carbonate) hardness is the part balanced by bicarbonate and is removed by boiling, which precipitates CaCO₃ scale. Permanent hardness is balanced by sulfate or chloride and stays after boiling; it needs ion exchange or reverse osmosis.
related: [chemistry/ppm, chemistry/molarity, chemistry/normality, chemistry/titration]
''', f'''
## How to use the water hardness calculator

Enter the **calcium** and **magnesium** concentrations in mg/L from your water test. The calculator returns total hardness as mg/L CaCO₃ (the same as ppm in dilute water) with a soft-to-very-hard rating, plus German degrees, French degrees, grains per gallon and mmol/L. If you only have a total hardness result, clear Ca and Mg and enter it directly to convert between units.

## Water hardness formula

<p class="formula">Hardness (mg/L CaCO₃) = 2.497 × Ca + 4.118 × Mg</p>

<p class="formula">°dH = ppm ÷ 17.848 &nbsp;·&nbsp; °fH = ppm ÷ 10 &nbsp;·&nbsp; gpg = ppm ÷ 17.118 &nbsp;·&nbsp; mmol/L = ppm ÷ 100.09</p>

## Example

A well water with 60 mg/L calcium and 15 mg/L magnesium:

- From calcium: 2.497 × 60 = {fCa*wh_Ca:.1f} mg/L
- From magnesium: 4.118 × 15 = {fMg*wh_Mg:.1f} mg/L
- Total hardness = **{wh_H:.1f} mg/L as CaCO₃** — very hard
- = {wh_H/17.848:.2f} °dH = {wh_H/10:.2f} °fH = {wh_H/17.118:.2f} gpg

## Hardness classification

| Hardness as CaCO₃ | Rating | German degrees | Grains per gallon |
|---|---|---|---|
{wh_rows}
## Hardness for typical Ca and Mg levels

| Calcium | Magnesium | Total hardness | German degrees |
|---|---|---|---|
{wh_crows}
## Notes

- Lab titrations with EDTA report total hardness directly as mg/L CaCO₃.
- To convert between mg/L and other concentration units, use the [ppm calculator](/chemistry/ppm/).
''')

# ================================================================ STATISTICS

# ---------------------------------------------------------------- Uniform distribution
un_a, un_b, un_x1, un_x2 = 2.0, 10.0, 4.0, 7.0
un_P = (un_x2 - un_x1) / (un_b - un_a)
un_rows = ''.join(f"| {x:g} | {(x-un_a)/(un_b-un_a):.4f} | {1-(x-un_a)/(un_b-un_a):.4f} |\n" for x in (2, 3, 4, 5, 6, 7, 8, 9, 10))
page('statistics', 'uniform-distribution', f'''
title: Uniform Distribution Calculator (Continuous, Probability)
description: Calculate probabilities for a continuous uniform distribution between a and b — P(x₁ ≤ X ≤ x₂), the density, the mean, variance and standard deviation.
category: statistics
{intro("In a continuous uniform distribution every value between a minimum a and a maximum b is equally likely, so probabilities are simply lengths of intervals. This uniform distribution calculator gives the probability that X falls between two values, the probability density, and the mean, variance and standard deviation.")}
keywords: [uniform distribution calculator, continuous uniform distribution, uniform probability calculator, rectangular distribution, uniform distribution mean and variance, uniform distribution formula, probability between two values]
updated: {D}
variables:
  - {{ id: a, label: Minimum a, default: {un_a:g} }}
  - {{ id: b, label: Maximum b, default: {un_b:g} }}
  - {{ id: x1, label: Lower value x₁, default: {un_x1:g} }}
  - {{ id: x2, label: Upper value x₂, default: {un_x2:g} }}
  - {{ id: P, label: P(x₁ ≤ X ≤ x₂), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: f, label: Probability density f(x) = 1 ÷ (b − a), min: 0, decimals: 6 }}
  - {{ id: mu, label: Mean (a + b) ÷ 2 }}
  - {{ id: v, label: Variance (b − a)² ÷ 12, min: 0 }}
  - {{ id: sd, label: Standard deviation, min: 0 }}
equations:
  - P = max(0, min(x2, b) - max(x1, a)) / (b - a)
  - f = 1 / (b - a)
  - mu = (a + b) / 2
  - v = (b - a)^2 / 12
  - sd = sqrt(v)
faq:
  - q: What is the formula for a uniform distribution probability?
    a: P(x₁ ≤ X ≤ x₂) = (x₂ − x₁) ÷ (b − a) for an interval inside [a, b]. Parts of the interval outside [a, b] have zero probability.
  - q: What are the mean and variance of a uniform distribution?
    a: Mean = (a + b) ÷ 2, variance = (b − a)² ÷ 12, standard deviation = (b − a) ÷ √12 ≈ 0.2887 (b − a).
  - q: Where is the uniform distribution used?
    a: For random number generators, rounding and quantisation error, waiting times when arrivals are spread evenly, and in measurement uncertainty — a ± tolerance with no other information is treated as rectangular, giving a standard uncertainty of half-width ÷ √3.
  - q: What about the discrete uniform distribution?
    a: For n equally likely whole-number outcomes (like a die), each has probability 1/n, the mean is (a + b) ÷ 2 and the variance is (n² − 1) ÷ 12.
related: [statistics/normal-distribution, statistics/exponential-distribution, statistics/probability, statistics/measurement-uncertainty]
''', f'''
## How to use the uniform distribution calculator

Enter the **minimum a** and **maximum b** of the distribution and the interval **x₁ to x₂** you are interested in. The calculator returns the probability that X falls in that interval, the constant probability density, and the mean, variance and standard deviation. For P(X ≤ x), set x₁ equal to a.

## Uniform distribution formulas

<p class="formula">f(x) = 1 ÷ (b − a) &nbsp;·&nbsp; P(x₁ ≤ X ≤ x₂) = (x₂ − x₁) ÷ (b − a)</p>

<p class="formula">μ = (a + b) ÷ 2 &nbsp;·&nbsp; σ² = (b − a)² ÷ 12</p>

## Example

A bus arrives at a random time uniformly between 2 and 10 minutes after you reach the stop. The chance it arrives between minute 4 and minute 7:

- P = (7 − 4) ÷ (10 − 2) = 3 ÷ 8 = **{un_P*100:.1f}%**
- Density = 1 ÷ 8 = **{1/(un_b-un_a):g}** per minute
- Mean wait = (2 + 10) ÷ 2 = **{(un_a+un_b)/2:g} min**, variance = 8² ÷ 12 = **{(un_b-un_a)**2/12:.4f}**, standard deviation = **{(un_b-un_a)/math.sqrt(12):.4f} min**

## Cumulative probabilities (a = 2, b = 10)

| x | P(X ≤ x) | P(X > x) |
|---|---|---|
{un_rows}
## Notes

- Every interval of the same length inside [a, b] has the same probability.
- The sum of many independent uniform variables tends towards a [normal distribution](/statistics/normal-distribution/).
''')

# ---------------------------------------------------------------- Geometric distribution
ge_p, ge_k = 0.2, 3
ge_P = (1 - ge_p) ** (ge_k - 1) * ge_p
ge_rows = ''.join(f"| {k} | {(1-ge_p)**(k-1)*ge_p*100:.2f}% | {(1-(1-ge_p)**k)*100:.2f}% | {(1-ge_p)**k*100:.2f}% |\n" for k in range(1, 13))
page('statistics', 'geometric-distribution', f'''
title: Geometric Distribution Calculator (Trials to First Success)
description: Calculate geometric distribution probabilities — the chance the first success comes on trial k, within k trials or after k — plus the mean and variance.
category: statistics
{intro("The geometric distribution describes how many independent tries it takes to get the first success when each try has the same probability p. This geometric distribution calculator gives the probability that the first success comes exactly on trial k, by trial k or only after k, along with the expected number of trials.")}
keywords: [geometric distribution calculator, geometric probability calculator, probability of first success, number of trials until success, geometric distribution formula, geometric distribution mean, cumulative geometric probability]
updated: {D}
variables:
  - {{ id: p, label: Probability of success per trial (p), family: percent, unit: '%', default: {ge_p*100:g}, min: 0, max: 1 }}
  - {{ id: k, label: Trial number of the first success (k), default: {ge_k}, min: 1 }}
  - {{ id: P, label: P(X = k) — first success on trial k, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: Pc, label: P(X ≤ k) — success within k trials, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: Pg, label: P(X > k) — no success in k trials, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: mu, label: Expected number of trials (1 ÷ p), min: 0 }}
  - {{ id: sd, label: Standard deviation, min: 0 }}
equations:
  - P = (1 - p)^(k - 1) * p
  - Pc = 1 - (1 - p)^k
  - Pg = (1 - p)^k
  - mu = 1 / p
  - sd = sqrt(1 - p) / p
faq:
  - q: What is the geometric distribution formula?
    a: P(X = k) = (1 − p)^(k − 1) × p — k − 1 failures followed by one success. The probability of success within k trials is P(X ≤ k) = 1 − (1 − p)^k.
  - q: What is the mean of a geometric distribution?
    a: The expected number of trials up to and including the first success is 1 ÷ p, and the variance is (1 − p) ÷ p². With p = 20% you expect 5 trials on average.
  - q: What is the difference between the two definitions of the geometric distribution?
    a: This calculator counts trials up to and including the first success (k = 1, 2, 3 …). Some textbooks count only the failures before it (k = 0, 1, 2 …); then P = (1 − p)^k × p and the mean is (1 − p) ÷ p.
  - q: Is the geometric distribution memoryless?
    a: Yes — having already failed several times does not change the chance of success on the next trial. It is the discrete counterpart of the exponential distribution.
related: [statistics/binomial-probability, statistics/exponential-distribution, statistics/poisson-probability, statistics/probability]
''', f'''
## How to use the geometric distribution calculator

Enter the **probability of success** on each trial and the **trial number k**. The calculator returns the probability that the first success happens exactly on trial k, by trial k at the latest, and not within k trials, plus the mean and standard deviation of the number of trials. Clear p and enter a target P(X ≤ k) to find the success rate needed.

## Geometric distribution formulas

<p class="formula">P(X = k) = (1 − p)<sup>k−1</sup> p &nbsp;·&nbsp; P(X ≤ k) = 1 − (1 − p)<sup>k</sup></p>

<p class="formula">μ = 1 ÷ p &nbsp;·&nbsp; σ = √(1 − p) ÷ p</p>

## Example

A sales call succeeds 20% of the time. The chance that the first sale comes on the 3rd call:

- P(X = 3) = 0.8² × 0.2 = **{ge_P*100:.1f}%**
- P(X ≤ 3) = 1 − 0.8³ = **{(1-0.8**3)*100:.1f}%**, P(X > 3) = 0.8³ = **{0.8**3*100:.1f}%**
- Expected calls = 1 ÷ 0.2 = **{1/ge_p:g}**, standard deviation = √0.8 ÷ 0.2 = **{math.sqrt(0.8)/0.2:.4f}**

## Geometric probabilities for p = 20%

| k | P(X = k) | P(X ≤ k) | P(X > k) |
|---|---|---|---|
{ge_rows}
## Notes

- The trials must be independent with a constant success probability.
- To count successes in a fixed number of trials instead, use the [binomial probability calculator](/statistics/binomial-probability/).
''')

# ---------------------------------------------------------------- Hypergeometric distribution
C = math.comb
hg_N, hg_K, hg_n, hg_k = 52, 4, 5, 1
def hyp(N, K, n_, k): return C(K, k) * C(N - K, n_ - k) / C(N, n_)
hg_P = hyp(hg_N, hg_K, hg_n, hg_k)
hg_mu = hg_n * hg_K / hg_N
hg_var = hg_n * hg_K / hg_N * (hg_N - hg_K) / hg_N * (hg_N - hg_n) / (hg_N - 1)
hg_rows = ''.join(f"| {k} | {C(4,k)*C(48,5-k):,} | {hyp(52,4,5,k)*100:.4f}% | {sum(hyp(52,4,5,j) for j in range(k+1))*100:.4f}% |\n" for k in range(5))
page('statistics', 'hypergeometric-distribution', f'''
title: Hypergeometric Distribution Calculator (Without Replacement)
description: Calculate the hypergeometric probability of exactly k successes in n draws without replacement — for cards, lotteries and lot sampling — with the mean.
category: statistics
{intro("When you draw items without putting them back — cards from a deck, parts from a production lot — each draw changes the odds for the next one, and the binomial distribution no longer fits. This hypergeometric distribution calculator gives the probability of exactly k successes in n draws, the chance of at least one, and the expected number of successes.")}
keywords: [hypergeometric distribution calculator, hypergeometric probability calculator, sampling without replacement, card probability calculator, lot acceptance sampling, hypergeometric formula, probability of at least one]
updated: {D}
variables:
  - {{ id: N, label: Population size (N), default: {hg_N}, min: 1 }}
  - {{ id: K, label: Successes in the population (K), default: {hg_K}, min: 0 }}
  - {{ id: n, label: Number of draws (n), default: {hg_n}, min: 0 }}
  - {{ id: k, label: Successes in the draw (k), default: {hg_k}, min: 0 }}
  - {{ id: P, label: P(X = k), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: P1, label: P(X ≥ 1) — at least one success, family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: mu, label: Expected successes (n K ÷ N), min: 0 }}
  - {{ id: sd, label: Standard deviation, min: 0 }}
equations:
  - P = nCr(K, k) * nCr(N - K, n - k) / nCr(N, n)
  - P1 = 1 - nCr(N - K, n) / nCr(N, n)
  - mu = n * K / N
  - sd = sqrt(n * K / N * (N - K) / N * (N - n) / (N - 1))
faq:
  - q: What is the hypergeometric distribution formula?
    a: P(X = k) = C(K, k) × C(N − K, n − k) ÷ C(N, n) — the ways to choose k of the K successes and n − k of the failures, divided by all ways to choose n items.
  - q: When should I use hypergeometric instead of binomial?
    a: When sampling without replacement from a finite population. If the sample is less than about 5% of the population, the binomial distribution with p = K/N gives nearly the same answer.
  - q: What is the probability of being dealt exactly one ace in 5 cards?
    a: C(4,1) × C(48,4) ÷ C(52,5) = 778,320 ÷ 2,598,960 ≈ 29.95%.
  - q: How is it used in quality control?
    a: In acceptance sampling, a lot of N parts contains K defectives and you inspect n. P(X = 0) is the chance the sample shows no defects, so 1 − P(X = 0) is the chance of catching at least one.
related: [statistics/binomial-probability, statistics/combinations, statistics/probability, statistics/geometric-distribution]
''', f'''
## How to use the hypergeometric distribution calculator

Enter the **population size N**, the number of **successes K** in it, the number of **draws n** and the number of **successes k** you want in the draw. The calculator returns the probability of exactly k successes, the probability of at least one success, and the mean and standard deviation of the number of successes.

## Hypergeometric formula

<p class="formula">P(X = k) = C(K, k) × C(N − K, n − k) ÷ C(N, n)</p>

<p class="formula">μ = n K ÷ N &nbsp;·&nbsp; σ² = n (K/N) (1 − K/N) (N − n) ÷ (N − 1)</p>

## Example

The chance of exactly one ace in a 5-card hand (N = 52 cards, K = 4 aces, n = 5, k = 1):

- C(4, 1) × C(48, 4) = 4 × 194,580 = 778,320 favourable hands
- C(52, 5) = 2,598,960 possible hands
- P = 778,320 ÷ 2,598,960 = **{hg_P*100:.2f}%**
- P(at least one ace) = 1 − C(48, 5) ÷ C(52, 5) = **{(1-C(48,5)/C(52,5))*100:.2f}%**
- Expected aces = 5 × 4 ÷ 52 = **{hg_mu:.4f}**, standard deviation = **{math.sqrt(hg_var):.4f}**

## Aces in a 5-card hand

| Aces k | Hands | P(X = k) | P(X ≤ k) |
|---|---|---|---|
{hg_rows}
## Notes

- k cannot exceed K or n, and n − k cannot exceed N − K; such combinations have zero probability.
- The counts use combinations — see the [combinations calculator](/statistics/combinations/).
''')

# ---------------------------------------------------------------- Process capability
pc = dict(USL=10.05, LSL=9.95, mu=10.01, s=0.012)
pc_Cp = (pc['USL'] - pc['LSL']) / (6 * pc['s'])
pc_Cpu = (pc['USL'] - pc['mu']) / (3 * pc['s'])
pc_Cpl = (pc['mu'] - pc['LSL']) / (3 * pc['s'])
pc_Cpk = min(pc_Cpu, pc_Cpl)
pc_ppm = (Phi(-3 * pc_Cpu) + Phi(-3 * pc_Cpl)) * 1e6
pc_rows = ''.join(f"| {c:.2f} | {3*c:.1f}σ | {2*Phi(-3*c)*1e6:,.{3 if c >= 1.9 else 1}f} | {(1-2*Phi(-3*c))*100:.5f}% |\n" for c in (0.5, 0.67, 1.0, 1.33, 1.5, 1.67, 2.0))
page('statistics', 'process-capability', f'''
title: Process Capability Calculator (Cp, Cpk, PPM)
description: Calculate process capability indices Cp, Cpk, Cpu and Cpl from the specification limits, process mean and standard deviation, plus expected ppm defects.
category: statistics
{intro("Process capability compares the spread of a process with the tolerance it has to meet. This process capability calculator returns Cp (potential capability), Cpk (actual capability, allowing for an off-centre mean) and the expected parts per million outside the specification limits, assuming a normal distribution.")}
keywords: [process capability calculator, cpk calculator, cp cpk calculator, process capability index, cpk formula, ppm defects, cpu cpl]
updated: {D}
variables:
  - {{ id: USL, label: Upper specification limit (USL), default: {pc['USL']:g} }}
  - {{ id: LSL, label: Lower specification limit (LSL), default: {pc['LSL']:g} }}
  - {{ id: mu, label: Process mean (x̄), default: {pc['mu']:g} }}
  - {{ id: s, label: Process standard deviation (σ), default: {pc['s']:g}, min: 0, help: 'Use the within-subgroup σ for Cp/Cpk; the overall σ gives Pp/Ppk.' }}
  - {{ id: Cp, label: Cp (potential capability), decimals: 3 }}
  - {{ id: Cpu, label: Cpu (upper), decimals: 3 }}
  - {{ id: Cpl, label: Cpl (lower), decimals: 3 }}
  - {{ id: Cpk, label: Cpk (actual capability), decimals: 3 }}
  - {{ id: ppm, label: Expected out of specification, suffix: ppm, min: 0, decimals: 1 }}
equations:
  - Cp = (USL - LSL) / (6 * s)
  - Cpu = (USL - mu) / (3 * s)
  - Cpl = (mu - LSL) / (3 * s)
  - Cpk = min(Cpu, Cpl)
  - ppm = (normcdf(-3 * Cpu) + normcdf(-3 * Cpl)) * 1e6
faq:
  - q: What is the difference between Cp and Cpk?
    a: Cp = (USL − LSL) ÷ 6σ compares the tolerance width with the process spread and ignores where the process is centred. Cpk = min(USL − x̄, x̄ − LSL) ÷ 3σ also accounts for an off-centre mean, so Cpk ≤ Cp, and they are equal only when the process is centred.
  - q: What is a good Cpk value?
    a: 1.33 is the usual minimum for an established process (about 63 ppm out of tolerance when centred), 1.67 for new or safety-critical characteristics, and 2.0 corresponds to six sigma quality.
  - q: What is the difference between Cpk and Ppk?
    a: Cpk uses the short-term, within-subgroup standard deviation (from a control chart, R̄/d₂); Ppk uses the overall standard deviation of all data. Ppk reflects what the customer actually receives.
  - q: Does Cpk assume a normal distribution?
    a: The ppm estimate does. Check normality with a histogram or probability plot first; skewed data (such as flatness or runout) need a transformation or a non-normal capability method.
related: [statistics/six-sigma, statistics/normal-distribution, statistics/z-score, statistics/standard-deviation]
''', f'''
## How to use the process capability calculator

Enter the **upper and lower specification limits**, the **process mean** and the **process standard deviation**. The calculator returns Cp, the one-sided indices Cpu and Cpl, Cpk (the smaller of the two) and the expected fraction outside the limits in parts per million. Collect at least 25 subgroups from a stable process before trusting the result.

## Process capability formulas

<p class="formula">Cp = (USL − LSL) ÷ 6σ &nbsp;·&nbsp; Cpu = (USL − x̄) ÷ 3σ &nbsp;·&nbsp; Cpl = (x̄ − LSL) ÷ 3σ &nbsp;·&nbsp; Cpk = min(Cpu, Cpl)</p>

<p class="formula">ppm = [Φ(−3 Cpu) + Φ(−3 Cpl)] × 10⁶</p>

## Example

A shaft diameter specified 10.00 ± 0.05 mm (USL 10.05, LSL 9.95), with mean 10.01 mm and σ = 0.012 mm:

- Cp = 0.10 ÷ (6 × 0.012) = **{pc_Cp:.3f}**
- Cpu = (10.05 − 10.01) ÷ (3 × 0.012) = **{pc_Cpu:.3f}**, Cpl = (10.01 − 9.95) ÷ 0.036 = **{pc_Cpl:.3f}**
- Cpk = min({pc_Cpu:.3f}, {pc_Cpl:.3f}) = **{pc_Cpk:.3f}**
- Expected out of tolerance = [Φ(−{3*pc_Cpu:.3f}) + Φ(−{3*pc_Cpl:.3f})] × 10⁶ = **{pc_ppm:.1f} ppm**

Centring the process at 10.00 mm would raise Cpk to {pc_Cp:.3f} without reducing the variation.

## Cpk and expected defects (centred process)

| Cpk | Distance to nearest limit | Out of spec (ppm) | Yield |
|---|---|---|---|
{pc_rows}
## Notes

- Capability only means something for a process in statistical control.
- Six sigma quality with a 1.5σ long-term shift corresponds to 3.4 defects per million — see the [six sigma calculator](/statistics/six-sigma/).
''')

# ---------------------------------------------------------------- Six sigma / DPMO
ss_D, ss_U, ss_O = 27, 1500, 5
ss_dpmo = ss_D / (ss_U * ss_O) * 1e6
ss_Y = 1 - ss_dpmo / 1e6
def zinv(p):
    lo, hi = -10.0, 10.0
    for _ in range(200):
        m = (lo + hi) / 2
        if Phi(m) < p: lo = m
        else: hi = m
    return (lo + hi) / 2
ss_sig = zinv(ss_Y) + 1.5
ss_rows = ''.join(f"| {s:g}σ | {(1-Phi(s-1.5))*1e6:,.{1 if s >= 5 else 0}f} | {Phi(s-1.5)*100:.4f}% |\n" for s in (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6))
page('statistics', 'six-sigma', f'''
title: Six Sigma Calculator (DPMO, Yield & Sigma Level)
description: Calculate defects per million opportunities (DPMO), process yield and the six sigma level from defects, units and opportunities per unit, with the 1.5σ shift.
category: statistics
{intro("Six Sigma measures quality by counting defects per million opportunities and converting that rate into a sigma level, where 6σ means just 3.4 defects per million. This six sigma calculator works out DPU, DPMO, yield and the sigma level from your defect count, using the standard 1.5σ long-term shift.")}
keywords: [six sigma calculator, dpmo calculator, sigma level calculator, defects per million opportunities, process sigma calculator, dpmo to sigma, yield to sigma]
updated: {D}
variables:
  - {{ id: Dn, label: Number of defects, default: {ss_D}, min: 0 }}
  - {{ id: U, label: Number of units inspected, default: {ss_U}, min: 0 }}
  - {{ id: O, label: Defect opportunities per unit, default: {ss_O}, min: 0 }}
  - {{ id: DPU, label: Defects per unit (DPU), min: 0, decimals: 4 }}
  - {{ id: DPMO, label: Defects per million opportunities (DPMO), min: 0, max: 1000000, decimals: 1 }}
  - {{ id: Y, label: Yield (1 − DPMO ÷ 10⁶), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: sig, label: Sigma level (with 1.5σ shift), decimals: 2 }}
equations:
  - DPU = Dn / U
  - DPMO = Dn / (U * O) * 1e6
  - Y = 1 - DPMO / 1e6
  - Y = normcdf(sig - 1.5)
faq:
  - q: How do I calculate DPMO?
    a: DPMO = defects ÷ (units × opportunities per unit) × 1,000,000. With 27 defects in 1,500 units having 5 opportunities each, DPMO = 27 ÷ 7,500 × 10⁶ = 3,600.
  - q: How is DPMO converted to a sigma level?
    a: Sigma level = z(1 − DPMO/10⁶) + 1.5, where z is the inverse of the standard normal distribution. The 1.5 is the conventional allowance for the process mean drifting over the long term.
  - q: Why is six sigma 3.4 defects per million and not 0.001?
    a: A pure 6σ distance to the limit gives about 0.001 ppm, but Six Sigma assumes the mean shifts 1.5σ in the long run, leaving 4.5σ to the nearest limit — and 4.5σ corresponds to 3.4 ppm.
  - q: What is an opportunity?
    a: A distinct chance for a defect that the customer cares about and that you check — for example each solder joint on a board. Define opportunities consistently, because counting more of them lowers DPMO.
related: [statistics/process-capability, statistics/normal-distribution, statistics/z-score, statistics/probability]
''', f'''
## How to use the six sigma calculator

Enter the **number of defects** found, the **number of units** inspected and the **defect opportunities per unit**. The calculator returns defects per unit, DPMO, the yield (first-pass yield per opportunity) and the process sigma level. To find the DPMO for a target sigma level, clear the defects and enter the sigma level.

## Six sigma formulas

<p class="formula">DPU = D ÷ U &nbsp;·&nbsp; DPMO = D ÷ (U × O) × 10⁶ &nbsp;·&nbsp; Yield = 1 − DPMO ÷ 10⁶</p>

<p class="formula">Sigma level = Φ⁻¹(Yield) + 1.5</p>

## Example

27 defects found in 1,500 assemblies with 5 opportunities each:

- DPU = 27 ÷ 1,500 = **{ss_D/ss_U:.4f}**
- DPMO = 27 ÷ (1,500 × 5) × 10⁶ = **{ss_dpmo:,.0f}**
- Yield = 1 − 0.0036 = **{ss_Y*100:.2f}%**
- Sigma level = Φ⁻¹(0.9964) + 1.5 = {zinv(ss_Y):.3f} + 1.5 = **{ss_sig:.2f}σ**

## Sigma level to DPMO (1.5σ shift)

| Sigma level | DPMO | Yield |
|---|---|---|
{ss_rows}
## Notes

- Without the 1.5σ shift (short-term sigma), subtract 1.5 from the sigma levels above.
- For a measured characteristic with specification limits, use the [process capability calculator](/statistics/process-capability/) — Cpk × 3 is the short-term sigma level.
''')

# ---------------------------------------------------------------- Expected value
ev_x, ev_p = (100, 20, 0, -10), (0.05, 0.15, 0.5, 0.3)
ev_E = sum(x * p for x, p in zip(ev_x, ev_p))
ev_E2 = sum(x * x * p for x, p in zip(ev_x, ev_p))
ev_V = ev_E2 - ev_E ** 2
ev_rows = ''.join(f"| {x:+g} | {p*100:g}% | {x*p:+.2f} | {x*x*p:.2f} |\n" for x, p in zip(ev_x, ev_p))
ev_dice = sum(range(1, 7)) / 6
page('statistics', 'expected-value', f'''
title: Expected Value Calculator (Mean, Variance of Outcomes)
description: Calculate the expected value E(X) of a discrete random variable from up to four outcomes and their probabilities, with the variance and standard deviation.
category: statistics
{intro("The expected value is the long-run average result of a random event — each outcome weighted by its probability. This expected value calculator takes up to four outcomes and their probabilities and returns E(X), the variance and the standard deviation, and checks that the probabilities add up to 100%.")}
keywords: [expected value calculator, expected value formula, e(x) calculator, mean of discrete random variable, probability distribution calculator, expected value of a game, variance of random variable]
updated: {D}
variables:
  - {{ id: x1, label: Outcome 1 value, default: {ev_x[0]} }}
  - {{ id: p1, label: Outcome 1 probability, family: percent, unit: '%', default: {ev_p[0]*100:g}, min: 0, max: 1 }}
  - {{ id: x2, label: Outcome 2 value, default: {ev_x[1]} }}
  - {{ id: p2, label: Outcome 2 probability, family: percent, unit: '%', default: {ev_p[1]*100:g}, min: 0, max: 1 }}
  - {{ id: x3, label: Outcome 3 value, default: {ev_x[2]} }}
  - {{ id: p3, label: Outcome 3 probability, family: percent, unit: '%', default: {ev_p[2]*100:g}, min: 0, max: 1 }}
  - {{ id: x4, label: Outcome 4 value, default: {ev_x[3]} }}
  - {{ id: p4, label: Outcome 4 probability, family: percent, unit: '%', default: {ev_p[3]*100:g}, min: 0, max: 1, help: 'Set unused outcomes to probability 0.' }}
  - {{ id: E, label: Expected value E(X) }}
  - {{ id: V, label: Variance, min: 0 }}
  - {{ id: sd, label: Standard deviation, min: 0 }}
  - {{ id: ps, label: Sum of probabilities (should be 100%), family: percent, unit: '%', min: 0 }}
equations:
  - E = x1*p1 + x2*p2 + x3*p3 + x4*p4
  - V = x1^2*p1 + x2^2*p2 + x3^2*p3 + x4^2*p4 - E^2
  - sd = sqrt(V)
  - ps = p1 + p2 + p3 + p4
faq:
  - q: What is the formula for expected value?
    a: E(X) = Σ xᵢ pᵢ — multiply each outcome by its probability and add the results. The probabilities must add up to 1 (100%).
  - q: How do I calculate the variance of a random variable?
    a: Var(X) = Σ xᵢ² pᵢ − E(X)². The standard deviation is the square root of the variance and is in the same units as the outcomes.
  - q: What is the expected value of rolling a die?
    a: (1 + 2 + 3 + 4 + 5 + 6) ÷ 6 = 3.5. The expected value need not be a possible outcome — it is the average over many rolls.
  - q: How is expected value used in decisions?
    a: A bet or project with a positive expected value gains on average over many repetitions. Insurance, lotteries and casino games have a negative expected value for the buyer; risk (the standard deviation) matters too when the stake is large.
related: [statistics/probability, statistics/binomial-probability, math/weighted-average, statistics/standard-deviation]
''', f'''
## How to use the expected value calculator

Enter up to four **outcome values** (gains as positive numbers, losses as negative) and the **probability** of each. Set the probability of unused outcomes to 0. The calculator returns the expected value, variance and standard deviation, and the total of the probabilities so you can check it is 100%.

## Expected value formulas

<p class="formula">E(X) = Σ xᵢ pᵢ &nbsp;·&nbsp; Var(X) = Σ xᵢ² pᵢ − E(X)² &nbsp;·&nbsp; σ = √Var(X)</p>

## Example

A game pays +100 with probability 5%, +20 with 15% and 0 with 50%, and costs −10 with probability 30%:

| Outcome x | Probability p | x × p | x² × p |
|---|---|---|---|
{ev_rows}
- E(X) = 5 + 3 + 0 − 3 = **{ev_E:g}**
- Var(X) = {ev_E2:g} − {ev_E:g}² = **{ev_V:g}**, standard deviation = √{ev_V:g} = **{math.sqrt(ev_V):.2f}**

On average the game pays {ev_E:g} per play, but the large standard deviation shows individual results vary widely.

## Notes

- For a fair die the expected value is {ev_dice:g}.
- Expected value is a [weighted average](/math/weighted-average/) with probabilities as the weights.
''')

# ---------------------------------------------------------------- Birthday paradox
def bday(n_, d=365):
    q = 1.0
    for i in range(n_): q *= (d - i) / d
    return 1 - q
bd_rows = ''.join(f"| {k} | {bday(k)*100:.2f}% | {(1-(364/365)**(k-1))*100:.2f}% |\n" for k in (2, 5, 10, 15, 20, 23, 30, 40, 50, 57, 60, 70, 80, 100))
page('statistics', 'birthday-paradox', f'''
title: Birthday Paradox Calculator (Shared Birthday Probability)
description: Calculate the probability that at least two people in a group share a birthday — the birthday problem — and the chance someone shares your birthday.
category: statistics
{intro("In a room of just 23 people there is a better than even chance that two share a birthday, which surprises most people because there are 365 days. This birthday paradox calculator gives the exact probability of a shared birthday for any group size, and the much smaller chance that someone shares your own birthday.")}
keywords: [birthday paradox calculator, birthday problem calculator, shared birthday probability, probability two people share a birthday, 23 people birthday, birthday probability, collision probability]
updated: {D}
variables:
  - {{ id: n, label: Number of people, default: 23, min: 1, help: 'Exact up to about 120 people; beyond that the probability is effectively 100%.' }}
  - {{ id: d, label: Days in the year, default: 365, min: 1, help: 'Use 365 (ignoring 29 February), or any number of equally likely categories.' }}
  - {{ id: P, label: P(at least two share a birthday), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: Pn, label: P(all birthdays different), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: Py, label: P(someone shares your birthday), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: pairs, label: Number of pairs in the group, min: 0 }}
equations:
  - Pn = nPr(d, n) / d^n
  - P = 1 - Pn
  - Py = 1 - ((d - 1) / d)^(n - 1)
  - pairs = n * (n - 1) / 2
faq:
  - q: Why do only 23 people give a 50% chance?
    a: Because every pair of people is a chance for a match, and 23 people form 253 pairs. The probability that all birthdays differ is 365/365 × 364/365 × … × 343/365 = 49.3%, so a shared birthday has a 50.7% chance.
  - q: What is the formula for the birthday problem?
    a: P(shared) = 1 − 365! ÷ ((365 − n)! × 365ⁿ) = 1 − (365 × 364 × … × (366 − n)) ÷ 365ⁿ.
  - q: How many people do you need for a 99% chance?
    a: 57 people give about 99.0%, and 70 people about 99.9%. With 366 people a match is certain (ignoring 29 February).
  - q: How likely is it that someone shares my birthday?
    a: Much less likely — 1 − (364/365)^(n − 1). In a group of 23 (you plus 22 others) it is only about 5.9%, and you need 253 other people for a 50% chance.
related: [statistics/probability, statistics/permutations, statistics/combinations, statistics/odds-probability]
''', f'''
## How to use the birthday paradox calculator

Enter the **number of people** in the group. The calculator returns the probability that at least two of them share a birthday, the probability that all birthdays are different, the chance that at least one other person shares *your* birthday, and the number of pairs. Change the number of days to apply the same maths to other "collisions", such as hash values or ID numbers.

## Birthday problem formula

<p class="formula">P(all different) = d × (d − 1) × … × (d − n + 1) ÷ dⁿ = ₙP(d, n) ÷ dⁿ</p>

<p class="formula">P(shared) = 1 − P(all different) &nbsp;·&nbsp; P(shares yours) = 1 − ((d − 1) ÷ d)<sup>n−1</sup></p>

## Example

A group of 23 people:

- P(all different) = 365 × 364 × … × 343 ÷ 365²³ = **{(1-bday(23))*100:.2f}%**
- P(at least one shared birthday) = 1 − {(1-bday(23)):.4f} = **{bday(23)*100:.2f}%**
- P(someone shares your birthday) = 1 − (364/365)²² = **{(1-(364/365)**22)*100:.2f}%**
- Pairs = 23 × 22 ÷ 2 = **253**

## Shared-birthday probability by group size

| People | P(any two share) | P(someone shares yours) |
|---|---|---|
{bd_rows}
## Notes

- Real birthdays are not perfectly uniform, which makes a match slightly *more* likely than these figures.
- The counting uses permutations — see the [permutations calculator](/statistics/permutations/).
''')

# ---------------------------------------------------------------- Measurement uncertainty (RSS)
mu_u = (0.05, 0.03, 0.02887, 0.02, 0.0)
mu_names = ('Reference standard (certificate, k = 2 → 0.10 ÷ 2)', 'Repeatability (standard deviation of the mean)', 'Resolution 0.1 (half-width 0.05 ÷ √3)', 'Temperature effect', '—')
mu_uc = math.sqrt(sum(u * u for u in mu_u))
mu_k = 2.0
mu_rows = ''.join(f"| {nm} | {u:.4f} | {u*u:.6f} | {u*u/mu_uc**2*100:.1f}% |\n" for nm, u in zip(mu_names[:4], mu_u[:4]))
divs = [('Normal (from a certificate, k = 2)', 'U ÷ 2', 2), ('Normal (k = 3)', 'U ÷ 3', 3), ('Rectangular (tolerance, resolution)', 'a ÷ √3', math.sqrt(3)), ('Triangular', 'a ÷ √6', math.sqrt(6)), ('U-shaped (sinusoidal, mismatch)', 'a ÷ √2', math.sqrt(2))]
mu_drows = ''.join(f"| {nm} | {f} | {dv:.4f} | {1/dv:.4f} |\n" for nm, f, dv in divs)
page('statistics', 'measurement-uncertainty', f'''
title: Measurement Uncertainty Calculator (RSS Combined & Expanded)
description: Combine standard uncertainties by root-sum-square into a combined standard uncertainty and an expanded uncertainty U = k·uc, as in the GUM method.
category: statistics
{intro("A measurement result is only complete with its uncertainty, built from several independent contributions such as the reference standard, repeatability and resolution. This measurement uncertainty calculator combines up to five standard uncertainties by root-sum-square and applies a coverage factor, the method used in [measurement uncertainty for calibration](ib:measurement-uncertainty-in-calibration) and when checking the [test uncertainty ratio](ib:test-uncertainty-ratio-tur-calibration).")}
keywords: [measurement uncertainty calculator, uncertainty calculator, combined standard uncertainty, expanded uncertainty calculator, root sum square uncertainty, uncertainty budget, gum uncertainty]
updated: {D}
variables:
  - {{ id: u1, label: Standard uncertainty u₁, default: {mu_u[0]:g}, min: 0, help: 'All contributions in the same unit as the measurement, already converted to standard uncertainties (1σ).' }}
  - {{ id: u2, label: Standard uncertainty u₂, default: {mu_u[1]:g}, min: 0 }}
  - {{ id: u3, label: Standard uncertainty u₃, default: {mu_u[2]:g}, min: 0 }}
  - {{ id: u4, label: Standard uncertainty u₄, default: {mu_u[3]:g}, min: 0 }}
  - {{ id: u5, label: Standard uncertainty u₅, default: 0, min: 0, help: 'Leave at 0 if not used.' }}
  - {{ id: k, label: Coverage factor k, default: {mu_k:g}, min: 0, help: 'k = 2 gives about 95% confidence for a normal distribution; k = 3 about 99.7%.' }}
  - {{ id: uc, label: Combined standard uncertainty u_c, min: 0, decimals: 5 }}
  - {{ id: U, label: Expanded uncertainty U = k × u_c, min: 0, decimals: 5 }}
equations:
  - uc = sqrt(u1^2 + u2^2 + u3^2 + u4^2 + u5^2)
  - U = k * uc
faq:
  - q: How do I combine measurement uncertainties?
    a: Convert each contribution to a standard uncertainty (one standard deviation), then add them in quadrature — u_c = √(u₁² + u₂² + …). This root-sum-square rule applies to independent (uncorrelated) contributions with sensitivity coefficients of 1.
  - q: What is the coverage factor k?
    a: It multiplies the combined standard uncertainty to give an interval with a stated confidence. k = 2 gives about 95% for a normal distribution and is the usual choice on calibration certificates.
  - q: How do I convert a tolerance or resolution to a standard uncertainty?
    a: Treat a ± a limit with equal probability across it as a rectangular distribution and divide the half-width by √3. A digital display of resolution r has half-width r/2, so u = r ÷ (2√3).
  - q: Why not just add the uncertainties?
    a: Independent errors rarely all reach their maximum in the same direction at once. Simple addition gives a worst case that overstates the uncertainty; root-sum-square gives a statistically realistic combination.
related: [engineering/calibration-error, engineering/instrument-accuracy, statistics/standard-error, statistics/uniform-distribution]
''', f'''
## How to use the measurement uncertainty calculator

Enter up to five **standard uncertainties** in the same unit as the measurement (convert each one first — see the divisor table below) and the **coverage factor k**. The calculator returns the combined standard uncertainty and the expanded uncertainty U, which is reported as result ± U.

## Measurement uncertainty formula

<p class="formula">u<sub>c</sub> = √(u₁² + u₂² + u₃² + u₄² + u₅²) &nbsp;·&nbsp; U = k × u<sub>c</sub></p>

## Example

Uncertainty budget for a pressure gauge calibration (values in bar):

| Contribution | Standard uncertainty | u² | Share of variance |
|---|---|---|---|
{mu_rows}
- u_c = √(0.05² + 0.03² + {mu_u[2]:.4f}² + 0.02²) = **{mu_uc:.5f} bar**
- U = 2 × {mu_uc:.5f} = **{mu_k*mu_uc:.5f} bar** (≈ ±{mu_k*mu_uc:.2f} bar at about 95% confidence)

The reference standard dominates the budget, so a better standard would reduce the uncertainty most.

## Converting a contribution to a standard uncertainty

| Distribution | Standard uncertainty | Divisor | Multiplier |
|---|---|---|---|
{mu_drows}
## Notes

- If contributions are correlated, or the result depends on inputs through a formula, apply sensitivity coefficients cᵢ and use u_c² = Σ(cᵢ uᵢ)² plus covariance terms.
- Compare the expanded uncertainty with the instrument's tolerance — see the [calibration error calculator](/engineering/calibration-error/).
''')

print('ok')
