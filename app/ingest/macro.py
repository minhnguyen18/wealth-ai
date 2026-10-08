import pandas as pd
from app.db import get_conn

FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"

SERIES = {
    "DGS10":    "10-year Treasury yield (%)",
    "FEDFUNDS": "Federal funds rate (%)",
    "CPIAUCSL": "Consumer price index",
    "UNRATE":   "Unemployment rate (%)",
    "T10Y2Y":   "10y minus 2y yield spread (%)",
}


def fetch_series(series_id: str, start: str) -> pd.DataFrame:
    df = pd.read_csv(
        FRED_CSV.format(sid=series_id),
        index_col=0, parse_dates=True,
        na_values=".",            # FRED marks missing values with "."
    )
    s = df.iloc[:, 0].loc[start:].dropna()
    return pd.DataFrame({
        "date": s.index.strftime("%Y-%m-%d"),
        "series_id": series_id,
        "value": s.values,
    })


def save_macro(df: pd.DataFrame) -> int:
    rows = list(df.itertuples(index=False, name=None))
    with get_conn() as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO macro (date, series_id, value) VALUES (?, ?, ?)",
            rows,
        )
    return len(rows)