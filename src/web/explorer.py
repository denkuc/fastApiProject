from fastapi import APIRouter, HTTPException

from errors import Missing, Duplicate
from model.explorer import Explorer
import service.explorer as service


router = APIRouter(prefix="/explorer", tags=["explorer"])


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    """Return a list of all explorers."""
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> Explorer:
    """Return a single explorer by name."""
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(explorer: Explorer) -> Explorer:
    """Create a new explorer."""
    try:
        return service.create(explorer)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.patch("/{name}")
def modify(name: str, explorer: Explorer) -> Explorer | None:
    """Partially patch an existing explorer, only the defined fields """
    try:
        return service.modify(name, explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.put("/{name}")
def replace(name: str, explorer: Explorer) -> Explorer | None:
    """Replace an existing explorer."""
    try:
        return service.replace(name, explorer)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.message)


@router.delete("/{name}")
def delete(name: str) -> Explorer | None:
    """Delete an existing explorer."""
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.message)
