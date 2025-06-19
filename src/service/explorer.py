from model.explorer import Explorer
import data.explorer as data


def get_all() -> list[Explorer]:
    """Return a list of all explorers."""
    return data.get_all()


def get_one(name: str) -> Explorer | None:
    """Return a single explorer by name."""
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer:
    """Create a new explorer."""
    return data.create(explorer)


def modify(name: str, explorer: Explorer) -> Explorer | None:
    """Partially patch an existing explorer, only the defined fields """
    return data.modify(name, explorer)


def replace(name: str, explorer: Explorer) -> Explorer | None:
    """Replace an existing explorer."""
    return data.replace(name, explorer)


def delete(name: str) -> Explorer | None:
    """Delete an existing explorer."""
    return data.delete(name)
