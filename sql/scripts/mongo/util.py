from pymongo import MongoClient

def get_mongo_collection(collection_name="postings"):
    client = MongoClient("mongodb://root:secretpassword@localhost:27017/?authSource=admin")
    db = client["marketplace"]
    return db[collection_name]

def build_base_posting(user_id, title, price, status, category, country,
                       description=None, city=None, item_count=1, specifications=None):
    return {
        "user_id": user_id,
        "title": title,
        "price": price,
        "status": status,
        "description": description,
        "category": category,
        "item_count": item_count,
        "location_city": city,
        "location_country": country,
        "specifications": specifications or []
    }

def insert_many_postings(postings):
    if postings:
        collection = get_mongo_collection()
        collection.insert_many(postings)
