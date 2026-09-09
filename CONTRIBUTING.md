# Contributing to Awesome Threat Intelligence

## Contribution Guidelines

This list follows a strict taxonomy and metadata schema to ensure consistency and machine-readability.

### Adding New Entries

All new entries must be added to `data/entries.json` with the following required fields:

```json
{
  "name": "Tool or Provider Name",
  "description": "Concise 1-2 line description. No marketing language.",
  "category": "One of the 10 top-level categories",
  "subcategory": "TIP | Feed | ISAC | Sharing Group | OSINT | Malware Analysis | IOC / Data Enrichment | Detection Rules | Framework | Standard | Research | LLM Assistant | AI Platform | Automated Analysis | Predictive Intel",
  "license": "Open Source | Commercial | Freemium",
  "deployment": "SaaS | Self-hosted | Hybrid | N/A",
  "vendor": "Company or project name",
  "vendor_hq_country": "Country where vendor is headquartered",
  "region": "EU | US | APAC | Other",
  "data_type": "Indicators | TTPs | Malware | Vulnerabilities | Mixed | Behavioral | External Threats",
  "access_type": "Free | Paid | API | Invite-only | Freemium",
  "last_verified": "YYYY-MM-DD",
  "api_available": "Yes | No",
  "stix_taxii_support": "Yes | No",
  "focus_area": "Primary focus of the tool/provider",
  "integrations": "Comma-separated list of integration types",
  "url": "Primary URL",
  "tags": ["tag1", "tag2"]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Name of the tool, feed, or platform |
| `description` | string | 1-2 lines, objective, no marketing language |
| `category` | string | Must match one of the 10 defined categories exactly |
| `subcategory` | string | Subcategory within the category |
| `license` | string | Open Source, Commercial, or Freemium |
| `deployment` | string | SaaS, Self-hosted, Hybrid, or N/A |
| `vendor` | string | Company or project name |
| `vendor_hq_country` | string | Country where vendor HQ is located (require source) |
| `region` | string | EU, US, APAC, or Other |
| `data_type` | string | Indicators, TTPs, Malware, Vulnerabilities, or Mixed |
| `access_type` | string | Free, Paid, API, or Invite-only |
| `last_verified` | string | Date the entry was verified as active (YYYY-MM-DD) |
| `api_available` | string | Yes or No |
| `stix_taxii_support` | string | Yes or No |
| `focus_area` | string | Primary use case or focus |
| `integrations` | string | Comma-separated list of integration types |
| `url` | string | Primary URL for the resource |
| `tags` | array | Array of lowercase tags |

### Category Definitions

1. **Threat Intelligence Platforms** - Systems that ingest, enrich, correlate, and manage threat intelligence
2. **Intelligence Feeds & Data Providers** - Sources that provide raw or processed intelligence data
3. **OSINT & Collection Tools** - Tools that collect intelligence from public sources
4. **Frameworks & Standards** - Models and protocols for structuring/exchanging intelligence

### Rules

- **Do NOT create new categories.** Use the existing taxonomy.
- **Do NOT mix categories.** If a tool fits multiple categories, choose the primary one.
- **Verify before submitting.** All entries must be active and maintained.
- **No marketing language.** Descriptions must be objective and concise.
- **Provide sources for vendor HQ.** If unsure, note "Needs verification" in a PR comment.
- **Use `last_verified` with today's date** when adding a new entry.

### Pull Request Process

1. Fork the repository
2. Add your entry to `data/entries.json` (not README.md directly)
3. Run the validation script: `python3 scripts/validate.py`
4. Regenerate the README: `python3 scripts/generate_readme.py`
5. Submit a pull request with a clear description

### Updating Existing Entries

- Update the `last_verified` date when confirming an entry is still active
- Flag entries that appear unmaintained with a comment in the PR
- Do not remove entries without discussion -- mark them as "Needs verification" first

### Validation

Before submitting, ensure:
- All required fields are present
- `category` matches one of the 10 defined categories exactly
- `license` is one of: Open Source, Commercial, Freemium
- `region` is one of: EU, US, APAC, Other
- `access_type` is one of: Free, Paid, API, Invite-only
- `last_verified` is in YYYY-MM-DD format
- No duplicate entries exist
- URL is valid and accessible

Thank you for contributing!
