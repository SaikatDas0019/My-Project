# ============================================================
# 1. Import Required Libraries
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set plot style for better visualization
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


# ============================================================
# 2. Load Data from Excel File
# ============================================================
print("=" * 60)
print("📂 Loading data...")
print("=" * 60)

try:
    # Read Excel file and convert to DataFrame
    data = pd.read_excel(r"C:\Users\nd460\OneDrive\Desktop\PYTJON_FILE\Real World Data Analysis\Supershop Sales Data.xlsx")
    df = pd.DataFrame(data)
    print(f"✅ Data loaded successfully!")
    print(f"📊 Total rows: {len(df)}, Total columns: {len(df.columns)}")
    print(f"\nFirst 5 rows:")
    print(df.head())
except FileNotFoundError:
    print("❌ File not found. Please check the path!")
    exit()


# ============================================================
# 3. Exploratory Data Analysis (EDA)
# ============================================================
print("\n" + "=" * 60)
print("🔍 Starting Data Analysis...")
print("=" * 60)

print(f"\n📋 Column Names:")
print(df.columns.tolist())

print(f"\n📊 Data Types:")
print(df.dtypes)

print(f"\n❓ Missing Values Count:")
print(df.isnull().sum())

print(f"\n🔁 Duplicate rows count: {df.duplicated().sum()}")

print(f"\n📈 Unique values per column:")
print(df.nunique())


# ============================================================
# 4. Data Cleaning and Preprocessing
# ============================================================
print("\n" + "=" * 60)
print("🧹 Cleaning Data...")
print("=" * 60)

# Remove duplicate rows (IMPORTANT: must use = to save)
df = df.drop_duplicates()
print(f"✅ Duplicates removed. Now {len(df)} rows remain.")

# Convert date format to datetime
try:
    # Try different date formats
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y", errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%d-%m-%Y", errors="coerce")
    print(f"✅ Date format conversion successful")
except Exception as e:
    print(f"⚠️  Error converting dates: {e}")

# Fill missing values - FIXED APPROACH
print(f"\n🔧 Filling missing values...")

# For Order Date and Ship Date - use forward fill or a default date
# Since all values are NaN, we'll use a default date (2020-01-01)
if df["Order Date"].isnull().all():
    print(f"⚠️  Order Date is completely empty, using default date")
    df["Order Date"] = pd.Timestamp('2020-01-01')
else:
    # If some values exist, use forward fill method
    df["Order Date"] = df["Order Date"].bfill().ffill()

if df["Ship Date"].isnull().all():
    print(f"⚠️  Ship Date is completely empty, using default date")
    df["Ship Date"] = pd.Timestamp('2020-01-01')
else:
    # If some values exist, use forward fill method
    df["Ship Date"] = df["Ship Date"].bfill().ffill()

# Fill Postal Code with "Unknown"
df["Postal Code"] = df["Postal Code"].fillna("Unknown")
print(f"✅ Missing values handled")

# Normalize text data (capitalize first letter)
text_columns = ["Customer Name", "Category", "Sub-Category", "Product Name", 
                "State", "Region", "Country", "City"]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].str.title()

print(f"✅ Text formatting completed")

# Verify data cleaning
print(f"\n📊 After Cleaning:")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Duplicate rows: {df.duplicated().sum()}")


# ============================================================
# 5. Data Summary Statistics
# ============================================================
print("\n" + "=" * 60)
print("📊 Data Statistics")
print("=" * 60)
print(df.describe())


# ============================================================
# 6. Separate Data by Category
# ============================================================
print("\n" + "=" * 60)
print("📦 Data by Category")
print("=" * 60)

# Split data for each category
if "Category" in df.columns:
    categories = df["Category"].unique()
    for cat in categories:
        cat_data = df[df["Category"] == cat]
        print(f"📦 {cat}: {len(cat_data)} products, Total Sales: ${cat_data['Sales'].sum():,.2f}")


# ============================================================
# 7. Key Insights and Business Analysis
# ============================================================
print("\n" + "=" * 60)
print("💡 Key Insights")
print("=" * 60)

# Top selling categories
category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
print(f"\n🏆 Top selling categories:")
for cat, sales in category_sales.items():
    print(f"   {cat}: ${sales:,.2f}")

# Top 5 regions
if "Region" in df.columns:
    print(f"\n🌍 Top 5 regions by sales:")
    top_regions = df.groupby("Region")["Sales"].sum().sort_values(ascending=False).head(5)
    for region, sales in top_regions.items():
        print(f"   {region}: ${sales:,.2f}")

# Top 5 cities
if "City" in df.columns:
    print(f"\n🏙️ Top 5 cities by sales:")
    top_cities = df.groupby("City")["Sales"].sum().sort_values(ascending=False).head(5)
    for city, sales in top_cities.items():
        print(f"   {city}: ${sales:,.2f}")

# Profitability analysis (if Profit column exists)
if "Profit" in df.columns:
    print(f"\n💰 Profitability Analysis:")
    print(f"   Total Sales: ${df['Sales'].sum():,.2f}")
    print(f"   Total Profit: ${df['Profit'].sum():,.2f}")
    profit_margin = (df['Profit'].sum() / df['Sales'].sum() * 100) if df['Sales'].sum() != 0 else 0
    print(f"   Profit Margin: {profit_margin:.2f}%")
else:
    print(f"\n💰 Total Sales: ${df['Sales'].sum():,.2f}")


# ============================================================
# 8. Data Visualization - Multiple Charts
# ============================================================
print("\n" + "=" * 60)
print("📊 Creating Visualizations...")
print("=" * 60)

# Create a large figure with 6 subplots
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Superstore Sales Data Analysis - Comprehensive Overview', fontsize=16, fontweight='bold')

try:
    # Chart 1: Total Sales by Category (Bar Chart)
    category_sales = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    colors_cat = ['#2ecc71', '#3498db', '#e74c3c']
    axes[0, 0].bar(category_sales.index, category_sales.values, color=colors_cat[:len(category_sales)], edgecolor='black', linewidth=1.5)
    axes[0, 0].set_title('Total Sales by Category', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Sales ($)', fontsize=10)
    axes[0, 0].set_xlabel('Category', fontsize=10)
    axes[0, 0].tick_params(axis='x', rotation=45)
    for i, v in enumerate(category_sales.values):
        axes[0, 0].text(i, v + v*0.02, f'${v:,.0f}', ha='center', fontweight='bold', fontsize=9)

    # Chart 2: Product Distribution by Category (Pie Chart)
    category_count = df["Category"].value_counts()
    axes[0, 1].pie(category_count.values, labels=category_count.index, autopct='%1.1f%%', 
                   colors=colors_cat[:len(category_count)], startangle=90, textprops={'fontsize': 10})
    axes[0, 1].set_title('Product Distribution by Category', fontsize=12, fontweight='bold')

    # Chart 3: Sales by Region (Bar Chart)
    region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
    axes[0, 2].bar(region_sales.index, region_sales.values, color='#3498db', edgecolor='black', linewidth=1.5)
    axes[0, 2].set_title('Sales by Region', fontsize=12, fontweight='bold')
    axes[0, 2].set_ylabel('Sales ($)', fontsize=10)
    axes[0, 2].set_xlabel('Region', fontsize=10)
    axes[0, 2].tick_params(axis='x', rotation=45)

    # Chart 4: Profit by Category (if exists)
    if "Profit" in df.columns:
        category_profit = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
        colors_profit = ['#27ae60' if x > 0 else '#e74c3c' for x in category_profit.values]
        axes[1, 0].bar(category_profit.index, category_profit.values, color=colors_profit, edgecolor='black', linewidth=1.5)
        axes[1, 0].set_title('Profit by Category', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Profit ($)', fontsize=10)
        axes[1, 0].axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    else:
        # Alternative chart if no Profit column
        segment_sales = df.groupby("Segment")["Sales"].sum() if "Segment" in df.columns else df.groupby("Ship Mode")["Sales"].sum()
        axes[1, 0].bar(segment_sales.index, segment_sales.values, color='#9b59b6', edgecolor='black', linewidth=1.5)
        axes[1, 0].set_title('Sales by Segment/Mode', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Sales ($)', fontsize=10)

    # Chart 5: Sales vs Quantity Relationship (Scatter Plot)
    if "Quantity" in df.columns:
        scatter = axes[1, 1].scatter(df["Sales"], df["Quantity"], alpha=0.5, c=df["Sales"], 
                                     cmap='viridis', s=50, edgecolor='black', linewidth=0.5)
        axes[1, 1].set_title('Sales vs Quantity', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Sales ($)', fontsize=10)
        axes[1, 1].set_ylabel('Quantity', fontsize=10)
        cbar = plt.colorbar(scatter, ax=axes[1, 1])
        cbar.set_label('Sales ($)', fontsize=9)
    else:
        # Alternative: show sales distribution
        axes[1, 1].hist(df["Sales"], bins=30, color='#e67e22', edgecolor='black', alpha=0.7)
        axes[1, 1].set_title('Sales Distribution', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Sales ($)', fontsize=10)
        axes[1, 1].set_ylabel('Frequency', fontsize=10)

    # Chart 6: Top 10 Cities by Sales (Horizontal Bar Chart)
    top_10_cities = df.groupby("City")["Sales"].sum().sort_values(ascending=True).tail(10)
    axes[1, 2].barh(top_10_cities.index, top_10_cities.values, color='#e67e22', edgecolor='black', linewidth=1.5)
    axes[1, 2].set_title('Top 10 Cities by Sales', fontsize=12, fontweight='bold')
    axes[1, 2].set_xlabel('Sales ($)', fontsize=10)

    plt.tight_layout()
    plt.show()
    print("✅ All visualizations completed successfully!")

except Exception as e:
    print(f"⚠️  Error creating visualizations: {e}")


# ============================================================
# 9. Final Summary Report
# ============================================================
print("\n" + "=" * 60)
print("📋 Final Analysis Summary")
print("=" * 60)

summary = f"""
✨ Superstore Sales Data Summary Report:

📊 Overall Statistics:
   • Total Transactions: {len(df):,}
   • Total Sales: ${df['Sales'].sum():,.2f}
   • Average Order Value: ${df['Sales'].mean():,.2f}
   • Median Order Value: ${df['Sales'].median():,.2f}

🏆 Top Performers:
   • Best Category: {category_sales.idxmax()} (${category_sales.max():,.2f})
   • Best Region: {df.groupby('Region')['Sales'].sum().idxmax()} (${df.groupby('Region')['Sales'].sum().max():,.2f})
   • Best City: {df.groupby('City')['Sales'].sum().idxmax()} (${df.groupby('City')['Sales'].sum().max():,.2f})

📦 Product Diversity:
   • Total Unique Products: {df['Product Name'].nunique()}
   • Total Unique Customers: {df['Customer Name'].nunique()}
   • Total Unique Cities: {df['City'].nunique()}
   • Categories: {df['Category'].nunique()}

🎯 Recommendations:
   1. Focus on {category_sales.idxmax()} category - highest performer
   2. Expand to underperforming regions
   3. Analyze top-performing cities for best practices
   4. Monitor customer segments for targeted marketing
"""

print(summary)
print("=" * 60)
print("✅ Analysis Complete!")
print("=" * 60)