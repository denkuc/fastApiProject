from datetime import timedelta, datetime
import os
from jose import jwt
from model.user import User

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import user as data
else:
    from data import user as data

from passlib.context import CryptContext


# Move this to secret storage
SECRET_KEY = "some-dummy-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def get_jwt_username(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None
    return username


def get_current_user(token: str) -> User | None:
    if username := get_jwt_username(token):
        return get_one(username)
    if user := lookup_user(username):
        return user
    return None


def lookup_user(username: str) -> User | None:
    if user := get_one(username):
        return user
    return None


def auth_user(username: str, password: str) -> User | None:
    if not (user := lookup_user(username)):
        return None
    if not verify_password(password, user.hash):
        return None
    return user


def create_access_token(data_: dict, expires_delta: timedelta | None = None):
    """Return a new JWT token."""
    src = data_.copy()
    now = datetime.now()
    if not expires_delta:
        expires_delta = timedelta(minutes=15)
    src.update({"exp": now + expires_delta})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_all() -> list[User]:
    """Return a list of all users."""
    return data.get_all()


def get_one(name: str) -> User:
    """Return a single user by name."""
    return data.get_one(name)


def create(user: User) -> User:
    """Create a new user."""
    return data.create(user)


def modify(name: str, user: User) -> User:
    """Partially patch an existing user, only the defined fields """
    return data.modify(name, user)


def delete(name: str) -> None:
    """Delete an existing user."""
    return data.delete(name)
