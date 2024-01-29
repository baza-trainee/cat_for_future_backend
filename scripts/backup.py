import os
from datetime import datetime
import shutil

DB_CONTAINER = "postgres_cats"
WEB_CONTAINER = "backend_cats"
MAX_BACKUPS = 3

BACKUP_DIR = "backup-postgres"
STATIC_BACKUP_DIR = "backup-media"
TIME_FORMAT = "%Y%m%d_%H%M%S"
TIMESTAMP = datetime.now().strftime(TIME_FORMAT)
BACKUP_PATH = os.path.join(BACKUP_DIR, f"backup_{TIMESTAMP}.sql")
STATIC_BACKUP_PATH = os.path.join(STATIC_BACKUP_DIR, f"static_{TIMESTAMP}")

env_file_path = ".env"
config = dict()
if os.path.exists(env_file_path):
    with open(env_file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key] = value

DATABASE_URI = config.get("DATABASE_URI")

os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(STATIC_BACKUP_DIR, exist_ok=True)

cmd_db = f"docker exec {DB_CONTAINER} pg_dump {DATABASE_URI} > {BACKUP_PATH}"
cmd_static = f"docker cp {WEB_CONTAINER}:/backend_app/calendarapi/static/media {STATIC_BACKUP_PATH}"

os.system(cmd_db)
os.system(cmd_static)

backup_list = os.listdir(BACKUP_DIR)
if len(backup_list) > MAX_BACKUPS:
    old_backup = sorted(
        backup_list, key=lambda x: datetime.strptime(x, f"backup_{TIME_FORMAT}.sql")
    )[0]
    os.remove(os.path.join(BACKUP_DIR, old_backup))

static_backup_list = os.listdir(STATIC_BACKUP_DIR)
if len(static_backup_list) > MAX_BACKUPS:
    old_static_backup = sorted(
        static_backup_list, key=lambda x: datetime.strptime(x, f"static_{TIME_FORMAT}")
    )[0]
    shutil.rmtree(os.path.join(STATIC_BACKUP_DIR, old_static_backup))
