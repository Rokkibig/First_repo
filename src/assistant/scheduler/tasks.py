"""Scheduling stubs for triggering morning preparation workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

try:  # pragma: no cover - optional dependency for illustrative scheduling
    from celery import Celery
    from celery.schedules import crontab
except ImportError:  # pragma: no cover - executed when Celery is not available
    Celery = None  # type: ignore
    crontab = None  # type: ignore

from ..morning import create_default_service

TIMEZONE = "CET"


@dataclass(frozen=True)
class SessionTiming:
    """Representation of a scheduled session."""

    hour: int
    minute: int
    label: str


SESSION_SCHEDULE: Dict[str, SessionTiming] = {
    "pre_open": SessionTiming(hour=7, minute=30, label="07:30"),
    "market_open": SessionTiming(hour=9, minute=0, label="09:00"),
    "mid_morning": SessionTiming(hour=11, minute=0, label="11:00"),
    "us_open": SessionTiming(hour=14, minute=30, label="14:30"),
    "late_session": SessionTiming(hour=17, minute=0, label="17:00"),
    "close_review": SessionTiming(hour=20, minute=0, label="20:00"),
}


scheduler_app: Optional[Celery]
if Celery is not None:
    scheduler_app = Celery("assistant_scheduler")
    scheduler_app.conf.timezone = TIMEZONE
else:  # pragma: no cover - scheduler stub without Celery available
    scheduler_app = None


def _celery_task(*decorator_args, **decorator_kwargs):  # pragma: no cover - helper
    """Create a Celery task decorator that becomes a no-op when Celery is missing."""

    def decorator(func):
        if scheduler_app is not None:
            return scheduler_app.task(*decorator_args, **decorator_kwargs)(func)
        return func

    return decorator


@_celery_task(name="assistant.run_morning_preparation")
def run_morning_preparation(session_label: str = SESSION_SCHEDULE["pre_open"].label) -> str:
    """Trigger the morning preparation workflow for the requested session."""
    if session_label == SESSION_SCHEDULE["pre_open"].label:
        service = create_default_service()
        return service.run()
    return f"Session hook executed for {session_label}."


def register_periodic_tasks(app: Optional[Celery] = None) -> None:
    """Register periodic tasks for the defined sessions on the scheduler app."""
    app = app or scheduler_app
    if app is None or crontab is None:  # pragma: no cover - occurs without Celery
        return
    for name, timing in SESSION_SCHEDULE.items():
        app.add_periodic_task(
            crontab(minute=timing.minute, hour=timing.hour, timezone=TIMEZONE),
            run_morning_preparation.s(timing.label),
            name=f"assistant.{name}",
        )


if scheduler_app is not None:  # pragma: no cover - only executed with Celery
    @scheduler_app.on_after_configure.connect
    def _setup_periodic_tasks(sender, **_kwargs):
        register_periodic_tasks(sender)
