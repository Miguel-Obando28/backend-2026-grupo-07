from pydantic import BaseModel, Field


# Creación de categoría
class CategoriaCreate(BaseModel):
    nombre: str = Field(
        ..., min_length=2, max_length=50, description="Nombre de la categoría"
    )
    descripcion: str | None = Field(
        None, max_length=255, description="Descripción opcional"
    )


# Actualización
class CategoriaUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=2, max_length=50)
    descripcion: str | None = Field(None, max_length=255)


# Respuesta
class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None

    class Config:
        from_attributes = True
