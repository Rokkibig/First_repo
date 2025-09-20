"""Unit tests for the MorningPreparationService orchestration."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest
from unittest.mock import MagicMock

ROOT_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from assistant.morning import MorningPreparationService


class MorningPreparationServiceTestCase(unittest.TestCase):
    """Validate the orchestration logic of the morning service."""

    def test_collect_market_context_aggregates_connector_payloads(self) -> None:
        connector = MagicMock()
        connector.fetch_latest_snapshot.return_value = {"price": 123}
        connector.name = "alpha"
        service = MorningPreparationService(market_connectors=[connector])

        context = service.collect_market_context()

        connector.fetch_latest_snapshot.assert_called_once()
        self.assertIn("alpha", context)
        self.assertEqual(context["alpha"], {"price": 123})

    def test_run_invokes_pipeline_steps(self) -> None:
        service = MorningPreparationService()
        service.collect_market_context = MagicMock(return_value={"market": "data"})
        service.fetch_economic_events = MagicMock(return_value=[{"event": "test"}])
        service.build_trading_scenarios = MagicMock(return_value=[{"name": "baseline"}])
        service.generate_briefing_report = MagicMock(return_value="report")

        result = service.run()

        service.collect_market_context.assert_called_once_with()
        service.fetch_economic_events.assert_called_once_with()
        service.build_trading_scenarios.assert_called_once_with({"market": "data"}, [{"event": "test"}])
        service.generate_briefing_report.assert_called_once_with(
            {"market": "data"},
            [{"event": "test"}],
            [{"name": "baseline"}],
        )
        self.assertEqual(result, "report")


if __name__ == "__main__":  # pragma: no cover - test runner entry point
    unittest.main()
