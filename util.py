import os
import random
import string
import time
import getpass
import hashlib
import datetime as dt



KEY_FILE_SALT = "CHANGE THIS SALT"
DATE_TIME_FMT = "%Y-%m-%d"



def get_today_str() -> str:
    return dt.datetime.today().strftime(DATE_TIME_FMT)



def clear_console():
    os.system("cls" if os.name == "nt" else "clear")



def hash_key(key: str) -> str:
    data = KEY_FILE_SALT + key + KEY_FILE_SALT
    hash_object = hashlib.sha256()
    hash_object.update(data.encode())
    hash_value = hash_object.hexdigest()
    return hash_value
    

def make_key_file(dir: str) -> str:
    if not os.path.exists(dir):
        print("The directory not exists.")
        return
    key_string = ''.join(random.sample(string.ascii_letters + "0123456789", 50))
    key_file_name = ''.join(random.sample(string.ascii_letters, 5)) + str(int(time.time()))  + ".txt"
    key_file_path = dir + '/' + key_file_name
    with open(key_file_path, 'w') as f:
        f.write(key_string)
    return key_file_path



def make_passwd() -> str:
    passwd = ""
    while True:
        passwd = getpass.getpass("Enter new password: ")
        if passwd == "": print("Password cannot be empty")
        cross_check_passwd = getpass.getpass("Enter new password again: ")
        if passwd != cross_check_passwd:
            print("Password incorrect!")
        else:
            break
    return passwd