from datetime import UTC, datetime, timedelta

from app.application.mappers import Mapper
from app.schemas.prestamo import PrestamoCreate
from fastapi import HTTPException, status


class PrestamoService:

    @staticmethod
    def registrar_prestamo(
        dto: PrestamoCreate, stock_herramienta: int, prestamos_activos_usuario: int
    ):
        # Regla de Negocio 1: Validar stock de la herramienta
        if stock_herramienta <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La herramienta seleccionada no tiene stock disponible para préstamo.",
            )

        # Regla de Negocio 2: Límite de préstamos activos por usuario
        if prestamos_activos_usuario >= 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ha alcanzado el límite máximo de 3 préstamos activos simultáneos.",
            )

        # Regla de Negocio 3: Asignar fecha esperada automática (7 días) si no viene especificada
        fecha_prestamo = datetime.now(UTC)
        fecha_devolucion = dto.fecha_devolucion_esperada or (
            fecha_prestamo + timedelta(days=7)
        )

        # Estructura simulada previa a la persistencia con ORM
        prestamo_db_simulado = type(
            "PrestamoDB",
            (),
            {
                "id": 1,
                "usuario_id": dto.usuario_id,
                "herramienta_id": dto.herramienta_id,
                "fecha_prestamo": fecha_prestamo,
                "fecha_devolucion_esperada": fecha_devolucion,
                "fecha_devolucion_real": None,
                "estado": "ACTIVO",
            },
        )()

        return Mapper.prestamo_to_response(prestamo_db_simulado)
