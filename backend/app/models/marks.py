from sqlalchemy import Column, Integer, String

from app.database.db import Base


class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)

    student_email = Column(String)

    subject = Column(String)

    marks = Column(Integer)