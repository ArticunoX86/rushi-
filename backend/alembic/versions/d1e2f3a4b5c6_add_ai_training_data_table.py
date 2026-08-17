"""add_ai_training_data_table

Revision ID: d1e2f3a4b5c6
Revises: bc823c61e078
Create Date: 2026-08-17 16:45:00.000000

Creates the ai_training_data table which stores the AI knowledge base
(objection handling scripts, FAQs, sales playbooks, persona rules, and
product knowledge) that get dynamically injected into the Gemini prompt
during every live call.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'd1e2f3a4b5c6'
down_revision: Union[str, Sequence[str], None] = 'bc823c61e078'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the ai_training_data table."""
    op.create_table(
        'ai_training_data',

        # Primary key and timestamps
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),

        # Tenant scoping
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=True),

        # Classification
        sa.Column(
            'category',
            sa.Enum(
                'OBJECTION_HANDLING',
                'PRODUCT_KNOWLEDGE',
                'SALES_PLAYBOOK',
                'FAQ',
                'PERSONA_RULE',
                name='trainingcategory'
            ),
            nullable=False,
        ),

        # Training content
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('trigger_phrase', sa.Text(), nullable=True),
        sa.Column('situation_context', sa.Text(), nullable=True),
        sa.Column('ideal_response', sa.Text(), nullable=False),

        # Routing / injection tags
        sa.Column('tags', postgresql.JSON(astext_type=sa.Text()), nullable=True),

        # Priority and status
        sa.Column('priority', sa.Integer(), nullable=False, server_default='5'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),

        # Usage analytics
        sa.Column('usage_count', sa.Integer(), nullable=False, server_default='0'),

        # Constraints
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # Indexes for fast lookups
    op.create_index(
        'ix_ai_training_data_category',
        'ai_training_data',
        ['category'],
    )
    op.create_index(
        'ix_ai_training_data_is_active',
        'ai_training_data',
        ['is_active'],
    )
    op.create_index(
        'ix_ai_training_data_priority',
        'ai_training_data',
        ['priority'],
    )


def downgrade() -> None:
    """Drop the ai_training_data table."""
    op.drop_index('ix_ai_training_data_priority', table_name='ai_training_data')
    op.drop_index('ix_ai_training_data_is_active', table_name='ai_training_data')
    op.drop_index('ix_ai_training_data_category', table_name='ai_training_data')
    op.drop_table('ai_training_data')

    # Drop the enum type
    sa.Enum(name='trainingcategory').drop(op.get_bind(), checkfirst=True)
