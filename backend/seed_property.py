import sys
import os
from decimal import Decimal

# Ensure the backend directory is in the python path
sys.path.append(os.getcwd())

from app.database.session import SessionLocal
from app.models.property import Property
from app.models.enums import PropertyType, ListingType, PropertyStatus, FurnishingType

def seed_mumbai_property():
    db = SessionLocal()
    
    # Check if we already have it to avoid duplicates
    existing = db.query(Property).filter(Property.title == "Luxury 3BHK in Bandra West").first()
    if existing:
        print("✅ Property already exists in the database!")
        return

    new_prop = Property(
        title="Luxury 3BHK in Bandra West",
        description="A stunning sea-facing 3BHK apartment in the heart of Bandra West with modern amenities and a beautiful balcony.",
        property_type=PropertyType.APARTMENT,
        listing_type=ListingType.SALE,
        status=PropertyStatus.AVAILABLE,
        city="Mumbai",
        locality="Bandra West",
        address="123 Carter Road, Bandra West, Mumbai",
        pincode="400050",
        price=Decimal("45000000.00"),  # 4.5 Cr
        maintenance_cost=Decimal("15000.00"),
        bedrooms=3,
        bathrooms=3,
        area_sqft=1850,
        furnishing=FurnishingType.FURNISHED,
        parking=True,
        lift=True,
        security=True,
        owner_name="Rahul Sharma",
        owner_phone="+919876543210"
    )

    db.add(new_prop)
    db.commit()
    print("✅ Successfully added fake Mumbai property to the database!")

if __name__ == "__main__":
    seed_mumbai_property()
