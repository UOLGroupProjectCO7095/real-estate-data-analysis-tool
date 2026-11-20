"""
Acceptance Criteria Verification Test Suite.

Directly maps to the 4 user acceptance criteria:
1. The system should check required property fields.
2. The system should validate property prices.
3. The system should check property information formats.
4. The system should identify invalid property records.
"""

import unittest
from src.data_cleaning import (
    check_required_fields,
    validate_price,
    check_property_id_format,
    check_property_type_format,
    check_room_count_format,
    check_listing_url_format,
    validate_property_record,
    filter_valid_records,
    process_pipeline_records,
)
from src.property_search import Property


class TestAcceptanceCriteria(unittest.TestCase):

    def setUp(self):
        self.valid_record = {
            "property_id": "PROP5001",
            "property_type": "house",
            "location": "Cambridge South",
            "price": 425000.0,
            "bedrooms": 3,
            "bathrooms": 2.0,
            "listing_url": "https://properties.example.com/item/5001"
        }

    # -------------------------------------------------------------------------
    # Criterion 1: The system should check required property fields.
    # -------------------------------------------------------------------------
    def test_criterion_1_required_fields_all_present(self):
        is_valid, errors = check_required_fields(self.valid_record)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_criterion_1_required_fields_missing_or_blank(self):
        record_missing = self.valid_record.copy()
        del record_missing["property_type"]
        record_missing["location"] = "   "
        record_missing["price"] = None

        is_valid, errors = check_required_fields(record_missing)
        self.assertFalse(is_valid)
        self.assertIn("property_type", errors)
        self.assertIn("location", errors)
        self.assertIn("price", errors)

    # -------------------------------------------------------------------------
    # Criterion 2: The system should validate property prices.
    # -------------------------------------------------------------------------
    def test_criterion_2_validate_prices(self):
        # Valid prices (numeric, string formatting, positive bounds)
        self.assertTrue(validate_price(150000)[0])
        self.assertTrue(validate_price("$550,000.00")[0])
        self.assertTrue(validate_price("£320000")[0])

        # Invalid prices (zero, negative, exceeding upper ceiling, non-numeric)
        self.assertFalse(validate_price(0)[0])
        self.assertFalse(validate_price(-25000)[0])
        self.assertFalse(validate_price(2_000_000_000)[0])
        self.assertFalse(validate_price("not_a_number")[0])
        self.assertFalse(validate_price(None)[0])
        self.assertFalse(validate_price(True)[0])

    # -------------------------------------------------------------------------
    # Criterion 3: The system should check property information formats.
    # -------------------------------------------------------------------------
    def test_criterion_3_property_formats(self):
        # Property ID format
        self.assertTrue(check_property_id_format("PROP_99")[0])
        self.assertTrue(check_property_id_format(101)[0])
        self.assertFalse(check_property_id_format("")[0])
        self.assertFalse(check_property_id_format(-5)[0])

        # Property Type format
        self.assertTrue(check_property_type_format("Apartment")[0])
        self.assertTrue(check_property_type_format("villa")[0])
        self.assertFalse(check_property_type_format("spaceship")[0])

        # Room count format
        self.assertTrue(check_room_count_format(3, "bedrooms")[0])
        self.assertTrue(check_room_count_format("1.5", "bathrooms")[0])
        self.assertFalse(check_room_count_format(-1, "bedrooms")[0])
        self.assertFalse(check_room_count_format(150, "bathrooms")[0])

        # Listing URL format
        self.assertTrue(check_listing_url_format("https://rightmove.co.uk/p/1")[0])
        self.assertFalse(check_listing_url_format("ftp://bad_scheme")[0])
        self.assertFalse(check_listing_url_format("invalid_url_text")[0])

    # -------------------------------------------------------------------------
    # Criterion 4: The system should identify invalid property records.
    # -------------------------------------------------------------------------
    def test_criterion_4_identify_invalid_records(self):
        dataset = [
            self.valid_record,
            {
                "property_id": "PROP_INVALID_1",
                "property_type": "penthouse_custom",  # Invalid type format
                "location": "London",
                "price": -1000,                       # Invalid price
                "bedrooms": 2,
                "bathrooms": 1,
                "listing_url": "https://example.com/p1"
            },
            {
                "property_id": "PROP_INVALID_2",
                # missing property_type
                "location": "Bristol",
                "price": 200000,
                "bedrooms": -5,                       # Invalid room count
                "bathrooms": 1,
                "listing_url": "not_a_valid_url"      # Invalid URL format
            }
        ]

        valid_list, rejected_list = filter_valid_records(dataset)

        self.assertEqual(len(valid_list), 1)
        self.assertEqual(len(rejected_list), 2)

        # Ensure reasons for rejection are explicitly captured
        rej1_errors = rejected_list[0]["errors"]
        self.assertTrue(any("Invalid 'property_type'" in e for e in rej1_errors))
        self.assertTrue(any("Invalid 'price'" in e for e in rej1_errors))

        rej2_errors = rejected_list[1]["errors"]
        self.assertTrue(any("Missing or empty required field: property_type" in e for e in rej2_errors))

    # -------------------------------------------------------------------------
    # Open Pipeline Test: Auto-integrates with Member 1 and Member 4 entities
    # -------------------------------------------------------------------------
    def test_open_pipeline_integration_with_member_entities(self):
        # 1. Pipeline with None invokes fetch_raw_collected_data() from src.data_collection
        valid_from_file, rej_from_file = process_pipeline_records(None)
        self.assertIsInstance(valid_from_file, list)
        self.assertIsInstance(rej_from_file, list)

        # 2. Pipeline with invalid source type returns empty results safely
        v_bad, r_bad = process_pipeline_records(12345)
        self.assertEqual(len(v_bad), 0)
        self.assertEqual(len(r_bad), 0)

        # 3. Once Member 4 creates Property objects, pipeline consumes them directly
        prop_obj = Property(
            property_id="P_MEM4",
            property_type="apartment",
            location="Oxford",
            price=300000,
            bedrooms=2,
            bathrooms=1,
            listing_url="https://oxfordproperties.com/p"
        )
        valid_recs, rejected_recs = process_pipeline_records([prop_obj])
        self.assertEqual(len(valid_recs), 1)
        self.assertEqual(len(rejected_recs), 0)

    # -------------------------------------------------------------------------
    # URL Processing and Details Extraction Tests
    # -------------------------------------------------------------------------
    def test_extract_details_from_url_amberstudent_ensuite(self):
        from src.data_cleaning import extract_details_from_url
        url = "https://amberstudent.com/places/dover-street-apartments-leicester-2106166153995?range_available_price=79%2C150&move_in_month=jan-2027&meta_types=ensuite"
        d = extract_details_from_url(url)
        self.assertEqual(d["property_id"], "PROP_2106166153995")
        self.assertEqual(d["property_type"], "ensuite")
        self.assertEqual(d["location"], "Leicester")
        self.assertEqual(d["price"], "114")
        self.assertEqual(d["listing_url"], url)
        self.assertTrue(len(d["amenities"]) > 0)
        self.assertTrue(len(d["room_types"]) > 0)

    def test_extract_details_from_url_general_and_fallbacks(self):
        from src.data_cleaning import extract_details_from_url
        # Empty and non-string inputs
        self.assertEqual(extract_details_from_url("")["property_type"], "")
        self.assertEqual(extract_details_from_url(None)["property_type"], "")

        # General property URL with query price
        url2 = "https://example.com/listings/luxury-condo-london?price=500000"
        d2 = extract_details_from_url(url2)
        self.assertEqual(d2["property_type"], "condo")
        self.assertEqual(d2["location"], "London")
        self.assertEqual(d2["price"], "500000")

        # Fallback slug without recognized city or type
        url3 = "https://example.com/items/special-lot"
        d3 = extract_details_from_url(url3)
        self.assertTrue(d3["property_id"].startswith("PROP_"))
        self.assertEqual(d3["property_type"], "apartment")
        self.assertEqual(d3["location"], "City Centre")


if __name__ == "__main__":
    unittest.main()
