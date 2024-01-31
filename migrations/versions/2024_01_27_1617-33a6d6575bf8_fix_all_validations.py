"""fix all validations

Revision ID: 33a6d6575bf8
Revises: a85f6317dad6
Create Date: 2024-01-27 16:17:43.449946

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "33a6d6575bf8"
down_revision: Union[str, None] = "a85f6317dad6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "cat_photos",
        "media_path",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=500),
        existing_nullable=False,
    )
    op.alter_column(
        "cats",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=10),
        existing_nullable=True,
    )
    op.alter_column(
        "cats",
        "description",
        existing_type=sa.VARCHAR(length=2000),
        type_=sa.String(length=200),
        existing_nullable=True,
    )
    op.drop_constraint("cats_user_id_fkey", "cats", type_="foreignkey")
    op.create_foreign_key(
        None, "cats", "user", ["user_id"], ["id"], ondelete="SET NULL"
    )
    op.alter_column(
        "contacts",
        "email",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=35),
        existing_nullable=False,
    )
    op.alter_column(
        "contacts",
        "post_address",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=100),
        existing_nullable=True,
    )
    op.alter_column(
        "documents",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=120),
        existing_nullable=False,
    )
    op.alter_column(
        "hero",
        "title",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=120),
        existing_nullable=False,
    )
    op.alter_column(
        "hero",
        "sub_title",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=120),
        existing_nullable=False,
    )
    op.alter_column(
        "hero",
        "left_text",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "instructions",
        "title",
        existing_type=sa.VARCHAR(length=150),
        type_=sa.String(length=120),
        existing_nullable=False,
    )
    op.alter_column(
        "instructions",
        "description",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=500),
        existing_nullable=False,
    )
    op.alter_column(
        "stories",
        "title",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=120),
        existing_nullable=True,
    )
    op.alter_column(
        "user",
        "name",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=25),
        existing_nullable=True,
    )
    op.alter_column(
        "user",
        "email",
        existing_type=sa.VARCHAR(length=100),
        type_=sa.String(length=50),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user",
        "email",
        existing_type=sa.String(length=50),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "user",
        "name",
        existing_type=sa.String(length=25),
        type_=sa.VARCHAR(length=100),
        existing_nullable=True,
    )
    op.alter_column(
        "stories",
        "title",
        existing_type=sa.String(length=120),
        type_=sa.VARCHAR(length=200),
        existing_nullable=True,
    )
    op.alter_column(
        "instructions",
        "description",
        existing_type=sa.String(length=500),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    op.alter_column(
        "instructions",
        "title",
        existing_type=sa.String(length=120),
        type_=sa.VARCHAR(length=150),
        existing_nullable=False,
    )
    op.alter_column(
        "hero",
        "left_text",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    op.alter_column(
        "hero",
        "sub_title",
        existing_type=sa.String(length=120),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    op.alter_column(
        "hero",
        "title",
        existing_type=sa.String(length=120),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    op.alter_column(
        "documents",
        "name",
        existing_type=sa.String(length=120),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "contacts",
        "email",
        existing_type=sa.String(length=35),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    op.alter_column(
        "contacts",
        "post_address",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=200),
        existing_nullable=True,
    )
    op.drop_constraint(None, "cats", type_="foreignkey")
    op.create_foreign_key("cats_user_id_fkey", "cats", "user", ["user_id"], ["id"])
    op.alter_column(
        "cats",
        "description",
        existing_type=sa.String(length=200),
        type_=sa.VARCHAR(length=2000),
        existing_nullable=True,
    )
    op.alter_column(
        "cats",
        "name",
        existing_type=sa.String(length=10),
        type_=sa.VARCHAR(length=100),
        existing_nullable=True,
    )
    op.alter_column(
        "cat_photos",
        "media_path",
        existing_type=sa.String(length=500),
        type_=sa.VARCHAR(length=200),
        existing_nullable=False,
    )
    # ### end Alembic commands ###