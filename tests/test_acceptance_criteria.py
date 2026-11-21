"""
Acceptance Criteria Verification Test Suite (Member 2 - Data Processing).

USER STORY 1: Clean Property Data
As a data processing team member, I want to clean property data so that the analysis is based on accurate and complete information.
Acceptance Criteria:
1. The system should check required property fields.
2. The system should validate property prices.
3. The system should check property information formats.
4. The system should identify invalid property records (including the 8 rubric validation areas).

USER STORY 2: Identify Duplicate Property Records
As a data processing team member, I want to identify duplicate property records so that repeated property information can be detected and handled.
Acceptance Criteria:
1. The system should compare property records.
2. The system should identify matching property information.
3. The system should flag duplicate property records.
4. The system should report detected duplicates.
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

        # 4. Open multi-source merging from Member 1 and Member 4
        from src.data_cleaning import merge_and_process_member_sources
        from src.data_collection import generate_mock_collected_properties
        from src.property_search import generate_mock_member4_properties

        m1_batch = generate_mock_collected_properties(count=3)
        m4_batch = generate_mock_member4_properties(count=3)

        merged_valid, merged_rej = merge_and_process_member_sources(m1_batch, m4_batch)
        self.assertEqual(len(merged_valid), 6)
        self.assertEqual(len(merged_rej), 0)

    # -------------------------------------------------------------------------
    # URL Processing and Details Extraction Tests
    # -------------------------------------------------------------------------
    def test_extract_details_from_url_amberstudent_ensuite(self):
        from src.data_cleaning import extract_details_from_url
        url = "https://amberstudent.com/places/dover-street-apartments-leicester-2106166153995?range_available_price=79%2C150&move_in_month=jan-2027&meta_types=ensuite"
        d = extract_details_from_url(url)
        self.assertEqual(d["property_id"], "PROP_2106166153995")
        self.assertEqual(d["property_type"], "ensuite")
        self.assertIn("Leicester", d["location"])
        self.assertEqual(d["price"], "114")
        self.assertEqual(d["listing_url"], url)
        self.assertTrue(len(d["amenities"]) > 0)
        self.assertTrue(len(d["room_types"]) > 0)

    def test_extract_details_from_url_queens_court(self):
        from src.data_cleaning import extract_details_from_url
        url = "https://amberstudent.com/places/queens-court-leicester-2103176973356"
        d = extract_details_from_url(url)
        self.assertEqual(d["property_id"], "PROP_2103176973356")
        self.assertEqual(d["property_name"], "Queens Court Leicester")
        self.assertEqual(d["price"], "89")
        self.assertEqual(d["room_breakdown"]["Total Rooms"], 9)
        self.assertEqual(d["room_breakdown"]["Non Ensuite"], 5)
        self.assertEqual(d["room_breakdown"]["Studio"], 3)
        self.assertEqual(d["room_breakdown"]["1B"], 1)

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

    # =========================================================================
    # Acceptance Tests for the 8 Validation Areas
    # =========================================================================
    def test_acceptance_area_1_data_type_validation(self):
        from src.data_cleaning import validate_data_types
        # Valid data types
        valid_rec = {
            "property_id": "PROP100",
            "property_type": "flat",
            "location": "Manchester City",
            "price": 250000.0,
            "bedrooms": 2,
            "bathrooms": 1.5,
            "listing_url": "https://example.com/p100"
        }
        ok, errors = validate_data_types(valid_rec)
        self.assertTrue(ok)
        self.assertEqual(len(errors), 0)

        # Invalid data types: float bedroom (2.5), non-numeric price, bool bathrooms
        bad_types = {
            "property_id": "PROP101",
            "property_type": 12345,  # non-string
            "location": "Manchester",
            "price": "not_numeric",  # non-numeric price
            "bedrooms": 2.5,         # float bedroom rejected
            "bathrooms": True,       # bool bathroom rejected
            "listing_url": "https://example.com/p101"
        }
        ok_bad, bad_errors = validate_data_types(bad_types)
        self.assertFalse(ok_bad)
        self.assertTrue(any("bedrooms must be a whole integer" in e for e in bad_errors))
        self.assertTrue(any("price" in e and "not a numeric value" in e for e in bad_errors))
        self.assertTrue(any("bathrooms must be numeric" in e for e in bad_errors))
        self.assertTrue(any("property_type must be a textual string" in e for e in bad_errors))

    def test_acceptance_area_2_price_boundary_validation(self):
        from src.data_cleaning import validate_price_boundaries
        # Positive and within configured limits [100.0, 50,000,000.0]
        self.assertTrue(validate_price_boundaries(450000, min_price=100.0, max_price=50_000_000.0)[0])
        self.assertTrue(validate_price_boundaries("£1,250,000", min_price=100.0, max_price=50_000_000.0)[0])

        # Below configured minimum
        ok_low, msg_low = validate_price_boundaries(50.0, min_price=100.0)
        self.assertFalse(ok_low)
        self.assertIn("below configured minimum", msg_low)

        # Above configured maximum
        ok_high, msg_high = validate_price_boundaries(60_000_000.0, max_price=50_000_000.0)
        self.assertFalse(ok_high)
        self.assertIn("exceeds configured maximum", msg_high)

    def test_acceptance_area_3_property_attribute_validation(self):
        from src.data_cleaning import validate_property_attributes
        valid_attr = {
            "bedrooms": 3,
            "bathrooms": 2,
            "size_sqft": 1200.5,
            "year_built": 2018
        }
        ok, errors = validate_property_attributes(valid_attr)
        self.assertTrue(ok)
        self.assertEqual(len(errors), 0)

        # Invalid attributes: size negative, year_built out of range
        bad_attr = {
            "bedrooms": 150,  # exceeds 100
            "bathrooms": -1,  # negative
            "size_sqft": -500, # negative size
            "year_built": 1400 # too old
        }
        ok_bad, bad_errors = validate_property_attributes(bad_attr)
        self.assertFalse(ok_bad)
        self.assertTrue(any("exceeds reasonable limit" in e for e in bad_errors))
        self.assertTrue(any("cannot be negative" in e for e in bad_errors))
        self.assertTrue(any("size_sqft must be greater than zero" in e for e in bad_errors))
        self.assertTrue(any("year_built" in e for e in bad_errors))

    def test_acceptance_area_4_property_type_validation_rubric_categories(self):
        from src.data_cleaning import check_property_type_format
        # Supported categories from coursework rubric
        for rubric_type in ["Detached", "Semi-detached", "Flat", "Terraced", "Bungalow", "Cottage"]:
            with self.subTest(ptype=rubric_type):
                ok, msg = check_property_type_format(rubric_type)
                self.assertTrue(ok, f"Expected {rubric_type} to be supported: {msg}")

        # Unsupported category
        ok_bad, msg_bad = check_property_type_format("Spaceship_Station")
        self.assertFalse(ok_bad)
        self.assertIn("Invalid property_type", msg_bad)

    def test_acceptance_area_5_location_format_validation(self):
        from src.data_cleaning import validate_location_format
        # Valid locations
        self.assertTrue(validate_location_format("Leicester (85 Jarrom St, LE2 7DJ)")[0])
        self.assertTrue(validate_location_format("London Central, Westminster")[0])
        self.assertTrue(validate_location_format("Oxford High Street")[0])

        # Invalid locations
        self.assertFalse(validate_location_format("")[0])
        self.assertFalse(validate_location_format("   ")[0])
        self.assertFalse(validate_location_format(None)[0])
        self.assertFalse(validate_location_format("12345")[0]) # Purely numbers
        self.assertFalse(validate_location_format("---")[0])   # Purely symbols

    def test_acceptance_area_6_date_validation_and_chronology(self):
        from src.data_cleaning import validate_date_format, validate_date_chronology
        # Valid date formats
        self.assertTrue(validate_date_format("2026-11-20", "listing_date")[0])
        self.assertTrue(validate_date_format("2026-11-20T10:30:00", "updated_date")[0])

        # Invalid date format
        self.assertFalse(validate_date_format("not-a-date", "listing_date")[0])
        self.assertFalse(validate_date_format("1920-01-01", "listing_date")[0]) # Out of realistic range

        # Date chronology
        self.assertTrue(validate_date_chronology("2026-11-01", "2026-11-20")[0])
        ok_rev, msg_rev = validate_date_chronology("2026-11-20", "2026-11-01")
        self.assertFalse(ok_rev)
        self.assertIn("cannot be earlier than listing_date", msg_rev)

    def test_acceptance_area_7_cross_field_consistency(self):
        from src.data_cleaning import validate_cross_field_consistency
        # 1. Studio with 4 bedrooms is inconsistent
        bad_studio = {"property_type": "studio", "bedrooms": 4, "bathrooms": 1}
        ok_s, err_s = validate_cross_field_consistency(bad_studio)
        self.assertFalse(ok_s)
        self.assertTrue(any("studio' cannot have 4 bedrooms" in e for e in err_s))

        # 2. Studio with 0 or 1 bedroom is consistent
        good_studio = {"property_type": "studio", "bedrooms": 0, "bathrooms": 1}
        self.assertTrue(validate_cross_field_consistency(good_studio)[0])

        # 3. Land with bedrooms/bathrooms is inconsistent
        bad_land = {"property_type": "land", "bedrooms": 2, "bathrooms": 1}
        ok_l, err_l = validate_cross_field_consistency(bad_land)
        self.assertFalse(ok_l)
        self.assertTrue(any("land' cannot have 2 bedrooms" in e for e in err_l))

        # 4. Land with 0 bedrooms and 0 bathrooms is consistent
        good_land = {"property_type": "land", "bedrooms": 0, "bathrooms": 0}
        self.assertTrue(validate_cross_field_consistency(good_land)[0])

        # 5. Extreme bedroom to bathroom discrepancy (5 beds, 0 baths)
        bad_ratio = {"property_type": "house", "bedrooms": 5, "bathrooms": 0}
        ok_r, err_r = validate_cross_field_consistency(bad_ratio)
        self.assertFalse(ok_r)
        self.assertTrue(any("cannot have 0 bathrooms" in e for e in err_r))

    def test_acceptance_area_8_allowed_value_validation(self):
        from src.data_cleaning import validate_allowed_values
        valid_opts = {
            "property_type": "terraced",
            "status": "available",
            "furnishing": "furnished",
            "tenure": "freehold"
        }
        ok, errors = validate_allowed_values(valid_opts)
        self.assertTrue(ok)
        self.assertEqual(len(errors), 0)

        # Invalid options
        bad_opts = {
            "property_type": "terraced",
            "status": "demolished",  # unsupported status
            "furnishing": "gold-plated", # unsupported furnishing
            "tenure": "alien_lease"  # unsupported tenure
        }
        ok_bad, bad_errors = validate_allowed_values(bad_opts)
        self.assertFalse(ok_bad)
        self.assertTrue(any("Invalid 'status'" in e for e in bad_errors))
        self.assertTrue(any("Invalid 'furnishing'" in e for e in bad_errors))
        self.assertTrue(any("Invalid 'tenure'" in e for e in bad_errors))

    # =========================================================================
    # Acceptance Tests for User Story 2: Duplicate Property Record Detection & Handling
    # =========================================================================
    def test_duplicate_criterion_1_exact_id_duplicates(self):
        from src.data_cleaning import is_exact_duplicate, identify_duplicates
        rec1 = self.valid_record.copy()
        rec2 = self.valid_record.copy()
        rec2["price"] = 430000.0  # slight variation but identical ID

        is_dup, reason = is_exact_duplicate(rec1, rec2)
        self.assertTrue(is_dup)
        self.assertIn("Exact property_id match", reason)

        # In dataset identification
        report = identify_duplicates([rec1, rec2])
        self.assertEqual(report["total_records"], 2)
        self.assertEqual(report["unique_count"], 1)
        self.assertEqual(report["duplicate_count"], 1)
        self.assertEqual(report["duplicate_records"][0]["property_id"], rec2["property_id"])

    def test_duplicate_criterion_2_listing_url_duplicates(self):
        from src.data_cleaning import is_url_duplicate, canonicalize_url
        rec1 = {
            "property_id": "PROP_SOURCE_A_101",
            "property_type": "apartment",
            "location": "Leicester City",
            "price": 120,
            "bedrooms": 1,
            "bathrooms": 1,
            "listing_url": "https://amberstudent.com/places/queens-court-leicester-2103176973356?utm_source=google"
        }
        rec2 = {
            "property_id": "PROP_SOURCE_B_999",  # different ID
            "property_type": "apartment",
            "location": "Leicester",
            "price": 120,
            "bedrooms": 1,
            "bathrooms": 1,
            "listing_url": "https://amberstudent.com/places/queens-court-leicester-2103176973356/"  # trailing slash, no tracking query
        }

        # Canonical URLs match
        self.assertEqual(canonicalize_url(rec1["listing_url"]), canonicalize_url(rec2["listing_url"]))

        # URL duplicate detected
        is_dup, reason = is_url_duplicate(rec1, rec2)
        self.assertTrue(is_dup)
        self.assertIn("Duplicate canonical listing URL", reason)

    def test_duplicate_criterion_3_semantic_attribute_duplicates(self):
        from src.data_cleaning import is_semantic_duplicate
        # Same physical property scraped with different IDs and slightly different URL formats
        rec1 = {
            "property_id": "MEMBER1_SCRAPE_55",
            "property_type": "house",
            "location": "Manchester South, High Street",
            "price": 320000,
            "bedrooms": 3,
            "bathrooms": 2,
            "listing_url": "https://source1.co.uk/item/55"
        }
        rec2 = {
            "property_id": "MEMBER4_DOMAIN_88",
            "property_type": "house",
            "location": "Manchester South",
            "price": 320000,
            "bedrooms": 3,
            "bathrooms": 2,
            "listing_url": "https://source2.co.uk/listing/88"
        }

        is_sem, reason = is_semantic_duplicate(rec1, rec2)
        self.assertTrue(is_sem)
        self.assertIn("Semantic property duplicate", reason)

    def test_duplicate_criterion_4_handling_strategies(self):
        from src.data_cleaning import handle_duplicates
        rec1 = {"property_id": "PROP1", "property_type": "house", "location": "Leeds", "price": 200000, "bedrooms": 3, "bathrooms": 2, "listing_url": "https://ex.com/1", "amenities": ["Garden"]}
        rec2 = {"property_id": "PROP1", "property_type": "house", "location": "Leeds", "price": 205000, "bedrooms": 3, "bathrooms": 2, "listing_url": "https://ex.com/1", "amenities": ["Parking"]}
        rec3 = {"property_id": "PROP2", "property_type": "flat", "location": "London", "price": 500000, "bedrooms": 2, "bathrooms": 1, "listing_url": "https://ex.com/2"}

        dataset = [rec1, rec2, rec3]

        # 1. Strategy: keep_first
        kept_first, dups_first = handle_duplicates(dataset, strategy="keep_first")
        self.assertEqual(len(kept_first), 2)
        self.assertEqual(len(dups_first), 1)
        self.assertEqual(kept_first[0]["price"], 200000)

        # 2. Strategy: keep_last
        kept_last, dups_last = handle_duplicates(dataset, strategy="keep_last")
        self.assertEqual(len(kept_last), 2)
        self.assertEqual(kept_last[0]["price"], 205000)

        # 3. Strategy: flag_only
        flagged, dups_flagged = handle_duplicates(dataset, strategy="flag_only")
        self.assertEqual(len(flagged), 3)
        self.assertFalse(flagged[0]["is_duplicate"])
        self.assertTrue(flagged[1]["is_duplicate"])
        self.assertEqual(flagged[1]["duplicate_of"], "PROP1")

        # 4. Strategy: merge_records
        merged, _ = handle_duplicates(dataset, strategy="merge_records")
        self.assertEqual(len(merged), 2)
        p1_merged = [m for m in merged if m["property_id"] == "PROP1"][0]
        self.assertIn("Garden", p1_merged["amenities"])
        self.assertIn("Parking", p1_merged["amenities"])

        # 5. Strategy: remove_all (quarantine)
        quarantined_valid, _ = handle_duplicates(dataset, strategy="remove_all")
        self.assertEqual(len(quarantined_valid), 1)
        self.assertEqual(quarantined_valid[0]["property_id"], "PROP2")

        # 6. Invalid strategy raises ValueError
        with self.assertRaises(ValueError):
            handle_duplicates(dataset, strategy="unsupported_strategy")

    def test_duplicate_report_generation(self):
        from src.data_cleaning import generate_duplicate_report
        rec1 = self.valid_record.copy()
        rec2 = self.valid_record.copy()
        report_text = generate_duplicate_report([rec1, rec2])
        self.assertIn("DUPLICATE PROPERTY DETECTION REPORT", report_text)
        self.assertIn("Total Records Analyzed : 2", report_text)
        self.assertIn("Duplicates Detected    : 1", report_text)
        self.assertIn("Exact property_id match", report_text)

    # =========================================================================
    # USER STORY 2: DIRECT ACCEPTANCE CRITERIA VERIFICATION
    # 1. The system should compare property records.
    # 2. The system should identify matching property information.
    # 3. The system should flag duplicate property records.
    # 4. The system should report detected duplicates.
    # =========================================================================

    # Criterion 1: The system should compare property records.
    def test_user_story_2_criterion_1_compare_property_records(self):
        from src.data_cleaning import compare_property_records
        rec1 = self.valid_record.copy()
        rec2 = self.valid_record.copy()

        # Identical comparison
        res_ident = compare_property_records(rec1, rec2)
        self.assertTrue(res_ident["is_match"])
        self.assertEqual(len(res_ident["differing_fields"]), 0)
        self.assertEqual(res_ident["similarity_score"], 1.0)
        self.assertIn("property_id", res_ident["identical_fields"])

        # Differing comparison (same ID but different location/price)
        rec_diff = self.valid_record.copy()
        rec_diff["location"] = "Leeds Central"
        rec_diff["price"] = 999000
        res_diff = compare_property_records(rec1, rec_diff)
        self.assertTrue(res_diff["is_match"]) # Matched on property_id
        self.assertIn("location", res_diff["differing_fields"])
        self.assertIn("price", res_diff["differing_fields"])

        # Completely distinct records
        rec_other = {
            "property_id": "PROP_DISTINCT_888",
            "property_type": "land",
            "location": "Yorkshire Green",
            "price": 100000,
            "bedrooms": 0,
            "bathrooms": 0,
            "listing_url": "https://distinct.org/item"
        }
        res_other = compare_property_records(rec1, rec_other)
        self.assertFalse(res_other["is_match"])
        self.assertEqual(len(res_other["identical_fields"]), 0)

        # Invalid input comparison
        res_invalid = compare_property_records(None, rec1)
        self.assertFalse(res_invalid["is_match"])

    # Criterion 2: The system should identify matching property information.
    def test_user_story_2_criterion_2_identify_matching_property_info(self):
        from src.data_cleaning import identify_matching_property_info
        rec1 = {
            "property_id": "PROP100",
            "property_type": "flat",
            "location": "Leicester City",
            "price": 150000,
            "bedrooms": 2,
            "bathrooms": 1,
            "listing_url": "https://amberstudent.com/places/flat-100?utm_source=ad"
        }
        rec2 = {
            "property_id": "PROP999",  # different ID
            "property_type": "flat",    # matching
            "location": "Leicester City", # matching
            "price": 150000,            # matching
            "bedrooms": 2,              # matching
            "bathrooms": 1,              # matching
            "listing_url": "https://amberstudent.com/places/flat-100/" # canonical URL matching
        }

        match_info = identify_matching_property_info(rec1, rec2)
        self.assertTrue(match_info["has_matches"])
        self.assertIn("property_type", match_info["matching_attributes"])
        self.assertIn("location", match_info["matching_attributes"])
        self.assertIn("bedrooms", match_info["matching_attributes"])
        self.assertIn("canonical_listing_url", match_info["matching_attributes"])
        self.assertEqual(match_info["match_category"], "CANONICAL_URL")

        # Distinct records
        rec3 = {"property_id": "P3", "property_type": "villa", "location": "Bristol", "price": 900000, "bedrooms": 5, "bathrooms": 4, "listing_url": "https://bristol.org"}
        distinct_info = identify_matching_property_info(rec1, rec3)
        self.assertEqual(distinct_info["match_category"], "NONE")

        # Invalid dictionary input
        self.assertFalse(identify_matching_property_info(None, None)["has_matches"])

    # Criterion 3: The system should flag duplicate property records.
    def test_user_story_2_criterion_3_flag_duplicate_property_records(self):
        from src.data_cleaning import flag_duplicate_property_records
        rec1 = {"property_id": "P1", "property_type": "flat", "location": "London", "price": 400000, "bedrooms": 2, "bathrooms": 1, "listing_url": "https://ex.com/p1"}
        rec2 = {"property_id": "P1", "property_type": "flat", "location": "London", "price": 400000, "bedrooms": 2, "bathrooms": 1, "listing_url": "https://ex.com/p1"}
        rec3 = {"property_id": "P2", "property_type": "house", "location": "Leeds", "price": 200000, "bedrooms": 3, "bathrooms": 2, "listing_url": "https://ex.com/p2"}

        dataset = [rec1, rec2, rec3]
        flagged = flag_duplicate_property_records(dataset)

        self.assertEqual(len(flagged), 3)

        # First record is primary
        self.assertFalse(flagged[0]["is_duplicate"])
        self.assertIsNone(flagged[0]["duplicate_of"])
        self.assertEqual(flagged[0]["duplicate_flag_status"], "PRIMARY_RECORD")

        # Second record is flagged duplicate
        self.assertTrue(flagged[1]["is_duplicate"])
        self.assertEqual(flagged[1]["duplicate_of"], "P1")
        self.assertEqual(flagged[1]["duplicate_flag_status"], "FLAGGED_DUPLICATE")
        self.assertIn("Exact property_id match", flagged[1]["duplicate_reason"])

        # Third record is primary
        self.assertFalse(flagged[2]["is_duplicate"])
        self.assertEqual(flagged[2]["duplicate_flag_status"], "PRIMARY_RECORD")

        # Non-list input raises TypeError
        with self.assertRaises(TypeError):
            flag_duplicate_property_records("not_a_list")

    # Criterion 4: The system should report detected duplicates.
    def test_user_story_2_criterion_4_report_detected_duplicates(self):
        from src.data_cleaning import report_detected_duplicates
        rec1 = {"property_id": "PROP_A", "property_type": "studio", "location": "Manchester", "price": 100000, "bedrooms": 0, "bathrooms": 1, "listing_url": "https://manchester.org/1"}
        rec2 = {"property_id": "PROP_A", "property_type": "studio", "location": "Manchester", "price": 100000, "bedrooms": 0, "bathrooms": 1, "listing_url": "https://manchester.org/1"}
        rec3 = {"property_id": "PROP_B", "property_type": "studio", "location": "Manchester", "price": 100000, "bedrooms": 0, "bathrooms": 1, "listing_url": "https://manchester.org/2"}

        report = report_detected_duplicates([rec1, rec2, rec3])

        # Validate audit metrics
        self.assertEqual(report["total_records_analyzed"], 3)
        self.assertEqual(report["duplicates_detected_count"], 2) # rec2 exact ID, rec3 semantic
        self.assertEqual(report["unique_records_count"], 1)
        self.assertGreater(report["duplicate_detection_rate_pct"], 0.0)

        # Validate duplicate items list
        self.assertEqual(len(report["detected_duplicates"]), 2)
        self.assertEqual(report["detected_duplicates"][0]["duplicate_of_id"], "PROP_A")

        # Validate formatted text report
        self.assertIn("DUPLICATE PROPERTY DETECTION REPORT", report["formatted_report"])
        self.assertIn("Duplicates Detected", report["formatted_report"])

        # Non-list input raises TypeError
        with self.assertRaises(TypeError):
            report_detected_duplicates(12345)


if __name__ == "__main__":
    unittest.main()
