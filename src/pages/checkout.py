import streamlit as st

def render():
    st.title("Checkout")

    st.write("Choose a payment method:")

    st.write("Show items / the shopping cart")

    if st.button("Pay"):
        st.session_state.selected_page = "Receipt"
        st.rerun()
