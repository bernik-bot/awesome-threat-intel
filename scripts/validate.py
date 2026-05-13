#!/usr/bin/env python3
"""Validate entries.json against the schema."""

import json
import os
import re
import sys

VALID_CATEGORIES = [
    "Threat Intelligence Platforms",
    "Intelligence Feeds & Data Providers",
    "OSINT & Collection Tools",
    "Frameworks & Standards",
    "Threat Intelligence AI",
]

VALID_LICENSES = ["Open Source", "Commercial", "Freemium", "N/A"]
VALID_DEPLOYMENTS = ["SaaS", "Self-hosted", "Hybrid", "N/A"]
VALID_REGIONS = ["EU", "US", "APAC", "Other", "Middle East", "North America", "Unknown", "Europe/Asia"]
VALID_DATA_TYPES = ["Indicators", "TTPs", "Malware", "Vulnerabilities", "Mixed", "Behavioral", "External Threats"]
VALID_ACCESS_TYPES = ["Free", "Paid", "API", "Invite-only", "Freemium"]
VALID_YES_NO = ["Yes", "No"]

REQUIRED_FIELDS = [
    "name", "description", "category", "subcategory", "license",
    "deployment", "vendor", "vendor_hq_country", "region", "data_type",
    "access_type", "last_verified", "api_available", "stix_taxii_support",
    "focus_area", "integrations", "url", "tags",
]

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
URL_PATTERN = re.compile(r"^https?://.+$")


def validate_entry(entry, index):
    """Validate a single entry. Returns a list of errors."""
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in entry:
            errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): missing field '{field}'")

    if entry.get("category") not in VALID_CATEGORIES:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid category '{entry.get('category')}'")

    if entry.get("license") not in VALID_LICENSES:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid license '{entry.get('license')}'")

    if entry.get("deployment") not in VALID_DEPLOYMENTS:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid deployment '{entry.get('deployment')}'")

    if entry.get("region") not in VALID_REGIONS:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid region '{entry.get('region')}'")

    if entry.get("data_type") not in VALID_DATA_TYPES:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid data_type '{entry.get('data_type')}'")

    if entry.get("access_type") not in VALID_ACCESS_TYPES:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid access_type '{entry.get('access_type')}'")

    if entry.get("api_available") not in VALID_YES_NO:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid api_available '{entry.get('api_available')}'")

    if entry.get("stix_taxii_support") not in VALID_YES_NO:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid stix_taxii_support '{entry.get('stix_taxii_support')}'")

    if entry.get("last_verified") and not DATE_PATTERN.match(entry["last_verified"]):
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid date format '{entry.get('last_verified')}' (use YYYY-MM-DD)")

    if entry.get("url") and not URL_PATTERN.match(entry["url"]):
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): invalid URL '{entry.get('url')}'")

    if not isinstance(entry.get("tags"), list):
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): 'tags' must be an array")

    if entry.get("description") and len(entry["description"]) > 200:
        errors.append(f"Entry #{index} ({entry.get('name', 'unknown')}): description too long (max 200 chars)")

    return errors


def validate_duplicates(data):
    """Check for duplicate entries by name."""
    names = {}
    errors = []
    for i, entry in enumerate(data):
        name = entry.get("name", "").lower()
        if name in names:
            errors.append(f"Duplicate entry: '{entry.get('name')}' (first seen at index {names[name]}, again at index {i})")
        else:
            names[name] = i
    return errors


def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "entries.json")

    with open(data_path, "r") as f:
        data = json.load(f)

    all_errors = []

    for i, entry in enumerate(data):
        all_errors.extend(validate_entry(entry, i))

    all_errors.extend(validate_duplicates(data))

    if all_errors:
        print(f"Validation failed with {len(all_errors)} error(s):")
        for error in all_errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"Validation passed: {len(data)} entries, 0 errors.")
        sys.exit(0)


if __name__ == "__main__":
    main()
