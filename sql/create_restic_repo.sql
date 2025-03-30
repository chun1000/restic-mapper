CREATE TABLE IF NOT EXISTS restic_repo (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE,
last_backup_date TEXT,
restic_path_id INTEGER,
backup_delay_day INTEGER,
keep_policy_id INTEGER,
ignore_policy_id INTEGER,
key_file TEXT,
FOREIGN KEY(restic_path_id) REFERENCES restic_path(id),
FOREIGN KEY(keep_policy_id) REFERENCES keep_policy(id),
FOREIGN KEY(ignore_policy_id) REFERENCES ignore_policy(id)
)