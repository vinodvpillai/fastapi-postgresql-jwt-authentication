from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.dto.aut_dto import (
    UserCreateDTO, 
    UserUpdateDTO, 
    UserResponseDTO, 
    Token, 
    UserLoginDTO
)
from app.service.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class AuthController:
    def __init__(self):
        self.router = APIRouter()
        self.router.post("/register", response_model=UserResponseDTO)(self.register_user)
        self.router.post("/login", response_model=Token)(self.login_user)
        self.router.put("/update", response_model=UserResponseDTO)(self.update_user)
        self.router.delete("/disable/{userId}", response_model=UserResponseDTO)(self.disable_user)
        self.router.get("/users", response_model=List[UserResponseDTO])(self.get_all_users)
        self.router.post("/logout")(self.logout_user)
    
    #def update_user(self, user: UserUpdateDTO, current_user: UserResponseDTO = Depends(AuthService.get_current_user), db: Session = Depends(get_db)):
    def update_user(self, user: UserUpdateDTO, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        auth_service = AuthService(db)
        current_user = auth_service.get_current_user(token)
        return auth_service.update_user(current_user.id, user)
    
    def register_user(self, user: UserCreateDTO, db: Session = Depends(get_db)):
        auth_service = AuthService(db)
        return auth_service.register_user(user)

    def login_user(self, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = auth_service.create_access_token(
            data={"sub": user.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    def disable_user(self, userId: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        auth_service = AuthService(db)
        auth_service.get_current_user(token)
        return auth_service.disable_user(userId)

    def get_all_users(self, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), skip: int = 0, limit: int = 10):
        auth_service = AuthService(db)
        auth_service.get_current_user(token)
        return auth_service.get_all_users(skip, limit)
    
    def logout_user(self, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        auth_service = AuthService(db)
        auth_service.get_current_user(token)
        auth_service.logout_user(token)
        return {"message": "Logout successful"}

# Instantiate the controller and include its router in the main application
auth_controller = AuthController()
auth_router = auth_controller.router