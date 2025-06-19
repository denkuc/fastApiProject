import os
import pytest
from model.creature import Creature
from errors import Missing, Duplicate


os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Harmless, but elusive",
        aka="Abominable Snowman"
    )


def test_create(sample: Creature):
    resp = creature.create(sample)
    assert creature == resp


def test_create_duplicate(sample: Creature):
    creature.create(sample)
    with pytest.raises(Duplicate):
        creature.create(sample)


def test_get_one(sample: Creature):
    resp = creature.get_one(sample.name)
    assert sample == resp


def test_get_one_missing():
    with pytest.raises(Missing):
        creature.get_one("chupacabra")


def test_modify(sample: Creature):
    sample.area = "Rocky Mountains"
    resp = creature.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    new_sample = Creature(
        name="chupacabra",
        country="PR",
        area="Caribbean",
        description="Vampiric goat-sucker",
        aka="El Chupacabra"
    )
    with pytest.raises(Missing):
        creature.modify(new_sample.name, new_sample)


def test_delete(sample: Creature):
    resp = creature.delete(sample.name)
    assert resp is None


def test_delete_missing(sample: Creature):
    with pytest.raises(Missing):
        creature.delete(sample.name)
