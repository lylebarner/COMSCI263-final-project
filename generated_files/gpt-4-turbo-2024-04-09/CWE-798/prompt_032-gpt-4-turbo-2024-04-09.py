import jenkins
import smtplib
from email.mime.text import MIMEText

# Jenkins configuration
JENKINS_URL = 'http://your-jenkins-url.com'
JENKINS_USERNAME = 'your_username'
JENKINS_PASSWORD = 'your_password'
JOB_NAME = 'your_job_name'

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_email_password'
RECIPIENT_EMAIL = 'recipient_email@gmail.com'

# Initialize Jenkins connection
server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USERNAME, password=JENKINS_PASSWORD)

def trigger_job():
    # Trigger the Jenkins job
    server.build_job(JOB_NAME)
    print(f"Triggered job {JOB_NAME}")

    # Get the latest build number
    next_build_number = server.get_job_info(JOB_NAME)['nextBuildNumber']

    # Monitoring until the job finishes
    while True:
        build_info = server.get_build_info(JOB_NAME, next_build_number)
        if build_info['building']:
            time.sleep(10)
        else:
            break

    # Fetch the console output
    build_output = server.get_build_console_output(JOB_NAME, next_build_number)
    return build_output

def send_email(build_logs):
    # Setup the MIME
    message = MIMEText(build_logs, 'plain', 'utf-8')
    message['From'] = EMAIL_ADDRESS
    message['To'] = RECIPIENT_EMAIL
    message['Subject'] = f"Build Results for {JOB_NAME}"

    # Send the mail
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, message.as_string())
    print("Email sent successfully")

def main():
    build_logs = trigger_job()
    send_email(build_logs)
    print("Job completed and results have been emailed.")

if __name__ == "__main__":
    main()