from sqlalchemy.orm import sessionmaker
from models import engine, Task, User

Session = sessionmaker(bind=engine)

def get_session():
    return Session()

# --- CORE FUNCTIONS ---

def register_user():
    session = get_session()
    r_username = input("Enter username: ")
    r_email = input("Enter Email: ")

    existing_user = session.query(User).filter_by(username=r_username).first()
    
    if existing_user:
        print(f"Welcome back {existing_user.username} (ID: {existing_user.id})")
        user_id = existing_user.id
        session.close() # Close before returning
        return user_id
    else:
        # FIX 1: Fixed typo 'usename' -> 'username'
        new_user = User(username=r_username, email=r_email)
        session.add(new_user)
        try:
            session.commit()
            print(f"User with ID {new_user.id} added")
            user_id = new_user.id
            session.close()
            return user_id
        except Exception as e:
            session.rollback()
            print(f"Error: {e}")
            session.close()
            return None

def view_task(user_id):
    session = get_session()
    user = session.query(User).filter_by(id=user_id).first()
    
    # FIX 2: Check if the TASKS list is empty, not if the user is missing
    if not user.tasks:
        print("You have no tasks.")
    else:
        print(f"\n--- Tasks for {user.username} ---")
        for task in user.tasks:
            print(f"[{task.id}] {task.title}: {task.content}") # Fixed bracket placement
    
    session.close()

def add_task(user_id):
    session = get_session()
    a_title = input("Task title: ")
    a_content = input("Task content: ")

    # Note: user_id is passed correctly here
    new_task = Task(title=a_title, content=a_content, user_id=user_id)
    
    try:
        session.add(new_task)
        session.commit()
        print(f"Task Saved!")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

def delete_task(user_id): 
    session = get_session()
    t_id = input("Enter Task ID to delete: ")
    
    # FIX 3: Complete Rewrite of Logic
    
    # Step 1: Query the TASK table (not User) looking for the ID
    task_to_delete = session.query(Task).filter_by(id=t_id).first()
    
    if task_to_delete:
        # Step 2: SECURITY CHECK - Does this task belong to the logged-in user?
        if task_to_delete.user_id == user_id:
            try:
                session.delete(task_to_delete)
                session.commit()
                print(f"Task {t_id} Deleted!")
            except Exception as e:
                session.rollback()
                print(f"Error: {e}")
        else:
            print("SECURITY ALERT: You cannot delete a task that isn't yours!")
    else:
        print("Task not found.")
        
    session.close()

def main():
    print("---- TASK MANAGER 2.0 (ORM Edition) ----")
    
    # Log in first
    current_user_id = register_user()

    if not current_user_id:
        print("Login Failed")
        return 

    while True:
        print("\n1. VIEW MY TASKS")
        print("2. ADD TASK")
        print("3. DELETE TASK")
        print("4. EXIT")
        ch = input("Select: ")
        
        if ch == '1':
            view_task(current_user_id)
        elif ch == '2':
            add_task(current_user_id)
        elif ch == '3':
            delete_task(current_user_id)
        elif ch == '4':
            print("BYE!")
            break
        else:
            print("Invalid Choice")

if __name__ == '__main__':
    main()