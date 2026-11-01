from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(
        ..., min_length=2, max_length=50, description="Nombre del usuario"
    )
    apellido: str = Field(
        ..., min_length=2, max_length=50, description="Apellido del usuario"
    )
    email: EmailStr = Field(..., description="Correo institucional o personal válido")
    rut: str = Field(..., min_length=8, max_length=10, description="RUT del usuario")


class UsuarioResponse(UsuarioCreate):
    id: int

    class Config:
        from_attributes = True
