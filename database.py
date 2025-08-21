import sqlite3

class Database:
    def __init__(self, db_name="students.db"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Students Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            email TEXT,
            phone TEXT,
            enrollment_year INTEGER,
            course_batch TEXT,
            city TEXT,
            graduation_year INTEGER
        )
        """)

        # Programming Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Programming (
            programming_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            language TEXT,
            problems_solved INTEGER,
            assessments_completed INTEGER,
            mini_projects INTEGER,
            certifications_earned INTEGER,
            latest_project_score INTEGER,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
        """)

        # Soft Skills Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS SoftSkills (
            soft_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            communication INTEGER,
            teamwork INTEGER,
            presentation INTEGER,
            leadership INTEGER,
            critical_thinking INTEGER,
            interpersonal_skills INTEGER,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
        """)

        # Placements Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Placements (
            placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            mock_interview_score INTEGER,
            internships_completed INTEGER,
            placement_status TEXT,
            company_name TEXT,
            placement_package REAL,
            interview_rounds_cleared INTEGER,
            placement_date TEXT,
            FOREIGN KEY(student_id) REFERENCES Students(student_id)
        )
        """)

        conn.commit()
        conn.close()
        print("✅ All tables created successfully!")

    def insert(self, query, values):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        conn.close()

    def fetch(self, query):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
