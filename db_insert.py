from faker import Faker
from conn import create_connection
import random

#initialize
class insertDb_table:
    def __init__(self, host, user, password):
            self.conn = create_connection(host, user, password)
            self.cur = self.conn.cursor()
            self.fake = Faker()
            self.db_name = "studentDB"
            self.cur.execute(f"USE {self.db_name}")
    #insert_StudentsData
    def insert_StudentsData(self, count):
        for i in range(1, count + 1):
            name = self.fake.name()
            age = random.randint(18, 25)
            gender = self.fake.random_element(elements=('Male', 'Female', 'Others'))
            email = self.fake.email()
            phone = self.fake.phone_number()
            enrollment_year = self.fake.date_between('-6y', 'today').year
            course_batch = f"Batch {random.randint(2018, 2024)}-{random.choice(['A', 'B', 'C', 'D'])}"
            city = self.fake.city()
            graduation_year = self.fake.date_between('-6y', 'today').year

            self.cur.execute(
                """
                INSERT INTO Students 
                (student_id,name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (i,name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
            )

        self.conn.commit()
        print(f"{count} student records inserted.")

    #insert_ProgrammingData
    def insert_ProgrammingData(self, student_ids):
        for sid in student_ids:
            student_id = sid  
            language = self.fake.language_name()
            problems_solved = random.randint(1, 100)
            assessments_completed = random.randint(1, 10)
            mini_projects = random.randint(1, 5)
            certifications_earned = random.randint(1, 10)
            latest_project_score = random.randint(1, 100)

            self.cur.execute(
                """
                INSERT INTO Programming 
                (student_id, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (sid, language, problems_solved, assessments_completed, mini_projects, certifications_earned, latest_project_score)
            )

        self.conn.commit()
        print(f"{len(student_ids)} programming records inserted.")

    #insert_SoftSkillsData
    def insert_SoftSkillsData(self, student_ids):
        for sid in student_ids:
            student_id = sid 
            communication = random.randint(1,100)
            teamwork = random.randint(1,100)
            presentation = random.randint(1,100)
            leadership = random.randint(1,100)
            critical_thinking = random.randint(1,100)
            interpersonal_skills = random.randint(1,100)
            self.cur.execute(
                """
                INSERT INTO SoftSkills 
                (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (sid, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills)
            )

        self.conn.commit()
        print(f"{len(student_ids)} SoftSkills records inserted.")

    #insert_Placements
    def insert_Placements(self, student_ids):
        for sid in student_ids:
            student_id = sid
            mock_interview_score = random.randint(1, 100)
            internships_completed = random.randint(0, 5)
            placement_status = random.choice(['Ready', 'Not Ready', 'Placed'])        
            company_name = self.fake.company() if placement_status == 'Placed' else None
            placement_package = round(random.uniform(3.0, 15.0), 2) if placement_status == 'Placed' else 0.0
            interview_rounds_cleared = random.randint(1, 5)
            placement_date = self.fake.date_this_decade() if placement_status == 'Placed' else None
            self.cur.execute(
                """
                INSERT INTO Placements 
                (student_id, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
                """,
                (sid, mock_interview_score, internships_completed, placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
            )

        self.conn.commit()
        print(f"{len(student_ids)} SoftSkills records inserted.")
       



