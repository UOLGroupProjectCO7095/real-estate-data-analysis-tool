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

    # =========================================================================
    # White-Box Branch Coverage for All 8 Validation Areas
    # =========================================================================
    def test_white_box_validate_data_types_branches(self):
        from src.data_cleaning import validate_data_types
        # None and non-dict branches
        self.assertFalse(validate_data_types(None)[0])
        self.assertFalse(validate_data_types("not_dict")[0])

        # Price branches: bool, unsupported type, string unparseable
        self.assertFalse(validate_data_types({"price": True})[0])
        self.assertFalse(validate_data_types({"price": ["not_num"]})[0])
        self.assertFalse(validate_data_types({"price": "abc"})[0])
        self.assertTrue(validate_data_types({"price": 50000})[0])
        self.assertTrue(validate_data_types({"price": "£50,000"})[0])

        # Bedrooms branches: bool, non-int float, int float, int string, non-int string, unparseable str, unsupported
        self.assertFalse(validate_data_types({"bedrooms": True})[0])
        self.assertFalse(validate_data_types({"bedrooms": 2.5})[0])
        self.assertTrue(validate_data_types({"bedrooms": 2.0})[0])
        self.assertTrue(validate_data_types({"bedrooms": "3"})[0])
        self.assertFalse(validate_data_types({"bedrooms": "3.5"})[0])
        self.assertFalse(validate_data_types({"bedrooms": "two"})[0])
        self.assertFalse(validate_data_types({"bedrooms": [2]})[0])

        # Bathrooms branches: bool, non-numeric str, unsupported
        self.assertFalse(validate_data_types({"bathrooms": True})[0])
        self.assertFalse(validate_data_types({"bathrooms": "three"})[0])
        self.assertFalse(validate_data_types({"bathrooms": [1]})[0])
        self.assertTrue(validate_data_types({"bathrooms": 1.5})[0])

        # Textual fields non-string branches
        self.assertFalse(validate_data_types({"property_type": 123})[0])
        self.assertFalse(validate_data_types({"location": ["London"]})[0])
        self.assertFalse(validate_data_types({"listing_url": 999})[0])

    def test_white_box_property_attributes_branches(self):
        from src.data_cleaning import validate_property_attributes
        self.assertFalse(validate_property_attributes(None)[0])
        self.assertFalse(validate_property_attributes("string")[0])

        # Size branches: bool, negative, > 100k, unparseable
        self.assertFalse(validate_property_attributes({"size_sqft": True})[0])
        self.assertFalse(validate_property_attributes({"size_sqft": -10})[0])
        self.assertFalse(validate_property_attributes({"size_sqft": 150_000})[0])
        self.assertFalse(validate_property_attributes({"size_sqft": "huge"})[0])
        self.assertTrue(validate_property_attributes({"size_sqft": 1500})[0])

        # Year built branches: < 1500, > 2035, non-int
        self.assertFalse(validate_property_attributes({"year_built": 1400})[0])
        self.assertFalse(validate_property_attributes({"year_built": 2050})[0])
        self.assertFalse(validate_property_attributes({"year_built": "ancient"})[0])
        self.assertTrue(validate_property_attributes({"year_built": 2020})[0])

    def test_white_box_location_format_branches(self):
        from src.data_cleaning import validate_location_format
        self.assertFalse(validate_location_format(None)[0])
        self.assertFalse(validate_location_format(12345)[0])
        self.assertFalse(validate_location_format("")[0])
        self.assertFalse(validate_location_format("A")[0]) # < 2 letters
        self.assertFalse(validate_location_format("12345 678")[0]) # only numbers
        self.assertTrue(validate_location_format("Leeds Central")[0])

    def test_white_box_date_branches(self):
        from src.data_cleaning import validate_date_format, validate_date_chronology
        self.assertFalse(validate_date_format(None)[0])
        self.assertFalse(validate_date_format(12345)[0])
        self.assertFalse(validate_date_format("")[0])
        self.assertFalse(validate_date_format("invalid-date-format")[0])
        self.assertFalse(validate_date_format("1950-01-01")[0]) # < 1970
        self.assertFalse(validate_date_format("2099-01-01")[0]) # > current + 5
        self.assertTrue(validate_date_format("2026-11-20")[0])

        # Chronology branches
        self.assertTrue(validate_date_chronology(None, "2026-11-20")[0])
        self.assertTrue(validate_date_chronology("2026-11-20", None)[0])
        self.assertFalse(validate_date_chronology("bad_date_1", "bad_date_2")[0])
        self.assertFalse(validate_date_chronology("2026-11-20", "2026-11-01")[0]) # updated < listing
        self.assertTrue(validate_date_chronology("2026-11-01", "2026-11-20")[0])  # updated >= listing

    def test_white_box_cross_field_and_allowed_values_branches(self):
        from src.data_cleaning import validate_cross_field_consistency, validate_allowed_values
        self.assertFalse(validate_cross_field_consistency(None)[0])
        self.assertFalse(validate_cross_field_consistency("not_dict")[0])

        # Studio with beds > 1 vs beds <= 1
        self.assertFalse(validate_cross_field_consistency({"property_type": "studio", "bedrooms": 3})[0])
        self.assertTrue(validate_cross_field_consistency({"property_type": "studio", "bedrooms": 1})[0])

        # Land with beds/baths vs 0
        self.assertFalse(validate_cross_field_consistency({"property_type": "land", "bedrooms": 1, "bathrooms": 0})[0])
        self.assertFalse(validate_cross_field_consistency({"property_type": "land", "bedrooms": 0, "bathrooms": 1})[0])
        self.assertTrue(validate_cross_field_consistency({"property_type": "land", "bedrooms": 0, "bathrooms": 0})[0])

        # Allowed values branches
        self.assertFalse(validate_allowed_values(None)[0])
        self.assertFalse(validate_allowed_values("not_dict")[0])
        self.assertFalse(validate_allowed_values({"property_type": "unknown_castle"})[0])
        self.assertFalse(validate_allowed_values({"status": "invalid_status"})[0])
        self.assertFalse(validate_allowed_values({"furnishing": "invalid_furnishing"})[0])
        self.assertFalse(validate_allowed_values({"tenure": "invalid_tenure"})[0])
        self.assertTrue(validate_allowed_values({
            "property_type": "detached",
            "status": "available",
            "furnishing": "furnished",
            "tenure": "freehold"
        })[0])

    # =========================================================================
    # White-Box Branch Coverage for Duplicate Engine
    # =========================================================================
    def test_white_box_canonicalize_url(self):
        from src.data_cleaning import canonicalize_url
        self.assertEqual(canonicalize_url(None), "")
        self.assertEqual(canonicalize_url(12345), "")
        url = "https://EXAMPLE.COM/places/flat-1/?utm_source=fb&utm_medium=cpc&id=10"
        canon = canonicalize_url(url)
        self.assertNotIn("utm_source", canon)
        self.assertIn("id=10", canon)
        self.assertTrue(canon.startswith("https://example.com/places/flat-1"))

    def test_white_box_duplicate_pair_and_handling_branches(self):
        from src.data_cleaning import (
            is_exact_duplicate,
            is_url_duplicate,
            is_semantic_duplicate,
            check_duplicate_pair,
            identify_duplicates,
            handle_duplicates,
            deduplicate_dataset,
            generate_duplicate_report
        )
        # Non-dict inputs
        self.assertFalse(is_exact_duplicate(None, {})[0])
        self.assertFalse(is_url_duplicate({}, None)[0])
        self.assertFalse(is_semantic_duplicate(None, {})[0])

        # Exact core fields match
        r1 = {"property_id": "P1", "property_type": "flat", "location": "London", "price": 100, "bedrooms": 1, "bathrooms": 1, "listing_url": "https://a.com"}
        r2 = {"property_id": "P2", "property_type": "flat", "location": "London", "price": 100, "bedrooms": 1, "bathrooms": 1, "listing_url": "https://a.com"}
        self.assertTrue(is_exact_duplicate(r1, r2)[0])

        # Semantic price tolerance branch (> 5% difference is NOT duplicate)
        r3 = r1.copy()
        r3["property_id"] = "P3"
        r3["price"] = 200 # 100% price difference
        self.assertFalse(is_semantic_duplicate(r1, r3, price_tolerance_pct=0.05)[0])

        # identify_duplicates TypeError branch
        with self.assertRaises(TypeError):
            identify_duplicates("not_a_list")

        # Report for empty dataset vs dataset with duplicates
        rep_empty = generate_duplicate_report([])
        self.assertIn("No duplicate property records were detected", rep_empty)

        rep_dup = generate_duplicate_report([r1, r2])
        self.assertIn("IDENTIFIED DUPLICATE RECORDS:", rep_dup)

        # deduplicate_dataset helper
        deduped = deduplicate_dataset([r1, r2], strategy="keep_first")
        self.assertEqual(len(deduped), 1)

    def test_white_box_compare_property_records_branches(self):
        from src.data_cleaning import compare_property_records, format_comparison_table
        # None and non-dict branches
        self.assertFalse(compare_property_records(None, {})["is_match"])
        self.assertFalse(compare_property_records({}, None)["is_match"])

        # Identical records branch
        r1 = {
            "property_id": "P_COMP_1",
            "property_type": "flat",
            "location": "A Very Long Location Description Exceeding Twenty Six Characters For Truncation",
            "price": "£250,000",
            "bedrooms": 2,
            "bathrooms": 1,
            "listing_url": "https://example.com/very/long/listing/url/path/exceeding/twenty/six/characters"
        }
        res_ident = compare_property_records(r1, r1.copy())
        self.assertTrue(res_ident["are_identical"])
        self.assertTrue(res_ident["is_match"])
        self.assertEqual(res_ident["similarity_score"], 1.0)

        # Price unparseable branch
        r_bad_price = {**r1, "property_id": "P_COMP_2", "price": "unparseable_price_string"}
        res_bad_p = compare_property_records(r1, r_bad_price)
        self.assertEqual(res_bad_p["price_difference"]["amount"], 0.0)

        # Truncation and table formatting branch
        tbl = format_comparison_table(r1, r_bad_price)
        self.assertIn("SIDE-BY-SIDE PROPERTY RECORD COMPARISON", tbl)
        self.assertIn("...", tbl) # Truncation executed

    def test_white_box_student_accommodation_branches(self):
        from src.data_cleaning import (
            validate_student_accommodation_factors,
            validate_student_property_record,
            format_student_property_details,
            create_student_property_record,
            load_student_accommodations
        )

        # 1. validate_student_accommodation_factors None/non-dict branch
        self.assertFalse(validate_student_accommodation_factors(None)[0])
        self.assertFalse(validate_student_accommodation_factors(["not_a_dict"])[0])

        # 2. Location branches
        r_loc_empty = create_student_property_record(student_preferred_location="   ")
        self.assertFalse(validate_student_accommodation_factors(r_loc_empty)[0])

        # 3. Affordable rent branches: non-numeric, zero, monthly pcm, moderate, premium
        r_rent_non_num = create_student_property_record(affordable_rent="Free accommodation")
        self.assertFalse(validate_student_accommodation_factors(r_rent_non_num)[0])

        r_rent_zero = create_student_property_record(affordable_rent="£0/week")
        self.assertFalse(validate_student_accommodation_factors(r_rent_zero)[0])

        r_rent_monthly = create_student_property_record(affordable_rent="£850 pcm monthly")
        ok, _, ev_monthly = validate_student_accommodation_factors(r_rent_monthly)
        self.assertTrue(ok)
        self.assertEqual(ev_monthly["monthly_rent"], 850.0)

        r_rent_mod = create_student_property_record(affordable_rent="£200/week")
        ok, _, ev_mod = validate_student_accommodation_factors(r_rent_mod)
        self.assertTrue(ok)
        self.assertIn("Moderate Affordability", ev_mod["affordability_tier"])

        r_rent_prem = create_student_property_record(affordable_rent="£320/week")
        ok, _, ev_prem = validate_student_accommodation_factors(r_rent_prem)
        self.assertTrue(ok)
        self.assertIn("Premium Accommodation", ev_prem["affordability_tier"])

        # 4. Bills branches: partial bills, bills excluded
        r_bills_partial = create_student_property_record(bills_included="Only water is included")
        ok, _, ev_b_part = validate_student_accommodation_factors(r_bills_partial)
        self.assertTrue(ok)
        self.assertIn("Partially Included", ev_b_part["bills_status"])

        r_bills_excl = create_student_property_record(bills_included="No bills included, tenant pays all")
        ok, _, ev_b_excl = validate_student_accommodation_factors(r_bills_excl)
        self.assertTrue(ok)
        self.assertEqual(ev_b_excl["bills_status"], "Bills Excluded")

        # 5. Room type branches: unknown type, studio, private room, shared room
        r_room_bad = create_student_property_record(room_type="penthouse_suite_invalid")
        self.assertFalse(validate_student_accommodation_factors(r_room_bad)[0])

        r_room_studio = create_student_property_record(room_type="studio")
        ok, _, _ = validate_student_accommodation_factors(r_room_studio)
        self.assertTrue(ok)

        r_room_priv = create_student_property_record(room_type="private_room")
        ok, _, _ = validate_student_accommodation_factors(r_room_priv)
        self.assertTrue(ok)

        # 6. Safety & Facilities: facilities as list, basic security
        r_fac_list = create_student_property_record(
            facilities=["On-site laundry", "Gym", "Study room", "Communal kitchen"],
            safety_security="CCTV and secure entry"
        )
        ok, _, _ = validate_student_accommodation_factors(r_fac_list)
        self.assertTrue(ok)

        # 7. Reviews branches: 10-point scale (/10)
        r_rev_10 = create_student_property_record(reviews_ratings="9.0 / 10 rating from students")
        ok, _, ev_rev = validate_student_accommodation_factors(r_rev_10)
        self.assertTrue(ok)
        self.assertEqual(ev_rev["factor_breakdown"]["reviews_ratings"]["rating_score"], 4.5)

        # 8. validate_student_property_record None branch
        self.assertFalse(validate_student_property_record(None)[0])

        # 9. format_student_property_details non-dict branch and evaluation=None branch
        self.assertIn("Error", format_student_property_details("not_dict"))
        full_prop = create_student_property_record(property_id="PROP_WB_01")
        fmt_res = format_student_property_details(full_prop)
        self.assertIn("PROP_WB_01", fmt_res)

        # 10. load_student_accommodations non-existent path
        loaded_empty = load_student_accommodations(json_path="non_existent_file_path_12345.json")
        self.assertEqual(loaded_empty, [])


if __name__ == "__main__":
    unittest.main()
