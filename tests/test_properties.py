import csv
from pathlib import Path
from unittest.mock import patch
from src.properties import Property_manager as pm


def create_test_file(tmp_path, monkeypatch):
    test_file = tmp_path /"properties.csv"
    fields =[
        "property_id",
        "property_type",
        "location",
        "price",
        "bedrooms",
        "bathrooms",
        "listing_url"
    ]
    with open(test_file, "w", newline="", encoding ="utf-8") as f:
         writer = csv.DictWriter (f, fieldnames=fields, delimiter="\t")
         writer.writeheader()
    monkeypatch.setattr(pm,"CSV_FILE", test_file)

def test_register_property(tmp_path, monkeypatch):
    create_test_file(tmp_path, monkeypatch)
    property_data = {
        "property_id": "TEST001",
        "property_type": "Apartment",
        "location": "leicester",
        "price": "180000",
        "bedrooms": "2",
        "bathrooms": "1",
        "listing_url": "https://properties.example.com/1002"
    }
    result = pm.register_property(property_data)
    assert result is True

def test_duplicate_property(tmp_path, monkeypatch):
        create_test_file(tmp_path, monkeypatch)
        property_data = {
            "property_id": "TEST002",
            "property_type": "Apartment",
            "location": "Leicester",
            "price": "180000",
            "bedrooms": "2",
            "bathrooms": "1",
            "listing_url": "https://properties.example.com/1002"
        }

        first_result = pm.register_property(property_data)
        second_result = pm.register_property(property_data)

        assert first_result is True
        assert second_result is False

def test_update_property(tmp_path, monkeypatch):
        create_test_file(tmp_path, monkeypatch)
        property_data={
            "property_id": "TEST003",
            "property_type": "Apartment",
            "location": "Leicester",
            "price": "180000",
            "bedrooms": "2",
            "bathrooms": "1",
            "listing_url": "https://properties.example.com/1003"
        }
        pm.register_property(property_data)
        result=pm.update_property("TEST003",
                                  {"price": "200000"},)
        assert result is True
        updated_property =pm.get_property("TEST003")
        assert updated_property["price"] == "200000"