#!/usr/bin/env python3
"""Save one hero photo per property into site/stay/photos/<id>.jpg.

Listing photos are the first thing that rots: hosts swap galleries, PM sites
move paths, and CDN links go dead the day a house is delisted. Cards fall back
to remote URLs and then to a drawn placeholder, but a local copy is what keeps
the grid looking like something months from now. Downscaled hard — cards render
these around 310 CSS px, so 760 wide is already retina."""
import json, glob, io, os, subprocess, concurrent.futures as cf
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))          # stay/
OUT = os.path.join(HERE, '..', 'site', 'stay', 'photos')   # the app's photo folder
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')
MAXW, QUALITY = 760, 78

def variant(url):
    """Ask the CDN for a sane size where it understands how."""
    if 'muscache.com' in url and '?' not in url:
        return url + '?im_w=1200'
    return url

def grab(prop):
    imgs = prop.get('images') or []
    if not imgs: return (prop['id'], None, 'no image url')
    dest = os.path.join(OUT, prop['id'] + '.jpg')
    # idempotent: keep what we already have so re-runs only fetch what is new.
    # Delete a file (or the folder) to force it to be pulled again.
    if os.path.exists(dest) and os.path.getsize(dest) > 4000:
        return (prop['id'], os.path.getsize(dest), 'cached')
    for url in imgs[:3]:                       # first that actually works
        try:
            r = subprocess.run(['curl', '-sS', '-L', '--max-time', '25', '-A', UA, variant(url)],
                               capture_output=True, timeout=40)
            if r.returncode != 0 or len(r.stdout) < 4000: continue
            im = Image.open(io.BytesIO(r.stdout))
            im = im.convert('RGB')
            if im.width > MAXW:
                im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
            im.save(dest, 'JPEG', quality=QUALITY, optimize=True)
            return (prop['id'], os.path.getsize(dest), url)
        except Exception as e:
            continue
    return (prop['id'], None, 'all urls failed')

def main():
    os.makedirs(OUT, exist_ok=True)
    props = []
    for f in sorted(glob.glob(os.path.join(HERE, 'raw-*.json'))):
        props += json.load(open(f))['properties']
    ok = bytes_ = 0
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for pid, size, note in ex.map(grab, props):
            if size: ok += 1; bytes_ += size
            else: print(f'  no photo: {pid:44s} {note}')
    print(f'\n{ok}/{len(props)} photos saved, {bytes_/1e6:.1f} MB total')

if __name__ == '__main__':
    main()
