import sys
import getpass #Hides input for passwrod
from sqlalchemy.orm import sessionmaker
from models import User ,  Task , engine

Session = sessionmaker(bind = engine)

def get_session():
    return Session()

def register_user():
    session = get_session()
    print("\n--- Register User ---")
    username = input("Choose username: ")
    email = input("Enter email: ")
    # 1. Ask for password securely (hidden input)
    password = getpass.getpass("Choose Password: ")

    if session.query(User).filter_by(username = username).first():
        print("Username already exists!!")
        session.close()
        return None
    
    new_user = User(username = username , email = email)
    new_user.set_password(password)
    try:
        session.add(new_user)
        session.commit()
        print("Account Created! Please log in. ")
        return None
    
    except Exception as e:
        session.rollback()
        print(f"Error:{e}")
        return None
    
    finally:
        session.close()


def login_user():
    session = get_session()
    print("---- Log in ----")
    username = input("Enter username: ")
    password = getpass.getpass("Enter Password: ")

    user = session.query(User).filter_by(username = username).first()

    #verify Password
    if user and user.check_password(password):
        print("Log in successful!")
        user_id = user.id
        session.close()
        return user_id
    
    else:
        print("Invalid username or password.")
        session.close()
        return None
    
def view_task(u_id):
    session = get_session()
    user  = session.query(User).filter_by(id = u_id).first()

    if user and user.tasks:
        print(f"Task for {user.username}")
        for task in user.tasks:
            print(f"[{task.id}] | {task.title} | {task.content}")

    else:
        print("---- YOU HAVE NO TASK ----")
        
    session.close()


def add_task(u_id):
    session = get_session()
    print("--- ADD TASKS ---")
    u_title = input("Enter title: ")
    u_content = input("Enter Content: ")
    try:
        new_task = Task(title = u_title , content = u_content , user_id = u_id )
        session.add(new_task)
        session.commit()
        print("Task Added Successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


def delete_task(u_id):
    session = get_session()
    t_id = input("Enter the task ID to delete: ")
    task_to_delete = session.query(Task).filter_by(id = t_id).first()
    if task_to_delete:
        if task_to_delete.user_id == u_id:
            try:
                session.delete(task_to_delete)
                session.commit()

            except Exception as e:
                session.rollback()
                print(f"Error: {e}")

            finally:
                session.close()

        else:
            print("SECURITY ALERT: You cannot delete a task that isn't yours!")
        
    else:
        print("Task Not Found")
  


def main():
    print("----- SECURE TASK MANAGER -----")
    current_user_id = None

    # AUTH LOOP
    while not current_user_id:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        ch = input("Select: ")
        if ch == '1':
            current_user_id = login_user()
        elif ch == '2':
            register_user()
        elif ch == '3':
            sys.exit()
        else:
            print("Invalid Choice!")

    # APP LOOP (Only runs if logged in)
    while True:
        print("--- MAIN MENU ---")
        print("1. View My Tasks")
        print("2. Add Task")
        print("3. Delete Task")
        print("4. Logout")

        ch = input("Select: ")
        if ch == '1':
            view_task(current_user_id)
        elif ch == '2':
            add_task(current_user_id)
        elif ch == '3':
            delete_task(current_user_id)
        elif ch == '4':
            print("Logged out.")
            current_user_id = None
            break
        else:
            print("Invalid Choice")

if __name__ == '__main__':
    main()