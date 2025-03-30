CREATE TABLE IF NOT EXISTS restic_repo (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE,
last_backup_date TEXT,
restic_path_id INTEGER,
backup_dir TEXT,
backup_delay_day INTEGER,
keep_policy_id INTEGER,
byte_compressed TEXT,
byte_raw TEXT,
ignore_policy_id INTEGER,
FOREIGN KEY(restic_path_id) REFERENCES restic_path(id),
FOREIGN KEY(keep_policy_id) REFERENCES keep_policy(id),
FOREIGN KEY(ignore_policy_id) REFERENCES ignore_policy(id)
)