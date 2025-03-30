import util
from rich.console import Console
from rich.table import Table
from rich.style import Style
from pynput import keyboard
import time
import os

TABLE_PAGE_SIZE = 5



def stringfy_all_item(in_list: list):
    return [stringfy_all_item(elem) if isinstance(elem, list) else str(elem) for elem in in_list]



class SelectableTable:
    def render_table(self):
        util.clear_console()
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
                self.final_key_input = "f"
                return False
            elif key.char == 'n':
                self.final_key_input = "n"
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
                self.final_key_input = "q"
                self.cursor = -1
                return False
        except:
            pass
    
    
    
    def __init__(self, title: str, header: list, items: list):
        self.cursor = 0
        self.title = title
        self.header = header
        self.items = stringfy_all_item(items)
        self.max_page_num = (len(items) + TABLE_PAGE_SIZE - 1) // TABLE_PAGE_SIZE
        self.final_key_input = None
       
    
    
    def clear_input_buffer(self):
        if os.name == "nt":
            import msvcrt
            time.sleep(0.25)
            while msvcrt.kbhit(): msvcrt.getch()
        else:
            pass
        
        
        
    def run(self):
        self.render_table()
        with keyboard.Listener(on_press=self.on_press) as listner:
            listner.join()
        self.clear_input_buffer()
            
            
        