# AI-Powered Unified Telemetry & Log Analytics

A lightweight prototype for ingesting heterogeneous telemetry/log data, normalizing it into a unified schema, detecting anomalies with deterministic analytics, and using AI agents for root-cause investigation and explainability.

## Prototype flow

Multiple log sources → ingestion/normalization → DuckDB → analytics/anomaly detection → AI investigation → explainability → Streamlit dashboard

## Design principles

- Keep the runtime lightweight and locally runnable.
- Use deterministic/statistical analytics for anomaly detection.
- Use LLM agents for investigation, correlation, hypothesis generation, and natural-language interaction.
- Every AI finding should be traceable to supporting telemetry events and measurable evidence.
- Avoid exposing or relying on hidden chain-of-thought; the explainability layer exposes evidence, rules, metrics, retrieved events, confidence, and alternatives.
- Start with synthetic telemetry so the prototype is reproducible and contains known incidents.

## Planned capabilities

1. Unified telemetry schema
2. Synthetic multi-platform telemetry generator
3. DuckDB-based local telemetry store
4. Statistical anomaly detection
5. Root-cause investigation agent
6. Evidence/explainability layer
7. Streamlit dashboard
8. Natural-language "Ask Telemetry" interface
9. Later: historical incident RAG

## Repository structure

```
.github/
  agents/                 # GitHub Copilot development agents
  copilot-instructions.md # project-wide Copilot guidance
src/
  ingestion/              # parsers and normalization
  storage/                # DuckDB access
  analytics/              # anomaly detection and correlation
  agents/                 # runtime telemetry agents
  explainability/         # evidence and explanation objects
  retrieval/              # structured log retrieval / later RAG
  generator/              # synthetic telemetry
  dashboard/              # Streamlit UI
data/
  raw/                    # generated/source logs
  processed/              # normalized data
tests/
docs/
```

## Getting started

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt
streamlit run src/dashboard/app.py
```

The first milestone is the deterministic telemetry pipeline. Runtime LLM configuration will be added after the data and evidence layers are working.
