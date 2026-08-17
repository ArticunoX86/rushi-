import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.ai_training_data import TrainingCategory


# ==================================================
# BASE SCHEMA
# ==================================================

class AITrainingDataBase(BaseModel):
    title: str = Field(..., description="Short descriptive title of this training entry")
    category: TrainingCategory = TrainingCategory.OBJECTION_HANDLING
    trigger_phrase: Optional[str] = Field(None, description="Keyword or phrase that signals this entry is relevant")
    situation_context: Optional[str] = Field(None, description="When this entry should be applied")
    ideal_response: str = Field(..., description="The AI's ideal response or action in this situation")
    tags: Optional[List[str]] = Field(default_factory=list, description="Intent tags for smart injection")
    priority: int = Field(5, ge=1, le=10, description="Priority 1-10. Higher = injected first")
    is_active: bool = True


# ==================================================
# CREATE / UPDATE
# ==================================================

class AITrainingDataCreate(AITrainingDataBase):
    pass


class AITrainingDataUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[TrainingCategory] = None
    trigger_phrase: Optional[str] = None
    situation_context: Optional[str] = None
    ideal_response: Optional[str] = None
    tags: Optional[List[str]] = None
    priority: Optional[int] = Field(None, ge=1, le=10)
    is_active: Optional[bool] = None


# ==================================================
# RESPONSE
# ==================================================

class AITrainingDataResponse(AITrainingDataBase):
    id: uuid.UUID
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================================================
# BULK IMPORT
# ==================================================

class AITrainingDataBulkImport(BaseModel):
    entries: List[AITrainingDataCreate]


# ==================================================
# STATS
# ==================================================

class TrainingCategoryStats(BaseModel):
    category: TrainingCategory
    total: int
    active: int
    total_usage: int


class AITrainingStatsResponse(BaseModel):
    total_entries: int
    active_entries: int
    total_usage_across_all: int
    top_entries: List[AITrainingDataResponse]
    by_category: List[TrainingCategoryStats]
