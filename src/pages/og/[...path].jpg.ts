import type { APIRoute } from 'astro';
import { allCalcs, slugOf } from '../../lib/calcs.ts';
import { CATEGORIES, catBySlug } from '../../data/categories.ts';
import { ogPng, prettyEq } from '../../lib/og.ts';

export async function getStaticPaths() {
  const calcs = await allCalcs();
  return [
    ...calcs.map((c) => {
      const cat = catBySlug(c.data.category)!;
      return { params: { path: `${c.data.category}/${slugOf(c)}` }, props: { o: { title: c.data.title, kicker: cat.name, color: cat.color, formula: prettyEq(c.data.equations?.[0]), sub: c.data.description } } };
    }),
    ...CATEGORIES.map((cat) => ({ params: { path: cat.slug }, props: { o: { title: `${cat.name} Calculators`, kicker: `${calcs.filter((c) => c.data.category === cat.slug).length} free tools`, color: cat.color, sub: cat.blurb } } })),
  ];
}
export const GET: APIRoute = async ({ props }) =>
  new Response(new Uint8Array(await ogPng((props as any).o)), { headers: { 'Content-Type': 'image/jpeg' } });
