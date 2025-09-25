from omnix.agents.talk_to_sql import ask

def test_trend_province():
    out = ask("Show last 6 weeks RX in ON")
    assert out["intent"] == "trend_rx_by_week_province"
    assert len(out["rows"]) > 0
    assert "year_week" in out["rows"][0] and "rx" in out["rows"][0]

def test_underperf_segment():
    out = ask("Which HCP segment underperformed vs forecast in Ontario?")
    assert out["intent"] == "underperf_segment_vs_forecast"
    assert len(out["rows"]) > 0
    assert set(out["rows"][0]).issuperset({"segment","rx","forecast_rx","delta"})

def test_anomaly_districts():
    out = ask("Flag anomalous districts")
    assert out["intent"] == "anomaly_district_rx"
    assert len(out["rows"]) >= 0  # could be empty if no anomalies
