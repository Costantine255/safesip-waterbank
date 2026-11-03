# Methodology

## How the data is collected

Each SafeSip WaterBank hub is a solar-powered (12V) drinking-water kiosk drawing
from a borehole source. Water passes through reverse-osmosis treatment to reduce
salinity, then is dispensed to the community.

Onboard IoT sensors log, at 15-minute intervals:

- litres dispensed
- hub operational state (pumping, idle, fault)
- solar generation and battery state
- treated-water TDS and pH

Readings are buffered on the hub controller and uploaded when connectivity allows.
Manual field test kits provide weekly turbidity and pH cross-checks.

## From sensors to open data

1. **Collection** - raw 15-minute readings per hub.
2. **Anonymization** (`scripts/anonymize.py`) - hub serials replaced with
   pseudonyms, coordinates rounded to 0.1 degrees, any personal fields dropped.
   Hubs never log per-user identity; volumes are aggregate.
3. **Aggregation** (`scripts/aggregate_daily.py`) - readings rolled up to one row
   per hub per day: litres dispensed, estimated unique users, uptime percentage,
   solar generation.
4. **Publication** - datasets released here under CC-BY-4.0.

## What is not published

- Exact hub GPS coordinates (rounded before publication)
- The AI demand-prediction model, which is proprietary (patent filed in Tanzania)
- Any personal data: none is collected at the hubs

## Data quality

- Missing days in the consumption series indicate hub downtime or telemetry gaps,
  not zero consumption.
- `unique_users_est` is an estimate derived from dispensing sessions, not a
  headcount.
- Sensor quality readings are cross-checked with manual field tests weekly.
