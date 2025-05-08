import streamlit as st
from pages import home, account, cart, search_page, product, checkout_login, checkout, receipt

st.set_page_config(page_title="DB Exam (title tbd!)", layout="wide", initial_sidebar_state="collapsed")

# Hide sidebar completely (ish)
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# Session state for page selection
if "selected_page" not in st.session_state:
    st.session_state.selected_page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    
# --- TOP NAVBAR ---
col1, col2, col3 = st.columns([2, 5, 2])

# Left: Home button
with col1:
    if st.button("🏠 Home"):
        st.session_state.selected_page = "Home"

# Center: Search bar and button side by side
with col2:
    search_col1, search_col2 = st.columns([5, 1])
    with search_col1:
        search_query = st.text_input(
            "", 
            placeholder="Search...",
            label_visibility="collapsed"
        )
    with search_col2:
        if st.button("🔍", key="search"):
            st.session_state.selected_page = "Search"
            st.rerun()


# Right: Account and Cart buttons
with col3:
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.session_state.logged_in:
            if st.button("👤 Account"):
                st.session_state.selected_page = "Account"
            
            if st.button("🚪 Logout"):
                st.session_state.selected_page = "Home"
                st.session_state.logged_in = False
                st.session_state.product_id = None
                st.rerun()
        else:
            if st.button("👤 Login"):
                st.session_state.selected_page = "Checkout Login"

    with sub_col2:
        if st.button(f"🛒 Cart"):
            st.session_state.selected_page = "Cart"

st.markdown("---")

# --- PAGE ROUTING ---
page = st.session_state.selected_page

if page == "Home":
    home.render()

elif page == "Account":
    account.render()

elif page == "Cart":
    cart.render()

elif page == "Search":
    search_page.render(search_query)

elif page == "Product Page":
    product.render(st.session_state.product_id)

elif page == "Checkout Login":
    checkout_login.render()

elif page == "Checkout":
    checkout.render()

elif page == "Receipt":
    receipt.render()
