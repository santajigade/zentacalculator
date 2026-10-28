import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
g0 = 9.80665; pi = math.pi

expand('engineering/4-20ma-scaling', '''
## Reverse scaling: process value to mA

To find the current a transmitter should output for a known process value:

<p class="formula">I = 4 + 16 × (V − L) ÷ (H − L)</p>

For a 0–10 bar transmitter reading 6.5 bar: I = 4 + 16 × 0.65 = **14.4 mA**. In the calculator, press × on Loop current and type the process value.

## Why 4–20 mA?

- **Live zero**: 4 mA at 0% lets you tell a real zero from a broken wire (0 mA).
- **Current is immune to wire resistance**: the same current flows through the whole loop, so long cables do not change the reading, within the supply's limits.
- **Loop-powered devices**: 4 mA is enough to power two-wire transmitters.

## Loop power budget

The supply must cover every voltage drop in the loop:

<p class="formula">V<sub>supply</sub> ≥ V<sub>transmitter min</sub> + I<sub>max</sub> × (R<sub>load</sub> + R<sub>cable</sub>)</p>

With a 24 V supply, a transmitter needing 12 V and a 250 Ω input card, the maximum cable resistance at 20 mA (or 22 mA for alarms) is (24 − 12) ÷ 0.022 − 250 ≈ **295 Ω**.

## Reversed and split ranges

- **Reverse acting**: 20 mA at 0% and 4 mA at 100%. Enter the range high as the value at 4 mA and the range low as the value at 20 mA.
- **Split range**: two valves share one signal, e.g. valve A over 4–12 mA and valve B over 12–20 mA. Scale each half separately.

## HART on top of 4–20 mA

HART adds a digital signal on top of the analog current, letting you read the tag, range and diagnostics without disturbing the 4–20 mA value. Check the transmitter's LRV and URV via HART when commissioning to make sure they match the DCS scaling.
''', [
 ('What is 12 mA in percent?', '50% of span. 4 mA is 0% and 20 mA is 100%, so each 1.6 mA is 10%.'),
 ('What does a reading below 3.8 mA mean?', 'Under NAMUR NE 43, values below 3.8 mA indicate a fault or a reading below range, and below 3.6 mA a failure signal.'),
], before='## Converting mA to volts')

expand('engineering/cable-voltage-drop', '''
## Copper resistance per conductor size

| Size (mm²) | Resistance at 20 °C (Ω/km) | Typical max current, clipped direct (A) |
|---|---|---|
| 1.5 | 12.1 | 19–20 |
| 2.5 | 7.41 | 26–27 |
| 4 | 4.61 | 35–36 |
| 6 | 3.08 | 45–46 |
| 10 | 1.83 | 61–63 |
| 16 | 1.15 | 81–85 |
| 25 | 0.727 | 105–112 |

Resistance values follow IEC 60228 for plain copper. Current ratings depend heavily on installation method, grouping and ambient temperature — check your local wiring rules.

## Voltage drop limits

Common design limits (as a percentage of supply voltage):

| Circuit | Typical limit |
|---|---|
| Lighting | 3% |
| Other final circuits | 5% |
| Motor starting | 10–15% (briefly) |

Limits vary by country. IEC 60364 and BS 7671 use 3% for lighting and 5% for other uses from the origin of the installation.

## Temperature effect

Copper resistance rises about 0.39% per °C. At a conductor temperature of 70 °C, resistance is about 20% higher than at 20 °C, so voltage drop is higher in fully loaded cables.

## Choosing a cable size

1. Size for current-carrying capacity first.
2. Check voltage drop over the run length.
3. If the drop is too high, step up one or two sizes.
4. Check fault-loop impedance and protective device coordination.
''', [
 ('What is an acceptable voltage drop?', 'Typically 3% for lighting and 5% for other circuits, but follow your local electrical code.'),
 ('Does a longer cable increase voltage drop?', 'Yes. Voltage drop is proportional to length, so doubling the run doubles the drop.'),
], before='## Remember')

expand('engineering/control-valve-kv-cv', '''
## Kv and Cv quick table

| Kv (m³/h) | Cv (US gpm) | Flow of water at 1 bar ΔP |
|---|---|---|
''' + ''.join(f"| {kv} | {kv*1.156:.2f} | {kv} m³/h |\n" for kv in [0.1, 0.63, 1, 2.5, 4, 6.3, 10, 16, 25, 40, 63, 100]) + '''
Valve makers often offer Kv values in a preferred-number series (1, 1.6, 2.5, 4, 6.3, 10…).

## Valve authority

A control valve controls well only if it takes a reasonable share of the system pressure drop:

<p class="formula">Authority = ΔP<sub>valve</sub> ÷ (ΔP<sub>valve</sub> + ΔP<sub>rest of system</sub>)</p>

Aim for an authority of about **0.3–0.5**. Below about 0.25 the valve has little control over flow until it is nearly closed.

## Choked flow and cavitation

At high pressure drops, liquid can flash or cavitate inside the valve, limiting flow and damaging the trim. The simple Kv formula assumes no choking. For high ΔP, check the maximum allowable pressure drop using the valve's liquid pressure recovery factor (F<sub>L</sub>) per IEC 60534.

## Gases and steam

For gases and steam, the Kv formula is different and depends on inlet pressure, temperature and whether flow is critical. Use the manufacturer's sizing tool or IEC 60534-2-1 for gas and steam valves.
''', [
 ('What is the difference between Kv and Cv?', 'Kv is flow in m³/h of water at 1 bar pressure drop. Cv is flow in US gpm of water at 1 psi drop. Cv = 1.156 × Kv.'),
 ('What Kv should I select?', 'Calculate the Kv needed at maximum flow, then pick a valve whose rated Kv is roughly 1.25–1.5 times larger, so the valve works mostly between 20% and 80% open.'),
], before='## Sizing tips')

expand('engineering/darcy-weisbach-head-loss', '''
## Finding the friction factor

The Darcy friction factor depends on Reynolds number and pipe roughness:

- **Laminar flow** (Re < 2,300): f = 64 ÷ Re.
- **Turbulent flow**: use the Colebrook equation or the explicit Swamee–Jain approximation:

<p class="formula">f = 0.25 ÷ [log₁₀(ε ÷ 3.7D + 5.74 ÷ Re<sup>0.9</sup>)]²</p>

Find Re with the [Reynolds number calculator](/engineering/reynolds-number/).

## Pipe roughness values

| Material | Absolute roughness ε (mm) |
|---|---|
| Drawn copper, PVC, PE | 0.0015 |
| Stainless steel | 0.015 |
| Commercial steel (new) | 0.045 |
| Galvanised steel | 0.15 |
| Cast iron | 0.26 |
| Concrete | 0.3–3.0 |

Old pipes become rougher with scale and corrosion, which raises friction losses over time.

## Minor losses in fittings

Valves, bends and tees add losses: h = K × v² ÷ 2g.

| Fitting | Typical K |
|---|---|
| 90° long-radius elbow | 0.3–0.5 |
| 90° standard elbow | 0.75–0.9 |
| Tee, flow through branch | 1.0–1.8 |
| Gate valve, fully open | 0.15–0.2 |
| Globe valve, fully open | 6–10 |
| Pipe entrance (sharp) | 0.5 |
| Pipe exit | 1.0 |

Add the K values for all fittings and include them with the straight-pipe loss to get total head loss for [pump sizing](/engineering/pump-power/).
''', [
 ('What is the difference between Darcy and Fanning friction factors?', 'The Darcy factor is four times the Fanning factor. Make sure your chart or correlation uses the same one as your formula.'),
 ('How does diameter affect head loss?', 'For the same flow, head loss varies roughly with 1 ÷ D⁵, so a slightly larger pipe greatly reduces losses.'),
], before='## Typical friction factors (turbulent water)')

expand('engineering/dp-flow-square-root', '''
## Low-flow cut-off

Because flow is the square root of DP, small DP errors near zero become large flow errors. A 0.1% DP zero error appears as about 3.2% of flow. Most transmitters and DCS blocks apply a **low-flow cut-off**, often 5–10% of flow, below which the reading is forced to zero.

## Rangeability (turndown)

DP flow meters have limited turndown, typically 3:1 to 4:1, because DP falls with the square of flow:

| Flow (% of max) | DP (% of max) |
|---|---|
| 100% | 100% |
| 50% | 25% |
| 25% | 6.25% |
| 10% | 1% |

At 10% flow the transmitter is measuring only 1% of its range. For wider turndown, use two transmitters with different ranges, or a different meter type.

## Where to take the square root

The square root can be done in the transmitter (output linear with flow) or in the DCS (transmitter output linear with DP). Do it in **one place only**. Taking it twice is a common commissioning error.

## Primary elements that use this

- Orifice plates — see the [orifice flow calculator](/engineering/orifice-flow/)
- Venturi tubes and flow nozzles
- Averaging pitot tubes
- Wedge and V-cone meters
''', [
 ('Why is DP flow a square-root relationship?', "From Bernoulli's equation, the pressure difference across a restriction is proportional to velocity squared, so flow is proportional to the square root of DP."),
 ('What DP corresponds to 50% flow?', '25% of the DP range.'),
], before='## With a 4–20 mA signal')

expand('engineering/flow-meter-k-factor', '''
## K-factor examples

| Meter type | Typical K-factor |
|---|---|
| Small paddle-wheel sensor (DN15) | 300–500 pulses/L |
| Turbine meter, DN25 | 50–150 pulses/L |
| Turbine meter, DN100 | 1–5 pulses/L |
| Positive displacement meter | 1–100 pulses/L |
| Mag meter pulse output | Configurable, e.g. 1 pulse per 10 L |

Always use the calibrated K-factor printed on the meter certificate.

## Units conversions

| From | To | Multiply by |
|---|---|---|
| pulses/L | pulses/US gal | 3.785 |
| pulses/L | pulses/m³ | 1,000 |
| pulses/US gal | pulses/L | 0.2642 |

## Linearity and the K-factor curve

A turbine meter's K-factor is not perfectly constant; it varies with flow rate and viscosity. Calibration certificates often give K at several flow points. Many flow computers apply a **linearisation table** to correct for this.

## Choosing the pulse output

Make sure the maximum pulse frequency is within the counter input's limit, and the minimum gives enough resolution:

- At maximum flow, frequency should be below the input's maximum (for example 10 kHz).
- At minimum flow, at least a few pulses per second gives a stable rate display.
''', [
 ('How do I find the K-factor of a flow meter?', 'Count the pulses while passing a known volume, then divide pulses by volume. Repeat at several flows for accuracy.'),
 ('How do I convert pulses to total volume?', 'Total volume = total pulses ÷ K-factor.'),
], before='## Tips')

expand('engineering/heat-duty', '''
## Heat duty examples

| Fluid | Mass flow | ΔT | Heat duty |
|---|---|---|---|
''' + ''.join(f"| {n} | {m} kg/s | {dt} K | {m*cp*dt:,.0f} kW |\n" for n, m, cp, dt in [('Water', 1, 4.186, 10), ('Water', 2, 4.186, 20), ('Thermal oil', 3, 2.1, 30), ('Air', 5, 1.006, 25), ('Milk', 1.5, 3.9, 60)]) + '''
## Steam heating

When heating with steam, the steam gives up latent heat as it condenses:

<p class="formula">Steam flow = Heat duty ÷ latent heat</p>

At about 7 bar(g), saturated steam has a latent heat of roughly 2,050 kJ/kg. A 100 kW duty needs about 0.049 kg/s, or **175 kg/h** of steam.

## Log mean temperature difference

To size a heat exchanger, combine duty with the overall heat-transfer coefficient U and area A:

<p class="formula">Q = U × A × LMTD</p>

where LMTD = (ΔT₁ − ΔT₂) ÷ ln(ΔT₁ ÷ ΔT₂), using the temperature differences at each end of the exchanger.

## Cooling towers and chillers

Cooling capacity is often quoted in tons of refrigeration (TR): 1 TR = 3.517 kW. A chiller cooling 10 kg/s of water by 5 K removes 209 kW, about **59.5 TR**.
''', [
 ('What is the heat duty formula?', 'Q = ṁ × cp × ΔT: mass flow × specific heat × temperature change.'),
 ('How much heat to warm 1,000 L of water by 10 °C?', 'About 41,860 kJ, or 11.6 kWh.'),
], before='## Practical uses')

expand('engineering/horizontal-tank-volume', '''
## Dished ends

Many horizontal tanks have dished (torispherical or ellipsoidal) heads that add volume beyond the cylindrical shell:

| Head type | Volume of one head (full) |
|---|---|
| 2:1 ellipsoidal | π × D³ ÷ 24 |
| Hemispherical | π × D³ ÷ 12 |
| Flat | 0 |

For a 2 m diameter tank, each 2:1 ellipsoidal head adds about **1.05 m³** when full. Partly filled heads need extra calculation; tank vendors provide strapping tables.

## Strapping tables

A strapping table lists volume at each level, usually every 10 mm or 1 cm. It is used in the DCS or tank gauge to convert level to volume. You can build one quickly with this calculator by stepping the level.

## Level transmitter range

For a level transmitter on a horizontal tank:

- **Range** = 0 to the tank inner diameter (plus any nozzle offset).
- The volume is **not** linear with level, so configure a characterisation table rather than linear scaling.
- At 50% level the tank is exactly 50% full by volume, but at 25% level it is only about 19.6% full.

## Vertical vs horizontal

In a vertical cylinder, volume is proportional to level. A horizontal tank uses floor space differently and has a non-linear level–volume curve, which is why this calculator exists.
''', [
 ('Is 25% level the same as 25% volume in a horizontal tank?', 'No. At 25% of the diameter, a horizontal cylinder holds about 19.6% of its volume, because the bottom is narrower.'),
 ('How do I include dished heads?', 'Add the head volumes from the table above when full. For partial levels, use the vendor strapping table or a detailed head-volume formula.'),
], before='## Using it with a level transmitter')

expand('engineering/hydraulic-cylinder-force', '''
## Force table for common bores (at 160 bar)

| Bore | Rod | Push force | Pull force |
|---|---|---|---|
''' + ''.join(f"| {d} mm | {r} mm | {160e5*pi*(d/1000)**2/4/1000:.1f} kN | {160e5*pi*((d/1000)**2-(r/1000)**2)/4/1000:.1f} kN |\n" for d, r in [(32, 18), (40, 22), (50, 28), (63, 36), (80, 45), (100, 56), (125, 70)]) + '''
## Cylinder speed

Speed depends on oil flow and the effective area:

<p class="formula">v = Q ÷ A</p>

With 20 L/min into a 50 mm bore (19.6 cm²), extend speed is 20,000 cm³/min ÷ 19.6 cm² ≈ **1,019 cm/min**, about 0.17 m/s. Retraction is faster because the rod side has a smaller area.

## Regenerative circuits

In a regenerative circuit, oil from the rod end is fed back to the cap end during extension. Extension becomes faster but the push force is reduced to pressure × rod area.

## Safety margins

- Size cylinders for **at least 25% more** force than the load requires, to cover friction and pressure losses.
- Check **rod buckling** for long strokes under compression.
- Use pressure relief valves set below the cylinder's rated pressure.
''', [
 ('How much force does a 50 mm cylinder produce at 200 bar?', 'Area = π × 0.05² ÷ 4 = 0.00196 m², so force = 20,000,000 × 0.00196 = 39.3 kN.'),
 ('Why is pull force lower than push force?', 'On retraction the rod takes up part of the piston area, so the pressure acts on a smaller annular area.'),
], before='## Quick sizing tips')

expand('engineering/hydrostatic-pressure', '''
## Pressure per metre of liquid

| Liquid | Density (kg/m³) | Pressure per metre |
|---|---|---|
''' + ''.join(f"| {n} | {r} | {r*g0/100:.1f} mbar ({r*g0/6894.757:.3f} psi) |\n" for n, r in [('Water', 998), ('Seawater', 1025), ('Diesel', 840), ('Petrol', 740), ('Sulphuric acid 98%', 1840), ('Mercury', 13534)]) + '''
## Pressure at the bottom of a tank

Total pressure at the bottom = liquid pressure + pressure above the liquid. In a **closed** tank, the vapour or blanket pressure adds to the reading, which is why level in pressurised tanks is measured with a **differential pressure** transmitter connected to both the bottom and the top.

## Density changes with temperature

Water at 80 °C has a density of about 972 kg/m³, nearly 3% less than at 20 °C. A level transmitter calibrated for cold water will read about 3% low on hot water. Compensate in the DCS or recalibrate for the operating temperature.

## Interface level

When two immiscible liquids are present (oil on water), a DP transmitter measures the combined effect. If the total level is known, the interface position can be calculated from the two densities.
''', [
 ('What pressure does 10 m of water create?', 'About 0.98 bar (98 kPa or 14.2 psi).'),
 ('Does tank shape affect hydrostatic pressure?', 'No. Pressure depends only on liquid height and density, not on the shape or volume of the tank.'),
], before='## Ranging a level transmitter')

expand('engineering/mass-flow-rate', '''
## Mass flow of water

| Volumetric flow | Mass flow (998 kg/m³) |
|---|---|
''' + ''.join(f"| {q} m³/h | {q*998:,.0f} kg/h ({q*998/3600:.2f} kg/s) |\n" for q in [1, 5, 10, 25, 50, 100, 250]) + '''
## Gases: actual vs standard flow

For gases, density changes strongly with pressure and temperature, so volumetric flow is often quoted at standard or normal conditions:

- **Nm³/h**: normal cubic metres at 0 °C and 1.01325 bar(a) (common in Europe).
- **Sm³/h**: standard cubic metres, often at 15 °C (check which standard).
- **SCFM**: standard cubic feet per minute, often at 60 °F and 14.696 psia.

Mass flow = standard volume flow × gas density at those standard conditions.

## Coriolis meters

Coriolis meters measure mass flow directly, along with density and temperature, independent of fluid properties. They are widely used for custody transfer, batching and chemical dosing.

## Energy flow

For fuels, multiply mass flow by calorific value to get energy flow. Natural gas at 50 kg/h with a calorific value of about 50 MJ/kg delivers 2,500 MJ/h, roughly **694 kW**.
''', [
 ('How do I convert m³/h to kg/h?', 'Multiply by the density in kg/m³. For water at 20 °C, 10 m³/h is about 9,982 kg/h.'),
 ('Why is mass flow preferred over volume flow?', 'Mass does not change with temperature or pressure, so mass flow gives consistent results for billing, mixing and energy balances.'),
], before='## Density changes with temperature')

expand('engineering/orifice-flow', '''
## Beta ratio effects

| β (d/D) | 1 − β⁴ | Velocity of approach factor 1/√(1 − β⁴) |
|---|---|---|
''' + ''.join(f"| {b} | {1-b**4:.4f} | {1/math.sqrt(1-b**4):.4f} |\n" for b in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75]) + '''
ISO 5167-2 limits β to between 0.10 and 0.75 for standard orifice plates.

## Permanent pressure loss

An orifice plate recovers only part of the differential pressure downstream. The permanent loss is roughly:

<p class="formula">Δω ≈ (1 − β<sup>1.9</sup>) × ΔP</p>

At β = 0.5, about 73% of the measured DP is lost permanently, which costs pumping energy. Venturi tubes recover far more.

## Straight-run requirements

Orifice plates need undisturbed flow. Typical upstream straight lengths are 10–40 pipe diameters depending on the fittings and β ratio, plus about 5–8 diameters downstream. ISO 5167 tables give exact values; flow conditioners can shorten them.

## Tapping arrangements

| Taps | Location |
|---|---|
| Flange taps | 25.4 mm (1 in) each side of the plate |
| Corner taps | At the plate faces |
| D and D/2 taps | 1 D upstream, 0.5 D downstream |

The discharge coefficient depends on the tapping type, so use the matching correlation (Reader-Harris/Gallagher in ISO 5167).
''', [
 ('What is a typical orifice discharge coefficient?', 'About 0.60–0.62 for sharp-edged concentric orifices in turbulent flow.'),
 ('What beta ratio should I use?', 'Typically 0.3–0.7. Lower beta gives more DP and better low-flow measurement but higher permanent pressure loss.'),
], before='## Good practice')

expand('engineering/pipe-flow-velocity', '''
## Velocity for common pipe sizes

| Nominal size | Inner diameter (approx.) | 5 m³/h | 20 m³/h | 50 m³/h |
|---|---|---|---|---|
''' + ''.join(f"| DN{dn} | {d} mm | {5/3600/(pi*(d/1000)**2/4):.2f} m/s | {20/3600/(pi*(d/1000)**2/4):.2f} m/s | {50/3600/(pi*(d/1000)**2/4):.2f} m/s |\n" for dn, d in [(25, 27.9), (40, 41.0), (50, 52.5), (80, 77.9), (100, 102.3), (150, 154.1)]) + '''
Inner diameters are for Schedule 40 steel pipe. Plastic and stainless tubing have different wall thicknesses.

## Choosing a pipe size

Rearrange the formula to find the diameter for a target velocity:

<p class="formula">D = √(4Q ÷ (π × v))</p>

For 50 m³/h at 2 m/s: D = √(4 × 0.01389 ÷ 6.283) = **94 mm**, so DN100 is a suitable size.

## Water hammer

Fast valve closure in a pipe with high velocity creates a pressure surge. The Joukowsky equation gives the surge: ΔP = ρ × a × Δv, with a about 1,200–1,400 m/s in steel water pipes. Stopping 2 m/s instantly can create a surge of over 25 bar. Keep velocities moderate and close valves slowly.
''', [
 ('What is a good velocity for water in a pipe?', 'Typically 1–2.5 m/s for pumped water lines, lower on pump suction (0.5–1.5 m/s).'),
 ('How do I calculate flow from velocity and diameter?', 'Q = v × π × D² ÷ 4. At 1.5 m/s in a 100 mm pipe, Q = 0.0118 m³/s, about 42 m³/h.'),
], before='## Why velocity matters for flow meters')

expand('engineering/pitot-tube-velocity', '''
## Flow from a single velocity

A pitot tube measures **point** velocity. To get flow in a duct or pipe, either:

- **Traverse** the duct: measure at many points across the area (log-Tchebycheff or equal-area method) and average the velocities.
- **Estimate**: in fully developed turbulent pipe flow, average velocity is roughly 0.8–0.85 times the centreline velocity.

Then Q = average velocity × cross-section area.

## Air density matters

Air density changes with temperature, pressure and altitude:

| Condition | Density (kg/m³) |
|---|---|
| 0 °C, sea level | 1.29 |
| 20 °C, sea level | 1.20 |
| 50 °C, sea level | 1.09 |
| 20 °C, 1,500 m altitude | 1.01 |

Using 1.2 kg/m³ at 50 °C overestimates density by 10% and underestimates velocity by about 5%.

## Averaging pitot tubes

Industrial averaging pitot tubes (such as multi-port probes) sample pressure at several points across the pipe and give a DP related to average velocity. They have low permanent pressure loss and suit large pipes and ducts.

## Aircraft airspeed

Aircraft use pitot-static systems to measure indicated airspeed from dynamic pressure. At altitude, the lower air density means true airspeed is higher than indicated airspeed.
''', [
 ('What velocity does 100 Pa of dynamic pressure give in air?', 'At 1.2 kg/m³: v = √(2 × 100 ÷ 1.2) = 12.9 m/s.'),
 ('Can a pitot tube measure liquid flow?', 'Yes. Use the liquid density, for example 998 kg/m³ for water.'),
], before='## Measuring tips')

expand('engineering/pt100-resistance', '''
## Tolerance classes (IEC 60751)

| Class | Tolerance at temperature t (°C) | At 0 °C | At 100 °C |
|---|---|---|---|
| AA | ±(0.1 + 0.0017 abs(t)) | ±0.10 °C | ±0.27 °C |
| A | ±(0.15 + 0.002 abs(t)) | ±0.15 °C | ±0.35 °C |
| B | ±(0.3 + 0.005 abs(t)) | ±0.30 °C | ±0.80 °C |
| C | ±(0.6 + 0.01 abs(t)) | ±0.60 °C | ±1.60 °C |

## 2-, 3- and 4-wire connections

| Connection | Lead-resistance error | Typical use |
|---|---|---|
| 2-wire | Full lead resistance added | Short runs, low accuracy |
| 3-wire | Mostly cancelled if leads are equal | Most industrial installations |
| 4-wire | Eliminated | Laboratory and high-accuracy work |

With 2-wire, 10 m of 0.5 mm² copper (about 0.36 Ω each way, 0.72 Ω total) adds roughly **1.8 °C** of error, since a Pt100 changes about 0.385 Ω/°C.

## Below 0 °C

For temperatures below 0 °C, IEC 60751 uses the full Callendar–Van Dusen equation with an extra C term:

<p class="formula">R = R₀ × [1 + A·t + B·t² + C·(t − 100)·t³]</p>

where C = −4.183 × 10<sup>−12</sup>. The calculator's formula is exact from 0 to 850 °C and very close down to about −50 °C.

## Self-heating

The measuring current heats the sensor slightly. Transmitters typically use 0.5–1 mA to keep self-heating below a few hundredths of a degree.
''', [
 ('What is the resistance of a Pt100 at 0 °C?', 'Exactly 100.00 Ω. A Pt1000 is 1,000 Ω at 0 °C.'),
 ('How much does a Pt100 change per degree?', 'About 0.385 Ω per °C near room temperature.'),
], before='## Field tips')

expand('engineering/pump-power', '''
## Motor selection

Select a motor larger than the shaft power, to cover end-of-curve operation and fluid density changes:

| Shaft power | Typical service factor | Motor size |
|---|---|---|
| Up to 7.5 kW | +20–25% | Next standard size up |
| 7.5–22 kW | +15% | Next standard size up |
| Above 22 kW | +10% | Next standard size up |

Standard IEC motor sizes include 0.75, 1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45 and 55 kW.

## Electrical input power

<p class="formula">P<sub>electrical</sub> = P<sub>shaft</sub> ÷ η<sub>motor</sub></p>

A 6 kW shaft load on a 90% efficient motor draws about 6.67 kW. Over 8,000 hours a year at 0.12 per kWh, that is about **6,400** in electricity, often more than the pump's purchase price.

## Affinity laws

For a centrifugal pump at different speeds:

| Quantity | Changes with speed |
|---|---|
| Flow | ∝ n |
| Head | ∝ n² |
| Power | ∝ n³ |

Reducing speed by 20% with a VFD cuts power to about 51% — a large energy saving compared with throttling a valve.

## NPSH

To avoid cavitation, the net positive suction head available (NPSHa) must exceed the pump's required NPSH (NPSHr), with a margin of at least 0.5–1 m.
''', [
 ('How do I calculate pump power?', 'Hydraulic power = ρ × g × Q × H. Divide by pump efficiency for shaft power. 50 m³/h at 30 m of head with 70% efficiency needs about 5.8 kW.'),
 ('What is a typical centrifugal pump efficiency?', 'About 50–75% for small pumps and 75–90% for large pumps at their best efficiency point.'),
], before='## Finding total head')

expand('engineering/reynolds-number', '''
## Reynolds number for water in pipes

At 20 °C (ρ = 998 kg/m³, μ = 1.002 mPa·s):

| Diameter | 0.5 m/s | 1 m/s | 2 m/s |
|---|---|---|---|
''' + ''.join(f"| {d} mm | {998*0.5*d/1000/1.002e-3:,.0f} | {998*1*d/1000/1.002e-3:,.0f} | {998*2*d/1000/1.002e-3:,.0f} |\n" for d in [15, 25, 50, 100, 200]) + '''
Water in industrial pipes is almost always turbulent.

## Kinematic viscosity form

If you have kinematic viscosity ν (in m²/s or centistokes), use:

<p class="formula">Re = v × D ÷ ν</p>

1 cSt = 10<sup>−6</sup> m²/s. Water at 20 °C is about 1.0 cSt.

## Why it matters for flow meters

Many flow meters have Reynolds-number limits:

- **Orifice plates**: discharge coefficients are well defined above about Re = 5,000–10,000.
- **Vortex meters**: need Re above about 10,000–20,000 to shed vortices reliably.
- **Turbine meters**: calibration shifts with viscosity at low Re.
- **Electromagnetic and Coriolis meters**: largely unaffected.

## Viscous liquids

Oils and syrups can have viscosities hundreds of times higher than water. Flow of a 100 cP oil at 1 m/s in a 50 mm pipe gives Re ≈ 450 — laminar. Pressure-drop and meter behaviour are then very different from water.
''', [
 ('What Reynolds number is turbulent?', 'In pipes, flow is turbulent above about 4,000, laminar below about 2,300, and transitional in between.'),
 ('Is Reynolds number dimensionless?', 'Yes. Use consistent units (for example SI) so the units cancel.'),
], before='## Typical viscosities at 20 °C')

expand('engineering/thermal-expansion', '''
## Coefficients of linear expansion

| Material | α (×10⁻⁶ per K) |
|---|---|
| Invar | 1.2 |
| Glass (borosilicate) | 3.3 |
| Concrete | 10–12 |
| Carbon steel | 11–13 |
| Stainless steel 304/316 | 16–17 |
| Copper | 17 |
| Aluminium | 23 |
| PVC | 50–80 |
| HDPE | 120–200 |

Plastic pipes expand about **10 times** more than steel for the same temperature change.

## Volume expansion of liquids

Liquids expand in volume: ΔV = β × V × ΔT. Water's β is about 0.00021 per K at 20 °C, rising to about 0.0006 near 80 °C. A 1,000 L closed heating system warmed from 10 °C to 80 °C expands by roughly 25–30 L, which is why an expansion vessel is needed.

## Thermal stress

If expansion is prevented, stress builds up:

<p class="formula">σ = E × α × ΔT</p>

For steel (E = 200 GPa, α = 12 × 10⁻⁶), a 50 K rise in a fully restrained pipe creates 120 MPa of stress — a large share of the yield strength of common steels.

## Bimetal strips

Two metals with different α bonded together bend when heated. Thermostats, circuit breakers and dial thermometers use this effect.
''', [
 ('How much does a 100 m steel pipe expand for 50 °C?', '12 × 10⁻⁶ × 100 × 50 = 0.06 m, or 60 mm.'),
 ('Why do bridges have expansion joints?', 'To allow the deck to lengthen and shorten with temperature without building up damaging stress.'),
], before='## Allowing for expansion')

expand('engineering/three-phase-motor-power', '''
## Current at different voltages

For a 11 kW motor (pf 0.85, efficiency 90%):

| Line voltage | Full-load current |
|---|---|
''' + ''.join(f"| {v} V | {11000/0.9/(math.sqrt(3)*v*0.85):.1f} A |\n" for v in [380, 400, 415, 440, 480, 690]) + '''
## Single-phase vs three-phase

| | Single-phase | Three-phase |
|---|---|---|
| Power formula | P = V × I × pf | P = √3 × V<sub>L</sub> × I<sub>L</sub> × pf |
| Typical use | Homes, small motors under 2–3 kW | Industrial motors and large loads |
| Torque | Pulsating | Smooth |

## Starting current

Direct-on-line (DOL) starting draws **6–8 times** the full-load current briefly. Star-delta starters reduce it to about one-third, and soft starters or VFDs reduce it further. Size cables, fuses and generators to cope with starting current.

## Power factor correction

Motors draw reactive power that does no useful work but loads cables and transformers. Adding capacitors raises power factor towards 0.95–0.98, reducing current and, in many tariffs, electricity charges.

## Apparent, real and reactive power

- **Apparent power** S (kVA) = √3 × V × I
- **Real power** P (kW) = S × pf
- **Reactive power** Q (kVAr) = √(S² − P²)
''', [
 ('What is the current of a 7.5 kW motor at 415 V?', 'About 14 A, assuming 0.85 power factor and 88–90% efficiency.'),
 ('Why is √3 used in three-phase power?', 'Because line voltage is √3 times phase voltage in a balanced three-phase system.'),
], before='## Practical notes')

expand('engineering/torque-power-speed', '''
## Torque for standard motor ratings

At 1,460 rpm (4-pole, 50 Hz):

| Power | Torque | Torque at 2,940 rpm (2-pole) |
|---|---|---|
''' + ''.join(f"| {p} kW | {p*1000*60/(2*pi*1460):.1f} N·m | {p*1000*60/(2*pi*2940):.1f} N·m |\n" for p in [0.75, 1.5, 3, 5.5, 7.5, 11, 22, 45, 90]) + '''
## Gearboxes

A gearbox trades speed for torque. With a ratio i and efficiency η:

- Output speed = input speed ÷ i
- Output torque = input torque × i × η

An 11 kW motor (72 N·m at 1,460 rpm) through a 20:1 gearbox at 95% efficiency gives about **1,368 N·m** at 73 rpm.

## Imperial form

<p class="formula">HP = Torque (lbf·ft) × rpm ÷ 5,252</p>

At 5,252 rpm, torque in lbf·ft and horsepower are numerically equal — which is why car torque and power curves cross there.

## Starting and breakdown torque

Induction motors typically produce 150–250% of rated torque at start and up to 200–300% at breakdown. Check the motor datasheet when driving high-inertia or heavily loaded machines.
''', [
 ('How do I calculate torque from kW and rpm?', 'T = 9,549 × P (kW) ÷ rpm. An 11 kW motor at 1,460 rpm gives about 72 N·m.'),
 ('Why do slower motors give more torque?', 'For the same power, torque is inversely proportional to speed, so halving the speed doubles the torque.'),
], before='## Why it matters')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/engineering/*.mdx')):
    c = 'engineering/' + os.path.basename(p)[:-4]; print(c, words(c))
