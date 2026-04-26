#!/usr/bin/env python3
"""
optics_reclassify.py — flip 16 mistagged optics records to 'loose' strictness,
and drop the optics tag from 3 records where it's incidental.

Usage:
  cd ~/Documents/agroma-data
  python3 optics_reclassify.py

Then commit and push:
  git add app_data_v3.json
  git commit -m "Reclassify mistagged optics records (theory-of-vision, descriptive)"
  git push
"""
import json
from pathlib import Path

PATH = Path("app_data_v3.json")

# These are theory of vision, atomist eidola, colour theory, or descriptive
# observation. None contain mathematical optics. Flipped to 'loose' so they
# disappear from the strict public view but are preserved in the data.
RECLASSIFY = [
    "phi1254:phi001:5.16.3",      # Gellius — Epicurean simulacra (theory of vision)
    "phi1254:phi001:5.16.4",      # Gellius — Plato emission theory (theory of vision)
    "phi0550:phi001:4.164-230",   # Lucretius — atomist simulacra
    "phi1017:phi017:1.2.1",       # Seneca NQ — Augustus halo anecdote
    "phi1017:phi017:1.2.2-4",     # Seneca NQ — Greek halo terminology
    "phi1017:phi017:1.3.5-6",     # Seneca NQ — basins/droplets observation
    "phi1017:phi017:1.3.7-8",     # Seneca NQ — water optical medium
    "phi1017:phi017:1.3.10-13",   # Seneca NQ — rainbow colour theory
    "phi1017:phi017:1.4.1-2",     # Seneca NQ — rainbow speed
    "phi1017:phi017:1.5.1-4",     # Seneca NQ — clouds-as-mirrors empirical
    "phi1017:phi017:1.5.5-9",     # Seneca NQ — water-droplet rainbow
    "phi1017:phi017:1.6.5",       # Seneca NQ — water-globe magnification observation
    "phi1017:phi017:1.7.2",       # Seneca NQ — sun-rods false colour
    "phi1017:phi017:1.11.2",      # Seneca NQ — parhelia Greek terminology
    "phi1017:phi017:1.13.1-2",    # Seneca NQ — parhelia cloud properties
    "phi1017:phi017:2.55.4",      # Seneca NQ — Clidemus on lightning
]

# Optics tag is incidental — these are about astronomy or meteorology.
# Drop optics, keep other tags.
RETAG = [
    "phi1017:phi017:1.12.1",      # Seneca NQ — eclipse observation by bowls (astronomy)
    "phi1017:phi017:1.17.3",      # Seneca NQ — conjunction observation (astronomy)
    "phi1017:phi017:4.3.3-5",     # Seneca NQ — hail rounding (meteorology, not optics)
]


def main():
    if not PATH.exists():
        raise SystemExit(f"Could not find {PATH}. Run this script from the agroma-data directory.")

    data = json.loads(PATH.read_text())
    if "records" not in data:
        raise SystemExit("Bad JSON shape: no 'records' key.")

    by_id = {r["id"]: r for r in data["records"]}
    missing = [i for i in (RECLASSIFY + RETAG) if i not in by_id]
    if missing:
        raise SystemExit(f"Missing record IDs: {missing}")

    n_reclass = 0
    n_retag = 0
    for rid in RECLASSIFY:
        r = by_id[rid]
        if r["strictness"] != "loose":
            r["strictness"] = "loose"
            n_reclass += 1
    for rid in RETAG:
        r = by_id[rid]
        if "optics" in (r.get("topics") or []):
            r["topics"].remove("optics")
            n_retag += 1

    PATH.write_text(json.dumps(data, ensure_ascii=False, indent=1))

    strict = sum(1 for r in data["records"] if r["strictness"] in ("strict", "quant-astro"))
    print(f"Reclassified to 'loose': {n_reclass}")
    print(f"Retagged (dropped optics): {n_retag}")
    print(f"Strict corpus now: {strict} records")


if __name__ == "__main__":
    main()
