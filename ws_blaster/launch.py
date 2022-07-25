from ctypes import util
import streamlit as st

from PIL import Image
from ws_blaster.manage import Manage
from ws_blaster.utils import save_uploadedfile, open_driver
from PIL import Image
import pandas as pd
from ws_blaster.blasting import Blaster

# Hide streamlit header and footer
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)

# INVOKE logo and WS logo setup
invoke_logo_path = 'D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\images\\invoke_logo.jpg'
ws_logo_path = 'D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\images\\ws-logo.png'
invoke_logo = Image.open(invoke_logo_path)
ws_logo = Image.open(ws_logo_path)
st.sidebar.title('Whatsapp Blaster')
st.sidebar.image(invoke_logo)
st.image(ws_logo)
option1 = st.sidebar.selectbox('Select option', ('Blast Messages', 'Account Management'))

# BLASTING
blaster = Blaster(user_path='D:\\Desktop\\INVOKE\\ws_blaster\\ahilan-branch\\venvAhilan\\ws-blaster-prod\\Users')

if option1 == 'Blast Messages':

    option2 = st.selectbox('How do you to want define your contacts to blast?', ('Upload contact file (csv/xlsx)', 'Manual input',))

    # upload CSV file
    if option2 == 'Upload contact file (csv/xlsx)':
        contacts = st.file_uploader("")

        # check the file has '.csv' or not
        if contacts:
            if contacts.name[-3:] == 'csv':
                contacts = pd.read_csv(contacts, na_filter = False)
            else:
                contacts = pd.read_excel(contacts, na_filter = False)

            # select phone number column in the csv file  
            phone_number_column = st.selectbox('Select phone number column', [''] + list(contacts.columns))
            if phone_number_column != '':
                contacts = blaster.clean_numbers(contacts, phone_number_column)
        
    # upload phone number manually
    else:
        contacts = st.text_area("Key in phone number(s) to blast (Separate multiple phone numbers with a ',' e.g. 601111111111,601222222222)")
        contacts = contacts.split(',')
        contacts = [x.strip() for x in contacts]
        
        details = {'phone':contacts}
        dataframe = pd.DataFrame(details)
        blaster.extract_from_file()
        print(blaster.columns)
        
        #print(str(dataframe.columns[-1]))
        #print(type(str(dataframe.columns[-1])))
        contacts = blaster.clean_numbers(contact_df.columns) # return clean df
        #if len(contacts) == 0 :
            #st.write('Please make sure your numbers are in the right format')
        
image = Image.open('images/invoke_logo.jpg')
st.sidebar.title('Whatsapp Blaster')
st.sidebar.image(image)
option1 = st.sidebar.selectbox('Select option', ('Blast Messages', 'Account Management'))

##############################################################
# Blasting
##############################################################
blaster = Blaster(user_path="./Users")
if option1 == 'Blast Messages':
    st.image("images/whats-app-img.png")
    uploaded_file = st.file_uploader("Choose a file (csv)", type='csv')
    if uploaded_file is not None:
        blaster.extract_from_file(uploaded_file)
        col = st.selectbox('Select phone number column', blaster.columns)
        numbers = blaster.clean_numbers(col)
        st.json(blaster.contact_numbers_info)
