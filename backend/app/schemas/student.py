from pydantic import BaseModel


class StudentCreate(BaseModel):
    student_id: str
    name: str
    email: str
    course: str
    year: str