from model.user import User
from errors import Missing, Duplicate


fakes = [
    User(name="John Doe", hash="abs"),
    User(name="jane Doe", hash="abc"),
]


def find(name: str) -> User | None:
    for user in fakes:
        if user.name == name:
            return user
    return None


def check_missing(name: str) -> None:
    if not find(name):
        raise Missing(f"User {name} not found")


def check_duplicate(name: str) -> None:
    if find(name):
        raise Duplicate(f"User {name} already exists")


def get_all() -> list[User]:
    return fakes


def get_one(name: str) -> User:
    check_missing(name)
    return find(name)


def create(user: User) -> User:
    check_duplicate(user.name)
    return user


def modify(name: str, user: User) -> User:
    check_missing(name)
    return user


def delete(name: str) -> None:
    check_missing(name)
    return None
