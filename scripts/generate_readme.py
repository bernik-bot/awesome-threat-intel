#!/usr/bin/env python3
"""Generate README.md from structured JSON data."""

import json
import os
from datetime import datetime

CATEGORIES_ORDER = [
    "Threat Intelligence Platforms",
    "Intelligence Feeds & Data Providers",
    "OSINT & Collection Tools",
    "Frameworks & Standards",
]

CATEGORY_DEFINITIONS = {
    "Threat Intelligence Platforms": (
        "Systems that ingest, enrich, correlate, and manage threat intelligence. "
        "If it aggregates and operationalizes intelligence, it belongs here."
    ),
    "Intelligence Feeds & Data Providers": (
        "Sources that provide raw or processed intelligence data "
        "(IOCs, TTPs, reports, reputation data). If it primarily provides data, it belongs here."
    ),
    "OSINT & Collection Tools": (
        "Tools used to collect intelligence from public or semi-public sources. "
        "If it gathers data but does not provide curated intel, it belongs here."
    ),
    "Frameworks & Standards": (
        "Models and protocols used to structure or exchange intelligence "
        "(MITRE ATT&CK, STIX, TAXII, etc.)."
    ),
}

LICENSING_BADGES = {
    "Open Source": "![Open Source](https://img.shields.io/badge/License-Open%20Source-green)",
    "Commercial": "![Commercial](https://img.shields.io/badge/License-Commercial-orange)",
    "Freemium": "![Freemium](https://img.shields.io/badge/License-Freemium-blue)",
}

REGION_BADGES = {
    "EU": "![EU](https://img.shields.io/badge/Region-EU-blueviolet)",
    "US": "![US](https://img.shields.io/badge/Region-US-blueviolet)",
    "APAC": "![APAC](https://img.shields.io/badge/Region-APAC-blueviolet)",
    "Other": "",
}


def get_badge(entry):
    """Return a string of badges for an entry."""
    badges = []

    license_badge = LICENSING_BADGES.get(entry.get("license", ""), "")
    if license_badge:
        badges.append(license_badge)

    region = entry.get("region", "")
    if region == "EU":
        badges.append("![EU](https://img.shields.io/badge/Region-EU-blueviolet)")
    elif region == "APAC":
        badges.append("![APAC](https://img.shields.io/badge/Region-APAC-blueviolet)")

    if entry.get("api_available") == "Yes":
        badges.append("![API](https://img.shields.io/badge/API-Yes-brightgreen)")

    if entry.get("stix_taxii_support") == "Yes":
        badges.append("![STIX/TAXII](https://img.shields.io/badge/STIX%2FTAXII-Yes-brightgreen)")

    return " ".join(badges)


def get_subcategory_label(subcategory):
    """Return a display label for the subcategory."""
    labels = {
        "TIP": "Platform",
        "Feed": "Feed",
        "ISAC": "ISAC",
        "Sharing Group": "Sharing Group",
        "OSINT": "OSINT Tool",
        "Malware Analysis": "Malware Analysis",
        "IOC / Data Enrichment": "Enrichment",
        "Detection Rules": "Detection Rules",
        "Framework": "Framework",
        "Standard": "Standard",
        "Research": "Research",
        "Cyber and threat intel AI": "Cyber and threat intel AI",
        "Predictive Intel": "Predictive Intel",
    }
    return labels.get(subcategory, subcategory)


def generate_category_section(category, entries):
    """Generate markdown for a single category."""
    lines = []
    lines.append(f"## {category}")
    lines.append("")
    lines.append(f"*{CATEGORY_DEFINITIONS.get(category, '')}*")
    lines.append("")

    subcategories = {}
    for entry in entries:
        sub = entry.get("subcategory", "Other")
        if sub not in subcategories:
            subcategories[sub] = []
        subcategories[sub].append(entry)

    for subcat, sub_entries in subcategories.items():
        if len(subcategories) > 1:
            lines.append(f"### {subcat}")
            lines.append("")

        lines.append("| Name | Description | License | Region | Access |")
        lines.append("|------|-------------|---------|--------|--------|")

        for entry in sorted(sub_entries, key=lambda e: e["name"].lower()):
            name = entry["name"]
            url = entry.get("url", "")
            desc = entry.get("description", "")
            license_type = entry.get("license", "N/A")
            region = entry.get("region", "N/A")
            access = entry.get("access_type", "N/A")

            if url:
                name_link = f"[{name}]({url})"
            else:
                name_link = name

            lines.append(f"| {name_link} | {desc} | {license_type} | {region} | {access} |")

        lines.append("")

    return "\n".join(lines)


def generate_readme(data):
    """Generate the full README content."""
    lines = []

    lines.append("# Awesome Threat Intelligence [![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome)")
    lines.append("")
    lines.append("> A curated list of awesome threat intelligence resources, tools, feeds, and platforms.")
    lines.append(">")
    lines.append("> **Last updated:** " + datetime.now().strftime("%Y-%m-%d"))
    lines.append("> **Total entries:** " + str(len(data)))
    lines.append("")

    lines.append("## About This List")
    lines.append("")
    lines.append("This list is organized by a clean, non-overlapping taxonomy. Each entry includes structured metadata")
    lines.append("enabling filtering by license, region, deployment model, data type, and more.")
    lines.append("")
    lines.append("### Badge Legend")
    lines.append("")
    lines.append("- ![Open Source](https://img.shields.io/badge/License-Open%20Source-green) = Free and open-source software")
    lines.append("- ![Commercial](https://img.shields.io/badge/License-Commercial-orange) = Commercial/paid software")
    lines.append("- ![Freemium](https://img.shields.io/badge/License-Freemium-blue) = Free tier with paid upgrades")
    lines.append("- ![EU](https://img.shields.io/badge/Region-EU-blueviolet) = Vendor headquartered in the European Union")
    lines.append("- ![API](https://img.shields.io/badge/API-Yes-brightgreen) = REST/GraphQL API available")
    lines.append("- ![STIX/TAXII](https://img.shields.io/badge/STIX%2FTAXII-Yes-brightgreen) = STIX/TAXII protocol support")
    lines.append("")

    lines.append("### Quick Filter Guide")
    lines.append("")
    lines.append("- **Looking for open-source TIPs?** See [Threat Intelligence Platforms](#threat-intelligence-platforms) and filter by `Open Source` license")
    lines.append("- **Looking for free threat feeds?** See [Intelligence Feeds & Data Providers](#intelligence-feeds--data-providers) and filter by `Free` access")
    lines.append("- **Looking for EU-based vendors?** Look for the ![EU](https://img.shields.io/badge/Region-EU-blueviolet) badge")
    lines.append("")

    lines.append("### Taxonomy")
    lines.append("")
    lines.append("| Category | Description |")
    lines.append("|----------|-------------|")
    for cat in CATEGORIES_ORDER:
        lines.append(f"| [{cat}](#{cat.lower().replace(' & ', '-').replace(' ', '-').replace('--', '-')}) | {CATEGORY_DEFINITIONS.get(cat, '')} |")
    lines.append("")

    lines.append("---")
    lines.append("")

    for category in CATEGORIES_ORDER:
        cat_entries = [e for e in data if e.get("category") == category]
        if cat_entries:
            lines.append(generate_category_section(category, cat_entries))
            lines.append("---")
            lines.append("")

    lines.append("## Contributing")
    lines.append("")
    lines.append("Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.")
    lines.append("")

    lines.append("## License")
    lines.append("")
    lines.append("[![CC0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/cc-zero.svg)](https://creativecommons.org/publicdomain/zero/1.0/)")
    lines.append("")
    lines.append("To the extent possible under law, the authors have waived all copyright and related or neighboring rights to this work.")
    lines.append("")

    return "\n".join(lines)


def main():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data", "entries.json")
    output_path = os.path.join(os.path.dirname(__file__), "..", "README.md")

    with open(data_path, "r") as f:
        data = json.load(f)

    readme_content = generate_readme(data)

    with open(output_path, "w") as f:
        f.write(readme_content)

    print(f"README.md generated with {len(data)} entries.")


if __name__ == "__main__":
    main()
