from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer 
from email_sender.settings import SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
from email_sender.settings import *
from typing import Optional
from jose import JWTError,jwt
from datetime import timedelta
from fastapi import Depends,HTTPException,status 
from sqlmodel import select
from email_sender.db_connections import *
from email_sender.model.user import *


serializer = URLSafeTimedSerializer(SECRET_KEY)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


async def get_current_user(session:DB_SESSION,token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY_token, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email  is None:
            raise credential_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credential_exception
    user = session.exec(select(UserDB).where(UserDB.email == token_data.email)).first()
    if user is None or user.token != token:   
        raise credential_exception
    return user

 

async def get_current_admin_user(current_user: UserDB = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource.")
    return current_user



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_token, algorithm=ALGORITHM)
    return encoded_jwt