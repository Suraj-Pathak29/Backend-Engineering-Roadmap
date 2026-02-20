from fastapi import FastAPI , HTTPException , Depends
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker , declarative_base , Session 
from sqlalchemy import create_engine  , String , Integer , Column
from dotenv import load_dotenv
import os

# --- 1. DATABASE SETUP ----
load_dotenv()
DB_PASS = os.getenv("DB_PASSWORD")
DATABASE_URL = f"postgresql://postgres:{DB_PASS}@localhost/learning_db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False , bind=engine)
Base = declarative_base()


# --- 2. SQLALCHEMY MODEL (The Table) ---
class UserDB(Base):
    __tablename__ = 'api_users'
    id = Column(Integer , primary_key=True , index=True)
    username = Column(String , unique=True , index = True )
    email = Column(String)

# Create the table immediately
Base.metadata.create_all(bind=engine)


# --- 3. PYDANTIC MODEL (The Validation) ---
class UserSchema(BaseModel):
    username: str
    email: str


# --- 4. FASTAPI APP ---
app = FastAPI()


# --- 5. DEPENDENCY (The Magic) ---
# This function opens a connection, hands it to the route, 
# and GUARANTEES it closes when the request is done.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- 6. THE ROUTE ---
# We ask for 'db: Session' and use Depends(get_db) to inject it.
@app.post("/users/")
def create_user(user: UserSchema , db: Session = Depends(get_db)):
    existing_user =  db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400 , detail="username already registered")
    
    # Create new User object
    new_user = UserDB(username= user.username , email= user.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Reloads the object with the new ID from the DB

    return{"message":"User Created" , "User_ID":new_user.id}

@app.get("/users/")
def read_user(db: Session=Depends(get_db)):
    # Fetch all users
    users = db.query(UserDB).all()
    return users
