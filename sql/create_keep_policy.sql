CREATE TABLE IF NOT EXISTS keep_policy (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT UNIQUE,
keep_last INTEGER, 
keep_hourly INTEGER, 
keep_daily INTEGER, 
keep_weekly INTEGER, 
keep_monthly INTEGER, 
keep_yearly INTEGER,
keep_within TEXT
)