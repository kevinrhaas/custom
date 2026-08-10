# Band profiling spec — Uptown Porchfest 2026 Schedule Planner

You are enriching bands playing Uptown Porchfest (Minneapolis, Lowry Hill East).
For EACH band in your batch file, research the web and produce ONE JSON object.

## Research
Use WebSearch + WebFetch. Good sources: the band's own links (already supplied in
the batch file — Bandcamp, Spotify, Instagram, website), Bandcamp genre tags,
local press (City Pages / Racket / Star Tribune / Minnesota Playlist / The Current /
KFAI / Reviler / Cities97), Songkick/Bandsintown, Last.fm.

Budget roughly 2-4 searches/fetches per band. These are small local acts — many
will have thin footprints. That is EXPECTED and fine: when the web is thin, base
your ratings on the supplied `genre` + `bio` and set `confidence` accordingly.
NEVER invent facts, band members, releases, or press quotes. An honest thin
profile beats a fabricated rich one.

## Output: one object per band, ALL fields required

```json
{
  "band_name": "<EXACT string from the batch file — do not reformat>",
  "one_liner": "<=90 chars, punchy, concrete. No 'this band is'.",
  "profile": "2-4 sentences. What they actually sound like live, who they are, notable releases/press IF REAL.",
  "sounds_like": ["1-3 comparable well-known artists"],
  "genre_tags": ["2-5 tags from the CONTROLLED VOCAB below, most important first"],
  "dims": {
    "energy":       1-5,
    "loudness":     1-5,
    "tempo":        1-5,
    "electronic":   1-5,
    "vocal_forward":1-5,
    "danceability": 1-5,
    "experimental": 1-5,
    "brightness":   1-5,
    "grit":         1-5,
    "kid_friendly": 1-5
  },
  "confidence": "high" | "medium" | "low",
  "sources": ["urls you actually opened/used"]
}
```

## CONTROLLED VOCAB for `genre_tags` — use these exact strings, nothing else
rock, indie, alternative, punk, hardcore, metal, emo, garage, psychedelic,
shoegaze, folk, americana, country, bluegrass, blues, jazz, funk, soul, rnb,
hiphop, pop, electronic, ambient, experimental, noise, world, classical,
reggae, latin, brass, singer-songwriter, jam, cover-band

## Dimension rubric — anchor to these, be decisive, USE THE FULL 1-5 RANGE
A festival-goer filters on these, so a dataset where everything is a 3 is useless.

- **energy** — 1 ambient/background · 3 steady head-nod · 5 frantic, moshy, sweaty
- **loudness** — 1 unamplified acoustic · 3 normal full-band · 5 wall-of-amps heavy
- **tempo** — 1 ballads/drone · 3 mid-tempo · 5 fast/thrashy
- **electronic** — 1 all-acoustic instruments · 3 electric guitars/bass/drums · 5 synths, samples, programmed beats, DJ
- **vocal_forward** — 1 fully instrumental · 3 vocals as one element · 5 lyrics are the point (hip-hop, singer-songwriter, spoken word)
- **danceability** — 1 sit and listen · 3 tap your foot · 5 the street becomes a dance floor
- **experimental** — 1 familiar/traditional forms · 3 a fresh twist · 5 avant-garde, noise, odd meters, outsider
- **brightness** — 1 dark, heavy, mournful, goth · 3 bittersweet/neutral · 5 sunny, joyful, celebratory
- **grit** — 1 polished and clean · 3 live-band natural · 5 raw, lo-fi, distorted, abrasive
- **kid_friendly** — 1 loud and/or explicit, not for kids · 3 fine but loud · 5 delightful for a family with a stroller

Genre implies a lot: hardcore/metal → high energy+loudness+grit, low brightness,
low kid_friendly. Steel drum / jugband / bluegrass → high brightness+kid_friendly,
low loudness. Ambient/classical → low energy+danceability, high kid_friendly.
Hip-hop → high vocal_forward+danceability, high electronic.

## Deliverable
Write a JSON ARRAY of your batch's objects to:
`/tmp/claude-0/-home-user/a3c98d7b-7fd4-56f3-add3-517e9465c372/scratchpad/profiles_batchN.json`
(N = your batch number). Validate it parses with `node -e "JSON.parse(require('fs').readFileSync('<file>'))"`.

EVERY band in your batch file must appear exactly once. Your final message should
be just: `batchN: <count> profiles written` plus one line noting any band you
found essentially nothing on.
