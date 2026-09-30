from datetime import datetime, timezone

from src.ingestion.schema import TelemetryEvent


def test_telemetry_event_contract():
    event = TelemetryEvent(
        event_id="TEST-001",
        timestamp=datetime.now(timezone.utc),
        source="test",
        platform="platform-a",
        component="COMMS",
        severity="INFO",
        event_type="HEARTBEAT",
        message="Heartbeat received",
    )

    assert event.event_id == "TEST-001"
    assert event.component == "COMMS"
