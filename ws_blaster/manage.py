import streamlit as st
from ws_blaster.utils import open_driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import listdir
import time
import shutil

def opt3():
    option3 = st.selectbox('Select set of accounts to check', ('', 'meniaga','AyuhMalaysia','Burner Accounts'))
    if option3 != '':
        if option3 == 'Burner Accounts':
            option3 = 'burner'
            return option3

def remove_DS_store(option3):
        mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
        accs = [f for f in listdir(mypath)]
        if ".DS_Store" in accs:
                accs.remove(".DS_Store")
        return accs

def account_collection(accs, option3):
    available = []
    not_available = []
    mypath = 'user-data-dir=Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
    for acc in accs:
        driver = open_driver(mypath + acc)
        try:
            elems = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.PARTIAL_LINK_TEXT,'Need help to get started?')))
            not_available.append(acc)
        except:
            available.append(acc)
        driver.quit()

    return (available, not_available)

def checking_acc_availability(available, not_available):
    if len(available) == 0:
        st.subheader('All accounts are not available!')
        return st.subheader('Unavailable accounts: ', ', '.join(not_available))
    elif len(not_available) == 0:
        st.subheader('All accounts are available!')
        return st.subheader('Available accounts: ' + str(', '.join(available)))
    else:
        st.subheader('Available account(s): ' + str(', '.join(available)))
        return st.subheader('Unavailable account(s): ' + str(', '.join(not_available)))

def add_new_acc(taken, option3, name):
    if len(taken) == 0:
                option4 = st.button('Add Account(s)')
                if option4:
                    mypath = 'user-data-dir=Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
                    for n in name:
                        driver = open_driver(mypath + n, headless = False)
                        try:
                            f = WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH,'//*[@title="Search input textbox"]')))
                            st.subheader(n + ' added!')
                            time.sleep(1)
                            driver.quit()
                        except:
                            driver.quit()
                            st.subheader('Unable to link account(' + n + '). Please try again!')
                            mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
                            path_delete = mypath + n
                            shutil.rmtree(path_delete)
            
    elif len(taken) == 1:
        st.write('Account name--' + str(taken[0]) + ' is not available. Please choose another name!')
    
    else:
        st.write(str(', '.join(taken)) + ' are not available. Please choose another name!')

def delete_unav_account(not_available):
    if len(not_available) == 0:
        st.subheader('No account(s) to delete!')
    else:
        st.subheader('Unavailable account(s): ' + str(', '.join(not_available)))
        mypath = '/Users/amerwafiy/Desktop/ws-blasting/Users/amerwafiy/Library/Application Support/Google/Chrome/' + option3 + '/'
        for n in not_available:
            path_delete = mypath + n
            shutil.rmtree(path_delete)
        st.subheader('Succesfully deleted unavailable account(s)!')

def main_option_2(option2):
        if option2 == 'Check available account(s)':
            option3 = opt3()
            

            accs = remove_DS_store(option3)
            with st.spinner('Checking Accounts...'):
                available = account_collection(accs, option3)[0]
                not_available = account_collection(accs, option3)[1]
                
            checking_avb_account = checking_acc_availability(available, not_available)

            return checking_avb_account

        elif option2 == 'Add new account(s)':
            option3 = opt3()
            accs = remove_DS_store(option3)

            name = st.text_area("Enter Whatsapp account name:")
            name = name.split(',')
            name = [x.strip() for x in name]
            taken = [x for x in name if x in accs]
            check_new_account = add_new_acc(taken, option3, name)

            return check_new_account
    
        elif option2 == 'Delete unavailable account(s)':
            option3 = opt3()
            accs = remove_DS_store(option3)

            st.subheader('Accounts: ' + ', '.join(accs))

            with st.spinner('Deleting Accounts...'):
                available = account_collection(accs, option3)[0]
                not_available = account_collection(accs, option3)[1]

                # here
                delete_not_av = delete_unav_account(not_available)
                return delete_not_av   

    def main_acc_management(option1):
        option1 == 'Account Management'
        st.image('/Users/amerwafiy/Desktop/ws-blasting/ws-logo.png')

        option2 = st.selectbox('Select option', ('Add new account(s)','Check available account(s)', 'Delete unavailable account(s)'))
        main_manager = main_option_2(option2)
    
        return main_manager       
