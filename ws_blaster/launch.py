from ctypes import util
import streamlit as st
import time
from PIL import Image
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

if option1 == 'Account Management':
    select_option = st.selectbox('Select option', 
                            ('',
                            'Add new account(s)',
                            'Check available account(s)', 
                            'Delete unavailable account(s)'))

    if select_option == 'Check available account(s)':
        select_platform = st.selectbox('Select set of accounts to check', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))
        if select_platform != '':
            if select_platform == 'Burner Accounts':
                select_platform = 'burner'

            get_acc = manage.get_all_account_name(select_platform)
            check_all_acc_exist = manage.checking_account_list_dir()

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
            
    elif select_option == 'Add new account(s)':
        select_platform_new_acc = st.selectbox('Where do you want to add the account(s)?', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))

        get_accs = manage.get_all_account_name(select_platform_new_acc)
        name = st.text_area("Enter Whatsapp account name:")
        get_taken = manage.get_taken(name, select_platform_new_acc)

        if len(get_taken) == 0:
            button_add_account = st.button('Add Account(s)')
            if button_add_account:
                for name_acc in get_taken:
                    try:
                        create_new_acc = manage.create_new_user_file(select_platform_new_acc, name_acc)
                        st.subheader(name_acc + ' added!')
                        time.sleep(1)
                        manage.create_new_user_file.quit()
                    except:
                        manage.create_new_user_file.quit()
                        manage.automatically_deleted_account_if_error(select_platform_new_acc, name_acc)
        elif len(get_taken) == 1:
            st.write('Account name--' + str(get_taken[0]) + ' is not available. Please choose another name!')
        else:
            st.write(str(', '.join(get_taken)) + ' are not available. Please choose another name!')
                        

    elif select_option == 'Delete unavailable account(s)':
        select_platform = st.selectbox('From which set of account(s) do you want to delete?', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))

        if select_platform != '':
            if select_platform == 'Burner Accounts':
                select_platform  = 'burner'
            accs = manage.get_all_account_name(select_platform)
            st.subheader('Accounts: ' + ', '.join(accs))






