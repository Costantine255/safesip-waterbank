#!/usr/bin/env python3
"""Anonymize raw hub telemetry for open publication.

Reads raw per-hub telemetry and writes the publishable layer:
- hub identifiers replaced with pseudonyms (HUB-NN)
- GPS coordinates rounded to 0.1 degrees (~11 km)
- per-user records dropped; only aggregate volumes published

Usage:
    python anonymize.py raw_telemetry.csv anonymized.csv --mapping hub_map.json
"""

import argparse
import csv
import hashlib
import json
import sys


def pseudonym(hub_serial: str) -> str:
    digest = hashlib.sha256(hub_serial.encode()).hexdigest()
    return "HUB-%02d" % (int(digest[:4], 16) % 100)


def round_coord(value: str) -> str:
    try:
        return "%.1f" % round(float(value), 1)
    except (TypeError, ValueError):
        return ""


DROP_COLUMNS = {"user_id", "phone", "name", "exact_lat", "exact_lon"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Anonymize hub telemetry.")
    parser.add_argument("input", help="Raw telemetry CSV")
    parser.add_argument("output", help="Anonymized output CSV")
    parser.add_argument("--mapping", help="JSON file to store the pseudonym map")
    args = parser.parse_args()

    mapping = {}
    with open(args.input, newline="") as src:
        reader = csv.DictReader(src)
        kept = [c for c in reader.fieldnames if c not in DROP_COLUMNS]
        if "hub_serial" not in reader.fieldnames:
            sys.exit("error: input must contain a hub_serial column")
        rows = []
        for row in reader:
            serial = row["hub_serial"]
            if serial not in mapping:
                mapping[serial] = pseudonym(serial)
            out = {"hub_id": mapping[serial]}
            for col in kept:
                if col in ("lat", "lon"):
                    out[col] = round_coord(row[col])
                elif col != "hub_serial":
                    out[col] = row[col]
            rows.append(out)

    with open(args.output, "w", newline="") as dst:
        writer = csv.DictWriter(dst, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    if args.mapping:
        with open(args.mapping, "w") as fh:
            json.dump(mapping, fh, indent=2)

    print("wrote %d anonymized rows for %d hubs" % (len(rows), len(mapping)))


if __name__ == "__main__":
    main()
