"""Quality pass (2026-11-07) on thin pages from the first batches (2026-10-27/28):
worked examples, Python-computed reference tables, practical notes, keyword-first titles,
intro phrase "<topic> calculator". Slugs, categories and variable ids unchanged.
NOTE: one-shot script (asserts the old text); do not re-run on already-updated pages."""
import sys, os, re, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fixflow import fix_text
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'src', 'content', 'calculators')
U = '2026-11-07'

def path(cid): return f'{BASE}/{cid}.mdx'
def load(cid):
    _, fm, body = open(path(cid)).read().split('---', 2); return fm, body
def save(cid, fm, body): open(path(cid), 'w').write(fix_text('---' + fm + '---' + body))
def q(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def set_fm(cid, **kv):
    fm, body = load(cid)
    for k, v in kv.items():
        if k == 'description': assert 120 <= len(v) <= 160, (cid, len(v))
        if isinstance(v, list): line = f'{k}: [' + ', '.join(v) + ']'
        elif k == 'intro': line = 'intro: ' + json.dumps(v, ensure_ascii=False)
        else: line = f'{k}: ' + q(v)
        assert re.search(rf'^{k}: ', fm, re.M), (cid, k)
        fm = re.sub(rf'^{k}: .*$', lambda m: line, fm, count=1, flags=re.M)
    fm = re.sub(r'^updated: .*$', f'updated: {U}', fm, flags=re.M)
    save(cid, fm, body)

def rep(cid, old, new):
    fm, body = load(cid); assert body.count(old) == 1, (cid, old[:50]); save(cid, fm, body.replace(old, new))

def section(cid, heading, new):
    """replace a whole '## heading' section (up to the next ## or end)"""
    fm, body = load(cid)
    i = body.index(heading); j = body.find('\n## ', i + 1)
    body = body[:i] + new.strip('\n') + '\n' + (body[j:] if j != -1 else '')
    save(cid, fm, body.rstrip('\n') + '\n')

def append(cid, text):
    fm, body = load(cid); save(cid, fm, body.rstrip('\n') + '\n\n' + text.strip('\n') + '\n')

def intro_check(cid, phrase):
    fm, _ = load(cid); t = re.search(r'^intro: (.*)$', fm, re.M).group(1).lower()
    assert phrase + ' calculator' in t, (cid, phrase)

# ============================================================ 1. Current divider
c = 'electronics/current-divider'
set_fm(c,
    title='Current Divider Calculator (Current Divider Rule & Branch Currents)',
    intro="When current reaches parallel branches, it splits between them — more through the lower resistance. The [current divider rule](https://www.instrumentationblog.in/current-divider-rule-explained/) follows directly from [Kirchhoff's current law](https://www.instrumentationblog.in/kirchhoffs-current-law-kcl-explained/) and is the basis of [shunt resistors in instrumentation](https://www.instrumentationblog.in/shunt-resistors-in-instrumentation/). This current divider calculator gives each branch current, the equivalent resistance and the voltage across the pair.",
    related=['electronics/voltage-divider', 'physics/resistors-series-parallel', 'electronics/shunt-resistor', 'physics/ohms-law'])
It, R1, R2 = 1.0, 100.0, 300.0
I1 = It * R2 / (R1 + R2); I2 = It * R1 / (R1 + R2); Req = R1 * R2 / (R1 + R2)
section(c, '## Example', f'''
## Worked example

A total current of {It:g} A enters {R1:g} Ω and {R2:g} Ω in parallel:

- I₁ = {It:g} × {R2:g} ÷ ({R1:g} + {R2:g}) = **{I1:g} A**
- I₂ = {It:g} × {R1:g} ÷ ({R1:g} + {R2:g}) = **{I2:g} A** (check: {I1:g} + {I2:g} = {It:g} A)
- R<sub>eq</sub> = {R1:g} × {R2:g} ÷ {R1+R2:g} = **{Req:g} Ω**, so the voltage across the pair is {It:g} A × {Req:g} Ω = **{It*Req:g} V**
''')
rows = ''
for ratio in (1, 2, 3, 4, 9, 10, 99, 999):
    rows += f"| {ratio:g} | {ratio/(1+ratio)*100:.2f}% | {1/(1+ratio)*100:.2f}% | {ratio/(1+ratio):.4g} × R₁ |\n"
Rs = (100.0, 200.0, 400.0); G = [1/r for r in Rs]; Gt = sum(G)
three = ' · '.join(f"I through {r:g} Ω = {g/Gt:.4f} A" for r, g in zip(Rs, G))
rep(c, '## Ammeter shunts', f'''## Current split by resistance ratio

| R₂ ÷ R₁ | Share through R₁ | Share through R₂ | R<sub>eq</sub> |
|---|---|---|---|
{rows}
The branch with the **smaller** resistance always takes the larger share; with a 1 : 999 ratio it carries 99.9% of the current, which is how an ammeter shunt works.

## Three or more branches

Use conductances G = 1/R: I<sub>n</sub> = I<sub>T</sub> × G<sub>n</sub> ÷ ΣG. For 1 A into 100 Ω, 200 Ω and 400 Ω: {three}.

## Ammeter shunts''')
append(c, '''
## Practical notes

- Include wire and connector resistance when one branch is a low-value shunt — 10 mΩ of wiring is 10% of a 0.1 Ω shunt.
- For accurate current sharing between parallel power devices, add small equal ballast resistors; tiny differences in on-resistance otherwise make one device carry most of the current.
- The rule assumes an ideal current source. If the source has internal resistance, the total current changes with the load — solve with the source voltage and [Ohm's law](/physics/ohms-law/) instead.
''')
intro_check(c, 'current divider')

# ============================================================ 2. Op-amp gain
c = 'electronics/op-amp-gain'
set_fm(c, description='Calculate the voltage gain, gain in dB and output of an inverting or non-inverting op-amp amplifier from Rf and Rin — or the resistor for a target gain.')
Rf, Ri, Vin = 100e3, 10e3, 0.1
Gn = 1 + Rf / Ri; Gi = -Rf / Ri
rep(c, '## Resistor pairs for common gains', f'''## Worked example

Non-inverting amplifier with R<sub>f</sub> = 100 kΩ, R<sub>in</sub> = 10 kΩ and a {Vin*1e3:g} mV input:

- Gain = 1 + 100 ÷ 10 = **{Gn:g}**, or 20 log₁₀({Gn:g}) = **{20*math.log10(Gn):.2f} dB**
- Output = {Gn:g} × {Vin*1e3:g} mV = **{Gn*Vin:g} V**

Switch to **inverting** with the same resistors: gain = −100 ÷ 10 = **{Gi:g}** ({20*math.log10(abs(Gi)):.2f} dB) and the output is **{Gi*Vin:g} V**.

## Resistor pairs for common gains''')
pairs = [(2, (10e3, 10e3), (20e3, 10e3)), (5, (40.2e3, 10e3), (49.9e3, 10e3)), (10, (90.9e3, 10e3), (100e3, 10e3)),
         (11, (100e3, 10e3), (110e3, 10e3)), (101, (100e3, 1e3), (100e3, 990))]
def k(r): return f'{r/1e3:g} k' if r >= 1e3 else f'{r:g} Ω'
rows = ''
for g, (nf, ni), (vf, vi) in pairs:
    rows += f"| {g} | {k(nf)} / {k(ni)} → {1+nf/ni:.4g} | {k(vf)} / {k(vi)} → −{vf/vi:.4g} |\n"
section(c, '## Resistor pairs for common gains', f'''
## Resistor pairs for common gains

| Target gain | Non-inverting R<sub>f</sub> / R<sub>in</sub> → actual gain | Inverting R<sub>f</sub> / R<sub>in</sub> → actual gain |
|---|---|---|
{rows}
Standard E96 (1%) values get within about 1% of most targets; use 0.1% resistors when the gain must be precise.
''')
bw = ''
for g in (1, 2, 10, 11, 100, 1000):
    bw += f"| {g} | {1e6/g/1e3:,.1f} kHz | {10e6/g/1e3:,.1f} kHz |\n"
section(c, '## Bandwidth', f'''
## Bandwidth

Every op-amp has a gain-bandwidth product (GBW): the closed-loop bandwidth is roughly GBW ÷ noise gain, where the noise gain is 1 + R<sub>f</sub>/R<sub>in</sub> for **both** configurations. An inverting amplifier with a gain of −1 therefore has the bandwidth of a gain-of-2 stage.

| Noise gain | Bandwidth, GBW = 1 MHz | Bandwidth, GBW = 10 MHz |
|---|---|---|
{bw}''')
append(c, '''
## Practical notes

- Keep resistors roughly 1 kΩ–1 MΩ: low values load the op-amp output and the source, high values add noise and offset from input bias current.
- The inverting amplifier's input impedance is only R<sub>in</sub> — buffer high-impedance sensors or use the non-inverting form.
- Check the output swing against the rails and the slew rate (a 10 V peak at 20 kHz needs about 1.3 V/µs).
''')
intro_check(c, 'op-amp gain')

# ============================================================ 3. PWM duty cycle
c = 'electronics/pwm-duty-cycle'
set_fm(c, title='PWM Duty Cycle Calculator (Average & RMS Voltage)')
f, ton, V = 1e3, 0.25e-3, 12.0
T = 1 / f; Dd = ton / T
rep(c, '## 8-bit PWM values', f'''## Worked example

A {f/1e3:g} kHz PWM signal with a {ton*1e3:g} ms pulse from a {V:g} V supply:

- Period T = 1 ÷ {f:g} Hz = **{T*1e3:g} ms**, so the off time is {T*1e3:g} − {ton*1e3:g} = **{(T-ton)*1e3:g} ms**
- Duty cycle = {ton*1e3:g} ÷ {T*1e3:g} = **{Dd*100:g}%**
- Average voltage = {Dd:g} × {V:g} = **{Dd*V:g} V**; RMS voltage = √{Dd:g} × {V:g} = **{math.sqrt(Dd)*V:g} V**

## 8-bit PWM values''')
rows = ''
for d in (0, 0.10, 0.25, 0.50, 0.75, 0.90, 1.0):
    rows += f"| {d*100:.0f}% | {math.floor(d*255+0.5)} | {math.floor(d*1023+0.5)} | {d*12:.2f} V |\n"
section(c, '## 8-bit PWM values', f'''
## 8-bit and 10-bit PWM values

| Duty cycle | 8-bit value (0–255) | 10-bit value (0–1023) | Average of 12 V |
|---|---|---|---|
{rows}''')
res = ''
for bits in (8, 10, 12, 16):
    res += f"| {bits}-bit ({2**bits:,} steps) | {16e6/2**bits/1e3:,.3f} kHz | {72e6/2**bits/1e3:,.3f} kHz | {100/2**bits:.4f}% |\n"
rep(c, '## Average vs RMS', f'''## PWM resolution vs frequency

A timer counting at f<sub>clk</sub> with N-bit resolution can produce at most f<sub>clk</sub> ÷ 2<sup>N</sup> (fast PWM); phase-correct PWM halves it.

| Resolution | Max. frequency at 16 MHz | Max. frequency at 72 MHz | Duty step |
|---|---|---|---|
{res}
The Arduino Uno's default analogWrite frequencies come from the 16 MHz clock with a ÷64 prescaler: 16 MHz ÷ 64 ÷ 256 = **{16e6/64/256:.2f} Hz** on pins 5 and 6 (fast PWM) and 16 MHz ÷ 64 ÷ 510 = **{16e6/64/510:.2f} Hz** on the others (phase-correct).

## Average vs RMS''')
append(c, '''
## Practical notes

- To turn PWM into a steady analogue voltage, add an [RC low-pass filter](/electronics/rc-filter/) with a cutoff at least 10× below the PWM frequency.
- Inductive loads (motors, solenoids) need a flyback diode across them; the current keeps flowing during the off time.
- At very low or very high duty cycles, the driver's rise and fall times become a large part of the pulse and the real average differs from D × V.
''')
intro_check(c, 'pwm duty cycle')

# ============================================================ 4. Box volume
c = 'math/box-volume'
set_fm(c, description='Calculate the volume, surface area and space diagonal of a box or rectangular prism in litres, cubic metres, cubic feet or gallons — plus volumetric weight.')
l, w, h = 60.0, 40.0, 30.0
Vb = l * w * h; Sb = 2 * (l*w + l*h + w*h); db = math.sqrt(l*l + w*w + h*h)
FT3 = 28316.846592
rep(c, '## Common box sizes', f'''## Worked example

A box measuring {l:g} × {w:g} × {h:g} cm:

- Volume = {l:g} × {w:g} × {h:g} = {Vb:,.0f} cm³ = **{Vb/1000:g} L** ({Vb/FT3:.3f} ft³)
- Surface area = 2 × ({l*w:,.0f} + {l*h:,.0f} + {w*h:,.0f}) = {Sb:,.0f} cm² = **{Sb/1e4:g} m²**
- Space diagonal = √({l:g}² + {w:g}² + {h:g}²) = **{db:.2f} cm** — the longest rod that fits inside
- Volumetric weight (÷ 5,000) = **{Vb/5000:g} kg**

## Common box sizes''')
rows = ''
for dims in ((30, 20, 15), (40, 30, 30), (45, 45, 45), (60, 40, 40), (60, 45, 45), (100, 100, 100)):
    v = dims[0] * dims[1] * dims[2]
    rows += f"| {' × '.join(map(str, dims))} | {v/1000:,.1f} L | {v/FT3:.2f} ft³ | {v/5000:.1f} kg |\n"
section(c, '## Common box sizes', f'''
## Common box sizes

| Box (cm) | Volume | Cubic feet | Volumetric weight (÷ 5,000) |
|---|---|---|---|
{rows}''')
append(c, '''
## Practical notes

- Measure **inside** dimensions for capacity and **outside** dimensions for shipping and shelf space — corrugated board walls are typically 3–7 mm thick.
- 1 m³ = 1,000 L = 35.31 ft³; 1 ft³ = 28.32 L = 7.48 US gallons.
- For irregular items, the packed volume is usually 20–30% larger than the sum of the items because of gaps and padding.
''')
intro_check(c, 'box volume')

# ============================================================ 5. RL time constant
c = 'electronics/rl-time-constant'
set_fm(c, title='RL Time Constant Calculator (τ = L/R, Current Rise & Decay)')
L_, R_, V_, t_ = 0.1, 50.0, 24.0, 2e-3
tau = L_ / R_; If = V_ / R_
rep(c, '## Current vs time constants', f'''## Worked example

A {L_*1e3:g} mH coil with {R_:g} Ω total resistance is switched onto {V_:g} V:

- τ = {L_:g} H ÷ {R_:g} Ω = **{tau*1e3:g} ms**; final current = {V_:g} ÷ {R_:g} = **{If:g} A**
- After t = {t_*1e3:g} ms (one time constant) the rising current is {If:g} × (1 − e⁻¹) = **{If*(1-math.exp(-t_/tau)):.4f} A**
- If the coil is instead discharging from {If:g} A, after {t_*1e3:g} ms it is {If:g} × e⁻¹ = **{If*math.exp(-t_/tau):.4f} A**
- It takes about 5τ = **{5*tau*1e3:g} ms** to reach full current

## Current vs time constants''')
rows = ''
for m in (0.5, 1, 2, 3, 4, 5):
    rows += f"| {m:g} τ | {(1-math.exp(-m))*100:.1f}% | {math.exp(-m)*100:.1f}% |\n"
section(c, '## Current vs time constants', f'''
## Current vs time constants

| Time | Rising (% of final) | Decaying (% of initial) |
|---|---|---|
{rows}''')
rows2 = ''
for p in (0.5, 0.632, 0.9, 0.95, 0.99, 0.999):
    rows2 += f"| {p*100:g}% | {-math.log(1-p):.3f} τ |\n"
rep(c, '## Typical time constants', f'''## Time to reach a given percentage

Rising current reaches a fraction x of its final value at t = −τ ln(1 − x):

| Current reached | Time |
|---|---|
{rows2}
## Typical time constants''')
append(c, '''
## Practical notes

- Use the **total** loop resistance — coil resistance plus series resistors and the driver's on-resistance — or τ will be overestimated.
- Iron-cored coils are not linear: inductance changes with current and with the armature position in relays and solenoids, so treat τ as an estimate and measure if timing matters.
- To speed up a slow-releasing relay, add a Zener or resistor in series with the flyback diode; the larger voltage across the coil collapses the current faster.
''')
intro_check(c, 'rl time constant')
print('improved 5 pages')
