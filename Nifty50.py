import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


# ==================================================
# Stoke's Data save
# ==================================================
data = yf.download("^NSEI", start="2024-01-01",end="2026-05-15")
data.to_excel("Nifty50.xlsx")
print(data)


# ==================================================
# Load Data from excel file
# ==================================================
data = pd.read_excel("Nifty50.xlsx")


# ==================================================
# Data's Type Change
# ==================================================
print(data.dtypes)

data["Price"] = pd.to_datetime(data['Price'], format='%d-%m-%y', errors='coerce')
data["Close"].astype(float)
data["High"].astype(float)
data["Low"].astype(float)
data["Open"].astype(float)
data["Volume"].astype(float)

print(data.dtypes)


# ==================================================
# Last 30 Day's Data
# ==================================================
data_last_30 = data.iloc[-30:,:]


# ==================================================
# Overwell Statictics
# ==================================================
print('='*50)
print("Overwell Statictics")
print('='*50)

print("Highest Price:", data['High'].max())
print("Date:", data.loc[data['High'].idxmax(), "Price"])
print("Price:", data.loc[data['High'].idxmax(), "Volume"])

print("\nLowest Price:", data['Low'].min())
print("Date:", data.loc[data['Low'].idxmin(), "Price"])
print("Price:", data.loc[data['Low'].idxmin(), "Volume"])

print("\nAvarage Price:", data['Close'].mean() / 4 + data['High'].mean() / 4 + data['Low'].mean() / 4 + data['Open'].mean() / 4)

print("\nMax Volume:",data["Volume"].max())
print("Date:", data.loc[data['Volume'].idxmax(), "Price"])
print("Price:", data.loc[data["Volume"].idxmax(), "Close"])

print("\nLow Volume:", data['Volume'].min())
print("Date:", data.loc[data['Volume'].idxmin(), "Price"])
print("Price:", data.loc[data["Volume"].idxmin(), "Close"])


# ==================================================
# Chart
# ==================================================

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# ALL DAY
axes[0, 0].plot(data.index, data["Low"], label='Low', color='red')
axes[0, 0].plot(data.index, data["High"], label='High', color='green')
axes[0, 0].plot(data.index, data["Close"], label='Close', color='blue')
axes[0, 0].plot(data.index, data["Open"], label='Open', color='black')
avg_price = data['Close'] / 4 + data['High'] / 4 + data['Low'] / 4 + data['Open'] / 4
axes[0, 0].plot(data.index, avg_price, label='Average Price', color='yellow')
axes[0, 0].set_title("2024-01-01 to 2026-05-15", fontsize=12)
axes[0, 0].set_xlabel('Day')
axes[0, 0].set_ylabel('Price')
axes[0, 0].legend()
axes[0, 0].grid()

axes[0, 1].plot(data.index, data["Volume"], label='Volume', color='purple')
axes[0, 1].set_title("Volume (All Data)", fontsize=12)
axes[0, 1].set_xlabel('Day')
axes[0, 1].set_ylabel('Volume')
axes[0, 1].legend()
axes[0, 1].grid()

# LAST 30 DAY
avg_price_30 = data_last_30['Close'] / 4 + data_last_30['High'] / 4 + data_last_30['Low'] / 4 + data_last_30['Open'] / 4
ma = np.convolve(avg_price_30, np.ones(5)/5, mode="valid")
axes[1, 0].plot(data_last_30.index, data_last_30["Low"], label='Low', color='red')
axes[1, 0].plot(data_last_30.index, data_last_30["High"], label='High', color='green')
axes[1, 0].plot(data_last_30.index, data_last_30["Close"], label='Close', color='blue')
axes[1, 0].plot(data_last_30.index, data_last_30["Open"], label='Open', color='black')
axes[1, 0].plot(data_last_30.index, avg_price_30, label='Average Price', color='yellow')
axes[1, 0].plot(data_last_30.index[4:], ma, label="Moving Avg", color='orange')
axes[1, 0].set_title("Last 30 Days", fontsize=12)
axes[1, 0].set_xlabel('Day')
axes[1, 0].set_ylabel('Price')
axes[1, 0].legend()
axes[1, 0].grid()

axes[1, 1].plot(data_last_30.index, data_last_30["Volume"], label='Volume', color='purple')
axes[1, 1].set_title("Volume (Last 30 Days)", fontsize=12)
axes[1, 1].set_xlabel('Day')
axes[1, 1].set_ylabel('Volume')
axes[1, 1].legend()
axes[1, 1].grid()

plt.suptitle("Nifty50", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()