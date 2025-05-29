import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email server configurations
email_host = 'smtp.example.com'
email_port = 587
email_username = 'your_email@example.com'
email_password = 'your_email_password'

# Email content
report_subject = 'Daily Report'
report_body = 'This is the daily report content.'

# Email addresses
from_email = 'your_email@example.com'
to_email = 'recipient@example.com'

# Create message
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = to_email
msg['Subject'] = report_subject
msg.attach(MIMEText(report_body, 'plain'))

# Connect to server and send email
try:
    server = smtplib.SMTP(email_host, email_port)
    server.starttls()
    server.login(email_username, email_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()
    print("Report sent successfully!")
except Exception as e:
    print(f"An error occurred: {str(e)}")