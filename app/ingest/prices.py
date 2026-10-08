import pandas as pd
import yfinance as yf
from app.db import get_conn


def fetch_prices(tickers: list[str], start: str) -> pd.DataFrame:
    """Download adjusted daily closes and return them in long format."""
    raw = yf.download(tickers, start=start, auto_adjust=True, progress=False)
    if raw.empty:
        raise ValueError(f"No data returned for {tickers}")

    close = raw["Close"]                    # wide: rows=dates, cols=tickers
    if isinstance(close, pd.Series):        # older yfinance + single ticker
        close = close.to_frame(tickers[0])

    long = (
        close.rename_axis("date")
             .reset_index()                 # date becomes a column
             .melt(id_vars="date", var_name="ticker", value_name="close")
             .dropna()                      # holidays / pre-IPO dates
    )
    long["date"] = long["date"].dt.strftime("%Y-%m-%d")
    return long[["date", "ticker", "close"]]


def save_prices(df: pd.DataFrame) -> int:
    rows = list(df.itertuples(index=False, name=None))
    with get_conn() as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO prices (date, ticker, close) VALUES (?, ?, ?)",
            rows,
        )
    return len(rows)


def load_prices(tickers: list[str] | None = None) -> pd.DataFrame:
    """Read prices back as WIDE format, ready for math."""
    with get_conn() as conn:
        df = pd.read_sql("SELECT date, ticker, close FROM prices", conn,
                         parse_dates=["date"])
    if tickers:
        df = df[df["ticker"].isin(tickers)]
    return df.pivot(index="date", columns="ticker", values="close").sort_index()