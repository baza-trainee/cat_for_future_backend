"""update tables

Revision ID: 9b034cb68575
Revises: 22ebce52b91d
Create Date: 2024-01-23 01:58:55.093361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9b034cb68575"
down_revision: Union[str, None] = "22ebce52b91d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("media_path", sa.String(length=500), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("accountability")
    op.add_column(
        "contacts", sa.Column("phone_first", sa.String(length=30), nullable=False)
    )
    op.add_column(
        "contacts", sa.Column("phone_second", sa.String(length=30), nullable=False)
    )
    op.drop_column("contacts", "phone")
    op.drop_column("user", "city")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("city", sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    )
    op.add_column(
        "contacts",
        sa.Column("phone", sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    )
    op.drop_column("contacts", "phone_second")
    op.drop_column("contacts", "phone_first")
    op.create_table(
        "accountability",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "media_path", sa.VARCHAR(length=500), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="accountability_pkey"),
    )
    op.drop_table("documents")
    # ### end Alembic commands ###