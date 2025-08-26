import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to database
conn = sqlite3.connect("university.db")


def grade_distribution():
    df = pd.read_sql_query("""
        SELECT grade, COUNT(*) AS count
        FROM grades
        GROUP BY grade
    """, conn)
    plt.figure(figsize=(6, 4))
    sns.barplot(data=df, x="grade", y="count", palette="viridis")
    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()


def attendance_summary():
    df = pd.read_sql_query("""
        SELECT status, COUNT(*) AS count
        FROM attendance
        GROUP BY status
    """, conn)
    plt.figure(figsize=(6, 4))
    sns.barplot(data=df, x="status", y="count", palette="coolwarm")
    plt.title("Attendance Summary")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()


def average_assignment_scores():
    df = pd.read_sql_query("""
        SELECT a.title, AVG(s.score) AS average_score
        FROM assignment_submissions s
        JOIN assignments a ON a.assignmentId = s.assignmentId
        GROUP BY a.title
    """, conn)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="title", y="average_score", palette="crest")
    plt.title("Average Scores per Assignment")
    plt.xlabel("Assignment")
    plt.ylabel("Average Score")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def top_performers():
    grade_points = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
    df = pd.read_sql_query("""
        SELECT s.studentId, s.studentFirstName || ' ' || s.studentLastName AS fullName, g.grade
        FROM grades g
        JOIN student s ON s.studentId = g.studentId
    """, conn)
    df["points"] = df["grade"].map(grade_points)
    top_df = df.groupby("fullName")["points"].mean().reset_index().sort_values(by="points", ascending=False)
    print("\n🏅 Top Performers by Average Grade:")
    print(top_df.head())


def absence_report():
    df = pd.read_sql_query("""
        SELECT s.studentId, s.studentFirstName || ' ' || s.studentLastName AS fullName, COUNT(*) AS absences
        FROM attendance a
        JOIN student s ON s.studentId = a.studentId
        WHERE a.status = 'Absent'
        GROUP BY s.studentId
        ORDER BY absences DESC
    """, conn)
    print("\n🚫 Students with Most Absences:")
    print(df if not df.empty else "No absences recorded.")


def view_student_performance(student_id):
    print(f"\n📘 Performance Report for Student ID {student_id}:")

    grades = pd.read_sql_query("""
        SELECT c.courseName, g.grade
        FROM grades g
        JOIN section s ON s.sectionId = g.sectionId
        JOIN course c ON c.courseId = s.courseId
        WHERE g.studentId = ?
    """, conn, params=(student_id,))
    print("\nGrades:")
    print(grades if not grades.empty else "No grades found.")

    attendance = pd.read_sql_query("""
        SELECT date, status
        FROM attendance
        WHERE studentId = ?
        ORDER BY date
    """, conn, params=(student_id,))
    print("\nAttendance:")
    print(attendance if not attendance.empty else "No attendance found.")

    submissions = pd.read_sql_query("""
        SELECT a.title, s.score
        FROM assignment_submissions s
        JOIN assignments a ON a.assignmentId = s.assignmentId
        WHERE s.studentId = ?
    """, conn, params=(student_id,))
    print("\nAssignment Scores:")
    print(submissions if not submissions.empty else "No submissions found.")


# Uncomment below to test functions individually
# grade_distribution()
# attendance_summary()
# average_assignment_scores()
# top_performers()
# absence_report()
# view_student_performance(1)

# conn.close() is intentionally left open for module use.

