import math
from page import page
C='construction'; U='updated: 2026-10-27'

V=4*3*0.1
page(C,'concrete-slab',f'''
title: Concrete Slab Calculator
description: Calculate the concrete volume for a slab, patio or driveway — plus pre-mix bags needed, with a waste allowance.
category: construction
keywords: [concrete calculator, concrete slab, cubic meters of concrete, cubic yards, concrete bags, patio, driveway]
{U}
featured: true
variables:
  - {{ id: L, label: Length, family: length, unit: m, imperialUnit: ft, default: 4, min: 0 }}
  - {{ id: W, label: Width, family: length, unit: m, imperialUnit: ft, default: 3, min: 0 }}
  - {{ id: T, label: Thickness, family: length, unit: mm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: wst, label: Waste allowance, family: percent, unit: '%', default: 10, min: 0, max: 1 }}
  - {{ id: V, label: Concrete volume (incl. waste), family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: yd, label: In cubic yards, min: 0, decimals: 2 }}
  - {{ id: bags, label: 40 kg pre-mix bags (≈0.018 m³ each), min: 0, decimals: 0 }}
equations:
  - V = L * W * T * (1 + wst)
  - yd = V / 0.764554858
  - bags = ceil(V / 0.018)
faq:
  - q: How do I calculate concrete for a slab?
    a: Multiply length × width × thickness (all in metres) to get cubic metres, then add 5–10% for waste and uneven ground.
  - q: How thick should a slab be?
    a: Typically 100 mm (4 in) for patios and paths, 100–150 mm for driveways for cars, and more for heavy vehicles — follow local building rules.
  - q: Should I use bags or ready-mix?
    a: Bags suit small jobs under about 0.5 m³. For larger pours, ready-mix concrete delivered by truck is usually cheaper and more consistent.
related: [construction/concrete-mix, construction/concrete-column, construction/rebar-weight]
''',f'''
## How to use this calculator

Enter the slab's **length**, **width** and **thickness**, and a **waste allowance**. The volume (m³ and cubic yards) and approximate number of 40 kg pre-mix bags are calculated.

## Formula

<p class="formula">Volume = length × width × thickness × (1 + waste)</p>

## Example

A 4 m × 3 m patio, 100 mm thick, 10% waste:

- Volume = 4 × 3 × 0.1 × 1.1 = **{V*1.1:.2f} m³** ({V*1.1/0.764554858:.2f} yd³)
- Pre-mix bags (40 kg) ≈ **{math.ceil(V*1.1/0.018)}**

## Tips

- Compact the sub-base and use formwork to keep thickness even.
- Add reinforcement mesh or rebar for driveways and larger slabs.
- Bag yields vary by brand — check the label (a US 80 lb bag yields about 0.6 ft³).
''')

page(C,'concrete-column',f'''
title: Concrete Column & Footing Calculator (Round)
description: Calculate concrete volume for round columns, piers, post holes and sonotubes.
category: construction
keywords: [concrete column calculator, round column, pier, post hole concrete, sonotube, cylinder concrete]
{U}
variables:
  - {{ id: d, label: Diameter, family: length, unit: mm, imperialUnit: in, default: 300, min: 0 }}
  - {{ id: h, label: Height / depth, family: length, unit: m, imperialUnit: ft, default: 1.2, min: 0 }}
  - {{ id: n, label: Number of columns, default: 6, min: 1 }}
  - {{ id: V, label: Total concrete volume, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: bags, label: 40 kg pre-mix bags, min: 0, decimals: 0 }}
equations:
  - V = pi * (d / 2)^2 * h * n
  - bags = ceil(V * 1.05 / 0.018)
faq:
  - q: How much concrete for a post hole?
    a: Volume = π × radius² × depth. A 300 mm hole 1.2 m deep needs about 0.085 m³ — roughly 5 bags of 40 kg pre-mix.
  - q: Do I subtract the post?
    a: For accuracy, yes — subtract the post's volume below ground. For wooden posts it is usually small.
  - q: Does the bag count include waste?
    a: Yes, 5% extra is added.
related: [construction/concrete-slab, math/cylinder-volume]
''',f'''
## How to use this calculator

Enter the column **diameter**, **height** (or hole depth) and the **number** of columns. The total volume and 40 kg bags (with 5% extra) are calculated.

## Formula

<p class="formula">V = π × (d ÷ 2)² × h × n</p>

## Example

Six piers, 300 mm diameter and 1.2 m deep:

V = π × 0.15² × 1.2 × 6 = **{math.pi*0.15**2*1.2*6:.3f} m³** → about **{math.ceil(math.pi*0.15**2*1.2*6*1.05/0.018)}** bags

## Square columns

For square or rectangular columns, use width × depth × height instead.
''')

page(C,'brick-calculator',f'''
title: Brick Calculator
description: Estimate the number of bricks for a wall from its size, brick dimensions and mortar joint — with waste.
category: construction
keywords: [brick calculator, how many bricks, bricks per square metre, brick wall, mortar joint, bricklaying]
{U}
featured: true
variables:
  - {{ id: L, label: Wall length, family: length, unit: m, imperialUnit: ft, default: 10, min: 0 }}
  - {{ id: H, label: Wall height, family: length, unit: m, imperialUnit: ft, default: 2, min: 0 }}
  - {{ id: open, label: Openings (doors, windows), family: area, unit: m2, imperialUnit: ft2, default: 2, min: 0 }}
  - {{ id: bl, label: Brick length, family: length, unit: mm, imperialUnit: in, default: 215, min: 0 }}
  - {{ id: bh, label: Brick height, family: length, unit: mm, imperialUnit: in, default: 65, min: 0 }}
  - {{ id: j, label: Mortar joint, family: length, unit: mm, imperialUnit: in, default: 10, min: 0 }}
  - {{ id: wst, label: Waste, family: percent, unit: '%', default: 5, min: 0, max: 1 }}
  - {{ id: A, label: Net wall area, family: area, unit: m2, imperialUnit: ft2, min: 0 }}
  - {{ id: per, label: Bricks per m², min: 0, decimals: 1 }}
  - {{ id: n, label: Bricks needed, min: 0, decimals: 0 }}
equations:
  - A = L * H - open
  - per = 1 / ((bl + j) * (bh + j))
  - n = ceil(A * per * (1 + wst))
faq:
  - q: How many bricks are in a square metre?
    a: About 60 standard UK bricks (215 × 65 mm with 10 mm joints) per m² of single-skin wall.
  - q: Is this for a single or double wall?
    a: Single skin (half-brick thick). Double the result for a one-brick-thick wall.
  - q: How much waste should I allow?
    a: 5% is common; use 10% for complex walls with many cuts.
related: [construction/mortar-mix, construction/paint-calculator]
''',f'''
## How to use this calculator

Enter the wall's **length**, **height** and the total area of **openings**. Brick size and joint default to the UK standard (215 × 65 mm, 10 mm joint) — change them for your bricks.

## Formula

<p class="formula">Bricks per m² = 1 ÷ ((brick length + joint) × (brick height + joint))</p>

## Example

A 10 m × 2 m wall with 2 m² of openings:

- Net area = 18 m²
- Bricks per m² = 1 ÷ (0.225 × 0.075) = **{1/(0.225*0.075):.1f}**
- With 5% waste: **{math.ceil(18/(0.225*0.075)*1.05)} bricks**

## Common brick sizes

| Region | Size (mm) |
|---|---|
| UK standard | 215 × 102.5 × 65 |
| India (modular) | 190 × 90 × 90 |
| US modular | 194 × 92 × 57 (7⅝ × 3⅝ × 2¼ in) |
''')

page(C,'paint-calculator',f'''
title: Paint Calculator (Walls & Rooms)
description: Calculate how much paint you need for a room from wall size, doors, windows, number of coats and coverage.
category: construction
keywords: [paint calculator, how much paint, litres of paint, gallons of paint, wall paint, room painting]
{U}
featured: true
variables:
  - {{ id: P, label: Room perimeter (total wall length), family: length, unit: m, imperialUnit: ft, default: 16, min: 0 }}
  - {{ id: H, label: Wall height, family: length, unit: m, imperialUnit: ft, default: 2.7, min: 0 }}
  - {{ id: dw, label: Doors and windows area, family: area, unit: m2, imperialUnit: ft2, default: 5, min: 0 }}
  - {{ id: c, label: Number of coats, default: 2, min: 1 }}
  - {{ id: cov, label: Paint coverage, suffix: m² per litre, default: 10, min: 0.1 }}
  - {{ id: A, label: Paintable area, family: area, unit: m2, imperialUnit: ft2, min: 0 }}
  - {{ id: Lp, label: Paint needed, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
equations:
  - A = P * H - dw
  - Lp = A * c / cov / 1000
faq:
  - q: How much does one litre of paint cover?
    a: Typically 8–12 m² per coat on smooth, primed walls. Check the tin — rough or porous surfaces need more.
  - q: How many coats do I need?
    a: Usually two. A new or very different colour may need a primer plus two coats.
  - q: How do I measure the perimeter?
    a: Add the lengths of all walls. A 5 m × 3 m room has a perimeter of 16 m.
related: [construction/wallpaper, construction/drywall, math/rectangle]
''',f'''
## How to use this calculator

Enter the **total wall length** (perimeter), **wall height**, area of **doors and windows**, the number of **coats** and the paint's **coverage**. The litres (or US gallons) needed are calculated.

## Formula

<p class="formula">Paint = (perimeter × height − openings) × coats ÷ coverage</p>

## Example

A 5 × 3 m room with 2.7 m walls (perimeter 16 m), 5 m² of doors and windows, 2 coats at 10 m²/L:

- Paintable area = 16 × 2.7 − 5 = **{16*2.7-5:.1f} m²**
- Paint = {16*2.7-5:.1f} × 2 ÷ 10 = **{(16*2.7-5)*2/10:.2f} L**

## Ceiling

For the ceiling, add length × width (15 m² here) as a separate calculation — ceiling paint often has different coverage.
''')

page(C,'tile-calculator',f'''
title: Tile Calculator (Floor & Wall)
description: Calculate how many tiles you need for a floor or wall from the area and tile size — with grout gap and waste.
category: construction
keywords: [tile calculator, how many tiles, floor tiles, wall tiles, tiles per square metre, bathroom tiles]
{U}
variables:
  - {{ id: L, label: Area length, family: length, unit: m, imperialUnit: ft, default: 4, min: 0 }}
  - {{ id: W, label: Area width, family: length, unit: m, imperialUnit: ft, default: 3, min: 0 }}
  - {{ id: tl, label: Tile length, family: length, unit: mm, imperialUnit: in, default: 600, min: 0 }}
  - {{ id: tw, label: Tile width, family: length, unit: mm, imperialUnit: in, default: 600, min: 0 }}
  - {{ id: g, label: Grout joint, family: length, unit: mm, imperialUnit: in, default: 3, min: 0 }}
  - {{ id: wst, label: Waste / cuts, family: percent, unit: '%', default: 10, min: 0, max: 1 }}
  - {{ id: A, label: Area, family: area, unit: m2, imperialUnit: ft2, min: 0 }}
  - {{ id: n, label: Tiles needed, min: 0, decimals: 0 }}
equations:
  - A = L * W
  - n = ceil(A / ((tl + g) * (tw + g)) * (1 + wst))
faq:
  - q: How much extra tile should I buy?
    a: About 10% for straight layouts and 15% for diagonal or herringbone patterns. Keep a few spare for future repairs.
  - q: How many 600 × 600 tiles are in a square metre?
    a: About 2.8 tiles (before waste).
  - q: Should I buy tiles by the box?
    a: Yes — round up to whole boxes, and buy from the same batch so the colour matches.
related: [construction/flooring, construction/square-footage, math/rectangle]
''',f'''
## How to use this calculator

Enter the **area dimensions**, **tile size**, **grout joint** and **waste** allowance. The area and number of tiles are calculated.

## Formula

<p class="formula">Tiles = area ÷ ((tile length + joint) × (tile width + joint)) × (1 + waste)</p>

## Example

A 4 × 3 m floor with 600 × 600 mm tiles, 3 mm joints, 10% waste:

- Area = **12 m²**
- Tiles = 12 ÷ (0.603 × 0.603) × 1.1 = **{math.ceil(12/(0.603*0.603)*1.1)} tiles**

## Tiles per m² (before waste)

| Tile size | Tiles per m² |
|---|---|
| 300 × 300 mm | {1/(0.303**2):.1f} |
| 600 × 300 mm | {1/(0.603*0.303):.1f} |
| 600 × 600 mm | {1/(0.603**2):.1f} |
| 800 × 800 mm | {1/(0.803**2):.2f} |
''')

page(C,'flooring',f'''
title: Flooring Calculator (Laminate & Wood)
description: Calculate how many boxes of laminate, vinyl or wood flooring you need — with waste and total cost.
category: construction
keywords: [flooring calculator, laminate flooring, how many boxes, wood flooring, vinyl plank, flooring cost]
{U}
variables:
  - {{ id: A, label: Floor area, family: area, unit: m2, imperialUnit: ft2, default: 20, min: 0 }}
  - {{ id: wst, label: Waste allowance, family: percent, unit: '%', default: 8, min: 0, max: 1 }}
  - {{ id: bx, label: Coverage per box, family: area, unit: m2, imperialUnit: ft2, default: 2.2, min: 0.01 }}
  - {{ id: pb, label: Price per box, family: currency, default: 35, min: 0, decimals: 2 }}
  - {{ id: n, label: Boxes needed, min: 0, decimals: 0 }}
  - {{ id: cost, label: Flooring cost, family: currency, min: 0, decimals: 2 }}
equations:
  - n = ceil(A * (1 + wst) / bx)
  - cost = n * pb
faq:
  - q: How much extra flooring should I buy?
    a: About 5–10% for straight installation, more for diagonal layouts or rooms with many corners.
  - q: Where do I find the coverage per box?
    a: On the box or product page, usually in m² or ft².
  - q: Do I need underlay?
    a: Laminate and many vinyl floors need underlay unless it is pre-attached. Buy it for the same area.
related: [construction/tile-calculator, construction/square-footage]
''',f'''
## How to use this calculator

Enter the **floor area**, **waste** allowance, the **coverage per box** and the **price per box**. The number of boxes (rounded up) and the cost are calculated.

## Example

20 m² with 8% waste, boxes covering 2.2 m² at 35 each:

- Boxes = 20 × 1.08 ÷ 2.2 = **{math.ceil(20*1.08/2.2)}**
- Cost = **{math.ceil(20*1.08/2.2)*35}**

## Measuring tips

- Split L-shaped rooms into rectangles and add the areas.
- Include closets and spaces under doors.
- Let flooring acclimatise in the room for 24–48 hours before laying.
''')

page(C,'drywall',f'''
title: Drywall / Plasterboard Calculator
description: Estimate the number of drywall (plasterboard) sheets for walls and ceilings, with waste.
category: construction
keywords: [drywall calculator, plasterboard calculator, gypsum board, how many sheets, sheetrock, wall boards]
{U}
variables:
  - {{ id: A, label: Wall and ceiling area to cover, family: area, unit: m2, imperialUnit: ft2, default: 60, min: 0 }}
  - id: sa
    label: Sheet size
    default: 2.88
    options:
      - {{ label: 2400 × 1200 mm (2.88 m²), value: 2.88 }}
      - {{ label: 1800 × 900 mm (1.62 m²), value: 1.62 }}
      - {{ label: 4 × 8 ft (32 ft² / 2.97 m²), value: 2.9729 }}
      - {{ label: 4 × 12 ft (48 ft² / 4.46 m²), value: 4.4594 }}
  - {{ id: wst, label: Waste, family: percent, unit: '%', default: 10, min: 0, max: 1 }}
  - {{ id: n, label: Sheets needed, min: 0, decimals: 0 }}
equations:
  - n = ceil(A * (1 + wst) / sa)
faq:
  - q: How many drywall sheets do I need?
    a: Divide the total area by the sheet area and add about 10% for cuts and openings.
  - q: Should I subtract doors and windows?
    a: For large openings, yes. Small windows are often ignored because the offcuts are rarely reusable.
  - q: How many screws per sheet?
    a: Roughly 30–40 screws for a 2400 × 1200 mm sheet on studs at 600 mm centres.
related: [construction/paint-calculator, construction/square-footage]
''',f'''
## How to use this calculator

Enter the total **area** of walls and ceilings and choose the **sheet size**. The number of sheets with waste is calculated.

## Example

60 m² with 2400 × 1200 mm sheets and 10% waste:

60 × 1.1 ÷ 2.88 = **{math.ceil(60*1.1/2.88)} sheets**

## Measuring walls

Wall area = room perimeter × wall height. For a 5 × 4 m room with 2.4 m walls: 18 × 2.4 = 43.2 m², plus the ceiling of 20 m².
''')

page(C,'roof-pitch',f'''
title: Roof Pitch Calculator
description: Calculate roof pitch as an angle, ratio (x:12) and percentage — plus rafter length — from rise and run.
category: construction
keywords: [roof pitch calculator, roof angle, rise over run, rafter length, 4/12 pitch, roof slope]
{U}
featured: true
variables:
  - {{ id: rise, label: Rise, family: length, unit: m, imperialUnit: ft, default: 1.5, min: 0 }}
  - {{ id: run, label: Run (horizontal half-span), family: length, unit: m, imperialUnit: ft, default: 4.5, min: 0 }}
  - {{ id: ang, label: Pitch angle, family: angle, unit: deg }}
  - {{ id: x12, label: Pitch (x in 12), decimals: 2 }}
  - {{ id: pct, label: Slope, family: percent, unit: '%' }}
  - {{ id: raf, label: Rafter length (without overhang), family: length, unit: m, imperialUnit: ft, min: 0 }}
equations:
  - ang = atan(rise / run)
  - x12 = 12 * rise / run
  - pct = rise / run
  - raf = sqrt(rise^2 + run^2)
faq:
  - q: What does a 4/12 roof pitch mean?
    a: The roof rises 4 units for every 12 units of horizontal run — an angle of about 18.4°.
  - q: What is the minimum pitch for shingles?
    a: Asphalt shingles generally need at least 2/12 with special underlayment and 4/12 otherwise. Check the manufacturer's instructions.
  - q: How do I measure rise and run?
    a: Run is half the building width (wall to ridge, horizontally). Rise is the vertical height from the wall plate to the ridge.
related: [math/right-triangle-trig, math/slope, construction/stairs]
''',f'''
## How to use this calculator

Enter the **rise** and **run** to get the pitch angle, the x:12 pitch, the slope percentage and the rafter length. You can also enter an angle to find the rise.

## Formulas

<p class="formula">angle = tan⁻¹(rise ÷ run)   pitch = 12 × rise ÷ run   rafter = √(rise² + run²)</p>

## Example

Rise 1.5 m over a run of 4.5 m:

- Angle = **{math.degrees(math.atan(1.5/4.5)):.1f}°**
- Pitch = **4:12**
- Rafter = **{math.sqrt(1.5**2+4.5**2):.2f} m** (add the overhang)

## Common pitches

| Pitch | Angle |
|---|---|
| 3/12 | {math.degrees(math.atan(3/12)):.1f}° |
| 4/12 | {math.degrees(math.atan(4/12)):.1f}° |
| 6/12 | {math.degrees(math.atan(6/12)):.1f}° |
| 8/12 | {math.degrees(math.atan(8/12)):.1f}° |
| 12/12 | 45° |
''')

H=2.7; n=math.ceil(H/0.18-1e-9); rh=H/n
page(C,'stairs',f'''
title: Stair Calculator (Risers & Treads)
description: Calculate the number of steps, riser height, total run and stair angle from the floor-to-floor height.
category: construction
keywords: [stair calculator, stair rise and run, number of steps, riser height, tread depth, staircase design]
{U}
variables:
  - {{ id: H, label: Total rise (floor to floor), family: length, unit: m, imperialUnit: ft, default: 2.7, min: 0 }}
  - {{ id: tr, label: Target max riser height, family: length, unit: mm, imperialUnit: in, default: 180, min: 0.01 }}
  - {{ id: td, label: Tread depth (going), family: length, unit: mm, imperialUnit: in, default: 270, min: 0 }}
  - {{ id: n, label: Number of risers, min: 0, decimals: 0 }}
  - {{ id: rh, label: Actual riser height, family: length, unit: mm, imperialUnit: in, min: 0 }}
  - {{ id: run, label: Total run (horizontal length), family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: ang, label: Stair angle, family: angle, unit: deg }}
equations:
  - n = ceil(H / tr)
  - rh = H / n
  - run = (n - 1) * td
  - ang = atan(rh / td)
faq:
  - q: What is a comfortable riser height?
    a: About 150–180 mm (6–7 in), with treads around 250–300 mm. Many codes cap risers at about 190–200 mm for homes.
  - q: Why is the number of treads one less than risers?
    a: The top step is the upper floor itself, so there is one fewer tread than risers.
  - q: What is the 2R + G rule?
    a: Twice the riser plus the going should be about 550–700 mm (often around 630 mm) for a comfortable stride.
related: [construction/roof-pitch, math/right-triangle-trig]
''',f'''
## How to use this calculator

Enter the **total rise**, your **maximum riser height** and the **tread depth**. The number of risers, actual riser height, total run and angle are calculated.

## Formulas

<p class="formula">risers = ⌈rise ÷ max riser⌉   riser = rise ÷ risers   run = (risers − 1) × tread</p>

## Example

Floor-to-floor 2.7 m, max riser 180 mm, tread 270 mm:

- Risers = **{n}**, each **{rh*1000:.0f} mm**
- Total run = {n-1} × 270 = **{(n-1)*0.27:.2f} m**
- Angle = **{math.degrees(math.atan(rh/0.27)):.1f}°**
- Check: 2R + G = {2*rh*1000+270:.0f} mm ✓

Always check your local building code for limits on riser, going, headroom and handrails.
''')

page(C,'gravel',f'''
title: Gravel & Aggregate Calculator
description: Calculate how much gravel, sand or crushed stone you need in m³, tonnes and cubic yards for a given area and depth.
category: construction
keywords: [gravel calculator, how much gravel, tonnes of gravel, crushed stone, aggregate, sand calculator, cubic yards]
{U}
variables:
  - {{ id: L, label: Length, family: length, unit: m, imperialUnit: ft, default: 10, min: 0 }}
  - {{ id: W, label: Width, family: length, unit: m, imperialUnit: ft, default: 3, min: 0 }}
  - {{ id: D, label: Depth, family: length, unit: mm, imperialUnit: in, default: 75, min: 0 }}
  - id: rho
    label: Material
    default: 1600
    options:
      - {{ label: Gravel / crushed stone (~1,600 kg/m³), value: 1600 }}
      - {{ label: Sand, dry (~1,550 kg/m³), value: 1550 }}
      - {{ label: Pea gravel (~1,700 kg/m³), value: 1700 }}
      - {{ label: Topsoil (~1,300 kg/m³), value: 1300 }}
      - {{ label: Mulch / bark (~400 kg/m³), value: 400 }}
  - {{ id: V, label: Volume, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: yd, label: Cubic yards, min: 0, decimals: 2 }}
  - {{ id: t, label: Weight, family: mass, unit: t, imperialUnit: lb, min: 0 }}
equations:
  - V = L * W * D
  - yd = V / 0.764554858
  - t = V * rho
faq:
  - q: How deep should a gravel driveway be?
    a: Typically 100–150 mm (4–6 in) of compacted base plus a 50 mm top layer. Paths need around 50–75 mm.
  - q: How many tonnes is a cubic metre of gravel?
    a: About 1.5–1.7 tonnes, depending on the stone and moisture.
  - q: Should I order extra?
    a: Yes, about 5–10%, because gravel settles and compacts.
related: [construction/excavation, construction/concrete-slab]
''',f'''
## How to use this calculator

Enter the **length**, **width** and **depth**, and choose the **material**. The volume and weight are calculated.

## Example

A 10 × 3 m path, 75 mm deep:

- Volume = 10 × 3 × 0.075 = **{10*3*0.075:.2f} m³** ({10*3*0.075/0.764554858:.2f} yd³)
- Gravel weight ≈ {10*3*0.075:.2f} × 1.6 = **{10*3*0.075*1.6:.2f} tonnes**

## Typical depths

| Use | Depth |
|---|---|
| Decorative garden cover | 30–50 mm |
| Footpath | 50–75 mm |
| Driveway (total) | 150–200 mm |
| Mulch for beds | 50–75 mm |
''')

page(C,'rebar-weight',f'''
title: Rebar Weight Calculator
description: Calculate the weight of steel reinforcement bars (rebar) from diameter, length and quantity.
category: construction
keywords: [rebar weight, steel bar weight, d2/162, tmt bar weight, reinforcement steel, kg per metre]
{U}
featured: true
variables:
  - id: d
    label: Bar diameter
    default: 12
    options:
      - {{ label: 6 mm, value: 6 }}
      - {{ label: 8 mm, value: 8 }}
      - {{ label: 10 mm, value: 10 }}
      - {{ label: 12 mm, value: 12 }}
      - {{ label: 16 mm, value: 16 }}
      - {{ label: 20 mm, value: 20 }}
      - {{ label: 25 mm, value: 25 }}
      - {{ label: 32 mm, value: 32 }}
  - {{ id: L, label: Length of each bar, family: length, unit: m, imperialUnit: ft, default: 12, min: 0 }}
  - {{ id: n, label: Number of bars, default: 10, min: 0 }}
  - {{ id: wpm, label: Weight per metre, suffix: kg/m, min: 0, decimals: 3 }}
  - {{ id: W, label: Total weight, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - wpm = d^2 / 162.2
  - W = wpm * L * n
faq:
  - q: What is the formula for rebar weight?
    a: Weight (kg/m) = d² ÷ 162.2, where d is the diameter in mm. It comes from steel's density of 7,850 kg/m³.
  - q: How much does a 12 m, 12 mm bar weigh?
    a: About 0.888 kg/m × 12 m = 10.65 kg.
  - q: Is TMT bar weight the same?
    a: Yes — TMT and other deformed bars are rated by nominal diameter and use the same formula.
related: [construction/steel-plate-weight, construction/concrete-slab]
''',f'''
## How to use this calculator

Choose the **bar diameter**, then enter the **length** and **number of bars**. The weight per metre and total weight are calculated.

## Formula

<p class="formula">kg/m = d² ÷ 162.2</p>

## Example

10 bars of 12 mm, each 12 m long:

- Weight per metre = 144 ÷ 162.2 = **{144/162.2:.3f} kg/m**
- Total = {144/162.2:.3f} × 12 × 10 = **{144/162.2*120:.1f} kg**

## Weight per metre table

| Diameter | kg/m | 12 m bar |
|---|---|---|
{chr(10).join(f"| {d} mm | {d*d/162.2:.3f} | {d*d/162.2*12:.2f} kg |" for d in (6,8,10,12,16,20,25,32))}
''')

page(C,'steel-plate-weight',f'''
title: Steel Plate Weight Calculator
description: Calculate the weight of steel, stainless steel or aluminium plates and sheets from their dimensions.
category: construction
keywords: [steel plate weight, sheet metal weight, metal weight calculator, ms plate weight, aluminium sheet weight]
{U}
variables:
  - id: rho
    label: Material
    default: 7850
    options:
      - {{ label: Mild / carbon steel (7,850 kg/m³), value: 7850 }}
      - {{ label: Stainless steel (8,000 kg/m³), value: 8000 }}
      - {{ label: Aluminium (2,700 kg/m³), value: 2700 }}
      - {{ label: Copper (8,960 kg/m³), value: 8960 }}
      - {{ label: Brass (8,500 kg/m³), value: 8500 }}
  - {{ id: L, label: Length, family: length, unit: mm, imperialUnit: in, default: 2000, min: 0 }}
  - {{ id: W, label: Width, family: length, unit: mm, imperialUnit: in, default: 1000, min: 0 }}
  - {{ id: t, label: Thickness, family: length, unit: mm, imperialUnit: in, default: 6, min: 0 }}
  - {{ id: n, label: Quantity, default: 1, min: 0 }}
  - {{ id: M, label: Weight, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - M = rho * L * W * t * n
faq:
  - q: How do I calculate steel plate weight?
    a: Weight = length × width × thickness × density. Steel is about 7,850 kg/m³, so 1 m² of 1 mm plate weighs 7.85 kg.
  - q: Quick rule for mild steel plate?
    a: 7.85 kg per m² for each mm of thickness.
  - q: Is stainless steel heavier?
    a: Slightly — about 2% more than carbon steel.
related: [construction/rebar-weight, physics/density]
''',f'''
## How to use this calculator

Choose the **material** and enter the **length**, **width**, **thickness** and **quantity**. The weight appears in kg or lb.

## Formula

<p class="formula">Weight = length × width × thickness × density</p>

## Example

A 2,000 × 1,000 × 6 mm mild steel plate:

Weight = 2 × 1 × 0.006 × 7,850 = **{2*1*0.006*7850:.1f} kg**

## Quick rule

Mild steel plate weighs **7.85 kg per m² per mm** of thickness. Aluminium weighs about 2.7 kg per m² per mm.
''')

dry=1*1.33; xs=4
page(C,'mortar-mix',f'''
title: Mortar Calculator (Cement & Sand)
description: Calculate cement bags and sand needed for a given volume of mortar at any mix ratio, such as 1:4 or 1:6.
category: construction
keywords: [mortar calculator, cement sand ratio, plaster mix, cement bags, 1:4 mortar, 1:6 mortar]
{U}
variables:
  - {{ id: Vw, label: Wet mortar volume, family: volume, unit: m3, imperialUnit: ft3, default: 1, min: 0 }}
  - {{ id: s, label: Sand parts per 1 part cement, default: 4, min: 0 }}
  - {{ id: Vd, label: Dry volume (×1.33), family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: Vc, label: Cement volume, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: bags, label: Cement bags (50 kg), min: 0, decimals: 1 }}
  - {{ id: Vs, label: Sand volume, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
equations:
  - Vd = Vw * 1.33
  - Vc = Vd / (1 + s)
  - bags = Vc * 1440 / 50
  - Vs = Vc * s
faq:
  - q: Why multiply by 1.33?
    a: Dry materials shrink when water is added and voids fill, so about 33% more dry volume is needed than the final wet volume.
  - q: Which mix ratio should I use?
    a: 1:3 to 1:4 for strong work such as external plaster and load-bearing brickwork; 1:5 to 1:6 for internal walls. Follow your engineer's specification.
  - q: How much does a cement bag hold?
    a: A 50 kg bag of cement occupies about 0.0347 m³ (cement bulk density about 1,440 kg/m³).
related: [construction/concrete-mix, construction/brick-calculator]
''',f'''
## How to use this calculator

Enter the **wet mortar volume** and the **sand ratio** (4 for 1:4). The dry volume, cement bags and sand volume are calculated.

## Formulas

<p class="formula">Dry volume = wet × 1.33<br/>Cement = dry ÷ (1 + sand parts)   Sand = cement × sand parts</p>

## Example — 1 m³ of 1:4 mortar

- Dry volume = 1.33 m³
- Cement = 1.33 ÷ 5 = 0.266 m³ = **{1.33/5*1440/50:.1f} bags** of 50 kg
- Sand = 0.266 × 4 = **{1.33/5*4:.3f} m³**
''')

page(C,'concrete-mix',f'''
title: Concrete Mix Calculator (Cement, Sand, Aggregate)
description: Calculate cement bags, sand and coarse aggregate for nominal concrete mixes like M15, M20 and M25.
category: construction
keywords: [concrete mix calculator, m20 mix ratio, cement sand aggregate, concrete material calculation, 1:1.5:3]
{U}
variables:
  - {{ id: V, label: Wet concrete volume, family: volume, unit: m3, imperialUnit: ft3, default: 1, min: 0 }}
  - id: mix
    label: 'Mix (cement : sand : aggregate)'
    default: 5.5
    options:
      - {{ label: 'M10 — 1 : 3 : 6 (total 10 parts)', value: 10 }}
      - {{ label: 'M15 — 1 : 2 : 4 (total 7 parts)', value: 7 }}
      - {{ label: 'M20 — 1 : 1.5 : 3 (total 5.5 parts)', value: 5.5 }}
      - {{ label: 'M25 — 1 : 1 : 2 (total 4 parts)', value: 4 }}
  - {{ id: Vd, label: Dry volume (×1.54), family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: bags, label: Cement bags (50 kg), min: 0, decimals: 1 }}
  - {{ id: sand, label: Sand, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: agg, label: Coarse aggregate, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
equations:
  - Vd = V * 1.54
  - bags = Vd / mix * 1440 / 50
  - sand = Vd / mix * (mix - 1) / 3
  - agg = Vd / mix * (mix - 1) * 2 / 3
faq:
  - q: What is the M20 mix ratio?
    a: For nominal mixes, M20 is 1 : 1.5 : 3 (cement : sand : aggregate). Design mixes for important structures are proportioned by a lab.
  - q: Why multiply by 1.54?
    a: To allow for voids and shrinkage — dry ingredients occupy about 54% more volume than the finished concrete.
  - q: How much water is needed?
    a: Typically a water–cement ratio of about 0.45–0.55 by weight for these mixes. Too much water weakens concrete.
related: [construction/concrete-slab, construction/mortar-mix, construction/rebar-weight]
''',f'''
## How to use this calculator

Enter the **wet volume** and choose the **mix**. The dry volume, cement bags, sand and coarse aggregate are calculated.

This calculator assumes the sand-to-aggregate ratio is 1 : 2, as in all the listed nominal mixes.

## Example — 1 m³ of M20 (1 : 1.5 : 3)

- Dry volume = 1.54 m³
- Cement = 1.54 ÷ 5.5 = 0.28 m³ = **{1.54/5.5*1440/50:.1f} bags**
- Sand = 0.28 × 1.5 = **{1.54/5.5*1.5:.2f} m³**
- Aggregate = 0.28 × 3 = **{1.54/5.5*3:.2f} m³**

Nominal mixes follow common Indian practice (IS 456). For structural work, always follow your structural engineer's design.
''')

page(C,'wallpaper',f'''
title: Wallpaper Calculator
description: Estimate how many rolls of wallpaper you need from room perimeter, wall height and roll size — including pattern repeat waste.
category: construction
keywords: [wallpaper calculator, how many rolls of wallpaper, wallpaper rolls, room wallpaper, pattern repeat]
{U}
variables:
  - {{ id: P, label: Wall length to cover, family: length, unit: m, imperialUnit: ft, default: 14, min: 0 }}
  - {{ id: H, label: Wall height, family: length, unit: m, imperialUnit: ft, default: 2.5, min: 0 }}
  - {{ id: rw, label: Roll width, family: length, unit: cm, imperialUnit: in, default: 53, min: 0.01 }}
  - {{ id: rl, label: Roll length, family: length, unit: m, imperialUnit: ft, default: 10, min: 0.01 }}
  - {{ id: rep, label: Pattern repeat, family: length, unit: cm, imperialUnit: in, default: 0, min: 0 }}
  - {{ id: drops, label: Drops (strips) needed, min: 0, decimals: 0 }}
  - {{ id: perRoll, label: Drops per roll, min: 0, decimals: 0 }}
  - {{ id: rolls, label: Rolls needed, min: 0, decimals: 0 }}
equations:
  - drops = ceil(P / rw)
  - perRoll = floor(rl / (H + rep + 0.1))
  - rolls = ceil(drops / perRoll)
faq:
  - q: What size is a standard wallpaper roll?
    a: In Europe and the UK, usually 53 cm × 10.05 m. US rolls vary; check the label.
  - q: What is a pattern repeat?
    a: The vertical distance before the pattern repeats. Larger repeats waste more paper when matching strips.
  - q: Should I subtract doors and windows?
    a: Usually not — the offcuts rarely fit elsewhere, and spare paper is useful for repairs.
related: [construction/paint-calculator, construction/drywall]
''',f'''
## How to use this calculator

Enter the **wall length** to cover, **wall height**, **roll width and length**, and the **pattern repeat** (0 for plain paper). The number of strips, strips per roll and rolls needed are calculated. 10 cm per strip is allowed for trimming.

## Example

14 m of wall, 2.5 m high, standard 53 cm × 10 m rolls, no repeat:

- Drops = 14 ÷ 0.53 → **{math.ceil(14/0.53)}**
- Drops per roll = 10 ÷ 2.6 → **{math.floor(10/2.6)}**
- Rolls = **{math.ceil(math.ceil(14/0.53)/math.floor(10/2.6))}**

Buy all rolls from the same batch number so the colour matches.
''')

page(C,'fence',f'''
title: Fence Calculator (Posts & Panels)
description: Calculate the number of fence posts, panels or rails and the concrete needed for any fence length.
category: construction
keywords: [fence calculator, fence posts, fence panels, how many posts, fencing materials, post spacing]
{U}
variables:
  - {{ id: L, label: Fence length, family: length, unit: m, imperialUnit: ft, default: 30, min: 0 }}
  - {{ id: sp, label: Post spacing (panel width), family: length, unit: m, imperialUnit: ft, default: 1.83, min: 0.01 }}
  - {{ id: rails, label: Rails per section, default: 3, min: 0 }}
  - {{ id: pn, label: Panels / sections, min: 0, decimals: 0 }}
  - {{ id: po, label: Posts needed, min: 0, decimals: 0 }}
  - {{ id: rl, label: Rails needed, min: 0, decimals: 0 }}
equations:
  - pn = ceil(L / sp)
  - po = pn + 1
  - rl = pn * rails
faq:
  - q: How many fence posts do I need?
    a: Divide the fence length by the post spacing, round up, and add one for the end post.
  - q: What spacing should posts have?
    a: Standard panels are about 1.83 m (6 ft) wide; post-and-rail fences often use 2–2.4 m (8 ft).
  - q: How deep should posts go?
    a: A common rule is about a quarter to a third of the post's above-ground height, typically 600 mm for a 1.8 m fence.
related: [construction/concrete-column, construction/board-feet]
''',f'''
## How to use this calculator

Enter the **fence length**, **post spacing** and **rails per section**. The number of panels, posts and rails is calculated. Add extra posts for corners and gates.

## Example

30 m of fence with 1.83 m panels and 3 rails per section:

- Panels = **{math.ceil(30/1.83)}**
- Posts = **{math.ceil(30/1.83)+1}**
- Rails = **{math.ceil(30/1.83)*3}**

## Concrete for posts

A post hole of 300 mm diameter and 600 mm deep takes about 0.04 m³ of concrete. Use the [column calculator](/construction/concrete-column/) for exact amounts.
''')

page(C,'board-feet',f'''
title: Board Feet Calculator (Lumber)
description: Calculate board feet of lumber from thickness, width and length — plus total cost.
category: construction
keywords: [board feet calculator, lumber calculator, board foot, timber volume, hardwood pricing, bf]
{U}
variables:
  - {{ id: t, label: Thickness, suffix: in, default: 2, min: 0 }}
  - {{ id: w, label: Width, suffix: in, default: 6, min: 0 }}
  - {{ id: l, label: Length, suffix: ft, default: 8, min: 0 }}
  - {{ id: q, label: Number of pieces, default: 10, min: 0 }}
  - {{ id: pr, label: Price per board foot, family: currency, default: 4.5, min: 0, decimals: 2 }}
  - {{ id: bf, label: Total board feet, min: 0 }}
  - {{ id: cost, label: Total cost, family: currency, min: 0, decimals: 2 }}
equations:
  - bf = t * w * l / 12 * q
  - cost = bf * pr
faq:
  - q: What is a board foot?
    a: A volume of wood 1 inch thick, 12 inches wide and 1 foot long (144 cubic inches).
  - q: Do I use nominal or actual size?
    a: Hardwood is usually priced on nominal rough-sawn thickness (such as 4/4 = 1 in). Check how your supplier measures.
  - q: How many board feet in a cubic metre?
    a: About 423.8 board feet.
related: [construction/fence, conversion/volume-converter]
''',f'''
## How to use this calculator

Enter **thickness** and **width** in inches, **length** in feet, the **quantity** and the **price per board foot**. Total board feet and cost are calculated.

## Formula

<p class="formula">Board feet = thickness (in) × width (in) × length (ft) ÷ 12</p>

## Example

Ten 2 × 6 in boards, 8 ft long, at 4.50 per board foot:

- Board feet = 2 × 6 × 8 ÷ 12 × 10 = **{2*6*8/12*10:.0f}**
- Cost = **{2*6*8/12*10*4.5:.2f}**
''')

page(C,'square-footage',f'''
title: Square Footage & Cost Calculator
description: Calculate the area of a room or space in ft² and m² and the total cost at a price per unit area.
category: construction
keywords: [square footage calculator, sq ft calculator, area cost, price per square foot, room area, carpet cost]
{U}
variables:
  - {{ id: L, label: Length, family: length, unit: ft, default: 12, min: 0 }}
  - {{ id: W, label: Width, family: length, unit: ft, default: 15, min: 0 }}
  - {{ id: A, label: Area, family: area, unit: ft2, min: 0 }}
  - {{ id: pr, label: Price per square foot, family: currency, default: 3.5, min: 0, decimals: 2 }}
  - {{ id: cost, label: Total cost, family: currency, min: 0, decimals: 2 }}
equations:
  - A = L * W
  - cost = A / 0.09290304 * pr
faq:
  - q: How do I calculate square footage?
    a: Multiply length by width in feet. A 12 × 15 ft room is 180 ft².
  - q: How do I handle irregular rooms?
    a: Split the space into rectangles, calculate each one, and add them up.
  - q: How do I convert square feet to square metres?
    a: Multiply by 0.0929. Switch the Area unit to m² to see it directly.
related: [conversion/sq-ft-to-sq-m, construction/flooring, construction/tile-calculator]
''',f'''
## How to use this calculator

Enter the **length** and **width** (in feet, metres or any unit) and the **price per square foot**. The area and total cost are calculated.

## Example

A 12 × 15 ft room at 3.50 per ft²:

- Area = **180 ft²** ({180*0.09290304:.1f} m²)
- Cost = **630.00**

## Tip

Add 5–15% to material quantities for cutting waste, depending on the material and layout.
''')

page(C,'excavation',f'''
title: Excavation & Dirt Calculator
description: Calculate excavation volume in m³ and cubic yards, including soil swell, and the number of truckloads needed.
category: construction
keywords: [excavation calculator, dirt calculator, cubic yards of dirt, soil volume, truckloads, swell factor]
{U}
variables:
  - {{ id: L, label: Length, family: length, unit: m, imperialUnit: ft, default: 10, min: 0 }}
  - {{ id: W, label: Width, family: length, unit: m, imperialUnit: ft, default: 8, min: 0 }}
  - {{ id: D, label: Depth, family: length, unit: m, imperialUnit: ft, default: 1.5, min: 0 }}
  - {{ id: sw, label: Swell factor, family: percent, unit: '%', default: 25, min: 0, max: 2 }}
  - {{ id: cap, label: Truck capacity, family: volume, unit: m3, imperialUnit: ft3, default: 10, min: 0.01 }}
  - {{ id: Vb, label: Bank (in-ground) volume, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: Vl, label: Loose volume to haul, family: volume, unit: m3, imperialUnit: ft3, min: 0 }}
  - {{ id: yd, label: Loose cubic yards, min: 0, decimals: 1 }}
  - {{ id: trucks, label: Truckloads, min: 0, decimals: 0 }}
equations:
  - Vb = L * W * D
  - Vl = Vb * (1 + sw)
  - yd = Vl / 0.764554858
  - trucks = ceil(Vl / cap)
faq:
  - q: What is swell factor?
    a: Excavated soil loosens and takes up more space than it did in the ground — typically 10–40% more depending on soil type.
  - q: What swell factor should I use?
    a: Around 10–15% for sand, 20–30% for common earth and clay, and 40–60% for rock.
  - q: How big is a dump truck?
    a: Common sizes carry about 6–15 m³ (8–20 yd³). Check with your haulier.
related: [construction/gravel, construction/concrete-slab]
''',f'''
## How to use this calculator

Enter the **length**, **width** and **depth** of the excavation, the soil's **swell factor** and the **truck capacity**. You get the in-ground volume, loose volume and number of truckloads.

## Example

A 10 × 8 m basement dug 1.5 m deep in common earth (25% swell), 10 m³ trucks:

- Bank volume = **{10*8*1.5:.0f} m³**
- Loose volume = **{10*8*1.5*1.25:.0f} m³** ({10*8*1.5*1.25/0.764554858:.1f} yd³)
- Truckloads = **{math.ceil(10*8*1.5*1.25/10)}**
''')

page(C,'rectangular-tank',f'''
title: Rectangular Tank Volume Calculator
description: Calculate the capacity of a rectangular or square water tank, sump or overhead tank in litres, m³ and gallons.
category: construction
keywords: [tank volume calculator, rectangular tank capacity, water tank litres, sump capacity, overhead tank size]
{U}
variables:
  - {{ id: L, label: Inside length, family: length, unit: m, imperialUnit: ft, default: 2, min: 0 }}
  - {{ id: W, label: Inside width, family: length, unit: m, imperialUnit: ft, default: 1.5, min: 0 }}
  - {{ id: H, label: Water depth (or inside height), family: length, unit: m, imperialUnit: ft, default: 1.2, min: 0 }}
  - {{ id: V, label: Capacity, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: M, label: Weight of water, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - V = L * W * H
  - M = V * 1000
faq:
  - q: How do I calculate tank capacity in litres?
    a: Multiply length × width × height in metres to get m³, then multiply by 1,000.
  - q: How much does the water weigh?
    a: About 1 kg per litre — a 3,600-litre tank holds about 3.6 tonnes, so the base or roof slab must be designed for it.
  - q: How do I size a tank for a household?
    a: Estimate daily use (often 100–150 litres per person) and multiply by the days of storage you want.
related: [engineering/horizontal-tank-volume, math/cylinder-volume, conversion/volume-converter]
''',f'''
## How to use this calculator

Enter the tank's **inside length**, **width** and **water depth**. The capacity and the weight of the water are calculated. Find the water depth for a given volume by typing the volume instead.

## Example

A 2 × 1.5 m tank filled to 1.2 m:

V = 2 × 1.5 × 1.2 = 3.6 m³ = **3,600 litres** ({3600/3.785411784:.0f} US gal), weighing about **3.6 tonnes**.

For round tanks use the [cylinder calculator](/math/cylinder-volume/), and for horizontal cylindrical tanks the [horizontal tank calculator](/engineering/horizontal-tank-volume/).
''')
print('construction ok')
