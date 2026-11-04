from typing import Annotated

from app.infrastructure.models.models import (
    HerramientaModel,
    PrestamoModel,
    UsuarioModel,
)
from app.presentation.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


class PrestamoCreate(BaseModel):
    herramienta_id: int
    usuario_id: int


class PrestamoResponse(BaseModel):
    id: int
    herramienta_id: int
    usuario_id: int
    estado: str

    class Config:
        from_attributes = True


@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
def crear_prestamo(prestamo: PrestamoCreate, db: Annotated[Session, Depends(get_db)]):
    # 1. Validar que el usuario exista
    usuario = (
        db.query(UsuarioModel).filter(UsuarioModel.id == prestamo.usuario_id).first()
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario especificado no existe.",
        )

    # 2. Validar que la herramienta exista
    herramienta = (
        db.query(HerramientaModel)
        .filter(HerramientaModel.id == prestamo.herramienta_id)
        .first()
    )
    if not herramienta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La herramienta especificada no existe.",
        )

    # 3. Validar si la herramienta ya se encuentra prestada (activo)
    prestamo_activo = (
        db.query(PrestamoModel)
        .filter(
            PrestamoModel.herramienta_id == prestamo.herramienta_id,
            PrestamoModel.estado == "activo",
        )
        .first()
    )

    if prestamo_activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La herramienta ya se encuentra en préstamo activo.",
        )

    # 4. Crear el préstamo si pasa todas las validaciones
    db_prestamo = PrestamoModel(
        herramienta_id=prestamo.herramienta_id,
        usuario_id=prestamo.usuario_id,
        estado="activo",
    )
    db.add(db_prestamo)
    db.commit()
    db.refresh(db_prestamo)
    return db_prestamo


@router.get("/", response_model=list[PrestamoResponse], status_code=status.HTTP_200_OK)
def listar_prestamos(
    skip: int = 0, limit: int = 100, db: Annotated[Session, Depends(get_db)] = None
):
    return db.query(PrestamoModel).offset(skip).limit(limit).all()


@router.put(
    "/{prestamo_id}/devolver",
    response_model=PrestamoResponse,
    status_code=status.HTTP_200_OK,
)
def devolver_prestamo(prestamo_id: int, db: Annotated[Session, Depends(get_db)]):
    prestamo = db.query(PrestamoModel).filter(PrestamoModel.id == prestamo_id).first()
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Préstamo no encontrado"
        )

    prestamo.estado = "devuelto"
    db.commit()
    db.refresh(prestamo)
    return prestamo
