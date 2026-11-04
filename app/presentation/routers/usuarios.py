from typing import Annotated

from app.infrastructure.models.models import UsuarioModel
from app.presentation.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    rol: str = "estudiante"


class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str

    class Config:
        from_attributes = True


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        db_usuario = UsuarioModel(
            nombre=usuario.nombre, email=usuario.email, rol=usuario.rol
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo electrónico ya se encuentra registrado.",
        )


@router.get("/", response_model=list[UsuarioResponse], status_code=status.HTTP_200_OK)
def listar_usuarios(
    skip: int = 0, limit: int = 100, db: Annotated[Session, Depends(get_db)] = None
):
    return db.query(UsuarioModel).offset(skip).limit(limit).all()
