"""
Category Partition Test Suite for Property Validation.

Technique: Black-Box Testing -> Specification-Based -> Category Partition Method (Ostrand & Balcer).
Function under test: validate_required_fields, validate_property_record
Author: Member 2 (Data Processing)
"""

import unittest
from src.data_cleaning import (
    validate_required_fields,
    validate_property_record,
    REQUIRED_PROPERTY_FIELDS,
)


class TestCategoryPartitionValidation(unittest.TestCase):
    """
    Categories and Partitions identified:
    Category 1: Record Type
        - Partition 1.1: None
        - Partition 1.2: Non-dictionary (e.g. list, string, integer)
        - Partition 1.3: Dictionary

    Category 2: Required Fields Presence
        - Partition 2.1: All required keys present
        - Partition 2.2: One required key missing
        - Partition 2.3: Multiple required keys missing
        - Partition 2.4: Empty dictionary (all keys missing)

    Category 3: Field Value Emptiness
        - Partition 3.1: All values non-empty
        - Partition 3.2: Value is None
        - Partition 3.3: Value is empty string ""
        - Partition 3.4: Value is whitespace string "   "
    """

    def setUp(self):
        self.valid_baseline = {
            "property_id": "PROP1001",
            "property_type": "Apartment",
            "location": "Downtown, City Centre",
            "price": 250000.0,
            "bedrooms": 2,
            "bathrooms": 1.5,
            "listing_url": "https://properties.example.com/item/1001"
        }

    # Partition 1.1: Record is None
    def test_record_type_none(self):
        is_valid, errors = validate_required_fields(None)
        self.assertFalse(is_valid)
        self.assertIn("RECORD_IS_NONE", errors)

    # Partition 1.2: Record is non-dict
    def test_record_type_invalid_type(self):
        for invalid_input in [["PROP1"], "string_record", 12345]:
            with self.subTest(invalid_input=invalid_input):
                is_valid, errors = validate_required_fields(invalid_input)
                self.assertFalse(is_valid)
                self.assertIn("RECORD_MUST_BE_DICT", errors)

    # Partition 2.1 & 3.1: All required keys present and populated
    def test_all_required_keys_present_and_valid(self):
        is_valid, errors = validate_required_fields(self.valid_baseline)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    # Partition 2.2: One required key missing
    def test_single_required_key_missing(self):
        for field in REQUIRED_PROPERTY_FIELDS:
            with self.subTest(missing_field=field):
                record = self.valid_baseline.copy()
                del record[field]
                is_valid, errors = validate_required_fields(record)
                self.assertFalse(is_valid)
                self.assertIn(field, errors)

    # Partition 2.3: Multiple required keys missing
    def test_multiple_required_keys_missing(self):
        record = self.valid_baseline.copy()
        del record["price"]
        del record["bedrooms"]
        del record["listing_url"]
        is_valid, errors = validate_required_fields(record)
        self.assertFalse(is_valid)
        self.assertIn("price", errors)
        self.assertIn("bedrooms", errors)
        self.assertIn("listing_url", errors)
        self.assertEqual(len(errors), 3)

    # Partition 2.4: Empty dictionary
    def test_empty_record_dict(self):
        is_valid, errors = validate_required_fields({})
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), len(REQUIRED_PROPERTY_FIELDS))

    # Partition 3.2: Required field value is None
    def test_required_field_value_is_none(self):
        for field in REQUIRED_PROPERTY_FIELDS:
            with self.subTest(none_field=field):
                record = self.valid_baseline.copy()
                record[field] = None
                is_valid, errors = validate_required_fields(record)
                self.assertFalse(is_valid)
                self.assertIn(field, errors)

    # Partition 3.3 & 3.4: Required field value is empty string or whitespace
    def test_required_field_value_is_whitespace_or_empty(self):
        for field in REQUIRED_PROPERTY_FIELDS:
            with self.subTest(empty_field=field):
                record = self.valid_baseline.copy()
                record[field] = "   "
                is_valid, errors = validate_required_fields(record)
                self.assertFalse(is_valid)
                self.assertIn(field, errors)

    # Full record validation integration test under Category Partition
    def test_full_property_record_valid_specification(self):
        is_valid, errors = validate_property_record(self.valid_baseline)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
