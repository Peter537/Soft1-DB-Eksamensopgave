import pandas as pd
import random
from util import insert_many_postings
from model.posting import build_base_posting

def insert_phones():
    print("Inserting phones from phones.csv")
    path = '../datasets/electronic/phones.csv'
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
        user_id = next((ids[brand] for brand in ids if brand.lower() in row['Brand'].lower()), 1)

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
