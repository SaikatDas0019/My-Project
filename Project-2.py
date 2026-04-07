import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
np.random.seed(0)

data = {
    "Day" : np.arange(1, 1001),
    "Price" : np.random.randint(80, 150, 1000),
    "Volume" : np.random.randint(1, 100, 1000), 
    "Profit" : np.random.randint(-20, 50, 1000),
    "Catagory" : np.random.choice(["Tech", "Bank", "Auto"], 1000),
    "Rating" : np.random.randint(1, 5, 1000)
}

df = pd.DataFrame(data)
# df.to_excel("Shope Data.xlsx", index=False)
print(df)
"""

df = pd.read_excel(r"C:\Users\nd460\OneDrive\Desktop\PYTJON FILE\Real World Data Analysis\Shope Data.xlsx")

# Data Analysis
print(df)
# print(df.info())
# print(df.describe())
# print(df.isnull().sum())
# print(df.duplicated())
# print(df.nunique())


Auto = df[df["Catagory"] == "Auto"]
Bank = df[df["Catagory"] == "Bank"]
Tech = df[df["Catagory"] == "Tech"]

"""
# Graph
plt.plot(Auto["Day"], Auto["Volume"], marker='o', color='green', label="Auto")
plt.plot(Tech["Day"], Tech["Volume"], marker='o', label="Tech")
plt.plot(Bank["Day"], Bank["Volume"], marker='o', color='black', label="Bank")
plt.legend()
plt.title("Volume")
plt.xlabel("Catagory")
plt.ylabel("Volume")
plt.show()


# Real Graph
ma = np.convolve(Auto["Volume"], np.ones(50)/50, mode="valid")

plt.plot(Auto["Day"], Auto["Volume"], marker='o', color='green', label="Auto")
plt.plot(range(49, len(Auto["Volume"])), ma, label="Auto's Moving Avg", color="red", linestyle="--")
plt.legend()
plt.title("Volume")
plt.xlabel("Catagory")
plt.ylabel("Volume")
plt.show()
"""

df["Total Sales"] = df["Price"] * df["Volume"]
df["Total Profit"] = df["Profit"] * df["Volume"]
df["Profit|Loss"] = df["Profit"].apply(lambda x: "Prifit" if x > 0 else "Loss")
df.to_excel("Shope Data.xlsx", index=False)

DF = df.iloc[-30:,:].reset_index(drop=True)
print(DF)

# Total Sales & Total Profit Graph
sma = np.convolve(DF["Total Sales"], np.ones(5)/5, mode="valid")
pma = np.convolve(DF["Total Profit"], np.ones(5)/5, mode="valid")

plt.plot(DF["Day"], DF["Total Sales"], label="Total Sales", color="green")
plt.plot(DF["Day"][4:], sma, label="Sales's Moving Avg", color="red", linestyle="-.")
plt.plot(DF["Day"], DF["Total Profit"], label="Total Profit", color="black")
plt.plot(DF["Day"][4:], pma, label="Profit's Moving Avg", color="red", linestyle="--")
plt.legend()
plt.title("Total Sales & Profit")
plt.ylabel("Sales & Profit")
plt.xlabel("Day")
plt.show()
