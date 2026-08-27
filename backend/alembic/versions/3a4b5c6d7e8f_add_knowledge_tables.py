"""add knowledge tables and vector extension

Revision ID: 3a4b5c6d7e8f
Revises: 023ae7e47788
Create Date: 2026-08-17 17:19:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision = '3a4b5c6d7e8f'
down_revision = '023ae7e47788'
branch_labels = None
depends_on = None


def upgrade():
    # Create vector extension if it doesn't exist
    op.execute('CREATE EXTENSION IF NOT EXISTS vector;')

    # Create knowledge_documents table
    op.create_table('knowledge_documents',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('document_type', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_knowledge_documents_id'), 'knowledge_documents', ['id'], unique=False)

    # Create document_chunks table
    op.create_table('document_chunks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('document_id', sa.String(), nullable=False),
    sa.Column('chunk_text', sa.Text(), nullable=False),
    sa.Column('embedding', Vector(768), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['knowledge_documents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_document_chunks_id'), 'document_chunks', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_document_chunks_id'), table_name='document_chunks')
    op.drop_table('document_chunks')
    op.drop_index(op.f('ix_knowledge_documents_id'), table_name='knowledge_documents')
    op.drop_table('knowledge_documents')
    op.execute('DROP EXTENSION IF EXISTS vector;')
