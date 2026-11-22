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

    # =========================================================================
    # Category 4: Duplicate Types & Partitions (Ostrand & Balcer)
    # =========================================================================
    def test_category_duplicate_partitions(self):
        from src.data_cleaning import check_duplicate_pair
        base = self.valid_baseline.copy()

        # Partition 4.1: Exact ID Match
        id_dup = self.valid_baseline.copy()
        id_dup["location"] = "Different Location"
        is_dup, reason = check_duplicate_pair(base, id_dup)
        self.assertTrue(is_dup)
        self.assertIn("Exact property_id match", reason)

        # Partition 4.2: Canonical URL Match
        url_dup = {
            "property_id": "PROP_OTHER",
            "property_type": "apartment",
            "location": "Other City",
            "price": 999999,
            "bedrooms": 1,
            "bathrooms": 1,
            "listing_url": self.valid_baseline["listing_url"] + "?utm_source=test"
        }
        is_dup_u, reason_u = check_duplicate_pair(base, url_dup)
        self.assertTrue(is_dup_u)
        self.assertIn("Duplicate canonical listing URL", reason_u)

        # Partition 4.3: Semantic Attribute Match
        sem_dup = {
            "property_id": "PROP_OTHER_2",
            "property_type": "apartment",
            "location": "Downtown, City Centre",
            "price": 250000.0,
            "bedrooms": 2,
            "bathrooms": 1.5,
            "listing_url": "https://other-portal.org/item/888"
        }
        is_dup_s, reason_s = check_duplicate_pair(base, sem_dup)
        self.assertTrue(is_dup_s)
        self.assertIn("Semantic property duplicate", reason_s)

        # Partition 4.4: Completely Disjoint Record (Unique)
        unique_rec = {
            "property_id": "PROP_UNIQUE_999",
            "property_type": "villa",
            "location": "Edinburgh South",
            "price": 890000.0,
            "bedrooms": 5,
            "bathrooms": 4,
            "listing_url": "https://other-domain.co.uk/unique"
        }
        is_dup_n, _ = check_duplicate_pair(base, unique_rec)
        self.assertFalse(is_dup_n)

    # =========================================================================
    # Category 5: Duplicate Resolution Strategy Partitions
    # =========================================================================
    def test_category_duplicate_resolution_strategies(self):
        from src.data_cleaning import handle_duplicates
        batch = [
            self.valid_baseline.copy(),
            self.valid_baseline.copy(),
            {
                "property_id": "PROP_UNIQUE",
                "property_type": "house",
                "location": "Bristol",
                "price": 300000,
                "bedrooms": 3,
                "bathrooms": 2,
                "listing_url": "https://unique.org/p"
            }
        ]

        # Partition 5.1: keep_first
        k_first, d_first = handle_duplicates(batch, strategy="keep_first")
        self.assertEqual(len(k_first), 2)
        self.assertEqual(len(d_first), 1)

        # Partition 5.2: keep_last
        k_last, d_last = handle_duplicates(batch, strategy="keep_last")
        self.assertEqual(len(k_last), 2)

        # Partition 5.3: flag_only
        flagged, _ = handle_duplicates(batch, strategy="flag_only")
        self.assertEqual(len(flagged), 3)

        # Partition 5.4: merge_records
        merged, _ = handle_duplicates(batch, strategy="merge_records")
        self.assertEqual(len(merged), 2)

        # Partition 5.5: remove_all (quarantine)
        quarantine, _ = handle_duplicates(batch, strategy="remove_all")
        self.assertEqual(len(quarantine), 1)
        self.assertEqual(quarantine[0]["property_id"], "PROP_UNIQUE")

        # Partition 5.6: Invalid strategy raises ValueError
        with self.assertRaises(ValueError):
            handle_duplicates(batch, strategy="invalid_strategy_xyz")

    # =========================================================================
    # Category 6: Property Record Comparison Partitions (Criterion 1)
    # =========================================================================
    def test_category_property_comparison_partitions(self):
        from src.data_cleaning import compare_property_records
        base = self.valid_baseline.copy()

        # Partition 6.1: Identical Records
        res_ident = compare_property_records(base, base.copy())
        self.assertTrue(res_ident["are_identical"])
        self.assertTrue(res_ident["is_match"])
        self.assertEqual(res_ident["similarity_score"], 1.0)

        # Partition 6.2: Same ID, Mutated Location
        mut_loc = base.copy()
        mut_loc["location"] = "Manchester North"
        res_same_id = compare_property_records(base, mut_loc)
        self.assertTrue(res_same_id["is_match"])
        self.assertFalse(res_same_id["are_identical"])
        self.assertIn("location", res_same_id["differing_fields"])

        # Partition 6.3: Canonical URL Match
        url_match = {
            "property_id": "P_OTHER_URL",
            "property_type": "flat",
            "location": "Other Area",
            "price": 999999,
            "bedrooms": 1,
            "bathrooms": 1,
            "listing_url": base["listing_url"] + "/?utm_source=ad"
        }
        res_url = compare_property_records(base, url_match)
        self.assertTrue(res_url["is_match"])
        self.assertTrue(res_url["url_canonical_match"])

        # Partition 6.4: Completely Disjoint Records
        disjoint = {
            "property_id": "P_DISJOINT",
            "property_type": "detached",
            "location": "Edinburgh South",
            "price": 850000,
            "bedrooms": 5,
            "bathrooms": 4,
            "listing_url": "https://other.co.uk/unique"
        }
        res_disjoint = compare_property_records(base, disjoint)
        self.assertFalse(res_disjoint["is_match"])
        self.assertEqual(res_disjoint["similarity_score"], 0.0)

        # Partition 6.5: Invalid Inputs (None, non-dict)
        self.assertFalse(compare_property_records(None, base)["is_match"])
        self.assertFalse(compare_property_records(base, "not_dict")["is_match"])


if __name__ == "__main__":
    unittest.main()
