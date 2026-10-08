from app.config import BENCHMARK, HISTORY_START, DATA_DIR
from app.db import init_db
from app.ingest.portfolio import load_portfolio_csv, save_holdings
from app.ingest.prices import fetch_prices, save_prices
from app.ingest.macro import SERIES, fetch_series, save_macro


def main():
    init_db()

    holdings = load_portfolio_csv(DATA_DIR / "sample_portfolio.csv")
    print(f"Holdings: {save_holdings(holdings)} rows")

    tickers = sorted(set(holdings["ticker"]) | {BENCHMARK})
    prices = fetch_prices(tickers, HISTORY_START)
    print(f"Prices:   {save_prices(prices)} rows for {tickers}")

    for sid, name in SERIES.items():
        try:
            n = save_macro(fetch_series(sid, HISTORY_START))
            print(f"Macro:    {n:>5} rows  {sid} ({name})")
        except Exception as e:
            print(f"Macro:    FAILED {sid}: {e}")   # one bad series shouldn't kill the run


if __name__ == "__main__":
    main()