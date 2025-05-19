import streamlit as st
from pages.screens import Screen
from db.mongo.postings import get_all_posting_by_search, get_max_price

def render():
    search_query = st.session_state.get("search_query", "")

    col1, col2 = st.columns([1, 5])
    
    with col1:
        st.title("Price")
        price_max = get_max_price(search_query)
        min_price, max_price = st.slider(
            "Select price range",
            min_value=0,
            max_value=int(price_max),
            value=(0, int(price_max))
        )

    # --- Pagination ---
    if "search_page_num" not in st.session_state:
        st.session_state.search_page_num = 0

    per_page = 20
    skip = st.session_state.search_page_num * per_page

    # Fetch filtered data from DB
    data, total_results = get_all_posting_by_search(
        search_query,
        skip=skip,
        limit=per_page,
        min_price=min_price,
        max_price=max_price
    )
    max_page = (total_results - 1) // per_page

    with col2:
        st.title(f"Search results ({total_results})")

        head_col1, head_col2, head_col3, head_col4 = st.columns([1, 3, 2, 1])
        with head_col1:
            st.write("ID")
        with head_col2:
            st.write(f"Title")
        with head_col3:
            st.write("Price")
        with head_col4:
            st.write("Action")

        for item in data:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
            with col1:
                st.write(item["_id"])
            with col2:
                st.write(f'{item["title"]}{" (sold out)" if item["status"] == "inactive" else ""}')
            with col3:
                st.write(item["price"])
            with col4:
                if st.button("View", key=f"view_{item['_id']}"):
                    st.session_state.product_id = item["_id"]
                    st.session_state.selected_page = Screen.PRODUCT.value
                    st.rerun()
            st.markdown("---")

        sub_col1, _, sub_col2, _, sub_col3 = st.columns([1, 1, 1, 1, 1])
        with sub_col1:
            if st.button("⬅️ Prev") and st.session_state.search_page_num > 0:
                st.session_state.search_page_num -= 1
                st.rerun()
        with sub_col2:
            st.markdown(f"**Page {st.session_state.search_page_num + 1} of {max_page + 1}**")
        with sub_col3:
            if st.button("➡️ Next") and st.session_state.search_page_num < max_page:
                st.session_state.search_page_num += 1
                st.rerun()
