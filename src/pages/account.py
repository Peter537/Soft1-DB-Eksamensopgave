import streamlit as st

def render():
    st.title("Account Page")

    st.write(f"User ID: {st.session_state.user_id}")
    st.write(f"Email: {st.session_state.email}")
    st.write(f"Name: {st.session_state.name}")
    
    st.write("Phone: 123-456-7890")

    st.write("Order history")
    
    data = [
        {"#": 1, "Title": "Product 1", "Price": "$10.00", "Status": "Delivered"},
        {"#": 2, "Title": "Product 2", "Price": "$20.00", "Status": "Pending"},
        {"#": 3, "Title": "Product 3", "Price": "$30.00", "Status": "Cancelled"},
    ]

    for item in data:
        col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
        with col1:
            st.write(item["#"])
        with col2:
            st.write(item["Title"])
        with col3:
            st.write(item["Price"])
        with col4:
            st.write(item["Status"])

        st.markdown("---")
