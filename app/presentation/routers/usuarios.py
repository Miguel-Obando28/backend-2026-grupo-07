from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from fastapi import APIRouter, status

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate):
    # Aquí se llamará al servicio de aplicación
    return usuario


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios():
    # Aquí se llamará al servicio de aplicación
    return []
