from sqlalchemy.orm import Session
from app.model.user import User
from app.dto.aut_dto import UserCreateDTO, UserUpdateDTO

class UserRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def get_user_by_email(self, email:str):
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, username:str):
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, user: UserCreateDTO, hashed_password: str):
        db_user = User(username=user.username, email=user.email, description=user.description, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user: UserUpdateDTO):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            update_data = user.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def disable_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            db_user.is_active = False # type: ignore
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def get_all_users(self, skip: int = 0, limit: int = 10):
        return self.db.query(User).offset(skip).limit(limit).all()
