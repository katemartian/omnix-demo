from __future__ import annotations
from pathlib import Path
import duckdb
from typing import Optional

_DB: Optional[duckdb.DuckDBPyConnection] = None

def get_conn() -> duckdb.DuckDBPyConnection:
    """Singleton DuckDB connection with tables registered from data/ CSVs."""
    global _DB
    if _DB is not None:
        return _DB
    root = Path(__file__).resolve().parents[2] / "data"
    _DB = duckdb.connect(database=":memory:")
    #_DB.execute("PRAGMA verify_parallelism=false")  # stable unit tests
    # Register CSVs as views (read_csv_auto infers types)
    _DB.execute(f"CREATE VIEW dim_hcp AS SELECT * FROM read_csv_auto('{root/'dim_hcp.csv'}', HEADER=TRUE)")
    _DB.execute(f"CREATE VIEW dim_geo AS SELECT * FROM read_csv_auto('{root/'dim_geo.csv'}', HEADER=TRUE)")
    _DB.execute(f"CREATE VIEW dim_payer AS SELECT * FROM read_csv_auto('{root/'dim_payer.csv'}', HEADER=TRUE)")
    _DB.execute(f"CREATE VIEW fact_sales AS SELECT * FROM read_csv_auto('{root/'fact_sales.csv'}', HEADER=TRUE)")
    return _DB
