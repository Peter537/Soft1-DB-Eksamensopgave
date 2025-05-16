from pymongo import MongoClient

def get_mongo_client():
    return MongoClient("mongodb://root:secretpassword@localhost:27017/?authSource=admin")

def get_mongo_collection(db_name="marketplace", collection_name="postings"):
    client = get_mongo_client()
    db = client[db_name]
    return db[collection_name]
