from pydantic import BaseModel


# Creación de categoría
class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: str | None = None


# Actualización
class CategoriaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None


# Respuesta
class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None

    class Config:
        from_attributes = True
