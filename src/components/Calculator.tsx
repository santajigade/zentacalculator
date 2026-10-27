/** @jsxImportSource preact */
import { useEffect, useMemo, useRef, useState } from 'preact/hooks';
import { compileAll, solve, fmtNum, type SolveResult } from '../lib/solver.ts';
import { findUnit, getUnits, toBase, fromBase } from '../lib/units.ts';
import Chart from './Chart.tsx';
import { SITE } from "../site.config.ts";
import { detectRegion, type Region } from "../lib/region.ts";
import { parseList, listStats } from "../lib/stats.ts";

export interface VarSpec {
  id: string; label: string; family: string; unit?: string; imperialUnit?: string; default?: number;
  min?: number; max?: number; prefix?: string; suffix?: string; help?: string; decimals?: number;
  options?: { label: string; value: number }[];
  bands?: { max: number; label: string; color: string }[];
}
export interface CalcSpec {
  title: string; variables: VarSpec[]; equations: string[]; freedom?: number;
  chart?: { x: string; y: string; from?: number; to?: number };
  dataset?: { label: string; default?: string; placeholder?: string; help?: string };
}

const DAY = 86400000;
const todayDays = () => { const d = new Date(); return Math.floor(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / DAY); };
const isoDate = (days: number) => new Date(Math.round(days) * DAY).toISOString().slice(0, 10);
const hhmm = (h: number) => { const m = Math.round((((h % 24) + 24) % 24) * 60) % 1440; return `${String(Math.floor(m / 60)).padStart(2, '0')}:${String(m % 60).padStart(2, '0')}`; };
const parseNum = (s: string) => {
  const t = s.replace(/[,\s_]/g, '');
  if (t === '' || t === '-' || t === '.') return NaN;
  return Number(t);
};

export default function Calculator({ spec, path, embed = false }: { spec: CalcSpec; path: string; embed?: boolean }) {
  const vars = spec.variables;
  const ids = vars.map((v) => v.id);
  const byId = useMemo(() => Object.fromEntries(vars.map((v) => [v.id, v])), [spec]);
  const eqs = useMemo(() => compileAll(spec.equations), [spec]);
  const bounds = useMemo(() => Object.fromEntries(vars.map((v) => [v.id, { min: v.min, max: v.max }])), [spec]);

  const selectIds = vars.filter((v) => v.options).map((v) => v.id);
  const freedom = (spec.freedom ?? vars.length - spec.equations.length) - selectIds.length;
  const keep = (arr: string[]) => (freedom > 0 ? arr.slice(-freedom) : []);
  const DATA = '__data';

  // Date fields hold days since 1970-01-01; clock fields hold hours after midnight
  const parseField = (v: VarSpec, text: string, unitId: string): number => {
    if (v.family === 'date') { const t = Date.parse(`${text}T00:00:00Z`); return Number.isFinite(t) ? t / DAY : NaN; }
    if (v.family === 'clock') { const m = /^(\d{1,2}):(\d{2})/.exec(text); return m ? +m[1] + +m[2] / 60 : NaN; }
    const n = parseNum(text);
    return Number.isFinite(n) ? toBase(n, findUnit(v.family, unitId)) : NaN;
  };
  // Default unit: imperial alternative for US-style regions, otherwise the file's unit
  const defaultUnit = (v: VarSpec, r: Region | null) =>
    findUnit(v.family, r?.imperial && v.imperialUnit ? v.imperialUnit : v.unit);

  const initial = (r: Region | null = null) => {
    const units: Record<string, string> = {};
    const raw: Record<string, string> = {};
    const order: string[] = [];
    for (const v of vars) {
      const u = defaultUnit(v, r);
      units[v.id] = u.id;
      if (v.default !== undefined && v.family === 'date') { raw[v.id] = isoDate(todayDays() + v.default); order.push(v.id); continue; }
      if (v.default !== undefined && v.family === 'clock') { raw[v.id] = hhmm(v.default); order.push(v.id); continue; }
      if (v.default !== undefined) {
        // defaults are written in the file's unit; convert if we switched unit
        const same = v.options || u.id === findUnit(v.family, v.unit).id;
        raw[v.id] = String(same ? v.default : Number(fromBase(toBase(v.default, findUnit(v.family, v.unit)), u).toPrecision(3)));
        if (!v.options) order.push(v.id);
      }
    }
    if (spec.dataset) raw[DATA] = spec.dataset.default ?? '';
    return { units, raw, order: keep(order) };
  };
  const [state, setState] = useState(() => initial());
  const [region, setRegion] = useState<Region | null>(null);
  const pre = (v: VarSpec) => v.prefix ?? (v.family === 'currency' ? region?.currency ?? '$' : '');
  const [showSteps, setShowSteps] = useState(false);
  const [toast, setToast] = useState('');
  const lastResult = useRef<SolveResult | null>(null);

  // After hydration: apply the visitor's region, then restore from URL (?V=12&V.u=kV)
  useEffect(() => {
    const r = detectRegion();
    setRegion(r);
    const q = new URLSearchParams(location.search);
    const s = initial(r);
    if (spec.dataset && q.has('data')) s.raw[DATA] = q.get('data')!;
    if (![...q.keys()].some((k) => ids.includes(k.split('.')[0]))) { setState(s); return; }
    const order: string[] = [];
    for (const v of vars) {
      if (q.has(`${v.id}.u`)) s.units[v.id] = findUnit(v.family, q.get(`${v.id}.u`)!).id;
      if (q.has(v.id)) { s.raw[v.id] = q.get(v.id)!; if (!v.options) order.push(v.id); }
    }
    if (order.length) s.order = keep(order);
    setState(s);
  }, []);

  // ---- compute ----
  const known: Record<string, number> = {};
  for (const id of [...state.order, ...selectIds]) {
    const n = parseField(byId[id], state.raw[id] ?? '', state.units[id]);
    if (Number.isFinite(n)) known[id] = n;
  }
  const dataList = spec.dataset ? parseList(state.raw[DATA] ?? '') : [];
  if (spec.dataset) Object.assign(known, listStats(dataList));
  const ready = (!spec.dataset || dataList.length > 0) && Object.keys(known).filter((k) => !k.startsWith('data_')).length - selectIds.filter((id) => id in known).length >= freedom;
  const hints = lastResult.current?.values ?? {};
  const result = useMemo(
    () => (ready ? solve(eqs, known, ids, bounds, hints) : null),
    [JSON.stringify(known), ready],
  );
  if (result) lastResult.current = result;

  const displayValue = (id: string): string => {
    if (state.order.includes(id) || byId[id].options) return state.raw[id] ?? '';
    const v = result?.values[id];
    if (v === undefined || !Number.isFinite(v)) return '';
    if (byId[id].family === 'date') return isoDate(v);
    if (byId[id].family === 'clock') return hhmm(v);
    const d = fromBase(v, findUnit(byId[id].family, state.units[id]));
    const dec = byId[id].decimals;
    return dec !== undefined ? String(Number(d.toFixed(dec))) : fmtNum(Number(d.toPrecision(Math.abs(d) >= 1e6 ? 12 : 7)));
  };
  // Human-friendly grouped value, e.g. 8,45,00,00,000 (uses the site locale)
  const pretty = (id: string, text: string): string => {
    const v = byId[id];
    if (v.family === 'date') {
      const t = Date.parse(`${text}T00:00:00Z`);
      return Number.isFinite(t) ? new Date(t).toLocaleDateString(region?.locale ?? SITE.locale, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' }) : '';
    }
    const n = parseNum(text);
    if (!Number.isFinite(n) || Math.abs(n) < 1000 || !['none', 'currency'].includes(v.family)) return '';
    return `${pre(v)}${n.toLocaleString(region?.locale ?? SITE.locale, { maximumFractionDigits: v.decimals ?? 2 })}${v.suffix ? ` ${v.suffix}` : ''}`;
  };

  // Shareable link with the current values (built only when the visitor clicks "Share link",
  // so the address bar stays clean for SEO and analytics)
  const shareUrl = (): string => {
    const q = new URLSearchParams();
    for (const id of [...state.order, ...selectIds]) {
      if (state.raw[id]) q.set(id, state.raw[id]);
    }
    if (spec.dataset && state.raw[DATA] && state.raw[DATA] !== (spec.dataset.default ?? '')) q.set('data', state.raw[DATA]);
    for (const v of vars) if (state.units[v.id] !== defaultUnit(v, region).id) q.set(`${v.id}.u`, state.units[v.id]);
    const qs = q.toString();
    return location.origin + location.pathname + (qs ? `?${qs}` : '');
  };

  // ---- handlers ----
  const onInput = (id: string, text: string) => {
    setState((s) => {
      const raw = { ...s.raw, [id]: text };
      if (byId[id].options) return { ...s, raw }; // dropdowns are always inputs
      let order = s.order.filter((x) => x !== id);
      if (text.trim() !== '') {
        order = keep([...order, id]);
      }
      return { ...s, raw, order };
    });
  };
  const onUnit = (id: string, unitId: string) => {
    setState((s) => {
      const v = byId[id];
      const raw = { ...s.raw };
      if (s.order.includes(id)) {
        const n = parseNum(raw[id] ?? '');
        if (Number.isFinite(n)) {
          const base = toBase(n, findUnit(v.family, s.units[id]));
          raw[id] = fmtNum(fromBase(base, findUnit(v.family, unitId)));
        }
      }
      return { ...s, raw, units: { ...s.units, [id]: unitId } };
    });
  };
  const flash = (m: string) => { setToast(m); setTimeout(() => setToast(''), 1800); };
  const copy = async (text: string, msg: string) => {
    try { await navigator.clipboard.writeText(text); flash(msg); } catch { flash('Copy failed'); }
  };
  const reset = () => setState(initial(region));
  const clearAll = () => setState((s) => ({ ...s, raw: { ...Object.fromEntries(selectIds.map((id) => [id, s.raw[id]])), [DATA]: '' }, order: [] }));
  const outputsOnly = freedom <= 0;

  const missing = Math.max(0, freedom - state.order.filter((id) => id in known).length);
  const resultText = vars.map((v) => {
    const u = findUnit(v.family, state.units[v.id]);
    const opt = v.options?.find((o) => String(o.value) === state.raw[v.id]);
    return `${v.label}: ${opt ? opt.label : `${pre(v)}${displayValue(v.id)} ${u.label || v.suffix || ''}`.trim()}`;
  }).join('\n');

  return (
    <div class={`calc ${embed ? 'calc--embed' : ''}`}>
      <div class="calc__fields">
        {spec.dataset && (
          <div class="field field--data">
            <label for="f-data" class="field__label">
              {spec.dataset.label}
              {spec.dataset.help && <span class="field__help" title={spec.dataset.help} aria-label={spec.dataset.help}>?</span>}
            </label>
            <textarea id="f-data" class="field__textarea" rows={3} value={state.raw[DATA] ?? ''}
              placeholder={spec.dataset.placeholder ?? 'e.g. 12, 15, 9, 21, 15'}
              onInput={(e) => { const t = (e.target as HTMLTextAreaElement).value; setState((s) => ({ ...s, raw: { ...s.raw, [DATA]: t } })); }} />
            <span class="field__pretty">{dataList.length} number{dataList.length === 1 ? '' : 's'} — separate with commas, spaces or new lines</span>
          </div>
        )}
        {vars.map((v) => {
          const units = getUnits(v.family);
          const isKnown = state.order.includes(v.id);
          const val = displayValue(v.id);
          const computed = !isKnown && !v.options && val !== '';
          const base = result?.values[v.id];
          const band = v.bands && base !== undefined ? v.bands.find((b) => base <= b.max) ?? v.bands[v.bands.length - 1] : undefined;
          return (
            <div class={`field ${computed ? 'field--computed' : ''} ${isKnown ? 'field--known' : ''}`} key={v.id}>
              <label for={`f-${v.id}`} class="field__label">
                {v.label}
                {v.help && <span class="field__help" title={v.help} aria-label={v.help}>?</span>}
              </label>
              <div class="field__row">
                {v.options ? (
                  <select id={`f-${v.id}`} class="field__select" value={state.raw[v.id]}
                    onChange={(e) => onInput(v.id, (e.target as HTMLSelectElement).value)}>
                    {v.options.map((o) => <option value={String(o.value)}>{o.label}</option>)}
                  </select>
                ) : (
                  <>
                    {pre(v) && <span class="field__affix">{pre(v).trim()}</span>}
                    <input id={`f-${v.id}`} class="field__input" type={v.family === 'date' ? 'date' : v.family === 'clock' ? 'time' : 'text'} inputMode={v.family === 'date' || v.family === 'clock' ? undefined : 'decimal'} autocomplete="off" readOnly={outputsOnly}
                      value={val} placeholder={computed ? '' : 'Enter value'}
                      onInput={(e) => onInput(v.id, (e.target as HTMLInputElement).value)} />
                    {isKnown && val !== '' && (
                      <button type="button" class="field__clear" aria-label={`Clear ${v.label} to calculate it`}
                        title="Clear to calculate this field" onClick={() => onInput(v.id, '')}>×</button>
                    )}
                    {units.length > 1 ? (
                      <select class="field__unit" aria-label={`${v.label} unit`} value={state.units[v.id]}
                        onChange={(e) => onUnit(v.id, (e.target as HTMLSelectElement).value)}>
                        {units.map((u) => <option value={u.id}>{u.label}</option>)}
                      </select>
                    ) : (units[0].label || v.suffix) ? <span class="field__affix">{units[0].label || v.suffix}</span> : null}
                  </>
                )}
              </div>
              {computed && <span class="field__badge">calculated</span>}
              {!v.options && pretty(v.id, val) && <span class="field__pretty">{pretty(v.id, val)}</span>}
              {band && (
                <div class="band">
                  <div class="band__bar">
                    {v.bands!.map((b) => <span style={{ background: b.color, opacity: b === band ? 1 : 0.28 }} />)}
                  </div>
                  <strong style={{ color: band.color }}>{band.label}</strong>
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div class="calc__status" aria-live="polite">
        {outputsOnly
          ? <span>Edit the numbers above — results update as you type.</span>
          : missing > 0
          ? <span>Enter {missing} more value{missing > 1 ? 's' : ''} — any field works, the rest is calculated.</span>
          : <span>Type in any field to change it. Press × on a value to calculate that field instead.</span>}
        {result && result.unsolved.length > 0 && <span class="warn">No valid solution for these inputs. Check the values.</span>}
        {result && result.inconsistent.length > 0 && <span class="warn">Inputs are inconsistent.</span>}
        {toast && <span class="toast">{toast}</span>}
      </div>

      <div class="calc__actions">
        <button type="button" class="btn btn--primary" onClick={() => copy(resultText, 'Result copied')}>Copy result</button>
        {!embed && <button type="button" class="btn" onClick={() => copy(shareUrl(), 'Link copied')}>Share link</button>}
        <button type="button" class="btn" onClick={() => setShowSteps((s) => !s)} aria-expanded={showSteps}>
          {showSteps ? 'Hide steps' : 'Show steps'}
        </button>
        <button type="button" class="btn btn--ghost" onClick={clearAll}>Clear</button>
        <button type="button" class="btn btn--ghost" onClick={reset}>Reset</button>
      </div>

      {showSteps && result && (
        <div class="steps">
          <p class="steps__note">Values below are in base units ({[...new Set(vars.map((v) => (getUnits(v.family).find((u) => u.factor === 1 && !u.offset) ?? getUnits(v.family)[0]).label).filter(Boolean))].join(', ') || 'plain numbers'}).</p>
          <ol>
          {result.steps.map((s) => (
            <li>
              <div class="steps__eq">{s.equation}</div>
              <div class="steps__sub">{s.substituted}</div>
              <div class="steps__res"><b>{byId[s.variable]?.label ?? s.variable}</b> = {fmtNum(s.value)}{s.method === 'numeric' && <em> (solved numerically)</em>}</div>
            </li>
          ))}
          </ol>
        </div>
      )}

      {spec.chart && result && result.unsolved.length === 0 && (
        <Chart spec={spec} eqs={eqs} values={result.values} known={known} order={state.order}
          selectIds={selectIds} units={state.units} bounds={bounds} />
      )}

      {embed && <a class="calc__credit" href={path} target="_blank" rel="noopener">Powered by {SITE.name}</a>}
    </div>
  );
}
