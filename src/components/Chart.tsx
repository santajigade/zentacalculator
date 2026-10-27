/** @jsxImportSource preact */
import { useMemo, useState } from 'preact/hooks';
import { solve, fmtNum } from '../lib/solver.ts';
import type { Equation } from '../lib/expr.ts';
import { findUnit, fromBase, toBase } from '../lib/units.ts';
import type { CalcSpec } from './Calculator.tsx';

interface Props {
  spec: CalcSpec; eqs: Equation[]; values: Record<string, number>; known: Record<string, number>;
  order: string[]; selectIds: string[]; units: Record<string, string>;
  bounds: Record<string, { min?: number; max?: number }>;
}

const W = 640, H = 300, PAD = { l: 64, r: 18, t: 16, b: 42 };

function niceTicks(lo: number, hi: number, n = 5): number[] {
  if (!(hi > lo)) return [lo];
  const step0 = (hi - lo) / n;
  const mag = 10 ** Math.floor(Math.log10(step0));
  const step = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => s >= step0)!;
  const out: number[] = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + step * 1e-9; v += step) out.push(+v.toPrecision(12));
  return out;
}
const short = (v: number) => {
  const a = Math.abs(v);
  if (a >= 1e9) return `${+(v / 1e9).toPrecision(3)}B`;
  if (a >= 1e6) return `${+(v / 1e6).toPrecision(3)}M`;
  if (a >= 1e4) return `${+(v / 1e3).toPrecision(3)}k`;
  return fmtNum(+v.toPrecision(4));
};

export default function Chart({ spec, eqs, values, known, order, selectIds, units, bounds }: Props) {
  const plotVars = spec.variables.filter((v) => !v.options);
  const byId = Object.fromEntries(spec.variables.map((v) => [v.id, v]));
  const [x, setX] = useState(spec.chart!.x);
  const [y, setY] = useState(spec.chart!.y);
  const xu = findUnit(byId[x].family, units[x]);
  const yu = findUnit(byId[y].family, units[y]);
  const curX = values[x] !== undefined ? fromBase(values[x], xu) : 1;

  const defRange = (): [number, number] => {
    if (x === spec.chart!.x && spec.chart!.from !== undefined && spec.chart!.to !== undefined) return [spec.chart!.from, spec.chart!.to];
    const lo = byId[x].min !== undefined && fromBase(byId[x].min!, xu) >= 0 ? 0 : -Math.abs(curX) * 2;
    return [lo, curX === 0 ? 10 : Math.abs(curX) * 2];
  };
  const [range, setRange] = useState<{ x: string; r: [number, number] } | null>(null);
  const [from, to] = range && range.x === x ? range.r : defRange();
  const [hover, setHover] = useState<number | null>(null);

  const pts = useMemo(() => {
    if (x === y || !(to > from)) return [];
    // inputs held fixed: the user's knowns, with x forced in and y removed
    const freedom = order.length;
    let keep = order.filter((id) => id !== y && id !== x);
    keep = keep.slice(Math.max(0, keep.length - (freedom - 1)));
    // if x and y were both user inputs, hold one more (computed) variable fixed
    for (const v of plotVars) {
      if (keep.length >= freedom - 1) break;
      if (v.id !== x && v.id !== y && !keep.includes(v.id)) keep.push(v.id);
    }
    const fixed: Record<string, number> = {};
    for (const id of [...keep, ...selectIds]) if (id in known) fixed[id] = known[id];
    for (const id of keep) if (!(id in fixed) && id in values) fixed[id] = values[id];
    const out: { x: number; y: number }[] = [];
    const N = 80;
    let hints = values;
    for (let i = 0; i <= N; i++) {
      const xv = from + ((to - from) * i) / N;
      const r = solve(eqs, { ...fixed, [x]: toBase(xv, xu) }, spec.variables.map((v) => v.id), bounds, hints);
      const yv = r.values[y];
      if (yv !== undefined && Number.isFinite(yv) && r.inconsistent.length === 0) {
        out.push({ x: xv, y: fromBase(yv, yu) });
        hints = r.values;
      }
    }
    return out;
  }, [x, y, from, to, JSON.stringify(known), units[x], units[y]]);

  const ys = pts.map((p) => p.y);
  let yMin = Math.min(...ys, 0), yMax = Math.max(...ys);
  if (!(yMax > yMin)) yMax = yMin + 1;
  const sx = (v: number) => PAD.l + ((v - from) / (to - from)) * (W - PAD.l - PAD.r);
  const sy = (v: number) => H - PAD.b - ((v - yMin) / (yMax - yMin)) * (H - PAD.t - PAD.b);
  const d = pts.map((p, i) => `${i ? 'L' : 'M'}${sx(p.x).toFixed(1)},${sy(p.y).toFixed(1)}`).join('');
  const area = pts.length ? `${d}L${sx(pts[pts.length - 1].x)},${sy(Math.max(yMin, 0))}L${sx(pts[0].x)},${sy(Math.max(yMin, 0))}Z` : '';
  const cur = values[x] !== undefined && values[y] !== undefined ? { x: fromBase(values[x], xu), y: fromBase(values[y], yu) } : null;
  const hp = hover !== null ? pts[hover] : null;

  const onMove = (e: MouseEvent | TouchEvent) => {
    const svg = e.currentTarget as SVGSVGElement;
    const rect = svg.getBoundingClientRect();
    const cx = ('touches' in e ? e.touches[0].clientX : e.clientX) - rect.left;
    const vx = from + ((cx / rect.width) * W - PAD.l) / (W - PAD.l - PAD.r) * (to - from);
    let best = 0;
    pts.forEach((p, i) => { if (Math.abs(p.x - vx) < Math.abs(pts[best].x - vx)) best = i; });
    setHover(pts.length ? best : null);
  };

  const label = (id: string, u: { label: string }) => `${byId[id].label}${u.label ? ` (${u.label})` : ''}`;

  return (
    <div class="chart">
      <div class="chart__controls">
        <label>Plot <select value={y} onChange={(e) => setY((e.target as HTMLSelectElement).value)}>
          {plotVars.map((v) => <option value={v.id}>{v.label}</option>)}</select></label>
        <label>against <select value={x} onChange={(e) => { setX((e.target as HTMLSelectElement).value); setRange(null); }}>
          {plotVars.filter((v) => v.id !== y).map((v) => <option value={v.id}>{v.label}</option>)}</select></label>
        <label>from <input type="number" value={from} onChange={(e) => setRange({ x, r: [+(e.target as HTMLInputElement).value, to] })} /></label>
        <label>to <input type="number" value={to} onChange={(e) => setRange({ x, r: [from, +(e.target as HTMLInputElement).value] })} /></label>
      </div>
      {x === y ? <p class="chart__empty">Pick two different variables.</p> : pts.length < 2 ? <p class="chart__empty">No plottable values in this range.</p> : (
        <svg viewBox={`0 0 ${W} ${H}`} class="chart__svg" role="img" aria-label={`${label(y, yu)} versus ${label(x, xu)}`}
          onMouseMove={onMove} onTouchMove={onMove} onMouseLeave={() => setHover(null)}>
          {niceTicks(yMin, yMax).map((t) => (
            <g><line x1={PAD.l} x2={W - PAD.r} y1={sy(t)} y2={sy(t)} class="chart__grid" />
              <text x={PAD.l - 8} y={sy(t) + 4} text-anchor="end" class="chart__tick">{short(t)}</text></g>
          ))}
          {niceTicks(from, to, 6).map((t) => (
            <text x={sx(t)} y={H - PAD.b + 18} text-anchor="middle" class="chart__tick">{short(t)}</text>
          ))}
          <text x={(W + PAD.l) / 2} y={H - 4} text-anchor="middle" class="chart__axis">{label(x, xu)}</text>
          <path d={area} class="chart__area" />
          <path d={d} class="chart__line" />
          {cur && cur.x >= from && cur.x <= to && cur.y >= yMin && cur.y <= yMax && (
            <circle cx={sx(cur.x)} cy={sy(cur.y)} r="6" class="chart__cur"><title>Your value</title></circle>
          )}
          {hp && (
            <g>
              <line x1={sx(hp.x)} x2={sx(hp.x)} y1={PAD.t} y2={H - PAD.b} class="chart__hover" />
              <circle cx={sx(hp.x)} cy={sy(hp.y)} r="4.5" class="chart__dot" />
              <g transform={`translate(${Math.min(sx(hp.x) + 10, W - 190)},${PAD.t + 4})`}>
                <rect width="180" height="44" rx="8" class="chart__tip" />
                <text x="10" y="18" class="chart__tiptext">{byId[x].label}: {fmtNum(+hp.x.toPrecision(6))} {xu.label}</text>
                <text x="10" y="35" class="chart__tiptext chart__tiptext--b">{byId[y].label}: {fmtNum(+hp.y.toPrecision(6))} {yu.label}</text>
              </g>
            </g>
          )}
        </svg>
      )}
      <p class="chart__caption">{label(y, yu)} vs {label(x, xu)} — other inputs held at your current values.</p>
    </div>
  );
}
