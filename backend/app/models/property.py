from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.database.base_model import TimestampMixin
from app.models.enums import (
    FurnishingType,
    ListingType,
    PropertyStatus,
    PropertyType,
)


class Property(Base, TimestampMixin):
    """
    Real Estate Property Model.
    """

    __tablename__ = "properties"
    tenant_id = mapped_column(ForeignKey('tenants.id'), nullable=True)


    # ==================================================
    # Basic Information
    # ==================================================

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    property_type: Mapped[PropertyType] = mapped_column(
        Enum(PropertyType),
        nullable=False,
    )


    listing_type: Mapped[ListingType] = mapped_column(
        Enum(ListingType),
        nullable=False,
    )


    status: Mapped[PropertyStatus] = mapped_column(
        Enum(PropertyStatus),
        default=PropertyStatus.AVAILABLE,
        nullable=False,
    )


    # ==================================================
    # Location
    # ==================================================

    city: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )


    locality: Mapped[str] = mapped_column(
        String(150),
        index=True,
        nullable=False,
    )


    address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )


    pincode: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )


    # ==================================================
    # Pricing
    # ==================================================

    price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )


    maintenance_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2),
        nullable=True,
    )


    # ==================================================
    # Property Details
    # ==================================================

    bedrooms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    bathrooms: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    area_sqft: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    furnishing: Mapped[FurnishingType] = mapped_column(
        Enum(FurnishingType),
        nullable=False,
    )


    # ==================================================
    # Amenities
    # ==================================================

    parking: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    lift: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    security: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )


    # ==================================================
    # Ownership
    # ==================================================

    owner_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )


    owner_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )


    # ==================================================
    # Assignment
    # ==================================================

    assigned_to: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )


    assigned_user = relationship(
        "User",
        backref="properties",
    )


    def __repr__(self):
        return f"<Property {self.title}>"