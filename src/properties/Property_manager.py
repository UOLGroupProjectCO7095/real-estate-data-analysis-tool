import csv
from pathlib import Path
import os
## reads the csv files
CURRENT_FILE = Path(__file__).resolve()
BASE_DIR = next(
    parent for parent in CURRENT_FILE.parents if (parent /"data" /"properties.csv").exists()
)
CSV_FILE = BASE_DIR / "data" / "properties.csv"

def load_properties():
    with open(CSV_FILE, "r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file, delimiter="\t")
        properties = []

        for row in reader:
            cleaned_row = {
                key.strip().lstrip("\ufeff"): value.strip() if value else ""
                for key, value in row.items()
                if key is not None
            }
            properties.append(cleaned_row)

        return properties

def get_property(property_id):
    properties = load_properties()
    for existing_property in properties:
       if existing_property["property_id"] == property_id:
           return existing_property
    return None

def register_property(property_data):
    properties = load_properties()
    required_fields=["property_id", "property_type", "location", "price", "bedrooms", "bathrooms", "listing_url"]
    for field in required_fields:
        if field not in property_data or str(property_data[field]).strip() == "":
            return False
    property_id = str(property_data["property_id"]).strip()

    for existing_property in properties:
        existing_id = str(existing_property.get("property_id", "")).strip()
        if existing_id == property_id:
            return False
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["property_id", "property_type", "location", "price", "bedrooms", "bathrooms", "listing_url"],
            delimiter="\t"
        )
        writer.writerow(property_data)
    return True

def register_property_with_message(property_data):
    result = register_property(property_data)
    if result:
        return "property registered!"
    else:
        return "property not registered!"

def update_property(property_id, updated_data):
    properties = load_properties()
    for property in properties:
        if property["property_id"] == property_id:
            property.update(updated_data)
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.DictWriter(
                    csv_file,
                    fieldnames=properties[0].keys(),
                    delimiter="\t"
                )
                writer.writeheader()
                writer.writerows(properties)
            return True
    return False

