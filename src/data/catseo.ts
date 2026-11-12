// SEO content for category landing pages: meta title/description, H1, intro, grouped lists, guide text and FAQs.
// Text supports [label](url) and **bold**. Calculator ids in groups are slugs within the category.
export interface CatSEO {
  title: string; description: string; h1: string; intro: string;
  groups?: { name: string; ids: string[] }[];
  about?: { h: string; p: string }[];
  faq?: { q: string; a: string }[];
}
const IB = 'https://www.instrumentationblog.in';

export const CAT_SEO: Record<string, CatSEO> = {
  engineering: {
    title: 'Engineering Calculators – Flow, Pressure, Level & Instrumentation Calculators',
    description: 'Free engineering calculators for process and instrumentation engineers: 4–20 mA scaling, orifice and DP flow, Kv/Cv, pipe pressure drop, tank level, Pt100, pump power and more.',
    h1: 'Engineering calculators',
    intro: 'Free online engineering calculators for process, instrumentation and mechanical engineers. Scale a **4–20 mA** signal, size an **orifice plate** or **control valve**, work out **pipe pressure drop**, convert **tank level to volume** or check a **Pt100** reading — every calculator solves for any value you leave blank and shows the formula and steps. For in-depth articles on field instruments, see [Instrumentation Blog](' + IB + '/).',
    groups: [
      { name: 'Instrumentation & signals', ids: ['4-20ma-scaling', 'loop-resistance', 'pt100-resistance', 'dp-flow-square-root', 'flow-meter-k-factor', 'instrument-accuracy', 'turndown-ratio', 'rtd-lead-wire-error', 'signal-converter', 'plc-analog-scaling', 'low-flow-cutoff', 'sensor-response-time'] },
      { name: 'Calibration', ids: ['calibration-error', 'five-point-calibration'] },
      { name: 'Process control & PID tuning', ids: ['ziegler-nichols-pid-tuning', 'lambda-tuning', 'fopdt-step-test'] },
      { name: 'Flow measurement', ids: ['orifice-flow', 'venturi-flow', 'pitot-tube-velocity', 'weir-flow', 'mass-flow-rate', 'gas-flow-correction', 'pipe-flow-velocity', 'reynolds-number', 'rotameter-correction', 'vortex-shedding-frequency'] },
      { name: 'Pipe & open-channel hydraulics', ids: ['hazen-williams', 'minor-losses', 'manning-equation'] },
      { name: 'Pressure, level & tanks', ids: ['hydrostatic-pressure', 'dp-level-range', 'ultrasonic-level', 'vertical-tank-volume', 'horizontal-tank-volume', 'spherical-tank-volume', 'absolute-gauge-pressure', 'manometer', 'barlow-formula', 'darcy-weisbach-head-loss', 'water-hammer', 'api-gravity', 'cone-bottom-tank-volume', 'tank-drain-time'] },
      { name: 'Pressure vessels & testing', ids: ['pressure-vessel-thickness', 'hydrostatic-test-pressure'] },
      { name: 'Valves, pumps & heat', ids: ['control-valve-kv-cv', 'valve-authority', 'pump-power', 'npsh-available', 'pump-affinity-laws', 'pressure-to-head', 'fan-affinity-laws', 'compressor-power', 'heat-duty', 'thermal-expansion', 'air-receiver-size'] },
      { name: 'Heat transfer & HVAC', ids: ['lmtd', 'convection-heat-transfer', 'chiller-tonnage', 'dew-point', 'tank-heater-sizing', 'pipe-heat-loss', 'air-changes-per-hour'] },
      { name: 'Process & fluid properties', ids: ['residence-time', 'kinematic-viscosity'] },
      { name: 'Mechanical', ids: ['torque-power-speed', 'pulley-speed', 'hydraulic-cylinder-force', 'gear-ratio', 'shaft-diameter', 'bearing-life', 'bolt-torque', 'spring-rate', 'chain-length'] },
      { name: 'Strength of materials & structures', ids: ['beam-deflection', 'bending-stress', 'area-moment-of-inertia', 'factor-of-safety', 'weld-size'] },
      { name: 'Safety & reliability', ids: ['pfd-avg', 'availability-mtbf', 'safe-failure-fraction', 'weibull-reliability', 'acceleration-factor'] },
    ],
    about: [
      { h: 'Calculators built for the plant floor', p: 'These tools cover the everyday sums of process instrumentation: converting transmitter signals, checking loop power budgets, sizing primary flow elements and turning level into volume. They use the same equations found in ISO 5167, IEC 60751 and standard fluid-mechanics references, with units you can switch between metric and imperial.' },
      { h: 'Solve for any value', p: 'Unlike fixed-direction calculators, every field can be an input or an output. Enter a flow and solve for differential pressure, or enter a target process value and get the mA signal. Each result shows the formula used so you can check the working.' },
    ],
    faq: [
      { q: 'Are these engineering calculators free?', a: 'Yes. All calculators are free, need no sign-up and work on mobile.' },
      { q: 'Which standards do the flow calculators follow?', a: 'Orifice and Venturi calculators use the ISO 5167 flow equation with a user-entered discharge coefficient; the Pt100 calculator uses the IEC 60751 Callendar–Van Dusen equation.' },
      { q: 'Can I embed a calculator on my website?', a: 'Yes. Every calculator has an Embed button that gives you a copy-paste code snippet.' },
    ],
  },
  electrical: {
    title: 'Electrical Calculators – Power, Motor, Cable & Transformer Calculators',
    description: 'Free electrical calculators: kW to amps, kVA to kW, cable voltage drop, power factor correction, transformer current and fault level, motor slip, earthing, THD and more.',
    h1: 'Electrical calculators',
    intro: 'Free online electrical calculators for electricians, electrical engineers and students. Convert **kW to amps** and **kVA to kW**, check **cable voltage drop**, size a **capacitor bank for power factor correction**, find **transformer full-load and short-circuit current**, size **earth conductors** and measure **THD** — with formulas, worked examples and reference tables on every page.',
    groups: [
      { name: 'Power & current', ids: ['kw-to-amps', 'amps-to-watts', 'kva-to-kw', 'line-phase-voltage', 'power-factor-correction', 'capacitor-bank-kvar', 'ups-sizing', 'battery-bank-size', 'generator-size'] },
      { name: 'Generators', ids: ['generator-frequency', 'generator-power-angle'] },
      { name: 'Energy, demand & metering', ids: ['load-factor', 'energy-meter-constant'] },
      { name: 'Motors & drives', ids: ['three-phase-motor-power', 'motor-starting-current', 'induction-motor-slip', 'voltage-unbalance', 'braking-resistor', 'motor-starting-voltage-dip'] },
      { name: 'Transformers & fault level', ids: ['transformer-size', 'transformer-current', 'transformer-short-circuit', 'transformer-turns-ratio', 'transformer-efficiency', 'autotransformer', 'per-unit', 'ct-burden'] },
      { name: 'Cables, busbars, earthing & power quality', ids: ['cable-voltage-drop', 'wire-resistance', 'busbar-size', 'skin-depth', 'earth-fault-loop-impedance', 'earth-conductor-size', 'earthing-resistance', 'thd', 'neutral-current-harmonics', 'star-delta-transformation'] },
      { name: 'Solar PV', ids: ['solar-string-sizing'] },
      { name: 'Transmission lines & insulation testing', ids: ['ferranti-effect', 'polarization-index'] },
      { name: 'Lighting', ids: ['lumen-method'] },
    ],
    about: [
      { h: 'For LV and MV power systems', p: 'The calculators cover single-phase, three-phase and DC circuits at common Indian, European and North American voltages (230/415 V, 400 V, 120/208/480 V and 11 kV). Formulas follow IEC 60364, IEC 60076, IEEE 519 and NEMA MG 1 where relevant, and each page explains the assumptions.' },
      { h: 'From quick checks to design', p: 'Use them for quick site checks — will this cable drop too much voltage, how many amps will this motor draw — or as a starting point for design. For final designs, always confirm against manufacturer data and your local wiring regulations.' },
    ],
    faq: [
      { q: 'How do I convert kW to amps for a three-phase motor?', a: 'I = P ÷ (√3 × V × PF × efficiency). Use the kW to amps or three-phase motor power calculator, which apply this formula for you.' },
      { q: 'Do these calculators work for 50 Hz and 60 Hz systems?', a: 'Yes. Where frequency matters — such as power factor correction or motor speed — you can enter 50 or 60 Hz.' },
      { q: 'Are the results suitable for final design?', a: 'They are accurate for the formulas shown, but final designs must also consider installation conditions, derating and local regulations.' },
    ],
  },
  electronics: {
    title: 'Electronics Calculators – LED Resistor, Voltage Divider, 555 Timer, Filters & More',
    description: 'Free electronics calculators: LED resistor, voltage divider, resistor colour code, 555 timer, RC filter, op-amp gain, buck and boost converter, PCB trace width, ADC resolution.',
    h1: 'Electronics calculators',
    intro: 'Free online electronics calculators for hobbyists, students and circuit designers. Find the right **LED resistor**, design a **voltage divider**, read a **resistor colour code**, set a **555 timer** frequency, choose an **RC filter** cut-off, size a **buck or boost converter** and check **PCB trace width** — each with formulas, standard values and design tips.',
    groups: [
      { name: 'Resistors & basic circuits', ids: ['led-resistor', 'voltage-divider', 'current-divider', 'resistor-color-code', 'zener-resistor', 'transistor-base-resistor', 'wheatstone-bridge'] },
      { name: 'Capacitors, inductors & AC', ids: ['capacitor-energy', 'capacitors-series-parallel', 'inductor-energy', 'rl-time-constant', 'reactance', 'resonant-frequency', 'rc-filter', 'lc-filter', 'capacitor-lifetime', 'air-core-inductor', 'inductor-al-value'] },
      { name: 'Timing, amplifiers & signals', ids: ['555-timer', 'op-amp-gain', 'instrumentation-amplifier-gain', 'pwm-duty-cycle', 'adc-resolution', 'snr', 'dbm-to-watts', 'rc-phase-shift-oscillator', 'crystal-load-capacitance', 'uart-baud-rate-error', 'i2c-pull-up-resistor'] },
      { name: 'Op-amp circuits, active filters & comparators', ids: ['summing-amplifier', 'differential-amplifier', 'op-amp-integrator', 'sallen-key-low-pass', 'schmitt-trigger'] },
      { name: 'Power electronics & PCB', ids: ['buck-converter', 'boost-converter', 'mosfet-power-loss', 'heat-sink', 'pcb-trace-width', 'microstrip-impedance', 'battery-charge-time', 'lm317', 'buck-boost-converter', 'flyback-transformer', 'peukerts-law']
      },
      { name: 'RF & wireless', ids: ['antenna-length', 'free-space-path-loss'] },
      { name: 'Sensors & current sensing', ids: ['ntc-thermistor', 'strain-gauge', 'shunt-resistor', 'transimpedance-amplifier', 'hall-effect-current-sensor'] },
    ],
    about: [
      { h: 'Design faster, with fewer mistakes', p: 'Each calculator works in both directions: get the output of a circuit, or enter the output you want and solve for the component value. Results are shown in convenient units — kΩ, µF, mH, kHz — and pages list the nearest standard values.' },
      { h: 'Learn as you calculate', p: 'Every page explains the formula, gives a worked example and includes reference tables, so the calculators double as a quick electronics reference.' },
    ],
    faq: [
      { q: 'What resistor do I need for an LED?', a: 'R = (supply voltage − LED forward voltage) ÷ LED current. The LED resistor calculator does this for single LEDs and series strings.' },
      { q: 'Can I solve for a component value?', a: 'Yes. Enter the result you want, then press × on the component field to have it calculated.' },
      { q: 'Are standard E12/E24 values included?', a: 'Pages such as the LED resistor and resistor colour code calculators list standard values to help you pick real parts.' },
    ],
  },
  physics: {
    title: 'Physics Calculators – Mechanics, Electricity, Waves & Heat Calculators',
    description: 'Free physics calculators with formulas and steps: force, velocity, SUVAT, kinetic and potential energy, projectile motion, Ohm’s law, pressure, density, waves, optics and gravity.',
    h1: 'Physics calculators',
    intro: 'Free online physics calculators for students, teachers and engineers. Solve **SUVAT** and **projectile motion** problems, find **force**, **momentum**, **kinetic** and **potential energy**, apply **Ohm’s law**, work out **pressure**, **density** and **buoyancy**, and explore **waves**, **optics** and **gravity** — every calculator shows the formula and solves for any unknown.',
    groups: [
      { name: 'Motion & kinematics', ids: ['speed-distance-time', 'acceleration', 'suvat-equations', 'free-fall', 'projectile-motion', 'momentum', 'impulse', 'elastic-collision', 'angular-velocity'] },
      { name: 'Forces & energy', ids: ['force', 'weight', 'torque', 'centripetal-force', 'hookes-law', 'kinetic-energy', 'potential-energy', 'work-and-power', 'friction-force', 'inclined-plane', 'rotational-kinetic-energy', 'youngs-modulus'] },
      { name: 'Fluids, heat & gases', ids: ['pressure', 'density', 'buoyancy', 'stokes-law', 'drag-force', 'heat-conduction', 'newtons-law-of-cooling', 'latent-heat', 'ideal-gas-law', 'bernoulli-equation', 'lift-force', 'liquid-thermal-expansion', 'stefan-boltzmann-law', 'final-temperature', 'carnot-efficiency'] },
      { name: 'Electricity & magnetism', ids: ['ohms-law', 'resistors-series-parallel', 'rc-time-constant', 'coulombs-law', 'parallel-plate-capacitor', 'magnetic-field', 'lorentz-force', 'faradays-law', 'electric-field'] },
      { name: 'Waves, sound & light', ids: ['wavelength-frequency', 'doppler-effect', 'decibel', 'snells-law', 'thin-lens', 'pendulum', 'spring-mass-frequency', 'simple-harmonic-motion', 'speed-of-sound', 'string-frequency', 'beat-frequency', 'inverse-square-law'] },
      { name: 'Modern, nuclear & quantum physics', ids: ['photon-energy', 'de-broglie-wavelength', 'wiens-law', 'mass-energy-equivalence', 'radioactive-activity', 'time-dilation'] },
      { name: 'Gravity & orbits', ids: ['gravitational-force', 'escape-velocity', 'orbital-period'] },
    ],
    about: [
      { h: 'For homework, exams and real problems', p: 'The calculators cover the core of school and university physics — mechanics, thermodynamics, electricity, waves and astrophysics. Units switch between SI and imperial, and each page has worked examples and reference tables.' },
    ],
    faq: [
      { q: 'Do the physics calculators show the working?', a: 'Yes. Press “Show steps” to see the formula and how the answer was found.' },
      { q: 'Can I use different units?', a: 'Yes. Each field has a unit selector, and values convert automatically.' },
    ],
  },
  chemistry: {
    title: 'Chemistry Calculators – Molarity, Moles, pH, Dilution, Gas Laws & More',
    description: 'Free chemistry calculators: molarity, moles, dilution (C1V1 = C2V2), pH, buffers, gas laws, percent yield, titration, colligative properties, Nernst and Arrhenius equations.',
    h1: 'Chemistry calculators',
    intro: 'Free online chemistry calculators for students and lab work. Calculate **molarity**, **moles** and **dilutions**, find **pH** and **buffer** pH, apply the **gas laws**, check **percent yield** and **titrations**, and work with **colligative properties** and **electrochemistry** — with formulas and worked examples.',
    groups: [
      { name: 'Concentration & solutions', ids: ['molarity', 'molality', 'moles', 'dilution', 'mass-percent', 'ppm', 'percent-composition', 'normality', 'solution-preparation', 'brix-specific-gravity'] },
      { name: 'Stoichiometry & reaction yield', ids: ['limiting-reagent', 'theoretical-yield'] },
      { name: 'Vapour pressure, gas solubility & water chemistry', ids: ['raoults-law', 'henrys-law', 'water-hardness', 'dissolved-oxygen-saturation', 'tds-conductivity', 'conductivity-cell-constant'] },
      { name: 'Acids, bases & analysis', ids: ['ph', 'pka', 'weak-acid-ph', 'henderson-hasselbalch', 'titration', 'beer-lambert'] },
      { name: 'Electrochemistry', ids: ['nernst-equation', 'faraday-electrolysis', 'cell-potential'] },
      { name: 'Gas laws', ids: ['boyles-law', 'charles-law', 'combined-gas-law', 'gay-lussacs-law', 'avogadros-law', 'daltons-law', 'grahams-law', 'van-der-waals', 'gas-density'] },
      { name: 'Thermodynamics, kinetics & colligative properties', ids: ['specific-heat', 'gibbs-free-energy', 'arrhenius-equation', 'activation-energy', 'half-life', 'boiling-point-elevation', 'freezing-point-depression', 'osmotic-pressure', 'percent-yield', 'equilibrium-constant', 'bomb-calorimeter', 'integrated-rate-law', 'enthalpy-of-reaction'] },
    ],
    faq: [
      { q: 'How do I calculate molarity?', a: 'Molarity = moles of solute ÷ litres of solution. The molarity calculator also finds the mass to weigh out.' },
      { q: 'Are these suitable for lab use?', a: 'Yes — they use standard formulas. Always double-check critical preparations against your lab procedures.' },
    ],
  },
  math: {
    title: 'Math Calculators – Percentage, Geometry, Algebra & Trigonometry Calculators',
    description: 'Free math calculators: percentage and percentage change, area and volume of shapes, Pythagoras, trigonometry, quadratic equations, logarithms, fractions, GCF and LCM.',
    h1: 'Math calculators',
    intro: 'Free online math calculators for everyday sums, homework and work. Find **percentages** and **percentage change**, calculate the **area** and **volume** of any shape, solve **right triangles** and **quadratic equations**, and work with **logarithms**, **exponents**, **fractions** and **ratios** — step by step.',
    groups: [
      { name: 'Percentages & ratios', ids: ['percentage', 'percentage-change', 'percent-error', 'ratio', 'fraction-to-decimal', 'average', 'weighted-average', 'fraction-calculator'] },
      { name: 'Geometry: 2D shapes', ids: ['circle', 'rectangle', 'triangle-area', 'trapezoid-area', 'polygon', 'ellipse', 'arc-length'] },
      { name: 'Geometry: 3D shapes', ids: ['box-volume', 'cylinder-volume', 'cone', 'sphere', 'pyramid-volume', 'frustum-volume', 'torus', 'hemisphere', 'capsule'] },
      { name: 'Triangles & trigonometry', ids: ['pythagorean-theorem', 'right-triangle-trig', 'law-of-cosines', 'law-of-sines', 'sss-triangle', 'slope', 'angle-converter'] },
      { name: 'Coordinate geometry, vectors & interpolation', ids: ['distance-midpoint', 'vector', 'complex-number', 'linear-interpolation', 'circle-three-points'] },
      { name: 'Algebra & numbers', ids: ['quadratic-equation', 'cubic-equation', 'exponent', 'square-root', 'logarithm', 'factorial', 'gcf-lcm', 'arithmetic-sequence', 'geometric-sequence', 'modulo', 'scientific-notation'] },
      { name: 'Systems of linear equations', ids: ['system-of-equations', 'system-of-3-equations', 'matrix-determinant'] },
    ],
    faq: [
      { q: 'How do I calculate a percentage of a number?', a: 'Multiply the number by the percentage and divide by 100. The percentage calculator also finds what percent one number is of another.' },
      { q: 'Do the calculators show steps?', a: 'Yes. Press “Show steps” to see the formula and working.' },
    ],
  },
  statistics: {
    title: 'Statistics Calculators – Standard Deviation, Probability, Z-Score & Sample Size',
    description: 'Free statistics calculators: mean, median, mode, standard deviation, z-score, normal distribution, confidence interval, margin of error, sample size, binomial and Poisson probability.',
    h1: 'Statistics calculators',
    intro: 'Free online statistics and probability calculators. Paste a data set to get the **mean, median, mode**, **standard deviation** and **quartiles**, find **z-scores** and **normal distribution** probabilities, calculate **confidence intervals**, **margin of error** and **sample size**, and work out **binomial**, **Poisson**, **permutation** and **combination** problems.',
    groups: [
      { name: 'Descriptive statistics', ids: ['mean-median-mode', 'standard-deviation', 'quartiles', 'coefficient-of-variation', 'geometric-mean', 'sum-of-squares', 'standard-error'] },
      { name: 'Distributions', ids: ['z-score', 'normal-distribution', 'empirical-rule', 'binomial-probability', 'poisson-probability', 'exponential-distribution', 'uniform-distribution', 'geometric-distribution', 'hypergeometric-distribution'] },
      { name: 'Hypothesis tests & p-values', ids: ['one-sample-t-test', 'two-sample-t-test', 'p-value'] },
      { name: 'Inference & surveys', ids: ['confidence-interval', 'margin-of-error', 'sample-size', 'relative-risk'] },
      { name: 'Probability & counting', ids: ['probability', 'odds-probability', 'permutations', 'combinations', 'bayes-theorem', 'expected-value', 'birthday-paradox'] },
      { name: 'Quality & measurement', ids: ['process-capability', 'control-chart', 'six-sigma', 'measurement-uncertainty'] },
    ],
    faq: [
      { q: 'Can I paste a list of numbers?', a: 'Yes. Data-set calculators accept numbers separated by commas, spaces or new lines.' },
      { q: 'Sample or population standard deviation?', a: 'The standard deviation calculator shows both.' },
    ],
  },
  conversion: {
    title: 'Unit Converters – Length, Weight, Temperature, Pressure, Flow & Land Area',
    description: 'Free unit converters: cm to inches, kg to lbs, °F to °C, psi to bar, flow rate, pressure, energy, power and Indian land units (gaj, guntha, cent, acre) — instant and accurate.',
    h1: 'Unit converters',
    intro: 'Free online unit converters for everyday and engineering units. Convert **length**, **weight**, **temperature**, **volume**, **speed**, **pressure**, **flow rate**, **energy**, **power** and **torque**, plus Indian land units such as **gaj**, **guntha** and **cent** — with conversion tables on every page.',
    groups: [
      { name: 'Length & distance', ids: ['length-converter', 'cm-to-inches', 'inches-to-cm', 'mm-to-inches', 'feet-to-inches', 'feet-to-meters', 'meters-to-feet', 'km-to-miles', 'miles-to-km'] },
      { name: 'Weight & mass', ids: ['kg-to-lb', 'lbs-to-kg', 'oz-to-grams', 'stone-to-kg'] },
      { name: 'Temperature', ids: ['temperature-converter', 'fahrenheit-to-celsius'] },
      { name: 'Volume', ids: ['volume-converter', 'liters-to-gallons', 'gallons-to-liters', 'ml-to-oz'] },
      { name: 'Area & land', ids: ['area-converter', 'sq-ft-to-sq-m', 'sq-m-to-sq-ft', 'acres-to-hectares', 'gaj-to-sq-ft', 'guntha-to-sq-ft', 'cent-to-sq-ft'] },
      { name: 'Engineering units', ids: ['pressure-converter', 'psi-to-bar', 'flow-rate-converter', 'power-converter', 'kw-to-hp', 'energy-converter', 'torque-converter', 'speed-converter', 'mph-to-kmh'] },
      { name: 'Numbers', ids: ['number-to-million'] },
    ],
    faq: [
      { q: 'Are the conversion factors exact?', a: 'Yes — they use exact SI definitions where they exist (for example 1 inch = 2.54 cm and 1 lb = 0.45359237 kg).' },
      { q: 'Do you support Indian land units?', a: 'Yes: gaj (square yard), guntha, cent, acre and hectare.' },
    ],
  },
  finance: {
    title: 'Finance Calculators – EMI, SIP, Income Tax, GST, FD, PPF & Investment Calculators',
    description: 'Free finance calculators for India and worldwide: EMI, SIP, step-up SIP, income tax (new vs old regime), GST, FD, RD, PPF, EPF, NPS, compound interest, CAGR and ROI.',
    h1: 'Finance calculators',
    intro: 'Free online financial calculators for loans, savings, investments and tax. Work out your **loan EMI**, plan a **SIP** or **lumpsum** investment, compare the **new and old income tax regimes**, add or remove **GST**, and see what your **FD**, **RD**, **PPF**, **EPF**, **NPS** or **Sukanya Samriddhi** account will grow to.',
    groups: [
      { name: 'Loans', ids: ['emi', 'loan-payment', 'mortgage', 'credit-card-payoff', 'debt-to-income', 'simple-interest'] },
      { name: 'Mutual funds & investing', ids: ['sip', 'step-up-sip', 'lumpsum', 'swp', 'cagr', 'compound-interest', 'stock-average', 'pe-ratio', 'dividend-yield', 'roi', 'real-return'] },
      { name: 'Government savings schemes (India)', ids: ['ppf', 'epf', 'nps', 'sukanya-samriddhi', 'nsc', 'kvp', 'scss', 'post-office-mis', 'fd', 'rd'] },
      { name: 'Tax & salary', ids: ['income-tax-india', 'gst', 'hra-exemption', 'gratuity', 'sales-tax-vat', 'salary-increase', 'hourly-to-salary'] },
      { name: 'Planning', ids: ['retirement-corpus', 'savings-goal', 'inflation', 'future-value', 'present-value', 'annuity-payout', 'doubling-time'] },
      { name: 'Business & marketing', ids: ['break-even', 'profit-margin', 'discount', 'commission', 'payback-period', 'roas', 'ad-metrics', 'customer-lifetime-value'] },
    ],
    faq: [
      { q: 'Are the Indian interest rates up to date?', a: 'Small savings scheme rates are updated each quarter when the government announces them; you can also enter any rate yourself.' },
      { q: 'Is this financial advice?', a: 'No. The calculators give estimates to help you plan; consult a qualified adviser for decisions.' },
    ],
  },
  health: {
    title: 'Health Calculators – BMI, BMR, Calories, Body Fat, Ideal Weight & More',
    description: 'Free health and fitness calculators: BMI, BMR and daily calories, body fat, ideal weight, macros, water intake, heart rate zones, plus clinical tools like eGFR and QTc.',
    h1: 'Health calculators',
    intro: 'Free online health and fitness calculators. Check your **BMI**, estimate **daily calories** with BMR, measure **body fat** and **ideal weight**, plan **macros**, **protein** and **water intake**, and find your **heart rate zones** — plus clinical calculators such as **eGFR**, **creatinine clearance** and **QTc**.',
    faq: [
      { q: 'Are these calculators medical advice?', a: 'No. They give estimates for general information. Speak to a doctor about your health.' },
    ],
  },
  construction: {
    title: 'Construction Calculators – Concrete, Bricks, Cement, Steel, Paint & Tiles',
    description: 'Free construction calculators: concrete volume and mix, bricks, mortar, cement and sand, rebar and steel weight, paint, tiles, flooring, roof pitch and stairs.',
    h1: 'Construction calculators',
    intro: 'Free online construction calculators for builders, engineers and home owners. Estimate **concrete**, **cement, sand and aggregate**, **bricks** and **mortar**, **rebar weight**, **paint**, **tiles** and **flooring**, and design **roofs** and **stairs** — with wastage allowances built in.',
  },
  biology: {
    title: 'Biology Calculators – Lab, Genetics, Cell Culture & Microscopy Calculators',
    description: 'Free biology calculators for the lab: DNA and protein concentration, serial dilution, PCR, primer Tm, centrifuge RCF, cell counting, doubling time, Hardy–Weinberg and population growth.',
    h1: 'Biology calculators',
    intro: 'Free online biology calculators for students and lab scientists. Calculate **DNA, RNA and protein concentration**, plan **serial dilutions**, **PCR** and **ligations**, convert **centrifuge rpm to g-force**, count cells with a **hemocytometer**, and model **population growth** and **Hardy–Weinberg** genetics.',
  },
  ecology: {
    title: 'Ecology & Energy Calculators – Carbon Footprint, Solar, EV and Water Savings',
    description: 'Free ecology calculators: carbon footprint of cars, flights and electricity, solar system size and output, EV charging and running cost, rainwater harvesting and water savings.',
    h1: 'Ecology & energy calculators',
    intro: 'Free online calculators for a lighter footprint. Measure the **carbon footprint** of driving, flying and electricity, size a **solar system** and **battery**, compare **EV vs petrol** costs, and work out **rainwater harvesting** and **water savings**.',
    groups: [
      { name: 'Solar, wind & storage', ids: ['solar-system-size', 'solar-output', 'battery-storage', 'wind-turbine-power'] },
      { name: 'Electric vehicles & transport', ids: ['ev-vs-petrol', 'ev-charging-time', 'bike-vs-car', 'car-carbon-footprint', 'flight-emissions'] },
      { name: 'Carbon footprint & offsets', ids: ['electricity-co2', 'carbon-offset-cost', 'tree-offset', 'led-savings'] },
      { name: 'Water saving', ids: ['rainwater-harvesting', 'shower-water', 'water-leak', 'garden-irrigation'] },
      { name: 'Garden & field ecology', ids: ['compost-ratio', 'pond-liner', 'mark-recapture', 'population-density'] },
    ],
    about: [
      { h: 'Turn green choices into numbers', p: 'Saving energy, water and carbon is easier when you can see the figures. These calculators show how many kWh a rooftop solar system will make, how much CO₂ your car or flight emits, what an EV really costs per kilometre compared with petrol, and how much water a leaking tap or long shower wastes in a year.' },
      { h: 'How the figures are calculated', p: 'Carbon results use published emission factors per kWh, litre of fuel and passenger kilometre, which you can change to match your country or supplier. Solar estimates use peak sun hours and a system loss factor; EV costs use your own tariff and fuel price. Every result shows the formula so you can check it.' },
      { h: 'For homes, schools and field work', p: 'Use them to size a home solar and battery system, plan rainwater storage, compare commuting options, or set class projects on energy saving. The field ecology tools (mark and recapture, population density) help students and researchers estimate wildlife populations.' },
    ],
    faq: [
      { q: 'How much CO₂ does 1 kWh of electricity produce?', a: 'It depends on the grid. India averages about 0.7 kg CO₂ per kWh, the UK about 0.2 kg and France under 0.1 kg. Enter your own factor in the electricity CO₂ calculator.' },
      { q: 'What size solar system do I need for my home?', a: 'Divide your daily kWh use by the local peak sun hours and allow about 20% for losses. 10 kWh a day with 5 sun hours needs roughly a 2.5 kW system.' },
      { q: 'Is an EV cheaper to run than a petrol car?', a: 'Usually yes. At typical Indian prices an EV costs about ₹1 to ₹2 per km against ₹6 to ₹8 per km for petrol. Try the EV vs petrol calculator with your own numbers.' },
      { q: 'How many trees offset one tonne of CO₂?', a: 'A mature tree absorbs about 20 to 25 kg of CO₂ a year, so roughly 40 to 50 trees offset one tonne each year.' },
    ],
  },
  'everyday-life': {
    title: 'Everyday Calculators – Age, Dates, Time, Fuel Cost, Tips & More',
    description: 'Free everyday calculators: age, days between dates, countdowns, time duration, hours worked, fuel cost, electricity bill, tip and bill split, CGPA to percentage.',
    h1: 'Everyday life calculators',
    intro: 'Free online calculators for daily life. Work out your exact **age**, count **days between dates**, add up **hours worked**, estimate **fuel** and **electricity costs**, split a **bill**, and convert **CGPA to percentage**.',
  },
  food: {
    title: 'Cooking Calculators – Recipe Scaling, Cups to Grams, Oven Temperature & More',
    description: 'Free food and cooking calculators: recipe scaler, grams to cups, cooking measurement converter, oven temperatures, baker’s percentage, rice to water ratio and party food planning.',
    h1: 'Food & cooking calculators',
    intro: 'Free online cooking calculators. **Scale recipes**, convert **grams to cups** and **oven temperatures**, get the right **rice-to-water** and **coffee** ratios, use **baker’s percentages** and plan food and drinks for parties.',
  },
  sports: {
    title: 'Sports Calculators – Cricket Run Rate, Running Pace, 1RM & More',
    description: 'Free sports calculators: cricket run rate, net run rate, batting and bowling averages, running pace and race predictor, one-rep max, cycling gears and swim pace.',
    h1: 'Sports calculators',
    intro: 'Free online sports calculators. Work out **cricket run rate**, **net run rate** and **batting and bowling averages**, plan your **running pace** and predict **race times**, estimate your **one-rep max**, and more.',
  },
  other: {
    title: 'Other Calculators – Tech, Pets, Pregnancy and Handy Tools',
    description: 'Free handy calculators: download time, data storage, screen PPI, print size, password strength, dog and cat age, pregnancy due date, LPG cylinder duration and more.',
    h1: 'Other calculators',
    intro: 'Handy calculators that don’t fit anywhere else — **download time**, **data storage**, **screen PPI** and **print size**, **password strength**, **dog and cat age**, **due dates** and **LPG cylinder** duration.',
  },
};
