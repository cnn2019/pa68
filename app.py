import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# โหลดข้อมูล
df = pd.read_csv("grades.csv")
st.title("📊 สรุปผลสัมฤทธิ์ทางการเรียน (รายวิชา)")

# -----------------------------
# คำนวณ GPA เฉลี่ยต่อวิชา
# -----------------------------
grade_cols = ["0","1","1.5","2","2.5","3","3.5","4"]
weights = [0,1,1.5,2,2.5,3,3.5,4]

for col in grade_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["GPA_avg"] = (df[grade_cols] * weights).sum(axis=1) / df["จำนวนนักเรียน"]

# -----------------------------
# แสดงผล: GPA เฉลี่ย
# -----------------------------
st.subheader("📈 ค่าเฉลี่ย GPA ต่อวิชา")
fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="GPA_avg", y="รายวิชา", data=df, ax=ax, palette="Blues_r")
st.pyplot(fig)

# -----------------------------
# แสดงผล: การกระจายเกรด (Stacked Bar)
# -----------------------------
st.subheader("📊 การกระจายเกรดรายวิชา")
df_melt = df.melt(id_vars=["รายวิชา"], value_vars=grade_cols, 
                  var_name="Grade", value_name="Count")
pivot = df_melt.pivot(index="รายวิชา", columns="Grade", values="Count")
pivot.fillna(0, inplace=True)

pivot.plot(kind="barh", stacked=True, figsize=(10,6), colormap="tab20c")
st.pyplot(plt)

# -----------------------------
# Heatmap
# -----------------------------
st.subheader("🔥 Heatmap การกระจายเกรด")
fig, ax = plt.subplots(figsize=(10,6))
sns.heatmap(df[grade_cols], annot=True, fmt="g", cmap="YlGnBu", cbar=True,
            yticklabels=df["รายวิชา"])
st.pyplot(fig)
