from sqlite3 import IntegrityError

from model.user import User
from .init import (conn, curs, get_db)
from errors import Missing, Duplicate


curs.execute("CREATE TABLE IF NOT EXISTS user (name TEXT PRIMARY KEY, hash TEXT)")

curs.execute("CREATE TABLE IF NOT EXISTS xuser (name TEXT PRIMARY KEY, hash TEXT)")


def row_to_model(row: tuple) -> User:
    name, hash_ = row
    return User(name=name, hash=hash_)


def model_to_row(user: User) -> dict:
    return user.model_dump()


def get_one(name: str) -> User:
    qry = "SELECT * FROM user WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if not row:
        raise Missing(f"User {name} not found")

    return row_to_model(row)


def get_all() -> list[User]:
    qry = "SELECT * FROM user"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(user: User, table: str = "user") -> None:
    """ Add a user to user or xuser table """
    qry = f"INSERT INTO {table} (name, hash) VALUES (:name, :hash)"
    params = model_to_row(user)
    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise Duplicate(f"{table}: user {user.name} already exists")


def modify(name: str, user: User) -> User:
    qry = "UPDATE user SET hash=:hash WHERE name=:name0"
    params = {"name0": name, **model_to_row(user)}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"User {name} not found")
    conn.commit()
    return user


def delete(name: str) -> None:
    """ Drop user from user table add it to xuser table """
    user = get_one(name)
    qry = "DELETE FROM user WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"User {name} not found")
    create(user, table="xuser")
    conn.commit()

