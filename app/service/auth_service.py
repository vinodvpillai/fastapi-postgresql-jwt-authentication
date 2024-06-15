from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.repository.user_repository import UserRepository
from app.dto.aut_dto import UserCreateDTO, UserUpdateDTO, TokenData, UserResponseDTO
from app.core.env_settings import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.core.token_blacklist import token_blacklist

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register_user(self, user: UserCreateDTO):
        hashed_password = self.get_password_hash(user.password)
        return self.user_repository.create_user(user, hashed_password)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_user_by_username(username)
        if user is None or not self.verify_password(password, user.hashed_password):
            return False
        return user

    def get_user(self, username: str):
        return self.user_repository.get_user_by_username(username)
    
    def get_user_by_email(self, email: str):
        return self.user_repository.get_user_by_email(email)

    def get_user_by_id(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)

    def update_user(self, user_id: int, user: UserUpdateDTO):
        return self.user_repository.update_user(user_id, user)

    def disable_user(self, user_id: int):
        return self.user_repository.disable_user(user_id)

    def get_all_users(self, skip: int = 0, limit: int = 10):
        users = self.user_repository.get_all_users(skip, limit)
        userlist = [UserResponseDTO.model_validate(user.__dict__) for user in users]
        return userlist
    
    def logout_user(self, token: str):
        token_blacklist.add_token(token)
    
    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt
    
    def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        if self.is_token_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been blacklisted",
                headers={"WWW-Authenticate": "Bearer"},
            )
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            username: str = payload.get("sub") # type: ignore
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        user = self.get_user(token_data.username) # type: ignore
        if user is None:
            raise credentials_exception
        userResponseDTO = UserResponseDTO.model_validate(user.__dict__)
        return userResponseDTO

    def is_token_blacklisted(self, token: str) -> bool:
        return token_blacklist.is_blacklisted(token)