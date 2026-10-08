import pandas as pd
from app.db import get_conn

REQUIRED = {"client_id", "ticker", "shares"}


def load_portfolio_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {missing}")

    df["ticker"] = df["ticker"].str.strip().str.upper()
    df["client_id"] = df["client_id"].str.strip()

    if (df["shares"] <= 0).any():
        raise ValueError("All share counts must be positive")

    # Same ticker listed twice for a client? Combine the lots.
    return df.groupby(["client_id", "ticker"], as_index=False)["shares"].sum()


def save_holdings(df: pd.DataFrame) -> int:
    rows = list(df[["client_id", "ticker", "shares"]].itertuples(index=False, name=None))
    with get_conn() as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO holdings (client_id, ticker, shares) VALUES (?, ?, ?)",
            rows,
        )
    return len(rows)


def get_holdings(client_id: str) -> pd.DataFrame:
    with get_conn() as conn:
        return pd.read_sql(
            "SELECT ticker, shares FROM holdings WHERE client_id = ?",
            conn, params=(client_id,),
        )