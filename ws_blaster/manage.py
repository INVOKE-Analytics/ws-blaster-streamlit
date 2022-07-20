from ws_blaster.utils import open_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
import time
import shutil

class Manage:
    def __init__(self):
        pass
    
    def get_account_options(self):
        return ['', 'Meniaga', "Ayuh Malaysia", "Burner Account"]    

    def opt3(self):
        """
        Description: To choose option3

        """
        option3 = self.get_account_options()
        if option3 != '':
            if option3 == 'Burner Accounts':
                option3 = 'burner'
                return option3

    def remove_DS_store(self, mypath): 
        """ 
        Description: To remove .DS Store file
        
        """
        self.mypath = mypath
        #option3 = self.opt3()
        #mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
        accs = [f for f in listdir(self.mypath)]
        if ".DS_Store" in accs:
            return accs.remove(".DS_Store")
        return accs

    #   START if len(taken) == 0:        
    def get_item_in_name(self, string_names):
        self.string_names = string_names
        name = self.get_name(self.string_names)
        for n in name:
            return n

    def try_Add_account(self):
        """
        Component 1 for 'Add account'
        """
        option3 = self.opt3(self)
        mypath = 'user-data-dir=Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
        n = self.get_item_in_name(self)
        driver = open_driver(mypath + n, headless = False)
        f = WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH,'//*[@title="Search input textbox"]')))
        time.sleep(1)
        return f

    def exept_Add_account_path_delete(self):
        """
        Component 2 for 'Add account'
        """
        option3 = self.opt3(self)
        mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
        n = self.get_item_in_name(self)
        path_delete = mypath + n
        return shutil.rmtree(path_delete) 

    def get_list_available_unavaible_account(self,accs,mypath):
        """
        Return list of available and not_available 
        """
        self.accs = accs
        accs = self.get_accs(self)
        self.mypath = mypath
        #option3 = self.opt3(self)

        available = []
        not_available = []
        #mypath = 'user-data-dir=Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
        for acc in accs:
            driver = open_driver(self.mypath + acc)
            try:
                elems = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,'Need help to get started?')))
                not_available.append(acc)
            except:
                available.append(acc)
            driver.quit()

        return (available, not_available)

    def get_accs(self,accs)->list:
        """
        Return list of accs
        """
        self.accs = accs
        option3 = self.opt3()
        accs = self.remove_DS_store(option3)
        return accs

    def get_name(self,name)->list:
        """
        Return list of name
        """
        self.name = name.split(',') 
        name = [x.strip() for x in name]
        return name

    def get_taken(self):
        """
        Return name_item within name list, that only exist in accs
        """
        name = self.get_name(self)
        accs = self.get_accs(self)
        taken = [x for x in name if x in accs]
        return taken

    def option1_acc_management(self):
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