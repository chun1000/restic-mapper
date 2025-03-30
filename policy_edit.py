from sql_func import ResticSql
from selectable_table import SelectableTable
import pandas as pd
import sys
import time
from keep_policy import KeepPolicy



def run_sub_func_make_directory(sql_runner: ResticSql):
    print("Enter an alias for the directory")
    alias = input()
    print("Enter the directory where repositories are saved")
    path = input()
    sql_runner.insert_path_info(alias, path)


def run_menu_directory(sql_runner: ResticSql):
    while True:
        df = sql_runner.get_all_path_info()
        header = df.columns.tolist()
        content = df.values.tolist()
        table = SelectableTable("Directory Menu", header, content)
        table.run()
        if table.final_key_input == 'n':
            run_sub_func_make_directory(sql_runner)
        elif table.final_key_input == 'f':
            pass
        elif table.final_key_input == 'q':
            break
        else:
            print("Warning: Unknown key input")



def run_sub_menu_dir_select(sql_runner: ResticSql) -> int:
    while True:
        df = sql_runner.get_all_path_info()
        header = df.columns.tolist()
        content = df.values.tolist()
            
        dir_table = SelectableTable("Select backup directory", header, content)
        dir_table.run() 
        if dir_table.final_key_input == 'f' and dir_table.cursor != -1:
            dir_id = df['id'].iloc[dir_table.cursor]
            dir_name = df['name'].iloc(dir_table.cursor)
            print(dir_name + "selected?[Y/N]")
            input_line = input()
            if input_line == "Y":
                return dir_id
            else:
                continue
        elif dir_table.final_key_input == 'n':
            run_sub_func_make_directory(sql_runner)
        else:
            return -1


def run_menu_restic_repo(sql_runner: ResticSql):
    while True:
        df = sql_runner.get_all_restic_repo()
        header = df.columns.tolist()
        content = df.values.tolist()
        table = SelectableTable("Repo Menu", header, content)
        table.run()
        
        if table.final_key_input == 'n':
            print("Enter an alias for the directory")
            alias = input()
            print("Enter backup delay day")
            backup_delay_day = input()
            dir_id = run_sub_menu_dir_select(sql_runner)
        elif table.final_key_input == 'f':
            pass
        elif table.final_key_input == 'q':
            break
        else:
            print("Warning: Unknown key input")
        

def run_menu_keep_policy(sql_runner: ResticSql):
    while True:
        df = sql_runner.get_all_keep_policy()
        header = df.columns.tolist()
        content = df.values.tolist()
        table = SelectableTable("Keep policy menu", header, content)
        table.run()
        if table.final_key_input == 'n':
            print("Enter an alias for the keep policy:")
            name = input()
            policy = KeepPolicy(name)
            
            keep_dict = {
                "keep_last" : policy.set_keep_last,
                "keep_hourly" : policy.set_keep_hourly,
                "keep_daily" : policy.set_keep_daily,
                "keep_weekly" : policy.set_keep_weekly,
                "keep_monthly" : policy.set_keep_monthly,
                "keep_yearly" : policy.set_keep_yearly,
            }
            
            for text, method in keep_dict.items():
                print(f"Enter {text}. If you don't want to set, just press Enter")
                input_str = input()
                if input_str != "": method(int(input_str))
                
            print(f"Enter keep_within. If you don't want to set, just press Enter")
            input_str = input()
            if input_str != "": policy.set_keep_within(input_str)
            sql_runner.insert_keep_policy(policy)
        elif table.final_key_input == 'q':
            break
        
            

            
def run_menu_ignore_policy(sql_runner: ResticSql):
    while True:
        df = sql_runner.get_all_ignore_policy()
        header = df.columns.tolist()
        content = df.values.tolist()
        table = SelectableTable("Ignore policy menu", header, content)
        table.run()
        if table.final_key_input == 'n':
            exclude_file_path = None
            iexclude_file_path = None
            exclude_larger_than = None
        
        
            print("Enter an alias for the ignore policy")
        
            name = input()
            print("Enter exclude_file path. If you don't want to set, just press Enter")
            input_str = input()
            if input_str == "":
                print("Enter iexclude_file path. If you don't want to set, just press Enter")
                input_str = input()
                if input_str != "": iexclude_file_path = input_str
            else: exclude_file_path = input_str
            print("Enter exclude_larger_than. If you don't want to set, just press Enter")
            input_str = input()
            if input_str != "": exclude_larger_than = input_str
            sql_runner.insert_ignore_policy(name, exclude_file_path, iexclude_file_path, exclude_larger_than)            
        elif table.final_key_input == 'f':
            pass
        elif table.final_key_input == 'q':
            break
        else:
            print("Warning: Unknown key input")
            



def run_policy_edit(sql_runner: ResticSql):
    try:
        print("1. Directory 2. Repo 3. KeepPolicy 4. IgnorePolicy 5. Exit")
        input_cmd = input()
        if input_cmd == "1":
            print("Run directories menu...")
            run_menu_directory(sql_runner)
        elif input_cmd == "2":
            run_menu_restic_repo(sql_runner)
        elif input_cmd == "3":
            run_menu_keep_policy(sql_runner)
        elif input_cmd == "4":
            run_menu_ignore_policy(sql_runner)
        elif input_cmd == "5":
            pass
        else:
            pass
    except Exception as e:
        print(e)
    