from sqlalchemy.orm import Session
from repositories.user import UserRepository
from schemas import UserCreate, UserUpdate
from models import User


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> User:
        return self.repo.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )

    def get_user(self, user_id: int) -> User | None:
        return self.repo.get_user_by_id(user_id)

    def get_all_users(self) -> list[User]:
        return self.repo.get_all_users()

    def update_user(self, user_id: int, user_data: dict) -> User | None:
        user = self.repo.get_user_by_id(user_id)
        if user:
            return self.repo.update_user(user, **user_data)  
        return None

    def delete_user(self, user_id: int) -> bool:
        user = self.repo.get_user_by_id(user_id)
        if user:
            self.repo.delete_user(user)
            return True
        return False
