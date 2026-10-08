from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # reads .env into environment variables

ROOT = Path(__file__).resolve().parent.parent   # .../wealth-ai
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "wealth.db"

DATA_DIR.mkdir(exist_ok=True)

BENCHMARK = "SPY"          # S&P 500 ETF, what we compare portfolios against
HISTORY_START = "2018-01-01"