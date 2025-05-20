from db.mongo.connection_mongo import get_mongo_collection
from model.posting import build_base_posting
import re

def create_posting(user_id, title, price, category, description, location_city, location_country, item_count, specifications):
    print("Creating posting in MongoDB")

    conn = get_mongo_collection()

    posting = build_base_posting(
        user_id=user_id,
        title=title,
        price=price,
        status="active",
        category=category,
        description=description,
        city=location_city,
        country=location_country,
        item_count=item_count,
        specifications=specifications
    )

    result = conn.insert_one(posting)
    return result.inserted_id


def get_postings_by_user_id(user_id, skip=0, limit=20):
    """
    Returns (postings_page, total_count) for a given user.
    """
    conn = get_mongo_collection()
    query = {"user_id": user_id}

    total = conn.count_documents(query)
    cursor = (
        conn
        .find(query)
        .skip(skip)
        .limit(limit)
        .sort("_id", 1)  # optional: keep a consistent ordering
    )

    return list(cursor), total


def get_all_posting_by_search(search, skip=0, limit=20, min_price=None, max_price=None):
    conn = get_mongo_collection()

    query = {}
    if search:
        escaped = re.escape(search)
        regex = {"$regex": f".*{escaped}.*", "$options": "i"}
        query['$or'] = [
            {'title': regex},
            {'category': regex}
        ]

    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter['$gte'] = min_price
        if max_price is not None:
            price_filter['$lte'] = max_price
        query['price'] = price_filter

    pipeline = [
        {'$match': query},
        {'$sort': {'_id': -1}},
        {'$facet': {
            'results': [
                {'$skip': skip},
                {'$limit': limit}
            ],
            'total_count': [
                {'$count': 'count'}
            ]
        }}
    ]

    aggregation = list(conn.aggregate(pipeline))
    if not aggregation:
        return [], 0

    facet = aggregation[0]
    results = facet.get('results', [])
    count_list = facet.get('total_count', [])
    total_count = count_list[0]['count'] if count_list else 0

    return results, total_count


def get_posting_by_id(posting_id):
    print("Getting posting by ID in MongoDB")

    conn = get_mongo_collection()

    posting = conn.find_one({"_id": posting_id})

    return posting


def get_all_categories():
    print("Getting all categories in postings in MongoDB")
    conn = get_mongo_collection()

    categories = conn.find(
        {},
        {
            "category": 1
        }
    )

    categories = [category["category"] for category in categories]

    return list(set(categories))


def get_max_price(search):
    conn = get_mongo_collection()
    search = search.lower()

    pipeline = [
        {
            "$match": {
                "$or": [
                    {"title": {"$regex": search, "$options": "i"}},
                    {"description": {"$regex": search, "$options": "i"}},
                    {"category": {"$regex": search, "$options": "i"}}
                ],
                "price": {"$exists": True}
            }
        },
        {
            "$addFields": {
                "price_str": {
                    "$cond": [
                        {"$isNumber": "$price"},
                        {"$toString": "$price"},
                        "$price"
                    ]
                }
            }
        },
        {
            "$addFields": {
                "price_numeric": {
                    "$convert": {
                        "input": {
                            "$replaceAll": {
                                "input": {
                                    "$replaceAll": {
                                        "input": "$price_str",
                                        "find": ",",
                                        "replacement": ""
                                    }
                                },
                                "find": "\\$",
                                "replacement": ""
                            }
                        },
                        "to": "double",
                        "onError": 0,
                        "onNull": 0
                    }
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "max_price": {"$max": "$price_numeric"}
            }
        }
    ]

    result = list(conn.aggregate(pipeline))
    return result[0]["max_price"] if result else 1000


def decrease_item_count(posting_id, quantity):
    print("Decreasing item count in MongoDB")

    conn = get_mongo_collection()

    posting = conn.find_one({"_id": posting_id})
    
    if posting and posting["item_count"] > 0:
        # if item_count is 1 then set status to sold and item_count to 0
        new_item_count = posting["item_count"] - quantity

        if new_item_count == 0:
            conn.update_one(
                {"_id": posting_id},
                {"$set": {"item_count": 0, "status": "inactive"}}
            )
        else:
            conn.update_one(
                {"_id": posting_id},
                {"$set": {"item_count": new_item_count}}
            )


def delete_posting(posting_id):
    print("Deleting posting in MongoDB")

    conn = get_mongo_collection()

    conn.update_one(
        {"_id": posting_id},
        {"$set": {"status": "deleted"}}
    )
