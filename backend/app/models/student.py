from sqlalchemy import Column, Integer, String

from app.database.db import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(String, unique=True)

    name = Column(String)

    email = Column(String, unique=True)

    course = Column(String)

    year = Column(String)