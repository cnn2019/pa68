import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# โหลดข้อมูล
df = pd.read_csv("grades.csv")

st.title("📊 ผลสัมฤทธิ์ทางการเรียน")

# โหมดการดูข้อมูล
view_mode = st.sidebar.radio("เลือกโหมดการดู", ["ภาพรวมทั้งห้อง", "รายบุคคล"])

if view_mode == "ภาพรวมทั้งห้อง":
    st.header("📈 ภาพรวมทั้งห้อง")

    # ค่าเฉลี่ยแต่ละวิชา
    avg_subject = df.drop(columns=["Name"]).mean()

    st.subheader("ค่าเฉลี่ยแต่ละวิชา")
    st.bar_chart(avg_subject)

    st.subheader("Distribution ของค่า GPA เฉลี่ยต่อคน")
    df["GPA"] = df.drop(columns=["Name"]).mean(axis=1)
    fig, ax = plt.subplots()
    sns.histplot(df["GPA"], bins=5, kde=True, ax=ax)
    st.pyplot(fig)

else:
    st.header("👤 รายบุคคล")

    # เลือกชื่อนักเรียน
    student_name = st.selectbox("เลือกนักเรียน", df["Name"])
    student = df[df["Name"] == student_name].iloc[0]

    # แสดงตารางเกรด
    st.subheader("เกรดรายวิชา")
    st.table(student.drop(labels=["Name"]).to_frame("เกรด"))

    # Radar chart
    import numpy as np

    subjects = df.columns[1:]
    values = student[subjects].values
    values = np.append(values, values[0])  # ปิดกราฟ

    angles = np.linspace(0, 2*np.pi, len(subjects), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw={"polar": True})
    ax.plot(angles, values, "o-", linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(subjects)
    ax.set_ylim(0, 4)
    st.pyplot(fig)

    # แสดง GPA ของนักเรียน
    gpa = student[subjects].mean()
    st.metric("GPA", f"{gpa:.2f}")
