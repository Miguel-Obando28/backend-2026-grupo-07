from pydantic import BaseModel


# 1. Esquema para la creación (Datos que envía el cliente por POST)
class HerramientaCreate(BaseModel):
    nombre: str
    descripcion: str | None = None
    stock: int
    categoria_id: int


# 2. Esquema para la actualización (Datos opcionales para PUT/PATCH)
class HerramientaUpdate(BaseModel):
    nombre: str | None = None
    descripcion: str | None = None
    stock: int | None = None
    categoria_id: int | None = None


# 3. Esquema para la respuesta (Lo que devuelve la API al cliente)
class HerramientaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str | None = None
    stock: int
    categoria_id: int

    class Config:
        from_attributes = (
            True  # Permite leer datos directamente desde modelos ORM de SQLAlchemy
        )
