import streamlit as st
from db.mongo.postings import create_posting

def render():
    st.title("Make A New Posting")

    if "specifications" not in st.session_state:
        st.session_state.specifications = []

    user_id = st.session_state.user_id
    title = st.text_input("Title")
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["car", "furniture", "dress", "shoes", "phone", "pc", "kitchenware", "t-shirt", "jacket", "sweater", "jeans"])
    description = st.text_area("Description")
    location_city = st.text_input("Location City")
    location_country = st.text_input("Location Country")
    item_count = st.number_input("Item Count", min_value=1, step=1)

    st.subheader("Specifications")

    with st.form(key="spec_form", clear_on_submit=True):
        spec_key = st.text_input("Specification Key")
        spec_value = st.text_input("Specification Value")
        add_spec = st.form_submit_button("Add Specification")
        if add_spec and spec_key and spec_value:
            st.session_state.specifications.append({"key": spec_key, "value": spec_value})

    if st.session_state.specifications:
        for i, spec in enumerate(st.session_state.specifications):
            st.write(f"**{i+1}. {spec['key']}**: {spec['value']}")

    required_filled = bool(title.strip()) and price > 0 and bool(location_country.strip())

    if not required_filled:
        st.warning("Please fill in all required fields: Title, Price, and Location Country.")

    if st.button("Create Posting", disabled=not required_filled):
        id = create_posting(
            user_id, title, price, category,
            description if description.strip() else None,
            location_city if location_city.strip() else None,
            location_country, item_count, st.session_state.specifications
        )
        st.success(f"Posting created successfully with ID: {id}")
