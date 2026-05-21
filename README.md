Simple Trading Analysis Bot (MVP)

Description
- Starter Python script to load OHLC CSV, compute basic indicators (SMA, EMA, MACD, RSI), generate simple buy/sell signals, and run a basic backtest.

Quick start

1. Create or place a CSV named `Data1.csv` in the project folder with columns: `Date,Open,High,Low,Close,Volume` (Date in ISO format preferred).
2. Install deps:

```bash
pip install -r requirements.txt
```

3. Run:

```bash
python Trading_analysis.py --csv Data1.csv --out myrun --capital 10000
```

Outputs
- `myrun_portfolio.csv` — portfolio time series
- `myrun_trades.csv` — executed trades (if any)

Notes
- This is an MVP for learning; strategy rules are simple and not production-ready.
- For live data, integrate `yfinance` or a brokerage API and add risk checks before execution.
