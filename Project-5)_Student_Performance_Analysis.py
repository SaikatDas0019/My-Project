# ==================================================
# 1. Import Required Libraries
# ==================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ==================================================
# Load Data from Excel file
# ==================================================
print("="*50)
print("Loading Data...")
print("="*50)

df = pd.read_excel(r"C:\Users\nd460\OneDrive\Desktop\PYTJON_FILE\Real World Data Analysis\Student_Performance.xlsx")

print("="*50)
print("✅ Data Loaded Successfully")
print("="*50)


# ==================================================
# This Data's information
# ==================================================
print("="*50)
print("This Data's information")
print("="*50)
print(df.describe())
print(df.info())
print("Null Cell:-\n", df.isnull().sum())
print("Duplicate Rows:-", df.duplicated().sum())


# ==================================================
# Data Cleaning
# ==================================================
print("="*50)
print("Cleaning data...")
print("="*50)
df = df.drop_duplicates()
print("✅ Deleted Duplicate Rows successfully")

df['Math'] = df['Math'].fillna(df['Math'].mean())
df['English'] = df['English'].fillna(df['English'].mean())
df['Science'] = df['Science'].fillna(df['Science'].mean())
df['History'] = df['History'].fillna(df['History'].mean())

print("✅ Filled Null cell successfully")

print("="*50)
print("✅ Data cleaned successfully")
print("="*50)


# ==================================================
# New colume add
# ==================================================
print("="*50)
print("New column adding...")
print("="*50)

df["Total Marks"] = df["Math"] + df["English"] + df["Science"] + df["History"]
df["Percentage"] = df["Total Marks"]*100/400
df["Average Marks"] = df["Total Marks"]/4

def grade (per):
    if per >= 90:
        return "AA"
    elif per >= 80 and per < 90:
        return "A+"
    elif per >= 60 and per < 80:
        return "A"
    elif per >= 45 and per < 60:
        return "B+"
    elif per >= 35 and per < 45:
        return "B"
    elif per >= 25 and per < 35:
        return "C"
    else:
        return "D"

df["Grade"] = df["Percentage"].apply(grade)

print("="*50)
print("✅ New column added")
print("="*50)


# ==================================================
# Hilight Student List
# ==================================================
# Top 10 Students
top_10 = df.nlargest(10, "Total Marks")[["Roll No", "Student Name", "Class", "Total Marks", "Percentage"]]
print("\nTop 10 Student List:-\n", top_10)

# Bottom 5 Students
bottom_10 = df.nsmallest(10, "Total Marks")[["Roll No", "Student Name", "Class", "Total Marks", "Percentage"]]
print("\nBottom 10 Student List:-\n", bottom_10)

# Top student in every subject
print("\nপ্রতিটি বিষয়ে শীর্ষ ছাত্র")
print("Highest in Math:-", df.loc[df["Math"].idxmax(), "Student Name"], "(", df["Math"].max(), "Mark)")
print("Highest in English:-", df.loc[df["English"].idxmax(), "Student Name"], "(", df["English"].max(), "Mark)")
print("Highest in Science:-", df.loc[df["Science"].idxmax(), "Student Name"], "(", df["Science"].max(), "Mark)")
print("Highest in History:-", df.loc[df["History"].idxmax(), "Student Name"], "(", df["History"].max(), "Mark)")

# Lowest marks in each subject
print("\nপ্রতিটি বিষয়ে সবচেয়ে কম মার্ক")
print("Lowest in Math:-", df.loc[df["Math"].idxmin(), "Student Name"], "(", df["Math"].min(), "Marks)")
print("Lowest in English:-", df.loc[df["English"].idxmin(), "Student Name"], "(", df["English"].min(), "Marks)")
print("Lowest in Science:-", df.loc[df["Science"].idxmin(), "Student Name"], "(", df["Science"].min(), "Marks)")
print("Lowest in History:-", df.loc[df["History"].idxmin(), "Student Name"], "(", df["History"].min(), "Marks)")

# Average, highest, lowest marks of each class
print("\nপ্রতিটি ক্লাসের গড় মার্ক\n")
print(df.groupby("Class")[["Math", "English", "Science", "History", "Total Marks"]].mean())
print("\nপ্রতিটি ক্লাসের সর্বোচ্চ মার্ক\n")
print(df.groupby("Class")[["Math", "English", "Science", "History", "Total Marks"]].max())
print("\nপ্রতিটি ক্লাসের সর্বনিম্ন মার্ক\n")
print(df.groupby("Class")[["Math", "English", "Science", "History", "Total Marks"]].min())


# ==================================================
# Overall Statistics
# ==================================================
print("\nসামগ্রিক পরিসংখ্যান (Overall Statistics)")
print("Total Student:-", len(df))
print("Highest Marks:-", df["Total Marks"].max())
print("Lowest Marks:-", df["Total Marks"].min())
print("Average Marks:-", df["Total Marks"].mean())


# ==================================================
# Data Visualization - Multiple Charts
# ==================================================
print("\n" + "=" * 60)
print("📊 Creating Visualizations...")
print("=" * 60)


fig, axes = plt.subplots(2, 3, figsize=(18, 10))  # ✅ subplots
fig.suptitle("Student Performance Analysis - Comprehensive Overview", fontsize=16, fontweight='bold')  # ✅ suptitle

# 1st Graph - Top 10 Students
top_10 = df.nlargest(10, "Total Marks")
axes[0, 0].bar(range(len(top_10)), top_10["Total Marks"].values, color='#2ecc71', edgecolor='black')  # ✅ bar + .values
axes[0, 0].set_xticks(range(len(top_10)))
axes[0, 0].set_xticklabels(top_10["Student Name"].values, rotation=45, ha='right')  # ✅ set_xticklabels + .values
axes[0, 0].set_title("Top 10 Students by Total Marks", fontsize=12, fontweight='bold')
axes[0, 0].set_ylabel("Total Marks", fontsize=10)
axes[0, 0].grid(True, alpha=0.3)
print("✅ 1st Graph created")

# 2nd Graph - Grade Distribution
grade_counts = df["Grade"].value_counts()
colors = ['#e74c3c', '#e67e22', '#f39c12', '#f1c40f', '#2ecc71', '#3498db']
axes[0, 1].pie(grade_counts.values, labels=grade_counts.index, autopct='%1.1f%%',
               colors=colors[:len(grade_counts)], startangle=90)
axes[0, 1].set_title('Grade Distribution', fontsize=12, fontweight='bold')
print("✅ 2nd Graph created")

# 3rd Graph - Total Marks Distribution
axes[0, 2].hist(df["Total Marks"].dropna(), bins=15, color='#3498db', edgecolor='black', alpha=0.7)
axes[0, 2].set_title('Total Marks Distribution', fontsize=12, fontweight='bold')
axes[0, 2].set_xlabel('Total Marks', fontsize=10)
axes[0, 2].set_ylabel('Frequency', fontsize=10)
axes[0, 2].grid(True, alpha=0.3)
print("✅ 3rd Graph created")

# 4th Graph - Subject-wise Box Plot
subject_data = [df["Math"].dropna(), df["English"].dropna(), 
                df["Science"].dropna(), df["History"].dropna()]
axes[1, 0].boxplot(subject_data, labels=["Math", "English", "Science", "History"])
axes[1, 0].set_title('Subject-wise Marks Distribution (Box Plot)', fontsize=12, fontweight='bold')
axes[1, 0].set_ylabel('Marks', fontsize=10)
axes[1, 0].grid(True, alpha=0.3)
print("✅ 4th Graph created")

# 5th Graph - Top 10 by Average Marks
top_10_avg = df.nlargest(10, "Average Marks").sort_values("Average Marks")
axes[1, 1].barh(top_10_avg["Student Name"].values, top_10_avg["Average Marks"].values,
                color='#9b59b6', edgecolor='black')
axes[1, 1].set_title('Top 10 Students by Average Marks', fontsize=12, fontweight='bold')
axes[1, 1].set_xlabel('Average Marks', fontsize=10)
axes[1, 1].grid(True, alpha=0.3)
print("✅ 5th Graph created")

# 6th Graph - Math vs English Scatter Plot
scatter = axes[1, 2].scatter(df["Math"].dropna(), df["English"].dropna(), 
                            c=df.loc[df["Math"].notna(), "Total Marks"],
                            cmap='viridis', s=100, alpha=0.6, edgecolor='black')
axes[1, 2].set_title('Math vs English Marks', fontsize=12, fontweight='bold')
axes[1, 2].set_xlabel('Math Marks', fontsize=10)
axes[1, 2].set_ylabel('English Marks', fontsize=10)
cbar = plt.colorbar(scatter, ax=axes[1, 2])
cbar.set_label('Total Marks', fontsize=9)
axes[1, 2].grid(True, alpha=0.3)
print("✅ 6th Graph created")

plt.tight_layout()
plt.show()

print("\n✅ All Visualizations Completed!")