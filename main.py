"""
Main Entry Point - Real Estate Data Collection and Analysis Tool.
Interactive Text-Based Console Application.
Compatible with standard Python & PyCharm.
"""

import os
import sys
import csv
import unittest
from typing import List, Dict, Any, Optional

from src.data_cleaning import (
    REQUIRED_PROPERTY_FIELDS,
    validate_property_record,
    check_required_fields,
    validate_price,
    validate_price_boundaries,
    validate_data_types,
    check_property_id_format,
    check_property_type_format,
    check_room_count_format,
    check_listing_url_format,
    validate_location_format,
    filter_valid_records,
    process_pipeline_records,
    extract_details_from_url,
    compare_property_records,
    format_comparison_table,
    identify_matching_property_info,
    flag_duplicate_property_records,
    report_detected_duplicates,
    identify_duplicates,
    handle_duplicates,
    generate_duplicate_report,
    identify_missing_property_info,
    generate_missing_data_report,
    generate_data_processing_summary,
    format_executive_summary_report,
    validate_student_accommodation_factors,
    validate_student_property_record,
    format_student_property_details,
    create_student_property_record,
    save_student_property_record,
    load_student_accommodations,
    format_amberstudent_locations_catalog,
    get_amberstudent_preferred_locations,
    match_amberstudent_location,
    merge_and_process_member_sources,
)
from src.data_collection import fetch_raw_collected_data, generate_mock_collected_properties
from src.property_search import Property, generate_mock_member4_properties

DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "Data", "properties.csv")


def display_records(records: List[Dict[str, Any]], title: str):
    """Displays a list of records in a formatted table."""
    print(f"\n--- {title} ({len(records)} records) ---")
    if not records:
        print("No records to display.")
        return

    header = f"{'ID':<16} | {'Type':<12} | {'Location':<22} | {'Price':<12} | {'Beds':<5} | {'Baths':<5}"
    print(header)
    print("-" * len(header))
    for r in records:
        print(
            f"{str(r.get('property_id', '')):<16} | "
            f"{str(r.get('property_type', '')):<12} | "
            f"{str(r.get('location', '')):<22} | "
            f"{str(r.get('price', '')):<12} | "
            f"{str(r.get('bedrooms', '')):<5} | "
            f"{str(r.get('bathrooms', '')):<5}"
        )


# ==============================================================================
# OPTION 1: Import & Process Stored Property Records
# ==============================================================================

def handle_import_and_process_stored_properties():
    """
    1. Import & Process Stored Property Records
    Connects to stored property collection (Data/properties.csv),
    processes through data validation pipeline, and separates reliable vs rejected records.
    """
    print("\n" + "=" * 70)
    print("      1. IMPORT & PROCESS STORED PROPERTY RECORDS      ")
    print("=" * 70)
    print("[*] Loading property records from Data/properties.csv...")
    raw_records = fetch_raw_collected_data()
    print(f"[*] Ingested {len(raw_records)} raw records from collection storage.")

    valid_recs, rejected_recs = process_pipeline_records(raw_records)
    display_records(valid_recs, "Processed & Validated Reliable Property Records")

    if rejected_recs:
        print(f"\n--- Identified Invalid Records ({len(rejected_recs)} records) ---")
        for rej in rejected_recs:
            rec = rej["record"]
            print(f"Index {rej['index']} (ID: {rec.get('property_id', 'UNKNOWN')}):")
            for err in rej["errors"]:
                print(f"    x {err}")
    else:
        print("\n[✓] All ingested records are valid and reliable.")
    print("=" * 70)


# ==============================================================================
# OPTION 2: Merge Property Data from External Sources
# ==============================================================================

def handle_merge_external_sources():
    """
    2. Merge Property Data from External Sources
    Ingests live/mock batches from Member 1 (Data Collection) and Member 4 (Properties Domain),
    merges them into a unified stream, validates every record, and displays the processed results.
    """
    print("\n" + "=" * 70)
    print("      2. MERGE PROPERTY DATA FROM EXTERNAL SOURCES      ")
    print("=" * 70)
    print("[*] Contacting Member 1 (Data Collection)... Generating batch of 4 records.")
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
    print("=" * 70)


# ==============================================================================
# OPTION 3: Add & Validate Manual Student Property Records
# ==============================================================================

def handle_manual_student_property_entry():
    """
    3. Add & Validate Manual Student Property Records
    Captures base property attributes and the 12 essential student factors:
      1. Student-preferred Location (AmberStudent Verified - https://amberstudent.com/)
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
    print("      3. ADD & VALIDATE MANUAL STUDENT PROPERTY RECORDS      ")
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

    print("\n1. Student-Preferred Location (Source: https://amberstudent.com/):")
    print("   Choose an AmberStudent Preferred Location or press [Enter] for default:")
    print("     [1] Leicester City Centre (LE1) - Dover St, Highcross, Station (DMU/UoL)")
    print("     [2] Clarendon Park & Queens Rd (LE2) - Victoria Park, UoL Campus, Cafes & Tesco")
    print("     [3] The West End & Narborough Rd (LE3) - CODE, Bede Park, River Soar, DMU Doorstep")
    print("     [4] DMU Campus Quarter (LE2) - Queens Court, Ben Russell Court, Jarrom St")
    print("     [5] Highfields & London Rd Corridor (LE2) - Railway Station, UoL & DMU")
    print("     [6] London - Bloomsbury & King's Cross (WC1) - UCL, KCL, LSE")
    print("     [7] Manchester - Oxford Road Corridor (M13) - Univ of Manchester, MMU")
    print("     [8] Enter custom location / paste from https://amberstudent.com/...")
    loc_choice = input("   Select option (1-8) or enter text [default: 1]: ").strip()

    amber_loc_map = {
        "1": "Leicester City Centre (LE1) - 5 mins to University of Leicester & DMU, 3 mins to Tesco Superstore, 8 mins to City Centre & Station",
        "2": "Clarendon Park & Queens Road (LE2) - 8 mins across Victoria Park to University of Leicester, Queens Rd cafes & Tesco",
        "3": "The West End & Narborough Road (LE3) - 3 mins walk to DMU campus, Bede Park, Lidl & River Soar",
        "4": "DMU Campus & Hospital Quarter (LE2) - 1-3 mins walk to DMU, Jarrom St / Eastern Blvd, 8 mins to City Centre",
        "5": "Highfields & London Road Corridor (LE2) - Midway between UoL and DMU, 3 mins to Leicester Railway Station & Tesco",
        "6": "London Bloomsbury & King's Cross (WC1) - Walking distance to UCL, KCL, LSE, King's Cross & Brunswick Centre",
        "7": "Manchester Oxford Road Corridor (M13) - Walking distance to University of Manchester & MMU, Oxford Rd Station"
    }

    if loc_choice in amber_loc_map:
        stu_loc = amber_loc_map[loc_choice]
        print(f"   ✓ Selected AmberStudent Verified Location: {stu_loc.split(' - ')[0]}")
    elif loc_choice == "8":
        custom_in = input("   Enter your custom location / AmberStudent details: ").strip()
        stu_loc = custom_in if custom_in else amber_loc_map["1"]
    elif not loc_choice:
        stu_loc = amber_loc_map["1"]
    else:
        stu_loc = loc_choice

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


# ==============================================================================
# OPTION 4: Extract & Process Property Data from URLs
# ==============================================================================

def handle_extract_property_data_from_urls():
    """
    4. Extract & Process Property Data from URLs
    Reads listing URL, extracts real property data, validates against acceptance criteria,
    displays room breakdown and student factors, and persists clean data.
    """
    print("\n" + "=" * 70)
    print("      4. EXTRACT & PROCESS PROPERTY DATA FROM URLS      ")
    print("=" * 70)
    print("Example URLs:")
    print("  • https://amberstudent.com/places/dover-street-apartments-leicester-2106166153995")
    print("  • https://amberstudent.com/places/pennine-house-leicester-2005064014733")
    print("  • https://amberstudent.com/places/the-summit-leicester-1809051412099")
    print("  • https://www.rightmove.co.uk/properties/145678901")

    url_input = input("\nEnter Listing URL [or press Enter for Dover Street Apartments default]: ").strip()
    if not url_input:
        url_input = "https://amberstudent.com/places/dover-street-apartments-leicester-2106166153995"

    print("\n[*] Processing URL and reading real listing data...")
    prop = extract_details_from_url(url_input)

    print("\n" + "-" * 70)
    print("                EXTRACTED REAL PROPERTY DATA                ")
    print("-" * 70)
    print(f"  • Property ID            : {prop.get('property_id')}")
    if prop.get('property_name'):
        print(f"  • Property Name          : {prop.get('property_name')}")
    print(f"  • Extracted Property Type : {prop.get('property_type')}")
    print(f"  • Extracted Location      : {prop.get('location')}")
    print(f"  • Extracted Price         : £{prop.get('price')}")
    print(f"  • Default Bedrooms        : {prop.get('bedrooms')}")
    print(f"  • Default Bathrooms       : {prop.get('bathrooms')}")

    if prop.get('room_types'):
        print("\n  • Room Types:")
        for rt in prop.get('room_types', []):
            print(f"      - {rt}")

    if prop.get('room_breakdown'):
        print("\n  • Room Breakdown Summary:")
        for k, v in prop.get('room_breakdown', {}).items():
            print(f"      * {k}: {v}")

    if prop.get('amenities'):
        print("\n  • Amenities:")
        for amen in prop.get('amenities', []):
            print(f"      ✓ {amen}")

    print("-" * 70)

    # Automatically validate the record
    print("[*] Validating record against Acceptance Criteria...")
    is_valid, errors = validate_property_record(prop)

    if is_valid:
        print("[PASSED] Record is 100% VALID and reliable for processing!")

        if prop.get("student_preferred_location"):
            print("\n[+] Student Accommodation detected! Suitable details list down:")
            report_text = format_student_property_details(prop)
            print("\n" + report_text)

        # Optionally persist
        save_choice = input(f"\nPersist record to {DATA_FILE_PATH}? (y/n) [default: y]: ").strip().lower()
        if save_choice != "n":
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
                print(f"[SAVED] Record successfully appended to {DATA_FILE_PATH}")
            except Exception as e:
                print(f"[!] Warning: Could not write to storage: {e}")
    else:
        print("[REJECTED] The record has invalid or missing fields:")
        for err in errors:
            print(f"    x {err}")

    print("=" * 70)


# ==============================================================================
# OPTION 5: Validate Property Records
# ==============================================================================

def handle_validate_property_records():
    """
    5. Validate Property Records
       - Check Required Property Fields
       - Validate Property Prices
       - Validate Data Types & Information Formats
       - Identify Invalid Property Records
    """
    records = fetch_raw_collected_data()
    total = len(records)

    while True:
        print("\n" + "=" * 70)
        print("                 5. VALIDATE PROPERTY RECORDS                  ")
        print("=" * 70)
        print(f"Stored records available: {total} records from {DATA_FILE_PATH}\n")
        print("Validation Areas:")
        print("  1. Check Required Property Fields (Check missing/blank mandatory keys)")
        print("  2. Validate Property Prices (Positive value, £50 - £50,000,000 bounds)")
        print("  3. Validate Data Types & Information Formats (ID, Type, Beds, URL syntax)")
        print("  4. Identify Invalid Property Records (Full rejection diagnosis)")
        print("  5. Run Complete Quality Assurance Validation Audit (All checks)")
        print("  6. Return to Main Menu")
        print("=" * 70)

        sub_choice = input("Select a validation check (1-6) [default: 5]: ").strip()
        if not sub_choice:
            sub_choice = "5"

        if sub_choice == "1":
            print("\n--- [Audit 1: Check Required Property Fields] ---")
            missing_count = 0
            for idx, r in enumerate(records):
                ok, errs = check_required_fields(r)
                if not ok:
                    missing_count += 1
                    print(f"  x Row #{idx} [ID: {r.get('property_id', 'UNKNOWN')}]: Missing {errs}")
            if missing_count == 0:
                print(f"  [✓] All {total} property records contain all mandatory required fields.")
            else:
                print(f"  [!] {missing_count} out of {total} records have missing required fields.")

        elif sub_choice == "2":
            print("\n--- [Audit 2: Validate Property Prices & Boundaries] ---")
            price_errs_count = 0
            for idx, r in enumerate(records):
                p_val = r.get("price")
                ok, p_err = validate_price(p_val)
                if not ok:
                    price_errs_count += 1
                    print(f"  x Row #{idx} [ID: {r.get('property_id')}]: Invalid price '{p_val}' -> {p_err}")
                else:
                    ok_b, b_err = validate_price_boundaries(p_val, min_price=50.0, max_price=50000000.0)
                    if not ok_b:
                        price_errs_count += 1
                        print(f"  x Row #{idx} [ID: {r.get('property_id')}]: Boundary violation -> {b_err}")
            if price_errs_count == 0:
                print(f"  [✓] All {total} property records possess valid positive prices within bounds.")
            else:
                print(f"  [!] Found {price_errs_count} price validation errors.")

        elif sub_choice == "3":
            print("\n--- [Audit 3: Validate Data Types & Information Formats] ---")
            fmt_errs = 0
            for idx, r in enumerate(records):
                row_errs = []
                ok_id, id_e = check_property_id_format(r.get("property_id"))
                if not ok_id:
                    row_errs.append(id_e)
                ok_t, t_e = check_property_type_format(r.get("property_type"))
                if not ok_t:
                    row_errs.append(t_e)
                ok_bed, bed_e = check_room_count_format(r.get("bedrooms"), "bedrooms")
                if not ok_bed:
                    row_errs.append(bed_e)
                ok_url, url_e = check_listing_url_format(r.get("listing_url"))
                if not ok_url:
                    row_errs.append(url_e)
                ok_loc, loc_e = validate_location_format(r.get("location"))
                if not ok_loc:
                    row_errs.append(loc_e)

                if row_errs:
                    fmt_errs += 1
                    print(f"  x Row #{idx} [ID: {r.get('property_id')}]: Format issues -> {row_errs}")

            if fmt_errs == 0:
                print(f"  [✓] All {total} property records satisfy syntax and type specifications.")
            else:
                print(f"  [!] Found {fmt_errs} records with format/type irregularities.")

        elif sub_choice == "4":
            print("\n--- [Audit 4: Identify Invalid Property Records] ---")
            valid_recs, invalid_recs = filter_valid_records(records)
            print(f"  • Total Evaluated : {total}")
            print(f"  • Valid Records    : {len(valid_recs)}")
            print(f"  • Invalid Records  : {len(invalid_recs)}")

            if invalid_recs:
                print("\n  Invalid Records Breakdown:")
                for rej in invalid_recs:
                    rec = rej["record"]
                    print(f"    x Row #{rej['index']} (ID: {rec.get('property_id', 'UNKNOWN')}):")
                    for err in rej["errors"]:
                        print(f"        - {err}")
            else:
                print("  [✓] No invalid records identified.")

        elif sub_choice == "5":
            print("\n--- [Comprehensive Property Validation Audit] ---")
            valid_recs, invalid_recs = filter_valid_records(records)
            pass_rate = (len(valid_recs) / total * 100) if total > 0 else 0.0

            print(f"  • Dataset Ingested : {total} records from {DATA_FILE_PATH}")
            print(f"  • Reliable Valid   : {len(valid_recs)} ({pass_rate:.1f}%)")
            print(f"  • Rejected Invalid : {len(invalid_recs)} ({100.0 - pass_rate:.1f}%)")

            if invalid_recs:
                print(f"\n  Identified {len(invalid_recs)} Invalid Records:")
                for rej in invalid_recs:
                    print(f"    • ID {rej['record'].get('property_id')}: {len(rej['errors'])} error(s) -> {rej['errors']}")
            else:
                print("  [✓] 100% of stored records passed all 8 QA validation areas.")

        elif sub_choice == "6":
            break
        else:
            print("[!] Invalid selection. Please enter 1-6.")


# ==============================================================================
# OPTION 6: Detect & Manage Duplicate Property Records
# ==============================================================================

def handle_detect_and_manage_duplicates():
    """
    6. Detect & Manage Duplicate Property Records
       - Compare Property Records
       - Identify Matching Property Information
       - Flag Duplicate Records
       - Generate Duplicate Detection Reports
    """
    records = fetch_raw_collected_data()

    while True:
        print("\n" + "=" * 70)
        print("          6. DETECT & MANAGE DUPLICATE PROPERTY RECORDS         ")
        print("=" * 70)
        print(f"Dataset: {len(records)} records from {DATA_FILE_PATH}\n")
        print("Duplicate Management Actions:")
        print("  1. Identify Matching Property Information & Compare Records")
        print("  2. Flag Duplicate Records with In-Memory Audit Markers")
        print("  3. Generate Duplicate Detection Audit Report")
        print("  4. Apply Handling Strategy (keep_first, keep_last, flag, merge, quarantine) & Save")
        print("  5. Run Complete End-to-End Duplicate Pipeline (Default)")
        print("  6. Return to Main Menu")
        print("=" * 70)

        sub_choice = input("Select an action (1-6) [default: 5]: ").strip()
        if not sub_choice:
            sub_choice = "5"

        if sub_choice == "1":
            print("\n[*] Comparing property records and identifying matching information...")
            matches = identify_matching_property_info(records)
            print(f"  • Total Matches Found: {len(matches)}")
            for m in matches[:10]:
                print(f"    - [{m['match_type'].upper()}] Record #{m['record_a_index']} matches #{m['record_b_index']} ({m['similarity_score']:.1f}% match): {m['reason']}")
            if len(matches) > 10:
                print(f"    ... and {len(matches) - 10} more matching pairs.")

        elif sub_choice == "2":
            print("\n[*] Flagging duplicate records in dataset...")
            flagged = flag_duplicate_property_records(records)
            dup_flagged = [r for r in flagged if r.get("is_duplicate")]
            print(f"  • Flagged {len(dup_flagged)} duplicate records out of {len(records)} total.")
            for r in dup_flagged[:10]:
                print(f"    ! ID: {r.get('property_id')} | Flag: {r.get('duplicate_flag')} | Reason: {r.get('duplicate_reason')}")

        elif sub_choice == "3":
            print("\n[*] Generating Duplicate Detection Report...")
            report_text = generate_duplicate_report(records)
            print("\n" + report_text)

        elif sub_choice == "4" or sub_choice == "5":
            report_text = generate_duplicate_report(records)
            print("\n" + report_text)

            analysis = identify_duplicates(records)
            if analysis["duplicate_count"] == 0:
                print("[✓] All records are unique. No deduplication required.")
                if sub_choice == "5":
                    break
                continue

            print("\nSelect a Duplicate Handling Strategy:")
            print("  1. keep_first    : Retain primary occurrence and separate duplicates (Default)")
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

            if sub_choice == "5":
                break

        elif sub_choice == "6":
            break
        else:
            print("[!] Invalid selection. Please enter 1-6.")


# ==============================================================================
# OPTION 7: Identify Missing Property Information
# ==============================================================================

def handle_identify_missing_property_information():
    """
    7. Identify Missing Property Information
       - Check Missing & Empty Fields
       - Identify Incomplete Property Records
       - Display Missing Information
       - Generate Missing-Data Reports
    """
    records = fetch_raw_collected_data()
    total = len(records)

    while True:
        print("\n" + "=" * 70)
        print("          7. IDENTIFY MISSING PROPERTY INFORMATION             ")
        print("=" * 70)
        print(f"Stored records: {total} records from {DATA_FILE_PATH}\n")
        print("Missing Data Operations:")
        print("  1. Check Missing & Empty Fields (Field-level summary & percentages)")
        print("  2. Identify Incomplete Property Records (List incomplete listings)")
        print("  3. Display Missing Information Table (Detailed breakdown)")
        print("  4. Generate Comprehensive Missing-Data Audit Report")
        print("  5. Return to Main Menu")
        print("=" * 70)

        sub_choice = input("Select an operation (1-5) [default: 4]: ").strip()
        if not sub_choice:
            sub_choice = "4"

        if sub_choice == "1":
            print("\n[*] Auditing missing & empty fields across dataset...")
            analysis = identify_missing_property_info(records)
            print(f"\n  • Total Records Analyzed: {analysis['total_records']}")
            print(f"  • Completeness Score    : {analysis['completeness_rate']:.1f}%\n")
            print(f"  {'Field Name':<20} | {'Missing Count':<14} | {'Missing %':<10}")
            print("  " + "-" * 50)
            for f in analysis["checked_fields"]:
                cnt = analysis["field_missing_counts"].get(f, 0)
                pct = analysis["field_missing_percentages"].get(f, 0.0)
                print(f"  {f:<20} | {cnt:<14} | {pct:>8.1f}%")

        elif sub_choice == "2":
            print("\n[*] Identifying incomplete property records...")
            analysis = identify_missing_property_info(records)
            incompletes = analysis["incomplete_records"]
            print(f"  • Found {len(incompletes)} incomplete records out of {total} total.")
            if not incompletes:
                print("  [✓] All property records are 100% complete.")
            else:
                for item in incompletes[:15]:
                    pid = item["property_id"]
                    idx = item["index"]
                    missing_fields = ", ".join(item["missing_fields"])
                    print(f"    • Row #{idx:<3} [ID: {pid:<16}]: Missing -> [{missing_fields}]")
                if len(incompletes) > 15:
                    print(f"    ... and {len(incompletes) - 15} more incomplete records.")

        elif sub_choice == "3":
            print("\n[*] Displaying missing information matrix...")
            analysis = identify_missing_property_info(records)
            incompletes = analysis["incomplete_records"]
            if not incompletes:
                print("  [✓] Zero missing values detected across all attributes.")
            else:
                hdr = f"{'Row':<6} | {'Property ID':<18} | {'Missing Fields'}"
                print(hdr)
                print("-" * len(hdr) + "-" * 20)
                for item in incompletes:
                    print(f"{item['index']:<6} | {item['property_id']:<18} | {', '.join(item['missing_fields'])}")

        elif sub_choice == "4":
            print("\n[*] Generating Missing-Data Audit Report...")
            report = generate_missing_data_report(records)
            print("\n" + report)

        elif sub_choice == "5":
            break
        else:
            print("[!] Invalid selection. Please enter 1-5.")


# ==============================================================================
# OPTION 8: Compare Property Records
# ==============================================================================

def handle_compare_property_records():
    """
    8. Compare Property Records
       - Side-by-Side Property Comparison
       - Identify Field-Level Differences
    """
    print("\n" + "=" * 70)
    print("                 8. COMPARE PROPERTY RECORDS                   ")
    print("=" * 70)
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
    print("\n[*] Running side-by-side comparison and identifying field-level differences...")
    res = compare_property_records(rec_a, rec_b)
    table = format_comparison_table(rec_a, rec_b, res)
    print("\n" + table)

    # Explicit summary of field-level differences
    print("\n--- Field-Level Differences Breakdown ---")
    p_diff = res.get("price_difference", {})
    if p_diff:
        print(f"  • Price Variance   : £{p_diff.get('amount', 0):.2f} ({p_diff.get('percentage', 0):.1f}%)")
    print(f"  • Matching Fields  : {', '.join(res.get('matching_fields', [])) or 'None'}")
    print(f"  • Differing Fields : {', '.join(res.get('differing_fields', [])) or 'None'}")
    print(f"  • Overall Match    : {res.get('similarity_score', 0):.1f}% Similarity Score")
    print("=" * 70)


# ==============================================================================
# OPTION 9: Run Data Processing Test Suites
# ==============================================================================

def handle_run_data_processing_test_suites():
    """
    9. Run Data Processing Test Suites
       - Property Validation Tests
       - Duplicate Detection Tests
       - Missing Data Tests
       - Integration & Performance Tests
       - Test Coverage Report
    """
    while True:
        print("\n" + "=" * 70)
        print("            9. RUN DATA PROCESSING TEST SUITES                 ")
        print("=" * 70)
        print("Available Test Suites:")
        print("  1. Property Validation Tests (Acceptance & Specification BVA)")
        print("  2. Duplicate Detection Tests (Deduplication Acceptance & White-Box)")
        print("  3. Missing Data Tests (Missing Data Acceptance & Quality Checks)")
        print("  4. Integration & Performance Tests (Random Fuzzing, Concolic & Symbolic)")
        print("  5. Run Complete Test Suite & Generate Test Coverage Report (Default)")
        print("  6. Return to Main Menu")
        print("=" * 70)

        sub_choice = input("Select a test suite (1-6) [default: 5]: ").strip()
        if not sub_choice:
            sub_choice = "5"

        loader = unittest.TestLoader()

        if sub_choice == "1":
            print("\n[*] Running Property Validation Tests...")
            suite = loader.loadTestsFromName("tests.test_acceptance_criteria.TestAcceptanceCriteria")
            # Select validation tests
            val_suite = unittest.TestSuite([
                t for t in suite if any(k in t.id() for k in ["criterion_1", "criterion_2", "criterion_3", "criterion_4", "acceptance_area"])
            ])
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(val_suite)

        elif sub_choice == "2":
            print("\n[*] Running Duplicate Detection Tests...")
            suite = loader.loadTestsFromName("tests.test_acceptance_criteria.TestAcceptanceCriteria")
            dup_suite = unittest.TestSuite([
                t for t in suite if "duplicate" in t.id()
            ])
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(dup_suite)

        elif sub_choice == "3":
            print("\n[*] Running Missing Data Tests...")
            suite = loader.loadTestsFromName("tests.test_acceptance_criteria.TestAcceptanceCriteria")
            miss_suite = unittest.TestSuite([
                t for t in suite if "missing" in t.id()
            ])
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(miss_suite)

        elif sub_choice == "4":
            print("\n[*] Running Integration & Performance Tests (Fuzzing, Concolic, Symbolic)...")
            suite_fuzz = loader.discover("tests/black_box_random", pattern="test_*.py")
            suite_conc = loader.discover("tests/concolic_testing", pattern="test_*.py")
            suite_sym = loader.discover("tests/symbolic_execution", pattern="test_*.py")
            combined = unittest.TestSuite([suite_fuzz, suite_conc, suite_sym])
            runner = unittest.TextTestRunner(verbosity=2)
            runner.run(combined)

        elif sub_choice == "5":
            print("\n[*] Executing All Test Suites and Computing Statement/Branch Coverage...")
            import run_tests_with_coverage
            run_tests_with_coverage.main()

        elif sub_choice == "6":
            break
        else:
            print("[!] Invalid selection. Please enter 1-6.")


# ==============================================================================
# OPTION 10: View Data Processing Summary & Reports
# ==============================================================================

def handle_view_data_processing_summary_and_reports():
    """
    10. View Data Processing Summary & Reports
    Displays high-level executive dashboard summarizing validation health,
    deduplication status, completeness, student accommodation coverage, and QA compliance.
    """
    print("\n" + "=" * 70)
    print("      10. VIEW DATA PROCESSING SUMMARY & REPORTS        ")
    print("=" * 70)
    records = fetch_raw_collected_data()
    dashboard = format_executive_summary_report(records)
    print("\n" + dashboard)
    print("=" * 70)


# ==============================================================================
# MAIN MENU LOOP (Exact 11-Option Structure Requested by User)
# ==============================================================================

def main():
    while True:
        print("\n" + "=" * 65)
        print("       REAL ESTATE DATA ANALYSIS TOOL")
        print("              DATA PROCESSING MODULE")
        print("=" * 65)
        print("")
        print("  PROPERTY DATA COLLECTION & INTEGRATION")
        print("")
        print("  1. Import & Process Stored Property Records")
        print("  2. Merge Property Data from External Sources")
        print("  3. Add & Validate Manual Student Property Records")
        print("  4. Extract & Process Property Data from URLs")
        print("")
        print("  DATA QUALITY MANAGEMENT")
        print("")
        print("  5. Validate Property Records")
        print("     - Check Required Property Fields")
        print("     - Validate Property Prices")
        print("     - Validate Data Types & Information Formats")
        print("     - Identify Invalid Property Records")
        print("")
        print("  6. Detect & Manage Duplicate Property Records")
        print("     - Compare Property Records")
        print("     - Identify Matching Property Information")
        print("     - Flag Duplicate Records")
        print("     - Generate Duplicate Detection Reports")
        print("")
        print("  7. Identify Missing Property Information")
        print("     - Check Missing & Empty Fields")
        print("     - Identify Incomplete Property Records")
        print("     - Display Missing Information")
        print("     - Generate Missing-Data Reports")
        print("")
        print("  PROPERTY COMPARISON & QUALITY ASSURANCE")
        print("")
        print("  8. Compare Property Records")
        print("     - Side-by-Side Property Comparison")
        print("     - Identify Field-Level Differences")
        print("")
        print("  9. Run Data Processing Test Suites")
        print("     - Property Validation Tests")
        print("     - Duplicate Detection Tests")
        print("     - Missing Data Tests")
        print("     - Integration & Performance Tests")
        print("     - Test Coverage Report")
        print("")
        print("  10. View Data Processing Summary & Reports")
        print("")
        print("  11. Exit")
        print("")
        print("=" * 65)

        choice = input("  Select an option (1-11): ").strip()

        if choice == "1":
            handle_import_and_process_stored_properties()
        elif choice == "2":
            handle_merge_external_sources()
        elif choice == "3":
            handle_manual_student_property_entry()
        elif choice == "4":
            handle_extract_property_data_from_urls()
        elif choice == "5":
            handle_validate_property_records()
        elif choice == "6":
            handle_detect_and_manage_duplicates()
        elif choice == "7":
            handle_identify_missing_property_information()
        elif choice == "8":
            handle_compare_property_records()
        elif choice == "9":
            handle_run_data_processing_test_suites()
        elif choice == "10":
            handle_view_data_processing_summary_and_reports()
        elif choice == "11":
            print("\nExiting Data Processing Module. Goodbye!")
            break
        else:
            print("[!] Invalid option. Please select a number between 1 and 11.")


if __name__ == "__main__":
    main()
