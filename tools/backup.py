import os
import shutil
import time

from dotenv import load_dotenv

load_dotenv()
DB_NAME = os.getenv("DB_NAME")

def backup_database(db_path):
    backup_folder = 'backup'
    os.makedirs(backup_folder, exist_ok=True)

    timestamp = int(round(time.time() * 1000))
    new_name = f"backup_{timestamp}.sqlite3"
    backup_filename = os.path.join(backup_folder, new_name)
    
    try:
        shutil.copyfile(db_path, backup_filename)
        print(f"Database backup created: {backup_filename}")
    except Exception as e:
        print(f"Error creating database backup: {e}")

if __name__ == '__main__':
    backup_database('instance/' + DB_NAME)
