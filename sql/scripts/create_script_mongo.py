from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

def get_mongo_collection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["marketplace"]
    return db["postings"]

def build_base_posting(user_id, title, price, status, category, country,
                       description=None, city=None, item_count=1, specifications=None):
    return {
        "user_id": user_id,
        "title": title,
        "price": price,
        "status": status,  # "active", "deleted", "inactive"
        "description": description,
        "category": category,
        "item_count": item_count,
        "location_city": city,
        "location_country": country,
        "specifications": specifications or []
    }

def insert_posting(posting_data):
    collection = get_mongo_collection()
    result = collection.insert_one(posting_data)
    print(f"Inserted document with _id: {result.inserted_id}")

# 🚗 Car example
def insert_cars():
    # Simulated user_id from SQL
    user_id = 101

    car_specs = [
        {"key": "brand", "value": "Toyota"},
        {"key": "model", "value": "Corolla"},
        {"key": "year", "value": "2019"},
        {"key": "mileage", "value": "50,000 km"}
    ]

    car_posting = build_base_posting(
        user_id=user_id,
        title="2019 Toyota Corolla",
        price=15000,
        status="active",
        category="car",
        country="Denmark",
        city="Copenhagen",
        specifications=car_specs
    )

    insert_posting(car_posting)

def insert_pcs():
    user_id = 102

    pc_specs = [
        {"key": "CPU", "value": "Intel i7"},
        {"key": "RAM", "value": "16GB"},
        {"key": "Storage", "value": "512GB SSD"}
    ]

    pc_posting = build_base_posting(
        user_id=user_id,
        title="High-end gaming PC",
        price=1200,
        status="active",
        category="computer",
        country="Germany",
        specifications=pc_specs
    )

    insert_posting(pc_posting)

def insert_mongo_documents():
    insert_cars()
    insert_pcs()
