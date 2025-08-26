# Student Performance Tracking System – SQL + Streamlit

Video Walkthrough: https://youtu.be/Q-U7CMLzDco 

This project builds a relational database system for managing and visualizing **student academic performance**. The system tracks students, courses, attendance, grades, and assignments using **SQLite and SQL**, and presents insights through a **Streamlit-powered web dashboard**. It demonstrates skills in database engineering, data querying, and frontend analytics.

## Getting Started

### 1. Install dependencies
```bash
pip install streamlit pandas matplotlib seaborn
python db_seed.py
streamlit run Web_app.py
```

##  Project Structure (as Table)

| File/Folder           | Description                                      |
|-----------------------|--------------------------------------------------|
| `db_seed.py`          | Full schema creation and data seeding script     |
| `analytics.py`        | Functions for querying and visualizing data      |
| `Web_app.py`          | Streamlit dashboard UI                           |
| `university.db`       | Generated SQLite database                        |
| `README.md`           | Project overview and documentation               |



## Tools and Technologies

- **Database**: SQLite, SQL
- **Backend**: Python (sqlite3, pandas)
- **Visualization**: matplotlib, seaborn
- **Interface**: Streamlit
- **Schema Design**: Normalized relational model (13 tables)


## Database Schema

| Table Name              | Description                                 |
|-------------------------|---------------------------------------------|
| `student`               | Stores student demographic data             |
| `faculty`               | Stores instructor information               |
| `course`                | Contains course catalog details             |
| `section`               | Specific offerings of a course              |
| `semester`              | Labels for academic terms                   |
| `enrollment`            | Mapping of students to sections             |
| `grades`                | Stores final letter grades                  |
| `attendance`            | Tracks student presence per session         |
| `assignments`           | Information about course assignments        |
| `assignment_submissions`| Student submissions and scores per assignment |


## Data Seeding

The `db_seed.py` script creates all tables and inserts structured seed data:
- 10 students
- 10 course sections
- 14 enrollments
- Grades, attendance logs, and submissions for 5+ students


## Visual Reports (via Streamlit)

- 📈 Grade distribution by letter grade
- 📊 Average scores per assignment
- 🕒 Attendance summary by status
- 🏆 Top performers by GPA
- 📘 Full performance reports per student





