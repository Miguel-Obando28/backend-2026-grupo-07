from datetime import datetime

from pydantic import BaseModel


# Registrar un nuevo préstamo
class PrestamoCreate(BaseModel):
    usuario_id: int
    herramienta_id: int
    fecha_devolucion_esperada: datetime


# Actualizar el estado o devolución del préstamo
class PrestamoUpdate(BaseModel):
    estado: str | None = None  # Ej: "Devuelto", "Atrasado"
    fecha_devolucion_real: datetime | None = None


# Respuesta completa del préstamo
class PrestamoResponse(BaseModel):
    id: int
    usuario_id: int
    herramienta_id: int
    fecha_prestamo: datetime
    fecha_devolucion_esperada: datetime
    fecha_devolucion_real: datetime | None = None
    estado: str

    class Config:
        from_attributes = True
