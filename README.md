# 🚀 Export Automation

> **A Python + Flask automation platform for lead management, validation, classification, outreach, and reporting.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20App-black?logo=flask)](https://flask.palletsprojects.com/)
[![Gmail SMTP](https://img.shields.io/badge/Gmail-SMTP-red?logo=gmail)](https://support.google.com/mail/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Export Automation is a lightweight, modular lead-processing and outreach system built with **Python and Flask**. It takes lead data from CSV files, normalizes and validates it, classifies contacts, prevents duplicate outreach, supports Gmail-based email campaigns, and generates reports through both a CLI and web dashboard.

The project is designed to run locally, including on **WSL/Ubuntu**, and keeps sensitive configuration in environment variables.

---

## ✨ Features

- 📥 **CSV Lead Import** — import and normalize lead lists
- 🔎 **Email Validation** — validate email syntax before outreach
- 🏷️ **Lead Classification** — classify businesses and individuals using local rules
- 📧 **Gmail Outreach** — send personalized emails through Gmail SMTP
- 🧪 **Dry-Run Mode** — test campaigns without sending real emails
- 🛡️ **Duplicate Protection** — avoid sending repeatedly to the same lead
- ⏱️ **Daily Send Limits** — control campaign volume
- 📝 **Activity Logging** — keep a CSV-backed record of processing and outreach
- 📊 **Reporting** — generate campaign and lead reports
- 🌐 **Flask Dashboard** — manage leads, campaigns, reports, and settings from a browser
- 🖥️ **WSL Compatible** — designed to run smoothly on Windows + WSL/Ubuntu
- 🔐 **Environment Configuration** — credentials stay outside the source code

---

## 🏗️ Architecture

```text
                    ┌──────────────────┐
                    │   CSV Lead Data  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Extraction    │
                    │  & Normalization │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Validation    │
                    │  Email / Fields  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Classification   │
                    │ Business / Person│
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Outreach Engine  │
                    │ Gmail / Dry Run  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Logging & Reports│
                    └──────────────────┘
```

---

## 📁 Project Structure

```text
export-automation/
│
├── app.py                         # Flask web application
├── main.py                        # CLI entry point
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules
│
├── app_logging/
│   └── activity_logger.py         # Activity and outreach logging
│
├── extraction/
│   └── data_extractor.py          # Lead normalization/extraction
│
├── classification/
│   └── classifier.py              # Lead classification rules
│
├── validation/
│   └── email_validator.py         # Email validation
│
├── search/
│   └── manual_csv.py              # CSV-based lead intake
│
├── outreach/
│   └── gmail_sender.py             # Gmail SMTP sender
│
├── reports/
│   └── report_generator.py         # Report generation
│
├── templates/                     # Flask/Jinja templates
├── static/                        # CSS/JS/static assets
├── data/                          # Runtime data and logs
└── sample_leads.csv               # Example input data
```

---

## ⚙️ Requirements

- Python **3.10+**
- pip
- Git
- WSL 2 + Ubuntu (recommended on Windows)
- Gmail account with **2-Step Verification** and an **App Password** for live email sending

---

## 🐧 Installation on WSL / Ubuntu

### 1. Clone the repository

```bash
git clone https://github.com/Mohitrath/export-automation.git
cd export-automation
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create your environment file

```bash
cp .env.example .env
```

Edit it with:

```bash
nano .env
```

Example configuration:

```env
GMAIL_EMAIL=your_gmail@gmail.com
GMAIL_APP_PASSWORD=your_16_character_app_password
SECRET_KEY=your_secret_key
SEARCH_KEYWORD=Siming Bowls
DAILY_SEND_LIMIT=25
SEND_DELAY_SECONDS=3
PRESENTATION_PATH=assets/company_presentation.pdf
MONITOR_CC=
```

> ⚠️ **Never commit `.env` to GitHub.** It may contain credentials and secret keys. The project `.gitignore` is configured to keep it out of Git.

---

## 🔐 Gmail App Password

For live email delivery, use a Google **App Password**, not your normal Gmail password.

1. Enable 2-Step Verification on your Google account.
2. Open your Google Account security settings.
3. Create an App Password for the application.
4. Put the generated password in `.env` as `GMAIL_APP_PASSWORD`.

For development and testing, use **dry-run mode** so that no real emails are sent.

---

## 🧪 Run in Dry-Run Mode

Import the sample leads:

```bash
python main.py import sample_leads.csv
```

Classify the leads:

```bash
python main.py classify
```

Run the outreach pipeline without sending real emails:

```bash
python main.py send
```

Dry-run mode is recommended before any live campaign.

---

## 🌐 Start the Web Dashboard

Run:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

On Windows + WSL, you can normally open the address directly in your Windows browser.

### Dashboard capabilities

| Section | Purpose |
|---|---|
| Dashboard | Overview of leads and campaign activity |
| Leads | Import and manage CSV leads |
| Classify | Process and classify leads |
| Campaign | Compose and test outreach campaigns |
| Report | View/export campaign results |
| Settings | Manage application configuration |

---

## 🚀 Live Email Sending

**Do not enable live sending until you have reviewed the dry-run output and confirmed your recipient list.**

CLI:

```bash
python main.py send --live
```

The application uses the configured daily limit and records activity to help prevent duplicate outreach.

---

## 📊 Reporting

The project maintains CSV-backed activity data and provides reporting through the Flask interface.

Typical workflow:

```text
Import → Validate → Classify → Dry Run → Review → Send → Report
```

---

## 🛡️ Privacy & Security

This project is intended to run locally and does not require sending lead data to an external classification service.

Security recommendations:

- Never commit `.env` or credentials.
- Never publish Gmail App Passwords.
- Use dry-run mode while developing.
- Keep campaign limits conservative.
- Only contact people/businesses where you have a legitimate basis to do so.
- Add appropriate consent/unsubscribe and applicable legal compliance workflows before commercial bulk outreach.

---

## 🧩 Technology Stack

| Technology | Role |
|---|---|
| **Python** | Core application logic |
| **Flask** | Web dashboard and HTTP routes |
| **Jinja2** | HTML templates |
| **SMTP / Gmail** | Email delivery |
| **CSV** | Lead storage and activity logs |
| **python-dotenv** | Environment configuration |
| **WSL / Ubuntu** | Local Linux development environment |

---

## 🔮 Future Improvements

- [ ] Database support with PostgreSQL/SQLite
- [ ] Authentication and user accounts
- [ ] Advanced lead scoring
- [ ] Campaign analytics and charts
- [ ] Email templates and personalization variables
- [ ] Unsubscribe and consent management
- [ ] Scheduled campaigns
- [ ] Background job processing
- [ ] Docker support
- [ ] Automated tests and CI/CD

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome.

```bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

Then open a pull request on GitHub.

---

## 📄 License

This project is released under the **MIT License**.

---

## 👨‍💻 Author

**Mohit Kumar**

GitHub: [@Mohitrath](https://github.com/Mohitrath)

---

⭐ If this project helped you, consider giving the repository a star!
