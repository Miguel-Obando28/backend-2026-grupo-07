from app.infrastructure.models.herramienta import HerramientaModel
from sqlalchemy.orm import Session


class HerramientaService:

    @staticmethod
    def obtener_herramientas(
        db: Session, skip: int = 0, limit: int = 10, search: str | None = None
    ):
        query = db.query(HerramientaModel)

        # Filtrar por nombre si se envía el parámetro search
        if search:
            query = query.filter(HerramientaModel.nombre.ilike(f"%{search}%"))

        # Aplicar paginación (skip y limit)
        return query.offset(skip).limit(limit).all()
