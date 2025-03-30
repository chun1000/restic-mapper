import sqlite3
import sys
import os
import hashlib
import string
import random
import time
from rich.console import Console
from rich.table import Table
from rich.style import Style
from pynput import keyboard


DB_PATH = "restic-meta.db"
KEY_PATH = "key/"
DATE_TIME_FORMAT = "%Y-%m-%d"
KEY_FILE_SALT = "CHANGE THE SALT IF YOU WANT"

TABLE_PAGE_SIZE = 5



def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


class SelectableTable:
    def render_table(self):
        clear_console()
        page_start = (self.cursor // TABLE_PAGE_SIZE) * TABLE_PAGE_SIZE
        page_end = min(page_start + TABLE_PAGE_SIZE, len(self.items))
        page_items = self.items[page_start:page_end]
        
        table = Table(title=self.title)
        for header_item in self.header:
            table.add_column(header_item)
        
        for i in range(len(page_items)):
            if i == self.cursor - page_start:
                table.add_row(*page_items[i], style=Style(color="white", bgcolor="green", bold=True))
            else:
                table.add_row(*page_items[i])
        console = Console()
        console.print(table)
        console.print(f'[{self.cursor // TABLE_PAGE_SIZE + 1}/{self.max_page_num}]')
        console.print('[W] Up [S] Down [A] Left [D] Right [N] New [F] Ok [Q] Quit')
        
        
    
    
    def on_press(self, key):
        try:
            if key.char == 'f':
                return False
            elif key.char == 'w':
                self.cursor = max(0, self.cursor - 1)
                self.render_table()
            elif key.char == 's':
                self.cursor = min(len(self.items) - 1, self.cursor + 1)
                self.render_table()
            elif key.char == 'a':
                self.cursor = max(0, self.cursor - TABLE_PAGE_SIZE) 
                self.render_table()
            elif key.char == 'd':
                self.cursor = min(len(self.items) - 1, self.cursor + TABLE_PAGE_SIZE)
                self.render_table()
            elif key.char == 'q':
                self.cursor = -1
                return False
        except:
            pass
    
    def __init__(self, title: str, header: list, items: list):
        self.cursor = 0
        self.title = title
        self.header = header
        self.items = items
        self.max_page_num = (len(items) + TABLE_PAGE_SIZE - 1) // TABLE_PAGE_SIZE
       
        
        
    def run(self):
        self.render_table()
        with keyboard.Listener(on_press=self.on_press) as listner:
            listner.join()
        




def hash_key_file(key_file_content: str) -> str:
    data = KEY_FILE_SALT + key_file_content + KEY_FILE_SALT
    hash_object = hashlib.sha256()
    hash_object.update(data.encode())
    hash_value = hash_object.hexdigest()
    return hash_value







def read_sql_file(file_name: str):
    SQL_FOLDER_DIR = "sql/"
    with open(SQL_FOLDER_DIR + file_name, "r") as f:
        return f.read()


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

def create_all_table_if_not_exists(con: sqlite3.Connection):
    con.execute(read_sql_file("create_keep_policy.sql"))
    con.execute(read_sql_file("create_restic_path.sql"))
    con.execute(read_sql_file("create_restic_repo.sql"))
    con.execute(read_sql_file("create_ignore_policy.sql"))



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
    con = sqlite3.connect(DB_PATH)
    header = ["itemA", "itemB", "itemC"]
    item = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 2, 3], [17, 5, 6], [187, 8, 9], [19, 11, 12], [20, 14, 15], [21, 2, 3], [22, 5, 6], [23, 8, 9], [24, 11, 12], [25, 14, 15]]
    for i in range(len(item)):
        item[i] = [str(r) for r in item[i]]
    t = SelectableTable("Hello", header, item)
    t.run()
    print(t.cursor)
    
    #if len(sys.argv) == 1:
    #    setup_mode_start(con)
    
    #if sys.argv[1] == "run":
    #    pass
    #elif sys.argv[1] == "setup":
     #   pass
    
    #con.close()