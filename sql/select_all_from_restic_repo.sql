SELECT id, name, last_backup_date, restic_path_id, 
backup_dir, backup_delay_day, keep_policy_id,
byte_compressed, byte_raw, ignore_policy_id
FROM restic_repo