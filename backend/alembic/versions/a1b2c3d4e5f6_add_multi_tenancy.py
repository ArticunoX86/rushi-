"""Add multi-tenancy

Revision ID: a1b2c3d4e5f6
Revises: 76bc056b7a97
Create Date: 2026-08-11 12:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '76bc056b7a97'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create tenants table
    op.create_table('tenants',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Insert default tenant
    # Using raw SQL for data migration
    op.execute("INSERT INTO tenants (id, name, is_active) VALUES ('00000000-0000-0000-0000-000000000000', 'Default Master Tenant', true)")

    # Add is_superadmin to users
    op.add_column('users', sa.Column('is_superadmin', sa.Boolean(), server_default='false', nullable=False))

    # Add tenant_id to all tables
    tables = ['users', 'roles', 'leads', 'properties', 'calls', 'app_logs', 'conversations', 'devices']
    
    bind = op.get_bind()
    from sqlalchemy import inspect
    inspector = inspect(bind)
    existing_tables = inspector.get_table_names()

    for table in tables:
        if table in existing_tables:
            op.add_column(table, sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=True))
            # Set existing records to default tenant
            op.execute(f"UPDATE {table} SET tenant_id = '00000000-0000-0000-0000-000000000000'")
            # Create Foreign Key
            op.create_foreign_key(f"fk_{table}_tenant_id", table, 'tenants', ['tenant_id'], ['id'])
        else:
            print(f"Skipping {table} because it does not exist.")

def downgrade() -> None:
    tables = ['users', 'roles', 'leads', 'properties', 'calls', 'app_logs', 'agent_scripts', 'script_faqs', 'conversations', 'devices']
    for table in tables:
        try:
            op.drop_constraint(f"fk_{table}_tenant_id", table_name=table, type_='foreignkey')
            op.drop_column(table, 'tenant_id')
        except Exception:
            pass
    op.drop_column('users', 'is_superadmin')
    op.drop_table('tenants')
