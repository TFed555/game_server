from dataclasses import dataclass

@dataclass
class UserDomainModel:
    login: str
    password_hash: str
    is_active: bool
    id: str|None