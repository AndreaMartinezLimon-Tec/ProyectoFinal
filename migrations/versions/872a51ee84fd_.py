"""empty message

Revision ID: 872a51ee84fd
Revises: 
Create Date: 2022-11-30 13:39:41.909825

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '872a51ee84fd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('proveedor',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('telefono', sa.String(length=255), nullable=False),
    sa.Column('marca', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nombre')
    )
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('telefono', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('juguete',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nombre', sa.String(length=255), nullable=False),
    sa.Column('costo', sa.Integer(), nullable=False),
    sa.Column('cantidad', sa.Integer(), nullable=False),
    sa.Column('proveedor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['proveedor_id'], ['proveedor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('juguete_imagen',
    sa.Column('id_imagen', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=128), nullable=False),
    sa.Column('data', sa.LargeBinary(), nullable=False),
    sa.Column('renderate_date', sa.Text(), nullable=False),
    sa.Column('juguete_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['juguete_id'], ['juguete.id'], ),
    sa.PrimaryKeyConstraint('id_imagen')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('juguete_imagen')
    op.drop_table('juguete')
    op.drop_table('usuario')
    op.drop_table('proveedor')
    # ### end Alembic commands ###
