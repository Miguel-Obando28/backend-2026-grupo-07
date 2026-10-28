from pydantic import BaseModel, EmailStr


# Datos requeridos para registrar un usuario
class UsuarioCreate(BaseModel):
    nombre: str
    rut: str
    email: EmailStr
    telefono: str | None = None


# Datos opcionales para actualizar un usuario
class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None


# Datos devueltos al cliente
class UsuarioResponse(BaseModel):
    id: int
    nombre: str
    rut: str
    email: EmailStr
    telefono: str | None = None

    class Config:
        from_attributes = True
