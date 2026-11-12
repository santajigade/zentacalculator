import type { APIRoute } from 'astro';
import { allCalcs, slugOf } from '../../lib/calcs.ts';
import { catBySlug } from '../../data/categories.ts';
import { ogPng, prettyEq } from '../../lib/og.ts';
import { pinQueue } from '../../lib/pins.ts';

// Tall Pinterest images, only for calculators already released to the pin feed (keeps builds fast).
export async function getStaticPaths() {
  const calcs = await allCalcs();
  const released = new Set((await pinQueue()).map((p) => p.calc.id));
  return calcs.filter((c) => released.has(c.id)).map((c) => ({
    params: { path: `${c.data.category}/${slugOf(c)}` },
    props: { o: { title: c.data.title, kicker: catBySlug(c.data.category)!.name, color: catBySlug(c.data.category)!.color, formula: prettyEq(c.data.equations?.[0]), sub: c.data.description } },
  }));
}
export const GET: APIRoute = async ({ props }) =>
  new Response(new Uint8Array(await ogPng((props as any).o, true)), { headers: { 'Content-Type': 'image/jpeg' } });
