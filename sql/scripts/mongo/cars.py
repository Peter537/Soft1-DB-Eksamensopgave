import pandas as pd
from util import insert_many_postings, build_base_posting

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
    path = '../../datasets/cars/used_cars.csv'
    df = pd.read_csv(path).dropna()

    postings = []

    for _, row in df.iterrows():
        user_id = next((ids[car] for car in ids if car.lower() in row['title'].lower()), 1)

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
    path = '../../datasets/cars/used_cars1.csv'
    df = pd.read_csv(path).dropna()

    postings = []

    for _, row in df.iterrows():
        title = f"{row['mark']} {row['model']}"
        user_id = next((ids[car] for car in ids if car.lower() in row['mark'].lower()), 1)

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
    path = '../../datasets/cars/used_cars2.csv'
    df = pd.read_csv(path)

    postings = []

    for _, row in df.iterrows():
        user_id = next((ids[car] for car in ids if car.lower() in row['title'].lower()), 1)

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
