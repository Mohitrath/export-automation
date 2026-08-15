"""Business / individual segmentation (Section 5.4 of the spec).

The spec calls for routing every address to a third-party LLM for
classification. That means exporting every buyer's email to an external API
just to sort them into two buckets — unnecessary data sharing for a task a
plain heuristic handles well. This uses local pattern matching instead: no
buyer data leaves the machine.
"""
import csv

BUSINESS_LOCAL_PARTS = {
    'info', 'sales', 'contact', 'hello', 'office', 'support', 'admin',
    'business', 'orders', 'enquiries', 'inquiries', 'export', 'import',
    'purchase', 'procurement', 'team', 'accounts', 'marketing',
}


def classify(rows):
    business, individual = [], []
    for r in rows:
        email = (r.get('email') or '').strip().lower()
        if not email or '@' not in email:
            continue
        local = email.split('@')[0]
        is_business = local in BUSINESS_LOCAL_PARTS or any(w in local for w in BUSINESS_LOCAL_PARTS)
        (business if is_business else individual).append(email)
    return sorted(set(business)), sorted(set(individual))


def save(path, emails):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['email'])
        w.writerows([[e] for e in emails])
