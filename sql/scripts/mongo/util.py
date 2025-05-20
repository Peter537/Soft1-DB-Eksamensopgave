from pymongo import MongoClient

def get_mongo_collection(collection_name="postings"):
    client = MongoClient("mongodb://localhost:27017")
    db = client["marketplace"]
    return db[collection_name]

def insert_many_postings(postings):
    if postings:
        collection = get_mongo_collection()
        collection.insert_many(postings)
