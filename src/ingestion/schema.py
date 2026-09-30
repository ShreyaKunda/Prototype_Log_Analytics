"""Canonical telemetry data contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TelemetryEvent(BaseModel):
    """Normalized event shared by every telemetry source."""

    event_id: str
    timestamp: datetime
    source: str
    platform: str
    component: str
    severity: str
    event_type: str
    message: str
    host: str | None = None
    metric_name: str | None = None
    metric_value: float | None = None
    trace_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    raw_log: str | None = None
