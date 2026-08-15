"""Lead intake (Section 5.1 stand-in).

The spec describes adapters that scrape Google, Facebook, LinkedIn, and
business directories for buyer emails. That's excluded here: pulling contact
data off social platforms without consent breaks those platforms' terms and
turns outreach into unsolicited harvesting. Instead, leads come from a CSV
the operator supplies themselves — trade-fair badge scans, inbound
inquiries, directory entries they've manually gathered, etc.
"""
import csv

REQUIRED = {'buyer_name', 'company_name', 'email', 'website', 'country', 'source_platform'}


def load_csv(path):
    with open(path, 'r', newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    if rows:
        missing = REQUIRED - set(rows[0].keys())
        if missing:
            raise ValueError(f'Missing columns: {sorted(missing)}')
    return rows
