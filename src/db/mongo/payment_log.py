from bson import ObjectId
from datetime import datetime
from db.mongo.connection_mongo import get_mongo_collection

def insert_payment_log(user_email: str, cart_items: list, total_amount: float):
    collection = get_mongo_collection(collection_name="payment_log")

    log_doc = {
        "user_email": user_email,
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
            "quantity": item.get("quantity", 1),

            "specifications": item.get("specifications", [])
        })

        if item.get("description") is not None:
            log_doc["items"][-1]["description"] = item["description"]

        if item.get("review_id") is not None:
            log_doc["items"][-1]["review_id"] = item["review_id"]

    collection.insert_one(log_doc)

def get_payment_log_by_email(user_email: str):
    collection = get_mongo_collection(collection_name="payment_log")
    logs = collection.find({"user_email": user_email}).sort("created_at", -1)
    return list(logs)

def get_payment_log_by_id(log_id: str):
    collection = get_mongo_collection(collection_name="payment_log")
    log = collection.find_one({"_id": ObjectId(log_id)})
    return log

# set the review_id for a specific item in the payment log
def update_payment_log_review_id(log_id: str, item_index: int, review_id: str):
    collection = get_mongo_collection(collection_name="payment_log")
    collection.update_one(
        {"_id": log_id, f"items.{item_index}.review_id": None},
        {"$set": {f"items.{item_index}.review_id": review_id}}
    )