import streamlit as st
from pages.screens import Screen

from bson import ObjectId
from db.mongo.postings import get_posting_by_id
from db.mongo.payment_log import insert_payment_log
from db.redis.cart import get_cart, clear_cart, remove_from_cart

def render():
    st.title("Checkout")

    cart = get_cart(st.session_state.session_id)
    st.write("Choose a payment method:")
    selected_payment = st.selectbox("Select payment method", ["Credit Card", "PayPal", "Bank Transfer"])

    total_price = 0
    enriched_items = []

    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    for item in cart["items"]:
        posting_id = ObjectId(item["postingId"])
        posting = get_posting_by_id(posting_id)

        if not posting:
            continue  # skip if not found

        quantity = item.get("quantity", 1)
        price = float(posting.get("price", 0))
        total_price += price * quantity

        with col1:
            st.write(posting["title"])
        with col2:
            st.write(quantity)
        with col3:
            st.write(f"{price:.2f}")
        with col4:
            if st.button("Remove", key=f"remove_{posting_id}"):
                remove_from_cart(st.session_state.session_id, item["postingId"])
                st.success(f"Removed {posting['title']} from cart")
                st.rerun()

        # Build enriched item for logging
        enriched_item = {
            "posting_id": posting["_id"],
            "seller_id": posting["user_id"], 
            "title": posting["title"],
            "price": price,
            "description": posting.get("description"),
            "quantity": quantity,
            "specifications": posting.get("specifications", [])
        }

        enriched_items.append(enriched_item)

    st.write(f"**Total price: {total_price:.2f}**")

    if st.button("Pay"):
        user_id = st.session_state.get("user_id", 1) # TODO: what should we do when user is not logged in? should a user only have to give email and phone number instead?
        insert_payment_log(user_id, enriched_items, total_price)

        clear_cart(st.session_state.session_id)  
        st.session_state.bought_items = enriched_items
        st.session_state.selected_page = Screen.RECEIPT.value
        st.rerun()
