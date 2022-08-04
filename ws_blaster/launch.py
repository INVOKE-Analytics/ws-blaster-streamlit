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
    # TODO: Check if unavailable and send pictures
    if uploaded_file and platform != "Select":
        start = st.button('Start Blasting')
        percent_complete = 0
        if start:
            st.info("Setting up Web Drivers")
            blaster.setup_drivers_in_account(platform, headless=True)
            my_progress = st.progress(0.0)
            for i, number in enumerate(numbers):
                acc, driver = blaster.nav_to_number(number)
                message = blaster.get_random_message()
                status = blaster.send_message(driver, message)
                my_progress.progress((i+1)/len(numbers))
                blaster.apply_random_wait(i)
            st.success("Messages sent to all numbers")
            blaster.close_drivers()
