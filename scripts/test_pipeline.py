"""Smoke tests for the anonymization and aggregation pipeline (stdlib only)."""

import csv
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, *args):
    return subprocess.run(
        [sys.executable, os.path.join(HERE, script), *args],
        capture_output=True, text=True,
    )


def test_anonymize_drops_pii_and_pseudonymizes():
    with tempfile.TemporaryDirectory() as tmp:
        raw = os.path.join(tmp, "raw.csv")
        out = os.path.join(tmp, "anon.csv")
        with open(raw, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["hub_serial", "timestamp", "user_id", "phone",
                        "lat", "lon", "litres_dispensed"])
            w.writerow(["SN-001", "2026-10-01T08:00:00", "u1",
                        "+255700000000", "-6.82349", "37.66123", "12.5"])
        r = run("anonymize.py", raw, out)
        assert r.returncode == 0, r.stderr
        with open(out) as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 1
        row = rows[0]
        assert row["hub_id"].startswith("HUB-")
        assert "SN-001" not in str(row.values())
        assert "user_id" not in row and "phone" not in row
        assert row["lat"] == "-6.8" and row["lon"] == "37.7"


def test_aggregate_daily_produces_one_row_per_hub_day():
    with tempfile.TemporaryDirectory() as tmp:
        anon = os.path.join(tmp, "anon.csv")
        out = os.path.join(tmp, "daily.csv")
        with open(anon, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["hub_id", "timestamp", "region", "litres_dispensed",
                        "up_minutes", "solar_kwh"])
            w.writerow(["HUB-01", "2026-10-01T08:00:00", "Morogoro", "10.0", "60", "4.1"])
            w.writerow(["HUB-01", "2026-10-01T08:15:00", "Morogoro", "12.0", "60", "4.1"])
            w.writerow(["HUB-01", "2026-10-02T08:00:00", "Morogoro", "9.0", "30", "3.9"])
        r = run("aggregate_daily.py", anon, out)
        assert r.returncode == 0, r.stderr
        with open(out) as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 2
        assert float(rows[0]["litres_dispensed"]) == 22.0
        assert rows[0]["date"] == "2026-10-01"


if __name__ == "__main__":
    test_anonymize_drops_pii_and_pseudonymizes()
    test_aggregate_daily_produces_one_row_per_hub_day()
    print("all pipeline tests passed")
