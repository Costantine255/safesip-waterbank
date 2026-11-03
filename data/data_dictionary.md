# Data dictionary

## hub_daily_consumption.csv

| Column | Type | Description |
|---|---|---|
| hub_id | string | Anonymized hub identifier, format HUB-NN |
| date | date | Calendar date, YYYY-MM-DD |
| region | string | Tanzanian region where the hub operates |
| litres_dispensed | float | Total litres dispensed that day |
| unique_users_est | integer | Estimated unique users, derived from dispensing sessions |
| uptime_pct | float | Percentage of the day the hub was operational (0-100) |
| solar_kwh | float | Solar energy generated that day (kWh) |

## water_quality_readings.csv

| Column | Type | Description |
|---|---|---|
| hub_id | string | Anonymized hub identifier, format HUB-NN |
| week_start | date | Monday of the measurement week, YYYY-MM-DD |
| tds_ppm | float | Total dissolved solids after reverse-osmosis treatment (ppm) |
| ph | float | pH of treated water |
| turbidity_ntu | float | Turbidity of treated water (NTU) |
| test_type | string | `sensor` (continuous hub sensor) or `manual` (field test kit) |

## Notes

- All hub identifiers are pseudonyms assigned at publication time; the mapping to
  physical hubs is held by SafeSip and never published.
- `unique_users_est` is an estimate: one dispensing session is counted as one user
  visit, capped at 3 sessions per estimated user per day.
- Missing days indicate hub downtime or telemetry gaps, not zero consumption.
