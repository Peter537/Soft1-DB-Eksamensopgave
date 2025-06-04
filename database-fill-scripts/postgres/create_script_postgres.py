import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import bcrypt
import os

DEFAULT_PASSWORD =  "password123"
BCRYPT_PASSWORD = bcrypt.hashpw(DEFAULT_PASSWORD.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_for_connection():
    try:
        conn = psycopg2.connect(
            dbname="ExamDB",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        print("PostgreSQL connection successful.")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
    

def create_postgres_tables(cur):
    cur.execute("DROP TABLE IF EXISTS user_reviews;")
    cur.execute("DROP TABLE IF EXISTS users;")

    create_users = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL UNIQUE,
        name VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        is_company BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    create_user_reviews = """
    CREATE TABLE IF NOT EXISTS user_reviews (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        reviewed_user_id INTEGER REFERENCES users(id),
        reviewed_posting VARCHAR NOT NULL,
        rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cur.execute(create_users)
    cur.execute(create_user_reviews)
    print("Tables created successfully in PostgreSQL.")


def normal_users(cur, path='../datasets/users/names.txt'):
    if not os.path.isfile(path):
        print(f"User names file not found: {path}")
        return
    
    df = pd.read_csv(path, sep='\t', skiprows=8, header=None, names=['name', 'gender'])
    df = df.drop("gender", axis=1).drop_duplicates(subset=['name'])
    
    user_data = [
        (
            name.lower().replace(" ", "") + "@example.com",
            name,
            BCRYPT_PASSWORD
        )
        for name in df['name']
    ]
    
    insert_query = """
    INSERT INTO users (email, name, password)
    VALUES %s
    ON CONFLICT (email) DO NOTHING;
    """
    execute_values(cur, insert_query, user_data)
    print("All normal users created successfully.")


def company_users(cur, path='../datasets/users/company_names.csv'):
    if not os.path.isfile(path):
        print(f"Company names file not found: {path}")
        return
    
    df = pd.read_csv(path)[['Company Name']].drop_duplicates()
    
    company_data = [
        (
            name.lower().replace(" ", "") + "@company.com",
            name,
            BCRYPT_PASSWORD,
            True
        )
        for name in df['Company Name']
    ]

    insert_query = """
    INSERT INTO users (email, name, password, is_company)
    VALUES %s
    ON CONFLICT (email) DO NOTHING;
    """
    execute_values(cur, insert_query, company_data)
    print("All company users created successfully.")


def run_all_scripts():
    conn = check_for_connection()
    if not conn:
        return
    try:
        with conn:
            with conn.cursor() as cur:
                create_postgres_tables(cur)
                normal_users(cur)
                company_users(cur)

        print("All PostgreSQL data inserted and connection closed.")
        print("---------------------------------------- \n")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()