from conn import create_connection

class CreateDB_table:
    def __init__(self, host, user, password):
        self.conn = create_connection(host, user, password)
        self.cur = self.conn.cursor()
        self.db_name = "studentDB"

    def Create_DB(self):
        self.cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        self.cur.execute(f"USE {self.db_name}")

    def table_exists(self, table_name):
        self.cur.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = self.cur.fetchone()
        return result is not None

    def Create_table(self):
        self.cur.execute(f"USE {self.db_name}")

        existing_tables = []

        tables = {
            "Students": """
                CREATE TABLE Students (
                    student_id INT PRIMARY KEY,
                    name VARCHAR(100),
                    age INT,
                    gender CHAR(20),
                    email VARCHAR(100),
                    phone VARCHAR(100),
                    enrollment_year INT,
                    course_batch VARCHAR(100),
                    city VARCHAR(100),
                    graduation_year INT
                )
            """,

            "Programming": """
                CREATE TABLE Programming (
                    programming_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT,
                    language VARCHAR(100),
                    problems_solved INT,
                    assessments_completed INT,
                    mini_projects INT,
                    certifications_earned INT,
                    latest_project_score INT,
                    FOREIGN KEY(student_id) REFERENCES Students(student_id)
                )
            """,

            "SoftSkills": """
                CREATE TABLE SoftSkills (
                    soft_skill_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT,
                    communication INT,
                    teamwork INT,
                    presentation INT,
                    leadership INT,
                    critical_thinking INT,
                    interpersonal_skills INT,
                    FOREIGN KEY(student_id) REFERENCES Students(student_id)
                )
            """,

            "Placements": """
                CREATE TABLE Placements (
                    placement_id INT AUTO_INCREMENT PRIMARY KEY,
                    student_id INT,
                    mock_interview_score INT,
                    internships_completed INT,
                    placement_status VARCHAR(100),
                    company_name VARCHAR(100),
                    placement_package FLOAT,
                    interview_rounds_cleared INT,
                    placement_date DATE,
                    FOREIGN KEY(student_id) REFERENCES Students(student_id)
                )
            """
        }

        for table_name, create_sql in tables.items():
            if self.table_exists(table_name):
                existing_tables.append(table_name)
            else:
                self.cur.execute(create_sql)

        self.conn.commit()

        if existing_tables:
            print(f"Tables already exist: {', '.join(existing_tables)}")
        else:
            print("All tables created successfully.")

    def close(self):
        self.cur.close()
        self.conn.close()
