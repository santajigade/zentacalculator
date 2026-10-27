// Unit families. Every value is stored internally in the family's base unit
// (first entry, factor 1). Equations in calculator files are written in base units.
// display = (base - offset) / factor   |   base = display * factor + offset

export interface Unit { id: string; label: string; factor: number; offset?: number; }

export const UNIT_FAMILIES: Record<string, Unit[]> = {
  none: [{ id: '', label: '', factor: 1 }],
  length: [
    { id: 'm', label: 'm', factor: 1 },
    { id: 'mm', label: 'mm', factor: 1e-3 },
    { id: 'cm', label: 'cm', factor: 1e-2 },
    { id: 'km', label: 'km', factor: 1e3 },
    { id: 'in', label: 'in', factor: 0.0254 },
    { id: 'ft', label: 'ft', factor: 0.3048 },
    { id: 'yd', label: 'yd', factor: 0.9144 },
    { id: 'mi', label: 'mi', factor: 1609.344 },
    { id: 'nmi', label: 'nmi', factor: 1852 },
    { id: 'um', label: 'µm', factor: 1e-6 },
  ],
  mass: [
    { id: 'kg', label: 'kg', factor: 1 },
    { id: 'g', label: 'g', factor: 1e-3 },
    { id: 'mg', label: 'mg', factor: 1e-6 },
    { id: 't', label: 't', factor: 1e3 },
    { id: 'lb', label: 'lb', factor: 0.45359237 },
    { id: 'oz', label: 'oz', factor: 0.028349523125 },
    { id: 'st', label: 'st', factor: 6.35029318 },
  ],
  time: [
    { id: 'yr', label: 'years', factor: 1 },
    { id: 'mo', label: 'months', factor: 1 / 12 },
    { id: 'wk', label: 'weeks', factor: 7 / 365.25 },
    { id: 'd', label: 'days', factor: 1 / 365.25 },
    { id: 'h', label: 'hours', factor: 1 / 8766 },
    { id: 'min', label: 'minutes', factor: 1 / 525960 },
    { id: 's', label: 'seconds', factor: 1 / 31557600 },
  ],
  percent: [
    { id: '%', label: '%', factor: 0.01 },
    { id: 'frac', label: 'fraction', factor: 1 },
  ],
  temperature: [
    { id: 'K', label: 'K', factor: 1 },
    { id: 'C', label: '°C', factor: 1, offset: 273.15 },
    { id: 'F', label: '°F', factor: 5 / 9, offset: 273.15 - (32 * 5) / 9 },
  ],
  pressure: [
    { id: 'Pa', label: 'Pa', factor: 1 },
    { id: 'kPa', label: 'kPa', factor: 1e3 },
    { id: 'bar', label: 'bar', factor: 1e5 },
    { id: 'mbar', label: 'mbar', factor: 100 },
    { id: 'psi', label: 'psi', factor: 6894.757293168 },
    { id: 'atm', label: 'atm', factor: 101325 },
    { id: 'mmHg', label: 'mmHg', factor: 133.322387415 },
    { id: 'mH2O', label: 'mH₂O', factor: 9806.65 },
    { id: 'inH2O', label: 'inH₂O', factor: 249.08891 },
    { id: 'MPa', label: 'MPa', factor: 1e6 },
  ],
  voltage: [
    { id: 'V', label: 'V', factor: 1 },
    { id: 'mV', label: 'mV', factor: 1e-3 },
    { id: 'kV', label: 'kV', factor: 1e3 },
  ],
  current: [
    { id: 'A', label: 'A', factor: 1 },
    { id: 'mA', label: 'mA', factor: 1e-3 },
    { id: 'uA', label: 'µA', factor: 1e-6 },
    { id: 'kA', label: 'kA', factor: 1e3 },
  ],
  resistance: [
    { id: 'ohm', label: 'Ω', factor: 1 },
    { id: 'mohm', label: 'mΩ', factor: 1e-3 },
    { id: 'kohm', label: 'kΩ', factor: 1e3 },
    { id: 'Mohm', label: 'MΩ', factor: 1e6 },
  ],
  power: [
    { id: 'W', label: 'W', factor: 1 },
    { id: 'mW', label: 'mW', factor: 1e-3 },
    { id: 'kW', label: 'kW', factor: 1e3 },
    { id: 'MW', label: 'MW', factor: 1e6 },
    { id: 'hp', label: 'hp', factor: 745.69987158 },
    { id: 'PS', label: 'PS (metric hp)', factor: 735.49875 },
    { id: 'BTUh', label: 'BTU/h', factor: 0.29307107 },
    { id: 'TR', label: 'ton (refrig.)', factor: 3516.8528 },
  ],
  area: [
    { id: 'm2', label: 'm²', factor: 1 },
    { id: 'cm2', label: 'cm²', factor: 1e-4 },
    { id: 'mm2', label: 'mm²', factor: 1e-6 },
    { id: 'km2', label: 'km²', factor: 1e6 },
    { id: 'ha', label: 'ha', factor: 1e4 },
    { id: 'in2', label: 'in²', factor: 0.00064516 },
    { id: 'ft2', label: 'ft²', factor: 0.09290304 },
    { id: 'yd2', label: 'yd²', factor: 0.83612736 },
    { id: 'acre', label: 'acre', factor: 4046.8564224 },
  ],
  volume: [
    { id: 'm3', label: 'm³', factor: 1 },
    { id: 'L', label: 'L', factor: 1e-3 },
    { id: 'mL', label: 'mL', factor: 1e-6 },
    { id: 'cm3', label: 'cm³', factor: 1e-6 },
    { id: 'in3', label: 'in³', factor: 1.6387064e-5 },
    { id: 'ft3', label: 'ft³', factor: 0.028316846592 },
    { id: 'galUS', label: 'US gal', factor: 0.003785411784 },
    { id: 'galUK', label: 'UK gal', factor: 0.00454609 },
    { id: 'cup', label: 'US cup', factor: 0.0002365882365 },
    { id: 'cupM', label: 'metric cup', factor: 0.00025 },
    { id: 'floz', label: 'US fl oz', factor: 0.0000295735295625 },
    { id: 'tbsp', label: 'tbsp', factor: 0.00001478676478125 },
    { id: 'tsp', label: 'tsp', factor: 0.00000492892159375 },
  ],
  flow: [
    { id: 'm3s', label: 'm³/s', factor: 1 },
    { id: 'm3h', label: 'm³/h', factor: 1 / 3600 },
    { id: 'Lmin', label: 'L/min', factor: 1e-3 / 60 },
    { id: 'Ls', label: 'L/s', factor: 1e-3 },
    { id: 'gpm', label: 'US gpm', factor: 0.003785411784 / 60 },
    { id: 'cfm', label: 'ft³/min', factor: 0.028316846592 / 60 },
  ],
  velocity: [
    { id: 'ms', label: 'm/s', factor: 1 },
    { id: 'kmh', label: 'km/h', factor: 1 / 3.6 },
    { id: 'fts', label: 'ft/s', factor: 0.3048 },
    { id: 'mph', label: 'mph', factor: 0.44704 },
    { id: 'kn', label: 'knots', factor: 1852 / 3600 },
  ],
  density: [
    { id: 'kgm3', label: 'kg/m³', factor: 1 },
    { id: 'gcm3', label: 'g/cm³', factor: 1000 },
    { id: 'lbft3', label: 'lb/ft³', factor: 16.01846337 },
  ],
  viscosity: [
    { id: 'Pas', label: 'Pa·s', factor: 1 },
    { id: 'mPas', label: 'mPa·s', factor: 1e-3 },
    { id: 'cP', label: 'cP', factor: 1e-3 },
    { id: 'P', label: 'P', factor: 0.1 },
  ],
  energy: [
    { id: 'J', label: 'J', factor: 1 },
    { id: 'kJ', label: 'kJ', factor: 1e3 },
    { id: 'MJ', label: 'MJ', factor: 1e6 },
    { id: 'Wh', label: 'Wh', factor: 3600 },
    { id: 'kWh', label: 'kWh', factor: 3.6e6 },
    { id: 'cal', label: 'cal', factor: 4.184 },
    { id: 'kcal', label: 'kcal', factor: 4184 },
    { id: 'BTU', label: 'BTU', factor: 1055.05585 },
    { id: 'therm', label: 'therm', factor: 105505585 },
  ],
  force: [
    { id: 'N', label: 'N', factor: 1 },
    { id: 'kN', label: 'kN', factor: 1e3 },
    { id: 'kgf', label: 'kgf', factor: 9.80665 },
    { id: 'tf', label: 'tonne-force', factor: 9806.65 },
    { id: 'lbf', label: 'lbf', factor: 4.4482216152605 },
  ],
  torque: [
    { id: 'Nm', label: 'N·m', factor: 1 },
    { id: 'kNm', label: 'kN·m', factor: 1e3 },
    { id: 'lbft', label: 'lbf·ft', factor: 1.3558179483314 },
    { id: 'lbin', label: 'lbf·in', factor: 0.1129848290276 },
    { id: 'kgfm', label: 'kgf·m', factor: 9.80665 },
  ],
  massflow: [
    { id: 'kgs', label: 'kg/s', factor: 1 },
    { id: 'kgh', label: 'kg/h', factor: 1 / 3600 },
    { id: 'th', label: 't/h', factor: 1000 / 3600 },
    { id: 'lbh', label: 'lb/h', factor: 0.45359237 / 3600 },
    { id: 'lbs', label: 'lb/s', factor: 0.45359237 },
  ],
  tempdiff: [
    { id: 'K', label: 'K / °C', factor: 1 },
    { id: 'F', label: '°F', factor: 5 / 9 },
  ],
  angle: [
    { id: 'rad', label: 'rad', factor: 1 },
    { id: 'deg', label: '°', factor: Math.PI / 180 },
    { id: 'grad', label: 'grad', factor: Math.PI / 200 },
    { id: 'turn', label: 'turns', factor: 2 * Math.PI },
  ],
  capacitance: [
    { id: 'F', label: 'F', factor: 1 },
    { id: 'mF', label: 'mF', factor: 1e-3 },
    { id: 'uF', label: 'µF', factor: 1e-6 },
    { id: 'nF', label: 'nF', factor: 1e-9 },
    { id: 'pF', label: 'pF', factor: 1e-12 },
  ],
  seconds: [
    { id: 's', label: 's', factor: 1 },
    { id: 'ms', label: 'ms', factor: 1e-3 },
    { id: 'min', label: 'min', factor: 60 },
    { id: 'h', label: 'h', factor: 3600 },
  ],
  data: [
    { id: 'B', label: 'B', factor: 1 },
    { id: 'bit', label: 'bit', factor: 0.125 },
    { id: 'kB', label: 'kB', factor: 1e3 },
    { id: 'MB', label: 'MB', factor: 1e6 },
    { id: 'GB', label: 'GB', factor: 1e9 },
    { id: 'TB', label: 'TB', factor: 1e12 },
    { id: 'KiB', label: 'KiB', factor: 1024 },
    { id: 'MiB', label: 'MiB', factor: 1024 ** 2 },
    { id: 'GiB', label: 'GiB', factor: 1024 ** 3 },
    { id: 'TiB', label: 'TiB', factor: 1024 ** 4 },
  ],
  land: [ // land-area units used in South Asia (local units vary by state; these are the common definitions)
    { id: 'm2', label: 'm²', factor: 1 },
    { id: 'ft2', label: 'sq ft', factor: 0.09290304 },
    { id: 'yd2', label: 'sq yd (gaj)', factor: 0.83612736 },
    { id: 'acre', label: 'acre', factor: 4046.8564224 },
    { id: 'ha', label: 'hectare', factor: 1e4 },
    { id: 'cent', label: 'cent', factor: 40.468564224 },
    { id: 'guntha', label: 'guntha', factor: 101.17141056 },
    { id: 'kanal', label: 'kanal', factor: 505.857053 },
    { id: 'marla', label: 'marla', factor: 25.2928526 },
  ],
  currency: [{ id: '', label: '', factor: 1 }],
  date: [{ id: 'date', label: '', factor: 1 }],   // value = days since 1970-01-01 (UTC)
  clock: [{ id: 'clock', label: '', factor: 1 }], // value = hours after midnight
};

export function getUnits(family: string): Unit[] {
  const u = UNIT_FAMILIES[family];
  if (!u) throw new Error(`Unknown unit family "${family}"`);
  return u;
}
export function findUnit(family: string, id?: string): Unit {
  const units = getUnits(family);
  return units.find((u) => u.id === id) ?? units[0];
}
export const toBase = (v: number, u: Unit) => v * u.factor + (u.offset ?? 0);
export const fromBase = (v: number, u: Unit) => (v - (u.offset ?? 0)) / u.factor;
