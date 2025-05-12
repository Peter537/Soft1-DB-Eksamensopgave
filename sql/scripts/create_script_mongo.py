from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

import pandas as pd

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

def insert_cars():
    PATHS = [
        '../../datasets/cars/used_cars.csv',
        '../../datasets/cars/used_cars_2.csv',
        '../../datasets/cars/used_cars_3.csv'
    ]

    user_ids = [101, 102, 103, 104, 105]

    for path in PATHS:
        df = pd.read_csv(path, sep=',', skiprows=1)
        df = df.drop_duplicates(subset=['title'])

        for index, row in df.iterrows():
            user_id = 101
            car_posting = build_base_posting(
                user_id=user_id,
                title=row['title'],
                price=row['price'],
                status="active",
                category="car",
                country=row['country'],
                description=row['description'],
                city=row['city'],
                item_count=row['item_count'],
                specifications=[
                    {"key": "Mileage", "value": row['mileage']},
                    {"key": "Year", "value": row['year']},
                    {"key": "Fuel Type", "value": row['fuel_type']}
                ]
            )
            insert_posting(car_posting)
            #user_id = user_ids[(user_ids.index(user_id) + 1) % len(user_ids)]

def insert_pcs():
    paths = [
        '../../datasets/pcs/used_pcs.csv',
        '../../datasets/pcs/used_pcs_2.csv',
        '../../datasets/pcs/used_pcs_3.csv'
    ]

    user_ids = [101, 102, 103, 104, 105]

    for path in paths:
        df = pd.read_csv(path, sep=',', skiprows=1)
        df = df.drop_duplicates(subset=['title'])

        for index, row in df.iterrows():
            user_id = 101
            pc_posting = build_base_posting(
                user_id=user_id,
                title=row['title'],
                price=row['price'],
                status="active",
                category="pc",
                country=row['country'],
                description=row['description'],
                city=row['city'],
                item_count=row['item_count'],
                specifications=[
                    {"key": "RAM", "value": row['ram']},
                    {"key": "Storage", "value": row['storage']},
                    {"key": "Processor", "value": row['processor']}
                ]
            )
            insert_posting(pc_posting)
            #user_id = user_ids[(user_ids.index(user_id) + 1) % len(user_ids)]

def run_all_scripts():
    collection = get_mongo_collection()

    collection.delete_many({})
    print("Cleared all existing postings.")

    insert_cars()
    insert_pcs()
    print("All MongoDB postings inserted successfully.")

