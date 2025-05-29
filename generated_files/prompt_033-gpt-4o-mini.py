import os
import time
import paramiko
from schedule import every, run_pending
from datetime import datetime

# SFTP server credentials
SFTP_HOST = 'your_sftp_server.com'
SFTP_PORT = 22
SFTP_USERNAME = 'your_username'
SFTP_PASSWORD = 'your_password'
LOCAL_LOG_DIR = '/path/to/local/logs'
REMOTE_LOG_DIR = '/path/to/remote/logs'

def upload_logs():
    # Establish SFTP connection
    try:
        transport = paramiko.Transport((SFTP_HOST, SFTP_PORT))
        transport.connect(username=SFTP_USERNAME, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Upload each log file
        for filename in os.listdir(LOCAL_LOG_DIR):
            if filename.endswith('.log'):
                local_filepath = os.path.join(LOCAL_LOG_DIR, filename)
                remote_filepath = os.path.join(REMOTE_LOG_DIR, filename)
                sftp.put(local_filepath, remote_filepath)
                print(f"{datetime.now()}: Uploaded {local_filepath} to {remote_filepath}")

        sftp.close()
        transport.close()

    except Exception as e:
        print(f"Error uploading logs: {e}")

# Schedule the upload every hour
every().hour.at(":00").do(upload_logs)

if __name__ == '__main__':
    while True:
        run_pending()
        time.sleep(60)  # wait one minute before checking again