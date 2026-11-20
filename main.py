"""
Main Entry Point - Real Estate Data Collection and Analysis Tool.
Interactive Text-Based Console Application.
Compatible with standard Python & PyCharm.
"""

import os
import sys
from typing import List, Dict, Any

from src.data_cleaning import (
    validate_property_record,
    filter_valid_records,
    process_pipeline_records,
)
from src.data_collection import fetch_raw_collected_data
from src.property_search import Property

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "Data", "properties.csv")


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


def handle_process_collected_data():
    """
    Openly connects to Data Collection (Member 1) and Properties (Member 4).
    As soon as data is collected or created, this seamlessly consumes and validates it.
    """
    print("\n[+] Triggering Open Data Collection Ingestion Pipeline...")
    # Calls the open connector which automatically loads from Data/properties.csv or live collection
    raw_records = fetch_raw_collected_data()
    print(f"[*] Ingested {len(raw_records)} raw records from collection source.")

    valid_recs, rejected_recs = process_pipeline_records(raw_records)

    display_records(valid_recs, "Processed & Validated Reliable Property Records")

    if rejected_recs:
        print(f"\n--- Identified Invalid Records ({len(rejected_recs)} records) ---")
        for rej in rejected_recs:
            rec = rej["record"]
            print(f"Index {rej['index']} (ID: {rec.get('property_id', 'UNKNOWN')}):")
            for err in rej["errors"]:
                print(f"    x {err}")


def handle_manual_validation():
    """Validates a single user-entered property record against all 4 acceptance criteria."""
    print("\n--- Manual Property Validation ---")
    prop = {}
    prop["property_id"] = input("Enter Property ID (e.g., PROP101): ").strip()
    prop["property_type"] = input("Enter Property Type (apartment/house/condo/villa/studio/townhouse/duplex/land): ").strip()
    prop["location"] = input("Enter Location: ").strip()
    prop["price"] = input("Enter Price: ").strip()
    prop["bedrooms"] = input("Enter Bedrooms Count: ").strip()
    prop["bathrooms"] = input("Enter Bathrooms Count: ").strip()
    prop["listing_url"] = input("Enter Listing URL: ").strip()

    is_valid, errors = validate_property_record(prop)
    print("\n" + "=" * 55)
    if is_valid:
        print("[PASSED] Record meets all criteria and is validated for analysis.")
    else:
        print("[REJECTED] The record has invalid or missing fields:")
        for err in errors:
            print(f"  - {err}")
    print("=" * 55)


def handle_run_all_tests():
    """Runs all test suites and displays software quality metrics."""
    import run_tests_with_coverage
    run_tests_with_coverage.main()


def main():
    while True:
        print("\n" + "=" * 65)
        print("  REAL ESTATE DATA ANALYSIS TOOL - DATA PROCESSING PIPELINE  ")
        print("=" * 65)
        print("1. Process & Validate Collected Properties (Open Ingestion Pipeline)")
        print("2. Validate a Single Property Record Manually")
        print("3. Run Test Suites & Check Coverage (CO7095 QA Standard)")
        print("4. Exit")
        print("=" * 65)

        choice = input("Select an option (1-4): ").strip()
        if choice == "1":
            handle_process_collected_data()
        elif choice == "2":
            handle_manual_validation()
        elif choice == "3":
            handle_run_all_tests()
        elif choice == "4":
            print("\nExiting application. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
