import streamlit as st

from db.mongo.payment_log import get_payment_log_by_email
from pages.screens import Screen

def render():

    col1, col2 = st.columns(2)
    with col1:
        st.title("Account Page")

        st.write(f"User ID: {st.session_state.user_id}")
        st.write(f"Email: {st.session_state.email}")
        st.write(f"Name: {st.session_state.name}")

    with col2:
        if st.button("Make new posting"):
            st.session_state.selected_page = Screen.POSTING.value
            st.rerun()

        if st.button("View own postings"):
            st.session_state.selected_page = Screen.MY_POSTINGS.value
            st.rerun()
            
    st.write("---")

    st.title("Order history")

    data = get_payment_log_by_email(st.session_state.email)
    
    if not data:
        st.write("No orders yet...")
    else:
        st.write("---")
        for order in data:
            st.write(f"Order ID: {order['_id']}")
            st.write(f"Total Price: {order['total_amount']}")
            st.write(f"Date: {order['created_at']}")
            st.write("Items:")
            for item in order['items']:
                st.write(f"- {item['title']} (Quantity: {item['quantity']})")

            if st.button("Make review?", key=f"review_{order['_id']}"):
                st.session_state.order_id = order['_id']
                st.session_state.selected_page = Screen.REVIEW.value
                st.rerun()
                print("Review button clicked")

            st.write("---")

