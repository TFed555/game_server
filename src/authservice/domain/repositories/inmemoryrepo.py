import uuid
from userrepository import AuthRepositoryProtocol
from domain.entities.userdomainmodel import UserDomainModel

class InMemoryUserRepository(AuthRepositoryProtocol):
    def __init__(self):
        self._users: dict[str, UserDomainModel] = {}

    def getByID(self, user_id: str):
        user = self._users[user_id]
        if not user:
            return None
        else:
            return user

    def addUser(self, user: UserDomainModel):
        for l in self._users.values():
            if l.login == user.login:
                return False
        user_id = str(uuid.uuid4())
        self._users[user_id] = user
        return True