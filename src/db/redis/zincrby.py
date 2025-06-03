from db.redis.connection_redis import get_redis_client
from db.mongo.postings import get_posting_by_id
from bson import ObjectId

conn = get_redis_client()

def increment_posting_view(posting_id):
    conn.zincrby("views:current_hour", 1, str(posting_id))


def delete_all_views():
    conn.delete("views:current_hour")


def get_top_10_postings():
    top_postings_raw = conn.zrevrange("views:current_hour", 0, 24, withscores=True)
    postings = []
    count = 0
    for posting_id_bytes, score in top_postings_raw:
        try:
            posting_id_str = posting_id_bytes.decode("utf-8")

            try:
                posting_id = ObjectId(posting_id_str)
            except Exception as e:
                continue
            posting = get_posting_by_id(posting_id)
            if posting:
                posting["views"] = int(score)
                postings.append(posting)
                count += 1
                if count >= 10:
                    break
        except Exception as e:
            continue
    return postings
