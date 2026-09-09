import {copyFileSync, existsSync, mkdirSync, readdirSync, readFileSync} from 'node:fs';
import {join} from 'node:path';

// This Vinext release skips prerendering redirected routes with trailingSlash.
// Keep its default export and also provide directory indexes for static hosts.
const output = 'dist/client';
const pages = readdirSync('app', {recursive: true}).filter(name => /(^|[/\\])page\.tsx$/.test(name));
for (const page of pages) {
  const route = page.replace(/[/\\]?page\.tsx$/, '').replaceAll('\\', '/');
  const html = join(output, route ? `${route}.html` : 'index.html');
  if (!existsSync(html)) throw new Error(`Missing exported route: /${route}. The build is incomplete.`);
  if (route) {
    const directory = join(output, route);
    mkdirSync(directory, {recursive: true});
    copyFileSync(html, join(directory, 'index.html'));
    const rsc = join(output, `${route}.rsc`);
    if (existsSync(rsc)) copyFileSync(rsc, join(directory, 'index.rsc'));
  }
}

// Confirm public files referenced by the master content made it into the export.
const academic = JSON.parse(readFileSync('app/generated/academic.json', 'utf8'));
function check(value) {
  if (Array.isArray(value)) return value.forEach(check);
  if (!value || typeof value !== 'object') return;
  for (const [key, item] of Object.entries(value)) {
    if (['url', 'pdf', 'appendix', 'portrait', 'replication_url'].includes(key) && typeof item === 'string' && item.startsWith('/')) {
      const pathname = decodeURIComponent(new URL(item, 'https://local.invalid').pathname);
      if (!existsSync(join(output, pathname.slice(1)))) throw new Error(`Missing exported file: ${pathname}`);
    } else check(item);
  }
}
check(academic);
if (!existsSync(join(output, 'Matthias-Fleckenstein-CV.pdf'))) throw new Error('Missing exported CV.');
console.log(`Verified ${pages.length} exported pages, the CV, and all local content links.`);
