from datetime import datetime

from pydantic import BaseModel, Field


# Registrar un nuevo préstamo
class PrestamoCreate(BaseModel):
    usuario_id: int = Field(..., gt=0, description="ID válido del usuario")
    herramienta_id: int = Field(..., gt=0, description="ID válido de la herramienta")
    fecha_devolucion_esperada: datetime = Field(
        ..., description="Fecha límite estimada"
    )


# Actualizar el estado o devolución del préstamo
class PrestamoUpdate(BaseModel):
    estado: str | None = Field(
        None, min_length=3, max_length=30
    )  # Ej: "Devuelto", "Atrasado"
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
