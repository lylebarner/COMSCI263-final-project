import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SMTP_SERVER = 'smtp.example.com'  # Replace with your SMTP server
SMTP_PORT = 587  # Replace with your SMTP port
USERNAME = 'your_email@example.com'  # Replace with your email
PASSWORD = 'your_password'  # Replace with your email password
RECIPIENT_EMAIL = 'recipient@example.com'  # Replace with recipient's email

def send_report():
    # Create a multipart email message
    msg = MIMEMultipart()
    msg['From'] = USERNAME
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = 'Scheduled Report'

    # Email body content
    body = "This is your scheduled report."
    msg.attach(MIMEText(body, 'plain'))

    # Send email using SMTP
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(USERNAME, PASSWORD)  # Authenticate
            server.send_message(msg)  # Send email
            print("Report sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Schedule to send the report every day at 9 AM
schedule.every().day.at("09:00").do(send_report)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute