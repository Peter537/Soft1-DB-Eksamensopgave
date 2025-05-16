import json
from db.redis.connection_redis import get_redis_client

redis = get_redis_client()

def get_cart_key(session_id):
    return f"cart:{session_id}"


def add_to_cart(session_id, posting_id, quantity, price):
    key = f"cart:{session_id}"
    cart_json = redis.get(key)

    if cart_json:
        cart = json.loads(cart_json)
    else:
        cart = {
            "sessionId": session_id,
            "items": []
        }

    posting_id = str(posting_id)

    for item in cart["items"]:
        if item["postingId"] == posting_id:
            item["quantity"] += quantity
            break
    else:
        cart["items"].append({
            "postingId": posting_id,
            "quantity": quantity,
            "price": price
        })

    redis.set(key, json.dumps(cart))


def remove_from_cart(session_id, posting_id):
    key = get_cart_key(session_id)
    cart_data = redis.get(key)
    if not cart_data:
        return

    cart = json.loads(cart_data)
    cart["items"] = [item for item in cart["items"] if item["postingId"] != posting_id]
    redis.set(key, json.dumps(cart))


def get_cart(session_id):
    key = get_cart_key(session_id)
    cart_data = redis.get(key)
    if not cart_data:
        return {"sessionId": session_id, "items": []}
    return json.loads(cart_data)


def clear_cart(session_id):
    redis.delete(get_cart_key(session_id))
