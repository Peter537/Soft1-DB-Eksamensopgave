import streamlit as st
from db.mongo.postings import get_all_posting_by_user_id

def render():
    st.title("My Postings")

    postings = get_all_posting_by_user_id(st.session_state.user_id)

    if not postings:
        st.write("No postings yet...")
    else:
        for posting in postings:
            st.write(f"**Title:** {posting['title']}")
            st.write(f"**Price:** ${posting['price']}")
            st.write(f"**Category:** {posting['category']}")
            st.write(f"**Description:** {posting['description']}")
            st.write(f"**Location:** {posting['location_city']}, {posting['location_country']}")
            st.write(f"**Item Count:** {posting['item_count']}")
            st.write("**Specifications:**")
            for spec in posting['specifications']:
                st.write(f"&emsp; **- {spec['key']}**: {spec['value']}")
            st.write("---")
