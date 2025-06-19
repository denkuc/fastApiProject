from model.creature import Creature
import data.creature as data


def get_all() -> list[Creature]:
    """Return a list of all creatures."""
    return data.get_all()


def get_one(name: str) -> Creature | None:
    """Return a single creature by name."""
    return data.get_one(name)


def create(creature: Creature) -> Creature:
    """Create a new creature."""
    return data.create(creature)


def modify(name: str, creature: Creature) -> Creature | None:
    """Partially patch an existing creature, only the defined fields """
    return data.modify(name, creature)


def replace(name: str, creature: Creature) -> Creature | None:
    """Replace an existing creature."""
    return data.replace(name, creature)


def delete(name: str) -> bool:
    """Delete an existing creature."""
    return data.delete(name)
