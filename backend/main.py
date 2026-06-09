from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import Base, engine, get_db
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin
)

from app.utils.security import (
    hash_password,
    verify_password
)

from app.utils.jwt_handler import (
    create_access_token
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SmartCampus API")


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