"""added_cats is_reserved and relationship cats to user many to one

Revision ID: a85f6317dad6
Revises: 7e74cb57e0c9
Create Date: 2024-01-23 20:32:53.461704

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a85f6317dad6"
down_revision: Union[str, None] = "7e74cb57e0c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "cats",
        sa.Column("is_reserved", sa.Boolean(), server_default="false", nullable=False),
    )
    op.add_column("cats", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "cats", "user", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "cats", type_="foreignkey")
    op.drop_column("cats", "user_id")
    op.drop_column("cats", "is_reserved")
    # ### end Alembic commands ###
