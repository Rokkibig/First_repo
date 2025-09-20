"""Economic calendar client placeholder."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


def _current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class EconomicCalendarClient:
    """Stub client that simulates fetching upcoming economic events."""

    provider: str = "mock"
    session: Any = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def fetch_events(self) -> List[Dict[str, Any]]:
        """Return placeholder economic events."""
        events = self.metadata.get("events")
        if events is not None:
            return events
        return [
            {
                "timestamp": _current_timestamp(),
                "event": "Central bank speech",
                "importance": "high",
                "provider": self.provider,
            }
        ]
