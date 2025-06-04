from bson import ObjectId
from db.mongo.connection_mongo import get_mongo_collection
from model.posting import build_base_posting
import re


def ensure_objectid(id):
    if isinstance(id, ObjectId):
        return id
    try:
        return ObjectId(id)
    except Exception:
        print(f"Invalid ObjectId: {id}")
        return None


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

    try:
        result = conn.insert_one(posting)
        return result.inserted_id
    except Exception as e:
        print(f"Error creating posting: {e}")
        return None


def get_postings_by_user_id(user_id, skip=0, limit=20):
    conn = get_mongo_collection()
    query = {"user_id": user_id}
    try:
        total = conn.count_documents(query)
        cursor = conn.find(query).skip(skip).limit(limit).sort("_id", 1)
        return list(cursor), total
    except Exception as e:
        print(f"Error fetching postings by user_id: {e}")
        return [], 0


def normalize_price_pipeline(price_field="price_str"):
    return [
        {
            "$addFields": {
                price_field: {
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
                                        "input": "$" + price_field,
                                        "find": ",",
                                        "replacement": ""
                                    }
                                },
                                "find": "\\$|kr| |€|£|\\s",
                                "replacement": ""
                            }
                        },
                        "to": "double",
                        "onError": 0,
                        "onNull": 0
                    }
                }
            }
        }
    ]


def get_all_posting_by_search(search: str, skip: int = 0, limit: int = 20, min_price: float = None, max_price: float = None):
    conn = get_mongo_collection()
    query = {}

    if search:
        escaped = re.escape(search)
        regex = {"$regex": f".*{escaped}.*", "$options": "i"}
        query['$or'] = [
            {'title': regex},
            {'category': regex},
            {'description': regex}
        ]

    price_match = {}
    
    if min_price is not None:
        price_match['$gte'] = min_price
    if max_price is not None:
        price_match['$lte'] = max_price
    
    pipeline = []
    
    if query:
        pipeline.append({"$match": query})
    
    pipeline.extend(normalize_price_pipeline())
    
    if price_match:
        pipeline.append({"$match": {"price_numeric": price_match}})

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
    try:
        aggregation = list(conn.aggregate(pipeline))
        if not aggregation:
            return [], 0
        facet = aggregation[0]
        results = facet.get("results", [])
        count_list = facet.get("total_count", [])
        total_count = count_list[0]["count"] if count_list else 0
        return results, total_count
    
    except Exception as e:
        print(f"Error in get_all_posting_by_search: {e}")
        return [], 0


def get_posting_by_id(posting_id):
    conn = get_mongo_collection()
    oid = ensure_objectid(posting_id)
    if not oid:
        return None
    try:
        posting = conn.find_one({"_id": oid})
        return posting
    except Exception as e:
        print(f"Error in get_posting_by_id: {e}")
        return None


def get_all_categories():
    conn = get_mongo_collection()
    try:
        categories = conn.distinct("category")
        return categories
    except Exception as e:
        print(f"Error getting categories: {e}")
        return []


def get_max_price(search: str) -> float:
    conn = get_mongo_collection()
    escaped = re.escape(search)
    regex = {"$regex": f".*{escaped}.*", "$options": "i"}
    pipeline = [
        {
            "$match": {
                "$or": [
                    {"title": regex},
                    {"description": regex},
                    {"category": regex}
                ],
                "price": {"$exists": True}
            }
        }
    ]
    pipeline.extend(normalize_price_pipeline())
    pipeline.append({
        "$group": {
            "_id": None,
            "max_price": {"$max": "$price_numeric"}
        }
    })
    try:
        result = list(conn.aggregate(pipeline))
        if result:
            return result[0].get("max_price", 0.0)
        return 1000.0
    except Exception as e:
        print(f"Error in get_max_price: {e}")
        return 1000.0


def decrease_item_count(posting_id, quantity):
    conn = get_mongo_collection()
    oid = ensure_objectid(posting_id)
    if not oid:
        return
    try:
        posting = conn.find_one({"_id": oid})
        if posting and posting.get("item_count", 0) > 0:
            new_item_count = posting["item_count"] - quantity
            if new_item_count <= 0:
                conn.update_one(
                    {"_id": oid},
                    {"$set": {"item_count": 0, "status": "inactive"}}
                )
            else:
                conn.update_one(
                    {"_id": oid},
                    {"$set": {"item_count": new_item_count}}
                )
    except Exception as e:
        print(f"Error in decrease_item_count: {e}")
