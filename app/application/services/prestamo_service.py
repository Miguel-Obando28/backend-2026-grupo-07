from datetime import UTC, datetime, timedelta

from app.application.mappers import Mapper
from app.infrastructure.repositories.prestamo_repository import PrestamoRepository
from app.schemas.prestamo import PrestamoCreate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session


class PrestamoService:

    @staticmethod
    def registrar_prestamo(db: Session, dto: PrestamoCreate):
        # 1. Obtener stock real desde la base de datos usando el repositorio
        stock_herramienta = PrestamoRepository.obtener_stock_herramienta(
            db, dto.herramienta_id
        )

        # Regla de Negocio 1: Validar stock de la herramienta
        if stock_herramienta <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La herramienta seleccionada no tiene stock disponible para préstamo.",
            )

        # 2. Obtener conteo de préstamos activos del usuario desde el repositorio
        prestamos_activos = PrestamoRepository.contar_prestamos_activos_por_usuario(
            db, dto.usuario_id
        )

        # Regla de Negocio 2: Límite de préstamos activos por usuario
        if prestamos_activos >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ha alcanzado el límite máximo de 3 préstamos activos simultáneos.",
            )

        # Regla de Negocio 3: Asignar fecha esperada automática (7 días) si no viene especificada
        fecha_prestamo = datetime.now(UTC)
        fecha_devolucion = dto.fecha_devolucion_esperada or (
            fecha_prestamo + timedelta(days=7)
        )

        # Datos para guardar
        prestamo_data = {
            "usuario_id": dto.usuario_id,
            "herramienta_id": dto.herramienta_id,
            "fecha_prestamo": fecha_prestamo,
            "fecha_devolucion_esperada": fecha_devolucion,
            "estado": "ACTIVO",
        }

        # Guardar en la base de datos real
        prestamo_db = PrestamoRepository.guardar_prestamo(db, prestamo_data)

        return Mapper.prestamo_to_response(prestamo_db)
