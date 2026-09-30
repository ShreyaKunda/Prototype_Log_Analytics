from src.generator.synthetic import generate_demo_events


def test_demo_generator_contains_known_incident():
    events = generate_demo_events(seed=42, minutes=20)

    assert len(events) > 0
    assert any(event.event_type == "CONNECTION_TIMEOUT" for event in events)
    assert any(
        event.metric_name == "network_latency_ms" and event.metric_value > 80
        for event in events
    )
