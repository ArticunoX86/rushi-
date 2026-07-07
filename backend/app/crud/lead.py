from uuid import UUID

from sqlalchemy.orm import Session

from app.models.lead import Lead

from app.schemas.lead import (
    LeadCreate,
    LeadUpdate,
    LeadSearch,
)


# ==================================================
# Create Lead
# ==================================================

def create_lead(
    db: Session,
    lead_data: LeadCreate,
):

    lead = Lead(
        **lead_data.model_dump()
    )


    db.add(lead)

    db.commit()

    db.refresh(lead)


    return lead



# ==================================================
# Get Lead By ID
# ==================================================

def get_lead(
    db: Session,
    lead_id: UUID,
):

    return (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )



# ==================================================
# Get All Leads
# ==================================================

def get_leads(
    db: Session,
    skip: int = 0,
    limit: int = 50,
):

    return (
        db.query(Lead)
        .offset(skip)
        .limit(limit)
        .all()
    )



# ==================================================
# Update Lead
# ==================================================

def update_lead(
    db: Session,
    lead_obj: Lead,
    update_data: LeadUpdate,
):

    update_dict = update_data.model_dump(
        exclude_unset=True
    )


    for field, value in update_dict.items():

        setattr(
            lead_obj,
            field,
            value,
        )


    db.commit()

    db.refresh(lead_obj)


    return lead_obj



# ==================================================
# Delete Lead
# ==================================================

def delete_lead(
    db: Session,
    lead_obj: Lead,
):

    db.delete(
        lead_obj
    )


    db.commit()


    return True



# ==================================================
# AI Lead Search
# ==================================================

def search_leads(
    db: Session,
    filters: LeadSearch,
):

    query = db.query(
        Lead
    )


    if filters.status:

        query = query.filter(
            Lead.status
            ==
            filters.status
        )


    if filters.priority:

        query = query.filter(
            Lead.priority
            ==
            filters.priority
        )


    if filters.preferred_city:

        query = query.filter(
            Lead.preferred_city.ilike(
                f"%{filters.preferred_city}%"
            )
        )


    if filters.property_type:

        query = query.filter(
            Lead.property_type
            ==
            filters.property_type
        )


    if filters.min_budget:

        query = query.filter(
            Lead.budget_max
            >=
            filters.min_budget
        )


    if filters.max_budget:

        query = query.filter(
            Lead.budget_max
            <=
            filters.max_budget
        )


    if filters.bedrooms:

        query = query.filter(
            Lead.bedrooms
            ==
            filters.bedrooms
        )


    return query.all()