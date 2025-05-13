from pymongo import MongoClient
import pandas as pd
import random

def get_mongo_collection():
    client = MongoClient("mongodb://root:secretpassword@localhost:27017/?authSource=admin")
    db = client["marketplace"]
    return db["postings"]


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


def insert_cars():
    car_match_ids = {
        "Volvo": 27807,
        "Hyundai": 26816,
        "BMW": 29803,
        "Mercedes-Benz": 27322,
        "Volkswagen": 27115,
        "Nissan": 28275,
        "Toyota": 27375
    }

    used_cars(car_match_ids)
    used_cars1(car_match_ids)
    used_cars2(car_match_ids)


def used_cars(ids):
    print("Inserting used cars from used_cars.csv")
    path = '../../datasets/used_cars.csv'
    df = pd.read_csv(path).dropna()

    postings = []

    for _, row in df.iterrows():
        user_id = next((ids[car] for car in ids if car.lower() in row['title'].lower()), 101)

        posting = build_base_posting(
            user_id=user_id,
            title=row['title'],
            price=row['price'],
            status="active",
            category="car",
            country="Nigerian",
            city=row['location'],
            description=(
                f"Used {row['title']} for sale. The car is from the year {row['year']} and has a mileage of "
                f"{row['odometer']} km. It is a {row['fuel']} with {row['transmission']} transmission."
            ),
            specifications=[
                {"key": "Year", "value": row['year']},
                {"key": "Mileage", "value": row['odometer']},
                {"key": "Fuel Type", "value": row['fuel']},
                {"key": "Transmission", "value": row['transmission']},
                {"key": "Engine", "value": row['engine']},
                {"key": "Color", "value": row['paint']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting used cars from used_cars.csv \n")


def used_cars1(ids):
    print("Inserting used cars from used_cars1.csv")
    path = '../../datasets/used_cars1.csv'
    df = pd.read_csv(path).dropna()

    postings = []

    for _, row in df.iterrows():
        title = f"{row['mark']} {row['model']}"
        user_id = next((ids[car] for car in ids if car.lower() in row['mark'].lower()), 101)

        posting = build_base_posting(
            user_id=user_id,
            title=title,
            price=row['price'],
            status="active",
            category="car",
            country="Japan",
            description=(
                f"Used {title} for sale. The car is from the year {row['year']} and has a mileage of "
                f"{row['mileage']} km. It is a {row['fuel']} with {row['transmission']} transmission."
            ),
            specifications=[
                {"key": "Year", "value": row['year']},
                {"key": "Mileage", "value": row['mileage']},
                {"key": "Fuel Type", "value": row['fuel']},
                {"key": "Transmission", "value": row['transmission']},
                {"key": "Engine capacity", "value": row['engine_capacity']},
                {"key": "Drive", "value": row['drive']},
                {"key": "Hand drive", "value": row['hand_drive']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting used cars from used_cars1.csv \n")


def used_cars2(ids):
    print("Inserting used cars from used_cars2.csv")
    path = '../../datasets/used_cars2.csv'
    df = pd.read_csv(path)

    postings = []

    for _, row in df.iterrows():
        user_id = next((ids[car] for car in ids if car.lower() in row['title'].lower()), 101)

        posting = build_base_posting(
            user_id=user_id,
            title=row['title'],
            price=row['Price'],
            status="active",
            category="car",
            country="UK",
            description=(
                f"Used {row['title']} for sale. The car is from the year {row['Registration_Year']} and has a mileage of "
                f"{row['Mileage(miles)']} km. It is a {row['Fuel type']} with {row['Gearbox']} transmission."
            ),
            specifications=[
                {"key": "Year", "value": row['Registration_Year']},
                {"key": "Mileage", "value": row['Mileage(miles)']},
                {"key": "Fuel Type", "value": row['Fuel type']},
                {"key": "Gearbox", "value": row['Gearbox']},
                {"key": "Engine", "value": row['Engine']},
                {"key": "Doors", "value": row['Doors']},
                {"key": "Seats", "value": row['Seats']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting used cars from used_cars2.csv \n")


def insert_pcs():
    print("Inserting pcs from pc.csv")
    path = '../../datasets/pc.csv'
    df = pd.read_csv(path).dropna()

    ids = {
        "Apple": 28573,
        "HP": 27990,
        "Lenovo": 28227,
        "Dell": 26856,
        "Asus": 28949,
        "Samsung": 26773,
        "MSI": 28415
    }

    postings = []

    for _, row in df.iterrows():
        user_id = next((ids[brand] for brand in ids if brand.lower() in row['brand'].lower()), 101)

        posting = build_base_posting(
            user_id=user_id,
            title=row['name'],
            price=row['price'],
            status="active",
            category="pc",
            country="Denmark",
            city="Copenhagen",
            description=(
                f"{row['name']} for sale. It has a {row['processor']} processor and {row['Ram']} RAM. "
                f"The GPU is {row['GPU']}."
            ),
            item_count=random.randint(1, 10),
            specifications=[
                {"key": "Brand", "value": row['brand']},
                {"key": "Spec Rating", "value": row['spec_rating']},
                {"key": "OS", "value": row['OS']},
                {"key": "RAM", "value": row['Ram']},
                {"key": "Ram Type", "value": row['Ram_type']},
                {"key": "GPU", "value": row['GPU']},
                {"key": "CPU", "value": row['CPU']},
                {"key": "Processor", "value": row['processor']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting pcs from pc.csv \n")



def insert_phones():
    print("Inserting phones from phones.csv")
    path = '../../datasets/phones.csv'
    df = pd.read_csv(path)

    ids = {
        "Apple": 28573,
        "Samsung": 26773,
        "Google": 28235,
        "OnePlus": 36178,
        "Xiaomi": 28315,
        "Oppo": 26802,
        "Vivo": 26818
    }

    postings = []

    for _, row in df.iterrows():
        user_id = next((ids[brand] for brand in ids if brand.lower() in row['Brand'].lower()), 101)

        posting = build_base_posting(
            user_id=user_id,
            title=row['Model'],
            price=row['Price ($)'],
            status="active",
            category="phone",
            country="Germany",
            city="Berlin",
            description=(
                f'{row['Model']} for sale. It has a storage of {row['Storage ']} and RAM of {row['RAM ']}. '
                f'The camera is {row['Camera (MP)']} MP and the battery capacity is {row['Battery Capacity (mAh)']} mAh.'
            ),
            item_count=random.randint(1, 10),
            specifications=[
                {"key": "Brand", "value": row['Brand']},
                {"key": "Storage", "value": row['Storage ']},
                {"key": "RAM", "value": row['RAM ']},
                {"key": "Screen Size (inches)", "value": row['Screen Size (inches)']},
                {"key": "Camera", "value": row['Camera (MP)']},
                {"key": "Battery Capacity (mAh)", "value": row['Battery Capacity (mAh)']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting phones from phones.csv \n")


def insert_shoes():
    print("Inserting shoes from shoes.csv")
    path = '../../datasets/shoes.csv'
    df = pd.read_csv(path)

    ids = {
        "Nike": 31028,
        "Adidas": 28244,
        "Reebok": 30894,
        "Converse": 33974,
        "Puma": 28037,
        "Skechers": 32791
    }
    
    postings = []

    for _, row in df.iterrows():

        user_id = next((ids[brand] for brand in ids if brand.lower() in row['Brand'].lower()), 101)

        posting = build_base_posting(
            user_id=user_id,
            title=row['Model'],
            price=row['Price (USD)'],
            status="active",
            category="shoes",
            country="Italy",
            city="Rome",
            description=(
                f'{row['Model']} for sale. It has a size of {row['Size']} and is available in {row['Color']}. '
                f'The material is {row['Material']} and the type is {row['Type']}.'
            ),
            item_count=random.randint(1, 10),
            specifications=[
                {"key": "Brand", "value": row['Brand']},
                {"key": "Size", "value": row['Size']},
                {"key": "Color", "value": row['Color']},
                {"key": "Material", "value": row['Material']},
                {"key": "Type", "value": row['Type']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting shoes from shoes.csv \n")

def insert_clothes():
    print("Inserting clothes from clothes.csv")
    path = '../../datasets/clothes.csv'
    df = pd.read_csv(path)

    ids = {
        "Nike": 31028,
        "Adidas": 28244,
        "Reebok": 30894,
        "Converse": 33974,
        "Puma": 28037,
        "Skechers": 32791
    }

    postings = []

    for _, row in df.iterrows():

        user_id = next((ids[brand] for brand in ids if brand.lower() in row['Brand'].lower()), 101)

        posting = build_base_posting(
            user_id=user_id,
            title=row['Brand'] + " " + row['Category'] + f" ({row['Size']})",
            price=row['Price'],
            status="active",
            category=row['Category'],
            country="France",
            city="Paris",
            description=(
                f'{row['Category']} from {row['Brand']} for sale. It has a size of {row['Size']} and is available in {row['Color']}. '
                f'The material is {row['Material']}.'
            ),
            item_count=random.randint(1, 10),
            specifications=[
                {"key": "Brand", "value": row['Brand']},
                {"key": "Size", "value": row['Size']},
                {"key": "Color", "value": row['Color']},
                {"key": "Material", "value": row['Material']},
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting clothes from clothes.csv \n")

def run_all_scripts():
    collection = get_mongo_collection()
    collection.delete_many({})
    print("Cleared all existing postings.")

    insert_cars()
    insert_pcs()
    insert_phones()
    insert_shoes()
    insert_clothes()

    print("All MongoDB postings inserted successfully.")
