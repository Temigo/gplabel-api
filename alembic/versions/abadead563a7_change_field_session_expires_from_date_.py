"""change field Session.expires from date to datetime

Revision ID: abadead563a7
Revises: d8d9e5a51799
Create Date: 2023-06-03 17:36:18.614207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abadead563a7'
down_revision = 'd8d9e5a51799'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
