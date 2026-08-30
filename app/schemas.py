from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# ----------------------------------------
# 1. مخططات بيانات الدورات (Course Schemas)
# ----------------------------------------
class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructor: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int


# ----------------------------------------
# 2. مخططات بيانات الطلاب (Student Schemas)
# ----------------------------------------
class StudentBase(BaseModel):
    name: str
    email: str
    age: int = Field(gt=0, description="Age must be greater than 0")

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int