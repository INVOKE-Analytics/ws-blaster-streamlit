import streamlit as st
from ws_blaster.utils import open_driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
import time
import shutil

class Manage:
    def __init__(self):
        pass

    def opt3(self):
        """
        Description:
            For Account Management, there is 3 type of Account used:
            - Meniaga
            - Ayuh Malaysia 
            - Burner Account 

        """
        option3 = st.selectbox('Select set of accounts to check', ('', 'meniaga','AyuhMalaysia','Burner Accounts'))
        if option3 != '':
            if option3 == 'Burner Accounts':
                option3 = 'burner'
                return option3

    def remove_DS_store(self): 
        """ 
        Description:
            - This function will remove .DS_Store file which is produced in 
                Macbook.

        Need to test

        Return --> List[str]
        """
        self.option3 = Manage.opt3()
        mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + self.option3 + '/'
        accs = [f for f in listdir(mypath)]
        if ".DS_Store" in accs:
                accs.remove(".DS_Store")
        return accs

    def account_collection(self, accs): 
        """
        Description:
            - This function will collect list of available and non-available function 
        
        Need to test

        Return --> tuple(list,list)
        """
        self.option3 = Manage.opt3()
        self.accs = accs
        accs = Manage.remove_DS_store()
        
        available = []
        not_available = []

        mypath = 'user-data-dir=Users/amerwafiy/Library/Application Support/Google/Chrome/' + self.option3 + '/'
        for acc in self.accs:
            driver = open_driver(mypath + accs)
            try:
                elems = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,'Need help to get started?')))
                not_available.append(accs)
            except:
                available.append(accs)
            driver.quit()

        return (available, not_available)

    def checking_acc_availability(self, available, not_available):
        """
        Description:
            - This function will check the availability of account 
            based on `account_collection` function

        Need to test

        Return --> DeltaGenerator
        """
        self.available = available
        self.not_available = available

        if len(self.available) == 0:
            st.subheader('All accounts are not available!')
            return st.subheader('Unavailable accounts: ', ', '.join(not_available))
        elif len(self.not_available) == 0:
            st.subheader('All accounts are available!')
            return st.subheader('Available accounts: ' + str(', '.join(available)))
        else:
            st.subheader('Available account(s): ' + str(', '.join(available)))
            return st.subheader('Unavailable account(s): ' + str(', '.join(not_available)))

    def add_new_acc(self, taken, option3, name):
        """
        Description:
            - This function will check either the accound name is taken or not. 
            - If taken, you need to create new account. 
            - We also can cheese the available account. 

        Need to test
        Return --> string
        """
        self.taken = taken 
        self.option3 = option3
        self.name = name

        if len(self.taken) == 0:
            option4 = st.button('Add Account(s)')
            if option4:
                mypath = 'user-data-dir=Users/amerwafiy/Library/Application Support/Google/Chrome/' + self.option3 + '/'
                for n in self.name:
                    driver = open_driver(mypath + n, headless = False)
                    try:
                        f = WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH,'//*[@title="Search input textbox"]')))
                        
                        time.sleep(1)
                        return st.subheader(n + ' added!')
                        driver.quit()
                    except:
                        driver.quit()
                        st.subheader('Unable to link account(' + n + '). Please try again!')
                        mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
                        path_delete = mypath + n
                        return shutil.rmtree(path_delete)
                
        elif len(self.taken) == 1:
            return st.write('Account name--' + str(self.taken[0]) + ' is not available. Please choose another name!')
        
        else:
            return st.write(str(', '.join(self.taken)) + ' are not available. Please choose another name!')

    def delete_unav_account(self, option3, not_available):
        """
        Need to test

        Return --> DeltaGenerator
        """
        self.option3 = option3
        self.option3 = Manage.opt3()
        self.not_available = not_available

        if len(self.not_available) == 0:
            return st.subheader('No account(s) to delete!')
        else:
            st.subheader('Unavailable account(s): ' + str(', '.join(self.not_available)))
            mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + self.option3 + '/'
            for n in self.not_available:
                path_delete = mypath + n
                shutil.rmtree(path_delete)
            return st.subheader('Succesfully deleted unavailable account(s)!')


    def main_option_2(self, option2):

        self.option2 = option2
        
        if self.option2 == 'Check available account(s)':
            option3 = Manage.opt3()
            
            accs = Manage.remove_DS_store(option3)
            with st.spinner('Checking Accounts...'):
                available = Manage.account_collection(accs, option3)[0]
                not_available = Manage.account_collection(accs, option3)[1]
                
            checking_avb_account = Manage.checking_acc_availability(available, not_available)

            return checking_avb_account

        elif self.option2 == 'Add new account(s)':
            option3 = Manage.opt3()
            accs = Manage.remove_DS_store(option3)

            name = st.text_area("Enter Whatsapp account name:")
            name = name.split(',')
            name = [x.strip() for x in name]
            taken = [x for x in name if x in accs]
            check_new_account = Manage.add_new_acc(taken, option3, name)

            return check_new_account
    
        elif self.option2 == 'Delete unavailable account(s)':
            option3 = Manage.opt3()
            accs = Manage.remove_DS_store(option3)

            st.subheader('Accounts: ' + ', '.join(accs))

            with st.spinner('Deleting Accounts...'):
                available = Manage.checking_acc_availability(accs, option3)[0]
                not_available = Manage.checking_acc_availability(accs, option3)[1]

                # here
                delete_not_av = Manage.delete_unav_account(not_available)
                return delete_not_av
                    

    def main_acc_management(self, option1):

        self.option1 = option1

        self.option1 == 'Account Management'
        st.image('/Users/amerwafiy/Desktop/ws-blasting/ws-logo.png')

        option2 = st.selectbox('Select option', ('Add new account(s)','Check available account(s)', 'Delete unavailable account(s)'))
        main_manager = Manage.main_option_2(option2)
    
        return main_manager