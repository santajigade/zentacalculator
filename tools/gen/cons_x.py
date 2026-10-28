import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
pi = math.pi

expand('construction/board-feet', '''
## Board feet for common lumber sizes (per piece)

| Nominal size | 8 ft | 10 ft | 12 ft | 16 ft |
|---|---|---|---|---|
''' + ''.join(f"| {t}×{w} | {t*w*8/12:.2f} | {t*w*10/12:.2f} | {t*w*12/12:.2f} | {t*w*16/12:.2f} |\n" for t, w in [(1, 4), (1, 6), (2, 4), (2, 6), (2, 8), (2, 10), (2, 12), (4, 4), (6, 6)]) + '''
## Nominal vs actual size

Board feet are calculated from **nominal** sizes for softwood framing lumber. A “2×4” actually measures about 1½ × 3½ inches after drying and planing. Hardwoods are usually sold by rough thickness in quarters: 4/4 (1 inch), 5/4, 6/4, 8/4.

## Board feet to cubic measure

- 1 board foot = 144 cubic inches = 1/12 cubic foot
- 1 board foot ≈ 0.00236 m³ (2.36 litres)
- 1 m³ ≈ 424 board feet

## Linear feet vs board feet

Some yards sell dimensional lumber by the **linear foot** (length only) and hardwood by the **board foot** (volume). To compare prices, convert: price per board foot = price per linear foot ÷ (thickness × width ÷ 12).

## Add for waste

Allow 10–15% extra for defects, knots and offcuts, more for high-grade furniture projects where you need clear stock.
''', [
 ('How many board feet is a 2×4×8?', '2 × 4 × 8 ÷ 12 = 5.33 board feet (nominal).'),
 ('How many board feet are in a cubic metre?', 'About 424 board feet.'),
])

expand('construction/brick-calculator', '''
## Bricks per square metre by size

| Brick size (mm) | Joint | Bricks per m² (half-brick wall) |
|---|---|---|
''' + ''.join(f"| {l} × {h} | 10 mm | {1/((l+10)/1000*(h+10)/1000):.1f} |\n" for l, h in [(215, 65), (230, 75), (190, 90), (190, 57), (290, 90)]) + '''
## Wall thickness

| Wall type | Thickness | Bricks per m² (215 × 65) |
|---|---|---|
| Half-brick (stretcher bond) | about 102.5 mm | 59 |
| One-brick (230 mm, English bond) | about 215 mm | 118 |

A full-brick wall uses about twice as many bricks as a half-brick wall of the same face area.

## Mortar needed

As a rough guide, a half-brick wall uses about 0.02–0.025 m³ of mortar per square metre. For 20 m² of wall, plan on about 0.4–0.5 m³ of mortar. See the [mortar mix calculator](/construction/mortar-mix/) for cement and sand.

## Bricks per day

An experienced bricklayer typically lays 300–500 bricks a day on straightforward walls, fewer on detailed work. Use this to estimate labour time.

## Ordering tips

- Order all bricks for a job from the same batch for consistent colour.
- Keep a few spare for future repairs.
- Check pallet sizes (often 400–500 bricks) and round up to whole pallets if that is cheaper.
''', [
 ('How many bricks are in 1 m² of wall?', 'About 60 standard 215 × 65 mm bricks for a half-brick wall with 10 mm joints.'),
 ('How many bricks for a 10 m × 2 m wall?', 'About 1,190 bricks plus 5–10% waste for a half-brick wall, before subtracting doors and windows.'),
], before='## Common brick sizes')

expand('construction/concrete-column', '''
## Concrete per metre of column height

| Diameter / size | Volume per metre | 40 kg bags per metre |
|---|---|---|
''' + ''.join(f"| Ø {d} mm round | {pi*(d/2000)**2:.4f} m³ | {math.ceil(pi*(d/2000)**2*1.05/0.018)} |\n" for d in [150, 200, 250, 300, 400, 450, 600]) + ''.join(f"| {s} × {s} mm square | {(s/1000)**2:.4f} m³ | {math.ceil((s/1000)**2*1.05/0.018)} |\n" for s in [230, 300, 400, 450]) + '''
## Sonotubes and footings

Round forms (cardboard tubes) are common for deck and porch footings. Add the volume of any spread footing at the base: a 600 × 600 × 300 mm pad is 0.108 m³.

## Reinforcement

Structural columns need steel reinforcement designed by an engineer. Check minimum cover (often 40 mm for columns) and use the [rebar weight calculator](/construction/rebar-weight/) to estimate steel.

## Pouring tips

- Pour in layers and vibrate or rod each one to remove air pockets.
- Avoid dropping concrete more than about 1.5 m freely to prevent segregation.
- Keep exposed tops damp for at least 7 days while curing.
''', [
 ('How much concrete is in a 300 mm × 3 m column?', 'π × 0.15² × 3 = 0.212 m³.'),
 ('How many bags for a 200 mm post hole 1 m deep?', 'About 0.031 m³, or 2 bags of 40 kg pre-mix (plus waste).'),
], before='## Square columns')

expand('construction/concrete-mix', '''
## Nominal mix ratios by grade

| Grade | Mix (cement : sand : aggregate) | Typical use |
|---|---|---|
| M10 | 1 : 3 : 6 | Levelling course, PCC |
| M15 | 1 : 2 : 4 | Floors, pathways |
| M20 | 1 : 1.5 : 3 | RCC slabs, beams, columns (small buildings) |
| M25 | 1 : 1 : 2 | Heavier RCC work |

The number after M is the characteristic compressive strength in N/mm² at 28 days. Above M20, design mixes based on lab tests are recommended.

## Materials for 1 m³ by grade

| Grade | Cement bags (50 kg) | Sand (m³) | Aggregate (m³) |
|---|---|---|---|
''' + ''.join(f"| {g} | {1.54/sum(r)*1440/50:.1f} | {1.54/sum(r)*r[1]:.3f} | {1.54/sum(r)*r[2]:.3f} |\n" for g, r in [('M10', (1, 3, 6)), ('M15', (1, 2, 4)), ('M20', (1, 1.5, 3)), ('M25', (1, 1, 2))]) + '''
Values use the 1.54 dry-volume factor and a cement density of 1,440 kg/m³. Add 2–5% for wastage.

## Water–cement ratio

Strength depends heavily on the water–cement ratio. Typical values are 0.45–0.55 for structural concrete. Adding extra water to make concrete easier to place reduces strength and durability. Use a plasticiser instead.

## Curing

Concrete gains about 70% of its 28-day strength in 7 days if kept moist. Cure by ponding, wet hessian or curing compound for at least 7 days (10–14 days in hot, dry weather).
''', [
 ('How many cement bags are needed for 1 m³ of M20 concrete?', 'About 8 bags of 50 kg for a nominal 1 : 1.5 : 3 mix.'),
 ('Why multiply by 1.54?', 'Dry materials shrink when water is added and voids fill, so about 1.54 m³ of dry materials make 1 m³ of wet concrete.'),
])

expand('construction/concrete-slab', '''
## Concrete for common slab sizes

| Slab | 100 mm thick | 150 mm thick |
|---|---|---|
''' + ''.join(f"| {l} × {w} m | {l*w*0.1:.2f} m³ | {l*w*0.15:.2f} m³ |\n" for l, w in [(2, 2), (3, 3), (4, 3), (5, 4), (6, 6), (10, 5)]) + '''
## Typical slab thicknesses

| Use | Thickness |
|---|---|
| Garden shed base, paths | 75–100 mm |
| Patio | 100 mm |
| Garage floor, driveway (cars) | 100–150 mm |
| House floor slab | 100–150 mm (plus sub-base) |
| Heavy vehicles | 150–200 mm or more, engineered |

## Ready-mix or bags?

- **Under about 0.5 m³**: bagged pre-mix is practical.
- **0.5–1 m³**: consider mixing on site with a mixer.
- **Over 1 m³**: ready-mixed concrete delivered by truck is usually cheaper and more consistent. Check the minimum order and short-load charges.

## Sub-base and reinforcement

A well-compacted hardcore or crushed-stone sub-base (often 100–150 mm) prevents cracking from settlement. Many slabs include steel mesh or fibre reinforcement and a damp-proof membrane. Use the [gravel calculator](/construction/gravel/) for sub-base material.

## Cubic yards (US)

Ready-mix in the US is ordered by the cubic yard. 1 m³ = 1.308 yd³. A 10 × 10 ft slab 4 inches thick needs 1.23 yd³.
''', [
 ('How much concrete do I need for a 10 × 10 ft slab?', 'At 4 inches thick, about 1.23 cubic yards (0.94 m³), plus waste.'),
 ('How thick should a concrete patio be?', 'Typically 100 mm (4 inches) on a compacted sub-base.'),
], before='## Tips')

expand('construction/drywall', '''
## Sheets needed by room size

Walls only, 2.4 m ceiling, 1.2 × 2.4 m sheets (2.88 m²), 10% waste:

| Room | Wall area (approx.) | Sheets |
|---|---|---|
''' + ''.join(f"| {l} × {w} m | {2*(l+w)*2.4:.1f} m² | {math.ceil(2*(l+w)*2.4*1.1/2.88)} |\n" for l, w in [(3, 3), (3, 4), (4, 4), (4, 5), (5, 6)]) + '''
Add the ceiling area (length × width) if you are boarding that too.

## Standard sheet sizes

| Size | Area |
|---|---|
| 1200 × 2400 mm | 2.88 m² |
| 1200 × 2700 mm | 3.24 m² |
| 4 × 8 ft | 32 ft² |
| 4 × 12 ft | 48 ft² |

Longer sheets reduce joints on tall walls and ceilings.

## Other materials

| Material | Rough quantity per 100 m² of board |
|---|---|
| Screws | about 1,000–1,200 (at 300 mm centres) |
| Joint tape | about 120–140 m |
| Joint compound | about 40–50 kg (ready-mixed) |

## Board types

- **Standard**: dry areas.
- **Moisture-resistant** (often green): bathrooms and kitchens.
- **Fire-rated** (often pink or red): garages, escape routes and where codes require.
- **Sound-rated**: party walls and bedrooms.
''', [
 ('How many sheets of drywall do I need for a 12 × 12 room?', 'With 8 ft walls, the walls are about 384 sq ft — 12 sheets of 4 × 8 ft plus 10% waste, or 13–14 sheets. Add 5 sheets for the ceiling.'),
 ('Should I subtract doors and windows?', 'Subtract large openings, but many installers leave small windows in the calculation to cover waste and offcuts.'),
], before='## Measuring walls')

expand('construction/excavation', '''
## Swell factors by soil type

| Material | Typical swell |
|---|---|
| Sand and gravel | 10–15% |
| Topsoil | 20–30% |
| Common earth | 20–30% |
| Clay | 30–40% |
| Broken rock | 50–75% |

Excavated soil takes up more room in a truck than in the ground. When compacted as fill, it may shrink to less than its original bank volume.

## Sloped sides

Deep trenches often need sloped or stepped sides for safety. For a trench with sloped sides, average the top and bottom widths:

<p class="formula">V = L × D × (top width + bottom width) ÷ 2</p>

A trench 20 m long, 2 m deep, 1 m wide at the bottom and 3 m at the top holds 20 × 2 × 2 = **80 m³**.

## Truck capacities

| Vehicle | Typical capacity |
|---|---|
| Small tipper | 3–5 m³ |
| Standard tipper / dump truck | 6–10 m³ |
| Large articulated dump truck | 15–25 m³ |

Weight limits often control before volume does, especially with wet clay or rock.

## Safety

Trenches deeper than about 1.2–1.5 m generally need shoring, sloping or trench boxes. Check for underground services before digging and follow local regulations.
''', [
 ('What is swell factor?', 'The percentage increase in volume when soil is dug up and loosened. 25% swell means 10 m³ in the ground becomes 12.5 m³ loose.'),
 ('How many truckloads to remove 120 m³ of soil?', 'With 25% swell, 150 m³ loose. At 8 m³ per truck, that is 19 loads.'),
])

expand('construction/fence', '''
## Posts and panels for common lengths

1.8 m (6 ft) panels:

| Fence length | Panels | Posts | Rails (3 per section) |
|---|---|---|---|
''' + ''.join(f"| {L} m | {math.ceil(L/1.8)} | {math.ceil(L/1.8)+1} | {math.ceil(L/1.8)*3} |\n" for L in [10, 20, 30, 50, 100]) + '''
Add one extra post for each corner and gate, and two posts for each gate opening.

## Post depth

A common rule is to bury **one-third** of the post's total length, or at least 600 mm. For a 1.8 m fence, use 2.4 m posts set about 600 mm deep. Use deeper holes in soft ground or exposed, windy sites.

## Concrete per post

A 300 mm diameter hole 600 mm deep, minus a 100 × 100 mm post, needs about 0.036 m³ — roughly four 20 kg bags of post-mix (each makes about 0.01 m³). See the [concrete column calculator](/construction/concrete-column/).

## Picket fences

For a picket fence, also count pickets:

<p class="formula">Pickets = fence length ÷ (picket width + gap)</p>

30 m of 90 mm pickets with 50 mm gaps needs about 30,000 ÷ 140 = **215 pickets**.

## Before you build

- Check boundary lines and local height limits.
- Locate underground services before digging.
- Ask neighbours if the fence is on a shared boundary.
''', [
 ('How many posts do I need for a 30 m fence?', 'With 1.8 m panels, 17 panels and 18 posts, plus extras for corners and gates.'),
 ('How far apart should fence posts be?', 'Usually 1.8–2.4 m (6–8 ft), depending on panel size and wind exposure.'),
], before='## Concrete for posts')

expand('construction/flooring', '''
## Waste allowance by layout

| Layout | Typical waste |
|---|---|
| Straight lay, simple rectangle | 5–8% |
| Room with alcoves and doorways | 10% |
| Diagonal lay | 12–15% |
| Herringbone or chevron | 15–20% |

## Underlay and trims

- **Underlay** covers the same area as the floor; rolls are often 10–15 m².
- **Skirting or scotia** trim: measure the room perimeter minus doorways.
- **Expansion gap**: leave about 8–10 mm around the edges for laminate and engineered wood.

## Acclimatising

Wood and laminate flooring should rest in the room for 24–48 hours before fitting so it adjusts to the room's temperature and humidity. This reduces gaps and buckling later.

## Cost per square metre

Total cost per m² = (boxes × price + underlay + trims + adhesive) ÷ floor area. Include fitting labour if you are comparing installed prices.

## Square feet and square metres

Many boxes list coverage in square feet. 1 m² = 10.764 ft². Use the [area converter](/conversion/area-converter/) if the box and your measurements use different units.
''', [
 ('How much extra flooring should I buy?', 'Usually 8–10% for a standard room, more for diagonal or herringbone patterns.'),
 ('How many boxes of laminate for 20 m²?', 'With 2.2 m² per box and 8% waste, 21.6 ÷ 2.2 = 10 boxes.'),
], before='## Measuring tips')

expand('construction/gravel', '''
## Gravel density and coverage

| Material | Density (t/m³) | Coverage of 1 tonne at 50 mm deep |
|---|---|---|
''' + ''.join(f"| {n} | {r} | {1/r/0.05:.1f} m² |\n" for n, r in [('Pea gravel', 1.6), ('Crushed stone (20 mm)', 1.5), ('Sand', 1.6), ('Hardcore / MOT Type 1', 2.1), ('Decorative slate', 1.4), ('Topsoil', 1.3)]) + '''
## Bulk bags

A typical bulk bag holds about 0.6–0.8 m³, or roughly 0.8–1 tonne of gravel. Check your supplier's bag size.

## Compaction

Sub-base materials like crushed stone compact by 10–20% when rolled. Order extra for compacted layers, or measure the depth after compaction.

## Layers for a driveway

| Layer | Depth |
|---|---|
| Geotextile membrane | — |
| Compacted sub-base (crushed stone) | 100–150 mm |
| Binding layer (smaller stone) | 50 mm |
| Top layer (decorative gravel) | 30–50 mm |

Too thick a top layer is hard to walk and drive on; 30–50 mm is usually enough.

## Cubic yards and tons (US)

1 cubic yard of gravel weighs roughly 1.3–1.5 short tons. A 10 × 10 ft area at 3 inches deep needs 0.93 yd³.
''', [
 ('How much does 1 m³ of gravel weigh?', 'About 1.5–1.7 tonnes, depending on the type and how wet it is.'),
 ('How much gravel do I need for a path 10 m × 1 m?', 'At 50 mm deep, 0.5 m³ — about 0.8 tonnes.'),
], before='## Typical depths')

expand('construction/mortar-mix', '''
## Mortar ratios by use

| Mix (cement : sand) | Typical use |
|---|---|
| 1 : 3 | Strong work, below ground, ceramic tile beds |
| 1 : 4 | General brickwork, external plaster |
| 1 : 5 | Standard brickwork above ground |
| 1 : 6 | Internal plaster, non-load-bearing blockwork |

Lime or a plasticiser is often added to improve workability and reduce cracking.

## Materials for 1 m³ of wet mortar

| Mix | Cement bags (50 kg) | Sand (m³) |
|---|---|---|
''' + ''.join(f"| 1 : {s} | {1.33/(1+s)*1440/50:.1f} | {1.33/(1+s)*s:.3f} |\n" for s in [3, 4, 5, 6]) + '''
## Plastering quantities

For plaster, multiply the area by thickness to get the wet volume:

- 12 mm internal plaster over 100 m² = 1.2 m³ wet mortar
- 20 mm external plaster over 50 m² = 1.0 m³ wet mortar

Add 10–15% for uneven surfaces and wastage.

## Working time

Cement mortar should be used within about 1–2 hours of mixing. Do not add water to mortar that has started to stiffen.
''', [
 ('How many bags of cement for 1 m³ of 1:4 mortar?', 'About 7.7 bags of 50 kg.'),
 ('Why multiply wet volume by 1.33?', 'Dry sand and cement occupy more volume than the finished mortar because voids fill with water and fine particles.'),
])

expand('construction/paint-calculator', '''
## Paint for common rooms

2.7 m walls, 2 coats, 10 m² per litre, 4 m² of doors and windows:

| Room | Perimeter | Paint needed |
|---|---|---|
''' + ''.join(f"| {l} × {w} m | {2*(l+w)} m | {(2*(l+w)*2.7-4)*2/10:.1f} L |\n" for l, w in [(3, 3), (3, 4), (4, 4), (4, 5), (5, 6)]) + '''
## Coverage by surface

| Surface | Typical coverage per coat |
|---|---|
| Smooth, previously painted wall | 10–14 m²/L |
| New plaster (mist coat) | 6–8 m²/L |
| Rough render or brick | 4–6 m²/L |
| Wood (gloss/satin) | 12–16 m²/L |

Check the coverage on the tin — it varies by brand and finish.

## Primers and colour changes

- New plaster needs a diluted mist coat first.
- Going from dark to light colours often needs a primer or an extra coat.
- Bare wood and metal need suitable primers.

## Exterior walls

For a house exterior, measure each wall's width × height, subtract windows and doors, and add up. Rough masonry uses much more paint than smooth surfaces.
''', [
 ('How much paint do I need for a 12 × 12 ft room?', 'For 8 ft walls (about 384 sq ft minus openings) and two coats, about 2 US gallons.'),
 ('How many coats of paint do I need?', 'Usually two for good coverage. Three may be needed for large colour changes or porous surfaces.'),
], before='## Ceiling')

expand('construction/rebar-weight', '''
## Bars per tonne

| Diameter | kg/m | Metres per tonne | 12 m bars per tonne |
|---|---|---|---|
''' + ''.join(f"| {d} mm | {d*d/162.2:.3f} | {1000/(d*d/162.2):,.0f} | {1000/(d*d/162.2)/12:.1f} |\n" for d in [8, 10, 12, 16, 20, 25, 32]) + '''
## Where the formula comes from

Steel density is 7,850 kg/m³. For a 1 m bar of diameter d (mm):

<p class="formula">Weight = π × (d ÷ 2000)² × 1 × 7,850 = d² ÷ 162.2</p>

## US bar sizes

| US bar | Diameter | lb/ft |
|---|---|---|
| #3 | 3/8 in (9.5 mm) | 0.376 |
| #4 | 1/2 in (12.7 mm) | 0.668 |
| #5 | 5/8 in (15.9 mm) | 1.043 |
| #6 | 3/4 in (19.1 mm) | 1.502 |
| #8 | 1 in (25.4 mm) | 2.670 |

The number is the diameter in eighths of an inch.

## Estimating steel for a slab

Typical residential RCC uses roughly 80–120 kg of steel per m³ of concrete for slabs and 150–250 kg/m³ for columns and beams. Use these only for rough budgets — the structural design gives exact quantities.

## Laps and wastage

Add for lap lengths (often 40–50 × bar diameter), bends and offcuts. Allow 3–5% wastage for cutting.
''', [
 ('What is the weight of 12 mm rebar per metre?', '0.888 kg/m.'),
 ('How many 12 m bars of 10 mm make a tonne?', 'About 135 bars.'),
], before='## Weight per metre table')

expand('construction/rectangular-tank', '''
## Capacity of common tank sizes

| Inside dimensions (L × W × H) | Capacity |
|---|---|
''' + ''.join(f"| {l} × {w} × {h} m | {l*w*h*1000:,.0f} L ({l*w*h*264.172:,.0f} US gal) |\n" for l, w, h in [(1, 1, 1), (2, 1, 1), (2, 1.5, 1.2), (2, 2, 1.5), (3, 2, 1.5), (4, 3, 2)]) + '''
## Usable vs total capacity

The usable volume is less than the full volume because:

- An **overflow** sits below the top edge.
- An **outlet** sits above the floor to avoid drawing sediment.
- A **freeboard** of 100–300 mm is often left at the top.

Measure the depth from the outlet to the overflow for the usable volume.

## Water demand

| Use | Typical daily use |
|---|---|
| Per person (domestic, India urban guidelines) | 135 L |
| Per person (many developed countries) | 150–300 L |
| Garden watering | 5–10 L per m² |

A family of four using 135 L each needs 540 L a day. A 2,000 L tank stores about 3.7 days of supply.

## Weight and structure

Water weighs 1 kg per litre. A 2,000 L tank weighs 2 tonnes when full, plus the tank itself. Rooftop tanks need a structural check.

## Level sensors

For automatic control, the level is directly proportional to volume in a rectangular tank, so a linear level sensor scaled to the tank height gives volume directly.
''', [
 ('How many litres is a 1 m × 1 m × 1 m tank?', '1,000 litres.'),
 ('How do I find the litres in a tank from cm?', 'Multiply length × width × height in cm and divide by 1,000.'),
])

expand('construction/roof-pitch', '''
## Pitch conversions

| Pitch (x in 12) | Angle | Slope % | Rafter factor |
|---|---|---|---|
''' + ''.join(f"| {x}/12 | {math.degrees(math.atan(x/12)):.1f}° | {x/12*100:.1f}% | {math.hypot(1,x/12):.3f} |\n" for x in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12]) + '''
Multiply the run by the **rafter factor** to get the rafter length (without overhang).

## Roof area from plan area

Roof surface area = plan area × rafter factor. A 10 × 8 m house with a 6/12 pitch has a roof area of about 80 × 1.118 = **89.4 m²**, plus overhangs.

## Minimum pitches for roofing materials

| Material | Typical minimum pitch |
|---|---|
| Asphalt shingles | 2/12 to 4/12 (with underlayment rules) |
| Clay or concrete tiles | about 4/12 (varies by tile) |
| Slate | about 4/12 to 6/12 |
| Metal sheets | 1/12 or lower for some profiles |
| Membrane (flat roofs) | about 1/4 in 12 for drainage |

Always follow the manufacturer's minimum pitch.

## Snow and rain

Steeper roofs shed rain and snow faster, but cost more and catch more wind. Flat roofs need a slight fall (often 1:40 to 1:80) to drain.
''', [
 ('What angle is a 6/12 roof?', '26.57°.'),
 ('How do I measure roof pitch?', 'Measure 12 inches horizontally with a level and the vertical rise at that point. The rise in inches gives the pitch in 12.'),
], before='## Common pitches')

expand('construction/square-footage', '''
## Area of common shapes

| Shape | Formula |
|---|---|
| Rectangle | length × width |
| Triangle | base × height ÷ 2 |
| Circle | π × radius² |
| Trapezoid | (side a + side b) ÷ 2 × height |
| L-shape | Split into two rectangles and add |

## Square feet for rooms

| Room | Size (ft) | Area (sq ft) | Area (m²) |
|---|---|---|---|
''' + ''.join(f"| {n} | {l} × {w} | {l*w} | {l*w*0.09290304:.1f} |\n" for n, l, w in [('Small bedroom', 10, 10), ('Bedroom', 12, 12), ('Master bedroom', 14, 16), ('Living room', 16, 20), ('Garage (single)', 12, 20), ('Garage (double)', 20, 20)]) + '''
## Feet and inches

Convert inches to decimal feet before multiplying: 12 ft 6 in = 12.5 ft. A room 12 ft 6 in × 10 ft 3 in is 12.5 × 10.25 = **128.1 sq ft**.

## Price per square foot

Total cost = area × price per sq ft. For materials, add 5–15% for waste. For property, price per square foot depends on whether the area is carpet, built-up or super built-up — see the [sq ft to sq m converter](/conversion/sq-ft-to-sq-m/).
''', [
 ('How many square feet is a 12 × 12 room?', '144 sq ft.'),
 ('How do I calculate square footage of an irregular room?', 'Split it into rectangles and triangles, calculate each area and add them.'),
], before='## Tip')

expand('construction/stairs', '''
## Comfortable stair dimensions

A common comfort rule is:

<p class="formula">2 × riser + going ≈ 600–630 mm</p>

| Riser | Going (tread) | 2R + G |
|---|---|---|
| 150 mm | 300 mm | 600 |
| 170 mm | 280 mm | 620 |
| 180 mm | 260 mm | 620 |
| 190 mm | 250 mm | 630 |

## Typical building code limits

| | UK (private stairs) | US (IRC residential) |
|---|---|---|
| Max riser | 220 mm | 7¾ in (197 mm) |
| Min going / tread | 220 mm | 10 in (254 mm) |
| Max pitch | 42° | — |
| Min headroom | 2.0 m | 6 ft 8 in (2.03 m) |

Codes vary — check your local building regulations.

## Number of risers for common floor heights

| Floor-to-floor height | Risers (≤ 180 mm) | Actual riser |
|---|---|---|
''' + ''.join(f"| {h} mm | {math.ceil(h/180)} | {h/math.ceil(h/180):.1f} mm |\n" for h in [2600, 2800, 3000, 3200, 3500]) + '''
## Treads vs risers

A straight flight always has **one fewer tread than risers**, because the top step is the upper floor itself. The calculator's total run already accounts for this.
''', [
 ('How many steps for a 3 m floor height?', 'With a 180 mm maximum riser, 17 risers of about 176 mm and 16 treads.'),
 ('What is a comfortable stair angle?', 'About 30–37°. Steeper than 42° is not allowed for normal stairs in many codes.'),
])

expand('construction/steel-plate-weight', '''
## Weight per square metre by thickness

| Thickness | Steel (7,850 kg/m³) | Stainless (7,930) | Aluminium (2,700) |
|---|---|---|---|
''' + ''.join(f"| {t} mm | {7.85*t:.2f} kg/m² | {7.93*t:.2f} kg/m² | {2.7*t:.2f} kg/m² |\n" for t in [1, 2, 3, 5, 6, 8, 10, 12, 16, 20, 25]) + '''
## Standard plate sizes

| Size | Area |
|---|---|
| 1,250 × 2,500 mm | 3.125 m² |
| 1,500 × 3,000 mm | 4.5 m² |
| 2,000 × 6,000 mm | 12 m² |
| 4 × 8 ft | 2.97 m² |

A 6 mm steel plate 1,500 × 3,000 mm weighs 4.5 × 47.1 = **212 kg**.

## Chequer (tread) plate

Chequer plate weighs more than its nominal thickness suggests because of the raised pattern — typically about 0.5–1 mm extra equivalent thickness. Check the supplier's table.

## Holes and cut-outs

Subtract cut-outs: a 100 mm hole in 10 mm steel removes π × 0.05² × 0.01 × 7,850 = 0.62 kg.
''', [
 ('How much does a 10 mm steel plate weigh per square metre?', '78.5 kg/m².'),
 ('How much does a 4 × 8 sheet of 1/4 inch steel weigh?', 'About 327 lb (148 kg).'),
], before='## Quick rule')

expand('construction/tile-calculator', '''
## Tiles per m² for common sizes (3 mm joint)

| Tile | Tiles per m² | Tiles for 10 m² + 10% |
|---|---|---|
''' + ''.join(f"| {a} × {b} mm | {1/((a+3)/1000*(b+3)/1000):.1f} | {math.ceil(10/((a+3)/1000*(b+3)/1000)*1.1)} |\n" for a, b in [(100, 100), (200, 200), (300, 300), (300, 600), (400, 400), (600, 600), (600, 1200), (800, 800)]) + '''
## Adhesive and grout

| Material | Rough quantity |
|---|---|
| Tile adhesive (6 mm notched trowel) | 3–4 kg per m² |
| Tile adhesive (10–12 mm trowel, large tiles) | 5–6 kg per m² |
| Grout | 0.2–1 kg per m², depending on tile size and joint width |

Larger tiles with thin joints need less grout.

## Wall tiles

For walls, calculate each wall separately: width × height minus windows and doors. Tiles often stop at a set height, such as 1.2 m or full height in showers.

## Layout tips

- Start from the centre of the room so cut tiles at the edges are equal.
- Avoid slivers less than half a tile wide at visible edges.
- Buy all tiles from the same batch (shade and calibre) and keep a few spares for repairs.
''', [
 ('How many 600 × 600 tiles in 1 m²?', 'About 2.75 tiles with 3 mm joints, before waste.'),
 ('How much extra tile should I buy?', '10% for straight layouts, 15% for diagonal or complex rooms.'),
], before='## Tiles per m² (before waste)')

expand('construction/wallpaper', '''
## Rolls needed by room

Standard 0.53 × 10 m rolls, 2.5 m walls, no pattern repeat:

| Room perimeter | Drops | Rolls |
|---|---|---|
''' + ''.join(f"| {p} m | {math.ceil(p/0.53)} | {math.ceil(math.ceil(p/0.53)/math.floor(10/(2.5+0.1)))} |\n" for p in [10, 12, 14, 16, 18, 20]) + '''
## Pattern repeat

A pattern repeat means each drop must be cut longer so the pattern lines up. Large repeats (over 50 cm) can waste a lot of paper — sometimes a whole drop per roll.

| Match type | What it means |
|---|---|
| Free match | No pattern alignment, least waste |
| Straight match | Pattern aligns horizontally across drops |
| Offset (drop) match | Pattern shifts by half a repeat on alternate drops |

## Roll sizes

| Type | Typical size |
|---|---|
| Standard European roll | 0.53 × 10.05 m |
| US double roll | about 0.53 × 10 m (sold as two single rolls) |
| Wide roll | 0.70 × 10 m |

## Windows and doors

Most decorators do **not** subtract windows and doors from small rooms, because partial drops above and below them still use up paper. For large openings, subtract one drop per full-width door.

## Batch numbers

Buy all rolls with the same batch number, as colours can vary between print runs. Buy one extra roll for repairs.
''', [
 ('How many rolls of wallpaper for a 4 × 4 m room?', 'With 2.5 m walls and no repeat, about 31 drops — 11 standard rolls at 3 drops per roll.'),
 ('How many drops are in a roll?', 'For 2.5 m walls, a 10 m roll gives 3 full drops (plus a short offcut).'),
])

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/construction/*.mdx')):
    c = 'construction/' + os.path.basename(p)[:-4]; print(c, words(c))
