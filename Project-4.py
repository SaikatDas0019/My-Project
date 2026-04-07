import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


df = pd.read_excel(r"C:\Users\nd460\OneDrive\Desktop\PYTJON FILE\Real World Data Analysis\df.xlsx")

"""
data["S. No."].astype(int)
data["DISCOUNTED_PRICE"].astype(float)
data["ACTUAL_PRICE"].astype(float)
data["DISCOUNT_PERCENTAGE"].astype(float)
data["RATING"].astype(float)
data["RATING_COUNT"].astype(float)

data.to_excel("df.xlsx")
"""

# df = data.iloc[:30,:]

# Rating Graph
plt.plot(df["S. No."], df["RATING"], label="Rating", color="orange", marker='o')
plt.title("Product Rating")
plt.xlabel("S. No.")
plt.xlabel("Rating & Rating Count")
plt.grid()
plt.show()

# Rating Count Graph
plt.plot(df["S. No."], df["RATING_COUNT"], label="Rating Count", color="red", marker='o')
plt.title("Product Rating Count")
plt.xlabel("S. No.")
plt.xlabel("Rating Count")
plt.grid()
plt.show()

# Price Graph
plt.plot(df["S. No."], df["DISCOUNTED_PRICE"], label="DISCOUNTED PRICE", color="orange", marker='o')
plt.plot(df["S. No."], df["ACTUAL_PRICE"], label="ACTUAL PRICE", color="green", marker='o')
plt.legend()
plt.title("PRICE")
plt.xlabel("S. No.")
plt.xlabel("PRICE")
plt.grid()
plt.show()