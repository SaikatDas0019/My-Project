import os
import sys
import argparse
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def load_csv(path):
    # Robust CSV loader: accept files with Date/Day as first col and Close/Price as value col
    try:
        df = pd.read_csv(path)
    except Exception as e:
        raise RuntimeError(f"Failed to read CSV {path}: {e}")

    # Normalize column names
    cols_lower = [c.lower() for c in df.columns]

    # If there's a 'price' column, treat it as Close
    if 'price' in cols_lower and 'close' not in cols_lower:
        price_col = df.columns[cols_lower.index('price')]
        df.rename(columns={price_col: 'Close'}, inplace=True)

    # If first column looks like a date, parse it; otherwise keep as index (string)
    first_col = df.columns[0]
    if pd.api.types.is_datetime64_any_dtype(df[first_col]) or pd.to_datetime(df[first_col], errors='coerce').notna().any():
        df[first_col] = pd.to_datetime(df[first_col], errors='coerce')
        df.rename(columns={first_col: 'Date'}, inplace=True)
        df.set_index('Date', inplace=True)
    else:
        # use the first column as index (non-datetime), rename to 'Index' for clarity
        df.rename(columns={first_col: 'Index'}, inplace=True)
        df.set_index('Index', inplace=True)

    # Ensure Close exists
    if 'Close' not in df.columns:
        # try common alternatives
        for alt in ['close', 'adj close', 'price']:
            if alt in cols_lower:
                df.rename(columns={df.columns[cols_lower.index(alt)]: 'Close'}, inplace=True)
                break

    # Convert Close to numeric
    if 'Close' in df.columns:
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    return df


def compute_indicators(df):
    df = df.copy()
    # require Close
    if 'Close' not in df.columns:
        raise RuntimeError('No Close/Price column found in data. Provide CSV with Close or Price column.')

    close = pd.to_numeric(df['Close'], errors='coerce')
    # Drop rows without numeric close
    df = df.loc[close.notna()].copy()
    close = df['Close']

    # If not enough data for long windows, still compute using available rows
    df['SMA_20'] = close.rolling(min_periods=1, window=20).mean()
    df['SMA_50'] = close.rolling(min_periods=1, window=50).mean()
    df['EMA_12'] = close.ewm(span=12, adjust=False).mean()
    df['EMA_26'] = close.ewm(span=26, adjust=False).mean()

    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_SIGNAL'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # RSI (handle division by zero)
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(min_periods=1, window=14).mean()
    ma_down = down.rolling(min_periods=1, window=14).mean()
    rs = ma_up / ma_down.replace(0, np.nan)
    df['RSI_14'] = 100 - (100 / (1 + rs))

    return df


def generate_signals(df):
    df = df.copy()
    # Simple rules:
    # Buy when EMA12 > EMA26 and MACD > MACD_SIGNAL and RSI < 40
    # Sell when EMA12 < EMA26 and MACD < MACD_SIGNAL and RSI > 60
    cond_buy = (df['EMA_12'] > df['EMA_26']) & (df['MACD'] > df['MACD_SIGNAL']) & (df['RSI_14'] < 40)
    cond_sell = (df['EMA_12'] < df['EMA_26']) & (df['MACD'] < df['MACD_SIGNAL']) & (df['RSI_14'] > 60)
    df['signal'] = 0
    df.loc[cond_buy, 'signal'] = 1
    df.loc[cond_sell, 'signal'] = -1
    return df


def backtest_signals(df, init_capital=10000):
    df = df.copy()
    position = 0
    entry_price = 0.0
    cash = init_capital
    equity = init_capital
    shares = 0
    trades = []

    df['portfolio_value'] = np.nan
    df['holdings'] = 0.0
    df['cash'] = 0.0

    for idx, row in df.iterrows():
        price = row['Close']
        sig = row['signal']

        # Enter long
        if sig == 1 and position == 0:
            shares = int(cash // price)
            if shares > 0:
                entry_price = price
                cash -= shares * price
                position = 1
                trades.append({'Date': idx, 'Type': 'BUY', 'Price': price, 'Shares': int(shares)})

        # Exit long
        if sig == -1 and position == 1:
            cash += shares * price
            trades.append({'Date': idx, 'Type': 'SELL', 'Price': price, 'Shares': int(shares)})
            shares = 0
            position = 0

        holdings = shares * price
        equity = cash + holdings
        df.at[idx, 'portfolio_value'] = equity
        df.at[idx, 'holdings'] = holdings
        df.at[idx, 'cash'] = cash

    # if still holding at end, compute final
    total_return = (equity - init_capital) / init_capital

    # max drawdown
    pv = df['portfolio_value'].dropna()
    running_max = pv.cummax()
    drawdown = (pv - running_max) / running_max
    max_dd = drawdown.min()

    stats = {
        'init_capital': init_capital,
        'final_value': float(equity),
        'total_return_pct': float(total_return * 100),
        'max_drawdown_pct': float(max_dd * 100) if not np.isnan(max_dd) else 0.0,
        'trades': trades,
    }
    return df, stats


def save_outputs(df, stats, out_prefix='signals_output'):
    perf_csv = f"{out_prefix}_portfolio.csv"
    df.to_csv(perf_csv)
    # trades to csv
    trades_df = pd.DataFrame(stats['trades'])
    if not trades_df.empty:
        trades_df.to_csv(f"{out_prefix}_trades.csv", index=False)

    return perf_csv


def plot_results(df, stats, out_prefix='signals_output'):
    # Price + signals
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax[0].plot(df.index, df['Close'], label='Close', color='black')
    if 'SMA_20' in df.columns:
        ax[0].plot(df.index, df['SMA_20'], label='SMA_20', linestyle='--')
    if 'SMA_50' in df.columns:
        ax[0].plot(df.index, df['SMA_50'], label='SMA_50', linestyle='--')

    # plot buy/sell markers
    buys = df[df['signal'] == 1]
    sells = df[df['signal'] == -1]
    if not buys.empty:
        ax[0].scatter(buys.index, buys['Close'], marker='^', color='green', label='Buy')
    if not sells.empty:
        ax[0].scatter(sells.index, sells['Close'], marker='v', color='red', label='Sell')

    ax[0].set_title('Price & Signals')
    ax[0].legend()

    # MACD + RSI subplot
    if 'MACD' in df.columns and 'RSI_14' in df.columns:
        ax[1].plot(df.index, df['MACD'], label='MACD')
        ax[1].plot(df.index, df['MACD_SIGNAL'], label='MACD_SIGNAL', linestyle='--')
        ax2 = ax[1].twinx()
        ax2.plot(df.index, df['RSI_14'], label='RSI_14', color='purple', alpha=0.6)
        ax[1].legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax[1].set_title('MACD and RSI')

    plt.tight_layout()
    price_png = f"{out_prefix}_price.png"
    fig.savefig(price_png)
    plt.close(fig)

    # Portfolio curve
    if 'portfolio_value' in df.columns:
        fig2, axp = plt.subplots(figsize=(12, 4))
        axp.plot(df.index, df['portfolio_value'], label='Portfolio Value')
        axp.set_title('Portfolio Value Over Time')
        axp.legend()
        perf_png = f"{out_prefix}_portfolio.png"
        fig2.savefig(perf_png)
        plt.close(fig2)
    else:
        perf_png = None

    return price_png, perf_png


def main():
    parser = argparse.ArgumentParser(description='Simple trading analysis bot (CSV-based)')
    parser.add_argument('--csv', dest='csv', help='Path to OHLCV CSV', default='Data1.csv')
    parser.add_argument('--ticker', dest='ticker', help='Ticker to fetch via yfinance (e.g. ^NSEI for Nifty 50)', default=None)
    parser.add_argument('--out', dest='out', help='Output prefix', default='output')
    parser.add_argument('--capital', dest='capital', type=float, default=10000)
    args = parser.parse_args()
    df = None
    # If a ticker is provided, fetch from yfinance
    if args.ticker:
        try:
            raw = yf.download(args.ticker, progress=False)
        except Exception as e:
            print(f"Failed to download ticker {args.ticker}: {e}")
            sys.exit(1)

        if raw.empty:
            print(f"No data returned for ticker {args.ticker}")
            sys.exit(1)

        # ensure Date index
        raw.index.name = 'Date'
        df = raw.copy()
        # prefer 'Close' or 'Adj Close'
        if 'Adj Close' in df.columns:
            df.rename(columns={'Adj Close': 'Close'}, inplace=True)
        elif 'Close' not in df.columns and 'close' in df.columns:
            df.rename(columns={'close': 'Close'}, inplace=True)
    else:
        if not os.path.exists(args.csv):
            print(f"CSV not found: {args.csv}\nPlace a CSV (Date,Open,High,Low,Close,Volume) in the project folder or provide --csv path or --ticker.")
            sys.exit(1)

        df = load_csv(args.csv)
    df = compute_indicators(df)
    df = generate_signals(df)
    df_bt, stats = backtest_signals(df, init_capital=args.capital)

    # Save outputs
    perf_csv = save_outputs(df_bt, stats, out_prefix=args.out)

    # Create charts
    try:
        price_png, perf_png = plot_results(df_bt, stats, out_prefix=args.out)
        print(f"Saved charts: {price_png}, {perf_png}")
    except Exception as e:
        print(f"Failed to create charts: {e}")

    # Print summary
    print('--- Backtest Summary ---')
    print(f"Initial capital: {stats['init_capital']}")
    print(f"Final value: {stats['final_value']:.2f}")
    print(f"Total return: {stats['total_return_pct']:.2f}%")
    print(f"Max drawdown: {stats['max_drawdown_pct']:.2f}%")
    print(f"Trades: {len(stats['trades'])}")
    print(f"Portfolio csv saved to: {perf_csv}")


if __name__ == '__main__':
    main()
