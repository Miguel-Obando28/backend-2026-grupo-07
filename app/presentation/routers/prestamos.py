from typing import Annotated

from app.application.services.prestamo_service import PrestamoService
from app.presentation.dependencies import get_db
from app.schemas.prestamo import PrestamoCreate, PrestamoResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
def crear_prestamo(dto: PrestamoCreate, db: Annotated[Session, Depends(get_db)]):
    return PrestamoService.registrar_prestamo(db, dto)
