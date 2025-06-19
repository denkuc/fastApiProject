""" uses the named params to pass to execute() """
from sqlite3 import IntegrityError

from errors import Missing, Duplicate
from .init import curs, conn
from model.creature import Creature


curs.execute(
    """CREATE TABLE IF NOT EXISTS creature (
    name TEXT PRIMARY KEY,
    country TEXT,
    area TEXT,
    description TEXT,
    aka TEXT)"""
)


def row_to_model(row: tuple) -> Creature:
    return Creature(name=row[0], country=row[1], area=row[2], description=row[3], aka=row[4])


def model_to_dict(model: Creature) -> dict:
    return model.model_dump()


def get_one(name: str) -> Creature | None:
    qry = "SELECT * FROM creature WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if not row:
        raise Missing(f"Creature with name '{name}' not found")

    return row_to_model(row)


def get_all() -> list[Creature]:
    qry = "SELECT * FROM creature"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> Creature:
    qry = "INSERT INTO creature VALUES (:name, :country, :area, :description, :aka)"
    params = model_to_dict(creature)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(f"Creature with name '{creature.name}' already exists")
    conn.commit()
    return get_one(creature.name)


def modify(name: str, creature: Creature) -> Creature:
    qry = "UPDATE creature SET country=:country, area=:area, description=:description, aka=:aka WHERE name=:name"
    params = model_to_dict(creature)
    params["name"] = name
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"Creature with name '{name}' not found")
    conn.commit()
    return get_one(name)


def replace(name: str, creature: Creature):
    qry = "REPLACE INTO creature VALUES (:name, :country, :area, :description, :aka)"
    params = model_to_dict(creature)
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"Creature with name '{name}' not found")
    conn.commit()
    return creature


def delete(name: str):
    qry = "DELETE FROM creature WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(f"Creature with name '{name}' not found")
    conn.commit()
