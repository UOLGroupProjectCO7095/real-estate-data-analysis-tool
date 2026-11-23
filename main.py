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
    validate_student_property_record,
    format_student_property_details,
    create_student_property_record,
    save_student_property_record,
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


def handle_manual_student_property_entry():
    """
    Rich Manual Data Entry for Student Accommodation Records.
    Captures base property attributes and the 12 essential student factors:
      1. Student-preferred Location
      2. Affordable Rent
      3. Bills Included
      4. Room Type
      5. Safety and Security
      6. Facilities
      7. Transport Accessibility
      8. Contract Duration
      9. Flatmates
     10. Reviews and Ratings
     11. Deposit and Payment
     12. Availability

    Validates all attributes and immediately lists down all suitable details.
    """
    print("\n" + "=" * 75)
    print("      MANUAL STUDENT ACCOMMODATION DATA ENTRY & SUITABILITY LISTING      ")
    print("=" * 75)
    print("Enter the student property details below.")
    print("Tip: Press [Enter] without typing to accept the student-friendly default.\n")

    # Base property fields
    print("--- [Part A: Core Property Details] ---")
    prop_id = input("  • Property ID [default: PROP_STU_LEICESTER_01]: ").strip()
    if not prop_id:
        prop_id = "PROP_STU_LEICESTER_01"

    prop_type = input("  • Property Type (ensuite, studio, shared room, apartment) [default: ensuite]: ").strip()
    if not prop_type:
        prop_type = "ensuite"

    location = input("  • Location / City [default: Leicester City Centre (LE1)]: ").strip()
    if not location:
        location = "Leicester City Centre (LE1)"

    price_input = input("  • Rent Price (£/week) [default: 115]: ").strip()
    price = 115.0
    if price_input:
        try:
            price = float(price_input.replace("£", "").replace("$", "").replace(",", ""))
        except ValueError:
            price = 115.0

    beds_input = input("  • Number of Bedrooms [default: 1]: ").strip()
    bedrooms = int(beds_input) if beds_input.isdigit() else 1

    baths_input = input("  • Number of Bathrooms [default: 1]: ").strip()
    bathrooms = float(baths_input) if baths_input.replace(".", "").isdigit() else 1.0

    url = input("  • Listing URL [default: https://amberstudent.com/places/dover-street-apartments-leicester-2106166153995]: ").strip()
    if not url:
        url = "https://amberstudent.com/places/dover-street-apartments-leicester-2106166153995"

    # The 12 Student Factors
    print("\n--- [Part B: 12 Student-Centric Accommodation Factors] ---")

    print("\n1. Student-Preferred Location (Close to university, city centre, supermarkets, transport):")
    stu_loc = input("   Enter location details [default: Leicester LE1 (5 mins to University of Leicester & DMU, 3 mins to Tesco, 8 mins to City Centre)]: ").strip()
    if not stu_loc:
        stu_loc = "Leicester LE1 (5 mins to University of Leicester & DMU, 3 mins to Tesco, 8 mins to City Centre)"

    print("\n2. Affordable Rent (Weekly/monthly rent fitting student budget):")
    aff_rent = input(f"   Enter rent details [default: £{price:.0f}/week (£{price*52/12:.0f}/month) - Highly affordable within student budget (<= £160/wk)]: ").strip()
    if not aff_rent:
        aff_rent = f"£{price:.0f}/week (£{price*52/12:.0f}/month) - Highly affordable within student budget (<= £160/wk)"

    print("\n3. Bills Included (Electricity, water, heating, Wi-Fi included in rent):")
    bills = input("   Enter utilities included [default: All-Inclusive: Electricity, Water, Heating, and High-Speed Wi-Fi]: ").strip()
    if not bills:
        bills = "All-Inclusive: Electricity, Water, Heating, and High-Speed Wi-Fi"

    print("\n4. Room Type (En-suite, studio, shared room or private room):")
    room_t = input(f"   Enter room type [default: {prop_type} (Private modern bathroom, shared communal kitchen & lounge)]: ").strip()
    if not room_t:
        room_t = f"{prop_type} (Private modern bathroom, shared communal kitchen & lounge)"

    print("\n5. Safety and Security (CCTV, secure entry, reception, safe neighbourhood):")
    safety = input("   Enter security features [default: 24/7 CCTV surveillance, electronic key-fob secure entry, reception desk & safe student neighbourhood]: ").strip()
    if not safety:
        safety = "24/7 CCTV surveillance, electronic key-fob secure entry, reception desk & safe student neighbourhood"

    print("\n6. Facilities (Laundry, kitchen, gym, study rooms and common areas):")
    facilities = input("   Enter on-site facilities [default: On-site laundry, fully fitted communal kitchen, 24/7 fitness gym, quiet study rooms, social lounge]: ").strip()
    if not facilities:
        facilities = "On-site laundry, fully fitted communal kitchen, 24/7 fitness gym, quiet study rooms, social lounge"

    print("\n7. Transport Accessibility (Walking distance or convenient bus and train connections):")
    transport = input("   Enter transport links [default: Walking distance to campus (5 mins), 2 min to bus stop (routes 14, 48), 10 min to central train station]: ").strip()
    if not transport:
        transport = "Walking distance to campus (5 mins), 2 min to bus stop (routes 14, 48), 10 min to central train station"

    print("\n8. Contract Duration (Flexible contracts, semester stays or 12-month agreements):")
    contract = input("   Enter contract terms [default: Flexible contracts: 44-week academic term, 51-week full year, or single-semester stay]: ").strip()
    if not contract:
        contract = "Flexible contracts: 44-week academic term, 51-week full year, or single-semester stay"

    print("\n9. Flatmates (Single-gender, mixed-gender or shared accommodation preferences):")
    flatmates = input("   Enter flatmate preferences [default: Mixed-gender flats (single-gender female-only and male-only wings available on request)]: ").strip()
    if not flatmates:
        flatmates = "Mixed-gender flats (single-gender female-only and male-only wings available on request)"

    print("\n10. Reviews and Ratings (Previous students' experiences and accommodation reviews):")
    reviews = input("   Enter reviews & ratings [default: 4.8 / 5.0 (92 student reviews) - 'Excellent study atmosphere, fast Wi-Fi and friendly reception staff']: ").strip()
    if not reviews:
        reviews = "4.8 / 5.0 (92 student reviews) - 'Excellent study atmosphere, fast Wi-Fi and friendly reception staff'"

    print("\n11. Deposit and Payment (Deposit requirements, instalments and cancellation policies):")
    deposit = input("   Enter payment terms [default: £150 refundable deposit, 3 termly instalments linked to student loans, free cancellation before August]: ").strip()
    if not deposit:
        deposit = "£150 refundable deposit, 3 termly instalments linked to student loans, free cancellation before August"

    print("\n12. Availability (Whether the room is available for their intended move-in date):")
    availability = input("   Enter availability status [default: Available for September 2026 Academic Year (Early move-in available on request)]: ").strip()
    if not availability:
        availability = "Available for September 2026 Academic Year (Early move-in available on request)"

    # Build the record
    record = {
        "property_id": prop_id,
        "property_type": prop_type,
        "location": location,
        "price": price,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "listing_url": url,
        "student_preferred_location": stu_loc,
        "affordable_rent": aff_rent,
        "bills_included": bills,
        "room_type": room_t,
        "safety_security": safety,
        "facilities": facilities,
        "transport_accessibility": transport,
        "contract_duration": contract,
        "flatmates": flatmates,
        "reviews_ratings": reviews,
        "deposit_payment": deposit,
        "availability": availability
    }

    # Validate against both base criteria and the 12 student factors
    print("\n[*] Validating student record against Quality Assurance & Validation Standards...")
    is_valid, errors, evaluation = validate_student_property_record(record)

    if not is_valid:
        print("\n[REJECTED] The record failed validation:")
        for err in errors:
            print(f"    x {err}")
        return

    # List down all suitable details!
    print("\n[+] Record successfully validated! Listing down all suitable details:")
    report_text = format_student_property_details(record, evaluation)
    print("\n" + report_text)

    # Persistence prompt
    save_choice = input("\nWould you like to persist this record to Data/properties.csv and Data/student_accommodations.json? (y/n) [default: y]: ").strip().lower()
    if save_choice != "n":
        saved, msg = save_student_property_record(record)
        if saved:
            print(f"[SUCCESS] {msg}")
        else:
            print(f"[!] Warning: {msg}")

    print("=" * 75)


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

        if prop.get("student_preferred_location"):
            print("\n[+] Student Accommodation detected! Suitable details list down:")
            report_text = format_student_property_details(prop)
            print("\n" + report_text)

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


def handle_detect_and_handle_duplicates():
    """
    User Story 2: Identify Duplicate Property Records & Handle Them.
    Scans stored properties, detects exact ID, URL, and semantic duplicates,
    and applies configurable handling strategies (keep_first, keep_last, flag_only, merge, quarantine).
    """
    print("\n" + "=" * 65)
    print("      DUPLICATE PROPERTY DETECTION & HANDLING PIPELINE          ")
    print("=" * 65)
    from src.data_collection import fetch_raw_collected_data
    from src.data_cleaning import identify_duplicates, handle_duplicates, generate_duplicate_report

    records = fetch_raw_collected_data()
    print(f"[*] Ingested {len(records)} records from {DATA_FILE_PATH}")

    # Generate and display duplicate report
    report_text = generate_duplicate_report(records)
    print("\n" + report_text)

    analysis = identify_duplicates(records)
    if analysis["duplicate_count"] == 0:
        print("[✓] All records are unique. No deduplication required.")
        return

    print("\nSelect a Duplicate Handling Strategy:")
    print("  1. keep_first    : Retain primary/first occurrence and separate duplicates (Default)")
    print("  2. keep_last     : Retain latest occurrence and discard earlier duplicates")
    print("  3. flag_only     : Keep all records but mark duplicates with audit flags")
    print("  4. merge_records : Consolidate complementary fields into unified records")
    print("  5. remove_all    : Strict quarantine (remove any listing involved in duplication)")

    strat_choice = input("Enter choice (1-5) [default: 1]: ").strip()
    strat_map = {
        "1": "keep_first",
        "2": "keep_last",
        "3": "flag_only",
        "4": "merge_records",
        "5": "remove_all"
    }
    strategy = strat_map.get(strat_choice, "keep_first")
    print(f"\n[*] Applying handling strategy: '{strategy}'...")

    handled_records, duplicates = handle_duplicates(records, strategy=strategy)
    display_records(handled_records, f"Resulting Records after '{strategy}' ({len(handled_records)} records)")

    persist_choice = input(f"\nPersist clean deduplicated records ({len(handled_records)} rows) to Data/properties.csv? (y/n) [default: y]: ").strip().lower()
    if persist_choice != "n":
        try:
            with open(DATA_FILE_PATH, mode="w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["property_id", "property_type", "location", "price", "bedrooms", "bathrooms", "listing_url"])
                for r in handled_records:
                    writer.writerow([
                        r.get("property_id", ""),
                        r.get("property_type", ""),
                        r.get("location", ""),
                        r.get("price", ""),
                        r.get("bedrooms", ""),
                        r.get("bathrooms", ""),
                        r.get("listing_url", "")
                    ])
            print(f"[SUCCESS] Persisted {len(handled_records)} deduplicated records to {DATA_FILE_PATH}!")
        except Exception as e:
            print(f"[!] Error writing to file: {e}")

    print("=" * 65)


def handle_compare_two_properties():
    """
    Acceptance Criterion 1: The system should compare property records.
    Allows user to select two properties from storage to perform a field-by-field
    side-by-side comparison and view the similarity metrics.
    """
    print("\n" + "=" * 65)
    print("      SIDE-BY-SIDE PROPERTY RECORD COMPARISON TOOL              ")
    print("=" * 65)
    from src.data_collection import fetch_raw_collected_data
    from src.data_cleaning import compare_property_records, format_comparison_table

    records = fetch_raw_collected_data()
    if len(records) < 2:
        print("[!] Not enough stored records to compare. Need at least 2 records.")
        return

    print(f"Loaded {len(records)} records from {DATA_FILE_PATH}.\n")
    print("Available Property Records (First 10 shown):")
    for idx, r in enumerate(records[:10]):
        print(f"  [{idx}] ID: {r.get('property_id'):<16} | {r.get('property_type'):<10} | {r.get('location'):<20} | £{r.get('price')}")

    idx_a_str = input(f"\nSelect index for Record A [default: 0]: ").strip()
    idx_b_str = input(f"Select index for Record B [default: 1]: ").strip()

    try:
        idx_a = int(idx_a_str) if idx_a_str else 0
        idx_b = int(idx_b_str) if idx_b_str else 1
        rec_a = records[idx_a]
        rec_b = records[idx_b]
    except (ValueError, IndexError):
        print("[!] Invalid index selected. Comparing first two records by default.")
        rec_a = records[0]
        rec_b = records[1]

    # Perform comparison
    print("\n[*] Comparing property records...")
    res = compare_property_records(rec_a, rec_b)
    table = format_comparison_table(rec_a, rec_b, res)
    print("\n" + table)
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
        print("3. Add Manual Student Property Record (12 Student Factors & Breakdown)")
        print("4. Automated Property URL Ingestion & Real Data Validation")
        print("5. Identify & Handle Duplicate Property Records (Data Deduplication)")
        print("6. Compare Two Property Records (Side-by-Side Analysis)")
        print("7. Run Test Suites & Check Coverage (CO7095 QA Standard)")
        print("8. Exit")
        print("=" * 65)

        choice = input("Select an option (1-8): ").strip()
        if choice == "1":
            handle_process_collected_data()
        elif choice == "2":
            handle_simulate_and_merge_member_sources()
        elif choice == "3":
            handle_manual_student_property_entry()
        elif choice == "4":
            handle_manual_validation()
        elif choice == "5":
            handle_detect_and_handle_duplicates()
        elif choice == "6":
            handle_compare_two_properties()
        elif choice == "7":
            handle_run_all_tests()
        elif choice == "8":
            print("\nExiting application. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please enter 1, 2, 3, 4, 5, 6, 7, or 8.")


if __name__ == "__main__":
    main()
