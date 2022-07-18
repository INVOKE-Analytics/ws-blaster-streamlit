import streamlit as st

# Hide streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def subheader(word):
    return st.subheader(word)

def button(word):
    return st.button(word)

def spinner(word):
    return st.spinner(word)

def write(word):
    return st.write(word)

def selectbox(word):
    return st.selectbox(word)

def image(word):
    return st.image(word)