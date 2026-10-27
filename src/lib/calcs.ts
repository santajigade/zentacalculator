import { getCollection, type CollectionEntry } from 'astro:content';

export type Calc = CollectionEntry<'calculators'>;
export const slugOf = (c: Calc) => c.id.split('/').pop()!;
export const urlOf = (c: Calc) => `/${c.data.category}/${slugOf(c)}/`;

let cache: Calc[] | null = null;
export async function allCalcs(): Promise<Calc[]> {
  if (!cache) cache = (await getCollection('calculators')).sort((a, b) => a.data.title.localeCompare(b.data.title));
  return cache;
}
/** Find by "category/slug" or bare slug. */
export const findCalc = (all: Calc[], ref: string) =>
  all.find((c) => `${c.data.category}/${slugOf(c)}` === ref || slugOf(c) === ref);

export { embedSnippet } from './embed.ts';

// ---- Internal linking: similarity between calculators (build time only) ----
const STOP = new Set(['calculator', 'calculators', 'converter', 'the', 'and', 'for', 'of', 'to', 'a', 'in', 'on', 'with', 'how', 'per', 'vs', 'from', 'by', 'your', 'my', 'is', 'or', 'an', 'at', 'free', 'online']);
const tokCache = new Map<string, Set<string>>();
function tokens(c: Calc): Set<string> {
  let t = tokCache.get(c.id);
  if (!t) {
    const text = [c.data.title, c.data.title, ...c.data.keywords].join(' ').toLowerCase();
    t = new Set(text.split(/[^a-z0-9]+/).filter((w) => w.length > 1 && !STOP.has(w)).map((w) => w.replace(/s$/, '')));
    tokCache.set(c.id, t);
  }
  return t;
}
let idf: Map<string, number> | null = null;
function weights(all: Calc[]): Map<string, number> {
  if (!idf) {
    const df = new Map<string, number>();
    for (const c of all) for (const w of tokens(c)) df.set(w, (df.get(w) ?? 0) + 1);
    idf = new Map([...df].map(([w, n]) => [w, Math.log(all.length / n)]));
  }
  return idf;
}
function similarity(a: Calc, b: Calc, W: Map<string, number>): number {
  const A = tokens(a), B = tokens(b);
  let shared = 0, n = 0, wa = 0, wb = 0;
  for (const w of A) { wa += W.get(w) ?? 0; if (B.has(w)) { shared += W.get(w) ?? 0; n++; } }
  for (const w of B) wb += W.get(w) ?? 0;
  const same = a.data.category === b.data.category;
  if (!same && n < 2) return 0; // a single shared word across categories is usually a coincidence
  const score = shared / Math.sqrt(wa * wb || 1);
  if (!same && score < 0.25) return 0;
  return score + (same ? 0.1 : 0);
}
/** Most similar calculators, best first. */
export function similarTo(c: Calc, all: Calc[], n: number, filter: (x: Calc) => boolean = () => true): Calc[] {
  return all.filter((x) => x.id !== c.id && filter(x))
    .map((x) => [x, similarity(c, x, weights(all))] as const)
    .sort((p, q) => q[1] - p[1] || p[0].data.title.localeCompare(q[0].data.title))
    .slice(0, n).map((p) => p[0]);
}
