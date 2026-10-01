"""Tests for deterministic telemetry storage and evidence queries."""

from datetime import timedelta

from src.generator.synthetic import generate_demo_events
from src.storage.duckdb_store import DuckDBTelemetryStore


def test_insert_and_time_range_query(tmp_path):
    events = generate_demo_events()
    store = DuckDBTelemetryStore(tmp_path / "telemetry.duckdb")
    store.insert_events(events)

    start = events[10].timestamp
    end = events[12].timestamp
    results = store.query_telemetry(
        start_time=start,
        end_time=end,
        metric_name="network_latency_ms",
    )

    assert results
    assert all(item["metric_name"] == "network_latency_ms" for item in results)
    assert all(start <= item["timestamp"] <= end for item in results)
    assert all(item["event_id"] for item in results)


def test_filters_are_combined(tmp_path):
    events = generate_demo_events()
    store = DuckDBTelemetryStore(tmp_path / "telemetry.duckdb")
    store.insert_events(events)

    results = store.query_telemetry(
        component="APPLICATION",
        event_type="CONNECTION_TIMEOUT",
    )

    assert len(results) == 3
    assert all(item["component"] == "APPLICATION" for item in results)


def test_metric_summary_returns_evidence_not_anomaly_decision(tmp_path):
    events = generate_demo_events()
    store = DuckDBTelemetryStore(tmp_path / "telemetry.duckdb")
    store.insert_events(events)

    summary = store.metric_summary(
        "network_latency_ms",
        start_time=events[0].timestamp,
        end_time=events[-1].timestamp + timedelta(seconds=1),
    )

    assert summary["count"] == 30
    assert summary["max"] > summary["mean"]
    assert "anomaly" not in summary
