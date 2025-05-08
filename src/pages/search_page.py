import streamlit as st

def render(search_query):
    st.write(f"Debug: you searched for: '{search_query}'")

    col1, col2 = st.columns([1, 5])

    with col1:
        st.title("Price")
        st.write("placeholder for price slider")
    with col2:
        st.title("Search results")
        data = [
                {"Title": "Item 1", "Price": "$10"},
                {"Title": "Item 2", "Price": "$20"},
                {"Title": "Item 3", "Price": "$30"},
        ]

        for item in data:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(item["Title"])
            with col2:
                st.write(item["Price"])
            with col3:
                if st.button("View", key=item["Title"]):
                    st.session_state.selected_page = "Product Page"
                    st.rerun()
