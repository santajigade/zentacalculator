import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words
f = lambda x, d=0: f"{x:,.{d}f}"

# ---------------- alcohol units
drinks = [('Beer, 330 mL bottle', 330, 5), ('Beer, pint (568 mL)', 568, 4.5), ('Strong beer, 500 mL can', 500, 8), ('Wine, 175 mL glass', 175, 13), ('Wine, 750 mL bottle', 750, 13), ('Spirit, 25 mL shot', 25, 40), ('Spirit, 60 mL (large peg)', 60, 42.8), ('Cider, 500 mL', 500, 5)]
rows = ''.join(f"| {n} | {a}% | {v*a/1000:.1f} | {v*a/100*0.789/14:.1f} | {v*a/100*0.789*7:.0f} |\n" for n, v, a in drinks)
expand('health/alcohol-units', f'''
## Units, standard drinks and calories

| Drink | ABV | UK units | US standard drinks | Calories from alcohol |
|---|---|---|---|---|
{rows}
Calories shown are from the alcohol alone (7 kcal per gram). Sugary mixers, cocktails and sweet wines add more.

## Standard drink sizes around the world

A “standard drink” is not the same everywhere:

| Country | Alcohol per standard drink |
|---|---|
| United Kingdom | 8 g (1 unit) |
| Australia | 10 g |
| United States | 14 g |
| Japan | 20 g |

Always check which definition a guideline uses before comparing limits.

## How long alcohol stays in your body

The liver clears roughly **one UK unit (8 g) per hour**, but this varies with body size, sex, food, medicines and liver health. Coffee, cold showers and sleep do not speed it up. If you drink late, you may still be over the driving limit the next morning.

## Lowering your intake

- Choose lower-strength drinks and smaller glasses.
- Alternate alcoholic drinks with water.
- Have several alcohol-free days each week.
- Track units for a week with this calculator — most people underestimate what they drink.

The World Health Organization notes that no level of drinking is completely free of health risk.
''', [
 ('How many units are in a large glass of wine?', 'A 250 mL glass of 13% wine has about 3.3 UK units, almost a quarter of the UK weekly guideline of 14 units.'),
 ('Does a shot of spirits have less alcohol than a beer?', 'A 25 mL shot of 40% spirit has 1 unit, while a pint of 4.5% beer has about 2.6 units. Size matters as much as strength.'),
])

# ---------------- BMI
hs = [155, 160, 165, 170, 175, 180, 185, 190]
rows = ''.join(f"| {h} cm ({int(h/2.54//12)}′{round(h/2.54%12)}″) | {18.5*(h/100)**2:.1f} kg | {24.9*(h/100)**2:.1f} kg | {29.9*(h/100)**2:.1f} kg |\n" for h in hs)
expand('health/bmi', f'''
## Healthy weight range by height

| Height | BMI 18.5 | BMI 24.9 | BMI 29.9 |
|---|---|---|---|
{rows}
Weights between the BMI 18.5 and 24.9 columns fall in the healthy range for adults.

## BMI cut-offs for Asian populations

Studies show that people of South Asian, Chinese and other Asian backgrounds tend to have more body fat and higher diabetes risk at the same BMI. A WHO expert consultation suggested lower action points, and several countries use them:

| Category | Standard (WHO) | Common Asian cut-offs |
|---|---|---|
| Healthy | 18.5–24.9 | 18.5–22.9 |
| Overweight | 25–29.9 | 23–24.9 (or 23–27.4) |
| Obese | 30 or more | 25 or more (or 27.5+) |

If you are of Asian heritage, a BMI of 23 or above is worth discussing with a doctor.

## BMI for children and teenagers

For people under 18, BMI is compared with growth charts for the same age and sex, giving a **percentile**. The adult categories above do not apply. Use your country's paediatric BMI charts or ask a health professional.

## BMI Prime

BMI Prime is your BMI divided by 25, the upper limit of the healthy range. A BMI Prime of 0.74–1.00 is in the healthy range; 1.10 means 10% above the upper limit.

## Better together: BMI plus waist size

Waist size shows where fat is stored, which BMI cannot. Check your [waist-to-height ratio](/health/waist-to-height/) as well — keeping your waist below half your height is a simple target.
''', [
 ('What BMI is considered obese?', 'A BMI of 30 or more under the standard WHO categories. Many Asian countries use a lower threshold of 25 or 27.5.'),
 ('Does BMI differ for men and women?', 'The formula and adult categories are the same for both. Women naturally carry more body fat at the same BMI, which BMI does not show.'),
], before='## Limitations')

# ---------------- BMR
def mif(s, a, m, h): return 10*m + 625*h - 5*a + s
def hb(male, a, m, h):
    return 88.362 + 13.397*m + 479.9*h - 5.677*a if male else 447.593 + 9.247*m + 309.8*h - 4.330*a
expand('health/bmr', f'''
## BMR by formula

For a 30-year-old man, 70 kg, 175 cm:

| Formula | BMR (kcal/day) |
|---|---|
| Mifflin–St Jeor (used here) | {mif(5,30,70,1.75):.0f} |
| Revised Harris–Benedict (1984) | {hb(True,30,70,1.75):.0f} |
| Katch–McArdle (needs body fat %; 15% shown) | {370+21.6*70*0.85:.0f} |

The formulas usually agree within 5%. Katch–McArdle can be better for very lean or muscular people because it uses lean body mass. Find yours with the [lean body mass calculator](/health/lean-body-mass/).

## BMR by age and weight

Women, 165 cm (Mifflin–St Jeor):

| Weight | Age 25 | Age 40 | Age 60 |
|---|---|---|---|
''' + ''.join(f"| {m} kg | {mif(-161,25,m,1.65):.0f} | {mif(-161,40,m,1.65):.0f} | {mif(-161,60,m,1.65):.0f} |\n" for m in [55, 65, 75, 85]) + f'''
BMR falls by about 50 kcal a day for every 10 years of age, mainly because muscle mass declines.

## What affects your metabolism

- **Muscle mass**: muscle uses more energy at rest than fat. Strength training helps maintain it.
- **Age**: metabolism slows gradually from middle age.
- **Body size**: larger bodies need more energy.
- **Hormones**: thyroid conditions can raise or lower BMR. See a doctor if you suspect a problem.
- **Severe dieting**: very low calorie intake can reduce energy expenditure, making further weight loss harder.

## Using TDEE for goals

- **Maintain weight**: eat about your TDEE.
- **Gradual weight loss**: a modest deficit of 300–500 kcal below TDEE.
- **Gain muscle**: a small surplus of 200–300 kcal with strength training.

Track your weight for 2–3 weeks and adjust, because every formula is an estimate.
''', [
 ('Does BMR include exercise?', 'No. BMR is energy used at complete rest. TDEE adds daily movement and exercise using the activity factor.'),
 ('Why is my BMR lower than my friend’s?', 'BMR depends on weight, height, age, sex and especially muscle mass. Two people of the same weight can differ by 100–200 kcal a day.'),
], before='## Limitations')

# ---------------- body fat
expand('health/body-fat', '''
## Body fat measurement methods compared

| Method | Typical accuracy | Cost and access |
|---|---|---|
| DEXA scan | ±1–2% | Clinic, expensive |
| Hydrostatic (underwater) weighing | ±2% | Labs, rare |
| Air displacement (Bod Pod) | ±2–3% | Some gyms and labs |
| Skinfold calipers (trained tester) | ±3–4% | Cheap |
| **US Navy tape method** | ±3–4% | Free — tape measure |
| Bioelectrical impedance (smart scales) | ±4–5% | Cheap, varies with hydration |

The Navy method is as good as most home options. Use the same method each time to track change.

## Body fat by age (general guide)

Healthy body fat tends to rise slightly with age:

| Age | Men | Women |
|---|---|---|
| 20–39 | 8–19% | 21–32% |
| 40–59 | 11–21% | 23–33% |
| 60–79 | 13–24% | 24–35% |

Ranges follow commonly cited guidance based on BMI-matched data (Gallagher et al., 2000). They are a guide, not a diagnosis.

## Essential fat

Some fat is vital for hormones, nerves and organs. Essential fat is about 2–5% for men and 10–13% for women. Going below these levels is dangerous, even for athletes.

## Fat mass and lean mass

Multiply your weight by your body fat percentage to get fat mass. The rest is lean mass — muscle, bone, organs and water. Losing fat while keeping lean mass is the goal of most training plans.
''', [
 ('Why does my smart scale show a different number?', 'Smart scales use bioelectrical impedance, which changes with hydration, meals and exercise. Readings can vary by several percent from day to day.'),
 ('How fast can I lower my body fat?', 'A realistic rate is about 0.5–1% of body fat per month with a modest calorie deficit and strength training.'),
], before='## Tips for consistent results')

# ---------------- BSA
def most(h, m): return math.sqrt(h*m/3600)
def dub(h, m): return 0.007184*h**0.725*m**0.425
def hay(h, m): return 0.024265*h**0.3964*m**0.5378
rows = ''.join(f"| {h} cm, {m} kg | {most(h,m):.2f} | {dub(h,m):.2f} | {hay(h,m):.2f} |\n" for h, m in [(150, 50), (160, 60), (170, 70), (175, 80), (185, 95), (110, 18)])
expand('health/body-surface-area', f'''
## BSA by formula

| Height and weight | Mosteller | Du Bois | Haycock |
|---|---|---|---|
{rows}
The formulas agree closely for typical adults. Haycock was developed with children included and is often preferred in paediatrics.

## Typical BSA values

| Group | Average BSA |
|---|---|
| Newborn | 0.25 m² |
| Child, 10 years | 1.1 m² |
| Adult woman | 1.6 m² |
| Adult man | 1.9 m² |

## Where BSA is used

- **Chemotherapy**: many cancer drug doses are given per m² of BSA.
- **Cardiac index**: cardiac output divided by BSA, to compare heart function between people of different sizes.
- **Kidney function**: GFR is often reported per 1.73 m², the BSA of an average adult.
- **Burns**: the extent of burns is estimated as a percentage of total body surface.

## Units

BSA is in square metres. The Mosteller formula uses height in centimetres and weight in kilograms. If you enter feet, inches or pounds, the calculator converts them for you.
''', [
 ('Why is GFR adjusted to 1.73 m²?', '1.73 m² is the average BSA of adults in early studies. Adjusting to it lets doctors compare kidney function between people of different sizes.'),
 ('Can I use BSA to dose medicine at home?', 'No. Dosing by BSA is done by doctors and pharmacists for specific drugs. Always follow your prescription.'),
], before='## Important')

# ---------------- calories burned
acts = [('Walking, 5 km/h', 3.5), ('Walking briskly, 6.4 km/h', 5.0), ('Running, 8 km/h', 8.3), ('Running, 9.7 km/h', 9.8), ('Cycling, moderate (19–22 km/h)', 8.0), ('Swimming, moderate freestyle', 5.8), ('Yoga (hatha)', 2.5), ('Weight training, vigorous', 6.0), ('Dancing, ballroom (fast)', 5.5), ('Housework, moderate effort', 3.5)]
rows = ''.join(f"| {n} | {m} | {m*3.5*60/200*30:.0f} | {m*3.5*80/200*30:.0f} | {m*3.5*80/200*60:.0f} |\n" for n, m in acts)
expand('health/calories-burned', f'''
## Calories burned by activity

| Activity | MET | 60 kg, 30 min | 80 kg, 30 min | 80 kg, 60 min |
|---|---|---|---|---|
{rows}
MET values are from the Compendium of Physical Activities. Your actual burn depends on effort, fitness and terrain.

## Net vs gross calories

The formula gives **gross** calories, which include the energy you would have used anyway at rest (1 MET). To find the **extra** calories from exercise, use (MET − 1) instead of MET. For a 30-minute walk at 3.5 MET, the net burn is about 70% of the gross figure.

## Fitness trackers vs MET estimates

Watches and trackers combine heart rate and movement. Independent studies have found calorie estimates that are off by 20% or more, even when heart rate is accurate. Treat any single number as a rough guide and look at trends over weeks.

## Exercise and weight loss

Exercise burns fewer calories than many people expect — a 30-minute run is about one large snack. Exercise matters most for heart health, mood, muscle and keeping weight off. Combine it with eating habits for weight loss, and see the [BMR calculator](/health/bmr/) for your daily needs.
''', [
 ('Does a heavier person burn more calories?', 'Yes. Moving a heavier body takes more energy, so calories burned rise in proportion to body weight for the same activity.'),
 ('How many calories does walking 10,000 steps burn?', 'Roughly 300–500 kcal for most adults, depending on weight and pace. See the steps to distance calculator for an estimate.'),
], before='## Notes')

# ---------------- creatinine clearance
expand('health/creatinine-clearance', '''
## Creatinine unit conversion

| mg/dL | µmol/L |
|---|---|
''' + ''.join(f"| {c} | {c*88.4:.0f} |\n" for c in [0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0]) + '''
To convert µmol/L to mg/dL, divide by 88.4.

## Which body weight to use

The original Cockcroft–Gault study used actual body weight, but in practice:

- **Normal weight**: use actual body weight.
- **Obesity**: many clinicians use ideal or adjusted body weight, because actual weight overestimates clearance. See the [ideal weight calculator](/health/ideal-weight/).
- **Underweight**: use actual body weight.

Hospital pharmacists may follow a specific local policy.

## Kidney function stages (by GFR)

| Stage | GFR (mL/min/1.73 m²) | Description |
|---|---|---|
| G1 | 90 or more | Normal or high |
| G2 | 60–89 | Mildly decreased |
| G3a | 45–59 | Mildly to moderately decreased |
| G3b | 30–44 | Moderately to severely decreased |
| G4 | 15–29 | Severely decreased |
| G5 | Below 15 | Kidney failure |

These stages (KDIGO) use eGFR plus other markers such as protein in the urine. Creatinine clearance is mainly used for adjusting drug doses.

## Things that affect creatinine

Muscle mass, diet (especially cooked meat), some medicines and dehydration can change creatinine levels without any change in kidney function. Very muscular people may have higher creatinine; frail elderly people may have low creatinine that hides reduced kidney function.
''', [
 ('Why does the formula use age?', 'Muscle mass and kidney function both tend to decline with age, so the same creatinine level means lower clearance in an older person.'),
 ('Should I use this to adjust my own medicines?', 'No. Dose adjustments should always be made by your doctor or pharmacist.'),
], before='## Important')

# ---------------- heart rate zones
rows = ''.join(f"| {a} | {220-a} | {208-0.7*a:.0f} | {0.64*(208-0.7*a):.0f}–{0.76*(208-0.7*a):.0f} | {0.77*(208-0.7*a):.0f}–{0.95*(208-0.7*a):.0f} |\n" for a in [20, 30, 40, 50, 60, 70])
expand('health/heart-rate-zones', f'''
## Max heart rate by age

| Age | 220 − age | Tanaka (208 − 0.7 × age) | Moderate (64–76%) | Vigorous (77–95%) |
|---|---|---|---|---|
{rows}
Moderate and vigorous ranges use the percentage-of-max method from the American College of Sports Medicine. The Karvonen method in the calculator adjusts these for your resting heart rate.

## The five-zone model

| Zone | % of heart rate reserve | Feels like | Used for |
|---|---|---|---|
| 1 | 50–60% | Very easy, can chat freely | Warm-up, recovery |
| 2 | 60–70% | Easy, can hold a conversation | Endurance base, fat use |
| 3 | 70–80% | Moderate, short sentences | Aerobic fitness |
| 4 | 80–90% | Hard, a few words at a time | Threshold training |
| 5 | 90–100% | Maximum effort | Short intervals |

Most endurance plans spend about 80% of training time in zones 1–2.

## The talk test

No monitor? Use your breathing:

- **Moderate**: you can talk but not sing.
- **Vigorous**: you can only say a few words before pausing for breath.

## Guidelines

The WHO recommends adults do at least **150–300 minutes of moderate** or **75–150 minutes of vigorous** aerobic activity each week, plus muscle-strengthening on two or more days.
''', [
 ('Why is my real max heart rate different?', 'Age formulas are averages with a spread of about ±10 beats per minute. A supervised exercise test gives your true maximum.'),
 ('Do beta-blockers affect heart rate zones?', 'Yes. They lower heart rate, so zones based on age will be too high. Use perceived effort and ask your doctor.'),
], before='## Safety')

# ---------------- ideal weight
def dev(m, hin): return (50 if m else 45.5) + 2.3*(hin-60)
def rob(m, hin): return (52 if m else 49) + (1.9 if m else 1.7)*(hin-60)
def mil(m, hin): return (56.2 if m else 53.1) + (1.41 if m else 1.36)*(hin-60)
def ham(m, hin): return (48 if m else 45.5) + (2.7 if m else 2.2)*(hin-60)
rows = ''
for h in [155, 160, 165, 170, 175, 180, 185]:
    hin = h/2.54
    rows += f"| {h} cm | {dev(1,hin):.1f} | {dev(0,hin):.1f} | {rob(1,hin):.1f} | {rob(0,hin):.1f} | {18.5*(h/100)**2:.0f}–{24.9*(h/100)**2:.0f} |\n"
expand('health/ideal-weight', f'''
## Ideal weight by height (kg)

| Height | Devine (men) | Devine (women) | Robinson (men) | Robinson (women) | Healthy BMI range |
|---|---|---|---|---|---|
{rows}
## Which formula to trust?

All four classic formulas were designed for drug dosing, not to define a perfect body weight. They give a single number, whereas real health spans a range. For personal goals, the **healthy BMI range** in the last column is a better guide, ideally combined with waist size.

## Ideal vs adjusted body weight

Doctors sometimes use **adjusted body weight** for drug dosing in people with obesity:

<p class="formula">Adjusted weight = Ideal weight + 0.4 × (Actual weight − Ideal weight)</p>

For a man 175 cm (ideal {dev(1,175/2.54):.1f} kg) weighing 100 kg, adjusted weight = {dev(1,175/2.54)+0.4*(100-dev(1,175/2.54)):.1f} kg.

## Frame size

Some charts adjust ideal weight for small, medium or large frames, often by about ±10%. Wrist circumference is a simple way to estimate frame: a smaller wrist for your height suggests a smaller frame.
''', [
 ('What is the ideal weight for a 5′10″ man?', f'About {dev(1,70):.0f} kg ({dev(1,70)*2.2046:.0f} lb) by the Devine formula. The healthy BMI range for that height is about {18.5*1.778**2:.0f}–{24.9*1.778**2:.0f} kg.'),
 ('What is the ideal weight for a 5′4″ woman?', f'About {dev(0,64):.0f} kg ({dev(0,64)*2.2046:.0f} lb) by the Devine formula, with a healthy BMI range of about {18.5*1.6256**2:.0f}–{24.9*1.6256**2:.0f} kg.'),
], before='## Important')

# ---------------- lean body mass
def boer(male, m, h): return 0.407*m + 26.7*h - 19.2 if male else 0.252*m + 47.3*h - 48.3
rows = ''.join(f"| {h} cm, {m} kg | {boer(1,m,h/100):.1f} kg | {boer(0,m,h/100):.1f} kg |\n" for h, m in [(160, 55), (165, 65), (170, 70), (175, 80), (180, 90), (185, 100)])
expand('health/lean-body-mass', f'''
## Lean body mass table (Boer formula)

| Height, weight | Men | Women |
|---|---|---|
{rows}
## Other LBM formulas

| Formula | Men | Women |
|---|---|---|
| Boer (1984) | 0.407W + 0.267H − 19.2 | 0.252W + 0.473H − 48.3 |
| James (1976) | 1.1W − 128(W/H)² | 1.07W − 148(W/H)² |
| Hume (1966) | 0.3281W + 0.33929H − 29.5336 | 0.29569W + 0.41813H − 43.2933 |

W is weight in kg and H is height in cm. The James formula becomes unreliable at high body weights.

## LBM from body fat percentage

If you know your body fat percentage, from a scan or the [body fat calculator](/health/body-fat/):

<p class="formula">LBM = Weight × (1 − body fat %)</p>

This is usually more accurate than height-and-weight formulas, especially for very muscular or very lean people.

## Protein by lean mass

Some coaches set protein targets per kilogram of lean mass, often 1.6–2.2 g/kg of LBM for people doing regular strength training. See the [protein intake calculator](/health/protein-intake/).
''', [
 ('Is lean body mass the same as muscle mass?', 'No. Lean body mass includes muscle, bones, organs, skin and water. Muscle is roughly half of it.'),
 ('Can I increase my lean body mass?', 'Yes, mainly by building muscle through regular strength training, enough protein and adequate sleep.'),
], before='## Using your result')

# ---------------- macros
rows = ''.join(f"| {c} | {c*.3/4:.0f} g | {c*.4/4:.0f} g | {c*.3/9:.0f} g |\n" for c in [1500, 1800, 2000, 2200, 2500, 2800, 3000])
expand('health/macros', f'''
## Grams per day at a 30/40/30 split

| Calories | Protein (30%) | Carbs (40%) | Fat (30%) |
|---|---|---|---|
{rows}
## Recommended ranges

The US National Academies give these acceptable ranges for adults:

| Macronutrient | Share of calories |
|---|---|
| Carbohydrate | 45–65% |
| Fat | 20–35% |
| Protein | 10–35% |

Higher-protein plans (25–35%) are popular for weight loss and muscle gain because protein is filling and helps keep muscle.

## Good sources of each macro

- **Protein**: eggs, dairy, fish, chicken, lentils, beans, tofu, paneer.
- **Carbohydrate**: whole grains, oats, rice, fruit, vegetables, legumes.
- **Fat**: nuts, seeds, olive oil, avocado, oily fish.

Choose mostly whole foods. The quality of each macro matters as much as the amount.

## Fibre and alcohol

- Aim for **25–38 g of fibre** a day from vegetables, fruit, whole grains and legumes.
- Alcohol has 7 kcal per gram. If you drink, count it in your daily calories.
''', [
 ('How many grams of protein is 30% of 2,000 calories?', '600 kcal ÷ 4 = 150 g of protein a day.'),
 ('Do I need to hit my macros exactly?', 'No. Being within about 5–10 g of each target on most days is enough. Total calories and protein matter most.'),
], before='## Common splits')

# ---------------- MAP
rows = ''.join(f"| {s}/{d} | {d+(s-d)/3:.0f} | {s-d} |\n" for s, d in [(90, 60), (110, 70), (120, 80), (130, 85), (140, 90), (160, 100), (180, 110)])
expand('health/mean-arterial-pressure', f'''
## MAP for common readings

| Blood pressure (mmHg) | MAP | Pulse pressure |
|---|---|---|
{rows}
## Why doctors watch MAP

MAP reflects the average pressure pushing blood into organs during a whole heartbeat. If it falls too low, the brain, kidneys and heart may not get enough blood:

- **Below about 60–65 mmHg**: organs may be under-perfused. In intensive care, a target of 65 mmHg is common for people with septic shock.
- **70–100 mmHg**: typical range for healthy adults.
- **Persistently high**: reflects high blood pressure, which strains the heart and arteries over time.

## Pulse pressure

Pulse pressure is the difference between the top and bottom numbers. In older adults, a wide pulse pressure (often above 60 mmHg) can be a sign of stiff arteries.

## Measuring blood pressure at home

- Sit quietly for 5 minutes, back supported, feet flat.
- Rest your arm at heart level. Use the correct cuff size.
- Take 2–3 readings a minute apart and average them.
- Avoid caffeine, exercise and smoking for 30 minutes beforehand.
''', [
 ('Is the MAP formula exact?', 'It is an estimate. At rest the heart spends about two-thirds of each beat in diastole, which is why diastolic pressure counts twice. At fast heart rates the estimate is less accurate.'),
 ('What MAP is too low?', 'A MAP below about 60–65 mmHg may not supply enough blood to the organs. Seek medical help if low readings come with dizziness or fainting.'),
])

# ---------------- pack years
rows = ''.join(f"| {c} | {c/20:.2g} | {c/20*10:.0f} | {c/20*20:.0f} | {c/20*30:.0f} |\n" for c in [5, 10, 15, 20, 30, 40])
expand('health/pack-years', f'''
## Pack-years table

| Cigarettes a day | Packs a day | 10 years | 20 years | 30 years |
|---|---|---|---|---|
{rows}
## If your smoking changed over time

Add up each period separately. Someone who smoked 10 a day for 10 years and then 20 a day for 15 years has 5 + 15 = **20 pack-years**.

## Other tobacco

Pack-years are defined for cigarettes. For bidis, cigars or pipes, doctors may convert using rough equivalents, but there is no single standard. Mention all tobacco use to your doctor, including chewing tobacco, which carries its own risks for mouth cancer.

## Benefits of quitting

Health benefits start soon after the last cigarette and keep growing:

| Time after quitting | Change |
|---|---|
| Weeks to months | Circulation and lung function begin to improve |
| 1 year | Risk of heart disease is about half that of a smoker |
| 5–10 years | Risk of mouth, throat and bladder cancer drops sharply |
| 10 years | Risk of dying from lung cancer is about half that of a smoker |

Stop-smoking services, nicotine replacement and prescription medicines can double or triple your chance of quitting.
''', [
 ('Is 20 pack-years a lot?', 'It is the threshold the US Preventive Services Task Force uses to recommend annual lung cancer screening for people aged 50–80 who smoke or quit within the last 15 years.'),
 ('Do e-cigarettes count towards pack-years?', 'No. Pack-years measure cigarette smoking. Tell your doctor about vaping separately.'),
])

# ---------------- protein intake
rows = ''.join(f"| {m} kg | {m*0.8:.0f} g | {m*1.2:.0f} g | {m*1.6:.0f} g | {m*2.0:.0f} g |\n" for m in [50, 60, 70, 80, 90, 100])
expand('health/protein-intake', f'''
## Daily protein by weight and goal

| Body weight | Minimum (0.8 g/kg) | Older adults (1.2 g/kg) | Strength training (1.6 g/kg) | Fat loss, high end (2.0 g/kg) |
|---|---|---|---|---|
{rows}
## Who needs more protein

- **Older adults** (65+): 1.0–1.2 g/kg helps slow age-related muscle loss.
- **People doing strength training**: about 1.6 g/kg is enough for most; benefits level off above that.
- **During weight loss**: 1.6–2.2 g/kg helps keep muscle while eating less.
- **Pregnancy and breastfeeding**: needs rise. Follow your doctor's advice.

People with kidney disease may need to **limit** protein — ask a doctor or dietitian.

## Plant-based protein

Vegetarians and vegans can meet their needs by mixing sources through the day: lentils, chickpeas, beans, soy, tofu, tempeh, seitan, dairy, nuts and seeds. Combining grains and legumes, such as rice with dal, improves the amino acid balance.

## A day at 120 g of protein

- Breakfast: 3 eggs and a glass of milk — about 26 g
- Lunch: 150 g chicken or 200 g paneer with rice — about 40 g
- Snack: Greek yoghurt and a handful of nuts — about 20 g
- Dinner: 150 g fish or 1.5 cups of cooked lentils with vegetables — about 30 g
''', [
 ('Is 0.8 g/kg enough?', 'It prevents deficiency for most healthy adults, but active people, older adults and those losing weight often benefit from more.'),
 ('Do I need protein powder?', 'No. It is a convenient option, but food can provide all the protein you need.'),
])

# ---------------- steps to distance
rows = ''.join(f"| {h} cm | {0.414*h:.0f} cm | {0.414*h/100*10000/1000:.1f} km | {10000*0.414*h/100/1609.344:.1f} mi | {1000/(0.414*h/100):.0f} |\n" for h in [150, 160, 170, 180, 190])
expand('health/steps-to-distance', f'''
## 10,000 steps by height

| Height | Step length | Distance | Miles | Steps per km |
|---|---|---|---|---|
{rows}
Running strides are longer — often 1.2–1.5 times walking step length — so you cover more distance per step when you run.

## Steps and walking pace

| Pace | Steps per minute (approx.) | Intensity |
|---|---|---|
| Slow stroll | 60–80 | Light |
| Normal walk | 90–100 | Light to moderate |
| Brisk walk | 100–120 | Moderate |
| Very brisk / power walk | 120–140 | Vigorous for many people |

About **100 steps per minute** is a widely used marker for moderate-intensity walking in adults.

## How many steps do you need?

Large studies, including a 2022 meta-analysis in *The Lancet Public Health*, found that the risk of early death fell as daily steps increased, levelling off at around **6,000–8,000 steps** for adults over 60 and **8,000–10,000** for younger adults. Any increase from a low base helps.

## Ways to add steps

- Walk during phone calls.
- Take the stairs for short trips.
- Get off one stop early or park further away.
- A 10-minute walk after meals adds about 1,000 steps each time.
''', [
 ('How many steps are in a mile?', 'About 2,000–2,500 walking steps for most adults, depending on height and pace.'),
 ('How many steps are in a kilometre?', 'About 1,300–1,500 walking steps for most adults.'),
], before='## Measure your own step length')

# ---------------- VO2 max
rows = ''.join(f"| {d:,} m ({d/1609.344:.2f} mi) | {(d-504.9)/44.73:.1f} |\n" for d in [1600, 2000, 2200, 2400, 2600, 2800, 3000, 3200])
expand('health/vo2-max', f'''
## Cooper test results

| Distance in 12 minutes | Estimated VO₂ max (ml/kg/min) |
|---|---|
{rows}
## Other ways to estimate VO₂ max

| Method | How it works |
|---|---|
| Lab treadmill or cycle test | Measures oxygen use directly — the gold standard |
| Resting heart rate method | VO₂ max ≈ 15.3 × (max HR ÷ resting HR) (Uth et al., 2004) |
| Rockport walk test | Time and heart rate after walking 1 mile |
| Smartwatch estimates | Use heart rate during runs; accuracy varies by device |

For example, with a max heart rate of 180 and a resting heart rate of 60, the resting method gives 15.3 × 3 = 45.9 ml/kg/min.

## Why VO₂ max matters

VO₂ max is one of the strongest predictors of long-term health. Higher cardiorespiratory fitness is linked with lower risk of heart disease and early death in large studies. Moving from the lowest fitness group to the next one up gives a large part of the benefit.

## VO₂ max and age

VO₂ max typically declines by about 10% per decade after age 30 in inactive people. Regular endurance training can slow this considerably, and many active 60-year-olds have the fitness of inactive 40-year-olds.
''', [
 ('Can I take the Cooper test on a treadmill?', 'Yes. Set the incline to 1% to mimic outdoor running and run as far as you can in 12 minutes.'),
 ('How quickly can VO₂ max improve?', 'Untrained people often see a 10–20% improvement in 2–3 months of regular aerobic training.'),
], before='## Improving VO₂ max')

# ---------------- waist to height
rows = ''.join(f"| {h} cm ({int(h/2.54//12)}′{round(h/2.54%12)}″) | below {h*0.5:.0f} cm ({h*0.5/2.54:.1f} in) | {h*0.5:.0f}–{h*0.6:.0f} cm | {h*0.6:.0f} cm or more |\n" for h in [150, 160, 170, 180, 190])
expand('health/waist-to-height', f'''
## Healthy waist size by height

| Height | Healthy | Increased risk | High risk |
|---|---|---|---|
{rows}
The cut-offs of 0.5 and 0.6 follow the 2022 NICE guideline in the UK, which advises adults to keep their waist to less than half their height.

## Why waist size matters

Fat stored around the abdomen (visceral fat) is linked with type 2 diabetes, high blood pressure and heart disease, even in people with a normal BMI. Waist-to-height ratio captures this, and it works across different ethnic groups and for both men and women.

## Waist-to-height for children

The same 0.5 boundary is often used for children over 5, which makes it simpler than BMI percentiles. Measure in the same way and ask your doctor if the ratio is above 0.5.

## Reducing your ratio

- Regular aerobic activity and strength training reduce abdominal fat.
- Cutting back on sugary drinks, refined carbohydrates and alcohol helps.
- Sleep and stress also affect where fat is stored.

Re-measure every 4–6 weeks, at the same time of day.
''', [
 ('What is the waist-to-height ratio for a 5′6″ person?', 'Height 168 cm, so keep your waist below 84 cm (33 inches) for a ratio under 0.5.'),
 ('Should I measure over clothing?', 'No. Measure on bare skin, midway between the lowest rib and the top of the hip bone, after breathing out normally.'),
], before='## Categories')

# ---------------- waist to hip
rows = ''.join(f"| {w} cm | {w/hp:.2f} |" + ''.join('' for _ in [0]) + "\n" for w, hp in [])
expand('health/waist-to-hip', '''
## Waist-to-hip ratio table

| Waist ↓ / Hips → | 90 cm | 95 cm | 100 cm | 105 cm | 110 cm |
|---|---|---|---|---|---|
''' + ''.join(f"| {w} cm | " + ' | '.join(f"{w/h:.2f}" for h in [90, 95, 100, 105, 110]) + " |\n" for w in [70, 75, 80, 85, 90, 95, 100]) + '''
Above 0.90 for men or 0.85 for women indicates substantially increased risk, according to the WHO.

## Waist size alone

The WHO also gives waist circumference thresholds:

| | Increased risk | Substantially increased risk |
|---|---|---|
| Men (European) | above 94 cm | above 102 cm |
| Women (European) | above 80 cm | above 88 cm |
| Men (South Asian) | above 90 cm | — |
| Women (South Asian) | above 80 cm | — |

Ethnic-specific thresholds come from the International Diabetes Federation.

## Which measure is best?

| Measure | Strength |
|---|---|
| BMI | Simple, widely used, but ignores fat distribution |
| Waist circumference | Easy, captures abdominal fat |
| Waist-to-hip ratio | Shows body shape (apple vs pear) |
| [Waist-to-height ratio](/health/waist-to-height/) | Works across heights, sexes and ethnic groups |

Using two of these together gives a better picture than any one alone.
''', [
 ('Is a waist-to-hip ratio of 0.8 good?', 'Yes for women (below 0.85) and well within the healthy range for men (below 0.90).'),
 ('Can the ratio be healthy if both waist and hips are large?', 'Yes, which is why waist size on its own and BMI are also worth checking.'),
], before='## How to measure')

# ---------------- water intake
rows = ''.join(f"| {m} kg | {0.033*m:.1f} L | {0.033*m+0.35:.1f} L | {0.033*m+0.7:.1f} L |\n" for m in [50, 60, 70, 80, 90, 100])
expand('health/water-intake', f'''
## Daily water by weight

| Body weight | No exercise | 30 min exercise | 60 min exercise |
|---|---|---|---|
{rows}
## Official recommendations

These figures are for **total water**, from both drinks and food:

| Source | Women | Men |
|---|---|---|
| European Food Safety Authority | 2.0 L/day | 2.5 L/day |
| US National Academies | 2.7 L/day | 3.7 L/day |

Food usually supplies about 20% of total water, so the amount you need to drink is lower.

## Signs of dehydration

- Dark yellow urine or not urinating often
- Thirst, dry mouth, headache
- Tiredness, dizziness or poor concentration

Older adults may not feel thirsty even when they need fluids, so regular drinking matters more with age.

## When to be careful

People with heart failure or kidney disease may be told to **limit** fluids. Drinking very large amounts in a short time can cause low blood sodium (hyponatraemia), especially during long endurance events. Follow medical advice if you have a condition that affects fluid balance.
''', [
 ('Do tea and coffee count towards water intake?', 'Yes. The mild diuretic effect of caffeine does not cancel out the water in tea and coffee for regular drinkers.'),
 ('How much water should I drink in hot weather?', 'More than usual — often an extra 0.5–1 L a day, or more if you sweat heavily. Let thirst and urine colour guide you.'),
], before='## A simple check')

# ---------------- weight loss time
rows = ''.join(f"| {d} kcal | {d*7/7700:.2f} kg | {d*7/7700*2.2046:.1f} lb | {5/(d*7/7700):.0f} weeks |\n" for d in [250, 300, 500, 750, 1000])
expand('health/weight-loss-time', f'''
## Weekly loss by daily deficit

| Daily deficit | Loss per week | In pounds | Weeks to lose 5 kg |
|---|---|---|---|
{rows}
These use the common estimate of 7,700 kcal per kilogram of body fat.

## Why the scale doesn't follow the maths exactly

- **Water weight**: early loss is often faster because stored carbohydrate holds water.
- **Metabolic adaptation**: as you lose weight, you need fewer calories, so the same intake gives a smaller deficit.
- **Daily swings**: salt, hormones and meals can move the scale by 1–2 kg from day to day.

Track the **weekly average** rather than single weigh-ins.

## Finding your deficit

1. Estimate your daily needs with the [BMR and TDEE calculator](/health/bmr/).
2. Subtract a moderate amount, usually 300–500 kcal.
3. Re-check every few weeks, because your TDEE drops as your weight does.

## Keeping it off

Most weight is regained when people return to old habits. Gradual changes you can live with — more vegetables and protein, fewer sugary drinks, regular activity and enough sleep — work better long term than strict diets.
''', [
 ('How long does it take to lose 10 kg?', 'At a 500 kcal daily deficit, about 22 weeks (5 months) on paper. Real progress is often slower as the body adapts.'),
 ('Is it better to eat less or exercise more?', 'Both help. Eating less creates most of the deficit for most people, while exercise protects muscle, improves health and helps maintain weight loss.'),
], before='## Important')

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/health/*.mdx')):
    c = 'health/' + os.path.basename(p)[:-4]; print(c, words(c))
