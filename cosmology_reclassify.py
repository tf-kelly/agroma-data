#!/usr/bin/env python3
"""
cosmology_reclassify.py — flip 18 mistagged cosmology records to 'loose',
and drop the cosmology tag from 1 record where it's incidental.

Usage:
  cd ~/Documents/agroma-data
  python3 cosmology_reclassify.py

Then commit and push:
  git add app_data_v3.json
  git commit -m "Reclassify mistagged cosmology records (Pre-Socratic doxography, metaphysics)"
  git push
"""
import json
from pathlib import Path

PATH = Path("app_data_v3.json")

# Pre-Socratic doxography (Senecan NQ), Senecan Epistulae metaphysics (causes,
# being), Apuleius psychology, rhetorical denials of infinity. None contain
# mathematical-cosmological content.
RECLASSIFY = [
    "phi1212:phi001:27",          # Apuleius — Pre-Socratic name-list
    "phi1212:phi001:51",          # Apuleius — psychology continuation
    "phi1014:phi003:1.1-3",       # Seneca Mai. — rhetorical "nihil infinitum"
    "phi1017:phi015:6.9-22",      # Seneca Ep. 58 — Plato's six classes (metaphysics)
    "phi1017:phi015:7.4",         # Seneca Ep. 65.4 — Aristotle's four causes
    "phi1017:phi015:7.7-11",      # Seneca Ep. 65.7-11 — Plato's five causes
    "phi1017:phi017:3.13.1",      # Seneca NQ — Thales on water
    "phi1017:phi017:3.14.1-2",    # Seneca NQ — Egyptian elements
    "phi1017:phi017:3.29.1-3",    # Seneca NQ — Berosos's cosmogony
    "phi1017:phi017:4.2.17",      # Seneca NQ — Anaxagoras on Nile
    "phi1017:phi017:4.2.22",      # Seneca NQ — Thales on etesian winds
    "phi1017:phi017:4.3.6",       # Seneca NQ — Anaxagoras on hail
    "phi1017:phi017:5.13.1",      # Seneca NQ — whirlpool physics
    "phi1017:phi017:6.6.1",       # Seneca NQ — Thales's water-earth
    "phi1017:phi017:6.9.1",       # Seneca NQ — Anaxagoras on earthquakes
    "phi1017:phi017:6.13.1",      # Seneca NQ — Aristotle/Theophrastus earthquakes
    "phi1017:phi017:6.21.2",      # Seneca NQ — Posidonius's earthquake taxonomy
    "phi1017:phi017:7.1.6-7",     # Seneca NQ — stars as concretions
]

# Cosmology tag is incidental — Myth-of-Er reference is narrative, not mathematical.
RETAG = [
    "phi1038:phi001:1.8e.1",      # V.M. — Myth of Er narrative reference
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
        if "cosmology" in (r.get("topics") or []):
            r["topics"].remove("cosmology")
            n_retag += 1

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1))

    strict = sum(1 for r in data["records"] if r["strictness"] in ("strict", "quant-astro"))
    print(f"Reclassified to 'loose': {n_reclass}")
    print(f"Retagged (dropped cosmology): {n_retag}")
    print(f"Strict corpus now: {strict} records")


if __name__ == "__main__":
    main()
