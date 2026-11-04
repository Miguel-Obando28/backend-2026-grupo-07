from pydantic import BaseModel


class HerramientaBase(BaseModel):
    nombre: str
    codigo_serial: str
    categoria_id: int


class HerramientaCreate(HerramientaBase):
    pass


class HerramientaUpdate(BaseModel):
    nombre: str | None = None
    codigo_serial: str | None = None
    categoria_id: int | None = None


class HerramientaResponse(HerramientaBase):
    id: int

    class Config:
        from_attributes = True
