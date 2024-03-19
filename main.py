from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()
students = {
    1: {
        "name": "Arjun",
        "age": 10,
        "year": 4
    },
    2: {
        "name": "samir",
        "age": 1000,
        "year": 4
    }
}

# Model for student data
class Student(BaseModel):
    name: str
    age: int
    year: str

# Model for updating student data (optional fields)
class UpdateStudent(BaseModel):
    name: str | None = None
    age: int | None = None
    year: str | None = None

# Root endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Get student by ID
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="Student ID", gt=0)):
    return students.get(student_id, {"error": "Student not found"})

# Get student by query (improved with list comprehension)
@app.get('/get-student')
def get_student_by_query(id: str, name: str | None = None):
    matching_students = [student for student_id, student in students.items() if student["name"] == name]
    return matching_students or {"Data": "NotFound"}

# Create student (error handling improved)
@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student already exists"}
    students[student_id] = student
    return students

# Update student (using model validation and error handling)
@app.put('/update-student/{student_id}')
def update_student(student_id: int, student: UpdateStudent | None = None):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    updated_student = {**students[student_id]}  # Create a copy

    if student:
        if student.name is not None:
            updated_student["name"] = student.name
        if student.year is not None:
            updated_student["year"] = student.year
        if student.age is not None:
            updated_student["age"] = student.age

    students[student_id] = updated_student
    return students


@app.delete("/delete/{student_id}")
def delete_student_by_id(student_id:int):
    if student_id not in students:
        return {"Error":"Student not found"}
    del students[student_id]
    return students
