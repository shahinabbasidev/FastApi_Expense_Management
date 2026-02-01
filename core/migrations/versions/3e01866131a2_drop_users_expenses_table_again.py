"""drop users_expenses table again

Revision ID: 3e01866131a2
Revises: 84353c8ea656
Create Date: 2026-02-01 17:10:00.873813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e01866131a2'
down_revision: Union[str, Sequence[str], None] = '84353c8ea656'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table("users_expenses")


def downgrade() -> None:
    """Downgrade schema."""
    pass
