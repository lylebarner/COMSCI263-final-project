import os
import paramiko
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# Define server and log details
SFTP_HOST = 'sftp.example.com'
SFTP_PORT = 22
USERNAME = 'yourusername'
PASSWORD = 'yourpassword'
LOG_DIRECTORY = '/path/to/logs'
REMOTE_DIRECTORY = '/path/remote/logs'

# Establish an SFTP connection
def create_sftp_client():
    transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
    transport.connect(username=USERNAME, password=PASSWORD)
    sftp = paramiko.SFTPClient.from_transport(transport)
    return sftp

# Upload logs function
def upload_logs():
    sftp = create_sftp_client()
    try:
        # Ensure remote directory exists
        try:
            sftp.stat(REMOTE_DIRECTORY)
        except FileNotFoundError:
            sftp.mkdir(REMOTE_DIRECTORY)

        # Upload files
        for filename in os.listdir(LOG_DIRECTORY):
            if filename.endswith('.log'):  # Checks for log files
                local_path = os.path.join(LOG_DIRECTORY, filename)
                remote_path = os.path.join(REMOTE_DIRECTORY, filename)
                sftp.put(local_path, remote_path)
                print(f"Uploaded {filename} to {REMOTE_DIRECTORY}")
    finally:
        sftp.close()

# Scheduled task setup
scheduler = BlockingScheduler()
scheduler.add_job(upload_logs, 'interval', hours=1)  # Schedule this task to run every hour

# Execution
if __name__ == "__main__":
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass