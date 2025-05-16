import streamlit as st
from db.mongo.postings import get_all_categories
from pages.screens import Screen

def render():
    st.title("Recommendations")
    st.write("placeholder for recommendations")

    st.title("Categories")
    categories = get_all_categories()
    
    for i in range(0, len(categories), 4):
        row = categories[i:i+4]
        cols = st.columns(4)
        for col, category in zip(cols, row):
            with col:
                if st.button(category, key=category):
                    st.session_state.search_query = category
                    st.session_state.search_input = category  # Reset input box
                    st.session_state.search_page_num = 0
                    st.session_state.selected_page = Screen.SEARCH.value
                    st.rerun()

    st.title("Most viewed")
    st.write("placeholder for most viewed")
    # get from redis 
