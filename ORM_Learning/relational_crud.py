from sqlalchemy.orm import sessionmaker
from models import User , Task , engine

Session = sessionmaker(bind = engine)
session = Session()


print("---- Creating Data ----")


# 1. Create a User
user_1 = User(username = 'pyhton_fan' , email = 'code@python.org')


# 2. Create Tasks (Notice we don't set user_id yet!)
task_1 = Task(title = 'Learn SQLAlchemy' , content = 'Master relationships')
task_2 = Task(title = 'Build API' , content = 'Use FastAPi next week')
task_3 = Task(title = 'manual' , content = 'Old way' , user_id = user_1.id )


# 3. THE MAGIC: Link them using the Python List
# SQLAlchemy automatically sets the user_id for us!
user_1.tasks.append(task_1)
user_1.tasks.append(task_2)


# 4. Add ONLY the user. 
# SQLAlchemy is smart enough to add the tasks too because they are linked.
session.add(task_3)

session.commit()

print("User and Tasks saved!")

# --- VERIFICATION ---
print("\n --- Reading data via Relationship ---")

#Fetch the user
user = session.query(User).filter_by(username='pyhton_fan').first()
print(f"User: {user.username}")
print(f"Tasks:")

# Loop through the relationship list directly
for t in user.tasks:
    print(f" - {t.title} (TASK ID: {t.id})")

session.close()