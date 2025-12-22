"""Add mock data

Revision ID: 12f4c22ca083
Revises: 0893dc289ca0
Create Date: 2025-10-31 02:57:35.699623

"""
from typing import Sequence, Union
import uuid
from datetime import date
from passlib.context import CryptContext
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12f4c22ca083'
down_revision: Union[str, Sequence[str], None] = '0893dc289ca0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def upgrade() -> None:
    """Upgrade schema."""
    user_table = sa.table('T_Users',
        sa.column('user_id', sa.UUID(as_uuid=True)),
        sa.column('user_login', sa.String),
        sa.column('user_password', sa.String),
        sa.column('user_name', sa.String)
    )
    user_data = [
        {
            'user_id': uuid.uuid4(),
            'user_login': 'ivanov@gmail.com',
            'user_password': pwd_context.hash('hello123'.encode('utf-8')[:72].decode('utf-8', 'ignore')),
            'user_name': 'Ivan'
        },
        {
            'user_id': uuid.uuid4(),
            'user_login': 'admin@gmail.com',
            'user_password': pwd_context.hash('admin'.encode('utf-8')[:72].decode('utf-8', 'ignore')),
            'user_name': 'Admin'
        }
    ]
    op.bulk_insert(user_table, user_data)

    producttype_table = sa.table('T_ProductTypes',
        sa.column('prodtype_id', sa.UUID(as_uuid=True)),
        sa.column('prodtype_name', sa.String)
        )
    producttype_data = [
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Молочные продукты'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Алкогольные напитки'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Газированные напитки'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Ферментированные напитки'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Овощи'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Фрукты'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Консервы'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Рыба и морепродукты'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Соусы'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Продукты из мяса'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Продукты сельскохозяйственного производства'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Еда и напитки из растительного сырья'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Сладкие закуски'
        },
        {
            'prodtype_id': uuid.uuid4(),
            'prodtype_name': 'Соленые закуски'
        }
    ]
    op.bulk_insert(producttype_table, producttype_data)

    product_table = sa.table('T_Products',
        sa.column('product_id', sa.UUID(as_uuid=True)),
        sa.column('product_name', sa.String),
        sa.column('product_thumbnail', sa.String),
        sa.column('product_type', sa.UUID(as_uuid=True)),
        sa.column('product_desc', sa.String),
        sa.column('product_rating', sa.Float),
        sa.column('product_barcode', sa.BigInteger)
        )
    product_data = [
        {
            'product_id': uuid.uuid4(),
            'product_name': 'Сметана',
            'product_thumbnail': None,
            'product_type': producttype_data[10]['prodtype_id'],
            'product_desc': 'Сметана 15% 100г',
            'product_rating': None,
            'product_barcode': 123321123
        },
        {
            'product_id': uuid.uuid4(),
            'product_name': 'Батон летний',
            'product_thumbnail': None,
            'product_type': producttype_data[10]['prodtype_id'],
            'product_desc': 'Батон 300 грамм, не нарезан',
            'product_rating': None,
            'product_barcode': 111222333
        }
    ]
    op.bulk_insert(product_table, product_data)

    order_table = sa.table("T_Orders",
        sa.column('order_id', sa.UUID(as_uuid=True)),
        sa.column('id_user', sa.UUID(as_uuid=True)),
        sa.column('order_date', sa.Date)
        )
    order_data = [
        {
            'order_id': uuid.uuid4(),
            'id_user': user_data[1]['user_id'],
            'order_date': date.today()
        }
    ]
    op.bulk_insert(order_table, order_data)

    orderproduct_table = sa.table("T_OrdersProducts",
        sa.column('order_product_id', sa.UUID(as_uuid=True)),
        sa.column('id_order', sa.UUID(as_uuid=True)),
        sa.column('id_product', sa.UUID(as_uuid=True)),
        sa.column('product_date_start', sa.Date),
        sa.column('product_date_end', sa.Date)
    )
    orderproduct_data = [
        {
            'order_product_id': uuid.uuid4(),
            'id_order': order_data[0]['order_id'],
            'id_product': product_data[0]['product_id'],
            'product_date_start': None,
            'product_date_end': date.today()
        },
        {
            'order_product_id': uuid.uuid4(),
            'id_order': order_data[0]['order_id'],
            'id_product': product_data[1]['product_id'],
            'product_date_start': None,
            'product_date_end': date.today()
        }
    ]
    op.bulk_insert(orderproduct_table, orderproduct_data)

def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM T_OrderProduct")
    op.execute("DELETE FROM T_Products")
    op.execute("DELETE FROM T_ProdcutTypes")
    op.execute("DELETE FROM T_Orders")
    op.execute("DELETE FROM T_Products")
