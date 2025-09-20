"""Alpha Vantage market data connector stub."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AlphaVantageConnector:
    """Placeholder connector for the Alpha Vantage API."""

    api_key: Optional[str] = None
    symbol: str = "SPY"
    session: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    name: str = "alpha_vantage"

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "AlphaVantageConnector":
        """Instantiate the connector from configuration values."""
        return cls(
            api_key=config.get("api_key"),
            symbol=config.get("symbol", "SPY"),
            metadata={k: v for k, v in config.items() if k not in {"api_key", "symbol"}},
        )

    def fetch_latest_snapshot(self) -> Dict[str, Any]:
        """Retrieve a placeholder market snapshot from Alpha Vantage."""
        return {
            "symbol": self.symbol,
            "price": self.metadata.get("mock_price", 0.0),
            "source": self.name,
        }
