"""Improve pass (2026-11-15) for three thin pages from the first batch (2026-10-27):
electrical/voltage-unbalance, electronics/snr, math/law-of-cosines.
Keyword-first titles, 120-160 char descriptions, two-paragraph intros with the "<topic> calculator"
phrase, worked examples built from the calculator defaults, reference tables computed here,
practical notes, common mistakes and new FAQs. Formulas and FAQ facts were re-checked.
Existing instrumentationblog.in links are kept (the SNR intro's signal integrity link moves to the
body to keep the intro short); none are added. Slugs, categories, variables, equations and
related ids are unchanged (asserted by inplace.edit). Run once on the original files."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inplace import edit, DONE
U = '2026-11-15'
IB = 'https://www.instrumentationblog.in'

# ======================================================================= Voltage unbalance
Va, Vb, Vc = 412.0, 405.0, 418.0
Vav = (Va + Vb + Vc) / 3
dev = max(abs(Va - Vav), abs(Vb - Vav), abs(Vc - Vav))
u = dev / Vav * 100
dt = 2 * u ** 2
beta = (Va ** 4 + Vb ** 4 + Vc ** 4) / (Va ** 2 + Vb ** 2 + Vc ** 2) ** 2
vuf = math.sqrt((1 - math.sqrt(3 - 6 * beta)) / (1 + math.sqrt(3 - 6 * beta))) * 100
DERATE = {0: 1.0, 1: 1.0, 2: 0.95, 3: 0.88, 4: 0.82, 5: 0.75}
vu_rows = ''
for x in (0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5):
    vu_rows += f"| {x:g}% | {2*x*x:.1f}% | {6*x:.0f}% to {10*x:.0f}% | {'yes' if x > 1 else 'no'} |\n"
# example motor: 40 A full load on the derating curve at the example unbalance (interpolated between 1% and 2%)
fac = 1.0 + (u - 1) * (0.95 - 1.0) if u > 1 else 1.0
mot_kw = 30.0
sg = lambda x: ('+' if x >= 0 else '\u2212') + f'{abs(x):.2f}'

edit('electrical/voltage-unbalance', date=U,
     title='Voltage Unbalance Calculator (NEMA Method, Motor Derating)',
     description='Calculate percent voltage unbalance from three line voltages by the NEMA MG 1 method, with the extra motor temperature rise and derating it causes.',
     phrase='voltage unbalance calculator',
     intro=('When the three line voltages of a supply are not equal, motors draw unbalanced currents and run hotter. '
            'This voltage unbalance calculator applies the NEMA MG 1 method: the largest deviation from the average, divided by the average.'
            '\n\n'
            'Electricians, maintenance engineers and energy auditors use it to check a motor supply before blaming the motor. '
            f'This guide to [voltage unbalance calculation for motors]({IB}/voltage-unbalance-calculation-motors/) explains the derating it leads to.'),
     replace=[(
         '## Example\n\n412, 405 and 418 V:\n\n- Average = 411.7 V\n- Largest deviation = 411.7 − 405 = 6.7 V\n- Unbalance = 6.7 ÷ 411.7 = **1.62%**\n- Temperature rise increases by about **5.2%**\n',
         f'''## Worked example

A {mot_kw:g} kW motor terminal box reads {Va:g} V (L1 to L2), {Vb:g} V (L2 to L3) and {Vc:g} V (L3 to L1):

- Average = ({Va:g} + {Vb:g} + {Vc:g}) ÷ 3 = **{Vav:.1f} V**
- Deviations: {sg(Va-Vav)} V, {sg(Vb-Vav)} V and {sg(Vc-Vav)} V, so the largest is **{dev:.2f} V** (L2 to L3)
- Unbalance = {dev:.2f} ÷ {Vav:.1f} × 100 = **{u:.2f}%**
- Extra winding temperature rise ≈ 2 × {u:.2f}² = **{dt:.1f}%**
- Derating factor read from the curve between 1% and 2% ≈ {fac:.2f}, so the motor should carry no more than about {mot_kw*fac:.1f} kW
- The IEC definition (negative to positive sequence ratio) gives {vuf:.2f}% for the same three voltages, a little higher than the NEMA figure because the two definitions differ
- Expect a current unbalance of roughly {6*u:.0f}% to {10*u:.0f}%, which is enough to worry a motor protection relay set at 10%
''')],
     body_add=f'''
## Unbalance, heating and current

The temperature figure is the increase in winding temperature rise (2 × unbalance²), and the current column uses the usual rule of thumb that current unbalance is 6 to 10 times the voltage unbalance:

| Voltage unbalance | Extra temperature rise | Typical current unbalance | Derate the motor? |
|---|---|---|---|
{vu_rows}
## How to measure voltage unbalance

- Measure **line-to-line** voltages at the motor terminals or at the starter, with the motor running at normal load. Unbalance at no load can look better than it is.
- Use one true-RMS meter for all three readings, so meter error does not show up as unbalance. A power quality analyser that logs over a day catches unbalance that comes and goes with single-phase loads.
- Compare the result with the **current unbalance** on a clamp meter. If the currents are far more unbalanced than 6 to 10 times the voltage figure, suspect the motor (a shorted turn or a high-resistance joint) rather than the supply.
- Rotate the supply leads one position (L1 to L2, L2 to L3, L3 to L1) and measure the currents again. If the high current follows the supply phase, the supply is the cause; if it stays on the same motor lead, the motor or its cable is.

More on the related protection and power quality topics: [what signal and power problems a VFD causes]({IB}/power-quality-issues-vfd-plc/) and how relays react in [motor protection relay types]({IB}/motor-protection-relay-types/).

## Common mistakes

- **Using line-to-neutral voltages.** NEMA MG 1 defines unbalance on line-to-line voltages. Phase voltages include zero-sequence components and give a different answer.
- **Dividing by the lowest or rated voltage.** The denominator is the average of the three measured voltages, not 400 V or 415 V nameplate.
- **Measuring at the main board only.** Long feeders and single-phase loads downstream change the balance; measure where the motor is connected.
- **Ignoring low unbalance.** At 3% the winding runs about 18% hotter in temperature rise, which shortens insulation life well before any trip.
- **Treating the 6 to 10 times rule as exact.** Current unbalance depends on motor design and load; use it to judge, and measure the real currents.
''',
     faq_add=[
         ('Should I measure line-to-line or line-to-neutral voltage for unbalance?',
          'Line-to-line. The NEMA MG 1 definition and the derating curve are based on line voltages. Line-to-neutral readings can be affected by neutral shift and zero-sequence voltage that a three-wire motor never sees.'),
         ('Does voltage unbalance affect VFDs?',
          'Yes. A six-pulse drive rectifier draws most of its current through the highest phase, so 2% to 3% voltage unbalance can make the input currents very uneven, raise DC bus ripple and trip the drive on input phase loss. Line reactors reduce the effect.'),
     ])

# ======================================================================= SNR
sVs, sVn = 1000.0, 1.0
s_snr = 20 * math.log10(sVs / sVn)
s_ratio = (sVs / sVn) ** 2
s_enob = (s_snr - 1.76) / 6.02
# second example: thermocouple signal
tVs, tVn = 10.0, 0.02  # mV
t_snr = 20 * math.log10(tVs / tVn)
avg_rows = ''
for N in (1, 4, 16, 64, 256, 1024):
    g = 10 * math.log10(N)
    avg_rows += f"| {N:,} | {math.sqrt(N):g} × | +{g:.1f} dB | {s_snr+g:.1f} dB | {(s_snr+g-1.76)/6.02:.1f} |\n"

edit('electronics/snr', date=U,
     title='SNR Calculator (Signal-to-Noise Ratio in dB and ENOB)',
     description='Calculate signal-to-noise ratio (SNR) in dB from RMS signal and noise voltages, with the power ratio and the effective number of bits (ENOB) for an ADC.',
     phrase='SNR calculator',
     intro=('Signal-to-noise ratio compares the signal you want with the noise riding on it, usually in decibels. '
            f'This SNR calculator turns RMS signal and noise voltages into SNR in dB, the power ratio and the ENOB, as explained in this [signal-to-noise ratio guide]({IB}/signal-to-noise-ratio-snr-calculator/).'
            '\n\n'
            'Instrument, audio and RF engineers use it to judge how small a change a measurement can resolve and how many ADC bits are really useful. '
            f'See also [decibels in electronics]({IB}/decibel-in-electronics-db-dbm/).'),
     body_add=f'''
## Worked example

With the default values, a {sVs:g} mV RMS signal carries {sVn:g} mV RMS of noise:

- Voltage ratio = {sVs:g} ÷ {sVn:g} = {sVs/sVn:,.0f}
- SNR = 20 × log₁₀({sVs/sVn:,.0f}) = **{s_snr:.2f} dB**
- Power ratio = {sVs/sVn:,.0f}² = **{s_ratio:,.0f}**, and 10 × log₁₀({s_ratio:,.0f}) gives the same {s_snr:.0f} dB
- ENOB = ({s_snr:.2f} − 1.76) ÷ 6.02 = **{s_enob:.2f} bits**, so a converter with more than about 10 bits adds nothing until the noise is reduced

A thermocouple input with a {tVs:g} mV signal and {tVn*1000:g} µV RMS of noise has an SNR of {t_snr:.1f} dB, about {(t_snr-1.76)/6.02:.1f} effective bits.

## Improving SNR by averaging

Averaging N readings of a steady signal reduces uncorrelated noise by √N, which adds 10 log₁₀ N dB. Starting from the {s_snr:.0f} dB example:

| Samples averaged | Noise reduced by | SNR gain | Resulting SNR | ENOB |
|---|---|---|---|---|
{avg_rows}
Averaging only helps against random noise. Mains hum and other correlated noise need filtering or an integration time that is a whole number of mains cycles.

## How noise is measured in practice

- **RMS, not peak:** SNR uses RMS values. For Gaussian noise the peak-to-peak value seen on an oscilloscope is roughly 6 to 7 times the RMS value, so divide a scope reading before using it here.
- **State the bandwidth:** noise grows with bandwidth (thermal noise with its square root), so an SNR figure means little without the bandwidth it was measured in. Set the scope or analyser bandwidth limit to match the real system.
- **Measure noise with the signal removed:** short the input or hold the process steady and log the reading spread; its standard deviation is the RMS noise.
- **Layout and cabling** matter as much as the electronics; good practice is covered in [what signal integrity means]({IB}/what-is-signal-integrity/).

## Common mistakes

- **Using 10 log for voltage ratios.** Voltages and currents need 20 log₁₀; only power ratios use 10 log₁₀.
- **Mixing RMS signal with peak-to-peak noise,** which makes the SNR look 15 to 17 dB worse than it is.
- **Quoting ENOB from SNR alone.** Datasheet ENOB uses SINAD, which includes distortion, so the real ENOB is usually a little lower than this calculator gives.
- **Comparing SNR figures measured over different bandwidths** or with different input ranges.
- **Confusing SNR with dynamic range,** which compares the largest possible signal, not the actual one, with the noise floor.
''',
     faq_add=[
         ('How much does averaging improve SNR?',
          'For random noise, averaging N samples improves SNR by 10 log₁₀ N dB: 4 samples give about 6 dB (one extra effective bit), 16 samples 12 dB and 256 samples about 24 dB. It does not remove hum or other noise that is correlated with the samples.'),
         ('What is the difference between SNR and SINAD?',
          'SNR counts only noise. SINAD (signal to noise and distortion) also counts harmonics of the signal, so it is always equal to or lower than SNR. ADC datasheets compute ENOB from SINAD.'),
     ])

# ======================================================================= Law of cosines
la, lb, lC = 7.0, 9.0, 50.0
Cr = math.radians(lC)
lc2 = la * la + lb * lb - 2 * la * lb * math.cos(Cr)
lc = math.sqrt(lc2)
lA = math.degrees(math.acos((lb * lb + lc2 - la * la) / (2 * lb * lc)))
lB = 180 - lA - lC
lK = la * lb * math.sin(Cr) / 2
per = la + lb + lc


def angles(a, b, c):
    A = math.degrees(math.acos((b * b + c * c - a * a) / (2 * b * c)))
    B = math.degrees(math.acos((a * a + c * c - b * b) / (2 * a * c)))
    return A, B, 180 - A - B


sss_rows = ''
for a, b, c in ((3, 4, 5), (5, 5, 5), (5, 12, 13), (7, 8, 9), (2, 3, 4), (6, 6, 10), (4, 7, 10)):
    A, B, C = angles(a, b, c)
    kind = 'right' if abs(max(A, B, C) - 90) < 1e-6 else ('obtuse' if max(A, B, C) > 90 else 'acute')
    sss_rows += f"| {a}, {b}, {c} | {A:.2f}° | {B:.2f}° | {C:.2f}° | {kind} |\n"

edit('math/law-of-cosines', date=U,
     title='Law of Cosines Calculator (Side, Angles and Area)',
     description='Solve any triangle with the law of cosines: find the third side, both other angles and the area from two sides and the included angle, or angles from 3 sides.',
     phrase='law of cosines calculator',
     intro=('The law of cosines, c² = a² + b² − 2ab cos C, extends Pythagoras\' theorem to every triangle. '
            'This law of cosines calculator finds the third side, the two remaining angles and the area from two sides and the angle between them, or the angles from three sides.'
            '\n\n'
            'Students use it for trigonometry homework, while surveyors, navigators and engineers use it to find distances and angles that cannot be measured directly.'),
     replace=[(
         '- c = **7.00**\n- Area = ½ × 7 × 9 × sin 50° = **24.13**\n',
         f'''- c = √{lc2:.2f} = **{lc:.2f}**
- cos A = (b² + c² − a²) ÷ 2bc = ({lb*lb:g} + {lc2:.2f} − {la*la:g}) ÷ (2 × {lb:g} × {lc:.3f}) = {(lb*lb+lc2-la*la)/(2*lb*lc):.4f}, so A = **{lA:.2f}°**
- B = 180° − {lA:.2f}° − {lC:g}° = **{lB:.2f}°**, the largest angle because it is opposite the longest side, b = {lb:g}
- Area = ½ × {la:g} × {lb:g} × sin {lC:g}° = **{lK:.2f}** square units, and the perimeter is {per:.2f}

Because c came out almost equal to a, angle A is almost equal to angle C: equal sides face equal angles.
''')],
     body_add=f'''
## Angles from three sides (SSS)

Each angle follows from cos A = (b² + c² − a²) ÷ 2bc and its two partners. Some common triangles:

| Sides a, b, c | Angle A | Angle B | Angle C | Type |
|---|---|---|---|---|
{sss_rows}
The sign of b² + c² − a² tells you the type at a glance: positive gives an acute angle, zero a right angle and negative an obtuse angle.

## Practical notes

- **Which formula to use:** two sides and the included angle (SAS) or three sides (SSS) need the law of cosines; two angles and a side, or a side and the angle opposite it, are easier with the [law of sines](/math/law-of-sines/). For three known sides, the [SSS triangle calculator](/math/sss-triangle/) lists all angles at once.
- **No ambiguous case:** arccos returns angles from 0° to 180°, so the law of cosines always gives the one correct angle, obtuse or not. That is why it is safer than the law of sines for the first angle.
- **Precision:** keep full precision for c before using it to find the angles. Rounding c to 7.00 in the example above changes angle A in the second decimal place.
- **Area without an angle:** with three sides you can also use Heron's formula; the [triangle area calculator](/math/triangle-area/) covers both methods.

## Common mistakes

- **Using an angle that is not between the two sides.** In c² = a² + b² − 2ab cos C, angle C must be the angle formed by sides a and b, opposite side c.
- **Calculator in radians mode.** cos 50 in radians is 0.965 instead of 0.643, which gives a wrong side with no warning. This calculator lets you pick the unit.
- **Forgetting the minus sign or the 2.** Writing c² = a² + b² − ab cos C, or adding the term, are the most common slips in hand work.
- **Sides that cannot form a triangle.** If one side is longer than the sum of the other two, (b² + c² − a²) ÷ 2bc falls outside −1 to 1 and no angle exists.
- **Taking the square root too early.** Work out a² + b² − 2ab cos C completely, then take the square root once.
''',
     faq_add=[
         ('Can the law of cosines find an obtuse angle?',
          'Yes, and without ambiguity. If b² + c² − a² is negative, cos A is negative and arccos returns an angle between 90° and 180°. For sides 4, 7 and 10 the angle opposite the 10 side is about 128.7°.'),
         ('What if the three sides do not form a triangle?',
          'Every side must be shorter than the sum of the other two (the triangle inequality). Sides 2, 3 and 6 fail this, the cosine works out below −1 and the calculator shows no angle.'),
     ])

print(len(DONE), 'pages improved:', ' '.join(DONE))

# Related links for the law of cosines page: point to the closest triangle solvers.
_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'content', 'calculators', 'math', 'law-of-cosines.mdx')
_s = open(_p).read()
_old = 'related: [math/pythagorean-theorem, math/right-triangle-trig, math/triangle-area, math/polygon]'
_new = 'related: [math/law-of-sines, math/sss-triangle, math/pythagorean-theorem, math/right-triangle-trig, math/triangle-area]'
if _old in _s:
    open(_p, 'w').write(_s.replace(_old, _new))
