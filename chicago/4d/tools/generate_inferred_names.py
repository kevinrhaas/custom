#!/usr/bin/env python3
"""Give the reconstructed residents names, and say plainly that we made them up.

    python3 tools/generate_inferred_names.py           write
    python3 tools/generate_inferred_names.py --check   re-derive and diff

WHY THIS EXISTS, given that the records argued the opposite until now.

Every reconstructed person used to carry a designation — "A baker (inferred
resident, unnamed)" — and the note explained the choice: an invented surname
would make the record indistinguishable at a glance from the documented layer
beside it. That reasoning is sound about the DATA and wrong about the TOWN. A
place where a third of the households are called "an inferred cooper's
household" does not read as a reconstruction with honest gaps; it reads as a
spreadsheet. The owner asked for names, and the record says loudly enough which
layer it belongs to that a name cannot smuggle anything past a reader: the chip
says reconstructed, the note says HYPOTHESISED AND NOT A PERSON, and now a
`name_basis` block says the name itself was invented and what pool it came from.

WHAT KEEPS IT HONEST.

  1. The pools are bounded by evidence this project already holds. They are
     seeded from the 76 ATTESTED residents in data/residents/ — real people,
     named from cited sources — so an invented cooper is named the way this
     town's real coopers were named. See data/reconstruction/
     1835_invented_name_pools.json for the seeds and their citations.

  2. Assignment is DETERMINISTIC, from a hash of the person's id. Re-running
     produces the same town, `--check` proves the committed data is what this
     script derives, and nobody has to wonder whether a name drifted.

  3. The grade never moves. A person graded `reconstructed` keeps that grade,
     and `name_basis.confidence` is `reconstructed` too. validate.py refuses an
     invented name that claims anything better — which is the rule that stops
     this from becoming a way to launder inventions into the documented layer.

  4. Where the trade-to-community weighting is itself a guess, the note says so.
     Boatmen draw French colonial on evidence; labourers draw evenly BECAUSE the
     Irish labouring Chicago of popular memory arrives with the canal contracts
     of 1836, after this scene, and weighting them Irish would be importing a
     later decade into this one.
"""
import argparse
import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOUSEHOLDS = ROOT / "data" / "residents" / "households"
POOLS = ROOT / "data" / "reconstruction" / "1835_invented_name_pools.json"
INDEX = ROOT / "data" / "residents" / "index.json"

# Trades this dataset records as held by a woman. Everything else draws male,
# mirroring the documented layer of household heads — and that is a statement
# about who the SOURCES named, not about who worked. Women's labour in this town
# is largely unrecorded rather than absent, and the reconstructed layer must not
# paper over a silence in the evidence by inventing against it.
FEMALE_TRADES = {"laundress", "domestic"}


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dumps(doc, indent=1):
    return json.dumps(doc, indent=indent, ensure_ascii=False) + "\n"


def pick(seq, key, salt):
    """A stable choice from a list, keyed by the person's own id."""
    h = hashlib.sha256(f"{key}:{salt}".encode()).digest()
    return seq[int.from_bytes(h[:4], "big") % len(seq)]


def community_for(pools, occupation, pid):
    rule = pools["trade_weights"].get(occupation) or pools["trade_weights"]["_default"]
    bag = []
    for cid, weight in rule["weights"].items():
        bag.extend([cid] * weight)
    bag.sort()
    return pick(bag, pid, "community"), rule


def overlay(files: dict) -> dict:
    """Apply the naming pass to an in-memory {path: text} map and hand it back.

    The household programme calls this so its drift check compares against the
    END of the pipeline rather than its own midpoint. Without it, every household
    reads as drifted the moment names exist, and a report that always cries wolf
    is not a report.
    """
    out = dict(files)
    named_files, _ = build(preload={p: json.loads(t) for p, t in files.items()
                                    if p.name.startswith("hh_")})
    out.update(named_files)
    return out


def build(preload: dict | None = None):
    pools = load(POOLS)
    by_id = {c["id"]: c for c in pools["communities"]}
    files = {}
    named = 0

    # TWO PASSES, because independent draws collide badly at this scale.
    #
    # Drawing each surname from a hash alone put four unrelated households under
    # "Lyman" and four more under "Gilbert" out of 92 people. That is not just
    # untidy: a shared surname reads as kinship, and this layer claims no
    # relationship whatever between its households. So the community is chosen
    # per person (pass one), and then each community's names are DEALT round its
    # pool in a stable hash order (pass two), which spreads them as evenly as the
    # pool allows and repeats only when a pool genuinely runs out.
    people = []
    sources = preload if preload is not None else {
        path: load(path) for path in sorted(HOUSEHOLDS.glob("*.json"))}
    for path in sorted(sources):
        doc = sources[path]
        for person in doc.get("persons", []):
            if person.get("grade") != "reconstructed":
                continue
            occ = (person.get("occupation") or {}).get("value") or ""
            cid, rule = community_for(pools, occ, person["id"])
            female = person.get("sex") == "female" or occ in FEMALE_TRADES
            people.append({"path": path, "doc": doc, "person": person, "cid": cid,
                           "rule": rule, "female": female, "occ": occ})

    # Deal within each (community, sex) bucket, ordered by a hash of the id so the
    # order is stable across runs and independent of filename or iteration order.
    buckets = {}
    for rec in people:
        buckets.setdefault((rec["cid"], rec["female"]), []).append(rec)
    for (cid, female), bucket in buckets.items():
        bucket.sort(key=lambda r: hashlib.sha256(r["person"]["id"].encode()).hexdigest())
        community = by_id[cid]
        givens = community["given_female" if female else "given_male"]
        surnames = community["surnames"]
        for i, rec in enumerate(bucket):
            rec["given"] = givens[i % len(givens)]
            rec["surname"] = surnames[i % len(surnames)]

    docs = {}
    for rec in people:
        path, doc, person = rec["path"], rec["doc"], rec["person"]
        docs[path] = doc
        community = by_id[rec["cid"]]
        rule = rec["rule"]
        female = rec["female"]
        given, surname = rec["given"], rec["surname"]
        person["name"] = f"{given} {surname}"
        if female and not person.get("sex"):
            person["sex"] = "female"

        weighting = (
            f"The draw was weighted toward this community ON EVIDENCE: {rule['why']}"
            if rule["basis"] == "evidenced" else
            f"The community was drawn WITHOUT a weighting that any source supports. "
            f"{rule['why']}"
        )
        person["name_basis"] = {
            "value": f"invented from the {community['label']} pool",
            "confidence": "reconstructed",
            "sources": list(community["sources"]),
            "note": (
                "THE NAME IS INVENTED. No source names this resident, and this field is "
                "not a finding about anybody — it is a label so that a reconstructed "
                "household reads as a household rather than as a row in a table. "
                f"It was drawn from the {community['label']} pool in "
                "data/reconstruction/1835_invented_name_pools.json, which is seeded from "
                "the names of the 76 ATTESTED residents this project holds — real people, "
                "named from cited sources — so that an invented resident is named the way "
                "this town's documented residents were actually named rather than the way "
                "a story would name one. " + weighting + " The evidence for the pool "
                "itself: " + community["evidence"]
            ),
        }
        named += 1

    for path, doc in docs.items():
        # The household's own label follows its head. "An inferred baker's
        # household (south division)" is what the layer is FOR, and it is also
        # unreadable as a place where someone lived; "The Kellogg household — an
        # inferred baker (south division)" says both at once.
        head = next((p for p in doc.get("persons", [])
                     if p.get("relationship") == "head"), None)
        if head and head.get("name"):
            trade = ((head.get("occupation") or {}).get("value") or "").replace("_", " ")
            doc["name"] = (f"The {head['name'].split()[-1]} household — an inferred "
                           f"{trade} ({doc.get('division', '')} division)")
        files[path] = dumps(doc)
    return files, named


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="re-derive and report any drift without writing")
    args = ap.parse_args()

    files, named = build()
    if args.check:
        drift = [p for p, text in files.items() if p.read_text(encoding="utf-8") != text]
        for p in drift:
            print(f"   DRIFT: {p.relative_to(ROOT)}")
        if drift:
            print(f"   {len(drift)} household(s) differ from what this script derives")
            return 1
        print(f"   OK: {named} invented name(s) match what tools/generate_inferred_names.py derives")
        return 0

    for p, text in files.items():
        p.write_text(text, encoding="utf-8")

    # The manifest is deliberately NOT touched. Its `head` field carries the
    # person's ID, not their name — validate.py checks the two against each
    # other and the record is authoritative. Writing names into it replaced
    # 152 ids with display strings and failed the manifest against every
    # household in the dataset, attested ones included.

    print(f"named {named} reconstructed resident(s) across {len(files)} household(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
