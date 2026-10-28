import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from page import page
D = '2026-10-27'

def egfr(cr, age, fem):
    k = 0.7 if fem else 0.9; a = -0.241 if fem else -0.302
    return 142 * min(cr/k, 1)**a * max(cr/k, 1)**-1.2 * 0.9938**age * (1.012 if fem else 1)

page('health', 'egfr', f'''
title: eGFR Calculator (CKD-EPI 2021)
description: Estimate glomerular filtration rate (eGFR) from serum creatinine, age and sex using the race-free CKD-EPI 2021 equation, with CKD stages.
category: health
keywords: [egfr calculator, ckd-epi 2021, glomerular filtration rate, kidney function calculator, creatinine egfr, ckd stage, gfr calculator]
updated: {D}
variables:
  - {{ id: cr, label: Serum creatinine, suffix: mg/dL, default: 1.0, min: 0.05, help: 'To convert from µmol/L, divide by 88.4.' }}
  - {{ id: age, label: Age, suffix: years, default: 50, min: 18, max: 110 }}
  - id: s
    label: Sex
    default: 0
    options:
      - {{ label: Male, value: 0 }}
      - {{ label: Female, value: 1 }}
  - id: gfr
    label: eGFR
    suffix: mL/min/1.73 m²
    min: 0
    decimals: 0
    bands:
      - {{ max: 15, label: G5 Kidney failure, color: '#dc2626' }}
      - {{ max: 30, label: G4 Severely decreased, color: '#ea580c' }}
      - {{ max: 45, label: G3b Moderately–severely decreased, color: '#f59e0b' }}
      - {{ max: 60, label: G3a Mildly–moderately decreased, color: '#eab308' }}
      - {{ max: 90, label: G2 Mildly decreased, color: '#84cc16' }}
      - {{ max: 1000, label: G1 Normal or high, color: '#16a34a' }}
equations:
  - gfr = 142 * min(cr / (0.9 - 0.2*s), 1)^(-0.302 + 0.061*s) * max(cr / (0.9 - 0.2*s), 1)^(-1.2) * 0.9938^age * (1 + 0.012*s)
faq:
  - q: What is a normal eGFR?
    a: 90 or above is normal. Values of 60–89 can be normal in older adults if there are no other signs of kidney damage.
  - q: Why does the 2021 equation not use race?
    a: The 2021 CKD-EPI equation was refitted without a race coefficient, following recommendations from US kidney organisations, to avoid race-based adjustments.
  - q: How do I convert µmol/L to mg/dL?
    a: Divide by 88.4. A creatinine of 88 µmol/L is about 1.0 mg/dL.
  - q: Is eGFR the same as creatinine clearance?
    a: No. eGFR is normalised to 1.73 m² of body surface area and is used for CKD staging. Creatinine clearance (Cockcroft–Gault) is often used for drug dosing.
related: [health/creatinine-clearance, health/body-surface-area, health/bmi, chemistry/osmotic-pressure]
''', f'''
## How to use this calculator

Enter **serum creatinine** in mg/dL, **age** and **sex**. The result is the estimated GFR in mL/min per 1.73 m², with the matching CKD stage.

This tool is for education. Diagnosis and treatment decisions need a clinician, repeated tests and other markers such as urine albumin.

## The CKD-EPI 2021 equation

<p class="formula">eGFR = 142 × min(Scr/κ, 1)<sup>α</sup> × max(Scr/κ, 1)<sup>−1.200</sup> × 0.9938<sup>age</sup> × 1.012 [female]</p>

| | Female | Male |
|---|---|---|
| κ | 0.7 | 0.9 |
| α | −0.241 | −0.302 |

## eGFR by creatinine and age

| Creatinine | Male, 40 | Male, 70 | Female, 40 | Female, 70 |
|---|---|---|---|---|
''' + ''.join(f"| {c} mg/dL | {egfr(c,40,0):.0f} | {egfr(c,70,0):.0f} | {egfr(c,40,1):.0f} | {egfr(c,70,1):.0f} |\n" for c in [0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0]) + '''
## CKD stages (KDIGO)

| Stage | eGFR | Description |
|---|---|---|
| G1 | 90+ | Normal or high |
| G2 | 60–89 | Mildly decreased |
| G3a | 45–59 | Mildly to moderately decreased |
| G3b | 30–44 | Moderately to severely decreased |
| G4 | 15–29 | Severely decreased |
| G5 | under 15 | Kidney failure |

Chronic kidney disease is diagnosed when eGFR stays below 60 for more than 3 months, or when there are other signs of kidney damage.

## When eGFR is less reliable

- Very high or low muscle mass (bodybuilders, amputees, frail elderly).
- Acute kidney injury, when creatinine is changing quickly.
- Pregnancy and children (use paediatric equations).
- High meat intake or creatine supplements shortly before the test.

Cystatin C based equations can help in these situations.
''')

page('health', 'qtc', f'''
title: QTc Calculator (Corrected QT Interval)
description: Calculate the corrected QT interval (QTc) from QT and heart rate using the Bazett, Fridericia, Framingham and Hodges formulas.
category: health
keywords: [qtc calculator, corrected qt interval, bazett formula, fridericia formula, qt prolongation, ecg qtc, framingham qtc]
updated: {D}
variables:
  - {{ id: qt, label: QT interval, suffix: ms, default: 400, min: 100, max: 800 }}
  - {{ id: hr, label: Heart rate, suffix: bpm, default: 75, min: 20, max: 250 }}
  - {{ id: rr, label: RR interval, suffix: s, min: 0, decimals: 3 }}
  - {{ id: baz, label: QTc — Bazett, suffix: ms, min: 0, decimals: 0 }}
  - {{ id: fri, label: QTc — Fridericia, suffix: ms, min: 0, decimals: 0 }}
  - {{ id: fra, label: QTc — Framingham, suffix: ms, min: 0, decimals: 0 }}
  - {{ id: hod, label: QTc — Hodges, suffix: ms, min: 0, decimals: 0 }}
equations:
  - rr = 60 / hr
  - baz = qt / sqrt(rr)
  - fri = qt / rr^(1/3)
  - fra = qt + 154 * (1 - rr)
  - hod = qt + 1.75 * (hr - 60)
faq:
  - q: What is a normal QTc?
    a: Commonly under about 450 ms in men and 460–470 ms in women. Above 500 ms is associated with a higher risk of dangerous arrhythmias.
  - q: Which QTc formula is best?
    a: Bazett is the most widely used but over-corrects at high heart rates and under-corrects at low ones. Fridericia and Framingham are often preferred when the heart rate is outside 60–100 bpm.
  - q: Why correct the QT interval?
    a: QT naturally shortens as heart rate rises. Correcting it to a standard heart rate of 60 bpm lets measurements be compared.
  - q: What can prolong the QT interval?
    a: Some medicines (certain antibiotics, antiarrhythmics, antipsychotics and antiemetics), low potassium or magnesium, and inherited long-QT syndromes.
related: [health/heart-rate-zones, health/mean-arterial-pressure, health/bmi, health/creatinine-clearance]
''', '''
## How to use this calculator

Enter the **QT interval** in milliseconds and the **heart rate** in beats per minute. The calculator shows the RR interval and the QTc by four common formulas.

This tool is for education and does not replace interpretation of an ECG by a qualified clinician.

## The formulas

| Formula | QTc |
|---|---|
| Bazett (1920) | QT ÷ √RR |
| Fridericia (1920) | QT ÷ ∛RR |
| Framingham (1992) | QT + 154 × (1 − RR) |
| Hodges (1983) | QT + 1.75 × (HR − 60) |

QT is in ms and RR in seconds (RR = 60 ÷ heart rate).

## How the formulas compare (QT 400 ms)

| Heart rate | Bazett | Fridericia | Framingham | Hodges |
|---|---|---|---|---|
''' + ''.join(f"| {h} bpm | {400/math.sqrt(60/h):.0f} | {400/(60/h)**(1/3):.0f} | {400+154*(1-60/h):.0f} | {400+1.75*(h-60):.0f} |\n" for h in [50, 60, 75, 90, 110, 130]) + '''
At 60 bpm all formulas agree. At faster rates Bazett gives noticeably higher values.

## Interpreting QTc (adults)

| QTc | Men | Women |
|---|---|---|
| Normal | under 450 ms | under 460 ms |
| Borderline | 450–470 ms | 460–480 ms |
| Prolonged | over 470 ms | over 480 ms |
| High risk | over 500 ms | over 500 ms |

Thresholds vary between guidelines. A short QTc (under about 350 ms) can also be significant.

## Measuring QT

Measure from the start of the QRS complex to the end of the T wave, usually in lead II or V5, and average over 3–5 beats. In atrial fibrillation, average several RR intervals.
''')

page('health', 'iv-drip-rate', f'''
title: IV Drip Rate Calculator (gtt/min and mL/h)
description: Calculate IV infusion rates in drops per minute and mL per hour from volume, time and drip factor — for nursing and clinical practice.
category: health
keywords: [iv drip rate calculator, drops per minute, gtt/min, infusion rate calculator, ml per hour, drip factor, iv flow rate, nursing calculations]
updated: {D}
variables:
  - {{ id: v, label: Volume to infuse, suffix: mL, default: 1000, min: 0 }}
  - {{ id: t, label: Infusion time, suffix: hours, default: 8, min: 0.01 }}
  - id: df
    label: Drip factor
    default: 20
    options:
      - {{ label: 10 gtt/mL (macrodrip), value: 10 }}
      - {{ label: 15 gtt/mL (macrodrip), value: 15 }}
      - {{ label: 20 gtt/mL (macrodrip), value: 20 }}
      - {{ label: 60 gtt/mL (microdrip), value: 60 }}
  - {{ id: mlh, label: Flow rate, suffix: mL/h, min: 0, decimals: 1 }}
  - {{ id: gtt, label: Drip rate, suffix: drops/min, min: 0, decimals: 0 }}
equations:
  - mlh = v / t
  - gtt = v * df / (t * 60)
faq:
  - q: How do I calculate drops per minute?
    a: Drops per minute = volume (mL) × drip factor (gtt/mL) ÷ time (minutes). 1,000 mL over 8 hours with a 20 gtt/mL set is about 42 drops per minute.
  - q: What is a drip factor?
    a: The number of drops that make 1 mL with a particular IV set. It is printed on the packaging — commonly 10, 15 or 20 for macrodrip and 60 for microdrip sets.
  - q: Why is microdrip mL/h the same as drops per minute?
    a: With a 60 gtt/mL set, drops per minute equals mL per hour, because there are 60 minutes in an hour.
  - q: Should I round drops per minute?
    a: Yes, round to the nearest whole drop, as you cannot count part of a drop.
related: [health/body-surface-area, health/water-intake, health/creatinine-clearance, chemistry/dilution]
''', '''
## How to use this calculator

Enter the **volume** to infuse, the **time** in hours and the **drip factor** of your IV set. You get the flow rate in mL/h (for infusion pumps) and the drip rate in drops per minute (for gravity sets).

This tool supports calculation practice. Always follow the prescription, local protocols and independent double-checks.

## The formulas

<p class="formula">mL/h = volume ÷ hours &nbsp;·&nbsp; gtt/min = volume × drip factor ÷ minutes</p>

## Drip rate chart (drops per minute)

| Volume and time | mL/h | 10 gtt/mL | 15 gtt/mL | 20 gtt/mL | 60 gtt/mL |
|---|---|---|---|---|---|
''' + ''.join(f"| {v} mL over {t} h | {v/t:.0f} | {v*10/(t*60):.0f} | {v*15/(t*60):.0f} | {v*20/(t*60):.0f} | {v*60/(t*60):.0f} |\n" for v, t in [(100, 0.5), (250, 1), (500, 4), (1000, 6), (1000, 8), (1000, 12), (500, 24)]) + '''
## Worked example

1,000 mL over 8 hours with a 20 gtt/mL set:

- Flow rate = 1,000 ÷ 8 = **125 mL/h**
- Time in minutes = 480
- Drip rate = 1,000 × 20 ÷ 480 = **41.7 ≈ 42 drops/min**

## Counting drops

Count drops in the drip chamber for 15 seconds and multiply by 4, or count for a full minute for accuracy. Adjust the roller clamp until the count matches.

## Infusion time from rate

Rearranged: time (h) = volume ÷ mL/h. 500 mL at 125 mL/h takes 4 hours. In the calculator, press × on Infusion time and enter the rate.

## Macrodrip vs microdrip

- **Macrodrip** (10–20 gtt/mL): larger drops, for routine adult fluids.
- **Microdrip** (60 gtt/mL): small drops, for paediatrics and precise low rates.
''')

def iom(b):
    if b < 18.5: return (12.5, 18)
    if b < 25: return (11.5, 16)
    if b < 30: return (7, 11.5)
    return (5, 9)
page('health', 'pregnancy-weight-gain', f'''
title: Pregnancy Weight Gain Calculator
description: See the recommended total weight gain in pregnancy based on pre-pregnancy BMI, using the Institute of Medicine (IOM) 2009 guidelines.
category: health
keywords: [pregnancy weight gain calculator, how much weight to gain in pregnancy, iom guidelines, pregnancy bmi, weight gain during pregnancy, twins weight gain]
updated: {D}
variables:
  - {{ id: m, label: Pre-pregnancy weight, family: mass, unit: kg, imperialUnit: lb, default: 60, min: 30 }}
  - {{ id: h, label: Height, family: length, unit: cm, imperialUnit: in, default: 162, min: 1.2, max: 2.2 }}
  - id: bmi
    label: Pre-pregnancy BMI
    min: 0
    decimals: 1
    bands:
      - {{ max: 18.5, label: Underweight, color: '#3b82f6' }}
      - {{ max: 25, label: Healthy weight, color: '#16a34a' }}
      - {{ max: 30, label: Overweight, color: '#f59e0b' }}
      - {{ max: 100, label: Obese, color: '#dc2626' }}
  - {{ id: lo, label: Recommended gain — lower, family: mass, unit: kg, imperialUnit: lb, min: 0, decimals: 1 }}
  - {{ id: hi, label: Recommended gain — upper, family: mass, unit: kg, imperialUnit: lb, min: 0, decimals: 1 }}
equations:
  - bmi = m / h^2
  - lo = 12.5 - 1 * step(bmi - 18.4999) - 4.5 * step(bmi - 24.9999) - 2 * step(bmi - 29.9999)
  - hi = 18 - 2 * step(bmi - 18.4999) - 4.5 * step(bmi - 24.9999) - 2.5 * step(bmi - 29.9999)
freedom: 2
faq:
  - q: How much weight should I gain during pregnancy?
    a: It depends on your BMI before pregnancy. For a healthy BMI (18.5–24.9), the IOM recommends 11.5–16 kg (25–35 lb) for a single baby.
  - q: How much weight should I gain with twins?
    a: For twins, IOM provisional ranges are 17–25 kg (37–54 lb) for healthy BMI, 14–23 kg for overweight and 11–19 kg for obese.
  - q: How fast should I gain weight?
    a: Typically 0.5–2 kg in the first trimester, then about 0.4 kg a week (1 lb) in the second and third trimesters for a healthy BMI.
  - q: Is it safe to lose weight during pregnancy?
    a: Weight loss is not generally recommended in pregnancy. Speak to your doctor or midwife about any weight concerns.
related: [other/due-date, health/bmi, health/bmr, health/water-intake]
''', '''
## How to use this calculator

Enter your **weight before pregnancy** and your **height**. The calculator works out your pre-pregnancy BMI and the recommended total weight gain range for a single baby.

This is general guidance. Your doctor or midwife may recommend a different target based on your health.

## IOM 2009 recommendations (single baby)

| Pre-pregnancy BMI | Total gain | Weekly gain, 2nd and 3rd trimesters |
|---|---|---|
| Underweight (under 18.5) | 12.5–18 kg (28–40 lb) | about 0.5 kg (1–1.3 lb) |
| Healthy (18.5–24.9) | 11.5–16 kg (25–35 lb) | about 0.4 kg (0.8–1 lb) |
| Overweight (25–29.9) | 7–11.5 kg (15–25 lb) | about 0.3 kg (0.5–0.7 lb) |
| Obese (30+) | 5–9 kg (11–20 lb) | about 0.2 kg (0.4–0.6 lb) |

Source: Institute of Medicine (now National Academy of Medicine), *Weight Gain During Pregnancy*, 2009.

## Where the weight goes

For a typical healthy pregnancy of about 13 kg:

| Component | Approximate weight |
|---|---|
| Baby | 3.4 kg |
| Placenta | 0.7 kg |
| Amniotic fluid | 0.8 kg |
| Uterus | 0.9 kg |
| Breast tissue | 0.4 kg |
| Blood volume | 1.4 kg |
| Fluid in tissues | 1.5 kg |
| Fat stores | 3–4 kg |

## Healthy habits

- Eat regular balanced meals; most people need only about 300–450 extra kcal a day in the second and third trimesters, and none in the first.
- Stay active with approved exercise such as walking or swimming.
- Take supplements such as folic acid and iron as advised.

## Asian BMI cut-offs

Some guidelines suggest lower BMI cut-offs for Asian women, which would shift some people into a higher category. Ask your care provider which cut-offs they use.
''')

def ldl(tc, hdl, tg): return tc - hdl - tg/5
page('health', 'ldl-cholesterol', f'''
title: LDL Cholesterol Calculator (Friedewald)
description: Estimate LDL cholesterol from total cholesterol, HDL and triglycerides using the Friedewald formula, plus non-HDL cholesterol and ratios.
category: health
keywords: [ldl calculator, ldl cholesterol calculator, friedewald formula, non hdl cholesterol, cholesterol ratio, lipid profile calculator, calculated ldl]
updated: {D}
variables:
  - {{ id: tc, label: Total cholesterol, suffix: mg/dL, default: 200, min: 0 }}
  - {{ id: hdl, label: HDL cholesterol, suffix: mg/dL, default: 50, min: 1 }}
  - {{ id: tg, label: Triglycerides, suffix: mg/dL, default: 150, min: 0, help: 'Friedewald is not valid when triglycerides are 400 mg/dL or more.' }}
  - {{ id: ldl, label: LDL cholesterol (calculated), suffix: mg/dL, decimals: 0 }}
  - {{ id: nhdl, label: Non-HDL cholesterol, suffix: mg/dL, decimals: 0 }}
  - {{ id: ratio, label: Total / HDL ratio, min: 0, decimals: 2 }}
equations:
  - ldl = tc - hdl - tg / 5
  - nhdl = tc - hdl
  - ratio = tc / hdl
freedom: 3
faq:
  - q: What is a healthy LDL level?
    a: Under 100 mg/dL (2.6 mmol/L) is often described as optimal for most adults. Targets are lower for people at high cardiovascular risk — your doctor will set yours.
  - q: When is the Friedewald formula not accurate?
    a: When triglycerides are 400 mg/dL or more, in non-fasting samples with high triglycerides, and at very low LDL levels. Labs may use the Martin–Hopkins or Sampson formulas or measure LDL directly.
  - q: How do I convert mmol/L to mg/dL?
    a: Multiply cholesterol values by 38.67 and triglycerides by 88.57.
  - q: What is non-HDL cholesterol?
    a: Total cholesterol minus HDL. It includes all the cholesterol carried by potentially harmful particles and does not need fasting.
related: [health/bmi, health/waist-to-height, health/macros, health/heart-rate-zones]
''', '''
## How to use this calculator

Enter **total cholesterol**, **HDL** and **triglycerides** in mg/dL from your lipid profile. The calculator estimates LDL, non-HDL cholesterol and the total-to-HDL ratio.

This is for understanding results, not diagnosis. Discuss your numbers and overall cardiovascular risk with a doctor.

## The Friedewald formula

<p class="formula">LDL = Total cholesterol − HDL − Triglycerides ÷ 5</p>

In mmol/L, use triglycerides ÷ 2.2 instead of ÷ 5.

## Example

Total 200, HDL 50, triglycerides 150 mg/dL:

- LDL = 200 − 50 − 30 = **120 mg/dL**
- Non-HDL = **150 mg/dL**
- Total/HDL ratio = **4.0**

## General reference ranges (adults, mg/dL)

| Measure | Desirable | Borderline | High |
|---|---|---|---|
| Total cholesterol | under 200 | 200–239 | 240+ |
| LDL | under 100 | 130–159 | 160+ |
| HDL | 60+ (protective) | 40–59 | under 40 is low |
| Triglycerides | under 150 | 150–199 | 200+ |
| Non-HDL | under 130 | 130–159 | 160+ |

Ranges follow common US (NCEP ATP III) categories. Treatment targets depend on individual risk.

## Unit conversion

| mg/dL | mmol/L (cholesterol) | mmol/L (triglycerides) |
|---|---|---|
''' + ''.join(f"| {v} | {v/38.67:.2f} | {v/88.57:.2f} |\n" for v in [50, 100, 130, 150, 200, 240, 300]) + '''
## Lowering LDL

Diet changes (less saturated and trans fat, more fibre), regular exercise, weight management and not smoking all help. Many people also need medication, depending on their risk. Follow your doctor's advice.
''')

# ---------------- math
page('math', 'weighted-average', f'''
title: Weighted Average Calculator
description: Calculate a weighted average (weighted mean) from up to five values and weights — for grades, prices, portfolios and survey scores.
category: math
keywords: [weighted average calculator, weighted mean, weighted average formula, weighted grade calculator, average with weights, weighted score]
updated: {D}
featured: true
variables:
  - {{ id: x1, label: Value 1, default: 85 }}
  - {{ id: w1, label: Weight 1, default: 30, min: 0 }}
  - {{ id: x2, label: Value 2, default: 72 }}
  - {{ id: w2, label: Weight 2, default: 20, min: 0 }}
  - {{ id: x3, label: Value 3, default: 90 }}
  - {{ id: w3, label: Weight 3, default: 50, min: 0 }}
  - {{ id: x4, label: Value 4 (optional), default: 0 }}
  - {{ id: w4, label: Weight 4, default: 0, min: 0 }}
  - {{ id: x5, label: Value 5 (optional), default: 0 }}
  - {{ id: w5, label: Weight 5, default: 0, min: 0 }}
  - {{ id: W, label: Sum of weights, min: 0 }}
  - {{ id: wa, label: Weighted average }}
equations:
  - W = w1 + w2 + w3 + w4 + w5
  - wa = (x1*w1 + x2*w2 + x3*w3 + x4*w4 + x5*w5) / W
faq:
  - q: How do I calculate a weighted average?
    a: Multiply each value by its weight, add the products, then divide by the sum of the weights.
  - q: Do the weights have to add up to 100?
    a: No. The calculator divides by the total of the weights, so you can use percentages, credits, quantities or any positive numbers.
  - q: What is the difference between a weighted and a simple average?
    a: A simple average treats every value equally. A weighted average gives more influence to values with larger weights.
  - q: How do I ignore an unused row?
    a: Leave its weight at 0.
related: [math/average, everyday-life/grade-needed, finance/stock-average, statistics/mean-median-mode]
''', '''
## How to use this calculator

Enter up to five **values** and their **weights**. Leave unused rows with a weight of 0. The calculator shows the total weight and the weighted average.

## The formula

<p class="formula">Weighted average = Σ(xᵢ × wᵢ) ÷ Σwᵢ</p>

## Example: course grade

| Component | Score | Weight | Score × weight |
|---|---|---|---|
| Assignments | 85 | 30% | 25.5 |
| Midterm | 72 | 20% | 14.4 |
| Final exam | 90 | 50% | 45.0 |
| **Total** | | **100%** | **84.9** |

The weighted grade is **84.9**, while the simple average of 85, 72 and 90 is 82.3.

## Common uses

| Use | Values | Weights |
|---|---|---|
| Course grades | Scores | Percentage weights or credits |
| GPA / CGPA | Grade points | Credit hours |
| Average purchase price | Prices | Quantities bought |
| Portfolio return | Asset returns | Amount invested in each |
| Survey ratings | Rating levels (1–5) | Number of responses |

## Weighted price example

Buying 100 units at 20 and 300 units at 24 gives a weighted average price of (2,000 + 7,200) ÷ 400 = **23**, not the simple average of 22. See the [stock average calculator](/finance/stock-average/) for share purchases.

## Weighted vs arithmetic mean

If all weights are equal, the weighted average equals the ordinary [average](/math/average/).
''')

page('math', 'box-volume', f'''
title: Box Volume Calculator (Rectangular Prism)
description: Calculate the volume, surface area and diagonal of a box or rectangular prism — in litres, cubic metres, cubic feet or gallons.
category: math
keywords: [box volume calculator, volume of a box, rectangular prism volume, cuboid volume, cubic feet calculator, surface area of a box, cubic meters calculator]
updated: {D}
variables:
  - {{ id: l, label: Length, family: length, unit: cm, imperialUnit: in, default: 60, min: 0 }}
  - {{ id: w, label: Width, family: length, unit: cm, imperialUnit: in, default: 40, min: 0 }}
  - {{ id: h, label: Height, family: length, unit: cm, imperialUnit: in, default: 30, min: 0 }}
  - {{ id: V, label: Volume, family: volume, unit: L, imperialUnit: ft3, min: 0 }}
  - {{ id: S, label: Surface area, family: area, unit: m2, imperialUnit: ft2, min: 0 }}
  - {{ id: d, label: Space diagonal, family: length, unit: cm, imperialUnit: in, min: 0 }}
equations:
  - V = l * w * h
  - S = 2 * (l*w + l*h + w*h)
  - d = sqrt(l^2 + w^2 + h^2)
faq:
  - q: How do I calculate the volume of a box?
    a: Multiply length × width × height. A 60 × 40 × 30 cm box holds 72,000 cm³, or 72 litres.
  - q: How do I convert cm³ to litres?
    a: Divide by 1,000. 1,000 cm³ = 1 litre.
  - q: How many cubic feet is a box?
    a: Measure in feet and multiply, or measure in inches, multiply and divide by 1,728.
  - q: What is the longest item that fits in a box?
    a: The space diagonal, √(l² + w² + h²). For a 60 × 40 × 30 cm box it is 78.1 cm.
related: [math/cylinder-volume, math/rectangle, construction/rectangular-tank, other/aquarium-volume]
''', '''
## How to use this calculator

Enter the **length**, **width** and **height**. You get the volume, the total surface area and the space diagonal. Change any unit — the results convert automatically.

## The formulas

<p class="formula">V = l × w × h &nbsp;·&nbsp; S = 2(lw + lh + wh) &nbsp;·&nbsp; d = √(l² + w² + h²)</p>

## Common box sizes

| Box (cm) | Volume | Cubic feet |
|---|---|---|
''' + ''.join(f"| {l} × {w} × {h} | {l*w*h/1000:.1f} L | {l*w*h/28316.85:.2f} ft³ |\n" for l, w, h in [(30, 20, 15), (40, 30, 30), (45, 45, 45), (60, 40, 40), (60, 45, 45), (100, 100, 100)]) + '''
## Shipping: volumetric weight

Couriers charge by actual or volumetric weight, whichever is higher:

<p class="formula">Volumetric weight (kg) = L × W × H (cm) ÷ 5,000</p>

A 60 × 40 × 30 cm box has a volumetric weight of 14.4 kg. Some carriers divide by 6,000 for road freight — check your courier.

## Moving and storage

- A standard moving box is roughly 1.5–3 ft³.
- A storage unit 5 × 10 × 8 ft holds 400 ft³ (11.3 m³).
- A 20 ft shipping container has about 33 m³ of internal space.

## Cube

For a cube with side s: V = s³, S = 6s², d = s√3.
''')

def loc(a, b, C): return math.sqrt(a*a + b*b - 2*a*b*math.cos(math.radians(C)))
page('math', 'law-of-cosines', f'''
title: Law of Cosines Calculator
description: Find the third side, the angles and the area of any triangle from two sides and the included angle, using the law of cosines.
category: math
keywords: [law of cosines calculator, cosine rule, sas triangle, find third side of triangle, triangle calculator, solve triangle, cosine law]
updated: {D}
variables:
  - {{ id: a, label: Side a, family: length, unit: cm, imperialUnit: in, default: 7, min: 0 }}
  - {{ id: b, label: Side b, family: length, unit: cm, imperialUnit: in, default: 9, min: 0 }}
  - {{ id: C, label: Angle C (between a and b), family: angle, unit: deg, default: 50, min: 0, max: 3.1416 }}
  - {{ id: c, label: Side c, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: A, label: Angle A, family: angle, unit: deg, min: 0 }}
  - {{ id: B, label: Angle B, family: angle, unit: deg, min: 0 }}
  - {{ id: K, label: Area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
equations:
  - c = sqrt(a^2 + b^2 - 2*a*b*cos(C))
  - A = acos((b^2 + c^2 - a^2) / (2*b*c))
  - B = pi - A - C
  - K = a * b * sin(C) / 2
faq:
  - q: What is the law of cosines?
    a: c² = a² + b² − 2ab·cos C. It relates the three sides of any triangle to one of its angles.
  - q: When do I use the law of cosines instead of the law of sines?
    a: Use cosines when you know two sides and the angle between them (SAS) or all three sides (SSS). Use sines when you know two angles and a side, or two sides and a non-included angle.
  - q: How do I find an angle from three sides?
    a: cos A = (b² + c² − a²) ÷ 2bc. In the calculator, enter a, b and c and press × on angle C.
  - q: Is the Pythagorean theorem a special case?
    a: Yes. When C = 90°, cos C = 0 and the formula becomes c² = a² + b².
related: [math/pythagorean-theorem, math/right-triangle-trig, math/triangle-area, math/polygon]
''', f'''
## How to use this calculator

Enter two sides, **a** and **b**, and the **angle C** between them. The calculator finds the third side, the other two angles and the area. You can also enter all three sides and press × on angle C to find the angles.

## The law of cosines

<p class="formula">c² = a² + b² − 2ab cos C</p>

and for angles:

<p class="formula">cos A = (b² + c² − a²) ÷ 2bc</p>

## Worked example

a = 7, b = 9, C = 50°:

- c² = 49 + 81 − 126 × cos 50° = 130 − 80.99 = 49.01
- c = **{loc(7,9,50):.2f}**
- Area = ½ × 7 × 9 × sin 50° = **{0.5*7*9*math.sin(math.radians(50)):.2f}**

## Third side for different angles (a = 7, b = 9)

| Angle C | Side c |
|---|---|
''' + ''.join(f"| {C}° | {loc(7,9,C):.2f} |\n" for C in [10, 30, 60, 90, 120, 150, 170]) + '''
As the angle opens, the third side grows from about b − a towards a + b.

## Law of sines

<p class="formula">a ÷ sin A = b ÷ sin B = c ÷ sin C</p>

Use it with two angles and a side. Beware the ambiguous case (two sides and a non-included angle), which can have two solutions.

## Real-world uses

- **Surveying**: distance across a lake from two measured sides and the angle between them.
- **Navigation**: distance between two ships from their bearings and distances.
- **Engineering**: forces in trusses and linkages.
''')

page('math', 'polygon', f'''
title: Regular Polygon Calculator (Angles, Area, Perimeter)
description: Find the interior and exterior angles, number of diagonals, perimeter and area of any regular polygon — triangle, hexagon, octagon and more.
category: math
keywords: [polygon calculator, interior angle of polygon, sum of interior angles, hexagon area, octagon area, regular polygon area, exterior angle, number of diagonals]
updated: {D}
variables:
  - {{ id: n, label: Number of sides, default: 6, min: 3, decimals: 0 }}
  - {{ id: s, label: Side length, family: length, unit: cm, imperialUnit: in, default: 10, min: 0 }}
  - {{ id: sum, label: Sum of interior angles, suffix: °, decimals: 1 }}
  - {{ id: ia, label: Each interior angle, suffix: °, decimals: 2 }}
  - {{ id: ea, label: Each exterior angle, suffix: °, decimals: 2 }}
  - {{ id: dg, label: Number of diagonals, decimals: 0 }}
  - {{ id: P, label: Perimeter, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: A, label: Area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
equations:
  - sum = (n - 2) * 180
  - ia = sum / n
  - ea = 360 / n
  - dg = n * (n - 3) / 2
  - P = n * s
  - A = n * s^2 / (4 * tan(pi / n))
faq:
  - q: What is the sum of interior angles of a polygon?
    a: (n − 2) × 180°. A hexagon (6 sides) has 720°, so each angle of a regular hexagon is 120°.
  - q: How many diagonals does a polygon have?
    a: n(n − 3) ÷ 2. An octagon has 20 diagonals.
  - q: What is the area of a regular hexagon?
    a: (3√3 ÷ 2) × s², about 2.598 × s². With 10 cm sides, about 259.8 cm².
  - q: Do exterior angles always add to 360°?
    a: Yes, for any convex polygon the exterior angles sum to 360°.
related: [math/triangle-area, math/circle, math/rectangle, math/law-of-cosines]
''', '''
## How to use this calculator

Enter the **number of sides** and the **side length**. The calculator shows the angles, number of diagonals, perimeter and area of the regular polygon. The angle results apply to any polygon with that number of sides; the area and perimeter assume all sides and angles are equal.

## The formulas

| Quantity | Formula |
|---|---|
| Sum of interior angles | (n − 2) × 180° |
| Each interior angle | (n − 2) × 180° ÷ n |
| Each exterior angle | 360° ÷ n |
| Diagonals | n(n − 3) ÷ 2 |
| Area | n × s² ÷ (4 tan(π ÷ n)) |

## Polygon table

| Polygon | Sides | Interior angle | Diagonals | Area (side 1) |
|---|---|---|---|---|
''' + ''.join(f"| {nm} | {n} | {(n-2)*180/n:.2f}° | {n*(n-3)//2} | {n/(4*math.tan(math.pi/n)):.4f} |\n" for nm, n in [('Triangle', 3), ('Square', 4), ('Pentagon', 5), ('Hexagon', 6), ('Heptagon', 7), ('Octagon', 8), ('Nonagon', 9), ('Decagon', 10), ('Dodecagon', 12)]) + '''
Multiply the last column by the side length squared to get the area.

## Hexagons in nature and design

Regular hexagons tile a flat surface with no gaps and use the least perimeter for a given area among shapes that tile, which is why honeycombs and many floor tiles are hexagonal.

## Radius of a regular polygon

- Circumradius (centre to corner): R = s ÷ (2 sin(π ÷ n))
- Inradius (centre to middle of a side): r = s ÷ (2 tan(π ÷ n))

As n grows large, the polygon approaches a circle.
''')

def ram(a, b): return math.pi*(3*(a+b) - math.sqrt((3*a+b)*(a+3*b)))
page('math', 'ellipse', f'''
title: Ellipse Calculator (Area, Perimeter, Eccentricity)
description: Calculate the area, perimeter (Ramanujan approximation), eccentricity and foci distance of an ellipse from its two semi-axes.
category: math
keywords: [ellipse calculator, area of ellipse, perimeter of ellipse, circumference of ellipse, eccentricity calculator, oval area, ellipse foci]
updated: {D}
variables:
  - {{ id: a, label: Semi-major axis (a), family: length, unit: cm, imperialUnit: in, default: 10, min: 0 }}
  - {{ id: b, label: Semi-minor axis (b), family: length, unit: cm, imperialUnit: in, default: 6, min: 0 }}
  - {{ id: A, label: Area, family: area, unit: cm2, imperialUnit: in2, min: 0 }}
  - {{ id: P, label: Perimeter (approx.), family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: ec, label: Eccentricity, min: 0, max: 1, decimals: 4 }}
  - {{ id: fc, label: Centre to each focus, family: length, unit: cm, imperialUnit: in, min: 0 }}
equations:
  - A = pi * a * b
  - P = pi * (3*(a + b) - sqrt((3*a + b) * (a + 3*b)))
  - ec = sqrt(1 - b^2 / a^2)
  - fc = sqrt(a^2 - b^2)
freedom: 2
faq:
  - q: What is the area of an ellipse?
    a: π × a × b, where a and b are the semi-axes (half the longest and shortest widths).
  - q: Is there an exact formula for the perimeter of an ellipse?
    a: No simple exact formula exists. Ramanujan’s approximation used here is accurate to within a tiny fraction of a percent for most shapes.
  - q: What is eccentricity?
    a: A measure of how stretched the ellipse is, from 0 (a circle) to nearly 1 (very flat).
  - q: How do I measure an oval table?
    a: Measure the full length and width, then halve each to get a and b.
related: [math/circle, math/arc-length, math/sphere, math/polygon]
''', f'''
## How to use this calculator

Enter the **semi-major axis** (half the longest width) and the **semi-minor axis** (half the shortest width). You get the area, perimeter, eccentricity and the distance from the centre to each focus.

## The formulas

| Quantity | Formula |
|---|---|
| Area | π a b |
| Perimeter (Ramanujan) | π [3(a + b) − √((3a + b)(a + 3b))] |
| Eccentricity | √(1 − b² ÷ a²) |
| Focus distance | √(a² − b²) |

## Example

a = 10 cm, b = 6 cm:

- Area = π × 10 × 6 = **{math.pi*60:.2f} cm²**
- Perimeter ≈ **{ram(10,6):.2f} cm**
- Eccentricity = **{math.sqrt(1-36/100):.4f}**

## Ellipse table (a = 10)

| b | Area | Perimeter | Eccentricity |
|---|---|---|---|
''' + ''.join(f"| {b} | {math.pi*10*b:.1f} | {ram(10,b):.2f} | {math.sqrt(1-b*b/100):.3f} |\n" for b in [10, 8, 6, 4, 2, 1]) + '''
When b = a, the ellipse is a circle and the eccentricity is 0.

## Planet orbits

Planets move in ellipses with the Sun at one focus. Earth's orbit has an eccentricity of about 0.017 — almost a circle. Halley's Comet has about 0.967, a long, thin ellipse.

## Drawing an ellipse

Push two pins into a board at the foci, loop a string of length 2a around them and trace with a pencil keeping the string tight. This is the gardener's method for oval flower beds.
''')

page('math', 'factorial', f'''
title: Factorial Calculator (n!)
description: Calculate the factorial of a number (n!) exactly up to 170, with the number of digits and a table of factorials.
category: math
keywords: [factorial calculator, n factorial, factorial of a number, 10 factorial, 52 factorial, permutations factorial, gamma function]
updated: {D}
variables:
  - {{ id: n, label: Number (n), default: 10, min: 0, max: 170 }}
  - {{ id: f, label: n!, min: 0 }}
  - {{ id: dg, label: Number of digits, min: 0, decimals: 0 }}
equations:
  - f = fact(n)
  - dg = floor(log10(f)) + 1
freedom: 1
faq:
  - q: What is a factorial?
    a: The product of all whole numbers from 1 to n. 5! = 5 × 4 × 3 × 2 × 1 = 120.
  - q: What is 0 factorial?
    a: 0! = 1, by definition. It keeps formulas for combinations and permutations consistent.
  - q: Why is 170 the limit?
    a: 171! is larger than the biggest number standard double-precision arithmetic can store (about 1.8 × 10³⁰⁸).
  - q: Can I take the factorial of a decimal?
    a: The gamma function extends factorials to non-integers, with n! = Γ(n + 1). The calculator returns Γ(n + 1) for decimal inputs.
related: [statistics/permutations, statistics/combinations, math/exponent, statistics/binomial-probability]
''', '''
## How to use this calculator

Enter a whole number **n** from 0 to 170. The calculator shows n! and how many digits it has. Results above 15 digits are shown in scientific notation.

## The formula

<p class="formula">n! = n × (n − 1) × (n − 2) × … × 2 × 1</p>

## Factorial table

| n | n! |
|---|---|
''' + ''.join(f"| {n} | {math.factorial(n):,} |\n" for n in range(0, 21)) + '''
## How fast factorials grow

| n | n! (approx.) | Digits |
|---|---|---|
''' + ''.join(f"| {n} | {float(math.factorial(n)):.3e} | {len(str(math.factorial(n)))} |\n" for n in [25, 50, 52, 70, 100, 170]) + '''
52! — the number of ways to shuffle a deck of cards — has 68 digits.

## Stirling's approximation

For large n:

<p class="formula">n! ≈ √(2πn) × (n ÷ e)<sup>n</sup></p>

At n = 10 it gives 3,598,696, within 0.83% of the true 3,628,800, and it gets more accurate as n grows.

## Where factorials are used

- **Permutations**: arranging n items in order — n!. See the [permutations calculator](/statistics/permutations/).
- **Combinations**: n! ÷ (r!(n − r)!). See the [combinations calculator](/statistics/combinations/).
- **Probability**: binomial and Poisson distributions.
- **Series**: Taylor series for eˣ, sin x and cos x.
''')
print('batchB2 done')
