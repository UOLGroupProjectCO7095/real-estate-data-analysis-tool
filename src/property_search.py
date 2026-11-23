"""
Property Entities & Domain Model (Member 4 - Properties).

Defines the PropertyRecord domain entity and simulated Property creation.
- In production: Real property domain objects created by Member 4.
- In testing/simulation: Generates simulated Property entities to test open merging.
"""

import random
from typing import Dict, Any, List, Optional


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


def generate_mock_member4_properties(count: int = 5) -> List[Property]:
    """
    Generates simulated Property objects created by Member 4.
    """
    types = ["apartment", "villa", "duplex", "house", "ensuite"]
    cities = ["London", "Manchester", "Leicester", "Cardiff", "Oxford"]

    mock_properties: List[Property] = []
    for i in range(1, count + 1):
        rand_id = f"MOCK_PROP_M4_{random.randint(10000, 99999)}"
        ptype = random.choice(types)
        city = random.choice(cities)
        price = random.randint(120, 950) * 1000 if ptype != "ensuite" else random.randint(100, 220)
        beds = random.randint(1, 4)
        baths = max(1, beds - 1)

        city_urls = {
            "London": "https://www.zoopla.co.uk/to-rent/property/london/",
            "Manchester": "https://www.zoopla.co.uk/to-rent/property/manchester/",
            "Leicester": "https://amberstudent.com/places/search/leicester-1811058253133",
            "Cardiff": "https://www.rightmove.co.uk/property-to-rent/Cardiff.html",
            "Oxford": "https://www.rightmove.co.uk/property-to-rent/Oxford.html"
        }
        url = city_urls.get(city, f"https://www.rightmove.co.uk/property-to-rent/{city}.html")

        mock_properties.append(Property(
            property_id=rand_id,
            property_type=ptype,
            location=f"{city} High Street",
            price=price,
            bedrooms=beds,
            bathrooms=baths,
            listing_url=url
        ))

    return mock_properties
