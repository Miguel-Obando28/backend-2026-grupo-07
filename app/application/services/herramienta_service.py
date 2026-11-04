from app.infrastructure.models.models import HerramientaModel
from app.schemas.herramienta import HerramientaCreate, HerramientaUpdate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class HerramientaService:

    @staticmethod
    def crear_herramienta(db: Session, herramienta: HerramientaCreate):
        db_herramienta = HerramientaModel(**herramienta.dict())
        db.add(db_herramienta)
        db.commit()
        db.refresh(db_herramienta)
        return db_herramienta

    @staticmethod
    def obtener_herramientas(
        db: Session, skip: int = 0, limit: int = 100, search: str | None = None
    ):
        query = db.query(HerramientaModel)
        if search:
            query = query.filter(HerramientaModel.nombre.ilike(f"%{search}%"))
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def obtener_herramienta_por_id(db: Session, herramienta_id: int):
        herramienta = (
            db.query(HerramientaModel)
            .filter(HerramientaModel.id == herramienta_id)
            .first()
        )
        if not herramienta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Herramienta no encontrada",
            )
        return herramienta

    @staticmethod
    def actualizar_herramienta(
        db: Session, herramienta_id: int, herramienta_data: HerramientaUpdate
    ):
        herramienta = HerramientaService.obtener_herramienta_por_id(db, herramienta_id)

        update_data = herramienta_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(herramienta, key, value)

        db.commit()
        db.refresh(herramienta)
        return herramienta

    @staticmethod
    def eliminar_herramienta(db: Session, herramienta_id: int):
        herramienta = HerramientaService.obtener_herramienta_por_id(db, herramienta_id)
        db.delete(herramienta)
        db.commit()
