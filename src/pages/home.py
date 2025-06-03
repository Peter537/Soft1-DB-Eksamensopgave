import streamlit as st
from db.mongo.postings import get_all_categories
from db.redis.zincrby import get_top_10_postings
from pages.screens import Screen

def render():
    st.title("Categories")
    categories = get_all_categories()
    
    for i in range(0, len(categories), 4):
        row = categories[i:i+4]
        cols = st.columns(4)
        for col, category in zip(cols, row):
            with col:
                if st.button(category, key=category):
                    st.session_state.search_query = category
                    st.session_state.search_input = category
                    st.session_state.search_page_num = 0
                    st.session_state.selected_page = Screen.SEARCH.value
                    st.rerun()


    st.title("Most viewed")
    top_10_postings = get_top_10_postings()

    if top_10_postings:
        st.write("---")
        max_cols = 3

        for i in range(0, len(top_10_postings), max_cols):
            row = top_10_postings[i:i+max_cols]
            cols = st.columns(max_cols)
            for col, posting in zip(cols, row):
                with col:
                    title_shortened = posting["title"][:25] + "..." if len(posting["title"]) > 20 else posting["title"]
                    st.write(f"**{title_shortened}**")
                    st.write(f"Price: ${posting['price']}")
                    st.write(f"Views: {posting['views']}")
                    if st.button("View", key=posting["_id"]):
                        st.session_state.product_id = posting["_id"]
                        st.session_state.selected_page = Screen.PRODUCT.value
                        st.rerun()
    else:
        st.write("No postings have been viewed yet.")
