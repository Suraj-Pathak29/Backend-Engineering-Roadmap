import psycopg2 , os
from dotenv import load_dotenv

#Load variables from .env file
load_dotenv()


DB_HOST = "localhost"
DB_NAME = "learning_db"
DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASSWORD")


try:
    conn = psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASS
    )

    cur = conn.cursor()

    # 1. Get input from the user (Simulation of a Frontend)
    print("--- Add New Student ---")
    s_name = input("Enter Name: ")
    s_age = input("Enter Age: ")
    s_skill = input("Enter Skill: ")




    # 2. The SQL Query with Placeholders (%s)
    # We use %s for EVERYTHING (even numbers). The library handles the type conversion.
    # Notice "RETURNING id" at the end!

    cur.execute("INSERT INTO students (name , age , skill) VALUES (%s, %s, %s) RETURNING id;",(s_name , s_age , s_skill))
    
    # GRAB THE ID IMMEDIATELY
    # fetchone() returns a tuple like (5,) -> so we use [0] to get the number 5
    new_student_id = cur.fetchone()[0]
    print(f"Student added with ID: {new_student_id}")
    
    # --- PART 2: Insert Project ---
    ask_project = input("Add a project for this student? (y/n): ")
    if ask_project.lower() == 'y':
        p_title = input("Enter Project title: ")
        cur.execute("INSERT INTO projects (title,student_id) VALUES (%s, %s);", (p_title,new_student_id))
        print(f"Project {p_title} assigned to Student ID {new_student_id}")
    

    # We commit at the end. If the project insert fails, the student insert also rolls back!
    conn.commit()
    print("All Changes are saved to database.")
    cur.close()
    conn.close()
    

except Exception as e:
    print(f"Error: {e}")

    # If error, rollback changes so we don't have half-data
    if conn:
        conn.rollback()
    