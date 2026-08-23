#!/usr/bin/env python3
"""Build the Stay Finder map geometry: site/stay/js/geo.js.

Downloads four layers from US Census TIGERweb (public domain), clips them to
the map frame, simplifies with Douglas-Peucker and writes the app's geo.js.
The downloads are ~20 MB and are cached in geo-cache/, which is gitignored —
delete it to force a refetch. Nothing here is a judgement call, so the output
is regenerable from scratch:

    python3 build-geo.py

Why these four and not a coastline layer: TIGER has no coastline product. The
land polygon (USLandmass) is shoreline-clipped but generalised, and the areal
water layer is detailed but stops at the 3-mile county limit. Neither alone is
a map. Together, painted water -> land -> water, they are: see the paint-order
note in the generated header.
"""
import json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'geo-cache')
OUT = os.path.join(HERE, '..', 'site', 'stay', 'js', 'geo.js')

W,E,S,N = -83.85, -81.10, 26.50, 29.95   # map frame

TIGER = 'https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb'
ENVELOPE = f'{W},{S},{E},{N}'
SOURCES = {
    # shoreline-clipped state land polygon
    'landmass.json': (f'{TIGER}/USLandmass/MapServer/0/query',
                      [('where', "NAME='Florida'")]),
    # bays, sounds and coastal water — the detailed shoreline
    'water.json':    (f'{TIGER}/Hydro/MapServer/1/query',
                      [('where', "MTFCC IN ('H2051','H2053')")]),
    'lakes.json':    (f'{TIGER}/Hydro/MapServer/1/query',
                      [('where', "MTFCC IN ('H2030','H2040') AND NAME IS NOT NULL")]),
    'rivers.json':   (f'{TIGER}/Hydro/MapServer/0/query',
                      [('where', "MTFCC='H3010' AND NAME IS NOT NULL")]),
}

def fetch(name):
    """Download one TIGERweb layer as GeoJSON, cached on disk."""
    path = os.path.join(CACHE, name)
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    os.makedirs(CACHE, exist_ok=True)
    url, extra = SOURCES[name]
    args = ['curl', '-sS', '--max-time', '300', '-o', path, '-G', url]
    params = extra + [('outFields', 'NAME,MTFCC'), ('returnGeometry', 'true'),
                      ('f', 'geojson'), ('geometryPrecision', '5')]
    if name != 'landmass.json':                 # the state polygon needs no envelope
        params += [('geometry', ENVELOPE), ('geometryType', 'esriGeometryEnvelope'),
                   ('inSR', '4326'), ('spatialRel', 'esriSpatialRelIntersects')]
    for k, v in params:
        args += ['--data-urlencode', f'{k}={v}']
    print(f'  fetching {name} ...', flush=True)
    if subprocess.run(args).returncode != 0 or not os.path.exists(path):
        sys.exit(f'could not download {name} from TIGERweb')
    return path

# ---------- Sutherland-Hodgman clip of a ring against the frame ----------
def clip_poly(ring):
    def inside(p, edge):
        return {'l':p[0]>=W,'r':p[0]<=E,'b':p[1]>=S,'t':p[1]<=N}[edge]
    def isect(a, b, edge):
        (x1,y1),(x2,y2) = a,b
        if edge in ('l','r'):
            x = W if edge=='l' else E
            t = (x-x1)/(x2-x1) if x2!=x1 else 0.0
            return [x, y1+t*(y2-y1)]
        y = S if edge=='b' else N
        t = (y-y1)/(y2-y1) if y2!=y1 else 0.0
        return [x1+t*(x2-x1), y]
    out = ring
    for edge in ('l','r','b','t'):
        if not out: return []
        inp, out = out, []
        for i in range(len(inp)):
            cur, prv = inp[i], inp[i-1]
            ci, pi = inside(cur,edge), inside(prv,edge)
            if ci:
                if not pi: out.append(isect(prv,cur,edge))
                out.append(cur)
            elif pi:
                out.append(isect(prv,cur,edge))
    return out

def clip_line(coords):
    runs, cur = [], []
    for i,p in enumerate(coords):
        if W<=p[0]<=E and S<=p[1]<=N:
            if not cur and i>0: cur.append(coords[i-1])
            cur.append(p)
        else:
            if cur: cur.append(p); runs.append(cur); cur=[]
    if cur: runs.append(cur)
    return [r for r in runs if len(r)>=2]

def rdp(pts, eps):
    if len(pts) < 3: return pts
    stack, keep = [(0,len(pts)-1)], [False]*len(pts)
    keep[0]=keep[-1]=True
    while stack:
        i,j = stack.pop()
        x1,y1 = pts[i]; x2,y2 = pts[j]
        dx,dy = x2-x1, y2-y1
        den = math.hypot(dx,dy) or 1e-12
        dmax,idx = 0.0,-1
        for k in range(i+1,j):
            x0,y0 = pts[k]
            d = abs(dy*x0 - dx*y0 + x2*y1 - y2*x1)/den
            if d>dmax: dmax,idx = d,k
        if idx>0 and dmax>eps:
            keep[idx]=True; stack.append((i,idx)); stack.append((idx,j))
    return [p for p,k in zip(pts,keep) if k]

def rdp_ring(ring, eps):
    """RDP on a closed ring. Plain RDP fails here: pts[0] and pts[-1] coincide,
    so the anchor line is degenerate and every deviation reads as zero. Split
    the ring at the vertex farthest from pts[0] and simplify the two arcs."""
    r = ring[:-1] if len(ring) > 1 and ring[0] == ring[-1] else ring[:]
    if len(r) < 4: return ring
    x0, y0 = r[0]
    far = max(range(len(r)), key=lambda i: (r[i][0]-x0)**2 + (r[i][1]-y0)**2)
    if far == 0: return ring
    a = rdp(r[:far+1], eps)
    b = rdp(r[far:] + [r[0]], eps)
    out = a[:-1] + b[:-1]
    return out + [out[0]] if len(out) >= 3 else ring

def rnd(pts, nd=4):
    out=[]
    for x,y in pts:
        p=[round(x,nd),round(y,nd)]
        if not out or p!=out[-1]: out.append(p)
    return out

def ring_area(r):   # deg^2, shoelace
    a=0.0
    for i in range(len(r)):
        x1,y1=r[i]; x2,y2=r[(i+1)%len(r)]
        a += x1*y2 - x2*y1
    return abs(a)/2

def poly_layer(path, eps, min_area, want_names=False):
    out=[]
    for f in json.load(open(path))['features']:
        g=f['geometry']; nm=(f['properties'].get('NAME') or '')
        polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
        for poly in polys:
            for ring in poly:                     # outer + holes both drawn
                c = clip_poly(ring)
                if len(c) < 4: continue
                s = rnd(rdp_ring(c, eps))
                if len(s) < 4 or ring_area(s) < min_area: continue
                out.append({'n':nm,'r':s} if want_names else s)
    return out


MAJOR = ('Suwannee','Withlacoochee','Crystal','Homosassa','Chassahowitzka','Weeki Wachee',
         'Hillsborough','Alafia','Manatee','Little Manatee','Anclote','Pithlachascotee',
         'Rainbow','Waccasassa','Steinhatchee','Myakka','Peace','Braden','Cotee')

def poly_features(path, eps, min_area, want_names=False):
    """Group rings BY FEATURE. Each feature paints as its own even-odd path, so
    outer+hole works per feature and adjacent county polygons can never cancel
    each other into phantom land."""
    out=[]
    for f in json.load(open(path))['features']:
        g=f['geometry']; nm=(f['properties'].get('NAME') or '')
        polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
        rings=[]
        for poly in polys:
            for ring in poly:
                c = clip_poly(ring)
                if len(c) < 4: continue
                s = rnd(rdp_ring(c, eps))
                if len(s) < 4 or ring_area(s) < min_area: continue
                rings.append(s)
        if rings:
            out.append({'n':nm,'p':rings} if want_names else {'p':rings})
    return out

# Paint order: frame filled with water, LAND on top, then bays/passes carved back.
# TIGER coastal water stops at the 3-mile county limit, so the open Gulf must
# come from the frame fill, not from a water polygon.
land  = poly_features(fetch('landmass.json'), 0.0003, 1e-5)
water = poly_features(fetch('water.json'),   0.0022, 1.2e-5)
lakes = poly_features(fetch('lakes.json'), 0.0030, 2.0e-4, want_names=True)

rivers=[]
for f in json.load(open(fetch('rivers.json')))['features']:
    g=f['geometry']; nm=(f['properties'].get('NAME') or '')
    major = any(m in nm for m in MAJOR)
    parts=[g['coordinates']] if g['type']=='LineString' else g['coordinates']
    for part in parts:
        for run in clip_line(part):
            s = rnd(rdp(run, 0.0030))
            if len(s) < (2 if major else 5): continue
            rec={'l':s}
            if major: rec['n']=nm; rec['m']=1
            rivers.append(rec)

cnt=lambda fs: sum(len(r) for f in fs for r in f['p'])
print(f'land   feats {len(land):4d} pts {cnt(land):6d}')
print(f'water  feats {len(water):4d} pts {cnt(water):6d}')
print(f'lakes  feats {len(lakes):4d} pts {cnt(lakes):6d}')
print(f'rivers runs  {len(rivers):4d} pts {sum(len(r["l"]) for r in rivers):6d}')

HEADER = """/* Map geometry for the Gulf Coast frame — built by stay/build-geo.py from
   US Census TIGERweb (USLandmass shoreline-clipped land; Hydro areal water
   and named lakes; Hydro linear named rivers), clipped to the search box and
   Douglas-Peucker simplified. Paint order matters: the frame fills with
   water, land paints on top, then bays and passes carve back out — TIGER
   coastal water stops at the 3-mile county limit, so the open Gulf can only
   come from the frame fill. Rings are grouped per feature and each paints as
   its own even-odd path, so islands survive as holes and neighbouring county
   polygons can never cancel each other into phantom land. Islands under
   roughly a square kilometre (Cabbage Key, Useppa) are below this source's
   resolution and are not drawn — their pins sit on the sound.
   Public domain (US Census Bureau). */
"""
geo = {'bbox':[W,S,E,N],'land':land,'water':water,'lakes':lakes,'rivers':rivers}
with open(OUT, 'w') as fh:
    fh.write(HEADER + 'window.STAY_GEO = ' + json.dumps(geo, separators=(',',':')) + ';\n')
print('wrote site/stay/js/geo.js —', round(os.path.getsize(OUT)/1024, 1), 'KB')
