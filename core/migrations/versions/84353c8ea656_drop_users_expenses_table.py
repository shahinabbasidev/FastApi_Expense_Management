"""drop users_expenses table

Revision ID: 84353c8ea656
Revises: 3616f6058988
Create Date: 2026-02-01 17:08:54.240598

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "84353c8ea656"
down_revision: Union[str, Sequence[str], None] = "3616f6058988"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
