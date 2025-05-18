from db.redis.connection_redis import get_redis_client
from db.mongo.postings import get_posting_by_id
from bson import ObjectId


def increment_posting_view(posting_id):
    redis = get_redis_client()
    redis.zincrby("views:current_hour", 1, str(posting_id))


def delete_all_views():
    redis = get_redis_client()
    redis.delete("views:current_hour")


def get_top_10_postings():
    redis = get_redis_client()
    top_10_postings = redis.zrevrange("views:current_hour", 0, 9, withscores=True)
    top_10_postings = [(ObjectId(posting_id.decode("utf-8")), int(score)) for posting_id, score in top_10_postings]
    
    postings = []

    for posting_id, score in top_10_postings:
        posting = get_posting_by_id(posting_id)
        if posting:
            posting["views"] = score
            postings.append(posting)
            
    return postings
