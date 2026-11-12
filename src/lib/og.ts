// Social share images (Open Graph, 1200x630) rendered at build time with satori + resvg.
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import sharp from 'sharp';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { mkdirSync, existsSync, writeFileSync } from 'node:fs';

import { join } from 'node:path';
const NM = join(process.cwd(), 'node_modules');
const font = (p: string) => readFileSync(join(NM, p));
let FONTS: any[] | null = null;
const fonts = () => FONTS ??= [
  { name: 'Jakarta', data: font('@fontsource/plus-jakarta-sans/files/plus-jakarta-sans-latin-500-normal.woff'), weight: 500, style: 'normal' },
  { name: 'Jakarta', data: font('@fontsource/plus-jakarta-sans/files/plus-jakarta-sans-latin-800-normal.woff'), weight: 800, style: 'normal' },
  { name: 'Mono', data: font('@fontsource/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff'), weight: 500, style: 'normal' },
  { name: 'Mono', data: font('@fontsource/jetbrains-mono/files/jetbrains-mono-greek-500-normal.woff'), weight: 500, style: 'normal' },
  { name: 'Mono', data: font('@fontsource/jetbrains-mono/files/jetbrains-mono-latin-ext-500-normal.woff'), weight: 500, style: 'normal' },
];

const SUP: Record<string, string> = { '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹' };
export function prettyEq(e?: string): string | undefined {
  if (!e) return;
  let s = e.replace(/\bsqrt\(/g, '√(').replace(/\bpi\b/g, 'π').replace(/\s*\*\s*/g, ' × ').replace(/\s*\/\s*/g, ' ÷ ')
    .replace(/\^(\d)\b/g, (_, d) => SUP[d]).replace(/\^\((\d)\)/g, (_, d) => SUP[d]);
  if (/[a-z_]{4,}\(|\^|\?|<|>|==|\d\.\d/.test(s) || s.length > 46) return;
  return s;
}

const h = (type: string, style: any, children?: any) => ({ type, props: { style, children } });

export interface OgInput { title: string; kicker: string; color: string; formula?: string; sub?: string; }

function card(o: OgInput) {
  const t = o.title.replace(/\s*\(.*\)\s*$/, '').replace(/\s+[–—-]\s+.*$/, '');
  const size = t.length > 38 ? 60 : t.length > 24 ? 70 : 82;
  return h('div', { width: '100%', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '64px 72px', fontFamily: 'Jakarta', color: '#fff',
    backgroundColor: '#0b1022', backgroundImage: `radial-gradient(circle at 92% 8%, ${o.color}cc 0%, ${o.color}33 34%, transparent 62%), radial-gradient(circle at 0% 100%, #4f5bff55 0%, transparent 50%)` }, [
    h('div', { display: 'flex', alignItems: 'center', gap: 18 }, [
      h('div', { width: 64, height: 64, borderRadius: 16, background: 'linear-gradient(135deg,#6d5bff,#4f5bff)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 42, fontWeight: 800 }, 'Z'),
      h('div', { fontSize: 34, fontWeight: 800, letterSpacing: -0.5, display: 'flex' }, ['Zenta', h('span', { fontWeight: 500, marginLeft: 8, opacity: 0.85 }, 'Calculator')]),
      h('div', { marginLeft: 'auto', fontSize: 22, fontWeight: 800, letterSpacing: 3, padding: '10px 20px', borderRadius: 999, background: o.color, color: '#fff', textTransform: 'uppercase' }, o.kicker),
    ]),
    h('div', { display: 'flex', flexDirection: 'column', gap: 26 }, [
      h('div', { fontSize: size, fontWeight: 800, lineHeight: 1.05, letterSpacing: -2, maxWidth: 1040 }, t),
      o.formula
        ? h('div', { display: 'flex', alignSelf: 'flex-start', fontFamily: 'Mono', fontSize: 34, padding: '14px 26px', borderRadius: 14, background: 'rgba(255,255,255,0.08)', border: '1px solid rgba(255,255,255,0.18)', color: '#fde68a' }, o.formula)
        : h('div', { fontSize: 30, fontWeight: 500, opacity: 0.85, maxWidth: 1000, lineHeight: 1.35 }, (o.sub ?? '').replace(/\s*[–—]\s*/g, ', ')),
    ]),
    h('div', { display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: 26, fontWeight: 500 }, [
      h('div', { display: 'flex', opacity: 0.85 }, 'Free online calculator · Formula, steps & examples'),
      h('div', { display: 'flex', fontWeight: 800, padding: '12px 24px', borderRadius: 999, background: '#fff', color: '#0b1022' }, 'zentacalculator.com'),
    ]),
  ]);
}

const CACHE = join(process.cwd(), '.og-cache');
export async function ogPng(o: OgInput): Promise<Buffer> {
  const key = createHash('sha1').update(JSON.stringify(o) + 'v2').digest('hex');
  const f = join(CACHE, key + '.jpg');
  if (existsSync(f)) return readFileSync(f);
  const svg = await satori(card(o) as any, { width: 1200, height: 630, fonts: fonts() });
  const png = await sharp(new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } }).render().asPng()).jpeg({ quality: 84, mozjpeg: true }).toBuffer();
  mkdirSync(CACHE, { recursive: true }); writeFileSync(f, png);
  return png;
}
