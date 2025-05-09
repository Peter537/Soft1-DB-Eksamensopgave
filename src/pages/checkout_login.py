import streamlit as st
from pages.screens import Screen

def render():
    st.title("Login or continue as guest")

    st.write("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.selected_page = Screen.CHECKOUT.value
        st.session_state.logged_in = True
        st.rerun()

    st.write("---")

    if st.session_state.logged_in == False:
        if st.button("Or continue as guest?"):
            st.session_state.selected_page = Screen.CHECKOUT.value
            st.rerun()
