from typing import Annotated

from app.infrastructure.models.models import HerramientaModel , PrestamoModel
from app.presentation.dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/herramientas", tags=["Herramientas"])


class HerramientaCreate(BaseModel):
    nombre: str
    codigo_serial: str
    categoria_id: int


class HerramientaResponse(BaseModel):
    id: int
    nombre: str
    codigo_serial: str
    categoria_id: int

    class Config:
        from_attributes = True


@router.post(
    "/", response_model=HerramientaResponse, status_code=status.HTTP_201_CREATED
)
def crear_herramienta(
    herramienta: HerramientaCreate, db: Annotated[Session, Depends(get_db)]
):
    db_herramienta = HerramientaModel(
        nombre=herramienta.nombre,
        codigo_serial=herramienta.codigo_serial,
        categoria_id=herramienta.categoria_id,
    )
    db.add(db_herramienta)
    db.commit()
    db.refresh(db_herramienta)
    return db_herramienta


@router.get(
    "/", response_model=list[HerramientaResponse], status_code=status.HTTP_200_OK
)
def listar_herramientas(
    skip: int = Query(0, description="Cantidad de registros a saltar (paginación)"),
    limit: int = Query(100, description="Límite de registros a retornar"),
    categoria_id: int | None = Query(None, description="Filtrar por ID de categoría"),
    search: str | None = Query(
        None, description="Buscar por coincidencia en el nombre"
    ),
    sort_by: str | None = Query(
        "id", description="Campo para ordenar (ej. id, nombre)"
    ),
    order: str | None = Query("asc", description="Dirección del orden: asc o desc"),
    db: Annotated[Session, Depends(get_db)] = None,
):
    query = db.query(HerramientaModel)

    # 1. Filtrado por categoría si se proporciona
    if categoria_id is not None:
        query = query.filter(HerramientaModel.categoria_id == categoria_id)

    # 2. Filtrado por texto (búsqueda parcial en el nombre)
    if search:
        query = query.filter(HerramientaModel.nombre.ilike(f"%{search}%"))

    # 3. Ordenamiento dinámico
    if hasattr(HerramientaModel, sort_by):
        sort_column = getattr(HerramientaModel, sort_by)
        if order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

    # 4. Paginación y ejecución
    herramientas = query.offset(skip).limit(limit).all()
    return herramientas


@router.get(
    "/{herramienta_id}",
    response_model=HerramientaResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_herramienta(herramienta_id: int, db: Annotated[Session, Depends(get_db)]):
    herramienta = (
        db.query(HerramientaModel).filter(HerramientaModel.id == herramienta_id).first()
    )
    if not herramienta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Herramienta no encontrada"
        )
    return herramienta


@router.put(
    "/{herramienta_id}",
    response_model=HerramientaResponse,
    status_code=status.HTTP_200_OK,
)
def actualizar_herramienta(
    herramienta_id: int,
    datos: HerramientaCreate,
    db: Annotated[Session, Depends(get_db)],
):
    herramienta = (
        db.query(HerramientaModel)
        .filter(HerramientaModel.id == herramienta_id)
        .first()
    )
    if herramienta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Herramienta no encontrada.",
        )
    herramienta.nombre = datos.nombre
    herramienta.codigo_serial = datos.codigo_serial
    herramienta.categoria_id = datos.categoria_id
    try:
        db.commit()
        db.refresh(herramienta)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El código serial ya existe o la categoría no es válida.",
        )
    return herramienta


@router.delete("/{herramienta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_herramienta(
    herramienta_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    herramienta = (
        db.query(HerramientaModel)
        .filter(HerramientaModel.id == herramienta_id)
        .first()
    )
    if herramienta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Herramienta no encontrada.",
        )
    tiene_prestamos = (
        db.query(PrestamoModel)
        .filter(PrestamoModel.herramienta_id == herramienta_id)
        .first()
    )
    if tiene_prestamos:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar: la herramienta tiene préstamos asociados.",
        )
    db.delete(herramienta)
    db.commit()
