from faker import Faker
import random
from database import Database

fake = Faker()
db = Database()

def generate_students(n=50):
    for _ in range(n):
        name = fake.name()
        age = random.randint(20, 25)
        gender = random.choice(["Male", "Female", "Other"])
        email = fake.email()
        phone = fake.phone_number()
        enrollment_year = random.randint(2019, 2023)
        course_batch = random.choice(["Batch A", "Batch B", "Batch C"])
        city = fake.city()
        graduation_year = enrollment_year + 4

        query = """INSERT INTO Students 
                   (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
        db.insert(query, values)

def generate_programming():
    students = db.fetch("SELECT student_id FROM Students")
    for (student_id,) in students:
        language = random.choice(["Python", "SQL", "Java", "C++"])
        problems_solved = random.randint(10, 200)
        assessments_completed = random.randint(1, 10)
        mini_projects = random.randint(0, 5)
        certifications_earned = random.randint(0, 3)
        latest_project_score = random.randint(40, 100)

        query = """INSERT INTO Programming 
                   (student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        values = (student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
        db.insert(query, values)

def generate_soft_skills():
    students = db.fetch("SELECT student_id FROM Students")
    for (student_id,) in students:
        communication = random.randint(50, 100)
        teamwork = random.randint(50, 100)
        presentation = random.randint(50, 100)
        leadership = random.randint(50, 100)
        critical_thinking = random.randint(50, 100)
        interpersonal_skills = random.randint(50, 100)

        query = """INSERT INTO SoftSkills 
                   (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
        values = (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
        db.insert(query, values)

def generate_placements():
    students = db.fetch("SELECT student_id FROM Students")
    for (student_id,) in students:
        mock_interview_score = random.randint(40, 100)
        internships_completed = random.randint(0, 3)
        placement_status = random.choice(["Ready", "Not Ready", "Placed"])
        company_name = fake.company() if placement_status == "Placed" else None
        placement_package = random.uniform(30000, 120000) if placement_status == "Placed" else None
        interview_rounds_cleared = random.randint(0, 5) if placement_status != "Not Ready" else 0
        placement_date = fake.date_this_year() if placement_status == "Placed" else None

        query = """INSERT INTO Placements 
                   (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        values = (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
        db.insert(query, values)

if __name__ == "__main__":
    db.create_tables()
    generate_students(50)
    generate_programming()
    generate_soft_skills()
    generate_placements()
    print("✅ Fake data inserted successfully!")
