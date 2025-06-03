from db.postgres.connection_postgres import get_conn
import bcrypt


def create_user(email, name, password, is_company=False):
    print("Creating user in PostgreSQL")
    hashed_pw = hash_password(password)
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                insert_query = """
                INSERT INTO users (email, name, password, is_company)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """
                cursor.execute(insert_query, (email, name, hashed_pw, is_company))
                user_id = cursor.fetchone()[0]
            conn.commit()
        return user_id
    except Exception as e:
        print("Error creating user")
        return None


def login_user(email, password):
    print("Logging in user in PostgreSQL")
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                select_query = """
                SELECT id, name, password FROM users WHERE email = %s;
                """
                cursor.execute(select_query, (email,))
                user = cursor.fetchone()
                if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                    return user[0], user[1]
        return None
    except Exception as e:
        print(f"Error logging in user: {e}")
        return None


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def get_user_by_id(user_id):
    print("Getting user by ID in PostgreSQL")
    try:
        with get_conn() as conn:
            with conn.cursor() as cursor:
                select_query = """
                SELECT id, name, email FROM users WHERE id = %s;
                """
                cursor.execute(select_query, (user_id,))
                user = cursor.fetchone()
                if user:
                    return {
                        "id": user[0],
                        "name": user[1],
                        "email": user[2]
                    }
        return None
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None
    