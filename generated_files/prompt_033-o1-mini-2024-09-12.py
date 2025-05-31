import os
import paramiko
import schedule
import time
from datetime import datetime

# Configuration
SFTP_HOST = 'sftp.example.com'
SFTP_PORT = 22
SFTP_USERNAME = 'your_username'
SFTP_PASSWORD = 'your_password'  # Alternatively, use a private key
LOCAL_LOG_DIR = '/path/to/local/logs'
REMOTE_DIR = '/path/to/remote/logs'
UPLOAD_INTERVAL = 60  # in minutes

def upload_logs():
    print(f"Starting upload at {datetime.now()}")
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        if not os.path.exists(LOCAL_LOG_DIR):
            print(f"Local directory {LOCAL_LOG_DIR} does not exist.")
            return
        
        for filename in os.listdir(LOCAL_LOG_DIR):
            local_path = os.path.join(LOCAL_LOG_DIR, filename)
            remote_path = os.path.join(REMOTE_DIR, filename)
            if os.path.isfile(local_path):
                print(f"Uploading {local_path} to {remote_path}")
                sftp.put(local_path, remote_path)
        
        sftp.close()
        transport.close()
        print(f"Upload completed at {datetime.now()}")
    except Exception as e:
        print(f"Error during upload: {e}")

def main():
    schedule.every(UPLOAD_INTERVAL).minutes.do(upload_logs)
    print(f"Scheduled log uploads every {UPLOAD_INTERVAL} minutes.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()