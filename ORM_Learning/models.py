import os , bcrypt
from dotenv import load_dotenv
from sqlalchemy import create_engine , Column , String , Integer , ForeignKey
from sqlalchemy.orm import declarative_base , relationship

load_dotenv()
DB_PASS = os.getenv('DB_PASSWORD')

DATABASE_URL = f"postgresql://postgres:{DB_PASS}@localhost/learning_db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

# --- MODEL 1: THE USER ---
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer , primary_key=True)
    username = Column(String(50) , unique = True , nullable = False)
    email = Column(String(100) , unique = True , nullable = False)
    password_hash = Column(String(128))

    # Magic Link 1:
    # This creates a virtual list 'tasks' on every User object.
    # back_populates="owner" means "Look at the Task class for the 'owner' field to link us."
    tasks = relationship("Task" , back_populates = "owner") 
    
    def set_password(self , plain_password):
        password_bytes = plain_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes , salt)
        # Decode back to string for storage in DB
        self.password_hash = hashed.decode('utf-8')


    def check_password(self , plain_password):
        input_bytes = plain_password.encode('utf-8')
        stored_bytes = self.password_hash.encode('utf-8')

        return bcrypt.checkpw(input_bytes , stored_bytes) 
    
    def __repr__(self):
        return f"<User(username = {self.username})>"


# --- MODEL 2: THE TASK ---
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer , primary_key=True)
    title = Column(String(100) , nullable=False)
    content = Column(String(200))

    # The actual Foreign Key (The Bridge)
    # This says: "The value in this column must exist in users.id"
    user_id = Column(Integer , ForeignKey('users.id'))

    # Magic Link 2:
    # This creates a virtual property 'owner' on every Task object.
    # It lets you access the User object directly (e.g., my_task.owner.username)
    owner = relationship("User", back_populates = "tasks")


    def __repr__(self):
        return f"<Task(title = {self.title})>"
    

if __name__ == '__main__':
    print("Creating User and Task tables........")
    Base.metadata.create_all(engine)
    print("Table Created !!!")



























