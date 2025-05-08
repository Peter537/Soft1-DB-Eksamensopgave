import streamlit as st

def render(search_query):
    st.write(f"Debug: you searched for: '{search_query}'")

    col1, col2 = st.columns([1, 5])

    with col1:
        st.title("Price")
        min, max = st.slider("Price range", 0, 1000, (0, 1000), 1)

        st.write(f"Debug: Min: {min}, Max: {max}") # Debugging line

    with col2:
        st.title("Search results")

        data = [
                {"#": 1, "Title": "Product 1", "Price": "$10.00"},
                {"#": 2, "Title": "Product 2", "Price": "$20.00"},
                {"#": 3, "Title": "Product 3", "Price": "$30.00"},
        ]

        for item in data:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
            with col1:
                st.write(item["#"])
            with col2:
                st.write(item["Title"])
            with col3:
                st.write(item["Price"])
            with col4:
                if st.button("View", key=item["Title"]):
                    st.session_state.product_id = item["#"]
                    st.session_state.selected_page = "Product Page"
                    st.rerun()

            st.markdown("---")
