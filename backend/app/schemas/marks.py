from pydantic import BaseModel


class MarksCreate(BaseModel):
    subject: str
    marks: int