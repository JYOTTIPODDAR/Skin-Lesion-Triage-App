from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from database.database import SessionLocal
from database.models import User
from schemas.auth import UserRegister, UserLogin, ForgotPassword

from utils.security import hash_password, verify_password
from utils.jwt import create_access_token, verify_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


security = HTTPBearer()


# =====================================
# GET CURRENT USER FROM JWT
# =====================================

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


# =====================================
# REGISTER
# =====================================

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


    # HASH PASSWORD 🔐
    hashed_password = hash_password(user.password)


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


# =====================================
# LOGIN
# =====================================

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


    # VERIFY HASHED PASSWORD 🔐
    password_valid = verify_password(
        user.password,
        existing_user.password_hash
    )

    if not password_valid:

        db.close()

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    # CREATE JWT TOKEN 🔑
    access_token = create_access_token(
        existing_user.id
    )

    db.close()

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }


# =====================================
# FORGOT PASSWORD
# =====================================

@router.post("/forgot-password")
def forgot_password(user: ForgotPassword):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:

        db.close()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )


    # HASH NEW PASSWORD 🔐
    existing_user.password_hash = hash_password(
        user.new_password
    )

    db.commit()

    db.close()

    return {
        "message": "Password reset successfully"
    }


# =====================================
# CURRENT USER
# =====================================

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