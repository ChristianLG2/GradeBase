import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to the database
conn = sqlite3.connect("university.db")

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("🎓 University Student Performance Dashboard")

menu = ["Overview", "Grade Distribution", "Attendance Summary", "Assignment Averages", "Top Performers", "Student Report"]
choice = st.sidebar.selectbox("Select Report", menu)

if choice == "Overview":
    st.subheader("📊 Overview of Data")
    student_count = pd.read_sql("SELECT COUNT(*) AS count FROM student", conn)["count"][0]
    course_count = pd.read_sql("SELECT COUNT(*) AS count FROM course", conn)["count"][0]
    assignment_count = pd.read_sql("SELECT COUNT(*) AS count FROM assignments", conn)["count"][0]
    st.metric("Students", student_count)
    st.metric("Courses", course_count)
    st.metric("Assignments", assignment_count)

elif choice == "Grade Distribution":
    st.subheader("📈 Grade Distribution")
    df = pd.read_sql("""
        SELECT grade, COUNT(*) AS count FROM grades GROUP BY grade
    """, conn)
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="grade", y="count", ax=ax, palette="viridis")
    ax.set_title("Grade Distribution")
    st.pyplot(fig)

elif choice == "Attendance Summary":
    st.subheader("📊 Attendance Summary")
    df = pd.read_sql("""
        SELECT status, COUNT(*) AS count FROM attendance GROUP BY status
    """, conn)
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="status", y="count", ax=ax, palette="coolwarm")
    ax.set_title("Attendance Summary")
    st.pyplot(fig)

elif choice == "Assignment Averages":
    st.subheader("📝 Average Scores per Assignment")
    df = pd.read_sql("""
        SELECT a.title, AVG(s.score) AS average_score
        FROM assignment_submissions s
        JOIN assignments a ON a.assignmentId = s.assignmentId
        GROUP BY a.title
    """, conn)
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=df, x="title", y="average_score", ax=ax, palette="crest")
    ax.set_title("Average Scores per Assignment")
    plt.xticks(rotation=45)
    st.pyplot(fig)

elif choice == "Top Performers":
    st.subheader("🏅 Top Performing Students")
    grade_points = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
    df = pd.read_sql("""
        SELECT s.studentId, s.studentFirstName || ' ' || s.studentLastName AS fullName, g.grade
        FROM grades g
        JOIN student s ON s.studentId = g.studentId
    """, conn)
    df["points"] = df["grade"].map(grade_points)
    gpa_df = df.groupby("fullName")["points"].mean().reset_index().sort_values(by="points", ascending=False)
    st.dataframe(gpa_df.rename(columns={"points": "Average Grade Points"}))

elif choice == "Student Report":
    st.subheader("📘 View Individual Student Report")
    students = pd.read_sql("SELECT studentId, studentFirstName || ' ' || studentLastName AS name FROM student", conn)
    selected_id = st.selectbox("Select Student", students["studentId"], format_func=lambda x: students.loc[students["studentId"] == x, "name"].values[0])

    st.write("### Grades")
    grades = pd.read_sql("""
        SELECT c.courseName, g.grade
        FROM grades g
        JOIN section s ON s.sectionId = g.sectionId
        JOIN course c ON c.courseId = s.courseId
        WHERE g.studentId = ?
    """, conn, params=(selected_id,))
    st.dataframe(grades)

    st.write("### Attendance")
    attendance = pd.read_sql("""
        SELECT date, status
        FROM attendance
        WHERE studentId = ?
        ORDER BY date
    """, conn, params=(selected_id,))
    st.dataframe(attendance)

    st.write("### Assignment Submissions")
    submissions = pd.read_sql("""
        SELECT a.title, s.score
        FROM assignment_submissions s
        JOIN assignments a ON a.assignmentId = s.assignmentId
        WHERE s.studentId = ?
    """, conn, params=(selected_id,))
    st.dataframe(submissions)

