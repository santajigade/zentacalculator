def L(*items):
    """items: (slug, title[, note]) -> YAML 'links:' block for frontmatter."""
    out = 'links:\n'
    for it in items:
        slug, title = it[0], it[1]
        note = f', note: "{it[2]}"' if len(it) > 2 else ''
        out += f'  - {{ title: "{title}", url: "https://www.instrumentationblog.in/{slug}/"{note} }}\n'
    return out

import json as _json, re as _re
def intro(text):
    """intro: line with [label](ib:slug) expanded to instrumentationblog.in URLs, JSON-quoted for YAML."""
    t = _re.sub(r'\]\(ib:([a-z0-9-]+)\)', lambda m: f'](https://www.instrumentationblog.in/{m.group(1)}/)', text)
    return 'intro: ' + _json.dumps(t, ensure_ascii=False)
