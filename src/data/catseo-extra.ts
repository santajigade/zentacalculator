// Extra content for category landing pages (added 2026-11-16 to make each hub page genuinely useful).
// Merged into CAT_SEO in src/pages/[category]/index.astro: groups are used only when the category has none,
// about and faq entries are appended after the existing ones. Text supports [label](url) and **bold**.
import type { CatSEO } from './catseo.ts';

type Extra = Pick<CatSEO, 'groups' | 'about' | 'faq'>;

export const CAT_EXTRA: Record<string, Extra> = {
  engineering: {
    about: [
      { h: 'Flow and level measurement', p: 'For differential pressure flow, size the primary element with the [orifice flow](/engineering/orifice-flow/) or [Venturi](/engineering/venturi-flow/) calculator, then set the transmitter range with the [DP flow square root](/engineering/dp-flow-square-root/) calculator. Pulse output meters need the [K-factor calculator](/engineering/flow-meter-k-factor/), and gas meters reading at line conditions need [gas flow correction](/engineering/gas-flow-correction/) to standard conditions. For level, set a DP transmitter range with the [DP level range calculator](/engineering/dp-level-range/), then convert level into volume for a [vertical](/engineering/vertical-tank-volume/), [horizontal](/engineering/horizontal-tank-volume/) or [spherical tank](/engineering/spherical-tank-volume/).' },
      { h: 'Control, calibration and safety', p: 'Check a loop before commissioning with the [loop resistance](/engineering/loop-resistance/) and [4-20 mA scaling](/engineering/4-20ma-scaling/) calculators, and verify instruments with the [calibration error](/engineering/calibration-error/) and [five-point calibration](/engineering/five-point-calibration/) tools. Tune controllers with [Ziegler-Nichols](/engineering/ziegler-nichols-pid-tuning/) or [lambda tuning](/engineering/lambda-tuning/) from a [FOPDT step test](/engineering/fopdt-step-test/). For functional safety, the [PFDavg](/engineering/pfd-avg/) and [safe failure fraction](/engineering/safe-failure-fraction/) calculators follow IEC 61508 and IEC 61511.' },
    ],
    faq: [
      { q: 'Who builds these engineering calculators?', a: 'They are written and checked by an electronics and instrumentation engineer with hands-on experience of process instruments, and every formula is shown on the page so you can verify it.' },
    ],
  },
  electronics: {
    about: [
      { h: 'Analog and power circuits', p: 'For op-amp stages there are [op-amp gain](/electronics/op-amp-gain/), [summing](/electronics/summing-amplifier/), [differential](/electronics/differential-amplifier/), [instrumentation amplifier](/electronics/instrumentation-amplifier-gain/), [integrator](/electronics/op-amp-integrator/) and [transimpedance](/electronics/transimpedance-amplifier/) calculators, plus [Sallen-Key](/electronics/sallen-key-low-pass/) and [RC filters](/electronics/rc-filter/). Power designers can size [buck](/electronics/buck-converter/), [boost](/electronics/boost-converter/) and [buck-boost](/electronics/buck-boost-converter/) converters, an [LM317](/electronics/lm317/) regulator, a [heat sink](/electronics/heat-sink/) and [MOSFET losses](/electronics/mosfet-power-loss/).' },
      { h: 'Sensors, digital and RF', p: 'Sensor front ends are covered by the [Wheatstone bridge](/electronics/wheatstone-bridge/), [strain gauge](/electronics/strain-gauge/), [NTC thermistor](/electronics/ntc-thermistor/), [shunt resistor](/electronics/shunt-resistor/) and [Hall-effect current sensor](/electronics/hall-effect-current-sensor/) calculators. For microcontrollers, check [ADC resolution](/electronics/adc-resolution/), [I2C pull-up](/electronics/i2c-pull-up-resistor/) values and [UART baud rate error](/electronics/uart-baud-rate-error/). For RF and PCB work there are [dBm to watts](/electronics/dbm-to-watts/), [free space path loss](/electronics/free-space-path-loss/), [antenna length](/electronics/antenna-length/), [microstrip impedance](/electronics/microstrip-impedance/) and [PCB trace width](/electronics/pcb-trace-width/).' },
    ],
  },
  physics: {
    about: [
      { h: 'Mechanics: from SUVAT to orbits', p: 'Most school and first-year physics problems are mechanics. The [SUVAT calculator](/physics/suvat-equations/) solves any of the five constant-acceleration equations once you know three values, and the [projectile motion calculator](/physics/projectile-motion/) splits a launch into horizontal and vertical parts to give range, height and flight time. For forces, start with [Newton\'s second law](/physics/force/), then add [friction](/physics/friction-force/), an [inclined plane](/physics/inclined-plane/) or [drag](/physics/drag-force/). Energy problems are often quicker: equate [kinetic](/physics/kinetic-energy/) and [potential energy](/physics/potential-energy/) and the path the object took no longer matters. For planets and satellites, use [gravitational force](/physics/gravitational-force/), [orbital period](/physics/orbital-period/) and [escape velocity](/physics/escape-velocity/).' },
      { h: 'Heat, waves and light', p: 'Thermal tools cover [specific heat and final temperature](/physics/final-temperature/), [latent heat](/physics/latent-heat/), [conduction through a wall](/physics/heat-conduction/) and [Newton\'s law of cooling](/physics/newtons-law-of-cooling/), which is how forensic scientists and food engineers estimate cooling times. For waves, the [wavelength and frequency calculator](/physics/wavelength-frequency/) links v = fλ, the [Doppler effect calculator](/physics/doppler-effect/) gives the pitch shift of a moving source, and the [decibel calculator](/physics/decibel/) handles sound and signal levels. Optics is covered by [Snell\'s law](/physics/snells-law/) and the [thin lens equation](/physics/thin-lens/).' },
      { h: 'Electricity, magnetism and modern physics', p: 'Start circuits with [Ohm\'s law](/physics/ohms-law/) and [resistors in series and parallel](/physics/resistors-series-parallel/), then move on to the [RC time constant](/physics/rc-time-constant/) and [parallel plate capacitor](/physics/parallel-plate-capacitor/). Fields are covered by [Coulomb\'s law](/physics/coulombs-law/), [electric field](/physics/electric-field/), [magnetic field](/physics/magnetic-field/), the [Lorentz force](/physics/lorentz-force/) and [Faraday\'s law](/physics/faradays-law/). For twentieth-century physics there are [photon energy](/physics/photon-energy/), [de Broglie wavelength](/physics/de-broglie-wavelength/), [E = mc²](/physics/mass-energy-equivalence/), [time dilation](/physics/time-dilation/) and [radioactive activity](/physics/radioactive-activity/).' },
    ],
    faq: [
      { q: 'Which physics calculator should I use for a falling object?', a: 'Without air resistance, use the free fall calculator (g = 9.81 m/s²). If the object is light or fast, such as a raindrop or a skydiver, air drag matters, so combine the drag force calculator with Newton\'s second law.' },
      { q: 'What value of g is used?', a: 'Standard gravity, 9.80665 m/s², unless the calculator lets you enter your own value, for example for the Moon (1.62 m/s²) or Mars (3.71 m/s²).' },
    ],
  },
  chemistry: {
    about: [
      { h: 'Solutions and concentration', p: 'Most lab calculations come back to concentration. Use the [moles calculator](/chemistry/moles/) to convert between mass and amount, the [molarity calculator](/chemistry/molarity/) for mol/L, and the [solution preparation calculator](/chemistry/solution-preparation/) to find how many grams to weigh for a given volume. To make a weaker solution from a stock, use the [dilution calculator](/chemistry/dilution/) (C₁V₁ = C₂V₂). Other units have their own tools: [molality](/chemistry/molality/) for colligative properties, [normality](/chemistry/normality/) for titrations, [mass percent](/chemistry/mass-percent/) and [ppm](/chemistry/ppm/) for trace levels.' },
      { h: 'Acids, bases and equilibrium', p: 'The [pH calculator](/chemistry/ph/) handles strong acids and bases, and the [weak acid pH calculator](/chemistry/weak-acid-ph/) uses Ka for acetic acid and similar compounds. For buffers, the [Henderson-Hasselbalch calculator](/chemistry/henderson-hasselbalch/) gives the pH from the acid and conjugate base ratio, and the [pKa calculator](/chemistry/pka/) converts between Ka and pKa. Titration results go in the [titration calculator](/chemistry/titration/). For reactions at equilibrium, use the [equilibrium constant](/chemistry/equilibrium-constant/) and [Gibbs free energy](/chemistry/gibbs-free-energy/) calculators to see which way a reaction runs.' },
      { h: 'Gases, kinetics and industrial chemistry', p: 'The [ideal gas law](/physics/ideal-gas-law/) and the [combined gas law](/chemistry/combined-gas-law/) cover most gas problems, with [Van der Waals](/chemistry/van-der-waals/) for real gases at high pressure. Reaction speed is handled by the [Arrhenius equation](/chemistry/arrhenius-equation/), [activation energy](/chemistry/activation-energy/), [half-life](/chemistry/half-life/) and the [integrated rate law](/chemistry/integrated-rate-law/). Plant and water chemists will find [water hardness](/chemistry/water-hardness/), [TDS from conductivity](/chemistry/tds-conductivity/), [dissolved oxygen saturation](/chemistry/dissolved-oxygen-saturation/), [combustion air](/chemistry/combustion-air/) and [GCV to NCV](/chemistry/gcv-to-ncv/) for fuels.' },
    ],
    faq: [
      { q: 'Where do the molar masses come from?', a: 'Molar mass tools use IUPAC standard atomic weights. For hydrates and salts, enter the molar mass of the exact compound on the bottle label.' },
      { q: 'What is the difference between molarity and molality?', a: 'Molarity is moles per litre of solution and changes slightly with temperature. Molality is moles per kilogram of solvent and does not, which is why it is used for boiling point elevation and freezing point depression.' },
    ],
  },
  math: {
    about: [
      { h: 'Percentages and everyday maths', p: 'The most used maths tools are the simplest. The [percentage calculator](/math/percentage/) answers "what is X% of Y", "X is what percent of Y" and the reverse. For price rises, salary changes or test scores, use [percentage change](/math/percentage-change/), and for lab work [percent error](/math/percent-error/). Other everyday helpers include [ratios](/math/ratio/), [fractions](/math/fraction-calculator/), [fraction to decimal](/math/fraction-to-decimal/), [averages](/math/average/), [weighted averages](/math/weighted-average/) for grades, and [scientific notation](/math/scientific-notation/) and [significant figures](/math/significant-figures/) for science homework.' },
      { h: 'Geometry: area, volume and triangles', p: 'Area tools cover the [circle](/math/circle/), [rectangle](/math/rectangle/), [triangle](/math/triangle-area/), [trapezoid](/math/trapezoid-area/), [ellipse](/math/ellipse/) and regular [polygons](/math/polygon/). For volume there are the [cylinder](/math/cylinder-volume/), [sphere](/math/sphere/), [cone](/math/cone/), [pyramid](/math/pyramid-volume/), [frustum](/math/frustum-volume/), [capsule](/math/capsule/) and [torus](/math/torus/). Triangle problems are solved with the [Pythagorean theorem](/math/pythagorean-theorem/), [right triangle trigonometry](/math/right-triangle-trig/), the [law of sines](/math/law-of-sines/), the [law of cosines](/math/law-of-cosines/) and the [SSS triangle calculator](/math/sss-triangle/).' },
      { h: 'Algebra and higher maths', p: 'Solve a [quadratic equation](/math/quadratic-equation/) with real or complex roots, a [cubic equation](/math/cubic-equation/), or a [2 by 2](/math/system-of-equations/) and [3 by 3 system](/math/system-of-3-equations/) of linear equations. The [matrix determinant and inverse](/math/matrix-determinant/) calculator handles 3 by 3 matrices step by step. For sequences and growth there are [arithmetic](/math/arithmetic-sequence/) and [geometric sequences](/math/geometric-sequence/), [exponents](/math/exponent/) and [logarithms](/math/logarithm/). Engineers will also use [linear interpolation](/math/linear-interpolation/) to read between table values, plus [vectors](/math/vector/) and [complex numbers](/math/complex-number/).' },
    ],
    faq: [
      { q: 'Do the geometry calculators accept different units?', a: 'Yes. You can switch between metric and imperial units, and the area or volume is shown in matching square or cubic units.' },
      { q: 'Can the equation solvers give complex roots?', a: 'Yes. The quadratic and cubic solvers show complex roots in a + bi form when the discriminant is negative.' },
    ],
  },
  statistics: {
    about: [
      { h: 'Describing your data', p: 'Paste a list of numbers into the [mean, median and mode calculator](/statistics/mean-median-mode/) for the basic summary, then use [standard deviation](/statistics/standard-deviation/) and [quartiles](/statistics/quartiles/) to see the spread. The [coefficient of variation](/statistics/coefficient-of-variation/) compares spread between data sets with different units, and the [geometric mean](/statistics/geometric-mean/) is the right average for growth rates. To see how unusual a single value is, convert it to a [z-score](/statistics/z-score/) or check it against the [empirical rule](/statistics/empirical-rule/).' },
      { h: 'Probability and distributions', p: 'For counting problems, start with [combinations](/statistics/combinations/) and [permutations](/statistics/permutations/). Then choose the distribution that matches your situation: [binomial](/statistics/binomial-probability/) for a fixed number of yes or no trials, [Poisson](/statistics/poisson-probability/) for events per hour or per metre, [normal](/statistics/normal-distribution/) for measurements, [exponential](/statistics/exponential-distribution/) for waiting times, and [hypergeometric](/statistics/hypergeometric-distribution/) for sampling without replacement. [Bayes\' theorem](/statistics/bayes-theorem/) updates a probability with new evidence, which is how medical test results are interpreted.' },
      { h: 'Testing and quality', p: 'Before a survey, use the [sample size calculator](/statistics/sample-size/); after it, report the [margin of error](/statistics/margin-of-error/) and a [confidence interval](/statistics/confidence-interval/). To compare groups, run a [one-sample](/statistics/one-sample-t-test/) or [two-sample t-test](/statistics/two-sample-t-test/) and read the [p-value](/statistics/p-value/). In manufacturing, [process capability](/statistics/process-capability/), [six sigma](/statistics/six-sigma/) and [control charts](/statistics/control-chart/) show whether a process can hold its tolerance, and [measurement uncertainty](/statistics/measurement-uncertainty/) combines error sources for calibration work.' },
    ],
    faq: [
      { q: 'What does a p-value of 0.05 mean?', a: 'If there were really no effect, a result at least as extreme as yours would happen about 5% of the time. It does not mean there is a 95% chance your hypothesis is true.' },
      { q: 'Which distribution should I use?', a: 'Binomial for a count of successes in n trials, Poisson for a count of events in a time or space interval, normal for continuous measurements, and exponential for the time between random events.' },
    ],
  },
  conversion: {
    about: [
      { h: 'Everyday and travel conversions', p: 'Quick one-way converters cover the questions people search most: [cm to inches](/conversion/cm-to-inches/), [feet to metres](/conversion/feet-to-meters/), [kg to lb](/conversion/kg-to-lb/), [miles to km](/conversion/miles-to-km/), [°F to °C](/conversion/fahrenheit-to-celsius/), [gallons to litres](/conversion/gallons-to-liters/) and [mph to km/h](/conversion/mph-to-kmh/). Each shows the exact factor, a worked example and a table of common values, so you can convert in your head next time. Note that US and UK (imperial) gallons differ by about 20%, which matters for fuel economy and recipes.' },
      { h: 'Indian land and number units', p: 'Land in India is still measured in local units that vary by state. The [gaj to sq ft](/conversion/gaj-to-sq-ft/), [guntha to sq ft](/conversion/guntha-to-sq-ft/) and [cent to sq ft](/conversion/cent-to-sq-ft/) converters use the standard values, and the [acres to hectares](/conversion/acres-to-hectares/) and [area converter](/conversion/area-converter/) handle everything else. Always check the local value on your property documents, because a bigha or a gaj can differ between regions. The [number to million](/conversion/number-to-million/) converter switches between lakh and crore and the international million and billion system.' },
      { h: 'Engineering units', p: 'For plant and design work there are full converters for [pressure](/conversion/pressure-converter/) (bar, psi, kPa, mmH₂O, inHg), [flow rate](/conversion/flow-rate-converter/), [power](/conversion/power-converter/), [energy](/conversion/energy-converter/), [torque](/conversion/torque-converter/) and [temperature](/conversion/temperature-converter/), plus shortcuts like [psi to bar](/conversion/psi-to-bar/) and [kW to hp](/conversion/kw-to-hp/). All factors follow the SI definitions, for example 1 psi = 6,894.757 Pa and 1 inch = 25.4 mm exactly.' },
    ],
    faq: [
      { q: 'Why does horsepower give two different answers?', a: 'Mechanical horsepower (hp) is 745.7 W, while metric horsepower (PS) is 735.5 W. Motor nameplates in India and Europe usually use kW, and older equipment may use either hp.' },
      { q: 'How big is a gaj?', a: 'In most of North India 1 gaj (square yard) is 9 sq ft, or 0.836 m². Some local land records use slightly different values, so check your documents.' },
    ],
  },
  finance: {
    about: [
      { h: 'Loans and EMIs', p: 'The [EMI calculator](/finance/emi/) shows your monthly instalment, total interest and a year-by-year schedule for a home, car or personal loan. To see how much a prepayment saves, compare the result with the [loan payment calculator](/finance/loan-payment/), and for credit cards use the [credit card payoff calculator](/finance/credit-card-payoff/), which shows how long the minimum payment really takes. Lenders also look at your [debt to income ratio](/finance/debt-to-income/); most banks prefer total EMIs below about 40% to 50% of take-home pay.' },
      { h: 'Saving and investing in India', p: 'For market investments, plan a monthly [SIP](/finance/sip/), a [step-up SIP](/finance/step-up-sip/) that grows with your salary, or a one-time [lumpsum](/finance/lumpsum/), and compare funds with [CAGR](/finance/cagr/). Fixed-income options have their own calculators: [FD](/finance/fd/), [RD](/finance/rd/), [PPF](/finance/ppf/), [Sukanya Samriddhi](/finance/sukanya-samriddhi/), [NSC](/finance/nsc/), [KVP](/finance/kvp/), [Post Office MIS](/finance/post-office-mis/) and [SCSS](/finance/scss/). For retirement, combine [EPF](/finance/epf/), [NPS](/finance/nps/) and a [retirement corpus](/finance/retirement-corpus/) estimate, then plan withdrawals with an [SWP](/finance/swp/). Always check current interest rates with the bank or post office, because government scheme rates are revised every quarter.' },
      { h: 'Tax, salary and business', p: 'Salaried users can estimate [income tax](/finance/income-tax-india/) under the old and new regimes, the [HRA exemption](/finance/hra-exemption/), [gratuity](/finance/gratuity/) and a [salary increase](/finance/salary-increase/). Business owners can work out [GST](/finance/gst/), [profit margin](/finance/profit-margin/), [break-even](/finance/break-even/), [ROI](/finance/roi/), [payback period](/finance/payback-period/) and marketing numbers like [ROAS](/finance/roas/) and [customer lifetime value](/finance/customer-lifetime-value/). Finally, the [inflation](/finance/inflation/) and [real return](/finance/real-return/) calculators show what your money will actually buy in the future.' },
    ],
    faq: [
      { q: 'Why does my bank\'s EMI differ slightly from the calculator?', a: 'Banks may charge interest from the disbursement date, round the EMI, or add processing fees and insurance. The calculator uses the standard reducing balance formula.' },
      { q: 'What is the difference between CAGR and absolute return?', a: 'Absolute return is the total gain as a percentage. CAGR spreads that gain evenly over the years, so you can compare investments held for different lengths of time.' },
    ],
  },
  health: {
    groups: [
      { name: 'Body weight & composition', ids: ['bmi', 'ideal-weight', 'body-fat', 'lean-body-mass', 'waist-to-height', 'waist-to-hip', 'body-surface-area', 'weight-loss-time'] },
      { name: 'Calories, diet & nutrition', ids: ['bmr', 'macros', 'protein-intake', 'water-intake', 'calories-burned', 'alcohol-units'] },
      { name: 'Fitness & heart', ids: ['heart-rate-zones', 'vo2-max', 'steps-to-distance', 'mean-arterial-pressure'] },
      { name: 'Clinical calculators', ids: ['egfr', 'creatinine-clearance', 'qtc', 'ldl-cholesterol', 'iv-drip-rate', 'pack-years', 'pregnancy-weight-gain'] },
    ],
    about: [
      { h: 'Weight and body composition', p: 'The [BMI calculator](/health/bmi/) is a quick screening tool, but it cannot tell muscle from fat. For a fuller picture, add the [waist to height ratio](/health/waist-to-height/), which is a better guide to health risk from belly fat, and estimate [body fat](/health/body-fat/) with the US Navy tape method. The [ideal weight calculator](/health/ideal-weight/) shows the range given by the common formulas, and [lean body mass](/health/lean-body-mass/) is useful for setting protein targets.' },
      { h: 'Calories, food and fitness', p: 'Your [BMR](/health/bmr/) is the energy you burn at rest. Multiply it by your activity level to get daily calories, then split them with the [macro calculator](/health/macros/). The [weight loss time calculator](/health/weight-loss-time/) shows how long a goal takes at a safe deficit. For training, set [heart rate zones](/health/heart-rate-zones/), estimate [VO₂ max](/health/vo2-max/) and convert [steps to distance](/health/steps-to-distance/).' },
      { h: 'Clinical calculators for professionals', p: 'Doctors, nurses and pharmacists use the [eGFR](/health/egfr/) (CKD-EPI 2021) and [creatinine clearance](/health/creatinine-clearance/) (Cockcroft-Gault) calculators for kidney function and drug dosing, [QTc](/health/qtc/) for ECG intervals, the [IV drip rate](/health/iv-drip-rate/) for infusions and [LDL cholesterol](/health/ldl-cholesterol/) from a lipid panel. These tools follow the published formulas, but results must always be read by a qualified professional together with the full clinical picture.' },
    ],
    faq: [
      { q: 'Is BMI accurate for athletes?', a: 'Not very. Muscular people can have a BMI in the overweight range with low body fat. Use body fat percentage or waist to height ratio alongside BMI.' },
      { q: 'Which BMI cut-offs are used for Asian adults?', a: 'Many Asian health bodies, including in India, use lower cut-offs: overweight from 23 and obesity from 25 (or 27.5 in some guidelines), because health risks rise at lower BMI.' },
    ],
  },
  construction: {
    groups: [
      { name: 'Concrete & masonry', ids: ['concrete-slab', 'concrete-column', 'concrete-mix', 'mortar-mix', 'brick-calculator', 'rebar-weight'] },
      { name: 'Earthwork & landscaping', ids: ['excavation', 'gravel', 'fence', 'rectangular-tank'] },
      { name: 'Interiors & finishes', ids: ['paint-calculator', 'tile-calculator', 'flooring', 'drywall', 'wallpaper', 'square-footage'] },
      { name: 'Roofs, stairs, timber & steel', ids: ['roof-pitch', 'stairs', 'board-feet', 'steel-plate-weight'] },
    ],
    about: [
      { h: 'Estimate materials before you buy', p: 'Running out of material halfway through a job costs more than ordering a little extra. The [concrete slab](/construction/concrete-slab/) and [concrete column](/construction/concrete-column/) calculators give volume in m³ and cubic yards, and the [concrete mix calculator](/construction/concrete-mix/) splits it into cement bags, sand and aggregate for M15, M20 or M25 mixes. For walls, the [brick calculator](/construction/brick-calculator/) counts bricks and the [mortar mix calculator](/construction/mortar-mix/) gives the cement and sand. [Rebar weight](/construction/rebar-weight/) uses the D²/162 rule for steel bars.' },
      { h: 'Finishing work', p: 'For interiors, the [paint calculator](/construction/paint-calculator/) subtracts doors and windows and allows for two coats, the [tile calculator](/construction/tile-calculator/) and [flooring calculator](/construction/flooring/) add a wastage allowance for cuts, and the [drywall](/construction/drywall/) and [wallpaper](/construction/wallpaper/) calculators count sheets and rolls. Start with the [square footage calculator](/construction/square-footage/) if the room is L-shaped or irregular.' },
      { h: 'Wastage and rules of thumb', p: 'Professional estimators add wastage: about 5% for concrete, 5% to 10% for bricks and tiles laid straight, and 10% to 15% for tiles laid diagonally or in rooms with many corners. Dry mix volume for concrete is about 1.54 times the wet volume because the materials shrink when water is added. The calculators include these allowances where they apply, and say so in the results.' },
    ],
    faq: [
      { q: 'How many cement bags are in 1 m³ of M20 concrete?', a: 'With a nominal 1 : 1.5 : 3 mix, about 8 bags of 50 kg. The concrete mix calculator works this out for any mix ratio and volume.' },
      { q: 'Do the calculators work in feet and metres?', a: 'Yes. Enter dimensions in feet, inches, metres or mm and the results come out in both metric and imperial units where useful.' },
      { q: 'How much extra material should I order?', a: 'Usually 5% to 10%, and up to 15% for diagonal tiling or complex shapes. The calculators let you set your own wastage percentage.' },
    ],
  },
  biology: {
    groups: [
      { name: 'DNA, RNA & protein', ids: ['dna-concentration', 'dna-copy-number', 'protein-concentration-a280', 'protein-molecular-weight', 'gc-content', 'primer-tm'] },
      { name: 'Molecular biology methods', ids: ['pcr-amplification', 'ligation-ratio', 'serial-dilution', 'centrifuge-rcf'] },
      { name: 'Cell culture & microbiology', ids: ['hemocytometer', 'cell-doubling-time', 'bacterial-growth', 'specific-growth-rate'] },
      { name: 'Microscopy', ids: ['magnification', 'field-of-view'] },
      { name: 'Populations, genetics & plants', ids: ['exponential-population-growth', 'logistic-growth', 'hardy-weinberg', 'water-potential'] },
    ],
    about: [
      { h: 'Calculators for the molecular biology bench', p: 'Check nucleic acid yield and purity with the [DNA concentration calculator](/biology/dna-concentration/), then convert ng to copies for qPCR standards with the [DNA copy number calculator](/biology/dna-copy-number/). Design primers with the [primer Tm](/biology/primer-tm/) and [GC content](/biology/gc-content/) calculators, set up a cloning reaction with the [ligation ratio calculator](/biology/ligation-ratio/), and convert rpm to g force with the [centrifuge RCF calculator](/biology/centrifuge-rcf/), because protocols are written in × g but most centrifuges are set in rpm.' },
      { h: 'Cell culture and microbiology', p: 'Count cells with the [hemocytometer calculator](/biology/hemocytometer/), plan [serial dilutions](/biology/serial-dilution/) for plating, and measure growth with the [cell doubling time](/biology/cell-doubling-time/), [bacterial growth](/biology/bacterial-growth/) and [specific growth rate](/biology/specific-growth-rate/) calculators. Under ideal conditions E. coli can double in about 20 minutes, while most mammalian cell lines take 20 to 40 hours.' },
      { h: 'Ecology and genetics', p: 'For population biology, compare [exponential growth](/biology/exponential-population-growth/) with [logistic growth](/biology/logistic-growth/), which levels off at the carrying capacity. The [Hardy-Weinberg calculator](/biology/hardy-weinberg/) gives allele and genotype frequencies and tests whether a population is in equilibrium, and the [water potential calculator](/biology/water-potential/) explains osmosis in plant cells.' },
    ],
    faq: [
      { q: 'How do I convert rpm to g force?', a: 'RCF = 1.118 × 10⁻⁵ × r × rpm², where r is the rotor radius in cm. For example, 10,000 rpm on a 10 cm rotor is about 11,180 × g.' },
      { q: 'What is a good 260/280 ratio for DNA?', a: 'About 1.8 for pure DNA and about 2.0 for pure RNA. Lower values suggest protein or phenol contamination.' },
      { q: 'Are these calculators suitable for lab protocols?', a: 'Yes, they use standard formulas and show the working, but always check results against your kit or instrument manual.' },
    ],
  },
  'everyday-life': {
    groups: [
      { name: 'Dates & time', ids: ['age-calculator', 'days-between-dates', 'date-plus-days', 'days-until', 'time-duration', 'hours-worked', 'sleep-calculator', 'commute-time'] },
      { name: 'Money at home', ids: ['electricity-cost', 'fuel-cost', 'fuel-economy', 'unit-price', 'cost-per-use', 'habit-cost', 'rent-split', 'tip-calculator'] },
      { name: 'Home & devices', ids: ['inverter-battery-backup', 'tv-size'] },
      { name: 'Study & reading', ids: ['cgpa-to-percentage', 'grade-needed', 'reading-time', 'typing-speed'] },
    ],
    about: [
      { h: 'Dates, time and planning', p: 'The [age calculator](/everyday-life/age-calculator/) gives your exact age in years, months and days, which forms often ask for. Count the [days between two dates](/everyday-life/days-between-dates/), find the date [a number of days from today](/everyday-life/date-plus-days/), or count down the [days until an event](/everyday-life/days-until/). For work, add up a timesheet with the [hours worked calculator](/everyday-life/hours-worked/), and for rest, the [sleep calculator](/everyday-life/sleep-calculator/) suggests bedtimes that end on a full sleep cycle.' },
      { h: 'Household bills and running costs', p: 'Find what an appliance costs to run with the [electricity cost calculator](/everyday-life/electricity-cost/), or what a trip costs with the [fuel cost calculator](/everyday-life/fuel-cost/). When shopping, the [unit price calculator](/everyday-life/unit-price/) shows which pack size is really cheaper, and the [cost per use calculator](/everyday-life/cost-per-use/) helps decide whether an expensive item is worth it. For power cuts, the [inverter battery backup calculator](/everyday-life/inverter-battery-backup/) estimates how long your inverter will last.' },
      { h: 'Students', p: 'Convert a [CGPA to percentage](/everyday-life/cgpa-to-percentage/) using the CBSE (× 9.5) or university formula, work out the [grade you need](/everyday-life/grade-needed/) on a final exam, and estimate [reading time](/everyday-life/reading-time/) for an assignment. Each calculator explains the formula so you can check results by hand.' },
    ],
    faq: [
      { q: 'Does the age calculator count leap years?', a: 'Yes. It uses the real calendar, so leap days and months of different lengths are counted correctly.' },
      { q: 'How do I find the running cost of an appliance?', a: 'Multiply its power in kW by the hours used and by your tariff per kWh. A 1.5 kW AC running 8 hours at ₹8 per unit costs about ₹96 a day.' },
      { q: 'Is the CGPA to percentage formula the same for every university?', a: 'No. CBSE uses CGPA × 9.5, but many universities publish their own formula. Check your marksheet or university rules.' },
    ],
  },
  food: {
    groups: [
      { name: 'Recipe scaling & conversion', ids: ['recipe-scaler', 'grams-to-cups', 'cooking-converter', 'butter-converter', 'liquid-weight', 'oven-temperature', 'sugar-to-honey', 'yeast-converter', 'cake-pan'] },
      { name: 'Baking & ratios', ids: ['bakers-percentage', 'rice-water', 'coffee-ratio', 'brine'] },
      { name: 'Party & holiday planning', ids: ['meat-per-person', 'party-drinks', 'pizza-size', 'turkey-cooking-time', 'turkey-thawing'] },
      { name: 'Nutrition & food cost', ids: ['calories-from-macros', 'food-cost'] },
    ],
    about: [
      { h: 'Scale and convert recipes', p: 'The [recipe scaler](/food/recipe-scaler/) multiplies every ingredient for more or fewer servings. When a recipe uses cups but you weigh in grams, use [grams to cups](/food/grams-to-cups/), which uses the real density of each ingredient: a cup of flour weighs about 120 g, but a cup of sugar about 200 g. The [oven temperature converter](/food/oven-temperature/) switches between °C, °F and gas marks, and the [cake pan converter](/food/cake-pan/) adjusts a recipe for a different tin.' },
      { h: 'Ratios that give better results', p: 'Bakers write bread recipes as [baker\'s percentages](/food/bakers-percentage/), with flour as 100%, which makes any recipe easy to scale. The [rice to water calculator](/food/rice-water/) gives the ratio for basmati, brown or sushi rice, and the [coffee ratio calculator](/food/coffee-ratio/) sets grams of coffee per ml of water for pour-over, French press or espresso. The [brine calculator](/food/brine/) gives salt per litre for pickling and wet brines.' },
      { h: 'Planning food for a group', p: 'For parties, estimate [meat per person](/food/meat-per-person/), [drinks](/food/party-drinks/) and [pizza](/food/pizza-size/) so you neither run short nor waste food. Restaurant owners can set menu prices with the [food cost calculator](/food/food-cost/); many aim for a food cost of 28% to 35% of the menu price.' },
    ],
    faq: [
      { q: 'Why does a cup of flour weigh less than a cup of sugar?', a: 'Flour is lighter and full of air. A cup of plain flour is about 120 g, while a cup of granulated sugar is about 200 g. That is why weighing gives more consistent results.' },
      { q: 'Are cups the same in every country?', a: 'No. A US cup is 236.6 ml, while the metric cup used in Australia and many Indian recipes is 250 ml, about 6% more. For small batches the difference rarely matters; for baking, weighing in grams is safest.' },
      { q: 'How much rice should I cook per person?', a: 'About 75 to 90 g of uncooked rice per adult as a side, or 100 g or more as a main dish.' },
    ],
  },
  sports: {
    groups: [
      { name: 'Cricket', ids: ['cricket-run-rate', 'required-run-rate', 'net-run-rate', 'cricket-batting', 'bowling-economy'] },
      { name: 'Running & endurance', ids: ['pace-calculator', 'pace-speed-converter', 'race-time-predictor', 'running-cadence', 'swim-pace', 'cycling-gear-speed'] },
      { name: 'Strength & fitness', ids: ['one-rep-max', 'jump-height'] },
      { name: 'Other sports', ids: ['baseball-batting', 'baseball-era', 'effective-field-goal', 'football-points', 'golf-handicap', 'bowling-handicap', 'win-percentage'] },
    ],
    about: [
      { h: 'Cricket statistics', p: 'Work out the current and [required run rate](/sports/required-run-rate/) during a chase, a team\'s [net run rate](/sports/net-run-rate/) for the points table, and player stats like [batting average and strike rate](/sports/cricket-batting/) and [bowling economy](/sports/bowling-economy/). The net run rate calculator follows the ICC method, where a team that is bowled out is counted as having faced its full quota of overs.' },
      { h: 'Running, cycling and swimming', p: 'The [pace calculator](/sports/pace-calculator/) finds your pace, time or distance for any race, and the [race time predictor](/sports/race-time-predictor/) uses the Riegel formula to estimate a marathon time from a shorter race. Convert between min/km and km/h with the [pace to speed converter](/sports/pace-speed-converter/), check your [running cadence](/sports/running-cadence/), and plan pool sessions with the [swim pace calculator](/sports/swim-pace/).' },
      { h: 'Strength and team sports', p: 'Estimate your [one rep max](/sports/one-rep-max/) from a lighter set without the risk of a true maximum lift, and measure explosive power with the [jump height calculator](/sports/jump-height/). For other sports there are [baseball batting average](/sports/baseball-batting/) and [ERA](/sports/baseball-era/), basketball [effective field goal percentage](/sports/effective-field-goal/), [golf handicap](/sports/golf-handicap/) and [win percentage](/sports/win-percentage/).' },
    ],
    faq: [
      { q: 'How is net run rate calculated?', a: 'Runs scored per over across the tournament minus runs conceded per over. If a team is all out, its full quota of overs is used, not the overs actually faced.' },
      { q: 'How accurate is the race time predictor?', a: 'It is a good guide for races up to about four times the distance you entered, if you have trained for the longer distance. It tends to be optimistic for a first marathon.' },
      { q: 'Is a one rep max estimate safe to train with?', a: 'Use it to set training loads, usually 60% to 85% of the estimate. Estimates are most accurate from sets of 3 to 10 reps.' },
    ],
  },
  other: {
    groups: [
      { name: 'Tech & digital', ids: ['download-time', 'data-storage-converter', 'video-file-size', 'screen-ppi', 'print-size-dpi', 'aspect-ratio', 'password-strength', 'battery-life', 'paper-weight-gsm'] },
      { name: 'Home & utilities', ids: ['lpg-cylinder', 'water-heater-time', 'aquarium-volume'] },
      { name: 'Pets', ids: ['dog-age', 'cat-age', 'dog-food-calories'] },
      { name: 'Pregnancy & family', ids: ['due-date', 'ovulation'] },
      { name: 'School', ids: ['grade-percentage'] },
    ],
    about: [
      { h: 'Tech and digital tools', p: 'The [download time calculator](/other/download-time/) shows how long a file takes at your internet speed, remembering that speeds are sold in megabits (Mbps) while files are measured in megabytes (MB), a factor of 8. Convert between [data storage units](/other/data-storage-converter/), estimate [video file size](/other/video-file-size/) from bitrate, and check [screen PPI](/other/screen-ppi/) or the largest sharp [print size](/other/print-size-dpi/) for a photo. The [password strength checker](/other/password-strength/) estimates how long a password would take to guess.' },
      { h: 'Home and pets', p: 'Estimate how long an [LPG cylinder](/other/lpg-cylinder/) will last, how long a [water heater](/other/water-heater-time/) takes to heat a tank, or the [volume of an aquarium](/other/aquarium-volume/). Pet owners can convert [dog years](/other/dog-age/) and [cat years](/other/cat-age/) into human years with newer, research-based formulas rather than the old "× 7" rule, and set daily [dog food calories](/other/dog-food-calories/).' },
      { h: 'Family planning', p: 'The [due date calculator](/other/due-date/) estimates the delivery date from the last period, conception or IVF transfer date, and the [ovulation calculator](/other/ovulation/) shows the fertile window. These are estimates only; always follow the dates given by your doctor or midwife.' },
    ],
    faq: [
      { q: 'Why does my download take longer than the calculator says?', a: 'The calculator uses your full line speed. Real downloads are slower because of Wi-Fi, server limits and protocol overhead, often by 10% to 30%.' },
      { q: 'Is one dog year really seven human years?', a: 'No. Dogs age fastest in their first year or two, then more slowly. The dog age calculator uses a DNA-based formula (16 × ln(dog age) + 31) and shows the old × 7 figure next to it for comparison.' },
      { q: 'Which LPG cylinder size does the calculator use?', a: 'It starts with the 14.2 kg domestic cylinder, but you can enter any size, such as 5 kg or a 19 kg commercial cylinder.' },
    ],
  },
};
