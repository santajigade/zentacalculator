import math
from page import page
C='other'; U='updated: 2026-10-27'

page(C,'dog-age',f'''
title: Dog Age Calculator (Dog Years to Human Years)
description: Convert your dog's age to human years using the modern DNA-based formula — and compare with the old "×7" rule.
category: other
keywords: [dog age calculator, dog years to human years, how old is my dog, dog age in human years, puppy age]
{U}
featured: true
variables:
  - {{ id: a, label: Dog's age, suffix: years, default: 5, min: 0.1, max: 25 }}
  - {{ id: h, label: Human-equivalent age (DNA formula), suffix: years, min: 0, decimals: 0 }}
  - {{ id: h7, label: Old "× 7" rule, suffix: years, min: 0, decimals: 0 }}
equations:
  - h = 16 * ln(a) + 31
  - h7 = a * 7
faq:
  - q: Is one dog year really seven human years?
    a: No. Dogs mature very quickly in their first two years, then age more slowly. The 7:1 rule is a rough myth.
  - q: Where does the formula come from?
    a: From a 2020 study in Cell Systems comparing DNA methylation ("epigenetic clocks") in Labrador retrievers and humans — human age ≈ 16 ln(dog age) + 31.
  - q: Do big dogs age faster?
    a: Yes — large breeds generally have shorter lifespans, so they "age" faster in later life than small breeds.
related: [other/cat-age, other/dog-food-calories, everyday-life/age-calculator]
''',f'''
## How to use this calculator

Enter your dog's **age in years** (decimals allowed — 6 months = 0.5). The human-equivalent age using the DNA-based formula is shown, plus the old ×7 rule for comparison.

## Formula

<p class="formula">human age ≈ 16 × ln(dog age) + 31</p>

## Comparison

| Dog age | DNA formula | ×7 rule |
|---|---|---|
| 1 | {16*math.log(1)+31:.0f} | 7 |
| 2 | {16*math.log(2)+31:.0f} | 14 |
| 5 | {16*math.log(5)+31:.0f} | 35 |
| 10 | {16*math.log(10)+31:.0f} | 70 |
| 14 | {16*math.log(14)+31:.0f} | 98 |

The formula was derived from Labradors and is less reliable for puppies under about 1 year.
''')

page(C,'cat-age',f'''
title: Cat Age Calculator (Cat Years to Human Years)
description: Convert your cat's age into human years using the widely used veterinary guideline.
category: other
keywords: [cat age calculator, cat years to human years, how old is my cat, cat age in human years, kitten age]
{U}
variables:
  - {{ id: a, label: Cat's age, suffix: years, default: 8, min: 0, max: 30 }}
  - {{ id: h, label: Human-equivalent age, suffix: years, min: 0, decimals: 0 }}
equations:
  - h = 15 * min(a, 1) + 9 * max(0, min(a, 2) - 1) + 4 * max(0, a - 2)
faq:
  - q: How do you convert cat years to human years?
    a: A common guideline is 15 human years for the first year, 9 more for the second, then about 4 human years for each cat year after that.
  - q: When is a cat considered senior?
    a: Many vets consider cats senior from about 11 years (around 60 in human terms) and geriatric from about 15.
  - q: Do indoor cats live longer?
    a: On average, yes — indoor cats often live 12–18 years or more.
related: [other/dog-age, everyday-life/age-calculator]
''',f'''
## How to use this calculator

Enter your cat's **age in years**. The human-equivalent age is calculated.

## The guideline

- First year = 15 human years
- Second year = +9 (24 at age 2)
- Each year after = +4

## Examples

| Cat age | Human age |
|---|---|
| 1 | 15 |
| 2 | 24 |
| 5 | 36 |
| 8 | 48 |
| 12 | 64 |
| 16 | 80 |

Based on guidelines from the American Animal Hospital Association and International Cat Care.
''')

page(C,'due-date',f'''
title: Pregnancy Due Date Calculator
description: Estimate your baby's due date and how many weeks pregnant you are from the first day of your last period.
category: other
keywords: [due date calculator, pregnancy calculator, how many weeks pregnant, estimated due date, naegele rule, lmp]
{U}
featured: true
variables:
  - {{ id: lmp, label: First day of last menstrual period, family: date, default: -70 }}
  - {{ id: cyc, label: Average cycle length, suffix: days, default: 28, min: 20, max: 45 }}
  - {{ id: today, label: Today, family: date, default: 0 }}
  - {{ id: due, label: Estimated due date, family: date }}
  - {{ id: wk, label: Weeks pregnant today, min: 0, decimals: 1 }}
  - {{ id: left, label: Days until due date, decimals: 0 }}
equations:
  - due = lmp + 280 + (cyc - 28)
  - wk = (today - lmp - (cyc - 28)) / 7
  - left = due - today
faq:
  - q: How is the due date calculated?
    a: By Naegele's rule — 280 days (40 weeks) after the first day of the last period, adjusted for cycles longer or shorter than 28 days.
  - q: How accurate is it?
    a: Only about 4–5% of babies arrive on their due date; most are born within two weeks either side. An early ultrasound gives a more accurate date.
  - q: Why count from the last period, not conception?
    a: The period date is usually known. Conception typically happens about two weeks later, so you are counted as "2 weeks pregnant" at conception.
related: [other/ovulation, everyday-life/days-until]
''','''
## How to use this calculator

Choose the **first day of your last period** and your average **cycle length**. Your estimated due date, how many weeks pregnant you are today, and the days remaining are calculated.

## Formula (Naegele's rule)

<p class="formula">Due date = LMP + 280 days + (cycle length − 28)</p>

## Trimesters

| Trimester | Weeks |
|---|---|
| First | 1–13 |
| Second | 14–27 |
| Third | 28–40 |

This tool gives an estimate only. Your doctor or midwife will confirm your due date, usually with an ultrasound scan.
''')

page(C,'ovulation',f'''
title: Ovulation & Fertile Window Calculator
description: Estimate your ovulation date, fertile window and next period from your last period and cycle length.
category: other
keywords: [ovulation calculator, fertile window, when do i ovulate, fertile days, next period, cycle calculator]
{U}
variables:
  - {{ id: lmp, label: First day of last period, family: date, default: -5 }}
  - {{ id: cyc, label: Average cycle length, suffix: days, default: 28, min: 20, max: 45 }}
  - {{ id: ov, label: Estimated ovulation day, family: date }}
  - {{ id: fs, label: Fertile window starts, family: date }}
  - {{ id: fe, label: Fertile window ends, family: date }}
  - {{ id: np, label: Next period expected, family: date }}
equations:
  - np = lmp + cyc
  - ov = np - 14
  - fs = ov - 5
  - fe = ov + 1
faq:
  - q: When does ovulation happen?
    a: About 14 days before the next period starts — day 14 of a 28-day cycle, but later in longer cycles.
  - q: What is the fertile window?
    a: About six days — the five days before ovulation and the day of ovulation (plus a day after as a margin), because sperm can survive several days.
  - q: Can I use this for contraception?
    a: No. Cycle-based estimates are not reliable enough to prevent pregnancy.
related: [other/due-date, everyday-life/date-plus-days]
''','''
## How to use this calculator

Choose the **first day of your last period** and your **average cycle length**. Your estimated ovulation date, fertile window and next period are shown.

## How it works

<p class="formula">Next period = LMP + cycle length   Ovulation ≈ next period − 14 days</p>

Cycles vary month to month, so these dates are estimates. Ovulation tests or tracking basal body temperature can give a more personal picture. Speak to a doctor if your cycles are very irregular.
''')

page(C,'password-strength',f'''
title: Password Strength (Entropy) Calculator
description: Calculate password entropy in bits and estimate how long it would take to crack by brute force.
category: other
keywords: [password strength, password entropy, how long to crack password, brute force time, strong password]
{U}
featured: true
variables:
  - {{ id: L, label: Password length, suffix: characters, default: 12, min: 1 }}
  - id: N
    label: Character set
    default: 94
    options:
      - {{ label: Digits only (10), value: 10 }}
      - {{ label: Lowercase letters (26), value: 26 }}
      - {{ label: Upper + lowercase (52), value: 52 }}
      - {{ label: Letters + digits (62), value: 62 }}
      - {{ label: All printable ASCII (94), value: 94 }}
  - {{ id: gps, label: Attacker guesses per second, default: 10000000000, min: 1 }}
  - {{ id: bits, label: Entropy, suffix: bits, min: 0, decimals: 1 }}
  - {{ id: yrs, label: Average time to crack, family: time, unit: yr, min: 0 }}
equations:
  - bits = L * log2(N)
  - yrs = 2^(bits - 1) / gps / 31557600
faq:
  - q: What is password entropy?
    a: A measure of unpredictability in bits — log₂ of the number of possible passwords. Each extra bit doubles the guesses needed.
  - q: How long should a password be?
    a: At least 12–16 characters for important accounts. A passphrase of several random words is long and easy to remember.
  - q: Does this apply to any password?
    a: Only to truly random passwords. Real passwords based on words, names or patterns are cracked far faster.
related: [other/data-storage-converter]
''','''
## How to use this calculator

Enter the **length**, choose the **character set**, and set the attacker's **guessing speed** (10 billion per second is a strong offline attack on a fast hash). Entropy and average cracking time are calculated.

## Formulas

<p class="formula">bits = length × log₂(character set)<br/>average time = 2<sup>bits − 1</sup> ÷ guesses per second</p>

## Examples (10 billion guesses per second)

| Password | Bits | Average time |
|---|---|---|
| 8 digits | 26.6 | under a second |
| 8 lowercase | 37.6 | about 10 seconds |
| 12 letters + digits | 71.5 | thousands of years |
| 16 printable ASCII | 104.9 | far longer than the age of the universe |

Use a password manager, unique passwords for every site and two-factor authentication.
''')

page(C,'download-time',f'''
title: Download Time Calculator
description: Estimate how long a file takes to download or upload at a given internet speed (Mbps).
category: other
keywords: [download time calculator, upload time, internet speed, mbps to mb/s, file transfer time, bandwidth]
{U}
variables:
  - {{ id: s, label: File size, family: data, unit: GB, default: 5, min: 0 }}
  - {{ id: sp, label: Connection speed, suffix: Mbps, default: 100, min: 0.0001 }}
  - {{ id: ef, label: Real-world efficiency, family: percent, unit: '%', default: 90, min: 0.01, max: 1 }}
  - {{ id: t, label: Time, family: seconds, unit: min, min: 0 }}
  - {{ id: mbs, label: Effective speed, suffix: MB/s, min: 0, decimals: 2 }}
equations:
  - t = s * 8 / (sp * 1000000 * ef)
  - mbs = sp * ef / 8
faq:
  - q: What is the difference between Mbps and MB/s?
    a: Mbps is megabits per second; MB/s is megabytes per second. There are 8 bits in a byte, so 100 Mbps ≈ 12.5 MB/s.
  - q: Why is my download slower than my plan?
    a: Network overheads, Wi-Fi, server speed and other users all reduce real throughput. 80–90% of the plan is typical on a good wired connection.
  - q: How long does a 50 GB game take on 100 Mbps?
    a: About 74 minutes at 90% efficiency.
related: [other/data-storage-converter, other/video-file-size]
''','''
## How to use this calculator

Enter the **file size**, your **connection speed** in Mbps, and a **real-world efficiency**. The transfer time and effective speed are calculated.

## Formula

<p class="formula">time = size (bits) ÷ (speed × efficiency)</p>

## Example

A 5 GB file on a 100 Mbps connection at 90%: 40,000 Mb ÷ 90 Mbps = **444 s ≈ 7.4 minutes** (11.25 MB/s).
''')

page(C,'video-file-size',f'''
title: Video File Size Calculator (Bitrate)
description: Calculate video file size from bitrate and duration — or the bitrate for a target file size.
category: other
keywords: [video file size calculator, bitrate calculator, mbps video, recording size, storage for video, 4k file size]
{U}
variables:
  - {{ id: br, label: Total bitrate (video + audio), suffix: Mbps, default: 20, min: 0 }}
  - {{ id: t, label: Duration, family: seconds, unit: min, default: 60, min: 0 }}
  - {{ id: s, label: File size, family: data, unit: GB, min: 0 }}
equations:
  - s = br * 1000000 * t / 8
faq:
  - q: How do I calculate video file size?
    a: File size = bitrate × duration ÷ 8. One hour at 20 Mbps is about 9 GB.
  - q: What bitrate should I use?
    a: Common streaming targets are about 5–8 Mbps for 1080p and 15–25 Mbps for 4K (H.264); HEVC needs roughly half.
  - q: How long can I record on a 128 GB card?
    a: Press × on Duration and type 128 GB as the file size.
related: [other/download-time, other/data-storage-converter]
''','''
## How to use this calculator

Enter the **bitrate** in Mbps and the **duration**. The file size is calculated. Or enter a storage size to find the recording time.

## Formula

<p class="formula">size (bytes) = bitrate (bits/s) × seconds ÷ 8</p>

## Example

60 minutes at 20 Mbps: 20 × 3,600 ÷ 8 = 9,000 MB = **9 GB**.
''')

page(C,'screen-ppi',f'''
title: Screen PPI Calculator (Pixel Density)
description: Calculate pixels per inch (PPI) and dot pitch of a screen from its resolution and diagonal size.
category: other
keywords: [ppi calculator, pixel density, pixels per inch, screen resolution, dot pitch, retina display]
{U}
variables:
  - {{ id: w, label: Horizontal resolution, suffix: px, default: 2560, min: 1 }}
  - {{ id: h, label: Vertical resolution, suffix: px, default: 1440, min: 1 }}
  - {{ id: d, label: Diagonal, family: length, unit: in, default: 27, min: 0 }}
  - {{ id: ppi, label: Pixel density, suffix: PPI, min: 0, decimals: 1 }}
  - {{ id: pitch, label: Dot pitch, family: length, unit: mm, min: 0 }}
equations:
  - ppi = sqrt(w^2 + h^2) / (d / 0.0254)
  - pitch = 0.0254 / ppi
faq:
  - q: How is PPI calculated?
    a: PPI = √(width² + height²) ÷ diagonal in inches.
  - q: What PPI looks sharp?
    a: For a desktop monitor viewed at arm's length, about 110 PPI and above looks sharp; phones held closer often exceed 400 PPI.
  - q: What is dot pitch?
    a: The distance between pixels — the reciprocal of PPI.
related: [everyday-life/tv-size, other/aspect-ratio]
''','''
## How to use this calculator

Enter the screen's **resolution** and **diagonal**. Pixel density and dot pitch are calculated.

## Formula

<p class="formula">PPI = √(w² + h²) ÷ diagonal</p>

## Common screens

| Screen | PPI |
|---|---|
| 24″ 1080p | 91.8 |
| 27″ 1440p | 108.8 |
| 27″ 4K | 163.2 |
| 32″ 4K | 137.7 |
| 6.1″ 2532 × 1170 phone | 457.5 |
''')

page(C,'aspect-ratio',f'''
title: Aspect Ratio Calculator
description: Resize images and video while keeping the aspect ratio — find the missing width or height.
category: other
keywords: [aspect ratio calculator, resize image, 16:9 calculator, width height ratio, video dimensions, resolution scaling]
{U}
variables:
  - {{ id: rw, label: Ratio width, default: 16, min: 0.0001 }}
  - {{ id: rh, label: Ratio height, default: 9, min: 0.0001 }}
  - {{ id: w, label: New width, suffix: px, default: 1280, min: 0 }}
  - {{ id: h, label: New height, suffix: px, min: 0, decimals: 0 }}
equations:
  - w / h = rw / rh
faq:
  - q: How do I keep the aspect ratio when resizing?
    a: New height = new width × (ratio height ÷ ratio width). For 16:9 at 1,280 px wide, height = 720 px.
  - q: What are common aspect ratios?
    a: 16:9 for video and monitors, 4:3 for older screens and many photos, 3:2 for DSLR photos, 1:1 for square posts and 9:16 for vertical video.
  - q: Can I enter the original pixel size as the ratio?
    a: Yes — enter, for example, 1920 and 1080 as the ratio values.
related: [other/screen-ppi, other/print-size-dpi]
''','''
## How to use this calculator

Enter the **ratio** (or the original width and height in pixels) and either the **new width** or the **new height**. The missing dimension is calculated.

## Common sizes

| Ratio | Sizes |
|---|---|
| 16:9 | 1280×720, 1920×1080, 3840×2160 |
| 4:3 | 1024×768, 1600×1200 |
| 3:2 | 1080×720, 6000×4000 |
| 9:16 | 1080×1920 (stories, reels) |
''')

page(C,'grade-percentage',f'''
title: Test Score & Grade Percentage Calculator
description: Convert a test score to a percentage — and find the letter grade on a typical scale.
category: other
keywords: [grade calculator, test score percentage, marks to percentage, score out of, percentage grade]
{U}
variables:
  - {{ id: s, label: Score (points earned), default: 42, min: 0 }}
  - {{ id: tot, label: Total points possible, default: 50, min: 0.0001 }}
  - id: p
    label: Percentage
    family: percent
    unit: '%'
    min: 0
    bands:
      - {{ max: 0.5999, label: F (below 60%), color: '#dc2626' }}
      - {{ max: 0.6999, label: D (60–69%), color: '#f97316' }}
      - {{ max: 0.7999, label: C (70–79%), color: '#eab308' }}
      - {{ max: 0.8999, label: B (80–89%), color: '#3b82f6' }}
      - {{ max: 100, label: A (90%+), color: '#16a34a' }}
equations:
  - p = s / tot
faq:
  - q: How do I convert marks to a percentage?
    a: Divide the score by the total and multiply by 100. 42 out of 50 is 84%.
  - q: Which grading scale is used?
    a: The common US 10-point scale (A 90+, B 80–89, C 70–79, D 60–69). Your school's scale may differ.
  - q: How many marks do I need for a target?
    a: Press × on Score and type the percentage you want.
related: [everyday-life/grade-needed, math/percentage]
''','''
## How to use this calculator

Enter the **score** and the **total possible**. The percentage and letter grade are shown.

## Formula

<p class="formula">percentage = score ÷ total × 100</p>

## Example

42 out of 50 = **84%** → **B** on a 10-point scale.
''')

page(C,'paper-weight-gsm',f'''
title: Paper Weight Calculator (GSM)
description: Calculate the weight of paper sheets or a ream from GSM and paper size.
category: other
keywords: [gsm calculator, paper weight, ream weight, a4 paper weight, paper gsm to kg, printing paper]
{U}
variables:
  - id: area
    label: Paper size
    default: 0.06237
    options:
      - {{ label: A4 (210 × 297 mm), value: 0.06237 }}
      - {{ label: A3 (297 × 420 mm), value: 0.12474 }}
      - {{ label: A5 (148 × 210 mm), value: 0.03108 }}
      - {{ label: US Letter (8.5 × 11 in), value: 0.060322 }}
      - {{ label: US Legal (8.5 × 14 in), value: 0.076774 }}
      - {{ label: A0 (1 m²), value: 0.999949 }}
  - {{ id: gsm, label: Paper weight, suffix: g/m² (GSM), default: 80, min: 0 }}
  - {{ id: n, label: Number of sheets, default: 500, min: 0 }}
  - {{ id: w1, label: Weight per sheet, family: mass, unit: g, min: 0 }}
  - {{ id: wt, label: Total weight, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - w1 = gsm * area / 1000
  - wt = w1 * n
faq:
  - q: What does GSM mean?
    a: Grams per square metre — the weight of one square metre of the paper.
  - q: How much does a ream of A4 80 GSM weigh?
    a: About 2.5 kg (500 sheets × 4.99 g).
  - q: What GSM is typical?
    a: 70–90 GSM for office paper, 120–170 for brochures and flyers, 250–350 for business cards.
related: [other/print-size-dpi]
''','''
## How to use this calculator

Choose the **paper size**, enter the **GSM** and the **number of sheets**. The weight per sheet and total weight are calculated — useful for postage and shipping.

## Formula

<p class="formula">weight = GSM × sheet area × sheets</p>

## Example

A ream of A4 at 80 GSM: 80 × 0.06237 = 4.99 g per sheet → **2.49 kg** per 500 sheets.
''')

page(C,'print-size-dpi',f'''
title: Print Size Calculator (Pixels & DPI)
description: Calculate the maximum print size of an image from its pixel dimensions and print resolution (DPI/PPI).
category: other
keywords: [print size calculator, dpi calculator, pixels to inches, print resolution, 300 dpi, photo print size]
{U}
variables:
  - {{ id: px, label: Image width, suffix: px, default: 6000, min: 0 }}
  - {{ id: py, label: Image height, suffix: px, default: 4000, min: 0 }}
  - {{ id: dpi, label: Print resolution, suffix: DPI, default: 300, min: 1 }}
  - {{ id: w, label: Print width, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: h, label: Print height, family: length, unit: cm, imperialUnit: in, min: 0 }}
  - {{ id: mp, label: Megapixels, min: 0, decimals: 1 }}
equations:
  - w = px / dpi * 0.0254
  - h = py / dpi * 0.0254
  - mp = px * py / 1000000
faq:
  - q: What DPI should I print at?
    a: 300 DPI for high-quality photo prints viewed up close; 150–200 DPI is often fine for larger prints viewed from further away.
  - q: How big can I print a 24 MP photo?
    a: A 6,000 × 4,000 pixel image prints at about 50.8 × 33.9 cm (20 × 13.3 in) at 300 DPI.
  - q: Are DPI and PPI the same?
    a: They are often used interchangeably. Strictly, PPI is image pixels per inch and DPI is printer ink dots per inch.
related: [other/aspect-ratio, other/screen-ppi]
''','''
## How to use this calculator

Enter the image's **pixel dimensions** and the **print resolution**. The print size and megapixels are calculated. Or enter a print size to find the required pixels.

## Formula

<p class="formula">print size (in) = pixels ÷ DPI</p>

## Example

6,000 × 4,000 px at 300 DPI → **50.8 × 33.9 cm** (20 × 13.3 in), 24 MP.
''')

page(C,'battery-life',f'''
title: Battery Life Calculator
description: Estimate how long a battery will last from its capacity (mAh) and the device's current draw.
category: other
keywords: [battery life calculator, mah calculator, battery runtime, how long will battery last, power bank]
{U}
variables:
  - {{ id: cap, label: Battery capacity, suffix: mAh, default: 2000, min: 0 }}
  - {{ id: I, label: Average current draw, family: current, unit: mA, default: 50, min: 0.000001 }}
  - {{ id: ef, label: Usable capacity factor, family: percent, unit: '%', default: 85, min: 0.01, max: 1 }}
  - {{ id: t, label: Estimated runtime, family: time, unit: h, min: 0 }}
equations:
  - t = cap / 1000 * ef / I / 8766
faq:
  - q: How is battery life calculated?
    a: Runtime (hours) = capacity (mAh) ÷ current (mA), reduced by a factor for losses and the cut-off voltage.
  - q: Why use 85%?
    a: Batteries rarely deliver their full rated capacity in practice because of temperature, ageing and voltage cut-offs.
  - q: How long will a 10,000 mAh power bank charge a phone?
    a: Converter losses and voltage differences mean a typical power bank delivers about 60–70% of its rated mAh to a phone.
related: [ecology/battery-storage, other/led-resistor]
''','''
## How to use this calculator

Enter the battery **capacity** (mAh), the device's **average current** and a **usable capacity factor**. The estimated runtime is calculated.

## Formula

<p class="formula">runtime = capacity × factor ÷ current</p>

## Example

2,000 mAh at 50 mA average with 85% usable: 2,000 × 0.85 ÷ 50 = **34 hours**.
''')

page(C,'data-storage-converter',f'''
title: Data Storage Converter (KB, MB, GB, TB)
description: Convert data sizes between bytes, KB, MB, GB, TB and binary units (KiB, MiB, GiB).
category: other
keywords: [data storage converter, mb to gb, gb to tb, bytes converter, gib vs gb, file size converter]
{U}
featured: true
variables:
  - {{ id: u0, label: Gigabytes (GB), family: data, unit: GB, default: 1, min: 0 }}
  - {{ id: u1, label: Megabytes (MB), family: data, unit: MB, min: 0 }}
  - {{ id: u2, label: Terabytes (TB), family: data, unit: TB, min: 0 }}
  - {{ id: u3, label: Gibibytes (GiB), family: data, unit: GiB, min: 0 }}
  - {{ id: u4, label: Mebibytes (MiB), family: data, unit: MiB, min: 0 }}
  - {{ id: u5, label: Bytes, family: data, unit: B, min: 0 }}
equations:
  - u0 = u1
  - u1 = u2
  - u2 = u3
  - u3 = u4
  - u4 = u5
faq:
  - q: What is the difference between GB and GiB?
    a: A GB (gigabyte) is 1,000,000,000 bytes; a GiB (gibibyte) is 1,073,741,824 bytes (2³⁰).
  - q: Why does my 1 TB drive show 931 GB?
    a: Drive makers use decimal TB, while some operating systems display binary units. 1 TB = 931 GiB.
  - q: How many MB are in a GB?
    a: 1,000 MB in decimal units, or 1,024 MiB in a GiB.
related: [other/download-time, other/video-file-size]
''','''
## How to use this converter

Type a value in **any** field — decimal (KB, MB, GB, TB) or binary (KiB, MiB, GiB). Every field updates.

## Decimal vs binary

| Unit | Bytes |
|---|---|
| 1 KB | 1,000 |
| 1 KiB | 1,024 |
| 1 MB | 1,000,000 |
| 1 MiB | 1,048,576 |
| 1 GB | 1,000,000,000 |
| 1 GiB | 1,073,741,824 |

A "1 TB" drive holds 1,000,000,000,000 bytes, shown as **931 GiB** by systems that use binary units.
''')

page(C,'dog-food-calories',f'''
title: Dog Food Calorie Calculator
description: Estimate your dog's daily calorie needs from body weight and life stage — plus cups of food per day.
category: other
keywords: [dog food calculator, dog calories per day, how much to feed my dog, rer mer, dog feeding chart]
{U}
variables:
  - {{ id: m, label: Dog's weight, family: mass, unit: kg, imperialUnit: lb, default: 20, min: 0.1 }}
  - id: f
    label: Life stage / activity
    default: 1.6
    options:
      - {{ label: Neutered adult (1.6 × RER), value: 1.6 }}
      - {{ label: Intact adult (1.8 × RER), value: 1.8 }}
      - {{ label: Weight loss (1.0 × RER), value: 1.0 }}
      - {{ label: Inactive / senior (1.2 × RER), value: 1.2 }}
      - {{ label: Active / working (2–5 × RER, using 3), value: 3 }}
      - {{ label: Puppy under 4 months (3 × RER), value: 3.0001 }}
      - {{ label: Puppy 4 months to adult (2 × RER), value: 2 }}
  - {{ id: kc, label: Food energy, suffix: kcal per cup, default: 350, min: 1 }}
  - {{ id: rer, label: Resting energy requirement (RER), suffix: kcal/day, min: 0, decimals: 0 }}
  - {{ id: mer, label: Daily calories, suffix: kcal/day, min: 0, decimals: 0 }}
  - {{ id: cups, label: Cups of food per day, min: 0, decimals: 2 }}
equations:
  - rer = 70 * m^0.75
  - mer = rer * f
  - cups = mer / kc
faq:
  - q: How many calories does my dog need?
    a: Start with the resting energy requirement, RER = 70 × weight(kg)^0.75, then multiply by a factor for life stage and activity.
  - q: Where do I find kcal per cup?
    a: On the food bag or the manufacturer's website. It varies widely between brands.
  - q: Should I include treats?
    a: Treats should be no more than about 10% of daily calories — reduce meals to compensate.
related: [other/dog-age, health/bmr]
''','''
## How to use this calculator

Enter your dog's **weight**, choose the **life stage**, and enter the food's **kcal per cup**. RER, daily calories and cups per day are calculated.

## Formulas

<p class="formula">RER = 70 × kg<sup>0.75</sup>   MER = RER × factor</p>

## Example

A 20 kg neutered adult dog, food with 350 kcal per cup:

- RER = 70 × 20<sup>0.75</sup> = **662 kcal**
- Daily = 662 × 1.6 = **1,059 kcal**
- About **3.0 cups** per day

These are starting points — adjust based on body condition, and ask your vet for advice.
''')

page(C,'aquarium-volume',f'''
title: Aquarium Volume Calculator
description: Calculate fish tank volume in litres and gallons from its dimensions — plus the approximate weight when filled.
category: other
keywords: [aquarium volume calculator, fish tank litres, tank gallons, aquarium size, fish tank weight]
{U}
variables:
  - {{ id: L, label: Length, family: length, unit: cm, imperialUnit: in, default: 100, min: 0 }}
  - {{ id: W, label: Width (front to back), family: length, unit: cm, imperialUnit: in, default: 40, min: 0 }}
  - {{ id: H, label: Water height, family: length, unit: cm, imperialUnit: in, default: 45, min: 0 }}
  - {{ id: V, label: Water volume, family: volume, unit: L, imperialUnit: galUS, min: 0 }}
  - {{ id: wt, label: Weight of water, family: mass, unit: kg, imperialUnit: lb, min: 0 }}
equations:
  - V = L * W * H
  - wt = V * 1000
faq:
  - q: How do I calculate aquarium volume?
    a: Multiply length × width × water height in cm and divide by 1,000 to get litres.
  - q: How heavy is a full aquarium?
    a: Water alone weighs about 1 kg per litre; add the glass, gravel and decorations — roughly another 20–30%.
  - q: How many fish can I keep?
    a: Old "1 inch per gallon" rules are unreliable. Consider adult fish size, behaviour and filtration, and ask a specialist.
related: [construction/rectangular-tank, ecology/pond-liner]
''','''
## How to use this calculator

Enter the tank's **length**, **width** and **water height**. The volume and weight of the water are calculated.

## Example

A 100 × 40 cm tank filled to 45 cm: 100 × 40 × 45 = 180,000 cm³ = **180 litres** (47.6 US gal), weighing about **180 kg** of water.
''')

page(C,'led-resistor',f'''
title: LED Resistor Calculator
description: Calculate the series resistor needed for an LED from supply voltage, LED forward voltage and current.
category: other
keywords: [led resistor calculator, current limiting resistor, led series resistor, forward voltage, arduino led]
{U}
featured: true
variables:
  - {{ id: Vs, label: Supply voltage, family: voltage, unit: V, default: 5, min: 0 }}
  - id: Vf
    label: LED colour (typical forward voltage)
    default: 2
    options:
      - {{ label: Red (2.0 V), value: 2 }}
      - {{ label: Yellow / orange (2.1 V), value: 2.1 }}
      - {{ label: Green (2.2 V), value: 2.2 }}
      - {{ label: Blue / white (3.2 V), value: 3.2 }}
      - {{ label: Infrared (1.3 V), value: 1.3 }}
  - {{ id: I, label: LED current, family: current, unit: mA, default: 20, min: 0.000001 }}
  - {{ id: R, label: Resistor needed, family: resistance, unit: ohm, min: 0 }}
  - {{ id: P, label: Resistor power, family: power, unit: mW, min: 0 }}
equations:
  - R = (Vs - Vf) / I
  - P = (Vs - Vf) * I
faq:
  - q: How do I calculate the resistor for an LED?
    a: R = (supply voltage − LED forward voltage) ÷ LED current. For a red LED on 5 V at 20 mA, R = 3 ÷ 0.02 = 150 Ω.
  - q: Which standard resistor should I choose?
    a: Pick the next higher standard value (E12 series), which slightly reduces current and is safer.
  - q: What wattage resistor do I need?
    a: Choose a rating at least double the calculated power — a ¼ W resistor is fine for most single indicator LEDs.
related: [physics/ohms-law, other/voltage-divider]
''','''
## How to use this calculator

Enter the **supply voltage**, choose the **LED colour** and set the **current**. The resistor value and its power dissipation are calculated.

## Formula

<p class="formula">R = (V<sub>supply</sub> − V<sub>f</sub>) ÷ I</p>

## Example

Red LED (2.0 V) on 5 V at 20 mA: R = 3 ÷ 0.02 = **150 Ω**, dissipating **60 mW**.

Check your LED's datasheet for exact forward voltage and maximum current; many modern indicator LEDs are bright enough at 5–10 mA.
''')

page(C,'voltage-divider',f'''
title: Voltage Divider Calculator
description: Calculate the output voltage of a resistor voltage divider — or the resistor needed for a target output.
category: other
keywords: [voltage divider calculator, resistor divider, vout = vin r2/(r1+r2), voltage divider formula, sensor scaling]
{U}
variables:
  - {{ id: Vin, label: Input voltage, family: voltage, unit: V, default: 12, min: 0 }}
  - {{ id: R1, label: R1 (top resistor), family: resistance, unit: kohm, default: 10, min: 0 }}
  - {{ id: R2, label: R2 (bottom resistor), family: resistance, unit: kohm, default: 4.7, min: 0 }}
  - {{ id: Vout, label: Output voltage, family: voltage, unit: V, min: 0 }}
  - {{ id: I, label: Divider current, family: current, unit: mA, min: 0 }}
equations:
  - Vout = Vin * R2 / (R1 + R2)
  - I = Vin / (R1 + R2)
faq:
  - q: What is the voltage divider formula?
    a: Vout = Vin × R2 ÷ (R1 + R2), where R2 is the resistor between the output and ground.
  - q: Can I use a divider as a power supply?
    a: Not for real loads — the output drops when current is drawn. Use a regulator instead. Dividers are for signals and reference voltages.
  - q: How do I scale 12 V to a 3.3 V microcontroller input?
    a: Press × on R2, set Vout to 3.3 V and choose R1; the calculator gives R2. Leave some margin below the input's maximum.
related: [physics/ohms-law, other/led-resistor, physics/resistors-series-parallel]
''','''
## How to use this calculator

Enter the **input voltage** and **R1** and **R2**. The output voltage and divider current are calculated. To design a divider, press × on a resistor and enter the target output.

## Formula

<p class="formula">V<sub>out</sub> = V<sub>in</sub> × R₂ ÷ (R₁ + R₂)</p>

## Example

12 V with R1 = 10 kΩ and R2 = 4.7 kΩ: V<sub>out</sub> = 12 × 4.7 ÷ 14.7 = **3.84 V**, current **0.82 mA**.
''')

page(C,'lpg-cylinder',f'''
title: LPG Gas Cylinder Duration Calculator
description: Estimate how many days an LPG gas cylinder will last from its weight and your daily cooking use.
category: other
keywords: [lpg cylinder duration, how long does gas cylinder last, cooking gas usage, lpg consumption, 14.2 kg cylinder]
{U}
variables:
  - {{ id: kg, label: Gas in cylinder, family: mass, unit: kg, imperialUnit: lb, default: 14.2, min: 0 }}
  - {{ id: hrs, label: Burner use per day, suffix: hours, default: 2, min: 0.0001 }}
  - {{ id: rate, label: Burner consumption, suffix: g/hour, default: 150, min: 0.0001 }}
  - {{ id: per, label: Gas used per day, family: mass, unit: g, min: 0 }}
  - {{ id: days, label: Cylinder will last, suffix: days, min: 0, decimals: 0 }}
equations:
  - per = hrs * rate / 1000
  - days = kg / per
faq:
  - q: How long does a 14.2 kg LPG cylinder last?
    a: For a typical family cooking about 2 burner-hours a day at around 150 g/hour, roughly 45–50 days.
  - q: How much gas does a burner use?
    a: Typically 100–200 g per hour depending on burner size and flame setting.
  - q: How can I make it last longer?
    a: Use lids, keep burners clean, use a pressure cooker and match flame size to the pan.
related: [everyday-life/electricity-cost, conversion/energy-converter]
''','''
## How to use this calculator

Enter the **gas weight** in the cylinder, **burner hours per day** and the burner's **consumption**. Daily use and the number of days are calculated.

## Example

14.2 kg cylinder, 2 burner-hours a day at 150 g/hour: 300 g/day → about **47 days**.
''')

page(C,'water-heater-time',f'''
title: Water Heater (Geyser) Heating Time Calculator
description: Calculate how long an electric water heater takes to heat a tank of water — and the energy used.
category: other
keywords: [water heater heating time, geyser calculator, how long to heat water, tank heating time, immersion heater]
{U}
variables:
  - {{ id: V, label: Tank volume, family: volume, unit: L, imperialUnit: galUS, default: 25, min: 0 }}
  - {{ id: t1, label: Cold water temperature, family: temperature, unit: C, imperialUnit: F, default: 20 }}
  - {{ id: t2, label: Target temperature, family: temperature, unit: C, imperialUnit: F, default: 55 }}
  - {{ id: P, label: Heater power, family: power, unit: kW, default: 2, min: 0.000001 }}
  - {{ id: ef, label: Efficiency, family: percent, unit: '%', default: 90, min: 0.01, max: 1 }}
  - {{ id: kwh, label: Energy used, suffix: kWh, min: 0, decimals: 2 }}
  - {{ id: t, label: Heating time, family: seconds, unit: min, min: 0 }}
equations:
  - kwh = V * 1000 * 4.186 * (t2 - t1) / 3600 / ef
  - t = kwh * 3600000 / P
faq:
  - q: How long does a geyser take to heat water?
    a: A 25-litre, 2 kW heater raising water by 35 °C takes about 34 minutes at 90% efficiency.
  - q: How much electricity does it use?
    a: About 1.16 kWh per 1,000 litres per °C, divided by efficiency. The example above uses about 1.1 kWh.
  - q: What temperature should I set?
    a: Around 50–60 °C balances comfort, energy use and protection against bacteria such as Legionella.
related: [chemistry/specific-heat, everyday-life/electricity-cost, ecology/shower-water]
''','''
## How to use this calculator

Enter the **tank volume**, **cold** and **target temperatures**, the heater's **power** and **efficiency**. Energy used and heating time are calculated.

## Formula

<p class="formula">time = m c ΔT ÷ (P × efficiency)</p>

## Example

25 L from 20 °C to 55 °C with a 2 kW heater at 90%:

- Energy = 25 × 4.186 × 35 ÷ 3,600 ÷ 0.9 = **1.13 kWh**
- Time = **34 minutes**
''')
print('other ok')
