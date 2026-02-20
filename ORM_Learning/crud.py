from sqlalchemy.orm import sessionmaker
from models import Student , engine
# ^ We import the 'Student' class and 'engine' from models.py


# 1. Create a Session Factory
# This is a class that produces sessions. We bind it to our engine.
Session  =sessionmaker(bind=engine)


#Start a session
session = Session()



# --- PART A: CREATE (INSERT) ---
print("--- Adding Data ---")

# Create Python Objects (No SQL needed!)
s_1 = Student(name = "spongebob" , age = 20 , grade = "A" , email = "sponge@sea.com")
s_2 = Student(name = "Patrick" , age = 22 , grade = "C" , email = "star@sea.com")
s_3 = Student(name = 'Suraj' , age = 21 , grade = 'A' , email = 'sun@sea.com')
s_4 = Student(name = 'Muskan' , age = 26 , grade = 'B' , email = 'smile@sea.com')
s_5 = Student(name = 'Vini' , age = 28 , grade = 'F' , email = 'vin@sea.com')

# Add them to the "staging area"
session.add(s_1)
session.add(s_2)
session.add(s_3)
session.add(s_4)
session.add(s_5)


#commit to DB
session.commit()
print("Student added successfully!")


# --- PART B: READ (SELECT) ---
print("--- Reading data ---")


# Old Way: "SELECT * FROM orm_students"
# New Way: Query the Class directly
all_students = session.query(Student).all()

for i in all_students:
    print(f"ID: {i.id} | Name:{i.name} | Age:{i.age} | Grade:{i.grade}")
    

# --- PART C: FILTERING (WHERE Clause) ---
print("\n--- Filtering Data ---")

# Old Way: "SELECT * FROM orm_students WHERE graed = 'A'"
# New Way: .filter_by()


found_student = session.query(Student).filter_by(grade = "A").all()
if found_student:
    for student in found_student:
        if student:
            print(f"Found him: {student.name} is {student.age} having grade {student.grade}")
else:
    print("Not found")


#clean up
session.close()