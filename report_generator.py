"""Builds run summary stats from the send log (Section 5.7 / 7.1)."""


def summarize(rows):
    total = len(rows)
    sent = [r for r in rows if r.get('status') == 'sent']
    failed = [r for r in rows if r.get('status') == 'failed']
    dry_run = [r for r in rows if r.get('status') == 'dry-run']
    rate = (len(sent) / total * 100) if total else 0.0
    return {
        'total': total,
        'sent': len(sent),
        'failed': len(failed),
        'dry_run': len(dry_run),
        'success_rate': round(rate, 2),
        'failed_rows': failed[-25:],
    }
