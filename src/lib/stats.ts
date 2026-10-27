// Statistics of a list of numbers, exposed to equations as data_* variables.
export function parseList(text: string): number[] {
  return (text.match(/-?\d*\.?\d+(?:[eE][-+]?\d+)?/g) ?? []).map(Number).filter(Number.isFinite);
}

export function listStats(xs: number[]): Record<string, number> {
  const n = xs.length;
  if (!n) return {};
  const s = [...xs].sort((a, b) => a - b);
  const sum = xs.reduce((a, b) => a + b, 0);
  const mean = sum / n;
  const ss = xs.reduce((a, x) => a + (x - mean) ** 2, 0);
  const q = (p: number) => { // linear interpolation (same as Excel QUARTILE.INC)
    const i = (n - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
    return s[lo] + (s[hi] - s[lo]) * (i - lo);
  };
  const counts = new Map<number, number>();
  for (const x of xs) counts.set(x, (counts.get(x) ?? 0) + 1);
  const top = Math.max(...counts.values());
  const mode = [...counts].filter(([, c]) => c === top).map(([v]) => v).sort((a, b) => a - b)[0];
  const out: Record<string, number> = {
    data_n: n, data_sum: sum, data_mean: mean, data_median: q(0.5),
    data_min: s[0], data_max: s[n - 1], data_range: s[n - 1] - s[0],
    data_q1: q(0.25), data_q3: q(0.75),
    data_varp: ss / n, data_sdp: Math.sqrt(ss / n),
    data_sumsq: xs.reduce((a, x) => a + x * x, 0),
  };
  if (n > 1) { out.data_var = ss / (n - 1); out.data_sd = Math.sqrt(ss / (n - 1)); }
  out.data_mode = mode; out.data_modecount = top;
  if (xs.every((x) => x > 0)) out.data_gmean = Math.exp(xs.reduce((a, x) => a + Math.log(x), 0) / n);
  return out;
}
