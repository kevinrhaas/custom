#!/usr/bin/env python3
"""Bundle the app into one self-contained page for publishing as an Artifact.

The artifact sandbox blocks every external host, so nothing can be a separate
file or a remote image: CSS, both data files and the app all inline, and the
photos become data: URIs. Remote gallery URLs are replaced by the embedded copy
rather than left to fail silently against the CSP."""
import base64, io, json, os, re, sys
from PIL import Image

ARTW = 620          # cards render ~310 CSS px; 620 is already retina

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
rd = lambda *p: open(os.path.join(HERE, *p), encoding='utf-8').read()

html = rd('index.html')
title = re.search(r'<title>(.*?)</title>', html, re.S).group(1)
body = html[html.index('<body>') + len('<body>'):html.index('</body>')]
body = re.sub(r'\s*<script src="js/[^"]+"></script>', '', body)

# data.js -> photos as data URIs
data_src = rd('js', 'data.js')
DATA = json.loads(data_src[data_src.index('{'):data_src.rindex(';')])
embedded = 0
for p in DATA['properties']:
    if not p.get('photo'):
        p['images'] = []                       # remote URLs cannot load here
        continue
    im = Image.open(os.path.join(HERE, p['photo'])).convert('RGB')
    if im.width > ARTW:                        # re-encode smaller: every byte is inlined
        im = im.resize((ARTW, round(im.height * ARTW / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=72, optimize=True)
    # Only one copy of the bytes: the lightbox already falls back to `photo`
    # when `images` is empty, and embedding both would double the page.
    p['photo'] = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    p['images'] = []
    embedded += 1

out = [f'<title>{title}</title>',
       '<style>\n' + rd('css', 'app.css') + '\n</style>',
       body.strip(),
       '<script>\n' + rd('js', 'geo.js') + '\n</script>',
       '<script>\nwindow.STAY_DATA = ' + json.dumps(DATA, separators=(',', ':')) + ';\n</script>',
       '<script>\n' + rd('js', 'app.js') + '\n</script>']
page = '\n\n'.join(out)

dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'artifact.html')
open(dest, 'w', encoding='utf-8').write(page)
print(f'{dest} — {len(page)/1e6:.2f} MB, {embedded} photos embedded')
