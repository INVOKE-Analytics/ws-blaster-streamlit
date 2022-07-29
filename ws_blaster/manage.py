import streamlit as st
from ws_blaster.utils import open_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
import time
import shutil
import pathlib

class Manage:
    def __init__(self, user_path):
        self.user_path = user_path
        self.driver_dict = {}
        self.account_dict = {}
        self.list_dir = {}
        self.new_account = []
        self.available = [] # if len > 1, there is account
        self.not_available = []
        self.exist_account = self.available + self.not_available
        self.screenshot = []
    
    def get_name(self, name:str):
        """
        Return name in list data type
        """
        name = name.split(',') 
        name = [x.strip() for x in name]
        return name

    @property
    def get_all_account_name(self, platform:str)->list[str]:
        """
        Return a list of directory of platform
        """
        path_to_accs = self.user_path  + '\\' + platform
        accs = [f for f in listdir(path_to_accs)]
        return accs

    @property
    def checking_banned_or_not(self,platform:str)->tuple[list,list]:
        """
        Return list of available and not-available 
        account.
        Checking whether the account is banned or not. 
        """
        accs = self.get_all_account_name(platform)
        path_to_platform = 'user-data-dir=' + str(self.user_path) + '\\' + str(platform) + '\\' 
       
        for acc in accs:
            driver = open_driver(path_to_platform+acc)
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,'Need help to get started?')))
                self.not_available.append(acc)
            except:
                self.available.append(acc)
            driver.quit()

        return (self.available, self.not_available)

    @property
    def take_screenshot(self, driver):
        # TODO: QR code will be refreshed after 15 seconds
        """
        Take the screenshot of the QR code 
        """
        driver.save_screenshot('D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\screenshot\\QR_code.png')
        ss = 'screenshot'
        self.screenshot.append(ss)

    @property
    def create_new_user_file(self, platform:str, account_name):
        """
        Create new file user account in platform file
        """
        path_to_platform = 'user-data-dir=' + self.user_path + '\\' + str(platform) + '\\'
        driver = open_driver(path_to_platform + account_name, headless=True)
        self.driver_dict[path_to_platform] = account_name
        return driver
    
    @property
    def deleted_account(self, platform:str, name:str):
        """
        To delete the directory which deleted the account too.
        """
        path_to_acount =  str(self.user_path) + '\\' + str(platform) + '\\' + str(name)
        shutil.rmtree(path_to_acount)
        self.account_dict[name] = 'deleted'

    @property
    def get_taken(self, name:str, platform:str)->list[str]:
        """
        Return list of the account name, if the account is existed (added)
        """
        name = self.get_name(name)
        accs = self.get_all_account_name(platform)
        taken = [x for x in name if x in accs]
        return taken

    def get_screenshot(self, photo):
        return st.image(photo)


