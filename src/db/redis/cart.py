import json
from db.redis.connection_redis import get_redis_client

CART_EXPIRE_SECONDS = 3600

conn = get_redis_client()

def get_cart_key(session_id):
    return f"cart:{session_id}"


def add_to_cart(title, session_id, posting_id, quantity, price):
    key = get_cart_key(session_id)
    posting_id = str(posting_id)
    quantity = int(quantity)

    with conn.pipeline() as pipe:
        while True:
            try:
                pipe.watch(key)
                cart_json = pipe.get(key)
                if cart_json:
                    cart = json.loads(cart_json)
                else:
                    cart = {"sessionId": session_id, "items": []}

                for item in cart["items"]:
                    if item["postingId"] == posting_id:
                        item["quantity"] += quantity
                        break
                else:
                    cart["items"].append({
                        "title": title,
                        "postingId": posting_id,
                        "quantity": quantity,
                        "price": price
                    })
                pipe.multi()
                pipe.set(key, json.dumps(cart), ex=CART_EXPIRE_SECONDS)
                pipe.execute()
                break
            except conn.WatchError:
                continue


def remove_from_cart(session_id, posting_id):
    key = get_cart_key(session_id)
    posting_id = str(posting_id)
    with conn.pipeline() as pipe:
        while True:
            try:
                pipe.watch(key)
                cart_data = pipe.get(key)
                if not cart_data:
                    pipe.unwatch()
                    return
                cart = json.loads(cart_data)
                cart["items"] = [item for item in cart["items"] if item["postingId"] != posting_id]
                pipe.multi()
                pipe.set(key, json.dumps(cart), ex=CART_EXPIRE_SECONDS)
                pipe.execute()
                break
            except conn.WatchError:
                continue


def get_cart(session_id):
    key = get_cart_key(session_id)
    cart_data = conn.get(key)
    if not cart_data:
        return {"sessionId": session_id, "items": []}
    return json.loads(cart_data)


def clear_cart(session_id):
    conn.delete(get_cart_key(session_id))
