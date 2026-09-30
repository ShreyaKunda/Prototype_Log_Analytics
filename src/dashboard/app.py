"""Streamlit entry point for the telemetry analytics prototype."""

import streamlit as st

from src.generator.synthetic import generate_demo_events

st.set_page_config(page_title="Telemetry Intelligence", layout="wide")

st.title("AI-Powered Telemetry Intelligence")
st.caption("Unified telemetry • anomaly detection • root-cause investigation • explainability")

events = generate_demo_events()
st.metric("Telemetry events", len(events))

st.subheader("Sample normalized events")
st.dataframe(
    [
        {
            "Event ID": event.event_id,
            "Time": event.timestamp,
            "Platform": event.platform,
            "Component": event.component,
            "Severity": event.severity,
            "Type": event.event_type,
            "Metric": event.metric_name,
            "Value": event.metric_value,
        }
        for event in events
    ],
    use_container_width=True,
)

st.info(
    "Foundation milestone: synthetic multi-platform telemetry is now normalized "
    "into a common schema. Analytics and runtime agents are the next layers."
)
