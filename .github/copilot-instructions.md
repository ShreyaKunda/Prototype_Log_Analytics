# Project instructions for GitHub Copilot

## Project goal

Build a lightweight AI-powered unified telemetry/log analytics prototype.

## Architecture

Use this pipeline:

1. Heterogeneous logs
2. Parse and normalize into a common TelemetryEvent schema
3. Store/query with DuckDB
4. Run deterministic analytics and anomaly detection
5. Retrieve relevant evidence
6. Runtime AI agents investigate anomalies and generate hypotheses
7. Explainability layer converts findings into evidence-backed explanations
8. Streamlit presents the results

## Engineering rules

- Prefer simple Python modules over heavy frameworks.
- Keep interfaces typed and testable.
- Do not make the LLM responsible for basic counting, filtering, aggregation, or statistical anomaly detection.
- Never fabricate telemetry evidence.
- AI findings must reference actual event IDs, metrics, or rules.
- Do not expose hidden chain-of-thought. Return concise rationale backed by observable evidence.
- Keep provider-specific LLM code behind a small interface.
- Use synthetic data for the initial prototype.
- Do not add Kafka, Elasticsearch, Kubernetes, vector databases, or other infrastructure unless explicitly requested.
- Keep secrets out of source control.
- Add tests for normalization, anomaly detection, retrieval, and explanation objects.

## Coding style

- Python 3.11+
- Type hints
- Small functions/classes
- Clear docstrings for public interfaces
- Pydantic models for important data contracts
