from db.postgres.connection_postgres import get_db

def create_new_review(user_id, posting_id, rating, review_text):
    print("Creating review in PostgreSQL")

    try:
        conn = get_db()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO reviews (user_id, posting_id, rating, review_text)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        cursor.execute(insert_query, (user_id, posting_id, rating, review_text))
        review_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return review_id
    except Exception as e:
        print(f"Error creating review: {e}")
        return None
    