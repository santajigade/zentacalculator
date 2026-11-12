#!/usr/bin/env bash
# Build the site and publish dist/ to the `site` branch (Hostinger pulls this branch into public_html).
set -euo pipefail
npm ci --silent || npm install --silent
npm test
npx astro build
TMP=$(mktemp -d)
cp -r dist/. "$TMP"/
# Keep previous builds' hashed assets so pages cached in browsers/CDN never lose their CSS/JS
OLD_TREE=$(mktemp)
if git fetch -q origin site 2>/dev/null; then
  git ls-tree -r FETCH_HEAD > "$OLD_TREE" 2>/dev/null || true
  git archive FETCH_HEAD _astro 2>/dev/null | tar -x -C "$TMP" --skip-old-files 2>/dev/null || true
fi
git -C "$TMP" init -q -b site
git -C "$TMP" add -A
git -C "$TMP" -c user.name="Zenta Calculator" -c user.email="santaji.gade@gmail.com" commit -q -m "Publish site $(date -u +%Y-%m-%dT%H:%MZ)"
git -C "$TMP" push -q -f "$(git remote get-url origin)" site:site
echo "Published to branch 'site'."
# Ping Bing/IndexNow with the pages that changed (only from GitHub Actions; never fails the publish)
if [ -n "${GITHUB_ACTIONS:-}" ]; then sleep 90; python3 tools/indexnow.py "$OLD_TREE" dist || true; fi
