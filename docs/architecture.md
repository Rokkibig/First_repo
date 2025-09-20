# Assistant Architecture Overview

## Morning Preparation Workflow

The `assistant.morning` package encapsulates the orchestration logic for the
morning preparation workflow. The central `MorningPreparationService` class
coordinates the following steps:

1. **Collect Market Context** – gathers placeholder market snapshots from the
   configured data connectors (Alpha Vantage, Twelve Data, yfinance).
2. **Fetch Economic Events** – pulls upcoming events from the economic calendar
   client.
3. **Build Trading Scenarios** – aggregates scenario insights. Stubbed builders
   can be replaced with real analytics modules.
4. **Generate Briefing Report** – assembles a textual report for downstream
   distribution channels.

`create_default_service` wires the service with stub connectors backed by the
configuration files found in `configs/`.

## Data Layer

The `assistant.data` package provides lightweight connectors for third-party
market data providers. Each connector exposes a `fetch_latest_snapshot()` method
returning structured payloads. Configuration is supplied through JSON files in
`configs/` and loaded via `assistant.data.config.load_json_config`.

An `EconomicCalendarClient` delivers placeholder event data that can later be
extended to integrate with a real provider.

## Scheduling

The `assistant.scheduler` package introduces a Celery-based (optional) stub for
triggering the morning preparation workflow and session hooks. The
`scheduler_app` object is initialised only when Celery is installed. When
available, it registers periodic tasks defined in `SESSION_SCHEDULE` that cover:

- 07:30 CET – Morning briefing generation via `MorningPreparationService`.
- 09:00, 11:00, 14:30, 17:00, 20:00 CET – Session-specific hook placeholders.

Projects that prefer Airflow or another scheduler can replace the Celery stub
while reusing the schedule metadata exported in `SESSION_SCHEDULE`.

## Command Line Interface

The `scripts/run_morning_briefing.py` entry point constructs the default service
and prints the generated briefing. The script accepts an optional export path to
persist the generated report, making it easy to integrate the workflow into
cron jobs or deployment pipelines.
