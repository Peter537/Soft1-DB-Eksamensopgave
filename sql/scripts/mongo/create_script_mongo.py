from cars import insert_cars
from pcs import insert_all_pcs
from furniture import insert_all_furniture
from kitchenware import insert_kitchenware
from phones import insert_phones
from clothes import insert_all_clothes
from util import get_mongo_collection

def run_all_scripts():
    collection = get_mongo_collection()
    collection.delete_many({})

    collection = get_mongo_collection(collection_name="payment_log")
    collection.delete_many({})
    print("Cleared all existing postings.")
    
    insert_all_furniture()
    insert_kitchenware()
    insert_cars()
    insert_all_pcs()
    insert_phones()
    insert_all_clothes()

    print("All MongoDB postings inserted successfully.")
