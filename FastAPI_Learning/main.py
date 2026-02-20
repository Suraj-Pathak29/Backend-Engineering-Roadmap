from fastapi import FastAPI
from pydantic import BaseModel , Field
from typing import Optional

# 1. Create the App
app = FastAPI()


class StudentSchema(BaseModel):
    name: str
    age: int = Field(gt=0 , lt=100) #lt:{LESS_THAN} gt:{GREATER_THAN}
    skill: str 
    # Optional field (default is None if not provided)
    grade: Optional[str] = None


# 2. Create a POST Route
# usage: @app.post instead of @app.get
# student: StudentSchema -> This forces the input to match the class above!
@app.post("/students")
def create_student(student: StudentSchema):
    # If code reaches here, the data is GUARANTEED to be valid.
    # We can access fields like student.name, student.age
    return {
        "message":"Student received successfully",
        "data_received":student,
        "status":"prending_save"
    }


# 3. Create a Route (Endpoint)
# When someone goes to "http://localhost:8000/", run this function.
@app.get("/")
def home():
    # We return a Dictionary. FastAPI automatically turns it into JSON.
    return {"message":"API is online" , "Status": "active"}


# 4. Create a Dynamic Route
# {name} is a variable. If I go to "/hello/Suraj", name = "Suraj"
@app.get("/hello/{name}")
def say_hello(name: str):
    return {"greeting": f"hello {name}!" , "type": "personalized"}


# 5. A Math Route (Type Checking)
# FastAPI ensures 'a' and 'b' are integers automatically!
@app.get("/add/{a}/{b}")
def add_numbers(a: int , b: int):
    return{"result": a + b , "operation": "addition"}

@app.get("/multi/{a}/{b}")
def multiply_num(a: int , b: int):
    return {"result": a * b , "operation": "multiplication"}
