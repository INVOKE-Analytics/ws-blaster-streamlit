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

    def get_all_sim_name(self, platform:str, client:str)->list[str]:
        """
        Return a list of directory of platform
        """
        path_to_accs = self.user_path  + '\\' + platform + '\\' + client
        sim_list = [f for f in listdir(path_to_accs)]
        return sim_list

    def add_client_directory(self, platform, client:str):
        filepath = self.user_path + '\\' + str(platform) 
        make_dir = os.mkdir(filepath + '\\' + client)
        return make_dir

    def get_all_client_dir(self, platform):
        path_to_platform = self.user_path + '\\' + platform 
        client_dir = [f for f in listdir(path_to_platform)]
        return client_dir


    def get_all_platform(self):
        path_to_accs = self.user_path  
        platform_list = [f for f in listdir(path_to_accs)]
        return platform_list

    def checking_banned_or_not(self,platform:str, client:str)->tuple[list,list]:
        """
        Return list of available and not-available 
        account.
        Checking whether the account is banned or not. 
        """
        sim_list = self.get_all_sim_name(platform, client)
        path_to_platform = 'user-data-dir=' + str(self.user_path) + '\\' + str(platform) + '\\' + str(client) + '\\'
       
        for simcard in sim_list:
            driver = open_driver(path_to_platform+simcard)
            try:
                # if available, will found there phrase
                #WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH,
                #                    '//*[@title="Search input textbox"]')))
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
        # TODO: QR code will be refreshed after 15 seconds
        """
        Take the screenshot of the QR code 
        """
        driver.save_screenshot('D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\screenshot\\QR_code.png')
        ss = 'screenshot'
        self.screenshot.append(ss)

    def create_new_user_file(self, platform:str, client:str, account_name:str):
        # TODO: Client has been added here, not tested yet
        """
        Create new file user account in platform file
        """
        path_to_platform = 'user-data-dir=' + self.user_path + '\\' + str(platform) + '\\' + str(client) + '\\'
        driver = open_driver(path_to_platform + account_name, headless=True)
        self.driver_dict[path_to_platform] = account_name
        return driver
    
    
    def deleted_account(self, platform:str, client:str, simcard:str):
        """
        To delete the directory which deleted the account too.
        """
        path_to_acount =  str(self.user_path) + '\\' + str(platform) + '\\' + str(client) + '\\' + str(simcard)
        shutil.rmtree(path_to_acount)
        self.account_dict[client] = 'deleted'

    
    def get_taken(self, name:str, platform:str, client:str)->list[str]:
        """
        Return list of the account name, if the account is existed (added)
        """
        name = self.get_name(name)
        sim_list = self.get_all_sim_name(platform,client)
        taken = [x for x in name if x in sim_list]
        return taken

    def get_screenshot(self, photo):
        return st.image(photo)
