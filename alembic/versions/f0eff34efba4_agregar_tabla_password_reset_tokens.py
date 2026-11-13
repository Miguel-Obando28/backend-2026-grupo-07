"""agregar_tabla_password_reset_tokens

Revision ID: f0eff34efba4
Revises: f01d7abe6f7e
Create Date: 2026-11-13 02:19:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f0eff34efba4"
down_revision = "f01d7abe6f7e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "password_reset_tokens",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("jti", sa.String(), nullable=False, unique=True),
        sa.Column(
            "user_id", sa.Integer(), sa.ForeignKey("usuarios.id"), nullable=False
        ),
        sa.Column("used", sa.Boolean(), default=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("password_reset_tokens")
