import streamlit as st

def render():
    st.title("Shopping Cart")
    
    cart_items = [
        {"Product": "Item 1", "Amount": 2, "Price": "$20.00"},
        {"Product": "Item 2", "Amount": 1, "Price": "$30.00"},
        {"Product": "Item 3", "Amount": 3, "Price": "$50.00"},
    ]

    st.write("Items in your cart:")
    for item in cart_items:
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        with col1:
            st.write(item["Product"])
        with col2:
            st.write(item["Amount"])
        with col3:
            st.write(item["Price"])
        with col4:
            if st.button("Remove", key=item["Product"]):
                st.success(f"Removed {item['Product']} from cart")

    st.write("---")
    st.write("Total price: $100.00")

    if st.button("Checkout"):
        if st.session_state.logged_in:
            st.session_state.selected_page = "Checkout"
        else:
            st.session_state.selected_page = "Checkout Login"
        st.rerun()
        