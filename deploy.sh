#!/usr/bin/env bash
# Build the site and publish dist/ to the `site` branch (Hostinger pulls this branch into public_html).
set -euo pipefail
npm ci --silent || npm install --silent
npm test
npx astro build
TMP=$(mktemp -d)
cp -r dist/. "$TMP"/
git -C "$TMP" init -q -b site
git -C "$TMP" add -A
git -C "$TMP" -c user.name="Zenta Calculator" -c user.email="santaji.gade@gmail.com" commit -q -m "Publish site $(date -u +%Y-%m-%dT%H:%MZ)"
git -C "$TMP" push -q -f "$(git remote get-url origin)" site:site
echo "Published to branch 'site'."
