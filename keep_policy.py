import re

class KeepPolicy:
    def __init__(self, name: str):
        self.name = name
        self.keep_last = None
        self.keep_hourly = None
        self.keep_daily = None
        self.keep_weekly = None
        self.keep_monthly = None
        self.keep_yearly = None
        self.keep_within = None
        
    
    
    def get_header(self):
        return "(name, keep_last, keep_hourly, keep_daily, keep_weekly, keep_monthly, keep_yearly, keep_within)"
    
    
    def get_values(self):
        keep_list = [self.keep_last, self.keep_hourly, self.keep_daily,
                      self.keep_weekly, self.keep_monthly, self.keep_yearly]
        value_str = ""
        value_str += f'"{self.name}"'
         
        for elem in keep_list:
             value_str += f", {"Null" if elem is None else elem}"
        
        value_str += f', {"Null" if self.keep_within is None else self.keep_within}'
        value_str = "(" + value_str + ")"
        return value_str
         
        
        
    def set_keep_within(self, within : str):
        pattern = r'^(\d+y)?(\d+m)?(\d+d)?(\d+h)?$'
        if within == "":
            self.keep_within = None
        elif re.match(pattern, within):
            self.keep_within = within
        else:
            raise ValueError("Invalid keep within format")
        
        
        
    def set_keep_last(self, num: int):
        self.keep_last = num
    def set_keep_hourly(self, num: int):
        self.keep_hourly = num
    def set_keep_daily(self, num: int):
        self.keep_daily = num
    def set_keep_weekly(self, num: int):
        self.keep_weekly = num
    def set_keep_monthly(self, num: int):
        self.keep_monthly = num
    def set_keep_yearly(self, num: int):
        self.keep_yearly = num
        