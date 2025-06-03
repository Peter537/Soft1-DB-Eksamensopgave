import streamlit as st
from db.mongo.postings import get_postings_by_user_id

def render():

    if "my_postings_page_num" not in st.session_state:
        st.session_state.my_postings_page_num = 0

    per_page = 10
    skip = st.session_state.my_postings_page_num * per_page

    # Fetch paginated data + total count from DB
    postings, total_results = get_postings_by_user_id(
        st.session_state.user_id,
        skip=skip,
        limit=per_page
    )
    max_page = (total_results - 1) // per_page

    st.title(f"My Postings ({total_results if total_results else 0})")

    if total_results == 0:
        st.write("No postings yet...")
        return

    for posting in postings:
        st.write(f"**Title:** {posting['title']}")
        st.write(f"**Price:** ${posting['price']}")
        st.write(f"**Category:** {posting['category']}")
        if posting.get("description"):
            st.write(f"**Description:** {posting['description']}")
        loc = posting.get("location_city")
        country = posting.get("location_country")
        if country:
            st.write(f"**Location:** {loc + ', ' if loc else ''}{country}")
        st.write(f"**Item Count:** {posting['item_count']}")
        
        if posting.get("specifications"):
            st.write("**Specifications:**")
            for spec in posting.get("specifications", []):
                st.write(f"  - **{spec['key']}**: {spec['value']}")
                
        st.markdown("---")

    # Pagination controls
    col1, _, col2, _, col3, = st.columns([1, 1, 1, 1, 1])
    with col1:
        if st.button("⬅️ Prev") and st.session_state.my_postings_page_num > 0:
            st.session_state.my_postings_page_num -= 1
            st.rerun()
    with col2:
        st.markdown(f"**Page {st.session_state.my_postings_page_num + 1} of {max_page + 1}**")
    with col3:
        if st.button("➡️ Next") and st.session_state.my_postings_page_num < max_page:
            st.session_state.my_postings_page_num += 1
            st.rerun()
