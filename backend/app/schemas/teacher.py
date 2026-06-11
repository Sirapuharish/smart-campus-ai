from pydantic import BaseModel


class TeacherMarksCreate(BaseModel):
    student_id: str
    subject: str
    marks: int