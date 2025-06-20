from jose import jwt, JWTError
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # move to .env later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(user_id: int):
    return create_token({"sub": str(user_id)}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(user_id: int):
    return create_token({"sub": str(user_id)}, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
