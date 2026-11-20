"""
Property Entities & Domain Model (Member 4 - Properties).

Defines the PropertyRecord domain entity. Provides open conversion methods
between raw dictionaries and strongly-typed objects once Member 4 develops this module.
"""

from typing import Dict, Any, Optional


class Property:
    """
    Domain entity representing a validated property record.
    """

    def __init__(
        self,
        property_id: str,
        property_type: str,
        location: str,
        price: float,
        bedrooms: float,
        bathrooms: float,
        listing_url: str
    ):
        self.property_id = property_id
        self.property_type = property_type
        self.location = location
        self.price = float(price)
        self.bedrooms = float(bedrooms)
        self.bathrooms = float(bathrooms)
        self.listing_url = listing_url

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Property":
        """Factory method to construct Property object from dictionary."""
        return cls(
            property_id=str(data.get("property_id", "")),
            property_type=str(data.get("property_type", "")).lower().strip(),
            location=str(data.get("location", "")).strip(),
            price=float(str(data.get("price", "0")).replace(",", "").replace("$", "").replace("£", "").strip()),
            bedrooms=float(data.get("bedrooms", 0)),
            bathrooms=float(data.get("bathrooms", 0)),
            listing_url=str(data.get("listing_url", "")).strip()
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts entity back to dictionary."""
        return {
            "property_id": self.property_id,
            "property_type": self.property_type,
            "location": self.location,
            "price": self.price,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "listing_url": self.listing_url
        }

    def __repr__(self) -> str:
        return f"Property(id='{self.property_id}', type='{self.property_type}', price={self.price}, location='{self.location}')"
