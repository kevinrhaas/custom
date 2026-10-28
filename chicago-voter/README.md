# Chicago Voter — Ballot Match

A short, adaptive scenario survey that fills in every race on one Chicago ballot,
**Tuesday, November 3, 2026 · Ward 30 · Precinct 04 · ballot style 124**
(3rd Congressional, 2nd Legislative, 3rd Representative, 8th County Board,
Board of Review 2nd, Board of Education Subdistrict 1B), and tells you why.

Live at `site/chicago-voter/` → `https://kevinrhaas.github.io/custom/chicago-voter/`.

## How it works

- **Axes.** Every candidate is scored −2…+2 on the survey axes that matter for their
  office (taxes & spending, public safety, immigration & Washington, rights & guns,
  experience vs. shake-up, property taxes, water & climate, schools). Each score
  carries a one-line evidence note from the cited research.
- **Questions** (`site/chicago-voter/js/questions.js`) are scenarios. Each one places
  you on one axis and comes in two or three variants (picked at random, and "ask it
  another way" swaps them), so no two runs read alike. A couple are oblique
  "mind-reader" variants in the spirit of AutoSelector's Mind Reader.
- **Adaptive order.** The next question is whichever could still move the most
  undecided races (axis weight × how far apart the candidates are × how close the
  race is × how unsure we are of you). The survey stops when no question could change
  the ballot, which is usually after 8 to 10 questions. A final lightning round asks
  directly about any public question your answers didn't settle.
- **Judges** follow one rule you pick: follow the big bar associations, a stricter
  line, retain all, or skip. You can override any single judge.
- **The live ballot.** The oval field (one oval per mark on the ballot) fills in as you
  answer, the four stars of the Chicago flag light up as each quarter of the ballot is
  decided, and each answer reports which races moved and why. Any race can be
  overridden by hand.

## Data and provenance

`research/*.json` is the cited research, gathered October 28, 2026 from candidate
sites, the Tribune, Sun-Times/WBEZ questionnaires, WTTW, Capitol News Illinois,
Chalkbeat, Block Club, Injustice Watch's 2026 judicial guide, the Chicago Bar
Association, the Chicago Council of Lawyers, the ISBA and the Alliance of Bar
Associations. Every candidate and judge record carries its source URLs, and the app
shows them.

`build.mjs` turns the research into `site/chicago-voter/js/data.js`. Run it with
`node chicago-voter/build.mjs`. It adds only editorial layout: the ballot order and
line numbers, which axes each office touches and how much, the judge flag tiers, and
plain-English readings of what a Yes vote on each public question means. All of it
is labeled in the file.

Judge flag tiers:

- **concern:** a major bar (CBA, Council of Lawyers, ISBA) rated them Not Recommended.
- **caution:** only an Alliance member bar said No, or Injustice Watch documents a
  notable controversy.
- **clean:** everyone else.

## Checks

```
node chicago-voter/build.mjs
node chicago-voter/smoke.mjs [--shots DIR]   # 390×780 and 1280×800, four answer patterns, zero page errors
```

This is a mirror of the user's own answers, not an endorsement.
