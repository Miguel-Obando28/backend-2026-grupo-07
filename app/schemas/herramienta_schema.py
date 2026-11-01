from pydantic import BaseModel, Field


class HerramientaCreate(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    categoria: str = Field(..., min_length=3, max_length=50)
    stock: int = Field(..., gt=0, description="El stock inicial debe ser mayor a 0")


class HerramientaResponse(HerramientaCreate):
    id: int
    disponible: bool

    class Config:
        from_attributes = True
