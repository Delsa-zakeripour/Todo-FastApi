"""Create phone number for user column

Revision ID: 6021d4be4182
Revises: 
Create Date: 2026-09-19 16:36:42.734347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6021d4be4182'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
 

def downgrade() -> None:
    """Downgrade schema."""
    pass
