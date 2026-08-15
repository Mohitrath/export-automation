# Export Manifest — EXPORT Automation System (WSL build)

A runnable implementation of the buyer-outreach pipeline described in the
API 3 documentation, **minus the scraping adapters**. Google/Facebook/
LinkedIn/directory scraping was left out on purpose: harvesting contact
data off those platforms without consent breaks their terms and turns
outreach into unsolicited spam. This version keeps everything else —
CSV lead intake, validation, business/individual classification, Gmail
dispatch with dry-run/live modes and daily caps, duplicate prevention,
logging, and a CSV report — with a proper web UI.

## What's included

| Stage | This build |
|---|---|
| Lead discovery | Manual CSV import (`search/manual_csv.py`) — bring your own leads |
| Extraction | `extraction/data_extractor.py` — normalizes rows into the buyer schema |
| Validation | `validation/email_validator.py` — regex syntax check |
| Classification | `classification/classifier.py` — local pattern matching, no data leaves your machine |
| Outreach | `outreach/gmail_sender.py` — Gmail SMTP, dry-run by default |
| Logging | `app_logging/activity_logger.py` — CSV-backed, powers dedup + reporting |
| Reporting | `reports/report_generator.py` + `/report` and `/download-report` |
| Web UI | Flask app (`app.py`) + Jinja templates in `templates/` |

## 1. Install (WSL / Ubuntu)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
cd ~/export-automation        # wherever you copy this folder to
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

## 2. Configure

Edit `.env`:

```
GMAIL_EMAIL=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password
SEARCH_KEYWORD=Singing Bowls
DAILY_SEND_LIMIT=25
SEND_DELAY_SECONDS=3
PRESENTATION_PATH=assets/company_presentation.pdf
MONITOR_CC=
```

Gmail App Password setup:
1. Enable 2-Step Verification on the sending Gmail account.
2. Google Account → Security → App Passwords.
3. Generate one for "Mail" and paste the 16-character password into `.env`.

Drop your real `assets/company_presentation.pdf` in place of the
placeholder before doing a live send.

## 3. Try it without sending anything

```bash
python main.py import sample_leads.csv
python main.py classify
python main.py send                 # dry run by default
```

## 4. Run the web UI

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser (works fine from WSL — Windows
can reach `localhost` directly).

Pages: Dashboard, Leads (CSV import), Classify, Campaign (compose +
dry-run/live), Report, Settings.

## 5. Go live

Only after you've reviewed a dry run:

```bash
python main.py send --live
```

or flip "Mode" to **Live send** on the Campaign page. Every send is
checked against `data/sent_log.csv` first, so re-running never
double-emails someone.

## Before using this for real commercial campaigns

This is a single-operator tool. It doesn't yet include an unsubscribe
link, consent tracking, or the compliance workflow that CAN-SPAM, GDPR,
or India's IT Act expect from commercial bulk email — add those before
sending to anyone who hasn't explicitly opted in. Only import leads you
have a legitimate basis to contact.
