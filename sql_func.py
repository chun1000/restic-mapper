import sqlite3
import pandas as pd
import os
import re
from keep_policy import KeepPolicy

DB_PATH = "restic-meta.db"
DATE_TIME_FORMAT = "%Y-%m-%d"


def read_sql_file(file_name: str):
    SQL_FOLDER_DIR = "sql/"
    with open(SQL_FOLDER_DIR + file_name, "r") as f:
        return f.read()


class ResticSql:
    def __init__(self):
        self.con = con = sqlite3.connect(DB_PATH)
        con.execute(read_sql_file("create_keep_policy.sql"))
        con.execute(read_sql_file("create_path_info.sql"))
        con.execute(read_sql_file("create_restic_repo.sql"))
        con.execute(read_sql_file("create_ignore_policy.sql"))   

    def __del__(self):
        self.con.close()

    def get_all_path_info(self) -> pd.DataFrame:
        df = pd.read_sql("SELECT * FROM path_info", self.con)
        return df

    def insert_path_info(self, name: str, path: str):
        if not os.path.exists(path):
            print("The directory not exists.")
            return
        sql_cmd = f"INSERT INTO path_info (name, path) VALUES ('{name}', '{path}')"
        self.con.execute(sql_cmd)
        self.con.commit()

    def get_all_keep_policy(self) -> pd.DataFrame:
        sql_cmd = "SELECT * FROM keep_policy"
        return pd.read_sql(sql_cmd, self.con)

    def insert_keep_policy(self, keep_policy: KeepPolicy):
        
        sql_cmd = f"INSERT INTO keep_policy {keep_policy.get_header()} VALUES {keep_policy.get_values()}"
        self.con.execute(sql_cmd)
        self.con.commit()
        
        
    
    def get_all_ignore_policy(self) -> pd.DataFrame:
        sql_cmd = "SELECT * FROM ignore_policy"
        return pd.read_sql(sql_cmd, self.con)
    
    
    
    def insert_ignore_policy(self, name: str, exclude: str, iexclude: str, exclude_larger_than : str):
        if exclude != None and not os.path.exists(exclude):
            print("The exclude file not exists.")
            return
        if iexclude != None and not os.path.exists(iexclude):
            print("The iexclude file not exists.")
            return
        if exclude_larger_than != None:
            pattern = r"(?i)^(\d+)(k|m|g|t)$"
            if not re.match(pattern, exclude_larger_than):
                raise ValueError("Invalid exclude_larger_than format")
        header = ""
        self.con.execute('INSERT INTO ignore_policy (name, exclude_file, iexclude_file,' +
                         'exclude_larger_than) VALUES (?, ?, ?, ?)', (name, exclude, iexclude, exclude_larger_than))
        self.con.commit()

        

    def get_all_restic_repo(self) -> pd.DataFrame:
        sql_cmd = "SELECT * FROM restic_repo"
        return pd.read_sql(sql_cmd, self.con)
    
    
    
    def insert_restic_repo(self, name: str, restic_path_id: int, 
                           backup_delay_day: int, 
                           keep_policy_id: int, ignore_policy_id: int):
        pass
        