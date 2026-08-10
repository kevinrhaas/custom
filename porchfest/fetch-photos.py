#!/usr/bin/env python3
"""fetch-photos.py — pull the band photos local and shrink them to card size.

The lineup links full-resolution camera JPEGs on the festival's S3 bucket —
5000px wide, several megabytes each. The app showed all 91 in the band browser,
so browsing the lineup pulled hundreds of megabytes off someone else's bucket,
over the same saturated cell tower the whole app is designed to avoid needing.

This downloads each one once and writes a card-sized thumbnail into
../site/porchfest/app/img/<id>.jpg. The app then references them relatively:
same origin, cached, and no hotlink to break when the festival tidies up.

They stay as files rather than data URIs inlined into the page. Routing has to
work instantly on a dead tower and it does — the payload with the street graph
and every set time is already in the page. Photos are decoration: they load
lazily as you scroll the browser, and degrade to the band's initials when they
do not. Inlining ~2MB of base64 would slow the thing that matters to speed up
the thing that does not.

    python3 fetch-photos.py            # skips anything already downloaded
    python3 fetch-photos.py --force    # re-fetch everything
"""
import json, os, sys, subprocess, io
from PIL import Image, ImageOps

# Three of the photos are HEIC straight off an iPhone. Those never rendered in
# the live app at all outside Safari — Chrome and Firefox cannot decode HEIC —
# so converting them here fixes them rather than merely relocating them.
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    print('note: pillow-heif not installed — HEIC photos will be skipped')

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'site', 'porchfest', 'app', 'img')
DATA = os.path.join(HERE, 'data.json')
MAP = os.path.join(HERE, 'photos.json')

# The card photo is 132px tall in a column that is at most ~420px wide, and
# retina doubles that. 640x360 covers it with room to spare.
MAX_W, MAX_H, QUALITY = 640, 360, 78

force = '--force' in sys.argv
os.makedirs(OUT, exist_ok=True)
bands = json.load(open(DATA))['bands']
todo = [b for b in bands if b.get('img')]

mapping, kept, skipped, failed, total_in, total_out = {}, 0, 0, [], 0, 0

for i, b in enumerate(todo, 1):
    dest = os.path.join(OUT, b['id'] + '.jpg')
    rel = 'img/' + b['id'] + '.jpg'
    if os.path.exists(dest) and not force:
        mapping[b['id']] = rel
        skipped += 1
        continue
    try:
        raw = subprocess.run(['curl', '-sSL', '--max-time', '90', b['img']],
                             capture_output=True, check=True).stdout
        if not raw:
            raise RuntimeError('empty response')
        total_in += len(raw)
        im = Image.open(io.BytesIO(raw))
        # Honour the camera's rotation flag, or portraits arrive on their side.
        im = ImageOps.exif_transpose(im)
        im = im.convert('RGB')
        im.thumbnail((MAX_W, MAX_H), Image.LANCZOS)
        im.save(dest, 'JPEG', quality=QUALITY, optimize=True, progressive=True)
        total_out += os.path.getsize(dest)
        mapping[b['id']] = rel
        kept += 1
        print(f"  [{i}/{len(todo)}] {b['n'][:34]:36s} "
              f"{len(raw)/1e6:5.1f}MB -> {os.path.getsize(dest)/1024:5.1f}KB")
    except Exception as e:
        failed.append((b['n'], str(e)[:70]))
        print(f"  [{i}/{len(todo)}] {b['n'][:34]:36s} FAILED: {str(e)[:60]}")

json.dump(mapping, open(MAP, 'w'))
print(f"\nfetched {kept}, already had {skipped}, failed {len(failed)}")
if kept:
    print(f"{total_in/1e6:.0f} MB downloaded -> {total_out/1e6:.1f} MB stored "
          f"({total_out/total_in*100:.1f}%)")
if failed:
    print("FAILURES (these bands fall back to their initials):")
    for n, e in failed:
        print(f"  {n}: {e}")
print(f"wrote photos.json ({len(mapping)} entries)")
