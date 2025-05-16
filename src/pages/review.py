import streamlit as st
from db.postgres.review import create_new_review

def render():
    st.title("Review page")

    st.write(f"debug {st.session_state.order_id}")

    user_id = -1  # the seller
    reviewed_user_id = st.session_state.user_id
    reviewed_posting = "posting_id"  # fix later

    description = st.text_area("Write your review here", key="review_text")
    rating = st.number_input("Rating", min_value=1, max_value=5, step=1, key="rating")

    if 1 <= rating <= 5:
        if st.button("Submit Review"):
            # Replace with actual logic
            # create_new_review(
            #     order_id=st.session_state.order_id,
            #     user_id=user_id,
            #     reviewed_user_id=reviewed_user_id,
            #     posting_id=reviewed_posting,
            #     description=description,
            #     rating=rating
            # )
            st.success("Review submitted!")
    else:
        st.warning("Please select a rating between 1 and 5")
