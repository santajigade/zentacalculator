// Pinterest pin schedule: which calculators have been released to the pin feed so far.
import { allCalcs, type Calc } from './calcs.ts';
import SCHEDULE from '../data/pins.json';
import MANUAL from '../data/pins-manual.json';

/** Pins uploaded by hand (.csv); they get images but stay out of the RSS feed so Pinterest does not pin them twice. */
export const manualPins = new Set(MANUAL as string[]);

const DAY = 864e5;
const today = () => new Date(Date.now() + 5.5 * 3600e3).toISOString().slice(0, 10); // IST date

/** Released pins, newest first. Backlog follows src/data/pins.json (4 a day); new calculators are pinned the day after they go live. */
export async function pinQueue(): Promise<{ calc: Calc; date: string }[]> {
  const t = today();
  const sched = SCHEDULE as Record<string, string>;
  return (await allCalcs())
    .map((calc) => ({ calc, date: sched[calc.id] ?? new Date(+new Date(calc.data.updated) + DAY).toISOString().slice(0, 10) }))
    .filter((p) => p.date <= t)
    .sort((a, b) => b.date.localeCompare(a.date) || a.calc.id.localeCompare(b.calc.id));
}
