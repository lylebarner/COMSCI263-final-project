import requests
from requests.auth import HTTPBasicAuth
import smtplib
from email.mime.text import MIMEText
import time

# Jenkins settings
JENKINS_URL = 'http://your-jenkins-server'
JENKINS_USER = 'jenkins-username'
JENKINS_TOKEN = 'jenkins-api-token'
JOB_NAME = 'your-job-name'

# Email settings
SMTP_SERVER = 'smtp.yourmail.com'
SMTP_PORT = 587
EMAIL_USER = 'your.email@domain.com'
EMAIL_PASS = 'your-email-password'
EMAIL_TO = ['recipient1@domain.com', 'recipient2@domain.com']

def trigger_jenkins_job(job_name, params=None):
    build_url = f"{JENKINS_URL}/job/{job_name}/build"
    if params:
        build_url += "WithParameters"
    response = requests.post(
        build_url,
        auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN),
        params=params,
        timeout=10
    )
    if response.status_code in (200, 201, 202):
        print('Build triggered successfully.')
        queue_url = response.headers.get('Location')
        return queue_url
    else:
        print(f"Failed to trigger build: {response.status_code}, {response.text}")
        return None

def get_build_number_from_queue(queue_url):
    while True:
        queue_response = requests.get(
            f"{queue_url}api/json",
            auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN)
        )
        data = queue_response.json()
        executable = data.get('executable')
        if executable:
            return executable['number']
        print("Waiting for build to start...")
        time.sleep(3)

def get_build_status_and_logs(job_name, build_number):
    api_url = f"{JENKINS_URL}/job/{job_name}/{build_number}/api/json"
    log_url = f"{JENKINS_URL}/job/{job_name}/{build_number}/consoleText"
    resp = requests.get(api_url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN))
    build_data = resp.json()
    building = build_data['building']
    while building:
        print('Build in progress...')
        time.sleep(5)
        resp = requests.get(api_url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN))
        build_data = resp.json()
        building = build_data['building']

    result = build_data['result']
    logs = requests.get(log_url, auth=HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN)).text
    return result, logs

def send_email(subject, body, to_addrs):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_USER
    msg['To'] = ', '.join(to_addrs)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, to_addrs, msg.as_string())

def main():
    print("Triggering Jenkins job...")
    queue_url = trigger_jenkins_job(JOB_NAME)
    if not queue_url:
        return
    print("Fetching build number...")
    build_number = get_build_number_from_queue(queue_url)
    print(f'Build number: {build_number}')
    print('Waiting for build to complete...')
    result, logs = get_build_status_and_logs(JOB_NAME, build_number)
    subject = f'Jenkins Build Result: {JOB_NAME} #{build_number} - {result}'
    body = f'Jenkins Job: {JOB_NAME}\nBuild Number: {build_number}\nResult: {result}\n\nLogs:\n{logs[:3000]}'
    print("Sending email with build results...")
    send_email(subject, body, EMAIL_TO)
    print("Done.")

if __name__ == '__main__':
    main()