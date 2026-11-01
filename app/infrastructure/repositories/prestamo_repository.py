from app.infrastructure.models.models import HerramientaModel, PrestamoModel
from sqlalchemy.orm import Session


class PrestamoRepository:

    @staticmethod
    def contar_prestamos_activos_por_usuario(db: Session, usuario_id: int) -> int:
        """Cuenta cuántos préstamos activos tiene un usuario (Regla de negocio: máx 3)."""
        return (
            db.query(PrestamoModel)
            .filter(
                PrestamoModel.usuario_id == usuario_id, PrestamoModel.estado == "ACTIVO"
            )
            .count()
        )

    @staticmethod
    def obtener_stock_herramienta(db: Session, herramienta_id: int) -> int:
        """Obtiene el stock actual de una herramienta."""
        herramienta = (
            db.query(HerramientaModel)
            .filter(HerramientaModel.id == herramienta_id)
            .first()
        )
        return herramienta.stock if herramienta else 0

    @staticmethod
    def guardar_prestamo(db: Session, prestamo_data: dict) -> PrestamoModel:
        """Inserta un nuevo préstamo en la base de datos."""
        nuevo_prestamo = PrestamoModel(**prestamo_data)
        db.add(nuevo_prestamo)
        db.commit()
        db.refresh(nuevo_prestamo)
        return nuevo_prestamo
