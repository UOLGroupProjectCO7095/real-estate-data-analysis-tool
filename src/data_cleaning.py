"""
Data Cleaning and Validation Module for Real Estate Properties.

This module provides validation functions to ensure property records contain
all required fields and conform to data quality, domain, and type constraints.
"""

from typing import Any, Dict, List, Optional, Tuple
import re

# Canonical required fields based on project schema in Data/properties.csv
REQUIRED_PROPERTY_FIELDS: List[str] = [
    "property_id",
    "property_type",
    "location",
    "price",
    "bedrooms",
    "bathrooms",
    "listing_url"
]

# Standard allowed property types in real estate domain
ALLOWED_PROPERTY_TYPES: List[str] = [
    "apartment",
    "house",
    "condo",
    "townhouse",
    "villa",
    "studio",
    "duplex",
    "land"
]


def validate_required_fields(record: Any) -> Tuple[bool, List[str]]:
    """
    Checks that the record contains all required property fields and that none are None or empty.

    Parameters:
        record: Dictionary representing a property record.

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_missing_or_empty_fields)
    """
    if record is None:
        return False, ["RECORD_IS_NONE"]
    if not isinstance(record, dict):
        return False, ["RECORD_MUST_BE_DICT"]

    missing_or_empty: List[str] = []
    for field in REQUIRED_PROPERTY_FIELDS:
        if field not in record:
            missing_or_empty.append(field)
        else:
            val = record[field]
            if val is None:
                missing_or_empty.append(field)
            elif isinstance(val, str) and val.strip() == "":
                missing_or_empty.append(field)

    is_valid = len(missing_or_empty) == 0
    return is_valid, missing_or_empty


def validate_property_id(property_id: Any) -> Tuple[bool, str]:
    """
    Validates that property_id is non-empty string or positive integer.
    """
    if property_id is None:
        return False, "property_id cannot be None"
    if isinstance(property_id, int):
        if property_id <= 0:
            return False, "property_id as int must be positive"
        return True, ""
    if isinstance(property_id, str):
        cleaned = property_id.strip()
        if not cleaned:
            return False, "property_id string cannot be empty"
        return True, ""
    return False, "property_id must be string or integer"


def validate_property_type(property_type: Any) -> Tuple[bool, str]:
    """
    Validates property type against accepted real estate categories.
    """
    if property_type is None:
        return False, "property_type cannot be None"
    if not isinstance(property_type, str):
        return False, "property_type must be a string"
    cleaned = property_type.strip().lower()
    if cleaned not in ALLOWED_PROPERTY_TYPES:
        return False, f"Invalid property_type '{property_type}'. Allowed: {ALLOWED_PROPERTY_TYPES}"
    return True, ""


def validate_price(price: Any) -> Tuple[bool, str]:
    """
    Validates that price is a positive number (int or float) within realistic real estate bounds.
    """
    if price is None:
        return False, "price cannot be None"
    if isinstance(price, bool):
        return False, "price cannot be a boolean"
    if isinstance(price, (int, float)):
        val = float(price)
        if val <= 0.0:
            return False, "price must be greater than zero"
        if val > 1_000_000_000.0:
            return False, "price exceeds maximum realistic threshold (1 billion)"
        return True, ""
    if isinstance(price, str):
        cleaned = price.strip().replace(",", "").replace("$", "").replace("£", "")
        try:
            val = float(cleaned)
            if val <= 0.0:
                return False, "price must be greater than zero"
            if val > 1_000_000_000.0:
                return False, "price exceeds maximum realistic threshold (1 billion)"
            return True, ""
        except ValueError:
            return False, "price string must be numeric"
    return False, "price must be a number or numeric string"


def validate_room_count(count: Any, room_name: str = "bedrooms") -> Tuple[bool, str]:
    """
    Validates room count (bedrooms / bathrooms). Must be non-negative number within realistic range (0 to 100).
    """
    if count is None:
        return False, f"{room_name} cannot be None"
    if isinstance(count, bool):
        return False, f"{room_name} cannot be a boolean"
    if isinstance(count, (int, float)):
        val = float(count)
        if val < 0.0:
            return False, f"{room_name} cannot be negative"
        if val > 100.0:
            return False, f"{room_name} exceeds reasonable limit (100)"
        return True, ""
    if isinstance(count, str):
        cleaned = count.strip()
        try:
            val = float(cleaned)
            if val < 0.0:
                return False, f"{room_name} cannot be negative"
            if val > 100.0:
                return False, f"{room_name} exceeds reasonable limit (100)"
            return True, ""
        except ValueError:
            return False, f"{room_name} string must be numeric"
    return False, f"{room_name} must be a number or numeric string"


def validate_url(url: Any) -> Tuple[bool, str]:
    """
    Validates that listing_url is a well-formed http/https URL string.
    """
    if url is None:
        return False, "listing_url cannot be None"
    if not isinstance(url, str):
        return False, "listing_url must be a string"
    cleaned = url.strip()
    if not cleaned:
        return False, "listing_url cannot be empty"
    # Basic URL pattern validation
    url_pattern = re.compile(
        r"^https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+(?:/.*)?$", re.IGNORECASE
    )
    if not url_pattern.match(cleaned):
        return False, "listing_url must be a valid http or https URL"
    return True, ""


def validate_property_record(record: Any) -> Tuple[bool, List[str]]:
    """
    Performs comprehensive validation of a single property record:
    1. Checks presence of all required fields.
    2. Performs domain, boundary, and type validation on individual fields.

    Parameters:
        record: Dictionary containing property data.

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_error_messages)
    """
    errors: List[str] = []

    # Step 1: Required fields existence check
    req_valid, req_errors = validate_required_fields(record)
    if not req_valid:
        for err in req_errors:
            errors.append(f"Missing or empty required field: {err}")
        return False, errors

    # Step 2: Field level validations
    id_ok, id_msg = validate_property_id(record.get("property_id"))
    if not id_ok:
        errors.append(f"Invalid 'property_id': {id_msg}")

    type_ok, type_msg = validate_property_type(record.get("property_type"))
    if not type_ok:
        errors.append(f"Invalid 'property_type': {type_msg}")

    loc = record.get("location")
    if loc is None or not isinstance(loc, str) or not loc.strip():
        errors.append("Invalid 'location': location must be a non-empty string")

    price_ok, price_msg = validate_price(record.get("price"))
    if not price_ok:
        errors.append(f"Invalid 'price': {price_msg}")

    bed_ok, bed_msg = validate_room_count(record.get("bedrooms"), "bedrooms")
    if not bed_ok:
        errors.append(f"Invalid 'bedrooms': {bed_msg}")

    bath_ok, bath_msg = validate_room_count(record.get("bathrooms"), "bathrooms")
    if not bath_ok:
        errors.append(f"Invalid 'bathrooms': {bath_msg}")

    url_ok, url_msg = validate_url(record.get("listing_url"))
    if not url_ok:
        errors.append(f"Invalid 'listing_url': {url_msg}")

    return len(errors) == 0, errors


def filter_valid_records(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Processes a list of property records, separating them into valid and rejected records.

    Parameters:
        records: List of property dictionaries.

    Returns:
        Tuple[List[dict], List[dict]]: (valid_records, rejected_records_with_reasons)
    """
    if not isinstance(records, list):
        raise TypeError("records must be a list")

    valid_records: List[Dict[str, Any]] = []
    rejected_records: List[Dict[str, Any]] = []

    for idx, rec in enumerate(records):
        is_valid, errors = validate_property_record(rec)
        if is_valid:
            valid_records.append(rec)
        else:
            rejected_records.append({
                "index": idx,
                "record": rec,
                "errors": errors
            })

    return valid_records, rejected_records
