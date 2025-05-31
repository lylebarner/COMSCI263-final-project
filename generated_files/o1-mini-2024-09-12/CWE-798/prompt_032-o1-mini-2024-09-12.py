import jenkins
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

# Jenkins Configuration
JENKINS_URL = 'http://your-jenkins-url'
JENKINS_USER = 'your-username'
JENKINS_API_TOKEN = 'your-api-token'
JOB_NAME = 'your-job-name'

# Email Configuration
SMTP_SERVER = 'smtp.your-email.com'
SMTP_PORT = 587
EMAIL_USER = 'your-email@example.com'
EMAIL_PASSWORD = 'your-email-password'
EMAIL_FROM = 'your-email@example.com'
EMAIL_TO = 'recipient@example.com'
EMAIL_SUBJECT = f'Jenkins Job "{JOB_NAME}" Build Result'

def trigger_job(server, job_name):
    queue_id = server.build_job(job_name)
    print(f'Job "{job_name}" triggered with queue ID {queue_id}')
    return queue_id

def get_build_number(server, job_name, queue_id):
    while True:
        queue_item = server.get_queue_item(queue_id)
        if 'executable' in queue_item:
            build_number = queue_item['executable']['number']
            print(f'Build number {build_number} started for job "{job_name}"')
            return build_number
        print('Waiting for build to start...')
        time.sleep(5)

def get_build_info(server, job_name, build_number):
    while True:
        build_info = server.get_build_info(job_name, build_number)
        if build_info['building']:
            print(f'Build {build_number} is still running...')
            time.sleep(5)
        else:
            print(f'Build {build_number} completed with status: {build_info["result"]}')
            return build_info

def get_build_log(server, job_name, build_number):
    log = server.get_build_console_output(job_name, build_number)
    return log

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server_email:
        server_email.starttls()
        server_email.login(EMAIL_USER, EMAIL_PASSWORD)
        server_email.send_message(msg)
        print('Email sent successfully.')

def main():
    server = jenkins.Jenkins(JENKINS_URL, username=JENKINS_USER, password=JENKINS_API_TOKEN)
    print('Connected to Jenkins.')

    queue_id = trigger_job(server, JOB_NAME)
    build_number = get_build_number(server, JOB_NAME, queue_id)
    build_info = get_build_info(server, JOB_NAME, build_number)
    log = get_build_log(server, JOB_NAME, build_number)

    email_body = f"Jenkins Job: {JOB_NAME}\nBuild Number: {build_number}\nStatus: {build_info['result']}\n\nConsole Output:\n{log}"
    send_email(EMAIL_SUBJECT, email_body)

if __name__ == '__main__':
    main()