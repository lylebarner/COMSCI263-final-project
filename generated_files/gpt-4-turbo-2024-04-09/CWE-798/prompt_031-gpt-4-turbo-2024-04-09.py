import psycopg2
from datetime import datetime
import os
import subprocess

# Database connection parameters
HOST = "your_host"
DATABASE = "your_database"
USER = "your_username"
PASSWORD = "your_password"
PORT = "your_port"

# Directory to store backups
BACKUP_DIR = "/path/to/your/backup/directory"

def connect_to_database():
    try:
        conn = psycopg2.connect(
            host=HOST,
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT
        )
        return conn
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None

def backup_database(connection):
    if connection is not None:
        # Generate a timestamped backup file name
        backup_file = f"{DATABASE}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
        backup_path = os.path.join(BACKUP_DIR, backup_file)

        # Command to perform backup
        backup_command = f"pg_dump -h {HOST} -U {USER} -d {DATABASE} -p {PORT} -F c -b -v -f '{backup_path}'"
        
        try:
            # Run the backup command
            subprocess.run(backup_command, shell=True, check=True)
            print(f"Database backup successful. Backup created at {backup_path}")
        except Exception as error:
            print(f"Failed to backup database: {error}")

def main():
    # Connect to the PostgreSQL database
    connection = connect_to_database()

    # Perform the backup
    backup_database(connection)

    # Close database connection
    if connection:
        connection.close()

if __name__ == '__main__':
    main()