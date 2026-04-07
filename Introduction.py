import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# CSV File Read:

df = pd.read_csv("Data1.csv")
print(df)


# Graph:

plt.plot(df["Day"], df["Price"], marker='o')
plt.title("Stock Price")
plt.xlabel("Day")
plt.ylabel("Price")
plt.show()


# Data Analysis:

print("\nLowest Price:-", df["Price"].min())
print("Hihgt Price:-",df["Price"].max())
print("Average Price:-",df["Price"].mean())


# Moving Average (Real Style)

price = df["Price"].values

ma = np.convolve(price, np.ones(3)/3, mode='valid')

plt.plot(df["Day"], price, label="Price", marker='o', color='green')
plt.plot(df["Day"][2:], ma, label="Moving Avg", marker='o', color="red", linestyle='--')

plt.title("Stock Price")
plt.xlabel("Day")
plt.ylabel("Price")

plt.legend()
plt.grid()

plt.show()