import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const variable = z.object({
  id: z.string().regex(/^[A-Za-z_][A-Za-z0-9_]*$/).refine((id) => !['pi', 'e', 'g0'].includes(id) && !id.startsWith('data_'), 'reserved name (pi, e, g0, data_*)'),
  label: z.string(),
  family: z.string().default('none'),       // unit family from src/lib/units.ts
  unit: z.string().optional(),              // default display unit id
  imperialUnit: z.string().optional(),      // default unit for US visitors (e.g. lb, in, °F)
  default: z.number().optional(),           // default value in the DISPLAY unit
  min: z.number().optional(),               // bounds in BASE units (used by the solver)
  max: z.number().optional(),
  prefix: z.string().optional(),            // e.g. "₹" or "$"
  suffix: z.string().optional(),            // fixed label for family "none"
  help: z.string().optional(),
  decimals: z.number().int().min(0).max(10).optional(), // round displayed results
  options: z.array(z.object({ label: z.string(), value: z.number() })).optional(),
  bands: z.array(z.object({ max: z.number(), label: z.string(), color: z.string() })).optional(),
});

const calculators = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/calculators' }),
  schema: z.object({
    title: z.string(),
    description: z.string().max(170),
    category: z.string(),
    keywords: z.array(z.string()).default([]),
    updated: z.coerce.date(),
    author: z.string().default('santaji-gadepatil'), // id from src/data/authors.ts
    reviewer: z.string().optional(),
    featured: z.boolean().default(false),
    variables: z.array(variable).min(2),
    equations: z.array(z.string()).min(1),
    freedom: z.number().optional(),         // how many fields the user must fill (default vars - equations)
    chart: z.object({ x: z.string(), y: z.string(), from: z.number().optional(), to: z.number().optional() }).optional(),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    related: z.array(z.string()).default([]),
    intro: z.string().optional(), // 1–3 sentence topic intro shown above the calculator; supports [text](url) and **bold**
    links: z.array(z.object({ title: z.string(), url: z.string().url(), note: z.string().optional() })).default([]), // external further reading
    dataset: z.object({ label: z.string(), default: z.string().optional(), placeholder: z.string().optional(), help: z.string().optional() }).optional(), // list input → data_n, data_mean, data_median, data_mode, data_sd …
  }),
});

export const collections = { calculators };
