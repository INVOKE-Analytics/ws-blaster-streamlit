import streamlit as st
from ws_blaster.utils import open_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from os import listdir, path
import time
import shutil
import pathlib
import re

class Manage:
    def __init__(self, user_path):
        self.user_path = pathlib.Path(user_path)
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

    def get_all_sim_name(self, platform:str, client:str)->list[str]:
        """
        Return a list of directory of platform
        """
        path_to_client = self.user_path/platform/client
        sim_list = [f for f in listdir(path_to_client)]
        return sim_list

    def add_client_directory(self, platform, client:str):
        filepath = self.user_path/platform 
        new_dir = os.mkdir(str(filepath / client))
        return new_dir

    def get_all_client_dir(self, platform):
        path_to_platform = self.user_path/platform
        client_dir = [f for f in listdir(path_to_platform)]
        return client_dir


    def get_all_platform(self):
        path_to_user = self.user_path
        platform_list = [f for f in listdir(path_to_user)]
        return platform_list

    def convert_posix_for_windows(self, the_path):
        '''
        TODO: For WINDOWS OS only

        Return the Posix path string into Windows path 
        '''
        sub_path =  re.sub('\\\\', '\\\\\\\\', the_path)
        expander = 'D:\\\\Desktop\\\\INVOKE\\\\ws_blaster\\\\ahilan-branch\\\\venvAhilan\\\\ws-blaster-prod\\\\'
        return expander + sub_path


    def checking_banned_or_not(self,platform:str, client:str)->tuple[list,list]:
        """
        Return list of available and not-available 
        account.
        Checking whether the account is banned or not. 
        """
        sim_list = self.get_all_sim_name(platform, client)
        
        for simcard in sim_list:
            path_to_platform = str(self.user_path/platform/client/simcard)

            # NOTE: This is for Windows only. HASH it for Linux
            # START
            path_to_platform = self.convert_posix_for_windows(str(path_to_platform))
            # END

            driver = open_driver('user-data-dir=' + path_to_platform)
            try:
                f = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,'//*[@title="Search input textbox"]')))
                self.available.append(simcard)
                print("AVAILABLE")
                
            except:
                # If not avaialble, will found these phrase
                f = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/canvas')))
                self.not_available.append(simcard)
                print("NOT AVAILABLE")
                
            driver.quit()

        return (self.available, self.not_available)

    def take_screenshot(self, driver):
        # NOTE : QR code will be refreshed after 15 seconds
        """
        Take the screenshot of the QR code 
        """
        driver.save_screenshot('ws-blaster-prod/screenshot/QR_code.png')
        ss = 'screenshot'
        self.screenshot.append(ss)

    def create_new_user_file(self, platform:str, client:str, account_name:str):
        """
        Create new file user account in platform file
        """
        path_to_platform = str(self.user_path/platform/client/account_name)

        # NOTE: This is for Windows only. HASH it for Linux
        # START
        path_to_platform_conv = self.convert_posix_for_windows(str(path_to_platform))
        print('#'*100)
        print('user-data-dir=' + path_to_platform_conv)
        print('#'*100)
        # END

        driver = open_driver('user-data-dir=' + path_to_platform_conv, headless=True)
        self.driver_dict[path_to_platform] = account_name
        return driver
    
    def deleted_account(self, platform:str, client:str, simcard:str):
        """
        To delete the directory which deleted the account too.
        """
        path_to_account =  self.user_path/platform/client/simcard
        print(100*'#')
        print(path_to_account.exists())
        print(100*'#')
        shutil.rmtree(path_to_account)
        self.account_dict[client] = 'deleted'

    
    def get_taken(self, name:str, platform:str, client:str)->list[str]:
        """
        Return list of the account name, if the account is existed (added)
        """
        name = self.get_name(name)
        sim_list = self.get_all_sim_name(platform,client)
        print("SIMLIST",sim_list, "NAME", name)
        taken = [x for x in name if x in sim_list]
        return taken

    def get_screenshot(self, photo):
        return st.image(photo)
