"""Part C expansion (2026-11-15): 20 thin pages from tools/upgrade-backlog.txt, brought to the
api-gravity standard: two-paragraph intros, worked examples computed from the calculator defaults,
practice notes, computed reference tables, common mistakes and new FAQs. Assembled from four
sections below. Edits are applied in place by inplace.edit (slug, category, variables, equations and
related ids are asserted unchanged). Run once on the original files."""

# ======================================================================= SECTION 1
"""Part C expand (2026-11-15), slice 1: kinematic-viscosity, spherical-tank-volume, availability-mtbf,
manometer, pressure-to-head. Worked examples use each page's default inputs; all numbers computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-15'
g = 9.80665
pi = math.pi

# ---------------------------------------------------------------- Kinematic viscosity
W_DATA = [(0, 1.792, 999.8), (10, 1.306, 999.7), (20, 1.002, 998.2), (30, 0.797, 995.7), (40, 0.653, 992.2),
          (50, 0.547, 988.0), (60, 0.467, 983.2), (80, 0.355, 971.8), (100, 0.282, 958.4)]
kv_w = ''.join(f"| {t} °C | {mu:.3f} | {rho:.1f} | {mu/rho*1000:.4f} |\n" for t, mu, rho in W_DATA)
kv_vg = ''
for vg in (10, 22, 32, 46, 68, 100, 150, 220, 320, 460):
    kv_vg += f"| ISO VG {vg} | {vg} cSt | {vg*0.9:g} to {vg*1.1:g} cSt | {vg*0.87:.1f} cP |\n"
mu0, rho0 = 1.002, 998.2
nu0 = mu0 / 1000 / rho0 * 1e6
oil_nu, oil_rho = 46, 870
oil_mu = oil_nu * oil_rho / 1000

edit('engineering/kinematic-viscosity', date=U, phrase='kinematic viscosity calculator',
     intro=("Dynamic viscosity measures a fluid's resistance to shear, and kinematic viscosity is that resistance divided by density. "
            "This kinematic viscosity calculator converts between the two with ν = μ ÷ ρ, so a value in cP becomes cSt and back.\n\n"
            "Lubrication engineers use it to match ISO VG oil grades, and process and instrument engineers use it for Reynolds numbers, "
            "pipe friction and flow meter sizing. See [viscosity measurement explained](https://www.instrumentationblog.in/viscosity-measurement-explained/)."),
     before='## Dynamic and kinematic viscosity of common fluids', min_words=0,
     body_add=f'''
## Converting cSt back to cP

The calculator works in both directions. An ISO VG {oil_nu} hydraulic oil has a kinematic viscosity of {oil_nu} cSt at 40 °C and a density of about {oil_rho} kg/m³ at that temperature:

- μ = ν × ρ = {oil_nu} × 10⁻⁶ × {oil_rho} = {oil_mu/1000:.4f} Pa·s = **{oil_mu:.1f} cP**

For quick work, cP = cSt × SG, so a fluid lighter than water always has fewer cP than cSt.

## How viscosity is measured

- **Capillary (glass U-tube) viscometers** such as Ubbelohde or Cannon-Fenske tubes time how long a fixed volume takes to drain under gravity. Because gravity drives the flow, the result is kinematic viscosity, ν = K × t, where K is the tube constant. This is the ASTM D445 and ISO 3104 method used for oil grades.
- **Rotational viscometers** (Brookfield type) measure the torque to turn a spindle in the sample, which gives dynamic viscosity in cP or mPa·s. They are used for paints, slurries and food products.
- **Inline process viscometers** (vibrating rod or torsional resonator) report the product of viscosity and density, so they are often paired with a density meter to give both μ and ν.

## Water viscosity by temperature

Viscosity of water falls by a factor of six between freezing and boiling, while density changes by only 4%:

| Temperature | μ (cP) | ρ (kg/m³) | ν (cSt) |
|---|---|---|---|
{kv_w}
## ISO viscosity grades at 40 °C

Each ISO VG grade is a midpoint kinematic viscosity with a ±10% band. The cP column assumes a typical mineral oil density of 870 kg/m³ at 40 °C:

| Grade | Midpoint | Allowed range | Approx. μ |
|---|---|---|---|
{kv_vg}
''')
edit('engineering/kinematic-viscosity', date=U,
     body_add='''
## Common mistakes

- **Mixing temperatures.** Taking μ at 20 °C from one table and ρ at 40 °C from another gives a wrong ν. Both values must be at the same temperature.
- **Dividing by SG when the density is in kg/m³.** cSt = cP ÷ SG only works with SG or g/cm³. With kg/m³ you must also multiply by 1,000.
- **Using cSt where a formula expects m²/s.** In the Reynolds number Re = vD ÷ ν, 1 cSt is 10⁻⁶ m²/s. Forgetting the factor makes Re a million times too small.
- **Comparing oil grades at different temperatures.** ISO VG is defined at 40 °C; SAE engine oil grades also refer to 100 °C. A VG 46 oil is far thicker than 46 cSt at room temperature.
- **Treating non-Newtonian fluids as one number.** Slurries, polymers and paints change viscosity with shear rate, so a single cP value only holds at the shear rate it was measured at.
''',
     faq_add=[("What is the kinematic viscosity of ISO VG 46 oil?",
               "46 cSt at 40 °C by definition, with an allowed range of 41.4 to 50.6 cSt. At a density of about 870 kg/m³ that is roughly 40 cP. At 100 °C a typical VG 46 mineral oil is only about 6.8 cSt."),
              ("Why does air have a higher kinematic viscosity than water?",
               "Air's dynamic viscosity (0.018 cP) is about 55 times lower than water's, but its density is about 830 times lower. Dividing by the tiny density gives about 15 cSt for air against 1 cSt for water.")])

# ---------------------------------------------------------------- Spherical tank
def cap(D, h):
    return pi * h * h * (1.5 * D - h) / 3
def level_for(D, frac):
    lo, hi, Vt = 0.0, D, pi * D ** 3 / 6
    for _ in range(100):
        m = (lo + hi) / 2
        if cap(D, m) < frac * Vt: lo = m
        else: hi = m
    return (lo + hi) / 2
sD, sh = 10.0, 4.0
sV, sVt = cap(sD, sh), pi * sD ** 3 / 6
rho_lpg = 500
sp_rows = ''
for D in (8, 10, 12, 14, 16, 18, 20):
    Vt = pi * D ** 3 / 6
    sp_rows += f"| {D} m | {Vt:,.0f} m³ | {level_for(D, 0.85):.2f} m ({level_for(D, 0.85)/D*100:.1f}%) | {Vt*0.85*rho_lpg/1000:,.0f} t |\n"
h85 = level_for(10, 0.85)

edit('engineering/spherical-tank-volume', date=U, phrase='spherical tank volume calculator',
     intro=("Storage spheres for LPG, ammonia and other pressurised liquids hold more or less than a simple level percentage suggests, because the cross-section changes with height. "
            "This spherical tank volume calculator uses the spherical-cap formula to turn a liquid level into a volume.\n\n"
            "Terminal operators, instrument engineers and inventory accountants use it to build level-to-volume tables, set high-level alarms and check fill limits. "
            "See [LPG level measurement in bullets and spheres](https://www.instrumentationblog.in/lpg-level-measurement-bullet-sphere/)."),
     body_add=f'''
## From volume to mass

Inventory is usually reported in tonnes. In the worked example, if the 4 m of liquid is propane at about {rho_lpg} kg/m³ (its density near 20 °C), the stock is {sV:.2f} × {rho_lpg} = **{sV*rho_lpg/1000:.1f} t**. Use the density at the measured liquid temperature: liquid propane gets noticeably lighter as it warms, so the same volume holds less mass on a hot afternoon.

## How level is measured on spheres

- **Radar or servo gauges** on a still pipe on the top of the sphere measure the liquid surface directly. Because the vessel is under pressure, the gauge sits on a pressure-rated nozzle or behind a ball valve.
- **Differential pressure transmitters** need the vapour pressure on the low side, and the vapour density matters at high pressure. See the [DP level range calculator](/engineering/dp-level-range/).
- **Strapping tables** from a calibration survey replace the ideal formula for custody transfer, because real spheres are slightly out of round and have legs, nozzles and internal pipes.

## Sphere sizes and the 85% fill level

Because the top of a sphere is narrow, 85% of the volume is reached well before 85% of the height. Masses assume LPG at {rho_lpg} kg/m³:

| Diameter | Capacity | Level at 85% volume | LPG at 85% |
|---|---|---|---|
{sp_rows}
## Common mistakes

- **Treating level percent as volume percent.** At 40% level a sphere is only {sV/sVt*100:.1f}% full; at 90% level it is already 97.2% full.
- **Using the outside diameter.** Shell plates on large spheres can be 40 to 60 mm thick, which changes the capacity by around 2 to 4% on a 10 m sphere.
- **Measuring level from the wrong datum.** The formula needs the depth from the lowest inside point. Gauges are often referenced to a nozzle or flange, so add the offset first.
- **Forgetting the bottom fittings.** Liquid trapped in the drain sump and outlet piping below the sphere is not part of the cap volume.
- **Setting alarms by level instead of volume.** A high-level alarm for 85% fill must be set at about {h85/10*100:.0f}% of the height on any sphere, not at 85%.
''',
     faq_add=[("At what level is a sphere 85% full?",
               f"At {h85/10*100:.1f}% of its inside diameter, whatever the size. For a 10 m sphere that is {h85:.2f} m of liquid. The ratio is the same for every sphere because the shape scales.")])

# ---------------------------------------------------------------- Availability
amtbf, amttr, atm = 87600.0, 8.0, 8760.0
aA = amtbf / (amtbf + amttr)
adt = (1 - aA) * 8760
alam = 8760 / amtbf
aR = math.exp(-atm / amtbf)
av_rows = ''
for mtbf_y in (1, 2, 5, 10, 20):
    mt = mtbf_y * 8760
    av_rows += f"| {mtbf_y} yr | " + ' | '.join(f"{mt/(mt+r)*100:.3f}%" for r in (2, 8, 24, 72, 168)) + " |\n"
fd_ops, fd_fail = 40 * 3 * 8760, 6

edit('engineering/availability-mtbf', date=U, phrase='availability calculator',
     intro=("Availability is the fraction of time equipment is ready to work. It depends on how often the equipment fails (MTBF) and how quickly it is repaired (MTTR). "
            "This availability calculator also gives the failure rate, downtime per year and reliability over a mission time.\n\n"
            "Maintenance, reliability and control system engineers use it to compare instruments, pumps and controllers and to justify spares or redundancy, as in "
            "[SIS final element reliability](https://www.instrumentationblog.in/sis-final-element-reliability/)."),
     before='## Availability and downtime', min_words=0,
     body_add=f'''
## Worked example

A transmitter has an MTBF of {amtbf:,.0f} h (10 years), an average repair time of {amttr:g} h and you want the chance of a fault-free year ({atm:,.0f} h):

- Availability A = {amtbf:,.0f} ÷ ({amtbf:,.0f} + {amttr:g}) = **{aA*100:.5f}%**
- Downtime per year = (1 − A) × 8,760 = **{adt:.2f} h** (about {adt*60:.0f} minutes)
- Failure rate λ = 8,760 ÷ {amtbf:,.0f} = **{alam:g} failures per year**
- Probability of no failure in a year R = e<sup>−{atm:,.0f}/{amtbf:,.0f}</sup> = **{aR*100:.2f}%**

So roughly 1 transmitter in 10 of this type will fail in any given year, but each one is out of service for well under an hour a year on average.

## Where MTBF and MTTR come from

- **Field data:** MTBF = total operating hours ÷ number of failures. For example, 40 identical pumps running 3 years with {fd_fail} failures give {fd_ops:,} ÷ {fd_fail} = {fd_ops/fd_fail:,.0f} h, about {fd_ops/fd_fail/8760:.0f} years.
- **Databases and vendors:** OREDA, exida and manufacturer FMEDA reports publish failure rates for valves, transmitters and logic solvers. Vendor figures usually exclude misuse and process-related failures, so field MTBF is often lower.
- **MTTR** must include the whole outage: detecting the fault, getting a technician and spare to site, the repair itself, testing and restart. Logistics often take longer than the repair.

## Availability by MTBF and MTTR

| MTBF | MTTR 2 h | 8 h | 24 h | 72 h | 1 week |
|---|---|---|---|---|---|
{av_rows}
''')
edit('engineering/availability-mtbf', date=U,
     body_add='''
## Common mistakes

- **Reading MTBF as a lifetime.** MTBF describes random failures during useful life. It says nothing about wear-out, so a 100-year MTBF valve still needs overhaul.
- **Leaving waiting time out of MTTR.** A 1 h repair that waits 2 days for a spare part has an MTTR of about 49 h for availability purposes.
- **Multiplying availabilities of redundant units.** Multiplying applies to items in series (all must work). For parallel redundancy combine the unavailabilities instead.
- **Mixing MTBF and MTTF.** For repairable items the difference is the MTTR, which is negligible here. For non-repairable parts such as fuses or bulbs, use MTTF.
- **Ignoring planned downtime.** This formula covers unplanned failures only. Scheduled shutdowns and proof tests reduce operational availability further.
''',
     faq_add=[("How do I calculate MTBF from field data?",
               "Divide the total operating hours of all units by the number of failures. 40 pumps running for 3 years (1,051,200 h in total) with 6 failures have an MTBF of 175,200 h, or 20 years. Count only failures of the function you care about, and use several years of data."),
              ("What is the difference between MTBF and MTTF?",
               "MTTF (mean time to failure) is used for items that are replaced, not repaired. MTBF applies to repairable equipment and equals MTTF plus MTTR. When repairs take hours and failures come years apart, the two are practically the same number.")])

# ---------------------------------------------------------------- Manometer
mrm, mrf, mL, mth = 1000.0, 1.2, 150.0, 30.0
mh = mL * math.sin(math.radians(mth))
mdp = (mrm - mrf) * g * mh / 1000
hg_m, hg_f, hg_h = 13546.0, 998.0, 200.0
hg_dp = (hg_m - hg_f) * g * hg_h / 1000
mn_rows = ''
for a in (90, 45, 30, 20, 10, 5):
    s = math.sin(math.radians(a))
    mn_rows += f"| {a}° | {1/s:.2f} | {(1000-1.2)*g*s/1000:.3f} Pa | {200*s:.1f} mm | {(1000-1.2)*g*0.2*s:.1f} Pa |\n"

edit('engineering/manometer', date=U, phrase='manometer calculator',
     intro=("A manometer measures pressure difference as the height of a liquid column, and tilting the tube spreads a small height over a longer, easier-to-read scale. "
            "This manometer calculator converts a U-tube or inclined manometer reading into pressure, including the fluid above the manometer liquid.\n\n"
            "HVAC technicians use it for duct and filter pressures, and instrument technicians use it as a simple reference standard. See the "
            "[U-tube manometer working principle and formula](https://www.instrumentationblog.in/u-tube-manometer-working-formula/)."),
     before='## Pressure for a 100 mm scale reading (Pa, measuring air)', min_words=0,
     body_add=f'''
Check the default result: {mh:.0f} mm of water is 75 × 9.79 ≈ {mdp*1000:.1f} Pa, or {mdp*1000/g:.1f} mm H₂O once the air above the water is allowed for.

## Liquid over liquid example

A vertical mercury U-tube measures the pressure drop across an orifice in a water line. The mercury levels differ by {hg_h:g} mm, with water filling both legs above the mercury:

- Δp = ({hg_m:,.0f} − {hg_f:,.0f}) × 9.80665 × {hg_h/1000:g} = **{hg_dp:.2f} kPa**

Ignoring the water above the mercury would give {hg_m*g*hg_h/1e6:.2f} kPa, an error of about {hg_f/(hg_m-hg_f)*100:.0f}%.

## Where manometers are used

- **Ventilation and filters:** inclined manometers show the pressure drop across air filters and fans, with a mark at the replacement point.
- **Combustion draft:** a few tens of Pa of furnace draft are read on an inclined gauge with light oil.
- **Calibration:** a vertical water or mercury column is a primary standard for low pressures, because the result depends only on density, g and a length.
- **Flow measurement:** U-tubes across orifice plates and pitot tubes give the differential pressure for flow calculations.

## Inclination and sensitivity (water, measuring air)

| Angle | Scale magnification | Pa per mm of scale | Vertical rise for 200 mm scale | Pressure at 200 mm scale |
|---|---|---|---|---|
{mn_rows}
''')
edit('engineering/manometer', date=U,
     body_add='''
## Common mistakes

- **Reading only one leg of a U-tube.** The pressure depends on the difference between the two levels. If one leg rises 50 mm, the other falls 50 mm, so h is 100 mm.
- **Using the scale length as the height on an inclined gauge.** Multiply by sin θ first, or use a scale already marked in Pa or mm H₂O.
- **Wrong fluid density.** Gauge oil, water and mercury change density with temperature, and a scale marked for SG 0.826 oil reads wrong if filled with water.
- **Reading the meniscus incorrectly.** Read the bottom of a water meniscus and the top of a mercury meniscus, with the eye level with the surface.
- **Trapped bubbles or dirty tubes.** An air bubble in a liquid-filled leg adds a false column, and a dirty bore makes the liquid stick.
''',
     faq_add=[("What is a well-type manometer?",
               "One leg is replaced by a large reservoir, so its level hardly moves and you read only the single tube. The small fall of the reservoir is allowed for in the scale, which is compressed by the ratio of the tube area to the reservoir area.")])

# ---------------------------------------------------------------- Pressure to head
pdp, prho = 5.0, 998.0
pH = pdp * 1e5 / (prho * g)
ps, pd, pz = 0.5, 5.5, 0.4
pTH = (pd - ps) * 1e5 / (prho * g) + pz
kgcm2 = 98066.5 / (prho * g)
ph_rows = ''
for b in (0.5, 1, 2, 5, 10, 16, 25, 40):
    Hm = b * 1e5 / (prho * g)
    ph_rows += f"| {b:g} bar | {b*14.5038:.1f} psi | {Hm:.2f} m | {Hm/0.3048:.1f} ft |\n"

edit('engineering/pressure-to-head', date=U, phrase='pressure to head calculator',
     intro=("Pump curves are drawn in metres or feet of head, while gauges read in bar or psi, so you often need to convert between them. "
            "This pressure to head calculator uses H = Δp ÷ (ρ·g) for any liquid density, and converts head back to pressure.\n\n"
            "Pump engineers use it to check a pump against its curve, and instrument engineers use the same relation for "
            "[hydrostatic level measurement](https://www.instrumentationblog.in/hydrostatic-level-measurement/) and transmitter ranges."),
     before='## Head of 1 bar and 1 psi for common liquids', min_words=0,
     body_add=f'''
## Pump head from two gauges

A water pump (ρ = {prho:g} kg/m³) has a suction gauge reading {ps:g} bar g and a discharge gauge reading {pd:g} bar g. The discharge gauge is mounted {pz:g} m higher than the suction gauge and both pipes are the same size, so the velocity heads cancel:

- Pressure head = ({pd:g} − {ps:g}) × 100,000 ÷ ({prho:g} × 9.80665) = {(pd-ps)*1e5/(prho*g):.2f} m
- Total head = {(pd-ps)*1e5/(prho*g):.2f} + {pz:g} = **{pTH:.2f} m**

Compare this with the pump curve at the measured flow. A head well below the curve points to wear, a closed suction valve or air in the liquid.

## Where the conversion is used

- **Pump testing and commissioning:** suction and discharge pressures give the developed head at the operating point.
- **Level measurement:** a pressure transmitter at the tank bottom reads ρgh, so the same formula turns pressure into liquid height.
- **Static head in buildings:** each 10.2 m of water column adds about 1 bar, which sets pressure ratings for high-rise riser pipes.

## Water head for common pressures

At {prho:g} kg/m³ (water near 20 °C):

| Pressure | psi | Head (m) | Head (ft) |
|---|---|---|---|
{ph_rows}
''')
edit('engineering/pressure-to-head', date=U,
     body_add=f'''
## Common mistakes

- **Using one gauge reading as pump head.** Pump head comes from the pressure difference between discharge and suction, not the discharge gauge alone.
- **Ignoring gauge elevation.** A gauge 2 m above the pump centreline reads about 0.2 bar less on water. Add the height difference between the gauges to the head.
- **Mixing gauge and absolute pressure.** A suction reading in bar a and a discharge reading in bar g give a head about 10 m wrong on water.
- **Using water density for every liquid.** A pump making 50 m of head produces only about 3.6 bar on petrol but 4.9 bar on water.
- **Converting kg/cm² as if it were bar.** 1 kg/cm² is 0.981 bar, so it gives {kgcm2:.2f} m of water rather than 10.22 m.
''',
     faq_add=[("How many metres of head is 1 kg/cm²?",
               f"About {kgcm2:.2f} m of water. 1 kg/cm² is 98,066.5 Pa, and dividing by 998 kg/m³ × 9.80665 m/s² gives {kgcm2:.2f} m, which is why older gauges in kg/cm² read almost directly in tens of metres of water.")])

print('done c1')

# ======================================================================= SECTION 2
"""Part C expansion (2026-11-15), slice 2: chiller-tonnage, valve-authority, turndown-ratio,
residence-time, barlow-formula. All numbers are computed here from the pages' own equations."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-15'
TRW = 3516.8528  # W per ton of refrigeration (units.ts)

# ---------------------------------------------------------------- Chiller tonnage
cV, cdT, ccp, crho = 50.0, 5.0, 4186.0, 998.0
cm = crho * cV / 3600
cQ = cm * ccp * cdT
cTR = cQ / TRW
gpm = cV * 1000 / 3.785411784 / 60
dTF = cdT * 1.8
tr_gpm = gpm * dTF / 24
# flow needed per TR for different delta T (water)
fl_rows = ''
for dT in (4, 5, 6, 7, 8, 10):
    m3h = TRW / (crho * ccp * dT) * 3600
    g = m3h * 1000 / 3.785411784 / 60
    fl_rows += f"| {dT} K ({dT*1.8:g} °F) | {m3h:.3f} m³/h | {g:.2f} gpm | {100*m3h:,.1f} m³/h |\n"
# low delta T syndrome: same flow, real delta T smaller
ld = 3.5
ld_TR = crho * cV / 3600 * ccp * ld / TRW
ld_V = cTR * TRW / (crho * ccp * ld) * 3600

edit('engineering/chiller-tonnage', date=U, phrase='chiller tonnage calculator',
     intro=("A chiller's cooling load is the heat the chilled water picks up: mass flow × specific heat × temperature rise. "
            "This chiller tonnage calculator turns flow and ΔT into kW and tons of refrigeration (1 TR = 3.517 kW).\n\n"
            "HVAC designers, plant engineers and energy auditors use it to size new chillers, check whether an existing machine "
            "is loaded, and set pump flows. See the step-by-step guide to "
            "[calculating industrial chiller capacity](https://www.instrumentationblog.in/calculate-industrial-chiller-capacity/)."),
     replace=[('- Capacity = 290.1 ÷ 3.517 = **82.5 TR**\n', f'- Capacity = 290.1 ÷ 3.517 = **82.5 TR**\n\nThe same example in US units: 50 m³/h is {gpm:.1f} gpm and 5 K is {dTF:g} °F, so tons = {gpm:.1f} × {dTF:g} ÷ 24 = **{tr_gpm:.1f} TR**, which agrees with the SI result.\n')],
     before='## Notes',
     body_add=f'''
## Chilled water flow needed per ton

For water (ρ = {crho:g} kg/m³, c<sub>p</sub> = {ccp:g} J/kg·K), the flow that carries one ton of refrigeration at each design ΔT, and the flow for a 100 TR chiller:

| Design ΔT | Flow per TR | Flow per TR | Flow for 100 TR |
|---|---|---|---|
{fl_rows}
The familiar rule of 2.4 gpm per ton belongs to a 10 °F (5.6 K) ΔT. Designing for a larger ΔT cuts the flow, the pipe size and the pump power, at the cost of a lower supply temperature or a larger coil.

## How chiller load is measured in practice

On site the load is found from three measurements: a flow meter on the chilled water header (an electromagnetic or ultrasonic clamp-on meter is common) and two matched temperature sensors on the supply and return lines. Because ΔT is small, the temperature sensors matter most: an error of 0.2 K on a 5 K ΔT is already a 4% error in tonnage. Use a matched pair of RTDs in thermowells, or clamp-on sensors under insulation, and log readings over a stable period rather than taking one spot value. Building management systems and BTU meters do this calculation continuously.

## Low ΔT syndrome

If the plant is designed for 5 K but runs at {ld:g} K, the same {cV:g} m³/h only carries {ld_TR:.1f} TR. To deliver the full {cTR:.1f} TR at {ld:g} K the pumps would need {ld_V:.1f} m³/h. Fouled coils, open bypass valves and three-way valves on coils are the usual causes, and the chillers end up running at part load while the pumps are at full speed.

## Common mistakes

- **Using the nominal ΔT instead of the measured one.** Real ΔT is often 1 to 2 K below design, which hides spare capacity or a problem.
- **Ignoring glycol.** A glycol mixture has a lower specific heat and a higher density than water; enter both, or the load will be overstated.
- **Mixing up volume and mass flow units.** The formula needs mass flow, so multiply the volume flow by density, and convert m³/h to m³/s (÷ 3,600).
- **Confusing refrigeration tons with weight tons.** 1 TR is a rate of heat removal (3.517 kW), not 1,000 kg of anything.
- **Sizing on the instantaneous peak alone.** Add allowances for pump heat, pipe gains and future load, but check part-load efficiency too: an oversized chiller cycles and wastes energy.
''',
     faq_add=[('How many kW of electricity does a chiller use per ton?',
               'It depends on the machine. A modern water-cooled centrifugal chiller uses roughly 0.5 to 0.7 kW of input power per TR at full load, while an air-cooled chiller typically uses about 1.0 to 1.3 kW per TR. Divide the cooling load by the COP to get the input power.')])

# ---------------------------------------------------------------- Valve authority
R = 50.0  # inherent rangeability for the equal-percentage characteristic
def inst(x, N):
    f = R ** (x - 1)
    return f / math.sqrt(N + (1 - N) * f * f)
NS = (1.0, 0.5, 0.33, 0.25, 0.1)
va_rows = ''
for x in (0.1, 0.25, 0.5, 0.75, 0.9):
    va_rows += f"| {x*100:g}% | " + ' | '.join(f"{inst(x, N)*100:.0f}%" for N in NS) + " |\n"
vdpv, vdps = 0.5, 1.0
vN = vdpv / (vdpv + vdps)
# valve dp needed for N = 0.5 with the same circuit
need = vdps * 0.5 / (1 - 0.5)
q50 = inst(0.5, vN) * 100

edit('engineering/valve-authority', date=U, phrase='valve authority calculator',
     intro=("Valve authority is the share of the circuit's variable pressure drop taken by the control valve at full flow. "
            "Too low and the valve loses control at small openings. This valve authority calculator works out N from the valve and system pressure drops and rates the result.\n\n"
            "HVAC designers and control engineers use it when selecting a valve size, a useful check alongside the "
            "[control valve flow coefficient](https://www.instrumentationblog.in/control-valve-flow-coefficient/), and when tracing why a loop hunts at low load."),
     replace=[('a smaller valve (higher Δp) would control better.\n', f'a smaller valve (higher Δp) would control better.\n\nTo lift the authority of this branch to 0.5, the valve itself must drop {need:g} bar at design flow, so select a valve with a smaller Kv. With N = {vN:.3f}, an equal-percentage valve at half stroke already passes about {q50:.0f}% of design flow.\n')],
     before='## Notes',
     body_add=f'''
## Installed flow of an equal-percentage valve

Flow as a share of design flow at each stroke position, for an equal-percentage valve with an inherent rangeability of {R:g}:1, computed from Q/Q<sub>max</sub> = f ÷ √(N + (1 − N) f²) with f = {R:g}<sup>(x − 1)</sup>:

| Stroke | N = 1 | N = 0.5 | N = 0.33 | N = 0.25 | N = 0.1 |
|---|---|---|---|---|---|
{va_rows}
At N = 1 the curve is the inherent characteristic. As authority falls, the curve bows upward, so most of the flow change is squeezed into the first part of the stroke and the loop gain at low load becomes very high.

## How to get the pressure drops

- **Valve Δp:** from the valve sizing at design flow, Δp = (Q ÷ Kv)² in bar with Q in m³/h for water. Pick the next smaller standard Kv and recalculate.
- **Circuit Δp:** add the coil or heat exchanger drop from its datasheet, the branch pipe friction and the fittings at the same design flow. Only include the part of the circuit whose flow changes when this valve moves.
- **On a running plant:** read pressure gauges or test points across the valve and across the branch at full flow with the valve wide open.

## Common mistakes

- **Including the whole pump head.** Pressure drops held constant by a differential pressure controller or in the common header do not belong in the denominator.
- **Using the valve's Δp at part load.** Authority is defined with the valve fully open at design flow.
- **Oversizing to save pump head.** A valve sized for a very low Δp gives N well below 0.25, and the loop will cycle at light load.
- **Treating authority as fixed.** When other branches close, the available pressure across the branch rises and the effective authority changes; pressure-independent valves avoid this.
- **Ignoring the valve characteristic.** Low authority hurts an equal-percentage valve less than a linear one in coil circuits, so check both together.
''',
     faq_add=[('Do pressure independent control valves need an authority check?',
               'Much less. A pressure independent control valve (PICV) has a built-in regulator that holds a constant pressure across its control element, so its authority is effectively 1 within its working pressure range. You still need to make sure the minimum differential pressure the PICV requires is available at the index circuit.')])

# ---------------------------------------------------------------- Turndown ratio
tQmax, tQmin = 100.0, 10.0
tTD = tQmax / tQmin
tdpr = (tQmin / tQmax) ** 2
# accuracy: 1% of span vs 0.5% of reading at several flows
ac_rows = ''
for q in (100, 50, 25, 10, 5):
    fs = 1.0 * tQmax / 100
    ac_rows += f"| {q:g} m³/h | ±{fs:.1f} m³/h | ±{fs/q*100:.1f}% | ±{0.005*q:.3f} m³/h | ±0.5% |\n"
# two stacked DP transmitters: high range 0-100%, low range 0-10% of max DP
lo_dp = 0.10
lo_flow = math.sqrt(lo_dp) * 100

edit('engineering/turndown-ratio', date=U, phrase='turndown ratio calculator',
     intro=("Turndown (rangeability) is the ratio of the maximum to the minimum flow an instrument can measure or control accurately. "
            "This turndown ratio calculator works it out in either direction and shows the DP left at minimum flow.\n\n"
            "Instrument engineers use it to check whether one meter or valve can cover the whole operating range. See "
            "[turndown ratio in flow meters](https://www.instrumentationblog.in/turndown-ratio-in-flow-meters/) and "
            "[control valve rangeability](https://www.instrumentationblog.in/control-valve-rangeability-turndown/)."),
     before='## Typical turndown by meter type', min_words=0,
     body_add=f'''
## Worked example

A process runs between {tQmin:g} and {tQmax:g} m³/h:

- Turndown = {tQmax:g} ÷ {tQmin:g} = **{tTD:.1f} : 1**
- For an orifice meter, DP at minimum flow = ({tQmin:g} ÷ {tQmax:g})² = **{tdpr*100:g}%** of the DP at maximum flow

If the transmitter is ranged 0 to 250 mbar, minimum flow produces only {250*tdpr:g} mbar, close to the noise level of the reading. A vortex, magnetic or Coriolis meter covers this 10:1 range comfortably; an orifice plate with one transmitter does not.
''')
# second edit pass adds the practice, table and mistakes sections at the end of the page
edit('engineering/turndown-ratio', date=U,
     body_add=f'''
## Accuracy at reduced flow

A meter rated ±1% of full scale (0 to {tQmax:g} m³/h) against a meter rated ±0.5% of reading:

| Flow | Error, 1% of span | As % of reading | Error, 0.5% of reading | As % of reading |
|---|---|---|---|---|
{ac_rows}
## Getting more turndown in practice

- **Stacked DP transmitters:** a second transmitter ranged to 10% of the maximum DP takes over below about {lo_flow:.0f}% of maximum flow, extending an orifice installation to roughly 10:1.
- **Two meters in parallel:** a small and a large meter with automatic switching, common in custody transfer and boiler fuel lines.
- **Split-range control valves:** a small valve opens first and a large valve takes over, raising the overall rangeability of the control loop.
- **Choose the meter for the range:** if the turndown needed is above about 10:1, a linear meter (magnetic, Coriolis, ultrasonic) is usually simpler than tricks with DP meters.

## Common mistakes

- **Quoting the catalogue turndown for the application.** A Coriolis meter's 100:1 is for its own maximum flow; if the meter is sized for twice your maximum, half of that range is wasted.
- **Forgetting the square law.** A 10:1 flow range on a DP meter means a 100:1 DP range for the transmitter.
- **Mixing accuracy bases.** Compare meters on the same basis: % of reading and % of span give very different errors at low flow.
- **Ignoring the low-flow cutoff.** Many transmitters force readings below a cutoff to zero, which sets the real minimum flow.
- **Confusing valve rangeability with installed rangeability.** The installed value is lower because the valve's pressure drop changes with flow.
''',
     faq_add=[('What turndown do I need for a flow meter?',
               'Divide the highest flow the process will see by the lowest flow you still need to measure within the required accuracy, then add a margin. A meter whose rated turndown, applied to its actual sized range, covers that ratio is suitable.')])

# ---------------------------------------------------------------- Residence time
rV, rQ = 10.0, 5.0
rtau = rV / rQ
rSV = 1 / rtau
cs_rows = ''
for k in (0.1, 0.25, 0.5, 1, 2, 3):
    f1 = 1 - math.exp(-k)
    # two equal tanks in series, each tau/2: F = 1 - exp(-2k)(1 + 2k)
    f2 = 1 - math.exp(-2 * k) * (1 + 2 * k)
    cs_rows += f"| {k:g} τ ({k*rtau*60:g} min) | {f1*100:.1f}% | {f2*100:.1f}% | {'0%' if k < 1 else '100%'} |\n"
# pipe residence
pD, pv, pL = 0.1, 1.5, 300.0
p_t = pL / pv
p_Q = pv * math.pi * pD ** 2 / 4 * 3600

edit('engineering/residence-time', date=U, phrase='residence time calculator',
     intro=("Residence time is the average time a fluid spends inside a vessel: the liquid volume divided by the throughput. "
            "This residence time calculator works out τ = V ÷ Q for tanks, reactors, settling basins and pipes, plus the space velocity.\n\n"
            "Process and water treatment engineers use it to size buffer tanks and clarifiers, check reaction or contact time, "
            "and work out how long a change at the inlet takes to reach the outlet."),
     before='## Notes',
     body_add=f'''
## How fluid really leaves a tank

The formula gives the average. In a well-mixed tank (CSTR) the fraction of the inlet fluid that has already left after a time t is 1 − e<sup>−t/τ</sup>. Splitting the same volume into two equal tanks in series narrows the spread towards plug flow. For the {rV:g} m³ tank at {rQ:g} m³/h (τ = {rtau:g} h):

| Time after entry | One mixed tank | Two tanks in series | Ideal plug flow |
|---|---|---|---|
{cs_rows}
This is why disinfection contact tanks are baffled: a mixed tank lets about 10% of the water out in a tenth of the nominal time.

## Residence time in a pipe

For a pipe, τ = L ÷ v. A {pD*1000:g} mm line {pL:g} m long at {pv:g} m/s holds the fluid for {p_t:.0f} s ({p_t/60:.1f} min), carrying {p_Q:.1f} m³/h. The same result follows from τ = V ÷ Q with the pipe's internal volume. This sets the transport delay seen by an analyser at the end of a sample line.

## Measuring residence time

The actual residence time distribution is found with a tracer test: inject a pulse or step of salt, dye or a conductivity tracer at the inlet and log the outlet concentration. The mean of the response curve is the real residence time; if it is much shorter than V ÷ Q, part of the tank is a dead zone and flow is short-circuiting.

## Common mistakes

- **Using the total vessel volume.** Use the liquid volume at operating level, minus the space taken by internals, agitators and settled solids.
- **Using the wrong flow.** Include recycle streams that pass through the vessel; a 100% recycle halves the residence time per pass.
- **Assuming every particle stays τ.** For contact, kill or reaction time, design on the short end of the distribution, not the average.
- **Mixing units.** m³ divided by m³/h gives hours; convert to minutes or seconds before comparing with a specification.
- **Ignoring density change in reactors.** For gas reactions with a change in moles, space time based on the inlet flow differs from the actual mean residence time.
''',
     faq_add=[('What is hydraulic retention time in wastewater treatment?',
               'Hydraulic retention time (HRT) is the same τ = V ÷ Q applied to an aeration tank, clarifier or digester using the average daily influent flow. It is different from sludge retention time (SRT), which is how long the biomass stays in the system and is controlled by sludge wasting.')])

# ---------------------------------------------------------------- Barlow formula
bS, bt, bD, bF = 290.0, 7.11, 168.3, 0.72
bPb = 2 * bS * bt / bD
bPd = bPb * bF
# minimum wall for a design pressure of 10 MPa
Pdes = 10.0
tmin = Pdes * bD / (2 * bS * bF)
tmill = tmin / 0.875
# Barlow (OD) vs Lame inner-surface hoop stress at the same pressure
th_rows = ''
for Dt in (100, 50, 30, 20, 15, 10, 6):
    t = 1.0; D = Dt * t; ro = D / 2; ri = ro - t; P = 1.0
    sb = P * D / (2 * t)
    sl = P * (ro ** 2 + ri ** 2) / (ro ** 2 - ri ** 2)
    sm = P * (D - t) / (2 * t)
    th_rows += f"| {Dt} | {sb:.2f} P | {sm:.2f} P | {sl:.2f} P | {(sb/sl-1)*100:+.1f}% |\n"
hyd = 1.25 * bPd

edit('engineering/barlow-formula', date=U, phrase="barlow's formula calculator",
     intro=("Barlow's formula relates the internal pressure a pipe can hold to its wall thickness, outside diameter and material strength. "
            "This Barlow's formula calculator gives the burst and design pressure with a design factor, or the minimum wall for a given pressure.\n\n"
            "Piping and pipeline engineers, inspectors and fabricators use it for quick wall thickness checks, pressure ratings of tube and line pipe, "
            "and as a sanity check before [hydrostatic testing](https://www.instrumentationblog.in/hydrostatic-testing-in-oil-gas-industry/)."),
     before='## Schedule 40 carbon steel pipe', min_words=0,
     body_add=f'''
Going the other way, the minimum wall for a design pressure of {Pdes:g} MPa on the same pipe is t = {Pdes:g} × {bD:g} ÷ (2 × {bS:g} × {bF:g}) = **{tmin:.2f} mm**. With a 12.5% mill under-tolerance, order at least {tmin:.2f} ÷ 0.875 = {tmill:.2f} mm nominal wall, before any corrosion allowance.
''')
edit('engineering/barlow-formula', date=U,
     body_add=f'''
## How accurate is Barlow for thick walls?

Hoop stress for an internal pressure P, comparing Barlow with the outside diameter, the mean diameter form (D − t) and the exact Lamé stress at the bore:

| D/t | Barlow, D/2t | Mean diameter, (D − t)/2t | Lamé at bore | Barlow vs Lamé |
|---|---|---|---|---|
{th_rows}
Using the outside diameter keeps Barlow on the safe side of the exact bore stress at every D/t: by about 1% for thin pipe, rising to about 15% at a D/t of 6. The mean-diameter form is closer to Lamé but reads slightly low. ASME B31.3 limits its thin-wall equation to walls thinner than D/6; beyond that, thick-wall design is required.

## Where Barlow's formula is used

- **Pipelines:** ASME B31.4 and B31.8 use the Barlow form with SMYS, a design factor, a joint factor and a temperature derating factor to set maximum operating pressure.
- **Tubing and instrument tubing:** manufacturers' pressure ratings for stainless tube are based on the same equation with an allowable stress.
- **Hydrotest planning:** the test pressure must stay below the pressure that yields the pipe. For the example, a test at 1.25 × design = {hyd:.2f} MPa gives a hoop stress of {hyd/bPb*100:.0f}% of SMYS.

## Common mistakes

- **Using the nominal wall without mill tolerance.** Seamless pipe can be 12.5% thinner than nominal, so the real rating is lower.
- **Mixing up yield and tensile strength.** SMYS with a design factor gives a working pressure; tensile strength with F = 1 gives an estimate of burst.
- **Using the inside diameter by habit.** The standard Barlow form uses the outside diameter, which is the conservative choice.
- **Forgetting temperature derating.** Allowable stress falls at high temperature; use the code value at design temperature.
- **Ignoring weld joint efficiency.** Welded pipe ratings in B31.3 multiply the stress by a joint quality factor E below 1 for some seam types.
''',
     faq_add=[('What is the difference between Barlow and Lamé equations?',
               "Barlow assumes the hoop stress is uniform through the wall, which is accurate for thin walls. Lamé's thick-cylinder solution shows the stress is highest at the bore and falls toward the outside surface. For thick walls Barlow with the outside diameter becomes increasingly conservative, and codes such as ASME B31.3 require thick-wall methods once the wall reaches one sixth of the diameter.")])

print('done')

# ======================================================================= SECTION 3
"""Part C fragment (2026-11-15): water-hammer, venturi-flow, hazen-williams,
convection-heat-transfer, instrument-accuracy. Every number is computed here."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-15'
G = 9.80665

# ---------------------------------------------------------------- Water hammer
rho, a, dv, L = 1000.0, 1200.0, 2.0, 500.0
wdP = rho * a * dv            # Pa
wdH = a * dv / G
wtc = 2 * L / a
# Korteweg wave speed: a = sqrt((K/rho) / (1 + (K/E)(D/e)))
Kw = 2.19e9
def wave(E, De):
    return math.sqrt((Kw / rho) / (1 + Kw / E * De))
MAT = [('Steel', 207e9), ('Ductile iron', 170e9), ('PVC', 3.0e9), ('HDPE', 0.9e9)]
wv_rows = ''
for nm, E in MAT:
    wv_rows += f"| {nm} | {E/1e9:g} GPa | " + ' | '.join(f"{wave(E, De):,.0f} m/s" for De in (20, 50, 100)) + " |\n"
# slow closure (Michaud): dH = 2 L v / (g t) for t > 2L/a
mi_rows = ''
for t in (0.5, wtc, 2, 5, 10, 20):
    if t <= wtc + 1e-9:
        dh = wdH
        note = 'full Joukowsky surge'
    else:
        dh = 2 * L * dv / (G * t)
        note = 'Michaud estimate'
    mi_rows += f"| {t:.2f} s | {dh:,.1f} m | {rho*G*dh/1e5:,.1f} bar | {note} |\n"
t5 = 5.0
dh5 = 2 * L * dv / (G * t5)

edit('engineering/water-hammer', date=U, phrase='water hammer calculator', min_words=0,
     intro=("Water hammer is the pressure spike that appears when a valve closes quickly or a pump trips and the moving liquid "
            "stops almost at once. This water hammer calculator uses the Joukowsky equation to find the surge pressure, the "
            "surge head and the critical closure time of a pipeline.\n\n"
            "Pipeline, water utility and plant engineers use it to set pipe pressure ratings, choose valve closing times and "
            "protect gauges. Read more on the [Joukowsky equation for water hammer](https://www.instrumentationblog.in/joukowsky-equation-water-hammer/) "
            "and the [hammer effect in pressure gauges](https://www.instrumentationblog.in/hammer-effect-in-pressure-gauges/)."),
     before='## Surge for water in steel pipe',
     body_add=f'''
## Worked example

Water ({rho:,.0f} kg/m³) flows at {dv:g} m/s in a {L:,.0f} m steel line with a wave speed of {a:,.0f} m/s, and a valve at the end shuts suddenly:

- Surge pressure ΔP = {rho:,.0f} × {a:,.0f} × {dv:g} = {wdP:,.0f} Pa = **{wdP/1e5:.1f} bar**
- Surge head ΔH = {a:,.0f} × {dv:g} ÷ 9.80665 = **{wdH:.1f} m**
- Critical closure time t<sub>c</sub> = 2 × {L:,.0f} ÷ {a:,.0f} = **{wtc:.3f} s**

The surge adds to the pressure already in the line, so a pipe running at 6 bar briefly sees about {6 + wdP/1e5:.0f} bar at the valve. If the valve instead closes over {t5:g} s, much longer than {wtc:.2f} s, Michaud's estimate ΔH ≈ 2Lv ÷ (g t) gives only {dh5:.1f} m ({rho*G*dh5/1e5:.1f} bar).
''')
edit('engineering/water-hammer', date=U, phrase='water hammer calculator',
     body_add=f'''
## Wave speed from the pipe wall

The wave speed depends on how stiff the liquid and the pipe wall are. The Korteweg formula is a = √[(K/ρ) ÷ (1 + (K/E)(D/e))], with K the bulk modulus of the liquid (water about 2.19 GPa), E the elastic modulus of the pipe wall, D the internal diameter and e the wall thickness. Values for water, computed with that formula:

| Pipe material | E | D/e = 20 | D/e = 50 | D/e = 100 |
|---|---|---|---|---|
{wv_rows}
Thin flexible walls stretch and absorb part of the surge, which is why plastic pipe sees much smaller pressure spikes than steel at the same velocity. Air or gas bubbles in the liquid lower the wave speed even more, but they make the surge less predictable.

## Effect of valve closing time

For the example pipeline ({L:,.0f} m, {dv:g} m/s, t<sub>c</sub> = {wtc:.2f} s). Closures slower than t<sub>c</sub> use Michaud's linear estimate, which is a first check only; a transient analysis is needed for a final design.

| Closing time | Surge head | Surge pressure | Basis |
|---|---|---|---|
{mi_rows}
Most of the velocity change in a gate or butterfly valve happens in the last 10 to 20% of travel, so the effective closing time is far shorter than the full stroke time. Two-stage or characterised closing helps.

## Common mistakes

- **Using the stroke time of the valve as the closing time.** Flow barely changes until the valve is nearly shut, so the real deceleration happens in a fraction of the stroke.
- **Forgetting the pump trip case.** When a pump stops, the pressure first drops on the discharge side. If it falls to vapour pressure, the column separates and the rejoining slug can cause a surge larger than the Joukowsky value.
- **Taking the steel wave speed for plastic pipe.** PVC and HDPE give wave speeds three to five times lower, so using 1,200 m/s overstates their surge.
- **Comparing the surge alone with the pipe rating.** Add the steady operating pressure to the surge before comparing with the pressure class of the pipe, valves and flanges.
- **Using the length of the whole network.** L is the distance from the valve to the nearest point where the wave reflects, such as a reservoir, a large tank or a big header.
''',
     faq_add=[('How do I calculate the pressure wave speed in a pipe?',
               'Use the Korteweg formula a = √[(K/ρ) ÷ (1 + (K/E)(D/e))]. For water (K = 2.19 GPa) in steel pipe with D/e = 50 it gives about '
               f'{wave(207e9, 50):,.0f} m/s; in PVC with the same D/e it gives about {wave(3.0e9, 50):,.0f} m/s.'),
              ('Does closing a valve slowly stop water hammer?',
               f'It reduces it. If the closure is slower than the critical time 2L/a, the surge falls roughly in proportion; for a {L:,.0f} m line at {dv:g} m/s, closing over {t5:g} s cuts the head rise from about {wdH:.0f} m to about {dh5:.0f} m.')])

# ---------------------------------------------------------------- Venturi
D, d, cd, dP, rv = 0.100, 0.060, 0.985, 20000.0, 998.0
b = d / D; At = math.pi * d * d / 4; E = 1 / math.sqrt(1 - b ** 4)
Qv = cd * At * math.sqrt(2 * dP / (rv * (1 - b ** 4)))
vt = Qv / At; vi = Qv / (math.pi * D * D / 4)
def vq(dd, DD=0.1, p=20000.0):
    bb = dd / DD
    return cd * math.pi * dd * dd / 4 * math.sqrt(2 * p / (rv * (1 - bb ** 4))) * 3600
bt_rows = ''
for dd in (0.040, 0.050, 0.060, 0.070, 0.075):
    bb = dd / 0.1
    bt_rows += f"| {dd*1000:.0f} mm | {bb:.2f} | {1/math.sqrt(1-bb**4):.4f} | {vq(dd):.1f} m³/h | {vq(dd, p=5000):.1f} m³/h |\n"
pl_lo, pl_hi = 0.05 * dP, 0.20 * dP

edit('engineering/venturi-flow', date=U, phrase='Venturi meter flow calculator',
     intro=("A Venturi tube narrows a pipe smoothly to a throat, where the fluid speeds up and its pressure drops; that "
            "differential pressure gives the flow rate. This Venturi meter flow calculator solves for flow, throat velocity or "
            "DP from the inlet and throat diameters.\n\n"
            "Water utilities, irrigation designers and instrument engineers use Venturis where low pressure loss matters. See the "
            "[Venturi tube flow meter](https://www.instrumentationblog.in/venturi-tube-flow-meter/) explained and "
            "[flow nozzle vs orifice plate vs Venturi](https://www.instrumentationblog.in/flow-nozzle-vs-orifice-plate-vs-venturi/)."),
     replace=[(f'''## Example

D = 100 mm, d = 60 mm, ΔP = 200 mbar, water:

- β = 0.6, Q = **68.0 m³/h**
''', f'''## Worked example

Water ({rv:g} kg/m³) in a {D*1000:.0f} mm line with a {d*1000:.0f} mm throat, C<sub>d</sub> = {cd:g} and a measured DP of 200 mbar ({dP:,.0f} Pa):

- β = {d*1000:.0f} ÷ {D*1000:.0f} = **{b:.2f}**, so 1 − β⁴ = {1-b**4:.4f}
- Throat area = π × {d:.3f}² ÷ 4 = {At*1e4:.3f} cm² ({At:.6f} m²)
- Q = {cd:g} × {At:.6f} × √(2 × {dP:,.0f} ÷ ({rv:g} × {1-b**4:.4f})) = {Qv:.5f} m³/s = **{Qv*3600:.1f} m³/h**
- Throat velocity = {Qv:.5f} ÷ {At:.6f} = **{vt:.2f} m/s** (inlet velocity {vi:.2f} m/s)

The permanent pressure loss of a classical Venturi is about 5 to 20% of the DP, so this meter costs only {pl_lo/100:.0f} to {pl_hi/100:.0f} mbar of pumping head.
''')],
     body_add=f'''
## Throat size and beta ratio

For a 100 mm line carrying water, computed with C<sub>d</sub> = {cd:g}. E is the velocity of approach factor 1/√(1 − β⁴):

| Throat | β | E | Flow at 200 mbar | Flow at 50 mbar |
|---|---|---|---|---|
{bt_rows}
A smaller throat gives a larger DP for the same flow, which helps at low flows but costs more pressure. Pick the throat so the normal flow sits at 50 to 80% of the transmitter range.

## How a Venturi is installed and measured

- **Taps:** the high-pressure tap is in the inlet cylinder, about half a pipe diameter upstream of the convergent cone, and the low-pressure tap is in the throat. Large Venturis use piezometer rings with several holes so one blocked hole does not spoil the reading.
- **Limits of ISO 5167-4:** classical Venturi tubes are covered for pipe sizes of about 50 to 1,200 mm, β of 0.4 to 0.75 and pipe Reynolds numbers from 2 × 10⁵ to 1 × 10⁶, where the published C<sub>d</sub> of about 0.984 to 0.995 applies.
- **Transmitter:** a DP transmitter with square-root extraction, or a linear signal that the control system takes the square root of. Mount it below the taps on liquid service so gas bubbles vent back to the line.
- **Straight pipe:** Venturis need less upstream straight pipe than orifice plates, but a bend or partly open valve just upstream still distorts the profile.

## Common mistakes

- **Leaving out 1 − β⁴.** Ignoring the velocity of approach factor understates flow by {(E-1)*100:.1f}% at β = {b:.1f}, and by much more at β = 0.75.
- **Using an orifice C<sub>d</sub>.** 0.6 is right for a sharp-edged orifice, not a Venturi; the error would be close to 40%.
- **Mixing up the measured DP and the permanent loss.** The DP between inlet and throat is the measuring signal; the pressure lost across the whole meter is far smaller.
- **Using the nominal pipe size for D.** Use the measured inlet bore of the Venturi body, since a 4 inch schedule 40 pipe is 102.3 mm, not 100 mm.
- **Applying the liquid formula to gas.** Gases expand through the throat, so an expansibility factor ε below 1 must be included for compressible flow.
''',
     faq_add=[('How do I size the throat of a Venturi meter?',
               'Choose the DP you want at maximum flow (often 200 to 500 mbar for water), then solve the flow equation for d, keeping β between about 0.4 and 0.75. In this calculator enter the flow and DP and clear the throat diameter to solve for it.')])

# ---------------------------------------------------------------- Hazen-Williams
Qh, dh_, Lh, Ch = 50 / 3600, 0.100, 100.0, 130.0
def hw(Q, d, L, C):
    return 10.67 * L * Q ** 1.852 / (C ** 1.852 * d ** 4.8704)
h0 = hw(Qh, dh_, Lh, Ch)
c_rows = ''
for C in (150, 140, 130, 120, 100, 80):
    hh = hw(Qh, dh_, Lh, C)
    c_rows += f"| {C} | {hh:.3f} m | {hh*9.80665:.2f} kPa | {hh/h0*100:.0f}% |\n"
fl_rows = ''
for q in (25, 50, 75, 100):
    hh = hw(q / 3600, dh_, Lh, Ch)
    fl_rows += f"| {q} m³/h | {q/3600/(math.pi*dh_**2/4):.2f} m/s | {hh:.3f} m | {hh*9.80665:.2f} kPa |\n"
# US customary form: p (psi/ft) = 4.52 Q^1.852 / (C^1.852 d^4.87), Q gpm, d in
Qg = Qh / 3.785411784e-3 * 60; din = dh_ / 0.0254
p_us = 4.52 * Qg ** 1.852 / (Ch ** 1.852 * din ** 4.87)
p_si = h0 * 9.80665 / Lh  # kPa per m
p_si_psift = p_si / 6.894757 * 0.3048

edit('engineering/hazen-williams', date=U, phrase='Hazen-Williams calculator',
     intro=("The Hazen-Williams equation is the standard empirical formula for friction loss in water pipes, with a single C "
            "factor for pipe roughness. This Hazen-Williams calculator gives head loss, pressure drop and velocity from flow, "
            "pipe diameter, length and C.\n\n"
            "Water supply, fire sprinkler and irrigation designers use it to size pipes and pumps quickly. See "
            "[how to calculate pressure drop in pipes](https://www.instrumentationblog.in/calculate-pressure-drop-in-pipes/) for the wider method."),
     body_add=f'''
## Effect of the C factor

Same example (50 m³/h, 100 mm, 100 m). C falls as pipes age, scale and corrode, and head loss rises quickly as it does:

| C factor | Head loss | Pressure drop | vs C = 130 |
|---|---|---|---|
{c_rows}
Designers often use a lower C than the new-pipe value to allow for 20 to 30 years of service, for example 100 to 120 for unlined steel.

## Head loss vs flow

Friction loss rises with Q<sup>1.852</sup>, so doubling the flow multiplies head loss by about {2**1.852:.2f}. For 100 m of 100 mm pipe at C = 130:

| Flow | Velocity | Head loss | Pressure drop |
|---|---|---|---|
{fl_rows}
## The US customary form

Fire sprinkler hydraulic calculations (NFPA 13) use p = 4.52 Q<sup>1.852</sup> ÷ (C<sup>1.852</sup> d<sup>4.87</sup>), with p in psi per foot, Q in gpm and d in inches. The example is {Qg:.1f} gpm in a {din:.3f} in bore: p = {p_us:.4f} psi/ft, which agrees within rounding with the SI result of {p_si:.4f} kPa/m ({p_si_psift:.4f} psi/ft). Hydraulic software applies the formula pipe by pipe and adds fittings as equivalent lengths.

## Common mistakes

- **Using the nominal size instead of the bore.** A 100 mm (4 in) schedule 40 steel pipe has a 102.3 mm bore; at d<sup>4.87</sup> that 2.3% difference changes head loss by about {((102.3/100)**4.87-1)*100:.0f}%.
- **Using it for hot water, oil or gas.** The constants assume water near room temperature. Use the [Darcy-Weisbach calculator](/engineering/darcy-weisbach-head-loss/) for other fluids.
- **Forgetting the minor losses.** Valves, bends and tees can add as much loss as the straight pipe in short, fitting-rich runs.
- **Taking the new-pipe C for an old main.** Tuberculated cast iron can drop to C = 60 to 80, more than doubling friction loss.
- **Mixing units.** The 10.67 constant needs Q in m³/s and d in m; the 4.52 constant needs gpm and inches. Putting litres per second or millimetres into either gives nonsense.
''',
     faq_add=[('How accurate is the Hazen-Williams equation?',
               'For clean water at normal temperatures in turbulent flow it is usually within about 5 to 10% of Darcy-Weisbach, which is good enough for distribution and sprinkler design. The main uncertainty is the C factor, not the formula. Accuracy falls at very low or very high velocities.')])

# ---------------------------------------------------------------- Convection
hc, Ac, Tsc, Tfc = 25.0, 2.0, 80.0, 25.0
Qc = hc * Ac * (Tsc - Tfc)
# Simplified free convection in air, vertical surface (Holman):
# laminar h = 1.42 (dT/L)^0.25, turbulent h = 1.31 dT^(1/3)
nc_rows = ''
for dT in (10, 25, 55, 100):
    hl = 1.42 * (dT / 0.5) ** 0.25
    ht = 1.31 * dT ** (1 / 3)
    nc_rows += f"| {dT} K | {hl:.1f} W/m²·K | {hl*Ac*dT:,.0f} W | {ht:.1f} W/m²·K |\n"
# Dittus-Boelter for water at about 40 °C in a 25 mm tube
kw, nu, Pr, Dt = 0.631, 0.658e-6, 4.32, 0.025
db_rows = ''
for v in (0.5, 1.0, 2.0):
    Re = v * Dt / nu
    Nu = 0.023 * Re ** 0.8 * Pr ** 0.4
    db_rows += f"| {v:g} m/s | {Re:,.0f} | {Nu:.0f} | {Nu*kw/Dt:,.0f} W/m²·K |\n"
Re1 = 1.0 * Dt / nu; Nu1 = 0.023 * Re1 ** 0.8 * Pr ** 0.4; h1 = Nu1 * kw / Dt
hl55 = 1.42 * (55 / 0.5) ** 0.25

edit('engineering/convection-heat-transfer', date=U, phrase='convection heat transfer calculator',
     intro=("Convection is heat carried away by a moving fluid, and its rate depends on the heat transfer coefficient h, the "
            "surface area and the temperature difference. This convection heat transfer calculator solves Q = h·A·(Ts − T∞) "
            "for any one unknown.\n\n"
            "Process, HVAC and electronics engineers use it to estimate heat loss from hot equipment, size heaters and coolers, "
            "and check surface temperatures. It pairs with [calculating heat loss in piping](https://www.instrumentationblog.in/calculate-heat-loss-in-piping/)."),
     body_add=f'''
## Estimating the heat transfer coefficient

The hard part of any convection problem is h, which depends on the fluid, its velocity, the geometry and whether the flow is laminar or turbulent. Engineers find it from a Nusselt number correlation, Nu = hL ÷ k.

**Free convection in air.** For a vertical surface, simplified correlations give h = 1.42 (ΔT/L)<sup>0.25</sup> in laminar flow and h = 1.31 ΔT<sup>1/3</sup> in turbulent flow (W/m²·K, ΔT in K, L the height in m). For a 0.5 m high surface:

| ΔT | h, laminar (L = 0.5 m) | Q for 2 m², laminar | h, turbulent (surfaces over about 1 m tall) |
|---|---|---|---|
{nc_rows}
At ΔT = 55 K the laminar value is about {hl55:.1f} W/m²·K, so the 25 W/m²·K in the worked example implies a light forced draught, not still air.

**Forced convection inside tubes.** The Dittus-Boelter equation Nu = 0.023 Re<sup>0.8</sup> Pr<sup>0.4</sup> (heating, Re above about 10,000) gives, for water at about 40 °C (k = {kw} W/m·K, ν = {nu*1e6:.3f} mm²/s, Pr = {Pr}) in a 25 mm tube:

| Velocity | Re | Nu | h |
|---|---|---|---|
{db_rows}
At 1 m/s, h ≈ {h1:,.0f} W/m²·K, about {h1/hc:.0f} times the air value in the example. That is why liquid cooling moves so much more heat through the same area.

## Common mistakes

- **Using the wrong temperature difference.** ΔT is between the surface and the bulk fluid far from it, not between the inlet and outlet of the fluid. For a fluid that heats up along an exchanger, use the [LMTD](/engineering/lmtd/).
- **Taking h from a table without checking the flow regime.** Tables give wide ranges; a value from the wrong end can be ten times off. Calculate it from a correlation when the result matters.
- **Ignoring radiation from hot surfaces.** In still air, radiation from a painted surface at 80 °C is of the same size as natural convection, so adding only convection understates the loss by about half.
- **Mixing up h and U.** h is a single film coefficient; U combines both films and the wall. Using a film h where an overall U belongs overstates heat transfer.
- **Forgetting fouling.** Scale and deposits add thermal resistance over time, so design values are often 10 to 30% below clean values.
''',
     faq_add=[('How do I calculate the heat transfer coefficient h?',
               f'From a Nusselt number correlation: h = Nu × k ÷ L. For turbulent water in a tube, Dittus-Boelter gives Nu = 0.023 Re^0.8 Pr^0.4; water at 1 m/s in a 25 mm tube has h of about {h1:,.0f} W/m²·K. For still air on a vertical wall, h is only about 3 to 6 W/m²·K.')])

# ---------------------------------------------------------------- Instrument accuracy
lo, hi, rd, acc = 0.0, 100.0, 25.0, 0.005
err = acc * (hi - lo); ar = err / abs(rd)
# Total probable error example: DP transmitter 0-250 mbar
span = 250.0
TPE = [('Reference accuracy', 0.065), ('Ambient temperature effect', 0.10), ('Static pressure effect', 0.05),
       ('Stability (1 year)', 0.10), ('Input card (DCS/PLC)', 0.10)]
tpe_rows = ''.join(f"| {nm} | ±{p:g}% | ±{p/100*span:.3f} mbar |\n" for nm, p in TPE)
rss = math.sqrt(sum(p * p for _, p in TPE)); lin = sum(p for _, p in TPE)
tpe_rows += f"| **Root sum of squares** | **±{rss:.3f}%** | **±{rss/100*span:.3f} mbar** |\n"
tpe_rows += f"| Simple sum (worst case) | ±{lin:.3f}% | ±{lin/100*span:.3f} mbar |\n"
# DP flow: 0.5% of DP span at 25% flow (6.25% DP)
flow_rows = ''
for f in (1.0, 0.75, 0.5, 0.25, 0.1):
    dpf = f * f
    ferr = 0.5 * 0.005 / dpf * 100   # % of reading in flow
    flow_rows += f"| {f*100:.0f}% | {dpf*100:.2f}% | ±{0.5/dpf:.1f}% | ±{ferr:.2f}% |\n"

edit('engineering/instrument-accuracy', date=U, phrase='instrument accuracy calculator', min_words=0,
     intro=("Instrument accuracy can be stated as a percentage of span, of full scale or of reading, and the difference matters "
            "most at low readings. This instrument accuracy calculator turns any % of span figure into the real error band in "
            "engineering units and as % of reading.\n\n"
            "Instrument engineers use it to select transmitters, set alarm margins and check that a meter is good enough for "
            "custody transfer or control. See [accuracy reading vs full scale](https://www.instrumentationblog.in/flow-meter-accuracy-reading-vs-full-scale/) "
            "and [pressure transmitter accuracy specifications](https://www.instrumentationblog.in/pressure-transmitter-accuracy-specifications/)."),
     before='## ±1% of full scale vs ±1% of reading',
     body_add=f'''
## Worked example

A transmitter ranged {lo:g} to {hi:g} with an accuracy of ±{acc*100:g}% of span reads {rd:g}:

- Error band = {acc*100:g}% × ({hi:g} − {lo:g}) = **±{err:g} units**
- As a percentage of reading = {err:g} ÷ {rd:g} = **±{ar*100:g}%**
- The true value lies between **{rd-err:g}** and **{rd+err:g}**

The same ±{err:g} units at a reading of 100 would be only ±{err/100*100:g}% of reading, so the error relative to the value grows four times as the reading falls to a quarter of range.
''')
edit('engineering/instrument-accuracy', date=U, phrase='instrument accuracy calculator',
     body_add=f'''
## Accuracy of DP flow at low flow

On a DP flow meter the DP rises with flow squared, so a fixed ±0.5% of DP span becomes a large flow error at low flow. Flow error in % of reading is about half the DP error in % of reading:

| Flow (% of max) | DP (% of span) | DP error, % of reading | Flow error, % of reading |
|---|---|---|---|
{flow_rows}
This is why DP flow loops are rarely used below about 25 to 30% of maximum flow, and why the [turndown ratio](/engineering/turndown-ratio/) of a DP meter is often quoted as 3:1 or 4:1.

## Total probable error of a loop

The datasheet "reference accuracy" applies only at reference conditions. In service, ambient temperature, static pressure, drift and the input card all add error. For a DP transmitter with a 250 mbar span (typical datasheet values):

| Error source | % of span | mbar |
|---|---|---|
{tpe_rows}
The independent errors combine by root sum of squares, giving ±{rss:.2f}% of span, about {rss/0.065:.1f} times the reference accuracy alone.

## How accuracy is checked in practice

During calibration the transmitter is compared with a reference standard at several points, usually 0, 25, 50, 75 and 100% of span, rising and falling. The reference should be at least four times more accurate than the device under test (a 4:1 test uncertainty ratio). The as-found error at each point is compared with the tolerance; see the [calibration error calculator](/engineering/calibration-error/).

## Common mistakes

- **Reading % of span as % of reading.** ±0.5% of span is a fixed band in units, which can be many percent of a small reading.
- **Using reference accuracy as the loop accuracy.** Add temperature, static pressure, stability and the input card by root sum of squares.
- **Forgetting the effect of re-ranging.** Many smart transmitters quote accuracy as a % of the calibrated span plus a term in % of URL, which grows when the span is turned down.
- **Adding all errors linearly.** A straight sum gives the worst case ({lin:.3f}% in the table above), which overstates the probable error of independent sources.
- **Ignoring the reference standard.** A calibrator only as good as the device under test cannot prove that it meets its specification.
''',
     faq_add=[('What is total probable error?',
               f'The combined error of an instrument loop under real operating conditions, found as the square root of the sum of the squares of the independent errors (reference accuracy, ambient temperature, static pressure, stability and input card). In the example on this page it is ±{rss:.2f}% of span compared with ±0.065% reference accuracy.')])

print('c3 done')

# ======================================================================= SECTION 4
"""Part C expansions (2026-11-15), slice 4: ultrasonic-level, signal-converter, fan-affinity-laws,
sensor-response-time, vertical-tank-volume. All numbers are computed here from the page defaults."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit
U = '2026-11-15'
M = '−'
def sg(x, f):
    s = format(x, f)
    return s.replace('-', M)

# ---------------------------------------------------------------- Ultrasonic level
def c_air(T): return 331.3 * math.sqrt(1 + T / 273.15)
ut, uT, uE = 0.020, 30.0, 6.0
uc = c_air(uT); ud = uc * ut / 2; uL = uE - ud
uc20 = c_air(20); ud20 = uc20 * ut / 2; uL20 = uE - ud20
uerr = uL20 - uL
ue_rows = ''
for dist in (0.5, 1, 2, 4, 6, 8, 10, 15):
    ue_rows += f"| {dist:g} m | " + ' | '.join(f"{2*dist/c_air(T)*1000:.2f} ms" for T in (0, 20, 40)) + " |\n"
co2 = 267.0

edit('engineering/ultrasonic-level', date=U, phrase='ultrasonic level calculator',
     intro="An ultrasonic level transmitter sends a sound pulse down to the liquid surface and times the echo, and the speed of sound in air changes by about 0.6 m/s per °C. This ultrasonic level calculator converts echo time and air temperature into distance and level, as explained in [ultrasonic level transmitter working](https://www.instrumentationblog.in/ultrasonic-level-transmitter-working/).\n\nInstrument technicians use it to check a transmitter's reading against a manual dip, set the empty distance and span, and see how much a temperature error shifts the level.",
     before='## Installation tips',
     body_add=f'''
## What a temperature error costs

Take the same echo of {ut*1000:g} ms with an empty distance of {uE:g} m, but suppose the transmitter's temperature compensation fails and it assumes 20 °C while the air in the tank is really {uT:g} °C:

- Assumed speed of sound at 20 °C = 331.3 × √(1 + 20/273.15) = **{uc20:.1f} m/s**
- Distance it reports = {uc20:.1f} × {ut:g} ÷ 2 = **{ud20:.3f} m**, so level = {uE:g} − {ud20:.3f} = **{uL20:.3f} m**
- True level at {uT:g} °C = **{uL:.3f} m**, so the reading is **{uerr*1000:.0f} mm** too high

The error grows with distance, so it is worst when the tank is nearly empty, which is exactly when a pump may be running dry.

## Echo time by distance and temperature

Round-trip echo time t = 2d ÷ c:

| Distance to surface | 0 °C | 20 °C | 40 °C |
|---|---|---|---|
{ue_rows}
A transmitter that measures to 15 m must wait about 90 ms for each echo, which is why long-range units update more slowly and average several pulses.

## Setting up the transmitter in practice

The transmitter does not know where the bottom of the tank is: you enter the **empty distance** (sensor face to the 0% point) and the **span** (0% to 100%), and it scales the 4 to 20 mA output between them. The 100% point must stay below the **blanking distance**, so a sensor with 0.3 m blanking cannot read the last 0.3 m under its face. During commissioning, run the false echo suppression (echo mapping) with the tank empty or at low level, so the unit learns and ignores reflections from ladders, welds and agitator blades. Then compare the reading with a manual dip at two levels at least.

## Common mistakes

- **Measuring the empty distance to the nozzle flange** instead of the transducer face. The face sits some way inside or above the flange, and the whole offset ends up in the level.
- **Mounting in a long, narrow nozzle.** The pulse rings off the nozzle walls and the unit locks onto that echo. Keep the transducer face at or just below the end of the nozzle.
- **Trusting the built-in temperature probe in a stratified tank.** The probe reads the air at the sensor, but a warm vapour layer near the liquid has a different speed of sound.
- **Using ultrasonic over foam.** Foam absorbs the pulse, so the echo is weak or comes from the top of the foam rather than the liquid.
- **Ignoring the gas in the tank.** In carbon dioxide sound travels at about {co2:g} m/s at 20 °C, roughly {(1-co2/uc20)*100:.0f}% slower than in air, so an air-calibrated unit reads badly wrong.
''',
     faq_add=[('How do I set the 4 to 20 mA range of an ultrasonic level transmitter?',
               'Enter the empty distance from the sensor face to the 0% point, which gives 4 mA, and the span up to the 100% point, which gives 20 mA. The 100% point must be at least the blanking distance below the sensor face, or the top of the range cannot be measured.'),
              ('Does the gas above the liquid affect an ultrasonic level reading?',
               f'Yes. The speed of sound depends on the gas as well as the temperature. In carbon dioxide it is about {co2:g} m/s at 20 °C against {uc20:.0f} m/s in air, so a transmitter set up for air would read the distance about {(1-co2/uc20)*100:.0f}% too short. Radar is not affected by the gas composition.')])

# ---------------------------------------------------------------- Signal converter
def conv(P): return dict(I=4 + 16 * P, I0=20 * P, V10=10 * P, V15=1 + 4 * P, V5=5 * P)
sv = 3.8; sP = (sv - 1) / 4; sc = conv(sP)
NE = [('Failure (low)', 3.6), ('Under-range limit', 3.8), ('0% (live zero)', 4.0), ('100%', 20.0), ('Over-range limit', 20.5), ('Failure (high)', 21.0)]
ne_rows = ''.join(f"| {nm} | {i:.1f} mA | {sg((i-4)/16*100, '.2f')}% | {sg(1+4*(i-4)/16, '.3f')} V |\n" for nm, i in NE)
r_rows = ''.join(f"| {R:g} Ω | {0.004*R:.2f} V | {0.012*R:.2f} V | {0.020*R:.2f} V |\n" for R in (50, 100, 250, 500))
Rmax = (24 - 12) / 0.020

edit('engineering/signal-converter', date=U, phrase='signal converter calculator',
     intro="Field instruments, PLC inputs and drives use different analog standards, and a signal isolator or converter maps one onto another by percent of range. This signal converter calculator translates 4 to 20 mA, 0 to 20 mA, 0 to 10 V and 1 to 5 V values in any direction, as covered in [4 to 20 mA signal conversion](https://www.instrumentationblog.in/4-to-20-ma-signal-conversion/).\n\nInstrument and control engineers use it when configuring isolators, checking a PLC input card or fault-finding a loop with a multimeter.",
     before='## Choosing a signal',
     body_add=f'''
## Worked example: from a 1 to 5 V reading

A controller input reads **{sv:g} V** across its 250 Ω resistor. Enter it in the 1 to 5 V field:

- Percent of range = ({sv:g} − 1) ÷ 4 = **{sP*100:.0f}%**
- 4 to 20 mA loop current = 4 + 16 × {sP:.2f} = **{sc['I']:.1f} mA**
- 0 to 10 V equivalent = **{sc['V10']:.1f} V**, 0 to 20 mA = **{sc['I0']:.1f} mA**, 0 to 5 V = **{sc['V5']:.1f} V**

Multiply the percent by the transmitter range to get engineering units: on a 0 to 10 bar transmitter {sP*100:.0f}% is {sP*10:.1f} bar.

## NAMUR NE 43 signal levels

Most modern transmitters follow NAMUR NE 43, which keeps the measurement between 3.8 and 20.5 mA and reserves the values beyond for fault signalling:

| Signal | Current | Percent of range | 1 to 5 V equivalent |
|---|---|---|---|
{ne_rows}
A receiver that clips at 0% and 100% hides these states, so set its alarm limits to catch them.

## Current to voltage with a resistor

A current loop becomes a voltage across a precision resistor, V = I × R:

| Resistor | At 4 mA | At 12 mA | At 20 mA |
|---|---|---|---|
{r_rows}
The resistor's tolerance goes straight into the reading, so use 0.1% resistors. Each one also adds to the loop load: with a 24 V supply and a transmitter that needs 12 V, the loop can drive at most (24 − 12) ÷ 0.020 = **{Rmax:.0f} Ω** in total.

## Common mistakes

- **Forgetting the live zero.** 4 mA is 0%, so it maps to 0 V on a 0 to 10 V output, not 2 V. Mapping mA to volts by simple proportion (V = mA ÷ 2) gives a 2 V offset at zero.
- **Converter configured for the wrong input range.** If an isolator is set to 0 to 20 mA but fed 4 to 20 mA, 4 mA shows up as 20% and the span is wrong too.
- **Ground loops.** Non-isolated converters tie the field and control system grounds together, and the circulating current shows up as an offset or noise. Use an isolator when the two sides are grounded at different points.
- **Exceeding the loop load.** Adding a recorder, an indicator and a 250 Ω input in series can push the transmitter below its minimum voltage, and the signal flattens near 20 mA.
- **Reading 0 to 10 V over long cables.** Voltage signals lose accuracy to cable resistance and pick up noise. For long runs, convert to 4 to 20 mA at the field end.
''',
     faq_add=[('What does a reading below 4 mA or above 20 mA mean?',
               'Under NAMUR NE 43, 3.8 to 4 mA and 20 to 20.5 mA are valid under-range and over-range readings. A signal at or below 3.6 mA, or at or above 21 mA, means the transmitter has detected a fault, or the loop is open or shorted.')])

# ---------------------------------------------------------------- Fan affinity laws
fQ, fdp, feta, fN1, fN2 = 10000 / 3600, 1000.0, 0.70, 1450.0, 1160.0
fPs = fQ * fdp / feta; fPs2 = fPs * (fN2 / fN1) ** 3
hrs = 6000; fsave = (fPs - fPs2) * hrs / 1000
rho20 = 1.204
d_rows = ''
for T in (0, 20, 40, 80, 150, 250):
    r = rho20 * 293.15 / (273.15 + T)
    d_rows += f"| {T} °C | {r:.3f} kg/m³ | {fdp*r/rho20:,.0f} Pa | {fPs*r/rho20/1000:.2f} kW |\n"
Th = 150; rh = rho20 * 293.15 / (273.15 + Th)
ratio_cold = (rho20 * 293.15 / (273.15 + 20)) / rh

edit('engineering/fan-affinity-laws', date=U, phrase='fan affinity laws calculator',
     intro="A fan's air power is airflow times pressure rise, and its shaft power is that divided by the fan efficiency. This fan affinity laws calculator finds both, then scales flow, pressure and power to a new speed: flow with the speed ratio, pressure with its square and power with its cube.\n\nHVAC designers, energy auditors and plant engineers use it to size fan motors and to estimate [VFD energy savings](https://www.instrumentationblog.in/vfd-sizing-selection-guide/) before slowing a fan instead of throttling it with a damper.",
     before='## Notes',
     body_add=f'''
## Energy saving example

Using the worked example above, the fan runs **{hrs:,} hours a year** at {fN2:,.0f} rpm instead of {fN1:,.0f} rpm:

- Shaft power falls from {fPs/1000:.3f} kW to {fPs2/1000:.3f} kW, a saving of **{(fPs-fPs2)/1000:.3f} kW**
- Shaft energy saved = {(fPs-fPs2)/1000:.3f} × {hrs:,} = **{fsave:,.0f} kWh per year**

Motor and drive losses are not included; a VFD itself loses roughly 2 to 3% of its throughput.

## Air density and fan power

Pressure and power scale with gas density at the same volume flow and speed. For the example fan rated at {fdp:,.0f} Pa with air at 20 °C ({rho20} kg/m³, sea level):

| Gas temperature | Density | Pressure rise | Shaft power |
|---|---|---|---|
{d_rows}
## Using the fan laws in practice

The laws compare two operating points of the same fan in the same system, so they hold only if the system curve passes through the origin: all of the pressure is friction that varies with flow squared. Airflow is usually measured in the field with a pitot tube traverse across the duct, pressure rise with a manometer across the fan, and power with a clamp-on power meter at the motor. In variable air volume systems that hold a fixed duct static pressure, the fan cannot follow the cube law all the way down, so real savings are smaller than the calculator shows.

## Common mistakes

- **Applying the laws to a damper change.** Closing a damper moves the fan to a new point on the same speed curve. The fan laws only describe speed (or diameter) changes.
- **Starting a hot gas fan cold.** A fan sized for gas at {Th} °C moves air that is {ratio_cold:.2f} times denser at 20 °C, so on a cold start it needs {ratio_cold:.2f} times the power and can overload its motor.
- **Mixing static and total pressure.** Use fan total pressure with total efficiency, or static pressure with static efficiency.
- **Mixing units.** Air power is m³/s × Pa = W. Feeding m³/h or CFM straight into that product gives an answer 3,600 or 1,700 times too large.
- **Extrapolating to very low speeds.** Below about 30 to 40% speed, motor cooling, fan stall and minimum duct pressure take over, and efficiency no longer stays constant.
''',
     faq_add=[('Why does a hot gas fan overload its motor at a cold start?',
               f'Fan power is proportional to gas density. A fan designed for gas at {Th} °C handles air about {ratio_cold:.2f} times denser when it starts cold at 20 °C, so it draws about {ratio_cold:.2f} times its hot running power. Size the motor for the cold start or keep the inlet damper closed until the gas warms up.')])

# ---------------------------------------------------------------- Sensor response time
tau1, tau2 = 8.0, 2.0
def two_lag(t, a, b): return 1 - (a * math.exp(-t / a) - b * math.exp(-t / b)) / (a - b)
def t_for(frac, f):
    lo, hi = 0.0, 1000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) < frac: lo = mid
        else: hi = mid
    return (lo + hi) / 2
c63 = t_for(1 - math.exp(-1), lambda t: two_lag(t, tau1, tau2))
c90 = t_for(0.9, lambda t: two_lag(t, tau1, tau2))
s90 = tau1 * math.log(10)
sum90 = (tau1 + tau2) * math.log(10)
ramp_rows = ''
for r in (1, 2, 5, 10, 20):
    ramp_rows += f"| {r} °C/min | " + ' | '.join(f"{r*tau/60:.2f} °C" for tau in (2, 8, 30, 60)) + " |\n"

edit('engineering/sensor-response-time', date=U, phrase='sensor response time calculator',
     intro="Temperature sensors in thermowells, damped pressure transmitters and many analysers respond like a first-order lag, reaching 63.2% of a step change in one time constant. This sensor response time calculator converts the time constant into T50, T90 and T99 and predicts the reading at any time, as described in [temperature sensor response time](https://www.instrumentationblog.in/temperature-sensor-response-time/).\n\nInstrument and safety engineers use it to check whether a sensor is fast enough for a control loop or a trip, and how long to wait during calibration.",
     before='## Response time multiples',
     body_add=f'''
## Worked example: sensor plus transmitter damping

The same Pt100 (τ = {tau1:g} s) feeds a transmitter with **{tau2:g} s damping**. Two first-order lags in series respond as

<p class="formula">y(t) = 1 − (τ₁e<sup>−t/τ₁</sup> − τ₂e<sup>−t/τ₂</sup>) ÷ (τ₁ − τ₂)</p>

Solving that numerically for the step response:

- Time to 63.2% = **{c63:.2f} s** (sensor alone: {tau1:g} s)
- T90 = **{c90:.2f} s** (sensor alone: {s90:.2f} s)
- Treating the pair as one lag with τ = {tau1:g} + {tau2:g} = {tau1+tau2:g} s gives T90 = {sum90:.2f} s, a slightly cautious estimate

So {tau2:g} s of damping adds about {c90-s90:.1f} s to the T90. Enter {tau1+tau2:g} s here as the time constant for a quick conservative answer.

## How response time is measured

Datasheets quote response times from a **plunge test**: the sensor, sitting at room temperature, is plunged into a stirred water bath or a stream of water or air at a stated velocity, and the times to 50% and 90% of the step are recorded. The result depends heavily on the medium and its velocity, so a time constant measured in flowing water says little about the same sensor in still air or in a thermowell. In the plant, you can estimate the installed time constant from a step test: record the reading after a known process step and take the time to 63.2% of the change.

## Lag error during a ramp

When the process changes at a steady rate r, a first-order sensor settles into lagging behind by r × τ:

| Ramp rate | τ = 2 s | τ = 8 s | τ = 30 s | τ = 60 s |
|---|---|---|---|---|
{ramp_rows}
## Common mistakes

- **Treating T90 as the time constant.** T90 is 2.303 τ. Entering a datasheet T90 of 18 s as τ predicts a sensor more than twice as slow as it is.
- **Using a liquid time constant for gas service.** A sensor with τ = 5 s in flowing water can take a minute or more in still air.
- **Forgetting the thermowell.** The well, any air gap and a loose sensor tip often dominate the response, so the bare sensor figure is far too optimistic.
- **Adding damping to a trip loop.** Damping hides noise but adds to the safety function's response time budget; check the total before raising it.
- **Reading too soon during calibration.** In a dry block or bath, wait at least 5 time constants (99.3%) of the whole sensor and block system before recording a point.
''',
     faq_add=[('How much does a temperature sensor lag behind a ramp?',
               f'Once the ramp is established, a first-order sensor reads r × τ behind the process, where r is the ramp rate. A sensor with τ = 8 s in a process rising at 5 °C per minute reads 5 × 8 ÷ 60 = {5*8/60:.2f} °C low.')])

# ---------------------------------------------------------------- Vertical tank volume
vD, vH, vh = 3.0, 5.0, 3.2
vA = math.pi * vD ** 2 / 4
vV = vA * vh * 1000; vVt = vA * vH * 1000; vpc = vh / vH; vk = vA
vtarget = 30000; vht = vtarget / 1000 / vA
wall = 0.008; vDo = vD; vDi = vDo - 2 * wall
oderr = (vDo ** 2 / vDi ** 2 - 1) * 100
GAL = 3.785411784
lv_rows = ''
for lev in (0.5, 1, 1.5, 2, 2.5, 3, 3.2, 3.5, 4, 4.5, 5):
    v = vA * lev
    lv_rows += f"| {lev:g} m | {v*1000:,.0f} L | {v:.2f} m³ | {v*1000/GAL:,.0f} gal | {lev/vH*100:.0f}% |\n"

edit('engineering/vertical-tank-volume', date=U, phrase='vertical tank volume calculator',
     intro="In a vertical cylindrical tank, volume rises in direct proportion to level, so one strapping factor converts a level reading into litres. This vertical tank volume calculator gives liquid volume, total capacity and percent full, as explained in [tank volume from level measurement](https://www.instrumentationblog.in/tank-volume-from-level-measurement/).\n\nOperators, instrument engineers and storage planners use it to turn a level transmitter or a dip reading into inventory, scale a DCS volume display and plan how much a tank can still receive.",
     before='## Capacity per metre of level',
     body_add=f'''
## Worked example

A tank with a **{vD:g} m** inside diameter and **{vH:g} m** straight side holds liquid at **{vh:g} m**:

- Cross-section = π × {vD:g}² ÷ 4 = **{vA:.4f} m²**, which is **{vk:.3f} L per mm** of level
- Liquid volume = {vA:.4f} × {vh:g} = {vV/1000:.3f} m³ = **{vV:,.0f} L**
- Total capacity = {vA:.4f} × {vH:g} = **{vVt:,.0f} L**
- Percent full = {vh:g} ÷ {vH:g} = **{vpc*100:.0f}%**, leaving room for {vVt-vV:,.0f} L

To receive a total of {vtarget:,} L the level must reach {vtarget/1000:g} ÷ {vA:.4f} = **{vht:.3f} m**.

## Level to volume table for this tank

| Level | Volume | m³ | US gallons | Percent full |
|---|---|---|---|---|
{lv_rows}
## Using it with level instruments

Because volume is linear with level, a DCS can show volume by scaling the level transmitter directly: 0 to {vH:g} m becomes 0 to {vVt:,.0f} L. Remember that the transmitter's zero is often a nozzle some distance above the floor, so add that offset to the measured level first. Manual gauging works two ways: an **innage dip** measures the liquid depth directly, and an **ullage (outage) dip** measures from the reference point at the top down to the surface, so level = reference height − ullage. Multiply volume by density for mass; for that, a hydrostatic transmitter measures mass more directly than level does.

## Common mistakes

- **Using the outside diameter.** For a {vDo:g} m outside diameter with an {wall*1000:g} mm wall, the inside diameter is {vDi:.3f} m, and using the outside figure overstates the volume by {oderr:.1f}%.
- **Measuring level from the wrong datum.** Level must be measured from the bottom of the straight side. A transmitter nozzle 300 mm above the floor needs that 300 mm added.
- **Leaving out the bottom.** A cone or dished bottom holds liquid below the straight side; add it separately or the tank seems to empty early.
- **Calling percent full by level the usable capacity.** Overflow nozzles, high level alarms and the roof take up the top, so the safe fill is often 90% or less.
- **Ignoring internals and temperature.** Heating coils, agitators and the thermal expansion of a large tank all shift volume, which is why custody transfer tanks use calibrated strapping tables.
''',
     faq_add=[('How do I find the level from an ullage dip?',
               'Subtract the ullage from the tank reference height: level = reference height − ullage. With a 5.50 m reference height and a 2.30 m ullage, the level is 3.20 m. Then use the level here to get the volume.')])

print('done')
