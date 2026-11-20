"""
Data Collection Module (Member 1 - Data Collection).

This module provides open interfaces for data collection (e.g. web scraping,
API fetching, or file loading). Once Member 1 implements the real collectors,
they plug directly into get_collected_properties() without altering the pipeline.
"""

import os
import csv
from typing import List, Dict, Any


def fetch_raw_collected_data() -> List[Dict[str, Any]]:
    """
    Hook for Member 1 to return raw scraped or fetched data.
    If Member 1 has written records to Data/properties.csv, it loads them.
    If Data/properties.csv is empty or missing, returns an empty list or hook data.
    """
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "properties.csv")
    if not os.path.exists(data_path):
        return []

    collected: List[Dict[str, Any]] = []
    with open(data_path, mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            collected.append(dict(row))
    return collected
