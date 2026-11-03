#!/usr/bin/env python3
"""Aggregate anonymized hub readings into the daily consumption dataset.

Reads anonymized per-reading telemetry and writes hub_daily_consumption.csv:
one row per hub per day with litres dispensed, estimated unique users,
uptime percentage, and solar generation.

Usage:
    python aggregate_daily.py anonymized.csv hub_daily_consumption.csv
"""

import argparse
import csv
from collections import defaultdict
from datetime import datetime


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate telemetry to daily rows.")
    parser.add_argument("input", help="Anonymized telemetry CSV")
    parser.add_argument("output", help="Daily consumption CSV")
    args = parser.parse_args()

    days = defaultdict(lambda: {
        "litres": 0.0, "sessions": 0, "up_minutes": 0,
        "solar_kwh": 0.0, "region": "",
    })

    with open(args.input, newline="") as src:
        for row in csv.DictReader(src):
            try:
                ts = datetime.fromisoformat(row["timestamp"])
            except (KeyError, ValueError):
                continue
            key = (row["hub_id"], ts.date().isoformat())
            cell = days[key]
            cell["litres"] += float(row.get("litres_dispensed", 0) or 0)
            cell["sessions"] += 1
            cell["up_minutes"] += int(float(row.get("up_minutes", 0) or 0))
            cell["solar_kwh"] = max(cell["solar_kwh"],
                                    float(row.get("solar_kwh", 0) or 0))
            cell["region"] = row.get("region", "")

    with open(args.output, "w", newline="") as dst:
        writer = csv.writer(dst)
        writer.writerow(["hub_id", "date", "region", "litres_dispensed",
                         "unique_users_est", "uptime_pct", "solar_kwh"])
        for (hub_id, date), cell in sorted(days.items()):
            users_est = min(cell["sessions"], cell["sessions"] // 3 + 1) \
                if cell["sessions"] else 0
            uptime = round(min(100.0, cell["up_minutes"] / 14.4), 1)
            writer.writerow([hub_id, date, cell["region"],
                             round(cell["litres"], 1), users_est,
                             uptime, round(cell["solar_kwh"], 2)])

    print("wrote %d daily rows" % len(days))


if __name__ == "__main__":
    main()
