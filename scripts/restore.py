from datetime import datetime
import os

DB_CONTAINER = "postgres_advokato"
WEB_CONTAINER = "backend_advokato"

BACKUP_DIR = "backup-postgres-advokato"
STATIC_BACKUP_DIR = "backup-static-advokato"

TIME_FORMAT = "%Y%m%d_%H%M%S"

env_file_path = ".env"
config = dict()
if os.path.exists(env_file_path):
    with open(env_file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "=" in line and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key] = value

DB_USER = config.get("POSTGRES_USER")
DB_PASS = config.get("POSTGRES_PASSWORD")
DB_NAME = config.get("POSTGRES_DB")
DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@postgres:5432/{DB_NAME}"

if not os.path.exists(BACKUP_DIR):
    print("Backup directory does not exist. Exiting.")
    exit(1)

BACKUPS = sorted(
    os.listdir(BACKUP_DIR),
    key=lambda x: datetime.strptime(x, f"backup_{TIME_FORMAT}.sql"),
    reverse=True,
)
BACKUPS_STATIC = sorted(
    os.listdir(STATIC_BACKUP_DIR),
    key=lambda x: datetime.strptime(x, f"static_{TIME_FORMAT}"),
    reverse=True,
)

if not BACKUPS:
    print("No backup files found in the directory. Exiting.")
    exit(1)

print("Оберіть backup-файл зі списку, для відновлення бази даних. Введіть цифру:")
for i, backup in enumerate(BACKUPS, start=1):
    print(f"{i} - {backup}")

choice = int(input("Ваш вибір: "))

# db
os.system(
    f"docker exec {DB_CONTAINER} psql {DATABASE_URI} -c 'DROP SCHEMA public CASCADE;'"
)
os.system(f"docker exec {DB_CONTAINER} psql {DATABASE_URI} -c 'CREATE SCHEMA public;'")
os.system(
    f"docker exec -i {DB_CONTAINER} psql {DATABASE_URI} < {BACKUP_DIR}/{BACKUPS[choice - 1]}"
)

# media
os.system(f"sudo rm -rf calendarapi/static/media")
os.system(
    f"cd {STATIC_BACKUP_DIR}/{BACKUPS_STATIC[choice - 1]} && docker cp . {WEB_CONTAINER}:/backend_app/calendarapi/static/media/"
)
