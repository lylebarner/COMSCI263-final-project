# Dependencies: paramiko (pip install paramiko)
import paramiko
import schedule
import time

def upload_logs():
    sftp_host = 'sftp.example.com'
    sftp_port = 22
    sftp_username = 'username'
    sftp_password = 'password'
    local_log_path = '/path/to/local/logs'
    remote_log_path = '/path/to/remote/logs'

    transport = paramiko.Transport((sftp_host, sftp_port))
    transport.connect(username=sftp_username, password=sftp_password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    for log_file in os.listdir(local_log_path):
        local_file_path = os.path.join(local_log_path, log_file)
        remote_file_path = os.path.join(remote_log_path, log_file)
        sftp.put(local_file_path, remote_file_path)

    sftp.close()
    transport.close()

schedule.every().hour.do(upload_logs)

while True:
    schedule.run_pending()
    time.sleep(1)