

from fastapi import APIRouter,HTTPException,status
from pwdlib import PasswordHash

from schemas.auth import UserRegister
from database.database import SessionLocal
from database.models import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

password_hash = PasswordHash.recommended()


@router.post("/register",status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        db.close()
        raise HTTPException(
        status_code=409,
        detail="Email already registered"
    )

    hashed_password = password_hash.hash(user.password)

    new_user = User(
        username=user.name,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }