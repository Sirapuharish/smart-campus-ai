from sqlalchemy import Column, Integer, String

from app.database.db import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_email = Column(String)

    date = Column(String)

    status = Column(String)