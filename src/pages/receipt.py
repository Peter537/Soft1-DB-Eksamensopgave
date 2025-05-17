import streamlit as st

def render():
    st.title("Receipt")

    title, price, quantity, seller_id = st.columns(4)
    with title:
        st.write("**Title**")
    with price:
        st.write("**Price**")
    with quantity:
        st.write("**Quantity**")
    with seller_id:
        st.write("**Seller ID**")

    total_amount = 0    

    for item in st.session_state.bought_items:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write(item["title"])
        with col2:
            st.write(f"${item['price']}")
            total_amount += item["price"]
        with col3:
            st.write(item["quantity"])
        with col4:
            st.write(item["seller_id"])
        st.write("---")
    
    st.write(f"**Total Amount: ${total_amount}**")
    st.write("Thank you for your purchase!")