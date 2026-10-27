// Tiny, safe math-expression parser (no eval). Compiles a string like
// "P * (1 + r/n)^(n*t)" into a function of a variable map.

export type Scope = Record<string, number>;
type Node =
  | { t: 'num'; v: number }
  | { t: 'var'; name: string }
  | { t: 'neg'; a: Node }
  | { t: 'bin'; op: string; a: Node; b: Node }
  | { t: 'call'; fn: string; args: Node[] };


// Lanczos approximation for Γ(x); exact-ish for integers (factorials)
const LG = [676.5203681218851, -1259.1392167224028, 771.32342877765313, -176.61502916214059,
  12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
function gamma(x: number): number {
  if (x < 0.5) return Math.PI / (Math.sin(Math.PI * x) * gamma(1 - x));
  if (Number.isInteger(x) && x <= 171) { let f = 1; for (let i = 2; i < x; i++) f *= i; return f; }
  x -= 1; let a = 0.99999999999980993; const t = x + 7.5;
  for (let i = 0; i < 8; i++) a += LG[i] / (x + i + 1);
  return Math.sqrt(2 * Math.PI) * t ** (x + 0.5) * Math.exp(-t) * a;
}
function lnGamma(x: number): number {
  if (Number.isInteger(x) && x <= 171) return Math.log(gamma(x));
  x -= 1; let a = 0.99999999999980993; const t = x + 7.5;
  for (let i = 0; i < 8; i++) a += LG[i] / (x + i + 1);
  return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
}
// Abramowitz–Stegun 7.1.26 refined (max error ~1.2e-7)
function erf(x: number): number {
  const z = Math.abs(x), t = 1 / (1 + 0.5 * z);
  const r = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 +
    t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
  return x >= 0 ? 1 - r : r - 1;
}


// Calendar helpers on day numbers (days since 1970-01-01, UTC)
const ymd = (d: number) => { const t = new Date(Math.round(d) * 86400000); return [t.getUTCFullYear(), t.getUTCMonth(), t.getUTCDate()]; };
function monthsBetween(a: number, b: number): number {
  const sgn = b < a ? -1 : 1; if (sgn < 0) [a, b] = [b, a];
  const [y1, m1, d1] = ymd(a), [y2, m2, d2] = ymd(b);
  let m = (y2 - y1) * 12 + (m2 - m1); if (d2 < d1) m -= 1;
  return sgn * m;
}
function yearsBetween(a: number, b: number): number { const m = monthsBetween(a, b); return m < 0 ? -Math.floor(-m / 12) : Math.floor(m / 12); }
function workdays(a: number, b: number): number { // Mon–Fri from a (inclusive) to b (exclusive)
  const sgn = b < a ? -1 : 1; if (sgn < 0) [a, b] = [b, a];
  a = Math.round(a); b = Math.round(b);
  const full = Math.floor((b - a) / 7); let n = full * 5;
  for (let d = a + full * 7; d < b; d++) { const w = (((d + 4) % 7) + 7) % 7; if (w !== 0 && w !== 6) n++; }
  return sgn * n;
}

function exactComb(n: number, k: number): number { k = Math.min(k, n - k); let r = 1; for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i; return Math.round(r); }
function exactPerm(n: number, k: number): number { let r = 1; for (let i = 0; i < k; i++) r *= n - i; return r; }

const FUNCS: Record<string, (...a: number[]) => number> = {
  sqrt: Math.sqrt, cbrt: Math.cbrt, abs: Math.abs, exp: Math.exp,
  ln: Math.log, log: Math.log10, log10: Math.log10, log2: Math.log2,
  sin: Math.sin, cos: Math.cos, tan: Math.tan,
  asin: Math.asin, acos: Math.acos, atan: Math.atan, atan2: Math.atan2,
  sinh: Math.sinh, cosh: Math.cosh, tanh: Math.tanh,
  // small tolerance so 2.7/0.18 (=15.000000000000002) rounds to 15, as a person would expect
  floor: (x) => Math.floor(x + 1e-9), ceil: (x) => Math.ceil(x - 1e-9), round: Math.round,
  min: Math.min, max: Math.max, pow: Math.pow,
  mod: (a, b) => ((a % b) + b) % b,
  gamma, fact: (n) => gamma(n + 1),
  nCr: (n, k) => (k < 0 || k > n ? 0 : Number.isInteger(n) && Number.isInteger(k) ? exactComb(n, k) : Math.exp(lnGamma(n + 1) - lnGamma(k + 1) - lnGamma(n - k + 1))),
  nPr: (n, k) => (k < 0 || k > n ? 0 : Number.isInteger(n) && Number.isInteger(k) ? exactPerm(n, k) : Math.exp(lnGamma(n + 1) - lnGamma(n - k + 1))),
  erf, normcdf: (z) => 0.5 * (1 + erf(z / Math.SQRT2)),
  yearsBetween, monthsBetween, workdays,
  weekday: (d) => (((Math.floor(d) + 4) % 7) + 7) % 7, // 0 = Sunday (days since 1970-01-01)
  gcd: (a, b) => { a = Math.abs(Math.round(a)); b = Math.abs(Math.round(b)); while (b) [a, b] = [b, a % b]; return a; },
  lcm: (a, b) => { a = Math.abs(Math.round(a)); b = Math.abs(Math.round(b)); if (!a || !b) return 0; let x = a, y = b; while (y) [x, y] = [y, x % y]; return a / x * b; },
  step: (x) => (x > 1e-9 ? 1 : 0), // 1 when x > 0, else 0 (for thresholds such as tax rebates)
  sign: Math.sign, hypot: Math.hypot, deg: (r) => (r * 180) / Math.PI, rad: (d) => (d * Math.PI) / 180,
};
const CONSTS: Record<string, number> = { pi: Math.PI, e: Math.E, g0: 9.80665 };

function tokenize(src: string): string[] {
  const re = /\s*(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?|[A-Za-z_][A-Za-z0-9_]*|\*\*|[-+*/^(),])/y;
  const out: string[] = [];
  let i = 0;
  while (i < src.length) {
    if (/\s/.test(src[i])) { i++; continue; }
    re.lastIndex = i;
    const m = re.exec(src);
    if (!m) throw new Error(`Unexpected character "${src[i]}" in "${src}"`);
    out.push(m[1] === '**' ? '^' : m[1]);
    i = re.lastIndex;
  }
  return out;
}

function parse(src: string): Node {
  const tk = tokenize(src);
  let p = 0;
  const peek = () => tk[p];
  const eat = (s?: string) => {
    const t = tk[p++];
    if (s && t !== s) throw new Error(`Expected "${s}" but got "${t}" in "${src}"`);
    return t;
  };
  // precedence: + -  <  * /  <  unary -  <  ^ (right assoc)
  function sum(): Node {
    let a = prod();
    while (peek() === '+' || peek() === '-') { const op = eat(); a = { t: 'bin', op, a, b: prod() }; }
    return a;
  }
  function prod(): Node {
    let a = unary();
    while (peek() === '*' || peek() === '/') { const op = eat(); a = { t: 'bin', op, a, b: unary() }; }
    return a;
  }
  function unary(): Node {
    if (peek() === '-') { eat(); return { t: 'neg', a: unary() }; }
    if (peek() === '+') { eat(); return unary(); }
    return power();
  }
  function power(): Node {
    const a = atom();
    if (peek() === '^') { eat(); return { t: 'bin', op: '^', a, b: unary() }; }
    return a;
  }
  function atom(): Node {
    const t = eat();
    if (t === undefined) throw new Error(`Unexpected end of "${src}"`);
    if (t === '(') { const n = sum(); eat(')'); return n; }
    if (/^[\d.]/.test(t)) return { t: 'num', v: parseFloat(t) };
    if (/^[A-Za-z_]/.test(t)) {
      if (peek() === '(') {
        if (!FUNCS[t]) throw new Error(`Unknown function "${t}"`);
        eat('(');
        const args: Node[] = [];
        if (peek() !== ')') { args.push(sum()); while (peek() === ',') { eat(); args.push(sum()); } }
        eat(')');
        return { t: 'call', fn: t, args };
      }
      return { t: 'var', name: t };
    }
    throw new Error(`Unexpected "${t}" in "${src}"`);
  }
  const n = sum();
  if (p < tk.length) throw new Error(`Unexpected "${tk[p]}" in "${src}"`);
  return n;
}

function evalNode(n: Node, s: Scope): number {
  switch (n.t) {
    case 'num': return n.v;
    case 'var': {
      if (n.name in s) return s[n.name];
      if (n.name in CONSTS) return CONSTS[n.name];
      return NaN;
    }
    case 'neg': return -evalNode(n.a, s);
    case 'call': return FUNCS[n.fn](...n.args.map((a) => evalNode(a, s)));
    case 'bin': {
      const a = evalNode(n.a, s), b = evalNode(n.b, s);
      switch (n.op) {
        case '+': return a + b; case '-': return a - b;
        case '*': return a * b; case '/': return a / b;
        default: return Math.pow(a, b);
      }
    }
  }
}

function collectVars(n: Node, out: Set<string>) {
  if (n.t === 'var') { if (!(n.name in CONSTS)) out.add(n.name); }
  else if (n.t === 'neg') collectVars(n.a, out);
  else if (n.t === 'bin') { collectVars(n.a, out); collectVars(n.b, out); }
  else if (n.t === 'call') n.args.forEach((a) => collectVars(a, out));
}

export interface Compiled { src: string; vars: string[]; fn: (s: Scope) => number; }

export function compile(src: string): Compiled {
  const node = parse(src);
  const set = new Set<string>();
  collectVars(node, set);
  return { src, vars: [...set], fn: (s) => evalNode(node, s) };
}

/** "lhs = rhs" → residual lhs - rhs */
export interface Equation { src: string; lhs: Compiled; rhs: Compiled; vars: string[]; }

export function compileEquation(src: string): Equation {
  const parts = src.split('=');
  if (parts.length !== 2) throw new Error(`Equation must contain exactly one "=": "${src}"`);
  const lhs = compile(parts[0]), rhs = compile(parts[1]);
  return { src, lhs, rhs, vars: [...new Set([...lhs.vars, ...rhs.vars])] };
}
