import psycopg2 , os
from dotenv import load_dotenv

load_dotenv()

DB_PASS = os.getenv("DB_PASSWORD")

DB_CONFIG = {
    "host":"localhost",
    "database":"learning_db",
    "user":"postgres",
    "password": DB_PASS
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def view_students():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT s.id , s.name, s.age, s.skill, p.title FROM students s LEFT JOIN projects p ON s.id = p.student_id;")

        rows = cur.fetchall()
        print("---- Student Roster ----")
        print(f"{'ID':<5}  {'Name':<20}  {'Age' :<10}  {'Skill':<15}  {'Project'}")
        print("-" * 75)
        
        for row in rows:
            if row[4] is not None:
                project = row[4]
            else:
                project = "No Project"
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<10} {row[3]:<15} {project}")

        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error Fetching data:{e}")


def add_student():
    s_name = input("Enter name: ")
    s_age = input("Enter age: ")
    s_skill = input("Enter skill: ")
    
    conn = None #SO that if exception comes it does not show conn var not defined
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = "INSERT INTO students (name,age,skill) VALUES (%s,%s,%s) RETURNING id;"
        cur.execute(query , (s_name , s_age , s_skill))

        new_id = cur.fetchone()[0]
        print(f"Student added with ID {new_id}")
        if input(f"Do you want to add project with student ID {new_id} (Y/N) : ").lower() == 'y':
            p_title = input("Enter project title: ")
            cur.execute("INSERT INTO projects (title , student_id ) VALUES (%s, %s)" , (p_title , new_id))
            print("Project added")
        
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Error:{e}")

        if conn:
            conn.rollback()
            print("Transactioon rolled back")



def delete_student():
    s_ask = input("Enter student id you want to delete")
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM students where id = %s;" , (s_ask,))
        conn.commit()
        print(f"Student with ID {s_ask} Deleted!")
        cur.close()
        conn.close()


    except Exception as e:
        print(f"Delete Failed:{e}")
        print("Hint: You cannot delete a student who has active projects!")
        if conn:
            conn.rollback()



def main():

    while True:
        print("--- STUDENT MANAGER ---")
        print("--- VIEW STUDENTS : PRESS(1) ---")
        print("--- ADD STUDENT : PRESS(2) ---")
        print("--- DELETE STUDENT : PRESS(3) ---")
        print("--- EXIT : PRESS(4) ---")
        ch = input("Enter Your Choice: ")
        if ch == '1':
            view_students()
        
        elif ch == '2':
            add_student()
        
        elif ch == '3':
            delete_student()

        elif ch == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()


