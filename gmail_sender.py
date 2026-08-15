"""Gmail SMTP dispatch (Section 9 of the spec)."""
import smtplib
import ssl
import time
from email.message import EmailMessage


def send_campaign(recipients, sender, password, subject, body, attachment_path, delay, cc=''):
    results = []
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        for recipient in recipients:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
            if cc:
                msg['Cc'] = cc
            msg.set_content(body)
            if attachment_path and attachment_path.exists():
                data = attachment_path.read_bytes()
                msg.add_attachment(data, maintype='application', subtype='pdf', filename=attachment_path.name)
            try:
                smtp.send_message(msg)
                results.append((recipient, 'sent', ''))
                time.sleep(delay)
            except smtplib.SMTPServerDisconnected:
                try:
                    smtp.connect('smtp.gmail.com', 465)
                    smtp.login(sender, password)
                    smtp.send_message(msg)
                    results.append((recipient, 'sent', 'reconnected'))
                    time.sleep(delay)
                except Exception as e:
                    results.append((recipient, 'failed', str(e)))
            except Exception as e:
                results.append((recipient, 'failed', str(e)))
    return results
