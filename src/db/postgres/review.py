from db.postgres.connection_postgres import get_db

def create_new_review(user_id, reviewed_user_id, reviewed_posting, rating, description):

    try:
        db = get_db()
        cursor = db.cursor()

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
        db.commit()
        cursor.close()
        db.close()
        return review_id
    except Exception as e:
        print(f"Error creating review: {e}")
        return None
    