from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    description: str

class UserUpdateDTO(BaseModel):
    description: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: EmailStr
    description: str
    is_active: bool

    class Config:
        orm_mode = True

class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None