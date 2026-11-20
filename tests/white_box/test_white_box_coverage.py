"""
White-Box Test Suite (Statement, Branch, and Condition Coverage).

Technique: White-Box Testing -> Control Flow Testing (McCabe Cyclomatic Complexity, Branch/Path Coverage).
Functions under test: validate_required_fields, validate_property_id, validate_property_type,
                      validate_price, validate_room_count, validate_url, validate_property_record, filter_valid_records
Author: Member 2 (Data Processing)
"""

import unittest
from src.data_cleaning import (
    validate_required_fields,
    validate_property_id,
    validate_property_type,
    validate_price,
    validate_room_count,
    validate_url,
    validate_property_record,
    filter_valid_records,
)


class TestWhiteBoxBranchCoverage(unittest.TestCase):
    """
    Targets every decision branch and path in the validation functions to achieve 100% coverage:
    - validate_required_fields:
        Branch 1: record is None
        Branch 2: record not isinstance dict
        Branch 3: field not in record
        Branch 4: val is None
        Branch 5: val is whitespace str
        Branch 6: val valid non-empty
    - validate_property_id:
        Branch 1: id is None
        Branch 2: id is int <= 0
        Branch 3: id is int > 0
        Branch 4: id is empty str
        Branch 5: id is non-empty str
        Branch 6: id is unsupported type (float, list)
    - validate_property_type:
        Branch 1: type is None
        Branch 2: type not str
        Branch 3: type not in ALLOWED_PROPERTY_TYPES
        Branch 4: type in ALLOWED_PROPERTY_TYPES (case insensitive)
    - validate_price:
        Branch 1: price is None
        Branch 2: price is bool
        Branch 3: price is (int, float) <= 0
        Branch 4: price is (int, float) > 1B
        Branch 5: price is valid (int, float)
        Branch 6: price is str with currency symbols, valid float
        Branch 7: price is str, non-numeric ValueError
        Branch 8: price is unsupported type
    - validate_room_count:
        Branch 1: count is None
        Branch 2: count is bool
        Branch 3: count < 0
        Branch 4: count > 100
        Branch 5: count valid (int, float)
        Branch 6: count valid str
        Branch 7: count invalid str (ValueError)
        Branch 8: count unsupported type
    - validate_url:
        Branch 1: url is None
        Branch 2: url not str
        Branch 3: url empty str
        Branch 4: url regex mismatch
        Branch 5: url valid match
    - filter_valid_records:
        Branch 1: records not isinstance list -> TypeError
        Branch 2: mix of valid and invalid records
    """

    def test_branch_validate_required_fields(self):
        # Branch 1
        ok, err = validate_required_fields(None)
        self.assertFalse(ok)
        self.assertIn("RECORD_IS_NONE", err)

        # Branch 2
        ok, err = validate_required_fields("not_a_dict")
        self.assertFalse(ok)
        self.assertIn("RECORD_MUST_BE_DICT", err)

        # Branch 3, 4, 5, 6
        rec = {
            "property_id": "P1",
            "property_type": "apartment",
            "location": None,  # Branch 4
            "price": "   ",     # Branch 5
            "bedrooms": 2,     # Branch 6
            # bathrooms omitted -> Branch 3
            "listing_url": "https://example.com"
        }
        ok, err = validate_required_fields(rec)
        self.assertFalse(ok)
        self.assertIn("location", err)
        self.assertIn("price", err)
        self.assertIn("bathrooms", err)

    def test_branch_validate_property_id(self):
        self.assertEqual(validate_property_id(None), (False, "property_id cannot be None"))
        self.assertEqual(validate_property_id(-5), (False, "property_id as int must be positive"))
        self.assertEqual(validate_property_id(0), (False, "property_id as int must be positive"))
        self.assertEqual(validate_property_id(101), (True, ""))
        self.assertEqual(validate_property_id(""), (False, "property_id string cannot be empty"))
        self.assertEqual(validate_property_id("   "), (False, "property_id string cannot be empty"))
        self.assertEqual(validate_property_id("PROP_001"), (True, ""))
        self.assertEqual(validate_property_id([101]), (False, "property_id must be string or integer"))

    def test_branch_validate_property_type(self):
        self.assertEqual(validate_property_type(None), (False, "property_type cannot be None"))
        self.assertEqual(validate_property_type(123), (False, "property_type must be a string"))
        ok, msg = validate_property_type("castle")
        self.assertFalse(ok)
        self.assertIn("Invalid property_type", msg)
        self.assertEqual(validate_property_type(" Condo "), (True, ""))

    def test_branch_validate_price(self):
        self.assertEqual(validate_price(None), (False, "price cannot be None"))
        self.assertEqual(validate_price(True), (False, "price cannot be a boolean"))
        self.assertEqual(validate_price(0), (False, "price must be greater than zero"))
        self.assertEqual(validate_price(-100), (False, "price must be greater than zero"))
        self.assertEqual(validate_price(1_000_000_001), (False, "price exceeds maximum realistic threshold (1 billion)"))
        self.assertEqual(validate_price(350000), (True, ""))
        self.assertEqual(validate_price("$500,000"), (True, ""))
        self.assertEqual(validate_price("-50"), (False, "price must be greater than zero"))
        self.assertEqual(validate_price("2000000000"), (False, "price exceeds maximum realistic threshold (1 billion)"))
        self.assertEqual(validate_price("invalid_numeric"), (False, "price string must be numeric"))
        self.assertEqual(validate_price({"price": 100}), (False, "price must be a number or numeric string"))

    def test_branch_validate_room_count(self):
        self.assertEqual(validate_room_count(None), (False, "bedrooms cannot be None"))
        self.assertEqual(validate_room_count(True), (False, "bedrooms cannot be a boolean"))
        self.assertEqual(validate_room_count(-1), (False, "bedrooms cannot be negative"))
        self.assertEqual(validate_room_count(105), (False, "bedrooms exceeds reasonable limit (100)"))
        self.assertEqual(validate_room_count(3), (True, ""))
        self.assertEqual(validate_room_count("2"), (True, ""))
        self.assertEqual(validate_room_count("-2"), (False, "bedrooms cannot be negative"))
        self.assertEqual(validate_room_count("150"), (False, "bedrooms exceeds reasonable limit (100)"))
        self.assertEqual(validate_room_count("two"), (False, "bedrooms string must be numeric"))
        self.assertEqual(validate_room_count([2]), (False, "bedrooms must be a number or numeric string"))

    def test_branch_validate_url(self):
        self.assertEqual(validate_url(None), (False, "listing_url cannot be None"))
        self.assertEqual(validate_url(12345), (False, "listing_url must be a string"))
        self.assertEqual(validate_url("   "), (False, "listing_url cannot be empty"))
        self.assertEqual(validate_url("not_url"), (False, "listing_url must be a valid http or https URL"))
        self.assertEqual(validate_url("https://example.com/prop/1"), (True, ""))

    def test_validate_property_record_decision_paths(self):
        # Missing required field
        ok, errors = validate_property_record({"property_id": "P1"})
        self.assertFalse(ok)
        self.assertTrue(len(errors) > 0)

        # Invalid field values on present fields
        bad_rec = {
            "property_id": -10,
            "property_type": "invalid_type",
            "location": "Downtown",
            "price": -500,
            "bedrooms": -1,
            "bathrooms": -1,
            "listing_url": "ftp://bad"
        }
        ok, errors = validate_property_record(bad_rec)
        self.assertFalse(ok)
        self.assertEqual(len(errors), 6)

    def test_filter_valid_records(self):
        with self.assertRaises(TypeError):
            filter_valid_records("not_a_list")

        dataset = [
            {
                "property_id": "P101",
                "property_type": "apartment",
                "location": "London",
                "price": 450000,
                "bedrooms": 2,
                "bathrooms": 1,
                "listing_url": "https://properties.co.uk/p101"
            },
            {
                "property_id": "P102",
                "property_type": "invalid_type",
                "location": "Manchester",
                "price": 250000,
                "bedrooms": 1,
                "bathrooms": 1,
                "listing_url": "https://properties.co.uk/p102"
            }
        ]
        valid, rejected = filter_valid_records(dataset)
        self.assertEqual(len(valid), 1)
        self.assertEqual(len(rejected), 1)
        self.assertEqual(rejected[0]["index"], 1)


if __name__ == "__main__":
    unittest.main()
