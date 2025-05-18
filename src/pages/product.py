import streamlit as st
from pages.screens import Screen
from db.mongo.postings import get_posting_by_id
from db.postgres.users import get_user_by_id
from db.postgres.review import get_all_reviews_by_posting_id
from db.redis.zincrby import increment_posting_view
from db.redis.cart import add_to_cart

def render(product_id):
    st.title("Product information")

    posting = get_posting_by_id(product_id)

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
        amount = st.selectbox("**Amount**", list(range(1, posting['item_count'] + 1)))

        if posting['item_count'] > 0:
            if st.button("Add to cart"):
                add_to_cart(posting['title'], st.session_state.session_id, posting['_id'], amount, posting['price'])
                st.success(f"Added {amount} of {posting['title']} to cart")

            def handle_buy_now():
                add_to_cart(posting['title'], st.session_state.session_id, posting['_id'], amount, posting['price'])
                st.session_state.selected_page = Screen.CART.value

            st.button("Buy now", on_click=handle_buy_now)
        else:
            st.warning("This item is out of stock.")

    st.write("---")
    
    if posting['specifications']:
        st.write("**Specifications**:")

        for spec in posting['specifications']:
            st.write(f"{spec['key']}: {spec['value']}")

    if posting['description']:
        st.write("---")
        st.write("**Description**:")
        st.write(posting['description'])
        st.write("---")

    reviews = get_all_reviews_by_posting_id(posting['_id'])

    if reviews['average_rating'] is not None and reviews['reviews']:
        st.write("**Reviews**:")
        st.write(f"**Average rating**: {reviews['average_rating']:.1f}")
        st.write('---')
        for i, review in enumerate(reviews['reviews']):
            st.write(f"**Review {i + 1}:**")
            st.write(f"Rating: {review['rating']}")
            st.write(f"Description: {review['description']}")
            st.write("---")
