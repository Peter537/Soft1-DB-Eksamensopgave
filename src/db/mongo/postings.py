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


def get_all_posting_by_search(
    search: str,
    skip: int = 0,
    limit: int = 20,
    min_price: float = None,
    max_price: float = None
):
    conn = get_mongo_collection()

    # 1) Build the “text‐match” part of the query
    query = {}
    if search:
        escaped = re.escape(search)
        regex = {"$regex": f".*{escaped}.*", "$options": "i"}

        query['$or'] = [
            {'title':       regex},
            {'category':    regex},
            {'description': regex},
        ]

    # 2) We’re going to convert `price` → `price_numeric`, then match on that
    #    If the user gave min_price or max_price, we’ll build a second filter
    price_match = {}
    if min_price is not None:
        price_match['$gte'] = min_price
    if max_price is not None:
        price_match['$lte'] = max_price

    # 3) Build the aggregation pipeline
    pipeline = []

    # 3a) First, apply the text‐only portion of the match (title/category/description).
    #     We do NOT match on `price` yet, because price is still a string in many docs.
    if query:
        pipeline.append({"$match": query})

    # 3b) Now add a field called “price_str” that ensures every doc has a string in `price_str`.
    #     If price is already a number, we toString() it; if it's a string, leave as‐is.
    pipeline.append({
        "$addFields": {
            "price_str": {
                "$cond": [
                    {"$isNumber": "$price"},
                    {"$toString": "$price"},
                    {"$ifNull": ["$price", "0"]}  
                    # if price is missing or null, treat as "0"
                ]
            }
        }
    })

    # 3c) Strip out commas, currency symbols, etc., and convert to double → “price_numeric”
    pipeline.append({
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
                            "find": "\\$|kr| |€|£",  
                            # you might need to add other symbols (e.g. “kr”, “ ” [NBSP], “€”, “£”)
                            "replacement": ""
                        }
                    },
                    "to": "double",
                    "onError": 0,
                    "onNull":  0
                }
            }
        }
    })

    # 3d) Now that we have “price_numeric”, we can filter on any min_price/max_price
    if price_match:
        # only include this stage if the user asked for some price bounds
        pipeline.append({
            "$match": {"price_numeric": price_match}
        })

    # 3e) Finally, sort, skip, limit, and facet to get total_count
    pipeline.append({"$sort": {"_id": -1}})
    pipeline.append({
        "$facet": {
            "results": [
                {"$skip": skip},
                {"$limit": limit}
            ],
            "total_count": [
                {"$count": "count"}
            ]
        }
    })

    # 4) Run the aggregation
    aggregation = list(conn.aggregate(pipeline))
    if not aggregation:
        return [], 0

    facet = aggregation[0]
    results = facet.get("results", [])
    count_list = facet.get("total_count", [])
    total_count = count_list[0]["count"] if count_list else 0

    return results, total_count


def get_posting_by_id(posting_id):

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


def get_max_price(search: str) -> float:
    conn = get_mongo_collection()
    escaped = re.escape(search)
    regex = {"$regex": f".*{escaped}.*", "$options": "i"}

    pipeline = [
        {
            "$match": {
                "$or": [
                    {"title":       regex},
                    {"description": regex},
                    {"category":    regex}
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
                        {"$ifNull": ["$price", "0"]}  
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
                                        "input": {
                                            "$replaceAll": {
                                                "input": "$price_str",
                                                "find": ",",
                                                "replacement": ""
                                            }
                                        },
                                        "find": "\\$|kr| |€|£",
                                        "replacement": ""
                                    }
                                },
                                "find": "\\s",  # strip any whitespace as well
                                "replacement": ""
                            }
                        },
                        "to": "double",
                        "onError": 0,
                        "onNull":  0
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
    if result:
        return result[0].get("max_price", 0.0)
    # If no documents at all matched, you can pick a sensible default:
    return 1000.0


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
