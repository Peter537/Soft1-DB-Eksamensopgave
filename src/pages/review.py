import streamlit as st
from db.postgres.review import create_new_review
from db.mongo.payment_log import get_payment_log_by_id, update_payment_log_review_id

def render():
    st.title("Review page")

    st.write(f"debug {st.session_state.order_id}")
    st.write("---")

    payment_log = get_payment_log_by_id(st.session_state.order_id)

    for item in payment_log["items"]:
        st.write(f"Title: {item['title']}")
        st.write(f"Price: {item['price']}")
        st.write(f"Quantity: {item['quantity']}")
    
        rating = st.selectbox(f"Rate {item['title']}", [1, 2, 3, 4, 5], key=f"rating_{item['posting_id']}")
        review_text = st.text_area(f"Write a review for {item['title']}", key=f"review_{item['posting_id']}")

        if st.button(f"Submit review for {item['title']}", key=f"submit_{item['posting_id']}"):
            review_id = create_new_review(
                user_id=item['seller_id'],
                reviewed_user_id=payment_log['user_id'],
                reviewed_posting=item['posting_id'],
                rating=rating,
                description=review_text,
            )

            update_payment_log_review_id(
                log_id=payment_log["_id"],
                item_index=payment_log["items"].index(item),
                review_id=review_id
            )

            st.success(f"Review for {item['title']} submitted successfully!")

        st.write("---")
