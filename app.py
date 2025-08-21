import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from database import Database

db = Database()

# ---------------- Load Data ----------------
def load_students():
    query = """
    SELECT s.student_id, s.name, s.age, s.gender, s.city, 
           p.language, p.problems_solved, p.latest_project_score,
           ss.communication, ss.teamwork, ss.presentation,
           pl.placement_status, pl.company_name, pl.placement_package
    FROM Students s
    JOIN Programming p ON s.student_id = p.student_id
    JOIN SoftSkills ss ON s.student_id = ss.student_id
    JOIN Placements pl ON s.student_id = pl.student_id
    """
    results = db.fetch(query)
    columns = ["ID", "Name", "Age", "Gender", "City", "Language",
               "Problems Solved", "Project Score",
               "Communication", "Teamwork", "Presentation",
               "Placement Status", "Company", "Package"]
    return pd.DataFrame(results, columns=columns)

# ---------------- Eligibility Dashboard ----------------
def eligibility_dashboard():
    st.title("🎓 Placement Eligibility Dashboard")

    # Load Data
    df = load_students()

    # Sidebar filters
    st.sidebar.header("Filters")
    min_problems = st.sidebar.slider("Min Problems Solved", 0, 200, 50)
    min_project_score = st.sidebar.slider("Min Project Score", 40, 100, 60)
    min_communication = st.sidebar.slider("Min Communication Skill", 50, 100, 70)
    status_filter = st.sidebar.multiselect("Placement Status", df["Placement Status"].unique(), default=df["Placement Status"].unique())

    # Apply filters
    filtered = df[
        (df["Problems Solved"] >= min_problems) &
        (df["Project Score"] >= min_project_score) &
        (df["Communication"] >= min_communication) &
        (df["Placement Status"].isin(status_filter))
    ]

    # Show Data
    st.subheader("📋 Eligible Students")
    st.dataframe(filtered)

    # Summary stats
    st.subheader("📊 Statistics")
    col1, col2 = st.columns(2)
    col1.metric("Total Students", len(df))
    col2.metric("Eligible Students", len(filtered))

    # ---------------- Charts ----------------
    st.subheader("📈 Visual Insights")

    # 1. Placement Status Distribution
    st.write("### Placement Status Distribution")
    status_counts = df["Placement Status"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.bar(status_counts.index, status_counts.values, color=["orange", "red", "green"])
    ax1.set_xlabel("Status")
    ax1.set_ylabel("Count")
    st.pyplot(fig1)

    # 2. Problems Solved Distribution
    st.write("### Problems Solved Comparison")
    fig2, ax2 = plt.subplots()
    ax2.hist(df["Problems Solved"], bins=20, alpha=0.5, label="All Students")
    ax2.hist(filtered["Problems Solved"], bins=20, alpha=0.5, label="Eligible Students")
    ax2.set_xlabel("Problems Solved")
    ax2.set_ylabel("Number of Students")
    ax2.legend()
    st.pyplot(fig2)

    # 3. Average Soft Skills by Placement Status
    st.write("### Average Soft Skills by Placement Status")
    avg_skills = df.groupby("Placement Status")[["Communication", "Teamwork", "Presentation"]].mean()
    st.bar_chart(avg_skills)

# ---------------- SQL Insights Page ----------------
def sql_insights():
    st.title("📊 SQL Insights")

    queries = {
        "1. Average Programming Performance per Batch": """
            SELECT course_batch, AVG(problems_solved) as avg_problems
            FROM Students s 
            JOIN Programming p ON s.student_id = p.student_id
            GROUP BY course_batch;
        """,
        "2. Top 5 Students Ready for Placement": """
            SELECT s.name, p.problems_solved, ss.communication, pl.mock_interview_score
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            JOIN SoftSkills ss ON s.student_id = ss.student_id
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status='Ready'
            ORDER BY p.problems_solved DESC, ss.communication DESC, pl.mock_interview_score DESC
            LIMIT 5;
        """,
        "3. Average Soft Skills Scores": """
            SELECT AVG(communication), AVG(teamwork), AVG(presentation)
            FROM SoftSkills;
        """,
        "4. Placement Packages by Company": """
            SELECT company_name, AVG(placement_package) as avg_package
            FROM Placements
            WHERE placement_status='Placed'
            GROUP BY company_name;
        """,
        "5. Gender Distribution of Placements": """
            SELECT gender, COUNT(*)
            FROM Students s
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status='Placed'
            GROUP BY gender;
        """,
    }

    for desc, query in queries.items():
        st.subheader(desc)
        results = db.fetch(query)
        st.dataframe(results)

# ---------------- Main App ----------------
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Eligibility Dashboard", "SQL Insights"])

    if page == "Eligibility Dashboard":
        eligibility_dashboard()
    elif page == "SQL Insights":
        sql_insights()

if __name__ == "__main__":
    main()

