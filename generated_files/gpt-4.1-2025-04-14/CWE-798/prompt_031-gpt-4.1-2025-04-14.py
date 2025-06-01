import os
import subprocess
import datetime
import time

# Connection parameters
DB_HOST = "your_host"
DB_PORT = "5432"
DB_NAME = "your_db"
DB_USER = "your_user"
DB_PASSWORD = "your_password"

# Backup settings
BACKUP_DIR = "/path/to/backup/dir"
BACKUP_INTERVAL_SECONDS = 24 * 60 * 60  # Every 24 hours

os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_database():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"{DB_NAME}_backup_{timestamp}.sql")
    env = os.environ.copy()
    env["PGPASSWORD"] = DB_PASSWORD

    cmd = [
        "pg_dump",
        "-h", DB_HOST,
        "-p", DB_PORT,
        "-U", DB_USER,
        "-F", "c",      # custom format
        "-b",           # include large objects
        "-v",           # verbose
        "-f", backup_file,
        DB_NAME
    ]

    print(f"Backing up database to {backup_file} ...")
    try:
        result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
        print("Backup successful:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Backup failed:", e.stderr)
    finally:
        # Remove password from env for safety
        env["PGPASSWORD"] = ""

if __name__ == "__main__":
    while True:
        backup_database()
        print(f"Next backup in {BACKUP_INTERVAL_SECONDS} seconds.\n")
        time.sleep(BACKUP_INTERVAL_SECONDS)
