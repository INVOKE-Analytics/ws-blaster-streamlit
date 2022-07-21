from sklearn.metrics import accuracy_score
from ws_blaster.utils import open_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
import time
import shutil
import pathlib

class Manage:
    def __init__(self, user_path, platform):
        self.user_path = pathlib.Path(user_path)
        self.platform = platform
        self.driver_dict = {}
        self.account_dict = {}

    def get_name(self,name):
        """
        Return list of name
        """
        self.name = name.split(',') 
        name = [x.strip() for x in name]
        return name
    
    def get_all_account_list_dir(self):
        mypath = 'user-data-dir=' + self.user_path + '/' 
        accs = [f for f in listdir(mypath)]
        return accs

    def checking_account(self):
        accs = self.get_all_account_list_dir(self)
        path_to_platform = 'user-data-dir=' + self.user_path + '/' + self.platform + '/'

        available = [] # if len > 1, there is account
        not_available = []
        for acc in accs:
            driver = open_driver(path_to_platform + acc)
            try:
                not_available.append(acc)
            except:
                available.append(acc)
            driver.quit()

        return (available, not_available)
    
        
    def add_new_account(self):
        """
        Component 1 for 'Add account'
        """
        name = self.get_name(self)
        for account_name in name:
            path_to_account = 'user-data-dir=' + self.user_path + '/' + self.platform + '/' + account_name
            driver = open_driver(path_to_account, headless = False)
            self.account_dict[account_name] = driver
    
    def setup_new_driver_for_new_account(self):
        mypath = self.add_new_account(self)
        driver = open_driver(mypath, headless = False)
        self.driver_dict[driver] = driver # will add into the dict, means new account added 

    def automatically_deleted_account_if_error(self):
        """
        Component 2 for 'Add account'
        """
        n = self.get_name(self)
        mypath = 'user-data-dir=' + self.user_path + '/' + self.platform + '/' + n
        return shutil.rmtree(mypath) 

    def get_taken(self):
        """
        Return name_item within name list, that only exist in accs
        """
        name = self.get_name(self)
        accs = self.get_accs(self)
        taken = [x for x in name if x in accs]
        return taken

    def get_option1(self):
        """
        Return option1 -- 'Account management'
        """
        option1 = 'Account Management'
        return option1

    def ws_logo(self):
        path = '/Users/amerwafiy/Desktop/ws-blasting/ws-logo.png'
        return path

    def select_box_option1_acc_management(self):
        return  ['Add new account(s)','Check available account(s)', 'Delete unavailable account(s)']