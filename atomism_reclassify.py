#!/usr/bin/env python3
"""
atomism_reclassify.py — flip 14 mistagged atomism records to 'loose' strictness,
and drop the atomism tag from 8 records where it's incidental.

Usage:
  cd ~/Documents/agroma-data
  python3 atomism_reclassify.py

Then commit and push:
  git add app_data_v3.json
  git commit -m "Reclassify mistagged atomism records (Senecan polemic, doxography, Pre-Socratics)"
  git push
"""
import json
from pathlib import Path

PATH = Path("app_data_v3.json")

# Pre-Socratic doxography, Senecan polemic against atomism, atomist physics
# without mathematical content. None contain mathematical-atomism material.
RECLASSIFY = [
    "phi1254:phi001:5.15.8",      # Gellius — voice as flux of atoms (no quantification)
    "phi0550:phi001:4.298-317",   # Lucretius — mirror inversion (thin, both atomism & optics)
    "phi1017:phi017:2.6.2",       # Seneca NQ — polemic against atomist air theory
    "phi1017:phi017:2.7.1",       # Seneca NQ — atomic void in air (doxography)
    "phi1017:phi017:2.12.4",      # Seneca NQ — Aristotelian exhalations (mistagged as atomism)
    "phi1017:phi017:2.18.1",      # Seneca NQ — Anaximander on thunder (not atomism)
    "phi1017:phi017:2.19.1",      # Seneca NQ — Anaxagoras on thunder (not atomism)
    "phi1017:phi017:4.9.1",       # Seneca NQ — Democritus on heat (atomist physics, no math)
    "phi1017:phi017:4.10.1",      # Seneca NQ — atmospheric stratification
    "phi1017:phi017:5.1.2",       # Seneca NQ — dust-motes as atomist evidence
    "phi1017:phi017:5.2.1",       # Seneca NQ — Democritus on wind formation
    "phi1017:phi017:6.20.1",      # Seneca NQ — Democritus on earthquake causes
    "phi1017:phi017:6.20.5",      # Seneca NQ — Epicurean methodological pluralism
    "phi1017:phi017:7.13.2",      # Seneca NQ — atomist celestial outer-shell
]

# Atomism tag is incidental — these are about Plato, Pre-Socratics, geometry/astronomy
# more broadly, or Aristotelian theory. Keep the records (other tags carry real math
# content) but drop the atomism tag.
RETAG = [
    "phi1212:phi001:27",          # Apuleius Apol. 27 — Pre-Socratic name-list
    "phi0474:phi048:5.87",        # Cicero De Fin. 5.87 — Plato's travels
    "phi0474:phi037:1.217",       # Cicero De Or. 1.217 — geometry/music as philosophy
    "phi0474:phi049:5.64-66",     # Cicero Tusc. 5.64-66 — Archimedes' tomb (no atomism)
    "phi1254:phi001:5.15.7",      # Gellius NA 5.15.7 — Plato's percussion theory (NOT atomist)
    "phi0972:phi001:88",          # Petronius Sat. 88 — Eumolpus's Eudoxus tribute
    "phi1017:phi017:1.15.7-8",    # Seneca NQ 1.15.7-8 — mirror catalogue
    "phi0474:phi049:1.41",        # Cicero Tusc. 1.41 — numerus animus (atomism incidental)
]


def main():
    if not PATH.exists():
        raise SystemExit(f"Could not find {PATH}. Run from agroma-data directory.")

    data = json.loads(PATH.read_text())
    if "records" not in data:
        raise SystemExit("Bad JSON shape: no 'records' key.")

    by_id = {r["id"]: r for r in data["records"]}
    missing = [i for i in (RECLASSIFY + RETAG) if i not in by_id]
    if missing:
        raise SystemExit(f"Missing record IDs: {missing}")

    n_reclass, n_retag = 0, 0
    for rid in RECLASSIFY:
        r = by_id[rid]
        if r["strictness"] != "loose":
            r["strictness"] = "loose"
            n_reclass += 1
    for rid in RETAG:
        r = by_id[rid]
        if "atomism" in (r.get("topics") or []):
            r["topics"].remove("atomism")
            n_retag += 1

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1))

    strict = sum(1 for r in data["records"] if r["strictness"] in ("strict", "quant-astro"))
    print(f"Reclassified to 'loose': {n_reclass}")
    print(f"Retagged (dropped atomism): {n_retag}")
    print(f"Strict corpus now: {strict} records")


if __name__ == "__main__":
    main()
