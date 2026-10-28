from app.schemas.categoria import CategoriaResponse
from app.schemas.herramienta import HerramientaResponse
from app.schemas.prestamo import PrestamoResponse
from app.schemas.usuario import UsuarioResponse


class Mapper:

    @staticmethod
    def usuario_to_response(usuario_db) -> UsuarioResponse:
        if not usuario_db:
            return None
        return UsuarioResponse(
            id=usuario_db.id,
            nombre=usuario_db.nombre,
            rut=usuario_db.rut,
            email=usuario_db.email,
            telefono=usuario_db.telefono,
        )

    @staticmethod
    def herramienta_to_response(herramienta_db) -> HerramientaResponse:
        if not herramienta_db:
            return None
        return HerramientaResponse(
            id=herramienta_db.id,
            nombre=herramienta_db.nombre,
            descripcion=herramienta_db.descripcion,
            stock=herramienta_db.stock,
            categoria_id=herramienta_db.categoria_id,
        )

    @staticmethod
    def categoria_to_response(categoria_db) -> CategoriaResponse:
        if not categoria_db:
            return None
        return CategoriaResponse(
            id=categoria_db.id,
            nombre=categoria_db.nombre,
            descripcion=categoria_db.descripcion,
        )

    @staticmethod
    def prestamo_to_response(prestamo_db) -> PrestamoResponse:
        if not prestamo_db:
            return None
        return PrestamoResponse(
            id=prestamo_db.id,
            usuario_id=prestamo_db.usuario_id,
            herramienta_id=prestamo_db.herramienta_id,
            fecha_prestamo=prestamo_db.fecha_prestamo,
            fecha_devolucion_esperada=prestamo_db.fecha_devolucion_esperada,
            fecha_devolucion_real=prestamo_db.fecha_devolucion_real,
            estado=prestamo_db.estado,
        )
