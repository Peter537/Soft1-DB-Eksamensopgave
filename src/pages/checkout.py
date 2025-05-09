import streamlit as st
from pages.screens import Screen

def render():
    st.title("Checkout")

    st.write("Choose a payment method:")
    payment_methods = ["Credit Card", "PayPal", "Bank Transfer"]
    selected_payment = st.selectbox("Select payment method", payment_methods)

    st.write("Show items / the shopping cart")

    cart_items = [
        {"Product": "Item 1", "Amount": 2, "Price": "$20.00"},
        {"Product": "Item 2", "Amount": 1, "Price": "$30.00"},
        {"Product": "Item 3", "Amount": 3, "Price": "$50.00"},
    ]

    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    for item in cart_items:
        with col1:
            st.write(item["Product"])
        with col2:
            st.write(item["Amount"])
        with col3:
            st.write(item["Price"])
        with col4:
            if st.button("Remove", key=item["Product"]):
                st.success(f"Removed {item['Product']} from cart")

    if st.button("Pay"):
        st.session_state.selected_page = Screen.RECEIPT.value
        st.rerun()
