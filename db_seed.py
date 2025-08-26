import sqlite3
from datetime import datetime, timedelta
import random

# Connect to SQLite
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# Drop all existing tables if they exist
cursor.executescript("""
DROP TABLE IF EXISTS assignment_submissions;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS enrollment;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS semester;
DROP TABLE IF EXISTS department;
DROP TABLE IF EXISTS college;
""")

# Create tables
cursor.executescript("""
CREATE TABLE college (
    collegeId INTEGER PRIMARY KEY AUTOINCREMENT,
    collegeName TEXT NOT NULL
);

CREATE TABLE department (
    departmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    departmentName TEXT NOT NULL,
    departmentCode TEXT NOT NULL,
    collegeId INTEGER NOT NULL,
    FOREIGN KEY (collegeId) REFERENCES college(collegeId)
);

CREATE TABLE semester (
    semesterId INTEGER PRIMARY KEY AUTOINCREMENT,
    semesterName TEXT NOT NULL,
    semesterYear TEXT NOT NULL
);

CREATE TABLE student (
    studentId INTEGER PRIMARY KEY AUTOINCREMENT,
    studentFirstName TEXT NOT NULL,
    studentLastName TEXT NOT NULL,
    studentGender TEXT CHECK(studentGender IN ('M', 'F')),
    studentCity TEXT NOT NULL,
    studentState TEXT NOT NULL,
    studentDob TEXT NOT NULL
);

CREATE TABLE faculty (
    facultyId INTEGER PRIMARY KEY AUTOINCREMENT,
    facultyLastName TEXT NOT NULL,
    facultyFirstName TEXT NOT NULL
);

CREATE TABLE course (
    courseId INTEGER PRIMARY KEY AUTOINCREMENT,
    courseName TEXT NOT NULL,
    courseNumber INTEGER NOT NULL,
    coursesCredit INTEGER NOT NULL,
    departmentId INTEGER NOT NULL,
    FOREIGN KEY (departmentId) REFERENCES department(departmentId)
);

CREATE TABLE section (
    sectionId INTEGER PRIMARY KEY AUTOINCREMENT,
    sectionNumber INTEGER NOT NULL,
    sectionCapacity INTEGER NOT NULL,
    courseId INTEGER NOT NULL,
    facultyId INTEGER NOT NULL,
    semesterId INTEGER NOT NULL,
    FOREIGN KEY (courseId) REFERENCES course(courseId),
    FOREIGN KEY (facultyId) REFERENCES faculty(facultyId),
    FOREIGN KEY (semesterId) REFERENCES semester(semesterId)
);

CREATE TABLE enrollment (
    sectionId INTEGER NOT NULL,
    studentId INTEGER NOT NULL,
    PRIMARY KEY (sectionId, studentId),
    FOREIGN KEY (sectionId) REFERENCES section(sectionId),
    FOREIGN KEY (studentId) REFERENCES student(studentId)
);

CREATE TABLE grades (
    gradeId INTEGER PRIMARY KEY AUTOINCREMENT,
    studentId INTEGER NOT NULL,
    sectionId INTEGER NOT NULL,
    grade TEXT CHECK(grade IN ('A', 'B', 'C', 'D', 'F')),
    FOREIGN KEY (studentId) REFERENCES student(studentId),
    FOREIGN KEY (sectionId) REFERENCES section(sectionId)
);

CREATE TABLE attendance (
    attendanceId INTEGER PRIMARY KEY AUTOINCREMENT,
    studentId INTEGER NOT NULL,
    sectionId INTEGER NOT NULL,
    date TEXT NOT NULL,
    status TEXT CHECK(status IN ('Present', 'Absent', 'Late')),
    FOREIGN KEY (studentId) REFERENCES student(studentId),
    FOREIGN KEY (sectionId) REFERENCES section(sectionId)
);

CREATE TABLE assignments (
    assignmentId INTEGER PRIMARY KEY AUTOINCREMENT,
    sectionId INTEGER NOT NULL,
    title TEXT NOT NULL,
    maxScore INTEGER NOT NULL,
    dueDate TEXT,
    FOREIGN KEY (sectionId) REFERENCES section(sectionId)
);

CREATE TABLE assignment_submissions (
    submissionId INTEGER PRIMARY KEY AUTOINCREMENT,
    studentId INTEGER NOT NULL,
    assignmentId INTEGER NOT NULL,
    score INTEGER,
    FOREIGN KEY (studentId) REFERENCES student(studentId),
    FOREIGN KEY (assignmentId) REFERENCES assignments(assignmentId)
);
""")

# Seed Data

# Colleges
cursor.executemany("""
INSERT INTO college (collegeName) VALUES (?)
""", [
    ("College of Physical Science and Engineering",),
    ("College of Business and Communication",),
    ("College of Language and Letters",)
])

# Departments
cursor.executemany("""
INSERT INTO department (departmentName, departmentCode, collegeId) VALUES (?, ?, ?)
""", [
    ("Computer Information Technology", "CIT", 1),
    ("Economics", "ECON", 2),
    ("Humanities and Philosophy", "HUM", 3)
])

# Faculty
cursor.executemany("""
INSERT INTO faculty (facultyFirstName, facultyLastName) VALUES (?, ?)
""", [
    ("Marty", "Morring"),
    ("Nate", "Nathan"),
    ("Ben", "Barrus"),
    ("John", "Jensen"),
    ("Bill", "Barney")
])

# Semesters
cursor.executemany("""
INSERT INTO semester (semesterName, semesterYear) VALUES (?, ?)
""", [
    ("Fall", "2019"),
    ("Winter", "2018")
])

# Courses
cursor.executemany("""
INSERT INTO course (courseName, courseNumber, coursesCredit, departmentId) VALUES (?, ?, ?, ?)
""", [
    ("Intro to Databases", 111, 3, 1),
    ("Econometrics", 388, 4, 2),
    ("Microeconomics", 150, 3, 2),
    ("Classical Heritage", 376, 2, 3)
])

# Students
students = [
    ("Paul", "Miller", "M", "Dallas", "TX", "1996-02-22"),
    ("Katie", "Smith", "F", "Provo", "UT", "1995-07-22"),
    ("Kelly", "Jones", "F", "Provo", "UT", "1998-06-22"),
    ("Devon", "Merril", "M", "Mesa", "AZ", "2000-07-22"),
    ("Mandy", "Murdock", "F", "Topeka", "KS", "1996-11-22"),
    ("Alece", "Adams", "F", "Rigby", "ID", "1997-05-22"),
    ("Bryce", "Carlson", "M", "Bozeman", "MT", "1997-11-22"),
    ("Preston", "Larsen", "M", "Decatur", "TN", "1996-09-22"),
    ("Julia", "Madsen", "F", "Rexburg", "ID", "1998-09-22"),
    ("Susan", "Sorensen", "F", "Mesa", "AZ", "1998-08-09")
]
cursor.executemany("""
INSERT INTO student (studentFirstName, studentLastName, studentGender, studentCity, studentState, studentDob)
VALUES (?, ?, ?, ?, ?, ?)
""", students)

# Sections
sections = [
    (1, 30, 1, 1, 1), (1, 50, 3, 2, 1), (2, 50, 3, 2, 1),
    (1, 35, 2, 3, 1), (1, 30, 4, 4, 1), (2, 30, 1, 1, 2),
    (3, 35, 1, 5, 2), (1, 50, 3, 2, 2), (2, 50, 3, 2, 2),
    (1, 30, 4, 4, 2)
]
cursor.executemany("""
INSERT INTO section (sectionNumber, sectionCapacity, courseId, facultyId, semesterId)
VALUES (?, ?, ?, ?, ?)
""", sections)

# Enrollments
enrollments = [
    (7, 6), (6, 7), (8, 7), (10, 7), (5, 4), (9, 9),
    (4, 2), (4, 3), (4, 5), (5, 5), (1, 1), (3, 1), (9, 8), (6, 10)
]
cursor.executemany("""
INSERT INTO enrollment (sectionId, studentId) VALUES (?, ?)
""", enrollments)

# Grades
grades = [
    (6, 7, 'A'), (7, 6, 'B'), (7, 8, 'A'), (7, 10, 'A'),
    (9, 9, 'C'), (8, 9, 'B'), (10, 6, 'B'), (1, 1, 'A'),
    (2, 2, 'B'), (3, 3, 'C'), (4, 4, 'B'), (5, 5, 'A')
]
cursor.executemany("""
INSERT INTO grades (studentId, sectionId, grade)
VALUES (?, ?, ?)
""", grades)

# Attendance
statuses = ['Present', 'Absent', 'Late']
start_date = datetime.strptime("2024-09-02", "%Y-%m-%d")
attendance = []

for day in range(5):
    date_str = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
    for student_id in [1, 2, 3, 4, 5]:
        attendance.append((student_id, 1, date_str, random.choice(statuses)))

cursor.executemany("""
INSERT INTO attendance (studentId, sectionId, date, status)
VALUES (?, ?, ?, ?)
""", attendance)

# Assignments
assignments = [
    (1, "Homework 1", 100, "2024-09-05"),
    (1, "Project 1", 150, "2024-09-10"),
    (1, "Midterm Exam", 200, "2024-09-15")
]
cursor.executemany("""
INSERT INTO assignments (sectionId, title, maxScore, dueDate)
VALUES (?, ?, ?, ?)
""", assignments)

# Assignment Submissions
assignment_submissions = []
for assignment_id in [1, 2, 3]:
    for student_id in [1, 2, 3, 4, 5]:
        score = random.randint(50, 100) if assignment_id != 3 else random.randint(120, 200)
        assignment_submissions.append((student_id, assignment_id, score))

cursor.executemany("""
INSERT INTO assignment_submissions (studentId, assignmentId, score)
VALUES (?, ?, ?)
""", assignment_submissions)

# Finalize
conn.commit()
cursor.close()
conn.close()

print("All schema and seed data created successfully in university.db.")



