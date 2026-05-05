# ==================================================
# 1. Import required libreries
# ==================================================
import matplotlib.pyplot as plt
import pandas as pd

def alt(self):
    if self == '':
        self = 0
    else:
        try:
            self = int(self)
        except ValueError:
            self = 0

# ==================================================
# 2. User Information
# ==================================================
name = input("Enter your name: ").strip() or "Saikat Das"
roll = input("Enter your Roll No.: ").strip()
alt(roll)


print("="*50)
print("📑 Enter your 10th Marks")
print("="*50)

beng = int(input("🟢 Bengali Mark: ") or 72)
alt(beng)
eng = int(input("🟢 English Mark: ") or 77)
alt(eng)
math = int(input("🟢 Math Mark: ") or 70)
alt(math)
ph_sc = int(input("🟢 Physical Science Mark: ") or 75)
alt(ph_sc)
life_sc = int(input("🟢 Life Science Mark: ") or 80)
alt(life_sc)
his = int(input("🟢 History Mark: ") or 54)
alt(his)
geo = int(input("🟢 Geography Mark: ") or 71)
alt(geo)

# ==================================================
# 3. Grade Divition
# ==================================================
def grade(mark):
    if mark >= 90:
        return "AA"
    elif mark >= 80 and mark < 90:
        return "A+"
    elif mark >= 60 and mark < 80:
        return "A"
    elif mark >= 45 and mark < 60:
        return "B+"
    elif mark >= 35 and mark < 45:
        return "B"
    elif mark >= 25 and mark < 35:
        return "C"
    elif mark < 25:
        return "D"

# ==================================================
# 4. Marksheet in DataFrame
# ==================================================
marks = {
    "Subject" : ["Bengali", "English", "Math", "Physical Sc.", "Life Sc.", "History", "Geography"],
    "Written" : [beng, eng, math, ph_sc, life_sc, his, geo],
    "Project" : 10,
    "Total" : [beng+10, eng+10, math+10, ph_sc+10, life_sc+10, his+10, geo+10],
    "Grade" : [grade(beng+10), grade(eng+10), grade(math+10), grade(ph_sc+10), grade(life_sc+10), grade(his+10), grade(geo+10)]
}

df = pd.DataFrame(marks)

# ==================================================
# 5. Overwell Statistics
# ==================================================
print("="*50)
print("❇️ Overwell Statistics")
print("="*50)

print("""🔶 Full Marks:
      1. Written: 90
      2. Project: 10
      3. Total: 100""")

print("\nName:-",name)
print("Roll:-",roll)
print("\n🔶 Marksheet:")
print(df)

total_marks = df['Total'].sum()
percentage = total_marks*100/700
grade0 = grade(percentage)
print("\n🔶 Total Marks:-", total_marks)
print("🔶 Percentage:-", percentage)
print("🔶 Grade:-", grade0)

# ==================================================
# 6. 🧐Data Vesualisation
# ==================================================
print('='*50)
print("Data Vesualising...")
print('='*50)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].barh(df['Subject'], df["Total"])
axes[0].set_title("Total Marks")

print("✅ 1st Chart Created")

grade_count = df['Grade'].value_counts()
axes[1].pie(grade_count.values, labels=grade_count.index, autopct='%1.1f%%')
axes[1].set_title("Grade")

print("✅ 2nd Chart Created")

plt. tight_layout()
plt.show()

print('='*50)
print("✅ All Vesualisation Complated.")
print('='*50)