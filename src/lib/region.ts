// Guess the visitor's region in the browser (no tracking, no network):
// time zone first (more reliable than browser language), then language tag.

export interface Region { country: string; imperial: boolean; currency: string; locale: string; }

const TZ: [RegExp, string][] = [
  [/^Asia\/(Kolkata|Calcutta)$/, 'IN'],
  [/^America\/(Toronto|Vancouver|Edmonton|Winnipeg|Halifax|Regina|St_Johns|Montreal)$/, 'CA'],
  [/^America\/(New_York|Chicago|Denver|Los_Angeles|Phoenix|Anchorage|Detroit|Boise|Indiana|Kentucky|Juneau)/, 'US'],
  [/^Pacific\/Honolulu$/, 'US'],
  [/^Europe\/(London|Belfast)$/, 'GB'],
  [/^Europe\/Dublin$/, 'IE'],
  [/^Europe\/Zurich$/, 'CH'],
  [/^Europe\/(Stockholm)$/, 'SE'],
  [/^Europe\/(Oslo)$/, 'NO'],
  [/^Europe\/(Copenhagen)$/, 'DK'],
  [/^Europe\/(Warsaw)$/, 'PL'],
  [/^Europe\//, 'EU'],
  [/^Australia\//, 'AU'],
  [/^Pacific\/Auckland$/, 'NZ'],
  [/^Asia\/Tokyo$/, 'JP'],
  [/^Asia\/(Dubai|Muscat)$/, 'AE'],
  [/^Asia\/Riyadh$/, 'SA'],
  [/^Asia\/Singapore$/, 'SG'],
  [/^Asia\/(Karachi)$/, 'PK'],
  [/^Asia\/(Dhaka)$/, 'BD'],
  [/^Africa\/Lagos$/, 'NG'],
  [/^Africa\/Johannesburg$/, 'ZA'],
];

const CURRENCY: Record<string, string> = {
  US: '$', CA: '$', AU: '$', NZ: '$', SG: '$', IN: '₹', GB: '£', IE: '€', EU: '€',
  CH: 'CHF ', SE: 'kr ', NO: 'kr ', DK: 'kr ', PL: 'zł ', JP: '¥', AE: 'AED ', SA: 'SAR ',
  PK: '₨', BD: '৳', NG: '₦', ZA: 'R ', DE: '€', FR: '€', ES: '€', IT: '€', NL: '€',
};
const IMPERIAL = new Set(['US', 'LR', 'MM']);

export function detectRegion(): Region {
  let country = '';
  let locale = 'en-US';
  try {
    locale = navigator.language || locale;
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    country = TZ.find(([re]) => re.test(tz))?.[1] ?? '';
    if (!country) {
      for (const l of navigator.languages ?? [navigator.language]) {
        const m = /-([A-Z]{2})$/i.exec(l);
        if (m) { country = m[1].toUpperCase(); break; }
      }
    }
  } catch { /* SSR or locked-down browser */ }
  if (!country) country = 'US';
  return { country, imperial: IMPERIAL.has(country), currency: CURRENCY[country] ?? '$', locale };
}
