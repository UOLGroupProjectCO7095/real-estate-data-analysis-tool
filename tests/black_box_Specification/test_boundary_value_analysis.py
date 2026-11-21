"""
Boundary Value Analysis (BVA) & Equivalence Partitioning (EP) Test Suite.

Technique: Black-Box Testing -> Specification-Based -> Boundary Value Analysis.
Functions under test: validate_price, validate_room_count, validate_property_type
Author: Member 2 (Data Processing)
"""

import unittest
from src.data_cleaning import (
    validate_price,
    validate_room_count,
    validate_property_type,
    validate_url,
    ALLOWED_PROPERTY_TYPES,
)


class TestBoundaryValueAnalysis(unittest.TestCase):
    """
    BVA for Price:
    - Lower boundary: <= 0 (invalid), min positive epsilon (e.g. 0.01) (valid)
    - Nominal values: 100_000, 500_000 (valid)
    - Upper boundary: 1,000,000,000 (valid), 1,000,000,001 (invalid)

    BVA for Room Count (Bedrooms / Bathrooms):
    - Lower boundary: -1 (invalid), 0 (valid), 1 (valid)
    - Upper boundary: 100 (valid), 101 (invalid)
    """

    # --- Price BVA & EP ---
    def test_price_boundary_zero_and_negative(self):
        for invalid_price in [0, 0.0, -1, -500.50]:
            with self.subTest(price=invalid_price):
                ok, msg = validate_price(invalid_price)
                self.assertFalse(ok)
                self.assertIn("greater than zero", msg)

    def test_price_lower_valid_boundary(self):
        ok, msg = validate_price(0.01)
        self.assertTrue(ok)
        self.assertEqual(msg, "")

    def test_price_nominal_values(self):
        for valid_price in [1500, 250000, "350,000", "$450000", "£750000.50"]:
            with self.subTest(price=valid_price):
                ok, msg = validate_price(valid_price)
                self.assertTrue(ok)
                self.assertEqual(msg, "")

    def test_price_upper_boundary(self):
        # 1 Billion is max valid limit
        ok, msg = validate_price(1_000_000_000)
        self.assertTrue(ok)

        # Exceeding 1 Billion is rejected
        ok_above, msg_above = validate_price(1_000_000_000.01)
        self.assertFalse(ok_above)
        self.assertIn("exceeds maximum realistic threshold", msg_above)

    def test_price_type_partitions(self):
        # Boolean is rejected
        ok, _ = validate_price(True)
        self.assertFalse(ok)
        # None is rejected
        ok, _ = validate_price(None)
        self.assertFalse(ok)
        # Non-numeric string is rejected
        ok, _ = validate_price("one_million")
        self.assertFalse(ok)

    # --- Room Count BVA & EP ---
    def test_room_count_lower_boundary(self):
        # -1 is invalid
        ok, msg = validate_room_count(-1, "bedrooms")
        self.assertFalse(ok)
        self.assertIn("negative", msg)

        # 0 is valid (e.g. studio / vacant plot)
        ok_zero, _ = validate_room_count(0, "bedrooms")
        self.assertTrue(ok_zero)

        # 1 is valid
        ok_one, _ = validate_room_count(1, "bedrooms")
        self.assertTrue(ok_one)

    def test_room_count_upper_boundary(self):
        # 100 is valid limit
        ok_100, _ = validate_room_count(100, "bedrooms")
        self.assertTrue(ok_100)

        # 101 exceeds reasonable threshold
        ok_101, msg_101 = validate_room_count(101, "bedrooms")
        self.assertFalse(ok_101)
        self.assertIn("exceeds reasonable limit", msg_101)

    def test_room_count_type_partitions(self):
        ok, _ = validate_room_count(None, "bathrooms")
        self.assertFalse(ok)
        ok, _ = validate_room_count(False, "bathrooms")
        self.assertFalse(ok)
        ok, _ = validate_room_count("three", "bathrooms")
        self.assertFalse(ok)

    # --- Property Type EP ---
    def test_property_type_valid_categories(self):
        for ptype in ALLOWED_PROPERTY_TYPES:
            with self.subTest(ptype=ptype):
                ok, _ = validate_property_type(ptype.upper())
                self.assertTrue(ok)

    def test_property_type_invalid_categories(self):
        for invalid_type in ["submarine", "spaceship", "castle_in_the_air", "", None, 123]:
            with self.subTest(invalid_type=invalid_type):
                ok, _ = validate_property_type(invalid_type)
                self.assertFalse(ok)

    # --- Listing URL EP ---
    def test_listing_url_valid_and_invalid(self):
        ok, _ = validate_url("https://realestate.com/prop/1001")
        self.assertTrue(ok)

        ok, _ = validate_url("http://sub.domain.co.uk/listing?id=1")
        self.assertTrue(ok)

        ok_ftp, _ = validate_url("ftp://files.example.com")
        self.assertFalse(ok_ftp)

        ok_bad, _ = validate_url("not_a_valid_url")
        self.assertFalse(ok_bad)

    # --- Configured Price Boundaries BVA ---
    def test_configured_price_boundaries_bva(self):
        from src.data_cleaning import validate_price_boundaries
        min_p = 100.0
        max_p = 50_000_000.0

        # Lower bound BVA: min_p - 0.01, min_p, min_p + 0.01
        self.assertFalse(validate_price_boundaries(min_p - 0.01, min_p, max_p)[0])
        self.assertTrue(validate_price_boundaries(min_p, min_p, max_p)[0])
        self.assertTrue(validate_price_boundaries(min_p + 0.01, min_p, max_p)[0])

        # Upper bound BVA: max_p - 0.01, max_p, max_p + 0.01
        self.assertTrue(validate_price_boundaries(max_p - 0.01, min_p, max_p)[0])
        self.assertTrue(validate_price_boundaries(max_p, min_p, max_p)[0])
        self.assertFalse(validate_price_boundaries(max_p + 0.01, min_p, max_p)[0])

    # --- Property Attribute Size BVA ---
    def test_property_size_bva(self):
        from src.data_cleaning import validate_property_attributes
        # Lower bound: 0 (invalid), 0.1 (valid), 1 (valid)
        self.assertFalse(validate_property_attributes({"size_sqft": 0})[0])
        self.assertTrue(validate_property_attributes({"size_sqft": 0.1})[0])
        self.assertTrue(validate_property_attributes({"size_sqft": 1})[0])

        # Upper bound: 100000 (valid), 100001 (invalid)
        self.assertTrue(validate_property_attributes({"size_sqft": 100_000})[0])
        self.assertFalse(validate_property_attributes({"size_sqft": 100_000.1})[0])

    # --- Duplicate Detection Cardinality Boundaries BVA ---
    def test_duplicate_dataset_cardinality_boundaries(self):
        from src.data_cleaning import identify_duplicates
        # Boundary 0: Empty list
        rep_0 = identify_duplicates([])
        self.assertEqual(rep_0["total_records"], 0)
        self.assertEqual(rep_0["duplicate_count"], 0)

        # Boundary 1: Single record (no duplicates possible)
        single = [{"property_id": "P1", "property_type": "house", "location": "London", "price": 100, "bedrooms": 1, "bathrooms": 1, "listing_url": "https://a.com/1"}]
        rep_1 = identify_duplicates(single)
        self.assertEqual(rep_1["unique_count"], 1)
        self.assertEqual(rep_1["duplicate_count"], 0)

        # Boundary 2: 2 identical records (1 unique, 1 duplicate)
        rep_2 = identify_duplicates([single[0], single[0]])
        self.assertEqual(rep_2["unique_count"], 1)
        self.assertEqual(rep_2["duplicate_count"], 1)

        # Boundary N: 5 identical records (1 unique, 4 duplicates)
        rep_n = identify_duplicates([single[0]] * 5)
        self.assertEqual(rep_n["unique_count"], 1)
        self.assertEqual(rep_n["duplicate_count"], 4)


if __name__ == "__main__":
    unittest.main()
