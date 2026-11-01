from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base

# 1. Entidad Categoría
class CategoriaModel(Base):
    __tablename__ = "categorias"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(255), nullable=True)
    
    # Relación 1:N con Herramientas
    herramientas = relationship("HerramientaModel", back_populates="categoria")

# 2. Entidad Herramienta
class HerramientaModel(Base):
    __tablename__ = "herramientas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo_serial = Column(String(50), unique=True, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    
    categoria = relationship("CategoriaModel", back_populates="herramientas")
    prestamos = relationship("PrestamoModel", back_populates="herramienta")

# 3. Entidad Usuario
class UsuarioModel(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    rol = Column(String(50), default="estudiante")
    
    prestamos = relationship("PrestamoModel", back_populates="usuario")

# 4. Entidad Préstamo
class PrestamoModel(Base):
    __tablename__ = "prestamos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    herramienta_id = Column(Integer, ForeignKey("herramientas.id"), nullable=False)
    estado = Column(String(50), default="activo") # activo, devuelto
    
    usuario = relationship("UsuarioModel", back_populates="prestamos")
    herramienta = relationship("HerramientaModel", back_populates="prestamos")