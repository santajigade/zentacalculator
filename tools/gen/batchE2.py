import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
from ib import intro
D = '2026-10-28'

page('electronics', 'zener-resistor', f'''
title: Zener Diode Resistor Calculator (Voltage Regulator)
description: Calculate the series resistor and power ratings for a Zener diode shunt regulator from input voltage, Zener voltage and load current.
category: electronics
{intro("A Zener diode with a series resistor is the simplest voltage regulator: the Zener holds a fixed voltage while the resistor drops the rest and limits current. This Zener diode resistor calculator sizes the resistor and checks the power in both parts — see [what a Zener diode is](ib:what-is-a-zener-diode).")}
keywords: [zener diode resistor calculator, zener regulator calculator, zener series resistor, zener diode calculation, zener power dissipation, shunt regulator]
updated: {D}
variables:
  - {{ id: Vin, label: Minimum input voltage, family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: Vz, label: Zener voltage, family: voltage, unit: V, default: 5.1, min: 0 }}
  - {{ id: IL, label: Maximum load current, family: current, unit: mA, default: 20, min: 0 }}
  - {{ id: Iz, label: Minimum Zener current, family: current, unit: mA, default: 5, min: 0, help: 'Keep at least 5–10 mA (or the datasheet test current) for good regulation.' }}
  - {{ id: R, label: Series resistor, family: resistance, unit: ohm, min: 0 }}
  - {{ id: PR, label: Resistor power, family: power, unit: mW, min: 0 }}
  - {{ id: Pz, label: Zener power with no load, family: power, unit: mW, min: 0 }}
equations:
  - R = (Vin - Vz) / (IL + Iz)
  - PR = (Vin - Vz)^2 / R
  - Pz = Vz * (Vin - Vz) / R
faq:
  - q: How do I calculate the Zener series resistor?
    a: R = (V_in − V_z) ÷ (I_load + I_z,min), using the lowest input voltage and highest load current so the Zener never drops out of regulation.
  - q: How much power does the Zener dissipate?
    a: The most when the load is disconnected — then all the resistor current flows through the Zener. P = V_z × (V_in − V_z) ÷ R.
  - q: When should I use a regulator IC instead?
    a: For more than a few tens of milliamps, or when efficiency matters. Zener regulators waste power and regulate less tightly than ICs.
  - q: Why does Zener voltage change with temperature?
    a: Zeners below about 5 V have a negative temperature coefficient and those above have a positive one; around 5.1–5.6 V the effects nearly cancel.
related: [electronics/led-resistor, electronics/voltage-divider, physics/ohms-law, electronics/transistor-base-resistor]
''', '''
## How to use the Zener diode resistor calculator

Enter the **minimum input voltage**, the **Zener voltage**, the **maximum load current** and the **minimum Zener current** to keep it regulating. You get the series resistor value, its power, and the Zener's worst-case dissipation when the load is removed. Choose the next lower standard resistor and a Zener rated at least twice the calculated power.

## Zener resistor formula

<p class="formula">R = (V<sub>in</sub> − V<sub>Z</sub>) ÷ (I<sub>L</sub> + I<sub>Z,min</sub>)</p>

<p class="formula">P<sub>R</sub> = (V<sub>in</sub> − V<sub>Z</sub>)² ÷ R &nbsp;·&nbsp; P<sub>Z,max</sub> = V<sub>Z</sub> × (V<sub>in</sub> − V<sub>Z</sub>) ÷ R</p>

## Example

12 V in, 5.1 V Zener, 20 mA load, 5 mA minimum Zener current:

- R = 6.9 ÷ 0.025 = **276 Ω** → use 270 Ω
- Resistor power ≈ **176 mW** → 0.5 W resistor
- Zener power with no load ≈ **130 mW** → 0.5 W Zener

## Common Zener voltages (E24 series)

2.7, 3.3, 3.6, 3.9, 4.7, 5.1, 5.6, 6.2, 6.8, 8.2, 9.1, 10, 12, 15, 18, 24 V. Popular packages: BZX55/BZX79 (0.5 W) and 1N47xx (1 W).

## Other uses

- **Overvoltage clamps** on sensor inputs.
- **Reference voltages** for comparators.
- **Intrinsic safety barriers** use Zeners to limit voltage into hazardous areas.
''')

page('electronics', 'transistor-base-resistor', f'''
title: Transistor Base Resistor Calculator (BJT Switch)
description: Calculate the base resistor for an NPN or PNP transistor used as a switch — from load current, hFE and drive voltage, with overdrive for saturation.
category: electronics
{intro("To use a bipolar transistor as a switch for a relay, LED strip or buzzer, you must drive enough base current to saturate it fully. This transistor base resistor calculator works out the resistor from the load current and gain — see the [basics of transistors](ib:basics-of-transistors) and [BJT currents and voltages](ib:bjt-currents-and-voltages-explained).")}
keywords: [transistor base resistor calculator, bjt base resistor, transistor as switch calculator, base current calculation, npn switch resistor, hfe calculation]
updated: {D}
variables:
  - {{ id: Vin, label: Drive voltage (e.g. microcontroller output), family: voltage, unit: V, default: 5, min: 0 }}
  - {{ id: Vbe, label: Base-emitter voltage, family: voltage, unit: V, default: 0.7, min: 0 }}
  - {{ id: Ic, label: Load (collector) current, family: current, unit: mA, default: 100, min: 0 }}
  - {{ id: hfe, label: Minimum current gain (hFE), default: 100, min: 1 }}
  - {{ id: k, label: Overdrive factor, default: 5, min: 1, help: '2–10 × the minimum base current ensures hard saturation. Forced beta = hFE ÷ overdrive.' }}
  - {{ id: Ib, label: Base current, family: current, unit: mA, min: 0 }}
  - {{ id: Rb, label: Base resistor, family: resistance, unit: kohm, min: 0 }}
equations:
  - Ib = Ic / hfe * k
  - Rb = (Vin - Vbe) / Ib
faq:
  - q: How do I calculate a transistor base resistor?
    a: Find the base current I_B = I_C ÷ hFE × overdrive, then R_B = (V_in − V_BE) ÷ I_B. For 100 mA with hFE 100, 5× overdrive and 5 V drive, R_B ≈ 860 Ω.
  - q: Why use an overdrive factor?
    a: hFE varies widely between parts and with temperature. Driving 2–10 times the minimum base current guarantees saturation and a low V_CE.
  - q: Do I need a diode with a relay?
    a: Yes. Put a flyback diode across the relay coil to absorb the voltage spike when the transistor turns off.
  - q: When should I use a MOSFET instead?
    a: For loads above a few hundred milliamps, a logic-level MOSFET needs no continuous drive current and wastes less power.
related: [electronics/led-resistor, electronics/mosfet-power-loss, electronics/zener-resistor, physics/ohms-law]
''', '''
## How to use the transistor base resistor calculator

Enter the **drive voltage**, the transistor's **V<sub>BE</sub>**, the **load current**, the **minimum hFE** from the datasheet and an **overdrive factor**. You get the base current and the base resistor value — round down to the nearest standard value.

## Base resistor formula

<p class="formula">I<sub>B</sub> = (I<sub>C</sub> ÷ h<sub>FE</sub>) × k &nbsp;·&nbsp; R<sub>B</sub> = (V<sub>in</sub> − V<sub>BE</sub>) ÷ I<sub>B</sub></p>

## Example

Switching a 100 mA relay from a 5 V microcontroller pin with a BC547-class transistor (hFE ≥ 100), 5× overdrive:

- I<sub>B</sub> = 100 ÷ 100 × 5 = **5 mA**
- R<sub>B</sub> = 4.3 ÷ 0.005 = **860 Ω** → use 820 Ω

## Common small-signal transistors

| Transistor | Type | Max I<sub>C</sub> | Typical hFE |
|---|---|---|---|
| BC547 | NPN | 100 mA | 110–800 |
| 2N3904 | NPN | 200 mA | 100–300 |
| 2N2222A | NPN | 600 mA | 100–300 |
| BC337 | NPN | 800 mA | 100–630 |
| BD139 | NPN | 1.5 A | 40–250 |
| TIP120 | NPN Darlington | 5 A | ≥ 1,000 |

## Practical tips

- Check that the microcontroller pin can supply the base current (often 10–20 mA max).
- Add a 10 kΩ resistor from base to emitter to keep the transistor off while the pin floats at power-up.
- Saturation voltage V<sub>CE(sat)</sub> is typically 0.1–0.3 V; power dissipated ≈ I<sub>C</sub> × V<sub>CE(sat)</sub>.
''')

def tauL(L, R): return L/R
page('electronics', 'rl-time-constant', f'''
title: RL Time Constant Calculator
description: Calculate the time constant τ = L/R of an inductor-resistor circuit, plus current rise and decay at any time — for relays, solenoids and filters.
category: electronics
{intro("When voltage is applied to an inductor through a resistance, current rises exponentially with a time constant τ = L/R — and decays the same way when switched off. This RL time constant calculator gives τ and the current at any moment — see [RC and RL time constants explained](ib:rc-and-rl-time-constant-explained).")}
keywords: [rl time constant calculator, rl circuit calculator, inductor time constant, l/r time constant, inductor current rise, rl circuit formula]
updated: {D}
variables:
  - {{ id: L, label: Inductance, family: inductance, unit: mH, default: 100, min: 0 }}
  - {{ id: R, label: Resistance, family: resistance, unit: ohm, default: 50, min: 0 }}
  - {{ id: V, label: Supply voltage, family: voltage, unit: V, default: 24, min: 0 }}
  - {{ id: t, label: Time after switching, family: seconds, unit: ms, default: 2, min: 0 }}
  - {{ id: tau, label: Time constant (τ), family: seconds, unit: ms, min: 0 }}
  - {{ id: If, label: Final current (V/R), family: current, unit: A, min: 0 }}
  - {{ id: Ir, label: Current at time t (rising), family: current, unit: A, min: 0 }}
  - {{ id: Id, label: Current at time t (decaying), family: current, unit: A, min: 0 }}
equations:
  - tau = L / R
  - If = V / R
  - Ir = If * (1 - exp(-t / tau))
  - Id = If * exp(-t / tau)
faq:
  - q: What is the RL time constant?
    a: τ = L ÷ R. After one time constant, current reaches 63.2% of its final value when rising, or falls to 36.8% when decaying.
  - q: How long until the current is fully established?
    a: About 5 time constants, when it reaches 99.3% of the final value.
  - q: Why do relays drop out slowly with a flyback diode?
    a: The diode keeps current circulating through the coil's own low resistance, giving a long L/R decay. Adding a Zener or resistor in series speeds it up.
  - q: How is this different from an RC circuit?
    a: In RC circuits voltage changes exponentially with τ = RC; in RL circuits current does, with τ = L/R.
related: [physics/rc-time-constant, electronics/inductor-energy, electronics/reactance, electronics/rc-filter]
''', '''
## How to use the RL time constant calculator

Enter the **inductance**, the total **resistance** in the circuit (coil resistance plus any series resistor), the **supply voltage** and a **time** after switching. You get the time constant, the final current and the current at that time for both rising and decaying cases.

## RL circuit formulas

<p class="formula">τ = L ÷ R &nbsp;·&nbsp; i(t)<sub>rise</sub> = (V/R)(1 − e<sup>−t/τ</sup>) &nbsp;·&nbsp; i(t)<sub>decay</sub> = (V/R) e<sup>−t/τ</sup></p>

## Current vs time constants

| Time | Rising (% of final) | Decaying (% of initial) |
|---|---|---|
''' + ''.join(f"| {n} τ | {(1-math.exp(-n))*100:.1f}% | {math.exp(-n)*100:.1f}% |\n" for n in [0.5, 1, 2, 3, 4, 5]) + '''
## Typical time constants

| Device | L | R | τ |
|---|---|---|---|
| 24 V DC relay coil | 0.5–2 H | 1–3 kΩ | about 0.5 ms |
| Solenoid valve coil | 0.1–1 H | 20–100 Ω | 5–20 ms |
| Contactor coil (DC) | 2–10 H | 100–500 Ω | 10–50 ms |

## Inductive kick

Interrupting inductor current suddenly creates a voltage spike V = L × di/dt. See the [inductor energy calculator](/electronics/inductor-energy/) for suppression methods.
''')

page('electronics', 'instrumentation-amplifier-gain', f'''
title: Instrumentation Amplifier Gain Calculator (Rg)
description: Calculate the gain-setting resistor Rg for INA128, INA333, AD620 and other instrumentation amplifiers — or the gain from a given Rg.
category: electronics
{intro("Instrumentation amplifiers amplify the tiny differential signal from bridges, strain gauges and thermocouples while rejecting common-mode noise, with a single resistor setting the gain. This instrumentation amplifier gain calculator finds Rg for popular parts — see [how an instrumentation amplifier works](ib:instrumentation-amplifier-working) and how it [differs from an op-amp](ib:instrumentation-amplifier-vs-op-amp-key-differences).")}
keywords: [instrumentation amplifier gain calculator, rg calculator, ina128 gain resistor, ad620 gain calculation, in-amp gain formula, ina333 gain]
updated: {D}
variables:
  - id: k
    label: Amplifier (gain constant)
    default: 50000
    options:
      - {{ label: 'INA128 / INA129 (50 kΩ)', value: 50000 }}
      - {{ label: 'AD620 (49.4 kΩ)', value: 49400 }}
      - {{ label: 'INA333 (100 kΩ)', value: 100000 }}
      - {{ label: 'AD8221 (49.4 kΩ, precision)', value: 49400.001 }}
      - {{ label: 'INA826 (49.4 kΩ, 36 V)', value: 49400.002 }}
  - {{ id: G, label: Gain, default: 100, min: 1, decimals: 2 }}
  - {{ id: Rg, label: Gain resistor (Rg), family: resistance, unit: ohm, min: 0 }}
  - {{ id: Vd, label: Differential input, family: voltage, unit: mV, default: 20 }}
  - {{ id: Vo, label: Output voltage, family: voltage, unit: V }}
equations:
  - G = 1 + k / Rg
  - Vo = G * Vd
faq:
  - q: What is the INA128 gain formula?
    a: G = 1 + 50 kΩ ÷ R_G. For a gain of 100, R_G = 505 Ω.
  - q: What is the AD620 gain formula?
    a: G = 1 + 49.4 kΩ ÷ R_G. For a gain of 100, R_G ≈ 499 Ω.
  - q: What gain do I get with no resistor?
    a: A gain of 1 — leaving R_G open makes the amplifier a precision differential buffer.
  - q: Why use an instrumentation amplifier instead of an op-amp?
    a: It has very high input impedance on both inputs, excellent common-mode rejection and gain set by one resistor without matched-resistor networks.
related: [electronics/op-amp-gain, electronics/wheatstone-bridge, electronics/strain-gauge, electronics/adc-resolution]
''', '''
## How to use the instrumentation amplifier gain calculator

Choose the **amplifier**, then enter the **gain** you want to get the gain resistor R<sub>G</sub> — or enter R<sub>G</sub> and press × on Gain to find the gain. Add a **differential input** to see the output voltage.

## Instrumentation amplifier gain formula

<p class="formula">G = 1 + k ÷ R<sub>G</sub> &nbsp;·&nbsp; R<sub>G</sub> = k ÷ (G − 1)</p>

where k is the internal resistor constant from the datasheet.

## Rg for common gains

| Gain | INA128 (50 kΩ) | AD620 (49.4 kΩ) | INA333 (100 kΩ) |
|---|---|---|---|
''' + ''.join(f"| {g} | {50000/(g-1):,.1f} Ω | {49400/(g-1):,.1f} Ω | {100000/(g-1):,.1f} Ω |\n" for g in [2, 5, 10, 20, 50, 100, 200, 500, 1000]) + '''
Use 0.1% metal-film resistors with low temperature coefficients — R<sub>G</sub> tolerance appears directly as gain error.

## Typical application: load cell

A 2 mV/V load cell on 5 V excitation gives 10 mV at full load. A gain of 250 (R<sub>G</sub> ≈ 200 Ω for INA128) scales it to 2.5 V for a 0–5 V ADC.

## Output range

The output cannot swing to the rails and is also limited by the common-mode voltage at the inputs — check the datasheet's input/output range charts, especially on single 3.3 or 5 V supplies.
''')

def ntc(R25, B, T): return R25*math.exp(B*(1/(T+273.15)-1/298.15))
page('electronics', 'ntc-thermistor', f'''
title: NTC Thermistor Calculator (Beta Equation)
description: Calculate NTC thermistor resistance at any temperature, or temperature from resistance, using the beta (B) equation — for 10k, 100k and other thermistors.
category: electronics
{intro("An NTC thermistor's resistance falls sharply as it warms, making it a cheap and sensitive temperature sensor. The beta equation converts between resistance and temperature using the R25 and B values from the datasheet. This NTC thermistor calculator works both ways — see [NTC and PTC thermistor working](ib:ntc-ptc-thermistor-working) and [thermistor vs thermocouple](ib:thermistor-vs-thermocouple).")}
keywords: [ntc thermistor calculator, thermistor resistance to temperature, beta equation thermistor, 10k thermistor calculator, b value thermistor, thermistor temperature calculation]
updated: {D}
variables:
  - {{ id: R25, label: Resistance at 25 °C (R25), family: resistance, unit: kohm, default: 10, min: 0 }}
  - {{ id: B, label: Beta value (B25/85), suffix: K, default: 3950, min: 0 }}
  - {{ id: T, label: Temperature, suffix: °C, default: 60 }}
  - {{ id: R, label: Resistance at temperature, family: resistance, unit: kohm, min: 0 }}
  - {{ id: alpha, label: Sensitivity at temperature, suffix: '%/°C', decimals: 2 }}
equations:
  - R = R25 * exp(B * (1 / (T + 273.15) - 1 / 298.15))
  - alpha = -B / (T + 273.15)^2 * 100
faq:
  - q: What is the thermistor beta equation?
    a: R = R25 × exp[B × (1/T − 1/298.15)], with T in kelvin. It is accurate to about ±1 °C over a range of 50–100 °C around 25 °C.
  - q: How do I find temperature from resistance?
    a: Enter the measured resistance and press × on Temperature. The calculator solves T = 1 ÷ (1/298.15 + ln(R/R25) ÷ B) − 273.15.
  - q: What is a 10k 3950 thermistor?
    a: A thermistor with 10 kΩ at 25 °C and a beta value of 3,950 K — one of the most common types for 3D printers, appliances and HVAC.
  - q: When should I use the Steinhart–Hart equation instead?
    a: For wide temperature ranges or better than ±0.5 °C accuracy, use the three-coefficient Steinhart–Hart equation or the manufacturer's R–T table.
related: [engineering/pt100-resistance, electronics/voltage-divider, electronics/wheatstone-bridge, conversion/temperature-converter]
''', '''
## How to use the NTC thermistor calculator

Enter the thermistor's **R25** and **beta value** from the datasheet, then a **temperature** to get its resistance — or enter a measured **resistance** and press × on Temperature to read the temperature. The sensitivity shows how much resistance changes per °C at that point.

## NTC beta equation

<p class="formula">R<sub>T</sub> = R₂₅ × e<sup>B (1/T − 1/298.15)</sup> &nbsp;·&nbsp; T = 1 ÷ [1/298.15 + ln(R/R₂₅) ÷ B]</p>

T is in kelvin (°C + 273.15).

## 10 kΩ, B = 3950 thermistor

| Temperature | Resistance | Sensitivity |
|---|---|---|
''' + ''.join(f"| {T} °C | {ntc(10,3950,T):.2f} kΩ | {-3950/(T+273.15)**2*100:.2f} %/°C |\n" for T in [-20, 0, 10, 25, 40, 60, 80, 100, 125]) + '''
## Reading a thermistor with an ADC

Place the thermistor in a [voltage divider](/electronics/voltage-divider/) with a fixed resistor equal to R25. The divider output is most linear and sensitive around 25 °C. Keep the measuring current low (under about 100 µA for 10 kΩ) to avoid self-heating.

## NTC vs Pt100

| | NTC thermistor | Pt100 RTD |
|---|---|---|
| Sensitivity | about −4%/°C | +0.39%/°C |
| Range | −40 to 150 °C typical | −200 to 600 °C+ |
| Linearity | Strongly non-linear | Nearly linear |
| Cost | Very low | Higher |
| Interchangeability | ±0.2–1 °C | Class A/B standards |
''')

def dbm2w(d): return 10**(d/10)/1000
page('electronics', 'dbm-to-watts', f'''
title: dBm to Watts Converter (and Watts to dBm)
description: Convert dBm to watts, milliwatts and dBW and back — with voltage across 50 Ω — for RF, Wi-Fi, radio and fibre power levels.
category: electronics
{intro("dBm expresses power in decibels relative to 1 milliwatt, so RF and optical power levels spanning many orders of magnitude become easy numbers to add and subtract. This dBm to watts converter works both ways and shows the equivalent voltage in a 50 Ω system — see [decibels in electronics: dB and dBm](ib:decibel-in-electronics-db-dbm).")}
keywords: [dbm to watts, watts to dbm, dbm to mw, dbm calculator, dbm converter, dbw to dbm, rf power conversion]
updated: {D}
variables:
  - {{ id: dbm, label: Power in dBm, suffix: dBm, default: 20, decimals: 2 }}
  - {{ id: P, label: Power, family: power, unit: mW, min: 0 }}
  - {{ id: dbw, label: Power in dBW, suffix: dBW, decimals: 2 }}
  - {{ id: V, label: RMS voltage across 50 Ω, family: voltage, unit: V, min: 0 }}
equations:
  - P = 10^(dbm / 10) / 1000
  - dbw = dbm - 30
  - V = sqrt(P * 50)
faq:
  - q: How do I convert dBm to watts?
    a: P(W) = 10^(dBm/10) ÷ 1,000. 20 dBm = 100 mW; 30 dBm = 1 W.
  - q: How do I convert watts to dBm?
    a: dBm = 10 × log₁₀(P in mW). 1 W = 30 dBm; 10 W = 40 dBm.
  - q: What is the difference between dBm and dBW?
    a: dBW is referenced to 1 W, so dBW = dBm − 30.
  - q: What do negative dBm values mean?
    a: Power below 1 mW. Wi-Fi signals of −30 to −70 dBm are tiny fractions of a milliwatt.
related: [physics/decibel, electronics/snr, physics/wavelength-frequency, conversion/power-converter]
''', '''
## How to use the dBm to watts converter

Enter a value in **dBm** to get watts (choose W, mW or kW), dBW and the RMS voltage across a 50 Ω load. To convert from watts, enter the power and press × on dBm.

## dBm to watts formula

<p class="formula">P(mW) = 10<sup>dBm/10</sup> &nbsp;·&nbsp; dBm = 10 log₁₀(P/1 mW) &nbsp;·&nbsp; dBW = dBm − 30</p>

## dBm to watts table

| dBm | Power | Voltage (50 Ω) |
|---|---|---|
''' + ''.join(f"| {d} | {(f'{dbm2w(d):g} W' if dbm2w(d)>=1 else (f'{dbm2w(d)*1000:g} mW' if dbm2w(d)>=1e-3 else f'{dbm2w(d)*1e6:.3g} µW'))} | {math.sqrt(dbm2w(d)*50):.3g} V |\n" for d in [-90, -60, -30, -10, 0, 10, 20, 27, 30, 40, 50, 60]) + '''
## Typical power levels

| Signal | Level |
|---|---|
| Wi-Fi router transmit | 15–20 dBm |
| Mobile phone transmit (max) | 23–33 dBm |
| Wi-Fi receive (good) | −30 to −60 dBm |
| Wi-Fi receive (usable limit) | about −80 dBm |
| GPS signal at ground | about −130 dBm |
| Fibre optic transmitter | −10 to +3 dBm |

## Link budgets

In dB terms, you simply add gains and subtract losses: transmit 20 dBm + 6 dBi antenna − 80 dB path loss + 3 dBi antenna = −51 dBm received.
''')

page('electronics', 'battery-charge-time', f'''
title: Battery Charging Time Calculator
description: Calculate how long a battery takes to charge from its capacity, charging current, starting charge level and charging efficiency — lead-acid or lithium.
category: electronics
{intro("How long a battery takes to charge depends on its capacity, the charger current and how much charge it needs — plus losses that make real charging slower than Ah ÷ A. This battery charging time calculator includes the state of charge and efficiency — see [industrial battery charger float and boost charging](ib:industrial-battery-charger-float-boost) and the main [causes of battery failure](ib:causes-of-battery-failure).")}
keywords: [battery charging time calculator, battery charge time formula, how long to charge battery, ah charging time, lead acid charging time, lithium battery charge time]
updated: {D}
variables:
  - {{ id: C, label: Battery capacity, suffix: Ah, default: 150, min: 0 }}
  - {{ id: I, label: Charging current, family: current, unit: A, default: 15, min: 0 }}
  - {{ id: s0, label: Starting state of charge, family: percent, unit: '%', default: 20, min: 0, max: 1 }}
  - {{ id: s1, label: Target state of charge, family: percent, unit: '%', default: 100, min: 0, max: 1 }}
  - id: eta
    label: Battery type (charging efficiency)
    default: 0.8
    options:
      - {{ label: 'Lead-acid flooded / tubular (≈ 80%)', value: 0.8 }}
      - {{ label: 'Lead-acid AGM / gel (≈ 85%)', value: 0.85 }}
      - {{ label: 'Lithium-ion / LiFePO4 (≈ 95%)', value: 0.95 }}
  - {{ id: Ah, label: Charge required, suffix: Ah, min: 0, decimals: 1 }}
  - {{ id: t, label: Estimated charging time, family: seconds, unit: h, min: 0 }}
  - {{ id: cr, label: Charging rate (C-rate), suffix: C, min: 0, decimals: 3 }}
equations:
  - Ah = C * (s1 - s0)
  - t = Ah / (I * eta) * 3600
  - cr = I / C
faq:
  - q: How do I calculate battery charging time?
    a: Time (h) = Ah needed ÷ (charging current × efficiency). Charging 120 Ah into a lead-acid battery at 15 A takes about 120 ÷ (15 × 0.8) = 10 hours.
  - q: Why does the last 20% take longer?
    a: Chargers switch to constant-voltage (absorption) mode near full charge, and the current tapers off. Lead-acid batteries can need several extra hours to reach 100%.
  - q: What charging current should I use?
    a: For lead-acid, about 10% of capacity (C/10) — 15 A for a 150 Ah battery. Lithium batteries accept 0.5C or more; check the datasheet.
  - q: What is C-rate?
    a: Charging current divided by capacity. 15 A on a 150 Ah battery is 0.1C.
related: [everyday-life/inverter-battery-backup, other/battery-life, ecology/battery-storage, ecology/ev-charging-time]
''', '''
## How to use the battery charging time calculator

Enter the **battery capacity**, the **charging current**, the **starting** and **target state of charge**, and choose the **battery type** for charging efficiency. You get the charge needed in Ah, the estimated time and the C-rate.

## Battery charging time formula

<p class="formula">t (h) = C × (SoC<sub>target</sub> − SoC<sub>start</sub>) ÷ (I × η)</p>

## Charging time for a 150 Ah lead-acid battery (20% → 100%)

| Charging current | C-rate | Time |
|---|---|---|
''' + ''.join(f"| {i} A | {i/150:.2f}C | {150*0.8/(i*0.8):.1f} h |\n" for i in [5, 10, 15, 20, 30]) + '''
Add 1–3 hours for the absorption stage of lead-acid batteries.

## Recommended charging currents

| Battery | Typical charge rate |
|---|---|
| Flooded / tubular lead-acid (inverter batteries) | C/10 – C/8 |
| AGM / gel lead-acid | C/5 – C/10 |
| LiFePO4 | 0.2C – 1C |
| Li-ion (phone, laptop) | 0.5C – 1C, fast charge up to 2C+ |

## Charging stages (lead-acid)

1. **Bulk** — constant current until about 80% charge.
2. **Absorption** — constant voltage (about 14.4–14.8 V for 12 V) while current tapers.
3. **Float** — lower voltage (about 13.5–13.8 V) to maintain full charge.
''')

page('electronics', 'capacitors-series-parallel', f'''
title: Capacitors in Series and Parallel Calculator
description: Calculate the total capacitance of up to four capacitors in series or parallel, with the total voltage rating guide and charge.
category: electronics
{intro("Capacitors combine the opposite way to resistors: in parallel their capacitances add, while in series the total is smaller than the smallest one. This capacitors in series and parallel calculator handles up to four capacitors — see the [capacitor working principle](ib:capacitor-working-principle) and [series vs parallel circuits](ib:series-vs-parallel-circuits-explained).")}
keywords: [capacitors in series calculator, capacitors in parallel calculator, total capacitance calculator, series capacitance formula, equivalent capacitance, capacitor combination]
updated: {D}
variables:
  - id: s
    label: Connection
    default: 1
    options:
      - {{ label: Series, value: 1 }}
      - {{ label: Parallel, value: 0 }}
  - {{ id: C1, label: C1, family: capacitance, unit: uF, default: 10, min: 0.000000000001 }}
  - {{ id: C2, label: C2, family: capacitance, unit: uF, default: 22, min: 0.000000000001 }}
  - {{ id: C3, label: C3 (0 = not used), family: capacitance, unit: uF, default: 0, min: 0 }}
  - {{ id: C4, label: C4 (0 = not used), family: capacitance, unit: uF, default: 0, min: 0 }}
  - {{ id: Ct, label: Total capacitance, family: capacitance, unit: uF, min: 0 }}
equations:
  - Ct = s / (1/C1 + 1/C2 + step(C3)/(C3 + 1e-30) + step(C4)/(C4 + 1e-30)) + (1 - s) * (C1 + C2 + C3 + C4)
faq:
  - q: How do capacitors add in parallel?
    a: Directly — C_total = C1 + C2 + C3 + … Two 10 µF capacitors in parallel make 20 µF.
  - q: How do capacitors add in series?
    a: As reciprocals — 1/C_total = 1/C1 + 1/C2 + … Two 10 µF capacitors in series make 5 µF.
  - q: Why put capacitors in series?
    a: To raise the voltage rating. Each capacitor shares the voltage; add balancing resistors so the voltage divides evenly.
  - q: How do I leave a capacitor out?
    a: Enter 0 for C3 or C4 — unused capacitors are ignored in both series and parallel.
related: [electronics/capacitor-energy, physics/resistors-series-parallel, electronics/rc-filter, electronics/reactance]
''', '''
## How to use the capacitors in series and parallel calculator

Choose **series** or **parallel** and enter up to four capacitor values. Enter **0** for any capacitor you are not using. The result is the equivalent capacitance.

## Capacitors in series and parallel formulas

<p class="formula">Parallel: C = C₁ + C₂ + C₃ + … &nbsp;·&nbsp; Series: 1/C = 1/C₁ + 1/C₂ + 1/C₃ + …</p>

For two capacitors in series: C = C₁C₂ ÷ (C₁ + C₂).

## Examples

| Capacitors | Series | Parallel |
|---|---|---|
| 10 µF + 10 µF | 5 µF | 20 µF |
| 10 µF + 22 µF | 6.88 µF | 32 µF |
| 100 nF + 100 nF + 100 nF | 33.3 nF | 300 nF |
| 1 µF + 100 nF | 90.9 nF | 1.1 µF |

## Voltage ratings

- **Parallel**: every capacitor sees the full voltage, so the lowest voltage rating applies.
- **Series**: voltage divides in inverse proportion to capacitance — the smallest capacitor takes the most voltage. For equal capacitors, ratings add, but add equal balancing resistors across each one.

## Compared with resistors

Capacitors in parallel behave like resistors in series, and vice versa. See the [resistors in series and parallel calculator](/physics/resistors-series-parallel/).
''')

page('electronics', 'mosfet-power-loss', f'''
title: MOSFET Power Dissipation Calculator (Conduction and Switching Loss)
description: Estimate MOSFET conduction and switching losses from Rds(on), current, voltage, switching frequency and rise/fall times — and the junction temperature.
category: electronics
{intro("A MOSFET used as a switch loses power in two ways: conduction loss from its on-resistance and switching loss during each turn-on and turn-off. Together they decide whether it needs a heat sink. This MOSFET power dissipation calculator estimates both — see [what a MOSFET is](ib:what-is-a-mosfet-working-principle) and [MOSFET gate driver ICs](ib:mosfet-gate-driver-ics-explained).")}
keywords: [mosfet power dissipation calculator, mosfet conduction loss, mosfet switching loss, rds on power loss, mosfet junction temperature, mosfet heat calculation]
updated: {D}
variables:
  - {{ id: I, label: Drain current (RMS), family: current, unit: A, default: 10, min: 0 }}
  - {{ id: Rds, label: Rds(on) at operating temperature, family: resistance, unit: mohm, default: 20, min: 0, help: 'Rds(on) rises about 1.5–1.8 × from 25 °C to 125 °C — use the hot value.' }}
  - {{ id: V, label: Drain-source voltage when off, family: voltage, unit: V, default: 24, min: 0 }}
  - {{ id: f, label: Switching frequency, family: frequency, unit: kHz, default: 50, min: 0 }}
  - {{ id: tsw, label: Rise + fall time (total), family: seconds, unit: ns, default: 100, min: 0 }}
  - {{ id: Rth, label: Junction-to-ambient thermal resistance, suffix: °C/W, default: 40, min: 0 }}
  - {{ id: Ta, label: Ambient temperature, suffix: °C, default: 40 }}
  - {{ id: Pc, label: Conduction loss, family: power, unit: W, min: 0 }}
  - {{ id: Ps, label: Switching loss, family: power, unit: W, min: 0 }}
  - {{ id: P, label: Total loss, family: power, unit: W, min: 0 }}
  - {{ id: Tj, label: Estimated junction temperature, suffix: °C, decimals: 1 }}
equations:
  - Pc = I^2 * Rds
  - Ps = 0.5 * V * I * tsw * f
  - P = Pc + Ps
  - Tj = Ta + P * Rth
faq:
  - q: How do I calculate MOSFET conduction loss?
    a: P = I_RMS² × Rds(on). 10 A through 20 mΩ gives 2 W. Use Rds(on) at the expected junction temperature, not the 25 °C value.
  - q: How do I estimate switching loss?
    a: P_sw ≈ ½ × V × I × (t_rise + t_fall) × f. Fast gate drive and lower frequency reduce it.
  - q: What junction temperature is safe?
    a: Most MOSFETs are rated to 150 or 175 °C; design for 100–125 °C maximum for reliability.
  - q: Do I need a heat sink?
    a: If the estimated junction temperature without a heat sink exceeds your target, yes — use the heat sink calculator to size it.
related: [electronics/heat-sink, electronics/buck-converter, electronics/pwm-duty-cycle, electronics/transistor-base-resistor]
''', '''
## How to use the MOSFET power dissipation calculator

Enter the **RMS drain current**, the **Rds(on)** at operating temperature, the **off-state voltage**, the **switching frequency**, the total **rise + fall time**, the **thermal resistance** to ambient (or to the heat sink path) and the **ambient temperature**. You get conduction loss, switching loss, total loss and the estimated junction temperature.

## MOSFET loss formulas

<p class="formula">P<sub>cond</sub> = I<sub>RMS</sub>² × R<sub>DS(on)</sub> &nbsp;·&nbsp; P<sub>sw</sub> ≈ ½ × V × I × (t<sub>r</sub> + t<sub>f</sub>) × f</p>

<p class="formula">T<sub>j</sub> = T<sub>a</sub> + P<sub>total</sub> × R<sub>θJA</sub></p>

## Example

10 A, 20 mΩ, 24 V, 50 kHz, 100 ns total transition time:

- Conduction loss = 100 × 0.02 = **2.0 W**
- Switching loss = 0.5 × 24 × 10 × 100 ns × 50 kHz = **0.6 W**
- Total = **2.6 W**; with 40 °C/W and 40 °C ambient, T<sub>j</sub> ≈ **144 °C** → add a heat sink

## Reducing losses

- Choose lower Rds(on) — but larger MOSFETs have more gate charge and slower switching.
- Use a proper gate driver to switch in tens of nanoseconds.
- Lower the switching frequency where ripple allows.
- Improve cooling: copper area on the PCB, a heat sink or airflow. See the [heat sink calculator](/electronics/heat-sink/).

## Not included

Gate-drive loss (Q<sub>g</sub> × V<sub>gs</sub> × f), body-diode conduction and reverse-recovery losses add more in synchronous converters.
''')

def sg(R, GF, eps): return R*GF*eps
page('electronics', 'strain-gauge', f'''
title: Strain Gauge Calculator (ΔR and Bridge Output)
description: Calculate the resistance change and Wheatstone bridge output of a strain gauge from gauge factor, strain and excitation — for quarter, half and full bridges.
category: electronics
{intro("A strain gauge is a fine foil grid whose resistance changes slightly when it is stretched or compressed. Wired into a Wheatstone bridge, it measures force, pressure and weight in load cells and transmitters. This strain gauge calculator gives the resistance change and bridge output — see the [strain gauge working principle](ib:strain-gauge-working-principle) and [bonded vs unbonded strain gauges](ib:bonded-and-unbonded-strain-gauges).")}
keywords: [strain gauge calculator, gauge factor calculation, strain gauge bridge output, microstrain to mv/v, quarter bridge calculator, load cell output, delta r strain]
updated: {D}
variables:
  - {{ id: R, label: Gauge resistance, family: resistance, unit: ohm, default: 350, min: 0 }}
  - {{ id: GF, label: Gauge factor, default: 2.0, min: 0 }}
  - {{ id: ue, label: Strain, suffix: µε, default: 1000 }}
  - {{ id: Vex, label: Bridge excitation, family: voltage, unit: V, default: 10, min: 0 }}
  - id: n
    label: Bridge configuration
    default: 1
    options:
      - {{ label: Quarter bridge (1 active gauge), value: 1 }}
      - {{ label: Half bridge (2 active gauges, bending), value: 2 }}
      - {{ label: Full bridge (4 active gauges), value: 4 }}
  - {{ id: dR, label: Resistance change per gauge, family: resistance, unit: mohm, min: 0 }}
  - {{ id: Vo, label: Bridge output (linear approximation), family: voltage, unit: mV }}
  - {{ id: mvv, label: Sensitivity, suffix: mV/V, decimals: 4 }}
equations:
  - dR = R * GF * ue * 1e-6
  - Vo = Vex * n * GF * ue * 1e-6 / 4
  - mvv = Vo / Vex * 1000
faq:
  - q: What is the gauge factor?
    a: The ratio of relative resistance change to strain, GF = (ΔR/R) ÷ ε. Metal foil gauges have GF ≈ 2; semiconductor gauges can exceed 100.
  - q: What is a microstrain?
    a: One millionth of a unit of strain (10⁻⁶ m/m). Steel at its typical working stress sees about 500–1,500 µε.
  - q: How big is the output of a strain gauge bridge?
    a: Very small: a quarter bridge with GF 2 at 1,000 µε gives about 0.5 mV/V — 5 mV with 10 V excitation — so an instrumentation amplifier is needed.
  - q: Why use a full bridge?
    a: It gives four times the output of a quarter bridge and cancels temperature effects and lead resistance, which is why load cells use full bridges.
related: [electronics/wheatstone-bridge, electronics/instrumentation-amplifier-gain, physics/hookes-law, physics/pressure]
''', '''
## How to use the strain gauge calculator

Enter the **gauge resistance**, **gauge factor**, **strain** in microstrain, **bridge excitation** and choose the **bridge configuration**. You get the resistance change per gauge, the bridge output and its sensitivity in mV/V.

## Strain gauge formulas

<p class="formula">ΔR = R × GF × ε &nbsp;·&nbsp; V<sub>out</sub> ≈ V<sub>ex</sub> × N × GF × ε ÷ 4</p>

where N is the number of active arms (1, 2 or 4). The quarter-bridge result is slightly non-linear at large strains — see the [Wheatstone bridge calculator](/electronics/wheatstone-bridge/) for the exact value.

## Output at 10 V excitation, GF = 2

| Strain | ΔR (350 Ω gauge) | Quarter bridge | Full bridge |
|---|---|---|---|
''' + ''.join(f"| {u} µε | {sg(350,2,u*1e-6)*1000:.1f} mΩ | {10*2*u*1e-6/4*1000:.2f} mV | {10*4*2*u*1e-6/4*1000:.2f} mV |\n" for u in [10, 100, 500, 1000, 2000]) + '''
## From strain to stress

For steel (E ≈ 200 GPa), stress = E × ε: 1,000 µε corresponds to about 200 MPa.

## Load cells

Load cells are rated in **mV/V** at full load — commonly 2 mV/V. With 10 V excitation, a 2 mV/V cell gives 20 mV at full capacity. Amplify it with an [instrumentation amplifier](/electronics/instrumentation-amplifier-gain/).
''')
print('E2 done')
