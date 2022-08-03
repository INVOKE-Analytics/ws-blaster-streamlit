
from soupsieve import select
import streamlit as st
import time
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ws_blaster.manage import Manage
from ws_blaster.utils import save_uploadedfile, open_driver
import streamlit as st

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
invoke_logo_path = '../ws-blaster-prod/images/invoke_logo.jpg'
ws_logo_path = '../ws-blaster-prod/images/ws-logo.png'
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
        Check available simcard registed in the apps.

        Available simcard is a registered simcard that still valid and not being banned.
        Not-available simcard is a registered simcard that have been banned.
        """
        st.markdown("----------------------------------------------")
        st.info("CHECK AVAILABLE simcard")
        # choose the platform
        select_platform = st.selectbox('Select set of simcard to check', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))

        select_client = st.selectbox('Select client', manage.get_all_client_dir(select_platform))
        if select_platform != '':
            if select_platform == 'Burner Accounts':
                select_platform = 'burner'

            # press the button to start CHECK
            button = st.button("CHECK")
            if button:
                with st.spinner('Checking simcard status...'):
                    time.sleep(2)
                    check_all_acc_exist = manage.checking_banned_or_not(select_platform, select_client)

                    available = check_all_acc_exist[0]
                    not_available = check_all_acc_exist[1]

                    if len(available) == 0:
                        st.error('All sim(s) are not available!')
                    elif len(not_available) == 0:
                        st.success('All sim(s) are available!')
                        st.subheader('Available sim(s): ')
                        st.code('\n' + str(' | '.join(available)))
                    else:
                        st.success('Available sim(s): ')
                        st.code(str(' |  '.join(available)))
                        st.error('Unavailable sim(s): ')
                        st.code(str(' |  '.join(not_available)))

def add_new_client():
    client_platform = st.selectbox('Choose platform for client', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))
    client_name = st.text_area("Enter client name:")
    button = st.button("Add client")

    if button:
        with st.spinner("Adding new client..."):
            time.sleep(2)
            manage.add_client_directory(client_platform, client_name)

            st.success("{} sucessfully added!".format(client_name))

def add_new_account():
        """
        Adding new simcard. 
        
        How it works:
        1. Choose platform and new name. 
        2. Apps will produce a screenshot of the Whatsapp QR code.
        3. Scan the QR code using your mobile Whatsapp. 

        More:
        1. For every QR scan, a new simcard is created. 
        2. For every new name, even though it scanned by the same mobile, 
        it will create a new simcard. 
            Example: 
            new_name: Ammar_1 --> scanned by Ammar --> Ammar_1 simcard created
            new_name: Ammar_2 --> scanned by Ammar --> Ammar_2 simcard created
        3. QR code is refresh for every 15 seconds.
        """
        st.markdown("----------------------------------------------")
        st.info("ADD NEW simcard")
        select_platform_new_acc = st.selectbox('Where do you want to add the simcard(s)?', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))
        select_client = st.selectbox('Select Client', tuple([' ',]) + tuple(manage.get_all_client_dir(select_platform_new_acc)))
        # TODO: Adding client into open_driver

        if select_client != ' ':
            name = st.text_area("Enter Whatsapp simcard name:")
            get_name = manage.get_name(name)
            get_taken = manage.get_taken(name, select_platform_new_acc, select_client)

            if len(get_taken) == 0:
                button_add_account = st.button('Add simcard(s)')
                if button_add_account:
                    for name_acc in get_name:
                        try:
                            driver = manage.create_new_user_file(select_platform_new_acc,
                                                                select_client, 
                                                                name_acc)
                            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                        '//*[@id="app"]/div/div/div[2]/div[1]/div/div[2]/div/canvas')))

                            # take screenshot
                            manage.take_screenshot(driver)
                            st.success('QR code screenshot taken!')
                            ss = Image.open('./screenshot/QR_code.png')
                            manage.get_screenshot(ss)

                            # wait until all cache file get
                            f = WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.XPATH,
                                        '//*[@title="Search input textbox"]')))
                            st.success(name_acc + ' added!')
                            time.sleep(1)
                        except:
                            manage.deleted_account(select_platform_new_acc, name_acc)
            elif len(get_taken) == 1:
                st.write('simcard name--' + str(get_taken[0]) + ' is not available. Please choose another name!')
            else:
                st.write(str(', '.join(get_taken)) + ' are not available. Please choose another name!')
                        
def deleting_account():
        """
        To delete NOT-AVAILABLE simcard only.
        Not-available simcard is banned simcard.
        """
        st.markdown("----------------------------------------------")
        st.info("DELETING ACCOUNT")
        select_platform = st.selectbox('Select platform', 
                                ('',
                                'meniaga',
                                'AyuhMalaysia',
                                'Burner Accounts'))

        select_client = st.selectbox('Select client', tuple([' ',]) + tuple(manage.get_all_client_dir(select_platform)))

        if select_platform != '' and select_client != ' ':
            if select_platform == 'Burner Accounts':
                select_platform  = 'burner'

            button = st.button("Start Checking")
            
            if button:
                with st.spinner('Checking all simcard...'):
                    time.sleep(2)
                    accs = manage.get_all_sim_name(select_platform,select_client)
                st.subheader('List of simcard: ')
                st.code( ' | '.join(accs))

                with st.spinner("Checking banned simcard..."):
                    time.sleep(2)
                    available = manage.checking_banned_or_not(select_platform, select_client)[0]
                    not_available = manage.checking_banned_or_not(select_platform,select_client)[1]
                
                if len(not_available) == 0:
                    st.success('All simcard is valid! \n No simcard need to be to deleted!')

                elif len(not_available) == 1:
                    st.error('Unavailable simcard:')
                    st.code(+ '\n' + ' | '.join(not_available))
                    
                    for not_av in not_available:
                        st.error("Are you sure you want to delete the simcard?")
                        button_yes = st.button("Yes")
                        button_no  = st.button("No")
                        if  button_yes:
                            manage.deleted_account(select_platform, not_av)
                            st.caption("All the banned simcard has been deleted")
                        elif button_no:
                            st.caption("No simcard is deleted.")

def user_learning():
    """
    Tutorial for user.
    """
    st.title("Terms Used")
    st.markdown(
            """
            ### 👉 Platform
            > The product that we use to execute the blasting. 

                Example: Decoris, Meniaga, Ayuh Malaysia
            """)

    st.markdown(
            """
            ### 👉 Client
            > Client that used WhatApp Blaster service

                Example: Mc Donald, Restauran Maju
            
            """
    )
    st.markdown(
            """
            ### 👉 Simcard account
            > The sim card name that have been registered for the platform chosen by the client.

            > For every client, they have 3 simcard that can be used.

                Example:  011-123 4567
            
            """)

    st.markdown(
        """
        ### ✅ Full-path
        > Format
            Platform > Client > Simcard account
        > Example:  
            Meniaga > Restauran Maju > 011- 123 4567
        """
    )
    st.title("Steps")
    st.markdown(
        """
        ### How to setup a new simcard for new client?

            1. Add new client name on "Add client name" section
            2. Move to "Add new simcard(s)
            3. Choose the platform of the client. 
            4. Select client name that has been added previously. 
            5. Enter Whatsapp number a simcard.
            6. Click "Add simcard(s)" button.
        """
    )


def main_account_management():
    st.sidebar.warning(
        """
        Select option
        > Tutorial
            Learn how to setup a simcard.

        > simcard Setup
            Setup a new simcard.
        """
    )
    choice = st.selectbox('Select option',('', 'Tutorial', 'simcard Setup'))
    
    if choice == "Tutorial":
        user_learning()
        
    elif choice == "simcard Setup":
        select_option = st.selectbox('Select what do you want to do?', 
                                        ('',
                                        'Add new client', 
                                        'Add new simcard',
                                        'Check available simcard', 
                                        'Delete unavailable simcard'))

        if select_option == 'Add new client':
            add_new_client()

        elif select_option == 'Check available simcard':
            check_available_account()

        elif select_option == 'Add new simcard':
            add_new_account()

        elif select_option == 'Delete unavailable simcard':
            deleting_account()


if __name__ == '__main__':
    if option1=='Account Management':
        main_account_management()










