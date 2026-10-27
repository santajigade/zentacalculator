import { allCalcs, urlOf } from '../lib/calcs.ts';
import { catBySlug } from '../data/categories.ts';

export async function GET() {
  const items = (await allCalcs()).map((c) => ({
    t: c.data.title, u: urlOf(c), c: catBySlug(c.data.category)?.name ?? '', k: c.data.keywords.join(' ').toLowerCase(),
  }));
  return new Response(JSON.stringify(items), { headers: { 'Content-Type': 'application/json' } });
}
