# Wau-Bun — an interactive telling

Juliette Augusta Magill Kinzie's *Wau-Bun: The Early Day in the North-West*
(1856), rebuilt as something you can move around in: a chart of every
character against every scene, a scene-by-scene reader, the full cast, and a
plain table of the same data.

Live at `/custom/wau-bun/`. Static HTML + CSS + three data files and one app
file. No build step, no framework, no dependencies.

## The three parts

| Part | Title | Chapters | Status |
|------|-------|----------|--------|
| 1 | Journey West (1830 – March 1831) | I–XVII | **complete** — 49 scenes, 83 characters |
| 2 | The Early Frontier (c. 1770s–1816) | XVIII–XXIII | chapter outline |
| 3 | Wau Bun (1831–1833) | XXIV–XXXVIII | chapter outline |

## The data model

Everything is derived from two lists per scene, so nothing has to be kept in
sync by hand:

```js
{
  id: 's25', act: 'a3', chapter: 'VIII', chapterTitle: 'Fort Winnebago',
  title: 'The chiefs call on their new mother',
  date: 'After breakfast', place: 'Fort Winnebago', placeShort: 'Fort Winnebago',
  summary: '…',                 // what happens, in plain contemporary English
  points: ['…'],                // the pivotal turns, as bullets
  cast:     ['juliette','john'],// PRESENT in the scene  → solid mark
  offstage: ['fourlegs'],       // spoken of / acting at a distance → dashed mark
  pivotal: true                 // ★ in the chart, filterable
}
```

First appearance, last appearance, the arc line between them, scene counts,
the "enters" / "last seen" badges and the cast sparklines are all **computed**
in `js/app.js` (`buildIndex`) from `cast` / `offstage`. Add a character to a
scene and every view updates.

Characters live in `js/data-characters.js` with an `id`, `name`, optional
`alias`, a `faction` (one of four), a `role` and a `bio`.

## Adding Part 2 or Part 3

Fill in `acts` and `scenes` on `WAUBUN_PART2` / `WAUBUN_PART3` in
`js/data-parts23.js` using the same shape as `js/data-part1.js`, add any new
people to `js/data-characters.js`, and delete that part's `outline` array. The
app switches from the outline view to the four full views as soon as a part
has scenes.

## Colour

The four faction hues are the validated categorical palette (slots 1–4), and
faction blocks are ordered `kinzie → native → military → settler` so that only
validated *adjacent* colour pairs ever touch in the chart. Two of the light
steps sit below 3:1 against the surface, so colour never carries identity on
its own: every mark has a text label, the legend is always present, and the
Table view carries the whole dataset in text.

## Checks

```bash
# from the repo root
python3 -m http.server 8899 --directory site   # then open /wau-bun/
node --input-type=module --check < site/wau-bun/js/app.js
```

The repo's deploy workflow parses every `site/**/*.js` before publishing.
