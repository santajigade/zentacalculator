import sys, math, os, re; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page import page, n
from ib import intro
from statistics import NormalDist
D = '2026-11-08'
pi = math.pi
DESC = []
def P(cat, slug, fm, body):
    d = re.search(r'^description: (.*)$', fm, re.M).group(1).strip()
    assert 120 <= len(d) <= 160, (slug, len(d))
    t = re.search(r'^intro: (.*)$', fm, re.M).group(1)
    kw = slug.replace('-', ' ')
    DESC.append(slug)
    page(cat, slug, fm, body)

ncdf = NormalDist().cdf

# ======================================================================= ELECTRICAL

# ---------------------------------------------------------------- Solar string sizing
sVoc, sVmp, sbv, sbm, sTmin, sThot, sN, sVmax, sVlo, sVhi = 49.5, 41.6, -0.27, -0.35, 0.0, 70.0, 16, 1000.0, 200.0, 850.0
sVocc = sVoc * (1 + sbv / 100 * (sTmin - 25)); sVmph = sVmp * (1 + sbm / 100 * (sThot - 25)); sVmpc = sVmp * (1 + sbm / 100 * (sTmin - 25))
sNmax = math.floor(sVmax / sVocc); sNmin = math.ceil(sVlo / sVmph); sNmppt = math.floor(sVhi / sVmpc)
ss_rows = ''
for T in (25, 10, 0, -10, -20, -30):
    vc = sVoc * (1 + sbv / 100 * (T - 25))
    ss_rows += f"| {T} °C | {vc:.2f} V | {math.floor(600/vc)} | {math.floor(1000/vc)} | {math.floor(1500/vc)} |\n"
P('electrical', 'solar-string-sizing', f'''
title: Solar String Sizing Calculator (Modules per String, Voc & Vmp)
description: Work out the maximum and minimum number of PV modules per string from Voc, Vmp, temperature coefficients and the inverter's max DC and MPPT voltages.
category: electrical
{intro("A PV string must stay below the inverter's maximum DC voltage on the coldest morning and above the MPPT minimum on the hottest afternoon. This solar string sizing calculator corrects the module Voc and Vmp for temperature and gives the maximum and minimum number of modules per string, plus the string voltages for your chosen string length — the voltage check step in [solar PV system sizing](ib:solar-pv-system-sizing-calculation).")}
keywords: [solar string sizing calculator, pv string sizing, modules per string calculator, solar string voltage calculator, voc temperature correction, inverter string size, mppt voltage range]
updated: {D}
variables:
  - {{ id: Voc, label: Module open-circuit voltage Voc (STC), family: voltage, unit: V, default: {sVoc:g}, min: 0 }}
  - {{ id: Vmp, label: Module max-power voltage Vmp (STC), family: voltage, unit: V, default: {sVmp:g}, min: 0 }}
  - {{ id: bv, label: Temperature coefficient of Voc, suffix: '%/°C', default: {sbv:g}, help: 'From the module datasheet, usually −0.25 to −0.35 %/°C.' }}
  - {{ id: bm, label: Temperature coefficient of Vmp (or Pmax), suffix: '%/°C', default: {sbm:g} }}
  - {{ id: Tmin, label: Lowest expected ambient temperature, family: temperature, unit: C, imperialUnit: F, default: {sTmin:g}, help: 'Record low for the site — at dawn the cells are at ambient temperature.' }}
  - {{ id: Thot, label: Highest cell temperature, family: temperature, unit: C, imperialUnit: F, default: {sThot:g}, help: 'Roughly ambient + 25–35 °C on a hot sunny day.' }}
  - {{ id: N, label: Modules per string (your design), default: {sN}, min: 1 }}
  - {{ id: Vmax, label: Inverter maximum DC input voltage, family: voltage, unit: V, default: {sVmax:g}, min: 0 }}
  - {{ id: Vlo, label: Inverter MPPT minimum voltage, family: voltage, unit: V, default: {sVlo:g}, min: 0 }}
  - {{ id: Vhi, label: Inverter MPPT maximum voltage, family: voltage, unit: V, default: {sVhi:g}, min: 0 }}
  - {{ id: Vocc, label: Module Voc at the lowest temperature, family: voltage, unit: V }}
  - {{ id: Vmph, label: Module Vmp at the highest cell temperature, family: voltage, unit: V }}
  - {{ id: Vmpc, label: Module Vmp at the lowest temperature, family: voltage, unit: V }}
  - {{ id: Nmax, label: Maximum modules per string (max DC voltage), decimals: 0 }}
  - {{ id: Nmppt, label: Maximum modules to stay inside MPPT range, decimals: 0 }}
  - {{ id: Nmin, label: Minimum modules per string (MPPT minimum), decimals: 0 }}
  - {{ id: SVoc, label: String Voc on the coldest morning, family: voltage, unit: V }}
  - {{ id: SVmp, label: String Vmp on the hottest afternoon, family: voltage, unit: V }}
equations:
  - Vocc = Voc * (1 + bv / 100 * (Tmin - 298.15))
  - Vmph = Vmp * (1 + bm / 100 * (Thot - 298.15))
  - Vmpc = Vmp * (1 + bm / 100 * (Tmin - 298.15))
  - Nmax = floor(Vmax / Vocc)
  - Nmppt = floor(Vhi / Vmpc)
  - Nmin = ceil(Vlo / Vmph)
  - SVoc = N * Vocc
  - SVmp = N * Vmph
faq:
  - q: How do I calculate the maximum number of solar panels in a string?
    a: Correct the module Voc to the lowest expected temperature, Voc_cold = Voc × (1 + β_Voc × (T_min − 25)), then divide the inverter's maximum DC voltage by it and round down.
  - q: Why does Voc rise in cold weather?
    a: Silicon cell voltage has a negative temperature coefficient of about −0.3 %/°C, so on a −10 °C morning Voc is about 10% above its 25 °C datasheet value. That is the condition that can exceed the inverter's voltage limit.
  - q: What sets the minimum string length?
    a: On a hot afternoon Vmp falls; the string Vmp must stay above the inverter's MPPT minimum (and its start-up voltage), otherwise the inverter cannot track the maximum power point or clips power.
  - q: Which temperature should I use for the cold case?
    a: The record or design low ambient temperature for the site. The US NEC 690.7 allows the datasheet coefficient method used here; some codes give a fixed table of correction factors instead.
related: [ecology/solar-system-size, ecology/solar-output, electrical/cable-voltage-drop, electrical/battery-bank-size]
''', f'''
## How to use the solar string sizing calculator

Enter the module **Voc** and **Vmp** at STC and their **temperature coefficients** from the datasheet, the site's **lowest ambient temperature** and the **highest cell temperature**, then the inverter's **maximum DC voltage** and **MPPT range**. The calculator gives the temperature-corrected module voltages, the maximum and minimum modules per string, and the string voltages for the length you enter in **Modules per string**.

## Solar string sizing formulas

<p class="formula">V<sub>oc,cold</sub> = V<sub>oc</sub> × [1 + β<sub>Voc</sub> × (T<sub>min</sub> − 25 °C)] &nbsp;·&nbsp; N<sub>max</sub> = ⌊V<sub>max,inv</sub> ÷ V<sub>oc,cold</sub>⌋</p>

<p class="formula">V<sub>mp,hot</sub> = V<sub>mp</sub> × [1 + β<sub>Vmp</sub> × (T<sub>cell,max</sub> − 25 °C)] &nbsp;·&nbsp; N<sub>min</sub> = ⌈V<sub>MPPT,min</sub> ÷ V<sub>mp,hot</sub>⌉</p>

A string length is acceptable when N<sub>min</sub> ≤ N ≤ N<sub>max</sub>. For best energy yield, also keep N ≤ the MPPT-range limit so the cold-weather Vmp stays inside the tracking window.

## Worked example

A {sVoc:g} V Voc / {sVmp:g} V Vmp module (β<sub>Voc</sub> = {sbv:g} %/°C, β<sub>Vmp</sub> = {sbm:g} %/°C), site low {sTmin:g} °C, hot cell temperature {sThot:g} °C, inverter 1,000 V max, MPPT 200–850 V:

- V<sub>oc,cold</sub> = {sVoc:g} × (1 + 0.0027 × 25) = **{sVocc:.2f} V** → N<sub>max</sub> = ⌊1000 ÷ {sVocc:.2f}⌋ = **{sNmax}**
- V<sub>mp,hot</sub> = {sVmp:g} × (1 − 0.0035 × 45) = **{sVmph:.2f} V** → N<sub>min</sub> = ⌈200 ÷ {sVmph:.2f}⌉ = **{sNmin}**
- Cold Vmp = **{sVmpc:.2f} V** → at most **{sNmppt}** modules stay inside the 850 V MPPT limit
- A {sN}-module string: Voc on the coldest morning = **{sN*sVocc:.1f} V**, Vmp on the hottest afternoon = **{sN*sVmph:.1f} V** — both within limits

## Cold-weather Voc and maximum string length ({sVoc:g} V module, {sbv:g} %/°C)

| Lowest temperature | Module Voc | Max modules (600 V) | Max modules (1,000 V) | Max modules (1,500 V) |
|---|---|---|---|---|
{ss_rows}
## Practical notes

- Check **current** too: the string Isc × 1.25 (and parallel strings per MPPT) must not exceed the inverter's maximum input current.
- Use the inverter's **start-up voltage** if it is higher than the MPPT minimum.
- Bifacial and high-efficiency modules may have different coefficients — always take β from the exact datasheet.
- Shading, soiling and mismatch lower Vmp further; leave a margin above the MPPT minimum rather than designing exactly to it.
''')

# ---------------------------------------------------------------- Neutral current with harmonics
nI, nh3 = 100.0, 0.30
def neut(I, h3):
    I1 = I / math.sqrt(1 + h3 ** 2); I3 = h3 * I1; In = 3 * I3; h3r = I3 / I
    if h3r <= 0.15: Ides = I
    elif h3r <= 0.33: Ides = I / 0.86
    elif h3r <= 0.45: Ides = In / 0.86
    else: Ides = In
    return I1, I3, In, h3r, Ides
nI1, nI3, nIn, nh3r, nIdes = neut(nI, nh3)
assert 0.15 < nh3r <= 0.33
nt_rows = ''
for h in (0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80):
    a, b, c, d, e = neut(100, h)
    basis = 'phase' if d <= 0.33 else 'neutral'
    nt_rows += f"| {h*100:.0f}% | {d*100:.1f}% | {c:.1f} A | {c/100:.2f} | {basis} | {e:.1f} A |\n"
P('electrical', 'neutral-current-harmonics', f'''
title: Neutral Current Calculator with Third Harmonics (Neutral Sizing)
description: Calculate neutral current in a balanced three-phase four-wire circuit from third-harmonic content, and the IEC 60364-5-52 design current for sizing the cable.
category: electrical
{intro("In a balanced three-phase circuit the fundamental currents cancel in the neutral, but third harmonics are in phase and add — so a neutral feeding LED lighting, computers or drives can carry more current than the phases. This neutral current calculator finds the neutral current from the third-harmonic content and applies the IEC 60364-5-52 Annex E reduction factors, as explained in [neutral conductor sizing with harmonics](ib:neutral-conductor-sizing-harmonics) and [power system harmonics](ib:power-harmonics-explained).")}
keywords: [neutral current calculator, neutral current harmonics, third harmonic neutral current, neutral conductor sizing harmonics, triplen harmonics neutral, iec 60364-5-52 annex e, neutral sizing calculator]
updated: {D}
variables:
  - {{ id: I, label: Phase current (RMS), family: current, unit: A, default: {nI:g}, min: 0 }}
  - {{ id: h3, label: Third-harmonic current (% of fundamental), family: percent, unit: '%', default: {nh3*100:g}, min: 0, help: 'The 3rd-harmonic reading on a power-quality analyser, relative to the 50/60 Hz component.' }}
  - {{ id: I1, label: Fundamental phase current, family: current, unit: A, min: 0 }}
  - {{ id: I3, label: Third-harmonic phase current, family: current, unit: A, min: 0 }}
  - {{ id: In, label: Neutral current, family: current, unit: A, min: 0 }}
  - {{ id: r, label: Neutral ÷ phase current, min: 0, decimals: 3 }}
  - id: h3r
    label: Third harmonic as % of phase RMS current (IEC basis)
    family: percent
    unit: '%'
    min: 0
    bands:
      - {{ max: 0.15, label: '0–15%: size on phase current, factor 1.0', color: '#16a34a' }}
      - {{ max: 0.33, label: '15–33%: size on phase current, factor 0.86', color: '#eab308' }}
      - {{ max: 0.45, label: '33–45%: size on neutral current, factor 0.86', color: '#f97316' }}
      - {{ max: 1e9, label: 'Over 45%: size on neutral current, factor 1.0', color: '#dc2626' }}
  - {{ id: Ides, label: Design current for four-core cable selection, family: current, unit: A, min: 0 }}
equations:
  - I1 = I / sqrt(1 + h3^2)
  - I3 = h3 * I1
  - In = 3 * I3
  - r = In / I
  - h3r = I3 / I
  - Ides = (1 - step(h3r - 0.15)) * I + (step(h3r - 0.15) - step(h3r - 0.33)) * I / 0.86 + (step(h3r - 0.33) - step(h3r - 0.45)) * In / 0.86 + step(h3r - 0.45) * In
faq:
  - q: Why does the neutral carry third-harmonic current?
    a: The 50 Hz currents of the three phases are 120° apart and cancel in the neutral. Third-harmonic currents of the three phases are all in phase (3 × 120° = 360°), so they add, and the neutral carries three times the third-harmonic current of one phase.
  - q: Can the neutral current be higher than the phase current?
    a: Yes. With pure third harmonics the neutral current exceeds the phase current once the third harmonic is about 33% of the phase RMS current (about 35% of the fundamental). Circuits feeding many single-phase rectifier loads commonly reach 1.4–1.7 × phase current.
  - q: What are the IEC 60364-5-52 reduction factors for harmonics?
    a: For four- and five-core cables, Annex E gives 1.0 (size on phase current) up to 15% third harmonic, 0.86 (phase current) for 15–33%, 0.86 (neutral current) for 33–45%, and 1.0 (neutral current) above 45%, where the harmonic is a percentage of the phase current.
  - q: Do other harmonics add in the neutral?
    a: Only triplen harmonics (3rd, 9th, 15th …) add. The 5th, 7th, 11th and 13th cancel in a balanced system, like the fundamental. Load unbalance adds a further fundamental-frequency neutral current.
related: [electrical/thd, electrical/cable-voltage-drop, electrical/kw-to-amps, electrical/busbar-size]
''', f'''
## How to use the neutral current calculator

Enter the **phase RMS current** and the **third-harmonic current as a percentage of the fundamental** (the value a power-quality analyser shows in its harmonic spectrum). The calculator splits the phase current into its fundamental and third-harmonic parts, gives the neutral current, re-expresses the harmonic as a percentage of the phase RMS current (the basis IEC 60364-5-52 uses) and returns the design current for choosing a four-core or five-core cable.

## Neutral current formulas

<p class="formula">I₁ = I ÷ √(1 + h₃²) &nbsp;·&nbsp; I₃ = h₃ × I₁ &nbsp;·&nbsp; I<sub>N</sub> = 3 × I₃</p>

This assumes balanced phases and that the third harmonic is the only significant triplen harmonic. Other odd harmonics raise the phase RMS slightly but cancel in the neutral.

## Worked example

Phase current {nI:g} A with a third harmonic of {nh3*100:g}% of the fundamental:

- Fundamental I₁ = {nI:g} ÷ √(1 + 0.3²) = **{nI1:.2f} A**, third harmonic I₃ = **{nI3:.2f} A**
- Neutral current I<sub>N</sub> = 3 × {nI3:.2f} = **{nIn:.1f} A** ({nIn/nI:.3f} × phase current)
- As a share of the phase RMS current the harmonic is **{nh3r*100:.1f}%**, which falls in the 15–33% band
- Size the cable on the phase current with a factor of 0.86: design current = {nI:g} ÷ 0.86 = **{nIdes:.1f} A**

## Neutral current and design current for 100 A phase current

| 3rd harmonic (% of fundamental) | % of phase current | Neutral current | I<sub>N</sub> ÷ I | Sized on | Design current |
|---|---|---|---|---|---|
{nt_rows}
## Practical notes

- **Do not use a reduced neutral** on circuits feeding LED drivers, IT equipment, UPS or single-phase VFDs; many designers use a full-size or double-size neutral for such loads.
- The IEC factors apply to four- and five-core cables where the neutral is inside the same cable and adds heat; for single-core cables, check the neutral on its own current.
- Measure the harmonic spectrum at full load — percentages measured at light load often look high while the actual amps are small.
- Harmonic filters or 3rd-harmonic blocking transformers (zig-zag, delta windings) reduce the neutral current at the source.
''')

# ---------------------------------------------------------------- Motor starting voltage dip
mSt, mz, mP, meta, mpf, mk = 1000.0, 0.06, 110e3, 0.95, 0.87, 6.0
def dip(St, z, P, eta, pf, k):
    Ssc = St / z; Sst = k * P / (eta * pf) / 1000; return Ssc, Sst, Sst / (Ssc + Sst)
mSsc, mSst, mdip = dip(mSt, mz, mP, meta, mpf, mk)
md_rows = ''
for name, kk in (('Direct-on-line (DOL)', 6.0), ('Autotransformer, 80% tap', 6.0 * 0.64), ('Soft starter (≈3.5 × FLC)', 3.5), ('Star–delta', 2.0), ('VFD (≈1.2 × FLC)', 1.2)):
    _, s, d = dip(mSt, mz, mP, meta, mpf, kk)
    md_rows += f"| {name} | {kk:.2f} × FLC | {s:,.0f} kVA | {d*100:.2f}% |\n"
mt_rows = ''
for P_kw in (37, 75, 110, 160, 250):
    cells = []
    for St in (500, 1000, 2000):
        _, _, d = dip(St, 0.06 if St > 630 else 0.045, P_kw * 1e3, 0.95, 0.87, 6.0)
        cells.append(f"{d*100:.1f}%")
    mt_rows += f"| {P_kw} kW | " + ' | '.join(cells) + " |\n"
P('electrical', 'motor-starting-voltage-dip', f'''
title: Motor Starting Voltage Dip Calculator (Transformer kVA & Z%)
description: Estimate the voltage dip when a motor starts on a transformer, from motor kW, starting current, transformer kVA and Z% — for DOL, star-delta and soft starts.
category: electrical
{intro("When an induction motor starts it draws five to seven times its full-load current at a low power factor, and that current through the supply impedance pulls the bus voltage down. This motor starting voltage dip calculator estimates the dip from the motor's starting kVA and the transformer's short-circuit kVA, using the simplified method in [motor starting voltage dip calculation](ib:motor-starting-voltage-dip-calculation), and compares the [motor starting methods](ib:motor-starting-methods-compared).")}
keywords: [motor starting voltage dip calculator, voltage dip calculation motor starting, motor starting voltage drop, transformer voltage dip, dol starting voltage dip, motor starting kva, voltage sag motor start]
updated: {D}
variables:
  - {{ id: St, label: Transformer rating, suffix: kVA, default: {mSt:g}, min: 0 }}
  - {{ id: z, label: Transformer impedance (Z%), family: percent, unit: '%', default: {mz*100:g}, min: 0 }}
  - {{ id: P, label: Motor rated output, family: power, unit: kW, imperialUnit: hp, default: {mP/1e3:g}, min: 0 }}
  - {{ id: eta, label: Motor efficiency, family: percent, unit: '%', default: {meta*100:g}, min: 0, max: 1 }}
  - {{ id: pf, label: Motor full-load power factor, default: {mpf:g}, min: 0.01, max: 1 }}
  - {{ id: k, label: Starting current (× full-load current), default: {mk:g}, min: 0, help: 'DOL 6–7, star–delta ≈ 2, soft starter 2.5–4, VFD ≈ 1–1.5.' }}
  - {{ id: Ssc, label: Transformer short-circuit capacity, suffix: kVA, min: 0 }}
  - {{ id: Sst, label: Motor starting kVA, suffix: kVA, min: 0 }}
  - id: dip
    label: Voltage dip during starting
    family: percent
    unit: '%'
    min: 0
    bands:
      - {{ max: 0.05, label: Small — fine for most loads, color: '#16a34a' }}
      - {{ max: 0.10, label: Moderate — may cause visible lighting flicker, color: '#eab308' }}
      - {{ max: 0.15, label: High — check contactor drop-out and other motors, color: '#f97316' }}
      - {{ max: 1e9, label: Too high — use reduced-voltage starting or a bigger supply, color: '#dc2626' }}
  - {{ id: Vr, label: Remaining voltage during start, family: percent, unit: '%', min: 0 }}
equations:
  - Ssc = St / z
  - Sst = k * P / (eta * pf) / 1000
  - dip = Sst / (Ssc + Sst)
  - Vr = 1 - dip
faq:
  - q: How do you calculate the voltage dip when a motor starts?
    a: A simple estimate is ΔV = S_start ÷ (S_sc + S_start), where S_start is the motor's starting kVA (starting current multiple × rated kVA) and S_sc the short-circuit kVA of the supply (transformer kVA ÷ Z%).
  - q: What voltage dip is acceptable during motor starting?
    a: Common design limits are around 10–15% at the motor terminals so the motor still develops enough torque and contactors do not drop out, and lower — about 3–5% — at buses feeding lighting or sensitive electronics, where flicker is noticed.
  - q: Why is the result conservative?
    a: The formula adds impedance magnitudes as if they were in phase. In reality the motor's starting power factor (0.2–0.4) and the transformer's X/R ratio differ slightly, so the true dip is usually a little smaller. Upstream source impedance and cable impedance make it larger, so include them for long feeders.
  - q: How do I reduce motor starting voltage dip?
    a: Use star–delta, autotransformer or soft starting, or a VFD; start large motors one at a time; or supply them from a larger or lower-impedance transformer.
related: [electrical/motor-starting-current, electrical/transformer-short-circuit, electrical/three-phase-motor-power, electrical/transformer-size]
''', f'''
## How to use the motor starting voltage dip calculator

Enter the **transformer kVA** and **impedance**, the **motor output**, **efficiency**, **power factor** and the **starting current** as a multiple of full-load current. The calculator returns the transformer short-circuit capacity, the motor starting kVA and the voltage dip on the transformer secondary. Change the starting-current multiple to compare starting methods.

## Motor starting voltage dip formula

<p class="formula">S<sub>sc</sub> = S<sub>T</sub> ÷ Z% &nbsp;·&nbsp; S<sub>start</sub> = k × P ÷ (η × PF)</p>

<p class="formula">ΔV = S<sub>start</sub> ÷ (S<sub>sc</sub> + S<sub>start</sub>)</p>

This is the impedance-divider method: the motor's locked-rotor impedance and the supply impedance form a voltage divider. It assumes an infinite upstream grid; add the utility fault level for weak supplies.

## Worked example

A {mP/1e3:g} kW motor (η = {meta*100:g}%, PF = {mpf:g}) started direct-on-line at {mk:g} × FLC on a {mSt:,.0f} kVA, {mz*100:g}% transformer:

- Short-circuit capacity S<sub>sc</sub> = {mSt:,.0f} ÷ 0.06 = **{mSsc:,.0f} kVA**
- Starting kVA = {mk:g} × 110 ÷ (0.95 × 0.87) = **{mSst:,.0f} kVA**
- Voltage dip = {mSst:,.0f} ÷ ({mSsc:,.0f} + {mSst:,.0f}) = **{mdip*100:.2f}%**, leaving **{(1-mdip)*100:.1f}%** voltage during the start

## Effect of starting method (same motor and transformer)

| Starting method | Line current | Starting kVA | Voltage dip |
|---|---|---|---|
{md_rows}
## DOL voltage dip by motor and transformer size

| Motor | 500 kVA (4.5%) | 1,000 kVA (6%) | 2,000 kVA (6%) |
|---|---|---|---|
{mt_rows}
Assumes η = 95%, PF = 0.87 and 6 × FLC starting current.

## Practical notes

- The motor's torque falls with the square of voltage: a 15% dip leaves only about 72% of the rated starting torque.
- Long cables add impedance between the transformer and the motor; the dip at the motor terminals is then larger than the bus dip shown here.
- On generator supplies the dip is much larger because a generator's transient reactance (typically 15–30%) is far higher than a transformer's impedance.
''')

# ======================================================================= ELECTRONICS

# (Peukert runtime and p-value from z dropped: covered by peukerts-law and p-value from the 2026-11-07 batch)
# ---------------------------------------------------------------- Transimpedance amplifier
tIp, tRf, tCin, tGBW = 10e-6, 100e3, 20e-12, 10e6
tVo = tIp * tRf; tf3 = math.sqrt(tGBW / (2 * pi * tRf * tCin)); tCfb = math.sqrt(tCin / (pi * tRf * tGBW)); tCf45 = math.sqrt(tCin / (2 * pi * tRf * tGBW))
tia_rows = ''
for Rf in (10e3, 100e3, 1e6, 10e6):
    cells = []
    for GBW in (1e6, 10e6, 100e6):
        f = math.sqrt(GBW / (2 * pi * Rf * tCin))
        cells.append(f"{f/1e3:,.1f} kHz" if f < 1e6 else f"{f/1e6:.2f} MHz")
    tia_rows += f"| {Rf/1e3:,.0f} kΩ | " + ' | '.join(cells) + f" | {math.sqrt(tCin/(pi*Rf*10e6))*1e12:.2f} pF |\n"
P('electronics', 'transimpedance-amplifier', f'''
title: Transimpedance Amplifier Calculator (Photodiode TIA Rf, Cf, Bandwidth)
description: Design a photodiode transimpedance amplifier: output voltage from Rf, maximum bandwidth from op-amp GBW and input capacitance, and the feedback capacitor Cf.
category: electronics
{intro("A transimpedance amplifier turns a photodiode's tiny current into a voltage, Vout = I × Rf, but the photodiode's capacitance and the op-amp's gain-bandwidth limit how fast it can be. This transimpedance amplifier calculator gives the output voltage, the achievable −3 dB bandwidth and the feedback capacitor for a flat (Butterworth) or 45° phase-margin response — see how a [transimpedance amplifier works with a photodiode](ib:transimpedance-amplifier-photodiode).")}
keywords: [transimpedance amplifier calculator, tia calculator, photodiode amplifier calculator, transimpedance amplifier bandwidth, feedback capacitor transimpedance, photodiode tia design, current to voltage converter op amp]
updated: {D}
variables:
  - {{ id: Ip, label: Photodiode current, family: current, unit: uA, default: {tIp*1e6:g}, min: 0 }}
  - {{ id: Rf, label: Feedback resistor Rf, family: resistance, unit: kohm, default: {tRf/1e3:g}, min: 0 }}
  - {{ id: Cin, label: Total input capacitance (photodiode + op-amp), family: capacitance, unit: pF, default: {tCin*1e12:g}, min: 0 }}
  - {{ id: GBW, label: Op-amp gain-bandwidth product, family: frequency, unit: MHz, default: {tGBW/1e6:g}, min: 0 }}
  - {{ id: Vout, label: Output voltage (magnitude), family: voltage, unit: V, min: 0 }}
  - {{ id: f3, label: Achievable −3 dB bandwidth, family: frequency, unit: kHz, min: 0 }}
  - {{ id: Cfb, label: Feedback capacitor for flat (Butterworth) response, family: capacitance, unit: pF, min: 0 }}
  - {{ id: Cf45, label: Minimum feedback capacitor (45° phase margin), family: capacitance, unit: pF, min: 0 }}
equations:
  - Vout = Ip * Rf
  - f3 = sqrt(GBW / (2 * pi * Rf * Cin))
  - Cfb = sqrt(Cin / (pi * Rf * GBW))
  - Cf45 = sqrt(Cin / (2 * pi * Rf * GBW))
faq:
  - q: What is the gain of a transimpedance amplifier?
    a: The transimpedance gain is Rf in volts per amp — Vout = I × Rf. A 1 MΩ feedback resistor gives 1 V per µA.
  - q: What limits transimpedance amplifier bandwidth?
    a: The input capacitance (photodiode junction plus op-amp input) and the op-amp GBW. With the right feedback capacitor the −3 dB bandwidth is about √(GBW ÷ (2π Rf Cin)), so raising Rf tenfold cuts bandwidth by about √10.
  - q: Why does a TIA need a feedback capacitor?
    a: The input capacitance creates a rising noise gain that meets the op-amp's falling open-loop gain at a steep angle, so without Cf the circuit peaks or oscillates. Cf adds a zero that restores phase margin.
  - q: How do I get more bandwidth from a photodiode amplifier?
    a: Reverse-bias the photodiode to reduce its capacitance, choose a smaller-area photodiode, use a higher-GBW op-amp with low input capacitance, or use a lower Rf followed by a second gain stage.
related: [electronics/op-amp-gain, electronics/rc-filter, electronics/snr, electronics/adc-resolution]
''', f'''
## How to use the transimpedance amplifier calculator

Enter the **photodiode current**, the **feedback resistor**, the **total input capacitance** (photodiode junction capacitance at its bias plus the op-amp's common-mode and differential input capacitance) and the op-amp's **gain-bandwidth product**. The calculator returns the output voltage, the achievable bandwidth and two values of feedback capacitor: the larger gives a flat Butterworth response, the smaller is the minimum for a 45° phase margin (faster, with some peaking). To find Rf for a target output, press × on Rf.

## Transimpedance amplifier formulas

<p class="formula">V<sub>out</sub> = I<sub>p</sub> × R<sub>f</sub> &nbsp;·&nbsp; f<sub>−3dB</sub> ≈ √(GBW ÷ (2π R<sub>f</sub> C<sub>in</sub>))</p>

<p class="formula">C<sub>f</sub> (Butterworth) ≈ √(C<sub>in</sub> ÷ (π R<sub>f</sub> GBW)) &nbsp;·&nbsp; C<sub>f</sub> (45°) ≈ √(C<sub>in</sub> ÷ (2π R<sub>f</sub> GBW))</p>

These approximations hold when C<sub>f</sub> is much smaller than C<sub>in</sub>, which is the usual case.

## Worked example

A photodiode with {tCin*1e12:g} pF total capacitance producing {tIp*1e6:g} µA, R<sub>f</sub> = {tRf/1e3:g} kΩ and a {tGBW/1e6:g} MHz op-amp:

- V<sub>out</sub> = {tIp*1e6:g} µA × {tRf/1e3:g} kΩ = **{tVo:g} V**
- Bandwidth = √(10 MHz ÷ (2π × 100 kΩ × 20 pF)) = **{tf3/1e3:.0f} kHz**
- Feedback capacitor: **{tCfb*1e12:.2f} pF** for a flat response (minimum **{tCf45*1e12:.2f} pF** for 45° phase margin) — use the nearest standard value, e.g. 2.7 pF

## Achievable bandwidth (20 pF input capacitance)

| R<sub>f</sub> | GBW 1 MHz | GBW 10 MHz | GBW 100 MHz | C<sub>f</sub> at 10 MHz |
|---|---|---|---|---|
{tia_rows}
## Practical notes

- Values of C<sub>f</sub> below about 0.5 pF are swamped by the resistor's own parasitic capacitance (≈ 0.1–0.2 pF for an 0805 part); use a T-network or a lower R<sub>f</sub>.
- Choose an op-amp with **FET or CMOS inputs** — bias current flows through R<sub>f</sub> and appears directly as an output offset.
- Photovoltaic mode (zero bias) gives the lowest dark current and noise; photoconductive mode (reverse bias) gives lower capacitance and higher speed.
- Thermal noise of R<sub>f</sub> is √(4kT/R<sub>f</sub>) in current terms, so a larger R<sub>f</sub> improves signal-to-noise as well as gain.
''')

# ======================================================================= ENGINEERING (reliability)

# ---------------------------------------------------------------- Weibull reliability
wb, weta, wt = 1.5, 10000.0, 5000.0
def weib(b, eta, t):
    R = math.exp(-(t / eta) ** b); h = b / eta * (t / eta) ** (b - 1)
    return R, h, eta * math.gamma(1 + 1 / b), eta * (-math.log(0.9)) ** (1 / b)
wR, wh, wM, wB10 = weib(wb, weta, wt)
wr_rows = ''
for b in (0.5, 1.0, 1.5, 2.0, 3.5):
    wr_rows += f"| {b:g} | " + ' | '.join(f"{math.exp(-(x) ** b)*100:.1f}%" for x in (0.1, 0.5, 1.0, 2.0)) + f" | {math.gamma(1+1/b):.4f} | {(-math.log(0.9))**(1/b):.4f} |\n"
P('engineering', 'weibull-reliability', f'''
title: Weibull Reliability Calculator (R(t), Failure Rate, MTTF, B10)
description: Calculate Weibull reliability, probability of failure, hazard rate, mean life (MTTF) and B10 life from the shape parameter β and characteristic life η.
category: engineering
{intro("The Weibull distribution is the standard model for component life because its shape parameter β covers early failures (β < 1), random failures (β = 1) and wear-out (β > 1). This Weibull reliability calculator gives the reliability and probability of failure at a chosen time, the instantaneous failure rate, the mean time to failure and the B10 life from β and the characteristic life η.")}
keywords: [weibull reliability calculator, weibull distribution calculator, weibull failure rate, weibull mttf, b10 life calculator, weibull shape parameter beta, characteristic life eta]
updated: {D}
variables:
  - {{ id: beta, label: Shape parameter β, default: {wb:g}, min: 0.01 }}
  - {{ id: eta, label: Characteristic life η (scale), family: seconds, unit: h, default: {weta:g}, min: 0 }}
  - {{ id: t, label: Operating time t, family: seconds, unit: h, default: {wt:g}, min: 0 }}
  - {{ id: R, label: Reliability R(t), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: F, label: Probability of failure F(t), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: hz, label: Hazard (failure) rate at t, suffix: per 10⁶ h, min: 0 }}
  - {{ id: MTTF, label: Mean life (MTTF), family: seconds, unit: h, min: 0 }}
  - {{ id: B10, label: B10 life (10% failed), family: seconds, unit: h, min: 0 }}
equations:
  - R = exp(-(t / eta)^beta)
  - F = 1 - R
  - hz = 3.6e9 * beta / eta * (t / eta)^(beta - 1)
  - MTTF = eta * gamma(1 + 1 / beta)
  - B10 = eta * (-ln(0.9))^(1 / beta)
faq:
  - q: What is the Weibull reliability function?
    a: R(t) = exp(−(t/η)^β). At t = η the reliability is always e⁻¹ ≈ 36.8%, whatever β is — so η is the time by which 63.2% of units have failed.
  - q: What does the shape parameter β mean?
    a: β < 1 means a falling failure rate (infant mortality), β = 1 a constant failure rate (the exponential distribution, random failures) and β > 1 a rising failure rate (wear-out). Bearings are typically around 1.1–1.5 and fatigue or corrosion failures 2–4.
  - q: How is MTTF calculated for a Weibull distribution?
    a: MTTF = η × Γ(1 + 1/β), where Γ is the gamma function. For β = 1 it equals η; for β = 2 it is 0.886 η; for β = 3.5 it is about 0.9 η.
  - q: What is B10 life?
    a: The time by which 10% of the population has failed (90% reliability), B10 = η × (−ln 0.9)^(1/β). It is the usual rating life for rolling bearings.
related: [engineering/availability-mtbf, engineering/bearing-life, statistics/exponential-distribution, engineering/pfd-avg]
''', f'''
## How to use the Weibull reliability calculator

Enter the **shape parameter β** and the **characteristic life η** (from a Weibull plot of failure data or a supplier's life test) and the **operating time t**. The calculator returns the reliability and probability of failure at t, the hazard rate at t in failures per million hours, the mean life and the B10 life. To find the time for a target reliability, enter R and press × on t.

## Weibull reliability formulas

<p class="formula">R(t) = e<sup>−(t/η)<sup>β</sup></sup> &nbsp;·&nbsp; F(t) = 1 − R(t)</p>

<p class="formula">h(t) = (β/η)(t/η)<sup>β−1</sup> &nbsp;·&nbsp; MTTF = η Γ(1 + 1/β) &nbsp;·&nbsp; B10 = η (−ln 0.9)<sup>1/β</sup></p>

## Worked example

A pump seal with β = {wb:g} and η = {weta:,.0f} h, after t = {wt:,.0f} h:

- (t/η)<sup>β</sup> = 0.5<sup>1.5</sup> = {0.5**1.5:.4f}, so R = e<sup>−{0.5**1.5:.4f}</sup> = **{wR*100:.2f}%** and F = **{(1-wR)*100:.2f}%**
- Hazard rate = (1.5 ÷ 10,000) × 0.5<sup>0.5</sup> = **{wh*1e6:.1f} per 10⁶ h** — and rising, because β > 1
- MTTF = 10,000 × Γ(1.667) = **{wM:,.0f} h**; B10 life = **{wB10:,.0f} h**

## Weibull reliability at multiples of η

| β | t = 0.1η | t = 0.5η | t = η | t = 2η | MTTF ÷ η | B10 ÷ η |
|---|---|---|---|---|---|---|
{wr_rows}
## Practical notes

- With β > 1, **preventive replacement** before wear-out makes sense; with β ≤ 1 it does not — replacing a part early only resets the infant-mortality period.
- Fit β and η from field data with a Weibull probability plot (median ranks) or maximum likelihood; at least 5–10 failures give a usable β.
- A three-parameter Weibull adds a failure-free time γ: replace t with (t − γ) when no failures can occur before γ.
- For β = 1 the result equals the exponential model used for MTBF and SIL calculations, with η = MTBF.
''')

# ---------------------------------------------------------------- Safe failure fraction
fS, fDD, fDU = 300.0, 450.0, 50.0
fSFF = (fS + fDD) / (fS + fDD + fDU); fDC = fDD / (fDD + fDU)
P('engineering', 'safe-failure-fraction', f'''
title: Safe Failure Fraction Calculator (SFF, Diagnostic Coverage)
description: Calculate the safe failure fraction (SFF) and diagnostic coverage from λS, λDD and λDU failure rates, with IEC 61508 SIL limits for Type A and Type B devices.
category: engineering
{intro("The safe failure fraction is the share of a device's failures that are either safe or dangerous but detected by diagnostics, and together with hardware fault tolerance it caps the SIL a subsystem can claim. This safe failure fraction calculator works out SFF and diagnostic coverage from the FMEDA failure rates and shows the IEC 61508 architectural limits — background in [safe failure fraction in functional safety](ib:safe-failure-fraction-functional-safety) and [hardware fault tolerance and SFF](ib:hardware-fault-tolerance-sff-iec-61508).")}
keywords: [safe failure fraction calculator, sff calculator, sff iec 61508, diagnostic coverage calculator, lambda du lambda dd, hardware fault tolerance sil, sff type a type b]
updated: {D}
variables:
  - {{ id: lS, label: Safe failure rate λS, suffix: FIT, default: {fS:g}, min: 0, help: '1 FIT = 1 failure per 10⁹ hours. Use the FMEDA or safety-manual values.' }}
  - {{ id: lDD, label: Dangerous detected failure rate λDD, suffix: FIT, default: {fDD:g}, min: 0 }}
  - {{ id: lDU, label: Dangerous undetected failure rate λDU, suffix: FIT, default: {fDU:g}, min: 0 }}
  - {{ id: lt, label: Total failure rate, suffix: FIT, min: 0 }}
  - id: SFF
    label: Safe failure fraction (SFF)
    family: percent
    unit: '%'
    min: 0
    max: 1
    bands:
      - {{ max: 0.5999999, label: Below 60%, color: '#dc2626' }}
      - {{ max: 0.8999999, label: 60% to below 90%, color: '#f97316' }}
      - {{ max: 0.9899999, label: 90% to below 99%, color: '#eab308' }}
      - {{ max: 1e9, label: 99% or more, color: '#16a34a' }}
  - {{ id: DC, label: Diagnostic coverage (DC), family: percent, unit: '%', min: 0, max: 1 }}
  - {{ id: mttf, label: MTTF from the total failure rate, suffix: years, min: 0 }}
equations:
  - lt = lS + lDD + lDU
  - SFF = (lS + lDD) / lt
  - DC = lDD / (lDD + lDU)
  - mttf = 1e9 / lt / 8766
faq:
  - q: How is safe failure fraction calculated?
    a: SFF = (λS + λDD) ÷ (λS + λDD + λDU) — all safe failures plus dangerous detected failures, divided by the total failure rate. Only the dangerous undetected failures count against it.
  - q: What SFF is needed for SIL 2?
    a: Under IEC 61508 Route 1H with no redundancy (HFT 0), a Type A device needs SFF ≥ 60% and a Type B device SFF ≥ 90% for SIL 2. With HFT 1, Type A needs no minimum (below 60% is enough) and Type B needs SFF ≥ 60%.
  - q: What is the difference between SFF and diagnostic coverage?
    a: Diagnostic coverage looks only at dangerous failures, DC = λDD ÷ (λDD + λDU). SFF also counts safe failures, so a device with many safe failures can have a high SFF even with modest diagnostics.
  - q: What are Type A and Type B devices?
    a: Type A devices are simple, with well-known failure modes and field data (relays, solenoid valves, simple transmitters). Type B devices contain complex components such as microprocessors whose failure modes are not fully known — most smart transmitters and logic solvers.
related: [engineering/pfd-avg, engineering/availability-mtbf, engineering/weibull-reliability, engineering/instrument-accuracy]
''', f'''
## How to use the safe failure fraction calculator

Enter the **safe**, **dangerous detected** and **dangerous undetected** failure rates in FIT from the device's FMEDA report or safety manual (λS can include λSD + λSU, and λDD includes failures that the diagnostics drive to a safe state). The calculator returns the total failure rate, the SFF with its IEC 61508 band, the diagnostic coverage and the equivalent MTTF.

## Safe failure fraction formula

<p class="formula">SFF = (λ<sub>S</sub> + λ<sub>DD</sub>) ÷ (λ<sub>S</sub> + λ<sub>DD</sub> + λ<sub>DU</sub>) &nbsp;·&nbsp; DC = λ<sub>DD</sub> ÷ (λ<sub>DD</sub> + λ<sub>DU</sub>)</p>

## Worked example

A pressure transmitter with λ<sub>S</sub> = {fS:g} FIT, λ<sub>DD</sub> = {fDD:g} FIT and λ<sub>DU</sub> = {fDU:g} FIT:

- Total failure rate = **{fS+fDD+fDU:g} FIT** (MTTF ≈ {1e9/(fS+fDD+fDU)/8766:,.0f} years)
- SFF = ({fS:g} + {fDD:g}) ÷ {fS+fDD+fDU:g} = **{fSFF*100:.2f}%**
- DC = {fDD:g} ÷ ({fDD:g} + {fDU:g}) = **{fDC*100:.0f}%**
- As a Type B device with HFT 0 it is limited to **SIL 2** (90–99% SFF); in a 1oo2 arrangement (HFT 1) it could be used up to SIL 3

## Maximum SIL by SFF and hardware fault tolerance (IEC 61508-2, Route 1H)

| SFF | Type A, HFT 0 | Type A, HFT 1 | Type A, HFT 2 | Type B, HFT 0 | Type B, HFT 1 | Type B, HFT 2 |
|---|---|---|---|---|---|---|
| < 60% | SIL 1 | SIL 2 | SIL 3 | Not allowed | SIL 1 | SIL 2 |
| 60% – < 90% | SIL 2 | SIL 3 | SIL 4 | SIL 1 | SIL 2 | SIL 3 |
| 90% – < 99% | SIL 3 | SIL 4 | SIL 4 | SIL 2 | SIL 3 | SIL 4 |
| ≥ 99% | SIL 3 | SIL 4 | SIL 4 | SIL 3 | SIL 4 | SIL 4 |

HFT N means the subsystem still works after N dangerous faults (1oo1 = 0, 1oo2 = 1, 1oo3 = 2).

## Practical notes

- The architectural limit is separate from the **PFDavg** limit — a SIF must meet both, and the PFDavg depends mainly on λ<sub>DU</sub> and the proof-test interval.
- IEC 61511 (process sector) allows Route 2H or its own HFT table based on prior use instead of SFF; check which route your project uses.
- "No effect" and "no part" failures are excluded from the SFF calculation in IEC 61508 Edition 2.
- Detected failures only count as safe if the diagnostic response actually takes the process to a safe state (or alarms and the repair is done within the MTTR assumed).
''')

# ---------------------------------------------------------------- Arrhenius acceleration factor
aEa, aTu, aTs, aN, ath, aCL = 0.7, 55.0, 125.0, 77, 1000.0, 0.60
kB = 8.617333262e-5
aAF = math.exp(aEa / kB * (1 / (aTu + 273.15) - 1 / (aTs + 273.15)))
aHeq = aN * ath * aAF; alam = -math.log(1 - aCL) / aHeq; aFIT = alam * 1e9; aMTTF = 1 / alam
ae_rows = ''
for Ea in (0.3, 0.5, 0.7, 1.0):
    ae_rows += f"| {Ea:g} eV | " + ' | '.join(f"{math.exp(Ea/kB*(1/(Tu+273.15)-1/(398.15)) ):,.1f}" for Tu in (25, 40, 55, 85)) + " |\n"
P('engineering', 'acceleration-factor', f'''
title: Arrhenius Acceleration Factor Calculator (HTOL, FIT & MTTF)
description: Calculate the Arrhenius acceleration factor between stress and use temperatures, equivalent device-hours, and FIT rate and MTTF from a zero-failure life test.
category: engineering
{intro("Accelerated life tests run parts hot so that a few weeks represent years of field use, and the Arrhenius model converts test hours into equivalent use hours. This acceleration factor calculator gives the Arrhenius acceleration factor from the activation energy and the two temperatures, then the upper-bound failure rate in FIT and the MTTF demonstrated by a test with zero failures at your confidence level.")}
keywords: [acceleration factor calculator, arrhenius acceleration factor, htol calculator, fit rate calculator, accelerated life test calculator, activation energy reliability, mttf from life test]
updated: {D}
variables:
  - {{ id: Ea, label: Activation energy Ea, suffix: eV, default: {aEa:g}, min: 0, help: 'JEDEC and many suppliers use 0.7 eV for general semiconductor failure mechanisms.' }}
  - {{ id: Tu, label: Use (field) temperature, family: temperature, unit: C, imperialUnit: F, default: {aTu:g}, min: 0 }}
  - {{ id: Ts, label: Stress (test) temperature, family: temperature, unit: C, imperialUnit: F, default: {aTs:g}, min: 0 }}
  - {{ id: N, label: Number of devices tested, default: {aN}, min: 0 }}
  - {{ id: th, label: Test duration, family: seconds, unit: h, default: {ath:g}, min: 0 }}
  - {{ id: CL, label: Confidence level, family: percent, unit: '%', default: {aCL*100:g}, min: 0, max: 0.9999 }}
  - {{ id: AF, label: Acceleration factor, min: 0, decimals: 2 }}
  - {{ id: Heq, label: Equivalent device-hours at use temperature, suffix: device-h, min: 0 }}
  - {{ id: FIT, label: Failure rate upper bound (0 failures), suffix: FIT, min: 0 }}
  - {{ id: MTTF, label: Demonstrated MTTF (lower bound), family: seconds, unit: h, min: 0 }}
  - {{ id: MTTFy, label: Demonstrated MTTF in years, suffix: years, min: 0 }}
equations:
  - AF = exp(Ea / 8.617333262e-5 * (1 / Tu - 1 / Ts))
  - Heq = N * th * AF / 3600
  - FIT = -ln(1 - CL) / Heq * 1e9
  - MTTF = Heq * 3600 / (-ln(1 - CL))
  - MTTFy = MTTF / 3600 / 8766
faq:
  - q: What is the Arrhenius acceleration factor formula?
    a: AF = exp[(Ea ÷ k) × (1/T_use − 1/T_stress)], with temperatures in kelvin and Boltzmann's constant k = 8.617 × 10⁻⁵ eV/K. It is the ratio of the failure rate at the stress temperature to that at the use temperature.
  - q: What activation energy should I use?
    a: Use the value for the failure mechanism if it is known — for example around 0.3–0.5 eV for oxide defects and 0.5–0.9 eV for electromigration. 0.7 eV is the common default for semiconductor HTOL reports; a lower Ea gives a smaller, more conservative AF.
  - q: How is the FIT rate calculated with zero failures?
    a: With no failures, the upper confidence bound on the failure rate is λ = −ln(1 − CL) ÷ (device-hours × AF). At 60% confidence −ln(0.4) = 0.916, at 90% it is 2.303. This equals the chi-square method χ²(CL, 2) ÷ (2 × device-hours × AF).
  - q: Why is MTTF from a life test so large?
    a: Because it is an MTTF for random failures during the useful life, not a wear-out lifetime. An MTTF of 1,000 years means that in a population of 1,000 devices about one fails per year — not that a single device lasts 1,000 years.
related: [chemistry/arrhenius-equation, engineering/weibull-reliability, engineering/availability-mtbf, electronics/capacitor-lifetime]
''', f'''
## How to use the acceleration factor calculator

Enter the **activation energy**, the **use temperature** (junction or component temperature in the field) and the **stress temperature** of the test. That gives the acceleration factor. To turn a life test into a failure rate, also enter the **number of devices**, the **test hours** and the **confidence level**; the calculator assumes the test finished with **zero failures** and returns the equivalent device-hours, the upper-bound FIT rate and the lower-bound MTTF.

## Acceleration factor formulas

<p class="formula">AF = exp[(E<sub>a</sub> ÷ k)(1/T<sub>use</sub> − 1/T<sub>stress</sub>)] &nbsp;·&nbsp; k = 8.617 × 10⁻⁵ eV/K</p>

<p class="formula">λ<sub>upper</sub> = −ln(1 − CL) ÷ (N × t × AF) &nbsp;·&nbsp; FIT = λ × 10⁹ h &nbsp;·&nbsp; MTTF = 1/λ</p>

## Worked example

A JEDEC-style HTOL test of {aN} devices for {ath:,.0f} h at {aTs:g} °C with no failures, field use at {aTu:g} °C, E<sub>a</sub> = {aEa:g} eV, 60% confidence:

- AF = exp[(0.7 ÷ 8.617 × 10⁻⁵) × (1/328.15 − 1/398.15)] = **{aAF:.2f}**
- Equivalent device-hours = {aN} × {ath:,.0f} × {aAF:.2f} = **{aHeq:,.0f} h**
- Failure rate ≤ 0.916 ÷ {aHeq:,.0f} = **{aFIT:.0f} FIT**
- MTTF ≥ **{aMTTF:,.0f} h** (about {aMTTF/8766:,.0f} years)

## Acceleration factor for a 125 °C stress test

| E<sub>a</sub> | Use 25 °C | Use 40 °C | Use 55 °C | Use 85 °C |
|---|---|---|---|---|
{ae_rows}
## Practical notes

- Use the **junction temperature** (ambient + power × θ<sub>JA</sub>) for both test and use, not the oven or room temperature.
- The Arrhenius model covers temperature-driven mechanisms only. Humidity (Peck model, 85 °C/85% RH), voltage and temperature cycling (Coffin–Manson) need their own acceleration factors.
- With r failures, replace −ln(1 − CL) by χ²(CL; 2r + 2) ÷ 2 — for example 2.02 at 60% confidence and 1 failure.
- Don't push the stress temperature past the point where new failure mechanisms appear (package glass transition, solder melting), or the acceleration factor is meaningless.
''')

# ======================================================================= CHEMISTRY

# ---------------------------------------------------------------- TDS from conductivity
cEC, cT, ca, ck = 750.0, 20.0, 2.0, 0.65
cEC25 = cEC / (1 + ca / 100 * (cT - 25)); cTDS = ck * cEC25
tds_rows = ''
for name, ec in (('Pure (RO / distilled) water', 5), ('Rain water', 50), ('Soft tap water', 200), ('Typical tap water', 500), ('Hard ground water', 1000), ('Brackish water', 5000), ('Sea water', 53000)):
    tds_rows += f"| {name} | {ec:,} µS/cm | {0.5*ec:,.0f} mg/L | {0.65*ec:,.0f} mg/L | {0.7*ec:,.0f} mg/L |\n"
P('chemistry', 'tds-conductivity', f'''
title: TDS to Conductivity Calculator (EC µS/cm to ppm, mg/L)
description: Convert electrical conductivity (EC) in µS/cm to total dissolved solids (TDS) in mg/L or ppm, with temperature compensation to 25 °C and an adjustable factor.
category: chemistry
{intro("Conductivity meters measure how well water carries current, and total dissolved solids are estimated from it with a conversion factor of about 0.5–0.7. This TDS to conductivity calculator converts EC in µS/cm to TDS in mg/L (ppm), first correcting the reading to 25 °C, and works in reverse to give the conductivity for a target TDS — see how [electrical conductivity](ib:electrical-conductivity-explained) and a [conductivity sensor](ib:conductivity-sensor-working) work.")}
keywords: [tds to conductivity calculator, conductivity to tds, ec to ppm calculator, us/cm to ppm, tds calculator, tds conversion factor, conductivity temperature compensation]
updated: {D}
variables:
  - {{ id: EC, label: Measured conductivity, suffix: µS/cm, default: {cEC:g}, min: 0 }}
  - {{ id: T, label: Water temperature, family: temperature, unit: C, imperialUnit: F, default: {cT:g} }}
  - {{ id: a, label: Temperature coefficient, suffix: '%/°C', default: {ca:g}, min: 0, help: 'About 2 %/°C for most natural waters; set 0 if your meter already compensates to 25 °C.' }}
  - {{ id: k, label: TDS conversion factor, default: {ck:g}, min: 0, help: 'NaCl solutions ≈ 0.5; natural waters 0.55–0.75 (often 0.65).' }}
  - {{ id: EC25, label: Conductivity at 25 °C, suffix: µS/cm, min: 0 }}
  - {{ id: ECm, label: Conductivity at 25 °C in mS/cm, suffix: mS/cm, min: 0, decimals: 4 }}
  - id: TDS
    label: Total dissolved solids (TDS)
    suffix: mg/L (ppm)
    min: 0
    bands:
      - {{ max: 300, label: Excellent for drinking (WHO taste rating), color: '#16a34a' }}
      - {{ max: 600, label: Good, color: '#22c55e' }}
      - {{ max: 900, label: Fair, color: '#eab308' }}
      - {{ max: 1200, label: Poor, color: '#f97316' }}
      - {{ max: 1e9, label: Unacceptable taste for drinking, color: '#dc2626' }}
equations:
  - EC25 = EC / (1 + a / 100 * (T - 298.15))
  - ECm = EC25 / 1000
  - TDS = k * EC25
faq:
  - q: How do you convert conductivity to TDS?
    a: TDS (mg/L) = k × EC (µS/cm at 25 °C), with k usually between 0.55 and 0.75 for natural waters. A factor of 0.5 is used for sodium chloride solutions and 0.65–0.7 for typical fresh water.
  - q: Is TDS in ppm the same as mg/L?
    a: For dilute water, yes — 1 mg/L ≈ 1 ppm because a litre of water weighs about 1 kg. In sea water and brines the density is higher, so the two differ by a few percent.
  - q: Why does conductivity need temperature compensation?
    a: Ions move faster in warm water, so conductivity rises by about 2% per °C. Readings are referred to 25 °C so that samples measured at different temperatures can be compared.
  - q: What TDS is safe for drinking water?
    a: The WHO gives no health-based limit, but taste is rated excellent below 300 mg/L, good up to 600 and unacceptable above about 1,200. India's BIS IS 10500 sets 500 mg/L as acceptable and 2,000 mg/L as permissible where no other source exists.
related: [chemistry/ppm, chemistry/water-hardness, chemistry/dissolved-oxygen-saturation, chemistry/molarity]
''', f'''
## How to use the TDS to conductivity calculator

Enter the **measured conductivity** in µS/cm, the **water temperature** and the **temperature coefficient** (2 %/°C is typical; enter 0 if your meter already shows a 25 °C compensated value), then the **TDS factor**. The calculator gives the conductivity at 25 °C and the TDS in mg/L (ppm). To find the conductivity that corresponds to a target TDS, enter the TDS and press × on the measured conductivity.

## TDS and conductivity formulas

<p class="formula">EC<sub>25</sub> = EC<sub>T</sub> ÷ [1 + α (T − 25 °C)] &nbsp;·&nbsp; TDS = k × EC<sub>25</sub></p>

The factor k depends on which ions are dissolved: about 0.5 for NaCl, 0.55–0.7 for most fresh waters, and up to 0.8 for waters rich in sulphate. For accurate work, calibrate k against a gravimetric TDS test (evaporation at 180 °C) for your water.

## Worked example

A sample reads {cEC:g} µS/cm at {cT:g} °C (α = {ca:g} %/°C, k = {ck:g}):

- EC<sub>25</sub> = {cEC:g} ÷ [1 + 0.02 × (20 − 25)] = {cEC:g} ÷ 0.9 = **{cEC25:.1f} µS/cm**
- TDS = {ck:g} × {cEC25:.1f} = **{cTDS:.0f} mg/L** — rated "good" for taste and just above India's 500 mg/L acceptable limit

## Typical conductivity and TDS

| Water | Conductivity (25 °C) | TDS, k = 0.5 | TDS, k = 0.65 | TDS, k = 0.7 |
|---|---|---|---|---|
{tds_rows}
Values are typical; real samples vary widely.

## Practical notes

- **1 mS/cm = 1,000 µS/cm**; some meters show EC in mS/cm or dS/m (1 dS/m = 1 mS/cm), and hydroponic "CF" units are EC in mS/cm × 10.
- Different TDS meters use different built-in factors (0.5 "NaCl", 0.7 "442"), so two meters can show different ppm for the same water — compare EC, not ppm.
- Conductivity is not a measure of purity against non-ionic contaminants: sugar, oils and many organics do not conduct and are not counted.
- Keep the conductivity cell clean and calibrated with a standard (e.g. 1,413 µS/cm KCl); the cell constant drifts as electrodes foul.
''')

print(len(DESC), 'pages:', ' '.join(DESC))
