import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# -------- EMAIL CONFIGURATION --------
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'  # Use app password if 2FA is enabled
RECIPIENT_EMAIL = 'recipient@example.com'
# --------------------------------------

def create_report():
    # Prepare your report here (can be dynamic)
    report = "Scheduled Report\n\nThis is your scheduled email report."
    return report

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        print(f"Email sent to {RECIPIENT_EMAIL}.")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()

def job():
    report = create_report()
    send_email("Your Scheduled Report", report)

# Schedule the job here: every day at 9:00 AM
schedule.every().day.at("09:00").do(job)

print("Scheduler started. Waiting to send scheduled reports...")
while True:
    schedule.run_pending()
    time.sleep(60)
