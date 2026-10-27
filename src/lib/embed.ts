/** iframe + attribution link + auto-resize listener, used by the Embed dialog and the on-page embed box */
export function embedSnippet(siteUrl: string, siteName: string, title: string, path: string): string {
  const page = siteUrl + path, src = siteUrl + '/embed' + path;
  return `<iframe src="${src}" title="${title}" width="100%" height="640" style="border:1px solid #e2e5ee;border-radius:12px;max-width:720px" loading="lazy"></iframe>\n`
    + `<p style="font-size:13px"><a href="${page}">${title}</a> by <a href="${siteUrl}/">${siteName}</a></p>\n`
    + `<script>addEventListener('message',function(e){if(e.origin==='${siteUrl}'&&e.data&&e.data.zentaHeight){document.querySelectorAll('iframe[src="${src}"]').forEach(function(f){if(f.contentWindow===e.source)f.style.height=e.data.zentaHeight+'px'})}})</script>`;
}
