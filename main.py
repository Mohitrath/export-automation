from pathlib import Path
import argparse

from config import (
    DATA_DIR, BUYERS_CSV, SENT_LOG_CSV, BUSINESS_CSV, INDIVIDUAL_CSV,
    GMAIL_EMAIL, GMAIL_APP_PASSWORD, PRESENTATION_PATH, DAILY_SEND_LIMIT,
    SEND_DELAY_SECONDS, MONITOR_CC,
)
from search.manual_csv import load_csv
from extraction.data_extractor import normalize_record
from app_logging.activity_logger import (
    ensure_csv, append_row, read_rows, sent_emails, log_send, BUYER_FIELDS, SEND_FIELDS,
)
from classification.classifier import classify, save
from outreach.gmail_sender import send_campaign


def ensure_data():
    DATA_DIR.mkdir(exist_ok=True)
    ensure_csv(BUYERS_CSV, BUYER_FIELDS)
    ensure_csv(SENT_LOG_CSV, SEND_FIELDS)


def import_leads(file):
    ensure_data()
    rows = load_csv(Path(file))
    existing = {r['email'].lower() for r in read_rows(BUYERS_CSV)}
    imported, skipped_invalid, skipped_dupe = 0, 0, 0
    for raw in rows:
        r = normalize_record(raw)
        if not r:
            skipped_invalid += 1
            continue
        if r['email'] in existing:
            skipped_dupe += 1
            continue
        append_row(BUYERS_CSV, BUYER_FIELDS, r)
        existing.add(r['email'])
        imported += 1
    return {'imported': imported, 'invalid': skipped_invalid, 'duplicate': skipped_dupe}


def classify_leads():
    ensure_data()
    business, individual = classify(read_rows(BUYERS_CSV))
    save(BUSINESS_CSV, business)
    save(INDIVIDUAL_CSV, individual)
    return len(business), len(individual)


def _audience_emails(audience):
    if audience == 'business':
        return [r['email'] for r in read_rows(BUSINESS_CSV)]
    if audience == 'individual':
        return [r['email'] for r in read_rows(INDIVIDUAL_CSV)]
    return [r['email'] for r in read_rows(BUYERS_CSV)]


def campaign(subject, body, audience='all', live=False):
    ensure_data()
    already_sent = sent_emails(SENT_LOG_CSV)
    candidates = [e.lower() for e in _audience_emails(audience) if e]
    recipients = [e for e in dict.fromkeys(candidates) if e not in already_sent][:DAILY_SEND_LIMIT]

    if not live:
        return [(e, 'dry-run', 'not sent') for e in recipients]

    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        raise RuntimeError('Set GMAIL_EMAIL and GMAIL_APP_PASSWORD in .env before a live send.')
    if not PRESENTATION_PATH.exists():
        raise FileNotFoundError(f'Missing presentation file at {PRESENTATION_PATH}')
    if not recipients:
        return []

    results = send_campaign(
        recipients, GMAIL_EMAIL, GMAIL_APP_PASSWORD, subject, body,
        PRESENTATION_PATH, SEND_DELAY_SECONDS, cc=MONITOR_CC,
    )
    for email, status, error in results:
        log_send(SENT_LOG_CSV, email, status, error)
    return results


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='EXPORT Automation System')
    sub = p.add_subparsers(dest='cmd')

    a = sub.add_parser('import')
    a.add_argument('csv')

    sub.add_parser('classify')

    a = sub.add_parser('send')
    a.add_argument('--live', action='store_true')
    a.add_argument('--audience', choices=['all', 'business', 'individual'], default='all')
    a.add_argument('--subject', default='Singing Bowls Export Presentation')
    a.add_argument('--body', default='Hello,\n\nPlease find our company presentation attached.\n\nRegards')

    args = p.parse_args()
    ensure_data()

    if args.cmd == 'import':
        print('Import result:', import_leads(args.csv))
    elif args.cmd == 'classify':
        b, i = classify_leads()
        print(f'Business: {b} | Individual: {i}')
    elif args.cmd == 'send':
        r = campaign(args.subject, args.body, args.audience, args.live)
        print('Processed:', len(r))
        for row in r:
            print(row)
    else:
        p.print_help()
