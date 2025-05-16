import streamlit as st
from pages.screens import Screen
from db.postgres.users import login_user

def render():
    st.title("Login or continue as guest")

    st.write("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    login_clicked = st.button("Login")
    error_message = None

    if login_clicked:
        if not email or not password:
            error_message = "Please enter both email and password"
        else:
            login_result = login_user(email, password)
            
            if login_result is None:
                error_message = "Invalid username or password"
            else:
                user_id, name = login_result
                st.session_state.email = email
                st.session_state.name = name
                st.session_state.user_id = user_id
                st.session_state.selected_page = Screen.CHECKOUT.value
                st.session_state.logged_in = True
                st.rerun()

    if error_message:
        st.error(error_message)

    st.write("---")

    if st.session_state.logged_in == False:
        if st.button("Or continue as guest?"):
            st.session_state.selected_page = Screen.CHECKOUT.value
            st.rerun()
