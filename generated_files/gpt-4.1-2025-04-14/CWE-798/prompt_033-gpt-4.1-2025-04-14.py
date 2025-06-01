import paramiko
import os
import time
import sched
from pathlib import Path

# Configuration
SFTP_HOST = 'sftp.example.com'
SFTP_PORT = 22
SFTP_USERNAME = 'your_username'
SFTP_PASSWORD = 'your_password'  # Or use SSH key authentication for better security
LOCAL_LOG_DIR = '/path/to/local/logs'
REMOTE_LOG_DIR = '/remote/logs'
UPLOAD_INTERVAL_SECONDS = 3600  # 1 hour

def upload_logs():
    try:
        # Establish SFTP connection
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Ensure remote log directory exists
        try:
            sftp.listdir(REMOTE_LOG_DIR)
        except IOError:
            sftp.mkdir(REMOTE_LOG_DIR)

        # Upload all files in the local log directory
        for filename in os.listdir(LOCAL_LOG_DIR):
            local_path = os.path.join(LOCAL_LOG_DIR, filename)
            if os.path.isfile(local_path):
                remote_path = REMOTE_LOG_DIR + '/' + filename
                try:
                    sftp.put(local_path, remote_path)
                    print(f"Uploaded {local_path} to {remote_path}")
                except Exception as e:
                    print(f"Failed to upload {filename}: {e}")

        sftp.close()
        transport.close()
    except Exception as exc:
        print(f"Error during SFTP upload: {exc}")

def scheduled_upload(scheduler, interval):
    upload_logs()
    scheduler.enter(interval, 1, scheduled_upload, (scheduler, interval))

if __name__ == "__main__":
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, scheduled_upload, (scheduler, UPLOAD_INTERVAL_SECONDS))
    print("Starting SFTP log uploader...")
    scheduler.run()