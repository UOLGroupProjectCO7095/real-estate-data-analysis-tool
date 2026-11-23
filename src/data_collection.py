"""
Data Collection Module (Member 1 - Data Collection).

Provides open collection interfaces.
- In production: Gathers live real estate properties from web sources or Data/properties.csv.
- In testing/simulation: Supplies simulated collected property batches to test integration.
"""

import os
import csv
import random
from typing import List, Dict, Any


def generate_mock_collected_properties(count: int = 5) -> List[Dict[str, Any]]:
    """
    Generates simulated batches of collected properties (representing Member 1's scraped data).
    Contains a realistic mix of valid properties and occasional edge cases.
    """
    types = ["apartment", "house", "condo", "studio", "townhouse", "ensuite"]
    cities = ["London", "Manchester", "Birmingham", "Leicester", "Edinburgh", "Leeds", "Bristol"]

    mock_records: List[Dict[str, Any]] = []
    for i in range(1, count + 1):
        rand_id = f"MOCK_COLLECT_{random.randint(10000, 99999)}"
        ptype = random.choice(types)
        city = random.choice(cities)
        price = random.randint(80, 850) * 1000 if ptype != "ensuite" else random.randint(90, 250)
        beds = random.randint(1, 5) if ptype != "studio" else 0
        baths = max(1, beds - 1) if beds > 0 else 1

        city_urls = {
            "London": "https://www.rightmove.co.uk/property-to-rent/London.html",
            "Manchester": "https://www.rightmove.co.uk/property-to-rent/Manchester.html",
            "Birmingham": "https://www.rightmove.co.uk/property-to-rent/Birmingham.html",
            "Leicester": "https://amberstudent.com/places/search/leicester-1811058253133",
            "Edinburgh": "https://www.rightmove.co.uk/property-to-rent/Edinburgh.html",
            "Leeds": "https://amberstudent.com/places/search/leeds-1811055811329",
            "Bristol": "https://www.rightmove.co.uk/property-to-rent/Bristol.html"
        }
        url = city_urls.get(city, f"https://www.rightmove.co.uk/property-to-rent/{city}.html")

        mock_records.append({
            "property_id": rand_id,
            "property_type": ptype,
            "location": f"{city} Central",
            "price": str(price),
            "bedrooms": str(beds),
            "bathrooms": str(baths),
            "listing_url": url
        })

    return mock_records


def fetch_raw_collected_data() -> List[Dict[str, Any]]:
    """
    Production hook for Member 1 to return raw scraped or fetched data.
    Loads from Data/properties.csv if populated, or live collection pipeline.
    """
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "properties.csv")
    if not os.path.exists(data_path):
        return []

    collected: List[Dict[str, Any]] = []
    with open(data_path, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            collected.append(dict(row))
    return collected
