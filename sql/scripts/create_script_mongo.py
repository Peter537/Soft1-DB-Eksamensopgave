
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

def check_for_connection():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["admin"]
        # Check if the connection is successful
        client.admin.command('ping')
        print("MongoDB connection successful.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return False
    return True

def insert_mongo_documents():
    if not check_for_connection():
        return
    
    # To be implemented
   

def run_all_scripts():
    check_for_connection()
    insert_mongo_documents()
    print("All mongoDB scripts executed successfully.")
    