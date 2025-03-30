import sqlite3
import sys
import os
import hashlib
import string
import random
import time
from selectable_table import SelectableTable
from util import read_sql_file



DB_PATH = "restic-meta.db"
KEY_PATH = "key/"
DATE_TIME_FORMAT = "%Y-%m-%d"
KEY_FILE_SALT = "CHANGE THE SALT IF YOU WANT"









        




def hash_key_file(key_file_content: str) -> str:
    data = KEY_FILE_SALT + key_file_content + KEY_FILE_SALT
    hash_object = hashlib.sha256()
    hash_object.update(data.encode())
    hash_value = hash_object.hexdigest()
    return hash_value










'''
def print_table_with_select_ui(
    input_table: list, table_header: list, num_row_screen: int, help_str : str
) -> int:
    screen_start = 0
    input_table_len = len(input_table)
    while True:
        clear_console()
        print(help_str)
        partial_list = input_table[screen_start:screen_start + num_row_screen]
        print(tabulate(partial_list, table_header, tablefmt='grid'))
        print('prev:[p], next:[n], select:[number], exit: [x]')
        input_str = input()
        if input_str == 'p':
            screen_start = max(screen_start - num_row_screen, 0)
        elif input_str == 'n':
            screen_start = min(screen_start + num_row_screen, input_table_len - num_row_screen)
        elif input_str == 'x':
            return -1
        elif input_str.isdecimal():
            return int(input_str)
        else:
            pass
'''



def add_directory(con: sqlite3.Connection, dir: str):
    if not os.path.exists(dir):
        print("The directory not exists.")
        return
    if len(os.listdir(dir)) != 0:
        print("The directory is not empty!")
        return
    
    key_string = ''.join(random.sample(string.ascii_letters + "0123456789", 50))
    print(hash_key_file(key_string))
    key_file_name = ''.join(random.sample(string.ascii_letters, 5)) + str(int(time.time()))  + ".txt"
    key_file_dir = KEY_PATH + key_file_name
    with open(key_file_dir, 'w') as f:
        f.write(key_string)
    
    sql_add_dir = "INSERT INTO restic_path (path, key_file) VALUES ('{0}', '{1}')".format(dir, key_file_dir)
    con.execute(sql_add_dir)
    con.commit()



def add_backup_policy_cli(con: sqlite3.Connection):
    help = "Select directory backup repository saved."
    header = ["id", "path", "key_file"]
    read_data = con.execute('SELECT * FROM restic_path')
    print_table_with_select_ui(list(read_data), header, 5, help)
    
    print("Enter backup policy name: ")
    name = input()
    last_backup_date = "1234"

def setup_mode_start(con: sqlite3.Connection):
    create_all_table_if_not_exists(con)
    menu_list = [
        "1. Add Directory", "2. Add Backup Policy", "3. Add Keep Policy",
        "4. Add Ignore Policy", "5. List Directory", "6. List Backup Policy",
        "7. List Keep Policy", "8. List Ignore Policy", "9. Remove Directory",
        "10. Remove Backup Policy", "11. Remove Keep Policy", "12. Remove Ignore Policy",
        "13. List Backup Snaphost", "14. Extract Snapshot", "15.Force Backup"
    ]
    while(True):
        try:
            for i in range(len(menu_list)):
                if i % 4 == 0:
                    print()
                print(menu_list[i], end=' ')
            print()
            menu_num = input()
            
            if menu_num == '1':
                print("Enter New directory: ")
                dir = input()
                add_directory(con, dir)
            elif menu_num == '2':
                add_backup_policy_cli(con)
        except ValueError as e:
            pass


if __name__ == "__main__":
    pass
    #if len(sys.argv) == 1:
    #    setup_mode_start(con)
    
    #if sys.argv[1] == "run":
    #    pass
    #elif sys.argv[1] == "setup":
     #   pass