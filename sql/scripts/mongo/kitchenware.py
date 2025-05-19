import pandas as pd
import random
from util import insert_many_postings
from model.posting import build_base_posting

def insert_kitchenware():
    print("Inserting clothes from clothes.csv")
    path = '../../datasets/kitchen_utensils/kitchenware.csv'
    df = pd.read_csv(path)

    id = 26768
    postings = []

    for _, row in df.iterrows():
        posting = build_base_posting(
            user_id=id,
            title=row['title'],
            price=row['price/value'],
            status="active",
            category="kitchenware",
            country="USA",
            city="New York",
            description=None if pd.isna(row['description']) else row['description'],
            item_count=random.randint(1, 10),
            specifications=[
                {"key": "Brand", "value": row['brand']}
            ]
        )
        postings.append(posting)
    
    insert_many_postings(postings)
    print("Done inserting kitchenware from kitchenware.csv \n")

