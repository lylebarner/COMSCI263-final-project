import psycopg2
import subprocess

# Database connection parameters
DATABASE = "your_database_name"
USER = "your_username"
PASSWORD = "your_password"
HOST = "your_host"
PORT = "5432"

# Establishing connection to the database
try:
    conn = psycopg2.connect(
        dbname=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    print("Connected to the database")
except psycopg2.Error as e:
    print("Error connecting to the database:", e)

# Perform database backup using pg_dump utility
backup_path = "path_to_store_backups"
backup_command = f"pg_dump -U {USER} -h {HOST} -p {PORT} {DATABASE} > {backup_path}"
subprocess.run(backup_command, shell=True)

# Close the database connection
conn.close()
print("Backup completed and database connection closed.")