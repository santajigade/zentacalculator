import type { APIRoute } from 'astro';
import { SITE } from '../../site.config.ts';
import { slugOf, urlOf } from '../../lib/calcs.ts';
import { catBySlug } from '../../data/categories.ts';
import { pinQueue } from '../../lib/pins.ts';

// RSS feed for Pinterest "Auto-publish from RSS": a few new calculator pins every day.
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const clean = (s: string) => s.replace(/\s*[–—]\s*/g, ', ');
export const GET: APIRoute = async () => {
  const items = (await pinQueue()).slice(0, 60).map(({ calc: c, date }) => {
    const cat = catBySlug(c.data.category)!;
    const link = `${SITE.url}${urlOf(c)}?utm_source=pinterest&utm_medium=social&utm_campaign=pins`;
    const img = `${SITE.url}/pins/${c.data.category}/${slugOf(c)}.jpg`;
    const tags = ['#' + cat.name.replace(/\W/g, ''), '#calculator', '#freetools', '#formula'].join(' ');
    return `<item><title>${esc(clean(c.data.title))}</title><link>${esc(link)}</link><guid isPermaLink="false">zc-pin-${c.id}</guid>
<pubDate>${new Date(date + 'T06:00:00+05:30').toUTCString()}</pubDate><category>${esc(cat.name)}</category>
<description>${esc(`${clean(c.data.description)} Free online ${cat.name.toLowerCase()} calculator with formula and steps. ${tags}`)}</description>
<enclosure url="${img}" type="image/jpeg" length="0"/><media:content url="${img}" medium="image" type="image/jpeg" width="1000" height="1500"/></item>`;
  });
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>
<title>${esc(SITE.name)}: free calculators</title><link>${SITE.url}/</link><description>Free online calculators for engineering, science, math and finance.</description><language>en</language>
${items.join('\n')}
</channel></rss>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
};
