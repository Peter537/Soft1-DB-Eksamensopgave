from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

from db.mongo.connection_mongo import get_mongo_collection

def insert_payment_log(user_id: int, cart_items: list, total_amount: float):
    collection = get_mongo_collection(collection_name="payment_log")

    log_doc = {
        "user_id": user_id,
        "total_amount": total_amount,
        "created_at": datetime.now(),
        "items": []
    }

    for item in cart_items:
        log_doc["items"].append({
            "posting_id": ObjectId(item["posting_id"]),
            "seller_id": item["seller_id"],
            "title": item["title"],
            "price": item["price"],
            "description": item.get("description"),
            "quantity": item.get("quantity", 1),
            "review_id": item.get("review_id"),  # Could be None
            "specifications": item.get("specifications", [])
        })

    collection.insert_one(log_doc)
