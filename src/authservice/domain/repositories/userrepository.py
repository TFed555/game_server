from typing import Protocol
from domain.entities import UserDomainModel

class AuthRepositoryProtocol(Protocol):
    def getByID(self, user_id: str) -> UserDomainModel | None:
        ...

    def getByEmail(self, email: str) -> UserDomainModel | None:
        ...

    def getAll(self) -> list[UserDomainModel] | None:
        ...

    def addUser(self, user: UserDomainModel) -> str:
        ...

    def updateUser(self) -> None:
        ...

    def deleteUser(self) -> None:
        ...

    def userExists(self, user_id: str) -> bool:
        ...
