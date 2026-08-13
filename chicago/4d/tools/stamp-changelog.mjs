// stamp-changelog.mjs — stamp ship time onto the newest changelog entry and
// regenerate every entry's human `date` from its `ts`.
//
// The self-improvement loop prepends a new CHANGELOG entry with an EMPTY `ts`
// (`ts: ''`). This script fills that first empty `ts` with the real deploy time
// so dates reflect when a change actually shipped and can't be fabricated. It
// then rewrites every `date:` to a Central Time alias derived from that entry's
// `ts`, keeping the fleet-standard shape ({v, title, ts, date, items}).
//
// Run before merging whenever renderers/web/js/changelog.js changed. Nothing
// stamps later in the pipeline — tools/publish.sh only copies the file to the
// public URL the fleet parses, it never edits it.
import { readFile, writeFile } from 'node:fs/promises';

const FILE = new URL('../renderers/web/js/changelog.js', import.meta.url);
const nowIso = new Date().toISOString();

function ctAlias(iso){
  const d = new Date(iso);
  if(isNaN(d)) return '';
  return d.toLocaleString('en-US',{ timeZone:'America/Chicago', month:'short',
    day:'numeric', year:'numeric', hour:'numeric', minute:'2-digit' }) + ' CT';
}

let src = await readFile(FILE, 'utf8');

// 1) Fill the first empty ts (newest entry sits at the top of the array).
let stamped = false;
src = src.replace(/ts:\s*(['"])\1/g, () => { stamped = true; return `ts: '${nowIso}'`; });

// 2) Regenerate every `date:` from the ts on the same entry. We walk entries by
//    matching each `ts: '<iso>'` and rewriting the `date: '...'` that follows it.
//
//    An entry written the way the contract describes it — `ts: ''`, no date, let
//    the stamper do the rest — has no `date:` to rewrite, so this used to skip it
//    and hand back a file the contract check then rejected for a missing date.
//    An author following the documented rule got a failure and no hint which
//    half of the rule was wrong, so the key is created when it is absent.
src = src.replace(/ts:\s*'([^']*)'(\s*,\s*)date:\s*'[^']*'/g,
  (_, iso, sep) => `ts: '${iso}'${sep}date: '${ctAlias(iso)}'`);
src = src.replace(/ts:\s*'([^']*)'(?!\s*,\s*date:)/g,
  (_, iso) => `ts: '${iso}', date: '${ctAlias(iso)}'`);


// ---- version assignment (fleet contract, 2026-08-10) ----------------------
// Authors write `v: null`; the number is assigned HERE, after any merge, where
// the real answer is knowable. Two branches that each prepend an entry both
// compute the same "top + 1", and whichever merges second is silently wrong.
// See polecat-platform docs/SHELL-API.md, and the `merge=union` half of the fix
// in .gitattributes — deriving the number alone does not stop the conflict.
//
// Numbered by POSITION, top being newest, because this tool patches text rather
// than parsing entries: re-serialising the file to sort by ts would reformat
// entries it did not author. Entries that already have a version are never
// touched — Manager keys release rows on `v` and every reader's "seen" marker
// compares against it, so renumbering history would re-notify everyone.
{
  const nulls = [...src.matchAll(/v:\s*null/g)];
  if (nulls.length) {
    const firstNumbered = src.match(/v:\s*(\d+)/);
    const base = firstNumbered ? Number(firstNumbered[1]) : 0;
    for (let i = nulls.length - 1, n = base; i >= 0; i--) {
      const m = nulls[i];
      src = src.slice(0, m.index) + `v: ${++n}` + src.slice(m.index + m[0].length);
    }
    console.log(`Assigned ${nulls.length} changelog version(s) from v${base}.`);
  }
  // A stamper that emits a duplicate version is worse than one that stops: the
  // duplicate ships and the contract check only catches it later, if at all.
  const vs = [...src.matchAll(/v:\s*(\d+)/g)].map((m) => Number(m[1]));
  for (let i = 1; i < vs.length; i++) {
    if (vs[i - 1] <= vs[i]) {
      console.error(`changelog: versions not strictly decreasing (v${vs[i - 1]} then `
        + `v${vs[i]}) — refusing to write.`);
      process.exit(1);
    }
  }
}

await writeFile(FILE, src);
console.log(stamped ? `Stamped newest changelog entry: ${nowIso}` : 'No empty changelog timestamp to stamp; dates refreshed.');
