import streamlit as st

def render():
    st.title("Product information")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Title: x")
        st.write("Price: $x")
        st.write("Seller: x")
        st.write("Location: x")

    with col2:
        amount = st.number_input("Amount", min_value=1, max_value=100, value=1, step=1)

        if st.button("Add to cart"):
            st.success(f"Added {amount} of item x to cart")

        if st.button("Buy now"):
            st.session_state.selected_page = "Cart"
            st.rerun()

    st.write("---")
    st.write("Specs: x")
    st.write("Description: x")
