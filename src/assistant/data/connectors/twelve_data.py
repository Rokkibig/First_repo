"""Twelve Data market data connector stub."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TwelveDataConnector:
    """Placeholder connector for Twelve Data API."""

    api_key: Optional[str] = None
    instruments: list[str] = field(default_factory=lambda: ["EUR/USD"])
    session: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    name: str = "twelve_data"

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "TwelveDataConnector":
        """Instantiate the connector from configuration values."""
        return cls(
            api_key=config.get("api_key"),
            instruments=config.get("instruments", ["EUR/USD"]),
            metadata={k: v for k, v in config.items() if k not in {"api_key", "instruments"}},
        )

    def fetch_latest_snapshot(self) -> Dict[str, Any]:
        """Return a placeholder snapshot for FX instruments."""
        return {
            "instruments": self.instruments,
            "quote": self.metadata.get("mock_quote", 0.0),
            "source": self.name,
        }
