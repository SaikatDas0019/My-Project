# ==================================================
# 1. Import Required Libraries
# ==================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ==================================================
# 2. Load for Excel file
# ==================================================
print("="*50)
print("Data Loding...")
print("="*50)
df = pd.read_excel(r"C:\Users\nd460\OneDrive\Desktop\PYTJON_FILE\Real World Data Analysis\df.xlsx")
print("="*50)
print("✅ Data Loaded successfully")
print("="*50)


# ==================================================
# 3. Data's Information
# ==================================================
print("="*50)
print("ℹ️  Data's Information")
print("="*50)
print("\n1st 20 Rows:-\n",df.head(20))
print("\nℹ️  Data's Describe:-\n",df.describe())
print("\n",df.info())
print("\n🟢 Null Cell:-\n",df.isnull().sum())
print("\n🟢 Duplicate Datas:-",df.duplicated().sum())


# ==================================================
# 4. Type Casting
# ==================================================
print("="*50)
print("Type Changing...")
print("="*50)
"""
data["S. No."].astype(int)
data["DISCOUNTED_PRICE"].astype(float)
data["ACTUAL_PRICE"].astype(float)
data["DISCOUNT_PERCENTAGE"].astype(float)
data["RATING"].astype(float)
data["RATING_COUNT"].astype(float)

data.to_excel("df.xlsx")
"""
print("="*50)
print("✅ Type Changed successfully")
print("="*50)


# ==================================================
# 5. Fill Null Cell
# ==================================================
print('='*50)
print("\n🛠️  filling Null Cell...")
print('='*50)
df["RATING"] = df["RATING"].fillna(df["RATING"].mean())
df["RATING_COUNT"] = df["RATING_COUNT"].fillna(df["RATING_COUNT"].mean())
print('='*50)
print("✅ Filled Null Cell successfully.")
print('='*50)


# ==================================================
# 6. Last 30 Day's Data
# ==================================================
df1 = df.iloc[-30:,:]
print("\n🟢 Last 30 Day's Data:-\n",df1)


# ==================================================
# 7. Overall Statistics
# ==================================================
print('='*50)
print("🟢 Overall Statistics")
print('='*50, "\n")

print('🔶 Highest Price Product:-', df["ACTUAL_PRICE"].max())
print("🔶 Lowest Price Product:-", df["ACTUAL_PRICE"].min())
print("🔶 Total Sale:-", df["DISCOUNTED_PRICE"].sum())
print("🔶 Average Discount:-", df["DISCOUNT_PERCENTAGE"].mean(), "%")
print("🔶 Average Rating:-", df['RATING'].mean())


print("="*50)
print("✅ All Data Analysis Complete.")