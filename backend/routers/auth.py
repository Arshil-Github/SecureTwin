# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select
from backend.database import get_db, AsyncSessionLocal
from backend.models.user import User
from backend.schemas.user import UserRead, UserCreate, UserUpdate
from backend.config import settings
from backend.fraud.hooks import check_device_trust
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserRead)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        full_name=user_in.full_name,
        age=user_in.age,
        monthly_income=user_in.monthly_income,
        risk_appetite=user_in.risk_appetite,
        trusted_devices=[user_in.device_fingerprint] if user_in.device_fingerprint else []
    )
    
    # FRAUD_HOOK
    if user_in.device_fingerprint:
        check_device_trust(0, user_in.device_fingerprint) # user_id 0 for new user
        
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/login")
async def login(req: dict, db: AsyncSession = Depends(get_db)):
    email = req.get("email")
    password = req.get("password")
    fingerprint = req.get("device_fingerprint")
    
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # FRAUD_HOOK
    is_new_device = False
    if fingerprint:
        res = check_device_trust(user.id, fingerprint)
        if fingerprint not in (user.trusted_devices or []):
            is_new_device = True
            # In real app, we'd add to trusted after OTP
            user.trusted_devices = (user.trusted_devices or []) + [fingerprint]
            await db.commit()

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer", "user": user, "is_new_device": is_new_device}

@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
