"""Batch 2026-11-15: 6 calculators. Engineering (DP interface level, bubbler level, mass balance for
mixing two streams), electrical (motor winding resistance unbalance with temperature correction,
soft starter current limit and starting torque) and math (unit circle). All reference tables and
worked examples are computed here from the calculator defaults."""
import sys, math, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page
from ib import intro as _intro
D = '2026-11-15'
pi = math.pi
G0 = 9.80665
DASH = re.compile('[' + chr(0x2013) + chr(0x2014) + ']')
DONE = []


def intro(p1, p2, phrase):
    assert phrase.lower() in p1.lower(), phrase
    t = p1 + '\n\n' + p2
    plain = re.sub(r'\]\(ib:[a-z0-9-]+\)', ']', t)
    n = len(plain.split())
    assert 60 <= n <= 90, (phrase, n)
    return _intro(t)


def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    assert 'featured' not in fm
    assert not DASH.search(fm) and not DASH.search(body), slug
    body = re.sub(r'(?<=[\s(*|;])-(?=\d)', '−', body)
    n = len(body.split())
    assert n >= 520, (slug, n)
    page(cat, slug, fm, body)
    DONE.append(f'{cat}/{slug}')


# ======================================================================= ENGINEERING

# ---------------------------------------------------------------- Interface level by DP
def ilev(H, s1, s2, sf, h):
    dp = (s2 * h + s1 * (H - h) - sf * H) * 1000 * G0
    lrv = (s1 - sf) * H * 1000 * G0
    urv = (s2 - sf) * H * 1000 * G0
    return dict(dp=dp, lrv=lrv, urv=urv, span=urv - lrv, pc=(dp - lrv) / (urv - lrv))
iH, i1, i2, iF, ih = 2.0, 0.85, 1.0, 0.934, 1.2
IL = ilev(iH, i1, i2, iF, ih)
mb = lambda pa: pa / 100
il_rows = ''
for h in (0, 0.25, 0.5, 0.75, 1.0):
    r = ilev(iH, i1, i2, iF, h * iH)
    il_rows += f"| {h*100:.0f}% | {h*iH:.2f} m | {mb(r['dp']):.2f} mbar | {r['dp']/1000/G0*1000:.0f} mmH₂O | {4+16*r['pc']:.2f} mA |\n"
is_rows = ''
for a, b, nm in ((0.70, 1.00, 'Light hydrocarbon on water'), (0.85, 1.00, 'Crude or diesel on water'), (0.92, 1.00, 'Heavy oil on water'),
                 (1.00, 1.20, 'Water on brine (SG 1.2)'), (0.80, 1.60, 'Solvent on chlorinated solvent'), (0.86, 1.84, 'Oil on 98% sulphuric acid')):
    sp = (b - a) * iH * 1000 * G0
    is_rows += f"| {nm} | {a:.2f} | {b:.2f} | {b-a:.2f} | {sp/100:.1f} mbar |\n"
# accuracy effect of a 0.01 SG error in the light phase at 50% interface
r50 = ilev(iH, i1, i2, iF, 0.5 * iH)
r50e = ilev(iH, i1 + 0.01, i2, iF, 0.5 * iH)
err_pc = ((r50e['dp'] - r50['lrv']) / r50['span'] - 0.5) * 100

P('engineering', 'interface-level', f'''
title: Interface Level Calculator (DP Transmitter, Two Liquids)
description: Calculate oil and water interface level from DP transmitter reading, or set the LRV, URV and span for interface measurement with remote seals.
category: engineering
{intro("Interface level is the height of the boundary between two liquids that do not mix, such as oil floating on water in a separator. This interface level calculator gives the DP a transmitter sees, the LRV, URV and span, as explained in [interface level measurement](ib:interface-level-measurement).",
       "Instrument engineers use it to range transmitters on separators, decanters and desalters, and to check quickly whether the density difference is large enough for DP to work.", 'interface level calculator')}
keywords: [interface level calculator, dp interface level measurement, oil water interface level, interface level transmitter range, lrv urv interface level, interface level formula, separator interface level]
published: {D}
updated: {D}
variables:
  - {{ id: H, label: Distance between the HP and LP taps, family: length, unit: mm, imperialUnit: in, default: {iH*1000:g}, min: 0 }}
  - {{ id: s1, label: SG of the upper (light) liquid, default: {i1:g}, min: 0 }}
  - {{ id: s2, label: SG of the lower (heavy) liquid, default: {i2:g}, min: 0 }}
  - {{ id: sf, label: SG of the seal fill fluid or wet leg, default: {iF:g}, min: 0, help: 'Silicone fill fluids are typically 0.93 to 0.97. Enter 0 for a transmitter with direct, dry connections where both taps are always covered by liquid and nothing fills the lines (rare).' }}
  - {{ id: h, label: Interface height above the HP tap, family: length, unit: mm, imperialUnit: in, default: {ih*1000:g}, min: 0, help: 'Must lie between 0 and the tap distance. The vessel must be full so that the LP tap is always covered by the light liquid.' }}
  - {{ id: dp, label: Differential pressure (HP minus LP), family: pressure, unit: mbar, imperialUnit: inH2O }}
  - {{ id: lrv, label: LRV (interface at the HP tap), family: pressure, unit: mbar, imperialUnit: inH2O }}
  - {{ id: urv, label: URV (interface at the LP tap), family: pressure, unit: mbar, imperialUnit: inH2O }}
  - {{ id: span, label: Calibrated span, family: pressure, unit: mbar, imperialUnit: inH2O }}
  - {{ id: pc, label: Interface level (percent of range), family: percent, unit: '%' }}
equations:
  - dp = (s2 * h + s1 * (H - h) - sf * H) * 1000 * g0
  - lrv = (s1 - sf) * H * 1000 * g0
  - urv = (s2 - sf) * H * 1000 * g0
  - span = (s2 - s1) * H * 1000 * g0
  - pc = (dp - lrv) / span
faq:
  - q: How does a DP transmitter measure interface level?
    a: "With the vessel full, the pressure difference between the two taps is the weight of the liquid column between them. Heavy liquid weighs more than light liquid, so the DP rises as the interface moves up. The change from interface at the bottom tap to interface at the top tap is (SG heavy − SG light) × tap distance."
  - q: Why is the LRV negative for interface measurement with remote seals?
    a: "The capillary on the LP side carries a column of fill fluid as tall as the tap distance. If the fill fluid is heavier than the light process liquid, that column outweighs the process liquid above the HP tap and the DP at minimum interface is below zero. This is normal; the transmitter is simply ranged from a negative LRV."
  - q: What density difference is needed for DP interface measurement?
    a: "As a rule of thumb at least 0.1 SG, and more for short tap distances. With a 2 m tap distance and a 0.15 SG difference the span is only about 29 mbar, so a 0.01 SG error in the light liquid moves the reading by several percent. Below about 0.1 SG consider guided wave radar or a displacer instead."
  - q: Can I measure interface level if the vessel is not full?
    a: "Not with a single DP transmitter. If the upper tap is uncovered, the reading depends on both the total level and the interface position. You then need a second measurement of total level, or a technology that sees both surfaces such as guided wave radar."
  - q: Does the transmitter mounting height matter with remote seals?
    a: "For the span and LRV, no: the fill fluid in both capillaries from the transmitter up to the lower tap cancels out, and only the fill fluid column between the two taps remains. Mounting height still matters for the minimum allowed pressure on the seals in vacuum service."
related: [engineering/dp-level-range, engineering/hydrostatic-pressure, engineering/4-20ma-scaling, engineering/bubbler-level, physics/density, engineering/api-gravity]
''', f'''
## How to use the interface level calculator

Enter the **distance between the two taps**, the **specific gravity of the light and heavy liquids**, the **specific gravity of the seal fill fluid** (or of the wet leg) and the **interface height** above the lower tap. The calculator gives the DP the transmitter sees, the LRV and URV to configure, the span and the interface as a percentage of range. To turn a live reading into an interface height, enter the DP and press × on the interface height so it becomes the result.

## Interface level formula

<p class="formula">ΔP = ρ<sub>w</sub> g [SG<sub>2</sub> h + SG<sub>1</sub> (H − h) − SG<sub>f</sub> H]</p>

<p class="formula">LRV = ρ<sub>w</sub> g (SG<sub>1</sub> − SG<sub>f</sub>) H &nbsp;·&nbsp; URV = ρ<sub>w</sub> g (SG<sub>2</sub> − SG<sub>f</sub>) H &nbsp;·&nbsp; span = ρ<sub>w</sub> g (SG<sub>2</sub> − SG<sub>1</sub>) H</p>

H is the tap distance, h the interface height above the HP tap, SG<sub>1</sub> the light liquid, SG<sub>2</sub> the heavy liquid and SG<sub>f</sub> the fill fluid; ρ<sub>w</sub> = 1,000 kg/m³ and g = 9.80665 m/s², so 1 mmH₂O is 9.80665 Pa.

## Worked example

An oil and water separator has taps {iH*1000:,.0f} mm apart, oil of SG {i1:g} on water of SG {i2:g}, and remote seals filled with silicone of SG {iF:g}. The interface is {ih*1000:,.0f} mm above the lower tap:

- LRV = ({i1:g} − {iF:g}) × {iH:g} m × 1,000 × 9.80665 = **{mb(IL['lrv']):.2f} mbar**
- URV = ({i2:g} − {iF:g}) × {iH:g} × 1,000 × 9.80665 = **{mb(IL['urv']):.2f} mbar**
- Span = ({i2:g} − {i1:g}) × {iH:g} × 1,000 × 9.80665 = **{mb(IL['span']):.2f} mbar**
- DP at the interface = ({i2:g} × {ih:g} + {i1:g} × {iH-ih:g} − {iF:g} × {iH:g}) × 9,806.65 = **{mb(IL['dp']):.2f} mbar**
- Interface = ({mb(IL['dp']):.2f} − ({mb(IL['lrv']):.2f})) ÷ {mb(IL['span']):.2f} = **{IL['pc']*100:.1f}%** of range, which checks against {ih:g} ÷ {iH:g} = {ih/iH*100:.0f}%

## DP and output across the range

For the example separator ({iH*1000:,.0f} mm taps, SG {i1:g} over {i2:g}, fill SG {iF:g}):

| Interface (% of range) | Height above HP tap | DP | DP | Output (4 to 20 mA) |
|---|---|---|---|---|
{il_rows}
## Span for common liquid pairs

For a {iH*1000:,.0f} mm tap distance. The span is independent of the fill fluid:

| Liquid pair | SG light | SG heavy | SG difference | Span |
|---|---|---|---|---|
{is_rows}
## How interface level is measured in practice

Most separators use a DP transmitter with **two flush diaphragm seals** and capillaries, because the process liquids are often hot, waxy or corrosive and impulse lines would plug. The seals are mounted on nozzles above and below the expected interface band, and the vessel is kept liquid full, usually by an overflow weir or by level control on the total level. The transmitter can be mounted at or below the lower tap. The range is set from the LRV and URV calculated above, then checked by sampling the vessel at its try cocks or sight glass.

Other technologies are common where DP is weak: **guided wave radar** sees both the top surface and the interface when the upper liquid has a low dielectric constant; **displacers** work well over short ranges; and **capacitance** or **nuclear density profilers** handle emulsion bands in desalters.

## Common mistakes

- **Leaving the LP tap uncovered.** If the top of the vessel contains gas, the transmitter measures a mix of total level and interface and the reading is meaningless.
- **Using design densities that do not match the process.** A 0.01 SG change in the oil at 50% interface moves this example reading by {err_pc:+.1f}% of range, so use the measured density at operating temperature.
- **Forgetting the fill fluid column.** Ranging the transmitter from 0 instead of the negative LRV puts the whole range out by the weight of the capillary fill.
- **Ignoring the emulsion layer.** A DP transmitter reports one average interface; a thick rag layer between oil and water shifts the reading toward the middle of the band.
- **Placing taps outside the interface band.** The interface must stay between the taps; outside them the output saturates at 0% or 100% and hides the real position.
''')

# ---------------------------------------------------------------- Bubbler (purge) level
def bub(Pmbar, sg, zmm, Lmax):
    Ppa = Pmbar * 100
    h = Ppa / (sg * 1000 * G0)
    L = h + zmm / 1000
    Pmax = sg * 1000 * G0 * (Lmax - zmm / 1000)
    return dict(h=h, L=L, Pmax=Pmax, pc=L / Lmax)
bP, bS, bZ, bL = 250.0, 1.05, 100.0, 3.0
BB = bub(bP, bS, bZ, bL)
bt_rows = ''
for L in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
    bt_rows += f"| {L:.1f} m | " + ' | '.join(f"{sg*1000*G0*(L-bZ/1000)/100:.1f} mbar" for sg in (0.8, 1.0, 1.05, 1.2, 1.4)) + " |\n"
# density by two dip tubes 1 m apart
d2_rows = ''
for dP in (78.5, 98.1, 103.0, 117.7, 137.3):
    d2_rows += f"| {dP:.1f} mbar | {dP*100/(G0*1.0):,.0f} kg/m³ | {dP*100/(G0*1.0)/1000:.3f} |\n"

P('engineering', 'bubbler-level', f'''
title: Bubbler Level Calculator (Purge Dip Tube Back Pressure)
description: Convert bubbler (purge) dip tube back pressure to tank level for any liquid density, and find the maximum back pressure to size the transmitter.
category: engineering
{intro("A bubbler pushes a small flow of air down a dip tube, and the pressure needed to release bubbles equals the liquid head above the tube end. This bubbler level calculator turns that back pressure into level, as described in [bubbler level measurement with a purge](ib:bubbler-level-measurement-purge).",
       "Instrument engineers use it to range the transmitter and check readings. Bubblers suit sludge, slurries and corrosive liquids, because only the dip tube touches the process.", 'bubbler level calculator')}
keywords: [bubbler level calculator, bubbler level measurement, purge level measurement, dip tube level calculation, back pressure to level, bubbler tube level formula, air purge level system]
published: {D}
updated: {D}
variables:
  - {{ id: Pb, label: Dip tube back pressure (gauge), family: pressure, unit: mbar, imperialUnit: inH2O, default: {bP:g}, min: 0, help: 'Measured by the transmitter on the purge line, relative to the tank vapour space (an open tank: relative to atmosphere).' }}
  - {{ id: sg, label: Liquid specific gravity, default: {bS:g}, min: 0 }}
  - {{ id: z, label: Height of dip tube end above tank bottom, family: length, unit: mm, imperialUnit: in, default: {bZ:g}, min: 0 }}
  - {{ id: Lmax, label: Maximum level (from tank bottom), family: length, unit: m, imperialUnit: ft, default: {bL:g}, min: 0 }}
  - {{ id: h, label: Liquid head above the dip tube end, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: L, label: Level above tank bottom, family: length, unit: m, imperialUnit: ft, min: 0 }}
  - {{ id: Pmax, label: Back pressure at maximum level (URV), family: pressure, unit: mbar, imperialUnit: inH2O, min: 0 }}
  - {{ id: pc, label: Level (percent of maximum), family: percent, unit: '%' }}
equations:
  - h = Pb / (sg * 1000 * g0)
  - L = h + z
  - Pmax = sg * 1000 * g0 * (Lmax - z)
  - pc = L / Lmax
faq:
  - q: How does a bubbler level system work?
    a: "Gas flows through a regulator and a small rotameter into a dip tube that reaches near the tank bottom. The gas pressure rises until it equals the liquid head at the tube end, then bubbles escape. From then on the pressure in the tube, measured by a gauge or transmitter, follows the level: level = back pressure ÷ (density × g)."
  - q: How much purge flow does a bubbler need?
    a: "Only enough for a slow, steady stream of bubbles, often around 1 standard cubic foot per hour (about 0.5 L/min). Too much flow adds friction loss in the tube and makes the reading high and noisy; too little lets liquid creep up the tube and slows the response when the level rises."
  - q: Why does the bubbler not read down to the tank bottom?
    a: "The back pressure is the head above the tube end, so the measurement starts at the tube end. The tube is kept a little above the bottom to stay clear of sludge, and the calculator adds that height back so the level is reported from the tank bottom."
  - q: Can a bubbler be used on a closed or pressurised tank?
    a: "Yes, with a DP transmitter: the HP side connects to the purge line and the LP side to the vapour space. The DP is then the liquid head alone, and the gas supply pressure must exceed the tank pressure plus the maximum head."
  - q: Can bubblers measure density as well as level?
    a: "Yes. Two dip tubes ending at a known vertical distance apart give a pressure difference that depends only on density: ρ = ΔP ÷ (g × Δz). This is used in sugar, mining and chemical tanks, and the density can then compensate the level reading."
related: [engineering/hydrostatic-pressure, engineering/dp-level-range, engineering/interface-level, engineering/ultrasonic-level, engineering/vertical-tank-volume, engineering/4-20ma-scaling]
''', f'''
## How to use the bubbler level calculator

Enter the **back pressure** measured on the purge line, the **specific gravity** of the liquid, the **height of the dip tube end** above the tank bottom and the **maximum level** you need to measure. The calculator gives the head above the tube end, the level from the tank bottom, the level as a percentage of maximum and the back pressure at maximum level, which is the URV for the transmitter. To find the back pressure for a known level, enter the level and press × on the back pressure.

## Bubbler level formula

<p class="formula">h = P<sub>b</sub> ÷ (SG × ρ<sub>w</sub> × g) &nbsp;·&nbsp; L = h + z &nbsp;·&nbsp; P<sub>max</sub> = SG × ρ<sub>w</sub> × g × (L<sub>max</sub> − z)</p>

P<sub>b</sub> is the gauge back pressure in Pa, ρ<sub>w</sub> = 1,000 kg/m³, g = 9.80665 m/s² and z the height of the tube end above the bottom. The transmitter is ranged from 0 (level at the tube end) to P<sub>max</sub>.

## Worked example

A tank of liquor with SG {bS:g} has a dip tube ending {bZ:g} mm above the bottom and a maximum level of {bL:g} m. The transmitter reads **{bP:g} mbar**:

- Head above the tube end h = {bP*100:,.0f} Pa ÷ ({bS:g} × 1,000 × 9.80665) = **{BB['h']:.3f} m**
- Level from the bottom L = {BB['h']:.3f} + {bZ/1000:.3f} = **{BB['L']:.3f} m**, or **{BB['pc']*100:.1f}%** of the {bL:g} m maximum
- Back pressure at maximum level = {bS:g} × 1,000 × 9.80665 × ({bL:g} − {bZ/1000:.1f}) = **{BB['Pmax']/100:.1f} mbar**, so range the transmitter 0 to {BB['Pmax']/100:.0f} mbar and set the gas regulator comfortably above that

## Back pressure by level and density

For a dip tube {bZ:g} mm above the bottom:

| Level | SG 0.8 | SG 1.0 | SG 1.05 | SG 1.2 | SG 1.4 |
|---|---|---|---|---|---|
{bt_rows}
## Density from two dip tubes

Two tubes whose ends are 1.000 m apart vertically give a pressure difference that depends only on density:

| ΔP between tubes | Density | SG |
|---|---|---|
{d2_rows}
## How a bubbler is installed

A typical panel has a filter regulator, a **differential pressure flow regulator** or needle valve with a small rotameter, a check valve and the pressure transmitter, teed into the purge line close to the tank. The dip tube is usually 15 to 25 mm pipe in a material that suits the liquid, often with a notch or a 45° cut at the end so bubbles leave evenly instead of pulsing. Instrument air is common; nitrogen is used where air would oxidise or contaminate the product. Because the transmitter never touches the liquid, it can be mounted at a convenient height, and the tube can be rodded out or blown down if it fouls.

## Common mistakes

- **Purging too hard.** Friction in a long or narrow purge line adds pressure that is not liquid head, so the level reads high. Keep the flow low and the transmitter tee near the tank.
- **Forgetting the tube end offset.** The bubbler measures from the tube end, not from the tank bottom; adding z back is essential for volume calculations.
- **Using the wrong density.** Level is inversely proportional to SG, so a 5% density error gives a 5% level error. Use the density at operating temperature, or add a second tube for density compensation.
- **Gas supply pressure set too low.** If the supply is below the maximum back pressure, purge flow stops before the tank is full and the reading freezes.
- **Ignoring pressure in a closed tank.** In a vented or pressurised tank the reading must be referenced to the vapour space with a DP transmitter, or any tank pressure appears as false level.
''')

# ---------------------------------------------------------------- Mass balance (mixing two streams)
def mix(m1, x1, m2, x2, xt):
    m3 = m1 + m2
    mc = m1 * x1 + m2 * x2
    return dict(m3=m3, mc=mc, x3=mc / m3, m2r=m1 * (x1 - xt) / (xt - x2))
mm1, mx1, mm2, mx2, mxt = 1200.0, 0.32, 800.0, 0.05, 0.20
MX = mix(mm1, mx1, mm2, mx2, mxt)
md_rows = ''
for xt in (0.40, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05):
    w = 1000 * (0.50 - xt) / xt
    md_rows += f"| {xt*100:.0f}% | {w:,.0f} kg | {1000+w:,.0f} kg | {(1000+w)/1000:.2f} |\n"
ms_rows = ''
for f in (0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0):
    m2 = mm1 * f; x3 = (mm1 * mx1 + m2 * mx2) / (mm1 + m2)
    ms_rows += f"| {m2:,.0f} kg/h | {mm1+m2:,.0f} kg/h | {x3*100:.2f}% |\n"

P('engineering', 'mass-balance', f'''
title: Mass Balance Calculator (Mixing Two Streams, Blending)
description: Do a mass balance for mixing two streams: find the outlet flow and concentration, or the flow of one stream needed to hit a target blend.
category: engineering
{intro("A mass balance says that what enters a mixing point must leave it, both in total and for each component. This mass balance calculator combines two streams of different flow and concentration, giving the outlet flow and strength, and the flow of the second stream needed for a target blend.",
       "Process engineers use it to size dilution water for acids and caustic, to blend products and to check plant data; students use it for material balance problems.", 'mass balance calculator')}
keywords: [mass balance calculator, mixing two streams, blending calculation, material balance calculator, mixing concentration calculator, dilution water flow, component mass balance]
published: {D}
updated: {D}
variables:
  - {{ id: m1, label: Stream 1 mass flow, family: massflow, unit: kgh, imperialUnit: lbh, default: {mm1:g}, min: 0 }}
  - {{ id: x1, label: Stream 1 concentration (mass fraction), family: percent, unit: '%', default: {mx1*100:g}, min: 0, max: 1 }}
  - {{ id: m2, label: Stream 2 mass flow, family: massflow, unit: kgh, imperialUnit: lbh, default: {mm2:g}, min: 0 }}
  - {{ id: x2, label: Stream 2 concentration (mass fraction), family: percent, unit: '%', default: {mx2*100:g}, min: 0, max: 1, help: 'Enter 0 for pure water or solvent used as diluent.' }}
  - {{ id: xt, label: Target concentration (for the flow needed below), family: percent, unit: '%', default: {mxt*100:g}, min: 0, max: 1, help: 'Must lie between the two stream concentrations.' }}
  - {{ id: m3, label: Mixed (outlet) mass flow, family: massflow, unit: kgh, imperialUnit: lbh, min: 0 }}
  - {{ id: mc, label: Component mass flow in the outlet, family: massflow, unit: kgh, imperialUnit: lbh, min: 0 }}
  - {{ id: x3, label: Mixed concentration, family: percent, unit: '%', min: 0 }}
  - {{ id: m2r, label: Stream 2 flow needed for the target, family: massflow, unit: kgh, imperialUnit: lbh }}
equations:
  - m3 = m1 + m2
  - mc = m1 * x1 + m2 * x2
  - x3 = mc / m3
  - m2r = m1 * (x1 - xt) / (xt - x2)
faq:
  - q: What is the mass balance equation for mixing?
    a: "Total mass: m₃ = m₁ + m₂. Component: m₃ x₃ = m₁ x₁ + m₂ x₂, where x is the mass fraction of the component. Dividing gives the mixed concentration x₃ = (m₁ x₁ + m₂ x₂) ÷ (m₁ + m₂). Mass is conserved with or without chemical reaction, but component balances only hold for non-reacting components."
  - q: How much water do I need to dilute a solution?
    a: "Water flow = m₁ (x₁ − x_target) ÷ x_target, which is the formula above with x₂ = 0. Diluting 1,000 kg of 50% caustic to 20% needs 1,000 × 0.30 ÷ 0.20 = 1,500 kg of water, giving 2,500 kg of solution."
  - q: Can I use volume flows instead of mass flows?
    a: "Only if the densities are equal and the liquids do not shrink on mixing. Concentrated acids, caustic and alcohol solutions change volume when diluted, so convert volume flows to mass with each stream's density first, or use mass flow meters."
  - q: What is the lever rule?
    a: "A graphical form of the same balance: the ratio of the two stream flows equals the inverse ratio of their distances from the mixed concentration, m₁ ÷ m₂ = (x₃ − x₂) ÷ (x₁ − x₃). It is quick for mental checks on blends."
related: [chemistry/dilution, chemistry/mass-percent, physics/final-temperature, engineering/mass-flow-rate, engineering/residence-time, chemistry/solution-preparation]
''', f'''
## How to use the mass balance calculator

Enter the **mass flow and concentration** of each incoming stream. Concentration is the mass fraction of the component you are tracking, such as acid, salt, sugar or a fuel component, as a percentage. The calculator gives the **outlet flow**, the **component flow** and the **mixed concentration**. Enter a **target concentration** to see how much of stream 2 would be needed with the stream 1 flow you entered. Any field can be solved: clear one and enter a known result instead.

## Mass balance formulas

<p class="formula">m<sub>3</sub> = m<sub>1</sub> + m<sub>2</sub> &nbsp;·&nbsp; m<sub>3</sub> x<sub>3</sub> = m<sub>1</sub> x<sub>1</sub> + m<sub>2</sub> x<sub>2</sub></p>

<p class="formula">m<sub>2,needed</sub> = m<sub>1</sub> (x<sub>1</sub> − x<sub>t</sub>) ÷ (x<sub>t</sub> − x<sub>2</sub>)</p>

The same equations work for any consistent units: kg/h, t/h or a batch in kg.

## Worked example

{mm1:,.0f} kg/h of {mx1*100:g}% caustic soda is mixed with {mm2:,.0f} kg/h of a {mx2*100:g}% weak caustic return stream:

- Outlet flow = {mm1:,.0f} + {mm2:,.0f} = **{MX['m3']:,.0f} kg/h**
- NaOH flow = {mm1:,.0f} × {mx1:g} + {mm2:,.0f} × {mx2:g} = {mm1*mx1:,.0f} + {mm2*mx2:,.0f} = **{MX['mc']:,.0f} kg/h**
- Mixed concentration = {MX['mc']:,.0f} ÷ {MX['m3']:,.0f} = **{MX['x3']*100:.1f}%**
- To make exactly {mxt*100:g}% instead, stream 2 must be {mm1:,.0f} × ({mx1:g} − {mxt:g}) ÷ ({mxt:g} − {mx2:g}) = **{MX['m2r']:,.0f} kg/h**

## Outlet strength as stream 2 increases

Stream 1 fixed at {mm1:,.0f} kg/h of {mx1*100:g}%, stream 2 at {mx2*100:g}%:

| Stream 2 flow | Outlet flow | Outlet concentration |
|---|---|---|
{ms_rows}
## Water needed to dilute 1,000 kg of 50% solution

| Target strength | Water to add | Final mass | Mass ratio final ÷ initial |
|---|---|---|---|
{md_rows}
## Mass balances in practice

On a plant, the balance is used two ways. In **design**, it sizes the dilution water flow meter and control valve for a target strength, and sets the ratio for a ratio controller that trims water flow against the concentrate flow. In **operation**, it reconciles measured data: if the outlet analyser and the inlet flows disagree, at least one meter or analyser is wrong. A useful habit is to check the total balance first, then each component, and to close the balance within the combined uncertainty of the meters, typically 1 to 2% for good mass flow measurement.

Real mixing also has an energy balance. Diluting strong acid or caustic releases heat of solution, so the outlet can be much hotter than a simple average; use the [final temperature calculator](/physics/final-temperature/) only for liquids without significant heat of mixing.

## Common mistakes

- **Mixing mass and volume.** Entering one stream in litres and the other in kilograms breaks the balance unless you convert with the correct densities.
- **Mixing up concentration bases.** Mass percent, volume percent, molarity and g/L are not interchangeable; convert all streams to mass fraction before mixing.
- **Target outside the feed range.** The blend can only fall between the two feed concentrations; a target outside that range gives a negative flow.
- **Ignoring reactions.** If the streams react, such as acid with alkali, the component balance must include the reaction; total mass is still conserved.
- **Averaging percentages.** The mixed strength is a flow-weighted average, not the simple average of the two percentages.
''')

# ======================================================================= ELECTRICAL

# ---------------------------------------------------------------- Motor winding resistance unbalance
def wind(R1, R2, R3, Tm, Tr, k):
    Ra = (R1 + R2 + R3) / 3
    dev = max(abs(R1 - Ra), abs(R2 - Ra), abs(R3 - Ra))
    u = dev / Ra
    mm = (max(R1, R2, R3) - min(R1, R2, R3)) / min(R1, R2, R3)
    Rc = Ra * (k + Tr) / (k + Tm)
    return dict(Ra=Ra, dev=dev, u=u, mm=mm, Rc=Rc)
w1, w2, w3, wT, wR, wk = 0.512, 0.508, 0.521, 32.0, 25.0, 234.5
WR = wind(w1, w2, w3, wT, wR, wk)
wt_rows = ''
for T in (10, 20, 25, 40, 60, 75, 95):
    wt_rows += f"| {T} °C | {(234.5+T)/(234.5+25):.4f} | {(225+T)/(225+25):.4f} | {1.0*(234.5+75)/(234.5+T):.4f} |\n"
ws_rows = ''
for f in (0.005, 0.01, 0.02, 0.03, 0.05, 0.10):
    r = wind(0.510, 0.510, 0.510 * (1 + f), 25, 25, 234.5)
    ws_rows += f"| +{f*100:g}% | {0.510*(1+f):.4f} Ω | {r['u']*100:.2f}% | {r['mm']*100:.2f}% |\n"
WVERD = (f"At {WR['u']*100:.2f}% the unbalance is inside the common 2% alert level, but the max to min spread of {WR['mm']*100:.1f}% would exceed it, "
         "which is why a test sheet must say which definition it uses. Trend the readings against earlier tests before deciding.") if WR['u'] < 0.02 else \
        (f"At {WR['u']*100:.2f}% the winding is over the common 2% alert level, so re-check the connections and retest.")

P('electrical', 'motor-winding-resistance-unbalance', f'''
title: Motor Winding Resistance Unbalance Calculator
description: Calculate the percent unbalance of three motor winding resistance readings and correct the average to a reference temperature for copper or aluminium.
category: electrical
{intro("A winding resistance test measures the DC resistance of each motor phase with a low resistance ohmmeter. This motor winding resistance unbalance calculator gives the average, the percent unbalance and the spread, and corrects the average to a reference temperature, as covered in [the motor winding resistance test](ib:motor-winding-resistance-test).",
       "Maintenance electricians and rewind shops use it to find shorted turns, loose joints and broken strands before a fault burns out the winding.", 'motor winding resistance unbalance calculator')}
keywords: [motor winding resistance unbalance calculator, winding resistance test, resistance unbalance formula, motor winding resistance temperature correction, phase resistance imbalance, three phase motor resistance test]
published: {D}
updated: {D}
variables:
  - {{ id: R1, label: Resistance U to V (or phase 1), family: resistance, unit: ohm, default: {w1:g}, min: 0 }}
  - {{ id: R2, label: Resistance V to W (or phase 2), family: resistance, unit: ohm, default: {w2:g}, min: 0 }}
  - {{ id: R3, label: Resistance W to U (or phase 3), family: resistance, unit: ohm, default: {w3:g}, min: 0 }}
  - {{ id: Tm, label: Winding temperature during the test, family: temperature, unit: C, imperialUnit: F, default: {wT:g} }}
  - {{ id: Tr, label: Reference temperature, family: temperature, unit: C, imperialUnit: F, default: {wR:g}, help: 'Use 25 °C to compare with factory data, or the value on the test sheet. 75 °C is often used for efficiency and loss calculations.' }}
  - id: k
    label: Winding material
    default: {wk:g}
    options:
      - {{ label: 'Copper (k = 234.5)', value: 234.5 }}
      - {{ label: 'Aluminium (k = 225)', value: 225 }}
  - {{ id: Ra, label: Average resistance, family: resistance, unit: ohm, min: 0 }}
  - {{ id: dev, label: Largest deviation from the average, family: resistance, unit: mohm, min: 0 }}
  - {{ id: u, label: Resistance unbalance (max deviation ÷ average), family: percent, unit: '%', min: 0 }}
  - {{ id: mm, label: Spread (max − min) ÷ min, family: percent, unit: '%', min: 0 }}
  - {{ id: Rc, label: Average resistance at reference temperature, family: resistance, unit: ohm, min: 0 }}
equations:
  - Ra = (R1 + R2 + R3) / 3
  - dev = max(max(abs(R1 - Ra), abs(R2 - Ra)), abs(R3 - Ra))
  - u = dev / Ra
  - mm = (max(max(R1, R2), R3) - min(min(R1, R2), R3)) / min(min(R1, R2), R3)
  - Rc = Ra * (k + Tr - 273.15) / (k + Tm - 273.15)
faq:
  - q: How do you calculate winding resistance unbalance?
    a: "Average the three readings, find the reading furthest from the average, and divide that deviation by the average: unbalance = max |R − R_avg| ÷ R_avg × 100%. Some test sheets use (R_max − R_min) ÷ R_min instead, which gives roughly twice the figure, so always state which definition you use."
  - q: What is an acceptable resistance unbalance for a motor?
    a: "Common maintenance practice treats readings within about 1 to 2% of the average as normal for a healthy winding. Unbalance above about 2% is worth investigating, and above about 5% usually points to a real defect such as shorted turns, a high resistance joint or broken strands. Follow the manufacturer or your test standard where they give a limit."
  - q: Why correct winding resistance to a reference temperature?
    a: "Copper resistance rises about 0.39% per °C near room temperature, so a reading on a warm motor is not comparable with factory data at 25 °C. The correction R_ref = R × (234.5 + T_ref) ÷ (234.5 + T) for copper, or 225 for aluminium, puts all results on the same basis. Unbalance itself needs no correction because all three phases are at the same temperature."
  - q: Why use a low resistance ohmmeter instead of a multimeter?
    a: "Motor windings are often well below 1 Ω, so the test leads and contact resistance of a two wire multimeter swamp the reading. A four wire (Kelvin) micro ohmmeter injects a test current through one pair of leads and measures voltage with another, so lead resistance drops out and milliohm differences become visible."
  - q: Do I measure line to line or phase resistance?
    a: "On a three terminal motor you can only measure line to line. In star, each reading is two phase windings in series, so phase resistance is half the reading. In delta, each reading is one winding in parallel with the other two in series, so phase resistance is 1.5 times the reading. Unbalance can be judged on the line to line readings directly."
related: [electrical/voltage-unbalance, electrical/wire-resistance, electrical/polarization-index, electrical/three-phase-motor-power, electrical/induction-motor-slip, electrical/motor-starting-current]
''', f'''
## How to use the motor winding resistance unbalance calculator

Enter the **three resistance readings** from your low resistance ohmmeter, line to line on U to V, V to W and W to U for a three terminal motor, or per phase when all six leads are brought out. Add the **winding temperature** during the test (from an embedded RTD, or ambient for a motor that has been idle for several hours), the **reference temperature** and the **winding material**. The calculator gives the average, the largest deviation, the unbalance in two common forms and the average corrected to the reference temperature.

## Winding resistance unbalance formulas

<p class="formula">R<sub>avg</sub> = (R<sub>1</sub> + R<sub>2</sub> + R<sub>3</sub>) ÷ 3 &nbsp;·&nbsp; unbalance = max|R<sub>i</sub> − R<sub>avg</sub>| ÷ R<sub>avg</sub> × 100%</p>

<p class="formula">R<sub>ref</sub> = R<sub>avg</sub> × (k + T<sub>ref</sub>) ÷ (k + T<sub>test</sub>), &nbsp; k = 234.5 for copper, 225 for aluminium</p>

## Worked example

A motor is tested at {wT:g} °C and reads **{w1:g}, {w2:g} and {w3:g} Ω** line to line:

- Average = ({w1:g} + {w2:g} + {w3:g}) ÷ 3 = **{WR['Ra']:.4f} Ω**
- Deviations: {(w1-WR['Ra'])*1000:+.2f}, {(w2-WR['Ra'])*1000:+.2f} and {(w3-WR['Ra'])*1000:+.2f} mΩ, so the largest is **{WR['dev']*1000:.2f} mΩ**
- Unbalance = {WR['dev']*1000:.2f} ÷ {WR['Ra']*1000:.1f} = **{WR['u']*100:.2f}%**; the max to min spread is ({w3:g} − {w2:g}) ÷ {w2:g} = **{WR['mm']*100:.2f}%**
- Corrected to {wR:g} °C: {WR['Ra']:.4f} × (234.5 + {wR:g}) ÷ (234.5 + {wT:g}) = **{WR['Rc']:.4f} Ω**

{WVERD}

## Temperature correction factors

Multiply a reading at the test temperature by the factor in the column you need:

| Test temperature | Copper, to 25 °C | Aluminium, to 25 °C | Copper, to 75 °C |
|---|---|---|---|
{wt_rows}
## How one faulty phase shows up

Two readings of 0.5100 Ω and one reading higher by the amount shown, as from a loose lug or a few broken strands:

| Third reading high by | Third reading | Unbalance (from average) | Spread (max − min) ÷ min |
|---|---|---|---|
{ws_rows}
Because the average includes the faulty phase, the deviation from average is only about two thirds of the actual change, and the spread is close to the change itself.

## How the test is done

Isolate and lock out the motor, disconnect the supply cables at the terminal box so the cable is not in the measurement, and remove the star or delta links if you want each phase separately. Use a four wire micro ohmmeter with a test current of at least 1 A, and wait for the reading to settle, because winding inductance makes the current rise slowly. Take each reading in both current directions and average them to cancel thermal EMFs. Record the temperature at the same time. Comparing results with earlier tests on the same motor is often more useful than any fixed limit.

## Common mistakes

- **Testing through the cable.** A long supply cable adds its own resistance and connection joints to each reading and can hide or create an unbalance.
- **Using a two wire meter.** Lead and probe contact resistance of tens of milliohms is the same size as the differences you are looking for.
- **Not waiting for the reading to stabilise.** Large windings have long time constants; an early reading is too low and varies from phase to phase.
- **Correcting unbalance for temperature.** All phases are at the same temperature, so correct the average, not the percentage.
- **Comparing with a different definition.** Max deviation from average and (max − min) ÷ min differ by about a factor of two; use the one your acceptance criterion uses.
''')

# ---------------------------------------------------------------- Soft starter current and torque
def soft(FLC, k, LRT, Il, Tl):
    v = Il / k
    return dict(Is=Il * FLC, v=v, Ts=v * v * LRT, Ilmin=k * math.sqrt(Tl / LRT), mg=v * v * LRT / Tl, Idol=k * FLC)
sF, sK, sT, sI, sL = 100.0, 6.5, 1.6, 3.5, 0.30
SS = soft(sF, sK, sT, sI, sL)
st_rows = ''
for Il in (2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0):
    r = soft(sF, sK, sT, Il, sL)
    st_rows += f"| {Il:.1f} × FLC | {r['v']*100:.0f}% | {r['Ts']*100:.0f}% | {r['Ts']/(sT)*100:.0f}% |\n"
sl_rows = ''
for nm, Tl in (('Centrifugal pump (valve closed)', 0.10), ('Centrifugal fan (damper closed)', 0.15), ('Centrifugal pump (against static head)', 0.30),
               ('Screw compressor (unloaded)', 0.35), ('Loaded conveyor', 0.80), ('Crusher or mixer under load', 1.0)):
    st_rows2 = sK * math.sqrt(Tl * 1.0 / sT)
    sl_rows += f"| {nm} | {Tl*100:.0f}% | {st_rows2:.2f} × FLC | {sK*math.sqrt(Tl*1.5/sT):.2f} × FLC |\n"

P('electrical', 'soft-starter-current', f'''
title: Soft Starter Current Calculator (Current Limit & Torque)
description: Calculate soft starter starting current, motor voltage and starting torque from the current limit setting, and the minimum current limit for the load.
category: electrical
{intro("A soft starter lowers motor voltage during starting, which cuts inrush current but also starting torque. This soft starter current calculator turns a current limit setting and the locked rotor data into starting current, motor voltage and starting torque, as explained in [how a soft starter works](ib:soft-starter-working-principle).",
       "Electrical engineers use it to set current limits, check that a generator or weak supply can start the motor, and confirm the load will still accelerate.", 'soft starter current calculator')}
keywords: [soft starter current calculator, soft starter current limit setting, soft starter starting torque, soft starter inrush current, reduced voltage starting torque, soft start current limit calculation]
published: {D}
updated: {D}
variables:
  - {{ id: FLC, label: Motor full-load current, family: current, unit: A, default: {sF:g}, min: 0 }}
  - {{ id: k, label: Locked rotor current (× FLC), default: {sK:g}, min: 1, help: 'From the motor datasheet (IA/IN), typically 5.5 to 8 for IE2 and IE3 motors.' }}
  - {{ id: LRT, label: Locked rotor torque (% of full-load torque), family: percent, unit: '%', default: {sT*100:g}, min: 0, help: 'From the datasheet (TA/TN or MA/MN), typically 130 to 250%.' }}
  - {{ id: Il, label: Soft starter current limit (× FLC), default: {sI:g}, min: 0 }}
  - {{ id: Tl, label: Load breakaway torque (% of motor full-load torque), family: percent, unit: '%', default: {sL*100:g}, min: 0 }}
  - {{ id: Is, label: Starting current (line), family: current, unit: A, min: 0 }}
  - {{ id: Idol, label: Direct on line starting current, family: current, unit: A, min: 0 }}
  - {{ id: v, label: Effective motor voltage at current limit, family: percent, unit: '%', min: 0 }}
  - {{ id: Ts, label: Starting torque (% of full-load torque), family: percent, unit: '%', min: 0 }}
  - {{ id: mg, label: Starting torque ÷ load torque, min: 0, decimals: 2 }}
  - {{ id: Ilmin, label: Current limit at which motor torque equals load torque, suffix: × FLC, min: 0, decimals: 2 }}
equations:
  - Is = Il * FLC
  - Idol = k * FLC
  - v = Il / k
  - Ts = v ^ 2 * LRT
  - mg = Ts / Tl
  - Ilmin = k * sqrt(Tl / LRT)
faq:
  - q: How does a soft starter reduce starting current?
    a: "Thyristors in each phase switch on part way through each half cycle, so the motor sees a reduced RMS voltage. At standstill an induction motor behaves like a fixed impedance, so its current falls in proportion to voltage: at 50% voltage it draws half its locked rotor current."
  - q: Why does a soft starter reduce starting torque so much?
    a: "Torque is proportional to voltage squared. Limiting current to 3.5 × FLC on a motor with 6.5 × FLC locked rotor current means 54% voltage and only 29% of the locked rotor torque. That is why soft starters suit pumps and fans, whose torque is low at low speed, better than loaded conveyors or crushers."
  - q: What current limit should I set on a soft starter?
    a: "High enough that motor torque clearly exceeds the load torque through the whole acceleration, usually 3 to 4 × FLC for pumps and fans and 4 to 5 × FLC for heavier loads. A common check is that the starting torque at the current limit is at least about 1.5 times the load torque so the motor accelerates in a reasonable time."
  - q: What is the difference between a soft starter and a VFD for starting?
    a: "A soft starter only lowers voltage at fixed 50 or 60 Hz, so current and torque fall together. A VFD lowers voltage and frequency together and can produce full rated torque at about rated current. Use a VFD when the load needs high starting torque from a weak supply."
  - q: Does starting with a soft starter heat the motor less?
    a: "Not necessarily. The rotor heat in a start is roughly equal to the kinetic energy given to the load, and a longer, lower torque start can add more heating. Check the allowed starts per hour of both the motor and the soft starter for long or frequent starts."
related: [electrical/motor-starting-current, electrical/motor-starting-voltage-dip, electrical/three-phase-motor-power, electrical/generator-size, electrical/induction-motor-slip, engineering/torque-power-speed]
''', f'''
## How to use the soft starter current calculator

Enter the motor **full-load current**, the **locked rotor current** and **locked rotor torque** from the motor datasheet, the **current limit** you plan to set on the soft starter and the **breakaway torque** of the load as a percentage of motor full-load torque. The calculator gives the starting current drawn from the supply, the equivalent motor voltage, the starting torque, the ratio of motor torque to load torque and the lowest current limit at which the motor could just hold the load. Any input can be solved: for example, enter a required starting torque and press × on the current limit.

## Soft starter formulas

<p class="formula">V ÷ V<sub>N</sub> = I<sub>limit</sub> ÷ I<sub>LR</sub> &nbsp;·&nbsp; T<sub>start</sub> = (V ÷ V<sub>N</sub>)² × T<sub>LR</sub></p>

<p class="formula">I<sub>limit,min</sub> = I<sub>LR</sub> × √(T<sub>load</sub> ÷ T<sub>LR</sub>)</p>

These follow from the motor behaving as a fixed impedance at standstill: current is proportional to voltage and torque to voltage squared.

## Worked example

A {sF:g} A motor has a locked rotor current of {sK:g} × FLC and a locked rotor torque of {sT*100:.0f}%. It drives a pump needing {sL*100:.0f}% torque to break away against static head, and the soft starter is set to {sI:g} × FLC:

- Starting current = {sI:g} × {sF:g} = **{SS['Is']:.0f} A**, against **{SS['Idol']:.0f} A** direct on line
- Effective voltage = {sI:g} ÷ {sK:g} = **{SS['v']*100:.1f}%**
- Starting torque = {SS['v']:.4f}² × {sT*100:.0f}% = **{SS['Ts']*100:.1f}%** of full-load torque
- Torque margin = {SS['Ts']*100:.1f} ÷ {sL*100:.0f} = **{SS['mg']:.2f}**, so the pump will start
- Lowest workable current limit = {sK:g} × √({sL:g} ÷ {sT:g}) = **{SS['Ilmin']:.2f} × FLC**; in practice set comfortably above this

## Starting torque by current limit

For the example motor ({sK:g} × FLC locked rotor current, {sT*100:.0f}% locked rotor torque):

| Current limit | Motor voltage | Starting torque (% of FLT) | Torque as % of DOL starting torque |
|---|---|---|---|
{st_rows}
## Minimum current limit for typical loads

Breakaway torques are typical values; check the actual load curve. The last column allows the motor torque to be 1.5 times the load torque:

| Load | Breakaway torque | Limit for torque = load | Limit for 1.5 × load torque |
|---|---|---|---|
{sl_rows}
## Setting up a soft starter in practice

Most soft starters offer a **voltage ramp** with an initial voltage, a ramp time and a **current limit** that caps the current during the ramp. For pumps and fans the usual approach is an initial voltage of 30 to 40%, a ramp of 10 to 20 s and a current limit of 3 to 4 × FLC. Watch the first start: if the motor sits at the current limit without accelerating, the limit is too low; if it reaches speed in a second or two, the ramp is doing little. Many pump starters also have a **soft stop** or pump control mode to reduce water hammer when stopping. After starting, a bypass contactor usually closes so the thyristors do not carry running current.

## Common mistakes

- **Treating the current limit as harmless.** Every step down in current is a much larger step down in torque, because torque falls with the square of voltage.
- **Using full-load torque instead of breakaway torque.** Loads such as conveyors and positive displacement pumps need high torque at zero speed, often more than at full speed.
- **Ignoring the locked rotor data.** Using a generic 6 × FLC for a motor with 7.5 × FLC locked rotor current gives the wrong voltage and torque.
- **Sizing a generator on running current.** The supply must deliver the soft starter current limit for the whole start, which can be four times the running current.
- **Expecting a soft starter to replace a VFD.** It cannot give full torque at low current; heavy loads on weak supplies need a VFD.
''')

# ======================================================================= MATH

# ---------------------------------------------------------------- Unit circle
def uc(deg):
    th = math.radians(deg)
    s, c = math.sin(th), math.cos(th)
    t0 = deg % 360
    ref = min(deg % 180, 180 - deg % 180)
    return dict(s=s, c=c, t=s / c, csc=1 / s, sec=1 / c, cot=c / s, t0=t0, ref=ref, q=math.floor(t0 / 90 + 1e-9) + 1)
ud = 150.0
UC = uc(ud)
EX = {0: ('0', '1', '0'), 30: ('1/2', '√3/2', '√3/3'), 45: ('√2/2', '√2/2', '1'), 60: ('√3/2', '1/2', '√3'), 90: ('1', '0', 'undefined'),
      120: ('√3/2', '−1/2', '−√3'), 135: ('√2/2', '−√2/2', '−1'), 150: ('1/2', '−√3/2', '−√3/3'), 180: ('0', '−1', '0'),
      210: ('−1/2', '−√3/2', '√3/3'), 225: ('−√2/2', '−√2/2', '1'), 240: ('−√3/2', '−1/2', '√3'), 270: ('−1', '0', 'undefined'),
      300: ('−√3/2', '1/2', '−√3'), 315: ('−√2/2', '√2/2', '−1'), 330: ('−1/2', '√3/2', '−√3/3')}
RAD = {0: '0', 30: 'π/6', 45: 'π/4', 60: 'π/3', 90: 'π/2', 120: '2π/3', 135: '3π/4', 150: '5π/6', 180: 'π', 210: '7π/6', 225: '5π/4',
       240: '4π/3', 270: '3π/2', 300: '5π/3', 315: '7π/4', 330: '11π/6'}
uc_rows = ''
for a in sorted(EX):
    s, c, t = EX[a]
    # check the exact values against floating point
    th = math.radians(a)
    def ev(x):
        return {'0': 0, '1': 1, '1/2': .5, '√2/2': 2 ** .5 / 2, '√3/2': 3 ** .5 / 2, '√3/3': 3 ** .5 / 3, '√3': 3 ** .5}[x.lstrip('−')] * (-1 if x.startswith('−') else 1)
    assert abs(ev(s) - math.sin(th)) < 1e-12 and abs(ev(c) - math.cos(th)) < 1e-12, a
    if t != 'undefined':
        assert abs(ev(t) - math.tan(th)) < 1e-9, a
    uc_rows += f"| {a}° | {RAD[a]} | ({c}, {s}) | {s} | {c} | {t} |\n"
sg_rows = ('| I (0° to 90°) | + | + | + | all positive |\n| II (90° to 180°) | + | − | − | sin, csc |\n'
           '| III (180° to 270°) | − | − | + | tan, cot |\n| IV (270° to 360°) | − | + | − | cos, sec |\n')

P('math', 'unit-circle', f'''
title: Unit Circle Calculator (sin, cos, tan of Any Angle)
description: Find the point on the unit circle for any angle in degrees or radians, with sin, cos, tan, csc, sec, cot, reference angle and quadrant.
category: math
{intro("The unit circle has radius 1 and its centre at the origin; at angle θ its point is (cos θ, sin θ), which defines the trig functions for every angle. This unit circle calculator gives that point, all six trig functions, the reference angle and the quadrant for any angle.",
       "Students use it to check homework and learn exact values, and engineers use it to resolve vectors, phasors and rotating parts into components.", 'unit circle calculator')}
keywords: [unit circle calculator, unit circle, sin cos tan of any angle, reference angle calculator, unit circle values, trig functions calculator, coterminal angle, quadrant of an angle]
published: {D}
updated: {D}
variables:
  - {{ id: th, label: Angle θ, family: angle, unit: deg, default: {ud:g}, help: 'Any angle, positive (counterclockwise) or negative (clockwise), in degrees, radians, gradians or turns.' }}
  - {{ id: cs, label: cos θ (x coordinate), decimals: 6 }}
  - {{ id: sn, label: sin θ (y coordinate), decimals: 6 }}
  - {{ id: tn, label: tan θ (y ÷ x), decimals: 6 }}
  - {{ id: csc, label: csc θ (1 ÷ sin θ), decimals: 6 }}
  - {{ id: sec, label: sec θ (1 ÷ cos θ), decimals: 6 }}
  - {{ id: cot, label: cot θ (x ÷ y), decimals: 6 }}
  - {{ id: t0, label: Coterminal angle (0° to 360°), family: angle, unit: deg }}
  - {{ id: rf, label: Reference angle, family: angle, unit: deg }}
  - {{ id: qd, label: Quadrant (1 to 4), decimals: 0, help: 'An angle exactly on an axis (0°, 90°, 180°, 270°) lies between quadrants; the number shown is the quadrant that starts there.' }}
equations:
  - cs = cos(th)
  - sn = sin(th)
  - tn = tan(th)
  - csc = 1 / sin(th)
  - sec = 1 / cos(th)
  - cot = cos(th) / sin(th)
  - t0 = mod(th, 2 * pi)
  - rf = min(mod(th, pi), pi - mod(th, pi))
  - qd = floor(mod(th, 2 * pi) / (pi / 2)) + 1
faq:
  - q: What is the unit circle?
    a: "A circle of radius 1 centred at the origin. For an angle θ measured counterclockwise from the positive x axis, the point on the circle is (cos θ, sin θ). Because the radius is 1, cos² θ + sin² θ = 1 for every angle, and tan θ is the slope y ÷ x of the radius."
  - q: How do I find the reference angle?
    a: "First reduce the angle to 0° to 360°. In quadrant I the reference angle is θ itself; in quadrant II it is 180° − θ; in quadrant III it is θ − 180°; in quadrant IV it is 360° − θ. The trig functions of θ equal those of the reference angle, with the sign set by the quadrant."
  - q: How do I remember which functions are positive in each quadrant?
    a: "Use ASTC, often remembered as All Students Take Calculus: all six functions are positive in quadrant I, sine and cosecant in II, tangent and cotangent in III and cosine and secant in IV."
  - q: Why is tan 90° undefined?
    a: "At 90° the point is (0, 1), so tan θ = y ÷ x divides by zero. The calculator shows a very large number because 90° in radians cannot be stored exactly. Secant is undefined at 90° and 270°, while cosecant and cotangent are undefined at 0° and 180°."
  - q: What is a coterminal angle?
    a: "Angles that end at the same point on the circle, differing by whole turns of 360° (2π rad). 510°, 150° and −210° are coterminal. The calculator reduces any angle to its coterminal value between 0° and 360°."
related: [math/inverse-trig, math/right-triangle-trig, math/angle-converter, math/arc-length, math/vector, math/circle]
''', f'''
## How to use the unit circle calculator

Enter an **angle** in degrees, or switch the unit to radians, gradians or turns. The calculator gives the coordinates of the point on the unit circle (cos θ, sin θ), the other four trig functions, the coterminal angle between 0° and 360°, the reference angle and the quadrant. Negative angles are measured clockwise, and angles larger than one turn are reduced automatically. To find an angle from a known sine, cosine or tangent, use the [inverse trig calculator](/math/inverse-trig/), which returns the principal value.

## Unit circle formulas

<p class="formula">(x, y) = (cos θ, sin θ) &nbsp;·&nbsp; tan θ = y ÷ x &nbsp;·&nbsp; x² + y² = 1</p>

<p class="formula">csc θ = 1 ÷ sin θ &nbsp;·&nbsp; sec θ = 1 ÷ cos θ &nbsp;·&nbsp; cot θ = x ÷ y</p>

To convert, radians = degrees × π ÷ 180, so 1 rad = 57.2958°.

## Worked example

For **θ = {ud:g}°**:

- In radians, {ud:g}° × π ÷ 180 = 5π/6 = {math.radians(ud):.4f} rad
- It lies in **quadrant {UC['q']}** (between 90° and 180°), and the reference angle is 180° − {ud:g}° = **{UC['ref']:g}°**
- cos {ud:g}° = −cos 30° = −√3/2 = **{UC['c']:.6f}**; sin {ud:g}° = sin 30° = 1/2 = **{UC['s']:.6f}**, so the point is ({UC['c']:.4f}, {UC['s']:.4f})
- tan {ud:g}° = {UC['s']:.4f} ÷ ({UC['c']:.4f}) = **{UC['t']:.6f}** (−√3/3)
- csc = **{UC['csc']:.6f}**, sec = **{UC['sec']:.6f}**, cot = **{UC['cot']:.6f}**
- Check: {UC['c']:.6f}² + {UC['s']:.6f}² = {UC['c']**2 + UC['s']**2:.6f}

## Unit circle exact values

| Degrees | Radians | Point (cos, sin) | sin θ | cos θ | tan θ |
|---|---|---|---|---|---|
{uc_rows}
## Signs of the trig functions by quadrant

| Quadrant | sin, csc | cos, sec | tan, cot | Positive functions |
|---|---|---|---|---|
{sg_rows}
## Using the unit circle outside the classroom

The unit circle is how engineers split anything that rotates or points in a direction into components. A force of F at angle θ has components F cos θ and F sin θ; an AC voltage phasor of magnitude V at phase angle θ has real and reactive parts V cos θ and V sin θ; and a point on a rotating crank of radius r sits at (r cos θ, r sin θ). The unit circle values are simply these with the size set to 1. Programming languages work in radians, so convert degrees first, and use atan2(y, x) rather than atan(y ÷ x) to recover the angle in the correct quadrant, as the [vector calculator](/math/vector/) does.

## Common mistakes

- **Calculator in the wrong mode.** sin 150 in radian mode gives −0.7149, not 0.5; check the unit before reading results.
- **Wrong reference angle in quadrant III and IV.** Measure the reference angle to the x axis, not the y axis: for 240° it is 60°, not 30°.
- **Forgetting the sign.** The reference angle gives the size of the value; the quadrant gives the sign. cos 150° is −√3/2, not √3/2.
- **Swapping sine and cosine.** The x coordinate is cos θ and the y coordinate is sin θ.
- **Treating sin⁻¹ as csc.** sin⁻¹ x is the inverse function arcsin; csc θ is 1 ÷ sin θ.
''')

print(len(DONE), 'pages:', ' '.join(DONE))
