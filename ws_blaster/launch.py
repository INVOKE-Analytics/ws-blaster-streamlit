import time
import streamlit as st

from PIL import Image
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

image = Image.open('images/invoke_logo.jpg')
st.sidebar.title('Whatsapp Blaster')
st.sidebar.image(image)
option1 = st.sidebar.selectbox(
    'Select option', ('Blast Messages', 'Account Management'))

##############################################################
# Blasting
##############################################################
blaster = Blaster(user_path="./Users")
if option1 == 'Blast Messages':
    st.image("images/whats-app-img.png")

    # Upload csv file to extract phone numbers
    uploaded_file = st.file_uploader(
        "Choose a file with phone numbers (csv)", type='csv')
    if uploaded_file is not None:
        blaster.extract_from_file(uploaded_file)
        col = st.selectbox('Select phone number column', blaster.columns)
        numbers = blaster.clean_numbers(col)
        st.json(blaster.contact_numbers_info)

    # Upload pictures
    if uploaded_file:
        uploaded_imgs = st.file_uploader(
            "Choose imgs you want to blast (png)", type='png', accept_multiple_files=True)
        blaster.save_files_to_blast(uploaded_imgs)

    # Variations of the same message
    if uploaded_file:
        message_variations = st.select_slider(
            "How many variations of the same message do you have?", options=list(range(1, 5)))
        for i in range(message_variations):
            message = st.text_area("Enter message: ", key=i)
            blaster.add_message_variations_to_blast(message)

    # Choose the set of platform to blast from
    if uploaded_file:
        platform = st.selectbox("Choose set of accounts to blast from",
                                ('Select', 'meniaga', 'AyuhMalaysia', "Burner Accounts"))

    # Start Blasting
    if uploaded_file and platform != "Select":
        st.info("Setting up Web Drivers")
        blaster.setup_drivers_in_account(platform, headless=True)
        start = st.button('Start Blasting')
        if start:
            my_progress = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.1)
                # st.write('hello')
                my_progress.progress(percent_complete + 1)
            st.success("Messages sent to all numbers")
