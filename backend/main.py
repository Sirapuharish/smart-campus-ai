from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session

from app.database.db import Base, engine, get_db

from app.models.user import User
from app.models.attendance import Attendance

from app.models.marks import Marks
from app.schemas.marks import MarksCreate
from app.models.marks import Marks

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin
)

from app.schemas.attendance import (
    AttendanceCreate
)

from app.utils.security import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import (
    create_access_token,
    verify_token
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartCampus API")

security = HTTPBearer()


@app.get("/")
def home():
    return {"message": "SmartCampus API Running"}


@app.post("/register", response_model=UserResponse)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="student"
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email,
            "role": db_user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_current_user_payload(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    )
):

    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload


@app.get("/me")
def get_current_user(
    payload: dict = Depends(
        get_current_user_payload
    )
):

    return {
        "email": payload["sub"],
        "role": payload["role"]
    }


@app.get("/student/profile")
def student_profile(
    payload: dict = Depends(
        get_current_user_payload
    ),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == payload["sub"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


@app.post("/student/attendance")
def add_attendance(
    attendance: AttendanceCreate,
    payload: dict = Depends(
        get_current_user_payload
    ),
    db: Session = Depends(get_db)
):

    new_attendance = Attendance(
        student_email=payload["sub"],
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()

    return {
        "message": "Attendance added successfully"
    }


@app.get("/student/attendance")
def get_attendance(
    payload: dict = Depends(
        get_current_user_payload
    ),
    db: Session = Depends(get_db)
):

    records = db.query(
        Attendance
    ).filter(
        Attendance.student_email == payload["sub"]
    ).all()

    return records

@app.post("/student/marks")
def add_marks(
    marks_data: MarksCreate,
    payload: dict = Depends(
        get_current_user_payload
    ),
    db: Session = Depends(get_db)
):

    new_marks = Marks(
        student_email=payload["sub"],
        subject=marks_data.subject,
        marks=marks_data.marks
    )

    db.add(new_marks)
    db.commit()

    return {
        "message": "Marks added successfully"
    }

@app.get("/student/marks")
def get_marks(
    payload: dict = Depends(
        get_current_user_payload
    ),
    db: Session = Depends(get_db)
):

    records = db.query(
        Marks
    ).filter(
        Marks.student_email == payload["sub"]
    ).all()

    return records

@app.get("/student/dashboard")
def student_dashboard(
    payload: dict = Depends(
        get_current_user_payload
    ),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == payload["sub"]
    ).first()

    attendance_records = db.query(
        Attendance
    ).filter(
        Attendance.student_email == payload["sub"]
    ).all()

    marks_records = db.query(
        Marks
    ).filter(
        Marks.student_email == payload["sub"]
    ).all()

    average_marks = 0

    if marks_records:
        total_marks = sum(
            mark.marks for mark in marks_records
        )

        average_marks = total_marks / len(
            marks_records
        )

    return {
        "name": user.name,
        "email": user.email,
        "attendance_records": len(
            attendance_records
        ),
        "subjects_count": len(
            marks_records
        ),
        "average_marks": round(
            average_marks,
            2
        )
    }