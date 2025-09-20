"""yfinance market data connector stub."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class YFinanceConnector:
    """Placeholder connector for the yfinance library."""

    ticker: str = "^GSPC"
    session: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    name: str = "yfinance"

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "YFinanceConnector":
        """Instantiate the connector from configuration values."""
        return cls(
            ticker=config.get("ticker", "^GSPC"),
            metadata={k: v for k, v in config.items() if k not in {"ticker"}},
        )

    def fetch_latest_snapshot(self) -> Dict[str, Any]:
        """Return a placeholder quote for an index or equity."""
        return {
            "ticker": self.ticker,
            "price": self.metadata.get("mock_price", 0.0),
            "source": self.name,
        }
