from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.property import Property
from app.models.lead import Lead


# ==================================================
# Match Properties For Lead
# ==================================================

def get_property_recommendations(
    db: Session,
    lead_id: UUID,
):


    # Get Lead

    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id
        )
        .first()
    )


    if not lead:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )



    # Base Property Query

    query = db.query(
        Property
    )



    # City Matching
    if lead.preferred_city and lead.preferred_city.lower() != "string":
        query = query.filter(
            Property.city.ilike(
                f"%{lead.preferred_city}%"
            )
        )



    # Locality Matching
    if lead.preferred_locality and lead.preferred_locality.lower() != "string":
        query = query.filter(
            Property.locality.ilike(
                f"%{lead.preferred_locality}%"
            )
        )



    # Bedroom Matching

    if lead.bedrooms:

        query = query.filter(
            Property.bedrooms
            ==
            lead.bedrooms
        )



    # Property Type Matching

    if lead.property_type:

        query = query.filter(
            Property.property_type
            ==
            lead.property_type
        )



    # Budget Matching
    if lead.budget_max and lead.budget_max > 0:
        query = query.filter(
            Property.price <= lead.budget_max
        )



    properties = query.all()



    return {
        "lead": {
            "name": f"{lead.first_name} {lead.last_name}",
            "requirement": {
                "city": lead.preferred_city,
                "bedrooms": lead.bedrooms,
                "budget": lead.budget_max,
            },
        },

        "matches_found": len(properties),

        "recommended_properties": properties,
    }