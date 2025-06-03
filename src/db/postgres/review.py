from db.postgres.connection_postgres import get_conn

def create_new_review(user_id, reviewed_user_id, reviewed_posting, rating, description):
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO user_reviews (user_id, reviewed_user_id, reviewed_posting, rating, description)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        str(user_id), 
                        str(reviewed_user_id), 
                        str(reviewed_posting), 
                        rating, 
                        description
                    )
                )

                review_id = cursor.fetchone()[0]
                conn.commit()

        return review_id
    except Exception as e:
        print(f"Error creating review: {e}")
        return None


def get_all_reviews_by_posting_id(posting_id):
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT 
                        id,
                        user_id,
                        reviewed_user_id,
                        reviewed_posting,
                        rating,
                        description,
                        created_at,
                        AVG(rating) OVER () AS avg_rating
                    FROM user_reviews
                    WHERE reviewed_posting = %s
                    """,
                    (str(posting_id),)
                )

                reviews = cursor.fetchall()

        if not reviews:
            return {"average_rating": None, "reviews": []}

        return {
            "average_rating": reviews[0][7], 
            "reviews": [
                {
                    'id': review[0], 
                    'seller_id': review[1], 
                    'reviewed_user_id': review[2], 
                    'reviewed_posting': review[3], 
                    'rating': review[4], 
                    'description': review[5],
                    'created_at': review[6]
                }
                for review in reviews
            ]
        }
    except Exception as e:
        print(f"Error fetching reviews: {e}")
        return None
    