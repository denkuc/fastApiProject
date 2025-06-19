from model.creature import Creature


_creatures = [
    Creature(name="Bigfoot", country="Canada", area="North America", description="Big and hairy", aka="Sasquatch"),
    Creature(name="Loch Ness Monster", country="Scotland", area="Loch Ness", description="Long and scaly", aka="Nessie"),
    Creature(name="Mothman", country="USA", area="West Virginia", description="Tall and feathery", aka="The Point Pleasant Mothman"),
    Creature(name="Yeti", country="Nepal", area="Himalayas", description="White and furry", aka="The Abominable Snowman")
]


def get_all() -> list[Creature]:
    """Return a list of all creatures."""
    return _creatures


def get_one(name: str) -> Creature | None:
    """Return a single creature by name."""
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None


def create(creature: Creature) -> Creature:
    """Create a new creature."""
    _creatures.append(creature)
    return creature


def modify(name: str, creature: Creature) -> Creature | None:
    """Partially patch an existing creature, only the defined fields """
    for i, _creature in enumerate(_creatures):
        if _creature.name == name:
            _creatures[i] = _creature.model_copy(update=creature.model_dump(exclude_unset=True))
            return _creatures[i]


def replace(name: str, creature: Creature) -> Creature | None:
    """Replace an existing creature."""
    for i, _creature in enumerate(_creatures):
        if _creature.name == name:
            _creatures[i] = creature
            return creature
    return None


def delete(name: str) -> Creature | None:
    """Delete an existing creature."""
    for i, _creature in enumerate(_creatures):
        if _creature.name == name:
            _creatures.pop(i)

    return None
