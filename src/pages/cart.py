import streamlit as st
from pages.screens import Screen
from db.redis.cart import get_cart, remove_from_cart

def render():
    st.title("Shopping Cart")

    cart = get_cart(st.session_state.session_id)
    st.write("---")
    
    st.write("Items in your cart:")

    header_col1, header_col2, header_col3, header_col4 = st.columns([3, 1, 1, 1])
    
    with header_col1:
        st.write("Item")
    with header_col2:
        st.write("Quantity")
    with header_col3:
        st.write("Price")
    with header_col4:
        st.write("Action")

    total_price = 0

    for item in cart["items"]:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.write(item["postingId"])
        with col2:
            st.write(item['quantity'])
        with col3:
            total_price += item['quantity'] * item['price']
            st.write(item['price'])
        with col4:
            if st.button("Remove", key=item["postingId"]):
                remove_from_cart(st.session_state.session_id, item["postingId"])
                st.success(f"Removed {item['postingId']} from cart")
                st.rerun()

        st.write("---")

    st.write(f"Total price: {total_price}")

    if st.button("Checkout"):
        if st.session_state.logged_in:
            st.session_state.selected_page = Screen.CHECKOUT.value
        else:
            st.session_state.selected_page = Screen.CHECKOUT_LOGIN.value
        st.rerun()
        