import { defineConfig } from 'astro/config';
import preact from '@astrojs/preact';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { readdirSync, existsSync } from 'node:fs';

// Empty categories are noindex, so keep them out of the sitemap too
const contentDir = './src/content/calculators';
const filled = new Set(existsSync(contentDir)
  ? readdirSync(contentDir, { withFileTypes: true })
      .filter((d) => d.isDirectory() && readdirSync(`${contentDir}/${d.name}`).some((f) => /\.mdx?$/.test(f)))
      .map((d) => d.name)
  : []);
const isEmptyCategory = (page) => {
  const m = /^https?:\/\/[^/]+\/([^/]+)\/$/.exec(page);
  const isPage = existsSync(`./src/pages/${m?.[1]}.md`) || existsSync(`./src/pages/${m?.[1]}.astro`);
  return m && !isPage && !filled.has(m[1]);
};

export default defineConfig({
  site: 'https://zentacalculator.com', // keep in sync with src/site.config.ts
  trailingSlash: 'always', // matches how Apache/Hostinger serves folders
  build: { format: 'directory' },
  integrations: [
    preact(),
    mdx(),
    sitemap({ filter: (page) => !page.includes('/embed/') && !page.includes('/404') && !isEmptyCategory(page) }),
  ],
});
