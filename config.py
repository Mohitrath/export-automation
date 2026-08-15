import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', '')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', '')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
SEARCH_KEYWORD = os.getenv('SEARCH_KEYWORD', 'Singing Bowls')
DAILY_SEND_LIMIT = int(os.getenv('DAILY_SEND_LIMIT', '25'))
SEND_DELAY_SECONDS = float(os.getenv('SEND_DELAY_SECONDS', '3'))
PRESENTATION_PATH = BASE_DIR / os.getenv('PRESENTATION_PATH', 'assets/company_presentation.pdf')
MONITOR_CC = os.getenv('MONITOR_CC', '')

DATA_DIR = BASE_DIR / 'data'
BUYERS_CSV = DATA_DIR / 'buyers.csv'
SENT_LOG_CSV = DATA_DIR / 'sent_log.csv'
BUSINESS_CSV = DATA_DIR / 'business_emails.csv'
INDIVIDUAL_CSV = DATA_DIR / 'individual_emails.csv'
