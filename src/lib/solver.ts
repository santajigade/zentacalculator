// Generic "solve for any field" engine.
// Given a set of equations and some known values, repeatedly finds an equation with
// exactly one unknown and solves it (directly when isolated, otherwise numerically).

import { compileEquation, type Equation, type Scope } from './expr.ts';

export interface VarBounds { min?: number; max?: number; }
export interface Step { variable: string; equation: string; substituted: string; value: number; method: 'direct' | 'numeric'; }
export interface SolveResult { values: Scope; steps: Step[]; unsolved: string[]; inconsistent: string[]; }

export function compileAll(srcs: string[]): Equation[] { return srcs.map(compileEquation); }

const residual = (eq: Equation, s: Scope) => eq.lhs.fn(s) - eq.rhs.fn(s);
const scale = (eq: Equation, s: Scope) => Math.abs(eq.lhs.fn(s)) + Math.abs(eq.rhs.fn(s));

/** Build a log-spaced grid of trial points over ±[1e-9, 1e13] plus 0. */
const GRID: number[] = (() => {
  const pos: number[] = [];
  for (let k = -9; k <= 13; k++) for (const m of [1, 2, 5]) pos.push(m * 10 ** k);
  return [...pos.map((x) => -x).reverse(), 0, ...pos];
})();

/** Find a root of a scalar function f via grid bracketing + bisection. */
function findRoot(f: (v: number) => number, verify: (v: number) => boolean, bounds: VarBounds, hint?: number): number | undefined {
  const ok = (v: number) => (bounds.min === undefined || v >= bounds.min - 1e-12) && (bounds.max === undefined || v <= bounds.max + 1e-12);
  const pts = [...GRID];
  if (hint !== undefined && Number.isFinite(hint)) pts.push(hint, hint * 0.999, hint * 1.001);
  if (bounds.min !== undefined) pts.push(bounds.min);
  if (bounds.max !== undefined) pts.push(bounds.max);
  const xs = [...new Set(pts)].filter(ok).sort((a, b) => a - b);

  const roots: number[] = [];
  let px = NaN, pf = NaN;
  for (const cx of xs) {
    const cf = f(cx);
    if (cf === 0) { if (verify(cx)) roots.push(cx); }
    else if (Number.isFinite(cf) && Number.isFinite(pf) && pf !== 0 && Math.sign(cf) !== Math.sign(pf)) {
      let a = px, b = cx, fa = pf;
      for (let i = 0; i < 200; i++) {
        const m = (a + b) / 2;
        if (m === a || m === b) break;
        const fm = f(m);
        if (fm === 0) { a = b = m; break; }
        if (Math.sign(fm) === Math.sign(fa)) { a = m; fa = fm; } else b = m;
      }
      const r = (a + b) / 2;
      if (verify(r)) roots.push(r); // rejects sign changes across poles
    }
    px = cx; pf = cf;
  }
  if (!roots.length) return undefined;
  if (hint !== undefined && Number.isFinite(hint)) {
    return roots.reduce((best, r) => (Math.abs(r - hint) < Math.abs(best - hint) ? r : best));
  }
  const nonNeg = roots.filter((r) => r >= 0);
  return nonNeg.length ? Math.min(...nonNeg) : roots.reduce((b, r) => (Math.abs(r) < Math.abs(b) ? r : b));
}

function solveOne(eq: Equation, x: string, known: Scope, bounds: VarBounds, hint?: number): number | undefined {
  const f = (v: number) => residual(eq, { ...known, [x]: v });
  const verify = (v: number) => {
    const s = { ...known, [x]: v };
    return Number.isFinite(v) && Math.abs(residual(eq, s)) <= 1e-7 * Math.max(scale(eq, s), 1e-300);
  };
  return findRoot(f, verify, bounds, hint);
}

export function fmtNum(v: number): string {
  if (!Number.isFinite(v)) return String(v);
  if (v === 0) return '0';
  const a = Math.abs(v);
  if (a >= 1e15 || a < 1e-6) return v.toExponential(6).replace(/\.?0+e/, 'e');
  return String(parseFloat(v.toPrecision(10)));
}

function substitute(src: string, s: Scope, target: string): string {
  return src.replace(/[A-Za-z_][A-Za-z0-9_]*/g, (name) => {
    if (name === target || !(name in s)) return name;
    const v = fmtNum(s[name]);
    return v.startsWith('-') ? `(${v})` : v;
  });
}

interface Prop { values: Scope; steps: Step[]; used: Set<number>; }

function propagate(equations: Equation[], start: Scope, bounds: Record<string, VarBounds>, hints: Scope): Prop {
  const values: Scope = { ...start };
  const steps: Step[] = [];
  const used = new Set<number>();
  let progress = true;
  while (progress) {
    progress = false;
    for (let i = 0; i < equations.length; i++) {
      if (used.has(i)) continue;
      const eq = equations[i];
      const missing = eq.vars.filter((v) => !(v in values));
      if (missing.length !== 1) continue;
      const x = missing[0];
      let val: number | undefined;
      let method: Step['method'] = 'numeric';
      for (const [iso, other] of [[eq.lhs, eq.rhs], [eq.rhs, eq.lhs]] as const) {
        if (iso.vars.length === 1 && iso.src.trim() === x) {
          const v = other.fn(values);
          if (Number.isFinite(v)) { val = v; method = 'direct'; }
        }
      }
      if (val === undefined) val = solveOne(eq, x, values, bounds[x] ?? {}, hints[x]);
      used.add(i);
      if (val === undefined) continue;
      values[x] = val;
      steps.push({ variable: x, equation: eq.src, substituted: substitute(eq.src, values, x), value: val, method });
      progress = true;
    }
  }
  return { values, steps, used };
}

const isConsistent = (eq: Equation, s: Scope) => Math.abs(residual(eq, s)) <= 1e-6 * Math.max(scale(eq, s), 1e-300);

export function solve(
  equations: Equation[], known: Scope, allVars: string[],
  bounds: Record<string, VarBounds> = {}, hints: Scope = {},
): SolveResult {
  let { values, steps } = propagate(equations, known, bounds, hints);

  // Coupled system: guess one unknown ("shooting"), propagate, and root-find on
  // the residual of an equation that ends up over-determined.
  let unsolved = allVars.filter((v) => !(v in values));
  if (unsolved.length) {
    for (const u of unsolved) {
      const run = (g: number) => propagate(equations, { ...values, [u]: g }, bounds, hints);
      const extraRes = (p: Prop) => {
        const eq = equations.find((e, i) => !p.used.has(i) && e.vars.every((v) => v in p.values))
          ?? equations.find((e) => e.vars.every((v) => v in p.values) && !isConsistent(e, p.values));
        return eq ? residual(eq, p.values) : NaN;
      };
      const f = (g: number) => extraRes(run(g));
      const verify = (g: number) => {
        const p = run(g);
        return allVars.every((v) => v in p.values) && equations.every((e) => isConsistent(e, p.values));
      };
      const root = findRoot(f, verify, bounds[u] ?? {}, hints[u]);
      if (root !== undefined) {
        const p = run(root);
        values = p.values;
        const system = equations.map((e) => e.src).join('  and  ');
        steps = [...steps, { variable: u, equation: system, substituted: `solved simultaneously for ${u}`, value: root, method: 'numeric' }, ...p.steps];
        break;
      }
    }
    unsolved = allVars.filter((v) => !(v in values));
  }

  const inconsistent = equations
    .filter((eq) => eq.vars.every((v) => v in values))
    .filter((eq) => !isConsistent(eq, values))
    .map((eq) => eq.src);
  return { values, steps, unsolved, inconsistent };
}
