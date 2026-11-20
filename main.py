"""
Main Entry Point - Real Estate Data Collection and Analysis Tool.
Interactive Text-Based Console Application.
"""

import os
import sys
import csv
from typing import List, Dict, Any

from src.data_cleaning import (
    validate_property_record,
    filter_valid_records,
    REQUIRED_PROPERTY_FIELDS,
)


DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "Data", "properties.csv")


def load_properties_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """Loads property records from a CSV file."""
    if not os.path.exists(file_path):
        print(f"[!] Warning: Data file '{file_path}' not found.")
        return []

    records = []
    with open(file_path, mode="r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append(dict(row))
    return records


def display_records(records: List[Dict[str, Any]], title: str):
    """Displays a list of records in a formatted table."""
    print(f"\n--- {title} ({len(records)} records) ---")
    if not records:
        print("No records to display.")
        return

    header = f"{'ID':<12} | {'Type':<12} | {'Location':<20} | {'Price':<12} | {'Beds':<5} | {'Baths':<5}"
    print(header)
    print("-" * len(header))
    for r in records:
        print(
            f"{str(r.get('property_id', '')):<12} | "
            f"{str(r.get('property_type', '')):<12} | "
            f"{str(r.get('location', '')):<20} | "
            f"{str(r.get('price', '')):<12} | "
            f"{str(r.get('bedrooms', '')):<5} | "
            f"{str(r.get('bathrooms', '')):<5}"
        )


def validate_single_property_interactive():
    """Prompts user to input a single property record and validates it."""
    print("\n--- Enter Property Details for Validation ---")
    prop = {}
    prop["property_id"] = input("Enter Property ID (e.g., PROP2001): ").strip()
    prop["property_type"] = input("Enter Property Type (apartment/house/condo/villa/studio/townhouse/duplex/land): ").strip()
    prop["location"] = input("Enter Location: ").strip()
    prop["price"] = input("Enter Price (e.g., 250000): ").strip()
    prop["bedrooms"] = input("Enter Bedrooms Count (e.g., 2): ").strip()
    prop["bathrooms"] = input("Enter Bathrooms Count (e.g., 1.5): ").strip()
    prop["listing_url"] = input("Enter Listing URL (e.g., https://properties.com/2001): ").strip()

    is_valid, errors = validate_property_record(prop)
    print("\n" + "=" * 50)
    if is_valid:
        print("[SUCCESS] Property Record is VALID and reliable for processing!")
    else:
        print("[REJECTED] Validation failed with errors:")
        for err in errors:
            print(f"  - {err}")
    print("=" * 50)


def validate_stored_properties():
    """Validates all property records stored in Data/properties.csv."""
    records = load_properties_from_csv(DATA_FILE_PATH)
    if not records:
        print("[!] No records loaded from storage.")
        return

    print(f"\nLoaded {len(records)} records from {DATA_FILE_PATH}.")
    valid_recs, rejected_recs = filter_valid_records(records)

    display_records(valid_recs, "Validated & Reliable Property Records")

    if rejected_recs:
        print(f"\n--- Rejected Records ({len(rejected_recs)} records) ---")
        for rej in rejected_recs:
            rec = rej["record"]
            print(f"Index {rej['index']} (ID: {rec.get('property_id', 'UNKNOWN')}):")
            for err in rej["errors"]:
                print(f"    x {err}")


def run_all_tests():
    """Runs all test suites with coverage directly from the text UI."""
    import run_tests_with_coverage
    run_tests_with_coverage.main()


def main():
    while True:
        print("\n" + "=" * 60)
        print("  REAL ESTATE DATA COLLECTION & ANALYSIS TOOL (CLI)  ")
        print("=" * 60)
        print("1. Validate All Stored Property Records (Data/properties.csv)")
        print("2. Validate a Single Property Record Manually")
        print("3. Run All Test Suites & Measure Coverage (CO7095 QA)")
        print("4. Exit")
        print("=" * 60)

        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            validate_stored_properties()
        elif choice == "2":
            validate_single_property_interactive()
        elif choice == "3":
            run_all_tests()
        elif choice == "4":
            print("\nExiting application. Goodbye!")
            break
        else:
            print("[!] Invalid choice. Please select an option between 1 and 4.")


if __name__ == "__main__":
    main()
