"""Morning briefing orchestration service."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

from ..data import (
    AlphaVantageConnector,
    EconomicCalendarClient,
    TwelveDataConnector,
    YFinanceConnector,
)
from ..data.config import load_json_config


@dataclass
class MorningPreparationService:
    """Coordinate the steps required for the morning market briefing."""

    market_connectors: Iterable[Any] = field(default_factory=list)
    economic_calendar: Optional[Any] = None
    scenario_builders: Iterable[Any] = field(default_factory=list)

    def collect_market_context(self) -> Dict[str, Any]:
        """Collect market data snapshots from configured connectors."""
        context: Dict[str, Any] = {}
        for connector in self.market_connectors:
            fetch = getattr(connector, "fetch_latest_snapshot", None)
            if callable(fetch):
                context[getattr(connector, "name", connector.__class__.__name__)] = fetch()
        return context

    def fetch_economic_events(self) -> List[Dict[str, Any]]:
        """Fetch the latest economic calendar events."""
        if self.economic_calendar is None:
            return []
        fetch = getattr(self.economic_calendar, "fetch_events", None)
        if callable(fetch):
            return list(fetch())
        return []

    def build_trading_scenarios(
        self,
        market_context: Dict[str, Any],
        economic_events: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Build trading scenarios based on collected data."""
        scenarios: List[Dict[str, Any]] = []
        for builder in self.scenario_builders:
            build = getattr(builder, "build", None)
            if callable(build):
                scenarios.append(build(market_context, economic_events))
        if not scenarios:
            scenarios.append(
                {
                    "name": "baseline",
                    "description": "Default scenario awaiting implementation.",
                    "inputs": {
                        "market_context": market_context,
                        "economic_events": economic_events,
                    },
                }
            )
        return scenarios

    def generate_briefing_report(
        self,
        market_context: Dict[str, Any],
        economic_events: List[Dict[str, Any]],
        scenarios: List[Dict[str, Any]],
    ) -> str:
        """Generate a textual briefing report from the prepared artefacts."""
        lines = ["=== Morning Briefing Report ===", ""]
        lines.append("-- Market Context --")
        if market_context:
            for source, payload in market_context.items():
                lines.append(f"Source: {source}")
                lines.append(f"  Data: {payload}")
        else:
            lines.append("No market context available.")

        lines.append("")
        lines.append("-- Economic Events --")
        if economic_events:
            for event in economic_events:
                lines.append(f"  - {event}")
        else:
            lines.append("No economic events retrieved.")

        lines.append("")
        lines.append("-- Trading Scenarios --")
        if scenarios:
            for scenario in scenarios:
                name = scenario.get("name", "unnamed")
                description = scenario.get("description", "")
                lines.append(f"  * {name}: {description}")
        else:
            lines.append("No scenarios generated.")

        lines.append("")
        lines.append("=== End of Report ===")
        return "\n".join(lines)

    def run(self) -> str:
        """Execute the full morning preparation workflow."""
        market_context = self.collect_market_context()
        economic_events = self.fetch_economic_events()
        scenarios = self.build_trading_scenarios(market_context, economic_events)
        return self.generate_briefing_report(market_context, economic_events, scenarios)


def create_default_service(config_dir: str = "configs") -> MorningPreparationService:
    """Factory that builds a service wired to the stub connectors."""
    alpha_config = load_json_config(f"{config_dir}/alpha_vantage.json")
    twelve_config = load_json_config(f"{config_dir}/twelve_data.json")
    yfinance_config = load_json_config(f"{config_dir}/yfinance.json")
    calendar_config = load_json_config(f"{config_dir}/economic_calendar.json")

    connectors = [
        AlphaVantageConnector.from_config(alpha_config),
        TwelveDataConnector.from_config(twelve_config),
        YFinanceConnector.from_config(yfinance_config),
    ]
    economic_calendar = EconomicCalendarClient(
        provider=calendar_config.get("provider", "mock"),
        metadata=calendar_config.get("metadata", {}),
    )
    return MorningPreparationService(
        market_connectors=connectors,
        economic_calendar=economic_calendar,
    )
