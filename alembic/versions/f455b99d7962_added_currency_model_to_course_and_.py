"""added currency model to course and Payment Status for Enrollment

Revision ID: f455b99d7962
Revises: 3f37d51f9db4
Create Date: 2026-09-06 12:36:01.995214

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f455b99d7962"
down_revision: Union[str, Sequence[str], None] = "3f37d51f9db4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Create PostgreSQL enum type first
    enrollment_status_enum = sa.Enum(
        "PENDING",
        "ACTIVE",
        "CANCELLED",
        name="enrollmentstatus",
    )

    enrollment_status_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    # Create currencies table
    op.create_table(
        "currencies",
        sa.Column("code", sa.String(length=3), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("symbol", sa.String(length=10), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
        ),
        sa.Column(
            "decimal_places",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )

    # Course payment fields
    op.add_column(
        "courses",
        sa.Column(
            "requires_payment",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "courses",
        sa.Column(
            "price",
            sa.Numeric(precision=10, scale=2),
            nullable=True,
        ),
    )

    op.add_column(
        "courses",
        sa.Column(
            "currency_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_courses_currency_id",
        "courses",
        "currencies",
        ["currency_id"],
        ["id"],
    )

    # Enrollment payment status
    # Existing enrollments are marked ACTIVE.
    op.add_column(
        "enrollments",
        sa.Column(
            "payment_status",
            enrollment_status_enum,
            server_default="ACTIVE",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "enrollments",
        "payment_status",
    )

    op.drop_constraint(
        "fk_courses_currency_id",
        "courses",
        type_="foreignkey",
    )

    op.drop_column(
        "courses",
        "currency_id",
    )

    op.drop_column(
        "courses",
        "price",
    )

    op.drop_column(
        "courses",
        "requires_payment",
    )

    op.drop_table(
        "currencies",
    )

    enrollment_status_enum = sa.Enum(
        "PENDING",
        "ACTIVE",
        "CANCELLED",
        name="enrollmentstatus",
    )

    enrollment_status_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )
