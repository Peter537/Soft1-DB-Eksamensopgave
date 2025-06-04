import pandas as pd
import random
from util import insert_many_postings
from model.posting import build_base_posting

def insert_all_furniture():
    insert_furniture()
    insert_furniture1()


def insert_furniture():
    print("Inserting furniture from furniture.csv")
    path = '../datasets/furniture/furniture.csv'
    df = pd.read_csv(path).dropna()

    postings = []

    for _, row in df.iterrows():
        user_id = 1

        posting = build_base_posting(
            user_id=user_id,
            title=row['furniture'],
            price=row['price'],
            status="active",
            category="furniture",
            country="Sweden",
            city="Stockholm",
            description=(f'{row['furniture']} for sale for {row['price']}.'),
            item_count=random.randint(1, 10),
            specifications=[
                {"key": "Type", "value": row['type']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting furniture from furniture.csv \n")


def insert_furniture1():
    print("Inserting furniture from furniture1.csv")
    path = '../datasets/furniture/ikea.csv'
    df = pd.read_csv(path)

    postings = []

    for _, row in df.iterrows():
        user_id = 30527 # IKEA only

        posting = build_base_posting(
            user_id=user_id,
            title=row['name'],
            price=row['price'],
            status="active",
            category="furniture",
            country="Sweden",
            city="Stockholm",
            description=(
                f'{row['name']} for sale for {row['price']}. {row['short_description']}'
            ),
            item_count=random.randint(1, 10),
            specifications=[
                {"key": "Type", "value": row['category']},
                {"key": "Designer", "value": row['designer']},
                {"key": "Depth", "value": row['depth']},
                {"key": "Height", "value": row['height']},
                {"key": "Width", "value": row['width']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting furniture from furniture1.csv \n")
