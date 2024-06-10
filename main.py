import streamlit as st
from streamlit_option_menu import option_menu
from login import login
from deploy import deploy

def main():
    st.set_page_config(page_title="Phuean Jai", page_icon=":smiley:", layout="wide")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    with st.sidebar:
        st.image("image/speech.jpg", use_column_width=True)
        app = option_menu(
            menu_title='Phuean Jai',
            options=['Home', 'Account'],
            icons=['house', 'person'],
            default_index=0,
        )

    if app == "Home":
        st.title("Home")
        st.write("Welcome to the Home Page!")
    elif app == "Account":
        if st.session_state['logged_in']:
            deploy()
        else:
            login()
            if st.session_state['logged_in']:
                st.rerun()   # Refresh the app to reflect the login status

if __name__ == "__main__":
    main()
