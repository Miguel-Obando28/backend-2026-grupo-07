from app.schemas.herramienta import HerramientaCreate, HerramientaResponse
from fastapi import APIRouter, status

router = APIRouter(prefix="/herramientas", tags=["Herramientas"])


@router.post(
    "/", response_model=HerramientaResponse, status_code=status.HTTP_201_CREATED
)
def crear_herramienta(herramienta: HerramientaCreate):
    return herramienta


@router.get("/", response_model=list[HerramientaResponse])
def listar_herramientas():
    return []
