"""create leads table

Revision ID: f9cf3baf0ef0
Revises: e43ed8028a72
Create Date: 2026-07-07 10:06:22.852028

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.

revision: str = "f9cf3baf0ef0"

down_revision: Union[str, Sequence[str], None] = "e43ed8028a72"

branch_labels: Union[str, Sequence[str], None] = None

depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    """Upgrade schema."""


    op.create_table(
        "leads",


        # ================================
        # Customer Information
        # ================================

        sa.Column(
            "first_name",
            sa.String(100),
            nullable=False,
        ),

        sa.Column(
            "last_name",
            sa.String(100),
            nullable=True,
        ),

        sa.Column(
            "email",
            sa.String(255),
            nullable=True,
        ),

        sa.Column(
            "phone",
            sa.String(20),
            nullable=False,
        ),


        # ================================
        # Requirements
        # ================================

        sa.Column(
            "preferred_city",
            sa.String(100),
            nullable=True,
        ),

        sa.Column(
            "preferred_locality",
            sa.String(150),
            nullable=True,
        ),

        sa.Column(
            "budget_min",
            sa.Numeric(
                precision=12,
                scale=2,
            ),
            nullable=True,
        ),

        sa.Column(
            "budget_max",
            sa.Numeric(
                precision=12,
                scale=2,
            ),
            nullable=True,
        ),

        sa.Column(
            "bedrooms",
            sa.Integer(),
            nullable=True,
        ),


        # REUSE EXISTING PROPERTY ENUM

        sa.Column(
            "property_type",
            postgresql.ENUM(
                "APARTMENT",
                "VILLA",
                "HOUSE",
                "PLOT",
                "COMMERCIAL",
                name="propertytype",
                create_type=False,
            ),
            nullable=True,
        ),



        # ================================
        # Lead Management
        # ================================

        sa.Column(
            "status",
            postgresql.ENUM(
                "NEW",
                "CONTACTED",
                "INTERESTED",
                "NOT_INTERESTED",
                "FOLLOW_UP",
                "CONVERTED",
                name="leadstatus",
            ),
            nullable=False,
        ),

        sa.Column(
            "priority",
            postgresql.ENUM(
                "LOW",
                "MEDIUM",
                "HIGH",
                name="leadpriority",
            ),
            nullable=False,
        ),

        sa.Column(
            "source",
            postgresql.ENUM(
                "WEBSITE",
                "MANUAL",
                "CSV_IMPORT",
                "API",
                name="leadsource",
            ),
            nullable=False,
        ),



        # ================================
        # AI Calling Fields
        # ================================

        sa.Column(
            "call_attempts",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "last_call_time",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "next_followup_time",
            sa.DateTime(timezone=True),
            nullable=True,
        ),

        sa.Column(
            "conversation_summary",
            sa.Text(),
            nullable=True,
        ),



        # ================================
        # Relations + Base
        # ================================

        sa.Column(
            "assigned_to",
            sa.UUID(),
            nullable=True,
        ),

        sa.Column(
            "id",
            sa.UUID(),
            nullable=False,
        ),

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


        sa.ForeignKeyConstraint(
            ["assigned_to"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )


    op.create_index(
        "ix_leads_phone",
        "leads",
        ["phone"],
    )


    op.create_index(
        "ix_leads_preferred_city",
        "leads",
        ["preferred_city"],
    )




def downgrade() -> None:
    """Downgrade schema."""


    op.drop_index(
        "ix_leads_preferred_city",
        table_name="leads",
    )


    op.drop_index(
        "ix_leads_phone",
        table_name="leads",
    )


    op.drop_table(
        "leads",
    )