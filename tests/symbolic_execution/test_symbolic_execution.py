"""
Research Component: Symbolic Execution Analysis & Test Suite.

Technique: Symbolic Execution (White-Box Research Component).
Target Functions: validate_property_id, validate_price, validate_room_count, validate_required_fields

--------------------------------------------------------------------------------
SYMBOLIC EXECUTION TREE & PATH CONDITIONS:
--------------------------------------------------------------------------------

Function 1: validate_price(price)
Let alpha represent symbolic price:

Tree Nodes & Path Conditions (PC):
Root: validate_price(alpha)
 |-- [Branch 1: alpha is None]
 |     Path Condition: PC1 = (alpha == None)
 |     Output: (False, "price cannot be None")
 |
 |-- [Branch 2: alpha is bool]
 |     Path Condition: PC2 = (type(alpha) == bool)
 |     Output: (False, "price cannot be a boolean")
 |
 |-- [Branch 3: type(alpha) in (int, float)]
 |    |-- [Branch 3a: float(alpha) <= 0.0]
 |    |     Path Condition: PC3a = (type(alpha) in (int, float) and alpha <= 0.0)
 |    |     Output: (False, "price must be greater than zero")
 |    |
 |    |-- [Branch 3b: float(alpha) > 1,000,000,000.0]
 |    |     Path Condition: PC3b = (type(alpha) in (int, float) and alpha > 1_000_000_000.0)
 |    |     Output: (False, "price exceeds maximum realistic threshold (1 billion)")
 |    |
 |    |-- [Branch 3c: 0.0 < float(alpha) <= 1,000,000,000.0]
 |          Path Condition: PC3c = (type(alpha) in (int, float) and 0.0 < alpha <= 1_000_000_000.0)
 |          Output: (True, "")
 |
 |-- [Branch 4: type(alpha) == str]
 |    |-- Clean alpha: remove ',', '$', '£', strip whitespace
 |    |-- Try parse float:
 |         |-- [Branch 4a: ValueError on float conversion]
 |         |     Path Condition: PC4a = (type(alpha) == str and not is_convertible_to_float(cleaned))
 |         |     Output: (False, "price string must be numeric")
 |         |
 |         |-- [Branch 4b: float(cleaned) <= 0.0]
 |         |     Path Condition: PC4b = (type(alpha) == str and is_convertible_to_float(cleaned) and float(cleaned) <= 0.0)
 |         |     Output: (False, "price must be greater than zero")
 |         |
 |         |-- [Branch 4c: float(cleaned) > 1_000_000_000.0]
 |         |     Path Condition: PC4c = (type(alpha) == str and is_convertible_to_float(cleaned) and float(cleaned) > 1_000_000_000.0)
 |         |     Output: (False, "price exceeds maximum realistic threshold (1 billion)")
 |         |
 |         |-- [Branch 4d: 0.0 < float(cleaned) <= 1_000_000_000.0]
 |               Path Condition: PC4d = (type(alpha) == str and is_convertible_to_float(cleaned) and 0.0 < float(cleaned) <= 1_000_000_000.0)
 |               Output: (True, "")
 |
 |-- [Branch 5: type(alpha) not in (NoneType, bool, int, float, str)]
       Path Condition: PC5 = (type(alpha) not in {None, bool, int, float, str})
       Output: (False, "price must be a number or numeric string")
"""

import unittest
from src.data_cleaning import (
    validate_price,
    validate_property_id,
    validate_room_count,
    validate_required_fields,
    REQUIRED_PROPERTY_FIELDS,
)


class TestSymbolicExecution(unittest.TestCase):
    """
    Test cases derived directly from the symbolic execution tree solving each path condition.
    """

    # --- Symbolic Execution Tests for validate_price ---
    def test_symbolic_price_pc1(self):
        # PC1: alpha == None
        self.assertEqual(validate_price(None), (False, "price cannot be None"))

    def test_symbolic_price_pc2(self):
        # PC2: type(alpha) == bool
        self.assertEqual(validate_price(True), (False, "price cannot be a boolean"))

    def test_symbolic_price_pc3a(self):
        # PC3a: numeric and alpha <= 0.0
        self.assertEqual(validate_price(0.0), (False, "price must be greater than zero"))
        self.assertEqual(validate_price(-50), (False, "price must be greater than zero"))

    def test_symbolic_price_pc3b(self):
        # PC3b: numeric and alpha > 1,000,000,000.0
        self.assertEqual(
            validate_price(1_000_000_001.0),
            (False, "price exceeds maximum realistic threshold (1 billion)")
        )

    def test_symbolic_price_pc3c(self):
        # PC3c: numeric and 0.0 < alpha <= 1,000,000,000.0
        self.assertEqual(validate_price(250000.0), (True, ""))

    def test_symbolic_price_pc4a(self):
        # PC4a: string not convertible to float
        self.assertEqual(validate_price("not_numeric"), (False, "price string must be numeric"))

    def test_symbolic_price_pc4b(self):
        # PC4b: string convertible to float <= 0.0
        self.assertEqual(validate_price("0"), (False, "price must be greater than zero"))
        self.assertEqual(validate_price("-$100"), (False, "price must be greater than zero"))

    def test_symbolic_price_pc4c(self):
        # PC4c: string convertible to float > 1B
        self.assertEqual(
            validate_price("£1,500,000,000"),
            (False, "price exceeds maximum realistic threshold (1 billion)")
        )

    def test_symbolic_price_pc4d(self):
        # PC4d: string convertible to float in range (0, 1B]
        self.assertEqual(validate_price("$500,000.00"), (True, ""))

    def test_symbolic_price_pc5(self):
        # PC5: unsupported type
        self.assertEqual(validate_price([1000]), (False, "price must be a number or numeric string"))

    # --- Symbolic Execution Tests for validate_property_id ---
    def test_symbolic_id_all_path_conditions(self):
        # PC1: id is None
        self.assertEqual(validate_property_id(None), (False, "property_id cannot be None"))
        # PC2: int <= 0
        self.assertEqual(validate_property_id(0), (False, "property_id as int must be positive"))
        # PC3: int > 0
        self.assertEqual(validate_property_id(101), (True, ""))
        # PC4: string empty or whitespace
        self.assertEqual(validate_property_id(""), (False, "property_id string cannot be empty"))
        self.assertEqual(validate_property_id("   "), (False, "property_id string cannot be empty"))
        # PC5: string non-empty
        self.assertEqual(validate_property_id("ID_999"), (True, ""))
        # PC6: other types
        self.assertEqual(validate_property_id(3.14), (False, "property_id must be string or integer"))

    # --- Symbolic Execution Tests for Cross-Field Validation Paths ---
    def test_symbolic_cross_field_path_conditions(self):
        from src.data_cleaning import validate_cross_field_consistency
        # PC_CF1: ptype == 'studio' and bedrooms > 1 -> Inconsistent
        rec_cf1 = {"property_type": "studio", "bedrooms": 3, "bathrooms": 1}
        ok1, err1 = validate_cross_field_consistency(rec_cf1)
        self.assertFalse(ok1)
        self.assertIn("studio' cannot have 3 bedrooms", err1[0])

        # PC_CF2: ptype == 'studio' and bedrooms <= 1 -> Consistent
        rec_cf2 = {"property_type": "studio", "bedrooms": 0, "bathrooms": 1}
        ok2, err2 = validate_cross_field_consistency(rec_cf2)
        self.assertTrue(ok2)

        # PC_CF3: ptype == 'land' and (bedrooms > 0 or bathrooms > 0) -> Inconsistent
        rec_cf3 = {"property_type": "land", "bedrooms": 1, "bathrooms": 0}
        ok3, err3 = validate_cross_field_consistency(rec_cf3)
        self.assertFalse(ok3)

        # PC_CF4: ptype == 'land' and bedrooms == 0 and bathrooms == 0 -> Consistent
        rec_cf4 = {"property_type": "land", "bedrooms": 0, "bathrooms": 0}
        ok4, err4 = validate_cross_field_consistency(rec_cf4)
        self.assertTrue(ok4)

    # --- Symbolic Execution Tests for Duplicate Engine Paths ---
    def test_symbolic_duplicate_decision_tree_paths(self):
        from src.data_cleaning import check_duplicate_pair
        r_base = {
            "property_id": "P_SYM_1",
            "property_type": "apartment",
            "location": "Cambridge",
            "price": 300000,
            "bedrooms": 2,
            "bathrooms": 1,
            "listing_url": "https://symbolic.org/p1"
        }

        # PC_DUP1: id1 == id2 -> Exact Match
        r_pc1 = r_base.copy()
        r_pc1["location"] = "Leeds"
        is_dup1, reason1 = check_duplicate_pair(r_base, r_pc1)
        self.assertTrue(is_dup1)
        self.assertIn("Exact property_id match", reason1)

        # PC_DUP2: id1 != id2 and canon(url1) == canon(url2) -> URL Duplicate
        r_pc2 = {
            "property_id": "P_SYM_2",
            "property_type": "house",
            "location": "Manchester",
            "price": 999999,
            "bedrooms": 5,
            "bathrooms": 4,
            "listing_url": "https://symbolic.org/p1?utm_campaign=test"
        }
        is_dup2, reason2 = check_duplicate_pair(r_base, r_pc2)
        self.assertTrue(is_dup2)
        self.assertIn("Duplicate canonical listing URL", reason2)

        # PC_DUP3: id1 != id2 and canon(url1) != canon(url2) and semantic(r1, r2) -> Semantic Duplicate
        r_pc3 = {
            "property_id": "P_SYM_3",
            "property_type": "apartment",
            "location": "Cambridge",
            "price": 300000,
            "bedrooms": 2,
            "bathrooms": 1,
            "listing_url": "https://symbolic.org/p3"
        }
        is_dup3, reason3 = check_duplicate_pair(r_base, r_pc3)
        self.assertTrue(is_dup3)
        self.assertIn("Semantic property duplicate", reason3)

        # PC_DUP4: id1 != id2 and canon(url1) != canon(url2) and not semantic(r1, r2) -> Unique
        r_pc4 = {
            "property_id": "P_SYM_4",
            "property_type": "detached",
            "location": "Cardiff",
            "price": 500000,
            "bedrooms": 4,
            "bathrooms": 3,
            "listing_url": "https://symbolic.org/p4"
        }
        is_dup4, _ = check_duplicate_pair(r_base, r_pc4)
        self.assertFalse(is_dup4)


if __name__ == "__main__":
    unittest.main()
