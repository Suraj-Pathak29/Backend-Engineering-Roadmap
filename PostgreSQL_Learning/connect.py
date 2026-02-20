import psycopg2 , os
from dotenv import load_dotenv

load_dotenv()


# 1. Setup Connection Variable
DB_HOST = "localhost"
DB_NAME = "learning_db"
DB_USER = "postgres"
DB_PASS = os.getenv("DB_PASSWORD")

try:
    # 2. Connect to database
    conn = psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASS
    )
    print("Connection Successful")

    # 3. Create a cursor
    cur = conn.cursor()

    # 4. Execute a SQL Query
    cur.execute("SELECT students.name , projects.title FROM students JOIN projects ON students.id = projects.student_id;")

    # 5. Fetch the results
    # FETCHALL() grabs all rows that matched the query

    students = cur.fetchall()
    print("\n-- Student List ---")

    for student in students:
        # student is a tuple:(id,name,age,skill,project_id,title,student_id)
        print(f"Name:{student[0]} | title:{student[1]} ")

    # 6. Clean up
    cur.close()
    conn.close()
    print("\n Connection Closed.")

except Exception as e:
    print(f"Error:{e}")

