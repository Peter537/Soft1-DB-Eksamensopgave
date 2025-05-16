import streamlit as st

def render():
    st.title("Receipt")
    st.write("placeholder for receipt")

    for item in st.session_state.bought_items:
        st.write(item["posting_id"])
        st.write(item['title'])
        st.write(item['price'])
        st.write(item['quantity'])
        st.write("---")
    