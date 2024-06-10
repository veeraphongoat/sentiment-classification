import streamlit as st

def register():
    
    with st.form("register_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submit_button = st.form_submit_button(label="Register")

    if submit_button:
        if password != confirm_password:
            st.error("Passwords do not match")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters long")
        else:
            st.success("Registration successful!")
            # Add code here to handle registration logic
            # For example, save the data to a database or send it to an API