import os
import subprocess
import datetime
import psycopg2

# Connection parameters
HOST = 'your_host'
PORT = 'your_port'
DATABASE = 'your_database'
USER = 'your_username'
PASSWORD = 'your_password'

def backup_database():
    # Create a backup filename based on the current date and time
    backup_filename = f"{DATABASE}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    
    # Construct the pg_dump command
    command = f"pg_dump -h {HOST} -p {PORT} -U {USER} -W {PASSWORD} -F c -b -v -f {backup_filename} {DATABASE}"
    
    try:
        # Execute the backup command
        subprocess.run(command, shell=True, check=True)
        print(f"Backup of '{DATABASE}' completed successfully: {backup_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")

if __name__ == "__main__":
    # Request password from user (to avoid storing it in plaintext)
    os.environ["PGPASSWORD"] = PASSWORD
    backup_database()