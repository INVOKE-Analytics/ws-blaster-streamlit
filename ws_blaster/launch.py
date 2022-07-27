from ctypes import util
import click
import streamlit as st
import time
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ws_blaster.manage import Manage
from ws_blaster.utils import save_uploadedfile, open_driver
from PIL import Image
import pandas as pd
from ws_blaster.blasting import Blaster

# Hide streamlit header and footer
hide_st_style = """
             <style>
             #MainMenu {visibility: hidden;}
             footer {visibility: hidden;}
             header {visibility: hidden;}
             </style>
             """
st.markdown(hide_st_style, unsafe_allow_html=True)

# INVOKE logo and WS logo setup
invoke_logo_path = 'D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\images\\invoke_logo.jpg'
ws_logo_path = 'D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\images\\ws-logo.png'
invoke_logo = Image.open(invoke_logo_path)
ws_logo = Image.open(ws_logo_path)
st.sidebar.title('Whatsapp Blaster')
st.sidebar.image(invoke_logo)
st.image(ws_logo)
option1 = st.sidebar.selectbox('Select option', ('Blast Messages', 'Account Management'))


##############################################################
# Blasting
##############################################################


##############################################################
# Account Management
##############################################################

manage = Manage(user_path='D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users')


def check_available_account():
        """
        Check available account registed in the apps.

        Available account is a registered account that still valid and not being banned.
        Not-available account is a registered account that have been banned.
        """
        select_platform = st.selectbox('Select set of accounts to check', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))
        if select_platform != '':
            if select_platform == 'Burner Accounts':
                select_platform = 'burner'

            with st.spinner('Checking Accounts...'):
                check_all_acc_exist = manage.checking_banned_or_not(select_platform)

            available = check_all_acc_exist[0]
            not_available = check_all_acc_exist[1]

            if len(available) == 0:
                st.subheader('All accounts are not available!')
                st.subheader('Unavailable accounts: ', ', '.join(not_available))
            elif len(not_available) == 0:
                st.subheader('All accounts are available!')
                st.subheader('Available accounts: ' + str(', '.join(available)))
            else:
                st.subheader('Available account(s): ' + str(', '.join(available)))
                st.subheader('Unavailable account(s): ' + str(', '.join(not_available)))
            
def add_new_account():
        """
        Adding new account. 
        
        How it works:
        1. Choose platform and new name. 
        2. Apps will produce a screenshot of the Whatsapp QR code.
        3. Scan the QR code using your mobile Whatsapp. 

        More:
        1. For every QR scan, a new account is created. 
        2. For every new name, even though it scanned by the same mobile, 
        it will create a new account. 
            Example: 
            new_name: Ammar_1 --> scanned by Ammar --> Ammar_1 account created
            new_name: Ammar_2 --> scanned by Ammar --> Ammar_2 accound created
        3. QR code is refresh for every 15 seconds.
        """
        select_platform_new_acc = st.selectbox('Where do you want to add the account(s)?', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))

        name = st.text_area("Enter Whatsapp account name:")
        get_name = manage.get_name(name)
        get_taken = manage.get_taken(name, select_platform_new_acc)

        if len(get_taken) == 0:
            button_add_account = st.button('Add Account(s)')
            if button_add_account:
                for name_acc in get_name:
                    try:
                        driver = manage.create_new_user_file(select_platform_new_acc, name_acc)
                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/canvas')))
                        manage.take_screenshot(driver)
                        st.success('QR code screenshot taken!')
                        WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH,'//*[@title="Search input textbox"]')))
                        st.subheader(name_acc + ' added!')
                        time.sleep(1)
                    except:
                        manage.automatically_deleted_account_if_error(select_platform_new_acc, name_acc)
        elif len(get_taken) == 1:
            st.write('Account name--' + str(get_taken[0]) + ' is not available. Please choose another name!')
        else:
            st.write(str(', '.join(get_taken)) + ' are not available. Please choose another name!')
                        
def deleting_account():
        """
        To delete NOT-AVAILABLE account only.
        Not-available account is banned account.
        """
        select_platform = st.selectbox('From which set of account(s) do you want to delete?', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))

        if select_platform != '':
            if select_platform == 'Burner Accounts':
                select_platform  = 'burner'
            
            with st.spinner('Checking unavailable account...'):
                accs = manage.get_all_account_name(select_platform)
                st.subheader('Accounts: ' + ', '.join(accs))

            
            #available = manage.checking_account_list_dir(select_platform)[0]
            not_available = manage.checking_banned_or_not(select_platform)[1]
            
            if len(not_available) == 0:
                st.subheader('No account(s) to delete!')

            elif len(not_available) == 1:
                st.subheader('Unavailable account(s): ' + str(', '.join(not_av)))
                
                question = st.selectbox("Are you sure you want to delete the account?",
                                            ("Yes", "No"))

                if question == 'Yes':
                    manage.automatically_deleted_account_if_error(select_platform, not_av)
                elif question == 'No':
                    st.caption("No account is deleted.")
            else:
                for not_av in not_available:
                    st.subheader('Unavailable account(s): ' + str(', '.join(not_av)))
                
                    question = st.selectbox("Are you sure you want to delete the account?",
                                            ("Yes", "No"))

                    if question == 'Yes':
                        manage.automatically_deleted_account_if_error(select_platform, not_av)
                    elif question == 'No':
                        st.caption("No account is deleted.")


if option1 == 'Account Management':
    select_option = st.selectbox('Select option', 
                                    ('',
                                    'Add new account(s)',
                                    'Check available account(s)', 
                                    'Delete unavailable account(s)'))

    if select_option == 'Check available account(s)':
            check_available_account()

    elif select_option == 'Add new account(s)':
            add_new_account()

    elif select_option == 'Delete unavailable account(s)':
            deleting_account()










