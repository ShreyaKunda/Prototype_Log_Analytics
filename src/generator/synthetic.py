"""Generate reproducible synthetic telemetry for the prototype."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from random import Random

from src.ingestion.schema import TelemetryEvent


def generate_demo_events(seed: int = 42, minutes: int = 30) -> list[TelemetryEvent]:
    """Generate normal telemetry plus a known communication incident."""
    rng = Random(seed)
    start = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    events: list[TelemetryEvent] = []

    for minute in range(minutes):
        ts = start + timedelta(minutes=minute)

        latency = 30 + rng.uniform(-5, 5)
        packet_loss = max(0.0, rng.uniform(0, 0.8))

        # Inject a deliberately known incident in the middle of the timeline.
        if 15 <= minute <= 19:
            latency += (minute - 14) * 35
            packet_loss += (minute - 14) * 2.5

        events.append(
            TelemetryEvent(
                event_id=f"NET-{minute:04d}-LAT",
                timestamp=ts,
                source="network-platform",
                platform="Platform-B",
                component="COMMS",
                severity="WARNING" if latency > 80 else "INFO",
                event_type="LATENCY",
                message=f"Network latency measured at {latency:.1f} ms",
                host="node-01",
                metric_name="network_latency_ms",
                metric_value=round(latency, 2),
                raw_log=f"latency={latency:.2f}ms",
            )
        )

        events.append(
            TelemetryEvent(
                event_id=f"NET-{minute:04d}-LOSS",
                timestamp=ts,
                source="network-platform",
                platform="Platform-B",
                component="COMMS",
                severity="ERROR" if packet_loss > 5 else "INFO",
                event_type="PACKET_LOSS",
                message=f"Packet loss measured at {packet_loss:.1f}%",
                host="node-01",
                metric_name="packet_loss_pct",
                metric_value=round(packet_loss, 2),
                raw_log=f"packet_loss={packet_loss:.2f}%",
            )
        )

        if 17 <= minute <= 19:
            events.append(
                TelemetryEvent(
                    event_id=f"APP-{minute:04d}-TIMEOUT",
                    timestamp=ts + timedelta(seconds=20),
                    source="application-platform",
                    platform="Platform-A",
                    component="APPLICATION",
                    severity="ERROR",
                    event_type="CONNECTION_TIMEOUT",
                    message="Connection timeout while contacting COMMS subsystem",
                    host="app-01",
                    raw_log="connection timeout",
                )
            )

    return events
