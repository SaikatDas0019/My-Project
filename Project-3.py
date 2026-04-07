import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_excel(r"C:\Users\nd460\OneDrive\Desktop\PYTJON FILE\Real World Data Analysis\Shope Data.xlsx")

# df["EMA_5"] = df["Total Sales"].ewm(span=5).mean()

# df.to_excel(r"C:\Users\nd460\OneDrive\Desktop\PYTJON FILE\Real World Data Analysis\Shope Data.xlsx", index=False)

df1 = df.iloc[-30:,:].reset_index(drop=True)
print(df1)

# Profit Data
profit_data = df1[df1["Profit|Loss"] == "Profit"]

# Loss Data
loss_data = df1[df1["Profit|Loss"] == "Loss"]

# Diffarence color Graph
plt.scatter(profit_data["Day"], profit_data["Total Profit"], color="green", label="Profit")
plt.scatter(loss_data["Day"], loss_data["Total Profit"], color="red", label="Loss")

plt.plot(df1["Day"], df1["Total Sales"], label="Sales", linewidth=2)
plt.plot(df1["Day"], df1["Total Profit"], label="Total Profit", linewidth=2)

plt.plot(df1["Day"], df1["EMA_5"], label="EMA 5", linestyle="--")

plt.legend()
plt.title("Total Profit|loss")
plt.xlabel("Day")
plt.ylabel("Profit|Loss")
plt.show()
