import uuid
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.ai_training_data import AITrainingData, TrainingCategory
from app.schemas.ai_training_data import AITrainingDataCreate, AITrainingDataUpdate


class CRUDAITrainingData:
    """
    CRUD operations for AI Training Data / Knowledge Base.
    """

    # ==================================================
    # READ
    # ==================================================

    def get(self, db: Session, entry_id: uuid.UUID) -> Optional[AITrainingData]:
        return db.query(AITrainingData).filter(AITrainingData.id == entry_id).first()

    def get_all(
        self,
        db: Session,
        category: Optional[TrainingCategory] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[AITrainingData]:
        query = db.query(AITrainingData)
        if category:
            query = query.filter(AITrainingData.category == category)
        if is_active is not None:
            query = query.filter(AITrainingData.is_active == is_active)
        return (
            query.order_by(AITrainingData.priority.desc(), AITrainingData.usage_count.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_active(self, db: Session) -> List[AITrainingData]:
        """Get all active entries ordered by priority (used for prompt injection)."""
        return (
            db.query(AITrainingData)
            .filter(AITrainingData.is_active == True)
            .order_by(AITrainingData.priority.desc())
            .all()
        )

    def get_relevant(self, db: Session, keywords: List[str]) -> List[AITrainingData]:
        """
        Category-filtered injection: return active entries whose trigger_phrase
        or tags overlap with the detected keywords in the customer's message.
        Falls back to top-priority entries if no specific match is found.
        """
        if not keywords:
            # No keywords detected — return top-priority entries (persona rules + playbooks)
            return (
                db.query(AITrainingData)
                .filter(
                    AITrainingData.is_active == True,
                    AITrainingData.category.in_([
                        TrainingCategory.PERSONA_RULE,
                        TrainingCategory.SALES_PLAYBOOK,
                    ])
                )
                .order_by(AITrainingData.priority.desc())
                .limit(5)
                .all()
            )

        all_active = self.get_active(db)
        matched = []
        general = []

        lower_keywords = [k.lower() for k in keywords]

        for entry in all_active:
            # Always include persona rules and high-priority playbooks
            if entry.category in (TrainingCategory.PERSONA_RULE, TrainingCategory.SALES_PLAYBOOK):
                general.append(entry)
                continue

            # Check trigger phrase
            trigger_match = (
                entry.trigger_phrase
                and any(kw in entry.trigger_phrase.lower() for kw in lower_keywords)
            )

            # Check tags
            tag_match = False
            if entry.tags:
                entry_tags = [t.lower() for t in entry.tags]
                tag_match = any(kw in entry_tags for kw in lower_keywords) or \
                            any(tag in lower_keywords for tag in entry_tags)

            if trigger_match or tag_match:
                matched.append(entry)

        # Return matched + general entries, deduplicated, capped at 8 total
        combined = matched + [g for g in general if g not in matched]
        return combined[:8]

    def get_stats(self, db: Session) -> dict:
        """Return usage stats for the training dashboard."""
        all_entries = db.query(AITrainingData).all()
        active_entries = [e for e in all_entries if e.is_active]
        total_usage = sum(e.usage_count for e in all_entries)
        top_entries = sorted(active_entries, key=lambda e: e.usage_count, reverse=True)[:5]

        by_category = {}
        for entry in all_entries:
            cat = entry.category.value
            if cat not in by_category:
                by_category[cat] = {"category": entry.category, "total": 0, "active": 0, "total_usage": 0}
            by_category[cat]["total"] += 1
            by_category[cat]["total_usage"] += entry.usage_count
            if entry.is_active:
                by_category[cat]["active"] += 1

        return {
            "total_entries": len(all_entries),
            "active_entries": len(active_entries),
            "total_usage_across_all": total_usage,
            "top_entries": top_entries,
            "by_category": list(by_category.values()),
        }

    # ==================================================
    # WRITE
    # ==================================================

    def create(self, db: Session, obj_in: AITrainingDataCreate) -> AITrainingData:
        db_obj = AITrainingData(
            title=obj_in.title,
            category=obj_in.category,
            trigger_phrase=obj_in.trigger_phrase,
            situation_context=obj_in.situation_context,
            ideal_response=obj_in.ideal_response,
            tags=obj_in.tags or [],
            priority=obj_in.priority,
            is_active=obj_in.is_active,
            usage_count=0,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def bulk_create(self, db: Session, entries: List[AITrainingDataCreate]) -> List[AITrainingData]:
        created = []
        for obj_in in entries:
            created.append(self.create(db, obj_in))
        return created

    def update(self, db: Session, db_obj: AITrainingData, obj_in: AITrainingDataUpdate) -> AITrainingData:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def soft_delete(self, db: Session, entry_id: uuid.UUID) -> Optional[AITrainingData]:
        """Soft delete: set is_active=False instead of removing the record."""
        obj = self.get(db, entry_id)
        if obj:
            obj.is_active = False
            db.commit()
            db.refresh(obj)
        return obj

    def hard_delete(self, db: Session, entry_id: uuid.UUID) -> bool:
        obj = self.get(db, entry_id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False

    def increment_usage(self, db: Session, entry_ids: List[uuid.UUID]) -> None:
        """Increment usage_count for all entries that were injected in a call."""
        if not entry_ids:
            return
        db.query(AITrainingData).filter(
            AITrainingData.id.in_(entry_ids)
        ).update(
            {AITrainingData.usage_count: AITrainingData.usage_count + 1},
            synchronize_session="fetch"
        )
        db.commit()


# Singleton instance
ai_training_data = CRUDAITrainingData()
