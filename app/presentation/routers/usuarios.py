from typing import Annotated

from app.application.services.usuario_service import UsuarioService
from app.presentation.dependencies import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(dto: UsuarioCreate, db: Annotated[Session, Depends(get_db)]):
    return UsuarioService.crear_usuario(db, dto)


@router.get("/", response_model=list[UsuarioResponse], status_code=status.HTTP_200_OK)
def listar_usuarios(db: Annotated[Session, Depends(get_db)]):
    return UsuarioService.obtener_usuarios(db)
