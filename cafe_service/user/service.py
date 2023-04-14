from typing import Dict
from cafe_service.provider.auth_provider import AuthProvider
from user.repository import UserRepo


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo

    def create(self, email: str, password: str, name: str) -> Dict[str, any]:
        password = AuthProvider.hashpw(password)
        created_user = self.repo.create(
            name=name,
            email=email,
            password=password,
        )
        return created_user
