import uuid

from app.infrastructure.database import get_db
from app.infrastructure.models.models import (
    UsuarioModel as User,
)  # <-- Importación corregida apuntando al modelo unificado
from app.infrastructure.models.password_reset import PasswordResetToken
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth/password", tags=["Password Reset"])


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str


@router.post("/forgot")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # 1. Buscar usuario por email (si no existe, se da respuesta genérica por seguridad)
    user = db.query(User).filter(User.email == payload.email).first()
    generic_response = {
        "message": "Si el correo existe, se ha enviado un enlace de recuperación."
    }

    if not user:
        return generic_response

    # 2. Generar JTI único para asegurar que el enlace sea de un solo uso
    token_jti = str(uuid.uuid4())

    # 3. Guardar el JTI en la base de datos como no utilizado
    db_token = PasswordResetToken(jti=token_jti, user_id=user.id, used=False)
    db.add(db_token)
    db.commit()

    # 4. Retornar el enlace con el token generado
    return {
        "message": "Enlace generado con éxito",
        "reset_link": f"http://localhost:3000/reset-password?token={token_jti}",
    }


@router.post("/reset", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    # 1. Buscar el token en la base de datos por su JTI
    db_token = (
        db.query(PasswordResetToken)
        .filter(PasswordResetToken.jti == payload.reset_token)
        .first()
    )

    if not db_token or db_token.used:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido, expirado o ya utilizado",
        )

    # 2. Buscar al usuario asociado
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado"
        )

    # 3. Actualizar la contraseña y marcar el token como utilizado (Transacción)
    try:
        # Nota: Asegúrate de usar la función de hasheo si tu proyecto la requiere (ej. get_password_hash)
        user.hashed_password = payload.new_password
        db_token.used = True

        db.add(user)
        db.add(db_token)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la contraseña",
        )
