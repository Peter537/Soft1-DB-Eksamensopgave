import pandas as pd
import random
from util import insert_many_postings, build_base_posting


def insert_all_pcs():
    insert_pcs()
    insert_pcs2()


def insert_pcs():
    print("Inserting pcs from pc.csv")
    path = '../../datasets/electronic/pc.csv'
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
        user_id = next((ids[brand] for brand in ids if brand.lower() in row['brand'].lower()), 1)

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


def insert_pcs2():
    print("Inserting pcs from pc2.csv")
    path = '../../datasets/electronic/pc2.csv'
    df = pd.read_csv(path)

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
        user_id = next((ids[brand] for brand in ids if brand.lower() in row['Brand'].lower()), 1)

        title = f"{row['Brand']} {row['Processor']} {row['RAM']} GB"

        posting = build_base_posting(
            user_id=user_id,
            title=title,
            price=row['Price'],
            status="active",
            category="pc",
            country="Denmark",
            city="Copenhagen",
            description=row['Product_Description'],
            item_count=random.randint(1, 10),
            specifications=[
                {"key": "Brand", "value": row['Brand']},
                {"key": "Screen_Size", "value": row['Screen_Size']},
                {"key": "RAM", "value": row['RAM']},
                {"key": "Processor", "value": row['Processor']},
                {"key": "GPU", "value": row['GPU']},
                {"key": "GPU_Type", "value": row['GPU_Type']},
                {"key": "Resolution", "value": row['Resolution']},
                {"key": "Condition", "value": row['Condition']}
            ]
        )
        postings.append(posting)

    insert_many_postings(postings)
    print("Done inserting pcs from pc2.csv \n")

