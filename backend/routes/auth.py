from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pwdlib import PasswordHash

from schemas.auth import UserRegister, UserLogin
from database.database import SessionLocal
from database.models import User
from utils.jwt import create_access_token, verify_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

password_hash = PasswordHash.recommended()

security = HTTPBearer()


# -------------------------
# JWT Authentication
# -------------------------

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    user_id = verify_access_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return user_id


# -------------------------
# Register
# -------------------------

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register(user: UserRegister):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        db.close()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
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

    user_id = new_user.id

    db.close()

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }


# -------------------------
# Login
# -------------------------

@router.post("/login")
def login(user: UserLogin):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        db.close()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    password_valid = password_hash.verify(
        user.password,
        existing_user.password_hash
    )

    if not password_valid:
        db.close()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        existing_user.id
    )

    db.close()

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------
# Current User
# -------------------------

@router.get("/me")
def get_me(
    user_id: int = Depends(get_current_user)
):

    db = SessionLocal()

    current_user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not current_user:
        db.close()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    response = {
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

    db.close()

    return response