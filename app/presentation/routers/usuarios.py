from typing import Annotated

from app.presentation.dependencies import get_db
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
)  # Ajusta según tus schemas
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(dto: UsuarioCreate, db: Annotated[Session, Depends(get_db)]):
    # Aquí puedes llamar a tu servicio de usuario cuando lo tengas integrado
    pass


@router.get("/", response_model=list[UsuarioResponse], status_code=status.HTTP_200_OK)
def listar_usuarios(db: Annotated[Session, Depends(get_db)]):
    # Lógica para listar usuarios desde la base de datos
    pass
