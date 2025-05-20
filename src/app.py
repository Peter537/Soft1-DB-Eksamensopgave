import streamlit as st

st.set_page_config(page_title="DB Exam (title tbd!)", layout="wide", initial_sidebar_state="collapsed")

hide_sidebar = """
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

from pages.screens import Screen
from pages import home, account, cart, search_page, product, checkout_login, checkout, receipt, make_posting, review, my_postings, sign_up
import uuid
from streamlit_cookies_manager import EncryptedCookieManager
import time

# 2) Init cookie manager
cookies = EncryptedCookieManager(prefix="app_", password="YOUR_SECRET")
if not cookies.ready():
    st.stop()

# 3) Read raw cookie, if present
raw = cookies.get("session_id")  # returns None or the string we wrote

sid = None
if raw:
    try:
        # Expect format "<uuid>--<timestamp>"
        stored_uuid, stored_ts = raw.split("--")
        if time.time() - float(stored_ts) < 3600:  # less than 1 hour old?
            sid = stored_uuid
    except Exception:
        # on any parsing error, we'll just issue a new one
        sid = None

# 4) If no valid sid, generate new and write cookie
if sid is None:
    sid = str(uuid.uuid4())

    # store both the uuid and the current time
    cookies["session_id"] = f"{sid}--{time.time()}"
    cookies.save()

st.session_state.session_id = sid
st.write(f"🔑 Your session ID is: `{sid}`")


# Session state for page selection
if "selected_page" not in st.session_state:
    st.session_state.selected_page = Screen.HOME.value

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "search_input" not in st.session_state:
    st.session_state.search_input = ""

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())
    
if "not_in_checkout" not in st.session_state:
    st.session_state.not_in_checkout = False

# --- TOP NAVBAR ---
col1, col2, col3 = st.columns([2, 5, 2])

# Left: Home button
with col1:
    if st.button("🏠 Home"):
        st.session_state.selected_page = Screen.HOME.value

# Center: Search bar and button side by side
with col2:
    search_col1, search_col2 = st.columns([5, 1])
    with search_col1:
        new_input = st.text_input(" ", placeholder="Search...", label_visibility="collapsed", value=st.session_state.search_input)
        st.session_state.search_input = new_input 

    with search_col2:
        if st.button("🔍", key="search"):
            st.session_state.search_query = st.session_state.search_input 
            st.session_state.search_page_num = 0
            st.session_state.selected_page = Screen.SEARCH.value
            st.rerun()


# Right: Account and Cart buttons
with col3:
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        if st.session_state.logged_in:
            if st.button("👤 Account"):
                st.session_state.selected_page = Screen.ACCOUNT.value
            
            if st.button("🚪 Logout"):
                st.session_state.selected_page = Screen.HOME.value
                st.session_state.logged_in = False
                st.session_state.product_id = None
                st.session_state.not_in_checkout = False
                st.rerun()
        else:
            if st.button("👤 Login"):
                st.session_state.not_in_checkout = True
                st.session_state.selected_page = Screen.CHECKOUT_LOGIN.value

    with sub_col2:
        if st.button(f"🛒 Cart"):
            st.session_state.selected_page = Screen.CART.value

st.markdown("---")

# --- PAGE ROUTING ---
page = st.session_state.selected_page

match page:
    case Screen.HOME.value:
        home.render()
    case Screen.ACCOUNT.value:
        account.render()
    case Screen.CART.value:
        cart.render()
    case Screen.SEARCH.value:
        search_page.render()
    case Screen.PRODUCT.value:
        product.render(st.session_state.product_id)
    case Screen.CHECKOUT_LOGIN.value:
        checkout_login.render()
    case Screen.CHECKOUT.value:
        checkout.render()
    case Screen.RECEIPT.value:
        receipt.render()
    case Screen.POSTING.value:
        make_posting.render()
    case Screen.REVIEW.value:
        review.render()
    case Screen.MY_POSTINGS.value:
        my_postings.render()
    case Screen.SIGNUP.value:
        sign_up.render()
