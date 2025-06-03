from db.postgres.connection_postgres import get_conn
import bcrypt


def create_user(email, name, password, is_company=False):
    print("Creating user in PostgreSQL")

    new_user = {
        "email": email,
        "name": name,
        "password": hash_password(password),
        "is_company": is_company
    }

    try:
        conn = get_conn()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO users (email, name, password, is_company)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        cursor.execute(insert_query, (new_user["email"], new_user["name"], new_user["password"], new_user["is_company"]))
        user_id = cursor.fetchone()[0]

        conn.commit()
        cursor.close()
        conn.close()

        return user_id
    except Exception as e:
        print(f"Error creating user: {e}")
        return None


def login_user(email, password):
    print("Logging in user in PostgreSQL")

    try:
        conn = get_conn()
        cursor = conn.cursor()

        select_query = """
        SELECT id, name, password FROM users WHERE email = %s;
        """
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            return user[0], user[1]
        else:
            return None
    except Exception as e:
        print(f"Error logging in user: {e}")
        return None


def hash_password(password):
    return bcrypt.hashpw(
        password.encode('utf-8'), 
        bcrypt.gensalt()
    ).decode('utf-8')


def get_user_by_id(user_id):
    print("Getting user by ID in PostgreSQL")

    try:
        conn = get_conn()
        cursor = conn.cursor()

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
        else:
            return None
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None
    