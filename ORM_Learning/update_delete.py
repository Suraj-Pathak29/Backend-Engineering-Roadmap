from sqlalchemy.orm import sessionmaker
from models import Student , engine

Session = sessionmaker(bind = engine)
session = Session()


# --- PART 1: UPDATE ---
print("--- Updating Grades ---")

# 1. Find the student we want to change
student_to_update = session.query(Student).filter_by(name='Patrick').first()

if student_to_update:
    print(f"Before update: {student_to_update.name} has grade: {student_to_update.grade}")

    # 2. Modify the attribute directly
    student_to_update.grade = "A+"

    # 3. Commit the change
    session.commit()
    print(F"After update: {student_to_update.name} has grade: {student_to_update.grade}")
else:
    print("Not found")


# --- PART 2: DELETE ---
print("\n--- Deleting Data ---")

# 1. Find the student we want to remove

student_to_delete = session.query(Student).filter_by(name = 'spongebob').first()
if student_to_delete:
    print(f"Deleting: {student_to_delete.name}")

    # 2. Mark for deletion
    session.delete(student_to_delete)

    # 3. Commit the change (Actually runs the DELETE SQL)
    session.commit()
    print("Student deleted successfully!")
else:
    print("Not found")

# Verify: List all remaining students

remaining_students = session.query(Student).all()
print(f"\nRemaining Students: {[s.name for s in remaining_students]}")

session.close()




        




























