import uuid
from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID, JSON
from app.database.base import Base
from app.database.base_model import TimestampMixin
import enum


class TrainingCategory(str, enum.Enum):
    OBJECTION_HANDLING = "OBJECTION_HANDLING"
    PRODUCT_KNOWLEDGE = "PRODUCT_KNOWLEDGE"
    SALES_PLAYBOOK = "SALES_PLAYBOOK"
    FAQ = "FAQ"
    PERSONA_RULE = "PERSONA_RULE"


class AITrainingData(Base, TimestampMixin):
    """
    AI Knowledge Base / Training Data Model.

    Stores curated entries (objection scripts, FAQs, playbooks, persona rules)
    that are dynamically injected into the Gemini prompt during every call.
    This effectively 'trains' the AI engine with domain-specific knowledge.
    """

    __tablename__ = "ai_training_data"

    # Tenant scoping
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)

    # ==================================================
    # Classification
    # ==================================================

    category = Column(
        SAEnum(TrainingCategory),
        nullable=False,
        default=TrainingCategory.OBJECTION_HANDLING,
        index=True,
    )

    # ==================================================
    # Training Content
    # ==================================================

    title = Column(
        String(255),
        nullable=False,
    )

    trigger_phrase = Column(
        Text,
        nullable=True,
        comment="Keywords/phrase that signals this entry is relevant (e.g. 'not interested', 'too expensive')",
    )

    situation_context = Column(
        Text,
        nullable=True,
        comment="Human-readable description of when this entry applies",
    )

    ideal_response = Column(
        Text,
        nullable=False,
        comment="What the AI should say or do in this situation",
    )

    # ==================================================
    # Routing Tags (used for category-filtered injection)
    # ==================================================

    tags = Column(
        JSON,
        nullable=True,
        default=list,
        comment="List of intent tags for smart injection (e.g. ['not_interested', 'price_objection'])",
    )

    # ==================================================
    # Priority & Status
    # ==================================================

    priority = Column(
        Integer,
        default=5,
        nullable=False,
        comment="1=lowest, 10=highest. Higher priority entries are injected first.",
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ==================================================
    # Analytics
    # ==================================================

    usage_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Incremented each time this entry is injected in a live call",
    )

    def __repr__(self):
        return f"<AITrainingData [{self.category}] {self.title}>"
