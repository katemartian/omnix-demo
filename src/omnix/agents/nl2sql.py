from __future__ import annotations
import re
from datetime import date, timedelta
from typing import Dict, Tuple

def _recent_weeks(n: int) -> Tuple[str, str]:
    end = date.today()
    start = end - timedelta(weeks=n)
    return (start.isoformat(), end.isoformat())

def parse_intent(text: str) -> Dict:
    t = text.lower().strip()

    # 1) Trend last N weeks Rx for province
    m = re.search(r"last\s+(\d+)\s+weeks?.*rx.*(in|for)\s+([a-z]{2})", t)
    if m:
        weeks = int(m.group(1))
        prov = m.group(3).upper()
        start, end = _recent_weeks(weeks)
        return {"intent": "trend_rx_by_week_province", "weeks": weeks, "province": prov, "start": start, "end": end}

    # 2) Underperformance vs forecast by segment in province for quarter (simplified to last 13 weeks)
    if "underperform" in t and ("segment" in t or "hcp segment" in t):
        prov = "ON" if "ontario" in t or " on " in f" {t} " else None
        start, end = _recent_weeks(13)
        return {"intent": "underperf_segment_vs_forecast", "province": prov, "start": start, "end": end}

    # 3) Anomalous districts (z-score over last N weeks)
    if "anomal" in t and "district" in t:
        start, end = _recent_weeks(12)
        return {"intent": "anomaly_district_rx", "start": start, "end": end, "z": 2.0}

    # Fallback
    return {"intent": "unknown"}

def to_sql(parsed: Dict) -> Tuple[str, Tuple]:
    intent = parsed.get("intent")

    if intent == "trend_rx_by_week_province":
        sql = """
        WITH j AS (
          SELECT CAST(date AS DATE) AS d, rx, g.province
          FROM fact_sales f
          JOIN dim_geo g ON f.geo_id = g.geo_id
          WHERE CAST(date AS DATE) BETWEEN ? AND ? AND g.province = ?
        )
        SELECT strftime(d, '%Y-%W') AS year_week, SUM(rx) AS rx
        FROM j
        GROUP BY 1
        ORDER BY 1
        """
        return sql, (parsed["start"], parsed["end"], parsed["province"])

    if intent == "underperf_segment_vs_forecast":
        where_prov = "AND g.province = ?" if parsed["province"] else ""
        sql = f"""
        WITH j AS (
          SELECT CAST(date AS DATE) AS d, rx, forecast_rx, h.segment, g.province
          FROM fact_sales f
          JOIN dim_hcp h ON f.hcp_id = h.hcp_id
          JOIN dim_geo g ON f.geo_id = g.geo_id
          WHERE CAST(date AS DATE) BETWEEN ? AND ? {where_prov}
        )
        SELECT segment,
               SUM(rx) AS rx,
               SUM(forecast_rx) AS forecast_rx,
               (SUM(rx) - SUM(forecast_rx)) AS delta
        FROM j
        GROUP BY segment
        ORDER BY delta ASC
        """
        params = (parsed["start"], parsed["end"]) + ((parsed["province"],) if parsed["province"] else ())
        return sql, params

    if intent == "anomaly_district_rx":
        # Z-score on district weekly totals, flag |z| >= threshold
        sql = """
        WITH j AS (
          SELECT CAST(date AS DATE) AS d, rx, g.district
          FROM fact_sales f
          JOIN dim_geo g ON f.geo_id = g.geo_id
          WHERE CAST(date AS DATE) BETWEEN ? AND ?
        ),
        wk AS (
          SELECT district, strftime(d, '%Y-%W') AS year_week, SUM(rx) AS rx
          FROM j GROUP BY district, strftime(d, '%Y-%W')
        ),
        stats AS (
          SELECT district,
                 AVG(rx) AS mu,
                 STDDEV_POP(rx) AS sigma
          FROM wk GROUP BY district
        )
        SELECT w.district, w.year_week, w.rx,
               CASE WHEN s.sigma = 0 THEN 0 ELSE (w.rx - s.mu)/s.sigma END AS z
        FROM wk w JOIN stats s USING(district)
        WHERE ABS(CASE WHEN s.sigma = 0 THEN 0 ELSE (w.rx - s.mu)/s.sigma END) >= ?
        ORDER BY ABS(z) DESC
        """
        return sql, (parsed["start"], parsed["end"], parsed["z"])

    return "SELECT 'unknown' AS message", ()
