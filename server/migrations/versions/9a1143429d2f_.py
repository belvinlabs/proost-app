"""empty message

Revision ID: 9a1143429d2f
Revises: 385105ddb063
Create Date: 2019-10-24 16:25:19.435762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a1143429d2f'
down_revision = '385105ddb063'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sync', sa.Column('end', sa.DateTime(), nullable=True, comment='A timestamp of when the sync started'))
    op.add_column('sync', sa.Column('start', sa.DateTime(), nullable=True, comment='A timestamp of when the sync started'))
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sync', 'start')
    op.drop_column('sync', 'end')
    # ### end Alembic commands ###


def upgrade_user_db():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_user_db():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

