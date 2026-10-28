from app.schemas.prestamo import PrestamoCreate, PrestamoResponse
from fastapi import APIRouter, status

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
def registrar_prestamo(prestamo: PrestamoCreate):
    return prestamo


@router.get("/", response_model=list[PrestamoResponse])
def listar_prestamos():
    return []
