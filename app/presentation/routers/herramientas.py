from typing import Annotated

from app.application.services.herramienta_service import HerramientaService
from app.presentation.dependencies import get_db
from app.schemas.herramienta_schema import HerramientaResponse
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/herramientas", tags=["Herramientas"])


@router.get(
    "/", response_model=list[HerramientaResponse], status_code=status.HTTP_200_OK
)
def listar_herramientas(
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0, description="Registros a omitir para la paginación"),
    limit: int = Query(
        10, ge=1, le=100, description="Cantidad máxima de registros por página"
    ),
    search: str | None = Query(None, description="Término para filtrar por nombre"),
):
    # Pasamos los parámetros al servicio
    return HerramientaService.obtener_herramientas(
        db, skip=skip, limit=limit, search=search
    )
