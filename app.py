import csv

from flask import Flask, request, redirect, url_for, render_template, flash, send_file

from config import (
    SECRET_KEY, SEARCH_KEYWORD, DAILY_SEND_LIMIT, SEND_DELAY_SECONDS,
    GMAIL_EMAIL, GMAIL_APP_PASSWORD, PRESENTATION_PATH, MONITOR_CC,
    DATA_DIR, BUYERS_CSV, SENT_LOG_CSV, BUSINESS_CSV, INDIVIDUAL_CSV,
)
from main import ensure_data, import_leads, classify_leads, campaign
from app_logging.activity_logger import read_rows, sent_emails
from reports.report_generator import summarize

app = Flask(__name__)
app.secret_key = SECRET_KEY

DEFAULT_SUBJECT = f'{SEARCH_KEYWORD} — Export Presentation'
DEFAULT_BODY = 'Hello,\n\nPlease find our company presentation attached.\n\nRegards'


@app.context_processor
def inject_globals():
    return {'search_keyword': SEARCH_KEYWORD}


def _counts():
    buyers = read_rows(BUYERS_CSV)
    business = read_rows(BUSINESS_CSV)
    individual = read_rows(INDIVIDUAL_CSV)
    sent = sent_emails(SENT_LOG_CSV)
    return {
        'buyer_count': len(buyers),
        'business_count': len(business),
        'individual_count': len(individual),
        'sent_count': len(sent),
    }


@app.route('/')
def home():
    ensure_data()
    c = _counts()
    return render_template(
        'home.html', active='home',
        gmail_ready=bool(GMAIL_EMAIL and GMAIL_APP_PASSWORD),
        daily_limit=DAILY_SEND_LIMIT, send_delay=SEND_DELAY_SECONDS, **c,
    )


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    ensure_data()
    if request.method == 'POST':
        f = request.files.get('file')
        if not f or not f.filename:
            flash('Choose a CSV file first.', 'error')
            return redirect(url_for('upload'))
        tmp = DATA_DIR / 'upload_tmp.csv'
        f.save(tmp)
        try:
            result = import_leads(tmp)
            flash(
                f"Imported {result['imported']} new leads "
                f"({result['duplicate']} duplicate, {result['invalid']} invalid skipped).",
                'success',
            )
        except ValueError as e:
            flash(str(e), 'error')
        finally:
            tmp.unlink(missing_ok=True)
        return redirect(url_for('upload'))
    buyers = read_rows(BUYERS_CSV)
    return render_template('upload.html', active='upload', buyers=buyers)


@app.route('/classify', methods=['GET', 'POST'])
def cl():
    ensure_data()
    ran = False
    if request.method == 'POST':
        classify_leads()
        ran = True
    business = [r['email'] for r in read_rows(BUSINESS_CSV)]
    individual = [r['email'] for r in read_rows(INDIVIDUAL_CSV)]
    return render_template(
        'classify.html', active='classify', ran=ran,
        business_emails=business, individual_emails=individual,
        business_count=len(business), individual_count=len(individual),
    )


@app.route('/send', methods=['GET', 'POST'])
def send():
    ensure_data()
    c = _counts()
    results, was_live = None, False
    if request.method == 'POST':
        live = request.form.get('live') == 'yes'
        audience = request.form.get('audience', 'all')
        subject = request.form.get('subject') or DEFAULT_SUBJECT
        body = request.form.get('body') or DEFAULT_BODY
        try:
            results = campaign(subject, body, audience, live)
            was_live = live
            label = 'Live send' if live else 'Dry run'
            flash(f'{label} complete — {len(results)} recipient(s) processed.', 'success')
        except Exception as e:
            flash(str(e), 'error')
    return render_template(
        'send.html', active='send', results=results, was_live=was_live,
        default_subject=DEFAULT_SUBJECT, default_body=DEFAULT_BODY,
        daily_limit=DAILY_SEND_LIMIT, **c,
    )


@app.route('/report')
def report():
    ensure_data()
    rows = read_rows(SENT_LOG_CSV)
    summary = summarize(rows)
    return render_template('report.html', active='report', summary=summary, rows=rows)


@app.route('/settings')
def settings():
    return render_template(
        'settings.html', active='settings',
        gmail_ready=bool(GMAIL_EMAIL and GMAIL_APP_PASSWORD), gmail_email=GMAIL_EMAIL,
        search_keyword=SEARCH_KEYWORD, daily_limit=DAILY_SEND_LIMIT,
        send_delay=SEND_DELAY_SECONDS, presentation_path=PRESENTATION_PATH,
        presentation_exists=PRESENTATION_PATH.exists(), monitor_cc=MONITOR_CC,
    )


@app.route('/download-report')
def download():
    ensure_data()
    out = DATA_DIR / 'report.csv'
    rows = read_rows(SENT_LOG_CSV)
    with out.open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['email', 'status', 'timestamp', 'error'])
        for r in rows:
            w.writerow([r.get('email'), r.get('status'), r.get('timestamp'), r.get('error')])
    return send_file(out, as_attachment=True, download_name='campaign_report.csv')


if __name__ == '__main__':
    ensure_data()
    app.run(host='127.0.0.1', port=5000, debug=True)
