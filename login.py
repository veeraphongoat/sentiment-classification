import streamlit as st
from register import register

def login():
    st.title("Welcome :red[Phuean Jai] Speech to tone")

    with st.sidebar.expander("Login/Register"):
        choice = st.radio("Select Option", ["Login", "Register"])

    if choice == "Login":
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button(label="Login")
        
        if login_button:
            # Add your login logic here
            st.session_state['logged_in'] = True
            st.rerun()
    else:
        register()
