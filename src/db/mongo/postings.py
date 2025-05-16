from db.mongo.connection_mongo import get_mongo_collection

def create_posting(title, description, price, user_id):
    print("Creating posting in MongoDB")
    conn = get_mongo_collection()

    posting = {
        "title": title,
        "description": description,
        "price": price,
        "user_id": user_id
    }

    result = conn.insert_one(posting)
    return result.inserted_id

def get_all_posting_by_search(search, skip=0, limit=20, min_price=None, max_price=None):
    conn = get_mongo_collection()
    search = search.lower()

    match_stage = {
        "$or": [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
            {"category": {"$regex": search, "$options": "i"}}
        ],
        "price": {"$exists": True}
    }

    # Optional price filtering
    if min_price is not None and max_price is not None:
        match_stage["price"] = {
            "$exists": True,
            "$ne": None,
            "$gte": min_price,
            "$lte": max_price
        }

    pipeline = [
        {"$match": match_stage},
        {"$sort": {"_id": -1}},
        {"$skip": skip},
        {"$limit": limit}
    ]

    results = list(conn.aggregate(pipeline))
    total_count = conn.count_documents(match_stage)
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
