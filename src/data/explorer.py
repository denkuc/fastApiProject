""" uses the named params to pass to execute() """
from sqlite3 import IntegrityError

from errors import Missing, Duplicate
from .init import curs, conn
from model.explorer import Explorer


curs.execute(
    """CREATE TABLE IF NOT EXISTS explorer (
    name TEXT PRIMARY KEY,
    country TEXT,
    description TEXT)"""
)


def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])


def model_to_dict(model: Explorer) -> dict:
    return model.model_dump() if model else {}


def get_one(name: str) -> Explorer:
    qry = "SELECT * FROM explorer WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if not row:
        raise Missing(f"Explorer with name '{name}' not found")

    return row_to_model(row)


def get_all() -> list[Explorer]:
    qry = "SELECT * FROM explorer"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    qry = "INSERT INTO explorer VALUES (:name, :country, :description)"
    params = model_to_dict(explorer)
    try:
        curs.execute(qry, params)
        conn.commit()
    except IntegrityError:
        raise Duplicate(f"Explorer with name '{explorer.name}' already exists")

    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    qry = "UPDATE explorer SET country=:country, description=:description WHERE name=:name"
    params = model_to_dict(explorer)
    params["name"] = name
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"Explorer with name '{name}' not found")

    conn.commit()
    return get_one(name)


def replace(name: str, explorer: Explorer):
    qry = "REPLACE INTO explorer VALUES (:name, :country, :description)"
    params = model_to_dict(explorer)
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"Explorer with name '{name}' not found")

    conn.commit()
    return explorer


def delete(name: str):
    qry = "DELETE FROM explorer WHERE name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"Explorer with name '{name}' not found")
    conn.commit()
    return bool(res)
