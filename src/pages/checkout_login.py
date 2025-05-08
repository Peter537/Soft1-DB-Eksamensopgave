import streamlit as st

def render():
    st.title("Login or continue as guest")

    st.write("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.selected_page = "Checkout"
        st.rerun()

    st.write("---")

    if st.button("Or continue as guest?"):
        st.session_state.selected_page = "Checkout"
        st.rerun()
        