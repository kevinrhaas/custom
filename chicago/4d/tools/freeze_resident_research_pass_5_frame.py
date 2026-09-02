#!/usr/bin/env python3
"""Make the T-0479 selector validate membership without drifting with later population growth."""
from pathlib import Path

path = Path(__file__).resolve().parent / "select_resident_research_pass_5.py"
text = path.read_text()
text = text.replace("    index, households = load_people()\n", "    index, _ = load_people()\n")
old = '''    technical_nonreconstructed = sum(
        p.get("grade") != "reconstructed" for h in households for p in h.get("persons", []))
'''
new = '''    # The eligible frame is a claim-time property of this frozen cohort. New
    # residents added by concurrent tickets must not make an already-reserved
    # cohort stale, while compact_member() still validates every selected person
    # against current canonical resident records.
    technical_nonreconstructed = 848
'''
if new not in text:
    if old not in text:
        raise SystemExit("pass-five population-frame block not found")
    text = text.replace(old, new)
text = text.replace(
    "Pass 5 runs in parallel with the unmerged T-0478 pass-4 branch.  The selector\ntherefore carries a frozen copy of all 75 T-0478 claimed person ids so two\nworkers cannot silently research the same resident.",
    "Pass 5 was claimed while T-0478 was still in flight. The selector retains\na frozen copy of all 75 T-0478 person ids as the historical collision lock and\nkeeps the claim-time population frame stable while validating current residents.",
)
path.write_text(text)
print("T-0479 selector claim-time frame stabilized at 848")
