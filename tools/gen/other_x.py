import sys, math; sys.path.insert(0, '' + __import__('os').path.dirname(__import__('os').path.abspath(__file__)) + '')
from expand import expand, words

expand('other/aquarium-volume', '''
## Common tank sizes

| Tank (L × W × H) | Volume | Water weight |
|---|---|---|
''' + ''.join(f"| {l} × {w} × {h} cm | {l*w*h/1000:.0f} L ({l*w*h/1000/3.785:.0f} US gal) | {l*w*h/1000:.0f} kg |\n" for l, w, h in [(40, 25, 25), (60, 30, 35), (80, 35, 40), (100, 40, 50), (120, 45, 50), (150, 50, 60)]) + '''
## Actual water volume

Substrate, rocks, decorations and the gap at the top reduce the real water volume by about **10–20%**. Use the real volume when dosing medicines, fertilisers or water conditioners.

## Total weight

A filled aquarium weighs roughly: water + glass + substrate + rock. As a rule of thumb, allow about **1.2–1.4 kg per litre** of tank volume. A 200 L tank can weigh 250–280 kg, so make sure the stand and floor can support it.

## Filtration and heating

| Equipment | Rule of thumb |
|---|---|
| Filter flow | 4–6 times the tank volume per hour |
| Heater | about 1 W per litre (more in cold rooms) |
| Water change | 10–25% weekly |

## Stocking

The old “one inch of fish per gallon” rule is unreliable. Consider adult fish size, activity, waste output and the tank's footprint. Larger tanks are more stable and forgiving for beginners.

## Other shapes

- **Cylinder**: π × r² × height.
- **Bow-front**: approximate with a rectangle using the average depth.
''', [
 ('How many litres is a 60 × 30 × 35 cm tank?', '63 litres, or about 17 US gallons.'),
 ('How much does a 100 litre aquarium weigh?', 'About 120–140 kg when filled, including glass and substrate.'),
])

expand('other/aspect-ratio', '''
## Common aspect ratios

| Ratio | Decimal | Used for |
|---|---|---|
| 1:1 | 1.00 | Instagram square posts, profile pictures |
| 4:3 | 1.33 | Older TVs, iPads, many compact cameras |
| 3:2 | 1.50 | 35 mm film, DSLR photos |
| 16:10 | 1.60 | Laptop screens |
| 16:9 | 1.78 | HD and 4K video, TVs, YouTube |
| 21:9 | 2.33 | Ultrawide monitors, cinema |
| 9:16 | 0.56 | Stories, Reels, Shorts (vertical video) |
| 4:5 | 0.80 | Instagram portrait posts |

## 16:9 resolutions

| Name | Resolution |
|---|---|
| HD (720p) | 1280 × 720 |
| Full HD (1080p) | 1920 × 1080 |
| QHD (1440p) | 2560 × 1440 |
| 4K UHD | 3840 × 2160 |
| 8K UHD | 7680 × 4320 |

## Finding the ratio of an image

Divide width and height by their greatest common divisor. 1920 × 1080: GCD is 120, so the ratio is **16:9**.

## Cropping vs letterboxing

When content and screen ratios differ, you can either crop (losing parts of the image) or letterbox / pillarbox (adding black bars). Choose based on whether the edges of the image matter.

## Social media sizes

| Platform | Recommended size |
|---|---|
| Instagram post (portrait) | 1080 × 1350 (4:5) |
| Instagram / TikTok story | 1080 × 1920 (9:16) |
| YouTube thumbnail | 1280 × 720 (16:9) |
| LinkedIn post image | 1200 × 627 (about 1.91:1) |
''', [
 ('What is the height of a 16:9 image 1920 pixels wide?', '1,080 pixels.'),
 ('What aspect ratio is 1080 × 1350?', '4:5.'),
], before='## Common sizes')

expand('other/battery-life', '''
## Typical battery capacities

| Battery | Capacity (approx.) | Voltage |
|---|---|---|
| AA alkaline | 2,000–2,800 mAh | 1.5 V |
| AA NiMH rechargeable | 1,900–2,500 mAh | 1.2 V |
| AAA alkaline | 1,000–1,200 mAh | 1.5 V |
| CR2032 coin cell | 220–240 mAh | 3 V |
| 18650 Li-ion | 2,500–3,500 mAh | 3.6–3.7 V |
| Smartphone battery | 3,000–5,000 mAh | 3.85 V |

## Sleep mode makes the difference

For microcontroller projects, average current is what matters:

<p class="formula">I<sub>avg</sub> = (I<sub>active</sub> × t<sub>active</sub> + I<sub>sleep</sub> × t<sub>sleep</sub>) ÷ total time</p>

A sensor drawing 20 mA for 1 second every minute and 10 µA in sleep averages about 0.34 mA — a 2,000 mAh battery could last around **8 months** instead of 4 days.

## mAh vs Wh

mAh ignores voltage. To compare batteries of different voltages, use watt-hours: Wh = mAh × V ÷ 1,000. A 5,000 mAh phone battery at 3.85 V holds 19.25 Wh.

## Power banks

A 10,000 mAh power bank (at 3.7 V) delivers less at 5 V USB output after conversion losses — typically 60–70% of its rating, about 6,000–7,000 mAh at the phone's battery voltage.
''', [
 ('How long will a 2,000 mAh battery last at 100 mA?', 'About 20 hours in theory, or around 17 hours allowing for 85% usable capacity.'),
 ('Why does my battery die faster in the cold?', 'Low temperatures slow the chemical reactions, reducing usable capacity, especially for alkaline and lithium-ion cells.'),
])

expand('other/cat-age', '''
## Cat age chart

| Cat age | Human-equivalent age | Life stage |
|---|---|---|
''' + ''.join(f"| {a} | {15*min(a,1)+9*max(0,min(a,2)-1)+4*max(0,a-2):.0f} | {s} |\n" for a, s in [(0.5, 'Kitten'), (1, 'Junior'), (2, 'Junior'), (3, 'Prime'), (6, 'Prime'), (7, 'Mature'), (10, 'Mature'), (11, 'Senior'), (14, 'Senior'), (15, 'Super senior'), (18, 'Super senior'), (20, 'Super senior')]) + '''
Life stages follow guidance from the American Association of Feline Practitioners (AAFP) and the American Animal Hospital Association (AAHA).

## How long do cats live?

Indoor cats commonly live 12–18 years, and many reach their early 20s. Outdoor cats tend to have shorter lives because of traffic, fights and disease.

## Senior cat care

From about age 11, vets often recommend check-ups every 6 months, with blood tests to catch kidney disease, thyroid problems and diabetes early. Watch for changes in appetite, thirst, weight and litter habits.
''', [
 ('How old is a 10-year-old cat in human years?', 'About 56 human years.'),
 ('Is a 15-year-old cat old?', 'Yes. At 15 a cat is about 76 in human terms and is considered a super senior.'),
])

expand('other/data-storage-converter', '''
## Why your drive shows less space

A drive sold as **1 TB** holds 1,000,000,000,000 bytes. Windows reports sizes in binary units but labels them “GB/TB”, so it shows about **931 GB**. Nothing is missing — it is a units difference.

| Advertised | Bytes | Shown by Windows |
|---|---|---|
''' + ''.join(f"| {n} | {b:,.0f} | {b/1024**3:,.0f} GB |\n" for n, b in [('128 GB', 128e9), ('256 GB', 256e9), ('512 GB', 512e9), ('1 TB', 1e12), ('2 TB', 2e12), ('4 TB', 4e12)]) + '''
macOS and many Linux tools use decimal units, so they match the advertised size.

## Bits vs bytes

Internet speeds are in **bits** per second (Mbps); file sizes are in **bytes**. 1 byte = 8 bits, so a 100 Mbps connection downloads at most 12.5 MB/s. See the [download time calculator](/other/download-time/).

## How much fits?

| Content | Approximate size |
|---|---|
| Photo (12 MP JPEG) | 3–5 MB |
| Song (MP3, 4 min) | 4–8 MB |
| HD movie (2 h, streaming quality) | 3–6 GB |
| 4K movie (2 h) | 15–25 GB |
| Smartphone OS update | 1–6 GB |
''', [
 ('How many GB is 1 TB?', '1,000 GB in decimal units, or 1,024 GiB in binary units.'),
 ('Why does my 1 TB drive show 931 GB?', 'The drive uses decimal units (10¹² bytes), while Windows shows binary gibibytes labelled as GB.'),
], before='## Decimal vs binary')

expand('other/dog-age', '''
## Dog age chart (DNA-based formula)

| Dog age | Human-equivalent | Old × 7 rule |
|---|---|---|
''' + ''.join(f"| {a} | {16*math.log(a)+31:.0f} | {a*7:.0f} |\n" for a in [1, 2, 3, 4, 5, 7, 10, 12, 14, 16]) + '''
The DNA formula comes from a 2020 study of DNA methylation in Labrador retrievers (Wang et al., *Cell Systems*). Dogs age very quickly in their first year, then more slowly.

## Size matters

Large and giant breeds age faster and have shorter lifespans than small breeds:

| Size | Typical lifespan |
|---|---|
| Small (under 10 kg) | 12–16 years |
| Medium (10–25 kg) | 10–14 years |
| Large (25–45 kg) | 9–12 years |
| Giant (over 45 kg) | 7–10 years |

A 10-year-old Chihuahua and a 10-year-old Great Dane are at very different life stages.

## Senior dog care

Most dogs are considered seniors from about 7 years (earlier for giant breeds). Twice-yearly vet visits, joint care, dental care and a diet suited to their age help keep older dogs healthy.
''', [
 ('Is one dog year really seven human years?', 'No. Dogs age much faster early on — a 1-year-old dog is roughly like a 31-year-old by the DNA formula.'),
 ('How old is a 10-year-old dog in human years?', 'About 68 by the DNA-based formula.'),
])

expand('other/dog-food-calories', '''
## Daily calories by weight (neutered adult, factor 1.6)

| Dog weight | RER | Daily calories |
|---|---|---|
''' + ''.join(f"| {m} kg | {70*m**0.75:.0f} kcal | {70*m**0.75*1.6:.0f} kcal |\n" for m in [3, 5, 10, 15, 20, 30, 40, 50]) + '''
## Life-stage factors

| Situation | Multiply RER by |
|---|---|
| Neutered adult | 1.6 |
| Intact adult | 1.8 |
| Inactive or obese-prone | 1.2–1.4 |
| Weight loss | 1.0 (based on target weight) |
| Puppy under 4 months | 3.0 |
| Puppy 4 months to adult | 2.0 |
| Working dog | 2–5 |

These are starting points from veterinary nutrition guidelines; adjust based on body condition.

## Body condition score

Vets use a 9-point scale. At the ideal score (4–5), you can feel the ribs easily under a thin layer of fat and see a waist from above. Adjust food by about 10% and re-check after 2–3 weeks.

## Treats count

Treats should be no more than **10% of daily calories**. Subtract them from the food allowance.
''', [
 ('How many calories does a 20 kg dog need?', 'About 1,050 kcal a day for a neutered adult (RER 662 × 1.6).'),
 ('How do I convert calories to cups?', 'Divide daily calories by the kcal per cup on the food label.'),
])

expand('other/download-time', '''
## Download times at different speeds

| File size | 25 Mbps | 100 Mbps | 300 Mbps | 1 Gbps |
|---|---|---|---|---|
''' + ''.join(f"| {n} | " + ' | '.join((lambda s: f"{int(s//60)} min {int(s%60)} s" if s >= 60 else f"{s:.0f} s")(b*8/(sp*1e6*0.9)) for sp in [25, 100, 300, 1000]) + " |\n" for n, b in [('100 MB app', 1e8), ('1 GB', 1e9), ('5 GB game update', 5e9), ('25 GB 4K movie', 25e9), ('100 GB game', 1e11)]) + '''
Times assume 90% real-world efficiency.

## Why real downloads are slower

- **Server speed**: the other end may limit your download.
- **Wi-Fi**: walls and distance reduce speed; a wired connection is faster.
- **Network congestion**: evening peak times are slower.
- **Protocol overhead**: TCP/IP headers use a few percent of bandwidth.

## Upload time

Many connections have much slower upload speeds. A 100/20 Mbps plan uploads a 5 GB video in about 37 minutes at 90% efficiency, versus about 7.4 minutes to download it.
''', [
 ('How long does it take to download 1 GB at 100 Mbps?', 'About 80 seconds at full speed, or about 90 seconds in practice.'),
 ('What is the difference between Mbps and MB/s?', 'Mbps is megabits per second; MB/s is megabytes per second. Divide Mbps by 8 to get MB/s.'),
])

expand('other/due-date', '''
## Pregnancy milestones

| Weeks | Milestone (typical) |
|---|---|
| 4–6 | Positive pregnancy test, heartbeat may be seen on ultrasound |
| 8–14 | First-trimester screening and dating scan in many countries |
| 18–22 | Detailed anatomy scan |
| 24 | Viability milestone often referenced in care |
| 28 | Start of third trimester |
| 37–42 | Term; most babies are born in this window |

Schedules differ by country and provider.

## How accurate is the due date?

Only about **4–5% of babies** arrive on their exact due date. Most are born within a week either side. An early ultrasound (before about 14 weeks) is usually more accurate than the date of the last period, and your care provider may adjust the due date after it.

## IVF due dates

For IVF pregnancies, the due date is based on the embryo transfer date: 266 days after egg retrieval, or 261 days after a 5-day embryo transfer.

## Irregular cycles

Naegele's rule assumes ovulation about 14 days before the next period. If cycles are irregular, the estimate is less reliable — an early scan gives a better date.

This calculator gives an estimate for planning. Always follow advice from your doctor or midwife.
''', [
 ('How is a due date calculated?', 'By adding 280 days (40 weeks) to the first day of the last menstrual period, adjusted for cycle length.'),
 ('What if I do not know my last period date?', 'An ultrasound scan in the first trimester can estimate the due date accurately.'),
], before='## Trimesters')

expand('other/grade-percentage', '''
## Percentage to letter grade (typical US scale)

| Percentage | Letter | GPA |
|---|---|---|
| 93–100 | A | 4.0 |
| 90–92 | A− | 3.7 |
| 87–89 | B+ | 3.3 |
| 83–86 | B | 3.0 |
| 80–82 | B− | 2.7 |
| 77–79 | C+ | 2.3 |
| 73–76 | C | 2.0 |
| 70–72 | C− | 1.7 |
| 67–69 | D+ | 1.3 |
| 60–66 | D | 1.0 |
| Below 60 | F | 0.0 |

Scales differ between schools and countries. Check your institution's policy.

## Other grading systems

| System | Top grades |
|---|---|
| UK university | First (70%+), 2:1 (60–69%), 2:2 (50–59%), Third (40–49%) |
| India (CBSE, 9-point) | A1 (91–100), A2 (81–90), B1 (71–80)… |
| ECTS (Europe) | A (top 10%), B (next 25%)… |

## Weighted grades

If assignments have different weights, multiply each percentage by its weight and add them up. To work out what you need on a final exam, use the [grade needed calculator](/everyday-life/grade-needed/).

## Percentage to CGPA (India)

Many universities in India convert CGPA to percentage with a formula set by the university — for example CBSE uses CGPA × 9.5. Check your university's rule before converting.
''', [
 ('What percentage is 42 out of 50?', '84%.'),
 ('What letter grade is 85%?', 'A B on a typical US scale.'),
])

expand('other/led-resistor', '''
## Typical LED forward voltages

| LED colour | Forward voltage |
|---|---|
| Infrared | 1.2–1.5 V |
| Red | 1.8–2.2 V |
| Orange / yellow | 2.0–2.2 V |
| Green (standard) | 1.9–2.4 V |
| Green (true / high-brightness) | 2.8–3.4 V |
| Blue | 2.8–3.4 V |
| White | 2.8–3.4 V |

Check the datasheet for your exact LED.

## Resistors for a 20 mA red LED (2.0 V)

| Supply | Calculated | Nearest standard (E12, round up) | Power |
|---|---|---|---|
''' + ''.join(f"| {vs} V | {(vs-2)/0.02:.0f} Ω | {min([x for x in [10,12,15,18,22,27,33,39,47,56,68,82,100,120,150,180,220,270,330,390,470,560,680,820,1000,1200] if x>=(vs-2)/0.02])} Ω | {(vs-2)*0.02*1000:.0f} mW |\n" for vs in [3.3, 5, 9, 12, 24]) + '''
Always round **up** to the next standard value so the current stays below the limit.

## LEDs in series

Several LEDs can share one resistor in series: R = (Vs − n × Vf) ÷ I. Three 2.0 V red LEDs on 12 V at 20 mA need (12 − 6) ÷ 0.02 = **300 Ω**.

## LEDs in parallel

Do not share one resistor between LEDs in parallel. Small differences in forward voltage make one LED hog the current. Give each LED its own resistor.

## Modern LEDs need less current

Many modern indicator LEDs are bright at 2–10 mA. Using a lower current saves power and extends LED life.
''', [
 ('What resistor do I need for an LED on 5 V?', 'For a red LED (2 V) at 20 mA, (5 − 2) ÷ 0.02 = 150 Ω.'),
 ('Can I connect an LED without a resistor?', 'Not directly to a voltage source — the current would rise until the LED fails. Use a resistor or a constant-current driver.'),
])

expand('other/lpg-cylinder', '''
## How long a cylinder lasts

14.2 kg cylinder:

| Daily use | At 150 g/hour | At 200 g/hour |
|---|---|---|
''' + ''.join(f"| {h} h/day | {14.2/(h*0.15):.0f} days | {14.2/(h*0.2):.0f} days |\n" for h in [1, 1.5, 2, 3, 4]) + '''
## Common cylinder sizes

| Cylinder | Gas content |
|---|---|
| India domestic | 14.2 kg |
| India commercial | 19 kg |
| Small / portable | 5 kg |
| UK propane (common) | 13 kg, 19 kg, 47 kg |

## Burner consumption

A typical domestic burner uses about 150–250 g of LPG per hour on high flame. Small burners and simmer settings use much less. Rating plates often list consumption in g/h or kW (1 kW ≈ 75–80 g/h of LPG).

## Saving gas

- Use lids on pots — cooking without a lid uses noticeably more gas.
- Match the pan size to the burner so flames do not lick up the sides.
- Use a pressure cooker for rice, dal and pulses.
- Soak beans and grains before cooking.
- Keep burners clean for a blue flame; a yellow flame wastes gas.

## Safety

Check the hose and regulator regularly for cracks, turn off the regulator when not in use and never test for leaks with a flame — use soapy water.
''', [
 ('How long does a 14.2 kg LPG cylinder last?', 'For a family cooking 2 hours a day at about 150 g/hour, roughly 47 days.'),
 ('How much LPG does a burner use per hour?', 'About 150–250 g per hour on high flame for a domestic burner.'),
])

expand('other/ovulation', '''
## Ovulation day by cycle length

| Cycle length | Ovulation (approx.) | Fertile window |
|---|---|---|
''' + ''.join(f"| {c} days | Day {c-14} | Days {c-19}–{c-13} |\n" for c in [24, 26, 28, 30, 32, 35]) + '''
Day 1 is the first day of the period.

## Signs of ovulation

- Changes in cervical mucus — clear, stretchy and slippery, like raw egg white.
- A slight rise in basal body temperature (about 0.2–0.5 °C) **after** ovulation.
- Positive ovulation predictor kits (LH surge), usually 24–36 hours before ovulation.
- Mild one-sided pelvic pain for some people.

## How accurate are calendar methods?

Cycle lengths vary, and ovulation does not always happen 14 days before the next period. Calendar estimates are a starting point; combining them with ovulation tests or temperature tracking is more reliable.

This calculator is not a method of contraception.

## When to see a doctor

Consider talking to a doctor if cycles are very irregular, or if you have been trying to conceive for 12 months (6 months if aged 35 or over) without success.
''', [
 ('When is the fertile window?', 'The 5 days before ovulation and the day of ovulation.'),
 ('Can I use this to avoid pregnancy?', 'No. Calendar estimates are not reliable enough for contraception.'),
])

expand('other/paper-weight-gsm', '''
## GSM guide

| GSM | Typical use |
|---|---|
| 60–70 | Newsprint, notebooks |
| 75–80 | Everyday office printer paper |
| 90–120 | Letterheads, quality documents |
| 130–170 | Flyers, brochures, posters |
| 200–250 | Brochure covers, light card |
| 300–350 | Business cards, postcards, invitations |
| 400+ | Premium business cards, packaging |

## Paper sizes and areas

| Size | Dimensions | Area | Weight of 1 sheet at 80 gsm |
|---|---|---|---|
''' + ''.join(f"| {n} | {w} × {h} mm | {w*h/1e6:.4f} m² | {80*w*h/1e6:.2f} g |\n" for n, w, h in [('A3', 297, 420), ('A4', 210, 297), ('A5', 148, 210), ('US Letter', 216, 279), ('US Legal', 216, 356)]) + '''
An A0 sheet is exactly 1 m², so a sheet of A0 at 80 gsm weighs 80 g. Each smaller A size is half the previous one.

## GSM vs US paper weight (lb)

US paper is labelled by the weight of 500 sheets in its basic size, which differs by paper type:

| US weight | Approx. GSM |
|---|---|
| 20 lb bond | 75 |
| 24 lb bond | 90 |
| 80 lb text | 120 |
| 80 lb cover | 216 |
| 100 lb cover | 270 |

## Postage

Postage often depends on weight. Ten A4 sheets at 80 gsm weigh about 50 g, plus about 5–10 g for a C4 envelope.
''', [
 ('How much does an A4 sheet of 80 gsm paper weigh?', 'About 5 g.'),
 ('How much does a ream of A4 paper weigh?', '500 sheets of 80 gsm A4 weigh about 2.5 kg.'),
])

expand('other/password-strength', '''
## Character sets

| Characters used | Pool size (N) | Bits per character |
|---|---|---|
| Digits only | 10 | 3.32 |
| Lowercase letters | 26 | 4.70 |
| Upper + lowercase | 52 | 5.70 |
| Letters + digits | 62 | 5.95 |
| All printable ASCII | 95 | 6.57 |

## Entropy and strength

| Entropy | Strength (for random passwords) |
|---|---|
| Under 40 bits | Weak |
| 40–60 bits | Moderate |
| 60–80 bits | Strong |
| 80+ bits | Very strong |

## Passphrases

A random passphrase of common words can be strong and memorable. Four words chosen randomly from a 7,776-word list (diceware) give 4 × 12.9 = **51.7 bits**; six words give **77.5 bits**.

## Why real passwords are weaker

The formula assumes **random** characters. Human-chosen passwords like “Summer2024!” follow patterns that attackers try first, so their real strength is far lower than the formula suggests.

## Good practice

- Use a password manager to generate and store long random passwords.
- Use a different password for every site.
- Turn on two-factor authentication wherever possible.
- Check whether your passwords have appeared in known data breaches.
''', [
 ('How long should a password be?', 'At least 12–16 random characters, or a passphrase of 5–6 random words.'),
 ('Is a long passphrase better than a short complex password?', 'Usually yes. Length adds more entropy than symbols, and passphrases are easier to remember.'),
])

expand('other/print-size-dpi', '''
## Maximum print size at 300 DPI

| Camera / image | Pixels | Print size at 300 DPI |
|---|---|---|
''' + ''.join(f"| {n} | {w} × {h} | {w/300*2.54:.1f} × {h/300*2.54:.1f} cm ({w/300:.1f} × {h/300:.1f} in) |\n" for n, w, h in [('8 MP', 3264, 2448), ('12 MP phone', 4032, 3024), ('24 MP camera', 6000, 4000), ('45 MP camera', 8192, 5464), ('Full HD frame', 1920, 1080), ('4K frame', 3840, 2160)]) + '''
## How much DPI do you need?

| Use | Recommended DPI |
|---|---|
| Photo prints held in the hand | 300 |
| Magazines and brochures | 300 |
| Posters viewed from a metre or more | 150–200 |
| Large banners and billboards | 30–100 |
| Screen display | Resolution matters, not DPI |

The further away a print is viewed, the lower the DPI can be.

## Common photo print sizes

| Print | Pixels needed at 300 DPI |
|---|---|
| 4 × 6 in (10 × 15 cm) | 1200 × 1800 |
| 5 × 7 in | 1500 × 2100 |
| 8 × 10 in | 2400 × 3000 |
| A4 | 2480 × 3508 |
| A3 | 3508 × 4961 |

## DPI vs PPI

PPI (pixels per inch) describes the image; DPI (dots per inch) describes how a printer lays down ink. In everyday use the terms are often interchanged. Changing the DPI setting in a file without resampling does not change its pixels — only the print size.
''', [
 ('How big can I print a 12 MP photo?', 'About 34 × 26 cm (13.4 × 10 in) at 300 DPI, or larger at lower DPI for posters.'),
 ('How many pixels for an A4 print?', '2480 × 3508 pixels at 300 DPI.'),
])

expand('other/screen-ppi', '''
## Pixel density of common screens

| Screen | Resolution | Size | PPI |
|---|---|---|---|
''' + ''.join(f"| {n} | {w} × {h} | {d}″ | {math.hypot(w,h)/d:.0f} |\n" for n, w, h, d in [('Full HD monitor', 1920, 1080, 24), ('QHD monitor', 2560, 1440, 27), ('4K monitor', 3840, 2160, 27), ('4K monitor', 3840, 2160, 32), ('Laptop FHD', 1920, 1080, 15.6), ('Laptop QHD+', 2560, 1600, 14), ('Phone FHD+', 2400, 1080, 6.5), ('4K TV', 3840, 2160, 55)]) + '''
## When is PPI “enough”?

Whether you can see individual pixels depends on viewing distance:

| Viewing distance | PPI where pixels become hard to see (20/20 vision) |
|---|---|
| 25–30 cm (phone) | about 300 |
| 50–60 cm (laptop) | about 150 |
| 60–80 cm (desktop monitor) | about 110–140 |
| 2.5 m (TV) | about 35 |

This is why a 55-inch 4K TV at 80 PPI looks sharp from the sofa.

## Scaling

High-PPI screens usually run with display scaling (for example 150%) so text stays readable. A 27-inch 4K monitor at 150% gives the same workspace as a 1440p monitor but with sharper text.
''', [
 ('What is the PPI of a 27-inch 1440p monitor?', 'About 109 PPI.'),
 ('Is higher PPI always better?', 'Only up to the point where your eyes cannot see individual pixels at your viewing distance.'),
])

expand('other/video-file-size', '''
## Typical bitrates

| Video | Typical bitrate |
|---|---|
| 720p streaming | 2–5 Mbps |
| 1080p streaming | 5–8 Mbps |
| 1080p camera recording (H.264) | 15–30 Mbps |
| 4K streaming | 15–25 Mbps |
| 4K camera recording (H.264/H.265) | 50–150 Mbps |
| ProRes 422 HQ, 4K | about 700 Mbps |

## File size per hour

| Bitrate | Per minute | Per hour |
|---|---|---|
''' + ''.join(f"| {b} Mbps | {b*60/8:.0f} MB | {b*3600/8/1000:.1f} GB |\n" for b in [5, 10, 20, 50, 100, 150]) + '''
## Codecs

Newer codecs give similar quality at lower bitrates:

| Codec | Size vs H.264 at similar quality |
|---|---|
| H.264 (AVC) | Baseline |
| H.265 (HEVC) | about 40–50% smaller |
| AV1 | about 50% smaller |

## Recording time on a card

Card capacity (GB) × 8,000 ÷ bitrate (Mbps) ÷ 60 = minutes. A 128 GB card at 100 Mbps holds about **170 minutes**.

## Audio

Audio is usually small next to video: 128–320 kbps for stereo, adding about 1–2.4 MB per minute.
''', [
 ('How big is 1 hour of 1080p video?', 'At 20 Mbps, about 9 GB. Streaming-quality 1080p at 5 Mbps is about 2.25 GB.'),
 ('How many minutes of 4K fit on a 64 GB card?', 'At 100 Mbps, about 85 minutes.'),
])

expand('other/voltage-divider', '''
## Common divider ratios

| R1 | R2 | Vout ÷ Vin | 12 V in → | 5 V in → |
|---|---|---|---|---|
''' + ''.join(f"| {a} kΩ | {b} kΩ | {b/(a+b):.3f} | {12*b/(a+b):.2f} V | {5*b/(a+b):.2f} V |\n" for a, b in [(10, 10), (10, 4.7), (20, 10), (30, 10), (47, 10), (100, 10)]) + '''
## Choosing resistor values

- **Too low**: wastes current and can drain batteries. 1 kΩ + 1 kΩ on 12 V draws 6 mA.
- **Too high**: the divider becomes sensitive to the load and to ADC input currents.
- For microcontroller ADC inputs, a total of 10–100 kΩ is a common compromise; add a small capacitor (e.g. 100 nF) on the output to stabilise readings.

## Loading effect

Any load connected to Vout appears in parallel with R2, lowering the output. If the load is 10 kΩ and R2 is 10 kΩ, the effective R2 becomes 5 kΩ. Keep the load at least 10 times larger than R2, or buffer the output with an op-amp.

## Not for power supplies

A voltage divider is not a substitute for a regulator. It cannot supply steady voltage to a varying load — use a linear regulator or a buck converter for that.

## Measuring battery voltage

To read a 12 V battery with a 3.3 V ADC, keep the ratio below 3.3 ÷ 14.4 = 0.229 to allow for charging voltage. R1 = 39 kΩ and R2 = 10 kΩ gives 0.204, so 14.4 V reads as 2.94 V with a safe margin.
''', [
 ('How do I get 3.3 V from 5 V with resistors?', 'R2 ÷ (R1 + R2) = 0.66, for example R1 = 10 kΩ and R2 = 20 kΩ (gives 3.33 V) — only for high-impedance inputs.'),
 ('Can I power a device with a voltage divider?', 'No. Use a regulator. Dividers are for signals and reference voltages, not for supplying current.'),
])

expand('other/water-heater-time', '''
## Heating times for common tanks

From 15 °C to 55 °C at 90% efficiency:

| Tank | 1.5 kW | 2 kW | 3 kW |
|---|---|---|---|
''' + ''.join(f"| {v} L | " + ' | '.join(f"{v*4.186*40/3600/0.9/p*60:.0f} min" for p in [1.5, 2, 3]) + " |\n" for v in [10, 15, 25, 50, 100, 150]) + '''
## Running cost

Energy used × electricity price. Heating 50 L by 40 °C uses about 2.6 kWh; at 0.15 per kWh that is about 0.39 per full heat-up.

## Standing losses

Stored hot water loses heat through the tank walls. Well-insulated tanks lose 1–2 kWh a day; older tanks can lose more. Lagging pipes and setting a sensible temperature reduce this.

## Temperature settings

- **Storage tanks**: keep at **60 °C** or above to control Legionella bacteria.
- **At the tap**: 50 °C or below reduces scald risk; thermostatic mixing valves help.
- Each 10 °C reduction in set temperature saves a noticeable amount of energy in standing losses.

## Heat pumps and solar

Heat-pump water heaters use about a third of the electricity of a resistance heater for the same hot water. Solar water heaters can cover most needs in sunny climates.
''', [
 ('How long does a 25 litre geyser take to heat?', 'About 30–40 minutes with a 2 kW element, heating from 15 °C to 55 °C.'),
 ('How much electricity does a water heater use?', 'About 0.05 kWh per litre for a 40 °C rise, before standing losses.'),
])

import glob, os
for p in sorted(glob.glob('/home/claude/zentacalculator/src/content/calculators/other/*.mdx')):
    c = 'other/' + os.path.basename(p)[:-4]; print(c, words(c))
