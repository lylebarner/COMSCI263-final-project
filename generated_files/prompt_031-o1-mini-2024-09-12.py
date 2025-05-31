import subprocess
import datetime
import time
import os

# Connection parameters
DB_HOST = 'your_host'
DB_PORT = '5432'
DB_NAME = 'your_database'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'

# Backup settings
BACKUP_DIR = 'backups'
BACKUP_INTERVAL = 24 * 60 * 60  # in seconds (e.g., 24 hours)

def perform_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'{DB_NAME}_backup_{timestamp}.sql')
    
    env = os.environ.copy()
    env['PGPASSWORD'] = DB_PASSWORD
    
    command = [
        'pg_dump',
        '-h', DB_HOST,
        '-p', DB_PORT,
        '-U', DB_USER,
        '-F', 'c',
        '-b',
        '-v',
        '-f', backup_file,
        DB_NAME
    ]
    
    try:
        subprocess.check_call(command, env=env)
        print(f'Backup successful: {backup_file}')
    except subprocess.CalledProcessError as e:
        print(f'Backup failed: {e}')

def main():
    while True:
        perform_backup()
        time.sleep(BACKUP_INTERVAL)

if __name__ == '__main__':
    main()