import streamlit as st
from pages.screens import Screen
from db.postgres.users import login_user

def render():
    st.title("Login or continue as guest")


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
                if st.session_state.not_in_checkout:
                    st.session_state.selected_page = Screen.HOME.value
                else:
                    st.session_state.selected_page = Screen.CHECKOUT.value
                st.session_state.logged_in = True
                st.rerun()

    if error_message:
        st.error(error_message)

    st.write("---")

    if st.session_state.logged_in == False:
        if st.button("Or continue as guest?"):
            st.session_state.show_guest_inputs = True

    if st.session_state.get("show_guest_inputs", False):
        if st.session_state.not_in_checkout:
            st.session_state.selected_page = Screen.HOME.value
            st.session_state.not_in_checkout = False
            st.rerun()
        else:
            st.session_state.email = st.text_input("Email", key="guest_email")
            st.session_state.name = st.text_input("Name", key="guest_name")

            if st.button("Continue"):
                if not st.session_state.email or not st.session_state.name:
                    st.error("Please enter both email and name")
                else:
                    st.session_state.selected_page = Screen.CHECKOUT.value
                    st.session_state.show_guest_inputs = False
                    st.rerun()


    if st.button("Sign up"):
        st.session_state.selected_page = Screen.SIGNUP.value
        st.rerun()