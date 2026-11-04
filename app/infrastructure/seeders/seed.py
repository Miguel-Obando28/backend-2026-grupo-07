from app.infrastructure.database import SessionLocal
from app.infrastructure.models.models import (
    CategoriaModel,
    HerramientaModel,
    PrestamoModel,
    UsuarioModel,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


def run_seeders():
    db: Session = SessionLocal()
    try:
        # 1. Crear Categorías
        cat1 = db.query(CategoriaModel).filter_by(nombre="Electricidad").first()
        if not cat1:
            cat1 = CategoriaModel(nombre="Electricidad")
            db.add(cat1)

        cat2 = db.query(CategoriaModel).filter_by(nombre="Carpintería").first()
        if not cat2:
            cat2 = CategoriaModel(nombre="Carpintería")
            db.add(cat2)
        db.commit()

        # 2. Crear Herramientas con su codigo_serial obligatorio
        herrc1 = db.query(HerramientaModel).filter_by(codigo_serial="TLD-001").first()
        if not herrc1:
            herrc1 = HerramientaModel(
                nombre="Taladro Percutor",
                codigo_serial="TLD-001",
                categoria_id=cat1.id,
            )
            db.add(herrc1)

        herrc2 = db.query(HerramientaModel).filter_by(codigo_serial="SRC-002").first()
        if not herrc2:
            herrc2 = HerramientaModel(
                nombre="Sierra Circular",
                codigo_serial="SRC-002",
                categoria_id=cat2.id,
            )
            db.add(herrc2)
        db.commit()

        # 3. Crear Usuarios
        user1 = db.query(UsuarioModel).filter_by(email="ana@example.com").first()
        if not user1:
            user1 = UsuarioModel(nombre="Ana Gómez", email="ana@example.com")
            db.add(user1)

        user2 = db.query(UsuarioModel).filter_by(email="carlos@example.com").first()
        if not user2:
            user2 = UsuarioModel(nombre="Carlos Ruiz", email="carlos@example.com")
            db.add(user2)
        db.commit()

        # 4. Crear Préstamos
        if user1 and herrc1:
            prestamo1 = (
                db.query(PrestamoModel)
                .filter_by(usuario_id=user1.id, herramienta_id=herrc1.id)
                .first()
            )
            if not prestamo1:
                prestamo1 = PrestamoModel(usuario_id=user1.id, herramienta_id=herrc1.id)
                db.add(prestamo1)

        if user2 and herrc2:
            prestamo2 = (
                db.query(PrestamoModel)
                .filter_by(usuario_id=user2.id, herramienta_id=herrc2.id)
                .first()
            )
            if not prestamo2:
                prestamo2 = PrestamoModel(usuario_id=user2.id, herramienta_id=herrc2.id)
                db.add(prestamo2)
        db.commit()

        print("¡Seeders ejecutados exitosamente!")
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error de base de datos al ejecutar los seeders: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run_seeders()
