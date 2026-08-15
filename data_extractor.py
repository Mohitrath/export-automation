"""Normalizes raw CSV rows into the buyer schema (Section 5.2 of the spec).

Source of truth for a record is whatever the operator uploads — there is no
scraping adapter here. Bring your own leads (trade-fair contacts, inbound
inquiries, directory listings you've manually collected, etc.).
"""
from validation.email_validator import is_valid_email

REQUIRED_COLUMNS = ['buyer_name', 'company_name', 'email', 'website', 'country', 'source_platform']


def normalize_record(row: dict):
    email = str(row.get('email', '')).strip().lower()
    if not is_valid_email(email):
        return None
    return {
        'buyer_name': str(row.get('buyer_name', '')).strip(),
        'company_name': str(row.get('company_name', '')).strip(),
        'email': email,
        'website': str(row.get('website', '')).strip(),
        'country': str(row.get('country', '')).strip(),
        'source_platform': str(row.get('source_platform', '')).strip() or 'Manual CSV',
    }
