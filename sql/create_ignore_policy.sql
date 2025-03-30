CREATE TABLE IF NOT EXISTS ignore_policy (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE,
exclude_file TEXT,
iexclude_file TEXT,
exclude_larger_than INTEGER
)