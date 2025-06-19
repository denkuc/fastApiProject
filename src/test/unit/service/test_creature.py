from model.creature import Creature
from service import creature as code

sample = Creature(name="Bigfoot", country="Canada", area="North America", description="Big and hairy", aka="Sasquatch")


def test_create():
    resp = code.create(sample)
    assert resp == sample


def test_get_exists():
    resp = code.get_one(sample.name)
    assert resp == sample


def test_get_not_exists():
    resp = code.get_one("Not a creature")
    assert resp is None
