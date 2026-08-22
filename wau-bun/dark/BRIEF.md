# The brief for the dark retelling

Wau-Bun (1856) is Juliette Kinzie's memoir of the Wisconsin/Illinois frontier.
It is in the public domain. This app already offers each scene three ways:
a summary, a light modernization, and her 1856 original.

This is a **fourth** reading of the same book: the identical events, told in a
modern horror-suspense voice. The book earns it — it contains a massacre, a
captivity, a starvation winter, a woman held under water to keep her out of a
fight, prisoners tunnelling out of a black-hole, a man asking cheerful
questions on his way to the gallows. The 1856 prose reports those things in a
drawing-room register. This mode restores the dread they actually carried.

## What you are writing

For each scene id you are given, read `wau-bun/source-scenes/<id>.txt`. Its
first two lines are a header: the scene's part, chapter and title, and the
paragraph and word count you are writing against. Everything after the blank
line is the passage.

Write your version to `wau-bun/dark/<id>.txt`:

- Plain UTF-8 text. Paragraphs separated by one blank line. No markdown, no
  headings, no title, no commentary, no notes to the reader — prose only.
- **Match the paragraph count** of the source (± 1 is fine; a very long source
  paragraph may split in two if a beat genuinely lands there).
- **Match the length.** Aim for 100% of the source word count. Below 90% the
  build fails and the work comes back to you. Longer is fine, up to ~115%.

## Non-negotiable: everything in the source survives

This is a retelling, not an adaptation.

- Every event, in the same order. Every person, by the same name. Every place,
  date, number, distance and price. Every turn of the plot.
- **Dialogue stays dialogue and keeps its content.** If someone says a thing in
  the source, they say that thing in yours. You may modernize the phrasing of
  narration freely; do not change what a speaker actually said.
- **Invent nothing.** No supernatural element, no new character, no new
  incident, no motive the source does not support. If the source says a horse
  came back on its own, a horse came back on its own — there is nothing in the
  woods.
- Keep the historical record intact, including the parts that reflect badly on
  the settlers and the government. Juliette's own asides about how the Ho-Chunk
  and Sauk were treated are among the most important lines in the book — carry
  them over with their full force. Do not soften them and do not editorialize
  past them.
- The narration is first person (Juliette) wherever the source is first person,
  and third person wherever the source is third. Do not switch.

## How to write it (this is the part that goes wrong)

The commonest failure is to work down the source sentence by sentence, swapping
a word here and breaking a paragraph there. That produces the source again with
a fresh coat of paint. It is not a second reading of the book and it is not what
this mode is for.

Do it this way instead:

1. Read the source passage twice. Write yourself a scratch list of the beats:
   what happens, in order, plus every name, number, date, place and line of
   dialogue you must carry.
2. **Stop looking at the source.** Write the scene from your list, in your own
   sentences, as though you were writing it for the first time.
3. Then check back against the source once, to confirm nothing was dropped and
   no dialogue drifted. Fix omissions — do not re-import phrasing.

The build measures this. It strips the quoted dialogue (which is supposed to
match) and compares the remaining narration against the source's; if more than
10% of the source's eight-word runs survive verbatim in your version, the build
fails and names your scene. Aim to keep proper nouns and quoted speech and to
share almost nothing else.

## The voice

The target is contemporary popular horror-suspense. That is a set of craft
habits, not any particular author's book:

- Short declarative sentences under pressure. Let a one-line paragraph land.
- Concrete sensory detail over abstraction: what it smelled like, what the
  ground did underfoot, what the light was doing.
- Dread built out of ordinary things — a dog standing over something, a dish
  of food pulled close in the dark, a sail that will not fill.
- Close narration: what the narrator noticed, and what she noticed she was
  thinking, in the order she noticed it.
- Withhold and reveal. The source often front-loads its outcome; you may hold
  the turn until the end of the paragraph, as long as you do not change it.
- Restraint at the worst moments. The most violent material in this book does
  not need heightening; report it plainly and let it do its own work.
- Do not overreach for atmosphere in quiet, funny or domestic scenes — a good
  deal of this book is comic, and comedy in a taut voice stays comic. Match the
  scene, not a genre template.

**Write original prose.** Do not quote, paraphrase, or imitate any passage from
any modern novel, and do not name any author anywhere in your output. The style
is a craft target you are hitting in your own words.

## Repo rules

- Write ONLY to `wau-bun/dark/<id>.txt`. Change nothing else — no app files,
  no data files, no README, no git commands.
- No model identifiers anywhere in what you write.
- If a source file is missing or empty, skip that id and say so in your report.

Report back: the ids you wrote, and for each, your word count against the
source's.
