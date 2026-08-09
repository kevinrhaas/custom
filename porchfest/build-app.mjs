// Inject the baked payload into the template -> app/index.html (single file).
import fs from 'node:fs';
import path from 'node:path';
const here = path.dirname(new URL(import.meta.url).pathname);
const tpl  = fs.readFileSync(path.join(here, 'app.template.html'), 'utf8');
const data = fs.readFileSync(path.join(here, 'data.json'), 'utf8');
if (!tpl.includes('/*__DATA__*/')) { console.error('template lost its /*__DATA__*/ marker'); process.exit(1); }
// </script> inside JSON would close the host <script> tag early.
const safe = data.replace(/<\//g, '<\\/');
const out = tpl.replace('/*__DATA__*/', safe);
const dest = path.join(here, '..', 'site', 'porchfest', 'app', 'index.html');
fs.writeFileSync(dest, out);
console.log(`wrote ${path.relative(process.cwd(), dest)}  ${(out.length/1024).toFixed(1)} KB`);
