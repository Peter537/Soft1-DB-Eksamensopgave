import streamlit as st
from db.postgres.users import create_user
from pages.screens import Screen

def render():
    st.title("Sign Up")
    st.write("Create a new account")

    email = st.text_input("Email")
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if not email or not password or not name:
            st.error("Please fill in all fields")
        else:
            user_id = create_user(email, name, password)
            
            st.session_state.email = email
            st.session_state.name = name
            st.session_state.user_id = user_id
            st.session_state.logged_in = True

            if st.session_state.not_in_checkout:
                st.session_state.selected_page = Screen.HOME.value
            else:
                st.session_state.selected_page = Screen.CHECKOUT.value
            st.toast("Account created successfully!")
            st.rerun()
