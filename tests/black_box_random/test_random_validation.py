"""
Random-Based Black-Box Test Suite for Property Validation.

Technique: Black-Box Testing -> Random-Based Testing (Fuzzing / Automated Input Generation).
Functions under test: validate_required_fields, validate_property_record
Author: Member 2 (Data Processing)
"""

import unittest
import random
import string
from src.data_cleaning import (
    validate_required_fields,
    validate_property_record,
    REQUIRED_PROPERTY_FIELDS,
    ALLOWED_PROPERTY_TYPES,
)


def generate_random_string(min_len=1, max_len=20) -> str:
    chars = string.ascii_letters + string.digits + " _-"
    return "".join(random.choice(chars) for _ in range(random.randint(min_len, max_len)))


def generate_random_valid_record(index: int) -> dict:
    ptype = random.choice(ALLOWED_PROPERTY_TYPES)
    if ptype == "studio":
        beds = 0
        baths = 1
    elif ptype == "land":
        beds = 0
        baths = 0
    elif ptype in ["ensuite", "non-ensuite", "1b"]:
        beds = 1
        baths = 1
    else:
        beds = random.randint(1, 10)
        baths = random.randint(1, 8)

    return {
        "property_id": f"PROP_{index}_{random.randint(1000, 9999)}",
        "property_type": ptype,
        "location": f"{generate_random_string(5, 15)}, City",
        "price": round(random.uniform(50000.0, 5000000.0), 2),
        "bedrooms": beds,
        "bathrooms": baths,
        "listing_url": f"https://realestate-test.org/listing/{index}"
    }


def generate_random_fuzzed_record(index: int) -> dict:
    """
    Randomly mutates fields to test robustness against unexpected inputs.
    """
    record = generate_random_valid_record(index)
    mutation_type = random.choice([
        "omit_field",
        "none_value",
        "empty_string",
        "negative_price",
        "extreme_price",
        "invalid_type",
        "corrupted_url",
        "valid"
    ])

    if mutation_type == "omit_field":
        field = random.choice(REQUIRED_PROPERTY_FIELDS)
        del record[field]
    elif mutation_type == "none_value":
        field = random.choice(REQUIRED_PROPERTY_FIELDS)
        record[field] = None
    elif mutation_type == "empty_string":
        field = random.choice(["property_id", "location", "listing_url"])
        record[field] = "   "
    elif mutation_type == "negative_price":
        record["price"] = -random.uniform(1.0, 50000.0)
    elif mutation_type == "extreme_price":
        record["price"] = 2_000_000_000.0
    elif mutation_type == "invalid_type":
        record["property_type"] = "unknown_type_" + generate_random_string(4, 8)
    elif mutation_type == "corrupted_url":
        record["listing_url"] = "not_a_valid_url"

    return record


class TestRandomBlackBoxValidation(unittest.TestCase):
    """
    Executes repeated pseudo-random tests to ensure stability, absence of unhandled
    exceptions, and adherence to specification.
    """

    def setUp(self):
        # Set fixed seed for reproducibility in automated grading environments
        random.seed(42)

    def test_random_valid_records_always_pass_required_fields(self):
        for i in range(50):
            valid_rec = generate_random_valid_record(i)
            is_valid, errors = validate_required_fields(valid_rec)
            self.assertTrue(is_valid, f"Failed on iteration {i}: {errors}")
            self.assertEqual(len(errors), 0)

    def test_random_valid_records_always_pass_full_validation(self):
        for i in range(50):
            valid_rec = generate_random_valid_record(i)
            is_valid, errors = validate_property_record(valid_rec)
            self.assertTrue(is_valid, f"Failed on iteration {i}: {errors}")
            self.assertEqual(len(errors), 0)

    def test_random_fuzzed_records_never_raise_unhandled_exception(self):
        """
        Fuzzing test: Generates 100 randomly corrupted or valid records and verifies
        the validator never crashes with unexpected runtime errors (TypeError, KeyError, etc.).
        """
        for i in range(100):
            record = generate_random_fuzzed_record(i)
            try:
                is_valid, errors = validate_property_record(record)
                self.assertIsInstance(is_valid, bool)
                self.assertIsInstance(errors, list)
            except Exception as exc:
                self.fail(f"Unhandled exception on random test #{i} with input {record}: {exc}")

    def test_random_duplicate_injection_and_handling(self):
        """
        Fuzzing test for duplicates: Generates random streams, injects duplicates,
        and verifies deterministic duplicate detection and resolution across all strategies.
        """
        from src.data_cleaning import identify_duplicates, handle_duplicates
        base_records = [generate_random_valid_record(i) for i in range(30)]

        # Inject 10 duplicates randomly
        injected_records = list(base_records)
        injected_count = 0
        for _ in range(10):
            target = random.choice(base_records)
            dup = target.copy()
            # Randomly pick duplication mode
            mode = random.choice(["exact", "url_param", "semantic_price"])
            if mode == "url_param":
                dup["listing_url"] = target["listing_url"] + "?tracking_id=123"
            elif mode == "semantic_price":
                dup["property_id"] = f"MOCK_NEW_{random.randint(10000, 99999)}"
            injected_records.append(dup)
            injected_count += 1

        # Run duplicate identification
        report = identify_duplicates(injected_records)
        self.assertEqual(report["total_records"], 30 + injected_count)
        self.assertGreaterEqual(report["duplicate_count"], injected_count)
        self.assertEqual(report["unique_count"], 30)

        # Test all resolution strategies
        for strat in ["keep_first", "keep_last", "flag_only", "merge_records", "remove_all"]:
            handled, dups = handle_duplicates(injected_records, strategy=strat)
            self.assertIsInstance(handled, list)
            self.assertIsInstance(dups, list)


if __name__ == "__main__":
    unittest.main()
