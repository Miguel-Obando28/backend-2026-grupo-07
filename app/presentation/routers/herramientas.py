from typing import Annotated

from app.presentation.dependencies import get_db
from app.schemas.herramienta import (
    HerramientaCreate,
    HerramientaResponse,
)  # Ajusta según tus schemas
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/herramientas", tags=["Herramientas"])


@router.post(
    "/", response_model=HerramientaResponse, status_code=status.HTTP_201_CREATED
)
def crear_herramienta(dto: HerramientaCreate, db: Annotated[Session, Depends(get_db)]):
    # Lógica para registrar nueva herramienta
    pass


@router.get(
    "/", response_model=list[HerramientaResponse], status_code=status.HTTP_200_OK
)
def listar_herramientas(db: Annotated[Session, Depends(get_db)]):
    # Lógica para consultar inventario de herramientas
    pass
