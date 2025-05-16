from db.postgres.connection_postgres import get_db

def create_new_review(user_id, reviewed_user_id, reviewed_posting, rating, description):

    print(f"create_new_review: {user_id}, {reviewed_user_id}, {reviewed_posting}, {rating}, {description}")

    try:
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO user_reviews (user_id, reviewed_user_id, reviewed_posting, rating, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, reviewed_user_id, str(reviewed_posting), rating, description)
        )

        db.commit()
        cursor.close()
        db.close()
        return True
    except Exception as e:
        print(f"Error creating new review: {e}")
        return False
    