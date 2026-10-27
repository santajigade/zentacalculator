import { SITE } from '../site.config.ts';
export const GET = () => new Response(`User-agent: *\nAllow: /\nDisallow: /embed/\n\nSitemap: ${SITE.url}/sitemap-index.xml\n`);
