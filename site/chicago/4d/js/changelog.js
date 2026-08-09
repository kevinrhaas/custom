export const CHANGELOG = [ // newest first
  { v: 3, title: 'The Sauganash stands at Lake and Market', kind: 'feature',
    ts: '2026-08-09T23:26:56.854Z', date: 'Aug 9, 2026, 6:26 PM CT',
    items: [
      'The georeference now places buildings. The Sauganash moved off the datum origin — which is in the middle of the river — to its surveyed corner at Lake and Market, about a hundred metres east of the forks.',
      'Placement method is recorded on the record itself: modern street successors, the platted eighty-foot street width, and the georeference\'s twenty-metre uncertainty carried forward rather than hidden.',
      'Fixed a convention bug where the archetype built its facade facing south while the contract defines a bearing of zero as facing north. The first rotated building would have faced backwards.',
    ] },
  { v: 2, title: 'Controls, and three fixes found by looking', kind: 'fix',
    ts: '2026-08-09T23:11:09.000Z', date: 'Aug 9, 2026, 6:11 PM CT',
    items: [
      'The building rendered pure black on real GPUs. The confidence shader touched its channel even when switched off, and a NaN multiplied by zero is still a NaN.',
      'A well-documented building was drawn as guesswork: two attributes were tagged conjectural while their own notes gave typological reasoning, and an unknown size was dithering the whole massing. Size and character are different kinds of not-knowing.',
      'The sky-derived environment map was overriding albedo, so every surface converged on the sky colour whatever it was made of. A documented white wall now reads white.',
      'Added a real controls panel — key map, walking speed, field of view, render quality and jump-to viewpoints. Run already existed on Shift and there was no way to discover it.',
    ] },
  { v: 1, title: 'Milestone 0 — one building, end to end', kind: 'feature',
    ts: '2026-08-09T22:16:34.000Z', date: 'Aug 9, 2026, 5:16 PM CT',
    items: [
      'A walkable reconstruction of the Sauganash Hotel as it stood in summer 1835, generated from a provenance-tracked record rather than modelled by hand.',
      'The confidence view: documented geometry renders solid, inferred is tinted, and anything we are guessing at becomes dithered massing. The tint and the citation come from the same record.',
      'The datum is verified — the forks at Wolf Point, derived from the 1834 Wright survey against modern control and re-derived from its own traces on every commit.',
    ] },
];

export const LATEST_VERSION = CHANGELOG[0].v;
