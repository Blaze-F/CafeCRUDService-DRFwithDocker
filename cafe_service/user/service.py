from typing import Dict
from provider.auth_provider import AuthProvider
from user.repository import UserRepo


class UserService:
    def __init__(self, repo: UserRepo) -> None:
        self.repo = repo
        self.auth_provider = AuthProvider()

    def create(self, phone: str, password: str, name: str) -> Dict[str, any]:
        password = self.auth_provider.hashpw(password=password)
        created_user = self.repo.create(
            name=name,
            phone=phone,
            password=password,
        )
        return created_user
