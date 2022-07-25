import streamlit as st

from PIL import Image
from ws_blaster.manage import Manage
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