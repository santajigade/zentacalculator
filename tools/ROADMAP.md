# Zenta Calculator — calculator backlog

Daily target: ~20 new calculators, focus on **Engineering, Electrical, Electronics, Physics, Chemistry, Math, Statistics**.
Pick the next unchecked items top-down (mix 2–3 categories per batch). Tick `[x]` when published.
Subcategory = the `groups` entry in `src/data/catseo.ts` the calculator should be added to.
(ib) = a matching instrumentationblog.in article probably exists — check `tools/gen/ib_slugs.txt`.

## Engineering — Instrumentation & signals
- [x] RTD lead wire error (2/3/4-wire) (ib)
- [ ] Thermocouple mV ↔ °C (Type K, J, T — NIST polynomials) (ib)
- [ ] Pt1000 / Ni1000 / Cu10 resistance tables
- [ ] HART loop minimum resistance check (ib)
- [ ] Transmitter re-ranging / turndown accuracy
- [x] Calibration error & as-found / as-left tolerance (ib)
- [x] 5-point calibration table generator (ib)
- [x] Analog input raw counts ↔ engineering units (PLC) (ib)
- [x] Square-root low-flow cutoff
- [x] Signal converter: 0–10 V ↔ 4–20 mA ↔ 1–5 V
- [x] PID tuning: Ziegler–Nichols (ib)
- [x] PID tuning: Cohen–Coon / IMC lambda (ib)
- [x] First-order process time constant & dead time
- [x] Sensor response time (63.2%, T90)
- [ ] Thermowell wake frequency (ASME PTC 19.3 TW simplified) (ib)

## Engineering — Flow
- [ ] Orifice plate bore sizing (β from flow & DP) (ib)
- [ ] Flow nozzle flow
- [ ] V-cone flow (ib)
- [x] Rotameter density correction (ib)
- [ ] Magmeter velocity & minimum conductivity
- [ ] Ultrasonic transit-time flow (ib)
- [x] Vortex shedding frequency (Strouhal)
- [ ] Gas flow through orifice (expansibility factor)
- [ ] Steam flow (saturated steam density table)
- [ ] SCFM ↔ ACFM ↔ Nm³/h
- [ ] MMSCFD natural gas converter (ib)
- [ ] Open channel: Parshall flume
- [x] Manning equation (open channel)
- [x] Hazen–Williams head loss
- [x] Minor losses (K factors, fittings)
- [x] Equivalent pipe length
- [ ] Pipe size for target velocity
- [ ] Flow through restriction orifice
- [ ] Gas line sizing (velocity limit)

## Engineering — Pressure, level & tanks
- [x] Manometer (U-tube, inclined) (ib)
- [x] Absolute ↔ gauge ↔ vacuum pressure (ib)
- [ ] Bubbler (purge) level (ib)
- [ ] Interface level by DP (ib)
- [ ] Capacitance level probe
- [ ] Radar level: dielectric constant & reflection
- [x] Spherical tank volume (ib)
- [ ] Horizontal tank with dished/hemispherical heads
- [x] Cone-bottom tank volume
- [x] Tank fill / drain time
- [x] Pressure vessel wall thickness (ASME, simplified)
- [x] Pipe wall thickness (Barlow)
- [x] Hydrostatic test pressure (ib)
- [ ] Pressure gauge range selection (ib)
- [ ] Bourdon gauge accuracy class error (ib)

## Engineering — Valves, pumps & compressors
- [ ] Control valve sizing for gas (Cg / Cv)
- [ ] Control valve sizing for steam
- [x] Valve authority
- [ ] Cavitation index (σ) / choked flow
- [ ] Actuator thrust / torque sizing (ib)
- [x] Pump NPSH available (ib)
- [x] Pump affinity laws
- [x] Pump head from pressure
- [ ] System curve & duty point
- [x] Compressor power (isentropic)
- [x] Air compressor receiver size
- [x] Compressed air leak cost
- [x] Fan affinity laws & fan power
- [ ] Safety relief valve sizing (API 520 liquid, simplified)

## Engineering — Heat transfer & HVAC
- [x] LMTD heat exchanger
- [x] Heat exchanger area (Q = U·A·LMTD) (ib)
- [ ] Steam consumption for heating
- [x] Pipe heat loss (insulated)
- [ ] Insulation thickness
- [x] Convection heat transfer (Q = hAΔT)
- [x] Radiation heat transfer (Stefan–Boltzmann)
- [x] Cooling tower range/approach & evaporation
- [x] Chiller tonnage (TR) from flow & ΔT
- [ ] Air conditioner BTU / room size
- [ ] Duct size (equal friction)
- [x] CFM air changes per hour — air-changes-per-hour
- [x] Psychrometric: dew point from RH (ib)
- [x] Relative humidity ↔ absolute humidity (exists: engineering/dew-point)
- [x] Heater kW for tank heating

## Engineering — Mechanical design
- [x] Bolt torque (T = K·D·F)
- [x] Shaft diameter for torque
- [x] Beam deflection (simply supported, cantilever)
- [x] Bending stress (M/Z)
- [x] Moment of inertia (rectangle, circle, I-beam) — area-moment-of-inertia (rectangle, circle, tube; I-beam not yet)
- [x] Spring rate (helical compression)
- [x] Gear ratio & speed
- [x] Chain / sprocket speed & length — chain-length
- [ ] Belt tension
- [x] Bearing L10 life
- [ ] Press fit interference
- [x] Factor of safety
- [x] Young's modulus / stress-strain
- [x] Weld size (fillet throat)
- [ ] Conveyor belt speed & capacity

## Engineering — Process & chemical
- [ ] Mass balance (mixing two streams)
- [x] Residence time
- [ ] Reactor space time / conversion
- [x] Boiler efficiency (direct method)
- [ ] Steam table lookup (saturated)
- [x] Specific gravity ↔ density ↔ °Brix / °Baumé
- [ ] Viscosity converter (cP, cSt, SSU)
- [x] Kinematic ↔ dynamic viscosity
- [ ] Combustion air requirement
- [x] Flue gas O₂ to excess air
- [ ] Heating value converter (GCV/NCV)
- [x] Gas density (ideal + Z) — gas-density (chemistry)
- [ ] Molar flow ↔ mass flow ↔ volume flow

## Engineering — Safety & reliability
- [ ] Risk graph / LOPA (simplified) (ib)
- [ ] 1oo2 / 2oo3 PFDavg (ib)
- [x] Safe failure fraction (SFF) (ib)
- [ ] Proof test coverage effect
- [x] MTTF ↔ FIT ↔ failure rate converter (FIT table in availability-mtbf; life-test FIT: acceleration-factor)
- [x] Weibull reliability
- [ ] Hazardous area: temperature class check (ib)
- [ ] IS loop entity parameters (Uo/Io/Co/Lo) check

## Electrical
- [ ] Cable size for load current (with derating) (ib)
- [x] Neutral sizing with harmonics (ib)
- [ ] MCCB / breaker selection (ib)
- [ ] Fuse I²t / let-through
- [x] Motor starting voltage dip (ib)
- [ ] Soft starter current (ib)
- [x] Capacitor bank current & kVAr ↔ µF
- [x] Busbar size (current density)
- [ ] Arc flash incident energy (simplified) (ib)
- [x] Battery bank sizing (Ah for backup)
- [ ] Substation battery sizing (IEEE 485 simplified) (ib)
- [x] Solar string sizing (Voc, Vmp vs inverter)
- [ ] Solar inverter sizing
- [ ] Energy consumption kWh (plant) (ib)
- [x] Maximum demand & load factor
- [ ] Electricity bill with demand charges (India HT tariff)
- [x] Lighting: lumens & lux (room) 
- [x] Number of light fixtures (lumen method)
- [x] Single-phase transformer current (exists: transformer-current)
- [x] Autotransformer power
- [x] Generator frequency & poles
- [x] Synchronous generator power angle
- [x] Transmission line: Ferranti effect (ib)
- [x] Skin depth (ib)
- [x] Insulation resistance / PI (ib)
- [ ] Motor winding resistance unbalance (ib)
- [x] Watt-hour meter constant (imp/kWh)
- [x] Lightning protection: rolling sphere radius
- [x] Voltage drop for DC (solar/battery) (exists: cable-voltage-drop)

## Electronics
- [x] Op-amp: summing, differential, integrator (ib)
- [x] Sallen–Key low-pass filter (ib)
- [x] LC filter / pi filter
- [x] RC snubber (ib)
- [x] Linear regulator power (LM317 resistors)
- [x] LM317 output voltage resistor calculator
- [x] Buck-boost / SEPIC (ib) (buck-boost-converter; SEPIC covered in notes)
- [x] Flyback transformer turns ratio (ib)
- [x] Inductor design (turns for AL value)
- [x] Air-core coil inductance (Wheeler)
- [ ] Ohm's law for AC (power, apparent, reactive)
- [ ] Decoupling capacitor selection (ib)
- [x] Crystal load capacitance
- [x] RC oscillator / phase-shift oscillator frequency (ib)
- [x] Schmitt trigger thresholds
- [x] Comparator hysteresis resistors (exists: schmitt-trigger)
- [x] Photodiode transimpedance amplifier (ib)
- [ ] Thermocouple amplifier gain
- [x] Battery internal resistance & runtime (Peukert) (peukerts-law)
- [x] Antenna length (λ/2, λ/4 dipole)
- [x] Free-space path loss
- [x] Microstrip impedance (ib)
- [x] Skin effect in PCB / wire (ib)
- [ ] Binary / hex / decimal / BCD converter (ib)
- [ ] Gray code converter (ib)
- [x] Logic level / pull-up resistor (I2C)
- [x] UART baud rate error
- [ ] RS-485 cable length & termination (ib)
- [x] Hall-effect current sensor scaling (ib)
- [x] Shunt resistor current measurement (ib)

## Physics
- [x] Impulse & momentum change
- [x] Elastic / inelastic collision
- [x] Friction force & coefficient
- [x] Inclined plane
- [x] Angular velocity ↔ rpm
- [x] Rotational kinetic energy & moment of inertia
- [x] Simple harmonic motion
- [x] Spring-mass frequency
- [x] Stress, strain & Young's modulus
- [x] Bernoulli equation (ib)
- [x] Stokes' law / terminal velocity
- [x] Drag force
- [x] Lift force
- [x] Thermal expansion of liquids (volumetric)
- [x] Latent heat
- [x] Newton's law of cooling
- [x] Stefan–Boltzmann radiation
- [x] Wien's law
- [x] Photon energy (E = hf)
- [x] de Broglie wavelength
- [x] E = mc²
- [x] Radioactive activity (Bq, Ci)
- [x] Magnetic field of a wire / solenoid
- [x] Lorentz force
- [x] Faraday's law (EMF) (ib)
- [x] Capacitance of parallel plates (ib)
- [x] Electric field & potential
- [x] Speed of sound in gases
- [x] Standing waves / string frequency
- [x] Beat frequency
- [x] Inverse square law (light, sound, radiation)
- [x] Lens power & magnification (mirror) — covered by thin-lens
- [x] Relativistic time dilation
- [x] Specific heat mixture (final temperature)
- [x] Carnot efficiency

## Chemistry
- [x] Mass ↔ moles ↔ volume (STP) (exists: chemistry/moles)
- [ ] Molar mass from formula
- [ ] Empirical formula
- [x] Limiting reagent
- [x] Theoretical yield
- [x] Normality
- [x] Solution preparation from solid (mass needed)
- [x] Stock dilution series (exists: biology/serial-dilution)
- [x] pOH / [H+] / [OH−]
- [x] Ka ↔ pKa, Kb ↔ pKb
- [x] pH of weak acid / weak base
- [x] Equilibrium constant (Kc, Kp)
- [x] Reaction rate & order
- [x] Activation energy from two rates
- [x] Enthalpy of reaction (Hess)
- [x] Heat of combustion / calorimetry (bomb)
- [x] Faraday electrolysis (mass deposited)
- [x] Cell potential (E°cell)
- [x] Raoult's law (vapour pressure)
- [x] Henry's law (gas solubility)
- [x] Van der Waals equation
- [x] Gay-Lussac's law
- [x] Avogadro's law
- [x] Water hardness (ppm CaCO₃)
- [x] TDS ↔ conductivity (ib)
- [x] Dissolved oxygen saturation
- [x] Conductivity cell constant (ib)
- [ ] ORP / chlorine dose (water treatment)

## Math
- [x] Linear equation solver / two equations
- [x] System of 3 equations
- [x] Cubic equation
- [ ] Polynomial roots
- [x] Matrix determinant / inverse (2×2, 3×3)
- [x] Vector magnitude, dot & cross product
- [x] Distance & midpoint
- [x] Equation of a line (two points) (exists: slope)
- [x] Circle equation from points
- [x] Angle converter (deg, rad, grad)
- [x] Law of sines
- [x] Triangle solver (SSS, SAS, ASA) — SSS: sss-triangle; SAS exists: law-of-cosines; ASA exists: law-of-sines
- [x] Hexagon / octagon (exists: math/polygon)
- [x] Prism / pyramid / frustum volume
- [x] Torus / capsule / hemisphere (torus done)
- [ ] Surface area of shapes
- [x] Arithmetic sequence
- [x] Geometric sequence & series
- [ ] Prime factorization
- [ ] Prime number checker
- [ ] LCM of many numbers
- [x] Fraction calculator (+ − × ÷) — fraction-calculator
- [ ] Mixed number ↔ improper fraction
- [ ] Decimal to fraction
- [x] Scientific notation
- [ ] Significant figures
- [ ] Rounding
- [x] Modulo
- [ ] Roman numerals
- [ ] Derivative (power rule, numeric)
- [ ] Definite integral (numeric)
- [ ] Limits / series sums
- [x] Interpolation (linear) (very useful for engineers)
- [ ] Unit circle / trig values
- [ ] Inverse trig
- [x] Complex numbers (polar ↔ rectangular)
- [ ] Log base converter / antilog
- [x] Exponential growth & decay (exists: biology/exponential-population-growth)
- [ ] Percentage increase/decrease of a value
- [ ] Ratio to percentage

## Statistics
- [x] t-test (one sample, two sample)
- [ ] Chi-square test
- [ ] Linear regression (least squares)
- [ ] Correlation coefficient
- [x] Variance (exists: standard-deviation)
- [ ] Mean absolute deviation
- [ ] Percentile / percentile rank
- [x] Outlier (IQR / Grubbs) (exists: quartiles)
- [x] Expected value
- [x] Bayes' theorem
- [x] Birthday paradox
- [x] Lottery odds (exists: combinations)
- [x] Exponential distribution
- [x] Uniform distribution
- [x] Hypergeometric distribution
- [x] Geometric distribution
- [x] P-value from z / t
- [ ] Moving average
- [x] Process capability (Cp, Cpk)
- [x] Control chart limits (X-bar, R)
- [x] Six sigma DPMO / sigma level
- [x] Measurement uncertainty (RSS combination)
