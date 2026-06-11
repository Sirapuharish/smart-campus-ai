from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    date: str
    status: str