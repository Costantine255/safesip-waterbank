# Data

## Datasets

### hub_daily_consumption.csv

One row per hub per day. Core demand dataset.

- `hub_id` - anonymized hub identifier (e.g. HUB-01)
- `date` - ISO date (YYYY-MM-DD)
- `region` - region name (e.g. Morogoro)
- `litres_dispensed` - litres dispensed that day
- `unique_users_est` - estimated unique users that day
- `uptime_pct` - hub uptime percentage that day
- `solar_kwh` - solar energy generated (kWh)

### water_quality_readings.csv

One row per hub per week. Quality spot-checks from hub sensors and manual tests.

- `hub_id` - anonymized hub identifier
- `week_start` - ISO date of week start
- `tds_ppm` - total dissolved solids after treatment (ppm)
- `ph` - pH reading
- `turbidity_ntu` - turbidity (NTU)
- `test_type` - sensor or manual

Full column definitions: see `data_dictionary.md`.

## Anonymization

Hub identifiers are pseudonymized. No personal data is collected or published:
hubs log aggregate dispensing volumes, not per-user records. GPS coordinates are
rounded to 0.1 degrees (about 11 km) before publication. See `scripts/anonymize.py`
and `docs/methodology.md`.

## Sample data

`data/sample/` contains small synthetic files that document the schema. They are
not real hub readings. Production files are populated from hub telemetry by the
SafeSip team.

## License

CC-BY-4.0 (see `LICENSE-DATA.md`). You may use, share, and adapt the data with
attribution to SafeSip.
