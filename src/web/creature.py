from fastapi import APIRouter, HTTPException

from errors import Missing, Duplicate
from model.creature import Creature
import service.creature as service


router = APIRouter(prefix="/creature", tags=["creature"])


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    """Return a list of all creatures."""
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    """Return a single creature by name."""
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(creature: Creature) -> Creature:
    """Create a new creature."""
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature | None:
    """Partially patch an existing creature, only the defined fields """
    try:
        return service.modify(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature | None:
    """Replace an existing creature."""
    try:
        return service.replace(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.delete("/{name}")
def delete(name: str) -> bool:
    """Delete an existing creature."""
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.message)
