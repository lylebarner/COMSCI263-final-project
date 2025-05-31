import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from requests.auth import HTTPBasicAuth

# Jenkins settings
JENKINS_URL = 'http://your-jenkins-url'
JENKINS_USER = 'your-username'
JENKINS_TOKEN = 'your-api-token'

# Email settings
SMTP_SERVER = 'smtp.your-email-provider.com'
SMTP_PORT = 587
EMAIL_USER = 'your-email@example.com'
EMAIL_PASSWORD = 'your-email-password'
TO_EMAIL = 'recipient@example.com'

def trigger_job(job_name):
    url = f"{JENKINS_URL}/job/{job_name}/build"
    response = requests.post(url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN))
    return response.status_code

def get_job_logs(job_name, build_number):
    url = f"{JENKINS_URL}/job/{job_name}/{build_number}/consoleText"
    response = requests.get(url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN))
    return response.text

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)

def main(job_name):
    trigger_response = trigger_job(job_name)
    
    if trigger_response == 201:
        print(f"Job '{job_name}' triggered successfully.")
        # Add a sleep or wait mechanism to get the build number and wait for completion

        build_number = 1  # Replace with logic to fetch the latest build number
        logs = get_job_logs(job_name, build_number)
        subject = f"Build Results for {job_name} #{build_number}"
        
        send_email(subject, logs)
        print("Build logs sent via email.")
    else:
        print(f"Failed to trigger job '{job_name}': {trigger_response}")

if __name__ == "__main__":
    main("your-jenkins-job-name")