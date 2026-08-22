# The brief for the Modern reading

*Wau-Bun* (1856) is Juliette Kinzie's memoir of the Wisconsin and Illinois
frontier. It is in the public domain (Project Gutenberg #12183). The app offers
each scene four ways, and this is the second of them:

| mode | what it is |
|------|------------|
| Summary | a short prose summary plus the plot points |
| **Modern** | **the whole passage in plain present-day English — this brief** |
| Retold | the same events in a tauter, more immediate voice (`wau-bun/dark/`) |
| 1856 | Kinzie's first-edition text, unaltered |

## What Modern is for

The app was built on a light modernization of the 1856 text: obsolete spellings
fixed, some punctuation updated, otherwise left alone. It still reads like 1856
— long periodic sentences, inversions, "it may be readily imagined that", a
comma every six words. A reader who wants Kinzie's own voice can pick the 1856
tab and get it exactly.

Modern is for the reader who wants to know what she *said*, in the English they
actually speak. Same paragraph, same order, same facts, same jokes, same
length. Just put plainly.

It is **not** a summary, **not** an abridgement, and **not** a rewrite in a new
voice — that is what the Retold reading is for. Think of it as a translation
between two forms of English. Twenty-one scenes already exist in this voice, in
`wau-bun/modern/s1.txt` through `s21.txt`; read two or three before you start.

## What you are writing

For each scene id you are given, read `wau-bun/source-scenes/<id>.txt`. Its
first two lines are a header giving the part, chapter, title, and the paragraph
and word count you are writing against. Everything after the blank line is the
passage.

Write your version to `wau-bun/modern/<id>.txt`:

- Plain UTF-8 text, paragraphs separated by one blank line. Prose only — no
  markdown, no heading, no title, no notes to the reader.
- **Match the paragraph count exactly.** Modern renders the passage paragraph
  for paragraph. (Only split a paragraph if the source itself is a run-on that
  is genuinely two; never merge.)
- **Match the length.** Aim for 100% of the source word count. Below 90% the
  build fails and names your scene. Up to ~115% is fine.

## The rules

- **Cut nothing.** Every event, person, place, date, number, distance, price,
  aside and joke survives. If the source spends a paragraph on how a short-cake
  was made, so do you.
- **Add nothing.** No invented image, sensation, weather or inferred feeling.
  You are re-expressing sentences, not enriching them.
- **Dialogue keeps its content.** You may modernize the wording *around* a
  speech freely; what a speaker actually says stays what they said.
- **Keep the person.** First person where Kinzie narrates, third where the
  passage is third (the Fort Dearborn chapters, the Lytle captivity), and
  quoted first-person testimony stays inside its quotation.
- **Keep the record.** Her judgements about how the Ho-Chunk, Sauk and
  Pottawatomi were treated are among the most important lines in the book. They
  carry over at full force, unsoftened and without editorial comment from you.
  Her period vocabulary is part of the historical record; leave it as she wrote
  it rather than substituting modern terms into her narration.
- **Keep the humour.** A great deal of this book is funny. A joke that only
  worked because of an 1856 construction should be rebuilt so it still lands.

## How to do it well

Work paragraph by paragraph with the source open — unlike the Retold reading,
closeness here is correct and expected. What you are changing is the *sentence
construction*, not the content:

- Break the long periodic sentences into ones a person would say out loud.
- Put the subject and verb near the front. Undo the inversions.
- Replace the dead formulae — "it may be readily imagined", "we were not
  suffered to remain", "such being the case" — with what they mean.
- Prefer the plain word: *dwelling* → house, *at length* → finally,
  *commenced* → began, *in consequence of* → because.
- Keep her asides and her dry tone. She is often being funny on purpose, and a
  flattened sentence loses the joke.
- Where the source has an obvious scanning artefact (a garbled verb, "Port
  Winnebago" for Fort Winnebago, a corrupted date like 1163 for 1763), render
  the plain sense. Do not propagate a transcription error, and do not invent a
  fact to paper over one — if it cannot be resolved, leave the passage as the
  source has it and say so in your report.

## Repo rules

- Write ONLY to `wau-bun/modern/<id>.txt`. Nothing else — no app files, no data
  files, no README, no git commands.
- No model identifiers anywhere in what you write, and no author names.
- If a source file is missing or empty, skip that id and say so.

Report the ids you wrote with your word and paragraph counts against the
source's.
