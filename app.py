import streamlit as st
import mysql.connector
import pandas as pd
from db_create import CreateDB_table
from db_insert import insertDb_table

# -------------------------------
# Database credentials
# -------------------------------
HOST = "gateway01.us-west-2.prod.aws.tidbcloud.com"
USER = "4VNm5hSdn9KZBiM.root"
PASSWORD = "44L1IntgljTiVfG2"
DATABASE = "studentDB"

# -------------------------------
# Create database connection
# -------------------------------
def create_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

# -------------------------------
# Get Eligible Students Function
# -------------------------------
def get_eligible_students(problems_threshold=50,Assessment=5,Projects=2,Certification=5,LatestProjectScore=50,soft_threshold=50,ready_only=False):
    conn = create_connection()
    query = f"""
        SELECT 
            S.student_id,
            S.name,
            P.problems_solved,p.assessments_completed,p.mini_projects,p.certifications_earned,p.latest_project_score,
            ROUND((SS.communication + SS.teamwork + SS.presentation + SS.leadership + SS.critical_thinking + SS.interpersonal_skills)/6, 2) AS avg_soft_skills,
            PL.placement_status
        FROM Students S
        JOIN Programming P ON S.student_id = P.student_id
        JOIN SoftSkills SS ON S.student_id = SS.student_id
        JOIN Placements PL ON S.student_id = PL.student_id
        WHERE 
            P.problems_solved >= %s
            AND P.assessments_completed>=%s
            AND P.mini_projects>=%s
            AND P.certifications_earned>=%s
            AND p.latest_project_score>=%s
            AND ((SS.communication + SS.teamwork + SS.presentation + SS.leadership + SS.critical_thinking + SS.interpersonal_skills)/6) >= %s
    """
    params = [problems_threshold,Assessment,Projects,Certification,LatestProjectScore,soft_threshold]

    if ready_only:
        query += " AND PL.placement_status = 'Ready'"

    df = pd.read_sql(query, conn, params=params)    
    conn.close()
    return df

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Student Database & Placement Dashboard", layout="wide")

# Unified Sidebar Menu
menu = [
    "🏗️ Create Database & Tables",
    "📝 Insert Student Data",
    "👨‍🎓 Explore Students",
    "🔍 View Eligible Students",
    "📊 SQL Insights"
]
choice = st.sidebar.selectbox("Select Action", menu)

st.title("🎓 Student Database & Placement Dashboard")

# 1. Create Database & Tables
if choice == "🏗️ Create Database & Tables":
    st.subheader("📂 Create Database and Tables")
    if st.button("Create Now"):
        try:
            db_creator = CreateDB_table(HOST, USER, PASSWORD)
            db_creator.Create_DB()
            db_creator.Create_table()
            db_creator.close()
            st.success("✅ Database and tables created successfully.")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# 2. Insert Student Data
elif choice == "📝 Insert Student Data":
    st.subheader("➕ Insert Random Student Data")
    count = st.number_input("Number of Students to Insert", min_value=1, max_value=100, value=5, step=1)

    if st.button("Insert Data"):
        try:
            db_inserter = insertDb_table(HOST, USER, PASSWORD)
            db_inserter.insert_StudentsData(count)
            student_ids = list(range(1, count + 1))
            db_inserter.insert_ProgrammingData(student_ids)
            db_inserter.insert_SoftSkillsData(student_ids)
            db_inserter.insert_Placements(student_ids)
            db_inserter.cur.close()
            db_inserter.conn.close()
            st.success(f"✅ Inserted {count} records into all tables.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
# 3. Explore Students
elif choice == "👨‍🎓 Explore Students":    
    choice2=st.sidebar.selectbox("👨‍🎓 Explore Students", ["By ID", "All Students"])
    conn = create_connection()   
    
    if choice2=="By ID": 
        student_id = st.number_input("Enter Student Id", min_value=1, max_value=500,step=1)       
        query=f"""
        SELECT s.*,p.language,p.problems_solved,p.assessments_completed,p.mini_projects,p.certifications_earned,p.latest_project_score,
        ss.communication,ss.teamwork,ss.presentation,ss.leadership,ss.critical_thinking,ss.interpersonal_skills,
        pl.mock_interview_score,pl.internships_completed,pl.placement_status,pl.company_name,pl.placement_package,pl.interview_rounds_cleared, pl.placement_date
        FROM Students s
        JOIN Programming p ON s.student_id=p.student_id
        JOIN SoftSkills ss ON s.student_id=ss.student_id 
        JOIN Placements pl ON s.student_id=pl.student_id
        WHERE s.student_id={student_id}
        """
        df = pd.read_sql(query, conn)
        st.dataframe(df, use_container_width=True)

    if  choice2=="All Students":    
        st.subheader("👥 All Students Details")
        query="""
        SELECT s.*,p.language,p.problems_solved,p.assessments_completed,p.mini_projects,p.certifications_earned,p.latest_project_score,
        ss.communication,ss.teamwork,ss.presentation,ss.leadership,ss.critical_thinking,ss.interpersonal_skills,
        pl.mock_interview_score,pl.internships_completed,pl.placement_status,pl.company_name,pl.placement_package,pl.interview_rounds_cleared, pl.placement_date
        FROM Students s
        JOIN Programming p ON s.student_id=p.student_id
        JOIN SoftSkills ss ON s.student_id=ss.student_id 
        JOIN Placements pl ON s.student_id=pl.student_id
        """
        df = pd.read_sql(query, conn)
        st.dataframe(df, use_container_width=True)

# 4. View Eligible Students
elif choice == "🔍 View Eligible Students":
    st.sidebar.subheader("🎯 Filter Eligible Students")

    col1, col2, col3,col4,col5,col6,col7 = st.columns(7)
    with col1:
        problems_threshold = st.sidebar.slider("Min Problems Solved", 0, 100, 50)
    with col2:
        Assessment = st.sidebar.slider("Min Assessment Completed", 0, 10, 5)
    with col3:
        Projects = st.sidebar.slider("Min Mini Projects Completed", 0, 5, 2)
    with col4:
        Certification = st.sidebar.slider("Min Certification earned", 0, 10, 5)
    with col5:
        LatestProjectScore = st.sidebar.slider("Min Latest Project Score", 0, 100, 50)
    with col6:
        soft_threshold = st.sidebar.slider("Min Avg Soft Skill Score", 0, 100, 50)
    with col7:
        ready_only = st.sidebar.checkbox("Only Placement-Ready")

    if st.sidebar.button("Show Eligible Students"):
        df = get_eligible_students(problems_threshold,Assessment,Projects,Certification,LatestProjectScore,soft_threshold,ready_only)
        if df.empty:
            st.warning("⚠️ No students found matching the criteria.")
        else:
            st.success(f"✅ {len(df)} students found:")
            st.dataframe(df, use_container_width=True)

# 5. 10 SQL queries - SQL Insights
elif choice == "📊 SQL Insights":
    st.sidebar.subheader("📈10 SQL queries")    
    conn = create_connection()
    choice3 = st.sidebar.radio(
    "Navigate",
    ["📊 Average Problems Solved per Batch",
     "🏆 Top 5 Students Ready for Placement", 
     "🎤 Soft Skill Score Distribution", 
     "✅ Students with More Than 2 Internships and Placed",
     "🎯 Students with High Programming and Soft Skills",
     "💼 Placement Status Distribution",
     "💰 Average Placement Package by Batch",
     "🎓 Top 5 Students by Latest Project Score",
     "⏳ Students Not Ready for Placement but High Soft Skills",
     "🏙️ Number of Students per City"]    
)
    
    if choice3=="📊 Average Problems Solved per Batch":
        queries = """
            SELECT course_batch, AVG(problems_solved) AS avg_problems_solved
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            GROUP BY course_batch
            ORDER BY avg_problems_solved DESC
        """
    elif choice3=="🏆 Top 5 Students Ready for Placement": 
        queries = """
            SELECT S.name, P.problems_solved
            FROM Students S
            JOIN Programming P ON S.student_id = P.student_id
            JOIN Placements PL ON S.student_id = PL.student_id
            WHERE PL.placement_status = 'Ready'
            ORDER BY P.problems_solved DESC
            LIMIT 5
        """
    elif choice3=="🎤 Soft Skill Score Distribution": 
        queries = """
            SELECT communication, teamwork, presentation
            FROM SoftSkills
        """
    elif choice3=="✅ Students with More Than 2 Internships and Placed": 
        queries = """
            SELECT s.name, pl.mock_interview_score, pl.internships_completed, 
                   pl.interview_rounds_cleared, pl.placement_date, pl.company_name, pl.placement_package
            FROM Students s
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.internships_completed > 2 AND pl.placement_status = 'Placed'
        """
    elif choice3=="🎯 Students with High Programming and Soft Skills": 
        queries = """
            SELECT s.name, p.problems_solved, ss.communication, ss.teamwork
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            JOIN SoftSkills ss ON s.student_id = ss.student_id
            WHERE p.problems_solved > 100 AND ss.communication > 80 AND ss.teamwork > 80
        """
    elif choice3=="💼 Placement Status Distribution": 
        queries = """
            SELECT placement_status, COUNT(*) AS count
            FROM Placements
            GROUP BY placement_status
        """
    elif choice3=="💰 Average Placement Package by Batch": 
        queries = """
            SELECT s.course_batch, AVG(pl.placement_package) AS avg_package
            FROM Students s
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status = 'Placed'
            GROUP BY s.course_batch
            ORDER BY avg_package DESC
        """
    elif choice3=="🎓 Top 5 Students by Latest Project Score": 
        queries = """
            SELECT s.name, p.latest_project_score
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            ORDER BY p.latest_project_score DESC
            LIMIT 5
        """
    elif choice3=="⏳ Students Not Ready for Placement but High Soft Skills": 
        queries = """
            SELECT s.name, ss.communication, ss.teamwork, ss.presentation, ss.leadership,
                   ss.critical_thinking, ss.interpersonal_skills, pl.placement_status
            FROM Students s
            JOIN SoftSkills ss ON s.student_id = ss.student_id
            JOIN Placements pl ON s.student_id = pl.student_id
            WHERE pl.placement_status = 'Not Ready'
            AND (
                ss.communication > 85 OR ss.teamwork > 85 OR ss.presentation > 85 OR
                ss.leadership > 85 OR ss.critical_thinking > 85 OR ss.interpersonal_skills > 85
            )
        """
    elif choice3=="🏙️ Number of Students per City": 
        queries = """
            SELECT city, COUNT(*) AS student_count
            FROM Students
            GROUP BY city
            ORDER BY student_count DESC
        """
       
    st.markdown(f"**{choice3}**")
    df = pd.read_sql(queries, conn)
    st.dataframe(df, use_container_width=True)
  
    conn.close()
