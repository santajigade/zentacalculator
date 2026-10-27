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
