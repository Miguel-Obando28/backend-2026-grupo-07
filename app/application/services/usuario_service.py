from app.infrastructure.models.models import UsuarioModel
from sqlalchemy.orm import Session


class UsuarioService:

    @staticmethod
    def obtener_usuarios(db: Session):
        return db.query(UsuarioModel).all()

    @staticmethod
    def obtener_usuario_por_id(db: Session, usuario_id: int):
        return db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
