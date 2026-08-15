"""Regex-based email validation (Section 5.3 / 12.1 of the spec).

Deliberately syntax-only: no network lookups, no MX checks, no third-party
disposable-email services. Keeps validation fast, offline, and side-effect free.
"""
import re

PATTERN = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$"
)
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')


def is_valid_email(email: str) -> bool:
    if not email:
        return False
    e = email.strip().lower()
    if len(e) > 254 or not PATTERN.fullmatch(e):
        return False
    if e.endswith(IMAGE_EXTENSIONS):
        return False
    domain = e.rsplit('@', 1)[1]
    return len(domain) <= 50


def validation_reason(email: str) -> str:
    """Human-readable reason an address was rejected, for the upload report."""
    if not email or not email.strip():
        return 'empty'
    e = email.strip().lower()
    if len(e) > 254:
        return 'too long'
    if e.endswith(IMAGE_EXTENSIONS):
        return 'looks like an image filename, not an address'
    if not PATTERN.fullmatch(e):
        return 'malformed address'
    return 'domain too long'
