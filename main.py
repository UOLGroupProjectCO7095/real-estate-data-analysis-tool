"""
Main Entry Point - Real Estate Data Collection and Analysis Tool.
Interactive Text-Based Console Application.
Compatible with standard Python & PyCharm.
"""

import os
import sys
import csv
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


def handle_simulate_and_merge_member_sources():
    """
    Option to test open multi-source merging:
    Ingests live/mock batches from Member 1 (Data Collection) and Member 4 (Properties Domain),
    merges them into a unified stream, validates every record, and displays the processed results.
    """
    print("\n" + "=" * 65)
    print("  SIMULATE & TEST OPEN MERGE FROM MEMBER 1 & MEMBER 4  ")
    print("=" * 65)
    print("[*] Contacting Member 1 (Data Collection)... Generating batch of 4 records.")
    from src.data_collection import generate_mock_collected_properties
    from src.property_search import generate_mock_member4_properties, Property
    from src.data_cleaning import merge_and_process_member_sources

    m1_records = generate_mock_collected_properties(count=4)
    print(f"    ✓ Member 1 produced {len(m1_records)} records.")

    print("[*] Contacting Member 4 (Properties Domain)... Generating batch of 4 Property objects.")
    m4_entities = generate_mock_member4_properties(count=4)
    print(f"    ✓ Member 4 produced {len(m4_entities)} domain entities.")

    print("[*] Merging Member 1 & Member 4 streams into Data Processing Pipeline...")
    valid_merged, rejected_merged = merge_and_process_member_sources(
        collection_records=m1_records,
        property_entities=m4_entities
    )

    display_records(valid_merged, f"Merged & Validated Properties ({len(valid_merged)} records)")

    if rejected_merged:
        print(f"\n--- Rejected During Merge ({len(rejected_merged)} records) ---")
        for rej in rejected_merged:
            print(f"  x ID: {rej['record'].get('property_id')} - Errors: {rej['errors']}")

    save_choice = input("\nWould you like to persist these merged valid records to Data/properties.csv? (y/n) [default: y]: ").strip().lower()
    if save_choice != "n":
        try:
            with open(DATA_FILE_PATH, mode="a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                for r in valid_merged:
                    writer.writerow([
                        r["property_id"],
                        r["property_type"],
                        r["location"],
                        r["price"],
                        r["bedrooms"],
                        r["bathrooms"],
                        r["listing_url"]
                    ])
            print(f"[SUCCESS] Appended {len(valid_merged)} merged records to {DATA_FILE_PATH}!")
        except Exception as e:
            print(f"[!] Error saving to file: {e}")
    print("=" * 65)


def handle_manual_validation():
    """Reads listing URL, automatically extracts real property data, validates it, and saves it."""
    print("\n" + "=" * 65)
    print("      AUTOMATED PROPERTY URL INGESTION & VALIDATION      ")
    print("=" * 65)
    url_input = input("Enter Listing URL: ").strip()

    if not url_input:
        print("[!] No URL entered. Aborting.")
        return

    from src.data_cleaning import extract_details_from_url
    print("\n[*] Processing URL and reading real listing data...")
    prop = extract_details_from_url(url_input)

    print("\n" + "-" * 65)
    print("                EXTRACTED REAL PROPERTY DATA                ")
    print("-" * 65)
    print(f"  • Property ID           : {prop.get('property_id')}")
    if prop.get('property_name'):
        print(f"  • Property Name         : {prop.get('property_name')}")
    print(f"  • Extracted Property Type: {prop.get('property_type')}")
    print(f"  • Extracted Location     : {prop.get('location')}")
    print(f"  • Extracted Price        : £{prop.get('price')}")
    print(f"  • Default Bedrooms       : {prop.get('bedrooms')}")
    print(f"  • Default Bathrooms      : {prop.get('bathrooms')}")
    
    print("\n  • Room Types:")
    for rt in prop.get('room_types', []):
        print(f"      - {rt}")

    if prop.get('room_breakdown'):
        print("\n  • Room Breakdown Summary:")
        for k, v in prop.get('room_breakdown', {}).items():
            print(f"      * {k}: {v}")

    print("\n  • Amenities:")
    for amen in prop.get('amenities', []):
        print(f"      ✓ {amen}")

    print("-" * 65)

    # Automatically validate the record
    print("[*] Validating record against Acceptance Criteria...")
    is_valid, errors = validate_property_record(prop)

    if is_valid:
        print("[PASSED] Record is 100% VALID and reliable for processing!")

        # Automatically persist to Data/properties.csv
        try:
            with open(DATA_FILE_PATH, mode="a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    prop["property_id"],
                    prop["property_type"],
                    prop["location"],
                    prop["price"],
                    prop["bedrooms"],
                    prop["bathrooms"],
                    prop["listing_url"]
                ])
            print(f"[SAVED] Record automatically appended to {DATA_FILE_PATH}")
        except Exception as e:
            print(f"[!] Warning: Could not write to storage: {e}")
    else:
        print("[REJECTED] The record has invalid or missing fields:")
        for err in errors:
            print(f"    x {err}")

    print("=" * 65)


def handle_run_all_tests():
    """Runs all test suites and displays software quality metrics."""
    import run_tests_with_coverage
    run_tests_with_coverage.main()


def main():
    while True:
        print("\n" + "=" * 65)
        print("  REAL ESTATE DATA ANALYSIS TOOL - DATA PROCESSING PIPELINE  ")
        print("=" * 65)
        print("1. Process & Validate Stored Properties (Data/properties.csv)")
        print("2. Merge & Process Member 1 & Member 4 Sources (Open Simulation)")
        print("3. Automated Property URL Ingestion & Real Data Validation")
        print("4. Run Test Suites & Check Coverage (CO7095 QA Standard)")
        print("5. Exit")
        print("=" * 65)

        choice = input("Select an option (1-5): ").strip()
        if choice == "1":
            handle_process_collected_data()
        elif choice == "2":
            handle_simulate_and_merge_member_sources()
        elif choice == "3":
            handle_manual_validation()
        elif choice == "4":
            handle_run_all_tests()
        elif choice == "5":
            print("\nExiting application. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please enter 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()
