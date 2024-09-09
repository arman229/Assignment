from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlmodel import SQLModel,Field
from fastapi import FastAPI
from enum import Enum
from datetime import datetime

class RoleAdminOrUser(str, Enum):
    user = "user"
    admin = "admin"
    
class UserDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    role: RoleAdminOrUser = RoleAdminOrUser.user 
    token: Optional[str] = None  
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)   
    
    
class SignUpForm(BaseModel):
    email: EmailStr
    username:str
    password: str
    
class SignUpFormUpdate(BaseModel):
    username:str
    password: str
    
class PasswordResetRequest(BaseModel):
     email: EmailStr

class PasswordResetForm(BaseModel):
    password: str
    token: str    
    
class TokenData(BaseModel):
    email: Optional[str] = None    
    


# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     role: Optional[str] = None
    
# class UserInDB(User):
#     hashed_password: str
#     token: Optional[str] = None
#     created_at: datetime
#     updated_at: datetime
    
