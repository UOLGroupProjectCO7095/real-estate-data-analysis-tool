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
    """Validates a property record, starting with listing URL to auto-extract details or fill manually."""
    print("\n--- Property Validation via Listing URL ---")
    url_input = input("Enter Listing URL: ").strip()

    # Step 1: Process URL and extract details
    extracted = {}
    if url_input:
        from src.data_cleaning import extract_details_from_url
        extracted = extract_details_from_url(url_input)
        print("\n[+] Processed URL and Extracted Property Details:")
        print(f"  - Extracted Property ID   : {extracted.get('property_id')}")
        print(f"  - Extracted Property Type : {extracted.get('property_type')}")
        print(f"  - Extracted Location      : {extracted.get('location')}")
        print(f"  - Extracted Price         : {extracted.get('price')}")
        print(f"  - Default Bedrooms        : {extracted.get('bedrooms')}")
        print(f"  - Default Bathrooms       : {extracted.get('bathrooms')}")
        print(f"  - Listing URL             : {url_input}")
        print("\nPress [Enter] to keep extracted values, or type a new value to customize:")

    prop = {}
    prop["listing_url"] = url_input

    def prompt_field(label: str, key: str, default_val: str) -> str:
        prompt_str = f"Enter {label}" + (f" [{default_val}]" if default_val else "") + ": "
        val = input(prompt_str).strip()
        return val if val else default_val

    prop["property_id"] = prompt_field("Property ID", "property_id", extracted.get("property_id", "PROP101"))
    prop["property_type"] = prompt_field("Property Type (apartment/house/condo/villa/studio/townhouse/duplex/land/ensuite)", "property_type", extracted.get("property_type", "apartment"))
    prop["location"] = prompt_field("Location", "location", extracted.get("location", "London"))
    prop["price"] = prompt_field("Price", "price", str(extracted.get("price", "250000")))
    prop["bedrooms"] = prompt_field("Bedrooms Count", "bedrooms", str(extracted.get("bedrooms", "1")))
    prop["bathrooms"] = prompt_field("Bathrooms Count", "bathrooms", str(extracted.get("bathrooms", "1")))

    is_valid, errors = validate_property_record(prop)
    print("\n" + "=" * 60)
    if is_valid:
        print("[PASSED] Record meets all criteria and is validated for analysis!")
        print(f"Summary: ID={prop['property_id']}, Type={prop['property_type']}, Location={prop['location']}, Price={prop['price']}, Beds={prop['bedrooms']}, Baths={prop['bathrooms']}")
    else:
        print("[REJECTED] The record has invalid or missing fields:")
        for err in errors:
            print(f"  - {err}")
    print("=" * 60)


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
