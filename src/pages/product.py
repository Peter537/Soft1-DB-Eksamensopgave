import streamlit as st
from pages.screens import Screen
from db.mongo.postings import get_posting_by_id
from db.postgres.users import get_user_by_id
from db.redis.zincrby import increment_posting_view
from db.redis.cart import add_to_cart

def render(product_id):
    st.title("Product information")

    posting = get_posting_by_id(product_id)
    print(f"user_id{posting['user_id']}")

    increment_posting_view(product_id)

    seller = get_user_by_id(posting['user_id'])
    print(posting)

    print("user", seller)

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Product ID**: {posting['_id']}")
        st.write(f"**Title**: {posting['title']}")
        st.write(f"**Price**: {posting['price']}")
        st.write(f"**Seller**: {seller.get('name', 'Unknown')}")
        
        if posting['location_city'] and posting['location_country']:
            st.write(f"**Location**: {posting['location_city']}, {posting['location_country']}")

    with col2:
        amount = st.number_input("**Amount**", min_value=1, max_value=posting['item_count'], value=1, step=1)

        if st.button("Add to cart"):
            add_to_cart(posting['title'], st.session_state.session_id, posting['_id'], amount, posting['price'])
            st.success(f"Added {amount} of {posting['title']} to cart")

        if st.button("Buy now"):
            add_to_cart(posting['title'], st.session_state.session_id, posting['_id'], amount, posting['price'])
            st.session_state.selected_page = Screen.CART.value
            st.rerun()

    st.write("---")
    
    if posting['specifications']:
        st.write("**Specifications**:")

        for spec in posting['specifications']:
            st.write(f"{spec['key']}: {spec['value']}")

    if posting['description']:
        st.write("---")
        st.write("**Description**:")
        st.write(posting['description'])
