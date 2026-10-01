"""Lightweight DuckDB storage and evidence-query helpers for telemetry."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

import duckdb

from src.ingestion.schema import TelemetryEvent


class DuckDBTelemetryStore:
    """Persist normalized telemetry and expose deterministic query tools.

    This layer retrieves and summarizes evidence for AI agents. It does not
    decide whether an observation is anomalous.
    """

    def __init__(self, db_path: str | Path = "data/processed/telemetry.duckdb") -> None:
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(self.db_path)

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS telemetry (
                    event_id VARCHAR PRIMARY KEY,
                    timestamp TIMESTAMP,
                    source VARCHAR,
                    platform VARCHAR,
                    component VARCHAR,
                    severity VARCHAR,
                    event_type VARCHAR,
                    message VARCHAR,
                    host VARCHAR,
                    metric_name VARCHAR,
                    metric_value DOUBLE,
                    trace_id VARCHAR,
                    metadata JSON,
                    raw_log VARCHAR
                )
                """
            )

    def insert_events(self, events: Iterable[TelemetryEvent]) -> int:
        rows = list(events)
        if not rows:
            return 0

        with self._connect() as conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO telemetry
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        event.event_id,
                        event.timestamp,
                        event.source,
                        event.platform,
                        event.component,
                        event.severity,
                        event.event_type,
                        event.message,
                        event.host,
                        event.metric_name,
                        event.metric_value,
                        event.trace_id,
                        json.dumps(event.metadata),
                        event.raw_log,
                    )
                    for event in rows
                ],
            )
        return len(rows)

    def query_telemetry(
        self,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        component: str | None = None,
        metric_name: str | None = None,
        severity: str | None = None,
        event_type: str | None = None,
        source: str | None = None,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        """Return traceable telemetry evidence using optional filters."""
        if limit < 1:
            raise ValueError("limit must be greater than zero")

        clauses: list[str] = []
        params: list[Any] = []

        filters = (
            ("timestamp >= ?", start_time),
            ("timestamp <= ?", end_time),
            ("component = ?", component),
            ("metric_name = ?", metric_name),
            ("severity = ?", severity),
            ("event_type = ?", event_type),
            ("source = ?", source),
        )
        for clause, value in filters:
            if value is not None:
                clauses.append(clause)
                params.append(value)

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        query = f"""
            SELECT event_id, timestamp, source, platform, component, severity,
                   event_type, message, host, metric_name, metric_value,
                   trace_id, CAST(metadata AS VARCHAR) AS metadata, raw_log
            FROM telemetry
            {where}
            ORDER BY timestamp ASC
            LIMIT ?
        """
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
            columns = [item[0] for item in conn.description]

        return [dict(zip(columns, row)) for row in rows]

    def metric_summary(
        self,
        metric_name: str,
        *,
        start_time: datetime | None = None,
        end_time: datetime | None = None,
        component: str | None = None,
    ) -> dict[str, Any]:
        """Return descriptive metric statistics without anomaly classification."""
        clauses = ["metric_name = ?", "metric_value IS NOT NULL"]
        params: list[Any] = [metric_name]

        if start_time is not None:
            clauses.append("timestamp >= ?")
            params.append(start_time)
        if end_time is not None:
            clauses.append("timestamp <= ?")
            params.append(end_time)
        if component is not None:
            clauses.append("component = ?")
            params.append(component)

        with self._connect() as conn:
            row = conn.execute(
                f"""
                SELECT COUNT(*) AS count,
                       AVG(metric_value) AS mean,
                       STDDEV_SAMP(metric_value) AS stddev,
                       MIN(metric_value) AS min,
                       MAX(metric_value) AS max
                FROM telemetry
                WHERE {' AND '.join(clauses)}
                """,
                params,
            ).fetchone()

        return {
            "metric_name": metric_name,
            "count": row[0],
            "mean": row[1],
            "stddev": row[2],
            "min": row[3],
            "max": row[4],
            "component": component,
            "start_time": start_time,
            "end_time": end_time,
        }

    def count(self) -> int:
        with self._connect() as conn:
            return int(conn.execute("SELECT COUNT(*) FROM telemetry").fetchone()[0])
