import pandas as pd
import random
from util import insert_many_postings
from model.posting import build_base_posting

def insert_shoes():
    print("Inserting shoes from shoes.csv")
    path = '../../datasets/clothing/shoes.csv'
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

        user_id = next((ids[brand] for brand in ids if brand.lower() in row['Brand'].lower()), 1)

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
    path = '../../datasets/clothing/clothes.csv'
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

        user_id = next((ids[brand] for brand in ids if brand.lower() in row['Brand'].lower()), 1)

        posting = build_base_posting(
            user_id=user_id,
            title=row['Brand'] + " " + row['Category'] + f" ({row['Size']})",
            price=row['Price'],
            status="active",
            category=row['Category'].lower(),
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


def insert_all_clothes():
    insert_clothes()
    insert_shoes()