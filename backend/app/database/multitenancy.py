import contextvars
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import event
from sqlalchemy.orm import with_loader_criteria

# Context variable to hold the current tenant ID
current_tenant_id: contextvars.ContextVar[Optional[UUID]] = contextvars.ContextVar("current_tenant_id", default=None)

def set_current_tenant_id(tenant_id: Optional[UUID]):
    """Set the current tenant ID for the request context."""
    current_tenant_id.set(tenant_id)

def get_current_tenant_id() -> Optional[UUID]:
    """Get the current tenant ID from the request context."""
    return current_tenant_id.get()

# Global SQLAlchemy event to inject tenant_id filter into all ORM queries
@event.listens_for(Session, "do_orm_execute")
def _add_tenant_filter(execute_state):
    # Don't filter if there's no tenant in context (e.g., background tasks, super admin, or login)
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        return
        
    # Exclude system tables that are global (like Tenant, User if superadmin, etc.)
    # In a strict SaaS, User should be tenant-scoped too, but we need to check if the class has a tenant_id
    
    # We apply a dynamic filter to all models that have a 'tenant_id' column
    execute_state.statement = execute_state.statement.options(
        with_loader_criteria(
            # Apply to any mapped class
            lambda cls: hasattr(cls, 'tenant_id'),
            # The filter criterion
            lambda cls: cls.tenant_id == tenant_id,
            include_aliases=True
        )
    )

from sqlalchemy.orm import mapper

@event.listens_for(Session, "before_flush")
def _receive_before_flush(session, flush_context, instances):
    tenant_id = get_current_tenant_id()
    if not tenant_id:
        return
        
    for obj in session.new:
        if hasattr(obj, 'tenant_id'):
            # Only set it if it's not already explicitly set
            if getattr(obj, 'tenant_id') is None:
                setattr(obj, 'tenant_id', tenant_id)
