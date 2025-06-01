import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time

def send_email():
    sender_email = "your_email@example.com"
    receiver_email = "receiver@example.com"
    password = "your_password"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Scheduled Report"

    body = "Hi, this is your requested report. Please find the attached document."
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.example.com", 587)  # SMTP server address and port
        server.starttls()
        server.login(sender_email, password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email successfully sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")

schedule.every().day.at("10:00").do(send_email)

while True:
    schedule.run_pending()
    time.sleep(1)