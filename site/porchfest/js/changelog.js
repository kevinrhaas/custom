export const CHANGELOG = [ // newest first
  { v: 2, title: 'Route by the big names, or dig for hidden gems', kind: 'feature',
    ts: '2026-08-10T00:42:09.856Z', date: 'Aug 9, 2026, 7:42 PM CT',
    items: [
      'A Big names dial sits above the ten taste dimensions. Slide it up and the route favours the acts with the biggest footprint; slide it down for hidden gems and spend the afternoon on bands nobody has heard yet. One-tap presets for both.',
      'Every band now carries a draw score from zero to one hundred. There is no attendance or streaming data for a porchfest, so this is an evidence score rather than a measurement: rooms played, who they opened for, releases, press and how much the research could actually verify.',
      'The sixteen most notable acts are badged in the band browser, each showing the evidence that earned it, and a new sort puts the biggest names first. Nothing is labelled negatively, because a band with no badge is very often the best set of the day.',
      'Draw rides in as an eleventh axis on the same scale as taste, so asking for big names trades off against what you actually like rather than overriding it.',
      'Scoring defends against the ways a keyword sweep misreads a bio. A negation cue voids a match, so rather than a road-hardened touring act is not a touring credit. Low-confidence profiles are discounted, so a profile that rests on its own festival bio cannot score as a festival booking. Patterns are narrow, so the current lineup is not the radio station.',
      'Shared plans carry the new dial, and links shared before it existed still open exactly as they did.',
    ] },
  { v: 1, title: 'Route your way through 91 bands', kind: 'feature',
    ts: '2026-08-09T23:47:11.704Z', date: 'Aug 9, 2026, 6:47 PM CT',
    items: [
      'Uptown Porchfest puts 91 bands on 33 porches across six blocks of the Wedge, all overlapping. This works out where to stand and when, as an ordered schedule with the walking legs between stops.',
      'Every band is rated one to five on ten dimensions — energy, loudness, tempo, electronic, vocals, danceability, experimental, brightness, grit and kid-friendly — so you can ask for loud and fast, or quiet enough for a stroller, instead of reading 91 bios.',
      'Choosing a route is an orienteering problem with time windows: maximise taste-match subject to walking times, each set window, your finish time and an optional band count. Randomised greedy insertion plus a swap local search.',
      'It re-plans on every control change rather than behind a button. Input is debounced to the pause, then a fast pass gives immediate feedback and a thorough pass replaces the route only if it genuinely scored better.',
      'Band count is a hard ceiling and a soft floor, so exactly six or between three and five are obeyed when the clock allows, and produce the best short route plus a warning when it does not.',
      'Walking distances come from a pedestrian graph of the real street network baked into the page, with Dijkstra for both distance and the drawn path. Validated against an OSRM foot matrix at three percent median error.',
      'The map is hand-drawn SVG from that same street data, which is why the app needs no tiles, no CDN and no API. Once loaded it makes zero network requests, which matters on a saturated cell tower at a street festival.',
      'Map pins merge when they would overlap and split apart again as you zoom, so a route that returns to a porch never hides its own earlier stop.',
      'A plan packs into the URL, so sharing it needs no backend and no account. Schedule also exports to calendar, or opens as walking directions.',
    ] },
];

export const LATEST_VERSION = CHANGELOG[0].v;
