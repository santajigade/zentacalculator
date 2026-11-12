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
  const ids = s.match(/[A-Za-z]+\w*/g) ?? [];
  if (ids.some((w) => /^[a-z]{2,}$/.test(w)) || ids.every((w) => /^[a-z]/.test(w))) return; // internal names like ph, pf, bmi, y = p × x
  return s;
}

const rs = (t: string) => t.replace(/₹\s?/g, 'Rs ').replace(/\s+[–—]\s+/g, ', ');
const h = (type: string, style: any, children?: any) => ({ type, props: { style, children } });

export interface OgInput { title: string; kicker: string; color: string; formula?: string; sub?: string; }

function card(o: OgInput) {
  const t = o.title.replace(/\s*\([^)]*\)/g, '').replace(/\s+[–—-]\s+.*$/, '');
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
        : h('div', { fontSize: 30, fontWeight: 500, opacity: 0.85, maxWidth: 1000, lineHeight: 1.35 }, rs(o.sub ?? '')),
    ]),
    h('div', { display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: 26, fontWeight: 500 }, [
      h('div', { display: 'flex', opacity: 0.85 }, 'Free online calculator · Formula, steps & examples'),
      h('div', { display: 'flex', fontWeight: 800, padding: '12px 24px', borderRadius: 999, background: '#fff', color: '#0b1022' }, 'zentacalculator.com'),
    ]),
  ]);
}

// Tall Pinterest pin (1000x1500), coloured by category
const shade = (hex: string, f: number) => '#' + [1, 3, 5].map((i) => Math.round(parseInt(hex.slice(i, i + 2), 16) * f).toString(16).padStart(2, '0')).join('');
function pin(o: OgInput) {
  const t = o.title.replace(/\s*\([^)]*\)/g, '').replace(/\s+[–—-]\s+.*$/, '');
  const size = t.length > 40 ? 76 : t.length > 26 ? 88 : 100;
  const tick = (x: string) => h('div', { display: 'flex', alignItems: 'center', gap: 18, fontSize: 34, fontWeight: 500 }, [
    h('div', { width: 44, height: 44, borderRadius: 999, background: '#ffb547', display: 'flex', alignItems: 'center', justifyContent: 'center' },
      h('div', { width: 12, height: 22, borderRight: '5px solid #11163a', borderBottom: '5px solid #11163a', transform: 'rotate(45deg) translate(-2px,-3px)' })), x]);
  return h('div', { width: '100%', height: '100%', boxSizing: 'border-box', display: 'flex', flexDirection: 'column', padding: '80px 76px 76px', fontFamily: 'Jakarta', color: '#fff',
    backgroundColor: shade(o.color, 0.22), backgroundImage: `radial-gradient(circle at 100% 0%, ${o.color} 0%, ${o.color}66 38%, transparent 68%), radial-gradient(circle at 0% 100%, ${shade(o.color, 0.6)}cc 0%, transparent 60%)` }, [
    h('div', { display: 'flex', alignItems: 'center', gap: 20 }, [
      h('div', { width: 76, height: 76, borderRadius: 20, background: 'linear-gradient(135deg,#4f5bff,#8b5cf6)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 50, fontWeight: 800 }, 'Z'),
      h('div', { fontSize: 42, fontWeight: 800, display: 'flex' }, ['Zenta', h('span', { fontWeight: 500, marginLeft: 10, opacity: 0.85 }, 'Calculator')]),
    ]),
    h('div', { display: 'flex', alignSelf: 'flex-start', marginTop: 90, fontSize: 28, fontWeight: 800, letterSpacing: 4, padding: '12px 26px', borderRadius: 999, background: 'rgba(255,255,255,0.12)', border: '1px solid rgba(255,255,255,0.25)', textTransform: 'uppercase' }, o.kicker),
    h('div', { marginTop: 34, fontSize: size, fontWeight: 800, lineHeight: 1.04, letterSpacing: -2.5 }, t),
    h('div', { marginTop: 40, fontSize: 40, fontWeight: 500, opacity: 0.9, lineHeight: 1.4 }, rs(o.sub ?? '')),
    o.formula && o.formula.length <= 26
      ? h('div', { display: 'flex', alignSelf: 'flex-start', marginTop: 48, fontFamily: 'Mono', fontSize: 48, padding: '22px 34px', borderRadius: 18, background: 'rgba(255,255,255,0.08)', border: '2px solid #ffb547', color: '#ffd28a' }, o.formula)
      : h('div', { display: 'flex' }, ''),
    h('div', { display: 'flex', flexDirection: 'column', gap: 22, marginTop: 'auto' }, [tick('Solve for any value'), tick('Formula and steps shown'), tick('Free, no sign-up')]),
    h('div', { display: 'flex', alignItems: 'center', justifyContent: 'center', marginTop: 56, padding: '26px 0', borderRadius: 999, background: '#fff', color: '#11163a', fontSize: 40, fontWeight: 800 }, 'Try it free at zentacalculator.com'),
  ]);
}

const CACHE = join(process.cwd(), '.og-cache');
export async function ogPng(o: OgInput, tall = false): Promise<Buffer> {
  const key = createHash('sha1').update(JSON.stringify(o) + (tall ? 'pin4' : 'v4')).digest('hex');
  const f = join(CACHE, key + '.jpg');
  if (existsSync(f)) return readFileSync(f);
  const [w, hh] = tall ? [1000, 1500] : [1200, 630];
  const svg = await satori((tall ? pin(o) : card(o)) as any, { width: w, height: hh, fonts: fonts() });
  const png = await sharp(new Resvg(svg, { fitTo: { mode: 'width', value: w } }).render().asPng()).jpeg({ quality: 84, mozjpeg: true }).toBuffer();
  mkdirSync(CACHE, { recursive: true }); writeFileSync(f, png);
  return png;
}
