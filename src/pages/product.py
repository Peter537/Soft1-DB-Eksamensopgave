import streamlit as st
from pages.screens import Screen

def render(product_id):
    st.title("Product information")

    st.write(f"Debug: you are viewing product with id: {product_id}")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Title: Computer 3000x hyper")
        st.write("Price: $1000.00")
        st.write("Seller: Amazon.com")
        st.write("Location: Seattle, WA")

    with col2:
        amount = st.number_input("Amount", min_value=1, max_value=100, value=1, step=1)

        if st.button("Add to cart"):
            st.success(f"Added {amount} of items product_id: {product_id} to cart")

        if st.button("Buy now"):
            st.session_state.selected_page = Screen.CART.value
            st.rerun()

    st.write("---")
    st.write("Specs: CPU: x, RAM: x, Storage: x")
    st.write("Description: Computer with x CPU, x RAM, and x Storage...")
