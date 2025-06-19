from model.explorer import Explorer

# fake data
_explorers = [
    Explorer(name="Alice", country="Wonderland", description="Curiouser and curiouser"),
    Explorer(name="Bilbo", country="Middle Earth", description="There and back again"),
    Explorer(name="Dorothy", country="Oz", description="There's no place like home"),
    Explorer(name="Dr. Livingstone", country="Africa", description="Dr. Livingstone, I presume")
]


def get_all() -> list[Explorer]:
    """Return a list of all explorers."""
    return _explorers


def get_one(name: str) -> Explorer | None:
    """Return a single explorer by name."""
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None


def create(explorer: Explorer) -> Explorer:
    """Create a new explorer."""
    _explorers.append(explorer)
    return explorer


def modify(name: str, explorer: Explorer) -> Explorer | None:
    """Partially patch an existing explorer, only the defined fields """
    for i, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            _explorers[i] = _explorer.model_copy(update=explorer.model_dump(exclude_unset=True))
            return _explorers[i]


def replace(name: str, explorer: Explorer) -> Explorer | None:
    """Replace an existing explorer."""
    for i, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            _explorers[i] = explorer
            return explorer
    return None


def delete(name: str) -> Explorer | None:
    """Delete an existing explorer."""
    for i, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            _explorers.pop(i)

    return None
