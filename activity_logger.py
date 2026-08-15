"""Single point of truth for all CSV read/write operations (Section 6)."""
import csv
from pathlib import Path
from datetime import datetime, timezone

BUYER_FIELDS = ['buyer_name', 'company_name', 'email', 'website', 'country', 'source_platform']
SEND_FIELDS = ['email', 'status', 'timestamp', 'error']


def ensure_csv(path: Path, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open('w', newline='', encoding='utf-8') as f:
            csv.DictWriter(f, fieldnames=fields).writeheader()


def append_row(path: Path, fields, row: dict):
    ensure_csv(path, fields)
    with path.open('a', newline='', encoding='utf-8') as f:
        csv.DictWriter(f, fieldnames=fields).writerow(row)


def read_rows(path: Path):
    if not path.exists():
        return []
    with path.open('r', newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def sent_emails(path: Path):
    return {r['email'].strip().lower() for r in read_rows(path) if r.get('status') == 'sent' and r.get('email')}


def log_send(path: Path, email: str, status: str, error: str = ''):
    append_row(path, SEND_FIELDS, {
        'email': email,
        'status': status,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'error': error,
    })
