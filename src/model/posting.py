
def build_base_posting(user_id, title, price, status, category, country,
                       description=None, city=None, item_count=1, specifications=None):
    posting = {
        "user_id": user_id,
        "title": title,
        "price": price,
        "status": status,
        "category": category,
        "item_count": item_count,
        "location_country": country
    }

    if description:
        posting["description"] = description
    if city:
        posting["location_city"] = city
    if specifications:
        valid_specs = [
            {"key": spec["key"], "value": spec["value"]}
            for spec in specifications
            if spec.get("key") and spec.get("value")
        ]
        if valid_specs:
            posting["specifications"] = valid_specs

    return posting
