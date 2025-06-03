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
        posting_id = item.get("posting_id")

        if not isinstance(posting_id, ObjectId):
            posting_id = ObjectId(posting_id)

        item_doc = {
            "posting_id": posting_id,
            "seller_id": item.get("seller_id"),
            "title": item.get("title"),
            "price": item.get("price"),
            "quantity": item.get("quantity", 1),
            "specifications": item.get("specifications", [])
        }
        if item.get("description") is not None:
            item_doc["description"] = item["description"]
        if item.get("review_id") is not None:
            item_doc["review_id"] = item["review_id"]
        log_doc["items"].append(item_doc)

    try:
        collection.insert_one(log_doc)
    except Exception as e:
        print(f"Error inserting payment log: {e}")


def get_payment_log_by_email(user_email: str):
    collection = get_mongo_collection(collection_name="payment_log")
    try:
        logs = collection.find({"user_email": user_email}).sort("created_at", -1)
        return list(logs)
    except Exception as e:
        print(f"Error fetching payment log by email: {e}")
        return []


def get_payment_log_by_id(log_id: str):
    collection = get_mongo_collection(collection_name="payment_log")
    try:
        log = collection.find_one({"_id": ObjectId(log_id)})
        return log
    except Exception as e:
        print(f"Error fetching payment log by id: {e}")
        return None


def update_payment_log_review_id(log_id: str, item_index: int, review_id: str):
    collection = get_mongo_collection(collection_name="payment_log")
    try:
        result = collection.update_one(
            {"_id": ObjectId(log_id), f"items.{item_index}.review_id": None},
            {"$set": {f"items.{item_index}.review_id": review_id}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error updating payment log review id: {e}")
        return False
    