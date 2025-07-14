"""add on delete cascade

Revision ID: 9cf7594fe6f4
Revises: 8771ff8e8fbc
Create Date: 2025-07-09 02:31:32.921338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cf7594fe6f4'
down_revision: Union[str, Sequence[str], None] = '8771ff8e8fbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Primeiro remova a constraint antiga
    op.drop_constraint('reviews_book_id_fkey', 'reviews', type_='foreignkey')

    # Depois adicione novamente com ondelete="CASCADE"
    op.create_foreign_key(
        'reviews_book_id_fkey',
        source_table='reviews',
        referent_table='books',
        local_cols=['book_id'],
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Reverte: remove a nova constraint
    op.drop_constraint('reviews_book_id_fkey', 'reviews', type_='foreignkey')

    # Recria a antiga, sem CASCADE
    op.create_foreign_key(
        'reviews_book_id_fkey',
        source_table='reviews',
        referent_table='books',
        local_cols=['book_id'],
        remote_cols=['id']
        # sem ondelete
    )
