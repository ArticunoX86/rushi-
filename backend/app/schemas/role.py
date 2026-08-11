from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import List, Optional

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: List[str] = []

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    name: Optional[str] = None

class RoleResponse(RoleBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
