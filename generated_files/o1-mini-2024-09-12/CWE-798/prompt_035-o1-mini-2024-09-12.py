import smtplib
from email.mime.text import MIMEText
import schedule
import time

# Email configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
USERNAME = 'your_username'
PASSWORD = 'your_password'
FROM_EMAIL = 'from@example.com'
TO_EMAIL = 'to@example.com'
SUBJECT = 'Scheduled Report'
BODY = 'This is your scheduled report.'

def send_email():
    msg = MIMEText(BODY)
    msg['Subject'] = SUBJECT
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(USERNAME, PASSWORD)
        server.send_message(msg)
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')

# Schedule the report to be sent every day at 9:00 AM
schedule.every().day.at("09:00").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(60)